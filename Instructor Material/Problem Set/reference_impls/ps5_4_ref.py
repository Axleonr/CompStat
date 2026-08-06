"""
PS5.4 reference run -- prior-predictive simulation for a varying-intercepts
tank-survival model (reedfrogs-style hierarchical prior), reproducing the
qualitative sigma-widening effect independently confirmed this session
against McElreath's stat_rethinking_2023 Week 6 Problem 1 prompt structure:
    alpha_j ~ Normal(alpha_bar, sigma)
    alpha_bar ~ Normal(0, 1)
    sigma ~ Exponential(rate)
Pure forward simulation, no posterior sampler, no fitting.
"""
import numpy as np

def invlogit(x):
    return 1.0 / (1.0 + np.exp(-x))

rng = np.random.default_rng(20260715)
n = 20000

rate_settings = {
    "Exponential(10)  [tight/small sigma]": 10.0,
    "Exponential(1)   [baseline]":           1.0,
    "Exponential(0.1) [wide/large sigma]":   0.1,
}

print(f"{'sigma prior':38s} {'mean sigma':>10s} {'frac p<0.05':>12s} {'frac p>0.95':>12s} {'frac in (0.05,0.95)':>20s}")
summary = {}
for label, rate in rate_settings.items():
    sigma = rng.exponential(scale=1.0/rate, size=n)
    alpha_bar = rng.normal(0, 1, size=n)
    alpha = rng.normal(alpha_bar, sigma)
    p = invlogit(alpha)

    frac_low = np.mean(p < 0.05)
    frac_high = np.mean(p > 0.95)
    frac_mid = np.mean((p >= 0.05) & (p <= 0.95))
    summary[label] = dict(mean_sigma=sigma.mean(), frac_low=frac_low, frac_high=frac_high, frac_mid=frac_mid)
    print(f"{label:38s} {sigma.mean():10.3f} {frac_low:12.3f} {frac_high:12.3f} {frac_mid:20.3f}")

print("\nEdge mass (frac_low + frac_high), by sigma prior -- should increase as sigma prior widens:")
for label, r in summary.items():
    edge = r['frac_low'] + r['frac_high']
    print(f"  {label:38s} edge_mass={edge:.3f}")
