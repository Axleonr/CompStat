"""
PS8.5 reference implementation (capstone).
Diagnose: single failing PS7.6 chain (delta=0.5, theta0=-5.0, seed=0) --
ESS from scratch (reusing PS8.1's estimator) plus the PS8.2-logged
multi-chain R-hat for this same failing configuration (reused by
reference, not recomputed here).
Adjust: increase proposal scale to delta=6.0.
Rerun: same 4 dispersed starts as PS8.2's failing configuration
  (-8, -5, 5, 8), fresh seeds.
Re-evaluate: multi-chain R-hat, pooled mean/variance vs. known mixture
  truth (mean=0, variance=26), per-chain right-mode-visit fraction.
"""
import numpy as np
from reference_impls.bimodal_mh import run_bimodal_mh
from reference_impls.ps8_1_ref import ess_initial_positive_sequence
from reference_impls.ps8_2_ref import classic_rhat

BURN_IN = 2000
N_ITER = 20000


def diagnose():
    chain, n_acc = run_bimodal_mh(N_ITER, seed=0, delta=0.5, theta0=-5.0)
    ess, tau, cutoff = ess_initial_positive_sequence(chain)
    return dict(
        ess=ess, tau=tau,
        acc_rate=n_acc / N_ITER,
        mean=chain.mean(), var=chain.var(ddof=1),
        frac_right=(chain > 0).mean(),
        # multi-chain R-hat for this configuration is PS8.2's own logged
        # value (5.8915, seeds 301-304) -- reused by reference, not
        # recomputed, per the problem's design (avoid redundant compute).
        rhat_reused_from_ps8_2=5.8915,
    )


def adjust_rerun_reevaluate(seed_base, delta=6.0):
    inits = [-8.0, -5.0, 5.0, 8.0]
    seeds = [seed_base + i for i in range(4)]
    chains = []
    per_chain = []
    for theta0, s in zip(inits, seeds):
        c, n_acc = run_bimodal_mh(N_ITER, seed=s, delta=delta, theta0=theta0)
        post = c[BURN_IN:]
        chains.append(post)
        per_chain.append(dict(
            theta0=theta0, seed=s, acc_rate=n_acc / N_ITER,
            mean=post.mean(), var=post.var(ddof=1),
            frac_right=(post > 0).mean(),
        ))
    chains = np.array(chains)
    rhat, B, W = classic_rhat(chains)
    pooled = chains.reshape(-1)
    ess_one_chain, _, _ = ess_initial_positive_sequence(chains[0])
    return dict(
        per_chain=per_chain, rhat=rhat,
        pooled_mean=pooled.mean(), pooled_var=pooled.var(ddof=1),
        ess_one_chain=ess_one_chain,
    )


if __name__ == "__main__":
    d = diagnose()
    print("--- DIAGNOSE (delta=0.5, single chain, seed 0) ---")
    for k, v in d.items():
        print(f"  {k}: {v}")

    print("\n--- ADJUST -> RERUN -> RE-EVALUATE (delta=6.0) ---")
    primary = adjust_rerun_reevaluate(1301)
    for pc in primary["per_chain"]:
        print(" ", pc)
    print("  R-hat:", primary["rhat"])
    print("  pooled mean:", primary["pooled_mean"], " pooled var:", primary["pooled_var"])
    print("  single-chain ESS (delta=6.0):", primary["ess_one_chain"])

    print("\n--- calibration (3 additional 4-chain batches) ---")
    for sb in [1401, 1501, 1601]:
        r = adjust_rerun_reevaluate(sb)
        fracs = [pc["frac_right"] for pc in r["per_chain"]]
        print(f"  seed_base={sb}: R-hat={r['rhat']:.5f} pooled_mean={r['pooled_mean']:.4f} "
              f"pooled_var={r['pooled_var']:.4f} fracs={[round(f,3) for f in fracs]}")
