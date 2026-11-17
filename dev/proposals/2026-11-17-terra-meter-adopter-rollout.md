# Make Meter visible and report at goodnight

**Author**: GPT-6.1 Terra (Medium)
**Status**: awaiting-decision
**Review**: usual + Security Review
**Proposed tier**: heavy — the existing automatic trigger applies to shipped templates and documentation; the accepted narrowing is not yet implemented
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-17
**In brief**: Offer Meter setup with consent and report the current project’s usage at every goodnight.

## Decision summary

Offer Meter setup at attended session start and report usage at every goodnight after consent. Extend the installed Meter command to render this refresh's current-project usage in Gauge's existing usage format, reusing its formatter; do not install the full Gauge. A full handoff still performs its separate locked pre-prune refresh, so it runs two refreshes. The new recurring cost depends on log growth and is unmeasured.

## Context

The Maintainer requested both outcomes on 2026-11-16 in `dev/PLANNING.md` under “Make the usage meter work, offer it, and report at session end.” The original Meter Decision required refresh at full handoff; `tools/session.py` does that before pruning, but not at reflection-only goodnight. Cairn's `dev/rules/custom_session_routines.md` adds its own report, while `templates/skills/session-end/SKILL.md` does not. The accepted staged-modules plan offers rules-folder guidance only. `bootstrap/_scaffold/config.py` installs Meter but has no Gauge mapping; the installed `templates/core/dev/measurement/README.md` has no Meter instructions. The separate findability audit remains queued.

## Proposal

1. At an attended session start, if Meter is present and there is no existing consent or remembered refusal, offer setup. This reaches existing adopters at their next attended start as well as new ones. Show the actual proposed source roots and projects, private ledger, project aggregates and recurring cost; obtain the person's yes before writing configuration. A refusal can be remembered as a non-private instruction in the existing custom session routine file only with the person's yes. Reoffer only when the person asks. Unattended starts make no offer, private read or configuration write.
2. Add `refresh --report` to the existing Meter CLI. It renders only the approved current project's sanitized aggregate built in memory by that same refresh, using the existing Gauge usage formatter. The plan chooses the shared formatter's exact home. Default `refresh --json` stays unchanged. Do not add an arbitrary aggregate-file reader, freshness receipt, collector or schema. An unconfigured current project, failure or partial refresh yields an honest status, never stale counts. Reflection receives only sanitized current-project usage or closed status: no source keys, paths, raw child errors or other project's usage.
3. On every explicit goodnight, including reflection-only, the shipped session-end skill invokes that refresh and puts its result in the reflection when Meter is present and enabled. The full-handoff lock still runs its own separate refresh immediately before pruning; do not deduplicate it against the report. Absent or disabled Meter does not collect. Keep its existing fail-closed prune behavior.
4. Change both copies of the session-start and session-end skills, the installed measurement guide and Cairn's measurement guide; update the existing Meter CLI and reuse the Gauge formatter. The install mapping remains unchanged; the full Gauge stays Cairn-only. The installed guide explains consent, commands, storage and limits. No automatic consent, network access or committed aggregate is authorized.

## Rationale

The offer addresses discovery and the in-memory report ties output to this refresh and approved project. Plan C7 measured a synthetic 1 GiB refresh median of 8.9817 seconds; a real refresh was refused at the source budget in 3.07 seconds, so it did not establish report performance. The extra call's real recurring cost remains unmeasured and input-dependent.

## Alternatives considered

Installing all 1,296 lines of Gauge brings a larger Cairn-specific tool and its other pulse inputs to adopters; the proposed shared usage formatter gives the requested usage view without its broader test and artifact views. Doing nothing leaves both adopter outcomes undelivered.

## Documentation / doctrine surface

Shipped session-start and session-end skills and the installed measurement guide carry the instructions; Cairn's guide describes the same CLI. Meter and Gauge share the formatter. No methodology or install-mapping change is proposed.

## Evidence / verification plan

### Tests required

Using synthetic sources, exercise a fresh install and upgrade, attended offer and consent, refusal, unattended silence and no private read or write before consent. Through the real CLI, verify default receipt compatibility, current approved project and this-refresh binding, absent or disabled Meter, partial and failure statuses, and no stale counts when project B has an old aggregate but is not configured. Verify reflection output excludes paths, source keys, child errors and other-project usage; test both goodnight modes and the separate locked pre-prune refresh. Select checks by changed file.

### Examples / smoke checks

Inspect installed guidance and exercise a synthetic reflection-only goodnight and full handoff. Measure both refresh calls and state inputs and limitations.

#### Security preflight — five questions

- **S1:** The person supplies consent and named roots/projects through configuration; Meter receives local source records and project identity from those configured locations. Those sources can supply data about themselves, not consent or policy.
- **S2:** The plan must demonstrate failing mutations: an unconfigured project with an old aggregate, partial or failed refresh, and a refused or unattended setup. These negative controls are not yet run; existing Meter checks remain required.
- **S3:** `python tools/meter.py refresh --report` selects the approved current project and this refresh's configured sources; the plan must name the exact test commands and input sets. Adopter-facing promise: “Report only this refresh's approved current project; report incomplete or unavailable status honestly.” Tests must exercise that sentence.
- **S4:** Missing, disabled, invalid or unapproved configuration, parsing and refresh errors fail to no collection or no current report as applicable; partial results do not become complete. These defaults grant less authority, never fallback to an old aggregate.
- **S5:** A local actor able to change approved source logs can forge usage within that approval; sanitization and consent do not establish billing accuracy. Existing private-file protections and access boundaries remain in force.

### Independent scientific check

N/A: no scientific claim or numerical model is proposed.

## Signals the change is wrong

Offers recur after refusal, consent is ambiguous, reports misstate incomplete data, or the recurring cost outweighs the information.

## Scope delta

**Scope delta**: degraded. The original full Gauge pulse included test and artifact views; this route supplies its usage view only. **Disposition**: awaiting Maintainer decision.

## Assurance path

**Assurance path**: high-assurance — installed execution guidance and private-source consent require boundary review.

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

## Response -- GPT-6.1 Terra (author, Medium) -- 2026-11-17

- Ordinary 1 and Security 2: specify the in-memory current-project report, formatter reuse, default compatibility, failure behavior, costs and alternatives. The full-handoff refresh stays separate because the Security Review identifies its locked pre-prune safety role; two calls are explicit.
- Ordinary 2 and Security 3: specify attended start, consent, optional non-private refusal instruction and reoffer only on request.
- Ordinary 3 and Security 1: add S1–S5 and reflection privacy limits. Negative controls and exact test commands remain plan and implementation work, not claimed results.

**Scope delta**: degraded as recorded above; the Maintainer decides the proposed route. **Elapsed:** unknown. **Tokens:** unknown.
