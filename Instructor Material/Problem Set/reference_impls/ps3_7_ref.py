"""
PS3.7 (optional) reference implementation.
Bootstrap of the MEDIAN at n=15 from a known (simulatable) population --
exhibit the H-2 phenomenon: for odd n, the bootstrap median is always exactly
one of the original observations (discrete, <=n unique values), while the true
sampling distribution of the median (simulated by drawing many FRESH samples
from the known population) is effectively continuous (unique values ~= number
of simulation draws).
"""
import numpy as np

N = 15


def bootstrap_median_dist(data, r, seed):
    rng = np.random.default_rng(seed)
    n = len(data)
    idx = rng.integers(0, n, size=(r, n))
    return np.median(data[idx], axis=1)


def true_sampling_dist_of_median(n, M, seed, dist="normal"):
    rng = np.random.default_rng(seed)
    meds = np.empty(M)
    for i in range(M):
        if dist == "normal":
            x = rng.normal(0, 1, size=n)
        else:
            raise ValueError(dist)
        meds[i] = np.median(x)
    return meds


def run_once(data_seed, boot_seed, true_seed, r=2000, M=2000):
    rng = np.random.default_rng(data_seed)
    original = rng.normal(0, 1, size=N)

    boot_meds = bootstrap_median_dist(original, r, boot_seed)
    true_meds = true_sampling_dist_of_median(N, M, true_seed)

    n_unique_boot = len(np.unique(np.round(boot_meds, 10)))
    n_unique_true = len(np.unique(np.round(true_meds, 10)))

    # also: the bootstrap median values must all be members of the original sample
    is_subset = np.all(np.isin(np.round(boot_meds, 8), np.round(original, 8)))

    return dict(n_unique_boot=n_unique_boot, n_unique_true=n_unique_true,
                is_subset=is_subset, boot_std=boot_meds.std(ddof=1),
                true_std=true_meds.std(ddof=1))


if __name__ == "__main__":
    print("=== PRIMARY LOGGED RUN (data_seed=8, boot_seed=8, true_seed=8, r=2000, M=2000) ===")
    p = run_once(8, 8, 8)
    for k, v in p.items():
        print(f"  {k} = {v}")

    print("\n=== CALIBRATION (10 seed sets) ===")
    unique_boot_list = []
    unique_true_list = []
    subset_list = []
    for sd in range(100, 110):
        r = run_once(sd, sd + 1, sd + 2)
        unique_boot_list.append(r['n_unique_boot'])
        unique_true_list.append(r['n_unique_true'])
        subset_list.append(r['is_subset'])
        print(f"  seed={sd}: n_unique_boot={r['n_unique_boot']}  n_unique_true={r['n_unique_true']}  "
              f"is_subset={r['is_subset']}  boot_std={r['boot_std']:.4f}  true_std={r['true_std']:.4f}")

    print("\nn_unique_boot range:", min(unique_boot_list), max(unique_boot_list))
    print("n_unique_true range:", min(unique_true_list), max(unique_true_list))
    print("all is_subset True:", all(subset_list))
