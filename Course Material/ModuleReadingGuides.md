# Module Reading Guides

*This document is in the process of being split: it holds the theory component of all modules not yet split into their own units.*

## Module 5 — Bayesian Modeling Framework

*\<Introduction block\>*

### Reading Sequence
All readings come from *Gelman et al. (BDA)*. The module is self-contained within that text. Read in order — earlier chapters build the modeling vocabulary that later chapters require.

1. *Gelman et al. (2013) — Bayesian Data Analysis, 3rd ed.*\
	Read both chapters 1 and 2 in full.

	***Ch 1: Probability and inference***

	- **Focus**: Establish the Bayesian model structure: the joint distribution, likelihood, prior, and posterior, and what each component commits you to. This chapter's probability framework is used throughout the program — make sure the notation and the interpretive conventions are solid before proceeding.
	- **Builds toward**: This chapter's framework is what Module 7 will use when constructing a posterior to sample from.

	***Ch 2: Single-parameter models***

	- **Focus**: Use single-parameter models to develop the intuition for prior-to-posterior updating, conjugacy, and what prior choice implies for the posterior. The arithmetic here is simple enough that you can trace every step; the conceptual content is what matters. 
	**§2.8** and **§2.9** are the chapter's most direct material for Goal 5.2: read them as a treatment of prior selection as a modeling choice with traceable consequences, not as an aside on a special case. The same sections are the primary basis for Goal 5.4's prior-sensitivity component — §2.8 in particular makes explicit how disputing a posterior conclusion amounts to a claim about missing prior or likelihood information.
	- **Builds toward**: The prior sensitivity reasoning developed here is revisited and extended in Ch 5, where the same questions are posed for hierarchical variance parameters.

2. *Gelman et al. (2013) — Bayesian Data Analysis, 3rd ed.*\
***Ch 3 (Selected sections): Multiparameter models***\
**§3.1** and the opening of **§3.2** (through the statement of the joint posterior) are the required reading.\
**§3.3–§3.8** are reference — skim for the structural pattern, not the algebra.\
**§3.9** can be skipped.

	- **Focus:** The chapter's central lesson for this module is that marginalization is the general operation for moving from a joint posterior to inference about a single parameter, and that this operation resists closed-form solution as soon as the model leaves the conjugate family.\
	**§3.1** establishes why marginalization is necessary. **§3.2**'s opening shows what the joint posterior looks like in a concrete case. The conjugate examples that follow (§3.3 onward) are additional instances of the same pattern — glance at them to confirm the pattern holds, but do not work through the derivations. The bioassay example in §3.7 is the chapter's clearest illustration of the nonconjugate case, where even a simple two-parameter model requires numerical methods; it's worth a skim if the motivation for computational methods feels abstract.

	- **Builds toward**: Multiparameter posterior structure is what makes closed-form computation impossible in general — motivating the need for the sampling methods in Modules 7–8.

3. *Gelman et al. (2013) — Bayesian Data Analysis, 3rd ed.*\
	***Ch 5 (selected sections): Hierarchical models***\
	**§5.1–§5.2**, **§5.5** and **§5.7** are required. **§5.3–§5.4** are reference — read for what they illustrate about the problem's structure, not for the computational machinery. **§5.6** can be skipped.

	- **Focus**: The chapter's central argument for this module runs through three steps: exchangeability as the modeling assumption that makes hierarchical structure the natural choice (§5.1–§5.2); partial pooling as the consequence of that structure, and what it implies about information flow across groups (§5.5, eight-schools example); and prior sensitivity on the variance parameters as the place where the modeling layer's choices have the most visible consequences (§5.7). §5.3–§5.4 work out the conjugate hierarchical case in detail — they are worth reading to see why the marginal posterior of the hyperparameters has the form it does, and why complete pooling and no pooling are limiting cases of the same model, but the integration and simulation steps they develop are outside this module's scope by design.
	- **Builds toward**: Hierarchical models are the canonical setting where MCMC becomes necessary, making this reading a bridge to Module 7.

### Self-Assessment
#### Quick Checklist
After finishing the reading, can you:
- Specify a Bayesian model as a computational object — joint distribution, likelihood, prior, and posterior — and articulate what each component commits you to? (Goal 5.1)
- Given a choice among informative, weakly informative, and vague priors, justify it by its verifiable consequences for the posterior, rather than treating the choice as arbitrary or a defensive hedge? (Goal 5.2)
- Identify the structural patterns in multiparameter and hierarchical models and explain what hierarchical structure implies computationally? (Goal 5.3)
- Criticize a Bayesian model by interrogating prior sensitivity, likelihood misspecification, and predictive adequacy — independently of how the model will be fit? (Goal 5.4)
- Maintain a clear separation between modeling questions (what is the right prior? is the likelihood appropriate?) and computational questions (how do I sample the posterior?)? (Goal 5.5)

#### Conceptual Questions
1.	A Bayesian model specifies a joint distribution over data and parameters. What does this specification assume, and what work does the prior do within that specification? Is the prior subjective? (Goal 5.1)
2.	Prior sensitivity analysis tests whether the posterior changes substantially when the prior changes. What would a large change in the posterior imply about your model? What would a small change imply? When is sensitivity analysis required and when can it be skipped? (Goal 5.4)
3.	Hierarchical models pool information across groups. What is the computational cost of that pooling? Why does it make closed-form posterior computation generally impossible? (Goal 5.3)
4.	This module deliberately separates modeling from computation. Why is that separation useful? What goes wrong if you think about the two together? (Goal 5.5)
5.	*BDA Ch 11 (Basics of Markov chain simulation)* is the conceptual follow-up to this module, and is assigned in Module 7. What question would you expect that chapter to answer that this module does not? (Goal 5.5)
*Note: This question deliberately asks you to reason about a chapter you have not yet read. You are not expected to know what BDA Ch 11 contains — you are expected to reason from what Module 5 does cover: what modeling questions it settles, and what questions it leaves open. The answer you construct here will be tested against the actual Ch 11 content when you reach Module 7.*

## Module 6 — Markov Chains as Computational Objects

*\<Introduction block\>*

### Reading Sequence
Begin with the concrete example (LPW Ch 3) before formalizing anything. The module is designed to move from observation to theory: watch a chain run on a simple target, then read the formal properties as an explanation of what you observed.

1. *Levin, Peres & Wilmer (2009) — Markov Chains and Mixing Times*\
**Ch 3: Metropolis and Glauber chains** — read as a concrete entry point before the formal theory
	- **Focus**: Before reading any formal definitions, observe what a Markov chain on a simple target actually does. Ch 3 gives you a concrete example. Watch the chain mix (or fail to). Identify mixing and stationarity as empirical phenomena. Then proceed to the formal theory with those observations in mind.
		> **Note**: Ch 3 introduces some formal notation and terminology (transition kernels, stationarity conditions) before those concepts are developed in Ch 1 — hold them lightly on first pass and let Ch 1 supply the grounding retroactively. The Ising model figure (Figure 3.2, low/critical/high temperature configurations) is the clearest observational content in the chapter — give it close attention even as you move more quickly through the surrounding derivations.
		
	- **Builds toward**: The empirical phenomena you observe here are exactly what Goal 6.1 asks you to identify before formalizing — and they are what the formal theory in Ch 1 explains.

2. *Levin, Peres & Wilmer (2009) — Markov Chains and Mixing Times*\
**Ch 1: Secs
1.1 (Markov chains),
1.3 (irreducibility and aperiodicity),
	1.5 (stationary distributions),
	1.6 (reversibility and time reversals — detailed balance)**
	> **Skip**: **§1.2** **(Random Mapping Representation)** and **1.4 (Random Walks on Graphs)** fall between the assigned sections but are not required for any goal in this module — skip them.
	- **Focus**: This is the core formal theory. For each property (irreducibility, aperiodicity, stationarity, detailed balance), connect it back to what you observed in Ch 3: what does this property guarantee about long-run behavior, and what failure does its absence produce? Detailed balance is the most important concept here — it is the condition that MCMC algorithms are designed to satisfy.
	- **Builds toward**: Detailed balance from this chapter is the condition that Module 7 will use to derive the Metropolis-Hastings acceptance ratio.

3. *Levin, Peres & Wilmer (2009) — Markov Chains and Mixing Times*\
**Ch 4: Introduction to Markov Chain Mixing — total variation distance, convergence theorem, mixing time**
	- **Focus**: Focus on mixing time as an operational concept: how many steps does it take for the chain to be close to stationarity, and what determines that number? Total variation distance is the measure — understand what it is measuring and why it is the right quantity. The coupling characterization of total variation distance (Proposition 4.7, Figure 4.2) is worth sitting with: it gives a second, more intuitive way to see what the distance is measuring beyond the formal definition.
	- **Builds toward**: Mixing time is the bridge from formal theory to practical consequences: a chain with slow mixing produces correlated output, which is what Module 8's ESS diagnostic measures.

4. *Levin, Peres & Wilmer (2009) — Markov Chains and Mixing Times*\
**Ch 12: §12.1–12.2 (spectral representation, relaxation time, spectral gap);
§12.3.1 (the n-cycle example only);
§12.7 (Time Averages)**
	> **Skip: §12.3.2 through §12.6** (lumped chains and the path, product chains, the spectral formula for target time, and the ℓ² bound) are not required for this module's goals. This is substantial material — roughly two-thirds of the chapter — and skipping it is intentional, not a shortcut: these sections develop machinery for problems outside this module's scope (card shuffling, Glauber dynamics spectral gaps for product measures, hitting times). §12.7 picks up directly after §12.3.1 in relevance, even though several chapter sections fall between them.
	- **Focus**: **§12.1–12.2** develop the spectral representation of a reversible chain and define the absolute spectral gap, the spectral gap, and the relaxation time — and give the key operational inequality showing that variance decays at a rate governed by the gap. **§12.3.1 (the n-cycle)** is the chapter's clearest source of geometric intuition: the eigenvalues are literally cosines of angles around the cycle, and seeing the spectral gap shrink as O(n⁻²) for a long cycle is what makes "small spectral gap means slow mixing" concrete rather than abstract. Then **§12.7 (Time Averages)** connects the spectral gap directly to a practical question: how many MCMC samples do you need to estimate a posterior expectation to a given accuracy? Theorem 12.21 answers this in terms of γ⁻¹ — note that this is the same spectral gap defined in §12.2, so keep that definition in view when reading §12.7.
	- **Builds toward**: The spectral gap concept provides the theoretical vocabulary for diagnosing why a sampler is performing poorly — a vocabulary that becomes practically relevant in Module 8. The §12.7 result is the direct, quantitative version of that connection: it is what Goal 5 asks you to explain.

### Self-Assessment
#### Quick Checklist
After finishing the reading, can you:
- Describe a concrete Markov chain mixing on a simple target, and identify mixing, stationarity, and failure to converge as empirical phenomena? (Goal 6.1)
- Define irreducibility, aperiodicity, and stationarity and explain what each guarantees about long-run behavior? (Goal 6.2)
- Explain detailed balance as a sufficient condition for stationarity and state why it is the condition MCMC algorithms are designed to satisfy? (Goal 6.3)
- Define mixing time and the spectral gap as measures of convergence speed and develop geometric intuition for why some chains mix slowly? (Goal 6.4)
- Connect poor mixing to downstream consequences for MCMC output quality — explaining what slow mixing implies for estimates derived from sampler output? (Goal 6.5)

#### Conceptual Questions
1.	Irreducibility, aperiodicity, and detailed balance are all conditions a Markov chain can satisfy. What does each condition guarantee individually, and what do they guarantee together? (Goal 6.2)
2.	Detailed balance is described as a sufficient condition for stationarity, not a necessary one. What does that mean? Could you construct a chain that has the right stationary distribution but does not satisfy detailed balance? (Goal 6.3)
3.	Mixing time measures how long it takes a chain to get close to stationarity. "Close" is measured in total variation distance. Why is total variation the right distance measure here? What would it mean for a chain to be "not close" to its stationary distribution? (Goal 6.4)
4.	The spectral gap governs mixing speed. What is the relationship between a small spectral gap and slow mixing? Using the n-cycle as a concrete case, explain why a longer cycle has a smaller spectral gap and what that implies for how long the chain takes to mix. (Goal 6.4)
5.	This module argues that understanding Markov chains as dynamical systems is not optional background for MCMC practitioners. Make that argument concretely: what would a student who skipped this module be unable to explain or diagnose? (Goal 6.5)
6.	Theorem 12.21 shows that the number of MCMC samples needed to estimate a posterior expectation to a given accuracy scales with the inverse of the spectral gap. What does this mean in practical terms for a chain that mixes slowly, and why isn't the number of raw samples alone an adequate measure of how much information you have? (Goal 6.5)

## Module 7 — MCMC Methods

*\<Introduction block\>*

### Reading Sequence
Begin with SIR as a conceptual bridge from Module 2's importance sampling to the MCMC setting. Then develop MH and Gibbs as principled solutions to the sampling problem SIR leaves open. The reference sources (Roberts & Rosenthal; VanDerwerken) should be consulted for specific goals, not read in sequence.

1. *Givens & Hoeting (2013) — Computational Statistics, 2nd ed*.\
**Ch 6, §6.3.1: Sampling Importance Resampling (SIR) Algorithm**
	- **Focus**: Read this as the bridge from Module 2. SIR extends the importance sampling idea from computing a single estimate to producing an approximate sample from a target distribution by resampling proportionally to importance weights. Identify exactly where it connects back to Module 2 (Goal 2.6), and why it still requires a good proposal.
	- **Builds toward**: SIR frames the core challenge that motivates MCMC: producing an approximate sample from a complex target when direct sampling is impossible.
	
2. *Gelman et al. (2013) — Bayesian Data Analysis, 3rd ed.* [Reference]\
**Ch 10, §10.4: Importance sampling as background context for SIR**
	> [Optional]
	- **Focus**: If the connection between importance sampling and SIR is not clear after Givens & Hoeting, this section provides additional framing from a Bayesian computation perspective. Not required if Givens & Hoeting was sufficient.
	- **Builds toward**: This reading reinforces the Module 2 connection and situates SIR within the Bayesian computation workflow.
	
3. *Robert & Casella (2004) — Monte Carlo Statistical Methods, 2nd ed.*\
**Ch 7: Metropolis-Hastings — derivation, variants, practical choices**
	- **Focus**: Focus on the derivation from detailed balance: understand why the acceptance ratio takes the form it does, and what happens to the chain's stationary distribution if you change it. Then focus on the proposal distribution problem: how does proposal width affect acceptance rate and autocorrelation, and why is there a tradeoff?
	- **Builds toward**: The acceptance ratio derivation here connects directly back to Module 6's detailed balance condition — MH is the algorithm designed to satisfy that condition for an arbitrary target.
	
4. *Gelman et al. (2013) — Bayesian Data Analysis, 3rd ed.*\
**Ch 11: Basics of Markov chain simulation (now introduced with full context)**
	- **Focus**: Read this after R&C Ch 7. BDA Ch 11 provides the Bayesian practitioner's perspective on the same methods — the emphasis is on how to think about the sampler as a tool for posterior inference rather than as a generic algorithm. Focus on **§11.1–§11.3**, which connect the sampling algorithms to the Bayesian modeling framework built in Module 5. In particular, §11.3 ("Using Gibbs and Metropolis as building blocks") is the primary source for Goal 7.6: it introduces Metropolis-within-Gibbs as the answer to the question that R&C Chs 9–10 leave open — what do you do when a full conditional is not tractable?
	  > **Read §11.3 after finishing R&C Chs 9–10, not before**.
	
	  > **§11.4–§11.5** (convergence monitoring and ESS) can be read for orientation here, but will be revisited as primary content in Module 8 alongside Geyer (1992), where they belong in the diagnostic workflow. Deep engagement with those sections should wait.
	- **Builds toward**: BDA Ch 11 connects the algorithmic machinery to the Bayesian modeling framework from Module 5 — this is where the two threads meet.
	
5. *Robert & Casella (2004) — Monte Carlo Statistical Methods, 2nd ed.*\
**Chs 9–10: The Two-Stage and Multi-Stage Gibbs Sampler — structure, conditional specification, blocking**
	- **Focus**: Focus on why full conditional distributions guarantee acceptance at every step (the derivation from detailed balance), and on the distinction between random-scan and deterministic-scan Gibbs. The blocking discussion is practically important — understand how block structure affects mixing.
	- **Builds toward**: The deterministic-scan Gibbs subtlety addressed in VanDerwerken (below) is the most common conceptual confusion about Gibbs samplers — keep it in mind while reading R&C's treatment. Also note: because Gibbs sampling produces full conditional distributions as a byproduct at every step, it creates an opportunity for variance-reduced density estimation that other samplers do not; this is the basis for the Rao-Blackwellization technique covered in Module 9.
	
6. *Roberts & Rosenthal (2001) — Optimal Scaling for Various Metropolis-Hastings Algorithms* [Reference]\
**Statistical Science 16(4) — targeted reading for Goal 7.3**
	- **Focus**: Read for the acceptance rate target result: the theoretical result that optimal Metropolis-Hastings performance (in certain settings) corresponds to an acceptance rate of approximately 0.234 for random walk proposals in high dimensions. Understand what this result gives you and what it does not: it is a guideline, not a formula.
	- **Builds toward**: The proposal scaling result provides a theoretical anchor for the practical advice — “tune your acceptance rate” — that Module 8 will revisit in the diagnostic workflow.
	
7. *VanDerwerken (2017) — Not Every Gibbs Sampler is a Special Case of the MH Algorithm* [Reference]\
**Communications in Statistics — Theory and Methods 46(20) — targeted reading for 7.5**
	- **Focus**: Short paper. Read for the single result: deterministic-scan Gibbs does not satisfy detailed balance in general, and therefore cannot be understood as a special case of MH. The random-scan version can. Understand why this distinction matters for how you reason about the chain's stationary distribution.
	- **Builds toward**: This result is what Goal 7.5 asks you to articulate. Without it, the deterministic-scan / random-scan distinction seems like a technical footnote; with it, it is a conceptual clarification about what the algorithm is actually doing.

### Self-Assessment
#### Quick Checklist
After finishing the reading, can you:
- Explain SIR as a bridge from importance sampling to approximate sampling, tracing the connection back to Module 2 and framing the central challenge that MCMC addresses? (Goal 7.1)
- Derive the Metropolis-Hastings acceptance ratio from the detailed balance condition and explain what it enforces? (Goal 7.2)
- Characterize how proposal distribution choice governs the acceptance rate / autocorrelation tradeoff in MH? (Goal 7.3)
- Derive Gibbs sampling from full conditional distributions and explain why acceptance is guaranteed at every step? (Goal 7.4)
- Distinguish random-scan from deterministic-scan Gibbs and explain why the deterministic-scan version does not satisfy detailed balance in general? (Goal 7.5)
- Implement Metropolis-within-Gibbs and identify when this hybrid is warranted? (Goal 7.6)
- Describe SIR, MH, and Gibbs as three members of a common family of approximate sampling strategies, each solving the same core problem by different design choices? (Goal 7.7)

#### Conceptual Questions
1.	SIR produces an approximate sample from a target distribution by resampling from importance weights. What limits its accuracy, and why does naive SIR fail in high dimensions? What problem does MCMC solve that SIR does not? (Goal 7.1)
2.	The Metropolis-Hastings acceptance ratio ensures the chain has the correct stationary distribution. Explain the mechanism: what would happen to the stationary distribution if you changed the ratio? (Goal 7.2)
3.	A narrow proposal distribution in MH produces high acceptance rates but strongly autocorrelated samples. A wide proposal produces frequent rejections and similarly slow exploration. What is being traded off, and is there a principled way to resolve the tradeoff? (Goal 7.3)
4.	Gibbs sampling is sometimes described as “MH with acceptance probability 1.” VanDerwerken (2017) shows this is only true for the random-scan version. What is the substantive difference between random-scan and deterministic-scan Gibbs, and why does it matter for the chain's theoretical properties? (Goal 7.5)
5.	Metropolis-within-Gibbs combines MH steps for some parameters with Gibbs steps for others. When is this warranted, and what does it require about the model structure? (Goal 7.6)

## Module 8 — MCMC Diagnostics & Reliability

*\<Introduction block\>*

### Reading Sequence
*Geyer (1992)* and *BDA* Ch 11 are the two primary sources and should be read in tandem — Geyer provides the theoretical grounding for ESS and autocorrelation, BDA provides the applied diagnostic workflow. Stan Reference Manual is the practical reference throughout. Secondary sources (Flegal et al., Cowles & Carlin, Link & Eaton) are targeted — consult them for specific goals.

1. *Geyer (1992) — Practical Markov Chain Monte Carlo*\
**Statistical Science 7(4) — read in full**
	> **Note**: The published version of this paper appeared in Statistical Science 7(4), which included discussion and commentary pieces by other authors. Read only Geyer's article (pp. 473–483); the additional comments in the document are from other contributors and are not assigned.
	- **Focus**: This is the foundational treatment of ESS, autocorrelation, and the ergodic theorem for MCMC. Focus on why effective sample size is different from the raw number of iterations, how autocorrelation determines the size of that difference, and what the ergodic theorem actually guarantees about the validity of MCMC time averages. Read alongside the Module 6 ergodic theorem material (LPW Ch 12, §12.7).
	- **Builds toward**: Geyer's ESS definition is what Goal 8.1 asks you to explain; his autocorrelation treatment is what Goal 8.2 requires.
	
2. *Gelman et al. (2013) — Bayesian Data Analysis, 3rd ed.*\
**Ch 11: Basics of Markov chain simulation — convergence diagnostics, R-hat, trace plots, warm-up, and ESS**
	- **Focus**: Read alongside Geyer. Focus on **§11.4–§11.5**. §11.4 translates the theoretical concepts into an applied diagnostic workflow: how to use trace plots to identify mixing problems, how R-hat diagnoses between-chain versus within-chain variance, and what warm-up is doing. §11.5 develops the effective number of simulation draws (n_eff) — the ESS formula, the variogram-based autocorrelation estimator used to compute it, and the stopping rules (R-hat < 1.1 and n_eff ≥ 5m). Both sections are required; §11.5 is what 8.1 and the stopping-rule component of Goal 8.6 depend on. This is the chapter to return to when running a sampler in practice.

	- **Builds toward**: Goal 8.1 (ESS formula and computation), and the diagnostic workflow that Goal 8.6 asks you to internalize as a reliable iterative practice, not a one-time checklist.
	
3. *Stan Development Team — Stan Reference Manual* [Reference]\
**Section on ESS, R-hat, and warm-up**; https://mc-stan.org/docs/reference-manual
	- **Focus**: Consult as a practical reference throughout. Stan's documentation is the authoritative source for how R-hat and ESS are implemented in practice. Pay particular attention to the bulk ESS / tail ESS distinction and the updated R-hat definition, which correct known issues with older implementations.
	- **Builds toward**: When you deploy a sampler in Module 10 or in practice, this is the reference you will use to interpret the output.
	
4. *Gelman et al. (2013) — Bayesian Data Analysis, 3rd ed.* [Reference]\
**Ch 11: Basics of Markov chain simulation — revisit targeted sections**
	- **Focus**: Return to Ch 11 if needed for clarification on how MCMC output is used for posterior inference. This is supplementary to the Ch 11 convergence diagnostics material covered as primary reading, not an additional assignment. Note: BDA Ch 11 was primary reading in Module 7, where it introduced simulation-based inference with full context. No new reading is expected here — this entry is a pointer back, not an additional assignment.
	- **Builds toward**: Reinforces the connection between the diagnostic questions (is the chain mixing?) and the inferential question (can I trust this posterior summary?).
	
5. *Flegal, Haran & Jones (2008) — Markov Chain Monte Carlo: Can We Trust the Third Significant Figure?*\
**Statistical Science 23(2) — targeted reading for Goals 2 and 6**
	- **Focus**: Read for the Monte Carlo standard error framework for dependent samples and its relationship to ESS. This extends Geyer's ESS concept by providing a concrete method for quantifying the uncertainty in a posterior summary that accounts for autocorrelation. Note that the fixed-width stopping rule in Section 4 — the comparison between consistent batch means (CBM) and the Gelman-Rubin diagnostic (GRD) for deciding when to stop a chain — is a direct and distinctive contribution to 8.6's iterative workflow; the paper shows concretely when GRD terminates too early. Sections 4.2 and 5 are illustrative rather than technically required, but they make the workflow argument concrete. Short and focused.
	- **Builds toward**: Provides the formal machinery for constructing reliable uncertainty estimates from MCMC output — a practical extension of Goal 8.1's ESS framing, with direct relevance to the iterative workflow of Goal 8.6.
	
6. *Cowles & Carlin (1996)* — MCMC Convergence Diagnostics: A Comparative Review\
**JASA 91(434) — targeted reading; read critically**
	- **Focus**: Read as a survey of the diagnostic landscape as of 1996, not as a recipe. The paper compares multiple convergence diagnostics and finds none definitively superior. The takeaway is not a recommended diagnostic but an understanding of what different diagnostics are measuring and where each can be fooled.
	**Prioritize**: **§2.1** (Gelman-Rubin) and **§2.3** (Geweke) are the diagnostics with ongoing practical relevance; read these in detail.
	  > The remaining diagnostics require problem-specific coding and are rarely used in practice — read them for the framework (what does each try to detect? what does it miss?) without memorizing their mechanics. Table 1 (p. 890) is the clearest single summary of all diagnostics; return to it throughout. **§3.2** and **§4.2** show comparative failure modes — read at least the trivariate normal (**§3.2**) and bimodal mixture (**§4.2**) comparative remarks.
	
	  **Section 5** is the practical conclusion; read in full. Note that Section 5's recommendation — use a combination of strategies rather than any single diagnostic — remains the correct modern position and anticipates the Stan/BDA workflow.
	- **Builds toward**: Reading critically means asking: what failure mode does each diagnostic detect, and what failure mode does it miss? This is the right question to bring to any convergence diagnostic.
	
7. *Link & Eaton (2012) — On Thinning of Chains in MCMC*\
**Methods in Ecology and Evolution 3(1) — short paper, read in full**
	- **Focus**: Read for the single result: thinning MCMC chains (keeping every kth sample) does not improve statistical efficiency relative to keeping all samples. Keeping all samples always produces higher or equal ESS for the same computational cost. Thinning may be justified on storage grounds but not on inferential ones. Note that Geyer (1992), §3.6, Theorem 3.3 proves the same fundamental result analytically: for a reversible irreducible Markov chain, any subsampling strictly inflates variance. Link & Eaton restates this for a practitioner audience and quantifies it concretely for the two-state case. Reading both together reinforces Goal 8.5 from complementary angles.
	- **Builds toward**: Goal 8.5 asks you to explain this result and identify the narrow circumstances where thinning may be practically justified. This paper is the sole source for that goal.

**Secondary depth**: Robert & Casella (2004), Ch 6 (Markov chains). For students who want the measure-theoretic underpinning of MCMC convergence. R&C Ch 6 is more demanding than LPW — it works from Meyn & Tweedie and uses Harris recurrence, atoms, and drift conditions throughout — but every concept is framed explicitly in terms of MCMC algorithms. §6.1 is a concise survey of key results in accessible language; §6.7.1 (Ergodic Theorems) is the section most directly relevant to Goal 8.1 — it is where the ergodic theorem connects chain convergence to the validity of MCMC time averages. Not required; consult if the LPW treatment of convergence felt disconnected from MCMC in practice.

### Self-Assessment
#### Quick Checklist
After finishing the reading, can you:
- Explain effective sample size as the central measure of MCMC output quality, distinguishing it from raw sample count and connecting it to autocorrelation? (Goal 8.1)
- Compute and interpret autocorrelation function estimates from MCMC output and explain what high autocorrelation implies for reliability? (Goal 8.2)
- Apply trace plots, R-hat, and ESS as principled diagnostics — explaining what each measures and what it can and cannot detect? (Goal 8.3)
- Explain warm-up and its role in allowing the chain to reach the typical set, and distinguish samples that should and should not be retained? (Goal 8.4)
  *(Note: The “typical set” refers to the region of high posterior probability where the chain must reside before warm-up samples are discarded. This terminology comes from the HMC literature; in the sources assigned here it appears as “reaching stationarity” or “escaping the influence of starting values” in BDA, and “the run being long enough” in Geyer.)*
- Explain why thinning does not improve statistical efficiency and identify the narrow circumstances where it may be practically justified? (Goal 8.5)
- Describe a reliable iterative workflow for running a sampler, evaluating its output, and deciding whether to trust results or return to the sampler? (Goal 8.6)

#### Conceptual Questions
1.	Effective sample size is smaller than the raw number of MCMC draws whenever the chain is autocorrelated. Explain the mechanism: why does autocorrelation reduce the information content of each additional draw? (Goal 8.1)
2.	R-hat diagnoses convergence by comparing within-chain to between-chain variance across multiple chains. What does a high R-hat value indicate? What does a low R-hat value guarantee? Is a low R-hat sufficient to conclude the chain has converged? (Goal 8.3)
3.	Trace plots are often the first diagnostic a practitioner examines. What are you looking for in a trace plot, and what failure modes can a trace plot detect? What failure modes can it miss? (Goal 8.3)
4.	Link & Eaton (2012) show that thinning does not improve statistical efficiency. Given that, why do many practitioners continue to thin? Evaluate the common justifications for thinning in light of the paper's result. (Goal 8.5)
5.	Warm-up samples are discarded. What is the conceptual justification? What determines how many warm-up samples to discard, and what happens if you discard too few? (Goal 8.4)

## Module 9 — Density Estimation

*\<Introduction block\>*

### Reading Sequence
*Silverman* is the primary text for Chs 2, 3, and 5 (§5.2). The two items from *Givens & Hoeting* are targeted and should be consulted for the specific goals they address. Read Silverman Chs 2 and 3 first before consulting any secondary source. Note that Silverman Ch 3 covers both the kernel estimator and bandwidth selection in the same chapter (§3.2–§3.4) — items 2 and 3 below both draw from Ch 3.

1. *Silverman (1986) — Density Estimation for Statistics and Data Analysis*\
**Ch 2: Histograms and naive estimators (context for the density estimation problem)**
	- **Focus**: Use Ch 2 to establish the density estimation problem from first principles: what does it mean to estimate a density, why parametric models are sometimes insufficient, and how the naive estimator fails. The histogram discussion is not an aside — it makes the bias-variance tradeoff concrete before the kernel estimator appears.
	- **Builds toward**: The histogram's limitation — sensitivity to bin placement and width — is precisely the problem the kernel estimator addresses.

2. *Silverman (1986) — Density Estimation for Statistics and Data Analysis*\
**Ch 3, §3.2–§3.3: The kernel estimator and bias-variance analysis**
	- **Focus**: This is the conceptual core of the module. Focus on what the kernel does (smooth the contribution of each observation to the density estimate), what the bandwidth does (control the degree of smoothing), and how the choice of kernel matters far less than the choice of bandwidth. The Gaussian kernel is conventional; the bandwidth is where most practical decisions happen. §3.2 and §3.3 develop the full MISE analysis and the bias-variance decomposition — read these carefully, as they provide the theoretical grounding for the bandwidth selection rules in §3.4 (item 3 below).
		> Note: Ch 4 covers the kernel method for multivariate data and is outside this module's scope.
	- **Builds toward**: The bias-variance framework developed here in §3.2–§3.3 is the foundation for the principled bandwidth selection rules developed in §3.4 (item 3).
	
3. *Silverman (1986) — Density Estimation for Statistics and Data Analysis*\
**Ch 3, §3.4: Bandwidth selection**
	- **Focus**: Continue within Ch 3 from items 1–2. §3.4 is the full bandwidth selection treatment: subjective choice, reference to a standard distribution (the rule-of-thumb), least-squares cross-validation, and likelihood cross-validation. Focus on why bandwidth selection is a bias-variance problem: small bandwidth → low bias, high variance; large bandwidth → high bias, low variance. For each selector in §3.4, ask what assumptions it makes and when it would fail. The rule-of-thumb is fast but assumes approximately Gaussian data; cross-validation selectors are more adaptive but more variable in finite samples.
	- **Builds toward**: Principled bandwidth selection is what distinguishes a reliable density estimate from an arbitrary one — this material is what Goal 9.3 requires.
	
4. *Givens & Hoeting (2013) — Computational Statistics, 2nd ed.*\
**Ch 6, §6.4.4: Rao-Blackwellization for density estimation in MCMC settings**
	- **Focus**: G&H §6.4.4 develops the general principle — that conditioning on available structure reduces variance without changing what you are estimating (Eq. 6.81 via the conditional variance formula) — and then applies it in a Monte Carlo estimation context. The connection to density estimation specifically runs through the following link: Gibbs samplers produce full conditional distributions as a byproduct at every step, and averaging over those conditionals to estimate a posterior density yields a lower-variance estimate than using the marginal samples alone. Keep that density-estimation application explicitly in view while reading the general variance-reduction derivation in §6.4.4. Goal 9.4 asks why this strategy is particularly well-suited to MCMC settings where conditional distributions are already available.
	- **Builds toward**: This reading connects forward to Module 10's posterior predictive check workflow.
	
5. *Silverman (1986) — Density Estimation for Statistics and Data Analysis*\
**Ch 5, §5.2: The nearest-neighbour estimator**
	- **Focus**: §5.1 frames the chapter — read it as a brief introduction situating nearest-neighbour and adaptive methods as responses to the kernel estimator's limitations in sparse regions. §5.2 is the core: the definition of the nearest-neighbour estimator (Eq. 5.1), the formal bias-variance expressions (Eqs. 5.4–5.5), and the explicit comparison with the kernel estimator at the same point (Eq. 5.6). Focus on the bias-variance contrast that Goal 9.5 specifically asks for: in nearest-neighbour estimation, the local bandwidth adapts to data density, giving different behavior in sparse and dense regions than a fixed-bandwidth kernel. The comparison in §5.2 shows where nearest-neighbour overcorrects.
		> **§5.3 (adaptive kernel estimates)** is optional depth — read if you want to see how the chapter's logic leads to a hybrid approach that blends kernel and nearest-neighbour ideas.
		> **§5.4 (maximum penalized likelihood)** is outside this module's scope.
	- **Builds toward**: The local vs. global bandwidth distinction is a principled algorithmic choice with predictable consequences — understanding it completes the module's coverage of the density estimation design space.

6. *Givens & Hoeting (2013) — Computational Statistics, 2nd ed.*\
**Ch 10, §10.4.3.1: Nearest-neighbour density estimation**
	- **Focus**: Read after Silverman §5.2 as confirmatory depth. G&H provides a more applied treatment of the same nearest-neighbour material with worked examples and practical guidance. Goal 9.5 is met by Silverman; G&H reinforces it.
	- **Builds toward**: Together with Silverman §5.2, this reading ensures both the formal bias-variance analysis and the practical implementation perspective are covered for Goal 9.5.

### Self-Assessment
#### Quick Checklist
After finishing the reading, can you:
- Articulate the density estimation problem — what it means to estimate a distribution nonparametrically and why point estimates and parametric models are sometimes insufficient? (Goal 9.1)
- Implement kernel density estimation, explain the role of kernel and bandwidth, and characterize the bias-variance tradeoff that bandwidth selection governs? (Goal 9.2)
- Apply at least one principled bandwidth selection method and explain the consequences of under- and over-smoothing? (Goal 9.3)
- Explain the Rao-Blackwell estimator as a variance-reduction strategy for density estimation and identify why it is particularly well-suited to MCMC settings, where conditional distributions are already available? (Goal 9.4)
- Implement nearest-neighbor density estimation and contrast its bias-variance characteristics with KDE? (Goal 9.5)
- Interpret density estimates critically, recognizing what each method implicitly assumes and how those assumptions affect the estimate? (Goal 9.6)

#### Conceptual Questions
1.	The kernel estimator places a smooth kernel at each observation and sums. What determines the shape of the resulting estimate? Why does the choice of kernel matter much less than the choice of bandwidth? (Goal 9.2)
2.	Bandwidth selection is a bias-variance problem. Describe the tradeoff precisely: what does a small bandwidth optimize, what does a large bandwidth optimize, and what does the optimal bandwidth balance? (Goal 9.2)
3.	Silverman's rule-of-thumb bandwidth assumes the data are approximately Gaussian. When is this assumption dangerous, and what would you use instead? (Goal 9.3)
4. The Rao-Blackwell theorem says that conditioning on available structure can only reduce the variance of an unbiased estimator. How does this idea translate into a practical variance reduction strategy for Monte Carlo estimators? What does "conditioning" mean in this context, and what determines whether it is feasible to apply? (Goal 9.4)
5.	The Rao-Blackwell estimator for posterior densities averages over full conditionals available from a Gibbs sampler. Why does conditioning on additional information reduce variance? And why is this information only available in certain sampler architectures? (Goal 9.4)
6.	Nearest-neighbor estimation uses a local bandwidth — the bandwidth at each point is determined by the local data density. What is the consequence in sparse regions? In dense regions? How does this compare to the behavior of a fixed-bandwidth kernel estimator in the same regions? (Goal 9.5)

## Module 10 — Applied Cases

*\<Introduction block\>*

### Reading Sequence
Module 10 is primarily a doing module rather than a reading module. The readings below are short synthesis pieces and a targeted BDA section. They should be read alongside applied work, not in a single sitting before starting.

1. *Gelman et al. (2013) — Bayesian Data Analysis, 3rd ed.*\
**Ch 6: Model checking — prior predictive, posterior predictive, and graphical checks**
	- **Focus**: This chapter introduces the posterior predictive check as a principled model criticism tool. Focus on what a posterior predictive check tests (whether the model can reproduce features of the observed data) and what a failure implies (the model is misspecified in some detectable way). Also important: what a passing check does not imply.
	- **Builds toward**: Goal 10.4 asks you to demonstrate a posterior predictive check — this chapter is the source. Return to it when you conduct one in an applied case.
2. *Efron & Hastie (2016) — Computer Age Statistical Inference*\
**Epilogue: A short timeline from 1900 to 2016 tracing statistical progress**
	- **Focus**: Read as a disciplinary retrospective, not for new technical content. The Epilogue traces the movement of statistical progress between Applications, Mathematics, and Computation across the twentieth century. It closes the frame opened by Tukey (1962) in Module 0. Note: the Epilogue is short and is the correct synthesis reading — Chs 16–18 cover Lasso and neural networks and are not retrospectives.
	- **Builds toward**: Goal 10.6 asks you to situate the program's methods within the broader arc of modern statistical practice. This reading, paired with Gelman & Vehtari (2021), is what makes that situating possible.
3. *Gelman & Vehtari (2021)* — What Are the Most Important Statistical Ideas of the Past 50 Years?\
**JASA 116(536) — read in full**
	- **Focus**: Read as a second disciplinary retrospective, paired with the Efron & Hastie Epilogue. Gelman & Vehtari cover ideas rather than history — their list includes counterfactual causal inference, regularization, Bayesian computation, and multilevel modeling. Assess which of these ideas you have encountered in the program and which remain outside it.
	- **Builds toward**: This reading closes the frame opened by Tukey (1962) in Module 0 — ask yourself whether Tukey's call for a reformation of statistics has been answered, and if so, by what.

[Optional] *Donoho (2017)*, '50 years of data science,' Journal of Computational and Graphical Statistics 26(4). Opens explicitly with Tukey (1962) and traces the subsequent data science debate. A second perspective alongside Gelman & Vehtari for Goal 10.6. Freely available online.

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
- Select and justify appropriate methods for each component of a multi-part applied problem, recognizing when a problem's structure calls for a specific tool and when alternatives would be equally valid? (Goal 10.1)
- Construct, fit, and diagnose a Bayesian model end-to-end — from prior specification through MCMC sampling, diagnostic evaluation, and interpretation of posterior output? (Goal 10.2)
- Apply bootstrap inference as a validation or subsidiary analysis tool within a larger workflow, and recognize when its assumptions are stressed? (Goal 10.3)
- Demonstrate a posterior predictive check as a model criticism tool — explaining what it tests, what a failure implies, and what it cannot detect? (Goal 10.4)
- Produce a complete analysis that is reproducible, honestly reported, and explicit about the assumptions and limitations of every methodological choice? (Goal 10.5)
- Situate the program's methods within the broader arc of modern statistical practice using Efron & Hastie (Epilogue) and Gelman & Vehtari (2021)? (Goal 10.6)

#### Conceptual Questions
1.	Tukey (1962) argued for a reformation of statistics toward data analysis. Looking back at the program, which methods most directly embody Tukey's argument? Which remain more 'mathematical statistics' in his sense? (Goal 10.6)
2.	Gelman & Vehtari (2021) list several ideas they consider most important in the past 50 years. Which of these ideas does this program cover? Which does it not cover, and why might those omissions be defensible at this scope? (Goal 10.6)
3.	A posterior predictive check shows that your model cannot reproduce a key feature of the data. What are your options, and what does each option commit you to? (Goal 10.4)
4.	The program treats the bootstrap and MCMC as conceptually related: both are simulation-based inference methods. What do they share, and where does the analogy break down? (Goal 10.1)
5.	In Efron & Hastie's retrospective, statistics moves between Applications, Mathematics, and Computation across the twentieth century. Where would you locate the program's methods on that map, and does that location feel right to you? (Goal 10.6)









