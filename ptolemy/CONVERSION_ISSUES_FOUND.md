# PTOLEMY to DWUCK4 Conversion Issues Found

## Critical Discrepancies Discovered

Comparing the existing `DW_36S_DP_PTOLEMY_GS.in` file with my newly created files revealed **several important conversion factors** that I missed:

---

## Issue 1: Imaginary Surface Potential - MULTIPLIED BY 4a! ❌

### What I Did (WRONG):
| Parameter | PTOLEMY | My DWUCK4 |
|-----------|---------|-----------|
| **Deuteron Wsᵢ** | 10.340 MeV | +10.340 |
| **Proton Wsᵢ** | 8.619 MeV | +08.619 |

### What Should Be (CORRECT):
| Parameter | PTOLEMY | Existing File | Formula |
|-----------|---------|---------------|---------|
| **Deuteron Wsᵢ** | 10.340 MeV | **+95.641** | 10.340 × 4 × 2.313 = 95.641 |
| **Proton Wsᵢ** | 8.619 MeV | **+58.020** | 8.619 × 4 × 1.683 = 58.020 |

> [!CAUTION]
> DWUCK4 uses the **derivative Woods-Saxon form WITHOUT the 4a factor**, so you must **pre-multiply** by 4a when converting from PTOLEMY (which includes 4a in the derivative).

The factor is: **Wsᵢ(DWUCK4) = Wsᵢ(PTOLEMY) × 4 × asᵢ**

---

## Issue 2: Spin-Orbit Potential - MULTIPLIED BY 4! ❌

### What I Did (WRONG):
| Parameter | PTOLEMY | My DWUCK4 |
|-----------|---------|-----------|
| **Deuteron Vso** | 3.557 MeV | -03.557 |
| **Proton Vso** | 5.438 MeV | -05.438 |

### What Should Be (CORRECT):
| Parameter | PTOLEMY | Existing File | Formula |
|-----------|---------|---------------|---------|
| **Deuteron Vso** | 3.557 MeV | **-14.228** | 3.557 × 4 = 14.228 |
| **Proton Vso** | 5.438 MeV | **-21.752** | 5.438 × 4 = 21.752 |

> [!CAUTION]
> DWUCK4 spin-orbit requires a **factor of 4** multiplier when converting from PTOLEMY.

The factor is: **Vso(DWUCK4) = Vso(PTOLEMY) × 4**

---

## Issue 3: Imaginary Spin-Orbit - Same Factor of 4

### What I Did:
| Parameter | PTOLEMY | My DWUCK4 |
|-----------|---------|-----------|
| **Proton Wsoᵢ** | -0.080 MeV | +00.080 |

### What Should Be:
| Parameter | PTOLEMY | Existing File | Formula |
|-----------|---------|---------------|---------|
| **Proton Wsoᵢ** | -0.080 MeV | **+00.320** | 0.080 × 4 = 0.320 |

---

## Issue 4: Bound State Potential Depth ❌

### What I Did (Placeholder):
Card 14, column 5: `+06.000`

### What Should Be:
Card 14, column 5: **`36.439`** (no sign)

This appears to be the **bound state well depth** calculated from the binding energy. The existing file uses 36.439 MeV.

---

## Summary of Conversion Factors

| PTOLEMY Parameter | DWUCK4 Conversion | Multiplier |
|-------------------|-------------------|------------|
| **V** (central) | Direct | 1× |
| **Wᵢ** (volume imag) | Direct | 1× |
| **Wsᵢ** (surface imag) | **Multiply by 4asᵢ** | **4asᵢ** |
| **Vso** (real spin-orbit) | **Multiply by 4** | **4×** |
| **Wsoᵢ** (imag spin-orbit) | **Multiply by 4** | **4×** |
| **Radius parameters** | Direct | 1× |
| **Diffuseness** | Direct | 1× |

---

## Physics Explanation

These factors arise from different **normalizations of the derivative Woods-Saxon form**:

### Surface Imaginary Potential
PTOLEMY convention:
$$W_s(r) = -W_{si} \frac{d}{dr} f(r, R_{si}, a_{si})$$

DWUCK4 convention (includes 4a explicitly):
$$W_s(r) = -4a_{si} W_{si}' \frac{d}{dr} f(r, R_{si}, a_{si})$$

Therefore: **Wsᵢ(DWUCK4) = Wsᵢ(PTOLEMY) × 4 × asᵢ**

### Spin-Orbit Potential
The factor of 4 in spin-orbit is related to the Thomas factor and different normalizations of the $\mathbf{L} \cdot \mathbf{s}$ term.

---

## Impact on My Files

My files significantly **underestimated**:
1. Surface absorption (by factor of ~9-10)
2. Spin-orbit coupling (by factor of 4)

This explains why my calculations might show different angular distributions or magnitudes than expected!

---

## Action Required

I need to **regenerate both input files** with the correct conversion factors.
