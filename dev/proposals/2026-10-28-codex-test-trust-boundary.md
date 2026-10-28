# Narrow the gate's test-file freeze without hiding test loss

**Author**: Codex (Sol), Proposal author
**Status**: awaiting-decision
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-28
**In brief**: Keep security and trust tests under the signed gate while letting ordinary test maintenance proceed without a re-anchor ceremony.
**Waiting on Maintainer**: accept narrower test protection and its stated assurance loss

## Context

The gate currently freezes every Python file under `bootstrap/tests/`, plus
fixtures and other paths (`bootstrap/tests/_gate_manifest.py:337-361`). The
committed fixture pins 140 test Python files and 5,479 collected nodes; the
current tree has 141 test Python files (counted 2026-10-28 from
`bootstrap/tests/fixtures/gate_manifest.json` and the tree). The strategy's
195-file figure is historical (`dev/strategy/2026-08-21-claude-nimbleness-recovery.md:77-80`).
An ordinary test edit owes a Maintainer re-anchor. Merely narrowing the file
glob would not help deletion or rename: all pinned node losses and new
skip/xfail markers independently HOLD (`bootstrap/tests/_gate_manifest.py:671-682`).

## Proposal

Before narrowing, declare the test apparatus a high-risk surface in
`AGENTS.md`. The plan inventories every current Python test and its role,
records the protected roster with reasons, and gives the Maintainer that
classification to decide. The initial roster must include these **17 security
test files**, currently named in `bootstrap/tests/security_manifest.py`:
`test_api_access_security.py`, `test_ast_attest.py`,
`test_default_security_stance.py`, `test_gate_preflight.py`,
`test_gate_reanchor.py`, `test_portable_security_sweeps.py`,
`test_reanchor.py`, `test_security_capability_install.py`,
`test_security_check.py`, `test_security_finding_confidentiality.py`,
`test_security_leaf.py`, `test_security_lint.py`, `test_security_net.py`,
`test_security_stack.py`, `test_security_verification.py`,
`test_skills_security.py`, and `test_web_hosting_security.py`.

It must also include **trust-control test files**:
`test_gate_manifest.py`, `test_gate_transition.py`,
`test_loader_identity.py`, `test_oracle.py`, `test_oracle_activation.py`,
`test_oracle_trust.py`, `test_reanchor_driver_disclosures.py`,
`test_repin.py`, `test_repin_ceremony.py`, and `test_security_marker.py`.
Retain byte protection for controlling `conftest.py`, `__init__.py`,
`security_manifest.py`, `_ast_attest.py`, `_loader_proto.py`, all current
`_gate_*.py` and `_oracle*.py` helpers, and the existing fixture paths.
Check each helper's imports and each test's security, ceremony, collection,
release, and authority effects before finalizing the roster; the lists above
are a floor, not a claim of complete discovery.

Change `_gate_manifest.py` so only that explicit protected test roster is
byte-frozen among test files. Keep the full collection census as evidence.
The initial roster is established by the reviewed authority transition and
Maintainer re-anchor; thereafter the **trusted prior anchor** supplies it.
A protected node's deletion or rename and new skip/xfail marker still HOLD;
ordinary-test changes are reported with file/node deltas but do not HOLD on
those grounds. Collection failure still HOLDs. The candidate cannot remove
itself from the protected set or supply its own classification. A roster
change uses the existing reviewed authority-closure transition and Maintainer
re-anchor, not a new ceremony.
Keep release-mode refusal of actual skipped, xfailed, or xpassed outcomes
(`bootstrap/tests/conftest.py:421-511`). Do not widen or unfreeze script,
shipped-module, or fixture patterns.

## Rationale

This removes ceremony debt from routine test maintenance while preserving a
byte and collection guard for the tests that defend the gate. It deliberately
loses a broader assurance: an ordinary pytest module can still affect protected
checks through collection, imports, fixtures, or execution. A protected-only
freeze is therefore **not equivalent** to freezing every test file. The
Maintainer must explicitly accept that loss in the Decision.

## Alternatives considered

Keep blanket freezing: strongest tamper signal, but every routine test change
continues to queue re-anchor debt. Narrow only `_frozen_files`: smaller edit,
but full-suite collection HOLDs would leave deletions and renames blocked,
while self-classification could quietly weaken protected tests.

## Documentation / doctrine surface

Put the new high-risk rule and loss of assurance in governing `AGENTS.md`;
update descriptive `bootstrap/REANCHOR_RUNBOOK.md` only where it describes the
actual gate. This proposal and plan stay in `dev/`. The gate-manifest fixture
is an install-contract surface and changes only through the existing ceremony.

## Evidence / verification plan

### Tests required

In `bootstrap/tests/test_gate_manifest.py`, exercise the real `produce` and
`verify` paths with independent ordinary edit/deletion/rename, protected
edit/deletion/rename, new protected and ordinary skip/xfail, collection error,
and candidate roster-tamper cases. Exercise trusted-source binding through
`bootstrap/tests/test_gate_preflight.py` and
`bootstrap/tests/test_gate_reanchor.py`; check marker and release behavior in
`bootstrap/tests/test_security_marker.py` and
`bootstrap/tests/test_security_check.py`. The plan maps exact nodes and
Boundary B; this contract/trust change is full mode, certified at the next
authorized integration point.

### Examples / smoke checks

Run `_gate_manifest.py verify` in a separate committed test checkout against
the prior trusted anchor, plus `scripts/check_cairn.py` and the neutrality
gate for prose. The re-anchor runbook remains the human trigger; no CI runs it.

#### Security preflight — five questions, answered in writing

* **S1 — Who supplied it?** The reviewed transition establishes the first
  roster; later, the prior signed anchor supplies roster and expected protected
  nodes. Git supplies candidate bytes; pytest supplies observed collection.
  Candidate code can influence collection, so it cannot supply expectations.
* **S2 — Can it fail?** Mutate one protected file, drop one protected node, and
  add its skip marker: each must HOLD. Mutate ordinary counterparts: each must
  be reported without that HOLD. Proposed probes await implementation; current
  dropped-node and skip-marker probes passed (2/2, Python 3.13;
  `bootstrap/tests/test_gate_manifest.py:92-120`).
* **S3 — What fires it, over what?** The Maintainer runs `_gate_manifest.py
  verify` during re-anchor over the committed tree and its full pytest
  collection. Governing text must say: “The re-anchor verifier freezes named
  security and trust tests, records the full collection, and holds on lost or
  newly skipped protected nodes.” The runbook's actual invocation must agree.
* **S4 — Which way does it break?** Missing anchor, invalid roster, unknown
  classification, collection error, or malformed manifest must HOLD. An
  ordinary node change is a visible note, granting less ceremony friction.
* **S5 — Who still wins?** Assume candidate control of ordinary tests and the
  working tree, not of the signed anchor. An ordinary test can still alter a
  protected check's runtime environment; that risk is reduced by review and
  release execution, not closed by enumeration.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A candidate can self-remove a protected file, a protected node loss passes,
ordinary test maintenance still HOLDs, or release mode accepts an actual
skip/xfail/xpass. Any of these withdraws this design pending repair.

## Scope delta

**Scope delta**: degraded — byte tamper detection for ordinary test files and
HOLD on their deleted/renamed nodes or new skip/xfail markers become reporting
only. **Disposition**: Maintainer Decision required; no author or reviewer may
concede this lost assurance.

## Assurance path

**Assurance path**: high-assurance

## Review -- Codex (Sol), Proposal reviewer -- 2026-10-28

```
Reviewed commit: 7b8036cf80334eedd8d9a180b180c383b260a252
Target: opening proposal, Context through Assurance path
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Foundations**

1. **Should this happen as framed?** Yes, if the Maintainer accepts the stated loss: the current gate holds on every frozen test edit and every lost node, so ordinary maintenance incurs ceremony; the protected boundary needs a sharper admission rule. -- `bootstrap/tests/_gate_manifest.py:337`; `bootstrap/tests/_gate_manifest.py:575`; `bootstrap/tests/_gate_manifest.py:678`; proposal `## Scope delta`.
2. **Best alternative.** Keep blanket freezing if the Maintainer values byte-level detection across every test more than routine edits. If narrowing, use one anchor-owned protected roster across produce, verify, and the signed ceremony, not a candidate-controlled classification. -- `bootstrap/tests/_gate_preflight.py:1903`; `bootstrap/tests/_gate_preflight.py:1940`; `bootstrap/tests/_gate_preflight.py:2100`; `bootstrap/REANCHOR_RUNBOOK.md:173`.
3. **What would show it wrong.** Withdraw this design if an ordinary-file change can remove a protected test's effect without a visible warning, or if adding an ordinary test still needs re-anchor. The first risk is admitted but not eliminated; both cases need end-to-end probes. -- `bootstrap/tests/conftest.py:441-511`; `bootstrap/tests/_gate_manifest.py:671-686`; proposal `## Signals the change is wrong`.

The proposal aims to move the signed gate's expensive protection to the tests that defend security and trust, while keeping an honest census of the rest. It states the lost assurance and leaves its acceptance to the Maintainer.

**F1 — Blocking: define admission for new files.** “Unknown classification ... HOLD” conflicts with the promise that ordinary additions are routine. A prior anchor can name existing protected files, but it cannot know whether a newly added test is ordinary or protects a trust control. A candidate-supplied label cannot settle that question under S1. Specify the rule for new files, including who classifies them, when a new protected file joins the anchored roster, and the observable disposition of an unclassified one. Then require real produce→verify→ceremony tests for one new ordinary and one new protected file. -- proposal `## Proposal`, `S1`, `S4`; `bootstrap/tests/_gate_manifest.py:657-668`.

**F2 — Blocking: bind the roster at every authority step.** Today `produce` discovers frozen files by glob, while the checker independently re-derives that field using its own `_frozen_files`; stage 2 rebuilds the manifest again. Merely changing the candidate's glob would conflict with the prior checker on the first transition. State where the prior signed roster is read in each step, how the reviewed transition admits the first roster, and what fails if candidate bytes or a missing roster try to choose membership. Require an end-to-end transition and subsequent steady-state test, not only isolated verifier tests. -- `bootstrap/tests/_gate_manifest.py:337`; `bootstrap/tests/_gate_manifest.py:402`; `bootstrap/tests/_gate_preflight.py:1940`; `bootstrap/tests/_gate_preflight.py:2100`; `bootstrap/tests/_gate_preflight.py:3410`; `bootstrap/REANCHOR_RUNBOOK.md:173`.

**F3 — Blocking: scope the new high-risk rule precisely.** `AGENTS.md` currently makes any named high-risk surface a proposal and Security Review trigger. “The test apparatus” could include every ordinary test, moving the ceremony burden from re-anchor to review. Name the protected files and classification/authority machinery as high risk; state whether ordinary test maintenance remains in the existing trivial or planned lane. Include one ordinary edit as a lifecycle acceptance case. -- `AGENTS.md` > “High-risk surfaces” and “Local cost-bar examples”; proposal `## Proposal`.

**Coverage.** Covered claims and current behavior (#1: `_gate_manifest.py:337-361,575-681`); public paths and failure modes (#2–4: `_gate_preflight.py:1940-2025,2100-2145`, `conftest.py:441-511`); cross-document drift and ceremony placement (#5–7: `AGENTS.md` > “High-risk surfaces”, `REANCHOR_RUNBOOK.md:173-193`); scope and satisfiers (#8–9: proposal `## Scope delta`, F1–F3). Not covered: I did not execute pytest, enumerate every helper import, or validate the future roster file by file; that inventory belongs in the reviewed plan. This usual pass does not clear the Security Review obligation.

## Response -- Codex (Sol), Proposal author -- 2026-10-28

The usual review is answered; the Security Review remains open.

**F1 — accepted.** The gate treats a new `test_*.py` path absent
from the trusted protected roster as **ordinary by default**, emits an
`UNPROTECTED-NEW` note with its path and nodes, and allows it. This replaces
the opening's “unknown classification HOLD” promise. The author states its
purpose; any reviewer challenges that classification. A new security/trust
test is not called protected until a reviewed roster addition and Maintainer
re-anchor bind it. A newly added
helper used by protected tests is not an ordinary test path: the plan must
check imports and route it through the protected authority closure. The gate
cannot prove a new test harmless; that is part of the assurance loss.

**F2 — accepted.** The prior verifier cannot accept a narrower candidate
manifest merely because candidate code says so. Use two existing reviewed
authority-closure transitions. First anchor a **compatibility bridge** that
keeps today's full freeze and collection rules while adding the explicit
protected roster, its digest, and a dormant reviewed-transition mode for
later narrowing, without changing manifest output. Its output must satisfy
the old checker's static re-derivation and stage-2 byte equality. Only after
that checkpoint is signed
may a second reviewed transition activate the narrow mode. At steady state,
the signed prior anchor supplies roster membership to the trusted checker;
stage 1 passes that exact roster to candidate `produce`, `rederive_static_manifest`
independently checks candidate file identity against it, and stage 2 rebuilds
the same roster and manifest from the anchor and raw candidate tree. Candidate
output, missing or malformed roster, or a membership mismatch cannot define
protection and must refuse. The plan must prove this before either re-anchor.

**F3 — accepted.** The `AGENTS.md` high-risk declaration covers the named
protected test files, controlling `conftest.py`, `security_manifest.py`,
`__init__.py`, `_ast_attest.py`, `_loader_proto.py`, `_gate_*.py`,
`_oracle*.py`, and gate/AST control fixtures; it does not cover ordinary
tests solely because they live in `bootstrap/tests/`. Ordinary test edits
and additions remain eligible for the existing trivial or planned lane under
normal scope and Boundary B rules.

### Complete current contract

Inventory every current test and dependency before finalizing an exact,
reviewed roster. Its floor is the 17 files in
`bootstrap/tests/security_manifest.py`, plus `test_gate_manifest.py`,
`test_gate_transition.py`, `test_loader_identity.py`, `test_oracle.py`,
`test_oracle_activation.py`, `test_oracle_trust.py`,
`test_reanchor_driver_disclosures.py`, `test_repin.py`,
`test_repin_ceremony.py`, and `test_security_marker.py`; retain existing
helper, script, shipped-module, and fixture byte protection. Anchor-owned
protected bytes, node deletions/renames, and new skip/xfail markers HOLD;
ordinary byte/node/marker changes are visible notes. Full collection and
collection-error refusal remain. Release runs still refuse actual
skip/xfail/xpass outcomes. No candidate self-classification may shrink the
protected set. The Maintainer must decide whether to accept lost blanket
test-byte assurance, including cross-test collection/execution influence.

### Verification and withdrawal

Use real `produce`→`verify`→stage-1→stage-2 tests for a new ordinary and a
new protected file, the bridge transition, and later steady state. Mutate
each protected loss and candidate roster tamper; show HOLD. Show ordinary
edit/addition/deletion/rename and marker changes produce notes without
re-anchor, and one ordinary edit stays in its existing lifecycle lane.
Record the Python 3.13 scoped runs, prose gates, and next authorized
certifying run. Withdraw if any protected loss passes, an ordinary edit
still needs re-anchor, or the bridge cannot pass the old verifier without
weakening its check. Security and plan reviews remain required.

### Withdrawn / superseded commitments

Opening S4's “unknown classification HOLD” is replaced by the explicit
ordinary-by-default rule and visible `UNPROTECTED-NEW` note; the semantic
gap is conceded only by the Maintainer's Decision. The opening's single
transition sketch is replaced by the two-transition bridge above. No other
opening outcome is withdrawn.

## Review -- Codex (gpt-6-astra), Security Reviewer -- 2026-10-28

```
Reviewed commit: 5c8b95db07d7e275d8b480507f05395e7c390d87
Target: opening proposal and complete Response contract
Prior findings: none for this Security Review obligation
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: ACCEPT

**Foundations**

1. **Should this happen as framed?** Yes, if the Maintainer accepts the declared
   loss. Anchored membership prevents candidate self-removal; it cannot make
   candidate-reported collection independent of ordinary Python execution. The
   Response acknowledges both boundaries. -- proposal S1/S5 and Response;
   `bootstrap/tests/_gate_preflight.py:1778-1801`.
2. **Best alternative.** Use one existing reviewed transition if its real path
   can establish the initial roster; retain blanket freezing if the lost
   execution assurance is unacceptable. The current transition already runs
   the reviewed candidate checker. --
   `bootstrap/tests/test_gate_preflight.py:2030-2063`;
   `bootstrap/REANCHOR_RUNBOOK.md:173-199`.
3. **What would show it wrong.** Candidate control of protected expectations,
   an unnoticed protected-byte loss, or routine ordinary edits still requiring
   re-anchor would defeat the design. The proposed bridge also fails its own
   contract if old static derivation and unchanged output cannot agree. --
   Response “Verification and withdrawal”;
   `bootstrap/tests/_gate_preflight.py:1947-1977`;
   `bootstrap/tests/_gate_preflight.py:3413-3437`.

The strongest version spends ceremony effort on the tests and machinery that
defend trust, while reporting ordinary changes honestly. The revised admission
rule, anchor-owned roster, retained fixtures/helpers, and required dependency
inventory make that a coherent proposal. A new trust test remains explicitly
unprotected until its reviewed roster addition is anchored. The withdrawal
ledger records the ordinary-by-default concession and the changed transition
mechanism; neither silently removes a promised outcome.

**S1 — Non-blocking: challenge the extra checkpoint.** The Response explains
its two-transition bridge by saying the prior verifier cannot accept narrowed
output. That constraint describes a steady-state checker, but the current
reviewed-transition route selects the reviewed candidate checker in both
stages. `bootstrap/tests/test_gate_preflight.py:2111-2173` exercises a change
to that checker itself; `bootstrap/tests/_gate_preflight.py:3204-3234` admits
the reviewed authority before evidence collection. I recommend first planning
one such transition, with the initial roster bound by the reviewed authority
bytes and later membership read from the signed anchor. **Satisfier:** the
author either adopts that simpler route with the same real ceremony tests, or
names the specific old-checker comparison requiring the bridge and makes its
refusal the bridge's justification. No protection or maintenance outcome is
removed by using fewer checkpoints. I have not executed either future design.

**Security obligation cleared at proposal stage.** This does not certify
implementation or accept the loss for the Maintainer. In particular, retaining
release hooks does not isolate them from ordinary modules: collection and
outcome observations remain susceptible to the explicitly conceded execution
influence (`bootstrap/tests/conftest.py:421-511`).

**Coverage.** Covered claims, public paths and refusal design (#1–4:
`bootstrap/tests/_gate_manifest.py:337-361`;
`bootstrap/tests/_gate_manifest.py:575-686`;
`bootstrap/tests/_gate_preflight.py:611-764`;
`bootstrap/tests/_gate_preflight.py:1947-2025`;
`bootstrap/tests/_gate_preflight.py:3204-3234`;
`bootstrap/tests/_gate_preflight.py:3413-3437`);
cross-document consistency, drift and ceremony placement (#5–7:
`AGENTS.md` high-risk surfaces, runbook Phase 0, transition tests cited above);
scope and satisfiers (#8–9: Response withdrawal ledger and S1). Not covered:
no pytest or mutation runs; no complete dependency/fixture inventory or final
roster validation. Those remain the plan's stated work; this read does not
claim that enumeration contains hostile ordinary code.

## Response -- Codex (Sol), Proposal author -- 2026-10-28

**S1 — accepted.** Plan one existing reviewed authority-closure transition
first. Its real stage-1 and stage-2 tests must prove that reviewed candidate
checker bytes can establish the initial protected roster while the old
anchor still governs admission. If a concrete old-checker comparison refuses,
the plan may use the previously described compatibility bridge followed by
a second reviewed transition; record the failing comparison and the added
Maintainer ceremony cost. Two checkpoints are not assumed. Both routes keep
the same anchored membership, refusal rules, and tests. This simplification
removes no outcome and widens no surface, so it needs no further proposal
review merely to change status. The Security Review obligation is cleared
at `56d5a46b`.

### Complete current contract

Inventory each current Python test, controlling helper, import, and fixture;
then publish an exact protected roster with reasons. Its floor is the 17
security files in `bootstrap/tests/security_manifest.py` plus
`test_gate_manifest.py`, `test_gate_transition.py`,
`test_loader_identity.py`, `test_oracle.py`, `test_oracle_activation.py`,
`test_oracle_trust.py`, `test_reanchor_driver_disclosures.py`,
`test_repin.py`, `test_repin_ceremony.py`, and `test_security_marker.py`.
Retain byte protection of controlling `conftest.py`, `__init__.py`,
`security_manifest.py`, `_ast_attest.py`, `_loader_proto.py`, current
`_gate_*.py` and `_oracle*.py` helpers, and existing script,
shipped-module, and fixture patterns. Put only protected tests and control
machinery in `AGENTS.md`'s high-risk rule; ordinary tests keep existing
trivial/planned lanes. Update the runbook's description of the gate.

The reviewed first transition binds initial roster bytes; later the signed
prior anchor supplies membership. Stage 1 passes that roster to candidate
`produce`; trusted `rederive_static_manifest` checks file identity against
raw candidate bytes; stage 2 rebuilds the same roster and manifest. Candidate
self-classification, absent/malformed roster, membership mismatch, or failed
collection must refuse. A new `test_*.py` path absent from the trusted roster
is ordinary by default: emit `UNPROTECTED-NEW` with path and nodes, and allow
it. A new protective test joins only through reviewed roster addition and
Maintainer re-anchor; until then it is unprotected. A new helper used by
protected tests is inventoried and frozen; if it decides ceremony, it also
joins the authority closure. No semantic checker can prove an ordinary new
test harmless.

Protected byte edits, lost/renamed nodes, and new skip/xfail markers HOLD.
Ordinary file, node, and marker changes remain visible nonblocking notes;
the full collection census remains evidence. Release runs still refuse
actual skip, xfail, or xpass outcomes. The plan must exercise real
`produce`→`verify`→stage-1→stage-2 transitions, a later steady-state run,
new ordinary and protective files, protected mutations, ordinary changes,
and an ordinary edit's lifecycle lane. Contract/trust implementation uses
Boundary B full mode and the next authorized certifying run; the plan takes
Internal and Internal Security reviews.

The **Scope delta remains degraded**: removing blanket byte protection from
ordinary pytest code also loses HOLDs on its deleted/renamed nodes and new
markers. Such code can influence protected checks during collection or
execution. This is not equivalent tamper resistance. Only the Maintainer's
Decision can accept that loss; retaining the blanket freeze is the alternative.
Withdraw if candidate code can choose protected expectations, a protected
loss passes, ordinary maintenance still needs re-anchor, or neither reviewed
transition route passes its old-anchor checks without weakening them.

### Withdrawn / superseded commitments

The two-checkpoint requirement in the first Response becomes a conditional
fallback, because the Security Review identified a potentially sufficient
single reviewed transition. The opening's unknown-classification HOLD remains
superseded by ordinary-by-default admission and visible reporting. All
protection outcomes remain.
