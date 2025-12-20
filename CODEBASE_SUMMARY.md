# DWUCK4 Codebase Summary

**Generated:** 2025-12-19

## Overview

DWUCK4 is a **nuclear physics simulation code** for calculating **distorted wave Born approximation (DWBA)** cross-sections for nuclear reactions. This is Fortran-based legacy scientific computing code originally developed by Peter Kunz, now archived on GitHub due to the original website being offline.

---

## Directory Structure

```
DWUCK4/
├── *.FOR, *.F          # Fortran source files
├── culib4/             # Single precision libraries (12 modules)
├── culib8/             # Double precision libraries (13 modules)
├── inputs/             # Example input files
├── outputs/            # Generated output files
├── tools/              # Python utilities
├── misc/               # Reference documents (optical model parameters)
├── dw4_doc.pdf         # Official documentation
├── CompileAndTest.sh   # Build and test script
└── README.md           # Repository information
```

---

## Core Components

### 1. Main Fortran Source Files

| File | Size | Description |
|------|------|-------------|
| `DWUCK4.FOR` | 2.6 KB | Main entry point/driver program |
| `ADWCK4.FOR` | 30.2 KB | Main calculation routines (largest module) |
| `BDWCK4.FOR` | 16.2 KB | Supporting calculation routines |
| `CDWCK4.FOR` | 22.6 KB | Additional calculation routines |

**Platform-specific I/O modules** (4 variants for different systems):
- `DW4IBM.F` - IBM mainframe version
- `DW4PC.F` - PC/DOS version
- `DW4UNIX.F` - Unix systems (used in current build)
- `DW4VAX.F` - VAX/VMS systems

### 2. Numerical Libraries

#### `culib4/` - Single Precision (REAL*4)
12 modules providing core numerical capabilities:

| Module | Function |
|--------|----------|
| `ANGMOM.FOR` | Angular momentum calculations |
| `COU.FOR` | Coulomb function calculations |
| `GAUSSR.FOR` | Gaussian integration routines |
| `LEGAUS.FOR` | Legendre-Gaussian quadrature |
| `LGNDR.FOR` | Legendre polynomial evaluation |
| `POTS.FOR` | Optical potential calculations |
| `SLATER.FOR` | Slater integral calculations |
| `BIND.FOR` | Binding energy calculations |
| `DSTRIP.FOR` | Stripping reaction utilities |
| `DWPLOT.FOR` | Plotting utilities |
| `FNLOC5.FOR` | Function location/finding |
| `POLFCT.FOR` | Polarization factor calculations |

#### `culib8/` - Double Precision (REAL*8)
13 modules (includes all culib4 modules plus):
- `ELSIG.FOR` - Elastic scattering cross-section calculations

### 3. Python Tools (`tools/` directory)

#### `make_dat.py` (185 lines)
**Purpose:** Interactive tool to create DWUCK4 input files in `.DAT` format

**Features:**
- Three operating modes:
  - `--sample`: Generate example case (Fe56 inelastic scattering)
  - `--interactive`: Guided prompts for user input
  - `--json`: Batch creation from JSON configuration
- Formats nuclear reaction parameters into Fortran fixed-format input
- Handles:
  - 16-digit control codes
  - Angular distributions (theta points)
  - Quantum numbers (L-values)
  - Radial integration parameters (DRF, RMAX)
  - Optical potential parameters
  - Multiple cases in single file

**Usage:**
```bash
python tools/make_dat.py --out inputs/custom.DAT --sample
python tools/make_dat.py --out inputs/custom.DAT --interactive
python tools/make_dat.py --out inputs/custom.DAT --json mycases.json
```

#### `plot_dwuck.py` (172 lines)
**Purpose:** Parse DWUCK4 output and create interactive visualizations

**Features:**
- Automatically extracts theta (scattering angle) vs. cross-section data from text output
- Creates interactive **Plotly** HTML plots
- Overlays experimental reference data from CSV files
- Linear fit capability for model-to-data comparison
- Fit model: `observed = a × model + b` (least-squares)

**Usage:**
```bash
python tools/plot_dwuck.py --input outputs/run_output.txt --out outputs/dwuck_plot.html
python tools/plot_dwuck.py --input outputs/run_output.txt --out outputs/dwuck_plot.html --ref reference.csv --fit
```

### 4. Input Files (`inputs/` directory)

| File | Description |
|------|-------------|
| `DW_36S_DP.in` | ³⁶S(d,p)³⁷S reaction at 8 MeV (two states: 0 keV 0f₇/₂ and 645 keV 1p₃/₂) |
| `case1.dat` | Example test case |
| `case_from_test.dat` | Derived from standard test |
| `my_case.dat` | Custom user case |
| `sample_case.dat` | Sample calculation |

**Input file format:** Fortran fixed-format cards with:
- Control code (16 digits) + reaction description
- Angular distribution parameters (n, start, step)
- Quantum numbers (L-values)
- Integration parameters (DRF, RMAX)
- Optical potential parameters (depths, radii, diffuseness)
- Projectile/target masses and charges

### 5. Test and Documentation Files

| File | Size | Purpose |
|------|------|---------|
| `dw4_doc.pdf` | 208 KB | Official DWUCK4 documentation |
| `DW4TST.DAT` | 9.8 KB | Standard test input (Fe56 inelastic scattering) |
| `DW4TST.LIS` | 209 KB | Expected output for validation |
| `CompileAndTest.sh` | 364 bytes | Build and test script |

### 6. Reference Documents (`misc/` directory)

- `ES-globals_beta_v5.pdf` - Excited state global optical model parameters
- `GS-globals_beta_v5.pdf` - Ground state global optical model parameters

These PDFs contain empirical parametrizations of optical potentials for various nuclei.

---

## Build System

### `CompileAndTest.sh`
Automated compilation and testing script:

```bash
#!/bin/bash
# Compile main modules with legacy Fortran support
gfortran --std=legacy -c *.FOR
gfortran -c DW4UNIX.F

# Compile single precision library
cd culib4
gfortran --std=legacy -c *.FOR

# Compile double precision library
cd ../culib8
gfortran --std=legacy -c *.FOR

# Link all object files
cd ..
gfortran *.o culib8/*.o -o DWUCK4.exe

# Run standard test
./DWUCK4.exe < DW4TST.DAT
```

**Key notes:**
- Uses `gfortran` with `--std=legacy` flag (required for old Fortran syntax)
- Links with `culib8` (double precision) for final executable
- Standard test compares output with `DW4TST.LIS`

---

## Workflow

### Typical Usage Pattern

1. **Compilation**
   ```bash
   ./CompileAndTest.sh
   ```
   Produces `DWUCK4.exe` executable

2. **Input Preparation**
   ```bash
   python tools/make_dat.py --out inputs/my_reaction.DAT --interactive
   ```
   Creates properly formatted input file

3. **Execution**
   ```bash
   ./DWUCK4.exe < inputs/my_reaction.DAT > outputs/my_output.txt
   ```
   Runs simulation, saves output

4. **Visualization**
   ```bash
   python tools/plot_dwuck.py --input outputs/my_output.txt --out outputs/plot.html
   ```
   Generates interactive plot

5. **Data Comparison** (optional)
   ```bash
   python tools/plot_dwuck.py --input outputs/my_output.txt \
     --ref experimental_data.csv --fit --out outputs/fitted_plot.html
   ```
   Compares model to experimental data with linear fit

---

## Physics Application

### Nuclear Transfer Reactions

Based on the input files, this code is used for:
- **Direct nuclear reactions**: (d,p), (p,p'), etc.
- **Differential cross-section calculations** vs. scattering angle
- **Spectroscopic factor extraction** from experimental data
- **Nuclear structure studies** of isotopes

### Current Focus: Sulfur Isotopes

The `DW_36S_DP.in` file indicates ongoing work on:
- Reaction: ³⁶S(d,p)³⁷S at 8 MeV
- States analyzed:
  - Ground state (0 keV, 0f₇/₂ orbital)
  - First excited state (645 keV, 1p₃/₂ orbital)
- Goal: Determine single-particle structure of ³⁷S

### Theoretical Framework

**DWBA (Distorted Wave Born Approximation):**
- Treats nuclear reaction in two steps:
  1. Elastic scattering distortions (optical model)
  2. Single nucleon transfer (Born approximation)
- Requires optical potential parameters for projectile and ejectile
- Calculates angular distributions and absolute/relative cross-sections
- Spectroscopic factors relate theoretical to experimental cross-sections

---

## Dependencies

### Required
- **gfortran** (GCC Fortran compiler) with legacy Fortran support
- **Python 3** (for tools)

### Python Libraries
- **NumPy** - numerical operations
- **Plotly** - interactive plotting
- **SciPy** - interpolation and fitting (for `plot_dwuck.py --fit`)

### Installation
```bash
# macOS (Homebrew)
brew install gcc

# Python dependencies
pip install numpy plotly scipy
```

---

## Key Features

### Theoretical Capabilities
- ✅ Inelastic scattering
- ✅ Stripping reactions (d,p), (³He,d), etc.
- ✅ Pickup reactions (p,d), (d,³He), etc.
- ✅ Elastic scattering
- ✅ Spin-orbit coupling
- ✅ Non-local potentials
- ✅ Multiple L-transfer calculations
- ✅ Finite-range interactions

### Computational Features
- Multi-case batch processing
- Automatic Coulomb function generation
- Gaussian quadrature integration
- Radial wavefunction calculation
- Angular momentum coupling

---

## File Format Details

### Input Card Format
DWUCK4 uses Fortran fixed-format input cards:
- **Card 1:** 16-digit code + description
  - Controls calculation options (stripping/pickup, form factors, potentials)
- **Card 2:** Angular distribution parameters
  - Number of angles, starting angle, step size
- **Card 3:** Quantum numbers
  - L-transfers, spins, parities
- **Card 4:** Integration parameters
  - Step size (DRF), maximum radius (RMAX)
- **Cards 5+:** Optical potential parameters
  - Real/imaginary depths, radii, diffuseness

### Output Format
Text file containing:
- Echo of input parameters
- Optical potential details
- Radial wavefunctions
- **Angular distribution table**: Theta (deg) vs. Cross-section (mb/sr)
- Sum rules and spectroscopic information

---

## Common Issues and Solutions

### Compilation
- **Issue:** Syntax errors in old Fortran
- **Solution:** Use `--std=legacy` flag with gfortran

### Runtime
- **Issue:** Input format errors
- **Solution:** Use `make_dat.py` to ensure correct formatting

### Plotting
- **Issue:** No data extracted from output
- **Solution:** Check output file contains "Theta" header and numeric data rows

---

## Related Tools and Resources

### Optical Model Parameters
- Global parametrizations in `misc/` directory
- Koning-Delaroche potentials (commonly used)
- Varner potentials for nucleons
- Daehnick potentials for deuterons

### Alternative Codes
- **FRESCO**: More modern, flexible DWBA code
- **CHUCK3**: Related code (also by Kunz) for coupled-channels
- **PTOLEMY**: Another DWBA code

---

## License
GNU General Public License (see LICENSE file)

---

## Contact and Support
As noted in README.md:
- Original author: Peter Kunz (University of Colorado)
- Repository maintainer: Available for DWUCK assistance via email
- This is archived legacy code for community use

---

## Version Information
This appears to be the final release version of DWUCK4, dating from the 1980s-1990s era. The code has been stable and unchanged for decades, serving as a reliable tool for nuclear reaction calculations in the low-energy regime (< 200 MeV).
