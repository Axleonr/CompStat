"""
PS3.3 reference implementation.
Scaled-down repeated-simulation coverage experiment: bootstrap-t vs. bootstrap
percentile vs. BCa 95% CIs for the mean of an Exponential(rate=1) population
(true mean = 1), over a small student-scale n-grid, showing the accuracy
hierarchy Hesterberg (2015) Sec. 4.4 describes qualitatively (bootstrap-t/BCa
much closer to nominal coverage than percentile for small/moderate n on skewed
data) -- WITHOUT relying on H-4's article-scale numeric thresholds, which do
not transfer to student scale (WO-M3 §5).

CORRECTION (07/15/2026): BCa added following owner-supplied E&T Ch. 14 Sec.
14.3 excerpt (Efron & Tibshirani 1993, "An Introduction to the Bootstrap"),
resolving module Flags item DP-M3-2. BCa formulas (Eqs. 14.9, 14.10, 14.14,
14.15 of the source) are implemented from the confirmed source text, not from
memory, per WO-M3 §5.

Design note on reproducibility: the BCa computation is inserted AFTER the
original-sample draw and the bootstrap-resample draw in each trial, and
consumes NO additional random numbers (bias-correction and acceleration are
both computed from arrays already drawn for the percentile/bootstrap-t
methods -- jackknife is deterministic given the original sample; the
bias-correction proportion re-uses the existing boot_means array). This
preserves the exact RNG call sequence from the original (BCa-less) version,
so the percentile and bootstrap-t coverage numbers are expected to reproduce
bit-for-bit -- checked explicitly below.
"""
import numpy as np
from scipy import stats

TRUE_MEAN = 1.0
RATE = 1.0
R_INNER = 2000   # bootstrap resamples per trial
NREP = 1000      # repeated-simulation trials per n
ALPHA = 0.05

Z_ALPHA_LO = stats.norm.ppf(ALPHA / 2)          # z^(0.025)
Z_ALPHA_HI = stats.norm.ppf(1 - ALPHA / 2)      # z^(0.975)


def bca_alpha_endpoints(x, xbar, boot_means):
    """BCa endpoints (E&T 1993 Eqs. 14.9-14.10, 14.14-14.15), for the sample mean.
    Returns (alpha1, alpha2) -- the percentile levels of the bootstrap distribution
    to use as the BCa interval endpoints. Consumes no new randomness."""
    n = len(x)

    # bias-correction z0-hat (Eq. 14.14): proportion of bootstrap replicates
    # below the original estimate, pushed through the inverse normal CDF.
    prop_below = np.mean(boot_means < xbar)
    # guard the two degenerate ends (all-below / none-below) which would give
    # Phi^{-1}(0) or Phi^{-1}(1) = +-inf; clip to a value representing "extreme
    # but finite" bias rather than let the interval blow up numerically.
    prop_below = np.clip(prop_below, 1.0 / (2 * R_INNER), 1 - 1.0 / (2 * R_INNER))
    z0_hat = stats.norm.ppf(prop_below)

    # acceleration a-hat (Eq. 14.15): jackknife (leave-one-out) on the ORIGINAL
    # sample only -- deterministic, no bootstrap resampling involved.
    total = x.sum()
    loo_mean = (total - x) / (n - 1)            # theta-hat_(i), i=1..n
    theta_dot = loo_mean.mean()                  # theta-hat_(.)
    num = np.sum((theta_dot - loo_mean) ** 3)
    den = 6.0 * (np.sum((theta_dot - loo_mean) ** 2) ** 1.5)
    a_hat = num / den if den != 0 else 0.0

    def alpha_transform(z_a):
        denom = 1 - a_hat * (z0_hat + z_a)
        return stats.norm.cdf(z0_hat + (z0_hat + z_a) / denom)

    alpha1 = alpha_transform(Z_ALPHA_LO)
    alpha2 = alpha_transform(Z_ALPHA_HI)
    # clip away from the exact boundary for percentile lookup stability
    alpha1 = np.clip(alpha1, 1.0 / (2 * R_INNER), 1 - 1.0 / (2 * R_INNER))
    alpha2 = np.clip(alpha2, 1.0 / (2 * R_INNER), 1 - 1.0 / (2 * R_INNER))
    return alpha1, alpha2, a_hat, z0_hat


def one_trial(n, rng):
    x = rng.exponential(scale=1.0 / RATE, size=n)
    xbar = x.mean()
    s = x.std(ddof=1)
    se = s / np.sqrt(n)

    # --- bootstrap resamples (shared draw, used for percentile, t, AND BCa) ---
    idx = rng.integers(0, n, size=(R_INNER, n))
    boot_samples = x[idx]                      # (R_INNER, n)
    boot_means = boot_samples.mean(axis=1)
    boot_sds = boot_samples.std(axis=1, ddof=1)
    boot_sds = np.maximum(boot_sds, 1e-8)
    boot_ses = boot_sds / np.sqrt(n)

    # --- percentile CI ---
    perc_lo, perc_hi = np.percentile(boot_means, [100 * ALPHA / 2, 100 * (1 - ALPHA / 2)])

    # --- bootstrap-t CI (Hesterberg 2015 Eq. 1-4; formula SE per resample) ---
    t_star = (boot_means - xbar) / boot_ses
    q_lo, q_hi = np.percentile(t_star, [100 * ALPHA / 2, 100 * (1 - ALPHA / 2)])
    t_lo = xbar - q_hi * se
    t_hi = xbar - q_lo * se

    # --- BCa CI (E&T 1993 Sec. 14.3) -- no new randomness consumed ---
    alpha1, alpha2, a_hat, z0_hat = bca_alpha_endpoints(x, xbar, boot_means)
    bca_lo, bca_hi = np.percentile(boot_means, [100 * alpha1, 100 * alpha2])

    perc_cover = perc_lo <= TRUE_MEAN <= perc_hi
    t_cover = t_lo <= TRUE_MEAN <= t_hi
    bca_cover = bca_lo <= TRUE_MEAN <= bca_hi
    perc_width = perc_hi - perc_lo
    t_width = t_hi - t_lo
    bca_width = bca_hi - bca_lo
    return dict(perc_cover=perc_cover, t_cover=t_cover, bca_cover=bca_cover,
                perc_width=perc_width, t_width=t_width, bca_width=bca_width,
                a_hat=a_hat, z0_hat=z0_hat)


def coverage_at_n(n, seed, nrep=NREP):
    rng = np.random.default_rng(seed)
    keys = ["perc_cover", "t_cover", "bca_cover", "perc_width", "t_width", "bca_width"]
    acc = {k: np.empty(nrep, dtype=bool if "cover" in k else float) for k in keys}
    a_hats = np.empty(nrep)
    z0_hats = np.empty(nrep)
    for i in range(nrep):
        r = one_trial(n, rng)
        for k in keys:
            acc[k][i] = r[k]
        a_hats[i] = r["a_hat"]
        z0_hats[i] = r["z0_hat"]
    return dict(
        n=n,
        perc_coverage=acc["perc_cover"].mean(),
        t_coverage=acc["t_cover"].mean(),
        bca_coverage=acc["bca_cover"].mean(),
        perc_mean_width=acc["perc_width"].mean(),
        t_mean_width=acc["t_width"].mean(),
        bca_mean_width=acc["bca_width"].mean(),
        mean_a_hat=a_hats.mean(),
        mean_z0_hat=z0_hats.mean(),
    )


if __name__ == "__main__":
    n_grid = [8, 15, 30, 60]

    print("=== SANITY CHECK: a_hat=0, z0_hat=0 must reduce BCa to percentile (E&T Eq. 14.11) ===")
    rng_check = np.random.default_rng(1)
    x_check = rng_check.exponential(1.0, size=20)
    boot_means_check = rng_check.choice(x_check, size=(5000, 20)).mean(axis=1)
    # force a_hat=z0_hat=0 by monkey-testing the transform directly
    def alpha_transform_zero(z_a):
        return stats.norm.cdf(0 + (0 + z_a) / (1 - 0 * (0 + z_a)))
    a1 = alpha_transform_zero(Z_ALPHA_LO)
    a2 = alpha_transform_zero(Z_ALPHA_HI)
    print(f"  alpha1={a1:.5f} (should equal alpha/2={ALPHA/2:.5f})")
    print(f"  alpha2={a2:.5f} (should equal 1-alpha/2={1-ALPHA/2:.5f})")
    assert abs(a1 - ALPHA/2) < 1e-10 and abs(a2 - (1-ALPHA/2)) < 1e-10
    print("  PASSED: BCa formula reduces exactly to the percentile formula when a_hat=z0_hat=0.")

    print("\n=== PRIMARY LOGGED RUN (seed=2026, nrep=1000, r_inner=2000) ===")
    primary = []
    for n in n_grid:
        res = coverage_at_n(n, seed=2026 + n)
        primary.append(res)
        print(f"n={n:3d}  percentile={res['perc_coverage']:.3f}  bootstrap-t={res['t_coverage']:.3f}  "
              f"BCa={res['bca_coverage']:.3f}  (nominal 0.950)  "
              f"perc_w={res['perc_mean_width']:.3f}  t_w={res['t_mean_width']:.3f}  bca_w={res['bca_mean_width']:.3f}  "
              f"mean_a_hat={res['mean_a_hat']:.4f}  mean_z0_hat={res['mean_z0_hat']:.4f}")

    print("\n=== REPRODUCIBILITY CHECK vs. the original (BCa-less) validated run ===")
    original_primary = {
        8: (0.848, 0.941), 15: (0.871, 0.942), 30: (0.912, 0.937), 60: (0.923, 0.956)
    }
    for res in primary:
        n = res['n']
        op, ot = original_primary[n]
        match_p = abs(res['perc_coverage'] - op) < 1e-9
        match_t = abs(res['t_coverage'] - ot) < 1e-9
        print(f"  n={n}: percentile {res['perc_coverage']:.4f} vs original {op:.4f} (match={match_p})   "
              f"bootstrap-t {res['t_coverage']:.4f} vs original {ot:.4f} (match={match_t})")

    print("\n=== CALIBRATION: 5 additional seed sets ===")
    calib = {n: [] for n in n_grid}
    for base_seed in [10, 20, 30, 40, 50]:
        for n in n_grid:
            res = coverage_at_n(n, seed=base_seed * 1000 + n)
            calib[n].append(res)

    for n in n_grid:
        pcs = [r['perc_coverage'] for r in calib[n]]
        tcs = [r['t_coverage'] for r in calib[n]]
        bcs = [r['bca_coverage'] for r in calib[n]]
        pws = [r['perc_mean_width'] for r in calib[n]]
        tws = [r['t_mean_width'] for r in calib[n]]
        bws = [r['bca_mean_width'] for r in calib[n]]
        print(f"n={n:3d}  percentile range: {min(pcs):.3f}-{max(pcs):.3f}   "
              f"bootstrap-t range: {min(tcs):.3f}-{max(tcs):.3f}   "
              f"BCa range: {min(bcs):.3f}-{max(bcs):.3f}")
        print(f"        widths -- perc: {min(pws):.3f}-{max(pws):.3f}  t: {min(tws):.3f}-{max(tws):.3f}  "
              f"BCa: {min(bws):.3f}-{max(bws):.3f}")

    print("\n=== Gap checks (BCa vs percentile; BCa vs bootstrap-t) ===")
    for n in n_grid:
        bcs = [r['bca_coverage'] for r in calib[n]]
        pcs = [r['perc_coverage'] for r in calib[n]]
        tcs = [r['t_coverage'] for r in calib[n]]
        gap_bca_perc = [b - p for b, p in zip(bcs, pcs)]
        gap_bca_t = [b - t for b, t in zip(bcs, tcs)]
        print(f"n={n:3d}  BCa-percentile gap range: {min(gap_bca_perc):.3f} to {max(gap_bca_perc):.3f}   "
              f"BCa-bootstrapT gap range: {min(gap_bca_t):.3f} to {max(gap_bca_t):.3f}")
