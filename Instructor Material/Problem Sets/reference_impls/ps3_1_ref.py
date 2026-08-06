"""
PS3.1 reference implementation.
Nonparametric bootstrap (from primitives: manual resample-with-replacement loop,
no library bootstrap routine) on:
  (a) the frozen 23-point CLEC-mirror dataset (synthetic; printed inline in the problem)
  (b) an ILEC-mirror sample (n=1664) drawn from a stated Gamma generative recipe

Checks:
  1. Bootstrap SE / 95% percentile CI for each arm, compared to the published
     Hesterberg (2015) analysis figures (Annex A3.1) as approximate MC-level targets.
  2. H-3 narrowness-bias relation: bootstrap SE should be smaller than s/sqrt(n) by
     approximately sqrt((n-1)/n).

This script is run multiple times (primary logged run + calibration batches with
different seeds) to set honest, margin-carrying tolerances for the student-facing
verification section, per SourcingComplianceMemo.md / ValidationLog_0_5.md rules.
"""
import numpy as np

# ---- CLEC-mirror data: frozen synthetic dataset (n=23), printed inline in the problem ----
CLEC = np.array([0.4, 11.3, 11.6, 44.5, 0.1, 51.1, 12.2, 12.1, 35.5, 56.7, 4.1, 0.1,
                 2.1, 52.7, 7.6, 42.6, 0.7, 3.2, 3.3, 1.6, 1.2, 14.4, 10.2])
assert len(CLEC) == 23

# ---- ILEC-mirror generative recipe (n=1664), stated to students ----
# Gamma(shape=k_ILEC, scale=theta_ILEC), chosen so that mean=8.41, sd=14.68
# (sd derived from the published s/sqrt(n)=0.36 relation: sd = 0.36*sqrt(1664)).
K_ILEC = 0.3282
THETA_ILEC = 25.625


def nonparam_bootstrap_mean(data, r, seed):
    """Nonparametric bootstrap of the sample mean, built from primitives:
    manual resample-with-replacement loop (no scipy/statsmodels bootstrap call)."""
    rng = np.random.default_rng(seed)
    n = len(data)
    boot_means = np.empty(r)
    for i in range(r):
        idx = rng.integers(0, n, size=n)      # resample indices with replacement
        boot_means[i] = data[idx].mean()
    return boot_means


def percentile_ci(boot_means, alpha=0.05):
    lo = np.percentile(boot_means, 100 * (alpha / 2))
    hi = np.percentile(boot_means, 100 * (1 - alpha / 2))
    return lo, hi


def run_once(ilec_gen_seed, boot_seed, r=10000):
    # ILEC-mirror sample
    rng_ilec = np.random.default_rng(ilec_gen_seed)
    ilec = rng_ilec.gamma(shape=K_ILEC, scale=THETA_ILEC, size=1664)

    results = {}
    for label, data in [("CLEC", CLEC), ("ILEC", ilec)]:
        n = len(data)
        s = data.std(ddof=1)
        s_over_sqrtn = s / np.sqrt(n)
        boot_means = nonparam_bootstrap_mean(data, r=r, seed=boot_seed)
        boot_se = boot_means.std(ddof=1)
        lo, hi = percentile_ci(boot_means)
        narrowness_factor = np.sqrt((n - 1) / n)
        predicted_boot_se = s_over_sqrtn * narrowness_factor
        results[label] = dict(
            n=n, mean=data.mean(), s=s, s_over_sqrtn=s_over_sqrtn,
            boot_se=boot_se, ci=(lo, hi),
            narrowness_factor=narrowness_factor,
            predicted_boot_se=predicted_boot_se,
        )
    return results


if __name__ == "__main__":
    print("=== PRIMARY LOGGED RUN (ilec_gen_seed=42, boot_seed=42, r=10000) ===")
    primary = run_once(ilec_gen_seed=42, boot_seed=42, r=10000)
    for label, d in primary.items():
        print(f"\n[{label}] n={d['n']}")
        print(f"  sample mean = {d['mean']:.5f}, sample sd = {d['s']:.5f}, s/sqrt(n) = {d['s_over_sqrtn']:.5f}")
        print(f"  bootstrap SE = {d['boot_se']:.5f}")
        print(f"  95% percentile CI = ({d['ci'][0]:.4f}, {d['ci'][1]:.4f})")
        print(f"  narrowness factor sqrt((n-1)/n) = {d['narrowness_factor']:.5f}")
        print(f"  predicted boot SE (s/sqrt(n) * factor) = {d['predicted_boot_se']:.5f}")
        print(f"  observed/predicted boot-SE ratio = {d['boot_se']/d['predicted_boot_se']:.4f}")

    print("\n=== CALIBRATION BATCHES (different ilec_gen_seed / boot_seed pairs) ===")
    calib_seeds = [(1, 1), (7, 13), (100, 200), (999, 4242)]
    clec_se_list, clec_ci_lo, clec_ci_hi = [], [], []
    ilec_se_list, ilec_mean_list = [], []
    ratio_list = []
    for gseed, bseed in calib_seeds:
        r = run_once(ilec_gen_seed=gseed, boot_seed=bseed, r=10000)
        c, i = r["CLEC"], r["ILEC"]
        clec_se_list.append(c["boot_se"])
        clec_ci_lo.append(c["ci"][0])
        clec_ci_hi.append(c["ci"][1])
        ilec_se_list.append(i["boot_se"])
        ilec_mean_list.append(i["mean"])
        ratio_list.append(c["boot_se"] / c["predicted_boot_se"])
        print(f"seeds(gen={gseed},boot={bseed}): CLEC boot_se={c['boot_se']:.4f} "
              f"CI=({c['ci'][0]:.2f},{c['ci'][1]:.2f})  ILEC boot_se={i['boot_se']:.5f} "
              f"ILEC mean={i['mean']:.4f}  CLEC ratio(obs/pred)={ratio_list[-1]:.4f}")

    print("\nCLEC boot_se range across calibration:", min(clec_se_list), "-", max(clec_se_list))
    print("CLEC CI-lo range:", min(clec_ci_lo), "-", max(clec_ci_lo))
    print("CLEC CI-hi range:", min(clec_ci_hi), "-", max(clec_ci_hi))
    print("ILEC boot_se range:", min(ilec_se_list), "-", max(ilec_se_list))
    print("ILEC mean range:", min(ilec_mean_list), "-", max(ilec_mean_list))
    print("CLEC narrowness ratio (obs/pred) range:", min(ratio_list), "-", max(ratio_list))

    # Two-arm contrast check (WO-M3 §5 escalation note): CLEC SE should be far larger
    # than ILEC SE, consistent with the real Verizon two-arm size asymmetry.
    print("\nTwo-arm contrast (primary run): CLEC boot_se / ILEC boot_se =",
          primary["CLEC"]["boot_se"] / primary["ILEC"]["boot_se"])
