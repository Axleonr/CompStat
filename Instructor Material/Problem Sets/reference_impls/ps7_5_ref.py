"""
PS7.5 reference implementation -- Metropolis-within-Gibbs.
Original adaptation (no numbered R&C exercise; informed by Sec 7.6.3's
narrative of a non-conjugate conditional handled by a random-walk MH step
inside Gibbs).

Model:
    x_i | mu, sigma ~ N(mu, sigma^2), i=1..n
    mu    ~ N(mu0, tau0^2)         (conjugate -> closed-form full conditional)
    sigma ~ HalfCauchy(0, s0)      (non-conjugate -> no standard full conditional)

Full conditionals:
    mu | sigma, data ~ N(mu_n, tau_n^2)      [standard normal-normal conjugacy]
    sigma | mu, data:  no closed form -> random-walk MH step (reusing the
        PS7.2 RW-MH machinery) targeting
        p(sigma | mu, data) ∝ sigma^{-n} exp(-sum((x-mu)^2)/(2 sigma^2)) * HalfCauchy_pdf(sigma; s0)
"""
import numpy as np

def half_cauchy_logpdf(sigma, s0):
    if sigma <= 0:
        return -np.inf
    return np.log(2.0) - np.log(np.pi*s0) - np.log(1.0 + (sigma/s0)**2)

def log_target_sigma(sigma, mu, x, s0):
    if sigma <= 0:
        return -np.inf
    n = len(x)
    ss = np.sum((x-mu)**2)
    return -n*np.log(sigma) - ss/(2*sigma**2) + half_cauchy_logpdf(sigma, s0)

def mwg_sampler(x, n_iter, seed, mu0=0.0, tau0_sq=100.0, s0=5.0,
                delta_sigma=0.5, sigma_init=1.0, mu_init=0.0):
    rng = np.random.default_rng(seed)
    n = len(x)
    xbar = x.mean()
    mu, sigma = mu_init, sigma_init
    mus = np.empty(n_iter)
    sigmas = np.empty(n_iter)
    n_accept = 0
    for t in range(n_iter):
        # Gibbs step 1: mu | sigma, data -- conjugate, direct draw
        tau_n_sq = 1.0/(1.0/tau0_sq + n/sigma**2)
        mu_n = tau_n_sq*(mu0/tau0_sq + n*xbar/sigma**2)
        mu = rng.normal(mu_n, np.sqrt(tau_n_sq))

        # Gibbs step 2: sigma | mu, data -- non-conjugate, RW-MH step
        cur_lp = log_target_sigma(sigma, mu, x, s0)
        prop = sigma + delta_sigma*rng.normal()
        prop_lp = log_target_sigma(prop, mu, x, s0)
        if np.log(rng.uniform()) < (prop_lp - cur_lp):
            sigma = prop
            n_accept += 1

        mus[t] = mu
        sigmas[t] = sigma
    return mus, sigmas, n_accept/n_iter

def gen_data(seed, n=50, mu_true=5.0, sigma_true=2.0):
    rng = np.random.default_rng(seed)
    return rng.normal(mu_true, sigma_true, size=n)

if __name__ == '__main__':
    mu_true, sigma_true, n = 5.0, 2.0, 50
    x = gen_data(seed=0, n=n, mu_true=mu_true, sigma_true=sigma_true)
    print(f"Synthetic data: n={n}, true mu={mu_true}, true sigma={sigma_true}, xbar={x.mean():.4f}, s={x.std(ddof=1):.4f}")

    n_iter, burn_in = 20000, 2000
    mus, sigmas, acc = mwg_sampler(x, n_iter, seed=0, delta_sigma=0.5)
    print(f"\nSigma-step acceptance rate: {acc:.4f}")
    mu_post = mus[burn_in:]
    sigma_post = sigmas[burn_in:]
    print(f"Posterior mean mu = {mu_post.mean():.4f} (|diff from true|={abs(mu_post.mean()-mu_true):.4f}), "
          f"95% CI=({np.percentile(mu_post,2.5):.4f},{np.percentile(mu_post,97.5):.4f})")
    print(f"Posterior mean sigma = {sigma_post.mean():.4f} (|diff from true|={abs(sigma_post.mean()-sigma_true):.4f}), "
          f"95% CI=({np.percentile(sigma_post,2.5):.4f},{np.percentile(sigma_post,97.5):.4f})")

    # Calibration across seeds
    n_cal = 100
    mu_diffs, sigma_diffs, accs = [], [], []
    for s in range(4000, 4000+n_cal):
        xs = gen_data(seed=s, n=n, mu_true=mu_true, sigma_true=sigma_true)
        ms, ss, a = mwg_sampler(xs, n_iter, seed=s+7000, delta_sigma=0.5)
        mu_diffs.append(abs(ms[burn_in:].mean()-mu_true))
        sigma_diffs.append(abs(ss[burn_in:].mean()-sigma_true))
        accs.append(a)
    mu_diffs, sigma_diffs, accs = map(np.array, (mu_diffs, sigma_diffs, accs))
    print(f"\n=== Calibration ({n_cal} seeds) ===")
    print(f"|mu post-mean - true| mean={mu_diffs.mean():.4f} max={mu_diffs.max():.4f} 99th={np.percentile(mu_diffs,99):.4f}")
    print(f"|sigma post-mean - true| mean={sigma_diffs.mean():.4f} max={sigma_diffs.max():.4f} 99th={np.percentile(sigma_diffs,99):.4f}")
    print(f"sigma-step acceptance rate: mean={accs.mean():.4f} min={accs.min():.4f} max={accs.max():.4f}")
