# Separation-of-terbium-from-proton-irradiated-gadolinium-oxide-targets


## Overview
This repository accompanies the project detailed in [_Separation of terbium from proton-irradiated gadolinium oxide targets – development of an effective, scalable and automatable process_(Applied Radiation and Isotopes, 2025)](https://doi.org/10.1016/j.apradiso.2025.112138). The included Python scripts were used to (i) calculate expected yields from proton irradiations of natGd₂O₃ targets, (ii) perform efficiency calibarion of a High Purity Germanium (HPGe) spectrometer, and (iii) automate the analysis of serial HPGe spectra. In addition to computational work, the first version of the "**Terbinator**", a remote-controlled valve and pump module, was built to semi-automate multi-column extraction chromatographic serpations for ¹⁵⁵Tb. 

All code developed for this project has been consolidated into a single Python library, **libname**, which will continue to be developed into a comprehensive package desinged for applications in nuclear physics, nulcear chemistry, radiochemicstry, and machine learning challenges in radiopharmaceutical development. Source code and tutorials for libname v0.0.x are provided in this repostiory. Representative example outputs are shown below.

<table>
  <tr>
    <th colspan="2" style="text-align:center">Example outputs of the <code>nuclab</code> Python package</th>
  </tr>
  <tr>
    <td align="center"><img src="example_outputs/calibration-plot.png" alt="Calibration Plot" width="400"/></td>
    <td align="center"><img src="example_outputs/decay_plots/154TB_540.180_activity-time.png" alt="Decay Plot" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><em>Fitted efficiency curve for HPGe detector using the <code>Calibration</code> class</em></td>
    <td align="center"><em>Exponential decay of ¹⁵⁴ᵐ¹Tb derived from serial HPGe spectra using the <code>Serial</code> class</em></td>
  </tr>
  <tr>
    <td align="center">
      <a href="example_outputs/calibration-results.csv">CSV</a> · 
      <a href="example_outputs/calibration-results.xlsx">XLSX</a>
    </td>
    <td align="center">
      <a href="example_outputs/154Tb_decay_results.csv">CSV</a> · 
      <a href="example_outputs/154Tb_decay_results.xlsx">XLSX</a>
    </td>
  </tr>
</table>



A detailed description with links of the contents of the repository are listed in the Table of Contents below.

## Table of Contents
- [Repository Contents](#repository-contents)
- [Setup Instructions](#setup-instructions)
- [`.Spe` File Naming Convention (Serial)](#spe-file-naming-convention)
- [Description of Methods](#de)
- [Acknoledgements](acknoldgments)
## Repository Contents

### Source Files
- **`src/`** – Contains the core Python implmentation of **libname**.
  - **`production.py`** – Implements the `Yield` class. Calculates theoretical end-of-bombardment (EoB) activity yields for irradiated targets.
  - **`calibration.py`** – Implements the `Calibration` class. Streamlines workflows for HPGe detector efficiency calibration.
  - **`serial.py`** – Implements the `Serial` class. Provides a pipeline for automated analysis of serial γ-spectra measurements.
  - **`utils.py`** – A collection of utility functions used internally by `production.py`, `calibration.py`, and `serial.py`.

### Workflow Tutorials
- **`workflows/`** – Contains interactive **Google Colab** Juypter notebooks demonstrating how to use each core class:
  - **`calibration_to_serial_workflow.ipynb`** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vivektara24/Separation-of-terbium-from-proton-irradiated-gadolinium-oxide-targets/blob/main/workflows/calibration_to_serial_workflow.ipynb) Demonstrates how to combine the `Calibration` and `Serial` classes to perform detector energy calibration and analyze serial HPGe measurements.
  - **`yield_workflow.ipynb`**

### Data Acquisition
- **`serial_data_acquisition/`** – Example JOB files for automated HPGe spectrum collection using MAESTRO (Windows v7.01, ORTEC®).
  - Includes example JOB files with compatible file naming conventions for automated spectrum recording.
  - May also include Linux/Python scripts for automatically renaming files as needed.

## Setup Instructions

You have three options for using the libname package:

- **Option 1: Pip Install (recommended)**  
  *(Coming soon, once available on PyPI)*
  ```bash
  pip install <package-name>
  ```
- **Option 2: Clone the Repository**  

```bash
git clone https://github.com/vivektara24/Separation-of-terbium-from-proton-irradiated-gadolinium-oxide-targets.git
cd Separation-of-terbium-from-proton-irradiated-gadolinium-oxide-targets
```

If you only need specfic files (e.g, `serial.py`, `utils.py`), you can fetch them directly with `wget` / `curl`:
```bash
wget https://raw.githubusercontent.com/vivektara24/Separation-of-terbium-from-proton-irradiated-gadolinium-oxide-targets/main/serial.py
wget https://raw.githubusercontent.com/vivektara24/Separation-of-terbium-from-proton-irradiated-gadolinium-oxide-targets/main/utils.py
```

- **Option 3: Download as ZIP (no git required)**  
1. Navigate to this repository's main page on GitHub
2. Click the green **Code** button → **Download ZIP**.
3. Unzip it on your computer.

#### Step 2. Install Dependencies
Install the required Python libraries using the provided `requirements.txt`:
```bash
pip install -r requirements.txt
```

#### Step 3. Run the Example
Try the tutorial in `example.py` to verify your installation.
```python
python example.py
```
## Example Output of Serial Class

## Package Improvment Ideas

1. peak summing in calibration class
2. the two methods in Knoll for HPGe detectors
3. optimzation techniques for yield class, using rx.Integrate maybe.
5. provide more informative statistics for qulatiy of curve fit
7. warning messages if attributes arent filled before calling the functions
9. Give default values based on work
10. save eff_fit_params

## Useful Links

- [Packaging Python Projects (official tutorial)](https://packaging.python.org/en/latest/tutorials/packaging-projects/)


## Acknowledgments

This work is supported in part by the Horizon-broadening Isotope Production Pipeline Opportunities (HIPPO) program, under GrantDE-SC0022550 from the Department of Energy's Isotope R&D and Production Program.
