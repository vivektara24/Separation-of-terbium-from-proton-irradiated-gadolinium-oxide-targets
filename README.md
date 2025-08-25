# Separation-of-terbium-from-proton-irradiated-gadolinium-oxide-targets

## Repository Contents
- 'serial.py' - Implements the Serial class, desinged to automate serial gamma-spectrum data analysis.
- 'calibration.py' - automatically determines calibration params and hpge efficiency fractional uncertainty.
- 'nuclear_physics_utils.py' - Utility functions designed to help the serial.py script
- 'example.py' - tutorial script on how to use the serial class.
  - Data for example in _ direcotry (can I use our actual spectra?)
  - example outputs in directory _.
- data_acquisition/ - Example JOB files for automated HPGe spectrum collection using MAESTRO for Windows, version 7.01, ORTEC®.
-
-
- Directory with example JOB files to create compatible files names and autmoaticlaly record spectra on HPGe using ORTEC
    - Additionally contains linux or python? code to automatically rename files accoridngly

## Tutorial: Quickstart Example

You must first download the serial.py file and the nuclear_physics_utils files and place them in the same direcory as your file that you plan to do the analysis in.

Import the Serial class and other reqired dependencies.
- Need to make a dependency list

To run an analysis, first define your inputs - the data directory, end-of-bombardment (EOB) time, and detector efficiency fit parameters.

```python
from serial import Serial
from datetime import datetime

# Directory with .Spe files
DATA_DIR = "example_data/"

# End-of-bombardment timestamp
EOB_TIME = datetime(2025, 2, 21, 7, 58)

# Example HPGe efficiency curve parameters
EFFICIENCY_FIT_PARAMS = [0.0377, -13.3, 0.9218, -0.0928, 0.0030, 0.0]

# Create analysis object
S = Serial(
    data_directory=DATA_DIR,
    eob_time=EOB_TIME,
    efficiency_fit_params=EFFICIENCY_FIT_PARAMS,
)

# Process spectra and run decay analysis
S.process_spectrum_files(plot_dir="plots/")
S.process_decay_data(plot_directory="plots/decay-fits")
'''

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
