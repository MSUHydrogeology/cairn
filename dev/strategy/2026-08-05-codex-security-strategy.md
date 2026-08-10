# Cairn security strategy: boundaries, evidence, and a finite path to release

**Author**: Codex (Strategy)
**Model**: GPT-5 (Codex)
**Date**: 2026-08-05
**Status**: living
**Type**: living-reference
**Surfaces this feeds**: `dev/PLANNING.md`; every security proposal and plan;
`SECURITY.md`; the v0.4.0 release-security register; future goodnight roadmap
scrubs

## Purpose

Cairn's security work has outgrown the finding-by-finding list that created it.
The original broad-look review's Theme 3 found six concrete failures. Most have
since shipped, and the remaining work now spans profile parsing, installation
containment, scanner coverage, security capabilities, provenance, release
evidence, identity, and trust-root ceremonies. Keeping those items under the
plans that discovered them has made the roadmap accurate but difficult to steer.

This document is the current organizing strategy. It does three jobs:

1. records what remains from Theme 3 and what has already shipped;
2. places every security-relevant roadmap liability -- including enabling
   studies, authority decisions, plans, proposals, and triggered residuals --
   into one of five stable clusters; and
3. supplies sequencing and stopping rules so new findings strengthen an
   existing boundary instead of automatically opening another scope.

The goal is practical: **help scientists build and release secure software
without turning security assurance into an endless ceremony.** Precision serves
that goal. It is not the goal by itself.

## Authority and update rule

This is a **living reference**, inline-revised as the portfolio changes.

* `dev/PLANNING.md` owns current task state, triggers, and which lifecycle
  artifact is active.
* Proposals and plans own design detail, evidence, review findings, and accepted
  residuals.
* This strategy owns the cluster taxonomy, cross-scope dependencies, threat
  posture, priorities, and the test for whether two findings belong together.

A roadmap item is security-relevant when failure could change what Cairn reads,
writes, executes, treats as authority, reports as assurance, or permits to move
through a release or deliberation ceremony. Placement under a general roadmap
heading does not put it outside this strategy. Coverage does not require every
item to become active implementation work: each receives one primary cluster
and a disposition to fix, gate on evidence, retain behind a trigger, accept as
a dated residual, or decline explicitly.

A broader product, documentation, or productivity task is not absorbed whole
merely because it touches one of these boundaries. Its owning artifact keeps
the non-security work; this strategy records the security condition that work
must preserve. For example, a scoped-test facility remains productivity work,
but cannot substitute for required security evidence without independently
demonstrated coverage.

Do not copy full plan designs here. Do not make `PLANNING.md` repeat them either.
At a lifecycle serialization point, update the task's cluster entry and link its
owning artifact. At a strategy refresh, remove completed work and retain only
the lasting boundary or accepted residual.

## Method

The initial synthesis read and cross-checked:

* Theme 3 and its B2 recommendation in
  [`2026-07-08-claude-broad-look-skeptical-review.md`](2026-07-08-claude-broad-look-skeptical-review.md);
* the current security-wave sequencing note;
* every open plan under `dev/plans/` whose contract is security-facing or whose
  review tier carries a security lens;
* the `release-security-orchestration` artifact and its External Security
  Reviews;
* every `dev/PLANNING.md` section for work meeting the security-relevance test,
  including lifecycle apparatus, lockfile, scaffold-engine, scan-coverage,
  release-authenticity, profile-parser, fork-advisory, byline, and gate-claims
  rows; and
* the implementing history for the six Theme 3 findings.

Claims marked implemented were checked against code or commits, not inferred
from a plan title. The living status is falsified if an active security artifact
has no cluster below, or a completed item remains represented as active work.

## Security objective and threat posture

Cairn protects five things:

1. **The scientist's tree** -- installation and upgrade must not read or write
   outside the named project, silently select a different profile, or execute a
   repository-controlled tool as authority.
2. **Scientific and project data** -- scanners and hosted/API checks must not
   leak source, credentials, findings, or identifiers through avoidable network
   or logging paths.
3. **The deliberation record** -- repository text must not impersonate trusted
   tool output, and identity/conformance checks must state whether they attest
   structure, authorization, or only presentation.
4. **The release trust chain** -- a verified release, the source tree used to
   build, the installed bytes, and the evidence attached to a release must not
   silently substitute for one another.
5. **The Maintainer's attention** -- a control that is too complex to run,
   habitually noisy, or described at greater strength than it delivers is a
   security liability.

The current Cairn-repository posture is **trusted-contributor, one Maintainer,
Maintainer-controlled machine**, dated 2026-08-03 where the gate-anchor Decision
records it. Candidate test collection executes code with best-effort isolation,
not containment. Signatures authenticate the key holder, not the process. The
gate re-anchor is revalidate-and-confirm, not nonce-backed single use. These are
accepted residuals with named expiry triggers, not universal Cairn guarantees.

Adopter-facing paths use a stronger posture where the inputs are not Cairn's:
profile files, lockfiles, module policy, repository paths, filenames, git
metadata, scanner output, URLs, and hosted-service responses are data until a
specific boundary validates them. A target under inspection never supplies the
trust material that declares itself clean.

## Design principles

### 1. Trust material comes from outside the candidate

A digest next to the bytes it covers is corruption detection, not tamper
evidence. A roster, lockfile, baseline, policy, or expected hash read from the
tree being judged cannot authenticate that tree. Every proposal names who owns
its oracle and why the subject cannot rewrite it.

### 2. Derive coverage from delivery, then challenge the derivation

Scanner targets come from the same manifest or registry that delivers the code.
Tests also use an independent on-disk or public-path oracle so a shared producer
cannot move subject and expected result together. New hand-maintained coverage
lists require a reason and a liveness check.

### 3. Optional capability may be incomplete; authority may not

An optional host tool can report `INCOMPLETE` when absent. Malformed policy,
unsafe path shape, altered authority material, scanner errors, credential
boundary violations, and a release check that silently skipped fail closed.
`NOT_APPLICABLE`, `INCOMPLETE`, `FINDINGS`, `DEGRADED`, and `CLEAN` stay distinct;
aggregation may never strengthen a child result.

### 4. Name the trigger at its real strength

Cairn has no CI. A Maintainer-run release command is described as
Maintainer-run. A suite test is described as suite-run. A human review is not an
authenticated identity check. Building automation merely to rescue overstated
prose is not a security strategy; either add the right trigger for an evidenced
need or correct the prose.

### 5. One boundary, one owner, one ceremony

Cluster findings only when they share all three: the same trust boundary, the
same implementation owner, and the same decisive verification path. Sharing a
word such as "security" or touching the same file is not enough. Conversely,
several plans that change one frozen scanner or one `_scaffold/config.py`
authority delta share a ceremony even when their user-facing capabilities are
different.

### 6. Security evidence must be able to fail

Every decisive check has a hazard-side negative control. Running the function
that supports a claim is not evidence about the call path that governs it.
Self-consistency tests are labeled as such; they do not stand in for an
independent oracle.

## Theme 3 migration

Theme 3 is superseded as a current work list. Its original items remain visible,
struck through in the broad-look note, while this table records their current
home.

| Theme 3 item | Current disposition |
|---|---|
| T3.1 -- Bandit/CI posture | **Resolved for the local release boundary.** `bootstrap/security_check.py` is the honest Maintainer-run trigger, binds evidence to committed repository bytes, and the live CI/floor vocabulary now matches actual enforcement. Human omission, host-process authentication, and tag binding remain accepted release residuals rather than false automation claims. |
| T3.2 -- release scan misses daily session code | **Implemented at `5c91c23`.** `scan_targets()` now unions the published install manifest and carries independent on-disk coverage. Remaining scan residuals are broader coverage questions under [VER-5], not the original omission. |
| T3.3 -- profile parser divergence and unknown keys | **Core implemented at `e7394cb`; residuals remain under [BND-1].** Unknown keys and parser divergence now refuse, while unknown module values, forward-compatibility cost, self-oracle tests, fallback precedence, and the totality claim remain open. |
| T3.4 -- R6 false-flags imported live code | **Implemented at `7066489`.** The AST reader now accounts for `from X import Y`; stale gate-manifest pins remain ceremony debt under [REL-3]. |
| T3.5 -- session-start claims read-only while writing | **Implemented at `b8d9e0b`.** Help and tests describe the mutating self-heal accurately. |
| T3.6 -- date-dependent test expires | **Implemented at `0bfba10`.** The CLI-path fixture is anchored to the real clock; injectable unit paths remain deterministic. |
| B2 unnumbered -- write-before-check / containment gap | **Still open under [BND-2].** The Class C adopter-tree writer inventory needs its own scoped proposal or explicit v0.4 disposition. |

## Cluster map

### [BND] Input, execution, and containment boundaries

**Question:** Can repository-controlled input choose what Cairn reads, writes,
executes, or treats as configuration authority?

**Current lifecycle owners**

* [BND-1] **Profile authority and upgrade reconstruction.** The implemented
  `profile-parse-fail-open` core plus its remaining G1/G2/G3/G5/totality rows;
  `_infer_init_lock_axes` guessing `human_team`; and the unmeasured other
  `base_hash` consumers. The next coherent proposal is a profile-authority
  consolidation, not one proposal per residual.
* [BND-2] **Adopter-tree write containment.** The `SECURITY_MUTATIONS.md` Class C
  orphan: six upgrade-family writers outside the common containment guard. It
  is a v0.4 backstop item and must not disappear behind another plan's scope
  fence.
* [BND-3] **Filesystem and executable shape.** Facade-loader symlink hardening,
  failed facade-import cleanup in `sys.modules`, side-door install surfaces,
  module destination renames/binary files, the local-interpreter check/use
  race, and the recorded `B607` PATH-resolution findings. Address on the next
  matching write/exec boundary, not through a generic hardening sweep.
* [BND-4] **Untrusted context rendering.** The archived
  `planner-line-semantics` and `agent-context-scrub` plans closed structural
  line manufacture in the orientation stream. The remaining boundary is
  narrower: framed relays from sibling tools and the pairs-only CRLF guard are
  clustered in `dev/PLANNING.md` rather than reopened as separate proposals.
* [BND-5] **Network client and hosted/API boundaries.** Plan
  [`api-web-security-modules`](../plans/api-web-security-modules.md) owns the
  shared hardened client, credential containment, loopback agent-facing checks,
  and Maintainer-only passive deployed checks. Its activation binding amendment
  belongs in [VER-3], not as a local exception.
* [BND-6] **Lockfile shape and version authority.** The deferred
  validate-on-read row owns strict `_LOCK_SCHEMA` interpretation, migration
  guidance, and the fail-open/fail-closed disposition before `upgrade` or
  `verify_integrity` relies on new schema semantics. It is distinct from
  [TRU-1]. BND-6 decides whether the input is structurally admissible; TRU-1
  decides whether its expected values come from an authentic source.

**Exit condition:** every adopter-controlled path or value reaches one named
validator before authority use; containment refusal cannot suppress a finding;
no repository-local executable is selected by ambient lookup; every deliberate
degrade is visible and typed.

### [VER] Verification capabilities and coverage

**Question:** What security evidence can an adopter gather, what material does
each check inspect, and can coverage silently narrow?

**Current lifecycle owners**

* [VER-1] **Content scanner character model.** Archived plans
  [`content-scan-detectors`](../plans/archive/content-scan-detectors.md) and
  [`separator-detection`](../plans/archive/separator-detection.md) have both
  landed and archived (SHIP-reviewed). They share one scanner and one test
  surface; the two files' frozen-file re-pin remains a pending
  Maintainer-supervised ceremony, batched across both plans.
* [VER-2] **Default adoption posture.** Archived plan
  [`default-security-stance`](../plans/archive/default-security-stance.md) makes
  `content-security` default-on, selects `python-security` only for a declared
  Python package, preserves exact explicit module lists, and keeps Cairn's own
  source scanner authoritative.
* [VER-3] **Activation and evidence aggregation.** Plan
  [`security-verification-activation`](../plans/security-verification-activation.md)
  owns the default-on narrowing dispatcher. It is the dependency root for
  portable and API/web capability admission. Before either registry entry
  lands, it must settle the reviewed closed binding mode for runner and policy
  material. Its typed result vocabulary is also the owner for constructive
  readiness: a security tool that finds a missing capability or unmet bar names
  the safe next action without strengthening `INCOMPLETE` into `CLEAN`.
* [VER-4] **Language and dependency capabilities.** Plans
  [`portable-security-sweeps`](../plans/portable-security-sweeps.md) and
  [`dependency-advisory-coverage`](../plans/archive/dependency-advisory-coverage.md)
  own one measured offline non-Python sweep and honest Python-distribution
  advisory coverage. The accepted dependency v1 stores no vulnerability
  baseline. Conda-native advisory coverage remains triggered research; Grype
  plus Syft is the first unevaluated candidate, and Cairn does not invent a
  conda-name-to-CPE authority map casually.
* [VER-5] **Coverage residuals.** Shape-based discovery of delivery registries
  (SC1), recorded LOW `B607` findings (SC2), the corrected monotonicity claim
  (SC3), the queued `shipped_executables()` authority unification, and Bandit
  allowlist liveness (SC5). [REL-2] is SC5's proposed owner.
* [VER-6] **Author-side security accounting.** Plan
  [`security-preflight-checklist`](../plans/archive/security-preflight-checklist.md)
  adds five design-time security questions to the proposal templates and a twin
  parity check. It guides review; it is not a substitute for a Security Review.
* [VER-7] **Cross-language security conformance.** The deferred
  language-neutral fixtures and golden vectors must pin security refusals,
  containment, lockfile shape, and exit semantics before a non-Python engine
  can claim parity with the Python reference. This is evidence for a future
  implementation boundary, not a reason to build that implementation now.

**Exit condition:** every shipped executable class has a derivation-backed scan
path; every capability states inspected material, network behavior, authority,
result vocabulary, and known blind spots; a removed finding or target cannot
leave a silent permanent exception.

### [TRU] Trust roots and provenance

**Question:** Which material is allowed to say "these are the expected bytes or
authorized identities," and how did the operator establish trust in it?

**Current lifecycle owners**

* [TRU-1] **Install-integrity anchor.** `verify_integrity.py` currently trusts
  the target's own lockfile. A successor must anchor the verbatim subset in an
  operator-trusted Cairn checkout, distinguish a legitimate fork from tamper,
  and define the self-checkout case. Cairn's own 38-file lockfile reconciliation
  is operational debt on this trust material: it remains a reviewed,
  freshly-remeasured batch rather than a hand-edited hash refresh.
* [TRU-2] **Fork-advisory source.** Plan
  [`fork-advisory-semantics`](../plans/fork-advisory-semantics.md) has landed its
  identity-bound byte comparison, but FA-R1 remains: an arbitrary
  `--cairn-root` is caller-designated, not authenticated.
* [TRU-3] **Verified source to installed bytes.** Release-authenticity RA3 and
  RA6: prove the working tree being built equals the verified release and make
  install-side provenance more than unsigned declarations. These share the
  trusted-source boundary with [TRU-1] and [TRU-2].
* [TRU-4] **Checker and frozen-set integrity.** Cairn's release checker cannot
  authenticate its own candidate bytes. This owner also carries the end-gate
  decision about whether the A/B/C engine packages join `frozen_files`, and the
  `_ast_attest` refusal for a mismatched `<kind>:` prefix. Keep these questions
  separate from merely running more checks: frozen coverage needs an explicit
  authority-set decision, and self-authentication needs a trusted-source
  launcher or anchored execution if the threat model demands closure. The
  missing AST-attestation re-anchor runbook and the dormant two-stage `promote`
  mechanism live here as trust-maintenance triggers, not active implementation.
* [TRU-5] **Gate-anchor and interpreter trust roots.** The gate preflight's
  trusted-contributor posture, first-use exact-byte bootstrap, external-anchor
  option, no-nonce replay residual, and the untracked local interpreter binding
  remain explicit high-risk surfaces with their existing expiry triggers.
* [TRU-6] **Release-signing residuals.** Signing-authority widening, a reported
  cross-channel fingerprint mismatch, transparency/keyless availability, and
  candidate git-config influence on future verification surfaces remain
  trigger-driven rather than standing implementation work.
* [TRU-7] **The gate anchor is unpublished, and no document says to publish it.**
  Added 2026-08-05; mirrors the `dev/PLANNING.md` deferral row of the same date.
  Measured: `refs/cairn/gate-anchor` exists locally at `e45e1fc`, and
  `git ls-remote origin 'refs/cairn/*'` returns **nothing**. No ordinary push can
  change that — git's default refspec is `refs/heads/*`, so `refs/cairn/*` is
  skipped by `git push`, by `git push origin master`, by `--all` (heads only) and
  by `--tags`; there is no configured `remote.origin.push` or `push.default`.
  Publishing takes an explicit `git push origin
  refs/cairn/gate-anchor:refs/cairn/gate-anchor`, and a collaborator needs a
  matching fetch refspec. **`bootstrap/REANCHOR_RUNBOOK.md` contains zero
  occurrences of `git push`** — it documents advancing the anchor locally via
  `git update-ref` and requires "local write access to `refs/cairn/gate-anchor`
  itself", but never publication. `refs/cairn/gate-authorization`, which the
  runbook resolves `A` from, has the same problem and is not present locally
  between ceremonies. So the differential-oracle trust root is **single-machine
  by construction**: a fresh clone has no anchor, and re-establishing a lost one
  is a Maintainer ceremony under a runbook silent on how it travels. This belongs
  to [TRU-5]'s surface but is a *distribution* gap rather than a trust-acquisition
  one, which is why it is its own row. It is a runbook gap, not a defect in the
  gate.

**Next consolidation:** one **trusted-source boundary** proposal may join
[TRU-1], [TRU-2], and [TRU-3] if it uses one operator-established verified
checkout and one decisive comparison path. It must not claim that an arbitrary
path authenticates itself. [TRU-4] joins only if execution actually begins from
trusted bytes.

**Exit condition:** candidate-controlled material can select what is examined
but never what counts as clean; every trust root has an acquisition story, an
expiry trigger, and a statement of what it does not authenticate.

### [REC] Deliberation authority, identity, context, and record integrity

**Question:** Can a mechanism or untrusted presentation mutate deliberation
state, create a commit, or be mistaken for authorization, independent review,
or trusted tool output?

**Current lifecycle owners**

* [REC-1] **Byline classification.** The landed classifier and its active
  residuals cover exact-name spoofing, Unicode folding classes, reviewer
  confusables, roster format/home, and the `Devine` prefix over-flag. The four
  archive-time follow-ups add exhaustive NFKD/casefold work, a hostile roster,
  and an independent oracle for the deletion set. These are one identity
  authority surface, not four future proposals.
* [REC-2] **Orientation-stream injection.** [BND-4] owns rendering untrusted git
  and filesystem text inert before it enters agent context.
* [REC-3] **Review-record conformance.** Plan
  [`review-gate-enforcement`](../plans/archive/review-gate-enforcement.md) reconciles the
  review schema and gates on declared tier/outcome. It remains a conformance
  backstop, not authentication that the declared reviewer performed the work.
  `transition-lint`, the planner's artifact/status cross-checks, the round-suffix
  regression, and the open `Touches`-header mutability decision are the same
  class of record-conformance work; each stays advisory or separately reviewed
  at the strength its own artifact declares.
* [REC-4] **Archive evidence claims.** The archive-commit-body auditability
  correction and its re-measured figure belong to lifecycle record integrity,
  not release scanning. The unfinished gate-claims axis-2/axis-3 sweep belongs
  under [REL-5].
* [REC-5] **Lifecycle mutation authority.** The Maintainer-run dogfood study is
  the evidence gate for typed lifecycle mutation. It must earn or decline the
  mutation arm by prevented failure and preserved assurance. A later commit arm
  is a separate privilege and Security-Review surface; version one prints the
  exact command rather than exercising that privilege. The study and mechanism
  share an authority question, but remain two ordered deliverables. Later
  lifecycle-routine skill payloads inherit the same authority boundary before
  they may perform proposal, review, Decision, or archive transitions.

**Exit condition:** every automated result says whether it checks syntax,
presentation, provenance, or authorization; untrusted data cannot imitate the
tool's grammar; no classifier is described as stronger than its oracle; and no
lifecycle mutation or commit occurs without a named authority and independently
reviewed privilege boundary.

### [REL] Release evidence, disclosure, and ceremonies

**Question:** What finite evidence blocks a release, who runs it, and which
ceremonies or human acts remain irreducible?

**Current lifecycle owners**

* [REL-1] **Finite v0.4.0 bar.** Plan
  [`release-security-bar`](../plans/release-security-bar.md) owns the six-item
  register, per-row deciders and negative controls, registered residuals, and
  the independent end-of-line audit. It decides readiness; this strategy does
  not.
* [REL-2] **One honest local command.** Proposed
  [`release-security-orchestration`](../proposals/archive/2026-08-05-codex-release-security-orchestration.md)
  consolidates clean-commit binding, Bandit and prose checks, release-only
  zero-skip pytest, quality gates, allowlist liveness, and false-CI/floor-gate
  wording. Its External Security Review recommends ship; Maintainer Decision
  and plan remain pending. The human invocation is explicit, not represented as
  automation.
* [REL-3] **Supervised re-anchor debt.** The dispositioned SC4 pins, stale R6
  pins, profile-parser manifest delta, `SKIP-XFAIL-NEW` over-reporting, and every
  frozen file changed by the active security cluster are one ceremony ledger.
  Re-derive the union immediately before the ceremony; never inherit counts
  from plans written against older commits.
* [REL-4] **Release-authenticity completion.** Disposition the old conditional
  External-round wording and either record the signing fingerprint in the
  Zenodo deposition or mark that channel prospective. The public-launch
  sequence owns the timing.
* [REL-5] **Claims versus enforcement.** Finish the behavioral/trigger sweep
  only as a bounded inventory. Live false-CI wording and the release-command
  recursion are [REL-2]; archive auditability is [REC-4]. Do not reopen already
  corrected lexical claims. The deferred governing-layer question -- whether
  an agent must name both a trigger and what it checks -- belongs to this owner,
  not to a free-standing doctrine change.
* [REL-6] **Security disclosure channel.** `SECURITY.md` needs a real private
  reporting route plus a front-page pointer, with Maintainer live verification
  that the forge setting exists. A stated private channel with no mechanism is
  not a control.

**Exit condition:** the release register is finite; every row is MET,
MET-by-registered-residual, or blocks; the local command fails on incomplete
evidence and names the exact commit; the final frozen union is supervised once;
the public has a working private disclosure route.

## Current portfolio and sequence

### Finish the admitted security cluster

1. `content-scan-detectors` and `separator-detection` are both landed and
   archived (SHIP-reviewed, 2026-08-10); their shared frozen-file re-pin
   remains a pending Maintainer-supervised ceremony.
2. Land `security-verification-activation`'s closed binding-mode amendment
   before admitting any API/web or portable registry entry.
3. `default-security-stance` is landed; preserve exact explicit module
   selection while the remaining scanner work closes.
4. Land `api-web-security-modules`, `portable-security-sweeps`, and
   `dependency-advisory-coverage` against the activation contract they actually
   inherit.
5. Preserve the landed `release-security-orchestration` command as the final
   release-gate scope before the shared supervised re-anchor.
6. Run one re-derived, Maintainer-supervised ceremony for the complete frozen
   union. `release-security-bar` may progress in parallel because its register
   is its principal surface.

`planner-line-semantics` and `agent-context-scrub` landed in the required order
and are archived. `review-gate-enforcement` follows the settled review schema
and its required External plan round; it should not be pulled into the scanner
ceremony merely because it carries a security consequence.

### Open next, after the current cluster

1. **Profile-authority consolidation** -- [BND-1], the quickest adopter-facing
   reduction of several parser/upgrade rows under one validator and one
   precedence contract.
2. **Trusted-source boundary** -- [TRU-1] through [TRU-3], after the release bar
   settles which source/install claims must hold for v0.4.0.
3. **Class C containment** -- [BND-2], no later than v0.4.0 preparation unless
   the Maintainer explicitly accepts it as a registered release residual.

### Queued authority work

* **Lifecycle mutation authority** -- [REC-5]. Run the Maintainer-owned dogfood
  study first. Open the typed mutation mechanism only if that evidence supports
  it; treat any commit capability as a later, separately reviewed privilege.
* **Lockfile schema authority** -- [BND-6]. Open on the next lockfile contract
  change, or earlier if [TRU-1]'s trusted-source design needs schema rejection.
  Do not let another provenance-field addition silently widen the reader.
* **Checker and facade residuals** -- [TRU-4] owns the end-gate frozen-set
  decision and attestation kind-prefix refusal; [BND-3] owns failed-import
  cleanup. Resolve each on the next matching authority or facade change rather
  than recombining them because they once shared a roadmap bullet.

### Triggered, not standing work

Do not schedule these merely because they are recorded:

* conda-native advisory research until Grype/Syft is executed or an adopter
  needs the coverage;
* LOW `B607` remediation until a PATH surprise or severity-floor decision;
* transparency/keyless signing until a zero-runtime-dependency verifier exists;
* signing-authority widening until the roster test fires;
* the first external-anchor/OS-containment/nonce upgrade until the gate-anchor
  posture's named adoption or control triggers fire; and
* forward-compatibility reversal until a real older-engine/newer-profile break.

Triggered work remains visible, but it does not compete with active
adopter-facing defects.

## Decision test for new findings

When a new security finding arrives:

1. **Reproduce it.** If behavior does not reproduce, correct the record rather
   than opening work.
2. **Name the protected asset and boundary.** Place it in exactly one primary
   cluster; cross-references are allowed, duplicate tasks are not.
3. **Check active ownership.** If an open plan already owns the same boundary
   and enforcer, amend or review that plan. Shared files alone do not justify
   absorption.
4. **Choose a disposition.** Fix now; guard with a named executable node;
   register a dated residual with an expiry trigger; or decline with a reason.
   "Keep investigating" is not a disposition.
5. **Name the decisive evidence.** Public-path execution plus a hazard-side
   negative control for code; exact source/trigger correction for prose;
   Maintainer ceremony only where authority actually requires it.
6. **Stop.** Once the cluster exit condition and the release register are met,
   new speculative hardening goes to a trigger, not onto the critical path.

## What this strategy deliberately does not do

* It does not declare v0.4.0 secure or ready; [REL-1] owns that finite audit.
* It does not convert every LOW scanner finding into blocking work.
* It does not require hosted CI under the current threat model.
* It does not treat local path validation as binary provenance or process
  containment.
* It does not merge API security, web-hosting security, dependency advisories,
  and content scanning into one universal runner; [VER-3] aggregates typed
  evidence while each capability keeps its own authority and tests.
* It does not let a strategy refresh rewrite append-only proposal or plan
  history. Only this living reference and the current-state roadmap are revised
  in place.

## Success measures

The strategy is working when:

* every security-relevant item in `dev/PLANNING.md` carries one primary cluster
  ID and one disposition: active owner, evidence gate, revival trigger, dated
  residual, or explicit decline;
* no active security plan is absent from the current portfolio;
* one shared ceremony replaces several plan-local ceremonies over the same
  frozen union;
* release documentation names the command and human act that really trigger a
  check;
* the v0.4.0 register reaches a finite verdict without moving unresolved
  blocking rows back to the roadmap; and
* a new finding can be routed in minutes without opening a proposal by default.

## Fold-up note

Three patterns may later merit methodology fold-back after recurrence across an
adopter: trust material must not come from the subject; scanner coverage derives
from delivery plus an independent oracle; and optional evidence may be
incomplete while authority failures fail closed. For now they remain Cairn's
project strategy, not universal doctrine.
