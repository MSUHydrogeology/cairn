# Plan: Meter agent cost from tool logs

**Source proposal**: dev/proposals/archive/2026-10-30-claude-metered-cost.md
**Status**: ready-to-implement
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Measure agent usage from opted-in local logs and stop unattended work between items when its spending reading is unsafe.

## Source proposal

The Maintainer accepted the revised heavy proposal at `2fc884de`: meter actual usage, report it, and apply a cooperative unattended spending stop. Retire self-reported Tokens once the meter passes its checks; retain Elapsed until metered time is shown equivalent. The proposal declares mutable logs and concurrent or in-flight overshoot residual risks.

## Scope

Implement the accepted meter and tool readers, private ledger and per-project aggregates, pulse, handoff refresh, drain admission, and documentation and template changes. Support Windows as well as other supported platforms. Keep the runtime standard-library-only. No per-artifact budgets or scores. The accepted proposal remains the detailed contract.

**Reuse.** `tools/session.py` supplies `_read_regular_bytes` and `encode_display`; `tools/_intent/identity.py` and `tools/_intent/record_io.py` supply claim identity and retention context. Search `tools/` for `gauge`, `session`, `intent`, and `drain` found the existing reporting and lifecycle entry points; extend those rather than duplicate them.

Proposed paths:
- `tools/meter.py`
- `templates/skills/_lib/meter.py`
- `bootstrap/tests/test_meter.py`

### Documentation / doctrine surface

Update `dev/measurement/README.md`, `doctrine/rationale.md`, the drain and shipped copy, and the proposal and plan templates and their shipped copies as applicable. Describe software behavior in its existing documentation; keep prescription in the governing layer. Preserve byte-identical session copies if touched. Deliver the meter and any runtime dependencies through the existing unconditional, verbatim skills mapping in `bootstrap/_scaffold/config.py`, with `templates/skills/_lib/meter.py` as shipped source and a matching self-hosted copy; update installer, upgrade and required manifest surfaces as needed.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Meter and local configuration, reporting and handoff | Reviewed plan | Ingestion, private ledger, project aggregates, pulse and refresh |
| C2 | Unattended admission and Q1 | C1 meter checks pass; reviewed plan | Freshness stop, template field retirement and documentation |

## Acceptance criteria

**C1.** Opt-in roots and projects only; private per-user cross-project ledger, project-only gitignored aggregates. Retain no message content; strip remote credentials, escape displayed names, and give content-free file/line errors. Bound regular-file reads and line size; reject links, invalid and non-finite or negative numbers; atomic writes refuse links. Check ancestor redirection and Windows junctions as well as leaf links, and verify private ledger placement; the existing helper alone does not provide bounded reads or ancestor checks. Deduplicate message IDs, distinguish four token kinds, fold subagents, use last running totals and establish cache accounting. Attribute reliably to items or else daily with ambiguity shown; retain claim mappings across pruning. Incremental rotation equals rebuild; missing logs are unknown. Report test wait and repeats, raw and weighted tokens and reported plan percentage; pulse shows weekly project/artifact figures, review passes, tier mix and always-loaded cost. Refresh on `session-end --handoff`. Fresh installations and upgrades deliver the meter and its dependencies so the installed handoff and drain entry points can use it, including on Windows.

**C2.** Before every unattended drain item, refresh and admit only a fresh finite reading below the configured limit, matching Maintainer-controlled source, account, unit and window. Missing, stale, invalid, mismatched and over-limit readings stop; attended work is unaffected, including refresh exceptions and malformed or partial logs through the actual admission entry point. Declare overshoot and mutable-log limits. After meter checks pass retire Tokens in both templates, retaining Elapsed until equivalence is shown. Compare same-log counts with `ccusage` and one week's weighted trend with plan percentage; record results and any unavailable data without claiming success.

## Scope delta

**Scope delta**: preserved.

## Verification

This plan switches to the verification contract in the Maintainer's 2026-10-30 AGENTS instructions: iteration runs tests naming changed files and prose gates; the final integration selection follows code review. Use `python tools/test_tiers.py for <paths>` to select tests, including integration/workflow tests naming the reviewed range. For governing text exceeding the runner limit, use passage-pinning tests and record omissions. Record platform coverage, including whether Windows junction behavior was actually exercised.

`bootstrap/tests/test_meter.py` covers privacy, input and write boundaries, counts, rotation, attribution and admission. Extend `bootstrap/tests/test_skills_install.py` and `bootstrap/tests/test_skills_upgrade.py` with fresh-install and upgrade public-entry checks that exercise installed handoff and drain with the meter and dependencies present; include supported-platform behavior. Exercise refresh exceptions and malformed or partial logs at the real admission entry. Run applicable claim, link, snippet and neutrality gates, following their actual triggers. Compare with `ccusage` and the week's plan percentage as accepted; unavailable data is an unmet check, not a pass.

Boundary B is wide for the trust boundary: after code review, run the integration selection on the clean final commit under canonical Python 3.13.x and record the template fields, counts, omissions, platform coverage and `Certified by: pending`. Boundary C is independent targeted falsification during code review, without rerunning a suite. Tree certification remains separate and only at authorized integration points.

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

## Response to plan review -- Codex gpt-6.1-terra -- 2026-10-30

- Delivery finding: accepted; Scope, C1 and Verification use the existing verbatim installer/upgrade path and map installed public-entry checks.
- Security advice: accepted; C1, C2 and Verification specify ancestor and junction coverage, private placement, bounded reads, refresh failures and platform evidence.
- Forward references: corrected the proposed-path declarations without changing the appended review.

**Elapsed**: unknown. **Tokens**: unknown.
