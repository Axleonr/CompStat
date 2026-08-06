# Computational Statistics Program — Problem Set Requirements
## Design Specification for the Exercises Build (Wave 3)
*Version 1.1 — requirements only. This document specifies what the problem sets must be; it does not contain the problems themselves. It is the governing specification against which drafted problem sets will be evaluated.*
*Changelog from 1.0: Section 4 (Sourcing and Data Policy) rewritten around a fact-anchoring and executable-validation policy; R1 tightened to require a citable or executed basis for every verification target; Section 7 gains a required validation-log deliverable.*

---

## 1. Purpose and Position in the Program

The program currently assesses understanding through two instruments: the quick checklists (module goals reworded as "can I do this?" prompts) and the conceptual questions (explanation, connection, and reasoning — explicitly not calculation). Neither instrument exercises the thing the program is fundamentally about: **writing, running, breaking, and diagnosing statistical algorithms.** Roughly half the module goals begin with "Implement," "Compute," "Apply," or "Observe," and none of them currently has a practice vehicle.

Problem sets fill that gap. They are the third assessment instrument, sitting between the conceptual questions and the Module 10 applied cases:

| Instrument | Tests | Mode |
|---|---|---|
| Quick checklist | Coverage — did the reading land? | Self-report |
| Conceptual questions | Understanding — can you explain and connect? | Written reasoning |
| **Problem sets (this build)** | **Execution — can you implement, verify, and diagnose?** | **Code + short write-up** |
| Applied cases (Wave 4) | Judgment — can you integrate under ambiguity? | Open-ended workflow |

**Boundary with Wave 4:** Problem sets are *closed* problems — each has a defined target and a defined way for the student to know they got it right. Applied cases are *open* problems where the choices made determine the quality of the conclusions. A problem that requires choosing between methods under genuine ambiguity belongs in Module 10, not in a problem set. This boundary is a scope-discipline rule: enforce it during drafting.

---

## 2. Governing Constraints (non-negotiable requirements)

**R1 — Self-verifiability.** There is no instructor and no grader. Every problem MUST include a mechanism by which a solo learner can determine, with high confidence, whether their solution is correct. Acceptable mechanisms, in order of preference:

1. **Known-answer targets:** the problem is posed against a target with a closed-form or analytically known answer (e.g., estimate an integral whose true value is known; sample from a distribution whose moments are known), so the implementation can be checked against truth.
2. **Convergence/consistency checks:** the correct implementation exhibits a verifiable quantitative signature (e.g., Monte Carlo error shrinking at the n^(−1/2) rate on a log-log plot; coverage of a bootstrap CI approaching nominal level over repeated simulation).
3. **Cross-method agreement:** two independent methods the student has already implemented must agree (e.g., inverse transform vs. acceptance-rejection on the same target; hand-rolled Gibbs vs. direct sampling on a conjugate model).
4. **Library-as-oracle comparison:** a standard library implementation is used *only* to verify a from-scratch implementation, never to substitute for it.

A problem with no verification mechanism from this list is not compliant and must be redesigned or moved to Wave 4.

**R1a — Provenance of the verification target (added in v1.1).** A verification mechanism is only as trustworthy as the number it is checked against. Regardless of whether the problem statement is original or adapted, the specific value, rate, or bound used in R1 (the "true" integral, the theoretical acceptance-rejection constant, the nominal coverage level, the conjugate posterior's closed form) MUST rest on one of:
1. a **citable mathematical fact** traceable to an assigned source or a standard reference (a conjugate-family result, a textbook table of moments, a named theorem) — cite it in the instructor-facing note; or
2. an **executed derivation** — the drafter has actually run a reference implementation and recorded the result in the validation log (Section 7).
A verification target that is merely asserted — computed silently during drafting with no citation and no logged execution — is non-compliant. This closes the specific failure mode where an unverified numeric claim is taken on faith; see Section 4 for the sourcing policy this supports.

**R2 — Goal traceability.** Every problem MUST cite the module goal(s) it exercises, using the numbering in `Module_Goals_Reference.md`. Every implementation-type goal (goals containing "Implement," "Compute," "Apply," or "Observe") MUST be exercised by at least one problem. Conversely, no problem may require material outside the module's assigned readings and its declared prerequisites — the same scope discipline applied to readings applies here. A goal-to-problem alignment matrix is a required deliverable per module (Section 7).

**R3 — Language neutrality.** Problems MUST be solvable in Python, R, or Julia. Problem statements are written in prose and mathematics, never in language-specific code. Where scaffolding is needed, use pseudocode. No starter-code repositories; the program has no infrastructure to maintain them.

**R4 — From-scratch policy.** The core algorithm named by the goal MUST be implemented by the student from primitives (loops, arithmetic, and the language's *uniform* RNG). Libraries are permitted for: (a) uniform random number generation (with the exception below), (b) linear algebra, (c) plotting, (d) verification per R1.4, and (e) any machinery from a *previous* module that the current problem is not about (e.g., using a library optimizer inside a Module 7 problem is fine; using it in a Module 4 Newton's-method problem is not). Module 1 exception: problems on PRNG mechanics implement the generator itself (an LCG at minimum), then may use library uniforms thereafter.

**R5 — Reproducibility.** Every problem involving randomness MUST require the student to set and report a seed, and every write-up must state what was run so that the student (or a future reader) could rerun it. This is a program-level value (Module 1, Goal 6; Module 10, Goal 5) rehearsed continuously rather than introduced at the end.

**R6 — Failure-mode representation.** The program's identity claim is that a practitioner should "recognize when a method is failing." Every module's problem set MUST include at least one **diagnosis problem**: a problem in which the student deliberately constructs or is handed a failing configuration (pathological importance weights, heavy-tailed bootstrap, non-mixing chain, over/under-smoothed KDE) and must produce and interpret the diagnostic evidence of failure. These problems are where the checklist verbs "identify," "recognize," and "diagnose" get exercised.

**R7 — Time discipline.** Each problem carries an estimated time; each problem set carries a total budget (Section 5). Problems exceeding ~2 hours must be split or trimmed. The lesson from the readings evaluation applies directly: unscoped assignments create overruns, so every problem states its deliverable explicitly ("a plot of X and a 3–5 sentence interpretation," not "explore X").

---

## 3. Problem Taxonomy

Each problem is typed. A compliant problem set draws on all four types, with the mix varying by module (Section 6).

- **Type I — Implementation.** Build the named algorithm from scratch against a known-answer target (R1.1/R1.3). The canonical type for "Implement" goals.
- **Type V — Verification & error behavior.** Study the implemented algorithm's quantitative behavior: convergence rates, variance comparisons, coverage experiments, efficiency measurements (R1.2). This is where "characterize its error" goals live.
- **Type D — Diagnosis & failure.** Construct or receive a failing case; detect and explain the failure from its computational symptoms (R6).
- **Type C — Connection.** A short problem that operationalizes a cross-module bridge in code (e.g., SIR built directly on the Module 2 importance sampler; bootstrap framed as a Module 1 resampling algorithm; ESS computed from the Module 7 chain). Connection problems keep the spine (1–2 → 6 → 7–8) load-bearing in practice, not just in prose.

**Deliverable format (all types):** working code + a short written component (typically 3–8 sentences or a labeled plot with interpretation). The write-up is not optional — the program's position is that output without interpretation is not statistics. But write-ups are capped in length to prevent the problem sets from becoming essay assignments; extended reasoning belongs to the conceptual questions.

---

## 4. Sourcing and Data Policy (revised v1.1)

The original v1.0 policy ("original problems preferred, adapted textbook exercises as a supplement") under-specified how a solo-study problem set defends against its highest actual risk: **an LLM-drafted verification target that is wrong but looks authoritative.** Full sourcing from textbooks does not solve this either — most assigned texts either lack exercises entirely (Silverman, LPW as a monograph) or publish only partial, non-public solutions, so a "sourced" problem is typically source-verified in its *statement* but still unverified in its *answer*. The policy below targets the answer directly, and treats problem-statement provenance as a secondary, non-blocking preference.

**4.1 — Three tiers of problem provenance, in order of preference:**

1. **Harvested from a solution-published source.** A small number of assigned or closely-aligned texts have public author-provided solutions and can be drawn on with minimal adaptation risk: BDA3's partial official solutions (Gelman's book site), and Robert & Casella's *Introducing Monte Carlo Methods with R*, whose odd-numbered exercise solutions the authors published openly — pedagogically aligned with the assigned MCSM text by the same authors, though it is not itself an assigned source and would need a bibliography entry if drawn on. Any other course materials with public solutions (e.g., instructor-posted assignments with self-check code) may be used if verified to actually carry a working, public answer — do not assume a linked course page still resolves or still matches the current edition. Adaptation must still be cited per 4.2.
2. **Original problem, fact-anchored verification target.** The default tier. The problem statement is original, but the specific number, rate, or bound the student checks against is not computed ad hoc by the drafter — it is tied to a citable mathematical fact per R1a.1 (a conjugate-family result, a standard distribution's known moments, a textbook table, a named theorem, the theoretical acceptance-rejection bound). The instructor-facing note names the fact and its source.
3. **Original problem, executed verification target.** Where no closed-form fact is available (most Type D diagnosis problems, all Module 8 problems built on the student's own Module 7 output, all Type C connection problems), the drafter runs a reference implementation before the problem is finalized and records the run in the validation log (Section 7). This is not optional scaffolding — it is the compliance mechanism for R1a.2, and it is expected to be the majority tier for Modules 1, 8, and 9, where harvestable or closed-form material is thin.

Every problem in the set must sit in one of these three tiers; a problem whose verification target has neither a citation (tier 1/2) nor a logged execution (tier 3) is non-compliant, full stop — this is the operational form of R1a. Problems whose R1 mechanism is structured self-audit only, with no numeric verification target, carry the tier value `self-audit` in place of 1/2/3; R1a's citation/execution-provenance requirements do not apply to them, since there is no target for R1a to anchor.

**4.2 — Adaptation and citation.** Textbook exercises drawn on under tier 1, or lightly adapted for tier 2/3, may be *adapted* but not assigned by pointer ("do Exercise 5.3 in Owen") — pointer assignments create solution-manual dependence, edition fragility (the Lange lesson), and an unverifiable-answer problem identical to the one this policy is designed to avoid. Any adapted problem cites its source in the instructor-facing note, and the citation is verified against the source text per the established protocol before the problem set is finalized.

**4.3 — Data policy, in order of preference:**
1. **Student-generated synthetic data** with a specified generative process and seed. This is the default: it guarantees availability, makes truth known (serving R1), and is itself practice in simulation. It is also the natural partner of tier 2/3 verification, since the generative process *is* the fact or the executed derivation.
2. **Classic small datasets reproduced inline** in the problem statement (≤ ~50 values), eliminating link rot.
3. **External datasets only if** hosted at a persistent, stable URL, openly licensed, and small. Each external dataset is a fragility the maintenance process must track; minimize them. Real-data work is primarily Wave 4's job.

**4.4 — What this policy does not solve.** Fact-anchoring and executed validation defend against a *wrong number*. They do not by themselves defend against a *mis-scoped* or *misaligned* problem — a technically correct problem that exercises the wrong goal, assumes an unassigned reading, or leaks into Wave 4's territory. That risk is addressed by the existing goal-alignment and scope-discipline requirements (R2, Section 7's evaluation protocol), which apply regardless of provenance tier and are not weakened or replaced by this section.

---

## 5. Time Budget and Hour Accounting

**Open decision for the project owner (flag, do not resolve silently):** the module map's "Est. Hours" (orientation note, total ~96–119 against the 120-hour ceiling) does not state whether it includes practice time. Two options:

- **Option A (recommended):** Declare existing estimates to be reading + self-assessment only. Add an explicit "Problem set hours" column to the module map, sized per the table below (~28–39 hours program-wide). This breaches the 120-hour ceiling (~124–158 total), so adopting Option A requires either raising the ceiling or explicitly re-tiering the program (e.g., core problems vs. optional depth problems, with only core counted against the ceiling).
- **Option B:** Hold the 120-hour ceiling, treat existing hours as all-inclusive, and size problem sets to fit inside current module estimates. This forces the problem sets to be very small (~2–3 problems per module) and will under-serve the implementation goals.

The recommendation is Option A with a **core/optional split**: each problem set designates a core subset and optional-depth problems (uncounted), mirroring the reading guides' required/optional convention. **Core ≈ full §5 module budget; optional problems are uncounted and sit above the budget line** (ratified reading, `PSDEP-F2Resolution.md`; supersedes the earlier "~60–70% of the budget" phrasing — the §6 mandatory per-module lists are binding requirements and are not thinned to hit a ratio). Whichever option is chosen, recompute the map totals from actual row sums — do not restate a total without re-adding it (the Module 3 arithmetic lesson).

**Per-module budgets (Option A sizing):**

| Module | Problems | Budget (hrs) | Rationale |
|---|---|---|---|
| 0 | 0–1 | 0–1 | No-code module by design; at most one written algorithm-description exercise |
| 1 | 4–5 | 3–4 | Small, foundational; LCG + inversion + A-R + chain-tracing |
| 2 | 5–6 | 4–5 | Heaviest implementation load below the MCMC arc |
| 3 | 5–6 | 4–5 | CI methods hierarchy + failure modes |
| 4 | 4–5 | 3–4 | Newton/quasi-Newton + EM; metaheuristics demonstration-level only |
| 5 | 3–4 | 2–3 | Modeling exercises, no sampling (see Section 6) |
| 6 | 3–4 | 2–3 | Empirical chain observation + theory verification |
| 7 | 5–6 | 5–6 | The program's implementation summit |
| 8 | 4–5 | 3–4 | Diagnostics applied to Module 7's own chains |
| 9 | 4–5 | 3–4 | KDE + bandwidth + RB + NN, run on Module 7/8 output |
| 10 | 0 | 0 | Practice is the applied cases (Wave 4) |
| **Total** | **37–47** | **~29–39** | |

---

## 6. Per-Module Requirements

These are binding design requirements per module, not problem drafts. Each item names the goal(s) it serves.

**Module 0.** No code (program guide commitment: "You will not write complex code here"). At most one Type C written exercise: describe a familiar estimator as an algorithm — inputs, process, outputs, and the four computational questions applied to it (Goals 1–3). Optional; zero-to-one hour. Because of the no-code commitment and the at-most-one-Type-C limit above, R6's diagnosis-problem requirement does not bind Module 0; the absence of a Type D problem here is by design, not an omission.

**Module 1.** Must include: implement an LCG and subject it to at least two empirical uniformity tests (Goals 1–2); implement inverse transform for a distribution with tractable CDF *and* one requiring numerical inversion (Goal 3); implement acceptance-rejection with at least two proposals and measure acceptance rates against the theoretical bound (Goal 4); a Type C chain-tracing problem producing the full generative chain narrative in code (Goal 5); a Type D problem exhibiting a correlation artifact or reproducibility failure from a bad generator or seed misuse (Goal 6).

**Module 2.** Must include: plain MC estimator on a known integral with an n^(−1/2) log-log verification (Goals 1–2, R1.2); antithetic and control variates with measured variance reduction and an explanation of the structural condition each exploited (Goal 3); importance sampling on a known target, including a Type D configuration where the proposal's tails are too light and the weight degeneracy is diagnosed empirically (Goal 4); a comparative Type V problem running ≥3 variance-reduction techniques on one problem, comparing variance at fixed budget (Goal 5). **Constraint from the goals file:** stratified sampling carries no standalone implementation requirement — it may appear only conceptually or as an optional-depth problem. A Type C problem may end with resampling from importance weights as a forward hook to SIR (Goal 6), clearly labeled as a preview.

**Module 3.** Must include: nonparametric and parametric bootstrap implementations (Goal 2); all three CI methods — bootstrap-t, percentile, BCa — on one estimation problem, with a repeated-simulation coverage experiment that makes the accuracy hierarchy *visible* rather than asserted (Goals 2–3, R1.2); a Type D heavy-tail failure problem (bootstrap distribution of the mean under a distribution with infinite variance) (Goal 4); a moving blocks bootstrap problem on serially dependent data, comparing naive vs. blocked interval widths (Goal 5); a Type C problem instrumenting the bootstrap as an algorithm per Goal 6. **Resolved:** Goal 4's clustered-data language is now supported by D&H Sec 3.8 (diagnostic source only). Per the Option A scope decision, no clustered-data implementation problem is required or expected for Module 3 — clustering is exercised at the conceptual/diagnostic level only, alongside the existing heavy-tail Type D problem. A clustered-data coding exercise remains explicitly out of scope pending any future revisit of the Goal 5 boundary.

**Module 4.** Must include: formulate two estimators as optimization problems (Goal 1); implement Newton's method and one quasi-Newton method (BFGS acceptable via its update formula) on a likelihood surface, including a step-size/stability failure case (Goal 2, Type D); implement EM for a two-component Gaussian mixture, verify monotone likelihood increase numerically, and exhibit convergence to a local optimum under a bad initialization (Goals 3–4 — the monotonicity check is the natural R1 mechanism, and the local-optimum run is the Type D problem). **Constraint from the goals file:** Goal 5 says metaheuristics are understood "without requiring deep implementation" — the metaheuristic problem is capped at running/lightly-modifying a provided-in-pseudocode simulated annealing loop on a multimodal objective, or is optional depth. No genetic algorithm implementation requirement.

**Module 5.** No sampling — this module's separation of modeling from computation is a program-level design commitment, and the problem set must respect it. Problems are model-construction exercises: specify a full joint distribution for a described scenario and state what each component commits you to (Goal 1); a prior-sensitivity study conducted *analytically or via prior predictive simulation only* (Goals 2, 4 — prior predictive draws use Module 1–2 machinery, not posterior samplers); write the hierarchical structure of a described multi-level problem and state its computational implications (Goal 3). Verification mechanism: these problems are the one place where R1 is satisfied by *structured self-audit* — each problem ships with an explicit checklist of properties the specified model must satisfy, against which the student audits their own specification. This is the weakest verification mode in the program; flag it as such rather than pretending otherwise.

**Module 6.** Must include: simulate a small discrete-state chain, empirically estimate its stationary distribution, and verify against the analytical solution of πP = π (Goals 1–2 — direct R1.1); verify detailed balance numerically for a reversible chain and exhibit its failure for a non-reversible one (Goal 3); a Type V mixing study on a two-state or random-walk chain where a single parameter controls the spectral gap, showing empirical mixing time responding to it (Goals 4–5). This module's problems are deliberately small: their function is to make Module 6's theory *observed* before Module 7 builds on it, honoring Goal 1's "empirical phenomena before formalizing" framing.

**Module 7.** The implementation summit. Must include: SIR built directly on the student's own Module 2 importance sampler (Goal 1, Type C — this is the arc's explicit bridge and must literally reuse prior code); Metropolis-Hastings from scratch on a target with known truth, with a proposal-scale study measuring acceptance rate vs. autocorrelation across ≥3 scales (Goals 2–3); Gibbs sampler on a conjugate two-parameter model verified against direct sampling or analytic marginals (Goal 4, R1.3); Metropolis-within-Gibbs on a model with one non-conjugate conditional (Goal 6); a Type D problem: a target (e.g., well-separated bimodal) on which a poorly tuned sampler visibly fails to mix, with the failure documented from the output (feeds Module 8). Goal 5's random-scan vs. deterministic-scan distinction may be exercised as a short empirical comparison or left to the conceptual questions — drafter's choice, recorded in the alignment matrix. **Forward requirement:** at least one chain produced here must be saved and specified precisely enough to be reused in Modules 8 and 9.

**Module 8.** Diagnostics must be applied to the student's *own* Module 7 output, including the deliberately failed chain — not to textbook trace plots. Must include: compute ACF and ESS from scratch from a stored chain, cross-checked against a library implementation (Goals 1–2, R1.4); run multiple dispersed-start chains and compute R-hat, on both the healthy and the failing sampler (Goal 3); a warm-up sensitivity problem (estimates with and without discarding warm-up on a badly initialized chain) (Goal 4); a thinning experiment demonstrating ESS loss from discarding draws at fixed post-thinning sample count (Goal 5); a capstone Type D/workflow problem: given the failing Module 7 chain, execute the full diagnose → adjust → rerun → re-evaluate loop and document the decision at each step (Goal 6).

**Module 9.** Must include: KDE from scratch (histogram + at least one smooth kernel), with the bias-variance tradeoff exhibited across a bandwidth sweep on data from a known density (Goals 1–2, R1.1); at least one principled bandwidth selector implemented and compared against the sweep (Goal 3); a Rao-Blackwellized density estimate computed from the Module 7 Gibbs output, variance-compared against the plain KDE of the same marginal (Goal 4, Type C — this is where the saved chain pays off); nearest-neighbor estimator implemented and contrasted with KDE on the same data, including tail behavior (Goal 5); a Type D interpretation problem where two defensible bandwidth choices yield qualitatively different pictures of the same data (Goal 6).

**Module 10.** No problem set. All Module 10 practice is the applied cases build (Wave 4). The one binding interface requirement: Wave 4 cases may assume every skill the problem sets certify, and nothing more.

---

## 7. Deliverables, Conventions, and Evaluation Protocol

**Canonical file:** a single versioned document, `ProblemSets1_0.md`, structured per module in the same order and header style as the reading guides. Solutions guidance lives in the same file, per problem, under a clearly marked fold (see below) — a separate solutions file doubles the synchronization surface and invites drift.

**Numbering:** per-module local numbering with a module prefix — `PS1.1, PS1.2, …, PS7.5`. **Do not use a global sequence.** The conceptual-question global numbering has already produced one renumbering cascade (Q49–Q51) and a collision-avoidance flag; the problem sets will be revised more often than the questions and must be insertion-safe by construction.

**Required anatomy of every problem:**
1. ID, type (I/V/D/C), estimated time, core/optional designation
2. Goal reference(s) (`Module_Goals_Reference.md` numbering)
3. Prerequisite pointer if the problem reuses prior code (e.g., "requires your PS2.4 importance sampler")
4. Problem statement (prose + math; pseudocode only where scaffolding is essential)
5. Explicit deliverable ("what to produce")
6. **Verification section:** the R1 mechanism, stated concretely enough that the student can execute it ("your estimate of I should be within 3 standard errors of 0.6827"; "your ESS should agree with the library value to within X%"), tagged with its **provenance tier (4.1)** and, per tier: the cited fact and source (tier 1/2) or a pointer to its validation-log entry (tier 3)
7. *Discussion note* (folded/afterward): what a correct solution should have revealed, common failure modes, and interpretation guidance. Not full solution code — the verification section, not a code listing, is the correctness instrument.

**Validation log (required deliverable, added v1.1):** a companion record, one entry per tier-3 problem (Section 4.1), showing the reference implementation actually run, the seed used, the resulting value, and the date/environment it was run in. This is the artifact that discharges R1a.2 — a tier-3 verification claim without a corresponding log entry is non-compliant. The log is instructor-facing, not student-facing, and is versioned alongside the problem set file.

**Per-module alignment matrix (required drafting deliverable):** a table mapping each goal to the problem(s) exercising it, with any deliberately unexercised goal justified (e.g., Module 4 Goal 5's no-deep-implementation constraint). This is the primary artifact the evaluation pass checks.

**Evaluation protocol for drafted sets** (mirrors the readings protocol): read canonical reference files → draft against this specification, tagging each problem's provenance tier at draft time → check the alignment matrix goal-by-goal → verify every problem carries a compliant R1a basis (citation for tier 1/2, logged execution for tier 3) → verify scope (no unassigned-reading dependencies; no Wave 4 leakage, per 4.4) → sum estimated times against the Section 5 budget → flag issues with severity → minimal-change fixes. No verification target is accepted on the drafter's unlogged say-so, tier 1/2/3 status notwithstanding.

**Build order:** draft the spine first — Modules 2 → 7 → 8 — because the cross-module code-reuse requirements (PS reuse of the importance sampler; Module 8/9 reuse of Module 7 chains) originate there and constrain everything else. Then 1, 3, 6, 9, then 4, 5, then the optional Module 0 exercise.

---

## 8. Open Flags for the Project Owner

1. **Hour accounting (Section 5):** Option A (add explicit problem-set hours; requires ceiling decision) vs. Option B (fit inside current estimates). Recommendation: Option A with core/optional split. Blocks the module-map update, not the drafting itself.
2. **Resolved (Phase 5A/Wave C, 07/23/2026):** Module 3's clustered-data thread is closed — see §6's Module 3 paragraph (D&H Sec 3.8 assigned as diagnostic source; no clustered-data implementation problem required or expected).
3. **Module 5 verification weakness:** structured self-audit is the best available R1 mechanism for pure modeling problems, but it is materially weaker than the rest of the program's mechanisms. Accept, or strengthen by adding prior-predictive-simulation checks to more of the Module 5 problems.
4. **Downstream document updates on adoption:** the orientation note's "Note on Engagement" section and the reading guides' self-assessment framing both describe a two-instrument model (checklist + conceptual questions) and will need a sentence acknowledging the problem sets; the module map needs the hours column per flag 1. Version bumps: orientation note → 1.4, reading guides → 1.5 (if touched), plus the new `ProblemSets1_0.md`.
5. **Resolved (Phase 5A/Wave C, 07/23/2026):** the tier-1/2/3 provenance scheme (Section 4.1) stands as the sourcing policy of record. Robert & Casella's *Introducing Monte Carlo Methods with R* (2010) now has a bibliography entry (`Bibliography1_4.md` Section III, problem-provenance role, not assigned reading).

---

**Phase 3 correction-pass edit (07/19/2026, adopted per E-M0-1 / DP-13, CP-1, resumed session — text supplied by `M5M0_DrafterCorrectionsMemo_1_1.md` §3.2):** §4.1 gained one sentence, placed immediately after the tier-membership sentence, establishing `self-audit` as a legal tier value (in place of 1/2/3) for problems whose R1 mechanism is structured self-audit only, with no numeric verification target, and exempting them from R1a's citation/execution-provenance requirements. Closes the gap that let PS0.1's and PS5.2's `(self-audit)` parenthetical tier annotations read as non-compliant against §4.1 as originally written — the ruling's "annotation clause folded in" note refers to this single sentence covering both the carve-out and the annotation-legitimacy question, per the drafter's own framing of it as one ready-made fix. No other §4.1 language changed.

**Phase 3 correction-pass edit (07/19/2026, adopted per E-M0-3 / DP-14, CP-1):** §6's Module 0 paragraph gained one sentence carving out R6's diagnosis-problem requirement for Module 0. R6 (line 47, §2) is unconditional as written, but Module 0's no-code commitment and its own at-most-one-Type-C limit make a Type D diagnosis problem impossible to produce here — a spec-internal conflict, not a drafting error. The added sentence makes the carve-out authoritative at its root so a mechanical per-module R6 check does not re-flag Module 0 in every future pass. The draft-side companion (`ProblemSet_M0_draft_0_1.md` Flags text) executes at CP-5.

**Phase 5A/Wave C edit (07/23/2026, per `WaveC_EditsInventory_1_0.md` [v1.1] §3, ratified `PSDEP-F2Resolution.md` and `ClusteredDataLooseThread-Corrections.md` §4):** §5's core-sizing text replaced the superseded "~60–70% of the budget" clause with the F2 ratified reading (core ≈ full §5 budget; optional uncounted, above the line). §6's Module 3 paragraph replaced the standing clustered-data flag with a resolution paragraph (D&H Sec 3.8 now the diagnostic source; no implementation problem required). §8 flags 2 and 5 closed in place as one-line resolution notes — items renumbered nowhere; flags 1, 3, 4 keep their original numbers unchanged (flag 4 is cited by number in `Phase5_SessionMap_and_Preconditions_1_1.md` §3.3). No internal version bump to this file (not required by the spec's completion criteria for this pass). Full loci and diffs: `Phase5A_WaveC_ExecutionReport.md`.

*End of specification.*
