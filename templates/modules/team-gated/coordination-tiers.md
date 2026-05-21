# Module: coordination-tiers

**Selected when:** the agent team is **concurrent** — more than
one agent in the working tree at once (the Agent-team axis). The
work-intent tier is added for any concurrent team; the typed-event
tier is added only for high-concurrency, domain-agent teams.
**Adds to:** the coordination section of
`dev/agent_collaboration.md`.

The kernel's baseline coordination — path-scoped commits, the
shared-file discipline — catches collisions at *commit* time. This
module adds the higher tiers of the Coordination module, which
give a *pre-edit* signal.

## Template content

Merged into the coordination section:

> **Tier 2 — work intents (concurrent teams).** Before touching a
> collision-prone surface, an agent writes a short, untracked file
> declaring who holds which paths, with what intent and status. It
> is a courtesy signal, not a lock. An empty intent directory
> means "nobody declared", never "nobody is working" —
> version-control state stays the source of truth.
>
> **Tier 3 — typed activity events (high-concurrency teams).** An
> append-only log of typed events — `start`, `heads_up`, `query`,
> `handoff`, `ack`, `release` — a typed channel, not a chat
> channel. The event schema carries no free-form decision field:
> a decision-bearing exchange points an event *at* the proposal or
> plan where the decision is written. The schema is the firewall.

A sequential team runs neither tier — only the kernel's baseline
discipline.

## Extensions

Two structural extensions ship with this module. Both
instrument the firewall claim `doctrine/coordination.md`
makes — that the work-intent protocol catches collisions
before commit, and that an empty intent set never means
"nobody is working" — by giving the team a durable
surface that records when the protocol fails and a
goodnight-time hygiene step that keeps the surface usable.

### Extension — Tracked collision log

A doctrine claim is durable in prose but not durably
*evaluable* without a record. The collision log is that
record: a tracked file recording the staged-index events
the protocol exists to catch, queryable across sessions.

Merged into the coordination section:

> **Collision log (concurrent teams).** The team maintains
> a tracked file recording staged-index events within the
> working tree. The log distinguishes three event kinds:
>
> * **true-staged-index** — one agent's commit includes
>   another agent's unstaged or unintentionally-staged
>   work, *or* an agent must unwind its index because
>   another actor's changes landed in its commit set.
>   Working-tree merge conflicts caught at pull time are
>   ordinary merge friction, *not* this event.
> * **prevented-overlap** — the work-intent protocol
>   caught a would-be collision before edit; recorded for
>   base-rate visibility.
> * **parallel-non-conflict** — concurrent activity on
>   different files; recorded as the baseline-rate
>   denominator.
>
> Only `true-staged-index` events count against the
> protocol-failure trigger. The team picks a rolling
> window; more than one `true-staged-index` event on a
> shared-coordination file within the window re-opens the
> team's architectural question — is the sharding right,
> is the required-mode set complete, is the typed-event
> log warranted? The window length is adopter-local; the
> existence of a rolling-window trigger is the structural
> rule.

### Extension — Goodnight intent-hygiene

Two complementary failures motivate the hygiene step. The
work-intent directory accretes "done" intents over time,
drowning the live signal: a reader scanning the directory
for active intents either wastes attention on stale ones
or treats a stale intent as live and defers unnecessarily.
And collision events recorded in the day's reflections
never reach the durable log unless someone migrates them
— reflections prune; the log is durable.

Merged into the coordination section (and operationally
sequenced alongside the goodnight routine in
`doctrine/session-routines.md`):

> **Goodnight intent-hygiene steps (concurrent teams).**
> The full-handoff owner's goodnight routine includes two
> steps that operate on the coordination surfaces:
>
> * **Prune-intents** — completed work intents are
>   removed or archived; the live directory holds only
>   intents whose work is still in flight.
> * **Migrate-collisions** — any `true-staged-index`
>   events from the day's reflections are appended to
>   the collision log.
>
> Both steps run once per session-day, by one writer, at
> the same point in the routine where roadmap scrub and
> reflections read already occur. The single-writer-at-
> goodnight shape is what lets the prune step run without
> reintroducing the very coordination hazard the
> work-intent protocol exists to prevent.

A sequential team runs neither extension; a concurrent
team that selected this module receives both.
