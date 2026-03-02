
import matplotlib.pyplot as plt
import numpy as np
import os
import re

def parse_dwuck_output(filename):
    """
    Parse DWUCK4 output to extract cross sections for each state.
    Returns a list of tuples: (ex_kev, angles, cross_sections)
    """
    results = []
    current_ex = None
    angles = []
    xsecs = []
    capture_data = False
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        # Check for 10Be(d,p) header
        # Header: 10Be(d,p)11Be  600 keV  1780 keV  0d5/2 unbound AK
        if "10Be(d,p)" in line and "keV" in line:
            # If we were capturing, save previous state
            if angles:
                results.append((current_ex, np.array(angles), np.array(xsecs)))
                angles = []
                xsecs = []
            
            # Extract excitation energy in keV
            # Look for the first "keV" occurrence and the number preceding it
            match = re.search(r"(\d+)\s+keV", line)
            if match:
                current_ex = int(match.group(1))
            else:
                current_ex = "Unknown"
            
            capture_data = False
            
        if "Tot-sig" in line:
            capture_data = False
            continue

        # Check for cross section data block start
        if "Theta" in line and "Inelsig" in line:
            capture_data = True
            continue
            
        if capture_data:
            parts = line.strip().split()
            if len(parts) >= 2:
                try:
                    ang = float(parts[0])
                    # Handle E notation or simple float
                    xs_str = parts[1].replace('E', 'e')
                    xs = float(xs_str)
                    angles.append(ang)
                    xsecs.append(xs)
                except ValueError:
                    continue
                
    # Save last state
    if angles:
        results.append((current_ex, np.array(angles), np.array(xsecs)))
        
    return results

def main():
    filenames = [
        "outputs/DW_10Be_DP_AK_all.out",
        "outputs/DW_10Be_DP_AK_ExScan.out"
    ]
    
    base_path = "/Users/calemhoffman/Documents/GitHub/DWUCK4/"
    
    all_results = []
    
    for fname in filenames:
        path = fname
        if not os.path.exists(path):
            path = os.path.join(base_path, fname)
        
        if os.path.exists(path):
            print(f"Parsing {path}...")
            all_results.extend(parse_dwuck_output(path))
        else:
            print(f"Warning: {path} not found.")

    if not all_results:
        print("No cross section data found in the output files.")
        return
        
    plt.figure(figsize=(10, 7))
    
    # Sort all results by excitation energy
    # Note: Some might be "Unknown" if regex fails, treat as 0
    all_results.sort(key=lambda x: x[0] if isinstance(x[0], int) else 0)
    
    # Use a colormap
    colors = plt.cm.plasma(np.linspace(0, 0.9, len(all_results)))
    
    for i, (ex_kev, ang, xs) in enumerate(all_results):
        label = f"Ex = {ex_kev/1000:.2f} MeV"
        plt.plot(ang, xs, label=label, color=colors[i], linewidth=2)
        
    plt.xlabel("Center-of-Mass Angle (deg)", fontsize=12)
    plt.ylabel("Cross Section (mb/sr)", fontsize=12)
    plt.title("10Be(d,p)11Be Combined Energy Scan", fontsize=14)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
    plt.grid(True, alpha=0.3, which='both')
    plt.yscale('log')
    plt.xlim(0, 60)
    
    plt.tight_layout()
    
    output_png = os.path.join(base_path, "outputs/DW_10Be_DP_AK_ExScan_Combined.png")
    plt.savefig(output_png, dpi=300)
    print(f"Plot saved to {output_png}")
    
    # Interactive plot
    try:
        import plotly.graph_objects as go
        fig = go.Figure()
        for i, (ex_kev, ang, xs) in enumerate(all_results):
            fig.add_trace(go.Scatter(x=ang, y=xs, name=f"{ex_kev/1000:.2f} MeV"))
        fig.update_layout(
            title="10Be(d,p)11Be Combined Energy Scan",
            xaxis_title="Angle (deg)",
            yaxis_title="Cross Section (mb/sr)",
            yaxis_type="log"
        )
        output_html = output_png.replace('.png', '.html')
        fig.write_html(output_html)
        print(f"Interactive plot saved to {output_html}")
    except ImportError:
        pass

if __name__ == "__main__":
    main()
