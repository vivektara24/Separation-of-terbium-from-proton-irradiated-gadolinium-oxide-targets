from datetime import datetime
import os
from nuclab.utils import *
import curie as ci
from pathlib import Path

class Calibration:
    """
    Streamlines workflows for High Purity Germanium (HPGe) detector efficiency calibration.

    Performs peak fitting on calibration spectra, derives line-by-line detector
    efficiencies with uncertainties, and fits these points with a user-defined efficiency
    function. Provides a compact estimate of the fractional uncertainty 
    in efficiency values returned by the fitted function. Results 
    (per-peak table, fit parameters, plots, etc.) can be saved for downstream analysis.
    The fitted efficiency parameters and fractional uncertainty are used as inputs to the
    `Serial` class in the nuclab package.

    Parameters
    ----------
    data_path : str or pathlib.Path
        Path to a single calibration spectrum file (``.Spe``) to process.
    eob_time : datetime.datetime, optional
        End-of-bombardment timestamp for calibration sources.
    gammas : pandas.DataFrame
        Table of gamma lines used for peak fitting. Must include columns such as 
        ``["energy", "intensity", "unc_intensity", "isotope"]`` with energies in keV.
    half_lives : dict of float to float
        Mapping from gamma energy (keV) to half-life (s) for all entries in the `gamma` DataFrame.
    calibration_eob_activities : dict[float, float], optional
        End-of-bombardment calibration source activities. Keyed by gamma energy (keV).
    eff_func : callable, optional
        Parametric detector efficiency function used for fitting and evaluation:
        ``eff_func(energy_keV, *params) -> efficiency``.

    Attributes
    ----------
    eff_fit_params : list[float] or None
        Best-fit parameters for ``eff_func``, obtained by fitting the efficiency
        function to the measured detector efficiencies across the gamma energies
        specified in the ``gammas`` DataFrame.
    unc_eff_fit_params : list[float] or None
        1σ standar error (standard deviation uncertainties) in the fitted parameters,`eff_fit_params`.
    fractional_unc_eff : float or None
        The average plus one standard deviation of the experimentally measured
        efficiency relative residual absolute values.
    peak_data : pandas.DataFrame
        Fitted peak data from processed spectra w/ metadata.
    """

    def __init__(self, data_path: str = None, eob_time: datetime = None, gammas: pd.DataFrame = None,
                 half_lives: dict[float, float] = None, calibration_eob_activities: dict[float, float] = None,
                 eff_func: callable = None):

        self.data_path = data_path
        self.eob_time = eob_time
        self.gammas = gammas
        self.half_lives = half_lives
        self.calibration_eob_activities = calibration_eob_activities
        self.eff_func = eff_func

        self.eff_fit_params: list[float] = []
        self.unc_eff_fit_params: list[float] =  []

        self.fractional_sigma_detector_eff = None

        self.peak_data = pd.DataFrame()     # accumulated enriched peaks


    def process_spectrum_file(self):
        """

        Analyze a single calibration spectrum (``.Spe``) at the specified data_path and populate
        per-line detector efficiencies.

        Parameters
        ----------
        None
            All required inputs are taken from instance attributes:
            ``data_path``, ``eob_time``, ``gammas``, ``half_lives``,
            ``calibration_eob_activities``.

        Returns
        -------
        pandas.DataFrame
            The populated ``peak_data`` DataFrame (also assigned to ``self.peak_data``).
        """
        # List all .Spe files in the directory
        file_path = str(self.data_path)
        file = os.path.basename(file_path)
        base_filename = os.path.splitext(file)[0]
            
        # Extract slot number from filename
        slot_number = "Unknown"
        detector_slot = "Unknown"
        parts = base_filename.split('-')
        for part in parts:
            if part.startswith('d1s'):
                slot_number = part[3:]
                if slot_number.isdigit():
                    detector_slot = int(slot_number)
                break
            
        # Load the Spectrum object
        sp = ci.Spectrum(file_path)
        #sp.saveas(f'Peak-Fit-Plots/{file}.svg')
            
        # Compute decay time since end of bombardment
        decay_time = (sp.start_time - self.eob_time).total_seconds()
            
        # Fit the peaks
        sp.fit_peaks(gammas=self.gammas)
        #sp.saveas(f'Peak-Fit-Plots/{file}-peak-fit.svg')

        peaks = sp.peaks
        if peaks is None or len(peaks) == 0:
            print(f"No peaks found in {file}")
            return None
        

            
        # If peaks were successfully fitted, process and save results
        if peaks is not None:
            peaks['file'] = file  # Store filename in the dataset
            peaks['decay time (s)'] = decay_time # Store time since EOB in the datset
            peaks['half-life (s)'] = peaks['energy'].map(self.half_lives)
                
            peaks['activity'] = calculate_activity(peaks['energy'].map(self.calibration_eob_activities), sp.peaks['decay time (s)'], sp.peaks['half-life (s)']) * 37000
                
            # Compute decay constant
            decay_constant = np.log(2) / peaks['half-life (s)']

            peaks['detector efficiency'] = peaks['counts'] * decay_constant / (peaks['intensity'] * peaks['activity'] * (1 - np.e ** (-decay_constant * peaks['live_time'])))

            peaks['uncertainty detector efficiency'] = np.sqrt(
                    (decay_constant * peaks['unc_counts'] /
                    peaks['activity'] /
                    peaks['intensity'] /
                    (1 - np.e ** (-decay_constant * peaks['live_time']))) ** 2 +
                    (peaks['counts'] * decay_constant * peaks['unc_intensity'] /
                    peaks['activity'] /
                    peaks['intensity'] ** 2 /
                    (1 - np.e ** (-decay_constant * peaks['live_time']))) ** 2
                )

                
                # Remove unnecessary columns
            cols_to_remove = ['efficiency', 'unc_efficiency']
            peaks.drop(columns=cols_to_remove, inplace=True)
            
            self.peak_data = peaks
                
                
            print(f'Finished fitting peaks for {file}')
            return self.peak_data


    def process_calibration_data(self, initial_guesses=None, plot_directory=None, plot_name="calibration-plot", xlim=None, ylim=None):
        """
        Fit the detector efficiency calibration curve to per-line detector efficiencies

        Parameters
        ----------
        initial_guesses : list[float]
            Initial estimates for the efficiency function parameters.
        plot_directory : str or pathlib.Path
            Directory to which the calibration plot will be saved.
        plot_name : str, default="calibration-plot"
            Base name for the saved calibration plot (without extension).
        xlim : tuple[float, float], optional
            X-axis limits for the calibration plot (energy axis).
        ylim : tuple[float, float], optional
            Y-axis limits for the calibration plot (efficiency axis).

        Returns
        -------
        params : list[float]
            Best-fit parameters of the efficiency function.
        unc_params : list[float]
            1σ standard errors of the fitted parameters, derived from the
            covariance matrix of the fit.
        """

        if plot_directory is not None:
            plot_directory = Path(plot_directory)
            plot_directory.mkdir(parents=True, exist_ok=True)
            plot_path = plot_directory / f"{plot_name}.png"
        else:
            plot_path = f"{plot_name}.png"





        # Read all sheets from the Excel file
        df = self.peak_data

        # Initialize a list to store results
        energy_vals = df['energy']

        efficicency_vals = df['detector efficiency']
        unc_efficiency_vals = df['uncertainty detector efficiency']
        

        params, unc_params = fit_decay(t_vals = energy_vals,
                                    a_vals = efficicency_vals,
                                    decay_function = self.eff_func,
                                    unc_a_vals = unc_efficiency_vals,
                                    xlabel="Energy (keV)",
                                    ylabel="Detector Efficiency (CPS/Bq)",
                                    plot_label="",
                                    initial_guess=initial_guesses,
                                    plot_filename=plot_path,
                                    xlim=xlim,
                                    ylim=ylim)
        
        self.eff_fit_params, self.unc_eff_fit_params = params, unc_params

        return params, unc_params
    


    def get_eff_fit_uncetainty(self):
        """
        Calculate the fractional uncertainty of the fitted efficiency function.

        For each calibration line, the relative absolue residual is defined as
        ``|y_fit - y| / y_fit``, where ``y`` is the measured efficiency and
        ``y_fit`` is the fitted efficiency at that energy. The overall
        fractional uncertainty is taken as the mean of these absolue relative
        residuals plus one standard deviation. This single value,
        stored in ``self.fractional_sigma_detector_eff``, can be propagated
        into activity and half-life calculations in the ``Serial`` class.
        
        Returns
        -------
        float
            Estimated fractional efficiency uncertainty. 
        """

        x, y = self.peak_data['energy'], self.peak_data['detector efficiency']
        params = self.eff_fit_params

        y_fit = self.eff_func(x, *params)

        mean_rel_abs_residuals = np.mean(abs(y_fit - y) / y_fit)

        std_rel_abs_residuals = np.std(abs(y_fit - y) / y_fit)

        self.fractional_sigma_detector_eff = mean_rel_abs_residuals + 1 * std_rel_abs_residuals

        return self.fractional_sigma_detector_eff
    

    def save_peak_data(self, output_csv: str, index: bool = False) -> None:
        """
        Save the processed peak_data DataFrame to a CSV file.

        Parameters
        ----------
        output_csv : str
            Path to the CSV file where peak data will be saved.
        index : bool, default=False
            Whether to include the DataFrame index in the output file.
        """
        if self.peak_data is None or self.peak_data.empty:
            raise ValueError("peak_data is empty. Process spectrum files before saving.")
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        
        # Save DataFrame to CSV
        self.peak_data.to_csv(output_csv, index=index)
        print(f"Peak data saved to {output_csv}")
