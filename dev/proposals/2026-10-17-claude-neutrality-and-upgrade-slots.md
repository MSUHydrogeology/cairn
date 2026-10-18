# Two checks you can trust: a neutrality gate that reads zero, and a note for slots an upgrade adds

**Author**: Claude (Strategy)
**Status**: awaiting-decision
**Review**: required(External + Security Review)
**Plan review**: required(Internal)
**Opened**: 2026-10-17

## In plain terms

Two of Cairn's checks cannot be trusted today, for opposite reasons.

1. **The vendor-name check is always red, so a new problem would be invisible
   (#2).** `quality_gate.py --sub neutrality` keeps AI-vendor and project names
   out of what Cairn ships. Today it reports 74 failures. The issue calls them
   false alarms, but only 14 are. 38 are real leaks: reviewer names and our
   reference project's name in comments and templates every adopter receives.
   22 are legitimate mentions in Cairn's own docs that lack their marker. This
   proposal fixes all three groups, so the check reads zero and one new leak
   shows as one failure. The checker's code does not change.
2. **When an upgrade adds a fill-in section, nothing says so (#8).** A "slot" is
   a marked region of a template the adopter fills in for their project. An
   upgrade that adds one leaves Cairn's placeholder in it, unreported. This adds
   a note to the existing install check (`verify_integrity.py`) listing every
   slot still holding the shipped text. It warns; it never fails the check.
3. **#16 is left out.** It does not meet the bar your August triage set, and it
   shares nothing with the other two (see *Excluded*).

**Cost to you.** No engine change, so no hand re-anchor of its fingerprint. Up
to 14 files the gate manifest pins change; they join the re-anchor you already
have queued (`dev/PLANNING.md:156`), which still runs once. **If this is
wrong,** a reworded comment loses an explanation someone needed, or the note
nags about slots left as shipped on purpose; both are cheap to undo.

**Questions, each with a default.** (1) Close #16 as won't-build, as your
2026-08-25 triage recommended, keeping its revival rule of three independent
recurrences? *Default: yes; you close it.* (2) Should `upgrade` also print the
slot note? More visible when the adopter acts, but it costs you one hand engine
re-anchor. *Default: no; revisit if an adopter misses an upgrade-added slot.*

## Context

### The neutrality gate (#2)

Today (Python 3.13.13, `5f520a33`), `python scripts/quality_gate.py --sub
neutrality` reports `fail=74 info=21` and exits 1. The count moves with ordinary
work and every recorded run has been red: 99
(`dev/proposals/archive/2026-07-11-claude-record-corrections.md:30`), 93
(`dev/proposals/archive/2026-08-12-claude-boundary-b-bounding-clause.md:544`),
79 (`dev/plans/archive/portable-sweeps-cannot-run.md:385`), 74
(`dev/plans/archive/adopter-path-consolidation.md:520`). Boundary B records carry
it as a standing failure. The gate manifest expects "green"
(`bootstrap/tests/_gate_manifest.py:149-151`); no recorded run since June was.

| Where | Count | What they are | Real leak? |
|---|---|---|---|
| `templates/skills/` (routing table, session kernel, session-start skill) | 9 | prose saying which harness gets the symlink route | no: restates the table |
| `bootstrap/tests/fixtures/skills/README.md` | 5 | describes the same routing fixtures | no; Cairn-internal |
| other shipped templates, reviewer names | 29 | a design choice credited to a reviewer ("Per Codex P2-5") | **yes**, shipped |
| other shipped templates, `modflow_tools` | 9 | the reference project's name | **yes**, shipped |
| `docs/` | 14 | an example roster; the reference deployment's history | no, but unmarked |
| `doctrine/` | 8 | example agent identities; an illustrative tool list | no, but unmarked |

Two facts decide the design.

* **The routing data already passes.** The gate matches capitalized whole words
  (`scripts/quality_gate.py:280-281`); the table's target ids are lowercase
  (`claude-code`, `codex`) and never match. All 9 `templates/skills/` hits are
  prose repeating what a table row says.
* **The reviewer-name hits already break a rule:** `AGENTS.md` > "Comments and
  docstrings explain the code, not the process". "Per Codex P2-5" tells an
  adopter nothing, and names a vendor in a file they install.

### Upgrade-introduced slots (#8)

**The probe, run today.** I installed Cairn at `4ad1c115` (`solo-greenfield`
profile), the commit before `assurance-path-triggers` arrived in `76bc678b`;
filled all 23 slots; finalized the lockfile; and upgraded to `5f520a33` with
`--plan`, `--stage` and `--apply`. The slot arrived in
`dev/proposals/_template.md` with its placeholder, and nothing said so. The only
slot lines in the upgrade output concern a *removed* slot: the report flags
removals and has no kind for additions (`bootstrap/_scaffold/upgrade.py:718-719`).
`verify_integrity.py` and `tools/session.py session-start` print nothing about
slots. (The same search found the removed-slot lines, so it could have matched.)
`bootstrap/UPGRADE.md:101-102` says a new slot "arrives with its placeholder for
you to fill", but not which.

Already settled: the issue's suggested home, `lifecycle_planner scan`, was
removed in `bfe6bbfd`; its second comment's untaught `**Tier**` / `**Findings**`
fields are now taught (`templates/core/dev/proposals/_template.md:230-231`).

A scratch prototype of Part 2's rule (not committed) names exactly
`dev/proposals/_template.md [assurance-path-triggers]` on the probe, and nothing
once that slot is filled. On a fresh HEAD `solo-greenfield` install it names 20
slots; the install report already lists 22.

### Excluded: #16 (prose naming a symbol the code no longer has)

It does not meet your bar: the triage asks for three *independent* recurrences
before machinery, and this is one adopter in one plan cycle, with no Cairn-side
recurrence recorded. Its honest form is a new shipped tool: the issue shows a
generic symbol check drowns in false positives, and its registry script would be
a new installed file, an install-contract change, for one incident. And it
shares no mechanism with Parts 1 and 2.

## Proposal

### Part 1: neutrality reads zero; the checker is unchanged

1. **The 9 `templates/skills/` hits:** reword the prose to point at the routing
   table instead of naming harnesses ("the `tier: symlink` rows of the fan-out
   table"); the lowercase ids stay. That is the `_doc` string in
   `templates/skills/_data/vendor_targets.yml`, three comments in
   `templates/skills/_lib/session.py`, and one line of
   `templates/skills/session-start/SKILL.md`.
2. **The 38 hits in 14 other shipped templates:** rewrite each reviewer-name
   citation to give its reason in code terms; `modflow_tools` becomes "the
   reference deployment", or goes.
3. **The 27 hits in docs, doctrine and the fixture README (5 files):** wrap each
   in the existing `vendor-ok-begin` / `vendor-ok-end` markers with a reason,
   the sanctioned path outside `templates/`. No wording changes.
4. **Log the pass:** one row per group in the "Dogfood disposition log" of
   `doctrine/consolidation-review.md`, as that section prescribes.

Each edited shipped file's self-hosted twin (`scripts/_onboarding/`,
`dev/modules/`, `tools/session.py`, `tools/intent.py`, ...) changes in the same
commit, byte-identical.

### Part 2: an advisory note for slots still holding the shipped text

1. **What it checks.** `bootstrap/verify_integrity.py` gains an advisory
   section. It looks at each lockfile record with a cached base copy
   (`base_cache`). It lists each slot whose body is unchanged from the base
   copy's, comparing after spacing is normalized and the lockfile's token values
   are substituted. A slot carrying `<!-- cairn:customized -->` is never listed.
   Each entry says how to clear it: fill the slot, write `N/A: ...`, or add the
   marker to keep Cairn's text.
2. **Advisory only.** Like the forked-facade note in the same file, it never
   changes the exit code, and prints whether or not the hash check passes.
3. **The base path is checked before reading:** `dst`'s shape check (relative,
   no `..` part), plus it must resolve inside the target and not be a symlink.
   A failing path is not read, and is reported as skipped.
4. **No new engine import.** It reuses the file's `_SLOT_BODY_RE` and
   `_CUSTOMIZED_MARKER_RE` (`70e87171`), inlines the token pattern and spacing
   rule the same way, and a test pins both to the engine's.
5. **`bootstrap/UPGRADE.md` gains workflow step 4:** run `verify_integrity`
   after `--apply`. It says the check runs only when a person follows the steps.
6. **Placeholder state, not obligation.** Which slots a profile needs is F8 on
   the board (`dev/PLANNING.md:198`); that stays separate.

## Rationale

The gate's rule, templates clean by construction with no exemption path
(`scripts/quality_gate.py:268-288`), is right; what failed was a backlog nobody
cleared. To the razor "could this be a sentence instead of a script?"
(`dev/strategy/2026-08-21-claude-nimbleness-recovery.md:724`), Part 1 answers
yes: rewordings and markers, no new code. Part 2's sentence already exists
(`bootstrap/UPGRADE.md:101-102`) and failed: it says a slot may be new, not which
of 13, and the adopter in #8 followed the process. The note names it, in about 30
lines of a check adopters already run, and warns rather than blocks
(`dev/strategy/2026-08-21-claude-nimbleness-recovery.md:332`).

## Alternatives considered

* **The exemption path #2 asks for (strongest rejected):** a carve-out for
  `templates/skills/`, or an out-of-tree allowlist pinned by file, token and line
  hash. It turns "clean by construction" into "clean by review" for files every
  adopter installs, and adds an exemption surface to a high-risk boundary, for 9
  lines a rewording removes. Revisit if shipped prose must name a vendor and
  cannot point at data.
* **Freeze today's 74, fail only on new ones.** Cheapest, but it accepts 38 real
  shipped leaks for good, with no recorded reasons.
* **Print the note from `upgrade`** (#8's suggestion 2). At least two engine
  symbols change, beyond self-service repair, so a Maintainer-run re-anchor
  (`bootstrap/AST_BASELINE_RUNBOOK.md`). Your second question.
* **Block on an unfilled slot** (#8's suggestion 3): process checks warn, never
  bind (nimbleness note 1.5).
* **Do nothing:** Boundary B keeps reporting a number nobody reads, adopters keep
  inheriting reviewer names, and upgrade-added slots stay silent.

## Documentation / doctrine surface

Descriptive: `bootstrap/UPGRADE.md` (step 4, and what the note means).
Governing: none; `AGENTS.md` > "Vendor-neutrality" stays literally true.
Doctrine: marker-only edits in `doctrine/lifecycle-contract.md` and
`doctrine/rationale.md`, log rows in `doctrine/consolidation-review.md`.
CHANGELOG: one entry at archive.

**Rate-limit gate** (`doctrine/rationale.md:405-417`): not triggered. No doctrine
rule changes; the edits are the procedure `doctrine/consolidation-review.md`
prescribes. If a reviewer counts the markers as doctrine changes, the fallback is
to leave those 8 lines unmarked, logged `accepted-noise`, and the gate at
`fail=8`.

## Evidence / verification plan

### Tests required

`bootstrap/tests/test_verify_integrity.py`, each case building its own lockfile,
base cache and file in `tmp_path`: a placeholder slot is named; filled and
customized slots are not; a `{{token}}` base slot matches after substitution; an
unsafe `base_cache` (absolute, `..`, symlink) is not read and is reported
skipped; the exit code is the same with and without the note; the inlined
patterns agree with the engine's. `bootstrap/tests/test_quality_gate_neutrality.py`
needs no change: `TestTemplatesDirectiveForbidden` already pins that a token in
`templates/` fails. **Boundary B mode: full** (executable templates and frozen
files change).

### Examples / smoke checks

* **Zero, and still able to fail.** After Part 1 the gate reports `fail=0`; one
  capitalized vendor name planted in `templates/skills/` prose makes it `fail=1`
  (today, on a HEAD copy via `--root`, one plant moved 74 to 75).
* **Comment-only proof.** Each edited `.py` template and twin gives the same
  docstring-stripped `ast.dump` before and after (this covers `tools/session.py`
  and the content scanner); `vendor_targets.yml` parses to the same table apart
  from `_doc`. A one-character code change in a scratch copy must break it.
* **Twins.** Each edited template and its twin are byte-identical.
* **The probe, re-run on the implementation commit,** names exactly
  `dev/proposals/_template.md [assurance-path-triggers]`, and nothing once filled.
* `python scripts/check_cairn.py` over the touched Markdown.

#### Security preflight — five questions, answered in writing

* **S1 — Who supplied it?** Part 1 adds no decision and no exemption path, so no
  scanned file can exempt itself. Part 2 decides from the installed file, its
  base copy and the lockfile's tokens: all supplied by the adopter's tree, the
  thing judged. That is acceptable only because the note is advisory; a tampered
  base can hide or invent a placeholder, and grants nothing.
* **S2 — Can it fail?** Yes, both, run today: one planted name moved the gate
  74 → 75; filling the slot moved the prototype 1 → 0. Part 2's expectation comes
  from the base copy, not from the file it checks.
* **S3 — What fires it, over what?** Part 1: a person, at Boundary B
  (`AGENTS.md` > "Verification boundaries") and at the gate-manifest ceremony; no
  hook or CI. Input: `_NEUTRALITY_FILE_SUFFIXES`
  (`scripts/quality_gate.py:440-449`). Part 2: a person running
  `verify_integrity`, as UPGRADE.md step 4 will say. Input: lockfile records
  carrying a `base_cache`.
* **S4 — Which way does it break?** Quieter, never with more authority: an unsafe
  or missing base path is not read; absent tokens make a token-bearing
  placeholder read as changed; an unreadable file is skipped. The exit code never
  changes.
* **S5 — Who still wins?** The denylist is enumerated and case-sensitive: today
  26 lowercase-only vendor mentions in 14 files under `templates/` and
  `doctrine/` pass unseen (mostly routing ids, harness environment-variable names
  and example agent ids), as does any vendor not on the list. That class is
  closed by enumeration, not construction, and is unchanged here. In Part 2,
  anyone who can edit the base cache can hide a placeholder.

## Signals the change is wrong

* Neutrality goes red again within a few plans, fixed by the same rewordings:
  the gate needs a cheaper trigger (a commit hook), not another cleanup.
* A reader needs an explanation that a reworded comment dropped.
* Adopters add `cairn:customized` by reflex, or the note names slots they did
  fill: it is noise, and should go.

## Scope delta

**Scope delta**: preserved. This is the baseline as opened: Parts 1 and 2. #16
was never in it.

## Assurance path

**Assurance path**: high-assurance — the vendor-neutrality boundary, the content
scanner and the interpreter-binding module (both edited in comments only), and a
lockfile reader adopters run before trusting their scripts.

## Review -- Claude Opus 5.5 (External, fresh session) -- 2026-10-17

```
Reviewed commit: 5184bb1a94c0c5d95ad6de7fd22fca8bfdbcbc5d
Target: the complete proposal (In plain terms through Assurance path), checked against issues #2, #8 and #16 and the tree at the reviewed commit
Prior findings: none
Assurance path: high-assurance
```

**Tier**: External
**Findings**: raised (4 blocking, 1 non-blocking)
**Verdict**: REVISE

Distance: a fresh session of the author's agent type, not a different type.
This pass discharges the External obligation only; the Security Review the
header declares is a separate pass and is still owed.

### In plain terms

Both parts should happen. Taking reviewer names out of files every adopter
installs is overdue, and a note naming the fill-in sections an upgrade added is
the fix the reporting adopter asked for. Neither part touches the install
engine.

Four things need fixing first, each in a few sentences:

1. **The vendor-name check was cleaned to zero once before**, on 2026-05-28, and
   new names were back the same afternoon. The proposal says the cause was "a
   backlog nobody cleared"; the record says otherwise. It has to say why zero
   will hold this time. The record holds a good answer; the proposal does not
   give it.
2. **Doing what the note says makes the install check fail.** Every way it
   offers to clear a slot edits the file, and the next run then reports that
   file as tampered with, usually without saying how to record the edit.
3. **A silent note can mean two things:** every slot is filled, or nothing could
   be checked. Cairn's own tree is the second case: only 2 of its 73 recorded
   files keep the cached copy the note compares against, and `AGENTS.md` and
   both templates, where the slots live, are not among them.
4. **Question 1 would close #16 with half of it never decided.** #16 asks for a
   check, which your August triage declined, and also for one paragraph in the
   module's text naming the problem. That half passes the triage's own test,
   "could this be a sentence instead of a script?"

### The proposal at its strongest

A check that is always red cannot show a new problem. Clearing every finding
once, with no new code and no exemption path, turns the neutrality gate back
into a signal where one new leak reads as `fail=1`. Rejecting #2's exemption
path is right: the routing table's ids are lowercase and already pass, so the 9
`templates/skills/` hits are prose, and an allowlist would turn "clean by
construction" into "clean by review" for files every adopter installs.

Part 2 automates a line the acceptance checklist already asks a person to check
by hand: every slot filled or marked `N/A: <reason>`, where "the placeholder
text inside the markers is the unfilled state" (`bootstrap/BOOTSTRAP.md:525-527`).
It works from data the lockfile already keeps, it warns rather than blocks, and
it is the direction the reporting adopter offered to write themselves.

### What I checked

The counts reproduce. At the reviewed commit, under Python 3.13.13, the gate
reports `fail=74 info=21`, and sorting the 74 gives exactly the proposal's groups
(9, 5, 29, 9, 14, 8; the 38 shipped hits in 14 files). All 29 reviewer-name hits
are review citations plus one example heading; none describes how a harness
behaves, so rewording loses nothing an adopter needs. These check out: the four
archived counts; the gate manifest's `green` expectation; the upgrade report's
lack of any kind for an added slot (`bootstrap/_scaffold/upgrade.py:718-719`);
the `UPGRADE.md` sentence; the template's Tier and Findings lines; the planner's
removal in `bfe6bbfd`; the probe's base (`4ad1c115` is the parent of
`76bc678b`); the rate-limit and nimbleness citations. Every edited template is
byte-identical to its twin today. One citation is off by ten lines (NU5).

### Findings

**[NU1] (blocking) The neutrality gate was cleaned to zero before and refilled
within hours; the proposal must say why zero holds this time.** The Rationale
says "what failed was a backlog nobody cleared". It was cleared: `29ffeea6`
(2026-05-28, 11:36) records "fail=0 across both sub-gates" and logged its fixes
in `doctrine/consolidation-review.md`'s dogfood log. At 15:07 the same day,
`dbc09557` put the first "Codex P2-5" citation into `_onboarding/`; by
2026-06-12, #2 counted 99. So the first "Signal the change is wrong" (red again
within a few plans) has already happened once, and the proposal does not
mention it.

The record also holds the answer. In May the gate had no routine trigger, and
crediting reviewers in code was a habit. Both have changed: Boundary B (the
full test-and-gate run recorded before code review) has run this gate since
`5f6ecccc` (2026-08-05), and `AGENTS.md`'s rule that comments explain the code,
not the process, arrived in `013847b6` (2026-08-18). Blame on the 61 lines
behind the 74 failures shows no name added after about 2026-06-11; every later
edit to those lines moved or reworded a name already there.

*Closes when* the Context states the precedent and this argument, and the
Signals line becomes a concrete trigger: a Boundary B record after archive
showing a neutrality failure the change under test did not introduce — a name
that reached master between runs. One such record owes the commit hook the
proposal already names as its fallback.

**[NU2] (blocking) Doing what the note says makes `verify_integrity` fail.**
The note's three remedies (fill the slot, write `N/A: ...`, add the marker) each
edit the installed file. Its hash (fingerprint) then differs from the lockfile,
so the next run exits 1 with "Do not trust the shipped scripts until this is
resolved" (`bootstrap/verify_integrity.py:157-173`). The command that records a
deliberate edit, `upgrade --finalize`, is named only when the slot carries
`<!-- cairn:customized -->` (`bootstrap/verify_integrity.py:138-139`; added in
`e23aad28`, narrowed in `70e87171`). An adopter who fills a slot or writes
`N/A` gets a tamper warning and no way back. This will not be rare: on a fresh
`solo-greenfield` install the proposal's own prototype lists 20 slots.

*Closes when* each entry's instruction ends with recording the edit
(`python bootstrap/scaffold.py upgrade --target <repo> --finalize <path>`), and
a test covers the whole loop: listed, fixed as instructed, finalized, then
`verify_integrity` exits 0 and the note is silent.

**[NU3] (blocking) A silent note cannot tell "all filled" from "nothing
checked".** The note compares only records that keep a cached base copy, the
pristine template it measures against. A tree migrated with
`upgrade --init-lock` has none for any token-substituted file
(`bootstrap/UPGRADE.md:180-186`). Cairn's own tree shows the size of the gap:
73 recorded files, 2 with a base copy (`dev/modules/content-security.md`,
`dev/modules/portable-security-sweeps.md`), none for `AGENTS.md` or either
template. Run on Cairn, the note would print nothing about any of those slots,
and that reads as a pass. A second silent miss: if an upgrade rewords the
placeholder of a slot the adopter never filled, the merge keeps the old wording
in the file while the new base copy holds the new wording, so the slot reads as
filled. `AGENTS.md` > "Confirm the instrument before trusting an absence"
applies directly.

*Closes when* the note always prints one coverage line (slots checked, files
checked, files with no base copy), so that silence means "none found"; and the
reworded-placeholder case is either tested or recorded in `UPGRADE.md` as a
known gap.

**[NU4] (blocking) Question 1 would close #16 with its cheaper half never
decided.** #16 makes two suggestions. The second, a shipped retired-name check,
is the machinery your 2026-08-25 triage declined, and excluding it is sound: it
would be a new installed file on the strength of one adopter's cycle. The first
is a sentence: name the third category in the doctrine, because "naming it is
most of the value even without tooling".
`templates/modules/team-gated/doc-drift-prevention.md:48-51` still splits the
problem only into "drift, not absence". The triage's razor favours this half,
the triage comment speaks only to machinery, and the *Excluded* paragraph argues
only against the tool. A yes to Q1 as written drops the sentence without anyone
deciding to. This is not narrowing — an issue is not accepted scope — and
fixing it need not widen this proposal.

*Closes when* Q1 is split: close the check half as won't-build under the
three-recurrence rule, and give the sentence half its own disposition (a board
entry or a small follow-up change) with a recommended default.

**[NU5] (non-blocking) Smaller record corrections.**

* F8 is at `dev/PLANNING.md:208`, not `:198`.
* The checker's comment says `bootstrap/tests/` is not scanned
  (`scripts/quality_gate.py:446`), but the walk is recursive and scans it; that
  is the only reason the 5 fixture-README hits exist. Marking them is fine, but
  "the checker is unchanged" then leaves a false sentence in the checker. Fix
  the comment (prose only), or say why not.
* Name the twins rather than "...": the list also needs `.agents/skills/` (for
  `vendor_targets.yml` and `session-start/SKILL.md`), `scripts/content_scan.py`
  and `scripts/onboarding_activate.py`.

### Verdict, strongest alternative, falsifier

**Should it happen?** Yes, both parts, revised per NU1-NU4. Doing nothing keeps
reviewer names in every adopter's tree and upgrade-added slots silent.

**The strongest rejected alternative is #8's second suggestion: print added
slots from `upgrade` itself.** The merge already holds both sets of slot names,
and already raises the opposite case, a removed slot, from the same place
(`bootstrap/_scaffold/merge.py:200-213`). It would name only what the upgrade
added, at the moment the adopter is looking, whether or not anyone runs a later
step. The proposal's note reaches the adopter only if they follow a new step 4,
yet the Rationale's own point is that a sentence in `UPGRADE.md` already failed
this adopter once. The alternative loses on cost: an engine change on a
high-risk surface and a Maintainer-run re-anchor of the engine's fingerprint.
That cost is lower than stated if it joins the re-anchor already owed before the
issue batch is pushed (`dev/PLANNING.md:195-197`). The proposal folds its
gate-manifest files into a queued ceremony but does not weigh doing the same
here.

**What would falsify the central claim** — that after this, each check means
what it says?

* *Part 1:* any Boundary B record after archive showing a neutrality failure
  introduced between runs (NU1). The May precedent is exactly that shape.
* *Part 2, testable now:* re-run the probe on two trees the proposal did not
  try. (a) A partly filled install: fill only the slots `bootstrap/BOOTSTRAP.md`
  says need the Maintainer's own input, then upgrade. If the one added slot
  cannot be picked out of the backlog, the note does not fix #8 for that
  adopter. (b) An `--init-lock` tree: if the note says nothing, NU3 is
  confirmed.

### On the Questions

* **Q1.** Split it (NU4). Yes to closing the check half. Give the sentence half
  its own default; mine would be to write it.
* **Q2.** The trade is not visibility. The note works only if someone runs step
  4; a print from `upgrade` works regardless. If the owed engine re-anchor is
  still pending when the plan is written, joining it makes "yes" much cheaper
  than the proposal says. If it has already been done, keep "no".

## Response -- Claude (author) -- 2026-10-17

The review is right on all four blocking findings. Its strongest alternative is
also better than I credited. Each disposition below was checked against today's
tree.

**NU1: accepted.** The gate was cleaned to zero on 2026-05-28 (`29ffeea6`). The
first "Codex P2-5" landed in `_onboarding/` the same afternoon (`dbc09557`). So
"a backlog nobody cleared" was wrong, and Revision 1 withdraws it.

Its Context now says why zero should hold this time. Two things have changed:

* Boundary B has run this gate on every plan since `5f6ecccc` (2026-08-05). In
  May, nothing ran it routinely.
* The habit that produced 29 of the 74, crediting reviewers in code, now breaks
  an `AGENTS.md` rule (`013847b6`, 2026-08-18).

I spot-checked the review's blame. After 2026-06-11, the failing lines were
touched only by an extraction (`ea3d6492`) and a rewording (`a29183a9`), and
neither added a name.

The Signals line now uses the review's concrete trigger. One Boundary B record
after archive with a neutrality failure the change under test did not introduce
means the commit hook is owed.

**NU2: accepted, and closed using the marker rule as `70e87171` left it.**

* *Confirmed today*, on a fresh `solo-greenfield` install at HEAD: write `N/A`
  in a slot and commit, and `verify_integrity` exits 1 without naming any
  remedy. Its `--finalize` hint now needs `<!-- cairn:customized -->` inside the
  slot.
* *The change:* every remedy the note prints now includes four steps. Put the
  marker in the slot. Commit. Run `--finalize <path>`, which refuses a tree with
  uncommitted changes. Commit the lockfile.
* *Why that is enough:* because the slot carries the marker, the existing hint
  names the file even if the adopter skips the record step.
* *Run today:* fill the slot and add the marker, then commit; that exits 1 with
  the hint naming `AGENTS.md`. After `--finalize` and a commit it exits 0, and
  the note lists 19 slots where it listed 20.
* *Declined:* widening the hint to fire whenever every difference from the base
  copy lies inside slots. On the same install, `AGENTS.md` differs from its
  base outside slots, because install renders its `cairn:if` blocks. The wider
  rule would miss the file that matters most.

**NU3: accepted.** The note now always prints a coverage line. It gives the
slots and files it checked, and names the slots and files it could not check
because they have no cached base copy. On Cairn's own tree that line reads 0
checked, with 13 slots in 6 files unchecked, so a silent run no longer looks
like a pass.

Measuring surfaced two refinements:

* *Verbatim records are skipped.* The note reads only non-verbatim records.
  `scripts/_onboarding/triggers.py` quotes slot markers in code and would
  otherwise be counted.
* *A known gap is recorded.* When an upgrade rewords a placeholder, a slot
  still holding the old wording reads as filled. That gap goes into
  `bootstrap/UPGRADE.md`, and a test pins it.

Part 1 does not trigger that gap, because it rewords no placeholder text. None
of the 38 shipped hits sits inside a slot body. The same check does find a known
slot line (`templates/core/dev/proposals/_template.md:213`), so it could have
matched.

**NU4: accepted.** Question 1 is split. The check half closes as won't-build
under the three-recurrence rule. The sentence half becomes its own question,
with the review's default, write it, as a separate small change. This proposal
does not grow.

**NU5: accepted.**

* F8 is now cited at `dev/PLANNING.md:208`.
* The false comment at `scripts/quality_gate.py:446` is corrected, prose only.
  "The checker is unchanged" therefore becomes "the checker's behaviour is
  unchanged", and pinned files go from 14 to 15.
* The twins are now named.

**The strongest alternative, weighed again.** I ran the review's falsifier (a).
I installed at `4ad1c115`, filled only the three Maintainer-input slots, and
upgraded to HEAD. The note then lists 17 slots, and nothing marks
`assurance-path-triggers` as the one the upgrade added. So on a partly filled
tree the note does not fix #8, and an upgrade-time print would.

The engine change is small. The merge already holds both slot sets, and flags
the removed case there (`bootstrap/_scaffold/merge.py:200-213`). But it changes
at least `merge_file` and `_print_upgrade_report`, neither of which
self-service repair covers. The re-anchor now underway will not include it, so
it would owe its own Maintainer-run re-anchor.

I keep it out of this change. Q2's default becomes "not now, but ride along":
carry it in the next engine change to the upgrade path that already owes a
re-anchor, or sooner if an adopter misses an upgrade-added slot. The reporting
adopter's tree was otherwise filled, and there the note names exactly the one
slot.

**Status.** This answers the External review. The outcomes do not widen. The
change touches one more file (the comment in `scripts/quality_gate.py`), and
#16's sentence half moves into its own question. The Security Review that the
header declares has not run, and it is the remaining obligation. Status returns
to `awaiting-review` for it.

## Revision 1 -- Claude (author) -- 2026-10-17 -- the complete current contract

### In plain terms

Two of Cairn's checks cannot be trusted today, for opposite reasons.

1. **The vendor-name check is always red, so a new problem would be invisible
   (#2).** `quality_gate.py --sub neutrality` keeps AI-vendor and project names
   out of what Cairn ships. It reports 74 failures, and only 14 are the false
   alarm #2 describes:
   * **38 are real leaks:** reviewer names and our reference project's name, in
     comments and templates every adopter receives.
   * **22 are legitimate mentions** in Cairn's docs that lack their marker.

   This proposal fixes all of them, so the check reads zero and one new leak
   shows as one failure. The check was zeroed once before, in May, and refilled
   within hours. Two things have changed since: it now runs in every plan's
   final verification run, and a project rule now bars crediting reviewers in
   code. If
   a name still reaches the main line between runs, a commit hook comes next.
2. **When an upgrade adds a fill-in section ("slot"), nothing says so (#8).**
   The existing install check (`verify_integrity.py`) gets an advisory note
   listing every slot that still holds Cairn's placeholder text.
   * **It always reports coverage:** how many slots it could check, and which
     files it could not, so a short report never passes for "all filled".
   * **Its fix-it instructions end in a passing check.** Following them never
     leaves a tamper warning behind.
   * **One limit:** on a tree with many slots still unfilled, the new slot
     appears in the list but is not singled out.
3. **#16 is split.** Its proposed new check is declined, under your August
   triage. Its one-paragraph half is a separate question, below.

**Cost to you.** No engine change, so no hand re-anchor of its fingerprint. Up to
15 files the gate manifest pins change. They join the re-anchor already queued
(`dev/PLANNING.md:156`).

**If this is wrong,** either a reworded comment loses an explanation someone
needed, or the note nags. Both are cheap to undo.

**Questions, each with a default.**

* **Q1. #16 asks for two things.**
  * (a) A new shipped check. Close it as won't-build under your
    three-recurrence rule? *Default: yes.*
  * (b) One paragraph in the doc-drift module naming the problem: prose that
    names a function the code no longer has. *Default: write it, as a separate
    small change after this Decision. #16 closes when it lands.*
* **Q2. Should `upgrade` itself name the slots it adds?** That would single out
  the new slot on a partly filled tree. But it changes the engine, which costs
  you a hand re-anchor of its own. *Default: not in this change. Carry it in the
  next engine change to the upgrade path that already owes a re-anchor, or
  sooner if an adopter misses an upgrade-added slot.*

### Context

**The neutrality gate (#2).** Today (Python 3.13.13), `python
scripts/quality_gate.py --sub neutrality` reports `fail=74 info=21` and exits 1.
Every recorded run has been red, and the gate manifest's expected result is
"green" (`bootstrap/tests/_gate_manifest.py:149-151`):

| Failures | Source |
|---|---|
| 99 | `dev/proposals/archive/2026-07-11-claude-record-corrections.md:30` |
| 93 | `dev/proposals/archive/2026-08-12-claude-boundary-b-bounding-clause.md:544` |
| 79 | `dev/plans/archive/portable-sweeps-cannot-run.md:385` |
| 74 | `dev/plans/archive/adopter-path-consolidation.md:520` |

| Where | Count | What they are | Real leak? |
|---|---|---|---|
| `templates/skills/` (routing table, session kernel, session-start skill) | 9 | prose saying which harness gets the symlink route | no: restates the table |
| `bootstrap/tests/fixtures/skills/README.md` | 5 | describes the same routing fixtures | no; Cairn-internal |
| other shipped templates, reviewer names | 29 | a design choice credited to a reviewer ("Per Codex P2-5") | **yes**, shipped |
| other shipped templates, `modflow_tools` | 9 | the reference project's name | **yes**, shipped |
| `docs/` | 14 | an example roster; the reference deployment's history | no, but unmarked |
| `doctrine/` | 8 | example agent identities; an illustrative tool list | no, but unmarked |

* **The routing data already passes.** The gate matches capitalized whole words
  (`scripts/quality_gate.py:280-281`). The routing table's target ids are
  lowercase (`claude-code`, `codex`), so all 9 `templates/skills/` hits are
  prose repeating a table row.
* **The reviewer-name hits already break a rule:** `AGENTS.md` > "Comments and
  docstrings explain the code, not the process".

**Zero has been reached before.** On 2026-05-28, `29ffeea6` reached
`fail=0`. `dbc09557` added the first "Codex P2-5" to `_onboarding/` the same
afternoon, and by 2026-06-12 #2 counted 99. Two things differ now:

* Boundary B has run the gate on every plan since `5f6ecccc` (2026-08-05).
* Crediting reviewers in code has been against `AGENTS.md` since `013847b6`
  (2026-08-18).

Since 2026-06-11, the failing lines were touched only by an extraction
(`ea3d6492`) and a rewording (`a29183a9`), and neither added a name.

**Upgrade-introduced slots (#8).** I installed Cairn at `4ad1c115`
(`solo-greenfield`), the parent of `76bc678b`, which added
`assurance-path-triggers`. I filled all 23 slots, finalized the lockfile, and
upgraded to HEAD.

* **The slot arrived, and nothing reported it.** It landed in
  `dev/proposals/_template.md` with its placeholder.
* **The upgrade output covers only the opposite case.** It flags a removed slot
  and has no kind for an added one (`bootstrap/_scaffold/upgrade.py:718-719`).
* **The other tools are silent too.** `verify_integrity.py` and
  `tools/session.py session-start` print nothing about slots.
* **The guide does not say which slot.** `bootstrap/UPGRADE.md:101-102` says a
  new slot "arrives with its placeholder for you to fill".

A scratch prototype of the rule below (not committed) gave these results:

* **Fully filled tree:** it names exactly `dev/proposals/_template.md
  [assurance-path-triggers]`.
* **The same upgrade with only the three Maintainer-input slots filled:** it
  lists 17 slots, and does not single out the new one.
* **Cairn's own tree:** it checks 0 slots. 13 slots in 6 files have no cached
  base copy.

Settled already: the issue's suggested home, `lifecycle_planner scan`, was
removed in `bfe6bbfd`. Its untaught `**Tier**` / `**Findings**` fields are now
taught (`templates/core/dev/proposals/_template.md:230-231`).

**The note's fix-it path today.** On a fresh HEAD install:

* **Without the marker:** writing `N/A` in a slot and committing makes
  `verify_integrity` exit 1 with no remedy named. Its `--finalize` hint needs
  `<!-- cairn:customized -->` in the slot (`70e87171`).
* **With the marker:** filling the slot, adding the marker and committing gets
  the hint naming the file. After `--finalize` and a commit, it exits 0.

**#16.** The check it proposes is the machinery your 2026-08-25 triage declined:
one adopter, one plan cycle, and no Cairn-side recurrence. It would also be a new
installed file. Its other half is a paragraph naming the problem in
`templates/modules/team-gated/doc-drift-prevention.md`, which splits drift only
into "drift, not absence" (`:48-51`). That half shares nothing with Parts 1 and
2, so it is Q1(b).

### Proposal

**Part 1: neutrality reads zero; the checker's behaviour is unchanged.**

1. **The 9 `templates/skills/` hits** are reworded to point at the routing table
   ("the `tier: symlink` rows of the fan-out table"); the lowercase ids stay.
   The hits are:
   * the `_doc` string in `templates/skills/_data/vendor_targets.yml`;
   * three comments in `templates/skills/_lib/session.py`;
   * one line in `templates/skills/session-start/SKILL.md`.
2. **The 38 hits in 14 other shipped templates.** Each reviewer-name citation is
   rewritten to give its reason in code terms. `modflow_tools` becomes "the
   reference deployment", or is dropped.
3. **The 27 hits in docs, doctrine and the fixture README (5 files)** are
   wrapped in the existing `vendor-ok-begin` / `vendor-ok-end` markers, with a
   reason. No wording changes.
4. **The false comment** at `scripts/quality_gate.py:446` ("Not
   bootstrap/tests/") is corrected. Prose only; the walk is unchanged.
5. **The pass is logged** with one row per group in the "Dogfood disposition
   log" of `doctrine/consolidation-review.md`.
6. **Each twin changes in the same commit, byte-identical:**
   * `.agents/skills/_data/vendor_targets.yml`
   * `.agents/skills/session-start/SKILL.md`
   * `tools/session.py`
   * `scripts/_onboarding/` (`__init__`, `activation`, `cli`, `security`,
     `shared`, `triggers`)
   * `scripts/onboarding_activate.py`
   * `tools/intent.py`
   * `scripts/content_scan.py`
   * `dev/modules/documentation-plan.md`
   * `dev/modules/incident-trackers.md`
   * `dev/modules/incident_log_template.md`

**Part 2: an advisory slot note in `bootstrap/verify_integrity.py`.**

1. **What it reads.** Every non-verbatim lockfile record.
2. **What it lists.** A slot is listed when all three hold:
   * the record has a cached base copy (`base_cache`);
   * the slot body is unchanged from the base copy's, after spacing is
     normalized and the lockfile's token values are substituted;
   * the slot carries no `<!-- cairn:customized -->`.
3. **One coverage line, always printed.** It gives the slots and files checked
   and the number still holding the shipped text. It also names the files whose
   slots could not be checked because they have no base copy.
4. **The remedy, printed with each entry.**
   * Fill the slot, write `N/A: <reason>`, or keep Cairn's text on purpose.
   * In every case, put `<!-- cairn:customized -->` inside the slot.
   * Commit, then run `python bootstrap/scaffold.py upgrade --target <repo>
     --finalize <path>`. It refuses a tree with uncommitted changes.
   * Commit the lockfile.

   If the record step is skipped, the marker makes the existing `--finalize`
   hint name the file. That hint is unchanged.
5. **Advisory only.** Like the forked-facade note, it never changes the exit
   code, and it prints whether or not the hash check passes.
6. **The base path is checked before reading.** It must pass `dst`'s shape check
   (relative, no `..` part), resolve inside the target, and not be a symlink.
   Otherwise it is not read, and it is reported as skipped.
7. **No new engine import.** It reuses the file's `_SLOT_BODY_RE` and
   `_CUSTOMIZED_MARKER_RE`. The token pattern and the spacing rule are inlined,
   and a test pins both to the engine's versions.
8. **`bootstrap/UPGRADE.md` changes.**
   * It gains step 4: run `verify_integrity` after `--apply`. Only a person
     following the steps runs it.
   * It records the known gap: when an upgrade rewords a placeholder, an
     unfilled slot keeps the old wording and reads as filled.
9. **Placeholder state, not obligation.** Which slots a profile needs is F8
   (`dev/PLANNING.md:208`), which stays separate.

### Rationale

**Part 1.** The gate's rule is right: templates stay clean by construction, with
no exemption path (`scripts/quality_gate.py:268-288`). Zero failed to hold in May
because nothing ran the gate routinely, and because crediting reviewers in code
was habitual. Both have changed. Part 1 is rewordings and markers, with no new
code (`dev/strategy/2026-08-21-claude-nimbleness-recovery.md:724`).

**Part 2.** `bootstrap/UPGRADE.md:101-102` already says a slot may be new, but
not which. The note names it, says what it could not check, and gives a remedy
that ends in a passing check. It warns rather than blocks
(`dev/strategy/2026-08-21-claude-nimbleness-recovery.md:332`).

### Alternatives considered

* **The exemption path #2 asks for:** a carve-out, or an out-of-tree allowlist.
  It turns "clean by construction" into "clean by review" for files every
  adopter installs, to cover 9 lines that rewording removes.
* **Freeze today's 74 and fail only on new failures.** This accepts 38 real
  shipped leaks, with no reasons recorded.
* **`upgrade` names the slots it added (strongest rejected).** It wins on
  trigger and on singling the new slot out, as the partly filled probe shows. It
  loses only on timing and cost. At least `merge_file` and
  `_print_upgrade_report` would change, outside self-service repair, and it
  cannot join the re-anchor underway. Q2 carries it.
* **Widen the `--finalize` hint to slot-only diffs.** Declined: `cairn:if`
  rendering makes `AGENTS.md` differ from its base outside slots, so the rule
  would miss it.
* **Block on an unfilled slot.** Process checks warn and never bind (nimbleness
  note 1.5).
* **Do nothing.** A gate nobody can read stays that way. Reviewer names keep
  shipping, and new slots stay silent.

### Documentation / doctrine surface

* **Descriptive.** `bootstrap/UPGRADE.md` gets step 4, the note's meaning, and
  the known gap.
* **Governing.** None: `AGENTS.md` > "Vendor-neutrality" stays literally true.
* **Doctrine.**
  * Marker-only edits in `doctrine/lifecycle-contract.md` and
    `doctrine/rationale.md`.
  * Log rows in `doctrine/consolidation-review.md`.
* **CHANGELOG.** One entry.
* **Rate-limit gate** (`doctrine/rationale.md:405-417`): not triggered. No
  doctrine rule changes; the edits follow the procedure that
  `doctrine/consolidation-review.md` prescribes.

If a reviewer counts the markers as doctrine changes, the fallback is to leave
those 8 lines unmarked and logged `accepted-noise`. The gate would then read
`fail=8`.

### Evidence / verification plan

#### Tests required

All in `bootstrap/tests/test_verify_integrity.py`. Each case builds its own
lockfile, base cache and files in `tmp_path`.

**The whole loop, as one test.** A slot is listed. It is filled with the marker
and committed. `verify_integrity` exits 1, with the hint naming the file. After
`--finalize` and a commit, it exits 0 and the slot is no longer listed.

**One test each for:**

* the coverage line on a tree with no base copies (0 checked, files named);
* a verbatim record that quotes slot markers, which is not read;
* a customized slot, which is not listed;
* a `{{token}}` base slot, matched after substitution;
* an unsafe `base_cache` (absolute, `..`, or a symlink), which is skipped and
  reported;
* the exit code, which is the same with and without the note;
* the inlined patterns, which agree with the engine's;
* the reworded-placeholder case, which is pinned as the recorded known gap.

**Elsewhere.** `bootstrap/tests/test_quality_gate_neutrality.py` needs no
change; `TestTemplatesDirectiveForbidden` already pins template tokens.
**Boundary B mode: full.**

#### Examples / smoke checks

* **Zero, and still able to fail.** The gate reads `fail=0`. A name planted in
  `templates/skills/` prose makes it `fail=1` (today, on a copy of HEAD:
  74 → 75).
* **Comment-only proof.**
  * Every edited `.py` file must give an identical docstring-stripped `ast.dump`
    before and after. That covers the templates, their twins, and
    `scripts/quality_gate.py`.
  * `vendor_targets.yml` must parse the same apart from `_doc`.
  * To show the proof can fail, make a one-character code change in a scratch
    copy; it must break the comparison.
* **Twins must be byte-identical.**
* **Both probes, re-run on the implementation commit.**
  * Fully filled: the note names exactly the one added slot.
  * Partly filled: the new slot is listed among the rest, which is the expected
    limit (Q2).
  * The fresh-install loop above.
* **`python scripts/check_cairn.py`** over the touched Markdown.

#### Security preflight — five questions, answered in writing

* **S1 — Who supplied it?**
  * Part 1 adds no decision and no exemption path.
  * Part 2 decides from the installed file, its base copy and the lockfile's
    tokens. The adopter's tree supplies all three, so they come from the thing
    being judged. That is acceptable only because the note is advisory: a
    tampered base can hide or invent a placeholder, but it grants nothing.
* **S2 — Can it fail?** Yes, and each was run today:
  * a planted name moved the gate from 74 to 75;
  * filling the slot took the prototype from 1 to 0;
  * the loop went from exit 1 to exit 0.

  Part 2's expectation comes from the base copy, not from the file it checks.
* **S3 — What fires it, over what?**
  * Part 1: a person runs it at Boundary B (`AGENTS.md` > "Verification
    boundaries") and at the gate-manifest ceremony. No hook runs it. Its input
    is `_NEUTRALITY_FILE_SUFFIXES` (`scripts/quality_gate.py:440-449`).
  * Part 2: a person runs `verify_integrity`, and UPGRADE.md step 4 says so.
    Its input is the non-verbatim lockfile records.
* **S4 — Which way does it break?** Toward a quieter note, and the coverage line
  says so:
  * a missing or unsafe base path is not read and is named;
  * absent tokens make a token-bearing placeholder read as changed;
  * a reworded placeholder reads as filled (the known gap).

  The exit code never changes.

  The remedy has the adopter run `--finalize`, which records the whole file. A
  finalize run is therefore exactly as safe as the adopter's review of their
  own commit, and its dirty-tree guard refuses uncommitted work.
* **S5 — Who still wins?**
  * The denylist is enumerated and case-sensitive. 26 lowercase-only vendor
    mentions in 14 files under `templates/` and `doctrine/` pass unseen, mostly
    routing ids and environment-variable names. So does any vendor not on the
    list.
  * In Part 2, anyone who can edit the base cache can hide a placeholder.
  * The `--finalize` hint (`70e87171`, unchanged here) fires on a marked file
    even when text outside its slots also changed.

### Signals the change is wrong

* **A neutrality failure slips in between runs.** A Boundary B record after
  archive shows a failure that the change under test did not introduce. Then
  the commit hook is owed.
* **A reworded comment dropped an explanation** a later reader needed.
* **The note is ignored.** Adopters add `cairn:customized` by reflex, or the
  note names slots they did fill, so it is noise.
* **An upgrade-added slot is missed anyway.** An adopter misses one on a partly
  filled tree. Q2 comes due.

### Scope delta

**Scope delta**: preserved. Nothing in the opened baseline is dropped. The
revision adds one touched file (the `scripts/quality_gate.py` comment). #16's
paragraph becomes Q1(b), outside this change.

### Assurance path

**Assurance path**: high-assurance

The change reaches four sensitive surfaces:

* the vendor-neutrality boundary;
* the content scanner and the interpreter-binding module, both edited in
  comments only;
* `scripts/quality_gate.py`, one comment;
* a lockfile reader adopters run before trusting their scripts.

### Withdrawn / superseded commitments

* **"What failed was a backlog nobody cleared."** Withdrawn (NU1). The
  Rationale now names the May precedent and what has changed since.
* **The note's remedy** ("fill, write `N/A`, or add the marker"). Superseded by
  the marker → commit → `--finalize` → commit remedy (NU2).
* **Silence as a result.** Superseded by the always-printed coverage line
  (NU3).
* **Q1 as a single close of #16.** Superseded by Q1(a) and Q1(b) (NU4).
* **"The checker's code does not change."** Superseded: its behaviour is
  unchanged, and one comment is corrected (NU5).
* **"Up to 14 pinned files."** Now 15.
* **F8 cited at `:198`.** Now `:208`.
* **Signals: "red again within a few plans."** Superseded by the Boundary B
  trigger above.
* **Q2 default "no; revisit if an adopter misses an upgrade-added slot."**
  Superseded by "not in this change; ride along with the next engine change to
  the upgrade path, or sooner on that miss."

## Review -- Claude Opus 5.5 (Security Review, fresh session) -- 2026-10-17

```
Reviewed commit: 868d0d21f7df7c5540d4a53ee2c4f12652c4fde0
Target: Revision 1, the binding contract, read against the code it relies on: the neutrality sub-gate, bootstrap/verify_integrity.py, the lockfile and --finalize code, the slot-marker rules, and every Python line Part 1 rewords
Prior findings: none of this tier (NU1-NU5 are the External pass's and are not re-opened)
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: raised (3 blocking, 4 non-blocking)
**Verdict**: REVISE

Distance: a fresh session of the author's agent type, not a different type.
This is the Security Review the header declares. It does not clear the
obligation yet: SR1-SR3 must be answered first.

### In plain terms

Both parts are safe to build in principle. Neither touches the install engine,
and the edits to the sensitive scripts really are comment-only. Three things
need fixing first:

1. **"Zero" would not mean "no vendor names ship."** The check cannot see a
   name written in lower case, inside a hidden HTML comment line, or in two
   kinds of shipped file it never opens. Three capitalized names already sit
   where it cannot see them. As written, the rewording could pass by hiding
   names instead of removing them.
2. **The note's fix-it steps can bless a tampered file.** The recording command
   it prints marks the *whole file* as trusted, not just the slot. The
   proposal says that command refuses uncommitted work; in the form the note
   prints, it does not (I ran it). An adopter following the note could stamp
   an injected instruction in `AGENTS.md` as trusted.
3. **Nothing yet guarantees the note can't change the verdict.** The proposal
   promises the exit code never changes but not how. A bad lockfile entry could
   crash the check, and the easy way to write the code could skip the tamper
   check for a file.

Each closes with a few contract sentences and tests, with no engine change.

### The proposal at its strongest

An always-red neutrality gate protects nothing. Part 1 clears it with rewordings
and markers, adds no exemption to `templates/`, and leaves the checker's
behaviour alone. Part 2 reads data the lockfile already keeps, warns rather than
blocks, and checks its one new path before reading it. Much of what the author
asked me to check holds:

* **The edits are comment-only.** Python's own parser and tokenizer put all 33
  Python hit lines in comments (16) or docstrings (17); none is code. No edited
  file reads its docstrings at run time (`__doc__`, `getdoc`). The three
  session-kernel hits (lines 215, 905, 1338) lie outside `_resolve_interpreter`,
  `encode_display` and the call sites that run the resolved path. Pinned help
  text is literal strings. Nothing reads `vendor_targets.yml`'s `_doc`, the
  matrix generator included.
* **The AST proof is the right instrument where it counts.**
  `content_scan.py:329` is a comment between the string pieces of one regex,
  and `_OHM_SIGNS` holds two look-alike characters that an editor's Unicode
  normalization would merge. The proof catches both.
* **"No exemption path in `templates/`" holds** as the gate means it. Part 1
  adds no marker there, and the gate fails any `vendor-ok` or `case-study`
  marker in `templates/` (`scripts/quality_gate.py:268-288`).
* **The rate-limit claim is sound.** The markers change no rule.
  `doctrine/consolidation-review.md` prescribes this disposition
  (`accepted-exemption-added`) and its log row. The 2026-05-28 pass applied it
  the same way to `docs/quickstart.md` and `bootstrap/fidelity-check.md`.
* **The new read cannot leave the tree.** `resolve()` follows every link in the
  path, so an outward parent-directory link fails containment, not only a leaf
  link.
* **No shipped Markdown hit is inside a slot body.** I re-ran this check, so
  Part 1 cannot set off the reworded-placeholder gap.

### What I checked

All runs used Python 3.13.13 at the reviewed commit, on a `git archive` copy and
scratch installs in my scratchpad, never the shared tree.

* **The gate.** It reports `fail=74 info=21`. The 27 non-template hits are in
  exactly 5 files.
* **Three hidden plants, all in shipped templates:**
  * a whole-line `<!-- Per Codex P2-5 -->` in
    `templates/skills/session-start/SKILL.md`;
  * a lower-case `claude` in a comment in `templates/skills/_lib/session.py`;
  * `Per Codex P9` in `templates/modules/team-gated/content_scan_roots.txt`.

  All three left the gate at 74. A visible prose plant then moved it to 75, so
  the gate could have fired.
* **The hint, on a file with an edit outside its slots.** On a fresh
  `solo-greenfield` install, I filled `project-conventions` with the marker,
  added a line outside every slot, and committed. `verify_integrity` exited 1,
  and the hint named `AGENTS.md`. After `--finalize AGENTS.md`, it exited 0
  with the outside edit recorded as trusted.
* **Scoped finalize on a dirty tree.** I appended a line to
  `dev/proposals/_template.md` without committing, then ran `--finalize` on
  that path. It exited 0 and reported advancing the hash "to the committed
  on-disk content". `verify_integrity` then exited 0.
* **A prototype of the note's rule.** On a fresh install it lists the author's
  20 slots, and all 27 base copies hash to their record's `base_hash`. With
  `modules_remove: [security-verification]` it lists 21. The extra one is the
  empty `AGENTS.md [security-verification]` slot.
* **`content_scan.py` on marker reasons.** A `vendor-ok-begin` reason holding
  an imperative gets "no flags". The same comment without the `vendor-ok`
  prefix is flagged.
* **`_SLOT_BODY_RE` on unclosed openers.** Its run time grows with the square of
  their count: 2,000 take 0.6 s, and 16,000 (368 KB) take 35 s. Its `\S+` slot
  name also matches terminal control bytes.

### Findings

**[SR1] (blocking) "Neutrality reads zero" can be met by hiding names, and three
are already hidden.** If the only test of the rewording is the gate reading zero,
a name that is lower-cased or moved into an HTML comment still passes, and still
ships to every adopter. The gate has four blind spots:

* **Case.** Matching is case-sensitive; S5 names this one.
* **Comment lines.** In `templates/`, a line that is entirely one HTML comment
  is skipped before the token scan (`scripts/quality_gate.py:278-279`):
  `_is_directive_only_line` treats every such line as a directive. S5 does not
  name this.
* **File types.** `.json` and `.txt` files under `templates/` are never read
  (`_NEUTRALITY_FILE_SUFFIXES`, `scripts/quality_gate.py:440`). Not named.
* **Off-list names.** The `_doc` string Part 1 rewords also names GitHub
  Copilot, Windsurf, Cline and OpenCode, none of them on the denylist.

The second is live today. `reviewer="Claude (Implementation)"` sits in
`cairn-accept` markers at
`templates/modules/team-gated/api-access-security.md:101` and
`templates/modules/team-gated/web-hosting-security.md:70` and `:93`. These are
reviewer credits in shipped files, the same class as the 29, and the gate reads
past them. `content_scan.py` does not check the `reviewer=` value, so rewording
it suppresses nothing.

*Closes when:*

* Part 1's acceptance adds a check that does not share the gate's matcher. A
  case-insensitive search of every changed line, for the denylist plus the
  off-list harness names in the edited files, finds only routing ids and paths
  (`claude-code`, `.claude/skills`, and the like).
* The three `cairn-accept` credits are reworded along with the 38.
* S5 names the comment-line and file-type blind spots.
* The smoke check records all three plant shapes and their expected results:
  75 for visible prose, 74 for a comment line, 74 for lower case.

The stronger fix is for the gate to scan non-marker comment lines in
`templates/`. That changes the checker's behaviour, which this proposal rules
out, so my default is a board entry rather than adding it here.

**[SR2] (blocking) The note's remedy records the whole file as trusted, and the
safeguard it cites does not exist.** `--finalize <path>` makes
`verify_integrity` trust everything in the file, not just the slot the adopter
filled. If anything else in the file changed, following the note blesses it:
an injected instruction, or another session's unfinished work.

* **The safeguard claim is false for the command printed.** Part 2 item 4 says
  `--finalize` "refuses a tree with uncommitted changes", and S4 leans on that.
  The guard runs only for the unscoped form, under `if only is None and not
  force` (`bootstrap/_scaffold/upgrade.py:1814-1831`). The scoped
  `--finalize <path>`, which both the note and the hint print, never checks
  (reproduced above).
* **S5's hint gap becomes the main path.** The hint fires for any modified file
  with a marked slot, whatever else changed (reproduced above). `70e87171`
  narrowed it so that it would not invite blessing "a change nobody can
  explain". Today the marker is rare, so that gap is small. But the remedy puts
  the marker in every slot an adopter clears, 20 on a fresh install. The hint
  would then fire on nearly every modified Markdown file, the condition the
  narrowing was meant to prevent.
* **A tampered base copy can make the note advise finalizing a tampered file.**
  S1 accepts that a tampered base "can invent a placeholder". Now the invented
  entry arrives with an instruction to finalize that file. For the same reason,
  Revision 1 was right to drop the original S4's "never with more authority".
  The ledger should record that the phrase was dropped.

*Closes when:*

* The claims in S4 and Part 2 item 4 are corrected.
* The remedy the note prints, and the hint it relies on, both say that
  finalizing records the whole file, and give the command that shows
  everything about to be recorded:
  `git diff "$(git log -1 --format=%H -- dev/.cairn/cairn-lock.yml)" -- <path>`.
  I ran it; it shows the edit outside the slots.
* The note prints no finalize step for a file failing the integrity check in
  the same run, and says to resolve that failure first.
* A test pins it: for a file with a listed slot *and* an edit outside its
  slots, the note prints no finalize step.

Checking that every difference lies inside slots stays possible if the base is
first rendered with the profile's `cairn:if` choices and tokens. It needs an
engine function, so I do not require it.

**[SR3] (blocking) The promise that the exit code never changes has no structure
behind it.** If the note shares the integrity loop, it can change the verdict.
That loop handles a living-state record with `skipped += 1; continue`
(`bootstrap/verify_integrity.py:121-124`), and the proposal calls an unreadable
base "reported as skipped". Suppose the note goes in that loop and skips a
record with a bad `base_cache`. That record's tamper check is skipped too, and
a modified file passes. This is the one way the change could grant more
authority.

Lockfile values the note reads can also crash the run:

* a `base_cache` that is not a string, or names a directory or a FIFO (reading
  a FIFO blocks forever);
* a base copy that is not UTF-8;
* `tokens` that is not a mapping, or a token value that is not a string.

A crash exits 1 even on a tree that passed. If the note runs first, it can also
hide the integrity report.

*Closes when:*

* The contract says the note is a separate pass after the verdict is fixed.
  * It reads only records the integrity pass accepted.
  * It never touches `violations` or `skipped`.
  * It requires a regular file.
  * It reports every read, decode or type error as "not checked" in the
    coverage line.
* Tests show two things:
  * a modified file with an unsafe `base_cache` still exits 1;
  * each malformed value above leaves the exit code and the integrity report as
    they would be without the note.

**[SR4] (non-blocking) Tighten what the note reads and prints.** Each item is
cheap and narrows what a tampered tree can do to the note.

* **Check the base copy's hash before reading it.** Every copy I measured
  matches its record's `base_hash`. With the check, editing the cache alone can
  no longer steer the note; the lockfile would have to change too, where review
  sees it. That shrinks S5's residual.
* **Require `base_cache` under `dev/.cairn/base/`**, the only place the engine
  writes copies.
* **Cap the size of each file parsed**, and report a larger one as not checked.
  This bounds the slow-down measured above.
* **Escape the names it prints, and shell-quote the paths** in any command it
  prints, for example with `ascii()` and `shlex.quote`. Both come from files in
  the tree.

**[SR5] (non-blocking) "In every case, put the marker in the slot" does more
than quiet the note.** The engine treats a marked slot as the adopter's own. A
module merge into it is skipped silently
(`bootstrap/_scaffold/slotmerge.py:281-282`), and so is the fidelity check
(`bootstrap/_scaffold/slotmerge.py:455-456`). An adopter who opted out of
`security-verification` sees that empty slot listed (measured above). If they
follow the remedy and later turn the module back on, its Security-Review
designation never merges, and nothing reports it. `bootstrap/SAFETY.md` Rule
7(e) records that residual for an adopter who *chooses* to customize; this
remedy would cause it.

*Closes when:*

* The marker is prescribed only to keep Cairn's text on purpose. Once SR2's
  remedy prints the finalize command, filling a slot or writing `N/A` no longer
  needs the marker.
* An empty slot is either not listed, or listed as awaiting a module, with no
  marker advice.

**[SR6] (non-blocking) The comment-only proof cannot see comments that tools
obey.** A docstring-stripped AST comparison ignores every comment, including
those that change a security tool's verdict. An added `# nosec` silences Bandit,
the Layer-4 gate over exactly these files, and the proof still passes. No hit
line carries one today, so the risk is in the edit.

*Closes when* the proof also checks one of two things. Either no added or
removed line in the edited `.py` files holds `nosec`, `noqa`, `pragma`, `type:`
or an encoding line. Or Bandit's findings are the same before and after.

**[SR7] (non-blocking) The 27 markers are justified, with three notes.**

* **25 of them are illustrative or historical mentions in files that do not
  ship.** `scaffold.py --manifest` takes no source from `docs/` or `doctrine/`;
  the adopter's `docs/DOCUMENTATION_PLAN.md` comes from
  `documentation_plan_template.md`.
* **Two groups should be reworded, not marked:**
  * `bootstrap/tests/fixtures/skills/README.md:35` ("Codex P2#3") is a reviewer
    credit, the class Part 1 rewords.
  * The six `modflow_tools` lines in `docs/DOCUMENTATION_PLAN.md` say Cairn does
    not yet host its own `dev/` tree, which is no longer true.

  A marker certifies that a mention is legitimate, not that the sentence is
  true.
* **Marker reasons are text the scanner skips.** `content_scan.py` exempts any
  HTML comment beginning `vendor-ok` from its check for instructions in
  comments (`_CAIRN_MARKER_RE`,
  `templates/modules/team-gated/content_scan.py:319-334`; reproduced above). So
  each new reason is hidden, agent-loaded text that only Rule 7's human
  injection review reads. The plan should say so.
* **Keep markers tight, and record `info=` next to `fail=0`** in the Boundary B
  baseline. Use one-line markers, or blocks that span only the hit lines. A name
  added inside a block later then shows as a changed count.

**Outside this proposal, recorded.** Cairn's own `verify_integrity --target .`
already reports 18 violations. Among them are two shipped-as-is scripts,
`scripts/claim_check.py` and `tools/_intent/conflict.py`. Cairn's lockfile
records every twin Part 1 edits, most of them as shipped-as-is scripts, so
Part 1 will add to that count. This is #2's always-red shape, on the check Part 2 extends. The plan
should finalize the edited twins once they are confirmed byte-identical to their
templates, or record that it does not.

### Verdict and what clears the obligation

**REVISE.** What the proposal changes is sound; the gaps are in what it relies
on. SR1-SR3 close with contract sentences and tests, with no new mechanism and
no engine change. After the author's Response and revision, a Security Review
pass that reads only SR1-SR3's closures clears the obligation. That pass is the
one clearing round the lifecycle allows.

**No new question for the Maintainer.** Where to put the stronger gate fix in
SR1 is the author's call; my default is a board entry.

## Response -- Claude (author) -- 2026-10-17 (to the Security Review)

All three blocking findings are accepted. Each was measured again today under
Python 3.13.13. One correction comes first: Revision 1 said `--finalize <path>`
refuses uncommitted work. It does not. Only the unscoped form runs the
dirty-tree guard (`bootstrap/_scaffold/upgrade.py:1814-1831`). Revision 2
withdraws the claim. Since Revision 1, `a3f39aef` changed the existing hint: it
now says "Check that nothing outside its slots changed (--finalize records the
whole file)". Revision 2 builds on that text.

**SR1: accepted. The gate gets stricter, and the claim is narrowed to what is
left.** I took the stronger fix rather than a board entry. In `templates/` it
costs three small changes to the checker:

* scan whole-line HTML comments;
* add `.json` and `.txt` to the file types read;
* add the four harness names the routing table itself lists (Copilot, Windsurf,
  Cline, OpenCode).

On a copy of HEAD this moves the gate from 74 to 81. The 7 new findings are the
three `reviewer="Claude (Implementation)"` credits and the four names on the one
`_doc` line, and Part 1 rewords all of them. The credits become
`reviewer="agent"`, the form `templates/core/NOTICE.md` already uses. Nothing is
exempted; the gate can only fail more often.

Your three plants, plus a visible one, against each gate (change in the count
from that gate's baseline: 74 today, 81 stricter):

| Plant | Current gate | Stricter gate |
|---|---|---|
| Whole-line comment | +0 | +1 |
| `.txt` | +0 | +1 |
| Visible prose | +1 | +1 |
| Lower case | +0 | +0 |

Lower case and names not on the list stay outside the gate. Two things cover
them:

* For this change, a one-time case-insensitive search of every changed line, run
  without the gate's matcher, must find only routing ids and paths.
* For the standing claim, "zero" is narrowed to say what it covers, and S5 names
  all four blind spots.

This changes the checker's behaviour, which Revision 1 ruled out. **That is a
widening, stated here plainly.**

**SR2: accepted.**

* **No finalize step for a failing file.** The note no longer reads any file
  that fails the integrity check in the same run. Such a file is counted "not
  checked: resolve the integrity failure above first", with no finalize step.
* **Show what will be recorded.** For a file that passes, each remedy ends with
  the review command
  `git diff "$(git log -1 --format=%H -- dev/.cairn/cairn-lock.yml)" -- <path>`,
  which shows every change since the lockfile was last committed. The `--finalize`
  command follows it, and the remedy says finalizing records the whole file.
  The existing hint gains the same review command after `a3f39aef`'s sentence.
* **Base copies are checked first** (SR4): a base copy must hash to its record's
  `base_hash` before it is read. Editing the cache alone can then no longer
  steer the note. All 32 copies on both upgraded probe trees match, and so do
  all 27 on a fresh install.
* **Ledger.** It records that Revision 1 dropped the original S4's "never with
  more authority".

**SR3: accepted, and given a structural form.** `verify()` finishes the integrity
pass and prints its report unchanged. It then fixes the exit code. Only after
that does it call the note, which runs as a separate function:

* **It receives only the accepted files.** It is passed the bytes of the files
  whose hash matched, which the integrity pass has already read. It never
  receives `violations`, `skipped` or the exit code.
* **The call is fenced.** It is wrapped so that any exception prints one
  "slot note not run" line, and nothing more.
* **Per-record failures become coverage counts.** Inside the note, each record's
  type, read and decode errors are counted as "not checked" in the coverage
  line.
* **Base copies are read defensively.** Each is opened without following links
  and without blocking. It must then be a regular file of at most 256 KiB, which
  is twelve times the largest shipped template.

The tests compare every malformed input you listed against a run with the note
replaced by a no-op. The exit code and the integrity report must be identical.

**SR4: accepted.**

* The base copy must match `base_hash`.
* `base_cache` must lie under `dev/.cairn/base/`.
* Each file read is capped at 256 KiB. With the hash checks, a tree can reach
  `_SLOT_BODY_RE`'s slow case only by also changing the lockfile.
* Slot names are printed with `ascii()`, and paths are passed through
  `shlex.quote`.

**SR5: accepted.** The marker is prescribed only for keeping Cairn's text on
purpose. Filling a slot or writing `N/A` no longer needs it, now that the
remedy prints the review and finalize steps. An empty slot that is also empty
in its base copy is counted as "empty: filled when its module is installed".
It is never listed and gets no advice.

**SR6: accepted.** The comment-only proof adds a check over the diff: no added
or removed line in an edited `.py` file may hold `nosec`, `noqa`, `pragma`,
`type:` or an encoding declaration.

**SR7: accepted.**

* **Reworded rather than marked:**
  * `bootstrap/tests/fixtures/skills/README.md:35`, a reviewer credit;
  * the stale "Cairn does not yet self-host `dev/`" sentences in
    `docs/DOCUMENTATION_PLAN.md`.
* **Marked:** the reference deployment's name stays only where it is history,
  under a marker.
* **Marker reasons:** short and declarative. The plan records that
  `content_scan.py` skips them, so only Rule 7's human review reads them.
* **Marker scope:** one-line markers, or blocks no wider than their hit lines.
* **Baseline:** Boundary B records `info=` beside `fail=0`.

**Outside the proposal: Cairn's own integrity record.** Cairn's own record
already shows 18 violations. The plan scoped-finalizes exactly the edited twins
that the record attests today, once each is confirmed byte-identical to its new
template; recent commits already do this. The 18 existing violations are left
alone, so the count does not grow.

**Status.** Revision 2 widens scope in one place: the checker's stricter scan
(SR1). It also touches five more files than Revision 1:

* `bootstrap/tests/test_quality_gate_neutrality.py`;
* the two security module templates holding the credits;
* `docs/DOCUMENTATION_PLAN.md`, now reworded;
* Cairn's own lockfile, for the scoped finalize.

That brings the files the gate manifest pins to 16. No engine change. Q1 and Q2
are unchanged, and nothing new goes to the Maintainer. The Security Review
obligation stays open until a second Security Review pass reads SR1–SR3's
closures, so Status returns to `awaiting-review`.

## Revision 2 -- Claude (author) -- 2026-10-17 -- the complete current contract

### In plain terms

Two of Cairn's checks cannot be trusted today, for opposite reasons.

1. **The vendor-name check is always red, so a new problem would be invisible
   (#2).** `quality_gate.py --sub neutrality` keeps AI-vendor and project names
   out of what Cairn ships. It reports 74 failures today. 38 are real leaks:
   reviewer names and our reference project's name in files every adopter
   receives. This proposal does three things:
   * makes the check a little stricter, so it also reads comment lines and two
     more file types;
   * fixes every finding;
   * makes zero mean something.

   **Zero will mean** that no listed vendor or project name appears, in its
   normal capitals, anywhere in a scanned file that ships. **It will not cover**
   lower-case spellings or names missing from the list. A one-time search
   covers those for this change. The check was zeroed once before, in May, and
   refilled within hours. Since then it has come to run in every plan's final
   verification, and a project rule now bars crediting reviewers in code.
2. **When an upgrade adds a fill-in section ("slot"), nothing says so (#8).**
   The install check (`verify_integrity.py`) gets an advisory note listing slots
   that still hold Cairn's placeholder text. It always says how much it could
   check.
   * **It reads only files that pass the integrity check.**
   * **Its instructions end in reviewing everything about to be recorded**, not
     in blessing a file blindly.
   * **It cannot change the check's verdict.** It runs after the verdict is
     fixed, and it has no way to reach it.
   * **One limit:** on a tree with many unfilled slots, the new slot is listed
     but not singled out.
3. **#16 is split.** Its proposed new check is declined. Its one-paragraph half
   is a question below.

**Cost to you.** There is no engine change, so no hand re-anchor of its
fingerprint. Up to 16 files the gate manifest pins change. They join the next
gate-manifest re-anchor. One is queued (`dev/PLANNING.md:156`); if it runs
first, these wait for the following one.

**If this is wrong,** a reworded comment loses an explanation someone needed, or
the note nags. Both are cheap to undo.

**Questions, each with a default.**

* **Q1. #16 asks for two things.**
  * (a) A new shipped check. Close it as won't-build under your three-recurrence
    rule? *Default: yes.*
  * (b) One paragraph in the doc-drift module, naming prose that refers to a
    function the code no longer has. *Default: write it, as a separate small
    change after this Decision; #16 closes when it lands.*
* **Q2. Should `upgrade` itself name the slots it adds?** That would single the
  new slot out on a partly filled tree, but it changes the engine and costs a
  hand re-anchor of its own. *Default: not in this change. Carry it in the next
  engine change to the upgrade path that already owes a re-anchor, or sooner if
  an adopter misses an upgrade-added slot.*

### Context

**The neutrality gate (#2).** Today, `python scripts/quality_gate.py --sub
neutrality` reports `fail=74 info=21` and exits 1. Every recorded run has been
red, against a manifest expecting "green"
(`bootstrap/tests/_gate_manifest.py:149-151`):

| Failures | Source |
|---|---|
| 99 | `dev/proposals/archive/2026-07-11-claude-record-corrections.md:30` |
| 93 | `dev/proposals/archive/2026-08-12-claude-boundary-b-bounding-clause.md:544` |
| 79 | `dev/plans/archive/portable-sweeps-cannot-run.md:385` |
| 74 | `dev/plans/archive/adopter-path-consolidation.md:520` |

| Where | Count | What they are | Disposition |
|---|---|---|---|
| `templates/skills/` (routing table, session kernel, session-start skill) | 9 | prose repeating the routing table | reword |
| `bootstrap/tests/fixtures/skills/README.md` | 5 | routing-fixture notes; one reviewer credit (`:35`) | credit reworded; rest marked |
| other shipped templates, reviewer names | 29 | a design choice credited to a reviewer | reword |
| other shipped templates, `modflow_tools` | 9 | the reference project's name | reword |
| `docs/` | 14 | an example roster; six stale "not yet self-hosted" lines | stale lines reworded; rest marked |
| `doctrine/` | 8 | example agent identities; an illustrative tool list | marked |

**The routing data already passes.** The gate matches capitalized whole words
(`scripts/quality_gate.py:280-281`). The routing table's ids are lowercase
(`claude-code`, `codex`). Reviewer credits in code already break `AGENTS.md` >
"Comments and docstrings explain the code, not the process".

**The gate has four blind spots** (the Security Review's plants, measured
today):

* **Whole-line HTML comments** in `templates/` are skipped before the token scan
  (`scripts/quality_gate.py:278-279`). Three reviewer credits sit there today
  (`templates/modules/team-gated/api-access-security.md:101`;
  `templates/modules/team-gated/web-hosting-security.md:70` and `:93`).
* **`.json` and `.txt` files** in `templates/` are never read
  (`scripts/quality_gate.py:440-449`).
* **Matching is case-sensitive.**
* **Names missing from the list pass.** The `_doc` string names four.

On a copy of HEAD, closing the first two and listing the four names moves the
gate from 74 to 81. Every one of the 7 new findings is a line Part 1 rewords.

**Zero has been reached before.** On 2026-05-28, `29ffeea6` reached `fail=0`.
That same afternoon, `dbc09557` added the first "Codex P2-5". Two things differ
now:

* Boundary B has run the gate on every plan since `5f6ecccc`.
* Crediting reviewers in code has been against `AGENTS.md` since `013847b6`.

Since 2026-06-11, the failing lines were touched only by an extraction
(`ea3d6492`) and a rewording (`a29183a9`), neither of which added a name.

**Upgrade-introduced slots (#8).** I installed `4ad1c115` (`solo-greenfield`),
filled all 23 slots, finalized and upgraded to HEAD.

* **What arrived:** `assurance-path-triggers` arrived holding its placeholder.
* **Upgrade output:** it flags removed slots and has no kind for added ones
  (`bootstrap/_scaffold/upgrade.py:718-719`).
* **Other tools:** `verify_integrity.py` and `session-start` say nothing.
* **The upgrade guide:** `bootstrap/UPGRADE.md:101-102` does not say which slot.

A scratch prototype of Part 2's rule gave:

* **Fully filled tree:** it names that one slot.
* **Only the three Maintainer slots filled:** it lists 17 and does not single
  out the new one.
* **Cairn's own tree:** it checks 0 slots, because it holds base copies for only
  2 files. It also finds 1 base copy whose hash no longer matches.

The issue's suggested home (`lifecycle_planner scan`) was removed in
`bfe6bbfd`. The fields its comment asked to be taught are now taught
(`templates/core/dev/proposals/_template.md:230-231`).

**Recording an edit today.**

* Filling a slot makes `verify_integrity` exit 1, because the file's hash
  changed.
* `--finalize <path>` records the whole file, and the scoped form skips the
  dirty-tree guard (`bootstrap/_scaffold/upgrade.py:1814-1831`).
* The hint names finalize only for a file with a slot marked customized, and
  since `a3f39aef` it asks the adopter to check outside the slots first.
* The Security Review showed that marker plus finalize can record an edit made
  outside the slots.

**#16.** The check it proposes is the machinery your 2026-08-25 triage declined.
Its other half is one paragraph for
`templates/modules/team-gated/doc-drift-prevention.md:48-51`; that is Q1(b).

### Proposal

**Part 1: neutrality reads zero, with a stricter checker.**

1. **The checker.** In `templates/`, `scripts/quality_gate.py` changes in four
   ways:
   * it scans whole-line HTML comments for tokens (a `vendor-ok` or
     `case-study` directive there already fails);
   * it reads `.json` and `.txt`;
   * Copilot, Windsurf, Cline and OpenCode join the denylist;
   * the false comment at `:446` is corrected.

   No exemption is added. Each change can only add failures.
2. **The 9 `templates/skills/` hits are reworded** to point at the routing table.
   The `_doc` string keeps no harness name in its prose; the lowercase ids in
   the rows stay.
3. **The 38 hits in 14 other shipped templates are reworded.** Each reviewer
   credit gives its reason in code terms. `modflow_tools` becomes "the reference
   deployment" or is dropped.
4. **The three `cairn-accept` credits** become `reviewer="agent"`.
5. **Rewordings in Cairn-internal files:**
   * the reviewer credit at `bootstrap/tests/fixtures/skills/README.md:35`;
   * the stale "not yet self-hosted" lines in `docs/DOCUMENTATION_PLAN.md`.
6. **Markers for the rest of `docs/`, `doctrine/` and the fixture README.**
   Illustrative or historical mentions there get `vendor-ok` markers. Each
   marker is either one line, or a block spanning only its hit lines, and
   carries a short declarative reason.
7. **The pass is logged** in the "Dogfood disposition log" of
   `doctrine/consolidation-review.md`.
8. **Twins change in the same commit, byte-identical.** They are:
   * `.agents/skills/_data/vendor_targets.yml`
   * `.agents/skills/session-start/SKILL.md`
   * `tools/session.py`
   * `scripts/_onboarding/` (`__init__`, `activation`, `cli`, `security`,
     `shared`, `triggers`)
   * `scripts/onboarding_activate.py`
   * `tools/intent.py`
   * `scripts/content_scan.py`
   * `dev/modules/documentation-plan.md`
   * `dev/modules/incident-trackers.md`
   * `dev/modules/incident_log_template.md`

   The edited twins that Cairn's own lockfile attests today are scoped-finalized.
   Its existing violations are left alone.

**Part 2: an advisory slot note in `bootstrap/verify_integrity.py`.**

1. **A separate pass, after the verdict.**
   * `verify()` runs the integrity pass and prints its report as today.
   * It then fixes the exit code.
   * Only then does it call the note. The note gets the bytes of the
     non-verbatim files whose hash matched, already read, and nothing else: not
     `violations`, not `skipped`, not the exit code.
   * The call is wrapped. Any exception prints one "slot note not run" line, and
     the exit code returned is the one fixed before the call.
2. **What it trusts.** It reads a record's `base_cache` only if all of these hold:
   * it is a string naming a path under `dev/.cairn/base/` inside the target;
   * no part of that path is a symlink;
   * it opens without following links and without blocking;
   * it is a regular file of at most 256 KiB;
   * it decodes as UTF-8;
   * it hashes to the record's `base_hash`.

   It substitutes tokens only from a string-to-string `tokens` mapping. Anything
   else is counted as not checked, with its reason.
3. **What it lists.** A slot is listed when its body is unchanged from the base
   copy's, after spacing is normalized and tokens substituted. Two kinds of slot
   are left out:
   * a slot carrying `<!-- cairn:customized -->`;
   * a slot that is also empty in its base copy. It is counted as "empty: filled
     when its module is installed".

   It reads slots with the file's `_SLOT_BODY_RE`. The token pattern and spacing
   rule are inlined, and a test pins both to the engine's.
4. **One coverage line, always printed.** It gives:
   * slots and files checked;
   * the number still holding the shipped text;
   * empty slots awaiting a module;
   * files not checked, by reason: no base copy, failed the integrity check,
     base hash mismatch, or unreadable.

   Names print through `ascii()`.
5. **The remedy for each listed slot.**
   1. Fill the slot or write `N/A: <reason>`, then commit.
   2. Review everything `--finalize` will record:
      `git diff "$(git log -1 --format=%H -- dev/.cairn/cairn-lock.yml)" -- <path>`.
   3. Run `python bootstrap/scaffold.py upgrade --target <repo> --finalize
      <path>`, then commit the lockfile.

   The remedy also says:
   * finalizing records the whole file;
   * to keep Cairn's text on purpose, add `<!-- cairn:customized -->` inside the
     slot instead.

   Paths are shell-quoted. A file that failed the integrity check gets no
   remedy, only "resolve the integrity failure above first".
6. **The existing hint gains the same review command,** after the sentence
   `a3f39aef` added. Which files it names does not change.
7. **`bootstrap/UPGRADE.md` gains:**
   * step 4: run `verify_integrity` after `--apply`, which only a person
     following the steps does;
   * the note's meaning;
   * the known gap: a placeholder that an upgrade rewords reads as filled.
8. **It reports placeholder state, not obligation.** Which slots a profile needs
   is F8 (`dev/PLANNING.md:208`), and it stays separate.

### Rationale

The gate's rule is right: templates stay clean by construction, with no
exemption path (`scripts/quality_gate.py:268-288`). Making it read the lines and
files it skipped serves that rule, and costs 7 findings Part 1 fixes anyway. Zero
failed to hold in May because nothing ran the gate routinely and crediting
reviewers in code was habitual. Both have changed.

The note puts the hand check (`bootstrap/BOOTSTRAP.md:525-527`) in a tool
adopters already run. It warns rather than blocks
(`dev/strategy/2026-08-21-claude-nimbleness-recovery.md:332`). Every way it can
go wrong is confined to its own output.

### Alternatives considered

* **The exemption path #2 asks for.** It turns "clean by construction" into
  "clean by review", to cover 9 lines a rewording removes.
* **Freeze today's 74 and fail only on new ones.** That accepts 38 shipped leaks
  with no reasons.
* **Keep the checker unchanged and record the blind spots on the board** (the
  Security Review's default). Rejected: a zero that misses a reviewer credit in
  a comment line is the failure Part 1 exists to remove, and the fix measured at
  7 findings.
* **A case-insensitive gate.** It would flag every routing id (`claude-code`,
  `.claude/skills`, the harness environment variables). That needs an
  allowlist, which is an exemption path.
* **`upgrade` names the slots it added. This is the strongest rejected
  alternative.** It singles the new slot out without needing a later step. It
  loses for now because it changes at least `merge_file` and
  `_print_upgrade_report`, which owe their own re-anchor. Q2 carries it.
* **Widen the hint to diffs that touch only slots.** Rejected: `cairn:if`
  rendering makes `AGENTS.md` differ from its base outside the slots.
* **Block on an unfilled slot.** Rejected: process checks warn.
* **Do nothing.** The gate stays unreadable, names keep shipping, and new slots
  stay silent.

### Documentation / doctrine surface

* **Descriptive.**
  * `bootstrap/UPGRADE.md`: step 4, the note's meaning, and the known gap.
  * `docs/DOCUMENTATION_PLAN.md`: stale lines corrected.
* **Governing.** None. `AGENTS.md` > "Vendor-neutrality" stays true.
* **Doctrine.** Marker-only edits in `doctrine/lifecycle-contract.md` and
  `doctrine/rationale.md`, plus log rows in `doctrine/consolidation-review.md`.
  * **Rate-limit gate** (`doctrine/rationale.md:405-417`): not triggered. No
    rule changes; this is the procedure `doctrine/consolidation-review.md`
    prescribes.
  * **Fallback:** if the markers count as doctrine changes, leave those 8 lines
    unmarked, and the gate reads `fail=8`.
* **CHANGELOG.** One entry.

Marker reasons are text `content_scan.py` skips
(`templates/modules/team-gated/content_scan.py:319-334`). Only Rule 7's human
review reads them, so they stay short and declarative.

### Evidence / verification plan

#### Tests required

**`bootstrap/tests/test_quality_gate_neutrality.py`.** One test for each:

* a token in a whole-line HTML comment in `templates/` fails;
* a token in a `templates/` `.txt` or `.json` file fails;
* each of the four new names fails;
* the existing nodes still pass.

**`bootstrap/tests/test_verify_integrity.py`.** Each case builds its own
lockfile, base cache and files in `tmp_path`.

* **The whole loop**
  1. The slot is listed.
  2. The adopter fills and commits it.
  3. The review command shows only that edit.
  4. After `--finalize` and a commit, the exit code is 0 and the slot is no
     longer listed.
* **No remedy for a failing file.** A listed slot plus an edit outside the slots
  makes the file fail the integrity check. The note then prints no finalize step,
  and says to resolve the failure first.
* **Verdict unchanged.** Each of these inputs leaves the exit code and integrity
  report identical to a run with the note replaced by a no-op:
  * a `base_cache` that is not a string;
  * a `base_cache` naming a directory or a FIFO;
  * a symlinked or outside path;
  * a path outside `dev/.cairn/base/`;
  * a file over the cap;
  * non-UTF-8 bytes;
  * a `base_hash` mismatch;
  * `tokens` that is not a mapping;
  * a token value that is not a string;
  * an exception raised inside the note.
* **The record still fails on its own.** A modified file with an unsafe
  `base_cache` still exits 1.
* **Coverage and listing.**
  * The coverage line on a tree with no base copies.
  * Verbatim records are not read.
  * Customized and empty slots are not listed.
  * Token substitution.
  * `ascii()` escaping of a control-byte slot name.
  * The inlined patterns agree with the engine's.
  * The reworded-placeholder known gap is pinned.

**Boundary B mode: full.**

#### Examples / smoke checks

* **The gate.** It reads `fail=0`; Boundary B records `info=` beside it. Each
  plant's expected result, from that zero:
  * visible prose: `fail=1`;
  * whole-line comment: `fail=1`;
  * `.txt`: `fail=1`;
  * lower case: `fail=0`, the named blind spot.
* **The one-time search.** A case-insensitive search of every changed line, for
  the denylist and the four names, finds only routing ids and paths
  (`claude-code`, `.claude/skills`, and the like).
* **The comment-only proof.**
  * Every edited `.py` gives an identical docstring-stripped `ast.dump`, the
    checker excepted.
  * No added or removed line holds `nosec`, `noqa`, `pragma`, `type:` or an
    encoding line.
  * `vendor_targets.yml` parses the same apart from `_doc`.
  * A one-character code change in a scratch copy breaks the comparison.
* **Twins.** They are byte-identical. Cairn's own violation count does not grow.
* **Both probes, re-run.**
  * Fully filled: one slot is named.
  * Partly filled: the new slot is listed among the rest (the Q2 limit).
* **`python scripts/check_cairn.py`** over the touched Markdown.

#### Security preflight — five questions, answered in writing

* **S1 — Who supplied it?**
  * Part 1 adds no decision and no exemption.
  * Part 2 decides from four things: installed bytes the integrity pass already
    matched to the lockfile, a base copy it re-checks against `base_hash`, the
    lockfile's tokens, and the lockfile itself. All of them come from the
    adopter's tree. Steering the note therefore takes a lockfile change, which
    review sees.
  * The note grants nothing, and it never advises recording a file that failed
    the check.
* **S2 — Can it fail?** Both checks can.
  * For the gate, the plants are as tabled above, all run today.
  * For the note, the prototype went from 1 to 0 when the slot was filled.
  * The note's expectation comes from the base copy, not from the checked file.
* **S3 — What fires it, over what?**
  * Part 1: a person runs it at Boundary B (`AGENTS.md` > "Verification
    boundaries") and at the gate-manifest ceremony; no hook runs it. It covers
    `_NEUTRALITY_FILE_SUFFIXES`, which now includes `.json` and `.txt` under
    `templates/`.
  * Part 2: a person runs `verify_integrity`, as UPGRADE.md step 4 says. It
    covers the non-verbatim records the integrity pass accepted.
* **S4 — Which way does it break?**
  * Every read, type or decode failure becomes a "not checked" count in the
    coverage line.
  * A reworded placeholder reads as filled: the known gap.
  * The exit code is fixed before the note runs, and the note cannot reach it.
  * `--finalize <path>` records the whole file and skips the dirty-tree guard.
    So the remedy shows the full diff first, and gives no remedy for a failing
    file.
* **S5 — Who still wins?**
  * Lower-case spellings, and names missing from the list. 26 lowercase-only
    mentions under `templates/` and `doctrine/` pass today, mostly routing ids
    and environment-variable names. This is closed by enumeration, and this
    change's one-time search covers only its own edits.
  * Anyone who changes the lockfile together with a base copy can steer the
    note.
  * An adopter who runs `--finalize` without reading the diff.
  * The hint (`70e87171`, `a3f39aef`) still names any modified file with a
    marked slot. Part 2 adds the diff command to it.

### Signals the change is wrong

* **A Boundary B record after archive** shows a neutrality failure the change
  under test did not introduce. Then the commit hook is owed.
* **A reworded comment dropped an explanation** someone needed.
* **The note becomes noise.** Adopters add `cairn:customized` by reflex, or the
  note names filled slots.
* **An upgrade-added slot is missed on a partly filled tree.** Then Q2 comes due.

### Scope delta

**Scope delta**: preserved. Nothing in the baseline is dropped. Revision 2
widens it in one place, the checker's stricter scan. It also touches five more
files: the neutrality test, two security module templates, a reworded
`docs/DOCUMENTATION_PLAN.md`, and Cairn's own lockfile (scoped finalize of
edited twins).

### Assurance path

**Assurance path**: high-assurance

The change reaches:

* the vendor-neutrality boundary and its checker;
* the content scanner and the interpreter-binding module, in comments only;
* the lockfile reader adopters run before trusting their scripts;
* Cairn's own install record.

### Withdrawn / superseded commitments

* **"`--finalize` refuses a tree with uncommitted changes"** (Revision 1, Part 2
  item 4 and S4). Withdrawn: false for the scoped form (SR2).
* **"A finalize run is exactly as safe as the adopter's review of their own
  commit."** Superseded: the remedy now prints the diff that finalize records,
  and no remedy for a failing file (SR2).
* **"Never with more authority"** (the opened proposal's S4). Recording it as
  dropped, as Revision 1 did (SR2).
* **"The checker's behaviour is unchanged."** Superseded by the stricter scan
  (SR1).
* **"Neutrality reads zero" as an unqualified claim.** Narrowed to what the
  gate covers, with the four blind spots named (SR1).
* **"In every case, put the marker in the slot."** Superseded: the marker is
  only for keeping Cairn's text on purpose (SR5).
* **The note reads every non-verbatim record.** Superseded: it reads only
  records the integrity pass accepted, and base copies matching `base_hash`
  (SR2, SR3, SR4).
* **The 27 markers.** Partly superseded:
  * the fixture credit and the stale docs lines are reworded (SR7);
  * markers are tight.
* **"Up to 15 pinned files."** Now 16.

## Review -- Claude Opus 5.5 (Security Review, round 2, fresh session) -- 2026-10-17

```
Reviewed commit: aa13b2f3d8b5fc7b73d484a5d57958b7d76cc3ab
Target: Revision 2 (the binding contract) and its Response, read for SR1-SR7's closures and for the widened scope (the stricter neutrality checker), against scripts/quality_gate.py, bootstrap/verify_integrity.py as of a3f39aef, the --finalize code, the lockfile helpers and Cairn's own lockfile
Prior findings: SR1-SR7 (this tier, round 1)
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: raised (1 blocking, 6 non-blocking)
**Verdict**: REVISE

Distance: a fresh session of the author's agent type, not a different type. I
wrote neither the proposal nor an earlier review of it. This is the second
Security Review round, which the lifecycle allows while the obligation is open.
It does not clear the obligation yet.

### In plain terms

Revision 2 answers the first Security Review well, and the stricter vendor-name
check is a good change in its own right. One thing still blocks:

* **The "review before you record" command can show nothing while the record
  step blesses a planted line.** The command compares the file with its copy at
  the last commit that touched the lockfile. That works only if the file still
  matched its record at that commit. On an ordinary first install the adopter
  fills slots before the first commit, so it did not. I planted a line in
  `AGENTS.md` that way, telling agents to download and run a remote script. The
  command printed nothing, `--finalize` recorded the line, and the install check
  then said OK.
  The note's own fix-it steps are safe, because they cover only files that match
  their record now. The problem is adding the command to the existing warning,
  which fires only for files that have already changed.

The fix is a few sentences and one test, with no new mechanism. The other six
findings are smaller and can land in the same revision or in the plan. They
cover three placeholders that drop out of the count silently, a "zero" sentence
that still says too much, a dropped fallback the ledger does not record, and
build details.

No new question for the Maintainer.

### The widened scope: the stricter checker

It should happen. It closes two of the four blind spots the first review found,
adds no exemption, and makes the checker do what Part 1 would otherwise only
promise. I measured it with a patched copy of `scripts/quality_gate.py` run on a
`git archive` of the reviewed commit:

* **The count.** It goes from 74 to 81. The 7 new failures are exactly the three
  `reviewer="Claude (Implementation)"` credits and the four names on line 2 of
  `templates/skills/_data/vendor_targets.yml`.
* **It only adds.** All 74 of today's failures are among the 81, and nothing
  else moved.
* **No false alarms in data.** The six `.json` and `.txt` files under
  `templates/` produce no finding. The one near miss, `CLAUDE.md` in
  `content_scan_roots.txt`, passes because matching is case-sensitive. The four
  new names hit nothing outside `templates/`.
* **Removing the comment-line skip hides nothing.** The directive check runs
  before the token scan and does not change. A directive line that also carries
  a name now counts twice (+1 today, +2 stricter): two genuine failures on one
  line, never a masked one.
* **The plant table reproduces.** Each figure is the change from that gate's
  baseline:

| Plant | Current gate | Stricter gate |
|---|---|---|
| Visible prose | +1 | +1 |
| Whole-line comment | +0 | +1 |
| `.txt` | +0 | +1 |
| `.json` value | +0 | +1 |
| Lower case | +0 | +0 |
| `ClaudeCode`, `GPT4o`, `Claude_Code` | +0 | +0 |
| A zero-width character inside a name | +0 | +0 |

The last two rows are blind spots the narrowed sentence does not name (SR10).

### SR1-SR7: where each stands

* **SR1: resolved**, as above. The leftover wording is SR10.
* **SR2: partly resolved.**
  * *No remedy for a failing file* holds by construction, because the note
    receives only files that match their record.
  * *The `base_hash` gate* is sound. 27 of 27 base copies match on a fresh
    install, and 1 of 2 on Cairn's tree, as stated.
  * *The claims and the ledger* are corrected.
  * *The review command* does not do what the contract says: SR8.
* **SR3: resolved.** The exit code is fixed before the note runs, the call is
  fenced, and per-record failures become counts. Build details are in SR12.
* **SR4: answered.** Details in SR12.
* **SR5: answered.** One consequence the ledger misses: SR11.
* **SR6 and SR7: answered.**

### What I checked

All runs used Python 3.13.13, on a `git archive` of the reviewed commit and on
scratch `solo-greenfield` installs, all in my scratchpad:

* the gate counts and plants above;
* the review command against `--finalize`, in four commit histories (SR8);
* a prototype of the note's rule on a fresh install: 17 listed slots in files
  that pass, plus 3 in living-state files (SR9);
* the no-follow, non-blocking open on macOS, against a symlink, a FIFO and a
  directory (SR12);
* `_SLOT_BODY_RE` timing on unclosed openers at the cap (SR12);
* Cairn's own lockfile records for every twin Part 1 edits (SR14).

### Findings

**[SR8] (blocking) The review command can show an empty diff while `--finalize`
records a planted line.** An adopter following the printed steps can record an
injected instruction in `AGENTS.md` as trusted. That is the file agents obey
(`bootstrap/SAFETY.md` Rule 7). This is SR2's harm, now with a tool telling the
adopter it checked.

The command shows the changes since the lockfile was last *committed*.
`--finalize` records every change since the file's recorded *hash*. The two
agree only when the file still held its recorded content at that commit.
Measured on scratch installs at the reviewed commit, with a slot filled and a
line planted outside it:

| History | The command shows | `--finalize` records |
|---|---|---|
| A. Install committed clean; slot filled and committed later | the fill, exactly | the fill |
| B. Slot filled (with the marker) and line planted **before the first commit**; everything committed together | **nothing** | the fill and the planted line; `verify_integrity` then says OK |
| C. Planted line committed with an unrelated scoped finalize of `NOTICE.md`; slot filled later | **the fill only** | the fill and the planted line |
| D. Lockfile never committed | `fatal: bad revision ''` | — |

So, to the author's question: when the file and the lockfile were not committed
together, a change committed *after* the lockfile's last commit is shown. A
change committed *at or before* it is hidden, including one carried in someone
else's unrelated finalize commit. Case B is an ordinary first install: fill the
slots the acceptance checklist asks for (`bootstrap/BOOTSTRAP.md:525-527`), then
commit.

The note's remedy (Part 2 item 5) is safe where it is. It is printed only for
files that match their record now, which is case A. The defect is item 6. It
adds the same command to the existing hint, and the hint fires only for files
that already fail (`bootstrap/verify_integrity.py:136-139`): cases B and C.
Item 5's heading, "Review everything `--finalize` will record", also states as
fact what holds only in case A. The S4 and S5 lines that rely on it inherit the
error.

*Closes when:*

* No printed command is described as showing what `--finalize` will record
  unless it does.
  * **The hint.** Default: drop item 6. The hint says plainly that
    `verify_integrity` keeps only a hash, so it cannot show what changed. The
    adopter reads the file, or its history (`git log -p -- <path>`), before
    recording it. One alternative: print the recorded hash and a one-line check
    that the commit's copy hashes to it, falling back to the whole-file review
    when it does not.
  * **Item 5.** It says what its command shows, and why that is complete for a
    file listed as matching its record. If the lockfile has never been
    committed, it says to commit the lockfile first.
* A test reproduces case B: a file already modified when the lockfile was
  committed, with a marked slot and a line outside it. The printed text must not
  present the commit diff as the whole change.

**[SR9] (non-blocking) Three of a fresh install's twenty placeholders vanish
from the count without a word.** A short count then reads as "nearly done" when
it is not, NU3's failure again. The note reads only records the integrity pass
accepted. Living-state files (the roadmap, the handoff, the signed agreement)
are skipped by that pass, not accepted, and the coverage line has no reason for
them. On a fresh install they hold `dev/NEXT_SESSION.md [next-start]`,
`dev/PLANNING.md [project-status]` and `dev/collaboration_agreement.md
[team-roster]`, all with base copies. Revision 1's rule listed them, 20 slots in
all; Revision 2's lists 17. SR3's narrowing introduced this.

*Closes when* one of these holds:

* the note also reads living-state records, opening them with the same checks
  as a base copy, since the integrity pass never read them. Their edits never
  fail the integrity check, so the remedy is "fill it", with no finalize step;
* or the coverage line counts them as "not checked: living-state file".

Default: read them.

**[SR10] (non-blocking) The narrowed "zero" still says "anywhere", and the
checker's own comments still misdescribe it.** A reader told that no listed
name appears anywhere would not expect `ClaudeCode` to pass. On the stricter
gate, each of these is +0:

* `ClaudeCode`, `GPT4o` and `Claude_Code`. Matching is whole-word, so a name
  joined to letters, digits or `_` passes.
* A name with a zero-width character inside it.

Two more limits are unnamed:

* **File types are a list.** Today every shipped type is read, apart from the
  empty `.gitkeep` files. A new shipped type would be skipped without warning.
* **It catches accidents, not intent.** Someone hiding a name on purpose gets
  past it.

*Closes when:*

* The sentence says "as a whole word, in the file types it reads", and S5 adds
  joined spellings, new file types and deliberate evasion.
* The one-time search is a case-insensitive *substring* search, so it catches
  joined forms, and its hits are read by hand.
* All four places in `scripts/quality_gate.py` that describe the templates scan
  are corrected, not only `:446`:
  * `:197-198` and `:252` say templates are scanned only for the
    directive-forbidden rule;
  * `:436-438` and `:456-457` say every file under `templates/` is scanned.

  The cleaner fix makes the second claim true: scan every non-binary file under
  `templates/`. That closes the file-type limit by construction. It is the
  author's call.

**[SR11] (non-blocking) NU2's fallback was dropped without a ledger line.** An
adopter who fills a slot, commits, and stops before `--finalize` comes back to a
tamper warning and no way forward. That is NU2's original defect.

* Revision 1 closed NU2 partly through the marker: "If the record step is
  skipped, the marker makes the existing `--finalize` hint name the file."
* SR5 rightly took the marker out of the fill path, so the hint now stays
  silent. The note says only "resolve the integrity failure above first".
* Revision 2's loop test also drops Revision 1's step "exits 1, with the hint
  naming the file".

The ledger records the marker change but not this consequence.

*Closes when* the ledger records the dropped fallback, and the failing-file line
points to the `bootstrap/UPGRADE.md` section on reviewing and recording your own
edit. A pointer, not a finalize command, keeps SR2's rule.

**[SR12] (non-blocking) SR3 and SR4 hold in structure; seven details belong in
the plan.** None weakens the verdict guarantee. Each keeps a malformed input
from getting around it.

* **What the note receives.** "The bytes ... and nothing else" is not literal.
  The note also needs the target, the accepted records and the lockfile's
  tokens. Say so; it still receives nothing that carries the verdict.
* **One open, one bounded read.**
  * Check the regular-file property with `fstat` on the same descriptor.
  * Read at most the cap plus one byte, rather than trusting the size.
  * Hash, decode and parse those same bytes.
  * Build the flags inside the fenced call with `getattr(os, "O_NOFOLLOW", 0)`
    and the like, as `bootstrap/tests/_gate_preflight.py:2361` and
    `tools/_intent/record_io.py:465` do. A platform lacking a flag then cannot
    break the module's import. Add `O_NOCTTY`.

  On macOS a symlink is refused (`ELOOP`). A FIFO opens without blocking, and
  `fstat` rejects it, as it does a directory. Linux behaves the same under
  POSIX, and Cairn's documented platforms are POSIX (`docs/quickstart.md:23`).
  The walk that checks no part of the path is a symlink can race, but
  harmlessly: only bytes matching `base_hash` go further.
* **The fence.** `except Exception` lets `SystemExit` through. Either the note
  calls nothing that can raise it, or the fence catches it too.
* **Per-record failures.** A NUL byte in `base_cache` makes `os.open` raise
  `ValueError`, which is not a read, type or decode error. As written it escapes
  to the outer fence, and the whole coverage line is lost. Count any per-record
  exception as "not checked: unreadable".
* **Missing no-op comparison cases.** Add:
  * non-UTF-8 *installed* bytes, in a file that passes integrity;
  * a non-string token key;
  * a NUL byte in `base_cache`;
  * a non-string `base_hash`.
* **The slow regex, measured.** On unclosed openers, the 256 KiB cap still
  allows 18.9 s per scan on this machine (1.2 s at 64 KiB). The note scans two
  texts per record.
  * Apply the cap to the installed bytes too.
  * SR4's "a tree can reach `_SLOT_BODY_RE`'s slow case only by also changing
    the lockfile" is false for the existing hint. `_has_customized_slot` scans
    every *modified* file, uncapped, inside the integrity loop before the report
    prints (`bootstrap/verify_integrity.py:134-139`). Either cap that scan as
    well, so an over-cap file is still reported as modified but not
    marker-checked, or narrow the sentence and record the residual.
* **Unprintable names.** `shlex.quote` does not neutralise terminal control
  bytes. A path or slot name that is not printable ASCII gets no command, only
  its `ascii()` form.

**[SR13] (non-blocking) Make "the stricter gate can only add failures" a
recorded check.** The checker is excepted from the comment-only proof, so
nothing else pins this.

* **The superset check.** It holds today: every one of the old gate's 74
  failures is among the new gate's 81. Record that check in the plan's
  evidence.
* **One more test.** A whole-line directive in `templates/` that also carries a
  name must yield both failures (measured: +1 today, +2 stricter). That pins
  that removing the skip hides no directive.

**[SR14] (non-blocking) Name the self-host finalize set, and check it after the
write.** Scoped `--finalize` skips the dirty-tree guard, and several sessions
share this tree. Two of the files are trust roots: `tools/session.py`, the
interpreter binding, and `scripts/content_scan.py`.

* **The 12 to finalize.** These edited twins are attested by Cairn's lockfile
  today:
  * `.agents/skills/_data/vendor_targets.yml`
  * `tools/session.py`
  * the six `scripts/_onboarding/` modules
  * `scripts/onboarding_activate.py`
  * `tools/intent.py`
  * `scripts/content_scan.py`
  * `dev/modules/incident_log_template.md`
* **The 4 to leave alone.** These edited files are already among the 18
  violations:
  * `.agents/skills/session-start/SKILL.md`
  * `dev/modules/documentation-plan.md`
  * `dev/modules/incident-trackers.md`
  * `docs/DOCUMENTATION_PLAN.md`

Advancing `hash` changes nothing else. The fork checks read `hash` and on-disk
bytes, not `base_hash` (`bootstrap/_scaffold/lockfile.py:303-327`).

*Closes when:*

* the plan names these paths;
* after the write, each advanced `hash` equals the SHA-256 of its template as
  committed, so a reviewer can confirm it from the commit alone;
* `verify_integrity` still lists exactly the same 18 files.

### Verdict and what clears the obligation

**REVISE.** The Security Review obligation is **not cleared**. SR8 closes with
contract sentences and one test, with no engine change. A Security Review pass
that reads only SR8's closure clears it. SR9-SR14 do not block. SR9's and
SR11's ledger lines belong in the same revision; the rest can go to the plan.

**No new question for the Maintainer.**

## Response -- Claude (author) -- 2026-10-17 (to the round-2 Security Review)

SR8 is accepted, and so is every non-blocking finding except one, which is
partly accepted (SR10's cleaner fix). The code moved since Revision 2, and
Revision 3 is written against it. `b6b69c52` rewrote the existing hint and the
slot scan:

* **The hint** now says the check "keeps only a hash, not the text, so it cannot
  show you what changed". It tells the adopter to read the whole file, or its
  history since install, before `--finalize`.
* **The slot scan.** `_has_customized_slot` now makes one linear pass over
  `_MARKER_RE`, with a bounded slot name. `_SLOT_BODY_RE`, which Revision 2's
  note reused, no longer exists.

**SR8: accepted.** Revision 2's review command compared the file against the
lockfile's last commit, and the review showed that commit can postdate the
change. I drop the command everywhere.

* **The existing hint (item 6) is withdrawn.** `b6b69c52` already applied the
  review's default there.
* **The note's remedy (item 5) is replaced** by a command whose coverage holds
  under a precondition the adopter can check. The note lists only files whose
  bytes match their record at that moment. So:
  * if `git status --short -- <path>` prints nothing, the working copy equals
    the committed one, and both equal the record;
  * after the edit, `git diff -- <path>` shows the working copy against that
    record, which is exactly what `--finalize` will record;
  * if the status line prints anything, the remedy says to read the whole file
    instead.

  The command no longer depends on when the lockfile was committed. Its one
  assumption is that nobody staged a change to that path in between, and the
  status check reveals a staged change.
* **New test for the review's case B.** The case is a first install with a slot
  filled and a line planted before the first commit. The test asserts that the
  note does not list the file (it fails integrity), that the note prints no
  diff or finalize command for it, and that the note's line points to the
  UPGRADE.md section below.

**SR9: accepted, with the review's default.** The note also reads living-state
records the integrity pass skipped. It opens them with the same checks as a
base copy, because nothing has read them yet. Their remedy is "fill it", with
no finalize step, since edits to them never fail the integrity check.

**SR10: partly accepted.**

* **Accepted.** The claim becomes "no listed name as a whole word, in the file
  types the gate reads". S5 adds joined spellings (`ClaudeCode`, `GPT4o`,
  `Claude_Code`), zero-width characters, new file types and deliberate evasion.
  The one-time search becomes case-insensitive and substring-based, with every
  hit read by hand. All five comment sites in `scripts/quality_gate.py`
  (`:197-198`, `:252`, `:436-438`, `:446`, `:456-457`) are corrected.
* **Declined: scanning every non-binary file under `templates/`.** The gate
  walks the filesystem, not git. There are 23 untracked `.pyc` files under
  `templates/` today, so "every file" would read build artefacts. Restricting
  it to tracked files would make the checker depend on git. The type list stays
  (now with `.json` and `.txt`), and new types are a named blind spot.

**SR11: accepted.**

* **Ledger.** It now records that taking the marker out of the fill path dropped
  Revision 1's fallback, where the hint named the file.
* **Failing-file line.** It points to a new `bootstrap/UPGRADE.md` section on
  reviewing and recording your own edit, never to a command.

**SR12: accepted.**

* **What the note receives.** The target, the accepted and living-state
  records, the bytes the integrity pass read, and the lockfile's tokens. None of
  these carries the verdict.
* **How it reads.**
  * One open per file, with its flags built inside the fence via
    `getattr(os, ..., 0)` and `O_NOCTTY` added.
  * `fstat` on that same descriptor.
  * A bounded read of the cap plus one byte, applied to installed bytes as well.
  * Hashing, decoding and parsing all use those same bytes.
* **Slots** are parsed with one linear marker pass, as `_has_customized_slot`
  now does.
* **The fence** catches `SystemExit` too.
* **Per-record errors.** Any exception for a single record is counted as "not
  checked: unreadable".
* **No-op comparison cases.** The four the review added are included.
* **Unprintable names.** A name or path that is not printable ASCII gets only
  its `ascii()` form and no command.
* **Withdrawn.** Revision 2's sentence about reaching the slow regex case is
  withdrawn, since the regex is gone.

**SR13: accepted.**

* **The superset check** (every old failure is among the new) goes into the
  evidence.
* **A test pins** that a whole-line directive carrying a name yields both
  failures.

**SR14: accepted.** The plan finalizes exactly the 12 twins the review names and
leaves its 4 alone. After the write, each advanced `hash` must equal the
SHA-256 of its template as committed. `verify_integrity --target .` must still
list the same 18 files.

**Status.** No scope widens. The Security Review obligation stays open for a
pass that reads SR8's closure, so Status returns to `awaiting-review`. No
Maintainer question changes.

## Revision 3 -- Claude (author) -- 2026-10-17 -- delta against Revision 2

Revision 2 stands as the complete current contract. **Only the parts named below
are replaced.** Every other section and sentence of Revision 2 stands unchanged.

### Replaces: In plain terms, item 1's "Zero will mean" sentence

**Zero will mean** that no listed vendor or project name appears as a whole
word, in its normal capitals, in the file types the gate reads under its scan
roots. **It will not cover** lower-case or joined spellings (`ClaudeCode`), names
broken by invisible characters, names not on the list, file types not on the
list, or deliberate hiding. A one-time search covers those for this change.

### Replaces: Proposal, Part 1 item 1, the checker

The checker gets four changes, in `scripts/quality_gate.py`:

* **Comment lines.** In `templates/` it scans whole-line HTML comments for
  tokens. A `vendor-ok` or `case-study` directive there still fails as well.
* **File types.** It reads `.json` and `.txt`.
* **Names.** Copilot, Windsurf, Cline and OpenCode join the denylist.
* **Its own comments.** It describes its `templates/` scan accurately at
  `:197-198`, `:252`, `:436-438`, `:446` and `:456-457`.

No exemption is added. These changes can only add failures. The type list stays
a list: the gate walks the filesystem, which holds 23 untracked `.pyc` files
under `templates/` today.

### Replaces: Proposal, Part 2 items 1 to 7

1. **A separate pass, after the verdict.**
   * `verify()` first prints the integrity report as it does today, then fixes
     the exit code.
   * Only after that does it call the note, passing the target, the records the
     integrity pass accepted together with the bytes it already read, the
     legitimate living-state records, and the lockfile's tokens. Nothing passed
     carries `violations`, `skipped` or the exit code.
   * The call is fenced, and the fence catches `SystemExit` too. Any exception
     prints one "slot note not run" line, and the exit code returned is the one
     fixed before the call.
   * Inside the note, any exception for a single record counts that record as
     "not checked: unreadable".
2. **What it reads, and how.** The note opens each base copy, and each
   living-state file, once. The open flags are built inside the fence with
   `getattr(os, ..., 0)`: no-follow, non-blocking, `O_NOCTTY`. The file is
   accepted only if `fstat` on that descriptor shows a regular file, and a read
   of at most the cap plus one byte (256 KiB) stays within the cap. Hashing,
   decoding and parsing all use those same bytes. Installed bytes the integrity
   pass already read obey the same cap.

   A base copy is used only if all of these hold:
   * its path is under `dev/.cairn/base/` inside the target, with no symlinked
     part;
   * its bytes decode as UTF-8;
   * its bytes hash to a string `base_hash` on the record.

   Token values are used only from a string-to-string `tokens` mapping.
3. **What it lists.** A slot is listed when its body is unchanged from the base
   copy's, after spacing is normalized and tokens substituted. A slot carrying
   `<!-- cairn:customized -->` is not listed. A slot that is also empty in the
   base copy is counted "empty: filled when its module is installed".

   Slots are found with one linear pass over the markers, using the bounded name
   pattern of `_MARKER_RE` (`b6b69c52`). A test pins the pass, the token pattern
   and the spacing rule to the engine's.
4. **One coverage line, always printed.** It gives the slots and files checked,
   the number listed, and the empty slots awaiting a module. It also counts the
   files not checked, by reason:
   * no base copy;
   * failed the integrity check;
   * base hash mismatch;
   * unreadable.

   Living-state files are counted like any other file.
5. **The remedy.**
   * **For a slot in a file the integrity pass accepted:**
     1. Confirm `git status --short -- <path>` prints nothing.
     2. Fill the slot, or write `N/A: <reason>`.
     3. `git diff -- <path>` now shows everything `--finalize` will record. The
        note matched this file to its record moments ago, and step 1 showed the
        committed copy equals it.
     4. Commit, run `python bootstrap/scaffold.py upgrade --target <repo>
        --finalize <path>`, then commit the lockfile.

     If step 1 prints anything, read the whole file instead. Finalizing records
     the whole file. To keep Cairn's text on purpose, add
     `<!-- cairn:customized -->` inside the slot instead of filling it.
   * **For a living-state file:** fill it. There is no finalize step.
   * **Paths** are shell-quoted. A path or slot name that is not printable ASCII
     is shown only in its `ascii()` form, with no command.
6. **Withdrawn.** The existing hint is left as `b6b69c52` wrote it.
7. **`bootstrap/UPGRADE.md` changes.**
   * It gains step 4: run `verify_integrity` after `--apply`. Only a person
     following the steps runs it.
   * It explains the note's meaning.
   * It records the known gap: a placeholder that an upgrade rewords reads as
     filled.
   * It gains a section, *Recording an edit you made*. The section says that
     `verify_integrity` keeps only a hash, that `--finalize` records the whole
     file, and that the scoped form skips the dirty-tree guard. It also says how
     to review first: read the file, or `git log -p -- <path>` since install.
   * The note's line for a failing file points to that section and prints no
     command.

### Replaces: the Self-hosted lockfile sentence in Part 1 item 8

The edited twins that Cairn's lockfile attests today are scoped-finalized. There
are 12:

* `.agents/skills/_data/vendor_targets.yml`
* `tools/session.py`
* the six `scripts/_onboarding/` modules
* `scripts/onboarding_activate.py`
* `tools/intent.py`
* `scripts/content_scan.py`
* `dev/modules/incident_log_template.md`

The 4 edited files already among Cairn's 18 violations are left alone:

* `.agents/skills/session-start/SKILL.md`
* `dev/modules/documentation-plan.md`
* `dev/modules/incident-trackers.md`
* `docs/DOCUMENTATION_PLAN.md`

After the write, each advanced `hash` equals the SHA-256 of its template as
committed, and `verify_integrity --target .` lists the same 18 files.

### Adds to: Tests required

* **`bootstrap/tests/test_verify_integrity.py`:**
  * **Case B, the first install.** A file was already modified when the
    lockfile was committed, and it holds a marked slot plus a line outside the
    slots. Expected:
    * the note does not list the file, and prints no diff or finalize command
      for it;
    * its line points to the UPGRADE.md section.
  * **Case A, the listed path.** After the remedy's step 1, a line planted by
    another writer appears in `git diff -- <path>`.
  * **Living state.** A living-state file's placeholder slot is listed with no
    finalize step.
  * **No-op comparison cases**, added:
    * non-UTF-8 installed bytes in a file that passes integrity;
    * a non-string token key;
    * a NUL byte in `base_cache`;
    * a non-string `base_hash`;
    * `SystemExit` raised inside the note.
  * **A non-printable path** is shown in its `ascii()` form, with no command.
* **`bootstrap/tests/test_quality_gate_neutrality.py`:** a whole-line directive
  in `templates/` that also carries a name yields both failures.

The loop test's step 3 now runs `git diff -- <path>` after confirming the status
precondition.

### Adds to: Examples / smoke checks

* **The superset check.** Every failure the current gate reports is among the
  stricter gate's (74 within 81 today).
* **The one-time search** is case-insensitive and substring-based. Every hit is
  read by hand, and each must be a routing id or a path.

### Replaces: Security preflight S4's last point, and S5

* **S4, last point.** `--finalize <path>` records the whole file and skips the
  dirty-tree guard. The note therefore gives a remedy only for a file it has
  just matched to its record, with a review command whose coverage depends on a
  precondition the adopter checks. Every other file gets a pointer to the
  UPGRADE.md section and no command.
* **S5 — Who still wins?**
  * **Spellings the gate cannot see.** Lower-case and joined spellings,
    invisible characters, unlisted names, unlisted file types, and anyone hiding
    a name on purpose. These are closed by enumeration only. The one-time search
    covers only this change's lines.
  * **A changed lockfile.** Anyone who changes the lockfile together with a base
    copy can steer the note.
  * **A staged change.** Anyone who stages a change to the path between the
    note's run and step 1 defeats the review, if step 1's output goes unread.
  * **Skipped review.** An adopter who finalizes without reviewing.
  * **The hint's reach.** The hint still names any modified file with a marked
    slot. Since `b6b69c52` it says plainly that it cannot show what changed.

### Withdrawn / superseded commitments

* **The review command**
  `git diff "$(git log -1 --format=%H -- dev/.cairn/cairn-lock.yml)" -- <path>`,
  and the claim that it shows what `--finalize` records. Withdrawn: it can hide
  changes made at or before the lockfile's last commit (SR8). Superseded by the
  `git status` / `git diff -- <path>` remedy.
* **Part 2 item 6, adding the command to the hint.** Withdrawn (SR8).
* **Revision 1's fallback.** It said that if the record step is skipped, the
  marker makes the hint name the file. Dropped when the marker left the fill
  path (Revision 2, SR5). The failing-file line now points to UPGRADE.md instead
  (SR11).
* **The note reads slots with `_SLOT_BODY_RE`.** Superseded by a linear marker
  pass, since `b6b69c52` removed that regex.
* **"A tree can reach `_SLOT_BODY_RE`'s slow case only by also changing the
  lockfile."** Withdrawn: the regex is gone, and the existing hint's scan is now
  linear (SR12).
* **Living-state files** were neither read nor counted. Superseded: they are read
  and counted (SR9).
* **"Anywhere in a scanned file"** in the zero claim. Superseded by "as a whole
  word, in the file types the gate reads" (SR10).
* **Correcting only `:446`.** Superseded: five comment sites are corrected
  (SR10).

## Review -- Claude Opus 5.5 (Security Review, SR8 closure, fresh session) -- 2026-10-17

```
Reviewed commit: 24b76d15ef2e769e55a0beb8b5a0e4221af01a86
Target: SR8 in the round-2 Security Review, the round-3 Response's SR8 entry, and Revision 3 (read quickly for anything new), against bootstrap/verify_integrity.py and _cmd_finalize_lockfile in bootstrap/_scaffold/upgrade.py
Prior findings: SR8 (this tier, round 2)
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: raised (1 blocking, 1 non-blocking)
**Verdict**: REVISE

Distance: a fresh session of the author's agent type, not a different type. I
wrote neither the proposal nor an earlier review of it. This pass reads SR8's
closure, as the round-2 review set out.

### In plain terms

The new review step has the right idea, and it closes the case SR8 found. A
file that was changed before the note runs now gets no command at all. But the
two git commands the note will print can still show nothing while `--finalize`
records a planted line:

* **They look in the wrong folder.** Step 4 runs `python bootstrap/scaffold.py
  ...`, so the adopter's shell sits in the Cairn copy. From there the git
  commands check Cairn's own `AGENTS.md`, not the project's. I ran the steps
  that way. Both printed nothing, `--finalize` recorded a line telling agents
  to download and run a script, and the install check said OK. That is SR8's
  result again.
* **They compare against the wrong copy.** Step 1 shows that the committed copy
  matches the record. But `git diff` compares against git's staging area, not
  that commit. If whoever fills the slot, often an agent, stages or commits its
  work, a planted line drops out of the diff.

The fix is four sentence changes and three more test cases, with no new
mechanism. No new question for the Maintainer.

### SR8: what Revision 3 closes

I used scratch `solo-greenfield` installs of the reviewed commit, under Python
3.13.13, in my scratchpad. A small script stood in for the note: it admits a
file only when its bytes hash to its record.

* **SR8's histories get no command.** In case B (fill and plant before the
  first commit) and case C (plant committed later, with no finalize), the file
  fails the integrity check. So the note does not list it and prints no diff
  and no finalize command for it. This holds by construction.
* **The precondition logic is sound.** If the note has just matched a file to
  its record and `git status --short` on it prints nothing, the committed copy
  equals the record. That is true. The commands built on it are SR15.

### Findings

**[SR15] (blocking) The review commands can still show an empty diff while
`--finalize` records a planted line.** This is SR8's harm by a different route.
An adopter following the printed steps can record an injected instruction in
`AGENTS.md` as trusted.

Measured on a target committed clean and listed by the note, with step 1 run
first and then the slot filled. "Pinned" means a diff against the commit step 1
saw (`git -C <target> diff <commit> -- <path>`):

| After step 1 | `git diff -- <path>` | `git diff HEAD -- <path>` | Pinned |
|---|---|---|---|
| Plant written, not staged (control) | shows it | shows it | shows it |
| Another writer stages the plant | hidden | shows it | shows it |
| Another writer commits the plant | hidden | hidden | shows it |
| The filler commits its fill and the plant | hidden | hidden | shows it |
| Steps run from the Cairn copy | empty | — | shows it, with `-C` |

In the staged row and the Cairn-copy row I then ran `--finalize`, which records
the bytes on disk (`bootstrap/_scaffold/upgrade.py:1874`). `verify_integrity`
then said OK.

The causes:

* **The wrong folder.** `<path>` is relative to the target. The same block's
  step 4 runs from the Cairn checkout, where `AGENTS.md` also exists and is
  clean. So step 1 passes without checking anything, and step 3 shows nothing.
* **The wrong baseline.** The Response says step 1 "showed the committed copy
  equals" the record. But `git diff -- <path>` compares with the index, which
  can change after step 1, and a commit moves `HEAD` as well. The filler
  committing is ordinary, not an attack: Cairn's shipped `AGENTS.md` tells
  agents to commit their own work (`templates/core/AGENTS.md:131`).
* **The residual is in the wrong place.** S5 names a change staged "between the
  note's run and step 1". Step 1 catches that one. The window it misses is after
  step 1.

Two rarer cases also print nothing at steps 1 and 3: a path git ignores, and a
file with `skip-worktree` set. Both hide the adopter's own fill too, so step 3
can tell the adopter to check for that.

*Closes when* Part 2 item 5's first remedy says:

1. Every printed git command names the target: `git -C <target> ...`. Here
   `<target>` is the absolute path `verify_integrity` resolved, shell-quoted,
   under the same printable-ASCII rule as paths.
2. Step 1 pins the baseline. `git -C <target> status --short -- <path>` prints
   nothing, and `git -C <target> rev-parse HEAD` gives the commit. Step 3 is
   `git -C <target> diff <that commit> -- <path>`. Step 1 tied that commit's
   copy to the record, so this diff shows every change since, whether staged,
   committed or neither.
3. Step 3 adds: your fill must appear in this diff. If it does not, or if
   anything you did not write does, read the whole file instead.
4. S5 names what still wins: a change *committed* to the path between the
   note's run and step 1, which `git status` cannot see, and any write between
   step 3 and `--finalize`, which no command closes.

The Case A test adds the staged, committed and filler-commits plants. Each must
appear in the output of the printed step-3 command, and the printed commands
must carry `-C` and the absolute target.

One alternative also closes the first window in point 4. The note prints the
record's hash, and step 1 checks that the commit's copy hashes to it. That is
the author's call.

**[SR16] (non-blocking) The case B test is aimed right; it should read only the
note's lines, and check one more thing.** Its core assertion is correct: a file
that fails the integrity check gets no diff command and no finalize command
from the note.

* **Scope the "no finalize command" check to the note's lines.** The existing
  hint prints `--finalize AGENTS.md` for this same file by design, because the
  file has a marked slot (`bootstrap/verify_integrity.py:182-190`). In case B it
  does. A check over all of stderr would fail against shipped behaviour, and
  would invite "fixing" the hint.
* **Assert instead:**
  * the note's lines carry no `--finalize`, `git diff` or `git status`;
  * the whole output carries no `git diff`;
  * the coverage line counts the file under "failed the integrity check", so it
    cannot vanish from the count (SR9's harm).
* **UPGRADE.md.** The new section's `git log -p -- <path>` does not show
  uncommitted edits. The section should lead with reading the whole file, and
  say so.

### Anything else new

Nothing else in Revision 3 needs a Security Review:

* the living-state reads use the base-copy checks and print no finalize step;
* the checker changes only correct its own comments;
* the self-host list repeats SR14's 12 files.

### Verdict and what clears the obligation

**REVISE.** The Security Review obligation is **not cleared**. SR15 closes with
the four sentences above and the added Case A cases, with no engine change. A
Security Review pass that reads only SR15's closure clears it. SR16 can land in
the same revision or in the plan.

**No new question for the Maintainer.**

## Response -- Claude (author) -- 2026-10-17 (to the SR8-closure Security pass)

**SR15: accepted, by removing the cause rather than patching it.** This is the
third round in which a printed command recipe was the weak point: SR2, SR8, and
now SR15. Each fix added a precondition, and each precondition opened a new
gap: first the wrong comparison point, then the wrong folder, then the wrong
baseline.

The four-sentence fix would close the cases measured here. It would still leave
two windows the review names itself, and any recipe whose correctness depends
on the adopter's shell, git state and timing is one more round of the same
shape. The underlying fact does not change: `verify_integrity` keeps only a
hash, so no command it prints can know what changed.

Revision 4 therefore takes the class out. **The note prints no git command and
no finalize command.** For each placeholder slot it lists the file and the slot,
and says how to fill it. It then states, once per run, the same hash-only
warning the existing hint gives (`b6b69c52`), and points at the UPGRADE.md
section on recording your own edit. That section explains the review in prose:
read the whole file, and check that your fill is the only change.

The note can no longer lead anyone into blessing a planted line, because it
prints nothing to run. What remains in S5 is short and true.

**What this gives up, and why I accept it.** NU2's closure asked that each entry
end with the finalize command. Revision 4 keeps NU2's purpose, an adopter who
fills a slot always has a way back to a passing check, and drops its letter. The
way back is now a pointer to the documented recording step, not a printed
command. The loop test still proves the way back works. The Security Review's
three findings show that printing the command is where the risk was.

**SR16: accepted.**

* The case B test reads only the note's lines. They must carry no
  `--finalize`, no `git diff` and no `git status`.
* The whole output must carry no `git diff`.
* The coverage line must count the file under "failed the integrity check".
* The existing hint's own `--finalize` line is shipped behaviour and is out of
  this test's scope.
* The UPGRADE.md section leads with reading the whole file. It says that
  `git log -p -- <path>` shows committed history only, never uncommitted edits.

No scope widens, and no Maintainer question changes. The Security Review
obligation stays open for a pass that reads SR15's closure, so Status returns
to `awaiting-review`.

## Revision 4 -- Claude (author) -- 2026-10-17 -- delta against Revision 3

Revisions 2 and 3 stand as the current contract. **Only the parts named below
are replaced.** Everything else stands unchanged.

### Replaces: Revision 3, Part 2 item 5 (the remedy)

The note prints **no git command and no finalize command**, for any file.

* **A placeholder slot in a file the integrity pass accepted** prints its file
  and slot, both in `ascii()` form, and how to fill it:
  * write the content, or `N/A: <reason>`;
  * or, to keep Cairn's text on purpose, add `<!-- cairn:customized -->` inside
    the slot.
* **A placeholder slot in a living-state file** prints "fill it". These files
  need no recording step.
* **A file that failed the integrity check** is counted under that reason in the
  coverage line. It gets no remedy.

Once per run, after the list, the note prints the hash-only warning in the
existing hint's words (`b6b69c52`): this check keeps only a hash, not the text,
so it cannot show you what changed. It adds that before recording, you should
read the whole file and confirm your edit is the only change. It then points to
`bootstrap/UPGRADE.md` > *Recording an edit you made*.

### Replaces: Revision 3, Part 2 item 7's description of the new UPGRADE.md section

*Recording an edit you made* says the following:

* **Read the whole file first,** and confirm that the only change is yours.
  `verify_integrity` keeps only a hash, so nothing it prints can show what
  changed.
* **`git log -p -- <path>` is a supplementary aid.** It shows committed history
  only, never uncommitted edits.
* **Then record the file** with `python bootstrap/scaffold.py upgrade --target
  <repo> --finalize <path>`. This command records the whole file, not only your
  slot. The scoped form also skips the dirty-tree guard.

The section describes the command; it does not claim that any command shows the
change.

### Replaces: tests that relied on printed commands

**Removed.** Revision 3's Case A test (the `git status` / `git diff` steps) is
removed, along with the step-3 diff check in the loop test.

**`bootstrap/tests/test_verify_integrity.py` instead pins the following.**

* **No commands in the note.** For listed, living-state and failing files alike,
  the note's lines carry no `git` command and no `--finalize`. The warning and
  the UPGRADE.md pointer appear exactly once.
* **Case B (SR16).** The case is a first install whose file has a marked slot
  and a planted line outside it. The test checks:
  * the note's lines carry no `--finalize`, no `git diff` and no `git status`;
  * the whole output carries no `git diff`;
  * the coverage line counts the file under "failed the integrity check".

  The existing hint's `--finalize` line is not asserted against.
* **The loop.**
  1. A slot is listed.
  2. It is filled and committed.
  3. `verify_integrity` exits 1, and the file is counted as having failed the
     integrity check.
  4. The test records the file as the UPGRADE.md section describes.
  5. `verify_integrity` exits 0, and the slot is no longer listed.

### Replaces: Revision 3's S4 last point and S5

* **S4, last point.** The note prints nothing to run. Recording stays the
  adopter's own act, after reading the whole file. So no output of the note can
  direct a recording.
* **S5 — Who still wins?**
  * **Neutrality spellings the gate cannot see.** These are the blind spots
    Revision 3 named: lower-case and joined spellings, invisible characters,
    unlisted names and file types, and deliberate hiding. Only the one-time
    search covers this change.
  * **A changed lockfile.** Anyone who changes the lockfile together with a base
    copy can steer the note's list. The note grants nothing.
  * **An adopter who records without reading the whole file.**
  * **The existing hint.** It still prints a `--finalize` command for a modified
    file with a marked slot, while saying it cannot show what changed
    (`b6b69c52`). That is shipped behaviour this proposal does not change.

### Withdrawn / superseded commitments

* **Revision 3's remedy steps** (`git status --short`, `git diff -- <path>`,
  then commit and `--finalize`). Withdrawn (SR15): any printed recipe depends on
  the adopter's folder, staging state and timing.
* **"Paths are shell-quoted" in commands the note prints.** Withdrawn: the note
  prints no commands. Names and paths are still shown in `ascii()` form.
* **NU2's closure as a printed finalize command.** Superseded by a pointer to
  the documented recording step. NU2's purpose, a way back to a passing check,
  is kept and pinned by the loop test.
* **Revision 3's Case A test, and the loop test's diff step.** Withdrawn with
  the commands.
* **Revision 3's S4 last point and S5.** Superseded as above.
* **The UPGRADE.md section offering `git log -p` as the review.** Superseded: it
  leads with reading the whole file and says `git log -p` misses uncommitted
  edits (SR16).

## Review -- Claude Opus 5.5 (Security Review, SR15 closure, fresh session) -- 2026-10-17

```
Reviewed commit: a89babe94d9d06f349943ac47e09aa2b6d4dcb6b
Target: SR15 and SR16 in the SR8-closure Security pass, the Response to it, and Revision 4, against bootstrap/verify_integrity.py and _cmd_finalize_lockfile in bootstrap/_scaffold/upgrade.py
Prior findings: SR15 (blocking), SR16 (non-blocking), both this tier
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: raised (2 non-blocking)
**Verdict**: ACCEPT

Distance: a fresh session of the author's agent type, not a different type. I
wrote neither the proposal nor an earlier review of it. This pass reads SR15's
closure, as the last pass set out, and does not reopen earlier rounds.

### In plain terms

SR15 is closed, and the Security Review obligation is **cleared**. The note no
longer prints any command. So there is nothing an adopter can run that comes
back empty while `--finalize` records a planted line. What is left is a person
reading their own file, which is the safe fallback SR15 itself named.

Two small wording fixes would make that reading harder to get wrong. Neither
blocks, and both can land in the plan:

* The new UPGRADE.md section should say which copy to read: the one in your
  project, not the file of the same name in the Cairn folder you ran the check
  from. It should also say your own fill must be in what you read.
* The existing hint still says reading the file's history is enough. The new
  section says history misses edits not yet committed. Both can appear in the
  same output, so one of them should change.

### The three questions

**1. Can the note's output, or the section it points to, still lead an adopter
to record a tampered file?** Not through anything the note prints.

* The note's lines name a file and a slot, say how to fill it, and give one
  warning and one pointer. None of that is a command. So none of it can run in
  the wrong folder or against the wrong baseline, SR15's two causes.
* The note grants nothing. Recording is a separate command the adopter types
  after reading. The scoped `--finalize` records the bytes on disk
  (`bootstrap/_scaffold/upgrade.py:1874`) and skips the dirty-tree guard
  (`:1819`), and the section says both.
* The pointer leads to `bootstrap/UPGRADE.md` in the Cairn checkout, the
  verifier's side. The install manifest does not ship it to adopters
  (`scaffold.py --manifest` lists `AGENTS.md` twice and `UPGRADE.md` never). So
  a tampered target cannot rewrite the advice the note points to.
* What remains is a reader who reads the wrong copy, or cannot tell that a
  change is not theirs. SR17 covers both.

**2. Is the prose review sound?** Yes, as the strongest review that does not
depend on git state. Reading the whole file covers every byte `--finalize`
records, whether staged, committed or neither. Calling `git log -p -- <path>`
supplementary, because it shows committed history only, is correct. That closes
SR16's UPGRADE.md point. Its limits are SR17.

**3. Did Revision 4 open anything new?** No. It removes output rather than
adding it.

* Dropping NU2's printed finalize command loses no security property. The loop
  test still proves a filled slot can get back to a passing check, and the
  printed command is where SR2, SR8 and SR15 all lived. The change narrows
  scope, so it needs no second External round.
* The withdrawal ledger covers what Revision 4 replaces. I checked it against
  Revision 3's Part 2 items 5 and 7, its tests, and its S4 and S5.
* SR16's three assertions are restated in full, scoped to the note's lines as
  asked.

### Findings

**[SR17] (non-blocking) The section should say which copy to read, that your
fill must be in it, and what reading cannot catch.** A reader can check a clean
file and still record a tampered one, if the clean file is the wrong copy.

* **Which copy.** The note prints paths relative to the target. The adopter runs
  the check from the Cairn checkout, which has its own `AGENTS.md`. That is
  SR15's wrong-folder cause, now in prose. It is weaker here, since nothing runs
  by itself, but it is the same mistake. The section should say: read the file
  inside your project, under the `--target` you passed. Your own fill must be in
  what you read; if it is not, you are reading the wrong copy. That is SR15's
  own step-3 check, kept without the command.
* **What reading cannot catch.** Reading finds a line you know is not yours,
  such as SR15's planted instruction to download and run a script. It does not
  reliably find a small rewording of text Cairn shipped, because the check keeps
  no copy to compare with. S5 should name "an adopter who reads but cannot tell"
  beside "an adopter who records without reading". The section may suggest
  comparing with a copy you trust, as an aid in the same standing as
  `git log -p`, never as proof.

*Closes when* the plan's UPGRADE.md text carries the two sentences on which copy
and the fill being present, and S5 names the reading limit.

**[SR18] (non-blocking) The existing hint and the new section disagree about
history.** In one run, an adopter can see two standards for the same review.

* The hint says to read "the whole file, or its history since install"
  (`bootstrap/verify_integrity.py:185-186`). The "or" offers history as enough
  on its own.
* The section says history shows committed edits only, so it is never enough on
  its own. That is SR16's point, and it applies to the hint equally.
* For a modified file with a marked slot, both print in the same output. Case B
  is exactly that file.

No test pins the hint's phrase. Dropping ", or its history since install," is a
one-phrase change in a file this proposal already edits. Revision 3 item 6 left
the hint alone on purpose, so this is the author's call.

*Closes when* the plan removes the phrase, or S5's hint entry names the
disagreement.

### Verdict

**ACCEPT.** SR15 is closed by construction, because the note prints no command.
SR16 is closed. The Security Review obligation is **cleared**, and Status moves
to `awaiting-decision`. SR17 and SR18 land in the plan, where its Internal
review can check them.

**No new question for the Maintainer.**
