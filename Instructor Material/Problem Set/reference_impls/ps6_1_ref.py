"""
PS6.1 reference implementation.
Part 1: analytic stationary distribution of a 4-state irreducible, aperiodic chain
        (exact linear algebra fact -- tier 2), cross-checked two ways.
Part 2: long-run simulation from primitives (manual categorical draw from the
        uniform RNG only -- no library Markov-chain routine) -- tier 3, calibrates
        the empirical-vs-analytic tolerance given to the student.
Part 3: periodic 2-cycle P = [[0,1],[1,0]] -- exact matrix powers, tier 2, no
        simulation needed (deterministic oscillation).
"""
import numpy as np

# ---------- Part 1: the main chain ----------
P = np.array([
    [0.5, 0.3, 0.2, 0.0],
    [0.2, 0.4, 0.3, 0.1],
    [0.1, 0.3, 0.4, 0.2],
    [0.0, 0.2, 0.3, 0.5],
])
assert np.allclose(P.sum(axis=1), 1.0)

# irreducibility check: all-ones reachability via repeated squaring of the
# 0/1 adjacency pattern until it stops changing or saturates
A = (P > 0).astype(int)
R = A.copy()
for _ in range(10):
    R = ((R @ A) > 0).astype(int) | R
irreducible = bool(np.all(R > 0))

# aperiodicity: sufficient (not necessary) witness -- strictly positive diagonal
aperiodic_witness = bool(np.all(np.diag(P) > 0))

# Method A: solve pi (P - I) = 0, sum(pi) = 1 via linear system
n = P.shape[0]
Aeq = np.vstack([(P.T - np.eye(n)), np.ones(n)])
beq = np.zeros(n + 1)
beq[-1] = 1.0
pi_linsolve, *_ = np.linalg.lstsq(Aeq, beq, rcond=None)

# Method B: left eigenvector for eigenvalue 1 (cross-check of Method A)
eigvals, eigvecs = np.linalg.eig(P.T)
idx = np.argmin(np.abs(eigvals - 1.0))
pi_eig = np.real(eigvecs[:, idx])
pi_eig = pi_eig / pi_eig.sum()

print("irreducible:", irreducible, " aperiodic (positive-diagonal witness):", aperiodic_witness)
print("pi (linear solve):   ", np.round(pi_linsolve, 6))
print("pi (eigenvector):    ", np.round(pi_eig, 6))
print("max abs diff between methods:", np.max(np.abs(pi_linsolve - pi_eig)))

pi_star = pi_linsolve  # exact analytic target used for the tier-3 comparison below

# ---------- Part 2: long-run simulation from primitives ----------
def simulate_chain(P, n_steps, start_state, seed):
    rng = np.random.default_rng(seed)
    n_states = P.shape[0]
    counts = np.zeros(n_states, dtype=np.int64)
    state = start_state
    for t in range(n_steps):
        counts[state] += 1
        u = rng.uniform()  # only primitive: uniform RNG
        cum = 0.0
        for j in range(n_states):
            cum += P[state, j]
            if u < cum:
                state = j
                break
    return counts / n_steps

N_STEPS = 200_000
PRIMARY_SEED = 2026
occ_primary = simulate_chain(P, N_STEPS, start_state=0, seed=PRIMARY_SEED)
max_abs_err_primary = np.max(np.abs(occ_primary - pi_star))
print("\nprimary run: N=", N_STEPS, "seed=", PRIMARY_SEED)
print("empirical occupancy:", np.round(occ_primary, 6))
print("analytic pi*:       ", np.round(pi_star, 6))
print("max abs error (primary):", max_abs_err_primary)

# calibration sweep: multiple seeds + a different start state
calib_seeds = [1, 2, 3, 4, 5, 6, 7, 8]
max_errs = []
for s in calib_seeds:
    occ = simulate_chain(P, N_STEPS, start_state=3, seed=s)
    err = np.max(np.abs(occ - pi_star))
    max_errs.append(err)
    print(f"  calib seed={s} start=3 max_abs_err={err:.6f}")
print("calibration max-abs-err range:", min(max_errs), "to", max(max_errs))
print("calibration max-abs-err worst case:", max(max_errs))

# ---------- Part 3: periodic 2-cycle contrast ----------
P_periodic = np.array([[0.0, 1.0], [1.0, 0.0]])
mu0 = np.array([1.0, 0.0])  # start entirely in state 0
print("\nPeriodic 2-cycle P = [[0,1],[1,0]], mu0 = (1,0):")
for t in range(8):
    mu_t = mu0 @ np.linalg.matrix_power(P_periodic, t)
    print(f"  t={t}: mu_t = {mu_t}")

# also confirm it never settles for a "mixed" start (sanity: any non-(0.5,0.5)
# start also keeps oscillating; a (0.5,0.5) start is the periodic chain's own
# stationary distribution and is a fixed point -- worth noting as a caveat)
mu0_half = np.array([0.5, 0.5])
print("\nFor comparison, mu0 = (0.5, 0.5) (already the periodic chain's stationary pi):")
for t in range(4):
    mu_t = mu0_half @ np.linalg.matrix_power(P_periodic, t)
    print(f"  t={t}: mu_t = {mu_t}")
