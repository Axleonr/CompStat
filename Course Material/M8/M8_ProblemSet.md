# Computational Statistics — Problem Sets

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

**Verification:** [Tier 3] For every one of the eleven saved parameters: the max absolute difference between your from-scratch ρ_k and the library ACF value, over lags k = 0..50, should be < 0.01; and |ESS_scratch − ESS_library| / ESS_library should be < 0.05 (5%).

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

**Verification:** [Tier 3] Healthy configuration: R-hat should be < 1.01 for all eleven parameters. Failing configuration: R-hat should be > 1.5.

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

**Verification:** [Tier 1, Tier 3]

Tier 1.
Vehtari's Aalto BDA course material (cite by content, not by an assignment sub-part number, which drifts across course years) for:

- The published classic R̂ ≈ 1
- The rank-normalized R̂ = 1.39 vs. the 1.01 threshold.

Tier 3. 

- For your own classic R-hat: it should fall in $[0.95, 1.10]$ at $n = 1,000$.
- No fixed numeric target is given for a self-implemented rank-normalized computation; if you attempt one, report it as an open exploration rather than a pass/fail check.

**Discussion note:** Your own classic R-hat on this N(0,1)-vs-t₃ pair should land very close to 1, reproducing the cited surprising result: two chains that are visibly, obviously sampling different distributions (different variance, different tail weight) can still show a "textbook-good" classic R-hat, because that statistic is built entirely from first- and second-moment (mean/variance) comparisons and has no way to see a difference in tail shape once means and rough scales roughly align. This is precisely the motivation for the rank-normalized version: transforming to ranks before comparing is designed to be sensitive to distributional differences that a pure variance-ratio statistic can miss. If you attempted your own from-scratch rank-normalization, you may well have found that a plain rank-transform on i.i.d. draws does not by itself reproduce the published 1.39 — that number depends on details of Vehtari et al.'s reference implementation (which also incorporates chain-splitting and, for other diagnostics, "folding") that go beyond a first attempt at the idea. That is a legitimate, informative finding, not a failure on your part: the qualitative lesson (R-hat's classic form can be blind to shape differences; rank-normalization is designed to help) stands regardless of whether your run managed to reproduce the exact published constant from first principles.

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

**Verification:** [Tier 1 — cite R&C Ch. 8 Exercise 8.1 (solved) for the theoretical direction: thinning cannot reduce variance relative to using every draw. Tier 3.] You should observe Var(thinned, m=1800) / Var(all, 18000) > 2, and Var(first-1800-unthinned) / Var(thinned, m=1800) > 1.05.

**Discussion note:** (folded) The first inequality is the R&C 8.1 result made concrete: using only 1,800 of your 18,000 draws (even spread evenly across the whole run) always costs you variance relative to using everything — thinning discards information, full stop, and the cost is not small (roughly 5–6x the variance, consistently, across many independent trials). The second inequality is the more interesting, easy-to-miss point: *if* you are somehow constrained to store only 1,800 draws total (a genuine memory/storage constraint, not a compute one), spreading those 1,800 draws across the whole run (thinning) still beats keeping only the first 1,800 draws you happened to generate — a short contiguous block is more autocorrelated internally than a thinned sample of the same size, so it carries less independent information per draw. This is the *only* legitimate practical argument for thinning: not that it improves efficiency (it never does, relative to keeping everything you generated), but that *given a hard storage budget smaller than your full run*, spacing out what you keep beats truncating to a short run of the same stored size. If your compute budget allows generating and keeping all the draws, there is no argument for thinning at all.

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

**Verification:** [Tier 3.] After adjustment: multi-chain R-hat should be < 1.01; the pooled sample mean should satisfy |mean − 0| < 1.0; the pooled sample variance should satisfy |variance − 26| < 3.0; each chain's right-mode-visit fraction should fall in [0.3, 0.7].

**Discussion note:** Your Step 1 diagnosis should show a genuinely ambiguous single-chain signal: the from-scratch ESS on the failing chain is a small fraction of its retained draws — clearly not great, but the number alone doesn't scream "catastrophic failure" the way you might expect (a low ESS is also just what a slow-mixing-but-otherwise-fine chain looks like). 

In our own run, we found the failing chain's ESS to be the *same order of magnitude* as the healthy, post-adjustment chain's ESS — a genuinely useful, slightly uncomfortable finding: single-chain ESS alone did not cleanly separate "broken" from "fine" here. Note what that means against your PS7.6 work: the qualitative evidence you already had there (a trace that never approaches the second mode; a near-zero mode-occupancy fraction) was *more* decisive than the formal single-chain statistic you have now added — formalizing a diagnosis does not automatically strengthen it. What did the job decisively was the multi-chain R-hat (only visible once you have more than one dispersed start) together with that same qualitative fact. Relatedly, Step 4's tolerance bands are deliberately the same ones your PS7.6 contrast run cleared — what is new here is not the bands but the standard of evidence: four dispersed chains agreeing with each other, not one chain agreeing with the truth. 

This is this module's version of R&C's Example 8.3/8.4 (the noisy AR(1) model), where every one of the chapter's diagnostics reported a clean pass on a chain that had, in fact, never left a minor secondary mode — a standing reminder that a green light from any single diagnostic, run on a single chain, is never sufficient proof of convergence. It is also a concrete instance of Betancourt's "Towards a Principled Bayesian Workflow" Step Ten: when a computational method's self-diagnostics fail, the appropriate response is to return and reconfigure the algorithm (here: the proposal scale) — and, more generally, if reconfiguring the algorithm had *not* resolved the failure, the appropriate next move would be to question the model or experimental setup itself, not to keep re-tuning indefinitely. 

Separately, and worth noting for its own sake: your Module 7 Gibbs sampler (PS7.3/PS7.4) never had a "proposal scale" to tune in the first place, because it accepts every draw by construction — but as this chain's original delta = 0.5 run showed (acceptance rate ≈ 0.84, yet total failure to mix across modes), a *high acceptance rate is not itself evidence of good mixing* for a Metropolis-type sampler either; acceptance rate and genuine exploration are different things, and this capstone's own diagnosis step is a direct demonstration of that gap.

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

**Verification:** [Tier 3.] Averaged over your 30 replications, the average gap using all 10 draws should exceed the average gap using the last 8 draws (first 2 discarded) by at least 50% (ratio > 1.5), for beta.

**Discussion note:** A single 10-iteration replication's with/without comparison can go either way — we found the "discard warm-up" side smaller in only about 84% of individual short replications, which is exactly why this problem asks you to average over 30 of them rather than trust any one run. That is not a flaw in the exercise; it is itself an honest lesson about warm-up: the *benefit* of discarding early draws is a statement about reducing systematic bias in expectation, not a guarantee that removes noise from any single short run. Averaged over enough replications, the benefit becomes clearly visible (this session's reference run found the with-warm-up gap roughly 2.3–2.8 times the without-warm-up gap, consistently, across several independent 30-replication batches). You should also notice that beta (the shared hyperparameter) shows a larger absolute gap than theta_5 (a pump-specific parameter) under the bad initialization — beta starts furthest, in relative terms, from its equilibrium value (1000 vs. a true posterior mean near 6), while each theta_i is pulled hard toward its own pump's data on the very first Gibbs step regardless of beta's starting value. The general principle Goal 4 wants you to take from this: draws generated before the chain has reached the typical set of the posterior are not samples *from* the posterior, and averaging them in — even just a couple of badly-placed early draws in a short chain — measurably pulls your estimate away from the truth in the direction of wherever you happened to start.

---