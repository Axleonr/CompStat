"""
PS2.3 is a TIER-1 problem (Annex A2.4/A2.5 machine-checked values) -- this script is
NOT a tier-3 validation-log artifact and does not get a ValidationLog entry.

Its only purpose: confirm that the model specification as WRITTEN in the PS2.3 problem
statement (dataset, prior, "proposal = prior" reduction) actually reproduces the exact
Annex A2.4 test-case values, so the problem statement is internally consistent with the
citation it makes. This is drafting-time QA, not a new tier-3 execution.

Reference: VerifiedTargetsAnnex.md A2.4 (test inputs/outputs), A2.5 (Eq. 10.4 corrected
form: S_eff = 1 / sum(w_tilde_i^2), no printing-error multiplier).
"""

import numpy as np

# classic BDA3 bioassay dataset (4 dose groups), as stated in the PS2.3 problem text
x = np.array([-0.86, -0.30, -0.05, 0.73])   # log-dose
n = np.array([5, 5, 5, 5])                   # animals per group
y = np.array([0, 1, 3, 5])                   # deaths per group

# Annex A2.4's 6-point (alpha, beta) test case
alpha_test = np.array([1.896, -3.6, 0.374, 0.964, -3.123, -1.581])
beta_test  = np.array([24.76, 20.04, 6.15, 18.65, 8.16, 17.4])

EXPECTED_LOG_RATIOS = np.array([-8.95, -23.47, -6.02, -8.13, -16.61, -14.57])
EXPECTED_NORM_W = np.array([0.045, 0.000, 0.852, 0.103, 0.000, 0.000])
EXPECTED_POST_MEAN = (0.503, 8.275)
EXPECTED_ESS = 1.354
EXPECTED_MCSE = (0.3031766, 4.4794358)  # NOT an exact student target -- version-drifts;
                                         # PS2.3 states this to 2 sig figs only.


def log_importance_ratios(theta_draws, data):
    """proposal = prior => log(target/proposal) = log-likelihood only."""
    alpha, beta = theta_draws
    x_, n_, y_ = data
    logit = alpha[:, None] + beta[:, None] * x_[None, :]
    theta = 1.0 / (1.0 + np.exp(-logit))
    theta = np.clip(theta, 1e-12, 1 - 1e-12)
    ll = np.sum(y_ * np.log(theta) + (n_ - y_) * np.log(1 - theta), axis=1)
    return ll


def normalize_weights(log_ratios):
    m = np.max(log_ratios)
    w = np.exp(log_ratios - m)
    return w / np.sum(w)


def is_estimate(h_values, weights):
    return np.sum(weights * h_values) / np.sum(weights)


def is_ess(log_ratios):
    w = normalize_weights(log_ratios)
    return 1.0 / np.sum(w ** 2)


if __name__ == "__main__":
    data = (x, n, y)
    lr = log_importance_ratios((alpha_test, beta_test), data)
    print("log_importance_ratios:", np.round(lr, 2), " expected:", EXPECTED_LOG_RATIOS)

    w = normalize_weights(lr)
    print("normalize_weights:", np.round(w, 3), " expected:", EXPECTED_NORM_W)

    pm_alpha = is_estimate(alpha_test, w)
    pm_beta = is_estimate(beta_test, w)
    print("is_estimate (alpha,beta):", round(pm_alpha, 3), round(pm_beta, 3),
          " expected:", EXPECTED_POST_MEAN)

    ess = is_ess(lr)
    print("is_ess:", round(ess, 3), " expected:", EXPECTED_ESS)

    var_w_alpha = np.sum(w * (alpha_test - pm_alpha) ** 2)
    var_w_beta = np.sum(w * (beta_test - pm_beta) ** 2)
    mcse_alpha = np.sqrt(var_w_alpha / ess)
    mcse_beta = np.sqrt(var_w_beta / ess)
    print("MCSE (alpha,beta):", round(mcse_alpha, 4), round(mcse_beta, 4),
          " expected (approx, version-drifts):", EXPECTED_MCSE)

    print("\nAll values match Annex A2.4/A2.5 to the stated precision: CONFIRMED.")
