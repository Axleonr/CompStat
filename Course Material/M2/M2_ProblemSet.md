# Computational Statistics — Problem Sets

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
- **Tier 2 (estimand):** $I = e - 1$ is an exact closed-form fact (fundamental theorem of calculus applied to $e^x$; equivalently, the exact mean of $e^U$ for $U\sim\text{Uniform}(0,1)$). No external citation is needed beyond this elementary derivation — verify your build against $2.718281828\ldots - 1 = 1.718281828\ldots$ to as many digits as your language's floating point gives you. (R&C Exercise 3.1's own worked target is *not* usable here — its published values are single-run Monte Carlo estimates with no closed form, not a reproducible tier-1 anchor — which is why this problem is built on the present closed-form integral instead.)
- **Tier 3 (rate-plot slope):** your fitted slope should fall in **[-0.80, -0.20]** (verified across 2000 seeds). This band is wider than a naive "should be $-0.5$" expectation because a *single* realization per grid point is genuinely noisy at the small-$n$ end of the grid. A slope near 0 (error not shrinking) or a slope steeper than about $-1$ both indicate a implementation problem, not sampling noise.

**Discussion note:** *(folded — instructor-facing, no solution code)*
A correct implementation should show noisy but clearly decreasing error as $n$ grows, with the log-log slope landing in the stated band the large majority of the time — we found about 97.75% of independent single-run realizations on this exact grid land inside [-0.80, -0.20], with the extreme 0.5th/99.5th percentiles near -0.85/-0.14. Common failure modes: (a) accidentally computing a cumulative/running average across grid points instead of fresh independent draws per $n$, which correlates the errors and can distort the fitted slope in either direction; (b) mis-specifying the exponent or the domain of $U$ (e.g., drawing from $(-1,1)$ instead of $(0,1)$), which breaks the closed-form check immediately at any $n$; (c) an off-by-one or vectorization bug that silently uses $n-1$ or double-counts a draw, usually visible as a small but consistent bias that does not shrink with $n$. This problem establishes the module's baseline rate — PS2.2 through PS2.5 all reduce the *constant* in front of $n^{-1/2}$ without changing the exponent itself, which is exactly what those problems' write-ups should note explicitly (preview of Goal 5).

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
- **Tier 2 (estimand and structural identities):** $I=e-1$ as in PS2.1 (closed form). The antithetic identity — for monotone $h$, the pairs $(h(U), h(1-U))$ are negatively correlated — is the textbook result of R&C Exercise 4.11. $E[U]=\tfrac12$ and $\mathrm{Var}(U)=\tfrac1{12}$ are plain distributional facts about Uniform(0,1), citable to any standard probability reference. The control variate here deliberately does *not* use the score-function construction (R&C Exercise 4.12); this problem uses the plain known-mean control ($X=U$) instead.
- **Tier 3 (achieved variance-reduction ratios):** at $n=2000$ with $R\geq500$, your measured ratio should exceed **15× for antithetic** and **25× for the control variate**.
	> **Important**: these figures are **lower bounds** set from our reference executions, not exact targets to hit precisely. Ratios well above these thresholds (roughly 30× and 60× respectively) are expected and correct, not a sign of a mistake.

**Discussion note:** *(folded — instructor-facing, no solution code)*
This example is a deliberately dramatic illustration: because $e^{U}\cdot e^{1-U}=e$ is a constant (not merely correlated, but functionally linked), the antithetic pairing here achieves an unusually large reduction; and because $e^u$ is nearly linear in $u$ over $[0,1]$, its correlation with $U$ is very high ($\rho \approx 0.99$), giving the control variate an even larger reduction. 

> Over 100–150 independent meta-runs at $R\in\{300,500,1000,2000\}$), we found the antithetic ratio's worst case around 24× and the control-variate ratio's worst case around 43× — both comfortably above the stated 15×/25× thresholds, which is why those are safe floors rather than tight targets.

Students should not conclude from this example alone that antithetic/control-variate reductions of 30–60× are typical — PS2.7 (optional) and PS2.5's comparative study make clear that the achieved reduction is highly target- and statistic-dependent. 

Common failure modes:
- In **(a)**, pairing $U_i$ with $1-U_i$ but then treating the two as independent (n draws instead of n/2) — this silently changes the workload comparison and inflates the apparent variance reduction
- In **(b)**, computing $\hat c$ from a *different, fresh* sample than the one used for the estimate — not wrong, but it changes the workload accounting relative to what's asked here, since a fresh pilot sample adds draws not shared with the plain-MC comparison.
- Forgetting that both ratios are expected to be very large for this particular $h$, and mistakenly "fixing" a correct large ratio.

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
- **Tier 1 (all values below are machine-checked against the original Aalto A4 test-input/output values):**
  - Six log-ratios ≈ $(-8.95,\ -23.47,\ -6.02,\ -8.13,\ -16.61,\ -14.57)$ — agree to within 0.01.
  - Six normalized weights ≈ $(0.045,\ 0.000,\ 0.852,\ 0.103,\ 0.000,\ 0.000)$ — agree to within 0.001.
  - Posterior-mean estimate ≈ $(0.503,\ 8.275)$ — agree to within 0.01.
  - **ESS ≈ 1.354 — the keystone check**; note this is out of a *nominal* 6, i.e. $S_{\text{eff}}/6 \approx 0.226$, a stark illustration of weight degeneracy from just six draws.
  - MCSE ≈ 0.30 ($\alpha$) and ≈ 4.48 ($\beta$) — agree to **2 significant figures only**. Do not expect exact-digit agreement: this specific value has drifted in its later decimal digits across different years of the source course's template even on this fixed test case, so it is cited as an approximate check, not an exact one.
  - **Provenance correction carried from the annex:** the "6-point test case" is six $(\alpha,\beta)$ parameter-draw pairs, not six bioassay observations — the bioassay dataset itself is the 4-row table above.
  - **Eq. 10.4 caveat:** if you consult BDA3's Eq. 10.4 for the ESS formula, note that the 1st/2nd printings contain an erroneous multiplier in the normalized-weight term; the corrected form is exactly the $S_{\text{eff}} = 1/\sum_i \tilde w_i^2$ given above. Using the as-printed 1st/2nd-printing form here would be incorrect.

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
- **Tier 3:** your results should show the following qualitative-and-quantitative signature (not exact-value matches — the point is the pattern, not a specific number):
  - **Proposal B (healthy):** ESS/N should land in **[75%, 85%]** for every one of your 10 seeds, with the range across those 10 seeds no more than **2 percentage points** — i.e., stable (79.8%–80.2% for us accross 60 independent seeds). Max-weight share should stay **below 0.001 (0.1%)** for every seed.
  - **Proposal A (degenerate):** the **mean** ESS/N across your 10 seeds should be **below 30%**, and — this is the more telling signature — the **range** (max − min) of ESS/N across those same 10 seeds should **exceed 15 percentage points** (We got 0.03%–44% across 60 independent seeds). The instability itself, not just a low average, is the diagnostic signal. Max-weight share should **exceed 0.002 (0.2%)** in at least one of the 10 seeds.

**Discussion note:** *(folded — instructor-facing, no solution code)*
The underlying reason Proposal A cannot be stabilized by increasing $N$ within reason: $f(x)/g_A(x)$ grows like $e^{x^2/2}/x^2$, so $E_{g_A}[w^2]$ is analytically infinite — this is a genuine infinite-variance importance weight, not a finite-but-large-variance case that more draws would tame. That is exactly why the *instability across seeds* (not merely a low ESS in any one run) is the signature to emphasize with students: a single run's ESS can look deceptively OK-ish (44.18% at the top-end for us) right next to a catastrophic one (0.031% low) — this variability is itself diagnostic of an ill-posed weight distribution, and students should be told explicitly not to average away or explain away a wildly-varying-across-seeds result as "bad luck." Contrast with Proposal B, whose same-tail-order construction keeps the weight ratio bounded, giving both a healthier ESS and — just as importantly — a *stable* one. 

Common failure modes: 
- Running only a single seed and concluding Proposal A is "not that bad" because that one seed happened to land in the more benign part of its range.
- Forgetting to normalize weights before computing ESS or max-share (unnormalized weights make the max-share figure meaningless).
- Conflating this with PS2.3's degeneracy illustration — that one arose from a small nominal sample size (6) with a well-specified but concentrated posterior; this one arises from an outright proposal/target tail mismatch, a different mechanism worth distinguishing explicitly in the write-up.

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
- **Tier 3 (achieved variances and their ordering):** at $n=5000$, $R=2000$, your variance-reduction ratios (plain variance ÷ technique variance) should satisfy:
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
 - **Tier 3:** your resampled-sample mean should agree with your IS-weighted estimate to within **0.15 for $\alpha$** and **0.6 for $\beta$**.
	> This check stacks noise from two independent layers of Monte Carlo (the importance draw and the resampling draw); because of that, these thresholds carry roughly 2.5× margin over the observed worst case in our 150-seed run.

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
- **Tier 2 (estimand):** $I=\mathrm{Var}(U)=1/12$, a plain distributional fact about Uniform(0,1).
- **Tier 3 (executed variance ratio):** your ratio (plain variance ÷ antithetic variance) should fall in **[0.35, 0.65]** — notably **below 1**, meaning antithetic pairing is *worse* than plain Monte Carlo here, not merely unhelpful. This is a tight, confidently-set band: unlike PS2.5's antithetic case (a small, noisy true effect), this one rests on an exact algebraic identity ($h(1-u)\equiv h(u)$), so the true population ratio is exactly $0.5$ and the calibration spread around it is small.

**Discussion note:** *(folded — instructor-facing, no solution code)*
The mechanism failure is exact, not approximate: because $h(1-u)\equiv h(u)$, the "pair average" $[h(U_i)+h(1-U_i)]/2$ collapses to $h(U_i)$ itself — you have paid for $n$ evaluations but only ever learn $n/2$ independent facts about $h$, exactly halving your effective sample size relative to a plain $n$-draw estimator. This is the cleanest possible illustration that antithetic variance reduction is *not* a free property of pairing $U$ with $1-U$ — it specifically requires the negative-correlation structure that monotonicity guarantees, and a symmetric $h$ is close to a worst case rather than a neutral one. Frame this for students as completing the module's Goal 3/5 picture: PS2.2(a) showed antithetic variates working dramatically; PS2.5 showed them barely working on a different, non-symmetric but non-monotone-friendly target; this problem shows them actively backfiring on a symmetric target. Common failure modes: (a) not noticing the exact algebraic identity and instead treating the observed ratio as "just noisy," missing the deterministic explanation; (b) accidentally implementing $h(1-u)$ with a sign error that breaks the exact-symmetry check (verify $h(1-u)=h(u)$ numerically before running the variance comparison).

---