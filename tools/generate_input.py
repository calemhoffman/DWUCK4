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
    'control_code_bound': '1001000000200000',    # For bound states (E < 0)
    'control_code_unbound': '1011000030000000',  # For unbound states (E > 0)
    'reaction': '36S(d,p)@ 8MeV',
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


def calculate_proton_optical_model(E_proton):
    """
    Calculate energy-dependent proton optical model potential depths.
    
    Based on empirical parametrization extracted from original DW_36S_DP.in file.
    This is NOT the CH89 global optical model (which is only valid for A >= 40).
    Instead, it uses a custom linear energy dependence fitted to the original data.
    
    Parameters:
    -----------
    E_proton : float
        Exit channel proton laboratory energy in MeV
        
    Returns:
    --------
    dict : Dictionary containing formatted optical potential card lines
    """
    # Reference energy and depths (from state 1: E_x = 0 keV)
    E_ref = 9.438  # MeV
    V_real_ref = -56.249  # Real volume depth
    W_surf_ref = 34.836   # Imaginary surface depth
    VSO_real_ref = -0.786 # Real spin-orbit depth
    WSO_imag_ref = 0.156  # Imaginary spin-orbit depth
    
    # Linear energy dependence coefficients (MeV/MeV)
    # Extracted from comparison of states 1 and 2
    dV_dE = 0.405    # Real volume
    dW_dE = -0.415   # Surface imaginary  
    dVSO_dE = 0.081  # Real SO
    dWSO_dE = -0.019 # Imaginary SO
    
    # Calculate energy difference
    dE = E_proton - E_ref
    
    # Calculate depths
    V_real = V_real_ref + dV_dE * dE
    W_surf = W_surf_ref + dW_dE * dE
    VSO_real = VSO_real_ref + dVSO_dE * dE
    WSO_imag = WSO_imag_ref + dWSO_dE * dE
    
    # Format the three optical potential cards
    # Fixed geometries: r and a values don't change with energy
    card2 = f"+01.    {V_real:+07.3f} +01.182 +00.672         {VSO_real:+07.3f} +01.182 +00.672 "
    card3 = f"+02.    +00.000 +00.000 +00.000         {W_surf:+07.3f} +01.290 +00.538 "
    card4 = f"-04.    -22.456 +00.991 +00.590         {WSO_imag:+07.3f} +00.991 +00.590 "
    
    return {
        'card2': card2,
        'card3': card3,
        'card4': card4,
        'depths': {
            'V_real': V_real,
            'W_surf': W_surf,
            'VSO_real': VSO_real,
            'WSO_imag': WSO_imag
        }
    }


def calculate_deuteron_optical_model(E_deuteron):
    """
    Calculate energy-dependent deuteron optical model potential depths.
    
    Based on empirical parametrization extracted from original DW_36S_DP.in file.
    Only the imaginary surface depth varies significantly with energy.
    
    Parameters:
    -----------
    E_deuteron : float
        Deuteron laboratory energy in MeV (beam energy)
        
    Returns:
    --------
    dict : Dictionary containing formatted optical potential card lines
    """
    # For deuteron, the beam energy is approximately constant at 8 MeV
    # But the effective energy in the exit channel changes slightly with Q-value
    # The deuteron gets the "leftover" energy after the proton takes its share
    
    # Reference: State 1 with Q = 2.079 MeV
    # Deuteron in exit channel has beam energy minus recoil
    # Approximation: E_d ≈ E_beam (8 MeV for entrance, varies in exit)
    
    E_ref = 8.0  # Reference beam energy
    W_D_ref = 42.340  # Imaginary surface depth at reference
    
    # From state 1 to state 2 comparison:
    # State 1: W_D = 42.340, Q = 2.079
    # State 2: W_D = 43.432, Q = 1.434  
    # ΔQ = -0.645 MeV means deuteron exit has MORE energy
    # ΔW_D = +1.092 MeV
    # So dW_D/dE_d ≈ +1.092/0.645 ≈ +1.69 MeV per MeV Q-change
    
    # For entrance channel, energy barely changes, so we use Q-value as proxy
    # This is an approximation - proper would be to calculate deuteron kinematics
    dW_D_dQ = +1.69  # MeV per MeV of Q-value change
    
    # We'll use Q-value directly from state (simpler than kinematic calculation)
    # Card is used in entrance channel where deuteron energy is fixed
    # The variation we see is likely due to different optical model parametrizations
    # That account for the reaction Q-value
    
    # For now, we'll just return reference values since deuteron energy
    # in entrance channel is constant. The W_D variation will be handled
    # by Q-value correlation below.
    
    # Fixed parameters
    V_real = -92.976
    r_V = 1.150
    a_V = 0.761
    VSO_real = -1.602
    r_SO = 1.335
    a_SO = 0.525
    r_W = 1.380
    a_W = 0.736
    
    # Imaginary surface will be calculated from Q-value in format_state_block
    # Return structure for consistency, but W_D will be overridden
    card2 = f"+01.    {V_real:+07.3f} +{r_V:06.3f} +{a_V:06.3f}         {VSO_real:+07.3f} +{r_SO:06.3f} +{a_SO:06.3f} "
    
    return {
        'card2': card2,
        'V_real': V_real,
        'r_V': r_V,
        'a_V': a_V,
        'VSO_real': VSO_real,
        'r_SO': r_SO,
        'a_SO': a_SO,
        'r_W': r_W,
        'a_W': a_W
    }


def calculate_deuteron_W_surface(Q_value):
    """
    Calculate deuteron imaginary surface depth based on Q-value.
    
    The Q-value correlation accounts for the energy dependence seen in
    the original file.
    
    Parameters:
    -----------
    Q_value : float
        Reaction Q-value in MeV
        
    Returns:
    --------
    float : Imaginary surface depth W_D in MeV
    """
    # Reference from state 1
    Q_ref = 2.079
    W_D_ref = 42.340
    
    # Linear dependence (negative because W_D increases as Q decreases)
    # State 1: Q=2.079, W_D=42.340
    # State 2: Q=1.434, W_D=43.432
    # ΔQ = -0.645, ΔW_D = +1.092
    # dW_D/dQ = -1.092/0.645 = -1.69
    dW_D_dQ = -1.69  # MeV per MeV
    
    dQ = Q_value - Q_ref
    W_D = W_D_ref + dW_D_dQ * dQ
    
    return W_D


def format_state_block(state):
    """Generate DWUCK4 input block for a single state."""
    lines = []
    
    # Determine if state is bound or unbound based on binding energy
    E_bind = float(state['E_bind_MeV'])
    is_bound = E_bind < 0
    
    # Select appropriate control code and marker
    control_code = FIXED_PARAMS['control_code_bound'] if is_bound else FIXED_PARAMS['control_code_unbound']
    bound_marker = 'bound ZR' if is_bound else 'unbound ZR'
    
    # Card 1: Title (80 chars fixed width)
    title = f"{control_code}    {FIXED_PARAMS['reaction']}    {int(state['Ex_keV'])} keV  {state['orbital']} {bound_marker}"
    title = title.ljust(80)  # Pad to 80 characters
    lines.append(title)
    
    # Card 2: Angles (fixed width: +90.    +00.    +01.)
    lines.append('+90.    +00.    +01.                                                            ')
    
    # Card 3: Quantum numbers (LMAX, NLTR, L-transfer, 2*J) - Fixed width
    L = int(state['L'])
    j2 = int(state['j_times_2'])
    # For unbound: use LMAX=15 to avoid buffer, bound: LMAX=30
    lmax = 15 if not is_bound else 30
    qn_card = f"+{lmax:02d}+01+{L:02d}+{j2:02d}"
    qn_card = qn_card.ljust(80)
    lines.append(qn_card)
    
    # Card 4: Integration parameters (NEGATIVE RMAX for unbound!)
    rmax = -15.0 if not is_bound else 50.0
    integration = f"+00.10  +00.    {rmax:+04.0f}."
    integration = integration.ljust(80)
    lines.append(integration)
    
    # Cards 5-8: Particle 1 (Deuteron) - Fixed width format
    # Card 5: ELAB, masses, etc
    p1_c1 = '+08.000  2.0     1.0    36.0    16.0    001.303                  2.0            '
    lines.append(p1_c1)
    
    # Cards 6-8: Deuteron optical potential (energy-dependent for entrance channel)
    deut_params = calculate_deuteron_optical_model(8.0)
    Q = float(state['Q_MeV'])
    W_D = calculate_deuteron_W_surface(Q)
    
    # Card 6: Volume real + volume imaginary
    p1_c2 = f"+01.    -92.976 +01.150 +00.761         -01.602 +01.335 +00.525 "
    lines.append(p1_c2)
    
    # Card 7: Surface imaginary (W_D varies with Q)
    p1_c3 = f"+02.    +00.000 +00.000 +00.000         {W_D:+07.3f} +01.380 +00.736 "
    lines.append(p1_c3)
    
    # Card 8: Spin-orbit
    p1_c4 = f"-04.    -14.228 +00.972 +01.011         +00.000 +00.000 +00.000 "
    lines.append(p1_c4)
    
    # Cards 9-12: Particle 2 (Proton) optical potential - energy-dependent
    E_proton = float(state['E_proton_MeV'])
    opt_pot = calculate_proton_optical_model(E_proton)
    
    # Card 9: Q-value line (MUST have proper sign formatting!)
    # DWUCK4 expects Q-value to be positive if Q > 0, negative if Q < 0
    # The format is +07.3f for negative, +06.3f for positive with leading space
    # Example: +02.079, -00.123
    if Q >= 0:
        Q_formatted = f"+{Q:06.3f}"
    else:
        Q_formatted = f"{Q:+07.3f}" # Negative sign included
    
    p2_c1 = f"{Q_formatted}  1.0     1.0    37.0    16.0    001.292                 +01.            "
    lines.append(p2_c1)
    
    # Cards 10-12: Proton optical potential
    lines.append(opt_pot['card2'])
    lines.append(opt_pot['card3'])
    lines.append(opt_pot['card4'])
    
    # Cards 13-15: Particle 3 (Bound/unbound neutron state)
    E_bind = float(state['E_bind_MeV'])
    # DWUCK4 expects binding energy to be positive for bound states, negative for unbound
    # The format is +06.3f for positive, +07.3f for negative with leading space
    if E_bind >= 0:
        E_bind_formatted = f"+{E_bind:06.3f}"
    else:
        E_bind_formatted = f"{E_bind:+07.3f}" # Negative sign included
    
    # Card 13: Binding energy line
    p3_c1 = f"{E_bind_formatted}  1.0     0.0    36.0    16.0    +01.30                  +01.            "
    lines.append(p3_c1)
    
    # Card 14: Bound state potential
    p3_c2 = '-01.    -01.    +01.28  +00.65  24.0                                            '
    lines.append(p3_c2)
    
    # Card 15: Quantum numbers with FISW=50.0 for unbound
    nodes = int(state['nodes'])
    fisw = 50.0  # Non-zero for all states (let DWUCK4 decide)
    p3_c3 = f"+{nodes:02.0f}.    +{L:02.0f}.    +{j2:02.0f}.    +01.    {fisw:+05.1f}   +00.    +00.00"
    p3_c3 = p3_c3.ljust(80)
    lines.append(p3_c3)
    
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
