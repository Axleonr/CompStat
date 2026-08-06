"""
PS8.6 reference implementation.
Deliberately poor initialization: init_beta = 1000 (~170x the converged
posterior mean of ~5.86). To make the transient's influence visible against
Monte Carlo noise, each replication is a very short chain (n_iter=10); the
comparison is averaged over 30 independent replications (fresh seeds) rather
than trusting a single short run (a single length-10 replication's gap can
go either way -- this is disclosed in the module Flags / discussion note).

Baseline (per the WO's stated provenance rule for this vehicle -- the pump
posterior has no tier-2 citable value): the tier-3 logged converged-run
posterior mean from the student's own long, well-initialized PS7.4 chain
(seed 101, init_beta=1.0, n_iter=20000, burn_in=2000) -- the same object
already used throughout this module.
"""
import numpy as np
from reference_impls.pump_gibbs import run_pump_gibbs

BAD_INIT_BETA = 1000.0
SHORT_N_ITER = 10
WARM_UP_W = 2
N_REPS = 30


def baseline_means():
    chain = run_pump_gibbs(20000, seed=101, init_beta=1.0)
    post = chain[2000:]
    return post[:, -1].mean(), post[:, 4].mean()  # beta, theta_5


def replication_gaps(seed_start, col, baseline, n_reps=N_REPS,
                      n_iter=SHORT_N_ITER, w=WARM_UP_W, init_beta=BAD_INIT_BETA):
    gaps_with, gaps_without = [], []
    for i in range(n_reps):
        c = run_pump_gibbs(n_iter, seed=seed_start + i, init_beta=init_beta)
        series = c[:, col]
        gaps_with.append(abs(series.mean() - baseline))
        gaps_without.append(abs(series[w:].mean() - baseline))
    return np.array(gaps_with), np.array(gaps_without)


def main():
    beta_baseline, theta5_baseline = baseline_means()
    g_with_beta, g_without_beta = replication_gaps(9000, col=-1, baseline=beta_baseline)
    g_with_t5, g_without_t5 = replication_gaps(9000, col=4, baseline=theta5_baseline)
    return dict(
        beta_baseline=beta_baseline, theta5_baseline=theta5_baseline,
        beta_gap_with=g_with_beta.mean(), beta_gap_without=g_without_beta.mean(),
        theta5_gap_with=g_with_t5.mean(), theta5_gap_without=g_without_t5.mean(),
    )


if __name__ == "__main__":
    res = main()
    print("baseline beta:", res["beta_baseline"], " baseline theta_5:", res["theta5_baseline"])
    print(f"beta:    avg gap WITH warm-up = {res['beta_gap_with']:.4f}   "
          f"avg gap WITHOUT warm-up = {res['beta_gap_without']:.4f}   "
          f"ratio = {res['beta_gap_with']/res['beta_gap_without']:.2f}")
    print(f"theta_5: avg gap WITH warm-up = {res['theta5_gap_with']:.4f}   "
          f"avg gap WITHOUT warm-up = {res['theta5_gap_without']:.4f}   "
          f"ratio = {res['theta5_gap_with']/res['theta5_gap_without']:.2f}")

    print("\n--- calibration (3 additional 30-replication batches, beta only) ---")
    for sb in [20000, 40000, 60000]:
        gw, gwo = replication_gaps(sb, col=-1, baseline=res["beta_baseline"])
        print(f"  seed_start={sb}: avg_gap_with={gw.mean():.4f} avg_gap_without={gwo.mean():.4f} "
              f"ratio={gw.mean()/gwo.mean():.2f}")
