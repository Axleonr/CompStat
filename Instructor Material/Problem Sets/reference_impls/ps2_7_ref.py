"""
PS2.7 reference implementation (optional) -- antithetic variates on a NON-monotone,
symmetric-about-0.5 statistic, where the technique structurally cannot help.

Target: I = E[(U-0.5)^2] = Var(U) = 1/12 for U~Uniform(0,1) (closed form, tier-2).

h(u) = (u-0.5)^2 is symmetric about u=0.5: h(1-u) = h(u) EXACTLY for all u. So the
antithetic pair average [h(U)+h(1-U)]/2 = h(U) exactly -- no averaging benefit at all;
using n/2 pairs at "n total workload" behaves like a plain estimator using only n/2
draws, which has TWICE the variance of a plain estimator using the full n draws.
This is a clean, deterministic negative case (not just a weak one), unlike PS2.2 (a).
"""

import numpy as np

I_TRUE = 1.0 / 12.0


def plain_mc(rng, n):
    u = rng.random(n)
    return np.mean((u - 0.5) ** 2)


def antithetic(rng, n):
    m = n // 2
    u = rng.random(m)
    h = (u - 0.5) ** 2
    h_pair = (1 - u - 0.5) ** 2  # should equal h exactly
    pair_avg = (h + h_pair) / 2.0
    return np.mean(pair_avg)


def variances_at(seed, n=2000, r=2000):
    rng = np.random.default_rng(seed)
    plain_vals = np.array([plain_mc(rng, n) for _ in range(r)])
    anti_vals = np.array([antithetic(rng, n) for _ in range(r)])
    return plain_vals.var(ddof=1), anti_vals.var(ddof=1), plain_vals.mean(), anti_vals.mean()


if __name__ == "__main__":
    # exact-equality sanity check
    rng0 = np.random.default_rng(123)
    u = rng0.random(10)
    h1 = (u - 0.5) ** 2
    h2 = (1 - u - 0.5) ** 2
    print("max abs diff h(u) vs h(1-u):", np.max(np.abs(h1 - h2)), "(should be ~0, i.e. exact symmetry)")

    print("\n=== Logged reference run (seed=0) ===")
    pv, av, pm, am = variances_at(seed=0)
    print(f"plain_var={pv}, anti_var={av}, ratio(plain/anti)={pv/av:.4f}")
    print(f"plain_mean={pm}, anti_mean={am}, I_true={I_TRUE}")

    print("\n=== Calibration: 200 meta-seeds ===")
    ratios = []
    for s in range(200):
        pv, av, _, _ = variances_at(seed=1000 + s)
        ratios.append(pv / av)
    ratios = np.array(ratios)
    print(f"ratio(plain/anti): mean={ratios.mean():.4f} sd={ratios.std():.4f} "
          f"min={ratios.min():.4f} max={ratios.max():.4f}")
