import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from pathlib import Path
from numpy.linalg import cond


def fit_decay(t_vals, a_vals, decay_function, unc_a_vals, xlabel, ylabel, plot_label, initial_guess=None, plot_filename="data-fit.png", xlim=None, ylim=None):
    """
    Fits the provided data to a given decay function and plots the fitted curve.

    Parameters:
    - t_values (array-like): Array of elapsed time values (in seconds).
    - A_values (array-like): Array of measured activity (e.g., Activity in mCi or Counts Per Second).
    - decay_function (function): The decay function to fit, with parameters to be optimized.
    - initial_guess (list, optional): Initial guesses for decay function parameters. Defaults to [10, 5, 1].
    - plot_filename (str, optional): Filename to save the plot. Defaults to "data-fit.png".

    Returns:
    - params (array): Optimized parameters for the decay function.
    - covariance (array): Covariance matrix of the estimated parameters.
    """

    # Fit the decay function to the provided data using non-linear least squares optimization
    params, covariance = curve_fit(f=decay_function, xdata=t_vals, ydata=a_vals, sigma=unc_a_vals, absolute_sigma=True, p0=initial_guess)

    # Calculate standard deviations (uncertainties) from the covariance matrix
    param_errors = np.sqrt(np.diag(covariance))


    # ---- Print which series/file is being analyzed ----
    # (use plot_label for human-readable, and filename for traceability)
    fname_str = Path(plot_filename).name if plot_filename else "(no file)"
    print("\n" + "="*50)
    print(f"Analyzing: {plot_label}  →  {fname_str}")
    print("Optimized Decay Parameters:")
    for i, (param, error) in enumerate(zip(params, param_errors)):
        print(f"  Parameter {i+1}: {param:.4f} ± {error:.4f}")
    print("="*50 + "\n")

        # Diagnostic: Jacobian condition number
    try:
        print(f"📐 Jacobian condition number: {cond(covariance):.2e}")
    except Exception as e:
        print("⚠️ Could not compute Jacobian condition number:", e)

    # Generate time values for plotting the fitted curve
    t_fit = np.linspace(1, max(t_vals), 200)  # 200 evenly spaced time points
    y_fit = decay_function(t_fit, *params)  # Compute fitted decay values

    # Plot
    plt.figure(figsize=(8, 5), dpi=120)
    plt.scatter(t_vals, a_vals, color="dodgerblue")
    plt.errorbar(t_vals, a_vals, yerr=unc_a_vals, label="Experimental", fmt="none", color="dodgerblue", alpha=0.8, ecolor="dodgerblue")
    plt.plot(t_fit, y_fit, label="Polynomial Fit", color="navy", linestyle="--", linewidth=2)

    # Formatting
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xlim(xlim)
    plt.ylim(ylim)
    #plt.title(f"{ylabel} vs {xlabel}: {plot_label}", fontsize=14)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)

    # Save and show plot
    plt.savefig(plot_filename, bbox_inches="tight", dpi=150)
    plt.show()

    return params, param_errors


def calculate_eob_activity(N, sigma, I, half_life, t):
    """
    Calculate the activity produced in a charged particle induced reaction.

    Parameters:
    - N (float): Atomic areal density (atoms/cm²)
    - sigma (float): Cross-section (cm²)
    - I (float): Projectile Intensity (particles/s)
    - half_life (float): Half-life (s)
    - t (float): Irradiation Length (s)

    Returns:
    - A_t (float): Activity Produced (Bq)
    """
    # Convert half-life to decay constant
    lambda_ = np.log(2) / half_life

    # Calculate activity
    A_t = N * sigma * I * (1 - np.exp(-lambda_ * t))

    return A_t

def calculate_N0(A_t, sigma, I, half_life, t):
    """
    Calulate atomic areal density (atoms/cm2).

    Parameters:
    - A_t (float): Activity Produced (Bq)
    - sigma (float): Cross-section (cm²)
    - I (float): Projectile Intensity (particles/s)
    - half_life (float): Half-life (s)
    - t (float): Irradiation Length (s)

    Returns:
    - N0 (float): Atomic areal density (atoms/cm²)
    """
    # Convert half-life to decay constant
    lambda_ = np.log(2) / half_life

    denominator = sigma * I * (1 - np.exp(-lambda_ * t))
    
    if denominator == 0:
        raise ValueError("Denominator is zero, check input values.")

    return A_t / denominator


def linear_interpolation(x_vals, y_vals, query, mode='y'):
    """
    Perform linear interpolation on given x and y vectors.

    Parameters:
    - x_vals (list or np.array): The x values.
    - y_vals (list or np.array): The y values.
    - query (float or np.array): The value(s) to interpolate.
    - mode (str): 'y' to find y for given x, 'x' to find x for given y.

    Returns:
    - Interpolated value(s) as float or np.array.
    """
    x_vals, y_vals = np.array(x_vals), np.array(y_vals)

    if mode == 'y':
        return np.interp(query, x_vals, y_vals)
    elif mode == 'x':
        return np.interp(query, y_vals, x_vals)
    else:
        raise ValueError("Mode must be 'y' or 'x'")

import numpy as np
import matplotlib.pyplot as plt

def calculate_parent_daughter_activities(A1_0, t_half1, t_half2, time):
    """
    Calculate the activities of the parent and daughter isotopes over time.
    
    Parameters:
    A1_0 (float): Initial activity of the parent isotope
    t_half1 (float): Half-life of the parent isotope
    t_half2 (float): Half-life of the daughter isotope
    time (numpy array): Time points for evaluation
    
    Returns:
    A1 (numpy array): Activity of the parent isotope over time
    A2 (numpy array): Activity of the daughter isotope over time
    """
    # Convert half-lives to decay constants
    lambda1 = np.log(2) / t_half1
    lambda2 = np.log(2) / t_half2
    
    # Parent activity
    A1 = A1_0 * np.exp(-lambda1 * time)
    
    # Daughter activity
    A2 = A1_0 * (lambda1 * lambda2 / (lambda2 - lambda1)) * (np.exp(-lambda1 * time) - np.exp(-lambda2 * time))
    
    return A1, A2

def calculate_activity(initial_activity, decay_time, half_life):

    decay_constant = np.log(2) / half_life

    return initial_activity * np.exp(-decay_constant * decay_time)