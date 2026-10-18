# Plan: maintainer attention — a list of what waits on the Maintainer, and no work left in archived plans

**Source proposal**: `dev/proposals/archive/2026-10-17-claude-maintainer-attention.md`
**Status**: revising-plan
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

## Plan review -- Claude Opus 5.5 (Internal, fresh session) -- 2026-10-18

```
Reviewed commit: c61da58bc06ca183cf473c5d70e2562a93ec2b54
Target: the whole plan (Source proposal through Dispositions), read against Revision 1 and the Decision of dev/proposals/archive/2026-10-17-claude-maintainer-attention.md; facts checked against the tree at b712020d2f76187db729152cbf7921f010c41e29, where the plan is unchanged
Prior findings: none
Assurance path: high-assurance — inherited
```

**Obligation**: required(Internal)
**Tier**: Internal
**Findings**: raised
**Verdict**: REVISE → `revising-plan` (5 blocking, 8 non-blocking)

Distance: a fresh session of the author's agent type. I did not write this plan
and will not implement it.

### In plain terms

The plan is well built. Every outcome the Maintainer accepted, with part B cut,
has a chunk, and the frozen-file, lockfile and code-baseline claims check out.
Five things need fixing before work starts, each a sentence or two:

* **A check that cannot fail.** C3 says it will prove a protected sentence is
  still protected by deleting two words and watching a test go red. The test
  would stay green.
* **A row that is gone.** One of the three board rows C4 promises to mark was
  removed this morning, after the plan was written, because the Maintainer had
  settled all of its questions.
* **A false alarm built in.** The new code-review check would count a step the
  work never reached as a "miss". This plan's own last step would be the first,
  and two misses in a month is the agreed sign that the whole design is wrong.
* **An unwritten format.** The plan does not say what a "waiting" line on the
  board file must look like. If the instructions show one form and the tool
  reads another, a waiting item silently drops off the list.
* **Two accepted sentences with no home.** Two sentences the Maintainer accepted
  about archived files are not named in any chunk.

The other eight findings are improvements the author may take or decline.

### The three readings

* **(a) The Waiting line documented in the templates' instructions, not as a
  header placeholder: delivers the outcome.** Revision 1 makes the line
  *optional*, written only "when the next move becomes yours". The board reads
  any value on a header line (`tools/board.py:35`), `{{...}}` included, so a
  placeholder would list every plan copied from the template as waiting. One
  consequence needs handling: the template's preamble is not copied into a
  plan, and the board reads only the header block, so the copied sentences must
  say *where* the line goes [PR6].
* **(b) The code-review miss check as a portable sentence in the shipped
  templates: delivers the outcome, with one gap.** Revision 1 puts the check at
  code review and names no surface for it. The template's code-review section is
  where a code reviewer meets it. An adopter's tree has no
  `dev/measurement/maintainer-view-misses.md`, so the shipped copy cannot name
  it. Shipping the check adds no mechanism: the Waiting line ships, and this is
  its guard against silent failure. The gap is Cairn's own copy, which would say
  only "the project's incident tracker". Cairn keeps six other tracked files in
  `dev/measurement/`, and Revision 1's closure of MA-6 is a *named* file [PR7].
* **(c) The shipped board template gets only the marker line: delivers the
  outcome as written.** Revision 1's documentation surface gives
  `templates/core/dev/PLANNING.md` "one line stating the row marker", and gives
  the restatement line to `dev/PLANNING.md`. The shipped restatement already
  says it is not the source, and points at `dev/plans/_template.md` >
  *Dispositions*. That pointer carries the new rule to an adopter only if the
  shipped *Dispositions* text states it in words, because `doctrine/` is not
  installed in an adopter tree (`bootstrap/tests/test_scope_reduction_trap.py:1-8`
  explains why that matters). So (c) holds, provided the shipped sentence
  states the rule rather than only citing `doctrine/lifecycle.md` [PR6].

### What checks out

* **Frozen files.** Of the files this plan touches, only
  `bootstrap/tests/test_replacement_tools.py` is a key in
  `bootstrap/tests/fixtures/gate_manifest.json` > `frozen_files` (183 keys).
  `bootstrap/tests/test_scope_reduction_trap.py` is also frozen, and is read but
  not edited. Not keys: both board copies, both plan templates, both
  `PLANNING.md` files, both doctrine files, `tools/session.py`, the lockfile,
  and the manifest itself. Added test nodes are recorded as `COLLECTION-ADDED`,
  not held (`bootstrap/tests/_gate_manifest.py:672-685`), so joining the queued
  re-anchor is right.
* **No AST impact.** `bootstrap/tests/_ast_attest.py` pins the scaffold engine.
  The plan touches no engine file, and the board's install row
  (`bootstrap/_scaffold/config.py:584`) does not change.
* **Twins.** `cmp tools/board.py templates/skills/_lib/board.py` exits 0 at the
  reviewed tree.
* **Lockfile.** `tools/board.py` is a verbatim record whose `hash` equals its
  `base_hash` today. A scoped `--finalize tools/board.py` behaves as the plan
  needs (`bootstrap/_scaffold/upgrade.py:1776-1899`):
  * it hashes the on-disk bytes;
  * the dirty-tree guard applies only to an unscoped finalize, so it is skipped;
  * it leaves `base_hash` alone;
  * it fails closed on an unknown path.

  Finalizing inside the C1 commit therefore works, as at `2ea3f869`, whose
  lockfile diff was one line. `verify_integrity --target .` reports 18
  mismatches today. `dev/plans/_template.md` is among them and `tools/board.py`
  is not, as the plan says.
* **"The plain board is byte-identical"** can fail and can be checked: `_render`
  prints a column only when some row has a value (`tools/board.py:100-104`).
* **"Judges nothing" holds in the design.** The list comes from
  `awaiting-decision` and declared lines only. The advisory is a token test.
  Node 2 pins that a fence token alone does not list. [PR4] and [PR9] make the
  declared-line rule exact.
* **Sequencing.** verification-practice C1–C4 have landed (`296cdfad`,
  `0a4becdb`, `399d406d`, `f4d4ff3c`); its Boundary B and code review remain.
  Its edits to `doctrine/plans.md` and the templates sit in other sections than
  this plan's.

### Findings

#### [PR1] blocking — C3's check that the frozen pin still reads the edited sentence cannot fail as written

**Plain.** C3 promises to prove that a protected sentence is still protected:
delete the words "Sequencing is free" from a copy of a template, and the test
goes red. It would stay green, for two reasons:

* the test accepts any one of three phrases, and the sentence keeps a second;
* the test reads the real files at fixed paths, so it never reads a scratch
  copy.

**Precision.** The plan-template pin is the alternation `[Ss]equencing is
free|moving work between chunks|Sequencing between chunks owes nothing`
(`bootstrap/tests/test_scope_reduction_trap.py:98-100`). After C3 the template
reads "Sequencing is free — moving work between chunks of a live plan owes
nothing". Deleting "Sequencing is free" leaves "moving work between chunks",
which still matches. I applied both edits to the text of both templates and ran
the pattern: it matched every time.

The test reads `CAIRN_ROOT / rel`
(`bootstrap/tests/test_scope_reduction_trap.py:281-283`). C1's node-2 mutation
has the same problem: `test_replacement_tools.py` loads
`CAIRN_ROOT / "tools" / "board.py"`
(`bootstrap/tests/test_replacement_tools.py:19-24`).

**Closes when** C3's mutation, in a throwaway worktree at C3's commit:

* removes the whole edited sentence, both phrases, from each template;
* names the parametrized node that goes red for each file.

C1's node-2 mutation also names a throwaway worktree in place of "a scratch
copy".

#### [PR2] blocking — C4 names a row that no longer exists, and its marking rule contradicts its own first example

**Plain.** C4 must show the list holding "at least the three named rows". One
of them, "Four deferred Maintainer questions", was removed from the board this
morning, because the Maintainer had settled all four. So the criterion cannot be
met. Separately, C4 says an authorized deferral is not marked. But the gate
re-anchor *is* an authorized deferral, and Revision 1 names it as a row to mark.

**Precision.** `30ff0cd5` retired the row at 10:47, six minutes after this plan
opened at `c61da58b`. The re-anchor row (`dev/PLANNING.md:156`) carries the
Maintainer's deferral, "If we don't need to re-anchor now, let's not".
Revision 1 reconciles the two by the next move. A marker goes on a row whose
next move is "a ceremony only you run, a question only you answer, or a
go-ahead only you give". An authorized deferral carries none only when its next
move is someone else's: F8's next move is a proposal anyone may open.

The accepted outcome, "today's waiting rows are marked", is still delivered in
full. The example vanished because the wait ended, so this is not a scope
change.

**Closes when:**

* C4 names the two rows that remain, plus its sweep: the re-anchor, and the
  stage-reader row's question (3) (`dev/PLANNING.md:485`);
* the criterion reads "at least the two named rows";
* the marking test reads: "the next move is one only the Maintainer can make;
  an authorized deferral whose next move is anyone's is not marked".

#### [PR3] blocking — the code-review check would count a chunk the work never reached as a miss

**Plain.** At code review, the reviewer checks that a Waiting line was written
for each fenced chunk. But a plan's last chunk is often a Maintainer-only step
that comes *after* code review. This plan's chunk M is one, and so is
verification-practice's. No Waiting line can exist for them yet. Read
literally, each such plan logs a false miss, and two misses in a month is the
agreed sign that declaring is the wrong design.

**Precision.** C2's sentence is "a Waiting line for each fenced chunk and
deviation request in the range". This plan's M is gated on "code review
cleared", and `dev/plans/verification-practice.md:223` is the same. Both hand
their wait to the queued re-anchor row, which C4 marks. Revision 1 says "in the
reviewed range", which means each fence the range reached. The tracker's
threshold is two `occurred` rows in its window (`tools/evolution_infer.py:66`).

**Closes when** the *Code review* sentence says, in substance:

* `git log -p` on the plan shows a Waiting line for each fenced chunk whose
  fence became the next move inside the reviewed range, and for each deviation
  request made in it;
* a fence not yet reached is not checked;
* a fence whose wait is declared on a marked board row is checked there.

#### [PR4] blocking — the form of a board-row marker is left to code review

**Plain.** The plan says a board row is marked with "a line inside the row". It
then lists, as an open question for the code reviewer, whether a bulleted line
counts. That is the contract between the instructions and the tool. If the
instructions show one form and the tool reads another, a marked row is silently
left off the list. It should be settled now, not by the code reviewer.

**Precision.** Board rows are bullets whose continuation lines are indented two
spaces (`dev/PLANNING.md:156`). The header regex anchors `**Name**:` at the start
of the stripped line (`tools/board.py:35`). So an indented line would match, and
a sub-bullet `  * **Waiting on Maintainer**: …` would not. Two places will each
document a form: C2's shipped line and C4's statement. Node 3 pins only the
negative case: mid-sentence, in backticks.

**Closes when** C1 states the row grammar. I recommend: a line inside the row
whose text, after leading spaces and an optional `* ` or `- `, begins
`**Waiting on Maintainer**:`, and nothing else. Then:

* node 1 lists both the indented form and the sub-bullet form;
* node 3 keeps the backticked negative;
* C2 and C4 document exactly that form;
* the *Boundary C* bullet becomes "does the parser match exactly the documented
  form".

#### [PR5] blocking — C3 does not name two clauses Revision 1 accepted

**Plain.** The Maintainer accepted two sentences that give the archive rule its
force:

* work handed to a plan not yet opened is a deferral to that work's board row,
  listing the items;
* a pointer to an archived file, or to an unopened plan, is not a live home.

Neither appears in C3's text or in its checks. Accepted scope is a floor, so
both need a chunk.

**Precision.** These are Revision 1 > Proposal > C, items 1 and 2. C3 names
"the rule and the live-home definition", and its criterion lists only the three
positive homes. It names "of a live plan" and the Q2 rule. The Q2 rule says
*when* a quoted Decision authorizes a later-plan `defer`. Neither of C3's
clauses says that the hand-off *is* a `defer` needing a board row that lists the
items. That clause is what closes LHM's six-plan failure.

**Closes when** C3's text and criteria carry both clauses:

* the negative live-home clause, in `doctrine/lifecycle.md` > "Archive
  precondition";
* the hand-off-is-a-`defer` clause, in `doctrine/plans.md` > "Accepted scope is
  a floor" and in both templates' *Scope delta*.

The Scope delta table's row "sequencing within a live plan, and Q2" then points
at them.

#### [PR6] non-blocking — C2's criteria do not check what the documentation tells an author

**Plain.** C2's checks confirm that the new sentences exist and match. They do
not check what the sentences tell an author. Because the board reads only a
plan's header, one missing word ("header") puts the line in the wrong place, and
the wait drops off the list without a sound.

The preamble sits above the template's rule and is not copied. C2's criteria
could pin:

* **the preamble** names the exact form, all three triggers (a fenced chunk, a
  `defer` batch, a deviation request), "delete it when answered", and the
  48-character budget. It also says that change notes carry the line: they
  live at `dev/plans/<slug>.md`, and the board reads them;
* **the copied sentences**, in *Sequence* and *Dispositions*, say "in the header
  block, beside Status";
* **the shipped `PLANNING.md` line** says the marker goes inside the row, when
  the row's next move is the Maintainer's, in the form [PR4] fixes;
* **the shipped *Dispositions* pointer** states the archive rule in words, not
  only as a `doctrine/` citation (reading (c));
* **an archiving plan carries no Waiting line.** A wait still open at archive
  moves to a marked board row. `--maintainer` reads no archive, so a line left
  in an archived plan is exactly the failure C3 forbids.

#### [PR7] non-blocking — Cairn's own template should name the miss tracker

**Plain.** Cairn's code reviewer would be told to record a miss in "the
project's incident tracker", but Cairn keeps several. The accepted design
records misses in one named file, so that two of them can be counted.

**Closes when:**

* Cairn's `dev/plans/_template.md` names
  `dev/measurement/maintainer-view-misses.md`, and the shipped copy keeps the
  portable phrase;
* C2's "identical sentences" criterion allows that one difference;
* C5 lands before C2, so the new path resolves when `claim_check` and
  `check_cairn.py` read Cairn's template.

#### [PR8] non-blocking — Boundary A misses three readers

* **C1.** `bootstrap/tests/test_notice_install.py` holds the twin byte-identity
  and SPDX-header tests (`bootstrap/tests/test_notice_install.py:105-124`). They
  read `tools/board.py` and its source; this is the test that owns "twin
  byte-identical".
* **C2.** Four tests render `templates/core/dev/PLANNING.md` into a scratch
  install and read the result: `test_onboarding_seed_roster.py`,
  `test_onboarding_slot_substitution.py`, `test_onboarding_activation_helper.py`
  and `test_skills_onboarding.py`.
* **C4.** "Prose a test does not read" is not true of `dev/PLANNING.md`.
  `test_scope_reduction_trap.py` pins its *Archive preconditions* text
  (`bootstrap/tests/test_scope_reduction_trap.py:259-260`), the section where C4
  adds a line.
* **A correction.** `test_review_and_verification_rules_ship.py` reads only the
  two `AGENTS.md` copies
  (`bootstrap/tests/test_review_and_verification_rules_ship.py:52-55`), not
  plan-template text. Running it costs little, but the stated reason is wrong.

Boundary B runs full, so none of these is a hole at integration. They are gaps
in iteration.

#### [PR9] non-blocking — pin where the advisory does not look

**Plain.** The fence advisory should name only live plans. The plan says so, but
no test proves it, and the plan does not say what `--maintainer --archive` does.
Fifteen archived plans carry 57 fence lines, so an advisory that read archives
would name all fifteen.

* **Negatives in node 2.** Add an archived plan, a `_template.md` and an active
  proposal, each with a fence token and no Waiting line. Assert that none is
  named, with and without `--archive`. State that `--maintainer` reads active
  artifacts only, or refuses `--archive`.
* **Every value encoded.** Node 5 should also cover the names printed on the
  advisory line, since a file name is contributor-controlled. Revision 1's
  test 5 says "every value".
* **A near-miss spelling.** A line written `**Waiting on Maintainer:** …`, with
  the colon inside the bold, fails the regex. Some sessions use that style in
  plan bodies. On a plan with no fence token, the miss is silent. Listing it,
  or naming it on the advisory line, keeps it visible.
* **A baseline for noise.** On day one the advisory will name both active
  plans, since each has a chunk M not yet reached. Recording that output in
  C1's commit gives Revision 1's "noisy check" signal a starting figure.

#### [PR10] non-blocking — the tool's own description becomes false

**Plain.** The board describes itself as reading header blocks "and nothing
else". After C1, `--maintainer` reads two more things. Adding one docstring
sentence would leave the old sentence contradicting the new one.

**Precision.** Three places say header-only:

* the docstring, "It parses header blocks and nothing else"
  (`tools/board.py:7`);
* the help text, "from header blocks only" (`tools/board.py:115-116`);
* the footer, "Derived from header blocks" (`tools/board.py:108-109`).

`docs/tool-usage.md` > "tools/board.py" also describes the board as reading
headers only (`docs/tool-usage.md:117-120`).

**Closes when:**

* "and nothing else" names the two `--maintainer` reads;
* the usage block and help text list `--maintainer`;
* the plain-mode footer stays byte-identical, as C1's criterion requires.

One descriptive sentence in `docs/tool-usage.md` would describe accepted
behaviour and add no outcome. The plan's "no `docs/` page changes" should
either take it or say why not.

#### [PR11] non-blocking — C4's shared-file steps

**Plain.** C4 edits the shared board. The doctrine for shared files asks for
two steps, and C4 names one. And because a commit by path takes the whole file,
another session's unfinished edit could ride along under C4's name.

**Precision.** `doctrine/coordination.md:112-125` requires both declaring an
intent naming the file and reading the intent set. C4 names only
`intent.py list`. `git commit dev/PLANNING.md` commits the whole file. Another
session committed to `dev/PLANNING.md` during this review (`30ff0cd5`).

**Closes when:**

* C4 claims as well as lists;
* its "the commit is narrow" criterion checks that the diff holds only C4's
  marks, statement and restatement line;
* its body quotes the Decision verbatim, as the instruction that authorizes a
  shared-file edit.

#### [PR12] non-blocking — the tracker should count both sources together

**Plain.** The tracker counts misses by kind. If a code-review miss and a
Maintainer-reported miss are recorded as two kinds, one of each never adds up to
the "two" that matters.

**Precision.** `tools/evolution_infer.py` counts `occurred` rows per Event Class,
with a threshold of two (`tools/evolution_infer.py:66`).

**Closes when:**

* C5's *What counts* defines one class covering both sources;
* its Purpose says what two rows mean. Per Revision 1, that is "declaring is the
  wrong design", not only a doctrine rate-limit suggestion.

#### [PR13] non-blocking — small mechanics, and two first sentences

* **Gates.** C1 and C5 are gated on "plan review landed". With this review at
  `revising-plan`, C1 could start before [PR4] and [PR9] are folded.
  `ready-to-implement` is the gate the sibling plan uses.
* **Red before.** C1 is one commit, so no commit holds the new nodes without the
  code. Record the parent SHA the nodes failed against, as `2ea3f869` did in its
  body.
* **The subprocess grep** fails falsely if the new docstring says "no
  subprocess". Grep for `import subprocess|subprocess\.|Popen|os\.system|os\.popen`
  instead.
* **Fresh install.** Run the installed `tools/board.py --maintainer` inside the
  scratch tree, not Cairn's copy with `--root`. That also proves the shipped
  twin runs in an adopter tree. Cairn's copy loads its encoder from its own
  location (`tools/board.py:50`), not from `--root`.
* **Sequencing.** verification-practice still has code review ahead. A
  `revising-code` fix could edit `doctrine/plans.md` or the templates again, so
  C2 and C3 should re-read their sections at edit time. Both plans commit to
  `master`, so "rebases onto it" can mean only that.
* **First sentences.** C1's "The board learns the list" and C5's "The miss
  tracker" open on a metaphor and on an undefined word. For example:
  * C1: "A new command lists everything waiting on the Maintainer."
  * C5: "A file that records each time something waited on the Maintainer
    without appearing on the list."

### Comprehension

*In plain terms* is clear, and defines "fence" at first use. C2, C3, C4 and C6
open plainly. C1 and C5 do not ([PR13]). Chunk M says "re-anchor", the name of
a ceremony the Maintainer runs.

### Coverage

**Covered.**

* **Scope fidelity.** Every A and C bullet of Revision 1, and the Decision,
  against the chunks and the Scope delta table.
* **Acceptance criteria.** Each read for whether it can fail.
* **Mechanics.** The frozen set, read from the manifest's keys and checked
  against a known key; the AST scope; twin identity; the finalize path through
  `_cmd_finalize_lockfile`.
* **Mapping.** Every test that reads each touched file, found by search.
* **The live tree.** The board rows, and the sibling plan's state.
* **The readings.** (a) to (c).

**Not covered / low confidence.**

* No suite and no board run, by brief. The [PR1] mutation was run as the pin's
  regex on the edited text, not under pytest.
* I did not count the plan's "some 57 install tests".
* The vendor-neutrality of lines not yet written cannot be checked.
* A same-type reviewer: no cross-type distance.
