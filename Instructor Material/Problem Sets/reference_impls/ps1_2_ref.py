"""
PS1.2 reference implementation.

Part (a) — Pareto power transform (closed-form inverse CDF), tier 1/2 (citable
identity + citable Pareto moments). This is a drafter-side sanity check on the
chosen tolerance band; NOT a required validation-log entry (WO tier cell: (a) is
tier 1/2, only (b) is tier 3).

Part (b) — standard normal via numerical inversion of Phi (bisection), tier 3.
This IS logged: seed, code, target, value obtained, tolerance.
"""
import numpy as np
from scipy.stats import norm

# ---------- Part (a): Pareto power transform (sanity check only) ----------
def pareto_sample(u, xm=1.0, alpha=6.0):
    return xm * u ** (-1.0 / alpha)

def part_a_check(seed, n=5000, xm=1.0, alpha=6.0):
    rng = np.random.default_rng(seed)
    u = rng.uniform(0, 1, n)
    x = pareto_sample(u, xm, alpha)
    true_mean = alpha * xm / (alpha - 1)
    true_var = (xm ** 2) * alpha / ((alpha - 1) ** 2 * (alpha - 2))
    se_mean = np.sqrt(true_var / n)
    sample_mean = x.mean()
    sample_var = x.var(ddof=1)
    print(f"[Part a, seed={seed}] true mean={true_mean:.4f} var={true_var:.4f} sd={np.sqrt(true_var):.4f}")
    print(f"  sample mean={sample_mean:.4f}  (3SE band: {true_mean-3*se_mean:.4f} to {true_mean+3*se_mean:.4f})  SE={se_mean:.4f}")
    print(f"  sample var ={sample_var:.4f}")
    print(f"  within 3SE: {abs(sample_mean-true_mean) <= 3*se_mean}")
    print()

# ---------- Part (b): standard normal via numerical inversion (LOGGED) ----------
def phi(x):
    return norm.cdf(x)  # library CDF eval permitted; root-finding loop below is the taught algorithm

def bisection_invert(u, lo=-10.0, hi=10.0, tol=1e-10, max_iter=200):
    flo, fhi = phi(lo) - u, phi(hi) - u
    for _ in range(max_iter):
        mid = 0.5 * (lo + hi)
        fmid = phi(mid) - u
        if abs(fmid) < tol or (hi - lo) < tol:
            return mid
        if (fmid > 0) == (flo > 0):
            lo, flo = mid, fmid
        else:
            hi, fhi = mid, fmid
    return 0.5 * (lo + hi)

def part_b_run(seed, n=5000, label=""):
    rng = np.random.default_rng(seed)
    u = rng.uniform(0, 1, n)
    x = np.array([bisection_invert(ui) for ui in u])
    sample_mean = x.mean()
    sample_var = x.var(ddof=1)
    se_mean = np.sqrt(1.0 / n)          # true variance = 1
    se_var = np.sqrt(2.0 / n)           # approx SE of sample variance for normal data
    print(f"[Part b, {label} seed={seed}, n={n}]")
    print(f"  sample mean={sample_mean:.5f}  (target 0, 3SE={3*se_mean:.5f})")
    print(f"  sample var ={sample_var:.5f}  (target 1, 3SE={3*se_var:.5f})")
    print(f"  |mean| <= 3SE: {abs(sample_mean) <= 3*se_mean}   |var-1| <= 3SE: {abs(sample_var-1) <= 3*se_var}")
    # cross-check the numerical inverse against the library's own ppf (independent check on the algorithm)
    max_abs_err_vs_ppf = np.max(np.abs(x - norm.ppf(u)))
    print(f"  max |bisection_x - norm.ppf(u)| over sample = {max_abs_err_vs_ppf:.2e}")
    print()
    return sample_mean, sample_var, max_abs_err_vs_ppf

if __name__ == "__main__":
    print("=== Part (a) sanity check (tier 1/2, not logged) ===")
    for s in [2024, 7, 555]:
        part_a_check(s)

    print("=== Part (b) primary logged run ===")
    part_b_run(2024, 5000, label="PRIMARY")

    print("=== Part (b) calibration (3 more seeds) ===")
    for s in [7, 555, 90210]:
        part_b_run(s, 5000, label="CALIBRATION")
