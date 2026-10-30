# Plan: Meter agent cost from tool logs

**Source proposal**: dev/proposals/archive/2026-10-30-claude-metered-cost.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Measure agent usage from opted-in local logs and stop unattended work between items when its spending reading is unsafe.

## Source proposal

The Maintainer accepted the revised heavy proposal at `2fc884de`: meter actual usage, report it, and apply a cooperative unattended spending stop. Retire self-reported Tokens once the meter passes its checks; retain Elapsed until metered time is shown equivalent. The proposal declares mutable logs and concurrent or in-flight overshoot residual risks.

## Scope

Implement the accepted meter and tool readers, private ledger and per-project aggregates, pulse, handoff refresh, drain admission, and documentation and template changes. Support Windows as well as other supported platforms. Keep the runtime standard-library-only. No per-artifact budgets or scores. The accepted proposal remains the detailed contract.

**Reuse.** `tools/session.py` supplies `_read_regular_bytes` and `encode_display`; `tools/_intent/identity.py` and `tools/_intent/record_io.py` supply claim identity and retention context. Search `tools/` for `gauge`, `session`, `intent`, and `drain` found the existing reporting and lifecycle entry points; extend those rather than duplicate them.

Proposed paths:
- tools/meter.py
- bootstrap/tests/test_meter.py

### Documentation / doctrine surface

Update `dev/measurement/README.md`, `doctrine/rationale.md`, the drain and shipped copy, and the proposal and plan templates and their shipped copies as applicable. Describe software behavior in its existing documentation; keep prescription in the governing layer. Preserve byte-identical session copies if touched.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Meter and local configuration, reporting and handoff | Reviewed plan | Ingestion, private ledger, project aggregates, pulse and refresh |
| C2 | Unattended admission and Q1 | C1 meter checks pass; reviewed plan | Freshness stop, template field retirement and documentation |

## Acceptance criteria

**C1.** Opt-in roots and projects only; private per-user cross-project ledger, project-only gitignored aggregates. Retain no message content; strip remote credentials, escape displayed names, and give content-free file/line errors. Bound regular-file reads and line size; reject links, invalid and non-finite or negative numbers; atomic writes refuse links. Deduplicate message IDs, distinguish four token kinds, fold subagents, use last running totals and establish cache accounting. Attribute reliably to items or else daily with ambiguity shown; retain claim mappings across pruning. Incremental rotation equals rebuild; missing logs are unknown. Report test wait and repeats, raw and weighted tokens and reported plan percentage; pulse shows weekly project/artifact figures, review passes, tier mix and always-loaded cost. Refresh on `session-end --handoff`.

**C2.** Before every unattended drain item, refresh and admit only a fresh finite reading below the configured limit, matching Maintainer-controlled source, account, unit and window. Missing, stale, invalid, mismatched and over-limit readings stop; attended work is unaffected. Declare overshoot and mutable-log limits. After meter checks pass retire Tokens in both templates, retaining Elapsed until equivalence is shown. Compare same-log counts with `ccusage` and one week's weighted trend with plan percentage; record results and any unavailable data without claiming success.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A maps changed behavior to the proposed meter test module (privacy, bounds, counting, rotation, attribution and admission), `bootstrap/tests/test_session_routines.py` and `bootstrap/tests/test_session_failsafe.py` (handoff and safe file behavior), `bootstrap/tests/test_session_start_drain_rules.py` (drain), `bootstrap/tests/test_skill_contract.py` and `bootstrap/tests/test_review_stance_in_shipped_files.py` (shipped instructions), and `bootstrap/tests/test_claim_check_module.py` (template claims). Search readers and byte pins for each changed file and add their owning checks to this map before implementation. Exercise actual public entry points and Windows-compatible paths. Run `python scripts/claim_check.py` on changed documents, `python scripts/check_cairn.py`, `python scripts/link_check.py`, `python scripts/sync_doc_snippets.py --check` if supported, and relevant neutrality gates; inspect triggers and use their documented invocation. Secret, malformed input and admission fixtures must fail under the corresponding broken behavior. The independent comparison and week-long smoke are acceptance checks, not a substitute for fixtures.

Boundary B: wide, because local ingestion and admission cross a trust boundary. On the final clean implementation commit under canonical Python 3.13.x, run the mapped owning families, affected public paths, standing gates and acceptance checks; record the full template fields, counts, clean pre/post state, elapsed time, omissions, and `Certified by: pending`. A missing comparison or other unmet check keeps work open. Boundary C: independent code review challenges the map and highest-risk claims with targeted falsification; it does not rerun Boundary B. Full-tree certification is separate and only at the authorized integration points.

## Plan review -- Codex gpt-6.1-terra -- 2026-10-30

**Reviewed commit**: ad7b9c3f
**Tier**: Internal
**Verdict**: REVISE

**Foundations**

1. **Delivery:** The criteria preserve the accepted meter and cooperative stop,
   but the shipped entry points cannot call a meter that is not installed --
   plan Scope; `bootstrap/_scaffold/config.py:912-915`.
2. **Alternative:** Reuse the existing shipped-tool mapping and handoff kernel
   rather than invent another delivery mechanism, while preserving all accepted
   outcomes -- `bootstrap/_scaffold/config.py:912-915`, `tools/session.py:2013`.
3. **Falsifier:** A fresh Windows or other supported-platform install cannot
   refresh its meter before drain or handoff, or its mapped checks cannot detect
   that failure -- plan Verification; `templates/skills/session-start/SKILL.md:82`.

**Finding -- blocking:** The plan names only `tools/meter.py` and its test as
proposed paths, while it changes the shipped drain and handoff. The installer
maps the shipped session kernel from `templates/skills/_lib/session.py`, and
there is no meter mapping in the committed installer. An adopter can therefore
receive instructions or a kernel that calls a missing tool. Specify how the
meter and its dependencies are delivered and upgraded, including any required
installer/manifest work, and map a fresh-install and upgrade public-entry test
on supported platforms. Preserve the accepted scope and its security obligations.

**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Coverage:** Read the committed plan, accepted proposal, plan template, drain,
handoff and installer mapping. Did not inspect private logs, run the meter or
exercise Windows; separate Security Review remains open.

## Plan review -- Codex gpt-6.1-sol (Security Review) -- 2026-10-30

**Reviewed commit**: ad7b9c3f
**Tier**: Internal Security Review
**Obligation**: local usage-log ingestion and unattended-run control
**Verdict**: APPROVE with advice; the ordinary review's delivery finding remains open.

**Foundations**

1. **Delivery:** C1 preserves scoped ingestion, private storage and safe reporting;
   C2 binds each admission to fresh Maintainer policy. These deliver the accepted
   cooperative boundary without claiming authenticated enforcement -- accepted
   proposal sections 1 and 3; plan C1/C2.
2. **Alternative:** Extend existing file-safety and drain paths, with focused
   fixtures, rather than add a separate authorization system --
   `tools/session.py:657-678`; `templates/skills/session-start/SKILL.md:139-147`.
3. **Falsifier:** A link escapes opted-in roots, secret metadata reaches output,
   or a refresh failure permits another unattended item -- C1/C2 and the plan's
   public-entry and broken-behavior verification requirements.

**Advice:** Make the existing C1 fixtures distinguish helper reuse from a complete
boundary. `_read_regular_bytes` checks the leaf and opened identity but ends in
unbounded `handle.read()`; it neither caps bytes nor checks ancestor links.
Implement bounded ingestion and exercise ancestor redirection, Windows junctions
and private ledger placement as well as leaf links. A pathname-only Windows case
is insufficient evidence for these properties. Close this advice with the mapped
input/write fixtures and an explicit platform-coverage record; no new subsystem
is needed.

For C2, include refresh exceptions and malformed/partial logs through the actual
admission entry point, confirming attended work remains available. Declared
mutable-log tampering and concurrent/in-flight overshoot remain accepted
residuals, not defects this plan promises to eliminate.

**Elapsed**: approximately 5 minutes. **Tokens**: unknown.

**Coverage:** Read committed proposal/plan, file-safety helpers and drain, plus
Terra's committed delivery finding. No implementation, private-log inspection,
Windows execution, suite or re-anchor; this clears only the named plan Security
Review obligation, not implementation security or the ordinary review finding.
