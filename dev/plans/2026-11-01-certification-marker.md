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

## Response to code review -- Codex GPT-6.1 Luna -- 2026-11-01

**Elapsed**: approximately 5 minutes
**Tokens**: unknown

- **Shipped instructions:** Added the record location, required contents, shared-history search, fetch caveat, and absent-record caveat to both adopter surfaces. `test_shipped_guidance_records_and_finds_actual_runs` checks both surfaces and its mutated fetch instruction fails the guard.
- **Guard and rule controls:** On a fresh copy of `79418af6`, `test_a_run_over_the_file_threshold_is_refused_regardless_of_selector` passed; it asserts real pytest invocations return the broad-run refusal both bare and with a selector option. The same targeted run passed `test_the_broad_run_refusal_no_longer_offers_the_override`, `test_shipped_guidance_records_and_finds_actual_runs`, and `test_record_schema_guard_detects_removed_reviewed_range`; their controls mutate conditional-push wording, fetch guidance, and the reviewed-range field.
- **Lookup results:** `docs/release-process.md` directs readers to `dev/strategy/archive/2026-05-27-claude-cairn-pre-release-sweep.md`, which records a historical full-suite result (264 passed, 2 skipped). It has no tested SHA or interpreter, so it is a location example, not a complete record under this plan. The re-anchor authorization in `dev/plans/archive/ceremony-without-external-review.md` explicitly says the full suite was waived; no re-anchor certification example exists there. `git log --all --grep='Tree certification --'` found no actual-run commit in locally available refs. A separate known-positive `git log --all --grep='Ship discoverable tree-certification records'` found `6772ff55`; this validates the search command, not certification evidence. These historical gaps remain; no archive was backfilled.
- **Checks:** On Python 3.13.13, the four focused nodes passed in 0.98 seconds; the selected five test files passed 123 tests in 4.18 seconds. Claim, link, snippet, and neutrality checks passed for the two changed adopter documents (neutrality: 0 failures). No full suite or re-anchor ran. The two changed rule-test files are gate-manifest-pinned; baseline refresh remains for the Maintainer's v0.6 cut, as the accepted plan directs.

**Coverage:** Both review findings are addressed with shipped text and targeted evidence. The record search found no complete historical example for re-anchor or ad-hoc runs; this gap is stated rather than filled with a fabricated record. Boundary B and independent review remain due.

## Targeted code review -- Codex GPT-6.1 -- 2026-11-01

**Tier**: Internal  
**Reviewed commits**: 6772ff55, 79418af6, 0914d80c  
**Verdict**: Both ordinary review findings closed  
**Elapsed**: approximately 2 minutes  
**Tokens**: unknown

**Foundations**

1. **Should it happen as framed?** Yes. Both shipped surfaces now name the record homes, contents, search and local-ref limitation; the focused test checks both.
2. **Best alternative.** Put the guidance only in one shipped surface and reference it from the other. The present wording makes the instruction available in both contexts without adding a ceremony.
3. **What would show it wrong?** Missing or misleading run evidence would defeat discoverability. The author's lookup reports the incomplete historical examples and absence of an ad-hoc example rather than presenting them as complete.

The author reports the real guard refusal, passing mutation controls and representative lookups with their gaps in 0914d80c. These close the missing-evidence finding; wide Boundary B remains due. **Bounding**: WIDER RUN REQUIRED for the planned final integration, not a new review check.

**Coverage:** Read the correction diffs and author response against both findings. Did not rerun implementation checks, perform Security Review, or assess the remaining Boundary B results.

## Security review disposition -- Codex GPT-6.1 -- 2026-11-01

**Obligation**: Internal Security Review  
**Reviewed commits**: 6772ff55, 79418af6; evidence response 0914d80c  
**Verdict**: ACCEPT; prior blockers closed, no new security finding  
**Bounding**: ACCEPTED for the planned wide Boundary B selection  
**Elapsed**: approximately 2 minutes  
**Tokens**: unknown

**Foundations**

1. **Should it happen as corrected?** Yes. Both shipped surfaces now require one actual-run record, identify ceremony evidence and shared-history fallback, include failures, and explain fetched-ref search limits and the absent-record caveat. These changes close the discoverability gap without changing the runtime guard or authorization triggers.
2. **Best alternative.** The corrected reuse of existing records delivers the accepted scope with no ledger, backfill, extra approval or standalone record commit. Keeping instructions only in local doctrine would leave adopters without them.
3. **What would show it wrong?** A bypass of the retained checks or evidence falsely presented as certification. The author reports the real refusal and mutation controls under Python 3.13.13, and labels incomplete historical examples as gaps rather than passed runs. The corrected guidance test covers both shipped surfaces; its normalization fix changes the control, not the rule.

Read the correction diffs and committed response; corroborated the release evidence pointer and explicit historical re-anchor waiver. The response supplies the previously missing named-check evidence. Historical gaps are disclosed as the plan permits. Complete canonical wide Boundary B, including disposition of the previously skipped real-Bandit checks; this acceptance does not substitute for that run.

**Coverage:** Targeted look at the correction and prior findings only. Did not rerun implementation checks, run broad tests, verify every historical record, or perform certification/re-anchor. No additional security pass is owed for these closed findings.

## Implementation verification -- Codex GPT-6.1 Luna -- 2026-11-01

**Boundary B: wide**; final tested commit `0d15f164`; implementation commits
`46a0c967`, `6772ff55`, `79418af6`; changed paths: `AGENTS.md`,
`bootstrap/tests/conftest.py`, `bootstrap/tests/test_certifying_run_rule.py`,
`bootstrap/tests/test_verification_boundaries.py`, `dev/plans/_template.md`,
`docs/glossary.md`, `doctrine/dual-review.md`, `doctrine/plans.md`,
`templates/core/AGENTS.md`, `templates/core/dev/plans/_template.md`.
Canonical `/Users/kendal30/conda_envs/lhm/bin/python`: 3.13.13. A fresh
`git archive 0d15f164` copy was used; `PYTHONDONTWRITEBYTECODE=1` for all
Python runs. Clean pre/post: its 836-file SHA-256 inventory matched a fresh
archive after removing only pytest's temporary `.pytest_cache` (no source
changes). Elapsed: pytest selections 8.66s reported by pytest; prose gates and
snapshot comparison completed, exact combined wall time not captured.

- Mapped iteration and integration/workflow selection: `python -m pytest
  bootstrap/tests/test_replacement_tools.py
  bootstrap/tests/test_scientific_check_guidance_ships.py
  bootstrap/tests/test_session_routines.py
  bootstrap/tests/test_status_vocabulary_advisory.py
  bootstrap/tests/test_verification_boundaries.py -q` — 123 passed, 4.55s.
  The selector reports 46 other AGENTS.md readers omitted by its guard; no
  additional suite was run.
- Bandit controls (Bandit 1.9.4 present): fail-closed when absent, scanner
  error, real missing-target refusal, clean real scan, Bandit's severity
  ranking, and local `test_no_blocking_security_findings` — 6 passed, 3
  warnings, 4.11s; zero skipped.
- Standing prose gates on both changed adopter surfaces: claim checks, links,
  snippet sync — all passed. Quality neutrality: 0 failures, 43 informational
  findings.
- The real broad-run refusal, mutation controls and representative run-record
  lookup were exercised and documented in the preceding implementation
  response. Historical records remain incomplete as described there; no
  archived record was changed. No full suite or re-anchor was run.

**Non-pass disposition:** none. The 46 selector-omitted AGENTS.md readers
remain outside this mapped selection; the standing release certification is
not part of this implementation Boundary B.
