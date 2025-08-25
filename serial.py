import os

import curie as ci
from nuclear_physics_utils import *

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Callable, Optional, Dict

from pathlib import Path

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Serial:

    """
    Pipeline for serial HPGe y-spectra analysis

    The class automates the analysis of serial HPGe measurements using
    user-defined y-lines. Per y-line end-of-bombardment (EoB) activites
    and half-lives are returned. Exponential decay-curves can be saved to
    a user-specified directory. For additional information on methods see
    supplementary information of "".

    Attributes
    ----------

    data_directory : str
        Path to the directory containing `.Spe` spectrum files. Files must follow
        the expected naming convention.
    efficiency_fit_params : list
        Parameters passed to the efficiency function used during spectrum analysis, 
        e.g., coefficients of an empirical efficiency curve.
    detector_eff_uncertainty : float
        Fractional uncertainty (e.g., 0.05 for 5%) associated with the detector efficiency.
    eob_time : datetime
        End-of-bombardment timestamp used to compute decay times for each spectrum.
    gammas : pandas.DataFrame
        Table of gamma lines used for peak fitting. Must include columns such as 
        ``["energy", "intensity", "unc_intensity", "isotope"]`` with energies in keV.
    half_lives : dict of float to float
        Mapping from gamma energy (keV) to half-life (s).
    peak_data : pandas.DataFrame
        Fitted peak data from processed spectra w/ metadata.
    decay_results : pandas.DataFrame
        Per-(isotope, energy) summary of results.
    """

    def __init__(self, data_directory: str = None, efficiency_fit_params: list = None, detector_eff_uncertianty: float = None,
                 eob_time: datetime =None, gammas: pd.DataFrame = None, half_lives: dict[float, float] = None):
        
        """
        Initialize the Serial analysis pipeline.

        Parameters
        ----------
        data_directory : str
            Path to the directory containing `.Spe` spectrum files. Files must follow
            the expected naming convention.
        efficiency_fit_params : list
            Parameters passed to the efficiency function used during spectrum analysis, 
            e.g., coefficients of an empirical efficiency curve.
        detector_eff_uncertainty : float
            Fractional uncertainty (e.g., 0.05 for 5%) associated with the detector efficiency.
        eob_time : datetime
            End-of-bombardment timestamp used to compute decay times for each spectrum.
        gammas : pandas.DataFrame
            Table of gamma lines used for peak fitting. Must include columns such as 
            ``["energy", "intensity", "unc_intensity", "isotope"]`` with energies in keV.
        half_lives : dict of float to float
            Mapping from gamma energy (keV) to half-life (s).
        """
        
        self.data_directory = data_directory
        self.efficiency_fit_params = efficiency_fit_params
        self.detector_eff_uncertainty = detector_eff_uncertianty
        self.eob_time = eob_time
        self.gammas = gammas
        self.half_lives = half_lives or {}
        self.peak_data = pd.DataFrame()     # accumulated enriched peaks
        self.decay_results = pd.DataFrame() # per-(isotope,energy) summary
    

    
    def process_spectrum_files(self, efficiency_func=None, plot_dir: str | None = None):
        """
        Process all `.Spe` spectrum files in the data directory.

        This method iterates over all `.Spe` files located in ``data_directory``,
        performs peak fitting using the CURIE `Spectrum` class, and calculates start of
        measurement activities and uncertainties. The processed peaks are mapped to metadata
        (e.g., detector slot, decay time, half-lives) concatenated across the measurments,
        and stored in ``self.peak_data``.

        Parameters
        ----------
        efficiency_func : callable
            A function to compute detector efficiency given gamma energy and efficiency 
            fit parameters. It should accept an array of energies and parameters 
            (e.g., `efficiency_func(energy, *params)`) and return an array of efficiencies.
            If None, detector efficiency is left as NaN and activities are not calculated.
        plot_dir : str, optional
            Directory where peak-fit plots can be saved. 
            Will be created if it does not exist. Default is None.

        Notes
        -----
        - Files without fitted peaks are skipped with a printed message.
        - If `efficiency_func` or `self.efficiency_fit_params` is missing, 
        detector efficiency and activity calculations are skipped.
        - Internal CURIE columns (e.g., ``decays``, ``chi2``) are dropped before returning.
        - The method does not perform any CSV/XLSX I/O; results are stored in memory.
        """


        Path(plot_dir).mkdir(parents=True, exist_ok=True)

        rows = []
        files = sorted([f for f in os.listdir(self.data_directory) if f.endswith(".Spe")])
        for file in files:
            file_path = os.path.join(self.data_directory, file)
            base_filename = os.path.splitext(file)[0]

            # Parse detector slot if present in name (e.g., '...-d1s12-...')
            detector_slot = None
            for part in base_filename.split("-"):
                if part.startswith("d1s") and part[3:].isdigit():
                    detector_slot = int(part[3:])
                    break

            sp = ci.Spectrum(file_path)

            # seconds since EOB
            decay_time = (sp.start_time - self.eob_time).total_seconds()

            # Fit peaks
            sp.fit_peaks(gammas=self.gammas)
            
            if plot_dir is not None:
                sp.saveas(f"{plot_dir}/{file}-peak-fit.svg")

            peaks = sp._peaks
            if peaks is None or len(peaks) == 0:
                print(f"No peaks found in {file}")
                continue

            # Work on a COPY, then append
            peaks = peaks.copy()

            # Add metadata/enriched columns (don’t touch self.peak_data inside loop)
            peaks["file"] = file
            peaks["detector_slot"] = detector_slot
            peaks["decay time (s)"] = decay_time
            peaks["half-life (s)"] = peaks["energy"].map(self.half_lives)

            # efficiency
            if efficiency_func is not None and self.efficiency_fit_params is not None:
                peaks["detector efficiency"] = efficiency_func(peaks["energy"], *self.efficiency_fit_params)
            else:
                # If not provided, keep NaN and avoid activity calc later for those rows
                peaks["detector efficiency"] = np.nan

            # Activity (only where we have what we need)
            need_cols = ["counts", "intensity", "live_time", "half-life (s)", "detector efficiency"]
            ok = peaks[need_cols].notna().all(axis=1)
            if ok.any():
                lam = np.log(2) / peaks.loc[ok, "half-life (s)"]
                denom = (1.0 - np.exp(-lam * peaks.loc[ok, "live_time"]))
                peaks.loc[ok, "activity"] = (
                    peaks.loc[ok, "counts"] * lam
                    / peaks.loc[ok, "detector efficiency"]
                    / peaks.loc[ok, "intensity"]
                    / denom
                )

                # Uncertainty on activity (propagation as in your formula)
                # Be sure these exist; if not, fill with NaN
                for c in ["unc_counts", "unc_intensity"]:
                    if c not in peaks.columns:
                        peaks[c] = np.nan

                term_counts = (lam * peaks.loc[ok, "unc_counts"]
                               / peaks.loc[ok, "detector efficiency"]
                               / peaks.loc[ok, "intensity"]
                               / denom) ** 2
                term_intensity = (peaks.loc[ok, "counts"] * lam * peaks.loc[ok, "unc_intensity"]
                                  / peaks.loc[ok, "detector efficiency"]
                                  / (peaks.loc[ok, "intensity"] ** 2)
                                  / denom) ** 2
                term_cal = (peaks.loc[ok, "counts"] * lam * self.detector_eff_uncertainty
                            / peaks.loc[ok, "detector efficiency"]
                            / peaks.loc[ok, "intensity"]
                            / denom) ** 2
                peaks.loc[ok, "uncertainty activity"] = np.sqrt(term_counts + term_intensity + term_cal)

                # EOB activity
                peaks.loc[ok, "eob activity"] = peaks.loc[ok, "activity"] * np.exp(
                    lam * peaks.loc[ok, "decay time (s)"]
                )
                peaks.loc[ok, "uncertainty eob activity"] = np.exp(
                    lam * peaks.loc[ok, "decay time (s)"]
                ) * peaks.loc[ok, "uncertainty activity"]

                # Log columns if you’ll use linearized fit later
                with np.errstate(divide="ignore", invalid="ignore"):
                    peaks.loc[ok, "ln(activity)"] = np.log(peaks.loc[ok, "activity"])
                    peaks.loc[ok, "uncertainty ln(activity)"] = (
                        peaks.loc[ok, "uncertainty activity"] / peaks.loc[ok, "activity"]
                    )

            # Drop CURIE internals you don’t want to keep (if present)
            drop_cols = ["efficiency", "unc_efficiency", "decays", "unc_decays",
                         "decay_rate", "unc_decay_rate", "filename", "chi2"]
            peaks = peaks.drop(columns=[c for c in drop_cols if c in peaks.columns], errors="ignore")

            rows.append(peaks)
            print(f"Finished fitting peaks for {file}")

        self.peak_data = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


    def process_decay_data(self, plot_directory: str | None = None):
        """
        Perform decay analysis on peak data grouped by (isotope, energy).

        This method groups the entries in ``self.peak_data`` by isotope and gamma
        energy, then fits the time-dependent activity data for each group to an
        exponential decay model. A nonlinear least-squares fit is performed on
        activity vs. time:

            A(t) = A0 * exp(-λ t)

        yielding estimates for the initial activity A0 and decay constant λ (and
        their standard uncertainties). The half-life is derived from λ.
        Optionally, diagnostic plots can be saved.

        In addition to the fitted A0, the method also computes the EOB (end-of-bombardment)
        activity statistics directly from the measured data. These are determined by
        taking the average of the decay-corrected activity values across all
        measurements for a gamma energy, along with their standard deviation and propagated
        uncertainty (based on the individual ``uncertainty eob activity`` values).

        The per-group fit results and summary statistics are stored in
        ``self.decay_results`` and returned as a DataFrame. No file I/O is
        performed except optional plot saving.

        Parameters
        ----------
        plot_directory : str or None, optional
            Path to a directory where activity-time fit plots will be saved for each
            (isotope, energy) group. If None (default), no plots are saved. If
            provided, the directory is created if it does not exist.


        Raises
        ------
        ValueError
            If ``self.peak_data`` is empty.
        KeyError
            If required columns are missing from ``self.peak_data``. Required columns:
            ``["isotope", "energy", "decay time (s)", "activity", "uncertainty activity"]``.

        Notes
        -----
        * Only groups with at least two finite activity points are fit.
        * Nonlinear fits use either a helper ``fit_decay`` function (if available)
        or fall back to SciPy's ``curve_fit``.
        * Half-life is computed from λ using: ``t½ = ln(2)/λ``.
        * Natural log columns (``ln(activity)``, ``uncertainty ln(activity)``) are
        created if missing for possible linear diagnostics.
        * Internal diagnostic columns (ln-space slope/intercept) are prepared but
        currently commented out; they can be added if needed.
        
        """
        if self.peak_data.empty:
            raise ValueError("self.peak_data is empty. Run process_spectrum_files() first.")

        if plot_directory:
            Path(plot_directory).mkdir(parents=True, exist_ok=True)

        # Ensure required columns exist
        req = ["isotope", "energy", "decay time (s)", "activity", "uncertainty activity"]
        for c in req:
            if c not in self.peak_data.columns:
                raise KeyError(f"Column '{c}' missing in peak_data.")

        # Ensure ln(activity) columns exist
        if "ln(activity)" not in self.peak_data.columns:
            with np.errstate(divide="ignore", invalid="ignore"):
                self.peak_data["ln(activity)"] = np.log(self.peak_data["activity"])
        if "uncertainty ln(activity)" not in self.peak_data.columns:
            self.peak_data["uncertainty ln(activity)"] = (
                self.peak_data["uncertainty activity"] / self.peak_data["activity"]
            )

        results = []
        grouped = (self.peak_data
                .sort_values(["isotope", "energy", "decay time (s)"])
                .groupby(["isotope", "energy"], dropna=False))

        # Nonlinear decay model (A-space)
        def exp_decay(t, A0, lam):
            return A0 * np.exp(-lam * t)

        for (isotope, energy), df in grouped:
            # Keep rows with finite values
            mask_A = (
                df[["decay time (s)", "activity", "uncertainty activity"]].notna().all(axis=1) &
                (df["activity"] > 0) & (df["uncertainty activity"] > 0)
            )
            gA = df.loc[mask_A].copy()

            if len(gA) < 2:
                continue

            tA   = gA["decay time (s)"].to_numpy(float)
            aA   = gA["activity"].to_numpy(float)
            sA   = gA["uncertainty activity"].to_numpy(float)

            # Initial guesses for nonlinear fit
            if "half-life (s)" in gA.columns and np.isfinite(gA["half-life (s)"]).any():
                hl_guess = gA["half-life (s)"].dropna().iloc[0]
                lam0 = np.log(2) / max(hl_guess, 1.0)
            else:
                # crude slope from ends in ln-space
                lam0 = max(-(np.log(aA[-1]) - np.log(aA[0])) / max(tA[-1] - tA[0], 1.0), 1e-8)
            A0_guess = aA[0] * np.exp(lam0 * tA[0])

            # --- Nonlinear fit on A(t) ---
            try:
                # if you have a helper fit_decay that returns (params, std_params), use it:
                params, std_params = fit_decay(
                    t_vals=tA,
                    a_vals=aA,
                    decay_function=exp_decay,
                    unc_a_vals=sA,
                    xlabel="Decay Time (s)",
                    ylabel="Measured Activity (Bq)",
                    plot_label=f"{isotope} @ {energy} keV",
                    initial_guess=[max(A0_guess, np.nanmax(aA)), lam0],
                    plot_filename=(f"{plot_directory}/{str(isotope).replace('/', '_')}_{energy:.3f}_activity-time.png"
                                if plot_directory else None)
                )
                A0_fit, lam_fit = params
                std_A0, std_lam = std_params
            except Exception:
                # fall back to curve_fit if fit_decay is not available
                from scipy.optimize import curve_fit
                popt, pcov = curve_fit(exp_decay, tA, aA, p0=[max(A0_guess, np.nanmax(aA)), lam0],
                                    sigma=sA, absolute_sigma=True, maxfev=10000)
                A0_fit, lam_fit = popt
                perr = np.sqrt(np.diag(pcov)) if pcov is not None else [np.nan, np.nan]
                std_A0, std_lam = perr

            # Derived half-life from nonlinear fit
            if np.isfinite(lam_fit) and lam_fit > 0:
                hl_fit = np.log(2) / lam_fit
                std_hl_fit = (np.log(2) / (lam_fit ** 2)) * std_lam if np.isfinite(std_lam) else np.nan
            else:
                hl_fit = np.nan
                std_hl_fit = np.nan


                    # Mean/std of decay-corrected A0 from rows (if present)
            if "eob activity" in df.columns and "uncertainty eob activity" in df.columns:
                A0_vals = df["eob activity"].to_numpy(float)
                A0_unc  = df["uncertainty eob activity"].to_numpy(float)
                mean_A0 = float(np.nanmean(A0_vals)) if A0_vals.size else np.nan
                std_A0_vals = float(np.nanstd(A0_vals, ddof=1)) if A0_vals.size > 1 else np.nan
                N = np.count_nonzero(np.isfinite(A0_unc))
                sigma_mean_A0 = float(np.sqrt(np.nansum(A0_unc ** 2)) / N) if N > 0 else np.nan
            else:
                mean_A0 = std_A0_vals = sigma_mean_A0 = np.nan

            results.append({
                "Isotope": isotope,
                "Energy (keV)": energy,
                # Nonlinear (A-space) fit outputs:
                "A0 (fit)": A0_fit,
                "Std A0 (fit)": std_A0,
                "Half-life (fit) [s]": hl_fit,
                "Std Half-life (fit) [s]": std_hl_fit,
                # ln-space diagnostics:
                # "ln-slope m [1/s]": m,
                # "Std ln-slope": std_m,
                # "ln-intercept b": b,
                # "Std ln-intercept": std_b,
                # "chi2 (ln-fit)": chi2,
                # "dof (ln-fit)": dof,
                # Aggregates from decay-corrected per-point A0:
                "Mean A0 (decay-corrected)": mean_A0,
                "Std A0 (decay-corrected)": std_A0_vals,
                "Unc Mean A0 (decay-corrected)": sigma_mean_A0,
                "N points": int(len(gA)),
            })

        self.decay_results = pd.DataFrame(results).sort_values(
            by=["Isotope", "Energy (keV)"], kind="mergesort"
        )



    

    # -----------------------------------------
    # 3) (Optional) Get per-group DataFrames in-memory
    # -----------------------------------------
    def grouped_peaks(self):
        """
        Generate per-group peak data grouped by isotope and energy.

        This method yields pairs of ``(isotope, energy)`` and their corresponding
        DataFrame of peaks, sorted by decay time. It is useful for in-memory access
        to grouped peak data without performing any file I/O.

        Returns
        -------
        generator of tuple
            A generator yielding tuples of the form ``((isotope, energy), df)``, where:
            
            * ``isotope`` : object
                Identifier of the isotope (e.g., string or numeric label) from ``self.peak_data``.
            * ``energy`` : float
                Gamma energy (keV) associated with the group.
            * ``df`` : pandas.DataFrame
                A copy of the subset of ``self.peak_data`` for that isotope/energy,
                sorted by ``decay time (s)``.

        Notes
        -----
        * If ``self.peak_data`` is empty, an empty dictionary is returned immediately.
        * Each returned DataFrame is independent (copy) and can be safely modified
        without affecting the underlying ``self.peak_data``.
        * Groups are sorted lexicographically by isotope, energy, and then by decay time.

        Examples
        --------
        >>> serial = Serial(...)
        >>> serial.process_spectrum_files(...)
        >>> for (iso, E), df in serial.grouped_peaks():
        ...     print(f"{iso} @ {E} keV has {len(df)} peaks")
        """
        if self.peak_data.empty:
            return {}
        for key, df in self.peak_data.sort_values(["isotope", "energy", "decay time (s)"]).groupby(["isotope", "energy"]):
            yield key, df.copy()


    def save_peak_data(
        self,
        filepath: str,
        sort_key: str = "decay time (s)",
        columns: list[str] | None = None,
        include_summary: bool = True,
    ) -> str:
        """
        Save per-γ-line peak data to an Excel workbook, one sheet per (isotope, energy),
        each sheet sorted by time since EoB.

        Parameters
        ----------
        filepath : str
            Output .xlsx path (directories will be created if needed).
        sort_key : str, optional
            Column to sort each sheet by (default: "decay time (s)").
        columns : list[str] or None, optional
            If provided, restrict output to these columns in this order.
            If None, write all columns.
        include_summary : bool, optional
            If True, add a "Summary" sheet with counts per group and sheet names.

        Returns
        -------
        str
            The filepath written.

        Notes
        -----
        - Groups are formed by (isotope, energy) using the columns "isotope" and "energy".
        Make sure these exist in `self.peak_data`.
        - Sheet names are sanitized and truncated to Excel's 31-character limit; collisions
        are deduplicated with numeric suffixes.
        """
        import os
        from pathlib import Path
        import numpy as np
        import pandas as pd

        # Basic guards
        if getattr(self, "peak_data", None) is None or self.peak_data.empty:
            raise ValueError("No peak data available. Run process_spectrum_files() first.")

        required_cols = {"isotope", "energy", sort_key}
        missing = [c for c in required_cols if c not in self.peak_data.columns]
        if missing:
            raise KeyError(f"Missing required columns in peak_data: {missing}")

        # Ensure parent directory exists
        Path(os.path.dirname(os.path.abspath(filepath)) or ".").mkdir(parents=True, exist_ok=True)

        # Group by (isotope, energy) and ensure stable ordering
        df = self.peak_data.copy()
        df = df.sort_values(["isotope", "energy", sort_key])

        # Helper: sanitize and dedupe sheet names
        def sanitize_sheet_name(name: str) -> str:
            # Remove illegal chars and trim to 31 chars (Excel limit)
            bad = set(r'[]:*?/\\')
            cleaned = "".join(("_" if ch in bad else ch) for ch in name)
            return cleaned[:31] if len(cleaned) > 31 else cleaned

        def make_sheet_name(isotope: str, energy: float) -> str:
            # Example: "Tb-154m1_540.18keV"
            # Try to preserve useful precision but keep names short
            # Use up to 2 decimals when needed
            if pd.isna(energy):
                label = f"{isotope}_unkE"
            else:
                label = f"{isotope}_{energy:.2f}keV"
            return sanitize_sheet_name(label)

        # Build list of groups
        groups = []
        for (iso, e), g in df.groupby(["isotope", "energy"], dropna=False):
            groups.append((iso, e, g.copy()))

        if not groups:
            raise ValueError("No (isotope, energy) groups found in peak_data.")

        # Choose columns
        if columns is not None:
            for c in columns:
                if c not in df.columns:
                    raise KeyError(f"Requested column '{c}' not found in peak_data.")
        # Writer
        with pd.ExcelWriter(filepath, engine="xlsxwriter") as writer:
            used_names = set()
            summary_rows = []

            for iso, energy, g in groups:
                # Sort per group by the chosen key (already globally sorted, but ensure per-group)
                g = g.sort_values(sort_key).reset_index(drop=True)

                # Column subset (optional)
                out = g[columns] if columns is not None else g

                # Build and dedupe sheet name
                base_name = make_sheet_name(str(iso), float(energy) if energy is not None else np.nan)
                sheet_name = base_name
                k = 1
                # Make sure sheet name is unique and within 31 chars
                while sheet_name in used_names:
                    suffix = f"_{k}"
                    sheet_name = sanitize_sheet_name(base_name[: (31 - len(suffix))] + suffix)
                    k += 1
                used_names.add(sheet_name)

                # Write sheet
                out.to_excel(writer, sheet_name=sheet_name, index=False)

                # Collect summary
                if include_summary:
                    summary_rows.append(
                        {
                            "isotope": iso,
                            "energy (keV)": energy,
                            "rows": len(out),
                            "sheet": sheet_name,
                        }
                    )

            # Summary sheet
            if include_summary and summary_rows:
                s = pd.DataFrame(summary_rows).sort_values(["isotope", "energy (keV)"])
                s.to_excel(writer, sheet_name="Summary", index=False)

        return filepath
    

    def save_decay_data(self, filepath: str = "decay_results.xlsx") -> str:
        """
        Save the decay analysis results to a single-sheet Excel file.

        Parameters
        ----------
        filepath : str, optional
            Path to the output `.xlsx` file (default: "decay_results.xlsx").
            Parent directories are created if needed.

        Returns
        -------
        str
            Absolute path to the written Excel file.

        Raises
        ------
        ValueError
            If `self.decay_results` is empty or missing.

        Notes
        -----
        - Writes all columns of `self.decay_results` to a single sheet called "DecayResults".
        - Intended for the summary DataFrame produced by `process_decay_data()`.
        """
        if getattr(self, "decay_results", None) is None or self.decay_results.empty:
            raise ValueError("No decay results available. Run process_decay_data() first.")

        # Ensure parent directory exists
        out_path = Path(filepath)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        # Write to Excel (single sheet)
        self.decay_results.to_excel(out_path, sheet_name="DecayResults", index=False)

        print(f"💾 Results saved to: {out_path.resolve()}")
        return str(out_path.resolve())
