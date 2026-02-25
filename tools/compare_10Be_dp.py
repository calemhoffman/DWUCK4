#!/usr/bin/env python3.11
"""
Compare DWUCK4 and Ptolemy cross sections for 10Be(d,p)11Be
all AK states (Ex=0, 0.1, 0.2, 0.3, 0.4 MeV).
Raw data — no normalization, no unit conversion.
  DWUCK4  outputs in fm²/sr
  Ptolemy outputs in mb/sr
"""

import numpy as np
import matplotlib.pyplot as plt
import re


def parse_dwuck4_multistate(filepath):
    """Parse DWUCK4 output with multiple states. Returns list of (angles, xs_fm2)."""
    states = []
    current_angles, current_xs = [], []
    in_data = False

    with open(filepath, 'r') as f:
        for line in f:
            if 'Inelsig,fm**2' in line:
                if current_angles:
                    states.append((np.array(current_angles), np.array(current_xs)))
                    current_angles, current_xs = [], []
                in_data = True
                continue
            if 'Tot-sig' in line:
                in_data = False
                continue
            if in_data:
                m = re.match(r'\s+(\d+\.\d+)\s+([0-9.Ee+\-]+)\s+', line)
                if m:
                    current_angles.append(float(m.group(1)))
                    current_xs.append(float(m.group(2)))
    if current_angles:
        states.append((np.array(current_angles), np.array(current_xs)))
    return states


def parse_ptolemy_xsec(filepath, columns):
    """Parse Ptolemy Xsec file for multiple columns."""
    results = {c: ([], []) for c in columns}
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#') or line.strip() == '' or 'Angel' in line:
                continue
            parts = line.split()
            for c in columns:
                if len(parts) > c:
                    try:
                        results[c][0].append(float(parts[0]))
                        results[c][1].append(float(parts[c]))
                    except ValueError:
                        pass
    return {c: (np.array(a), np.array(x)) for c, (a, x) in results.items()}


def main():
    dwuck_file  = '/Users/calemhoffman/Documents/GitHub/DWUCK4/outputs/DW_10Be_DP_AK_all.out'
    ptolemy_file = '/Users/calemhoffman/Documents/GitHub/DWUCK4/ptolemy/be10dp_ell2_boundapp.Xsec.txt.a'
    output_plot  = '/Users/calemhoffman/Documents/GitHub/DWUCK4/outputs/comparison_10Be_dp_all_AK.png'

    # State labels and Ptolemy column indices (1-indexed: cols 1-5 = AK states)
    labels = ['Ex=0', 'Ex=0.1', 'Ex=0.2', 'Ex=0.3', 'Ex=0.4']
    pt_cols = [1, 2, 3, 4, 5]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    # Parse data
    dw_states = parse_dwuck4_multistate(dwuck_file)
    pt_data = parse_ptolemy_xsec(ptolemy_file, pt_cols)

    print(f"DWUCK4: {len(dw_states)} states parsed")
    print(f"Ptolemy: {len(pt_cols)} columns parsed")

    # --- Plot ---
    fig, ax1 = plt.subplots(figsize=(10, 7))
    ax2 = ax1.twinx()

    for i, (label, col, color) in enumerate(zip(labels, pt_cols, colors)):
        pt_ang, pt_xs = pt_data[col]
        dw_ang, dw_xs = dw_states[i]

        ax1.plot(pt_ang, pt_xs, '-', color=color, lw=2.0,
                 label=f'Ptolemy {label}')
        ax2.plot(dw_ang, dw_xs, '--', color=color, lw=2.0, alpha=0.7,
                 label=f'DWUCK4 {label}')

        print(f"  {label}: Ptolemy={pt_xs[0]:.2f} mb/sr, DWUCK4={dw_xs[0]:.4f} fm²/sr, "
              f"ratio={pt_xs[0]/dw_xs[0]:.3f}")

    ax1.set_xlabel(r'$\theta_{\rm c.m.}$ (deg)', fontsize=13)
    ax1.set_ylabel(r'd$\sigma$/d$\Omega$  [mb/sr]  (Ptolemy, solid)', fontsize=13, color='#1f77b4')
    ax2.set_ylabel(r'd$\sigma$/d$\Omega$  [fm$^2$/sr]  (DWUCK4, dashed)', fontsize=13, color='#d62728')

    ax1.set_title(r'$^{10}$Be(d,p)$^{11}$Be   (0d$_{5/2}$)   $E_{\rm lab}=17.4$ MeV'
                  '\nAll AK states — Raw data, no normalization',
                  fontsize=14, fontweight='bold')

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=9,
               loc='upper right', ncol=2)

    ax1.set_xlim(-1, 62)
    ax1.grid(True, alpha=0.3)
    fig.tight_layout()
    plt.savefig(output_plot, dpi=200, bbox_inches='tight')
    print(f"\nPlot saved: {output_plot}")
    plt.close()


if __name__ == '__main__':
    main()
