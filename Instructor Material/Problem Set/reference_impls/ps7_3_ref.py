"""
PS7.3 reference implementation -- two-stage Gibbs sampler on the canonical
Binomial(n, Y) / Beta(x+alpha, n-x+beta) joint (Casella & George's classic
Gibbs-sampler pair), whose X-marginal is the Beta-Binomial(n, alpha, beta)
compound distribution (closed form). Cross-checked against direct ancestral
sampling (Y ~ Beta(alpha,beta), X|Y ~ Binomial(n,Y)) and the closed-form
mean/variance.
"""
import numpy as np
from scipy.special import betaln, gammaln

n, alpha, beta = 20, 2.0, 3.0

def beta_binomial_logpmf(k, n, a, b):
    return (gammaln(n+1) - gammaln(k+1) - gammaln(n-k+1)
            + betaln(k+a, n-k+b) - betaln(a, b))

def beta_binomial_mean_var(n, a, b):
    mean = n*a/(a+b)
    var = n*a*b*(a+b+n) / ((a+b)**2 * (a+b+1))
    return mean, var

def gibbs_run(n_iter, burn_in, seed, n=n, a=alpha, b=beta):
    rng = np.random.default_rng(seed)
    y = rng.beta(a, b)  # arbitrary init
    xs = np.empty(n_iter)
    for t in range(n_iter):
        x = rng.binomial(n, y)
        y = rng.beta(x + a, n - x + b)
        xs[t] = x
    return xs[burn_in:]

def direct_run(n_draws, seed, n=n, a=alpha, b=beta):
    rng = np.random.default_rng(seed)
    y = rng.beta(a, b, size=n_draws)
    x = rng.binomial(n, y)
    return x

if __name__ == '__main__':
    mean_true, var_true = beta_binomial_mean_var(n, alpha, beta)
    print(f"Closed-form Beta-Binomial(n={n}, a={alpha}, b={beta}): mean={mean_true}, var={var_true}")

    # Logged reference run
    n_iter, burn_in = 20000, 1000
    gibbs_x = gibbs_run(n_iter, burn_in, seed=0)
    direct_x = direct_run(n_iter - burn_in, seed=0)

    print("\n=== Seed 0 logged run ===")
    print(f"Gibbs  (N={len(gibbs_x)}): mean={gibbs_x.mean():.4f} (|diff from true|={abs(gibbs_x.mean()-mean_true):.4f}), "
          f"var={gibbs_x.var(ddof=1):.4f} (|diff|={abs(gibbs_x.var(ddof=1)-var_true):.4f})")
    print(f"Direct (N={len(direct_x)}): mean={direct_x.mean():.4f} (|diff from true|={abs(direct_x.mean()-mean_true):.4f}), "
          f"var={direct_x.var(ddof=1):.4f} (|diff|={abs(direct_x.var(ddof=1)-var_true):.4f})")
    print(f"|Gibbs mean - Direct mean| = {abs(gibbs_x.mean()-direct_x.mean()):.4f}")
    print(f"|Gibbs var  - Direct var | = {abs(gibbs_x.var(ddof=1)-direct_x.var(ddof=1)):.4f}")

    # histogram overlay check: compare empirical pmf (binned exactly, since X is integer 0..n) to closed form
    print("\nPer-value |empirical - closed-form| pmf gap (Gibbs vs direct), k=0..20:")
    max_gap_gibbs, max_gap_direct = 0.0, 0.0
    for k in range(n+1):
        p_true = np.exp(beta_binomial_logpmf(k, n, alpha, beta))
        p_gibbs = np.mean(gibbs_x == k)
        p_direct = np.mean(direct_x == k)
        max_gap_gibbs = max(max_gap_gibbs, abs(p_gibbs - p_true))
        max_gap_direct = max(max_gap_direct, abs(p_direct - p_true))
    print(f"max |empirical pmf - true pmf| over k=0..20: Gibbs={max_gap_gibbs:.4f}, Direct={max_gap_direct:.4f}")

    # Calibration over many seeds
    n_cal = 150
    mean_diffs_gibbs, var_diffs_gibbs = [], []
    mean_diffs_direct, var_diffs_direct = [], []
    cross_mean_diffs, cross_var_diffs = [], []
    max_pmf_gaps_gibbs = []
    for s in range(3000, 3000+n_cal):
        gx = gibbs_run(n_iter, burn_in, seed=s)
        dx = direct_run(n_iter - burn_in, seed=s+50000)
        mean_diffs_gibbs.append(abs(gx.mean() - mean_true))
        var_diffs_gibbs.append(abs(gx.var(ddof=1) - var_true))
        mean_diffs_direct.append(abs(dx.mean() - mean_true))
        var_diffs_direct.append(abs(dx.var(ddof=1) - var_true))
        cross_mean_diffs.append(abs(gx.mean() - dx.mean()))
        cross_var_diffs.append(abs(gx.var(ddof=1) - dx.var(ddof=1)))
        gap = max(abs(np.mean(gx==k) - np.exp(beta_binomial_logpmf(k,n,alpha,beta))) for k in range(n+1))
        max_pmf_gaps_gibbs.append(gap)

    def stats(a):
        a = np.array(a)
        return a.mean(), a.max(), np.percentile(a, 99)

    print(f"\n=== Calibration ({n_cal} seeds) ===")
    print(f"Gibbs mean-diff:  mean={stats(mean_diffs_gibbs)[0]:.4f} max={stats(mean_diffs_gibbs)[1]:.4f} 99th={stats(mean_diffs_gibbs)[2]:.4f}")
    print(f"Gibbs var-diff:   mean={stats(var_diffs_gibbs)[0]:.4f} max={stats(var_diffs_gibbs)[1]:.4f} 99th={stats(var_diffs_gibbs)[2]:.4f}")
    print(f"Direct mean-diff: mean={stats(mean_diffs_direct)[0]:.4f} max={stats(mean_diffs_direct)[1]:.4f} 99th={stats(mean_diffs_direct)[2]:.4f}")
    print(f"Direct var-diff:  mean={stats(var_diffs_direct)[0]:.4f} max={stats(var_diffs_direct)[1]:.4f} 99th={stats(var_diffs_direct)[2]:.4f}")
    print(f"Cross mean-diff:  mean={stats(cross_mean_diffs)[0]:.4f} max={stats(cross_mean_diffs)[1]:.4f} 99th={stats(cross_mean_diffs)[2]:.4f}")
    print(f"Cross var-diff:   mean={stats(cross_var_diffs)[0]:.4f} max={stats(cross_var_diffs)[1]:.4f} 99th={stats(cross_var_diffs)[2]:.4f}")
    print(f"Gibbs max-pmf-gap: mean={stats(max_pmf_gaps_gibbs)[0]:.4f} max={stats(max_pmf_gaps_gibbs)[1]:.4f} 99th={stats(max_pmf_gaps_gibbs)[2]:.4f}")
