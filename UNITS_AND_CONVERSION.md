# DWUCK4 Cross-Section Units and Conversion

## Output Units

DWUCK4 outputs differential cross-sections in **fm² (square femtometers)**, not mb/sr.

### Evidence from Output Files

From the 36S(d,p) output file header:
```
0 Theta Inelsig,fm**2      Polz       Asy       Ayy       A22  ...
```

The column is explicitly labeled as `fm**2` (square femtometers).

---

## Conversion to mb/sr

To convert from **fm²** to **mb/sr** (millibarns per steradian), use:

### Conversion Factor

```
1 fm² = 10 mb/sr
```

**Derivation:**
- 1 barn (b) = 10⁻²⁴ cm² = 100 fm²
- 1 millibarn (mb) = 10⁻³ barn = 0.1 fm²
- Therefore: **1 fm² = 10 mb**

Since DWUCK4 outputs are already per steradian (dσ/dΩ), the conversion is simply:

```
σ(mb/sr) = σ(fm²) × 10
```

---

## Example Conversion

From the 36S(d,p) ground state output:

| Theta (deg) | DWUCK4 Output (fm²) | Converted (mb/sr) |
|-------------|---------------------|-------------------|
| 16.00       | 5.6956              | 56.956            |
| 40.00       | 1.9877              | 19.877            |
| 70.00       | 0.7022              | 7.022             |

---

## Spectroscopic Factors

DWUCK4 calculates **unit spectroscopic factor** cross-sections (C²S = 1.0).

### To Get Experimental Cross-Sections

The DWUCK4 output represents the theoretical cross-section for **unit spectroscopic strength**. To compare with experiment or extract spectroscopic factors:

```
σ_experimental = C²S × σ_DWUCK4
```

Where:
- `C²S` = spectroscopic factor (dimensionless)
- `σ_DWUCK4` = DWUCK4 calculated cross-section per unit spectroscopic strength

### To Extract Spectroscopic Factors

If you have experimental data, extract the spectroscopic factor by:

```
C²S = σ_experimental / σ_DWUCK4
```

This is typically done by:
1. Converting both to the same units (mb/sr)
2. Fitting or calculating the ratio
3. The ratio gives the spectroscopic factor

---

## Total Integrated Cross-Sections

DWUCK4 also reports total reaction cross-sections:

From the output:
```
0Tot-sig   2.9397E+00    (for ground state)
0Tot-sig   9.1492E+00    (for excited state)
```

These are in **mb** (millibarns), representing the angle-integrated cross-section.

---

## Summary

| Quantity | DWUCK4 Units | Conversion to Standard Units |
|----------|--------------|------------------------------|
| Differential cross-section (dσ/dΩ) | fm² | Multiply by 10 to get mb/sr |
| Total cross-section (σ_tot) | mb | Already in millibarns |
| Spectroscopic factor | Implicit C²S = 1.0 | Divide experimental by DWUCK4 to extract |

---

## Practical Workflow

### For Comparison with Experimental Data

1. **Run DWUCK4** with your reaction parameters
2. **Extract dσ/dΩ** values from output (in fm²)
3. **Convert to mb/sr**: Multiply all values by 10
4. **Extract spectroscopic factor**:
   - Fit DWUCK4 calculation to experimental data
   - The normalization factor from the fit is C²S
   - Or calculate point-by-point ratios and average

### For Multiple States

When analyzing multiple states (like the two 36S states):
- Each state has its own angular distribution
- Each can have a different spectroscopic factor
- DWUCK4 output assumes C²S = 1.0 for each
- Sum rule: Σ(C²S) should equal the number of available nucleons

---

## Example Python Conversion

```python
import numpy as np

# DWUCK4 output data (theta, cross_section in fm²)
theta_dwuck = np.array([0, 10, 20, 30, 40])  # degrees  
sigma_dwuck = np.array([3.01, 4.52, 5.38, 4.89, 1.99])  # fm²

# Convert to mb/sr
sigma_mbsr = sigma_dwuck * 10.0

# If you have experimental data
sigma_exp = np.array([30, 50, 60, 45, 18])  # mb/sr

# Extract spectroscopic factor (simple average ratio)
spectroscopic_factor = np.mean(sigma_exp / sigma_mbsr)
print(f"Spectroscopic factor C²S = {spectroscopic_factor:.3f}")
```

---

## Notes

- DWUCK4's finite-range DWBA calculations include:
  - Optical model distortions
  - Finite-range form factors
  - Spin-orbit coupling
  - Non-local corrections (if enabled)

- The spectroscopic factor C²S accounts for:
  - Nuclear structure overlap
  - Configuration mixing
  - Deviations from single-particle picture

- For bound states: DWUCK4 calculates the bound-state wavefunction
- For unbound states: Uses appropriate energy and boundary conditions

---

## Recommended Tools

For fitting DWUCK4 to experimental data, use the `plot_dwuck.py` tool with reference data:

```bash
python3.11 tools/plot_dwuck.py \
  --input outputs/36S_dp_output.txt \
  --ref experimental_data.csv \
  --fit \
  --out outputs/fitted_plot.html
```

The `--fit` option performs linear least-squares fitting, where the slope parameter gives an estimate of the spectroscopic factor (when experimental data is in mb/sr and DWUCK4 is converted to mb/sr).
