"""
PS7.6 reference implementation -- Type D failure case: well-separated
bimodal mixture target, RW-MH with a deliberately small proposal scale,
single start in one mode. Documents the failure (stuck chain) against the
known true mixture mean/variance. This is the "failing export" chain
consumed by Module 8 (R-hat on a failing sampler) and the capstone
diagnose->adjust->rerun loop.
"""
import numpy as np

MU1, MU2, SD = -5.0, 5.0, 1.0  # well-separated equal-weight bimodal mixture

def target_logpdf(theta):
    # log of 0.5*N(theta;MU1,SD^2) + 0.5*N(theta;MU2,SD^2), via log-sum-exp
    lp1 = -0.5*((theta-MU1)/SD)**2 - np.log(SD*np.sqrt(2*np.pi))
    lp2 = -0.5*((theta-MU2)/SD)**2 - np.log(SD*np.sqrt(2*np.pi))
    m = max(lp1, lp2)
    return m + np.log(0.5*np.exp(lp1-m) + 0.5*np.exp(lp2-m))

def true_moments():
    mean = 0.5*MU1 + 0.5*MU2
    ex2 = 0.5*(SD**2+MU1**2) + 0.5*(SD**2+MU2**2)
    var = ex2 - mean**2
    return mean, var

def rw_mh(delta, n_iter, seed, theta0):
    rng = np.random.default_rng(seed)
    theta = np.empty(n_iter)
    cur = theta0
    cur_lp = target_logpdf(cur)
    n_accept = 0
    for t in range(n_iter):
        prop = cur + delta*rng.normal()
        prop_lp = target_logpdf(prop)
        if np.log(rng.uniform()) < (prop_lp - cur_lp):
            cur, cur_lp = prop, prop_lp
            n_accept += 1
        theta[t] = cur
    return theta, n_accept/n_iter

if __name__ == '__main__':
    true_mean, true_var = true_moments()
    print(f"True mixture moments: mean={true_mean}, var={true_var}")

    n_iter = 20000
    delta_small = 0.5
    theta0 = -5.0  # start in the left mode

    chain, acc = rw_mh(delta_small, n_iter, seed=0, theta0=theta0)
    print(f"\n=== Seed 0 logged run: delta={delta_small}, theta0={theta0}, n_iter={n_iter} ===")
    print(f"acceptance rate: {acc:.4f}")
    print(f"sample mean: {chain.mean():.4f} (true={true_mean}, |diff|={abs(chain.mean()-true_mean):.4f})")
    print(f"sample var:  {chain.var(ddof=1):.4f} (true={true_var}, |diff|={abs(chain.var(ddof=1)-true_var):.4f})")
    print(f"fraction of iterations with theta > 0 (i.e. visited right mode): {np.mean(chain>0):.4f}")
    print(f"min/max of chain: {chain.min():.4f} / {chain.max():.4f}")

    # Calibration: how consistently does this configuration get stuck?
    n_cal = 50
    means, varss, right_mode_fracs, accs = [], [], [], []
    for s in range(5000, 5000+n_cal):
        ch, a = rw_mh(delta_small, n_iter, seed=s, theta0=theta0)
        means.append(ch.mean())
        varss.append(ch.var(ddof=1))
        right_mode_fracs.append(np.mean(ch>0))
        accs.append(a)
    means, varss, right_mode_fracs, accs = map(np.array, (means, varss, right_mode_fracs, accs))
    print(f"\n=== Calibration ({n_cal} seeds, same delta/theta0/n_iter) ===")
    print(f"sample mean: mean={means.mean():.4f} min={means.min():.4f} max={means.max():.4f}")
    print(f"sample var:  mean={varss.mean():.4f} min={varss.min():.4f} max={varss.max():.4f}")
    print(f"right-mode visit fraction: mean={right_mode_fracs.mean():.4f} max={right_mode_fracs.max():.4f} "
          f"(fraction of the {n_cal} seeds that ever crossed to theta>0 at all: {np.mean(right_mode_fracs>0):.4f})")
    print(f"acceptance rate: mean={accs.mean():.4f} min={accs.min():.4f} max={accs.max():.4f}")

    # Contrast: a well-tuned (larger-scale) sampler for comparison, same seed/start
    delta_good = 6.0
    chain_good, acc_good = rw_mh(delta_good, n_iter, seed=0, theta0=theta0)
    print(f"\n=== Contrast: delta={delta_good} (well-tuned), same seed/start ===")
    print(f"acceptance rate: {acc_good:.4f}")
    print(f"sample mean: {chain_good.mean():.4f} (|diff|={abs(chain_good.mean()-true_mean):.4f})")
    print(f"sample var:  {chain_good.var(ddof=1):.4f} (|diff|={abs(chain_good.var(ddof=1)-true_var):.4f})")
    print(f"fraction visiting right mode: {np.mean(chain_good>0):.4f}")
