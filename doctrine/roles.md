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
a reviewer's stance and an implementer's stance produce
genuinely different readings of the same change. Stating the role explicitly *anchors* the agent in
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
* **Reviewer** — a fresh reviewer who did not write the work, on the
  work's side (`dual-review.md`): it questions the work's foundations
  and answers the stage's three questions in writing. Also carries
  **post-review decision-support**: a *neutral briefing* that lays out
  the decision space for the Maintainer — the trade-offs, what each
  option changes on disk, and a defensible recommendation — **without
  steering** the Decision. It supports the Maintainer's call; it does
  not pre-empt it, and the Decision authority stays the Maintainer's.
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
  every hat across sessions. The lifecycle and the one review
  still hold (the reviewer is the same agent in a fresh session;
  the Maintainer may ask for a different agent type, or read it
  themselves, when they want more distance).
* **Small-medium** — **lifecycle-stage roles**: a Strategy agent
  and an Implementation agent, each owning a stage of the
  lifecycle.
* **Large** — **domain-specialized agents**: each Domain Agent
  owns the full proposal → plan → implement arc for one domain of
  the codebase, and the one reviewer can come from a different
  domain (domain rotation, `dual-review.md`).

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

## When to dispatch which role

Naming the role is upstream of a prior question the Maintainer faces
every session: *which* role does this piece of work want? A few
heuristics, by the kind of work:

* **Strategy / Research** — when the work is *framing*, not building: a
  problem-space characterization, an audit of an emerging concern, a
  multi-year direction, or a decision that needs options weighed before
  any code. If you cannot yet name the files a change touches, you are
  in Strategy, not Implementation.
* **A Domain role** (the partitions your profile defines — e.g. by
  subsystem) — when the work needs *judgment about a specific area's
  contracts and invariants*. Reach for the domain even when **no code is
  touched**: a proposal that only moves docs or renames a config still
  changes a domain's contract, and "no code touched ≠ no domain
  involvement" — a doc that misstates a subsystem's behavior is a domain
  defect. Route a change *through* the domain that owns the surface, not
  around it.
* **Legacy** — when the change lands in an undocumented or untested part
  of the tree, where the safe move is to characterize current behavior
  before altering it. Legacy is a *precondition discipline*, not a
  separate task: it gates the Implementation that follows.
* **The Reviewer** — when a substantive change is ready to be
  questioned: a fresh session, asking the stage's three questions
  (`dual-review.md`). The dispatch does not pick a kind of review. The
  Maintainer may ask for more distance on one named artifact; that call is
  theirs, never inferred from the change's risk or size.

The dispatch is a frame, not a person: one capable agent fills many of
these across a week. The point is to enter each piece of work in the
*right frame*, because the frame determines the artifact — and the
wrong frame produces a confident artifact of the wrong kind.

## Capability floors — model selection by role and risk

A role is filled by an agent of some capability. In a multi-model
team, *which* model fills which role is not a neutral matter: an
under-capable Reviewer misses the very findings that justify the
review, and a high-capability model filling every role wastes
capacity and develops a context monopoly that erodes its distance
from the author when it later fills a Review role.

Each role has a **capability floor** — the minimum capability
required to fill the role responsibly given the project's risk
profile. The floor is named using **adopter-local capability tier
labels** (high / medium / low capability); each adopting team
maps the labels to its specific model lineup in its own
configuration.

The default mapping:

* **High-stakes roles** — Strategy / Research, proposal review
  (the premise is still movable, and a wrong one is cheapest to catch
  there), Security Review, Maintainer scribing — require the
  **high-capability tier** by default. The Maintainer may lower
  the floor for a specific session or sub-domain by explicit
  Decision; the default is high.
* **Standard-stakes roles** — Implementation for non-trivial
  work, plan review, code review (whose floor is also **not the
  implementing agent**) — accept the **medium-capability tier**;
  high-tier is permitted when available but not required.
* **Low-stakes roles** — Implementation of trivial chunks, User
  Agent for routine workflow exercise, non-substantive doc
  tweaks, and docstring and comment cleanup (below) — accept the
  **lower-capability tier**; higher tiers are not required.

**Docstring and comment cleanup, and related edits, may be written at low.**
This covers an edit that changes only docstrings, comments and other
non-executable wording: no executable token, and no bytes that a test, manifest
or attestation pins. It lowers the writing step only. The review keeps its
stage's floor (medium for code review), and where the edit touches a surface
this project's `AGENTS.md` names as high-risk it also owes the Security Review
that surface already requires, at high. Nothing in this row lowers a review or
removes a Security Review.

The floor is jointly determined by role **and** risk: the same
role on a greenfield experimental codebase has a lower floor than
on a high-stakes scientific codebase under regulatory review.
Cairn's doctrine names the invariant (a floor exists, by role
and risk); the adopter's project-specific placement on the
complexity axis (`dimensions/complexity.md`) determines the
numerical mapping.

**Diversity within tier.** Where multiple models meet a tier's
floor, a different *model architecture* than the author's is
available as useful distance when the Maintainer assigns it or
asks for it. It strengthens the floor; it does not replace it, and
it is never a default an agent applies. The floor is necessary;
model-architecture diversity is distance on request.

The mechanism that operationalizes the floor — a tier rubric, a
per-role default mapping template, a worked example — lives in
`templates/modules/team-gated/model-selection.md`, conditionally
installed at the moderate-or-complex end of the complexity axis.
Specific model names, vendor identities, and tier-to-model
mappings stay in the adopter's `case-studies/` write-up; the
doctrine names the invariant, the module instruments it, the
case study identifies the models.

**Orchestrated work — the fan-out.** The floor binds not only the
human-role roster but **orchestrated sub-agents**: a fan-out leaf
takes its floor from its own task, never by inheriting the
orchestrator's tier — the place the model-cost multiplier is
largest. A stronger, independent check can lower a *generative*
step's floor only when the model that checks the output is strictly
more capable **and** a different model architecture (same-model
fresh-session independence is *time* independence, not capability
headroom), acceptance criteria are pre-declared, the output is
falsifiable without trusting the author, and a failed check
escalates rather than retrying at the cheap tier.

**The cost rule's check is not a review.** An orchestrator may run a
sub-agent's generative step on a cheaper model only when the model that checks
the output is at a tier strictly above it and is a different model
architecture; a stronger model from the same maker is not one. The check is
the orchestrator's. It is never filed as a proposal, plan or code review pass
and never counts toward one, and no lifecycle review requires a different
architecture. Sending the context packet to a second maker's model crosses the
data-governance gate below, so that gate applies first.

Bright-line work never downshifts, and **no downshift
crosses a data-governance boundary**, regardless of cost. The
`model-selection` module holds the authoritative lists — the
bright-line set (Security Review, the high-risk trust boundaries,
premise-checking, novel design) and the
data-governance / tool-parity gate (proprietary code, collaborator
data, unpublished work, the security-review surface) — alongside the
task-type→tier rubric that operationalizes all of this.
