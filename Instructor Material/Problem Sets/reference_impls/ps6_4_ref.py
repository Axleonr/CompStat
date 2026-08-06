"""
PS6.4 reference implementation.
d(t) = sup_mu ||mu P^t - pi||_TV, computed exactly as max over POINT-MASS starts
(valid because TV distance is convex in mu, so the sup over the simplex is attained
at a vertex -- standard fact, used here as a computational simplification).
Chain A: the PS6.1 "main" (convergent) 4-state chain.
Chain B: the PS6.1 periodic 2-cycle (optional reinforcement).
"""
import numpy as np

def stationary(P):
    n = P.shape[0]
    Aeq = np.vstack([(P.T - np.eye(n)), np.ones(n)])
    beq = np.zeros(n + 1); beq[-1] = 1.0
    pi, *_ = np.linalg.lstsq(Aeq, beq, rcond=None)
    return pi

def tv(mu, pi):
    return 0.5 * np.sum(np.abs(mu - pi))

def d_of_t(P, pi, t_values):
    n = P.shape[0]
    out = []
    for t in t_values:
        Pt = np.linalg.matrix_power(P, t)
        d_t = max(tv(Pt[i, :], pi) for i in range(n))  # max over point-mass starts
        out.append(d_t)
    return out

# ---------- Chain A: PS6.1's main (convergent) chain ----------
P_main = np.array([
    [0.5, 0.3, 0.2, 0.0],
    [0.2, 0.4, 0.3, 0.1],
    [0.1, 0.3, 0.4, 0.2],
    [0.0, 0.2, 0.3, 0.5],
])
pi_main = stationary(P_main)
print("PS6.1 main chain pi:", np.round(pi_main, 6))

t_vals = list(range(0, 21))
d_vals = d_of_t(P_main, pi_main, t_vals)
print("\nd(t) for PS6.1 main chain, t=0..20:")
for t, d in zip(t_vals, d_vals):
    print(f"  d({t:2d}) = {d:.8f}")

# monotonicity check
diffs = np.diff(d_vals)
print("\nmax increase in d(t) (should be <=0 for non-increasing, allowing for fp noise):", max(diffs))
is_nonincreasing = all(diffs <= 1e-12)
print("non-increasing (within 1e-12 fp tolerance):", is_nonincreasing)
print("d(0) =", d_vals[0], " (exact fact: d(0) = 1 - min_i pi*_i = 1 - 0.1875 = 0.8125; can only reach 1.0 if pi* puts zero mass on some state, which it doesn't here)")
print("d(20) =", d_vals[-1])

# ---------- Chain B: periodic 2-cycle (optional reinforcement) ----------
P_per = np.array([[0.0, 1.0], [1.0, 0.0]])
pi_per = stationary(P_per)
print("\nPeriodic chain pi:", pi_per)
t_vals_per = list(range(0, 11))
d_vals_per = d_of_t(P_per, pi_per, t_vals_per)
print("d(t) for periodic 2-cycle, t=0..10:")
for t, d in zip(t_vals_per, d_vals_per):
    print(f"  d({t}) = {d}")
print("flat at 0.5 for all t:", all(abs(d - 0.5) < 1e-12 for d in d_vals_per))
