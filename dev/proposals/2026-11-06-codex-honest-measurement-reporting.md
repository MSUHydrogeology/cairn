# Honest on-demand measurement reporting

**Author**: Codex GPT-6.1 Terra (Medium)
**Status**: accepted
**Review**: usual
**Proposed tier**: light
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-11-06
**In brief**: Correct Cairn's product classification and make historical audit reports account honestly for separate review records.

## Decision summary

Cairn's on-demand reports can misrepresent shipped product work and miss or misattribute historical reviews. Correct the classifier and make the advisory audit report recognize separate review records using the existing reporting owner. This costs a small amount of parser and test maintenance; ambiguous historical attribution must remain visible rather than guessed.

## Context

`tools/gauge.py` classifies the entire `bootstrap/` tree as machinery, including the shipped scaffold, and leaves `.zenodo.json` unmatched. `tools/audit_report.py` scans each archived plan Markdown file as a plan and counts review headings, although its comment claims an independent author check that the code does not perform. The historical strategy `dev/strategy/2026-10-27-antigravity-lightweight-team-measurement.md` identifies standalone review files; its counts and proposed thresholds are historical, not current measurements. The accepted Meter plan `dev/plans/2026-11-04-metered-cost.md` excludes these corrections and owns pulse, artifact-size, review/model reporting and sidefile counting in Gauge.

## Proposal

For Cairn's own on-demand `tools/gauge.py` classification, classify `bootstrap/_scaffold/`, `bootstrap/scaffold.py`, and `.zenodo.json` as product while preserving the other buckets, unmatched-path reporting, and non-pulse command behavior. Do not change the accepted Meter pulse scope.

Make `tools/audit_report.py` distinguish historical standalone review records from parent plans, attribute them to a parent only where existing evidence supports it, and report unresolved or ambiguous records and coverage honestly. Reuse the Meter C3 reporting parser or interface where its delivered interface supports this; otherwise use a narrow compatible adapter without transferring C3 scope. Do not count an unsigned or same-author heading as proven independent; a named heading alone does not establish a distinct identity. Retain the report's advisory, read-only behavior and deterministic sampling of parent plans; do not infer model labels that are absent. No new collector, store, or automatic violation gate is authorized. In particular, a total over two reviews across distinct stages or scopes is not itself a violation. This outcome is intended for v0.7; any reuse depends on the delivered C3 interface, but this work must finish independently if that interface is unavailable.

## Rationale

The scaffold is delivered software, so its current bucket hides product work. Attributing sidefiles and exposing uncertainty makes the audit useful without turning incomplete historical conventions into enforcement.

## Alternatives considered

Do nothing adds no maintenance but keeps the misclassification and misleading audit coverage. A separate measurement service adds storage and operation costs without improving the source records. A numeric review-count alarm is simple but mistakes legitimate reviews of distinct stages or changed scope for violations.

## Documentation / doctrine surface

Update descriptions of these tools only where their behavior changes, in their existing software documentation or help. No governing doctrine change is proposed; deliberation stays here in `dev/`.

## Evidence / verification plan

A product path still classified as machinery, an unrelated path changing bucket, a sidefile counted as a separate plan, or an ambiguous attribution presented as certain falsifies the outcome.

### Tests required

Map affected callers and tests for `tools/gauge.py` and `tools/audit_report.py`; extend `bootstrap/tests/integration/test_gauge.py`, and `bootstrap/tests/test_replacement_tools.py` as their existing ownership warrants. Exercise the real command entry points with synthetic parent, independent and same-author reviews, missing and ambiguous links, standalone naming forms, and deterministic samples. Cover missing model labels as unspecified and unchanged non-pulse output behavior apart from the named classifications. Verify existing Meter reporting integration without duplicating its accepted tests or scope.

### Examples / smoke checks

Run the mapped affected tests, applicable prose gates, and final Boundary B on the committed result; no full-tree certification is implied.

#### Security preflight — five questions, answered in writing

N/A: no trust boundary added or widened; retain existing local input and read-only report boundaries.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Assurance path

**Assurance path**: standard

**Elapsed**: unknown. **Tokens**: unknown.

## Proposal review -- Codex GPT-6.1 Terra (Medium) -- 2026-11-06

**Reviewed commit**: `79cab916`. **Verdict**: PROCEED; no blocking findings. **Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**:

1. **Should it happen as framed?** Yes. Gauge's first-match `bootstrap/` rule places the shipped scaffold in machinery, while `audit_report.py` counts matching headings and scans every archived Markdown file without checking independence or parentage; these are distinct from Meter C3's pulse reporting.
2. **Best alternative.** Correct the existing advisory tools, reusing C3 only when its interface fits. Doing nothing keeps misleading results; a new service adds a store and maintenance without improving source evidence. The narrow adapter costs a parser but allows independent completion.
3. **What would show it wrong?** A real command that attributes an ambiguous sidefile as independent, changes an unrelated classification, or calls reviews across separate stages a violation would falsify the proposal; its synthetic entry-point cases name those checks.

**Advice**: When implementing, make identity uncertainty explicit even for signed headings: a name alone need not establish a distinct author. The proposal already requires evidence-supported attribution.

**Coverage**: Read the committed proposal, classifier and audit paths, Meter C3 and review guidance. Did not inspect every historical naming form or execute tests; the author's prose gates used noncanonical Python, so they are not Python 3.13 evidence.

## Author response -- Codex GPT-6.1 Terra (Medium) -- 2026-11-06

**Advice accepted:** A name alone does not establish a distinct identity; the proposal now says so. No authentication machinery or change to Meter C3 is added.

The opening claim, link, snippet and neutrality checks passed on a separate committed copy under Python 3.12.9; no proposal readers were selected by `tools/test_tiers.py for`. Final committed-copy prose checks under Python 3.13 remain due. **Elapsed:** unknown. **Tokens:** unknown.

## Decision -- Human Maintainer (via Codex GPT-6.1 Luna Low) -- 2026-11-06

**Elapsed**: unknown. **Tokens**: unknown.

**Tier**: light

**ACCEPTED.** The Maintainer's authorization, quoted verbatim:

> I accept all four of those proposals. Please scribe my acceptance and commence.

The accepted scope and assurance path are retained as proposed. No material
new recurring addition is introduced beyond the proposal's stated parser and
test maintenance.
