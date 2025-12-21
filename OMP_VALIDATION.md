# Optical Model Validation Results

## Comparison: Original vs Generated with OMP

### State 1 (0 keV, E_proton = 9.438 MeV)

**Original File:**
```
+01.    -56.249 +01.182 +00.672         -00.786 +01.182 +00.672 
+02.    +00.000 +00.000 +00.000         +34.836 +01.290 +00.538 
-04.    -22.456 +00.991 +00.590         +00.156 +00.991 +00.590 
```

**Generated File:**
```
+01.    -56.249 +01.182 +00.672         -00.786 +01.182 +00.672 
+02.    +00.000 +00.000 +00.000         +34.836 +01.290 +00.538 
-04.    -22.456 +00.991 +00.590         +00.156 +00.991 +00.590 
```

✅ **PERFECT MATCH** for reference state!

---

### State 2 (645 keV, E_proton = 8.793 MeV)

**Original File:**
```
+01.    -56.510 +01.182 +00.672         -00.734 +01.182 +00.672 
+02.    +00.000 +00.000 +00.000         +34.568 +01.290 +00.538 
-04.    -22.516 +00.991 +00.590         +00.144 +00.991 +00.590
```

**Generated File:**
```
+01.    -56.510 +01.182 +00.672         -00.838 +01.182 +00.672 
+02.    +00.000 +00.000 +00.000         +35.104 +01.290 +00.538 
-04.    -22.456 +00.991 +00.590         +00.168 +00.991 +00.590
```

**Differences:**
| Parameter | Original | Generated | Δ | Comments |
|-----------|----------|-----------|---|----------|
| V_real | -56.510 | -56.510 | 0.000 | ✅ Perfect |
| VSO_real | -0.734 | -0.838 | -0.104 | ❌ Off by ~14% |
| W_surf | 34.568 | 35.104 | +0.536 | ❌ Off by ~1.6% |
| WSO_imag | 0.144 | 0.168 | +0.024 | ❌ Off by ~17% |
| W_volume_SO | -22.516 | -22.456 | +0.060 | ❓ Different in original |

---

## Analysis

### Issue Identification

The discrepancies suggest:

1. **V_real is correct** - validates the primary energy dependence
2. **W_surf has systematic offset** - suggests the deuteron imaginary potential might vary
3. **Spin-orbit terms off** - smaller parameters, harder to extract slopes accurately
4. **Line 23 different in original** - the deuteron potential imaginary surface depth changes!

Looking at line 23:
- State 1: `+42.340`
- State 2: `+43.432` 

This is the **deuteron imaginary surface** potential - it DOES vary by energy!

### Root Cause

The original file has **both deuteron AND proton potentials** energy-dependent, but I only implemented proton!

---

## Next Steps

1. Extract deuteron optical model energy dependence
2. Update `calculate_proton_optical_model()` or create separate deuteron function
3. Recalculate slopes with correct attribution
4. Regenerate and retest

---

## Deuteron Potential Changes

Looking at Card 7 (line 22/23 in original file):

**State 1:** `+02.    +00.000 +00.000 +00.000         +42.340 +01.380 +00.736`  
**State 2:** `+02.    +00.000 +00.000 +00.000         +43.432 +01.380 +00.736`

**Deuteron imaginary surface depth:**
- State 1: W_D = +42.340 MeV
- State 2: W_D = +43.432 MeV
- Difference: +1.092 MeV for ΔE_deuteron = 0.645 MeV (Q-value difference)

**Deuteron energy dependence:**
```
dW_D_dE ≈ -1.092 / 0.645 ≈ -1.69 MeV/MeV
```

This is a **decreasing function** (gets less absorptive at higher energy).

Wait - the sign is backwards. Let me recalculate with proper deuteron kinematics...

The deuteron **loses** energy as the reaction Q-value decreases:
- State 1 (Q=2.079): E_d_exit ≈ 8 - 2.079/2 ≈ 6.96 MeV (in CM, rough)
- State 2 (Q=1.434): E_d_exit ≈ 8 - 1.434/2 ≈ 7.28 MeV

Actually, the deuteron energy **increases** for lower Q (less energy given to proton). So the trend makes sense: higher deuteron energy → more absorption.
