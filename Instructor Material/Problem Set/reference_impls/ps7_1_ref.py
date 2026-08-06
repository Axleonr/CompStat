"""
PS7.1 reference implementation -- CORRECTED after confirming the actual
PS2.3 text (previously unavailable; see Flag 1 follow-up).

PS2.3's log_importance_ratios(theta_draws, data) is NOT a generic-likelihood
function -- it is hard-wired to the bioassay Binomial-logistic log-likelihood
form (data = the 4-group dose/animals/deaths table; theta_draws = (alpha,beta)
pairs). "Literal reuse" therefore requires PS7.1 to use the SAME model/data/
prior as PS2.3 (not a different univariate normal-normal target, which was
the flawed first draft). Since the bioassay posterior has no closed form,
the SIR resampled-sample moments are checked against a large-N self-
normalized IS estimate from the SAME weighted draws (R1.3 cross-method-style
agreement) -- the same pattern already established by PS2.6 in Module 2
("resampled empirical mean reproduces the weighted estimate"), scaled up to
two resample sizes and both with/without replacement.
"""
import numpy as np

# Exact PS2.3 data (4-row bioassay table)
X = np.array([-0.86, -0.30, -0.05, 0.73])
N_ANIMALS = np.array([5, 5, 5, 5])
Y_DEATHS = np.array([0, 1, 3, 5])

# Exact PS2.3 prior = proposal: (alpha,beta) ~ N(mu, cov)
MU = np.array([0.0, 10.0])
SD_A, SD_B, RHO = 2.0, 10.0, 0.6
COV = np.array([[SD_A**2, RHO*SD_A*SD_B], [RHO*SD_A*SD_B, SD_B**2]])

def log_importance_ratios(theta_draws, data):
    x, n, y = data
    alpha, beta = theta_draws[:, 0], theta_draws[:, 1]
    logit = alpha[:, None] + beta[:, None]*x[None, :]
    log_theta = -np.logaddexp(0, -logit)
    log_1m_theta = -np.logaddexp(0, logit)
    return (y[None, :]*log_theta + (n-y)[None, :]*log_1m_theta).sum(axis=1)

def normalize_weights(log_ratios):
    m = np.max(log_ratios)
    w = np.exp(log_ratios - m)
    return w/w.sum()

def is_ess(log_ratios):
    w = normalize_weights(log_ratios)
    return 1.0/np.sum(w**2)

def is_estimate(h_values, weights):
    return np.sum(weights*h_values)/np.sum(weights)

def run_once(seed, N, M_small, M_large):
    rng = np.random.default_rng(seed)
    theta = rng.multivariate_normal(MU, COV, size=N)
    lr = log_importance_ratios(theta, (X, N_ANIMALS, Y_DEATHS))
    w = normalize_weights(lr)
    ess = is_ess(lr)

    ref_mean_a = is_estimate(theta[:, 0], w)
    ref_mean_b = is_estimate(theta[:, 1], w)
    ref_var_a = is_estimate(theta[:, 0]**2, w) - ref_mean_a**2
    ref_var_b = is_estimate(theta[:, 1]**2, w) - ref_mean_b**2

    results = {}
    for M in (M_small, M_large):
        idx_r = rng.choice(N, size=M, replace=True, p=w)
        idx_n = rng.choice(N, size=M, replace=False, p=w)
        samp_r, samp_n = theta[idx_r], theta[idx_n]
        results[M] = {
            'with_replacement': (samp_r[:,0].mean(), samp_r[:,0].var(ddof=1),
                                  samp_r[:,1].mean(), samp_r[:,1].var(ddof=1)),
            'without_replacement': (samp_n[:,0].mean(), samp_n[:,0].var(ddof=1),
                                     samp_n[:,1].mean(), samp_n[:,1].var(ddof=1)),
        }
    return {'ess': ess, 'ess_pct': 100*ess/N,
            'ref_mean_a': ref_mean_a, 'ref_mean_b': ref_mean_b,
            'ref_var_a': ref_var_a, 'ref_var_b': ref_var_b,
            'results': results}

if __name__ == '__main__':
    N, M_small, M_large = 50000, 1000, 5000

    out0 = run_once(seed=0, N=N, M_small=M_small, M_large=M_large)
    print("=== Seed 0 logged run ===")
    print(f"ESS = {out0['ess']:.2f} ({out0['ess_pct']:.2f}% of N={N})")
    print(f"Reference (large-N IS-weighted): mean_alpha={out0['ref_mean_a']:.4f}, mean_beta={out0['ref_mean_b']:.4f}, "
          f"var_alpha={out0['ref_var_a']:.4f}, var_beta={out0['ref_var_b']:.4f}")
    for M in (M_small, M_large):
        for mode in ('with_replacement', 'without_replacement'):
            ma, va, mb, vb = out0['results'][M][mode]
            print(f"  M={M:5d} {mode:20s}: alpha mean={ma:.4f} (|diff|={abs(ma-out0['ref_mean_a']):.4f}) "
                  f"var={va:.4f} (|diff|={abs(va-out0['ref_var_a']):.4f}) | "
                  f"beta mean={mb:.4f} (|diff|={abs(mb-out0['ref_mean_b']):.4f}) "
                  f"var={vb:.4f} (|diff|={abs(vb-out0['ref_var_b']):.4f})")

    n_cal = 200
    diffs = {M: {mode: {'ma':[], 'va':[], 'mb':[], 'vb':[]} for mode in ('with_replacement','without_replacement')} for M in (M_small,M_large)}
    ess_pcts = []
    for s in range(1000, 1000+n_cal):
        out = run_once(seed=s, N=N, M_small=M_small, M_large=M_large)
        ess_pcts.append(out['ess_pct'])
        for M in (M_small, M_large):
            for mode in ('with_replacement','without_replacement'):
                ma, va, mb, vb = out['results'][M][mode]
                diffs[M][mode]['ma'].append(abs(ma-out['ref_mean_a']))
                diffs[M][mode]['va'].append(abs(va-out['ref_var_a']))
                diffs[M][mode]['mb'].append(abs(mb-out['ref_mean_b']))
                diffs[M][mode]['vb'].append(abs(vb-out['ref_var_b']))

    print(f"\n=== Calibration (200 seeds) ===")
    print(f"ESS%: mean={np.mean(ess_pcts):.2f} min={np.min(ess_pcts):.2f} max={np.max(ess_pcts):.2f}")
    for M in (M_small, M_large):
        for mode in ('with_replacement','without_replacement'):
            d = diffs[M][mode]
            print(f"  M={M:5d} {mode:20s}: |alpha mean diff| max={np.max(d['ma']):.4f} 99th={np.percentile(d['ma'],99):.4f} | "
                  f"|alpha var diff| max={np.max(d['va']):.4f} 99th={np.percentile(d['va'],99):.4f} | "
                  f"|beta mean diff| max={np.max(d['mb']):.4f} 99th={np.percentile(d['mb'],99):.4f} | "
                  f"|beta var diff| max={np.max(d['vb']):.4f} 99th={np.percentile(d['vb'],99):.4f}")
