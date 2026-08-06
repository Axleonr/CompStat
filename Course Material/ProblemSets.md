# Computational Statistics Program — Problem Sets

*v1.0*


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

**Verification:** [Self-audit — this module's only available R1 mechanism, same mode Module 5 uses; there is no numeric target here, and none is needed, since this is a written conceptual exercise about a procedure the student already knows how to execute, not a new implementation to check against truth.] Self-audit checklist:
- [ ] Inputs, process, and outputs are each explicitly and separately named (not blended together in one description).
- [ ] All four computational questions are addressed, and each answer is specific to the chosen estimator (an answer that would apply word-for-word to any procedure at all is a sign the question wasn't engaged with concretely).
- [ ] The derive-vs-compute distinction is stated for at least one specific component of the procedure, not asserted in the abstract.
- [ ] No implementation code was written anywhere in this problem (Module 0's binding no-code constraint).

**Discussion note:** This exercise exists to install the vocabulary — algorithm, convergence, sensitivity, efficiency, failure condition, derive-vs-compute — that the rest of the program uses constantly without re-explaining. A good answer for the sample-mean-and-CI choice, for instance, would note: the *mean itself* is a one-step closed-form computation (no convergence question arises for it at all), while the *CI's coverage guarantee* is an asymptotic/derived property (relying on a CLT-style argument, not computed from the specific sample) — already a clean illustration of the closing distinction in step 3. A common shallow answer treats all four computational questions as generic filler ("efficiency: it's fast") rather than saying anything specific to the chosen procedure; the checklist's second item is aimed directly at catching that. **Scope discipline (WO-M0 §5):** this problem deliberately stops at description — no code, no simulation, no numeric check — consistent with Module 0's "no code" commitment; if a future revision drifts toward asking for an implementation or a computed check, that is scope creep to be deleted, not extended.

---

### Alignment matrix — Module 0

| Goal | Text (`Module_Goals_Reference.md`) | Problem(s) / justification |
|---|---|---|
| 0.1 | Reframe statistical procedures as algorithms: inputs, outputs, and the computational process connecting them | PS0.1 |
| 0.2 | Distinguish between deriving a statistical result analytically and computing one algorithmically — and articulate why that distinction matters | PS0.1 |
| 0.3 | Identify the questions that the computational framing opens up: convergence, sensitivity, efficiency, failure conditions | PS0.1 |
| 0.4 | Situate the program's core methods (simulation, resampling, optimization, MCMC) within a unified algorithmic view of statistics | Deliberately unexercised — per WO-M0 §3, this is checklist/conceptual-question territory (no implementation verb; R2's mandatory-coverage rule does not apply) |
| 0.5 | Read Tukey (1962) as a disciplinary argument — identify its central claim and assess its relevance to contemporary computational practice | Deliberately unexercised — per WO-M0 §3, a reading-and-conceptual-question goal with no problem-set vehicle by design (no implementation verb) |

### Module 0 hours
| Core problems | Core hours | Optional hours (uncounted) | Budget (§5) |
|---|---|---|---|
| 0 | 0 | 0.58 hr (35 min, PS0.1 only) | 0–1 |


---

## Module 1 — Random Number Generation & Simulation

### PS1.1 — Building and testing a linear congruential generator
**Type:** I | **Tier:** 2+3 | **Core/Optional:** Core | **Time:** 40 min | **Goals:** 1, 2
**Prerequisites:** None
**Statement:**
A linear congruential generator (LCG) produces a sequence of integers by the recurrence
$$X_{n+1} = (aX_n + c) \bmod m,$$
with uniform draws obtained as $U_n = X_n / m \in [0,1)$. Use the following fully specified generator (do not use your language's built-in RNG for this problem — implement the recurrence from primitives, per the module's from-scratch requirement):
- $m = 2^{31} - 1 = 2{,}147{,}483{,}647$
- $a = 16{,}807$
- $c = 0$
- Seed: $X_0 = 123{,}456{,}789$

Generate $n = 10{,}000$ draws $U_1, \dots, U_{10{,}000}$. Subject the sequence to two empirical uniformity tests:

1. **Binned chi-square goodness-of-fit test.** Partition $[0,1)$ into $k=10$ equal-width bins, count how many draws fall in each, and compute
$$\chi^2 = \sum_{i=1}^{k} \frac{(O_i - E_i)^2}{E_i}, \quad E_i = n/k.$$
Under the null hypothesis of uniformity, $\chi^2$ follows a chi-square distribution with $k-1$ degrees of freedom (a standard result of goodness-of-fit theory — available in any statistics reference and computable via your language's chi-square library functions, which you may use for this comparison only, per R1.4/R4).

2. **Lag-1 serial correlation test.** Compute the sample correlation $r_1$ between the pairs $(U_i, U_{i+1})$ for $i = 1, \dots, n-1$. Under the null hypothesis that the sequence is i.i.d., the sampling variance of $r_1$ is approximately $1/n$ for large $n$ (Bartlett's formula for the null variance of a serial correlation coefficient — again a standard textbook fact, not something to look up numerically). Form $z = r_1 \sqrt{n}$ and compare to the standard normal distribution.

Also produce a lag-1 pairs plot ($U_i$ vs. $U_{i+1}$) as a visual complement to the correlation test — you will reuse this style of plot in PS1.5 to see what a *bad* generator's version of this plot looks like.

Finally, write a brief note (3–5 sentences) on **period and seed dependence**: (a) verify empirically that your 10,000 draws contain no repeated value, and explain why this is a necessary (not sufficient) condition for the generator's period exceeding 10,000; (b) show what happens if you seed with $X_0 = 0$, and explain why this seed must be avoided for this generator.

**Deliverable:** Your LCG implementation; the chi-square statistic, its degrees of freedom, and the resulting p-value or critical-value comparison; the serial correlation $r_1$, $z$-statistic, and p-value; the lag-1 pairs plot; the period/seed-dependence note.

**Verification:** [Tier 2 + Tier 3]
- *Tier 2:* the null distributions used for both tests ($\chi^2_{k-1}$ for the goodness-of-fit statistic; $\text{Var}(r_1) \approx 1/n$ under the i.i.d. null, hence $r_1\sqrt{n} \approx N(0,1)$) are citable standard statistical facts, not computed targets — you may use your language's library functions (e.g., `scipy.stats.chi2`, R's `qchisq`/`pchisq`, or equivalents) to obtain the exact critical value/p-value from these named distributions.
- *Tier 3 (validation-log entry `PS1.1`):* under the stated seed and generator, a correct implementation should obtain a chi-square statistic of **8.09 (± 0.05)** on $df=9$ — comfortably below the $\alpha=0.05$ critical value of **16.92** — and a serial-correlation $z$-statistic of **−0.50 (± 0.02)**, comfortably inside $(-1.96, 1.96)$. Both indicate failure to reject uniformity/independence, as expected for this generator. Your own sequence should also contain zero repeated values among the 10,000 draws, and seeding with $X_0=0$ should produce a sequence that is identically zero from the first draw onward.
**Discussion note:** *(folded)* A well-constructed LCG with these parameters should pass both tests comfortably — the point of the exercise is less "does it pass" and more "what would failing look like, and why." Common failure modes to watch for: an off-by-one in the recurrence (updating $U_n$ before or after incrementing $n$ inconsistently), using floating-point division prematurely (accumulating rounding error across the multiplicative recurrence — keep $X_n$ as an integer throughout and only divide by $m$ at the end), and forgetting that $c=0$ makes $X_0=0$ an absorbing fixed point. On the serial-correlation test specifically: because it is a size-0.05 test, roughly 1 run in 20 will show $|z|>1.96$ purely by chance even for a good generator — a single rejection under a *different* seed than the one stated here is not by itself evidence of a bad generator, only evidence that you ran a hypothesis test (this is worth sitting with, since it previews the same logic used to interpret R-hat and other diagnostics later in the program). The period argument here is deliberately partial: "no repeats in 10,000 draws" rules out a short period but does not establish the generator's true (much longer) period, which is a number-theoretic fact about $a$ and $m$ this problem does not ask you to derive.

---

### PS1.2 — Inverse transform: closed-form and numerical
**Type:** I | **Tier:** 1/2 + 3 | **Core/Optional:** Core | **Time:** 45 min | **Goals:** 3
**Prerequisites:** None (library uniform RNG only — the from-scratch requirement here is the transform, not the generator; per R4's Module 1 exception, generator-primitives are PS1.1's job)
**Statement:**

**(a) Closed-form CDF case — the Pareto distribution.** The Pareto distribution with scale $x_m$ and shape $\alpha$ has CDF $F(x) = 1 - (x_m/x)^\alpha$ for $x \geq x_m$. Derive the inverse-transform sampler: show that if $U \sim \text{Unif}(0,1)$, then $X = x_m U^{-1/\alpha}$ is Pareto-distributed with parameters $(x_m, \alpha)$ (using $U$ in place of $1-U$ is valid since both are $\text{Unif}(0,1)$). Implement this power-transform sampler using $x_m = 1$, $\alpha = 6$, drawing $U$ from your language's library uniform generator (seeded, per R5) with $n = 5{,}000$ draws. Overlay a histogram of your draws against the true Pareto density.

**(b) Numerical-inversion case — the standard normal.** The standard normal CDF $\Phi$ has no closed-form inverse. Implement inverse-transform sampling for $N(0,1)$ by numerically solving $\Phi(X) = U$ for $X$ given $U$, using a root-finding method you implement yourself (bisection is sufficient) on a bounded search interval (e.g., $[-10, 10]$, since $\Phi(-10) \approx 0$ and $\Phi(10) \approx 1$ to far more precision than you need). You may call your language's standard normal CDF function to *evaluate* $\Phi$ at each iterate of your search — the algorithm under test here is the numerical-inversion/root-finding loop, not a from-scratch reimplementation of $\Phi$ itself. Seed your uniform generator with $2024$ and draw $n = 5{,}000$ values of $U$; invert each to obtain $X_1, \dots, X_{5000}$.

**Deliverable:** (a) the derivation (2–3 lines), the implementation, the density overlay plot, and the sample mean compared to the Pareto's known mean; (b) the bisection (or equivalent) implementation, the sample mean and variance of your 5,000 draws, and their comparison to the standard normal's known moments (0 and 1).

**Verification:** [Tier 1/2 for (a); Tier 3 for (b), validation-log entry `PS1.2`]
- *(a), tier 1/2:* the power-transform identity is a standard, directly-derivable result (probability integral transform applied to the Pareto CDF — see also R&C, *Introducing Monte Carlo Methods with R*, Ex. 2.13, a solved exercise on this same construction). The numeric check rests on the Pareto distribution's own known moments — a citable textbook fact, not something to look up in a solutions manual: for $x_m=1, \alpha=6$, $E[X] = \frac{\alpha x_m}{\alpha - 1} = 1.2$. At $n=5{,}000$, your sample mean should fall within **1.2 ± 0.0104** (a 3-standard-error band, using the Pareto's known variance $\text{Var}(X) = \frac{x_m^2 \alpha}{(\alpha-1)^2(\alpha-2)} = 0.06$).
- *(b), tier 3:* under the stated seed, a correct implementation should obtain a sample mean within **0 ± 0.0424** and a sample variance within **1 ± 0.0600** (both 3-standard-error bands around the standard normal's known moments, calibrated empirically across multiple seeds in the validation log — not an exact-match target, since library uniform streams differ across languages even under the same stated seed).
**Discussion note:** *(folded)* Part (a) is the "easy" case: a closed-form CDF gives a closed-form inverse, and the whole exercise reduces to algebra. Part (b) is the point of the problem: almost no distribution you'll want in practice has a closed-form inverse CDF, and numerical inversion (root-finding on the CDF) is the general-purpose fallback — this is the same idea you will meet again, in a different guise, when acceptance-rejection (PS1.3) handles targets where even the forward CDF is unpleasant. A common failure mode in (b) is a search interval that isn't wide enough for extreme $U$ values close to 0 or 1 (bisection will silently return a boundary value rather than erroring) — check the tails of your $U$ sample if your moments look off. Both tolerance bands here are 3-standard-error bands at your stated $n$; if you rerun with a much larger or smaller $n$, the band should be rescaled accordingly (narrower for larger $n$), not reused as a fixed number.

---

### PS1.3 — Acceptance-rejection: two proposals for a normal target
**Type:** I/V | **Tier:** 1+2+3 | **Core/Optional:** Core | **Time:** 50 min | **Goals:** 4
**Prerequisites:** None
**Statement:**

Target: the standard normal density $f(x) = \frac{1}{\sqrt{2\pi}} e^{-x^2/2}$. You will sample from $f$ using acceptance-rejection under two different proposal distributions $g$, each requiring a bound $M$ such that $f(x) \leq M g(x)$ for all $x$. Recall the accept-reject algorithm: draw $Y \sim g$, draw $U \sim \text{Unif}(0,1)$, accept $Y$ as a draw from $f$ if $U \leq f(Y)/(Mg(Y))$, otherwise reject and repeat. The acceptance probability of this procedure is exactly $1/M$ (a standard, provable fact of the accept-reject method — see also R&C, *Introducing Monte Carlo Methods with R*, Ex. 2.5).

**Proposal 1 — standard Laplace (double exponential):** $g_1(x) = \frac{1}{2} e^{-|x|}$. Derive the optimal bound $M_1 = \sup_x f(x)/g_1(x)$ (hint: maximize over $|x|$; the maximum occurs at $|x|=1$) and hence the theoretical acceptance rate $1/M_1$.

**Proposal 2 — standard Cauchy:** $g_2(x) = \frac{1}{\pi(1+x^2)}$. Derive the optimal bound $M_2 = \sup_x f(x)/g_2(x)$ (the maximum again occurs at $|x|=1$ once you differentiate $(1+x^2)e^{-x^2/2}$) and the theoretical acceptance rate $1/M_2$.

For each proposal: implement the accept-reject loop from scratch (you may draw the proposal variates $Y$ using your language's library sampler for the Laplace or Cauchy distribution, or your own inverse-transform construction from PS1.2 — the algorithm under test is the accept-reject loop itself, not the proposal-sampling mechanism). Run $20{,}000$ proposal attempts per proposal, seeded at $31415$; record the number accepted and the empirical acceptance rate. Compare each empirical rate to its theoretical $1/M$. Rank the two proposals by acceptance rate and explain, in 3–5 sentences, what structural feature of a proposal distribution (relative to the target) drives a higher or lower acceptance rate.

**Deliverable:** both derivations ($M_1$, $M_2$, with the maximization shown); the accept-reject implementation for each proposal; empirical acceptance counts/rates for each under the stated seed; the ranking and explanation.

**Verification:** [Tier 1 for the general accept-reject theorem; Tier 2 for the closed-form bounds; Tier 3 for the empirical rates, validation-log entry `PS1.3`]
- *Tier 1:* the fact that acceptance-rejection has acceptance probability $1/M$ is standard, solved theory (R&C Ex. 2.5 derives this same result; Ex. 2.7 similarly explores what proposal-parameter choices keep this ratio well-behaved, the same theme this problem's ranking discussion takes up).
- *Tier 2:* $M_1 = \sqrt{2/\pi}\, e^{1/2} \approx 1.3155$ and $M_2 = 2\sqrt{\pi/2}\, e^{-1/2} \approx 1.5203$ are closed-form derivations from the target/proposal density ratio — check your own derivation against these values before running the empirical step.
- *Tier 3:* at $20{,}000$ proposal attempts, seeded at $31415$, your empirical acceptance rate should fall within **0.7602 ± 0.0090** for the Laplace proposal and **0.6577 ± 0.0101** for the Cauchy proposal (3-standard-error bands, calibrated across multiple seeds in the validation log). The Laplace proposal should show the higher acceptance rate of the two.
**Discussion note:** *(folded)* Both maxima occur at $|x|=1$ — worth noticing, since it isn't a coincidence tied to either specific proposal; it reflects where each proposal's tail-decay rate relative to the target's Gaussian decay is "worst" (closest to violating the bound). The Laplace proposal wins here because its exponential tail ($e^{-|x|}$) more closely tracks the Gaussian's tail behavior than the Cauchy's polynomial tail ($1/x^2$) does — the Cauchy proposal "wastes" a lot of its probability mass far out in tails the normal barely visits, which is exactly what a heavier-tailed-than-necessary proposal does to acceptance rate. A common derivation error: forgetting to take the log before differentiating (differentiating $f/g$ directly is messy; differentiating $\log(f/g)$ has the same maximizer and is far easier algebra). If your empirical rate is far below either theoretical value, check that you are evaluating $f$ and $g$ as densities (not accidentally using log-densities or an unnormalized target) inside the accept/reject test.

---

### PS1.4 — Tracing the generative chain: PRNG state to a normal draw
**Type:** C | **Tier:** 3 | **Core/Optional:** Core | **Time:** 30 min | **Goals:** 5
**Prerequisites:** Requires your PS1.1 LCG (same recurrence and parameters: $m=2^{31}-1$, $a=16{,}807$, $c=0$)
**Statement:**

Every non-uniform random draw your code has produced in this module ultimately traces back to a sequence of raw PRNG states. This problem asks you to make that chain visible, end to end, for a single draw.

Using your PS1.1 LCG, seeded at $X_0 = 777$, produce **one** draw from $N(0,1)$ via the following construction, logging every intermediate value as you go:

1. Advance the LCG one step to get state $X$; set $U_a = X/m$. Transform $U_a$ via inverse transform into a candidate value $Y = -\ln(U_a)$ — a draw from $\text{Exponential}(1)$, the distribution of $|{\rm Laplace}(0,1)|$, used here as the **candidate** for $|Z|$ (note: this makes step 2 below the same accept-reject test as PS1.3's Laplace proposal, restricted to $x \geq 0$).
2. Advance the LCG one more step to get a new state $X$; set $U_b = X/m$. Accept $Y$ as a draw from the half-normal (i.e., $|Z|$) if $U_b \leq \exp\left(-\frac{(Y-1)^2}{2}\right)$ (this is $f(Y)/(Mg(Y))$ simplified in closed form, with $M = \sqrt{2/\pi}\,e^{1/2}$, the same bound as PS1.3). If rejected, return to step 1 (advancing the LCG again for a fresh candidate).
3. Once accepted, advance the LCG one final step to get state $X$; set $U_c = X/m$. If $U_c < 0.5$, set $Z = -Y$; otherwise $Z = +Y$.
4. Report $Z$ — your one traced draw from $N(0,1)$.

Write this up as a **commented trace**: for every LCG state produced, show the state's integer value, the uniform derived from it, what it was used for (candidate generation, accept/reject test, or sign), and — for each accept/reject attempt — whether it was accepted or rejected and why (the numeric comparison). The narrative should read as a single continuous chain: PRNG state → uniform → transform → (possibly repeated) test → accepted draw.

**Deliverable:** the full commented trace under seed $X_0=777$ (every LCG state, every derived uniform, every accept/reject decision, the final sign decision, and the resulting $Z$); a 2–3 sentence summary connecting this to Goal 5 — i.e., stating explicitly which raw PRNG outputs your final $Z$ value is actually "made of."

**Verification:** [Tier 3, validation-log entry `PS1.4`]
Because every step of this chain derives from the same deterministic LCG (no library randomness anywhere in this problem), the entire trace is exactly reproducible given the seed. Under $X_0 = 777$, a correct implementation must reproduce: attempt 1 rejected (LCG state 13,059,039 → $U_a=0.006081$ → $Y=5.102572$; LCG state 439,936,479 → $U_b=0.204861$ vs. accept-ratio 0.000221 → reject); attempt 2 accepted (LCG state 226,205,932 → $U_a=0.105335$ → $Y=2.250606$; LCG state 797,043,934 → $U_b=0.371153$ vs. accept-ratio 0.457486 → accept); sign-flip (LCG state 2,061,892,399 → $U_c=0.960143 \Rightarrow$ sign $+$); **final $Z = +2.250606$**, using 5 total LCG steps. Match all logged states/uniforms to at least 6 decimal places and the final $Z$ to at least 6 decimal places.
**Discussion note:** *(folded)* The point of this problem isn't the specific value $2.2506$ — it's that this number is not "generated," in any mysterious sense; it is a fully determined function of six integers produced by one deterministic recurrence, run five times from one seed. If your trace disagrees with the logged one, work backwards: check $X_1 = (16807 \times 777) \bmod (2^{31}-1)$ first (a single, checkable arithmetic fact) — if that already disagrees, the bug is in the LCG step itself, not downstream. Note that the *number* of attempts before acceptance is itself random (though fully determined by the seed) — under a different seed you might see 1 attempt or several; the specific count of 2 (for seed 777) is a property of this seed, not a general guarantee. This problem deliberately reuses PS1.1's exact generator (per the module's interface note) rather than introducing a new one, so that the "foundation" in "traced back to its uniform foundation" is concretely the same foundation you already built and tested.

---

### PS1.5 — RANDU's hyperplane defect, and a seed-misuse failure
**Type:** D | **Tier:** 2+3 | **Core/Optional:** Core | **Time:** 45 min | **Goals:** 6
**Prerequisites:** Requires your PS1.1 LCG (reused for the seed-misuse half only; the RANDU generator is separately specified below)

**Statement:**

**Part 1 — RANDU.** RANDU is a linear congruential generator historically notorious for producing badly structured output. *(Its specific identification with the production generator once shipped by IBM under this name is not independently re-confirmed within this session — see the discussion note. The recurrence below is the one under study regardless.)* Implement it:
$$X_{n+1} = 65{,}539 \, X_n \bmod 2^{31}, \qquad U_n = X_n / 2^{31}.$$
Seed with $X_0 = 1$ (RANDU's period behavior depends on the seed being odd; a seed of 0 is degenerate for the same reason PS1.1's LCG was). Generate $n = 5{,}000$ draws and form every consecutive triple $(U_i, U_{i+1}, U_{i+2})$.

Rather than taking on faith that these triples show structure, **derive and check it directly**: compute, for every triple, $K_i = X_{i+2} - 6X_{i+1} + 9X_i$, and verify it is an exact integer multiple of $2^{31}$ for every single triple (this is an algebraic consequence of the specific multiplier $65{,}539 = 2^{16}+3$ — you can confirm the underlying identity $a^2 \equiv 6a - 9 \pmod{2^{31}}$ numerically for $a=65{,}539$ before trusting the consequence). Report how many *distinct* values of $k_i = K_i / 2^{31}$ you observe across your 4,998 triples — this count is the number of parallel planes your triples are confined to. Optionally, produce a 3D scatter of the triples and view it along the direction $(9,-6,1)$ to see the planes collapse visually.

**Part 2 — seed misuse.** Using your **PS1.1 LCG** (the well-tested generator, not RANDU), simulate a common real-world mistake: running 20 "independent" replications, each reseeded from a loop counter or similarly low-entropy source. Reseed with $X_0 = 1000, 1001, \dots, 1019$ (one run per seed), draw 50 values per run, and record each run's *first* draw. Compute the lag-1 correlation of these 20 first-draws across runs (i.e., correlate run $i$'s first draw against run $i+1$'s). Separately, repeat the same 20-run experiment but draw each run's seed from a well-separated source (e.g., a master RNG seeded once, drawing large well-spread integers) instead of a sequential counter, and compute the same cross-run correlation. Compare the two.

**Deliverable:** RANDU implementation; the identity check (confirmed exactly, with zero exceptions, or reported honestly if not); the count and values of distinct planes found; optionally the 3D-scatter plot; the seed-misuse comparison (both correlation values, both seeding strategies shown); a 3–5 sentence interpretation of the practical consequences of each failure mode.

**Verification:** [Tier 2 for the generator's stipulated definition; Tier 3 for both empirical findings, validation-log entry `PS1.5`]
- *Tier 2:* the recurrence itself ($a=65{,}539$, $c=0$, $m=2^{31}$) is this problem's own stipulated generator (design informed by R&C Ex. 2.10, the harvest's flagged standout example for this goal). The specific numeric parameters are not independently traceable to a source available in this project — R&C's book text is not a session input, and Ex. 2.10 is even-numbered/unsolved, so the arXiv companion carries no confirmable solution — and are presented as a stipulation, consistent with the historical-attribution flag below.
- *Tier 3, Part 1:* under $X_0=1$, $n=5{,}000$, the identity should hold with **zero exceptions**, and you should find **15** distinct plane indices (specifically $k \in \{-5,-4,\dots,9\}$) — confirmed by this session's own reference run, not asserted from memory, and confirmed seed-invariant across three additional calibration seeds.
- *Tier 3, Part 2:* your correlated-seed ("BAD") first-draw correlation should exceed **0.99** (in this construction it is exactly $1.0000$, a mathematical certainty for this seed range, not a statistical estimate); your well-separated-seed ("GOOD") correlation should be small, with $|r| \lesssim 0.46$ (a $2/\sqrt{19}$ noise band at 20 runs) — expect a value near, but not exactly, zero.
**Discussion note:** *(folded)* Two genuinely different failure modes live in this one problem. RANDU's defect is a property of the *generator itself* — no seeding discipline fixes it, because every possible seed produces triples confined to the same 15 planes — provable directly from the identity's bounds ($u_{n+2}-6u_{n+1}+9u_n \in (-6,10)$ for $u\in[0,1)$), and confirmed across multiple seeds at drafting time, though your own assigned run (seed $X_0=1$ only) doesn't by itself establish it for every seed. Seed misuse, by contrast, is a property of *how a perfectly good generator was used* — PS1.1's LCG passed every uniformity test you threw at it, and yet careless reseeding still produced "independent" runs that were, in the case demonstrated here, perfectly correlated. The lesson is not "always use a good generator" (necessary but insufficient) but "a good generator plus bad seeding practice is still broken." On the historical-attribution flag: the mathematical content of this problem (the identity, the plane count, the correlation figures) is fully verified by this session's own execution and does not depend on resolving that flag; it is surfaced only so the specific claim "this is literally what IBM shipped" is not silently treated as confirmed when it wasn't checked here.

---

### PS1.6 — Optional: sampling deep in a tail, the naive way and a better way
**Type:** V/D | **Tier:** 2+3 | **Core/Optional:** Optional | **Time:** 35 min | **Goals:** 4, 6
**Prerequisites:** None
**Statement:**

Target: the standard normal distribution truncated to $[4, \infty)$ — a deep right tail (only about 1 in 30,000 standard normal draws land here). This problem is a trimmed version of R&C Ex. 2.22's fuller multi-part treatment of truncated-normal generation (naive rejection, its tail inefficiency, and improved proposals); only the naive-vs-one-improved-proposal comparison is covered here.

**Naive method.** Draw $Z \sim N(0,1)$ (library sampler) and reject any draw with $Z < 4$; seeded at $2468$, run exactly $20{,}000{,}000$ attempts (vectorized generation recommended; expect roughly 600–700 acceptances at the true rate). Track the accepted count and compute the empirical acceptance rate = accepted / attempts. State the theoretical rate this should match: $P(Z\geq 4)$, computed via your language's standard normal CDF function (not recalled from memory — compute it).

**Improved method.** Use a shifted-exponential proposal for the tail: $g(x) = a\,e^{-a(x-a)}$ for $x \geq a$ (an $\text{Exponential}(\text{rate}=a)$ variate, shifted to start at $a$), with $a=4$. Derive the accept-reject bound: with unnormalized target $\tilde f(x) = e^{-x^2/2}$ for $x \geq a$, show that
$$\frac{\tilde f(x)}{g(x)} = \frac{1}{a}\, e^{-a^2/2}\, e^{-(x-a)^2/2},$$
which is maximized at $x=a$, giving $M = \frac{1}{a} e^{-a^2/2}$. Implement accept-reject using this proposal and bound (drawing the proposal via inverse transform is one line: $Y = a - \frac{1}{a}\ln(1-U)$ for $U\sim\text{Unif}(0,1)$). Run $20{,}000$ proposal attempts, seeded at $2468$; record the accepted count and empirical rate.

Compare the two empirical rates (as a ratio) and comment, in 2–3 sentences, on why a proposal specifically shaped for the tail region outperforms drawing from the whole distribution and discarding almost everything.

**Deliverable:** naive method's attempt count, accepted count, and empirical rate, plus the theoretical $P(Z\geq 4)$ your language computed; the $M$ derivation; the improved method's implementation, accepted count, and empirical rate; the ratio of the two rates; the comparison discussion.

**Verification:** [Tier 2 for both theoretical rates' derivation/computation; Tier 3 for the empirical confirmation, validation-log entry `PS1.6`]
- *Tier 2:* the naive rate is exactly $P(Z\geq 4)$, computable via your language's normal CDF (a citable, library-computable fact, not a number to recall). The improved bound $M = \frac{1}{a}e^{-a^2/2}$ is this problem's own closed-form derivation (shown above); the general accept-reject theorem underlying the acceptance-rate calculation is the same standard result used in PS1.3 (R&C Ex. 2.5).
- *Tier 3:* under a stated seed, at $20{,}000{,}000$ naive attempts your empirical rate should fall within **3.167×10⁻⁵ ± 3.78×10⁻⁶**; at $20{,}000$ improved-method attempts your empirical rate should fall within **0.9466 ± 0.0048**. The ratio of improved to naive acceptance rate should be on the order of $10^4$ (this session's reference runs observed 23,000×–32,000× across five independent trials).
**Discussion note:** *(folded)* The naive method isn't wrong, exactly — it's just spending nearly all of its 20 million draws generating values the problem doesn't want, and only accidentally landing in the target region about 1 time in 30,000. The improved proposal is shaped to put almost all of its mass exactly where the target's mass is (in the tail beyond $a$), so it wastes far less effort — this is the general lesson of good proposal design (echoing PS1.3's ranking discussion): match the proposal's shape to the target's shape *where the target actually has mass*, which for a deep tail means matching the tail's local behavior, not the distribution's overall shape. If your naive empirical rate is off by an order of magnitude, check you used a large enough attempt count — this is a rare-event probability, and both very small and very large empirical deviations are possible with insufficient attempts (this session's own log discloses exactly this sensitivity at a smaller attempt count that was tried and rejected in favor of the stated specification).

---

## Alignment matrix — Module 1

| Goal | Text | Problem(s) / justification |
|---|---|---|
| 1.1 | Explain why computers cannot produce true randomness and how pseudorandom number generators construct sequences that behave statistically as if random | PS1.1 (building and empirically testing an LCG from primitives is the concrete grounding for this explanatory goal; the conceptual questions instrument may address the explanatory framing more directly, per R2 — this goal's verb is "Explain," not an R2-mandatory implementation verb) |
| 1.2 | Describe the key structural properties of a good uniform PRNG — period length, seed dependence, and the statistical tests used to evaluate generator quality | PS1.1 (period/seed-dependence note, two uniformity tests) primary; PS1.5 (RANDU's structural failure; seed-misuse facet) as the negative-case reinforcement |
| 1.3 | Implement the inverse transform method for generating non-uniform random variates, and explain the conditions under which it is applicable | PS1.2 (both sub-parts). **Tier-fork resolution (recorded at draft time, per the M2-F3 convention):** part (a) resolved to **tier 1**, citing R&C Ex. 2.13 (solved, power-transform identity for the Pareto) rather than falling back to the tier-2 (2.2, unsolved) alternative offered in the WO — 2.13's construction was a clean, direct match to the brief with no adaptation strain. Part (b) is **tier 3** (original numerical-inversion construction on the standard normal; WO confirms no harvested candidate exists for this half of the goal) |
| 1.4 | Implement the acceptance-rejection method, explain where its efficiency comes from, and identify the factors that make a proposal distribution better or worse | PS1.3 (two proposals, ranked) primary; PS1.6 (optional — naive-vs-tail-shaped-proposal contrast) reinforcement |
| 1.5 | Trace a sample from an arbitrary distribution back to its uniform foundation — articulating the full generative chain from PRNG output to non-uniform draw | PS1.4 (Type C, full commented trace, reuses PS1.1's LCG per the module's interface note) |
| 1.6 | Recognize the practical consequences of poor RNG choices: reproducibility failures, period exhaustion, and correlation artifacts in simulation output | PS1.5 (Type D — RANDU's hyperplane defect covers "correlation artifacts" from a bad generator; the seed-misuse facet covers "reproducibility failures" from bad seeding practice, satisfying R6's diagnosis-problem requirement for the module) |

## Module 1 hours (per `PSDEP-F2Resolution.md`: core ≈ full §5 budget)

| Core problems | Core hours (row-sum re-verified) | Optional hours (uncounted) | Budget (§5) |
|---|---|---|---|
| 5 (PS1.1–PS1.5) | PS1.1 40 + PS1.2 45 + PS1.3 50 + PS1.4 30 + PS1.5 45 = **210 min = 3.50 hr** | PS1.6 ≈ 35 min | 3–4 hr |

Row-sum re-verified by hand against the WO's per-problem time caps (§3): 40+45+50+30+45 = 210 exactly, matching both the WO's stated "core ≈ 3.5 hrs" and the skeleton's pre-recorded planning figure — no arithmetic discrepancy found.


---

## Module 2 — Monte Carlo Estimation & Variance Reduction

### PS2.1 — Plain Monte Carlo integration and the n^(−1/2) rate
**Type:** I/V | **Tier:** 2 (estimand) + 3 (rate-plot slope) | **Core/Optional:** Core | **Time:** 45 min | **Goals:** 1, 2
**Prerequisites:** None

**Statement:**
Consider the definite integral
$$I = \int_0^1 e^x \, dx,$$
which can be written equivalently as $I = E[e^U]$ for $U \sim \text{Uniform}(0,1)$. This is a closed-form quantity (elementary calculus, fundamental theorem of calculus): $I = e - 1 \approx 1.718281828$.

The plain Monte Carlo estimator of $I$ draws $U_1, \dots, U_n$ i.i.d. $\text{Uniform}(0,1)$ and forms
$$\hat{I}_n = \frac{1}{n}\sum_{i=1}^n e^{U_i}.$$

Before writing any code, state briefly (a few sentences, with the supporting one-line derivations):
1. Why $\hat{I}_n$ is unbiased for $I$, and why it is consistent as $n \to \infty$.
2. The estimator's variance, $\mathrm{Var}(\hat{I}_n) = \sigma^2/n$ where $\sigma^2 = \mathrm{Var}(e^U)$, and what this implies about the *rate* at which the estimator's typical error should shrink as $n$ grows (i.e., the scaling of the standard error with $n$).

Then investigate that rate empirically. Set and report a random seed. For each sample size in the grid
$$n \in \{100,\ 300,\ 1000,\ 3000,\ 10{,}000,\ 30{,}000,\ 100{,}000,\ 300{,}000,\ 1{,}000{,}000\},$$
draw a **fresh, independent** set of $n$ uniforms (do not reuse draws across grid points, and do not use a single running/cumulative average across $n$ — each $n$ gets its own independent estimate) and compute $\hat{I}_n$ and the absolute error $|\hat{I}_n - I|$.

**Deliverable:**
- The one-paragraph derivation of unbiasedness, consistency, and the variance/rate argument requested above.
- Working code implementing $\hat{I}_n$ from primitives (loop or vectorized sum over draws from the language's uniform generator; no library "integrate" or "expectation" routines).
- A table or printout of $|\hat{I}_n - I|$ for each of the nine grid values of $n$.
- A log-log plot: $\log_{10}(n)$ on the horizontal axis, $\log_{10}|\hat{I}_n - I|$ on the vertical axis, with a fitted least-squares line through the nine points and its slope reported numerically.
- A 3–5 sentence interpretation connecting the fitted slope to the variance argument in point 2 above, and explicitly naming the rate ($n^{-1/2}$) that a plain Monte Carlo estimator's error obeys.

**Verification:**
- **Tier 2 (estimand):** $I = e - 1$ is an exact closed-form fact (fundamental theorem of calculus applied to $e^x$; equivalently, the exact mean of $e^U$ for $U\sim\text{Uniform}(0,1)$). No external citation is needed beyond this elementary derivation — verify your build against $2.718281828\ldots - 1 = 1.718281828\ldots$ to as many digits as your language's floating point gives you. (Annex cross-reference: `VerifiedTargetsAnnex.md` entry **A2.1** records that R&C Exercise 3.1's own worked target is *not* usable here — its published values are single-run Monte Carlo estimates with no closed form, not a reproducible tier-1 anchor — which is why this problem is built on the present closed-form integral instead. This fork resolution is recorded in `VerifiedTargetsAnnex.md` A2.1 (Fork-resolution field).)
- **Tier 3 (rate-plot slope):** your fitted slope should fall in **[-0.80, -0.20]**. This band is wider than a naive "should be $-0.5$" expectation because a *single* realization per grid point is genuinely noisy at the small-$n$ end of the grid (per WO-M2 §5's escalation note) — see validation-log entry **PS2.1** for the reference run and the 2000-seed calibration study that sets this band. A slope near 0 (error not shrinking) or a slope steeper than about $-1$ both indicate a implementation problem, not sampling noise.

**Discussion note:** *(folded — instructor-facing, no solution code)*
A correct implementation should show noisy but clearly decreasing error as $n$ grows, with the log-log slope landing in the stated band the large majority of the time — the calibration study found about 97.75% of independent single-run realizations on this exact grid land inside [-0.80, -0.20], with the extreme 0.5th/99.5th percentiles near -0.85/-0.14. Common failure modes: (a) accidentally computing a cumulative/running average across grid points instead of fresh independent draws per $n$, which correlates the errors and can distort the fitted slope in either direction; (b) mis-specifying the exponent or the domain of $U$ (e.g., drawing from $(-1,1)$ instead of $(0,1)$), which breaks the closed-form check immediately at any $n$; (c) an off-by-one or vectorization bug that silently uses $n-1$ or double-counts a draw, usually visible as a small but consistent bias that does not shrink with $n$. This problem establishes the module's baseline rate — PS2.2 through PS2.5 all reduce the *constant* in front of $n^{-1/2}$ without changing the exponent itself, which is exactly what those problems' write-ups should note explicitly (Goal 5's point, previewed here).

---

### PS2.2 — Antithetic variates and control variates: measured variance reduction
**Type:** I/V | **Tier:** 2 (estimands + structural identities) + 3 (achieved variance-reduction ratios) | **Core/Optional:** Core | **Time:** 60 min | **Goals:** 3
**Prerequisites:** None (may reuse your PS2.1 plain-MC code as the baseline, but this problem is self-contained if not)

**Statement:**
Both parts of this problem target the same estimand as PS2.1: $I = E[e^U] = e-1$ for $U\sim\text{Uniform}(0,1)$, so that the variance-reduction techniques below can be measured directly against the plain Monte Carlo baseline.

**(a) Antithetic variates.** For a *monotone* transform $h$ (here $h(u) = e^u$, increasing on $[0,1]$), the antithetic construction pairs each draw $U$ with its complement $1-U$. Implement:
$$\hat{I}_n^{\text{anti}} = \frac{1}{n/2}\sum_{i=1}^{n/2} \frac{e^{U_i} + e^{1-U_i}}{2}, \qquad U_1,\dots,U_{n/2} \overset{\text{iid}}{\sim} \text{Uniform}(0,1),$$
which uses $n/2$ independent uniform draws but still evaluates $h$ a total of $n$ times — the same total workload as the plain estimator on $n$ straight draws. Fix a total budget $n = 2000$.

**(b) Control variate.** Use $X = U$ itself as the control: $U$ is correlated with $e^U$ (since $e^u$ is increasing), and its mean is known exactly, $E[U] = 1/2$ (a standard fact about the Uniform(0,1) distribution — likewise $\mathrm{Var}(U) = 1/12$). On the same budget $n=2000$ draws, implement:
$$\hat{I}_n^{\text{cv}} = \overline{e^U} - \hat{c}\,(\bar{U} - \tfrac12), \qquad \hat{c} = \frac{\widehat{\mathrm{Cov}}(e^{U},U)}{\widehat{\mathrm{Var}}(U)}$$
estimating $\hat c$ from the same $n$ draws via the ordinary sample covariance and sample variance. (Note for your write-up, not something to solve analytically: estimating $\hat c$ from the same sample used for the estimate is standard practice and is what you should do here; it introduces no first-order bias since $E[\bar U - \tfrac12]=0$ regardless of $\hat c$.)

**For both (a) and (b):** repeat the *entire* estimator (not just the underlying draws) independently $R \geq 500$ times at the fixed budget $n=2000$ (recommended $R=1000$ for a stable reading), and likewise repeat the plain MC estimator from PS2.1's construction $R$ times at $n=2000$ as the common baseline. Compute the empirical variance across replications for each of the three estimators (plain, antithetic, control-variate).

**Deliverable:**
- Working code for the antithetic and control-variate estimators, built from primitives (only the language's uniform generator, arithmetic, and basic sample covariance/variance — no library "control variate" or "variance reduction" routines).
- The three empirical variances (plain, antithetic, control-variate) at $n=2000$, $R\geq500$, with your seed(s) reported.
- The two variance-reduction ratios: (plain variance) / (antithetic variance), and (plain variance) / (control-variate variance).
- 3–5 sentences total explaining the *structural condition* each technique exploits: for antithetic, why pairing a monotone transform's value with its complement induces negative correlation between the pair; for the control variate, why a known mean plus nonzero correlation with the target lets you subtract a zero-mean, variance-reducing correction term.

**Verification:**
- **Tier 2 (estimand and structural identities):** $I=e-1$ as in PS2.1 (closed form). The antithetic identity — for monotone $h$, the pairs $(h(U), h(1-U))$ are negatively correlated — is the textbook result of R&C Exercise 4.11, cited via **Annex A2.2** (`VerifiedTargetsAnnex.md`); that entry anchors this structural identity only, not any moment fact. $E[U]=\tfrac12$ and $\mathrm{Var}(U)=\tfrac1{12}$ are plain distributional facts about Uniform(0,1), citable to any standard probability reference — no annex entry is needed for these (consistent with A2.2's own note that moment facts don't require one). **Sourcing note:** the control variate here deliberately does *not* use the score-function construction (R&C Exercise 4.12) — Annex entry **A2.3** found no confirmable in-corpus named locus for the expected-score identity, so per the WO's R1a stop rule this problem uses the plain known-mean control ($X=U$) instead. Ex. 4.12 remains an instructor-facing, statement-only pointer and anchors nothing here (M2-F4).
- **Tier 3 (achieved variance-reduction ratios):** at $n=2000$ with $R\geq500$, your measured ratio should exceed **15× for antithetic** and **25× for the control variate** — one-sided thresholds set from an executed reference run and a calibration sweep across replication counts (see validation-log entry **PS2.2**), not exact targets to hit precisely. Ratios well above these thresholds (reference run: roughly 30× and 60× respectively) are expected and correct, not a sign of a mistake.

**Discussion note:** *(folded — instructor-facing, no solution code)*
This example is a deliberately dramatic illustration: because $e^{U}\cdot e^{1-U}=e$ is a constant (not merely correlated, but functionally linked), the antithetic pairing here achieves an unusually large reduction; and because $e^u$ is nearly linear in $u$ over $[0,1]$, its correlation with $U$ is very high ($\rho \approx 0.99$), giving the control variate an even larger reduction. Reference calibration (100–150 independent meta-runs at $R\in\{300,500,1000,2000\}$) found the antithetic ratio's worst case around 24× and the control-variate ratio's worst case around 43× — both comfortably above the 15×/25× thresholds stated to the student, which is why those thresholds are safe floors rather than tight targets. Students should not conclude from this example alone that antithetic/control-variate reductions of 30–60× are typical — PS2.7 (optional) and PS2.5's comparative study make clear that the achieved reduction is highly target- and statistic-dependent. Common failure modes: (a) in (a), pairing $U_i$ with $1-U_i$ but then treating the two as independent (n draws instead of n/2) — this silently changes the workload comparison and inflates the apparent variance reduction; (b) in (b), computing $\hat c$ from a *different, fresh* sample than the one used for the estimate — not wrong, but it changes the workload accounting relative to what's asked here, since a fresh pilot sample adds draws not shared with the plain-MC comparison; (c) forgetting that both ratios are expected to be very large for this particular $h$, and mistakenly "fixing" a correct large ratio.

---

### PS2.3 — The importance sampler (module export): bioassay posterior via prior proposal
**Type:** I | **Tier:** 1 | **Core/Optional:** Core | **Time:** 60 min | **Goals:** 4 (+1, 2 via the MCSE part)
**Prerequisites:** None. **This problem is exported:** package your solution as the four named functions below exactly as specified — Module 7's SIR problem will require them by name and by this problem's ID.

**Statement:**
You will build a small, reusable importance-sampling toolkit and validate it against a fixed, machine-checked test case (no randomness is involved in the check itself — the test inputs below are fixed numbers, not simulated draws).

**The model (bioassay dose–response, a classic small dataset reproduced here in full):**

| Dose group $i$ | log-dose $x_i$ | animals $n_i$ | deaths $y_i$ |
|---|---|---|---|
| 1 | −0.86 | 5 | 0 |
| 2 | −0.30 | 5 | 1 |
| 3 | −0.05 | 5 | 3 |
| 4 |  0.73 | 5 | 5 |

Each group's deaths are Binomial: $y_i \sim \text{Binomial}(n_i, \theta_i)$ with $\mathrm{logit}(\theta_i) = \alpha + \beta x_i$. The log-likelihood, given parameters $(\alpha,\beta)$, is
$$\ell(\alpha,\beta) = \sum_{i=1}^4 \Big[y_i \log\theta_i + (n_i-y_i)\log(1-\theta_i)\Big], \qquad \theta_i = \frac{1}{1+e^{-(\alpha+\beta x_i)}}.$$

**Prior (also the importance proposal):** $(\alpha,\beta)$ bivariate normal with $\alpha \sim N(0, 2^2)$, $\beta \sim N(10, 10^2)$, and $\mathrm{corr}(\alpha,\beta) = 0.6$.

**Target:** the posterior $p(\alpha,\beta\mid y) \propto \ell\text{-likelihood} \times \text{prior}$. Because the **importance proposal is the prior itself**, the log unnormalized importance ratio $\log[\text{target}/\text{proposal}]$ reduces to just the log-likelihood — the prior term cancels exactly. State this cancellation explicitly in your write-up (1–2 sentences): it is the reason `log_importance_ratios` below needs only the likelihood, not the prior density.

**Build these four functions, with exactly these names and signatures** (language-neutral — implement in whichever of Python/R/Julia you're using):
- `log_importance_ratios(theta_draws, data)` → vector of log unnormalized weights (i.e., the log-likelihood above, evaluated at each draw)
- `normalize_weights(log_ratios)` → normalized weights summing to 1 (subtract the max log-ratio before exponentiating, for numerical stability — do not exponentiate the raw log-ratios directly)
- `is_estimate(h_values, weights)` → the self-normalized IS estimate, $\dfrac{\sum_i w_i\, h(\theta_i)}{\sum_i w_i}$
- `is_ess(log_ratios)` → the importance-sampling effective sample size, $S_{\text{eff}} = 1/\sum_i \tilde w_i^2$ where $\tilde w_i$ are the *normalized* weights (the corrected form — see the Verification section's caveat)

Validate your four functions against this fixed 6-point test case (these are the actual $(\alpha,\beta)$ values to plug in — not a sample you draw yourself):
$$\alpha_{\text{test}} = (1.896,\ -3.6,\ 0.374,\ 0.964,\ -3.123,\ -1.581), \quad \beta_{\text{test}} = (24.76,\ 20.04,\ 6.15,\ 18.65,\ 8.16,\ 17.4).$$

Finally, using `is_ess` and the weighted variance of your test-case draws, compute the Monte Carlo standard error of the posterior-mean estimate, substituting $S_{\text{eff}}$ for the usual sample size $S$: $\mathrm{MCSE} = \sqrt{\mathrm{Var}_w[\theta]/S_{\text{eff}}}$, for both $\alpha$ and $\beta$.

**Deliverable:**
- The four named functions, implemented from primitives (arithmetic and the language's own exp/log — no library ESS, IS, or Bayesian-inference routines).
- The 1–2 sentence prior-cancellation explanation.
- The function outputs on the test case: the six log-ratios, the six normalized weights, the posterior-mean estimate of $(\alpha,\beta)$, the ESS, and the two MCSEs.
- 3–5 sentences: (a) what the test-case weights themselves already reveal about importance-weight degeneracy (look at how many of the six weights are essentially zero), and (b) how the MCSE compares to what you'd expect from a plain Monte Carlo estimator with the same *nominal* sample size (6) versus its *effective* sample size ($S_{\text{eff}}$) — this is the direct link back to Goals 1–2's error characterization.

**Verification:**
- **Tier 1 (all values below are machine-checked, cited via `VerifiedTargetsAnnex.md` entry A2.4** — no in-session fetch performed; the annex entry carries the original Aalto A4 test-input/output values):
  - Six log-ratios ≈ $(-8.95,\ -23.47,\ -6.02,\ -8.13,\ -16.61,\ -14.57)$ — agree to within 0.01.
  - Six normalized weights ≈ $(0.045,\ 0.000,\ 0.852,\ 0.103,\ 0.000,\ 0.000)$ — agree to within 0.001.
  - Posterior-mean estimate ≈ $(0.503,\ 8.275)$ — agree to within 0.01.
  - **ESS ≈ 1.354 — the keystone check** (Annex A2.4); note this is out of a *nominal* 6, i.e. $S_{\text{eff}}/6 \approx 0.226$, a stark illustration of weight degeneracy from just six draws.
  - MCSE ≈ 0.30 ($\alpha$) and ≈ 4.48 ($\beta$) — agree to **2 significant figures only**. Do not expect exact-digit agreement: per Annex A2.4's own finding, this specific value has drifted in its later decimal digits across different years of the source course's template even on this fixed test case, so it is cited as an approximate check, not an exact one.
  - **Provenance correction carried from the annex:** the "6-point test case" is six $(\alpha,\beta)$ parameter-draw pairs, not six bioassay observations — the bioassay dataset itself is the 4-row table above.
  - **Eq. 10.4 caveat (Annex A2.5):** if you consult BDA3's Eq. 10.4 for the ESS formula, note that the 1st/2nd printings contain an erroneous multiplier in the normalized-weight term; the corrected form is exactly the $S_{\text{eff}} = 1/\sum_i \tilde w_i^2$ given above. Citing the as-printed 1st/2nd-printing form would be a provenance error.

**Discussion note:** *(folded — instructor-facing, no solution code)*
This is the module's exported artifact: Module 7's SIR problem (PS7.1) will require these four functions by name, unchanged, on new data — do not treat this problem's dataset or prior as somehow "baked in" to the functions themselves; the functions must accept `theta_draws`/`data`/`log_ratios`/`weights` as arguments generically. A second forward pointer: Module 8 revisits effective sample size for MCMC chains (autocorrelation-based ESS rather than importance-weight-based ESS) — worth flagging to students that "ESS" will reappear with a different formula but the same underlying idea (how many *effectively independent* draws do I actually have). On the test case, note for students that three of the six weights round to 0.000 not because they are exactly zero but because they are many orders of magnitude smaller than the dominant weight (draw 3, weight 0.852) — this is exactly what "a few weights dominate" looks like numerically, and it previews the fuller diagnosis PS2.4 will require on a deliberately harder (light-tailed-proposal) configuration. Common failure modes: (a) exponentiating raw (very negative) log-ratios directly without the max-subtraction stabilization, causing underflow to all-zero weights; (b) computing the prior density and multiplying/dividing it back in (redundant, since it cancels, and a likely source of a sign or normalization slip); (c) using the *nominal* sample size (6) rather than $S_{\text{eff}}$ in the MCSE formula, which would understate the true Monte Carlo uncertainty.

---

### PS2.4 — Diagnosing importance-weight degeneracy: a light-tailed proposal on a heavy-tailed target
**Type:** D | **Tier:** 3 | **Core/Optional:** Core | **Time:** 45 min | **Goals:** 4
**Prerequisites:** None

**Statement:**
Suppose you want to use importance sampling to study a standard Cauchy target, with density
$$f(x) = \frac{1}{\pi(1+x^2)}.$$
Consider two candidate proposals:
- **Proposal A (light-tailed):** standard Normal, $g_A(x) = \frac{1}{\sqrt{2\pi}} e^{-x^2/2}$.
- **Proposal B (heavy-tailed):** a wider Cauchy, $g_B(x) = \dfrac{1}{2\pi\big(1+(x/2)^2\big)}$ (same family as the target, but scale 2 instead of 1).

Because the target's tails decay only polynomially ($\sim 1/x^2$) while $g_A$'s tails decay like $e^{-x^2/2}$, the ratio $f(x)/g_A(x)$ grows without bound as $|x|\to\infty$ — Proposal A is a light-tailed proposal for a heavy-tailed target, the textbook configuration for importance-weight degeneracy. Proposal B, by contrast, has tails of the *same order* as the target ($f(x)/g_B(x) \to \tfrac12$ as $|x|\to\infty$, a finite limit), so it should behave well.

For each proposal, and for **each of 10 independent seeds**, draw $N = 20{,}000$ samples from the proposal, compute the unnormalized importance weights $w_i = f(x_i)/g(x_i)$, normalize them, and compute:
- the effective sample size, $S_{\text{eff}} = 1/\sum_i \tilde w_i^2$, expressed as a percentage of $N$;
- the maximum normalized weight (the "max-weight share" — the fraction of total weight carried by the single largest weight).

**Deliverable:**
- Working code implementing both proposals' sampling and weight computation from primitives.
- A table of ESS/N (%) and max-weight share for both proposals across all 10 seeds.
- One weight histogram for a representative seed of each proposal (Proposal A and Proposal B), plotted on the same horizontal scale so the concentration difference is visually obvious.
- 3–5 sentences diagnosing the failure: connect what you observe (ESS collapse, its instability across seeds, and weight concentration) to the tail-mismatch mechanism described above — specifically, why an occasional proposal draw landing far in the tail (where the light-tailed proposal under-samples relative to the heavy-tailed target) receives a hugely inflated weight that can dominate the entire estimate.

**Verification:**
- **Tier 3 (executed reference run, logged):** see validation-log entry **PS2.4**. Your results should show the following qualitative-and-quantitative signature (not exact-value matches — the point is the pattern, not a specific number):
  - **Proposal B (healthy):** ESS/N should land in **[75%, 85%]** for every one of your 10 seeds, with the range across those 10 seeds no more than **2 percentage points** — i.e., stable. Max-weight share should stay **below 0.001 (0.1%)** for every seed.
  - **Proposal A (degenerate):** the **mean** ESS/N across your 10 seeds should be **below 30%**, and — this is the more telling signature — the **range** (max − min) of ESS/N across those same 10 seeds should **exceed 15 percentage points**. The instability itself, not just a low average, is the diagnostic signal. Max-weight share should **exceed 0.002 (0.2%)** in at least one of the 10 seeds.
  - These thresholds were set from an executed 60-seed calibration study with comfortable margin (Proposal A's mean ESS/N ranged 0.03%–44% across 60 independent seeds in the reference run; Proposal B's stayed within 79.8%–80.2% throughout).

**Discussion note:** *(folded — instructor-facing, no solution code)*
The underlying reason Proposal A cannot be stabilized by increasing $N$ within reason: $f(x)/g_A(x)$ grows like $e^{x^2/2}/x^2$, so $E_{g_A}[w^2]$ is analytically infinite — this is a genuine infinite-variance importance weight, not a finite-but-large-variance case that more draws would tame. That is exactly why the *instability across seeds* (not merely a low ESS in any one run) is the signature to emphasize with students: a single run's ESS can look deceptively OK-ish (the high end of the 60-seed calibration reached 44.18% at N=20,000) right next to a catastrophic one (the low end of that same calibration fell to 0.031%) — this variability is itself diagnostic of an ill-posed weight distribution, and students should be told explicitly not to average away or explain away a wildly-varying-across-seeds result as "bad luck." Contrast with Proposal B, whose same-tail-order construction keeps the weight ratio bounded, giving both a healthier ESS and — just as importantly — a *stable* one. Common failure modes: (a) running only a single seed and concluding Proposal A is "not that bad" because that one seed happened to land in the more benign part of its range; (b) forgetting to normalize weights before computing ESS or max-share (unnormalized weights make the max-share figure meaningless); (c) conflating this with PS2.3's degeneracy illustration — that one arose from a small nominal sample size (6) with a well-specified but concentrated posterior; this one arises from an outright proposal/target tail mismatch, a different mechanism worth distinguishing explicitly in the write-up.

---

### PS2.5 — Comparing variance-reduction techniques at a fixed budget
**Type:** V | **Tier:** 2 (estimand) + 3 (achieved variances and their ordering) | **Core/Optional:** Core | **Time:** 45 min | **Goals:** 5
**Prerequisites:** None (structurally similar to PS2.2 and PS2.4, but a new target)

**Statement:**
Estimate $p = P(Z>2)$ for $Z\sim N(0,1)$, a standard-normal upper-tail probability. This has a closed form, $p = 1-\Phi(2)$, computable to arbitrary precision from the standard normal CDF (any statistical software's `pnorm`/`norm.cdf`, or the error function) — not something to recall from memory, but a citable, exactly-computable special-function value: $p \approx 0.022750$.

Compare **three** variance-reduction techniques against the plain Monte Carlo baseline, **all at a fixed total workload budget of $n=5000$** (matching PS2.2's workload convention: antithetic uses $n/2$ independent draws for $n$ total evaluations; the others use $n$ draws directly):

1. **Plain:** $Z_i \sim N(0,1)$ iid, $\hat p = \text{mean}(\mathbb{1}[Z_i>2])$.
2. **Antithetic:** draw $n/2$ uniforms, form $Z_i = \Phi^{-1}(U_i)$ and its antithetic partner $-Z_i$ (since $\Phi^{-1}(1-u) = -\Phi^{-1}(u)$ by the normal quantile function's symmetry — this *is* the monotone-transform antithetic identity from PS2.2/Annex A2.2, since $\mathbb{1}[z>2]$ is monotone nondecreasing in $z$). Average $[\mathbb{1}(Z_i>2)+\mathbb{1}(-Z_i>2)]/2$ over the $n/2$ pairs.
3. **Control variate:** use $X=Z$ itself as the control ($E[Z]=0$, a plain distributional fact). Estimate $\hat c$ in-sample exactly as in PS2.2, and form $\hat p_{\text{cv}} = \text{mean}(\mathbb{1}[Z_i>2]) - \hat c\cdot\text{mean}(Z_i)$.
4. **Importance sampling:** sample instead from a proposal centered at the threshold, $Z_i \sim N(2,1)$, and reweight: $w(z) = \phi(z;0,1)/\phi(z;2,1) = \exp(-2z+2)$, giving $\hat p_{\text{is}} = \text{mean}\big(w(Z_i)\,\mathbb{1}[Z_i>2]\big)$.

*(Stratified sampling is not implemented here — per the module's scope, it is mentioned only conceptually: note in your write-up, in one sentence, how you would stratify this problem, e.g. by splitting $[0,\infty)$ and $(-\infty,0)$ or a finer partition, without implementing it.)*

For each of the four estimators, repeat the entire estimator independently $R=2000$ times at $n=5000$ and record the empirical variance across replications.

**Deliverable:**
- Working code for all three techniques plus the plain baseline, built from primitives.
- A variance-comparison table: the four empirical variances, and each technique's ratio to the plain baseline's variance.
- 3–5 sentences on the *mechanism* differences: why antithetic pairing barely helps here (think about what the paired event $\{Z>2\}\cap\{-Z>2\}$ requires, and how often it can possibly occur), why the control variate helps modestly and reliably, and why importance sampling helps dramatically for *this specific kind* of target (a rare-event probability) by concentrating draws where the indicator is more often 1.
- One explicit sentence noting that **none of these techniques changes the underlying $n^{-1/2}$ convergence rate** — they change the constant multiplying it, not the exponent (tying back to PS2.1's baseline).

**Verification:**
- **Tier 2 (estimand):** $p=1-\Phi(2)\approx 0.022750$, a standard, exactly-computable special-function value — no external citation needed beyond stating it as a standard normal-distribution fact.
- **Tier 3 (achieved variances and their ordering, executed + logged — see validation-log entry PS2.5):** at $n=5000$, $R=2000$, your variance-reduction ratios (plain variance ÷ technique variance) should satisfy:
  - **Antithetic:** ratio in **[0.75, 1.35]** — i.e., close to 1. This is *not* a weak check, it's the honest result: the true population-level effect here is only about +2.4%, small enough that it can occasionally even read slightly *below* 1 due to replication noise. A ratio anywhere in this band is correct.
  - **Control variate:** ratio **> 0.95** — modest but real; expect something in the neighborhood of 1.05–1.30.
  - **Importance sampling:** ratio **> 10** — expect something in the neighborhood of 15–20, dramatically larger than the other two.
  - **Ordering:** importance sampling's variance should be far below control variate's, which should be at or modestly below antithetic's and plain's (which should be close to each other).

**Discussion note:** *(folded — instructor-facing, no solution code)*
This problem is deliberately built so the three techniques do *not* perform similarly — unlike PS2.2's dramatic e^U example, this is a case where the mechanism-target mismatch is real and instructive. Analytically (sanity-checked against the executed run, not given to students as the target): the antithetic ratio is exactly $(1-p)/(1-2p)\approx 1.024$, because the joint event "both $Z>2$ and $-Z>2$" is impossible for $c=2>0$, so the achievable negative correlation is bounded by $-p^2$ — tiny, since $p$ itself is tiny. The control variate's optimal-$c$ ratio is $1/(1-\rho^2)\approx 1.151$ where $\rho^2 = \phi(2)^2/[p(1-p)]\approx 0.131$ — a genuine, moderate correlation between $Z$ and the indicator. Importance sampling wins decisively because it directly addresses *where the budget is spent*: half of the proposal's draws now land above the threshold, versus only ≈2.3% under the plain sampler, which is exactly the lever a rare-event problem needs. Students should walk away recognizing this as the central lesson of Goal 5: these are mechanistically distinct interventions, and which one helps — and by how much — depends on the specific structure of the target and the statistic, not a fixed hierarchy of "better" techniques. A student who reports "antithetic did nothing" is not reporting a bug; a student whose antithetic ratio happens to land at 0.9 should say so plainly rather than "fixing" it. Common failure modes: (a) expecting antithetic to show a large reduction because it did in PS2.2, and treating a near-1 ratio as an implementation error; (b) forgetting the fixed-workload accounting for antithetic (n/2 draws, not n); (c) computing the IS weight with the wrong sign in the exponent (should shrink weight for draws far from the target region, not grow it).

---

### PS2.6 — Optional: resampling from importance weights (a preview of SIR, Module 7)
**Type:** C | **Tier:** 2 (theoretical motivation) + 3 (executed agreement check) | **Core/Optional:** Optional | **Time:** 30 min | **Goals:** 6
**Prerequisites:** Requires your PS2.3 importance sampler (the four named functions)

**Statement:** *This problem is a preview of Sampling Importance Resampling (SIR), which Module 7 formalizes as a full approximate-sampling method (PS7.1 — built on your PS2.3 functions; this problem is an optional preview of the same resampling pattern, not a prerequisite). Do not implement or explain any MCMC machinery here — this is strictly the importance-sampling-to-resampling bridge.*

Reusing your PS2.3 functions and the same bioassay model, prior, and proposal, draw a **real** sample of $N=4000$ pairs $(\alpha,\beta)$ from the prior (not the fixed 6-point test case this time). Compute the log importance ratios, normalize the weights, and compute the self-normalized IS estimate of the posterior mean of $(\alpha,\beta)$ using `is_estimate`.

Then **resample with replacement**, $M=4000$ times, from your $N=4000$ draws — using the normalized importance weights as the resampling probabilities. This produces a new pseudo-sample that behaves *as if drawn from the posterior* rather than the prior, even though every value in it came from your original prior draws. Set and report a single random seed before drawing your $N=4000$ sample; use the same seed context for the $M=4000$ resampling step (or set and report a second seed for it), so your full run is reproducible from your write-up.

**Deliverable:**
- Code performing the $N=4000$ draw, weight computation, and weighted resampling, reusing your PS2.3 functions unchanged.
- The IS-weighted posterior-mean estimate (from `is_estimate`) and the plain empirical mean of the resampled sample, for both $\alpha$ and $\beta$.
- Two histograms side by side (or overlaid): the raw prior draws' distribution vs. the resampled distribution, for one of the two parameters (your choice) — the resampled histogram should visibly concentrate around the posterior region rather than spanning the prior's full spread.
- 3–5 sentences: does the resampled sample's mean agree with the IS-weighted estimate? What does the resampled histogram's shape (versus the prior's) tell you about what resampling accomplished? Explicitly label this as a **preview of SIR (Module 7)** in your write-up, and note in one sentence what ESS-for-MCMC (Module 8) will later have in common with the ESS you computed here.

**Verification:**
- **Tier 2 (theoretical motivation):** the idea that resampling with replacement from normalized importance weights produces a sample that behaves as if drawn from the target is the subject of R&C Exercises 3.6 and 3.16 — both **unsolved** in the published solutions (both even-numbered), so no numeric target or solution text is available from them; they are cited here only as the conceptual basis for the construction, not as a source of any checkable value.
- **Tier 3 (executed agreement check — see validation-log entry PS2.6):** your resampled-sample mean should agree with your IS-weighted estimate to within **0.15 for $\alpha$** and **0.6 for $\beta$**. These thresholds carry roughly 2.5× margin over an executed 150-seed calibration study's observed worst case, because this check stacks two independent layers of Monte Carlo noise (the importance draw and the resampling draw).

**Discussion note:** *(folded — instructor-facing, no solution code)*
Expect ESS around 25–35% of $N=4000$ for this model — degenerate relative to a perfectly efficient sampler, but far healthier than PS2.3's 6-point test case (≈22.6%) or PS2.4's pathological configuration, since a real 4000-draw prior sample gives the importance sampler many chances to place mass near the posterior. The point of this problem is specifically the *mechanism*, not achieving a particularly clean numeric match: resampling trades the deterministic weighted-average estimate for a genuine (if noisier) pseudo-sample from the target, which is exactly the object SIR needs downstream (you cannot run further computations "on" a set of importance weights the way you can on an actual sample of draws — Gibbs, MH, and later diagnostics all expect draws, not weights). Common failure modes: (a) resampling from the *raw* (unnormalized) weights rather than the normalized ones, which numpy's `choice`-style functions will typically reject or silently mis-handle; (b) forgetting to compare against the *IS-weighted* estimate (the correct target) rather than the naive unweighted prior-sample mean (which would NOT be expected to agree, since it ignores the likelihood entirely).

---

### PS2.7 — Optional: when antithetic variates don't help — a non-monotone statistic
**Type:** V | **Tier:** 2 (estimand) + 3 (executed variance ratio) | **Core/Optional:** Optional | **Time:** 30 min | **Goals:** 3, 5
**Prerequisites:** Builds on PS2.2(a)'s antithetic code (same pairing construction, a different $h$)

**Statement:**
PS2.2(a) worked because $h(u)=e^u$ is *monotone* — the structural condition Annex A2.2's identity requires. This problem asks what happens when that condition is dropped. Consider
$$h(u) = (u-0.5)^2, \qquad I = E[h(U)] = \mathrm{Var}(U) = \tfrac{1}{12}, \quad U\sim\text{Uniform}(0,1)$$
(a standard distributional fact — no citation beyond this needed). Notice $h$ is **symmetric about $u=0.5$**: $h(1-u) = h(u)$ for every $u$ — not merely uncorrelated with its antithetic partner, but *identical* to it.

Implement the plain estimator and the antithetic estimator exactly as in PS2.2(a) (same pairing construction, fixed total workload $n=2000$, $R=2000$ replications), but with this $h$ in place of $e^u$.

**Deliverable:**
- Code for both estimators (largely a copy of PS2.2(a)'s structure with $h$ swapped).
- The two empirical variances and their ratio (plain ÷ antithetic).
- 3–5 sentences: what do you observe, and why does the exact symmetry $h(1-u)=h(u)$ break the mechanism that made antithetic pairing work in PS2.2(a)? (Hint for your own reasoning, not to be taken on faith: think about what the "pair average" $[h(U)+h(1-U)]/2$ actually equals when the two terms are identical, and what that implies about how much independent information $n/2$ pairs actually carry compared to $n$ independent plain draws.)

**Verification:**
- **Tier 2 (estimand):** $I=\mathrm{Var}(U)=1/12$, a plain distributional fact about Uniform(0,1) (no annex entry needed, consistent with Annex A2.2's own note on moment facts).
- **Tier 3 (executed variance ratio — see validation-log entry PS2.7):** your ratio (plain variance ÷ antithetic variance) should fall in **[0.35, 0.65]** — notably **below 1**, meaning antithetic pairing is *worse* than plain Monte Carlo here, not merely unhelpful. This is a tight, confidently-set band: unlike PS2.5's antithetic case (a small, noisy true effect), this one rests on an exact algebraic identity ($h(1-u)\equiv h(u)$), so the true population ratio is exactly $0.5$ and the calibration spread around it is small.

**Discussion note:** *(folded — instructor-facing, no solution code)*
The mechanism failure is exact, not approximate: because $h(1-u)\equiv h(u)$, the "pair average" $[h(U_i)+h(1-U_i)]/2$ collapses to $h(U_i)$ itself — you have paid for $n$ evaluations but only ever learn $n/2$ independent facts about $h$, exactly halving your effective sample size relative to a plain $n$-draw estimator. This is the cleanest possible illustration that antithetic variance reduction is *not* a free property of pairing $U$ with $1-U$ — it specifically requires the negative-correlation structure that monotonicity guarantees (Annex A2.2), and a symmetric $h$ is close to a worst case rather than a neutral one. Frame this for students as completing the module's Goal 3/5 picture: PS2.2(a) showed antithetic variates working dramatically; PS2.5 showed them barely working on a different, non-symmetric but non-monotone-friendly target; this problem shows them actively backfiring on a symmetric target. Common failure modes: (a) not noticing the exact algebraic identity and instead treating the observed ratio as "just noisy," missing the deterministic explanation; (b) accidentally implementing $h(1-u)$ with a sign error that breaks the exact-symmetry check (verify $h(1-u)=h(u)$ numerically before running the variance comparison, as the reference run does).

---

## Alignment matrix — Module 2

*(Per `ProblemSets_draft_skeleton.md` stub, filled per `ProblemSetRequirements1_1.md` R2. Goal 6's justification line is carried verbatim from WO-M2's ratified slate instruction, M2-F1.)*

| Goal | Text | Problem(s) / justification |
|---|---|---|
| 2.1 | Derive the Monte Carlo estimator from first principles and characterize its error — establishing why the method works and what governs the rate at which accuracy improves with sample size | **PS2.1** (primary: derivation + n^(−1/2) log-log rate verification). Reinforced by PS2.3's MCSE part (Goal 1/2 tie-in). |
| 2.2 | Explain the role of variance in Monte Carlo error and articulate why reducing variance is equivalent to getting more information from the same computational budget | **PS2.1** (variance/rate argument in the derivation step). **PS2.3** (MCSE-with-$S_{\text{eff}}$ part makes the "effective sample size = effective information" point concrete). |
| 2.3 | Implement and explain antithetic variates and control variates as principled modifications to the basic estimator, identifying the structural conditions that make each effective | **PS2.2** (primary: both techniques implemented, structural conditions stated). **PS2.7** (optional: the same structural condition shown to fail on a non-monotone statistic — completes the picture). |
| 2.4 | Implement importance sampling, explain the reweighting mechanism, and identify the conditions under which importance weights become pathological | **PS2.3** (primary: the exported importance sampler, reweighting mechanism, weight-degeneracy visible even in the test case). **PS2.4** (Type D: dedicated empirical diagnosis of pathological weights under a light-tailed proposal, per R6). |
| 2.5 | Recognize antithetic variates, control variates, stratification, and importance sampling as mechanistically distinct interventions in the same underlying error quantity — each reducing variance by a different structural means, none changing the fundamental $n^{-1/2}$ convergence rate | **PS2.5** (primary: ≥3-technique comparative study at fixed budget, explicit $n^{-1/2}$-invariance note). Stratified sampling appears only as PS2.5's required one-sentence conceptual mention, per the module's constraint (no standalone implementation). PS2.1's discussion note previews the rate-invariance point PS2.5 makes explicit. |
| 2.6 | Recognize importance sampling as a reweighting idea with scope beyond variance reduction — specifically, that resampling from importance weights produces an approximate sample from the target, laying the groundwork for SIR in Module 7 | **PS2.6 (optional only)** — per WO-M2's ratified slate instruction (M2-F1): Goal 6 is a *Recognize* goal exercised operationally only in optional PS2.6, backed by the conceptual questions and the spec's own permissive "may" (§6: "A Type C problem **may** end with resampling from importance weights as a forward hook to SIR"); deliberately not placed in core. |

## Module 2 hours (reconciled from row sums)

| Core problems | Core hours (row sum) | Optional hours (row sum, uncounted) | Budget (§5) |
|---|---|---|---|
| 5 (PS2.1–PS2.5: 45+60+60+45+45 = 255 min) | **4.25 hr** | PS2.6 (30) + PS2.7 (30) = 60 min = **1.00 hr** | 4–5 hr |

Core total matches WO-M2 §3's stated 255 min exactly; within the §5 budget as drafted, consistent with `PSDEP-F2Resolution.md`.

---

## Module 3 — Bootstrap & Resampling

### PS3.1 — The bootstrap, from primitives, on a real-world-shaped dataset
**Type:** I | **Tier:** 1+3 | **Core/Optional:** Core | **Time:** 45 min | **Goals:** 1, 2
**Prerequisites:** None

**Statement:**

Two datasets below represent repair times (in some time unit) for two groups of customers of a telecommunications carrier — a large group (ILEC, the incumbent carrier's own customers) and a small group (CLEC, a competitor's customers whose repairs the incumbent was contractually obligated to service). Both distributions are strongly right-skewed, as repair-time data typically is. *(Note on provenance: these are synthetic datasets constructed to match the summary statistics of a well-known published bootstrap teaching example — Hesterberg (2015), Sec. 1.1 — not the original raw repair-time records, which are not reproduced here. The published mean/SE/interval figures cited below are real; the individual data values are not.)*

**CLEC group (n = 23)** — use exactly these 23 values:

```
0.4, 11.3, 11.6, 44.5, 0.1, 51.1, 12.2, 12.1, 35.5, 56.7, 4.1, 0.1,
2.1, 52.7, 7.6, 42.6, 0.7, 3.2, 3.3, 1.6, 1.2, 14.4, 10.2
```

**ILEC group (n = 1,664)** — generate your own sample: draw 1,664 values from a Gamma distribution with shape parameter 0.3282 and scale parameter 25.625 (this gamma choice reproduces the published ILEC mean ≈ 8.41 and SE-of-mean ≈ s/√n ≈ 0.36). Set and report your own seed.

Implement the **nonparametric bootstrap** for the sample mean **from primitives**: write your own loop that (i) draws $n$ indices with replacement from $\{1,\dots,n\}$ using your language's uniform RNG, (ii) forms the resample, (iii) computes the resample mean, and (iv) repeats this $r=10{,}000$ times to build the bootstrap distribution. Do not call a library bootstrap routine (e.g., `boot()` in R, `scipy.stats.bootstrap`) — the resampling loop itself is the thing Goal 2 asks you to implement.

For each group, compute:
1. The bootstrap standard error (the sample SD of your $r$ bootstrap means).
2. The 95% bootstrap percentile interval (the 2.5th and 97.5th percentiles of your bootstrap distribution).
3. The classical formula estimate $s/\sqrt{n}$ (using the usual $n-1$ divisor for $s$).

Then verify the **narrowness-bias relation** (Hesterberg 2015, Sec. 3.2): the (exhaustive/theoretical) bootstrap SE for the sample mean is smaller than $s/\sqrt{n}$ by a factor of exactly $\sqrt{(n-1)/n}$ — because the empirical distribution's plug-in variance uses an $n$-divisor, not $n-1$. Check whether your bootstrap SE is close to $s/\sqrt n \cdot \sqrt{(n-1)/n}$ for the CLEC group.

Finally, write 3–5 sentences explaining *why* resampling with replacement from the observed data simulates the process of drawing a fresh sample from the population — i.e., state the plug-in principle in your own words and identify what is being substituted for what.

**Deliverable:** your bootstrap code (from-scratch resampling loop); a small table reporting, for each group, the bootstrap SE, the 95% percentile CI, $s/\sqrt n$, and the narrowness-relation check; 3–5 sentences on the plug-in principle.

**Verification:** [Tier 1 + Tier 3]
- **Tier 1** (cite `VerifiedTargetsAnnex.md` Annex A3.1, sourced to Hesterberg (2015), confirmed against the article text) — for context only, the published analysis reports: CLEC mean 16.50913, bootstrap SE 3.961816, 95% percentile CI (10.09, 25.41); ILEC mean 8.41161, bootstrap SE 0.357599. These are the article's own figures on the real data, not targets your synthetic-mirror run is expected to hit.
- **Tier 3** (basis: `ValidationLog` entry **PS3.1**'s logged synthetic-mirror run, `reference_impls/ps3_1_ref.py` — not the Annex): as *approximate* targets for this synthetic mirror (a different realization matching the published summary statistics, not the original data, so expect proximity rather than exact match) — CLEC bootstrap SE should be roughly in **[3.5, 4.6]**; CLEC 95% percentile CI should have its lower bound roughly in **[8, 10]** and upper bound roughly in **[23, 26]**; ILEC bootstrap SE should be roughly in **[0.28, 0.45]**; your own generated ILEC sample mean should land roughly in **[7.3, 9.5]**. This synthetic mirror matches the published mean and SE closely but was not tuned to reproduce the published interval shape.
- **Tier 1**, narrowness relation: your CLEC bootstrap SE should be within about ±10% of $s/\sqrt n \cdot \sqrt{(n-1)/n}$.
- **Tier 1**, two-arm contrast: your CLEC bootstrap SE should be at least 8× your ILEC bootstrap SE (reflecting the sample-size asymmetry — this is the point of using two arms of very different size).
- **Tier 3**: reference run and full tolerance derivation logged at `ValidationLog` entry **PS3.1** (`reference_impls/ps3_1_ref.py`).

**Discussion note:** (folded guidance; no solution code) A correct implementation should show the CLEC bootstrap distribution is much wider than ILEC's — driven almost entirely by the ~72× difference in sample size, not by a difference in how skewed the two underlying populations are. A common error is calling a library bootstrap function instead of writing the resample loop — this technically produces a similar-looking number but doesn't exercise Goal 2's "implement." Another common miss: forgetting that the percentile CI is read directly off the bootstrap distribution's quantiles, not computed from a formula. On the narrowness check: this factor is *exact* for the theoretical (infinite-resample) bootstrap of the mean; your Monte Carlo bootstrap at r=10,000 will be close but not identical, because of ordinary Monte Carlo noise on top of the exact plug-in relation — both sources of variation exist simultaneously and shouldn't be conflated (a preview of PS3.6's theme).

---

### PS3.2 — Parametric vs. nonparametric bootstrap
**Type:** I | **Tier:** 2+3 | **Core/Optional:** Core | **Time:** 40 min | **Goals:** 2
**Prerequisites:** None (independent of PS3.1, though it reuses the resampling-loop skill)

**Statement:**

Generate a synthetic sample of $n=20$ values from an Exponential distribution with mean 10 (i.e., rate $=0.1$). Set and report your seed. This is a case where the *true* generative family is known to you (by construction) — a situation that never quite holds with real data, but which lets you check both bootstrap methods against a closed-form fact.

**Nonparametric bootstrap:** as in PS3.1, resample your 20 values with replacement, $r=10{,}000$ times, and compute the bootstrap SE of the mean.

**Parametric bootstrap:** fit the exponential model to your data by computing $\hat\lambda = 1/\bar x$ (the MLE for an exponential rate). Then simulate $r=10{,}000$ **new** samples of size $n=20$, each drawn from $\text{Exponential}(\text{rate}=\hat\lambda)$ — not resampled from your original data — and compute the mean of each simulated sample. The SD of these $r$ simulated means is your parametric bootstrap SE.

Compare the two SEs, and compare each to what theory says it should be (see Verification). Write 3–5 sentences on what the parametric assumption buys you here (why might the parametric bootstrap SE be more stable/trustworthy when the assumed family is right?) and what it risks (what happens to this procedure if the true population were not exponential at all?).

**Deliverable:** your parametric and nonparametric bootstrap code; both SEs reported alongside their respective closed-form/plug-in targets; 3–5 sentences on the parametric tradeoff.

**Verification:** [Tier 2 + Tier 3]
- **Tier 2** (closed-form distributional fact — for an Exponential distribution, the SD equals the mean, so the SE of the sample mean is exactly $\text{mean}/\sqrt n$; no external citation needed beyond this standard fact): your **parametric** bootstrap SE should be within about **±8%** of $\bar x/\sqrt n$ (your own sample mean, standing in for the fitted rate). Your **nonparametric** bootstrap SE should be within about **±8%** of $(s/\sqrt n)\cdot\sqrt{(n-1)/n}$ (the same H-3 narrowness relation from PS3.1, on different data).
- As a **loose sanity check only** (not a precise target): your two bootstrap SEs should typically be within about a factor of 2 of each other — if they differ by much more than that, check your parametric simulation is drawing from the *fitted* distribution and not accidentally reusing the original data.
- **Tier 3**: reference run logged at `ValidationLog` entry **PS3.2** (`reference_impls/ps3_2_ref.py`) — confirms both ratio-checks hold to within ~2% across 20 independent replications, and documents why no single fixed numeric target for either raw SE is appropriate at this sample size.

**Discussion note:** (folded guidance; no solution code) Do NOT expect the parametric and nonparametric SEs to agree closely — at $n=20$ they can differ by up to roughly 30%, because the parametric SE tracks only $\bar x$ (via the fitted rate) while the nonparametric SE tracks the full empirical shape (via $s$), and these need not move in lockstep at small $n$. This is itself the lesson: the parametric bootstrap "buys" a smoother, more theoretically-grounded SE *if* the assumed family is correct, at the risk of that assumption being wrong (with real data, you would never know for certain that the population is exactly exponential). Students sometimes bootstrap the *original data* under the parametric label by mistake (i.e., they resample instead of re-simulating from the fitted model) — check that the parametric step calls the distribution's own random-generation routine with the fitted parameter, not the resample-with-replacement operation from PS3.1.

---

### PS3.3 — The accuracy hierarchy, made visible: a coverage experiment
**Type:** V | **Tier:** 1+3 | **Core/Optional:** Core | **Time:** 75 min | **Goals:** 2, 3
**Prerequisites:** the resampling-loop skill from PS3.1 (no code reuse required, just familiarity)

**Statement:**

The goal of this problem is to make an accuracy *hierarchy* visible in your own simulation output, rather than simply asserting that one CI method is better than another. You will compare **three** methods: bootstrap percentile, bootstrap-t, and BC$_a$ (bias-corrected and accelerated).

Population: Exponential with rate $=1$ (true mean $=1$). This is deliberately a **skewed** population — Hesterberg (2015, Sec. 4.4) shows that CI accuracy differences between bootstrap methods are much starker for skewed populations than symmetric ones.

For each sample size $n$ in the grid $\{8, 15, 30, 60\}$, repeat the following $1{,}000$ times: draw a fresh sample of size $n$ from Exponential(rate=1); draw $r=2{,}000$ bootstrap resamples of it; construct all **three** 95% CIs for the mean from that one set of bootstrap resamples (no need to redraw resamples per method); record whether each interval contains the true mean (1). Set and report the seed(s) you use to drive both the sample draws and the bootstrap resampling.

1. **Bootstrap percentile CI:** the 2.5th and 97.5th percentiles of the $r$ bootstrap means, as in PS3.1.
2. **Bootstrap-t CI:** for each bootstrap resample, compute its own mean $\hat\theta^*_b$ and its own formula SE $\text{SE}^*_b = s^*_b/\sqrt n$ (a formula SE is available for the mean — no nested/iterated bootstrap needed, per Hesterberg 2015 Sec. 4.6). Form $t^*_b = (\hat\theta^*_b - \hat\theta)/\text{SE}^*_b$, take the $\alpha/2$ and $1-\alpha/2$ quantiles of the $t^*_b$ distribution, and construct the interval as $(\hat\theta - q_{1-\alpha/2}\cdot\text{SE},\ \hat\theta - q_{\alpha/2}\cdot\text{SE})$, where SE is the *original* sample's $s/\sqrt n$ (note the endpoint reversal — easy to get backwards).
3. **BC$_a$ CI** (Efron & Tibshirani 1993, Ch. 14, Sec. 14.3): unlike the percentile interval, which always uses the $\alpha/2$ and $1-\alpha/2$ percentiles of the bootstrap distribution, BC$_a$ uses two *adjusted* percentile levels $\alpha_1,\alpha_2$ that shift to correct for bias and skewness:
$$
(\hat\theta_{\text{lo}}, \hat\theta_{\text{up}}) = \left(\hat\theta^{*(\alpha_1)},\ \hat\theta^{*(\alpha_2)}\right), \qquad
\alpha_1 = \Phi\!\left(\hat z_0 + \frac{\hat z_0 + z^{(\alpha/2)}}{1-\hat a(\hat z_0+z^{(\alpha/2)})}\right), \quad
\alpha_2 = \Phi\!\left(\hat z_0 + \frac{\hat z_0 + z^{(1-\alpha/2)}}{1-\hat a(\hat z_0+z^{(1-\alpha/2)})}\right)
$$
where $\hat\theta^{*(\alpha_1)}$ denotes the $100\alpha_1$-th percentile of your bootstrap distribution, $\Phi$ is the standard normal CDF, $z^{(p)}=\Phi^{-1}(p)$, and $\alpha=0.05$ is the same overall miscoverage rate used throughout this problem — so $z^{(\alpha/2)}=z^{(0.025)}\approx-1.960$, matching the percentile and bootstrap-t sections above. Two numbers must be estimated from your data:
- **Bias-correction** $\hat z_0 = \Phi^{-1}\!\left(\#\{\hat\theta^*_b < \hat\theta\}/r\right)$ — the (inverse-normal-transformed) proportion of your bootstrap means falling below the original sample mean.
- **Acceleration** $\hat a$, via the **jackknife**: let $\hat\theta_{(i)}$ be the sample mean with the $i$-th observation deleted ($n$ such leave-one-out means), and $\hat\theta_{(\cdot)}$ their average. Then
$$
\hat a = \frac{\sum_{i=1}^n (\hat\theta_{(\cdot)} - \hat\theta_{(i)})^3}{6\left(\sum_{i=1}^n (\hat\theta_{(\cdot)} - \hat\theta_{(i)})^2\right)^{3/2}}.
$$

**Sanity check before trusting your BC$_a$ code:** if you artificially force $\hat a=\hat z_0=0$, the formula above must reduce *exactly* to the percentile method's $\alpha_1=\alpha/2,\ \alpha_2=1-\alpha/2$ (E&T Eq. 14.11). Confirm this numerically before using your implementation for anything else.

Compute the empirical **coverage rate** and **mean CI width** for each of the three methods at each $n$. Plot coverage vs. $n$ for all three methods on the same axes, with a horizontal reference line at nominal 0.95. Also plot (or tabulate) mean width vs. $n$.

Write 3–5 sentences describing the pattern you see — where does BC$_a$ sit relative to the other two, and does that match the theoretical claim that BC$_a$ is *both* transformation-respecting (like percentile) *and* second-order accurate (like bootstrap-t)?

**Deliverable:** your coverage-experiment code (including the BC$_a$ sanity check); a table or plot of coverage vs. $n$ and width vs. $n$ for all three methods; 3–5 sentences of interpretation.

**Verification:** [Tier 1 + Tier 3]
- **Tier 1** (cite Annex A3.1 / Hesterberg 2015 Sec. 4.4, as a **qualitative** anchor only — the article's own numeric thresholds are article-scale, not student-scale, per the WO's escalation note): your bootstrap-t coverage should be visibly closer to the nominal 0.95 than your percentile coverage at small $n$, and the gap between the two methods should shrink as $n$ grows.
- **Tier 1** (cite E&T 1993 Ch. 14 Sec. 14.3, owner-supplied source, confirmed against the text): the sanity check ($\hat a=\hat z_0=0 \Rightarrow$ BC$_a$ = percentile) must pass exactly (to numerical precision) — this confirms your formula implementation against the source, independent of any simulation noise.
- **PRIMARY Tier 3 check (robust — verified with zero exceptions across 26 independent replications):** at every $n$ in the grid, mean CI width should satisfy **percentile width < BC$_a$ width < bootstrap-t width**, strictly. This ordering is far more reliable in a single run than any coverage-based comparison (width is a low-variance, continuous quantity; coverage is a noisy binary-outcome proportion at this trial count).
- **Tier 3** (student-scale numeric bands, `ValidationLog` entry **PS3.3**, `reference_impls/ps3_3_ref.py`): percentile coverage roughly in [0.78, 0.90] (n=8), [0.83, 0.93] (n=15), [0.87, 0.96] (n=30), [0.89, 0.97] (n=60); bootstrap-t coverage roughly in [0.89, 0.98] (n=8), [0.90, 0.98] (n=15), [0.90, 0.98] (n=30), [0.91, 0.98] (n=60); BC$_a$ coverage roughly in [0.79, 0.93] (n=8), [0.84, 0.94] (n=15), [0.87, 0.97] (n=30), [0.89, 0.98] (n=60). Gap check (bootstrap-t minus percentile) ≥0.05 at n=8, ≥0.02 at n=15, ≥0.01 at n=30.
- **SECONDARY Tier 3 check (a real but modest effect — average over the whole $n$-grid, not per-$n$):** averaged across your four $n$ values, (BC$_a$ coverage − percentile coverage) should be $\ge -0.01$, and (bootstrap-t coverage − BC$_a$ coverage) should be $\ge 0.01$. Don't be surprised if BC$_a$'s coverage *at a single $n$ in isolation* is occasionally a hair below percentile's — that is ordinary Monte Carlo noise on a small true effect (~0.5–1.5 coverage points), not a bug; the averaged check is the fair one.

**Discussion note:** (folded guidance; no solution code) The percentile interval under-covers noticeably at small $n$ because it inherits both the narrowness bias (PS3.1/H-3) and an incomplete skewness correction; bootstrap-t corrects for both by pivoting on a statistic closer to distribution-free (at the cost of a formula/nested SE per resample); BC$_a$ takes a different route — it keeps using percentiles of the *same* bootstrap distribution as the percentile method (so it inherits percentile's transformation-respecting property, E&T Sec. 14.3) but shifts *which* percentiles it reads off, using $\hat a$ and $\hat z_0$ to correct for the skewness and median-bias the plain percentile method ignores. This is why BC$_a$'s width lands between the other two: it is doing a real correction (unlike percentile), but a different, generally smaller one than bootstrap-t's full pivotal-statistic approach for this particular statistic (the mean) and population. A common implementation bug for BC$_a$ is computing the jackknife over *bootstrap* resamples instead of the *original* sample — the jackknife is deterministic and uses only your original $n$ data points, no resampling involved. Another common bug: forgetting the bootstrap-t endpoint reversal (subtracting the *upper* $t^*$ quantile to get the *lower* CI endpoint). Students should not expect their exact coverage numbers to match any published article figures — Hesterberg's own published thresholds are from large-scale, variance-reduced simulations; the point of this problem is the *qualitative and width-based* hierarchy, made visible in output the student generated themselves, per R1.2.

---

### PS3.4 — When the bootstrap can't help: an infinite-variance failure
**Type:** D | **Tier:** 2+3 | **Core/Optional:** Core | **Time:** 45 min | **Goals:** 4
**Prerequisites:** the resampling-loop skill from PS3.1

**Statement:**

Everything so far has bootstrapped the mean of a finite-variance population. Here you construct a case where that assumption fails outright: the standard **Cauchy distribution** (density $\frac{1}{\pi(1+x^2)}$) has no finite variance — and in fact no finite mean either, though its median and other robust measures are perfectly well-defined (it is symmetric about 0).

A remarkable fact about the Cauchy distribution (a consequence of its characteristic function $\varphi(t)=e^{-|t|}$, a standard stable-distribution result): **the sample mean of $n$ i.i.d. standard Cauchy draws is itself exactly standard-Cauchy-distributed, for every $n$.** Averaging does not concentrate it at all — there is no law of large numbers here. Contrast this with the standard Normal, where the sample mean's spread shrinks like $1/\sqrt n$ as usual.

**Exhibit A (the required quantitative check).** For $n \in \{20, 100, 500\}$: draw $M=300$ independent samples of size $n$ from (i) standard Normal and (ii) standard Cauchy; for each of the $M$ samples compute the sample mean; report the **interquartile range (IQR)** of those $M$ sample means (use IQR, not SD — Cauchy's SD is undefined and a naive implementation using it can misbehave). Compute the ratio $\text{IQR}(n{=}20)/\text{IQR}(n{=}500)$ for each population. Set and report the seed you use for these draws.

**Exhibit B (qualitative).** Pick one sample size (e.g. $n=50$). Draw **three different** original samples from standard Cauchy, and for each, run your nonparametric bootstrap of the mean (as in PS3.1) and plot the resulting bootstrap distribution. Do the same for three different original standard-Normal samples. Describe what you see: do the three Cauchy bootstrap histograms look like they're estimating "the same thing," the way the three Normal ones do? Set and report the seed(s) you use here (they may differ from Exhibit A's).

Diagnose, in 3–5 sentences: what does it mean for a statistic's bootstrap distribution to be trustworthy, and why does the bootstrap — which relies on the empirical distribution standing in reliably for the population — fail for this statistic on this population?

**Deliverable:** code for both exhibits; the two IQR-ratio numbers; the three-vs-three bootstrap histograms (or a written description if not plotting); 3–5 sentences of diagnosis.

**Verification:** [Tier 2 + Tier 3]
- **Tier 2** (standard distributional fact, citable to any standard probability/mathematical-statistics treatment of stable distributions — no assigned-reading citation needed, this is foundational theory, not a harvested result): the Normal IQR ratio should be roughly **[3.5, 6.5]** (theoretical value: $\sqrt{500/20}=5$). The Cauchy IQR ratio should be roughly **[0.5, 1.8]** (theoretical value: 1 — no shrinkage).
- **Contrast check:** Normal ratio ÷ Cauchy ratio should exceed **2.5**.
- **Tier 3**: reference run logged at `ValidationLog` entry **PS3.4** (`reference_impls/ps3_4_ref.py`) — also documents why Exhibit B is assessed qualitatively (a 3-sample coefficient-of-variation metric was tried and found not reliably separated; rather than loosen a numeric band to paper over that, Exhibit B is graded by description, not by number).

**Discussion note:** (folded guidance; no solution code) The instructive failure here is at the level of the *statistic itself*, not the resampling mechanism — the empirical distribution is a perfectly fine estimate of the Cauchy population, but the sample mean is simply not a well-behaved functional of it (no concentration, no LLN). This is a stronger and different failure than PS3.7's small-sample median instability (optional): there, more data eventually helps; here, more data never helps, because the mean's sampling distribution literally never narrows. Students should notice that a *robust* statistic (e.g., the median, or a trimmed mean) bootstrapped on the same Cauchy data would behave much better — this is worth a sentence in the write-up and is a natural bridge to why robust statistics exist. A frequent error is computing SD instead of IQR for the Cauchy exhibit and being confused by wild, meaningless numbers — that confusion is itself diagnostic of the underlying issue (an undefined population variance has no business being estimated by a sample SD, however large the sample).

---

### PS3.5 — Bootstrapping dependent data: the moving blocks bootstrap
**Type:** I/V | **Tier:** 2+3 | **Core/Optional:** Core | **Time:** 45 min | **Goals:** 5
**Prerequisites:** the resampling-loop skill from PS3.1

**Statement:**

Everything so far has bootstrapped i.i.d. data. Here the data are **serially dependent**: generate a stationary AR(1) series of length $n=200$,
$$X_t = \phi X_{t-1} + \varepsilon_t, \qquad \varepsilon_t \sim N(0,1), \qquad \phi = 0.7,$$
started from its stationary distribution (or with a burn-in of several hundred steps discarded). This process has known mean 0 and known marginal variance $\sigma_X^2 = 1/(1-\phi^2)$. Set and report your seed.

Implement two bootstrap procedures for the mean:

1. **Naive i.i.d. bootstrap:** resample individual time points with replacement (exactly as in PS3.1), ignoring the order/dependence structure entirely. Report the bootstrap SE and 95% percentile CI width.
2. **Moving blocks bootstrap (MBB):** for a chosen block length $L$, form all $n-L+1$ overlapping length-$L$ blocks of *consecutive* observations. Draw $\lceil n/L \rceil$ blocks with replacement (sampling block *start positions*, not individual points), concatenate them, and truncate to length $n$ — this is one bootstrap resample. Repeat $r=3{,}000$ times to build the bootstrap distribution of the mean; report SE and 95% CI width. Do this for **two block lengths**, $L=5$ and $L=20$.

Compare all three CI widths (naive, MBB-$L{=}5$, MBB-$L{=}20$).

Write 3–5 sentences on why the naive bootstrap understates the true uncertainty here, and what "resampling blocks instead of points" is doing to correct for that — and name one limitation the moving blocks bootstrap does not fully solve (e.g., what happens at block boundaries, or how to choose $L$).

**Deliverable:** both bootstrap implementations; a small table of SE/width for naive, MBB-5, and MBB-20; 3–5 sentences of interpretation.

**Verification:** [Tier 2 + Tier 3]
- **Tier 2** (standard time-series fact, citable to any standard time-series text's treatment of AR(1) processes: for positively autocorrelated series, the variance of the sample mean is inflated over the naive i.i.d. formula by a factor $(1+\phi)/(1-\phi)$ — here $\approx 5.67$, i.e. roughly a $\sqrt{5.67}\approx 2.4\times$ inflation in SE): your naive bootstrap SE should be within about ±25% of the naive (dependence-*ignoring*) theoretical value **0.099** — confirming your naive bootstrap is implemented correctly, even though it is the value the rest of this problem shows to be *wrong* for this data.
- **Primary check (Tier 3, the actual point of the problem):** both $\text{MBB-}L{=}5\ /\ \text{naive}$ and $\text{MBB-}L{=}20\ /\ \text{naive}$ **width ratios should be at least 1.4** — i.e., both blocked variants should produce a CI at least 40% wider than the naive one.
- Rough absolute bands (Tier 3, `ValidationLog` entry **PS3.5**, `reference_impls/ps3_5_ref.py`): naive width $\in [0.30, 0.45]$; MBB-5 width $\in [0.50, 0.85]$; MBB-20 width $\in [0.45, 1.10]$ (wider band — block-length-20 resamples carry more single-realization Monte Carlo variability at this series length).

**Discussion note:** (folded guidance; no solution code) The naive bootstrap's percentile CI is too narrow because resampling individual points with replacement destroys the positive autocorrelation — a naive resample looks like an *iid* series with the same marginal variance, understating how much the actual dependent series can wander. The moving blocks bootstrap preserves short-range dependence *within* each block (of length $L$) but breaks it *across* block boundaries — so it works best when $L$ is long enough to capture most of the autocorrelation (roughly, several multiples of $1/(1-\phi)$) but still short enough that many distinct blocks are available to resample from; choosing $L$ is a real bias-variance tradeoff the problem does not ask students to fully resolve, only to observe. Do not expect $L=20$ to reliably beat $L=5$ at recovering the *exact* AR(1)-aware theoretical SE at this single sample realization — both reliably beat naive, which is what Goal 5 asks for ("what each modification corrects for and what residual limitations remain").

---

### PS3.6 — The bootstrap has its own Monte Carlo error
**Type:** C | **Tier:** 1+3 | **Core/Optional:** Core | **Time:** 40 min | **Goals:** 6
**Prerequisites:** the PS3.1 CLEC-mirror dataset (reuse the same 23 values) and resampling-loop code

**Statement:**

Every bootstrap you have run in this module has two sources of error stacked on top of each other: (i) how well the *theoretical* (infinite-resample) bootstrap distribution approximates the true sampling distribution, and (ii) how well your *finite-$r$ Monte Carlo* bootstrap approximates the theoretical one. This problem isolates the second source and connects it back to the Module 1/2 machinery you already have for reasoning about Monte Carlo error.

Using the PS3.1 CLEC-mirror data, for each resample count $r \in \{200, 1{,}000, 5{,}000, 20{,}000\}$: run your nonparametric bootstrap of the mean $K=100$ times, using $K$ **different seeds** but the *same original 23-point sample* each time. For each of the $K$ runs at a given $r$, record the resulting bootstrap SE. Then compute the **standard deviation across those $K$ bootstrap-SE values** — call this $\text{MC-SD}(r)$. It measures how much your bootstrap SE estimate itself would bounce around if you (or someone else) reran the whole procedure with a different seed — i.e., the *Monte Carlo* error of the bootstrap SE, as distinct from anything about the CLEC population.

Check whether $\text{MC-SD}(r)$ shrinks like $1/\sqrt r$ as $r$ grows — the same rate you already know governs plain Monte Carlo estimation error (Module 1/2). A clean way to check this: compute $\text{MC-SD}(r)\cdot\sqrt r$ for each $r$ in your grid — if the $1/\sqrt r$ law holds, this normalized quantity should be roughly constant across all four $r$ values.

Write 3–5 sentences connecting this to Module 1/2's error-budget reasoning: what is playing the role of "sample size" here, and why is it a *different* quantity from the original data's sample size $n=23$?

**Deliverable:** code computing $\text{MC-SD}(r)$ across the $r$-grid; the four normalized values $\text{MC-SD}(r)\cdot\sqrt r$; 3–5 sentences connecting this to Module 1/2.

**Verification:** [Tier 1 + Tier 3]
- **Tier 1** (cite Annex A3.1 / Hesterberg 2015 Sec. 3.6, H-7): the published guidance is $r\ge 15{,}000$ for 10%-accurate percentile/bootstrap-t endpoints — note where this threshold falls relative to your own $r$-grid, and whether your MC noise is already comfortably small by $r=20{,}000$.
- **Tier 3** (`ValidationLog` entry **PS3.6**, `reference_impls/ps3_6_ref.py`): the ratio $\text{MC-SD}(200)/\text{MC-SD}(20{,}000)$ should be roughly in **[7, 14]** (theoretical value: $\sqrt{20{,}000/200}=10$). The four normalized values $\text{MC-SD}(r)\cdot\sqrt r$ should all lie within a factor of **1.5** of their own mean.

**Discussion note:** (folded guidance; no solution code) The "sample size" governing this error is $r$ (the number of bootstrap resamples), not $n=23$ (the number of original observations) — two completely different knobs that are easy to conflate. Increasing $n$ changes how well the empirical distribution approximates the population (a statistical question); increasing $r$ only changes how precisely you've computed a summary of a *fixed* empirical distribution (a pure computation question) — and, exactly as in plain Monte Carlo, that error shrinks at the $r^{-1/2}$ rate regardless of anything about the data. A common confusion: students sometimes expect increasing $r$ to make the CI narrower in a way that reflects "more evidence about the population" — it does not; $r$ only reduces the *noise in your estimate of* the (fixed-width) bootstrap CI, it does not change what that CI actually is.

---

### PS3.7 (Optional) — The bootstrap median's discreteness problem
**Type:** D | **Tier:** 1+3 | **Core/Optional:** Optional | **Time:** 35 min (uncounted) | **Goals:** 4
**Prerequisites:** the resampling-loop skill from PS3.1

**Statement:**

Draw one sample of $n=15$ from a Normal(0,1) population. Set and report your seed.

**Bootstrap distribution of the median:** resample this one sample with replacement $r=2{,}000$ times, and compute the median of each resample.

**True sampling distribution of the median:** because you know the population here, you can get the *actual* sampling distribution directly — draw $M=2{,}000$ **fresh, independent** samples of size 15 from Normal(0,1) (not resampled — newly simulated each time) and compute the median of each.

Compare the two resulting distributions of 2,000 values each. Specifically: (a) count the number of **distinct** values in each of the two distributions; (b) confirm that every value in your bootstrap distribution is exactly equal to one of your 15 original observations.

Write 3–5 sentences diagnosing why this happens (hint: for an odd-sized sample, the median of any resample — being one of the 15 observations — can only take one of 15 possible values, no matter how many times you resample) and why this makes the plain bootstrap a poor tool for studying the median's sampling behavior at small $n$, even though it is a perfectly fine tool for the mean at the same $n$.

**Deliverable:** both simulated distributions; the two distinct-value counts; confirmation that the bootstrap medians are a subset of the original data; 3–5 sentences of diagnosis.

**Verification:** [Tier 1 + Tier 3]
- **Tier 1** (cite Annex A3.1 / Hesterberg 2015 Sec. 3.3, H-2 — cited for the *phenomenon*, not a numeric target: no single number is claimed by the source either).
- **Structural checks (exact, no tolerance needed — these are logical certainties for odd $n$, not statistical tendencies):** the number of distinct values in your bootstrap-median distribution must be **≤15**; every bootstrap median value must be **exactly equal** to one of your 15 original observations.
- **Tier 3** (`ValidationLog` entry **PS3.7**, `reference_impls/ps3_7_ref.py`): the number of distinct values in your *true*-sampling-distribution simulation should be **≥1,980 out of 2,000** (near-certain for a continuous population — a much lower count signals an RNG or rounding bug, not a real effect).

**Discussion note:** (folded guidance; no solution code) This is a *structural* failure, not a sampling-noise phenomenon — unlike every other verification target in this module, the two structural checks here have no legitimate "close enough" band; either your bootstrap medians are a subset of your original data (they must be, by construction) or your implementation has a bug. This is a good contrast with PS3.4's Cauchy failure: there, the statistic (the mean) fails on a *particular population* (infinite variance); here, the statistic (the median) has an inherent discreteness problem tied to sample parity, independent of which population it's drawn from. Interestingly (Efron 1982, cited in Hesterberg 2015), the bootstrap *percentile interval* for the median is not nearly as bad as the discreteness of the full bootstrap distribution might suggest — a nuance worth a sentence if time allows, but not required.

---

## Alignment matrix — Module 3

| Goal | Text (Module_Goals_Reference.md) | Problem(s) / justification |
|---|---|---|
| 3.1 | Derive the nonparametric bootstrap from first principles — the empirical distribution, why sampling from it simulates the sampling process, what assumptions that substitution requires | **PS3.1** (statement requires the plug-in-principle write-up directly) |
| 3.2 | Implement parametric and nonparametric bootstrap and construct CIs through multiple methods, including bootstrap-t, percentile, and BCa | **PS3.1** (nonparametric implementation) + **PS3.2** (parametric implementation) + **PS3.3** (bootstrap-t, percentile, **and BCa** CI construction — BCa added 07/15/2026 per Flags DP-M3-2, now RESOLVED). **Fully certified** — all three named CI methods now have a drafted, tier-1/tier-3-verified vehicle. |
| 3.3 | Explain the theoretical conditions under which bootstrap CIs are valid; distinguish consistency from finite-sample accuracy | **PS3.1** (H-3 narrowness bias — a concrete finite-sample inaccuracy) + **PS3.3** (the coverage experiment — accuracy hierarchy directly observed) |
| 3.4 | Identify and diagnose conditions under which naive bootstrap fails: heavy-tailed distributions, extreme statistics, small samples, dependent or clustered data | **PS3.4** (heavy-tailed/infinite-variance failure) + **PS3.7, optional** (small-sample extreme-statistic failure — the median at n=15). *Dependent-data* diagnosis is also naturally visible in PS3.5 (secondary link; PS3.5's primary goal tag is 3.5, per the WO slate). *Clustered data* is **diagnostic/conceptual only, no implementation problem** — per DG-P2 (Option A) and the instructor note at the top of this file; this is the WO's own resolution, not a gap. |
| 3.5 | Apply modified resampling strategies — including the moving blocks bootstrap — for dependent/structured data; explain what each modification corrects for and what residual limitations remain | **PS3.5** |
| 3.6 | Relate the bootstrap to the Module 1 simulation primitives — a resampling algorithm, computationally analyzable like any other | **PS3.6** |

### Module 3 hours (recomputed from row sums, per `PSDEP-F2Resolution.md`: core ≈ full §5 budget)

| Problem | Core/Optional | Time |
|---|---|---|
| PS3.1 | Core | 45 min |
| PS3.2 | Core | 40 min |
| PS3.3 | Core | 75 min |
| PS3.4 | Core | 45 min |
| PS3.5 | Core | 45 min |
| PS3.6 | Core | 40 min |
| PS3.7 | Optional (uncounted) | 35 min |

**Core total (re-added by hand from rows): 45 + 40 + 75 + 45 + 45 + 40 = 290 min = 4.83 hr** against the 4–5 hr §5 budget — within budget, matching the WO's original figure exactly (the 07/14 session's temporary 275 min/4.58 hr figure, carried while BCa was blocked, is superseded now that DP-M3-2 is resolved and PS3.3's full 75-minute scope is restored). 6 core problems, inside the 5–6 count, matching the WO's core-count target exactly.

---


---

## Module 4 — Optimization: Gradient Methods, Metaheuristics & EM

### PS4.1 — Two Estimators as Optimization Problems

**Type:** I/V | **Tier:** 1+2+3 | **Core/Optional:** Core | **Time:** 55 min | **Goals:** 4.1

**Prerequisites:** None

**Statement:**
Many estimators you already know are, underneath, the solution to an optimization problem — a fact that is easy to state and easy to forget when using canned software. This problem asks you to make that formulation explicit for two different estimators, and to see how a feature of the objective function (how many local peaks it has) can be a property of the *data*, not just the model.

**Part (a) — the mixture MLE as an optimization problem.** Consider a two-component Gaussian mixture with *known* mixing weight w = 0.25 and *known* common variance σ² = 1, and unknown component means (μ₁, μ₂). For data x₁,…,xₙ, the log-likelihood is
ℓ(μ₁,μ₂) = Σᵢ log[ w·φ(xᵢ; μ₁, 1) + (1−w)·φ(xᵢ; μ₂, 1) ],
where φ(·; μ, σ²) is the Gaussian density. Write down this optimization problem explicitly (the objective, the decision variables, and the fact that the MLE is its maximizer). Then generate the following three datasets, using the generative process below, and evaluate ℓ over a grid to see how its shape differs:
- **Dataset A:** seed = 0, n = 400, true means (μ₁,μ₂) = (0, 4), a *fixed* (not random) split of n₁ = 100 points from component 1 and n₂ = 300 from component 2.
- **Dataset A′:** seed = 20260720, n = 400, true means (μ₁,μ₂) = (0, 4), a *random* Binomial(400, 0.25) split of n₁ points from component 1 (n₂ = 400 − n₁ from component 2) — same generating parameters and n as Dataset A, differing only in how the component split is realized.
- **Dataset B:** seed = 0, n = 30, true means (μ₁,μ₂) = (0, 1.0), same weight and fixed-split rule (n₁ = 8, n₂ = 22).

For each dataset, evaluate ℓ(μ₁,μ₂) on a grid with spacing no coarser than 0.06 (a 241×241 grid works) over μ₁,μ₂ ∈ [−4, 8] for Dataset A and Dataset A′ and μ₁,μ₂ ∈ [−4, 6] for Dataset B. Scan the grid for points whose value exceeds all 8 neighboring grid points; treat two such points as the same peak if they lie within 3 grid cells of each other (keep the higher one). Report how many distinct peaks each dataset's surface has, and where they sit.

**Part (b) — the median as a second optimization problem.** Formulate the sample median as the minimizer of the sum of absolute deviations: median(x) = argmin_c Σᵢ|xᵢ − c|. Contrast this briefly (2–3 sentences) with the sample mean as argmin_c Σᵢ(xᵢ−c)², and state which loss function makes which estimator the optimizer's solution. Confirm the identity numerically: generate any dataset with an odd sample size (so the minimizer is unique), and use any 1-D numerical minimizer to find the argmin of Σ|xᵢ−c|; compare it to the sample median. Set and report the seed you use.

**Deliverable:** A written formulation of both optimization problems (objective + decision variable + what the "solution" is); a contour or heatmap plot of ℓ(μ₁,μ₂) for Dataset A, Dataset A′, and Dataset B; a report of the number and location of local maxima found in each; the numerical median-vs-argmin comparison; 3–5 sentences identifying what changed between Dataset A and B (separation and sample size) and what did *not* change between Dataset A and A′ (same parameters, different realized split), and connecting both to why a locally-convergent optimizer (Newton's method, EM — coming in PS4.2–4.4) could behave differently across these surfaces.

**Verification:** [Tier 1 + Tier 2 + Tier 3 — Validation Log `PS4.1`]
- **Tier 1:** R&C Ch. 5, Ex. 5.1 (solved; arXiv:1001.2906) establishes that this mixture family's (μ₁,μ₂) log-likelihood surface is comparable across different realizations of the same generating process — fixed-split vs. random-split draws at the same true parameters and n. Dataset A and Dataset A′ instantiate that comparison.
- *Note on Dataset B:* Separately, and not itself a replication of 5.1 or 5.13: the same model family can produce a qualitatively different surface — unimodal rather than bimodal — when true separation and sample size are both smaller (Dataset B). This is an original observation on this model family, confirmed by the grid search below; it is distinct from 5.1's realization-invariance result above, and it is not a reproduction of 5.13's illustration (which changes the generating model's component count, not just separation within a two-component model).
- **Tier 2:** the median-as-L1-minimizer identity is a standard convex-analysis/order-statistic fact: Σ|xᵢ−c| is piecewise-linear in c, with slope changing sign exactly at the median for odd n.
- **Tier 3:** your grid search should find **exactly 2** local maxima for Dataset A (near (0.05, 3.90) and (4.25, 1.20)), **exactly 2** for Dataset A′ (near (−0.15, 3.95) and (4.10, 0.20), seed 20260720 — the *global* mode matches Dataset A's near (0, 4), while the *secondary* is again a far, label-switched mode whose exact location is realization-dependent; it is this two-mode structure, not the secondary's precise position, that carries the Tier-1 realization-invariance point above), and **exactly 1** for Dataset B (near (0.58, 0.63)), each within one grid cell (~0.05–0.08) of these values (Validation Log `PS4.1`, `reference_impls/ps4_1_ref.py`). Your numerical median check should agree with the sample median to within 1e-4.

**Discussion note:** *(folded)* Dataset A and Dataset A′ share the same generating parameters and n and differ only in how the component split is realized — this is the clean isolation of "the surface's shape is a property of the realized sample," holding the model and its parameters fixed (the realization-invariance point Ex. 5.1 makes). Dataset B is a different kind of contrast: it changes the true separation (itself a model parameter) *and* the sample size, so its shift from bimodal to unimodal reflects a change in the generating parameters, not just the draw — the two comparisons answer different questions and should not be conflated. A common mistake is to grid over too narrow a range and miss the second peak (Dataset A) or to over-interpret grid noise as a spurious extra peak (always check that a candidate peak survives a finer grid before reporting it — the reference run checked stability across four resolutions). For part (b), note that L1 loss is non-differentiable at each data point, so a naive gradient-based minimizer may need to be a derivative-free 1-D method (golden section, `scipy.optimize.minimize_scalar(method='bounded')`) rather than Newton's method — file this away, since Newton's method (PS4.2) will assume enough smoothness for a well-defined Hessian.

---

### PS4.2 — Newton's Method, Encoding Sensitivity, BFGS, and a Step-Size Failure

**Type:** I/D | **Tier:** 3 | **Core/Optional:** Core | **Time:** 70 min | **Goals:** 4.2

**Prerequisites:** None (uses the same mixture-likelihood family as PS4.1, but its own smaller dataset — see Part (a)). *Statement source: Part (a)'s two-encoding contrast (−log L vs. 1/L) adapts the `-like`-vs-`1/like` encoding-sensitivity question of R&C Ch. 5, Ex. 5.2 (arXiv:1001.2906) — an unsolved, even-numbered exercise, cited by concept only. It anchors the problem's construction, not a verification target; all verification here is tier-3.*

**Statement:**
This problem has three parts, all built on the same likelihood surface: implementing Newton's method from primitives, seeing that *how* you encode an equivalent objective can matter enormously for numerical stability, implementing a quasi-Newton method (BFGS) as a check, and deliberately breaking Newton's method with an oversized step.

**Part (a) — Newton's method under two objective encodings.** Use the same mixture model as PS4.1 (known weight w=0.25, known σ²=1, unknown (μ₁,μ₂)), but a smaller dataset: seed = 5, n = 20, true means (0, 4), fixed split. (A smaller n is used deliberately here — see the Discussion note.) Implement Newton's method from scratch: at each iterate θ = (μ₁,μ₂), compute the gradient and Hessian of your objective (central finite differences are acceptable — a step size of h ≈ 1e-5 for the gradient and h ≈ 1e-4 for the Hessian works well) and update θ ← θ − H⁻¹∇g(θ). Run this twice from the same starting point θ₀ = (1, 3), max 50 iterations, convergence tolerance 1e-8 on the step norm:
- **Encoding 1:** g₁(θ) = −log L(θ) (the negative log-likelihood).
- **Encoding 2:** g₂(θ) = 1/L(θ) (the reciprocal of the *raw* likelihood — not its log).

Record the full iterate sequence for both (not just the final point). Compare: do they reach the same (μ₁,μ₂)? How many iterations does each take, and how do the step sizes behave along the way?

**Part (b) — BFGS as a check.** Implement BFGS via its own update formula (the inverse-Hessian form: H⁻¹ update using the secant pairs sₖ = θₖ₊₁−θₖ, yₖ = ∇g(θₖ₊₁)−∇g(θₖ); a simple backtracking line search is sufficient) on encoding 1's objective, from the same θ₀ = (1, 3). Confirm it reaches the same optimum as part (a).

**Part (c) — an oversized step (Type D).** Modify your Newton update to θ ← θ − α·H⁻¹∇g(θ) for a step multiplier α. Run with α = 1.0 (standard Newton, your part-(a) baseline) and α = 1.9, both from θ₀ = (1,3), for a fixed 30-iteration budget. Report where each ends up.

**Deliverable:** The two Newton iterate sequences (table or plot of (μ₁,μ₂) vs. iteration) for both encodings, with a 3–5 sentence comparison of their numerical behavior; the BFGS result and its agreement with Newton; the α=1.0 vs. α=1.9 comparison with 2–4 sentences explaining, in terms of the local quadratic approximation, why the oversized step fails to behave like the standard one.

**Verification:** [Tier 3 — Validation Log `PS4.2`]
- **Tier 3:** both encodings should converge to the same (μ₁,μ₂) — reference run: (−0.1781, 3.7669) from both, agreeing to within 4×10⁻¹¹, cross-checked against a PS4.1-style grid search on the same data (agreement within one grid cell). BFGS should agree with Newton to within 1e-3 (reference run: agreement to 4×10⁻¹¹). With α=1.9 and a 30-iteration budget, your iterate should land far from your α=1.0 optimum (reference run: distance 3.16, at a distinctly worse point with log-likelihood ≈18.4 units worse) — if your α=1.9 run converges cleanly to the same point as α=1.0, double-check your step-multiplier is actually being applied (Validation Log `PS4.2`, `reference_impls/ps4_2_ref.py`).

**Discussion note:** *(folded)* Why n=20 here and not PS4.1's larger n=400 dataset: the reciprocal-likelihood encoding needs the *raw* (non-log) likelihood to be a representable floating-point number, and at n=400 the product of ~400 densities underflows to exactly 0.0, making 1/L undefined from the first iterate — this is itself a real lesson about encoding and floating point, but it would make the comparison inoperable rather than illustrative, so a smaller dataset is used here. Expect encoding 2 to need noticeably more iterations than encoding 1 to reach the same point — this is the numerical-stability point, not a bug. For part (c), a common misconception is that Newton's method "should" always converge near a good starting point; an oversized step shows that even a starting point close enough for the standard step to work well can fail once the step is scaled up, because the local quadratic model is only trustworthy within some radius.

---

### PS4.3 — Deriving and Implementing EM for a One-Parameter Mixture

**Type:** I | **Tier:** 2+3 | **Core/Optional:** Core | **Time:** 45 min | **Goals:** 4.3

**Prerequisites:** None

**Statement:**
Before tackling the full two-component Gaussian mixture (PS4.4), this problem isolates the E-step/M-step derivation in its simplest form: a two-component mixture with *known* component densities g and h, and a single unknown parameter — the mixing weight θ.

Let g = N(0, 1) and h = N(3, 2²) be known densities, and let θ = P(a given observation came from g). For a latent label Zᵢ ∈ {0,1} (1 = "came from g"), derive:
(a) the complete-data log-likelihood given the labels Zᵢ;
(b) the E-step quantity E[Zᵢ | θ, xᵢ] = θ·g(xᵢ) / [θ·g(xᵢ) + (1−θ)·h(xᵢ)];
(c) the resulting closed-form M-step update, θ⁽ʲ⁺¹⁾ = (1/n) Σᵢ E[Zᵢ | θ⁽ʲ⁾, xᵢ].

Implement the resulting EM iteration from these primitives. Generate data with **seed = 7 exactly** (required — see Discussion note), n = 25, true θ = 0.3, using g and h above. Run your EM from at least three different starting values of θ (e.g., 0.1, 0.5, 0.9) and confirm they all converge to the same fixed point. Cross-check that fixed point against a direct 1-D grid search (or a library scalar optimizer, used only as a check) maximizing the same marginal likelihood over θ.

**Deliverable:** The derivation (a)–(c) written out; the EM implementation; a table or plot showing convergence from each starting value; the grid-search cross-check; 2–3 sentences reporting how close your converged θ̂ is to the true θ=0.3.

**Verification:** [Tier 2 + Tier 3 — Validation Log `PS4.3`]
- **Tier 2:** the true generating θ = 0.3 is a citable fact about your own specified generative process (R&C Ex./Ex. 5.14 motivates this known-components/unknown-weight design by concept).
- **Tier 3:** with seed=7, all starting values should converge to θ̂ in [0.305, 0.315], agreeing with each other to within 1e-4 and with a grid-search cross-check to within 1e-3 (reference run: θ̂ = 0.309928 from all five tested starts, grid-search MLE 0.309921). Do **not** expect an arbitrary seed to reproduce this closeness to 0.3 — a 20-seed calibration in the reference run found |θ̂ − 0.3| ranging from 0.004 to 0.20 purely from n=25 sampling noise; seed=7 is required precisely because it demonstrates the intended point cleanly (Validation Log `PS4.3`, `reference_impls/ps4_3_ref.py`).

**Discussion note:** *(folded)* The requirement to use seed=7 exactly is a deliberate, disclosed departure from this module's usual "pick your own seed" convention (compare PS4.4/PS4.5, where you do choose your own). At n=25, the MLE for a mixing weight is a genuinely noisy estimate; the point of this problem is to confirm EM finds the *correct fixed point of the likelihood* reliably regardless of starting value (that part is seed-independent and always true), not that any given small sample recovers the true parameter to two decimal places (that part is seed-dependent and often does not hold nearly this well). Keep these two claims distinct in your write-up.

---

### PS4.4 — Full EM for a Two-Component Gaussian Mixture: Monotonicity and a Bad Initialization

**Type:** I/D | **Tier:** 2+3 | **Core/Optional:** Core | **Time:** 60 min | **Goals:** 4.3, 4.4

**Prerequisites:** None (builds conceptually on PS4.3's derivation pattern, extended to all five parameters)

**Statement:**
Now implement the full EM algorithm for a two-component Gaussian mixture where the mixing weight π, both means (μ₁,μ₂), *and* both variances (σ₁²,σ₂²) are unknown and estimated — a genuinely richer problem than PS4.1–4.2's known-weight/known-variance model or PS4.3's known-components model.

**Data:** generate synthetic data with seed = 3, n = 150, from a two-component Gaussian mixture with true (π, μ₁, σ₁², μ₂, σ₂²) = (0.25, 0, 1, 4, 2). *(A synthetic dataset is used here rather than the real `log(deaths)` data — see Discussion note.)*

**Part (a) — monotonicity.** Implement the E-step (responsibility rᵢ = π·N(xᵢ;μ₁,σ₁²) / [π·N(xᵢ;μ₁,σ₁²) + (1−π)·N(xᵢ;μ₂,σ₂²)]) and M-step (weighted means, weighted variances, and π as the average responsibility) from primitives. Starting from a reasonable, spread-out initialization (e.g., μ₁₀ = min(x), μ₂₀ = max(x), unit variances, π₀ = 0.5), run EM to convergence, recording the log-likelihood at *every* iteration. Verify it never decreases (beyond a small floating-point tolerance — see Verification).

**Part (b) — cross-check.** Fix π, σ₁², σ₂² at your converged values and grid-search over (μ₁,μ₂) alone (same grid technique as PS4.1/PS4.2). Confirm your EM's (μ₁,μ₂) sits at this profile grid's optimum.

**Part (c) — bad initialization (Type D).** Re-run EM from a deliberately bad initialization: set μ₁₀ = μ₂₀ = x̄ (the sample mean) and σ₁²₀ = σ₂²₀ = the sample variance (i.e., both components start **identical**). Report where this converges, and compare its final log-likelihood to part (a)'s.

**Deliverable:** The log-likelihood-vs-iteration plot from part (a) with a one-sentence confirmation of monotonicity; the cross-check grid result; the bad-init run's converged parameters and final log-likelihood, with 3–5 sentences explaining, in terms of the E-step, why identical starting components can never differentiate themselves.

**Verification:** [Tier 2 + Tier 3 — Validation Log `PS4.4`]
- **Tier 2:** your own fully specified generative process (seed, π, means, variances) is the citable fact grounding "what the truth is" for comparison; R&C Ex. 5.10's canonical two-component-mixture EM motivates this design by concept.
- **Tier 3:** your log-likelihood sequence must never decrease by more than 1e-8 at any single iteration (reference run: every increment was strictly positive; the smallest was +7.9×10⁻¹¹, i.e. no violation was actually observed — 1e-8 is a safety margin for floating-point noise, not a reflection of an observed failure). Your converged (μ₁,μ₂) should match your own grid-search cross-check to within one grid cell. Your bad-(identical-init) run should converge with π≈0.5 and μ₁≈μ₂ (both components collapsed together), with final log-likelihood at least 10 nats worse than your good-init run's (reference run: (π,μ₁,σ₁²,μ₂,σ₂²) = (0.5, 3.214, 4.852, 3.214, 4.852), a gap of 16.86 nats — Validation Log `PS4.4`, `reference_impls/ps4_4_ref.py`).

**Discussion note:** *(folded)* **Data-policy note:** the source exercise (R&C 5.10) uses the real `log(deaths)` dataset from the MASS R package. Per the module's sourcing rules, that series is not reproduced here — it runs well over the ~50-value inline-reproduction limit and is not hosted at a persistent, small, openly licensed URL — so a synthetic mixture with a fully specified generative process substitutes for it (this deviation is recorded in the module's Flags, not silently made). **On the bad initialization:** exact ties are what reliably trap this dataset's EM at an inferior fixed point — nearby-but-not-identical bad starts (e.g., both means within the same cluster but slightly apart) were checked and eventually break symmetry, just more slowly (roughly 150 iterations instead of 90) — so if your own experiments with a "nearly-tied" start don't reproduce the failure, that is expected, not a bug; use the *exact* tie as specified to guarantee the demonstration.

---

### PS4.5 — Simulated Annealing: Mode Recovery Across Temperature Schedules (Optional)

**Type:** V | **Tier:** 1+3 | **Core/Optional:** Optional | **Time:** 45 min | **Goals:** 4.5

**Prerequisites:** None (uses the same mixture-likelihood family as PS4.1)

**Statement:**
Metaheuristics like simulated annealing (SA) are meant to be *understood*, not built from scratch in this program — this problem has you run and lightly adapt a provided SA loop, not construct one.

**Objective:** the same mixture log-likelihood family as PS4.1/4.2 (weight w=0.25, σ²=1), with data generated at seed=0, n=30, true means (0, 4) (a smaller n than PS4.1's Dataset A — see Discussion note). Confirm via a PS4.1-style grid search that this dataset's surface has two modes (a dominant/global one and a secondary/local one) and note their (μ₁,μ₂) locations.

**Provided SA loop (pseudocode):**
```
function SA_maximize(objective, theta0, schedule, n_iter, step_sd):
    theta <- theta0
    cur_val <- objective(theta)
    best_theta, best_val <- theta, cur_val
    for k = 0 to n_iter - 1:
        T <- schedule(k)
        proposal <- theta + Normal(0, step_sd, size=2)     # random-walk proposal
        prop_val <- objective(proposal)
        delta <- prop_val - cur_val
        if delta > 0 or Uniform(0,1) < exp(delta / T):     # Metropolis acceptance
            theta, cur_val <- proposal, prop_val
            if cur_val > best_val:
                best_theta, best_val <- theta, cur_val
    return best_theta, best_val
```
Run this loop (as given, or with light modification — e.g., adjusting step_sd) starting from θ₀ = (2, 2) (equidistant from both modes), 300 iterations, 100 replications, across four named temperature schedules:
- fast geometric: T(k) = 8·0.90ᵏ
- moderate geometric: T(k) = 8·0.97ᵏ
- slow geometric: T(k) = 8·0.995ᵏ
- logarithmic: T(k) = 8 / log(k+2)

Set and report the seed(s) driving your 100 replications per schedule (the reference run used seeds 5000–5099, one per replicate). Your own recovery-rate numbers will differ from the reference values but should reproduce the same qualitative ordering across schedules.

For each schedule, classify each replication's final point as recovering the dominant mode or the secondary mode (whichever known mode it's closer to), and report the fraction recovering the dominant mode.

**Deliverable:** The two modes' locations (from your grid search); a table of recovery-rate (fraction reaching the dominant mode) per schedule; 3–5 sentences on the pattern across schedules and why patience in cooling helps.

**Verification:** [Tier 1 + Tier 3 — Validation Log `PS4.5`]
- **Tier 1:** R&C Ch. 5, Ex. 5.7 (solved; arXiv:1001.2906) is the citation anchor for the study design this problem adapts — an SA loop run across several temperature schedules, 100 replications each, classified against a dominant/secondary mode. The recovery-rate pattern itself is not asserted in 5.7's solution prose (its percentages appear only in Fig. 5.4's panel titles); the qualitative direction — slower cooling recovers the dominant mode more often — is established here by the tier-3 logged run alone (Validation Log `PS4.5`).
- **Tier 3:** your slow-geometric schedule's recovery rate should exceed your fast-geometric schedule's by at least 15 percentage points (reference run: 88/100 vs. 64/100, a 24-point gap) — the *direction and rough magnitude* of this gap is what must reproduce, not the exact counts, since outcomes are seed-dependent (Validation Log `PS4.5`, `reference_impls/ps4_5_ref.py`).

**Discussion note:** *(folded)* Why n=30 here and not PS4.1's larger Dataset A: at n=400, moving (μ₁,μ₂) by half a unit changes the log-likelihood by roughly 100+ units — two orders of magnitude larger than any reasonable temperature — so every schedule ends up behaving like plain greedy hill-climbing and the schedules become indistinguishable (checked directly: all four schedules landed in a narrow 63–69% band at n=400). The smaller-n dataset keeps the temperature scale and the likelihood's dynamic range comparable, which is what makes the schedule actually matter — a reminder that "temperature" is only meaningful relative to the scale of the objective it's operating on. Optional theory sub-part (uncounted toward the 45 min above, for students who want the "why"): R&C Ex. 5.6's pseudo-posterior πₘ(θ|x) ∝ ℓ(θ|x)^m construction shows *analytically* that raising a likelihood to an increasing power concentrates its mass on the mode as m grows — exactly the mechanism a falling temperature (equivalent to a rising effective power 1/T) exploits.

---

## Alignment Matrix — Module 4

| Goal | Text (`Module_Goals_Reference.md`) | Problem(s) / justification |
|---|---|---|
| 4.1 | Formulate common statistical estimators as solutions to optimization problems, and identify the objective function features that determine which algorithmic family is appropriate | PS4.1 (two formulations: mixture MLE and median-as-L1-minimizer; grid comparison identifies multimodality as the feature separating the two datasets) |
| 4.2 | Implement and explain Newton's and quasi-Newton methods, including the role of the Hessian and the practical significance of numerical stability and step selection | PS4.2 (Newton from primitives under two encodings; BFGS via its own update formula; step-size/stability Type D failure) |
| 4.3 | Explain the statistical logic of EM — missing data, latent variables, lower-bound ascent — and derive the E and M steps from that framework | PS4.3 (full E-step/M-step derivation for the one-parameter mixture); PS4.4 (extends the same logic to the full five-parameter mixture) |
| 4.4 | Explain why EM guarantees monotone likelihood increase, why this does not guarantee a global maximum, and what Wu (1983) establishes over Dempster et al. (1977) | PS4.4 (numeric monotonicity verification; Type D bad-initialization run demonstrating convergence to an inferior local optimum). The Wu-vs-Dempster-et-al. citation half of this goal is **not** exercised by any problem — it is conceptual-question territory per WO-M4 §5's escalation note; PS4.4's discussion note may carry a labeled-preview pointer to the citation but tests neither paper directly. |
| 4.5 | Recognize when metaheuristic approaches are warranted over gradient or EM methods, and understand their basic operating principles without requiring deep implementation | PS4.5 (**optional** vehicle, per `PSDEP-M1M3M4SlateResolution.md` M4-D1, ratified 07/10/2026 — running/lightly-modifying a provided SA loop, capped per §6's "without requiring deep implementation" constraint). **Recorded consequence:** for core-only students, Goal 5 is met by reading plus an uncounted optional problem, not a counted core one — an accepted, spec-sanctioned effect (ProblemSetRequirements1_1.md §6, Module 4 paragraph), recorded here so it is not silent. |

---

## Module 4 hours

| Core problems | Core hours (sum) | Optional hours (uncounted) | Budget (§5) |
|---|---|---|---|
| PS4.1 (55) + PS4.2 (70) + PS4.3 (45) + PS4.4 (60) = **230 min = 3.83 hr** | 3.83 hr | PS4.5 ≈ 45 min | 3–4 hr |

Reflects the DP-8/E-M4-1 Dataset A′ addition: PS4.1 raised 45→55, so core total is 230 min (3.83 hr) — a ruled +10 on the slate-resolved planning figure of 220 (`ProblemSets_draft_skeleton.md`, `PSDEP-F2Resolution.md`), in-band per DP-8 (230–235) and within the §5 3–4 hr envelope. 4 core problems, PS4.5 optional/uncounted.

---


---

## Module 5 — Bayesian Modeling Framework

### PS5.1 — The normal model with unknown mean and variance

**Type:** I | **Tier:** 1 | **Core/Optional:** Core | **Time:** 40 min | **Goals:** 5.1, 5.3

**Prerequisites:** None

**Statement:**

A factory production line makes windshields, and a small sample has been pulled off the line for hardness testing. Four measured hardness values (in the units the instrument reports) are:

$$y = (13.357,\ 14.928,\ 14.896,\ 14.820)$$

Assume these four values are an i.i.d. sample from a Normal distribution with unknown mean $\mu$ and unknown standard deviation $\sigma$. Adopt the standard noninformative prior for this model, $p(\mu,\sigma) \propto \sigma^{-1}$ (equivalently $p(\mu,\sigma^2)\propto \sigma^{-2}$).

1. **Specify the full model as a computational object.** Write down the likelihood, the prior, and the (unnormalized) joint posterior $p(\mu,\sigma \mid y)$. For each of the three components, state one sentence on what it commits you to — in particular, say plainly what it means for a *prior* to be improper (it is not a probability distribution over $\mu,\sigma$ at all), and under what condition the resulting *posterior* is nonetheless proper (here: whenever $n \ge 2$, since $n=1$ would leave $\sigma$ completely unpinned).
2. **Derive/state the marginal posterior of $\mu$.** Using the standard result for this conjugate-noninformative setup (cite it — you do not need to re-derive it from the joint integral), state that
$$\frac{\mu - \bar y}{s/\sqrt n} \Big|\, y \;\sim\; t_{n-1},$$
where $\bar y$ and $s^2$ are the sample mean and sample variance. Compute $\bar y$ and $s^2$ for the data above, and report the posterior mean of $\mu$ and a central 95% posterior interval.
3. **Exhibit the joint posterior.** The marginal posterior of $\sigma^2$ is Scaled-Inv-$\chi^2(n-1, s^2)$, and $\mu \mid \sigma^2, y \sim N(\bar y, \sigma^2/n)$. Using these two closed-form facts, generate at least 2,000 **direct draws** from the joint posterior (draw $\sigma^2$ first, then $\mu$ given that draw — no posterior sampler of any kind is used or needed here, since both steps draw directly from named closed-form distributions). Set and report a seed. Produce (a) a scatter or contour plot of the joint $(\mu,\sigma)$ draws and (b) the two marginal histograms/densities of $\mu$ and $\sigma$ alongside their exact closed-form curves for comparison.
4. **Posterior predictive.** State the closed form $\tilde y \mid y \sim t_{n-1}\big(\bar y,\ s^2(1+1/n)\big)$ for a new windshield's hardness. Report the predictive mean and a central 95% predictive interval. In 2–3 sentences, explain why the predictive interval is wider than the posterior interval for $\mu$ — name the two sources of uncertainty it combines (residual sampling variability *and* posterior uncertainty about $\mu,\sigma$ themselves) — this is the "what each component commits you to" point applied to the predictive distribution specifically.
5. **Structural-pattern note (Goal 3, multiparameter half).** In 2–3 sentences, name the specific structural device that let you get a marginal posterior for $\mu$ in closed form despite $\sigma$ being unknown (integrating $\sigma$ out of the joint analytically, leaving a Student-$t$ in place of what would be a Normal if $\sigma$ were known) — this "nuisance parameter integrated out, heavier-tailed marginal results" pattern recurs whenever a multiparameter model has one parameter of direct interest and others that are a necessary but secondary part of the model.

**Deliverable:** (i) the three model components with the one-sentence commitment statements (step 1); (ii) $\bar y$, $s^2$, posterior mean and 95% interval for $\mu$ (step 2); (iii) the joint-draw plot plus the two marginal comparison plots, with seed reported (step 3); (iv) predictive mean, predictive 95% interval, and the 2–3 sentence explanation of why it is wider (step 4); (v) the 2–3 sentence structural-pattern note (step 5).

**Verification:** [Tier 1] Cite Vehtari, Aalto BDA course (CS-E5710), Assignment 3 notebook (`avehtari.github.io/BDA_course_Aalto/assignments/template3.html`; live-fetched and confirmed this session, 07/15/2026). The four data values above are that notebook's own stated **test-input subset** for its `mu_point_est`/`mu_interval`/`mu_pred_point_est`/`mu_pred_interval` functions (the notebook's full `windshieldy1` sample has n=9; the test subset — used here so the cited machine-checked values apply exactly, per WO-M5 §5's rule against citing test-input values against different data — is these same four values). The notebook's confirmed machine-checked values on this exact subset: posterior mean of $\mu$ = 14.5, 95% posterior interval = (13.3, 15.7); posterior-predictive mean = 14.5, 95% predictive interval = (11.8, 17.2); marginal-$\mu$ Student-$t$ parameters (df=3, location=14.5, scale=0.3817557); predictive Student-$t$ parameters (df=3, location=14.5, scale=0.8536316). Your computed values should match these exactly (up to rounding/Monte-Carlo noise in the joint-draw plot only — the closed-form numbers in (ii) and (iv) should match to at least 3 significant figures).

Self-audit checklist (this module's R1 mechanism — **self-audit is explicitly the weakest verification mode in the program; it is not disguised as anything stronger here**, supplemented in this problem by the tier-1 numeric target above):
- [ ] All three model components (likelihood, prior, joint posterior) are written out explicitly, not just named.
- [ ] The improper-prior / proper-posterior distinction is stated in your own words, including the $n\ge2$ condition.
- [ ] Your reported posterior mean/interval for $\mu$ and your predictive mean/interval match the tier-1 target values above.
- [ ] Your explanation of the predictive interval's extra width names both uncertainty sources (not just one).
- [ ] The structural-pattern note names the specific mechanism (nuisance-parameter integration → Student-$t$ marginal), not just "it's more spread out."

**Discussion note:** A correct solution shows the posterior interval for $\mu$ noticeably narrower than the predictive interval for $\tilde y$ — this is the concrete payoff of distinguishing "uncertainty about a parameter" from "uncertainty about a future observation," a distinction many students conflate on first exposure. The most common failure mode is using the Normal quantiles instead of $t_{n-1}$ quantiles for the interval (a small-$n$ error that vanishes as $n$ grows, which is worth noting explicitly since $n=4$ here makes the Normal-vs-$t$ gap unusually visible). **Design note (disclosed):** this problem deliberately uses the assignment's 4-observation *test* subset rather than the full 9-observation `windshieldy1` sample specifically so that the cited tier-1 target values apply without adaptation — students curious to see the intervals narrow with more data are welcome to repeat the exercise on the full sample as an ungraded extension, but no numeric target is supplied for that larger sample here. **Module-level note:** per WO-M5 §2, this problem is exempt from the DG-P3 prior-predictive-simulation strengthening (M5-F2) — the prior $p(\mu,\sigma)\propto\sigma^{-1}$ is improper and therefore has no proper prior distribution to forward-simulate from; "prior predictive simulation" is not defined here, which is itself worth knowing as a limit case of Goal 4's prior-checking machinery.

---

### PS5.2 — Prior sensitivity for a Beta-Binomial model

**Type:** I/V | **Tier:** 2+3 (self-audit) | **Core/Optional:** Core | **Time:** 40 min | **Goals:** 5.2, 5.4

**Prerequisites:** None (the prior-predictive draws below reuse only direct-sampling primitives from Modules 1–2 — a uniform-to-Beta and a uniform-to-Binomial draw — not any specific earlier problem's code)

**Statement:**

An environmental monitoring program checks a number of freshwater sites for the presence of a nuisance indicator organism. Out of $n=40$ sites monitored this season, $y=15$ showed the organism present. Model the underlying prevalence $\pi$ (the population proportion of sites where the organism is present) with a Binomial likelihood, $y \mid \pi \sim \text{Binomial}(n,\pi)$.

You will examine how much the resulting inference depends on the choice of prior — this is the module's core prior-sensitivity exercise, and it is conducted entirely analytically and via **prior predictive simulation**, never via a posterior sampler.

1. **Choose three defensible priors for $\pi$** that a reasonable analyst might have picked before seeing the data, covering genuinely different assumptions: (a) $\text{Beta}(2,10)$ — a prior favoring low prevalence, with a small effective prior sample size ($a+b=12$); (b) $\text{Beta}(1,1)$ — flat/uniform, expressing no preference; (c) $\text{Beta}(20,20)$ — centered at $0.5$ but with a much larger effective prior sample size ($a+b=40$, equal to the data's $n$). For each, state in one sentence what an analyst choosing it would be assuming about $\pi$ *before* seeing any data.
2. **Prior predictive simulation (before touching the data).** For each of the three priors, using only Module 1–2 machinery (draw $\pi$ from the prior, then draw $y$ from $\text{Binomial}(n,\pi)$ given that $\pi$ — a pure forward simulation, no posterior sampler of any kind), generate at least 20,000 replicate datasets. Report, for each prior: the simulated mean of $y$ and a 90% simulated predictive interval for $y$. Set and report your seed(s).
3. **Cross-check your simulation analytically.** The exact (closed-form) mean of this prior-predictive distribution is $n\cdot a/(a+b)$ for a $\text{Beta}(a,b)$ prior (this is the Beta-Binomial compound distribution's known mean — cite it, do not re-derive it). Confirm your simulated mean from step 2 agrees with this closed form for all three priors.
4. **Where does the observed data fall?** For each prior, state whether the actual observed $y=15$ falls inside, near the edge of, or outside your simulated 90% predictive interval from step 2. This is a prior-predictive check in miniature: a prior whose predictive interval poorly anticipates the eventually-observed data is telling you something about that prior's assumptions, before any posterior is even computed.
5. **Compute and overlay the three posteriors.** Using Beta-Binomial conjugacy (a standard closed-form update — cite it), compute the exact posterior $\text{Beta}(a+y,\,b+n-y)$ for each of the three priors given the stated data ($y=15$, $n=40$). Plot all three posterior densities (and, for reference, all three priors) on one set of axes.
6. **Sensitivity statement.** In 2–3 sentences, state which aspect of your conclusion is *robust* to the choice of prior among these three, and which is *sensitive* — tie the sensitive/robust claim explicitly to the plotted comparison in step 5 (e.g., do the two weaker priors agree with each other more than either agrees with the strong prior? Is it the posterior mean, the posterior spread, or a downstream decision that moves?).

**Deliverable:** (i) the three priors named with their one-sentence "what this assumes" statements; (ii) simulated predictive mean + 90% interval per prior, with seed(s) reported; (iii) the analytic-vs-simulated cross-check numbers; (iv) the observed-data-vs-interval placement statement per prior; (v) the overlaid prior/posterior plot; (vi) the 2–3 sentence sensitivity statement.

**Verification:** [Tier 2 for the closed-form facts + Tier 3 for the simulation] The Beta-Binomial conjugate posterior update and the Beta-Binomial compound (prior-predictive) mean formula $n\cdot a/(a+b)$ are standard closed-form results for this conjugate family (cite any standard treatment of conjugate Binomial models, e.g. the assigned BDA3 Ch. 2 treatment of the Beta-Binomial model). The prior-predictive simulation values are tier-3, executed and logged in this session (see `ValidationLog` entry **PS5.2**, `reference_impls/ps5_2_ref.py`, 20000 draws/prior, seed 20260715): simulated predictive means 6.670 / 19.985 / 20.030 for Beta(2,10)/Beta(1,1)/Beta(20,20) respectively (vs. analytic means 6.667 / 20.000 / 20.000 — agreement within Monte Carlo noise, confirming the cross-check in step 3 is a real, reproducible check and not a coincidence); logged 90% predictive intervals [1,16] / [1,38] / [13,27]; logged posterior means 0.3269 / 0.3810 / 0.4375.

Self-audit checklist (this module's R1 mechanism — self-audit is explicitly the weakest verification mode in the program, per WO-M5 §5; supplemented here by the tier-2 closed forms and the tier-3 logged run):
- [ ] Each of the three priors' "what this assumes" sentence is stated in terms of the assumption, not just the parameter values.
- [ ] Your simulated predictive mean (20000 draws, any seed) should agree with the closed-form $n\cdot a/(a+b)$ check to within about **0.10 for Beta(2,10)**, **0.25 for Beta(1,1)**, and **0.10 for Beta(20,20)** — the flat prior's compound variance is roughly 6× the other two priors' at this $n$, so it needs a wider band at the same draw count; each figure is ≈3 Monte Carlo standard errors at 20,000 draws.
- [ ] The observed-data-placement statement is made for all three priors, not just one.
- [ ] The sensitivity statement explicitly names what moved (or didn't) across priors and points to the plot, rather than asserting sensitivity/robustness in the abstract.
- [ ] No posterior sampler was used anywhere in this problem — every random draw was a direct draw from a named closed-form distribution (Beta or Binomial).

**Discussion note:** The instructive result (reproduced in the logged reference run) is that the two *weak* priors — despite having very different means (0.167 vs. 0.5) — land closer to each other in the posterior (0.3269 vs. 0.3810) than either does to the *strong* prior (0.4375), because what drives sensitivity here is each prior's effective sample size ($a+b$) relative to the data's $n=40$, not its central tendency. A common misconception this problem is designed to surface: students often expect the prior with the "closer" mean to the data's empirical proportion ($15/40=0.375$) to dominate the comparison; instead it is the prior's *concentration* that matters most. The prior-predictive-check step (4) is also worth flagging as a genuinely useful diagnostic in its own right, independent of the sensitivity question: a prior whose predictive interval is surprised by the data you eventually see is a prior worth reexamining, and this is the a-priori (pre-data) version of the posterior-predictive-checking idea that recurs elsewhere in Bayesian workflow. **Design note (disclosed):** the stated dataset ($n=40$, $y=15$) is an original substitute for the harvest's real 274-site algae-monitoring dataset (Vehtari Aalto BDA Assignment 2) — substituted because that specific sub-exercise carries "no fixed numeric target by design" even in its source (per the harvest's own drafting summary), so no citable external number is being displaced; the substitution keeps the pedagogical structure (a real-flavored environmental binary-presence scenario) while keeping the dataset small enough to state directly and keeping this problem fully self-contained.

---

### PS5.3 — Hierarchical structure: when it closes in closed form, and when it doesn't

**Type:** I | **Tier:** 1 | **Core/Optional:** Core | **Time:** 45 min | **Goals:** 5.3

**Prerequisites:** None

**Statement:**

This problem has two parts, using two different hierarchical models, to draw a sharp contrast: one where the hierarchical structure defeats closed-form analysis, and one where it doesn't.

**Part A — a nonconjugate hierarchical model.** A therapy is being tested at $J$ independent clinical sites. Site $j$ enrolls $n_j$ patients and observes $y_j$ successes, modeled as $y_j \mid \theta_j \sim \text{Binomial}(n_j,\theta_j)$. Rather than modeling the $\theta_j$ directly with a Beta population distribution (which would be conjugate), suppose the population model is placed on the **logit** scale: $\text{logit}(\theta_j) \mid \mu,\tau \sim N(\mu,\tau^2)$ i.i.d. across sites, with some hyperprior $p(\mu,\tau)$ left unspecified (any proper or reference choice — its exact form does not matter for what follows).

1. Write the full joint posterior $p(\theta_1,\dots,\theta_J,\mu,\tau \mid y)$ as an explicit product of terms: the $J$ Binomial likelihood factors, the $J$ population-distribution factors (remember the Jacobian: since the population model is stated for $\text{logit}(\theta_j)$, the density of $\theta_j$ itself picks up a factor $1/[\theta_j(1-\theta_j)]$), and the hyperprior.
2. Consider integrating out every $\theta_j$ to obtain the marginal posterior $p(\mu,\tau\mid y)$ — the object you would actually need in order to summarize the hyperparameters. The $\theta_j$ integrals separate (the $\theta_j$ are conditionally independent given $\mu,\tau$), so this reduces to $J$ one-dimensional integrals of the form $\int_0^1 \theta_j^{y_j}(1-\theta_j)^{n_j-y_j}\cdot N(\text{logit}(\theta_j)\mid\mu,\tau^2)\cdot\frac{1}{\theta_j(1-\theta_j)}\,d\theta_j$. **Show that this integral has no closed form**, and say specifically *why*: name the one property that would have to hold for it to reduce to a standard family (the population density would need to be a conjugate prior for the Binomial — i.e. expressible as a Beta kernel in $\theta_j$ — and a logit-Normal density is not a Beta kernel in $\theta_j$ for any $(\mu,\tau)$). Contrast this explicitly with what would happen if the population distribution had been $\theta_j\sim\text{Beta}(\alpha,\beta)$ directly.
3. **Computational implication (2–3 sentences).** Given that neither the individual $\theta_j$ integrals nor the joint posterior collapse to a standard form, state what this means for actually fitting this model — some form of numerical integration or joint simulation (Gibbs/Metropolis-within-Gibbs) over $(\theta,\mu,\tau)$ is required. Do not attempt this fitting; the point of this problem is to recognize *that* it is required and *why*, which is exactly the boundary between what a modeling problem (this module) asks and what a computational-methods problem (Module 7's Gibbs sampler, later in this program) asks.

**Part B — a conjugate hierarchical model (the shrinkage/partial-pooling formula).** Now consider a different, fully conjugate hierarchical setting: $J$ groups, each with a summary statistic $y_j \mid \theta_j \sim N(\theta_j,\sigma_j^2)$ with $\sigma_j^2$ **known** for each group, and a population distribution $\theta_j \mid \mu,\tau \sim N(\mu,\tau^2)$ i.i.d. across groups.

4. Fixing $\mu$ and $\tau$ at given values (i.e. conditioning on them, not yet integrating over them), derive the conditional posterior distribution of a single $\theta_j$ given $(\mu,\tau,y_j)$. This is the same conjugate Normal-Normal update you have already used for a single-parameter Normal model with a Normal prior — here $N(\mu,\tau^2)$ is playing the role of that Normal prior for $\theta_j$. Show your conditional posterior is Normal with a precision-weighted mean: $$E(\theta_j\mid\mu,\tau,y) = \frac{y_j/\sigma_j^2 + \mu/\tau^2}{1/\sigma_j^2+1/\tau^2}.$$
5. The quantity actually reported in practice replaces the fixed $\mu$ above with $\hat\mu \equiv E(\mu\mid\tau,y)$ — the hyperparameter's own posterior mean given $\tau$ (itself a precision-weighted average of all $J$ groups' data, by the same conjugate-Normal logic one level up). State this substitution in one sentence (you do not need to re-derive $\hat\mu$'s own formula) and write the resulting expression for $E(\theta_j\mid\tau,y)$.
6. **Interpretation (2–3 sentences).** Explain in words what this formula says $\theta_j$'s estimate actually *is*: a weighted compromise between the group's own data $y_j$ and the population mean $\hat\mu$, with the weights set by relative precision ($1/\sigma_j^2$ vs. $1/\tau^2$). Say what happens to this compromise in the two limits $\tau\to0$ and $\tau\to\infty$, and connect each limit to a modeling choice you already know (complete pooling / no pooling).

**Deliverable:** (i) Part A's explicit joint-posterior product (all three levels: likelihood, population/Jacobian, hyperprior); (ii) the no-closed-form argument naming the specific missing property (conjugacy failure), with the Beta-population contrast; (iii) the 2–3 sentence computational-implication statement; (iv) Part B's derivation of $E(\theta_j\mid\mu,\tau,y)$ shown step by step; (v) the $\hat\mu$-substitution sentence and the resulting $E(\theta_j\mid\tau,y)$ expression; (vi) the 2–3 sentence shrinkage interpretation with both limiting cases.

**Verification:** [Tier 1] Cite Gelman et al., *BDA3*, Ch. 5 (already an assigned primary text), Exercises 5.11 and 5.12 as confirmed solved and analytic in the project's own harvest review of `solutions3.pdf` (both exercises verified sampler-free, no-closed-form/derivation content). Your Part A conclusion (no closed form; conjugacy failure is the specific cause) should match the argument shape of BDA3 5.11(b)–(c). Your Part B closed form should match BDA3 5.12's target exactly: $E(\theta_j\mid\tau,y) = \dfrac{y_j/\sigma_j^2 + \hat\mu/\tau^2}{1/\sigma_j^2+1/\tau^2}$, a precision-weighted average of the group datum and the (precision-weighted) population mean estimate.

Self-audit checklist (this module's R1 mechanism — self-audit, supplemented here by the tier-1 target above):
- [ ] Part A's joint posterior explicitly includes all three levels (likelihoods, population distribution *with* the Jacobian, hyperprior) — not collapsed or skipped.
- [ ] The no-closed-form argument names conjugacy failure specifically (not just "it's hierarchical so it's hard").
- [ ] The Beta-population contrast case is stated (what changes if $\theta_j\sim\text{Beta}$ instead).
- [ ] Part B's derived formula matches the tier-1 target exactly, including which quantities are known/fixed at each step.
- [ ] Both limiting cases ($\tau\to0$, $\tau\to\infty$) are stated and connected to pooling.

**Discussion note:** The two parts are deliberately paired: Part A shows a hierarchical model that is *structurally* elementary (three honest levels, nothing exotic) but computationally closed to you until Module 7's tools arrive; Part B shows a hierarchical model where the *same* three-level structure resolves completely by hand. The dividing line is not "hierarchical vs. not" — it is conjugacy at each level. A common error in Part A is trying to "integrate out $\theta_j$ anyway" by expanding the Binomial kernel and hoping terms cancel; there is nothing to find, and recognizing there is nothing to find (and being able to say precisely why) is the actual skill being tested. A common error in Part B is forgetting that $\mu$ itself has posterior uncertainty (treating it as a known constant beyond step 4) — flag this as the reason step 5's $\hat\mu$ substitution matters and is not just notational. **Forward pointer (labeled preview, per WO-M5 §4):** Part A's exact model (logit-Normal population on a Binomial likelihood) is the computational problem Module 7's Gibbs/Metropolis-within-Gibbs material solves — this problem is what tells you *that* the sampler is needed; Module 7 is what builds one.

---

### PS5.4 — Prior predictive simulation for a varying-intercepts model

**Type:** I/V/D | **Tier:** 1+3 | **Core/Optional:** Core | **Time:** 40 min | **Goals:** 5.2, 5.3, 5.4

**Prerequisites:** None (uses only direct-sampling primitives — Normal and Exponential draws, a deterministic logit transform — from Modules 1–2)

**Statement:**

Consider an experiment tracking tadpole survival across many separate tanks, where tank $j$'s survival probability is $\theta_j$ and the tanks are modeled as related but not identical via a varying-intercepts hierarchical structure:
$$\alpha_j \sim N(\bar\alpha,\sigma), \qquad \bar\alpha\sim N(0,1), \qquad \sigma\sim\text{Exponential}(\lambda),$$
with $\theta_j = \text{logit}^{-1}(\alpha_j)$ (the log-odds parameterization keeps $\theta_j\in(0,1)$ automatically).

**Before touching any data**, examine what this prior actually implies about tank survival probabilities — a *prior predictive* check, not a fit.

1. For each of three rates $\lambda \in \{10,\ 1,\ 0.1\}$ (a tight, a moderate, and a wide prior on $\sigma$), forward-simulate at least 10,000 draws of $\theta_j$: draw $\sigma\sim\text{Exponential}(\lambda)$, draw $\bar\alpha\sim N(0,1)$, draw $\alpha_j\sim N(\bar\alpha,\sigma)$, then transform $\theta_j=\text{logit}^{-1}(\alpha_j)$. This is pure forward simulation — no posterior sampler, no data, no fitting. Set and report your seed.
2. Plot the three resulting densities of $\theta_j$ (one curve per $\lambda$) on the same axes, restricted to $(0,1)$.
3. For each $\lambda$, report the fraction of simulated $\theta_j$ landing in the extreme tails ($\theta_j<0.05$ or $\theta_j>0.95$) — call this the "edge mass."
4. **State and explain the effect (2–3 sentences).** What happens to the edge mass as $\lambda$ decreases (i.e. as the prior on $\sigma$ gets wider)? Explain *why* in terms of what a widening $\sigma$ does to the spread of $\alpha_j$ on the logit scale, and why a wide spread on the logit scale does not translate into a "flat, uninformative" spread on the probability scale — it does the opposite, piling mass at the 0/1 extremes. Treat the Exponential(0.1) setting specifically as a failing configuration: a hyperprior that looks diffuse and 'safe' but is in fact making a strong, almost certainly unintended claim about tank survival before any data are seen — your edge-mass numbers are the diagnostic evidence of that failure.
5. **Connect to Goal 4 (2–3 sentences).** This is a prior-predictive check in its purest form: it interrogates an assumption (what a "reasonable-looking" hierarchical prior implies) entirely before seeing data. State one sentence on what this means for choosing $\sigma$'s prior in practice — a modeler who wants genuinely weakly-informative tank-to-tank variation should not simply pick "some Exponential" without first checking, exactly as you just did, what it implies on the scale that actually matters (probability of survival, not log-odds).

**Deliverable:** (i) the three-density overlay plot with seed reported; (ii) the three edge-mass fractions; (iii) the 2–3 sentence explanation of the effect and its logit-vs-probability-scale mechanism; (iv) the 2–3 sentence Goal 4 connection.

**Verification:** [Tier 1 for the qualitative target, Tier 3 for the specific logged run] The qualitative phenomenon — widening the $\sigma$-prior pushes prior tank-survival mass toward the 0/1 edges — is a documented result for exactly this varying-intercepts prior structure (McElreath, *Statistical Rethinking* course, `stat_rethinking_2023`, Week 6 Problem 1; the prior structure and the $\lambda\in\{10,0.1\}$ comparison rates were independently re-confirmed live this session against the public repository and an independent secondary source quoting the primary prompt directly — see `ValidationLog` entry **PS5.4** for the re-verification method and its one disclosed limitation). This session's own logged reference run (`reference_impls/ps5_4_ref.py`, seed 20260715, 20000 draws/setting) obtained edge mass 0.004 / 0.072 / 0.575 for $\lambda=10/1/0.1$ respectively — a monotonic, order-of-magnitude-scale increase. Your own run should reproduce this monotonic direction and its dramatic scale (not the exact fractions, which are seed-dependent).

Self-audit checklist (this module's R1 mechanism — self-audit is explicitly the weakest verification mode in the program, per WO-M5 §5; supplemented by the tier-1 qualitative citation and the tier-3 logged run):
- [ ] All three $\lambda$ settings are simulated with the full three-step draw (σ, then ᾱ, then $\alpha_j$) — not a shortcut that skips a level.
- [ ] The overlay plot shows all three densities distinctly, restricted to $(0,1)$.
- [ ] Edge mass increases monotonically as $\lambda$ decreases, and the explanation names the logit-vs-probability-scale mechanism specifically (not just "more spread out").
- [ ] The Goal 4 connection states a concrete practical consequence (check the implied prior predictive before fixing a hyperprior), not just a restatement of the definition of prior-predictive checking.
- [ ] No posterior sampler was used — this is pure forward simulation from named distributions.

**Discussion note:** This is the module's sharpest illustration of a genuinely counter-intuitive fact: "wide" is not the same as "uninformative," and the scale on which a prior is specified matters enormously for what it implies. A $\sigma\sim\text{Exponential}(0.1)$ prior *looks* diffuse and safe on the log-odds scale, but it concentrates a large fraction of prior mass at essentially-certain-survival or essentially-certain-death — a strong, and probably unintended, implicit claim. The common failure mode is describing the result only as "the plot gets more spread out," without naming the actual mechanism (a wide spread in $\alpha_j$ maps, through the logistic/inverse-logit function's saturating shape, to values that are pinned near 0 or 1 whenever $|\alpha_j|$ is more than a few units from zero). **Re-verification disclosure (per WO-M5 §5):** the live repository was reached and its content re-confirmed this session (see the validation-log entry for the exact method); the primary PDF's binary content itself was not directly re-rendered as text through this session's tools, so the re-confirmation rests on the repository's continued public availability/licensing plus an independent secondary source's verbatim quotation of the same prompt — this is disclosed rather than presented as a full primary-document re-read.

---

### PS5.5 — Why a flat hyperprior is not automatically safe

**Type:** I | **Tier:** 1 | **Core/Optional:** Optional | **Time:** 35 min | **Goals:** 5.2, 5.3

**Prerequisites:** Builds on the hierarchical normal model of PS5.3 Part B (same model family; here $\mu$ and $\tau$ are no longer fixed but are themselves given a prior)

**Statement:**

Return to the hierarchical normal model from PS5.3 Part B: $J$ groups, $y_j\mid\theta_j\sim N(\theta_j,\sigma_j^2)$ with $\sigma_j^2$ known, $\theta_j\mid\mu,\tau\sim N(\mu,\tau^2)$. There, $\mu$ and $\tau$ were held fixed. Now put a hyperprior directly on $(\mu,\tau)$ and ask whether the resulting posterior is even a valid (proper) probability distribution — a question that does not arise for a single-parameter model but becomes a real hazard the moment a variance component gets its own prior.

First, a fact you may use without re-deriving it: marginalizing out every $\theta_j$ analytically (a closed-form step, since this piece of the model is conjugate) gives $y_j\mid\mu,\tau \sim N(\mu,\ \sigma_j^2+\tau^2)$, independently across the $J$ groups. This is the object whose integral against the hyperprior you are examining below.

1. **The naive noninformative choice fails.** Try $p(\mu,\tau)\propto \tau^{-1}$ (the direct analogue of the single-parameter $\sigma^{-1}$ noninformative prior you used in PS5.1). Consider what happens to the marginalized likelihood from above as $\tau\to0^+$: it approaches a finite, positive limit (it does *not* vanish). Combine this with the hyperprior's own $\tau^{-1}$ behavior near $\tau=0$, and argue informally that the resulting posterior is **improper** — the issue lives at the $\tau\to0$ end, not at $\tau\to\infty$.
2. **Removing one power of $\tau$ shifts, but does not remove, the risk.** Try instead $p(\mu,\tau)\propto1$ (flat on $\tau$ itself). Argue informally that this repairs the $\tau\to0$ behavior (the hyperprior no longer blows up there) but now shifts the question to the $\tau\to\infty$ tail, where the marginalized likelihood's own decay rate (in $\tau$, after also accounting for $\mu$'s contribution) has to be fast enough to make the integral converge. State the known result — cite it, you do not need to complete the tail-integral calculation exactly — that propriety under this flat hyperprior requires $J>2$.
3. **Interpretation (2–3 sentences).** Explain why this is a genuinely different situation from the single-parameter noninformative-prior case (PS5.1), where $n\ge2$ was the only condition needed and no analogous "which tail is the problem" question arose. Name the practical lesson: adding a hyperprior on a *variance* (or scale) component in a hierarchical model is not something you can always make "more noninformative" for free — it introduces its own propriety conditions that must be checked, and the required condition can depend on $J$ (the number of groups) in a way that single-parameter models never do.

**Deliverable:** (i) the informal $\tau\to0$ argument for why $p(\mu,\tau)\propto\tau^{-1}$ is improper; (ii) the statement of the $\tau\to\infty$ tail issue for $p(\mu,\tau)\propto1$ and the cited $J>2$ propriety condition; (iii) the 2–3 sentence interpretation contrasting this with PS5.1's simpler single-parameter case.

**Verification:** [Tier 1] Cite Gelman et al., *BDA3*, Ch. 5, Exercises 5.9 and 5.10, confirmed solved and analytic in this project's harvest review of `solutions3.pdf` — both exercises examine exactly this improper-hyperprior hazard (5.9 for the hierarchical-binomial reparametrized case, 5.10 for the hierarchical-normal case used here). The target your argument should reach matches BDA3 5.10's confirmed result: $p(\mu,\tau)\propto\tau^{-1}$ gives an improper posterior; $p(\mu,\tau)\propto1$ gives a proper posterior **if and only if $J>2$** — a clean binary condition.

Self-audit checklist (this module's R1 mechanism — self-audit; the tier-1 citation above supplements it):
- [ ] The $\tau\to0$ argument for part 1 is stated in terms of the marginalized likelihood's own limiting behavior, not just asserted.
- [ ] Part 2 correctly identifies that the risk has *moved* to $\tau\to\infty$, not been eliminated.
- [ ] The $J>2$ condition is stated as the cited target, not re-derived from scratch (the problem does not require completing the tail integral).
- [ ] The interpretation names the specific contrast with PS5.1 (single dangerous limit vs. two, and a group-count-dependent condition that has no single-parameter analogue).

**Discussion note:** This problem is deliberately optional-depth and redundant-adjacent in spirit with PS5.3 — it does not introduce a new model family, only a new question (propriety) asked of a model family the student already built. The common misconception this targets directly: "flat prior = safe default" is true for a location parameter in a single-parameter model (as in PS5.1's $\mu$) but is *not* generally true for a scale/variance component in a hierarchical model, where the group count $J$ enters the propriety condition itself — a fact with no analogue anywhere else in this module and a genuine, well-known trap in applied hierarchical modeling. A student who skips this problem loses nothing required for goal coverage (PS5.3 already carries Goal 3's core hierarchical-structure requirement) but gains a specific, often-surprising piece of modeling judgment if they take it.

---

### PS5.6 — Optional and redundant: the 8-schools model, fully-analytic sub-parts only

**Type:** I | **Tier:** 1 | **Core/Optional:** Optional — redundant | **Time:** 30 min | **Goals:** 5.3 (redundant with PS5.3), 5.2 (redundant with PS5.2/PS5.5)

**Prerequisites:** Same hierarchical normal model family as PS5.3 Part B

**Statement:** **This problem is optional and redundant — it duplicates coverage already carried by PS5.3 (Goal 3, hierarchical structure) and PS5.2/PS5.5 (Goal 2, prior sensitivity/propriety); skipping it costs nothing toward this module's goal coverage.** It is included only as an additional worked instance of a canonical model, using exclusively its fully-analytic sub-parts.

A well-known hierarchical normal example models $J=8$ school-level treatment-effect estimates $y_j$ (with known standard errors $\sigma_j$) as $y_j\mid\theta_j\sim N(\theta_j,\sigma_j^2)$, $\theta_j\mid\mu,\tau\sim N(\mu,\tau^2)$ — the same structure as PS5.3 Part B and PS5.5, now with a specific, often-cited dataset. This problem uses **only** the two sub-questions of this model that resolve fully analytically, with no grid, no simulation, and no posterior sampler of any kind.

**(a) The $\tau=0$ limit (complete pooling).** Show that as $\tau\to0$, every $\theta_j$'s posterior collapses to the same common value (the precision-weighted grand mean), so that under complete pooling no school can be said to be better or worse than any other. This should follow directly from the shrinkage formula you derived in PS5.3 Part B (step 4) by taking the limit $\tau\to0$ there.

**(b) The $\tau=\infty$ limit (no pooling).** Show that as $\tau\to\infty$, the $\theta_j$ become independent: $\theta_j\mid y\sim N(y_j,\sigma_j^2)$ for each $j$ separately (again, this should fall out of your PS5.3 shrinkage formula's $\tau\to\infty$ limit). From this, write the closed-form pairwise comparison probability $\Pr(\theta_i>\theta_j\mid y)=\Phi\!\left(\dfrac{y_i-y_j}{\sqrt{\sigma_i^2+\sigma_j^2}}\right)$, and write (but do not evaluate) the general expression for $\Pr(\theta_i \text{ is the largest})$ as a single integral over the one free variable $\theta_i$, of the form $\int \left[\prod_{k\ne i}\Phi\!\left(\frac{\theta_i-y_k}{\sigma_k}\right)\right]\phi(\theta_i\mid y_i,\sigma_i)\,d\theta_i$. Setting up this integral (not evaluating it numerically) is the required deliverable — evaluating it requires one-dimensional quadrature or simulation, which is explicitly **optional illustration only** in this problem (see Verification below), not a required step, to keep this exercise inside the module's closed-form/derivation toolkit.

**Deliverable:** (i) the $\tau\to0$ collapse argument (part a); (ii) the $\tau\to\infty$ independence result and the closed-form pairwise-comparison formula, plus the correctly-set-up (unevaluated) single-integral expression for $\Pr(\theta_i\text{ largest})$ (part b).

**Verification:** [Tier 1] Cite Gelman et al., *BDA3*, Exercise 5.3, parts (b) and (d), confirmed present and solved in Gelman's publicly posted solutions (`solutions3.pdf`, 24 June 2019 build) per this project's verified-targets annex (Annex A5.1) — both sub-parts confirmed fully analytic (5.3(d)'s complete-pooling collapse is trivial and exact; 5.3(b)'s independent-schools closed forms and pairwise-$\Phi$ formula are exact, with the full numeric $\Pr(\text{best})$ table requiring one-dimensional quadrature beyond the closed-form derivation itself). As **optional illustration only** (not a required or verified part of this problem's deliverable), the confirmed posted-solution values under the $\tau=\infty$ limit are: $\Pr(\text{best})\approx$ 0.556 / 0.034 / 0.028 / 0.034 / 0.004 / 0.013 / 0.170 / 0.162 across the eight schools (labeled A–H in the posted solution's own ordering) — a curious student may evaluate the integral from part (b) numerically and compare, entirely ungraded — expect agreement to about ±0.01 rather than exact matching; the posted values appear to be simulation-derived rather than quadrature-derived (this project's own independent quadrature returns 0.550/0.035/0.026/0.037/0.003/0.012/0.170/0.168, agreeing to ≈0.006 — S4 evaluation, finding E-M5-5).

Self-audit checklist (this module's R1 mechanism):
- [ ] Part (a)'s collapse argument is derived as a limit of the PS5.3 shrinkage formula, not asserted independently.
- [ ] Part (b)'s independence result and pairwise-$\Phi$ formula are both stated, and the integral for $\Pr(\theta_i\text{ largest})$ is correctly set up (correct integrand, correct single free variable) even though it is not evaluated.
- [ ] No grid-over-posterior-conditionals and no posterior sampler appear anywhere in this problem (the M5-F1 ruling: the $\triangle$ grid reading is not used here — this problem stays inside the pure closed-form/derivation lane).
- [ ] The optional/redundant label is visible and the reason (duplicates PS5.3 and PS5.2/PS5.5) is stated, not just implied.

**Discussion note:** Parts (a) and (b) are the two extremes that make the shrinkage formula's behavior (PS5.3 Part B, step 6) concrete on a specific, well-known dataset: complete pooling erases all between-school distinctions, no pooling treats every school as unrelated, and the actual hierarchical posterior (not computed here — that is Module 7's job, per the forward pointer in PS5.3) sits somewhere between the two. **M5-F1 scoping decision (drafter, this session):** per the verified-targets annex's own recommendation, this problem is scoped to the closed-form derivation only; the fully evaluated $\Pr(\text{best})$ table is presented as confirmed, citable, optional illustration rather than a required computed deliverable, since evaluating the single integral in part (b) would require one-dimensional quadrature or simulation — not itself a posterior sampler, but also not a pure derivation, and the annex flagged this exact boundary as a drafter judgment call. Scoping it out entirely (rather than deciding it counts as permitted) is the more conservative reading and keeps this optional problem unambiguously inside the module's closed-form/derivation toolkit.

---

## Alignment matrix — Module 5

| Goal | Text (`Module_Goals_Reference.md`) | Problem(s) / justification |
|---|---|---|
| 5.1 | Specify a Bayesian model as a computational object — joint distribution, likelihood, prior, and posterior — and articulate what each component commits you to | **PS5.1** (core — the two-parameter Normal model, full component-by-component commitment statement); PS5.6 (optional, redundant illustration on a second dataset) |
| 5.2 | Reason about prior selection as a modeling choice with verifiable consequences, not a subjective input to be chosen arbitrarily or defensively | **PS5.2** (core — three priors, analytic + simulated predictive consequences, sensitivity statement); **PS5.4** (core — prior-predictive-simulation angle on a hierarchical scale prior); PS5.5, PS5.6 (optional, redundant depth) |
| 5.3 | Identify the structural patterns that arise in multiparameter and hierarchical models, and explain what hierarchical structure implies computationally | **PS5.1** (core, multiparameter half — nuisance-parameter integration, Student-$t$ marginal); **PS5.3** (core, hierarchical half — the module's primary anchor: nonconjugate no-closed-form case *and* conjugate shrinkage-formula case); **PS5.4** (core — the hierarchical prior structure itself, prior-predictive angle); PS5.5, PS5.6 (optional, redundant depth) |
| 5.4 | Criticize and revise a Bayesian model by interrogating its assumptions — prior sensitivity, likelihood misspecification, and predictive adequacy — independently of how it will be fit | **PS5.2** and **PS5.4** exercise the *prior-sensitivity* facet (core, via analytic comparison and prior-predictive simulation respectively). The *likelihood-misspecification* and *predictive-adequacy* facets are **deliberately unexercised** — per WO-M5 §2's recorded disposition (Wave A [m14]): conceptual-question/checklist territory, no problem-set vehicle by design. This justification is carried here per that disposition, not reopened. |
| 5.5 | Maintain a clear separation between the modeling layer and the computational layer: understand what questions belong to model construction and what questions belong to the sampler | **Deliberately unexercised** — per WO-M5 §2's recorded disposition (Wave A [m14]): no problem-set vehicle by design. PS5.3's forward pointer to Module 7 (the nonconjugate model *is* the computational problem Module 7 solves) and PS5.1's improper-prior/no-prior-predictive-defined discussion gesture at this separation informally, but neither problem claims this goal. |

## Module 5 hours

| Core problems | Core hours (row-summed) | Optional hours (uncounted, row-summed) | Budget (§5) |
|---|---|---|---|
| PS5.1 (40) + PS5.2 (40) + PS5.3 (45) + PS5.4 (40) = **4 core problems, 165 min = 2.75 hr** | 2.75 hr | PS5.5 (35) + PS5.6 (30) = 65 min ≈ 1.08 hr | 2–3 hr |

Core total re-verified by hand from this draft's own time fields: 40+40+45+40 = 165 min = 2.75 hr — matches the WO's stated core total exactly (`PSDEP-F2Resolution.md`: core ≈ full §5 budget); within the 2–3 hr budget. Optional total: 35+30 = 65 min, at the low end of the WO's "65–70 min" revision-note range (this draft's PS5.6 came in at 30 min rather than the WO's upper bound of 35, since the M5-F1 scoping decision removed the numeric-table evaluation step — see PS5.6's discussion note).


---

## Module 6 — Markov Chains as Computational Objects

### PS6.1 — Simulate, verify, and break: mixing, stationarity, and their absence
**Type:** I | **Tier:** 2+3 | **Core/Optional:** Core | **Time:** 40 min | **Goals:** 1, 2
**Prerequisites:** None.

**Statement:**
Define a 4-state Markov chain — call it your **main chain** — on states $S_0, S_1, S_2, S_3$ with transition matrix
$$
P = \begin{pmatrix}
0.5 & 0.3 & 0.2 & 0.0 \\
0.2 & 0.4 & 0.3 & 0.1 \\
0.1 & 0.3 & 0.4 & 0.2 \\
0.0 & 0.2 & 0.3 & 0.5
\end{pmatrix}
$$
(row $i$ = current state $S_i$, column $j$ = next state $S_j$; each row sums to 1, confirm this). Before doing anything computational, look at the matrix and confirm two structural facts by inspection: (i) **irreducible** — every state can reach every other state in some number of steps (trace the nonzero entries); (ii) **aperiodic** — every state has a strictly positive self-transition probability, which alone rules out periodic behavior.

*Part A (simulate).* From primitives — your own uniform-RNG draw and a manual categorical-sampling step (do **not** call a library "sample from a discrete distribution" routine) — simulate a single trajectory of the main chain for $N \ge 200{,}000$ steps, starting at $S_0$. Set and report your seed. Record how often each state is visited and convert to occupancy frequencies (visits to $S_i$ divided by $N$).

*Part B (solve analytically).* Using library linear algebra (permitted here per R4(b) — this is verification machinery, not the algorithm the goal is about), solve for the stationary distribution $\pi^*$ satisfying $\pi^* P = \pi^*,\ \sum_i \pi^*_i = 1$ — e.g. by solving the linear system directly, or via the left eigenvector of $P$ for eigenvalue 1. If you have access to both methods, use them to cross-check each other.

*Part C (compare).* Compute the maximum absolute difference between your Part A occupancy vector and your Part B $\pi^*$, state-by-state.

*Part D (periodic contrast).* Now consider a second, much smaller chain — call it the **periodic chain** — with two states and transition matrix
$$
P_{\text{per}} = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix},
$$
i.e. from either state the chain deterministically swaps to the other. Starting from $\mu_0 = (1, 0)$, compute the distribution $\mu_t = \mu_0 P_{\text{per}}^t$ for $t = 0, 1, \dots, 7$ by matrix powers — no simulation needed; this is exact and deterministic. Observe what happens: does $\mu_t$ ever settle down?

**Deliverable:** Your Part A occupancy-frequency vector; your Part B $\pi^*$; the Part C max absolute difference; the Part D sequence $\mu_0, \dots, \mu_7$ as a short table. In 5–6 sentences: (i) state what Parts A–C together confirm about your main chain reaching a stationary distribution; (ii) name, in your own words, what "mixing," "stationarity," and — by contrast — "failure to converge" each look like in the numbers you just produced (Parts A–C give you the first two; Part D gives you the third); (iii) explain what irreducibility and aperiodicity are each guaranteeing here — be specific about which guarantee (existence of a stationary distribution vs. convergence to it) each property is responsible for; (iv) explain in one or two sentences why $P_{\text{per}}$ never settles despite being a perfectly well-defined, irreducible chain — name the one structural property it lacks.

**Verification:** Part B's $\pi^*$ is a **tier-2** fact: the exact solution of $\pi^*P = \pi^*,\ \sum \pi^*_i = 1$ for the stated matrix — a fully determined linear-algebra computation, no simulation involved. Parts A vs. B (**tier 3**, executed and logged; validation-log entry PS6.1): at $N \ge 200{,}000$ steps, the max absolute difference between your Part A occupancy vector and your own Part B $\pi^*$ should be **less than 0.02** per state. Part D is a **tier-2** fact (exact matrix powers, no tolerance needed): $\mu_t$ must equal exactly $(1,0)$ at even $t$ and exactly $(0,1)$ at odd $t$, for every $t$ you compute — any other value indicates an implementation bug, not sampling noise.

**Discussion note:** (folded) If Parts A and B agree well but you're not sure your simulation is really "from primitives," the tell-tale sign of an accidental library shortcut is usually *too-good* agreement combined with suspiciously round timing — a hand-rolled categorical draw from a single uniform number (walk the cumulative-probability boundaries until you cross the drawn value) is slower and noisier than a compiled routine, and that noise is exactly what Part C's tolerance is sized to absorb. Irreducibility and aperiodicity are doing two genuinely different jobs, and it's worth being precise about which is which: irreducibility (together with finiteness) guarantees a stationary distribution *exists* — the periodic chain has one too, $\pi_{\text{per}} = (0.5, 0.5)$, exactly as irreducible as your main chain — while aperiodicity is what guarantees the chain actually *converges* to it from an arbitrary start. The periodic chain's stationary distribution is real; it's just a fixed point the chain approaches from nowhere except the fixed point itself, because starting anywhere off it, the chain oscillates around it forever rather than settling into it. This is the cleanest way to see why LPW's characterization of irreducibility — a chain is irreducible if and only if its associated state-transition graph is connected (LPW Ch. 1) — is necessary but not sufficient for what Goal 1 asks you to observe: connectivity alone buys you existence of $\pi$, not convergence to it. Zoom out on what you've actually done here: Parts A–C are Goal 1's first two phenomena (mixing and stationarity) made numeric — your simulated trajectory *mixes* toward $\pi^*$, and $\pi^*$ *is* the stationary distribution both by direct simulation and by exact linear algebra agreeing. Part D is the third phenomenon, failure to converge, built as a deliberate foil: same finite-state, well-defined, irreducible chain machinery, one missing property, qualitatively different long-run behavior. Hold onto both chains — a later problem in this module reuses your main chain (unchanged) to make the "how fast does it converge" question precise, and it will point back to this periodic chain again as a reminder of what "guaranteed to converge" was buying you all along.

---

### PS6.2 — Detailed balance: verifying it, and watching it fail
**Type:** I/D | **Tier:** 2+3 | **Core/Optional:** Core | **Time:** 35 min | **Goals:** 3
**Prerequisites:** None.

**Statement:**
You'll build two small chains and put detailed balance to the numeric test on both.

*Chain 1 (reversible, by construction).* Define a **birth–death chain** on states $\{0,1,2,3\}$ — a chain that only moves to a neighboring state or stays put, never jumps more than one state in a single step:
$$
P^{(1)} = \begin{pmatrix}
0.6 & 0.4 & 0.0 & 0.0 \\
0.3 & 0.3 & 0.4 & 0.0 \\
0.0 & 0.2 & 0.3 & 0.5 \\
0.0 & 0.0 & 0.5 & 0.5
\end{pmatrix}.
$$
Compute its stationary distribution $\pi^{(1)}$ (library linear algebra, as in PS6.1 Part B). Then, for **every** pair of states $(i,j)$ — including the pairs with zero transition probability in one or both directions — numerically check whether
$$
\pi^{(1)}(i)\, P^{(1)}(i,j) \;=\; \pi^{(1)}(j)\, P^{(1)}(j,i).
$$

*Chain 2 (non-reversible, by construction).* Define a **biased directed 4-cycle** on the same 4 states — a chain that only ever moves "forward" around a cycle (or stays put), never backward:
$$
P^{(2)} = \begin{pmatrix}
0.3 & 0.7 & 0.0 & 0.0 \\
0.0 & 0.3 & 0.7 & 0.0 \\
0.0 & 0.0 & 0.3 & 0.7 \\
0.7 & 0.0 & 0.0 & 0.3
\end{pmatrix}
$$
(state 3 wraps forward to state 0). Compute its stationary distribution $\pi^{(2)}$ the same way. Then run the same pairwise check as Chain 1 on every **adjacent** pair in the cycle (i.e., $(0,1), (1,2), (2,3), (3,0)$), and compute the **net flow** for each pair,
$$
\text{net}(i \to j) = \pi^{(2)}(i)\,P^{(2)}(i,j) \;-\; \pi^{(2)}(j)\,P^{(2)}(j,i).
$$
Confirm separately that Chain 2 is still irreducible (every state reachable from every other, even though every move is "forward").

**Deliverable:** $\pi^{(1)}$ and, for every pair $(i,j)$, the two sides of the detailed-balance equation and their difference. $\pi^{(2)}$ and, for every adjacent pair, the two sides and the net-flow value. A short (3–5 sentence) interpretation: does Chain 1 satisfy detailed balance? Does Chain 2? Does Chain 2 still have a valid, well-defined stationary distribution despite the failure? What does "net flow" mean physically in terms of probability circulating around the cycle rather than sitting still — and why is detailed balance a *sufficient* but not *necessary* condition for stationarity (i.e. what does Chain 2 prove by existing)?

**Verification:** Both $\pi^{(1)}$ and $\pi^{(2)}$ are **tier-2** facts (exact linear-algebra solutions of the stated matrices). The pairwise comparisons are **tier 3** (executed and logged; validation-log entry PS6.2): for Chain 1, $|\pi^{(1)}(i)P^{(1)}(i,j) - \pi^{(1)}(j)P^{(1)}(j,i)|$ should be **less than $10^{-8}$** for every pair (an exact identity up to floating-point solver precision, not a statistical tolerance — if you see a larger gap, suspect a $\pi^{(1)}$ computation bug, not sampling noise, since nothing here is sampled). For Chain 2, every one of the 4 adjacent-pair net-flow values should be **clearly nonzero** (magnitude greater than 0.05) and should agree with each other in sign and to within a small relative tolerance, by the cycle's built-in symmetry.

**Discussion note:** (folded) Chain 1 is a birth–death chain — a chain whose only allowed moves are to a nearest neighbor (or staying put) on a path. This structure is not a coincidence: any such chain is reversible with respect to its own stationary distribution, essentially because there's only ever one "edge" of probability flow to balance between any two connected states, and the balance equation between neighbors, iterated along the path, is enough to pin down the whole distribution up to normalization. Chain 2 breaks that structure on purpose: it moves only forward around a cycle, so there is a direction of net probability circulation baked into the transition rule itself, and detailed balance — which asks the flow between *every pair* to cancel exactly — has no chance of holding, even though the chain still settles into a perfectly good, unique stationary distribution (uniform, here, by the cycle's symmetry). This is Goal 3's central point made concrete: detailed balance is a *sufficient* condition for a distribution to be stationary (if it holds, you're guaranteed $\pi P = \pi$), but it is not *necessary* — Chain 2 is living proof, since it has a valid $\pi^{(2)}$ without detailed balance ever holding on a single pair. The reason MCMC algorithms are built to enforce detailed balance anyway, rather than aiming for stationarity directly, is constructive: detailed balance gives you a *local*, pairwise condition you can engineer into a proposal-and-accept/reject rule (this is exactly what Module 7's Metropolis–Hastings acceptance ratio does), whereas "has the right stationary distribution" alone is a *global* property with no obvious local recipe for achieving it. Keep the net-flow number in mind, too — 0.175 units of probability mass circulating past any point on this cycle, every step, forever, at stationarity — as a concrete image of what "detailed balance fails" *means*, not just a checkbox that comes back false.

---

### PS6.3 — Spectral gap and mixing time on the lazy $n$-cycle
**Type:** V/D | **Tier:** 2+3 | **Core/Optional:** Core | **Time:** 50 min | **Goals:** 4, 5 (Goal 1 also touched empirically, via the mixing observation in Part C)
**Prerequisites:** None.

**Statement:**
*Part A (build the family).* For each $n \in \{4,5,6,7,8,9,10\}$, construct the transition matrix $P_n$ of the **lazy random walk on the $n$-cycle**: from state $i \in \{0,\dots,n-1\}$ (indices taken mod $n$), stay at $i$ with probability $1/2$, move to $i+1$ with probability $1/4$, and move to $i-1$ with probability $1/4$. (The self-loop's "laziness" matters: the *non-lazy* random walk on an even cycle is periodic, and Goal 4's mixing-time question wouldn't even be well-posed for it — you're building on the aperiodicity point from PS6.1 directly.) Confirm that the uniform distribution $\pi_n = (1/n, \dots, 1/n)$ is stationary for $P_n$ (a quick exact check — $P_n$ is doubly stochastic, so this should hold for every $n$).

*Part B (spectral gap).* Using library eigendecomposition (linear algebra, permitted per R4(b)), compute the eigenvalues of each $P_n$ and record the **spectral gap** $\gamma_n = 1 - \lambda_2(P_n)$, where $\lambda_2$ is the second-largest eigenvalue (the largest, $\lambda_1$, is always 1 for a valid transition matrix).

*Part C (empirical mixing time).* Define the mixing time $\tau_n(\varepsilon)$, with $\varepsilon = 0.25$, as the smallest $t$ such that $\lVert \delta_0 P_n^t - \pi_n \rVert_{TV} \le \varepsilon$, where $\delta_0$ is the point mass at state 0 and $\lVert \cdot \rVert_{TV}$ is total variation distance. Compute $\tau_n(\varepsilon)$ **exactly** via matrix powers — feasible here because every $n$ in your sweep is $\le 10$ states, so no simulation or Monte Carlo estimate is needed at all.

*Part D (plot and connect).* Produce two plots: $\tau_n(\varepsilon)$ against $n$, and $\tau_n(\varepsilon)$ against $\gamma_n$ (or against $1/\gamma_n$, whichever relationship looks cleaner). In 3–5 sentences: describe the relationship between spectral gap and mixing time that you observe (does mixing time grow as the gap shrinks? roughly how — linearly in $1/\gamma_n$, or some other pattern?); then connect this to **Goal 5**, referencing your own PS6.1 Part A experience — explain concretely what a much smaller spectral gap (a much slower-mixing chain) would imply for the reliability of an occupancy-based estimate computed from a *fixed-length* simulated trajectory, and why you might need a substantially longer run on a slow-mixing chain to trust the same estimate you trusted after 200,000 steps in PS6.1.

*Part E (definitional anchor — one paragraph, hand-derived, not swept).* Separately from the $n$-cycle family above, consider the simplest possible chain that has a tunable spectral gap: the two-state chain with **switch probability** $p \in (0, 0.5]$,
$$
P = \begin{pmatrix} 1-p & p \\ p & 1-p \end{pmatrix}.
$$
By hand — this is the one place in this problem where you work the algebra directly rather than calling a library — show that the eigenvalues of $P$ are $1$ and $1-2p$ (hint: solve the characteristic equation $\det(P - \lambda I) = 0$ directly, or note that $P = (1-2p)I + 2p\,\bar P$ where $\bar P$ has every entry $1/2$), and hence that the spectral gap is $\gamma = 2p$. In one sentence, say what happens to mixing speed as $p \to 0$.

**Deliverable:** A table of $(n, \gamma_n, \tau_n(\varepsilon))$ for your sweep; the two plots from Part D; the Part E hand-derivation shown in your own algebra, plus your one-sentence answer about $p \to 0$; the 3–5 sentence write-up connecting Parts B–D to Goal 5 and to your PS6.1 experience.

**Verification:** The spectral gaps $\gamma_n$ are **tier-2** facts — exact library-computed eigenvalues of the fully specified matrices $P_n$ (permitted per R4(b) and the WO's own §5 note; this is verification/characterization machinery, not the "core algorithm from primitives" the module is built around). The mixing times $\tau_n(\varepsilon)$ are **tier 3** (executed and logged; validation-log entry PS6.3): each is an exact integer from a deterministic matrix-power computation (zero statistical tolerance — a mismatch against your own recomputation indicates a bug, not numerical noise), and across your swept range $\tau_n(\varepsilon)$ should be **non-decreasing** as $n$ increases, while $\gamma_n$ should be **strictly decreasing**. Part E's eigenvalues and gap formula are a **tier-2** self-verifying closed form: once derived, you can check them directly by confirming $Pv = \lambda v$ for your two eigenvectors.

**Discussion note:** (folded) The pattern you should see in Part D is that $\tau_n(\varepsilon)$ and $\gamma_n$ move in a roughly reciprocal relationship — their product stays close to a constant across most of your sweep (it drifts a little at the very smallest $n$, which is a small-number edge effect, not a sign of a bug), which is the signature of the well-known "diffusive" scaling for this family: the spectral gap of the lazy $n$-cycle shrinks like $1/n^2$ as $n$ grows, so mixing time grows like $n^2$ — a chain on twice as many states takes *roughly four times as long* to mix, not twice as long. This is the concrete content behind the geometric intuition Goal 4 is after: a longer cycle isn't just "more states to visit," it's a *worse-conditioned* chain in a precise, quantifiable sense, and the spectral gap is what quantifies it. (This is also this module's own conceptual question 33, if you want a second angle on the same relationship stated more qualitatively.) The Goal 5 connection is the practical payoff: your PS6.1 main chain had a comfortably large gap and 200,000 steps gave you an occupancy estimate accurate to a couple thousandths — but on a chain with a spectral gap ten or a hundred times smaller, that same run length would leave you far short of stationarity, and an occupancy-frequency "estimate" computed from it wouldn't actually be estimating $\pi$ yet; it would still be showing you the transient. This is precisely why "just run it longer" is not a free pass in practice — how much longer scales with $1/\gamma$, and a chain's spectral gap is not something you get to see just by watching a trace plot look stable for a while. Part E's two-state chain is the cleanest possible illustration of the gap itself: at $p=0.5$ the chain forgets its past state entirely in a single step ($\gamma=1$, fastest possible mixing), and as $p \to 0$ the chain becomes increasingly "sticky" — it almost never switches, the gap shrinks toward 0, and mixing time grows without bound. (Note, incidentally, that $p=1$ would reproduce PS6.1's periodic 2-cycle exactly — outside this problem's $p \in (0,0.5]$ domain on purpose, since $1-2p$ going negative changes what "gap" even means and that subtlety isn't this problem's job to resolve.) The chains you've just measured here are exactly the kind of object Module 7's samplers *are* — MH and Gibbs are Markov chains engineered to have a specific target as their stationary distribution, and everything this problem taught you about spectral gap and mixing time applies to them directly (preview).

---

### PS6.4 — Why mixing time is well-defined: TV contraction and monotonicity
**Type:** I | **Tier:** 1+3 | **Core/Optional:** Core | **Time:** 35 min | **Goals:** 4
**Prerequisites:** Requires the transition matrix $P$ you specified in PS6.1 (Parts A–C — the 4-state **main chain**, not the periodic chain), unchanged.

**Statement:**
Every mixing-time claim you made in PS6.3 quietly assumed something: that "distance to stationarity" only ever shrinks as $t$ grows, so that "the first $t$ where you're within $\varepsilon$" is a sensible, well-defined quantity rather than something that could flicker back above threshold later. This problem proves that assumption.

Let $\lVert \mu - \nu \rVert_{TV} = \frac{1}{2}\sum_x |\mu(x) - \nu(x)|$ denote total variation distance between two distributions $\mu, \nu$ on the same finite state space, and let $P$ be any transition matrix (rows summing to 1) on that space.

*Part A (TV contraction — reconstruct the proof).* Show that applying $P$ can only contract total variation distance, never increase it:
$$
\lVert \mu P - \nu P \rVert_{TV} \;\le\; \lVert \mu - \nu \rVert_{TV} \qquad \text{for all distributions } \mu, \nu.
$$
Work from the definition of TV distance and the fact that $P$'s rows sum to 1. (This is the TV-contraction result harvested from MIT OCW 18.445's LPW-based problem sets — Levin, Peres & Wilmer; a solved exercise, chapter-mapped to this module's assigned Ch. 4 reading. Its exercise number within the specific edition assigned to this program has not been independently confirmed, so no exercise or section number is cited here.) *Hint, if you want the shortest route*: bound $|(\mu P - \nu P)(y)|$ using the triangle inequality applied to the sum $\sum_x (\mu(x)-\nu(x))P(x,y)$, then sum over $y$ and swap the order of summation.

*Part B (monotonicity of $d(t)$ — derive as a corollary of Part A).* Let $\pi$ be a stationary distribution of $P$ (so $\pi P = \pi$), and define
$$
d(t) = \sup_{\mu} \lVert \mu P^t - \pi \rVert_{TV},
$$
the worst-case distance to stationarity over all possible starting distributions $\mu$, after $t$ steps. Using Part A — applied to the specific pair $(\mu P^t,\ \pi)$, and the fact that $\pi P = \pi$ — show that
$$
d(t+1) \;\le\; d(t) \qquad \text{for all } t \ge 0.
$$
(This is the companion harvested exercise — using the contraction result above, it proves $d(t)$ is non-increasing — likewise a solved MIT OCW 18.445 / LPW exercise, chapter-mapped but not exercise-number-verified; same citation-form caveat as Part A.)

*Part C (confirm it empirically, on your own chain).* Using your PS6.1 main-chain transition matrix $P$ (unchanged) and its stationary distribution $\pi^*$ (also from PS6.1), compute $d(t)$ **exactly** for $t = 0, 1, \dots, 20$. You can compute $d(t)$ tractably for a small chain like this one by using a fact worth noting explicitly: because $\lVert \mu P^t - \pi \rVert_{TV}$ is a convex function of $\mu$ (it's a linear map of $\mu$ composed with a norm), its supremum over the full probability simplex is attained at a vertex of the simplex — i.e., you only need to check point-mass starting distributions $\delta_0, \delta_1, \delta_2, \delta_3$ and take the max, not search over all possible $\mu$. Confirm your computed sequence is non-increasing.

*Part D (optional reinforcement — your discretion).* Repeat Part C's exact $d(t)$ computation for PS6.1's periodic chain. You should find it stays flat rather than decaying — monotonicity (Part B) still holds (trivially, since a constant sequence is non-increasing), but the chain never actually converges. This is the same aperiodicity point from PS6.1 Part D, now visible directly in $d(t)$ rather than in a single oscillating trajectory.

**Deliverable:** Parts A and B as short written derivations (a few lines of algebra/reasoning each — not a page of real analysis). Part C's $d(t)$ sequence for $t=0,\dots,20$, presented as a table or a plot on a log scale, with a one-line confirmation that it is non-increasing. If attempted, Part D's flat $d(t)$ sequence for the periodic chain, with a one- or two-sentence comparison to Part C.

**Verification:** Parts A and B are **tier 1**: the results being (re)proved are two solved exercises harvested from MIT OCW 18.445's LPW-based problem sets (TV contraction; $d(t)$ monotonicity), chapter-mapped to this module's assigned Ch. 4 reading — your derivation should arrive at the boxed inequalities above via your own reasoning, not a transcription of the source's proof. Part C is **tier 3** (executed and logged; validation-log entry PS6.4): your computed $d(t)$ sequence must be **non-increasing** at every step you compute (any observed increase larger than floating-point noise, roughly $10^{-10}$, indicates an implementation bug); you should also see $d(0)$ well above $0.5$ and $d(t)$ shrinking to a very small number (below $10^{-4}$) by around $t \approx 15$–$20$ for this particular chain. Part D, if attempted, is an exact structural fact with zero tolerance: $d(t)$ must equal exactly $0.5$ for every $t$.

**Discussion note:** (folded) The proof strategy in Part A is the elementary route — triangle inequality plus the fact that $P$'s rows sum to 1 — and it's worth noticing that it needs nothing beyond definitions you already have; it does *not* go through a coupling construction. LPW's own exposition of this material (§4.2–§4.4) leans heavily on coupling — building two copies of the chain on a shared probability space and bounding TV distance by their meeting time — which is a genuinely illuminating alternative technique, but one this module does not assign as reading (coupling is LPW Ch. 5, out of scope here). If you're curious what that alternative route looks like conceptually: two chains started from $\mu$ and $\nu$ respectively, run so that once they land on the same state they move together forever after — the probability they *haven't* yet met by time $t$ turns out to upper-bound $\lVert \mu P^t - \nu P^t\rVert_{TV}$, which gives another way to see why repeated applications of $P$ can only bring distributions closer together. You are not asked to formalize that argument here; the elementary proof in Part A is complete on its own and is the one this problem holds you to. Part B's derivation is the satisfying payoff of Part A: monotonicity of $d(t)$ isn't a separate fact requiring separate machinery — it falls straight out of contraction applied to the single pair $(\mu P^t, \pi)$, using $\pi$'s defining property $\pi P = \pi$ to keep the "target" side of the inequality fixed at $\pi$ across the step. Part C closes the loop back to PS6.3: mixing time (the first $t$ with $d(t)$ below some threshold) is only a *well-defined, unambiguous* number because $d(t)$ can't un-shrink partway through — without Part B's result, "the first $t$ below $\varepsilon$" could in principle mean different things depending on how far out you were willing to search. Part D (if you did it) makes the distinction between "monotonic" and "convergent" impossible to blur: the periodic chain's $d(t)$ is perfectly non-increasing — it's constant — while never once getting closer to 0. Monotonicity is a weaker, more generally-true statement than convergence; aperiodicity is what upgrades one into the other, and now you've seen that fact from three different angles across this module (a single trajectory that won't settle, in PS6.1; a flat vs. decaying $d(t)$ curve, here).

---

## Alignment matrix — Module 6

| Goal | Text (Module_Goals_Reference.md) | Problem(s) / justification |
|---|---|---|
| 6.1 | Observe a concrete Markov chain running on a simple target — identifying mixing, stationarity, and failure to converge as empirical phenomena before formalizing them theoretically | **PS6.1** (Parts A–D directly produce all three named phenomena — mixing/stationarity via the main chain's empirical-vs-analytic agreement, failure to converge via the periodic chain — and the write-up requires naming each explicitly; M6-D2 slate instruction discharged). **PS6.3** touches Goal 1 empirically as a secondary effect (Part C's mixing observation on the $n$-cycle family), per the WO's "(1 empirically)" annotation — not counted as this goal's primary vehicle. |
| 6.2 | Define the essential structural properties of a Markov chain — irreducibility, aperiodicity, and stationarity — and explain what each guarantees about long-run behavior | **PS6.1** (irreducibility and aperiodicity confirmed by inspection in the Statement; stationarity established via $\pi P=\pi$ in Part B; the write-up's item (iii) requires the student to state which guarantee — existence vs. convergence — each property is responsible for, using the periodic-chain contrast to make the distinction concrete) |
| 6.3 | Explain detailed balance as a sufficient condition for stationarity, and identify why it is the condition that MCMC algorithms are designed to satisfy | **PS6.2** (numerically verifies detailed balance on a reversible birth–death chain; exhibits its failure — with a nonzero, computed net flow — on a non-reversible chain that nonetheless has a valid stationary distribution, directly modeling the "sufficient, not necessary" relationship; discussion note previews the M6→M7 bridge: detailed balance as the local, engineerable condition MH's acceptance ratio is designed to enforce) |
| 6.4 | Characterize mixing time and the spectral gap as measures of convergence speed, and develop geometric intuition for why some chains mix slowly | **PS6.3** (*uses* the theory: empirical mixing-time-vs-spectral-gap study on the lazy $n$-cycle family, exhibiting the diffusive $n^2$-scaling geometric intuition directly, plus the two-state hand-derived definitional anchor) **and PS6.4** (*justifies* the theory: proves the TV-contraction and $d(t)$-monotonicity results that make "mixing time" a coherent, well-defined quantity in the first place — without Part B's monotonicity result, PS6.3's "first $t$ below threshold" definition would not obviously be unambiguous). These are complementary, not redundant: PS6.3 measures mixing time; PS6.4 establishes that the thing being measured is well-defined. |
| 6.5 | Connect poor mixing directly to downstream consequences — explain what slow mixing implies for the quality of estimates derived from sampler output | **PS6.3** Part D (the 3–5 sentence write-up explicitly connects spectral-gap magnitude to the reliability of a fixed-length occupancy-based estimate, referencing the student's own PS6.1 experience as the concrete point of comparison) |

**R6 (Type D / failure-mode representation) note:** discharged twice in this module, per the WO's own instruction — **PS6.2**'s non-reversible chain is a constructed failing configuration (detailed balance fails, with the failure's computational symptom — nonzero net flow — produced and interpreted), and **PS6.3**'s slow-mixing end of the $n$-cycle sweep is a diagnosed slow-mixing configuration (large $n$, small gap, large $\tau_n$, interpreted for its estimate-quality consequences in Goal 5). Both problems carry an explicit `/D` in their Type tag for this reason.

## Module 6 hours

| Core problems | Core hours (row sum) | Optional hours (uncounted) | Budget (§5) |
|---|---|---|---|
| 4 (PS6.1, PS6.2, PS6.3, PS6.4) | 40 + 35 + 50 + 35 = 160 min = 2.67 hr (2h40m) | 0 (zero optional, per the WO's no-enrichment disposition) | 2–3 hr |

Re-added by hand from the problem rows above (not restated from the WO without re-checking): 40 + 35 = 75; 75 + 50 = 125; 125 + 35 = **160 min = 2.67 hr** — matches WO-M6 §3's own stated total and OF-9's recorded M6 core row sum (160 min) exactly; within the 2–3 hr §5 budget.


---

## Module 7 — MCMC Methods

### PS7.1 — SIR: from importance weights to an approximate sample
**Type:** C | **Tier:** 3 | **Core/Optional:** Core | **Time:** 40 min | **Goals:** 1 (7 via discussion note)
**Prerequisites:** Requires your PS2.3 importance sampler — the named functions `log_importance_ratios`, `normalize_weights`, and `is_estimate`, unchanged, on PS2.3's own bioassay data and prior.

**Statement:**
Return to your PS2.3 bioassay setup exactly as you built it: the 4-group dose/animals/deaths table, the bivariate normal prior $(\alpha,\beta) \sim N\big((0,10),\, \Sigma\big)$ with $\Sigma = \begin{pmatrix}4 & 12\\ 12 & 100\end{pmatrix}$ (i.e. $\alpha$-sd 2, $\beta$-sd 10, correlation 0.6), and the prior-as-proposal pattern (so `log_importance_ratios` reduces to the log-likelihood alone, exactly as you established there). This time, instead of the small 6-point validation case, draw $N = 50{,}000$ values $(\alpha^{(i)},\beta^{(i)})$ from the prior. Call your `log_importance_ratios` function on these draws against the same bioassay data table, then your `normalize_weights` function on the result, to get self-normalized weights $w^{(i)}$ — unchanged code, new (larger) input.

Using `is_estimate`, compute the self-normalized IS estimate of the posterior mean of $\alpha$ and of $\beta$ from all $N$ weighted draws; call these your **reference estimates**. Using the same weights, also compute the IS-weighted second moment ($\text{is\_estimate}$ on $\alpha^2$, resp. $\beta^2$) and subtract the squared reference mean to get a **reference variance** for $\alpha$ and for $\beta$. (Because this bioassay posterior has no closed form — unlike a conjugate model — these large-$N$ weighted estimates, not an analytic fact, are what "the target's known moments" means for this problem: your best available estimate of the truth, established independently of the resampling step below.)

Sampling Importance Resampling (SIR) treats $\{(\alpha^{(i)},\beta^{(i)}), w^{(i)}\}$ not as an estimator input but as a weighted "urn": resampling from it converts importance weights into an actual approximate sample from the target, at the cost of some additional Monte Carlo noise. Perform four resamples from your $N$ draws, using $w^{(i)}$ as selection probabilities:
1. size $M=1{,}000$, with replacement
2. size $M=1{,}000$, without replacement
3. size $M=5{,}000$, with replacement
4. size $M=5{,}000$, without replacement

**Deliverable:** Your reference estimates (mean and variance of $\alpha$, mean and variance of $\beta$, from the full $N=50{,}000$ weighted draws). For each of the four resamples above, the resampled sample's mean and variance for $\alpha$ and for $\beta$, and each one's absolute difference from the corresponding reference estimate, in a small table (4 rows × 4 statistics). In 3–5 sentences, explain what SIR is doing conceptually — why resampling with probability proportional to $w^{(i)}$ converts a weighted sample into an (approximately) unweighted one — and frame it as the bridge from importance sampling (Module 2) to the approximate-sampling problem MCMC (the rest of this module) solves differently.

**Verification:** Tier 3 (executed and logged; validation log entry PS7.1). For every one of the four resamples, against your own reference estimates: $|\text{resampled }\alpha\text{ mean} - \text{reference}| < 0.15$; $|\text{resampled }\alpha\text{ variance} - \text{reference}| < 0.20$; $|\text{resampled }\beta\text{ mean} - \text{reference}| < 0.65$; $|\text{resampled }\beta\text{ variance} - \text{reference}| < 6.5$.

**Discussion note:** (folded) All four resamples should land inside the stated tolerances — this is a well-conditioned SIR setup because $M$ (1,000 or 5,000) is kept well below the importance sample's effective size (roughly 14,000–14,600 out of $N=50{,}000$, about 28–29%: this bioassay likelihood is informative but doesn't push the posterior so far from the wide prior that weights collapse the way they did on PS2.3's own tiny 6-point *validation* case — that ESS≈1.354-out-of-6 was a deliberately small test input, not representative of a production-sized draw). If you experiment with $M$ approaching or exceeding the effective sample size, the *without-replacement* resamples in particular degrade sharply — you start being forced to include many low-weight draws just to fill the quota, and the resampled distribution drifts back toward the (wrong) proposal rather than the target. That failure mode is a preview of a lesson this module returns to for MCMC as well: an approximate-sampling scheme is only as good as its effective sample size, however that size is achieved. Note also what this problem does *not* have that a closed-form-target check would: your "ground truth" here (the large-$N$ IS-weighted reference) is itself a Monte Carlo estimate, not an independent fact — the same pattern your PS2.6 preview (if you did it) already used at a smaller scale. That's an acceptable R1.3-style cross-check (two estimates from related but distinct procedures agreeing), not a weaker one, precisely because SIR and the weighted estimate can fail independently (a resampling bug won't show up in the weights themselves, and vice versa). Note the division of labor: this problem's check guards only the *resampling* step, because both sides of the comparison share the same weights — a bug in the weights themselves would corrupt reference and resample identically and pass unnoticed here. What guards the weights is your PS2.3 machine-checked test case (the fixed six-point validation against known outputs); this problem builds on functions already validated there, which is why it can focus its own check on the one new thing it introduces. Goal 7's "common family" framing: SIR, MH, and Gibbs are three different answers to the same question — how do you get draws from a target you can only evaluate (up to a constant), when direct sampling isn't available? SIR's answer is "weight-then-resample, once"; MH and Gibbs (below) build an iterative Markov chain instead, trading SIR's one-shot weight degeneracy risk for a different set of tuning/mixing risks you'll spend the rest of this module characterizing.

---

### PS7.2 — Random-walk Metropolis-Hastings: the proposal-scale tradeoff
**Type:** I/V | **Tier:** 1+3 | **Core/Optional:** Core | **Time:** 75 min | **Goals:** 2, 3 (7 via discussion note)
**Prerequisites:** None.

**Statement:**
*Part A (derivation, Goal 2).* A random-walk Metropolis sampler proposes $\theta' = \theta + \varepsilon$ with $\varepsilon$ drawn from a distribution symmetric about 0 (so the proposal density satisfies $q(\theta' \mid \theta) = q(\theta \mid \theta')$). Starting from the detailed-balance condition $\pi(\theta)\,q(\theta'\mid\theta)\,\alpha(\theta,\theta') = \pi(\theta')\,q(\theta\mid\theta')\,\alpha(\theta',\theta)$, derive the Metropolis-Hastings acceptance probability for this symmetric-proposal case, and show it reduces to
$$\alpha(\theta,\theta') = \min\left(1, \frac{\pi(\theta')}{\pi(\theta)}\right).$$
State in one or two sentences why the proposal terms cancel here but would not in general (asymmetric-proposal) Metropolis-Hastings.

*Part B (implementation, Goals 2–3).* Implement this random-walk Metropolis sampler from scratch (loops, arithmetic, your language's uniform RNG only — no MCMC library calls) targeting $\pi(\theta) = N(0,1)$, with proposal increments $\varepsilon \sim N(0, \delta^2)$. Run the sampler for $50{,}000$ iterations at each of three proposal scales, $\delta \in \{0.1, 1, 10\}$, from the same starting point and using a seed you set and report (a fresh seed per $\delta$, or one seed reused across all three — either is acceptable, but report which). For each $\delta$, record: the acceptance rate; the sample mean and variance of the chain (all $50{,}000$ draws, no warm-up discarded — warm-up handling is Module 8's subject, not this problem's); and the lag-1 and lag-20 sample autocorrelations, $\hat\rho_k = \frac{\sum_t (\theta_t-\bar\theta)(\theta_{t+k}-\bar\theta)}{\sum_t (\theta_t - \bar\theta)^2}$.

**Deliverable:** Your derivation (Part A, a few lines of algebra + the one-to-two-sentence cancellation note). A table with one row per $\delta \in \{0.1, 1, 10\}$ and columns: acceptance rate, sample mean, sample variance, lag-1 ACF, lag-20 ACF. A 4–6 sentence interpretation of the acceptance-rate/autocorrelation tradeoff across the three scales — in particular, compare what lag-1 vs. lag-20 autocorrelation tells you at each scale, since they don't tell the same story here.

**Verification:** Part A is tier 2 (a standard, citable derivation — your result should match the boxed formula above; any correct MCMC/Monte-Carlo reference derives the same symmetric-proposal special case). Part B: (i) tier 1 for context only — R&C's own worked example (Example 6.4/6.10) at these same three $\delta$ values on a comparable normal-target random-walk study reports acceptance rates of approximately 0.98, 0.80, and 0.15 respectively (cited as approximate order-of-magnitude context, not a pass/fail target); (ii) tier 3 for the actual pass/fail check (executed and logged; validation log entry PS7.2) — at $n_{\text{iter}}=50{,}000$: acceptance rate should fall in $[0.94,0.99]$ ($\delta=0.1$), $[0.65,0.75]$ ($\delta=1$), $[0.08,0.18]$ ($\delta=10$); lag-1 ACF in $[0.98,1.00]$, $[0.70,0.82]$, $[0.75,0.90]$ respectively; lag-20 ACF in $[0.82,0.95]$, $[-0.06,0.08]$, $[-0.03,0.10]$ respectively; and (known-truth sanity check, tier 2 — target mean 0/variance 1) sample mean in $[-0.35,0.35]$ and sample variance in $[0.65,1.30]$ at every $\delta$.

**Discussion note:** (folded) The headline finding: $\delta=10$'s lag-1 autocorrelation (≈0.84) is actually *higher* than $\delta=1$'s (≈0.78), even though $\delta=10$ has a much lower acceptance rate — because most proposals are rejected, the chain repeats its current value often, and repeated values inflate short-lag correlation. But by lag 20, both $\delta=1$ and $\delta=10$ have decorrelated to near zero, while $\delta=0.1$ is still around 0.90 — its small steps mean it takes many iterations to traverse the target's support at all, regardless of its near-perfect acceptance rate. The lesson: acceptance rate alone (or lag-1 ACF alone) can be misleading; a step size that "almost always accepts" is not thereby mixing well, and a step size with a low acceptance rate is not thereby mixing badly at longer lags. This is the empirical content behind the well-known guidance that random-walk Metropolis mixes best at a moderate (not extreme) acceptance rate — here, $\delta=1$'s ≈0.70 acceptance rate is the best-mixing of the three by the lag-20 criterion, consistent with $\delta=0.1$'s (too-timid) and $\delta=10$'s (too-bold, but recovering by longer lags) both being worse choices by that same criterion. Zooming out: unlike PS7.1's SIR (a one-shot weight-and-resample scheme), MH replaces the "how good is my sample" question with "how well is my chain moving" — same underlying goal (approximate the target), different mechanism and different failure signature. That family resemblance, and the different-mechanism/different-failure-mode contrast, is picked up again explicitly after PS7.3's Gibbs sampler below.

---

### PS7.3 — Two-stage Gibbs sampler on a conjugate Binomial/Beta joint
**Type:** I | **Tier:** 2+3 | **Core/Optional:** Core | **Time:** 50 min | **Goals:** 4
**Prerequisites:** None.

**Statement:**
Consider the joint distribution over $(X, Y)$, with $X \in \{0,1,\dots,n\}$ and $Y \in (0,1)$, defined by the two conditionals
$$X \mid Y=y \;\sim\; \text{Binomial}(n, y), \qquad Y \mid X=x \;\sim\; \text{Beta}(x+\alpha,\; n-x+\beta),$$
with $n = 20$, $\alpha = 2$, $\beta = 3$ fixed. (This pair of conditionals is a standard example precisely because each one is easy to sample from directly, even though the joint density itself is not a named distribution you'd write down first and factor.)

*Part A (derivation).* Derive the two full conditionals above from the joint density $p(x,y) \propto \binom{n}{x} y^{x+\alpha-1}(1-y)^{n-x+\beta-1}$ (i.e., show why conditioning on $y$ leaves a Binomial kernel in $x$, and conditioning on $x$ leaves a Beta kernel in $y$). Then derive the closed-form marginal of $X$ by integrating $y$ out of the joint, and show it is the Beta-Binomial compound distribution:
$$P(X=k) = \binom{n}{k}\frac{B(k+\alpha,\, n-k+\beta)}{B(\alpha,\beta)}, \qquad k=0,\dots,n,$$
with mean $n\alpha/(\alpha+\beta)$ and variance $\dfrac{n\alpha\beta(\alpha+\beta+n)}{(\alpha+\beta)^2(\alpha+\beta+1)}$.

*Part B (implementation).* Implement the two-stage Gibbs sampler from scratch: initialize $Y_0$, then alternate $X_t \sim \text{Binomial}(n, Y_{t-1})$ and $Y_t \sim \text{Beta}(X_t+\alpha,\, n-X_t+\beta)$, for $20{,}000$ iterations, discarding the first $1{,}000$ as warm-up. Set and report your seed. Separately, implement **direct sampling** from the same joint: draw $Y \sim \text{Beta}(\alpha,\beta)$, then $X \mid Y \sim \text{Binomial}(n, Y)$ — no Markov chain, just $19{,}000$ independent $(X,Y)$ draws.

*Part C (Goal 4, second clause).* Explain why this Gibbs sampler accepts every proposed draw with probability 1. Specifically: view each Gibbs step as a Metropolis-Hastings step whose proposal distribution is the *exact* full conditional (e.g., proposing $Y' \sim p(y \mid x)$ rather than some other candidate distribution). Write out the MH acceptance ratio $\alpha(\text{current}, \text{proposed}) = \min\left(1, \frac{\pi(\text{proposed})\,q(\text{current}\mid \text{proposed})}{\pi(\text{current})\,q(\text{proposed}\mid\text{current})}\right)$ for this case (where $\pi$ is that step's target — the full conditional itself) and show algebraically that it equals 1 identically, for any current/proposed pair. This is why Gibbs needs no accept/reject step at all: it is the special case of Metropolis-Hastings where the proposal *is* the target.

**Deliverable:** Parts A and C as short derivations (a few lines of algebra each). For Part B: your $19{,}000$ post-warm-up Gibbs draws of $X$ and your $19{,}000$ direct-sampling draws of $X$; a histogram of each overlaid on the closed-form Beta-Binomial pmf from Part A; a small table comparing (Gibbs mean, Gibbs variance), (direct-sampling mean, direct-sampling variance), and (closed-form mean, closed-form variance).

**Verification:** Part A/closed-form mean and variance are tier 2 (standard Beta-Binomial compound-distribution identity; your derivation should match the boxed formulas). Part B is tier 3 (executed and logged; validation log entry PS7.3): at $n_{\text{iter}}=20{,}000$ (burn-in 1,000, $N=19{,}000$ retained), $|\text{Gibbs mean} - 8.0| < 0.4$ and $|\text{Gibbs variance} - 20.0| < 1.6$ (closed-form check); $|\text{Gibbs mean} - \text{direct-sampling mean}| < 0.45$ and $|\text{Gibbs variance} - \text{direct-sampling variance}| < 1.4$ (cross-method check, R1.3); and $\max_{k=0,\dots,20} |\hat{P}(X{=}k) - P(X{=}k)| < 0.015$ for both your Gibbs and direct-sampling histograms against the closed-form pmf. Part C is tier 2 (a standard derivation; your algebra should reduce the ratio to exactly 1).

**Discussion note:** (folded) All three views of $X$'s distribution — Gibbs, direct sampling, and the closed form — should agree within Monte Carlo noise; if your Gibbs histogram matches direct sampling but *both* disagree with the closed form, suspect an error in your closed-form derivation (Part A) rather than your sampler. If Gibbs disagrees with both direct sampling and the closed form, suspect the sampler (a common bug: updating $Y$ using the *previous* iteration's $X$ instead of the just-drawn current $X$, breaking the alternating structure). Part C's punchline generalizes: Gibbs is not "MH without acceptance" as a separate algorithm — it is literally MH with a proposal so well-chosen (the exact conditional) that rejection never triggers. This is also why Gibbs needs no proposal-tuning step at all, unlike PS7.2's random-walk MH: there is no scale to choose, because the "proposal" is exact by construction. That convenience has a cost, explored next: it requires the full conditional to be tractable to sample from directly, which won't always hold (PS7.5).

**Instructor note (source provenance):** This problem's two-stage Beta-Binomial Gibbs construction adapts the *shape* of R&C Ch. 7, Ex. 7.2 (a conjugate two-stage Gibbs sampler with a closed-form marginal to check against) — an unsolved, even-numbered exercise, cited by concept only. R&C 7.2 anchors the construction, not a verification target: no R&C solution exists for it, so the model, hyperparameters, and all numeric targets here are original/derived. The tier-2 checks are Part A's standard Beta-Binomial identities; all runtime checks are tier-3. (Recorded per DP-18's "adapted" ruling, E-M7-3.)

---

### PS7.4 — Hierarchical Gibbs sampler: ten-pump failure-rate estimation (healthy chain export)
**Type:** I | **Tier:** 2+3 | **Core/Optional:** Core | **Time:** 75 min | **Goals:** 4 (6-adjacent interpretation)
**Prerequisites:** None.

**Statement:**
Ten pumps have been in service for different lengths of time and have recorded different numbers of failures. For pump $i=1,\dots,10$, let $t_i$ be its (known) exposure time and $y_i$ its number of recorded failures. Model failures as $y_i \mid \theta_i \sim \text{Poisson}(\theta_i t_i)$, where $\theta_i$ is pump $i$'s (unknown) failure rate. Pool information across pumps with a hierarchical prior: $\theta_i \mid \alpha,\beta \sim \text{Gamma}(\alpha,\beta)$ i.i.d. across pumps, with shape $\alpha = 1.8$ fixed and rate $\beta \sim \text{Gamma}(0.1, 1.0)$ (a weakly informative hyperprior).

Generate your synthetic dataset with $t = (10, 20, 15, 30, 25, 5, 40, 8, 12, 18)$ and true rates $\theta_{\text{true}} = (0.05, 0.15, 0.30, 0.02, 0.50, 0.80, 0.01, 0.60, 0.25, 0.10)$: draw $y_i \sim \text{Poisson}(\theta_{\text{true},i}\, t_i)$ for each pump using a seed you set and report.

Derive the full conditionals. Both are conjugate gamma updates:
$$\theta_i \mid y_i, \beta \;\sim\; \text{Gamma}(\alpha + y_i,\; \beta + t_i), \qquad \beta \mid \theta_1,\dots,\theta_{10} \;\sim\; \text{Gamma}\!\left(0.1 + 10\alpha,\; 1.0 + \textstyle\sum_i \theta_i\right).$$
Show the derivation for each (Poisson-Gamma conjugacy for $\theta_i$ given $\beta$; Gamma-Gamma conjugacy for $\beta$ given all $\theta_i$'s).

Implement the Gibbs sampler from scratch: alternately draw all ten $\theta_i$'s given the current $\beta$, then draw $\beta$ given the current $\theta_i$'s. Run **three chains** from different initial values of $\beta$ (e.g. 0.2, 1.0, 5.0) and different seeds, each for $20{,}000$ iterations. Call one of them — the one you'll keep — your **reference chain**; report its seed and initial state.

**Deliverable:**
1. Your full-conditional derivations.
2. For your reference chain, discarding the first $2{,}000$ iterations as warm-up (for this problem's own summaries only — see the export note below): the posterior mean and 95% credible interval for each of the 10 pumps' $\theta_i$, and for $\beta$; a one-sentence identification of the most and least reliable pump by posterior mean rate.
3. **Multi-start check:** across your three chains, the maximum pairwise difference (any two chains) in each $\theta_i$'s post-warm-up posterior mean, and in $\beta$'s posterior mean.
4. **Conjugate-conditional moment check:** fix $\beta$ at your reference chain's posterior mean of $\beta$. For each pump, draw $200{,}000$ values directly from $\text{Gamma}(\alpha+y_i,\, \beta_{\text{fixed}}+t_i)$ and report the maximum (over the 10 pumps) absolute difference between the empirical mean/variance of these draws and the closed-form Gamma mean $(\alpha+y_i)/(\beta_{\text{fixed}}+t_i)$ and variance $(\alpha+y_i)/(\beta_{\text{fixed}}+t_i)^2$.
5. **Export.** Per the saved-chain specification below, save your reference chain's **full, un-thinned, all-$20{,}000$-iterations** output (warm-up included — the 2,000-iteration discard above is for this problem's own summaries only, not for what you save).

> **Saved-chain specification.** Save the post-run output as a plain numeric matrix (or data frame) with one row per iteration and one column per parameter, in iteration order, with NO warm-up discarded and NO thinning applied, together with: the seed, the number of iterations, the initial state, and (for MH-type samplers) the proposal scale. Store column names matching the model's parameter names. This exact object is reused in Module 8 (diagnostics) and Module 9 (Rao-Blackwellized density estimation).

For this sampler, "one column per parameter" means eleven columns: $\theta_1,\dots,\theta_{10},\beta$. Keeping $\beta$ as a saved column is not optional bookkeeping — Module 9's Rao-Blackwellized density estimate needs, at every retained iteration, the value of $\beta$ that each $\theta_i$'s full conditional was drawn conditional on, and that is exactly what this column provides.

**Verification:** Tier 2 for the full-conditional forms (standard Poisson-Gamma and Gamma-Gamma conjugacy — your derivations should match the boxed formulas above). Tier 3 for the executed checks (validation log entry PS7.4): multi-start agreement — maximum pairwise difference in any $\theta_i$'s posterior mean across your three chains $< 0.02$, and in $\beta$'s posterior mean $< 0.15$; conjugate-conditional moment check — maximum (over the 10 pumps) $|\text{empirical mean} - \text{shape}/\text{rate}| < 0.01$ and $|\text{empirical variance} - \text{shape}/\text{rate}^2| < 0.01$.

**Discussion note:** (folded) If your synthetic draw gives some pump a small or zero failure count despite a high true rate (Poisson counts are noisy, especially at short exposure times), don't be surprised if the posterior doesn't flag that pump as unreliable — the model can only learn from the data it's given, and a pump that happens not to fail during its observed exposure will look reliable in the posterior regardless of its true underlying rate. That's not a bug; it's an honest description of what the data (don't) support, and worth a sentence in your write-up if it happens to you. The multi-start check is doing real work here, not just ceremony: because $\beta$ links all ten pumps together, a coding error in the hyperparameter update (e.g., using $9\alpha$ instead of $10\alpha$, or forgetting to re-draw $\beta$ every iteration) tends to produce chains that *each* look individually well-behaved (smooth trace, plausible values) but *disagree with each other* systematically — exactly the failure mode multi-start comparison is designed to catch, and exactly the kind of chain-level bug that a single-chain "does it look converged" check would miss. This sampler produces one of this module's two forward-exported chains (see PS7.6 for the other, deliberately failing one) — Module 8 will run diagnostics on this chain's raw, un-thinned output, and Module 9 will use it (specifically, the retained $\beta$ column together with each $\theta_i$'s column) to build a Rao-Blackwellized density estimate of the $\theta_i$ marginals.

---

### PS7.5 — Metropolis-within-Gibbs: a non-conjugate conditional
**Type:** I | **Tier:** 3 | **Core/Optional:** Core | **Time:** 60 min | **Goals:** 6
**Prerequisites:** Reuses your PS7.2 random-walk Metropolis-Hastings step (the accept/reject machinery, not its target).

**Statement:**
Model $n=50$ observations as $x_i \mid \mu,\sigma \sim N(\mu,\sigma^2)$. Put a conjugate prior on the mean, $\mu \sim N(\mu_0{=}0,\, \tau_0^2{=}100)$, but a **non-conjugate** prior on the scale, $\sigma \sim \text{Half-Cauchy}(0,\, s_0{=}5)$ (density $f(\sigma) = \frac{2}{\pi s_0 (1+(\sigma/s_0)^2)}$ for $\sigma>0$) — a common realistic choice, since the usual conjugate inverse-gamma prior on $\sigma^2$ is often a poor default (it puts unwanted mass near zero and is hard to interpret). Generate your synthetic data with true $\mu_{\text{true}}=5$, $\sigma_{\text{true}}=2$, using a seed you set and report.

The full conditional for $\mu$ given $\sigma$ is a standard normal-normal conjugate update (this is the only problem in this module that uses this particular conjugate identity — PS7.1 targets the bioassay logistic posterior, PS7.3 is Beta-Binomial, and PS7.4 is Gamma-Poisson):
$$\mu \mid \sigma, x \;\sim\; N(\mu_n,\tau_n^2), \qquad \tau_n^2=\left(\frac{1}{\tau_0^2}+\frac{n}{\sigma^2}\right)^{-1},\;\; \mu_n=\tau_n^2\left(\frac{\mu_0}{\tau_0^2}+\frac{n\bar x}{\sigma^2}\right).$$
The full conditional for $\sigma$ given $\mu$ has **no closed form** — write it down up to a constant:
$$p(\sigma\mid\mu,x) \;\propto\; \sigma^{-n}\exp\!\left(-\frac{\sum_i(x_i-\mu)^2}{2\sigma^2}\right)\cdot\frac{1}{1+(\sigma/s_0)^2}, \quad \sigma>0.$$
Since you can't sample this directly, update $\sigma$ with a random-walk Metropolis step *inside* the Gibbs loop: propose $\sigma' = \sigma + \delta\,\varepsilon$ with $\varepsilon\sim N(0,1)$ and $\delta=0.5$; reject automatically if $\sigma'\le 0$ (the prior is zero there); otherwise accept with the usual Metropolis probability $\min(1, p(\sigma'\mid\mu,x)/p(\sigma\mid\mu,x))$ — this is the identical accept/reject logic you built in PS7.2, now targeting a different (non-conjugate) density instead of a standard normal.

Run the sampler for $20{,}000$ iterations, alternating a direct draw of $\mu$ (Gibbs) and an MH step for $\sigma$ (Metropolis-within-Gibbs), discarding the first $2{,}000$ as warm-up.

**Deliverable:** The two full-conditional expressions above (with a sentence on why $\sigma$'s has no standard form). Your sampler's $\sigma$-step acceptance rate. Posterior mean and 95% credible interval for $\mu$ and for $\sigma$ (post-warm-up). A 3–5 sentence note comparing your posterior means to the true generating values, and stating in general terms when this hybrid (some parameters Gibbs, some Metropolis) is the right tool — i.e., when some full conditionals are tractable and others aren't, rather than abandoning Gibbs entirely for pure MH or forcing an intractable conditional into a conjugate family it doesn't belong to.

**Verification:** Tier 3 (executed and logged; validation log entry PS7.5). At $n=50$, $n_{\text{iter}}=20{,}000$ (burn-in 2,000), $\delta=0.5$: your posterior mean of $\mu$ should satisfy $|\text{mean} - 5.0| < 1.0$; your posterior mean of $\sigma$ should satisfy $|\text{mean} - 2.0| < 0.7$; your $\sigma$-step acceptance rate should fall in $[0.25, 0.55]$ (this last one is a sanity check that $\delta=0.5$ is reasonably tuned for this problem, not a recovery check — an acceptance rate far outside this band suggests a bug in the $\sigma$ target, not bad luck).

**Discussion note:** (folded) If your acceptance rate is near 0 or near 1, check the sign in your accept/reject comparison and your handling of $\sigma' \le 0$ before assuming your data draw was unlucky — this is the same A5.2-style bug class (inverted inequality) that PS7.7 hunts for directly. The general principle for Goal 6: Metropolis-within-Gibbs is warranted whenever a model has a mix of conjugate and non-conjugate structure — which is the common case for any realistically-specified hierarchical or non-conjugate-prior model, not a rare edge case. You don't need every conditional to be tractable to use Gibbs; you only need *a* valid way to update each block of parameters given the rest, and an MH step (as here) is one such way whenever direct sampling isn't available. This is also why the module doesn't ask you to derive an MH acceptance ratio from scratch a second time: the accept/reject *machinery* from PS7.2 is completely general-purpose — only the target density changes.

---

### PS7.6 — Diagnosing a stuck sampler: a well-separated bimodal target
**Type:** D | **Tier:** 3 | **Core/Optional:** Core | **Time:** 45 min | **Goals:** 3 (failure); feeds Module 8
**Prerequisites:** None (reuses your PS7.2 RW-MH machinery, but any from-scratch RW-MH implementation is fine here).

**Statement:**
Consider the fully specified target $\pi(\theta) = 0.5\,N(\theta; -5, 1) + 0.5\,N(\theta; 5, 1)$ — an equal-weight mixture of two unit-variance normals, five units on either side of zero, ten units apart. By the standard mixture-moment identities ($E[X]=\sum_k w_k\mu_k$, $E[X^2]=\sum_k w_k(\sigma_k^2+\mu_k^2)$), this target's true mean is $0$ and true variance is $26$.

Using your random-walk Metropolis-Hastings implementation (PS7.2), sample from $\pi$ with a **deliberately small** proposal scale $\delta=0.5$, starting from a **single** initial point $\theta_0 = -5$ (inside the left mode), for $20{,}000$ iterations. Report your seed. Then, *for contrast only* (not part of the failure case itself), rerun with a larger scale $\delta=6$ from the same start and seed, and record the same summaries.

**Deliverable:** For the $\delta=0.5$ run: acceptance rate; sample mean and variance; the fraction of iterations with $\theta>0$ (i.e., how often the chain ever reached the right mode); a trace plot of $\theta_t$ vs. $t$. Do the same four items for the $\delta=6$ contrast run. In 3–5 sentences, using the trace plot and the mode-occupancy fraction (not just the acceptance rate) as your evidence, diagnose *why* the $\delta=0.5$ chain fails and *why* the acceptance rate alone would have been a misleading diagnostic here (recall PS7.2's lesson that acceptance rate and mixing quality can point in different directions). Save the $\delta=0.5$ chain per the specification below — this is the module's deliberately **failing** export.

> **Saved-chain specification.** Save the post-run output as a plain numeric matrix (or data frame) with one row per iteration and one column per parameter, in iteration order, with NO warm-up discarded and NO thinning applied, together with: the seed, the number of iterations, the initial state, and (for MH-type samplers) the proposal scale. Store column names matching the model's parameter names. This exact object is reused in Module 8 (diagnostics) and Module 9 (Rao-Blackwellized density estimation).

For this problem, save the $\delta=0.5$, $\theta_0=-5$ chain (single column, $\theta$) — this is the chain Module 8 will compute R-hat on and, in its capstone problem, diagnose and attempt to fix.

**Verification:** Tier 2 for the target's true mean/variance (elementary finite-mixture moment identity — no citation beyond the formula itself). Tier 3 for the failure signature and the contrast run (executed and logged; validation log entry PS7.6): for the $\delta=0.5$ run, you should observe $|\text{sample mean} - 0| > 3$ and a right-mode ($\theta>0$) visit fraction $< 0.01$ — **this is the expected, verified failure**, not a sign of a bug in your sampler. For the $\delta=6$ contrast run, $|\text{sample mean} - 0| < 1.0$, $|\text{sample variance} - 26| < 3.0$, and right-mode visit fraction $\in [0.30, 0.70]$.

**Discussion note:** (folded) This failure is not a rare, unlucky draw — it is the deterministic consequence of the proposal scale, reproducible for essentially any seed with these settings, because a $\delta=0.5$ step (roughly half a mode's own width) has essentially no chance of ever proposing a jump across a 10-unit gap of near-zero target density. Everything about this chain *looks* locally healthy if you only look inside the one mode it's stuck in: reasonable acceptance rate (≈0.84, arguably "too high" by the PS7.2 moderate-acceptance-rate lesson, which is itself a clue), a trace plot that looks like it's "settled," a sample variance that looks like a believable single-mode variance (≈1, matching each component's own variance). Nothing *local* to the chain's own output reveals that an entire second mode, containing half the target's mass, is missing — you only know because you were told the target's true form in advance. Betancourt's discussion of this phenomenon calls it "metastability": a sampler can settle into what looks, by every local measure, like a converged chain, while remaining completely unaware that a substantial share of the target's probability lives somewhere it has never visited. This is exactly why Module 8 pairs single-chain diagnostics with multi-chain, dispersed-start comparisons: a second chain started near $\theta_0=5$ would reveal the discrepancy that this one chain, however long you ran it, never would.

---

### PS7.7 — Bug hunt: three ways a Metropolis sampler can look right and be wrong *(optional)*
**Type:** D | **Tier:** 1+3 | **Core/Optional:** Optional | **Time:** 45 min | **Goals:** 2, 3 (does not count toward Goal 3's from-scratch requirement)
**Prerequisites:** None.

**Statement:**
*Part A (conceptual lead-in, no code).* Suppose you replaced the usual stochastic Metropolis accept/reject rule with a **greedy** rule: accept the proposal if its target density exceeds the current point's ($r>1$), otherwise always reject (stay put). For a unimodal target, what does the resulting chain converge to, and why is that generally *not* useful for computing posterior expectations (as opposed to just finding the posterior mode)? Answer in 2–4 sentences.

*Part B (bug hunt).* Below is a *reconstruction* (not verbatim from any source) of a random-walk Metropolis sampler targeting a density via a function `target_logpdf(theta)`. It contains three planted bugs. Find all three, and for each: name the line, explain in 1–2 sentences what it does wrong, and explain its *statistical* consequence for the resulting chain (not just "it's a syntax issue").

```
function metropolis_sampler(theta0, n_iter, delta):
    theta_current = theta0
    chain = array of length n_iter

    for t in 1..n_iter:
        theta_propose = theta_current + delta * standard_normal_draw()
        log_ratio = target_logpdf(theta_propose) - target_logpdf(theta_current)

        u = uniform_draw(0, 1)
        if u > log_ratio:
            theta_current = theta_propose

        chain[t] = theta_propose

    return chain
```

*Part C (fix and rerun).* Correct all three bugs. Using your fixed sampler, target $N(0,1)$ with $\delta=1$, run $20{,}000$ iterations with a seed you set and report. Report the acceptance rate, sample mean, and sample variance.

**Deliverable:** Part A's answer. Part B's three bug identifications (location + mechanism + statistical consequence). Part C's corrected code, acceptance rate, sample mean, and sample variance.

**Verification:** Part A is tier 2 (a standard, derivable conceptual fact about greedy vs. stochastic acceptance — any correct reasoning about hill-climbing vs. sampling reaches the same conclusion: the chain collapses onto the mode and never characterizes the distribution's spread). Part B's three bugs are tier 1 (their existence and count — exactly three — are confirmed against the Aalto BDA course's Assignment 5 bug-hunt notebook; validation log entry PS7.7 records the citation). Part C is tier 3 (executed and logged; validation log entry PS7.7): at $\delta=1$, $n_{\text{iter}}=20{,}000$, your corrected sampler's acceptance rate should fall in $[0.64, 0.76]$, sample mean in $[-0.15, 0.15]$, sample variance in $[0.80, 1.20]$ — the same ballpark as your PS7.2 $\delta=1$ results, since this is structurally the same sampler once fixed.

**Discussion note:** (folded) The three bugs, if you're stuck: (1) `log_ratio` is a *log*-ratio, but it's never exponentiated before being compared to a draw from $\text{Uniform}(0,1)$ — comparing a log-quantity (which can be very negative) directly against a probability-scale draw is not the same computation as comparing the actual ratio; (2) the comparison direction is backwards — correct Metropolis-Hastings accepts when the uniform draw is *less than* the (true, exponentiated) ratio, favoring moves toward higher relative density, not the reverse; (3) the chain records `theta_propose` every iteration regardless of whether the move was accepted, so a rejected proposal is still written into the chain as if it had happened — the recorded sequence is then not a valid realization of the Markov chain at all. Bugs (1) and (2) compound in this reconstruction to produce a chain that "accepts" almost every large downhill move and diverges outward without bound (check your own numbers against the pre-fix pathology noted in the validation log if you want a sanity check that you've reproduced it) — a dramatic, easy-to-recognize symptom, but the more instructive lesson is that (3) alone, in isolation, would have produced a chain that still looks numerically tame (values still near the target's support) while being silently wrong, which is a much harder bug to catch by eyeballing the output. This is why "does the trace plot look reasonable" is never sufficient verification on its own — you need to know *what* the code is supposed to be doing, not just whether its output looks plausible.

---

## Alignment matrix — Module 7

| Goal | Text | Problem(s) / justification |
|---|---|---|
| 7.1 | Explain Sampling Importance Resampling (SIR) as a bridge from importance sampling to approximate sampling — connecting back to Module 2 and framing the central challenge that MCMC addresses | **PS7.1** (primary vehicle: implements SIR literally reusing the student's PS2.3 importance sampler, discussion note frames the IS→MCMC bridge) |
| 7.2 | Derive the Metropolis-Hastings algorithm from the detailed balance condition, and explain how the acceptance ratio enforces the correct stationary distribution | **PS7.2, Part A** (derivation from detailed balance to the symmetric-proposal acceptance formula) |
| 7.3 | Implement Metropolis-Hastings and characterize how proposal distribution choice governs the tradeoff between acceptance rate and autocorrelation | **PS7.2, Part B** (primary vehicle: from-scratch RW-MH at 3 proposal scales, acceptance-rate/autocorrelation tradeoff). Per the WO, PS7.7's bug-hunt (optional) does **not** count toward this goal — it interrogates given code rather than building a sampler from scratch. |
| 7.4 | Derive Gibbs sampling from the structure of full conditional distributions, and explain why acceptance is guaranteed at every step | **PS7.3** (derive both full conditionals + implement + explain *both* clauses, including the guaranteed-acceptance-as-MH-special-case clause per `PSDEP-M7SlateResolution.md` M7-D1) + **PS7.4** (implement/export on the ten-pump hierarchical model; derives and uses the gamma full conditionals) |
| 7.5 | Distinguish random-scan from deterministic-scan Gibbs — including why the deterministic-scan version does not satisfy detailed balance in general — and explain when each framing is appropriate | *(Per DG-P4 / `PSDEP-Phase0Resolutions.md`: routed to the program's conceptual questions, not a drafted problem. No harvested or original candidate exists program-wide for this scan-order distinction — see the Ch. 6/7 harvest summaries — and the spec's own §6 language explicitly permits this disposition. No problem drafted; do not read this row's absence as an oversight.)* |
| 7.6 | Implement Metropolis-within-Gibbs for models where full conditionals are not available in closed form, and identify when this hybrid is warranted | **PS7.5** (conjugate mean / non-conjugate half-Cauchy scale; MH-within-Gibbs reusing PS7.2's accept/reject machinery) |
| 7.7 | Recognize SIR, MH, and Gibbs as members of a common family of approximate sampling strategies — each solving the same core problem by different design choices | *(Carries no implementation verb — per WO-M7 §2, exercised through discussion notes rather than a standalone problem.)* Discussion notes of **PS7.1** (SIR framed explicitly against the "common family" question), **PS7.2** (MH's different mechanism/failure-mode contrast with SIR), and **PS7.3** (Gibbs as an MH special case) build this recognition cumulatively; also picked up by the program's conceptual questions (outside this problem set's scope). |

## Module 7 hours (re-added by hand from the drafted problems)

| Core problems | Core hours (re-summed) | Optional hours (uncounted) | Budget (§5) |
|---|---|---|---|
| 6 (PS7.1–PS7.6) | 40+75+50+75+60+45 = 345 min = **5.75 hr** | PS7.7 = 45 min | 5–6 hr |

Matches the WO's own slate-resolved planning figure (345 min / 5.75 hr) exactly; within the §5 budget.

---

## Module 8 — MCMC Diagnostics & Reliability

### PS8.1 — ACF and ESS From Scratch on Your Stored Chain

**Type:** I | **Tier:** 3 | **Core/Optional:** Core | **Time:** 45 min | **Goals:** 1, 2

**Prerequisites:** requires your saved PS7.4 chain (the ten-pump hierarchical Gamma-Poisson Gibbs sampler).

**Statement:**
Recall the saved-chain specification from Module 7:

> **Saved-chain specification.** Save the post-run output as a plain numeric matrix (or data frame) with one row per iteration and one column per parameter, in iteration order, with NO warm-up discarded and NO thinning applied, together with: the seed, the number of iterations, the initial state, and (for MH-type samplers) the proposal scale. Store column names matching the model's parameter names. This exact object is reused in Module 8 (diagnostics) and Module 9 (Rao-Blackwellized density estimation).

Load your saved PS7.4 chain (11 columns: theta_1, ..., theta_10, beta; 20,000 rows). Discard the first 2,000 iterations as warm-up — the same convention you used when reporting PS7.4's posterior summaries — leaving 18,000 retained draws per column.

For a retained column of draws x_1, ..., x_n with sample mean x̄, the lag-k autocorrelation is
ρ_k = [Σ_{t=1}^{n−k} (x_t − x̄)(x_{t+k} − x̄)] / [Σ_{t=1}^{n} (x_t − x̄)²].

Implement this from scratch and compute ρ_k for k = 0, ..., 50, for every one of the eleven retained columns.

Then implement the effective sample size (ESS) from scratch using the **initial-positive-sequence estimator**: pair consecutive autocorrelations as Γ_m = ρ_{2m} + ρ_{2m+1} for m = 0, 1, 2, ...; let M be the largest index such that Γ_0, ..., Γ_M are all strictly positive (stop pairing at the first m with Γ_m ≤ 0); the integrated autocorrelation time is τ = −1 + 2·Σ_{m=0}^{M} Γ_m, and ESS = n / τ. Apply this to all eleven columns.

Cross-check both your ACF and your ESS against a named library implementation available in your chosen language (R1.4 — library as oracle only, never as a substitute for your own implementation): for example, in Python, `statsmodels.tsa.stattools.acf` and `arviz.ess` (use the classical, non-rank-normalized ESS option — in `arviz` this is `method="mean"`, not the rank-normalized default — since your from-scratch estimator is the classical definition and the comparison must use matching definitions); in R, `stats::acf` and `coda::effectiveSize`; in Julia, `StatsBase.autocor` and `MCMCChains.ess` (classical/basic option). Whichever library you use, name it in your write-up.

Finally, write 3–5 sentences connecting your ESS results to the ACF structure you observed: which of the eleven parameters showed the highest lag-1 autocorrelation and the lowest ESS, which showed the lowest autocorrelation and highest ESS, and why that pattern is consistent with beta's role as a hyperparameter shared across all ten pumps versus each theta_i being informed more directly by its own pump's data.

**Deliverable:** a table (or plot) of ρ_k for k = 0..50 for at least beta and theta_5, a table of ESS (from-scratch and library) for all eleven parameters, and the 3–5 sentence interpretation described above.

**Verification:** [Tier 3 — executed reference run, logged in `ValidationLog` under PS8.1] For every one of the eleven saved parameters: the max absolute difference between your from-scratch ρ_k and the library ACF value, over lags k = 0..50, should be < 0.01; and |ESS_scratch − ESS_library| / ESS_library should be < 0.05 (5%).

**Discussion note:** (folded) A correct implementation should show near-exact agreement between the from-scratch and library ACF (the two are computing the same quantity by the same definition, so any real gap points to a bug — an off-by-one in the lag indexing or a bias-correction difference are the usual culprits). ESS agreement is looser than ACF agreement because different implementations use different truncation rules (initial-positive-sequence here; some libraries default to a fixed-lag cutoff or a rank-normalized transform) — a 5% gap is expected noise from that choice, not a red flag. beta typically shows the highest lag-1 autocorrelation and lowest ESS of the eleven parameters: it is the one hyperparameter every pump's Gibbs step depends on, so it changes more slowly than a pump-specific theta_i that is pulled hard toward its own (t_i, y_i) at every sweep. A student who instead finds a pump-level theta_i with very low ESS should check whether that pump has an unusual y_i/t_i ratio (an extreme observation can slow local mixing even in a Gibbs sampler with guaranteed acceptance).

---

### PS8.2 — Multi-Chain R-hat on a Healthy and a Failing Sampler

**Type:** I/V | **Tier:** 3 | **Core/Optional:** Core | **Time:** 50 min | **Goals:** 3

**Prerequisites:** requires your saved PS7.4 chain (healthy pump Gibbs) and your saved PS7.6 chain (failing bimodal RW-MH); you will also re-run each sampler from new starting points (your own PS7.4/PS7.6 code, not a new sampler).

> **Saved-chain specification.** Save the post-run output as a plain numeric matrix (or data frame) with one row per iteration and one column per parameter, in iteration order, with NO warm-up discarded and NO thinning applied, together with: the seed, the number of iterations, the initial state, and (for MH-type samplers) the proposal scale. Store column names matching the model's parameter names. This exact object is reused in Module 8 (diagnostics) and Module 9 (Rao-Blackwellized density estimation).

**Statement:**
This problem implements the **classic (Gelman-Rubin) R-hat** from its definition — one specific definition among several in circulation (a rank-normalized alternative exists; that contrast is left to the optional PS8.3). State explicitly in your write-up that you are implementing this classic form.

For m chains of n retained draws each of some scalar parameter, with chain means ψ̄_1, ..., ψ̄_m and grand mean ψ̄:

- within-chain variance: W = (1/m) Σ_j s_j², where s_j² = 1/(n−1) Σ_t (ψ_{jt} − ψ̄_j)²
- between-chain variance: B = n/(m−1) Σ_j (ψ̄_j − ψ̄)²
- pooled variance estimate: Var⁺ = ((n−1)/n)·W + (1/n)·B
- R-hat = √(Var⁺ / W)

Implement this from scratch (no library R-hat function — this is the from-scratch core of the problem; a library implementation may only be used afterward as an optional sanity check, per R4, and is not required).

**Healthy configuration:** re-run your PS7.4 pump Gibbs sampler four times, from dispersed initial values of beta: 0.1, 1.0, 5.0, and 20.0 (use four different seeds, one per chain, of your choice), 20,000 iterations each. Discard the first 2,000 iterations of each chain as warm-up. Compute R-hat for all eleven saved parameters (theta_1, ..., theta_10, beta).

**Failing configuration:** re-run your PS7.6 bimodal RW-MH sampler four times, at the same delta = 0.5 proposal scale that produced the original documented failure, from four dispersed starting values: theta0 = −8, −5, 5, and 8 (again, four different seeds, one per chain), 20,000 iterations each. Discard the first 2,000 iterations as warm-up (applying the same convention as the healthy configuration, for a like-for-like comparison). Compute R-hat.

Produce trace plots for both configurations (all four chains overlaid on one plot per configuration) and interpret: what does each configuration's R-hat and trace plot tell you, and what does it *not* tell you about whether the chain has converged?

**Deliverable:** your R-hat implementation; a table of R-hat for all eleven parameters under the healthy configuration and R-hat under the failing configuration; overlaid trace plots for both configurations; 3–5 sentences of interpretation.

**Verification:** [Tier 3 — executed reference run, logged in `ValidationLog` under PS8.2] Healthy configuration: R-hat should be < 1.01 for all eleven parameters. Failing configuration: R-hat should be > 1.5.

**Discussion note:** (folded) The healthy configuration's R-hat near 1 across all eleven parameters, from four widely dispersed starting values of beta, is exactly what "the chain's outcome doesn't depend on where you started it" looks like quantitatively — this is the core promise R-hat is designed to check. The failing configuration's R-hat is large because the between-chain variance B is enormous relative to the within-chain variance W: each of the four chains is trapped near its own starting mode (two chains end up clustered near −5, two near +5), so the "between-chain spread" looks like real posterior spread even though it is actually four different local, wrong pictures of the posterior. This is also the sharpest illustration of what R-hat *cannot* detect on its own: a **single** chain stuck in one mode (as in your original PS7.6 run) can have excellent within-chain behavior and would show no R-hat problem at all if you never ran a second chain from a different start — R-hat is fundamentally a multi-chain diagnostic, and a healthy-looking R-hat from a single chain (or from multiple chains that all happen to start in the same trap) proves nothing. This is why PS8.5's capstone requires you to actually change something about the sampler (not just watch it longer) before re-evaluating. For a sense of scale from outside this course: Vehtari's Aalto BDA Assignment 5 reports a similarly-failing Metropolis sampler on a bioassay model showing R-hat ≈ 2.28–2.29 and an ESS of only ≈ 5 out of 8,000 nominal post-warmup draws (cite as approximate context only — those exact decimals are specific to that assignment's own seed and since-modified code, not an independently reproducible target here); your own failing configuration's R-hat (well above 1.5) is the same species of result, generated and logged independently rather than borrowed from that source.

---

### PS8.3 — When Classic R-hat Is Fooled *(Optional)*

**Type:** V/D | **Tier:** 1+3 | **Core/Optional:** Optional | **Time:** 30 min | **Goals:** 3

**Prerequisites:** None (this problem does not use your PS7.4/PS7.6 chains — it constructs its own small example).

**Statement:**
The classic R-hat you implemented in PS8.2 is one specific way of comparing chains — based on within- and between-chain variance of the raw values. This problem shows a case where that specific choice can be fooled.

Construct two independent "chains": draw n = 1,000 i.i.d. values from a standard normal N(0,1) for chain 1, and 1,000 i.i.d. values from a Student-t distribution with 3 degrees of freedom for chain 2 (report your seed). Treat these as if they were two MCMC chains that had each individually "converged" — one to N(0,1), one to t₃ — and compute your PS8.2 classic R-hat implementation on this pair.

A rank-normalized version of R-hat exists (Vehtari et al., 2021), which first jointly ranks all pooled draws across chains and transforms the ranks to a normal scale before computing the same variance-ratio formula. In a published two-chain example matching this same N(0,1)-vs-t₃ construction, the classic R-hat comes out ≈ 1 despite the chains obviously not sampling the same distribution, while the rank-normalized version comes out at 1.39 — well above the recommended convergence threshold of 1.01.

You may attempt your own from-scratch rank-normalized R-hat as an open-ended exploration (no fixed target is given for it here — see the discussion note), or you may instead reason through, in your own words, why a rank-based transform would be more sensitive than a raw-variance comparison to two chains having different distributional shapes even when their classic R-hat looks fine. Either way, your write-up must explain what this example shows about what R-hat can and cannot detect.

**Deliverable:** your two constructed "chains"; your classic R-hat computation on them; 3–5 sentences explaining what the classic-R-hat-near-1-but-genuinely-different-distributions result shows about the limits of that diagnostic (and, if you attempted it, your own rank-normalized computation with honest reporting of what you got).

**Verification:** [Tier 1 — cite Annex A7.1/A8.1 for the published classic R̂ ≈ 1 and rank-normalized R̂ = 1.39 vs. the 1.01 threshold, from Vehtari's Aalto BDA course material (cite by content — "the N(0,1)-vs-t₃ example where classic R̂ ≈ 1 but rank-normalized R̂ = 1.39" — not by an assignment sub-part number, which drifts across course years). Tier 3 — executed reference run, logged in `ValidationLog` under PS8.3, for your own classic R-hat: it should fall in [0.95, 1.10] at n = 1,000.] No fixed numeric target is given for a self-implemented rank-normalized computation; if you attempt one, report it as an open exploration rather than a pass/fail check.

**Discussion note:** (folded) Your own classic R-hat on this N(0,1)-vs-t₃ pair should land very close to 1, reproducing the cited surprising result: two chains that are visibly, obviously sampling different distributions (different variance, different tail weight) can still show a "textbook-good" classic R-hat, because that statistic is built entirely from first- and second-moment (mean/variance) comparisons and has no way to see a difference in tail shape once means and rough scales roughly align. This is precisely the motivation for the rank-normalized version: transforming to ranks before comparing is designed to be sensitive to distributional differences that a pure variance-ratio statistic can miss. If you attempted your own from-scratch rank-normalization, you may well have found (as this session's own reference run did) that a plain rank-transform on i.i.d. draws does not by itself reproduce the published 1.39 — that number depends on details of Vehtari et al.'s reference implementation (which also incorporates chain-splitting and, for other diagnostics, "folding") that go beyond a first attempt at the idea. That is a legitimate, informative finding, not a failure on your part: the qualitative lesson (R-hat's classic form can be blind to shape differences; rank-normalization is designed to help) stands regardless of whether you can reproduce the exact published constant from first principles in half an hour.

---

### PS8.4 — Does Thinning Help? A Fixed-Budget Comparison

**Type:** V | **Tier:** 1+3 | **Core/Optional:** Core | **Time:** 35 min | **Goals:** 5

**Prerequisites:** requires your saved PS7.4 chain (healthy pump Gibbs); you will also re-run this sampler many times (your own PS7.4 code) to assess estimator variance empirically.

> **Saved-chain specification.** Save the post-run output as a plain numeric matrix (or data frame) with one row per iteration and one column per parameter, in iteration order, with NO warm-up discarded and NO thinning applied, together with: the seed, the number of iterations, the initial state, and (for MH-type samplers) the proposal scale. Store column names matching the model's parameter names. This exact object is reused in Module 8 (diagnostics) and Module 9 (Rao-Blackwellized density estimation).

**Statement:**
R&C's Chapter 8 includes a classic, fully general result (Exercise 8.1, solved): subsampling — thinning — a Markov chain average can only increase its variance relative to using every retained draw. State this citation in your write-up as the theoretical direction; you do not need to reproduce its proof.

This problem checks that direction empirically, and also investigates the one situation where thinning is still sometimes defended in practice. Using your PS7.4 pump Gibbs sampler (n_iter = 20,000, burn_in = 2,000, so 18,000 retained draws per run) and tracking the posterior mean of beta, run **200 independent replications** (200 different seeds) of the full sampler. From each replication's 18,000 retained draws, compute three different estimates of beta's posterior mean:

1. **All draws:** the mean of all 18,000 retained draws.
2. **Thinned:** the mean of every 10th draw across the full 18,000 (giving m = 1,800 draws, spread across the whole run).
3. **First-m unthinned:** the mean of just the first 1,800 retained draws (a contiguous block, the same size as (2), but not thinned).

Across your 200 replications, compute the empirical variance of each of these three estimators (i.e., the variance, over replications, of the 200 values each estimator produced). Compare the three variances and relate the ordering to the R&C 8.1 result.

Then, in 3–5 sentences, identify the narrow circumstances under which thinning is still practically justified (hint: compare estimator (2) against estimator (3) rather than against (1) — what does that comparison tell you about a situation where you can only afford to *store* a fixed number of draws?).

**Deliverable:** the three estimator-variance values (from 200 replications) and their pairwise ratios; the R&C 8.1 citation; 3–5 sentences on the narrow practical justification for thinning.

**Verification:** [Tier 1 — cite R&C Ch. 8 Exercise 8.1 (solved) for the theoretical direction: thinning cannot reduce variance relative to using every draw. Tier 3 — executed reference run, logged in `ValidationLog` under PS8.4.] You should observe Var(thinned, m=1800) / Var(all, 18000) > 2, and Var(first-1800-unthinned) / Var(thinned, m=1800) > 1.05.

**Discussion note:** (folded) The first inequality is the R&C 8.1 result made concrete: using only 1,800 of your 18,000 draws (even spread evenly across the whole run) always costs you variance relative to using everything — thinning discards information, full stop, and this problem's reference run showed the cost is not small (roughly 5–6x the variance, consistently, across many independent trials). The second inequality is the more interesting, easy-to-miss point: *if* you are somehow constrained to store only 1,800 draws total (a genuine memory/storage constraint, not a compute one), spreading those 1,800 draws across the whole run (thinning) still beats keeping only the first 1,800 draws you happened to generate — a short contiguous block is more autocorrelated internally than a thinned sample of the same size, so it carries less independent information per draw. This is the *only* legitimate practical argument for thinning: not that it improves efficiency (it never does, relative to keeping everything you generated), but that *given a hard storage budget smaller than your full run*, spacing out what you keep beats truncating to a short run of the same stored size. If your compute budget allows generating and keeping all the draws, there is no argument for thinning at all.

---

### PS8.5 — Capstone: Diagnose, Adjust, Rerun, Re-Evaluate

**Type:** D | **Tier:** 3 | **Core/Optional:** Core | **Time:** 50 min | **Goals:** 6

**Prerequisites:** requires your saved PS7.6 chain (failing bimodal RW-MH) and your PS8.2 R-hat implementation and result for that same failing configuration; you will re-run the PS7.6 sampler itself (your own code) with a changed proposal scale.

> **Saved-chain specification.** Save the post-run output as a plain numeric matrix (or data frame) with one row per iteration and one column per parameter, in iteration order, with NO warm-up discarded and NO thinning applied, together with: the seed, the number of iterations, the initial state, and (for MH-type samplers) the proposal scale. Store column names matching the model's parameter names. This exact object is reused in Module 8 (diagnostics) and Module 9 (Rao-Blackwellized density estimation).

**Statement:**
This is the module's capstone: a complete iteration of the workflow Modules 7 and 8 have been building toward. You will not just observe a failure — you will act on it.

**Step 1 — Diagnose, formally this time.** In PS7.6 you already diagnosed this failure qualitatively — from the trace plot and the mode-occupancy fraction. Now formalize that diagnosis with the quantitative tools you have since built. Using your stored PS7.6 failing chain (delta = 0.5, single start at theta0 = −5.0), compute its effective sample size using your PS8.1 from-scratch implementation. Then recall (do not recompute) the multi-chain R-hat you found in PS8.2 for this exact failing configuration (4 dispersed starts, delta = 0.5). State both numbers together with your trace plot, and write 2–3 sentences on what each one does and does not tell you on its own — paying particular attention to whether the formal single-chain number (the ESS) is actually as decisive as the qualitative evidence you already had in PS7.6.

**Step 2 — Adjust.** Based on your diagnosis, change **one thing** about the sampler to address the identified problem: increase the proposal scale from delta = 0.5 to **delta = 6.0**. (You are not building a new sampler — this is the same PS7.6 code, one parameter changed.) You have, of course, already seen a single delta = 6.0 chain mix well: PS7.6's contrast run. That is precisely the point of this capstone's remaining steps — one well-behaved chain from one starting point is a promising sign, not a verdict, and the question Steps 3–4 answer is whether the fix holds up to the multi-chain, dispersed-start standard of evidence this module has established.

**Step 3 — Rerun.** Re-run the adjusted sampler (delta = 6.0) from the same four dispersed starting points you used in PS8.2's failing configuration (theta0 = −8, −5, 5, 8), 20,000 iterations each, with fresh seeds. Discard the first 2,000 iterations as warm-up, as in PS8.2.

**Step 4 — Re-evaluate.** Recompute the multi-chain R-hat on these four new chains. Pool all four chains' retained draws and compute the pooled sample mean and variance. Compare against the target's known true moments (mean = 0, variance = 26 — the standard mixture-moment identity, tier-2). Also report each chain's fraction of iterations with theta > 0 (a simple check that each chain actually visited the right-hand mode, not just the left).

Write a capped write-up (8–10 sentences total across all four steps) documenting the decision at each step: what the diagnosis showed, why you chose this particular adjustment (rather than, say, a longer chain or a different starting point), what changed, and how you know the new configuration is trustworthy.

**Deliverable:** the Step 1 diagnosis (ESS, recalled R-hat, trace plot, 2–3 sentences); the Step 2 adjustment stated explicitly; the Step 3 rerun's trace plots (all four chains); the Step 4 re-evaluation (R-hat, pooled mean/variance vs. known truth, right-mode fractions); the capped 8–10 sentence workflow write-up.

**Verification:** [Tier 3 — executed reference run, logged in `ValidationLog` under PS8.5.] After adjustment: multi-chain R-hat should be < 1.01; the pooled sample mean should satisfy |mean − 0| < 1.0; the pooled sample variance should satisfy |variance − 26| < 3.0; each chain's right-mode-visit fraction should fall in [0.3, 0.7].

**Discussion note:** (folded) Your Step 1 diagnosis should show a genuinely ambiguous single-chain signal: the from-scratch ESS on the failing chain is a small fraction of its retained draws — clearly not great, but the number alone doesn't scream "catastrophic failure" the way you might expect (a low ESS is also just what a slow-mixing-but-otherwise-fine chain looks like). This session's own reference run found the failing chain's ESS to be the *same order of magnitude* as the healthy, post-adjustment chain's ESS — a genuinely useful, slightly uncomfortable finding: single-chain ESS alone did not cleanly separate "broken" from "fine" here. Note what that means against your PS7.6 work: the qualitative evidence you already had there (a trace that never approaches the second mode; a near-zero mode-occupancy fraction) was *more* decisive than the formal single-chain statistic you have now added — formalizing a diagnosis does not automatically strengthen it. What did the job decisively was the multi-chain R-hat (only visible once you have more than one dispersed start) together with that same qualitative fact. Relatedly, Step 4's tolerance bands are deliberately the same ones your PS7.6 contrast run cleared — what is new here is not the bands but the standard of evidence: four dispersed chains agreeing with each other, not one chain agreeing with the truth. This is this module's version of R&C's Example 8.3/8.4 (the noisy AR(1) model), where every one of the chapter's diagnostics reported a clean pass on a chain that had, in fact, never left a minor secondary mode — a standing reminder that a green light from any single diagnostic, run on a single chain, is never sufficient proof of convergence. It is also a concrete instance of Betancourt's "Towards a Principled Bayesian Workflow" Step Ten: when a computational method's self-diagnostics fail, the appropriate response is to return and reconfigure the algorithm (here: the proposal scale) — and, more generally, if reconfiguring the algorithm had *not* resolved the failure, the appropriate next move would be to question the model or experimental setup itself, not to keep re-tuning indefinitely. Separately, and worth noting for its own sake: your Module 7 Gibbs sampler (PS7.3/PS7.4) never had a "proposal scale" to tune in the first place, because it accepts every draw by construction — but as this chain's original delta = 0.5 run showed (acceptance rate ≈ 0.84, yet total failure to mix across modes), a *high acceptance rate is not itself evidence of good mixing* for a Metropolis-type sampler either; acceptance rate and genuine exploration are different things, and this capstone's own diagnosis step is a direct demonstration of that gap.

---

### PS8.6 — Warm-Up Sensitivity on a Badly Initialized Run

**Type:** I | **Tier:** 3 | **Core/Optional:** Core | **Time:** 30 min | **Goals:** 4

**Prerequisites:** requires your PS7.4 pump Gibbs sampler code (you will re-run it from a new, deliberately poor initial state — this is not your saved PS7.4 chain itself, but a fresh, short rerun of the same code) and your PS7.4 long-run converged posterior mean of beta, which serves as this problem's baseline.

**Statement:**
Initialize your PS7.4 pump Gibbs sampler with a deliberately poor starting value: set the initial beta to **1000** (roughly 170 times your converged posterior mean of beta from PS7.4). Run the sampler for only **10 iterations** — deliberately short, so that the influence of the starting value is not washed out by averaging over thousands of draws.

A single 10-iteration run's outcome is noisy, so you will average over **30 independent replications** (30 different seeds, same bad initial beta = 1000, same 10-iteration length each). For each replication, compute two estimates of beta's posterior mean: the mean of **all 10 draws** ("with warm-up"), and the mean of **the last 8 draws, discarding the first 2** ("without warm-up"). For each of the two estimates, compute its absolute gap from your PS7.4 baseline (the converged posterior mean of beta from your long, well-initialized PS7.4 run). Average each gap across your 30 replications.

Repeat the same comparison for theta_5 (pump 5), using the same 30 replications and your PS7.4 baseline posterior mean for theta_5.

Then, in a few sentences, identify which draws should not be retained and why — connecting this to the idea that a chain needs to run long enough to reach the *typical set* of the posterior before its draws are representative, and explain what you observe about whether beta or theta_5 is more sensitive to the poor initialization.

**Deliverable:** your 30-replication average gaps (with vs. without warm-up) for both beta and theta_5; the ratio of the two gaps for each parameter; 3–5 sentences of interpretation.

**Verification:** [Tier 3 — executed reference run, logged in `ValidationLog` under PS8.6.] Averaged over your 30 replications, the average gap using all 10 draws should exceed the average gap using the last 8 draws (first 2 discarded) by at least 50% (ratio > 1.5), for beta.

**Discussion note:** (folded) A single 10-iteration replication's with/without comparison can go either way — this session's own check found the "discard warm-up" side smaller in only about 84% of individual short replications, which is exactly why this problem asks you to average over 30 of them rather than trust any one run. That is not a flaw in the exercise; it is itself an honest lesson about warm-up: the *benefit* of discarding early draws is a statement about reducing systematic bias in expectation, not a guarantee that removes noise from any single short run. Averaged over enough replications, the benefit becomes clearly visible (this session's reference run found the with-warm-up gap roughly 2.3–2.8 times the without-warm-up gap, consistently, across several independent 30-replication batches). You should also notice that beta (the shared hyperparameter) shows a larger absolute gap than theta_5 (a pump-specific parameter) under the bad initialization — beta starts furthest, in relative terms, from its equilibrium value (1000 vs. a true posterior mean near 6), while each theta_i is pulled hard toward its own pump's data on the very first Gibbs step regardless of beta's starting value. The general principle Goal 4 wants you to take from this: draws generated before the chain has reached the typical set of the posterior are not samples *from* the posterior, and averaging them in — even just a couple of badly-placed early draws in a short chain — measurably pulls your estimate away from the truth in the direction of wherever you happened to start.

---

## Alignment Matrix — Module 8

| Goal | Text | Problem(s) / justification |
|---|---|---|
| 8.1 | Explain effective sample size as the central measure of MCMC output quality — distinguishing it from raw sample count and connecting it to the autocorrelation structure of the chain | PS8.1 |
| 8.2 | Compute and interpret autocorrelation function estimates from MCMC output, and explain what high autocorrelation implies for the reliability of downstream estimates | PS8.1 |
| 8.3 | Apply trace plots, R-hat, and ESS as principled convergence diagnostics — understanding what each measures and what it can and cannot detect | PS8.2 (core: classic R-hat, trace plots, and the R-hat-is-fundamentally-multi-chain limitation; ESS ceiling from PS8.1 also feeds this). PS8.3 (optional depth only): the classic-vs-rank-normalized "R-hat can be fooled" contrast. Per `PSDEP-M8SlateResolution.md` M8-D2, core coverage of this goal rests on PS8.2 alone and must not depend on PS8.3 — satisfied, since PS8.3 is optional and PS8.2 independently exercises trace plots, R-hat (with an explicit statement of which definition), and the "what can/cannot be detected" framing (the single-chain-vs-multi-chain point in PS8.2's own discussion note). |
| 8.4 | Explain warm-up and its role in allowing the chain to reach the typical set, and distinguish between samples that should and should not be retained | PS8.6 (sole discharge, per M8-D1: standalone problem, not a PS8.5 sub-part) |
| 8.5 | Explain why thinning does not improve statistical efficiency, and identify the narrow circumstances where it may be practically justified | PS8.4 |
| 8.6 | Develop a reliable iterative workflow for running a sampler, evaluating its output, and deciding whether to trust results or return to the sampler | PS8.5 |

## Module 8 Hours

| Problem | Core/Optional | Time |
|---|---|---|
| PS8.1 | Core | 45 min |
| PS8.2 | Core | 50 min |
| PS8.3 | Optional | 30 min (uncounted) |
| PS8.4 | Core | 35 min |
| PS8.5 | Core | 50 min |
| PS8.6 | Core | 30 min |

Core total (re-added from rows): 45 + 50 + 35 + 50 + 30 = **210 min = 3.5 hr** — matches WO-M8 §3's stated core total exactly, within the 3–4 hr §5 budget. Optional (uncounted): PS8.3 = 30 min.


---

## Module 9 — Density Estimation

### PS9.1 — Histogram and Gaussian-kernel KDE from scratch: the bias-variance tradeoff
**Type:** I/V | **Tier:** 2+3 | **Core/Optional:** Core | **Time:** 55 min | **Goals:** 1, 2
**Prerequisites:** None.

**Statement:**
Let $f_0$ be the two-component normal mixture
$$
f_0(x) = 0.55 \cdot N(x; -2.0,\, 0.6^2) \;+\; 0.45 \cdot N(x; 2.0,\, 0.9^2).
$$
This is your **known density** for this problem: fully specified, so any density estimate you compute can be checked directly against it. Draw a sample of $n=500$ from $f_0$ (draw a component indicator per observation with the stated mixture weights, then draw from the indicated component's normal), using a seed you set and report.

*Part A (histogram — Goal 1 framing).* Implement a histogram density estimator from scratch: choose bin edges over a stated range with a given bin width $h$, count the sample points falling in each bin, and normalize so the result integrates to 1 (height $=$ count $/(n \cdot h)$). Compute it at three bin widths: $h \in \{0.15,\ 0.5,\ 2.0\}$ — deliberately too fine, plausibly reasonable, and too coarse. This is the estimator that motivates the rest of the module: notice, before moving to Part B, what goes wrong at each extreme (Goal 1 — articulating why a fixed-bin, hard-edged estimator is an unsatisfying solution to the density estimation problem).

*Part B (Gaussian-kernel KDE — Goal 2, the core of this problem).* Implement a Gaussian-kernel KDE from scratch:
$$
\hat f_h(x) = \frac{1}{nh}\sum_{i=1}^n K\!\left(\frac{x - x_i}{h}\right), \qquad K(u) = \frac{1}{\sqrt{2\pi}}e^{-u^2/2}.
$$
Sweep the bandwidth over the stated grid $h \in \{0.05, 0.08, 0.12, 0.18, 0.25, 0.35, 0.5, 0.7, 1.0, 1.4, 2.0\}$. For each $h$, compute the **integrated squared error** against the known density,
$$
\mathrm{ISE}(h) = \int \left(\hat f_h(x) - f_0(x)\right)^2 dx,
$$
by numerical integration (e.g., a fine grid and the trapezoid rule over a range wide enough to capture both mixture components, such as $[-8, 8]$). Identify the sweep-minimizing bandwidth $h^\*$.

**Deliverable:**
1. A plot or table of the three histogram estimates (Part A) against $f_0$, with 2–3 sentences on what each bin width does wrong or right.
2. A plot of $\mathrm{ISE}(h)$ vs. $h$ across the swept grid (Part B), with $h^\*$ marked.
3. Your reported seed, sample, $h^\*$, and $\mathrm{ISE}(h^\*)$.
4. 3–5 sentences identifying the bias-variance pattern in the $\mathrm{ISE}(h)$ curve: what dominates the error at the small-$h$ end, what dominates at the large-$h$ end, and why the curve has an interior minimum rather than being monotone.

**Verification:** [Tier 2 + Tier 3]
- **Tier 2:** $f_0$ is a fully specified generative fact (a stated two-component normal mixture) — no external citation needed; it is the ground truth your ISE computation checks against directly.
- **Tier 3** (validation log entry PS9.1): your $\mathrm{ISE}(h)$ curve should be **U-shaped** across the stated grid (a single interior minimum, not monotone in either direction). Your sweep-minimizing $h^\*$ should fall in $[0.10, 0.35]$ for this density, $n=500$, and this grid. $\mathrm{ISE}$ at the smallest grid bandwidth ($h=0.05$) should be at least $1.5\times$ your $\mathrm{ISE}(h^\*)$; $\mathrm{ISE}$ at the largest grid bandwidth ($h=2.0$) should be at least $10\times$ your $\mathrm{ISE}(h^\*)$. Among your three histogram bin widths, the moderate one ($0.5$) should have the lowest ISE of the three.

**Discussion note:** (folded) At $h=0.05$, the KDE is dominated by variance: it fits the noise in your particular 500-point sample, producing a wiggly, spiky curve that looks nothing like the smooth two-bump mixture it's estimating — a different seed would give a visibly different wiggle pattern. At $h=2.0$, the KDE is dominated by bias: it smooths so aggressively that the two components blur into something closer to a single lump, systematically misrepresenting $f_0$'s shape regardless of sample size. Between these extremes, $\mathrm{ISE}(h)$ traces out the classic bias-variance U: squared bias grows with $h$, variance shrinks with $h$, and their sum is minimized somewhere in the interior — that minimum is what a bandwidth *selector* (next problem) tries to locate without knowing $f_0$, which of course you have the luxury of knowing here. The histogram in Part A is doing the same tradeoff along a coarser knob (bin width instead of a continuous bandwidth, plus hard edges instead of a smooth kernel) — worth noticing that the same U-shape logic governs both estimators, even though the module's implementation focus moves to the smoother KDE from here on.

---

### PS9.2 — Bandwidth selector (Silverman's rule of thumb)
**Type:** I/V | **Tier:** 2+3 | **Core/Optional:** Core | **Time:** 35 min | **Goals:** 3
**Prerequisites:** Reuses your PS9.1 synthetic sample (same seed, same known mixture density) and your PS9.1 sweep results.

**Statement:**
Implement Silverman's (1986) rule-of-thumb bandwidth selector, confirmed in-session against Ch 3 §3.4 of the assigned text (owner's 1998 reprint):
$$
h_{\text{Silverman}} = 0.9\, A\, n^{-1/5}, \qquad A = \min\!\left(\hat\sigma,\ \frac{\mathrm{IQR}}{1.34}\right).
$$
This is Silverman's own recommended rule (his Eq 3.31, built on the robust spread estimate $A$ of his Eq 3.30) — not the simpler, cruder $h = 1.06\,\hat\sigma\,n^{-1/5}$ variant (his Eq 3.28), which Silverman's own discussion shows oversmooths *even further* on multimodal data than the robust version already does.

Using your PS9.1 sample ($n=500$): compute $\hat\sigma$ (sample standard deviation) and the interquartile range (IQR), then compute $h_{\text{Silverman}}$ from the formula above. Compare it against three reference points from your PS9.1 work: (a) your sweep-optimal bandwidth $h^\*$, (b) the smallest grid bandwidth ($h=0.05$, the undersmoothed extreme), (c) the largest grid bandwidth ($h=2.0$, the oversmoothed extreme). Using your known density $f_0$, compute $\mathrm{ISE}(h_{\text{Silverman}})$ the same way you computed $\mathrm{ISE}(h)$ in PS9.1.

*Optional stretch (not counted in this problem's 35-minute budget; not verified):* implement a simple least-squares cross-validation selector (minimize an estimate of integrated square error computed from the data alone) and compare its selected bandwidth to $h_{\text{Silverman}}$ and $h^\*$.

**Deliverable:** $\hat\sigma$, IQR, $A$, and $h_{\text{Silverman}}$; $\mathrm{ISE}(h_{\text{Silverman}})$ and its ratio to $\mathrm{ISE}(h^\*)$; where $h_{\text{Silverman}}$ falls relative to your PS9.1 sweep grid (its nearest grid neighbors, and how it compares to both extremes); 3–5 sentences interpreting the consequence of using $h_{\text{Silverman}}$ instead of $h^\*$ on this dataset — is it under- or over-smoothed relative to sweep-optimal, and why does that happen *here specifically*?

**Verification:** [Tier 2 + Tier 3, validation log entry PS9.2]
- **Tier 2:** the selector formula itself (Eq 3.31, with $A$ per Eq 3.30) — confirmed in-session against Silverman (1986) Ch 3 §3.4, owner's 1998 reprint, pp. 43–48.
- **Tier 3:** your $h_{\text{Silverman}}$ should fall in $[0.45, 0.65]$ for this density and $n=500$. Your $\mathrm{ISE}(h_{\text{Silverman}})$ should exceed your $\mathrm{ISE}(h^\*)$ by a ratio of **at least 2.5** — i.e., the selector should land clearly on the oversmoothed side of your sweep, well short of either grid extreme.

**Discussion note:** (folded) $A$ is a single global spread number computed from your whole sample — it has no way to "see" that the data actually came from two well-separated components, so it necessarily returns a bandwidth calibrated as if smoothing toward *some* single-bump reference distribution with roughly the same overall spread. Silverman's own discussion of exactly this situation (Fig 3.3; an equal mixture of unit-variance normals, means separated by a stated amount) shows the rule-of-thumb bandwidth increasingly exceeding the true asymptotically-optimal one as that separation grows past roughly two standard deviations, worsening steadily beyond that. Your PS9.1 mixture isn't literally that idealized case (unequal weights, unequal component variances), but the separation here in standard-deviation units is well into the range where Silverman's own analysis shows this degradation — and your own numbers confirm it directly: $h_{\text{Silverman}}$ lands 2–3$\times$ your sweep-optimal $h^\*$, and its ISE is several times worse, without ever approaching the *catastrophic* oversmoothing of the grid's own $h=2.0$ extreme. This is the practical lesson Goal 3 is after: a "principled," textbook-recommended selector is not the same thing as *the* optimal bandwidth for your particular data — it is a generically-reasonable default, deliberately biased toward safety (undersmoothing is harder to fix by eye than oversmoothing), which will systematically oversmooth exactly the kind of multimodal structure this module has been asking you to detect and characterize in every other problem in this set.

---
### PS9.3 — Rao-Blackwellized density estimate vs. plain KDE (pump-failure Gibbs output)
**Type:** C | **Tier:** 3 | **Core/Optional:** Core | **Time:** 45 min | **Goals:** 4
**Prerequisites:** Requires your saved PS7.4 chain.

**Statement:**
Recall PS7.4's ten-pump hierarchical Gibbs sampler: $\theta_i \mid y_i, \beta \sim \text{Gamma}(\alpha + y_i,\ \beta + t_i)$ for each pump $i$, with $\alpha=1.8$ fixed. The full conditional for each $\theta_i$ is available to you in closed form at every retained iteration — this is exactly the situation Rao-Blackwellization exploits: instead of using your $\theta_i$ draws directly to estimate their marginal density, you can average the *known conditional density itself* over your retained $\beta$ draws.

> **Saved-chain specification.** Save the post-run output as a plain numeric matrix (or data frame) with one row per iteration and one column per parameter, in iteration order, with NO warm-up discarded and NO thinning applied, together with: the seed, the number of iterations, the initial state, and (for MH-type samplers) the proposal scale. Store column names matching the model's parameter names. This exact object is reused in Module 8 (diagnostics) and Module 9 (Rao-Blackwellized density estimation).

Load your saved PS7.4 reference chain (all 20,000 iterations, 11 columns: $\theta_1,\dots,\theta_{10},\beta$). Discard the first 2,000 iterations as warm-up — the same convention PS7.4 used for its own summaries — leaving 18,000 retained iterations. Work with **pump 3** ($t_3 = 15$; use your own drawn $y_3$).

*Part A (Rao-Blackwellized estimate).* Compute
$$
\hat f_{\text{RB}}(\theta) = \frac{1}{N}\sum_{s=1}^{N} \text{Gamma\_pdf}\!\left(\theta;\ \alpha + y_3,\ \beta^{(s)} + t_3\right)
$$
over your 18,000 retained $\beta^{(s)}$ draws ($N=18{,}000$), evaluated on a grid of $\theta$ values spanning your $\theta_3$ draws' range. This averages *densities*, not draws — check that your curve integrates to $\approx 1$ before proceeding (a curve that doesn't is the known failure mode of accidentally smoothing the conditional *means* instead of averaging the conditional *densities*).

*Part B (plain KDE).* Compute a Gaussian-kernel KDE of your retained $\theta_3$ draws directly (reusing your PS9.1 KDE code), using bandwidth $h = 0.15 \times$ the empirical standard deviation of your retained $\theta_3$ draws — a simple, fixed choice; this problem is about variance comparison, not bandwidth optimality.

*Part C (variance comparison).* Using **bootstrap-over-draws**: resample your 18,000 retained iterations with replacement (same resampled row indices applied to both the $\beta$ column and the $\theta_3$ column, since each iteration's $\beta^{(s)}$ and $\theta_3^{(s)}$ are paired), recompute both $\hat f_{\text{RB}}$ and the plain KDE on each of $B \geq 200$ bootstrap replicates, and compute the pointwise variance (across replicates) of each estimator at every grid point. Report the mean pointwise variance for each estimator and their ratio.

*Part D (explanation).* In 3–5 sentences, explain why this Gibbs sampler makes Rao-Blackwellization cheap: what would you need in order to Rao-Blackwellize a generic MCMC marginal, and why is that already sitting in your saved chain here?

**Deliverable:** Your $\hat f_{\text{RB}}$ and plain-KDE curves plotted together; your RB curve's numerical integral (confirming $\approx 1$); the mean pointwise variance of each estimator and their ratio; 3–5 sentences for Part D.

**Verification:** [Tier 3, validation log entry PS9.3]
Your RB curve must integrate to between 0.97 and 1.03 over the range you compute it on. Your variance ratio (plain-KDE variance $/$ RB variance, mean-pointwise) should be **at least 20** — RB should show a dramatic, not marginal, variance reduction; a ratio near or below 1 signals an implementation bug, most likely in the RB averaging step (Part A) rather than the bootstrap (Part C). The gamma full-conditional form itself is a tier-2 conjugacy fact, already derived in your PS7.4 work — no new derivation is required here.

**Discussion note:** (folded) The Rao-Blackwell theorem guarantees $\hat f_{\text{RB}}$ can't have *higher* variance than the plain empirical estimator, but it doesn't by itself tell you the advantage will be this large — a two-to-three-order-of-magnitude reduction is typical in exactly this setting (a scalar marginal with a smooth, closed-form conditional and a well-mixed chain), because the plain KDE is throwing away everything except the raw $\theta_3$ draws, while the RB estimate uses every retained $\beta$ draw's full conditional shape. This pattern — conditioning on structure a Gibbs sampler already computed, rather than discarding it after the draw is taken — is precisely the *parametric* Rao-Blackwellization R&C describe specifically for Gibbs samplers (their Ch 7 treatment, Example 7.15 / Eq 7.11): their general form for a Gibbs chain $(x^{(t)},y^{(t)})$ is $\hat f_X(x) = \frac{1}{T}\sum_t f(x \mid y^{(t)})$, of which this problem's $\hat f_{\text{RB}}$ is a direct instance, and their own worked examples (a bivariate-normal Gibbs sampler; a missing-data Poisson model) demonstrate the same kind of dramatic variance reduction you just measured. G&H §6.4.4 is useful background for the *general* Rao-Blackwell principle (the conditional-variance inequality guaranteeing RB can't do worse than the plain estimator), but their own worked example there is a static rejection-sampling setting, not an MCMC one — R&C is the more directly on-point source for what this problem does. The specific numbers here come from your own chain either way, not from either text. *(Both loci confirmed in-session against owner-supplied pages, 07/15/2026.)*

---
### PS9.4 — Nearest-neighbor density estimation: tail behavior vs. KDE
**Type:** I/V | **Tier:** 2+3 | **Core/Optional:** Core | **Time:** 40 min | **Goals:** 5
**Prerequisites:** Reuses your PS9.1 synthetic sample (same seed, same known mixture density) and your PS9.1 sweep-optimal KDE.

**Statement:**
Implement the 1-dimensional $k$-nearest-neighbor density estimator from scratch:
$$
\hat f_{\text{kNN}}(x) = \frac{k}{2\,n\,R_k(x)},
$$
where $R_k(x)$ is the distance from $x$ to its $k$-th nearest neighbor among your $n=500$ sample points, and $2R_k(x)$ is the width of the smallest interval centered at $x$ that contains exactly $k$ sample points. Use $k=25$.

Evaluate $\hat f_{\text{kNN}}$ against your known density $f_0$ (the same normal mixture from PS9.1) using the same ISE computation as PS9.1, and compare against your PS9.1 sweep-optimal KDE ($h^\*$).

Then examine **tail behavior**, where kNN and KDE are known to diverge sharply. Evaluate both estimators on a fine grid over $[5, 30]$ — a region essentially outside $f_0$'s effective support (verify this: compute $f_0$'s own integral over $[5,30]$ and confirm it is negligible). Compute each estimator's own integral (its "tail mass") over this region.

**Note on scope (per module design):** the $k$NN estimator does not integrate to 1 in general — do not attempt an integrate-to-1 check on it (unlike PS9.3's RB estimator). This problem scopes the comparison to pointwise/tail-region behavior specifically because that comparison is well-defined even though the global integral is not.

**Deliverable:** Your kNN and KDE curves plotted against $f_0$ over the main data range; your kNN ISE and its ratio to your PS9.1 KDE ISE; a table of both estimators' values at $x \in \{5,6,7,8,10\}$ alongside $f_0(x)$; each estimator's tail-mass integral over $[5,30]$; 3–5 sentences explaining *why* the two estimators behave so differently in the tail (what does $R_k(x)$ do as $x$ moves away from the data, compared to what the Gaussian kernel does at the same distance?).

**Verification:** [Tier 2 + Tier 3, validation log entry PS9.4]
- **Tier 2:** $f_0$ is the same fully-known generative fact used in PS9.1.
- **Tier 3:** your kNN ISE should exceed your PS9.1 KDE ISE (at $h^\*$) by a ratio of at least $1.5$. Your kNN tail-mass integral over $[5,30]$ should fall roughly in $[0.03, 0.12]$; your KDE tail-mass integral over the same region should be at least $10\times$ smaller than your kNN tail-mass.

**Discussion note:** (folded) The contrast is structural, not incidental to this particular sample: as $x$ moves away from the bulk of the data, $R_k(x)$ — the distance to the $k$-th nearest point — grows roughly linearly in $x$ (the $k$ nearest points are just your most extreme sample points, however far away $x$ is), so $\hat f_{\text{kNN}}(x) = k/(2nR_k(x))$ shrinks only like $1/x$: slow, polynomial decay. The Gaussian kernel, by contrast, contributes $\exp(-u^2/2)$ per point, so once $x$ is a few bandwidths from every sample point, the KDE is numerically indistinguishable from zero — decay is super-exponential. This is why kNN density estimates do not integrate to 1 (their tails are not integrable over an unbounded domain, a genuine mathematical property of the estimator, not a bug) while the Gaussian KDE always does. Practically: kNN's adaptivity is a double-edged sword — in sparse regions it widens $R_k(x)$ to keep including $k$ points, which is exactly the local adaptivity that makes it attractive in multivariate settings with regions of very different density, but the same mechanism is what produces the heavy, non-vanishing tail you just measured. Both assigned readings are confirmed in-session against owner-supplied pages (07/15/2026): Silverman (1986) Ch 5 §5.2 gives this exact estimator (his Eq 5.1, matching the formula above with the one-dimensional constant $c_1=2$) along with its formal bias-variance analysis (Eqs 5.4–5.5) and states the non-integrability property directly; Givens & Hoeting §10.4.3.1 give the same estimator in general dimension $p$ (their Eq 10.47) and are the more specific source for the double-edged-sword point above — they note that in a single dimension this kind of local adaptivity brings little advantage over an ordinary fixed-bandwidth kernel estimator, but that the same mechanism offers substantially more promise once you move to multivariate data, which is the module's motivation for introducing the method here despite its underwhelming 1-D performance.

---
### PS9.5 — Two defensible bandwidths, two different stories (Type D)
**Type:** D | **Tier:** 3 | **Core/Optional:** Core | **Time:** 40 min | **Goals:** 6
**Prerequisites:** None (new dataset; does not reuse PS9.1's sample).

**Statement:**
Draw a sample of $n=45$ using **seed $=7$ exactly** (this problem requires this specific seed — see the note at the end of this statement) from the mixture
$$
f_0(x) = 0.5 \cdot N(x; -1.3,\, 1.0^2) \;+\; 0.5 \cdot N(x; 1.3,\, 1.0^2).
$$
**Do not look at, compute, or reveal $f_0$ yet.** Treat your 45 numbers as an unlabeled dataset.

*Choice 1 ("data-driven").* Implement **leave-one-out likelihood cross-validation**: for each candidate bandwidth $h$ on a grid (e.g., $0.15$ to $2.00$ in steps of $0.05$), compute
$$
\mathrm{CV}(h) = \sum_{i=1}^n \log \hat f_{h,-i}(x_i),
$$
where $\hat f_{h,-i}$ is the KDE built from all points except $x_i$. Choose $h_{\mathrm{CV}} = \arg\max_h \mathrm{CV}(h)$. Plot your KDE at $h_{\mathrm{CV}}$ and count its local maxima.

*Choice 2 ("conservative/presentation-safe").* Sweep the same grid and find the smallest $h$ at which your KDE first shows exactly one local maximum; call it $h_{\text{collapse}}$. Set $h_{\text{large}} = 1.3 \times h_{\text{collapse}}$ — a deliberately extra-smooth choice, motivated by a real and common practical stance: *"with only 45 points, I'm not confident a bumpy KDE reflects real structure rather than noise, so I'll smooth more than the data alone suggests."* Plot your KDE at $h_{\text{large}}$ and count its local maxima.

*Write two short interpretations* (2–3 sentences each), one under each bandwidth choice, as if you had to report your conclusion about this dataset's shape to someone who would see only your chosen plot.

*Then, and only then*, reveal $f_0$ (given above) and compare: how many modes does $f_0$ actually have, and where? Which of your two "defensible" bandwidth choices got the mode count right, and which got it wrong? In 3–5 sentences, articulate what each bandwidth choice implicitly assumed about the data that turned out to be (in)correct.

**Note on the seed requirement:** unlike other problems in this set, this problem requires the specific seed given above rather than a seed of your choosing. The phenomenon this problem is built to exhibit — two defensible bandwidths disagreeing on mode count — is real for this population but does not occur for every draw from it; seed $=7$ is guaranteed to show it.

**Deliverable:** Your two KDE plots (Choice 1 and Choice 2) with mode counts marked; your two pre-reveal interpretations; the revealed $f_0$ and its true mode count/locations; your post-reveal comparison (3–5 sentences).

**Verification:** [Tier 3, validation log entry PS9.5]
Using seed $=7$ exactly: your LOO-CV-selected bandwidth should yield a KDE with **exactly 2** local maxima, located within about $\pm 0.3$ of $x=-1.03$ and $x=1.49$. Your large/conservative bandwidth ($1.3\times$ the smallest grid $h$ giving 1 mode) should yield a KDE with **exactly 1** local maximum, located within about $\pm 0.3$ of $x=-0.30$. A different mode count at this exact seed indicates an implementation bug (a structural fact of this fixed dataset), not sampling variation.

**Discussion note:** (folded) The generative truth has two modes at $\pm 1.186$ (from the mixture's symmetric $\pm 1.3$ component means, each with $\mathrm{sd}=1.0$). $h_{\mathrm{CV}}$'s two peaks (near $-1.03$ and $1.49$) land close to the true mode locations — in this instance, the data-driven choice happens to recover the right qualitative picture. $h_{\text{large}}$'s single peak (near $-0.30$) sits almost exactly *between* the two true modes: it isn't a bad location for a single "compromise" summary, but it actively misrepresents the population as unimodal-and-centered when it is really two symmetric subpopulations — a viewer shown only this plot would draw the wrong conclusion about the data's structure. Neither choice was unreasonable to make *before* the reveal: LOO-CV is a standard, principled selector, and "smooth more when $n$ is small and you're unsure" is genuinely sound practical advice in general — it just happens to be wrong here. That is the point of this problem: a defensible process does not guarantee a correct outcome, and mode count in particular is exactly the kind of feature a bandwidth choice can silently erase or fabricate. The base-rate check (Notes, validation log) found this exact divergence in only about 42% of draws from this population — worth a sentence in your own write-up: bimodality that is only sometimes visible, depending on the specific sample, is itself a realistic and common situation, not a contrived one.

---

## Alignment matrix — Module 9

| Goal | Text | Problem(s) / justification |
|---|---|---|
| 9.1 | Articulate the density estimation problem — what it means to estimate a distribution nonparametrically, and why point estimates and parametric models are sometimes insufficient | **PS9.1** (framing, nominal attachment — per `PSDEP-M9SlateResolution.md` M9-P3: "Articulate" is not an implementation verb, R2 requires no dedicated problem, and §6 pins Goals 1–2 jointly to the KDE item; recorded so it is not read as an omission). Part A's histogram-first framing and its discussion note carry this goal. |
| 9.2 | Implement kernel density estimation, explain the role of the kernel and bandwidth, and characterize the bias-variance tradeoff that bandwidth selection governs | **PS9.1** (primary vehicle: from-scratch Gaussian-kernel KDE, bandwidth sweep, ISE-vs-h bias-variance pattern) |
| 9.3 | Apply principled bandwidth selection methods and explain the consequences of under- and over-smoothing for the resulting estimate | **PS9.2** (primary vehicle: Silverman's (1986) rule-of-thumb selector, Ch 3 §3.4 Eq 3.31, implemented from the confirmed formula and compared against PS9.1's sweep-optimal $h^\*$ and both grid extremes; discussion note interprets the oversmoothing consequence specific to this bimodal data). Source-access STOP (historical Flag A) resolved 07/15/2026 when the owner supplied the required pages in-session — see `ExecutionSummary_M9.md` Reconciliation Addendum for the closure record. **R2 now satisfied for this goal.** |
| 9.4 | Explain the Rao-Blackwell estimator as a variance-reduction strategy for density estimation, and identify why it is particularly well-suited to MCMC settings where conditional distributions are already available | **PS9.3** (RB density estimate on the imported PS7.4 chain, variance-compared against plain KDE; Part D's explanation targets the "why MCMC settings" clause directly) |
| 9.5 | Implement nearest-neighbor density estimation and contrast its bias-variance characteristics with those of kernel methods | **PS9.4** (from-scratch kNN estimator, ISE contrast with PS9.1's KDE, tail-behavior focus) |
| 9.6 | Interpret density estimates critically — recognizing what each method implicitly assumes and how those assumptions affect the estimate — rather than treating output as an objective description of the data | **PS9.5** (Type D: two defensible bandwidths, qualitatively different mode-count pictures, generative truth reveals one choice wrong) |

All six goals now have an exercising problem; no NOT-EXERCISED rows remain.

## Module 9 hours

| Core problems drafted | Core hours (re-summed) | WO slate-resolved figure | Budget (§5) | Status |
|---|---|---|---|---|
| 5 of 5 (PS9.1, PS9.2, PS9.3, PS9.4, PS9.5) | 55+35+45+40+40 = 215 min = **3.58 hr** | 215 min = 3.58 hr | 3–4 hr | Matches the WO's slate-resolved figure exactly; within budget. Full slate delivered — no open gap. |


---

