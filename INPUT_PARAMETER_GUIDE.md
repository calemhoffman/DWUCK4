# DWUCK4 Input File Parameter Guide for Adding States

## Comparison: State 1 vs State 2 in DW_36S_DP.in

### Overview
- **State 1**: 0 keV, 0f₇/₂ (ground state)
- **State 2**: 645 keV, 1p₃/₂ (first excited state)

---

## Line-by-Line Parameter Changes

### Card 1: Title/Description
**State 1:**
```
1001000000200000    36S(d,p)@ 8MeV    0 keV  0f7/2 bound ZR
```

**State 2:**
```
1001000000200000    36S(d,p)@ 8MeV    645 keV  1p3/2 bound ZR
```

**Changes:**
- Energy label: `0 keV` → `645 keV`
- Orbital: `0f7/2` → `1p3/2`

**Control code** (1001000000200000): **SAME** for both states

---

### Card 2: Angular Distribution
**Both states:**
```
90.     0.0     1.
```

**No changes** - same angular distribution (90 points, 0° start, 1° step)

---

### Card 3: Quantum Numbers
**State 1:**
```
+30+01+03+07
```

**State 2:**
```
+30+01+01+03
```

**Changes:**
- **Field 3** (L-transfer): `+03` → `+01` (L=3 → L=1)
- **Field 4** (2×J): `+07` → `+03` (j=7/2 → j=3/2)

**Format**: `LMAX, NLTR, L-transfer, 2×J`

---

### Card 4: Integration Parameters
**Both states:**
```
+00.30  +000.0   +50.0          0.7
```

**No changes** - same integration parameters

---

### Cards 5-13: Particle Data

#### Particle 1 (Deuteron) - Cards 5-8
**IDENTICAL** for both states - no changes needed

**State 1 & 2:**
```
+08.000  2.0     1.0    36.0    16.0    001.303                  2.0
+01.    -92.976 +01.150 +00.761         -01.602 +01.335 +00.525
+02.    +00.000 +00.000 +00.000         +42.340 +01.380 +00.736
-04.    -14.228 +00.972 +01.011         +00.000 +00.000 +00.000
```

#### Particle 2 (Proton) - Cards 9-12
**Card 9 changes** (binding energy and Q-value):

**State 1:**
```
+02.079  1.0     1.0    37.0    16.0    001.292                 +01.
```

**State 2:**
```
+01.434  1.0     1.0    37.0    16.0    001.292                 +01.
```

**Change:**
- **Q-value**: `+02.079` → `+01.434` MeV
  - Q = (Beam energy) - (Excitation energy) - (Separation energy)
  - Difference: 0.645 MeV (the excitation energy difference!)

**Cards 10-12: Proton optical potential**

**State 1:**
```
+01.    -56.249 +01.182 +00.672         -00.786 +01.182 +00.672
+02.    +00.000 +00.000 +00.000         +34.836 +01.290 +00.538
-04.    -22.456 +00.991 +00.590         +00.156 +00.991 +00.590
```

**State 2:**
```
+01.    -56.510 +01.182 +00.672         -00.734 +01.182 +00.672
+02.    +00.000 +00.000 +00.000         +34.568 +01.290 +00.538
-04.    -22.516 +00.991 +00.590         +00.144 +00.991 +00.590
```

**Changes:** Slight adjustments in optical potential depths (energy-dependent)
- Real central depth: -56.249 → -56.510 MeV
- Real SO depth: -0.786 → -0.734 MeV
- Imaginary surface depth: 34.836 → 34.568 MeV
- Imaginary SO depth: 0.156 → 0.144 MeV

#### Particle 3 (Bound State) - Cards 13-15

**Card 13 changes** (binding energy):

**State 1:**
```
-04.304  1.0     0.0    36.0    16.0    +01.30                  +01.
```

**State 2:**
```
-03.659  1.0     0.0    36.0    16.0    +01.30                  +01.
```

**Change:**
- **Binding energy**: `-04.304` → `-03.659` MeV
  - More bound state is more negative
  - Ground state is deeper bound

**Card 14 changes** (bound state potential):

**State 1:**
```
-01.    -01.    +01.28  +00.65  24.0
```

**State 2:**
```
-01.    -01.    +01.28  +00.65  24.0
```

**No changes** - same Woods-Saxon parameters

**Card 15 changes** (quantum numbers):

**State 1:**
```
+00.0   +03.0   +07.0   +01.0   +50.0
```

**State 2:**
```
+01.0   +01.0   +03.0   +01.0   +50.0
```

**Changes:**
- **Field 1** (Nodes): `+00.0` → `+01.0` (0f₇/₂ has 0 nodes, 1p₃/₂ has 1 node)
- **Field 2** (L): `+03.0` → `+01.0` (L=3 → L=1)
- **Field 3** (2×J): `+07.0` → `+03.0` (j=7/2 → j=3/2)

---

## Summary of Key Parameters to Change

When adding a new state, you need to modify:

### 1. **Card 1** - Description
- Excitation energy (e.g., "1234 keV")
- Orbital designation (e.g., "2s1/2")

### 2. **Card 3** - Quantum Numbers
- **L-transfer** (column 3): orbital angular momentum
- **2×J** (column 4): 2 times total angular momentum

### 3. **Card 9** - Q-value (Particle 2 energy)
```
Q_new = Q_ground_state - E_excitation
```
For 36S(d,p) ground state: Q = +2.079 MeV
- 645 keV state: Q = 2.079 - 0.645 = 1.434 MeV ✓
- For 2000 keV state: Q = 2.079 - 2.000 = 0.079 MeV

### 4. **Cards 10-12** - Proton Optical Potential (optional)
Minor energy-dependent adjustments - can often keep same or interpolate

### 5. **Card 13** - Bound State Binding Energy
```
E_binding = Separation_energy + E_excitation
```
- Ground state: -4.304 MeV
- 645 keV state: -4.304 + 0.645 = -3.659 MeV ✓
- For 2000 keV: -4.304 + 2.000 = -2.304 MeV

### 6. **Card 15** - Bound State Quantum Numbers
- **Nodes**: Radial quantum number (n-L-1)
  - 0f₇/₂: n=0, nodes=0
  - 1p₃/₂: n=1, nodes=1
  - 2s₁/₂: n=2, nodes=2
- **L**: orbital angular momentum (0=s, 1=p, 2=d, 3=f, ...)
- **2×J**: 2 times total angular momentum

---

## Template for Adding New State

Here's a template with the variable parts marked:

```
1001000000200000    36S(d,p)@ 8MeV    [Ex] keV  [orbital] bound ZR
90.     0.0     1.
+30+01+[L]+[2J]
+00.30  +000.0   +50.0          0.7
+08.000  2.0     1.0    36.0    16.0    001.303                  2.0
+01.    -92.976 +01.150 +00.761         -01.602 +01.335 +00.525
+02.    +00.000 +00.000 +00.000         +42.340 +01.380 +00.736
-04.    -14.228 +00.972 +01.011         +00.000 +00.000 +00.000
+[Q_value]  1.0     1.0    37.0    16.0    001.292             +01.
+01.    -56.249 +01.182 +00.672         -00.786 +01.182 +00.672
+02.    +00.000 +00.000 +00.000         +34.836 +01.290 +00.538
-04.    -22.456 +00.991 +00.590         +00.156 +00.991 +00.590
[E_bind]  1.0     0.0    36.0    16.0    +01.30                  +01.
-01.    -01.    +01.28  +00.65  24.0
+[nodes]   +[L]    +[2J]   +01.0   +50.0
```

---

## Example: Adding a 2000 keV, 2s₁/₂ State

Assuming you want to add a 2000 keV excited state with 2s₁/₂ configuration:

**Orbital**: 2s₁/₂ → n=2, L=0 (s-wave), j=1/2
- **Nodes**: 2
- **L**: 0
- **2×J**: 1
- **L-transfer**: 0 (no orbital angular momentum transfer)
- **Q-value**: 2.079 - 2.000 = 0.079 MeV
- **Binding energy**: -4.304 + 2.000 = -2.304 MeV

**Card changes:**
```
Card 1:  1001000000200000    36S(d,p)@ 8MeV    2000 keV  2s1/2 bound ZR
Card 3:  +30+01+00+01
Card 9:  +00.079  1.0     1.0    37.0    16.0    001.292                 +01.
Card 13: -02.304  1.0     0.0    36.0    16.0    +01.30                  +01.
Card 15: +02.0   +00.0   +01.0   +01.0   +50.0
```

---

## Quick Reference Table

| Orbital | n | L | j | L-transfer | 2×J | Nodes |
|---------|---|---|---|------------|-----|-------|
| 0f₇/₂   | 0 | 3 | 7/2 | 3 | 7 | 0 |
| 1p₃/₂   | 1 | 1 | 3/2 | 1 | 3 | 1 |
| 1p₁/₂   | 1 | 1 | 1/2 | 1 | 1 | 1 |
| 2s₁/₂   | 2 | 0 | 1/2 | 0 | 1 | 2 |
| 1d₅/₂   | 1 | 2 | 5/2 | 2 | 5 | 0 |
| 1d₃/₂   | 1 | 2 | 3/2 | 2 | 3 | 0 |
| 0f₅/₂   | 0 | 3 | 5/2 | 3 | 5 | 0 |

**Note**: L-transfer = L of the transferred particle orbital

---

## Important Reminders

1. **Q-value formula**: `Q = Q_gs - E_excitation` (gets less positive/more negative for higher states)
2. **Binding energy formula**: `E_bind = E_bind_gs + E_excitation` (gets less negative for higher states)
3. **Nodes**: For orbital nℓⱼ, nodes = n - 1 (principal quantum number minus 1)
4. **File format**: Use the exact spacing and format - DWUCK4 uses fixed-format Fortran input!
5. **End marker**: Always end with: `9                   END OF DATA for DWUCK4`
