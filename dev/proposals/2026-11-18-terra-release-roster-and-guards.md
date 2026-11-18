# Refresh the release roster and decide held guards

**Author**: gpt-6.1-terra (Implementation, Medium)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy — the protected release roster and guard tests may change
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-18
**Rules that apply**: dev/rules/conventions.md, dev/rules/protected-surfaces.md, dev/rules/working-agreements.md
**In brief**: Refresh the Mac and Windows release-test roster and decide whether its held tests still earn their cost.

## Decision summary

The prepared roster predates later test changes, and 28 held guards await a decision. Refresh the roster and choose whether to keep all 28 or retire only those with demonstrated protection. Retirement may need explicitly authorized further Security Review. Assess the now-unfenced claims-tool tests too. This proposal does not run or sign a baseline.

## Context

The Group 5 rows in `dev/PLANNING.md` record the paused refresh and 28 holds. Prepared commits `345d0161` and `ae321704` added 99 POSIX-only rows, removed seven deleted nodes and recorded 63 Windows-only and 742 POSIX-only entries then, not now. Twenty Git-read route nodes have since become Windows-capable. The archived [promise-testing plan](../plans/archive/2026-11-08-promise-unit-testing.md) records the 28 holds: 24 roster entries, two shipped-source guards, one parity check and one release-procedure step. The deleted worklist is recoverable from Git before `546959c1`; source inspection found all 28 named functions still present, but did not establish their current roster membership or protection equivalence.

The Maintainer said on 2026-11-12, “retire now unless it disrupts the re-anchor”; the holds remained because of that condition. On 2026-11-13 they also said, “The rest you just take care of, please. I don't want loose ends left around.” The [warn-only Decision](archive/2026-11-16-claude-claims-check-warn-only.md) later lifted the pruning fence specifically on `tests/test_intents_tool.py`, with a later pass owning the assessment; it did not authorize an indiscriminate cut or establish that every related claims file was unfenced.

## Proposal

Reconcile `tests/security_manifest.py` with current Mac and Windows behavior, using the prepared commits as historical inputs. Remove deleted or obsolete IDs, including the 20 now-Windows-capable Git route entries if present; include only genuine opposite-platform setup skips. Resolve the setup skip in `tests/test_rules_folder_offer.py::test_count_command_and_offer_text`, the illegal-filename call-phase skip in `tests/contract/test_board_closeout_warning.py::test_warning_escapes_untrusted_name_and_never_shows_closeout`, and the four fixture skips in `tests/test_upgrade_removes_retired_files.py` by their actual behavior. Account for the 15 Windows-only nodes missed in the earlier rerun, and investigate in-body symlink-privilege and POSIX skips, which cannot simply be roster entries. Account for Windows Gitleaks, Bandit and Vermin availability; a missing tool, unexpected skip, xfail or xpass cannot be a strict pass. Current evidence determines the final roster and identity.

Choose one disposition for the 28 at Decision:

- **A — retain all.** Refresh the roster and keep the existing guards and their named references. This avoids a protection change but retains their runtime and maintenance cost.
- **B — retire eligible guards in the same update (recommended).** Reconcile each historical row to its current owner; a High-tier assessment identifies its public promise and distinct protection. Remove a guard only where an existing or focused public-entry check retains that protection and its other named roster, shipped-source, parity or release-procedure duties are correctly resolved. Keep a guard when equivalence is not established; do not turn an unproven removal into a pass. Update roster and references together; time and final cut count are unknown.

Assess `tests/test_intents_tool.py` under its now-lifted fence for redundant private-helper or same-branch tests, preserving the warn-default and explicit-block public promises and distinct refusal classes. Remove only eligible redundancy, if any; keep the rest. Add no unrelated claims-family expansion or mutation ledger.

The old code Security Review has reached its cap. This proposal's review examines the proposed change; it cannot clear or reset the old code obligation. If option B needs another pass over that capped code, stop and seek the Maintainer's explicit authorization for this specific question: **would removing the identified held guards leave a public path to unsafe writes, bypassed containment or a false release-gate pass without a retained check?** Scope the request to the proposed guard removals, their retained public witnesses and affected roster/reference changes; its value is detecting a lost protection before the single baseline update. No extra pass is authorized by this proposal alone.

## Rationale

One reviewed baseline update avoids changing the protected list twice and exposes the continuing burden and security tradeoff.

## Alternatives considered

Refresh only and postpone all guard decisions: smaller immediate work, but the held tests and potentially another roster change remain. Remove all 28 by count: cheaper to describe, but could silently remove a unique safety or release check.

## Documentation / doctrine surface

The deliberation stays in `dev/`; changed roster and tests belong in `tests/`, and any affected shipped-source or release-procedure references stay in their existing homes. No governance rule, signing or re-anchor is authorized by this proposal; a separate Maintainer-owned baseline operation remains a release prerequisite.

## Evidence / verification plan

The result fails if a required test is wrongly excluded, an unexpected skip is accepted, a removed guard loses protection or claims warn/block behavior changes. Reconcile names, test known-positive searches and record platform gaps. A strict record stays unpassed until its evidence exists.

### Tests required

Before changes use `/Users/kendal30/conda_envs/lhm/bin/python3.13 tests/tier_inventory.py for <changed paths>` and select affected public-entry nodes. Check roster identity and classification, warn-default and explicit-block claims behavior, and one representative negative per distinct changed refusal class. On Windows exercise the actual relevant native paths, including previously skipped nodes; on Mac exercise the applicable counterparts. Record exact commands, versions, skips and results. No permanent wording test, per-variant mutation ledger or repeated broad family is requested; the arc owner joins integration once at the end.

### Examples / smoke checks

Use source inventory and known-positive controls to verify roster additions and removals. Run claim check and applicable link, snippet, neutrality and prose-integrity gates on changed documents. A full certifying run, scanner installation and signing occur only under their existing release triggers, not to author this proposal.

#### Security preflight — five questions, answered in writing

**S1:** Maintainers and reviewed source supply the roster and test changes; platform results and project inputs may expose hostile paths or missing tools. The release runner selects by the roster, so a mistaken row can hide an omission.

**S2:** An omitted required node, an unexpected skip accepted as valid, or a disabled retained refusal should make its respective public check fail. One focused negative per changed refusal class distinguishes the protection; source count alone cannot.

**S3:** The reviewed plan binds exact `tests/tier_inventory.py` selections, public test nodes, platform commands and input sets to the final candidate. The existing release runner consumes the roster; its full record is a separate release operation, not evidence supplied by this proposal.

**S4:** Missing tools, unsupported skip classifications, uncollected roster IDs or unproven guard coverage leave the strict record unpassed and the affected guard retained. No silent waiver or roster bypass is authorized.

**S5:** A malicious project or defective runner can exercise a boundary outside the sampled cases. A focused negative does not prove every hostile input or security equivalence; retained protections and independent review remain necessary.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A platform's strict record hides a skipped required test, an actually supported Windows path is excluded, or a retired guard's unique protection cannot be demonstrated through a retained public check.

## Scope delta

**Scope delta**: preserved.

## Assurance path

Usual and Security proposal review, a heavy plan with Internal and Internal Security Review, and independent ordinary and Security code review as applicable. The existing cap and any explicit extra-pass authorization remain in force. No roster change, release record, signature or Maintainer Decision is claimed. Elapsed: unknown; tokens: unknown.

## Review -- Terra (Reviewer, Medium) -- 2026-11-18

**Reviewed commit**: cad52724f43cb26e7c12066caf0ec2e18c5929b2
**Tier**: usual
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: the choice makes the cost of retaining guards and the conditions for retiring them visible while updating platform classifications. -- Decision summary, Proposal options A and B
2. **Best alternative.** Retain all guards and refresh only the roster; it avoids removal risk but preserves their runtime and maintenance burden. -- Proposal option A, Alternatives considered
3. **What would show it wrong?** A strict record accepting an unexpected skip or a removed guard leaving a distinct unsafe path unchecked would falsify the result. -- Evidence / verification plan, Security preflight S2–S4

Option B retains a guard when equivalence is unproven and specifies the unresolved question for any explicitly authorized extra pass; this proposal cannot reset the old review cap. The now-lifted claims fence is scoped to the named file and public warn/block promises. The proposed longer opening supplies the decision and platform context rather than a per-test ledger. No governing rule change is proposed; roster and release work remain in their existing homes. Coverage: read the committed proposal, template and relevant archived hold disposition; did not collect tests, run either platform, establish current roster membership or assess the security boundary. Security Review remains separate.

## Review -- Codex Sol (Security Review, High) -- 2026-11-18

Reviewed commit: cad52724f43cb26e7c12066caf0ec2e18c5929b2

**Tier**: Security Review
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Steelman.** Refresh the native roster against actual behavior and retire a held guard only when its protection and any named procedural duties survive.

**Foundations**

1. **Should this happen as framed?** Yes. Only known opposite-platform setup skips are eligible. Missing tools, call-phase skips and unexpected outcomes leave evidence unpassed (Proposal S1–S4, `release/security_check.py:329-381`).
2. **Best alternative.** Option A keeps all 28 guards while refreshing the roster. It avoids losing a distinct protection and retains their current cost (Proposal A–B, archived promise-testing closeout).
3. **What would show it wrong?** A native-only test skipped on its own host, an omitted required ID accepted, or a retired guard's public failure path going undetected (Proposal Verification and S2–S4).

**Protections and authority.** Option B requires a public witness for each distinct protection and resolves named roster, shipped, parity and procedure duties. Unproven guards stay. Claims pruning stays within the named file and retains warn-default and explicit-block behavior. Any extra pass on the capped code requires the Maintainer's explicit authorization for the question as scoped in the Proposal. This pass grants no such authorization.

**Coverage.** Read the committed proposal, hold disposition, claims Decision and current outcome validator. No native test collection, execution, guard-equivalence assessment or old-code review ran.
