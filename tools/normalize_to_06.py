
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
    
    if 600 not in states:
        print(f"Error: Reference state (600 keV) not found. Found: {list(states.keys())}")
        return
        
    ang06, xs06 = states[600]
    
    # Sort Ex energies
    ex_energies = sorted([e for e in states.keys() if isinstance(e, int)])
    
    plt.figure(figsize=(12, 8))
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(ex_energies)))
    factors = {}

    for i, ex in enumerate(ex_energies):
        ang, xs = states[ex]
        
        # Range check (15 - 35 degrees) for normalization
        mask_ex = (ang >= 15) & (ang <= 35)
        
        # Interpolate xs06 to current angles to be safe (though they should match)
        common_ang = ang[mask_ex]
        common_xs = xs[mask_ex]
        ref_xs_interp = np.interp(common_ang, ang06, xs06)
        
        # Minimize (Factor * xs - ref_xs)^2
        # Factor = sum(xs * ref_xs) / sum(xs^2)
        # But user wants to scale TO 0.6 MeV, so ref_xs is the target.
        # Factor * xs = ref_xs
        norm_factor = np.sum(common_xs * ref_xs_interp) / np.sum(common_xs**2)
        factors[ex] = norm_factor
        
        label = f"Ex = {ex/1000:.1f} MeV (x{norm_factor:.3f})"
        if ex == 600:
             plt.plot(ang, xs * norm_factor, '-', color='black', label=f"Ref: 0.6 MeV", linewidth=3, zorder=10)
        else:
             plt.plot(ang, xs * norm_factor, color=colors[i], label=label, alpha=0.8)

    plt.axvspan(15, 35, color='gray', alpha=0.1, label='Norm Range (15-35°)')
    
    plt.xlabel("Center-of-Mass Angle (deg)", fontsize=12)
    plt.ylabel("Normalized Cross Section (mb/sr)", fontsize=12)
    plt.title("10Be(d,p)11Be: All States Normalized to Ex = 0.6 MeV\n(Reference region: 15-35°)", fontsize=14)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    plt.xlim(0, 60)
    plt.tight_layout()
    
    output_png = os.path.join(base_path, "outputs/Normalization_to_06MeV.png")
    plt.savefig(output_png, dpi=300)
    print(f"Combined normalization plot saved to {output_png}")
    
    print("\nNormalization Factors (Factor * Ex_state = 0.6_MeV_state):")
    for ex in ex_energies:
        print(f"Ex = {ex/1000:.1f} MeV: {factors[ex]:.4f}")

if __name__ == "__main__":
    main()
