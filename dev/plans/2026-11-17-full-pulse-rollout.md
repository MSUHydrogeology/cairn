# Plan: Offer Meter and deliver the full pulse

**Source proposal**: dev/proposals/archive/2026-11-17-terra-meter-adopter-rollout.md
**Author**: GPT-6.1 Terra (Medium)
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-17
**In brief**: Offer Meter setup with consent and deliver the complete pulse at every goodnight.

## Build summary

Offer informed Meter setup at attended session start. At each explicit goodnight,
produce the complete existing pulse with current-project usage from that refresh.
Share the pulse implementation with adopters and the future website; preserve
all fields and text. Keep the separately locked pre-prune refresh at full
handoff, even though two refreshes may run.

## Source proposal

The Maintainer accepted the reviewed full-scope proposal at `a802dada`:
“Accept and implement”. The required plan reviews precede implementation.

## Scope

Move Gauge's pulse and Audit’s pure artifact validation/reduction into
`tools/pulse.py` and its shipped twin `templates/skills/_lib/pulse.py`, a
standard-library-only module; retain Gauge's Git classifier and Audit's
producer. Install the module once, and add Meter's report entry, both copies of
the session skills, installed and Cairn measurement guidance, and focused tests.
Do not implement the website, change consent automatically, introduce a new
collector, commit an aggregate, or remove any existing pulse view. Follow the
source proposal's Security Review preservation notes and existing privacy rules.
Repair the existing wait-export work-limit failure as a prerequisite to a fresh
report; it changes neither the output contract nor the work limit.

Shared module paths:
- `tools/pulse.py`
- `templates/skills/_lib/pulse.py`

## Sequence

After the plan reviews, one Low-tier implementer executes C1–C4
in order. Claim exact paths; inspect the shared tree and safe-Git pins before
each chunk; stop on overlapping edits or a needed scope change. Edit each
shipped template first and copy to its twin; compare bytes. One explicit-path
commit per chunk. Use the changed-file selector to identify owning checks; run
the smallest checks of changed public promises and required prose gates. No
broad suite. Estimate 3–5 working days, unmeasured, not a mandatory duration; Windows current-project
binding and extraction of the pulse/Audit cycle are the principal uncertainty.

**C1: Extract and install.** Move Gauge's `_PULSE_*`, bounded readers,
parsers, comparison, builder and text renderer, plus Audit’s `_pulse_*` pure
validation/reduction helpers, into `pulse.py`. Keep Audit’s `_pulse_input`
producer and its path/identity checks; make it call the sibling pulse reader
and reducer, eliminating the Gauge/Audit dynamic cycle. Keep Gauge's non-pulse
code; delegate `--pulse` through shared argument registration. Add a standalone
pulse CLI and one install mapping. Load the sibling from the tool's own location,
never from an input or target root. Preserve all options, exit behavior,
`cairn-pulse/1` fields and text. `read_inputs(options, meter_aggregate_bytes=None)`
rejects simultaneous path and bytes, applies the same aggregate and cumulative
limits and strict schema to bytes as to a file, and retains path identity,
no-link/reparse, regular-file, XML entity, strict JSON and artifact/project
checks. `build_pulse` and `render_text` operate on validated inputs.

**C2: Fresh Meter report.** In both POSIX and Windows refresh paths, collect
only the selected current project's sanitized `_project_export` from the same
candidate that is successfully committed, exported and revalidated. Resolve the
current directory to exactly one configured, approved project using existing
project verification; no match or ambiguity provides unknown usage, never a
previous aggregate. Pass the bytes in memory to the shared module only after the
refresh and publication succeed. `refresh --report` registers the pulse options
but rejects `--meter-aggregate` before collection even on failure. A partial or
failed refresh reports its closed status and reason without stale usage; disabled
Meter may render explicitly supplied public inputs with unknown usage. Keep
`refresh --json` and its exit codes unchanged. Do not put raw child diagnostics,
source keys, paths or other-project data in reflections.

First repair `_wait_artifact_map` in both Meter copies: for each existing claim
group parse closed intervals once and sort by start. Sweep positive-duration
intervals, retaining the prior interval with greatest end; if the current start
is strictly before that end, mark both keys as overlapping, then retain the
later end. Zero- or negative-duration intervals do not enter the sweep. Charge
one comparison for each subsequent closed record to the existing counter and
retain its 100,000 limit. Keep owner collisions, open claims, later wait/claim
candidate comparisons, inclusive containment, confidence, targets and all other
limits unchanged. This changes the closed-claim overlap pass from quadratic to
sort plus linear sweep; the separately guarded wait/claim loop can still refuse.

**C3: Session guidance.** At an attended explicit session start, offer setup
when Meter is installed and no consent or remembered refusal exists. Show the
proposed roots, projects, private ledger, aggregate and recurring cost; write
configuration only after a yes. With permission, store a non-private refusal
instruction in the existing custom session routine; reoffer on request. If the
person declines to remember a refusal, no refusal is persisted. Unattended starts
do not offer, read private sources or write configuration. At every explicitly
invoked goodnight, run the report and include sanitized results or closed status
in the reflection. Preserve the full-handoff lock and pre-prune behavior. Update
both skill copies and guides, and document explicit public pulse inputs.
Replace Cairn's existing Goodnight `refresh --json` plus Gauge reading a saved
aggregate in `dev/rules/custom_session_routines.md` with this fresh report route;
retain its consent and no-commit duties and the separate locked pre-prune refresh.

**C4: Joined verification and closeout.** After code review and dispositions,
use the changed-file selector over the joined paths to identify owning checks;
run the smallest public-promise and synthetic installed and upgraded entry-point
selection once, retaining every required proposal check. Remove temporary
private-helper debugging tests. Record exact commands, interpreter, results,
elapsed time and omissions; measure both refresh calls on stated synthetic
inputs. Update the normal roadmap, changelog and lock records at closeout.

## Acceptance criteria

**C1:** Existing Gauge pulse text and JSON match shared and standalone outputs
for all views, before/after inputs and omitted inputs. Existing bounded-input,
artifact and project-mismatch refusals hold. Gauge's non-pulse behavior and
Audit's producer remain available; the installed module has no sibling runtime
or third-party dependency, and its source twins match.

**C2:** Public Meter report uses only fresh approved current-project usage;
unconfigured or ambiguous projects, partial or failed refreshes and old exports
never produce stale counts. Aggregate-path override is rejected even on failure;
bytes share path limits. Default receipts and handoff behavior are unchanged.
The wait export preserves overlap and attribution results, including touching,
nested and empty intervals, while a large group of non-overlapping closed claims
no longer spends the old pairwise budget.

**C3:** Fresh and upgraded adopters receive the attended offer, explicit consent,
optional remembered refusal and requested reoffer. Unattended operation makes
no offer or private read/write before consent. Reflection-only and full handoff
report honestly; no private source data or other-project usage enters reflection.

**C4:** Joined installed-entry checks cover the above promises, both refresh
calls are measured with stated limits, required reviews and checks have been
disposed, and the source twins and install lock match.

## Scope delta

None. Any later loss of accepted scope needs the Maintainer.

## Verification

Reuse `bootstrap/tests/integration/test_gauge.py` pulse, artifact and boundary
cases and `bootstrap/tests/integration/test_meter.py` receipt, export and native
reader cases. Extend their public-entry tests for C1–C2 rather than pinning
private helpers. Exercise installed and upgraded skills via existing scaffold
and session integration homes, with synthetic sources only. Compare full text and
JSON, including baseline, tier and artifact options; exercise invalid paths,
oversize and duplicate JSON, XML entities, mismatched project, conflicting path
and in-memory inputs. Use configured project A and unconfigured B with an old
aggregate; failed and partial refreshes must not report B's stale usage. Check
consent, refusal, unattended behavior and both goodnight modes. Apply
`python tools/test_tiers.py for <changed paths>` to identify owning checks and
run the selected public-promise checks and prose gates; name exact nodes and
platform limitations in the implementation record. One joined
synthetic install/upgrade run follows C3. Windows native evidence remains due
for the changed Windows report path; no private logs, whole suite or real-world
billing accuracy is claimed.

**Focused public controls.** Add these named nodes to the existing test homes;
run each with the project interpreter using `python -m pytest -q` and the full
node names below. Inputs are synthetic, with project A approved and project B
unconfigured and holding an old export. `bootstrap/tests/integration/test_meter.py::test_report_freshness_public` covers B, partial and failed refreshes, and
an aggregate path plus bytes, asserting no stale usage and refusal of the
override even after failure.
`bootstrap/tests/integration/test_meter.py::test_public_refresh_exports_many_closed_claims_without_pairwise_work`
uses public refresh with 450 same-identity closed claims: 445 disjoint earlier
claims, A[11,12], B[12,13], C[14,17], D[15,16], E[16:30,18]. Two one-second
waits at 12:00 and 17:30 yield two executions and 2,000 ms each of execution
and wall time; only B's execution gets artifact attribution. Assert the `ok`
receipt and no raw identifiers or paths in the export. The old pair loop exceeds
100,000 comparisons; the sweep and candidate scan use 1,349. Rerun with
`run_main_with_synthetic_home`'s `MAX_WAIT_EXPORT_WORK=448` override: expect
`unavailable/source_budget_exceeded` and the prior sanitized export unchanged.
The ledger may already have committed. Use a temporary small pairwise oracle on
generated intervals including empty intervals to compare overlap sets; remove it
after recording its result. Reuse `test_public_refresh_repeat_and_rebuild_publish_distinct_project_exports`,
`test_retained_wait_binding_is_sticky_across_refresh_and_rebuild`,
`test_the_export_shows_folded_days_without_an_artifact_and_waits_are_unchanged`
and `test_wait_rows_bind_dedupe_retain_and_export_sanitized_utc_totals` in the
same Meter test file. If the later wait/claim loop still exhausts its unchanged
limit, stop and report that distinct failure; do not increase the cap or drop
attribution.
`bootstrap/tests/integration/test_gauge.py::test_full_pulse_public_parity` compares
text and JSON for Gauge and the installed shared CLI with JUnit, baseline, tier,
artifact and aggregate inputs. `bootstrap/tests/test_session_routines.py::test_meter_offer_and_goodnight_public` covers attended consent, refusal and requested
reoffer, unattended silence, and both goodnight modes through installed guidance.
The joined install and upgrade smoke uses these same public entries after C3.

For the accepted S2 negative controls, temporarily break one protection at a
time and run its single corresponding node: allow old B's aggregate; allow stale
usage on partial or failed refresh; allow collection on refused or unattended
setup; and allow an aggregate-path override with bytes. Each targeted node must
fail with its mutation and pass unmutated; remove mutations and record outcomes.
These controls establish the tests can detect the named boundary failures; they
do not authorize private data or a new test framework.

## Plan review -- GPT-6.1 Terra (ordinary reviewer, Medium) -- 2026-11-17

Reviewed commit: dcface9ac6cd501c95e809cff0ebae6f3f99a357

**Obligation**: Assess whether the plan executes the accepted full-pulse outcome and its required checks.
**Tier**: Internal
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: approximately 4 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes: the Maintainer accepted the entire pulse, consented setup and both goodnight modes; C1–C3 retain those outcomes. -- accepted proposal, Decision and items 1–5
2. **Best alternative.** One dependency-free extraction reuses the existing pulse without shipping Gauge's unrelated classifier; existing public-entry tests provide the leanest evidence. -- `tools/gauge.py`, `tools/audit_report.py`, `bootstrap/tests/integration/test_gauge.py`
3. **What would show it wrong?** An installed or upgraded entry loses a view or reports stale or other-project usage. -- plan C1–C4 and Verification

**Blocking:** The accepted proposal's S2 requires *failing mutations* for old unconfigured-project aggregate, partial or failed refresh, refused or unattended setup, and conflicting aggregate path and bytes. The plan lists scenarios but does not require showing that their controls fail when protections are broken. S3 also requires the plan to name exact test commands and input sets; the plan defers exact nodes to implementation. Specify the controls and runnable gate commands or concrete new test nodes and inputs, retaining the existing public checks and avoiding broad reruns. -- accepted proposal, Security preflight S2–S3; plan Verification

**Coverage:** Read the plan and accepted proposal, current template, Gauge and Meter test entry points, Audit reducer/loader, install mapping and session skill entry points. Source inspection only; no test runs, private data, Windows execution, cost measurement or independent Security Review. The proposed functional prose does not explicitly remove a rule; its final wording remains for code review.

## Plan review -- Sol High -- 2026-11-17

Reviewed commit: dcface9ac6cd501c95e809cff0ebae6f3f99a357

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown
**Model basis**: assigned Sol High Security Review.

**Foundations**

1. **Should this happen as framed?** The extraction preserves accepted boundaries, but the existing goodnight route and required controls need explicit reconciliation. -- plan C1–C3; findings 1–2
2. **Best alternative.** Keep the dependency-free extraction and route Cairn's custom goodnight instruction through the same fresh report. -- `dev/rules/custom_session_routines.md`, Goodnight
3. **What would show it wrong?** Goodnight in unconfigured B with an old aggregate must never report that usage; breaking the fresh-project control must make its check fail. -- accepted S2–S3; Meter `_project_export`

1. **Blocking -- reconcile the live custom route.** The session-end skill runs project custom steps. Cairn's Goodnight section still mandates `refresh --json` followed by Gauge reading the existing aggregate, which can report stale usage for an unconfigured current project. C3 does not name this operative file. Include its reconciliation with the fresh report, retaining the separate locked pre-prune refresh. -- `.agents/skills/session-end/SKILL.md`; `dev/rules/custom_session_routines.md`
2. **Blocking -- make accepted controls executable.** As the ordinary finding states, S2 requires failing mutations and S3 requires plan-level commands and input sets; Verification currently defers exact nodes. Supply these for the named boundaries using existing public-entry test homes, without a new framework or broad matrix. -- accepted proposal Security preflight; plan Verification

**Coverage / rule loss:** Inspected Gauge readers/schema/rendering, Audit producer/reducer cycle, both Meter publication paths, receipts, session lock and install mapping. C1–C3 retain limits, identity, strict parsing, matching, owned code loading, override refusal, disabled public rendering, consent and reflection privacy. No rule loss is authorized. The coordinator reports the existing wait-export work guard blocks publication: C2 cannot deliver a fresh report until its output-equivalent bounded repair. This is a prerequisite to the existing contract, not extra scope. No runtime checks, private inputs, Windows execution, parity measurement or cost evidence. The modest word-target overrun records this newly reported prerequisite.

## Focused plan review -- GPT-6.1 Terra (ordinary reviewer, Medium) -- 2026-11-17

Reviewed commit: 01d58bb95d6af1ce14511d873ac9b3ad6a12edc5

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: approximately 2 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes: the revision preserves the accepted fresh full report and replaces Cairn's stale aggregate route. -- C2–C3; `dev/rules/custom_session_routines.md`
2. **Best alternative.** The bounded sweep repairs the existing export without a new collector or changed ceiling; named public tests and a temporary oracle reuse existing homes. -- C2 and Focused public controls; `tools/meter.py` `_wait_artifact_map`
3. **What would show it wrong?** A mutation survives its named control, or the sweep disagrees with the pairwise overlap set or changes attribution. -- Focused public controls

The revision names S2 mutations, targeted test nodes and synthetic inputs, including failure after the budget limit. Its sorted maximum-end sweep marks overlapping closed intervals while preserving touching and empty interval behavior; the separately charged candidate loop remains. Existing named Meter regression nodes are present. Functional prose retains consent, no-commit and locked pre-prune duties.

**Coverage:** Focused reread of the revision, accepted S2–S3 and current Meter overlap and candidate loops, plus named existing test nodes. No test execution, Windows run, private data, performance measurement or independent Security Review. Implementation and new tests remain unverified.

## Plan review -- Sol High, focused pass 2 -- 2026-11-17

Reviewed commit: 01d58bb95d6af1ce14511d873ac9b3ad6a12edc5

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: the custom stale-report route is replaced and accepted controls now have commands, nodes and inputs. -- revised C3; Focused public controls
2. **Best alternative.** The sorted maximum-end sweep repairs existing export work while preserving output and the unchanged ceiling. -- C2; `tools/meter.py`, `_wait_artifact_map`
3. **What would show it wrong?** A sweep/oracle overlap mismatch, changed public attribution or a surviving boundary mutation would falsify preservation. -- Focused public controls

The sweep marks each positive-duration interval that overlaps a predecessor and its maximum-end witness; an otherwise unmarked witness is marked when its first successor overlaps. Strict comparison preserves touching boundaries; empty intervals remain excluded only from overlap detection. Owner collisions, open claims, inclusive containment and the separately guarded candidate loop remain unchanged. The 450-claim fixture implies 449 sweep plus 900 candidate comparisons and requires prior-export preservation on lowered-cap refusal. Temporary oracle evidence and public regressions remain required, not claimed results.

**Coverage / rule loss:** Focused diff and relevant overlap/candidate source only. C3 retains consent, no-commit, reflection privacy and locked pre-prune duties; no added authority or rule loss. No actual refresh, private inputs, tests, Windows execution or parity/cost measurement. Both earlier findings are closed; no new blocker found.

## Review disposition -- GPT-6.1 Terra (plan author, Medium) -- 2026-11-17

Both focused reviews accept revision `01d58bb9`. C3 reconciles the existing
custom goodnight route; Verification names the accepted mutations, public
controls and inputs. C2 specifies the bounded wait-overlap repair and its
regression without changing the ceiling. The checks remain due in execution;
no test result is claimed here.

**Disposition**: ready-to-implement. **Elapsed**: about 2 minutes. **Tokens**: unknown.

## Implementation record — C1

**Model / role**: GPT-6.1 Luna, Implementation Low.

Gauge's bounded pulse reader, schema, comparison, builder and renderer now live
in the shared standard-library module, along with Audit's pure artifact
validation and reduction. Gauge and Audit load the sibling module from their
own tool directory; Audit keeps its explicit-file producer. The standalone
`pulse` command is registered for installation.

**Checks** (Python 3.13.13):

- `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q bootstrap/tests/integration/test_gauge.py::test_full_pulse_public_parity bootstrap/tests/integration/test_gauge.py::test_explicit_artifact_snapshot_runs_producer_into_pulse bootstrap/tests/integration/test_gauge.py::test_explicit_project_meter_aggregate_joins_pulse_without_private_reads bootstrap/tests/integration/test_gauge.py::test_artifact_snapshot_mismatch_and_secret_fail_closed` — 4 passed, 0.69 s.
- `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q bootstrap/tests/integration/test_gauge.py::test_pulse_rejects_snapshot_and_target_root bootstrap/tests/integration/test_gauge.py::test_json_without_pulse_refuses_before_git bootstrap/tests/integration/test_gauge.py::test_pulse_never_executes_git_or_target_python bootstrap/tests/integration/test_gauge.py::test_non_pulse_mode_rejects_before_and_inventory_inputs` — 4 passed, 0.35 s.
- `cmp templates/skills/_lib/pulse.py tools/pulse.py` and focused `py_compile` passed.

No broader Gauge selection, installed-adopter run, Windows run or C4 joined
selection was run. **Elapsed**: unknown. **Tokens**: unknown.
