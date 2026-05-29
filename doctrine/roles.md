# Roles

Cairn's work is organized by **roles**, not by people. A role is a
*frame* — a stance, a set of responsibilities, a kind of output.
One contributor (a human, or an AI agent) fills different roles at
different times; what matters is that the role is *named* before
substantive work, because different roles produce different
artifacts and a silently-wrong role wastes a turn.

## Roles as cognitive adapters

Naming the role is not bookkeeping — it is a **cognitive adapter**.
An AI agent reasons differently depending on the stance it holds:
a constructive Internal-review stance and an adversarial
External-review stance produce genuinely different readings of the
same change. Stating the role explicitly *anchors* the agent in
one definite stance for the turn; leaving it implicit lets the
reasoning drift between stances mid-task, blurring whether a given
output is help, critique, or implementation. The explicit role is
what makes the frame reliable — it adapts the model into the mode
the work needs, and holds it there.

## The Human Maintainer

One role is not interchangeable: the **Human Maintainer**. The
Maintainer holds product direction, scientific priorities, and
**final Decision authority** — the accept / reject / supersede
call on every proposal (`lifecycle.md`). Agents propose, review,
implement, and advise; the Maintainer decides. This is the fixed
point of the methodology: a scientific project has a human
accountable for its scientific direction, and Cairn does not
diffuse that accountability into the agent team.

Every adoption elects exactly one Maintainer. A multi-human team
still designates one Decision authority; shared decision rights
are a named follow-up, not the v1 model.

## The role roster

Beyond the Maintainer, the roster is a set of frames any
sufficiently capable agent can fill:

* **Strategy / Research** — surveys the landscape, frames
  problems, drafts proposals, holds the long-horizon view.
* **Implementation** — carries an accepted proposal through its
  plan: the code, the tests, the docs.
* **Internal Reviewer** — the constructive second read
  (`dual-review.md`). Also carries **post-review decision-support**: a
  *neutral briefing* that lays out the decision space for the
  Maintainer — the trade-offs, what each option changes on disk, and a
  defensible recommendation — **without steering** the Decision. It
  supports the Maintainer's call; it does not pre-empt it, and the
  Decision authority stays the Maintainer's.
* **External Reviewer** — the independent, make-it-prove-itself
  read.
* **User Agent** — works from the user's seat: runs the software,
  exercises the workflows, captures friction as issues, and **debugs
  from the user's seat** — reproduces and diagnoses failures from real
  use, rather than from a synthetic test. The capture-vs-fix boundary
  holds even mid-diagnosis: a fix past a trivial, in-scope correction
  is *captured* (routed to the owning implementer or an issue), not
  landed ad-hoc — **scope, not size, is the bar**: diagnosing a bug
  from the user's seat is not authorization to re-decide the owning
  surface's design, so a one-line change that re-decides that design is
  captured, while a larger fix squarely within the bug's own contract
  may land. When the
  team uses an issue tracker, the capture surface (issue structures,
  the capture-vs-fix rule, the tracker-unavailable fallback) is the
  `team-gated/issue-capture` module.
* **Security Review** — a focused-mode pass over the surfaces
  where untrusted input meets the system. Its standing protocol —
  the trust-boundary checklist and the review cadence — is the
  `team-gated/security-review` module, selected when the project
  has a non-trivial trust boundary.

A role is a *frame*, not a person. One agent fills several across
a session; switching roles within a session is fine but must be
**explicit** ("switching to Review mode"). Mixing roles silently
leads to deliberation drift — a reviewer who starts implementing,
or an implementer who quietly re-decides scope.

## The roster scales with the team

The roster is not fixed; it is selected from the team's shape (the
team axes in `dimensions/`). Three points on that scale:

* **Minimal** — the Maintainer plus one generalist agent wearing
  every hat across sessions. The lifecycle and the review tiers
  still hold (Internal review is the same agent in a fresh
  session; External review is the Maintainer, or a second agent
  type when one is available).
* **Small-medium** — **lifecycle-stage roles**: a Strategy agent
  and an Implementation agent, each owning a stage of the
  lifecycle.
* **Large** — **domain-specialized agents**: each Domain Agent
  owns the full proposal → plan → implement arc for one domain of
  the codebase, and review independence comes from domain rotation
  (`dual-review.md`).

The bootstrap reads the team's shape and installs the matching
roster — never more roster than the team can staff. A solo
scientist with one agent is not handed an apparatus built for a
five-agent team; the methodology adapts down as honestly as it
adapts up.

## Confirm the role before substantive work

Because roles produce different artifacts, an agent **names its
role before substantive work** — and if the role is neither
explicit nor inferable from the request, it asks rather than
assuming. Many requests are role-explicit by their verb ("review
this", "implement that"); for those, the agent states the inferred
role and proceeds. The cost of confirming is one sentence; the
cost of guessing wrong is a turn spent in the wrong frame.

## Capability floors — model selection by role and risk

A role is filled by an agent of some capability. In a multi-model
team, *which* model fills which role is not a neutral matter: an
under-capable Reviewer misses the very findings that justify the
Review tier, and a high-capability model filling every role wastes
capacity and develops a context monopoly that erodes structural
independence when it later fills a Review role.

Each role has a **capability floor** — the minimum capability
required to fill the role responsibly given the project's risk
profile. The floor is named using **adopter-local capability tier
labels** (high / medium / low capability); each adopting team
maps the labels to its specific model lineup in its own
configuration.

The default mapping:

* **High-stakes roles** — Strategy / Research, External Review,
  Security Review, Maintainer scribing — require the
  **high-capability tier** by default. The Maintainer may lower
  the floor for a specific session or sub-domain by explicit
  Decision; the default is high.
* **Standard-stakes roles** — Implementation for non-trivial
  work, Internal Review, Code Review — accept the
  **medium-capability tier**; high-tier is permitted when
  available but not required.
* **Low-stakes roles** — Implementation of trivial chunks, User
  Agent for routine workflow exercise, non-substantive doc
  tweaks — accept the **lower-capability tier**; higher tiers
  are not required.

The floor is jointly determined by role **and** risk: the same
role on a greenfield experimental codebase has a lower floor than
on a high-stakes scientific codebase under regulatory review.
Cairn's doctrine names the invariant (a floor exists, by role
and risk); the adopter's project-specific placement on the
complexity axis (`dimensions/complexity.md`) determines the
numerical mapping.

**Diversity within tier.** Where multiple models meet a tier's
floor, structural independence is stronger when the Reviewer is
a different *model architecture* than the author at the same
tier. This strengthens the floor; it does not replace it. The
floor is necessary; model-architecture diversity is the
additional independence gradient.

The mechanism that operationalizes the floor — a tier rubric, a
per-role default mapping template, a worked example — lives in
`templates/modules/team-gated/model-selection.md`, conditionally
installed at the moderate-or-complex end of the complexity axis.
Specific model names, vendor identities, and tier-to-model
mappings stay in the adopter's `case-studies/` write-up; the
doctrine names the invariant, the module instruments it, the
case study identifies the models.
