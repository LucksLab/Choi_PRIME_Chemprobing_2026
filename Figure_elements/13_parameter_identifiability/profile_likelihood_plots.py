import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.stats import norm
from sympy import symbols, exp, lambdify
import matplotlib as mpl

# Set Helvetica font globally
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Helvetica']

# Optional: make sure fonts are updated
mpl.rcParams['pdf.fonttype'] = 42  # Avoids Type 3 fonts in PDF output
mpl.rcParams['ps.fonttype'] = 42


# === Define model ===
t_sym, kappa_sym, kdeg_sym = symbols('t kappa kdeg')
y_expr = 1 - exp(-(kappa_sym / kdeg_sym) * (1 - exp(-kdeg_sym * t_sym)))
y_fn = lambdify((t_sym, kappa_sym, kdeg_sym), y_expr, 'numpy')

# === Simulated data ===
true_kappa = 1.5
true_kdeg = 0.7
timepoints = np.linspace(0.01, 5, 100)
true_y = y_fn(timepoints, true_kappa, true_kdeg)
noise_std = 0.1
y_noisy = true_y + norm.rvs(scale=noise_std, size=true_y.shape)

# === Residual ===
def residual(params):
    return np.sum((y_fn(timepoints, *params) - y_noisy) ** 2)

# === Best-fit ===
initial_guess = [1.0, 1.0]
result = minimize(residual, initial_guess, bounds=[(0.01, 5), (0.01, 5)])
best_fit = result.x

# === Profile likelihood computation ===
kappa_vals = np.linspace(0.5, 3.0, 100)
kdeg_vals = np.linspace(0.1, 1.5, 100)
profile_kappa = []
profile_kdeg = []

# Profile over kappa
for k in kappa_vals:
    def res_kdeg(kdeg_var):
        return residual([k, kdeg_var[0]])
    res = minimize(res_kdeg, [best_fit[1]], bounds=[(0.01, 5)])
    profile_kappa.append(res.fun)

# Profile over kdeg
for d in kdeg_vals:
    def res_kappa(kappa_var):
        return residual([kappa_var[0], d])
    res = minimize(res_kappa, [best_fit[0]], bounds=[(0.01, 5)])
    profile_kdeg.append(res.fun)

# === Plot ===
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 3))

ax1.plot(kappa_vals, profile_kappa, label='Profile over κ')
ax1.axvline(true_kappa, linestyle='--', color='gray', label='True κ')
ax1.axvline(best_fit[0], linestyle=':', color='darkred', label='Best Fit κ')
ax1.set_xlabel('κ')
ax1.set_ylabel('Loss')
ax1.set_title('Profile Likelihood: κ')
ax1.legend()

ax2.plot(kdeg_vals, profile_kdeg, label=r'Profile over $k_{deg}$')
ax2.axvline(true_kdeg, linestyle='--', color='gray', label=r'True $k_{deg}$')
ax2.axvline(best_fit[1], linestyle=':', color='darkred', label=r'Best Fit $k_{deg}$')
ax2.set_xlabel(r'$k_{deg}$')
ax2.set_ylabel('Loss')
ax2.set_title(r'Profile Likelihood: $k_{deg}$')
ax2.legend()

plt.tight_layout()
plt.savefig('profile_likelihood_plots.pdf')