<!-- cairn-internal-ref-allow: doctrine/plans.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- Forward-reference paths this plan creates; they materialize in Chunks A/E. -->
<!-- claim-check-allow: bootstrap/tests/_gate_preflight.py, bootstrap/tests/test_gate_preflight.py -->

# Plan: a reviewed pre-flight for the supervised gate re-anchor (Phase 0)

**Source proposal**: `dev/proposals/archive/2026-08-03-claude-gate-reanchor-preflight.md`
**Status**: open
**Plan review**: required(**External**, security lens) — carried from the proposal header and ratified at Decision. Additionally, **first use is gated on a focused External security review of the exact initial checker bytes and the recorded invocation** (SR6 / SR9); the Decision explicitly does *not* prospectively bless those bytes.
**Last update**: 2026-08-03
**Opened**: 2026-08-03

## Source proposal

Accepted 2026-08-03 after three External Security Review rounds (SR1-SR10) and
two author-initiated revisions. Phase 0 of `bootstrap/REANCHOR_RUNBOOK.md` is a
Maintainer-only trust-root ceremony that the runbook specifies in prose and no
tool verifies; the gap was filled twice by a disposable scratchpad script, which
returned a wrong answer on its second use and whose unsequenced three-step
handoff advanced `refs/cairn/gate-anchor` to a commit containing no blessing.
The Decision accepts a **trusted-contributor** threat model for Cairn's own trust
root, **as dated** (single-maintainer, as of 2026-08-03), with a mechanical
committer-identity tripwire as its expiry. This plan executes that decision; it
does not re-litigate it.

## Proposed paths

Proposed paths:
- `bootstrap/tests/_gate_preflight.py` — the checker; lands in Chunk A.
- `bootstrap/tests/test_gate_preflight.py` — its behavioural test; lands in Chunk E.

## Scope

Executes the design as revised through Round 5. **Out of scope, fenced
explicitly:** OS containment for the evidence stage (SR7 — deferred by Decision
under the accepted threat model, with a named upgrade path); a single-use nonce
or consumption ledger (SR10 — deferred to a wider threat model); shipping the
mechanism to adopters (proposal alternative 4 — `bootstrap/tests/` is not
installed, verified 0 entries under `scaffold.py --manifest`); and any change to
`_gate_reanchor.py`'s Stage A / Stage B contract, which this plan reads but does
not modify.

**No gate re-anchor is required by this plan's own work.** Every file it adds is
new under `bootstrap/tests/`, which reads as `FROZEN-NEW` (allowed and recorded),
and pytest collection only grows. No `FROZEN-MODIFIED` entry is produced. This is
a live invariant to re-check at Chunk E, not a carried-forward claim.

**Bootstrap ordering — the one genuinely awkward sequencing constraint.** The
accepted entry point executes the checker *from the anchor*. On first use the
checker is not in the anchor, because it has just been written. So: Chunks A-F
land the code and docs; Chunk G is a Maintainer-only step that reviews the exact
bytes and performs **one manual Phase 0 blessing by the existing runbook** — which
is what puts `_gate_preflight.py` into the anchor. Only from the *next* ceremony
onward does the anchored invocation apply. The plan must not pretend otherwise,
and Chunk G must not be performed by an implementing agent.

### Documentation / doctrine surface

`bootstrap/REANCHOR_RUNBOOK.md` gains the pre-flight step, the verbatim anchored
invocation, the enumerated residual trust set, and the two non-observable expiry
triggers (Chunk F). `CHANGELOG.md` gets an `Unreleased` entry at finalization
(Chunk H). `dev/PLANNING.md` gains the expiry row **in this plan-open commit**,
not at archive — per the Decision, so the expiry outlives the proposal's
readership. **No file under `doctrine/`, no `AGENTS.md` change, no shipped
template, no install-manifest entry.**

## Sequence

```
A -> B -> C -> D -> E -> F -> [G: Maintainer-only] -> H
```

### Chunk A -- the read-only checker

`bootstrap/tests/_gate_preflight.py`, `check` subcommand. Read-only against the
repository: no file written into the tree, no commit, no ref moved.

| # | Check | Disposition |
|---|-------|-------------|
| A1 | Canonical interpreter is 3.13.x | refuse |
| A2 | No uncommitted **tracked** changes | refuse |
| A3 | Frozen-surface membership validated against `git ls-files --stage`: stage-0 regular blob mode required; symlinks, submodules, ignored-but-globbed, and absent-from-index all refuse. Untracked enumeration **includes ignored entries** (SR5) | refuse |
| A4 | Stage-B authority-module identity vs the anchor. **Changed refuses with `REVIEW REQUIRED` and emits no bundle on any path** (SR3) | refuse |
| A5 | Record the six sha256 (Phase 0 step 1 audit trail) | report |
| A6 | Produced manifest pins equal the independently-recorded hashes | refuse |
| A7 | Manifest interpreter pin is 3.13.x | refuse |
| A8 | Live scope: files changed, frozen modified/added/**removed**, collection delta. Any removal or collection shrink refuses | refuse |
| A9 | Anchor ancestry; `anchor == HEAD` refuses (nothing to bless, or a half-run left it there) | refuse |
| A10 | **Committer-identity tripwire** — every commit in the anchor→HEAD range carries the Maintainer-recorded committer identity. Silent at 666/666 as_of 2026-08-03; fires when commit authority widens (the dated posture's expiry) | refuse |

`--trusted-repo` / `--trusted-ref` are accepted and threaded through to the
existing `_gate_manifest.verify` path **even though this repository passes
neither** — the Decision's constraint, so external anchoring stays a
configuration change rather than a retrofit.

### Chunk B -- the non-authoritative evidence stage

Candidate collection moves out of `check`'s read-only guarantee into an
explicitly-named **evidence** stage: a repository-less tree with the Stage A
scrub (`_gate_reanchor._scrubbed_environ`, which its own docstring calls
`contained, not hermetic`). Its residual — filesystem reachability, process
creation, network — is printed by the tool itself, not only documented. **No
containment claim appears anywhere in code, output, docs, or tests** (SR7).

### Chunk C -- the digest-bound bundle

A machine-readable bundle binding checked HEAD, observed anchor,
candidate-manifest digest, and drafted-message digest. Includes the drafted
commit message built from computed values: the six authority hashes, the observed
anchor, the checked HEAD, the prospective manifest digest. **Not** the resulting
`P` SHA — a message cannot contain its own SHA (SR4). Recovery mode accepts a
Maintainer-supplied `last_legitimate_anchor` and discloses any erroneous current
ref separately, never claiming to have inferred legitimacy.

### Chunk D -- `apply`

Separately reviewed; requires explicit Maintainer confirmation. Revalidates every
binding against live state and refuses on any drift. Constructs the commit object
with plumbing and verifies its parent, diff, and manifest-blob digest **before
any ref moves**, then advances branch and gate anchor in **one expected-old
`update-ref --stdin` transaction** (SR8). On abort: no ref moves, no success
reported, index residue reported explicitly rather than cleaned up silently. The
bundle is **revalidate-and-confirm, not mechanically single-use** — no
non-replayability claim (SR10).

### Chunk E -- tests

`bootstrap/tests/test_gate_preflight.py`, driving the CLI in sandboxed temp repos
(`test_gate_reanchor.py`'s `_two_stage_repo` is the model). One test per refusal;
each shown non-vacuous by mutation. Named explicitly:

* untracked files **outside** the surface do **not** refuse (the 2026-08-03 defect, pinned);
* an ignored `.py` inside the surface refuses; a tracked symlink refuses (SR5);
* a changed authority module emits **no bundle on any path** (SR3);
* the committer-identity check fires on a foreign committer and stays silent on the current single-identity history;
* `apply` refuses when HEAD moved after `check`; a stale anchor aborts leaving **both** refs unmoved; a constructed-but-unblessed commit never reaches the branch;
* altered worktree invocation text, altered worktree checker bytes, and an altered candidate hash record cannot influence the executed anchored bytes (SR9);
* the drafted message contains all six hashes, the observed anchor and the checked HEAD — and **no** self-referential SHA field.

**Deleted, deliberately:** any test asserting candidate collection cannot reach
the real repository, and any asserting mechanical non-replayability. A test
asserting a property the mechanism does not provide is worse than no test.

### Chunk F -- the runbook

`bootstrap/REANCHOR_RUNBOOK.md` Phase 0 gains: the pre-flight step; the **verbatim
anchored invocation** (`git archive refs/cairn/gate-anchor bootstrap/tests | tar
-x`, then the Maintainer-recorded interpreter with `-E -s`), with the instruction
to obtain it from `git show refs/cairn/gate-anchor:bootstrap/REANCHOR_RUNBOOK.md`
rather than the worktree; the enumerated residual trust set ending at write access
to the anchor ref; and the two non-observable expiry triggers.

### Chunk G -- first-use bootstrap (Maintainer-only; NOT an implementing-agent act)

Neither `check`, nor `apply`, nor the blessing below is this plan's or any
implementing agent's act. The implementer's job ends at identifying the candidate
commit and stating the expected scope.

1. A **focused External security review of the exact bytes** of `_gate_preflight.py`,
   its dependencies, and the recorded invocation text.
2. The Maintainer **records the reviewed hash set** out of band, with the runbook
   noting who compared them and at which immutable commit.
3. **One manual Phase 0 blessing by the existing runbook** — this is what puts the
   checker into the anchor and makes the anchored invocation available from the
   next ceremony onward.

### Chunk H -- CHANGELOG

`Unreleased` / `Fixed` entry at finalization, cross-linking the archived proposal.

## Acceptance criteria

**Binding, from the Decision and the three security rounds** — these are
conditions, not preferences:

* **No containment claim** anywhere in code, output, docs, or tests (SR7).
* **Entry is the anchored copy**; no worktree process is described as checking
  its own bytes, and there is **no launcher artifact** (SR6 / SR9).
* **Changed authority modules emit no bundle on any path** (SR3).
* **No ref moves before the commit object is constructed and verified**; branch
  and anchor advance in one expected-old transaction (SR8).
* **No self-referential SHA** and no claim of inferred anchor legitimacy (SR4).
* **Frozen membership is index-validated**, not filesystem-only (SR5).
* **The committer-identity tripwire** is silent on the current history and fires
  on variance (the dated posture's expiry).
* **`--trusted-repo` / `--trusted-ref` are threaded through** even while unused.

**Other criteria:** full suite green under the canonical `lhm` interpreter
(3.13.13) with collection grown by exactly the new nodes; `_gate_manifest.py
verify` reporting no `FROZEN-MODIFIED` attributable to this plan; `claim_check`
and `check_cairn` clean.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants.** `check` never mutates the repository — enforced by a test
  snapshotting `git status --porcelain`, `HEAD`, and every `refs/cairn/*` before
  and after a full run. The bundle's bound state equals the state `apply` acts on
  — enforced by revalidation and refusal on drift.
* **Failure modes.** All refusals **closed** (non-zero, no actionable output). A
  checker crash is closed by default — deliberately *not* fail-soft, unlike the
  post-commit hook. The evidence stage's host-access residual is **open and
  accepted** by Decision, printed rather than contained.
* **Edge cases.** Absent anchor ref (first-ever Phase 0 — refuse with a runbook
  pointer); `anchor == HEAD`; orphaned anchor; zero frozen changes; frozen file
  removed; collection shrunk; off-canon interpreter; paths with spaces and shell
  metacharacters. Out of scope: concurrent Maintainers.
* **Public-path → test mapping.** `check` and `apply` each exercised through the
  CLI, not by importing internals, in `bootstrap/tests/test_gate_preflight.py`.
* **Known omissions.** The checker cannot verify the six authority modules are
  *correct*, only *unchanged since the anchor*; a compromised module already
  anchored passes. That is Phase 0 step 1's job and stays human.

## Verification

* `python -m pytest bootstrap/tests` under `/Users/kendal30/conda_envs/lhm/bin/python` (3.13.13).
* `python bootstrap/tests/_gate_manifest.py verify --anchor-ref $(git rev-parse refs/cairn/gate-anchor)`.
* `python scripts/claim_check.py <changed .md>` and `python scripts/check_cairn.py`.
* Mutation-test every refusal: remove the check, confirm the test fails, revert, `diff` for byte-identity.

## Plan review

*Filled in after the required External (security lens) read.*

## Code review

*Filled in after implementation commits land (Chunks A-F, H).*

## Lasting-truth migration

*Filled in at archive time. Per the archive-preconditions rule, this plan
archives only once every deferred follow-up has a durable home outside it — the
SR7 containment upgrade, the SR10 nonce/ledger, and the external-anchoring
upgrade are all named in the Decision and belong on `dev/PLANNING.md` before
archive if not already homed.*

This section is append-only once written.
