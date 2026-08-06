"""
PS1.3 reference implementation — accept-reject for N(0,1) using two proposals.

Proposal 1: standard Laplace (double exponential), g1(x) = 0.5*exp(-|x|)
Proposal 2 (original, second proposal per WO): standard Cauchy, g2(x) = 1/(pi*(1+x^2))

Theoretical bounds M are derived in closed form (see problem's instructor note):
  M1 = sqrt(2/pi) * exp(0.5)             [max of f/g1 at |x|=1]
  M2 = 2 * sqrt(pi/2) * exp(-0.5)         [max of f/g2 at |x|=1]
Acceptance probability = 1/M (standard accept-reject theory, R&C Ex. 2.5).
"""
import numpy as np

M1_theory = np.sqrt(2/np.pi) * np.exp(0.5)
M2_theory = 2 * np.sqrt(np.pi/2) * np.exp(-0.5)
p1_theory = 1.0 / M1_theory
p2_theory = 1.0 / M2_theory

print(f"M1 (Laplace) theoretical = {M1_theory:.6f}  -> acceptance rate 1/M1 = {p1_theory:.6f}")
print(f"M2 (Cauchy)  theoretical = {M2_theory:.6f}  -> acceptance rate 1/M2 = {p2_theory:.6f}")
print()

def target_pdf(x):
    return np.exp(-0.5*x**2) / np.sqrt(2*np.pi)

def laplace_pdf(x):
    return 0.5*np.exp(-np.abs(x))

def cauchy_pdf(x):
    return 1.0/(np.pi*(1+x**2))

def accept_reject(rng, propose, prop_pdf, M, n_attempts):
    y = propose(rng, n_attempts)
    u = rng.uniform(0, 1, n_attempts)
    ratio = target_pdf(y) / (M * prop_pdf(y))
    accept_mask = u <= ratio
    accepted = y[accept_mask]
    return accepted, accept_mask.sum(), n_attempts

def laplace_sample(rng, n):
    # standard Laplace via inverse transform: sign * Exp(1)
    u = rng.uniform(-0.5, 0.5, n)
    return -np.sign(u) * np.log(1 - 2*np.abs(u))

def cauchy_sample(rng, n):
    return rng.standard_cauchy(n)

def run(seed, n_attempts=20000, label=""):
    rng = np.random.default_rng(seed)
    acc1, n_acc1, n_att1 = accept_reject(rng, laplace_sample, laplace_pdf, M1_theory, n_attempts)
    acc2, n_acc2, n_att2 = accept_reject(rng, cauchy_sample, cauchy_pdf, M2_theory, n_attempts)
    rate1 = n_acc1/n_att1
    rate2 = n_acc2/n_att2
    se1 = np.sqrt(p1_theory*(1-p1_theory)/n_attempts)
    se2 = np.sqrt(p2_theory*(1-p2_theory)/n_attempts)
    print(f"--- {label} seed={seed} n_attempts={n_attempts} ---")
    print(f"Laplace: accepted={n_acc1}  empirical rate={rate1:.5f}  theory={p1_theory:.5f}  SE={se1:.5f}  |diff|={abs(rate1-p1_theory):.5f}  within 3SE: {abs(rate1-p1_theory)<=3*se1}")
    print(f"Cauchy:  accepted={n_acc2}  empirical rate={rate2:.5f}  theory={p2_theory:.5f}  SE={se2:.5f}  |diff|={abs(rate2-p2_theory):.5f}  within 3SE: {abs(rate2-p2_theory)<=3*se2}")
    # sanity: accepted-sample moments should look standard-normal-ish
    print(f"accepted-Laplace-route sample: mean={acc1.mean():.4f} var={acc1.var(ddof=1):.4f} (n={len(acc1)})")
    print(f"accepted-Cauchy-route sample:  mean={acc2.mean():.4f} var={acc2.var(ddof=1):.4f} (n={len(acc2)})")
    print()
    return rate1, rate2

if __name__ == "__main__":
    print("=== PRIMARY logged run ===")
    run(31415, 20000, label="PRIMARY")
    print("=== Calibration (3 more seeds) ===")
    for s in [11, 22, 33]:
        run(s, 20000, label="CALIBRATION")
