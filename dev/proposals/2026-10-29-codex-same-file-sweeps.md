# Detect and record same-file commit sweeps

**Author**: Codex gpt-6.1-sol
**Status**: awaiting-review
**Review**: usual
**Plan review**: required(Internal)
**Opened**: 2026-10-29
**In brief**: Check shared-file commits for another person's uncommitted work and record confirmed sweeps so the recurrence gate can count them.

## Context

Path-scoped commits can collect two people's changes to the same file.
Commit `5094a977` contains both an Internal and an Internal Security plan
review, although its message attributes the commit to the ordinary review.
The queue records that incident and a claim-release problem in
`dev/PLANNING.md`. The local `dev/measurement/collision_log.md` is untracked:
its rows are observations, not a reproducible committed history. The gate in
`tools/evolution_infer.py` counts `occurred` rows by event class, while
`tools/_intent/conflict.py` records a conflict at pre-commit, not who wrote
individual lines. A zero count therefore does not establish that no sweep
occurred.

## Proposal

Add a small human-operated check to the shared-workflow guidance: before a
shared-tree commit, inspect the complete candidate diff for each path and
compare it with the committer's own intended changes. If foreign or uncertain
content appears, stop and coordinate with its author; do not commit it under
another attribution. Serialize same-file edits, or use separate worktrees and
integrate each author's commit, when the diff cannot be safely separated.
Reviewers retain the existing one-write and self-commit rules.

When a sweep is confirmed after a commit, record one `occurred` incident per
commit and affected path in the coordination incident tracker, with commit,
path, evidence and discovery date; do not infer authorship from overlapping
claims alone. Define a distinct `same-file-sweep` class in the tracker guidance
so the existing gate can count confirmed events in its rolling window. Record
prevented or uncertain overlaps separately without presenting them as confirmed
sweeps. Reconcile the known `5094a977` event once, without overwriting the local
tracker or treating its absence as proof. The gate remains advisory; its output
must identify that counts depend on reports and cannot detect unreported events.
No new automatic author-attribution detector or change to claim release is
proposed.

## Rationale

A diff and the people who wrote it can establish a sweep; a path claim cannot
identify ownership of individual lines. The check addresses the cause before
commit and the incident row lets the existing recurrence mechanism count a
confirmed failure. It costs a diff read and occasional coordination, rather
than a new provenance system. It cannot detect every unreported sweep.

## Alternatives considered

Automatic detection based on another active claim would flag legitimate
commits and miss absent, stale or released claims. Doing nothing leaves both
misattribution and the misleading zero-count interpretation unaddressed.
Isolating every edit in a worktree would provide stronger separation but impose
that cost even when no shared path is at risk.

## Documentation / doctrine surface

Put the shared-tree prescription in `AGENTS.md` and the corresponding adopter
coordination guidance in `doctrine/coordination.md` and its installed owner if
applicable; determine the exact installed route during planning. Define the
incident class in the tracker guidance and clarify the gate's reporting limit
at its user-facing output/documentation. Follow `docs/DOCUMENTATION_PLAN.md`.

## Evidence / verification plan

### Tests required

Search for readers and tests of each changed file and gate output. Exercise the
real gate with a fixture containing two in-window confirmed sweep rows and a
prevented row: it suggests the class at threshold two, does not count the
prevented row, and says reporting is incomplete. Check a known positive control
before relying on a negative result. Verify a shared-file scenario with two
authors' changes is identified by the prescribed diff inspection and that a
separate-author commit is not labeled a sweep. The plan maps exact existing test
nodes and installed paths before implementation.

### Examples / smoke checks

Run `python scripts/claim_check.py` on changed documents and
`python scripts/check_cairn.py`, plus applicable neutrality and snippet gates.
The plan specifies scoped checks under the canonical interpreter; no full-tree
certification is implied.

#### Security preflight

N/A: no trust boundary added, moved, or widened; the advisory reporting change
is not an authorization or enforcement decision.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Withdraw or redesign if the inspection cannot distinguish the known incident
from a legitimate multi-author commit, if reporting creates duplicate events,
or if the count is represented as comprehensive despite unreported sweeps.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: standard. This changes coordination guidance and advisory
reporting, not the work-intent enforcement or an adopter executable contract.
