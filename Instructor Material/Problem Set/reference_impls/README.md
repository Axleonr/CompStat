# `reference_impls/` — Instructor-Facing Reference Implementation Archive

*Companion to `ProblemSets.md` v1.0 and `ValidationLog.md` v1.0 (Phase 5B assembly, 07/23/2026). **Instructor-facing, not student-facing** — do not distribute to students; these are the drafter/evaluator reference solutions that back the tier-3 verification targets in the problem set. 52 files total.*

## How to run

Import paths inside this package are **package-relative**: files reference each other as `from reference_impls.<module> import ...`. This means the package must be run **from its parent directory** — i.e., this folder must be named `reference_impls/` and sit in your working directory (or on your `PYTHONPATH`) as-is, and individual scripts should be invoked as modules, e.g.:

```
cd <parent-of-reference_impls>
python3 -m reference_impls.ps8_1_ref
```

Running a file directly (`python3 reference_impls/ps8_1_ref.py`) will fail on the cross-module imports (`ps8_1_ref`, `ps8_2_ref`, `ps8_3_ref`, `ps8_5_ref`, `ps9_2_ref`, `ps9_4_ref` all import siblings this way). This relative-import structure was introduced at CP-7 (DP-19) to fix a Phase-3 finding (E-M8-1) where the original M8 scripts imported shared helpers via a hard-coded `/home/claude/work/` path and did not execute as delivered. `__init__.py` (empty) marks the directory as the package.

**No compute was performed during this assembly session.** Every changed reference was re-executed bit-for-bit at CP-V (Phase 3 closing verification) or confirmed against the log at Phase 4 launch; this archive assembles and verifies file *presence, structure, and static content* only (import resolution checked; all 52 files confirmed syntactically valid via `py_compile`; no scripts executed here). Two files were independently executed once during Phase 5B input verification, before this session began, specifically to confirm the addendum corrections below reproduce their certified values — see `Phase5B_AssemblyReport.md`.

## The two Phase-4 addendum corrections (verified, not assumed)

- **`ps4_1_ref.py`** — contains the Dataset A′ block (CP-6, DP-8; seed `20260720`), appended after the original Dataset A/B/median code. Confirmed present (`SEED_APRIME = 20260720` at line 114) and confirmed to reproduce the certified values (A′ split n1=130/n2=270; maxima at (−0.15,3.95)/−801.21 and (4.10,0.20)/−932.23; resolution-stable across grids 121/181/241/301).
- **`ps6_4_ref.py`** — carries the corrected line-51 comment (E-M6-5): the false "should be exactly 1.0" claim is replaced with the correct fact (`d(0) = 1 − min_i π*_i = 1 − 0.1875 = 0.8125`). Comment-only change; run values unaffected and confirmed unchanged (d(0)=0.8125, d(20)≈1.40e-6, periodic chain flat at 0.5).

## File → Problem ID mapping

Naming convention: `ps{module}_{problem}_ref.py` → `PS{module}.{problem}`. This mapping is cross-checked against every `Code:` pointer in `ValidationLog.md` (48 tier-3 problems; exact match, no discrepancies).

| Module | Ref files | Problem IDs covered |
|---|---|---|
| M1 | `ps1_1_ref.py` … `ps1_6_ref.py` | PS1.1–PS1.6 (all 6) |
| M2 | `ps2_1_ref.py`, `ps2_2_ref.py`, `ps2_4_ref.py`–`ps2_7_ref.py` | PS2.1, PS2.2, PS2.4–PS2.7 (6 of 7 — see note below) |
| M3 | `ps3_1_ref.py` … `ps3_7_ref.py` | PS3.1–PS3.7 (all 7) |
| M4 | `ps4_1_ref.py` … `ps4_5_ref.py` | PS4.1–PS4.5 (all 5) |
| M5 | `ps5_2_ref.py`, `ps5_4_ref.py` | PS5.2, PS5.4 only (2 of 6 — see note below) |
| M6 | `ps6_1_ref.py` … `ps6_4_ref.py` | PS6.1–PS6.4 (all 4) |
| M7 | `ps7_1_ref.py` … `ps7_7_ref.py` | PS7.1–PS7.7 (all 7) |
| M8 | `ps8_1_ref.py` … `ps8_6_ref.py` | PS8.1–PS8.6 (all 6) |
| M9 | `ps9_1_ref.py` … `ps9_5_ref.py` | PS9.1–PS9.5 (all 5) |

**Special / shared files (4, not problem-numbered 1:1):**
- **`pump_gibbs.py`** — shared ten-pump hierarchical Gibbs sampler (backs PS7.4's export and every M8/M9 problem that consumes the PS7.4 chain: PS8.1, PS8.2, PS8.4, PS8.6, PS9.3).
- **`bimodal_mh.py`** — shared bimodal random-walk Metropolis sampler (backs PS7.6's export and its M8 consumers: PS8.2, PS8.5).
- **`ps2_3_annex_confirmation.py`** — **not a tier-3 validation artifact.** PS2.3 is a tier-1 problem (Annex A2.4/A2.5 machine-checked values); this script is drafting-time QA confirming the problem statement's model spec reproduces the Annex test case. No `ValidationLog.md` entry corresponds to it.
- **`__init__.py`** — empty; package marker enabling the relative-import structure above.

**Problems with no reference implementation (5 of 54 — by design, not an omission):** PS0.1 (self-audit, no numeric target), PS5.1, PS5.3, PS5.5, PS5.6 (M5's binding design commitment is closed-form results and direct/prior-predictive simulation only — "NO posterior sampling anywhere"; these four are tier-1/2/self-audit problems with no executed target requiring a logged reference run). Cross-checked: 49 mapped files (48 tier-3 + `ps2_3_annex_confirmation.py`) + 5 no-ref problems = 54 total problems. ✓

## Archive contents (52 files)

```
reference_impls/
├── __init__.py
├── pump_gibbs.py
├── bimodal_mh.py
├── ps1_1_ref.py … ps1_6_ref.py        (6)
├── ps2_1_ref.py, ps2_2_ref.py,
│   ps2_3_annex_confirmation.py,
│   ps2_4_ref.py … ps2_7_ref.py         (8)
├── ps3_1_ref.py … ps3_7_ref.py        (7)
├── ps4_1_ref.py … ps4_5_ref.py        (5, incl. A′ addendum)
├── ps5_2_ref.py, ps5_4_ref.py          (2)
├── ps6_1_ref.py … ps6_4_ref.py        (4, incl. corrected comment)
├── ps7_1_ref.py … ps7_7_ref.py        (7)
├── ps8_1_ref.py … ps8_6_ref.py        (6, relative-import package)
└── ps9_1_ref.py … ps9_5_ref.py        (5, relative-import package)
```

## Structural verification performed this session

- File count: 52/52 confirmed.
- All internal cross-imports (`from reference_impls.X import Y`) resolve to a file present in this archive — no broken import paths.
- All 52 files pass `py_compile` (syntactically valid Python) — no truncated or corrupted files.
- No scripts executed (per Task 3's "no compute required" instruction); the two addendum files were executed once during input verification, prior to this assembly session, and are reported separately in `Phase5B_AssemblyReport.md`.
