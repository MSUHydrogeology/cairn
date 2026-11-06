# Plan: One safe boundary for Git reads

**Source proposal**: dev/proposals/archive/2026-11-04-codex-safe-git-reads.md
**Author**: Codex GPT-6.1 Terra (Medium)
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-06
**In brief**: Give ordinary repository reads one verified safety boundary so untrusted projects cannot run programs or turn failed checks into clean results.

## Source proposal

The delegated Sol Decision `05ea5d90` accepted the complete heavy proposal,
including N1–N3 and its delivery fence. The scheduling Decision `67e2c63b`
authorizes this prerequisite plan while architecture work continues. Dependent
Git views wait for this plan's verified boundary; this plan does not wait for
architecture, release or a human trust operation.

## Scope

Proposed paths:
- `templates/skills/_lib/git_read.py`
- `tools/git_read.py`

Deliver the accepted small standard-library helper, byte-identical at
`templates/skills/_lib/git_read.py` and `tools/git_read.py`, through the
existing unconditional skill mapping and install/upgrade contracts. Route all
ordinary readers named in the source proposal: upgrade, install and lockfile;
session; intent conflict and both generated hooks; content runner and audit
preflight; portable sweeps and its shim; link, snippet and self-checkers;
measurements, gauge, tier selector and legacy report. Preserve each caller's
parsing, capability and failure policy, and retire duplicated launch loops.
The accepted proposal's delivery/binding and caller-policy tables are normative
for every member. Keep hooks-path installation, merge-file, privileged gate,
release, signing, re-anchor and publication runners separate as specified.

Bind trusted helper bytes before execution in source and installed layouts,
including dispatcher, audit before injection, direct content/sweep, other first
importers and shim; pin reviewed bytes in trusted caller source, enforce required
lock records and execute the verified buffer. Never use target-selected code,
CWD, cached unverified modules or candidate-adjacent digests as authority.
Keep anchor-session extraction self-contained. Preserve fixed diagnostic policy,
caller-specific empty/absent/failure translations and the pre-confirmation
no-Git exception. New boundary questions beyond the accepted contract require
High-tier judgment; surface concrete gaps rather than inventing authority.

**Reuse.** Search of `_run_git_sterile`, session `_git`, intent `_git_path`,
and `additional_immutable_paths` found existing upgrade, session, intent and
dispatcher seams. Reuse guarded installation, sweep executable revalidation and
adapter shim, and existing caller test homes rather than a registry or framework.

### Documentation / doctrine surface

Update `docs/tool-usage.md`, `bootstrap/UPGRADE.md` and domain-local
`bootstrap/SAFETY.md` as behavior changes; retain governing AGENTS obligations
and mirror any necessary operative clarification in the shipped template.
No lifecycle change is authorized.

## Sequence

The existing installer, sweeps, source callers and test homes are available.
Estimate 5–10 workdays including reviews and verification; full migration,
per-member controls, native Windows and real old-Git availability are material
uncertainties. Missing named evidence remains work, not a waived check. Coordinate
shared session/caller edits with active owners; this plan is independently
finishable without another unfinished plan.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Implement and deliver bounded helper and pre-import bindings | Usual and Security plan reviews | Mirrored helper, fixed-source pins and installed-layout controls |
| C2 | Migrate every inventoried ordinary reader and repair N1–N3 | C1 | Preserved capabilities, caller-specific failure handling and real-entry regressions |
| C3 | Complete adversarial and platform evidence, reviews and verification | C1–C2; usual and Security code reviews | Per-member mutation evidence and final wide Boundary B |

## Acceptance criteria

**C1.** Each trusted importer resolves only its fixed delivery root, rejects
missing, linked/reparse, nonregular, oversized or mismatched helper bytes and
executes the once-read verified buffer before any probe. Dispatcher binds all
six apparatus records; audit binds before injection; direct self-audit checks
the fixed record; external target and target CWD cannot supply helper authority.
Verified copies, pins, install/upgrade records and shim agree. Positive-control
execution markers prove missing records, tamper, links, cache substitution,
pin removal and audit-order mutations are detected. Jointly rewritten trusted
local code/records, malicious host Git and same-user races remain stated limits.

**C2.** The full source inventory uses validated off-tree host Git with
per-launch revalidation, closed environment, bounded noninteractive offline
read forms and cleanup, including version/config, filter-safe status and sweep
screen/shim; reduced sweep mode remains Git-free. Revision and supplied paths
are safe data. Markdown discovery enumerates and filters rather than treating
`*.md` as a literal selection; real link, snippet and delegated self-checks
find planted defects with and without the literal-wildcard decoy and refuse an
empty selection. Failure cannot appear clean or as measured zero: every source
policy row distinguishes completed empty from failed/absent/incomplete, with
fixed reasons and only labeled bounded non-secret data. N1 post-confirmation
startup failures, including later groups, refuse apply/finalize without byte
changes and advise stage; the intentional pre-confirmation no-Git case remains.
N2 linked-worktree and N3 version-only hang controls detect their mutations.

**C3.** Each inventoried real entry point and routing member has a separately
mutated control with a demonstrated positive tripwire. Exercise executable and
PATH/symlink substitution, inherited environment, hooks, filters, fsmonitor,
signatures, missing objects/remote helpers, options/paths, timeout, overflow,
descendant and cleanup cases. Record real native Windows and real old-Git
results; object reads retain the 2.45.0 floor and older discovery is permitted
only with demonstrated prevention. Both reviews and all mapped checks pass;
unknown, failed or missing required evidence keeps implementation open.

## Scope delta

**Scope delta**: preserved. No reader, check or accepted outcome is transferred
to architecture or deferred.

## Verification

Boundary A: before edits map imports, consumers and `python tools/test_tiers.py
for <changed paths>`; run its selected tests and standing prose gates. Extend
existing upgrade edit-check, session, interpreter binding, intent, security
stack, portable sweep, security verification, doc-drift, self-check, count and
reference parity homes, plus nearest existing gauge/report/tier owners. Use
actual shipped layouts and entry points; retain the source proposal's detailed
F1/F2, SR1–SR3 and N1–N3 controls. Run each routing mutation in an isolated
copy and summarize reproducible evidence, not a new ledger. Check synthetic
forged advice, controls and secrets at real output sinks. S2 mutations run in
C1–C3; S3 is triggered by these existing real-entry tests and adopter commands.

Boundary C: independent code review falsifies the committed implementation;
separate Security Review is required. Boundary B: after reviews, run wide on a
clean unchanged final commit under canonical Python 3.13.x: all mapped
iteration and integration/workflow tests, installed public paths, required
security controls and standing claim, link, snippet and neutrality gates.
Record SHA/range, interpreter, pre/post state, commands and counts, elapsed,
non-pass dispositions, omissions and an evidence-qualified benefit-versus-effort
sentence. An expected reviewed engine AST mismatch remains unpassed pending a
separate Maintainer baseline operation; unexpected drift and integrity failures
remain implementation work. No certification, signing, ref movement or release
is authorized by this plan.
