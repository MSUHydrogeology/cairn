# Glossary

Cairn coins more vocabulary than it should. This page defines the terms that
carry weight — the ones you cannot skip and still follow the doctrine. Terms
that are ordinary English used ordinarily are not listed.

If a term you needed is missing, that is a defect worth reporting.

## The lifecycle

**Proposal** — a written argument for a change, made *before* the change
exists. Reviewed independently, then decided. The unit of deliberation.

**Plan** — the execution artifact for an accepted proposal that is large enough
to need one. Chunks, acceptance criteria, verification evidence.

**Lanes** — the three routes a change can take, chosen before anything is
written. *Trivial*: a typo or one-line fix gets the change and its test, with
no proposal and no code review. *Standard*: a change whose shape is settled gets
a short change note, a review, then the change, its test and a code review.
*Deliberate*: a new feature, a contract change or a high-risk surface gets a
proposal, a review, the Maintainer's decision, a plan, a plan review, the
implementation, a code review and an archive. When unsure, take the heavier
lane.

**Change note** — the one short file (about 150 lines or fewer) that the
standard lane uses in place of a proposal and a plan: why, what, approach,
verification, risk.

**Proposal states** — `awaiting-review` ⇄ `revising` → `awaiting-decision` →
then `accepted`, `rejected`, or `superseded`. Each name says who holds the
proposal next. The older words `proposed`, `reviewed` and `revised` are retired.

**Plan states** — `awaiting-plan-review` → `revising-plan` →
`ready-to-implement` → `implementing` → `awaiting-code-review` ⇄
`revising-code` → `ready-to-archive` → `archived`. The older words `open`,
`executing` and `review` are retired.

**Superseded** — a proposal the Maintainer closes because a newer proposal
amends or replaces it. Distinct from rejected: the idea may live on, in the
newer proposal. Like rejected, it archives in the Decision commit.

**Append-only** — the rule that you add to a proposal rather than editing what
is already there. Like a bound lab notebook: you can write a correction on the
next page, but you do not erase the earlier entry. The record has to show what
you believed *at the time*, not a cleaned-up version.

**Inline-revised** — the opposite rule, used for strategy notes (exploratory
writing in `dev/strategy/`): take the review's point, edit the note, and delete
the review. Like a working draft rather than a notebook. Strategy notes carry
their own statuses (`draft`, `reviewed`, `revised`, `settled`, `living`), which
are not the proposal statuses.

**Archive** — the closed end of the lifecycle. An archived artifact is history:
read it for context, do not edit it.

## Review

**Review** — one stance at every stage: a fresh reviewer who did not write the
work reads it on the work's side, asks whether it should exist as framed, what
the best alternative is and what would show it wrong, and answers in writing.
Floor: a fresh session.

**Called read** — a review the Maintainer asked for on one named piece of work,
from more distance: a different AI model, or a person. Also written
**External read**. It happens only when the Maintainer asks; no agent can
require one. The record quotes the Maintainer's words.

**Structural independence** — independence you can point at, rather than take
on trust: every review names its reviewer, so how far they stood from the
author is on the record. Journals ask whether a referee is too close to the
author, which is a judgement call. This is a fact in the file. One honest
limit: the record shows *who was named* as reviewer; nothing proves they were
who they said.

**Dual-Review** — an independent reviewer beside the author at every stage,
then the Maintainer's Decision. The reviewer is a fresh reviewer who did not
write the work. This is Cairn's central mechanism; the written record exists
to serve it.

**Code review** — the review of an implementation, by someone who is not the
implementer. A plan cannot archive until one has occurred.

**Security Review** — a focused review of a high-risk surface, its own pass
beside the usual review, triggered by named high-risk surfaces rather than by
size.

**Comprehension floor** — the rule that you cannot legitimately decide what you
cannot understand. An agent leads plain and keeps precision beneath; "I don't
understand this yet" is a mandatory pause.

**Cairn Plain Language** — the writing standard that gives the comprehension
floor a method: 17 numbered rules for what an agent writes to a person, including
how to separate measured, assumed and expected claims. See
[Cairn Plain Language](plain-language.md).

**Scope-reduction trap** — the pull toward saying "make it smaller." Asking for
less costs a reviewer nothing, looks prudent, and can never be shown wrong,
because the smaller version is the one that gets built. Each cut is defensible
alone; together they leave a long record and little shipped work.

**Outcome test** — how you tell a harmless cut from a real one. Ask whether the
smaller version still delivers what the original artifact *committed to*:
`preserved` (yes — nothing is owed), `degraded` (partly), or `lost` (no).
Compare against the artifact as written, never against a summary of its
purpose written afterwards by whoever is doing the cutting.

**Scope-cut** — narrowing an artifact's stated *claim* to match what it always
did. No work disappears, so it is an ordinary `accept`. Deliberately distinct
from a **scope reduction**, where work that was proposed or accepted stops
happening — only the Maintainer can allow one of those.

**Scope-remainder record** — what a reduction leaves behind, kept as one
grouped record attached to the artifact it came from rather than scattered into
separate backlog rows. It blocks the artifact from being archived until every
entry has been explicitly disposed of. Scattering is the failure it exists to
prevent: fragments preserve the words and lose the reach.

## Roles

**Human Maintainer** — final decision authority. The one role that is not
interchangeable.

**Role** — a frame, not a person. Any capable agent can occupy Strategy,
Implementation, or Reviewer; name yours before substantive work.

## The tree and the tooling

**`dev/`** — the folder holding proposals, plans, notes, and roadmap boards.
Scaffolding for building software, not the point of it.

**Strategy note** — Stage-0 exploration. Written *before* you are ready to
propose, and not a commitment.

**Module** — an optional piece of the apparatus, selected by your dimensional
profile. Some are default-on; some are gated on team shape.

**Dimensions** — the axes (age, size, complexity, language, human team, agent
team) along which the apparatus is fitted to a project.

**Scaffold** — the installer. Writes the selected apparatus into a target
repository.

**Lockfile** — the record of what was installed and its file digests. What
integrity checking and upgrades read.

**Fold-back** — suggesting an improvement back to Cairn itself, by filing an
issue on Cairn's issue tracker using the fold-back template.

**Work-intent** — a claim on files you are about to edit, so concurrent agents
do not collide. Advisory, and it fires.

**Twin** — a file Cairn both ships to you and uses on itself. The two copies
must stay exactly identical, and a test checks that they do.

## Verification

**Verification boundaries** — three separate testing jobs, deliberately not
paid for all at once: quick targeted runs while building (A), the
implementer's scoped record on a clean commit before code review (B), and the
reviewer's own attempt to break it (C). Re-running someone else's test command
is not the third one.

**Certifying run** — the full test suite on a clean, committed tree. It is run
only before a push, before the Maintainer's re-anchor ceremony, before a
release cut, or when the Maintainer asks. One green run certifies every change
at or before it; a change's record cites it as `Certified by: <commit>`, or
`pending` until one exists.

**Independent scientific check** — for a change that touches a scientific
assumption: one named check whose expected answer does not come from the code
or from a test written from the same understanding. The implementer makes the
feared mistake on purpose and records that the check fails.

**Claim check** — the checker that flags broken repository paths and
out-of-bounds line citations before commit. A discipline aid, not a gate.

**Drift gate** — a check that fails when the documentation no longer matches
what it describes. It exists because any hand-written summary of something that
keeps changing will eventually be wrong, and usually without anyone noticing.

**Verify before asserting** — the standing rule that a load-bearing claim is
checked against the tree, not recalled. Most of Cairn's own worst findings have
been claims that sounded right.

## Terms Cairn deliberately avoids

**"Best practice"** — Cairn states what it does and why, and where the evidence
is thin it says so.

**"AI-powered"** — Cairn is a methodology. The agents are yours.
