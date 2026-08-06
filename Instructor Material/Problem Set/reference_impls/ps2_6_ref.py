"""
PS2.6 reference implementation (optional) -- SIR preview.

Reuses PS2.3's four named functions (reimplemented locally here for a self-contained
reference script; the student's own PS2.3 code is what they should actually reuse).

New here: a REAL draw of N=4000 (alpha,beta) pairs from the prior (not the fixed
6-point test case), followed by resampling WITH REPLACEMENT from the normalized
importance weights -- i.e., Sampling Importance Resampling (SIR), previewed here and
formalized in Module 7 (PS7.1).

Adapts (paraphrase only, no solution text -- both R&C 3.6 and 3.16 are UNSOLVED/even
numbered, so there is no published solution to paraphrase from in the first place;
these are cited purely as the theoretical motivation for the resampling idea).
"""

import numpy as np

x = np.array([-0.86, -0.30, -0.05, 0.73])
n_grp = np.array([5, 5, 5, 5])
y = np.array([0, 1, 3, 5])

MEAN = np.array([0.0, 10.0])
COV = np.array([[4.0, 12.0], [12.0, 100.0]])


def log_importance_ratios(alpha, beta):
    logit = alpha[:, None] + beta[:, None] * x[None, :]
    theta = 1.0 / (1.0 + np.exp(-logit))
    theta = np.clip(theta, 1e-12, 1 - 1e-12)
    return np.sum(y * np.log(theta) + (n_grp - y) * np.log(1 - theta), axis=1)


def normalize_weights(lr):
    m = np.max(lr)
    w = np.exp(lr - m)
    return w / np.sum(w)


def is_estimate(h, w):
    return np.sum(w * h) / np.sum(w)


def is_ess(lr):
    w = normalize_weights(lr)
    return 1.0 / np.sum(w ** 2)


def run(seed, N=4000, M=4000):
    rng = np.random.default_rng(seed)
    draws = rng.multivariate_normal(MEAN, COV, size=N)
    alpha, beta = draws[:, 0], draws[:, 1]
    lr = log_importance_ratios(alpha, beta)
    w = normalize_weights(lr)
    ess = is_ess(lr)
    is_mean_alpha = is_estimate(alpha, w)
    is_mean_beta = is_estimate(beta, w)

    idx = rng.choice(N, size=M, replace=True, p=w)
    resampled_alpha = alpha[idx]
    resampled_beta = beta[idx]

    return dict(
        ess=ess, ess_pct=ess / N * 100,
        is_mean_alpha=is_mean_alpha, is_mean_beta=is_mean_beta,
        resample_mean_alpha=resampled_alpha.mean(), resample_mean_beta=resampled_beta.mean(),
        diff_alpha=abs(resampled_alpha.mean() - is_mean_alpha),
        diff_beta=abs(resampled_beta.mean() - is_mean_beta),
    )


if __name__ == "__main__":
    print("=== Logged reference run (seed=0) ===")
    o = run(seed=0)
    for k, v in o.items():
        print(f"  {k}: {v}")

    print("\n=== Calibration: 150 seeds ===")
    da, db, ep = [], [], []
    for seed in range(150):
        o = run(seed)
        da.append(o["diff_alpha"]); db.append(o["diff_beta"]); ep.append(o["ess_pct"])
    da, db, ep = map(np.array, (da, db, ep))
    print(f"diff_alpha: mean={da.mean():.4f} max={da.max():.4f} 99th pct={np.percentile(da,99):.4f}")
    print(f"diff_beta:  mean={db.mean():.4f} max={db.max():.4f} 99th pct={np.percentile(db,99):.4f}")
    print(f"ess_pct: mean={ep.mean():.2f} min={ep.min():.2f} max={ep.max():.2f}")
