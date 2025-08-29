# Separation-of-terbium-from-proton-irradiated-gadolinium-oxide-targets


## Overview
This repository accompanies the project detailed in **_Separation of terbium from proton-irradiated gadolinium oxide targets – development of an effective, scalable and automatable process_ (Applied Radiation and Isotopes, 2025)** — see [https://doi.org/10.1016/j.apradiso.2025.112138](https://doi.org/10.1016/j.apradiso.2025.112138).
 The included Python scripts were used to (i) calculate expected yields from proton irradiations of natGd₂O₃ targets, (ii) perform efficiency calibarion of a High Purity Germanium (HPGe) spectrometer, and (iii) automate the analysis of serial HPGe spectra. In addition to computational work, the first version of the "**Terbinator**", a remote-controlled valve and pump module, was built to semi-automate multi-column extraction chromatographic serpations for ¹⁵⁵Tb. 

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




A detailed description with links of the contents of the repository are listed in the Table of Contents below.

## Table of Contents
- [Repository Contents](#repository-contents)
- [Setup Instructions](#setup-instructions)
- [Theory](#theory)
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
  - **`yield_workflow.ipynb`**[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vivektara24/Separation-of-terbium-from-proton-irradiated-gadolinium-oxide-targets/blob/main/workflows/yield_workflow.ipynb) Demonstrates how to use the `Yield` class to calculate theoretical end-of-bombardment (EoB) activity values.

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

## Theory

Consider a large number **N** of identical radioactive atoms. We define **λ** as the total radioactive decay constant, which has dimensions of reciprocal time (typically s⁻¹).  

The product of λ and a time interval *t* (in consistent units) gives the probability that an individual atom will decay during that interval, valid for time intervals **≪ 1/λ**. We make the well-established assumption that λ is independent of the age of the atom and of all physical and chemical conditions such as temperature, pressure, concentration, etc.

The expectation value of the total number of atoms in the group that disintegrate per unit time, for intervals very short compared to **1/λ**, is called the **activity** of the group:

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?A=\lambda%20N" />
</p>

This has units of inverse time, since **N** is a dimensionless number.  

So long as the original group is not replenished by additional nuclei, the rate of change in **N** at any time *t* is equal to the activity:

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?-\frac{dN}{dt}=\lambda%20N" />
</p>


The old unit of activity was the **curie (Ci)**, originally defined as the number of disintegrations per second occurring in a mass of 1 g of ²²⁶₈₈Ra.  
Later the definition was divorced from the radium standard and fixed to:

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?1\,\text{Ci}=3.7\times10^{10}\,\text{s}^{-1}" />
</p>

(1 g of ²²⁶Ra has an activity of 0.988 Ci).  

More recently, the SI unit **becquerel (Bq)** was adopted, defined as:

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?1\,\text{Bq}=1\,\text{s}^{-1}" />
</p>

- **1 Ci** = 3.7 × 10¹⁰ Bq  
- **1 mCi** = 3.7 × 10⁷ Bq  
- **1 µCi** = 3.7 × 10⁴ Bq  

Stable nuclei may be transformed into radioactive species by bombardment with suitable particles, or photons at sufficiently high energy. The purpose of an accelerator of charged particles is to direct against a target a beam of a specific kind of particles of a chosen energy. Low energy accelerators are used to produce beams in the 10-100-MeV range, often for reaction or scattering studies to elucidate the structure of specific final states, perhaps even individual excited states. These accelerators should have accurate energy selection and reasonably high currents because the ultimate precision of many expirments is limited by counting statistics.

A [cyclotron](https://www.youtube.com/watch?v=cutKuFxeXmQ) is one type of particle accelerator. It is a circular device in which a beam of particles makes many (often hundreds) of revolutions, receiving a small voltage increment on each orbit until the particles reach energies in the MeV range. The earliest and simplest of these accelerators is the cyclotron, sometimes referred to as a magnetic resonance accelerator. The essential design idea of the cyclotron was concieved by Ernest Lawrence at the University of California Berkeley in 1929. The critical feature is that the time it takes for a particle to travel one semicircular path is independent of the radius of the path--as particles spiral to larger radii, they also gain energy and move at greater speed, and the gain in path length is exactly compensated by the increased speed. If the half-period of the AC voltage on the dees is set equal to the semicircular orbit time, then the field alternates in exact synchronization with the passage of particles through the gap, and the particle sees an accelerating voltage each time it crosses the gap.

The Lorentz force in the circular orbit, **qvB**, provides the necessary centripetal acceleration to maintain the circular motion at an instantaneous radius *r*:  

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?F=qvB=\frac{mv^{2}}{r}" />
</p>

The time necessary for a semicircular orbit is:  

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?t=%5Cfrac%7B%5Cpi%20r%7D%7Bv%7D=%5Cfrac%7B%5Cpi%20m%7D%7BqB%7D" />
</p>

The frequency of the AC voltage is:  

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?%5Cnu=%5Cfrac%7B1%7D%7B2t%7D=%5Cfrac%7BqB%7D%7B2%5Cpi%20m%7D" />
</p>

This is often called the **cyclotron frequency** or **cyclotron resonance frequency** for a particle of charge *q* and mass *m* moving in a uniform field *B*. Here, ν and B are intimately linked—for a given field strength, the frequency can only take one value for resonance.  

The velocity increases gradually as the particle spirals outward, reaching its maximum value at the largest radius *R*:  

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?v_{\text{max}}=\frac{qBR}{m}" />
</p>

which leads to a maximum kinetic energy:  

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?T=\tfrac{1}{2}mv_{\text{max}}^{2}=\frac{q^{2}B^{2}R^{2}}{2m}" />
</p>

For **charged particle induced nuclear reactions** (as done in a cyclotron), the expected activity produced in an irradiation is given by the production equation:

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?A(t)=N_0\cdot\sigma\cdot%20I\cdot\left(1-e^{-\lambda\cdot%20t_{\text{irrad}}}\right)" />
</p>

where:  
- **A(t)** – activity produced (Bq)  
- **λ** – decay constant (s⁻¹)  
- **t<sub>irrad</sub>** – irradiation length (s)  
- **σ** – reaction cross section (cm²)  
- **N₀** – atomic areal density of target material (atoms/cm²)  
  - Determined from *target mass, density, thickness, and molecular weight*  
- **I** – projectile intensity (particles/s)  
  - Calculated from the beam current (µA) using the charge per particle and the conversion factor 6.24 × 10¹⁸ charges/coulomb  


Activity is defined as the number of nuclear decays per unit time (1 Bq = 1 decay/second). Pulse-mode detectors are instruments designed to register each individual quantum of radiation interacting with the detector. A spectrometer is a specialized type of pulse-mode detector that also measures the energy of each quantum, producing a radiation energy spectrum as its output. To determine the activity of a multi-radionuclide sample, a spectrometer can be used to measure the net counts within energy peaks associated with specific radionuclides, from which the corresponding activities can be calculated.

<p align="center">
  <img src="example_outputs/peak_fit_plots/120-Min-Decay-Report-d1s200-000.Spe-peak-fit.svg" alt="Example HPGe Gamma Spectrum" width="1000"/>
  <br/>
  <em>Example HPGe gamma spectrum with fitted peaks.</em>
</p>

Most nuclear reactions leave the final nucleus in an excited state. These excited states decay rapidly to the ground through through the emission of one or more γ-rays. The energy of the γ-rays is charecteristic of the energy difference between nuclear states. 

Consider the decay of a nucleus of mass M at rest from an intial excited state Eᵢ to a final state E𝒻.

To conserve linear momentum, the final nucleus will not be at rest but must have a recoil momentum p<sub>R</sub> and corresponding recoil kinetic energy T<sub>R</sub>, which we assume to be nonrelativistic.

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?T_R=\frac{p_R^2}{2M}" />
</p>

Conservation of total energy and momentum give,

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?E_i=E_f+E_\gamma+T_R" /><br/>
  <img src="https://latex.codecogs.com/svg.latex?0=p_R+p_\gamma" />
</p>

The nucleus recoils with momentum equal and opposite to that of the gamma ray.

Defining,

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?\Delta%20E\equiv%20E_i-E_f" />
</p>

And using relative relationship,

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?E_\gamma=c\,p_\gamma" />
</p>

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?\Delta%20E=E_\gamma+\frac{E_\gamma^2}{2Mc^2}" />
</p>

Which has the solution,

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?E_\gamma=Mc^2\left[-1\pm\sqrt{1+\frac{2\Delta%20E}{Mc^2}}\right]" />
</p>

The energy differences of the nucleus are typically of the order of MeV, which the rest energies are of order A×10³ eV, where A is the mass number.

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?\Delta%20E\ll%20Mc^2" />
</p>

To a precision of the order 10⁻⁴ to 10⁻⁵ we keep only the first three terms in the expansion of the square root.

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?E_\gamma\approx\Delta%20E-\frac{(\Delta%20E)^2}{2Mc^2}" />
</p>

The actual γ-ray energy is thus diminished somewhat from the maximum available decay energy. Recoil correction to the energy is generally cosidered negligible amounting to a 10⁻⁵ correction that is usually far smaller than expeiremental uncerainty. The Mossbauer effect is one circumstance in which recoil plays an important role.

In this work we assume,

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?E_\gamma\approx\Delta%20E" />
</p>

For low energy γ-rays, recoil energy is less than 1 eV and has negligible effect. High-energy γ-rays (5–10 MeV radiation emitted following neutron capture) gives recoils in the range of 100 eV, which may be sufficient to drive the recoiling atom from its position in a solid lattice ("radiation damage").

---

Uncharged radiations such as gamma rays or neutrons must first undergo interaction in the detector before detection is possible. Because these radiations can travel large distances between interactions, detectors are often less that 100% efficient. A precise determination of the detector efficiency is therefore required to relate the number of pulses recorded to the number of neutrons or gamma rays emitted by the source. 

For a given γ-peak in the spectrum, the observed counts can be expressed as:

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?\text{counts}=\text{decays}\times\epsilon_{\text{abs}}\times%20I_\gamma" />
</p>

where:  
- **decays** – the total number of nuclear decays in the sample for the radionuclide emitting the γ-line  
- **I<sub>γ</sub>** – the emission probability (branching ratio) that the radionuclide decay produces the specific γ-ray of interest  
- **ϵ<sub>abs</sub>** – the absolute detector efficiency at the γ-ray energy of interest  

The **nuclab** `Calibration` class is used to determine absolute detector efficiencies. These depend not only on intrinsic detector properties but also on the experimental counting geometry. Formally, the absolute efficiency is defined as:

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?\epsilon_{\text{abs}}=\frac{\text{number%20of%20pulses%20recorded}}{\text{number%20of%20radiation%20quanta%20emitted%20by%20source}}" />
</p>

Over the course of a measurement, the activity of a radioactive source decreases exponentially:

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?A(t)=A_0e^{-\lambda%20t}" />
</p>

To obtain the total number of decays during a measurement, the activity curve is integrated over time (*units check: Bq × s = decays/s × s = decays*):

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?\int_{t_1}^{t_2}A(t)\,dt=\int_{t_1}^{t_2}A_0e^{-\lambda%20t}\,dt=\frac{-A_0}{\lambda}e^{-\lambda%20t}\Big|_{t_1}^{t_2}=\frac{A_0}{\lambda}(e^{-\lambda%20t_1}-e^{-\lambda%20t_2})" />
</p>

For the special case where the measurement starts at *t₁ = 0*:

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?\int_{0}^{t_2}A(t)\,dt=\frac{A_0}{\lambda}(1-e^{-\lambda%20t_2})" />
</p>

Relating the number of decays to the recorded counts gives:

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?\frac{\text{counts}}{\epsilon%20I_\gamma}=\frac{A_0}{\lambda}(1-e^{-\lambda%20t_2})" />
</p>

Solving for the initial activity *A₀* (i.e., the activity at the start of the measurement):

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?A_0=\frac{\text{counts}\cdot\lambda}{\epsilon%20I_\gamma\,(1-e^{-\lambda%20t_2})}" />
</p>

This formulation is important because it accounts for the decay of radioactive material during the measurement interval. In contrast, the general counts relation:

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?\text{counts}=\text{decays}\cdot\epsilon%20I_\gamma" />
</p>

does not incorporate the time-dependent decrease in activity.


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
