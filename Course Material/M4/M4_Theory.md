# Module 4
## Optimization: Gradient Methods, Metaheuristics & EM
*\<Introduction block\>*

#### Module Goal
*\<Module Goal block\>*

#### Specific Goals[^1]
[^1]:Specific goals will be cited as `Goal M.g` throughout the program. See `ProgramGoalsReference.md`

*\<Specific Goals block\>*

---

### Reading Guide
The module has three tracks corresponding to three algorithmic families. Tracks A and B should be read in order — EM builds on the optimization theory foundation Track A establishes. Track C is short and can be read at any point after Track A, but reading it last, with the full module in view, makes the structural contrast between the three families clearest.

***

#### Track A — Gradient Methods

1. *Lange (2010) — Numerical Analysis for Statisticians, 2nd ed.*\
**Sections 11.1–11.2**
	- **Focus**: Read **§11.1** as orientation, then work through **§11.2** carefully. The central results are Fermat's necessary condition (vanishing gradient at a local minimum), the second-order sufficient condition (positive definite Hessian at a stationary point), and what coerciveness guarantees about the existence of a minimum. These are the theoretical foundations on which all iteration schemes in this chapter rest. The examples in §11.2 are worth following through; they show what analytical solvability looks like and why it is exceptional.
		> **Exclude**: **§11.3–§11.4** (Optimization with Equality and Inequality Constraints, Lagrange multipliers, KKT conditions). These are important for constrained optimization but are not load-bearing for any goal in this module. **§11.5 (Convexity)** and **§11.6 (Block Relaxation)** are also excluded — convexity is used implicitly throughout the module but not developed here at the required depth, and block relaxation is a topic for the MM framework in Ch 12.
	- **Builds toward**: The stationarity and Hessian results from §11.2 are the theoretical underpinning for Newton's method in Ch 14 — you are establishing the optimality conditions that Newton's method is designed to find.

	**Sections 14.1–14.4**
	- **Focus**: **§14.1** is short — read it to see how Lange situates Newton's method relative to MM and EM. **§14.2** establishes the root-finding form of Newton's method (which most students will have seen in one dimension); **§14.3** applies it to optimization of a loglikelihood, introducing the score and observed information. This is where Ch 11's Hessian theory becomes a practical computation. **§14.4 (Ad Hoc Hessian Approximations)** is important for Goal 4.2: it explains why positive definite Hessian approximations are sought and introduces the outer-product approximation and the idea of replacing second-order terms that are small on average. Read §14.4 for the conceptual logic rather than for technical exhaustiveness.
	> **Exclude**: **§14.5–§14.8** (Scoring and Exponential Families, Gauss-Newton, Generalized Linear Models, MM Gradient Algorithm). These are well-crafted applications and extensions but are outside the stated goals of this module — they require the exponential family and GLM background that the program does not develop here, and the MM gradient algorithm presupposes Ch 12 (unassigned). **§14.10–§14.11** (Accelerated MM and Problems) are also excluded.
	
	- **Builds toward**: §14.1–§14.4 deliver Goal 4.2 directly. §14.9 (quasi-Newton) follows below.

3. *Nocedal & Wright (2006) — Numerical Optimization, 2nd ed.*\
**Section 3.1: Wolfe conditions and step-length selection**
	- **Focus**: Read as the formal backstory to the step-selection concern raised in Lange Ch 14. The sufficient decrease condition (Armijo) and curvature condition together constitute the Wolfe conditions; understand why both are needed and what each one prevents. This section is self-contained and short.
	- **Builds toward**: Step-length selection is what keeps Newton-type methods from overshooting or cycling far from the solution — this is the practical stability concern Goal 4.2 asks you to explain.

4. *Lange (2010) — Numerical Analysis for Statisticians, 2nd ed.*\
**Section 14.9: Quasi-Newton Methods**
	- **Focus**: Read after §14.1–§14.4 and the Wolfe conditions material. §14.9 introduces the secant condition and Davidon's rank-one update, followed by the DFP and BFGS rank-two updates. Focus on the conceptual logic: quasi-Newton methods avoid the cost of computing the Hessian exactly by building an approximation iteratively from gradient information. The self-correcting properties of BFGS (mentioned in Ch 14 and developed more fully in N&W §6.1) are the reason BFGS dominates in practice.

5. *Nocedal & Wright (2006) — Numerical Optimization, 2nd ed.*\
	**Section 6.1: BFGS method and convergence** & **Section 7.2: L-BFGS**
	- **Focus**: Use as targeted depth after Lange §14.9. §6.1 works through the BFGS update formula, convergence properties, and the self-correcting behavior in detail. §7.2 covers L-BFGS (limited-memory BFGS) for large-scale problems where storing the full approximate Hessian is infeasible. For §7.2, the goal is understanding what problem L-BFGS solves and how the two-loop recursion replaces explicit Hessian storage — implementation detail is not required.

	**Appendix A.** **[Optional]**
	Provides the formal definitions of conditioning and stability and their relationship to convergence. Read if the conditioning material in Lange Ch 14 feels underspecified; treat as a reference rather than a read-through.

***

#### Track B — EM Algorithm

6. *Dempster, Laird & Rubin (1977) — Maximum Likelihood from Incomplete Data via the EM Algorithm*\
**JRSS-B 39(1) — read in full**
	- **Focus**: Read for the founding argument: the missing data framing, the construction of the E and M steps, and the monotone likelihood claim. Do not read for technical completeness — Lange Ch 13 and Wu (1983) fill that in. Read DLR the way you read Tukey (1962) in Module 0: for the idea and its justification.
	- **Builds toward**: The missing data framing here is the conceptual key to Goal 4.3. Understanding EM as a statistical algorithm — not just a numerical procedure — depends on seeing what problem it is designed to solve.

7. *Lange (2010) — Numerical Analysis for Statisticians, 2nd ed.*\
**Ch 13, §13.1–13.4: Introduction, General Definition, Ascent Property, Missing Data in the Ordinary Sense**
	- **Focus**: Read after DLR. §13.1–§13.2 restate the EM definition formally; §13.3 (Ascent Property) is the most important section in the chapter — it proves monotone likelihood increase via Jensen's inequality. Work through this proof carefully: understanding why the ascent property holds, not just that it does, is what Goal 4.4 requires. §13.4 shows EM applied to exponential families with missing data, which is the most common practical setting and the clearest illustration of how the E step fills in a sufficient statistic.
	> **Note on §13.3**: Lange's introduction to Ch 13 warns that the proof involves measure theory and that some readers may want to take the result on faith. Do not do this. The proof in §13.3 is the Jensen's inequality argument — it is accessible and is the conceptual heart of Goal 4.4. Read it.

	> **Note on the MM framework**: Lange presents EM as a special case of the MM algorithm, and Ch 13 contains repeated references to Ch 12 (The MM Algorithm), which is not assigned. You do not need Ch 12 to follow Ch 13 — the EM derivation is self-contained — but students who find the MM references distracting may consult Ch 12 §12.1–§12.2 (Introduction and Philosophy of the MM Algorithm) for orientation. This is purely optional.

	> **Exclude**: **§13.5–§13.9** (Bayesian EM, Allele Frequency Estimation, Clustering, Transmission Tomography, Factor Analysis). These are worked examples of EM in specific contexts — well-constructed and worth returning to, but not load-bearing for any of the five module goals.
	Students who want a concrete example beyond §13.4 should read §**13.6 (Allele Frequency Estimation)**, which is the most self-contained of the application sections and clearly illustrates the interplay between observed phenotypes and latent genotypes as missing data.

	- **Builds toward**: §13.1–§13.4 deliver Goals 3 and 4 directly.

8. *Wu (1983) — On the Convergence Properties of the EM Algorithm*\
**Annals of Statistics 11(1) — read for the main result and its significance**
	- **Focus**: Read for what Wu establishes over DLR: the stationary point characterization, and why monotone increase does not imply convergence to the global maximum — or even to a local maximum, in the absence of additional conditions. You do not need to work through every proof; the conceptual contribution and its relationship to DLR's original claim is the target. Goal 4.4 asks you to articulate this relationship precisely.
	- **Builds toward**: This is the sole source for the DLR-versus-Wu distinction that Goal 4.4 requires.

***

#### Track C — Metaheuristics

9. *Givens & Hoeting (2013) — Computational Statistics, 2nd ed.* [Reference]\
**Ch 3: §3.3 (Simulated annealing); §3.4 (Genetic algorithms)**
	- **Focus**: Read for orientation and conceptual understanding, not implementation depth. The goal is to understand when metaheuristic approaches are warranted — discontinuous objectives, multimodal landscapes, discrete or combinatorial search spaces — and what each method does at the level of operating principles.
		> **Forward pointer**: Simulated annealing accepts worse solutions with a probability controlled by a temperature schedule. This is structurally parallel to the Metropolis-Hastings acceptance step in Module 7 — both use a ratio-based acceptance criterion to explore a target landscape. Noticing that parallel before reaching Module 7 makes the MH acceptance ratio feel less arbitrary when you derive it from detailed balance.

### Self-Assessment
#### Quick Checklist
After finishing the reading, can you:
- Formulate at least two common statistical estimators as optimization problems, and identify which objective function features determine the appropriate algorithmic family? (Goal 4.1)
- Explain Newton's method and quasi-Newton methods, including the role of the Hessian and the practical significance of numerical stability and step selection? (Goal 4.2)
- Explain the statistical logic of EM — missing data, latent variables, lower-bound ascent — and describe the construction of the E and M steps? (Goal 4.3)
- Explain why EM guarantees monotone likelihood increase, why this does not guarantee a global maximum, and what Wu (1983) establishes over Dempster et al. (1977)? (Goal 4.4)
- Recognize when metaheuristic approaches are warranted and describe the basic operating principles of simulated annealing and genetic algorithms without requiring deep implementation? (Goal 4.5)

#### Conceptual Questions
1. Newton's method converges quadratically near a solution but can diverge or cycle far from one. What is the mechanism of quadratic convergence, and what can go wrong far from the solution? (Goal 4.2)
2. Quasi-Newton methods approximate the Hessian rather than computing it exactly. What is the tradeoff? When would you prefer BFGS over Newton's method, and when might the approximation cause problems? (Goal 4.2)
3. EM is described as an algorithm for "maximum likelihood from incomplete data." What does incomplete data mean in this context, and how does that framing generate the two-step structure? (Goal 4.3)
4. EM guarantees that the likelihood increases at every iteration. Does this mean it will find the global maximum? Explain what Wu (1983) says about where EM converges and why that is weaker than convergence to the MLE. (Goal 4.4)
5. Simulated annealing accepts worse solutions with some probability. Gradient methods always move in an improving direction. What problem does that probabilistic acceptance solve, and why does gradient descent not solve it? (Goal 4.5)