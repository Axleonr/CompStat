# Computational Statistics — Module Goals Reference
## Modules 0–10

*Supplement to the Program Guide. Records specific goals defined in the intermediate-level refinement pass. Goals are meant to be assessable: a student completing the module should be able to demonstrate each one.*

---

## Module 0 — Computational Thinking & Statistical Algorithms

**High-level goal:** Reframe statistical procedures as algorithms acting on data, and establish the computational vocabulary that organizes the rest of the program.

1. Reframe statistical procedures as algorithms: inputs, outputs, and the computational process connecting them
2. Distinguish between *deriving* a statistical result analytically and *computing* one algorithmically — and articulate why that distinction matters
3. Identify the questions that the computational framing opens up: convergence, sensitivity, efficiency, failure conditions
4. Situate the program's core methods (simulation, resampling, optimization, MCMC) within a unified algorithmic view of statistics
5. Read Tukey (1962) as a disciplinary argument — identify its central claim and assess its relevance to contemporary computational practice

---

## Module 1 — Random Number Generation & Simulation

**High-level goal:** Understand how randomness is constructed computationally, and build the simulation primitives that all subsequent methods depend on.

1. Explain why computers cannot produce true randomness and how pseudorandom number generators construct sequences that behave statistically as if random
2. Describe the key structural properties of a good uniform PRNG — period length, seed dependence, and the statistical tests used to evaluate generator quality
3. Implement the inverse transform method for generating non-uniform random variates, and explain the conditions under which it is applicable
4. Implement the acceptance-rejection method, explain where its efficiency comes from, and identify the factors that make a proposal distribution better or worse
5. Trace a sample from an arbitrary distribution back to its uniform foundation — articulating the full generative chain from PRNG output to non-uniform draw
6. Recognize the practical consequences of poor RNG choices: reproducibility failures, period exhaustion, and correlation artifacts in simulation output

---

## Module 2 — Monte Carlo Estimation & Variance Reduction

**High-level goal:** Understand Monte Carlo as a principled estimation strategy, characterize its error, and learn to reduce that error — through importance sampling, stratification, and other variance reduction techniques — without simply adding more samples.

1. Derive the Monte Carlo estimator from first principles and characterize its error — establishing why the method works and what governs the rate at which accuracy improves with sample size
2. Explain the role of variance in Monte Carlo error and articulate why reducing variance is equivalent to getting more information from the same computational budget
3. Implement and explain antithetic variates and control variates as principled modifications to the basic estimator, identifying the structural conditions that make each effective
4. Implement importance sampling, explain the reweighting mechanism, and identify the conditions under which importance weights become pathological
5. Recognize antithetic variates, control variates, stratification, and importance sampling as mechanistically distinct interventions in the same underlying error quantity — each reducing variance by a different structural means, none changing the fundamental $n^{-1/2}$ convergence rate
6. Recognize importance sampling as a reweighting idea with scope beyond variance reduction — specifically, that resampling from importance weights produces an approximate sample from the target, laying the groundwork for SIR in Module 7

> *Note: Stratified sampling is covered at the conceptual level within this goal. Unlike antithetic variates, control variates, and importance sampling, it does not carry a standalone implementation requirement.*

---

## Module 3 — Bootstrap & Resampling

**High-level goal:** Perform inference through data-driven simulation, understand the theoretical basis for its validity, and recognize the conditions under which it breaks down.

1. Derive the nonparametric bootstrap from first principles — articulating what the empirical distribution is, why sampling from it simulates the sampling process, and what assumptions that substitution requires
2. Implement parametric and nonparametric bootstrap and construct confidence intervals through multiple methods, including bootstrap-t, percentile, and BCa approaches
3. Explain the theoretical conditions under which bootstrap confidence intervals are valid, and distinguish between the bootstrap's consistency and its accuracy in finite samples
4. Identify and diagnose the conditions under which naive bootstrap fails: heavy-tailed distributions, extreme statistics, small samples, and dependent or clustered data
5. Apply modified resampling strategies — including the moving blocks bootstrap — for dependent and structured data, and explain what each modification corrects for and what residual limitations remain
6. Relate the bootstrap to the simulation primitives from Module 1 — the bootstrap is a resampling algorithm, and its behavior is as amenable to computational analysis as any other

---

## Module 4 — Optimization: Gradient Methods, Metaheuristics & EM

**High-level goal:** Compute estimators via optimization, understand the structural differences between gradient, metaheuristic, and EM approaches, and know which problem features determine which method is appropriate.

1. Formulate common statistical estimators as solutions to optimization problems, and identify the objective function features that determine which algorithmic family is appropriate
2. Implement and explain Newton's and quasi-Newton methods, including the role of the Hessian and the practical significance of numerical stability and step selection
3. Explain the statistical logic of EM — missing data, latent variables, lower-bound ascent — and derive the E and M steps from that framework
4. Explain why EM guarantees monotone likelihood increase, why this does not guarantee a global maximum, and what Wu (1983) establishes over Dempster et al. (1977)
5. Recognize when metaheuristic approaches are warranted over gradient or EM methods, and understand their basic operating principles without requiring deep implementation

---

## Module 5 — Bayesian Modeling Framework

**High-level goal:** Construct and reason about Bayesian models as structured computational objects, independent of the sampling algorithms used to fit them.

1. Specify a Bayesian model as a computational object — joint distribution, likelihood, prior, and posterior — and articulate what each component commits you to
2. Reason about prior selection as a modeling choice with verifiable consequences, not a subjective input to be chosen arbitrarily or defensively
3. Identify the structural patterns that arise in multiparameter and hierarchical models, and explain what hierarchical structure implies computationally
4. Criticize and revise a Bayesian model by interrogating its assumptions — prior sensitivity, likelihood misspecification, and predictive adequacy — independently of how it will be fit
5. Maintain a clear separation between the modeling layer and the computational layer: understand what questions belong to model construction and what questions belong to the sampler

---

## Module 6 — Markov Chains as Computational Objects

**High-level goal:** Understand Markov chains as dynamical systems whose convergence properties govern the quality of MCMC samplers, building the theoretical vocabulary needed to reason about sampler behavior.

1. Observe a concrete Markov chain running on a simple target — identifying mixing, stationarity, and failure to converge as empirical phenomena before formalizing them theoretically
2. Define the essential structural properties of a Markov chain — irreducibility, aperiodicity, and stationarity — and explain what each guarantees about long-run behavior
3. Explain detailed balance as a sufficient condition for stationarity, and identify why it is the condition that MCMC algorithms are designed to satisfy
4. Characterize mixing time and the spectral gap as measures of convergence speed, and develop geometric intuition for why some chains mix slowly
5. Connect poor mixing directly to downstream consequences — explain what slow mixing implies for the quality of estimates derived from sampler output

---

## Module 7 — MCMC Methods

**High-level goal:** Implement and understand the core approximate sampling algorithms — SIR, Metropolis-Hastings, Gibbs, and Metropolis-within-Gibbs — as a related family of design choices whose behavior follows from the theory in Module 6.

1. Explain Sampling Importance Resampling (SIR) as a bridge from importance sampling to approximate sampling — connecting back to Module 2 and framing the central challenge that MCMC addresses
2. Derive the Metropolis-Hastings algorithm from the detailed balance condition, and explain how the acceptance ratio enforces the correct stationary distribution
3. Implement Metropolis-Hastings and characterize how proposal distribution choice governs the tradeoff between acceptance rate and autocorrelation
4. Derive Gibbs sampling from the structure of full conditional distributions, and explain why acceptance is guaranteed at every step
5. Distinguish random-scan from deterministic-scan Gibbs — including why the deterministic-scan version does not satisfy detailed balance in general — and explain when each framing is appropriate
6. Implement Metropolis-within-Gibbs for models where full conditionals are not available in closed form, and identify when this hybrid is warranted
7. Recognize SIR, MH, and Gibbs as members of a common family of approximate sampling strategies — each solving the same core problem by different design choices

---

## Module 8 — MCMC Diagnostics & Reliability

**High-level goal:** Evaluate MCMC output critically using principled diagnostics, understand what convergence does and does not guarantee, and develop a reliable workflow for determining when sampler output can be trusted.

1. Explain effective sample size as the central measure of MCMC output quality — distinguishing it from raw sample count and connecting it to the autocorrelation structure of the chain
2. Compute and interpret autocorrelation function estimates from MCMC output, and explain what high autocorrelation implies for the reliability of downstream estimates
3. Apply trace plots, R-hat, and ESS as principled convergence diagnostics — understanding what each measures and what it can and cannot detect
4. Explain warm-up and its role in allowing the chain to reach the typical set, and distinguish between samples that should and should not be retained
5. Explain why thinning does not improve statistical efficiency, and identify the narrow circumstances where it may be practically justified
6. Develop a reliable iterative workflow for running a sampler, evaluating its output, and deciding whether to trust results or return to the sampler

---

## Module 9 — Density Estimation

**High-level goal:** Estimate distributions nonparametrically from data and from MCMC output, understand the bias-variance tradeoffs governing each method, and apply density estimation as a practical tool for interpreting posterior and predictive distributions.

1. Articulate the density estimation problem — what it means to estimate a distribution nonparametrically, and why point estimates and parametric models are sometimes insufficient
2. Implement kernel density estimation, explain the role of the kernel and bandwidth, and characterize the bias-variance tradeoff that bandwidth selection governs
3. Apply principled bandwidth selection methods and explain the consequences of under- and over-smoothing for the resulting estimate
4. Explain the Rao-Blackwell estimator as a variance-reduction strategy for density estimation, and identify why it is particularly well-suited to MCMC settings where conditional distributions are already available
5. Implement nearest-neighbor density estimation and contrast its bias-variance characteristics with those of kernel methods
6. Interpret density estimates critically — recognizing what each method implicitly assumes and how those assumptions affect the estimate — rather than treating output as an objective description of the data

---

## Module 10 — Applied Cases

**High-level goal:** Integrate the program's methods into coherent, reproducible analyses of realistic problems, developing the workflow judgment that distinguishes competent method application from genuine computational statistical practice.

1. Select and justify appropriate methods for each component of a multi-part applied problem, recognizing when a problem's structure calls for a specific tool and when alternatives would be equally valid
2. Construct, fit, and diagnose a Bayesian model end-to-end — from prior specification through MCMC sampling, diagnostic evaluation, and interpretation of posterior output
3. Apply bootstrap inference as a validation or subsidiary analysis tool within a larger workflow, and recognize when its assumptions are being stressed by the data
4. Demonstrate a posterior predictive check as a model criticism tool — understanding what it tests, what a failure implies, and what it cannot detect
5. Produce a complete analysis that is reproducible, honestly reported, and explicit about the assumptions and limitations of every methodological choice made
6. Read Efron & Hastie (Epilogue) and Gelman & Vehtari (2021) as disciplinary retrospectives — situating the program's methods within the broader arc of modern statistical practice, and closing the frame opened by Tukey (1962) in Module 0
