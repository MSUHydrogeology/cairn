# Make the next-session handoff a local note

**Author**: Claude Sonnet 5.5 (Strategy; model id `claude-sonnet-5-5`)
**Status**: revising
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review) — the plan edits `bootstrap/_scaffold/config.py`, a named high-risk surface
**Opened**: 2026-10-26
**In brief**: The file that tells the next work session where to start stops being a tracked file and becomes a note on the operator's own machine, because the tracked copy was out of date about 20 hours after its last rewrite.

**The Maintainer's words.** This change started with his direction, not with an
incident. On 2026-10-16, recorded in the queued row at `dev/PLANNING.md:486-493`:

> "those docs should be, but maybe not NEXT_SESSION?" … "Let's put this up on the board"

On 2026-10-26, in chat:

> "Also, NEXT_SESSION becoming a local note should happen in v0.5 too."

The v0.5 planning session then recorded his answer to adding it to the release
(`dev/PLANNING.md:49`):

> "Yes, add it to 0.5 (Recommended)"

**Authoring tier.** Doctrine puts proposal authoring at the medium tier
(`doctrine/roles.md:174-178`), and Cairn's mapping gives that tier to Sonnet
(`dev/.cairn/model-selection-mapping.yml:25-30`). I wrote at that tier. I ran no
separate high-tier premise check (`doctrine/roles.md:178-180`); the proposal
review is the high-tier read of the premise.

## In brief

**Conclusion.** Stop tracking the handoff file. Cairn stops shipping
`dev/NEXT_SESSION.md`. At goodnight the designated owner writes a local note,
`dev/reflections/next-session.md`, in a folder git already ignores. What the next
session needs lives in a plan, the board, an issue or doctrine, as the Maintainer
asked. No tool logic changes (three message strings do): I found that
`session-start` does not open the file today.

**Why (measured).** The 2026-10-19 version said "The goal is release 0.4" and
`v0.4.0` was tagged 20 hours 19 minutes later; the file still said so six days
after. Four plans it listed as in flight were archived within 19 hours. 15 of the
25 commits that changed it changed nothing else. I did not measure how often an
agent acted on a stale line; that it cost work is an assumption.

**Cost.** One row deleted from an installer table in the engine, so a Security
Review. Four frozen files change and one test node drops, all inside the one 0.5
re-anchor. A new install gets one fewer file and one fewer slot to fill (20 become
19, measured on one profile). Existing projects keep their copy; `upgrade --plan`
prints one informational line.

**Not checked.** I ran no test, changed no repository file but this one, and did
not read the two adopter repositories. The full list is under "What I did not
check".

## Questions for the Maintainer

Each has my default. An unanswered question takes it.

1. **Where does the local note live, and does the install create it?**
   *Default:* `dev/reflections/next-session.md`; the install creates nothing, and
   the first goodnight writes the note. Git already ignores that folder in every
   install that has the `reflections` module, which is on by default
   (`.gitignore:9`, `bootstrap/_scaffold/config.py:82-84`, `:1113-1120`). Neither
   prune deletes a name without a date: I read `tools/session.py:1727-1752` and
   `templates/modules/default-on/prune_reflections.py`; I did not run them. A new
   ignore line would not reach projects that already installed Cairn, because
   `upgrade` adds ignore lines only when a module or a skill is newly added
   (`bootstrap/_scaffold/upgrade.py:1817`, `:2477`). The 2026-10-16 queue commit
   (`d963748a`) said "scaffold-seeded empty". An empty seed is ignored, so it
   would exist only on the machine that ran the install. *Alternative:* keep the
   path `dev/NEXT_SESSION.md` and ignore it. That brings the problems in Context,
   items 4 and 5.
2. **Does `session-start` read the note?** *Default:* the tool does not, as today
   (`tools/session.py:1488-1580` never opens the file). The skill's judgment step
   gets one sentence: read the note if it exists, as a hint to check; if it is
   absent, start from the board and the commit log. *Alternative:* the tool prints
   the note's age in commits. That is new code; I would add it only if asked.
3. **What are existing projects told?** *Default:* nothing changes in their tree.
   `bootstrap/UPGRADE.md` gets a short section: keep your file, or reduce it to a
   line or empty it; do not delete it and do not untrack it; write the new note at
   the new path. *Alternative:* teach `upgrade` to drop the retired lockfile
   record. That is new engine logic and a second Security Review, and the
   informational line would stop repeating. I would queue it after 0.5 only if the
   repeating line bothers anyone.
4. **Is Cairn's own tracked copy deleted in the same change?** *Default:* yes,
   last, after one read that moves anything durable out of it. I found one item
   with no home on the board (Context, "What would be lost"). Its lockfile record
   stays, as the agreement's did (`dev/.cairn/cairn-lock.yml:52-55`, `:82-85`).
   *Alternative:* leave it as a stale tracked file. I reject that: it keeps the
   problem in the one tree that proves the fix.
5. **How much of the handoff doctrine stays?** *Default:* the rewrite-from-scratch
   rule and the five-element shape stay, as guidance for the local note, with two
   added sentences: write only what no artifact carries, and stamp the note with
   the commit it was written at (`doctrine/session-routines.md:139-205`).
   *Alternative:* delete the five-element list, about 30 lines, to match the 0.5
   theme "plain, short, and fits the install" (`dev/PLANNING.md:33`).
6. **May the Decision say the rate-limit gate is not engaged?** *Default:* yes.
   This changes doctrine, so the gate applies (`doctrine/rationale.md:433-453`).
   It asks for recurrence, a routine-boundary synthesis, or a Maintainer high-risk
   classification, and the direction above is none of those. The model-tier
   proposal asked the same question and the Maintainer answered "Yes, not engaged
   (Recommended)" (`dev/proposals/archive/2026-10-26-claude-model-tier-rules.md`,
   Decision). I do not claim recurrence: the staleness cases below are one failure
   shape, but I set no window or count.

## Context

**How I searched.** I ran `git grep -n -i -I -E 'next[_-]session'` over the tracked
tree, leaving out the append-only history (`dev/proposals/archive`,
`dev/plans/archive`, `dev/reviews`, `dev/strategy`; 42 files mention the file and
none is edited). Control: the pattern finds `templates/core/dev/NEXT_SESSION.md`,
which contains it. A first pass with only the spelling `NEXT_SESSION` missed five
files that write "next-session" in prose (`doctrine/session-routines.md`, both
`session-end/SKILL.md` copies, both `agent_collaboration.md` copies). I then
searched "handoff", "next session" and "hand-written" and read each hit; no other
file describes the handoff file without naming it. I did not search untracked files
or the adopter repositories. I took the measurements at commit `1d5a047b`. Three later commits changed only
`dev/PLANNING.md`, added another proposal, and edited the `session-start` skill and its
test, none of which I cite by line. So every line number here holds at `c7705221`.

**Terms.** The *lockfile* (`dev/.cairn/cairn-lock.yml`) lists every file Cairn
installed, with a checksum, so `upgrade` can merge later changes. A *slot* is a named
block in a template that the project fills in. A *frozen file* has its checksum
pinned in the gate manifest (`bootstrap/tests/fixtures/gate_manifest.json`); an edit
owes an entry in the re-anchor, the Maintainer's ceremony at the cut that re-pins
those checksums. The *AST baseline* pins the parsed structure (abstract syntax tree)
of each symbol in the installer's code; changing a symbol owes an entry in the same
ceremony. A lockfile record marked *living-state* is a file the project edits, so the
tamper check skips it.

**What the file is.** The "cold-pickup handoff" (`templates/core/dev/NEXT_SESSION.md:4-10`).
The goodnight owner rewrites it from scratch each time
(`doctrine/session-routines.md:139-173`). Cairn's copy has 274 lines and 14,509
bytes. A new install writes a 44-line copy with one slot, `next-start`, which the
install report counts among its slots. Nothing in `tools/session.py` reads it; the
agent reaches it only because `AGENTS.md:174-180` says to "re-anchor on the `dev/`
tree".

### Why it is worth doing

`git log --format=%h -- dev/NEXT_SESSION.md`, since Cairn adopted itself on
2026-06-12. Commit counts are `git rev-list --count A..B`; all 25 commits are
ancestors of `HEAD`.

| Measure | Result |
|---|---|
| Commits that changed the file | 25 (29 with `--follow`, which adds the template's 4 earlier commits) |
| Of those, commits that changed no other file | 15 |
| Lines added and deleted, summed over the 25 | 1,419 and 1,145 (`git show --numstat`) |
| Quiet spell 1 | 49 days, 2026-06-12 to 2026-07-31; 186 commits landed in between |
| Quiet spell 2 | 48 days, 2026-09-01 to 2026-10-19; 290 commits landed in between |
| Commits since the last full rewrite (`778fe217`) | 218 at `1d5a047b`; the file changed in two of them |

Statements in the 2026-10-19 version that were stale when next read:

| Statement | What was true | Source |
|---|---|---|
| "The goal is release 0.4, with the repository made public" (`dev/NEXT_SESSION.md:12`) | `v0.4.0` was tagged 2026-10-20 09:34, 20 h 19 min after the rewrite at 13:15 on 10-19. The file still said so on 10-26. | `git for-each-ref refs/tags/v0.4.0`; `dev/PLANNING.md:11` |
| "166 commits are unpushed (`origin/master` is at `9832c411`)" (`:21`) | My local `origin/master` is `c0b73c17`, dated 2026-10-23. I did not fetch, so I know only that a push happened. | `git rev-parse origin/master` |
| Items 3 to 6 "In flight at the pause" | `board-as-basis` archived 10-19 17:59 (`60bf7cab`); `review-stance-and-lenses` 10-19 18:11 (`0974a4de`); the agreement removal 10-20 07:36 (`01e214f2`); `model-mapping-install-path` 10-20 08:16 (`fe16286f`). All within 19 h 1 min. | `git log -1` on each |
| A test file "is not frozen" (`0c3a483b:dev/NEXT_SESSION.md`, lines 117-118) | True at `0c3a483b`: it was not a key in `frozen_files`. False from 2026-10-20 08:38 (`6f29519d`, the re-anchor). Corrected 2026-10-26 13:37 (`9f61e8c8`). | the manifest at each commit |

The board already calls the file stale (`dev/PLANNING.md:197`). The 2026-09-01
version's header said "A stale line in this file was repeated four times in one
session before anyone opened the repository it described"
(`7a78c283:dev/NEXT_SESSION.md`, lines 5-7). The current header says only "may be
stale" (`dev/NEXT_SESSION.md:3-9`). I did not find the session that sentence
describes, so I treat it as the file's own report, not a measurement.

### What reads or depends on the file

| Group | Files | What happens |
|---|---|---|
| Engine (AST-attested) | `bootstrap/_scaffold/config.py:549` (the install-table row) | **Row deleted.** Changes the symbol `Assign:_CORE_MAPPINGS` and the published `scaffold.py --manifest` (96 rows become 95, measured). |
| Engine | `config.py:756` (a comment); `bootstrap/_scaffold/lockfile.py:85` (the living-state list) and `:62` (a comment) | **List entry stays**; comments reworded. No AST change. Context item 6 says why the entry stays. |
| Shipped sources, 10 | `templates/core/dev/NEXT_SESSION.md`; `templates/core/AGENTS.md:186-189`; `templates/core/dev/README.md`; `templates/core/dev/agent_collaboration.md`; `templates/modules/default-on/documentation_plan_template.md`; `templates/modules/default-on/verify_stems.py`; `templates/modules/default-on/reflections-README.md`; `templates/skills/session-end/SKILL.md`; `templates/skills/_lib/session.py`; `docs/dev-tour.md` (reaches adopters as `dev/modules/onboarding/dev-tour.md`) | 1 deleted (the first), 9 edited. The `session.py` edit is three message strings (`:1960`, `:1971`, `:2052`) and no logic. |
| Cairn's own copies, 8 | `tools/session.py`, `scripts/verify_stems.py`, `.agents/skills/session-end/SKILL.md`, `dev/reflections/README.md`, `dev/modules/onboarding/dev-tour.md` (byte-identical to their sources today, by `cmp`); `dev/README.md`, `dev/agent_collaboration.md`, `docs/DOCUMENTATION_PLAN.md` (differ from their templates by filled slots, so hand-edited) | Edited the same way. Seven are in Cairn's lockfile; with `AGENTS.md` that is 8 records to re-finalize. |
| Cairn-only prose | `AGENTS.md:174-184`, `:470-472`; `bootstrap/BOOTSTRAP.md:507`, `:631`; `bootstrap/fidelity-check.md:142`; `doctrine/session-routines.md`, `doctrine/proposals.md:135`, `:350`, `:382-385`, `doctrine/plans.md:1031-1034`, `doctrine/doc-governance.md:320`; `bootstrap/UPGRADE.md` (new section); `CHANGELOG.md:2901` and a new Unreleased entry; `docs/quickstart.md:298` ("20" becomes "19") | Edited. Four doctrine files, so question 6 applies. |
| Frozen files | `scripts/verify_stems.py` and its twin; `bootstrap/tests/test_upgrade.py:1795`; `bootstrap/tests/test_quickstart_sequence.py:197` | **4 edited.** `bootstrap/tests/test_verify_stems.py` (lines 6, 79) is frozen too; it only creates the file, so I expect no edit. |
| Gate manifest | `bootstrap/tests/fixtures/gate_manifest.json:2311` | One test node drops (item 9). Not hand-edited. |
| Left alone | `case-studies/modflow_tools-fidelity-manifest.yml:31` (a snapshot at a pinned commit); the 42 history files; `.gitignore`; `tools/board.py` | No change needed. |
| Not mine | `dev/PLANNING.md` (another session owns it; the queued row at `:486-494` leaves the board when this archives) | Untouched. |

### How the machinery treats the file today (measured on scratch copies)

I made two copies of this tree with `git archive` at `1d5a047b`, outside the
repository. In the second I deleted the template and the table row, which is the
engine change this proposal makes. I installed the `solo-greenfield` profile from
each and ran `upgrade` from the first install against the second copy. Python
3.13.13. Nothing in the repository was written.

1. **Today's install** writes the file, records it in the lockfile as living-state
   (`bootstrap/_scaffold/lockfile.py:56-70`), and lists its slot among 20 that
   "require agent attention".
2. **After the change** the install writes no file and no record, lists 19 slots,
   and `verify_integrity.py` passes. A frozen test compares the quickstart's "20
   unfilled block slots" (`docs/quickstart.md:298`) with the live count
   (`bootstrap/tests/test_quickstart_sequence.py:241-250`), so the prose must change.
3. **`upgrade --plan`** on the older install prints one line about the file,
   `removed-upstream 1: dev/NEXT_SESSION.md` (`upgrade.py:523` is the code). After
   `--stage` and `--apply` the file's bytes, its lockfile record and its cached base
   copy were unchanged, `verify_integrity.py` passed, and the next `--plan` printed
   the line again. The collaboration agreement took this path
   (`bootstrap/UPGRADE.md:46-60`).
4. **A `.gitignore` line does not untrack a tracked file.** With the path ignored and
   the file still tracked, `git status` still showed ` M dev/NEXT_SESSION.md` after an
   edit, and `git check-ignore` printed nothing. After `git rm --cached` and a commit
   it matched. Control: an untracked file under `dev/reflections/` matched at once.
5. **A retained lockfile record plus a missing file is a trap.** In a fresh clone of
   a project that had untracked the file, a bare `upgrade --finalize` refused ("1
   tracked file(s) missing on disk"). `verify_integrity.py` still printed OK; its
   note counted the file as "unreadable 1". Control: deleting a record that is not
   living-state (`dev/README.md`) made `verify_integrity.py` fail with "missing".
6. **Two mutants.** (a) Template deleted, table row kept: the install exits 0 with
   one warning, `[warn] core template missing: core/dev/NEXT_SESSION.md`. (b) The
   path removed from the living-state list: an upgraded tree fails
   `verify_integrity.py` with "illegal living_state opt-out ... (tamper / malformed
   lockfile)". That is why the list entry stays.
7. **`scripts/verify_stems.py`** scans `dev/PLANNING.md` and `dev/NEXT_SESSION.md`
   by default (`scripts/verify_stems.py:67-70`) and reports a missing file as an
   error (`:118`). In a tree with only `PLANNING.md` it exits 1, "file not found";
   with both files it exits 0 (control). A fresh install after the change would
   fail this check at once.
8. **`check_cairn.py`** on the edited copy gave two new flags, both at
   `CHANGELOG.md:2901`, a historical line that links to the deleted template.
9. **Engine and gate counts.** Following step 1 of `bootstrap/AST_BASELINE_RUNBOOK.md`,
   today's tree has 10 changed symbols (all functions) and the edited copy has 11;
   the new one is `Assign:_CORE_MAPPINGS`. `_gate_manifest.py verify` on the edited
   copy shows one `COLLECTION-DROPPED`, the node at `gate_manifest.json:2311`; the
   live tree shows none. `test_quickstart_sequence.py` is already `FROZEN-MODIFIED`
   on the live tree, so my edit to it adds no entry. The re-anchor gains three
   frozen files and one dropped node.
10. **A second `git worktree`** of a project does not contain the ignored note.
    Ignored files do not travel between worktrees or machines.

### What would be lost

The file is the only place for four kinds of text: the recommended first task and
why; stopping points of work in flight; bookkeeping owed to the board; coordination
warnings. It does the third job backwards: it holds "New roadmap rows owed" for
`dev/PLANNING.md` (`dev/NEXT_SESSION.md:240-251`). I checked its three rows against
the board. One is there (the interpreter-binding move, `dev/PLANNING.md:136-139`).
One looks fixed (`templates/modules/team-gated/security-review.md:181` is plain text
now). One has no row: correcting two stale citations in the stewardship proposal.
Whether it is still owed I did not check. The migration read must catch items like
it before Cairn's copy is deleted.

`docs/assets/shared-record-across-sessions.svg:98` promises "Nothing the next session
needs lives only in a chat window." A local note could break that promise, so the
rule below says nothing a later session needs may live only in the note.

## Proposal

**1. Cairn stops shipping the file.** Delete `templates/core/dev/NEXT_SESSION.md` and
the row at `bootstrap/_scaffold/config.py:549`. Leave `dev/NEXT_SESSION.md` in the
living-state list (`lockfile.py:85`); without it, upgraded projects fail the
integrity check (item 6b). A new install creates no handoff file, record or slot.

**2. The handoff becomes a local note.** The designated full-handoff owner writes it
at `dev/reflections/next-session.md` at goodnight, as an agent step; no tool writes
it. `doctrine/session-routines.md` gains:

> The next-session note is local. Write only what no durable artifact carries.
> Begin it with the date and the short commit id you wrote it at, so a reader can
> count the commits since. Cite a commit, a file or a board row for each claim.
> Treat the note as a hint and check each line against the log and the board
> before repeating it. Nothing a later session needs may live only in this note.

The goodnight bullet in both `AGENTS.md` copies gains "and a local next-session note
(never committed)". The `session-end` skill, `dev/agent_collaboration.md` and the
three strings in `session.py` say the same. The reflections README gains one
sentence: `next-session.md` is the one file in the folder that is not a reflection,
and the prunes leave it alone.

**3. `session-start` is unchanged** except for one sentence in the skill's judgment
step: read the note if it exists, as unverified; if it is absent, start from the board
and the commit log.

**4. `verify_stems.py` scans `dev/PLANNING.md` only by default**, in both twins. A
project that keeps its own tracked file passes `--scan`. The script is verbatim, so
existing projects receive the change as a verbatim update.

**5. Existing projects keep their copy.** See "Migration for existing installs".

**6. Cairn's own tree.** After the migration read, `git rm dev/NEXT_SESSION.md`; the
lockfile record stays, as the agreement's does. `CHANGELOG.md:2901` becomes plain code
text instead of a link. This lands last.

**7. Sequence.** Land after the Plain Language `--finalize` of `AGENTS.md` and after
the security-findings fixer's edits to `tools/session.py` (`dev/PLANNING.md:37-50`),
because we edit the same files. Keep the two `session.py` copies byte-identical
(`cmp`). The onboarding-at-install proposal
(`dev/proposals/2026-10-26-claude-retire-delayed-onboarding-prompts.md`) overlaps this
one: both add a section to `bootstrap/UPGRADE.md` and an entry to `CHANGELOG.md`, both
change the published manifest and the install report's slot count, and both feed the
same re-anchor. Every count in this proposal is against `1d5a047b`; whichever lands
second recounts. I read it only to find overlaps, and I edit none of its files.

**What this adds to the one 0.5 re-anchor** (Maintainer-only, at the cut). AST:
`Assign:_CORE_MAPPINGS`, the 11th changed symbol. Gate manifest: `scripts/verify_stems.py`,
`templates/modules/default-on/verify_stems.py` and `bootstrap/tests/test_upgrade.py`
(three new frozen-file edits); `test_quickstart_sequence.py` (already owed); one dropped
node; the new test file, which freezes at the cut. Lockfile: eight records re-finalized.

Proposed paths:
* `bootstrap/tests/test_next_session_local_note.py`
* `dev/reflections/next-session.md`

## Rationale

This is the shortest route to the Maintainer's direction that reuses what exists: the
`removed-upstream` path (item 3), the reflections ignore line (question 1), and the
habit that a file Cairn stops shipping becomes the project's own. It avoids three
traps I measured: an ignore line that does not untrack (item 4), a lockfile record
that outlives an ignored file (item 5), and an ignore line that never reaches existing
projects.

It also removes an instruction channel. A tracked prose file that the next agent is
told to read can be edited by any contributor; an untracked file is not carried by a
clone or a pull request. This is my reasoning; I did not test it.

## Alternatives considered

1. **Do nothing; keep the file tracked.** It keeps what the local note cannot give: a
   copy that a second machine or a reviewer sees in git. It costs what Context
   measured: 15 commits that touch only the file, long quiet spells, a rewrite stale
   in 20 hours, and a slot every new project must fill. I reject it because the
   Maintainer's direction is to end it, and the durable content already has homes.
2. **Keep it tracked, shrunk to a pointer stub of about 15 lines.** This is the
   cheapest alternative. It cuts the staleness but keeps a commit per goodnight, the
   install slot and the frozen-test edits, and a stub that only points duplicates
   what `session-start` already prints.
3. **Keep it tracked but generate it from the board.** This is the strongest
   alternative I rejected, because it keeps a shared copy that cannot drift from the
   board. The board "makes no judgment about ... what should happen next"
   (`tools/board.py:11-13`), and that judgment is the file's only content with no
   other home. A committed generated file is stale after the next commit unless
   something regenerates it. It also builds a generator, against "fix defects, build
   nothing new" (`dev/PLANNING.md:16-17`).
4. **The same path, ignored** (the board row's wording). Rejected for items 4 and 5.
5. **Another path outside the reflections folder** (`dev/.cairn/`, or a user-level
   folder). A new ignore line does not reach existing projects, and a user-level file
   is invisible to other worktrees and to other agents on the machine.

## What is lost

A handoff that follows a person to a second machine or worktree (item 10). The
mitigation is the rule that nothing a later session needs lives only in the note,
plus the places that already carry state: the board (`python tools/board.py
--maintainer`, `tools/board.py:8-32`), the plan's Waiting line
(`dev/plans/_template.md:44-45`), proposal and plan statuses, `dev/PLANNING.md` rows,
issues, and the commit log. A team that wants the note shared can track that one
file with `git add -f` (measured: it works) and accept the staleness cost; Cairn
does not ship that as the default.

**Two agents, one tree.** There is one file and one owner by doctrine
(`doctrine/session-routines.md:100-115`). If two agents wrote it, the last write wins;
nothing merges and nothing enters history. I accept that. **Two machines.** The second
has no note and starts from the board and the log.

## Migration for existing installs

For a project that already has Cairn installed, after `upgrade --apply`:

1. Run `upgrade --plan`. You should see `removed-upstream 1: dev/NEXT_SESSION.md`. It
   is information, and it prints on every plan while your lockfile lists the file. If
   the plan names this file under any other heading, stop and file an issue.
2. Keep your file, or reduce it to one line, or empty it. **Do not delete it and do
   not run `git rm --cached` on it.** Your lockfile still lists it, and a fresh clone
   without it makes a bare `upgrade --finalize` refuse. If you never filled its
   `next-start` slot, the integrity note keeps listing the file (measured). I expect an
   empty file has no slot to list; I did not run that.
3. At your next goodnight, write the new note at `dev/reflections/next-session.md`.
   First run `git check-ignore -v dev/reflections/next-session.md`. You should see
   the line that ignores it. If it prints nothing (you removed the `reflections`
   module, or edited `.gitignore`), add the path to `.gitignore` before you write.
4. `scripts/verify_stems.py` now scans `dev/PLANNING.md` only. To keep scanning your
   own file, run it with `--scan dev/PLANNING.md dev/NEXT_SESSION.md`.

I did not run these steps on a real project; the scratch "project" was a fresh install.

## Documentation / doctrine surface

Prescription goes to the governing layer (both `AGENTS.md` copies); the process to
`dev/agent_collaboration.md` and its template; the routine's detail to
`doctrine/session-routines.md`, with `proposals.md`, `plans.md` and `doc-governance.md`
losing their references to the file; the adopter's steps to `bootstrap/UPGRADE.md`; the
file maps to `dev/README.md`, `docs/dev-tour.md` and `docs/DOCUMENTATION_PLAN.md`, routed
by layer as `docs/DOCUMENTATION_PLAN.md` directs. Headings in `doctrine/session-routines.md` stay, so
existing citations resolve. Nothing names a model or a vendor.

## Evidence / verification plan

Cairn has no CI, so a person triggers every check below. Bold marks a check that only
a reader can make.

| Surface | Check | What triggers it |
|---|---|---|
| All edited Markdown | `python scripts/check_cairn.py`; `python scripts/claim_check.py <file>` | a person, before commit |
| Neutrality | `python scripts/quality_gate.py --sub neutrality --sub redundancy` | a person; the certifying run before a push includes it |
| Install, manifest, lockfile, upgrade | the new test file and the existing tests below | `pytest`, run by a person |
| The ignore line | new test: `git check-ignore -q dev/reflections/next-session.md` after a fresh install; control: `dev/reflections/README.md` is not ignored | `pytest` |
| Both prunes leave the note | new test with a dry run; control: an old dated file is listed | `pytest` |
| The note is read as a hint | **a reviewer reading the skill text**; no command sees an agent's behaviour | a person |

### Tests required

New file `bootstrap/tests/test_next_session_local_note.py`, modelled on
`bootstrap/tests/test_agreement_retired.py:72-121`. It checks: a fresh install has no
`dev/NEXT_SESSION.md`, no record and no manifest row; the path stays in
`_LIVING_STATE_DSTS` (the pattern at `test_agreement_retired.py:157`); `upgrade --plan`
prints exactly one `removed-upstream` line and `--apply` leaves file, record and cache
unchanged; a fresh clone refuses a bare `--finalize`; the default `verify_stems.py`
run passes with only `PLANNING.md`; no shipped source tells a reader to read or write
`dev/NEXT_SESSION.md` (the pattern at `test_agreement_retired.py:155-175`).

Existing tests, scoped: `test_agreement_retired.py`, `test_upgrade.py`
(`TestLivingStatePartition`), `test_quickstart_sequence.py`, `test_manifest.py`,
`test_verify_stems.py`, `test_core_dev_folders.py`, `test_lockfile_module.py`,
`test_prune_tools.py`, `test_session_failsafe.py`, `test_skill_contract.py`,
`test_ast_attest.py` (red by design until the re-anchor) and `test_gate_manifest.py`.
I found them by searching what reads each touched file and have run none. The plan's
mapping owns the final list.

Mutants, each beside an unmutated control: restore the table row (the install test must
fail); remove the living-state entry (the upgrade test must fail, as in item 6b);
restore the old `verify_stems.py` default (the fresh-install test must fail). Where a
finding says a change must reach every member of a set, list the set from the tree with
the search above and mutate each member in a separate copy.

Boundary B is `full`: the change touches the install contract, the engine and frozen
files. It is recorded `Certified by: pending` until the next certifying run. Nobody sets
`CAIRN_FULL_SUITE=1` for this change.

Smoke checks: `python bootstrap/scaffold.py --manifest` (95 rows, no `NEXT_SESSION`
row); `python bootstrap/scaffold.py --dry-run --config bootstrap/profiles/solo-greenfield.yml`;
`python scripts/check_cairn.py`.

#### Security preflight

This change touches a named high-risk surface (the engine) and the install contract, so
all five questions apply.

* **S1 — Who supplied it?** The change decides one thing: whether an installed file is
  "removed upstream". The input is the `src` field of a lockfile record, supplied by the
  project being upgraded. The answer is whether that template exists in the Cairn
  checkout doing the upgrade, which the project does not supply. The branch reads no file
  (`upgrade.py:520-524`); `_theirs_bytes` runs first with the record's `src`, the existing
  path that the 0.5 security-findings row covers. I add no input.
* **S2 — Can it fail?** Each check above has a one-line mutant; I ran two (item 6). The
  "exactly one line" test compares to a literal string, not to the engine's output, so it
  can fail. The new test does not exist yet, so I have not run it.
* **S3 — What fires it, over what?** A person runs `scaffold.py upgrade --plan`,
  `verify_integrity.py` or `pytest`. The adopter-facing sentence will be in
  `bootstrap/UPGRADE.md`; the new test pins that it and the printed line name the same path.
* **S4 — Which way does it break?** A half-done change (template gone, row kept) installs
  fewer files with one warning (item 6a): less authority, not more. A wrong edit to the
  living-state list fails closed (item 6b). If a project's `dev/reflections/` is not
  ignored, the note could be committed: local text leaks into git, and nothing executes.
* **S5 — Who still wins?** I assume someone who can edit a project's committed lockfile.
  They can still mark `dev/NEXT_SESSION.md` living-state and edit the file without the
  tamper check noticing. It is a prose note, and the list allowed it before this change.
  The class is closed by enumeration, not by construction. A hostile instruction written
  into a note an agent reads has no lexical signature; the rule above says to treat the
  note as data to check.

### Independent scientific check

N/A: no scientific assumption or result touched. No scientific data is involved; every
number above describes this repository, not the world.

## What I did not check

* I ran no test and no part of the suite. A proposal is prose; scoped runs belong to the
  plan and the certifying run to the Maintainer's schedule.
* I did not apply the edits to the repository. The scratch copy changed only the table row
  and the template.
* I measured the install on the `solo-greenfield` profile only. The 19-slot count and the
  96-to-95 row count may differ on the other two profiles.
* The scratch "project" was a fresh install, not a project with months of edits. I did not
  read or touch either adopter repository, as instructed.
* I did not fetch, so `origin/master` is the local reference.
* I did not measure how often an agent acted on a stale line, and I did not verify the
  "four times" sentence.
* I read, but did not run, the two prune functions and `test_manifest.py`.
* I did not check Windows or a case-insensitive disk, or whether the stewardship citations
  are still owed.

**Found on the way, not changed here.** `session-start` finds "the last handoff" by a
commit subject that starts with "Goodnight" (`tools/session.py:2076-2080`). Cairn's
handoff commits of 2026-10-19 begin "Handoff", so on this tree it prints a range of 508
commits (`7a78c283..HEAD`). That does not depend on the handoff file; it is a separate
defect, left for the Maintainer to route.

## Signals the change is wrong

I have no base rate for these thresholds; ten goodnights is a review point the Maintainer
can move.

* Within ten goodnights after release, a session starts without orientation that the
  board, the plans and the log could not give, and the Maintainer or an agent says so
  twice. The migration rule failed.
* `git ls-files dev/reflections` lists anything beyond `README.md`: a note was committed.
* After an upgrade, `upgrade --plan` prints anything beyond the one informational line
  about this file, or `verify_integrity.py` fails.
* The board gains rows that only restate what the old file held: the clutter moved
  instead of ending.
* The Security Review finds a way to use the retained record that the list does not
  already allow. I would withdraw proposal item 1.

## Scope delta

**Scope delta**: preserved (opening revision; nothing removed from this proposal).

Against the board row (`dev/PLANNING.md:486-494`), two of its means differ: it names an
"ignore pattern" and a "scaffold seed", and I propose neither, because the existing
reflections ignore line serves and a seed would not reach existing projects (question 1).
The outcome, a local and untracked handoff, is unchanged. If the Maintainer wants the note
to stay at `dev/NEXT_SESSION.md`, both means return and the engine grows by
`_SKILLS_GITIGNORE`. I record this so a reader sees the difference; I do not treat it as
a concession of baseline scope.

## Assurance path

**Assurance path**: high-assurance (the scaffold engine, the install contract and a
verbatim script that adopters execute are in the template's trigger list).

**Why a Security Review.** The change deletes a row from `_CORE_MAPPINGS` in
`bootstrap/_scaffold/config.py`, and `AGENTS.md:448-451` says a one-line engine change
needs a proposal and a Security Review unless it is a defect repair; this is not one. The published install manifest also changes by
one row. The `tools/session.py` edit is three message strings, away from
`_resolve_interpreter`, so I do not count it as touching the interpreter-binding surface
(`AGENTS.md`, "High-risk surfaces"); a reviewer who reads it differently should say so.

The Security Review should test three things: the one-row engine edit and its effect on
install, manifest and upgrade; the retained living-state record on a tree where the file
is missing; and the change to a verbatim script that adopters run.

## Review -- Claude Sonnet 5.5 (Internal) -- 2026-10-26

```
Reviewed commit: d8fa0fa329ddc97f8c4ea2a0ac85e335b772565d
Target: the whole proposal, against tools/session.py, .agents/skills/session-start and session-end, doctrine/session-routines.md, bootstrap/_scaffold/{config,lockfile,upgrade}.py, scripts/verify_stems.py, bootstrap/UPGRADE.md, and the onboarding proposal (2026-10-26-claude-retire-delayed-onboarding-prompts.md)
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual (pass 1 of 2). The Security Review is a separate later pass. I neither perform nor clear it.
**Findings**: raised (2 blocking, 12 non-blocking)
**Verdict**: REVISE

**Conclusion first.** The change should happen, and its shape is sound. A local note in `dev/reflections/` is the right place, and the author's measurements of history and install behaviour held up when I redid them. Two things must change before the Maintainer decides. First, the only instruction to read the note sits in a manual, single-tool skill, not in `AGENTS.md`, so a cold agent may never open it (F1). Second, the cost list is short by one frozen test and one skill pair, and it misses the one test the onboarding proposal names as the collision point (F2). The rest is wording, a better way to treat `verify_stems.py`, and two alternatives to weigh. I am fairly sure of the verdict. I measured the counts and the install behaviour. I judged the handoff question (F1) from the text of the skill and `AGENTS.md`, not from watching a cold agent.

**Foundations**

1. **Should this happen as framed?** Yes for the outcome: the Maintainer directed it, and the tracked file cost 25 commits (15 of them nothing else). Not as framed in the In brief: a local file does not cure staleness, so the cure must be the content rule and the stamp (F11). `git log --format=%h d8fa0fa3 -- dev/NEXT_SESSION.md | wc -l` gives 25; `AGENTS.md:174-180` names no note.
2. **Best alternative.** Doing nothing loses to the Maintainer's direction. The strongest option the author did not weigh is to put the next-session text in the owner's own dated reflection, under the heading every reflection already carries, `## Open threads / handoffs` (`tools/session.py:1875-1888`). It adds no new filename, no README special case and no prune exception, and the existing 30-date prune retires old notes on its own (F5).
3. **What would show it wrong.** The author's five signals watch for harm late and by report. The early test is a cold start: a fresh agent that reads only `AGENTS.md` and runs `ls dev/` and `rg next-session` should find the note, and today it would not (`git check-ignore -v dev/reflections/next-session.md` prints `.gitignore:9:dev/reflections/*`, so `rg` and `git ls-files` skip it). Add that probe (F1).

### Rulings on points (a) to (g)

**(a) Does the design deliver a handoff?** Only partly as written. The tool never reads the file today, so there is no regression (`grep -n -i 'next[_-]session' tools/session.py` hits only lines 1960, 1971, 2052, all strings). But today an agent finds the file by listing `dev/`. After the change it sits one folder down, ignored by git, among dated reflections. The one read instruction goes in `session-start`'s judgment step, and that skill is manual-only (`disable-model-invocation: true`) and Claude-specific. `AGENTS.md`, which every harness loads, gets the write clause in the goodnight bullet and no read clause in the session-start bullet. Fix in F1. The reflections folder is the right place. A fresh clone holds only `README.md` (`git ls-files dev/reflections`). Both prunes spare an undated name: I ran `_prune_reflections` in `--dry-run` on a scratch folder holding `next-session.md` and two old dated files; it listed the two dated files and not the note (the control). The reflections module already calls the folder "the cross-agent handoff surface" (`templates/modules/default-on/reflections.md:11-13`), which supports the choice. Does this repeat the onboarding finding of a mechanism nothing runs? Not that shape: no coded trigger is claimed to fire. It repeats the weaker shape: the stamp, the "cite each claim" rule and the "treat as a hint" rule are honour-system, and the proposal says so. That is the same discipline whose failure is the evidence. The honest framing is that the board and plans carry the handoff, and the note is a convenience (F3).

**(b) The evidence.** I re-derived these from `git log`, `git rev-list --count`, `git for-each-ref` and `git show`, and all matched: 25 commits touching the file; 15 that touch nothing else (a loop over `git show --name-only` counting one path); 29 with `--follow`; 1,419 added and 1,145 deleted; the quiet spells 49 and 48 days with 186 and 290 commits (`rev-list --count 7519c5da..d73baf11` and `7a78c283..778fe217`); 218 commits since `778fe217`, with 2 touching the file; `v0.4.0` tagged 2026-10-20 09:34:44, 20 h 19 min after the 13:15:24 rewrite; four plans archived by 08:16:01, 19 h 0 min after it; the quoted lines at `0c3a483b:dev/NEXT_SESSION.md` lines 12, 21 and 117-118. It is enough to carry out a direction the Maintainer already gave. It is not enough, alone, to remove a shipped file. A fair counter-argument has four parts. (1) It is one file in one repository. (2) Both failures are content failures: a long file that restates state that moves faster than the file. A short tracked stub would also cure them (Alternative 2). (3) The 15 commits that touch only the file are the handoff commits, which is what a handoff commit is. (4) The tracked history is the only record of what the next-session plan believed at each point, which is Cairn's own append-only principle, and the local note keeps none. The proposal's first sentence ("not an incident") already concedes that the Maintainer's word carries the decision, so I would say so in the In brief and drop the implication that the evidence does.

**(c) The options.** The rejection of "generate it from the board" is fair: the board states it makes no judgment about what comes next (`tools/board.py:11-13`) and a committed generated file is stale after the next commit. "The same path, ignored" fails for the reasons the author gives. I verified all three in a scratch project built from `git archive d8fa0fa3`: with the ignore line added and the file still tracked, `git status --short` still shows ` M dev/NEXT_SESSION.md` and `git check-ignore` prints nothing (control: an untracked file under `dev/reflections/` matches at once); after `git rm --cached` and a commit it matches; in a fresh clone of that project, a bare `upgrade --finalize` exits non-zero with "1 tracked file(s) missing on disk". One point of fairness: that trap hits every option that retires the path, including the author's own plan to `git rm` Cairn's copy; the agreement file is already in that state in Cairn's tree (`ls dev/collaboration_agreement.md` fails; its record stays at `dev/.cairn/cairn-lock.yml:82-85`). So the plan must re-finalize the eight records with a scoped `--finalize <path>`, not a bare one. Two better options were not weighed: F5.

**(d) Existing installs.** The default is acceptable. I checked the claim about `UPGRADE.md`. With the file deleted and no git involved, `verify_integrity.py` exits 0 and prints OK; the word "unreadable" appears only in its slot note ("unreadable 1"); a non-living-state file deleted as a control makes it exit 1 with `missing:`. So `bootstrap/UPGRADE.md:56-58` ("makes the integrity check report it unreadable") is true only of the note, and the new section should not copy it (F8). I also ran what the author did not: an emptied file gives `unreadable 0`, lists no slot, exit 0, and a bare `--finalize` succeeds. That backs the advice to empty it.

**(e) Inventory and counts.** The pattern `git grep -n -i -I -E 'next[_-]session'` first found the template, which contains it (control). Matched: 34 files outside history, of which 2 are the two proposals, leaving 32 = the author's 29 plus `CHANGELOG.md`, `dev/PLANNING.md`, `gate_manifest.json`; 42 history files; Cairn's 5 byte-identical copies by `cmp` and 3 that differ; 7 of the 8 copies in the lockfile plus `AGENTS.md` = 8 records; the AST changed set 10 to 11, with `Assign:_CORE_MAPPINGS` the new one (the runbook's step-1 script, on a scratch tree with the template and row deleted); one `COLLECTION-DROPPED` node, `gate_manifest.json:2311`, in `test_review_stance_in_shipped_files.py`, and `test_quickstart_sequence.py` already `FROZEN-MODIFIED` (`_gate_manifest.py verify`); `--manifest` 97 lines to 96, so 96 rows to 95; a `solo-greenfield` install 20 slots to 19. Did not match: "4 frozen files edited" is 5 (F2); "10 shipped sources, 8 copies, 8 records" is 11, 9 and 9 (F2). `AGENTS.md:448-451` says a one-line engine change "needs a proposal and Security Review unless it is a defect repair" meeting the lifecycle's conditions. A row deletion in `_CORE_MAPPINGS` is not a defect repair, so `usual + Security Review` is justified.

**(f) `verify_stems.py` and the rest.** Narrowing the default is a contract change for adopters who keep the file, because they receive it as a verbatim update and silently lose coverage; F6 offers a smaller route. I confirmed the exit-1 "file not found" today and the exit-0 after narrowing, and that `test_verify_stems.py` still passes 15 of 15 with both twins narrowed, so "no edit to that test" holds. The change list is not complete (F2, F14). The separate defect is real: `session-start` finds the last handoff with `git log --grep='^Goodnight'` (`tools/session.py:1528`, default at `:2077`); Cairn's handoff subjects since 2026-10-19 begin "Handoff"; the range is 508 commits at `1d5a047b` (`git rev-list --count 7a78c283..1d5a047b`) and 512 at this commit. I found no shipped text that tells the owner to begin the subject with "Goodnight" (F9).

**(g) Sequencing.** The proposal says to recount but does not say what. The onboarding proposal names the collision point, `bootstrap/tests/test_notice_install.py:184` (`assert len(rows) == 96`), and says "whichever lands second re-reads it" (onboarding proposal, "Interactions with other 0.5 rows"). This proposal never cites that test, though it says it read the other for overlaps. I ran the scratch tree with only the engine change: that test fails (`expected 96 ... found 95`). F2 lists what the second to land must re-read.

### Findings

**F1 (blocking). The read side of the handoff is not in `AGENTS.md`.** See (a). *Fix:* add one clause to the session-start bullet of both `AGENTS.md` copies, such as "read the local next-session note, if present, as an unverified hint"; keep the skill sentence; add the cold-start probe above to the Signals. Do not add tool code now. If the cold-start probe fails in practice, a one-line `session-start` print (path, stamped commit, commits since) is the next step and is a later proposal.

**F2 (blocking). The cost list and the sequencing are incomplete.** (i) `bootstrap/tests/test_notice_install.py:184` pins 96 rows. It is frozen (`gate_manifest.json`, `frozen_files`), fails on the scratch tree, and is not in the proposal: frozen edits are 5, gate-manifest additions 4. (ii) Item 3 edits the `session-start` skill, but neither `templates/skills/session-start/SKILL.md` nor `.agents/skills/session-start/SKILL.md` (byte-identical by `cmp`, one lockfile record) is in the inventory: shipped sources 11, Cairn's copies 9, records 9. The skill was edited yesterday (`c7705221`), and `test_session_start_drain_rules.py` and `test_review_stance_in_shipped_files.py` (which names the skill and `fidelity-check.md`) read it. (iii) The claim that both proposals "change the install report's slot count" is not supported by the onboarding proposal, which I read as changing the report's line count (one new line) and the text of existing slots, not their number. I did not run its design. *Fix:* correct the counts; add a sequencing sentence naming what the second to land re-reads: the `test_notice_install.py:184` figure (96, then 87 for onboarding, 95 for this; both together 86), the `--manifest` smoke count, the `UPGRADE.md` section order, the `CHANGELOG.md` entries, the AST changed set, the eight-or-more lockfile records, and `docs/quickstart.md:298` with its test.

**F3 (non-blocking). Two rules in the proposed doctrine paragraph pull against each other.** "Write only what no durable artifact carries" and "Nothing a later session needs may live only in this note" leave the note holding only what the next session does not need. That is coherent if the note is a convenience, but then say so. The recommended first task has no durable home in the design. `session-start` already awaits the operator's direction (`.agents/skills/session-start/SKILL.md`, step 3). *Fix:* say in the paragraph that the note is a convenience, that the board and plans carry the handoff, and that the first task is the operator's call.

**F4 (non-blocking). The migration read is overclaimed.** Question 4 and "What would be lost" say one item has no home, after checking three rows in one of six sections. The section "Notes for whoever coordinates next" (`dev/NEXT_SESSION.md:265-274`) holds three durable lessons. Searches of `AGENTS.md`, `doctrine`, `dev/agent_collaboration.md` and `dev/PLANNING.md` for the key phrases of those lessons ("agent id", "take turns", "heavy test runs") found nothing; a one-term control ("agent id") does hit in `doctrine/` and `tools/`, so the search can match, but a paraphrase could be missed. The file also cites a board row "Work-intent claims" that is not on the board. *Fix:* make the plan's migration chunk list every section's durable content and its home, and change the claim to "one item found so far, one section read".

**F5 (non-blocking). Two alternatives are not weighed.** (1) The owner's reflection, under its existing `## Open threads / handoffs` heading: no new name, no README or prune exception, stale text pruned by date. Cost: the reader must find the newest owner reflection; a fixed path is easier. (2) The handoff commit's body: dated, immutable, stamped by construction, and it travels across machines without a tracked file. Cost: the Maintainer asked for a local note, the commit may not exist when no tracked file changed (F9), and the history becomes public. Add both to Alternatives with the reason each loses or wins.

**F6 (non-blocking). Narrowing `verify_stems.py` costs keepers coverage silently.** Smaller change in both twins: keep `NEXT_SESSION.md` in the default list but skip it when absent (explicit `--scan` paths still error when missing). Fresh installs pass; projects that keep the file keep the check; migration step 4 disappears. Weigh it or say why not.

**F7 (non-blocking). The doctrine paragraph should check the ignore before the first write.** A project without the `reflections` module has no ignore line and the note could be committed (the proposal's own S4). `git check-ignore -q dev/reflections/next-session.md` appears only in the migration steps. *Fix:* put the check in the `session-routines.md` paragraph and the `session-end` skill sentence.

**F8 (non-blocking). The new `UPGRADE.md` section should say what the check does, and say that emptying works.** Use: bare `--finalize` refuses; `verify_integrity` still passes, with "unreadable 1" in its note; an emptied file lists no slot and finalizes. While `UPGRADE.md` is open, correct the agreement section's "report it unreadable" the same way (an existing promise in a file the work already edits; no rule text).

**F9 (non-blocking). Route the handoff-anchor defect rather than leave it.** With no tracked handoff file, a goodnight whose scrub changes nothing makes no commit, so the "handoff commit" anchor can be absent; `session-routines.md` ("the commit makes the handoff durable") will then be wrong for the note. The `Goodnight` marker mismatch already breaks the range. A prose-only fix sits in a file the work already edits: the `session-end` skill can say the handoff commit's subject begins "Goodnight". That sentence is rule text, so it needs the Maintainer's word at the Decision; put it as a question or a board row.

**F10 (non-blocking; for the Security Review). The Rationale's "removes an instruction channel" is one-sided.** It removes the route through a clone or a pull request. It adds a local route: an agent that read untrusted text writes a note, and the next agent reads it with no commit and no diff. Reword to what is true and hand the substance to the Security Review. I did not analyse it.

**F11 (non-blocking). Say what actually cures staleness.** Locality does not. The cures are the short content rule, the stamp, and an absent note being honest where a stale tracked file is not. State this in the In brief and Rationale, with the counter-argument in (b).

**F12 (non-blocking). Four line citations in `bootstrap/_scaffold/upgrade.py` are wrong at the reviewed commit** (that file is unchanged since `1d5a047b`): `:523` is `:543` (`FilePlan(dst, "removed-upstream", ...)`); `:520-524` is `:540-544`; `:1817` is `:1860` (module add, `seed_gitignore(target, _GITIGNORE_SEEDS...)`); `:2477` is `:2528` (skills, `_SKILLS_GITIGNORE`). The sentence "every line number here holds at `c7705221`" is therefore not true. All other cited lines I opened held. `claim_check.py` reports no flags, as it does not test line content.

**F13 (non-blocking). The Maintainer needs a translator for the In brief and several questions.** "Four frozen files", "re-anchor", "engine", "slot" are used before the Terms paragraph defines them. Question 1 asks two things and carries evidence (`.gitignore:9`, prune line ranges, `upgrade.py` lines). *Fix:* a one-line gloss at first use in the In brief; split Question 1; move evidence out of the questions.

**F14 (non-blocking). Smaller items.** `bootstrap/fidelity-check.md:142` lists an install-contract surface (the fidelity manifest spec); name it as one, not as plain prose. The test map omits `test_notice_install.py`, `test_review_stance_in_shipped_files.py` and `test_session_start_drain_rules.py`. The new test's "plan prints one `removed-upstream` line" and "bare finalize refuses" nodes repeat what `test_agreement_retired.py` pins for another path; keep them only if they pin this path. The changelog entry should say who writes it and when, as the onboarding proposal does.

### What I tried to break

| Claim | What I ran | Result |
|---|---|---|
| 20 slots become 19; manifest 96 to 95 | install `solo-greenfield` from `git archive d8fa0fa3` and from a copy with the template and row deleted | 20 to 19; 97 to 96 lines |
| `upgrade --plan` prints one `removed-upstream` line | `upgrade --plan` of the old install against the changed copy | one line, `1: dev/NEXT_SESSION.md` |
| `.gitignore` does not untrack; fresh clone traps `--finalize` | scratch git project, as in (c) | confirmed; control matched |
| Deleted file leaves `verify_integrity` OK | `verify_integrity.py` on the clone and on a deleted-file copy; control deleting `dev/README.md` | exit 0 with "unreadable 1"; control exit 1 `missing:` |
| Emptied file is safe | empty `dev/NEXT_SESSION.md`, `verify_integrity` and bare `--finalize` | exit 0, no slot listed, finalize ok |
| Engine change breaks which tests | 10 test files, scoped, on the changed copy | 117 run: 2 failed (`test_notice_install.py:184`, `test_quickstart_sequence.py` step 3), 115 passed; `TestLivingStatePartition` 1 failed, 3 passed |
| Narrowed default needs no edit to `test_verify_stems.py` | both twins edited in a scratch copy | 15 passed |
| Prunes spare the note | `_prune_reflections --dry-run` with a dated control; standalone prune read only | note not listed; dated files listed |

All runs used `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13), on `git archive` extractions in a throwaway folder, which I removed. I never set `CAIRN_FULL_SUITE`.

**Coverage.** Not covered, and left for the Security Review: its whole obligation (I did not clear it or run its five questions). Security-flavoured points I noticed and did not analyse: F10; the three `session.py` message strings, which the author does not count under the interpreter-binding surface (`AGENTS.md`, "High-risk surfaces", which lists warning visibility); and the retained living-state record on a tree where the file is missing. I did not re-run `check_cairn.py` (the scratch copy is not a git repository, so it cannot list files), so the two flags at `CHANGELOG.md:2901` are unchecked; I did not run the other 20 or so test files the plan will map, `test_upgrade.py` beyond one class, or any `--profile` other than `solo-greenfield`; I did not read the plan, either adopter repository, or Windows behaviour; and I ran the standalone `prune_reflections.py` dry run without a listing control. Lenses applied: foundations, evidence, scope and counts, contract surfaces. Not applied in depth: documentation routing under `docs/DOCUMENTATION_PLAN.md`. **There are 2 blocking findings (F1, F2).** No clearing round follows; the author's Response and revision carry the proposal to awaiting-decision.
