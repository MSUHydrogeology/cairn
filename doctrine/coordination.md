# Coordination

Multiple contributors — human and AI — work on one codebase
without colliding. Cairn's answer has two parts: a **default
coordination substrate** — stigmergy through a shared `dev/` tree
— and a **Coordination module** of three tiers that escalate with
team concurrency.

## Stigmergy — the `dev/` tree

Cairn's contributors coordinate **stigmergically**: by reading and
updating persistent artifacts, not by message-passing. The shared
artifact *is* the coordination channel. Those artifacts live in a
`dev/` tree — the deliberation layer (`doctrine/README.md`):

* the project charter and the roadmap boards;
* the **deliberation record** — proposals, plans, strategy notes;
* the process doctrine governing deliberation itself.

An agent picks up work by reading the `dev/` tree; it hands work
off by updating the `dev/` tree and committing. Nothing
load-bearing lives only in a conversation. This is what lets the
methodology survive context loss, agent handoff, and time: the
durable record is the source of truth, and it is reconstructible
from version control alone.

**Model-agnostic resilience.** Because the coordination channel is
a tree of git-committed files — not a live protocol bound to one
vendor's API — Cairn's coordination depends on no specific AI
tool. A team can run several agent types at once, swap one vendor
for another, or move to a locally-hosted open-weights model, and
the `dev/` tree is unchanged: the orchestration *is* the
filesystem and git, which every tool already speaks. This is a
deliberate resilience property. The dominant 2025 agent protocols
(MCP, A2A, ACP) couple a team's coordination to specific agent
infrastructure; stigmergy does not. An adopting project is never
locked to the model or vendor it started with — the methodology
outlives any single one.

## The Coordination module — three tiers

The deliberation record coordinates *what to build*. A second,
narrower problem is coordinating *who is editing what, right now*,
so two contributors do not collide mid-edit. The Coordination
module addresses it with three tiers that escalate with team
concurrency — one design with a parameter, not three separate
mechanisms.

### Tier 1 — baseline: shared-file & staged-index discipline

Always on, for any version-controlled adoption. A small set of
commit-time rules: a restricted edit cadence on the shared
communication files (the roadmap boards, the changelog),
path-scoped commits (commit named paths, never the whole index),
and the staged-index collision rules. This tier alone suffices for
a solo or sequential team.

### Tier 2 — asynchronous: work intents

For concurrent teams. The baseline catches collisions at *commit*
time; it gives no *pre-edit* signal. A **work intent** adds one:
before touching a collision-prone surface, a contributor writes a
short, untracked file declaring who holds which paths, with what
intent, and a status. It is a courtesy signal, not a lock — it
helps a second contributor *notice* an overlap before editing.

**Required signal+read for coordination-surface files.** A narrow
subset of files in any working tree exists *to coordinate across
sessions or across agents* — handoff notes, planning indices,
collaboration-norm documents, change logs. The courtesy framing
under-specifies the discipline for these: two contributors
silently editing different sections of a long shared file produce
no working-tree conflict, git merges both patches at commit time,
and the coordination signal each thought the other had read was
never read at all. For this subset the protocol upgrades to
**required**: an agent (a) declares an intent naming the file in
its paths set, *and* (b) reads the current intent set to check
for an active intent on the same file. An active intent on the
same file requires deferral or explicit coordination, not
concurrent edit. The required mode extends baseline Tier 2; it
does not replace it. Incidental shared files keep the courtesy
framing. Each adopting team identifies its own required-mode set
— the structural rule is doctrine; the file list is adopter-
local.

### Tier 3 — real-time: typed activity events

For high-concurrency, domain-agent teams. A minutes-scale signal:
an append-only log of **typed activity events** — a typed event
channel, not a chat channel.

### Substrate convergence

The Tier-2 work-intent signal and the Tier-3 typed-event log are
*purposes*, not file formats. Both can ride a single
**append-only claim/release log**: a `claim` event records who
holds which paths with what intent and a unique id; a matching
`release` event (shared id) closes it; active intents are claims
without a release. A team need not maintain a directory of
per-intent files to get Tier 2 — one append-only log, written
through atomic small-record appends, serves both tiers and makes
the "who is touching what right now" query a single read. The
per-file form remains valid; the log form is the recommended
substrate once a team has any concurrency, because it gives the
release lifecycle and the auto-close-on-commit hook (below) a
clean home.

## Coordination identity — per-session, not per-agent

A coordination mechanism that records *who* holds a path needs an
identity for that holder. The naive choice — one identity per
**agent** or per **tool** — silently breaks the moment a team runs
**multiple concurrent sessions of the same tool**: every session
resolves to the same identity, so one session's commit-time
auto-release closes *another* session's still-active claims, and
the pre-edit signal each session reads cannot distinguish "my own
claim" from "a sibling session's claim." The identity must be
**per-session**.

The portable rules:

* **Derive identity from the harness's session-scoped
  identifier**, not from a static per-tool name. Most agent
  harnesses expose a session id in the environment of the shells
  they spawn; it is stable across calls within a session and
  distinct across concurrent sessions. Both the pre-edit claim and
  the commit-time auto-release run inside the same session, so both
  resolve the same value — and sibling sessions resolve different
  values.
* **Hash the *whole* session id; never take a prefix.** Session ids
  are often time-ordered (e.g. UUIDv7), whose leading bytes are a
  shared timestamp — exactly the part two near-simultaneous
  sessions hold in common. A prefix-derived identity therefore
  collapses precisely the concurrent sessions this rule exists to
  separate. Hash the full id (e.g. a short hash digest) so the
  derivation is collision-safe and harness-neutral regardless of
  the id's flavor.
* **A static, machine-global identity override is an escape hatch,
  not a setting.** An explicit override (env var, config file) is
  useful for tests and deliberate one-offs and should remain the
  highest-priority resolution tier. But a *global* override
  (shell-profile export, shared config) re-introduces the exact
  shared-identity collapse — every session on the machine resolves
  to one identity. Keep the override for one-offs; warn when it
  shadows an available session id; never recommend it as a profile
  setting.
* **Auto-release closes only the committing session's own claims.**
  A post-commit hook that releases active claims whose paths
  intersect the commit is safe *only* because the per-session
  identity scopes it: it matches `claim.identity == this session
  AND paths intersect`. Identity-resolution failure must fail soft
  — warn and skip, never block the commit.

This is a methodology contribution in its own right: it is what
makes a release lifecycle (and its auto-close hook) correct under
same-tool concurrency, which is the common case for AI-agent teams
where one tool spawns many parallel sessions.

## The structural firewall

A real-time channel is dangerous to the methodology: real-time
conversation is the medium in which decisions naturally form, and
a decision that forms in chat and never reaches an artifact erodes
the durable record that gives Cairn its bite. The firewall is
**structural, not a remembered norm**. A Tier-3 event has a
constrained type — `start`, `heads_up`, `query`, `handoff`, `ack`,
`release` — and a fixed set of fields: agent, role, paths,
artifact, a short activity note. There is **no free-form decision
or rationale field.** A decision-bearing exchange is expressed by
pointing an event *at* the proposal or plan where the decision is
written; the event references the artifact, it does not contain
the decision. Because the schema admits no place to write a
decision, one cannot be written there. The same firewall — and
the same false-clear discipline — applies to Tier 2: an empty
work-intent set means "nobody declared," never "nobody is
working"; version-control state stays the source of truth.

## The hybrid-coordination doctrine

Cairn is therefore **hybrid**: stigmergic for the durable
*deliberation* layer, real-time for the ephemeral *coordination*
layer, with the structural firewall between them. The deliberation
differentiator is untouched; only coordination latency is
addressed. This split is itself a methodology contribution — it
shows how to add real-time agent coordination *without*
surrendering the recorded-deliberation discipline.

## Scope and limits

* **v1** ships Tier 1, Tier 2, and — for Tier 3 — only the local
  append-only typed-event log, the safest and most auditable form.
  A structured message channel, a real-time bus, and chat-room
  integration are named, cautioned follow-ups, gated on observed
  need.
* **Worktree topology.** Untracked work-intent and event-log files
  are visible only within one shared working tree. Multiple
  worktrees need a shared sidecar location or a tracked artifact;
  multiple clones or machines need the issue tracker or an
  approved shared service. A concurrency ladder must not recommend
  per-domain worktrees and then break the coordination mechanism
  it just introduced.
* **Compaction guard rail.** Two rules. Never depend on the
  channel for *project or decision* state — that reconstructs from
  the durable record, and a session starts by reading artifacts,
  never the channel. But a resuming agent *may* re-read the
  append-only event log to re-acquire ephemeral *coordination*
  state — who is touching what right now — which is safe because
  the log is activity-only.
* **Privacy.** Coordination mechanisms are local by default;
  generated coordination files carry no secrets, credentials,
  local machine paths, or proprietary data; routing activity
  through any third-party service requires explicit Maintainer
  approval.

## Adaptation

Tier 1 is part of the invariant kernel — default-on for every
adoption. Tiers 2 and 3 are team-gated (`dimensions/`): a
concurrent team enables work intents; a high-concurrency
domain-agent team additionally enables the typed-event log. A
solo or sequential team runs only the baseline.
