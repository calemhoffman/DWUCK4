# Optical Model Parameters for ex199 (1.991 MeV, 3/2⁻, 1p3/2)

## Reaction
- **Reaction**: ³⁶S(d,p)³⁷S
- **Final State**: 3/2⁻ at 1.991 MeV
- **Beam Energy**: 16.000 MeV (lab frame)
- **Orbital**: 1p3/2 (ℓ=1, nodes=1)

## Bound State (Target) Parameters
- **Target Ground State**: J^π = 0⁺
- **Transferred Neutron**:
  - Orbital angular momentum: ℓ = 1
  - Total angular momentum: j = 3/2
  - Radial nodes: n = 1 (nodes parameter = n-1 = 1)
  - Geometry: r₀ = 1.25 fm, a = 0.65 fm
  - Spin-orbit: V_so = 6 MeV, r_so = 1.10 fm, a_so = 0.65 fm
  - Coulomb radius: r_c = 1.3 fm

## Projectile (Deuteron) Parameters
- **Wavefunction**: av18
- **Geometry**: r₀ = 1.0 fm, a = 0.5 fm, ℓ = 0, r_c = 1.2 fm

---

## AK (Akyüz-Winther) Potential Set

### Incoming Channel (d + ³⁶S)
**Reference**: An and Cai (2006), Phys. Rev. C 73, 054605  
**Validity**: E < 183 MeV, 12 < A < 238

| Parameter | Value (MeV) | r₀ (fm) | a (fm) |
|-----------|-------------|---------|--------|
| V (real volume) | 91.007 | 1.150 | 0.761 |
| W_v (imag. volume) | 2.099 | 1.335 | 0.525 |
| W_s (imag. surface) | 10.340 | 1.380 | 0.736 |
| V_so (real spin-orbit) | 3.557 | 0.972 | 1.011 |
| W_so (imag. spin-orbit) | 0.000 | 0.000 | 0.000 |
| **Coulomb radius**: r_c = 1.303 fm

### Outgoing Channel (p + ³⁷S)
**Reference**: Koning and Delaroche (2003), Nucl. Phys. A 713, 231  
**Validity**: 0.001 < E < 200 MeV, 24 < A < 209 (Isospin dependent)

| Parameter | Value (MeV) | r₀ (fm) | a (fm) |
|-----------|-------------|---------|--------|
| V (real volume) | 53.770 | 1.182 | 0.672 |
| W_v (imag. volume) | 1.345 | 1.182 | 0.672 |
| W_s (imag. surface) | 8.754 | 1.290 | 0.538 |
| V_so (real spin-orbit) | 5.481 | 0.991 | 0.590 |
| W_so (imag. spin-orbit) | -0.068 | 0.991 | 0.590 |
| **Coulomb radius**: r_c = 1.292 fm

---

## QP (Queueille-Greenlees/Perey) Potential Set

### Incoming Channel (d + ³⁶S)
**Reference**: Perey and Perey (1963), At. Data Nucl. Data Tables 17, 1  
**Validity**: 12 < E < 25 MeV, A > 40

| Parameter | Value (MeV) | r₀ (fm) | a (fm) |
|-----------|-------------|---------|--------|
| V (real volume) | 87.171 | 1.150 | 0.810 |
| W_v (imag. volume) | 0.000 | 0.000 | 0.000 |
| W_s (imag. surface) | 18.240 | 1.340 | 0.680 |
| V_so (real spin-orbit) | 0.000 | 0.000 | 0.000 |
| W_so (imag. spin-orbit) | 0.000 | 0.000 | 0.000 |
| **Coulomb radius**: r_c = 1.150 fm

### Outgoing Channel (p + ³⁷S)
**Reference**: Perey (1963), At. Data Nucl. Data Tables 5, 17  
**Validity**: E < 20 MeV, 30 < A < 100

| Parameter | Value (MeV) | r₀ (fm) | a (fm) |
|-----------|-------------|---------|--------|
| V (real volume) | 50.021 | 1.250 | 0.650 |
| W_v (imag. volume) | 0.000 | 0.000 | 0.000 |
| W_s (imag. surface) | 13.500 | 1.250 | 0.470 |
| V_so (real spin-orbit) | 7.500 | 1.250 | 0.470 |
| W_so (imag. spin-orbit) | 0.000 | 0.000 | 0.000 |
| **Coulomb radius**: r_c = 1.250 fm

---

## Notes for DWUCK Input

1. **Potential Form**: Woods-Saxon for all components
2. **Angular Range**: 0° to 60° in 1° steps
3. **Partial Wave Expansion**: ℓ_min = 0, ℓ_max = 30
4. **Asymptotic Matching**: 50 fm
5. **Spectroscopic Factor**: To be determined from normalization fits
6. **Key Difference AK vs QP**:
   - AK uses modern global potentials with volume + surface absorption
   - QP uses older phenomenological potentials with surface-only absorption
