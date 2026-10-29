# Detect and record same-file commit sweeps

**Author**: Codex gpt-6.1-sol
**Status**: revising
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

## Review -- Codex gpt-6.1-sol -- 2026-10-29

```
Reviewed commit: 86a1b18e98b0accdeed295b2095a3c666f209465
Target: opening proposal
Prior findings: none
Assurance path: standard (declared; disputed below)
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Foundations**:

1. **Should this happen as framed?** The lightweight check and honest reporting are worthwhile, but the counting unit and prevention claim need correction before acceptance -- Proposal and Rationale above; `tools/evolution_infer.py::evaluate_tracker`.
2. **Best alternative.** Extend the existing diff read and require same-file serialization during inspection through commit; retain manual incident reporting rather than build attribution machinery or isolate every edit -- `AGENTS.md` > Git and commit workflow; `doctrine/coordination.md` > Tier 1 and Tier 2.
3. **What would show it wrong.** One multipath sweep satisfying recurrence, staged foreign text escaping inspection, or another writer changing the file after inspection would invalidate the claimed protection -- Proposal above; `tools/evolution_infer.py::evaluate_tracker`; `doctrine/coordination.md` > Tier 1.

The strongest benefit is restoring the author's ability to see what they are
signing while making an advisory zero count honest. Claims cannot establish
line authorship; the proposal correctly rejects that shortcut. The deferred
shared-write row records an earlier August observation and the October event,
so the proposal is not resting solely on one incident (`dev/PLANNING.md` >
Deferred). Keep this an extension of existing commit inspection: a second
routine inspection would add cost without a new instrument.

**R1 -- Blocking: the assurance declaration contradicts the template.**
The proposal explicitly edits `doctrine/coordination.md`, but declares standard
assurance, ordinary-only reviews and an N/A security preflight. The current
`dev/proposals/_template.md` > Assurance path explicitly makes governing
doctrine mandatory high-assurance and a Security-Review trigger. Satisfier:
revise the declarations and answer the preflight for the actual surface;
this usual pass discharges no Security Review.

**R2 -- Blocking: one incident can become recurrence.** “One incident per
commit and affected path” produces two `occurred` rows for a single commit
sweeping two paths. `evaluate_tracker` counts rows, so threshold two is met
without a second failure. Satisfier: define one countable event per sweep
commit with affected paths attached, or an equivalent deduplication contract;
add a two-path-one-commit negative case alongside the two-commit positive
case. Separate occurrence date from discovery date so a late report does not
silently move an old incident into the rolling window.

**R3 -- Blocking: define the complete diff and its stable interval.** The
existing plain `git diff <paths>` omits staged text, although a path commit
collects that text too. Inspection also precedes commit: another writer can
append afterward. Satisfier: prescribe inspection against HEAD for tracked
candidate paths (and direct inspection for new files), start agreed same-file
serialization before inspection and retain it through commit, and test staged
foreign content plus an intervening writer. Describe residual noncooperation
as an advisory limitation. Author testimony or recorded provenance must
confirm attribution; a diff alone only shows content.

**R4 -- Non-blocking: minimize incident evidence.** Prefer commit/path and
confirmation references; avoid copying private chat, credentials or unrelated
uncommitted text into a committed tracker. Satisfier: state the evidence
minimum and local-versus-published destination in tracker guidance.

**Covered**: claims/design/failure modes (R2–R3, gate evaluator); production
entry-point intent (Evidence plan); consistency/drift/lifecycle (R1,
coordination doctrine); scope and satisfiers (alternatives, R1–R4). **Not
covered / low confidence**: no live concurrency experiment, privacy audit,
implementation tests or scientific calculation; no broad suite run.

## Review -- Codex GPT-6 Security reviewer -- 2026-10-29

```
Reviewed commit: 77010b3edc70c57f0e8272df6eeb1ac39632a8f1
Target: opening proposal and usual review
Prior findings: usual R1–R4 considered, not closed
Assurance path: standard (declared; incorrect for the proposed doctrine edit)
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE

**Foundations**:

1. **Should this happen as framed?** Improve the existing commit inspection and
   report confirmed failures, but do not present a momentary diff read as
   protection across a shared-write interval --
   `doctrine/coordination.md:68` and Proposal above.
2. **Best alternative.** Agreed serialization of the affected file from the
   existing inspection through commit, with separate worktrees when that cannot
   be maintained; keep confirmation and reporting human-operated --
   `doctrine/coordination.md:105` and Alternatives above.
3. **What would show it wrong.** A post-inspection append is swept, a legitimate
   authored integration is called a sweep without confirmation, or one commit
   meets recurrence through multiple path rows -- usual R2–R3;
   `tools/evolution_infer.py:222`.

This addresses attribution integrity without giving a claims database authority
it cannot justify. The data remain project-supplied: the diff shows changed
text, claims show declared intent, and neither identifies who wrote a line.
The existing gate is a read-only suggestion, not permission to alter doctrine
(`tools/evolution_infer.py`, module docstring). Preserve that separation.

**S1 -- Blocking: declare and account for the actual security surface.**
Concur with usual R1. Editing governing doctrine requires high assurance and
Security Review regardless of whether this particular mechanism enforces
anything. Answer the five preflight questions for the human classification,
incident recording and advisory output: identify supplied evidence, deliberate
misclassification controls, triggers, uncertainty handling and the remaining
noncooperating-writer capability. Satisfier: corrected declarations and written
preflight under `dev/proposals/_template.md` > Assurance path / Security preflight.
This pass does not clear the obligation while those answers are absent.

**S2 -- Blocking: close the inspection interval and confirmation gaps.**
Concur with usual R3. Inspect the tracked candidate against HEAD, covering
staged and unstaged text, and inspect new files directly. Agree serialization
before inspection and retain it through commit; an active claim alone is not
that agreement. If the inspected bytes change, inspect again before committing.
Uncertain authorship remains uncertain until confirmed by an author or recorded
provenance. Satisfier: the revised prescription and the staged-content,
intervening-write and legitimate-integration controls requested in R3. Keep
noncooperation an explicit residual limitation, not a new automated detector.

Concur with R2's event identity and occurrence-date correction: the evaluator
counts rows without commit deduplication (`tools/evolution_infer.py:233`).
Concur with R4's evidence minimization: commit/path plus a short confirmation
reference suffices; do not publish private conversations, sensitive file content
or unrelated uncommitted text. State the local reporting home and any committed
summary separately. No transcript collection or extra routine is needed.

Covered: claims, production path and fail-closed limits (gate module and
`evaluate_tracker`); design/reuse/drift (coordination doctrine and S2);
lifecycle, scope and satisfiers (S1–S2, R2–R4). Not covered / low confidence:
no concurrency experiment, independent authorship confirmation of the historical
incident, implementation verification or privacy inventory; no suite run.
No scientific result is involved.
