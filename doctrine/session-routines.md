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
4. **Confirm role and starting point** (`roles.md`) before
   committing to substantive work.

The failure mode this prevents is expensive and specific: the
session's first load-bearing assertion, built on a stale mental
model. A compaction summary is lossy by design — re-anchoring on
the durable artifacts is cheaper than rediscovering them through a
wrong assertion.

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
full-handoff owner lands it without per-commit Maintainer approval
(covered by the deliberation-commit carve-in in
`templates/core/AGENTS.md` > *Git and commit workflow*; path-scoped,
listing the routine artifacts). **Pushing always waits on explicit
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

## The reflections channel

Each agent, at goodnight, writes a short **reflection** — what it
shipped, what went well, what went wrong and the lesson, what
threads remain open — to a per-agent file in an untracked
reflections directory. The channel is:

* **per-agent** — each agent writes its own; no agent writes or
  edits another's;
* **ephemeral** — reflections are untracked and periodically
  pruned; durable observations migrate out into doctrine or the
  roadmap;
* **a cross-agent handoff surface** — the full-handoff owner reads
  the session-day's reflections to understand every agent's
  experience before writing the next plan.

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
coordinate leaks before any item becomes a public Cairn proposal. The
mechanism is specified in `doctrine/fold-back.md`; this step is the
capture cadence that feeds it.

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

The trackers feed the rate-limit gate; the
[`lifecycle-metrics`](../templates/modules/default-on/lifecycle-metrics.md)
module's eventual cross-adopter harvest correlates across them.
The trackers' canonical 7-column semantic-field schema is the
contract that harvest reads against; adopters with existing
trackers may ship a per-tracker `tracker_schema.yml` mapping the
adopter's columns onto the canonical fields.

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
