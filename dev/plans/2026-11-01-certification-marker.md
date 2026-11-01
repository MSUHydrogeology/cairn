# Plan: Remove the pending certification marker

**Source proposal**: dev/proposals/archive/2026-11-01-codex-certification-label.md
**Status**: ready-to-implement
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Remove the per-change pending marker while keeping checks and one record of each actual tree-certification run.

## Source proposal

The Maintainer accepted the heavy proposal at `8d1c6bde`: remove the mandatory marker,
retain checks and triggers, and record each actual run once in a discoverable existing
shared record. Do not backfill archived plans or create a ledger.

## Scope

Change `AGENTS.md`, `templates/core/AGENTS.md`, both plan templates,
`doctrine/plans.md`, `doctrine/dual-review.md`, `docs/glossary.md`, the refusal message
in `bootstrap/tests/conftest.py`, and affected rule tests and shipped copies. Search for
further live readers and pins before editing. Retain the guard condition, certification
pair, failure and bisect rules, and all Boundary B evidence except the pending field.
Historical records remain intact.

**Reuse.** N/A: no code added. Search for `Certified by`, `certifying run`, and the
refusal message found the above live rules and
`bootstrap/tests/test_certifying_run_rule.py` and
`bootstrap/tests/test_verification_boundaries.py`; the gate manifest pins `conftest.py`
and the former test. Existing guard and rule tests are reused.

### Documentation / doctrine surface

Governing and shipped rules hold the prescription; plan templates and doctrine explain
the record; the glossary describes the distinction. No new document or process is
introduced.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Align rules, templates, refusal message and existing tests | Both plan reviews and author response | The accepted outcome and scoped iteration evidence |

## Acceptance criteria

C1 removes the mandatory per-change field across current surfaces, without weakening any
required change check, certification trigger, guard refusal, failed-run handling or
bisect rule. Tests exercise those retained obligations and the actual refusal, and
reject a restored mandatory marker. Shipped rules remain appropriate to adopters. Each
actual run has one shared record: use the existing release or re-anchor evidence record
for those runs; for a required push or Maintainer-requested run outside those
ceremonies, record it in a commit message in shared project history, under `Tree
certification -- <tested SHA>`. An otherwise useful commit may carry the record; no
standalone commit is required. Include tested SHA, commands, results and existing
required evidence, including failures. Readers find it by searching shared history after
fetching the relevant refs; `git log --all --grep='Tree certification --'` searches local
refs only. Readers are told where to find each kind; no per-plan backfill or new ledger. Absence of a marker
does not prove that a run passed. Security preflight S2/S3: C1 tests the changed
obligations and real guard through the existing tests and scoped checks.

## Scope delta

**Scope delta**: preserved.

## Verification

Before editing, search live references, readers and byte pins, check known-positive
search cases, and run `python tools/test_tiers.py for <paths>` for the actual changed
files. Follow protected-file procedures; no re-anchor is authorized. Boundary A runs the
selected tests and applicable claim, link, snippet and neutrality gates. Verify the
guard still refuses the same broad invocation and test rule mutations against a passing
control. Inspect release and re-anchor evidence homes and demonstrate lookup of each
record type with representative existing evidence; record any gap rather than claim a
nonexistent example.

After independent code and Security Reviews, Boundary B is **wide** for governing and protected surfaces. On one clean unchanged final commit under canonical Python 3.13.x, run the reviewed-range iteration selection plus mapped integration/workflow tests, owning families, installed public paths and standing gates; record SHA/range, clean pre/post state, interpreter, commands, counts, timing, non-pass dispositions and omissions. Boundary C independently falsifies the implementation and mapping. No full certification or re-anchor is authorized by this plan.

## Plan review -- Codex GPT-6.1 -- 2026-11-01

**Tier**: Internal  
**Obligation**: Internal  
**Reviewed commit**: 71ac7ae1  
**Verdict**: ACCEPT; no blocking findings  
**Elapsed**: approximately 3 minutes  
**Tokens**: unknown

**Foundations**

1. **Should it happen as framed?** Yes. The accepted Decision removes the per-change marker while retaining checks and one discoverable record per run. C1 preserves triggers, guard, failure and bisect rules; its wide verification covers the governing and protected surfaces. The guard's current refusal condition is separate from its pending-message text (`bootstrap/tests/conftest.py`).
2. **Best alternative.** Keep the pending field and the SHA-keyed run entry described in `doctrine/plans.md`. That retains a per-change indication, but also the misleading instruction the Maintainer chose to remove. The plan uses existing ceremony records or a searchable commit message, without a new ledger.
3. **What would show it wrong?** A weakened trigger or refusal, a required check becoming optional, or an actual run whose evidence cannot be located would defeat the Decision. The plan calls for mutation checks and representative lookup; their outcomes remain to be established during implementation.

**Non-blocking recommendation.** Make clear how an ad hoc run's record becomes reachable in shared Git history and avoid requiring an otherwise unnecessary separate commit solely to create the record. The proposed `git log --all` search only finds commits present in the reader's local refs; demonstrate the intended lookup rather than treating the command alone as proof of accessibility.

**Coverage:** Read the committed plan, accepted proposal and Decision, current certification and bisect rules, and the actual guard message. Did not enumerate all readers or pins, run tests, verify record lookup, assess implementation wording, or perform Security Review.


## Plan review -- Codex GPT-6.1 -- 2026-11-01 (Security)

**Tier**: Internal Security Review  
**Obligation**: Internal Security Review  
**Reviewed commit**: ed5181da  
**Verdict**: ACCEPT; no security findings  
**Elapsed**: approximately 4 minutes  
**Tokens**: unknown

**Foundations**

1. **Should it happen as framed?** Yes. C1 explicitly retains missing-check blockers, conditional push certification, release/re-anchor triggers, the refusal condition and failure/bisect handling. Removing the pending message grants no bypass: the actual guard decides from override, release mode, collection mode and file span, independently of that message (`bootstrap/tests/conftest.py`). 
2. **Best alternative.** Use the existing release or re-anchor evidence record, with the proposed searchable commit message only for other authorized runs. This is the plan's approach: one actual-run record, no ledger or archived-plan edits. Another record would add burden without authenticating results. Evidence: Acceptance criteria; `docs/release-process.md` evidence home and pre-cut commands; `bootstrap/REANCHOR_RUNBOOK.md` ceremony evidence.
3. **What would show it wrong?** A missing check becoming optional, altered guard behavior, or an authorized run whose outcome readers cannot find. C1 requires retained-obligation tests, actual-refusal coverage, mutation checks and representative lookup. Current rule tests pin wording; implementation must retain obligation coverage (`bootstrap/tests/test_certifying_run_rule.py`).

The ordinary review's accessibility recommendation applies: lookup must reach shared history, including failed results. Existing evidence requirements suffice; no additional ledger, review stage or approval is needed.

**Coverage:** Read the committed plan, accepted proposal/Decision, plan template, governing certification/bisect rules, actual guard, rule-test source, release evidence guidance and re-anchor runbook. Did not run tests, enumerate every reader/pin, demonstrate lookup or review implementation bytes.

## Response to plan reviews -- Codex GPT-6.1 -- 2026-11-01

**Elapsed**: approximately 2 minutes
**Tokens**: unknown

- Internal: accepted the advice; the criteria now allow the record in an otherwise
  useful commit and distinguish shared history from locally fetched refs. Verification
  retains the representative lookup check.
- Internal Security Review: accepted; the same guidance covers failed results.

## Code review -- Codex GPT-6.1 -- 2026-11-01

**Tier**: Internal  
**Reviewed commit**: 46a0c967  
**Verdict**: REVISE; two blocking findings  
**Bounding**: WIDER RUN REQUIRED  
**Elapsed**: approximately 4 minutes  
**Tokens**: unknown

**Foundations**

1. **Should it happen as framed?** Yes, once the accepted record and verification requirements are met. The diff removes the marker while retaining the guard predicate, certification pair, trigger and bisect wording.
2. **Best alternative.** Retain the old marker and separate certification entry; that preserves a per-change field the Decision removed. Existing ceremony evidence and useful commit messages keep one record per run without a new ledger (`doctrine/plans.md`).
3. **What would show it wrong?** An adopter unable to locate run evidence or a required check without evidence defeats the accepted criteria and verification plan. Both gaps remain below.

**Blocking findings**

- The record instructions appear only in `doctrine/plans.md` and the local glossary; adopters receive neither. The shipped `templates/core/AGENTS.md` and plan template mention certification but do not say where actual runs are recorded or found. This misses the criteria that each actual run has one shared record and readers are told where to find each kind. Put the applicable instructions on shipped operative surfaces and verify them there.
- The implementation commit reports mapped tests and gates but does not report the required actual guard refusal, passing-control rule mutations, or representative lookup for each record type (or a documented gap). These are named C1 checks, not discretionary review reruns. Supply their evidence and dispositions before advancing.

**Evidence and coverage:** Compared the implementation diff with C1, inspected the shipped rules and focused tests, and ran both focused rule files against an archived copy of 46a0c967: 58 passed under the local Python 3.12 interpreter. The tests check doctrine wording but do not assert the record instructions on shipped surfaces. Did not run the full suite, repeat the mapped iteration, verify every reader or pin, or perform Security Review.

## Code review -- Codex GPT-6.1 -- 2026-11-01 (Security)

**Tier**: Internal Security Review  
**Obligation**: Internal Security Review  
**Reviewed commit**: 46a0c967  
**Verdict**: REVISE; ordinary review blockers remain, no additional security defect  
**Bounding**: WIDER RUN REQUIRED  
**Elapsed**: approximately 3 minutes  
**Tokens**: unknown

**Foundations**

1. **Should it happen as framed?** Yes. The committed diff removes the marker without changing the guard predicate: an AST comparison against its parent found every preceding statement identical when excluding the final diagnostic. Governing rules retain the certification pair, conditional push/release/re-anchor/Maintainer triggers, failed-run bisect and missing-check blockers (`AGENTS.md`, `doctrine/plans.md`).
2. **Best alternative.** Existing ceremony evidence plus useful commit messages is sufficient. The revised doctrine includes failures, tested SHA, commands/results and fetched-ref limits; another ledger or approval step adds no security assurance. The ordinary review correctly identifies that adopters still need these instructions on shipped surfaces.
3. **What would show it wrong?** Lost refusal behavior, optional required checks, or undiscoverable actual-run evidence. The ordinary review's two blockers identify unmet accepted outcomes and named checks; close them with shipped instructions and the already-required implementation evidence.

The author's four Python 3.12 Bandit skips do not establish scanner success. Their triggers are three real-scanner checks in `test_security_check.py` (severity ranking, missing-target refusal, clean scan) and the local `test_security_lint.py` gate. Local absence is explicitly skippable; the release command independently fails closed. Complete the planned canonical Python 3.13 wide Boundary B with these checks available, reporting any remaining non-pass outcome. No full certification or re-anchor is needed for this change.

**Coverage:** Inspected committed changed rules/tests, guard AST equivalence and scanner skip/fail-closed triggers. Did not rerun implementation tests, perform actual record lookup, enumerate every pin, run canonical Boundary B or the full suite. The ordinary review blockers and pending Boundary B keep the work open.
