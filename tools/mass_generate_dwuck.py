#!/usr/bin/env python3.11
import os
import re
import subprocess
import shutil

# Configuration
STATES_LIST = "/Users/calemhoffman/Documents/GitHub/digios_crh/analysis/working/s36dp_files/states_list.txt"
BASE_DIR = "/Users/calemhoffman/Documents/GitHub/manuscripts/manuscripts/s36/dwba/"
DWUCK4_EXE = "/Users/calemhoffman/Documents/GitHub/DWUCK4/DWUCK4.exe"
LOCAL_INPUTS = "/Users/calemhoffman/Documents/GitHub/DWUCK4/inputs/"
LOCAL_OUTPUTS = "/Users/calemhoffman/Documents/GitHub/DWUCK4/outputs/"

# Conversion factors
def get_dwuck_xsec_scaling(wsi_ptolemy, asi_ptolemy):
    # Wsᵢ(DWUCK) = Wsᵢ(PTOLEMY) × 4 × asᵢ
    return wsi_ptolemy * 4.0 * asi_ptolemy

def get_dwuck_vso_scaling(vso_ptolemy):
    # Vso(DWUCK) = Vso(PTOLEMY) × 4
    return vso_ptolemy * 4.0

def f8(val):
    """Formats a value into a strict 8-character field."""
    if val is None:
        return "        "
    if isinstance(val, str):
        # Already formatted or a label
        return val.ljust(8)[:8]
    s = f"{val:+.3f}"
    if len(s) > 8: s = f"{val:+.2f}"
    if len(s) > 8: s = f"{val:+.1f}"
    return s.ljust(8)

def parse_ptolemy_in(filepath):
    """
    Parses a PTOLEMY .in.a file and returns a list of configurations.
    """
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Split by headers
    # Each block starts with a comment line $==== Ex=...
    blocks = re.split(r'(\$={10,}.*?\n)', content)
    configs = []
    
    current_header = ""
    for i in range(1, len(blocks), 2):
        header = blocks[i]
        body = blocks[i+1] if i+1 < len(blocks) else ""
        
        if "REACTION:" not in body:
            continue
            
        config = {}
        # Parse header: Ex=2.023(0f7/2)AK
        comment_match = re.search(r'Ex=([0-9.]+)\((.*?)\)(AK|QP)', header)
        if comment_match:
            config['ex_val'] = comment_match.group(1)
            config['orbital'] = comment_match.group(2)
            config['omp_set'] = comment_match.group(3)
        else:
            config['ex_val'] = "unknown"
            config['orbital'] = "unknown"
            config['omp_set'] = "AK" if "AK" in header else "QP"

        # Target section (Bound state)
        target_match = re.search(r'TARGET\nJBIGA=.*?\nnodes=([0-9]+) l=([0-9]+) jp=(.*?)\s', body)
        if target_match:
            config['nodes'] = int(target_match.group(1))
            config['l'] = int(target_match.group(2))
            config['jp'] = target_match.group(3)
            
        # Potentials
        def get_pot(section_name):
            match = re.search(section_name + r'.*?\nv\s*=\s*([0-9.]+)\s*r0\s*=\s*([0-9.]+)\s*a\s*=\s*([0-9.]+)\nvi\s*=\s*([0-9.]+)\s*ri0\s*=\s*([0-9.]+)\s*ai\s*=\s*([0-9.]+)\nvsi\s*=\s*([0-9.]+)\s*rsi0\s*=\s*([0-9.]+)\s*asi\s*=\s*([0-9.]+)\nvso\s*=\s*([0-9.]+)\s*rso0\s*=\s*([0-9.]+)\s*aso\s*=\s*([0-9.]+)\nvsoi\s*=\s*([0-9.-]+)\s*rsoi0\s*=\s*([0-9.]+)\s*asoi\s*=\s*([0-9.]+)\s*rc0\s*=\s*([0-9.]+)', body, re.DOTALL)
            if match:
                return [float(x) for x in match.groups()]
            return None

        config['incoming'] = get_pot("INCOMING")
        config['outgoing'] = get_pot("OUTGOING")
            
        if config['incoming'] and config['outgoing']:
            configs.append(config)
    return configs

def generate_dwuck_input(config):
    """
    Generates DWUCK4 input string from config.
    """
    ex = float(config['ex_val'])
    orbital = config['orbital']
    omp = config['omp_set']
    nodes = config['nodes']
    l_trans = config['l']
    jp_str = config['jp']
    num_j = float(re.findall(f'[0-9.]+', jp_str)[0])
    two_j = int(num_j * 2)
    
    q_val = 2.079 - ex
    bind_val = -4.304 + ex
    
    # Title - Fixed width 80 chars total
    title_text = f"36S(d,p)@{int(ex*1000):04}keV L={l_trans} J={jp_str} {orbital} {omp}"
    title = f"1001000000200000    {title_text:60}"[:80]
    lines = [title]
    
    # Card 2: Angles
    lines.append(f"{f8(60.)}{f8(0.)}{f8(1.)}")
    
    # Card 3: Quantum numbers (+30+01+LL+JJ)
    lines.append(f"+30+01+{l_trans:02}{two_j:02}")
    
    # Card 4: Integration
    lines.append(f"{f8(0.1)}{f8(0.)}{f8(50.)}")
    
    # Deuteron channel (Incoming)
    inc = config['incoming']
    v, r0, a, vi, ri0, ai, vsi, rsi0, asi, vso, rso0, aso, vsoi, rsoi0, asoi, rc0 = inc
    
    # Card 5
    lines.append(f"{f8(16.0)}{f8(2.0)}{f8(1.0)}{f8(36.0)}{f8(16.0)}{f8(rc0)}{f8(None)}{f8(2.0)}")
    
    # Card 6
    lines.append(f"+1.     {f8(-v)}{f8(r0)}{f8(a)}{f8(None)}{f8(-vi)}{f8(ri0)}{f8(ai)}")
    
    # Card 7
    ws_dwuck = vsi * 4.0 * asi
    lines.append(f"+2.     {f8(0.)}{f8(0.)}{f8(0.)}{f8(None)}{f8(ws_dwuck)}{f8(rsi0)}{f8(asi)}")
    
    # Card 8
    vso_dwuck = vso * 4.0
    lines.append(f"-4.     {f8(-vso_dwuck)}{f8(rso0)}{f8(aso)}{f8(None)}{f8(0.)}{f8(0.)}{f8(0.)}")
    
    # Proton channel (Outgoing)
    out = config['outgoing']
    v, r0, a, vi, ri0, ai, vsi, rsi0, asi, vso, rso0, aso, vsoi, rsoi0, asoi, rc0 = out
    
    # Card 9
    lines.append(f"{f8(q_val)}{f8(1.0)}{f8(1.0)}{f8(37.0)}{f8(16.0)}{f8(rc0)}{f8(None)}{f8(1.0)}")
    
    # Card 10
    lines.append(f"+1.     {f8(-v)}{f8(r0)}{f8(a)}{f8(None)}{f8(-vi)}{f8(ri0)}{f8(ai)}")
    
    # Card 11
    ws_dwuck = vsi * 4.0 * asi
    lines.append(f"+2.     {f8(0.)}{f8(0.)}{f8(0.)}{f8(None)}{f8(ws_dwuck)}{f8(rsi0)}{f8(asi)}")
    
    # Card 12
    vso_dwuck = vso * 4.0
    wsoi_dwuck = abs(vsoi) * 4.0
    lines.append(f"-4.     {f8(-vso_dwuck)}{f8(rso0)}{f8(aso)}{f8(None)}{f8(wsoi_dwuck)}{f8(rsoi0)}{f8(asoi)}")
    
    # Bound state (Particle 3)
    # Card 13
    lines.append(f"{f8(-abs(bind_val))}{f8(1.0)}{f8(0.0)}{f8(36.0)}{f8(16.0)}{f8(1.30)}{f8(None)}{f8(1.0)}")
    
    # Card 14
    # Geometry from target: r0=1.25, a=0.65, V=search, Vso=6, rso=1.1, aso=0.65
    lines.append(f"-1.     -1.     {f8(1.25)}{f8(0.65)}36.439  {f8(1.10)}{f8(0.65)}")
    
    # Card 15
    # Nodes, L, 2J
    lines.append(f"{f8(float(nodes))}{f8(float(l_trans))}{f8(float(two_j))}{f8(1.0)}{f8(50.0)}")
    
    # Card 16: End marker
    lines.append("9                   END OF DATA for DWUCK4")
    
    return "\n".join(lines)
    
    return "\n".join(lines)

def run_dwuck(input_str, out_path):
    proc = subprocess.Popen([DWUCK4_EXE], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = proc.communicate(input=input_str)
    with open(out_path, 'w') as f:
        f.write(stdout)
        if stderr:
            f.write("\nSTDERR:\n" + stderr)
    return proc.returncode == 0

def process_all():
    with open(STATES_LIST, 'r') as f:
        lines = f.readlines()
    
    processed_dirs = set()
    
    for line in lines:
        line = line.strip()
        if not line or "&" not in line:
            continue
        
        # Energy is the first field
        parts = line.replace('#', '').split('&')
        energy_str = parts[0].strip()
        try:
            energy = float(energy_str)
        except ValueError:
            continue
            
        # Map to directory
        dir_name = "ex" + f"{int(energy*100):03}" # floor(E*100) or similar? 
        # Check if dir_name corrected: 0.646 -> ex064, 1.398 -> ex139, 1.992 -> ex199
        # Actually it's more like ex + first two digits after decimal?
        # Let's try to match existing dirs
        dir_path = os.path.join(BASE_DIR, dir_name)
        if not os.path.exists(dir_path):
            # Try leading zero: 
            dir_name = "ex" + f"{int(energy*100):03}"
            dir_path = os.path.join(BASE_DIR, dir_name)
            if not os.path.exists(dir_path):
                print(f"Skipping {energy_str} - {dir_name} not found")
                continue

        if dir_name in processed_dirs:
            # We already parsed the .in file in this dir
            continue
        processed_dirs.add(dir_name)
        
        in_file = os.path.join(dir_path, "ptolemy", f"s36dp_{dir_name}.in.a")
        if not os.path.exists(in_file):
            print(f"File {in_file} not found")
            continue
            
        print(f"Processing {dir_name}...")
        configs = parse_ptolemy_in(in_file)
        
        target_dwuck_dir = os.path.join(dir_path, "dwuck")
        os.makedirs(target_dwuck_dir, exist_ok=True)
        
        for config in configs:
            omp = config['omp_set']
            orbital = config['orbital'].replace('/', '').replace('+', '').replace('-', '')
            
            dwuck_input = generate_dwuck_input(config)
            
            in_filename = f"DW_36S_DP_{omp}_{dir_name}_{orbital}.in"
            out_filename = f"DW_36S_DP_{omp}_{dir_name}_{orbital}.out"
            
            # Save locally for running
            local_in = os.path.join(LOCAL_INPUTS, in_filename)
            with open(local_in, 'w') as f:
                f.write(dwuck_input)
            
            # Run
            local_out = os.path.join(LOCAL_OUTPUTS, out_filename)
            success = run_dwuck(dwuck_input, local_out)
            
            if success:
                # Copy to target
                shutil.copy(local_in, os.path.join(target_dwuck_dir, in_filename))
                shutil.copy(local_out, os.path.join(target_dwuck_dir, out_filename))
                print(f"  Generated {in_filename} and {out_filename}")
            else:
                print(f"  Failed running {in_filename}")

if __name__ == "__main__":
    process_all()
