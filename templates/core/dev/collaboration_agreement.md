# Collaboration agreement — {{project_name}}

This is the **working agreement** for {{project_name}}'s human + AI
development team. It is short by design: a handful of norms the
team commits to, which the rest of the `dev/` tree then operates.
Amending it is itself a proposal.

## The team

{{project_name}} is built by the **Human Maintainer** and one or
more **AI agents**. The Maintainer holds the project's direction,
its priorities, and final decision authority. Agents propose,
review, implement, and advise; they do not decide.

<!-- cairn:slot team-roster -->
(The bootstrap records the team here: the maintainer; the human
contributors and their roles; the agents and their types.
Refreshed when the team changes.)
<!-- cairn:end team-roster -->

## The norms

* **Substantive change is deliberated.** A change worth a second
  opinion goes through a proposal — it is not committed because
  its author is confident. The lifecycle is in
  `proposals/_template.md`.
* **Review is honest.** A reviewer improves a change and, at the
  External tier, makes it prove it should land — reporting a real
  problem, and reporting honestly when there is none. Confidence
  proves itself.
* **The record is durable and append-only.** Deliberation is
  committed to `dev/`; a prior section is never rewritten, only
  revised by an appended one.
* **The Maintainer decides.** Acceptance, rejection, and
  supersession are the Maintainer's call. An agent unsure whether
  something is a decision surfaces it rather than assuming.
* **Roles are named.** An agent names its role before substantive
  work (see `agent_collaboration.md`); guessing wrong wastes a
  turn.
* **Coordination is through artifacts.** The team coordinates by
  reading and updating the `dev/` tree, not through side channels
  that leave no durable record.

## Amending this agreement

This agreement changes only through the proposal lifecycle — the
same discipline it asks of every other substantive change. A
proposal to amend it is reviewed and decided like any other.
