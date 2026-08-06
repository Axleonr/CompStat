"""
PS7.4 reference implementation -- ten-"pump" hierarchical Gamma-Poisson Gibbs
sampler (original synthetic construction, informed by R&C 7.12's classic
pump-failure shape but NOT the historical dataset -- policy 4.3.1 default:
student/drafter-generated synthetic data with a specified generative process
and seed).

Model:
    y_i | theta_i ~ Poisson(theta_i * t_i),  i = 1..10   (t_i known exposure)
    theta_i | alpha, beta ~ Gamma(alpha, beta) iid        (alpha fixed/known)
    beta ~ Gamma(gamma, delta)                            (hyperprior)

Full conditionals (both conjugate):
    theta_i | y_i, beta ~ Gamma(alpha + y_i,  beta + t_i)
    beta | theta_1..10  ~ Gamma(gamma + 10*alpha,  delta + sum(theta_i))
"""
import numpy as np

t = np.array([10, 20, 15, 30, 25, 5, 40, 8, 12, 18], dtype=float)
theta_true = np.array([0.05, 0.15, 0.30, 0.02, 0.50, 0.80, 0.01, 0.60, 0.25, 0.10])
alpha = 1.8
gamma_h, delta_h = 0.1, 1.0  # hyperprior shape/rate on beta
n_pumps = 10

def gen_data(seed):
    rng = np.random.default_rng(seed)
    y = rng.poisson(theta_true * t)
    return y

def gibbs_chain(y, n_iter, burn_in, seed, beta_init):
    rng = np.random.default_rng(seed)
    beta = beta_init
    theta = np.empty((n_iter, n_pumps))
    betas = np.empty(n_iter)
    for it in range(n_iter):
        th = rng.gamma(alpha + y, 1.0/(beta + t))  # numpy gamma uses scale = 1/rate
        beta = rng.gamma(gamma_h + n_pumps*alpha, 1.0/(delta_h + th.sum()))
        theta[it] = th
        betas[it] = beta
    return theta[burn_in:], betas[burn_in:]

def credible_interval(x, lo=2.5, hi=97.5):
    return np.percentile(x, lo), np.percentile(x, hi)

if __name__ == '__main__':
    y = gen_data(seed=0)
    print("Synthetic data (seed 0):")
    print("t_i:        ", t)
    print("theta_true: ", theta_true)
    print("y_i:        ", y)
    print("expected y_i (theta_true*t):", theta_true*t)

    n_iter, burn_in = 20000, 2000

    # Three chains, different seeds and different starting beta
    chains = []
    starts = [(101, 1.0), (202, 5.0), (303, 0.2)]
    for seed, beta0 in starts:
        th, be = gibbs_chain(y, n_iter, burn_in, seed=seed, beta_init=beta0)
        chains.append((th, be))

    print(f"\n=== Multi-start agreement ({len(chains)} chains, n_iter={n_iter}, burn_in={burn_in}) ===")
    means = np.array([th.mean(axis=0) for th, be in chains])  # (3, 10)
    beta_means = np.array([be.mean() for th, be in chains])
    print("Per-chain theta_i posterior means:")
    for i, m in enumerate(means):
        print(f"  chain {i} (seed {starts[i][0]}, beta0={starts[i][1]}): {np.round(m,4)}, beta_mean={beta_means[i]:.4f}")
    max_pairwise_theta_diff = 0.0
    for i in range(len(chains)):
        for j in range(i+1, len(chains)):
            d = np.max(np.abs(means[i]-means[j]))
            max_pairwise_theta_diff = max(max_pairwise_theta_diff, d)
    max_pairwise_beta_diff = np.max(np.abs(beta_means[:,None]-beta_means[None,:]))
    print(f"Max pairwise |theta_i mean diff| across chains: {max_pairwise_theta_diff:.4f}")
    print(f"Max pairwise |beta mean diff| across chains: {max_pairwise_beta_diff:.4f}")

    # Use chain 0 as "the" reference/healthy export chain
    th0, be0 = chains[0]
    print(f"\n=== Chain 0 (the saved/exported healthy chain): posterior summaries ===")
    for i in range(n_pumps):
        m = th0[:,i].mean()
        lo, hi = credible_interval(th0[:,i])
        print(f"  pump {i+1}: mean={m:.4f}, 95% CI=({lo:.4f}, {hi:.4f})")
    print(f"  beta: mean={be0.mean():.4f}, 95% CI={credible_interval(be0)}")

    ranking = np.argsort(th0.mean(axis=0))
    print(f"Most reliable (lowest theta) pump: {ranking[0]+1}; least reliable (highest theta): {ranking[-1]+1}")

    # Conjugate-conditional moment check: fix beta at chain-0's posterior mean,
    # draw a large batch of theta_i directly from Gamma(alpha+y_i, beta_fixed+t_i),
    # confirm empirical mean/var matches the closed-form Gamma mean/var.
    print("\n=== Conjugate-conditional moment check (fixed beta = chain-0 posterior mean) ===")
    beta_fixed = be0.mean()
    rng = np.random.default_rng(999)
    max_mean_gap, max_var_gap = 0.0, 0.0
    for i in range(n_pumps):
        shape_i, rate_i = alpha + y[i], beta_fixed + t[i]
        draws = rng.gamma(shape_i, 1.0/rate_i, size=200000)
        closed_mean, closed_var = shape_i/rate_i, shape_i/rate_i**2
        max_mean_gap = max(max_mean_gap, abs(draws.mean()-closed_mean))
        max_var_gap = max(max_var_gap, abs(draws.var(ddof=1)-closed_var))
    print(f"max |empirical mean - shape/rate| over 10 pumps: {max_mean_gap:.6f}")
    print(f"max |empirical var  - shape/rate^2| over 10 pumps: {max_var_gap:.6f}")

    # Calibration across more independent multi-start triples
    print("\n=== Calibration: 30 independent 3-chain-triples ===")
    max_theta_diffs, max_beta_diffs = [], []
    for rep in range(30):
        base = 10000 + rep*10
        chs = []
        for k, (seed_off, beta0) in enumerate([(1,1.0),(2,5.0),(3,0.2)]):
            th, be = gibbs_chain(y, n_iter, burn_in, seed=base+seed_off, beta_init=beta0)
            chs.append((th.mean(axis=0), be.mean()))
        th_means = np.array([c[0] for c in chs])
        be_means = np.array([c[1] for c in chs])
        m1 = max(np.max(np.abs(th_means[i]-th_means[j])) for i in range(3) for j in range(i+1,3))
        m2 = max(np.abs(be_means[i]-be_means[j]) for i in range(3) for j in range(i+1,3))
        max_theta_diffs.append(m1)
        max_beta_diffs.append(m2)
    max_theta_diffs, max_beta_diffs = np.array(max_theta_diffs), np.array(max_beta_diffs)
    print(f"max pairwise theta_i diff: mean={max_theta_diffs.mean():.4f} max={max_theta_diffs.max():.4f} 99th={np.percentile(max_theta_diffs,99):.4f}")
    print(f"max pairwise beta diff:    mean={max_beta_diffs.mean():.4f} max={max_beta_diffs.max():.4f} 99th={np.percentile(max_beta_diffs,99):.4f}")
