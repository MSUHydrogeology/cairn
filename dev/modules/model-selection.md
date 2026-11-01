<!-- cairn-internal-ref-allow: docs/methodology/roles.md reason=docs/methodology/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where docs/methodology/ references resolve") -->
# Module: model-selection

**Selected when:** the project sits at **moderate or complex** on
the Complexity axis (`dimensions/complexity.md`) — Review weight
and verification depth are non-trivial, capability-floor failures
have real cost. A greenfield experimental project at low
complexity does not install this module; if its complexity
placement moves up later the bootstrap re-evaluates.
**Adds to:** the role-and-capability discipline in
`docs/methodology/roles.md` (the "Capability floors" section), plus
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

> **Capability-tier labels (adopter-local).** Map the generic high,
> medium and low capability tiers to your own model lineup. The task
> sets the model floor; the lifecycle lane governs the process, not
> the tier. Where several families fill a tier, add a mapping row
> for each family using the existing schema. Diversity within a tier
> (`docs/methodology/roles.md`) is useful distance on request, never a
> default an agent applies.
>
> **Default tier-by-task mapping:**
>
> | Task | Default floor | Notes |
> |------|---------------|-------|
> | Strategy / Research | high | Includes premise-checking and genuinely novel design. |
> | Security judgment / Security Review | high | Includes judgment on security or trust boundaries, regardless of lane. |
> | Ordinary proposal authoring | medium | A premise-check is a separate high-tier task; its result is handed to the medium-tier author. |
> | Ordinary proposal review | medium | Raise to high when the review performs a premise-check, novel design or security judgment. |
> | Plan review | medium | Raise to high only for a high-tier judgment within its scope. |
> | Code review | medium | Fresh reviewer who did not implement the work; raise to high for a high-tier judgment within its scope. |
> | Accepted-plan execution | low | Includes non-trivial and high-risk chunks; review, security and Maintainer fences still apply. |
> | Trivial implementation | low | The process lane remains trivial; a task that makes a high-tier judgment keeps that floor. |
> | Authorized Decision scribing | low | Only when the Maintainer explicitly authorizes it; quote the authorization verbatim and keep the Decision commit exclusive. |
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
> **Override discipline.** The Maintainer may raise a task's floor.
> Lowering a task below its default floor requires an explicit
> Maintainer Decision recorded on the artifact (proposal or plan);
> it names the task, lowered floor, rationale and scope. A low-tier
> execution floor grants no authority to decide, review, waive a
> fence or make a security judgment.

## Orchestrated work — tiering the fan-out (template content)

The role→tier table above governs the **human-role roster**. Orchestrated
sub-agents — the fan-out a single call can spawn — use the same **task floors**,
not the orchestrator's tier or the lifecycle lane. A leaf's assignment does
not transfer the orchestrator's authority or its review obligations.

> **Tier the fan-out by task, not by inheritance.** A sub-agent gets its
> capability floor from *its own task* and does not silently inherit the
> orchestrator's tier. Executing an accepted, reviewed plan is low, including
> high-risk chunks; ordinary authoring and reviews are medium; strategy,
> premise-checking, novel design and security judgment or Security Review are
> high. A task may contain more than one kind of work: assign the floor for
> the judgment it performs.
>
> | Task type (fan-out leaf) | Default floor |
> |---|---|
> | Single search / retrieval | low |
> | Single-source extraction / parsing | low |
> | Mechanical transform / formatting | low |
> | Authorized Decision scribing | low |
> | Accepted, reviewed plan execution | low, including high-risk chunks |
> | Ordinary authoring or review | medium |
> | Strategy, premise-checking or novel design | high |
> | Security judgment or Security Review | high — never downshift |
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
> **High-judgment tasks never downshift — even as a fan-out leaf.** Security
> Review, security or trust-boundary judgment, premise-checking, and genuinely
> novel design stay at the high floor regardless of orchestration context. The one
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

> **Mapping-record schema — record dated Maintainer assignments.** The
> adopter's mapping names the model family assigned to each tier and the
> Maintainer who made that assignment. Each row uses the existing fields:
> `model`, `tier`, `date_verified`, `task_family` and `source`; optional
> fields such as `re_verification_trigger` may record when to revisit it.
> Add a row for each additional family assigned to a tier. The mapping is an
> assignment, not a benchmark claim, and no routine authenticates it.

**Filling the mapping.** The adopter-local mapping is
`dev/.cairn/model-selection-mapping.yml`: at least one row per tier you populate (high,
medium, low), copying the shape of the seeded row. In `model`, name the model family,
never a version; add another row for every additional family assigned to that tier. Put
the Maintainer assignment and date in `source` and `date_verified`. The assignment does
not claim benchmark evidence. `python scripts/check_model_selection.py` exits 0 once no
placeholder remains and at least one row exists. It checks shape, not truth or
authorization, and nothing reads `date_verified`; a person checks the assignment. The
installing agent runs the check at acceptance; after that a person runs it because
nothing does so automatically.

## Notes on the gating

This module is **conditionally installed**: the gate is the `Selected when:`
header above (moderate-or-complex on Complexity), mirroring `legacy-agent` (Age)
and `dual-language-tests` (Language). A project at low complexity does not
install it. A solo team still has tiers to choose between within one maker's
lineup, and the tier rule in `AGENTS.md` covers every profile, with or without
this module. The module is **doctrine-tracked**, not a config schema: the
adopter's tier-to-model assignment lives in its own mapping file.
