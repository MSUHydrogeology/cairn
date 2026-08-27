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

* `dev/PLANNING.md` owns current task state and which lifecycle artifact is
  active. **It no longer owns security triggers.** Until the 2026-08-26
  subtraction sweep it also carried a 1,010-line security-debt index; that index
  is now this document's *Live residual register*, and the board keeps a pointer.
* Proposals and plans own design detail, evidence, review findings, and accepted
  residuals.
* This strategy owns the cluster taxonomy, cross-scope dependencies, threat
  posture, priorities, the test for whether two findings belong together, and —
  since the bankruptcy pass — **the live residual and its revival trigger**.

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

**A residual leaves the register only two ways**: its trigger fires and a
lifecycle artifact takes ownership, or a measurement shows the subject no longer
exists. The second is a *recorded* act, not a quiet deletion — the sweep's own
dead-row list is in `dev/plans/subtraction-sweep.md`, each entry naming the
measurement. A trigger that can no longer fire is removed rather than left
standing, because a check that reports success while testing nothing is the
failure mode this project treats as worse than no check at all.

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
  [`api-web-security-modules`](../plans/archive/api-web-security-modules.md) owns the
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
  [`security-verification-activation`](../plans/archive/security-verification-activation.md)
  owns the default-on narrowing dispatcher. It is the dependency root for
  portable and API/web capability admission. Before either registry entry
  lands, it must settle the reviewed closed binding mode for runner and policy
  material. Its typed result vocabulary is also the owner for constructive
  readiness: a security tool that finds a missing capability or unmet bar names
  the safe next action without strengthening `INCOMPLETE` into `CLEAN`.
* [VER-4] **Language and dependency capabilities.** Plans
  [`portable-security-sweeps`](../plans/archive/portable-security-sweeps.md) and
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
  [`fork-advisory-semantics`](../plans/archive/fork-advisory-semantics.md) has landed its
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
  [`release-security-bar`](../plans/archive/release-security-bar.md) owns the six-item
  register, per-row deciders and negative controls, registered residuals, and
  the independent end-of-line audit. It decides readiness; this strategy does
  not. *Serialization update 2026-08-10:* the register is **populated and
  independently audited** — 47 verdicts (32 MET, 12 MET-by-residual, 3 NOT MET),
  audit verdict **REVISE**, agent work complete at Chunk H. The lasting boundary
  this strategy retains: **design principle 1 now has a confirmed instance inside
  Cairn's own tooling** — the integrity check reads its expected hashes from the
  candidate's own lockfile, so a coordinated tamper verifies as `OK`. Owning
  artifacts: `dev/PLANNING.md` **[TRU-1]** (tool half) and **[TRU-1b]** (the
  doctrine claim half, which no active plan owned until it was homed). The bar's
  own coverage residuals are the **Release bar (v0.5)** group, [RB5-1]–[RB5-5].
  Reproductions and per-row evidence stay in the plan, per this document's update
  rule.
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

## Live residual register

*Folded in from `dev/PLANNING.md`'s Security-cluster routing block at the
2026-08-26 subtraction sweep's C7 bankruptcy pass, under this document's update
rule: each row reduced to its **lasting boundary, residual, or revival
trigger**. Reproductions, per-row evidence and provenance stay in the archived
plan that produced each row; that is what makes this a register rather than a
second copy of the record.*

**How to read a row.** The tag is the cluster owner above. The *trigger* is what
revives it — a named change, a named ceremony, or a named report. A row with no
trigger is a standing decision waiting on someone, and says so.

**What is not here.** Rows whose subject the sweep deleted are listed as dead in
the sweep plan's C7 bankruptcy record, each with the measurement that showed the
subject gone. They are not carried forward as live triggers, because a trigger
that can never fire is the silent-success failure this project treats as worse
than no check.

### [BND] Input, execution, containment

* **[BND-1] Profile authority — five residuals from `profile-parse-fail-open`.**
  (G1) an unrecognized *module value* under `modules:` is accepted at exit 0 and
  printed in the roster — no downstream module validation exists; *trigger:* the
  first mistyped-module report, or the next change to `expand_preset`. (G2)
  unknown profile keys now refuse, and the reserved `schema` key rescues no
  already-released engine, so the disposition is free only while the adopter set
  is empty; *trigger:* the first genuine older-engine/newer-profile break, and
  the *remedy is a reversing proposal, never a quiet loosening*. (G3) two
  `bootstrap/tests/test_presets.py` nodes compare `_yaml_load` against itself
  when PyYAML is absent; *trigger:* the next edit to that file for any reason.
  (G5) `_resolve_current_profile`'s lockfile fallback is audible but was never
  examined for whether substituting the lockfile profile is right at all;
  *trigger:* the next upgrade-path proposal. (Decision point 4) the closed
  grammar's **totality claim is affirmed but unchecked** — the recommended
  focused round never ran, the External round affirmed it from the plan's own
  prose, and implementation landed anyway; *decide:* strike it as absorbed, or
  run the round against the landed code.
* **[BND-1] `_infer_init_lock_axes` guesses `human_team` from a filename.**
  `bootstrap/_scaffold/upgrade.py` infers `small-multi` from the presence of a
  root `CONTRIBUTING.md` and `solo` otherwise, so the engine can read a
  project's declared axis back wrong. Named upgrade path: read the manifest's
  `optional_templates` block instead of file presence. Reachable only on a first
  `upgrade --init-lock` in a tree with no committed `dev/.cairn/profile.yml`.
  *Trigger:* the next proposal touching that inference. *(Two provenances —
  `fork-advisory-semantics` scope 4 and `contributor-entry` R1 — merged
  2026-08-04.)*
* **[BND-1] The other consumers of `base_hash` were never swept.** The field
  ratchets forward on every `--finalize`, and the fork advisory was one consumer
  that read the ratchet as an upstream signal. No enumeration exists of the
  other readers or of which inherit the same wrong inference. *Trigger:* the
  next change to `--finalize`'s backfill, or any new detector keyed on
  `base_hash`.
* **[BND-6] Lockfile schema validate-on-read.** The `lockfile-provenance-fields`
  work added two provenance fields without bumping `_LOCK_SCHEMA` or teaching
  `read_lockfile` to validate on read — a **deliberate deferral, not an
  oversight**: `read_lockfile` is the second trust anchor, and teaching it to
  *reject* a lockfile on a version predicate is a fail-closed behaviour change on
  the path `upgrade` and `verify_integrity` both traverse. Plausibly its own
  Security-Review trigger, and exactly the "contract change married to a smaller
  change" bundling that proposal was split out to avoid. *Revive as:* validate
  `schema` on read, with a migration hint, and decide the fail-open /
  fail-closed disposition — its own proposal, on its own review tier.
* **[BND-3] Scaffold / engine shape — four boundary residuals.** Facade-loader
  symlink hardening across all three facades (refuse a submodule that is a
  symlink or resolves out-of-tree); cleanup of a partial `sys.modules` entry on
  a failed mid-load; a disposition for the side-door non-executable surfaces
  (onboarding activation log, preset sources, issue-capture forge starters); and
  relocation classification when a module's destination changes, with
  byte-preserving staging for non-text module files. *Trigger:* the next change
  on the matching write/exec boundary — not a generic hardening sweep.
* **[BND-3 / TRU-5] Interpreter trust-root check/use race (S2).** The
  `interpreter-trust-root-fallback` Security Review demonstrated a check/use
  race in `_has_symlink_component`'s symlink walk: replacing a checked real
  parent with a symlink between the walk and execution selects the retargeted
  binary. Pre-existing, and the attacker prerequisites generally permit
  replacing the interpreter directly — but the Decision explicitly did **not**
  accept it as closed. *Now lives in `templates/skills/_lib/session.py` and its
  twin `tools/session.py`* (the sweep moved the trust root out of the retired
  lifecycle CLI). *Revive as:* a design that closes the race — re-verify
  post-walk, or resolve and open atomically — as its own proposal on its own
  review tier.
* **[BND-3] Security-runner resource containment.** POSIX timeout cleanup kills
  a surviving process group; Windows descendant cleanup remains unverified and
  child disk growth is unbounded. *Trigger:* Windows support for this runner, a
  tool that writes candidate-controlled volumes, or the first cleanup/disk
  incident. Keep these as containment limits, not advisory-parser defects.
* **[BND-3] SC2 — the `B607` PATH-resolution findings, recorded and not fixed.**
  `git` invoked by name rather than absolute path, inside *an adopter's own
  repository*, which is a real question rather than a formality. **Re-measured
  2026-08-27 after the sweep relocated the code:** the session-kernel twins
  (`templates/skills/_lib/session.py`, `templates/skills/_lib/board.py`) carry
  **9 LOW findings — `B404`×1, `B603`×6, `B607`×2**, down from 16 across the two
  retired lifecycle files, with both `B607` sites in `session.py`. Deliberately
  deferred: bundling a code-hardening contract into a coverage contract is what
  cost `identity-not-name` a REVISE/SPLIT verdict. *Trigger:* an adopter
  reporting a `PATH`-resolution surprise, or any decision to lower the blocking
  threshold to LOW.
* **[BND-4] The pairs-only CRLF relay contract.** `_git` normalizes CRLF pairs
  before escaping, but a lone CR remains payload and must not become a line
  ending; splitting on `\r\n|\r|\n` reopens the reproduced author-name forgery.
  The regression tests are the guard. *Trigger:* any change to `_git` decoding,
  `_safe_stream`, or Windows line-ending handling — now in the session kernel
  twins, which is also where the tree's single terminal encoder
  (`encode_display`) lives.
* **[BND-4 / REC-2] Relayed sub-tool stream boundary.** Session routines relay
  structured stdout from sibling tools. Newline is legitimate data there, so
  field escaping cannot establish the same one-line authority boundary it does
  for filenames and git metadata. A successor must define framing and trust for
  relayed tool output before changing bytes. **Narrowed by the sweep:** the
  metrics relay is gone; the surviving relays are the intent and evolution
  tools. *Trigger:* the next session-stream format change, or a demonstrated
  forged `lifecycle:`-style line from one of these relays.
* **[BND-5] Container P3s.** The acceptance credential-residue leg (note or
  drop); `--user` on a future Docker acceptance leg; pinning the `git` apt
  version for image byte-reproducibility.

### [VER] Verification capabilities and coverage

* **[VER-1] Content-scanner homoglyph classification residuals.** Two
  follow-ups from the confusability-aware `homoglyph` rule, each needing its own
  proposal: (a) an exhaustive UTS #39-derived Greek classification to replace
  the 12-member curated `_NO_LATIN_TWIN` denylist — blocked on an oracle
  dependency, since `unicodedata` at UCD 15.1.0 exposes no confusables /
  skeleton / script / identifier-status accessor; (b) whole-script Cyrillic,
  left an explicit residual because flagging the whole script would cost
  legitimate international names. *Trigger:* either question recurring, or a
  Maintainer call to invest in one.
* **[VER-1] Content-scanner per-line-per-category flag limit.** `_scan_unicode`
  flags at most one hit per category per line; both source plans pinned the
  behaviour with a falsifiable test rather than changing it. Widening it would
  alter shipped `unicode-zero-width` / `unicode-bidi` / `unicode-line-separator`
  / `unicode-ignorable` / `unicode-tag` output for every adopter. *Trigger:* a
  demonstrated multi-hit-per-line attack the current limit misses.
* **[VER-3] A security test whose oracle is elapsed time fails open.**
  `bootstrap/tests/test_security_stack.py`,
  `test_a_t6_descendants_do_not_outlive_the_timeout`. The oracle is *absence of
  a sentinel within a window*, and absence has two causes it cannot distinguish:
  the grandchild died — the property holds — or it is merely slow, in which case
  the property is violated and unobserved. The verdict rests on about three
  seconds of scheduler luck, and the failure direction is the harmful one: a
  saturated machine does not make this flaky, it makes it **quietly green**. Its
  neighbour `test_a_t2_timeout_is_enforced_and_bounded` is the instructive
  contrast — it fails *closed* — so the pair reads as uniform and is not. The
  design intent (a side effect the grandchild itself produces, rather than a
  status this code returns) is sound; the defect is the *choice* of observable.
  *Fix direction:* assert on process state — a signal-0 probe or `waitpid` on
  the process group — which turns "I did not see it" into "it is not there";
  this is a real change, since the fixture never surfaces the grandchild's pid.
  *Generalises* to any other time-window oracle in the suite, so the fix is a
  claim about what makes a security test trustworthy, not a local patch.
  *Trigger, load-bearing:* **any evaluation of parallel test execution must fix
  this first** — under `pytest -n auto` the silent pass becomes routine. Fixing
  it edits a gate-frozen file, so it joins the re-anchor ceremony already owed
  rather than creating a new obligation.
* **[VER-3] Generated module-catalog parity.** Derive or executable-check the
  catalog in `templates/modules/README.md` against `_MODULE_MAPPINGS`,
  `_DEFAULT_ON_MODULES`, and token-gated selection; the current hand table omits
  default-on and team-gated modules. Include the preset roster comments and
  `docs/solo-legacy-recipe.md` in one catalog-wide design, so the next selector
  change cannot make those descriptions stale independently.
* **[VER-3 / BND-3] Vendor-wrapper scan-root discovery.**
  `content_scan_roots.txt` names optional wrapper filenames by hand, so a new
  vendor wrapper can go unscanned. Prefer deriving the installed wrapper path
  from trusted lockfile state; retain the fail-closed handling for missing
  required roots and option-shaped roots.
* **[VER-3] Constructive readiness.** When a Cairn tool finds a project below an
  expected bar it should offer and drive the path to readiness, not emit a bare
  "not ready" verdict — generative about adoption, not only diagnostic. Bounded
  by [VER-3]'s own rule that this must never strengthen `INCOMPLETE` into
  `CLEAN`.
* **[VER-4 / TRU-3] Dependency-advisory evidence tightening.** v1 reports the
  complete validated partition per run but stores no integrity-covered residual
  baseline for run-over-run diffs; its OSV source claim relies on pip-audit
  2.10.1's default endpoint constant rather than an explicit `--osv-url` argv
  pin, with the closed child environment preventing ambient override. *Trigger:*
  a requirement for historical drift evidence, a pip-audit version bump, or any
  widening of the pinned-source claim. A successor must bind the baseline into
  the install/integrity contract rather than trust an adjacent editable file.
* **[VER-4] Cairn security-check integrity preflight.**
  `templates/modules/team-gated/run_security_audit.py` refuses to run when its
  apparatus or policy inputs are not lockfile-clean; Cairn's own
  `bootstrap/security_check.py` has no equivalent preflight. Do not adopt the
  Python module sideways: define the authority for the checker's own bytes and
  policy inputs, then fail closed before any security phase executes when that
  authority disagrees.
* **[VER-4] Portable-security-sweeps deferred set (LT-1, LT-2, LT-4, LT-6).**
  Four follow-ups the plan fenced out of its own scope. **LT-1 — preset
  selection:** the adoption amendment's five-row table is unimplemented, and its
  home is a **new proposal** against the accepted `default-security-stance`
  selection contract — it edits `_PRESETS`, a symbol
  `_ast_attest._UPDATE_ALLOWLIST` does not admit, so it carries its own
  re-anchor accounting, and it changes what fresh adopters receive.
  *Trigger:* the next change to preset composition. **LT-2 — a permanent
  documented residual, not a deferral.** Measured 2026-08-10:
  `_selected_capability_ids` admits only module IDs ending in **`-security`**,
  and this module's ID ends in `-sweeps`, so the module is installed yet the
  dispatcher never sees it — a registry row would be **inert by construction**,
  and the chunk's required deletion mutant *could not fail*. **Maintainer
  accepted the third option** (*"Accept on the LT-2"*): portable sweeps runs via
  its own standing command, not through the dispatcher. The two rejected
  alternatives are recorded because the residual can be revisited — widening
  `_selected_capability_ids` (a trust-boundary change to what the dispatcher
  admits, so a Security Review) or renaming the module ID (shipped ID, lockfile,
  three paths, so Decision-bearing). *Revival condition:* the filter widening
  riding along with the activation plan's registry-admission chunk — at which
  point the inert-row and vacuous-mutant analysis is the evidence to re-read,
  **not** the branch table that assumes an effective row. **LT-4 — the three
  withdrawn adapters** (OSV-Scanner, zizmor, Trivy), named as a set so they are
  not silently forgotten; each arrives as its own proposal with its own
  executable chain, ambient-config execution evidence, network posture, output
  schema and offline-CLEAN disposition. **Distinct from** the conda-advisory row,
  which cites two of the same tools as *evidence about conda coverage* — a
  different question. **LT-6 — the `.json`-under-`templates/` precedent:** the
  licence half landed; the open question is whether `_self_hosted_twins()` should
  stop being `.py`-keyed, which generalizes a gate the plan does not own.
  *Trigger:* the second non-`.py` verbatim asset under `templates/`.
* **[VER-4] Conda advisory coverage.** `python-security` audits **Python
  distributions**; conda-managed native packages are outside its declared scope.
  Measured, not estimated: on the canonical environment **147 conda-only
  packages, 82 of them native** — `krb5`, `openssl`, `freetype`, `icu`, `hdf5`,
  the `aws-c-*` stack — `as_of 2026-08-03`. *Revival condition:* a maintained
  advisory authority for conda-forge packages **that execution demonstrates**,
  not documentation. Evidence already established so a successor does not
  re-derive it: **Trivy**'s conda coverage is SBOM/license only, vulnerability
  scanning unsupported; **OSV-Scanner** does not list Conda among supported
  ecosystems; **Grype/Syft** match by CPE rather than ecosystem and are
  unevaluated by anyone — the first candidate to actually run. A hand-built
  conda-name→CPE map is *not* another adapter: it makes Cairn the security
  authority for product identity, and needs its own Decision. Watch-outs a
  successor inherits: conda-forge can patch a CVE without bumping the upstream
  version (build strings carry no patch manifest), so naive version matching
  produces false positives in one direction and false negatives in the other;
  and vendored or statically-linked code has no record in any inventory.
* **[VER-5] SC1 — a name-keyed census is blind on the day it is written.** The
  struck registry census enumerated `*_MAPPINGS` by name, but `_OPTIONAL_TEMPLATES`
  in `bootstrap/_scaffold/config.py` is a live delivery registry that never
  reaches the manifest and whose name does not match the pattern. *Trigger:* a
  **shape-based** key — one that finds delivery registries by what they are
  rather than what they are called — or the first new delivery registry added
  under any name. Until then the gate's coverage claim is bounded by
  `install_manifest()`, which `bootstrap/SAFETY.md` states in terms.
* **[VER-5] SC3 — the union-vs-replacement monotonicity claim is unguarded, and
  the obvious guard is vacuous.** `scan_targets()` is a *union* with the
  manifest rather than a replacement, and no test guards that directly. The
  failure state is concrete: a later refactor deletes the union and the scan
  silently narrows. **The remedy this row used to prescribe was wrong** — the
  registry is a *subset* of the manifest, so deleting the union is a pure no-op
  and an assertion on "is a union" passes whether or not the property holds. The
  **provable** claim is narrower: *`scan_targets()` consumes `install_manifest`*,
  demonstrable by a sentinel monkeypatch that reddens under a
  hand-rolled-mapping refactor. Anyone writing this guard writes that claim.
  *Trigger:* any edit to `scan_targets()`.
* **[VER-6] Security-preflight residuals — three of six survive the sweep.** The
  five-question preflight block ships **declared-unenforced**, and these are its
  named expiry triggers. **R1**: plan templates carry a clause, not the block, so
  a security-touching plan whose source proposal predates the change inherits no
  answered block — *trigger:* the first such plan. **R2**: the security-touching
  gate is self-judged and nothing checks an "N/A" line — *trigger:* the *second*
  review that finds a security-touching change which wrote one. **R4**: five
  shapes, not all shapes — *trigger:* the first security finding that fits none
  of the five, at which point the shape has an instance and the recurrence limb
  applies to adding it. **Ritualization recovery** (cut to S1 and S2) fires on
  either of two `git grep`-able signals: three consecutive proposals whose S1-S5
  answers are byte-identical to a prior proposal's, or any proposal answering all
  "N/A" while its own `Touches` line names a surface `AGENTS.md` lists under
  High-risk surfaces. **Confirmed 2026-08-27:** the block itself survived the
  constitution rewrite in `templates/core/dev/proposals/_template.md`, and
  `templates/core/dev/plans/_template.md` still carries the clause — so R1 is
  still true of the tree, and the strategy's own [VER-6] conformance question is
  answered *survived*, not *silently dropped*.
* **[VER] The detached-checkout guard counts `__pycache__` as unexpected
  content.** `bootstrap/tests/test_security_check.py::test_detached_checkout_excludes_an_ignored_pytest_override`
  fails with `_RepoStateError: detached checkout does not contain exactly the
  committed paths`, because compiled bytecode caches are not committed content
  and the containment guard in `bootstrap/security_check.py` reports them as
  `extra`. It predates the work that found it — reproduced in a clean worktree at
  the commit before that plan opened — and it passes only when the generated
  `__pycache__` happens to be empty, so it is effectively always red for anyone
  who has run the suite before. **Sharper diagnosis:** the failure is
  *environmental, not a byte defect* — it and the two `TestLoaderContainmentMatrix`
  nodes all clear entirely under `PYTHONDONTWRITEBYTECODE=1`. So the successor's
  first question is narrow: should the guard ignore bytecode caches, or should
  the suite stop writing them? **Re-verified 2026-08-27**, unchanged by the
  sweep: red with caches present, green under the suppressor. **Why it is not
  `wontfix`:** it reaches no adopter, but it leaves a permanently red node in
  every future Boundary B record, which degrades release evidence — and the
  eligibility rule bars `wontfix` for anything release-blocking. **Why it was not
  fixed in place:** the two candidate fixes sit on different surfaces — relaxing
  the guard touches a named Security-Review surface, while making the test
  arrange a pristine checkout does not — and the guard's strictness is plausibly
  the point. *Trigger:* the next change to the containment guard or its callers,
  the next release sweep, or any Boundary B run whose record would otherwise
  carry this as a standing non-pass.
* **[VER-7] Language-neutral conformance fixtures and golden vectors.** For the
  extrication seam — exit semantics, path containment, lockfile schema, slot
  parsing, 3-way merge, security refusals — generated from the Python reference.
  The seam architecture shipped; the executable fixtures are deferred. This is
  evidence for a future implementation boundary, not a reason to build one.

### [TRU] Trust roots and provenance

* **[TRU-1] Install-integrity trust anchor.** `bootstrap/verify_integrity.py`
  reads expected hashes from **the candidate target's own**
  `dev/.cairn/cairn-lock.yml`, so a coordinated tamper — modify target files,
  then regenerate the lockfile over them — verifies as `OK`. `CAIRN_ROOT` exists
  in that module but only puts the engine on `sys.path`; it is not the hash
  source. Reproduced 2026-08-03 against the shipped module. *Revival condition:*
  anchor the **verbatim subset** against the caller's trusted `CAIRN_ROOT`
  checkout. A successor must define which files are genuinely verbatim, what
  happens when the caller's checkout *is* the candidate, and how a legitimately
  diverged fork is distinguished from a tamper — which is why this is a
  proposal, not a patch.
* **[TRU-1] There is no command that regenerates an existing lockfile.**
  *(Filed 2026-08-19 while executing the install-contract batch.)*
  `test_cairns_own_install_records_all_three_files_in_the_lockfile` states the
  rule in its own docstring — *"the lockfile is regenerated, never
  hand-edited"* — and `scaffold.py upgrade --init-lock` is the only writer,
  refusing when the file is already present (measured `as_of 2026-08-19` against
  a throwaway worktree: *"already exists; nothing to migrate"*, 0 lines changed).
  So a stale digest leaves an operator with two options the project forbids:
  delete-and-reinit, which discards the records that were correct and rewrites
  `migrated` / `cairn_commit` / `profile` besides, or hand-editing, which the
  docstring rules out. **This is the named-trigger rule failing on an artifact
  rather than a document** — it was invisible until someone needed the procedure,
  because the sentence reads like it describes one. *What was done instead,* so
  this is not read as an open failure: a purpose-built correction script,
  dry-run-verified and Maintainer-applied, rewriting only records whose digest
  disagreed with disk and moving a verbatim record's `hash` *and* `base_hash`
  only after proving byte-identity with its template. That script is a one-off in
  a scratchpad, deliberately — shipping it would answer the wrong question.
  ***What is owed is a decision, not a script:*** either the writer grows a
  targeted refresh with the same byte-identical proof, or the test's docstring
  stops naming a procedure that does not exist. The first is better; the second
  is the minimum. **Leaving both undone is the state that produced this row** —
  the instruction is followed by nobody and believed by everybody.
* **[TRU-1] Self-host lockfile reconciliation.** `scaffold.py upgrade --target .
  --cairn-root . --plan` reported **38** files as *"no recoverable base
  (review-only diff)"* against the base cache, each needing a by-hand
  `--stage`/`--apply` merge or a reviewed `--finalize` once its customization
  state is confirmed. Surfaced, not caused, by `solo-legacy-adopter-path`.
  *Revive by* re-running `--plan` fresh — **the figure above predates the
  subtraction sweep and will have moved** — confirming the current file list, and
  scoping the pass as several small reviewed `--finalize` batches rather than one
  large `--apply`.
* **[TRU-1b] The doctrine overstates what the integrity check can promise.** The
  claim-side twin of [TRU-1], which owns the tool side.
  `doctrine/runtime-contract.md` lists the integrity check as core/Required and
  describes it as detecting tampered apparatus fail-closed; `SECURITY.md`
  carries a matching overstatement. Measured: a coordinated tamper returns exit
  0, `OK`, with the marker byte still on disk, for both checked record types,
  while the untampered-lockfile control correctly returns exit 1. **Enforcers:
  none.** This is not an algorithm defect — no unsigned hash check *can* survive
  an attacker who rewrites both the bytes and their recorded digest, which is
  design principle 1. The defect is the **claim**. *Revival condition, either
  half discharges it:* narrow both sentences to what a lockfile-backed preflight
  can promise, **or** land [TRU-1]'s verbatim-subset anchoring, after which the
  claim becomes true for that subset and the wording should say which subset.
* **[TRU-2] FA-R1 — the fork advisory's comparison bytes are caller-trusted, not
  anchored.** The upstream operand is read from the checkout hosting the
  verifier, **or from any directory an operator names with `--cairn-root`, which
  may point inside the target**; containment is proven, provenance is not.
  *Revive when* `release-authenticity` lands an out-of-band trust bootstrap, or
  on the first Cairn install verified from a checkout the adopter did not obtain
  themselves.
* **[TRU-2] `identity-not-name` condition 3 is unlanded — a Maintainer call.**
  `format_forked_facade_warning` still advises removing the dormant engine
  package, which makes `tools/intent.py`'s `_load_engine()` raise `RuntimeError`
  and disables work-intent coordination. *Decide the shape:* (1) trivial commit
  now plus its own ceremony, (2) trivial commit now with re-anchor at the next
  ceremony, or (3) amend condition 3 and let the fenced chunk run inside the
  already-red window.
* **[TRU-3] RA3 — verifying the tree you build from.** The bootstrap proves a
  tag object is signed, not that a working tree equals that tag's tree. *Revive
  when* the scaffold gains a "verify my source" entry point, or when the
  lockfile's `cairn_commit` is cross-checked against a verified tag; either makes
  this an addition rather than a redesign.
* **[TRU-3] RA6 — install-side provenance.** Source-side signing landed; the
  lockfile's `source_repository` / `source_licenses` stay **declared**, not
  attested, and `python bootstrap/scaffold.py --manifest` stays unsigned.
  *Revive when* an adopter asks how they know their installed tree came from the
  release they verified, or when the fork-advisory scope reaches the same seam
  from the other side.
* **[TRU-4] The trust apparatus is protected by a glob, not by being named — and
  the ordering is the whole row.** Sixteen files that decide whether the gates
  pass are gate-frozen under the blanket `bootstrap/tests/**/*.py` glob:
  `conftest.py`, `_gate_manifest.py`, `_gate_preflight.py`, `_gate_reanchor.py`,
  `_ast_attest.py`, `_oracle.py`, `_oracle_activation.py`, `_oracle_trust.py`,
  `_loader_proto.py` and their `test_*` counterparts. Of these, **only
  `test_ast_attest.py` is named in `AGENTS.md` > High-risk surfaces**, and only
  in the re-anchoring sense. `bootstrap/tests/conftest.py` is the sharpest case:
  it carries the release-mode outcome rule that refuses a skip as release
  evidence and can set `session.exitstatus`, and it is named nowhere. The
  verification fence refuses bounded mode on a "contract surface", and the
  *broad* reading of that phrase — frozen-glob membership counts — is currently
  the only thing forcing a full suite when someone edits that rule. That reading
  is contested, and the narrow reading is defensible, since most frozen files
  are simply every `.py` under `bootstrap/tests/`. But adopting it would remove
  the *only* protection these sixteen files have. So the fence is doing security
  work **by accident**. *Ordering matters and is the point:* enumerate the
  trust-apparatus files as named trust-ceremony surfaces **first**, land that,
  and only then reconsider the glob reading — never the reverse, because a
  narrowing that lands first opens the fence widest at exactly the files it
  exists to protect. *Trigger:* any proposal to narrow or clarify the
  contract-surface fence, or the next Security Review reaching
  `bootstrap/tests/`.
* **[TRU-4] The frozen set does not cover a repository-root `conftest.py`.**
  `_frozen_files` discovers the frozen surface from five globs; a `conftest.py`
  at the repository root matches none of them, yet pytest loads it on every
  invocation this project actually uses. Verified by probe 2026-08-19 (removed
  immediately, never committed): a root conftest printing from
  `pytest_configure` fired under both a single-file run and the full suite, with
  `rootdir` at the repository root. This matters because
  `bootstrap/tests/conftest.py` **is** frozen, for precisely the reason that
  applies here — a conftest defines a gate's pass/fail semantics. A root conftest
  has the same power over the same session with none of the coverage, so the
  frozen set asserts an authority it does not hold. Adjacent surfaces each need
  their own disposition rather than being assumed in or out: a root `pytest.ini`
  / `pyproject.toml` / `tox.ini` / `setup.cfg` — **none exists today**, so the
  suite runs with no ini file and an inferred `rootdir`, and adding one would
  presently be an unreviewed act — and the `PYTEST_PLUGINS` / `PYTEST_ADDOPTS`
  environment variables, which cannot be frozen but whose absence a release run
  could assert. *Trigger:* the next change to the `_frozen_files` globs, or
  sooner — this is a live gap, not a latent one. Closing it edits a frozen file,
  so it costs a gate re-anchor; scope it to be worth that.
* **[TRU-4] `--noconftest` silently disables the release-mode outcome rule.**
  The flag skips loading `bootstrap/tests/conftest.py`, which carries the rule
  refusing a release when a security gate *skipped* rather than passed — and the
  suite still exits 0. Verified 2026-08-20: the flag appears **nowhere** in the
  tree outside the deliberation record, so nothing warns a reader and nothing
  asserts its absence on a release run. **Why this is filed rather than fixed in
  passing:** the exposure is as old as the outcome rule; the broad-run cost guard
  only made it visible, because a guard creates the first population of people
  motivated to get *past* a refusal. That is also why the fix is not "document
  the flag" — a note reading "this bypasses the guard" advertises the release
  control's off-switch to exactly that audience. If anything is written it
  belongs with the release trust surface and must lead with what else the flag
  disables; `CAIRN_FULL_SUITE=1` is the supported override and leaves every other
  control intact. *Candidate mechanism, not yet weighed:* a release run asserting
  its own conftest was loaded — the same shape as the `PYTEST_PLUGINS` absence
  assertion the row above contemplates, and probably the same disposition.
  *Trigger:* the next release-gate change, or any work on the row above; the two
  share a mechanism and should be weighed together.
* **[TRU-4] End-gate frozen-set decision.** Whether the A/B/C engine packages
  fold into the gate manifest's `frozen_files` — the same authority-set question
  the two rows above ask about `conftest.py`. Decide the authority set, do not
  merely run more checks.
* **[TRU-4] Attestation kind-prefix validation.** `_ast_attest` should reject a
  mismatched `<kind>:` prefix. *Trigger:* the next attestation-format change.
* **[TRU-4] The controlled re-anchor path cannot run for the ordinary case.**
  *(Observed 2026-08-13 during the second real gate re-anchor.)* There are two
  ways to move the gate's trust root and neither fits routine work. The
  **controlled** path refuses unless the differential oracle has *run*, and that
  oracle runs only when a pre-refactor baseline is configured — i.e. **during an
  engine refactor**. It reports itself *"dormant between refactors"* and the
  promotion then refuses, because the refusal cannot distinguish *"the check
  failed"* from *"the check did not need to run."* So a re-anchor caused by
  ordinary churn has only the **establishment** path, documented as *"supervised,
  one-time"*, which skips the authorization binding and the compare-and-swap that
  make the controlled path controlled. **Both of Cairn's real re-anchors went
  through it, and the sweep's gate-manifest re-anchor is a third.** A one-time
  procedure used three times is a routine procedure nobody designed. **Do not
  close this by configuring a baseline to satisfy the check** — that declares a
  refactor that did not happen, which is fabricating evidence to stop a control
  objecting, on a trust root. The honest options: give the controlled path a way
  to record *"no refactor, oracle not applicable"* without treating it as a
  failure, or accept the establishment path as the routine one and give it the
  bindings that absence currently costs.
* **[TRU-4 / REL-3] Who re-anchors the trust artifacts, and under what review.**
  The install-contract batch of 2026-08-19 was Maintainer-run under supervision
  across three artifacts — the AST baseline, the lockfile, and the gate manifest
  — and every figure in the row that requested it was stale by the time it ran,
  which is why the runbook forbids carrying a delta forward. **The artifacts are
  no longer stale; the question the batch raised is.** It is the same
  self-certification question as the interpreter re-pin below, and it is narrow:
  *who* regenerates and re-records, and under what review. Coverage is a
  sequencing question — whatever the anchor is at ceremony time covers whatever
  is committed then — so this does not need another plan's scope widened.
* **[TRU-4] Differential-oracle two-stage `promote`.** A dormant future-use
  mechanism for a Cairn-engine refactor needing behaviour-preservation
  promotion; trust root established, nothing pending. See
  `bootstrap/REANCHOR_RUNBOOK.md`.
* **[TRU-5] The gate-reanchor trusted-contributor posture is dated, and its
  expiry is not mechanical.** *Folded 2026-08-27 from `dev/PLANNING.md`'s Active
  block, where it survived a plan archive "because its commitments are live, not
  completed" — which is a register row's definition.* The trust root is
  established at `cfaace9` (re-anchored 2026-08-13, previously `e45e1fc`) and the
  preflight is in the anchor, so every ceremony from here runs the anchored
  loader. What stays open is the **posture**: Cairn accepts a
  *trusted-contributor* model for its own trust root, **single-maintainer, as of
  2026-08-03** — a dated acceptance, not a standing assumption. Its mechanical
  expiry is the Maintainer's signature on a checkpoint whose message binds the
  canonical range-review report digest, verified against the roster read from the
  anchor. **Two triggers cannot be mechanical and are named on purpose:** (a) the
  ceremony run on a checkout the Maintainer does not solely control; (b) any
  adopter taking the mechanism. On either, revisit the posture. Named upgrade
  paths: OS containment for the evidence stage, external anchoring via
  `_gate_manifest.py verify --trusted-repo` — supported all along and usable now
  that an anchor exists — and a single-use nonce or consumption ledger.
  *Historical correction preserved:* an earlier per-commit "signing epoch"
  tripwire was **retired, not renamed** — the epoch constant lived in the tree
  being blessed, so a candidate could move the line deciding which of its own
  commits were exempt, and refusing unsigned agent commits contradicted the
  normal workflow badly enough that operations disabled it. **A control routinely
  disabled is not a control.** Authorization now happens in exactly one place:
  the signed checkpoint.
* **[TRU-5] The interpreter-binding re-pin: reproduction confirmed, tier question
  open, and the pin itself is now gone.** *(Filed 2026-08-18; reproduction
  confirmed 2026-08-19; re-measured 2026-08-27.)* Symbol digests guarding the
  local interpreter binding were re-derived by an **implementing agent under
  explicit Maintainer authorization**, not by a Security Review, on a surface
  `AGENTS.md` lists as high-risk. A second agent re-derived them with its own
  stripper on both twins and got the recorded values exactly; the edit was
  comment-only and none of the five gated properties changed. **What remained was
  never technical:** the re-derivation rode an implementing commit while the pin's
  own text said to re-derive *"in that review's own commit"*, and a same-agent-type
  confirmation is a second reading rather than an independent tier. **Re-measured
  2026-08-27: the digest pin no longer exists** — `_INTERPRETER_SYMBOL_DIGESTS`
  has zero hits tree-wide, deleted with its host test module at C6. What guards
  the trust root now is behavioural, in `bootstrap/tests/test_session_kernel.py`
  and `test_session_failsafe.py`: a malformed binding refuses, a vanished
  interpreter falls back audibly, and the twins are byte-identical. **That is
  arguably better coverage than a digest and it is certainly different**, so the
  live question is no longer the re-pin's tier but whether a declared executable
  trust root should carry a byte-level pin at all. *Still open alongside it:* the
  `_has_symlink_component` coverage gap — the fence pins the caller and not the
  callee, so a behavioural change to symlink detection would not redden it. See
  the [BND-3 / TRU-5] check/use race entry, which is the same callee.
* **[TRU-6] RA1 (a) — Cairn's signing authority widens.** The principal-count
  warning in `bootstrap/container/verify-ref.sh` counts a roster the *adopter*
  typed and has no channel back here, so it is adopter hygiene, not a Cairn-side
  trigger. The mechanical half is the suite node
  `bootstrap/tests/test_verify_ref.py::test_cairn_roster_names_one_principal` —
  exactly 1 principal in `dev/.cairn/allowed_signers`, `as_of 2026-08-03`.
  *Revive when that node fires:* the one-signer, two-accounts trust model no
  longer describes Cairn.
* **[TRU-6] RA1 (b) — transparency-log / keyless verification.** *Revive when*
  such a verifier is usable without adding an adopter runtime dependency. The
  zero-dependency budget is the constraint, not the idea.
* **[TRU-6] RA1 (c) — a reported cross-channel fingerprint mismatch.** *Revive
  the moment* any adopter reports one: the two-channel comparison is the whole
  trust anchor, and a mismatch means it failed.
* **[TRU-6] RA5 — the candidate-git-config class on OTHER surfaces.** Closed for
  `bootstrap/container/verify-ref.sh` by construction — verification runs in a
  workspace the script creates, never in the candidate — but **not swept**: no
  enumeration exists of every config key that can influence a git verification,
  and the fetch still runs `upload-pack` inside the candidate. *Revive at* the
  next Cairn surface that shells out to `git` against a tree Cairn does not
  control.

### [REC] Deliberation authority, identity, context, record integrity

* **[REC-1] The byline identity classifier is gone, and with it the only
  mechanical reviewer-independence check.** *Raised 2026-08-27 by the C7
  bankruptcy pass; this is a **finding**, not a carried residual — the register
  would otherwise have inherited six ratified residuals whose subject no longer
  exists.* The 2026-08-03 `byline-classification` work shipped an identity fold
  and a whole-name exact match, and its independence comparator decided whether
  a `## Review` counted as independent of the author. **Measured 2026-08-27:
  `IdentityModel` has zero hits outside the deliberation record; so does
  `independent_review`; the only remaining reference to `human_maintainers` is
  in `CHANGELOG.md`; and the identity roster under `dev/.cairn/` was a two-line
  file no code read.** The sweep removed the classifier along with the lifecycle
  machinery that hosted it.

  **What that changes, stated plainly.** Reviewer independence is one half of
  the Dual-Review model, which is one of Cairn's two stated differentiators. It
  is now enforced by doctrine and by the Maintainer reading the record — and by
  nothing mechanical. **This may well be the right posture**: the check was
  advisory, it never authenticated anyone (`AGENTS.md` has always said the
  attribution *is* the record's integrity), and the roster it consulted had one
  entry. The sweep's whole thesis is that a control nobody needs is worse than
  no control. But the removal was a *side effect* of deleting the host module,
  not a decision anyone took, and the difference matters.

  **Six ratified residuals lose their subject with it** — the exact-name spoof
  accepted as dated, the presentation-fold equivalence with its three measured
  falsifying classes, the 3-of-4 independence widening with the Cyrillic
  homoglyph left open, the reveal-versus-inert escaper split, the token-style
  roster behaviour change, and the roster file's undocumented home. Their
  evidence stays in `dev/plans/archive/byline-classification.md`; the four
  archive-time follow-ups that sat on the board are on the sweep's dead list.
  **The `Devine` over-flag goes with them** — the AI registry's prefix match
  meant a real surname classified as `ai` with no roster escape; a genuine
  hazard, now moot, and recorded here so it is not rediscovered as new.

  **DECIDED 2026-08-27 — doctrinal-only independence, and the reason
  generalizes.** The Maintainer's authorization, verbatim:

  > "I am okay with doctrinal-only independence. Mechanical checks on process
  > create major headaches. Mechanical checks on formatting, correctness,
  > security, etc. are beneficial."

  So reviewer independence stays doctrine: `AGENTS.md` states the floors, and the
  attribution *is* the record's integrity. **No mechanical successor is owed**,
  and this row is closed rather than parked behind a trigger. The identity roster under
  `dev/.cairn/` was deleted in the same commit — nothing read
  it, and configuration nothing consults is a claim of coverage that does not
  exist. **If a future change wants mechanical independence back it needs a
  reviewer-identity contract, which never existed**: the only human list Cairn
  has confers Decision authority, and reusing it would couple two authorities to
  buy one check.

  **The general rule this settles**, recorded because it governs more than this
  row: *mechanical checks earn their place on **formatting, correctness and
  security**, and lose it on **process**.* A process check is a claim about
  whether people followed a procedure, which drifts, self-judges, and gets
  routed around — the failure this sweep spent 60,000 lines removing. A
  correctness check is a claim about bytes, which either holds or does not. When
  deciding whether a proposed gate is worth building, ask which of the two it is
  before asking how well it would work.
* **[REC] A second clearing review manufactures a competing authority pair.**
  *(Filed 2026-08-19 from `ceremony-as-code`'s M2; folded 2026-08-27 from
  `dev/PLANNING.md`'s Queued block.)* The M2 row says *"the **reviewer** produces
  and self-records the launcher/packet pair"*, singular — it assumes one
  reviewer. Two independent External Security reviews cleared round 2, so **two
  valid authority pairs exist**. They cannot be *mixed* — each launcher carries
  its own packet's digest, so a cross-pair combination fails the binding check —
  but nothing says which pair is canonical, and nothing stops someone later
  finding the unused one and running it in good faith. One was used; the other
  was never delivered to disk and is void by circumstance rather than by rule.
  **The review redundancy is a gain; the pair redundancy is a liability.** *What
  is owed is one sentence in the contract, not a mechanism:* a second clearing
  review confirms the same bytes and **produces no pair** unless the first is
  withdrawn.
* **[REC-3 / VER-3] Implementation-verification record conformance.** The v1
  contract instructs authors to append a dated, field-complete record only after
  the stable Boundary B run, but nothing proves the section is nonempty or
  schema-complete. *Trigger:* the first malformed record that reaches code
  review. A successor must validate the settled record schema without mistaking
  heading presence for evidence or rewriting append-only history. **The
  mechanism this row once expected is gone** — the sweep retired the lifecycle
  parser — so a successor builds the check, it does not extend one.
* **[REC-4] Gate-claims B2 — the archive-commit-body auditability claim is
  falsified.** `doctrine/proposals.md` > "Archive preconditions" and
  `doctrine/plans.md` > "Lasting-truth migration doctrine" both claim the
  migration is auditable from `git log` alone. Keep the "must", name the
  trigger, correct the consequence claim. Its own proposal, because the block is
  restated in `doctrine/lifecycle-contract.md` and
  `templates/core/dev/PLANNING.md`, which engages the loop-fidelity lens.
* **[REC-4] B2's evidentiary figure is re-measured at pickup, never carried.**
  The proposal's "zero archive commits" is falsified; measured 2026-08-04, plan
  archives 1 of 10 and proposal archives 2 of 21. **Re-run the enumeration
  before writing any number** — the sweep has since moved both denominators.
* **[REC-4] A lasting-truth attestation is written once and the section grows
  after it, and nothing re-checks.** *(The general form of the row above.)* A
  plan can archive attesting `Dispositions: none` while its own section names
  follow-ups in prose — measured on `ceremony-as-code`, where the attestation was
  accurate when written, three durable observations were appended below it, and
  the archive gate passed because it reads the attestation and never compares it
  to the section around it. **Two sentences in the instructions do most of the
  work, and both are wrong in the same direction:** *"Only `defer` needs a
  durable home outside the plan; the other dispositions **are** the home"* is
  true for an `accept` that actually landed somewhere a reader will meet, and
  **false for an observation**, where `accept` means nothing was written
  anywhere living and the plan is about to stop being read; and *"filled in at
  archive time"* implies one moment while *"append-only once written"* guarantees
  accretion, with nothing saying **an append re-opens the attestation**.
  *Suggested wording, deliberately not applied* — this is `templates/core`
  doctrine and wants a decision rather than an edit in passing: qualify the first
  as *"`accept` is the home only when the accepting change landed somewhere a
  reader will meet; an observation with no landing place is a `defer` and needs a
  row"*, and add to the second *"appending to this section re-opens the
  attestation."* **Why prose rather than a mechanism:** the remaining gap is a
  *consistency* question between an attestation and free prose, which a regex
  answers badly.
* **[REC-5] Lifecycle mutation authority — the boundary outlives its
  mechanism.** The typed-mutation direction presupposed the lifecycle CLI, which
  the sweep removed, and the Maintainer-run dogfood study that was to earn it
  has no subject. **What survives is the authority boundary, and it binds any
  future mechanism:** no lifecycle mutation or commit without a named authority
  and an independently reviewed privilege boundary, with commit a *separate*
  privilege from mutation. *Trigger:* any proposal to mechanize a lifecycle
  transition, which re-opens the study question rather than inheriting its
  answer.

### [REL] Release evidence, disclosure, ceremonies

* **[REL-3] Supervised re-anchor debt — one ceremony ledger, re-derived at the
  ceremony.** Four recorded contributors, none authorized as a standalone
  re-pin. (SC4) `bootstrap/security_check.py`,
  `bootstrap/tests/test_security_check.py`, `bootstrap/tests/test_security_lint.py`
  — **Maintainer disposition 2026-08-04, quoted verbatim: *"SC4 - fold in"***;
  scheduled, not open, and its removal condition is the ceremony running rather
  than a decision. (Dependency audit) `templates/modules/team-gated/run_security_audit.py`
  and `bootstrap/tests/test_security_stack.py`. (R6 fix)
  `bootstrap/tests/test_quality_gate_redundancy.py` and `scripts/quality_gate.py`,
  edited with no re-pin. (Profile parser) one `FROZEN-MODIFIED` on
  `bootstrap/tests/test_scaffold.py` plus one `COLLECTION-DROPPED` from a test
  rename. **Re-derive the union immediately before the ceremony; never inherit a
  count from a plan written against an older commit** — and note the sweep has
  since re-anchored the gate manifest over its own removals, so every figure
  above predates the current anchor.
* **[REL-3] `SKIP-XFAIL-NEW` over-reports.** The check reads
  `get_closest_marker("skipif")`, which resolves a module-level `pytestmark`, so
  any node added to such a module registers as newly marked. *Trigger:* the next
  supervised ceremony, or the next plan needing a node in a marked module.
* **[REL-4] `release-authenticity` — the Decision's flagged condition,
  undispositioned.** The approved ledger entry read "Accept, conditioned on a
  scoped External round for the tag-substitution fix only", but the Maintainer's
  quoted words said only "as revised". Either strike it in one line or name what
  discharges it.
* **[REL-4] Zenodo is a documented channel with nothing in it.**
  `bootstrap/PROVENANCE.md`'s channel table lists the per-version deposition as
  channel 3, but no fingerprint has ever been recorded in a deposition and no
  public-launch step names it. At launch, either record the fingerprint beside
  the deposition or correct the table row to say channel 3 is prospective.
* **[REL-5] The gate-claims audit's axes 2 and 3 were never swept
  systematically.** Axis 2 is behavioural — run the artifact that would check
  the stated control; axis 3 asks whether the named trigger contains the
  procedure. `gate-claims-vs-enforcement` sampled both, and two ledger rows fell
  out of a single ad-hoc axis-3 pass, which is the argument for finishing the
  sweep as its own bounded inventory.

* **[REL-5] The loop-fidelity gate covers one folder out of several.** *(Homed
  2026-08-13 at the Maintainer's instruction from `review-efficient-lifecycle`
  [CF9], which measured it and deliberately did not widen it.)*
  `check_cairn`'s `_CAIRN_INTERNAL_PREFIXES` is `('doctrine/',)` — **confirmed
  unchanged 2026-08-27**. The gate exists to stop a **shipped** `templates/**`
  surface citing a path that exists in Cairn's tree but not in an adopter's;
  with one prefix it catches `doctrine/` and nothing else, so a `bootstrap/`,
  `dev/plans/`, `dev/proposals/`, `dev/measurement/`, `case-studies/` or
  `dimensions/` citation dangles in an adopter tree and passes clean. **Measured,
  not inferred:** with `bootstrap/fidelity-check.md` and a `dev/plans/` path
  appended to a shipped surface, `check_cairn` printed *"OK -- 1 Markdown
  file(s) scanned; no issues."* **The live instance this row carried is gone** —
  `templates/core/AGENTS.md` cited `bootstrap/fidelity-check.md` in its
  drift-guard paragraph until the sweep's constitution rewrite removed that
  citation, verified 2026-08-27. So the gap is now latent rather than shipping,
  which lowers the urgency and changes nothing about the gap. **The first task was to count what
  widening would flag, and it is now counted: 128.** Measured 2026-08-27 by
  monkeypatching the prefix tuple to ten candidate prefixes (`doctrine/`,
  `bootstrap/`, `dev/plans/`, `dev/proposals/`, `dev/measurement/`,
  `dev/strategy/`, `case-studies/`, `dimensions/`, `examples/`, `docs/`) and
  running the gate's own `_check_dangling_internal_refs` over the 64
  template-instruction surfaces it inspects. **128 flags across 20 surfaces**,
  by cited prefix: `docs/` 54, `dev/` 39, `bootstrap/` 21, `dimensions/` 10,
  `case-studies/` 2, `examples/` 2. Concentrated rather than diffuse — four
  surfaces carry 72 percent of them.

  **Positive control, because a zero here would have meant nothing:** with a
  `dev/plans/` citation planted in a shipped surface, the current prefix set
  reports **0** and the widened set reports **129** — one more than the clean
  tree, which is the planted line. *(An earlier attempt returned 0 for both and
  was wrong: the widened copy ran from a scratch directory and resolved the repo
  root to itself. The control is what caught that.)*

  **So this is the "large population" branch** — staging or a deprecation
  window, not an ordinary fix. **The count is not the whole first task:** which
  of those ten prefixes genuinely dangles in an adopter tree is a separate
  judgment per prefix, and `docs/` — the largest contributor — is the most
  arguable of them. Doing it as a side effect of an unrelated plan is how a standing gate
  changes behaviour without anyone reviewing the change. *Trigger:* the next
  change to `check_cairn`'s prefix set or to shipped-template citation policy.
  **Note for the checker de-scope:** that work touches this exact tuple, so it is
  the most likely thing to trip this row.
* **[REL-6] `SECURITY.md` names no disclosure mechanism.** *(Split out of
  `contributor-entry` by Maintainer direction, 2026-08-03.)* It tells a reporter
  to report *"privately to the maintainer"* and names no route; verified
  2026-08-03, no root `CONTRIBUTING.md` exists and `README.md` carries no
  *Contributing* heading, so a would-be reporter has none. **Diagnosis of record:
  a stated control with no mechanism behind it** — the same shape as
  `bootstrap/PROVENANCE.md`'s unchecked signature. Fixing it needs no
  `CONTRIBUTING.md` and no doctrine change, which is why it separates cleanly.
  Two things travel with it: the channel's deciding property — whether the forge
  setting is actually enabled — **cannot be established by a reviewer and is a
  Maintainer live-verification step**; and `README.md` gains the pointer, because
  it is the only entry-layer file a first-time visitor reliably reads and a
  disclosure channel nobody can find from the front page is not a channel.

### Release bar (v0.5)

*Residuals of the v0.4.0 bar, revived together by a v0.5 bar rather than
individually.*

* **[RB5-1] The register's coverage gap — record the producing command, not the
  number.** The bar adjudicated ~25 surfaces; its declared scope contains
  substantially more, and the surplus has no register row. **The count is a
  moving target** — it read 49 one morning and 69 that afternoon, because the
  tree grew. So this row records the derivation:

  ```python
  # independent leg  =  Set 3 claim-bearing docs  ∪  every templates/**/*.py on disk
  # surface list     =  the committed H2 extraction over the register's Chunk RUN cells
  # gap              =  independent leg − surface list
  PATH_RE = re.compile(r"`([A-Za-z0-9_./-]+\.(?:py|sh|md|json|yml))(?::[0-9]+)?[^`]*`")
  runs    = re.split(r"^#### Chunk [A-H] — RUN", plan_text, flags=re.M)[1:]
  surface = {m.group(1) for c in runs for m in PATH_RE.finditer(c) if (root/m.group(1)).is_file()}
  ```

  *Revival condition:* a v0.5 bar, **which starts by re-running the command
  above rather than trusting any figure recorded anywhere.**
* **[RB5-2] Set 3 quantifies over a static candidate-path list, not a tree
  walk.** Its positive control catches a planted `templates/**/*.py` but not a
  planted adopter-installed Markdown security claim, because Set 3 is a fixed
  list. Ruled acceptable for v0.4.0 **as a recorded residual** — so the residual
  has to actually be recorded, which is this row. *Revival condition:* expanding
  the independent leg to a dynamic traversal, which is what makes the coverage
  assertion self-maintaining.
* **[RB5-3] The five proposal-level v0.5 deferrals.** Token-substituted lockfile
  anchoring; non-test derived-list integrity; extending the bar to Cairn's own
  dev tooling, including the `check_cairn` coverage gap; mutation testing as a
  standing mechanism; and cryptographic attestation. The second is the general
  form of [RB5-4].
* **[RB5-4] B6's reach table is unpinned.** No test keeps it in step with preset
  composition, so it can go stale silently. *Trigger:* the first time it is
  found stale by the staleness command — **which has its own defect, [RB5-5].**
* **[RB5-5] The staleness command can report FRESH when it matched nothing.**
  `git log -1 --format=%cI -- <surface list>` with an unquoted list under zsh
  passes one multi-word pathspec, git matches zero paths, and exit 0 with empty
  output is indistinguishable from "no commits since the audit". Audited
  severity **MEDIUM (operational tooling hazard)** — this is the mechanism that
  decides whether a release tag waits. *Fix:* explicit array expansion plus a
  non-zero-match assertion over the surface set, so an empty match is an error
  rather than a pass.
* **[RB5-6] The staleness surface list contains a path it is structurally blind
  to, and that path is an executable trust root.** `dev/.cairn/local-env.json`
  is in the derived surface list and is **untracked and gitignored**, so
  `git log … -- <that path>` returns empty **for all time** — it can never signal
  staleness, however the pathspec is quoted. This is **not** [RB5-5] and quoting
  cannot fix it: that one is a malformed-invocation hazard, this is a *tracking*
  hazard. On the bar's own standard it is a check that cannot fail, and its
  output is worse than silence — a permanent `FRESH` reads as "this trust root
  has not moved" when the mechanism has never been able to see it. `AGENTS.md` >
  High-risk surfaces classifies that file as an untracked, gitignored,
  lockfile-uncovered **executable trust root**, so the one member the mechanism
  is blind to is the highest-risk member of the list. Found on the mechanism's
  **first real run**, by the `git ls-files --error-unmatch` assertion [RB5-5]
  prescribes — which is the only reason it was visible at all. *Fix, either
  half:* exclude untracked paths from the derived surface list **and say so**,
  so the list stops implying coverage it lacks; **or** give that trust root a
  tracked witness — a committed digest or shape record — that `git log` can
  observe.

### Security pair close-out

*Residuals of `api-web-security-modules` and `security-verification-activation`.
The discharged items are not carried here; the plans hold them.*

* **[SP8-3] The dispatcher cannot ever report CLEAN for a credentialed
  capability — a design question, not a bug.** `_read_credentials` runs for
  `local` mode and refuses `E_CREDENTIAL_ABSENT` when a principal's credential
  is absent from the environment, and the dispatcher's child-env allowlist
  admits no credential name and no `SSL_CERT_FILE`. So both capabilities can
  report *unconfigured*, *refused* or *degraded*, never *passed* — which sits
  oddly beside registry entries declaring `evidence_mode: loopback`. Weakening
  the allowlist would be a real security regression and was correctly refused.
  Needs a proposal on what the dispatcher's role **is** for a credentialed
  capability.
* **[SP8-4] Three defects hid at one interface because each side tested
  itself.** The `-security` name-suffix filter, the single-token `argv_mode`,
  and the `details` dict-vs-string contract were invisible to both plans'
  reviews: the activation tests drive a **synthetic** runner and the facade
  tests invoke the CLI **directly**. `TestChunkGRealFacadeThroughRealDispatcher`
  closes this seam. The generalizable question — whether any reciprocal plan
  pair should be *required* to carry a both-sides-real integration test before
  either half archives — belongs in the Dual-Review doctrine, not in a plan.
* **[SP8-5] Cairn does not self-host the dispatcher, and that was never
  decided.** Activation pre-declared the decision to the first capability plan;
  no capability plan made it. Measured 2026-08-11 and **re-confirmed
  2026-08-27**: no copy of `run_security_verification.py` exists under
  `scripts/` — the path is cited nowhere precisely because it does not resolve —
  and the lockfile carries zero references. The de facto answer is "no
  self-hosting"; making it deliberate is a one-line decision nobody has taken.
  Related and still open: **Cairn's own lockfile does not record
  `dev/modules/security-verification.md`** even though the file is in the tree
  and the module is default-on, and **no gate reddened** — a scoped re-finalize.
* **[SP8-6] Two residuals re-homed from a review that does not exist.** The
  destination-collision path for activation's two new files, and the
  install-manifest byte-stability invariant having no standing test. Both
  declared "the code review" as their durable home; no such section was ever
  written. The second is a *gap claim* that wanted a reviewer's agreement it is
  real.
* **[SP8-7] `api-web-security-modules` never landed its
  `templates/modules/README.md` catalog row.** Activation landed its own row;
  api-web's was left because another session held the file. Activation assigned
  the pre-existing default-on drift fix to "whichever cluster scope lands its
  README row last" — with api-web's row never landing, that owner never
  resolved. Folds naturally into [VER-3]'s catalog-parity work.
* **[SP8-8] Every adopter's `AGENTS.md` reads `clean-locally-modified` on
  upgrade with no adopter edit.** The module merge pass rewrites the file after
  `install_core` while the base cache retains the unmerged template, so the
  classifier sees divergence the adopter did not create. Not a blocked upgrade —
  the kind stays inside `_ADVANCING_KINDS` — but an inaccurate label on the
  single most-read file Cairn installs.
* **[SP8-10] A test whose expectation depends on ambient state.**
  `bootstrap/tests/test_security_verification.py`'s child-env test computes
  `expected` from the parent `os.environ` at call time. Where the parent lacks
  `LC_CTYPE`, CPython's subprocess spawn auto-injects `LC_CTYPE="C.UTF-8"`; the
  dispatcher admits `LC_` via its allowlist prefixes, but the assertion fails
  exact set equality on the post-spawn injection. The expected-set calculation
  should account for CPython's auto-injected `LC_` keys.
* **[SP8-12] `test_verify_ref`'s two failures are NOT a missing GPG key.** That
  explanation was propagated all day — into two archived plans' verification
  sections, two commit bodies, and several sub-agent briefs — and it is
  **false**. Measured 2026-08-11: `test_verify_ref.py` alone is 67/67 green;
  both nodes fail only in the full suite, reproducibly across two consecutive
  runs, and not when paired with individual neighbours. So it is cross-file
  state pollution, and the conclusion those records drew ("not this work's") was
  right for the wrong reason. **A wrong reason is worse than none here:** "needs
  a GPG key" tells the next reader to stop looking. Narrowing the polluter is a
  bisect nobody has run. Same shape as [SP8-10].
* **[SP8-13] `intent.py claim` cannot record a legitimate wide claim, and its
  error advises the wrong remedy.** Met 2026-08-11 while claiming nine paths:
  refused at 553 bytes, then 522 after shortening `--action`, against the
  512-byte cap — with **342 bytes of that being paths alone**. The cap is
  correct and load-bearing: it keeps one record inside a single `os.write`,
  which is the append atomicity the whole surface rests on. The defect is that
  the error names `--stem` and a shorter `--action` as remedies while reporting
  paths as the dominant contributor — neither remedy touches paths — so the
  operator's only recourse is to split the claim and hope the overlap check
  still means something. **A cross-cutting refactor is exactly when a claim
  matters most and exactly when it cannot be filed.** Candidate shapes: fold a
  common prefix, or emit multiple lines sharing one `id` so the record stays
  inside one `os.write` per line while the claim stays whole. Either changes the
  record schema that `active_intents`, `conflict` and `prune_released_pairs` all
  read, so it takes a proposal.

### Unclustered

* **[Coordination] Refine the intent tool's necessity test.** Gate on
  *shared-worktree* multi-agent work, not team size — worktree-per-agent does
  not need it.
* **[Coordination] Move the intent config into `dev/.cairn/`.** Machine-edited
  settings belong in the machine-state directory; the transition reads both
  paths. *(No config file exists on disk today, so this is a design constraint
  on the first one written, not a move.)*
* **[Doctrine] Count-claims dedup.** Fold the three-kind concept into
  `doctrine/lifecycle.md` with a one-line pointer from `doctrine/proposals.md`
  and `doctrine/plans.md`.
* **[Doctrine] Model-tier vocabulary single-source** *(low residual)*. The
  tier→model binding is canonical in `dev/.cairn/model-selection-mapping.yml`;
  revisit only if a project later adds its own tier vocabulary.

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
   settles which source/install claims must hold for v0.4.0. *2026-08-10: that
   "after" has arrived* — the bar has settled them, and the answer is that the
   claims **do not currently hold**. This moves from "open next" to the highest
   priority in this cluster, and it gained a fourth item, **[TRU-1b]**: two
   adopter-facing sentences
   (`doctrine/runtime-contract.md:132`, `SECURITY.md:51`) assert a tamper-
   detection property the mechanism cannot deliver. Cheaper than it looks —
   `bootstrap/UPGRADE.md:366` already states the honest version, so the remedy is
   reconciling three documents to the one that is right, or narrowing the two to
   the subset [TRU-1]'s anchoring would make true.
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

## Refocus serialization note — 2026-08-26 (Claude, Strategy)

The 2026-08 refocus (`2026-08-21-claude-nimbleness-recovery`; the accepted
convergent-lifecycle contract; the open `subtraction-sweep` plan) leaves this
strategy's protected assets, design principles, cluster taxonomy, and decision
test intact — the sweep plan's "Not touched" list names the security stack
explicitly. Protected asset 5, the Maintainer's attention, is now the whole
project's stated objective, so this document anticipated the refocus rather
than conflicting with it. Recorded here so the two records agree:

* **The security suite is release-only** (Maintainer decision, 2026-08; the
  pytest marker + manifest chunk has landed; the `security_check.py` release
  path is unchanged). This is principle 4 applied: the trigger is named at its
  real strength — Maintainer-run, at release — not weakened.
* **The refocus's warn-never-refuse doctrine carves out exactly this
  strategy's fail-closed surfaces** (scaffold containment; release trust
  roots). The two documents state one rule from two directions; no conflict.

**Four rows conform when their sweep chunk lands** — folded in then, not now,
because revising ahead of execution would describe a future state. **All four
landed; conformed 2026-08-27 at the C7 bankruptcy pass, dispositions below.**

1. **[REC-3]**: `transition-lint` (sweep C5) and the planner's artifact/status
   cross-checks (C6) are removed. The record-conformance class stays doctrine;
   the tool dispositions end with the tools. **Conformed:** the tool-bound rows
   are on the dead list; the surviving class row is the register's
   implementation-verification conformance entry, which now says a successor
   *builds* the check rather than extending one.
2. **[REC-5]**: the typed lifecycle-mutation direction presupposed the
   lifecycle CLI, which C6 removes. The authority boundary it states — no
   lifecycle mutation or commit without a named authority and a reviewed
   privilege boundary — outlives the mechanism and binds any future one; the
   dogfood-study gate needs a re-disposition when C6 lands. **Conformed:** the
   mechanism and the study are dead; the boundary is restated in the register as
   binding on any future mechanism, and the study question re-opens with the
   next proposal to mechanize a transition rather than carrying an answer
   forward.
3. **Authority and update rule**: `dev/PLANNING.md`'s ownership of task state
   changes at C2 (minimal board view) and C7 (bankruptcy); restate then.
   **Conformed:** restated above — the board no longer owns security triggers.
4. **[VER-6]**: the preflight questions live in proposal templates the
   constitution rewrite (C2) replaces; they either survive into the
   deliberate-lane template or get an explicit re-disposition — not a silent
   drop. **Conformed: they survived.** Verified 2026-08-27 —
   `templates/core/dev/proposals/_template.md` still carries the five-question
   block and `templates/core/dev/plans/_template.md` still carries the clause,
   so R1's premise holds unchanged and the register records R1, R2, R4 and the
   ritualization-recovery limb as live. R3, R5 and R6 lost their subjects and are
   on the dead list.

**Where the security-debt index lives after C7 — done, 2026-08-27.**
`dev/PLANNING.md`'s Security-cluster routing block (1,010 lines, 93 rows) was
measured during sweep scoping as a **live** security-debt index with revival
triggers, not dead prose. C7's bankruptcy pass folded the surviving material
into this document's **Live residual register** — each live row reduced to its
lasting boundary, residual, or revival trigger per the update rule above — with
`PLANNING.md` keeping a pointer only. Every row that did *not* survive is named
on the sweep plan's dead list with the measurement that showed its subject gone,
so nothing was dropped by omission.

## Fold-up note

Three patterns may later merit methodology fold-back after recurrence across an
adopter: trust material must not come from the subject; scanner coverage derives
from delivery plus an independent oracle; and optional evidence may be
incomplete while authority failures fail closed. For now they remain Cairn's
project strategy, not universal doctrine.
