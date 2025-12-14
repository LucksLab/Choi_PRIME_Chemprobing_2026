import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.stats import norm, chi2
from sympy import symbols, exp, lambdify, diff
import matplotlib as mpl
from matplotlib.patches import Ellipse

# === Plot settings ===
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Helvetica']
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

# === Define model symbolically ===
t_sym, kappa_sym, kdeg_sym = symbols('t kappa kdeg')
y_expr = 1 - exp(-(kappa_sym / kdeg_sym) * (1 - exp(-kdeg_sym * t_sym)))
dy_dkappa = diff(y_expr, kappa_sym)
dy_dkdeg = diff(y_expr, kdeg_sym)
y_fn = lambdify((t_sym, kappa_sym, kdeg_sym), y_expr, 'numpy')
dy_dkappa_fn = lambdify((t_sym, kappa_sym, kdeg_sym), dy_dkappa, 'numpy')
dy_dkdeg_fn = lambdify((t_sym, kappa_sym, kdeg_sym), dy_dkdeg, 'numpy')

# === Simulation parameters ===
true_kappa = 1.5
true_kdeg = 0.7
timepoints = np.linspace(0.01, 5, 100)
true_y = y_fn(timepoints, true_kappa, true_kdeg)
noise_std = 0.1
initial_guess = [1.0, 1.0]

# === Generate noisy data ===
y_noisy = true_y + norm.rvs(scale=noise_std, size=true_y.shape)

# === Define residual ===
def residual(params):
    return np.sum((y_fn(timepoints, *params) - y_noisy) ** 2)

# === Fit model ===
result = minimize(residual, initial_guess, bounds=[(0.01, 5), (0.01, 5)])
best_fit = result.x

# === Jacobian and Fisher Information ===
J = np.vstack([
    dy_dkappa_fn(timepoints, *best_fit),
    dy_dkdeg_fn(timepoints, *best_fit)
]).T
Fisher = J.T @ J
cov = noise_std**2 * np.linalg.inv(Fisher)

# === Define quadratic form for contour ===
def fisher_quad(x, y, center, fisher_matrix):
    delta = np.array([x - center[0], y - center[1]])
    return delta.T @ fisher_matrix @ delta

# === Grid for contour ===
kappa_vals = np.linspace(0.5, 3.0, 200)
kdeg_vals = np.linspace(0.1, 1.5, 200)
KAPPA, KDEG = np.meshgrid(kappa_vals, kdeg_vals)
Z = np.zeros_like(KAPPA)
for i in range(KAPPA.shape[0]):
    for j in range(KAPPA.shape[1]):
        Z[i, j] = fisher_quad(KAPPA[i, j], KDEG[i, j], best_fit, Fisher)

# === Draw confidence ellipse ===
def draw_confidence_ellipse(ax, center, cov, confidence=0.95, **kwargs):
    chi2_val = chi2.ppf(confidence, df=2)
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    vals, vecs = vals[order], vecs[:, order]
    width, height = 2 * np.sqrt(vals * chi2_val)
    angle = np.degrees(np.arctan2(*vecs[:, 0][::-1]))
    ellipse = Ellipse(xy=center, width=width, height=height, angle=angle, **kwargs)
    ax.add_patch(ellipse)
    return vals, vecs

# === Plot ===
fig, ax = plt.subplots(figsize=(3, 3))
contour = ax.contourf(KAPPA, KDEG, Z, levels=30, cmap='Greys')
cbar = plt.colorbar(contour, ax=ax, label='Loss approximation')

# Add best fit and true value
ax.scatter(*best_fit, color='darkred', s=30, label='Best Fit')
ax.scatter(true_kappa, true_kdeg, color='black', marker='x', s=50, label='True Value')

# Draw ellipse and get eigenvalues/vectors
vals, vecs = draw_confidence_ellipse(ax, best_fit, cov, confidence=0.95,
                                     edgecolor='blue', facecolor='none', linewidth=2, label='95% CI')

# === Stiff and sloppy directions ===
# Scale eigenvectors by sqrt(eigenvalue * chi2 cutoff) for plotting
chi2_95 = chi2.ppf(0.95, df=2)
arrow_scale = np.sqrt(vals * chi2_95)
origin = best_fit

# Plot arrows
ax.arrow(origin[0], origin[1], vecs[0, 0] * arrow_scale[0], vecs[1, 0] * arrow_scale[0],
         width=0.005, head_width=0.02, color='black', length_includes_head=True)
ax.arrow(origin[0], origin[1], vecs[0, 1] * arrow_scale[1], vecs[1, 1] * arrow_scale[1],
         width=0.005, head_width=0.02, color='black', length_includes_head=True)

# Label arrows
#ax.text(origin[0] + vecs[0, 0] * arrow_scale[0] * 0.6,
#        origin[1] + vecs[1, 0] * arrow_scale[0] * 0.6, 'Stiff direction', color='black')

#ax.text(origin[0] + vecs[0, 1] * arrow_scale[1] * 0.6,
#        origin[1] + vecs[1, 1] * arrow_scale[1] * 0.6, 'Sloppy direction', color='black')

# Final plot settings
ax.set_xlabel("κ")
ax.set_ylabel("k_deg")
#ax.set_title("Fisher Contour with 95% CI")
ax.legend(frameon=False)

plt.tight_layout()
plt.savefig('fisher_contour_95CI.pdf')
plt.show()