import numpy as np
from scipy.integrate import solve_ivp
from numbalsoda import lsoda, lsoda_sig
from numba import cfunc, njit
import matplotlib.pyplot as plt
import pandas as pd
from lmfit.model import Model, save_modelresult, load_modelresult
import math

# =============================================================================
# Define functions
# =============================================================================

def calc_kadd_from_eyring(temp, m, b, S):
    """
    Calculate the association rate constant (k_add) from Eyring equation parameters.

    Parameters
    ----------
    temp : float
        Temperature in Kelvin.
    m : float
        Slope of the Eyring plot.
    b : float
        Intercept of the Eyring plot.
    S : float
        Concentration of probe in M.

    Returns
    -------
    float
        Association rate constant (k_add) in units of M^-1 s^-1.
    """

    eyring_y = m * (1 / temp) + b
    return (np.exp(eyring_y) * temp) / S

def ode_solution(y0, rates, x):
    """
    Solve a system of ordinary differential equations (ODEs) for chemical probing.

    Parameters
    ----------
    y0 : numpy array
        Initial values for the ODEs - U, R, S, M, Z.
    rates : numpy array
        Rate constants for the ODEs - k_o, k_c, k_add, k_hydr.
    x : numpy array
        Time points to evaluate the ODEs.

    Returns
    -------
    x : ndarray
        Array of time points.
    y : ndarray
        Array of the fraction of M over (U + R + M) at each time point.
    """

    @cfunc(lsoda_sig)
    def chem_probing_fastODE(t, y, du, p):
        du[0] = -p[0]*y[0] + p[1]*y[1]
        du[1] = p[0]*y[0] - p[1]*y[1] - p[2]*y[1]*y[2]
        du[2] = -p[2]*y[1]*y[2] - p[3]*y[2]
        du[3] = p[2]*y[1]*y[2]
        du[4] = p[3]*y[2]

    # address to ODE function
    funcptr = chem_probing_fastODE.address
    t_eval = x

    # integrate with lsoda method
    sol, success = lsoda(funcptr, y0, t_eval, data = rates)

    # calculate fraction of M over (U + R + M)
    y = sol[:, 3] / (sol[:, 0] + sol[:, 1] + sol[:, 3])

    return y

def pe_model(x, K, k_add, k_hydr, S):
    """ Pre-equilibrium assumption model """
    kappa = ((K / (K + 1)) * k_add * S) / k_hydr
    return 1 - np.exp(-kappa * (1 - np.exp(-k_hydr * x)))

def ss_model(x, k_o, k_c, k_add, k_hydr, S):
    """ Steady-state approximation model """
    num = k_o * k_add * S
    denom = k_o + k_c * k_add * S
    k_obs = num / denom
    kappa = k_obs / k_hydr
    return 1 - np.exp(-kappa * (1 - np.exp(-k_hydr * x)))

def solve_fmod(k_c, lnkhydr_model, k_add_mb, temp = 45):
    """ Solve the ODEs and calculate the pre-equilibrium assumption and steady-state approximation models """
    
    K = 0.5
    k_o = K * k_c

    S = 0.001584
    temp += 273.15 # convert to Kelvin
    k_add_m, k_add_b = k_add_mb
    k_add = calc_kadd_from_eyring(temp, k_add_m, k_add_b, S)
    k_hydr = np.exp(lnkhydr_model.eval(x=1 / temp)) * temp

    # Initial concentrations of U, R, S, M, Z
    y0 = np.array([1e-6, 1e-6, S, 0.0, 0.0])

    # Rate constants
    rates = np.array([k_o, k_c, k_add, k_hydr])
    
    # Print all rate constants
    print(f' - k_o = {k_o}')
    print(f' - k_c = {k_c}')
    print(f' - k_add = {k_add}')
    print(f' - k_hydr = {k_hydr}')

    # Solve for fmod (% modification)
    x = np.linspace(0, 2000, 50)
    y_ode = ode_solution(y0, rates, x)
    y_pe = pe_model(x, K, k_add, k_hydr, S)
    y_ss = ss_model(x, k_o, k_c, k_add, k_hydr, S)

    # Calculate residuals
    res_pe = y_pe - y_ode
    res_ss = y_ss - y_ode

    return {'x': x, 'y_ode': y_ode, 'y_pe': y_pe, 'res_pe': res_pe, 'y_ss': y_ss, 'res_ss': res_ss}

def plot_solutions(x, y_ode, y_pe, res_pe, y_ss, res_ss, t, ax):

    ax.plot(x, y_ode, label='ODE solution', ls='-', lw = 2, color='#fac748')
    ax.plot(x, y_pe, label='Pre-equilibrium assumption', marker = 'o', markersize = 1, ls='', color='#1d2f6f')

    exp = -int(math.log10(t))
    ax.text(0.95, 0.15, rf'$10^{{{exp}}}$ s', transform=ax.transAxes, ha='right', va='top', fontsize=10)

    #ax.set_ylabel(r'$f_{mod}$')
    #ax.set_xlabel('Time (s)')

    return ax

# =============================================================================
# Solve ODEs and plot
# =============================================================================

khydr_modelpath = snakemake.input[0]

lnkhydr_model = load_modelresult(khydr_modelpath)
k_add_mb = (-419.754617, -10.682813)

timescales = [1e12, 1e9, 1e6, 1e3, 1e0, 1e-3, 1e-6]
n = len(timescales)
# plot residue in a subplot above
fig, axs = plt.subplots(1, n, sharey = True, figsize=(8, 1.5))
plt.rcParams['font.family'] = 'Helvetica'

for i, t in enumerate(timescales):
    plot_solutions(**solve_fmod(t, lnkhydr_model, k_add_mb, 45), t = t, ax = axs[i])
    axs[i].set_xticks([0, axs[i].get_xlim()[1]/2, axs[i].get_xlim()[1]])
    axs[i].set_xticklabels([])

    # Set y-tick marks
    yticks = np.linspace(0, axs[i].get_ylim()[1], 4)
    axs[i].set_yticks(np.linspace(0, axs[i].get_ylim()[1], 4))
    axs[i].set_yticklabels([f"{ytick:.2f}" for ytick in yticks])

fig.text(0.02, 0.5, r'$f_{mod}$', va='center', rotation='vertical')
fig.text(0.5, 0.04, 'Time', ha='center')
plt.subplots_adjust(wspace = 0.12, left = 0.1, right = 0.98, bottom = 0.2, top = 0.95)
plt.savefig(snakemake.output[0])
