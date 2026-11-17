# Make Meter visible and report at goodnight

**Author**: GPT-6.1 Terra (Medium)
**Status**: awaiting-review
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
