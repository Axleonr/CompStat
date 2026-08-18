# Computational Statistics — Problem Sets

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

**Verification:** Tier 3 (executed and logged). For every one of the four resamples, against your own reference estimates: $|\text{resampled }\alpha\text{ mean} - \text{reference}| < 0.15$; $|\text{resampled }\alpha\text{ variance} - \text{reference}| < 0.20$; $|\text{resampled }\beta\text{ mean} - \text{reference}| < 0.65$; $|\text{resampled }\beta\text{ variance} - \text{reference}| < 6.5$.

**Discussion note:** (folded) All four resamples should land inside the stated tolerances — this is a well-conditioned SIR setup because $M$ (1,000 or 5,000) is kept well below the importance sample's effective size (roughly 14,000–14,600 out of $N=50{,}000$, about 28–29%: this bioassay likelihood is informative but doesn't push the posterior so far from the wide prior that weights collapse the way they did on PS2.3's own tiny 6-point *validation* case — that ESS≈1.354-out-of-6 was a deliberately small test input, not representative of a production-sized draw). If you experiment with $M$ approaching or exceeding the effective sample size, the *without-replacement* resamples in particular degrade sharply — you start being forced to include many low-weight draws just to fill the quota, and the resampled distribution drifts back toward the (wrong) proposal rather than the target. That failure mode is a preview of a lesson this module returns to for MCMC as well: an approximate-sampling scheme is only as good as its effective sample size, however that size is achieved. Note also what this problem does *not* have that a closed-form-target check would: your "ground truth" here (the large-$N$ IS-weighted reference) is itself a Monte Carlo estimate, not an independent fact — the same pattern your PS2.6 preview (if you did it) already used at a smaller scale. That's an acceptable cross-check (two estimates from related but distinct procedures agreeing), not a weaker one, precisely because SIR and the weighted estimate can fail independently (a resampling bug won't show up in the weights themselves, and vice versa). Note the division of labor: this problem's check guards only the *resampling* step, because both sides of the comparison share the same weights — a bug in the weights themselves would corrupt reference and resample identically and pass unnoticed here. What guards the weights is your PS2.3 machine-checked test case (the fixed six-point validation against known outputs); this problem builds on functions already validated there, which is why it can focus its own check on the one new thing it introduces. Goal 7's "common family" framing: SIR, MH, and Gibbs are three different answers to the same question — how do you get draws from a target you can only evaluate (up to a constant), when direct sampling isn't available? SIR's answer is "weight-then-resample, once"; MH and Gibbs (below) build an iterative Markov chain instead, trading SIR's one-shot weight degeneracy risk for a different set of tuning/mixing risks you'll spend the rest of this module characterizing.

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

**Verification:** Part A is tier 2 (a standard, citable derivation — your result should match the boxed formula above; any correct MCMC/Monte-Carlo reference derives the same symmetric-proposal special case). Part B: (i) tier 1 for context only — R&C's own worked example (Example 6.4/6.10) at these same three $\delta$ values on a comparable normal-target random-walk study reports acceptance rates of approximately 0.98, 0.80, and 0.15 respectively (cited as approximate order-of-magnitude context, not a pass/fail target); (ii) tier 3 for the actual pass/fail check (executed and logged) — at $n_{\text{iter}}=50{,}000$: acceptance rate should fall in $[0.94,0.99]$ ($\delta=0.1$), $[0.65,0.75]$ ($\delta=1$), $[0.08,0.18]$ ($\delta=10$); lag-1 ACF in $[0.98,1.00]$, $[0.70,0.82]$, $[0.75,0.90]$ respectively; lag-20 ACF in $[0.82,0.95]$, $[-0.06,0.08]$, $[-0.03,0.10]$ respectively; and (known-truth sanity check, tier 2 — target mean 0/variance 1) sample mean in $[-0.35,0.35]$ and sample variance in $[0.65,1.30]$ at every $\delta$.

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

**Verification:** Part A/closed-form mean and variance are tier 2 (standard Beta-Binomial compound-distribution identity; your derivation should match the boxed formulas). Part B is tier 3 (executed and logged): at $n_{\text{iter}}=20{,}000$ (burn-in 1,000, $N=19{,}000$ retained), $|\text{Gibbs mean} - 8.0| < 0.4$ and $|\text{Gibbs variance} - 20.0| < 1.6$ (closed-form check); $|\text{Gibbs mean} - \text{direct-sampling mean}| < 0.45$ and $|\text{Gibbs variance} - \text{direct-sampling variance}| < 1.4$ (cross-method check); and $\max_{k=0,\dots,20} |\hat{P}(X{=}k) - P(X{=}k)| < 0.015$ for both your Gibbs and direct-sampling histograms against the closed-form pmf. Part C is tier 2 (a standard derivation; your algebra should reduce the ratio to exactly 1).

**Discussion note:** (folded) All three views of $X$'s distribution — Gibbs, direct sampling, and the closed form — should agree within Monte Carlo noise; if your Gibbs histogram matches direct sampling but *both* disagree with the closed form, suspect an error in your closed-form derivation (Part A) rather than your sampler. If Gibbs disagrees with both direct sampling and the closed form, suspect the sampler (a common bug: updating $Y$ using the *previous* iteration's $X$ instead of the just-drawn current $X$, breaking the alternating structure). Part C's punchline generalizes: Gibbs is not "MH without acceptance" as a separate algorithm — it is literally MH with a proposal so well-chosen (the exact conditional) that rejection never triggers. This is also why Gibbs needs no proposal-tuning step at all, unlike PS7.2's random-walk MH: there is no scale to choose, because the "proposal" is exact by construction. That convenience has a cost, explored next: it requires the full conditional to be tractable to sample from directly, which won't always hold (PS7.5).

**Instructor note (source provenance):** This problem's two-stage Beta-Binomial Gibbs construction adapts the *shape* of R&C Ch. 7, Ex. 7.2 (a conjugate two-stage Gibbs sampler with a closed-form marginal to check against) — an unsolved, even-numbered exercise, cited by concept only. R&C 7.2 anchors the construction, not a verification target: no R&C solution exists for it, so the model, hyperparameters, and all numeric targets here are original/derived. The tier-2 checks are Part A's standard Beta-Binomial identities; all runtime checks are tier-3.

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

**Verification:** Tier 2 for the full-conditional forms (standard Poisson-Gamma and Gamma-Gamma conjugacy — your derivations should match the boxed formulas above). Tier 3 for the executed checks: multi-start agreement — maximum pairwise difference in any $\theta_i$'s posterior mean across your three chains $< 0.02$, and in $\beta$'s posterior mean $< 0.15$; conjugate-conditional moment check — maximum (over the 10 pumps) $|\text{empirical mean} - \text{shape}/\text{rate}| < 0.01$ and $|\text{empirical variance} - \text{shape}/\text{rate}^2| < 0.01$.

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

**Verification:** Tier 3 (executed and logged). At $n=50$, $n_{\text{iter}}=20{,}000$ (burn-in 2,000), $\delta=0.5$: your posterior mean of $\mu$ should satisfy $|\text{mean} - 5.0| < 1.0$; your posterior mean of $\sigma$ should satisfy $|\text{mean} - 2.0| < 0.7$; your $\sigma$-step acceptance rate should fall in $[0.25, 0.55]$ (this last one is a sanity check that $\delta=0.5$ is reasonably tuned for this problem, not a recovery check — an acceptance rate far outside this band suggests a bug in the $\sigma$ target, not bad luck).

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

**Verification:** Tier 2 for the target's true mean/variance (elementary finite-mixture moment identity — no citation beyond the formula itself). Tier 3 for the failure signature and the contrast run (executed and logged): for the $\delta=0.5$ run, you should observe $|\text{sample mean} - 0| > 3$ and a right-mode ($\theta>0$) visit fraction $< 0.01$ — **this is the expected, verified failure**, not a sign of a bug in your sampler. For the $\delta=6$ contrast run, $|\text{sample mean} - 0| < 1.0$, $|\text{sample variance} - 26| < 3.0$, and right-mode visit fraction $\in [0.30, 0.70]$.

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

**Verification:** Part A is tier 2 (a standard, derivable conceptual fact about greedy vs. stochastic acceptance — any correct reasoning about hill-climbing vs. sampling reaches the same conclusion: the chain collapses onto the mode and never characterizes the distribution's spread). Part B's three bugs are tier 1 (their existence and count — exactly three — are confirmed against the Aalto BDA course's Assignment 5 bug-hunt notebook). Part C is tier 3 (executed and logged): at $\delta=1$, $n_{\text{iter}}=20{,}000$, your corrected sampler's acceptance rate should fall in $[0.64, 0.76]$, sample mean in $[-0.15, 0.15]$, sample variance in $[0.80, 1.20]$ — the same ballpark as your PS7.2 $\delta=1$ results, since this is structurally the same sampler once fixed.

**Discussion note:** (folded) The three bugs, if you're stuck: (1) `log_ratio` is a *log*-ratio, but it's never exponentiated before being compared to a draw from $\text{Uniform}(0,1)$ — comparing a log-quantity (which can be very negative) directly against a probability-scale draw is not the same computation as comparing the actual ratio; (2) the comparison direction is backwards — correct Metropolis-Hastings accepts when the uniform draw is *less than* the (true, exponentiated) ratio, favoring moves toward higher relative density, not the reverse; (3) the chain records `theta_propose` every iteration regardless of whether the move was accepted, so a rejected proposal is still written into the chain as if it had happened — the recorded sequence is then not a valid realization of the Markov chain at all. Bugs (1) and (2) compound in this reconstruction to produce a chain that "accepts" almost every large downhill move and diverges outward without bound — a dramatic, easy-to-recognize symptom, but the more instructive lesson is that (3) alone, in isolation, would have produced a chain that still looks numerically tame (values still near the target's support) while being silently wrong, which is a much harder bug to catch by eyeballing the output. This is why "does the trace plot look reasonable" is never sufficient verification on its own — you need to know *what* the code is supposed to be doing, not just whether its output looks plausible.

---