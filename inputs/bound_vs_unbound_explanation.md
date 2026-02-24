# DWUCK4 Bound vs. Unbound States Analysis
    
This document breaks down the differences between the input configurations for the ground state (Line 1) and the 5000 keV excited state (Line 76) within the file `inputs/36S_scan_7MeV.in` and explains what these differences mean for the underlying DWUCK4 calculation.

## What are the differences?

Here are the exact texts of the lines:
*   **Line 1:** `1001000000200000    36S(d,p)@ 16MeV    0 keV  0f7/2 bound ZR`
*   **Line 76:** `1011000030000000    36S(d,p)@ 16MeV    5000 keV  0f7/2 unbound ZR`

### 1. The Control Code (First 16 Characters)
DWUCK4 uses a strict 16-digit integer string at the beginning of the first card to configure the physics model of the interaction:
*   **Line 1 (Bound):** `10`**`0`**`10000`**`0`**`0200000`
*   **Line 76 (Unbound):** `10`**`1`**`10000`**`3`**`0000000`

Notice the differences in the **3rd digit** (`0` vs `1`) and the **9th digit** (`0` vs `3`).
*   The **3rd digit** controls the form factor calculation method. Changing it to `1` instructs DWUCK4 that the transferred particle is in an unbound (continuum/resonant) state rather than a standard bound Wood-Saxon well.
*   The **9th digit** (and others) are specific integration flags modifying how the DWBA radial integration matches to asymptotic wavefunctions for large radii.

### 2. Theoretical Description Text
After the 16-character code, the remaining characters act as the "title" for the calculation block in the output printout.
*   **Line 1** labels the state as a `0 keV` `bound` state. 
*   **Line 76** labels the state as a `5000 keV` `unbound` state.

---

## What does this mean for the calculation?

### The Physics: Bound vs. Unbound
*   **Bound State (Line 1):** The neutron from the deuteron is transferred into a discrete, bound orbital around the ³⁶S core, forming the ³⁷S ground state. The binding energy of this neutron is negative (i.e., it takes energy to remove it). DWUCK4 calculates the radial wavefunction by finding the Wood-Saxon well depth that precisely gives this binding energy. The wavefunction exponentially decays to zero at large radii.
*   **Unbound State (Line 76):** An excitation energy of 5000 keV (5 MeV) places the nucleus above the neutron separation energy (the reaction Q-value is $2.079 - 5.000 = -2.921$ MeV, meaning the final system is less bound than expected, placing the transferred neutron in the continuum). This is a resonant scattering state. The neutron is not trapped in an exponentially decaying well; instead, its wavefunction oscillates out to infinity as it can technically escape the nucleus. 

### Processing and Integration Differences
Because the unbound wavefunction oscillates forever, DWUCK4 cannot just stop integrating when the wavefunction "dies out". 
1.  **Form Factor Generation:** DWUCK4 uses slightly different numerical routines (triggered by the `1011...` control block) to describe the form factor of the transferred particle as an unbound single-particle resonance.
2.  **Radial Integration (RMAX):** Due to this, the integration flag (Card 4) behaves differently. For bound states, DWUCK4 usually integrates to a positive maximum radius (`RMAX = 50.0 fm`). However, for the unbound states triggered by this code, RMAX is assigned a **negative** value (like `-15.0 fm`), signaling DWUCK4 to employ a special matching condition to incoming/outgoing functions.
3.  **Boundary Conditions (FISW):** On Card 15, the variable `FISW` defaults to something like `50.0` to force an integration match radius explicitly for unbound resonances. 

These control flags collectively ensure the DWBA integral remains finite and mathematically sound even when mathematically matching plane waves to a continuum resonance state.
