#!/usr/bin/env python3.11
"""
Compare PTOLEMY and DWUCK4 angular distributions for validation.
"""

import argparse
import re
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def parse_ptolemy_output(filepath):
    """
    Parse PTOLEMY output file to extract angular distributions.
    
    Returns:
        dict: {'angle': np.array, 'cross_section': np.array, 'ratio_ruth': np.array}
    """
    angles = []
    cross_sections = []
    ratio_ruth = []
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # Find the cross-section table (starts after "COMPUTATION OF CROSS SECTIONS")
    in_table = False
    for i, line in enumerate(lines):
        if 'COMPUTATION OF CROSS SECTIONS' in line:
            # Skip header lines
            in_table = True
            continue
        
        if in_table:
            # Stop at total or next section
            if 'TOTAL:' in line or 'ANALYZING POWERS' in line:
                break
            
            # Parse data lines (format: angle, xs_cm, xs/ruth, ...)
            # Example: "   0.00   80.537      0.000000    1.94    0.00     0.0   ..."
            match = re.match(r'\s+(\d+\.\d+)\s+([\d.]+)\s+([\d.]+)', line)
            if match:
                angle = float(match.group(1))
                xs = float(match.group(2))
                ruth = float(match.group(3))
                
                angles.append(angle)
                cross_sections.append(xs)
                ratio_ruth.append(ruth)
    
    return {
        'angle': np.array(angles),
        'cross_section': np.array(cross_sections),
        'ratio_ruth': np.array(ratio_ruth)
    }


def parse_dwuck4_output(filepath):
    """
    Parse DWUCK4 output file to extract angular distributions.
    
    Returns:
        dict: {'angle': np.array, 'cross_section': np.array}
    """
    angles = []
    cross_sections = []
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # Find cross-section data
    # DWUCK4 format varies, but typically has angle and xs columns
    # Look for lines with angle and cross-section data
    for line in lines:
        # Skip header/title lines
        if any(kw in line for kw in ['DWUCK', 'ANGLE', 'CENTER', '---']):
            continue
        
        # Try to parse numeric data (angle, xs, ...)
        # Format example: "  0.0    80.537    ..."
        parts = line.split()
        if len(parts) >= 2:
            try:
                angle = float(parts[0])
                xs = float(parts[1])
                
                # Sanity check: angles should be 0-180
                if 0 <= angle <= 180:
                    angles.append(angle)
                    cross_sections.append(xs)
            except (ValueError, IndexError):
                continue
    
    return {
        'angle': np.array(angles),
        'cross_section': np.array(cross_sections)
    }


def calculate_statistics(ptolemy_data, dwuck_data):
    """
    Calculate comparison statistics between PTOLEMY and DWUCK4.
    
    Returns:
        dict: Statistics including RMS difference, max difference, etc.
    """
    # Interpolate to common angle grid
    common_angles = ptolemy_data['angle']
    dwuck_xs_interp = np.interp(common_angles, dwuck_data['angle'], dwuck_data['cross_section'])
    
    ptolemy_xs = ptolemy_data['cross_section']
    
    # Calculate differences
    abs_diff = np.abs(ptolemy_xs - dwuck_xs_interp)
    rel_diff = abs_diff / (ptolemy_xs + 1e-10)  # Avoid division by zero
    
    rms_abs = np.sqrt(np.mean(abs_diff**2))
    rms_rel = np.sqrt(np.mean(rel_diff**2))
    max_abs = np.max(abs_diff)
    max_rel = np.max(rel_diff)
    
    return {
        'rms_absolute': rms_abs,
        'rms_relative': rms_rel * 100,  # as percentage
        'max_absolute': max_abs,
        'max_relative': max_rel * 100,
        'mean_ptolemy': np.mean(ptolemy_xs),
        'mean_dwuck': np.mean(dwuck_xs_interp)
    }


def plot_comparison(ptolemy_data, dwuck_data, output_path, stats):
    """
    Create comparison plot of PTOLEMY vs DWUCK4 angular distributions.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), 
                                     gridspec_kw={'height_ratios': [3, 1]})
    
    # Main plot: cross-sections
    ax1.semilogy(ptolemy_data['angle'], ptolemy_data['cross_section'], 
                 'b-', linewidth=2, label='PTOLEMY', alpha=0.8)
    ax1.semilogy(dwuck_data['angle'], dwuck_data['cross_section'], 
                 'r--', linewidth=2, label='DWUCK4', alpha=0.8)
    
    ax1.set_xlabel('Angle (degrees)', fontsize=12)
    ax1.set_ylabel('dσ/dΩ (mb/sr)', fontsize=12)
    ax1.set_title('³⁶S(d,p)³⁷S Ground State Comparison', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    
    # Add statistics text box
    stats_text = f"RMS difference: {stats['rms_relative']:.2f}%\n"
    stats_text += f"Max difference: {stats['max_relative']:.2f}%"
    ax1.text(0.95, 0.95, stats_text, transform=ax1.transAxes,
             fontsize=10, verticalalignment='top', horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Residual plot
    common_angles = ptolemy_data['angle']
    dwuck_xs_interp = np.interp(common_angles, dwuck_data['angle'], dwuck_data['cross_section'])
    residuals = (dwuck_xs_interp - ptolemy_data['cross_section']) / ptolemy_data['cross_section'] * 100
    
    ax2.plot(common_angles, residuals, 'ko-', markersize=4, linewidth=1)
    ax2.axhline(y=0, color='r', linestyle='--', linewidth=1)
    ax2.fill_between(common_angles, -5, 5, alpha=0.2, color='green', label='±5%')
    
    ax2.set_xlabel('Angle (degrees)', fontsize=12)
    ax2.set_ylabel('Residual (%)', fontsize=12)
    ax2.set_title('(DWUCK4 - PTOLEMY) / PTOLEMY', fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=9)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Comparison plot saved to: {output_path}")
    
    return fig


def main():
    parser = argparse.ArgumentParser(description='Compare PTOLEMY and DWUCK4 outputs')
    parser.add_argument('--ptolemy', required=True, help='Path to PTOLEMY output file')
    parser.add_argument('--dwuck', required=True, help='Path to DWUCK4 output file')
    parser.add_argument('--output', default='comparison_plot.png', help='Output plot filename')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("PTOLEMY vs DWUCK4 Validation")
    print("=" * 60)
    
    # Parse both outputs
    print(f"\n📖 Parsing PTOLEMY output: {args.ptolemy}")
    ptolemy_data = parse_ptolemy_output(args.ptolemy)
    print(f"   Found {len(ptolemy_data['angle'])} angle points")
    
    print(f"\n📖 Parsing DWUCK4 output: {args.dwuck}")
    dwuck_data = parse_dwuck4_output(args.dwuck)
    print(f"   Found {len(dwuck_data['angle'])} angle points")
    
    # Calculate statistics
    print("\n📊 Calculating comparison statistics...")
    stats = calculate_statistics(ptolemy_data, dwuck_data)
    
    print(f"\n{'Results':^60}")
    print("-" * 60)
    print(f"  RMS Absolute Difference: {stats['rms_absolute']:.4f} mb/sr")
    print(f"  RMS Relative Difference: {stats['rms_relative']:.2f}%")
    print(f"  Max Absolute Difference: {stats['max_absolute']:.4f} mb/sr")
    print(f"  Max Relative Difference: {stats['max_relative']:.2f}%")
    print(f"  Mean PTOLEMY σ:          {stats['mean_ptolemy']:.4f} mb/sr")
    print(f"  Mean DWUCK4 σ:           {stats['mean_dwuck']:.4f} mb/sr")
    print("-" * 60)
    
    # Validation assessment
    if stats['rms_relative'] < 5.0:
        print("\n✅ EXCELLENT agreement (RMS < 5%)")
    elif stats['rms_relative'] < 10.0:
        print("\n✓  GOOD agreement (RMS < 10%)")
    elif stats['rms_relative'] < 20.0:
        print("\n⚠  FAIR agreement (RMS < 20%) - check parameters")
    else:
        print("\n❌ POOR agreement (RMS > 20%) - parameters likely incorrect")
    
    # Create comparison plot
    print(f"\n📈 Creating comparison plot...")
    plot_comparison(ptolemy_data, dwuck_data, args.output, stats)
    
    print(f"\n{'Validation complete!':^60}\n")
    print("=" * 60)


if __name__ == '__main__':
    main()
