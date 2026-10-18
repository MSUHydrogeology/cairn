# Two checks you can trust: a neutrality gate that reads zero, and a note for slots an upgrade adds

**Author**: Claude (Strategy)
**Status**: revising
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
