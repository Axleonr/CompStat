# Program Orientation Note

***Start by reading this note***
Presently, this note is sort-of an hybrid between the original note and a syllabus. Some reference material temporarily lives here.

## What This Program Is

This program treats statistics as a computational discipline. That is not a stylistic claim about how statistics should be taught — it is a substantive claim about how statistical methods actually work. Every estimator in this program is an algorithm: it takes data as input, executes a computational process, and produces estimates, intervals, or decisions as output. Every inference procedure carries assumptions that can be tested. Every result can fail in ways that are diagnosable if you know what to look for.

The consequence of that framing is that this program does not survey methods. It builds the kind of understanding that lets you reason about why a method works, recognize when it is failing, and make informed decisions about which tool to use and how to evaluate its output. That is a different goal from knowing a large number of procedures, and it requires a different kind of engagement with the material.

**Prerequisites:** Probability and statistical inference at the level of distributions, expectation, and maximum likelihood. Linear algebra sufficient for multivariate distributions. Working fluency in a scientific computing language (Python, R, or Julia). Prior exposure to multivariate analysis or linear models is strongly recommended.

---

## How the Eleven Modules Fit Together

The program has an architecture. The modules are not a collection of independent topics — they are a designed sequence with explicit dependencies and connections. Understanding that architecture before you begin will help you read each module with the right orientation.

**Module 0** opens by reframing statistics itself. Before any algorithm appears, the module establishes that statistical procedures are algorithms, and that the computational framing opens up questions — about convergence, efficiency, sensitivity, and failure — that the traditional formulas-and-decision-rules view cannot ask. This is not a gentle warm-up: it is the interpretive lens through which every subsequent module should be read. Tukey (1962) is read in full here, and it is worth reading seriously.

**Modules 1–2** build the computational foundation. Module 1 examines where random numbers come from — how a deterministic algorithm produces sequences that behave statistically as random, and how non-uniform samples are generated from the uniform base. These are the simulation primitives that every subsequent method depends on, and understanding them is not optional. Module 2 develops Monte Carlo estimation: why it works, how its error behaves, and how to reduce that error systematically through importance sampling, variance reduction, and related techniques. Importance sampling in particular is introduced here as an idea with consequences beyond variance reduction — that thread is picked up in Module 7.

**Modules 3–4** cover two distinct computational inference paradigms. Module 3 develops the bootstrap: data-driven inference through resampling, its theoretical basis, and — equally important — the conditions under which it fails. Module 4 covers optimization as a computational inference strategy: gradient methods, the EM algorithm, and the metaheuristic approaches that handle objectives resistant to gradient descent. These two modules are relatively self-contained, and feed only into Module 10's applied workflow.

**Module 5** shifts to Bayesian modeling, but deliberately. The module focuses on model construction — specifying a joint distribution, choosing a prior, building the likelihood, and reasoning about the posterior as a computational object — without yet introducing the algorithms needed to sample it. This separation is intentional and important: a student who only learns to run a sampler on a given posterior has not learned Bayesian modeling. Module 5 builds the modeling layer; Modules 7–8 build the computational layer on top of it.

**Module 6** is the theoretical hinge of the MCMC arc. It treats Markov chains as dynamical systems whose convergence properties govern the quality of any sampler built on them. Irreducibility, aperiodicity, detailed balance, mixing time, and the spectral gap are developed here not as abstract facts but as explanations for sampler behavior. This module is what separates a student who can run a sampler from a student who understands why it worked or why it failed. It is the highest-value investment in the program's second half.

**Module 7** constructs the MCMC algorithms. With the Markov chain theory from Module 6 in place, the Metropolis-Hastings algorithm follows from the detailed balance condition as a derived result rather than a recipe. Gibbs sampling, Metropolis-within-Gibbs, and Sampling Importance Resampling (which connects back to Module 2's importance sampling) are developed as a related family of approximate sampling strategies — each solving the same core problem by different design choices. The connection between algorithm design and chain behavior is kept explicit throughout.

**Module 8** addresses the question practitioners most often skip: how do you know whether to trust your MCMC output? Effective sample size, autocorrelation, trace plots, R-hat, warm-up, and thinning are developed as principled tools for answering that question. The module's goal is a practitioner who treats diagnostic analysis as an integral part of MCMC, not an afterthought.

**Module 9** covers density estimation: the problem of estimating a distribution nonparametrically from data or from sampler output. This module is motivated by the practical need to interpret posterior distributions, predictive distributions, and sampler output as distributions rather than scalar summaries. Kernel density estimation, bandwidth selection, Rao-Blackwellization in MCMC settings, and nearest-neighbor methods are covered.

**Module 10** integrates the program's tools across applied cases. The emphasis is on workflow and judgment: selecting the right tool for each sub-problem, recognizing when a method's assumptions are being stressed, producing reproducible results, and reporting conclusions honestly. The module closes with two short disciplinary retrospectives (Efron & Hastie Epilogue and Gelman & Vehtari 2021) that situate the program's methods within the broader arc of modern statistical practice — closing the frame opened by Tukey in Module 0.

---

## The Program's Module Map

| Module | Name | Est. Hours* | Core Contribution | Feeds Into |
|--------|------|------------|-------------------|------------|
| 0 | Computational Thinking | 3–4 | Establishes the algorithmic framing of statistics | All modules |
| 1 | Random Number Generation | 5–6 | Builds the simulation primitives everything else depends on | Modules 2, 3, 7 |
| 2 | Monte Carlo Estimation | 12–15 | Error theory and variance reduction; importance sampling extended to resampling | Module 7 (SIR) |
| 3 | Bootstrap & Resampling | 13–15 | Data-driven inference and its limits | Module 10 |
| 4 | Optimization | 12–15 | Gradient, metaheuristic, and EM approaches to computing estimators | Module 10 |
| 5 | Bayesian Modeling | 6–8 | Model construction as a distinct layer from computation | Modules 7, 8, 10 |
| 6 | Markov Chains | 8–10 | Convergence theory that governs sampler quality | Modules 7, 8 |
| 7 | MCMC Methods | 15–18 | SIR, MH, Gibbs, and Metropolis-within-Gibbs as a related family | Modules 8, 9 |
| 8 | MCMC Diagnostics | 8–10 | Evaluating sampler output; workflow for trusting or questioning results | Module 10 |
| 9 | Density Estimation | 6–8 | Nonparametric distribution estimation from data and MCMC output | Module 10 |
| 10 | Applied Cases | 8–10 | Workflow integration and disciplinary retrospective | — |

**Estimated total: ~96–119 hours.** 

**These hours estimates include only core material; they **do not account** for any of the optional readings and problems.*


---

## The Central Spine

The program has a spine: Modules 1–2 (simulation foundations) → Module 6 (Markov chain theory) → Modules 7–8 (MCMC methods and diagnostics). These modules form a conceptual chain where each builds directly on the previous one. If you shortchange any of them, the later modules lose their explanatory foundation and become recipes instead of understood methods.

This program treats Markov chains as a subject, it dedicates an entire module to it before delving into MCMC; that one decision is what separates a student who can run a sampler from a student who can reason about why it worked.

---

## The Three Arcs

In addition to the spine, the program has three thematic arcs that run across modules:

**The simulation arc:** Modules 1, 2, 7, and 8 form a continuous development of simulation-based inference — from generating random numbers, to Monte Carlo estimation, to approximate sampling via MCMC, to evaluating whether that sampling is working. The importance sampling thread that begins in Module 2 (Goal 6) and resurfaces in Module 7 (SIR) is the explicit bridge between Monte Carlo estimation and MCMC.

**The Bayesian arc:** Modules 5, 6, 7, 8, and 10 form the Bayesian computation sequence. Module 5 builds the model; Module 6 provides the theory; Module 7 implements the sampler; Module 8 evaluates its output; Module 10 applies the result. These modules are designed to be read in order. Do not read Module 7 before Module 6. Do not run a sampler before reading Module 5.

**The disciplinary framing arc:** Tukey (1962) opens Module 0. Efron & Hastie's Epilogue and Gelman & Vehtari (2021) close Module 10. This is deliberate. The program begins with a historical argument about what statistics is and should be, and ends by asking you to assess that argument in light of the methods you have learned. The question whether Tukey's call for a reformation of statistics has been answered is one the program expects you to take seriously.

---

## A Note on Engagement

Beyond this note, the program gives you two further program-level documents. The Goals Reference states, module by module, exactly what each module aims to teach you — it is the specification the rest of the program is built against. The Bibliography lists every reading, with the role each one plays. Both are referenced by name throughout what follows, and you will return to them often.

Each module's reading guide contains focus notes, forward pointers, a Quick Checklist, and conceptual questions. The focus notes tell you what to attend to and what to move past in each reading. The forward pointers tell you where each reading is building toward. The Quick Checklist is not a second statement of that module's goals: it takes each goal already set out in the Goals Reference and turns it into a question you can put to yourself — a fast, module-local check on your own understanding, not a substitute for the goals themselves. The conceptual questions go further. They are calibrated to distinguish between having read something and having understood it.

A student who can answer the conceptual questions for each module has genuinely internalized the material. A student who can reproduce the reading's content without being able to answer them has not. The questions are not hard in a mathematical sense — they require explanation, connection, and reasoning, not calculation. But they do require that the reading was engaged with rather than processed.

Every module except Module 10 also carries a problem set, testing something the checklist and conceptual questions cannot: whether your understanding survives implementation. Where those two test whether the material was understood, the problem set tests whether it produces working code, the right diagnostic when something goes wrong, and estimates that meet a stated verification target rather than merely a plausible-looking one.

*Read actively. The program rewards it.*

## Reading a Problem's Header

Every problem in every problem set — Module 0 through Module 9 — opens with a short header carrying a **Type** and a **Tier**. This section tells you what they mean; the same explanation appears again at the top of each problem file, so you never have to leave it to look this up.

**Type** says what kind of work the problem asks for:
- **I — Implementation.** Build the named algorithm from scratch against a known-answer target.
- **V — Verification.** Study an already-implemented algorithm's quantitative behavior: convergence, variance, coverage, efficiency.
- **D — Diagnosis.** Given or constructed, a failing case: detect and explain the failure from its computational symptoms.
- **C — Connection.** A short problem that operationalizes a link to another module in code.

A problem's Type may combine more than one code, joined by a slash — `I/V`, for instance. That means the problem is all of them at once, and each definition applies to it in full.

**Tier** says how the problem's verification target was established. It is not a difficulty rating.
- **1** — checked against a specific worked answer.
- **2** — checked against an exact fact you can derive or cite: a closed form, a known distributional result.
- **3** — checked against a range established by actually running the method many times. Not an exact-match target.
- **self-audit** — no external numeric target; check yourself against a checklist instead.

A problem's Tier may also combine more than one value. Joined by a plus sign, the verification has more than one part, each checked at the tier named — for instance, `2 (estimand) + 3 (rate-plot slope)` means one part is checked against an exact fact, labeled "estimand," and another against an executed range, labeled "rate-plot slope"; each parenthetical label matches the line it belongs to in that problem's Verification section. `self-audit` written in parentheses after a numeric tier, as in `2+3 (self-audit)`, means a self-audit checklist supplements those checks — covering something the numeric checks alone can't, usually the quality of your reasoning. A slash between two tier numbers, as in `1/2`, means that part's check sits between the two and isn't a clean fit for either; the Verification section says why.
