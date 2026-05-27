# Doc governance — where content lives

A Cairn project keeps its governing instructions in two files, and a
reader — human or agent — must be able to predict which one holds a
given rule without searching both. `AGENTS.md` is the **operational**
reference; `agent_collaboration.md` is the **process** doctrine. This
document is the routing rule that keeps the two from blurring and, over
time, from re-accreting each other's content.

## The three buckets

Sort every piece of governing content into one of three buckets; the
bucket decides its home.

1. **Building the software → `AGENTS.md`.** How to make a correct
   change to *this* project: the architecture, the conventions, the
   test and build commands, the domain-specific rules a contributor
   must follow.

2. **Operating the repository safely as a concurrent multi-agent
   workspace → `AGENTS.md`, as a compact imperative.** The
   *operational safety minimum*: the small set of active gates that
   keep concurrent contributors from corrupting the repository or each
   other's work — commit discipline, the shared-file edit cadence, the
   coordination signal. Stated as terse imperatives a cold-starting
   agent can internalize fast.

3. **The deliberation and decision process → `agent_collaboration.md`.**
   How the team *decides*: the role roster, the proposal → review →
   decision lifecycle, the review tiers and structural-independence
   floors, the session handoff routines — the deeper *why* behind the
   operational rules.

`AGENTS.md` holds buckets 1 and 2 because they are what an agent must
have loaded to act correctly *right now*; `agent_collaboration.md`
holds bucket 3 because deliberation doctrine is read when reasoning
about *how to change the system*, not in the middle of a routine edit.

## One canonical home, thin pointers

Each rule lives in **exactly one** of the two files. The other file may
*point* to it — a one-line cross-reference — but never restates it. The
failure mode this prevents is duplication drift: the same rule copied
into both files, later edited in one, and now silently contradictory.
When you find content that belongs in the other bucket, **move it and
leave a pointer**; do not copy it.

## The operational-safety minimum stays minimal

Bucket 2 is the one most prone to bloat. Every incident tempts a new
"operational" paragraph, and `AGENTS.md` slowly becomes a process
manual a cold-starting agent cannot absorb — which defeats its purpose,
since the operational reference is only useful if it is read and
retained. Hold the line: the operational-safety minimum is a **short
imperative limited to active git / commit / coordination gates** — the
rules that, if missed, let one contributor damage the repository or
another's in-flight work. Detailed walkthroughs, the reasoning behind a
gate, role definitions, templates, and deliberation-process guidance
are bucket 3: they live in `agent_collaboration.md`, and `AGENTS.md`
points to them. A rule earns a place in `AGENTS.md` only if an agent
must follow it to make a correct change *and* it is terse enough not to
crowd out the rest.

## Adaptation

The routing rule is team-size-neutral. A solo project still benefits
from knowing which file a rule belongs in — it keeps `AGENTS.md`
readable as the project grows — and a large multi-agent team needs the
one-home rule to keep the two governing files from diverging. Both
files are part of every Cairn adoption; this rule governs how their
content is split from the first commit, so the duplication never has a
chance to accrete.
