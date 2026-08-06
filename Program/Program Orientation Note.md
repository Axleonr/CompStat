# Computational Statistics Program
## Program Orientation Note
*Read before Module 0*

---

## What This Program Is

This program treats statistics as a computational discipline. That is not a stylistic claim about how statistics should be taught — it is a substantive claim about how statistical methods actually work. Every estimator in this program is an algorithm: it takes data as input, executes a computational process, and produces estimates, intervals, or decisions as output. Every inference procedure carries assumptions that can be tested. Every result can fail in ways that are diagnosable if you know what to look for.

The consequence of that framing is that this program does not survey methods. It builds the kind of understanding that lets you reason about why a method works, recognize when it is failing, and make informed decisions about which tool to use and how to evaluate its output. That is a different goal from knowing a large number of procedures, and it requires a different kind of engagement with the material.

**Prerequisites:** Probability and statistical inference at the level of distributions, expectation, and maximum likelihood. Linear algebra sufficient for multivariate distributions. Working fluency in a scientific computing language (Python, R, or Julia). Prior exposure to multivariate analysis or linear models is strongly recommended.

---

## How the Eleven Modules Fit Together

The program has an architecture. The modules are not a collection of independent topics — they are a designed sequence with explicit dependencies and connections. Understanding that architecture before you begin will help you read each module with the right orientation.

**Module 0** opens by reframing statistics itself. Before any algorithm appears, the module establishes that statistical procedures are algorithms, and that the computational framing opens up questions — about convergence, efficiency, sensitivity, and failure — that the traditional formulas-and-decision-rules view cannot ask. This is not a gentle warm-up: it is the interpretive lens through which every subsequent module should be read. Tukey (1962) is read in full here, and it is worth reading seriously.

**Modules 1–2** build the computational foundation. Module 1 examines where random numbers come from — how a deterministic algorithm produces sequences that behave statistically as random, and how non-uniform samples are generated from the uniform base. These are the simulation primitives that every subsequent method depends on, and understanding them is not optional. Module 2 develops Monte Carlo estimation: why it works, how its error behaves, and how to reduce that error systematically through importance sampling, variance reduction, and related techniques. Importance sampling in particular is introduced here as an idea with consequences beyond variance reduction — that thread is picked up in Module 7.

**Modules 3–4** cover two distinct computational inference paradigms. Module 3 develops the bootstrap: data-driven inference through resampling, its theoretical basis, and — equally important — the conditions under which it fails. Module 4 covers optimization as a computational inference strategy: gradient methods, the EM algorithm, and the metaheuristic approaches that handle objectives resistant to gradient descent. These two modules are relatively self-contained and feed primarily into Module 10's applied workflow.

**Module 5** shifts to Bayesian modeling, but deliberately. The module focuses on model construction — specifying a joint distribution, choosing a prior, building the likelihood, and reasoning about the posterior as a computational object — without yet introducing the algorithms needed to sample it. This separation is intentional and important: a student who only learns to run a sampler on a given posterior has not learned Bayesian modeling. Module 5 builds the modeling layer; Modules 7–8 build the computational layer on top of it.

**Module 6** is the theoretical hinge of the MCMC arc. It treats Markov chains as dynamical systems whose convergence properties govern the quality of any sampler built on them. Irreducibility, aperiodicity, detailed balance, mixing time, and the spectral gap are developed here not as abstract facts but as explanations for sampler behavior. This module is what separates a student who can run a sampler from a student who understands why it worked or why it failed. It is the highest-value investment in the program's second half.

**Module 7** constructs the MCMC algorithms. With the Markov chain theory from Module 6 in place, the Metropolis-Hastings algorithm follows from the detailed balance condition as a derived result rather than a recipe. Gibbs sampling, Metropolis-within-Gibbs, and Sampling Importance Resampling (which connects back to Module 2's importance sampling) are developed as a related family of approximate sampling strategies — each solving the same core problem by different design choices. The connection between algorithm design and chain behavior is kept explicit throughout.

**Module 8** addresses the question practitioners most often skip: how do you know whether to trust your MCMC output? Effective sample size, autocorrelation, trace plots, R-hat, warm-up, and thinning are developed as principled tools for answering that question. The module's goal is a practitioner who treats diagnostic analysis as an integral part of MCMC, not an afterthought.

**Module 9** covers density estimation: the problem of estimating a distribution nonparametrically from data or from sampler output. This module is motivated by the practical need to interpret posterior distributions, predictive distributions, and sampler output as distributions rather than scalar summaries. Kernel density estimation, bandwidth selection, Rao-Blackwellization in MCMC settings, and nearest-neighbor methods are covered.

**Module 10** integrates the program's tools across applied cases. The emphasis is on workflow and judgment: selecting the right tool for each sub-problem, recognizing when a method's assumptions are being stressed, producing reproducible results, and reporting conclusions honestly. The module closes with two short disciplinary retrospectives (Efron & Hastie Epilogue and Gelman & Vehtari 2021) that situate the program's methods within the broader arc of modern statistical practice — closing the frame opened by Tukey in Module 0.

---

## The Program's Module Map

| Module | Name | Est. Hours | Core Contribution | Feeds Into |
|--------|------|-----------|-------------------|------------|
| 0 | Computational Thinking | 3–4 | Establishes the algorithmic framing of statistics | All modules |
| 1 | Random Number Generation | 5–6 | Builds the simulation primitives everything else depends on | Modules 2, 3, 7 |
| 2 | Monte Carlo Estimation | 12–15 | Error theory and variance reduction; importance sampling extended to resampling | Module 7 (SIR) |
| 3 | Bootstrap & Resampling | 13–15 | Data-driven inference and its limits | Module 10 |
| 4 | Optimization | 12–15 | Gradient, metaheuristic, and EM approaches to computing estimators | Module 5 |
| 5 | Bayesian Modeling | 6–8 | Model construction as a distinct layer from computation | Modules 7, 8, 10 |
| 6 | Markov Chains | 8–10 | Convergence theory that governs sampler quality | Modules 7, 8 |
| 7 | MCMC Methods | 15–18 | SIR, MH, Gibbs, and Metropolis-within-Gibbs as a related family | Modules 8, 9 |
| 8 | MCMC Diagnostics | 8–10 | Evaluating sampler output; workflow for trusting or questioning results | Module 10 |
| 9 | Density Estimation | 6–8 | Nonparametric distribution estimation from data and MCMC output | Module 10 |
| 10 | Applied Cases | 8–10 | Workflow integration and disciplinary retrospective | — |

**Total: ~96–119 hours.** *(Note: The previously stated total of 103–116 was a computation error; the corrected figure is the actual row sum. Module 3 revised from 10–12 to 13–15 hrs.)*

---

## The Central Spine

The program has a spine: Modules 1–2 (simulation foundations) → Module 6 (Markov chain theory) → Modules 7–8 (MCMC methods and diagnostics). These modules form a conceptual chain where each builds directly on the previous one. If you shortchange any of them, the later modules lose their explanatory foundation and become recipes instead of understood methods.

The most important single structural decision in the program is the placement of Module 6 immediately before MCMC. The UNAM program on which part of this program is based treats Markov chains as a prerequisite fact. This program treats them as a subject. That one decision is what separates a student who can run a sampler from a student who can reason about why it worked.

---

## The Three Arcs

In addition to the spine, the program has three thematic arcs that run across modules:

**The simulation arc:** Modules 1, 2, 7, and 8 form a continuous development of simulation-based inference — from generating random numbers, to Monte Carlo estimation, to approximate sampling via MCMC, to evaluating whether that sampling is working. The importance sampling thread that begins in Module 2 (Goal 6) and resurfaces in Module 7 (SIR) is the explicit bridge between Monte Carlo estimation and MCMC.

**The Bayesian arc:** Modules 5, 6, 7, 8, and 10 form the Bayesian computation sequence. Module 5 builds the model; Module 6 provides the theory; Module 7 implements the sampler; Module 8 evaluates its output; Module 10 applies the result. These modules are designed to be read in order. Do not read Module 7 before Module 6. Do not run a sampler before reading Module 5.

**The disciplinary framing arc:** Tukey (1962) opens Module 0. Efron & Hastie's Epilogue and Gelman & Vehtari (2021) close Module 10. This is deliberate. The program begins with a historical argument about what statistics is and should be, and ends by asking you to assess that argument in light of the methods you have learned. The question whether Tukey's call for a reformation of statistics has been answered is one the program expects you to take seriously.

---

## A Note on Engagement

The module reading guides contain focus notes, forward pointers, and conceptual questions. The focus notes tell you what to attend to and what to move past in each reading. The forward pointers tell you where each reading is building toward. The conceptual questions are the most important part: they are calibrated to distinguish between having read something and having understood it.

A student who can answer the conceptual questions for each module has genuinely internalized the material. A student who can reproduce the reading's content without being able to answer them has not. The questions are not hard in a mathematical sense — they require explanation, connection, and reasoning, not calculation. But they do require that the reading was engaged with rather than processed.

*Read actively. The program rewards it.*
