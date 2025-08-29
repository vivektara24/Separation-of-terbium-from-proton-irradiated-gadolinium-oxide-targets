from nuclab.utils import *
from pathlib import Path
from typing import Mapping, Iterable, Optional
import re

class Yield:
    '''
    Performs theoretical end-of-bombardment (EoB) activity yield calculations for accelerator based production of solid targets.

    Parameters
    ----------
    E0 : float
        Initial energy of the incident ion on the front face of the target material (MeV).
    srim_energies, srim_ranges : list[float]
        Paired SRIM data - energies (MeV) and their corresponding projected ranges (cm) for the incident ion in the target material.
    target_thickness : float
        Dimension of target in the direction parallel to particle beam (cm).
    dE : float
        Slice thickness in energy (MeV) used for target decomposition.
    density : float
        Density of the target material (g/cm3).
    moleuclar_weight : float
        Molecular weight of the target material.
    projectile_intensity : pandas.DataFrame
        Rate of particles incident on the target (particles/second).
    t_irrd: float
        The length of the irradiation time (s)
    
    Attributes
    ----------
    reactions: dict[str, dict]
        Mapping from isotope to its reaction data. Populate this attribute
        using `log_reactions_from_csvs`, which constructs the dictionary from
        cross-section (xs) data files.
        
    '''

    def __init__(self, E0: float = None, srim_energies: list = None, srim_ranges: float = None, target_thickness: float = None,
                 dE: float = None, density: float = None, molecular_weight: float = None,
                   projectile_intensity: float = None, t_irrad: float = None, reactions: dict[str, dict] | None = None):

        self.E0 = E0
        self.srim_energies = srim_energies
        self.srim_ranges = srim_ranges
        self.target_thickness = target_thickness
        self.dE = dE
        self.density = density
        self.molecular_weight = molecular_weight
        self.projectile_intensity = projectile_intensity
        self.t_irrad = t_irrad
        self.reactions = reactions or {}


        self.results: dict[str, dict] = {}


    def break_target_into_slices(self):
        """
        Decompose the target into thin slices based on energy loss.


        The funciton iterativley divides the target into slices defined by dE.
        Each slice has a physical thickness (cm) corresponding to an energy 
        loss of dE MeV, enabling energy-depth mapping across the entire 
        target thickness.

        Returns:
            slices : list[float]
                Thickness of each slice (cm)
            energies: list[float]
                Proton energy (MeV) at the entrance of each slice
        """
        current_energy = self.E0
        remaining_thickness = self.target_thickness
        slices = []
        energies = []

        while current_energy > 0 and remaining_thickness > 0:
            # Interpolate to find the projected range at the current energy
            range_at_current_energy = linear_interpolation(self.srim_energies, self.srim_ranges, current_energy, mode='y')

            # Determine the next energy step
            next_energy = max(current_energy - self.dE, 0)

            # Interpolate to find the projected range at the next energy
            range_at_next_energy = linear_interpolation(self.srim_energies, self.srim_ranges, next_energy, mode='y')

            # Compute the required slice thickness
            slice_thickness = range_at_current_energy - range_at_next_energy

            if slice_thickness <= 0:
                break  # Stop if we get a non-physical thickness

            # Ensure we do not exceed the target thickness
            if slice_thickness > remaining_thickness:
                slice_thickness = remaining_thickness

            slices.append(slice_thickness)
            energies.append(current_energy)

            remaining_thickness -= slice_thickness
            current_energy = next_energy  # Move to the next energy step

        return slices, energies




    def compute_areal_density(self, slice_thicknesses):
        """
        Computes the areal density for each slice of the decomposed target.

        Parameters
        """
        areal_densities = [(self.density * t) / self.molecular_weight * 6.022 * 10 ** 23 * 2 for t in slice_thicknesses]
        return areal_densities

    def interpolate_cross_sections(self, slice_energies, energy_vals, cross_section_vals):
        """
        Interpolates the cross-section values at each slice energy using linear interpolation.

        Parameters
        ----------
        slice_thicknesses : list[float]
            Thickness of each slice (cm).

        Returns
        -------
        list[float]
            Areal density of each slice (g/cm²).
        """
        interpolated_cross_sections = [
            linear_interpolation(energy_vals, cross_section_vals, E, mode='y') for E in slice_energies
        ]
        return interpolated_cross_sections

    def calculate_slice_activities(self, N_list, sigma_list, I, half_life, t):
        """
        Calculate the activity produced in each slice of the decomposed target

        Parameters
        ----------
        N_list : list[float]
            Atomic areal densities of each slice (atoms/cm²).
        sigma_list : list[float]
            Reaction cross-sections for each slice (cm²).
        I : float
            Projectile intensity (particles/s).
        half_life : float
            Half-life of the product nuclide (s).
        t : float
            Irradiation duration (s).

        Returns
        -------
        list[float]
            Activity produced in each slice (Bq).
        """
        # Convert half-life to decay constant
        lambda_ = np.log(2) / half_life

        # Compute activity for each slice
        activities = [N * sigma * I * (1 - np.exp(-lambda_ * t)) for N, sigma in zip(N_list, sigma_list)]

        return activities
    

    def load_reactions_from_csvs(
        self,
        directory: str | Path,
        isotope_half_lives: Mapping[str, float],
        filename_glob: str = "*.csv",
        energy_col: int | str = 0,
        xs_col: int | str = 1,
        xs_units: str = "mb",
        dropna: bool = True,
        encoding: Optional[str] = None,
    ) -> dict[str, dict]:
        """
        Populate self.reactions from CSV files in `directory`.

        Expected CSV content:
          - First column = incident energy (MeV)  [or use `energy_col` by name]
          - Second column = cross section (xs_units)  [or use `xs_col` by name]

        Filename parsing:
          - Isotope is inferred from the filename (last alphanumeric token before '.csv'),
            e.g., 'NatGd_P_X_154m1Tb.csv' -> '154m1Tb'.
          - You can override the glob via `filename_glob`.

        Args:
            directory: Folder containing cross-section CSVs.
            isotope_half_lives: Mapping isotope -> half-life in seconds (e.g., {"154Tb": 21.5*3600}).
            filename_glob: Pattern to match files (default "*.csv").
            energy_col: Column index or name for energy.
            xs_col: Column index or name for cross section.
            xs_units: Units of cross section in the CSVs: "b", "mb", "ub", "nb", or "pb".
            dropna: Whether to drop rows with NaNs in selected columns.
            encoding: Optional file encoding for pandas.

        Returns:
            The constructed reactions dict and also sets self.reactions.

        Notes:
            Cross sections are converted to m^2 using:
              1 barn = 1e-28 m^2
        """
        directory = Path(directory)
        if not directory.is_dir():
            raise NotADirectoryError(f"{directory} is not a valid directory.")

        # barn -> cm^2 conversion factors
        barn = 1e-24  # 1 barn = 1e-24 cm^2
        unit_map = {
            "b": barn,
            "mb": 1e-3 * barn,   # millibarn
            "ub": 1e-6 * barn,   # microbarn
            "µb": 1e-6 * barn,   # microbarn (unicode mu)
            "nb": 1e-9 * barn,   # nanobarn
            "pb": 1e-12 * barn,  # picobarn
        }
        xs_units_lc = xs_units.lower()
        if xs_units_lc not in unit_map:
            raise ValueError(f"Unsupported xs_units='{xs_units}'. Use one of {list(unit_map.keys())}.")

        reactions: dict[str, dict] = {}
        files: Iterable[Path] = directory.glob(filename_glob)

        # Helper to extract isotope name from filename
        def infer_isotope_name(p: Path) -> str:
            # Grab last token of the stem separated by underscores OR fallback to alnum run
            stem = p.stem
            if "_" in stem:
                candidate = stem.split("_")[-1]
            else:
                # last alnum run
                m = re.findall(r"[A-Za-z0-9]+", stem)
                candidate = m[-1] if m else stem
            return candidate

        for csv_path in files:
            try:
                df = pd.read_csv(csv_path, encoding=encoding)
            except Exception as e:
                print(f"[load_reactions_from_csvs] Skipping {csv_path.name}: read error -> {e}")
                continue

            # Select columns
            try:
                energy_series = df.iloc[:, energy_col] if isinstance(energy_col, int) else df[energy_col]
                xs_series = df.iloc[:, xs_col] if isinstance(xs_col, int) else df[xs_col]
            except Exception as e:
                print(f"[load_reactions_from_csvs] Skipping {csv_path.name}: column selection error -> {e}")
                continue

            data = pd.DataFrame({"E": energy_series, "XS": xs_series})
            if dropna:
                data = data.dropna(subset=["E", "XS"])

            if data.empty:
                print(f"[load_reactions_from_csvs] Skipping {csv_path.name}: no valid rows after cleaning.")
                continue

            # Convert cross section units to m^2
            data["XS_m2"] = data["XS"] * unit_map[xs_units_lc]

            isotope = infer_isotope_name(csv_path)
            if isotope not in isotope_half_lives:
                print(f"[load_reactions_from_csvs] Warning: no half-life for '{isotope}'. Skipping file {csv_path.name}.")
                continue

            reactions[isotope] = {
                "cross_section_energy_vals": data["E"].astype(float).tolist(),
                "cross_section_vals": data["XS_m2"].astype(float).tolist(),
                "half_life": float(isotope_half_lives[isotope]),
            }

        if not reactions:
            raise ValueError(f"No reactions could be loaded from {directory} with pattern '{filename_glob}'.")

        self.reactions = reactions
        return reactions



    def compute_activities_for_multiple_isotopes(self):
        """
        Compute activities for multiple isotopes produced in a target.

        The function first performs energy-depth mapping of the incident ion across
        the target material using `break_target_into_slices`. For each of the produced
        isotopes, the activit in each slice is calculated using:
            - Slice specific entrance energies
            - Slice specific atomic areal densities
            - Slice specific interpolated cross-sections

        Total activity for each isotope is calculated as the sum of the contrubutions 
        from all slices in the target material.

        Returns
        -------
        dict[str, dict]
            Mapping from isotope name to its computed data, including:
                - "slice_thicknesses" : list[float]
                    Thickness of each slice (cm).
                - "areal_densities" : list[float]
                    Atomic areal density of each slice (atoms/cm²).
                - "cross_sections" : list[float]
                    Interpolated cross-sections for each slice (cm²).
                - "activities" : list[float]
                    Activity produced in each slice (Bq).
                - "total_activity" : float
                    Sum of slice activities (Bq).
        """
        # Step 1: Break target into slices and get energies per slice
        slices, slice_energies = self.break_target_into_slices()

        # Compute atomic areal density for each slice using the TARGET material
        N_list = self.compute_areal_density(slices)

        # Store results for each isotope
        results = {}

        for isotope, data in self.reactions.items():
            cross_section_energy_vals = data['cross_section_energy_vals']
            cross_section_vals = data['cross_section_vals']
            half_life = data['half_life']

            # Step 2: Interpolate cross-section values for slice energies
            sigma_list = self.interpolate_cross_sections(slice_energies, cross_section_energy_vals, cross_section_vals)

            # Step 3: Compute activity for each slice
            activities = self.calculate_slice_activities(N_list, sigma_list, self.projectile_intensity, half_life, self.t_irrad)

            # Store results for this isotope
            results[isotope] = {
                "slice_thicknesses": slices,
                "areal_densities": N_list,
                "cross_sections": sigma_list,
                "activities": activities,
                "total_activity": sum(activities)  # Sum across slices
            }

            self.results = results

        return results
    

    def save_results_to_excel(self, filepath: str | Path = "isotope_results.xlsx", include_summary: bool = True) -> str:
        """
        Save computed isotope yields to an Excel workbook.

        For each isotope, a dedicated sheet is created with
        per-slice data:
            - Slice Thickness (cm)
            - Areal Density (atoms/cm²)
            - Cross Section (as provided)
            - Activity (Bq)
        Each sheet also contains a final totals row with the summed activity.
        
        
        Optionally, a "Summary" sheet is added, listing per isotope totals
        (in Bq and uCi) and the corresponding sheet name.

        Parameters
        ----------
        filepath : str or Path, optional
            Destination path for the Excel file (default = "isotope_results.xlsx").
        include_summary : bool, optional
            If True, include a summary sheet with per-isotope totals.

        Returns
        -------
        str
            Absolute path to the written Excel file.

        Raises
        ------
        ValueError
            If `self.results` is empty (i.e., no computed activities available).
        """
        
        if not self.results:
            raise ValueError("self.results is empty. Run compute_activities_for_multiple_isotopes() first.")

        out = Path(filepath)
        out.parent.mkdir(parents=True, exist_ok=True)

        def sanitize_sheet_name(name: str) -> str:
            bad = set(r'[]:*?/\\')
            cleaned = "".join("_" if ch in bad else ch for ch in str(name))
            return cleaned[:31]

        summary_rows = []

        with pd.ExcelWriter(out, engine="xlsxwriter") as writer:
            for isotope, data in self.results.items():
                df = pd.DataFrame({
                    "Slice Thickness (cm)": data["slice_thicknesses"],
                    "Areal Density (atoms/cm²)": data["areal_densities"],
                    "Cross Section": data["cross_sections"],
                    "Activity (Bq)": data["activities"],
                })

                total_bq = float(pd.Series(data["activities"]).sum())
                total_uCi = total_bq * 2.7027e-5

                totals_row = {
                    "Slice Thickness (cm)": "",
                    "Areal Density (atoms/cm²)": "",
                    "Cross Section": "TOTAL",
                    "Activity (Bq)": total_bq,
                }
                df_out = pd.concat([df, pd.DataFrame([totals_row])], ignore_index=True)

                sheet = sanitize_sheet_name(isotope)
                df_out.to_excel(writer, sheet_name=sheet, index=False)

                if include_summary:
                    summary_rows.append({
                        "Isotope": isotope,
                        "Total Activity (Bq)": total_bq,
                        "Total Activity (µCi)": total_uCi,
                        "Sheet": sheet,
                    })

            if include_summary and summary_rows:
                pd.DataFrame(summary_rows).sort_values("Isotope").to_excel(
                    writer, sheet_name="Summary", index=False
                )

        return str(out.resolve())
    

    


    