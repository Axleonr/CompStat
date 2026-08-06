# Computational Statistics: Program Guide

## Program Overview

This program treats statistics as a computational discipline. Every estimator is an algorithm, every inference procedure is a process that runs on data, and every result carries assumptions that can be tested. The goal is not to survey methods but to build the kind of understanding that lets you reason about *why* a method works, recognize *when* it is failing, and make informed decisions about which tool to use and how to evaluate its output.

The program covers the canonical toolkit of computational statistics — Monte Carlo simulation, resampling, optimization, density estimation, Bayesian modeling, and MCMC — at a depth that goes meaningfully beyond recipe-following. By the end, you should be able to implement these methods, explain their theoretical basis, and critically evaluate their results. Sequential Monte Carlo and particle filter methods, while related, are outside the current program's scope; the foundations covered here provide the preparation needed to approach those topics independently.

**Prerequisites:** Probability and statistical inference at the level of distributions, expectation, and maximum likelihood. Linear algebra sufficient for multivariate distributions. Working fluency in a scientific computing language (Python, R, or Julia). Prior exposure to multivariate analysis or linear models is strongly recommended.

---

## Module 0 — Computational Thinking & Statistical Algorithms

Statistics has traditionally been taught as a collection of formulas and decision rules. This module reframes the discipline from the ground up: statistical procedures are algorithms that take data as input and produce estimates, intervals, or decisions as output. That reframing has consequences. It means we can ask how fast an algorithm converges, how sensitive it is to its inputs, whether it can be made more efficient, and under what conditions it breaks.

This module establishes the vocabulary and mental habits that the rest of the program depends on. You will not write complex code here, but you will leave with a clearer picture of what it means to *compute* a statistical answer and why that question is different from simply *deriving* one.

**High-level goal:** Reframe statistical procedures as algorithms acting on data, and establish the computational vocabulary that organizes the rest of the program.

---

## Module 1 — Random Number Generation & Simulation

Every method in this program ultimately depends on the ability to generate random numbers. This module examines where those numbers come from. Computers are deterministic machines, so randomness must be constructed — through algorithms that produce sequences with the right statistical properties even though they are entirely determined by an initial seed. Understanding this is not merely a technical curiosity: it shapes how you think about reproducibility, about the limits of simulation, and about what it means to say a result is "random."

From this foundation the module moves to basic stochastic simulation — turning uniform random numbers into samples from arbitrary distributions — which is the primitive operation on which Monte Carlo and MCMC are built.

**High-level goal:** Understand how randomness is constructed computationally, and build the simulation primitives that all subsequent methods depend on.

---

## Module 2 — Monte Carlo Estimation & Variance Reduction

Monte Carlo methods use random simulation to solve problems that are analytically intractable — computing integrals, approximating expectations, and propagating uncertainty through complex models. This module develops the theoretical basis for Monte Carlo estimation: why it works, how its error behaves, and what controls the rate at which it improves with more computation.

The second half of the module addresses variance reduction — a family of techniques for getting more accurate estimates from the same computational budget. Importance sampling, antithetic variates, control variates, and stratified sampling are covered not as tricks but as principled modifications to the basic estimator, each with a clear explanation of where the efficiency gain comes from.

Importance sampling deserves particular attention: it reweights draws from a tractable proposal distribution to target a different distribution, and that reweighting idea has consequences beyond variance reduction. One natural extension — resampling from the importance weights to produce an equally-weighted approximate sample rather than a single estimate — is possible and will be revisited in Module 7, where approximate sampling from complex distributions is the central concern.

**High-level goal:** Understand Monte Carlo as a principled estimation strategy, characterize its error, and learn to reduce that error — through importance sampling, stratification, and other variance reduction techniques — without simply adding more samples.

---

## Module 3 — Bootstrap & Resampling

The bootstrap is one of the most conceptually elegant ideas in statistics: use the data itself as a model of the population, and simulate the sampling process by drawing from that model repeatedly. This module develops both parametric and nonparametric bootstrap from first principles, derives confidence intervals through multiple approaches, and examines the theoretical conditions under which the bootstrap provides valid inference.

Equally important is understanding when the bootstrap fails. Heavy-tailed distributions, extreme statistics, small samples, and dependent data all create situations where naive resampling breaks down. In particular, the bootstrap distribution of the mean can fail to converge under heavy tails, and naive resampling underestimates variability in dependent or clustered data unless modified — for example, through the moving blocks bootstrap. A practitioner who knows only that the bootstrap works is less useful than one who also knows where it stops working. The module covers confidence interval construction through three approaches — bootstrap-t, percentile, and BCa — developing each in sequence so that the accuracy and transformation properties that distinguish them are understood as a coherent hierarchy rather than a menu of alternatives.

The original Efron (1979) paper is assigned alongside the primary textbook — read for the founding argument in the same way Tukey (1962) frames Module 0 and Dempster, Laird & Rubin (1977) frames the EM section of Module 4.

**High-level goal:** Perform inference through data-driven simulation, understand the theoretical basis for its validity, and recognize the conditions under which it breaks down.

---

## Module 4 — Optimization: Gradient Methods, Metaheuristics & EM

Many of the most important estimators in statistics are defined as the solution to an optimization problem — maximum likelihood, MAP estimation, and regression coefficients are all computed by minimizing or maximizing an objective function. This module covers three families of optimization methods that arise frequently in statistical computation, each suited to different problem structures.

Gradient-based methods (first and second order) are the workhorses of smooth, well-behaved objectives. Metaheuristic methods — simulated annealing and genetic algorithms — address objectives that are discontinuous, multimodal, or otherwise resistant to gradient approaches. The EM algorithm occupies a special position: it is not a general-purpose optimizer but a statistical algorithm designed specifically for problems with missing or latent data. Each iteration is guaranteed to increase the likelihood monotonically, which gives EM its stability — but this does not guarantee convergence to a global maximum, and EM can settle at local optima depending on initialization. The rigorous convergence proof for EM is due to Wu (1983), which extended and corrected the original treatment by Dempster, Laird & Rubin (1977).

**High-level goal:** Compute estimators via optimization, understand the structural differences between gradient, metaheuristic, and EM approaches, and know which problem features determine which method is appropriate.

---

## Module 5 — Bayesian Modeling Framework

Before sampling from a posterior distribution, you have to construct one. This module focuses entirely on that construction — prior selection, likelihood specification, and the computational representation of a Bayesian model as an object that can be interrogated, criticized, and revised. Computation is deliberately deferred to Modules 6–8; the goal here is to develop modeling judgment independently of algorithmic execution.

This separation matters because conflating modeling with computation is one of the most common sources of confused Bayesian practice. A student who only learns to run a sampler on a given posterior has not learned Bayesian modeling — they have learned to operate software. This module addresses the modeling layer directly: what choices are you making, what do those choices commit you to, and how would you know if they were wrong.

**High-level goal:** Construct and reason about Bayesian models as structured computational objects, independent of the sampling algorithms used to fit them.

---

## Module 6 — Markov Chains as Computational Objects

This module is the theoretical foundation for everything that follows in the MCMC arc. A Markov chain is a dynamical system, and its long-run behavior — whether it converges, how quickly, and to what distribution — is governed by mathematical properties that can be analyzed precisely. Understanding these properties is not optional background for MCMC practitioners: it is the difference between someone who runs a sampler and someone who understands why it worked or why it failed.

The module covers the essential theory: irreducibility, aperiodicity, stationarity, and detailed balance as the conditions that guarantee convergence; mixing time and the spectral gap as measures of how fast convergence occurs; and the consequences of poor mixing for the quality of downstream estimates. The treatment emphasizes geometric and dynamical intuition over formal proof.

**High-level goal:** Understand Markov chains as dynamical systems whose convergence properties govern the quality of MCMC samplers, building the theoretical vocabulary needed to reason about sampler behavior.

---

## Module 7 — MCMC Methods

With the theoretical foundation from Module 6 in place, this module constructs and implements the core MCMC algorithms. It opens with Sampling Importance Resampling (SIR) as a conceptual entry point: SIR solves the problem of sampling from a distribution you cannot sample directly by reweighting draws from a proposal and resampling proportionally to those weights. This connects back to the importance sampling ideas from Module 2 and frames the central challenge — approximate sampling from complex distributions — before introducing the Markov chain solution.

Metropolis-Hastings is then developed in full generality, with careful attention to how proposal distribution choice affects mixing — a narrow proposal produces high acceptance rates but strongly autocorrelated samples, while too wide a proposal causes frequent rejections and similarly slow exploration. Gibbs sampling is introduced as an algorithm in which proposals are drawn from full conditional distributions, guaranteeing acceptance at every step; in its random-scan form it can be understood as a special case of Metropolis-Hastings, though the more common deterministic-scan version is better treated on its own terms. Metropolis-within-Gibbs combines both approaches for models where full conditionals are not available in closed form.

Throughout, the connection between algorithmic choices and the Markov chain properties from Module 6 is kept explicit. SIR, MH, and Gibbs are presented as three members of a family of approximate sampling strategies — each solving the same core problem by different means — rather than as isolated procedures to be memorized.

**High-level goal:** Implement and understand the core approximate sampling algorithms — SIR, Metropolis-Hastings, Gibbs, and Metropolis-within-Gibbs — as a related family of design choices whose behavior follows from the theory in Module 6.

---

## Module 8 — MCMC Diagnostics & Reliability

A sampler that runs without errors is not necessarily a sampler that is producing trustworthy output. This module addresses the question that practitioners most often skip: how do you know whether to trust your MCMC results? Convergence diagnostics — trace plots, R-hat, effective sample size, and autocorrelation analysis — are developed as principled tools for answering that question, not as bureaucratic checkboxes.

The module also covers warm-up and its role in allowing the chain to reach the typical set before samples are collected, and the role of thinning: while thinning is sometimes used to reduce storage burden, it does not improve statistical efficiency — keeping all samples always yields higher effective sample size than discarding intermediate draws. The practical workflow for iterating between running a sampler and evaluating its output is developed throughout. The goal is a practitioner who treats diagnostic analysis as an integral part of MCMC, not an afterthought.

**High-level goal:** Evaluate MCMC output critically using principled diagnostics, understand what convergence does and does not guarantee, and develop a reliable workflow for determining when sampler output can be trusted.

---

## Module 9 — Density Estimation

With a working sampler and a reliable diagnostic workflow in place, this module returns to a question that runs through the entire program: not just what a quantity is on average, but what its distribution actually looks like. Density estimation provides nonparametric tools for answering that question directly from data — or from MCMC output — without committing to a parametric family in advance.

The module is motivated by the problems students have already encountered: estimating posterior densities from sampler output, constructing posterior predictive distributions, and comparing distributions across groups or models. Kernel density estimation is covered in depth, including bandwidth selection and its consequences for the bias-variance tradeoff. The Rao-Blackwell estimator is introduced as a variance-reduction strategy particularly well-suited to MCMC settings, where conditional distributions are already available from the sampler. Nearest-neighbor methods are covered as an alternative approach with different bias-variance characteristics.

**High-level goal:** Estimate distributions nonparametrically from data and from MCMC output, understand the bias-variance tradeoffs governing each method, and apply density estimation as a practical tool for interpreting posterior and predictive distributions.

---

## Module 10 — Applied Cases

The final module integrates the program's tools across a set of substantial applied problems drawn from scientific and professional contexts. Each case is chosen to require genuine engagement with multiple modules — a problem might involve constructing a Bayesian model, implementing and diagnosing an MCMC sampler, using bootstrap intervals to validate a subsidiary claim, and interpreting a density estimate of the posterior predictive distribution.

The emphasis is on workflow and judgment: choosing the right tool for each sub-problem, recognizing when a method's assumptions are being stressed, and producing results that are reproducible and honestly reported. These cases are not exercises with known answers — they are problems where the computational and statistical choices you make determine the quality of the conclusions you can draw.

**High-level goal:** Integrate the program's methods into coherent, reproducible analyses of realistic problems, developing the workflow judgment that distinguishes competent method application from genuine computational statistical practice.

---

## References

The following sources informed the design and fact-checking of this program guide. This list records sources consulted during program development, not the assigned reading list — the canonical bibliography with module-level assignments is in the separate Bibliography file. Some sources below were considered and excluded from the assigned reading list; their inclusion here reflects their role in design and fact-checking only.

**Foundational texts**

- Dempster, A. P., Laird, N. M., & Rubin, D. B. (1977). Maximum likelihood from incomplete data via the EM algorithm. *Journal of the Royal Statistical Society: Series B (Methodological)*, 39(1), 1–22. https://doi.org/10.1111/j.2517-6161.1977.tb01600.x

- Wu, C. F. J. (1983). On the convergence properties of the EM algorithm. *Annals of Statistics*, 11(1), 95–103. *(Provides the rigorous convergence proof for EM, correcting and extending Dempster et al. 1977.)*

- Efron, B., & Hastie, T. (2016). *Computer Age Statistical Inference: Algorithms, Evidence, and Data Science*. Cambridge University Press.

- Gamerman, D., & Lopes, H. F. (2006). *Markov Chain Monte Carlo: Stochastic Simulation for Bayesian Inference* (2nd ed.). Chapman and Hall/CRC.

- Givens, G. H., & Hoeting, J. A. (2013). *Computational Statistics* (2nd ed.). Wiley.

**MCMC — algorithms and convergence**

- Roberts, G. O., & Rosenthal, J. S. (2001). Optimal scaling for various Metropolis-Hastings algorithms. *Statistical Science*, 16(4), 351–367.

- Brown, D., & Jones, G. L. (2024). Convergence rates of Metropolis-Hastings algorithms. *WIREs Computational Statistics*. https://doi.org/10.1002/wics.70002

- Atchadé, Y., & Perron, F. (2008). Approximate spectral gaps for Markov chains mixing times in high dimensions. *SIAM Journal on Mathematics of Data Science*.

**MCMC — Gibbs sampling**

- Geman, S., & Geman, D. (1984). Stochastic relaxation, Gibbs distributions, and the Bayesian restoration of images. *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 6(6), 721–741.

- VanDerwerken, D. (2017). Not every Gibbs sampler is a special case of the Metropolis-Hastings algorithm. *Communications in Statistics — Theory and Methods*, 46(20), 10005–10009. https://doi.org/10.1080/03610926.2016.1228961 *(Establishes that the deterministic-scan Gibbs sampler does not satisfy detailed balance in general.)*

**MCMC — diagnostics and thinning**

- Geyer, C. J. (1992). Practical Markov chain Monte Carlo. *Statistical Science*, 7(4), 473–483.

- Link, W. A., & Eaton, M. J. (2012). On thinning of chains in MCMC. *Methods in Ecology and Evolution*, 3(1), 112–115. https://doi.org/10.1111/j.2041-210X.2011.00131.x

- Stan Development Team. *Stan Reference Manual*, Section 15.4: Effective Sample Size. https://mc-stan.org/docs/reference-manual

- Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013). *Bayesian Data Analysis* (3rd ed.). Chapman and Hall/CRC.

**Bootstrap and resampling**

- Efron, B. (1979). Bootstrap methods: Another look at the jackknife. *Annals of Statistics*, 7(1), 1–26.

- Hall, P. (1990). Asymptotic properties of the bootstrap for heavy-tailed distributions. *Annals of Probability*, 18(3), 1342–1360. https://doi.org/10.1214/aop/1176990748

- Cornea-Madeira, A., & Davidson, R. (2015). A parametric bootstrap for heavy-tailed distributions. *Econometric Theory*, 31(3), 449–470.
