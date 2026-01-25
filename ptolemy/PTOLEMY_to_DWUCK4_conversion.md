# PTOLEMY to DWUCK4 Parameter Conversion

## Overview

This document describes the conversion of optical model parameters from PTOLEMY format to DWUCK4 format for the ³⁶S(d,p)³⁷S reaction at 16 MeV.

Two DWUCK4 input files were created:
1. **DW_36S_DP_AK_GS.in** - Using An & Cai (2006) + Koning & Delaroche (2009) parameters
2. **DW_36S_DP_QP_GS.in** - Using Perey & Perey (1963) + Perey (1963) parameters

---

## Input Files Created

| File | Deuteron OMP | Proton OMP | Location |
|------|--------------|------------|----------|
| [DW_36S_DP_AK_GS.in](file:///Users/calemhoffman/Documents/GitHub/DWUCK4/inputs/DW_36S_DP_AK_GS.in) | An & Cai (2006) | Koning & Delaroche (2009) | `inputs/` |
| [DW_36S_DP_QP_GS.in](file:///Users/calemhoffman/Documents/GitHub/DWUCK4/inputs/DW_36S_DP_QP_GS.in) | Perey & Perey (1963) | Perey (1963) | `inputs/` |

---

## Conversion Details

### Common Parameters (Both Files)

- **Beam Energy**: 16.000 MeV
- **Target**: ³⁶S (A=36, Z=16)
- **Residual**: ³⁷S (A=37, Z=16)
- **Final State**: 7/2⁻ ground state (Ex = 0.000 MeV)
- **L-transfer**: 3 (0f7/2 orbital)
- **Q-value**: +2.079 MeV
- **Binding Energy**: -4.304 MeV
- **Angular Range**: 0° to 90° in 1° steps
- **LMAX**: 30

### Bound State Potential (Card 14-15)

From PTOLEMY target configuration:
- **r₀**: 1.25 fm
- **a**: 0.65 fm
- **Vso**: 6.000 MeV
- **rso₀**: 1.10 fm
- **aso**: 0.65 fm
- **rc₀**: 1.3 fm

---

## Parameter Mapping: PTOLEMY → DWUCK4

### Deuteron Optical Potential (Cards 5-8)

DWUCK4 uses three cards for the optical potential:
- **Card type +01**: Real central potential (V, r₀, a) and Imaginary volume (Wᵢ, rᵢ₀, aᵢ)
- **Card type +02**: Zero padding and Imaginary surface (Wsᵢ, rsᵢ₀, asᵢ)
- **Card type -04**: Real spin-orbit (Vso, rso₀, aso) and Imaginary spin-orbit (Wsoᵢ, rsoᵢ₀, asoᵢ)

#### AK Set Deuteron (An & Cai 2006)

```
PTOLEMY → DWUCK4
V = 91.007 → +01. -91.007 +01.150 +00.761
Wᵢ = 2.099 → (same line) -02.099 +01.335 +00.525
Wsᵢ = 10.340 → +02. +00.000 +00.000 +00.000 +10.340 +01.380 +00.736
Vso = 3.557 → -04. -03.557 +00.972 +01.011 +00.000 +00.000 +00.000
rc₀ = 1.303 fm (in Card 5)
```

#### QP Set Deuteron (Perey & Perey 1963)

```
PTOLEMY → DWUCK4
V = 87.171 → +01. -87.171 +01.150 +00.810
Wᵢ = 0.000 → (same line) +00.000 +00.000 +00.000
Wsᵢ = 18.240 → +02. +00.000 +00.000 +00.000 +18.240 +01.340 +00.680
Vso = 0.000 → -04. +00.000 +00.000 +00.000 +00.000 +00.000 +00.000
rc₀ = 1.150 fm (in Card 5)
```

**Key difference**: QP set has no volume absorption (Wᵢ=0) or spin-orbit term (Vso=0).

---

### Proton Optical Potential (Cards 10-12)

Same three-card structure as deuteron.

#### AK Set Proton (Koning & Delaroche 2009)

```
PTOLEMY → DWUCK4
V = 52.968 → +01. -52.968 +01.182 +00.672
Wᵢ = 1.553 → (same line) -01.553 +01.182 +00.672
Wsᵢ = 8.619 → +02. +00.000 +00.000 +00.000 +08.619 +01.290 +00.538
Vso = 5.438 → -04. -05.438 +00.991 +00.590
Wsoᵢ = -0.080 → (same line) +00.080 +00.991 +00.590
rc₀ = 1.292 fm (in Card 9)
```

**Note**: Imaginary spin-orbit sign is flipped in DWUCK4 format (+0.080 vs -0.080).

#### QP Set Proton (Perey 1963)

```
PTOLEMY → DWUCK4
V = 48.926 → +01. -48.926 +01.250 +00.650
Wᵢ = 0.000 → (same line) +00.000 +00.000 +00.000
Wsᵢ = 13.500 → +02. +00.000 +00.000 +00.000 +13.500 +01.250 +00.470
Vso = 7.500 → -04. -07.500 +01.250 +00.470 +00.000 +00.000 +00.000
Wsoᵢ = 0.000 → (same line) +00.000 +00.000 +00.000
rc₀ = 1.250 fm (in Card 9)
```

**Key difference**: QP set has no volume absorption (Wᵢ=0) or imaginary spin-orbit (Wsoᵢ=0).

---

## Sign Conventions

> [!WARNING]
> DWUCK4 uses **negative signs** for attractive potentials (V and Vso), which is opposite to the PTOLEMY convention where values are positive for attractive potentials.

### Sign Conversion Rules

| Potential Type | PTOLEMY | DWUCK4 | Note |
|----------------|---------|--------|------|
| Real Central (V) | Positive | **Negative** | Attractive → negative |
| Imaginary Volume (Wᵢ) | Positive | **Negative** | Absorptive → negative |
| Imaginary Surface (Wsᵢ) | Positive | **Positive** | Surface derivative form |
| Real Spin-Orbit (Vso) | Positive | **Negative** | Attractive → negative |
| Imag Spin-Orbit (Wsoᵢ) | Negative | **Positive** | Sign flip (unclear convention) |

---

## Field Format Notes

DWUCK4 requires **strict fixed-format Fortran input**:

1. **Energies and potentials**: Format as `+XX.XXX` or `-XX.XXX`
2. **Radius parameters**: Format as `+XX.XXX`
3. **Card type indicators**: `+01.`, `+02.`, `-04.` at the start of optical potential cards
4. **Exact spacing**: Maintain column positions as shown in the templates

---

## Verification Recommendations

To verify these conversions:

1. **Run DWUCK4** with both input files:
   ```bash
   ./DWUCK4.exe < inputs/DW_36S_DP_AK_GS.in > outputs/AK_GS.out
   ./DWUCK4.exe < inputs/DW_36S_DP_QP_GS.in > outputs/QP_GS.out
   ```

2. **Compare with PTOLEMY output** from `s36dp_ex000.in.a`:
   - Extract cross sections from PTOLEMY output
   - Plot DWUCK4 vs PTOLEMY for both AK and QP sets
   - Calculate χ² and normalization factors

3. **Expected differences**:
   - Spectroscopic factor normalization may differ
   - Shape should be very similar if parameters are correct
   - AK and QP sets should show systematic differences

---

## Parameter Validity Ranges

### AK Set
- **Deuteron**: E < 183 MeV, 12 < A < 238 ✓ (16 MeV, A=36)
- **Proton**: 0.001 < E < 200 MeV, 24 < A < 209 ✓ (2.079 MeV, A=37)

### QP Set
- **Deuteron**: 12 < E < 25 MeV, A > 40 ⚠️ (16 MeV ✓, A=36 slightly below A>40)
- **Proton**: E < 20 MeV, 30 < A < 100 ✓ (2.079 MeV, A=37 ✓)

> [!CAUTION]
> The QP deuteron parameters (Perey & Perey 1963) specify A > 40, but we're using A=36. This is a slight extrapolation that may affect accuracy.

---

## References

Source parameter summary: [s36dp_ex000_parameters_summary.md](file:///Users/calemhoffman/Documents/GitHub/DWUCK4/ptolemy/s36dp_ex000_parameters_summary.md)

DWUCK4 format guide: [INPUT_PARAMETER_GUIDE.md](file:///Users/calemhoffman/Documents/GitHub/DWUCK4/INPUT_PARAMETER_GUIDE.md)
