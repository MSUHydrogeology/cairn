# Plan: Offer Meter and deliver the full pulse

**Source proposal**: dev/proposals/archive/2026-11-17-terra-meter-adopter-rollout.md
**Author**: GPT-6.1 Terra (Medium)
**Status**: revising-plan
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

Proposed paths:
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
