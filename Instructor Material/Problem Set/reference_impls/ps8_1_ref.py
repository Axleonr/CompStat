"""
PS8.1 reference implementation.
Computes ACF (through lag 50) and ESS (initial-positive-sequence estimator)
from scratch on the student's stored PS7.4 healthy chain (beta and theta_5),
after discarding the same 2,000-iteration warm-up used for PS7.4's posterior
summaries. Cross-checks against arviz (library oracle, R1.4).
"""
import numpy as np
import arviz as az
from statsmodels.tsa.stattools import acf as sm_acf
from reference_impls.pump_gibbs import run_pump_gibbs

MAX_LAG = 50


def acf_from_scratch(x, max_lag):
    n = len(x)
    xbar = x.mean()
    denom = np.sum((x - xbar) ** 2)
    rhos = np.empty(max_lag + 1)
    for k in range(max_lag + 1):
        num = np.sum((x[: n - k] - xbar) * (x[k:] - xbar))
        rhos[k] = num / denom
    return rhos


def ess_initial_positive_sequence(x):
    n = len(x)
    max_lag = n - 1
    rhos = acf_from_scratch(x, max_lag)
    # pair consecutive autocorrelations: Gamma_m = rho_{2m} + rho_{2m+1}
    m_max = (max_lag - 1) // 2
    gammas = np.empty(m_max + 1)
    for m in range(m_max + 1):
        gammas[m] = rhos[2 * m] + rhos[2 * m + 1]
    # truncate at first non-positive pair
    cutoff = m_max + 1
    for m in range(m_max + 1):
        if gammas[m] <= 0:
            cutoff = m
            break
    tau = -1.0 + 2.0 * gammas[:cutoff].sum()
    tau = max(tau, 1.0 / n)  # guard against pathological negative tau
    ess = n / tau
    return ess, tau, cutoff


def main():
    chain = run_pump_gibbs(20000, seed=101, init_beta=1.0)
    burn_in = 2000
    post = chain[burn_in:]
    names = [f"theta_{i+1}" for i in range(10)] + ["beta"]
    idx = {n: i for i, n in enumerate(names)}

    results = {}
    for pname in ["beta", "theta_5"]:
        x = post[:, idx[pname]]
        rhos = acf_from_scratch(x, MAX_LAG)
        ess_scratch, tau, cutoff = ess_initial_positive_sequence(x)

        # library cross-check (arviz), same post-warm-up array, chain dim added
        x_az = x.reshape(1, -1)
        ess_lib = float(az.ess(x_az, method="mean"))
        acf_lib = sm_acf(x, nlags=MAX_LAG, fft=True)

        results[pname] = dict(
            n=len(x),
            rho_lag1=rhos[1],
            rho_lag5=rhos[5],
            rho_lag10=rhos[10],
            rho_lag50=rhos[50],
            ess_scratch=ess_scratch,
            tau=tau,
            cutoff_m=cutoff,
            ess_lib=ess_lib,
            pct_diff=100.0 * abs(ess_scratch - ess_lib) / ess_lib,
            acf_lib_lag1=acf_lib[1],
            acf_lib_lag5=acf_lib[5],
            acf_max_abs_diff=float(np.max(np.abs(rhos - acf_lib))),
        )
    return results


def calibration(n_seeds=10, seeds=range(101, 111)):
    """Re-runs the sampler at several seeds (fresh chains, same model/data)
    to check how stable the from-scratch-vs-library ESS agreement is,
    before fixing a student-facing tolerance."""
    burn_in = 2000
    names = [f"theta_{i+1}" for i in range(10)] + ["beta"]
    idx = {n: i for i, n in enumerate(names)}
    pct_diffs = {"beta": [], "theta_5": []}
    for s in seeds:
        chain = run_pump_gibbs(20000, seed=s, init_beta=1.0)
        post = chain[burn_in:]
        for pname in ["beta", "theta_5"]:
            x = post[:, idx[pname]]
            ess_scratch, _, _ = ess_initial_positive_sequence(x)
            ess_lib = float(az.ess(x.reshape(1, -1), method="mean"))
            pct_diffs[pname].append(100.0 * abs(ess_scratch - ess_lib) / ess_lib)
    return pct_diffs


if __name__ == "__main__":
    res = main()
    for pname, r in res.items():
        print(f"--- {pname} ---")
        for k, v in r.items():
            print(f"  {k}: {v}")

    print("\n--- 10-seed calibration (fresh chains, seeds 101-110) ---")
    cal = calibration()
    for pname, vals in cal.items():
        print(f"{pname}: max={max(vals):.4f}%  mean={np.mean(vals):.4f}%")
