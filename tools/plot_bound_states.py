#!/usr/bin/env python3
"""
Plot all bound states from DWUCK4 output with individual subplots.
Usage:
    python tools/plot_bound_states.py outputs/36S_bound_states.out outputs/bound_states_plot.png
"""

import re
import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def parse_dwuck4_output(output_file):
    """
    Parse DWUCK4 output to extract angular distributions for each state.
    
    Returns:
        list of dict: Each dict contains {'title': str, 'theta': array, 'cross_section': array}
    """
    states = []
    
    with open(output_file, 'r') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Look for state title line (contains "36S(d,p)")
        if '36S(d,p)' in line:
            title = line.strip()
            
            # Extract excitation energy from title
            ex_match = re.search(r'(\d+)\s*keV', title)
            ex_kev = int(ex_match.group(1)) if ex_match else 0
            
            # Extract orbital info
            orbital_match = re.search(r'keV\s+(\S+)', title)
            orbital = orbital_match.group(1) if orbital_match else ''
            
            # Skip to the cross-section table (look for "Theta" header)
            j = i + 1
            while j < len(lines) and 'Theta' not in lines[j]:
                j += 1
            
            if j >= len(lines):
                i += 1
                continue
            
            # Skip the header line and any separator lines
            j += 1
            while j < len(lines) and not re.match(r'^\s*\d+\.\d+', lines[j]):
                j += 1
            
            # Now parse the data rows
            theta = []
            cross_section = []
            
            while j < len(lines):
                data_match = re.match(r'^\s*(\d+\.\d+)\s+([+-]?\d+\.\d+[Ee][+-]?\d+)', lines[j])
                if data_match:
                    theta.append(float(data_match.group(1)))
                    cross_section.append(float(data_match.group(2)))
                    j += 1
                else:
                    # End of this state's data
                    break
            
            if theta and cross_section:
                states.append({
                    'title': title.strip(),
                    'ex_kev': ex_kev,
                    'orbital': orbital,
                    'theta': np.array(theta),
                    'cross_section': np.array(cross_section)
                })
            
            i = j
        else:
            i += 1
    
    return states


def plot_bound_states(states, output_png):
    """
    Create a multi-panel plot with individual subplots for each state.
    """
    n_states = len(states)
    
    # Determine grid layout (aim for roughly square grid)
    ncols = int(np.ceil(np.sqrt(n_states)))
    nrows = int(np.ceil(n_states / ncols))
    
    # Create figure with subplots
    fig, axes = plt.subplots(nrows, ncols, figsize=(4*ncols, 3*nrows))
    
    # Flatten axes array for easier iteration
    if n_states == 1:
        axes = [axes]
    else:
        axes = axes.flatten()
    
    # Plot each state
    for idx, state in enumerate(states):
        ax = axes[idx]
        
        theta = state['theta']
        cs = state['cross_section']
        
        # Plot on log scale
        ax.semilogy(theta, cs, 'b-', linewidth=1.5, marker='o', markersize=3)
        
        # Labels and title
        ax.set_xlabel('θ (deg)', fontsize=9)
        ax.set_ylabel('dσ/dΩ (mb/sr)', fontsize=9)
        ax.set_title(f"{state['ex_kev']} keV, {state['orbital']}", fontsize=10, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.tick_params(labelsize=8)
        
        # Set reasonable y-axis limits
        if len(cs) > 0:
            ymin = np.min(cs[cs > 0]) if np.any(cs > 0) else 1e-6
            ymax = np.max(cs) if np.max(cs) > 0 else 1
            ax.set_ylim([ymin * 0.5, ymax * 2])
    
    # Hide any unused subplots
    for idx in range(n_states, len(axes)):
        axes[idx].axis('off')
    
    # Overall title
    fig.suptitle('³⁶S(d,p)³⁷S @ 8 MeV - Bound States Angular Distributions', 
                 fontsize=14, fontweight='bold', y=0.995)
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0, 1, 0.99])
    
    # Save figure
    output_path = Path(output_png)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_png, dpi=150, bbox_inches='tight')
    print(f"Saved plot to: {output_png}")
    
    return fig


def main():
    if len(sys.argv) != 3:
        print("Usage: python tools/plot_bound_states.py <output_file> <output_png>")
        print("\nExample:")
        print("  python tools/plot_bound_states.py outputs/36S_bound_states.out outputs/bound_states_plot.png")
        sys.exit(1)
    
    output_file = sys.argv[1]
    output_png = sys.argv[2]
    
    if not Path(output_file).exists():
        print(f"Error: Output file not found: {output_file}")
        sys.exit(1)
    
    print(f"Parsing DWUCK4 output: {output_file}")
    states = parse_dwuck4_output(output_file)
    
    if not states:
        print("Error: No states found in output file")
        sys.exit(1)
    
    print(f"Found {len(states)} states")
    for i, state in enumerate(states):
        print(f"  State {i+1}: {state['ex_kev']} keV, {state['orbital']}, {len(state['theta'])} angles")
    
    print(f"\nCreating plot...")
    plot_bound_states(states, output_png)
    print("Done!")


if __name__ == '__main__':
    main()
