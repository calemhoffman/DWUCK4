# Additional DWUCK4 Normalization Factors

## Question: Is there a factor of 1.4 needed?

**Answer:** It depends on the context and what you're comparing to. There are several potential sources of additional factors:

---

## 1. Finite-Range vs Zero-Range Normalization

### Code Evidence

From `BDWCK4.FOR` lines 155-162:
```fortran
FACT=     2.0*FMU(1)/(HBARC*FK(1))**2
     1    *2.0*FMU(2)/(HBARC*FK(2))**2
     2    *AMU**2/FOURPI

if(abs(fm(1)-fm(2)).GT.0.1) then
C   Stripping normalization factors
    flfact=100.0*SQRT(FLOAT(2*LTR+1)/FLOAT(JTR+1))
    fact=fact*float(jtr+1)
endif
```

DWUCK4 uses **finite-range DWBA**, which includes:
- Different kinematic factors than zero-range approximations
- Specific normalization conventions for stripping amplitudes

### Possible Factor Sources

Different DWBA codes and conventions can differ by factors including:
- **√(2j+1)** or **(2j+1)** factors
- Isospin factors **(√2 for proton vs neutron)**
- Finite-range corrections

---

## 2. Historical DWUCK Conventions

### Known Normalization Issues

From DWUCK4 literature and user experiences:

1. **DWUCK vs FRESCO**: Different codes have different internal normalizations
   - FRESCO outputs in mb/sr directly
   - DWUCK outputs in fm² with specific conventions

2. **Spectroscopic Factor Conventions**:
   - Some references define C²S differently
   - Single-particle vs reduced width amplitude conventions

3. **Form Factor Normalizations**:
   - Finite-range form factors vs local approximations
   - Different integration schemes

---

## 3. Specific Factor of ~1.4

A factor of **1.4** specifically could arise from:

### 3a. Isospin Factor (√2 ≈ 1.414)

For neutron transfer reactions:
- If comparing single-particle units to spectroscopic factors
- Isospin Clebsch-Gordan coefficient can introduce √2

**Example**: For (d,p) adding a neutron:
```
Factor = √(2) = 1.414
```

This is the **most likely source** of a 1.4 factor!

### 3b. Different Spectroscopic Factor Definitions

Some literature uses:
- **Reduced width amplitude**: θ² 
- **Spectroscopic factor**: C²S
- **Relationship**: C²S = (2j+1) × θ² for some conventions

For j=7/2:
```
2j+1 = 8, but this gives factor of 8, not 1.4
```

### 3c. Center-of-Mass to Lab Frame

For light targets, kinematic corrections can introduce factors of order unity, but typically not exactly 1.4.

---

## 4. How to Determine if You Need the Factor

### Method 1: Compare with Known Reactions

1. Find a similar reaction with known spectroscopic factors
2. Run DWUCK4 for that reaction
3. Compare DWUCK4 output × 10 to published values
4. The ratio tells you if additional factors are needed

### Method 2: Check Your Specific Case

For **³⁶S(d,p)³⁷S**:

1. Check if you have experimental data
2. Convert DWUCK4: `σ(mb/sr) = σ(fm²) × 10`
3. Fit to data and see if you need additional normalization
4. A consistent factor of ~1.4 would suggest:
   - **√2 isospin factor**
   - Or a specific code convention difference

### Method 3: Literature Review

Search for:
- Papers using DWUCK4 for (d,p) reactions
- How they extract spectroscopic factors
- What normalization factors they mention

---

## 5. DWUCK4 Output Already Includes

The DWUCK4 cross-sections already include:
- ✅ Kinematic factors (reduced mass, wave numbers)
- ✅ Angular momentum coupling coefficients
- ✅ Finite-range form factor normalization
- ✅ Spin factors (2j+1)
- ✅ DWBA distortion effects

What's typically **NOT** included:
- ❌ Spectroscopic factor (assumes C²S = 1.0)
- ❌ Isospin Clebsch-Gordan coefficients (may need √2)
- ❌ Code-specific normalization compared to other codes

---

## 6. Recommended Approach

### For Extracting Spectroscopic Factors

**If you have experimental data:**

```python
import numpy as np

# DWUCK4 output
sigma_dwuck_fm2 = ...  # fm²

# Convert to mb/sr
sigma_dwuck_mbsr = sigma_dwuck_fm2 * 10.0

# Experimental data
sigma_exp_mbsr = ...  # mb/sr

# Method 1: Direct ratio (simplest)
C2S_raw = sigma_exp / sigma_dwuck_mbsr

# Method 2: With potential isospin factor
C2S_isospin = sigma_exp / (sigma_dwuck_mbsr * np.sqrt(2))

# Method 3: Fit to determine normalization
from scipy.optimize import curve_fit

def model(theta, C2S):
    return C2S * sigma_dwuck_mbsr
    
popt, pcov = curve_fit(model, theta_exp, sigma_exp)
C2S_fitted = popt[0]
```

### Check Consistency

1. **Sum rule check**: For (d,p) populating multiple states in same shell:
   ```
   Σ C²S ≈ (2j+1) × occupation number
   ```

2. **Compare to shell model**: Expected occupancies from theory

3. **Systematic comparison**: If ALL states need factor of 1.4, it's likely systematic

---

## 7. Specific to (d,p) Reactions

### Neutron Transfer

For **(d,p)** specifically adding a neutron:

**Isospin Clebsch-Gordan coefficient**:
```
<Tz_final | Tz_neutron, Tz_target> = 1/√2 for neutron
```

This gives:
```
σ_physical = 2 × σ_isospin = (√2)² × σ_unit
```

But DWUCK4 may or may not include this depending on how you set up the calculation.

### Check Your Input

In your `DW_36S_DP.in`:
- Line with masses should specify if you want isospin factors
- Check DWUCK4 documentation on isospin handling

---

## Summary Table

| Factor | Value | Source | When Needed |
|--------|-------|--------|-------------|
| fm² → mb/sr | 10 | Unit conversion | **Always** |
| Isospin (neutron) | √2 ≈ 1.414 | CG coefficient | If not in DWUCK4 setup |
| Spectroscopic factor | Variable | Nuclear structure | Extract from data |
| Code normalization | Varies | DWUCK vs others | When comparing codes |

---

## My Recommendation for Your Case

For **³⁶S(d,p)³⁷S**:

1. **Start with**: `σ(mb/sr) = σ_DWUCK(fm²) × 10`

2. **If you have experimental data**:
   - Fit and check if systematic factor appears
   - If factor ≈ 1.4-1.5, likely **isospin factor = √2**

3. **Physical interpretation**:
   - The **√2 is real physics** for neutron transfer
   - Whether DWUCK4 includes it depends on input setup

4. **To verify**: Check if DWUCK4 output matches literature values for well-known (d,p) reactions

---

## Where to Find More Information

1. **DWUCK4 Manual** (`dw4_doc.pdf`): Check normalization section
2. **Kunz papers**: Original DWUCK papers explain conventions
3. **Recent (d,p) papers**: See what normalizations they use
4. **FRESCO comparison**: Run same calculation in FRESCO to compare

---

## Bottom Line

**Yes, you may need an additional factor of √2 ≈ 1.414** if:
- DWUCK4's isospin handling doesn't match your convention
- You're extracting spectroscopic factors for neutron transfer
- This is the **standard isospin Clebsch-Gordan coefficient**

The factor is **not arbitrary** - it has physical meaning related to isospin symmetry in nuclear reactions.
