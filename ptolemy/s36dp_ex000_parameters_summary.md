# Parameter Summary for PTOLEMY Input: s36dp_ex000.in.a

## Reaction Overview

**Reaction**: ³⁶S(d,p)³⁷S  
**Final State**: 7/2⁻ ground state (Ex = 0.000 MeV)  
**Beam Energy**: ELAB = 16.000 MeV  
**Parameter Set**: dpsb r0target

## Two Calculation Sets

This input file contains **two complete calculations** using different global optical model potentials:
1. **AK Set** (Lines 1-33): An and Cai (2006) for deuteron, Koning and Delaroche (2009) for proton
2. **QP Set** (Lines 34-66): Perey and Perey (1963) for deuteron, Perey (1963) for proton

---

## Common Parameters (Both AK and QP Sets)

### Angular Momentum Settings
- **lstep**: 1
- **lmin**: 0
- **lmax**: 30
- **maxlextrap**: 0
- **asymptopia**: 50

### Projectile (Deuteron) Configuration
- **Wavefunction**: av18
- **r₀**: 1.0 fm
- **a**: 0.5 fm
- **l**: 0 (orbital angular momentum)
- **rc₀**: 1.2 fm (Coulomb radius parameter)

### Target (³⁶S) Configuration
- **JBIGA**: 0⁺ (ground state spin-parity)
- **nodes**: 0 (n-1 where n is principal quantum number)
- **l**: 3 (orbital angular momentum of transferred neutron)
- **jp**: 7/2⁻ (final state spin-parity)
- **r₀**: 1.25 fm
- **a**: 0.65 fm
- **vso**: 6.0 MeV (spin-orbit potential depth)
- **rso₀**: 1.10 fm (spin-orbit radius parameter)
- **aso**: 0.65 fm (spin-orbit diffuseness)
- **rc₀**: 1.3 fm (Coulomb radius parameter)

### Angular Distribution Settings
- **anglemin**: 0.000°
- **anglemax**: 90.000°
- **anglestep**: 1.000°

---

## AK Set: Optical Model Potentials

### INCOMING (Deuteron) Optical Potential
**Reference**: An and Cai (2006)  
**DOI**: http://dx.doi.org/10.1103/PhysRevC.73.054605  
**Validity**: E < 183 MeV, 12 < A < 238

| Parameter | Value | Description |
|-----------|-------|-------------|
| **V** | 91.007 MeV | Real central potential depth |
| **r₀** | 1.150 fm | Real central radius parameter |
| **a** | 0.761 fm | Real central diffuseness |
| **Wᵢ** | 2.099 MeV | Imaginary volume potential depth |
| **rᵢ₀** | 1.335 fm | Imaginary volume radius parameter |
| **aᵢ** | 0.525 fm | Imaginary volume diffuseness |
| **Wsᵢ** | 10.340 MeV | Imaginary surface potential depth |
| **rsᵢ₀** | 1.380 fm | Imaginary surface radius parameter |
| **asᵢ** | 0.736 fm | Imaginary surface diffuseness |
| **Vso** | 3.557 MeV | Real spin-orbit potential depth |
| **rso₀** | 0.972 fm | Real spin-orbit radius parameter |
| **aso** | 1.011 fm | Real spin-orbit diffuseness |
| **Wsoᵢ** | 0.000 MeV | Imaginary spin-orbit potential depth |
| **rsoᵢ₀** | 0.000 fm | Imaginary spin-orbit radius parameter |
| **asoᵢ** | 0.000 fm | Imaginary spin-orbit diffuseness |
| **rc₀** | 1.303 fm | Coulomb radius parameter |

### OUTGOING (Proton) Optical Potential
**Reference**: Koning and Delaroche (2009)  
**DOI**: http://dx.doi.org/10.1016/S0375-9474(02)01321-0  
**Validity**: 0.001 < E < 200 MeV, 24 < A < 209, Isospin Dependent

| Parameter | Value | Description |
|-----------|-------|-------------|
| **V** | 52.968 MeV | Real central potential depth |
| **r₀** | 1.182 fm | Real central radius parameter |
| **a** | 0.672 fm | Real central diffuseness |
| **Wᵢ** | 1.553 MeV | Imaginary volume potential depth |
| **rᵢ₀** | 1.182 fm | Imaginary volume radius parameter |
| **aᵢ** | 0.672 fm | Imaginary volume diffuseness |
| **Wsᵢ** | 8.619 MeV | Imaginary surface potential depth |
| **rsᵢ₀** | 1.290 fm | Imaginary surface radius parameter |
| **asᵢ** | 0.538 fm | Imaginary surface diffuseness |
| **Vso** | 5.438 MeV | Real spin-orbit potential depth |
| **rso₀** | 0.991 fm | Real spin-orbit radius parameter |
| **aso** | 0.590 fm | Real spin-orbit diffuseness |
| **Wsoᵢ** | -0.080 MeV | Imaginary spin-orbit potential depth |
| **rsoᵢ₀** | 0.991 fm | Imaginary spin-orbit radius parameter |
| **asoᵢ** | 0.590 fm | Imaginary spin-orbit diffuseness |
| **rc₀** | 1.292 fm | Coulomb radius parameter |

---

## QP Set: Optical Model Potentials

### INCOMING (Deuteron) Optical Potential
**Reference**: Perey and Perey (1963)  
**DOI**: http://dx.doi.org/10.1016/0370-1573(91)90039-O  
**Validity**: 12 < E < 25 MeV, A > 40

| Parameter | Value | Description |
|-----------|-------|-------------|
| **V** | 87.171 MeV | Real central potential depth |
| **r₀** | 1.150 fm | Real central radius parameter |
| **a** | 0.810 fm | Real central diffuseness |
| **Wᵢ** | 0.000 MeV | Imaginary volume potential depth |
| **rᵢ₀** | 0.000 fm | Imaginary volume radius parameter |
| **aᵢ** | 0.000 fm | Imaginary volume diffuseness |
| **Wsᵢ** | 18.240 MeV | Imaginary surface potential depth |
| **rsᵢ₀** | 1.340 fm | Imaginary surface radius parameter |
| **asᵢ** | 0.680 fm | Imaginary surface diffuseness |
| **Vso** | 0.000 MeV | Real spin-orbit potential depth |
| **rso₀** | 0.000 fm | Real spin-orbit radius parameter |
| **aso** | 0.000 fm | Real spin-orbit diffuseness |
| **Wsoᵢ** | 0.000 MeV | Imaginary spin-orbit potential depth |
| **rsoᵢ₀** | 0.000 fm | Imaginary spin-orbit radius parameter |
| **asoᵢ** | 0.000 fm | Imaginary spin-orbit diffuseness |
| **rc₀** | 1.150 fm | Coulomb radius parameter |

### OUTGOING (Proton) Optical Potential
**Reference**: Perey (1963)  
**DOI**: http://dx/doi.org/10.1016/0092-640X(76)90007-3  
**Validity**: E < 20 MeV, 30 < A < 100

| Parameter | Value | Description |
|-----------|-------|-------------|
| **V** | 48.926 MeV | Real central potential depth |
| **r₀** | 1.250 fm | Real central radius parameter |
| **a** | 0.650 fm | Real central diffuseness |
| **Wᵢ** | 0.000 MeV | Imaginary volume potential depth |
| **rᵢ₀** | 0.000 fm | Imaginary volume radius parameter |
| **aᵢ** | 0.000 fm | Imaginary volume diffuseness |
| **Wsᵢ** | 13.500 MeV | Imaginary surface potential depth |
| **rsᵢ₀** | 1.250 fm | Imaginary surface radius parameter |
| **asᵢ** | 0.470 fm | Imaginary surface diffuseness |
| **Vso** | 7.500 MeV | Real spin-orbit potential depth |
| **rso₀** | 1.250 fm | Real spin-orbit radius parameter |
| **aso** | 0.470 fm | Real spin-orbit diffuseness |
| **Wsoᵢ** | 0.000 MeV | Imaginary spin-orbit potential depth |
| **rsoᵢ₀** | 0.000 fm | Imaginary spin-orbit radius parameter |
| **asoᵢ** | 0.000 fm | Imaginary spin-orbit diffuseness |
| **rc₀** | 1.250 fm | Coulomb radius parameter |

---

## Key Differences Between AK and QP Sets

### Deuteron Optical Potential Differences

| Parameter | AK (An & Cai 2006) | QP (Perey & Perey 1963) | Δ |
|-----------|-------------------|------------------------|-----|
| **V** | 91.007 MeV | 87.171 MeV | -3.836 MeV |
| **a** | 0.761 fm | 0.810 fm | +0.049 fm |
| **Wᵢ** | 2.099 MeV | 0.000 MeV | -2.099 MeV |
| **Wsᵢ** | 10.340 MeV | 18.240 MeV | +7.900 MeV |
| **Vso** | 3.557 MeV | 0.000 MeV | -3.557 MeV |
| **rc₀** | 1.303 fm | 1.150 fm | -0.153 fm |

**Key Observation**: The QP set has **no volume absorption** (Wᵢ=0) and **no spin-orbit term** (Vso=0), relying entirely on surface absorption (Wsᵢ). The AK set includes both volume and surface absorption plus a significant spin-orbit term.

### Proton Optical Potential Differences

| Parameter | AK (Koning & Delaroche 2009) | QP (Perey 1963) | Δ |
|-----------|------------------------------|----------------|-----|
| **V** | 52.968 MeV | 48.926 MeV | -4.042 MeV |
| **r₀** | 1.182 fm | 1.250 fm | +0.068 fm |
| **a** | 0.672 fm | 0.650 fm | -0.022 fm |
| **Wᵢ** | 1.553 MeV | 0.000 MeV | -1.553 MeV |
| **Wsᵢ** | 8.619 MeV | 13.500 MeV | +4.881 MeV |
| **Vso** | 5.438 MeV | 7.500 MeV | +2.062 MeV |
| **Wsoᵢ** | -0.080 MeV | 0.000 MeV | +0.080 MeV |
| **rc₀** | 1.292 fm | 1.250 fm | -0.042 fm |

**Key Observation**: Similar to the deuteron case, the QP set has **no volume absorption** (Wᵢ=0), relying entirely on surface absorption. The AK set includes both volume and surface absorption, plus a small imaginary spin-orbit term.

---

## Physical Form of Potentials

All optical potentials follow the Woods-Saxon form:

### Central Potential
$$V(r) = -V \cdot f(r, R, a)$$
$$W_i(r) = -W_i \cdot f(r, R_i, a_i)$$

where $f(r, R, a) = \frac{1}{1 + \exp[(r-R)/a]}$ and $R = r_0 A^{1/3}$

### Surface (Derivative) Potential
$$W_s(r) = -4a_{si} W_{si} \frac{d}{dr} f(r, R_{si}, a_{si})$$

### Spin-Orbit Potential
$$V_{so}(r) = V_{so} \left(\frac{\hbar}{m_\pi c}\right)^2 \frac{1}{r} \frac{d}{dr} f(r, R_{so}, a_{so}) \mathbf{L} \cdot \mathbf{s}$$

### Coulomb Potential
Point charge distribution for r < Rc and 1/r for r > Rc, where $R_c = r_{c0} A^{1/3}$

---

## References

1. **An, H., and Cai, C.** (2006). "Global deuteron optical model potential for the energy range up to 183 MeV." *Physical Review C* 73, 054605.  
   DOI: [10.1103/PhysRevC.73.054605](http://dx.doi.org/10.1103/PhysRevC.73.054605)

2. **Koning, A. J., and Delaroche, J. P.** (2003). "Local and global nucleon optical models from 1 keV to 200 MeV." *Nuclear Physics A* 713, 231-310.  
   DOI: [10.1016/S0375-9474(02)01321-0](http://dx.doi.org/10.1016/S0375-9474(02)01321-0)

3. **Perey, F., and Perey, C.** (1963) as cited in Daehnick, W. W., Childs, J. D., and Vrcelj, Z. (1980). "Global optical model potential for elastic deuteron scattering from 12 to 90 MeV." *Physical Review C* 21, 2253.  
   DOI: [10.1016/0370-1573(91)90039-O](http://dx.doi.org/10.1016/0370-1573(91)90039-O)

4. **Perey, F. G.** (1963). "Optical-model analysis of proton elastic scattering in the range of 9 to 22 MeV." *Physical Review* 131, 745.  
   DOI: [10.1016/0092-640X(76)90007-3](http://dx/doi.org/10.1016/0092-640X(76)90007-3)

---

## Summary

This PTOLEMY input file performs **two independent DWBA calculations** for the ³⁶S(d,p)³⁷S reaction leading to the 7/2⁻ ground state:

1. **AK Set**: Uses modern, comprehensive global optical models (An & Cai 2006 for deuteron, Koning & Delaroche 2003 for proton) with both volume and surface absorption terms.

2. **QP Set**: Uses classic Perey parametrizations (1963) with surface-only absorption (no volume imaginary terms).

The comparison between these two sets allows for evaluation of systematic uncertainties arising from different optical model parameter choices, which is critical for extracting reliable spectroscopic factors from (d,p) reactions.
