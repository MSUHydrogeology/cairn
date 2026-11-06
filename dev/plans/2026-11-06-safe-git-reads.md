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
no-Git exception. A High-tier owner must resolve and document the remaining in-contract
mechanisms for verified-buffer loading, enclosing-worktree exclusion before
probing, and Windows process/descendant cleanup before Low-tier execution.
New boundary questions also require High-tier judgment; no outcome is waived.

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
uncertainties. The recorded native Windows VM is available, but old-Git
availability and x64 compatibility on ARM64 remain unproven. First acquire
[MinGit 2.44.0 for Windows](https://github.com/git-for-windows/git/releases/tag/v2.44.0.windows.1)
into a disposable local VM directory, without system installation or PATH
changes. Verify `MinGit-2.44.0-64-bit.zip` SHA-256
`ed4e74e171c59c9c9d418743c7109aa595e0cc0d1c80cac574d69ed5e571ae59`,
then run its actual `--version` and establish compatibility below 2.45 before
claiming that capability. If this route fails, a High-tier owner selects a
credible alternative; real old-Git evidence remains required. Coordinate shared
session/caller edits with active owners; no unfinished plan is a prerequisite.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C0 | Resolve and document the three remaining boundary mechanisms; establish old-Git capability or a credible alternative | Usual and Security plan reviews; High-tier owner before Low execution | Concrete in-contract design choices and evidence route |
| C1 | Implement and deliver bounded helper and pre-import bindings | C0 | Mirrored helper, fixed-source pins and installed-layout controls |
| C2 | Migrate every inventoried ordinary reader and repair N1–N3 | C1 | Preserved capabilities, caller-specific failure handling and real-entry regressions |
| C3 | Complete iteration, adversarial and platform evidence, then code reviews and final verification | C1–C2; code reviews read iteration evidence; Boundary B follows review and fixes | Per-member mutation evidence, both reviews and final wide Boundary B |

## Acceptance criteria

**C0.** Before Low execution, a High-tier owner records concrete choices for
verified-buffer loading, enclosing-worktree exclusion before any probe and
Windows descendant cleanup, within the accepted contract. Establish the named
old-Git capability or a High-selected credible alternative; a mock or skipped
check is not evidence.

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
per-launch revalidation, closed environment and standard input (`DEVNULL`),
bounded noninteractive offline read forms and cleanup, including version/config,
filter-safe status and sweep
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
descendant, closed-standard-input and cleanup cases through real entry points.
Complete these and affected iteration checks before code review; review fixes
precede final Boundary B. Record real native Windows and real old-Git
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

Complete mapped iteration and adversarial/platform evidence before code review,
so reviewers can read it; address review fixes before Boundary B.
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

## Plan review -- Codex GPT-6.1 Terra (Medium) -- 2026-11-06

Reviewed commit: d55fe688659839bc49c4af060d216aff22aecf46

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised
**Verdict**: Revise before implementation.

**Foundations**

1. **Should this happen as framed?** The scope preserves the accepted migration, binding, N1–N3 and required evidence, but two sequencing prerequisites need resolution before its independent finish is credible -- plan Scope, Sequence and C3; source Decision `05ea5d90`.
2. **Best alternative.** Keep one helper and existing caller test homes, but identify the real evidence environments and place adversarial iteration before code review; this keeps the same outcomes without another framework -- plan Reuse and Verification; source proposal's delivery and test tables.
3. **What would show it wrong.** A real entry point surviving its separate routing mutation, a failed read reported clean, or inability to demonstrate the required real-platform controls would disprove delivery -- plan C2–C3 and source proposal Tests required.

**F1 -- blocking: real old-Git prerequisite is not established.** C3 requires real old-Git results, but Sequence lists only uncertainty; the source explicitly says those checks were not run and identifies no available installation or acquisition route. A prior native Windows VM is evidenced in `dev/plans/2026-11-05-architecture-and-reuse.md` under C1 native Windows capability; that is not old-Git evidence. Identify an available real old-Git environment or a credible, authorized way to obtain one, including constraints and uncertainty; keep missing evidence open. Do not substitute a mock or waive the Decision.

**F2 -- blocking: review precedes its evidence in the chunk gate.** C3 makes both code reviews a gate for completing adversarial and platform evidence, while Verification says code review falsifies the implementation and the governing rules require it to read iteration evidence. Arrange implementation and required iteration/adversarial evidence before code review, then review fixes and final Boundary B afterwards; preserve all controls.

**Advice:** Make closed standard input explicit for every read launch and test it at a real entry point. Existing upgrade `_run_git_sterile` uses `DEVNULL`; a noninteractive prompt setting alone does not establish that inherited input is unavailable.

**Coverage:** Read the committed plan, template, full operative source and Decisions, existing upgrade launcher, recorded Windows capability and reuse seams. The source tables remain normative for budgets, binding and caller policies. Did not run implementation tests, mutate members, establish old-Git availability, execute Windows, or assess the separate Security obligation. Over target to distinguish the two prerequisites and evidence. **Elapsed:** unknown; **tokens:** unknown.

## Plan review -- Codex GPT-6.1 Sol (High) -- 2026-11-06

Reviewed commit: a589416435e7f2d66b2e1e503a54c3bdc1a8a164

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: Revise before implementation.

**Foundations**

1. **Should this happen as framed?** Yes, retaining complete migration, pre-import binding, failure translations and separate anchored authority; sequencing and the remaining design owner need correction -- plan C1–C3; source Decision `05ea5d90`, delivery/binding and caller-policy tables.
2. **Best alternative.** Keep the small helper, existing delivery and test homes, resolving remaining security design within C1 before mechanical migration; this delivers the same outcomes without another framework -- plan Reuse; source Alternatives considered.
3. **What would show it wrong.** Run each member's real-entry mutation: any executed marker, surviving descendant, false-clean failure or lost capability disproves delivery; native Windows and below-floor Git must demonstrate their controls -- source Tests required; plan C3.

**SRP1 -- blocking: assign unfinished boundary design to High.** Scope requires High judgment only for questions “beyond the accepted contract.” The contract also leaves mechanism choices for verified-buffer loading, enclosing-worktree exclusion before probing, and bounded process/descendant cleanup on Windows. Accepting their outcomes does not settle those novel security choices. Name a High owner/gate to resolve them before Low execution, retaining the existing contract and required reviews. Medium planning of the accepted contract is not itself a floor violation. Close in Scope/Sequence; do not invent authority or remove outcomes.

Concur with ordinary F1/F2 and closed-stdin advice. The [official 2.44 release](https://github.com/git-for-windows/git/releases/tag/v2.44.0.windows.1) identifies `MinGit-2.44.0-64-bit.zip` and its SHA-256. Acquisition into a disposable VM directory, publisher-checksum verification and actual version/compatibility checks form a credible acquisition-first gate. Nothing was downloaded or executed; Windows ARM64 compatibility and actual old-Git controls remain unproven. Missing evidence keeps implementation open.

**Coverage:** Read the committed plan, template, full source/response/Decisions, upgrade launch and sweep validation seams, and recorded Windows capability; opened the official release. No implementation tests, mutations, package execution, native Windows, private data or trust operations. Claim check covered this isolated review candidate only. **Elapsed:** unknown; **tokens:** unknown.

## Plan review response -- Codex GPT-6.1 Terra (Medium) -- 2026-11-06

- **F1 accepted:** Sequence and C0 name an acquisition-first official MinGit
  route, checksum, actual version/compatibility check and High-owned fallback;
  no old-Git capability has yet been measured.
- **F2 accepted:** C3 and Verification place iteration and adversarial/platform
  evidence before code review and final Boundary B after review fixes.
- **Closed-input advice accepted:** C2 and C3 require `DEVNULL` and a real-entry
  control.
- **SRP1 accepted:** Scope, C0 and its criterion assign the three remaining
  in-contract security mechanisms to High before Low execution.

No accepted scope, evidence or review obligation is removed. **Elapsed**:
approximately 2 minutes. **Tokens**: unknown.
