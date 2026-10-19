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
* **Review is honest.** A reviewer improves a change by questioning its
  foundations — whether it should happen as framed, the best
  alternative, and what would show it wrong — reporting a real
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

**Optional: a signature log.** A team that wants "we agreed to these
norms" to be *auditable* rather than asserted can add a signature ritual —
opt-in, not a default (a solo project needs none):

* **Signature log.** Each participant signs the specific version they
  agreed to, with a short substantive sign-off comment — not just a name.
* **Re-signature on amendment.** Every accepted amendment re-opens the log;
  participants re-sign the new version, so a signature always attests the
  *current* text, never a superseded one.
* **Revision history.** Each amendment row ties the change to its
  triggering proposal / Decision.
* **Decision-time signature.** The Maintainer's Decision *is* the
  acceptance point; the amendment is in force from that row, and the log
  records the date it took effect.

This makes the agreement's authority traceable to who signed what, when —
the agreement analogue of the durable-record discipline Cairn already
prizes. Adopt it when the team is large enough that "everyone agreed" is
worth proving; skip it otherwise.
