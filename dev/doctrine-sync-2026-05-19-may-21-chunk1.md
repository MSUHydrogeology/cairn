# Doctrine-sync draft — Chunk 1

**Scope.** Cairn-native abstractions for the three doctrine
surfaces Chunks 3, 4, and 5 will apply:

* Chunk 3 — `doctrine/coordination.md` (Tier 2 extension:
  required signal + read mode).
* Chunk 4 — `templates/modules/team-gated/coordination-tiers.md`
  (extensions: collision-log + prune-intents).
* Chunk 5 — `doctrine/session-routines.md` (next-session
  handoff document: rewrite-from-scratch discipline).

**Discipline.** Cairn-native abstractions — invariant, failure
mode, structural fix, module classification — never adopter-
specific file names, tier labels, or model names. Specific
examples live in `case-studies/modflow_tools.md` (Chunk 10).
This draft is the wording-input the chunks consume; it gets
superseded once Chunks 3-5 land and may be removed at
plan-archive.

---

## 1. Work-intent **required-signal-read** mode (for Chunk 3)

### Failure mode

Cairn's Tier 2 today frames work intents as a courtesy signal:
contributors *may* declare before editing a collision-prone
surface; the empty-intent-set means "nobody declared," not
"nobody is working." That framing is correct as a baseline.
But it is structurally silent about a narrower class of files
where the cost of an undeclared concurrent edit is high and
predictable in advance.

Concretely: some files in a working tree are the surface a
team coordinates *through* — handoff notes, planning indices,
collaboration norms, change logs. Two agents editing one of
those files in parallel does not produce a working-tree merge
conflict (the file is usually long, the edits usually touch
different sections) — git silently merges the two patches at
commit time. The team-coordination signal carried by the file
is then mis-attributed: each agent thinks the other read the
state they wrote, when in fact neither did. The hazard is
*staged-index collision* — both edits land, neither agent
saw the other.

The baseline Tier 2 doctrine ("courtesy signal") under-
specifies what discipline applies to *these* files. An
adopter who reads only the baseline ends up treating
high-coordination-cost files identically to incidental
shared files, and discovers the staged-index hazard only
after it strikes.

### Invariant

> For files maintained by multiple agents under asynchronous
> edit, where the file's purpose is to coordinate across
> sessions or across agents, the work-intent protocol is
> **required**: before editing, an agent (a) declares an
> intent naming the file in its paths set, *and* (b) reads
> the current intent set to check for an active intent on
> the same file. An active intent on the same file requires
> deferral or explicit coordination, not concurrent edit.

The invariant has three structural pieces:

1. **Required-signal**: not "courtesy" for this subset — the
   declaration is a prerequisite, not an option.
2. **Required-read**: the protocol is bidirectional;
   declaring without reading the existing set leaves the
   collision hazard intact.
3. **Adopter-identified set**: the doctrine names the
   *kind* of file (multi-agent coordination surface), not
   the specific files. Each adopting team identifies its
   own set and documents it adopter-locally.

### Structural fix vs. social norm

The required mode is structural because the file set is
named in advance and the check is mechanical — "is this
path in the required-list? then signal-then-read." A social
norm ("be careful with shared files") cannot enforce the
read step; the structural rule can.

### Relationship to baseline Tier 2

The required mode *extends* baseline Tier 2; it does not
replace it. Baseline Tier 2 still applies to incidental
shared files where the cost of an undeclared concurrent
edit is low (most code files). Required mode applies to the
adopter-named subset only. An adopter who has not
identified any coordination-surface files runs only
baseline Tier 2.

### Implementation surface (illustrative; not normative)

How an adopter realizes the required-list is adopter-local.
Possibilities: a tracked list in the project's collaboration
doc; a one-line metadata header in each named file; a small
checker script invoked at commit time. The doctrine names
the invariant; the realization is an adopter choice.

### Decision-commit guard-rail (companion)

A second class of files needs a parallel but distinct
discipline: Decision-of-record artifacts (proposal- or
plan-based maintainer Decisions). For these,
the structural rule is not "signal + read" but "the
maintainer's commit permission must be explicit" — an
agent does not commit a Decision section without verbatim
maintainer instruction. This belongs in roles/lifecycle
rather than coordination-tiers, and is covered in Chunk 2
(see lifecycle abstractions there). Mentioned here only
because adopters often discover both patterns at the same
moment (concurrent-edit hazards and Decision-attribution
hazards are siblings).

---

## 2. Next-session handoff document: **rewrite-from-scratch** (for Chunk 5)

### Failure mode

A document that exists to bridge between work sessions —
the file the next session reads to orient before asserting —
has an attractive degenerate mode: each session appends
context, none removes. After N sessions, the document
holds context that is no longer applicable: pointers to
work that has shipped, instructions premised on assumptions
that have moved, decisions that were taken and reversed,
threads that closed.

A reader cannot tell, from the document alone, which
claims are still live and which have aged out. The reader
trusts the document, acts on a stale assertion, and the
session begins on a wrong premise. The cost is high: the
*purpose* of the handoff document is to be the orientation
surface, and an orientation surface that includes false
claims is worse than no orientation surface at all.

This failure mode is structural: append-by-default is the
path of least resistance for every individual session
writer, while the cost of staleness is paid by future
readers — a classic tragedy-of-the-commons shape.

### Invariant

> The next-session handoff document is a **single-session
> product**, written from scratch at goodnight by the
> handoff owner, not an accretion across sessions.
> Durable observations that should outlive one session
> migrate **out** of the handoff document and **into** their
> appropriate durable surface (doctrine, roadmap, proposal,
> reflection) **before** the rewrite. Anything still in the
> handoff document at goodnight that does not earn its place
> in next session's orientation is dropped.

Three structural pieces:

1. **Rewrite from scratch, not edit-in-place.** The
   physical action is "open a blank file and write," not
   "edit the existing file."
2. **Durable-claim migration is upstream of the rewrite.**
   The handoff owner asks "what here should outlive this
   single handoff?" and moves those claims to their durable
   home BEFORE writing the new handoff. The handoff
   document is then free to be one-session-shaped.
3. **Single writer at goodnight.** The handoff is written
   by the designated full-handoff owner (one per session-
   day per Cairn's existing session-routines doctrine), not
   accreted by every participating agent.

### Why this is a session-routines extension, not a new module

Cairn already has the goodnight routine with a designated
full-handoff owner. The rewrite-from-scratch discipline is
one more action in that owner's checklist — alongside
roadmap scrub, test-suite run, reflections read. It is not
a new coordination mechanism; it is the structural rule
for an existing artifact.

### Relationship to the reflections channel

The reflections channel (per-agent, ephemeral, periodically
pruned) is where session-level context is *also* recorded.
The two surfaces have complementary roles:

* **Reflections** are per-agent, write-only-by-author, and
  exist for the agent's own end-of-session sense-making
  plus a handoff signal to the full-handoff owner. They
  are not consumed by the next session directly.
* **The next-session handoff document** is single-writer
  (the handoff owner), consumed by the next session
  directly, and rewritten each goodnight.

The rewrite-from-scratch rule applies to the handoff
document, not the reflections; reflections are already
ephemeral and per-agent and have their own pruning
discipline.

### Implementation surface

The file name (`NEXT_SESSION.md`) is already a Cairn
convention; what this draft adds is the rewrite discipline
on top of it.

---

## 3. Coordination-tiers module: **collision-log** + **prune-intents** extensions (for Chunk 4)

Per Codex External Review Finding F2, these two extensions
live inside the existing team-gated `coordination-tiers`
module, not as new modules. Adopters who selected the
coordination-tiers module (any concurrent team) receive
both extensions; adopters who haven't installed the module
do not need them.

### Extension A — Collision log

#### Failure mode the extension addresses

Cairn's structural-firewall claim ("the work-intent
protocol catches collisions before commit; the typed-event
schema admits no decision field") is durably *stated* in
doctrine but not durably *evaluable*. A team can run for
weeks under the protocol and have no surface that records
whether the protocol actually caught the collisions it
claims to catch — only memory in the participating agents'
reflections, which prune.

Two distinct questions get conflated in the absence of a
log:

* Is the work-intent protocol working as designed?
  (i.e., is the collision rate at or near zero?)
* Has the threshold for the protocol-failure response
  been crossed? (i.e., are we seeing more collisions than
  the protocol's design point assumes?)

Both questions require a *tracked* record across sessions
— a single surface where collision events accumulate and
can be queried over a rolling window.

#### Invariant

> The coordination-tier module ships a tracked log of
> collision events. The log distinguishes **true staged-
> index collisions** (the protocol-failure event) from
> **prevented-overlap** events (the protocol catching a
> collision as designed) and **parallel-non-conflict**
> events (concurrent activity on different files; the
> baseline-rate denominator). Only the first kind counts
> against the protocol-failure trigger; the other two
> are logged for base-rate visibility.

Three structural pieces:

1. **Tracked, not ephemeral.** The log is a tracked file
   in the project; reflections feed it but do not replace
   it. (The migration is part of the goodnight routine —
   see Extension B.)
2. **Narrow event definition.** "True staged-index
   collision" is precisely defined: an event in which one
   agent's commit includes another agent's unstaged or
   unintentionally-staged work, OR an agent must unwind
   its index because another actor's changes landed in
   its commit set. Working-tree merge conflicts caught at
   pull time are *ordinary merge friction*, not the
   structural hazard the protocol targets, and are not
   counted.
3. **Rolling-window trigger.** A protocol-failure threshold
   (more than one true-staged-index event in the rolling
   window on a shared-coordination file) re-opens the
   adopter's architectural question (typically: is the
   current sharding right? is the required-list
   complete?). The window length is adopter-local; the
   *existence* of a rolling-window trigger is doctrine.

#### Why this matters for the structural-firewall claim

Without the log, the claim "the protocol catches
collisions" is a tradition — believed in, not seen. With
the log, the claim is evaluable: the team can read off
how often the protocol failed in the last N days, and
the failure-mode response is gated on data rather than
memory.

#### Implementation surface

A markdown table at a tracked path; columns for date,
event type, file, related commit(s), and a one-line note.
The file is single-writer at intake (the goodnight handoff
owner) sourced from the day's reflections.

### Extension B — Prune-intents (and the migration to the collision log)

#### Failure mode

The work-intent directory accretes "done" intents over
time. After enough sessions, the directory contains many
intents whose work has long since completed, drowning the
signal that "an active intent on this file means an agent
is currently editing it." A reader scanning the directory
for active intents wastes attention on stale ones, or
worse, treats a stale intent as live and defers
unnecessarily.

The complementary issue: collision events recorded in the
day's reflections never reach the collision log unless
someone migrates them; reflections prune, the log is
durable.

#### Invariant

> The full-handoff owner's goodnight routine includes a
> **prune-intents** step (removing or archiving completed
> intents) and a **migrate-collisions** step (appending
> any true-staged-index events from the day's reflections
> to the collision log). Both steps run once per session-
> day, by one writer, at the same point in the routine
> where roadmap scrub and reflections read already occur.

#### Why this is a goodnight extension, not a per-edit rule

The prune step has the same single-writer-at-goodnight
shape as the rest of the handoff routine. Putting it
elsewhere (e.g., per-edit) would multiply the writers and
re-introduce the very coordination hazard the work-intent
protocol exists to prevent. Goodnight is the right place
because it is already single-writer-by-design.

### Module classification

Per Codex F2: both extensions belong inside the existing
team-gated `coordination-tiers` module. An adopter
selecting the module (any concurrent team) receives both;
an adopter who hasn't selected the module does not need
them, because the module-gated invariants are what create
the surface those extensions instrument.

Concretely, the module file gains two new sub-sections
under "Template content": one naming the collision-log
surface + event definitions + rolling-window trigger
shape, and one naming the goodnight prune-intents +
migrate-collisions steps.

---

## Cross-cutting notes

### What stays in this draft vs. what stays in the case study

This draft is *abstraction only*. The concrete adopter
evidence — which specific files modflow_tools puts on its
required-list, what its collision log looks like, what
filename / column-shape / window-length it picked, what
event prompted the original observation — lives in
`case-studies/modflow_tools.md` (Chunk 10). The case study
is the link from this abstraction to the adopter that
surfaced it.

### Discipline check (Codex F5)

A useful self-test for the chunks 3-5 authors: if a draft
sentence references a specific filename, model name, or
adopter-specific term ("Opus", "Sonnet", "GPT-5",
specific doctrine-document filenames, the modflow_tools
plan stem, particular tier numbers, the specific commit-
message convention used for the goodnight commit, etc.),
that sentence belongs in the case study, not in core
doctrine. The doctrine names what an adopter needs to
identify; the case study shows one adopter's identifications.

### What this draft does NOT cover

* The dual-review-side abstractions (Decision-support
  Round-2 review pattern, the structural-property
  decomposition of when Round-2 fires) — those are
  Chunk 2's draft.
* The lifecycle-side abstractions (procedural-gap inline
  Decision, deferred-follow-up revival, PLANNING
  no-history) — those are Chunk 2's draft.
* The role-based-model-selection abstraction (capability
  floor by role and risk; module classification between
  team-gated and dimension-gated) — that is Chunk 2's
  draft.
* The case-study evidence ledger — that is Chunk 10.
* The Cairn `CHANGELOG.md` + version-bump wording — that
  is Chunk 10.

A reader who needs the full picture before Chunks 3-5
land should read this draft alongside the Chunk 2 draft.
