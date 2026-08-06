"""
PS3.5 reference implementation.
AR(1) serially dependent synthetic series (known mean=0, known phi, known
innovation sd) -- compare naive i.i.d. bootstrap (ignores dependence) vs.
moving blocks bootstrap (MBB, at >=2 block lengths) confidence-interval widths
for the mean. Naive bootstrap should under-cover / produce intervals that are
too narrow relative to the true (autocorrelation-inflated) sampling variance of
the mean; MBB should produce noticeably wider, more nearly-correct intervals.

Tier-2 anchor (standard time series fact): for a stationary AR(1) with lag-1
correlation phi and innovation variance sigma^2, the marginal variance is
sigma_X^2 = sigma^2/(1-phi^2), and for large n the variance of the sample mean
is approximately (sigma_X^2/n) * (1+phi)/(1-phi) -- the "inefficiency factor"
(1+phi)/(1-phi) from positive autocorrelation inflating the naive iid variance.
"""
import numpy as np

PHI = 0.7
SIGMA_INNOV = 1.0
N = 200


def true_se_naive_and_correct():
    sigma_x2 = SIGMA_INNOV**2 / (1 - PHI**2)
    sigma_x = np.sqrt(sigma_x2)
    naive_se = sigma_x / np.sqrt(N)
    inflation = (1 + PHI) / (1 - PHI)
    correct_se = sigma_x / np.sqrt(N) * np.sqrt(inflation)
    return naive_se, correct_se, inflation


def gen_ar1(n, phi, sigma, seed, burn_in=500):
    rng = np.random.default_rng(seed)
    total = n + burn_in
    eps = rng.normal(0, sigma, size=total)
    x = np.empty(total)
    x[0] = eps[0] / np.sqrt(1 - phi**2)  # start near stationary variance
    for t in range(1, total):
        x[t] = phi * x[t-1] + eps[t]
    return x[burn_in:]


def naive_bootstrap_ci(data, r, seed, alpha=0.05):
    rng = np.random.default_rng(seed)
    n = len(data)
    idx = rng.integers(0, n, size=(r, n))
    means = data[idx].mean(axis=1)
    lo, hi = np.percentile(means, [100*alpha/2, 100*(1-alpha/2)])
    return hi - lo, means.std(ddof=1)


def moving_blocks_bootstrap_ci(data, block_len, r, seed, alpha=0.05):
    rng = np.random.default_rng(seed)
    n = len(data)
    n_blocks_needed = int(np.ceil(n / block_len))
    n_starts = n - block_len + 1  # overlapping block start positions
    means = np.empty(r)
    for b in range(r):
        starts = rng.integers(0, n_starts, size=n_blocks_needed)
        resample = np.concatenate([data[s:s+block_len] for s in starts])[:n]
        means[b] = resample.mean()
    lo, hi = np.percentile(means, [100*alpha/2, 100*(1-alpha/2)])
    return hi - lo, means.std(ddof=1)


def run_once(data_seed, boot_seed, r=3000, block_lens=(5, 20)):
    data = gen_ar1(N, PHI, SIGMA_INNOV, seed=data_seed)
    naive_width, naive_se = naive_bootstrap_ci(data, r, seed=boot_seed)
    results = {"naive_width": naive_width, "naive_se": naive_se}
    for L in block_lens:
        w, se = moving_blocks_bootstrap_ci(data, L, r, seed=boot_seed + L)
        results[f"mbb_L{L}_width"] = w
        results[f"mbb_L{L}_se"] = se
    return results


if __name__ == "__main__":
    naive_se_theory, correct_se_theory, inflation = true_se_naive_and_correct()
    print(f"theory: naive (iid-assumption) SE = {naive_se_theory:.4f}, "
          f"correct (AR(1)-aware) SE = {correct_se_theory:.4f}, inflation factor = {inflation:.3f}")

    print("\n=== PRIMARY LOGGED RUN (data_seed=99, boot_seed=99, r=3000) ===")
    p = run_once(99, 99)
    for k, v in p.items():
        print(f"  {k} = {v:.4f}")
    print(f"  mbb_L20_width / naive_width = {p['mbb_L20_width']/p['naive_width']:.3f}")
    print(f"  mbb_L5_width  / naive_width = {p['mbb_L5_width']/p['naive_width']:.3f}")
    print(f"  mbb_L20_se / correct_se_theory = {p['mbb_L20_se']/correct_se_theory:.3f}")
    print(f"  naive_se / naive_se_theory = {p['naive_se']/naive_se_theory:.3f}")

    print("\n=== CALIBRATION (10 data seeds) ===")
    ratio_L20 = []
    ratio_L5 = []
    mbb20_over_theory = []
    naive_over_theory = []
    for ds in range(200, 210):
        r = run_once(ds, ds+1000)
        ratio_L20.append(r['mbb_L20_width']/r['naive_width'])
        ratio_L5.append(r['mbb_L5_width']/r['naive_width'])
        mbb20_over_theory.append(r['mbb_L20_se']/correct_se_theory)
        naive_over_theory.append(r['naive_se']/naive_se_theory)
        print(f"  seed={ds}: naive_w={r['naive_width']:.4f} L5_w={r['mbb_L5_width']:.4f} "
              f"L20_w={r['mbb_L20_width']:.4f}  L20/naive={ratio_L20[-1]:.3f}  L5/naive={ratio_L5[-1]:.3f}")
    print("\nL20/naive width ratio range:", min(ratio_L20), max(ratio_L20))
    print("L5/naive width ratio range:", min(ratio_L5), max(ratio_L5))
    print("mbb_L20_se / correct_se_theory range:", min(mbb20_over_theory), max(mbb20_over_theory))
    print("naive_se / naive_se_theory range:", min(naive_over_theory), max(naive_over_theory))
