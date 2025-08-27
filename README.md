# Separation-of-terbium-from-proton-irradiated-gadolinium-oxide-targets

This repository accompanies the project detailed in [Paper Title/Reference]. The included Python scripts were used to (i) calculate expected yields from proton irradiations of natGd₂O₃ targets, (ii) perform efficiency calibarion of a High Purity Germanium (HPGe) spectrometer, and (iii) automate the serial acquisition and analysis of HPGe spectra. In addition to computational work, the first version of the "**Terbinator**", a remote-controlled valve and pump module, was built to semi-automate multi-column extraction chromatographic serpations for ¹⁵⁵Tb. 

All code developed for this project has been consolidated into a single Python library, libname, which will continue to be developed into a comprehensive package desinged for applications in nuclear physics, nulcear chemistry, radiochemicstry, and machine learning challenges in radiopharmaceutical development. Source code and tutorials for libname v0.0.x are provided in this repostiory.

A detailed description with links of the contents of the repository are listed below.

## Table of Contents
- [Repository Contents](#repository-contents)
- [Setup Instructions](#setup-instructions)
- [Description of Methods](#de)
- [Quickstart Tutorials](#quickstart)
  - [Yield Class](#yield-class)
  - [Serial Class](#serial-class)
  - [Calibration Class](#calibration-class)
- [`.Spe` File Naming Convention (Serial)](#spe-file-naming-convention)
## Repository Contents

### Python Modules
1. **`yield_calc.py`** – Implements the `Yield` class. Calculates theoretical end-of-bombardment (EoB) activity yields for irradiated targets.
2. **`calibration.py`** – Implements the `Calibration` class. Streamlines workflows for HPGe detector efficiency calibration.
3. **`serial.py`** – Implements the `Serial` class. Provides a pipeline for automated analysis of serial γ-spectra measurements.
4. **`nuclear_physics_utils.py`** – A collection of utility functions used internally by `yield_calc.py`, `calibration.py`, and `serial.py`.

### Tutorials
- **`tutorials/`** – Contains interactive **Google Colab** Juypter notebooks demonstrating how to use each core class:
  - `serial_tutorial.ipynb`
  - `calibration_tutorial.ipynb`
  - `yield_tutorial.ipynb`

### Data Acquisition
- **`data_acquisition/`** – Example JOB files for automated HPGe spectrum collection using MAESTRO (Windows v7.01, ORTEC®).
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


- **Download source files as ZIP (no git required)**
1. Navigate to this repository's main page on Github
2. Click the green **Code** button → **Download ZIP**.
3. Unzip it on your computer.

**Download Specific Files (via scp/curl/wget)**
If you only need certain files (e.g `serial.py`, `utils.py`), you can fetch them directly:
```bash
wget https://raw.githubusercontent.com/vivektara24/Separation-of-terbium-from-proton-irradiated-gadolinium-oxide-targets/main/serial.py
wget https://raw.githubusercontent.com/vivektara24/Separation-of-terbium-from-proton-irradiated-gadolinium-oxide-targets/main/nuclear_physics_utils.py
```


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

## Quickstart Tutorials

### Quickstart Example w/ the Yield Class

This section provides an example using the `Yield` class to demostrate the workflow.

#### Step 1. Import the Necessary Libraries
```python
from yield_calc import Yield
from datetime import datetime
import numpy as np
import pandas as pd
```

#### Step 2. Define Inputs

```python
df = pd.read_csv('Gd2O3-SRIM-Data.csv')
srim_energies = df.iloc[:, 0]
srim_ranges = df.iloc[:, 1]
```

#### Step 3. Create the Yield Object

```python
y = Yield(E0=12.6, srim_energies=srim_energies, srim_ranges=srim_ranges, 
          target_thickness=0.037, dE=0.001, density=3.385, molecular_weight=362.50, projectile_intensity=2.37 * 10 ** 13, t_irrad=1800)
```

#### Step 4. Load reaction data from directory
```python
y.load_reactions_from_csvs(
    directory=".",
    isotope_half_lives=isotope_properties,
    filename_glob="NatGd_P_X_*.csv",  # or "*.csv"
    energy_col=0,
    xs_col=1,
    xs_units="mb",  # change if your CSVs are in barns/µb/nb/etc.
)
```

#### Step 5. Compute Expected Activites and save resutls to an xslx.
```python
results = y.compute_activities_for_multiple_isotopes()
path = y.save_results_to_excel("outputs/isotope_results.xlsx", include_summary=True)
```
### Quickstart Example w/ the Calibration Class

This section provides a minimal example using the `Serial` class to demostrate the workflow. A more complete tutorial is available in [`example.py`](example.py). Additionally the Application Programming Interface is available in .

#### Step 1. Import the Necessary Libraries

from calibration import Calibration
import numpy as np
import pandas as pd
import math

#### Step 2. Define the Inputs

```python
data_path = ''

eob_time = datetime(1984, 8, 1, 00)

gammas = pd.DataFrame({
    "energy": [121.7817, 244.6975, 344.2785, 778.904, 964.079, 1112.074, 1408.006], #152Eu
    "intensity": [28.53,    7.55,     26.59,    12.93,   14.51,   13.67,    20.87],
    "unc_intensity": [0.16,    0.04,     0.20,     0.08,    0.07,    0.08,     0.09],
    "isotope": ["152EU"] * 7,
})

# Dictionary mapping energy values (keV) to half-lives (seconds)
half_lives = {
    # 152Eu
    121.7817: 13.517 * 365 * 24 * 60 * 60,
    244.6975: 13.517 * 365 * 24 * 60 * 60,
    344.2785: 13.517 * 365 * 24 * 60 * 60,
    778.904: 13.517 * 365 * 24 * 60 * 60,
    964.079: 13.517 * 365 * 24 * 60 * 60,
    1112.074: 13.517 * 365 * 24 * 60 * 60,
    1408.006: 13.517 * 365 * 24 * 60 * 60,

}

inital_activity = {
    # 152Eu
    121.7817: 10,
    244.6975: 10,
    344.2785: 10,
    778.904: 10,
    964.079: 10,
    1112.074: 10,
    1408.006: 10,
}

initial_guesses = [-0.306655,-7.80031,0.739484,-0.0959825,0.00513815,-0.00121]

def EffFit(x,b1,b2,b3,b4,b5,b6):

    x = x/1000
    y = math.e**(b1*x**1+b2*x**0+b3*x**(-1)+b4*x**(-2)+b5*x**(-3)+b6*x**(-4))
    return y

cb = Calibration(data_path=data_path, eob_time=eob_time, gammas=gammas, half_lives=half_lives, initial_activites=inital_activity, eff_func=EffFit)

cb.process_spectrum_file()

cb.save_peak_data("outputs/eff_peak_data.csv")

cb.process_calibration_data(initial_guesses=p0, plot_directory='outputs', xlim=(59, 1450), ylim=(0, 3.5e-5))

print(cb.get_eff_fit_uncetainty())
```
### Quickstart Example w/ the Serial Class

This section provides a minimal example using the `Serial` class to demostrate the workflow. A more complete tutorial is available in [`example.py`](example.py). Additionally the Application Programming Interface is available in .

#### Step 1. Import the Necessary Libraries

```python
from yield_calc import Yield
from datetime import datetime
import numpy as np
import pandas as pd
```

#### Step 2. Define Inputs
Begin by specifying all required inputs for the analysis: the direcotry containing .Spe files, the end-of-bombardment (EoB) timestamp, the HPGe effeciecy cure function and parameters, a gamma-line table, and half-lives. To expeirmentally determine `EFFICENCY_FIT_PARAMS` on an HPGe detector, refer to the supplementary information of the linked paper (**"High Purity Germanium Detector Calibration Methods"**)

```python
# Directory with .Spe files
DATA_DIR = "example_data/"

# End-of-bombardment timestamp
EOB_TIME = datetime(2025, 2, 21, 7, 58)

# Example HPGe efficiency curve parameters
EFFICIENCY_FIT_PARAMS = [0.0377, -13.3, 0.9218, -0.0928, 0.0030, 0.0]

# Example HPGe effeciency function
def EffFit(energy_keV: np.ndarray | float,
           b1: float, b2: float, b3: float, b4: float, b5: float, b6: float) -> np.ndarray:
    x = np.asarray(energy_keV, dtype=float) / 1000.0  # keV → MeV
    y = np.exp(b1 * x**1 + b2 * x**0 + b3 * x**-1 + b4 * x**-2 + b5 * x**-3 + b6 * x**-4)
    return y

# Gamma-line table (example: 154m1Tb at 540.18 keV, 20% intensity, 3% uncertainty)
GAMMAS = pd.DataFrame({
    "energy":       [540.18],
    "intensity":    [20.0],
    "unc_intensity":[3.0],
    "isotope":      ["154TB"],
})

# Half-lives: energy (keV) → half-life (s)
HALF_LIVES = {
    540.18:   9.4 * 60 * 60,
}
```

Instantiate the Serial class with the defined inputs to set up the analysis.

```python
# Create analysis object
    S = Serial(
        data_directory=str(DATA_DIR),
        eob_time=EOB_TIME,
        efficiency_fit_params=list(EFFICIENCY_FIT_PARAMS),
        detector_eff_uncertianty=0.0860345384967799,  # 8.6% example (fractional)
        gammas=GAMMAS,
        half_lives=HALF_LIVES,
    )
```
Peform peak fitting across all spectra and store the results internally in the `Serial` object.

```python
# Process spectra
S.process_spectrum_files(plot_dir="plots/")
```

Save the peak-fit results to an xlsx file, grouped by gamma-line and sorted by decay time.

```python
# Save sorted peak fit data
S.save_peak_data(
        filepath=str(outputs_dir / "peak_data_by_gamma.xlsx"),
        sort_key="decay time (s)",
        columns=[
            "file", "isotope", "energy", "decay time (s)",
            "counts", "unc_counts", "intensity", "unc_intensity",
            "detector efficiency", "activity", "uncertainty activity",
            "eob activity", "uncertainty eob activity",
        ],
        include_summary=True,
    )
```

Fit exponential decays to the start of measurment activities to extract EoB activiteis and half-life values.

```python
# Run decay analysis
S.process_decay_data(plot_directory="plots/decay-fits")
```

Save the final decay data (including fitted EoB activities and half-lives) to a xlsx.

```python
# Save final results
S.save_decay_data(outputs_dir / "decay_results_vkt.xlsx")
```

## Example Output of Serial Class

## `.Spe` File Naming Convention  

Important experimental details are encoded directly in the `.Spe` filenames.  

In the `process_spectrum_files` method of the `Serial` class, each `.Spe` file is read and its filename is split on hyphens (`-`). The parser looks for a token of the form **`d1sXXX`** (e.g., `d1s200`), where `XXX` are digits representing the distance (in cm) between the sample and the face of the HPGe detector.  

This distance token is required to perform inverse-square law corrections when the measurement geometry differs from the HPGe calibration geometry. The token may appear anywhere in the filename, as long as it is a hyphen-delimited part.  

#### ✅ Valid Filenames  

1. `120-Min-Decay-Report-d1s200-001.Spe`  
2. `30-Min-Background-d1s5.Spe`  
3. `1-Hr-Scan-something-d1s42-more.Spe`  

#### ❌ Invalid Filenames  

1. `120-Min-Decay-Report-d1sABC-001.Spe` *(non-numeric value after `d1s`)*  
2. `120-Min-Decay-Report-DS1-001.Spe` *(incorrect token spelling/case)*  
3. `120-Min-Decay-Report-001.SPE` *(missing `d1s` token; case-sensitive extension may also cause issues)*

Example `.JOB` files for automated HPGe spectrum collection using **ORTEC® MAESTRO for Windows (v7.01)** are provided in the [`data_acquisition/`](data_acquisition/) directory of this repository. These job files define acquisition parameters and save spectra with filenames following the convention above.


#### Improvments

1. peak summing in calibration class
2. the two methods in Knoll for HPGe detectors
3. optimzation techniques for yield class, using rx.Integrate maybe.
