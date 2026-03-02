import matplotlib.pyplot as plt
import numpy as np
import os
import re
from scipy.optimize import curve_fit

def parse_dwuck_output(filename):
    states = {}
    current_ex = None
    angles = []
    xsecs = []
    capture_data = False
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        if "10Be(d,p)" in line and "keV" in line:
            if current_ex is not None and angles:
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
                
    if current_ex is not None and angles:
        states[current_ex] = (np.array(angles), np.array(xsecs))
        
    return states

def linear_model(x, m, b):
    return m * x + b

def main():
    filename = "outputs/DW_10Be_DP_AK_ExScan.out"
    base_path = "/Users/calemhoffman/Documents/GitHub/DWUCK4/"
    path = os.path.join(base_path, filename)
    
    if not os.path.exists(path):
        print(f"Error: {path} not found.")
        return

    states = parse_dwuck_output(path)
    
    # Load 1.78 MeV state as reference
    ref_path = os.path.join(base_path, "outputs/DW_10Be_DP_AK_Ex178.out")
    if not os.path.exists(ref_path):
        print(f"Error: {ref_path} not found.")
        return
    ref_states = parse_dwuck_output(ref_path)
    if 1780 not in ref_states:
        print(f"Error: Reference state (1780 keV) not found in {ref_path}.")
        return
        
    ang178, xs178 = ref_states[1780]
    
    ex_energies_kev = sorted([e for e in states.keys() if isinstance(e, int)])
    ex_energies_mev = np.array(ex_energies_kev) / 1000.0
    
    ranges = [(0, 10), (15, 35)]
    colors = ['blue', 'red']
    
    plt.figure(figsize=(10, 6))
    
    for (min_ang, max_ang), color in zip(ranges, colors):
        factors = []
        for ex in ex_energies_kev:
            ang, xs = states[ex]
            
            mask_ex = (ang >= min_ang) & (ang <= max_ang)
            common_ang = ang[mask_ex]
            common_xs = xs[mask_ex]
            
            # Reference counts in the same angular range
            mask_178 = (ang178 >= min_ang) & (ang178 <= max_ang)
            common_178_xs = xs178[mask_178]
            
            # Normalize to integrated counts (sum of cross sections)
            norm_factor = np.sum(common_178_xs) / np.sum(common_xs)
            factors.append(norm_factor)
            
        factors = np.array(factors)
        
        # Linear fit
        popt, pcov = curve_fit(linear_model, ex_energies_mev, factors)
        m, b = popt
        fit_y = linear_model(ex_energies_mev, m, b)
        
        # Plot data
        label = f"Range: {min_ang}-{max_ang}°"
        plt.scatter(ex_energies_mev, factors, color=color, label=label, s=50, zorder=5)
        
        # Plot fit
        fit_label = f"Fit: y = {m:.4f}x + {b:.4f}"
        plt.plot(ex_energies_mev, fit_y, color=color, linestyle='--', label=fit_label, alpha=0.7)

    plt.xlabel("Excitation Energy $E_x$ (MeV)", fontsize=12)
    plt.ylabel("Scale Factor (to $E_x = 1.78$ MeV)", fontsize=12)
    plt.title("Unbound DWUCK4: Scale Factors vs. Excitation Energy\n(Relative to Integrated Counts of $E_x = 1.78$ MeV)", fontsize=14)
    plt.legend(fontsize='medium')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output_png = os.path.join(base_path, "outputs/ScaleFactors_vs_Ex.png")
    plt.savefig(output_png, dpi=300)
    print(f"Plot saved to {output_png}")

if __name__ == "__main__":
    main()
