# Computational Statistics Program — Module Reading Guides

*Internal version 1.5.*
 
 
## Module 0 — Computational Thinking & Statistical Algorithms
**High-level goal**: Reframe statistical procedures as algorithms acting on data, and establish the computational vocabulary that organizes the rest of the program.
 
### Reading Sequence
Read in the order given.
 
1. *Tukey (1962) — The Future of Data Analysis* [Required]
**Read in full (~40 pages)**
	- **Focus**: Read as a disciplinary argument, not as historical background. Identify Tukey’s central claim about the relationship between statistics and data analysis, and note where his critique is directed. The argument is short enough that every section earns attention; resist the urge to skim.
	- **Builds toward**: Efron & Hastie Ch 1 picks up directly from Tukey’s framing — reading them together makes the progression from Tukey’s critique to modern computational practice explicit.
2. *Efron & Hastie (2016) — Computer Age Statistical Inference* [Primary]
**Ch 1: Algorithms and Inference**
	- **Focus**: Focus on the conceptual argument about what changed when computation entered statistical practice — what questions became askable, what the relationship between algorithms and inference looks like. Ch 2 (Frequentist Inference) is listed as optional orientation context; read it if you want a compact framing of classical inference as the foil for everything that follows, but it is not required.
	- **Builds toward**: This chapter’s framing of statistics as a computational discipline is the lens through which every subsequent module should be read.

### Self-Assessment
#### Quick Checklist
After finishing the reading, can you:
- Describe a familiar statistical procedure (e.g., least squares, MLE) as an algorithm — specifying its inputs, the computational process, and its outputs?
- Articulate the difference between deriving a statistical result analytically and computing one algorithmically, and explain why that distinction matters for how we evaluate methods?
- Name the questions the computational framing opens up (convergence, sensitivity, efficiency, failure conditions) and give one concrete example of each?
- Locate simulation, resampling, optimization, and MCMC within a unified algorithmic view of statistics?
- State Tukey’s central argument in one or two sentences and assess whether it has aged well?

#### Conceptual Questions
1.	Tukey writes that “data analysis” is not the same as mathematical statistics. What is the substance of that distinction, and what does it imply about how statistical methods should be evaluated?
2.	What does Efron & Hastie mean by an “algorithm” in the context of statistical inference? How is this different from a formula or a theorem?
3.	The computational framing of statistics asks: how fast does this converge, how sensitive is it to its inputs, under what conditions does it fail? Pick one of these questions and explain why it could not be asked — or was much harder to answer — in a purely analytical framework.
4.	Efron & Hastie describe a shift in statistical practice as computation became cheap. What was that shift, and what did it make possible that was not possible before?
 
## Module 1 — Random Number Generation & Simulation
**High-level goal**: Understand how randomness is constructed computationally, and build the simulation primitives that all subsequent methods depend on.

### Reading Sequence
The module has a natural two-stage structure: uniform generation first, then non-uniform. Read in the order given. Owen and L'Ecuyer cover the uniform layer in parallel — read them together before moving to the non-uniform material.

1. *Owen (2013) — Monte Carlo Theory, Methods and Examples* [Primary]
**Ch 3: Uniform random numbers**
	- **Focus**: Focus on what properties a sequence must have to behave statistically as random, and why a deterministic algorithm can produce such a sequence. The statistical tests for uniformity in this chapter are important: they are the operational definition of "good" randomness at the uniform level.
	- **Builds toward**: This lays the uniform foundation that all non-uniform methods (Ch 4 and Devroye) take as given.

2. *L'Ecuyer (1998) — Random Number Generation* [Required]
**In J. Banks (Ed.), Handbook of Simulation**
	- **Focus**: Focus on the internal mechanics of PRNG construction: LCGs, combined generators, period length, and what it means for a deterministic sequence to pass randomness tests. Owen covers what properties are required; L'Ecuyer explains how they are achieved. Read these together rather than sequentially — they address the same topic from complementary angles. Sections 4.3.5 through 4.4 (lacunary indices, matrix generators, LFSRs, nonlinear methods) go beyond what this module requires; read for awareness and move on.
	- **Builds toward**: Understanding generator mechanics is prerequisite to understanding reproducibility, period exhaustion, and the correlation artifacts that matter in Module 1, Goal 6.

3. *Owen (2013) — Monte Carlo Theory, Methods and Examples* [Primary]
**Ch 4: Non-uniform random numbers**
	- **Focus**: Read §4.1–4.2 carefully (inversion principle and worked examples) and §4.7 carefully (acceptance-rejection). The intervening sections can be read selectively: §4.3 introduces the practical challenge of inverting the normal CDF — the key point is that numerical inversion is feasible, not the implementation details of specific algorithms. §4.6 (Box-Muller and other transformations) is interesting background but is not load-bearing for this module's goals; students pressed for time may treat it as optional. §4.8 (gamma generators) illustrates acceptance-rejection proposal design in a realistic setting and is worth skimming; §4.9 (automatic generators) is optional. Keep the connection back to Ch 3 explicit throughout: inversion and acceptance-rejection both take U(0,1) draws as their input, and those draws come from the PRNG you just read about.
	- **Builds toward**: These two methods are the building blocks for every more complex sampling algorithm in the program; they reappear in Module 2 (importance sampling) and Module 7 (MCMC proposal design).

4. *Devroye (1986) — Non-Uniform Random Variate Generation* [Secondary]
**Ch II: Secs 2.1–2.3 (inversion method); Secs 3.1–3.3 (rejection method)**
	- **Focus**: Read after Owen Ch 4, not in parallel. Devroye's value is not coverage overlap but rigor and algorithmic design perspective. For the inversion method, note Devroye's Example 2.4 — the claim that inversion is "the only truly universal method" is the cleanest statement of when and why it applies. For acceptance-rejection, §3.2 is the essential section for this module: it works through the optimization of the proposal distribution explicitly, showing how to minimize the rejection constant c by choosing the best g within a parametric family. This is the formal treatment of what makes a proposal better or worse. Students pressed for time may treat §3.3 (generalizations) as a reference rather than a read-through.
	- **Builds toward**: Devroye's proposal optimization framework (§3.2) connects directly to Module 7's discussion of proposal distribution choice in Metropolis-Hastings.

**Optional depth**: *L'Ecuyer (1999), "Good Parameters and Implementations for Combined Multiple Recursive Random Number Generators,"* Operations Research 47(1). For students who want to see the technical construction of combined generators in detail. Not required for any Goal.

> **Synthesis note:** After finishing all four readings, pause before beginning the self-assessment. Try to state in one paragraph the complete generative chain — from PRNG seed through uniform output through non-uniform transformation to a final sample from an arbitrary target distribution. Each link in that chain is covered in the readings, but no single source assembles all of them. Constructing that narrative yourself is what Goal 5 asks for.

### Self-Assessment
#### Quick Checklist
After finishing the reading, can you:
•	Explain why a computer cannot generate true randomness, and describe what a pseudorandom number generator actually does?
•	Name and describe the key structural properties of a good uniform PRNG: period length, seed dependence, and the statistical tests used to evaluate output quality?
•	Implement the inverse transform method and state the conditions under which it applies?
•	Implement acceptance-rejection, explain where its efficiency comes from, and identify what makes a proposal distribution better or worse?
•	Trace a sample from an arbitrary target distribution back through the full generative chain to the PRNG output?
•	Describe at least two practical consequences of poor RNG choices in simulation?

#### Conceptual Questions
5.	A pseudorandom number generator is entirely deterministic — given the same seed, it produces the exact same sequence every time. In what sense, then, can its output be called "random"? What does randomness mean here, and how is that meaning established?
6.	The inverse transform and acceptance-rejection methods both produce draws from a target distribution, but they work in fundamentally different ways. What does each method require, and what does each assume about the target? When would you prefer one over the other?
7.	Period exhaustion is rarely discussed in practice. Why does it matter, and under what conditions could it become a real problem rather than a theoretical concern?
8.	Devroye treats the uniform generation problem as already solved and takes U(0,1) draws as given. Why is this a sensible division of labor? What would break if the uniform draws were not actually independent?
9.	Module 2 builds Monte Carlo estimation on top of the simulation primitives from this module. What specific properties of your RNG output does the validity of a Monte Carlo estimate depend on?
 
## Module 2 — Monte Carlo Estimation & Variance Reduction
**High-level goal**: Understand Monte Carlo as a principled estimation strategy, characterize its error, and learn to reduce that error — through importance sampling, stratification, and other variance reduction techniques — without simply adding more samples.

### Reading Sequence
This module has a deliberate two-stage structure. Stage 1 (error theory) must precede Stage 2 (variance reduction). Owen's variance reduction chapters assume the estimator framework and the role of variance as the controlling quantity — concepts that are built in R&C Ch 3. Do not read Owen Chs 8–9 before completing Stage 1.

#### Stage 1 — Error Theory Foundation

1. *Robert & Casella (2004) — Monte Carlo Statistical Methods, 2nd ed.* [Primary]
**Ch 3, Secs 3.1–3.2: The CLT-based estimator framework, variance as the controlling quantity, confidence interval construction**
	- **Focus**: This is the conceptual architecture for the entire module. Focus on the argument: why the sample mean converges (the strong law), what the CLT gives you (the error distribution), and how variance determines error. The proofs are worth reading once; the estimator intuition is what carries forward. Do not try to absorb all of Ch 3 now — the deferred R&C material returns at the end of Stage 2.
	- **Builds toward**: Every variance reduction technique in Stage 2 should be understood as a structured intervention in the error quantity defined here.

**Optional**: *Glasserman (2003), Monte Carlo Methods in Financial Engineering*,
**Secs 1.1.1–1.1.3 and Appendix A.** If you find R&C's register demanding, read Glasserman first as a more applied entry point to the same material, then return to R&C for the formal development. The financial engineering framing is incidental — the error theory is domain-agnostic.

#### Stage 2 — Variance Reduction

2. *Owen (2013) — Monte Carlo Theory, Methods and Examples* [Primary]
**Ch 8: Variance reduction (antithetic variates, control variates, stratification)**;
**Ch 9: Importance sampling**
	- **Focus**: For each technique, focus on three things: the mechanism (how does it reduce variance?), the structural condition that makes it effective (what property of the problem does it exploit?), and its limitation (when does it not help, or hurt?). Keep the Stage 1 framing explicit: each technique is a reduction in the n^−1/² error's leading constant, not a change in the fundamental convergence rate.
	- **Builds toward**: Importance sampling reappears in Module 7 as the conceptual foundation for SIR — the extension from computing a single estimate to producing an approximate sample from a target distribution.

3. *Robert & Casella (2004) — Monte Carlo Statistical Methods, 2nd ed.* [Primary]
**Ch 3, Sec 3.3.1 (Principles through Example 3.11, pp. 90–94); Sec 3.3.2 (the variance condition and Theorem 3.12 through the defensive mixture discussion, pp. 94–96)**
	- **Focus**: Return now to R&C Ch 3, picking up where Stage 1 left off. This scoped reading treats importance sampling as a principled estimator construction — the conditions for variance reduction, the formal weight characterization, and the defensive mixture as a robustness response to weight pathology. Read Problem 3.18 as a conceptual exercise for Goal 6: it tests whether you can connect the weight behavior to estimation failure.
Exclude: Examples 3.13–3.15, Sec 3.3.3 (AR recycling), Sec 3.4 (Laplace approximation), and Sec 3.6 Notes. These extend beyond the module's scope; the assigned six pages close the R&C Ch 3 loop without expanding into territory that belongs elsewhere in the program.
	- **Builds toward**: The weight variance and defensive mixture material here is the formal underpinning for the pathological weight discussion in Owen Ch 9 — reading them in this order lets R&C supply the theory and Owen supply the intuition.

**Optional depth**: *Owen (2013)*, **Ch 10 (Advanced variance reduction)**. Covers stratification theory, Latin hypercube sampling, and their theoretical properties in more depth. Not required for any Goal; suitable for students wanting a more thorough treatment of stratification.

> **A note on Rao-Blackwellization**: 
The Rao-Blackwell principle — that conditioning on available structure reduces variance without changing what you are estimating — is a natural extension of the variance reduction ideas in this module. It is introduced here by name so the concept is on record, but it is not assigned as a reading in Module 2. Its primary payoff in this program comes in Module 9, where it is developed and applied concretely to density estimation from MCMC output. Encountering it first in that context, where the relevant sampler structure is in hand, makes the principle a usable technique rather than an abstract theorem.

### Self-Assessment
#### Quick Checklist
After finishing the reading, can you:
•	Derive the Monte Carlo estimator from first principles and state what governs the rate at which accuracy improves with sample size?
•	Explain why variance is the central controlling quantity in Monte Carlo error, and articulate the equivalence between reducing variance and getting more information from the same computational budget?
•	Implement antithetic variates and control variates and identify the structural conditions that make each effective?
•	Implement importance sampling, explain the reweighting mechanism, and describe the conditions under which importance weights become pathological?
•	Explain antithetic variates, control variates, stratification, and importance sampling as four distinct interventions in the same underlying error quantity?
•	Explain how resampling from importance weights extends the importance sampling idea from estimation to approximate sampling, and why this matters for Module 7?

#### Conceptual Questions
10.	The Monte Carlo estimator is justified by the CLT. What exactly does that justification give you, and what does it not give you? What would have to be true about your simulation for the CLT-based confidence intervals to be valid?
11.	Control variates can substantially reduce variance, but they require knowing the expectation of a correlated random variable. If you knew that expectation, in what sense would you still need Monte Carlo? What is the practical scope of control variates?
12.	Antithetic variates, control variates, stratification, and importance sampling all reduce variance. They do so by different mechanisms. Describe each mechanism in one sentence, and explain why none of them changes the fundamental n^−1/² convergence rate.
13.	Importance sampling reweights draws from a proposal to estimate an expectation under a different target. What makes this idea useful beyond variance reduction? What problem does it solve that ordinary Monte Carlo cannot?
 
## Module 3 — Bootstrap & Resampling
**High-level goal**: Perform inference through data-driven simulation, understand the theoretical basis for its validity, and recognize the conditions under which it breaks down.
 
### Reading Sequence
Read Efron (1979) first — it is short and establishes the founding argument. Efron & Tibshirani then develops the method systematically across several stages; the readings are given in the order they should be read, not by chapter sequence alone. Davison & Hinkley is secondary but not supplemental — the failure modes material is part of what it means to understand the bootstrap.

1. *Efron (1979) — Bootstrap Methods: Another Look at the Jackknife* [Required]
**Annals of Statistics 7(1) — read in full**
	- **Focus**: Read for the founding argument: what the empirical distribution is, why sampling from it simulates the sampling process, and what assumptions that substitution requires. Do not read for technical completeness — subsequent readings will fill that in. Read it the way you read Tukey (1962) in Module 0: for the idea and its justification.
	- **Builds toward**: The empirical distribution concept introduced here is the conceptual foundation for everything in Efron & Tibshirani that follows.

2. *Efron & Tibshirani (1993) — An Introduction to the Bootstrap* [Primary]

	**Stage 1 — Bootstrap foundations and standard errors**

	- *Efron & Tibshirani*, 
	**Chs 1–2 and 4** [Required]

		- **Focus**: **Ch 1 (Introduction)** establishes the bootstrap as a computer-based simulation method for inference — read it as the systematic development of what Efron (1979) introduced. **Ch 2 (The accuracy of a sample mean)** demonstrates bootstrap standard error estimation on the simplest possible estimator; it previews the resampling algorithm before the formal definition.
		  > **Ch 3 (Random samples and probabilities)** is background probability review — the authors themselves note it "may be skimmed by readers eager to get to the details." It is not required for any Goal; treat it as optional reference material if the notation in later chapters needs grounding.

			**Ch 4 (The empirical distribution function and the plug-in principle)** is essential: it defines the empirical distribution and the plug-in principle, which is the conceptual foundation for why the bootstrap substitution works. Goal 1 depends on this chapter.

		- **Builds toward**: Ch 6, where the bootstrap is defined formally and the standard error algorithm is made precise.

	- *Efron & Tibshirani*, 
	**Ch 6** [Required]

		- **Focus**: This is the formal definition of the bootstrap standard error estimate, the resampling algorithm, and the parametric bootstrap. Focus on understanding the plug-in logic connecting Ch 4 to the bootstrap: the bootstrap standard error is the standard error of the statistic under the empirical distribution, approximated by simulation. Also note Sec 6.5 (parametric bootstrap) — Goal 2 requires implementing both parametric and nonparametric bootstrap.

		- **Builds toward**: The confidence interval chapters, where the bootstrap distribution is used not just to estimate standard errors but to construct interval endpoints directly.

	**Stage 1b — More complicated data structures and block bootstrap**

	- *Efron & Tibshirani*, 
	**Ch 8** [Required for Goal 5]

		- **Focus**: Ch 8 extends the basic bootstrap to data structures where straightforward nonparametric resampling breaks down or requires modification. Read **Secs 8.2–8.4** to understand what complications arise with one-sample problems involving structure, two-sample problems, and more general data arrangements. **Sec 8.5 (lutenizing hormone example)** shows the failure of naive resampling for serially correlated data in a concrete setting — read it alongside the failure mechanism established in Davison & Hinkley Sec 2.6.4, which diagnoses the same problem from the theoretical side. **Sec 8.6 (the moving blocks bootstrap)** is the required remediation: focus on what the blocks bootstrap corrects for, how block length is chosen, and what residual limitations remain. Goal 5 requires you to explain what this modification preserves that naive resampling destroys.

		> **Optional**: **Ch 10 (Estimates of bias)** covers bootstrap and jackknife bias estimation. Not required for any Goal, but useful as background before Ch 11 if the jackknife's bias treatment feels unmotivated on first reading.

		- **Builds toward**: Ch 11 (jackknife), where the relationship between the jackknife and bootstrap is formalized — the blocks bootstrap from Sec 8.6 provides a concrete case where the jackknife fails but the modified bootstrap succeeds.

	**Stage 2 — Jackknife**

	- *Efron & Tibshirani*, 
	**Ch 11** [Required]

		- **Focus**: Read after Ch 6. Ch 11 defines the jackknife, derives its standard error and bias estimates, and establishes its relationship to the bootstrap — the jackknife is a linear approximation to the bootstrap, and the two agree for linear statistics but diverge for nonlinear ones. **Sec 11.6 (failure of the jackknife for non-smooth statistics like the median)** is important: it illustrates that method failure is diagnosable, not merely possible. Goal 2 requires understanding this relationship.

		- **Builds toward**: The failure modes discussion in Davison & Hinkley, where the bootstrap itself encounters analogous limits.

	**Stage 3 — Confidence intervals**

	- *Efron & Tibshirani*, 
	**Ch 12** [Required]

		- **Focus**: Ch 12 introduces the bootstrap-t interval — the generalization of the Student's t approach using bootstrap replicates to estimate the t-distribution empirically. Read **Secs 12.1–12.5** as required; **Sec 12.6 (transformations and the bootstrap-t)** is depth. The bootstrap-t is second-order accurate but not transformation-respecting — hold that characterization for Ch 14, where it becomes the explicit foil.

		- **Builds toward**: Ch 13, where the percentile method is introduced as an alternative with different properties.

	- *Efron & Tibshirani*, 
	**Ch 13** [Required]

		- **Focus**: Ch 13 introduces the percentile interval. Read in full — it is short. Focus on what the percentile interval assumes (transformation-respecting but only first-order accurate) and where it fails relative to bootstrap-t. The coverage performance discussion (Sec 13.5) and the transformation-respecting property (Sec 13.6) are directly relevant to understanding why BCa was developed.

		- **Builds toward**: Ch 14, where BCa corrects both the coverage limitations of the percentile interval and the transformation problems of bootstrap-t simultaneously.

	- *Efron & Tibshirani*, 
	**Ch 14, Secs 14.1–14.3** [Required for Goal 2]

		- **Focus**: Secs 14.1–14.3 are the core of the BCa method: the motivation (neither bootstrap-t nor percentile passes the criteria for a good confidence interval), the worked example establishing the need for improvement, and the BCa construction including the bias-correction and acceleration constants. Focus on what BCa achieves that neither Ch 12 nor Ch 13 achieves alone: it is both second-order accurate and transformation-respecting. The accuracy hierarchy — standard normal < percentile < BCa, in terms of coverage error rate — is the conceptual payoff of the entire confidence interval sequence.

			> Sec 14.4 (ABC method) is secondary depth — read if you want to understand how BCa endpoints can be approximated analytically without Monte Carlo. Sec 14.5 (tooth data example) is optional depth; the authors flag it as more advanced and skippable on first reading.

		- **Builds toward**: Module 10, where bootstrap inference is deployed within an applied workflow and the choice of confidence interval method requires judgment about which assumptions are being stressed.

3. *Davison & Hinkley (1997) — Bootstrap Methods and Their Application* [Secondary]
**Sec 2.6 (selected subsections)**
	- **Focus**: **Sec 2.6.1 (consistency and asymptotic accuracy)** carries the formal theoretical content for Goal 3 — read it as the primary source for the conditions under which bootstrap confidence intervals are valid and for the pivotal/non-pivotal accuracy comparison. This subsection is not failure-mode material; it is the theoretical backstop that distinguishes what the bootstrap guarantees from what it merely approximates. **Sec 2.6.2 (rough statistics)** and **Sec 2.6.4 (when might the bootstrap fail?)** are the failure-mode content for Goal 4 — for each failure case, ask: what assumption does it violate, and what symptom would alert you in practice?
		> **Sec 2.6.3 (conditional properties)** is outside the module's scope; skip it. For the remediation methods that address the dependence failure mode identified in Sec 2.6.4, see Efron & Tibshirani Ch 8 (Stage 1b above).
	- **Builds toward**: The failure modes identified here reappear in Module 10, where the bootstrap is deployed as a subsidiary inference tool and its assumptions need to be evaluated in context.

4. *Davison & Hinkley (1997) — Bootstrap Methods and Their Application* [Secondary]
**Sec 3.8 (Hierarchical Data)**
	- **Focus**: Diagnostic/conceptual only — there is no implementation requirement attached to this reading. Sec 3.8 identifies why within-cluster correlation violates the i.i.d. resampling assumption behind the ordinary nonparametric bootstrap: observations drawn from the same cluster are not exchangeable with observations from a different cluster, so resampling individual observations as if they were i.i.d. misrepresents the data-generating process. **Keep this mechanism distinct from the serial-dependence failure mechanism** covered via Sec 2.6.4 above and Efron & Tibshirani Ch 8 (Stage 1b) — serial dependence is a temporal-correlation failure; clustering is a grouping/exchangeability failure. The two failure modes share a family resemblance (both violate the i.i.d. assumption naive resampling requires) but are not the same mechanism and should not be conflated. This section's remediation content (cluster-aware resampling schemes) is **not assigned** and is out of scope for this module, consistent with the standing Goal 5 boundary — Goal 5's implementation requirement remains scoped to the moving blocks bootstrap only.
	- **Builds toward**: Nothing further in this module; the clustering failure mode is exercised at the conceptual/diagnostic level only (see the Self-Assessment checklist below).

### Self-Assessment
#### Quick Checklist
After finishing the reading, can you:
- Derive the nonparametric bootstrap from first principles — defining the empirical distribution, explaining why sampling from it simulates the sampling process, and stating what assumptions that requires?
- Implement parametric and nonparametric bootstrap and construct bootstrap-t, percentile, and BCa confidence intervals?
- Explain the theoretical conditions under which bootstrap confidence intervals are valid, and distinguish consistency from finite-sample accuracy?
- Identify the conditions under which naive bootstrap fails: heavy tails, extreme statistics, small samples, and dependent or clustered data?
- Articulate why clustered data violates the i.i.d. assumption underlying naive resampling, and distinguish this clustering failure mechanism from the serial-dependence failure mechanism addressed by the moving blocks bootstrap?
- Apply the moving blocks bootstrap for serially dependent data, explain what block resampling preserves that naive resampling destroys, and identify the role of block length in the bias-variance tradeoff of the procedure?
- Implement bootstrap-t, percentile, and BCa confidence intervals and explain what each assumes and what accuracy guarantees each provides?
- Explain the accuracy hierarchy — first-order vs. second-order accuracy — and identify which interval methods achieve each?
- Explain transformation-respecting as a property and identify which methods satisfy it?
- Describe the bootstrap as a resampling algorithm and connect it to the simulation primitives from Module 1?

#### Conceptual Questions
15.	The bootstrap replaces the unknown population distribution with the empirical distribution. What exactly does that substitution assume, and under what conditions is it a good approximation? What does “consistency” mean here?
16.	There are multiple ways to construct a bootstrap confidence interval (bootstrap-t, percentile, BCa). They give different answers in finite samples. Why do they differ, and when does the difference matter?
16a.	The BCa method is described as both second-order accurate and transformation-respecting, while the percentile method is transformation-respecting but only first-order accurate, and the bootstrap-t is second-order accurate but not transformation-respecting. Explain what each of these properties means and why BCa achieves both while the others achieve only one.
17.	The bootstrap is sometimes described as “assumption-free.” Is that accurate? What does the bootstrap assume, and what does it not assume?
18.	The bootstrap fails for heavy-tailed distributions of the mean. Explain the mechanism of that failure — why does the empirical distribution not capture the behavior of the tail, and why does that matter for the bootstrap confidence interval?
19.	The moving blocks bootstrap corrects for temporal dependence by resampling overlapping blocks of consecutive observations rather than individual draws. What property of the data is being preserved, and what does naive resampling destroy? What role does block length play in the bias-variance tradeoff of the procedure?
 
## Module 4 — Optimization: Gradient Methods, Metaheuristics & EM
**High-level goal**: Compute estimators via optimization, understand the structural differences between gradient, metaheuristic, and EM approaches, and know which problem features determine which method is appropriate.

### Reading Sequence
The module has three tracks corresponding to three algorithmic families. Tracks A and B should be read in order — EM builds on the optimization theory foundation Track A establishes. Track C is short and can be read at any point after Track A, but reading it last, with the full module in view, makes the structural contrast between the three families clearest.

#### Track A — Gradient Methods

1. *Lange (2010) — Numerical Analysis for Statisticians, 2nd ed.* [Primary]
**Ch 11, Secs 11.1–11.2: Introduction and Unconstrained Optimization**
	- **Focus**: Read **Sec 11.1** as orientation, then work through **Sec 11.2** carefully. The central results are Fermat's necessary condition (vanishing gradient at a local minimum), the second-order sufficient condition (positive definite Hessian at a stationary point), and what coerciveness guarantees about the existence of a minimum. These are the theoretical foundations on which all iteration schemes in this chapter rest. The examples in Sec 11.2 are worth following through; they show what analytical solvability looks like and why it is exceptional.
		> **Exclude**: **Secs 11.3–11.4** (Optimization with Equality and Inequality Constraints, Lagrange multipliers, KKT conditions). These are important for constrained optimization but are not load-bearing for any goal in this module. **Sec 11.5 (Convexity)** and **Sec 11.6 (Block Relaxation)** are also excluded — convexity is used implicitly throughout the module but not developed here at the required depth, and block relaxation is a topic for the MM framework in Ch 12.
	- **Builds toward**: The stationarity and Hessian results from Sec 11.2 are the theoretical underpinning for Newton's method in Ch 14 — you are establishing the optimality conditions that Newton's method is designed to find.

2. *Lange (2010) — Numerical Analysis for Statisticians, 2nd ed*. [Primary]
**Ch 14, Secs 14.1–14.4**:
Introduction, Newton's Method and Root Finding, Newton's Method and Optimization, Ad Hoc Approximations of Hessians
	- **Focus**: **Sec 14.1** is short — read it to see how Lange situates Newton's method relative to MM and EM. **Sec 14.2** establishes the root-finding form of Newton's method (which most students will have seen in one dimension); **Sec 14.3** applies it to optimization of a loglikelihood, introducing the score and observed information. This is where Ch 11's Hessian theory becomes a practical computation. **Sec 14.4 (Ad Hoc Hessian Approximations)** is important for Goal 2: it explains why positive definite Hessian approximations are sought and introduces the outer-product approximation and the idea of replacing second-order terms that are small on average. Read Sec 14.4 for the conceptual logic rather than for technical exhaustiveness.
	> **Exclude**: **Secs 14.5–14.8** (Scoring and Exponential Families, Gauss-Newton, Generalized Linear Models, MM Gradient Algorithm). These are well-crafted applications and extensions but are outside the stated goals of this module — they require the exponential family and GLM background that the program does not develop here, and the MM gradient algorithm presupposes Ch 12 (unassigned). **Secs 14.10–14.11** (Accelerated MM and Problems) are also excluded.
	
	- **Builds toward**: Secs 14.1–14.4 deliver Goal 2 directly. Sec 14.9 (quasi-Newton) follows below.

3. *Nocedal & Wright (2006) — Numerical Optimization, 2nd ed.* [Secondary]
**Sec 3.1: Wolfe conditions and step-length selection**
	- **Focus**: Read as the formal backstory to the step-selection concern raised in Lange Ch 14. The sufficient decrease condition (Armijo) and curvature condition together constitute the Wolfe conditions; understand why both are needed and what each one prevents. This section is self-contained and short.
	- **Builds toward**: Step-length selection is what keeps Newton-type methods from overshooting or cycling far from the solution — this is the practical stability concern Goal 2 asks you to explain.

4. *Lange (2010) — Numerical Analysis for Statisticians, 2nd ed.* [Primary]
**Ch 14, Sec 14.9: Quasi-Newton Methods**
	- **Focus**: Read after Secs 14.1–14.4 and the Wolfe conditions material. Sec 14.9 introduces the secant condition and Davidon's rank-one update, followed by the DFP and BFGS rank-two updates. Focus on the conceptual logic: quasi-Newton methods avoid the cost of computing the Hessian exactly by building an approximation iteratively from gradient information. The self-correcting properties of BFGS (mentioned in Ch 14 and developed more fully in N&W Sec 6.1) are the reason BFGS dominates in practice.
	- **Builds toward**: Goal 2 requires understanding quasi-Newton methods, not just Newton's method. Sec 14.9 is the primary source; N&W below provides the convergence and practical detail.

5. *Nocedal & Wright (2006) — Numerical Optimization, 2nd ed.* [Secondary]
**Sec 6.1: BFGS method and convergence; Sec 7.2: L-BFGS**
	- **Focus**: Use as targeted depth after Lange Sec 14.9. Sec 6.1 works through the BFGS update formula, convergence properties, and the self-correcting behavior in detail. Sec 7.2 covers L-BFGS (limited-memory BFGS) for large-scale problems where storing the full approximate Hessian is infeasible. For Sec 7.2, the goal is understanding what problem L-BFGS solves and how the two-loop recursion replaces explicit Hessian storage — implementation detail is not required.
		> **Optional**: Nocedal & Wright Appendix A (conditioning and numerical stability). Provides the formal definitions of conditioning and stability and their relationship to convergence. Read if the conditioning material in Lange Ch 14 feels underspecified; treat as a reference rather than a read-through.
	- **Builds toward**: Goal 2's requirement to explain the practical significance of numerical stability and step selection is directly addressed across N&W Secs 3.1, 6.1, and Appendix A.

#### Track B — EM Algorithm

6. *Dempster, Laird & Rubin (1977) — Maximum Likelihood from Incomplete Data via the EM Algorithm* [Required]
**JRSS-B 39(1) — read in full**
	- **Focus**: Read for the founding argument: the missing data framing, the construction of the E and M steps, and the monotone likelihood claim. Do not read for technical completeness — Lange Ch 13 and Wu (1983) fill that in. Read DLR the way you read Tukey (1962) in Module 0: for the idea and its justification.
	- **Builds toward**: The missing data framing here is the conceptual key to Goal 3. Understanding EM as a statistical algorithm — not just a numerical procedure — depends on seeing what problem it is designed to solve.

7. *Lange (2010) — Numerical Analysis for Statisticians, 2nd ed.* [Primary]
**Ch 13, Secs 13.1–13.4: Introduction, General Definition, Ascent Property, Missing Data in the Ordinary Sense**
	- **Focus**: Read after DLR. Secs 13.1–13.2 restate the EM definition formally; Sec 13.3 (Ascent Property) is the most important section in the chapter — it proves monotone likelihood increase via Jensen's inequality. Work through this proof carefully: understanding why the ascent property holds, not just that it does, is what Goal 4 requires. Sec 13.4 shows EM applied to exponential families with missing data, which is the most common practical setting and the clearest illustration of how the E step fills in a sufficient statistic.
	> **Note on Sec 13.3**: Lange's introduction to Ch 13 warns that the proof involves measure theory and that some readers may want to take the result on faith. Do not do this. The proof in Sec 13.3 is the Jensen's inequality argument — it is accessible and is the conceptual heart of Goal 4. Read it.

	> **Note on the MM framework**: Lange presents EM as a special case of the MM algorithm, and Ch 13 contains repeated references to Ch 12 (The MM Algorithm), which is not assigned. You do not need Ch 12 to follow Ch 13 — the EM derivation is self-contained — but students who find the MM references distracting may consult Ch 12 Secs 12.1–12.2 (Introduction and Philosophy of the MM Algorithm) for orientation. This is purely optional.

	> **Exclude**: **Secs 13.5–13.9** (Bayesian EM, Allele Frequency Estimation, Clustering, Transmission Tomography, Factor Analysis). These are worked examples of EM in specific contexts — well-constructed and worth returning to, but not load-bearing for any of the five module goals. 
	Students who want a concrete example beyond Sec 13.4 should read Sec **13.6 (Allele Frequency Estimation)**, which is the most self-contained of the application sections and clearly illustrates the interplay between observed phenotypes and latent genotypes as missing data.

	- **Builds toward**: Secs 13.1–13.4 deliver Goals 3 and 4 directly.

8. *Wu (1983) — On the Convergence Properties of the EM Algorithm* [Secondary]
**Annals of Statistics 11(1) — read for the main result and its significance**
	- **Focus**: Read for what Wu establishes over DLR: the stationary point characterization, and why monotone increase does not imply convergence to the global maximum — or even to a local maximum, in the absence of additional conditions. You do not need to work through every proof; the conceptual contribution and its relationship to DLR's original claim is the target. Goal 4 asks you to articulate this relationship precisely.
	- **Builds toward**: This is the sole source for the DLR-versus-Wu distinction that Goal 4 requires.

#### Track C — Metaheuristics

9. *Givens & Hoeting (2013) — Computational Statistics, 2nd ed.* [Reference]
**Ch 3: Sec 3.3 (Simulated annealing); Sec 3.4 (Genetic algorithms)**
	- **Focus**: Read for orientation and conceptual understanding, not implementation depth. The goal is to understand when metaheuristic approaches are warranted — discontinuous objectives, multimodal landscapes, discrete or combinatorial search spaces — and what each method does at the level of operating principles. No implementation is required for Goal 5.
	> **Forward pointer**: Simulated annealing accepts worse solutions with a probability controlled by a temperature schedule. This is structurally parallel to the Metropolis-Hastings acceptance step in Module 7 — both use a ratio-based acceptance criterion to explore a target landscape. Noticing that parallel before reaching Module 7 makes the MH acceptance ratio feel less arbitrary when you derive it from detailed balance.

### Self-Assessment

#### Quick Checklist
After finishing the reading, can you:
- Formulate at least two common statistical estimators as optimization problems, and identify which objective function features determine the appropriate algorithmic family?
- Explain Newton's method and quasi-Newton methods, including the role of the Hessian and the practical significance of numerical stability and step selection?
- Explain the statistical logic of EM — missing data, latent variables, lower-bound ascent — and describe the construction of the E and M steps?
- Explain why EM guarantees monotone likelihood increase, why this does not guarantee a global maximum, and what Wu (1983) establishes over Dempster et al. (1977)?
- Recognize when metaheuristic approaches are warranted and describe the basic operating principles of simulated annealing and genetic algorithms without requiring deep implementation?

#### Conceptual Questions
20. Newton's method converges quadratically near a solution but can diverge or cycle far from one. What is the mechanism of quadratic convergence, and what can go wrong far from the solution?
21. Quasi-Newton methods approximate the Hessian rather than computing it exactly. What is the tradeoff? When would you prefer BFGS over Newton's method, and when might the approximation cause problems?
22. EM is described as an algorithm for "maximum likelihood from incomplete data." What does incomplete data mean in this context, and how does that framing generate the two-step structure?
23. EM guarantees that the likelihood increases at every iteration. Does this mean it will find the global maximum? Explain what Wu (1983) says about where EM converges and why that is weaker than convergence to the MLE.
24. Simulated annealing accepts worse solutions with some probability. Gradient methods always move in an improving direction. What problem does that probabilistic acceptance solve, and why does gradient descent not solve it?
 
## Module 5 — Bayesian Modeling Framework
**High-level goal**: Construct and reason about Bayesian models as structured computational objects, independent of the sampling algorithms used to fit them.
 
### Reading Sequence
All readings come from *Gelman et al. (BDA)*. The module is self-contained within that text. Read in order — earlier chapters build the modeling vocabulary that later chapters require. 
Ch 7 (simulation-based inference) is explicitly deferred to Module 7: do not read ahead.
 
1. *Gelman et al. (2013) — Bayesian Data Analysis, 3rd ed.* [Primary]
**Ch 1: Probability and inference**
	- **Focus**: Establish the Bayesian model structure: the joint distribution, likelihood, prior, and posterior, and what each component commits you to. This chapter’s probability framework is used throughout the program — make sure the notation and the interpretive conventions are solid before proceeding.
	- **Builds toward**: This chapter’s framework is what Module 7 will use when constructing a posterior to sample from.
2. *Gelman et al. (2013) — Bayesian Data Analysis, 3rd ed.* [Primary]
**Ch 2: Single-parameter models**
	- **Focus**: Use single-parameter models to develop the intuition for prior-to-posterior updating, conjugacy, and what prior choice implies for the posterior. The arithmetic here is simple enough that you can trace every step; the conceptual content is what matters. **Sec 2.8 (Noninformative prior distributions)** and **Sec 2.9 (Weakly informative prior distributions)** are the chapter's most direct material for Goal 2: read them as a treatment of prior selection as a modeling choice with traceable consequences, not as an aside on a special case. The same sections are the primary basis for Goal 4's prior-sensitivity component — Sec 2.8 in particular makes explicit how disputing a posterior conclusion amounts to a claim about missing prior or likelihood information.
	- **Builds toward**: The prior sensitivity reasoning developed here in Secs 2.8–2.9 is revisited and extended in Ch 5, Sec 5.7, where the same questions are posed for hierarchical variance parameters.
3. *Gelman et al. (2013) — Bayesian Data Analysis, 3rd ed.* [Primary]
**Ch 3: Multiparameter models (read selectively for structural patterns)**
	- **Focus**: Do not read for derivation detail. Read **Sec 3.1 (Averaging over nuisance parameters)** in full — this is the chapter's most direct material for Goal 3: it establishes why marginalization is necessary and what the joint-posterior-to-marginal-posterior route looks like in general. Read the opening of **Sec 3.2** (through the statement of the joint posterior for the normal model) for a concrete instance of that structure. Treat **Sec 3.4** (multinomial) and **Secs 3.5–3.6** (multivariate normal) as reference rather than required reading — skim them for the pattern (multiple parameters, an intractable-by-hand joint posterior), not for the algebra; their value for this module is illustrating that multiparameter posteriors resist closed-form summary.
		> **Sec 3.7 (bioassay example)** is optional and may be skimmed for how grid-based numerical computation handles a nonconjugate case.
	- **Builds toward**: Multiparameter posterior structure is what makes closed-form computation impossible in general — motivating the need for the sampling methods in Modules 7–8.
4. *Gelman et al. (2013) — Bayesian Data Analysis, 3rd ed.* [Primary]
**Ch 5 (selected): Hierarchical models — why they arise, what they require computationally**
	- **Focus**: Focus on the conceptual argument: why hierarchical structure arises from modeling multiple exchangeable groups, what partial pooling means, and what the computational cost is. **Secs 5.1–5.2** (constructing a hierarchical prior, exchangeability) and **Sec 5.5** (the eight-schools example) carry this argument most directly and should be read closely. **Secs 5.3–5.4** contain the computational machinery for conjugate hierarchical models — read these for what they illustrate about the structure of the problem (why the marginal posterior of the hyperparameters has the form it does, why complete pooling and no pooling are special cases of the same model) rather than working through the integration and simulation steps in detail; that level of computational engagement is outside this module's scope by design. **Sec 5.7** (weakly informative priors for variance parameters) is required: it is the chapter's most direct demonstration of prior sensitivity in a hierarchical setting and is the primary source for Goal 4 in this module.
	- **Builds toward**: Hierarchical models are the canonical setting where MCMC becomes necessary, making this reading a bridge to Module 7.
		> Note: **BDA Ch 11** (Basics of Markov chain simulation) is intentionally deferred to Module 7. Do not read it here. The goal of this module is to build the modeling layer independently of the computational layer — understanding what you are trying to sample before you learn how to sample it.

### Self-Assessment
#### Quick Checklist
After finishing the reading, can you:
- Specify a Bayesian model as a computational object — joint distribution, likelihood, prior, and posterior — and articulate what each component commits you to?
- Reason about prior selection as a modeling choice with verifiable consequences, distinguishing between informative, weakly informative, and vague priors and explaining what each implies?
- Identify the structural patterns in multiparameter and hierarchical models and explain what hierarchical structure implies computationally?
- Criticize a Bayesian model by interrogating prior sensitivity, likelihood misspecification, and predictive adequacy — independently of how the model will be fit?
- Maintain a clear separation between modeling questions (what is the right prior? is the likelihood appropriate?) and computational questions (how do I sample the posterior?)?

#### Conceptual Questions
25.	A Bayesian model specifies a joint distribution over data and parameters. What does this specification assume, and what work does the prior do within that specification? Is the prior subjective?
26.	Prior sensitivity analysis tests whether the posterior changes substantially when the prior changes. What would a large change in the posterior imply about your model? What would a small change imply? When is sensitivity analysis required and when can it be skipped?
27.	Hierarchical models pool information across groups. What is the computational cost of that pooling? Why does it make closed-form posterior computation generally impossible?
28.	This module deliberately separates modeling from computation. Why is that separation useful? What goes wrong if you think about the two together?
29.	BDA Ch 11 (Basics of Markov chain simulation) is deferred to Module 7. What question does that chapter answer that this module does not? What does Module 5 equip you to do that you could not do after only reading about MCMC methods?
*Note: This question deliberately asks you to reason about a chapter you have not yet read. You are not expected to know what BDA Ch 11 contains — you are expected to reason from what Module 5 does cover: what modeling questions it settles, and what questions it leaves open. The answer you construct here will be tested against the actual Ch 11 content when you reach Module 7.*
 
## Module 6 — Markov Chains as Computational Objects
**High-level goal**: Understand Markov chains as dynamical systems whose convergence properties govern the quality of MCMC samplers, building the theoretical vocabulary needed to reason about sampler behavior.

### Reading Sequence
Begin with the concrete example (LPW Ch 3) before formalizing anything. The module is designed to move from observation to theory: watch a chain run on a simple target, then read the formal properties as an explanation of what you observed.

1. *Levin, Peres & Wilmer (2009) — Markov Chains and Mixing Times* [Primary]
**Ch 3: Metropolis and Glauber chains** — read as a concrete entry point before the formal theory
	- **Focus**: Before reading any formal definitions, observe what a Markov chain on a simple target actually does. Ch 3 gives you a concrete example. Watch the chain mix (or fail to). Identify mixing and stationarity as empirical phenomena. Then proceed to the formal theory with those observations in mind. 
		> **Note**: Ch 3 introduces some formal notation and terminology (transition kernels, stationarity conditions) before those concepts are developed in Ch 1 — hold them lightly on first pass and let Ch 1 supply the grounding retroactively. The Ising model figure (Figure 3.2, low/critical/high temperature configurations) is the clearest observational content in the chapter — give it close attention even as you move more quickly through the surrounding derivations.
		
	- **Builds toward**: The empirical phenomena you observe here are exactly what Goal 1 asks you to identify before formalizing — and they are what the formal theory in Ch 1 explains.

2. *Levin, Peres & Wilmer (2009) — Markov Chains and Mixing Times* [Primary]
**Ch 1: Secs
1.1 (Markov chains),
1.3 (irreducibility and aperiodicity),
   1.5 (stationary distributions),
   1.6 (reversibility and time reversals — detailed balance)**
	> **Skip**: **Secs 1.2** **(Random Mapping Representation)** and **1.4 (Random Walks on Graphs)** fall between the assigned sections but are not required for any goal in this module — skip them.
	- **Focus**: This is the core formal theory. For each property (irreducibility, aperiodicity, stationarity, detailed balance), connect it back to what you observed in Ch 3: what does this property guarantee about long-run behavior, and what failure does its absence produce? Detailed balance is the most important concept here — it is the condition that MCMC algorithms are designed to satisfy.
	- **Builds toward**: Detailed balance from this chapter is the condition that Module 7 will use to derive the Metropolis-Hastings acceptance ratio.

4. *Levin, Peres & Wilmer (2009) — Markov Chains and Mixing Times* [Primary]
**Ch 4: Introduction to Markov Chain Mixing — total variation distance, convergence theorem, mixing time**
	- **Focus**: Focus on mixing time as an operational concept: how many steps does it take for the chain to be close to stationarity, and what determines that number? Total variation distance is the measure — understand what it is measuring and why it is the right quantity. The coupling characterization of total variation distance (Proposition 4.7, Figure 4.2) is worth sitting with: it gives a second, more intuitive way to see what the distance is measuring beyond the formal definition.
	- **Builds toward**: Mixing time is the bridge from formal theory to practical consequences: a chain with slow mixing produces correlated output, which is what Module 8's ESS diagnostic measures.

5. *Levin, Peres & Wilmer (2009) — Markov Chains and Mixing Times* [Primary]
**Ch 12: Secs 12.1–12.2 (spectral representation, relaxation time, spectral gap);
Sec 12.3.1 (the n-cycle example only);
Sec 12.7 (Time Averages)**
	> **Skip: Secs 12.3.2 through 12.6** (lumped chains and the path, product chains, the spectral formula for target time, and the ℓ² bound) are not required for this module's goals. This is substantial material — roughly two-thirds of the chapter — and skipping it is intentional, not a shortcut: these sections develop machinery for problems outside this module's scope (card shuffling, Glauber dynamics spectral gaps for product measures, hitting times). Sec 12.7 picks up directly after Sec 12.3.1 in relevance, even though several chapter sections fall between them.
	- **Focus**: **Secs 12.1–12.2** develop the spectral representation of a reversible chain and define the absolute spectral gap, the spectral gap, and the relaxation time — and give the key operational inequality showing that variance decays at a rate governed by the gap. **Sec 12.3.1 (the n-cycle)** is the chapter's clearest source of geometric intuition: the eigenvalues are literally cosines of angles around the cycle, and seeing the spectral gap shrink as O(n⁻²) for a long cycle is what makes "small spectral gap means slow mixing" concrete rather than abstract. Then **Sec 12.7 (Time Averages)** connects the spectral gap directly to a practical question: how many MCMC samples do you need to estimate a posterior expectation to a given accuracy? Theorem 12.21 answers this in terms of γ⁻¹ — note that this is the same spectral gap defined in Sec 12.2, so keep that definition in view when reading Sec 12.7.
	- **Builds toward**: The spectral gap concept provides the theoretical vocabulary for diagnosing why a sampler is performing poorly — a vocabulary that becomes practically relevant in Module 8. The Sec 12.7 result is the direct, quantitative version of that connection: it is what Goal 5 asks you to explain.

### Self-Assessment
#### Quick Checklist
After finishing the reading, can you:
- Describe a concrete Markov chain mixing on a simple target, and identify mixing, stationarity, and failure to converge as empirical phenomena?
- Define irreducibility, aperiodicity, and stationarity and explain what each guarantees about long-run behavior?
- Explain detailed balance as a sufficient condition for stationarity and state why it is the condition MCMC algorithms are designed to satisfy?
- Define mixing time and the spectral gap as measures of convergence speed and develop geometric intuition for why some chains mix slowly?
- Connect poor mixing to downstream consequences for MCMC output quality — explaining what slow mixing implies for estimates derived from sampler output?

#### Conceptual Questions
30.	Irreducibility, aperiodicity, and detailed balance are all conditions a Markov chain can satisfy. What does each condition guarantee individually, and what do they guarantee together?
31.	Detailed balance is described as a sufficient condition for stationarity, not a necessary one. What does that mean? Could you construct a chain that has the right stationary distribution but does not satisfy detailed balance?
32.	Mixing time measures how long it takes a chain to get close to stationarity. "Close" is measured in total variation distance. Why is total variation the right distance measure here? What would it mean for a chain to be "not close" to its stationary distribution?
33.	The spectral gap governs mixing speed. What is the relationship between a small spectral gap and slow mixing? Using the n-cycle as a concrete case, explain why a longer cycle has a smaller spectral gap and what that implies for how long the chain takes to mix.
34.	This module argues that understanding Markov chains as dynamical systems is not optional background for MCMC practitioners. Make that argument concretely: what would a student who skipped this module be unable to explain or diagnose?
35.	Theorem 12.21 shows that the number of MCMC samples needed to estimate a posterior expectation to a given accuracy scales with the inverse of the spectral gap. What does this mean in practical terms for a chain that mixes slowly, and why isn't the number of raw samples alone an adequate measure of how much information you have?
 
## Module 7 — MCMC Methods
**High-level goal**: Implement and understand the core approximate sampling algorithms — SIR, Metropolis-Hastings, Gibbs, and Metropolis-within-Gibbs — as a related family of design choices whose behavior follows from the theory in Module 6.
 
### Reading Sequence
Begin with SIR as a conceptual bridge from Module 2’s importance sampling to the MCMC setting. Then develop MH and Gibbs as principled solutions to the sampling problem SIR leaves open. The reference sources (Roberts & Rosenthal; VanDerwerken) should be consulted for specific goals, not read in sequence.
 
1. *Givens & Hoeting (2013) — Computational Statistics, 2nd ed*. [Primary]
**Ch 6, Sec 6.3.1: Sampling Importance Resampling (SIR) Algorithm**
	- **Focus**: Read this as the bridge from Module 2. SIR extends the importance sampling idea from computing a single estimate to producing an approximate sample from a target distribution by resampling proportionally to importance weights. Identify exactly where it connects back to Module 2, Goal 6, and why it still requires a good proposal.
	- **Builds toward**: SIR frames the core challenge that motivates MCMC: producing an approximate sample from a complex target when direct sampling is impossible.
	  
2. *Gelman et al. (2013) — Bayesian Data Analysis, 3rd ed.* [Reference]
**Ch 10, Sec 10.4: Importance sampling as background context for SIR**
	> **Optional reading.**
	- **Focus**: If the connection between importance sampling and SIR is not clear after Givens & Hoeting, this section provides additional framing from a Bayesian computation perspective. Not required if Givens & Hoeting was sufficient.
	- **Builds toward**: This reading reinforces the Module 2 connection and situates SIR within the Bayesian computation workflow.
	
3. *Robert & Casella (2004) — Monte Carlo Statistical Methods, 2nd ed.* [Primary]
**Ch 7: Metropolis-Hastings — derivation, variants, practical choices**
	- **Focus**: Focus on the derivation from detailed balance: understand why the acceptance ratio takes the form it does, and what happens to the chain’s stationary distribution if you change it. Then focus on the proposal distribution problem: how does proposal width affect acceptance rate and autocorrelation, and why is there a tradeoff?
	- **Builds toward**: The acceptance ratio derivation here connects directly back to Module 6’s detailed balance condition — MH is the algorithm designed to satisfy that condition for an arbitrary target.
	
4. *Gelman et al. (2013) — Bayesian Data Analysis, 3rd ed.* [Primary]
**Ch 11: Basics of Markov chain simulation (now introduced with full context)**
	- **Focus**: Read this after R&C Ch 7. BDA Ch 11 provides the Bayesian practitioner's perspective on the same methods — the emphasis is on how to think about the sampler as a tool for posterior inference rather than as a generic algorithm. Focus on **Secs 11.1–11.3**, which connect the sampling algorithms to the Bayesian modeling framework built in Module 5. In particular, Sec 11.3 ("Using Gibbs and Metropolis as building blocks") is the primary source for Goal 6: it introduces Metropolis-within-Gibbs as the answer to the question that R&C Chs 9–10 leave open — what do you do when a full conditional is not tractable?
	  > **Read Sec 11.3 after finishing R&C Chs 9–10, not before**.
	  
	  > **Secs 11.4–11.5** (convergence monitoring and ESS) can be read for orientation here, but will be revisited as primary content in Module 8 alongside Geyer (1992), where they belong in the diagnostic workflow. Deep engagement with those sections should wait.
	- **Builds toward**: BDA Ch 11 connects the algorithmic machinery to the Bayesian modeling framework from Module 5 — this is where the two threads meet.
	
5. *Robert & Casella (2004) — Monte Carlo Statistical Methods, 2nd ed.* [Primary]
**Chs 9–10: The Two-Stage and Multi-Stage Gibbs Sampler — structure, conditional specification, blocking**
	- **Focus**: Focus on why full conditional distributions guarantee acceptance at every step (the derivation from detailed balance), and on the distinction between random-scan and deterministic-scan Gibbs. The blocking discussion is practically important — understand how block structure affects mixing.
	- **Builds toward**: The deterministic-scan Gibbs subtlety addressed in VanDerwerken (below) is the most common conceptual confusion about Gibbs samplers — keep it in mind while reading R&C’s treatment. Also note: because Gibbs sampling produces full conditional distributions as a byproduct at every step, it creates an opportunity for variance-reduced density estimation that other samplers do not; this is the basis for the Rao-Blackwellization technique covered in Module 9.
	
6. *Roberts & Rosenthal (2001) — Optimal Scaling for Various Metropolis-Hastings Algorithms* [Reference]
**Statistical Science 16(4) — targeted reading for Goal 3**
	- **Focus**: Read for the acceptance rate target result: the theoretical result that optimal Metropolis-Hastings performance (in certain settings) corresponds to an acceptance rate of approximately 0.234 for random walk proposals in high dimensions. Understand what this result gives you and what it does not: it is a guideline, not a formula.
	- **Builds toward**: The proposal scaling result provides a theoretical anchor for the practical advice — “tune your acceptance rate” — that Module 8 will revisit in the diagnostic workflow.
	
7. *VanDerwerken (2017) — Not Every Gibbs Sampler is a Special Case of the MH Algorithm* [Reference]
**Communications in Statistics — Theory and Methods 46(20) — targeted reading for Goal 5**
	- **Focus**: Short paper. Read for the single result: deterministic-scan Gibbs does not satisfy detailed balance in general, and therefore cannot be understood as a special case of MH. The random-scan version can. Understand why this distinction matters for how you reason about the chain’s stationary distribution.
	- **Builds toward**: This result is what Goal 5 asks you to articulate. Without it, the deterministic-scan / random-scan distinction seems like a technical footnote; with it, it is a conceptual clarification about what the algorithm is actually doing.

### Self-Assessment
#### Quick Checklist
After finishing the reading, can you:
- Explain SIR as a bridge from importance sampling to approximate sampling, and identify where the connection to Module 2 lies?
- Derive the Metropolis-Hastings acceptance ratio from the detailed balance condition and explain what it enforces?
- Characterize how proposal distribution choice governs the acceptance rate / autocorrelation tradeoff in MH?
- Derive Gibbs sampling from full conditional distributions and explain why acceptance is guaranteed at every step?
- Distinguish random-scan from deterministic-scan Gibbs and explain why the deterministic-scan version does not satisfy detailed balance in general?
- Implement Metropolis-within-Gibbs and identify when this hybrid is warranted?
- Describe SIR, MH, and Gibbs as three members of a common family of approximate sampling strategies, each solving the same core problem by different design choices?

#### Conceptual Questions
36.	SIR produces an approximate sample from a target distribution by resampling from importance weights. What limits its accuracy, and why does naive SIR fail in high dimensions? What problem does MCMC solve that SIR does not?
37.	The Metropolis-Hastings acceptance ratio ensures the chain has the correct stationary distribution. Explain the mechanism: what would happen to the stationary distribution if you changed the ratio?
38.	A narrow proposal distribution in MH produces high acceptance rates but strongly autocorrelated samples. A wide proposal produces frequent rejections and similarly slow exploration. What is being traded off, and is there a principled way to resolve the tradeoff?
39.	Gibbs sampling is sometimes described as “MH with acceptance probability 1.” VanDerwerken (2017) shows this is only true for the random-scan version. What is the substantive difference between random-scan and deterministic-scan Gibbs, and why does it matter for the chain’s theoretical properties?
40.	Metropolis-within-Gibbs combines MH steps for some parameters with Gibbs steps for others. When is this warranted, and what does it require about the model structure?
 
## Module 8 — MCMC Diagnostics & Reliability
**High-level goal**: Evaluate MCMC output critically using principled diagnostics, understand what convergence does and does not guarantee, and develop a reliable workflow for determining when sampler output can be trusted.
 
### Reading Sequence
*Geyer (1992)* and *BDA* Ch 11 are the two primary sources and should be read in tandem — Geyer provides the theoretical grounding for ESS and autocorrelation, BDA provides the applied diagnostic workflow. Stan Reference Manual is the practical reference throughout. Secondary sources (Flegal et al., Cowles & Carlin, Link & Eaton) are targeted — consult them for specific goals.
 
1. *Geyer (1992) — Practical Markov Chain Monte Carlo* [Primary]
**Statistical Science 7(4) — read in full**
	> **Note**: The published version of this paper appeared in Statistical Science 7(4), which included discussion and commentary pieces by other authors. Read only Geyer’s article (pp. 473–483); the additional comments in the document are from other contributors and are not assigned.
	- **Focus**: This is the foundational treatment of ESS, autocorrelation, and the ergodic theorem for MCMC. Focus on why effective sample size is different from the raw number of iterations, how autocorrelation determines the size of that difference, and what the ergodic theorem actually guarantees about the validity of MCMC time averages. Read alongside the Module 6 ergodic theorem material (LPW Ch 12, Sec 12.7).
	- **Builds toward**: Geyer’s ESS definition is what Goal 1 asks you to explain; his autocorrelation treatment is what Goal 2 requires.
	
2. *Gelman et al. (2013) — Bayesian Data Analysis, 3rd ed.* [Primary]
**Ch 11: MCMC in practice — convergence diagnostics, R-hat, trace plots, warm-up, and ESS**
	- **Focus**: Read alongside Geyer. Focus on **Secs 11.4–11.5**. Sec 11.4 translates the theoretical concepts into an applied diagnostic workflow: how to use trace plots to identify mixing problems, how R-hat diagnoses between-chain versus within-chain variance, and what warm-up is doing. Sec 11.5 develops the effective number of simulation draws (n_eff) — the ESS formula, the variogram-based autocorrelation estimator used to compute it, and the stopping rules (R-hat < 1.1 and n_eff ≥ 5m). Both sections are required; Sec 11.5 is what Goal 1 and the stopping-rule component of Goal 6 depend on. This is the chapter to return to when running a sampler in practice.

	- **Builds toward**: Goal 1 (ESS formula and computation), and the diagnostic workflow that Goal 6 asks you to internalize as a reliable iterative practice, not a one-time checklist.
	
3. *Stan Development Team — Stan Reference Manual* [Reference]
**Section on ESS, R-hat, and warm-up**; https://mc-stan.org/docs/reference-manual
	- **Focus**: Consult as a practical reference throughout. Stan’s documentation is the authoritative source for how R-hat and ESS are implemented in practice. Pay particular attention to the bulk ESS / tail ESS distinction and the updated R-hat definition, which correct known issues with older implementations.
	- **Builds toward**: When you deploy a sampler in Module 10 or in practice, this is the reference you will use to interpret the output.
	
4. *Gelman et al. (2013) — Bayesian Data Analysis, 3rd ed.* [Reference]
**Ch 11: Basics of Markov chain simulation — revisit targeted sections**
	- **Focus**: Return to Ch 11 if needed for clarification on how MCMC output is used for posterior inference. This is supplementary to the Ch 11 convergence diagnostics material covered as primary reading, not an additional assignment. Note: BDA Ch 11 was primary reading in Module 7, where it introduced simulation-based inference with full context. No new reading is expected here — this entry is a pointer back, not an additional assignment.
	- **Builds toward**: Reinforces the connection between the diagnostic questions (is the chain mixing?) and the inferential question (can I trust this posterior summary?).
	
5. *Flegal, Haran & Jones (2008) — Markov Chain Monte Carlo: Can We Trust the Third Significant Figure?* [Secondary]
**Statistical Science 23(2) — targeted reading for Goals 2 and 6**
	- **Focus**: Read for the Monte Carlo standard error framework for dependent samples and its relationship to ESS. This extends Geyer’s ESS concept by providing a concrete method for quantifying the uncertainty in a posterior summary that accounts for autocorrelation. Note that the fixed-width stopping rule in Section 4 — the comparison between consistent batch means (CBM) and the Gelman-Rubin diagnostic (GRD) for deciding when to stop a chain — is a direct and distinctive contribution to Goal 6’s iterative workflow; the paper shows concretely when GRD terminates too early. Sections 4.2 and 5 are illustrative rather than technically required, but they make the workflow argument concrete. Short and focused.
	- **Builds toward**: Provides the formal machinery for constructing reliable uncertainty estimates from MCMC output — a practical extension of Goal 1’s ESS framing, with direct relevance to the iterative workflow of Goal 6.
	
6. *Cowles & Carlin (1996)* — MCMC Convergence Diagnostics: A Comparative Review [Secondary]
**JASA 91(434) — targeted reading; read critically**
	- **Focus**: Read as a survey of the diagnostic landscape as of 1996, not as a recipe. The paper compares multiple convergence diagnostics and finds none definitively superior. The takeaway is not a recommended diagnostic but an understanding of what different diagnostics are measuring and where each can be fooled. 
	**Prioritize**: **Sec 2.1** (Gelman-Rubin) and **Sec 2.3** (Geweke) are the diagnostics with ongoing practical relevance; read these in detail.
	  > The remaining diagnostics require problem-specific coding and are rarely used in practice — read them for the framework (what does each try to detect? what does it miss?) without memorizing their mechanics. Table 1 (p. 890) is the clearest single summary of all diagnostics; return to it throughout. **Secs 3.2** and **4.2** show comparative failure modes — read at least the trivariate normal (**Sec 3.2**) and bimodal mixture (**Sec 4.2**) comparative remarks.
	  
	  **Section 5** is the practical conclusion; read in full. Note that Section 5’s recommendation — use a combination of strategies rather than any single diagnostic — remains the correct modern position and anticipates the Stan/BDA workflow.
	- **Builds toward**: Reading critically means asking: what failure mode does each diagnostic detect, and what failure mode does it miss? This is the right question to bring to any convergence diagnostic.
	
7. *Link & Eaton (2012) — On Thinning of Chains in MCMC* [Secondary]
**Methods in Ecology and Evolution 3(1) — short paper, read in full**
	- **Focus**: Read for the single result: thinning MCMC chains (keeping every kth sample) does not improve statistical efficiency relative to keeping all samples. Keeping all samples always produces higher or equal ESS for the same computational cost. Thinning may be justified on storage grounds but not on inferential ones. Note that Geyer (1992), Sec 3.6, Theorem 3.3 proves the same fundamental result analytically: for a reversible irreducible Markov chain, any subsampling strictly inflates variance. Link & Eaton restates this for a practitioner audience and quantifies it concretely for the two-state case. Reading both together reinforces Goal 5 from complementary angles.
	- **Builds toward**: Goal 5 asks you to explain this result and identify the narrow circumstances where thinning may be practically justified. This paper is the sole source for that goal.
Secondary depth: Robert & Casella (2004), Ch 6 (Markov chains). For students who want the measure-theoretic underpinning of MCMC convergence. R&C Ch 6 is more demanding than LPW — it works from Meyn & Tweedie and uses Harris recurrence, atoms, and drift conditions throughout — but every concept is framed explicitly in terms of MCMC algorithms. Sec 6.1 is a concise survey of key results in accessible language; Sec 6.7.1 (Ergodic Theorems) is the section most directly relevant to Goal 1 — it is where the ergodic theorem connects chain convergence to the validity of MCMC time averages. Not required; consult if the LPW treatment of convergence felt disconnected from MCMC in practice.

### Self-Assessment
#### Quick Checklist
After finishing the reading, can you:
- Explain effective sample size as the central measure of MCMC output quality, distinguishing it from raw sample count and connecting it to autocorrelation?
- Compute and interpret autocorrelation function estimates from MCMC output and explain what high autocorrelation implies for reliability?
- Apply trace plots, R-hat, and ESS as principled diagnostics — explaining what each measures and what it can and cannot detect?
- Explain warm-up and its role in allowing the chain to reach the typical set, and distinguish samples that should and should not be retained?
  *(Note: The “typical set” refers to the region of high posterior probability where the chain must reside before warm-up samples are discarded. This terminology comes from the HMC literature; in the sources assigned here it appears as “reaching stationarity” or “escaping the influence of starting values” in BDA, and “the run being long enough” in Geyer.)*
- Explain why thinning does not improve statistical efficiency and identify the narrow circumstances where it may be practically justified?
- Describe a reliable iterative workflow for running a sampler, evaluating its output, and deciding whether to trust results or return to the sampler?

#### Conceptual Questions
41.	Effective sample size is smaller than the raw number of MCMC draws whenever the chain is autocorrelated. Explain the mechanism: why does autocorrelation reduce the information content of each additional draw?
42.	R-hat diagnoses convergence by comparing within-chain to between-chain variance across multiple chains. What does a high R-hat value indicate? What does a low R-hat value guarantee? Is a low R-hat sufficient to conclude the chain has converged?
43.	Trace plots are often the first diagnostic a practitioner examines. What are you looking for in a trace plot, and what failure modes can a trace plot detect? What failure modes can it miss?
44.	Link & Eaton (2012) show that thinning does not improve statistical efficiency. Given that, why do many practitioners continue to thin? Evaluate the common justifications for thinning in light of the paper’s result.
45.	Warm-up samples are discarded. What is the conceptual justification? What determines how many warm-up samples to discard, and what happens if you discard too few?
 
## Module 9 — Density Estimation
**High-level goal**: Estimate distributions nonparametrically from data and from MCMC output, understand the bias-variance tradeoffs governing each method, and apply density estimation as a practical tool for interpreting posterior and predictive distributions.
 
### Reading Sequence
*Silverman* is the primary text for Chs 2, 3, and 5 (Sec 5.2). The two items from *Givens & Hoeting* are targeted and should be consulted for the specific goals they address. Read Silverman Chs 2 and 3 first before consulting any secondary source. Note that Silverman Ch 3 covers both the kernel estimator and bandwidth selection in the same chapter (Secs 3.2–3.4) — items 2 and 3 below both draw from Ch 3.
 
1. *Silverman (1986) — Density Estimation for Statistics and Data Analysis* [Primary]
**Ch 2: Histograms and naive estimators (context for the density estimation problem)**
	- **Focus**: Use Ch 2 to establish the density estimation problem from first principles: what does it mean to estimate a density, why parametric models are sometimes insufficient, and how the naive estimator fails. The histogram discussion is not an aside — it makes the bias-variance tradeoff concrete before the kernel estimator appears.
	- **Builds toward**: The histogram’s limitation — sensitivity to bin placement and width — is precisely the problem the kernel estimator addresses.

2. *Silverman (1986) — Density Estimation for Statistics and Data Analysis* [Primary]
**Ch 3, Secs 3.2–3.3: The kernel estimator and bias-variance analysis**
	- **Focus**: This is the conceptual core of the module. Focus on what the kernel does (smooth the contribution of each observation to the density estimate), what the bandwidth does (control the degree of smoothing), and how the choice of kernel matters far less than the choice of bandwidth. The Gaussian kernel is conventional; the bandwidth is where most practical decisions happen. Secs 3.2 and 3.3 develop the full MISE analysis and the bias-variance decomposition — read these carefully, as they provide the theoretical grounding for the bandwidth selection rules in Sec 3.4 (item 3 below).
		****> Note: Ch 4 covers the kernel method for multivariate data and is outside this module’s scope.
	- **Builds toward**: The bias-variance framework developed here in Secs 3.2–3.3 is the foundation for the principled bandwidth selection rules developed in Sec 3.4 (item 3).
	
3. *Silverman (1986) — Density Estimation for Statistics and Data Analysis* [Primary]
**Ch 3, Sec 3.4: Bandwidth selection**
	- **Focus**: Continue within Ch 3 from items 1–2. Sec 3.4 is the full bandwidth selection treatment: subjective choice, reference to a standard distribution (the rule-of-thumb), least-squares cross-validation, and likelihood cross-validation. Focus on why bandwidth selection is a bias-variance problem: small bandwidth → low bias, high variance; large bandwidth → high bias, low variance. For each selector in Sec 3.4, ask what assumptions it makes and when it would fail. The rule-of-thumb is fast but assumes approximately Gaussian data; cross-validation selectors are more adaptive but more variable in finite samples.
	- **Builds toward**: Principled bandwidth selection is what distinguishes a reliable density estimate from an arbitrary one — this material is what Goal 3 requires.
	
4. *Givens & Hoeting (2013) — Computational Statistics, 2nd ed.* [Secondary]
**Ch 6, Sec 6.4.4: Rao-Blackwellization for density estimation in MCMC settings**
	- **Focus**: Read as a targeted extension of the Rao-Blackwell material from Module 2. G&H Sec 6.4.4 develops the general principle — that conditioning on available structure reduces variance without changing what you are estimating (Eq. 6.81 via the conditional variance formula) — and then applies it in a Monte Carlo estimation context. The connection to density estimation specifically runs through the following link: Gibbs samplers produce full conditional distributions as a byproduct at every step, and averaging over those conditionals to estimate a posterior density yields a lower-variance estimate than using the marginal samples alone. Keep that density-estimation application explicitly in view while reading the general variance-reduction derivation in Sec 6.4.4. Goal 4 asks why this strategy is particularly well-suited to MCMC settings.
	- **Builds toward**: This reading connects directly back to Module 2’s Rao-Blackwellization material and forward to Module 10’s posterior predictive check workflow.
	
5. *Silverman (1986) — Density Estimation for Statistics and Data Analysis* [Primary (for Goal 5)]
**Ch 5, Sec 5.2: The nearest-neighbour estimator**
	- **Focus**: Sec 5.1 frames the chapter — read it as a brief introduction situating nearest-neighbour and adaptive methods as responses to the kernel estimator’s limitations in sparse regions. Sec 5.2 is the core: the definition of the nearest-neighbour estimator (Eq. 5.1), the formal bias-variance expressions (Eqs. 5.4–5.5), and the explicit comparison with the kernel estimator at the same point (Eq. 5.6). Focus on the bias-variance contrast that Goal 5 specifically asks for: in nearest-neighbour estimation, the local bandwidth adapts to data density, giving different behavior in sparse and dense regions than a fixed-bandwidth kernel. The comparison in Sec 5.2 shows where nearest-neighbour overcorrects. 
		> **Sec 5.3 (adaptive kernel estimates)** is optional depth — read if you want to see how the chapter’s logic leads to a hybrid approach that blends kernel and nearest-neighbour ideas.
		> **Sec 5.4 (maximum penalized likelihood)** is outside this module’s scope.
	- **Builds toward**: The local vs. global bandwidth distinction is a principled algorithmic choice with predictable consequences — understanding it completes the module’s coverage of the density estimation design space.

6. *Givens & Hoeting (2013) — Computational Statistics, 2nd ed.* [Secondary (for Goal 5)]
**Ch 10, Sec 10.4.3.1: Nearest-neighbour density estimation**
	- **Focus**: Read after Silverman Sec 5.2 as confirmatory depth. G&H provides a more applied treatment of the same nearest-neighbour material with worked examples and practical guidance. Goal 5 is met by Silverman; G&H reinforces it.
	- **Builds toward**: Together with Silverman Sec 5.2, this reading ensures both the formal bias-variance analysis and the practical implementation perspective are covered for Goal 5.

### Self-Assessment
#### Quick Checklist
After finishing the reading, can you:
- Articulate the density estimation problem — what it means to estimate a distribution nonparametrically and why point estimates and parametric models are sometimes insufficient?
- Implement kernel density estimation, explain the role of kernel and bandwidth, and characterize the bias-variance tradeoff that bandwidth selection governs?
- Apply at least one principled bandwidth selection method and explain the consequences of under- and over-smoothing?
- Explain the Rao-Blackwell estimator as a variance-reduction strategy for density estimation and identify why it is well-suited to MCMC settings?
- Implement nearest-neighbor density estimation and contrast its bias-variance characteristics with KDE?
- Interpret density estimates critically, recognizing what each method implicitly assumes and how those assumptions affect the estimate?

#### Conceptual Questions
46.	The kernel estimator places a smooth kernel at each observation and sums. What determines the shape of the resulting estimate? Why does the choice of kernel matter much less than the choice of bandwidth?
47.	Bandwidth selection is a bias-variance problem. Describe the tradeoff precisely: what does a small bandwidth optimize, what does a large bandwidth optimize, and what does the optimal bandwidth balance?
48.	Silverman’s rule-of-thumb bandwidth assumes the data are approximately Gaussian. When is this assumption dangerous, and what would you use instead?
49. *The Rao-Blackwell theorem says that conditioning on available structure can only reduce the variance of an unbiased estimator. How does this idea translate into a practical variance reduction strategy for Monte Carlo estimators? What does "conditioning" mean in this context, and what determines whether it is feasible to apply?*
50.	The Rao-Blackwell estimator for posterior densities averages over full conditionals available from a Gibbs sampler. Why does conditioning on additional information reduce variance? And why is this information only available in certain sampler architectures?
51.	Nearest-neighbor estimation uses a local bandwidth — the bandwidth at each point is determined by the local data density. What is the consequence in sparse regions? In dense regions? How does this compare to the behavior of a fixed-bandwidth kernel estimator in the same regions?
 
## Module 10 — Applied Cases
**High-level goal**: Integrate the program’s methods into coherent, reproducible analyses of realistic problems, developing the workflow judgment that distinguishes competent method application from genuine computational statistical practice.
 
### Reading Sequence
Module 10 is primarily a doing module rather than a reading module. The readings below are short synthesis pieces and a targeted BDA section. They should be read alongside applied work, not in a single sitting before starting.
 
1. *Gelman et al. (2013) — Bayesian Data Analysis, 3rd ed.* [Primary]
**Ch 6: Model checking — prior predictive, posterior predictive, and graphical checks**
	- **Focus**: This chapter introduces the posterior predictive check as a principled model criticism tool. Focus on what a posterior predictive check tests (whether the model can reproduce features of the observed data) and what a failure implies (the model is misspecified in some detectable way). Also important: what a passing check does not imply.
	- **Builds toward**: Goal 4 asks you to demonstrate a posterior predictive check — this chapter is the source. Return to it when you conduct one in an applied case.
2. *Efron & Hastie (2016) — Computer Age Statistical Inference* [Primary]
**Epilogue: A short timeline from 1900 to 2016 tracing statistical progress**
	- **Focus**: Read as a disciplinary retrospective, not for new technical content. The Epilogue traces the movement of statistical progress between Applications, Mathematics, and Computation across the twentieth century. It closes the frame opened by Tukey (1962) in Module 0. Note: the Epilogue is short and is the correct synthesis reading — Chs 16–18 cover Lasso and neural networks and are not retrospectives.
	- **Builds toward**: Goal 6 asks you to situate the program’s methods within the broader arc of modern statistical practice. This reading, paired with Gelman & Vehtari (2021), is what makes that situating possible.
3. *Gelman & Vehtari (2021)* — What Are the Most Important Statistical Ideas of the Past 50 Years? [Primary]
**JASA 116(536) — read in full**
	- **Focus**: Read as a second disciplinary retrospective, paired with the Efron & Hastie Epilogue. Gelman & Vehtari cover ideas rather than history — their list includes counterfactual causal inference, regularization, Bayesian computation, and multilevel modeling. Assess which of these ideas you have encountered in the program and which remain outside it.
	- **Builds toward**: This reading closes the frame opened by Tukey (1962) in Module 0 — ask yourself whether Tukey’s call for a reformation of statistics has been answered, and if so, by what.

**Optional**: *Donoho (2017)*, ‘50 years of data science,’ Journal of Computational and Graphical Statistics 26(4). Opens explicitly with Tukey (1962) and traces the subsequent data science debate. A second perspective alongside Gelman & Vehtari for Goal 6. Freely available online.

### Applied Cases: Guidance
Each applied case should integrate tools from multiple modules. A well-designed case requires you to:
- State a clear inferential question and justify the choice of estimation method
- Construct and fit a model, implementing at least one simulation-based method (bootstrap or MCMC) with documented diagnostics
- Include at least one model check (posterior predictive or otherwise) and explain what it tests and what it cannot detect
- Report conclusions with honest uncertainty quantification, including a discussion of where the method could fail
The goal is judgment, not coverage. A case that deploys one method thoughtfully is more valuable than one that deploys five methods superficially.

### Self-Assessment
#### Quick Checklist
After completing Module 10, can you:
- Select and justify appropriate methods for each component of a multi-part applied problem?
- Construct, fit, and diagnose a Bayesian model end-to-end — from prior specification through MCMC sampling, diagnostic evaluation, and interpretation of posterior output?
- Apply bootstrap inference as a validation or subsidiary analysis tool within a larger workflow, and recognize when its assumptions are stressed?
- Demonstrate a posterior predictive check as a model criticism tool — explaining what it tests, what a failure implies, and what it cannot detect?
- Produce a complete analysis that is reproducible, honestly reported, and explicit about the assumptions and limitations of every methodological choice?
- Situate the program’s methods within the broader arc of modern statistical practice using Efron & Hastie (Epilogue) and Gelman & Vehtari (2021)?

#### Conceptual Questions
52.	Tukey (1962) argued for a reformation of statistics toward data analysis. Looking back at the program, which methods most directly embody Tukey’s argument? Which remain more ‘mathematical statistics’ in his sense?
53.	Gelman & Vehtari (2021) list several ideas they consider most important in the past 50 years. Which of these ideas does this program cover? Which does it not cover, and why might those omissions be defensible at this scope?
54.	A posterior predictive check shows that your model cannot reproduce a key feature of the data. What are your options, and what does each option commit you to?
55.	The program treats the bootstrap and MCMC as conceptually related: both are simulation-based inference methods. What do they share, and where does the analogy break down?
56.	In Efron & Hastie’s retrospective, statistics moves between Applications, Mathematics, and Computation across the twentieth century. Where would you locate the program’s methods on that map, and does that location feel right to you?
 








