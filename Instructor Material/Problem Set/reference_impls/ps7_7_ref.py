"""
PS7.7 reference implementation -- optional bug-hunt problem.
Original, paraphrased/reconstructed pseudocode-to-code translation (NOT
verbatim source code -- the actual Aalto A5 notebook text was never fetched;
only the harvest file's paraphrased bug descriptions were used) implementing
a RW-Metropolis sampler on a standard normal target with three planted bugs
matching the three-bug pattern confirmed in VerifiedTargetsAnnex.md entry
A7.1/A8.1 (tier-1: bugs' existence/count), alongside a corrected version
(tier-3: post-fix behavior, executed and logged here).

Bug 1: log-ratio computed but never exponentiated before use as an acceptance probability.
Bug 2: accept/reject inequality direction inverted.
Bug 3: chain records the proposed value every iteration, not the post-decision current state.
"""
import numpy as np

def target_logpdf(theta):
    return -0.5*theta**2 - 0.5*np.log(2*np.pi)

def buggy_sampler(delta, n_iter, seed, theta0=0.0):
    rng = np.random.default_rng(seed)
    chain = np.empty(n_iter)
    cur = theta0
    for t in range(n_iter):
        prop = cur + delta*rng.normal()
        log_ratio = target_logpdf(prop) - target_logpdf(cur)   # bug 1: never exponentiated
        u = rng.uniform()
        if u > log_ratio:                                       # bug 2: inverted inequality, compares to log-ratio not ratio
            cur = prop
        chain[t] = prop                                          # bug 3: records proposal, not post-decision state
    return chain

def fixed_sampler(delta, n_iter, seed, theta0=0.0):
    rng = np.random.default_rng(seed)
    chain = np.empty(n_iter)
    cur = theta0
    cur_lp = target_logpdf(cur)
    n_accept = 0
    for t in range(n_iter):
        prop = cur + delta*rng.normal()
        prop_lp = target_logpdf(prop)
        if np.log(rng.uniform()) < (prop_lp - cur_lp):
            cur, cur_lp = prop, prop_lp
            n_accept += 1
        chain[t] = cur
    return chain, n_accept/n_iter

if __name__ == '__main__':
    delta, n_iter = 1.0, 20000

    print("=== Buggy sampler, seed 0 ===")
    bchain = buggy_sampler(delta, n_iter, seed=0)
    print(f"mean={bchain.mean():.4f} (true=0), var={bchain.var(ddof=1):.4f} (true=1)")
    print(f"min/max: {bchain.min():.4f} / {bchain.max():.4f}  <- should look pathological if bugs matter")

    print("\n=== Fixed sampler, seed 0 ===")
    fchain, facc = fixed_sampler(delta, n_iter, seed=0)
    print(f"acceptance rate={facc:.4f}")
    print(f"mean={fchain.mean():.4f} (|diff|={abs(fchain.mean()):.4f}), var={fchain.var(ddof=1):.4f} (|diff from 1|={abs(fchain.var(ddof=1)-1):.4f})")

    # Calibration for the fixed sampler (reusing the same delta=1 setting as PS7.2)
    n_cal = 50
    accs, means, varss = [], [], []
    for s in range(6000, 6000+n_cal):
        ch, a = fixed_sampler(delta, n_iter, seed=s)
        accs.append(a); means.append(ch.mean()); varss.append(ch.var(ddof=1))
    accs, means, varss = map(np.array, (accs, means, varss))
    print(f"\n=== Fixed-sampler calibration ({n_cal} seeds) ===")
    print(f"acc rate: mean={accs.mean():.4f} min={accs.min():.4f} max={accs.max():.4f}")
    print(f"mean: min={means.min():.4f} max={means.max():.4f}")
    print(f"var:  min={varss.min():.4f} max={varss.max():.4f}")

    # Calibration for the buggy sampler, to show its pathology is consistent (not a one-off)
    baccs_meanabs, bvarss = [], []
    for s in range(6000, 6000+n_cal):
        bch = buggy_sampler(delta, n_iter, seed=s)
        baccs_meanabs.append(abs(bch.mean()))
        bvarss.append(bch.var(ddof=1))
    baccs_meanabs, bvarss = map(np.array, (baccs_meanabs, bvarss))
    print(f"\n=== Buggy-sampler calibration ({n_cal} seeds) ===")
    print(f"|mean|: mean={baccs_meanabs.mean():.4f} min={baccs_meanabs.min():.4f} max={baccs_meanabs.max():.4f}")
    print(f"var:    mean={bvarss.mean():.4f} min={bvarss.min():.4f} max={bvarss.max():.4f}")
