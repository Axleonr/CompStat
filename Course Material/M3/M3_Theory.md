# Module 3
## Bootstrap & Resampling

The bootstrap is one of the most conceptually elegant ideas in statistics: use the data itself as a model of the population, and simulate the sampling process by drawing from that model repeatedly. This module develops both parametric and nonparametric bootstrap from first principles, derives confidence intervals through multiple approaches, and examines the theoretical conditions under which the bootstrap provides valid inference.

Equally important is understanding when the bootstrap fails. Heavy-tailed distributions, extreme statistics, small samples, and dependent data all create situations where naive resampling breaks down. A practitioner who knows only that the bootstrap works is less useful than one who also knows where it stops working.

#### Module Goal

Perform inference through data-driven simulation, understand the theoretical basis for its validity, and recognize the conditions under which it breaks down.

#### Specific Goals[^1]
[^1]:Specific goals will be cited as `Goal M.g` throughout the program. See `ProgramGoalsReference.md`

1. Derive the nonparametric bootstrap from first principles — articulating what the empirical distribution is, why sampling from it simulates the sampling process, and what assumptions that substitution requires
2. Implement parametric and nonparametric bootstrap and construct confidence intervals through multiple methods, including bootstrap-t, percentile, and BCa approaches; explain the accuracy hierarchy among these methods — distinguishing first-order from second-order accuracy — and identify which methods are transformation-respecting and why that property matters.
3. Explain the theoretical conditions under which bootstrap confidence intervals are valid, and distinguish between the bootstrap's consistency and its accuracy in finite samples
4. Identify and diagnose the conditions under which naive bootstrap fails: heavy-tailed distributions, extreme statistics, small samples, and dependent or clustered data
5. Apply modified resampling strategies — including the moving blocks bootstrap — for dependent and structured data, and explain what each modification corrects for and what residual limitations remain
6. Relate the bootstrap to the simulation primitives from Module 1 — the bootstrap is a resampling algorithm, and its behavior is as amenable to computational analysis as any other

---

### Reading Guide
Read Efron (1979) first — it is short and establishes the founding argument. Efron & Tibshirani then develops the method systematically across several stages. Davison & Hinkley is secondary but not supplemental — the failure modes material is part of what it means to understand the bootstrap.

**Foundations**

1. *Efron (1979) — Bootstrap Methods: Another Look at the Jackknife*, from *Annals of Statistics Vol. 7 #1*\
	Read for the founding argument: what the empirical distribution is, why sampling from it simulates the sampling process, and what assumptions that substitution requires. Do not read for technical completeness — subsequent readings will fill that in. 


**Stage 1: Bootstrap foundations and standard errors**

2. *Efron & Tibshirani (1993) — An Introduction to the Bootstrap*\
	**Chapters 1, 2 & 4**

	- **Focus:** The empirical distribution and the plug-in principle from Ch 4 is the conceptual foundation for why the bootstrap substitution works.
	
	- **Builds toward**: Ch 6, where the bootstrap is defined formally and the standard error algorithm is made precise.

	> *Ch 3* is background probability review; treat it as optional reference material if the notation in later chapters needs grounding.

	**Chapter 6**\
	This is the formal definition of the bootstrap standard error estimate, the resampling algorithm, and the parametric bootstrap. 

	- **Focus**: Make sure you understand the plug-in logic connecting Ch 4 to the bootstrap: *what is the bootstrap standard error?* Also note §6.5 (parametric bootstrap) serves the implementation requirements of Goal 3.2

	**Chapter 8**\
	This chapter extends the basic bootstrap to more complicated data structures, including serially dependent data, and is the module's source for the moving blocks bootstrap.

	- **Focus**: Give §8.6 your closest reading, attending to the role of block length and the limitations that remain. Davison & Hinkley §2.6.4 diagnoses why naive resampling fails for dependent data; this chapter is where that failure is addressed.

	**Chapter 10: Estimates of bias [Optional]**\
	Covers bootstrap and jackknife bias estimation. Not required, but it is useful as background before Ch 11 if the jackknife's bias treatment feels unmotivated on first reading.

**Stage 2: Jackknife [Optional]**

3. *Efron & Tibshirani (1993) — An Introduction to the Bootstrap*\
	**Chapter 11**\
	Ch 11 defines the jackknife, derives its standard error and bias estimates, and establishes its relationship to the bootstrap.

	- **Focus**:  §11.6 is important: it illustrates that method failure is diagnosable, not merely possible.

	- **Builds toward**: The failure modes discussion in Davison & Hinkley, where the bootstrap itself encounters analogous limits.

**Stage 3: Confidence intervals**

4. *Efron & Tibshirani (1993) — An Introduction to the Bootstrap*\
	**Chapter 12**\
	Ch 12 introduces the bootstrap-t interval. Read **§12.1–§12.5** as required;
	**§12.6** (transformations and the bootstrap-t) is depth. 

	- **Builds toward**: Ch 13, where the percentile method is introduced as an alternative with different properties.

	**Chapter 13**\
	Ch 13 introduces the percentile interval.

	- **Focus**: Focus on what the percentile interval assumes and where it fails relative to bootstrap-t. The coverage performance discussion (§13.5) and the transformation-respecting property (§13.6) are directly relevant to understanding why BCa was developed.

	- **Builds toward**: Ch 14, where BCa corrects the problems and limitations of both the percentile interval and bootstrap-t.

	**Chapter 14, Sections 14.1–14.3**\
	This is the core of the BCa method: the motivation, the worked example, and the BCa construction including the bias-correction and acceleration constants. 
	
	- **Focus**: Focus on what BCa achieves that neither Ch 12 nor Ch 13 achieves alone. The accuracy hierarchy is the conceptual payoff of the entire confidence interval sequence.

	> §14.4 (ABC method) is secondary depth — read if you want to understand how BCa endpoints can be approximated analytically without Monte Carlo. 
	>§14.5 (tooth data example) is optional depth; the authors flag it as more advanced and skippable on first reading.

5. *Davison & Hinkley (1997) — Bootstrap Methods and Their Application*\
	**Section 2.6 (selected subsections)**\
	**§2.6.1** is the primary source for the conditions under which bootstrap confidence intervals are valid and for the pivotal/non-pivotal accuracy comparison.\
	**§2.6.2** and **§2.6.4** are the failure-mode content for Goal 3.4.

	- **Focus**: Note that §2.6.1 is the theoretical backstop that distinguishes what the bootstrap guarantees from what it merely approximates.\
	In §2.6.2 and §2.6.4, for each failure case, ask: *what assumption does it violate, and what symptom would alert you in practice?*

	> §2.6.3 (conditional properties) is outside the module's scope; skip it. For the remediation methods that address the dependence failure mode identified in §2.6.4, see Efron & Tibshirani Ch 8.

6. *Davison & Hinkley (1997) — Bootstrap Methods and Their Application*\
**Section 3.8: Hierarchical Data**\
Read §3.8 as a source for clustered data as a bootstrap failure mode. The cluster-aware resampling schemes it describes are not assigned.
	- **Focus**: Keep this failure distinct from the serial dependence covered in §2.6.4 above and in Efron & Tibshirani Ch 8. Serial dependence is a temporal-correlation failure; clustering is a grouping/exchangeability failure (within-cluster correlation). Both break the i.i.d. assumption naive resampling needs, but they are different mechanisms and should not be conflated. As you read, ask what symptom in a dataset would tell you clustering applies.


### Self-Assessment
#### Quick Checklist
After finishing the reading, can you:
- Derive the nonparametric bootstrap from first principles — defining the empirical distribution, explaining why sampling from it simulates the sampling process, and stating what assumptions that requires? (Goal 3.1)
- Implement parametric and nonparametric bootstrap and construct bootstrap-t, percentile, and BCa confidence intervals? (Goal 3.2)
- Explain the theoretical conditions under which bootstrap confidence intervals are valid, and distinguish consistency from finite-sample accuracy? (Goal 3.3)
- Identify the conditions under which naive bootstrap fails: heavy tails, extreme statistics, small samples, and dependent or clustered data? (Goal 3.4)
- Articulate why clustered data violates the i.i.d. assumption underlying naive resampling, and distinguish this clustering failure mechanism from the serial-dependence failure mechanism addressed by the moving blocks bootstrap? (Goal 3.4)
- Apply the moving blocks bootstrap for serially dependent data, explain what block resampling preserves that naive resampling destroys, and identify the role of block length in the bias-variance tradeoff of the procedure? (Goal 3.5)
- Implement bootstrap-t, percentile, and BCa confidence intervals and explain what each assumes and what accuracy guarantees each provides? (Goal 3.2)
- Explain the accuracy hierarchy — first-order vs. second-order accuracy — and identify which interval methods achieve each? (Goal 3.2)
- Explain transformation-respecting as a property and identify which methods satisfy it? (Goal 3.2)
- Describe the bootstrap as a resampling algorithm and connect it to the simulation primitives from Module 1? (Goal 3.6)

#### Conceptual Questions
1.	The bootstrap replaces the unknown population distribution with the empirical distribution. What exactly does that substitution assume, and under what conditions is it a good approximation? What does “consistency” mean here?
2.	There are multiple ways to construct a bootstrap confidence interval (bootstrap-t, percentile, BCa). They give different answers in finite samples. Why do they differ, and when does the difference matter?
3.	The BCa method is described as both second-order accurate and transformation-respecting, while the percentile method is transformation-respecting but only first-order accurate, and the bootstrap-t is second-order accurate but not transformation-respecting. Explain what each of these properties means and why BCa achieves both while the others achieve only one.
4.	The bootstrap is sometimes described as “assumption-free.” Is that accurate? What does the bootstrap assume, and what does it not assume? (Goal 3.3)
5.	The bootstrap fails for heavy-tailed distributions of the mean. Explain the mechanism of that failure — why does the empirical distribution not capture the behavior of the tail, and why does that matter for the bootstrap confidence interval?
6.	The moving blocks bootstrap corrects for temporal dependence by resampling overlapping blocks of consecutive observations rather than individual draws. What property of the data is being preserved, and what does naive resampling destroy? What role does block length play in the bias-variance tradeoff of the procedure?