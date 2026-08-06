"""
PS3.6 reference implementation.
Type C: instrument the bootstrap itself as an algorithm. Using the CLEC-mirror
data from PS3.1, for several resample counts r, repeat the WHOLE nonparametric
bootstrap K times (different seeds) and measure how much the resulting bootstrap
SE estimate itself varies across those K replications -- this "Monte Carlo SE of
the bootstrap SE" should shrink like 1/sqrt(r), directly paralleling Module 1/2's
n^(-1/2) Monte Carlo error reasoning, applied one level up (MC error of an MC
estimate). Tier-1 citation: Hesterberg (2015) Sec. 3.6 (H-7) recommends r>=15,000
for 10%-accurate percentile/bootstrap-t endpoints -- used here as guidance to
interpret the r-sweep, not re-derived from scratch.
"""
import numpy as np

CLEC = np.array([0.4, 11.3, 11.6, 44.5, 0.1, 51.1, 12.2, 12.1, 35.5, 56.7, 4.1, 0.1,
                 2.1, 52.7, 7.6, 42.6, 0.7, 3.2, 3.3, 1.6, 1.2, 14.4, 10.2])


def one_bootstrap_se(data, r, seed):
    rng = np.random.default_rng(seed)
    n = len(data)
    idx = rng.integers(0, n, size=(r, n))
    means = data[idx].mean(axis=1)
    return means.std(ddof=1)


def one_bootstrap_percentile(data, r, seed, q=97.5):
    rng = np.random.default_rng(seed)
    n = len(data)
    idx = rng.integers(0, n, size=(r, n))
    means = data[idx].mean(axis=1)
    return np.percentile(means, q)


def mc_noise_of_bootstrap_se(data, r, K, base_seed):
    ses = np.array([one_bootstrap_se(data, r, seed=base_seed + k) for k in range(K)])
    return ses.std(ddof=1), ses.mean()


def mc_noise_of_percentile(data, r, K, base_seed, q=97.5):
    qs = np.array([one_bootstrap_percentile(data, r, seed=base_seed + 500 + k, q=q) for k in range(K)])
    return qs.std(ddof=1), qs.mean()


if __name__ == "__main__":
    r_grid = [200, 1000, 5000, 20000]
    K = 100
    print("=== PRIMARY LOGGED RUN (K=100 replications per r, base_seed=42) ===")
    mcsd_list = []
    mcsd_q_list = []
    for r in r_grid:
        mcsd, mean_se = mc_noise_of_bootstrap_se(CLEC, r, K, base_seed=42)
        mcsd_q, mean_q = mc_noise_of_percentile(CLEC, r, K, base_seed=42)
        mcsd_list.append(mcsd)
        mcsd_q_list.append(mcsd_q)
        print(f"  r={r:6d}: MC-SD of bootstrap SE = {mcsd:.5f} (mean SE={mean_se:.4f})  "
              f"MC-SD*sqrt(r) = {mcsd*np.sqrt(r):.4f}   "
              f"MC-SD of 97.5th pctile = {mcsd_q:.5f} (mean={mean_q:.4f})  MC-SD_q*sqrt(r)={mcsd_q*np.sqrt(r):.4f}")

    print("\nratio of MC-SD (r=200) / MC-SD (r=20000):", mcsd_list[0]/mcsd_list[-1],
          " theory sqrt(20000/200)=", np.sqrt(20000/200))

    print("\n=== CALIBRATION: repeat entire sweep with 4 more base seeds ===")
    ratios = []
    normed_list_all = []
    for base_seed in [1000, 2000, 3000, 4000]:
        mcsds = []
        for r in r_grid:
            mcsd, _ = mc_noise_of_bootstrap_se(CLEC, r, K, base_seed=base_seed)
            mcsds.append(mcsd)
        ratio = mcsds[0]/mcsds[-1]
        ratios.append(ratio)
        normed = [m*np.sqrt(r) for m, r in zip(mcsds, r_grid)]
        normed_list_all.append(normed)
        print(f"  base_seed={base_seed}: MC-SDs={[f'{m:.5f}' for m in mcsds]}  ratio(r200/r20000)={ratio:.3f}  "
              f"normed(MC-SD*sqrt(r))={[f'{x:.4f}' for x in normed]}")

    print("\nratio range across calibration:", min(ratios), max(ratios), " theory:", np.sqrt(20000/200))
