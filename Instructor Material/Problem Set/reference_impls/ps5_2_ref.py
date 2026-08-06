"""
PS5.2 reference run — prior-predictive simulation under three Beta priors
for a Beta-Binomial environmental-monitoring model.
Stated data: n=40 sites monitored, y=15 showing presence of the indicator
organism (drafter-stated scenario, disclosed as a synthetic substitute for
the harvest's real 274-site algae dataset -- no numeric target from that
real dataset is being cited, so no fetch/anchor is required for the data
itself; see WO-M5 PS5.2 verification sketch: "no fixed numeric target by
design" for the prior-sensitivity comparison itself).

No posterior sampler anywhere: prior predictive draws are pure forward
simulation (draw pi ~ prior, then y ~ Binomial(n, pi)), matching Module
1-2 simulation primitives per the module's no-sampling constraint.
"""
import numpy as np

n = 40
y_obs = 15
priors = {
    "Beta(2,10)  -- weak, low-prevalence-leaning": (2, 10),
    "Beta(1,1)   -- flat/uniform":                 (1, 1),
    "Beta(20,20) -- strong, centered at 0.5":       (20, 20),
}

ndraws = 20000
seed = 20260715  # date-coded seed, reported to students

print(f"{'prior':35s} {'analytic_mean':>14s} {'sim_mean':>10s} {'sim_5pct':>9s} {'sim_95pct':>10s} {'post_mean':>10s}")
results = {}
for label, (a, b) in priors.items():
    rng = np.random.default_rng(seed)
    pi_draws = rng.beta(a, b, size=ndraws)
    y_draws = rng.binomial(n, pi_draws)

    analytic_pred_mean = n * a / (a + b)  # Beta-Binomial compound mean, closed form
    sim_mean = y_draws.mean()
    p5, p95 = np.percentile(y_draws, [5, 95])

    a_post, b_post = a + y_obs, b + n - y_obs
    post_mean = a_post / (a_post + b_post)

    results[label] = dict(a=a, b=b, analytic_pred_mean=analytic_pred_mean,
                           sim_mean=sim_mean, p5=p5, p95=p95,
                           post_mean=post_mean, a_post=a_post, b_post=b_post)
    print(f"{label:35s} {analytic_pred_mean:14.3f} {sim_mean:10.3f} {p5:9.1f} {p95:10.1f} {post_mean:10.4f}")

# Cross-check: simulated predictive mean vs closed-form Beta-Binomial compound mean
print("\nCross-check |sim_mean - analytic_pred_mean|:")
for label, r in results.items():
    print(f"  {label:35s} {abs(r['sim_mean'] - r['analytic_pred_mean']):.4f}")

# Where does the observed y=15 fall relative to each prior's predictive spread?
print(f"\nObserved y={y_obs} relative to each prior's simulated 90% predictive interval:")
for label, r in results.items():
    inside = r['p5'] <= y_obs <= r['p95']
    print(f"  {label:35s} [{r['p5']:.1f}, {r['p95']:.1f}]  observed inside? {inside}")
