# Plan: maintainer attention — a list of what waits on the Maintainer, and no work left in archived plans

**Source proposal**: `dev/proposals/archive/2026-10-17-claude-maintainer-attention.md`
**Status**: awaiting-plan-review
**Plan review**: required(Internal)
**Assurance path**: high-assurance — inherited: the change edits `doctrine/`, the authoring templates, and a tool adopters run
**Opened**: 2026-10-18

## Source proposal

**In plain terms.** This plan makes two changes.

* **A list of what waits on the Maintainer.** `python tools/board.py
  --maintainer` shows proposals awaiting a Decision. It also shows any plan or
  board row whose author wrote one line saying it waits on the Maintainer. The
  board still decides nothing: it reports what authors declared, and it flags
  plans that mention a fence (a chunk only the Maintainer can release) but
  declare no wait.
* **No work left in archived files.** Work still to be done must have a live
  home. Work handed to a plan not yet opened becomes a board row. Each archive
  commit writes its own changelog line.

Accepted 2026-10-18 at `e9043938`. Revision 1 binds, with every recommended
answer:

* **Q1:** Part B (agents taking their own turns) leaves this proposal. It is
  deferred to issue #13, and its board row was deposited at `07bd9950`.
* **Q2:** quoting the acceptance authorizes a later-plan deferral *only when the
  accepted text assigned that work to that plan*.

Part B is not in this plan's baseline.

## Scope

**Touched.**

* `tools/board.py`, its byte-identical shipped twin
  `templates/skills/_lib/board.py`, and that file's lockfile record in
  `dev/.cairn/cairn-lock.yml`.
* `bootstrap/tests/test_replacement_tools.py`, which gets five new nodes.
* `doctrine/lifecycle.md`:
  * the status sentence in "The proposal lifecycle";
  * "Archive precondition".
* `doctrine/plans.md`:
  * "Mutability rule";
  * "Accepted scope is a floor — the scope fence is not a licence to shrink";
  * "Lasting-truth migration doctrine".
* `dev/plans/_template.md` and `templates/core/dev/plans/_template.md`:
  * the preamble;
  * *Sequence*, *Scope delta*, *Dispositions* and *Code review*.
* `templates/core/dev/PLANNING.md`: one line.
* `dev/PLANNING.md`: one commit.
* One new tracker, at the path declared below.

Proposed paths:
* `dev/measurement/maintainer-view-misses.md` — the miss tracker (C5)

**Not touched**, each checked by `git diff --stat` over the implementation
range:

* `AGENTS.md` and `templates/core/AGENTS.md`, `doctrine/session-routines.md`,
  `doctrine/proposals.md`: Part B's surfaces left with it.
* `bootstrap/_scaffold/`: so there is **no AST impact**.
* `CHANGELOG.md`, until the archive commit (C3, applied to this plan itself).

**Frozen files.** One, `bootstrap/tests/test_replacement_tools.py`, read from
`bootstrap/tests/fixtures/gate_manifest.json` > `frozen_files`. Its bytes change,
and the gate manifest's pinned collection gains five nodes. Both join the
gate-manifest re-anchor already queued on `dev/PLANNING.md`; they start no new
ceremony.

The other files checked are not frozen: both `board.py` copies, both plan
templates, both `PLANNING.md` files, `doctrine/lifecycle.md` and
`doctrine/plans.md`. The instrument was checked against a known frozen key.

**Lockfile.** `tools/board.py` is a verbatim lockfile record (source
`skills/_lib/board.py`), so changing it leaves the record's hash stale.

* C1 reconciles it with a scoped finalize of that one path, following the
  precedent `2ea3f869`.
* `dev/plans/_template.md` already reports a hash mismatch in
  `bootstrap/verify_integrity.py --target .`. It is **not** finalized, because
  that would re-attest earlier, unreviewed drift.
* The lockfile schema is untouched.

### Sequencing with the sibling plans

`verification-practice` is implementing now and **lands first**. This plan
**rebases onto it**:

* **`doctrine/plans.md`.** That plan edits "Boundary A", "Boundary B" and "Code
  review — doctrine"; this one edits "Mutability rule", "Accepted scope is a
  floor" and "Lasting-truth migration doctrine".
* **Both plan templates.** That plan changes one word in the
  `verification-commands` slot; this one edits other sections.
* **Its pins.** It adds `bootstrap/tests/test_review_and_verification_rules_ship.py`,
  which pins plan-template text, so that file joins this plan's Boundary A.

C2 and C3 therefore start only from a tree that holds verification-practice's
last implementation commit. C1 and C5 touch none of its files and may run
earlier.

Two other siblings:

* `independent-scientific-check` edits the templates' *Acceptance criteria*,
  which this plan does not touch.
* `neutrality-and-upgrade-slots` makes the neutrality checker stricter. Every
  line this plan adds names no vendor, HTML comments included.

### Found while planning, not widened

* **A placeholder in the template header would list as waiting.** The plan
  templates document the `Waiting on Maintainer` line in prose, and their header
  block carries no such line. Otherwise every plan copied from a template would
  list as waiting on the Maintainer.
* **The shipped board template's restatement.**
  `templates/core/dev/PLANNING.md` restates the archive precondition too. The
  accepted text gives that file only the marker line, and its restatement
  already says "This copy is not the source", so it is delivered as written.
* **Two other mentions of sequencing.** `AGENTS.md` and
  `doctrine/dual-review.md` both say "sequencing may move work between chunks".
  The accepted C2 names `doctrine/plans.md` and the plan templates only, and
  "chunks" already means one plan's chunks, so neither changes.
* **A partial test class name.** `TestTheBoardReadsHeadersAndJudgesNothing`
  becomes a partial name once the board reads `dev/PLANNING.md` too. The
  accepted text puts the nodes in that class, and the property it pins, judging
  nothing, still holds. Renaming the class is not in scope.

### Documentation / doctrine surface

| Layer | Files |
|---|---|
| Doctrine | `doctrine/lifecycle.md`, `doctrine/plans.md` |
| Templates | both plan templates; `templates/core/dev/PLANNING.md` |
| Deliberation | `dev/PLANNING.md`; the new tracker |
| Descriptive | none; no `docs/` page changes |

The rate-limit grounds are the proposal's, and the Decision ratified them.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | **The board learns the list.** `board.py` gains `--maintainer`: <ul><li>it lists artifacts at `awaiting-decision`, artifacts whose header carries `**Waiting on Maintainer**:`, and `dev/PLANNING.md` lines carrying it (each named by line number);</li><li>one advisory footer line names each active plan whose body has `MAINTAINER-GATED` or `MAINTAINER-ONLY` but whose header has no Waiting line;</li><li>the footer names pushes (`git status`) and anything undeclared as unlisted, and names a missing `dev/PLANNING.md`.</li></ul>The field joins `_FIELDS`, and the docstring gains one sentence naming the two new reads. Twin byte-identical. Five nodes in `TestTheBoardReadsHeadersAndJudgesNothing`, each red before the code. Scoped finalize of `tools/board.py`. | plan review landed | one commit |
| C2 | **The line, written down.** Doctrine and templates say what the Waiting line is and when to write it:<ul><li>`doctrine/lifecycle.md` gains the exception to "status alone names the holder";</li><li>`doctrine/plans.md` > "Mutability rule" lists the line beside Status;</li><li>both plan templates get the line documented in the preamble, a *Sequence* sentence (write it when work reaches a fenced chunk), a *Dispositions* sentence (write it with a `defer` batch), and a *Code review* check (`git log -p` on the plan shows a Waiting line for each fenced chunk and deviation request in the range; a missing line is a finding, recorded in the project's incident tracker);</li><li>`templates/core/dev/PLANNING.md` gets one line stating the row marker.</li></ul> | C1; verification-practice's last implementation commit is in the tree | one commit |
| C3 | **Archived files are records.** Nothing still to be done may live only in an archived file:<ul><li>`doctrine/lifecycle.md` > "Archive precondition" gains the rule and the live-home definition;</li><li>`doctrine/plans.md` > "Accepted scope is a floor" gains "of a live plan" and the Q2 rule;</li><li>`doctrine/plans.md` > "Lasting-truth migration doctrine" gains changelog-at-archive;</li><li>both templates gain *Scope delta* "of a live plan" with the Q2 rule, and in *Dispositions* a pointer to the rule plus the changelog line.</li></ul> | C2 | one commit |
| C4 | **Today's waiting rows are marked.** One commit to `dev/PLANNING.md` under the Decision's instruction:<ul><li>the marker is stated once;</li><li>the rows that wait on the Maintainer are marked: the gate-manifest re-anchor, the open "Four deferred Maintainer questions", the stage-reader row's question (3), and any others a sweep finds (each listed in the commit body with its reason);</li><li>one line joins the *Archive preconditions* restatement for C3's rule.</li></ul> | C1, C3 | one commit |
| C5 | **The miss tracker.** A miss is recorded, not remembered. `dev/measurement/maintainer-view-misses.md` is forked from `dev/modules/incident_log_template.md`, with a 30-day window. A miss is a code-review "waiting-line miss" finding, or anything the Maintainer reports waited without being listed, board rows included. | plan review landed | one commit |
| C6 | **Boundary B, then the record.** The whole suite runs once on the finished work, and the result is written down: full mode (*Verification*), then `## Implementation verification`. Status moves to `awaiting-code-review`. | C1–C5 | one commit |
| M | **MAINTAINER-ONLY — no new ceremony.** `bootstrap/tests/test_replacement_tools.py` and its five new node IDs join the re-anchor row already queued. **An implementing agent must not perform the re-anchor.** The agent's part is the board note at archive. | code review cleared | Maintainer |

**Shared-file discipline.** C4 runs `python tools/intent.py list` before editing,
because `dev/PLANNING.md` is a coordination surface.

## Acceptance criteria

### C1

* **On a scratch tree, `--maintainer` lists exactly:**
  * an `awaiting-decision` proposal;
  * a plan carrying the line;
  * a `dev/PLANNING.md` line carrying it.

  Nothing else is listed (node 1).
* **A plan with a fence token in its body and no Waiting line** is named on the
  advisory line and is not listed as waiting (node 2). Deleting the advisory
  code in a scratch copy turns node 2 red.
* **A row that only mentions the marker mid-sentence** (in backticks) is not
  listed (node 3).
* **The footer** names pushes and undeclared items as unlisted, and names a
  missing `dev/PLANNING.md` (node 4).
* **A control character in a header value and in a row value** comes out escaped
  (node 5).
* **Each new node is red before the code change.** The record names the commit
  where each was red.
* **The plain board is unchanged** on a tree that carries no Waiting line: its
  output is byte-identical before and after.
* **The two copies are identical:**
  `cmp tools/board.py templates/skills/_lib/board.py` exits 0.
* **No new subprocess:** `grep -nE "subprocess|Popen|os\.system" tools/board.py`
  prints nothing.
* **The lockfile.** After `python bootstrap/scaffold.py upgrade --target .
  --finalize tools/board.py`:
  * the lockfile diff touches only the `tools/board.py` record;
  * `python bootstrap/verify_integrity.py --target .` lists no finding for
    `tools/board.py`.

### C2

* **`doctrine/lifecycle.md`** carries the exception: inside a plan, the Waiting
  line names a Maintainer gate.
* **"Mutability rule"** in `doctrine/plans.md` lists the line.
* **No template line begins with the marker.**
  `grep -n "^\*\*Waiting on Maintainer\*\*" dev/plans/_template.md templates/core/dev/plans/_template.md`
  prints nothing, so a copied plan carries no live line.
* **The added sentences match.** The *Sequence*, *Dispositions* and *Code
  review* sentences are identical in both plan templates.
* **A fresh install lists nothing.** Install into a scratch tree with
  `bootstrap/scaffold.py`, then run `board.py --maintainer --root <scratch>`. It
  lists zero rows, so the new `PLANNING.md` line does not list itself.
* **`python scripts/check_cairn.py` passes.** Any new `doctrine/` reference in a
  shipped template carries its `cairn-internal-ref-allow` marker.

### C3

* **The rule is in place.** `doctrine/lifecycle.md` > "Archive precondition"
  holds the rule, *nothing still to be done may have an archived artifact as its
  only home*. It also holds the live-home definition: an open artifact that names
  the item, an issue by number, or a board row.
* **Sequencing.** Both `doctrine/plans.md` and the two templates read "between
  chunks of a live plan". They keep the pinned phrases "Sequencing is free;
  removal is not" (doctrine) and "Sequencing is free" (templates).
* **The Q2 rule says "assigns".** The Decision quote authorizes a later-plan
  `defer` only when the accepted text assigns that work to that plan, and the
  `defer` line quotes the assigning sentence.
* **Changelog at archive.** `doctrine/plans.md` > "Lasting-truth migration
  doctrine" and both templates say the archive commit writes the plan's
  changelog entry. The `NEXT_SESSION.md` sentences in that section are
  unchanged.
* **`bootstrap/tests/test_scope_reduction_trap.py` passes unchanged.** Deleting
  "Sequencing is free" from a scratch copy of a template turns it red, which
  confirms the pin still reads the edited sentence.

### C4

* **The live list is not empty.** `python tools/board.py --maintainer` on the
  live tree lists at least the three named rows.
* **Every marker value is short.** Each is under 48 characters, so no `…`
  appears in the output.
* **The commit is narrow.** It touches only `dev/PLANNING.md`.
* **Every mark has a reason.** The commit body names each marked row and why its
  next move is the Maintainer's. A deferral already authorized is queued work and
  is not marked.

### C5

* **The tracker is a real tracker.** It has the template's sections, an empty
  `## Incidents` table, a 30-day window, and a *What counts* entry covering both
  sources.
* **It is read, not skipped.** `python tools/evolution_infer.py` reads it: it
  appears among the trackers read, not under `SKIPPED`.

### C6

* **The record is complete.** `## Implementation verification` carries every
  field in *Verification*, and lists the five new node IDs for the re-anchor row.

## Scope delta

**Scope delta**: preserved. The baseline is Revision 1 as accepted, and every
outcome in it maps to a chunk:

| Accepted outcome | Chunk |
|---|---|
| the line in plans and change notes | C1, C2 |
| the line in `dev/PLANNING.md` rows | C1, C4 |
| `--maintainer`, column | C1 |
| declare and check | C1 |
| the footer | C1 |
| today's rows marked | C4 |
| the lifecycle.md exception | C2 |
| the docstring | C1 |
| the archive rule | C3 |
| sequencing within a live plan, and Q2 | C3 |
| changelog at archive | C3 |
| the tracker and its code-review check | C2, C5 |
| the shipped `PLANNING.md` line | C2 |
| five test nodes | C1 |
| Boundary B full | C6 |

Part B is not in this baseline: the Decision cut it before this plan opened.

## Verification

**Boundary A (iteration, scoped).** Each chunk runs the tests that own the files
it touches, plus `python scripts/check_cairn.py` and `python
scripts/claim_check.py` on each edited document.

| Chunk | Tests |
|---|---|
| C1 | `test_replacement_tools.py`, `test_session_kernel.py`, `test_security_lint.py`, `test_skills_upgrade.py`, `test_skills_self_heal.py`, `test_verify_integrity.py` |
| C2, C3 | `test_scope_reduction_trap.py`, `test_verification_boundaries.py`, `test_review_and_verification_rules_ship.py`, `test_scaffold.py`, `test_claim_check_module.py`, `test_loop_fidelity_gate.py`, `test_documentation_plan_module.py`, `test_quickstart_sequence.py`, `test_core_dev_folders.py`, `test_upgrade.py`, `test_module_merge_lockfile.py` |
| C4, C5 | the claim and prose gates only (prose a test does not read) |

All tests are in `bootstrap/tests/`. The C2 and C3 set is not a confident bound:
some 57 install tests render the shipped plan template. So Boundary B is the
real check.

**Boundary B mode**: full. The refusal rules in `AGENTS.md` settle it:

1. **A frozen file changes.** `test_replacement_tools.py` is in the gate
   manifest's `frozen_files`, and its pinned collection grows. That touches the
   gate-manifest contract surface, and bounded mode refuses.
2. **Shipped surfaces change.** A tool adopters run, and two shipped templates,
   are edited. Most of the suite renders those templates, so no mapping bounds
   the change confidently. Uncertainty resolves to `full`.
3. **The lockfile is touched.** A lockfile record is reconciled. The schema is
   untouched, but whether a record edit counts as touching the contract surface
   is uncertain, and uncertainty resolves to `full`.
4. **The accepted text says so:** "Boundary B runs full".

**How it runs.** After C5, against a clean, unchanged commit, under the
canonical interpreter (Python 3.13.x, as `tools/session.py` resolves it):

```
CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0
python scripts/quality_gate.py --sub neutrality --sub redundancy
```

Then run `check_cairn.py`, and `claim_check.py` on each edited file. Run it from
a separate worktree at the tested commit. A worktree shares refs, so the gate
anchor is present, and other sessions' uncommitted files stay out of the count.

**Expected non-pass**, each disposed of rather than treated as noise:

* **The neutrality leg** carries pre-existing failures. Record the figure at the
  tested commit, and confirm no hit is on a line this plan added.
* **`test_gate_manifest.py`** has no expected failure. Changed frozen bytes do
  not redden it; only a deleted frozen file would.

The record uses the template's fields: mode, tested SHA, range, interpreter,
clean pre- and post-run state, a command table, non-pass disposition, and known
omissions.

**Boundary C** is the code reviewer's, run after Boundary B. The points worth
attacking:

* **The silent-miss case.** A plan that waits on the Maintainer must show up,
  either listed or flagged.
* **The mid-sentence filter.** Does it hold for a list-item marker
  (`* **Waiting on Maintainer**:`)?
* **The shipped template, read cold as an adopter.** Can you follow the Waiting
  line and the *Code review* check?
* **The lockfile diff.** Is it confined to one record?

**Security preflight.** N/A, as in the proposal: no trust boundary is added,
moved, or widened. The new read is a fixed path holding the same class of
Markdown the board already reads, through the same encoder, with no subprocess.
The chunking changes no answer.

## Dispositions

*Filled at archive-preparation.* Two items are known now:

* **The archive commit writes this plan's `CHANGELOG.md` entry**, applying C3
  to itself.
* **It adds a note to the queued re-anchor row** naming
  `test_replacement_tools.py` and the five node IDs (chunk M).
