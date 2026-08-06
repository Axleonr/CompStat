"""
PS7.2 reference implementation -- from-scratch random-walk Metropolis-Hastings
on a standard normal target, at three proposal scales delta in {0.1, 1, 10}
(matching R&C Example 6.4/6.10's own delta choices, cited as approximate).
Measures acceptance rate and lag-k autocorrelation at each scale.
"""
import numpy as np

def target_logpdf(theta):
    return -0.5*theta**2 - 0.5*np.log(2*np.pi)

def rw_mh(delta, n_iter, seed, theta0=0.0):
    rng = np.random.default_rng(seed)
    theta = np.empty(n_iter)
    cur = theta0
    cur_lp = target_logpdf(cur)
    n_accept = 0
    for t in range(n_iter):
        prop = cur + delta * rng.normal()
        prop_lp = target_logpdf(prop)
        log_alpha = prop_lp - cur_lp
        if np.log(rng.uniform()) < log_alpha:
            cur, cur_lp = prop, prop_lp
            n_accept += 1
        theta[t] = cur
    return theta, n_accept / n_iter

def autocorr(x, lag):
    x = x - x.mean()
    n = len(x)
    num = np.sum(x[:n-lag] * x[lag:])
    den = np.sum(x**2)
    return num / den

def run_scale(delta, n_iter, seed):
    chain, acc_rate = rw_mh(delta, n_iter, seed)
    acfs = {lag: autocorr(chain, lag) for lag in (1, 5, 20, 50)}
    return {
        'acc_rate': acc_rate,
        'acfs': acfs,
        'sample_mean': chain.mean(),
        'sample_var': chain.var(ddof=1),
    }

if __name__ == '__main__':
    deltas = [0.1, 1.0, 10.0]
    n_iter = 50000

    print("=== Seed 0 logged run, n_iter=50000 ===")
    for d in deltas:
        out = run_scale(d, n_iter, seed=0)
        print(f"delta={d:5.1f}: acc_rate={out['acc_rate']:.4f}, "
              f"mean={out['sample_mean']:.4f}, var={out['sample_var']:.4f}, "
              f"acf1={out['acfs'][1]:.4f}, acf5={out['acfs'][5]:.4f}, "
              f"acf20={out['acfs'][20]:.4f}, acf50={out['acfs'][50]:.4f}")

    print("\n=== Calibration: 50 seeds per scale ===")
    for d in deltas:
        accs, acf1s, acf5s, acf20s, means, varss = [], [], [], [], [], []
        for s in range(2000, 2050):
            out = run_scale(d, n_iter, seed=s)
            accs.append(out['acc_rate'])
            acf1s.append(out['acfs'][1])
            acf5s.append(out['acfs'][5])
            acf20s.append(out['acfs'][20])
            means.append(out['sample_mean'])
            varss.append(out['sample_var'])
        accs, acf1s, acf5s, acf20s, means, varss = map(np.array, (accs, acf1s, acf5s, acf20s, means, varss))
        print(f"delta={d:5.1f}: acc_rate mean={accs.mean():.4f} sd={accs.std():.4f} "
              f"min={accs.min():.4f} max={accs.max():.4f}")
        print(f"           acf1  mean={acf1s.mean():.4f} sd={acf1s.std():.4f} min={acf1s.min():.4f} max={acf1s.max():.4f}")
        print(f"           acf5  mean={acf5s.mean():.4f} sd={acf5s.std():.4f} min={acf5s.min():.4f} max={acf5s.max():.4f}")
        print(f"           acf20 mean={acf20s.mean():.4f} sd={acf20s.std():.4f} min={acf20s.min():.4f} max={acf20s.max():.4f}")
        print(f"           mean  mean={means.mean():.4f} sd={means.std():.4f} min={means.min():.4f} max={means.max():.4f}")
        print(f"           var   mean={varss.mean():.4f} sd={varss.std():.4f} min={varss.min():.4f} max={varss.max():.4f}")
