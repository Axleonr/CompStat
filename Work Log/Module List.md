### Updated Module List

| # | Module |
|---|---|
| 0 | Computational Thinking & Statistical Algorithms |
| 1 | Random Number Generation & Simulation |
| 2 | Monte Carlo Estimation & Variance Reduction |
| 3 | Bootstrap & Resampling |
| 4 | Optimization: Gradient Methods, Metaheuristics & EM |
| 5 | Bayesian Modeling Framework |
| 6 | Markov Chains as Computational Objects |
| 7 | MCMC Methods |
| 8 | MCMC Diagnostics & Reliability |
| 9 | Density Estimation |
| 10 | Applied Cases |

---

### Changes made

**Module 5 (old Density Estimation) — removed** from its original position and replaced by the Bayesian Modeling Framework, which now follows Optimization directly. The EM-to-Bayes transition is now uninterrupted.

**Modules 6–9 — renumbered down by one.** Bayesian Modeling becomes 5, Markov Chains becomes 6, MCMC Methods becomes 7, Diagnostics becomes 8. All internal cross-references updated accordingly — including the Module 2 forward reference to SIR and the Module 5 deferred-computation reference to Modules 6–8.

**Module 9 (new Density Estimation) — rewritten.** The module text is no longer framed as a standalone nonparametric methods unit. It now opens by situating density estimation as the natural next question after a working sampler and diagnostic workflow are in place. The Rao-Blackwell estimator is explicitly framed around MCMC settings, and posterior predictive distributions are named as the primary motivating application. The high-level goal reflects this reframing.

**Module 10 (Applied Cases) — unchanged.** Its reference to density estimates of the posterior predictive distribution is now more directly motivated by the preceding module.