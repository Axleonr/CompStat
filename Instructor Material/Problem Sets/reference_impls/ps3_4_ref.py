"""
PS3.4 reference implementation.
Heavy-tail (infinite-variance) bootstrap failure exhibit: standard Cauchy(0,1)
(infinite variance -- in fact the sample mean of n iid Cauchy draws has EXACTLY
the same Cauchy(0,1) distribution regardless of n, a citable tier-2 distributional
fact) contrasted with standard Normal(0,1) (finite variance, ordinary sqrt(n) scaling).

Two exhibits:
  (A) IQR-scaling: across M independent replications of size n, the spread (IQR,
      a robust measure since Cauchy's SD is undefined) of the sample MEAN itself
      should shrink like 1/sqrt(n) for Normal but NOT shrink for Cauchy.
  (B) Bootstrap-distribution instability: bootstrap the mean (from primitives) on
      3 different original samples of the same n for each population; Normal's
      three bootstrap SEs should be mutually consistent; Cauchy's should not be
      (and can be enormous / wildly different from run to run).
"""
import numpy as np


def iqr(x):
    q1, q3 = np.percentile(x, [25, 75])
    return q3 - q1


def exhibit_A(n_grid, M, seed):
    rng = np.random.default_rng(seed)
    results = {"normal": {}, "cauchy": {}}
    for n in n_grid:
        normal_means = np.array([rng.normal(0, 1, size=n).mean() for _ in range(M)])
        cauchy_means = np.array([rng.standard_cauchy(size=n).mean() for _ in range(M)])
        results["normal"][n] = iqr(normal_means)
        results["cauchy"][n] = iqr(cauchy_means)
    return results


def nonparam_bootstrap_mean(data, r, seed):
    rng = np.random.default_rng(seed)
    n = len(data)
    idx = rng.integers(0, n, size=(r, n))
    return data[idx].mean(axis=1)


def exhibit_B(n, r, seed):
    rng = np.random.default_rng(seed)
    normal_boot_ses = []
    cauchy_boot_ses = []
    for k in range(3):
        norm_sample = rng.normal(0, 1, size=n)
        cauchy_sample = rng.standard_cauchy(size=n)
        nb = nonparam_bootstrap_mean(norm_sample, r, seed=1000 + k)
        cb = nonparam_bootstrap_mean(cauchy_sample, r, seed=2000 + k)
        normal_boot_ses.append(nb.std(ddof=1))
        # use IQR for cauchy bootstrap distribution too (SD can be dominated by rare huge draws)
        cauchy_boot_ses.append((iqr(cb), cb.std(ddof=1)))
    return normal_boot_ses, cauchy_boot_ses


if __name__ == "__main__":
    n_grid = [20, 100, 500]
    print("=== EXHIBIT A: IQR of the sample mean vs n (M=300, primary seed=555) ===")
    res = exhibit_A(n_grid, M=300, seed=555)
    for pop in ["normal", "cauchy"]:
        print(f"  {pop}: " + ", ".join(f"n={n}: IQR={res[pop][n]:.4f}" for n in n_grid))
    ratio_normal = res["normal"][20] / res["normal"][500]
    ratio_cauchy = res["cauchy"][20] / res["cauchy"][500]
    print(f"  Normal IQR ratio (n=20 / n=500) = {ratio_normal:.3f}  (theory: sqrt(500/20)={np.sqrt(500/20):.3f})")
    print(f"  Cauchy IQR ratio (n=20 / n=500) = {ratio_cauchy:.3f}  (theory: 1.0, no shrinkage)")

    print("\n=== CALIBRATION: exhibit A across 6 more seeds ===")
    ratios_normal, ratios_cauchy = [], []
    for sd in [1, 2, 3, 4, 5, 6]:
        r2 = exhibit_A(n_grid, M=300, seed=sd * 111)
        ratios_normal.append(r2["normal"][20] / r2["normal"][500])
        ratios_cauchy.append(r2["cauchy"][20] / r2["cauchy"][500])
        print(f"  seed={sd*111}: normal ratio={ratios_normal[-1]:.3f}  cauchy ratio={ratios_cauchy[-1]:.3f}")
    print("  normal ratio range:", min(ratios_normal), max(ratios_normal))
    print("  cauchy ratio range:", min(ratios_cauchy), max(ratios_cauchy))

    print("\n=== EXHIBIT B: bootstrap SE consistency across 3 original samples (n=50, r=3000) ===")
    normal_ses, cauchy_ses = exhibit_B(n=50, r=3000, seed=777)
    print("  Normal bootstrap SEs across 3 original samples:", [f"{s:.4f}" for s in normal_ses])
    print("  Cauchy bootstrap (IQR, SD) across 3 original samples:", [(f"{a:.3f}", f"{b:.3f}") for a, b in cauchy_ses])
    normal_cv = np.std(normal_ses, ddof=1) / np.mean(normal_ses)
    cauchy_iqrs = [a for a, b in cauchy_ses]
    cauchy_cv = np.std(cauchy_iqrs, ddof=1) / np.mean(cauchy_iqrs)
    print(f"  Normal bootstrap-SE coefficient of variation across the 3 samples: {normal_cv:.4f}")
    print(f"  Cauchy bootstrap-IQR coefficient of variation across the 3 samples: {cauchy_cv:.4f}")

    print("\n=== CALIBRATION: exhibit B across 5 more seeds ===")
    normal_cvs, cauchy_cvs = [], []
    for sd in [11, 22, 33, 44, 55]:
        ns, cs = exhibit_B(n=50, r=3000, seed=sd)
        ncv = np.std(ns, ddof=1) / np.mean(ns)
        ciqrs = [a for a, b in cs]
        ccv = np.std(ciqrs, ddof=1) / np.mean(ciqrs)
        normal_cvs.append(ncv)
        cauchy_cvs.append(ccv)
        print(f"  seed={sd}: normal_cv={ncv:.4f}  cauchy_cv={ccv:.4f}")
    print("  normal_cv range:", min(normal_cvs), max(normal_cvs))
    print("  cauchy_cv range:", min(cauchy_cvs), max(cauchy_cvs))
