"""
PS9.3 reference implementation.
Step 1: reproduce a PS7.4-compliant reference Gibbs chain (10-pump hierarchical
        Poisson-Gamma model), matching WO-M7's saved-chain specification exactly
        (all 20,000 iterations, no warm-up discarded, no thinning, 11 columns:
        theta_1..theta_10, beta) -- this stands in for "the student's saved PS7.4
        chain" that PS9.3 imports.
Step 2: for pump j=3 (t_3=15, theta_true_3=0.30), discard the first 2,000
        iterations as warm-up (same policy PS7.4 uses for its own summaries),
        then compute:
          - the Rao-Blackwellized density estimate of theta_3's marginal, as the
            average of its gamma full-conditional densities over the retained beta draws
          - a plain Gaussian-kernel KDE of the same theta_3 draws
          - a bootstrap-over-iterations variance comparison of the two estimators
            on a grid of theta values
"""
import numpy as np

# ---------------------------------------------------------------------------
# Step 1: reproduce the PS7.4 model and reference chain
# ---------------------------------------------------------------------------
ALPHA = 1.8
T = np.array([10, 20, 15, 30, 25, 5, 40, 8, 12, 18], dtype=float)
THETA_TRUE = np.array([0.05, 0.15, 0.30, 0.02, 0.50, 0.80, 0.01, 0.60, 0.25, 0.10])
NPUMPS = 10

DATA_SEED = 74
data_rng = np.random.default_rng(DATA_SEED)
Y = data_rng.poisson(THETA_TRUE * T)

def run_gibbs_chain(seed, beta_init, n_iter=20000):
    rng = np.random.default_rng(seed)
    theta = np.full(NPUMPS, beta_init)  # arbitrary init draw start; refined below
    beta = beta_init
    # initialize theta from its conditional given the init beta, for a sane start
    theta = rng.gamma(ALPHA + Y, 1.0 / (beta + T))
    theta_chain = np.zeros((n_iter, NPUMPS))
    beta_chain = np.zeros(n_iter)
    for t in range(n_iter):
        theta = rng.gamma(ALPHA + Y, 1.0 / (beta + T))
        shape_b = 0.1 + NPUMPS * ALPHA
        rate_b = 1.0 + theta.sum()
        beta = rng.gamma(shape_b, 1.0 / rate_b)
        theta_chain[t] = theta
        beta_chain[t] = beta
    return theta_chain, beta_chain

# Three chains, different inits/seeds, matching PS7.4's multi-start spec
CHAIN_SEEDS = [741, 742, 743]
CHAIN_INITS = [0.2, 1.0, 5.0]
chains = [run_gibbs_chain(s, b0) for s, b0 in zip(CHAIN_SEEDS, CHAIN_INITS)]

# Reference chain = chain 1 (seed=741, init beta=1.0) -- "the one you'll keep"
REF_IDX = 1
ref_theta_chain, ref_beta_chain = chains[REF_IDX]
REF_SEED = CHAIN_SEEDS[REF_IDX]
REF_INIT = CHAIN_INITS[REF_IDX]

# Saved-chain export: full 20,000 iterations, 11 columns (theta_1..10, beta) -- no warm-up discarded
saved_chain = np.column_stack([ref_theta_chain, ref_beta_chain])  # shape (20000, 11)

# ---------------------------------------------------------------------------
# Multi-start check (mirrors PS7.4's own compliance check, confirms this is a
# healthy reference chain fit for PS9.3 to import)
# ---------------------------------------------------------------------------
WARMUP = 2000
post_means_theta = np.array([c[0][WARMUP:].mean(axis=0) for c in chains])
post_means_beta = np.array([c[1][WARMUP:].mean() for c in chains])
max_pairwise_theta_diff = 0.0
for i in range(3):
    for j in range(i + 1, 3):
        d = np.max(np.abs(post_means_theta[i] - post_means_theta[j]))
        max_pairwise_theta_diff = max(max_pairwise_theta_diff, d)
max_pairwise_beta_diff = 0.0
for i in range(3):
    for j in range(i + 1, 3):
        d = abs(post_means_beta[i] - post_means_beta[j])
        max_pairwise_beta_diff = max(max_pairwise_beta_diff, d)

# ---------------------------------------------------------------------------
# Step 2: PS9.3 proper -- pump j=3 (0-indexed: 2)
# ---------------------------------------------------------------------------
PUMP_IDX = 2  # pump "3" in 1-indexed problem language
y_j = Y[PUMP_IDX]
t_j = T[PUMP_IDX]

retained_theta_j = ref_theta_chain[WARMUP:, PUMP_IDX]
retained_beta = ref_beta_chain[WARMUP:]
Nret = len(retained_beta)

def gamma_pdf(x, shape, rate):
    # manual gamma density, from primitives (no scipy.stats call)
    x = np.asarray(x, dtype=float)
    out = np.zeros_like(x)
    pos = x > 0
    xin = x[pos]
    log_pdf = (shape * np.log(rate) - gammaln(shape) + (shape - 1) * np.log(xin) - rate * xin)
    out[pos] = np.exp(log_pdf)
    return out

def gammaln(z):
    # Stirling-based log-gamma (primitive; avoids scipy.special.gammaln)
    # Lanczos approximation, standard coefficients
    g = 7
    c = [0.99999999999980993, 676.5203681218851, -1259.1392167224028,
         771.32342877765313, -176.61502916214059, 12.507343278686905,
         -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7]
    z = z - 1
    x = c[0]
    for i in range(1, g + 2):
        x += c[i] / (z + i)
    t = z + g + 0.5
    return 0.5 * np.log(2 * np.pi) + (z + 0.5) * np.log(t) - t + np.log(x)

LOG_GAMMALN_CACHE = {}

def rb_density(theta_grid, betas, shape, tvalue):
    # average of gamma full-conditional densities Gamma(shape, rate=beta+t) over betas,
    # vectorized over (grid x betas) -- mathematically identical to the per-draw loop,
    # just avoiding Python-level looping for speed.
    theta_grid = np.asarray(theta_grid, dtype=float)
    betas = np.asarray(betas, dtype=float)
    rates = betas + tvalue                      # (n_draws,)
    lg = gammaln(shape)
    # log pdf matrix: rows = grid points, cols = draws
    with np.errstate(divide="ignore"):
        log_theta = np.log(theta_grid)[:, None]  # (n_grid, 1)
    log_pdf = (shape * np.log(rates)[None, :] - lg
               + (shape - 1) * log_theta
               - rates[None, :] * theta_grid[:, None])
    pdf = np.where(theta_grid[:, None] > 0, np.exp(log_pdf), 0.0)
    return pdf.mean(axis=1)

def gaussian_kernel(u):
    return (1.0 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * u ** 2)

def kde_density(theta_grid, draws, h):
    theta_grid = np.asarray(theta_grid, dtype=float)
    draws = np.asarray(draws, dtype=float)
    n = len(draws)
    u = (theta_grid[:, None] - draws[None, :]) / h  # (n_grid, n_draws)
    return gaussian_kernel(u).sum(axis=1) / (n * h)

GRID = np.linspace(0.0, 1.4, 700)
KDE_BW = 0.15 * retained_theta_j.std()  # simple, self-defined, fixed choice -- not graded on optimality

rb_curve = rb_density(GRID, retained_beta, ALPHA + y_j, t_j)
kde_curve = kde_density(GRID, retained_theta_j, KDE_BW)
rb_integral = np.trapezoid(rb_curve, GRID)
kde_integral = np.trapezoid(kde_curve, GRID)

# ---------------------------------------------------------------------------
# Bootstrap-over-draws variance comparison (coarser grid; expensive, so it is
# only executed on demand, not as an import-time side effect)
# ---------------------------------------------------------------------------
BOOT_GRID = np.linspace(0.05, 1.2, 150)

def run_bootstrap(B, boot_seed):
    boot_rng = np.random.default_rng(boot_seed)
    rb_boot = np.zeros((B, len(BOOT_GRID)))
    kde_boot = np.zeros((B, len(BOOT_GRID)))
    for b in range(B):
        idx = boot_rng.integers(0, Nret, size=Nret)
        beta_b = retained_beta[idx]
        theta_b = retained_theta_j[idx]
        rb_boot[b] = rb_density(BOOT_GRID, beta_b, ALPHA + y_j, t_j)
        kde_boot[b] = kde_density(BOOT_GRID, theta_b, KDE_BW)
    rb_pointwise_var = rb_boot.var(axis=0, ddof=1)
    kde_pointwise_var = kde_boot.var(axis=0, ddof=1)
    rb_mean_var = rb_pointwise_var.mean()
    kde_mean_var = kde_pointwise_var.mean()
    rb_integrated_var = np.trapezoid(rb_pointwise_var, BOOT_GRID)
    kde_integrated_var = np.trapezoid(kde_pointwise_var, BOOT_GRID)
    return {
        "rb_mean_var": rb_mean_var, "kde_mean_var": kde_mean_var,
        "rb_integrated_var": rb_integrated_var, "kde_integrated_var": kde_integrated_var,
        "advantage_ratio_mean": kde_mean_var / rb_mean_var,
        "advantage_ratio_integrated": kde_integrated_var / rb_integrated_var,
    }

if __name__ == "__main__":
    print(f"data seed={DATA_SEED}, y={Y}")
    print(f"reference chain: seed={REF_SEED}, init beta={REF_INIT}, n_iter=20000")
    print(f"multi-start max pairwise theta_i posterior-mean diff: {max_pairwise_theta_diff:.5f}")
    print(f"multi-start max pairwise beta posterior-mean diff: {max_pairwise_beta_diff:.5f}")
    print(f"\npump index (1-indexed) = 3, y_3={y_j}, t_3={t_j}")
    print(f"retained iterations (post warm-up) = {Nret}")
    print(f"theta_3 retained draws: mean={retained_theta_j.mean():.5f}, sd={retained_theta_j.std():.5f}")
    print(f"KDE bandwidth used = {KDE_BW:.5f}")
    print(f"RB curve integral = {rb_integral:.6f} (should be ~1)")
    print(f"KDE curve integral = {kde_integral:.6f} (should be ~1)")
    BOOT_SEED = 903
    B = 300
    print(f"\nbootstrap B={B}, boot_seed={BOOT_SEED}, grid=BOOT_GRID (150 pts, [0.05,1.2])")
    res = run_bootstrap(B, BOOT_SEED)
    print(f"RB mean pointwise variance   = {res['rb_mean_var']:.10f}")
    print(f"KDE mean pointwise variance  = {res['kde_mean_var']:.10f}")
    print(f"advantage ratio (KDE var / RB var), mean-pointwise      = {res['advantage_ratio_mean']:.3f}")
    print(f"RB integrated variance   = {res['rb_integrated_var']:.10f}")
    print(f"KDE integrated variance  = {res['kde_integrated_var']:.10f}")
    print(f"advantage ratio (KDE var / RB var), integrated          = {res['advantage_ratio_integrated']:.3f}")

