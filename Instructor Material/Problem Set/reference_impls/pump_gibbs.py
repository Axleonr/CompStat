"""
Reference re-implementation of the PS7.4 ten-pump hierarchical Gamma-Poisson
Gibbs sampler, per the exact model/data specification logged in
ValidationLog_0_3.md (PS7.4 entry). Data values are the documented tier-3
logged values (not re-derived from an RNG draw), so this is a faithful,
exact reproduction of the model each student's own PS7.4 solution is built
on -- used here only as the "student's own stored chain" input to Module 8
diagnostics problems, never to re-verify PS7.4 itself.

Model:
    y_i ~ Poisson(theta_i * t_i),  i = 1..10
    theta_i ~ Gamma(shape=alpha, rate=beta) iid,  alpha = 1.8 (fixed)
    beta ~ Gamma(shape=0.1, rate=1.0)

Full conditionals (standard Poisson-Gamma / Gamma-Gamma conjugacy):
    theta_i | y_i, beta ~ Gamma(shape = alpha + y_i, rate = beta + t_i)
    beta | theta         ~ Gamma(shape = 0.1 + 10*alpha, rate = 1.0 + sum(theta))
"""
import numpy as np

T = np.array([10, 20, 15, 30, 25, 5, 40, 8, 12, 18], dtype=float)
Y = np.array([1, 0, 3, 1, 19, 0, 1, 5, 0, 0], dtype=float)
ALPHA = 1.8
N_PUMPS = 10


def run_pump_gibbs(n_iter, seed, init_beta=1.0):
    """Runs the pump Gibbs sampler for n_iter iterations (no warm-up
    discarded, no thinning -- raw output per the saved-chain specification).
    Returns an (n_iter, 11) array: columns theta_1..theta_10, beta.
    """
    rng = np.random.default_rng(seed)
    theta = np.full(N_PUMPS, 0.5)  # arbitrary transient start; beta drives init
    beta = init_beta
    out = np.empty((n_iter, N_PUMPS + 1))
    for it in range(n_iter):
        # draw theta_i | beta
        shape_theta = ALPHA + Y
        rate_theta = beta + T
        theta = rng.gamma(shape=shape_theta, scale=1.0 / rate_theta)
        # draw beta | theta
        shape_beta = 0.1 + N_PUMPS * ALPHA
        rate_beta = 1.0 + theta.sum()
        beta = rng.gamma(shape=shape_beta, scale=1.0 / rate_beta)
        out[it, :N_PUMPS] = theta
        out[it, N_PUMPS] = beta
    return out


if __name__ == "__main__":
    chain = run_pump_gibbs(20000, seed=101, init_beta=1.0)
    print("chain shape:", chain.shape)
    print("post-mean (burn-in 2000 discarded), theta_1..10, beta:")
    print(chain[2000:].mean(axis=0))
