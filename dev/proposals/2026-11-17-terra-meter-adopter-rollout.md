# Make Meter visible and report at goodnight

**Author**: GPT-6.1 Terra (Medium)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy — the existing automatic trigger applies to shipped templates and documentation; the accepted narrowing is not yet implemented
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-17
**In brief**: Offer Meter setup with consent and deliver the complete pulse at every goodnight.

## Decision summary

Offer Meter setup at attended session start and deliver the entire existing pulse at goodnight. Share the pulse code with adopters rather than install Cairn's whole Gauge. It retains all views, text and `cairn-pulse/1` JSON; usage comes only from the current approved project's fresh Meter result. Full handoff keeps its separate locked refresh, so it can run two. Recurring cost depends on inputs and is unmeasured.

## Context

The Maintainer requested both outcomes on 2026-11-16 in `dev/PLANNING.md` under “Make the usage meter work, offer it, and report at session end.” The original Meter Decision required refresh at full handoff; `tools/session.py` does that before pruning, but not at reflection-only goodnight. Cairn's `dev/rules/custom_session_routines.md` adds its own report, while `templates/skills/session-end/SKILL.md` does not. The accepted staged-modules plan offers rules-folder guidance only. `bootstrap/_scaffold/config.py` installs Meter but has no Gauge mapping; the installed `templates/core/dev/measurement/README.md` has no Meter instructions. The separate findability audit remains queued.

## Proposal

Proposed paths:
- `tools/pulse.py`
- `templates/skills/_lib/pulse.py`

1. At attended session start, if Meter is present and there is no existing consent or remembered refusal, offer setup. Show actual proposed sources and projects, private ledger, project aggregates and recurring cost; get the person's yes before writing configuration. Remember refusal only with their yes, as a non-private instruction in the existing custom session routine; reoffer only on request. Unattended starts make no offer, private read or configuration write.
2. Add one shared shipped pulse module: byte-identical `tools/pulse.py` and `templates/skills/_lib/pulse.py`, with one install mapping. Move Gauge's entire pulse block and the pure artifact validation and reduction helpers from `tools/audit_report.py` into it (about 1,300 lines moved). Gauge delegates pulse and keeps its Cairn-only non-pulse Git classifier; Audit delegates the pure helpers, removing their dynamic cycle. The module has no sibling runtime or third-party dependencies.
3. Shared `read_inputs(options, meter_aggregate_bytes=None)` retains the bounded JUnit, baseline, tier, artifact, aggregate and label readers and rejects both aggregate path and bytes together. `build_pulse` retains every field of `cairn-pulse/1`; `render_text` retains every existing line. Shared argument registration serves the standalone pulse CLI, Gauge `--pulse` and Meter `refresh --report`. JSON returns the same full record. The future v0.9 website can consume this record API or JSON; building that website is outside this proposal.
4. Meter `refresh --report` supplies only this refresh's in-memory sanitized aggregate after current-project approval, export and revalidation. Preserve default `refresh --json`. Partial, failed or unconfigured results must not use stale counts. Reflections contain no source keys, paths, raw child errors or other-project usage. When Meter is disabled, pulse can still render explicitly supplied public inputs with unknown usage and no source collection.
5. At every explicit goodnight, including reflection-only, run the report; retain the full-handoff lock's separate pre-prune refresh and its fail-closed behavior. Change both copies of session-start and session-end skills, the installed and Cairn measurement guides, existing Meter, Gauge and Audit, and the install mapping. Explain consent, storage and limits. No automatic consent, network access, new collector, freshness receipt or committed aggregate is authorized.

## Rationale

The Maintainer wants the complete pulse retained until experience can show its usefulness and expects the v0.9 monitoring website may use it. Sharing the pulse preserves those views without shipping Gauge's unrelated classifier. Plan C7 measured a synthetic 1 GiB refresh median of 8.9817 seconds; a real refresh was refused at the source budget in 3.07 seconds, so it did not establish report performance. The extra call's real recurring cost is unmeasured and input-dependent.

## Alternatives considered

A usage-only formatter loses the other pulse views before they have been tried. Shipping all Gauge also carries Cairn-specific non-pulse code. Doing nothing leaves both adopter outcomes undelivered.

## Documentation / doctrine surface

Shipped session skills and the installed measurement guide carry instructions; Cairn's guide describes the same CLI. The shared pulse module changes the install mapping. No methodology change is proposed.

## Evidence / verification plan

### Tests required

Use synthetic sources and a fresh install and upgrade. Compare Gauge and shared pulse text and JSON for all existing views and bounded inputs; check path-plus-bytes rejection, standalone and Meter entries, mapping and byte identity. Verify consent, refusal, unattended silence and no private read or write before consent; default receipt compatibility; fresh current-project binding; partial, failed, disabled and unconfigured states; and no stale counts when an unconfigured project has an old aggregate. Check reflection privacy and the separate locked pre-prune refresh. Disabled Meter still renders explicit public inputs with unknown usage. Select checks by changed file.

### Examples / smoke checks

Exercise synthetic reflection-only and full-handoff reports; measure both refresh calls and state inputs and limits. Compare the full record and text with existing Gauge output.

#### Security preflight — five questions

- **S1:** The person supplies consent and named roots/projects through configuration; local logs supply usage, and explicit public files supply the other pulse inputs. Sources can supply data about themselves, not consent or policy.
- **S2:** The plan must demonstrate failing mutations for an unconfigured project with an old aggregate, partial or failed refresh, refused or unattended setup, and simultaneous aggregate path and bytes. These controls are not yet run; existing bounded-reader checks remain required.
- **S3:** `python tools/meter.py refresh --report` selects this refresh's approved current project; standalone pulse and Gauge select explicitly named public inputs. The plan must name exact test commands and input sets. Adopter-facing promise: “The pulse uses only this refresh's approved current-project usage and explicitly supplied public inputs; incomplete usage is reported honestly.” Tests must exercise it.
- **S4:** Missing, disabled, invalid or unapproved configuration and parse or refresh errors grant no collection or current usage as applicable; partial results never become complete and no old aggregate is a fallback. Disabled Meter leaves public pulse inputs available with unknown usage.
- **S5:** An actor able to alter approved logs can forge usage; one able to alter explicit public reports can forge those observations. Consent, bounds and sanitization do not establish billing accuracy or authenticate input truth.

### Independent scientific check

N/A: no scientific claim or numerical model is proposed.

## Signals the change is wrong

Offers recur after refusal, consent is ambiguous, reports misstate incomplete data, or the recurring cost outweighs the information.

## Scope delta

**Scope delta**: preserved. The complete pulse is restored.

## Assurance path

**Assurance path**: high-assurance — the install mapping, installed execution and private-source consent require boundary review.

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

## Maintainer scope direction and author response -- 2026-11-17

The Maintainer rejected the usage-only reduction in chat:

> For now, let's keep the pulse intact. We have never had it working so have no way of knowing if it's useful

> It would presumably get used by our status monitoring website in v0.9 too

The operative proposal restores all pulse views, text and schema through a shared shipped module. The earlier usage-only scope delta is withdrawn. This direction selects the broader alternative for review; it is not acceptance of the revised proposal. The changed module and input boundary return for review. **Elapsed:** unknown. **Tokens:** unknown.

## Review -- GPT-6.1 Terra (ordinary reviewer, Medium) -- 2026-11-17

```
Reviewed commit: 18e7707db8ebb493962cf530d46a4497897a103a
```

**Tier**: usual
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: about 3 minutes
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: the shared module delivers the full pulse the Maintainer chose, including its text and JSON, to adopters. -- Proposal items 2–3; Maintainer scope direction
2. **Best alternative.** Shipping all Gauge retains the pulse but also installs its Cairn-specific classifier; extraction reuses the pulse while avoiding that extra surface. -- `tools/gauge.py`; Proposal item 2
3. **What would show it wrong?** A fresh install or upgrade loses a pulse field, uses an old or other-project aggregate, or fails to report at reflection-only goodnight. -- Evidence / verification plan

The proposal now names the module, mapping, approximate moved code and unmeasured recurring cost; it keeps the locked handoff refresh and states that two may run. The offer requires consent, records refusal only with permission and permits a requested re-offer. The shared record is available to the future website without authorizing website work. The plan must make the stated parity and freshness checks executable; no results are claimed here.

**Coverage:** Read the revised proposal and its prior reviews against the existing Meter, Gauge, install mapping and session guidance examined in the first pass. No tests, VM, private inputs, performance measurement or Security Review. No existing duty is proposed for removal.

## Review -- GPT-6.1 Sol (Security Review, High), pass 2 -- 2026-11-17

```
Reviewed commit: 18e7707db8ebb493962cf530d46a4497897a103a
```

**Tier**: Security Review
**Findings**: none blocking
**Verdict**: ACCEPT
**Elapsed**: source inspection approximately 5 minutes; recording/checks unknown.
**Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes: preserve the complete pulse the Maintainer selected while separating public-report parsing from consented private collection. The revised preflight, fresh current-project binding and locked handoff refresh close the first pass's proposal blockers. -- Proposal items 2–5, S1–S5; `tools/meter.py`, `_project_export`
2. **Best alternative.** The single dependency-free pulse module is the least-burden credible full-scope route: moving the pure artifact reducer removes the Gauge/Audit dynamic cycle without shipping their unrelated scanners. -- `tools/gauge.py`, `_parse_artifact_snapshot`; `tools/audit_report.py`, `_pulse_artifact_metrics`, `_load_fixed_gauge_reader`
3. **What would show it wrong?** Synthetic installed-entry tests expose any lost pulse field, path override after refresh failure, bypassed byte limit, stale/other-project usage or private diagnostics in reflections. -- Evidence / verification plan; `tools/gauge.py`, `_pulse`, `_read_pulse_report`

The proposal retains every existing view and both output forms for actual use before judging usefulness.

**Plan closure notes, non-blocking.** Preserve the existing no-link/reparse, regular-file, identity, byte-budget, XML entity and strict-JSON protections during extraction. Apply aggregate and cumulative limits and schema validation to in-memory bytes too. Meter's fresh-report entry must reject an aggregate-path override even when failed collection supplies no bytes; standalone explicit-public rendering stays independent of private configuration. Load shared code only from the owned tooling location, never a public input or supplied target root. Retain artifact/project matching. These specify existing boundary promises, not a new guard framework. -- `tools/gauge.py`, `_read_pulse_report`, `_parse_pulse_report`, `_pulse`

**Coverage:** Committed-source inspection only: proposal, Gauge readers/rendering, Audit pure helpers and loader cycle, Meter export flow and install mapping. No implementation, tests, VM, private inputs or performance measurement. No existing duty is removed; heavy and plan Security Review remain. This is the second proposal Security Review pass; no further pass is requested.
