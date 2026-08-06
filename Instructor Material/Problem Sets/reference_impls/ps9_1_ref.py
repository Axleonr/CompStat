"""
PS9.1 reference implementation.
Known density: normal mixture f0(x) = w1*N(x;m1,s1^2) + w2*N(x;m2,s2^2).
Histogram estimator (from primitives) at three illustrative bin widths.
Gaussian-kernel KDE (from primitives) swept over a stated bandwidth grid.
ISE(h) computed by numerical integration of (f_hat_h - f0)^2 against the KNOWN density (tier-2 fact).
"""
import numpy as np

# ---------------------------------------------------------------------------
# Known density (tier-2: fully specified generative fact)
# ---------------------------------------------------------------------------
W1, M1, S1 = 0.55, -2.0, 0.6
W2, M2, S2 = 0.45,  2.0, 0.9

def true_density(x):
    x = np.asarray(x, dtype=float)
    p1 = (1.0 / (S1 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - M1) / S1) ** 2)
    p2 = (1.0 / (S2 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - M2) / S2) ** 2)
    return W1 * p1 + W2 * p2

# ---------------------------------------------------------------------------
# Synthetic sample
# ---------------------------------------------------------------------------
SEED = 902
rng = np.random.default_rng(SEED)
N = 500
comp = rng.uniform(size=N) < W1
x = np.where(comp, rng.normal(M1, S1, size=N), rng.normal(M2, S2, size=N))

# ---------------------------------------------------------------------------
# Histogram density estimator, from primitives (manual bin counting)
# ---------------------------------------------------------------------------
def histogram_density(sample, bin_width, lo=-8.0, hi=8.0):
    edges = np.arange(lo, hi + bin_width, bin_width)
    counts = np.zeros(len(edges) - 1)
    for v in sample:
        idx = int((v - lo) // bin_width)
        if 0 <= idx < len(counts):
            counts[idx] += 1
    density = counts / (len(sample) * bin_width)
    return edges, density

def histogram_eval(sample, bin_width, xgrid, lo=-8.0, hi=8.0):
    edges, density = histogram_density(sample, bin_width, lo, hi)
    idx = np.clip(((xgrid - lo) // bin_width).astype(int), 0, len(density) - 1)
    out = np.where((xgrid >= lo) & (xgrid < hi), density[idx], 0.0)
    return out

# ---------------------------------------------------------------------------
# Gaussian-kernel KDE, from primitives
# ---------------------------------------------------------------------------
def gaussian_kernel(u):
    return (1.0 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * u ** 2)

def kde_eval(sample, h, xgrid):
    n = len(sample)
    out = np.zeros_like(xgrid, dtype=float)
    for i, xv in enumerate(xgrid):
        u = (xv - sample) / h
        out[i] = np.sum(gaussian_kernel(u)) / (n * h)
    return out

# ---------------------------------------------------------------------------
# ISE via numerical integration against the known density (fine grid, trapezoid)
# ---------------------------------------------------------------------------
GRID_LO, GRID_HI, GRID_N = -8.0, 8.0, 4001
fine_grid = np.linspace(GRID_LO, GRID_HI, GRID_N)
f0_fine = true_density(fine_grid)

def ise(f_hat_vals):
    diff2 = (f_hat_vals - f0_fine) ** 2
    return np.trapezoid(diff2, fine_grid)

# ---------------------------------------------------------------------------
# Part 1: histogram at three illustrative bin widths
# ---------------------------------------------------------------------------
hist_widths = [0.15, 0.5, 2.0]
hist_results = {}
for bw in hist_widths:
    vals = histogram_eval(x, bw, fine_grid)
    hist_results[bw] = ise(vals)

# ---------------------------------------------------------------------------
# Part 2: KDE bandwidth sweep
# ---------------------------------------------------------------------------
h_grid = np.array([0.05, 0.08, 0.12, 0.18, 0.25, 0.35, 0.5, 0.7, 1.0, 1.4, 2.0])
kde_ise = np.array([ise(kde_eval(x, h, fine_grid)) for h in h_grid])
best_idx = int(np.argmin(kde_ise))
h_star = h_grid[best_idx]
ise_star = kde_ise[best_idx]

if __name__ == "__main__":
    print(f"seed={SEED}, n={N}")
    print("sample mean/sd:", x.mean(), x.std())
    print("\nHistogram ISE by bin width:")
    for bw in hist_widths:
        print(f"  bin_width={bw:.2f}  ISE={hist_results[bw]:.6f}")
    print("\nKDE ISE sweep:")
    for h, v in zip(h_grid, kde_ise):
        print(f"  h={h:.3f}  ISE={v:.6f}")
    print(f"\nsweep-minimizing bandwidth h* = {h_star:.3f}, ISE(h*) = {ise_star:.6f}")
    # sanity: KDE integrates to ~1
    check_h = 0.35
    kde_vals_check = kde_eval(x, check_h, fine_grid)
    integral = np.trapezoid(kde_vals_check, fine_grid)
    print(f"\nsanity check: KDE(h={check_h}) integrates to {integral:.6f} (should be ~1)")

def calibration_run(seeds):
    results = []
    for sd in seeds:
        r = np.random.default_rng(sd)
        c = r.uniform(size=N) < W1
        xs = np.where(c, r.normal(M1, S1, size=N), r.normal(M2, S2, size=N))
        ise_vals = np.array([ise(kde_eval(xs, h, fine_grid)) for h in h_grid])
        bi = int(np.argmin(ise_vals))
        results.append((sd, h_grid[bi], ise_vals[bi]))
    return results

if __name__ == "__main__":
    cal = calibration_run(range(1, 11))
    print("\nCalibration (10 independent seeds, same n=500, same grid):")
    hs = []
    for sd, h, v in cal:
        print(f"  seed={sd}  h*={h:.3f}  ISE(h*)={v:.6f}")
        hs.append(h)
    hs = np.array(hs)
    print(f"h* range across calibration: [{hs.min():.3f}, {hs.max():.3f}], mean={hs.mean():.3f}")
