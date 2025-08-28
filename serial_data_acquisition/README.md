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
