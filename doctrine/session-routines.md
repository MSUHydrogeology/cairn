<!-- ^ Illustrative / legacy-location adopter-tree paths cited in the routines doctrine; created on first use or superseded by dev/measurement/ homes. -->

# Session routines

A unit of work in Cairn is a **session** — one agent, one stretch
of context. Sessions end; context is lost or compacted; a
different agent, or the same agent later, picks the work up. Two
routines bracket a session so the handoff is clean: a
**session-start** orientation and a **goodnight** routine. They are
part of the invariant kernel — every adoption runs them — because
the methodology's whole premise is that work survives handoff, and
handoff is exactly where it is most fragile.

## Session start — orient before asserting

Run a short orientation pass at the moments where conversational
memory and the repository's actual state fall out of sync:

* a true cold start — a new working day, or picking up after time
  away;
* **after a context-loss event** — in a harness that compacts long
  sessions, right after compaction, when substantive prior work
  happened in the dropped window;
* when the user asks to "get oriented" or "catch up".

The pass has four moves:

1. **Re-anchor on shared context.** Skim the governing doctrine
   and the deliberation record — the `dev/` tree, the roadmap
   boards, the process doctrine.
2. **Catch up on what landed.** Read the commit log back to the
   last handoff; note commits from other contributors.
3. **Note in-flight threads.** Open proposals and plans are live
   multi-agent threads; surface them. *If the `coordination-tiers`
   module is installed*, also **read the active work-intent set**
   (`python tools/intent.py list`) and confirm the hooks are present
   (`python tools/intent.py hooks-status`): a starting session sees who holds
   which paths before its first edit. This is the *read* half of the
   work-intent convention — the complement to claiming before you edit
   (`coordination-tiers`); skipping it is how a session collides with an
   active claim it never saw.

   *If the lifecycle checker/planner is installed*
   (`tools/board.py`, the read-only arm of
   [`lifecycle-contract.md`](lifecycle-contract.md)), start from the
   **board** rather than from the artifacts:

   ```
   python tools/board.py
   ```

   One row per active artifact — kind, artifact, status, owner role,
   active work-intent, review obligation, evidence, what blocks it, and
   whether the row is still valid — under a header naming the `HEAD` the
   view was derived from and whether the lifecycle files differ from it.
   **Run the board, choose the row you need, then read that artifact and
   the evidence it cites** — not every active record. That ordering is the
   point of the view: it replaces "open everything under `dev/` and
   reconstruct the state" with one derived summary and one targeted read.

   The board is *derived*, and its own footer says so — the artifact is
   authoritative, and a row that looks wrong is a reason to open the
   artifact, not to trust the row. It is an **optional orientation aid**:
   it reports header fields, attests nothing about authenticity, and
   **mutates nothing** — never a mandate to act. The structural scan and
   the per-artifact transition report that once sat beside it were retired
   with the lifecycle planner; what they enforced now lives in review.
4. **Confirm role and starting point** (`roles.md`) before
   committing to substantive work.

The failure mode this prevents is expensive and specific: the
session's first load-bearing assertion, built on a stale mental
model. A compaction summary is lossy by design — re-anchoring on
the durable artifacts is cheaper than rediscovering them through a
wrong assertion.

The mirror failure mode is treating orientation as a mandate to
*act*: session start is orientation, not execution. Surface the
candidate next steps, name your role, and **await the operator's
direction** — which may already be in their opening message —
before beginning substantive work (implementing, editing, staging,
or committing). The only write the routine itself makes is the
tool's idempotent skills self-heal, not the agent's.

## Goodnight — leave a clean handoff

At the end of a working session, or before a planned context
handoff, run the goodnight routine so the next session starts on
solid ground. Treat the codebase as shared territory: do not sweep
up another contributor's work-in-progress, do not speak for them,
do not silently resolve threads they hold.

The routine has **two modes**, and no agent infers which applies
from "my session is ending":

* **Reflection-only participant** — every agent ending substantive
  work surveys the session, posts a status summary, writes its own
  reflection (below), notes open threads, and **stops**.
* **Designated full-handoff owner** — exactly one agent, named by
  the Maintainer, additionally scrubs the roadmap boards, verifies
  the docs and changelog, runs the test suite, **rewrites the
  next session's starting plan from scratch** (see below), and
  lands the handoff commit.

The full scrub happens once per session-day, by one owner — that
keeps the shared communication files a single-writer surface at
handoff time. **The handoff commit is part of the routine** — the
full-handoff owner lands it without Maintainer approval — there is no
per-commit approval gate to clear (`templates/core/AGENTS.md` >
*Git and commit workflow*), and the handoff is a routine step rather
than a deviation. It is still **path-scoped**, listing the routine
artifacts, because the git index is shared. **Pushing always waits on explicit
Maintainer approval** — the commit makes the handoff durable for the
next session; the push is the Maintainer's call on cadence.

### The staleness sweep — keep the roadmap honest

Part of the full-handoff owner's roadmap scrub is a **staleness
sweep**: flag board items that have aged out by their date-markers.
The reference windows are **adopter-tunable defaults, not hard
constants** — `queued` / `deferred` items older than ~2 months, and
`active` / `blocked` items with no update for ~1 month. For each
flagged item, do one of four things: **reaffirm** it (refresh its
date-marker), **reframe** it, **defer** it with explicit revival
conditions, or **remove** it (clearing the removal preconditions
first). When in doubt, surface it to the Maintainer rather than
scrubbing silently.

Two things make the sweep cheap and honest. First, the **date-marker
convention** on board items (`doctrine/lifecycle.md` and the roadmap
template) lets the owner perform the sweep by *reading the file*
rather than running `git blame` or trusting memory. Second, **sweep
any cross-cutting follow-up backlogs every session-day**, not only at
the staleness windows: their items go stale fastest, because the
parent decision has already shipped and the ship-time context fades
the longer they sit unrevisited.

### The next-session starting plan: written from scratch each goodnight

The handoff document is **a single-session product, not an
accretion across sessions**. Each goodnight the full-handoff
owner *rewrites* it — the physical action is "open a blank file
and write," not "edit the existing file." Anything in the
previous goodnight's version that does not earn its place in the
next session's orientation is dropped.

This rule prevents a structural failure mode: a handoff document
that accretes context across sessions gradually drifts from
current truth. After several sessions it holds pointers to work
that has shipped, instructions premised on assumptions that have
moved, decisions that were taken and reversed, threads that
closed. A reader cannot tell which claims are still live and
which have aged out; the reader trusts the document, acts on a
stale assertion, and the session begins on a wrong premise.
Append-by-default is the path of least resistance for every
individual session writer while the cost of staleness is paid by
future readers — a tragedy-of-the-commons shape that
rewrite-from-scratch breaks structurally.

**Durable-claim migration is upstream of the rewrite.** Before
writing the new handoff, the owner asks "what here should
outlive this single handoff?" and moves durable claims to their
proper home — doctrine, the roadmap, a proposal. The handoff
document is then free to be one-session-shaped. The rewrite
discipline is what *forces* migration to happen on the right
cadence: anything kept for the next session is acknowledged as
still-relevant; anything dropped has either landed in a durable
surface or earned its drop.

The rule applies only to the next-session handoff document.
Per-agent reflections have their own ephemeral-and-pruned
rhythm (below); they are not rewritten from scratch.

### The shape of a next-session entry

Rewrite-from-scratch keeps the handoff *current*; this names what a
recommended-next-task entry should *contain* so a cold reader can act
without the prior session's conversation. Five elements — make them
structural, not discretionary:

1. **Task + current state.** What the next task is, and the state it
   resumes from: what just landed, what is blocked (and on what), what
   a prior step just *un*blocked. The reader should not have to
   reconstruct "where are we" from the commit log.
2. **Roles to instantiate.** Draw from the project's role roster —
   and name the roles explicitly *not* needed for this task, with the
   reason. "No code touched" is **not** the same as "no domain
   involvement": a domain agent is a doctrine stakeholder on a
   doc-only change that touches its surface, and a role left silent by
   omission reads as an oversight rather than a decision.
3. **Agent-dispatch tier.** Whether the next step wants a same-agent-type
   read or a cross-agent-type one — aligned with any review tier the
   task carries (a declared-External **proposal** review wants a
   cross-type dispatch; a plan review is always Internal, same-type
   fresh-session).
4. **Reading order.** The two or three artifacts to read first, in
   order, *after* the session-start re-anchor — the durable surfaces
   that carry the load-bearing context, not an exhaustive list.
5. **First three concrete steps.** The literal opening moves
   (commands, files to open, the first commit's shape) so the next
   session converts orientation into action without a planning gap.

These compose with the rewrite discipline: each goodnight the entry is
rewritten, and the rewrite fills these five slots for the new
recommended task.

## Invoking the routines — the lifecycle skills

The routines above are also **invokable skills**, installed at scaffold time as
the agentskills.io `SKILL.md` pair under `.agents/skills/` (`session-start` and
`session-end`, invoked as `/session-start` / `/session-end`), backed by a
deterministic CLI
(`tools/session.py`). The skill bodies orchestrate the *mechanizable* steps
(gather git state, scaffold the reflection, prune, surface intents); this
doctrine stays the single source of *what* each routine is and *why*, and the
*judgment* steps remain the agent's.

Two invariants are load-bearing and structural, not stylistic:

* **Manual-only.** A routine fires only on an explicit operator request, never
  from conversational chatter — "goodnight, talk tomorrow" must not scrub a
  roadmap. The skill carries a best-effort suppress flag, but the **portable**
  guarantee is the CLI's reflection-only default: `session-end` does only
  non-destructive work unless an explicit `--handoff` is given.
* **Single-owner full handoff.** The destructive full handoff runs only behind
  `--handoff` **plus** a maintainer-designation marker **and** a fail-closed
  concurrent-handoff lock, so the "once per session-day, by one owner" rule
  above is enforced mechanically, not merely remembered: a second concurrent
  handoff fails closed rather than producing a double scrub. The marker is an
  **anti-accidental-run gate, not an authorization control** (it is trivially
  self-set); it stops an *unbidden* run, not a malicious local actor.

### Project-owned routine customization — `custom_session_routines.md`

The skills + `tools/session.py` carry the *universal* routine — the
invocation, the mechanizable gather/scaffold/prune, and the judgment steps every
adopter runs. The *tail* — a project's **concrete** steps (which doc-build
command, which test environment, the changelog cadence, a foldback-capture
protocol) — is **project-owned**, and lives in a single adopter file:

```
dev/rules/custom_session_routines.md
```

with two headed sections, `## Session start` and `## Goodnight`. The two shipped
skills carry a **generic pointer** to it — an identical string for every adopter,
so it ships from Cairn cleanly while the file's *contents* stay the adopter's.
The file is **Cairn-never-templated**, exactly like `RULES.md`: Cairn ships the
pointer, never the content; an adopter creates and fills it (or doesn't).

This is what lets an adopter **slim its always-loaded `AGENTS.md` routine
section** to a pointer rather than carrying the full procedure in every-session
context (the token-efficiency payoff — procedures load on-demand, not always-on).
It also resolves a contract gap: the shipped skills can point at a real,
installable, project-owned convention file instead of this Cairn-internal
doctrine (which is **not** in the adopter install set, so a direct reference to
it dangles in every adopter).

Three rules make the convention safe:

* **No bare pointer.** When an adopter slims its `AGENTS.md` routine section, it
  **MUST** retain a one-line inline routine summary *beside* the pointer — never
  a bare link. Routines are agent-followed, not mechanically enforced; a bare
  pointer is too easy to skip, which would silently drop the adopter's steps. The
  one-line summary keeps the routine legible in always-loaded context even if the
  pointer is missed.
* **Absent file or section = no custom steps.** If `custom_session_routines.md`
  is absent, *or* present but missing the section for the routine being run, the
  agent treats it as "no project-specific steps" — the same graceful no-op. The
  generic pointer reads "if present" precisely so an adopter that never creates
  the file loses nothing.
* **One file, two sections — with a documented fallback.** A single file with
  two headed sections is the default (one project-owned surface, parallel to
  `RULES.md`; the headers disambiguate start- vs end-specific steps). A project
  whose start/end routines diverge enough to warrant it MAY instead split into
  `dev/rules/custom_session_start.md` / `dev/rules/custom_session_end.md`; the
  single-file form is the recommended starting point.

## The reflections channel

Each agent, at goodnight, writes a short **reflection** — what it
shipped, what went well, what went wrong and the lesson, what
threads remain open — to a per-session file in an untracked
reflections directory. The channel is:

* **per-agent, per-session** — each agent writes its own, and each
  *session* writes a **distinct** file (`<date>-<agent>-<session>.md`)
  so concurrent same-agent sessions never share a path and cannot
  clobber one another. `<session>` is the harness session id where the
  tool exposes one, else a short **random** token fixed at session start
  (≥4 hex chars from random bytes, or a hash of the session id) — **never
  a minute-resolution timestamp**, which re-collides under concurrent
  start. No agent writes or edits another's;
* **ephemeral** — reflections are untracked and periodically
  pruned; durable observations migrate out into doctrine or the
  roadmap;
* **a cross-agent handoff surface** — the full-handoff owner reads
  the session-day's reflections — glob `dev/reflections/<date>-*.md`,
  which gathers *every* session, not just the last writer's — to
  understand every agent's experience before writing the next plan.

A reflection is a retrospective, not a deliberation surface: a
point that belongs in a proposal does not live in a reflection.

### Goodnight-time synthesis — one stub, not one per incident

The full-handoff owner reads the session-day's reflections not only
to write the next plan but to **synthesize** the period's recurring
signal. When several reflections or incidents point at the same
failure shape, the owner aggregates them into a *single*
doctrine-proposal stub — not one proposal per incident. This
synthesis is one of the two triggers the doctrine-evolution gate
permits (`rationale.md` > "How the doctrine evolves under
evidence"): it is the routine boundary at which observed failure is
allowed to become a doctrine change, on a cadence the team can
absorb. A single incident does not earn a doctrine change here
unless the Maintainer has classified it high-risk.

### Goodnight foldback-capture — when the fold-back-ledger module is installed

A deployment running the **fold-back-ledger** module adds one more
standing goodnight step for the full-handoff owner: scan the
session-day's doctrine activity for **Cairn-portable** candidates —
generalizable improvements that should fold *up* into Cairn — and
capture each in the deployment's fold-back ledger. Capture never lapses;
an **empty capture is success** (do not manufacture marginal
candidates). Whether to *open a sync* upstream is the separate,
judgment-gated decision the framework's harvest cadence governs. The
ledger is a cross-repository export surface, so candidates carry no
secrets, credentials, internal hostnames/IPs, local paths, or
proprietary domain detail, and the Maintainer confirms no private
coordinate leaks before any item becomes a public Cairn proposal. A
candidate is filed as an issue upstream rather than staged in a local
ledger; this step is the capture cadence that feeds it.

### Goodnight RULES.md maintenance — when the project keeps a RULES.md

A deployment that keeps a project-owned **`RULES.md`** (the
project-local rules file Cairn never templates — see
[`doctrine/doc-governance.md`](doc-governance.md) > "Project-owned rules")
adds one standing goodnight step for the full-handoff owner: scan the
session-day's work for **`RULES.md` drift**, in both directions.

* **Promote in.** Did a new project *bright-line rule* surface — one that
  must apply on every turn (an environment requirement, a naming/domain
  convention, a safety rail, a commit constraint) and is **project-owned,
  not Cairn doctrine**? If so, add a concise statement to `RULES.md` (and
  route its detail to an on-demand doc). The trigger is "an agent would
  get this wrong without it being always-on," not "it was mentioned."
* **Demote out.** Has `RULES.md` *bloated* past a small router — accreting
  bulk, tables, logs, or a rule that is really on-demand reference? Move
  that content to an on-demand `docs/` / `dev/` file and leave a pointer.
  `RULES.md` is a **router, not a doctrine dump**; a dated instance log or
  a long rationale tail belongs in a doc, never in every-call context.
* **Route, don't duplicate.** A rule lives in exactly one tier (slot /
  `RULES.md` / docs — the one-home table in `doc-governance.md`); the scan
  also catches a rule that drifted into two places.

Capture never lapses but an **empty scan is success** — most goodnights
add nothing. A genuinely *general* (non-project) rule that surfaces here
is a fold-back candidate (the step above), not a `RULES.md` addition.

### Goodnight onboarding-trigger evaluation — when progressive onboarding is installed

A deployment scaffolded from any of the three named profile presets
(or one that has opted in via `python scripts/onboarding_activate.py
--seed`) adds one more standing goodnight step for the full-handoff
owner, paired with the foldback-capture step above: **run the
progressive-onboarding activation helper**.

```bash
python scripts/onboarding_activate.py        # default: scan + activate
python scripts/onboarding_activate.py --dry-run   # show plan, no writes
```

The helper scans the deployment for fired triggers (maturity-ladder
transitions + action signals — the trigger matrix is enumerated in
[`doctrine/onboarding.md`](onboarding.md)), activates the corresponding
deferred onboarding tasks into `dev/PLANNING.md`'s `onboarding-tasks`
slot, emits at most one active-surfacing prompt per goodnight (the UX
caps [`onboarding.md`](onboarding.md) specifies), and appends one line
per activation to the tracked log at
`dev/.cairn/onboarding-activated.jsonl`. The run
is **idempotent**: re-running on unchanged deployment state is a
no-op, so a goodnight owner who fired the helper earlier in the day
loses nothing by firing it again at handoff.

A future `cairn-update` mini-command may fold this invocation into a
single goodnight wrapper; until then, the helper runs as its own
explicit step paired with foldback-capture. The progressive-onboarding
doctrine carries the full mechanism (trigger matrix + active-surfacing
shape + UX caps + state-file schema); this section names only the
when (goodnight) and the who (full-handoff owner).

### Goodnight incident-tracker migration — when the incident-trackers module is installed

A deployment running the **incident-trackers** module adds one more
standing goodnight step for the full-handoff owner: read the day's
reflections for incidents matching an event class defined in a
tracker the deployment maintains
(`dev/incident_log.md`, `dev/coordination_log.md`, etc. — per the
deployment's `incident-trackers` module instantiation), and migrate
a one-line dated entry to the matching tracker table.

The migrated entry MUST populate the `Impact` column
(`occurred` / `prevented` / `non-conflict`) and SHOULD populate
`Resolved By` if the resolution is already known; an unresolved
`occurred` entry uses `pending` in `Resolved By`, which is the
signal the [adaptive-doctrine rate-limit gate](rationale.md) looks
for when it bites on accumulated unresolved recurrences.
**Prevented incidents** (caught before propagating) and
**non-conflicts** (looked like the failure mode but structurally
weren't) are logged for base-rate visibility but do NOT count
against the rate-limit gate's trigger — only `Impact = occurred`
rows count.

The trackers feed the rate-limit gate. Their canonical 7-column
semantic-field schema is the contract any cross-adopter harvest
reads against; adopters with existing trackers may ship a
per-tracker `tracker_schema.yml` mapping the adopter's columns onto
the canonical fields. The module that was to perform that harvest
was retired in August 2026 — the schema outlives it and binds a
successor, so it is stated here as a standing contract rather than
as one tool's input format.

### Adoption drift surfacing — when the upgrade tooling is installed

The adoption→canonical checkpoint of loop-fidelity (see `lifecycle.md` >
"Loop-fidelity verification") is surfaced, not enforced: `upgrade --plan`
reports a one-line **adoption-drift** message — how far the adopter's installed
Cairn ref is behind canonical (the `cairn-lock.yml` commit vs the source HEAD).
A session-start or goodnight pass that runs `upgrade --plan` therefore sees, at
a glance, whether the per-change fold-back loop is closed *continuously* rather
than only on the periodic harvest cadence. It is **informational and
fail-open** — it surfaces drift, never blocks work, and **degrades gracefully**:
when the git metadata is missing or the Cairn source is a packaged release (no
git), it prints an explicit "unavailable" line rather than failing. Acting on
the drift (running the upgrade) stays a deliberate, separately-approved step.

## Adaptation

The routines are invariant, but their *weight* tracks the team. A
solo, single-agent project still runs both — orientation after
context loss and a goodnight handoff matter even with one agent —
but the two-mode goodnight collapses (the sole agent is always the
full-handoff owner), and the **reflections channel** is a
default-on module a solo project may keep as a personal log or
omit entirely (the cross-agent handoff function the channel exists
for only earns its keep with a multi-agent team). A multi-agent
team runs the full two-mode routine. The harness-specific details
— what counts as a "context-loss event", where an agent's scratch
area lives — are filled in by the bootstrap from the adopting
team's agent tools.
