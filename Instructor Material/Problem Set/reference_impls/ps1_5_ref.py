"""
PS1.5 reference implementation.

Part 1: RANDU generator (a=65539, c=0, m=2^31 -- stipulated per problem; historical
IBM attribution flagged [UNVERIFIED], see problem's discussion note) -- empirically
exhibit the parallel-hyperplane defect in consecutive triples via the algebraic
identity X_{n+2} = 6*X_{n+1} - 9*X_n (mod m), confirmed here by direct computation,
not asserted from memory. Count the number of distinct "planes" (integer k values).

Part 2: seed-misuse demonstration -- re-seeding a *good* LCG (PS1.1's generator)
inside a loop using a low-entropy, correlated seed sequence (e.g., seed = loop
counter, or seed = previous seed + small increment) versus fresh independent
seeding, and measuring the resulting cross-run correlation.
"""
import numpy as np

M_RANDU = 2**31
A_RANDU = 65539

def randu_sequence(seed, n):
    x = seed
    xs = []
    for _ in range(n):
        x = (A_RANDU * x) % M_RANDU
        xs.append(x)
    return np.array(xs, dtype=np.int64)

def hyperplane_check(seed, n=5000):
    xs = randu_sequence(seed, n)
    # identity to verify (not assumed): X_{n+2} - 6*X_{n+1} + 9*X_n should be an exact
    # integer multiple of m, for all n, if the classic RANDU identity holds.
    x0, x1, x2 = xs[:-2], xs[1:-1], xs[2:]
    combo = x2 - 6*x1 + 9*x0
    remainders = combo % M_RANDU
    exact_multiple = np.all(remainders == 0)
    k_values = combo // M_RANDU
    distinct_k = np.unique(k_values)
    print(f"seed={seed} n={n}")
    print(f"  identity X_(n+2) - 6 X_(n+1) + 9 X_n === 0 (mod m) holds for all triples: {exact_multiple}")
    print(f"  distinct plane indices k = (X_(n+2)-6X_(n+1)+9X_n)/m : {distinct_k.tolist()}")
    print(f"  number of distinct planes observed: {len(distinct_k)}")
    print()
    return exact_multiple, distinct_k

def lcg_good_sequence(seed, n, a=16807, c=0, m=2**31 - 1):
    x = seed
    xs = []
    for _ in range(n):
        x = (a * x + c) % m
        xs.append(x)
    return np.array(xs, dtype=np.float64) / m

def seed_misuse_demo(n_runs=20, draws_per_run=50):
    # BAD practice: reseed each "independent" run with a tightly-correlated seed
    # (here: seed = 1000 + run_index), simulating a common real-world bug (e.g.,
    # seeding from a loop counter or from wall-clock time sampled too coarsely).
    bad_runs = []
    for i in range(n_runs):
        seed = 1000 + i   # correlated seeds, differing by 1 each time
        bad_runs.append(lcg_good_sequence(seed, draws_per_run))
    bad_runs = np.array(bad_runs)  # shape (n_runs, draws_per_run)

    # GOOD practice: seed each run from a well-separated master sequence.
    rng = np.random.default_rng(999)
    good_runs = []
    for i in range(n_runs):
        seed = int(rng.integers(1, 2**31 - 2))
        good_runs.append(lcg_good_sequence(seed, draws_per_run))
    good_runs = np.array(good_runs)

    # Measure cross-run correlation: correlate run i's draws with run i+1's draws
    # (first draw of each run is the most exposed to seed correlation).
    bad_first_draws = bad_runs[:, 0]
    good_first_draws = good_runs[:, 0]
    bad_lag1_corr = np.corrcoef(bad_first_draws[:-1], bad_first_draws[1:])[0, 1]
    good_lag1_corr = np.corrcoef(good_first_draws[:-1], good_first_draws[1:])[0, 1]

    print(f"BAD (correlated seeds 1000..{999+n_runs}): first-draw lag-1 corr across runs = {bad_lag1_corr:.4f}")
    print(f"GOOD (well-separated random seeds): first-draw lag-1 corr across runs = {good_lag1_corr:.4f}")
    print(f"bad first draws (first 6): {bad_first_draws[:6]}")
    print(f"good first draws (first 6): {good_first_draws[:6]}")
    print()
    return bad_lag1_corr, good_lag1_corr

if __name__ == "__main__":
    print("=== Part 1: RANDU hyperplane structure ===")
    print("--- PRIMARY (seed=1, stated to students) ---")
    hyperplane_check(1, n=5000)
    print("--- Calibration (3 more seeds) ---")
    for s in [3, 12345, 777777]:
        hyperplane_check(s, n=5000)

    print("=== Part 2: seed-misuse demonstration ===")
    print("--- PRIMARY (n_runs=20, draws_per_run=50) ---")
    seed_misuse_demo(20, 50)
    print("--- Calibration (different run counts) ---")
    for nr in [30, 50]:
        seed_misuse_demo(nr, 50)
