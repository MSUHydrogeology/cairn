# Related practices, and what Cairn does differently

Cairn's ideas are not new. Recording decisions, reviewing before building, and
keeping a lab notebook are all long-established. If Cairn looked at you and
said "this is unprecedented," you should be suspicious.

So here is the honest comparison. Each section names a practice that overlaps
with Cairn, what it does well, and the one thing Cairn does differently. Where
the answer is "nothing much," it says so.

## Architecture Decision Records

**What they are.** Short documents, kept in the repository, recording an
architectural decision and its context — popularised by Michael Nygard around
2011 and now common in software teams.

**Overlap.** Substantial. Both are lasting documents about a decision, kept in
version control beside the code they concern.

**The difference.** A decision record is usually written *after* the decision,
to explain it. A Cairn proposal is written *before* the work, and something has
to happen to it — an independent read, a reply, a decision — before anyone
starts building. A decision record documents. A proposal has to be got past.

If your team keeps ADRs and is happy, you already have most of the value Cairn's
record provides. The part you do not have is the review tier.

## RFC, PEP, NEP, APE — community proposal processes

**What they are.** Structured proposal-and-review processes: the IETF's RFCs,
Python's PEPs, NumPy's NEPs, Astropy's APEs. A written proposal, public
discussion, a decision by a named authority.

**Overlap.** Large, and Cairn's lifecycle is openly modelled on this shape.

**The difference.** Two, both about scale. Those processes are built for
changes that affect thousands of people, where a written round of review is
cheap next to the consequences of getting it wrong. Cairn applies the same
shape to ordinary day-to-day changes in one repository — which only works if
the process stays light. Keeping it light is a live problem, not a solved one.
Second, Cairn's reviewers are usually AI models, so independence means *a
different model* rather than someone at a different institution.

If you already run something like this, Cairn's version will feel familiar.
Read it as the same idea, sized for one scientist working with agents.

## The lab notebook

**What it is.** The scientist's contemporaneous record of what was done, why,
and what happened.

**Overlap.** This is the closest cultural analogue, and Cairn's `dev/` tree is
best explained to a scientist as a lab notebook for software decisions.

**The difference.** A lab notebook records; it does not gate. Nothing in the
notebook convention says an entry must be independently read before the next
experiment runs. Cairn adds that step, and makes the reviewer's identity and
independence part of the record.

## Registered reports and pre-registration

**What they are.** In empirical science, committing to hypothesis, method, and
analysis *before* collecting data, so the analysis cannot be shaped to the
result.

**Overlap.** Direct, and deliberate. A Cairn proposal commits to what would
falsify the change before the implementation exists — the same move.

**The difference.** Mostly scope. Pre-registration governs a study; Cairn
applies the discipline to a code change. The shared insight is identical: a
plan written after you have seen the outcome is not a plan.

This is also where Cairn's own measurement work is bound — a study of the
method registers its analysis before the data exists, for the same reason.

## Code review

**What it is.** Another engineer reads a change before it merges.

**Overlap.** Cairn's code-review tier *is* this, with one added rule: the
reviewer must not be the implementer.

**The difference.** Cairn's earlier tier has no equivalent in normal code
review. Ordinary review happens after code exists, so it can catch a bug and
rarely questions the premise. Cairn's proposal review happens when there is
nothing to read but the argument, which is the only point where "this is the
wrong thing to build" is a cheap finding.

## Agile, Scrum, and the rest

**Overlap.** Little that is specific. Cairn says nothing about sprint length,
estimation, stand-ups, or team roles beyond who reviews what.

**The difference.** Cairn is about one change at a time — how it is argued,
checked, and recorded — not about how work is scheduled or divided. It sits
underneath whichever way you organise, and works the same if you organise no
particular way at all.

## Multi-agent AI frameworks

**What they are.** Systems that run several AI agents together — having them
debate, giving each a speciality, passing messages between them.

**Overlap.** Cairn has multiple agents in named roles, which looks similar from
the outside.

**The difference.** Cairn's agents do not talk to each other. They read and
write files in your repository, and that is the whole coordination mechanism.
The cost is real: nothing happens in real time, and no agent knows what another
is doing except by reading what it wrote. The payoff is also real — there is no
server to run, nothing to keep alive between sessions, and any AI tool that can
read and write files can take part. It is why changing tools does not change how
you work.

## So what is actually distinctive?

Stripped of everything shared:

1. **The review happens before the code exists**, when saying "that is the
   wrong thing to build" is still cheap.
2. **You can check that the reviewer was independent** — a different AI model,
   or a person — rather than taking it on trust.
3. **What would show the change to be wrong is written down first.**
4. **The whole exchange stays in your repository**, not in a chat history you
   cannot search a year later.

Each of these exists somewhere in the practices above. The combination, applied
to ordinary changes in a scientific codebase worked on by AI agents, is what
Cairn is.

**And the honest caveat**: none of this is validated by a controlled study.
Cairn is grounded in the research on human-AI development and explicit about
where it diverges — see [`doctrine/rationale.md`](../doctrine/rationale.md) —
but "grounded in" is not "proven by." If you want the evidence status of a
particular claim, that file is where it is stated.
