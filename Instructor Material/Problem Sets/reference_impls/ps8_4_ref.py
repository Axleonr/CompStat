"""
PS8.4 reference implementation.
Compares estimator variance (across independent replications of the PS7.4
healthy pump Gibbs sampler) for three ways of using a fixed compute budget
of n_iter=20000 (burn_in=2000, 18000 retained draws), estimating the
posterior mean of beta:
  (a) all 18000 retained draws
  (b) thinned to m draws, spaced every k=10th draw across the full run
  (c) the first m draws, unthinned (a contiguous block, same size as (b))
"""
import numpy as np
from reference_impls.pump_gibbs import run_pump_gibbs

N_ITER = 20000
BURN_IN = 2000
THIN_K = 10


def one_replication(seed):
    chain = run_pump_gibbs(N_ITER, seed=seed, init_beta=1.0)
    post = chain[BURN_IN:, -1]  # beta column, post-warmup
    n = len(post)  # 18000
    m = n // THIN_K  # 1800
    all_est = post.mean()
    thinned_est = post[::THIN_K].mean()
    first_est = post[:m].mean()
    return all_est, thinned_est, first_est, m, n


def main(n_reps=200, seed_start=10000):
    alls, thins, firsts = [], [], []
    for i in range(n_reps):
        a, t, f, m, n = one_replication(seed_start + i)
        alls.append(a)
        thins.append(t)
        firsts.append(f)
    alls = np.array(alls)
    thins = np.array(thins)
    firsts = np.array(firsts)
    return dict(
        m=m, n=n, n_reps=n_reps,
        var_all=alls.var(ddof=1),
        var_thinned=thins.var(ddof=1),
        var_first=firsts.var(ddof=1),
        mean_all=alls.mean(),
        mean_thinned=thins.mean(),
        mean_first=firsts.mean(),
    )


if __name__ == "__main__":
    res = main()
    print(f"n retained = {res['n']}, m (post-thinning / first-block size) = {res['m']}, replications = {res['n_reps']}")
    print(f"Var(all {res['n']} draws)      = {res['var_all']:.6e}   mean={res['mean_all']:.5f}")
    print(f"Var(thinned to {res['m']})     = {res['var_thinned']:.6e}   mean={res['mean_thinned']:.5f}")
    print(f"Var(first {res['m']} unthinned) = {res['var_first']:.6e}   mean={res['mean_first']:.5f}")
    print(f"ratio thinned/all: {res['var_thinned']/res['var_all']:.3f}")
    print(f"ratio first/thinned: {res['var_first']/res['var_thinned']:.3f}")
    print(f"ratio first/all: {res['var_first']/res['var_all']:.3f}")
