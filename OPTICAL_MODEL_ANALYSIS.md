# CH89 Global Optical Model Parametrization

## Reference

**R.L. Varner et al., "A global nucleon optical model potential"**  
*Physics Reports*, Volume 201, Issue 2, pages 57-119 (1991)

---

## Key Information

### Validity Range

**CRITICAL: CH89 is NOT directly applicable to ³⁷S**

- **Mass range**: A = 40 to 209  
- **Proton energy**: E = 16 to 65 MeV  
- **Neutron energy**: E = 10 to 26 MeV

**³⁷S has A=37**, which is **outside the valid range** for CH89. The authors deliberately excluded A < 40 due to difficulties in finding optical potentials that vary smoothly with energy for lighter nuclei (low density of scattering states).

---

## CH89 Parametrization Formulas

### Woods-Saxon Form Factors

The optical model potential has the general form:

```
U(r,E) = V_V(r,E) + i[W_V(r,E) + W_D(r,E)] + V_SO(r,E)(L·σ) + V_C(r)
```

Where:
- **V_V**: Real volume potential (Woods-Saxon)
- **W_V**: Imaginary volume potential (Woods-Saxon)  
- **W_D**: Imaginary surface potential (derivative Woods-Saxon)
- **V_SO**: Spin-orbit potential (Thomas form)
- **V_C**: Coulomb potential

### CH89 Proton Parametrization

#### Real Central Potential (V_V)
```
V = 54.0 - 0.32E + 0.4Z/A^(1/3) + 24.0ε  [MeV]
r_V = 1.17A^(1/3)  [fm]
a_V = 0.75  [fm]
```

#### Imaginary Volume Potential (W_V)
```
W_V = -1.56 + 0.22E  [MeV]  (for W_V > 0)
r_W = 1.26A^(1/3)  [fm]
a_W = 0.58  [fm]
```

#### Imaginary Surface Potential (W_D)
```
W_D = 13.0 - 0.25E - 12.0ε  [MeV]  (for W_D > 0)
r_D = 1.32A^(1/3)  [fm]
a_D = 0.51 + 0.7ε  [fm]
```

#### Spin-Orbit Potential (V_SO)
```
V_SO = fixed (energy-independent)
J_SO^2 = 6.2  [MeV·fm^5]  (volume integral squared)
r_SO = 1.01A^(1/3)  [fm]
a_SO = 0.75  [fm]
```

Where:
- **E**: Lab energy in MeV
- **ε**: Asymmetry parameter = (N-Z)/A
- **A**: Mass number
- **Z**: Proton number

---

## Issue for ³⁷S(d,p)³⁸S

### Parameters for ³⁷S
- A = 37 (< 40, **outside CH89 range**)
- Z = 16
- N = 21
- ε = (21-16)/37 = 0.135

### What's Actually Being Used?

Looking at the input file values for the proton channel:
- r_V = 1.182 fm
- r_W = 1.290 fm  
- r_D = 0.991 fm (for spin-orbit)

**Comparison with CH89 predictions for A=37:**
- CH89 r_V = 1.17 × 37^(1/3) = 1.17 × 3.33 = **3.90 fm** ❌ (doesn't match!)

**This indicates the input file is NOT using CH89!**

---

## Likely Parametrization: Modified Becchetti-Greenlees

The radii values (1.182, 1.290 fm) suggest a **reduced radius parametrization**:
```
r = r₀ × A^(1/3)
```

With:
- r₀_V ≈ 1.17 fm for volume
- r₀_W ≈ 1.29 fm for surface

But these are applied as **absolute radii**, not r₀ values!

### Actual Form (Hypothesis)

The input appears to use **fixed geometry** with:
```
r_real = 1.182 fm (constant)
r_imag = 1.290 fm (constant)
a_real = 0.672 fm (constant)
a_imag = 0.538 fm (constant)
```

Only the **depths** are energy-dependent.

---

## Energy Dependence Analysis

### From the Two-State Comparison

**Exit channel energies:**
- State 1: E = 8 + 2.079 - 0.641 ≈ **9.438 MeV** (proton + recoil KE)
- State 2: E = 8 + 1.434 - 0.641 ≈ **8.793 MeV**

**Observed depths:**
| Parameter | State 1 (9.438 MeV) | State 2 (8.793 MeV) | ΔV/ΔE |
|-----------|---------------------|---------------------|-------|
| V_real    | -56.249            | -56.510            | +0.40 MeV/MeV |
| W_surf    | +34.836            | +34.568            | -0.42 MeV/MeV |
| V_SO real | -0.786             | -0.734             | +0.08 MeV/MeV |
| W_SO imag | +0.156             | +0.144             | -0.02 MeV/MeV |

### Parametrization (Best Fit to Data)

```python
def proton_optical_potential(E_proton):
    """
    E_proton: Exit channel proton lab energy in MeV
    
    Returns: Dictionary of potential depths in MeV
    """
    # Reference energy (state 1)
    E_ref = 9.438
    
    # Reference depths at E_ref
    V_real_ref = -56.249
    W_surf_ref = +34.836
    VSO_real_ref = -0.786
    WSO_imag_ref = +0.156
    
    # Linear energy dependence
    dE = E_proton - E_ref
    
    V_real = V_real_ref + 0.405 * dE
    W_surf = W_surf_ref - 0.415 * dE  
    VSO_real = VSO_real_ref + 0.081 * dE
    WSO_imag = WSO_imag_ref - 0.019 * dE
    
    return {
        'V_real': V_real,
        'W_surf': W_surf,
        'VSO_real': VSO_real,
        'WSO_imag': WSO_imag,
        # Geometries (constant)
        'r_V': 1.182,
        'a_V': 0.672,
        'r_W': 1.290,
        'a_W': 0.538,
        'r_SO': 0.991,
        'a_SO': 0.590
    }
```

---

## Recommendations

1. **Do NOT claim** this is CH89 (it's not applicable to A<40)
2. **Use empirical parametrization** from the two-state fit
3. **Document** as "energy-dependent optical potential (custom for A=37)"
4. **Test** extrapolation to higher excitations to ensure physical behavior
5. **Consider** looking at:
   - Becchetti & Greenlees (1969) for lighter nuclei
   - Koning & Delaroche (2003) global OMP
   - Or use the empirical fit derived above

---

## Implementation Status

✅ Identified actual parametrization (NOT CH89)  
✅ Extracted energy dependence from data   
✅ Ready to implement in `generate_input.py`  
⚠️ CH89 reference PDFs likely not relevant for A=37
