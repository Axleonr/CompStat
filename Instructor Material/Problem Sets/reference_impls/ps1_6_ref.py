"""
PS1.6 (optional) reference implementation.

Target: standard normal truncated to [a, inf), a=4 (deep right tail).
Naive method: draw Z ~ N(0,1) (library sampler; not the goal here), reject until Z>=a.
Improved method: shifted-exponential proposal g(x) = a*exp(-a*(x-a)) for x>=a (rate a,
shifted to start at a); accept-reject with derived bound M = (1/a)*exp(-a^2/2)
(target unnormalized density exp(-x^2/2)).
"""
import numpy as np
from scipy.stats import norm

A = 4.0

def naive_rate_theory():
    return 1 - norm.cdf(A)

def improved_M():
    return (1.0/A) * np.exp(-A**2/2)

def improved_rate_theory():
    tail_mass = 1 - norm.cdf(A)          # = P(X>=a) for the *proper* normal density
    M = improved_M()
    # acceptance rate = (unnormalized-target integral) / M = sqrt(2pi)*tail_mass / M
    return np.sqrt(2*np.pi) * tail_mass / M

def naive_empirical(seed, n_attempts):
    rng = np.random.default_rng(seed)
    z = rng.normal(0, 1, n_attempts)
    accepted = z[z >= A]
    return len(accepted), n_attempts, accepted

def improved_empirical(seed, n_attempts):
    rng = np.random.default_rng(seed)
    u1 = rng.uniform(0, 1, n_attempts)
    y = A - np.log(1 - u1) / A          # shifted-exponential draw: Exp(rate=a) shifted by +a
    u2 = rng.uniform(0, 1, n_attempts)
    f_unnorm = np.exp(-y**2/2)
    g = A * np.exp(-A*(y-A))
    M = improved_M()
    ratio = f_unnorm / (M * g)
    accept_mask = u2 <= ratio
    accepted = y[accept_mask]
    return accept_mask.sum(), n_attempts, accepted

if __name__ == "__main__":
    print(f"a = {A}")
    print(f"naive theoretical rate  = P(Z>=a) = {naive_rate_theory():.8e}")
    print(f"improved theoretical M  = {improved_M():.8e}")
    print(f"improved theoretical rate = {improved_rate_theory():.6f}")
    print()

    N_NAIVE = 20_000_000  # need many attempts since naive rate is ~3e-5
    N_IMPROVED = 20_000

    print("=== PRIMARY logged run ===")
    seed = 2468
    n_acc, n_att, acc_sample = naive_empirical(seed, N_NAIVE)
    rate_naive = n_acc / n_att
    print(f"NAIVE (seed={seed}, attempts={n_att}): accepted={n_acc}  empirical rate={rate_naive:.6e}  theory={naive_rate_theory():.6e}")

    n_acc2, n_att2, acc_sample2 = improved_empirical(seed, N_IMPROVED)
    rate_improved = n_acc2 / n_att2
    print(f"IMPROVED (seed={seed}, attempts={n_att2}): accepted={n_acc2}  empirical rate={rate_improved:.6f}  theory={improved_rate_theory():.6f}")
    print(f"ratio improved/naive rate = {rate_improved/rate_naive:.1f}x")
    print(f"accepted-sample (improved) mean={acc_sample2.mean():.4f} min={acc_sample2.min():.4f} (should be >= {A})")
    print()

    print("=== Calibration (3 more seeds, smaller naive N for speed) ===")
    N_NAIVE_CALIB = 20_000_000
    for s in [13, 57, 999]:
        n_acc, n_att, _ = naive_empirical(s, N_NAIVE_CALIB)
        rate_naive_c = n_acc/n_att
        n_acc2, n_att2, _ = improved_empirical(s, N_IMPROVED)
        rate_improved_c = n_acc2/n_att2
        print(f"seed={s}: naive rate={rate_naive_c:.6e} (n_acc={n_acc})  improved rate={rate_improved_c:.6f} (n_acc={n_acc2})  ratio={rate_improved_c/rate_naive_c:.1f}x")
