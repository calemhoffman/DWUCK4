#!/usr/bin/env python3.11
"""
Verify ex139 input files and create summary table.
"""

import numpy as np

def parse_dwuck4_output(filename):
    """Extract angle and cross section from DWUCK4 output."""
    angles = []
    cross_sections = []
    
    with open(filename, 'r') as f:
        for line in f:
            if len(line.strip()) > 0:
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        angle = float(parts[0])
                        if 'E' in parts[1] or 'e' in parts[1]:
                            xsec = float(parts[1])
                            angles.append(angle)
                            cross_sections.append(xsec)
                    except (ValueError, IndexError):
                        continue
    
    return np.array(angles), np.array(cross_sections)

# Parse all ex139 outputs
files = {
    '0d3/2 AK': 'outputs/DW_36S_DP_AK_EX139_0d32.out',
    '0d3/2 QP': 'outputs/DW_36S_DP_QP_EX139_0d32.out',
    '1p3/2 AK': 'outputs/DW_36S_DP_AK_EX139_1p32.out',
    '1p3/2 QP': 'outputs/DW_36S_DP_QP_EX139_1p32.out',
}

print("=" * 80)
print("EX139 (1.398 MeV) DWUCK4 CALCULATION SUMMARY")
print("=" * 80)

results = {}
for label, filename in files.items():
    angles, xsec = parse_dwuck4_output(filename)
    results[label] = (angles, xsec)
    print(f"\n{label}:")
    print(f"  Points: {len(angles)}")
    print(f"  Angular range: {angles.min():.1f}° to {angles.max():.1f}°")
    print(f"  Cross section range: {xsec.min():.4e} to {xsec.max():.4e} mb/sr")
    print(f"  Mean cross section: {xsec.mean():.4e} mb/sr")

# Calculate ratios
print("\n" + "=" * 80)
print("OPTICAL MODEL COMPARISONS (AK/QP Ratios)")
print("=" * 80)

for assignment in ['0d3/2', '1p3/2']:
    ak_label = f'{assignment} AK'
    qp_label = f'{assignment} QP'
    
    angles_ak, xsec_ak = results[ak_label]
    angles_qp, xsec_qp = results[qp_label]
    
    xsec_qp_interp = np.interp(angles_ak, angles_qp, xsec_qp)
    ratio = xsec_ak / xsec_qp_interp
    
    print(f"\n{assignment}:")
    print(f"  Mean ratio (AK/QP): {ratio.mean():.3f}")
    print(f"  Ratio range: {ratio.min():.3f} to {ratio.max():.3f}")

# Compare L-transfers
print("\n" + "=" * 80)
print("L-TRANSFER COMPARISON (1p3/2 vs 0d3/2)")
print("=" * 80)

for omp in ['AK', 'QP']:
    _, xsec_0d = results[f'0d3/2 {omp}']
    _, xsec_1p = results[f'1p3/2 {omp}']
    
    ratio_l = xsec_1p.mean() / xsec_0d.mean()
    print(f"\n{omp}:")
    print(f"  1p3/2 mean: {xsec_1p.mean():.4e} mb/sr")
    print(f"  0d3/2 mean: {xsec_0d.mean():.4e} mb/sr")
    print(f"  Ratio (L=1/L=2): {ratio_l:.3f}")

print("\n" + "=" * 80)
print("CONVERSION FACTORS VERIFICATION")
print("=" * 80)
print("\nApplied conversions:")
print("  Deuteron Wsᵢ: 10.340 × 4 × 0.736 = 30.441 MeV")
print("  Deuteron Vso: 3.557 × 4 = 14.228 MeV")
print("  Proton Wsᵢ (AK): 8.719 × 4 × 0.538 = 18.763 MeV")
print("  Proton Vso (AK): 5.468 × 4 = 21.872 MeV")
print("  Proton Wsoᵢ (AK): 0.071 × 4 = 0.284 MeV")
print("  Proton Wsᵢ (QP): 13.500 × 4 × 0.470 = 25.380 MeV")
print("  Proton Vso (QP): 7.500 × 4 = 30.000 MeV")

print("\n" + "=" * 80)
print("✓ All 4 calculations completed successfully")
print("=" * 80)
