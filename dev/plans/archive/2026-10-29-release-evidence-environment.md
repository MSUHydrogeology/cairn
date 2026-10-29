# Plan: Release evidence environment

**Source proposal**: dev/proposals/archive/2026-10-29-codex-release-evidence-environment.md
**Status**: archived
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-29
**In brief**: Let release evidence run with the cache-only pytest setting while refusing settings that can steer collection.

## Source proposal

The Maintainer accepted the literal cache-only exception and its evidence requirements in the source proposal's Decision. The producer still trusts candidate collection and interpreter execution; this change does not contain candidate code.

## Scope

Change `bootstrap/tests/_gate_preflight.py` and its tests at the existing producer boundary. Preserve the release token, phases, cache suppression and other environment protections. Update affected descriptive text if the reader search finds it; no governing or doctrine surface changes. Carry the protected change through the existing pinning ceremony before release, with Maintainer actions reserved to the runbook.

**Reuse.** Search for `gather_evidence`, `PYTEST_ADDOPTS`, `_release_child_env`, and `_run_order_independence` across `bootstrap`, `scripts`, `docs`, and `dev` found the existing boundary, producer, release launcher, quality-gate grandchild, preflight and ceremony tests. Reuse the boundary and producer's explicit cache option; do not introduce an option parser or duplicate launcher.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Implement exact admission and tests; reconcile affected descriptions. | Plan review and Security Review | Boundary, targeted tests and evidence. |
| C2 | Prepare protected-change packet and independent read using `bootstrap/REANCHOR_RUNBOOK.md`. | C1 verification and code review | Ceremony inputs and reader record. |
| C3 | MAINTAINER-ONLY: verifier decisions, pinning and signing under the runbook. | Maintainer authorization and runbook prerequisites | Protected-file pinning before release. |

## Acceptance criteria

**C1.** At the existing launch boundary, absent or exactly `-p no:cacheprovider` permits producer launch; remove the exact value before launch. Empty, whitespace variants, `--ignore`, and an appended selector refuse before launch. Both plugin variables refuse by presence, including empty and in combination with the accepted cache value. Diagnostics identify offending names without values. Retain release-mode enforcement and direct and real quality-gate grandchild propagation. Compare actual pytest node identities with and without the cache value; a known node disappears under `--ignore` while the boundary refuses it. Record the appended-selector mutation and passing control through `gather_evidence` with producer marker. No scoped result claims release success.

**C2–C3.** Prepare and independently read the required protected-file packet at the reviewed candidate; the Maintainer performs the runbook's verifier decisions, pinning and signing. A HOLD remains a HOLD until the runbook's required human disposition. Do not move an anchor or sign as an agent. The separate release ceremony is not implied by this plan.

Security preflight S2 and S3: C1 runs the appended-selector mutation and control through the real evidence entry point, and the mapped tests below select the changed boundary. Existing preflight S1, S4 and S5 remain as corrected in the accepted proposal; candidate collection remains trusted.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A and B use Python 3.13.x and the owning families: `bootstrap/tests/test_gate_preflight.py`, `bootstrap/tests/test_security_check.py`, `bootstrap/tests/test_quality_gate_order_independence.py`, `bootstrap/tests/test_ceremony_review_report.py`, `bootstrap/tests/test_gate_reanchor.py`, and `bootstrap/tests/test_security_lint.py` (scan coverage). Exercise the actual evidence entry point, release environment and real grandchild, including the node-identity and selector controls above. Search readers and callers again after edits and add any affected consumer checks. Run these standing non-pytest checks and record outcomes:

* `python -c 'import sys; from bootstrap.security_check import run_bandit; sys.exit(run_bandit())'` invokes the release runner's Bandit phase directly, without its full suite. `scan_targets()` includes the ceremony authority closure, including the changed preflight; the phase rejects scanner errors, unallowlisted MEDIUM+ findings and stale allowlist entries. Missing Bandit is a failure, not a skip.
* For changed Markdown, run `python scripts/claim_check.py <file>` on each document, `python scripts/check_cairn.py` for internal links and claims, and `python scripts/link_check.py` for cross-references. Run `python scripts/quality_gate.py --sub neutrality` if doctrine or shipped templates change; neither is in the current scope. Snippet sync is N/A unless a synced source or block changes.
* The prior-manifest verifier is a manual Maintainer-triggered ceremony check, not a Boundary B gate or an automatic release phase. C2–C3 follow `bootstrap/REANCHOR_RUNBOOK.md`: the prepared `python scripts/repin.py verify-candidate` invokes the authenticated prior verifier with full collection against the candidate before the Maintainer's signing decision. Its HOLDs and errors are not replaced by Bandit or pytest.

Split test invocations within the guard's file limit and reconcile their union.

Boundary B is **wide** for this trust ceremony: after the final implementation commit, run the reviewed mapping on a clean unchanged commit; record tested SHA, range, interpreter, pre/post state, commands, counts, timings, non-pass dispositions, omissions and `Certified by: pending`. No full-suite certification or release run is implied; those occur only at authorized integration points. The protected-file pinning follows the runbook, not an old-anchor reconciliation invented here. Boundary C is the independent code reviewer's targeted falsification, including the recorded mutation and control.


## Plan review -- Codex (gpt-6.1-sol) -- 2026-10-29

```
Reviewed commit: 82bc87e4f6c0614c7437fd538f1c64d7368dc701
Target: scope, sequence, acceptance criteria and verification
Prior findings: none
Assurance path: Internal + Internal Security Review
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**Foundations**:

1. **Should this happen as framed?** The literal admission, removal before launch, refusal cases and collection controls deliver the accepted contract, subject to completing the verification map -- source proposal Current contract and plan C1.
2. **Best alternative.** Retain the existing boundary and producer cache option; moving the option to both launchers would add paths without improving the accepted outcome -- `bootstrap/tests/_gate_preflight.py:1900-1939`, `bootstrap/tests/_gate_manifest.py:514-523`.
3. **What would show it wrong.** A different collected node set under the admitted value, or a producer start after the appended selector, would defeat the plan's stated safety outcome -- plan C1 and source proposal Current contract.

**R1 -- blocking: make standing security gates reviewable before implementation.** Verification says to run applicable security gates and inspect their triggers, but names neither the gates nor their commands or properties. The template requires the reviewed mapping to identify every standing non-pytest gate for each touched surface before implementation; leaving discovery until execution prevents this review from checking whether the map covers the protected boundary. Identify the applicable gates, their triggers and properties, or record a supported N/A after inspecting the relevant triggers. Keep the mapped tests and scoped wide Boundary B; this does not call for a full suite. -- `dev/plans/_template.md`, Verification; plan Verification.

**Covered**: accepted scope and refusal cases (source proposal Current contract and plan C1); sequencing and Maintainer fence (plan C2-C3 and `bootstrap/REANCHOR_RUNBOOK.md`); consumer and verification mapping (plan Verification and R1); reuse and residual collection authority (plan Scope and source proposal Response); lifecycle and doctrine placement (plan header and Scope). The plan follows the runbook for pinning and does not require a separate historical-anchor reconciliation.

**Not covered / low confidence**: no independent execution, complete inventory of security gates, packet preparation, release run or Security Review. This pass clears only the ordinary plan-review obligation.


## Plan review -- Codex (gpt-6.1-sol), Security Review -- 2026-10-29

```
Reviewed commit: cb949cd25fb356b93ac5a8e4923a0cdf10e4d88a
Target: security boundary, acceptance criteria and verification mapping
Prior findings: ordinary R1
Assurance path: Internal + Internal Security Review
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised

**Foundations**:

1. **Should this happen as framed?** Yes, subject to the standing-gate mapping below: exact admission followed by removal preserves the accepted exception without admitting option parsing or collection selectors -- source proposal Current contract; plan C1; `bootstrap/tests/_gate_preflight.py:1900-1939`.
2. **Best alternative.** Keep compatibility handling at the existing launch boundary and reuse the producer's explicit cache flag; changing the release and grandchild launchers adds surfaces without delivering another accepted outcome -- `bootstrap/tests/_gate_manifest.py:514-523`, `bootstrap/security_check.py:983-1058`, `scripts/quality_gate.py:148-177`.
3. **What would show it wrong.** A producer marker after refusal, a different admitted node-identity set, or lost release enforcement in the real grandchild defeats the plan; its criteria name these experiments -- plan C1; `bootstrap/tests/test_gate_preflight.py:858-870`; `bootstrap/tests/test_security_check.py:785-829`.

The plan keeps the security-sensitive distinctions intact: empty ADDOPTS is
refused rather than treated as absent; both plugin variables refuse by
presence, including empty and combined cache/plugin cases; diagnostics disclose
names without values. Removing only the admitted literal before launch avoids
passing redundant inherited options to the producer. The guard remains on the
actual child environment immediately before execution, after scrubbing. Scope
explicitly retains trusted candidate collection and interpreter execution;
there is no new containment claim or widened environment authority.

**S1 -- blocking, shared satisfier with ordinary R1: name the standing security
checks before implementation.** The mapped pytest families cover the named
boundary and release propagation, but “applicable security gates” still leaves
the non-pytest map unspecified. This matters concretely:
`bootstrap/security_check.py` includes the changed preflight in
`_CEREMONY_CLOSURE_PY`, and `run_bandit()` scans the derived executable surface
and refuses missing/error evidence. Name the scoped command that invokes this
check and its property without invoking the entire release runner, together
with the other applicable standing gates or evidenced N/A dispositions.
Retain C2–C3's runbook prerequisites and prior-verifier checks; do not substitute
a green pytest selection for protected-file pinning. Satisfier: fold that exact
command/property/trigger map into Verification, answering ordinary R1 and this
finding together -- `bootstrap/security_check.py:683-696`,
`bootstrap/security_check.py:856-875`; `bootstrap/REANCHOR_RUNBOOK.md`,
“Run the maintained verifier and ceremony”; `dev/plans/_template.md`, Verification.

**Covered**: claims, completeness and fail-closed cases (plan C1 and launch
boundary); real public-path and release consumers (mapped preflight,
security-check and quality-gate tests); reuse and drift (reader search for
`gather_evidence`, `PYTEST_ADDOPTS`, `_release_child_env` and
`_run_order_independence` across bootstrap, scripts and docs, confirmed against
the known preflight and release launch sites); lifecycle and scope (accepted
contract, plan C2–C3 and runbook); satisfier (S1).
**Not covered / low confidence**: no implementation execution, mutation run,
complete standing-gate inventory, candidate packet, plugin-package audit,
full-suite certification or release ceremony. This is the fresh-context
Security plan pass; the author's operative-cell fold must resolve S1 before
implementation.


## Response to plan review -- Codex (gpt-6.1-sol) -- 2026-10-29

| Finding | Disposition |
|---|---|
| R1, S1 | Accepted. Verification now names the directly invoked Bandit phase, its closure and failure properties, documentation checks and conditional gates, and the Maintainer-triggered prior verifier. The scoped test map includes scan-coverage tests. |

## Implementation verification -- Codex (gpt-6.1-sol) -- 2026-10-29

**Implementation verified at** `0c07eb373f0a97197eeaddbb3399483cf960f888`.
**Boundary B mode**: wide
**Certified by**: pending
**Range**: `35cf29f492ad226f513b7a09f9e1b215c57b1ada..0c07eb373f0a97197eeaddbb3399483cf960f888`.
**Interpreter**: Python 3.13.13 (`/Users/kendal30/conda_envs/lhm/bin/python3.13`).
**Tree state**: clean before and after in a detached checkout at the tested SHA; `git status --short` was empty at both checks. `PYTHONDONTWRITEBYTECODE=1` prevented generated bytecode in the detached tree.

**Boundary A** ran on the implementation worktree before commit with the same mapping. The six mapped checks produced the outcomes below; the two signing-agent tests could not bind their socket in the managed environment. Their focused rerun is included in the Boundary B disposition.

**Boundary B commands and outcomes** (all from the clean detached checkout):

- `PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_gate_preflight.py -q` -- 335 passed, 2 failed in 156.74s. Both failures were before test assertions: `ssh-agent -s` could not bind its default socket under the managed environment.
- `PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_gate_preflight.py -q -k 'CandidateCodeCannotSignFromStageOne'` with approved host access -- 2 passed, 335 deselected in 0.58s. Together, the family checks passed all 337 tests.
- `PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_security_check.py -q` -- 111 passed, 3 warnings in 20.69s.
- `PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_quality_gate_order_independence.py -q` -- 10 passed in 2.42s.
- `PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_ceremony_review_report.py bootstrap/tests/test_gate_reanchor.py -q` -- 92 passed in 45.30s.
- `PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_security_lint.py -q` -- 11 passed in 1.91s.
- `PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -c 'import sys; from bootstrap.security_check import run_bandit; sys.exit(run_bandit())'` -- clean over 72 shipped files, 0 live allowlist entries.

The evidence tests prove the exact cache-only option is removed before producer launch, all other tested addopts and plugin controls refuse before launch, and real pytest node identities match with and without the cache-only option (2 nodes); `--ignore` drops a node and is refused through `gather_evidence` before the producer marker appears. The accepted-option producer marker passed.

**Omissions**: no full-suite certification, release run, prior-manifest verifier, packet preparation, pinning, signing, live ref operation, push, or historical comparison. C2-C3 and independent code review remain open. No known mapped consumer or required check remains unrun; the two socket-dependent cases passed in the focused rerun.

## Code review -- Codex (gpt-6.1-sol) -- 2026-10-29

```
Reviewed commit: 235eeb8a
Target: 35cf29f492ad226f513b7a09f9e1b215c57b1ada..0c07eb373f0a97197eeaddbb3399483cf960f888, and verification at 235eeb8a
Prior findings: none
```

**Obligation**: Internal
**Findings**: none

**Foundations**:

1. **Does it do what it claims?** The boundary admits the literal and removes it, and refuses other values and plugin variables before producer launch; the targeted controls passed -- `bootstrap/tests/_gate_preflight.py`, `TestEvidenceStage` controls below.
2. **Best alternative.** The existing boundary and producer cache option avoid a second policy or option parser; no simpler build preserves the accepted exact-match contract -- `bootstrap/tests/_gate_preflight.py`, `bootstrap/tests/_gate_manifest.py`.
3. **What would show it wrong.** Producer execution under a selector or plugin control, or retention of the admitted setting, would defeat the contract -- falsification ledger below.

**Bounding**: ACCEPTED. The changed launch boundary, its real collection control and the mapped downstream release and grandchild tests are covered by the author's wide record; the independent selector mutation challenged the boundary and its mapped tests.

**Falsification ledger** (detached checkout of `0c07eb37`, Python 3.13.13):

- Control: `python -m pytest bootstrap/tests/test_gate_preflight.py -q -k 'non_exact_addopts_refuses or plugin_control_refuses or exact_cache_option_is_removed or real_pytest_node_ids'` -- 12 passed, 325 deselected. This exercises producer markers, removal, plugin presence and real pytest collection identities.
- Mutant: replace exact comparison with a prefix comparison, admitting an appended selector. `python -m pytest bootstrap/tests/test_gate_preflight.py -q -k 'non_exact_addopts_refuses'` -- killed: 2 failed, 4 passed, 331 deselected; the appended selector and trailing-space cases reached the producer and failed the diagnostic assertion.

**Covered**: accepted scope and exact admission (`_gate_preflight.py`); producer refusal and removal plus node identities (ledger); release and real grandchild propagation and standing gates (implementation verification's mapped results); verification range and omissions (implementation verification); waiting-line history (`git log -p` over the range: no fenced chunk became the next move). The separate Security Review remains owed.

**Not covered / low confidence**: no full suite, release run, prior-manifest verifier, packet, signing, ref operation or historic anchor. Candidate code and collection remain trusted as the accepted contract states.

## Code review -- Codex (gpt-6.1-sol), Security Review -- 2026-10-29

```
Reviewed commit: 0c07eb373f0a97197eeaddbb3399483cf960f888
Target: 35cf29f492ad226f513b7a09f9e1b215c57b1ada..0c07eb373f0a97197eeaddbb3399483cf960f888; verification through 235eeb8a718a42118d824072d9f5acdba295b772
Prior findings: none
```

**Obligation**: Security Review of C1's protected evidence-launch boundary
**Tier**: Internal Security Review
**Findings**: none

**Foundations**:

1. **Should this happen as framed?** Yes: literal equality admits only the accepted cache setting, removes it before execution, and preserves presence-based plugin refusal on the scrubbed child environment -- `bootstrap/tests/_gate_preflight.py`, `gather_evidence`; falsification ledger below.
2. **Best alternative.** Keep this small boundary change and the producer's explicit cache suppression; parsing options or editing the two release launchers adds authority without improving this contract -- `bootstrap/tests/_gate_manifest.py`, `_collect`; `bootstrap/security_check.py`, `_release_child_env`; `scripts/quality_gate.py`, `_run_order_independence`.
3. **What would show it wrong.** An injected option or plugin reaching the producer, an admitted value surviving into its environment, or credentials surviving the scrub would defeat the boundary -- falsification ledger below.

**Bounding**: ACCEPTED for C1. The wide change-specific record covers the owning families, release/grandchild consumers and Bandit; the two socket-dependent failures have explicit successful rerun dispositions. C2-C3's packet, prior verifier and Maintainer-only signing remain open, rather than supplied by these results.

**Falsification ledger** (fresh detached checkout of `0c07eb37`; Python 3.13.13):

- Independent direct `gather_evidence` probe against a temporary committed marker producer, with explicit empty protected roster: absence and exact literal controls both launched; the producer saw no ADDOPTS, PYTHONPATH or injected credential-token variable, and HOME was redirected. Caller environment was restored afterward.
- The same probe crossed ten ADDOPTS states with absent, empty PLUGINS and empty DISABLE_PLUGIN_AUTOLOAD: 30 cases, two launches and 28 pre-launch refusals. Besides the controls, states were empty, leading tab, internal tab, trailing newline, appended terminal escape, appended selector, appended ignore and trailing nonbreaking space. Refusals left no producer marker; nonexact values were absent from diagnostics. No historical anchor or live ref was used.

**Covered**: claims, production boundary, edge cases and fail-closed behavior (ledger); reuse, drift and consumer consistency (known-positive search for `gather_evidence`, `PYTEST_ADDOPTS`, `_release_child_env` and `_run_order_independence`, followed by opening the boundary, producer and both consumer launch paths); lifecycle and scope (accepted contract, C1-C3 and verification through `235eeb8a`); satisfiers (no finding). Waiting-line history across the range reaches no Maintainer fence.

**Not covered / low confidence**: no independent full suite, release run, prior verifier, protected packet, pinning, signing, live ref operation or historical comparison; no plugin-package audit. Candidate code, interpreter execution and collection remain trusted. This clears only the C1 Security code-review obligation.

## Response to code review -- Codex (gpt-6.1-sol) -- 2026-10-29

| Pass | Disposition |
|---|---|
| Internal, `7a597268` | Accepted. No findings; accept C1's bounding. |
| Internal Security Review, `2c6443e9` | Accepted. No findings; accept C1's bounding. |

**C2 scope conflict**: no packet or reader inputs were created. C2's required packet is for this authority-closure change: the ordinary `repin packet` path refuses when a closure member differs from the anchor (`scripts/repin.py`, `build_packet`). The runbook's transition path (`transition-packet`, then `prepare-reader`) authenticates the prior anchor from its old roster against an independently supplied signer fingerprint (`scripts/repin.py`, command dispatch; `bootstrap/REANCHOR_RUNBOOK.md`, “For a reviewed authority transition”). This is the only documented packet path for a changed authority closure. The Maintainer's instruction excludes the old-anchor comparison/authentication needed by that path, so I did not run either command or inspect the live anchor. This blocks C2's accepted deliverables: ceremony inputs and the independent reader record. Removing those deliverables would remove accepted scope and needs the Maintainer's explicit allowance; none is recorded. C3's verifier decisions, pinning and signing remain untouched and Maintainer-only.

## Maintainer-authorized amendment -- Codex (gpt-6.1-sol) -- 2026-10-29

The following Maintainer authorization is verbatim:

> I am completely fine with not checking any changes against an anchor. We can re-anchor now
>
> Or rather, at v0.6
>
> They can each build the machinery, the new baseline does not need to be part of their plans. It can be a work board item for v0.6.
>
> Remove those requirements from the plans

**Scope delta**: C2's protected-change packet and independent reader record, and C3's prior-verifier dispositions, protected-file pinning and signing, are deferred out of this plan to the existing **Establish the v0.6 forward baseline** work-board item (`dev/PLANNING.md`). The item says comparison or reconciliation with the old anchor is not required and actual installation need not precede plan archive. The C3 Maintainer-only fence remains on that item; no C2 or C3 ceremony operation was run here.

**Loss**: this plan ships no packet, reader inputs or record, prior-verifier report or dispositions, pinned manifest or signature for candidate `0c07eb373f0a97197eeaddbb3399483cf960f888`. C1's implementation, tests, wide verification and both independent code reviews remain delivered. This amendment supersedes the earlier C2 conflict note, which accurately recorded that no scope allowance had yet been received. No prior-anchor comparison or reconciliation was performed.
