"""
Reference re-implementation of the PS7.6 well-separated bimodal-mixture
RW-Metropolis sampler, per the exact model/spec logged in
ValidationLog_0_3.md (PS7.6 entry). Used here only as the "student's own
stored failing chain" input to Module 8 diagnostics problems, never to
re-verify PS7.6 itself.

Target: 0.5*N(-5,1) + 0.5*N(5,1)   (true mean 0, true variance 26)
Proposal: theta' = theta + delta * Z,  Z ~ N(0,1)  (symmetric RW proposal,
    delta is the proposal SD)
"""
import numpy as np


def log_target_unnorm(x):
    # log of 0.5*N(-5,1) + 0.5*N(5,1) density (unnormalized constant cancels
    # in the M-H ratio; kept in normalized form here for direct evaluation)
    d1 = np.exp(-0.5 * (x + 5.0) ** 2)
    d2 = np.exp(-0.5 * (x - 5.0) ** 2)
    dens = 0.5 * d1 + 0.5 * d2
    return np.log(dens)


def run_bimodal_mh(n_iter, seed, delta, theta0=-5.0):
    """Runs the RW-MH sampler for n_iter iterations (no warm-up discarded,
    no thinning). Returns (chain, n_accept) where chain has shape (n_iter,).
    """
    rng = np.random.default_rng(seed)
    theta = theta0
    log_p_cur = log_target_unnorm(theta)
    chain = np.empty(n_iter)
    n_accept = 0
    for it in range(n_iter):
        prop = theta + delta * rng.standard_normal()
        log_p_prop = log_target_unnorm(prop)
        log_ratio = log_p_prop - log_p_cur
        if np.log(rng.uniform()) < log_ratio:
            theta = prop
            log_p_cur = log_p_prop
            n_accept += 1
        chain[it] = theta
    return chain, n_accept


if __name__ == "__main__":
    chain, n_acc = run_bimodal_mh(20000, seed=0, delta=0.5, theta0=-5.0)
    print("acceptance rate:", n_acc / 20000)
    print("sample mean:", chain.mean())
    print("sample var:", chain.var(ddof=1))
    print("frac theta>0:", (chain > 0).mean())
    print("range:", chain.min(), chain.max())
