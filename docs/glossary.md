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

**Proposal states** — `proposed` → `reviewed` → `revised` → then `accepted`,
`rejected`, or `superseded`.

**Plan states** — `open` → `executing` → `review` → `archived`.

**Superseded** — a proposal that review blocked *as written*, and whose author
replaced it rather than defended it. Distinct from rejected: the idea survived,
the proposal did not.

**Append-only** — the rule that you add to a proposal rather than editing what
is already there. Like a bound lab notebook: you can write a correction on the
next page, but you do not erase the earlier entry. The record has to show what
you believed *at the time*, not a cleaned-up version.

**Inline-revised** — the opposite rule, used for exploratory notes: take the
review's point, edit the note, and delete the review. Like a working draft
rather than a notebook. Confusingly, both this and append-only use the words
`reviewed` and `revised` — they mean opposite things about what you keep.

**Archive** — the closed end of the lifecycle. An archived artifact is history:
read it for context, do not edit it, and never mine it for metrics.

## Review

**Internal review** — a constructive read that helps a change land. Floor: the
same agent type in a fresh session.

**External review** — a harder read that makes a change prove it should land.
Floor: **a different agent type, or a human**. This floor is what "structural
independence" means in practice.

**Structural independence** — independence you can point at, rather than take
on trust: a different AI model, or a different person. Journals ask whether a
referee is too close to the author, which is a judgement call. This is not.
One honest limit: the record shows *who was named* as reviewer; nothing proves
they were who they said.

**Dual-Review** — the two tiers together. This is Cairn's central mechanism;
the written record exists to serve it.

**Code review** — the review of an implementation, by someone who is not the
implementer. A plan cannot archive until one has occurred.

**Security Review** — a focused mode of Internal or External review, triggered
by named high-risk surfaces rather than by size.

**Comprehension floor** — the rule that you cannot legitimately decide what you
cannot understand. An agent leads plain and keeps precision beneath; "I don't
understand this yet" is a mandatory pause.

## Roles

**Human Maintainer** — final decision authority. The one role that is not
interchangeable.

**Role** — a frame, not a person. Any capable agent can occupy Strategy,
Implementation, or a reviewer tier; name yours before substantive work.

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

**Fold-back** — the channel by which a deployment's improvements return
upstream to the methodology.

**Work-intent** — a claim on files you are about to edit, so concurrent agents
do not collide. Advisory, and it fires.

**Twin** — a file Cairn both ships to you and uses on itself. The two copies
must stay exactly identical, and a test checks that they do.

## Verification

**Verification boundaries** — three separate testing jobs, deliberately not
paid for all at once: quick targeted runs while building, one full run on a
clean tree before review, and the reviewer's own attempt to break it. Re-running
someone else's test command is not the third one.

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
