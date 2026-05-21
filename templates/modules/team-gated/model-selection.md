# Module: model-selection

**Selected when:** the project sits at **moderate or complex** on
the Complexity axis (`dimensions/complexity.md`) — Review weight
and verification depth are non-trivial, capability-floor failures
have real cost. A greenfield experimental project at low
complexity does not install this module; if its complexity
placement moves up later the bootstrap re-evaluates.
**Adds to:** the role-and-capability discipline in
`doctrine/roles.md` (the "Capability floors" section), plus
adopter-local configuration mapping the tier labels to specific
models.

(The module's file lives under `team-gated/` per Cairn's catch-all
convention for conditional modules; the actual gating axis —
Complexity — is named in the Selected-when header above. Other
modules follow the same pattern: `legacy-agent` gates on Age;
`dual-language-tests` gates on Language.)

A project at moderate or complex on the Complexity axis cannot
afford to leave the capability-floor question implicit. The
doctrine names the floor as adopter-local tier labels (high /
medium / low capability); this module gives the adopter the
rubric, the per-role default mapping, and a worked-example
shape they fill in with the models they actually use.

## Template content

Merged into the adopter's role/configuration documentation:

> **Capability-tier labels (adopter-local).** Map your model
> lineup onto three tier labels. Use the *strongest* model your
> team has access to as `high-capability tier`; pick a middle
> tier with broadly-comparable reasoning capability but lower
> cost for routine work as `medium-capability tier`; pick a
> fast / inexpensive tier for trivial work as `low-capability
> tier`. Where multiple vendors are available, list at least
> one model per vendor at each tier you populate — this is what
> lets the *diversity within tier* rule (`doctrine/roles.md`)
> apply.
>
> **Default tier-by-role mapping:**
>
> | Role | Default floor | Notes |
> |------|---------------|-------|
> | Strategy / Research | high | High-stakes by default; Maintainer Decision may lower. |
> | External Review | high | Different model architecture from author preferred (diversity within tier). |
> | Security Review | high | Same as External Review; focused-mode pass. |
> | Maintainer scribing | high | Decision-of-record artifacts; capability floor matches Strategy. |
> | Implementation (non-trivial) | medium | High permitted; not required. |
> | Internal Review | medium | Same as Implementation. |
> | Code Review | medium | Floor is "not the implementing agent"; tier is medium-or-higher. |
> | Implementation (trivial chunks) | low | Single commit, single area, no follow-ups. |
> | User Agent (routine workflow) | low | Concrete-mode workflow exercise, capture only. |
> | Non-substantive doc tweaks | low | Typo / wording / linkfix. |
>
> **Override discipline.** Lowering a high-stakes floor for a
> specific session or sub-domain requires an explicit Maintainer
> Decision recorded on the artifact (proposal or plan); the
> Decision names the role, the lowered floor, the rationale, and
> the scope. Raising a low-stakes role's tier is unrestricted.
>
> **Worked example.** Adopters publish their tier-to-model
> mapping in their `case-studies/<adopter>.md` write-up — e.g.
> "high-capability tier = vendor-A's flagship model + vendor-B's
> flagship model; medium = vendor-A's mid model + vendor-B's
> mid model; low = vendor-A's fast model." Mappings get updated
> as models evolve; the case study is the natural home because
> model names are vendor-specific and change cadence is
> independent of Cairn doctrine.

## Notes on the gating

This module is **conditionally installed** based on the
Complexity axis, but lives under `templates/modules/team-gated/`
per Cairn's catch-all convention for any non-default-on module.
The actual gate is the `Selected when:` header above
(moderate-or-complex on Complexity), mirroring the pattern of
`legacy-agent` (gates on Age) and `dual-language-tests` (gates on
Language).

A multi-agent team at low complexity does not install this
module; their capability-floor questions do not bite at that
stakes level. A solo single-agent team at any complexity also
does not install it: one model fills every role, and the
capability question is settled trivially by the model that is
available. The module earns its keep only when (a) stakes are
non-trivial and (b) more than one model is available to choose
between.

The module is **doctrine-tracked**, not a config schema. The
adopter's actual tier-to-model assignment lives in adopter-
local configuration; this module gives the rubric and the
defaults the adopter customizes.
