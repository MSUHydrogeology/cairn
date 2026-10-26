<!-- cairn-internal-ref-allow: doctrine/roles.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
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
rubric, the per-role default mapping, and a mapping file
(`dev/.cairn/model-selection-mapping.yml`) they fill in with the
models they actually use.

## Template content

Merged into the adopter's role/configuration documentation:

> **Capability-tier labels (adopter-local).** Map your model
> lineup onto three tier labels. Use the *strongest* model your
> team has access to as `high-capability tier`; pick a middle
> tier with broadly-comparable reasoning capability but lower
> cost for routine work as `medium-capability tier`; pick a
> fast / inexpensive tier for trivial work as `low-capability
> tier`. Where multiple vendors are available, list at least
> one model per vendor at each tier you populate — that keeps a
> different model architecture available when the Maintainer
> assigns one or asks for more distance. Diversity within a tier
> (`doctrine/roles.md`) is useful distance on request, never a
> default an agent applies.
>
> **Default tier-by-role mapping:**
>
> | Role | Default floor | Notes |
> |------|---------------|-------|
> | Strategy / Research | high | Research, premise-checking, novel design. High-stakes by default; Maintainer Decision may lower. |
> | Proposal authoring | medium | A premise-check inside a proposal is its own task, spawned at high, its result handed to the medium draft. |
> | Proposal review | high | The premise is still movable, and a wrong one is cheapest to catch here. |
> | Security Review | high | Focused-mode pass on a high-risk surface; its floor does not follow the stage it attaches to. |
> | Maintainer scribing | high | Decision-of-record artifacts; capability floor matches Strategy. |
> | Implementation (non-trivial) | medium | The standard lane, and the deliberate lane's plan chunks. High permitted; not required. |
> | Plan review | medium | Same as Implementation. |
> | Code review | medium | Floor is "not the implementing agent"; tier is medium-or-higher. |
> | Implementation (trivial chunks) | low | The trivial lane: single commit, single area, no follow-ups. |
> | User Agent (routine workflow) | low | Concrete-mode workflow exercise, capture only. |
> | Non-substantive doc tweaks | low | Typo / wording / linkfix. |
> | Docstring and comment cleanup, and related edits | low | The writing step only; the paragraph below says what stays unchanged. |
>
> **Docstring and comment cleanup, and related edits, may be written at low.**
> This covers an edit that changes only docstrings, comments and other
> non-executable wording: no executable token, and no bytes that a test, manifest
> or attestation pins. It lowers the writing step only. The review keeps its
> stage's floor (medium for code review), and where the edit touches a surface
> this project's `AGENTS.md` names as high-risk it also owes the Security Review
> that surface already requires, at high. Nothing in this row lowers a review or
> removes a Security Review.
>
> **Override discipline.** Lowering a high-stakes floor for a
> specific session or sub-domain requires an explicit Maintainer
> Decision recorded on the artifact (proposal or plan); the
> Decision names the role, the lowered floor, the rationale, and
> the scope. Raising a low-stakes role's tier is unrestricted.

## Orchestrated work — tiering the fan-out (template content)

The role→tier table above governs the **human-role roster**. Orchestrated
sub-agents — the fan-out a single call can spawn — are tiered by **task type**,
not by inheriting the orchestrator's tier. This is where the largest
model-cost multiplier lives: one orchestration call can spawn many sub-agent
calls, and by most tooling defaults each silently inherits the orchestrator's
(frontier) tier.

> **Tier the fan-out by task type, not by inheritance.** A sub-agent gets its
> capability floor from *its own task* and does not silently inherit the
> orchestrator's tier. Bounded leaves default to **low or medium**; the
> **high** floor is reserved for where judgment concentrates — the
> orchestration/synthesis **root**, and verification of **high-stakes claims**.
>
> | Task type (fan-out leaf) | Default floor |
> |---|---|
> | Single search / retrieval | low |
> | Single-source extraction / parsing | low |
> | Mechanical transform / formatting / scribing | low |
> | Routine verification of a bounded claim | medium |
> | Generative authoring (non-trivial, reviewed) | medium |
> | Synthesis / orchestration root | high |
> | Verification of a bright-line / high-stakes claim | high |
> | Bright-line task (see below) | high — never downshift |
>
> **Verification tier follows claim-stakes, not "decisiveness."** Which
> verification vote turns out decisive is unknowable until after it runs, so
> tier by the **stakes of the claim being verified**: bright-line / high-stakes
> claims get all-high verification; bounded / low-stakes claims may be medium.
> Do not try to downshift only the "non-decisive" votes — you cannot identify
> them a priori, and you may downshift the one that would have caught the
> refutation.
>
> **Route bounded work into sub-agents so it can be tiered — with a
> minimum-usefulness gate.** Pushing bounded / parallel / mechanical work into
> sub-agents lets you tier it while keeping the frontier main loop for
> irreducible judgment. But prefer inline work unless the fan-out has clear task
> independence, a narrow context packet, and a merge/review path — otherwise the
> context-packaging cost exceeds the saving.
>
> **A stronger, independent check can lower the *generative* step's floor — under
> four conditions, all required.** A cheaper author is safe *only when*: (a) the
> model that checks the output is at a tier **strictly above** the downshifted
> author; a stronger model from the same maker counts, and a model at the same
> tier does not (same-model fresh-session independence is *time* independence,
> not capability headroom);
> (b) acceptance criteria are pre-declared; (c) the output is
> falsifiable without trusting the author (compact, fully inspectable, backed by
> a checkable artifact); (d) a failed review **escalates** the next attempt,
> never retries indefinitely at the cheap tier. This does **not** apply to
> scientific assumptions, security-sensitive changes, architecture decisions,
> irreversible migrations, or large / diffuse edits a reviewer would have to
> re-derive to check — those are bright-line.
>
> **The cost rule's check is not a review.** An orchestrator may run a
> sub-agent's generative step on a cheaper model only when the model that checks
> the output is at a tier strictly above it; a stronger model from the same
> maker counts, and a model at the same tier does not. The check is
> the orchestrator's. It is never filed as a proposal, plan or code review pass
> and never counts toward one, and no lifecycle review requires a different
> architecture. Sending the context packet to a second maker's model crosses the
> data-governance gate below, so that gate applies first.
>
> **Bright-line tasks never downshift — even as a fan-out leaf.** Security
> Review, the high-risk trust boundaries, premise-checking, and genuinely novel
> design stay at the high floor regardless of orchestration context. The one
> exception is the docstring-and-comment cleanup row above, and only for its
> writing step: it lowers no review and no Security Review. One missed subtle
> failure there dwarfs a session of token savings.
>
> **Data-governance / tool-parity is a hard gate.** Never downshift across a
> data-governance boundary: proprietary code, collaborator data, unpublished
> work, and the security-review surface are never routed to a cheaper or
> different model / vendor *because* it is cheaper. And no downshift unless the
> candidate model's data-retention policy, tool access, and execution
> environment are at least as acceptable as the original tier's for that
> specific repository and task. Capability and price are not the only axes —
> this is a trust boundary.
>
> **Measure accuracy-per-dollar before hard-coding a downshift.** A lowered
> floor on a non-bright-line task is justified by a cheap A/B on representative
> tasks, not by assumption; tiering by task *type* is preferred over dynamic
> cost cascades, whose escalation overhead can exceed the saving.

> **Mapping-record schema — bind to measured capability, dated.** Tier *labels*
> are only a capability proxy: product-line names (Pro / Flash / mini) track
> capability within a *co-released* lineup, not across release generations or
> vendors — a newer mid-line model routinely out-benchmarks an older flagship
> until that flagship's next release flips it back. So bind each tier to the
> *currently top-benchmarking* model per vendor by **measurement, not name**,
> and record it in the adopter-local mapping file, never in this
> doctrine. Each mapping row carries: `model`, `tier`, `date-verified`,
> `task-family`, `source/benchmark`, `accepted-quality-threshold`, `price-basis`,
> `re-verification-trigger`. Re-rank on a low-frequency housekeeping pass;
> the `date-verified` stamp lets a reader see staleness, and no routine reads it.

**Filling the mapping.** The adopter-local mapping is
`dev/.cairn/model-selection-mapping.yml`: one row per tier you populate (high, medium,
low), copying the shape of the seeded row. In `model`, name the model family, never a
version; the latest release of that family is meant, so a new release does not make a row
stale, and a release that changes which family fits a tier does. Say in `source` who made
the assignment. `python scripts/check_model_selection.py` exits 0 once no placeholder
remains and at least one row exists. It checks shape, not truth, and nothing reads
`date_verified`, so noticing a stale mapping is yours to do. The installing agent runs the
check at the acceptance step; after that a person does, because nothing runs it
automatically.

## Notes on the gating

This module is **conditionally installed**: the gate is the `Selected when:`
header above (moderate-or-complex on Complexity), mirroring `legacy-agent` (Age)
and `dual-language-tests` (Language). A project at low complexity does not
install it. A solo team still has tiers to choose between within one maker's
lineup, and the tier rule in `AGENTS.md` covers every profile, with or without
this module. The module is **doctrine-tracked**, not a config schema: the
adopter's tier-to-model assignment lives in its own mapping file.
