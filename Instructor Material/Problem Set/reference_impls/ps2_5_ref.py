"""
PS2.5 reference implementation.

Estimand: p = P(Z > c) for Z ~ N(0,1), c = 2. Closed-form (tier-2): p = 1 - Phi(2),
computed here via erfc (a standard transcendental special function, not a Monte Carlo
estimate) -- executed rather than recalled from memory, per R1a.

Four estimators compared at a FIXED total workload budget n (number of h-evaluations):

  Plain:        Z_i ~ N(0,1) iid, n draws.              p_hat = mean(1(Z_i > c))
  Antithetic:   n/2 iid uniforms U_i -> Z_i = Phi^-1(U_i); antithetic partner is
                Phi^-1(1-U_i) = -Z_i (symmetry of the normal quantile function).
                n/2 pairs, n total evaluations of the indicator.
  Control var.: X = Z_i itself (E[Z]=0, a plain distributional fact), n draws.
                p_hat_cv = mean(1(Z_i>c)) - c_hat*(mean(Z_i) - 0), c_hat estimated
                in-sample via sample covariance/variance (same recipe as PS2.2).
  Importance:   proposal N(c,1) instead of N(0,1); n draws.
                weight w(z) = phi(z;0,1)/phi(z;c,1) = exp(-c*z + c^2/2)
                p_hat_is = mean(w(Z_i) * 1(Z_i>c)), Z_i ~ N(c,1)

Stratified sampling is mentioned only conceptually in the problem text (per WO-M2 §2's
constraint) -- no stratified estimator is implemented here.

As with PS2.2, the ACHIEVED variances are executed-and-logged (tier 3), not read off a
closed-form population formula, even where such a formula could in principle be derived.
"""

import numpy as np
from scipy.special import erfc

C = 2.0
P_TRUE = 0.5 * erfc(C / np.sqrt(2))
N_BUDGET = 5000
R = 2000


def phi_inv(u):
    # standard normal quantile function
    from scipy.special import ndtri
    return ndtri(u)


def plain_estimate(rng, n):
    z = rng.standard_normal(n)
    return np.mean(z > C)


def antithetic_estimate(rng, n):
    m = n // 2
    u = rng.random(m)
    z = phi_inv(u)
    ind = ((z > C).astype(float) + ((-z) > C).astype(float)) / 2.0
    return np.mean(ind)


def control_variate_estimate(rng, n):
    z = rng.standard_normal(n)
    ind = (z > C).astype(float)
    c_hat = np.cov(ind, z, ddof=1)[0, 1] / np.var(z, ddof=1)
    return np.mean(ind) - c_hat * (np.mean(z) - 0.0)


def importance_sampling_estimate(rng, n):
    z = rng.standard_normal(n) + C  # N(C,1)
    w = np.exp(-C * z + C ** 2 / 2.0)
    ind = (z > C).astype(float)
    return np.mean(w * ind)


def variances_at(seed, n=N_BUDGET, r=R):
    rng = np.random.default_rng(seed)
    plain = np.array([plain_estimate(rng, n) for _ in range(r)])
    anti = np.array([antithetic_estimate(rng, n) for _ in range(r)])
    cv = np.array([control_variate_estimate(rng, n) for _ in range(r)])
    is_ = np.array([importance_sampling_estimate(rng, n) for _ in range(r)])
    return {
        "plain_var": plain.var(ddof=1), "plain_mean": plain.mean(),
        "anti_var": anti.var(ddof=1), "anti_mean": anti.mean(),
        "cv_var": cv.var(ddof=1), "cv_mean": cv.mean(),
        "is_var": is_.var(ddof=1), "is_mean": is_.mean(),
    }


if __name__ == "__main__":
    print("P_TRUE = 1 - Phi(2) =", P_TRUE)
    print("\n=== Logged reference run (seed=0) ===")
    out = variances_at(seed=0)
    for k, v in out.items():
        print(f"  {k}: {v}")
    print("  ratio plain/anti:", out["plain_var"] / out["anti_var"])
    print("  ratio plain/cv:", out["plain_var"] / out["cv_var"])
    print("  ratio plain/is:", out["plain_var"] / out["is_var"])

    print("\n=== Calibration: 100 meta-seeds ===")
    ratios = {"anti": [], "cv": [], "is": []}
    for meta_seed in range(100):
        o = variances_at(seed=2000 + meta_seed)
        ratios["anti"].append(o["plain_var"] / o["anti_var"])
        ratios["cv"].append(o["plain_var"] / o["cv_var"])
        ratios["is"].append(o["plain_var"] / o["is_var"])
    for k, v in ratios.items():
        v = np.array(v)
        print(f"  {k}: mean={v.mean():.3f} sd={v.std():.3f} min={v.min():.3f} "
              f"1st pct={np.percentile(v,1):.3f} max={v.max():.3f}")
