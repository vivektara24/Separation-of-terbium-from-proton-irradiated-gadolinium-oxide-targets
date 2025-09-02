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




A detailed description with links of the contents of the repository are listed in the Table of Contents below.

## Table of Contents
- [Repository Contents](#repository-contents)
- [Setup Instructions](#setup-instructions)
- [Theory](#theory)
  - [Radiation Production](#radiation-production)
  - [γ-Decay](#γ-decay)
  - [Radiation Detection](#radiation-detection)
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

### Radiation Production
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

Conversions between the traditional curie (Ci) and the SI base unit (Bq) are shown below:

<p align="center">
  <b>1 Ci</b> = 3.7 × 10¹⁰ Bq<br/>
  <b>1 mCi</b> = 3.7 × 10⁷ Bq<br/>
  <b>1 µCi</b> = 3.7 × 10⁴ Bq
</p>


Stable nuclei may be transformed into radioactive species by bombardment with suitable particles, or photons at sufficiently high energy. Many radioactive isotopes are either absent in narture or diffucult to obtain, yet they can be produced.

For an efficient and effective disucussion of nuclear reactions, we must understand the notation or jargon that is widely used to describe them. Let us begin by considering one of the first nuclear reactions to be studied:

⁴He + ¹⁴N → ¹⁷O + ¹H + Q

Here an alpha particle reacts with a nitrogen nucleus-producing oxygen, a proton, and some energy, Q. Most nuclear reactions are studied by inducing a collision between two nuclei where the heavier reacting nucleus is at rest (the ``target`` nucleus) while the other nucleus (the ``projectile`` nucleus) is in motion, and this is called "normal kinematics". Such nuclear reactions might be described generally as:

Projectile (P) + Target (T) → Emitted Particle(s) (X) + Residual Nucleus (R) + Energy

A shorthand way to denote such reactions is, for the general case:

T(P, x)R

For the specific example discussed earlier:

¹⁴N(⁴He, p)¹⁷O

In a nuclear reaction moderated by the strong force in contrast to the weak force, there is conservation of the number of proton and neutrons (and thus the number of nucleons). There is also conservation of energy, momentum, angular momentum, and parity.

Consider the T(P, x)R reaction with only two products. Neglecting electron binding energies, we have, for the energy balance in the reaction,

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?m_Pc^{2}+m_Tc^{2}+T_P=m_Rc^{2}+m_xc^{2}+T_x" />
</p>

Note that since R and x may be complex nuclei, they could be formed in exctied states so that the values of m may be different than the ground state masses. The Q value of the reaction is defined as the difference in mass energies of the products and reactants, that is,

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?Q=(m_P+m_T-m_x-m_R)c^{2}=T_x+T_R-T_P" />
</p>

Note that if Q is positive the reaction is exoergic, while if Q is negative, the reaction is endoergic. Note that a necessary but not sufficient condition fo the occurrence of a nuclear reactions is that

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?Q+T_P>0" />
</p>

i.e for an endoergic process the decrease in the mass energies from reactants to products must be compensated for by the kinetic energy of the projectile.

If the masses of both the products and reactants are known, the Q-value can be calculated using mass excesses as

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?Q=\Delta_{\text{projectile}}+\Delta_{\text{target}}-\sum\Delta_{\text{products}}" />
</p>

If there are only two products in a so-called-two body reaction, we can show using conservation of momentum, that only <img src="https://latex.codecogs.com/svg.latex?T_x" /> and the angle <img src="https://latex.codecogs.com/svg.latex?\theta" /> of particle x with repsect to the direction of motion of P suffice to determine Q. The proof is rather long so I leave you the final result, the _Q-value equation_:

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?Q=T_x\left(1-\frac{m_x}{m_R}\right)-T_P\left(1-\frac{m_P}{m_R}\right)-\frac{2}{m_R}\sqrt{m_P\,T_P\,m_x\,T_x}\cos(\theta)" />
</p>

What does the Q-value equation say? Is says that if we measure the kinetic energy of the emitted particle x and angle at which it is emitted in a two-body reaction and we know the identiies of the reactants and products of the reactions, that we can determine the Q value of the reaction. In short, we can measure the energy relesase for any two-body reaction by mesureing the properties of one of the products.

For additional insight, let us now consider the same reaction as described in the center of mass (CM) reference frame. In the CM system the total momentum of the particles is zero, before and after the collision. The kinetic energy carried in by the projectile, <img src="https://latex.codecogs.com/svg.latex?T_{\text{Lab}}" />, is not fully avaialbe to be dissipated in the reaction, an amount, T_CM, must be carried away by the motion of the CM. Thus, the available energy to be used (dissipated) in the collision is only T_lab - T_CM = T_0 = [m_T/(M_T+mP)]T_Lab. The energy avalailabe for the nuclear reactions is Q + T_0. To make an endothermic reaction go, the sum Q + T_0 must be >= 0. Rearranging a few terms in the equation, the condition for having the reaction occur is that

T_p >= -Q(m_p + m_t)/m_T

This minimum kinetic energy that the projectile must have to make the reaction go forward is called the threshold energy for the reaction.


That is to say there are spontaneously decaying radisotopes that are not naturally occuring or difficult to obtain naturally, the spontenous decay of a radioisotope is one kind of nuclear reaction, defined by a change in the nuclear state? of a radioisotope. An additional type of nuclear reaction is acheived by accelerating a charged particle or by subjecting to regions of high thermal flux neutrons, and absorbiion a high energy gammas into a nucleus which leaves the nucleus in the compound state, the compound state emitts a gamma or neutorn or proton or alpha or spallation can occur of fission, which leaves behind an excited daugher isotope, this isotope can be radiactve istelf therefore by incucing a nuclear reaction you produce another radiosotipe that spontaeously udergoes anohter nuclear reaction.


The purpose of an accelerator of charged particles is to direct against a target a beam of a specific kind of particles of a chosen energy. Low energy accelerators are used to produce beams in the 10-100-MeV range, often for reaction or scattering studies to elucidate the structure of specific final states, perhaps even individual excited states. These accelerators should have accurate energy selection and reasonably high currents because the ultimate precision of many expirments is limited by counting statistics.

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

Radioactive nuclei, either natural or artificially produced by nuclear reactions, are unstable and tend to seek more stable configurations through expulsion of energetic particles, including one or more of the following,* where corresponding changes in the atomic number (Z) and number of nucleons (A) are indicated:

| Emission Type   | ΔZ  | ΔA  |
|-----------------|-----|-----|
| α-particle      | -2  | -4  |
| β⁻-particle     | +1  | 0   |
| β⁺-particle     | -1  | 0   |
| γ-ray           | 0   | 0   |

Some radionuclides decay by more than one mode.

γ-Decay
---

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

Radiation Detection
---
Uncharged radiations such as gamma rays or neutrons must first undergo interaction in the detector before detection is possible. Because these radiations can travel large distances between interactions, detectors are often less that 100% efficient. A precise determination of the detector efficiency is therefore required to relate the number of pulses recorded to the number of neutrons or gamma rays emitted by the source. 



For a given γ-peak in the spectrum, the observed counts can be expressed as:

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?\text{counts}=\text{decays}\times\epsilon_{\text{abs}}\times%20I_\gamma" />
</p>

where:  
- **decays** – the total number of nuclear decays in the sample for the radionuclide emitting the γ-line  
- **I<sub>γ</sub>** – the emission probability that the radionuclide decay produces the specific γ-ray of interest  
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

Activation Analysis
---

Activation analysis (AA) is an analytical technique that allows one to determine that amount of a given element X contained in some material Y. The basic steps in the activation technique are as follows:

- Irradiate Y with a source of ionizing radiation so that some generally very small amount of X will change into X*, a radioactive isotope of X.
- Using chemical or instrumental technqiues, "isolate" X and X* from all other elements is Y (not necessarily quantitatively) and measure the activity of X*.
- Calculate the amount of X present.

But how does one calculate the amount of X present, knowing the activity of X* produced in the irradiation? Since the radiactivity was produced in a nuclear reaction, it can be shown that the activity A_X* as a function of time is 

A_X* = N_x * sigma * phi *(1 - exp(-lamdaX*t_i))exp(-lamdaX*t_d)

Where N_X is the number of X nuclei present initialy, t_i is the length of the irradiation, and t_d is the time of decay after the end of an irrdiation. From this equation one could calcualte Nx from Ax. This equation for Ax is only valid for "thin targets", that is, samples that absorv <5% of the flux of activitng particles.)

This method of analyisis is called absolute activation analysis and is rarley done. The reasons for this are the need for detailed knowldge of the flux and energy of the bombarding particles in the sample and the comppound of the nuclear unceratinties such asthe cross sections, decay branching ratios, and so on in the final results. A simpler technique is to irradiate and count a known amount of pure X under the same conditions used for the mixute of X in Y. Then,

Mass of X in Y = (Known mass X)(Acitivty of X* in Y / Activity of X* in pure X)

Which is known as the comparator technqiue and is the most widely used method of AA. The method only depends on irrdiating and counting standards known amounts of pure material using the same conditions as the samples being analyzed.

Numerous tests have shown that with careful experimental manipuation, AA is an accurate (~1% accuracy) and precise (~5% precision) method of measuring elemental concentrations.


Nuclear Medicine
---
The most rapidly expanding area of radionuclide use is in **nuclear medicine**. Nuclear medicine deals withteh use of radiation and radioactivity to diagnose and treat disease.

<p align="center">
  <img src="images/blog-isotopes-hr.jpg" alt="Example HPGe Gamma Spectrum" width="500"/>
  <br/>
  <em>Dramatic tumor regression following ²²⁵Ac-PSMA therapy.</em>
</p>

The two principal areas of endeavor, **diagnosis** and **therapy**, involve different methods and considerations for radioactivity use. Recent work in this area has focused on developing combinations of two isotopes in one delivery system: one isotope provides a therapy function and another isotope provides a diagnostic function, called **theranostics**.

In diagnosis (imaging) emitted radiation from injected radionuclides is detected by special detectors (cameras) to give images of the body. In therapy, radionuclides are injected into the body and concentrated in the organ of choice and damage the tissue. Nuclear medicine combines nuclear and radiochemistry, pharmacy medicine, and radiation biology.

Radiopharmaceuticals are radioactive compounds used for diagnosis and therapy. Most (95%) radiopharmaceuticals are presently used for diagnosis. A radiopharmaceutical generally has two parts, the radionuclide and the pharmaceutical. The pharmaceutical component allows the compound to preferentially locate in organs or to particpate in some function of the organ. The radiation from the nuclide must be easily detected and lead to a controlled dose to the patient. The effective half-life of the radionuclide in the target organ or the body should be short to minimize unnecessary radiation exposure. Radiopharmecuticals should involve γ-emitting radionuclides, while those intended for therapy will involve α or β⁻ emitters. Therapy with α emitters is used for small tumors due to the short range of the α-particles in matter, while the β⁻ emitters are used with larger tumors.

<p align="center">
  <img src="images/radiopharmaceuticals-diagram.jpg" alt="Example HPGe Gamma Spectrum" width="500"/>
  <br/>
  <em>Molecular structure of a radiopharmaceutical.</em>
</p>


Additionally the Auger effect has been explored as a potential source for targeted radiotherapy. The Auger effects is based on the emission of a low energy inner-shell electron (typically <25 keV) from an atom post electron caputre (EC), internal conversion (IC), or incident X-ray excitation. The phenomenon can induce an Auger cascade, where the intial emission of a primary electron is followed by sequential relaxation process that release multiple low-energy electrons in close proximity to the emission site (2-500nm). The short range of the emitted Auger cascade results in medium-high levels of linear energy transfer (4-26 keV/μm) exerted on the surrounding tissue. This property makes Auger emitters the ideal candidates for delivering high levels of targeted radiation to a specific target with dimensions comparable to, for example, the DNA.

<p align="center">
  <img src="images/auger_effect.jpg" alt="Example HPGe Gamma Spectrum" width="500"/>
  <br/>
  <em>Diagram Explaining the Auger Effect.</em>
</p>


## Low Key Bugs in the Code
1. There are currently no warning messages if required class attributes arent filled before calling the functions, Instead the output will simply be incomplete.

## References

- Glenn F. Knoll. Radiation Detection and Measurement. 4th edition, Wiley, 2010 (ISBN
978-0-470-13148-0)

- Frank Herb Attix. Introduction to Radiological Physics and Dosimetry, John Wiley & Sons,
Inc. 1986 or reprinted in 2004 Wiley VCH

- Loveland, W. D., Morrissey, D. J., & Seaborg, G. T. (2017). Modern nuclear chemistry. https://doi.org/10.1002/9781119348450

- Krane, K. S., & Lynch, W. G. (1989). Introductory Nuclear Physics. Physics Today, 42(1), 78. https://doi.org/10.1063/1.2810884

## Useful Links

- [Packaging Python Projects (official tutorial)](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

## Real Talk

In our method we cailibrate an hpge detector by using calibration sources of a very well defined activity. Because we know the activity we may clearly establish the number of decays of each source for a given measurment time. We know that for each decay there are certain gammas that are emitted in a charecterized probablistic manner (# emissions of certain energy / # decays of certain isotopes), therefore we can clearly establish the number of gammas of certain energies that should be emitted by the calibration sources (especially for long measuremnt times). A fraction of the gammas truly emitted by the calibration sources are detected. Additionally coincidence summing may occur. Although coincendence summing was minimized by placing the sample 200cm from the face of the detector, coincidence summing may reduce the observed number of counts detected at certain peak energies, reducing the determined activities if those gammas are being analyzed. Each of these effects is incorporated into a single detector efficiency metric by simply measuring a known number of gammas across the energy spectrum for 24hr, looking at the number of counts detected at each energy, and taking the ratio of those number. This value is energy dependent so a function, whose form is a mystery to me, is fit to the data (CPS/Bq = # of counts detected in time interval / measurment time / # known number of decays in time interval).

We then detect the number of counts across the energy spectrum of a natGd2O3 sample that had been irradiated at 12.6 MeV for 30mins in a low-energy cyclotron tailored for 18F production, producing many radioactive terbium isotopes. Once again, knowing certain gammas are emitted in a charecterized probablistic manner by the Tb isotopes, we can determine the activity of each that had been produced in the irradition, by using the previously determined detector efficiencies at the know Tb gamma energies. We repeat this process at 2h intervals ~10hr post irradiation, correcting for sample decay during the measurment. We fit an exponential decay function to the measured activites across the serial measurments floating the end-of-bombardment (eob) activity and half-lifes of the Tb isotpes using the ``Serial`` class. Additionally we decay correct the start of measurment activites determined each measurment to eob and take the average.

156Tb has 2 metastable states that grow into the ground state with ~24hr and ~5hr have lives. In addition to the 2hr measurments, repeated 5 and 10 minute interval measurments were recorded ~1hr post eob. Adding this data to the decay analysis of 156Tb allowed us to see the growth in of the metastable states to the ground state. We fit the bateman equation to the decay to determine eob activities and half-lives for each of the isomers. We attempted to repeat this process to charecterize the isomers of 154Tb, but the growth in was observed to be neglible.

We compare the expirmentally determined activities to expected yields calculated using the production equation. To account for charged particle attenuation in the target material, we decomposed the target material into thin slices of 1 keV using stopping power values from SRIM. This allows us to have a beter estimatation of the proton beam energy at different thicknesses within the target material, enabling per slice energy dependent cross sections to be used. The total activity is simply the sum of the activites produced in each slice.

``But I'm not a rapper``

``You know what I mean?``

## Failed Proton Activation Analysis

Question: why does it matter if the Gd is in Gd2O3 or a nitrate form?

The 5- and 10-minute interval measurments taken ~1hr post eob described above were intially taken with the intention of assessing the elemental composition of the natGd2O3 post recycling by performing an activation analysis.

After going through through the radiochemical seperation process, ~95% of the Gd is recovered in the first 4 rinse fractions (~40mL 0.2M HNO3) if the first LN2 column. The fractions are dried down, leaving behind Gd(NO3)3 * XH2O salf. To recover Gd2O3 from the salt we implement the denitration paper described in the accanpying work, informed by the chemical process impelmeneted in Non-isothermal kinetics of the thermal decomposition of gadolinium nitrate. We attempted to quantify the number of 14N atoms in a target made from recycled materials, by measuring the amount of 11C that was created in the 14N(p, alpha)11C reaction. The issue with this is that the 16O present in Gd2O3 undergoes the 16O(p, alpha)13N reaction too. Both 11C and 13N only have 511 keV gamma emissions from B+ decay followed by positron emmision. To further complicate things they have relatively similar half-lives 20.34mins and 9.967 min respecivley. Additionally they are not the only B+ emitting radionuclides that were created, 152Tb, 153Tb, 154Tb, 156Tb, and 158Tb is also a positron emitting radionuclied, although the half-life are of these isotopes are large in compartison with 11C and 13C.

However we tried to fit a sum of two exponential decays to the decay of the 511keV peak over the course of the repeated 5- and 10-minute measurments, floating only the intilal activities and fixing the half-lives to what we know them to be for 11C, 13N. The 14N/16O ratio was determined to be 0.30682.


Although it was a bad idea to try this with the 511 keV peak, it serves as an example of how one can perform quality control of a chemical process by irrdiating a . 


by determing the start of measurment time activity through a mucerail implementaiton of an analytical solution of an exponential decay initial value problem prooved in this repository.

## Final Steps Before Posting
- reread, format everything correcly, adjust what needs to be adjusted
- Make sure results xlsx's are properly linked
- Add ``terbinator/`` repository w/ abstract, poster. Add images of the terbinator to the front page
- radiochemistry topics i can discuss: Aparent molar activity, chromatography, extraction chromatograpy, LN2 resin, DGA resin, Lathanide seperation chemistry?, limits of detection, MPAES, specific and molar activity, distribution ratio
- Phospohr imaging thing
- mass excess, mass energy, binding energy per nucleon, decay energy (Q value?), seperation energy, definition of an AMU, Beta decay
- Interaction of radiaion with matter (probably just em radiation, i.e photelectirc vs compoton vs pair produciton) (atix), Bethe equaiton, bragg curve, (knoll)
- Fission, spallation
- SRIM/stopping power
- semiconductor physics and general detector properties
- causes of detector inefficinecies
- exposure vs dose vs kerma
- ionizing radation chapter attix, charged particle equilibirum, 
- Tb as a theranostic isotope, why are Tb isotopes important?
- Lack of enriched 160Gd, implications for 161Tb production
- counting statstics
- we use a giger meuller counter, a CsI(Tl) scintiallation detector, general modes of operation of these detectors
- Multichannel pulse analysis, pulse processing and shaping
- overview of Germainum detectors
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
