"""
Example: HPGe analysis workflow using `Serial`.

Steps:
1) Configure inputs (paths, EOB time, efficiency function, gamma table, half-lives)
2) Create a `Serial` instance
3) Process .Spe files → peak table
4) Run decay analysis → per-(isotope, energy) results
5) Save results to Excel
6) (Optional) Iterate grouped peak DataFrames
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import Callable, Sequence


import pandas as pd
import numpy  as np

# Import Serial class
from serial import Serial  # assumes `serial.py` is in the same folder

# -----------------------------------------------------------------------------
# 1) Inputs
# -----------------------------------------------------------------------------

# Relative path to directory containing your `.Spe` files
DATA_DIR = Path("2Hr-Data/")


# End-of-bombardment timestamp
EOB_TIME = datetime(2025, 2, 21, 7, 58)  # YYYY, M, D, h, m

# Detector efficiency fit parameters (example)
EFFICIENCY_FIT_PARAMS: Sequence[float] = [0.0377, -13.3000, 0.9218, -0.0928, 0.0030, 0.0000]



def EffFit(energy_keV: np.ndarray | float,
           b1: float, b2: float, b3: float, b4: float, b5: float, b6: float) -> np.ndarray:
    """
    Empirical efficiency curve.

    Parameters
    ----------
    energy_keV : array-like or float
        Gamma energy in keV.
    b1..b6 : float
        Coefficients for the fit.

    Returns
    -------
    np.ndarray
        Detector efficiency for each energy value.
    """
    x = np.asarray(energy_keV, dtype=float) / 1000.0  # keV → MeV
    y = np.exp(b1 * x**1 + b2 * x**0 + b3 * x**-1 + b4 * x**-2 + b5 * x**-3 + b6 * x**-4)
    return y

# Gamma-line table (energy in keV; intensities in %)
GAMMAS = pd.DataFrame(
    {
        "energy": [
            344.2785, 586.27, 778.9045,  # 152Tb
            212.00,                      # 153Tb
            123.07, 1274.436, 1291.31,   # 154gTb
            540.18,                      # 154m1Tb
            426.78,                      # 154m2Tb
            105.318, 148.64, 180.08, 262.27,  # 155Tb
            534.29, 199.19, 1222.44      # 156Tb
        ],
        "intensity": [
            63.5, 9.21, 5.54,            # 152Tb
            28.5,                         # 153Tb
            26.0, 10.5, 6.9,              # 154gTb
            20.0,                         # 154m1Tb
            17.3,                         # 154m2Tb
            25.1, 2.65, 7.5, 5.3,         # 155Tb
            67.0, 41.0, 31.0              # 156Tb
        ],
        "unc_intensity": [
            1.7, 0.21, 0.13,             # 152Tb
            1.9,                          # 153Tb
            4.0, 0.8, 0.5,                # 154gTb
            3.0,                          # 154m1Tb
            1.2,                          # 154m2Tb
            1.3, 0.14, 0.4, 0.3,          # 155Tb
            6.0, 5.0, 3.0                 # 156Tb
        ],
        "isotope": [
            "152TB", "152TB", "152TB",
            "153TB",
            "154TB", "154TB", "154TB",
            "154TB",
            "154TB",
            "155TB", "155TB", "155TB", "155TB",
            "156TB", "156TB", "156TB",
        ],
    }
)

# Half-lives: energy (keV) → half-life (s)
HALF_LIVES = {
    344.2785: 17.5 * 60 * 60,
    586.27:   17.5 * 60 * 60,
    778.9045: 17.5 * 60 * 60,
    212.00:   2.34 * 24 * 60 * 60,
    123.07:   21.5 * 60 * 60,
    1274.436: 21.5 * 60 * 60,
    1291.31:  21.5 * 60 * 60,
    540.18:   9.4 * 60 * 60,
    426.78:   22.7 * 60 * 60,
    105.318:  5.32 * 24 * 60 * 60,
    148.64:   5.32 * 24 * 60 * 60,
    180.08:   5.32 * 24 * 60 * 60,
    262.27:   5.32 * 24 * 60 * 60,
    534.29:   5.35 * 24 * 60 * 60,
    199.19:   5.35 * 24 * 60 * 60,
    1222.44:  5.35 * 24 * 60 * 60,
}


# -----------------------------------------------------------------------------
# 2) Main
# -----------------------------------------------------------------------------

def main() -> None:
    # Output/plot paths
    plots_dir = Path("TESTPLOTS")
    outputs_dir = Path("outputs")
    plots_dir.mkdir(parents=True, exist_ok=True)
    outputs_dir.mkdir(parents=True, exist_ok=True)

    # Quick sanity check
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Data directory not found: {DATA_DIR.resolve()}")

    # Create analysis object
    S = Serial(
        data_directory=str(DATA_DIR),
        eob_time=EOB_TIME,
        efficiency_fit_params=list(EFFICIENCY_FIT_PARAMS),
        # NOTE: keep arg name consistent with your class signature
        detector_eff_uncertianty=0.0860345384967799,  # 8.6% example (fractional)
        gammas=GAMMAS,
        half_lives=HALF_LIVES,
    )

    # -------------------------------------------------------------------------
    # 3) Process spectrum files → peak_data
    # -------------------------------------------------------------------------
    S.process_spectrum_files(
        efficiency_func=EffFit,
        plot_dir=str(plots_dir),
    )

    # (Optional) save the enriched peak table via your class utility
    # Requires your `Serial.save_peak_data(...)` method
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

    # -------------------------------------------------------------------------
    # 4) Decay analysis → decay_results
    # -------------------------------------------------------------------------
    S.process_decay_data(
        plot_directory=str(plots_dir / "decay-fits")
    )

    # -------------------------------------------------------------------------
    # 5) Save per-group results to Excel
    # -------------------------------------------------------------------------
    S.save_decay_data(outputs_dir / "decay_results_vkt.xlsx")

    # -------------------------------------------------------------------------
    # 6) (Optional) Access grouped DataFrames
    # -------------------------------------------------------------------------
    print("\n📦 Grouped peak DataFrames (first few rows each):")
    for (iso, energy), df_group in S.grouped_peaks():
        print(f"\n  {iso} @ {energy:.3f} keV  |  n={len(df_group)}")
        print(df_group.head(5))

if __name__ == "__main__":
    main()