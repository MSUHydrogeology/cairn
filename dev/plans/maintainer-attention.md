# Plan: maintainer attention — a list of what waits on the Maintainer, and no work left in archived plans

**Source proposal**: `dev/proposals/archive/2026-10-17-claude-maintainer-attention.md`
**Status**: ready-to-archive
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
* `bootstrap/tests/test_replacement_tools.py`, which gets five new nodes: five
  test functions, none parametrized, so the collection grows by exactly five.
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
* One new tracker, `dev/measurement/maintainer-view-misses.md` (C5).

**Not touched**, each checked by `git diff --stat` over the implementation
range:

* `AGENTS.md` and `templates/core/AGENTS.md`, `doctrine/session-routines.md`,
  `doctrine/proposals.md`: Part B's surfaces left with it.
* `bootstrap/_scaffold/`: so there is **no AST impact**.
* `CHANGELOG.md`, until the archive commit (C3, applied to this plan itself).
* `docs/tool-usage.md`: its "tools/board.py" entry describes the plain board,
  which does not change. It is not on the accepted documentation surface, and
  whether to add a `--maintainer` sentence there is a question put to the
  Maintainer in the Response.

**Frozen files.** One, `bootstrap/tests/test_replacement_tools.py`, read from
`bootstrap/tests/fixtures/gate_manifest.json` > `frozen_files`. Its bytes change,
and the gate manifest's pinned collection gains five nodes. Both join the
gate-manifest re-anchor already queued on `dev/PLANNING.md`; they start no new
ceremony.

The other files checked are not frozen: both `board.py` copies, both plan
templates, both `PLANNING.md` files, `doctrine/lifecycle.md` and
`doctrine/plans.md`. The instrument was checked against a known frozen key.
`bootstrap/tests/test_scope_reduction_trap.py` is also frozen; this plan reads it
and does not edit it.

**Lockfile.** `tools/board.py` is a verbatim lockfile record (source
`skills/_lib/board.py`), so changing it leaves the record's hash stale.

* C1 reconciles it with a scoped finalize of that one path, following the
  precedent `2ea3f869`. Any later edit to `tools/board.py` (a code-review fix)
  owes the same finalize in its own commit.
* `dev/plans/_template.md` already reports a hash mismatch in
  `bootstrap/verify_integrity.py --target .`. It is **not** finalized, because
  that would re-attest earlier, unreviewed drift.
* The lockfile schema is untouched.

### Sequencing with the sibling plans

`verification-practice` has landed its implementation chunks C1–C4 (`296cdfad`,
`0a4becdb`, `399d406d`, `f4d4ff3c`) and its Boundary B record (`739e3aba`, now
`awaiting-code-review`). Read against the tree at `739e3aba`:

* **`doctrine/plans.md`.** That plan edited "Boundary A", "Boundary B" and the
  record-validity sentence; this one edits "Mutability rule", "Accepted scope is
  a floor" and "Lasting-truth migration doctrine". No section overlaps.
* **Both plan templates.** That plan changed one word in the
  `verification-commands` slot ("substantive code surface" became "substantive
  surface"); this one edits other sections.
* **Its pins.** `bootstrap/tests/test_review_and_verification_rules_ship.py`
  reads only the two `AGENTS.md` copies, which this plan does not touch, so it
  is not in this plan's Boundary A.

Its code review is still ahead, and a `revising-code` fix could edit those files
again. So C2 and C3 **re-read the section they edit at edit time**. Both plans
commit to `master`; "rebases onto it" means only that. C1 and C5 touch none of
its files and start as soon as this plan is `ready-to-implement`.

Three other siblings:

* `independent-scientific-check` edits the templates' *Acceptance criteria*,
  which this plan does not touch.
* `neutrality-and-upgrade-slots` makes the neutrality checker stricter. Every
  line this plan adds names no vendor, HTML comments included.
* `dev/proposals/2026-10-18-claude-board-as-basis.md` (not yet decided, no plan
  yet) would change `tools/board.py`, its twin and the same lockfile record
  after C1 lands. Nothing here changes for it, except that C1 must land
  finalized, list each artifact once, and read active artifacts only under
  `--maintainer`.

### Found while planning, not widened

* **A placeholder in the template header would list as waiting.** The plan
  templates document the `Waiting on Maintainer` line in prose, and their header
  block carries no such line. Otherwise every plan copied from a template would
  list as waiting on the Maintainer.
* **The shipped board template's restatement.**
  `templates/core/dev/PLANNING.md` restates the archive precondition too. The
  accepted text gives that file only the marker line, and its restatement
  already says "This copy is not the source", so it is delivered as written.
  Because `doctrine/` is not installed in an adopter tree, the shipped
  *Dispositions* text states the archive rule in words rather than only citing
  it.
* **Two other mentions of sequencing.** `AGENTS.md` and
  `doctrine/dual-review.md` both say "sequencing may move work between chunks".
  The accepted C2 names `doctrine/plans.md` and the plan templates only, and
  "chunks" already means one plan's chunks, so neither changes.
* **A partial test class name.** `TestTheBoardReadsHeadersAndJudgesNothing`
  becomes a partial name once the board reads `dev/PLANNING.md` too. The
  accepted text puts the nodes in that class, and the property it pins, judging
  nothing, still holds. Renaming the class is not in scope.
* **A near-miss spelling is documented, not detected.** A line written
  `**Waiting on Maintainer:** …`, with the colon inside the bold, does not match
  the header rule. On a plan that mentions a fence, the advisory names it anyway,
  since no wait is declared. On a plan with no fence token (a deviation request)
  only the code-review check and the miss tracker catch it. The template
  preamble says the colon sits outside the bold. Detecting a second spelling
  would add a rule the accepted text does not have.

### Documentation / doctrine surface

| Layer | Files |
|---|---|
| Doctrine | `doctrine/lifecycle.md`, `doctrine/plans.md` |
| Templates | both plan templates; `templates/core/dev/PLANNING.md` |
| Deliberation | `dev/PLANNING.md`; the new tracker |
| Descriptive | none; no `docs/` page changes |

The rate-limit grounds are the proposal's, and the Decision ratified them.

## Sequence

The rows are in run order. The labels C1–C6 and M keep the plan review's and
the Response's references, so C5 runs second and C2's gate names it.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | **A new command lists everything waiting on the Maintainer.** `python tools/board.py --maintainer` reads active artifacts only (`--archive` has no effect on it) and prints one entry per item, with the columns kind, artifact, reason and text:<ul><li>an artifact whose status begins `awaiting-decision`, or whose header carries `**Waiting on Maintainer**:`, appears **once**, however many ways it qualifies (reason `awaiting-decision` or `declared`);</li><li>a `dev/PLANNING.md` line that matches the **row form** below appears as kind `roadmap`, named `dev/PLANNING.md:<line>`;</li><li>**row form**: after leading spaces and one optional `* ` or `- `, the line is `**Waiting on Maintainer**: <what>`, read by the same rule as a header field. A mention inside a sentence or in backticks is not a marker, and a line with no text still counts as declared, so a blanked line stays visible;</li><li>one advisory footer line, always printed (`none` when empty), names each active plan whose body has `MAINTAINER-GATED` or `MAINTAINER-ONLY` and whose header has no Waiting line;</li><li>the footer names pushes (`git status`) and anything undeclared as unlisted, and names a missing `dev/PLANNING.md`.</li></ul>The field joins `_FIELDS`. The docstring's "and nothing else", the usage block and the help text are rewritten to name the two new reads; the plain-mode footer is unchanged. Twin byte-identical. Five nodes in `TestTheBoardReadsHeadersAndJudgesNothing`, each red on the parent commit. Scoped finalize of `tools/board.py`. The commit sets Status to `implementing`. | `ready-to-implement` | one commit |
| C5 | **A file that records each time something waited on the Maintainer without appearing on the list.** `dev/measurement/maintainer-view-misses.md`, forked from `dev/modules/incident_log_template.md`, with a 30-day window and **one** event class covering both sources: a code-review "waiting-line miss" finding, and anything the Maintainer reports as waiting without being listed, board rows included. Its Purpose says what two rows in the window mean: declaring is the wrong design (Revision 1), not only a rate-limit suggestion. The commit also drops this plan's `Proposed paths:` line, as the template says once a path resolves. It runs before C2 so Cairn's own template can name the file. | `ready-to-implement` | one commit |
| C2 | **The line, written down.** Doctrine and templates say what the Waiting line is and when to write it:<ul><li>`doctrine/lifecycle.md` gains the exception to "status alone names the holder": inside a plan, the Waiting line names a Maintainer gate;</li><li>`doctrine/plans.md` > "Mutability rule" lists the line beside Status;</li><li>both plan templates get a **preamble** paragraph (above the rule, so not copied into a plan) that gives the exact form, says it goes in the header block beside Status, names the three triggers (a fenced chunk, a `defer` batch, a deviation request), says to delete it when answered, gives the 48-character budget, says change notes (`dev/plans/<slug>.md`) carry it too, and says the colon sits outside the bold;</li><li>the sentences that **are** copied into a plan say where it goes: *Sequence* (write it when work reaches a fenced chunk) and *Dispositions* (write it with a `defer` batch), each "in the header block, beside Status";</li><li>the *Code review* check: `git log -p` on the plan shows a Waiting line for each fenced chunk whose fence became the next move inside the reviewed range, and for each deviation request made in it. A fence the range did not reach is not checked, and one whose wait is declared on a marked board row is checked there. A missing line is a finding, recorded in the miss tracker: Cairn's copy names `dev/measurement/maintainer-view-misses.md`, the shipped copy says "the project's incident tracker";</li><li>`templates/core/dev/PLANNING.md` gets one line stating the row marker, in the row form C1 fixes.</li></ul> | C1, C5; re-read each section at edit time | one commit |
| C3 | **Archived files are records.** Nothing still to be done may live only in an archived file:<ul><li>`doctrine/lifecycle.md` > "Archive precondition" gains the rule, the live-home definition, and the negative clause: a pointer to an archived artifact, or to an unopened plan, is not a live home;</li><li>`doctrine/plans.md` > "Accepted scope is a floor" gains "of a live plan", the hand-off clause (work handed to an unopened plan is a `defer`, with a board row listing the items) and the Q2 rule (a quoted Decision authorizes a later-plan `defer` only when the accepted text **assigns** that work to that plan; a plan that simply fell short is not an assignment);</li><li>`doctrine/plans.md` > "Lasting-truth migration doctrine" gains changelog-at-archive;</li><li>both templates gain, in *Scope delta*, "of a live plan", the hand-off clause and the Q2 rule; and in *Dispositions* the archive rule in words, the changelog line, and the sentence that an archiving plan carries no Waiting line (a wait still open then moves to a marked board row).</li></ul> | C2; re-read each section at edit time | one commit |
| C4 | **Today's waiting rows are marked.** One commit to `dev/PLANNING.md`, under the Decision's instruction (quoted verbatim in the body):<ul><li>claim the file and read the active set first (`python tools/intent.py claim`, then `list`);</li><li>the marker is stated once, inline in backticks and never as a line-initial example, in the row form;</li><li>a row is marked when its next move is one only the Maintainer can make: a ceremony only they run, a question only they answer, a go-ahead only they give. An authorized deferral whose next move is anyone's is not marked. Marked: the gate-manifest re-anchor row and the stage-reader row's question (3), plus any others a sweep of the whole board finds; the commit body lists each with its reason;</li><li>one line joins the *Archive preconditions* restatement for C3's rule.</li></ul> | C1, C3 | one commit |
| C6 | **Boundary B, then the record.** The whole suite runs once on the finished work, and the result is written down: full mode (*Verification*), then `## Implementation verification`. Status moves to `awaiting-code-review`. | C1–C5 | one commit |
| M | **MAINTAINER-ONLY — no new ceremony.** The *re-anchor* is the supervised ceremony, run only by the Maintainer, that brings the gate manifest up to date with the changed tests (`bootstrap/REANCHOR_RUNBOOK.md`). `bootstrap/tests/test_replacement_tools.py` and its five new node IDs join the re-anchor row already queued, which C4 marks, so M needs no Waiting line in this plan: the wait is declared on that row. **An implementing agent must not perform the re-anchor.** The agent's part is the board note at archive. | code review cleared | Maintainer |

**Shared-file discipline.** C4 claims `dev/PLANNING.md` with `python
tools/intent.py claim` and reads `python tools/intent.py list` before editing,
because the file is a coordination surface (`doctrine/coordination.md` >
"Required signal+read for coordination-surface files"). A commit by path takes
the whole file, so C4 checks the diff before committing (see its criteria).

## Acceptance criteria

**Reading these criteria.** Each ends with *Red when*: a change that turns it
red. Prose checks use `count(file, section, phrase)`, the number of times a fixed
phrase occurs in a section of a file, taken on whitespace-collapsed text (as the
existing pins do), the section running from its heading to the next heading of the
same or higher level. A count of a new phrase is taken at the chunk's parent and
must be 0 there, then the stated number at the chunk's commit. These are one-shot
checks the implementer runs and records; no standing test pins the new prose,
because the accepted evidence plan names five nodes. Boundary C attacks the prose.

### C1

Every node builds a scratch tree in `tmp_path`.

* **Node 1 lists exactly the declared set.** The tree holds:
  * listed: a proposal at `awaiting-decision`; a proposal whose status reads
    `awaiting-decision — note`; a plan carrying the line; a plan whose line has
    no text; a proposal that is both at `awaiting-decision` and carrying the
    line (**one** entry); a `dev/PLANNING.md` line indented two spaces; a
    `dev/PLANNING.md` sub-bullet line (`  * **Waiting on Maintainer**: …`);
  * not listed: a proposal at `awaiting-review`; a plan with no line; an archived
    plan carrying the line.

  *Red when:* the status is compared exactly (the decorated one drops); the board
  file is not read; the sub-bullet form is not matched; the both-ways artifact
  prints twice; an empty line is dropped; or an archived artifact appears.
* **Node 2 names a fence with no declared wait, and only a live plan.** An active
  plan with a fence token in its body and no Waiting line is named on the
  advisory line and is not listed as waiting. An archived plan, a `_template.md`
  and an active proposal, each with a fence token and no line, are named nowhere,
  with and without `--archive`. With none qualifying, the advisory line reads
  `none`. *Red when:* the advisory code is deleted, **in a throwaway `git
  worktree` at C1's commit** (the test loads `tools/board.py` from the tree it
  sits in, so a scratch copy would never be read); archives are scanned;
  `_`-prefixed files are not skipped; or the empty case prints nothing.
* **Node 3 ignores a mention.** A `dev/PLANNING.md` line that names the marker
  mid-sentence or inside backticks is not listed. *Red when:* the matcher is
  loosened to a substring search.
* **Node 4 names the gaps.** The footer names pushes and undeclared items as
  unlisted. On a tree with no `dev/PLANNING.md`, it names the missing file and
  the artifact entries still list. *Red when:* a missing file reads as zero rows
  without a word.
* **Node 5 encodes every value.** A control character (ESC) in a header value,
  in a row value, and in an artifact name printed on the advisory line or in a
  listed entry comes out escaped. *Red when:* any one of the three prints raw.
* **Exactly five nodes.** `pytest --collect-only -q
  bootstrap/tests/test_replacement_tools.py` shows five more nodes than at the
  parent. *Red when:* a node is parametrized or split.
* **Red before the code.** Run the five nodes against C1's parent, in a throwaway
  worktree at the parent with only the new test file copied in. Each fails
  because `--maintainer` is unknown, not on an import error. The commit body names
  the parent SHA and the failure. *Red when:* any node passes at the parent.
* **The plain board is unchanged.** Run the parent's `board.py` and the new one
  against the same `--root`, once on the live tree and once on a scratch tree
  with no Waiting line; `cmp` of the two outputs exits 0. *Red when:* the new
  column or any new footer text appears in plain mode.
* **The tool describes itself truly.** `python tools/board.py --help` names
  `--maintainer` and no longer says "header blocks only"; the docstring's "and
  nothing else" names the two `--maintainer` reads; the plain-mode footer line is
  unchanged. *Red when:* the old help sentence is left in place.
* **The two copies are identical.** `cmp tools/board.py
  templates/skills/_lib/board.py` exits 0, and the twin-parity test in
  `bootstrap/tests/test_notice_install.py` passes. *Red when:* either copy is
  edited alone.
* **No new subprocess.** First run the pattern on `tools/session.py` and see it
  match, which shows the instrument can fire. Then `grep -nE "import
  subprocess|subprocess\.|Popen|os\.system|os\.popen" tools/board.py` prints
  nothing. If a docstring trips it, reword the docstring, not the pattern.
  *Red when:* `import subprocess` is added.
* **The lockfile.** After `python bootstrap/scaffold.py upgrade --target .
  --finalize tools/board.py`, the lockfile diff touches only the `tools/board.py`
  record, and `python bootstrap/verify_integrity.py --target .` reports the same
  findings before and after C1, none for `tools/board.py`. *Red when:* the
  finalize is skipped (`tools/board.py` appears) or run unscoped (other records
  change).
* **A day-one figure.** The commit body records the advisory line the live tree
  prints, the starting figure for the "noisy check" signal. *Red when:* it is
  absent.

### C5

* **The tracker is a real tracker.** It has the template's sections, an empty
  `## Incidents` table, `**Rolling window**: 30 days`, and a *What counts* that
  names **one** `Class name` and says both sources count under it; its Purpose
  says two rows in the window mean declaring is the wrong design. *Red when:* a
  second `Class name` entry exists, or the window line is missing.
* **It is read, not skipped.** `python tools/evolution_infer.py` lists it among
  the trackers read, not under `SKIPPED`, and exits 0. *Red when:* the
  `## Incidents` heading is removed.
* **The two sources add up.** A scratch copy with two `occurred` rows dated today
  under the file's class, one described as a code-review finding and one as a
  Maintainer report, makes `python tools/evolution_infer.py --trackers <scratch
  copy>` print a rate-limit suggestion for that class. *Red when:* the file
  defines two classes (the rows then carry different names and no suggestion
  fires) or the window line cannot be parsed (exit 3).
* **The prose gates are clean** on the tracker, and `claim_check` on this plan is
  clean after its `Proposed paths:` line is dropped.

### C2

* **`doctrine/lifecycle.md` carries the exception.** `count(doctrine/lifecycle.md,
  "The proposal lifecycle", "Waiting on Maintainer")` is 1. *Red when:* the
  sentence is removed.
* **"Mutability rule" lists the line.** `count(doctrine/plans.md, "Mutability
  rule", "Waiting on Maintainer")` is 1. *Red when:* it is removed.
* **The preamble tells an author everything.** In each template, the paragraph
  that opens `**The Waiting line.**` (above the rule) contains each of: `fenced
  chunk`, `defer`, `deviation`, `delete`, `48`, `beside Status`, `colon`,
  `dev/plans/<slug>.md`. *Red when:* any one is missing; the check prints a line
  per missing term.
* **The copied sentences say where.** Below the rule, at C2's commit, `in the
  header block, beside Status` occurs 2 times in each template (*Sequence*,
  *Dispositions*).
  *Red when:* one drops the words, as a sentence that omits "header" would put the
  line where the board does not read it.
* **The *Code review* check is exact.** In each template's *Code review* section,
  `git log -p`, `became the next move`, `is not checked` and `marked board row`
  each occur once. Cairn's copy names `dev/measurement/maintainer-view-misses.md`
  once and the shipped copy says `the project's incident tracker` once and names
  no Cairn path. *Red when:* the "not reached" clause is dropped (the false-miss
  case returns) or the shipped copy names a Cairn path.
* **The added text is identical in both templates, but for the tracker name.**
  Take each template's added lines from C2's diff, leave out
  `cairn-internal-ref-allow` lines, replace the tracker path with `the project's
  incident tracker` in Cairn's, and `diff` exits 0. *Red when:* a word differs in
  one copy.
* **No template line begins with the marker.** `grep -nE '^ *([*-] )?\*\*Waiting
  on Maintainer\*\*' dev/plans/_template.md templates/core/dev/plans/_template.md`
  prints nothing, so a copied plan carries no live line. *Red when:* the
  preamble or header shows the line-initial form.
* **The shipped board line states the row form.** In
  `templates/core/dev/PLANNING.md`, `Waiting on Maintainer` occurs once (on
  collapsed text); the sentence says the marker goes inside the row, when the
  row's next move is the Maintainer's, in the row form C1 fixes; and no line of
  the file begins with the marker (the `grep -nE` above, run on this file,
  prints nothing). *Red when:* it is written as a line-initial example.
* **A fresh install lists nothing, with the installed tool.** Install into a
  scratch tree with `bootstrap/scaffold.py` (the `collaborative-team` preset
  works), `cd` into it and run its own `python tools/board.py --maintainer`. It
  exits 0 and lists zero entries. This also shows the shipped twin and encoder run
  in an adopter tree. *Red when:* the new `PLANNING.md` line lists itself.
* **`python scripts/check_cairn.py` passes.** Any new `doctrine/` reference in a
  shipped template carries its `cairn-internal-ref-allow` marker. *Red when:* a
  reference lacks one.

### C3

* **The rule and its negative clause are in place.** In
  `doctrine/lifecycle.md` > "Archive precondition", `only home` occurs once (the
  rule: nothing still to be done may have an archived artifact as its only home),
  `is not a live home` once (a pointer to an archived artifact or an unopened plan
  is not one), `by number` once (the issue home), and `board row` at least once.
  *Red when:* the negative clause is dropped.
* **Sequencing stays within a live plan.** `of a live plan` occurs once in
  `doctrine/plans.md` > "Accepted scope is a floor" and once in each template's
  *Scope delta*. *Red when:* a copy keeps the unqualified sentence.
* **The hand-off clause is in place.** `board row listing the items` occurs once
  in the same doctrine section and once in each template's *Scope delta*. This is
  the clause that closes the six-plan failure. *Red when:* it is dropped.
* **The Q2 rule says "assigns".** `assigns` occurs once in that doctrine section
  and once in each template's *Scope delta*, with the `defer` line quoting the
  assigning sentence and the Decision. *Red when:* the word reverts to "names".
* **Changelog at archive.** `writes its own changelog entry` occurs once in
  `doctrine/plans.md` > "Lasting-truth migration doctrine" and once in each
  template's *Dispositions*. The `NEXT_SESSION.md` sentences in that section are
  unchanged: C3's diff of `doctrine/plans.md` has no changed line containing
  `NEXT_SESSION`. *Red when:* either is edited.
* **The shipped *Dispositions* states the rule in words.** In each template,
  `only home` occurs once and `carries no Waiting line` once, so an adopter, who
  has no `doctrine/`, meets the rule itself. *Red when:* it cites a doctrine file
  and nothing else.
* **The standing pins pass unchanged.**
  `bootstrap/tests/test_scope_reduction_trap.py` passes at C3's commit with the
  phrases "Sequencing is free; removal is not" (doctrine) and "Sequencing is free"
  (templates) intact.
* **The pins still read these sentences.** In a throwaway worktree at C3's
  commit, delete the **whole** edited sentence from each template (both "Sequencing
  is free" and "moving work between chunks", since the pin accepts either) and
  "Sequencing is free; removal is not" from `doctrine/plans.md`. The test reads the
  files of the tree it sits in, so only a worktree can show this. Three nodes go
  red, and the record names them: `dev/plans/_template.md::sequencing between
  chunks owes nothing`, `templates/core/dev/plans/_template.md::sequencing between
  chunks owes nothing` and `doctrine/plans.md::sequencing is free, removal is
  not`. *Red when:* fewer than those three do, which means a second phrase still
  satisfies a pin; or more do, which means the deletion reached beyond the
  sentence.

### C4

* **The live list holds the named rows.** `python tools/board.py --maintainer` on
  the live tree lists, as kind `roadmap`, at least the gate-manifest re-anchor
  row and the stage-reader row's question (3), plus each row the sweep marked.
  *Red when:* a named row is unmarked.
* **Every marker value is short.** Each is under 48 characters, so `python
  tools/board.py --maintainer | grep -c '…'` prints 0. *Red when:* a value runs
  long.
* **Nothing lists itself.** The number of `roadmap` entries equals the number of
  rows the commit body says it marked, so the statement line and the restatement
  line are not markers. *Red when:* the statement is written as a line-initial
  marker (the count is one too high).
* **The commit is narrow.** `git show --stat` shows one file, `dev/PLANNING.md`,
  and its hunks (`git diff -U0 dev/PLANNING.md` before committing) are exactly
  the marks, the statement and the restatement line, each accounted for in the
  body. *Red when:* a hunk is another session's unfinished edit; stop and
  coordinate.
* **Every mark has a reason, and the Decision is quoted.** The body names each
  marked row and why its next move is the Maintainer's, and quotes the Decision's
  authorization verbatim and visually isolated:
  `git show -s --format=%B <C4> | grep -cF "Accept A, B, C and D as revised, with
  every recommended answer, including B’s scope cut and D’s scope delta."`
  prints 1. *Red when:* it is paraphrased (prints 0). A deferral already
  authorized, whose next move is anyone's, is queued work and is not marked.
* **The pinned restatement text survives.**
  `bootstrap/tests/test_scope_reduction_trap.py` passes at C4's commit, because it
  pins the *Archive preconditions* text of both `PLANNING.md` files.

### C6

* **The record is complete.** `## Implementation verification` carries each field
  *Verification* lists (mode, tested commit, reviewed range, interpreter, pre-run
  and post-run state, the command table, non-pass disposition, plan-specific
  commands, known omissions), and lists the five new node IDs, which match
  `pytest --collect-only -q` for the five added nodes. *Red when:* a field label
  is absent or an ID differs.

## Scope delta

**Scope delta**: preserved. The baseline is Revision 1 as accepted, and every
outcome in it maps to a chunk:

| Accepted outcome | Chunk |
|---|---|
| the line in plans and change notes | C1, C2 |
| the "Mutability rule" line | C2 |
| the line in `dev/PLANNING.md` rows, and its form | C1, C4 |
| `--maintainer`, column | C1 |
| declare and check | C1 |
| the footer | C1 |
| today's rows marked | C4 |
| the lifecycle.md exception | C2 |
| the docstring | C1 |
| the archive rule, its live-home definition, and the clause that a pointer to an archived artifact or an unopened plan is not a live home | C3 |
| a pointer from *Dispositions*, and one line in the board's restatement | C3, C4 |
| sequencing within a live plan | C3 |
| work handed to an unopened plan is a `defer`, with a board row listing the items | C3 |
| Q2: a quoted Decision authorizes a later-plan `defer` only when the accepted text assigns the work | C3 |
| changelog at archive | C3 |
| the tracker and its code-review check | C2, C5 |
| the shipped `PLANNING.md` line | C2 |
| five test nodes | C1 |
| Boundary B full | C6 |

Part B is not in this baseline: the Decision cut it before this plan opened.

One accepted example changed: the "Four deferred Maintainer questions" row was
retired at `30ff0cd5`, because all four questions were settled. The outcome,
"today's waiting rows are marked", is still delivered for the rows that wait
now. A wait that ended is not a removal.

## Verification

**Boundary A (iteration, scoped).** Each chunk runs the tests that own the files
it touches, plus `python scripts/check_cairn.py` and `python
scripts/claim_check.py` on each edited document.

| Chunk | Tests |
|---|---|
| C1 | `test_replacement_tools.py`, `test_notice_install.py` (twin byte-identity and SPDX header), `test_session_kernel.py`, `test_security_lint.py`, `test_skills_upgrade.py`, `test_skills_self_heal.py`, `test_verify_integrity.py` |
| C2, C3 | `test_scope_reduction_trap.py`, `test_verification_boundaries.py`, `test_scaffold.py`, `test_claim_check_module.py`, `test_loop_fidelity_gate.py`, `test_documentation_plan_module.py`, `test_quickstart_sequence.py`, `test_core_dev_folders.py`, `test_upgrade.py`, `test_module_merge_lockfile.py`; C2 also the four tests that render the shipped `PLANNING.md`: `test_onboarding_seed_roster.py`, `test_onboarding_slot_substitution.py`, `test_onboarding_activation_helper.py`, `test_skills_onboarding.py` |
| C4 | `test_scope_reduction_trap.py` (it pins the *Archive preconditions* text of both `PLANNING.md` files), then the claim and prose gates |
| C5 | the claim and prose gates; `python tools/evolution_infer.py` |

All tests are in `bootstrap/tests/`. The C2 and C3 set is not a confident bound:
57 test files drive a scaffold install, which renders the shipped plan template
(counted in the `verification-practice` plan). So Boundary B is the real check.

**Known omission.** No standing test pins the new C2–C4 prose. The accepted
evidence plan names five nodes and no prose pin, and a pin file would be a new
frozen-file ceremony. The prose is checked once, by the counts above, and again by
Boundary C. The older pins in `test_scope_reduction_trap.py` protect only the
sentences they already read, which is why C3 shows they still do.

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

**How it runs.** After the last implementation chunk (C4), against a clean,
unchanged commit, under the canonical interpreter (Python 3.13.x, as
`tools/session.py` resolves it):

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
* **The row form.** Does the parser match exactly the form the instructions
  document, and nothing an author would write by accident: a mention in
  backticks, mid-sentence, or a fenced example?
* **The near-miss spelling.** `**Waiting on Maintainer:**`, colon inside the
  bold: does the preamble say it is wrong, and does a fenced plan written that way
  show on the advisory?
* **Reached or not.** Can a code reviewer, reading the *Code review* sentence
  alone, tell a fence the range reached from one it did not?
* **The shipped template, read cold as an adopter.** Can you follow the Waiting
  line, the archive rule and the *Code review* check without `doctrine/`?
* **The lockfile diff.** Is it confined to one record?

**Security preflight.** N/A, as in the proposal: no trust boundary is added,
moved, or widened. The new read is a fixed path holding the same class of
Markdown the board already reads, through the same encoder, with no subprocess;
the file names the advisory prints are encoded too (C1 node 5). The chunking
changes no answer.

## Dispositions

*Filled at archive-preparation.* Three items are known now:

* **The archive commit writes this plan's `CHANGELOG.md` entry**, applying C3
  to itself.
* **It adds a note to the queued re-anchor row** naming
  `test_replacement_tools.py` and the five node IDs (chunk M).
* **This plan carries no Waiting line at archive**, applying C3 to itself: the
  open wait, the re-anchor, is declared on its marked board row.

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

## Response to plan review -- Claude Sonnet 5.5 (author) -- 2026-10-18

This answers the Internal plan review at `7d9e1637` (reviewed commit
`c61da58b`). I took the plan over from its first author. I checked each finding
against the tree at `739e3aba` before folding it, and reproduced [PR1]'s
mutation in a scratch copy of the pin test and its 17 surfaces: deleting only
"Sequencing is free" left all 99 nodes green, and deleting the whole sentence
turned exactly three red. All thirteen findings are answered: eleven accepted,
two in part ([PR9], [PR10]). Each is answered in an operative cell, and this
table points at them.

**What changed since the plan opened.**

* `30ff0cd5` retired the "Four deferred Maintainer questions" row, which is
  [PR2]'s trigger.
* `verification-practice` landed C1–C4 and its Boundary B record. None of its
  edits overlaps a section this plan edits; its code review is still ahead.
* A new proposal, `dev/proposals/2026-10-18-claude-board-as-basis.md`, builds on
  C1 and is noted in *Scope* > "Sequencing with the sibling plans".

| Finding | Disposition | Where |
|---|---|---|
| [PR1] C3's pin check cannot fail | accepted | *Acceptance criteria* > C3, "The pins still read these sentences": a throwaway worktree, the whole sentence removed from each template, and the three node IDs that must go red. *Acceptance criteria* > C1, node 2, now names a throwaway worktree in place of "a scratch copy". |
| [PR2] C4 names a retired row, and its marking rule contradicts its first example | accepted | *Sequence* > C4 names the two rows that remain plus the sweep, and states the marking test in the review's words. *Acceptance criteria* > C4 reads "at least" those two. *Scope delta* records that the retired row was a wait that ended, which is not a removal. |
| [PR3] the check counts a fence the work never reached | accepted | *Sequence* > C2, the *Code review* check: a fence "inside the reviewed range", "not reached" is not checked, and a wait declared on a marked board row is checked there. M declares its own wait on the marked re-anchor row. *Acceptance criteria* > C2, "The *Code review* check is exact". |
| [PR4] the form of a board-row marker is left to code review | accepted, the reviewer's grammar | *Sequence* > C1 defines the row form once. Node 1 lists the indented and sub-bullet forms and node 3 keeps the backticked negative. C2's shipped line and C4's statement use that form, and Boundary C's bullet becomes "The row form". One refinement: the parser reuses the header-field rule, so there is one grammar rather than two, and a line with no text counts as declared. |
| [PR5] two accepted clauses have no home | accepted | *Sequence* > C3 and *Acceptance criteria* > C3 carry both: the negative live-home clause in `doctrine/lifecycle.md`, and the hand-off-is-a-`defer` clause in `doctrine/plans.md` and both templates' *Scope delta*. *Scope delta* splits the row that hid them. Q2 also states that a plan which simply fell short is not an assignment, which is Revision 1's own last sentence on the point. |
| [PR6] C2's criteria do not check what the text tells an author | accepted, all five | *Acceptance criteria* > C2: the preamble's eight terms, "in the header block, beside Status" twice per template, and the shipped `PLANNING.md` line. *Acceptance criteria* > C3: the shipped *Dispositions* states the rule in words and "carries no Waiting line". *Dispositions* applies that last rule to this plan. The fifth applies Revision 1's accepted archive rule to waits; it adds no outcome. |
| [PR7] Cairn's template should name the tracker | accepted | *Sequence* > C2 (Cairn's copy names `dev/measurement/maintainer-view-misses.md`, the shipped copy keeps the portable phrase); *Acceptance criteria* > C2 allows exactly that one difference. C5 runs second and C2 gates on it. The rows are in run order and the labels are kept, so this table, the review and the Response still cite the same names. |
| [PR8] Boundary A misses three readers | accepted, all four | *Verification* > Boundary A table. I dropped `test_review_and_verification_rules_ship.py`: it reads `templates/core/AGENTS.md` and `AGENTS.md` only, and this plan touches neither. |
| [PR9] pin where the advisory does not look | accepted in part | **Accepted:** node 2's three negatives with and without `--archive`; `--maintainer` reads active artifacts only and ignores `--archive` rather than refusing it, because Cairn's tooling warns and does not block; node 5 covers names printed on the advisory line; C1's body records the day-one advisory figure. *Sequence* > C1 and *Acceptance criteria* > C1. **Declined:** detecting the `**Waiting on Maintainer:**` near-miss. On a plan that mentions a fence the advisory already names it, since no wait is declared. On a plan without one it is a deviation request, which the code-review check and the miss tracker exist for. Detecting a second spelling adds a rule to a contract Revision 1 fixes as one field. Instead the preamble says where the colon goes, and Boundary C attacks it. See *Scope* > "Found while planning". |
| [PR10] the tool's description becomes false | accepted in part | **Accepted:** the docstring, usage block and help text name the two reads, and the plain-mode footer stays byte-identical, which is why `--maintainer` carries its own footer. *Sequence* > C1; *Acceptance criteria* > C1, "The tool describes itself truly". **Declined:** the `docs/tool-usage.md` sentence. That page describes the plain board, which does not change, so nothing on it becomes false; it is not on the accepted documentation surface. Put to the Maintainer as the question below. |
| [PR11] C4's shared-file steps | accepted, all three | *Sequence* > C4 and *Shared-file discipline*: claim as well as list; the diff-hunk check; the Decision quoted verbatim. *Acceptance criteria* > C4 gives the `grep -cF` that fails on a paraphrase. |
| [PR12] the tracker should count both sources together | accepted | *Sequence* > C5 and *Acceptance criteria* > C5: one event class, a Purpose that says what two rows mean, and "The two sources add up", a scratch tracker run through `evolution_infer.py`. |
| [PR13] small mechanics, and two first sentences | accepted, all six | C1 and C5 gate on `ready-to-implement`. *Acceptance criteria* > C1: the parent SHA the nodes failed against, and the subprocess pattern, run first on `tools/session.py` to show it can match. *Acceptance criteria* > C2: a fresh install runs its own installed `tools/board.py` (I ran this once on the current board, which works). *Scope* > "Sequencing with the sibling plans" and C2 and C3's gates: re-read at edit time. C1 and C5 open on the suggested sentences. |

The comprehension note is also folded: chunk M now says what the re-anchor is.

**Calls I made while folding.** Each is a detail the plan had to settle because
two readings would diverge silently. None adds an outcome.

* An artifact's status is matched on its first word, so `awaiting-decision —
  note` still lists. A silent drop is the failure this feature exists to remove.
* An artifact is listed once, however many ways it qualifies, and a Waiting line
  with no text counts as declared.
* `--maintainer` ignores `--archive`.

**Question for the Maintainer.** Should C1 also add one sentence about
`--maintainer` to `docs/tool-usage.md`? *Recommended: no.* The page describes the
plain board, which does not change, and the board-as-basis proposal edits that
same entry next and can describe both flags in one edit. If you say yes, C1
gains that one sentence and nothing else changes. Nothing waits on the answer:
the plan is complete without it.

**Scope.** Nothing accepted is dropped, and *Scope delta* stands at `preserved`.
Two edits go a little past Revision 1's wording, and both answer a finding:

* [PR3] makes "in the reviewed range" exact: a fence the range reached.
* [PR6]'s last item states, in the one place an archiving author reads, that an
  archiving plan carries no Waiting line.

There is no second plan-review round. Status `revising-plan` ->
`ready-to-implement`.

## Implementation verification -- Claude Sonnet 5.5 -- 2026-10-18

**Boundary B mode**: full. All four refusal grounds in *Verification* held: a frozen
file's bytes and pinned collection changed (`test_replacement_tools.py`), a tool
adopters run and two shipped templates were edited, a lockfile record was
reconciled, and the accepted text says "Boundary B runs full".

**Tested commit**: `31d9cefeccabdf50ad2ee6d7a3cd2a6ff20bfe35` (C4, the last
implementation commit).

**Reviewed range**: `8e5df0f0af778759bb7c80a28204ce593dd97615` (the plan at
`ready-to-implement`) to `31d9cefeccabdf50ad2ee6d7a3cd2a6ff20bfe35`. This plan's
five commits are C1 `72254d0eeae5eef180dbde3ed01303870ecca140`, C5
`42fa680488c826de0135bd218921167e2b7f67ca`, C2
`c5c2c38fc1f4e71c839438a149a12de2967e7096`, C3
`753f7fedfa49fc0ed15a063d07b6a868f130f3da` and C4
`31d9cefeccabdf50ad2ee6d7a3cd2a6ff20bfe35`, in run order. Other sessions'
commits sit inside the range; none of them touches a file of this plan (checked
with `git show --name-only` over the five commits: only the planned files).

**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python
3.13.13.

**Pre-run state**: a detached `git worktree` at the tested commit, outside the
shared tree; `git rev-parse HEAD` = the tested commit, `git status --short` empty.
**Post-run state**: same `HEAD`, `git status --short` empty. The worktree shares
refs, so `refs/cairn/gate-anchor` was present, and other sessions' uncommitted
files were absent.

| Command | Exit | Outcomes | Elapsed |
|---|---|---|---|
| `CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0` | 0 | 3384 passed; 0 failed, 0 skipped, 0 xfail, 0 xpass; 3 warnings (a deprecation inside a third-party package, `stevedore`) | 1071.91 s (1077 s wall) |
| `python scripts/quality_gate.py --sub neutrality --sub redundancy` | 1 | neutrality fail=74, info=21; redundancy fail=0 | 2 s |
| `python scripts/check_cairn.py` | 1 | 5 issues in 181 files, all `cited path does not resolve` for two local-only files | 3 s |

**Non-pass disposition.**

* **Neutrality, 74 failures.** The 74 `file:line: token` lines are identical at
  the plan's parent `8e5df0f0` and at the tested commit (`diff` of the sorted
  lists exits 0). They fall in 22 files, none of which any of the five commits
  touched, so no hit is on a line this plan added. No vendor name appears in any
  added line.
* **`check_cairn.py`, 5 issues.** The worktree is a clean checkout, so it lacks
  `dev/measurement/suite-runs.jsonl` and `dev/measurement/suite-cost.md`, which
  are local-only files (`git ls-files` returns nothing for either) cited by
  `dev/plans/verification-practice.md` and
  `dev/reviews/2026-08-27-code-review-c5-c6-removals.md`. Neither file is in this
  plan's range. The same script in the shared working tree, which holds those
  files, printed `OK -- 181 Markdown file(s) scanned; no issues` at C4. This
  plan's own files carry no flag.
* **`test_gate_manifest.py`** passed, as the plan expected. The frozen file's
  changed bytes and the five added nodes do not redden it; the re-anchor is
  chunk M and was not run.

**Plan-specific acceptance commands.** Each ran at the commit named in its row; a
count is *parent -> tested*.

| Check | Where | Outcome |
|---|---|---|
| Five new nodes | tested commit | `pytest --collect-only -q bootstrap/tests/test_replacement_tools.py`: 15 at `8e5df0f0`, 20 now. The five added IDs, all in `TestTheBoardReadsHeadersAndJudgesNothing`: `test_maintainer_lists_exactly_what_authors_declared`, `test_a_fence_with_no_declared_wait_is_named_not_listed`, `test_a_mention_of_the_marker_is_not_a_marker`, `test_the_footer_names_what_the_list_cannot_see`, `test_every_value_the_view_prints_is_encoded` |
| Red before the code | parent `8e5df0f0`, test file copied in | all five fail with `SystemExit: 2`, `unrecognized arguments: --maintainer`; none on an import error |
| Mutations, C1 | overlay of C1's files on the parent; node 2 again at `72254d0e` | 15 mutations each turned the intended node red (exact status match, board file unread, sub-bullet unmatched, double listing, empty line dropped, archives read, advisory deleted, `_` files read, empty case silent, substring matcher, missing file silent, header/row/entry-name/advisory-name printed raw). Deleting the advisory at `72254d0e` itself: node 2 red |
| Plain board unchanged | `--root` = live tree and a scratch tree, with and without `--archive` | parent's `board.py` and the new one: `cmp` exits 0 each time; with a Waiting line added, the column appears (the instrument can fire) |
| Twins, subprocess, help | C1 and tested commit | `cmp` of the two `board.py` copies exits 0; the subprocess pattern matches `tools/session.py` and prints nothing on `tools/board.py`; `--help` names `--maintainer` and no longer says "header blocks only" |
| Lockfile | C1 and tested | the C1 lockfile diff is one line (`tools/board.py` `hash`); `verify_integrity --target .` lists the same 18 files before and after C1, C2, C3 and at the tested commit, none for `tools/board.py` |
| Tracker, C5 | working tree and scratch copies | `evolution_infer.py` lists it among the trackers read (0 rows, 30-day window), exit 0; a copy with two `occurred` rows dated today prints a rate-limit suggestion for `waiting-line-miss`; two class names -> no suggestion; window line removed -> exit 3; `## Incidents` heading removed -> exit 3 by name and `SKIPPED` in discovery |
| Prose counts, C2 | the commit before C2 | lifecycle "The proposal lifecycle" 0 -> 1, "Mutability rule" 0 -> 1; both templates: preamble holds all 8 terms, `in the header block, beside Status` 2 below the rule, *Code review* `git log -p` / `became the next move` / `is not checked` / `marked board row` 0 -> 1 each; Cairn's copy names the tracker once and the shipped copy says `the project's incident tracker` once; the added lines diff identical across the two templates once the tracker is swapped (a one-word change turns it 1); no line begins with the marker |
| Prose counts, C3 | the commit before C3 | lifecycle "Archive precondition": `only home`, `is not a live home`, `by number`, `board row` 0 -> 1; plans.md "Accepted scope is a floor": `of a live plan`, `board row listing the items`, `assigns` 0 -> 1; "Lasting-truth migration doctrine": `writes its own changelog entry` 0 -> 1; each template: *Scope delta* three, *Dispositions* `writes its own changelog entry`, `only home`, `carries no Waiting line` 0 -> 1; no changed line of `doctrine/plans.md` contains `NEXT_SESSION` |
| Pins still read the sentences | throwaway worktree at `753f7fed` | deleting the whole edited sentence from each template and "Sequencing is free; removal is not" from `doctrine/plans.md` turns exactly three nodes red: `dev/plans/_template.md::sequencing between chunks owes nothing`, `templates/core/dev/plans/_template.md::sequencing between chunks owes nothing`, `doctrine/plans.md::sequencing is free, removal is not`. Control: deleting only "Sequencing is free" leaves all 99 green |
| Fresh install | tested commit, `collaborative-team` preset | the installed `tools/board.py` (identical to the shipped twin) runs inside the scratch tree: exit 0, zero entries, advisory `none`; a line-initial form of the shipped `PLANNING.md` sentence lists itself |
| Live list, C4 | tested commit | `board.py --maintainer` lists the proposal at `awaiting-decision` and 2 `roadmap` entries (`dev/PLANNING.md:208`, `:500`), equal to the 2 rows marked; the ellipsis count is 0; the statement written line-initially would make it 3 |
| C4 narrow commit | `31d9cefe` | one file, 17 lines added, none removed; the Decision's authorization appears once, verbatim, in the commit body (`grep -cF` prints 1) |
| Claim and prose gates | tested commit | `claim_check.py` clean on all eight edited documents; `test_scope_reduction_trap.py` passes (99) at C3 and C4 |

**Day-one figures.** At C1 the advisory named both active plans, as this plan's
review predicted. It still names this plan at the tested commit, because its
body says `MAINTAINER-ONLY` in the chunk-M row and a wait declared on a marked
board row does not suppress it.

**Known omissions.**

* No standing test pins the C2–C4 prose, as *Verification* said; the counts above
  are one-shot checks, and Boundary C attacks the prose.
* The `--maintainer` row parser matches a line-initial marker even inside a
  fenced code block of `dev/PLANNING.md`. The grammar C1 fixes does not mention
  fences, so it was not widened; no such fence exists today.
* `--archive` is ignored by `--maintainer` without a message, as the plan fixed;
  the help text says so.
* The ESC-in-an-artifact-name part of node 5 is skipped inside the test on a
  filesystem that rejects the name. It ran here.
* The sweep marked 2 rows, the two the plan names. It considered and did not mark:
  the #19 row (its revisit is not yet due), the public-launch sequence (gated
  behind the third-party probe), and the authorized deferrals whose next move is
  anyone's. The code reviewer may disagree with a call; the reasons are in the C4
  commit body.
* C5's commit also changed one Scope bullet in this plan ("at the path declared
  below" now names the path), because dropping the `Proposed paths:` line left it
  pointing at nothing. It is the only edit to an operative cell since
  implementation began.
* C2 waited about ten minutes for another session's claim on
  `doctrine/plans.md` to release, and committed after it did; the hook was not
  overridden.
* The re-anchor (chunk M) and any AST re-anchor were not run; no file under
  `bootstrap/_scaffold/` changed.

## Code review -- Claude Sonnet 5.5 (fresh session, not the implementer) -- 2026-10-18

```
Reviewed commit: a2fb2d227cf8dfcf76896af8a1052cb44d630cb0
Target: the five implementation commits in run order -- C1 72254d0eeae5eef180dbde3ed01303870ecca140, C5 42fa680488c826de0135bd218921167e2b7f67ca, C2 c5c2c38fc1f4e71c839438a149a12de2967e7096, C3 753f7fedfa49fc0ed15a063d07b6a868f130f3da, C4 31d9cefeccabdf50ad2ee6d7a3cd2a6ff20bfe35 -- over the plan's base 8e5df0f0af778759bb7c80a28204ce593dd97615, and the Boundary B record a2fb2d22. Other sessions' commits inside the range were not reviewed.
Prior findings: none
```

**Bounding**: ACCEPTED. The record is `full` mode, so the field is not about a
bounded mapping; the surface I challenged was the record's one reproducible
figure, the 74 neutrality failures, and I reproduced it three ways (below).
**Verdict**: accept-with-followups -> `ready-to-archive`. Three findings, none
blocking; no implementation, test, template or fixture byte needs to change.
**Fresh full run**: not required. None of the Boundary C triggers applies:
the record is valid for the tested commit, it reports 0 skip / xfail / xpass,
I found no cross-surface dependency, I distrust no figure in it, and my review
changes no implementation, test, executable-template or fixture byte.

Distance: the same agent type as the implementer, in a fresh context. I wrote
neither the plan nor the code. That is Internal distance; this pass claims no
External stance.

### In plain terms

The work does what the Maintainer accepted, and I could not make the new list
hide a wait. The board lists only lines an author wrote, and the tests catch
every mutation I tried that would drop a declared wait. Three small things:

* **The plan's own record trips a doc check on a fresh checkout.** It cites two
  files that exist only on the main machine. Fixed in this commit.
* **The footer warning about plans that mention a gated step is noisy from day
  one.** It names both open plans, which is the exact "noisy check" sign the
  proposal said would mean the design is wrong. It is a first reading, not a
  defect; one sentence at archive homes it.
* **Five of my mutations survived the tests.** All five make the list longer,
  never shorter, so none can hide a wait. I left them.

### The Boundary B record, checked against the range

| Claim | What I did | Result |
|---|---|---|
| Tested commit is the last implementation commit | `git diff --stat 31d9cefe a2fb2d22` | holds: later bytes are the record, one mapping file and two proposals, all from other sessions; none is a file of this plan |
| Range base is the plan at `ready-to-implement` | `git log -1` on the base | holds: "Response to plan review: maintainer-attention -- ready-to-implement" |
| Interpreter 3.13.13 | ran the named path | holds |
| Commands are AGENTS.md's pair, with seed 0 | read the table | holds |
| 20 nodes now, 15 at the parent, five added | `--collect-only` in a worktree at each | holds: 20 and 15 |
| The five nodes fail at the parent | copied the new test file into a worktree at the base | holds: 5 fail (the sixth selected node is an older one that passes) |
| 74 neutrality failures, unchanged | ran the gate at the base, at the tested commit and at `a2fb2d22`; sorted the `FAIL` lines | holds: 74, 74, 74, identical lists, 22 files, none touched by the five commits |
| 0 skip, 0 xfail, 0 xpass; 3384 passed | not re-run (Boundary C is not Boundary B) | taken as recorded; consistent with everything above |
| Clean pre- and post-run state | not observable after the fact | taken as recorded |
| "This plan's own files carry no flag" | `check_cairn.py` and `claim_check.py` in a clean detached worktree at `a2fb2d22` | **false at the record's own commit**: see [CR1] |
| "Other sessions' commits ... none touches a file of this plan" | `git show --name-only` on each | **inexact**: `4f1b076f` edited `doctrine/plans.md`, in a different section from the three C2 and C3 edit (the ledger bullet near the Boundary B paragraph); C2 re-read it at edit time. The numbers are unaffected, since the tested commit contains it |

The instrument for the neutrality row was checked first: my first filter
matched nothing (the gate prints `FAIL`, not `fail`), so the empty diff proved
nothing. I fixed the filter, confirmed 74 non-empty lines, and then diffed.

### Scope fidelity

Every accepted outcome in the plan's *Scope delta* table has its evidence in the
diff, and nothing beyond it landed.

* **Files.** The union of the five commits is the plan's *Scope* list and
  nothing else. `AGENTS.md`, `templates/core/AGENTS.md`,
  `doctrine/session-routines.md`, `doctrine/proposals.md`, `bootstrap/_scaffold/`,
  `CHANGELOG.md` and `docs/tool-usage.md` are untouched by this plan's commits.
  (The two `AGENTS.md` copies do change inside the range, by other sessions.)
  The only unplanned edit is C5's one Scope bullet, which the record declares.
* **Twins.** `cmp tools/board.py templates/skills/_lib/board.py` exits 0 at the
  tested commit and at head; the twin-parity test passes.
* **Lockfile.** C1's diff to `dev/.cairn/cairn-lock.yml` is one line, the
  `tools/board.py` hash; that hash equals the file on disk; `verify_integrity`
  names the same files as before and none is the board. I checked the instrument:
  after editing both twins in step without a finalize, parity stays green and
  `verify_integrity` names the board. Only `verify_integrity` sees a stale
  record, so any later edit to the board owes its own scoped finalize.
* **Counts.** `only home`, `is not a live home`, `by number`, `assigns`,
  `board row listing the items`, `of a live plan` and `writes its own changelog
  entry` each occur once where the plan says; the shipped template carries no
  Cairn path; the added template text is identical across the two copies once
  the tracker name is swapped (I diffed it myself); no template line begins with
  the marker; C3's `doctrine/plans.md` diff has no `NEXT_SESSION` line.
* **Tracker.** `evolution_infer.py` lists it among the trackers read (0 rows,
  30-day window). A copy with two `occurred` rows, one per source, gets a
  rate-limit suggestion for `waiting-line-miss`.

### Falsification ledger

**Does `--maintainer` still judge nothing?** Yes, in the code. `_waiting` reads
header fields through `_header_fields` (stops at the first `##`), the row
grammar on `dev/PLANNING.md`, and two fixed words in plan text. Probes on
scratch trees: a marker line in a plan **body** is not listed; a fence word
inside a code block names the plan on the advisory and lists nothing; a marker
in a blockquote, in backticks, mid-sentence, or with the colon inside the bold
is not listed. One direction is not pinned by a test: see [CR3].

**Silent forms beyond the documented one.** Not listed and, with no fence word,
not named either: `**Waiting on maintainer**:` (lower case), a status written
`` `awaiting-decision` ``, `**awaiting-decision**` or `Awaiting-Decision`. The
plan documents and declines only the colon-inside-bold spelling, so these are
the same class, declined for the same reason. The weight of evidence is that
they do not occur: all 134 artifacts with a Status line write a bare lower-case
word. No finding.

**The two weaknesses the implementer flagged.**

* *The row parser matches a marker inside a fenced code block.* Confirmed, and
  so does one in an HTML comment. Acceptable as recorded. The wrong answer is an
  **extra** listed row that the Maintainer opens and sees is an example, never a
  missing one. The shipped and Cairn statements put the marker inline in
  backticks, so nothing in the tree trips it. Hardening is a dozen lines and I
  confirmed no pinned node would redden if it were added; it is not worth a new
  full run now.
* *The advisory names plans whose wait is declared on a board row.* Real, and
  the larger of the two: see [CR2].

**Output encoding.** Scratch trees with file names and values holding a newline,
a carriage return, a bidi override, a C1 control (CSI), a zero-width space, a
bell and a pipe. Every one comes out as an escape (`\x0a`, `\x0d`, `\u202e`,
`\x9b`, `\u200b`, `\x7c`); the output has no raw control or bidi character, and
every line starts with `board: `. Because the pipe is escaped too, a name cannot
fake a column. A value is cut at a carriage return before encoding, because the
header reader splits lines there; that loses text, never forges it.

**Plain board unchanged.** The parent's `board.py` and head's print identical
output on the head tree, with and without `--archive`. With a Waiting line
present the new column appears, as Revision 1 accepted. `--help` names
`--maintainer` and no longer says "header blocks only"; the subprocess pattern
matches `tools/session.py` (so it can fire) and prints nothing on
`tools/board.py`.

**A plan copied straight from a template.** Copying each template's body into a
scratch tree lists nothing (no placeholder lists as waiting), but the advisory
names the copy, because the template's own *Sequence* sentence holds both fence
words. No real plan keeps that sentence (none of the 54 plans I searched does),
so this is transient noise at most. No finding.

**The pins.** `test_scope_reduction_trap.py` passes (99). Deleting the whole
edited sentence from both templates and "Sequencing is free; removal is not"
from `doctrine/plans.md` turns exactly three nodes red, the three the plan
names. Reverting only C3's "of a live plan" in all three leaves all 99 green:
the new qualifier is unpinned, as the plan's known omission says.

**Mutations of my own** (on `tools/board.py` in a detached worktree, five-node
file; each mutant confirmed to change the output before I read its survival):

| Mutant | Result |
|---|---|
| `MAINTAINER-GATED` dropped from the fence words | caught: the fence node |
| advisory also applies to proposals | caught: the fence node |
| advisory prints only the first plan | caught: the fence node |
| "not listed" footer line removed | caught: the footer node |
| exit code 1 when anything is listed | caught: all five |
| reason column says `declared` for a decision | caught: the list node |
| row value truncated to 3 characters | caught: three nodes |
| row line number off by one | caught: three nodes |
| blockquote prefix accepted in a row | **survived** |
| `+` and numbered bullets accepted in a row | **survived** |
| a marker line in a plan **body** counts as declared | **survived** |
| status matched as a substring, not the first word | **survived** |
| the count line always prints 0 | **survived** |
| fenced code skipped in `dev/PLANNING.md` (hardening) | survives, as it should |

Both twins edited in step without a finalize: the parity test stays green and
`verify_integrity` names the board (see *Lockfile*).

**The C4 sweep.** I read every row of `dev/PLANNING.md` (the Queued rows, the
untriaged backlog, the Migrated roadmap, the re-anchor batch and the release
path) against the plan's test: a ceremony only the Maintainer runs, a question
only they answer, a go-ahead only they give. The two marked rows are right, and
I found no third. Closest calls, both left unmarked, both defensible: the
third-party probe row is blocked on an outside party's consent, and its text does
not say who recruits one; the public-launch sequence is called Maintainer-gated,
but its first step waits behind that probe. The F8, #13, #19 and
`NEXT_SESSION.md` rows are authorized deferrals whose next move is anyone's.
Marking more would also grow the list the Maintainer has to read. I would not
log either as a miss: a miss row needs a wait that was the Maintainer's.

**Does C3 read coherently beside AGENTS.md?** Yes. AGENTS.md says sequencing
may move work between chunks and that dropping an accepted outcome needs the
Maintainer. C3 narrows the first to chunks of a *live* plan and adds the
hand-off rule for an unopened one, which is a `defer`. The doctrine bullet's
last sentence sends a plan that simply fell short to "the archive batch", which
repeats the accepted Question 2 answer. A reader could take that to mean a known
shortfall can wait for archive; AGENTS.md's deviation gate says to raise it when
it arises, and the *Waiting-line check* looks for exactly that request. The two
agree if read together; I did not find that worth a doctrine edit.

### Waiting-line check

`git log -p` on this plan over `8e5df0f0..a2fb2d22` shows no fenced chunk
reached and no deviation request made. Chunk M (MAINTAINER-ONLY) is gated on
this review clearing, so its fence became the next move at this commit, not
inside the range; its wait is declared on the marked board row, which is in row
form and listed by `--maintainer` at head. No miss; nothing to record in
`dev/measurement/maintainer-view-misses.md`. The plan needs no Waiting line
for M.

### Findings

#### [CR1] low -- the Boundary B record cites two local-only files, so a fresh checkout reports two hard flags on this plan

**Plain.** The record names two measurement files that are git-ignored and
exist only on the main machine. On a clean copy of this exact commit,
`claim_check` reports two hard flags on this plan, and the record's sentence
"this plan's own files carry no flag" was true at the tested commit but false at
the commit that wrote it. A hard flag is to be resolved before commit.

**Evidence.** In a clean detached worktree at `a2fb2d22`,
`python scripts/claim_check.py dev/plans/maintainer-attention.md` reports 2 hard
flags (the two paths) and `python scripts/check_cairn.py` reports them too.
With a typed `Untracked paths:` declaration appended, the same check reports
both paths exempted and exits clean. The precedent is `059a823f` (the declaration
appended to an older review record) and the addendum in `a0810700`.

**Disposition: fixed in this commit.** The declaration is document-wide, so the
line at the end of this section satisfies it without editing the implementer's
text. The record's two inexact sentences are corrected by the table above
rather than rewritten. No action for the implementer.

#### [CR2] low -- the fence advisory names every open plan, and the proposal's other warning signs have no home after it archives

**Plain.** Today `--maintainer` ends its warning line with both open plans,
because each says `MAINTAINER-ONLY` in its last chunk and declares that wait on
a board row, which the advisory cannot see. That will repeat for any plan whose
last step is the queued re-anchor. The proposal named this exact pattern ("names
most active plans for most of their lives") as a sign the design is wrong, so it
is worth watching, and its other three signs (stale lines, pile-up, the misses)
live only in the archived proposal, with the tracker holding just the misses.

**Not a code defect.** The code does what Revision 1 accepted; the figure is
the first reading, 2 of 2, and both plans archive soon, after which the line
should read `none`. Suppressing a plan whose wait is on a board row would mean
inferring from the board, which is the judgment the design refuses.

**Disposition: accept.** In the archive-preparation commit, add one sentence to
the tracker's Purpose in `dev/measurement/maintainer-view-misses.md`: the other
three signs are read by use, with the day-one figure (2 of 2) as the baseline,
and a repeat for the same reason at the next two archives is the cue for the
redesign Revision 1 anticipates. No code, test or template changes.

#### [CR3] low -- five mutants survive, all of which list more, never less

**Plain.** The tests do not pin four loosenings of the row and status readers
(a blockquote or `+` or numbered prefix, a substring status match), the body
direction of "judges nothing" (a plan body that carries the marker is ignored),
or the footer's count. Each makes the list **longer**; none can hide a wait,
which is the failure the list exists to prevent.

**Disposition: wontfix.** Pinning them edits a frozen test file and so costs a
fresh full run, for a regression that would show up as an extra row. The
heading-stop that keeps bodies out is already pinned in `_header_fields`'s own
test, and a new body reader would have to appear in a diff. It does not reach an
adopter (tests are not shipped), block a release, or need a Decision. A note for
whoever edits the board next (the proposal `2026-10-18-claude-board-as-basis.md`
adds reads of plan text to this tool): add the body-marker assertion there,
inside its own test change.

### Comprehension

The core of the rule is plain: when a plan's next move is the Maintainer's, write
one line in the header and delete it when they answer. The preamble defines
"fenced chunk" where it is first used, and "deviation" is defined two paragraphs
above it; "defer batch" and "header block" lean on the template around them, and
a hydrogeologist would read them as Cairn terms. The sentence about why the line
is not printed in the header below is the heaviest, and it earns its place.
`doctrine/lifecycle.md`'s exception sentence reads well. In the command's own
output, the footer's "plans that mention a fence but declare no wait" is the one
place the Maintainer, not an author, meets the word "fence" without a gloss; a
rewording ("plans with a Maintainer-only step but no Waiting line") would be
test-safe and can ride along with the next edit to the board, which owes a
finalize. I do not count it as a finding.

### Coverage

**Covered.** Every Boundary B claim that can be re-observed after the fact; scope
fidelity against the *Scope delta* table; the board tool's behaviour by probe and
by mutation; encoding with hostile names and values; the row grammar, status
reading and advisory; the lockfile and twin; the two pinned sentences and the new
unpinned qualifier; the tracker; the template copies; the whole of
`dev/PLANNING.md` for the C4 sweep; the Waiting-line check.

**Not covered / low confidence.** The 3384-pass figure and the clean pre- and
post-run state are taken from the record. I did not read the five commit bodies'
Boundary A runs. Whether the third-party probe row *should* list is a judgment I
made, not one I can prove. Reviewer and implementer are the same agent type, so
there is no cross-type distance.

Untracked paths: `dev/measurement/suite-runs.jsonl`, `dev/measurement/suite-cost.md` -- both are gitignored local measurement files (`.gitignore` lines 18-19), so a fresh checkout does not carry them. Declared 2026-10-18 so the citations in the Implementation verification record above resolve on any checkout.
