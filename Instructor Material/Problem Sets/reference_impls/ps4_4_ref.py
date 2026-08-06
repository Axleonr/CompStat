"""
PS4.4 reference implementation.
Data-policy note: the source exercise (R&C 5.10) uses the real log(deaths) data
from the MASS package. Per policy 4.3 and WO-M4 Sec.5's escalation note, that
dataset is NOT reproduced (MASS's ldeaths-family series runs 72 monthly values,
over the ~50-value inline threshold, and it is not a persistent/open/small URL
source) -- a synthetic two-component Gaussian mixture is substituted instead,
generated with a fully specified generative process and seed. Flagged in the
module Flags section, not silently substituted.

Model: full two-component Gaussian mixture -- unknown weight pi, means mu1/mu2,
       variances sigma1^2/sigma2^2 (all five parameters estimated by EM; contrast
       with PS4.1/PS4.2's known-weight-and-variance model and PS4.3's
       known-components model).
Part A: EM from a "good" (spread, data-informed) initialization -- monotonicity
        check on the log-likelihood sequence.
Part B: cross-check the converged (mu1, mu2) against a grid search over
        (mu1, mu2) with the other three parameters fixed at their EM estimates
        (the same grid technique as PS4.1/PS4.2, applied here for internal
        consistency).
Part C: EM from a deliberately bad (exact-tie) initialization -- both components
        start identical -- producing a genuine, worse local optimum (here: total
        collapse to a single-component fit).
Run with: python3 ps4_4_ref.py
"""
import numpy as np

pi_true, mu1_true, sigma1_true = 0.25, 0.0, 1.0
mu2_true, sigma2_true = 4.0, np.sqrt(2.0)
n = 150


def gen_full_mixture(seed, n, pi_true, mu1_true, sigma1_true, mu2_true, sigma2_true):
    rng = np.random.default_rng(seed)
    z = rng.random(n) < pi_true
    x = np.where(z, rng.normal(mu1_true, sigma1_true, n), rng.normal(mu2_true, sigma2_true, n))
    return x, z


x, z = gen_full_mixture(seed=3, n=n, pi_true=pi_true, mu1_true=mu1_true, sigma1_true=sigma1_true,
                         mu2_true=mu2_true, sigma2_true=sigma2_true)
print(f"Synthetic dataset: n={n}, true n1={z.sum()}, true n2={n-z.sum()}, "
      f"range=[{x.min():.3f}, {x.max():.3f}]")


def dnorm(xv, mu, sig2):
    return np.exp(-0.5 * (xv - mu) ** 2 / sig2) / np.sqrt(2 * np.pi * sig2)


def loglik(x, pi_, mu1, sig1_2, mu2, sig2_2):
    f = pi_ * dnorm(x, mu1, sig1_2) + (1 - pi_) * dnorm(x, mu2, sig2_2)
    return np.sum(np.log(f + 1e-300))


def em_full(x, pi0, mu1_0, sig1_2_0, mu2_0, sig2_2_0, n_iter=300, tol=1e-10):
    pi_, mu1, sig1_2, mu2, sig2_2 = pi0, mu1_0, sig1_2_0, mu2_0, sig2_2_0
    ll_hist = [loglik(x, pi_, mu1, sig1_2, mu2, sig2_2)]
    for it in range(n_iter):
        f1 = pi_ * dnorm(x, mu1, sig1_2)
        f2 = (1 - pi_) * dnorm(x, mu2, sig2_2)
        r = f1 / (f1 + f2 + 1e-300)
        Neff1, Neff2 = r.sum(), (1 - r).sum()
        mu1_new = np.sum(r * x) / Neff1
        mu2_new = np.sum((1 - r) * x) / Neff2
        sig1_2_new = np.sum(r * (x - mu1_new) ** 2) / Neff1
        sig2_2_new = np.sum((1 - r) * (x - mu2_new) ** 2) / Neff2
        pi_new = Neff1 / len(x)
        pi_, mu1, sig1_2, mu2, sig2_2 = pi_new, mu1_new, sig1_2_new, mu2_new, sig2_2_new
        ll = loglik(x, pi_, mu1, sig1_2, mu2, sig2_2)
        ll_hist.append(ll)
        if abs(ll_hist[-1] - ll_hist[-2]) < tol:
            break
    return (pi_, mu1, sig1_2, mu2, sig2_2), ll_hist


print()
print("=== Part A: EM from a good initialization ===")
good_init = dict(pi0=0.5, mu1_0=x.min(), sig1_2_0=1.0, mu2_0=x.max(), sig2_2_0=1.0)
params_good, ll_good = em_full(x, **good_init)
print("init:", good_init)
print("converged (pi, mu1, sig1^2, mu2, sig2^2):", tuple(round(p, 4) for p in params_good))
print("n_iters:", len(ll_good) - 1, " final loglik:", round(ll_good[-1], 4))

diffs = np.diff(ll_good)
print("monotonicity check: min per-iteration increment =", diffs.min(),
      " (any increment < -1e-8? ", bool(np.any(diffs < -1e-8)), ")")

print()
print("=== Part B: cross-check (mu1,mu2) via grid search at EM's other estimates ===")
pi_hat, mu1_hat, sig1_2_hat, mu2_hat, sig2_2_hat = params_good
mu_grid = np.linspace(-4, 8, 241)
best = None
for m1 in mu_grid:
    for m2 in mu_grid:
        val = loglik(x, pi_hat, m1, sig1_2_hat, m2, sig2_2_hat)
        if best is None or val > best[2]:
            best = (m1, m2, val)
print("grid-search optimum (mu1, mu2 | other params fixed at EM values):", (round(best[0], 3), round(best[1], 3)))
print("EM (mu1, mu2):", (round(mu1_hat, 3), round(mu2_hat, 3)))
print("||diff|| =", round(np.hypot(best[0] - mu1_hat, best[1] - mu2_hat), 4), "(within one grid cell, 0.05 spacing)")

print()
print("=== Part C: bad (exact-tie) initialization -> inferior local optimum ===")
bad_init = dict(pi0=0.5, mu1_0=x.mean(), sig1_2_0=x.var(), mu2_0=x.mean(), sig2_2_0=x.var())
params_bad, ll_bad = em_full(x, **bad_init)
print("init:", bad_init)
print("converged (pi, mu1, sig1^2, mu2, sig2^2):", tuple(round(p, 4) for p in params_bad))
print("n_iters:", len(ll_bad) - 1, " final loglik:", round(ll_bad[-1], 4))
print("gap vs good-init solution (good - bad):", round(ll_good[-1] - ll_bad[-1], 4))
diffs_bad = np.diff(ll_bad)
print("bad-run monotonicity check: min per-iteration increment =", diffs_bad.min())
