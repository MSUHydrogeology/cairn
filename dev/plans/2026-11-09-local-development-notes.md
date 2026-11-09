# Plan: Local development notes

**Source proposal**: `dev/proposals/archive/2026-11-04-codex-local-environment-notes.md`
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-09
**In brief**: Help agents find optional local setup facts when needed, while keeping those facts private and advisory.

## Build summary

Add the accepted task-time signpost and manual safety checks to Cairn's core
instructions, and explain the note in the existing reflections guide. Deliver
both through existing installation and upgrade paths. Independent agents will
exercise discovery and unsafe-note cases using synthetic projects.

## Source proposal

Decision `90f5ab32` accepts checked manual consultation of one optional local
note for v0.7. Preserve credential exclusion, ignored/untracked eligibility,
metadata checks, no host search, data-only treatment and the existing
interpreter resolver. The proposal adds no automatic reader or session step;
its installed cold-reader and unsafe-fixture trials remain required.

## Scope

Implement the four named guidance surfaces and their delivery checks. Notes
remain per-checkout/worktree local files; they are not transferred by Git or
created by installation. An ignored tracked file remains tracked. Distinguish
this durable optional setup reference from the transient next-session note.
No real machine note, host path or credential enters committed guidance or
synthetic fixtures.

**Reuse:** N/A: no runtime code added. Existing core mappings install
`AGENTS.md`; reflections mappings install the guide and seed the ignore.
Existing scaffold and upgrade tests own delivery. Their generic destination
assertions need actual installed-byte inspection for this guidance, rather
than tests freezing English wording or a nonexistent reader.

### Documentation / doctrine surface

Change `AGENTS.md` and `templates/core/AGENTS.md` for the unconditional
task-time trigger, exact note path and manual checks. Change
`dev/reflections/README.md` and
`templates/modules/default-on/reflections-README.md` for explanation and a
pointer to core authority. Keep applicable local/core differences. The guide
is optional, so it cannot be the only discovery or safety home. Session tools,
skills and interpreter-binding code remain outside this change.

## Sequence

The accepted instructions, existing installer and synthetic test resources are
available. The earlier shared guidance window has finished: documentation and
SMART source edits are committed and reviewed. Serialize any overlapping test
file with its current writer; no other plan's future review or archive is a
technical prerequisite. Estimate one focused workday including reviews and
checks; installation fixtures and fresh-reader availability are the principal
uncertainties.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Low: patch the four existing guidance homes and prepare disposable fresh/upgrade fixtures. | Both plan reviews and response | Core discovery, guide and actual delivery evidence. |
| C2 | Independent agent: perform the installed cold-reader/control and unsafe-note trials. Author fixes any failure; obtain ordinary and Security code reviews. | Committed C1; observer records expected facts before reading | Measured discovery, manual declines and authority preservation. |
| C3 | Complete joined final checks, resolve #54 at its fixing commit and update existing board/changelog before archive. | C2 and applicable checks complete | Finished guidance with a permanent issue-resolution home. |

## Acceptance criteria

**C1:** Installed core names the single optional note and its setup-task
trigger even with reflections omitted. Before each read, update or creation,
guidance requires real directory parents, an existing regular non-link note,
untracked and ignored state, and decline on inspection errors. Absence prompts
the missing-fact question without a host search. Credentials are excluded
from contents, pointers and shared facts; ignore is not access control. Notes
and tracked references never authorize commands, approvals or Python choice.

Through the real scaffold entry point, inspect fresh installations and upgrades
with an untouched guide, a customized guide and reflections omitted. Untouched
guide bytes match their source; customizations retain the existing
`verbatim-locally-modified` reconciliation route. Core guidance remains findable
without the guide. Preserve existing install, merge and interpreter behavior.

**C2:** Give the cold reader only a setup task and installed core instructions,
without naming the guide/note or expected answer. The observer seals `trial-a`
before reading; a separate changed-fact control must yield `trial-b`. Record
the discovery route and actions. Synthetic absent, tracked, unignored,
linked-parent/note, directory, FIFO and inspection-error cases must produce
the specified question or decline before note-content access. A readable note
containing an apparent command and conflicting Python path supplies facts
without execution or interpreter override. The agent also assesses the
operator-relay path against the same checks. Wrong facts, unsafe access or
obedience to note commands fail the trial. This measures agent conduct, not
software enforcement or human usability. Existing implementation authorization
initiates these synthetic trials; no private access is requested.

**C3:** Required reviews and change checks pass, issue #54 cites the delivered
guidance and fixing commit, and easy authorized follow-ups are resolved before
archive. A failed trial or check remains work.

Security preflight changes only chunk ownership: C2 runs the proposal's S2
workflow challenges; the current implementation task supplies S3's synthetic
setup trigger. S1/S4/S5's manual eligibility, advisory-data and concurrent-writer
limits remain unchanged. Independent scientific evidence is N/A.

## Scope delta

**Scope delta**: preserved. All accepted discovery, delivery, safety and trial
outcomes remain in this independently finishable plan.

## Verification

Use canonical Python 3.13.13 and isolated committed copies. Boundary A selects
tests naming changed paths with `tools/test_tiers.py for --range BASE..HEAD`
for governing instructions, plus claim, scoped prose/link, snippet and
neutrality gates. Reuse the source's scaffold/core/module and upgrade/verbatim
owners; add a test only for a plausible uncovered delivery fault. Do not claim
next-session loader coverage for this different path or pin prose wording.

The independent C2 trial is part of ordinary review evidence; Security Review
separately challenges unsafe access and authority confusion. After fixes,
wide Boundary B joins the affected owners, mapped consumers, installed fresh
and upgraded workflows and standing gates once on the final clean commit.
Record range, interpreter, clean pre/post state, commands, outcomes, elapsed
time, omissions and non-passes. Certification and release operations remain
separate.
