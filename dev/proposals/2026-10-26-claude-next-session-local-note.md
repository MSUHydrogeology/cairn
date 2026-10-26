# Make the next-session handoff a local note

**Author**: Claude Sonnet 5.5 (Strategy; model id `claude-sonnet-5-5`)
**Status**: awaiting-review
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
