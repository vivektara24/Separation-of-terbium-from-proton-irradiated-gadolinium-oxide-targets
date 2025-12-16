# Separation-of-terbium-from-proton-irradiated-gadolinium-oxide-targets

<p align="center">
  <img src="images/medphys.png" alt="HIPPO Logo" height="120"/>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="images/hippo.png" alt="UW Medical Physics Logo" height="120"/>
</p>


**This work is supported in part by the Horizon-broadening Isotope Production Pipeline Opportunities (HIPPO) program, under GrantDE-SC0022550 from the Department of Energy's Isotope R&D and Production Program.
**

## Overview
This repository accompanies the project detailed in **_Separation of terbium from proton-irradiated gadolinium oxide targets – development of an effective, scalable and automatable process_ (Applied Radiation and Isotopes, 2025)** — see [https://doi.org/10.1016/j.apradiso.2025.112138](https://doi.org/10.1016/j.apradiso.2025.112138).
 The included Python scripts were used to (i) calculate expected yields from proton irradiations of natGd₂O₃ targets, (ii) perform efficiency calibarion of a High Purity Germanium (HPGe) spectrometer, and (iii) automate the analysis of serial HPGe measurments. In addition to computational work, the first version of the "**Terbinator**", a remote-controlled valve and pump module, was built to semi-automate multi-column extraction chromatographic serpations for ¹⁵⁵Tb. 

All code developed for this project has been consolidated into a single Python library, **nuclab**, which will continue to be developed into a comprehensive package desinged for applications in nuclear physics, nulcear chemistry, radiochemicstry, and machine learning challenges in radiopharmaceutical development. Source code and tutorials for **nuclab** are provided in this repostiory. Representative example outputs are shown below.

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
      <a href="example_outputs/efficiency_peak_data.csv">Peak fit data + per-line efficiency values (CSV)</a> · 
      <a href="example_outputs/calibration-results.xlsx">Efficiency fit parameters + fractional uncertainty (XLSX)</a>
    </td>
    <td align="center">
      <a href="example_outputs/per-line-peak-data.xlsx">Serial peak fit results (XLSX)</a> · 
      <a href="example_outputs/decay-analysis-results.xlsx">Decay analysis results (XLSX)</a>
    </td>
  </tr>
</table>

<p align="center">
 <td align="center"><em>Per-slice isotope activities & totals using the <code>Yield</code> class</em></td>
 <a href="example_outputs/theoretical-yield-results.xlsx">Theoretical yield results (XLSX)</a>
</p>

## Design Limitations
1. There are currently no warning messages if required class attributes arent filled before calling the functions, Instead the output will simply be incomplete.


## Table of Contents
- [Repository Contents](#repository-contents)
- [Setup Instructions](#setup-instructions)
- [Theory](#theory)
  - [Radiation Production](#radiation-production)
  - [γ-Decay](#γ-decay)
  - [Radiation Detection](#radiation-detection)
  - [Radiochemistry Concepts](#radiochemistry-concepts)
  - [Activation-Analysis](#activation-analysis)
  - [Nuclear Medicine](#nuclear-medicine)
- [References](#references)
- [Acknoledgements](acknowledgments)
## Repository Contents

### Source Files
- **`src/`** – Contains the core Python implementation of **nuclab**. Each file defines a module within the package.
  - **`production.py`** – Implements the `Yield` class. Calculates theoretical end-of-bombardment (EoB) activity yields for accelerator produced radionuclides.
  - **`calibration.py`** – Implements the `Calibration` class. Streamlines workflows for HPGe detector absolute efficiency calibration.
  - **`serial.py`** – Implements the `Serial` class. Provides a pipeline for automated analysis of serial γ-spectra measurements saved in `.Spe` format.
  - **`utils.py`** – A collection of utility functions used internally by `production.py`, `calibration.py`, and `serial.py`.

### Workflow Tutorials
- **`workflows/`** – Contains interactive **Google Colab** Juypter notebooks demonstrating how to use each core class:
  - **`calibration_to_serial_workflow.ipynb`** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vivektara24/Separation-of-terbium-from-proton-irradiated-gadolinium-oxide-targets/blob/main/workflows/calibration_to_serial_workflow.ipynb) Demonstrates how to combine the `Calibration` and `Serial` classes to perform detector absolute efficiency calibration and analysis of serial HPGe measurements.
  - **`yield_workflow.ipynb`**[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vivektara24/Separation-of-terbium-from-proton-irradiated-gadolinium-oxide-targets/blob/main/workflows/yield_workflow.ipynb) Demonstrates how to use the `Yield` class to calculate theoretical end-of-bombardment (EoB) activity values.

### Data Acquisition
- **`serial_data_acquisition/`** – Example JOB files for automated HPGe spectrum collection using MAESTRO (Windows v7.01, ORTEC®).
  - A description of the required file naming convention and examples of acceptable file names  
  - Includes example JOB files with compatible file naming conventions for automated spectrum recording.


#### Methods

The HPGe efficiency (Eff) calibration curve was obtained using 241Am, 133Ba, 137Cs, and 152Eu calibration sources, (Amersham UK); The radionuclides, their half-lives, calibration gamma-ray energies, intensities, and associated uncertainties are summarized in Supplementary Table 1. Measured efficiencies and their uncertainties were calculated with errors propagated through the quadrature sum of uncertainty contributions from the transition intensity and counting statistics. A polynomial of the natural logarithm of the efficiency was fit to these data using a non-linear least squares algorithm (Python, scipy.optimze.curve_fit, Eq. (S1)),

Eff_best(E) = exp(b1*E^1 + b2*E^2 + b3*E^3 + b4*E^-2 + b5*E^-3 + b6*E^-4)

where 𝑏1, ..., b6 are the efficiency fit parameters. The efficiency was assessed at 200 cm from the face of the HPGe spectrometer. Corrections were made using the inverse square law for measurements taken at different distances from the HPGe spectrometer. Uncertainty in HPGe detector efficiency was estimated as the average plus one standard deviation of the experimentally measured efficiency relative residual absolute values, resulting in an 8.6% relative efficiency uncertainty.

**Supplementary Table S1. Gamma-ray energies used for HPGe calibration**

| Radionuclide | Half-Life (y) | Eγ (keV) | Iγ (%) | Uncertainty Iγ (%) |
|-------------|---------------|----------|--------|--------------------|
| 241Am | 432.6 | 59.5412 | 35.9 | 0.40 |
| 152Eu | 13.517 | 121.7817 | 28.53 | 0.16 |
|  |  | 244.6975 | 7.55 | 0.04 |
|  |  | 344.2785 | 26.59 | 0.20 |
|  |  | 778.904 | 12.93 | 0.08 |
|  |  | 964.079 | 14.51 | 0.07 |
|  |  | 1112.074 | 13.67 | 0.08 |
|  |  | 1408.006 | 20.87 | 0.09 |
| 133Ba | 10.536 | 80.9971 | 32.9 | 0.30 |
|  |  | 276.7364 | 7.16 | 0.05 |
|  |  | 302.853 | 18.34 | 0.13 |
|  |  | 356.017 | 62.05 | 0.00 |
|  |  | 383.851 | 8.94 | 0.06 |
| 137Cs | 30.007 | 661.657 | 85.10 | 0.20 |



## References

- Glenn F. Knoll. Radiation Detection and Measurement. 4th edition, Wiley, 2010 (ISBN
978-0-470-13148-0)

- Frank Herb Attix. Introduction to Radiological Physics and Dosimetry, John Wiley & Sons,
Inc. 1986 or reprinted in 2004 Wiley VCH

- Loveland, W. D., Morrissey, D. J., & Seaborg, G. T. (2017). Modern nuclear chemistry. https://doi.org/10.1002/9781119348450

- Krane, K. S., & Lynch, W. G. (1989). Introductory Nuclear Physics. Physics Today, 42(1), 78. https://doi.org/10.1063/1.2810884

- Holiski, Connor K., et al. “Adsorption of terbium (III) on DGA and LN resins: Thermodynamics, isotherms, and kinetics.”
Journal of Chromatography A, vol. 1732, 2024, article no. 465211. https://doi.org/10.1016/j.chroma.2024.465211.

- Poole, C F, and Elsevier (Amsterdam. The Essence of Chromatography. Amsterdam, Elsevier, 2010.

## Useful Links

- [Packaging Python Projects (official tutorial)](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

``But I'm not a rapper``

``You know what I mean?``

## Gd2O3 Recycling and The Failed Proton Activation Analysis

The 5- and 10-minute interval measurments taken ~1hr post eob described above were intially taken with the intention of assessing the elemental composition of natGd2O3 recyled through the process described in the accompaying paper.

After going through through the radiochemical seperation process, ~95% of the Gd is recovered in the first 4 rinse fractions (~40mL 0.2M HNO3) of the first LN2 column. The fractions are dried down, leaving behind Gd(NO3)3 * XH2O salf. In the recovery process, across the temperature gradient (time) of the process, the composition of Gd(NO3)3 takes place through the following scheme shown in _Non-isothermal kinetics of the thermal decomposition of gadolinium nitrate._

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?350-450^{\circ}C:\;Gd(NO_{3})_{3}\;\rightarrow\;GdO(NO_{3})\;+\;aNO_{x}\;+\;bN_{2}\;+\;cO_{2}" />
</p>

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?450-550^{\circ}C:\;GdO(NO_{3})\;\rightarrow\;\tfrac{1}{4}Gd_{4}O_{5}(NO_{3})_{2}\;+\;dNO_{x}\;+\;eN_{2}\;+\;fO_{2}" />
</p>

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?550-700^{\circ}C:\;Gd_{4}O_{3}(NO_{3})_{2}\;\rightarrow\;2Gd_{2}O_{3}\;+\;gN_{2}\;+\;hO_{2}" />
</p>

It was confirmed by XRD that a ramping rate of 2C/min allowed for a complete denitration process, however when starting the ramping from 180C we observed some gadolinum nitrate still present in the final product.

<table>
  <tr>
    <td align="center"><img src="images/Picture9.png" alt="Calibration Plot" width="250"/></td>
    <td align="center"><img src="images/failedrec0.svg" alt="Decay Plot" width="250"/></td>
  </tr>
</table>

<p align="center">
  <em>
    Initial failed recycling that did not dissolve – likely was not Gd<sub>x</sub>(NO<sub>3</sub>)<sub>x</sub> (p35).  
    Failed dissolution w/ heat gun, later dissolved more so in conc. HNO₃ (p36).  
    Denitrated with some flaky white precipitate; had insoluble grey, then white flakes after GL32 drying.  
    Flakes and powder stuck to quartz tube very high up. – Furnace set from 180 °C to 600 °C but at a fast ramp rate of 16 °C/min.
  </em>
</p>

Additional comments from failed recycling processes:

6/19/2024 Recycling description: "furnace pushed from 180C to 400C to 600C. Done on two separate days (p33 and 37) due to yellowish color of powder."

10/10/2024 Recyling description: "SLOW RAMP (2C/min from 180-600C, then 2 hours at 600C)"


However numerous tests have shown that with careful experimental manipuation, AA is an accurate (~1% accuracy) and precise (~5% precision) method of measuring elemental concentrations. We attempted to quantify the number of 14N atoms remaining in the recycled natGd2O3, by measuring the 11C activity that is created in the 14N(p, alpha)11C reaction

 We attempted to quantify the number of 14N (99.579% nat. abundance) atoms in a target made from recycled materials, by measuring the amount of 11C that was created in the 14N(p, alpha)11C reaction. Complications in this procedure immediatley rise from the short-half life of 11C (~20 mins) and the fact that its only gamma emission is a 511 keV peak which contains lots of background. To further complicate the process The oxygen present in both gadolinium oxide and the various nitrate compounds undergoes the 16O(p, alpha)13N reaction to create another short-lived (~10 min), only 511 keV peak emitting radiosoptes. And once again to further complicate this process, 152Tb, 153Tb, 154Tb, 156Tb, and 158Tb are all B+ emitting radionuclides that were created in the irradiation.

The irrdidiations were conducted with the intent of creating tracer-scale amounts of Tb to use in the isolation expeiriments. Immediatley post eob the activity from the target was measured to be somewhere ~10 mCi. This level of activity lead to deadtimes greater than 10% at the maximum possible distance from the face of the hpge detector until ~45mins (~2x half-lives, ~4.5 half-lives of the isotopes respectivley) leading to a lack of statistics for the curve fitting to near eob to fit inital activities. In a "crude" attempt to quantify the results of the 5- and 10-min serial measurements we fit a sum of exponentials to 511 keV peak activity (using an average of the 11C and 11N 551 keV emission intensity) accross the measurements. We dont take into account any of the producued Tb isotopes. 

The atomic areal densities of 14N and 16O in the sample was determined to be 5.4x10^19 atoms/cm2 and 1.8e20 atoms/cm2 respectivley. We have a total pocket radius of 5cm giving 4.2x10^19 14N atoms and 1.4x10^20 16O atoms respectivley. 

Total number O = O from Gd2O3 + O from nitrates

Total number 0 - total number O * 

## Things I wanted to add but cba
- Interaction of Radiaion w/ Matter
  - Quantities for Describing The Interaction of Ionizing Radiation w/ Matter.
  - Exponential Attenuation
  - Gamma- and X-Ray Interactions in Matter
  - Charged Particle Interactions in Matter
- General Detector Properties
- ionizing radation chapter attix, charged particle equilibirum, 
- Lack of enriched 160Gd, implications for 161Tb production
- counting statstics

  
Some fraction of the incoming particle energy is imparted to the kinetic energy of
the compound nucleus to achieve conservation of momentum.

How is 161Tb an Auger emitter if it decays by B- 100% of the time to a stable isotope? approximately eleven Auger electrons (where did that come from?)

No carrier added?

Is coulomb barrier included in the threshold energy? or is the threshold energy stricly in terms of inducing a nuclear change post getting past the coulomb barrier?

The incident particle has many collisions inside the nucleus, depositing its energy to many
nucleons and becoming indistinguishable from them. This results in a highly excited
“compound nucleus” that can then “de-excite” in a process totally decoupled from the
incident event.

Deuterium-Tritium fission reactions

## Acknowledgments

I would first like to thank **Justin Peikin** who built this project from the ground up. The work in **_Separation of terbium from proton-irradiated gadolinium oxide targets – development of an effective, scalable and automatable process_ (Applied Radiation and Isotopes, 2025)** — see [https://doi.org/10.1016/j.apradiso.2025.112138](https://doi.org/10.1016/j.apradiso.2025.112138) can be largely attributed to his dedication to the project and foundational work.

I am also grateful to **Taylor Johnson** who built the control box of the **Terbinator**.

In addition, I would like to thank Dr. Jonathan Morrell, creator of the CURIE python package, for his constructive feedback on the _CURIE Toolkit Gamma Spectroscopy Peak Fitting Methods_ supplementary material section.

The Irrations were peformed carried out by the **Cyclotron Gang** at UW-Madison under the supervision of **Dr. Todd Barnhart** and **Dr. John Engle**.

Finally, I am thankful Dr. Ellison who encouraged me to explore the addtional topics presented in this repository.


**This work is supported in part by the Horizon-broadening Isotope Production Pipeline Opportunities (HIPPO) program, under GrantDE-SC0022550 from the Department of Energy's Isotope R&D and Production Program.
**
