"""
PS9.2 reference implementation.
Silverman (1986) rule-of-thumb bandwidth selector, Ch 3 Section 3.4, Eq 3.31:
    h = 0.9 * A * n**(-1/5),  A = min(sigma_hat, IQR/1.34)   (Eq 3.30 for A)
Confirmed in-session against the owner-supplied 1998 reprint pages (Ch 3, pp. 43-48).
NOT Eq 3.28 (h = 1.06*sigma_hat*n**(-1/5)) -- per owner ruling 07/15/2026, Eq 3.31
is the formula used (Silverman's own recommended choice; Eq 3.28 oversmooths further
still on multimodal data per Silverman's own discussion, paraphrased not quoted).

Reuses PS9.1's exact synthetic sample (same seed, same known mixture density).
"""
import numpy as np
from reference_impls.ps9_1_ref import (x as SAMPLE, N, h_grid, kde_ise, h_star,
                                        ise_star, ise, kde_eval, fine_grid,
                                        W1, M1, S1, W2, M2, S2)


def silverman_bandwidth(sample, n):
    sigma_hat = sample.std(ddof=1)
    q75, q25 = np.percentile(sample, [75, 25])
    iqr = q75 - q25
    A = min(sigma_hat, iqr / 1.34)
    h = 0.9 * A * n ** (-1.0 / 5.0)
    return h, sigma_hat, iqr, A


def analyze(sample, n=N):
    h_s, sigma_hat, iqr, A = silverman_bandwidth(sample, n)
    ise_vals = np.array([ise(kde_eval(sample, h, fine_grid)) for h in h_grid])
    best_idx = int(np.argmin(ise_vals))
    h_opt, ise_opt = h_grid[best_idx], ise_vals[best_idx]
    ise_s = ise(kde_eval(sample, h_s, fine_grid))
    return {
        "h_silverman": h_s, "sigma_hat": sigma_hat, "iqr": iqr, "A": A,
        "h_star": h_opt, "ise_star": ise_opt, "ise_silverman": ise_s,
        "ratio": ise_s / ise_opt,
    }


if __name__ == "__main__":
    primary = analyze(SAMPLE)
    print("PRIMARY (seed=902, n=500):")
    for k, v in primary.items():
        print(f"  {k} = {v:.5f}" if isinstance(v, float) else f"  {k} = {v}")

    print("\nGrid endpoints for reference:")
    print(f"  h=0.05 (undersmoothed extreme): ISE={kde_ise[0]:.6f}")
    print(f"  h=2.00 (oversmoothed extreme):  ISE={kde_ise[-1]:.6f}")

    print("\nCalibration (10 independent seeds, same n=500, same mixture/grid):")
    hs, ratios = [], []
    for sd in range(1, 11):
        r = np.random.default_rng(sd)
        c = r.uniform(size=N) < W1
        xs = np.where(c, r.normal(M1, S1, size=N), r.normal(M2, S2, size=N))
        res = analyze(xs)
        hs.append(res["h_silverman"])
        ratios.append(res["ratio"])
        print(f"  seed={sd}: h_Silverman={res['h_silverman']:.4f}  "
              f"h*={res['h_star']:.3f}  ISE(h*)={res['ise_star']:.6f}  "
              f"ISE(h_Silv)={res['ise_silverman']:.6f}  ratio={res['ratio']:.3f}")

    all_hs = [primary["h_silverman"]] + hs
    all_ratios = [primary["ratio"]] + ratios
    print(f"\nh_Silverman range across 11 runs: [{min(all_hs):.4f}, {max(all_hs):.4f}]")
    print(f"ratio range across 11 runs: [{min(all_ratios):.3f}, {max(all_ratios):.3f}]")
