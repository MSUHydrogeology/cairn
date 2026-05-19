# The Dual-Review model

Cairn's most distinctive practice is its review model. A change
does not ship because its author is confident; it ships because it
has been **reviewed across structural independence** and the
reasoning held up. The model has two tiers, and which tier a
change needs scales with the team (`dimensions/`) and the change's
risk.

## Two tiers, two purposes

* **Internal review** — *helps a change land.* A second reading
  from a constructive stance: catch problems, sharpen the
  argument, surface what the author missed. The Internal reviewer
  wants the change to succeed and is improving it toward that.
* **External review** — *makes a change prove it should land.* An
  adversarial-but-friendly reading: the change must justify
  itself. The External reviewer's job is to make confidence prove
  itself — to look for the reason this should *not* ship, and to
  report honestly when there is none.

The two are not redundant. Internal review improves a change;
External review tests whether it should exist. A change can be
well-improved and still wrong.

## Structural independence

A review is worth only as much as the reviewer's independence from
the author's blind spots. Cairn does not rely on a reviewer
*trying* to be independent; it arranges **structural**
independence — the reviewer's reasoning genuinely does not share
the author's:

* **A different agent type.** A different model architecture has
  different failure modes; it does not silently inherit the
  author's. This is the strongest readily-available independence,
  and it is the External-review floor.
* **A fresh session.** The same agent type, but with no shared
  context — the mental model is rebuilt from the artifacts, not
  carried over. This is the Internal-review floor.
* **A human.** The Maintainer or another contributor.
* **Domain rotation.** On a large team of domain-specialized
  agents, the reviewer is an agent from a *different* domain —
  independence by rotation rather than by model type.

The floors: **Internal review** accepts same-agent-fresh-session;
**External review** requires a different agent type or a human.
Code review — the implementation-side pass — has its own floor:
**not the implementing agent**.

## Asynchronous and commit-mediated

A review is not a live conversation. It is a **section appended to
the artifact** — the proposal, or the plan — and committed. This
is deliberate:

* The review joins the durable, append-only record
  (`lifecycle.md`): a later reader sees the critique, not only the
  outcome.
* It removes the synchronizing cost — author and reviewer need not
  be present at once, which matters across agent handoffs and time.
* It keeps the decision surface in the artifact. A review that
  happened in conversation and was never written down did not
  happen.

## Code review — the implementation side

Proposal review tests the *idea*; code review tests the
*implementation*. The plan-archive precondition (`lifecycle.md`)
makes code review mandatory before a plan archives — the bright
line that stops a fast implementation from closing its own loop.
Code review's floor is stricter than Internal review's: **not the
implementing agent**, because freshly written code is hard to spot
mistakes in for someone carrying the same reasoning patterns.

## Why this is the contribution

The Dual-Review model is a faithful instantiation of **scientific
peer review** — and, on the openness and independence axes, a more
rigorous one: the review is recorded in full, in the open, and the
independence is structural rather than declared. For a
scientific-software audience this is the practice that most
clearly carries the methodology's claim — that software built this
way earns trust the way a result does.

## Adaptation

Review *tiers* are roles any contributor can fill (`roles.md`);
the review *apparatus* is team-gated (`dimensions/`). A solo,
single-agent team runs the kernel's review — the same agent in a
fresh session — and reserves heavier scrutiny for genuinely
contract-touching changes. A team with two agent types, or
multiple humans, runs the full Dual-Review model. The bootstrap
never installs more review apparatus than the team can staff.
