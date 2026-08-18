# Computational Statistics — Problem Sets

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
- **Tier 3:** your $\mathrm{ISE}(h)$ curve should be **U-shaped** across the stated grid (a single interior minimum, not monotone in either direction). Your sweep-minimizing $h^\*$ should fall in $[0.10, 0.35]$ for this density, $n=500$, and this grid. $\mathrm{ISE}$ at the smallest grid bandwidth ($h=0.05$) should be at least $1.5\times$ your $\mathrm{ISE}(h^\*)$; $\mathrm{ISE}$ at the largest grid bandwidth ($h=2.0$) should be at least $10\times$ your $\mathrm{ISE}(h^\*)$. Among your three histogram bin widths, the moderate one ($0.5$) should have the lowest ISE of the three.

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

**Verification:** [Tier 2 + Tier 3]
- **Tier 2:** the selector formula itself (Eq 3.31, with $A$ per Eq 3.30) — confirmed against Silverman (1986) Ch 3 §3.4, pp. 43–48.
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

**Verification:** [Tier 3]
Your RB curve must integrate to between 0.97 and 1.03 over the range you compute it on. Your variance ratio (plain-KDE variance $/$ RB variance, mean-pointwise) should be **at least 20** — RB should show a dramatic, not marginal, variance reduction; a ratio near or below 1 signals an implementation bug, most likely in the RB averaging step (Part A) rather than the bootstrap (Part C). The gamma full-conditional form itself is a tier-2 conjugacy fact, already derived in your PS7.4 work — no new derivation is required here.

**Discussion note:** (folded) The Rao-Blackwell theorem guarantees $\hat f_{\text{RB}}$ can't have *higher* variance than the plain empirical estimator, but it doesn't by itself tell you the advantage will be this large — a two-to-three-order-of-magnitude reduction is typical in exactly this setting (a scalar marginal with a smooth, closed-form conditional and a well-mixed chain), because the plain KDE is throwing away everything except the raw $\theta_3$ draws, while the RB estimate uses every retained $\beta$ draw's full conditional shape. This pattern — conditioning on structure a Gibbs sampler already computed, rather than discarding it after the draw is taken — is precisely the *parametric* Rao-Blackwellization R&C describe specifically for Gibbs samplers (their Ch 7 treatment, Example 7.15 / Eq 7.11): their general form for a Gibbs chain $(x^{(t)},y^{(t)})$ is $\hat f_X(x) = \frac{1}{T}\sum_t f(x \mid y^{(t)})$, of which this problem's $\hat f_{\text{RB}}$ is a direct instance, and their own worked examples (a bivariate-normal Gibbs sampler; a missing-data Poisson model) demonstrate the same kind of dramatic variance reduction you just measured. G&H §6.4.4 is useful background for the *general* Rao-Blackwell principle (the conditional-variance inequality guaranteeing RB can't do worse than the plain estimator), but their own worked example there is a static rejection-sampling setting, not an MCMC one — R&C is the more directly on-point source for what this problem does. The specific numbers here come from your own chain either way, not from either text.

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

**Verification:** [Tier 2 + Tier 3]
- **Tier 2:** $f_0$ is the same fully-known generative fact used in PS9.1.
- **Tier 3:** your kNN ISE should exceed your PS9.1 KDE ISE (at $h^\*$) by a ratio of at least $1.5$. Your kNN tail-mass integral over $[5,30]$ should fall roughly in $[0.03, 0.12]$; your KDE tail-mass integral over the same region should be at least $10\times$ smaller than your kNN tail-mass.

**Discussion note:** (folded) The contrast is structural, not incidental to this particular sample: as $x$ moves away from the bulk of the data, $R_k(x)$ — the distance to the $k$-th nearest point — grows roughly linearly in $x$ (the $k$ nearest points are just your most extreme sample points, however far away $x$ is), so $\hat f_{\text{kNN}}(x) = k/(2nR_k(x))$ shrinks only like $1/x$: slow, polynomial decay. The Gaussian kernel, by contrast, contributes $\exp(-u^2/2)$ per point, so once $x$ is a few bandwidths from every sample point, the KDE is numerically indistinguishable from zero — decay is super-exponential. This is why kNN density estimates do not integrate to 1 (their tails are not integrable over an unbounded domain, a genuine mathematical property of the estimator, not a bug) while the Gaussian KDE always does. Practically: kNN's adaptivity is a double-edged sword — in sparse regions it widens $R_k(x)$ to keep including $k$ points, which is exactly the local adaptivity that makes it attractive in multivariate settings with regions of very different density, but the same mechanism is what produces the heavy, non-vanishing tail you just measured. Silverman (1986) Ch 5 §5.2 gives this exact estimator (his Eq 5.1, matching the formula above with the one-dimensional constant $c_1=2$) along with its formal bias-variance analysis (Eqs 5.4–5.5) and states the non-integrability property directly; Givens & Hoeting §10.4.3.1 give the same estimator in general dimension $p$ (their Eq 10.47) and are the more specific source for the double-edged-sword point above — they note that in a single dimension this kind of local adaptivity brings little advantage over an ordinary fixed-bandwidth kernel estimator, but that the same mechanism offers substantially more promise once you move to multivariate data, which is the module's motivation for introducing the method here despite its underwhelming 1-D performance.

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

**Verification:** [Tier 3]
Using seed $=7$ exactly: your LOO-CV-selected bandwidth should yield a KDE with **exactly 2** local maxima, located within about $\pm 0.3$ of $x=-1.03$ and $x=1.49$. Your large/conservative bandwidth ($1.3\times$ the smallest grid $h$ giving 1 mode) should yield a KDE with **exactly 1** local maximum, located within about $\pm 0.3$ of $x=-0.30$. A different mode count at this exact seed indicates an implementation bug (a structural fact of this fixed dataset), not sampling variation.

**Discussion note:** (folded) The generative truth has two modes at $\pm 1.186$ (from the mixture's symmetric $\pm 1.3$ component means, each with $\mathrm{sd}=1.0$). $h_{\mathrm{CV}}$'s two peaks (near $-1.03$ and $1.49$) land close to the true mode locations — in this instance, the data-driven choice happens to recover the right qualitative picture. $h_{\text{large}}$'s single peak (near $-0.30$) sits almost exactly *between* the two true modes: it isn't a bad location for a single "compromise" summary, but it actively misrepresents the population as unimodal-and-centered when it is really two symmetric subpopulations — a viewer shown only this plot would draw the wrong conclusion about the data's structure. Neither choice was unreasonable to make *before* the reveal: LOO-CV is a standard, principled selector, and "smooth more when $n$ is small and you're unsure" is genuinely sound practical advice in general — it just happens to be wrong here. That is the point of this problem: a defensible process does not guarantee a correct outcome, and mode count in particular is exactly the kind of feature a bandwidth choice can silently erase or fabricate. The base-rate check found this exact divergence in only about 42% of draws from this population — worth a sentence in your own write-up: bimodality that is only sometimes visible, depending on the specific sample, is itself a realistic and common situation, not a contrived one.

---