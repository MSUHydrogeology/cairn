<!-- cairn-internal-ref-allow: doctrine/coordination.md doctrine/session-routines.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
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
> collision-prone surface, an agent records a **claim** in a single
> append-only `dev/intents.jsonl` log — who holds which paths, with
> what action — and the claim is **auto-released** when the work
> lands (a post-commit hook closes claims whose paths the commit
> touched). It is a courtesy signal, not a lock. An empty active set
> means "nobody declared", never "nobody is working" —
> version-control state stays the source of truth. Cairn ships the
> tool that implements this (`tools/intent.py`, installed with this
> module); see "The work-intent tool" below.
>
> **Required scope (this concurrent team).** A `claim` is
> **required before every nontrivial edit** — any change that
> touches tracked files, alters behavior / doctrine / tests / docs,
> or plausibly overlaps another contributor's work. Trivial
> read-only checks and one-line mechanical follow-ups with no
> collision surface are exempt. The **coordination-surface** subset
> — the roadmap boards, the changelog, handoff and collaboration-norm
> docs — additionally requires the **`list`** read before editing
> (both halves: signal *and* read), because a silent concurrent edit
> there merges cleanly yet loses the coordination signal. Even
> required, the claim stays a **courtesy signal, not a lock**: it
> surfaces an overlap before the edit lands, it does not block the
> edit or reserve the path. (A solo or sequential team runs none of
> this — the broad requirement is the *Tier-2* posture, gated to
> concurrency.)
>
> **Tier 3 — typed activity events (high-concurrency teams).** An
> append-only log of typed events — `start`, `heads_up`, `query`,
> `handoff`, `ack`, `release` — a typed channel, not a chat
> channel. The event schema carries no free-form decision field:
> a decision-bearing exchange points an event *at* the proposal or
> plan where the decision is written. The schema is the firewall.

A sequential team runs neither tier — only the kernel's baseline
discipline.

## The work-intent tool

Selecting this module installs a runnable reference tool —
`tools/intent.py`, a stdlib-only CLI — so the Tier-2 protocol is a
command, not homework. (The doctrine above is the *why*; this is the
*how*.) The scaffold also seeds `dev/intents.jsonl` into `.gitignore`
(the log is session-local coordination state, never a tracked
artifact).

> **Running it.**
>
> * `python tools/intent.py claim --files <paths> --action "<summary>"`
>   — record a claim before editing a collision-prone surface. The
>   claim runs an immediate **conflict-check** against active claims and
>   warns you about overlaps, so the signaler gets immediate, actionable
>   value at the moment of signaling.
> * `python tools/intent.py list [--conflicts-with <paths>]` — show
>   active intents (optionally only those overlapping given paths).
> * `python tools/intent.py release <id>` — close a claim manually
>   (rarely needed; the hook does this automatically).
> * `python tools/intent.py install-hook` — **opt-in**: install a
>   post-commit hook that auto-releases the committing session's claims
>   whose paths the commit touched. The scaffold prints this command but
>   never runs it for you; the installer chains onto an existing
>   `post-commit` hook and **refuses** (without modifying the file) a
>   framework-managed (pre-commit / husky), non-shell, or non-executable
>   hook. `--uninstall` removes it.
> * `python tools/intent.py install-precommit` — **opt-in**: install the
>   **work-intent pre-commit check** (below). Narrower than `install-hook`:
>   it installs only into an absent `pre-commit` hook or one already
>   carrying the intent sentinel, and **refuses** (without modifying the
>   file) any foreign / framework-managed hook. `--uninstall` removes it.
> * `python tools/intent.py hooks-status` — report whether each of the
>   two hooks (post-commit auto-release, pre-commit work-intent check) is
>   installed. The one stable command session-start points at.

**Enforce mode.** The pre-commit check **blocks by default** — absent or
malformed `dev/intent-config.json`, it refuses a commit whose staged path is
held by a **different live session's** claim, while an unclaimed path only
*warns* (warn-on-unclaimed + block-on-cross-claim). Set `"enforce"` in
`dev/intent-config.json` to change it: `warn` (surface only, never block — opt
back into the old advisory-only behavior), `confirm` (proceed only on explicit
acknowledgement; degrades to `block` with no controlling terminal), or `block`
(the default; setting it explicitly is equivalent). The block fires only on a
**provably different live session**: the check recognizes the committer's *own*
claims by the per-session token and never blocks them, and a committer with **no
resolvable session token degrades to warn-only** (a static identity is shared
across same-type sessions, so ownership cannot be proven — the warning still
surfaces, but the strong action is withheld rather than misfiring on a possibly
own claim). A **stale** claim — older than the claim TTL (default **4h**,
configurable via `"claim_ttl_hours"`) — still warns but never blocks, so a
crashed or abandoned session cannot wedge a live committer. The
`CAIRN_INTENT_ALLOW_UNCLAIMED` bypass (or a tracked `{"solo_mode": true}`)
overrides the block for a deliberate one-off. (Doctrine: Cairn's
`doctrine/coordination.md` > "Enforcing the coordination check".)

**Claim before you edit.** The Tier-2 workflow is one habit: before
touching a collision-prone surface, run `python tools/intent.py claim`; the
immediate conflict-check tells you on the spot whether another session
already holds it. The post-commit hook then closes your claim when the work
lands, so the steady-state ceremony is a single `claim` per piece of
work. The session-start routine (`doctrine/session-routines.md`) carries
the *read* half — `python tools/intent.py list` before the first edit.

**The work-intent pre-commit check** is the structural *opening*
counterpart to the post-commit auto-release. Where the post-commit hook
*closes* a claim cheaply (no action required of a well-behaved author),
the pre-commit check *catches a missed claim at the moment it matters
most* — it reads the commit's staged set (`git diff --cached`, never
unstaged files) and **warns** when a staged path carries no active claim,
and (by default) **blocks** when a staged path is **held by a different
live session** (the shipped enforce-mode default is `block`; see *Enforce
mode* below). This closes the asymmetric-reward gap
`doctrine/coordination.md` names: releasing is automatic, so claiming must
be the one deliberate act, and the pre-commit check is what makes
forgetting it visible — and, for a genuine cross-session collision,
blocking — rather than silent.

> **Suppressing the self-directed warnings.** A solo or
> intentional-unclaimed commit silences the *self-directed* warnings (a
> staged path with no claim; an unresolvable identity) with a per-commit
> `CAIRN_INTENT_ALLOW_UNCLAIMED=1` env override, or repo-wide with a
> tracked `dev/intent-config.json` carrying `{"solo_mode": true}`. An
> **other-session-overlap** warning is **never** suppressed — that is the
> coordination payoff, and it must always surface.

**Shared-tree commit hygiene.** The pre-commit block is a *mitigation*, not a
cure. In a shared working tree (two agents, one git index), a bare `git commit`
with no pathspec commits the *whole* staged index — sweeping another session's
staged-but-uncommitted work into the wrong commit, under the wrong author. Three
habits, in increasing strength:

* **Verify the staged set before every commit** — `git status --short` (or a
  working-tree diff over the paths you mean to commit), so you see exactly what
  will land.
* **Scope commits explicitly in a shared tree** — `git commit -- <paths>`,
  naming the files the commit should contain. (Pathspec-commit takes
  *working-tree* content for those paths, so it is incompatible with
  `git add -p` partial staging — pick one.)
* **The root-cause cure is per-agent worktree isolation** — separate worktrees
  share no index, so there is no staged set to collide on. Pathspec-scoping and
  the fail-closed pre-commit hook are mitigations for the shared-tree case
  adopters will still hit; worktree isolation removes the hazard.

Recurrence of the event this guards against — one session's commit sweeping
another's staged work — is recorded as a `true-staged-index` entry in the
tracked **collision log** (`dev/measurement/collision_log.md`; see *Extension —
Tracked collision log* below). More than one such event on a shared-coordination
file within the team's rolling window re-opens the coordination-architecture
question.

**Per-session identity.** Identity resolves from `$CAIRN_AGENT` (an
explicit override / escape hatch), then a **per-session** value derived
from the harness's session env var, then a static `~/.cairn/agent.json`
`agent` key. An adopter on a harness the built-in registry does not know
adds a `[tool_tag, env_var]` pair under `harness_session_vars` in that
JSON config — **no edit to the tool**. The per-session derivation (and
why a global `$CAIRN_AGENT` export is an escape hatch, not a setting) is
the doctrine in
`cairn/doctrine/coordination.md` >
"Coordination identity — per-session, not per-agent".

**Atomicity is best-effort + filesystem-dependent.** The append uses a
single small `O_APPEND` write — non-interleaving on local filesystems
(APFS, ext4, xfs, btrfs), but **not** guaranteed on networked / overlay
filesystems (NFS, SMB, Windows shares, container overlay FS). A team on
such a filesystem, or at very high concurrency, should keep the `dev/`
tree on a local checkout and treat the append as advisory.

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
work-intent log accretes completed claim/release pairs over
time, drowning the live signal: a reader scanning the log
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
> * **Prune-intents** — completed claim/release pairs are
>   compacted out of the log past a grace window; the active
>   set holds only intents whose work is still in flight.
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

### Extension — Per-session identity for the claim/release log

A team that runs **multiple concurrent sessions of the same
agent tool** cannot identify intent-holders by tool or by
agent-type: every session resolves to one identity, so one
session's auto-release closes another's claims, and the
pre-edit read cannot tell a sibling session's claim from its
own. The fix — doctrine in
`cairn/doctrine/coordination.md`
> "Coordination identity — per-session, not per-agent" — is to
derive a **per-session** identity from the harness's
session-scoped identifier.

Merged into the coordination section:

> **Per-session coordination identity (concurrent same-tool
> teams).** When the team's work-intent / event log records who
> holds a path, the holder identity is **per-session**, derived
> from the harness's session ID, not a static per-tool name:
>
> * Resolve identity from the harness session ID present in the
>   session's shell environment; both the pre-edit claim and the
>   commit-time auto-release run in that session and resolve the
>   same value, while sibling sessions resolve different values.
> * **Hash the whole session ID, never a prefix** — time-ordered
>   IDs (UUIDv7) share leading bytes across near-simultaneous
>   sessions, exactly the ones the identity must separate.
> * A static, machine-global identity override is an **escape
>   hatch, not a setting** — keep it as the top-priority tier for
>   tests / one-offs, but a global export collapses sessions to
>   one identity; warn when it shadows an available session ID.
> * **Auto-release on commit** closes only the committing
>   session's own claims (`identity == this session AND paths
>   intersect`); identity-resolution failure fails soft.
>
> Each adopter supplies its own harnesses' session-ID env-var
> names; the structural rule is doctrine, the var names are
> adopter-local.

This extension presupposes the log-form substrate (the
claim/release lifecycle and the auto-close hook need a release
event to write); a team still on the per-file form adopts it
when it moves to the log.
