"""
PS1.1 reference implementation — LCG from primitives + two uniformity tests.
Generator: X_{n+1} = (a * X_n + c) mod m, a=16807, c=0, m=2^31-1 (stated in problem).
Seed (stated to students): X_0 = 123456789.
Draws: n = 10,000 (X_1 ... X_10000), U_i = X_i / m.

Test 1: chi-square goodness-of-fit on k=10 equal-width bins over [0,1), df = k-1 = 9.
Test 2: lag-1 serial correlation test using Bartlett's formula (Var(r_1) ~= 1/n under H0).

This script is executed once per seed for the primary logged run, then re-run under
3 additional seeds as an internal calibration check (not shown to students; establishes
that the tolerance holds generically for a correctly-implemented LCG, not just by luck
on one seed).
"""
import numpy as np
from scipy import stats

def lcg_sequence(seed, n, a=16807, c=0, m=2**31 - 1):
    x = seed
    xs = []
    for _ in range(n):
        x = (a * x + c) % m
        xs.append(x)
    return np.array(xs, dtype=np.float64) / m

def chi_square_test(u, k=10):
    edges = np.linspace(0, 1, k + 1)
    counts, _ = np.histogram(u, bins=edges)
    n = len(u)
    expected = n / k
    chi2_stat = np.sum((counts - expected) ** 2 / expected)
    df = k - 1
    p_value = 1 - stats.chi2.cdf(chi2_stat, df)
    crit_95 = stats.chi2.ppf(0.95, df)
    return chi2_stat, df, p_value, crit_95, counts

def serial_correlation_test(u):
    n = len(u)
    x = u[:-1]
    y = u[1:]
    r1 = np.corrcoef(x, y)[0, 1]
    se = 1.0 / np.sqrt(n)  # Bartlett's formula, white-noise null
    z = r1 / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return r1, se, z, p_value

def run(seed, n=10000, label=""):
    u = lcg_sequence(seed, n)
    chi2_stat, df, chi2_p, crit_95, counts = chi_square_test(u, k=10)
    r1, se, z, corr_p = serial_correlation_test(u)
    print(f"--- {label} seed={seed} n={n} ---")
    print(f"first 5 U: {u[:5]}")
    print(f"min U={u.min():.6f} max U={u.max():.6f} mean U={u.mean():.6f} (expect ~0.5)")
    print(f"chi2_stat={chi2_stat:.4f}  df={df}  crit_95={crit_95:.4f}  p={chi2_p:.4f}")
    print(f"bin counts: {counts.tolist()}  (expected {n/10} each)")
    print(f"serial r1={r1:.6f}  SE={se:.6f}  z={z:.4f}  p={corr_p:.4f}")
    print()
    return dict(chi2_stat=chi2_stat, chi2_p=chi2_p, crit_95=crit_95, r1=r1, z=z, corr_p=corr_p)

if __name__ == "__main__":
    # Primary logged run (the seed stated to students)
    primary = run(123456789, 10000, label="PRIMARY (stated seed)")

    # Degenerate-seed demonstration for the period/seed-dependence note
    x = 0
    a, c, m = 16807, 0, 2**31 - 1
    degenerate = [x]
    for _ in range(5):
        x = (a * x + c) % m
        degenerate.append(x)
    print(f"--- seed=0 degeneracy check --- sequence: {degenerate}")
    print()

    # Calibration: 3 additional seeds, same n, to confirm the tolerance band is not a
    # one-seed fluke (drafter-side check; not part of the student-facing target).
    calib_seeds = [987654321, 42, 271828183]
    calib_results = [run(s, 10000, label=f"CALIBRATION") for s in calib_seeds]

    print("=== Calibration summary ===")
    print("chi2_stat range:", [round(r['chi2_stat'], 3) for r in [primary] + calib_results])
    print("chi2_p range:", [round(r['chi2_p'], 4) for r in [primary] + calib_results])
    print("|z| range (serial corr):", [round(abs(r['z']), 4) for r in [primary] + calib_results])
