"""
PS9.4 reference implementation.
Reuses PS9.1's synthetic sample and known density.
Implements the 1D k-nearest-neighbor density estimator from primitives:
    f_hat(x) = k / (2 * n * R_k(x))
where R_k(x) is the distance from x to its k-th nearest neighbor in the sample.
Contrasts with PS9.1's sweep-optimal Gaussian-kernel KDE, focused on tail behavior.
"""
import numpy as np
from reference_impls.ps9_1_ref import (x as SAMPLE, N, true_density, kde_eval,
                                        h_star, fine_grid, ise)

K = 25  # chosen so k/n is a comparably "local" fraction to the KDE's effective window

def knn_density(sample, k, xgrid):
    sample = np.asarray(sample, dtype=float)
    xgrid = np.asarray(xgrid, dtype=float)
    n = len(sample)
    dists = np.abs(xgrid[:, None] - sample[None, :])   # (n_grid, n)
    dists_sorted = np.sort(dists, axis=1)
    Rk = dists_sorted[:, k - 1]                          # distance to k-th nearest neighbor
    Rk = np.maximum(Rk, 1e-12)
    return k / (2.0 * n * Rk)

# ISE of kNN against the known density, same fine grid as PS9.1
knn_curve_fine = knn_density(SAMPLE, K, fine_grid)
knn_ise = ise(knn_curve_fine)

# KDE at PS9.1's sweep-optimal bandwidth, for a like-for-like comparison
kde_curve_fine = kde_eval(SAMPLE, h_star, fine_grid)
kde_ise_at_hstar = ise(kde_curve_fine)

# ---------------------------------------------------------------------------
# Tail-region comparison: points well beyond the mixture's effective support
# (rightmost component: mean 2.0, sd 0.9 -> effectively negligible density by x=6)
# ---------------------------------------------------------------------------
TAIL_POINTS = np.array([5.0, 6.0, 7.0, 8.0, 10.0])
knn_tail = knn_density(SAMPLE, K, TAIL_POINTS)
kde_tail = kde_eval(SAMPLE, h_star, TAIL_POINTS)
true_tail = true_density(TAIL_POINTS)

# integral of each estimator restricted to a wide-but-finite tail region [5, 30]
# -- illustrates non-integrability behavior over a growing domain
def tail_mass(estimator_fn, lo, hi, npts=6000):
    grid = np.linspace(lo, hi, npts)
    vals = estimator_fn(grid)
    return np.trapezoid(vals, grid)

knn_tail_mass_5_30 = tail_mass(lambda g: knn_density(SAMPLE, K, g), 5.0, 30.0)
kde_tail_mass_5_30 = tail_mass(lambda g: kde_eval(SAMPLE, h_star, g), 5.0, 30.0)

if __name__ == "__main__":
    print(f"n={N}, k={K}, KDE h*={h_star}")
    print(f"kNN ISE (vs known density) = {knn_ise:.6f}")
    print(f"KDE ISE at h* (vs known density) = {kde_ise_at_hstar:.6f}")
    print("\nTail-region point values (x, true, kNN, KDE):")
    for xv, tv, kv, dv in zip(TAIL_POINTS, true_tail, knn_tail, kde_tail):
        print(f"  x={xv:5.1f}  true={tv:.3e}  kNN={kv:.3e}  KDE={dv:.3e}  kNN/KDE ratio={kv/max(dv,1e-300):.3e}")
    print(f"\nintegral of kNN estimate over [5,30] = {knn_tail_mass_5_30:.6f}")
    print(f"integral of KDE estimate over [5,30]  = {kde_tail_mass_5_30:.6f}")
    print(f"true density's integral over [5,30] (should be ~0): {np.trapezoid(true_density(np.linspace(5,30,6000)), np.linspace(5,30,6000)):.3e}")
