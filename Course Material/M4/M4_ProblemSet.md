# Computational Statistics — Problem Sets

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

**Verification:** [Tier 1 + Tier 2 + Tier 3]
- **Tier 1:** R&C Ch. 5, Ex. 5.1 (solved; arXiv:1001.2906) establishes that this mixture family's (μ₁,μ₂) log-likelihood surface is comparable across different realizations of the same generating process — fixed-split vs. random-split draws at the same true parameters and n. Dataset A and Dataset A′ instantiate that comparison.
- *Note on Dataset B:* Separately, and not itself a replication of 5.1 or 5.13: the same model family can produce a qualitatively different surface — unimodal rather than bimodal — when true separation and sample size are both smaller (Dataset B). This is an original observation on this model family, confirmed by the grid search below; it is distinct from 5.1's realization-invariance result above, and it is not a reproduction of 5.13's illustration (which changes the generating model's component count, not just separation within a two-component model).
- **Tier 2:** the median-as-L1-minimizer identity is a standard convex-analysis/order-statistic fact: Σ|xᵢ−c| is piecewise-linear in c, with slope changing sign exactly at the median for odd n.
- **Tier 3:** your grid search should find **exactly 2** local maxima for Dataset A (near (0.05, 3.90) and (4.25, 1.20)), **exactly 2** for Dataset A′ (near (−0.15, 3.95) and (4.10, 0.20), seed 20260720 — the *global* mode matches Dataset A's near (0, 4), while the *secondary* is again a far, label-switched mode whose exact location is realization-dependent; it is this two-mode structure, not the secondary's precise position, that carries the Tier-1 realization-invariance point above), and **exactly 1** for Dataset B (near (0.58, 0.63)), each within one grid cell (~0.05–0.08) of these values. Your numerical median check should agree with the sample median to within 1e-4.

**Discussion note:** Dataset A and Dataset A′ share the same generating parameters and n and differ only in how the component split is realized — this is the clean isolation of "the surface's shape is a property of the realized sample," holding the model and its parameters fixed (the realization-invariance point Ex. 5.1 makes). Dataset B is a different kind of contrast: it changes the true separation (itself a model parameter) *and* the sample size, so its shift from bimodal to unimodal reflects a change in the generating parameters, not just the draw — the two comparisons answer different questions and should not be conflated. A common mistake is to grid over too narrow a range and miss the second peak (Dataset A) or to over-interpret grid noise as a spurious extra peak (always check that a candidate peak survives a finer grid before reporting it — we checked stability across four resolutions). For part (b), note that L1 loss is non-differentiable at each data point, so a naive gradient-based minimizer may need to be a derivative-free 1-D method (golden section, `scipy.optimize.minimize_scalar(method='bounded')`) rather than Newton's method — file this away, since Newton's method (PS4.2) will assume enough smoothness for a well-defined Hessian.

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

**Verification:** [Tier 3]
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

**Verification:** [Tier 2 + Tier 3]
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

**Verification:** [Tier 2 + Tier 3]
- **Tier 2:** your own fully specified generative process (seed, π, means, variances) is the citable fact grounding "what the truth is" for comparison; R&C Ex. 5.10's canonical two-component-mixture EM motivates this design by concept.
- **Tier 3:** your log-likelihood sequence must never decrease by more than 1e-8 at any single iteration (reference run: every increment was strictly positive; the smallest was +7.9×10⁻¹¹, i.e. no violation was actually observed — 1e-8 is a safety margin for floating-point noise, not a reflection of an observed failure). Your converged (μ₁,μ₂) should match your own grid-search cross-check to within one grid cell. Your bad-(identical-init) run should converge with π≈0.5 and μ₁≈μ₂ (both components collapsed together), with final log-likelihood at least 10 nats worse than your good-init run's (reference run: (π,μ₁,σ₁²,μ₂,σ₂²) = (0.5, 3.214, 4.852, 3.214, 4.852), a gap of 16.86 nats — Validation Log `PS4.4`, `reference_impls/ps4_4_ref.py`).

**Discussion note:** *(folded)* **Data-policy note:** the source exercise (R&C 5.10) uses the real `log(deaths)` dataset from the MASS R package. Per the module's sourcing rules, that series is not reproduced here — it runs well over the ~50-value inline-reproduction limit and is not hosted at a persistent, small, openly licensed URL — so a synthetic mixture with a fully specified generative process substitutes for it. **On the bad initialization:** exact ties are what reliably trap this dataset's EM at an inferior fixed point — nearby-but-not-identical bad starts (e.g., both means within the same cluster but slightly apart) were checked and eventually break symmetry, just more slowly (roughly 150 iterations instead of 90) — so if your own experiments with a "nearly-tied" start don't reproduce the failure, that is expected, not a bug; use the *exact* tie as specified to guarantee the demonstration.

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

**Verification:** [Tier 1 + Tier 3]
- **Tier 1:** R&C Ch. 5, Ex. 5.7 (solved; arXiv:1001.2906) is the citation anchor for the study design this problem adapts — an SA loop run across several temperature schedules, 100 replications each, classified against a dominant/secondary mode. The recovery-rate pattern itself is not asserted in 5.7's solution prose (its percentages appear only in Fig. 5.4's panel titles); the qualitative direction — slower cooling recovers the dominant mode more often — is established here by the tier-3 logged run alone.
- **Tier 3:** your slow-geometric schedule's recovery rate should exceed your fast-geometric schedule's by at least 15 percentage points (we got 88/100 vs. 64/100) — the *direction and rough magnitude* of this gap is what must reproduce, not the exact counts, since outcomes are seed-dependent.

**Discussion note:** *(folded)* Why n=30 here and not PS4.1's larger Dataset A: at n=400, moving (μ₁,μ₂) by half a unit changes the log-likelihood by roughly 100+ units — two orders of magnitude larger than any reasonable temperature — so every schedule ends up behaving like plain greedy hill-climbing and the schedules become indistinguishable (checked directly: all four schedules landed in a narrow 63–69% band at n=400). The smaller-n dataset keeps the temperature scale and the likelihood's dynamic range comparable, which is what makes the schedule actually matter — a reminder that "temperature" is only meaningful relative to the scale of the objective it's operating on. Optional theory sub-part (uncounted toward the 45 min above, for students who want the "why"): R&C Ex. 5.6's pseudo-posterior πₘ(θ|x) ∝ ℓ(θ|x)^m construction shows *analytically* that raising a likelihood to an increasing power concentrates its mass on the mode as m grows — exactly the mechanism a falling temperature (equivalent to a rising effective power 1/T) exploits.

---