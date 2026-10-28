# Narrow the gate's test-file freeze without hiding test loss

**Author**: Codex (Sol), Proposal author
**Status**: awaiting-review
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-28
**In brief**: Keep security and trust tests under the signed gate while letting ordinary test maintenance proceed without a re-anchor ceremony.

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
