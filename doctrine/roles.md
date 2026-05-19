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
  (`dual-review.md`).
* **External Reviewer** — the independent, make-it-prove-itself
  read.
* **User Agent** — works from the user's seat: runs the software,
  exercises the workflows, captures friction as issues.
* **Security Review** — a focused-mode pass over the surfaces
  where untrusted input meets the system.

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
