# Computational Statistics — Problem Sets

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
- **Tier 1** (sourced to Hesterberg (2015), confirmed against the article text) — for context only, the published analysis reports: CLEC mean 16.50913, bootstrap SE 3.961816, 95% percentile CI (10.09, 25.41); ILEC mean 8.41161, bootstrap SE 0.357599. These are the article's own figures on the real data, not targets your synthetic-mirror run is expected to hit.
- **Tier 3** (synthetic-mirror run): as *approximate* targets for this synthetic mirror (a different realization matching the published summary statistics, not the original data, so expect proximity rather than exact match) — CLEC bootstrap SE should be roughly in **[3.5, 4.6]**; CLEC 95% percentile CI should have its lower bound roughly in **[8, 10]** and upper bound roughly in **[23, 26]**; ILEC bootstrap SE should be roughly in **[0.28, 0.45]**; your own generated ILEC sample mean should land roughly in **[7.3, 9.5]**. This synthetic mirror matches the published mean and SE closely but was not tuned to reproduce the published interval shape.
- **Tier 1**, narrowness relation: your CLEC bootstrap SE should be within about ±10% of $s/\sqrt n \cdot \sqrt{(n-1)/n}$.
- **Tier 1**, two-arm contrast: your CLEC bootstrap SE should be at least 8× your ILEC bootstrap SE (reflecting the sample-size asymmetry — this is the point of using two arms of very different size).

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
- **Tier 3:** Both ratio-checks hold to within ~2% across 20 independent replications; no single fixed numeric target for either raw SE is appropriate at this sample size.

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
- **Tier 1** (cite Hesterberg 2015 Sec. 4.4, as a **qualitative** anchor only — the article's own numeric thresholds are article-scale, not student-scale): your bootstrap-t coverage should be visibly closer to the nominal 0.95 than your percentile coverage at small $n$, and the gap between the two methods should shrink as $n$ grows.
- **Tier 1** (cite E&T 1993 Ch. 14 Sec. 14.3): the sanity check ($\hat a=\hat z_0=0 \Rightarrow$ BC$_a$ = percentile) must pass exactly (to numerical precision) — this confirms your formula implementation against the source, independent of any simulation noise.
- **PRIMARY Tier 3 check (robust — verified with zero exceptions across 26 independent replications):** at every $n$ in the grid, mean CI width should satisfy **percentile width < BC$_a$ width < bootstrap-t width**, strictly. This ordering is far more reliable in a single run than any coverage-based comparison (width is a low-variance, continuous quantity; coverage is a noisy binary-outcome proportion at this trial count).
- **Tier 3** (student-scale numeric bands): percentile coverage roughly in [0.78, 0.90] (n=8), [0.83, 0.93] (n=15), [0.87, 0.96] (n=30), [0.89, 0.97] (n=60); bootstrap-t coverage roughly in [0.89, 0.98] (n=8), [0.90, 0.98] (n=15), [0.90, 0.98] (n=30), [0.91, 0.98] (n=60); BC$_a$ coverage roughly in [0.79, 0.93] (n=8), [0.84, 0.94] (n=15), [0.87, 0.97] (n=30), [0.89, 0.98] (n=60). Gap check (bootstrap-t minus percentile) ≥0.05 at n=8, ≥0.02 at n=15, ≥0.01 at n=30.
- **SECONDARY Tier 3 check (a real but modest effect — average over the whole $n$-grid, not per-$n$):** averaged across your four $n$ values, (BC$_a$ coverage − percentile coverage) should be $\ge -0.01$, and (bootstrap-t coverage − BC$_a$ coverage) should be $\ge 0.01$. Don't be surprised if BC$_a$'s coverage *at a single $n$ in isolation* is occasionally a hair below percentile's — that is ordinary Monte Carlo noise on a small true effect (~0.5–1.5 coverage points), not a bug; the averaged check is the fair one.

**Discussion note:** (folded guidance; no solution code) The percentile interval under-covers noticeably at small $n$ because it inherits both the narrowness bias (PS3.1/H-3) and an incomplete skewness correction; bootstrap-t corrects for both by pivoting on a statistic closer to distribution-free (at the cost of a formula/nested SE per resample); BC$_a$ takes a different route — it keeps using percentiles of the *same* bootstrap distribution as the percentile method (so it inherits percentile's transformation-respecting property, E&T Sec. 14.3) but shifts *which* percentiles it reads off, using $\hat a$ and $\hat z_0$ to correct for the skewness and median-bias the plain percentile method ignores. This is why BC$_a$'s width lands between the other two: it is doing a real correction (unlike percentile), but a different, generally smaller one than bootstrap-t's full pivotal-statistic approach for this particular statistic (the mean) and population. A common implementation bug for BC$_a$ is computing the jackknife over *bootstrap* resamples instead of the *original* sample — the jackknife is deterministic and uses only your original $n$ data points, no resampling involved. Another common bug: forgetting the bootstrap-t endpoint reversal (subtracting the *upper* $t^*$ quantile to get the *lower* CI endpoint). Students should not expect their exact coverage numbers to match any published article figures — Hesterberg's own published thresholds are from large-scale, variance-reduced simulations; the point of this problem is the *qualitative and width-based* hierarchy, made visible in output the student generated themselves.

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
- **Tier 2** (standard distributional fact, citable): the Normal IQR ratio should be roughly **[3.5, 6.5]** (theoretical value: $\sqrt{500/20}=5$). The Cauchy IQR ratio should be roughly **[0.5, 1.8]** (theoretical value: 1 — no shrinkage).
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
- Rough absolute bands (Tier 3): naive width $\in [0.30, 0.45]$; MBB-5 width $\in [0.50, 0.85]$; MBB-20 width $\in [0.45, 1.10]$ (wider band — block-length-20 resamples carry more single-realization Monte Carlo variability at this series length).

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
- **Tier 1** (cite Hesterberg 2015 Sec. 3.6): the published guidance is $r\ge 15{,}000$ for 10%-accurate percentile/bootstrap-t endpoints — note where this threshold falls relative to your own $r$-grid, and whether your MC noise is already comfortably small by $r=20{,}000$.
- **Tier 3:** the ratio $\text{MC-SD}(200)/\text{MC-SD}(20{,}000)$ should be roughly in **[7, 14]** (theoretical value: $\sqrt{20{,}000/200}=10$). The four normalized values $\text{MC-SD}(r)\cdot\sqrt r$ should all lie within a factor of **1.5** of their own mean.

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
- **Tier 1** (cite Hesterberg 2015 Sec. 3.3 — cited for the *phenomenon*, not a numeric target: no single number is claimed by the source either).
- **Structural checks (exact, no tolerance needed — these are logical certainties for odd $n$, not statistical tendencies):** the number of distinct values in your bootstrap-median distribution must be **≤15**; every bootstrap median value must be **exactly equal** to one of your 15 original observations.
- **Tier 3:** the number of distinct values in your *true*-sampling-distribution simulation should be **≥1,980 out of 2,000** (near-certain for a continuous population — a much lower count signals an RNG or rounding bug, not a real effect).

**Discussion note:** (folded guidance; no solution code) This is a *structural* failure, not a sampling-noise phenomenon — unlike every other verification target in this module, the two structural checks here have no legitimate "close enough" band; either your bootstrap medians are a subset of your original data (they must be, by construction) or your implementation has a bug. This is a good contrast with PS3.4's Cauchy failure: there, the statistic (the mean) fails on a *particular population* (infinite variance); here, the statistic (the median) has an inherent discreteness problem tied to sample parity, independent of which population it's drawn from. Interestingly (Efron 1982, cited in Hesterberg 2015), the bootstrap *percentile interval* for the median is not nearly as bad as the discreteness of the full bootstrap distribution might suggest — a nuance worth a sentence if time allows, but not required.

---