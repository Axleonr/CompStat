"""
PS9.5 reference implementation.
New synthetic dataset (moderate n, moderately-separated bimodal mixture) where:
  - a leave-one-out likelihood cross-validation (LOO-CV) bandwidth ("data-driven,
    small") reveals two modes
  - the smallest bandwidth at which the KDE first collapses to a single mode,
    scaled up by a safety margin ("conservative/presentation-safe, large"),
    shows one mode
Both are self-contained, executable criteria -- no external formula citation needed.
"""
import numpy as np

W1, M1, S1 = 0.5, -1.3, 1.0
W2, M2, S2 = 0.5,  1.3, 1.0

def true_density(x):
    x = np.asarray(x, dtype=float)
    p1 = (1.0/(S1*np.sqrt(2*np.pi)))*np.exp(-0.5*((x-M1)/S1)**2)
    p2 = (1.0/(S2*np.sqrt(2*np.pi)))*np.exp(-0.5*((x-M2)/S2)**2)
    return W1*p1 + W2*p2

def gaussian_kernel(u):
    return (1.0/np.sqrt(2*np.pi))*np.exp(-0.5*u**2)

def kde_eval(sample, h, xgrid):
    sample = np.asarray(sample); xgrid = np.asarray(xgrid, dtype=float)
    n = len(sample)
    u = (xgrid[:, None] - sample[None, :]) / h
    return gaussian_kernel(u).sum(axis=1) / (n*h)

def loo_cv_score(sample, h):
    # leave-one-out log-likelihood: sum_i log f_hat_{-i}(x_i)
    sample = np.asarray(sample, dtype=float)
    n = len(sample)
    u = (sample[:, None] - sample[None, :]) / h
    K = gaussian_kernel(u)
    np.fill_diagonal(K, 0.0)
    f_loo = K.sum(axis=1) / ((n-1)*h)
    f_loo = np.maximum(f_loo, 1e-300)
    return np.sum(np.log(f_loo))

def count_modes(vals):
    # count strict local maxima on the grid (interior points only)
    modes = 0
    for i in range(1, len(vals)-1):
        if vals[i] > vals[i-1] and vals[i] > vals[i+1]:
            modes += 1
    return modes

FINE = np.linspace(-6, 6, 1200)
H_GRID = np.round(np.arange(0.15, 2.01, 0.05), 3)

def analyze(sample):
    cv_scores = np.array([loo_cv_score(sample, h) for h in H_GRID])
    h_cv = H_GRID[int(np.argmax(cv_scores))]
    modes_cv = count_modes(kde_eval(sample, h_cv, FINE))

    # smallest h (on the grid) giving exactly 1 mode
    h_collapse = None
    for h in H_GRID:
        if count_modes(kde_eval(sample, h, FINE)) == 1:
            h_collapse = h
            break
    h_large = None if h_collapse is None else round(min(h_collapse * 1.3, H_GRID[-1]), 3)
    modes_large = None if h_large is None else count_modes(kde_eval(sample, h_large, FINE))
    return h_cv, modes_cv, h_collapse, h_large, modes_large

if __name__ == "__main__":
    N = 45
    found = None
    for seed in range(1, 400):
        rng = np.random.default_rng(seed)
        comp = rng.uniform(size=N) < W1
        x = np.where(comp, rng.normal(M1, S1, size=N), rng.normal(M2, S2, size=N))
        h_cv, modes_cv, h_collapse, h_large, modes_large = analyze(x)
        if modes_cv == 2 and modes_large == 1 and h_cv < h_large:
            found = (seed, x, h_cv, modes_cv, h_collapse, h_large, modes_large)
            print(f"seed={seed}: h_cv={h_cv} (modes={modes_cv}), h_collapse={h_collapse}, "
                  f"h_large={h_large} (modes={modes_large})")
            if seed > 5:  # collect a few candidates, then stop after a reasonable one
                break
    if found is None:
        print("no qualifying seed found in range")
    else:
        seed, x, h_cv, modes_cv, h_collapse, h_large, modes_large = found
        print(f"\nSELECTED seed={seed}")
        print("sample:", np.round(np.sort(x), 3))
        print(f"h_cv={h_cv}, modes at h_cv={modes_cv}")
        print(f"h_collapse (smallest 1-mode h)={h_collapse}, h_large=1.3x={h_large}, modes at h_large={modes_large}")
