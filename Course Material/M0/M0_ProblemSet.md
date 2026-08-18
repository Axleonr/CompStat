# Computational Statistics — Problem Sets

## Module 0 — Computational Thinking & Statistical Algorithms

### PS0.1 — An estimator as an algorithm

**Type:** C | **Tier:** self-audit | **Core/Optional:** Optional | **Time:** 35 min | **Goals:** 0.1, 0.2, 0.3

**Prerequisites:** None

**Statement:**

Pick one estimator you already know well from prior coursework — for concreteness, the sample mean together with its standard confidence interval, or the ordinary-least-squares slope in simple linear regression, are both good choices, but any familiar estimator works.

1. **Describe it as an algorithm**, explicitly separating three things: the **inputs** (what data and any fixed constants the procedure needs), the **computational process** (the actual sequence of arithmetic operations that turns the inputs into a result — write this as prose or a short pseudocode sketch, not as language-specific code), and the **outputs** (what quantity or quantities the procedure returns, and in what form — a point estimate, an interval, etc.).
2. **Apply the four computational questions** below to your chosen estimator. Write 2–4 sentences for each — enough to show you have actually thought through what the question means for *this specific procedure*, not a generic restatement of the question:
   - **Convergence.** Does the procedure produce a single exact answer in one step, or does it approach an answer through some iterative or asymptotic process? If it's the latter, what is it converging *to*, and under what condition does that convergence happen?
   - **Sensitivity.** How does the output respond to small changes in the input data — a single altered or added observation, for instance? Is the procedure's sensitivity uniform across "typical" data, or are there specific conditions (e.g., outliers, small sample size) that make it much more sensitive?
   - **Efficiency.** How does the computational cost of the procedure scale as the input size grows? Is there a step that dominates the cost?
   - **Failure conditions.** Under what circumstances does the procedure break down entirely, produce a nonsensical answer, or fail to be defined at all (e.g., division by zero, a degenerate input)?
3. **Close with one sentence** distinguishing, for your specific procedure, what is *derived* analytically (worked out once, in closed form, by mathematical argument) from what is *computed* algorithmically (carried out numerically, step by step, on the specific data at hand) — most familiar estimators involve both, and naming which part is which is the point of this closing sentence.

**Deliverable:** (i) the three-part algorithm description (inputs/process/outputs); (ii) the four computational-questions answers (2–4 sentences each); (iii) the one-sentence derive-vs-compute distinction.

**Verification:** [Self-audit — the same mode Module 5 uses; there is no numeric target here, and none is needed, since this is a written conceptual exercise about a procedure the student already knows how to execute, not a new implementation to check against truth.] Self-audit checklist:
- [ ] Inputs, process, and outputs are each explicitly and separately named (not blended together in one description).
- [ ] All four computational questions are addressed, and each answer is specific to the chosen estimator (an answer that would apply word-for-word to any procedure at all is a sign the question wasn't engaged with concretely).
- [ ] The derive-vs-compute distinction is stated for at least one specific component of the procedure, not asserted in the abstract.
- [ ] No implementation code was written anywhere in this problem (Module 0's binding no-code constraint).

**Discussion note:** This exercise exists to install the vocabulary — algorithm, convergence, sensitivity, efficiency, failure condition, derive-vs-compute — that the rest of the program uses constantly without re-explaining. A good answer for the sample-mean-and-CI choice, for instance, would note: the *mean itself* is a one-step closed-form computation (no convergence question arises for it at all), while the *CI's coverage guarantee* is an asymptotic/derived property (relying on a CLT-style argument, not computed from the specific sample) — already a clean illustration of the closing distinction in step 3. A common shallow answer treats all four computational questions as generic filler ("efficiency: it's fast") rather than saying anything specific to the chosen procedure; the checklist's second item is aimed directly at catching that. This problem deliberately stops at description — no code, no simulation, no numeric check — consistent with Module 0's "no code" commitment.
