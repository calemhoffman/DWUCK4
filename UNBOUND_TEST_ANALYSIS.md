# Unbound State Test Case Analysis

## Working Example: O16(d,p)O17 (from DW4TST.DAT)

### Input Cards

**Card 1:** Control code + title
```
1011000030000000    O16(D,P)O17  D3/2+   UNBOUND STRIPPPING  RMAX= 15 FM
```

**Card 4:** Integration parameters (note NEGATIVE RMAX!)
```
+00.10  +00.    -15.
```
Key: **RMAX = -15.0** (negative!)

**Card 13:** Binding energy
```
+00.933 +01.    +00.    +16.    +08.    +01.25                  +01.
```
E_bind = +0.933 MeV (positive, above threshold)

**Card 15:** Bound state parameters
```
+00.    +02.    +03.    +01.    +51.30  +00.    +00.00
```
FISW = 51.30 (non-zero for unbound)

### Key Insight: NEGATIVE RMAX!

The example uses **RMAX = -15.0** (negative value) on Card 4!

From ADWCK4.FOR lines 65-68:
```fortran
IF(ABS(RMAX).LT.ABS(RZ)) THEN
  temp=RZ
  RZ=RMAX
  RMAX=temp
```

**Negative RMAX has special meaning in DWUCK4!**

Looking at line 118:
```fortran
IF(RMAX.LT.0.0) K=KC
```

When RMAX < 0, the code uses a different calculation mode!

## Our Implementation Issue

**Our Card 4 for unbound:**
```
+00.30  +000.0   +15.0          0.7
```
RMAX = +15.0 (positive)

**Should be:**
```
+00.30  +000.0   -15.0          0.7
```
RMAX = -15.0 (negative!)

## Fix Required

For unbound states, set RMAX to **negative** value:
```python
rmax = -15.0 if not is_bound else 50.0
```

The negative RMAX tells DWUCK4 to use special unbound state integration.

## Verification

Running the example:
- Control code: `1011000030000000` ✓
- RMAX: `-15.0` ✓
- E_bind: `+0.933` ✓
- FISW: `51.30` (non-zero) ✓

Result: Physical cross-section (should be ~mb range)
