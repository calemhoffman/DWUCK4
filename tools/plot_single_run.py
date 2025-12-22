import matplotlib.pyplot as plt
import sys
import numpy as np

def parse_dwuck_output(filename):
    """
    Parse DWUCK4 output to extract cross sections for each state.
    Returns a dict: {label: (angles, cross_sections)}
    """
    states = {}
    current_label = None
    angles = []
    xsecs = []
    capture_data = False
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        # Check for new state header
        # Use simple logic: if "36S(d,p)" and "bound ZR" or "unbound ZR"
        if "36S(d,p)" in line and ("bound ZR" in line or "unbound ZR" in line):
            # If we were capturing, save previous state
            if current_label is not None and angles:
                states[current_label] = (np.array(angles), np.array(xsecs))
                angles = []
                xsecs = []
            
            # Extract Label (entire line trimmed)
            current_label = line.strip()
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
            try:
                parts = line.strip().split()
                if len(parts) >= 2:
                     try:
                        ang = float(parts[0])
                        xs = float(parts[1]) # Inelsig is col 1
                     except ValueError:
                        continue
                     angles.append(ang)
                     xsecs.append(xs)
            except ValueError:
                pass
                
    # Save last state
    if current_label is not None and angles:
        states[current_label] = (np.array(angles), np.array(xsecs))
        
    return states

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tools/plot_single_run.py outputs/DW_36S_DP.out")
        sys.exit(1)
        
    filename = sys.argv[1]
    states = parse_dwuck_output(filename)
    
    if not states:
        print("No states found in output.")
        sys.exit(1)
        
    plt.figure(figsize=(10, 8))
    
    for i, (label, (ang, xs)) in enumerate(states.items()):
        # Shorten label for legend
        # "100100... 36S(d,p)... 0 keV 0f7/2 bound ZR" -> "0 keV 0f7/2"
        try:
            # Split on "MeV" to get the part after the reaction/energy
            # "100... 36S(d,p)@ 16MeV    0 keV ..." -> "0 keV ..."
            short_label = label.split("MeV")[1].strip()
        except:
            short_label = label[:20]
            
        plt.plot(ang, xs, label=short_label, linewidth=2)
        
    plt.xlabel("CM Angle (deg)")
    plt.ylabel("Cross Section (mb/sr)")
    plt.title("36S(d,p) Cross Section (DW_36S_DP.in)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    
    output_png = filename.replace('.out', '.png')
    plt.savefig(output_png, dpi=300)
    print(f"Plot saved to {output_png}")

if __name__ == "__main__":
    main()
