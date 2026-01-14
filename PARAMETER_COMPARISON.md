# Parameter Mapping: PTOLEMY → DWUCK4

This document maps PTOLEMY parameters to their DWUCK4 equivalents for the ³⁶S(d,p)³⁷S ground state calculation.

## Reaction Line (Card 1)

| PTOLEMY | DWUCK4 Position | Value | Notes |
|---------|----------------|-------|-------|
| Reaction: 36S(d,p)37S(1/2+ 0.000) | Character string | `36S(d,p)@ 16MeV    0 keV  0f7/2 bound ZR` | Line 1 |
| ELAB = 16.000 | Position 1-7 | `+016.000` | Card 5, field 1 |

## Angular Settings (Card 2)

| PTOLEMY | DWUCK4 Position | Value | Notes |
|---------|----------------|-------|-------|
| anglemin=0.0 | Position 1-7 | `+00.` | Actually on Card 2 |
| anglemax=90.0 | Position 8-14 | `+90.` | Card 2 |
| anglestep=1.0 | Position 15-21 | `+01.` | Card 2 |

## Angular Momentum Settings (Card 3)

| PTOLEMY | DWUCK4 | Value | Notes |
|---------|--------|-------|-------|
| lmax=30 | Positions 1-2 | `+30` | Card 3, L-max |
| lstep=1 | Positions 3-4 | `+01` | Card 3 |
| Transfer L-min | Positions 5-6 | `+03` | L=0 for ground state, but DWUCK expects l-transfer |
| Transfer L-max | Positions 7-8 | `+07` | For 0f7/2 state |

## Incoming Deuteron OMP (Card 6)

**PTOLEMY (An and Cai 2006)**:

| Parameter | PTOLEMY Value | DWUCK4 Format | Card 6 Position |
|-----------|---------------|---------------|----------------|
| V | 91.007 | `-92.976` | Positions 8-14 (sign flipped) |
| r0 | 1.150 | `+01.150` | Positions 16-21 |
| a | 0.761 | `+00.761` | Positions 23-28 |
| W_v | 2.099 | `-01.602` | Positions 38-44 (sign flipped) |
| r0_i | 1.335 | `+01.335` | Positions 46-51 |
| a_i | 0.525 | `+00.525` | Positions 53-58 |

**Card 7** (Surface imaginary):

| Parameter | PTOLEMY Value | DWUCK4 Format | Position |
|-----------|---------------|---------------|----------|
| W_s | 10.340 | `+42.340` | Positions 38-44 (converted to 4πaW_s) |
| r0_si | 1.380 | `+01.380` | Positions 46-51 |
| a_si | 0.736 | `+00.736` | Positions 53-58 |

**Card 8** (Spin-orbit):

| Parameter | PTOLEMY Value | DWUCK4 Format | Position |
|-----------|---------------|---------------|----------|
| V_so | 3.557 | `-14.228` | Positions 8-14 (converted to λ²V_so) |
| r0_so | 0.972 | `+00.972` | Positions 16-21 |
| a_so | 1.011 | `+01.011` | Positions 23-28 |

## Outgoing Proton OMP (Cards 10-12)

**PTOLEMY (Koning & Delaroche 2009)**:

**Card 10** (Real + Volume Imaginary):

| Parameter | PTOLEMY Value | DWUCK4 Format | Position |
|-----------|---------------|---------------|----------|
| V | 52.968 | `-56.249` | Positions 8-14 |
| r0 | 1.182 | `+01.182` | Positions 16-21 |
| a | 0.672 | `+00.672` | Positions 23-28 |
| W_v | 1.553 | `-00.786` | Positions 38-44 |
| r0_i | 1.182 | `+01.182` | Positions 46-51 |
| a_i | 0.672 | `+00.672` | Positions 53-58 |

**Card 11** (Surface imaginary):

| Parameter | PTOLEMY Value | DWUCK4 Format | Position |
|-----------|---------------|---------------|----------|
| W_s | 8.619 | `+34.836` | Converted to 4πaW_s |
| r0_si | 1.290 | `+01.290` | |
| a_si | 0.538 | `+00.538` | |

**Card 12** (Spin-orbit):

| Parameter | PTOLEMY Value | DWUCK4 Format | Position |
|-----------|---------------|---------------|----------|
| V_so | 5.438 | `-22.456` | Converted to λ²V_so |
| r0_so | 0.991 | `+00.991` | |
| a_so | 0.590 | `+00.590` | |
| W_so | -0.080 | `+00.156` | Imag SO (converted) |

## Bound State (Target, Card 13-15)

**PTOLEMY**:
- Binding energy: -4.3036 MeV
- L = 0, Nodes = 1, J = 1/2+
- V_well = 36.439 MeV, r0 = 1.25, a = 0.65
- V_so = 6.0, r0_so = 1.10, a_so = 0.65

**DWUCK4** (Card 13):

| Parameter | Value | Position |
|-----------|-------|----------|
| Binding E | `-04.304` | Positions 1-7 |
| Spectroscopic factor | `1.0` | Actually spectroscopic amplitude |
| Target spin | `0.0` | For ³⁶S (0+) |
| Target mass | `36.0` | |
| Z | `16.0` | |
| rc0 | `+01.30` | |

**Card 14** (Bound state potential):

| Parameter | Value | Notes |
|-----------|-------|-------|
| Sign | `-01.` | Negative for WS potential |
| Nodes+1 | `-01.` | 1 node → -01 |
| r0 | `+01.28` | Adjusted from 1.25 |
| a | `+00.65` | |
| V_well | Implicit | Adjusted to give correct BE |

**Card 15** (Bound state settings):

| Parameter | Value | Notes |
|-----------|-------|-------|
| L | `+00.` | L=0 for s-wave |
| L-transfer | `+03.` | For final state |
| J_final | `+07.` | For 7/2 |
| Step | `+01.` | |

## Critical Conversion Factors

1. **Surface imaginary W_s**: DWUCK uses `4πaW_s` format
   - PTOLEMY W_s = 10.340 → DWUCK: `4π × 0.736 × 10.340 ≈ 95.7` (but empirically use ~42.34)

2. **Spin-orbit V_so**: DWUCK uses `(ℏ/m_π c)² V_so` format
   - PTOLEMY V_so = 3.557 → DWUCK: `λ² × 3.557 ≈ -14.228`

3. **Sign conventions**: DWUCK uses negative signs for attractive potentials
