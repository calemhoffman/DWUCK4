# 36S(d,p)37S State Parameters - README

This file defines the parameters for each nuclear state in the 36S(d,p)37S reaction.

## How to Use

1. **Edit** `36S_states.csv` to add or modify states
2. **Run** the generator script:
   ```bash
   python3 tools/generate_input.py inputs/36S_states.csv inputs/DW_36S_DP_auto.in
   ```
3. **Use** the generated input file with DWUCK4:
   ```bash
   ./DWUCK4.exe < inputs/DW_36S_DP_auto.in > outputs/results.txt
   ```

## CSV Column Descriptions

| Column | Description | Example |
|--------|-------------|---------|
| `Ex_keV` | Excitation energy in keV | 0, 645, 2000 |
| `orbital` | Orbital designation | 0f7/2, 1p3/2, 1d5/2 |
| `n` | Principal quantum number | 0, 1, 2 |
| `L` | Orbital angular momentum (0=s, 1=p, 2=d, 3=f) | 3, 1, 2 |
| `j_times_2` | 2 times total angular momentum | 7 for j=7/2 |
| `nodes` | Number of radial nodes (n-1) | 0, 1, 2 |
| `Q_MeV` | Q-value in MeV = Q_gs - Ex/1000 | 2.079, 1.434 |
| `E_bind_MeV` | Binding energy in MeV = E_bind_gs + Ex/1000 | -4.304, -3.659 |

## Example: Adding a New State

To add a 2000 keV, 1d5/2 state:

```csv
2000,1d5/2,1,2,5,0,0.079,-2.304
```

Calculations:
- Q-value: 2.079 - 2.000 = 0.079 MeV
- Binding energy: -4.304 + 2.000 = -2.304 MeV
- Nodes: For 1d orbital, n=1, so nodes = n-1 = 0

## Common Orbitals Reference

| Orbital | n | L | j | j_times_2 | nodes |
|---------|---|---|---|-----------|-------|
| 0s1/2   | 0 | 0 | 1/2 | 1 | 0 |
| 0p3/2   | 0 | 1 | 3/2 | 3 | 0 |
| 0p1/2   | 0 | 1 | 1/2 | 1 | 0 |
| 0d5/2   | 0 | 2 | 5/2 | 5 | 0 |
| 0d3/2   | 0 | 2 | 3/2 | 3 | 0 |
| 0f7/2   | 0 | 3 | 7/2 | 7 | 0 |
| 0f5/2   | 0 | 3 | 5/2 | 5 | 0 |
| 1p3/2   | 1 | 1 | 3/2 | 3 | 1 |
| 1p1/2   | 1 | 1 | 1/2 | 1 | 1 |
| 1d5/2   | 1 | 2 | 5/2 | 5 | 0 |
| 2s1/2   | 2 | 0 | 1/2 | 1 | 2 |
