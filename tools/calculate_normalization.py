
import matplotlib.pyplot as plt
import numpy as np
import os
import re

def parse_dwuck_output(filename):
    """
    Parse DWUCK4 output to extract cross sections for each state.
    Returns a dict: {ex_kev: (angles, cross_sections)}
    """
    states = {}
    current_ex = None
    angles = []
    xsecs = []
    capture_data = False
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        if "10Be(d,p)" in line and "keV" in line:
            if angles:
                states[current_ex] = (np.array(angles), np.array(xsecs))
                angles = []
                xsecs = []
            
            match = re.search(r"(\d+)\s+keV", line)
            if match:
                current_ex = int(match.group(1))
            else:
                current_ex = "Unknown"
            capture_data = False
            
        if "Tot-sig" in line:
            capture_data = False
            continue

        if "Theta" in line and "Inelsig" in line:
            capture_data = True
            continue
            
        if capture_data:
            parts = line.strip().split()
            if len(parts) >= 2:
                try:
                    ang = float(parts[0])
                    xs_str = parts[1].replace('E', 'e')
                    xs = float(xs_str)
                    angles.append(ang)
                    xsecs.append(xs)
                except ValueError:
                    continue
                
    if angles:
        states[current_ex] = (np.array(angles), np.array(xsecs))
        
    return states

def main():
    filename = "outputs/DW_10Be_DP_AK_ExScan.out"
    base_path = "/Users/calemhoffman/Documents/GitHub/DWUCK4/"
    path = os.path.join(base_path, filename)
    
    if not os.path.exists(path):
        print(f"Error: {path} not found.")
        return

    states = parse_dwuck_output(path)
    
    if 800 not in states or 1800 not in states:
        print(f"Error: Required states (800 keV or 1800 keV) not found. Found: {list(states.keys())}")
        return
        
    ang08, xs08 = states[800]
    ang18, xs18 = states[1800]
    
    # Range check (15 - 35 degrees)
    mask08 = (ang08 >= 15) & (ang08 <= 35)
    mask18 = (ang18 >= 15) & (ang18 <= 35)
    
    # Interpolation if needed of angles don't match exactly, but usually they do in DWUCK
    # Let's assume they match for simplicity, or interpolate xs08 to ang18
    common_ang = ang18[mask18]
    common_xs18 = xs18[mask18]
    common_xs08 = np.interp(common_ang, ang08, xs08)
    
    # Calculate normalization factor: Factor * xs08 = xs18 (on average)
    # We want to minimize (Factor * xs08 - xs18)^2
    # Factor = sum(xs08 * xs18) / sum(xs08^2)
    norm_factor = np.sum(common_xs08 * common_xs18) / np.sum(common_xs08**2)
    
    print(f"Normalization Factor (0.8 MeV Normalized to 1.8 MeV): {norm_factor:.4f}")
    
    plt.figure(figsize=(10, 7))
    plt.plot(ang18, xs18, 'b-', label='1.8 MeV state', linewidth=2)
    plt.plot(ang08, xs08 * norm_factor, 'r--', label=f'0.8 MeV state (scaled by {norm_factor:.4f})', linewidth=2)
    plt.plot(ang08, xs08, 'r:', label='0.8 MeV state (original)', alpha=0.3)
    
    # Highlight fit range
    plt.axvspan(15, 35, color='gray', alpha=0.1, label='Normalization Range (15-35°)')
    
    plt.xlabel("Center-of-Mass Angle (deg)", fontsize=12)
    plt.ylabel("Cross Section (mb/sr)", fontsize=12)
    plt.title(f"10Be(d,p)11Be Normalization: 0.8 MeV vs 1.8 MeV\nScale Factor = {norm_factor:.4f}", fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    plt.xlim(0, 60)
    
    output_png = os.path.join(base_path, "outputs/Normalization_08_to_18.png")
    plt.savefig(output_png, dpi=300)
    print(f"Normalization plot saved to {output_png}")

if __name__ == "__main__":
    main()
