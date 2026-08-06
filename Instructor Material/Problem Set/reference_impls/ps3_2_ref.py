"""
PS3.2 reference implementation.
Small synthetic dataset with KNOWN generative truth: n=20 draws from
Exponential(mean=10) (rate=0.1). Compare:
  - nonparametric bootstrap SE of the sample mean (resample the 20 observed values)
  - parametric bootstrap SE of the sample mean (fit exponential MLE rate-hat = 1/xbar,
    then simulate NEW samples of size n from Exponential(rate-hat))
  - the true theoretical SE = true_mean/sqrt(n) (closed-form fact: for Exponential,
    sd = mean, so SE(mean) = mean/sqrt(n))
"""
import numpy as np

TRUE_MEAN = 10.0
N = 20
R = 10000


def nonparam_boot_se(data, r, seed):
    rng = np.random.default_rng(seed)
    n = len(data)
    means = np.empty(r)
    for i in range(r):
        idx = rng.integers(0, n, size=n)
        means[i] = data[idx].mean()
    return means.std(ddof=1), means


def param_boot_se(xbar_hat, n, r, seed):
    rng = np.random.default_rng(seed)
    means = np.empty(r)
    for i in range(r):
        # Exponential MLE: rate_hat = 1/xbar_hat  <=>  scale (numpy convention) = xbar_hat
        sample = rng.exponential(scale=xbar_hat, size=n)
        means[i] = sample.mean()
    return means.std(ddof=1), means


def run_once(data_seed, boot_seed_np, boot_seed_p, r=R):
    rng_data = np.random.default_rng(data_seed)
    data = rng_data.exponential(scale=TRUE_MEAN, size=N)
    xbar = data.mean()
    s = data.std(ddof=1)

    nonparam_se, _ = nonparam_boot_se(data, r, boot_seed_np)
    param_se, _ = param_boot_se(xbar, N, r, boot_seed_p)

    true_se = TRUE_MEAN / np.sqrt(N)          # closed-form, uses the TRUE mean (unknown to fitter)
    plugin_param_target = xbar / np.sqrt(N)    # what the parametric bootstrap should closely match
    narrowness_factor = np.sqrt((N - 1) / N)
    nonparam_predicted = (s / np.sqrt(N)) * narrowness_factor

    return dict(xbar=xbar, s=s, nonparam_se=nonparam_se, param_se=param_se,
                true_se=true_se, plugin_param_target=plugin_param_target,
                nonparam_predicted=nonparam_predicted,
                s_over_sqrtn=s/np.sqrt(N))


if __name__ == "__main__":
    print("=== PRIMARY LOGGED RUN (data_seed=7, boot_seed_np=7, boot_seed_p=7) ===")
    p = run_once(7, 7, 7)
    for k, v in p.items():
        print(f"  {k} = {v:.5f}")
    print("  param_se / plugin_param_target =", p["param_se"]/p["plugin_param_target"])
    print("  nonparam_se / nonparam_predicted =", p["nonparam_se"]/p["nonparam_predicted"])
    print("  nonparam_se / param_se =", p["nonparam_se"]/p["param_se"])

    print("\n=== CALIBRATION (20 different data seeds) ===")
    param_over_plugin = []
    nonparam_over_predicted = []
    param_se_list = []
    nonparam_se_list = []
    xbar_list = []
    ratio_np_p = []
    for i, ds in enumerate(range(100, 120)):
        r = run_once(ds, ds+1, ds+2)
        param_over_plugin.append(r["param_se"]/r["plugin_param_target"])
        nonparam_over_predicted.append(r["nonparam_se"]/r["nonparam_predicted"])
        param_se_list.append(r["param_se"])
        nonparam_se_list.append(r["nonparam_se"])
        xbar_list.append(r["xbar"])
        ratio_np_p.append(r["nonparam_se"]/r["param_se"])
        print(f"  seed={ds}: xbar={r['xbar']:.3f} param_se={r['param_se']:.4f} "
              f"nonparam_se={r['nonparam_se']:.4f} true_se={r['true_se']:.4f} "
              f"param/plugin={param_over_plugin[-1]:.4f} nonparam/predicted={nonparam_over_predicted[-1]:.4f}")

    print("\nparam_se/plugin_target range:", min(param_over_plugin), max(param_over_plugin))
    print("nonparam_se/predicted range:", min(nonparam_over_predicted), max(nonparam_over_predicted))
    print("param_se range:", min(param_se_list), max(param_se_list))
    print("nonparam_se range:", min(nonparam_se_list), max(nonparam_se_list))
    print("xbar range:", min(xbar_list), max(xbar_list))
    print("nonparam_se/param_se ratio range:", min(ratio_np_p), max(ratio_np_p))
