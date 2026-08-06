"""
PS2.2 reference implementation.

Target throughout: I = E[e^U], U ~ Uniform(0,1)  =>  I = e - 1  (same estimand as PS2.1;
tier-2, closed form).

Part (a) — antithetic variates on the monotone transform h(u) = e^u.
  Plain:      draw n iid U(0,1); estimator = mean(e^U_i), n evaluations of h.
  Antithetic: draw n/2 iid U(0,1); estimator = mean of (e^U_i + e^(1-U_i))/2 over the
              n/2 pairs -- also n evaluations of h, same total workload.

Part (b) — control variate using X = U itself (E[X] = 1/2, Var(X) = 1/12: plain
  distributional facts about Uniform(0,1); R1a.1 tier-2, no external citation needed).
  ĉ estimated in-sample via sample covariance / sample variance (standard practice);
  estimator = mean(e^U_i) - ĉ * (mean(U_i) - 0.5).

For each technique, we repeat the *whole estimator* R times independently at a fixed
budget n, and use the empirical variance across those R replications as "the achieved
variance" -- this is what the WO calls the tier-3 executed target (not the closed-form
population variance, even though one exists in this special case; see the exploratory
sanity-check numbers in the session notes).

We then run a calibration across many independent meta-seeds (each producing its own
R-replicate variance ratio) to see how much that measured ratio moves around, and use
the low end of that spread to set a conservative, one-sided student-facing threshold.
"""

import numpy as np

I_TRUE = np.e - 1.0
N_BUDGET = 2000   # total h-evaluations budget, shared across all three estimators
R = 2000          # replications used to estimate each estimator's variance


def plain_mc_estimate(rng, n):
    u = rng.random(n)
    return np.mean(np.exp(u))


def antithetic_estimate(rng, n):
    # n must be even; n/2 independent uniforms, n total evaluations of h
    m = n // 2
    u = rng.random(m)
    pair_avgs = (np.exp(u) + np.exp(1 - u)) / 2.0
    return np.mean(pair_avgs)


def control_variate_estimate(rng, n):
    u = rng.random(n)
    hv = np.exp(u)
    c_hat = np.cov(hv, u, ddof=1)[0, 1] / np.var(u, ddof=1)
    return np.mean(hv) - c_hat * (np.mean(u) - 0.5)


def variances_at(seed, n=N_BUDGET, r=R):
    rng = np.random.default_rng(seed)
    plain_vals = np.array([plain_mc_estimate(rng, n) for _ in range(r)])
    anti_vals = np.array([antithetic_estimate(rng, n) for _ in range(r)])
    cv_vals = np.array([control_variate_estimate(rng, n) for _ in range(r)])
    return {
        "plain_var": plain_vals.var(ddof=1),
        "anti_var": anti_vals.var(ddof=1),
        "cv_var": cv_vals.var(ddof=1),
        "plain_mean": plain_vals.mean(),
        "anti_mean": anti_vals.mean(),
        "cv_mean": cv_vals.mean(),
    }


if __name__ == "__main__":
    print("=== Part A: logged reference run (seed=0) ===")
    out = variances_at(seed=0)
    for k, v in out.items():
        print(f"  {k}: {v}")
    ratio_anti = out["plain_var"] / out["anti_var"]
    ratio_cv = out["plain_var"] / out["cv_var"]
    print("  variance-reduction ratio (plain/antithetic):", ratio_anti)
    print("  variance-reduction ratio (plain/control-variate):", ratio_cv)

    print("\n=== Part B: calibration across 100 meta-seeds ===")
    ratios_anti = []
    ratios_cv = []
    for meta_seed in range(100):
        o = variances_at(seed=1000 + meta_seed)
        ratios_anti.append(o["plain_var"] / o["anti_var"])
        ratios_cv.append(o["plain_var"] / o["cv_var"])
    ratios_anti = np.array(ratios_anti)
    ratios_cv = np.array(ratios_cv)
    print("antithetic ratio: mean=", ratios_anti.mean(), "sd=", ratios_anti.std(),
          "min=", ratios_anti.min(), "1st pct=", np.percentile(ratios_anti, 1))
    print("control-variate ratio: mean=", ratios_cv.mean(), "sd=", ratios_cv.std(),
          "min=", ratios_cv.min(), "1st pct=", np.percentile(ratios_cv, 1))


def calibrate_with_R(r, n_meta=150, n=N_BUDGET):
    ratios_anti = []
    ratios_cv = []
    for meta_seed in range(n_meta):
        o = variances_at(seed=5000 + meta_seed, n=n, r=r)
        ratios_anti.append(o["plain_var"] / o["anti_var"])
        ratios_cv.append(o["plain_var"] / o["cv_var"])
    ratios_anti = np.array(ratios_anti)
    ratios_cv = np.array(ratios_cv)
    print(f"--- R={r} ---")
    print("antithetic: mean=", ratios_anti.mean(), "sd=", ratios_anti.std(),
          "min=", ratios_anti.min(), "1st pct=", np.percentile(ratios_anti, 1))
    print("control-variate: mean=", ratios_cv.mean(), "sd=", ratios_cv.std(),
          "min=", ratios_cv.min(), "1st pct=", np.percentile(ratios_cv, 1))
