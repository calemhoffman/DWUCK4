import matplotlib.pyplot as plt
import re
import sys
import numpy as np

def parse_dwuck_output(filename):
    """
    Parse DWUCK4 output to extract cross sections for each state.
    Returns a dict: {excitation_energy: (angles, cross_sections)}
    """
    states = {}
    current_ex = None
    angles = []
    xsecs = []
    capture_data = False
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        # Check for new state header
        # Line format often: 1001... 36S(d,p)...  1000 keV ...
        if "36S(d,p)" in line and "keV" in line:
            # If we were capturing, save previous state
            if current_ex is not None and angles:
                states[current_ex] = (np.array(angles), np.array(xsecs))
                angles = []
                xsecs = []
            
            # Extract Ex
            try:
                # "   1000 keV"
                parts = line.split("keV")[0].strip().split()
                ex_kev_str = parts[-1]
                current_ex = int(ex_kev_str) / 1000.0 # to MeV
            except:
                pass
            capture_data = False
            
        if "Tot-sig" in line:
            capture_data = False
            continue

        # Check for cross section data block start
        if "Theta" in line and "Inelsig" in line:
            capture_data = True
            continue
            
        if capture_data:
            # Data lines: Angle  Inelsig ...
            # 10.00    1.234E-01
            try:
                parts = line.strip().split()
                if len(parts) >= 2:
                     # Check if first part is a number
                     try:
                        ang = float(parts[0])
                        xs = float(parts[1]) # Inelsig is col 1
                     except ValueError:
                        # Skip non-numeric lines (like other headers)
                        continue
                        
                     angles.append(ang)
                     xsecs.append(xs)
            except ValueError:
                pass
                
    # Save last state
    if current_ex is not None and angles:
        states[current_ex] = (np.array(angles), np.array(xsecs))
        
    return states

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tools/plot_scan_overlay.py outputs/36S_scan_7MeV.out")
        sys.exit(1)
        
    filename = sys.argv[1]
    states = parse_dwuck_output(filename)
    
    if not states:
        print("No states found in output.")
        sys.exit(1)
        
    plt.figure(figsize=(10, 8))
    
    # Sort by Ex
    sorted_ex = sorted(states.keys())
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(sorted_ex)))
    
    for i, ex in enumerate(sorted_ex):
        ang, xs = states[ex]
        label = f"Ex = {ex:.1f} MeV"
        plt.plot(ang, xs, label=label, color=colors[i], linewidth=2)
        
    plt.xlabel("CM Angle (deg)")
    plt.ylabel("Cross Section (mb/sr)")
    plt.title("36S(d,p) Cross Section vs Excitation Energy (L=3, 0f7/2)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    
    output_png = filename.replace('.out', '_overlay.png')
    plt.savefig(output_png, dpi=300)
    print(f"Plot saved to {output_png}")

if __name__ == "__main__":
    main()
