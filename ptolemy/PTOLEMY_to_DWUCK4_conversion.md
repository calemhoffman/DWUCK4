# Ptolemy → DWUCK4 Conversion Reference

> **Verified against**: ³⁶S(d,p)³⁷S known-correct DWUCK4 files in `temp/ex000/dwuck/`  
> **Last verified**: 2026-02-26

---

## Card Layout Overview

DWUCK4 uses strict **8-character Fortran** fixed-format fields. A (d,p) bound-state calculation has these cards:

| Card | Contents |
|------|----------|
| 1 | Control codes + title |
| 2 | θ_max, θ_min, Δθ |
| 3 | LMAX, LSTEP, L_transfer, NLMAX(=2j) |
| 4 | Integration step, 0, R_max |
| 5 | **Incoming channel header** |
| 6 | Incoming: real central + volume imaginary (type +1) |
| 7 | Incoming: surface imaginary (type +2) |
| 8 | Incoming: spin-orbit (type -4) |
| 9 | **Outgoing channel header** |
| 10 | Outgoing: real central + volume imaginary (type +1) |
| 11 | Outgoing: surface imaginary (type +2) |
| 12 | Outgoing: spin-orbit (type -4) |
| 13 | **Bound state header** |
| 14 | Bound: central WS (type ±1, auto-depth=-1) |
| 15 | Bound: spin-orbit (type -4, separate card) |
| 16 | Quantum numbers: nodes, l, 2j, step, R_max |
| 17 | `9` = end of data |

---

## Channel Header Format (Cards 5, 9, 13)

**Critical**: All values must be in correct 8-char field positions.

```
F1       F2       F3       F4       F5       F6       F7       F8
ELAB     MASSP    ZP       MASST    ZT       RC0      (blank)  PNLOC
```

| Field | F1 | F2 | F3 | F4 | F5 | F6 | F7 | F8 |
|-------|----|----|----|----|----|----|----|----|
| **Card 5** | E_lab | m_d=2 | Z_d=1 | m_target | Z_target | rc0_in | 0 | **PNLOC=2.0** |
| **Card 9** | Q-value | m_p=1 | Z_p=1 | m_residual | Z_residual | rc0_out | 0 | **PNLOC=1.0** |
| **Card 13** | −Sn | m_n=1 | Z_n=0 | m_core | Z_core | rc0_bound | 0 | **PNLOC=1.0** |

> [!CAUTION]
> **PNLOC must be in field F8 (columns 57–64).** If it falls in the wrong column, DWUCK4 reads it as `2*STR` (spin) instead, and non-locality corrections are silently disabled. This was the cause of a ~25% normalization error.

### Non-locality parameters
- Deuteron: **PNLOC = 2.0** fm
- Proton: **PNLOC = 1.0** fm
- Neutron (bound): **PNLOC = 1.0** fm

---

## Potential Parameter Conversions

### Scattering Channels (Cards 6–8, 10–12)

> [!WARNING]
> **All three potential cards (type +1, +2, -4) must always be present** for each scattering channel, even if the OMP has zero spin-orbit (e.g. Perey & Perey). Use all-zero values: `-4. +0.000 +0.000 +0.000 +0.000 +0.000 +0.000`. Omitting the card shifts all subsequent cards and produces NaN cross sections.

| Ptolemy parameter | DWUCK4 conversion | Formula |
|---|---|---|
| V (real central) | Sign flip | `DWUCK = −V` |
| r₀, a | Direct | unchanged |
| Wᵢ (volume imaginary) | Sign flip | `DWUCK = −Wᵢ` |
| rᵢ₀, aᵢ | Direct | unchanged |
| **Wsᵢ (surface imaginary)** | **×4a, positive** | **`DWUCK = +Wsᵢ × 4 × asᵢ`** |
| rsᵢ₀, asᵢ | Direct | unchanged |
| **Vso (real spin-orbit)** | **×4, sign flip** | **`DWUCK = −Vso × 4`** |
| rso₀, aso | Direct | unchanged |
| **Wsoᵢ (imag spin-orbit)** | **×4, positive** | **`DWUCK = +|Wsoᵢ| × 4`** |
| rsoᵢ₀, asoᵢ | Direct | unchanged |

### Verification (S-36 AK set)

| Parameter | Ptolemy | Formula | DWUCK4 | Match? |
|---|---|---|---|---|
| In Wsᵢ | 10.340 | ×4×0.736 | +30.441 | ✅ |
| In Vso | 3.557 | ×4 | −14.228 | ✅ |
| Out Wsᵢ | 8.619 | ×4×0.538 | +18.548 | ✅ |
| Out Vso | 5.438 | ×4 | −21.752 | ✅ |
| Out Wsoᵢ | −0.080 | ×4×|val| | +0.320 | ✅ |

### Physics Origin

The factor of **4** in spin-orbit comes from the Thomas form: DWUCK4 uses `Vso × (ℏ/mπc)² × (1/r)(dV/dr)` where `(ℏ/mπc)² ≈ 2.0 fm²`, giving an effective ×4 relative to Ptolemy's convention.

The factor of **4a** in surface imaginary comes from the derivative Woods-Saxon: DWUCK4 defines the surface form without the `4a` prefactor that Ptolemy includes, so the user must pre-multiply.

---

## Bound State (Cards 13–16)

### Card 14: Central WS potential

```
type   depth   r0     a
-1.    -1.     +1.25  +0.65
```

- `type = -1` → Woods-Saxon with auto-depth search
- `depth = -1` → DWUCK4 auto-calculates V to match binding energy (−Sn on Card 13)
- `r0, a` → from Ptolemy target bound-state parameters

### Card 15: Spin-orbit

The bound-state SO convention differs between bound and unbound states:

| Case | Card format | Vso value |
|---|---|---|
| **Bound** | Separate type −4 card | Raw Ptolemy Vso (no ×4) |
| **Unbound** | Same line as Card 14, field 5 | Vso × 4 |

**Bound** (separate card):
```
-4.    -6.000  +1.10  +0.65
```

**Unbound** (on Card 14):
```
-1.    -1.     +1.250  +0.650  24.000  +1.100  +0.650
```

> [!IMPORTANT]
> For **bound states**, use the raw Ptolemy Vso on a separate type −4 card. Using ×4 causes the depth search to fail.
> For **unbound states**, put Vso×4 on the same line as the central WS (field 5 with SO geometry in fields 6–7).

### Card 16: Quantum numbers

```
nodes   l      2j     step   rmax
+0.     +2.    +5.    +1.    +50.
```

- `nodes` = n−1 (Ptolemy convention)
- `l` = orbital angular momentum of transferred neutron
- `2j` = 2 × total j of transferred neutron

---

## Output Units

| Quantity | DWUCK4 unit | To convert to mb/sr |
|---|---|---|
| dσ/dΩ (Inelsig) | fm²/sr | **×10** |
| σ_tot (Tot-sig) | fm² | ×10 for mb |

DWUCK4 computes cross sections for **unit spectroscopic factor** (C²S = 1). Ptolemy includes the deuteron S-state probability (e.g. S_AV18 = 0.9422 for AV18 wavefunction), so:

```
σ_Ptolemy ≈ σ_DWUCK4 × 10 × S_deuteron
```

Expected ratio: Ptolemy(mb/sr) / DWUCK4(fm²/sr) ≈ 10 × 0.94 ≈ **9.4**

---

## Unbound States

When Ex > Sn (excitation energy above neutron separation energy), the transferred neutron is unbound. DWUCK4 handles this with different control codes and parameters.

### Differences from bound states

| Parameter | Bound | Unbound |
|---|---|---|
| Control code | `1001000000200000` | **`1011000030000000`** |
| LMAX (Card 3) | 30 | **15** |
| RMAX (Card 4) | +50 | **−15** (negative for unbound matching) |
| Card 13 energy | −Sn (negative) | **+(Ex−Sn)** (positive) |
| Q-value (Card 9) | Q_gs | **Q_gs − Ex** |
| Bound SO (Card 14) | Separate −4 card, raw Vso | **Same line**, Vso×4 |

### Control code breakdown
- Digit 3 = `1` → unbound form factor calculation
- Digit 9 = `3` → special integration matching for continuum states

> [!NOTE]
> Ptolemy cannot compute unbound states (its bound-state solver fails with positive binding energy). The OMP parameters must be taken from the `.in.a` file directly.

---

## Example Templates

### Bound state (10Be GS, AK set)

```
1001000000200000    10Be(d,p)11Be  17.4MeV  0 keV  0d5/2 bound AK
+61.000 +0.000  +1.000  
+30+01+0205
+0.100  +0.000  +50.000 
+17.400 +2.000  +1.000  +10.000 +4.000  +1.303          +2.000  
+1.     -88.744 +1.148  +0.746          -2.186  +1.351  +0.640  
+2.     +0.000  +0.000  +0.000          +27.393 +1.405  +0.665  
-4.     -14.228 +0.972  +1.011          +0.000  +0.000  +0.000  
-1.721  +1.000  +1.000  +11.000 +4.000  +1.578          +1.000  
+1.     -55.917 +1.122  +0.676          -1.202  +1.122  +0.676  
+2.     +0.000  +0.000  +0.000          +20.742 +1.307  +0.524  
-4.     -21.800 +0.894  +0.590          +0.232  +0.894  +0.590  
-0.504  +1.000  +0.000  +10.000 +4.000  +1.300          +1.000  
+1.     -1.     +1.250  +0.650  
-4.     -6.000  +1.100  +0.650  
+0.000  +2.000  +5.000  +1.000  +50.000 
9                   END OF DATA for DWUCK4
```

### Unbound state (10Be Ex=1.78, AK set)

```
1011000030000000    10Be(d,p)11Be  17.4MeV  1780 keV  0d5/2 unbound AK
+61.000 +0.000  +1.000  
+15+01+0205
+0.100  +0.000  -15.000 
+17.400 +2.000  +1.000  +10.000 +4.000  +1.303          +2.000  
+1.     -88.744 +1.148  +0.746          -2.186  +1.351  +0.640  
+2.     +0.000  +0.000  +0.000          +27.393 +1.405  +0.665  
-4.     -14.228 +0.972  +1.011          +0.000  +0.000  +0.000  
-3.501  +1.000  +1.000  +11.000 +4.000  +1.578          +1.000  
+1.     -55.917 +1.122  +0.676          -1.202  +1.122  +0.676  
+2.     +0.000  +0.000  +0.000          +20.742 +1.307  +0.524  
-4.     -21.800 +0.894  +0.590          +0.232  +0.894  +0.590  
+1.276  +1.000  +0.000  +10.000 +4.000  +1.300          +1.000  
-1.     -1.     +1.250  +0.650  24.000  +1.100  +0.650  
+0.000  +2.000  +5.000  +1.000  +50.000 
9                   END OF DATA for DWUCK4
```
