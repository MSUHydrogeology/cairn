<!-- A deletion manifest necessarily cites what it deletes: each path in the
     directive below resolved when this plan was written, and stops resolving
     as the chunk that removes it lands. The citation IS the record of what
     went, so it stays and the checker is told why. -->
# Plan: Subtraction sweep

**Source proposal**: `dev/proposals/archive/2026-08-25-claude-subtraction-sweep.md`
**Status**: archived — C1-C9 all landed; code review satisfied for every chunk group the plan names; dispositions final; lasting truths migrated. See `## Archive` at the foot.
**Plan review**: required(**Internal** + **Internal Security Review**) — two passes, one per clause, each naming its clause in its own `**Obligation**:` line. The Internal pass reads the deletion manifest. **The Security Review is a single pass covering both security surfaces this plan touches** — the trust-root extraction (C1) and the registry-edit approach (C5/C6) — because both are decided here, in this document, and reviewing the same design twice is the ratchet this sweep removes. C1 and C4 are its *fences*, not additional reviews.
**Last update**: 2026-08-27

> **Status-header correction, 2026-08-27.** This header read
> `awaiting-plan-review` from plan-open until today, while C1 through C7 were
> implemented and committed. Both plan reviews had landed and been answered; the
> Maintainer had ruled that no re-review was owed (*"There isn't a lifecycle
> requirement, we are dismantling it"*), and implementation began — but nobody
> advanced the status, so `python tools/board.py` reported a plan awaiting review
> that had in fact been built. Corrected here rather than at archive, because a
> derived board is only worth having if the artifacts it reads are true.
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

None outstanding. `tools/session.py` and `templates/skills/_lib/session.py`
were forward references until C1 created them; the declarations are dropped
because the paths now resolve.

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

### The manifest, per file

**This replaces the aggregate totals the first draft carried.** A plan reviewer
tried to reconstruct C6's inventory from those totals and could not — which is
the finding, in its strongest form. Line counts `as_of 2026-08-25`.

**C5 — transition lint** (2,455)

| file | lines | disposition |
|---|---|---|
| `scripts/transition_lint.py` | 923 | whole |
| `scripts/transition_lint_whitelist.py` | 46 | whole |
| `bootstrap/tests/test_transition_lint.py` | 1,486 | whole |

Self-host only; **no install-manifest row**, so no registry edit pairs with it.

**C5 — pilot / monitoring** (~4,315 + twin span)

| file | lines | disposition |
|---|---|---|
| `tools/lifecycle.py` + twin | ~1,440 each | partial — the monitoring span (`:1447` through `cmd_pilot_record`), **minus** `_has_symlink_component_below` (`:1846-1870`) and `_git_ok` (`:1999-2011`), both used by surviving code |
| `bootstrap/tests/test_pilot_evidence.py` | 1,437 | whole, **after** `TestVocabularyLoader` (`:362-514`) and `test_the_two_lifecycle_copies_are_byte_identical` (`:1173-1232`) are rehomed |
| `bootstrap/tests/test_lifecycle_contract.py` | 578 of 6,983 | partial — a gap-closing section a name-based search does not surface |
| `dev/measurement/pilot-activation.md`, `pilot-events.md` | — | whole |

**C5 — suite-run ledger** (2,285 + partials)

| file | lines | disposition |
|---|---|---|
| `bootstrap/tests/test_suite_ledger.py` | 1,394 | whole |
| `tools/suite_cost.py` | 619 | whole |
| `bootstrap/tests/conftest.py` | ~795 of 1,330 | **partial, and the delicate one** — interleaved with the `CAIRN_FULL_SUITE` broad-run guard and release-mode machinery **this plan's own verification depends on**. Isolate before cutting |
| `bootstrap/tests/test_broad_run_guard.py` | 82 of 669 | partial |
| `dev/measurement/suite-runs.jsonl` | — | whole |

**C6 — order 5, wholly removed sources** (19,126 after the kernel leaves)

| file | lines | disposition |
|---|---|---|
| `tools/lifecycle_planner.py` + twin | 6,353 each | whole |
| `tools/lifecycle.py` + twin | 3,910 each | whole **minus** the ~700-line kernel C1 extracts and minus C5's span |

**C6 — order 5, wholly removed tests** (13,413)

| file | lines |
|---|---|
| `bootstrap/tests/test_lifecycle_contract.py` | 6,983 |
| `bootstrap/tests/test_lifecycle_board.py` | 1,885 |
| `bootstrap/tests/test_lifecycle_vocabulary.py` | 1,037 |
| `bootstrap/tests/test_lifecycle_brief.py` | 1,170 |
| `bootstrap/tests/test_pilot_evidence.py` | 1,437 |
| `bootstrap/tests/test_byline_identity.py` | 685 |
| `bootstrap/tests/test_doctrine_vocabulary_drift.py` | 216 |

**C6 — repointed to the session kernel, NOT deleted** (~1,510 + two splits)

The first draft marked several of these for deletion. They test surfaces that
**survive C1**, so deleting them is coverage loss with no corresponding removal.

| file | lines | why it survives |
|---|---|---|
| `bootstrap/tests/test_skills_security.py` | 418 | a **member of `security_manifest.py`'s `SECURITY_FAMILY`** — covers the skills read-path that C1 keeps |
| `bootstrap/tests/test_skills_self_heal.py` | 224 | tests `_heal_skills_fanout` directly |
| `bootstrap/tests/test_prune_tools.py` | 256 | tests session-end's `_prune_reflections` |
| `bootstrap/tests/test_skills_upgrade.py` | 252 | upgrade round-trip for the kept CLI |
| `bootstrap/tests/test_skills_install.py` | 144 | install path for the kept CLI |
| `bootstrap/tests/test_skill_contract.py` | 126 | the SKILL.md contract itself |
| `bootstrap/tests/test_first_session_report.py` | 90 | session-start's output |
| `bootstrap/tests/test_lifecycle_failsafe.py` | 538 | **split** — trust-root fallback coverage repoints, the rest dies |
| `bootstrap/tests/test_lifecycle_cli.py` | 684 | **split** — the session subcommands repoint, the rest dies |

**C6 — partial edits, no deletion** (4 files)

`test_security_stack.py` (1,533, uses `tools/lifecycle.py` as a tamper-target
fixture), `test_security_check.py` (1,270, asserts both files in scan targets),
`test_security_lint.py` (483, lists both in a lint target set),
`test_scope_reduction_trap.py` (694, imports the planner; ~330 lines coupled).

**Two corrections to the first draft's own membership, both found by measuring
each file's actual target rather than its name:**

* `test_lifecycle_stage_patterns.py` (753) was listed as wholly dependent. It
  tests `templates/modules/default-on/lifecycle_metrics.py` — a module this
  sweep **keeps**. **Struck from the manifest.** Deleting live coverage of a
  surviving surface is the worse error direction, and a name-based reading
  produced it.
* `test_lifecycle_metrics_events.py` (560) is the same case, and was never in
  the manifest. Recorded here so a later reader does not re-add it.

**The order-5 headline moves, and downward.** The first draft claimed 36,332
across 15 files. Corrected membership plus the surviving kernel puts wholly-
removed order-5 nearer **32,500**, with ~1,500 lines of tests repointed rather
than deleted and ~1,400 lines of source (both kernel sides) surviving. The
sweep's net is nearer **~51,000** than the 61,000 headline.

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
   leaving a third convention alive beside two retired ones. Because this is an
   *addition* to accepted scope rather than a cut, it carries the same four
   falsifiers the accepted design states for the other two families: an archived
   file draws no flag; a prose file carries zero checker boilerplate; success is
   silent; and a genuinely broken link still fails. If `link-check-allow` cannot
   meet all four on the same rule, it stays as it is and this row is struck.

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

### What C1 extracts, and why it is not just the trust root

**Both plan reviewers reached this independently, and they were right.** C6
deletes `tools/lifecycle.py` and its twin to zero — 3,910 lines each. That file
is not only the dying machinery. It also holds:

* `cmd_session_start` (`:825`) and `cmd_session_end` (`:1332`) — the **entire
  mechanized content** of `.agents/skills/session-start/SKILL.md` and
  `session-end/SKILL.md`, both of which invoke `python tools/lifecycle.py
  session-start` / `session-end` **by name**. Those SKILL.md files are kept.
* `_heal_skills_fanout` (`:785`) — the skills fan-out self-heal that this
  repository's own `CLAUDE.md` names as load-bearing.
* `_warn_stale_once` (`:201`) — pinned by `test_lifecycle_brief.py`'s
  `TestInterpreterFence` as part of the **same protected surface** as the trust
  root. The first draft's extraction range (`:431-579`) omitted it.
* The trust root itself (`:431-579`) and all three call sites (`:307`, `:894`,
  `:1395`).

**Why the first draft missed it, stated plainly:** the coverage that would have
caught it — `test_skills_security.py`, `test_skills_self_heal.py`, and
`TestInterpreterFence` — loads `lifecycle.py` behind a `pytest.mark.skipif`
guard. Delete the file and those tests **skip rather than fail**. They go
*silent, not red*, which means this plan's own falling-test-count reconciliation
would not have caught it either. A guard written to keep a suite green in a
tree that lacks the file becomes, at deletion time, the thing that hides the
deletion.

**So C1 extracts a session kernel, not a validator.** `tools/session.py` and its
byte-identical twin `templates/skills/_lib/session.py` carry: `_warn_stale_once`; the trust-root trio (`:431-579`);
`_heal_skills_fanout` (`:785-821`); `cmd_session_start` (`:825-911`); the
full-handoff guards and prune/surface helpers (`:915-1262`); and the session-end
block (`:1282-1446`). That is **~800 lines before subtraction**, and two of its
helpers leave with their own rows — `_surface_foldback_candidates`
(`:1227-1262`) goes with foldback, and `_run_evolution_infer` (`:1194-1226`)
with the metrics work — so the kernel lands nearer **~700 lines per side**.
Measure it at implementation; do not carry this estimate forward as a fact.

**Every `skipif`-guarded loader of `lifecycle.py` is repointed in C1, not C6.**
That ordering is what converts a silent skip into a real test.

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

## Scope delta -- the lifecycle-metrics module is removed -- 2026-08-26

**Relayed authorization, quoted verbatim and visually isolated.** The Maintainer
gave this in a concurrent Strategy session, not to this session; it reached here
through that session's agent, and the attribution says so rather than implying
it was spoken to me:

> "Wow, okay, yes please tell the other agent to remove it"

"It" is the **lifecycle-metrics module**, from the immediately preceding
exchange: the Maintainer asked *"If we remove that module, how do we track our
productivity?"* and accepted the answer that the gauge classifier plus git's
one-commit-per-transition discipline carry what is needed.

**Why this is a delta and not an ordinary row.** The accepted build table has no
metrics row -- a drafting omission, acknowledged as such by its author. The
module therefore survived the sweep **by silence**, not by decision, while the
strategy note's measured-sweep section and the 2026-08-24 guide star both stated
the removal intent. A plan reviewer flagged it as never named in either
direction. Silence is not a decision, so this records one.

**Measured per file, not by name** (`as_of 2026-08-26`):

| file | lines | disposition |
|---|---|---|
| `tools/lifecycle_metrics.py` + `tools/_lifecycle_metrics/` | 2,226 | whole |
| `templates/modules/default-on/lifecycle_metrics.py` + `_lifecycle_metrics/` | 2,226 | whole, byte-identical twin |
| `bootstrap/tests/test_lifecycle_stage_patterns.py` | 753 | whole |
| `bootstrap/tests/test_lifecycle_metrics_events.py` | 560 | whole |
| `bootstrap/tests/test_lifecycle_metrics_config.py` | 266 | whole |
| `bootstrap/tests/test_metrics_status_normalization.py` | 162 | whole |
| `bootstrap/_scaffold/config.py` | registry rows | edited, atomic with the deletion |

**Total ~6,193 lines**, against the ~5,980 the relaying session estimated. The
gap is `test_metrics_status_normalization.py`, which matches no
`lifecycle_metrics` name pattern and is invisible to a name-based sweep -- the
same failure mode that put a false inclusion and six missing files in this
plan's first manifest.

**This reverses a strike recorded above, and the reversal is deliberate.**
`test_lifecycle_stage_patterns.py` was struck from the order-5 manifest as a
false inclusion *because it tests a module this sweep keeps*. That premise is
now retired: the module does not survive, so the file dies -- for its own
reason, as a metrics test, not as the planner test it was wrongly filed as. A
later reader should not read this as drift.

**One premise of the recommendation was stale, and the record says so.** The
relaying session argued in part that the module "is currently broken
(`dev/PLANNING.md:128` -- exits `INCOMPLETE`)". That row was **closed** at the
2026-08-25 goodnight: the handoff's own run wrote
`dev/measurement/snapshots/2026-08-25-1.csv` -- 120 rows, 71 proposals + 49
plans, exit 0, none refused -- because `retire-event-blocks` removed the
machinery whose activation cutoff caused the refusal. The row's reproduction
command was also wrong as written: it names the *template* copy, which refuses
by design, with a `--root` defaulting to the script's own directory.

The other two reasons are untouched and are what this delta rests on: the tool
parses the proposal/plan grammar the constitution rewrite replaces, and the
gauge classifier carries the empirical program. But if "it is already broken"
was weighed, it was weighed wrongly, and reversing this delta should stay cheap.

**Execution.** Removal runs inside the existing chunks and behind their existing
fences -- installed-source deletion atomic with its registry row, the Security
Review cleared before the first removal, a green fresh scaffold per commit.
Nothing about this delta is executed in the session that recorded it.

## C6 onboarding -- measured at the gate, not estimated -- 2026-08-26

**The gate is the first domino, not the last.** `_ALWAYS_ON_MAPPINGS` contains
exactly the nine onboarding engine files and nothing else, and the engine ships
verbatim to every adoption. So its tests, doctrine and presets all document live
code: there is no safe prefix to remove before the Maintainer's registry edit.
An earlier reading of this plan assumed the opposite.

**Validated in a throwaway worktree rather than estimated.** Three rounds, each
finding another importer the previous draft missed. What the edit actually
reaches:

| file | change |
|---|---|
| `bootstrap/_scaffold/config.py` | `_ALWAYS_ON_MAPPINGS` 9 rows -> `()` — **the gated edit** |
| `bootstrap/_scaffold/install.py` | `install_onboarding`, 222 lines |
| `bootstrap/_scaffold/__init__.py` | facade export |
| `bootstrap/_scaffold/cli.py` | import **and a named phase of the live install sequence** |
| `bootstrap/tests/test_upgrade_side_door_parity.py` | 126 of 444 lines |
| `bootstrap/tests/test_security_leaf.py` | roster entry |
| `bootstrap/tests/test_hardening.py`, `test_install_module.py` | the install-writer roster naming `install_onboarding` |
| `bootstrap/tests/_ast_attest.py` | a `_UPDATE_ALLOWLIST` key that would name nothing |
| `bootstrap/_scaffold/SECURITY_MUTATIONS.md` | its mutation-table row |

With all of that applied the suite collects and runs: **2,988 passed**, with the
residue being the two standing fences, the oracle's uncommitted-engine
comparison, and count pins.

**Two properties lose their subject, and that is a decision rather than
bookkeeping.**

* `assert_always_on_complete` fails closed before any write on an incomplete
  launcher+engine group. With the group empty it guards nothing, and
  `SECURITY_MUTATIONS.md` documents it as a live security mutation.
* The **side-door parity** property exists because always-on helpers ship
  *outside* `_MODULE_MAPPINGS` and were once missed by the release scan. Empty
  the group and the category is empty. Deleting those tests closes the record
  of a real blind spot; converting them into a guard that any *future*
  always-on member must be scanned keeps it closed. The second is an addition,
  so it is the Maintainer's call.

**~73 tests sit behind onboarding-shaped guards** across at least five files.
Three (`test_active_surfacing_mechanism`, `test_active_surfacing_render`,
`test_deferred_task_store`) name the progressive-onboarding plan in their own
docstrings and die with it. The others need reading one at a time — the
`guard names more than its tests need` rule this plan already carries, applied
here rather than assumed.

## Sequence

Nine chunks. **The `convergent-lifecycle` fence in §1 is satisfied** — its code
review cleared at `399c30c`, corrections folded at `503247b` and `fa79425`,
archived at `211c1f4`.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | **The session kernel** — extract everything in `tools/lifecycle.py` that must outlive it into `tools/session.py` + twin, and repoint all call sites. See "What C1 extracts, and why it is not just the trust root" below | fenced on the plan-level **Security Review** having cleared | 2–3 commits |
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

## C2 deviation -- the ~80-line template target is not reachable

**Declared under the deviation rule, and the direction matters: this delivers
*less compression* than the plan projected, not less scope.** Every outcome C2
committed to still lands. The estimate was wrong.

| file | before | after | cut |
|---|---|---|---|
| `dev/proposals/_template.md` | 674 | 298 | 56% |
| `dev/plans/_template.md` | 594 | 230 | 61% |
| `templates/core/dev/proposals/_template.md` | 623 | 246 | 60% |
| `templates/core/dev/plans/_template.md` | 583 | 218 | 63% |
| `AGENTS.md` | 602 | 353 | 41% |

**Why ~80 lines was never available.** Cutting to the target first and running
the suite after surfaced 28 failures across `test_scope_reduction_trap` and
`test_lifecycle_contract`. Three classes of content in these files are
load-bearing rather than preamble:

* **Doctrine the suite actively pins** — the anti-narrowing floor, the review
  basis, the assurance path, the contract revision and its withdrawal ledger.
  The scope-reduction rule is the one *this sweep's own plan* cites against
  itself, and the test pinning it demands the author say "why specifying was
  rejected" before cutting it.
* **Eight adopter-customization slots**, each a paired block whose guidance
  prose is ~100 lines across the two templates. Removing them removes adopter
  customization, not verbosity.
* **The five design-time security questions (S1-S5)**, which the first cut
  dropped by omission. S2 — *"if a check derives what it expects from the same
  object it is checking, that check cannot fail"* — is precisely the defect
  that put a false inclusion in this sweep's own manifest.

**The honest number is ~1,482 lines removed across the four templates**, against
a `-1,357` build-table estimate that covered all six constitution files. So the
templates alone exceeded the estimate for the whole row while missing their own
per-file target — the estimate was not merely low, it was distributed wrongly.

**What would make ~80 reachable, and why it is not done here.** The pins live in
`test_lifecycle_contract.py`, which C6 removes. Cutting further is therefore a
C7 opportunity, once the pins are gone — recorded so the remaining compression
is not lost as an omission.

## C4 fence -- disposition, recorded rather than stepped past

**The fence.** The Decision's accepted terms place *"the install-contract
ceremony with its Security Review clearing the registry-edit plan **before**
the first removal lands"*. C4 is that checkpoint. It ships no commits; its only
job is to make the ordering binding.

**What actually happened.** The Internal Security Review ran (`3ff6e4a`) and
returned **REVISE** with two blocking findings. Both are answered in the
Response above: C1 became the session kernel and has since been implemented and
verified, and the accepted set-comparison mechanics are now C5/C6 acceptance
criteria in full rather than a repeated phrase. No second Security Review pass
was requested.

**Why the fence is treated as satisfied without one.** The Maintainer's standing
instruction, given repeatedly across this work, is that review cycles are the
bottleneck being removed — *"we aren't doing review cycles anymore unless
absolutely required."* The findings were answered rather than argued, and the
larger of the two was answered by *building the thing the reviewer said was
missing*, which is stronger evidence than a second pass agreeing it is now
described.

**Stated plainly so a later reader is not misled:** this fence was cleared by
the author's answers and the Maintainer's standing instruction, **not** by a
reviewer confirming closure. If that distinction matters to someone reading
this after the fact, it is recorded here precisely so they can weigh it.

**What the fence still binds.** C5 and C6 remain bound by everything else the
Decision names — each installed-source deletion atomic with its registry row, a
green fresh scaffold per commit, set comparison rather than byte identity with
its positive-control mutation, the release scan after each registry-removal
commit, and every MAINTAINER-GATED marker. Clearing the review does not soften
any of those.

## C7 routing map -- where PLANNING.md's content goes

**Recorded here at the Maintainer's direction**, relayed through the concurrent
Strategy session that inventoried the file. The authorization, verbatim:

> "Please, yes, and ask them to add it to the plan to survive compaction"

The inventory is that session's; the direction is the Maintainer's; the reason
it lives here rather than in a session's context is the quoted instruction.

**The question it answers.** C7 previously carried checker-gate acceptance
criteria and no destination map — so "bankruptcy" had no answer to *where does
this go?*, which is the difference between retiring a roadmap and dropping it.
`dev/PLANNING.md` is 2,590 lines in nine blocks (`as_of 2026-08-26`; re-verify
the boundaries when C7 executes, since C2 and C6 both edit this file first).

| section | ~lines | disposition |
|---|---|---|
| Where the project stands (`:22`) | 55 | survives — trimmed PLANNING keeps a short status plus pointers |
| Onboarding (`:57`) | 63 | dies with the onboarding mechanism |
| Queued (`:120`) | 850 | triaged row by row: live to GitHub issues, dead to an explicit decline |
| Active (`:971`) | 204 | collapses to pointers; state lives in the artifacts and the board view |
| Status taxonomy (`:1175`) | 25 | to the constitution rewrite (C2) |
| Archive + removal preconditions (`:1200`) | 69 | to the constitution rewrite (C2) |
| Migrated roadmap (`:1269`) | 230 | one issue each, revival condition in the issue body |
| Security-cluster routing (`:1508`) | 1,010 | folds into `dev/strategy/2026-08-05-codex-security-strategy.md`'s cluster map; PLANNING keeps pointers |
| Release path (`:2518`) | 72 | survives — the version ladder is PLANNING's remaining job |

**The Queued block is not one-pass adjudication, and that distinction is load-
bearing.** The accepted `2026-08-04-claude-board-retro-disposition` rejected
one-pass adjudication as *"the load-bottleneck failure mode ... reproduced at
the worst possible size"* and bulk-decline as *"visible debt traded for
invisible debt, the strictly worse trade."* The Maintainer's supersession
(recorded above) licenses bankruptcy; it does not license either of the two
shapes that proposal named. So the 850-line Queued block is drained row by row
across one or more conducted sessions, with parks batched to the Maintainer —
not adjudicated in a single pass.

**Two sequencing constraints this adds:**

* **C7 runs after C6** for the Onboarding block, so no orphaned surface is left
  pointing at a removed mechanism.
* **The Queued drain may run before or alongside C7** rather than inside a
  single C7 commit.

**The acceptance criterion the map enables**, which C7 could not previously
state: **no live row is deleted without a named destination or an explicit
decline in the record.** A checker gate cannot express that; a destination map
can.

The security block's authority is that strategy doc's own committed
serialization note, not this table.

## C7 bankruptcy record -- the security block, executed 2026-08-27

The routing map above gave the security block a destination. This records the
pass that used it, and satisfies the map's own acceptance criterion -- *no live
row is deleted without a named destination or an explicit decline in the
record* -- for this block.

**Shape.** `dev/PLANNING.md` `### Security-cluster routing`: 1,010 lines, 13
groups, **93 top-level rows** (enumerated mechanically, not counted by eye).
`dev/PLANNING.md` goes 2,591 -> 1,612 lines. The surviving rows are now the
**Live residual register** in
`dev/strategy/2026-08-05-codex-security-strategy.md`, which goes 621 -> 1,283
lines; the board keeps a pointer and a where-to-look table.

**Method, and why it was not judgment alone.** The hazard in a bankruptcy pass
is dropping a row whose subject is still alive, or -- the quieter failure --
carrying forward a row whose subject the sweep already deleted, so the register
ships a revival trigger that can never fire. Both were checked mechanically
before any row was judged:

* Every backticked path in the block was extracted and resolved against the
  tree: **77 distinct paths, 32 unresolved**, of which most are bare basenames
  used in prose and four are cited *because* they do not exist (`pytest.ini`,
  `pyproject.toml`, `tox.ini`, `setup.cfg` -- the root-conftest row's point is
  that none exists).
* Every cited symbol was resolved the same way. This is what caught the
  byline-classification rows: `_fold_word` returns **zero non-`dev/` hits**, and
  `dev/.cairn/agent-identities.json` has **no reader anywhere outside the
  deliberation record**. Four rows whose class the cluster map still calls "one
  identity authority surface" had lost their entire subject to C6.

**Dead rows -- 14, each with the measurement that showed the subject gone.**
These are not carried into the register.

| row | measurement |
|---|---|
| Preflight **R3** | trigger was "the `transition-lint` proposal landing a lifecycle linter"; C5 removed the transition lint, so the trigger names a mechanism that cannot arrive |
| Preflight **R5** | pinned a sub-block of `Author-accounting`; `git grep` finds **zero** occurrences of that block in `templates/` after C2's rewrite |
| Preflight **R6** | `_has_kind` survives only in `scripts/gen_legacy_passes.py`, a one-off generator; the planner gate it described is gone |
| Structural line-reader follow-ups | `_gitignore_status` has **zero** hits tree-wide; the audited class-D `splitlines()` sites named lifecycle-metrics, removed at C6. Its one live limb -- the two private CR/LF helpers -- is folded into the register's [BND-4] pairs-only entry |
| Lifecycle mutation/commit arm | the lifecycle CLI it extended is gone (C6). The **authority boundary survives** and is restated in the register's [REC-5] entry as binding on any future mechanism |
| Lifecycle mechanization dogfood study | the study existed to earn the row above; with no mechanism there is nothing to earn |
| Planner cross-checks | `tools/lifecycle_planner.py` does not resolve (C6) |
| `_agent_of` round-suffix regression test | `_agent_of` appears only in `CHANGELOG.md` and archived artifacts |
| Lifecycle-routine skill payloads (post-v1) | the four proposed episodic skills were transitions of the removed CLI |
| Marker grammar's second, weaker definition | `templates/modules/default-on/_lifecycle_metrics/parse.py` does not resolve (C6) |
| One unchecked claim in the transition gates | `bootstrap/tests/test_lifecycle_contract.py` does not resolve; the planner that reported the claim met is gone |
| **Four** byline-classification rows (NFKD mappings unpinned; `casefold()` sampled not enumerated; no hostile roster tested; the B2 adjacency undecided) | the identity normalizer is gone -- `_fold_word` has zero non-`dev/` hits and `dev/.cairn/agent-identities.json` has no reader |
| SP8-1 item (b) | "fix `tools/lifecycle_planner.py`'s archive gate" -- the file does not resolve |
| SP8-9's planner-owned residuals | the `Dispositions:` parser, the `--include-archive` scan mode and the loop-fidelity precondition regex were all planner code (C6). The separate `bootstrap/tests/test_loop_fidelity_gate.py` is a different gate and is untouched |

**Already discharged, so not carried:** SP8-1 (a), SP8-2, SP8-9 and SP8-11 each
record their own discharge in the block; the archived plans hold the evidence.

**Live rows: 75, all folded.** Every remaining row reached the register. Two
were re-measured rather than transcribed, because the sweep had moved their
subject and a stale figure is the thing this plan keeps getting wrong:

* **SC2's `B607` findings** -- the row said "four `B607` findings" in
  `templates/skills/_lib/lifecycle.py` and `lifecycle_planner.py`, neither of
  which resolves. Re-measured with Bandit 1.9.4 against the surviving
  session-kernel twins: **9 LOW -- `B404` x1, `B603` x6, `B607` x2**, both
  `B607` sites in `session.py`. The finding is live and smaller; the register
  carries the new figure and says when it was taken.
* **The detached-checkout `__pycache__` guard** -- re-run 2026-08-27 without
  `PYTHONDONTWRITEBYTECODE`: still red, still green under the suppressor,
  unchanged by the sweep. The row's own sharper diagnosis holds.

**One orphan the pass surfaced, and the Maintainer closed.** The identity
roster was still on disk with **nothing reading it** -- C6 removed its only
consumer. It was *tracked*, not machine state, and covered by no lockfile
record, manifest entry or test, so nothing reddened. Deleted 2026-08-27 under
the Decision recorded in the strategy's [REC-1] entry, which also settles the
wider question the pass raised: reviewer independence stays doctrinal, and no
mechanical successor is owed.

**Two rows carry a Maintainer disposition and were preserved verbatim rather
than summarized**: SC4's *"SC4 - fold in"* and the detached-checkout guard's
filing instruction. A quoted authorization does not get paraphrased in a
compression pass.

**What the strategy owed, now paid.** Its refocus serialization note listed four
rows that would "conform when their sweep chunk lands". All four chunks have
landed and all four are conformed in that note, including [VER-6], whose
question was whether the five security-preflight questions survived C2's
constitution rewrite. **They survived** -- verified in both templates -- so the
answer is recorded as *survived*, not left as a silent drop.

### Second pass -- the security rows the routing map did not see

The map assigned the *Security-cluster routing* block to the strategy and the
*Queued* block to forge issues, as if the two were disjoint. **They were not.**
The strategy's own authority rule says placement under a general roadmap heading
does not put an item outside it, and Queued held **twelve security-cluster rows**
-- four tagged `[SEC]`, plus `[TRU-1]`x2, `[TRU-4]`, `[TRU-5]`, `[TRU-7]`,
`[BND-6]`, `[REL-6]`, `[REC]` -- with revival triggers, sitting in a backlog
routed to issue triage. Folded 2026-08-27 into the register with the rest; one
(`[TRU-7]`, the unpublished gate anchor) was a **duplicate** of a row the
strategy already carried in full and needed no content.

**The row-by-row mapping, added 2026-08-27 after code review.** The Internal
review of C7 found the counts above reconstruct only by re-deriving them, which
is a fair complaint about a record whose whole job is to make a drop
inspectable. Re-derivation confirms the arithmetic (11 + 1 + 7 = 19) and that
nothing live was lost, but the table belongs here rather than in a reviewer's
working notes:

| Queued row | disposition |
|---|---|
| `[SEC]` M2 conflates review with produce | folded -> register `[REC]`, second clearing review |
| The lasting-truth attestation grows after it is written | folded -> `[REC-4]` |
| `[SEC]` No regeneration procedure for an existing lockfile | folded -> `[TRU-1]` |
| `[SEC]` Two install-contract artifacts stale (RESOLVED) | **live remainder only** folded -> `[TRU-4 / REL-3]`, who re-anchors and under what review |
| `[SEC]` The interpreter-binding re-pin | folded -> `[TRU-5]` |
| The controlled re-anchor path cannot run | folded -> `[TRU-4]` |
| The loop-fidelity gate covers one folder | folded -> `[REL-5]` |
| Portable-security-sweeps deferred set | folded -> `[VER-4]` |
| `[REL-6]` `SECURITY.md` disclosure channel | folded -> `[REL-6]` |
| `[TRU-1]` Self-host lockfile reconciliation | folded -> `[TRU-1]`, second entry |
| `[BND-6]` Lockfile schema validate-on-read | folded -> `[BND-6]` |
| `[TRU-7]` The gate anchor is unpublished | **duplicate** -- the register already carried it in full |
| `[TOOL, URGENT]` metrics extraction broken | dead |
| `[TOOL]` divergent-activation-marker unreachable | dead |
| `[TOOL]` checker flags every Internal review as author-written | dead |
| `[REC]` Five plan-review sections owe basis fields | dead |
| `[REC-3]` Transition-lint | dead |
| The review-allocation pilot, never switched on | dead |
| `[VER]` AST attestation re-anchor after the tag pass | closed 2026-08-20 |

The fourth row is the one that reads oddly and is correct: its headline was
already marked RESOLVED, so only the live question it left behind -- *who*
re-records the trust artifacts, under what review -- was carried, and it landed
under a tag that does not match the row's original one.

**Seven more Queued rows were dead or closed**, taking the block from 852 lines
to 260. Six lost their subject to this sweep; each measurement:

| row | measurement |
|---|---|
| `[TOOL, URGENT]` corpus-wide metrics extraction is broken | the extractor is gone (C6); the row was already struck through |
| `[TOOL]` divergent-activation-marker check unreachable | `activation_commit`, `_reconcile_artifact` and `extract_proposal_row` all have zero hits outside `dev/` |
| `[TOOL]` the checker flags every Internal review as author-written | the planner's independence check is gone -- **the third independent corroboration** that nothing mechanical reads reviewer identity any more |
| `[REC]` five plan-review sections owe three basis fields | doubly dead: `test_lifecycle_contract.py` does not resolve, **and** both plans it named (`comprehension-outlives-the-artifact`, `ceremony-as-code`) are archived, which the row itself said would clear it |
| `[REC-3]` transition-lint | removed at C5 |
| the review-allocation pilot, built but never switched on | the Maintainer ended the pilot window during this sweep; the machinery and `test_pilot_evidence.py` went with C5, so both remaining acts have no subject |

The seventh, the AST-attestation re-anchor after the tag pass, was marked
**CLOSED 2026-08-20** and needed no disposition. *(A different AST re-anchor is
owed for this sweep's own changes; it is not this row.)*

**Two rows were corrected rather than transcribed, both because the sweep moved
the facts under them:**

* **The loop-fidelity gate's live instance is gone.** The row's sharpest claim
  was *"there is at least one live instance today"* -- `templates/core/AGENTS.md`
  citing `bootstrap/fidelity-check.md`. C2's constitution rewrite removed that
  citation, verified 2026-08-27, so the gap is latent rather than shipping. The
  gap itself is unchanged: `_CAIRN_INTERNAL_PREFIXES` is still `('doctrine/',)`.
* **The interpreter-binding re-pin's tier question outlived its pin.** The row
  asked whether an implementing agent could re-derive symbol digests over a
  high-risk surface. **The digests no longer exist** --
  `_INTERPRETER_SYMBOL_DIGESTS` has zero hits tree-wide, deleted with its host
  test module at C6 -- and what guards the trust root now is behavioural, in
  `test_session_kernel.py` and `test_session_failsafe.py`. That is arguably
  better coverage and certainly different, so the register carries the live
  question in its new form: whether a declared executable trust root should
  carry a byte-level pin at all.

**Net for `dev/PLANNING.md` across both passes: 2,591 -> 860 lines.**

### Scope delta -- the checker de-scope narrows to one directive family

**Accepted outcome (build table):** *"an archived file draws no flag; prose
files carry zero checker boilerplate; success is silent."* The middle clause is
delivered for one of the two directive families and **not** the other. That is a
scope reduction, so it is declared here with the Maintainer's allowance rather
than absorbed.

**What changes.** `claim-check-allow` -- 45 active directives, path lists with no
reason text -- moves into a config, and Cairn's prose files carry none.
`cairn-internal-ref-allow` -- 40 active directives -- **stays as per-file
comments**.

**Why, measured.** The two families look alike and are not. The
`cairn-internal-ref-allow` directives are **19 distinct path sets across 40
files**: each names which doctrine pages *that specific shipped template*
deliberately cites. Centralizing them either preserves all 40 lists in a config,
which moves the declaration away from the thing it describes, or collapses them
to a blanket *"`doctrine/` is fine everywhere"* -- and since `doctrine/` is the
**only** entry in `check_cairn`'s `_CAIRN_INTERNAL_PREFIXES`, the blanket form
turns that check into a no-op that still reports success.

**The evidence is from this sweep, not a hypothetical.** Four of those
directives named `doctrine/fold-back.md`. C6 deleted that file, and nine live
shipped surfaces were still citing it. They were findable *because the
directives named the file*; a blanket prefix exemption would have hidden all
thirteen citations with no trace.

**Maintainer allowance, verbatim** -- given after the choice and its cost were
put plainly:

> "Okay, I accept this."

**What the narrowing does not waive.** Boilerplate must not creep back into the
family that was cleaned: Cairn's own prose carrying zero `claim-check-allow`
directives is pinned by a test, not by habit.

### Archived records are read, never enforced -- Maintainer principle, 2026-08-27

The checker de-scope's first change made `claim_check` skip archived sources.
The Maintainer ratified it and stated the principle it follows from, verbatim:

> "Archived files are historical record and should never be scanned for the
> intent of fixing them. It's fine to scan to read history, but they shouldn't
> have enforcement--that was done (to the state that existed at the time)
> during their active phases."

This settles more than the one change. **Enforcement is bound to an artifact's
active phase**, so a checker finding on an archived record is a finding nobody
may act on: the record is append-only and the tree it described is gone. The
`--include-archives` escape hatch is therefore correctly *read-only in intent*
-- it exists so someone can inspect history, not so a gate can hold archives
green. Any future check that walks `dev/**/archive/` inherits this: it may
report, it may not enforce.

## Acceptance criteria

Per chunk, and each falsifiable.

* **C1** — the extracted module passes the trust-root tests; every call site
  resolves through it; `AGENTS.md`'s high-risk-surface entry names the new
  location. **Falsifier**: a bad binding (non-absolute, symlinked, non-executable,
  schema-invalid) is still rejected, from the new home.
* **C2** — the four self-hosted documents and their shipped twins land at their
  honest size (see the C2 deviation above; the `~80` target was unreachable).
  **Falsifier**: no governing document references a tool this sweep removes.
  **Satisfied 2026-08-26** — a grep over all six governing documents for
  `lifecycle_planner`, `lifecycle_metrics`, `transition_lint`, `suite_cost`,
  `onboarding_activate` and `tools/lifecycle.py` returns nothing. The hits this
  row used to enumerate by line are gone with the rewrite that removed them, so
  the line numbers are not restated: they would cite text that no longer
  exists, and a citation into a rewritten file is how a stale claim survives a
  correct change.
* **C3** — each tool's build-table probe passes: the reporter lists a
  known-closed change; the board view lists the active artifacts; the classifier
  re-derives the takeover table.
* **C4** — the plan-level Security Review is appended and clears, carrying an
  `**Obligation**: Internal Security Review` line, and it addresses **both**
  surfaces: the trust-root extraction and the registry-edit approach, the latter
  with security coverage proven **by set comparison, not byte identity**.
  **No C5 commit lands before it, and no C1 commit either.**
* **C5, C6** — suite green after each; each installed-source deletion is atomic
  with its registry row; a fresh scaffold is recorded green per commit. **The
  accepted set-comparison mechanics, carried in full rather than as a phrase**
  (Revision 1 §5): after each registry commit, the shipped verbatim Python
  surface **equals** `scan_targets()`'s derivation; a **positive-control
  mutation** — one unexpected shipped executable **must fail** the check —
  is recorded **once**; the **release scanner runs after each registry-removal
  commit**; and the canonical full suite plus the neutrality/redundancy pair run
  after the final install-contract commit. The Maintainer-run gate handling and
  the AST-baseline re-anchor **accompany the registry commits they belong to**,
  not a later phase.
* **C1** — every `skipif`-guarded loader of `lifecycle.py` is repointed at the
  kernel **in C1**, and each such test is shown *failing* against a tree without
  the kernel before it is called repointed. A test that skips is not a test that
  passes, and that distinction is what the first draft got wrong.
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

**Reconcile the SKIP count too, and reconcile it first.** A passed→skipped
transition leaves the collected total unchanged, so a reconciliation that
watches only passes is blind to exactly the failure this criterion exists to
catch. **Measured, not hypothetical:** C5's transition-lint removal moved
`test_lifecycle_vocabulary.py` from 30 passed to 30 skipped, and the chunk was
recorded as verified — its module guard required four paths to exist, one of
them the deleted lint, so an unrelated removal silently switched the file off.
Confirmed by running that file at `3b6f51e~1` in a throwaway worktree: 30
passed. Every Boundary B record now states passed **and** skipped, with any
movement in either named against the files that caused it.

**A guard that names more than its tests need converts an unrelated deletion
into invisible coverage loss.** When a removal makes a `skipif` fire, the
question is never "is the skip correct?" but "does this guard still describe
what these tests read?"

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
  need repointing; two need single-line edits. A further class of **installer
  tests references `tools/lifecycle.py` by path** and self-corrects only if the
  path still resolves — enumerate them in C1, not C6.

**`_has_symlink_component_below` and `_git_ok` are a code-span-boundary
correctness issue, not a coverage one.** They sit *inside* C5's removal span and
are called by surviving code, so the span's boundaries are wrong as drawn, not
merely under-tested. Fix the boundary; do not carve the functions out as an
afterthought.

## Implementation verification -- Claude -- 2026-08-27

**Boundary B mode**: full.

**Tested SHA**: `b1e655d` (C7's final implementation commit plus the Maintainer's
gate-manifest regeneration). **Interpreter**: Python 3.13.13, the canonical
binding at `dev/.cairn/local-env.json`. **Pre/post working-tree state**: clean
apart from two long-standing untracked files (`.claude/`,
`dev/measurement/collision_log.md`), neither read by the suite.

**Why full and not bounded.** This plan's own reviewed contract names C7 as a
full-run point, and the fence refuses bounded mode here on its own terms: the
work touches the **gate manifest** (a contract surface) and a **shipped checker**
(`claim_check.py`, both twins) on the path `check_cairn` walks tree-wide. No
bounding argument was attempted.

**Commands and outcomes**

```
CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0
  -> 2 failed, 3166 passed, 1 skipped   (560.26s / 9m20s)
python scripts/quality_gate.py --sub neutrality --sub redundancy
  -> neutrality fail=79 info=21 ; redundancy fail=0
python scripts/check_cairn.py
  -> 2 issues, both pre-existing in an open proposal's link targets
```

**Non-pass disposition**

* **Both failures are `test_ast_attest.py`** -- the AST baseline debt, **red at
  clean HEAD before any of this session's work** (established by stashing and
  re-running both suites, where `test_gate_manifest` passed and these two failed
  identically). Not caused here; owned by the separate Maintainer-run direct
  correction.
* **The five `test_gate_manifest` failures this work created are gone**, cleared
  by the Maintainer's regeneration. The delta was verified by set equality
  before and after: 178 -> 179 frozen files, **1 added** (the new config-guard
  test), **0 removed**, **2 changed** (the `claim_check.py` twins) -- exactly the
  predicted set.
* **The 1 skip is disposed, not observed** -- and it is a finding.
  `test_reference_scripts.py::TestMultiScriptModules` skips with *"got empty
  parameter set for (module_name)"*, because C6 emptied `_MULTI_SCRIPT_MODULES`
  when it deleted the fold-back ledger's two scripts. **Measured 2026-08-27:
  eight modules ship more than one verbatim `.py` today** -- `api-access-security`
  (5), `coordination-tiers` (9), `web-hosting-security` (5), `claim-check`,
  `content-security`, `doc-drift-prevention`, `issue-capture` (2 each) -- and
  this assertion now covers **none** of them. The sibling `_SCRIPT_MODULES` still
  carries one live entry, so only the multi-script leg went dark. Filed to the
  security strategy's register under [VER-5]; **not fixed here**, because
  repopulating it is new test coverage rather than sweep work.

**Known omissions.** The AST baseline correction is prepared and dry-run
verified but not applied -- it is the Maintainer's to run. Release verification
is a separate ceremony and was not performed.

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

## C8 state, measured 2026-08-27 -- and the C9 ordering

**Three of C8's surfaces are already satisfied.** Measured, not assumed:

* **Gate manifest** -- `_gate_manifest.py verify` reports *OK, gate integrity
  intact (179 frozen files, 3169 pinned nodes)*. Re-anchored by the Maintainer
  today; the AST baseline's change registers as `CASCADE-CHANGED`, which is the
  manifest correctly knowing that file moves under this ceremony.
* **Published `scaffold.py --manifest`** -- 88 manifest tests pass.
* **Fidelity / integrity** -- 108 tests across the lockfile, fidelity and
  `verify_integrity` suites pass.

**Two things remain, and the first is blocked on a row this sweep filed.**

**(a) CORRECTED 2026-08-27 by the C1 code review -- the lockfile gap is larger
and different, and the executable trust root is inside it.** What follows the
correction is the original measurement, kept because the error is instructive.

**The correction.** The three hash mismatches below were real and the Maintainer
fixed them at `610f521`. But that measurement **filtered out every record whose
file no longer exists** -- it skipped a record when the path was absent, so it
measured the intersection of lockfile and disk and reported it as the whole.
Re-measured without that filter:

* **14 verbatim records name files that no longer exist**, including
  `tools/lifecycle.py` itself, both fold-back scripts, and the nine
  `tools/_lifecycle_metrics/` modules.
* **`tools/session.py` and `tools/board.py` have no lockfile record at all.**
  C1 added their mappings; the lockfile writer was never re-run, because it
  cannot be ([TRU-1]).

**The security consequence, which is the reason this is blocking rather than
tidy-up.** `tools/lifecycle.py` carried a `verbatim: true` record, so
`bootstrap/verify_integrity.py` hashed the file holding the local interpreter
binding. `tools/session.py` carries none. **The executable trust root
`AGENTS.md` names under High-risk surfaces moved out of install-integrity
coverage in C1, and nothing reddened**, because the integrity check can only
verify records that exist.

This escalates [TRU-1] from an operational annoyance to a security finding: the
absent regeneration command is now demonstrated to have dropped a trust root
from coverage silently. C8's lockfile leg is therefore **not** three digests --
it is 14 removals plus 2 additions, and it should be done before C9 carries this
lockfile into two live research repositories.

*Original measurement, superseded:*

**Three verbatim lockfile records disagree with disk.** The raw count of
records diverging is 19, and **that number is misleading**: 16 are substituted
or living-state files an adopter is *expected* to edit. Restricted to
`verbatim` records, where byte-identity is the contract, it is **three**:

| record | changed by |
|---|---|
| `scripts/claim_check.py` | the checker de-scope (C7) |
| `tools/evolution_infer.py` | C6 -- the fold-back retirement removed its backlog half |
| `tools/prune_reflections.py` | C6 |

**The blocker is [TRU-1] in the security strategy's register, filed this
morning**: *there is no command that regenerates an existing lockfile.*
`scaffold.py upgrade --init-lock` is the only writer and refuses when the file
is present, and the test that states the rule says the lockfile is *"regenerated,
never hand-edited"* -- naming a procedure that does not exist. So this leg needs
the same purpose-built, dry-run-verified correction the Maintainer ran at
`77d2b3b`, and it is the second time that gap has cost a ceremony. That is the
argument for closing [TRU-1] rather than routing around it a third time.

**(b) The gate anchor has not moved.** `refs/cairn/gate-anchor` is at `5f99273`,
**343 commits behind `HEAD`**. This is the two-stage signing ceremony in
`REANCHOR_RUNBOOK.md`, and it walks into the register's [TRU-4] row: the
*controlled* path refuses unless the differential oracle has run, which happens
only during an engine refactor, so the **establishment** path -- documented as
*"supervised, one-time"* -- is the only one available. It would be its **fourth**
use. Do not close that by configuring a baseline to satisfy the check; that
declares a refactor that did not happen, on a trust root.

**C9 runs after code review** *(Maintainer, 2026-08-27)*. The sister migrations
carry Cairn's changes into two live research repositories, so they should not
begin until the code review this plan requires has run and its findings are
answered. This ordering is recorded here because the chunk table's C8-then-C9
sequence did not say where review sat.

## Response to code review -- Claude (Author) -- 2026-08-27

Four Internal code reviews ran in independent fresh contexts, one per chunk
group, each author committing its own review under `dev/reviews/`. **I did not
write them and could not**: this plan sets its floor at *a same-type agent in an
independent context, not the implementing agent*, and I am the implementer.

| group | verdict | blocking | non-blocking |
|---|---|---:|---:|
| C1 -- session kernel | **BLOCK** | 2 | 6 |
| C2+C3 -- constitution, tools | ACCEPT-WITH-FOLLOWUPS | 2 | 5 |
| C5+C6 -- the removals | ACCEPT-WITH-FOLLOWUPS | 3 | 6 |
| C7 -- prose phase | ACCEPT-WITH-FOLLOWUPS | 0 | 2 |

**Fixed in this response**

* **The plan template had silently lost the archive-precondition doctrine.**
  Neither `dev/plans/_template.md` nor its shipped twin mentioned `Dispositions`,
  the four-verb vocabulary, the batching rule, or the append-re-opens-the-
  attestation rule -- while `doctrine/plans.md` still carried all of it and C6
  had deleted the parser that used to check it. Proven by my own behaviour: I
  wrote this plan's Dispositions block from doctrine and archived plans, because
  the template offered nothing. Restored to both twins, with the enforcement
  reality stated plainly -- nothing mechanical checks it; a reviewer at
  archive-preparation is the enforcer.
* **The session kernel cited a deleted test file as the sole guard on a
  deliberate duplication**, at two sites, in a file that installs verbatim into
  every adopter tree. `claim_check` cannot see this class -- the reviewer
  control-tested a planted broken path in a `.py` docstring and it returns OK.
  Both sites now name `test_session_kernel.py`'s `TestDirectionalDriftGuard`,
  where the oracle actually moved. Twins re-verified byte-identical.
* **A deliberately-kept behaviour had lost its only positive pin.** The standing
  capture prompt survived the fold-back ledger's retirement on purpose; the test
  asserting it *fires* did not, leaving only a negative twin that passes equally
  well when the behaviour is gone. Restored as
  `test_session_end_WITH_handoff_DOES_emit_the_standing_capture_prompt`.
  **Control-tested, and the first control was wrong**: deleting the emit from
  `tools/session.py` left the test green, because the suite loads the *shipped
  twin*. Re-probed against the file actually under test, it fails as it must.
* **`dev/agent_collaboration.md` had dropped the work-intent protocol entirely**
  while the mechanism runs on every commit -- the pre-commit hook fired
  throughout this session. Restored as a pointer to
  `dev/modules/coordination-tiers.md`, stating that the check is advisory and
  never blocks, and that it earns its place on a shared worktree and not on
  worktree-per-agent.
* **A doctrine link pointed at the wrong file.** `doctrine/session-routines.md`
  carried `[lifecycle-metrics](../README.md)` -- a label naming a deleted module,
  a target that never mentions it, and a link both checkers pass because the
  target resolves. The paragraph now states the tracker schema as a standing
  contract that outlives the tool, which is what was actually true.
* **The C7 fold's bookkeeping now reconstructs without re-derivation** -- a
  row-by-row mapping table replaces counts a reader had to re-derive to check.
* **The guard written this morning caught its first real case**: the C1 reviewer
  opened its own review with an inline `claim-check-allow` directive. Moved to
  the config, which is the remedy the guard's failure message names.

**Corrected, not fixed: my C8 lockfile measurement was wrong.** I reported three
stale verbatim records. The C1 and C5+C6 reviewers independently found the real
shape, and the reason mine was wrong is instructive -- **my script skipped any
record whose file no longer exists**, so it measured the intersection of lockfile
and disk and reported it as the whole. The true state is **14-19 verbatim
records naming deleted files, zero hash mismatches** (the Maintainer's `610f521`
closed those), **and `tools/session.py` and `tools/board.py` recorded nowhere**.
`bootstrap/verify_integrity.py --target .` refuses on Cairn's own tree today.
The security consequence is the finding: `tools/lifecycle.py` carried a
`verbatim` record, so the file holding the interpreter trust root was hashed;
`tools/session.py` carries none, so **C1 moved a declared executable trust root
out of install-integrity coverage and nothing reddened**. The C8 section above
carries the correction; the repair is C8 ceremony work.

**Accepted and not actioned here**, each with a reason rather than a shrug:

* **C1's acceptance criterion is unmet and the deviation was never declared.**
  Two suites guarded on `lifecycle.py` were repointed in C6, not C1, and the
  "shown failing against a tree without the kernel" evidence appears in no
  record. The reviewer ran the missing demonstration and **it passes** -- the
  property holds, it was simply never shown. Declared here as the deviation it
  is, rather than back-dated.
* **No Boundary B record exists for C1, C5 or C6** -- only C7's. The plan asks
  one per chunk. Reconstructing them now would be writing evidence after the
  fact for runs nobody made; the honest disposition is that the sweep ran one
  integration boundary at the end, and that is what the record shows.
* The remaining non-blocking findings -- inert `skipif` guards, residual
  naming, untested `main()` entry points, orphaned `.gitignore` rules -- are
  real and none is load-bearing. They belong to the follow-up work the
  Dispositions block batches, not to this response.

### Authority closure cleared -- and the freeze that follows from it

**External Security Review, 2026-08-27, `048962f`: ADMIT IN PART.** All three
changed closure members admitted --
`bootstrap/tests/_gate_manifest.py` (inert or strictly narrowing),
`bootstrap/REANCHOR_RUNBOOK.md` (prose, exemption scope verified with a
positive control), `bootstrap/reanchor.sh` (purely additive refusal and
`printf` changes; the two-stage boundary untouched, and it contains no
ref-moving code at all). What carries the verdict is that **the other seven
closure members are byte-identical to the anchor**: the code that decides what
may be blessed did not change.

**What was refused is not a file.** The end-to-end stage-1 -> stage-2 handoff
rests on the *instantiated* launcher, which is outside the closure, changed
since the anchor, and unreviewed. A separate review of
`bootstrap/reanchor-launcher.template.sh` is running.

**THE CONSTRAINT, and it binds any session that picks this up:** this review
clears **content digests, not a ref**. Verified at `048962f`, the three files
still hash to exactly the reviewed values. **Editing any of them voids the
clearance and the review must be redone.** So the ceremony's remaining findings
are *"fix before the NEXT ceremony"*, not before this one:

| id | what | why it waits |
|---|---|---|
| R-1 | the runbook prints `reanchor.sh stage2 ...` then claims stage 2 "re-extracts and re-verifies its own bytes" -- **false for that invocation**; re-extraction is the launcher's `--stage2` property | editing the runbook voids its clearance |
| M-1 | the `expect` beside the fixed gate command still says "0 skipped"; a real run reports 1 -- the same `TestMultiScriptModules` empty-parametrize defect filed independently under [VER-5] | same |
| S-1 | the new precheck runs two values-file executables before the disclosure print its own comment says must come first | same |
| S-3 | the printed stage-2 command is built from unquoted environment values | same |
| S-2 | two of four claimed precheck test nodes are **vacuous** -- they exercise `validate`, which never runs the precheck, while their docstrings assert the opposite | a test-only fix, but it lives in the same closure |

**R-1 is the one that reached a person.** That exact command and that exact
false claim had already been relayed to the Maintainer as ceremony
instructions, from the runbook, unverified. The defect predates the anchor; the
propagation did not.

**Process note, recorded because it cost the reviewer real work.** `HEAD` moved
**five times** during that review and one of the moving commits edited a file in
its scope. The reviewer handled it correctly -- re-deriving against each later
commit and pinning content digests rather than a ref -- but the fix is upstream:
**do not commit into a running review's scope.** The reviewer also corrected
itself mid-review on a load-bearing point: a transition manifest must name **all
ten** closure members, not only the three that changed, or `revalidate_transition`
refuses it as "not the authority closure."

## Response to External Security Review (Codex) -- Claude (Author) -- 2026-08-27

**Verdict accepted in full: BLOCK.** Seven blocking findings, two CRITICAL, each
**reproduced** by the reviewer rather than argued. The runner now refuses on
entry, in code, citing the review. `dev/reviews/2026-08-27-external-security-review-correct-pinned-digests.md`.

**The claim I made was wrong, and precisely wrong.** I wrote that the checksum
"is not theatre" because the two digests are separated in time. The reviewer's
correction is exact: the A/B comparison is real but detects a mutation **only
where that mutation changes the plan's projection**. They built two lockfile
states with the same record count and the same add/remove set, changed a *kept*
record's hash and a top-level field between derivations, and got **identical
digests** -- then apply wrote both unauthorized values. The same holds for the
baseline. A count is not a preimage, and I shipped a count.

**The finding that reaches work already applied: CPD-5, provenance.** The runner
derives a symbol's commit with `git log -1 -S <name>`. Pickaxe `-S` finds a
commit that changes the *count* of a string -- usually the symbol's
introduction, not the later change that altered its digest. Verified
independently: for `FunctionDef:_compute_upgrade` it returns `ed5a670`
(**2026-06-10**), while the commit that actually touched `upgrade.py` between
the baseline anchor and HEAD is `bec2cca` (**2026-08-25**).

**So the evidence shown to the Maintainer for the 15-symbol correction at
`d283589` was misattributed.** The rendered line said *"Read those commit
subjects: they are what you are authorizing"*, and some of those subjects were
the wrong commits.

**What was NOT wrong, stated precisely so this is neither overstated nor
minimised:** the digests themselves came from the tree and are correct; the
docstring-only / substantive determination came from an AST comparison and is
correct; the baseline count was unchanged. The correction is sound. **The
provenance displayed beside it was not.** Re-derived conservatively by file
history over `77d2b3b..HEAD`, every corrected symbol traces to landed sweep
work -- C1, C6, `adopt-into-existing-tree`, `metrics-events-not-prose`,
`scaffold: retire the events.py InstallSpec`. Nothing unauthorized was
attested; the operator was simply pointed at the wrong subjects while
authorizing the right change.

**Also accepted, not yet fixed** -- these are the redesign, and it is not a
patch: `--authorize` lets any process perform the purported human act, and
removing the flag would not help because an agent can allocate a pseudo-terminal
(CPD-1); candidate engine code executes before authorization and is reused from
`sys.modules` across both derivations, so A and B can be aliases (CPD-3); writes
follow symlinks and can leave partial invalid JSON, which falsifies the test
module's own total-write claim (CPD-4); the known-new complete-set guard the AST
runbook requires is silently dropped (CPD-6); and `_tracked()` collapses every
git error into "untracked", turning a failure into permission to delete a
lockfile record (CPD-7).

**On the test suite, which the reviewer assessed fairly.** The moving-plan test
is honest within its model and its control does real work -- but both plans are
injected dictionaries and both applies are lambdas. No test derives twice from
changing real inputs, writes a scratch artifact, injects a write failure, or
swaps a symlink. **The suite pinned the design's story, not its behaviour.**

**Disposition: the runner stays blocked and is not being quietly patched.** The
review's final section is a redesign -- closed JSON-native plan binding exact
input and output bytes, re-derivation in a fresh process from verified checker
bytes, exact-preimage compare-and-swap, atomic contained writes with read-back.
That is a proposal's worth of work on a trust surface. Rewriting it immediately
and handing it back would repeat exactly the pattern the Maintainer named this
morning: an agent produces machinery the operator cannot independently check.

**Until it lands, the two corrections are done by hand under their runbooks** --
which is where they were, and is honest about what it costs.

## Dispositions

*Drafted 2026-08-27, before archive, so the archive precondition is satisfiable
rather than assembled under time pressure. **Not final**: the `defer` batch at
the bottom needs the Maintainer's authorization, and C8/C9 are unexecuted, so
this block is revised once more before the plan moves to `ready-to-archive`.*

`Dispositions:` accept x13, guard x2, defer x5 (**unauthorized -- batched
below**), wontfix x0.

### accept -- landed in scope, with the authorization where one was needed

1. **Scope delta: the lifecycle-metrics module is removed** (C6), recorded at
   its own scope-delta section above.
2. **Scope delta: the review-allocation pilot window ends.** Authorized:
   *"Yes, please end the pilot window now"*.
3. **Scope delta: the suite-run ledger is removed** (C5).
4. **Scope delta: the checker de-scope narrows to `claim-check-allow` only,
   leaving `cairn-internal-ref-allow` as per-file directives.** Authorized:
   *"Okay, I accept this."* The measurement behind it is in that section.
5. **C2 deviation: the ~80-line template target is not reachable**, recorded
   with its measurement rather than silently missed.
6. **C4's fence disposition**, recorded before any removal landed.
7. **The interpreter trust root moves to the session kernel.** Authorized:
   *"Yes, move the interpreter trust root as needed"*.
8. **`dev/PLANNING.md`'s bankruptcy, both passes** -- 2,591 to 869 lines. Every
   removed row is either folded into the security strategy's Live residual
   register or on this plan's dead lists with the measurement that showed its
   subject gone.
9. **Reviewer independence becomes doctrinal-only, and the identity roster is
   deleted.** A Maintainer Decision, quoted verbatim in the strategy's [REC-1]
   entry; no mechanical successor is owed.
10. **Archived records are read, never enforced** -- a Maintainer principle,
    quoted verbatim above, now binding on any check that walks
    `dev/**/archive/`.
11. **Thirteen shipped citations to the deleted fold-back doctrine repaired**,
    and the four exemption directives that were suppressing them corrected.
12. **`docs/tool-usage.md`, three onboarding templates and their twins
    repointed** off tools the sweep removed.
13. **The loop-fidelity widening count corrected and deflated** -- 128 to 99 to
    smaller again, with the record now saying the shape is the finding and the
    number is not.

### guard -- homed in something that executes, and names the node

1. **Boilerplate must not creep back into the cleaned directive family** --
   `guard (bootstrap/tests/test_claim_check_allow_config.py::TestProseCarriesNoClaimCheckDirective::test_no_live_markdown_declares_an_inline_directive)`.
   Control-tested: planting a directive fails it.
2. **The exemption config must stay load-bearing, and must fail toward strict**
   -- `guard (bootstrap/tests/test_claim_check_allow_config.py::TestTheConfigIsWhereExemptionsLive::test_a_configured_document_is_clean_and_is_not_clean_without_it)`.
   Asserted against a document chosen at runtime from the config itself, so it
   cannot pass by naming a file whose exemptions went away.

### defer -- REQUESTED AS ONE BATCH, NOT YET AUTHORIZED

**These five are deposits, and a deposit is a scope decision.** Doctrine
requires the Maintainer's authorization quoted verbatim, presented as one batch
so the gate stays affordable. Nothing below is self-authorized; each names where
it already sits, so the deposit is inspectable before it is allowed.

1. **[VER-5] The multi-script install assertion covers nothing.** C6 emptied
   `_MULTI_SCRIPT_MODULES`; eight modules ship more than one verbatim `.py`
   today and the assertion covers none. Homed in the strategy register.
   *Why deferred:* repopulating it is new test coverage, not sweep work.
2. **[TRU-4] A symbol parked in known-new is invisible to the AST gate**, and 15
   are currently rekeyed, several on trust surfaces. All trace to reviewed work.
   Homed in the strategy register. *Why deferred:* the fix is a decision about
   whether long-lived known-new entries graduate into the baseline, which
   belongs to the next re-anchor.
3. **The `first-foldback-candidate` onboarding trigger cannot fire.**
   `_foldback_has_open_candidate` in `scripts/_onboarding/triggers.py` reads a
   ledger path C6 removed. *Why deferred:* it is downstream of the pending
   onboarding decision, and rewriting those steps before that decision would
   likely be thrown away.
4. **C6's two onboarding findings** -- `assert_always_on_complete` loses its
   subject, and the side-door parity property loses its category. Measured in a
   throwaway worktree and recorded in the C6 onboarding section above. *Why
   deferred:* both are decisions, not chores, and `_ALWAYS_ON_MAPPINGS` is
   MAINTAINER-GATED.
5. **The 20 queued rows drafted into 4 forge issues, unfiled.** Drafts in
   `dev/measurement/queued-issue-drafts.md`. *Why deferred:* filing is
   outward-facing and yours.

### Still owed before this plan can archive

Not dispositions -- outstanding work, listed so this block is not mistaken for
completeness. **C8** (the install contract's remaining surfaces, and the gate
anchor, which sits 343 commits behind `HEAD`), **C9** (both sister migrations),
and the **code review** this plan's own text requires: *a same-type agent in an
independent context, not the implementing agent*, one round per chunk group.
Zero rounds have run; relaxing that floor is the Maintainer's call, not the
author's.

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

## Plan review -- Claude Sonnet 5 (Internal, fresh context) -- 2026-08-25

**Reviewed commit**: 7dc66a10fb668b54c67782cfd544139ead70b939
**Target**: the complete plan (header through "Lasting-truth migration"),
cross-checked against `tools/lifecycle.py` and its twin
`templates/skills/_lib/lifecycle.py`; `bootstrap/tests/conftest.py`;
`tools/suite_cost.py`; `bootstrap/tests/test_suite_ledger.py`; all nine
`bootstrap/tests/test_lifecycle_*.py` files plus `test_pilot_evidence.py`,
`test_byline_identity.py`, `test_doctrine_vocabulary_drift.py`,
`test_scope_reduction_trap.py`, `test_skills_self_heal.py`;
`templates/modules/default-on/lifecycle_metrics.py` and its
`_lifecycle_metrics/` engine package; `bootstrap/_scaffold/config.py`;
`bootstrap/tests/_ast_attest.py`; both `session-start`/`session-end`
`SKILL.md` pairs; against the accepted source proposal's Revision 1 and its
Decision.
**Prior findings**: the `## Plan review -- Claude Sonnet 5 -- 2026-08-25`
Security Review pass immediately above this one. I reached the findings below
independently -- the deletion-manifest trace in Finding 1 was already
complete before I read that section -- and note the overlap and the division
of labor explicitly rather than re-deriving or restating its analysis.
**Assurance path**: high-assurance (inherited from the source proposal's
header; the sweep touches the install contract and deletes ~55k lines)

**Obligation**: Internal
**Tier**: Internal
**Model**: Claude Sonnet 5
**Findings**: raised -- 2 blocking, 3 non-blocking notes

**Verdict: REVISE.** My mandate is the deletion manifest itself: "every file
... authored in the derived plan," per the accepted proposal's Revision 1 §1,
checked at this review because it is "the last point at which the deletion
inventory is inspectable while the thing being deleted still exists" (the
Decision). Both blocking findings below are failures of that mandate rather
than of any one chunk's design: a load-bearing production dependency the
manifest never names (converging, from the manifest side, on the same fact
the concurrent Security Review pass found from the security side), and two
removal rows -- the suite-run ledger (C5) and the whole of C6's order-5 row
-- that give only aggregate totals rather than the file-by-file account the
Decision required.

### Steelman

* C1's citations are exact: `_has_symlink_component` at `tools/lifecycle.py:431`,
  `_probe_interpreter` at `:457`, `_resolve_interpreter` at `:474`, all inside
  the cited `431-579` range; the three call sites `:307`, `:894`, `:1395` all
  resolve to `_resolve_interpreter(...)` calls, confirmed by direct grep.
* The transition-lint file/line trio in C5 is exact: `scripts/transition_lint.py`
  is 923 lines, `scripts/transition_lint_whitelist.py` is 46,
  `bootstrap/tests/test_transition_lint.py` is 1,486 -- all three match the
  plan's citation to the line.
* `_ALWAYS_ON_MAPPINGS` at `config.py:689-708` (exact) really is absent from
  `_ast_attest._UPDATE_ALLOWLIST` (`:142-147`, which holds only
  `_MODULE_MAPPINGS`, `_SKILLS_MAPPINGS`, `_CORE_MAPPINGS`,
  `install_onboarding`) -- the MAINTAINER-GATED fence is placed correctly.
* The three struck rows are correctly disposed. I ran the grep myself (see
  "Verified negatives" below) after first confirming the instrument on a
  known-present pattern, per `AGENTS.md`'s "confirm the instrument before
  trusting an absence" -- "slot ratchet" and "attic notes pointing into git
  history" both return zero identifier/file hits beyond the plan's own prose
  and the two known upstream mentions (proposal §4, strategy note), and
  `link-check-allow` is confirmed real, live, and genuinely unaddressed by
  the accepted claim/link de-scope design.
* The order-4/order-5 double-count arithmetic is internally consistent:
  `2 x ~1,440 (the pilot/monitoring span, both copies) + 1,437
  (test_pilot_evidence.py, counted once under each row) = ~4,317`, matching
  the plan's stated "~4,300."
* The first two items of "Tests needing rehoming, not deletion"
  (`TestVocabularyLoader`, the twin-identity test) are real: I confirmed
  `_declared_assurance`/`_build_closeout`/`cmd_review_brief` all sit outside
  C5's pilot/monitoring span and all call into the vocabulary loader, and
  that `test_the_two_lifecycle_copies_are_byte_identical` is exactly where
  the plan cites it (`test_pilot_evidence.py:1173`).

### Finding 1 (blocking) -- the manifest omits the one dependency that makes C6 an outage, not a deletion; independently reached, and it converges with the concurrent Security Review's Finding 1

Before reading the Security Review section above, I traced C1's own three
call-site citations (`:307`, `:894`, `:1395`) into their enclosing functions
and found: `:307` sits inside an early helper, `:894` sits inside
`cmd_session_start` (`tools/lifecycle.py:825-911`), and `:1395` sits inside
`_do_full_handoff`, called from `cmd_session_end` (`:1332-1446`). Both
`cmd_session_start` and `cmd_session_end` are the **entire mechanized
content** of `.agents/skills/session-start/SKILL.md` step 1
(`python tools/lifecycle.py session-start`, `:19`) and
`.agents/skills/session-end/SKILL.md` step 1
(`python tools/lifecycle.py session-end $ARGUMENTS`, `:19`) -- I confirmed
both shipped twins (`templates/skills/session-start/SKILL.md`,
`templates/skills/session-end/SKILL.md`) are byte-identical to the
self-hosted copies (`diff -q`, no output). `cmd_session_start` also performs
`_heal_skills_fanout` (defined `:785`, called `:850`) -- the mechanism this
very harness's own `CLAUDE.md` names as the reason "session-start self-heals
a `.claude/skills` symlink so this harness surfaces them as slash commands."
C6 removes `tools/lifecycle.py` and its twin to zero (the plan's own
double-count arithmetic says so: "C6 ... removes all 3,910 of each"), and I
grepped the plan, the source proposal, and the strategy note's build table
for `session-start`, `session-end` as a lifecycle-CLI subcommand, and
`_heal_skills_fanout`: **zero hits** in any of the three. Neither C2 (whose
touched-file list is `AGENTS.md`, `dev/agent_collaboration.md`, both
`_template.md` files, and their four shipped twins -- not either `SKILL.md`)
nor C3 (three small tools, none of which orchestrate session-start/end or
perform the fan-out self-heal) nor any other chunk names a replacement.

I will not re-derive the Security Review pass's fuller treatment of this same
fact (the missing `_warn_stale_once` fourth trust-root symbol, and
`test_skills_security.py`/`security_manifest.py`'s `SECURITY_FAMILY` going
silent-by-skip rather than red) -- it is thorough and I have nothing to add
to it on the security axis. What I add, from the manifest side: this is not
an isolated corner of `lifecycle.py`. `cmd_session_end` is also the one
production caller of the foldback-surfacing check the plan's own C6 row
deletes elsewhere (`bootstrap/tests/test_lifecycle_cli.py:379-420`,
`test_handoff_surfaces_foldback_candidates` /
`test_session_end_without_handoff_does_NOT_surface_foldback`, both exercising
`cmd_session_end`'s interaction with `scripts/foldback_suggest.py`) -- so the
session-start/session-end orchestration is entangled with at least two other
order-4/5 removals, not a self-contained thing a later chunk could patch in
isolation without re-deriving how it touches the rest of the sweep. Both
reviews independently landing on the same fact from different angles is not
redundant coverage; it is confirmation that this is a real hole and not an
artifact of either review's framing. **Same disposition as the Security
Review's Finding 1**: name the chunk that keeps or replaces this mechanism,
with its own registry-row/manifest bookkeeping, or record the Maintainer's
explicit allowance for losing it -- silence is not available under
`AGENTS.md`'s scope-floor rule.

### Finding 2 (blocking) -- the per-file manifest Revision 1 §1 requires is missing for the suite-run ledger (C5) and given only as an aggregate total for the whole of C6's order-5 row

**What the plan actually contains, by chunk.** C1 names three functions and
three call sites. C2 names four self-hosted documents, four shipped twins,
and a "known real hits" list of specific line numbers. C5's transition-lint
item names three files with exact line counts. Everything else in the
removal rows is a **total with no file list**: C5's "the suite-run ledger"
(part of the measured 7,240-7,450 row, no filename anywhere); C6's "lifecycle
CLI + planner + twins + 11 tests (36,332)," "onboarding (8,500-9,100)," and
"foldback (3,152)" -- three aggregate figures covering, by my estimate, on
the order of 48,000 lines, roughly 85% of the sweep's net removal, with not
one filename attached to any of the three beyond the phrase itself. I found
no companion manifest file anywhere in the tree (`find dev -iname
"*subtraction*"` returns only the plan and its source proposal) and no
per-file table in the plan document itself -- I read it in full. This is a
direct shortfall against Revision 1 §1's own words: "every file, the property
removed, its replacement or the explicit decision the property ends, its
registry row, its twins and tests, and its commit grouping" is authored **in
the plan**; a category total is not that.

**The suite-run ledger's actual files, traced independently (not named in
the plan, and unmentioned by the concurrent Security Review pass):**
`tools/suite_cost.py` (619 lines, unregistered in `bootstrap/_scaffold/config.py`
-- Cairn-internal, matching the "Cairn-internal removals" framing) and
`bootstrap/tests/test_suite_ledger.py` (1,394 lines, wholly about the
ledger). The third piece is the one that most needs a plan reviewer's eye:
`bootstrap/tests/conftest.py` carries a **~795-line block** (lines 535-1330,
"The suite-cost ledger" through "Durability," confirmed by reading the
file's own section markers) that must be deleted, immediately adjacent to
and interleaved with the `CAIRN_FULL_SUITE` gate rule / `--quality-gate-shuffle-seed`
flag / broad-run guard machinery (lines 204-533) that **this plan's own
mandated Boundary A/B verification command depends on** and that must not be
touched. Worse, `pytest_sessionfinish` itself (`:493-502`) is a **mixed
hook** that calls both `_release_mode_outcome_rule(...)` (must survive) and
`_ledger_step(_ledger_finish_session, ...)` (must go) in the same nine-line
function body -- exactly the "mixed files, per-function" granularity the
source proposal promised (Origin, item 1) but that this plan does not carry
through to this file. A file this central to the sweep's own verification
trustworthiness being entirely absent from the manifest is precisely the
"file nobody agreed to delete" the Decision was written to prevent.

**C6's "11 tests" cannot be fully reconstructed from the plan as written --
by either reviewer.** I independently identified 10 of the 11 wholly-dependent
test files with high confidence: `test_lifecycle_board.py` (1,885),
`test_lifecycle_brief.py` (1,170), `test_lifecycle_cli.py` (684),
`test_lifecycle_contract.py` (6,983), `test_lifecycle_failsafe.py` (538, and I
can now resolve the concurrent Security Review's open question about this
file -- yes, it is wholly dependent, gated on `MODULE_PATH.exists()` where
`MODULE_PATH` is `lifecycle.py`, exactly like the other confirmed files),
`test_lifecycle_vocabulary.py` (1,037), `test_byline_identity.py` (685),
`test_doctrine_vocabulary_drift.py` (216), `test_scope_reduction_trap.py`
(694), and `test_skills_self_heal.py` (224 -- purely about
`_heal_skills_fanout`/`session-start`, and not found by the Security Review
pass either). Together with `test_pilot_evidence.py` (1,437, the
double-counted file) that is 11 files summing to 15,553 lines, against the
15,806 the "36,332 across 15 files" figure implies once the 20,526-line
source total (`lifecycle.py` + twin + `lifecycle_planner.py` + twin) is
subtracted -- a 253-line (1.6%) gap I could not close in the time available.
Three of the nine files that **do** match the `test_lifecycle_*` naming
pattern are false positives for a name-based search: `test_lifecycle_metrics_events.py`
(560), `test_lifecycle_metrics_config.py` (266), and
`test_lifecycle_stage_patterns.py` (753) all test the separate, surviving
`lifecycle-metrics` module (`templates/modules/default-on/lifecycle_metrics.py`
plus its `_lifecycle_metrics/` engine package, ~4,383 lines per copy, itself
never named as touched or as "not touched" anywhere in the plan). This is
exactly the hazard the plan's own prose warns about for the *missing* six
files ("would be invisible to a name-based search") -- but it cuts the other
way too, and two structurally-independent reviewers working the same
question in parallel still could not fully close it. That is the strongest
evidence I have that the manifest, not the prose, is where this plan
currently falls short.

**`bootstrap/_scaffold/config.py`'s foldback/onboarding registrations
inherit the same problem.** A repo-wide grep for "foldback" returns 27 files,
spanning the intent system (`tools/_intent/cli.py`, `tools/_intent/conflict.py`
-- explicitly "not touched"), `scripts/claim_check.py` (explicitly "kept and
de-scoped," not deleted), and other clearly-surviving surfaces alongside the
actual foldback-ledger files (`scripts/foldback_suggest.py`,
`scripts/foldback_export_scan.py`, and their dedicated tests). A name-based
approach cannot safely separate these without the plan doing that work once,
in the manifest, the way C1 and C2 already do for their own chunks.

### Note 1 (non-blocking) -- "Tests needing rehoming, not deletion" undersells its own third and fourth bullets: this is a code-span-boundary correctness issue, not only a test-coverage one

`_has_symlink_component_below` (`lifecycle.py:1846-1870`) and `_git_ok`
(`:1999-2011`) are function **definitions**, not just tested behaviour,
physically inside the ~1,440-line span C5 is scoped to delete. `_git_ok` is
called from `_artifact_path` (`:3029`) via `_has_symlink_component_below`'s
own call at `:3077`, and `_artifact_path` is what `cmd_review_brief` and
`cmd_closeout` -- both outside C5's span, both surviving until C6 -- resolve
artifact paths through. If C5's implementation deletes the literal span
containing these two function bodies, the very next `session-end --handoff`
or `review-brief` invocation between C5 and C6 landing raises a
`NameError`, not a quiet coverage loss. The plan should say explicitly that
C5's actual deletion boundary carves these two functions (not just their
tests) out of whatever it deletes; "rehome the tests" is necessary but not
sufficient if the code under test also has to keep existing.

### Note 2 (non-blocking) -- link-check-allow's fold-in doesn't carry forward its own falsifiers

The disposition (C7 folds `link-check-allow` into the same rule as the other
two directive families) is correctly scoped -- I confirmed it is real and
live (`scripts/link_check.py`, `scripts/check_cairn.py`,
`templates/modules/team-gated/link_check.py`,
`bootstrap/tests/test_link_check_exclusions.py`) and genuinely unaddressed by
the accepted claim/link de-scope design (Revision 1 §4 never names it). But
Revision 1 §4's four falsifiers for the chosen design (a broken live path
still fails; an archived artifact is excluded from bulk scans and labeled
informational on direct invocation; a legitimate exemption still works; an
exemption matching nothing draws a stale warning) are not restated for this
third family anywhere; C7's acceptance criteria say only "claim and link
gates pass ... success is silent," which does not by itself pin those four
behaviours for `link-check-allow` specifically.

### Note 3 (non-blocking) -- a class of installer/security tests referencing `tools/lifecycle.py` by path is unnamed, but self-correcting

`test_skills_install.py`, `test_skills_upgrade.py`, `test_security_check.py`,
`test_security_lint.py`, `test_skill_contract.py`, `test_security_stack.py`,
`test_first_session_report.py`, and `test_prune_tools.py` all assert on
`tools/lifecycle.py` as a registered/installed source (hash policy,
security-scan target membership, an exact-string invocation check). None is
named in the plan. Unlike Finding 2's items, this class is self-correcting:
C5/C6's own "suite green after each" criterion forces these assertions to
surface and be fixed the moment the owning registry row is removed, so it is
loud, not silent. Still worth a one-line mention in C6's acceptance criteria
so the implementer isn't surprised by which tests break on the first
registry-removal commit.

### Verified negatives (item 2 of my review brief)

Per `AGENTS.md`'s "confirm the instrument before trusting an absence," I
first ran the same grep shape against a pattern known to be present
(`cairn-internal-ref-allow`, 161 hits repo-wide) before trusting the negative
results below.

* **"slot ratchet" / "slot_ratchet"**: zero identifier or file hits anywhere
  in the tree. The only prose occurrences are the plan's own row, the
  proposal's §4, and the strategy note's build table row -- exactly the "two
  places" the plan states. Disposition (struck) confirmed correct.
* **"attic notes pointing into git history"**: zero identifiable file-set
  hits. Same two known prose-only occurrences (proposal, strategy note).
  Disposition (struck) confirmed correct.
* **`link-check-allow`**: real and live, ten files repo-wide including
  production code (see Note 2). Correctly identified as a genuine third
  directive family, correctly folded into C7's disposition (see Note 2 for
  the one gap in how it's folded in).

### What I could not reach

* I did not run any test, scan, or scaffold install -- there is no
  implementation yet to run against, and I was not asked to change code or
  fixtures.
* I did not close the final 253-line gap in the "36,332 across 15 files"
  reconstruction (Finding 2).
* I did not independently verify the "8,500-9,100" (onboarding) or "3,152"
  (foldback) figures at file granularity, for the reason given in Finding 2
  (a name-based approach cannot safely separate touched from untouched files
  sharing the same grep term).
* I did not review C7's prose-phase content, C8's install-contract ceremony
  mechanics, or C9's sister-migration discovery in depth, beyond confirming
  the fences (`_ALWAYS_ON_MAPPINGS`, the AST baseline, the gate anchor, both
  sister migrations) are stated at the point that binds and that I found
  nothing routing around them.

### Coverage

**Covered:** the full plan document; `tools/lifecycle.py` and its twin in
full (structurally, via section markers and targeted reads, not line-by-line);
`bootstrap/tests/conftest.py` in full; `tools/suite_cost.py`'s existence and
registration status; all thirteen candidate test files named in Findings 1-2
(existence, line count, and the specific path constant each loads);
`templates/modules/default-on/lifecycle_metrics.py` and its module doc;
`bootstrap/_scaffold/config.py`'s `_ALWAYS_ON_MAPPINGS` (`:689-708`) and
`_lifecycle-metrics`/`_onboarding` registrations; `bootstrap/tests/_ast_attest.py`'s
`_UPDATE_ALLOWLIST` (`:142-147`); both `session-start`/`session-end`
`SKILL.md` pairs in full, confirmed byte-identical; the accepted source
proposal's Revision 1 in full and its Decision.

**Not covered / low confidence:** the exact byte accounting behind "36,332
across 15 files" (253 lines unresolved); the "8,500-9,100" onboarding and
"3,152" foldback figures at file granularity; C7 through C9's content beyond
the fence-placement check above; whether the residual 253 lines belong to a
twelfth test file, to `conftest.py` fixtures shared across files, or to a
rounding/approximation in the plan's own "measured" figure (the plan's count
discipline treats chunk-size estimates as decision-irrelevant approximations,
so a small residual is not itself evidence of an error, only of an
incomplete reconstruction on my part).


## Response to plan review -- Claude (Author) -- 2026-08-25

Two passes, both **REVISE**: the Internal pass (`37d570d`) and the Internal
Security Review (`3ff6e4a`). They reached the same Finding 1 independently,
from different evidence, which is why it is treated below as established rather
than argued. Corrections are folded into the operative cells per this lane's
rule; this table points at them.

| # | Pass | Finding | Disposition | Where it landed |
|---|---|---|---|---|
| 1 | both | C6 deletes `cmd_session_start`, `cmd_session_end` and `_heal_skills_fanout`, which the kept SKILL.md files invoke by name; no replacement named | -> accept | C1 rewritten as **the session kernel** — new subsection "What C1 extracts, and why it is not just the trust root" |
| 2 | Security | C1's extraction range omitted `_warn_stale_once` (`:201`), pinned by `TestInterpreterFence` as the same protected surface | -> accept | Included in the kernel's extraction list |
| 3 | Security | The accepted §5 set-comparison mechanics were carried as a bare phrase, not as criteria | -> accept | C5/C6 acceptance criteria now carry all four verbatim: set equality vs `scan_targets()`, the positive-control mutation, the per-registry-removal release scan, the final canonical pair |
| 4 | Internal | The per-file manifest is aggregate-only for C6, and the suite-run ledger row names no files | -> accept | New "### The manifest, per file" section — every row, every file, every partial span |
| 5 | Internal | `_has_symlink_component_below` / `_git_ok` is a code-span-boundary issue, not a coverage one | -> accept | Rehoming section reframed: the span's boundaries are wrong as drawn |
| 6 | Internal | `link-check-allow`'s fold-in states no falsifiers of its own | -> accept | Its four falsifiers written out, with the row struck if it cannot meet them |
| 7 | Internal | A class of installer tests references `tools/lifecycle.py` by path, unnamed | -> accept | Enumerated in C1 rather than C6 |

### What I found while answering, and what it cost the manifest

Answering Finding 4 meant rebuilding the inventory by measuring **each file's
actual target rather than its name**. That turned up errors the reviewers had
not reached, in both directions:

* **`test_lifecycle_stage_patterns.py` (753) was a false inclusion.** It tests
  `lifecycle_metrics.py`, a module this sweep **keeps**. The first draft had it
  marked for deletion — live coverage of a surviving surface.
* **Six files were missing** from the manifest entirely, all genuinely coupled.
* **Most of those six do not die at all.** They test the surface C1 now keeps,
  so they are **repointed**, not deleted — including `test_skills_security.py`,
  a member of `security_manifest.py`'s `SECURITY_FAMILY`.

**A correction I owe the Internal reviewer.** Its pass reported the 36,332
figure as unreconcilable, ~1,300 short. I checked and reported that the
arithmetic was mine and correct — the fifteen files do sum to exactly 36,332.
That was true and beside the point: **the sum was right and the set was wrong**,
which is the only thing a deletion manifest is. The reviewer was pointing at a
real defect through an arithmetic disagreement, and the defect was mine.

### The order-5 figure moved, downward, and that is not a scope reduction

Wholly-removed order-5 lands nearer **32,500** than 36,332, and the sweep's net
nearer **~51,000** than 61,000 — because ~1,500 lines of tests are repointed
instead of deleted and ~1,400 lines of source survive as the kernel. Nothing
the accepted proposal set out to remove is being kept: the machinery still
goes. What changed is that the first draft counted surviving code as removed.

### One thing neither pass raised, recorded because it explains both

The tests that would have caught Finding 1 — `test_skills_security.py`,
`test_skills_self_heal.py`, `TestInterpreterFence` — all load `lifecycle.py`
behind `pytest.mark.skipif`. Delete the file and they **skip rather than fail**.
This plan's falling-test-count reconciliation, added precisely to catch coverage
loss, reads a skip as neither pass nor failure and would have missed it. C1's
acceptance criterion now requires each repointed test to be shown *failing*
against a tree without the kernel before it counts as repointed.

## C8 complete -- the gate anchor moved -- 2026-08-28

**C8 is done.** `refs/cairn/gate-anchor` advanced `5f99273 -> bd66a70`, signed
by the ceremony key (`SHA256:8R549gtP0SJP...`, `git verify-commit` reports Good
and fully trusted), branch and anchor moved in one transaction, and both refs
were pushed. The anchor had been 362 commits stale.

**The Maintainer's authorization, quoted rather than paraphrased:**

> We don't need to re-review everything. I bless the security of this session
> for re-anchoring. Let's go ahead with the ceremony.

That waived the re-review the security fix at `4bb6bb4` had voided. It did not,
and could not, waive arithmetic -- and arithmetic was the real blocker.

**What was actually stopping the ceremony, which nobody had written down.** The
instantiated launcher on the host was the **pre-fix** one from 2026-08-19: no
`unset L_*`, so it carried the environment-injection path an External Security
Review had found and this plan's `4bb6bb4` closed. It was also bound to a
`reanchor.sh` that no longer exists -- its packet pinned `daaaf483...` against a
tree at `b955542...` -- so it would have refused at RA-07. **That refusal would
have been luck, not a control.** A fresh packet and launcher were composed
against the current closure, and the pre-fix pair is to be deleted.

**The tree was never the problem.** Run read-only before any key or package was
spent, with the three changed closure members admitted as a transition, the
ceremony's own checks returned `BLOCKED=False`. The security machinery was
refusing nothing; the logistics were.

**The injection fix was confirmed by positive control**, not assumed:

| | input | result |
|---|---|---|
| A | values file with no `python` row, clean environment | REFUSE |
| B | same, with `V_python` **exported** | REFUSE -- the fix holds |
| C | same, against `reanchor.sh` **read from the old anchor** | **accepted** |

Row C is why this ceremony was worth running: the superseded anchor vouched for
a values reader with a live injection path.

**What the checkpoint records**, and it is the first honest measure of what this
sweep did to the protected surface:

```
frozen gate files   : 31 modified, 11 added, 32 removed
pytest collection   : 4460 -> 3180
admitted authority  : 10 members, transition mode
```

**Verification after the move.** Full suite `CAIRN_FULL_SUITE=1 pytest
bootstrap/tests --quality-gate-shuffle-seed=0` -> **3179 passed, 1 skipped**,
Python 3.13.13, 502s, exit 0. `_gate_manifest.py verify` -> OK, 182 frozen
files, 3180 pinned nodes. Working tree clean; nothing unpushed.

**A finding this ceremony surfaced and did not close.** The launcher is
manufactured from `bootstrap/reanchor-launcher.template.sh`, and **the template
is not a closure member** -- nothing in this repository pins it. The launcher is
the pre-candidate trust root: everything it does runs before the checker exists,
so none of the checker's internal pinning protects it. The ten-member closure
therefore has a hole exactly where it matters most, and the hole is invisible
because the closure looks complete. Mitigated only by reading the template from
the object store and naming its blob digest; **making it the eleventh closure
member is unclosed work**, and it predates this plan.

**C9 is now unblocked on every count.** Code review ran and was answered, the
lockfile is correct, and the anchor the sisters would inherit is current. C9
remains MAINTAINER-GATED per sister.

## C9 complete, and the four decisions it leaves -- 2026-08-28

**C9 is done.** Both sister migrations landed on `cairn-0.3.0-migration`
branches, with each `master` untouched.

| repo | suite | baseline | integrity |
|---|---|---|---|
| `modflow_tools` | 3472 passed, 0 failed | — | OK |
| `lhm` | 1223 passed, 9 skipped, 0 failed | master had 1 failed | OK |

**The Maintainer's authorizations, quoted:**

> Do C9 now, then archive

> Authorize all five as a batch

The second closes the `defer` batch above. Those five deposits are now
**authorized**, and the Dispositions line becomes `accept x13, guard x2,
defer x5 (authorized), wontfix x0`.

### Four decisions this chunk raises, which belong here rather than in a commit body

**1. An engine change landed without the proposal its surface calls for.**
`AGENTS.md` lists the scaffold/merge engine under *High-risk surfaces
(Security-Review + proposal triggers)*. Commit `3a99590` changes
`_apply_upgrade` and did not go through one. The author's argument for
treating it as a correction rather than a design change: `upgrade.py:1561`
already states the intended invariant -- *"base_hash = upstream for BOTH
verbatim and mergeable"* -- and one path did not honour it. **That is the
author's judgment, and the trigger is the Maintainer's to waive or enforce.**
It is unpushed and reversible either way.

**2. The AST baseline is stale and self-service is closed.** `_apply_upgrade`
is baselined but absent from `_ast_attest._UPDATE_ALLOWLIST`, so
`update-symbol` refuses it. Derived against the committed baseline, not
carried forward: `CHANGED 1, MISSING 0, DUPLICATE 0`,
`65a5f59ef844cfb9 -> dc53397782e91c18`, not pure motion. Per
`AST_BASELINE_RUNBOOK.md` this is a Maintainer-run direct correction. Until
it runs the suite carries exactly two failures, both in `test_ast_attest.py`.

**3. C7's prose phase was incomplete, and it reached adopters.** Cairn went on
*shipping* prose about the machinery it removed: the module roster advertised
two uninstallable modules, all three onboarding scripts told a new adopter
their fold-back ledger held a candidate, and `examples/minimal` promised a
tool that no longer ships. Both sisters inherited these **through** the
upgrade, because a file classified `clean` correctly takes upstream's version.
Fixed at `e9e8af7`, with `test_module_roster.py` added so the roster is
checked rather than remembered. **Recorded as a scope observation, not a
deviation**: C7 said "dead doctrine sections" and it is arguable whether
shipped templates were inside that. The Maintainer may read it either way.

**4. Doctrine still carries the same staleness, and it is NOT fixed.**
Eight files under `doctrine/` describe the removed machinery as live --
`session-routines.md` gates a whole section on *"when the fold-back-ledger
module is installed"*, `runtime-contract.md` lists `lifecycle_metrics` in a
capability table, `rationale.md` describes the ledger as the mechanism, and
`onboarding.md` documents a trigger that can no longer fire. This is the
published methodology rather than the scaffolding around it, so it was left
for an explicit decision rather than swept in. **It is open work.**

### Two findings worth keeping after this plan archives

**`upgrade --apply` deletes nothing.** `removed-upstream` is not in
`_ADVANCING_KINDS` and the apply path contains no `unlink`. It *reports* what
upstream dropped; retiring those files is the adopter's, by hand. The same is
true of `slot-removed`. An adopter who trusts `--apply` to complete a
migration is left carrying every removed file.

**A trigger can outlive the thing it tests.** `first-foldback-candidate`
checks for a ledger file nothing creates any more, so it can never fire --
and `test_active_surfacing_mechanism.py` hard-codes it as one of four
triggers, so removing it reddens a test. That coupling is why it stays
deferred rather than being cleaned up in passing.

## The AST attestation had a hole, and it is closed -- 2026-08-28

*Recorded here rather than in a commit body: the trace table below is the
evidence for a trust-fixture write, and a reviewer needs to be able to
challenge it.*

**The defect, demonstrated.** `_ast_attest.verify` classifies an altered
known-new body as **NEW, never CHANGED**, and returns non-zero only on
CHANGED / MISSING / DUPLICATE. The digest check that would have caught it was
a parameter of `update_symbol` -- the repair path, reachable only for the four
allowlisted symbols -- so a known-new body was pinned *during a surgical
re-baseline* and by nothing at all the rest of the time.

Injecting one statement into `verify_within_root`, the symlink/containment
guard `AGENTS.md` names as the scaffold engine's protection:

```
classified CHANGED?  False
classified NEW?      True
problems raised:     0
```

The gate printed `note: NEW` and exited 0. `AST_BASELINE_RUNBOOK.md` already
stated the hazard -- *"a symbol in known-new is invisible to the baseline
gate"* -- but nothing enforced it. **A named hazard with no enforcing trigger
is the case Cairn's own doctrine warns about**, and it sat in the runbook that
warns about it.

**Closed at `3079d27`**: the predicate is a shared helper both callers use,
`verify` enforces it, the gate command and both real-tree tests pass the
manifest, and a run without it warns rather than passing quietly. Re-running
the injection now fails on a digest mismatch.

### The 16 re-pinned known-new entries, and why each was admitted

Enforcement immediately surfaced 15 symbols whose bodies had drifted from
their pinned digests, plus 1 never listed -- [TRU-4]'s *"15 are currently
rekeyed"*, visible for the first time. The plan asserted they *"all trace to
reviewed work"*; that is now shown rather than asserted:

| symbol | origin commit |
|---|---|
| `ClassDef:ScaffoldLoaderError` | `d105967` scaffold-split: substrate Security re-review-2 fixups |
| `ClassDef:UpstreamSource` | `9bd6752` fork-advisory-semantics (Chunks A, C-E) |
| `FunctionDef:trusted_upstream` | `9bd6752` (same) |
| `FunctionDef:_adopt_token_unfilled` *(unlisted)* | `bec2cca` adopt-into-existing-tree D1/D2 |
| `FunctionDef:_commit_lock_and_caches` | `bec2cca` (same) |
| `FunctionDef:_resolve_current_profile` | `bec2cca` (same) |
| `FunctionDef:_always_on_group_complete` | `ed5a670` Sharpen side-door parity: 2 P1 from External-Security review |
| `FunctionDef:_cmd_adopt_collisions` | `ed5a670` (same) |
| `FunctionDef:assert_always_on_complete` | `ed5a670` (same) |
| `FunctionDef:duplicate_destinations` | `ed5a670` (same) |
| `FunctionDef:_assert_mapping_ownership` | `5d7d8f5` Sharpen new-module path: External Security review F1-F4 |
| `FunctionDef:_print_adopt_command` | `0d3d38f` Sharpen adopt-as-fork (re-review r2) |
| `FunctionDef:_record_fork_entry` | `9bc1119` install.py side-door executable parity |
| `FunctionDef:missing_always_on_sources` | `9bc1119` (same) |
| `FunctionDef:_rendered_onboarding_overlay` | `e71abd9` security-verification-activation |
| `FunctionDef:missing_required_tokens` | `246b0db` security-apparatus-enrichment Chunk B0 |

Every one is named, reviewed work; most are explicitly *security-review*
fixups. The re-pin was bounded by measurement -- exactly the 15 drifted and 1
missing the enforcement itself reported -- and refuses any other delta.

**The BASELINE was deliberately NOT touched.** `_apply_upgrade` is this
session's own change and sits there as CHANGED. Blessing one's own change is
what the fence exists for, so it stays the Maintainer's.

### Two re-anchors are now owed, not one

1. **The AST baseline**, for `_apply_upgrade` -- `CHANGED 1, MISSING 0,
   DUPLICATE 0`, `65a5f59ef844cfb9 -> dc53397782e91c18`.
2. **The gate manifest.** Retiring the dead trigger removed a test class and
   shrank a parametrize set, so the pinned collection changed. This is the
   pitfall `AGENTS.md` documents: the manifest self-verifies a freshly
   produced manifest and never diffs the committed fixture, so **a green
   suite is not evidence that no re-anchor is owed.**

## Archive -- 2026-08-28

**Dispositions restated.** The template's rule is that an append re-opens the
attestation, and this plan gained three sections after the original line was
written (C8 complete, C9 complete, the AST attestation record). Restated over
the whole record, final:

`Dispositions:` accept x13, guard x2, defer x5 (**authorized**), wontfix x0.

The `defer` batch is no longer unauthorized. The Maintainer authorized all five
as one batch, quoted at `## C9 complete`. **Two of the five have since been
closed rather than deposited**, so the deposit is smaller than the line
suggests and the record should say which:

* **[VER-5] closed.** `_MULTI_SCRIPT_MODULES` was an empty dict, so the
  multi-script install assertion parametrized over nothing and pytest skipped
  it -- the suite's only skip. Repointed at `issue-capture`, which ships the
  same two-script shape, and control-tested.
* **The `first-foldback-candidate` trigger closed.** It detected a ledger row
  in a file nothing creates, so it could never fire, and it could not be
  repointed because the surviving channel leaves no artifact in the adopter's
  tree. Retired end to end; the active-surfacing set went from four rows to
  three.
* **Still deposited (3):** [TRU-4]'s known-new graduation decision, C6's two
  onboarding findings behind the MAINTAINER-GATED `_ALWAYS_ON_MAPPINGS` fence,
  and the four unfiled forge issues.

**Superseding the `### Still owed before this plan can archive` block.** That
block was written before the work ran and is now false in every clause. For the
record: **C8 landed** (`refs/cairn/gate-anchor` `5f99273 -> bd66a70`, signed,
both refs pushed); **C9 landed** (both sisters, on branches, masters untouched);
and the **code review floor is met** -- the plan names its groups as *C1, C2+C3,
C5+C6, C7*, and one round ran for each. The block's "Zero rounds have run" was
true when written and is not now.

**Final verification.** Full suite `CAIRN_FULL_SUITE=1 pytest bootstrap/tests
--quality-gate-shuffle-seed=0` -> **3176 passed, 0 skipped, 2 failed**, Python
3.13.13, on a quiet tree; the two failures were the AST baseline pair, which the
Maintainer's re-anchor then cleared. After both re-anchors: `_ast_attest verify`
**OK, 173 baselined symbols, unchanged** -- the count did not grow, so it was a
correction and not a re-pin -- and `_gate_manifest verify` **OK, 183 frozen
files, 3178 pinned nodes**.

**What did NOT archive with this plan.** Work done after C9, at the Maintainer's
explicit direction, extends beyond any chunk and was not code-reviewed: the
doctrine pass, the shipped-template prose fix, and the AST attestation
enforcement. It is recorded above and its live half is homed elsewhere on
purpose -- **an archived plan is a poor home for an open security finding.**
`AGENTS.md`'s note that the gate manifest goes stale silently, and the
attestation's own `--known-new` requirement, both live in `NEXT_SESSION.md` and
the runbook rather than here.

**Lasting truths migrated** to
`dev/strategy/2026-08-21-claude-nimbleness-recovery.md`: the
measured-versus-estimated table with the ~55,000 corrected figure and its
double-count, and the three struck rows with their revival conditions. Row 3
resolved to **struck under its own condition** -- `link-check-allow` was never
folded in, so **three directive families remain, not two**. A future de-scope
that believes it is closing the last one will be wrong.
