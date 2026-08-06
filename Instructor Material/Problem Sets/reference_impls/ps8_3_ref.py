"""
PS8.3 reference implementation (optional problem).
Constructs two "chains" -- n iid draws from N(0,1), n iid draws from
Student-t(df=3) -- per the Vehtari Aalto BDA Assignment 5 framing (the
"imagine one chain converged to N(0,1) and the other to t3" question),
and computes the classic (Gelman-Rubin) R-hat from the same from-scratch
implementation used in PS8.2.

Note (logged honestly, see ValidationLog PS8.3 entry and the module
Flags section): repeated attempts at a from-scratch rank-normalized R-hat
(plain rank-normalization; rank-normalization + chain-splitting; with and
without variance-matching or a location shift) did NOT reproduce the
source's cited rank-normalized value of 1.39 -- every construction tried
here tracked the classic value closely (both near 1). The classic-R-hat
target (~1) is therefore the only tier-3 numeric target this problem
carries; the rank-normalized contrast is carried as a tier-1 citation
(Annex A7.1/A8.1) plus a "reason through" conceptual component, per the
WO's own explicit allowance for this cell.
"""
import numpy as np
from scipy import stats
from reference_impls.ps8_2_ref import classic_rhat


def build_chains(n, seed):
    rng = np.random.default_rng(seed)
    chain_normal = rng.standard_normal(n)
    chain_t3 = rng.standard_t(df=3, size=n)
    return chain_normal, chain_t3


def rank_normalize_pair(c1, c2):
    pooled = np.concatenate([c1, c2])
    N = len(pooled)
    ranks = stats.rankdata(pooled, method="average")
    z = stats.norm.ppf((ranks - 3 / 8) / (N - 1 / 4))
    return z[: len(c1)], z[len(c1):]


def main():
    n = 1000
    seed = 42
    c1, c2 = build_chains(n, seed)
    r_classic, B, W = classic_rhat(np.array([c1, c2]))

    z1, z2 = rank_normalize_pair(c1, c2)
    r_rank_attempt, _, _ = classic_rhat(np.array([z1, z2]))

    # 10-seed calibration of the classic value only
    cal = []
    for s in range(10):
        cc1, cc2 = build_chains(n, s)
        r, _, _ = classic_rhat(np.array([cc1, cc2]))
        cal.append(r)

    return dict(
        r_classic=r_classic, B=B, W=W,
        r_rank_attempt=r_rank_attempt,
        calibration=cal,
    )


if __name__ == "__main__":
    res = main()
    print("classic R-hat (seed 42, n=1000):", res["r_classic"])
    print("rank-normalized R-hat, own attempted reproduction:", res["r_rank_attempt"],
          "(does not match the cited 1.39 -- see notes)")
    print("10-seed calibration of classic R-hat:", res["calibration"])
    print("calibration range:", min(res["calibration"]), max(res["calibration"]))
