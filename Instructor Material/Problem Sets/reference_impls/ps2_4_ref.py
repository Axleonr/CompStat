"""
PS2.4 reference implementation.

Target: standard Cauchy(0,1), density f(x) = 1/(pi*(1+x^2)).

Two proposals:
  BAD (light-tailed):  Normal(0,1).       f(x)/g(x) grows like exp(x^2/2)/x^2 -> unbounded;
                        E[weight^2] under the proposal is infinite (classic pathological case).
  GOOD (heavy-tailed):  Cauchy(0, scale=2). f(x)/g(x) -> 1/2 (a constant) as |x| -> infinity;
                        bounded weights, well-behaved.

No downstream expectation h(X) is estimated here -- per WO-M2's brief, this problem
diagnoses the WEIGHTS themselves (histogram, max-weight share, ESS), not an estimation
target. That's why it's Type D (diagnosis), not Type I.
"""

import numpy as np


def cauchy_pdf(x, loc=0.0, scale=1.0):
    return 1.0 / (np.pi * scale * (1 + ((x - loc) / scale) ** 2))


def normal_pdf(x, loc=0.0, scale=1.0):
    return (1.0 / (scale * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - loc) / scale) ** 2)


def sample_cauchy(rng, n, loc=0.0, scale=1.0):
    u = rng.random(n)
    return loc + scale * np.tan(np.pi * (u - 0.5))


def run(seed, N, bad=True):
    rng = np.random.default_rng(seed)
    if bad:
        draws = rng.standard_normal(N)
        g = normal_pdf(draws)
    else:
        draws = sample_cauchy(rng, N, scale=2.0)
        g = cauchy_pdf(draws, scale=2.0)
    f = cauchy_pdf(draws, scale=1.0)
    w = f / g
    wn = w / np.sum(w)
    ess = 1.0 / np.sum(wn ** 2)
    max_share = np.max(wn)
    return ess, max_share, wn


N = 20000
N_SEEDS_STUDENT = 10   # what the problem asks the student to run


if __name__ == "__main__":
    print(f"=== Logged reference run: N={N}, seeds 0-9 (what the problem asks for) ===")
    bad_pct, bad_share = [], []
    good_pct, good_share = [], []
    for seed in range(N_SEEDS_STUDENT):
        eb, sb, _ = run(seed, N, bad=True)
        eg, sg, _ = run(seed, N, bad=False)
        bad_pct.append(eb / N * 100)
        bad_share.append(sb)
        good_pct.append(eg / N * 100)
        good_share.append(sg)
        print(f"  seed={seed}: BAD ESS%={eb/N*100:6.3f}  max_share={sb:.4f}   "
              f"GOOD ESS%={eg/N*100:6.3f}  max_share={sg:.5f}")
    bad_pct = np.array(bad_pct); bad_share = np.array(bad_share)
    good_pct = np.array(good_pct); good_share = np.array(good_share)
    print(f"\nBAD  ESS%%: mean={bad_pct.mean():.2f} range={bad_pct.max()-bad_pct.min():.2f} "
          f"(min={bad_pct.min():.3f}, max={bad_pct.max():.2f})")
    print(f"BAD  max_share: min over 10 seeds={bad_share.min():.4f}")
    print(f"GOOD ESS%%: mean={good_pct.mean():.2f} range={good_pct.max()-good_pct.min():.2f}")
    print(f"GOOD max_share: max over 10 seeds={good_share.max():.5f}")

    print("\n=== Calibration study: 60 independent seeds, N=20000 ===")
    bp, bs, gp, gs = [], [], [], []
    for seed in range(60):
        eb, sb, _ = run(seed, N, bad=True)
        eg, sg, _ = run(seed, N, bad=False)
        bp.append(eb / N * 100); bs.append(sb)
        gp.append(eg / N * 100); gs.append(sg)
    bp, bs, gp, gs = map(np.array, (bp, bs, gp, gs))
    print(f"BAD  ESS%%: mean={bp.mean():.2f} sd={bp.std():.2f} min={bp.min():.3f} max={bp.max():.2f}")
    print(f"BAD  max_share: min={bs.min():.4f} mean={bs.mean():.4f} max={bs.max():.4f}")
    print(f"GOOD ESS%%: mean={gp.mean():.2f} sd={gp.std():.3f} min={gp.min():.2f} max={gp.max():.2f}")
    print(f"GOOD max_share: min={gs.min():.6f} mean={gs.mean():.6f} max={gs.max():.6f}")
    # block-of-10 range check (what a student running exactly 10 seeds would see)
    ranges = []
    for start in range(0, 60 - 10, 10):
        block = bp[start:start + 10]
        ranges.append(block.max() - block.min())
    print("BAD ESS%% range over 5 independent blocks of 10 seeds:", np.round(ranges, 2))
