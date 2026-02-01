#!/usr/bin/env python3.11
"""Fix unbound state input files to use proper DWUCK4 format"""

import re

files_to_fix = [
    ("/Users/calemhoffman/Documents/GitHub/DWUCK4/inputs/DW_36S_DP_QP_ex485_0f52.in", 0.555),
    ("/Users/calemhoffman/Documents/GitHub/DWUCK4/inputs/DW_36S_DP_AK_ex500_0f52.in", 0.696),
    ("/Users/calemhoffman/Documents/GitHub/DWUCK4/inputs/DW_36S_DP_QP_ex500_0f52.in", 0.696),
    ("/Users/calemhoffman/Documents/GitHub/DWUCK4/inputs/DW_36S_DP_AK_ex600_0f52.in", 1.696),
    ("/Users/calemhoffman/Documents/GitHub/DWUCK4/inputs/DW_36S_DP_QP_ex600_0f52.in", 1.696),
]

for filepath, binding in files_to_fix:
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # Fix line 1: control integers
    lines[0] = re.sub(r'^1001000000200000', '1011000030000000', lines[0])
    
    # Fix line 3: LMAX
    lines[2] = re.sub(r'^\+30\+01', '+15+01', lines[2])
    
    # Fix line 4: RMAX to negative
    lines[3] = re.sub(r'\+50\.000', '-15.000', lines[3])
    
    # Fix line 13: binding energy to positive
    lines[12] = re.sub(r'^-' + f'{binding:.3f}', f'+{binding:.3f}', lines[12])
    
    with open(filepath, 'w') as f:
        f.writelines(lines)
    
    print(f"Fixed {filepath}")

print("All files fixed!")
