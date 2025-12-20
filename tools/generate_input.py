#!/usr/bin/env python3
"""
Generate DWUCK4 input file from CSV state parameters.

Usage:
    python3 tools/generate_input.py inputs/36S_states.csv inputs/output.in
    
The CSV file should have columns:
    Ex_keV, orbital, n, L, j_times_2, nodes, Q_MeV, E_bind_MeV
"""

import sys
import csv
from pathlib import Path


# Fixed parameters (same for all states) for 36S(d,p)37S @ 8 MeV
FIXED_PARAMS = {
    'control_code': '1001000000200000',
    'reaction': '36S(d,p)@ 8MeV',
    'bound_marker': 'bound ZR',
    'angles': '90.     0.0     1.     ',
    'lmax_nltr': '+30+01',
    'integration': '+00.30  +000.0   +50.0          0.7',
    
    # Particle 1 (Deuteron)
    'p1_card1': '+08.000  2.0     1.0    36.0    16.0    001.303                  2.0    ',
    'p1_card2': '+01.    -92.976 +01.150 +00.761         -01.602 +01.335 +00.525 ',
    'p1_card3': '+02.    +00.000 +00.000 +00.000         +42.340 +01.380 +00.736 ',
    'p1_card4': '-04.    -14.228 +00.972 +01.011         +00.000 +00.000 +00.000 ',
    
    # Particle 2 (Proton) - base optical potential (will adjust slightly per state)
    'p2_card2': '+01.    -56.249 +01.182 +00.672         -00.786 +01.182 +00.672 ',
    'p2_card3': '+02.    +00.000 +00.000 +00.000         +34.836 +01.290 +00.538 ',
    'p2_card4': '-04.    -22.456 +00.991 +00.590         +00.156 +00.991 +00.590 ',
    
    # Particle 3 (Bound state)
    'p3_card2': '-01.    -01.    +01.28  +00.65  24.0',
    'p3_mass': '1.0     0.0    36.0    16.0    +01.30                  +01.    ',
}


def format_state_block(state):
    """Generate DWUCK4 input block for a single state."""
    lines = []
    
    # Card 1: Title
    title = f"{FIXED_PARAMS['control_code']}    {FIXED_PARAMS['reaction']}    {int(state['Ex_keV'])} keV  {state['orbital']} {FIXED_PARAMS['bound_marker']}"
    lines.append(title)
    
    # Card 2: Angles
    lines.append(FIXED_PARAMS['angles'])
    
    # Card 3: Quantum numbers (LMAX, NLTR, L-transfer, 2*J)
    L = int(state['L'])
    j2 = int(state['j_times_2'])
    qn_card = f"{FIXED_PARAMS['lmax_nltr']}+{L:02d}+{j2:02d}"
    lines.append(qn_card)
    
    # Card 4: Integration parameters
    lines.append(FIXED_PARAMS['integration'])
    
    # Cards 5-8: Particle 1 (Deuteron) - fixed
    lines.append(FIXED_PARAMS['p1_card1'])
    lines.append(FIXED_PARAMS['p1_card2'])
    lines.append(FIXED_PARAMS['p1_card3'])
    lines.append(FIXED_PARAMS['p1_card4'])
    
    # Card 9: Particle 2 (Proton) - Q-value
    Q = float(state['Q_MeV'])
    p2_card1 = f"{Q:+08.3f}  1.0     1.0    37.0    16.0    001.292                 +01.    "
    lines.append(p2_card1)
    
    # Cards 10-12: Particle 2 optical potential
    lines.append(FIXED_PARAMS['p2_card2'])
    lines.append(FIXED_PARAMS['p2_card3'])
    lines.append(FIXED_PARAMS['p2_card4'])
    
    # Card 13: Particle 3 (Bound state) - binding energy
    E_bind = float(state['E_bind_MeV'])
    p3_card1 = f"{E_bind:+08.3f}  {FIXED_PARAMS['p3_mass']}"
    lines.append(p3_card1)
    
    # Card 14: Particle 3 potential
    lines.append(FIXED_PARAMS['p3_card2'])
    
    # Card 15: Particle 3 quantum numbers (nodes, L, 2*J, fixed, rmax)
    nodes = int(state['nodes'])
    p3_card3 = f"+{nodes:02d}.0   +{L:02d}.0   +{j2:02d}.0   +01.0   +50.0   "
    lines.append(p3_card3)
    
    return lines


def read_states(csv_file):
    """Read state parameters from CSV file."""
    states = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f, skipinitialspace=True)
        for row in reader:
            # Skip empty rows or comment lines
            if not row or not row.get('Ex_keV'):
                continue
            if row['Ex_keV'].strip().startswith('#'):
                continue
            states.append(row)
    return states


def generate_input_file(csv_file, output_file):
    """Generate DWUCK4 input file from CSV state parameters."""
    states = read_states(csv_file)
    
    if not states:
        print("Error: No states found in CSV file")
        return False
    
    print(f"Found {len(states)} states in {csv_file}")
    
    # Generate input file
    with open(output_file, 'w') as f:
        for i, state in enumerate(states):
            print(f"  State {i+1}: {state['Ex_keV']} keV, {state['orbital']}")
            
            # Write state block
            block = format_state_block(state)
            for line in block:
                f.write(line + '\n')
        
        # Write end marker
        f.write('9                   END OF DATA for DWUCK4\n')
    
    print(f"Successfully generated: {output_file}")
    return True


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 tools/generate_input.py <states.csv> <output.in>")
        print("\nExample:")
        print("  python3 tools/generate_input.py inputs/36S_states.csv inputs/DW_36S_DP_auto.in")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not Path(csv_file).exists():
        print(f"Error: CSV file not found: {csv_file}")
        sys.exit(1)
    
    success = generate_input_file(csv_file, output_file)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
