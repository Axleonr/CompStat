# Computational Statistics — Problem Sets

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

**Verification:** [Tier 1] Vehtari, Aalto BDA course (CS-E5710), Assignment 3 notebook (`avehtari.github.io/BDA_course_Aalto/assignments/template3.html`; accessed 07/15/2026). 

The four data values above are that notebook's own stated **test-input subset** for its `mu_point_est`/`mu_interval`/`mu_pred_point_est`/`mu_pred_interval` functions (the notebook's full `windshieldy1` sample has n=9; the test subset — used here so the cited machine-checked values apply exactly — is these same four values). The notebook's confirmed machine-checked values on this exact subset: posterior mean of $\mu$ = 14.5, 95% posterior interval = (13.3, 15.7); posterior-predictive mean = 14.5, 95% predictive interval = (11.8, 17.2); marginal-$\mu$ Student-$t$ parameters (df=3, location=14.5, scale=0.3817557); predictive Student-$t$ parameters (df=3, location=14.5, scale=0.8536316). Your computed values should match these exactly (up to rounding/Monte-Carlo noise in the joint-draw plot only — the closed-form numbers in (ii) and (iv) should match to at least 3 significant figures).

Self-audit checklist (**self-audit is explicitly the weakest verification mode in the program; it is not disguised as anything stronger here**, supplemented in this problem by the tier-1 numeric target above):
- [ ] All three model components (likelihood, prior, joint posterior) are written out explicitly, not just named.
- [ ] The improper-prior / proper-posterior distinction is stated in your own words, including the $n\ge2$ condition.
- [ ] Your reported posterior mean/interval for $\mu$ and your predictive mean/interval match the tier-1 target values above.
- [ ] Your explanation of the predictive interval's extra width names both uncertainty sources (not just one).
- [ ] The structural-pattern note names the specific mechanism (nuisance-parameter integration → Student-$t$ marginal), not just "it's more spread out."

**Discussion note:** A correct solution shows the posterior interval for $\mu$ noticeably narrower than the predictive interval for $\tilde y$ — this is the concrete payoff of distinguishing "uncertainty about a parameter" from "uncertainty about a future observation," a distinction many students conflate on first exposure. The most common failure mode is using the Normal quantiles instead of $t_{n-1}$ quantiles for the interval (a small-$n$ error that vanishes as $n$ grows, which is worth noting explicitly since $n=4$ here makes the Normal-vs-$t$ gap unusually visible). **Design note:** this problem deliberately uses the assignment's 4-observation *test* subset rather than the full 9-observation `windshieldy1` sample specifically so that the cited tier-1 target values apply without adaptation — students curious to see the intervals narrow with more data are welcome to repeat the exercise on the full sample as an ungraded extension, but no numeric target is supplied for that larger sample here. **Note:** this problem's prior $p(\mu,\sigma)\propto\sigma^{-1}$ is improper and therefore has no proper prior distribution to forward-simulate from; "prior predictive simulation" is not defined here, which is itself worth knowing as a limit case of Goal 4's prior-checking machinery.

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

**Verification:** [Tier 2 for the closed-form facts + Tier 3 for the simulation] The Beta-Binomial conjugate posterior update and the Beta-Binomial compound (prior-predictive) mean formula $n\cdot a/(a+b)$ are standard closed-form results for this conjugate family (cite any standard treatment of conjugate Binomial models, e.g. the assigned BDA3 Ch. 2 treatment of the Beta-Binomial model). The prior-predictive simulation values are tier-3 (20000 draws/prior, seed 20260715): simulated predictive means 6.670 / 19.985 / 20.030 for Beta(2,10)/Beta(1,1)/Beta(20,20) respectively (vs. analytic means 6.667 / 20.000 / 20.000 — agreement within Monte Carlo noise, confirming the cross-check in step 3 is a real, reproducible check and not a coincidence); logged 90% predictive intervals [1,16] / [1,38] / [13,27]; logged posterior means 0.3269 / 0.3810 / 0.4375.

Self-audit checklist (self-audit is explicitly the weakest verification mode in the program; supplemented here by the tier-2 closed forms and the tier-3 logged run):
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

**Verification:** [Tier 1] Gelman et al., *BDA3*, Ch. 5, Exercises 5.11 and 5.12 (solved in `sites.stat.columbia.edu/gelman/book/solutions3.pdf`;  accessed 08/11/2026). 
- Your Part A conclusion (no closed form; conjugacy failure is the specific cause) should match the argument shape of BDA3 5.11(b)–(c).
- Your Part B closed form should match BDA3 5.12's target exactly:
  $$E(\theta_j\mid\tau,y) = \dfrac{y_j/\sigma_j^2 + \hat\mu/\tau^2}{1/\sigma_j^2+1/\tau^2}$$
  , a precision-weighted average of the group datum and the (precision-weighted) population mean estimate.

Self-audit checklist (self-audit, supplemented here by the tier-1 target above):
- [ ] Part A's joint posterior explicitly includes all three levels (likelihoods, population distribution *with* the Jacobian, hyperprior) — not collapsed or skipped.
- [ ] The no-closed-form argument names conjugacy failure specifically (not just "it's hierarchical so it's hard").
- [ ] The Beta-population contrast case is stated (what changes if $\theta_j\sim\text{Beta}$ instead).
- [ ] Part B's derived formula matches the tier-1 target exactly, including which quantities are known/fixed at each step.
- [ ] Both limiting cases ($\tau\to0$, $\tau\to\infty$) are stated and connected to pooling.

**Discussion note:** The two parts are deliberately paired: Part A shows a hierarchical model that is *structurally* elementary (three honest levels, nothing exotic) but computationally closed to you until Module 7's tools arrive; Part B shows a hierarchical model where the *same* three-level structure resolves completely by hand. The dividing line is not "hierarchical vs. not" — it is conjugacy at each level. A common error in Part A is trying to "integrate out $\theta_j$ anyway" by expanding the Binomial kernel and hoping terms cancel; there is nothing to find, and recognizing there is nothing to find (and being able to say precisely why) is the actual skill being tested. A common error in Part B is forgetting that $\mu$ itself has posterior uncertainty (treating it as a known constant beyond step 4) — this is the reason step 5's $\hat\mu$ substitution matters and is not just notational. **Forward pointer:** Part A's exact model (logit-Normal population on a Binomial likelihood) is the computational problem Module 7's Gibbs/Metropolis-within-Gibbs material solves — this problem is what tells you *that* the sampler is needed; Module 7 is what builds one.

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

**Verification:** [Tier 1, Tier 3] 

**Tier 1**.
Cite McElreath, *Statistical Rethinking* course, (`https://github.com/rmcelreath/stat_rethinking_2023`; accessed 08/11/2026), Week 6 Problem 1 for:

- The qualitative phenomenon: widening the $\sigma$-prior pushes prior tank-survival mass toward the 0/1 edges. It is a documented result for exactly this varying-intercepts prior structure.
- The prior structure and the $\lambda\in\{10,0.1\}$ comparison rates.

**Tier 3**. 
Reference run, seed 20260715, 20000 draws/setting.
- Obtained edge mass **0.004 / 0.072 / 0.575** for $\lambda=10/1/0.1$ respectively — a monotonic, order-of-magnitude-scale increase. 

Your own run should reproduce this monotonic direction and its dramatic scale (not the exact fractions, which are seed-dependent).

Self-audit checklist (self-audit is explicitly the weakest verification mode in the program; supplemented by the tier-1 qualitative citation and the tier-3 logged run):
- [ ] All three $\lambda$ settings are simulated with the full three-step draw (σ, then ᾱ, then $\alpha_j$) — not a shortcut that skips a level.
- [ ] The overlay plot shows all three densities distinctly, restricted to $(0,1)$.
- [ ] Edge mass increases monotonically as $\lambda$ decreases, and the explanation names the logit-vs-probability-scale mechanism specifically (not just "more spread out").
- [ ] The Goal 4 connection states a concrete practical consequence (check the implied prior predictive before fixing a hyperprior), not just a restatement of the definition of prior-predictive checking.
- [ ] No posterior sampler was used — this is pure forward simulation from named distributions.

**Discussion note:** This is the module's sharpest illustration of a genuinely counter-intuitive fact: "wide" is not the same as "uninformative," and the scale on which a prior is specified matters enormously for what it implies. A $\sigma\sim\text{Exponential}(0.1)$ prior *looks* diffuse and safe on the log-odds scale, but it concentrates a large fraction of prior mass at essentially-certain-survival or essentially-certain-death — a strong, and probably unintended, implicit claim. The common failure mode is describing the result only as "the plot gets more spread out," without naming the actual mechanism (a wide spread in $\alpha_j$ maps, through the logistic/inverse-logit function's saturating shape, to values that are pinned near 0 or 1 whenever $|\alpha_j|$ is more than a few units from zero).

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

**Verification:** [Tier 1] 
Gelman et al., *BDA3*, Ch. 5, Exercises 5.9 and 5.10 (solved in `sites.stat.columbia.edu/gelman/book/solutions3.pdf`;  accessed 08/11/2026). 

Both exercises examine exactly this improper-hyperprior hazard (5.9 for the hierarchical-binomial reparametrized case, 5.10 for the hierarchical-normal case used here). The target your argument should reach matches **BDA3 5.10**'s confirmed result: 
- $p(\mu,\tau)\propto\tau^{-1}$ gives an improper posterior
- $p(\mu,\tau)\propto1$ gives a proper posterior **if and only if $J>2$** — a clean binary condition.

Self-audit checklist (self-audit; the tier-1 citation above supplements it):
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

Self-audit checklist:
- [ ] Part (a)'s collapse argument is derived as a limit of the PS5.3 shrinkage formula, not asserted independently.
- [ ] Part (b)'s independence result and pairwise-$\Phi$ formula are both stated, and the integral for $\Pr(\theta_i\text{ largest})$ is correctly set up (correct integrand, correct single free variable) even though it is not evaluated.
- [ ] No grid-over-posterior-conditionals and no posterior sampler appear anywhere in this problem (the $\triangle$ grid reading is not used here — this problem stays inside the pure closed-form/derivation lane).
- [ ] The optional/redundant label is visible and the reason (duplicates PS5.3 and PS5.2/PS5.5) is stated, not just implied.

**Discussion note:** Parts (a) and (b) are the two extremes that make the shrinkage formula's behavior (PS5.3 Part B, step 6) concrete on a specific, well-known dataset: complete pooling erases all between-school distinctions, no pooling treats every school as unrelated, and the actual hierarchical posterior (not computed here — that is Module 7's job, per the forward pointer in PS5.3) sits somewhere between the two. This problem is scoped to the closed-form derivation only; the fully evaluated $\Pr(\text{best})$ table is presented as confirmed, citable, optional illustration rather than a required computed deliverable, since evaluating the single integral in part (b) would require one-dimensional quadrature or simulation.

---