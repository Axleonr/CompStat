"""
PS4.1 reference implementation.
Part A: two-component Gaussian mixture log-likelihood surface over (mu1, mu2)
        for two simulated datasets -- one designed to show a bimodal surface,
        one designed to show a unimodal surface (5.1/5.13-inspired, original data).
Part B: numerical confirmation that the sample median minimizes sum_i |x_i - c|
        (formulation #2, the order-statistic identity).
Run with: python3 ps4_1_ref.py
"""
import numpy as np
from scipy.optimize import minimize_scalar

# ---------- Part A: mixture log-likelihood surface ----------

def loglik_surface(x, w, sigma, mu1_grid, mu2_grid):
    """Log-likelihood of a two-component Gaussian mixture (known weight w,
    known common sigma) evaluated over a grid of (mu1, mu2)."""
    ll = np.zeros((len(mu1_grid), len(mu2_grid)))
    for i, mu1 in enumerate(mu1_grid):
        d1 = -0.5 * ((x - mu1) / sigma) ** 2 - 0.5 * np.log(2 * np.pi * sigma ** 2)
        c1 = w * np.exp(d1)
        for j, mu2 in enumerate(mu2_grid):
            d2 = -0.5 * ((x - mu2) / sigma) ** 2 - 0.5 * np.log(2 * np.pi * sigma ** 2)
            c2 = (1 - w) * np.exp(d2)
            ll[i, j] = np.sum(np.log(c1 + c2 + 1e-300))
    return ll


def count_local_maxima(surface, merge_radius=3):
    """Count grid points exceeding all 8 neighbors, merging maxima within
    merge_radius grid cells of a higher-valued one already kept."""
    R, C = surface.shape
    cand = []
    for i in range(1, R - 1):
        for j in range(1, C - 1):
            neigh = surface[i - 1:i + 2, j - 1:j + 2].copy()
            center = surface[i, j]
            neigh[1, 1] = -np.inf
            if center > neigh.max():
                cand.append((i, j, center))
    cand.sort(key=lambda t: -t[2])
    kept = []
    for (i, j, v) in cand:
        if all(abs(i - ki) > merge_radius or abs(j - kj) > merge_radius for (ki, kj, kv) in kept):
            kept.append((i, j, v))
    return len(kept), kept


def gen_mixture_data(seed, n, w, mu1_true, mu2_true, sigma):
    rng = np.random.default_rng(seed)
    n1 = int(round(w * n))
    n2 = n - n1
    x1 = rng.normal(mu1_true, sigma, n1)
    x2 = rng.normal(mu2_true, sigma, n2)
    return np.concatenate([x1, x2]), n1, n2


w, sigma = 0.25, 1.0

print("=== Dataset A (bimodal design): seed=0, n=400, true means (0, 4) ===")
xA, n1A, n2A = gen_mixture_data(seed=0, n=400, w=w, mu1_true=0.0, mu2_true=4.0, sigma=sigma)
mu_grid_A = np.linspace(-4, 8, 241)
surfA = loglik_surface(xA, w, sigma, mu_grid_A, mu_grid_A)
nmaxA, keptA = count_local_maxima(surfA)
peaksA = [(round(mu_grid_A[i], 3), round(mu_grid_A[j], 3), round(v, 3))
          for i, j, v in sorted(keptA, key=lambda t: -t[2])]
print(f"n1={n1A}, n2={n2A}, grid=241x241 over [-4,8], local maxima found = {nmaxA}")
for p in peaksA:
    print("  peak (mu1, mu2, loglik):", p)

print()
print("=== Dataset B (unimodal design): seed=0, n=30, true means (0, 1.0) ===")
xB, n1B, n2B = gen_mixture_data(seed=0, n=30, w=w, mu1_true=0.0, mu2_true=1.0, sigma=sigma)
mu_grid_B = np.linspace(-4, 6, 241)
surfB = loglik_surface(xB, w, sigma, mu_grid_B, mu_grid_B)
nmaxB, keptB = count_local_maxima(surfB)
peaksB = [(round(mu_grid_B[i], 3), round(mu_grid_B[j], 3), round(v, 3))
          for i, j, v in sorted(keptB, key=lambda t: -t[2])]
print(f"n1={n1B}, n2={n2B}, grid=241x241 over [-4,6], local maxima found = {nmaxB}")
for p in peaksB:
    print("  peak (mu1, mu2, loglik):", p)

# Stability check across grid resolutions for both datasets
print()
print("=== Resolution-stability check ===")
for label, x, lo, hi in [("A", xA, -4, 8), ("B", xB, -4, 6)]:
    for gn in [121, 181, 301]:
        mg = np.linspace(lo, hi, gn)
        s = loglik_surface(x, w, sigma, mg, mg)
        nm, _ = count_local_maxima(s)
        print(f"  dataset {label}, grid_n={gn}: nmax={nm}")

# ---------- Part A (cont'd): Dataset A' -- CP-6 addition, DP-8 package ----------
# Appended 2026-07-20 (Phase 3 correction pass, session CP-6). Does NOT modify the
# Dataset A / Dataset B code above (append-only per the drafter memo's instruction).
# Mechanics per M4_DrafterFindingsReport_1_0.md (E-M4-1/E-M4-2 package, ruled DP-8):
# same true means, same n, and same weight as Dataset A, but a RANDOM Binomial(n, w)
# split of the component sizes instead of Dataset A's FIXED round(w*n) split.
# Grid-searched identically to Dataset A: same range, same grid density, same
# merge_radius. Seed chosen and logged this session (not one of the six informal
# robustness-check seeds 1-6 used in the drafter's own pre-check).

def gen_mixture_data_random_split(seed, n, w, mu1_true, mu2_true, sigma):
    """Same generative process as gen_mixture_data, except n1 is drawn from
    Binomial(n, w) rather than fixed at round(w*n)."""
    rng = np.random.default_rng(seed)
    n1 = int(rng.binomial(n, w))
    n2 = n - n1
    x1 = rng.normal(mu1_true, sigma, n1)
    x2 = rng.normal(mu2_true, sigma, n2)
    return np.concatenate([x1, x2]), n1, n2


SEED_APRIME = 20260720  # CP-6 executor's own chosen seed for this logged run

print()
print("=== Dataset A' (random-split design): seed=%d, n=400, true means (0, 4) ===" % SEED_APRIME)
xAp, n1Ap, n2Ap = gen_mixture_data_random_split(seed=SEED_APRIME, n=400, w=w,
                                                  mu1_true=0.0, mu2_true=4.0, sigma=sigma)
surfAp = loglik_surface(xAp, w, sigma, mu_grid_A, mu_grid_A)
nmaxAp, keptAp = count_local_maxima(surfAp)
peaksAp = [(round(mu_grid_A[i], 3), round(mu_grid_A[j], 3), round(v, 3))
           for i, j, v in sorted(keptAp, key=lambda t: -t[2])]
print(f"n1={n1Ap}, n2={n2Ap} (random Binomial(400,0.25) split), grid=241x241 over [-4,8], local maxima found = {nmaxAp}")
for p in peaksAp:
    print("  peak (mu1, mu2, loglik):", p)

print()
print("=== Dataset A' resolution-stability check ===")
for gn in [121, 181, 301]:
    mg = np.linspace(-4, 8, gn)
    s = loglik_surface(xAp, w, sigma, mg, mg)
    nm, _ = count_local_maxima(s)
    print(f"  dataset A', grid_n={gn}: nmax={nm}")

# ---------- Part B: median as minimizer of sum |x_i - c| ----------

print()
print("=== Formulation #2: median minimizes sum|x_i - c| ===")
rng2 = np.random.default_rng(42)
x_med = rng2.normal(5, 2, 15)  # odd n -> unique minimizer
med = np.median(x_med)


def abs_loss(c):
    return np.sum(np.abs(x_med - c))


res = minimize_scalar(abs_loss, bounds=(x_med.min() - 1, x_med.max() + 1),
                       method='bounded', options={'xatol': 1e-10})
print("sorted data:", np.round(np.sort(x_med), 4))
print("sample median:", med)
print("numerical argmin of sum|x_i - c|:", res.x)
print("loss at numerical argmin:", res.fun)
print("loss at sample median:", abs_loss(med))
print("|argmin - median| =", abs(res.x - med))
