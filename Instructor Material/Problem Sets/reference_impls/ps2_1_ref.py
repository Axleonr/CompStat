"""
PS2.1 reference implementation — plain Monte Carlo estimator, log-log rate-plot slope.

Target: I = E[e^U], U ~ Uniform(0,1)  =>  I = integral_0^1 e^x dx = e - 1  (closed form, tier-2).

Purpose of this script (two parts):
  (A) Logged reference run (seed=0): the exact run whose numbers are cited in the
      validation-log entry and used as the worked illustration in the discussion note.
  (B) Calibration study (2000 independent seeds): establishes the ACHIEVABLE tolerance
      band for the fitted slope of a SINGLE realization per n-grid-point, per WO-M2 §5's
      escalation note ("the reference run must establish an achievable tolerance before
      the student-facing tolerance is written"). This is what justifies the
      student-facing band of [-0.8, -0.2] rather than a naive "≈ -0.5 exactly."

No student-facing tolerance is written until both parts have run and their output is
recorded in ValidationLog_0_1.md (see the PS2.1 entry).
"""

import numpy as np

I_TRUE = np.e - 1.0
N_GRID = np.array([100, 300, 1000, 3000, 10000, 30000, 100000, 300000, 1000000])


def run_once(seed, n_grid=N_GRID):
    """One realization: fresh independent U(0,1) draws at each grid point (not cumulative)."""
    rng = np.random.default_rng(seed)
    errors = []
    for n in n_grid:
        u = rng.random(n)
        est = np.mean(np.exp(u))
        errors.append(abs(est - I_TRUE))
    errors = np.array(errors)
    slope, intercept = np.polyfit(np.log10(n_grid), np.log10(errors), 1)
    return slope, errors


if __name__ == "__main__":
    # --- Part A: logged reference run ---
    seed = 0
    slope, errors = run_once(seed)
    print("=== Part A: logged reference run (seed=0) ===")
    print("I_true (e - 1):", I_TRUE)
    print("n_grid:", N_GRID.tolist())
    print("abs errors:", np.round(errors, 6).tolist())
    print("fitted slope (OLS, log10-log10):", slope)

    # --- Part B: calibration study for the achievable tolerance band ---
    print("\n=== Part B: calibration study (2000 seeds) ===")
    slopes = np.array([run_once(s)[0] for s in range(2000)])
    print("mean slope:", slopes.mean(), "std:", slopes.std())
    for p in [0.5, 1, 2.5, 5, 50, 95, 97.5, 99, 99.5]:
        print(f"  {p:>5}th pct: {np.percentile(slopes, p):.4f}")
    print("min/max:", slopes.min(), slopes.max())
    band = (-0.8, -0.2)
    coverage = np.mean((slopes >= band[0]) & (slopes <= band[1]))
    print(f"coverage of proposed band {band}: {coverage:.4f}")
