# Harvest Index Evaluation Findings
## Computational Statistics Program — Problem Set Build (Wave 3)

*Version 1.3 (closure, 07/23/2026, Phase 5A/Wave C). Filename unchanged per Phase 5 naming policy (`Phase5_SessionMap_and_Preconditions_1_1.md` §3.3) — version tracked here, not in the filename. Batch 1 evaluated the 12 harvest index files for Modules 1, 2, 7, 8; Batch 2 (added in 1.1) evaluated the Module 3 and 4 files; Batch 3 (added in 1.2) evaluates the Module 5 and 6 files (`harvest_index_vehtari_a1-3_module5.md`, `harvest_index_mcelreath_module5.md`, `harvest_index_bda3_ch1-3_5_module5.md`, `harvest_index_mit1844_module6.md`). All batches evaluated against `ProblemSetRequirements1_1.md` (R1–R7, Sections 4, 6, 7), `Tier1_SourceSurvey_1_0.md`, and `Module_Goals_Reference.md`, with claims spot-checked against `Bibliography1_4.md` and `ModuleReadingGuides1_4.md`. Corrections were subsequently applied across Waves A, B, and C — see the closure addendum appended at the end of this document for the full discharge record. This document's finding text is otherwise unedited: findings are recorded here as originally evaluated, not re-litigated.*

**Overall verdict (all batches):** The harvest files are spec-compliant in structure and provenance-tier discipline, with no severe issues. Five moderate findings and seventeen minor findings across 18 files, almost all fixable with targeted, minimal-change edits. One finding (M4) requires a supplementary harvest pass — R&C Ch 5's even-numbered exercises — before Module 4 drafting; nothing else blocks proceeding.

---

## What's Confirmed Sound

**Format and sourcing discipline (Section 4.2).** All 12 files use paraphrase-only entries, carry solved/unsolved status against the arXiv:1001.2906 odd-numbered pairing, and flag truncated or ambiguous extractions for re-verification rather than papering over them (Ch 6's 6.10–6.12, Ch 8's 8.18, both BDA3 Ch 10–11 pointers).

**Provenance-tier discipline (Section 4.1 / R1a).** This is the strongest aspect of the set:
- The Vehtari A5→Module 7 file correctly separates the citable bugs (tier-1-adjacent — existence and location sourced) from the unpublished corrected behavior (tier 3 — requires drafter execution and a validation-log entry).
- The Vehtari A5→Module 8 file correctly splits the published known-bad R-hat/ESS values (tier 1, citable) from the post-fix values (tier 3), and explicitly notes a single problem may legitimately mix tiers across its parts — exactly per R1a.
- Both Betancourt files correctly self-classify as tier-3-only conceptual material, since neither source publishes a numeric verification target.
- The A5→M8 file's caution against citing exact seed-4911 decimals as guaranteed-reproducible, pending drafter re-verification, is squarely in R1a's spirit.

**Scope discipline.** The Bayes-factor / marginal-likelihood / path-sampling cluster (Ch 3's 3.8/3.15/3.19; Ch 4's 4.1/4.2/4.13/4.14; Ch 7's 7.16; Ch 8's 8.3/8.15) is consistently flagged out-of-core-scope across all four chapters, with a sensible recommendation to resolve it once at the program level rather than per file. The Betancourt Workflow file's analysis of the scope mismatch between the source's 12-step apparatus and Module 8's narrow single-chain diagnostic scope is exemplary — it isolates the one usable element (Step Ten) and correctly redirects the rest to Modules 5/10.

**Verified bibliography claims.** I checked the A5→M8 file's assertion directly against `Bibliography1_4.md`: the Module 8 section does list Geyer (1992), Flegal et al. (2008), Cowles & Carlin (1996), and Link & Eaton (2012) (Roberts & Rosenthal (2001) is present but role-tagged to Module 7, not 8). Vehtari, Gelman, Simpson, Carpenter & Bürkner (2021) — the rank-normalized R-hat paper behind A5.11/A5.12 — is confirmed absent, as the harvest file states. Note this is a distinct paper from the already-assigned Gelman & Vehtari (2021) retrospective (Module 10, Goal 6); the harvest file keeps the two distinct, correctly, and any bibliography update should preserve that distinction.

---

## Open Findings — Moderate Severity

### Finding M1 — Mis-tagged "Goal 5" references in the Module 7 files (R2 traceability risk)

**Status: Open.**

Module 7 Goal 5 is specifically the random-scan vs. deterministic-scan Gibbs distinction (`Module_Goals_Reference.md`, M7 Goal 5). However:
- Ch 6's exercise 6.14 is tagged "Goals 3, 5."
- Ch 7's exercises 7.13 and 7.14 are tagged "Goals 4, 5," and 7.24 is tagged "Goal 5" alone.

All four of these concern mixing speed / autocorrelation as a function of correlation structure or reparameterization — none concerns scan order. The intended referent appears to be Module 6 Goals 4–5 (mixing time, spectral gap, consequences of poor mixing), reused here as cross-module reinforcement. Left as-is, an alignment matrix built directly from these tags would falsely register M7 Goal 5 as exercised, when in fact no harvested source addresses scan order at all.

**Recommended fix:** Retag 6.14, 7.13, 7.14, and 7.24 as "Goal 3 (mixing; cross-ref M6 Goals 4–5)" or equivalent, removing the bare "5." Add an explicit note to both chapter summaries that M7 Goal 5 (scan-order distinction) has no harvested candidate anywhere in this pass — consistent with the spec's own allowance to treat Goal 5 as an optional short empirical comparison or leave it to the conceptual questions (Section 6, Module 7 paragraph), but this disposition should be recorded, not left implicit.

### Finding M2 — Module 2 Goal 5's required comparative problem is not accounted for anywhere

**Status: Open.**

Section 6 requires, for Module 2: "a comparative Type V problem running ≥3 variance-reduction *techniques* on one problem, comparing variance at fixed budget" (Goal 5). Nothing in the Ch 3 or Ch 4 harvest satisfies this:
- Ch 3's 3.13 compares three *proposal choices within* importance sampling — one technique, three instances — not three techniques.
- Ch 4's 4.18 compares antithetic variates across five targets and four statistics — one technique studied broadly, not multiple techniques compared against each other.

The Vehtari A4 file's summary states Module 2 "Goals 3 and 5 remain dependent on the R&C Ch 3–4 harvest and/or original drafting, as already reflected there." This is accurate for Goal 3 (covered by 4.11/4.12/4.18) but not for Goal 5 — neither chapter's summary actually flags a Goal 5 gap or candidate.

**Recommended fix:** Add an explicit line to the Ch 4 summary noting Goal 5's ≥3-technique comparison has no harvested candidate and will require original (tier-3) drafting, with an executed reference run logged per Section 4.1.3.

### Finding M3 — Rao-Blackwellization scope framing overlooks its status as a named Module 9 goal

**Status: Open.**

Both the Ch 4 and Ch 7 summaries frame Rao-Blackwellization (RB) as unnamed in the program's goal set and recommend a single in-or-out scope decision for whether it belongs to Module 2/7 at all. This is incomplete: RB *is* a named goal — Module 9 Goal 4 ("Explain the Rao-Blackwell estimator... and identify why it is particularly well-suited to MCMC settings") — and Section 6's Module 9 requirements mandate a Rao-Blackwellized density estimate computed from the Module 7 Gibbs output, variance-compared against plain KDE (Goal 4, Type C).

The correct resolution is therefore not binary. RB material can reasonably stay optional-depth for Module 2/7's own goal sets while still being cross-listed as the upstream anchor for Module 9's *required* problem. Ch 7's exercise 7.15 (RB-vs-empirical variance comparison on Gibbs output) is structurally the closest available analogue to what Module 9 Goal 4 needs (RB applied to a Gibbs sampler's output), just applied to a scalar expectation rather than a density. Since Module 9 is the survey's "near zero" harvest-potential module, these RB-cluster exercises (4.9/4.10/4.15/4.16/4.19/4.20/4.21 in Ch 4; 7.15/7.16/7.25 in Ch 7) are among the only tier-1-adjacent anchors Module 9 is likely to get at all — the current framing risks them being discarded during the Module 2/7 scope call before Module 9's harvest pass even happens.

**Recommended fix:** Amend the RB flag in both the Ch 4 and Ch 7 summaries to note the Module 9 Goal 4 consumer explicitly, and recommend the cross-module scope decision be deferred until Module 9's own harvest/drafting pass, rather than resolved solely on Module 2/7 terms.

---

## Open Findings — Minor Severity

**m1 — Module 1's numerical-inversion requirement has no candidate.** Section 6 requires inverse transform for a distribution with a tractable CDF *and* one requiring numerical inversion (Goal 3). All of Ch 2's inverse-transform candidates (2.2, 2.12, 2.13, 2.15) have closed-form CDFs. The Ch 2 summary's "confirmed original-drafting" list names Goals 1–2 and the Goal 5 chain-tracing problem but omits this sub-requirement. *Fix: add to the Ch 2 summary.*

**m2 — Module 2's n^(−1/2) log-log verification has no direct match.** Required by Goals 1–2 (R1.2). Ch 3's 3.1 monitors convergence to a stated precision but does not construct the log-log rate plot itself. A small original wrapper around 3.1 (or an independent construction) is needed. *Fix: one line in the Ch 3 summary.*

**m3 — Ch 6's fit note for 6.14 slightly overstates the source's coverage.** It calls 6.14 "essentially the exact problem the spec requires," but the spec's study is acceptance rate *vs. autocorrelation* across ≥3 scales, while the book's own Example 6.4/6.10 publishes only acceptance rates (0.98/0.80/0.15) — the autocorrelation half is drafter-added and becomes tier 3. *Fix: qualify the claim in the Ch 6 fit note.*

**m4 — Module 8 Goal 4 (warm-up sensitivity) coverage is understated in the Ch 8 file.** 8.12's "Goal 4" tag is weak: a bimodal target with an intentionally small proposal variance demonstrates a mode-finding/mixing failure, not a warm-up/retention problem. The Vehtari A5→M8 file already states plainly that warm-up sensitivity is uncovered by that source; the Ch 8 summary should state the same conclusion explicitly so the net program-wide position (Goal 4 is original tier-3 drafting) isn't obscured by 8.12's loose tag. *Fix: retag or annotate 8.12, and add the explicit gap note to the Ch 8 summary.*

**m5 — The Vehtari A5→M7 bug-hunt problem cannot discharge the from-scratch implementation requirement (R4).** The file gestures at this ("interrogate rather than build") but doesn't state the R4 consequence outright: since the code is given, not built from primitives, the bug-hunt problem cannot itself satisfy Module 7's core "Implement MH from scratch" requirement (Goal 3) and must be paired with a genuine from-scratch build (e.g., drawn from 6.13 or the 6.14/Example 6.4 pairing). *Fix: add an explicit R4 note to the A5→M7 summary so the alignment matrix doesn't miscount the bug-hunt as satisfying the core implementation slot.*

**m6 — Two build-order dependencies are implied but not recorded.** (a) Ch 8's exercises 8.2, 8.4, 8.13, and 8.14 all presuppose that Ch 7's 7.12 (the pump-failure Gibbs sampler) is adopted as a core Module 7 problem; the Ch 8 file notes the *reuse* but not this *adoption dependency*. (b) Module 7 Goal 1 (SIR built on the student's own Module 2 importance sampler) is original-by-construction per the survey's own caveat (a), but no Module 7 harvest file restates this — the only related entry is the low-confidence BDA3-10.4 pointer, which the BDA3 file itself already flags as likely redundant with material already harvested elsewhere. *Fix: add both dependency notes at the point they first arise.*

**m7 — Bibliography bookkeeping is now load-bearing and should be closed out before drafting.** Five of the 12 files rest on Robert & Casella, *Introducing Monte Carlo Methods with R* (2010), which still has no bibliography entry (per open flag 5 in `ProblemSetRequirements1_1.md` Section 8). Vehtari, Gelman, Simpson, Carpenter & Bürkner (2021) needs an entry if A5.11/A5.12 are drafted (see confirmed-absent finding above). The Aalto provenance note should name both source URLs used across the two A5 files (`template5.html` notebook and `assignment5.html` quiz), and the CC-BY-NC reuse terms deserve a one-time recorded confirmation of fit rather than an implicit assumption. *Fix: not a harvest-file edit — a bibliography/orientation-note action item for the next corrections pass.*

---

## Net Coverage Position After This Evaluation

Consistent with the Tier-1 survey's own predictions, with the findings above folded in:

- **Well-anchored (tier 1/tier-1-adjacent available):** Module 2 (MC integration, importance sampling, ESS-from-weights); Module 7 (MH theory and implementation, Gibbs including hierarchical and missing-data variants, the improper-conditionals Type D exhibit); Module 8 (R-hat/ESS on a failing sampler, the classic-vs-improved R-hat blind spot, thinning theory).
- **Confirmed program-wide original-drafting residual** (no harvested candidate in any of the 12 files, and none expected from remaining Section 2–3 sources per the survey):
  - Module 1: Goals 1–2 (PRNG mechanics), Goal 5 (chain-tracing), numerical-inversion half of Goal 3 (Finding m1).
  - Module 2: Goals 1–2 rate-plot construction (Finding m2), Goal 5's ≥3-technique comparison (Finding M2).
  - Module 7: Goal 1 (SIR-on-own-sampler), Goal 5 (scan-order distinction, Finding M1), Goal 6 (Metropolis-within-Gibbs — noted in the Ch 7 file as needing original adaptation of Section 7.6.3's narrative).
  - Module 8: Goal 2 (ACF from scratch), Goal 4 (warm-up sensitivity, Finding m4), Goal 5 (thinning experiment, beyond the theory result in 8.1).

No finding in this document blocks proceeding to either (a) corrections to the 12 existing files, or (b) the harvest pass for the four remaining modules (3, 4, 5, 6) flagged as outstanding in the prior conversation.

---

# Batch 2 — Modules 3 and 4 (added in v1.1)

*Files evaluated: `harvest_index_hesterberg_module3.md` (Hesterberg 2015 → Module 3) and `harvest_index_ch5_module4.md` (R&C IntroMCwR Ch 5 → Module 4). Finding numbering continues the Batch 1 sequence.*

## What's Confirmed Sound — Batch 2

**Hesterberg → Module 3.** High-quality harvest, correctly framed as tier-1-adjacent per the survey's ⚠️ verify-at-harvest flag (narrative source with exact citable numeric targets, not an exercise+solution set).
- **Tier discipline on H-4 is exactly right:** the published coverage thresholds (n≥2383 percentile, n≥101 bootstrap-t, etc.) are citable facts from a peer-reviewed source, while any student-scale reproduction's specific targets are tier 3 requiring drafter execution and a validation-log entry — the file states both halves and correctly warns that small-scale runs won't match the article's variance-reduced large-simulation thresholds.
- **All three gap flags check out against the spec:** no BCa (the spec's required third CI method — remains on Efron & Tibshirani Ch 14, Secs 14.1–14.3); no dependent-data material (explicitly outside the article's stated scope — Goal 5 remains on E&T Sec 8.6); no infinite-variance case (correctly distinguished from the article's skewed-but-finite-variance exponential examples, so the spec's Type D "bootstrap of the mean under infinite variance" problem is rightly marked original construction with no source found).
- **Goal tags verified against `Module_Goals_Reference.md`**, including the non-obvious but apt H-7 → Goal 6 mapping (the bootstrap's own Monte Carlo error as a Module-1-style simulation-budget question — a natural Type C construction).
- **Arithmetic consistency spot-check passes:** H-3's narrowness-bias numbers are internally consistent (4.07 × √(22/23) = 3.98 ≈ the reported bootstrap SE 3.96).
- **The BDA3-for-Module-3 demotion is sound** (no dedicated resampling coverage in a Bayesian text) — recorded below as a survey-record update, so the "tangential" lead is formally closed rather than left dangling.

**Ch 5 → Module 4.** Candidate-level judgment is honest and careful within its coverage (see Finding M4 for the coverage problem itself):
- The off-model caveats on 5.5 (stochastic-gradient, not Newton), 5.11 (multinomial genetics, not Gaussian mixture), 5.15 (exponential mixture; degenerate-collapse rather than bad-init failure), and 5.19 (root-finder, not Newton) are exactly the discipline that prevents false coverage entries in the alignment matrix.
- The 5.21 erratum catch (solutions manual's own admission of duplication with 5.11) is correct handling — excluded with the reason recorded.
- 5.7 → Goal 5 is correctly identified as a near-ready match for the spec's cap ("running/lightly-modifying a provided-in-pseudocode SA loop on a multimodal objective") — provided SA function, established bimodal objective, quantifiable mode-recovery outcome across temperature schedules.
- The "check whether Example 5.2's mixture gets an EM treatment in the main text" action item is the right instinct (extended by Finding M4 to cover the even exercises as well).

## Open Findings — Moderate Severity (Batch 2)

### Finding M4 — Ch 5 harvest silently omits all even-numbered exercises, with an impossible supporting claim

**Status: Open. The only finding in either batch that blocks drafting (Module 4 only).**

The file's header states the chapter comprises "exercises 5.1–5.21" and that "all of 5.1–5.21 are odd, so the entire chapter's exercise set is solved." A consecutive range 5.1–5.21 cannot consist solely of odd numbers; the candidate table contains only odd-numbered exercises, so the evens (5.2–5.20) were evidently never triaged. This deviates from the established convention of every other R&C chapter harvest, where even-numbered (unsolved) exercises were listed with solved-status "No" and tier-2/3 handling — and where the evens supplied several of the program's strongest candidates (2.10 RANDU, 3.4 pathological-weights, 6.14 proposal-scale study, 7.12 pump-failure Gibbs, 8.8, among others).

The consequence is direct and material: the file's pivotal conclusion for Goals 3–4 — that "no exercise here actually *runs* EM on the mixture" — was drawn from odd-only coverage. An even-numbered exercise could be precisely the required EM-on-two-component-Gaussian-mixture candidate, and this cannot be known without looking.

**Recommended fix:** Supplementary harvest pass over Ch 5's even-numbered exercises (5.2–5.20), following the same conventions as the other chapter files (paraphrase-only, solved = No, tier 2/3 disposition), plus correction of the header claim. Complete before Module 4 drafting begins; combine with the file's own existing action item to check the main text's treatment of Example 5.2.

## Open Findings — Minor Severity (Batch 2)

**m8 — Module 3: the parametric bootstrap is unaccounted for.** Section 6 requires "nonparametric *and parametric* bootstrap implementations" (Goal 2). The Hesterberg file mentions the parametric bootstrap neither as a candidate nor in its gaps section. It remains dependent on the assigned Efron & Tibshirani reading (Ch 6) plus original drafting. Same class of omission: the Goal 5 *problem* (naive vs. blocked interval widths on serially dependent data) is original tier-3 drafting — E&T Sec 8.6 is a reading source, not a solved-problem source — and the gaps section's "covered by E&T" phrasing shouldn't be read as problem coverage. *Fix: add both to the file's gap section.*

**m9 — Module 3: the clustered-data prohibition is not carried forward.** Open flag 2 (restated in Section 6's Module 3 paragraph) bars any clustered-data problem until the Goal 4 "clustered data" language is trimmed or given an implementation source, and explicitly instructs that the dependency be recorded in the problem set's instructor notes. The Hesterberg file — the module's primary harvest artifact and the natural carrier of that note into drafting — is silent on it. *Fix: one-line note in the file's gap section referencing open flag 2.*

**m10 — Module 3: H-1's real-data recommendation needs a data-policy (4.3) disposition.** The Verizon CLEC arm (n=23) fits the inline-reproduction rule (≤~50 values), but the ILEC arm (n=1664) would be an external-dataset fragility, in tension with policy 4.3.1's synthetic default and the principle that real-data work is primarily Wave 4's job. *Fix: the fit note should specify one of — CLEC-only inline; a synthetic mirror of the ILEC arm's summary statistics; or deferring the two-arm version to Wave 4's applied cases.*

**m11 — Module 4: only one of the two required Goal 1 formulations has a candidate.** Section 6 requires formulating *two* estimators as optimization problems; the harvest yields one (the mixture MLE surface, 5.1/5.13). The second formulation is original drafting. *Fix: add to the Ch 5 summary's residual accounting.*

**m12 — Module 4: the core Newton and quasi-Newton implementation problems have no harvested candidate — only the failure case is flagged.** Unsurprising for a Monte-Carlo-optimization chapter, but the file's summary flags only the step-size failure-*case* mismatch (5.5/5.19 as inspiration), not that the Goal 2 implementation problems themselves (Newton's method plus one quasi-Newton via the BFGS update on a likelihood surface) are wholly original — with tier-2 anchors available through known-MLE verification targets per R1a.1. Also a small citation-precision slip in the header: the two-component-Gaussian-mixture requirement is attributed to "Module 4's Goal 3–4," but `Module_Goals_Reference.md` does not name the mixture — the requirement lives in `ProblemSetRequirements1_1.md` Section 6. *Fix: add the implementation gap to the residual accounting; correct the attribution.*

## Survey-Record Update (Batch 2)

The Hesterberg file's companion note recommends formally dropping BDA3 as a Module 3 lead (no dedicated bootstrap/resampling coverage; solved-exercise index doesn't touch resampling methodology). This evaluation concurs. The Tier-1 survey's Module 3 row ("Hesterberg (2015); BDA3 solved exercises tangentially") should be annotated accordingly in the next survey revision, so Module 3's source basis is recorded as: Efron & Tibshirani (assigned text, adaptation skeleton), Hesterberg 2015 (verified this pass), original drafting for the residual.

## Net Coverage Position — Modules 3 and 4

**Module 3** lands close to the survey's "low–medium" prediction, but stronger than expected on Goals 2–3: H-4 provides an already-executed, exactly-quantified version of the spec's central coverage-hierarchy experiment (minus BCa), and H-2/H-3 anchor the extreme-statistic failure case and the narrowness-bias derivation. Confirmed original-drafting residual: the BCa implementation (E&T-supported), the parametric bootstrap problem (m8), the infinite-variance Type D case (no source found in any pass), the moving-blocks comparison problem (m8), and the clustered-data item remains *blocked*, not merely unsourced (m9).

**Module 4** cannot be finalized until Finding M4's supplementary pass runs. Provisional position from the odd-only coverage: Goal 5 is effectively anchored (5.7 + Example 5.9's provided SA code); Goal 1 is half-anchored (5.1/5.13, one of two required formulations); Goals 3–4's required Gaussian-mixture EM problem has strong *adjacent* material (5.9's Q-function derivation, 5.11's MCEM contrast, 5.15's degenerate-convergence exhibit, 5.13's data-dependent modality for the bad-initialization story) but no direct implementation candidate *yet identified* — pending the even-exercise pass and the main-text check. Goal 2's implementations are wholly original (m12), with 5.5/5.19 as adaptation inspiration for the required failure case.


---

# Batch 3 — Modules 5 and 6 (added in v1.2)

*Files evaluated: `harvest_index_vehtari_a1-3_module5.md`, `harvest_index_mcelreath_module5.md`, `harvest_index_bda3_ch1-3_5_module5.md` (→ Module 5), `harvest_index_mit1844_module6.md` (→ Module 6). Finding numbering continues the running sequence. Cross-checks in this batch extended to `ModuleReadingGuides1_4.md` (Module 6 reading scope) and `Bibliography1_4.md` (LPW edition).*

## What's Confirmed Sound — Batch 3

**MIT 18.445 → Module 6.** The most methodologically disciplined file of the full 18-file set:
- **The proactive LPW edition-mismatch check is exemplary** — performed explicitly because of the Lange 1st/2nd-edition lesson, with the verification method recorded (AMS first-edition TOC vs. second-edition endmatter) and the residual risk (within-chapter exercise numbering unverified across editions) honestly left open rather than assumed away. See m16 for the one premise error the check itself didn't catch.
- **Scope discipline is aggressive and correct:** LPW Chs 2, 5, 6, 7, 9, 10, 21 excluded as outside Module 6's assigned reading regardless of individual quality, with 5.1 (coupling-based convergence proof) and 7.2 (flow identity) preserved as clearly labeled optional-depth. The assigned-scope claim (Ch 1 Secs 1.1/1.3/1.5/1.6, Ch 3, Ch 4, Ch 12) verified against `ModuleReadingGuides1_4.md` and the bibliography's LPW role note — accurate.
- The 4.3+4.4 core pairing (TV contraction + monotone distance-to-stationarity) with a tier-3 empirical coda matches the survey's anticipated pattern for this source, and the demotion of 1.11 (analytic existence proof) relative to the spec's simulate-and-verify R1.1 framing is correct.
- The Ch 3 and Ch 12 absences are correctly labeled "real gap, not verification-pending," with the n-cycle spectral-gap simulation (conceptual question 33's own example) identified as the original-construction route.

**McElreath → Module 5.** Exemplary verification honesty per R1a: verified-via-secondary-quotation status declared up front; SR-monks explicitly marked do-not-draft pending primary verification; "tier-3 at best" conclusion stated plainly. The `ulam`/Stan tension with Module 5's no-sampling commitment is caught, with two viable adaptation routes — and the specification-only route ("write out the model... without requiring the student to actually fit it") matches the spec's Goal 3 problem type nearly verbatim ("write the hierarchical structure of a described multi-level problem and state its computational implications").

**BDA3 Chs 1–3, 5 → Module 5.** Correctly self-classifies as a scoping map, not a finished harvest (the Ch 10–11 precedent applied consistently); re-flags the recommended-≠-solved trap with a concrete instance (Ch 5: Aalto recommends 5.1–5.2, solutions manual solves 3–12); flags the per-exercise MCMC-compatibility check needed before any Ch 3/5 exercise is treated as Module-5-compatible; and its follow-up priority ordering (Ch 5 → Ch 2 → deprioritize Ch 3 as likely redundant with Vehtari A3) is gap-driven and sound.

**Vehtari A1–A3 → Module 5.** The no-sampling constraint is restated up front and checked item-by-item — every candidate uses closed-form quantiles or direct draws from closed-form marginals, never an MCMC step. A1 is correctly demoted to prerequisite-check material. A2's prior-sensitivity exercise is a near-verbatim realization of the spec's core Goal 2 requirement, with adaptable starter code — correctly identified as the standout. Cross-file gap coordination across the three Module 5 files is coherent: Vehtari flags the hierarchical gap → the McElreath file exists specifically to fill it → the BDA3 file identifies a likely better (tier-1, no-sampler) closure and prioritizes it.

## Open Findings — Moderate Severity (Batch 3)

### Finding M5 — Vehtari A1–A3 file's blanket tier-1 claim overstates (R1a provenance risk)

**Status: Open.**

The file's summary states: "all items are tier-1 (machine-checked target values from the source itself), except A3-two-means." Three of the seven candidates do not meet that bar, per the file's own table:
- **A1-roulette:** "No fixed numeric target (visual/simulation task)."
- **A2-prior-sensitivity:** "No fixed numeric target (open-ended written comparison)" — and this is the file's own standout core candidate.
- **A2-posterior:** machine-check *mechanism* confirmed, but "specific numeric outputs weren't captured in this extraction pass" — the mechanism's existence is tier-1-adjacent; the targets are not yet in hand.

Under R1a, a blanket tier-1 label carried into the alignment matrix would corrupt exactly the provenance record the tier system exists to protect — the same failure class as Batch 1's Finding M1 (false coverage via loose labeling). The items themselves remain excellent candidates; only the classification is wrong.

**Recommended fix:** Replace the blanket tier line with per-item status: tier 1 = A3-normal-joint, A3-odds-ratio, A2-historical (captured numeric targets); tier-1-adjacent pending target capture = A2-posterior; no numeric target by design = A1-roulette, A2-prior-sensitivity (verified via Module 5's self-audit mechanism instead — see m14); verification-pending = A3-two-means (as already stated).

## Open Findings — Minor Severity (Batch 3)

**m13 — A2-prior-sensitivity is under-tagged.** Tagged Goal 2 only; the spec pairs the prior-sensitivity study with Goals 2 *and* 4, and Goal 4 names prior sensitivity verbatim in `Module_Goals_Reference.md`. *Fix: retag "2, 4."*

**m14 — Module 5's prescribed verification mechanism is unmentioned in all three M5 files, and two goal facets are unaccounted.** Section 6 prescribes that Module 5 problems satisfy R1 by *structured self-audit* — each problem ships with an explicit checklist of properties the specified model must satisfy — and instructs that this be flagged as the program's weakest verification mode. None of the three files mentions this; their summaries emphasize machine-checked numeric targets, which risks drafting defaulting to numeric-target-only verification and omitting the required checklists. Additionally, no candidate in any file serves Goal 4's likelihood-misspecification or predictive-adequacy facets, or Goal 5 (modeling-layer vs. computational-layer separation) — most plausibly conceptual-question and checklist-design territory, but the disposition should be recorded, not implied. *Fix: add a shared drafting note (natural home: the Vehtari file's summary, as the module's primary harvest artifact) covering the self-audit mechanism and the Goal 4/5 residual disposition.*

**m15 — Module 6: the spec's detailed-balance problem is missing from the gaps list.** The MIT file's "real, unresolved gaps" names only Ch 3 (Goal 1) and Ch 12 (Goal 4). But the spec's second required problem — verify detailed balance numerically for a reversible chain and exhibit its failure for a non-reversible one (Goal 3) — also has no harvested candidate: MIT's Ch 1 items (1.2, 1.11) don't touch Sec 1.6's reversibility material, and no file item is tagged Goal 3. Likewise the spec's first required problem (simulate a small chain, estimate the stationary distribution, verify against πP = π) is original drafting, though self-verifying by construction under R1.1, so the tier-3 burden is nominal. *Fix: add both to the file's gap accounting; net effect is that all three of Module 6's spec-required problems are original constructions, with the harvest supplying the theory anchors (1.2, 4.3, 4.4) rather than the problems themselves — consistent with the module's "deliberately small" design.*

**m16 — Module 6: edition-premise misstatement in the (otherwise exemplary) LPW edition check.** The file states the program's bibliography "assigns the second edition (2017) as the primary Module 6 text." Verified against `Bibliography1_4.md`: the entry is **Levin, Peres & Wilmer (2009)**, American Mathematical Society, with a parenthetical "(2nd ed. freely available online.)" — i.e., the canonical citation is the first edition, with second-edition *access*. The file's load-bearing conclusion survives (the assigned Chs 1/3/4/12 keep identical numbers and titles across editions, under either account of where the new chapters sit), but the premise should be corrected — and the latent ambiguity the check exposed (cite 2009, read 2017 online) should be pinned once at program level for within-chapter section/exercise numbering, which is precisely the residual the file itself flagged as unverified. *Fix: correct the file's premise sentence; add a one-time edition-pinning decision to the corrections queue (suggested resolution: retain the 2009 citation, record that section/exercise-level references are to be spot-verified against the freely available 2nd edition before citing to a student).*

**m17 — Provenance-ledger extensions (continues Batch 1's m7).** Add to the same bookkeeping action: Aalto assignment templates 1–3 URLs (`template{1,2,3}.html`, CC-BY-NC — joining the A4/A5 URLs already flagged); the McElreath course-repo license note plus the eventual verified week-PDF URLs once the reedfrogs prompt is confirmed against the primary source; and the BDA3 official solutions URL (`sites.stat.columbia.edu/gelman/book/solutions3.pdf`) as an access note if solved exercises are drafted from it. *Fix: fold into the existing m7 action item.*

## Consolidated Action — the Module 5 Hierarchical Gap

The three M5 files collectively imply, but do not jointly record, a single resolution order for the module's one substantive coverage gap (Goal 3's hierarchical half). Recording it here as one decision:
1. **First:** BDA3 Ch 5 solved-exercise retrieval pass (exercises 3–12 per the solutions-manual list) — highest tier-1 potential, most likely no-sampler-compatible, per the BDA3 file's own priority ranking. Per-exercise MCMC-compatibility check required.
2. **Complement or fallback:** the reedfrogs varying-intercepts structure as a specification-only Goal 3 exercise (McElreath file's primary recommendation), tier 3, pending primary-source verification of the prompt.
3. **Blocked:** SR-monks — do not draft until the actual homework prompt and author solutions are fetched (the McElreath file's own instruction).

## Net Coverage Position — Modules 5 and 6

**Module 5** is the best-anchored of the low-harvest modules, exceeding the survey's "medium-rich" expectation on Goals 1–2: A2 (Beta-Binomial posterior + the prior-sensitivity study) and A3 (joint Normal posterior, odds-ratio comparison) provide real-data, machine-checked or checkable, no-sampler candidates for Goals 1, 2, and the multiparameter half of Goal 3. Residual: the hierarchical half of Goal 3 (resolution order above); Goal 4 beyond prior sensitivity and Goal 5 (conceptual-question/checklist territory, m14); and the self-audit checklist design itself, which is original drafting work for every problem in the module (m14).

**Module 6** matches the survey's expectation precisely: strong tier-1 *theory* anchors squarely inside the assigned reading (1.2 for irreducibility, 4.3+4.4 for the results that make mixing time well-defined), while all three spec-required *problems* are original tier-3 constructions (simulate-and-verify πP = π — self-verifying; the detailed-balance verification pair, m15; the spectral-gap-parameter mixing study, file-flagged, with conceptual question 33's n-cycle as the natural base). Given the module's "deliberately small" design mandate, this original-drafting burden is low despite the thin problem-level harvest.


*End of findings.*

---

## Closure Addendum — v1.3 (07/23/2026)

*Appended per `ProblemSetDrafting_ExecutionPlan_1_0.md` Phase 5 item 4 and `HarvestCorrections_ExecutionPlan_1_1.md`'s own recommendation ("issue alongside Wave C, since C1/C2 are the last open items"). This is a closure record, not a re-evaluation — no finding above is re-opened, re-litigated, or re-audited.*

This document's full scope — **5 moderate findings (M1–M5), 17 minor findings (m1–m17), one survey-record item (C2), and one consolidated resolution order** (the Module 5 hierarchical gap) — is now fully discharged. Execution record: `HarvestCorrections_ExecutionPlan_1_1.md` (Decision Gates §0; Wave A §A1–A12; Wave B §B1–B3; Wave C §C1–C2).

- **M1–M5, m1–m6, m8–m16:** resolved in Wave A (12 files, 23 edits) and Wave B (B1 Ch 5 even-exercise pass, closing Finding M4's drafting block; B2 BDA3 Ch 5 solved-exercise verification; B3 McElreath primary-source verification) — all verified against re-uploaded canonical harvest files per the plan's own Verification Protocol. m9 resolved in Wave A (A9, `harvest_index_hesterberg_module3.md`).
- **m7 / m17 (bibliography and provenance-ledger closeout, C1):** resolved this pass (Phase 5A/Wave C) — `Bibliography1_4.md` Section III (new entries: Robert & Casella *Introducing Monte Carlo Methods with R*, 2010; Vehtari, Gelman, Simpson, Carpenter & Bürkner, 2021) and new Section XI "Provenance & Access Notes" (Aalto template/quiz-page ledger; McElreath course-repo license note; BDA3 official-solutions-PDF access note). Per-item loci and diffs: `Phase5A_WaveC_ExecutionReport.md`.
- **DG-2's outstanding C1 ledger entry (LPW edition-pinning, referenced in m16):** closed on inspection — the existing `Bibliography1_4.md` LPW entry already cites Levin, Peres & Wilmer (2009) with the 2nd-edition access note parenthetically; no bibliography edit was required (`WaveC_EditsInventory_1_0.md` item 1.4).
- **C2 (Tier1_SourceSurvey annotation):** dropped by owner ruling (07/13/2026) — `Tier1_SourceSurvey_1_0.md` has run its course and is out of scope for this and all subsequent passes; not executed, by design, not an oversight.

No further action is required against this document.
