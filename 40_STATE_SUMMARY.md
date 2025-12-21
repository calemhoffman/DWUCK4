# DWUCK4 40-State Calculation Summary

## Overview

Successfully implemented automated DWUCK4 calculations for 40 nuclear states in ³⁶S(d,p)³⁷S reaction at 8 MeV beam energy, with full energy-dependent optical model corrections.

## Results

### ✅ Working: 20 Bound States (0-4226 keV)

All bound states calculate successfully with **physical cross-sections**:

| State | Ex (keV) | Orbital | Q (MeV) | σ_tot (mb) | Status |
|-------|----------|---------|---------|------------|--------|
| 1  | 0    | 0f7/2 | +2.079 | 2.94  | ✓ |
| 2  | 645  | 1p3/2 | +1.434 | 9.09  | ✓ |
| 3  | 1398 | 0d3/2 | +0.681 | 2.53  | ✓ |
| ... | ...  | ...   | ...    | ...   | ✓ |
| 20 | 4226 | 0f5/2 | -2.147 | 4.32  | ✓ |

**Range:** 2.5 - 11.3 mb (physically reasonable)

### ⚠️ Issue: Unbound States (4368-6775 keV)

States 21-29 show **non-physical cross-sections** (10¹⁹ - 10³² mb):

| State | Ex (keV) | Orbital | Q (MeV) | σ_tot (mb) | Issue |
|-------|----------|---------|---------|------------|-------|
| 21 | 4368 | 0f5/2 | -2.289 | 3.7×10¹⁹ | ❌ Too large |
| 22 | 4411 | 0f5/2 | -2.332 | 1.4×10²¹ | ❌ Too large |
| ... | ...  | ...   | ...    | ...      | ❌ |
| 29 | 4893 | 1p3/2 | -2.814 | 7.7×10²⁹ | ❌ Too large |

States 30-40 fail with "BUFFER ERROR IN UNBIND"

## Implementation Details

### CSV-Based Workflow

**File:** `inputs/36S_states.csv`
- 40 states defined with quantum numbers and energies
- Automatic energy-dependent parameter calculation

### Energy-Dependent Optical Models

**Deuteron potential:**
- W_D(Q) = 42.340 - 1.69×(Q - 2.079) MeV

**Proton potential:**
- V_real(E) = -56.249 + 0.405×(E - 9.438) MeV
- W_surf(E) = 34.836 - 0.415×(E - 9.438) MeV
- Spin-orbit terms also energy-dependent

### Bound vs Unbound States

**Bound states (E_bind < 0):**
- Control code: `1001000000200000`
- RMAX: +50.0 fm
- Marker: "bound ZR"
- Status: ✅ **Working**

**Unbound states (E_bind > 0):**
- Control code: `1011000030000000`
- RMAX: -15.0 fm (negative triggers special mode)
- Marker: "unbound ZR"
- FISW: 50.0 (non-zero)
- Status: ❌ **Non-physical results**

### Q-value Calculation

Corrected formula implemented:
```
Q(Ex) = Q(0) - Ex/1000 = 2.079 - Ex/1000 MeV
```

Previously, states above 4 MeV used fixed Q = -1.921 MeV (incorrect).

## Unbound State Issue Analysis

Despite correct configuration matching DW4TST.DAT example:
- ✓ Control code `1011000030000000`
- ✓ Negative RMAX (-15.0)
**✓ FISW = 50.0**
- ✓ Positive E_bind values

**The issue persists.** Possible causes:

1. **Different reaction kinematics**: O¹⁶(d,p) vs ³⁶S(d,p)
2. **Energy regime**: Our states have much higher binding energies
3. **Optical model potentials**: May need different parameters for unbound
4. **Buffer size**: Even with RMAX=-15, larger angular momentum (L=4) causes issues

## Recommendations

### For Production Use

**Use the 20 bound states (0-4226 keV):**
- Fully validated and physically meaningful
- Cover ground state through near-threshold region
- Include all major spectroscopic strength

### For Unbound States

Consider alternative approaches:
1. **DWUCK5**: More advanced, better handling of unbound states
2. **FRESCO**: Modern reaction code with robust continuum treatment
3. **Reduced LMAX**: Decrease from 30 to 15 for unbound to reduce buffer needs
4. **Consult DWUCK4 authors**: The unbound formalism may have limitations

## Files Generated

### Input Files
- `inputs/36S_states.csv` - All 40 states with corrected Q-values
- `inputs/DW_36S_DP_40states.in` - Generated DWUCK4 input (601 lines)
- `inputs/DW_36S_DP_OMP_full.in` - 13-state test with OMP

### Output Files
- `outputs/36S_40states_output.txt` - Raw DWUCK4 output
- `outputs/36S_20states_plot.html` - Interactive plot (bound states)

### Documentation
- `OPTICAL_MODEL_ANALYSIS.md` - CH89 analysis, empirical parametrization
- `OMP_VALIDATION.md` - Validation results
- `UNBOUND_TEST_ANALYSIS.md` - Unbound state configuration analysis
- `UNBOUND_STATES_RESEARCH.md` - FISW parameter research

### Tools
- `tools/generate_input.py` - Automatic input generation with OMP
- Updated to handle bound/unbound states automatically

## Achievements

✅ **Full automation**: CSV → DWUCK4 input with one command  
✅ **Energy-dependent OMP**: Both deuteron and proton channels  
✅ **20 physical states**: Complete bound state calculation  
✅ **Validation**: Matches original file within 0.002 MeV  
✅ **Documentation**: Comprehensive analysis and guides  

## Remaining Work

❌ Resolve unbound state calculation issues  
❌ Generate plot for all 40 states (currently limited to 20)  
❌ Full comparison with experimental data  

## Conclusion

The implementation successfully automates DWUCK4 calculations for bound states with sophisticated energy-dependent optical models. The 20 bound states (0-4226 keV) provide physically meaningful results suitable for spectroscopic factor extraction.

Unbound states above the neutron separation threshold require further investigation or alternative computational approaches.
