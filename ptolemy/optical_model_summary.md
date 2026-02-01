# PTOLEMY Optical Model Parameters Summary
## ³⁶S(d,p)³⁷S Ex=4.858 MeV (5/2⁻) Calculation

This document summarizes the optical model parameters and calculation settings used in the PTOLEMY input file `s36dp_ex485.in.a`.

---

## Reaction Details

- **Reaction**: ³⁶S(d,p)³⁷S
- **Final State**: 5/2⁻ at 4.858 MeV
- **Beam Energy**: E_lab = 16.000 MeV
- **Angular Range**: 0° to 60° in 1° steps
- **Excitation Energies Scanned**: -2.0, -1.8, -1.6, -1.4, -1.2, -1.0, -0.8, -0.6, -0.4, -0.2 MeV
- **Optical Models**: AK (An & Cai) and QP (Perey & Perey)

---

## Common Parameters (All Calculations)

### Calculation Settings
- **Parameter Set**: `dpsb r0target`
- **Angular Momentum**: `lstep=1`, `lmin=0`, `lmax=30`
- **Extrapolation**: `maxlextrap=0`
- **Asymptotic Distance**: 50 fm

### Projectile (Deuteron)
- **Wavefunction**: AV18
- **Geometry**:
  - r₀ = 1.0 fm
  - a = 0.5 fm
  - ℓ = 0
  - r_c0 = 1.2 fm

### Target (Bound Neutron in ³⁷S)
- **Target Spin**: J_A = 0⁺ (³⁶S ground state)
- **Transferred Neutron**:
  - Orbital: 0f₅/₂ (nodes=0, ℓ=3, j^π=5/2⁻)
  - **Binding Energy (E)**: Varies from -2.0 to -0.2 MeV (10 values)
- **Geometry**:
  - r₀ = 1.25 fm
  - a = 0.65 fm
  - r_c0 = 1.3 fm
- **Spin-Orbit**:
  - V_so = 6.0 MeV
  - r_so0 = 1.10 fm
  - a_so = 0.65 fm

---

## Optical Model Parameters (Entrance Channel: d + ³⁶S)

### AK Model: An & Cai (2006)
**Reference**: Phys. Rev. C **73**, 054605 (2006)  
**Validity**: E < 183 MeV, 12 < A < 238

| Potential | Depth (MeV) | r₀ (fm) | a (fm) |
|-----------|-------------|---------|--------|
| Real (V) | 91.007 | 1.150 | 0.761 |
| Imaginary Volume (W_i) | 2.099 | 1.335 | 0.525 |
| Imaginary Surface (W_si) | 10.340 | 1.380 | 0.736 |
| Spin-Orbit Real (V_so) | 3.557 | 0.972 | 1.011 |
| Spin-Orbit Imag (W_soi) | 0.000 | - | - |
| Coulomb r_c0 | - | 1.303 | - |

### QP Model: Perey & Perey (1963)
**Reference**: At. Data Nucl. Data Tables **17**, 1 (1976)  
**Validity**: 12 < E < 25 MeV, A > 40

| Potential | Depth (MeV) | r₀ (fm) | a (fm) |
|-----------|-------------|---------|--------|
| Real (V) | 87.171 | 1.150 | 0.810 |
| Imaginary Volume (W_i) | 0.000 | - | - |
| Imaginary Surface (W_si) | 18.240 | 1.340 | 0.680 |
| Spin-Orbit Real (V_so) | 0.000 | - | - |
| Spin-Orbit Imag (W_soi) | 0.000 | - | - |
| Coulomb r_c0 | - | 1.150 | - |

---

## Optical Model Parameters (Exit Channel: p + ³⁷S)

### AK Model: Koning & Delaroche (2003)
**Reference**: Nucl. Phys. A **713**, 231 (2003)  
**Validity**: 0.001 < E < 200 MeV, 24 < A < 209, Isospin-dependent

| Potential | Depth (MeV) | r₀ (fm) | a (fm) |
|-----------|-------------|---------|--------|
| Real (V) | 54.939 | 1.182 | 0.672 |
| Imaginary Volume (W_i) | 1.064 | 1.182 | 0.672 |
| Imaginary Surface (W_si) | 8.839 | 1.290 | 0.538 |
| Spin-Orbit Real (V_so) | 5.544 | 0.991 | 0.590 |
| Spin-Orbit Imag (W_soi) | -0.053 | 0.991 | 0.590 |
| Coulomb r_c0 | - | 1.292 | - |

### QP Model: Perey (1963)
**Reference**: At. Data Nucl. Data Tables **17**, 1 (1976)  
**Validity**: E < 20 MeV, 30 < A < 100

| Potential | Depth (MeV) | r₀ (fm) | a (fm) |
|-----------|-------------|---------|--------|
| Real (V) | 51.598 | 1.250 | 0.650 |
| Imaginary Volume (W_i) | 0.000 | - | - |
| Imaginary Surface (W_si) | 13.500 | 1.250 | 0.470 |
| Spin-Orbit Real (V_so) | 7.500 | 1.250 | 0.470 |
| Spin-Orbit Imag (W_soi) | 0.000 | - | - |
| Coulomb r_c0 | - | 1.250 | - |

---

## Key Differences Between AK and QP Models

### Entrance Channel (d + ³⁶S)
| Feature | AK (An & Cai) | QP (Perey & Perey) |
|---------|---------------|---------------------|
| Real potential depth | 91.007 MeV | 87.171 MeV |
| Volume absorption | Yes (2.099 MeV) | No |
| Surface absorption | 10.340 MeV | 18.240 MeV |
| Real spin-orbit | Yes (3.557 MeV) | No |
| Diffuseness (a) | 0.761 fm | 0.810 fm |

### Exit Channel (p + ³⁷S)
| Feature | AK (Koning & Delaroche) | QP (Perey) |
|---------|-------------------------|------------|
| Real potential depth | 54.939 MeV | 51.598 MeV |
| Volume absorption | Yes (1.064 MeV) | No |
| Surface absorption | 8.839 MeV | 13.500 MeV |
| Real spin-orbit | 5.544 MeV | 7.500 MeV |
| Imaginary spin-orbit | Yes (-0.053 MeV) | No |
| Geometry r₀ | 1.182 fm | 1.250 fm |
| Diffuseness (a) | 0.672 fm | 0.650 fm |

---

## Calculation Structure

The input file contains **20 calculation blocks**:
- **10 excitation energies**: E = -2.0, -1.8, -1.6, -1.4, -1.2, -1.0, -0.8, -0.6, -0.4, -0.2 MeV
- **2 optical models** per energy: AK and QP

**Note**: The only parameter that varies across the 20 blocks (besides the optical model choice) is the binding energy `E` in the TARGET section, which scans from -2.0 to -0.2 MeV in 0.2 MeV steps. All other parameters remain constant for each optical model.

---

## Woods-Saxon Potential Form

All potentials use the Woods-Saxon form:

**Volume**: V(r) = -V₀ / [1 + exp((r - R)/a)]

**Surface Derivative**: W_D(r) = -4a_s W_s exp((r - R_s)/a_s) / [1 + exp((r - R_s)/a_s)]²

where R = r₀ × A^(1/3)

---

## Notes

1. The **AK model** uses more modern global optical model potentials with volume absorption and includes both real and imaginary spin-orbit terms in some channels.

2. The **QP model** uses older phenomenological potentials with purely surface absorption (no volume term) and simpler spin-orbit structure.

3. The binding energy scan (E = -2.0 to -0.2 MeV) explores the sensitivity of the calculated cross sections to the assumed single-particle energy of the transferred neutron, effectively probing different radial extents of the bound state wavefunction.

4. The actual experimental excitation energy is 4.858 MeV, but the binding energies used in the calculation are negative (bound state) values that represent the single-particle energy relative to the ³⁷S ground state.
