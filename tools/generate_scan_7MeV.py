#!/usr/bin/env python3.11
"""
Generate DWUCK4 input file for 36S(d,p) excitation energy scan (0-7 MeV).
Uses Ground State potentials for all states.
Handles Bound/Unbound transition logic.
Strict fixed-width formatting for "card" input.
"""

import sys

def fmt_f8(val, decimal_places=3):
    """Format a float to exactly 8 characters width with sign."""
    # DWUCK4 usually expects F8.4 (or similar), so 8 chars total.
    # Standard format: "+XX.XXXX" or similar.
    # Try {:+8.4f} but check length.
    
    # Special handling to match user templates which often use F8.3 or F8.2 padding spaces
    # User examples: "+00.10  ", "+00.    ", "+50.0   "
    # We will aim for "{:+8.xf}" 
    
    s = f"{val:+.{decimal_places}f}"
    
    # If too long, reduce precision?
    # DWUCK bounds are usually small like +/- 200.
    
    # Just force valid float representation in 8 chars?
    # Actually, Fortran F8.4 reading is flexible with spaces, but rigid with width.
    # It reads 8 characters. If we provide "   +50.0", it parses 50.0.
    # If we provide "+50.0   ", it parses 50.0.
    
    # Let's use standard rjust or ljust to ensure 8 chars.
    # The generated file had "+00.10  ". 
    # Let's just use f"{val:+8.3f}" (default python alignment).
    # Python {:+8.3f} aligns to right by default? "+50.000" (7 chars). " +50.000".
    
    # Let's standardize:
    # 1. Format number
    # 2. Slice or Pad
    
    # For RMAX card: "+00.10  ", "+00.    ", "+050.   "
    # It seems they use manual alignment.
    
    # Let's stick to simple: f"{val:+8.3f}" unless value needs more space.
    # Actually, let's use a custom formatter to ensure exactly 8 chars.
    
    # If value is integer-ish like 50.0, print "+50.0   "
    
    # For this specific task, let's just make sure it fits.
    
    res = f"{val:+.3f}" # e.g. "+50.000" (7 chars)
    if len(res) < 8:
        # Pad with spaces on right to match "Card" look? 
        # Or pad left? Fortran doesn't care if spaces are leading.
        # But user template used "+00.10  " (Left aligned in field?)
        # Let's pad Right for visual similarity to user file.
        res = res.ljust(8)
    else:
        # If > 8 chars, we might have issue. e.g. -100.000 (8 chars) OK.
        # -1000.000 (9 chars).
        if len(res) > 8:
            # removing digits?
            res = f"{val:+.2f}".ljust(8)
            
    return res[:8] # Strictly truncate to 8 to avoid pushing next column

def get_base_parameters():
    """Return the fixed optical model parameters and GS quantum numbers."""
    return {
        'title_base': '36S(d,p)@ 16MeV',
        'Q_gs': 2.079,      
        'BE_gs': -4.304,    
        
        # Fixed lines that are complex to split (Optical Models)
        # We can just output them as fixed strings if we trust them.
        # But ideally we should format them too if we want "strict".
        # For now, trust the user template strings for Potentials as they worked before.
        # Just ensure simple lines (Card 1, 2, 3, 4, Q, BE) are strict.
        
        'p1_card1': '+16.000  2.0     1.0    36.0    16.0    001.303                  2.0            ',
        'p1_card2': '+01.    -92.976 +01.150 +00.761         -01.602 +01.335 +00.525 ',
        'p1_card3': '+02.    +00.000 +00.000 +00.000         +42.340 +01.380 +00.736 ',
        'p1_card4': '-04.    -14.228 +00.972 +01.011         +00.000 +00.000 +00.000 ',
        
        'p2_card2': '+01.    -56.249 +01.182 +00.672         -00.786 +01.182 +00.672 ',
        'p2_card3': '+02.    +00.000 +00.000 +00.000         +34.836 +01.290 +00.538 ',
        'p2_card4': '-04.    -22.456 +00.991 +00.590         +00.156 +00.991 +00.590 ',
        
        'p3_card2': '-01.    -01.    +01.28  +00.65  24.0                                            ',
        'p3_mass': '1.0     0.0    36.0    16.0    +01.30                  +01.    ',
        
        'L': 3,
        'J2': 7,
        'Nodes': 0,
    }

def format_state(ex_mev, params):
    """Generate a single state block with strict width."""
    lines = []
    
    q_val = params['Q_gs'] - ex_mev
    be_val = params['BE_gs'] + ex_mev
    is_bound = be_val < 0
    
    if is_bound:
        control = '1001000000200000' # 16 chars
        comment = 'bound ZR'
        lmax_val = 30
        rmax = 50.0
    else:
        control = '1011000030000000' # 16 chars
        comment = 'unbound ZR'
        lmax_val = 15
        rmax = -15.0
        
    # Card 1: Control (20I1) + Title (15A4)
    # Control needs 20 characters. 16 given + 4 spaces.
    card1_ctrl = control.ljust(20) # cols 1-20
    # Title: "36S(d,p)@ 8MeV    X keV  0f7/2 unbound ZR"
    # Needs to fit in 60 chars (cols 21-80)
    title_str = f"{params['title_base']}    {ex_mev*1000:.0f} keV  0f7/2 {comment}"
    card1 = card1_ctrl + title_str
    card1 = card1.ljust(80) # Ensure at least 80
    lines.append(card1)
    
    # Card 2: Angles "+90.    +00.    +01."
    # Format 10F8.4
    # "+90." is 4 chars. "+90.    " is 8.
    c2 = fmt_f8(90.0) + fmt_f8(0.0) + fmt_f8(1.0)
    lines.append(c2.ljust(80))
    
    # Card 3: LMAX, NLTR, L, 2J
    # Format: 18I3 (ADWCK4 line 47: READ (5,9002)L,NLTR...)
    # 9002 FORMAT(18I3) -> 3 chars per integer.
    # LMAX (2 digit), NLTR (2 digit), L (2 digit), 2J (2 digit).
    # So "+30" (3 chars), "+01" (3 chars), "+03" (3 chars), "+07" (3 chars)
    c3 = f"{lmax_val:+03d}{1:+03d}{params['L']:+03d}{params['J2']:+03d}"
    # Verify: "+30+01+03+07" -> 12 characters. 4 integers * 3 chars. Correct.
    lines.append(c3.ljust(80))
    
    # Card 4: DRF, RZ, RMAX, VCE, FNRNG, AMASS
    # Format 10F8.4
    drf = 0.1
    rz = 0.0
    # rmax varies
    vce = 0.0
    fnrng = 0.0
    # amass if needed? template has "+00.10  +00.    +050.   "
    # Wait, template line: "+00.10  +00.    +50.0"
    # Field 1: +00.10
    # Field 2: +00.
    # Field 3: +50.0
    c4 = fmt_f8(drf) + fmt_f8(rz) + fmt_f8(rmax)
    lines.append(c4.ljust(80))
    
    # Particles
    lines.append(params['p1_card1'])
    lines.append(params['p1_card2'])
    lines.append(params['p1_card3'])
    lines.append(params['p1_card4'])
    
    # Particle 2 Q-value: Format F8.4?
    # DWUCK4.FOR line 377 (POTS): READ (5,9000)E,FM...
    # 9000 FORMAT(10F8.4)
    # So Q-value should be first 8 chars.
    q_str = fmt_f8(q_val)
    # Remaining fields: FM, Z, FMA, ZA ...
    # From template: "  1.0     1.0    37.0    16.0    001.292                 +01.            "
    # these are fixed.
    p2_rest = "  1.0     1.0    37.0    16.0    001.292                 +01.            "
    lines.append(q_str + p2_rest)
    
    lines.append(params['p2_card2'])
    lines.append(params['p2_card3'])
    lines.append(params['p2_card4'])
    
    # Particle 3 Binding Energy
    be_str = fmt_f8(be_val)
    p3_rest = params['p3_mass']
    lines.append(be_str + "  " + p3_rest) # Note: p3_mass string includes spacing
    # Actually P3 Card 1 format: E(Bind), FM...
    # Template: "-04.304  1.0     0.0    36.0    16.0    +01.30                  +01.    "
    # Be careful with spacing between be_str and p3_rest.
    # If be_str is 8 chars. Template "-04.304 " (8 chars? -04.304 is 7. space is 8?)
    # "  1.0" starts at col 9? "  1.0" is 5 chars.
    # Let's inspect p3_mass: "1.0     0.0..."
    # If we append it directly to 8-char BE, it starts at col 9.
    # "1.0     " is 8 chars.
    # So be_str + p3_mass should work if p3_mass starts correctly.
    
    lines.append(params['p3_card2'])
    
    # Card 3 Nodes...
    # Template: "+00.    +03.    +07.    +01.    +50.0   +00.    +00.00"
    # Format 10F8.4 (READ 9000 in Bind/Pots)
    # fields: Nodes(F8), L(F8), J2(F8), S(F8), FISW(F8)...
    c_nodes = fmt_f8(params['Nodes']) # e.g. "+0.000  "
    c_l = fmt_f8(params['L'])
    c_j = fmt_f8(params['J2'])
    c_s = fmt_f8(1.0) # Spin? Template "+01."
    c_fisw = fmt_f8(50.0) # FISW
    c_rest = fmt_f8(0.0) + fmt_f8(0.0)
    
    c_last = c_nodes + c_l + c_j + c_s + c_fisw + c_rest
    lines.append(c_last.ljust(80))
    
    return lines

def main():
    params = get_base_parameters()
    output_file = 'inputs/36S_scan_7MeV.in'
    
    with open(output_file, 'w') as f:
        for ex in range(8):
            state_lines = format_state(float(ex), params)
            for line in state_lines:
                f.write(line + '\n')
        f.write('9                   END OF DATA for DWUCK4\n')
        
    print(f"Generated {output_file} w/ strict parsing.")

if __name__ == "__main__":
    main()
