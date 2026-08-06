"""
PS1.4 reference implementation — chain-tracing.

Reuses PS1.1's LCG exactly (m=2^31-1, a=16807, c=0), per WO-M1 interface obligation.
Chain: LCG state -> uniform -> inverse-transform exponential candidate for |Z| ->
accept-reject test (M = sqrt(2/pi)*e^0.5, same bound family as PS1.3's Laplace case,
since |Laplace| ~ Exponential(1)) -> on acceptance, one more uniform randomizes the sign
-> final N(0,1) draw Z.

Every LCG state and every uniform is logged, plus the accept/reject outcome at each
attempt, so the full trace is reproducible from the stated seed.
"""
import numpy as np

M = np.sqrt(2/np.pi) * np.exp(0.5)  # same theoretical bound as PS1.3's Laplace case

def lcg_step(x, a=16807, c=0, m=2**31 - 1):
    return (a * x + c) % m

def trace_one_normal_draw(seed, max_attempts=50):
    x = seed
    m = 2**31 - 1
    trace = []
    attempt = 0
    while attempt < max_attempts:
        attempt += 1
        # step 1: advance LCG, get uniform for exponential candidate
        x = lcg_step(x)
        x_a = x
        u_a = x / m
        y = -np.log(u_a)  # candidate for |Z|, Exponential(1) via inverse transform
        # step 2: advance LCG again, get uniform for accept/reject test
        x = lcg_step(x)
        x_b = x
        u_b = x / m
        accept_ratio = np.exp(-0.5 * (y - 1)**2)
        accepted = u_b <= accept_ratio
        trace.append(dict(attempt=attempt, x_a=x_a, u_a=u_a, y=y, x_b=x_b, u_b=u_b,
                           accept_ratio=accept_ratio, accepted=accepted))
        if accepted:
            # step 3: advance LCG once more, use as sign coin flip
            x = lcg_step(x)
            u_c = x / m
            sign = -1.0 if u_c < 0.5 else 1.0
            z = sign * y
            return z, x, trace, u_c, sign
    raise RuntimeError("max_attempts exceeded")

def run(seed, label=""):
    z, final_x, trace, u_c, sign = trace_one_normal_draw(seed)
    print(f"--- {label} seed={seed} ---")
    for t in trace:
        print(f"  attempt {t['attempt']}: LCG->{t['x_a']} u_a={t['u_a']:.6f} y(exp cand)={t['y']:.6f} "
              f"| LCG->{t['x_b']} u_b={t['u_b']:.6f} accept_ratio={t['accept_ratio']:.6f} "
              f"accepted={t['accepted']}")
    print(f"  sign-flip: LCG->{final_x} u_c={u_c:.6f} -> sign={'-' if sign<0 else '+'}")
    print(f"  FINAL DRAW Z = {z:.6f}")
    print(f"  total LCG steps consumed: {2*len(trace) + 1}  ({len(trace)} attempts x 2 steps, + 1 sign-flip step)")
    print()
    return z, trace

if __name__ == "__main__":
    print("=== PRIMARY logged run ===")
    run(777, label="PRIMARY")

    print("=== Calibration (3 more seeds, to confirm attempt-count variability) ===")
    for s in [1, 2, 3]:
        run(s, label="CALIBRATION")

    print("=== Reproducibility check: re-running seed=777 gives identical trace ===")
    z1, trace1 = trace_one_normal_draw(777)[0], trace_one_normal_draw(777)[2]
    z2, trace2 = trace_one_normal_draw(777)[0], trace_one_normal_draw(777)[2]
    print(f"z1={z1:.10f}  z2={z2:.10f}  identical={z1==z2}  trace_len_equal={len(trace1)==len(trace2)}")
