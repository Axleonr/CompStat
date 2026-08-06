"""
PS4.5 reference implementation (Optional problem).
Objective: the same two-component mixture log-likelihood family used in
PS4.1/PS4.2 (weight w=0.25, sigma=1, true means 0 and 4), here with n=30 so the
per-step log-likelihood delta is on a scale (~7-10 units) a temperature
parameter can meaningfully compete with -- with n=400 (PS4.1's dataset) typical
deltas are ~100+ units and no reasonable temperature schedule discriminates
(checked; see Notes in the validation log).

Provided SA loop (pseudocode form is what the student receives; this is its
Python realization) run across four temperature schedules, 100 replications
each, from an uninformed start point theta0=(2,2) equidistant from both known
modes. Reports fraction of replications recovering the dominant (global) mode.
Run with: python3 ps4_5_ref.py
"""
import numpy as np

w, sigma = 0.25, 1.0


def gen_mixture_data(seed, n, w, mu1_true, mu2_true, sigma):
    rng = np.random.default_rng(seed)
    n1 = int(round(w * n))
    n2 = n - n1
    x1 = rng.normal(mu1_true, sigma, n1)
    x2 = rng.normal(mu2_true, sigma, n2)
    return np.concatenate([x1, x2]), n1, n2


x, n1, n2 = gen_mixture_data(seed=0, n=30, w=w, mu1_true=0.0, mu2_true=4.0, sigma=sigma)
print(f"dataset: n1={n1}, n2={n2}")


def loglik(theta, x, w, sigma):
    mu1, mu2 = theta
    phi1 = np.exp(-0.5 * ((x - mu1) / sigma) ** 2) / np.sqrt(2 * np.pi * sigma ** 2)
    phi2 = np.exp(-0.5 * ((x - mu2) / sigma) ** 2) / np.sqrt(2 * np.pi * sigma ** 2)
    f = w * phi1 + (1 - w) * phi2
    return np.sum(np.log(f + 1e-300))


# Grid search to establish the two known modes (same technique as PS4.1)
mu_grid = np.linspace(-4, 8, 241)


def find_modes(x, merge_radius=3):
    surf = np.zeros((len(mu_grid), len(mu_grid)))
    for i, m1 in enumerate(mu_grid):
        for j, m2 in enumerate(mu_grid):
            surf[i, j] = loglik((m1, m2), x, w, sigma)
    R, C = surf.shape
    cand = []
    for i in range(1, R - 1):
        for j in range(1, C - 1):
            neigh = surf[i - 1:i + 2, j - 1:j + 2].copy()
            c = surf[i, j]
            neigh[1, 1] = -np.inf
            if c > neigh.max():
                cand.append((i, j, c))
    cand.sort(key=lambda t: -t[2])
    kept = []
    for (i, j, v) in cand:
        if all(abs(i - ki) > merge_radius or abs(j - kj) > merge_radius for (ki, kj, kv) in kept):
            kept.append((i, j, v))
    return [(mu_grid[i], mu_grid[j], v) for i, j, v in sorted(kept, key=lambda t: -t[2])]


modes = find_modes(x)
print("modes found by grid search:", [(round(a, 3), round(b, 3), round(c, 3)) for a, b, c in modes])
global_mode = np.array(modes[0][:2])
local_mode = np.array(modes[1][:2])


# --- Provided SA loop (student-facing pseudocode realized here) ---
def sa_maximize(loglik_fn, x0, schedule_fn, n_iter, rng, step_sd=0.5):
    theta = np.array(x0, dtype=float)
    cur_val = loglik_fn(theta)
    best_theta, best_val = theta.copy(), cur_val
    for k in range(n_iter):
        T = schedule_fn(k)
        prop = theta + rng.normal(0, step_sd, size=2)
        prop_val = loglik_fn(prop)
        delta = prop_val - cur_val
        if delta > 0 or rng.random() < np.exp(min(delta / max(T, 1e-12), 0)):
            theta, cur_val = prop, prop_val
            if cur_val > best_val:
                best_theta, best_val = theta.copy(), cur_val
    return best_theta, best_val


def classify(theta):
    dg = np.linalg.norm(theta - global_mode)
    dl = np.linalg.norm(theta - local_mode)
    return 'global' if dg < dl else 'local'


schedules = {
    'fast_geometric (T0=8, decay 0.90)':     lambda k: 8.0 * 0.90 ** k,
    'moderate_geometric (T0=8, decay 0.97)': lambda k: 8.0 * 0.97 ** k,
    'slow_geometric (T0=8, decay 0.995)':    lambda k: 8.0 * 0.995 ** k,
    'logarithmic (T0=8 / log(k+2))':         lambda k: 8.0 / np.log(k + 2),
}

n_iter, n_reps = 300, 100
print()
print(f"=== SA mode-recovery study: {n_reps} replications x {n_iter} iterations per schedule ===")
results = {}
for name, sched in schedules.items():
    counts = {'global': 0, 'local': 0}
    for rep in range(n_reps):
        rng_rep = np.random.default_rng(5000 + rep)
        theta_f, val_f = sa_maximize(lambda th: loglik(th, x, w, sigma), [2.0, 2.0], sched, n_iter, rng_rep)
        counts[classify(theta_f)] += 1
    results[name] = counts
    print(f"{name}: global={counts['global']}/{n_reps}  local={counts['local']}/{n_reps}  "
          f"(recovery rate={counts['global']/n_reps:.2f})")
