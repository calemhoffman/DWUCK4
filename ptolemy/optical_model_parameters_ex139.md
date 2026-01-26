# Optical Model Parameters for ex139 (1.398 MeV, 3/2⁺)

## Reaction
- **Reaction**: ³⁶S(d,p)³⁷S
- **Final State**: 3/2⁺ at 1.398 MeV
- **Beam Energy**: 16.000 MeV (lab frame)
- **Two Orbital Assignments Tested**:
  1. **0d3/2**: ℓ=2, nodes=0 (preferred based on χ²)
  2. **1p3/2**: ℓ=1, nodes=1 (better fit: χ²/ν ≈ 1.7 vs 3.1)

---

## 0d3/2 Assignment Parameters

### Bound State (Target) Parameters
- **Target Ground State**: J^π = 0⁺
- **Transferred Neutron**:
  - Orbital angular momentum: ℓ = 2
  - Total angular momentum: j = 3/2
  - Radial nodes: n = 0 (nodes parameter = n-1 = 0)
  - Geometry: r₀ = 1.25 fm, a = 0.65 fm
  - Spin-orbit: V_so = 6 MeV, r_so = 1.10 fm, a_so = 0.65 fm
  - Coulomb radius: r_c = 1.3 fm

### Projectile (Deuteron) Parameters
- **Wavefunction**: av18
- **Geometry**: r₀ = 1.0 fm, a = 0.5 fm, ℓ = 0, r_c = 1.2 fm

### AK (Akyüz-Winther) Potential Set

#### Incoming Channel (d + ³⁶S)
**Reference**: An and Cai (2006), Phys. Rev. C 73, 054605

| Parameter | Value (MeV) | r₀ (fm) | a (fm) |
|-----------|-------------|---------|--------|
| V | 91.007 | 1.150 | 0.761 |
| W_v | 2.099 | 1.335 | 0.525 |
| W_s | 10.340 | 1.380 | 0.736 |
| V_so | 3.557 | 0.972 | 1.011 |
| W_so | 0.000 | 0.000 | 0.000 |
| r_c = 1.303 fm

#### Outgoing Channel (p + ³⁷S)
**Reference**: Koning and Delaroche (2003), Nucl. Phys. A 713, 231

| Parameter | Value (MeV) | r₀ (fm) | a (fm) |
|-----------|-------------|---------|--------|
| V | 53.530 | 1.182 | 0.672 |
| W_v | 1.406 | 1.182 | 0.672 |
| W_s | 8.719 | 1.290 | 0.538 |
| V_so | 5.468 | 0.991 | 0.590 |
| W_so | -0.071 | 0.991 | 0.590 |
| r_c = 1.292 fm

### QP (Queueille-Greenlees/Perey) Potential Set

#### Incoming Channel (d + ³⁶S)
**Reference**: Perey and Perey (1963)

| Parameter | Value (MeV) | r₀ (fm) | a (fm) |
|-----------|-------------|---------|--------|
| V | 87.171 | 1.150 | 0.810 |
| W_v | 0.000 | 0.000 | 0.000 |
| W_s | 18.240 | 1.340 | 0.680 |
| V_so | 0.000 | 0.000 | 0.000 |
| W_so | 0.000 | 0.000 | 0.000 |
| r_c = 1.150 fm

#### Outgoing Channel (p + ³⁷S)
**Reference**: Perey (1963)

| Parameter | Value (MeV) | r₀ (fm) | a (fm) |
|-----------|-------------|---------|--------|
| V | 49.695 | 1.250 | 0.650 |
| W_v | 0.000 | 0.000 | 0.000 |
| W_s | 13.500 | 1.250 | 0.470 |
| V_so | 7.500 | 1.250 | 0.470 |
| W_so | 0.000 | 0.000 | 0.000 |
| r_c = 1.250 fm

---

## 1p3/2 Assignment Parameters (Better Fit)

### Bound State (Target) Parameters
- **Target Ground State**: J^π = 0⁺
- **Transferred Neutron**:
  - Orbital angular momentum: ℓ = 1
  - Total angular momentum: j = 3/2
  - Radial nodes: n = 1 (nodes parameter = n-1 = 1)
  - Geometry: r₀ = 1.25 fm, a = 0.65 fm
  - Spin-orbit: V_so = 6 MeV, r_so = 1.10 fm, a_so = 0.65 fm
  - Coulomb radius: r_c = 1.3 fm

### Projectile (Deuteron) Parameters
- **Wavefunction**: av18
- **Geometry**: r₀ = 1.0 fm, a = 0.5 fm, ℓ = 0, r_c = 1.2 fm

### AK and QP Potential Sets
**Same as 0d3/2 assignment** (optical potentials are independent of transferred orbital)

---

## Fitting Results Summary

| Assignment | Potential | Normalization | χ²/ν | Conclusion |
|------------|-----------|---------------|------|------------|
| 0d3/2 | AK | 2.93 ± 0.28 | 3.13 | Poor fit |
| 0d3/2 | QP | 2.96 ± 0.28 | 3.15 | Poor fit |
| **1p3/2** | **AK** | **1.28 ± 0.12** | **1.75** | **Good fit** ✓ |
| **1p3/2** | **QP** | **1.32 ± 0.12** | **1.72** | **Good fit** ✓ |

**Recommendation**: The 1p3/2 assignment is strongly preferred based on χ² values.

---

## Notes for DWUCK Input

1. **Potential Form**: Woods-Saxon for all components
2. **Angular Range**: 0° to 60° in 1° steps
3. **Partial Wave Expansion**: ℓ_min = 0, ℓ_max = 30
4. **Asymptotic Matching**: 50 fm
5. **Spectroscopic Factor**: To be determined from normalization fits
6. **Recommended Assignment**: Use 1p3/2 (ℓ=1, n=1) based on superior fit quality
