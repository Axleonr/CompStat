"""
PS6.2 reference implementation.
Chain 1: birth-death (tridiagonal) chain on {0,1,2,3} -- reversible by construction.
Chain 2: biased directed 4-cycle -- non-reversible, still has a stationary distribution.
Both stationary distributions are exact linear-algebra facts (tier 2); the specific
detailed-balance products / net-flow numbers reported to the student are logged here (tier 3).
"""
import numpy as np

def stationary(P):
    n = P.shape[0]
    Aeq = np.vstack([(P.T - np.eye(n)), np.ones(n)])
    beq = np.zeros(n + 1); beq[-1] = 1.0
    pi, *_ = np.linalg.lstsq(Aeq, beq, rcond=None)
    return pi

# ---------- Chain 1: reversible birth-death chain ----------
P_bd = np.array([
    [0.6, 0.4, 0.0, 0.0],
    [0.3, 0.3, 0.4, 0.0],
    [0.0, 0.2, 0.3, 0.5],
    [0.0, 0.0, 0.5, 0.5],
])
assert np.allclose(P_bd.sum(axis=1), 1.0)
pi_bd = stationary(P_bd)
print("Chain 1 (birth-death) pi:", np.round(pi_bd, 6))

n = P_bd.shape[0]
print("\nDetailed balance check, chain 1 (all pairs i<j):")
max_db_violation = 0.0
for i in range(n):
    for j in range(i+1, n):
        lhs = pi_bd[i] * P_bd[i, j]
        rhs = pi_bd[j] * P_bd[j, i]
        diff = abs(lhs - rhs)
        max_db_violation = max(max_db_violation, diff)
        if P_bd[i, j] > 0 or P_bd[j, i] > 0:
            print(f"  pi[{i}]P[{i},{j}]={lhs:.8f}  vs  pi[{j}]P[{j},{i}]={rhs:.8f}  diff={diff:.2e}")
print("max |pi_i P_ij - pi_j P_ji}| over ALL pairs (including zero-zero pairs):", max_db_violation)

# ---------- Chain 2: biased directed 4-cycle (non-reversible) ----------
p_fwd = 0.7
P_cyc = np.array([
    [1-p_fwd, p_fwd,   0.0,     0.0],
    [0.0,     1-p_fwd, p_fwd,   0.0],
    [0.0,     0.0,     1-p_fwd, p_fwd],
    [p_fwd,   0.0,     0.0,     1-p_fwd],
])
assert np.allclose(P_cyc.sum(axis=1), 1.0)
pi_cyc = stationary(P_cyc)
print("\nChain 2 (biased 4-cycle) pi:", np.round(pi_cyc, 8))
print("(expected uniform by circulant symmetry: 0.25 each)")

print("\nDetailed balance check, chain 2 (adjacent pairs, cycle order):")
net_flows = []
for i in range(n):
    j = (i + 1) % n
    fwd_flow = pi_cyc[i] * P_cyc[i, j]
    back_flow = pi_cyc[j] * P_cyc[j, i]
    net = fwd_flow - back_flow
    net_flows.append(net)
    print(f"  pi[{i}]P[{i},{j}]={fwd_flow:.6f}  vs  pi[{j}]P[{j},{i}]={back_flow:.6f}  net flow={net:.6f}")
print("net flow values (should be identical nonzero by symmetry):", np.round(net_flows, 6))
print("min/max net flow:", min(net_flows), max(net_flows))

# sanity: confirm chain 2 is irreducible (cyclic connectivity) despite non-reversibility
A = (P_cyc > 0).astype(int)
R = A.copy()
for _ in range(10):
    R = ((R @ A) > 0).astype(int) | R
print("chain 2 irreducible:", bool(np.all(R > 0)))
