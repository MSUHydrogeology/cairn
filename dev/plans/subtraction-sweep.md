# Plan: Subtraction sweep

**Source proposal**: `dev/proposals/archive/2026-08-25-claude-subtraction-sweep.md`
**Status**: awaiting-plan-review
**Plan review**: required(**Internal** + **Internal Security Review**) — two passes, one per clause, each naming its clause in its own `**Obligation**:` line. The Internal pass reads the deletion manifest; the Security Review clears the registry-edit approach, and by the Decision's terms it must clear **before the first removal lands**.
**Last update**: 2026-08-25
**Opened**: 2026-08-25

## Source proposal

The proposal was **accepted as revised (Revision 1)** on 2026-08-25. It directs
execution of the strategy note's build table as of commit `570fedb`, in
dependency order: the constitution rewrite; three small replacement tools before
their predecessors die; the removals, each installed-source deletion atomic with
its owning registry row in `bootstrap/_scaffold/config.py`; the claim/link
checkers kept and de-scoped; the install-contract ceremony whose Security Review
clears the registry-edit approach **before the first removal lands**; then the
two sister migrations, sequential and each MAINTAINER-GATED.

The plan executes that decision. It does not re-litigate it.

**Why the manifest below is the point of this document.** The Decision names the
plan review as *"the load-bearing moment of this entire sweep — the last point
at which the deletion inventory is inspectable while the thing being deleted
still exists."* Everything after review is mechanical; a file missing from the
inventory is a file nobody agreed to delete.

## Proposed paths

None. Every path below exists today; this plan removes and edits, and creates
only the three replacement tools of C2 and the extracted trust-root module of C1.

## Scope

### What the discovery passes measured, against what the build table estimated

Three discovery passes ran 2026-08-25 against `HEAD` at the time, each writing
an inventory without touching the tree. Measured figures, `as_of 2026-08-25`:

| build-table row | order | estimate | **measured** | |
|---|---|---|---|---|
| Constitution rewrite + both templates | 1–2 | −~1,300 | −1,357 self-hosted | ~2,600 if shipped twins compress proportionally |
| Three small tools | 3 | +~530 | — | additive; not measured here |
| Transition lint, pilot ledgers, slot ratchet | 4 | −~4,000 | **7,240–7,450** | 1.8× low |
| Suite-run ledger | 4 | −~1,700 | **2,285** | 34% low |
| Lifecycle CLI + planner (+ twins, tests) | 5 | −~45,000 | **36,332** across 15 files | 19% high |
| Onboarding | 5 | −~2,000 | **8,500–9,100** | 4.3× low |
| Foldback | 5 | −~2,000 | **3,152** | 1.6× low |
| PLANNING bankruptcy + dead doctrine prose | 6 | −~6,000 | 2,576-line file, 117 tagged lines | see C7 |

**The 61k headline does not survive contact.** The Decision's own preamble said
to *"treat 61k as a headline until the manifest lands."* It has landed. Summing
the rows naively **double-counts ~4,300 lines** across the order-4/order-5
boundary: C5 removes ~1,440 lines from each side of the `lifecycle.py` twin pair
and C6 then removes all 3,910 of each, and `test_pilot_evidence.py` (1,437)
appears under both rows. Net removal is closer to **~55,000** than 61,000, and
that figure is a *consequence* of the manifest, not a target the manifest was
fitted to.

### Three things the build table names that the tree does not contain

Found by discovery; each needs the reviewer's eye because a plan cannot execute
a row that names nothing.

1. **"Slot ratchet" has no referent.** The phrase occurs in exactly two places
   repository-wide — the build table row and the proposal's §4 — and matches no
   identifier, file, or symbol. **Disposition: struck from C5** as a naming
   artifact. If the reviewer can identify what it meant, it returns as its own
   row rather than being folded silently into a neighbouring deletion.
2. **"Attic notes pointing into git history" has no identifiable file set.** The
   prose-slice pass could not turn it into a list. **Disposition: struck from
   C7.** Same condition for revival.
3. **A third directive family, `link-check-allow`, exists** and the accepted
   claim/link de-scope design does not address it. **Disposition: C7 handles it
   on the same rule as the other two families**, and says so, rather than
   leaving a third convention alive beside two retired ones.

### The trust root is inside the thing being deleted

`AGENTS.md` names `_resolve_interpreter` in `templates/skills/_lib/lifecycle.py`
a **high-risk executable trust root** whose schema, validation order, fallback
disposition, warning visibility and subprocess use each take a Security Review.
It is not a separate file: `_resolve_interpreter`, `_has_symlink_component` and
`_probe_interpreter` occupy `tools/lifecycle.py:431-579` (~150 lines) and the
byte-identical twin — the exact pair C6 deletes wholesale.

A plain file deletion destroys a surface the Maintainer explicitly kept.
**C1 extracts it first**, under the Security Review that surface already
requires. Maintainer decision, 2026-08-25, quoted verbatim:

> "Yes, move the interpreter trust root as needed"

### The pilot window ends, and that is an accepted-scope reduction

C5 removes the pilot/monitoring machinery, ending a 60-day measurement window
opened 2026-08-18 (`3c33dd0`) against the accepted `review-efficient-lifecycle`
plan. The proposal's Decision grants an allowance for the **suite-run ledger**
only. This is a second, separate reduction, and it has its own allowance.
Maintainer decision, 2026-08-25, quoted verbatim:

> "Yes, please end the pilot window now"

**Evidence it costs nothing**, recorded so it is not re-litigated: `pilot-report`
reads `0 / 6` counted stems with every measure at zero — review-input bytes,
transitions removed, escaped findings, Maintainer prompts — while **seven** plans
archived through the open window. The count requires a manual `pilot-record`
invocation at each archive that nobody ever ran, and `dev/measurement/pilot-events.md`
holds five `cairn-pilot-event` blocks, all of them schema documentation and one
placeholder example. Nothing was measured, so nothing is lost.

### The PLANNING row supersedes an accepted proposal

C7's bankruptcy pass does what `2026-08-04-claude-board-retro-disposition`
(accepted) explicitly rejected: it rejected one-pass adjudication as *"the
load-bottleneck failure mode ... reproduced at the worst possible size"* and
bulk-decline-below-a-threshold as *"visible debt traded for invisible debt, the
strictly worse trade."* Maintainer decision, 2026-08-25, quoted verbatim:

> "This proposal supersedes earlier ones, as far as the PLANNING.md row is concerned."

C7 records that supersession in the archived proposal's own tree position rather
than leaving two accepted artifacts in contradiction.

### Not touched

The intent system and collision log; the minimal board view once C2 lands it;
the security stack; the scaffold engine itself; the claim/link checkers (kept,
de-scoped in C7); and the trust-root validator, which relocates in C1 and is
never removed.

## Sequence

Nine chunks. **The `convergent-lifecycle` fence in §1 is satisfied** — its code
review cleared at `399c30c`, corrections folded at `503247b` and `fa79425`,
archived at `211c1f4`.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | **Trust-root extraction** — lift `_resolve_interpreter` + `_has_symlink_component` + `_probe_interpreter` (`tools/lifecycle.py:431-579`) and the twin into a standalone module with its own tests; repoint all call sites (`:307`, `:894`, `:1395`) | **Security Review** (the surface's own standing requirement) | 1–2 commits |
| C2 | **Constitution rewrite** — `AGENTS.md` 598→~350, `dev/agent_collaboration.md` 399→~150, `dev/proposals/_template.md` 674→~80, `dev/plans/_template.md` 594→~80, plus the four shipped `templates/core/` twins | — | 2–3 commits |
| C3 | **Three replacement tools** — warn-only audit reporter; ~100-line standalone board view; gauge classifier + dated snapshot. Each lands with its build-table probe passing | — | 3 commits |
| C4 | **Security Review of the registry-edit approach** — clears **before any removal**, per the Decision. Reviews how installed-source deletions pair atomically with their `config.py` registry rows, and proves security coverage **by set comparison, not byte identity** | **MAINTAINER-GATED entry** | review only |
| C5 | **Order-4 removals** — transition lint (`scripts/transition_lint.py` 923, `transition_lint_whitelist.py` 46, `test_transition_lint.py` 1486); the pilot/monitoring engine (~1,440 lines/side inside `lifecycle.py`); the suite-run ledger | — | 4–6 commits |
| C6 | **Order-5 removals** — lifecycle CLI + planner + twins + 11 tests (36,332); onboarding (8,500–9,100); foldback (3,152). **Only after C3's probes pass and C1 has landed** | `_ALWAYS_ON_MAPPINGS` edit is **MAINTAINER-GATED** | 6–9 commits |
| C7 | **Prose phase** — PLANNING bankruptcy; dead doctrine sections; claim/link checkers de-scoped across all three directive families | — | 3–4 commits |
| C8 | **Install-contract ceremony** — fidelity manifest, gate manifest, published `scaffold.py --manifest`; differential-oracle gate re-anchored per `REANCHOR_RUNBOOK.md` | **MAINTAINER-ONLY** | Maintainer-run |
| C9 | **Sister migrations** — `modflow_tools` first, then `lhm` after it is green | **MAINTAINER-GATED, each** | per-repo |

### Fences, stated once and bindingly

* **`_ALWAYS_ON_MAPPINGS`** (`bootstrap/_scaffold/config.py:689-708`) is absent
  from `_ast_attest._UPDATE_ALLOWLIST` — which holds only `_MODULE_MAPPINGS`,
  `_SKILLS_MAPPINGS`, `_CORE_MAPPINGS` and `install_onboarding`. Its edit is the
  **Maintainer-run, dry-run-verified direct correction**, never self-service.
* **The AST attestation baseline** re-anchors after every
  `bootstrap/_scaffold/` change, per `AST_BASELINE_RUNBOOK.md`. Derive the
  expected CHANGED set against the committed baseline each time; never carry a
  figure forward.
* **The gate anchor** (`refs/cairn/gate-anchor`) moves only in C8, only by the
  Maintainer, only per `REANCHOR_RUNBOOK.md`.
* **Both sister migrations** are MAINTAINER-GATED and sequential. `lhm` does not
  begin until `modflow_tools` is green.

### Foldback: both ledgers are drained, and that is the precondition

C6 deletes the foldback mechanism. A ledger is only safe to delete once every
row in it is upstream. Verified 2026-08-25: `modflow_tools`' Open-candidates
section is empty by design (issues #9–13, #17, filed 2026-08-20); `lhm` held one
undrained row, **#59 "The scientific-software dimension"**, status `candidate`,
never filed — now filed as issue **#18** and the ledger updated (`e205a110`).
The replacement channel already exists and is proven:
`.github/ISSUE_TEMPLATE/foldback.md` and the matching PR template.

## Acceptance criteria

Per chunk, and each falsifiable.

* **C1** — the extracted module passes the trust-root tests; every call site
  resolves through it; `AGENTS.md`'s high-risk-surface entry names the new
  location. **Falsifier**: a bad binding (non-absolute, symlinked, non-executable,
  schema-invalid) is still rejected, from the new home.
* **C2** — the four self-hosted documents and their shipped twins land at target
  size. **Falsifier**: no governing document references a tool this sweep removes.
  Known real hits to clear: `AGENTS.md:178`, `:312`, `dev/agent_collaboration.md:238`,
  `:341`, and their twins. `templates/core/AGENTS.md:457` is a confirmed false
  positive (generic English "onboarding") and is excluded.
* **C3** — each tool's build-table probe passes: the reporter lists a
  known-closed change; the board view lists the active artifacts; the classifier
  re-derives the takeover table.
* **C4** — the Security Review is appended and clears, with an
  `**Obligation**: Internal Security Review` line. **No C5 commit lands before it.**
* **C5, C6** — suite green after each; each installed-source deletion is atomic
  with its registry row; a fresh scaffold is recorded green per commit.
* **C6 (onboarding)** — sister routines still run. **C6 (foldback)** — sister
  goodnight routines updated and run clean.
* **C7** — claim and link gates pass; an archived file draws no flag; prose files
  carry zero checker boilerplate; success is silent.
* **C8** — the install contract's four surfaces agree; the gate verifies against
  the re-anchored trust root.
* **C9** — each sister's own verification is green before the next begins.

**Scope floor.** Accepted scope is a floor. The three struck rows above are
struck because they name nothing in the tree, and each is recorded with the
condition that revives it. Any *other* reduction is a deviation needing the
Maintainer's explicit allowance — a reviewer cannot create that authority by
calling remaining work out of scope.

## Verification

**Boundary A (iteration, scoped).** Per chunk: the tests owning the touched
surface, plus every standing gate for it. C2 and C7 are prose-dominant and run
the claim, link, snippet and neutrality gates.

**Boundary B mode: `full`.** Not a choice, and not per-chunk-negotiable. This
sweep touches the **install contract** (fidelity manifest, gate manifest,
lockfile schema, published `scaffold.py --manifest`), the **scaffold/merge
engine**, and **trust-ceremony surfaces** (the interpreter binding in C1, the
gate re-anchor in C8). `AGENTS.md` refuses bounded mode on either, and
uncertainty resolves to `full`.

Run after the final implementation commit of each of C1, C5, C6, C7, against a
clean unchanged commit under the canonical interpreter (Python 3.13.x):

```
CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0
python scripts/quality_gate.py --sub neutrality --sub redundancy
```

The bare form exits 4 by design. Record each as
`## Implementation verification -- <agent> -- YYYY-MM-DD` with tested SHA,
interpreter, clean pre/post state, commands, outcomes, timing, non-pass
disposition and known omissions.

**A falling test count is expected and must be accounted for, not observed.**
This sweep deletes ~15,800 lines of tests in C6 alone. Every Boundary B record
states the expected delta and reconciles it against the files that chunk removed.
An unexplained drop is a defect, not a success — the whole hazard of a deletion
sweep is that a suite gets quieter as it gets weaker.

**Boundary C (falsification, independent).** The code reviewer verifies each
record against the reviewed range and runs independent targeted falsification.
For this sweep the named instrument is **set comparison, not byte identity** —
the Decision says so for security coverage, and the same applies to registry
rows and manifest membership.

### Tests needing rehoming, not deletion

Discovery flagged these as **shared surface inside a dying file**. Deleting them
with their host loses coverage of something that survives.

* `TestVocabularyLoader` (`test_pilot_evidence.py:362-514`) — the vocabulary
  loader is still called by `cmd_review_brief`, `_declared_assurance` and
  `_build_closeout`, none of which sit inside the removed span.
* `test_the_two_lifecycle_copies_are_byte_identical` (`:1173-1232`) — still true
  and still valuable while C5 removes only part of `lifecycle.py`.
* `_has_symlink_component_below` (`lifecycle.py:1846-1870`) and `_git_ok`
  (`:1999-2011`) — inside C5's span, used by surviving code.
* Six tests using `lifecycle.py` purely as a generic scaffold-mechanism fixture
  need repointing; two need single-line edits.

## Code review

Floor: a same-type agent in an independent context, not the implementing agent.
**One round per chunk group** — C1, C2+C3, C5+C6, C7 — with a second round only
on a blocking finding.

**What review should anchor on**, per the Decision: code behaviour, trust roots,
and install-contract consequences — the registries publishing what C6 deletes,
reproduced with a named failing test; `_ALWAYS_ON_MAPPINGS` being Maintainer-run;
`scan_targets()` deriving coverage from those same registries. A reviewer who
spends a round on field spellings against a dying parser is running the ratchet
this sweep exists to remove.

## Lasting-truth migration

On archive: the measured-versus-estimated table above migrates to the strategy
note as the record of what the sweep actually cost, and the three struck rows
migrate with their revival conditions. The trust-root's new location updates
`AGENTS.md`'s high-risk-surface list in C1, not at archive.
