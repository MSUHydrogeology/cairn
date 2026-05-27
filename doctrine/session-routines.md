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
   multi-agent threads; surface them.
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
handoff time. Committing and pushing are never implied by running
the routine; they wait on explicit Maintainer approval.

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
