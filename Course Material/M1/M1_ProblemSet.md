# Computational Statistics — Problem Sets

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
- *Tier 3:* under the stated seed and generator, a correct implementation should obtain a chi-square statistic of **8.09 (± 0.05)** on $df=9$ — comfortably below the $\alpha=0.05$ critical value of **16.92** — and a serial-correlation $z$-statistic of **−0.50 (± 0.02)**, comfortably inside $(-1.96, 1.96)$. Both indicate failure to reject uniformity/independence, as expected for this generator. Your own sequence should also contain zero repeated values among the 10,000 draws, and seeding with $X_0=0$ should produce a sequence that is identically zero from the first draw onward.
**Discussion note:** *(folded)* A well-constructed LCG with these parameters should pass both tests comfortably — the point of the exercise is less "does it pass" and more "what would failing look like, and why." Common failure modes to watch for: an off-by-one in the recurrence (updating $U_n$ before or after incrementing $n$ inconsistently), using floating-point division prematurely (accumulating rounding error across the multiplicative recurrence — keep $X_n$ as an integer throughout and only divide by $m$ at the end), and forgetting that $c=0$ makes $X_0=0$ an absorbing fixed point. On the serial-correlation test specifically: because it is a size-0.05 test, roughly 1 run in 20 will show $|z|>1.96$ purely by chance even for a good generator — a single rejection under a *different* seed than the one stated here is not by itself evidence of a bad generator, only evidence that you ran a hypothesis test (this is worth sitting with, since it previews the same logic used to interpret R-hat and other diagnostics later in the program). The period argument here is deliberately partial: "no repeats in 10,000 draws" rules out a short period but does not establish the generator's true (much longer) period, which is a number-theoretic fact about $a$ and $m$ this problem does not ask you to derive.

---

### PS1.2 — Inverse transform: closed-form and numerical
**Type:** I | **Tier:** 1/2 + 3 | **Core/Optional:** Core | **Time:** 45 min | **Goals:** 3
**Prerequisites:** None (library uniform RNG only — the from-scratch requirement here is the transform, not the generator; generator-primitives are PS1.1's job)
**Statement:**

**(a) Closed-form CDF case — the Pareto distribution.** The Pareto distribution with scale $x_m$ and shape $\alpha$ has CDF $F(x) = 1 - (x_m/x)^\alpha$ for $x \geq x_m$. Derive the inverse-transform sampler: show that if $U \sim \text{Unif}(0,1)$, then $X = x_m U^{-1/\alpha}$ is Pareto-distributed with parameters $(x_m, \alpha)$ (using $U$ in place of $1-U$ is valid since both are $\text{Unif}(0,1)$). Implement this power-transform sampler using $x_m = 1$, $\alpha = 6$, drawing $U$ from your language's library uniform generator (seeded, per R5) with $n = 5{,}000$ draws. Overlay a histogram of your draws against the true Pareto density.

**(b) Numerical-inversion case — the standard normal.** The standard normal CDF $\Phi$ has no closed-form inverse. Implement inverse-transform sampling for $N(0,1)$ by numerically solving $\Phi(X) = U$ for $X$ given $U$, using a root-finding method you implement yourself (bisection is sufficient) on a bounded search interval (e.g., $[-10, 10]$, since $\Phi(-10) \approx 0$ and $\Phi(10) \approx 1$ to far more precision than you need). You may call your language's standard normal CDF function to *evaluate* $\Phi$ at each iterate of your search — the algorithm under test here is the numerical-inversion/root-finding loop, not a from-scratch reimplementation of $\Phi$ itself. Seed your uniform generator with $2024$ and draw $n = 5{,}000$ values of $U$; invert each to obtain $X_1, \dots, X_{5000}$.

**Deliverable:** (a) the derivation (2–3 lines), the implementation, the density overlay plot, and the sample mean compared to the Pareto's known mean; (b) the bisection (or equivalent) implementation, the sample mean and variance of your 5,000 draws, and their comparison to the standard normal's known moments (0 and 1).

**Verification:** [Tier 1/2 for (a); Tier 3 for (b)]
- *(a), tier 1/2:* the power-transform identity is a standard, directly-derivable result (probability integral transform applied to the Pareto CDF — see also R&C, *Introducing Monte Carlo Methods with R*, Ex. 2.13, a solved exercise on this same construction). The numeric check rests on the Pareto distribution's own known moments — a citable textbook fact, not something to look up in a solutions manual: for $x_m=1, \alpha=6$, $E[X] = \frac{\alpha x_m}{\alpha - 1} = 1.2$. At $n=5{,}000$, your sample mean should fall within **1.2 ± 0.0104** (a 3-standard-error band, using the Pareto's known variance $\text{Var}(X) = \frac{x_m^2 \alpha}{(\alpha-1)^2(\alpha-2)} = 0.06$).
- *(b), tier 3:* under the stated seed, a correct implementation should obtain a sample mean within **0 ± 0.0424** and a sample variance within **1 ± 0.0600** (both 3-standard-error bands around the standard normal's known moments — not an exact-match target, since library uniform streams differ across languages even under the same stated seed).
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

**Verification:** [Tier 1 for the general accept-reject theorem; Tier 2 for the closed-form bounds; Tier 3 for the empirical rates]
- *Tier 1:* the fact that acceptance-rejection has acceptance probability $1/M$ is standard, solved theory (R&C Ex. 2.5 derives this same result; Ex. 2.7 similarly explores what proposal-parameter choices keep this ratio well-behaved, the same theme this problem's ranking discussion takes up).
- *Tier 2:* $M_1 = \sqrt{2/\pi}\, e^{1/2} \approx 1.3155$ and $M_2 = 2\sqrt{\pi/2}\, e^{-1/2} \approx 1.5203$ are closed-form derivations from the target/proposal density ratio — check your own derivation against these values before running the empirical step.
- *Tier 3:* at $20{,}000$ proposal attempts, seeded at $31415$, your empirical acceptance rate should fall within **0.7602 ± 0.0090** for the Laplace proposal and **0.6577 ± 0.0101** for the Cauchy proposal (3-standard-error bands, calibrated across multiple seeds). The Laplace proposal should show the higher acceptance rate of the two.
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

**Verification:** [Tier 3]
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

**Verification:** [Tier 2 for the generator's stipulated definition; Tier 3 for both empirical findings]
- *Tier 2:* the recurrence itself ($a=65{,}539$, $c=0$, $m=2^{31}$) is this problem's own stipulated generator (design informed by R&C Ex. 2.10, the harvest's flagged standout example for this goal). The specific numeric parameters are not independently traceable to a source available in this project — R&C's book text is not a session input, and Ex. 2.10 is even-numbered/unsolved, so the arXiv companion carries no confirmable solution — and are presented as a stipulation, consistent with the historical-attribution flag below.
Tier 3, Part 1:* under $X_0=1$, $n=5{,}000$, the identity should hold with **zero exceptions**, and you should find **15** distinct plane indices (specifically $k \in \{-5,-4,\dots,9\}$).
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

**Verification:** [Tier 2 for both theoretical rates' derivation/computation; Tier 3 for the empirical confirmation]
- *Tier 2:* the naive rate is exactly $P(Z\geq 4)$, computable via your language's normal CDF (a citable, library-computable fact, not a number to recall). The improved bound $M = \frac{1}{a}e^{-a^2/2}$ is this problem's own closed-form derivation (shown above); the general accept-reject theorem underlying the acceptance-rate calculation is the same standard result used in PS1.3 (R&C Ex. 2.5).
- *Tier 3:* under a stated seed, at $20{,}000{,}000$ naive attempts your empirical rate should fall within **3.167×10⁻⁵ ± 3.78×10⁻⁶**; at $20{,}000$ improved-method attempts your empirical rate should fall within **0.9466 ± 0.0048**. The ratio of improved to naive acceptance rate should be on the order of $10^4$ (We observed 23,000×–32,000× across five independent trials).
**Discussion note:** *(folded)* The naive method isn't wrong, exactly — it's just spending nearly all of its 20 million draws generating values the problem doesn't want, and only accidentally landing in the target region about 1 time in 30,000. The improved proposal is shaped to put almost all of its mass exactly where the target's mass is (in the tail beyond $a$), so it wastes far less effort — this is the general lesson of good proposal design (echoing PS1.3's ranking discussion): match the proposal's shape to the target's shape *where the target actually has mass*, which for a deep tail means matching the tail's local behavior, not the distribution's overall shape. If your naive empirical rate is off by an order of magnitude, check you used a large enough attempt count — this is a rare-event probability, and both very small and very large empirical deviations are possible with insufficient attempts.

---