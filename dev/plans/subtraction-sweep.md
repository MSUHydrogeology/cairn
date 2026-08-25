# Plan: Subtraction sweep

**Source proposal**: `dev/proposals/archive/2026-08-25-claude-subtraction-sweep.md`
**Status**: revising-plan
**Plan review**: required(**Internal** + **Internal Security Review**) — two passes, one per clause, each naming its clause in its own `**Obligation**:` line. The Internal pass reads the deletion manifest. **The Security Review is a single pass covering both security surfaces this plan touches** — the trust-root extraction (C1) and the registry-edit approach (C5/C6) — because both are decided here, in this document, and reviewing the same design twice is the ratchet this sweep removes. C1 and C4 are its *fences*, not additional reviews.
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
| C1 | **Trust-root extraction** — lift `_resolve_interpreter` + `_has_symlink_component` + `_probe_interpreter` (`tools/lifecycle.py:431-579`) and the twin into a standalone module with its own tests; repoint all call sites (`:307`, `:894`, `:1395`) | fenced on the plan-level **Security Review** having cleared | 1–2 commits |
| C2 | **Constitution rewrite** — `AGENTS.md` 598→~350, `dev/agent_collaboration.md` 399→~150, `dev/proposals/_template.md` 674→~80, `dev/plans/_template.md` 594→~80, plus the four shipped `templates/core/` twins | — | 2–3 commits |
| C3 | **Three replacement tools** — warn-only audit reporter; ~100-line standalone board view; gauge classifier + dated snapshot. Each lands with its build-table probe passing | — | 3 commits |
| C4 | **Removal fence** — confirm the plan-level Security Review has landed and cleared before any removal commit, per the Decision's *"clearing the registry-edit plan before the first removal lands"*. Nothing to implement; this is the checkpoint that makes the ordering binding | **fence** | no commits |
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
* **C4** — the plan-level Security Review is appended and clears, carrying an
  `**Obligation**: Internal Security Review` line, and it addresses **both**
  surfaces: the trust-root extraction and the registry-edit approach, the latter
  with security coverage proven **by set comparison, not byte identity**.
  **No C5 commit lands before it, and no C1 commit either.**
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

## Plan review -- Claude Sonnet 5 -- 2026-08-25

**Reviewed commit**: 7dc66a10fb668b54c67782cfd544139ead70b939
**Target**: the complete plan (header through Lasting-truth migration),
cross-checked against `tools/lifecycle.py` and its twin
`templates/skills/_lib/lifecycle.py`, `templates/skills/session-start/SKILL.md`,
`templates/skills/session-end/SKILL.md`, `bootstrap/_scaffold/config.py`
(`_SKILLS_MAPPINGS`, `_ALWAYS_ON_MAPPINGS`), `bootstrap/security_check.py`'s
`scan_targets()`, `bootstrap/tests/security_manifest.py`,
`bootstrap/tests/_ast_attest.py`'s `_UPDATE_ALLOWLIST`,
`bootstrap/tests/test_skills_security.py`, and
`bootstrap/tests/test_lifecycle_brief.py`'s `TestInterpreterFence`, against the
accepted source proposal's Revision 1 and its Decision.
**Prior findings**: none
**Assurance path**: high-assurance (inherited from the source proposal's
header; the sweep touches the install contract and a named executable trust
root)
**Model**: Claude Sonnet 5
**Tier**: Internal
**Obligation**: Internal Security Review
**Findings**: raised

**Verdict: REVISE.** This pass covers both surfaces the plan declares for the
Security Review -- the trust-root extraction (C1) and the registry-edit
approach (C5/C6) -- per the plan's own framing that one pass covers both
because both are decided in this document. Two blocking findings, and both
are instances of the exact hazard this review was briefed to hunt: a
security-relevant surface goes quiet rather than failing loud, in a way the
plan's own line-count reconciliation cannot see.

### Steelman

* The trust-root line citations are exact. `_has_symlink_component` at
  `tools/lifecycle.py:431`, `_probe_interpreter` at `:457`,
  `_resolve_interpreter` at `:474`; the three call sites at `:307`, `:894`,
  `:1395` all resolve to `_resolve_interpreter(...)` calls, confirmed by
  direct read and grep. The twin (`templates/skills/_lib/lifecycle.py`) is
  byte-identical to `tools/lifecycle.py` today (`diff` confirms), matching
  the plan's framing that this is one duplicated pair, not two designs.
* `_ALWAYS_ON_MAPPINGS` (`config.py:689-708`, confirmed exact) really is
  absent from `_ast_attest._UPDATE_ALLOWLIST` (which holds only
  `_MODULE_MAPPINGS`, `_SKILLS_MAPPINGS`, `_CORE_MAPPINGS`,
  `install_onboarding` -- confirmed by reading the allowlist), so the plan's
  MAINTAINER-GATED fence on that edit is placed correctly.
* The gate-anchor and sister-migration fences are stated at the point that
  binds (C8/C9, both MAINTAINER-ONLY / MAINTAINER-GATED); I found nothing
  that routes around them. I did not move `refs/cairn/gate-anchor` or touch
  any code or fixture.
* C5's "tests needing rehoming" list is a real, useful catch -- I
  independently confirmed `test_the_two_lifecycle_copies_are_byte_identical`
  lives in `test_pilot_evidence.py:1173`, exactly as cited, and that
  `TestVocabularyLoader`'s callers survive the removed span.

### Finding 1 (blocking) -- C6 deletes the session-start/session-end orchestration mechanism, its only trust-root callers, and its dedicated security-gate suite, and the plan names none of it

**What C6 actually deletes.** `tools/lifecycle.py` is 3,910 lines today; the
plan's own double-counting arithmetic ("C5 removes ~1,440 lines from each
side of the `lifecycle.py` twin pair and C6 then removes all 3,910 of each")
states plainly that C6 removes the entire file, both copies, to zero. That
file is not only "the CLI" in the abstract -- `cmd_session_start` (`:825`)
and `cmd_session_end` (`:1332`) live inside it, and they are the **only** code
path the two skills Cairn keeps unconditionally (`_SKILLS_MAPPINGS`, "install
unconditionally, like core/") invoke:

* `templates/skills/session-start/SKILL.md`, step 1: `` python
  tools/lifecycle.py session-start `` -- described in the skill's own prose
  as performing the read-only gather **and** "one idempotent write ... the
  skills fan-out self-heal: it ensures every eligible, in-use symlink-tier
  read-path ... points at the canonical `.agents/skills/` source ... never
  clobbers a divergent target (it refuses or quarantines)."
* `templates/skills/session-end/SKILL.md`, step 1: `` python
  tools/lifecycle.py session-end $ARGUMENTS `` -- reflection scaffolding by
  default, and under `--handoff` the fail-closed concurrent-handoff lock and
  the work-intent-log prune, reached through `_do_full_handoff`
  (`lifecycle.py:1395`) -- the **third** of the plan's own three named
  `_resolve_interpreter` call sites.

Neither SKILL.md file is named anywhere in the plan's Sequence, and neither is
covered by C2 (whose scope is `AGENTS.md` / `dev/agent_collaboration.md` /
the two proposal-and-plan templates, with a named, specific "known real hits"
list that does not include either SKILL.md). After C6, both files still
instruct an agent to run `python tools/lifecycle.py session-start` /
`session-end` against a path that no longer exists.

**The trust root's only callers disappear with the file that dies.** I
grepped the tree for `_resolve_interpreter(` outside `tools/lifecycle.py` and
its twin: the only other hits are in test files. The plan's own C1 chunk
names exactly three call sites for repointing -- `:307` (inside
`cmd_session_start`), `:894` and `:1395` (inside `_do_full_handoff`, called
from `cmd_session_end`) -- and all three sit inside the very functions C6
deletes. Nothing in the plan names what calls the C1-extracted module once
C6 lands. An extraction with no surviving caller either ships dead code
(contradicting the Maintainer's "move the interpreter trust root **as
needed**" -- needed implies used), or, if a new caller gets invented during
C6 implementation to fill the gap, that caller and its own subprocess-use
pattern were never reviewed here -- defeating the point of gating C1 on this
Security Review at all.

**C1's own extraction scope misses a pinned fourth symbol.**
`bootstrap/tests/test_lifecycle_brief.py`'s `TestInterpreterFence`
(`:217-218`) names itself "Fence M3, asserted on both copies" -- the same
fence `AGENTS.md`'s high-risk-surfaces entry describes -- and pins **four**
symbols byte- and AST-digest-identical (`:119-143`): `_resolve_interpreter`,
`_probe_interpreter`, `_warn_stale_once`, and `_REBIND_REMEDY` -- "the reader
itself ..., its validation order classifier ..., its warning visibility ...,
and the remedy text those warnings carry." `_REBIND_REMEDY`
(`lifecycle.py:447-454`) sits inside the plan's cited `431-579` extraction
range and would move correctly under a literal line-range lift.
`_warn_stale_once` does **not** -- it is defined at `lifecycle.py:201`,
outside the cited range, yet `_resolve_interpreter` calls it directly
(`:561`) to emit the fallback-stale warning. The plan's C1 row names only
`_resolve_interpreter` + `_has_symlink_component` + `_probe_interpreter`; it
omits `_warn_stale_once` from the extraction's own stated scope, even though
warning *visibility* is one of the exact properties `AGENTS.md` requires a
Security Review to change, and the existing fence test already treats it as a
fourth, independently-pinned member of the same protected surface. Left as
scoped, the extraction either breaks loudly (an undefined-name error once
`lifecycle.py` is gone -- better than silent, but still a defect a plan
review exists to catch) or gets quietly reimplemented from scratch by
whoever notices, with no digest to check it against.

**The security-gate suite for exactly this surface goes silent, not red.**
`bootstrap/tests/test_skills_security.py` (418 lines) is a member of
`bootstrap/tests/security_manifest.py`'s `SECURITY_FAMILY` (`:104-108`),
described there in the manifest's own words as covering "the skills fan-out
symlink self-heal, which writes into the adopter's tree." It loads
`templates/skills/_lib/lifecycle.py` directly (`LIFECYCLE_SRC`, `:44`) and
tests exactly the surface above: content-scan over the canonical and
installed CLI/SKILL.md files, no-network-import in the CLI source,
`lifecycle.main(["session-start"])` opens no socket, three independent
anti-forgery oracles against a hostile artifact name forging an orientation
line, path-containment for the reflection write, per-artifact lockfile-hash
integrity, and a generated-output leak check. Its own guard is `pytestmark =
pytest.mark.skipif(not LIFECYCLE_SRC.exists(), reason="templates/skills not
available")` (`:48-50`). `test_lifecycle_brief.py`'s `TestInterpreterFence`
carries the identical guard pattern (`not (MODULE_PATH.exists() and
PLANNER_PATH.exists())`, `:68-71`). Once C6 deletes both copies of
`lifecycle.py`, **every one of these checks disappears by skipping, not by
failing and not by a line-count drop** -- the plan's own Verification
section's falling-test-count reconciliation ("An unexplained drop is a
defect, not a success") cannot catch this, because a skip does not change the
collected line count, only the outcome. Neither file is named anywhere in
the plan: not in the Sequence, not in "Tests needing rehoming, not deletion"
(which names four specific, narrower items and stops), not in the acceptance
criteria.

**This is an undeclared scope reduction, not just a gap.** The plan's own
"Not touched" list omits session-start/session-end orchestration by silence
rather than by naming it kept, or struck with a revival condition, unlike the
three items the plan does handle that way ("slot ratchet," "attic notes," the
third directive family). `AGENTS.md`'s own rule is explicit: "Removal counts
as a deviation, in both directions ... dropping an outcome the accepted
artifact committed to is a deviation exactly as adding one is ... a reviewer
cannot create that authority by calling the remainder out of scope." The
accepted proposal's Revision 1 §4 says only "onboarding removed; prose phase
as opened" for what order-5 touches beyond the CLI/planner/twins/tests it
names, and never scopes out session-start/session-end's mechanized
orchestration, its self-heal write, or its dedicated security tests.
Silently losing all three needs the Maintainer's explicit allowance under
this project's own rule, not a plan review pass.

**Falsifier, if the intended answer is "the SKILL.md files get rewritten in
some later, unnamed step":** name the chunk, and give the replacement command
its own registry-row and manifest bookkeeping (SKILL.md's `dst` is already a
`_SKILLS_MAPPINGS` row, so changing what it tells an agent to run is a
routine edit, not a deletion, but it still needs a named home in the sequence
and its own security coverage, given `test_skills_security.py` exists
specifically because this surface writes into the adopter's tree). If the
intended answer is instead "session-start/session-end lose their mechanized
gather and self-heal, and an agent does it by hand" -- that is a real,
larger reduction than any of the three the plan already discloses, and it
needs the same explicit-allowance treatment those three got, not silence.

### Finding 2 (blocking) -- the accepted set-comparison mechanics for C5/C6 are named but not carried into the plan's own acceptance criteria

The Decision's accepted terms state plainly: "security coverage proven by set
comparison rather than byte identity." The accepted proposal's Revision 1 §5
-- the material the Decision approved -- gave that phrase two concrete,
falsifiable components beyond the phrase itself: (a) a **positive-control
mutation**, "one unexpected shipped executable must fail the check," recorded
once; and (b) "the release scanner runs after each registry-removal commit."
`bootstrap/security_check.py`'s `scan_targets()` (`:683-755`, confirmed by
direct read) derives its scanned surface from `_MODULE_MAPPINGS`,
`_ALWAYS_ON_MAPPINGS`, and `install_manifest(modules=None)` -- exactly the
registries C5/C6 edit -- so a registry-row deletion that silently narrows
this union is precisely the failure mode SSP-4 (the External review)
identified and the Decision accepted the fix for.

The plan carries forward only the bare phrase "set comparison, not byte
identity," three times (`:193`, `:245`, `:273`), with no positive-control
mutation step and no per-registry-commit release-scan requirement anywhere in
C5 or C6's acceptance criteria (which say only "suite green after each ... a
fresh scaffold is recorded green per commit"). "Suite green" is not the same
falsifier as "one unexpected shipped executable must fail the check" -- a
suite can stay green while `scan_targets()`'s derivation has quietly shrunk,
which is the exact scenario SSP-4 demonstrated was possible with byte-identity
checks and the reason set comparison was chosen at all. Since "every
implementation chunk is a closed subset of that reviewed inventory" (Revision
1 §1) and the Decision's accepted terms include this mechanism by name,
dropping the positive-control mutation and the per-commit cadence without
flagging it is a narrowing of a Decision-approved commitment, and needs the
same explicit-allowance treatment as any other accepted-scope reduction, not
a silent restatement of the headline phrase.

**Falsifier, if this is intentional:** name where in Boundary A/B/C or the
C5/C6 acceptance criteria the positive-control mutation and the
per-registry-commit release scan actually live; I did not find them, and
their absence is exactly the kind of thing that reads as prudence at review
time and can never be shown wrong, because the version with them is never
built.

### What I could not reach

* I did not execute anything -- no test run, no scan, no scaffold install;
  the plan has no implementation yet to run against, and I was instructed to
  change no code or fixture.
* I did not independently re-derive the "36,332 across 15 files" / "11
  tests" figure for C6. The 15-files arithmetic is *consistent* with
  `lifecycle.py` + twin + `lifecycle_planner.py` + twin (20,526 lines) plus
  11 test files, but the closest 11-file combination of the obvious
  candidates I tried (every test file that imports `lifecycle.py` or
  `lifecycle_planner.py`, minus `test_lifecycle_metrics_events.py`, which
  belongs to the untouched `lifecycle-metrics` tool) sums to 14,460, about
  1,300 lines short of the 15,806 the arithmetic implies. I flag this as
  unresolved arithmetic, not a security finding -- the deletion manifest's
  completeness is the Internal pass's mandate, and I did not want to
  duplicate that reconciliation without also being able to close it.
* I did not review C2 through C9 end to end for non-security concerns (prose
  targets, the claim-check design, sister-migration discovery) -- out of this
  pass's scope by the plan's own framing.

### Coverage

**Covered:** `tools/lifecycle.py` and `templates/skills/_lib/lifecycle.py` in
full (diff-confirmed byte-identical); every line citation in this plan's C1
row and in my review brief, verified against the file; both SKILL.md files in
full; `bootstrap/_scaffold/config.py`'s `_SKILLS_MAPPINGS` (`:586-592`) and
`_ALWAYS_ON_MAPPINGS` (`:689-708`, exact); `bootstrap/tests/_ast_attest.py`'s
`_UPDATE_ALLOWLIST`; `bootstrap/security_check.py`'s `scan_targets()`
(`:683-755`); `bootstrap/tests/security_manifest.py` in full;
`bootstrap/tests/test_skills_security.py` (header plus the tests cited
above); `bootstrap/tests/test_lifecycle_brief.py`'s `TestInterpreterFence`
class and its header; the accepted source proposal's Revision 1 §§1, 4, 5 and
the Decision.

**Not covered / low confidence:** the exact byte accounting behind "36,332
across 15 files" (see above); whether `bootstrap/tests/test_lifecycle_failsafe.py`
(538 lines, also loads `templates/skills/_lib/lifecycle.py` behind an
identical `skipif` guard, also unnamed in the plan) is intended as part of
C6's "11 tests" or is a further, unnamed instance of the same gap -- I read
its header but not its full body; the C7 claim-check design and C9
sister-migration mechanics, out of scope for this pass.
