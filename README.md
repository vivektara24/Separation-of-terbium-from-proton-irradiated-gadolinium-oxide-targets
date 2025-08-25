# Separation-of-terbium-from-proton-irradiated-gadolinium-oxide-targets

This repostiory contains the poster and abstract presented at the Annual Summer HIPPO meeting at Brookhaven National Lab on research performed during the summer fo 2024. The project was funded by the Department of Energy's Isotope Program. The research was conducted under the mentorship of Dr. Paul Ellison of the Medical Physics deparment at the University of Wisconsin Madison.

## Repository Contents
- 'serial.py' - Implements the Serial class, desinged to automate serial gamma-spectrum data analysis.
- 'calibration.py' - automatically determines calibration params and hpge efficiency fractional uncertainty.
- 'nuclear_physics_utils.py' - Utility functions designed to help the serial.py script
- 'example.py' - tutorial script on how to use the serial class.
  - Data for example in _ direcotry (can I use our actual spectra?)
  - example outputs in directory _.
- Data Accquisition - Directory with example JOB files to create compatible files names and autmoaticlaly record spectra on HPGe using ORTEC
    - Additionally contains linux or python? code to automatically rename files accoridngly
