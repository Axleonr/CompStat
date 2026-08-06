"""
PS8.2 reference implementation.
Classic (Gelman-Rubin) R-hat, implemented from its definition, computed on:
  (a) 4 dispersed-start chains of the healthy PS7.4 pump Gibbs sampler
  (b) 4 dispersed-start chains of the failing PS7.6 bimodal RW-MH sampler
      (same delta=0.5 proposal scale that produced the documented failure)
"""
import numpy as np
from reference_impls.pump_gibbs import run_pump_gibbs
from reference_impls.bimodal_mh import run_bimodal_mh


def classic_rhat(chains):
    """chains: array of shape (m, n) -- m chains, n retained draws each.
    Returns the classic BDA3-form Gelman-Rubin R-hat."""
    m, n = chains.shape
    chain_means = chains.mean(axis=1)
    grand_mean = chain_means.mean()
    B = n / (m - 1) * np.sum((chain_means - grand_mean) ** 2)
    within_vars = chains.var(axis=1, ddof=1)
    W = within_vars.mean()
    var_plus = (n - 1) / n * W + B / n
    rhat = np.sqrt(var_plus / W)
    return rhat, B, W


def main():
    burn_in = 2000
    n_iter = 20000

    # --- healthy sampler: dispersed initial beta, 4 chains ---
    healthy_inits = [0.1, 1.0, 5.0, 20.0]
    healthy_seeds = [201, 202, 203, 204]
    names = [f"theta_{i+1}" for i in range(10)] + ["beta"]
    healthy_chains = []
    for init_b, s in zip(healthy_inits, healthy_seeds):
        c = run_pump_gibbs(n_iter, seed=s, init_beta=init_b)
        healthy_chains.append(c[burn_in:])
    healthy_chains = np.array(healthy_chains)  # (4, n_retained, 11)

    healthy_rhat = {}
    for i, name in enumerate(names):
        arr = healthy_chains[:, :, i]
        rhat, B, W = classic_rhat(arr)
        healthy_rhat[name] = rhat

    # per-chain posterior means for beta (sanity: dispersed starts converge)
    healthy_beta_chain_means = healthy_chains[:, :, -1].mean(axis=1)

    # --- failing sampler: dispersed starts across/near both modes, same delta ---
    failing_inits = [-8.0, -5.0, 5.0, 8.0]
    failing_seeds = [301, 302, 303, 304]
    failing_chains = []
    for theta0, s in zip(failing_inits, failing_seeds):
        chain, n_acc = run_bimodal_mh(n_iter, seed=s, delta=0.5, theta0=theta0)
        failing_chains.append(chain[burn_in:])  # same 2,000-iteration warm-up
        # convention applied to both configurations for a like-for-like comparison
    failing_chains = np.array(failing_chains)  # (4, n_iter-burn_in)
    failing_rhat, failing_B, failing_W = classic_rhat(failing_chains)
    failing_chain_means = failing_chains.mean(axis=1)

    return dict(
        healthy_rhat=healthy_rhat,
        healthy_beta_chain_means=healthy_beta_chain_means,
        failing_rhat=failing_rhat,
        failing_chain_means=failing_chain_means,
        failing_B=failing_B,
        failing_W=failing_W,
    )


if __name__ == "__main__":
    res = main()
    print("Healthy sampler R-hat (all 11 params):")
    for k, v in res["healthy_rhat"].items():
        print(f"  {k}: {v:.5f}")
    print("Healthy beta per-chain posterior means (4 dispersed starts):", res["healthy_beta_chain_means"])
    print()
    print("Failing sampler R-hat (single param, mean of mixture):", res["failing_rhat"])
    print("Failing chain means (4 dispersed starts):", res["failing_chain_means"])
    print("Failing B (between):", res["failing_B"], "W (within):", res["failing_W"])
