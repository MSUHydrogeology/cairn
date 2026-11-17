# Make Meter visible and report at goodnight

**Author**: GPT-6.1 Terra (Medium)
**Status**: revising
**Review**: usual + Security Review
**Proposed tier**: heavy — the existing automatic trigger applies to shipped templates and documentation; the accepted narrowing is not yet implemented
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-17
**In brief**: Offer Meter setup with consent and make its usage report available at every goodnight in adopter projects.

## Decision summary

Meter ships without an adopter-facing setup offer or a goodnight report. Add an offer through existing session guidance and deliver a refresh and pulse report at every goodnight when Meter is installed and enabled. The offer explains the private reads and asks before configuration. The report requires a renderer that adopters actually have; the existing Gauge is not in the install mapping. Delivery and recurring refreshes add work and storage; their costs are not yet measured.

## Context

The Maintainer requested both outcomes on 2026-11-16 in `dev/PLANNING.md` under “Make the usage meter work, offer it, and report at session end.” The original Meter Decision required refresh at full handoff; `tools/session.py` does that before pruning, but not at reflection-only goodnight. Cairn's `dev/rules/custom_session_routines.md` adds its own report, while `templates/skills/session-end/SKILL.md` does not. The accepted staged-modules plan offers rules-folder guidance only. `bootstrap/_scaffold/config.py` installs Meter but has no Gauge mapping; the installed `templates/core/dev/measurement/README.md` has no Meter instructions. The separate findability audit remains queued.

## Proposal

1. In shipped session guidance, offer help enabling Meter to a person using an installed project. Explain the named source roots and projects, local ledger and project aggregates, and recurring refresh cost. Show the exact proposed configuration and obtain the person's yes before writing it; a refusal or unattended run causes no configuration write or private collection. Avoid repeated unsolicited offers after a refusal using an existing appropriate consent or routine mechanism, without recording private paths in a committed file.
2. At every explicit goodnight, including reflection-only, when Meter is installed and enabled, refresh and render the existing pulse view for the current project's aggregate. Report partial, unavailable or failed refresh honestly; do not treat it as zero or render stale data as current. Keep the existing full-handoff safety behavior. Deliver the existing renderer and its needed dependencies to an adopter by an appropriate reviewed install route; do not assume Cairn's checkout is present. Do not invent a second reporting format.
3. Put setup, commands, storage and limitations in the installed measurement guide and point to it from the offer. No automatic consent, network access, or committed aggregate is authorized. Existing Meter privacy and access boundaries remain in force.

## Rationale

An offer addresses discovery; the routine makes the accepted report useful without requiring people to remember commands. The renderer's missing install route needs explicit design before implementation. Refresh cost depends on configured log growth and is unmeasured.

## Alternatives considered

Leave the local Cairn routine alone: adopters still lack the report and setup offer. Build a new collector or offer framework: unnecessary for these outcomes.

## Documentation / doctrine surface

Shipped session skills and installed measurement guidance carry the operative directions. The install mapping may need a change to deliver the existing renderer; its exact dependencies and route belong in the plan. No methodology change is proposed.

## Evidence / verification plan

### Tests required

Use the existing file-based selection and exercise a fresh adopter install and upgrade: the offer, refusal and explicit consent, disabled and enabled goodnights, partial and failed refresh, and a real renderer consuming the current aggregate. Use synthetic sources only. Verify the full-handoff safeguard and no private read or configuration write before consent. A missing renderer or a stale report falsifies delivery.

### Examples / smoke checks

Inspect installed guidance and run the routine with synthetic data, including reflection-only. Measure recurring refresh time and report the scope and limits.

### Independent scientific check

N/A: no scientific claim or numerical model is proposed.

## Signals the change is wrong

Offers recur after refusal, consent is ambiguous, reports misstate incomplete data, or the recurring cost outweighs the information.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance — installed execution guidance, private-source consent and the install route require careful boundary review.

**Elapsed:** unknown. **Tokens:** unknown.

## Review -- GPT-6.1 Terra (ordinary reviewer, Medium) -- 2026-11-17

```
Reviewed commit: 43f0d9e7beb894a4637cdebe310cdffbe2c05829
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: about 4 minutes
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** The offer and every-goodnight report are owed; the delivery choice and costs need a concrete comparison before Decision. -- `dev/PLANNING.md`, Meter row
2. **Best alternative.** Assess a small report using Meter's existing project aggregate and CLI against installing Gauge; changing the requested Gauge pulse needs the Maintainer's direction, since its wider pulse output would be lost. -- `tools/meter.py`, `tools/gauge.py`
3. **What would show it wrong?** A fresh adopter install or upgrade cannot offer once, then produce the requested current report after consent, including on reflection-only goodnight. -- `templates/skills/session-end/SKILL.md`, `bootstrap/_scaffold/config.py`

The proposal preserves the person's consent and names an actual gap: Meter ships, Gauge does not, and Cairn's report is local guidance.

1. **Blocking: report route and cost.** The proposal mandates the existing pulse but names no installable renderer or dependency set, useful report contents, or measured baseline; Gauge also reports broader test and artifact information, and Meter's CLI currently returns a receipt rather than usage. Compare the actual shipped dependencies and recurring work with a minimal report from the existing aggregate, identify what each delivers and loses, and recommend a concrete route for the Maintainer to decide. Specify how the reflection gets the report and avoid a redundant refresh on full handoff. -- `tools/gauge.py`, `tools/meter.py`, `tools/session.py`
2. **Blocking: offer trigger and refusal.** “Existing appropriate” mechanism does not establish when install, upgrade or a later session offers setup, or how refusal persists and a later requested re-offer works. Name the trigger and state home, without private paths in committed files, and the behavior for existing adopters and unattended sessions. -- `bootstrap/_scaffold/config.py`, proposal item 1
3. **Blocking: security preflight.** The current template requires five written answers for a security-touching change; the proposed consent and install route leaves that section absent. Answer them against the chosen route so the separate Security Review can assess its boundary. -- `dev/proposals/_template.md`, Security preflight

**Coverage:** Read the proposal, template, board direction, session routine, install mapping, Meter CLI and Gauge pulse route. No tests, cost measurement, private data or Security Review. Functional prose: no existing rule is proposed for removal; the shipped instructions still need a concrete home.

## Review -- GPT-6.1 Sol (Security Review, High) -- 2026-11-17

```
Reviewed commit: 60050f8f
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: source inspection approximately 8 minutes; recording/checks unknown.
**Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Consent-based setup and every-goodnight usage reporting close the adopter gap; delivery needs a smaller concrete route and explicit freshness protection. -- `bootstrap/_scaffold/config.py`, `templates/skills/session-end/SKILL.md`
2. **Best alternative.** Recommend Meter render this refresh's current approved project aggregate in memory, reusing Gauge's usage formatting and schema, without installing all Gauge. -- `tools/meter.py`, `_project_export`; `tools/gauge.py`, `_pulse`
3. **What would show it wrong?** Configure project A, leave an old aggregate in unconfigured B, and run goodnight in B: reporting B's old usage as current falsifies delivery. -- `tools/meter.py`, `_refresh_ledger`, `_closed_refresh_receipt`

The strongest outcome is useful local reporting with an informed person's consent and no new collector.

1. **Blocking: missing preflight.** Supply the template's S1–S5 against the chosen route. State that reflections receive only sanitized usage and closed statuses, never private source/configuration/ledger contents or raw child diagnostics. -- `dev/proposals/_template.md`, Security preflight
2. **Blocking: freshness.** A successful receipt covers configured projects, not necessarily this directory; an existing aggregate proves neither approval nor freshness. Bind rendering to the approved current project and this refresh. A combined refresh/report option could reuse the freshly built export; preserve default receipt behavior and fail honestly on partial/export failure. This is a recommendation, not an implemented guarantee. -- `tools/meter.py`, `_refresh_ledger`, `_posix_atomic_write_project_export`
3. **Non-blocking: least burden.** Use a non-private refusal line in existing custom-routine guidance, with the person's agreement; specify the attended offer trigger and requested re-offer. Keep the locked pre-prune refresh: an earlier reflection refresh cannot replace it. Measure and disclose the possible two refreshes at full handoff. -- `tools/session.py`, `_meter_refresh_before_prune`

**Coverage:** Source inspection only; no implementation, synthetic execution, private files, VM or cost measurement. No existing duty is waived. Heavy remains required under `dev/rules/protected-surfaces.md`; no tier exception is recommended.
