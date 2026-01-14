# PTOLEMY Parameters for ³⁶S(d,p)³⁷S Ground State

Extracted from: `ptolemy/s36dp_reference.out`  
Calculation date: 03 Oct 25

## Reaction Kinematics

| Parameter | Value | Units |
|-----------|-------|-------|
| Reaction | ³⁶S(d,p)³⁷S | |
| Target nucleus | ³⁶S | |
| Projectile | d (deuteron) | |
| Ejectile | p (proton) | |
| Beam energy (Lab) | 16.000 | MeV |
| Beam energy (CM) | 15.152 | MeV |
| Q-value | +2.0790 | MeV |
| Final state energy | 0.0000 | MeV |
| Final state J^π | 1/2+ | |

## Projectile Bound State (Deuteron)

| Parameter | Value | Description |
|-----------|-------|-------------|
| Type | AV18 | Argonne v18 wavefunction |
| Binding energy | -2.2246 | MeV |
| L | 0 | Orbital angular momentum |
| Nodes | 0 | Radial nodes |
| r0 | 1.0000 | fm |
| a | 0.5000 | fm |
| rc0 | 1.2000 | fm |
| S-state probability | 0.9422 | |
| Spectroscopic amplitude | 0.97069 | |

## Target Bound State (³⁶S + n → ³⁷S)

| Parameter | Value | Description |
|-----------|-------|-------------|
| Binding energy | -4.3036 | MeV |
| L | 0 | Orbital angular momentum |
| J^π | 1/2+ | Angular momentum / parity |
| Nodes | 1 | Radial nodes |
| V_well | 36.439 | MeV (adjusted from initial 78.47) |
| r0 | 1.25 | fm |
| a | 0.65 | fm |
| V_so | 6.0000 | MeV (spin-orbit) |
| r0_so | 1.10 | fm |
| a_so | 0.65 | fm |
| rc0 | 1.3 | fm |

## Incoming Channel OMP (d + ³⁶S)

**Reference**: An and Cai (2006), Phys. Rev. C 73, 054605

| Parameter | Value | Description |
|-----------|-------|-------------|
| V | 91.007 | MeV (real central) |
| r0 | 1.150 | fm |
| a | 0.761 | fm |
| W_v | 2.099 | MeV (volume imaginary) |
| r0_i | 1.335 | fm |
| a_i | 0.525 | fm |
| W_s | 10.340 | MeV (surface imaginary) |
| r0_si | 1.380 | fm |
| a_si | 0.736 | fm |
| V_so | 3.557 | MeV (real spin-orbit) |
| r0_so | 0.972 | fm |
| a_so | 1.011 | fm |
| W_so | 0.000 | MeV (imag spin-orbit) |
| rc0 | 1.303 | fm (Coulomb radius) |

## Outgoing Channel OMP (p + ³⁷S)

**Reference**: Koning and Delaroche (2009), Nucl. Phys. A 713, 231

| Parameter | Value | Description |
|-----------|-------|-------------|
| V | 52.968 | MeV (real central) |
| r0 | 1.182 | fm |
| a | 0.672 | fm |
| W_v | 1.553 | MeV (volume imaginary) |
| r0_i | 1.182 | fm |
| a_i | 0.672 | fm |
| W_s | 8.619 | MeV (surface imaginary) |
| r0_si | 1.290 | fm |
| a_si | 0.538 | fm |
| V_so | 5.438 | MeV (real spin-orbit) |
| r0_so | 0.991 | fm |
| a_so | 0.590 | fm |
| W_so | -0.080 | MeV (imag spin-orbit) |
| rc0 | 1.292 | fm (Coulomb radius) |

## Computational Settings

| Parameter | Value | Description |
|-----------|-------|-------------|
| LMAX | 30 | Maximum orbital angular momentum |
| LSTEP | 1 | L-value step size |
| LMIN | 0 | Minimum L-value |
| Angular min | 0.0 | degrees |
| Angular max | 90.0 | degrees |
| Angular step | 1.0 | degrees |
| Asymptopia (incoming) | 26.75 | fm |
| Asymptopia (outgoing) | 34.625 | fm |

## Key Results (for validation)

| Angle (deg) | σ (mb/sr) | σ/σ_Ruth |
|-------------|-----------|----------|
| 0.0 | 80.537 | 0.000000 |
| 10.0 | 28.928 | 0.001314 |
| 20.0 | 2.1825 | 0.001562 |
| 30.0 | 5.3948 | 0.019050 |
| 40.0 | 1.2957 | 0.013952 |
| 50.0 | 0.66541 | 0.016704 |
| 60.0 | 0.95188 | 0.046815 |
| 70.0 | 0.53076 | 0.045205 |
| 80.0 | 0.26644 | 0.035792 |
| 90.0 | 0.17300 | 0.034033 |

**Total integrated cross-section**: 14.495 mb/sr
