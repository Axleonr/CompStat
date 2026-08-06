"""
PS6.3 reference implementation.
Lazy random walk on the n-cycle (n=4..10): P[i,i]=1/2, P[i,i+-1 mod n]=1/4 each.
Spectral gap: exact circulant-eigenvalue fact (library eigendecomposition permitted, tier 2).
Empirical mixing time tau(eps): first t with exact TV distance (point-mass start) below
threshold eps, computed via matrix powers -- exact for n<=10 (tier 2, no simulation).
Two-state definitional anchor (switch probability p): eigenvalues {1, 1-2p}, gap=2p --
hand-derivable, confirmed numerically here as a cross-check only.
"""
import numpy as np

def lazy_cycle_P(n):
    P = np.zeros((n, n))
    for i in range(n):
        P[i, i] = 0.5
        P[i, (i+1) % n] += 0.25
        P[i, (i-1) % n] += 0.25
    return P

def tv_distance(mu, pi):
    return 0.5 * np.sum(np.abs(mu - pi))

def mixing_time(P, pi, eps, start_state=0, t_max=100000):
    n = P.shape[0]
    mu = np.zeros(n); mu[start_state] = 1.0
    Pt = np.eye(n)
    for t in range(t_max):
        d = tv_distance(mu, pi)
        if d <= eps:
            return t, d
        mu = mu @ P
    return None, None

EPS = 0.25
results = []
for n in range(4, 11):
    P = lazy_cycle_P(n)
    assert np.allclose(P.sum(axis=1), 1.0)
    pi = np.ones(n) / n  # uniform, exact fact for any circulant/doubly-stochastic matrix
    # verify pi is exactly stationary
    assert np.allclose(pi @ P, pi)

    eigvals = np.linalg.eigvals(P)
    eigvals_sorted = np.sort(np.real(eigvals))[::-1]  # descending
    lam1 = eigvals_sorted[1]  # second-largest eigenvalue (largest is 1)
    gap = 1 - lam1

    # closed-form circulant check: lambda_1 = 1/2 + 1/2*cos(2*pi/n)
    lam1_closed = 0.5 + 0.5*np.cos(2*np.pi/n)
    gap_closed = 1 - lam1_closed

    tau, d_at_tau = mixing_time(P, pi, EPS)

    results.append((n, gap, gap_closed, tau, d_at_tau))
    print(f"n={n:2d}  gap(eig)={gap:.6f}  gap(closed-form)={gap_closed:.6f}  "
          f"diff={abs(gap-gap_closed):.2e}  tau(eps={EPS})={tau}  TV_at_tau={d_at_tau:.4f}")

print("\nn^2 scaling check: tau * gap should be roughly constant-ish (diffusive scaling):")
for n, gap, gap_closed, tau, d in results:
    print(f"  n={n:2d}  tau={tau:3d}  gap={gap:.5f}  tau*gap={tau*gap:.4f}  n^2={n*n:4d}  tau/n^2={tau/(n*n):.4f}")

# ---------- Two-state definitional anchor (hand-derivable, not swept) ----------
print("\nTwo-state switch-probability-p chain, cross-check of hand-derived eigenvalues/gap:")
for p in [0.1, 0.3, 0.5, 0.7]:
    P2 = np.array([[1-p, p], [p, 1-p]])
    ev = np.sort(np.real(np.linalg.eigvals(P2)))[::-1]
    gap2 = 1 - ev[1]
    print(f"  p={p}: eigenvalues={np.round(ev,6)} (expected {{1, {1-2*p}}}), gap={gap2:.6f} (expected {2*p})")
