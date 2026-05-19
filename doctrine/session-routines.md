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
  the docs and changelog, runs the test suite, writes the next
  session's starting plan, and lands the handoff commit.

The full scrub happens once per session-day, by one owner — that
keeps the shared communication files a single-writer surface at
handoff time. Committing and pushing are never implied by running
the routine; they wait on explicit Maintainer approval.

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
