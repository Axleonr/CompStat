"""
PS4.3 reference implementation.
Model: two-component mixture with KNOWN component densities g = N(0,1) and
       h = N(3, 2^2), unknown mixing weight theta = P(component g).
       n=25, true theta=0.3 (required seed=7 -- see validation-log Notes for why).
Part A: EM (closed-form E-step responsibility + M-step average) run from five
        different starting values, confirming they all reach the same fixed point.
Part B: grid-search cross-check of the 1-D profile likelihood over theta (R1.4-style
        library-free oracle).
Part C: 20-seed calibration of |theta_hat - theta_true| to characterize small-n
        sampling variability honestly (informs the tolerance statement).
Run with: python3 ps4_3_ref.py
"""
import numpy as np
from scipy.stats import norm

g_params = (0.0, 1.0)
h_params = (3.0, 2.0)
n = 25
theta_true = 0.3


def gen_data(seed, n, theta_true, g_params, h_params):
    rng = np.random.default_rng(seed)
    z = rng.random(n) < theta_true
    x = np.where(z, rng.normal(g_params[0], g_params[1], n), rng.normal(h_params[0], h_params[1], n))
    return x, z


def dens_g(xv):
    return norm.pdf(xv, g_params[0], g_params[1])


def dens_h(xv):
    return norm.pdf(xv, h_params[0], h_params[1])


def em_fixed_weight(x, theta0, n_iter=500, tol=1e-10):
    theta = theta0
    history = [theta]
    for it in range(n_iter):
        gvals, hvals = dens_g(x), dens_h(x)
        num = theta * gvals
        denom = theta * gvals + (1 - theta) * hvals
        resp = num / denom
        theta_new = resp.mean()
        history.append(theta_new)
        if abs(theta_new - theta) < tol:
            theta = theta_new
            break
        theta = theta_new
    return theta, history


print("=== Part A: EM from multiple starting values (required seed=7) ===")
x, z = gen_data(seed=7, n=n, theta_true=theta_true, g_params=g_params, h_params=h_params)
print("data:", np.round(np.sort(x), 3))
print("empirical fraction truly from g:", z.mean())

final_thetas = []
for theta0 in [0.1, 0.3, 0.5, 0.7, 0.9]:
    theta_hat, hist = em_fixed_weight(x, theta0)
    final_thetas.append(theta_hat)
    print(f"start theta0={theta0}: converged theta_hat={theta_hat:.6f} in {len(hist)-1} iters")

print("max pairwise disagreement among the 5 starts:",
      max(final_thetas) - min(final_thetas))

print()
print("=== Part B: grid-search cross-check of the profile likelihood ===")


def negloglik_theta(theta, x):
    gvals, hvals = dens_g(x), dens_h(x)
    f = theta * gvals + (1 - theta) * hvals
    return -np.sum(np.log(f + 1e-300))


grid = np.linspace(0.001, 0.999, 9990)
vals = [negloglik_theta(t, x) for t in grid]
best_idx = int(np.argmin(vals))
print("grid-search MLE of theta:", grid[best_idx], " negloglik:", vals[best_idx])
print("EM final (theta0=0.5) vs grid-search MLE, |diff| =", abs(final_thetas[2] - grid[best_idx]))

print()
print("=== Part C: 20-seed calibration of sampling variability (n=25) ===")
devs = []
for seed in range(1, 21):
    x_, _ = gen_data(seed=seed, n=25, theta_true=0.3, g_params=g_params, h_params=h_params)
    theta_hat_, _ = em_fixed_weight(x_, 0.5)
    devs.append(abs(theta_hat_ - 0.3))
devs = np.array(devs)
print(f"mean |theta_hat-0.3| over 20 seeds: {devs.mean():.4f}, sd: {devs.std():.4f}, "
      f"min: {devs.min():.4f}, max: {devs.max():.4f}")
print("(this is why the numeric known-truth tolerance below requires the exact seed=7 "
      "dataset rather than an arbitrary student seed -- see validation log Notes)")
