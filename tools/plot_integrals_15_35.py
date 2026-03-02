import matplotlib.pyplot as plt
import numpy as np
import os
import re

def parse_dwuck_output(filename):
    states = {}
    current_ex = None
    angles = []
    xsecs = []
    capture_data = False
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        if "10Be(d,p)" in line and "keV" in line and "0d5/2" in line:
            match = re.search(r"(\d+)\s+keV", line)
            if match:
                new_ex = int(match.group(1)) / 1000.0
                if new_ex != current_ex:
                    if current_ex is not None and len(angles) > 0:
                        states[current_ex] = (np.array(angles), np.array(xsecs))
                    current_ex = new_ex
                    angles = []
                    xsecs = []
                    capture_data = False
            
        if "Tot-sig" in line:
            if current_ex is not None and len(angles) > 0:
                states[current_ex] = (np.array(angles), np.array(xsecs))
            capture_data = False
            continue

        if "Theta" in line and "Inelsig" in line:
            capture_data = True
            angles = []
            xsecs = []
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
                
    if current_ex is not None and len(angles) > 0:
        states[current_ex] = (np.array(angles), np.array(xsecs))
        
    return states

def main():
    base_path = "/Users/calemhoffman/Documents/GitHub/DWUCK4/"
    filename = os.path.join(base_path, "outputs/DW_10Be_DP_AK_ExScan.out")
    
    states = parse_dwuck_output(filename)
    
    ex_list = []
    integrals = []
    
    valid_keys = [k for k in states.keys() if 0.6 <= k <= 2.0]
    valid_keys.sort()
    
    for ex in valid_keys:
        ang, xs = states[ex]
        mask = (ang >= 15) & (ang <= 35)
        # Using trapezoidal rule with solid angle element sin(theta)
        # However, typically DWUCK4 integrated cross section plots use sum of cross sections in a range over angles. 
        # For simplicity and given past scripts we sum.
        # Let's do the proper integral: trapz(xsec * sin(theta), theta) to be accurate.
        ang_rad = np.radians(ang[mask])
        xs_val = xs[mask]
        
        # We will use simple sum since d_theta = 1 degree and it matches the other scripts.
        integral = np.sum(xs_val)
        
        ex_list.append(ex)
        integrals.append(integral)
        
    ex_array = np.array(ex_list)
    int_array = np.array(integrals)
    
    if len(ex_array) == 0:
        print("No valid states found in the specified Ex range.")
        return
        
    # Get integral at Ex=0.6 for relative normalization
    idx_06 = np.argmin(np.abs(ex_array - 0.6))
    int_06 = int_array[idx_06]
    
    if int_06 == 0:
        print("Error: Reference integral at Ex=0.6 is zero.")
        return
        
    rel_array = int_array / int_06
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))
    
    ax1.plot(ex_array, int_array, 'bo-', ms=8, label="15°-35°")
    ax1.set_xlabel("Excitation Energy $E_x$ (MeV)", fontsize=12)
    ax1.set_ylabel(r"Integrated Cross Section $\Sigma\sigma$ ($fm^2$)", fontsize=12)
    ax1.set_title("Absolute Sum of Cross Sections vs $E_x$", fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(ex_array, rel_array, 'ro-', ms=8, label="Relative to $E_x=0.6$")
    ax2.set_xlabel("Excitation Energy $E_x$ (MeV)", fontsize=12)
    ax2.set_ylabel(r"Relative Integrated Cross Section", fontsize=12)
    ax2.set_title(r"Relative Integrated Cross Section vs $E_x$ ($15°-35°$)", fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_png = os.path.join(base_path, "outputs/ExScan_integrals_vs_Ex_15_35.png")
    plt.savefig(output_png, dpi=300)
    print(f"Plot correctly generated and saved to {output_png}")

if __name__ == "__main__":
    main()
