<!-- cairn-internal-ref-allow: doctrine/coordination.md doctrine/session-routines.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
# Next-session candidates — Cairn

`NEXT_SESSION.md` carries the **cold-pickup handoff**: the
recommended next task and a queue of candidates, each with enough
context — file paths, scope, effort, payoff, risks — to begin
without the prior session's conversation.

It complements `PLANNING.md`: `PLANNING.md` says *what* is queued;
`NEXT_SESSION.md` says *how to actually pick it up*.

`NEXT_SESSION.md` is **rewritten from scratch** by the full-
handoff owner at each goodnight — the physical action is "open
a blank file and write," not "edit the previous version."
Anything in the previous goodnight's version that does not
earn its place in the next session's orientation is dropped;
durable claims migrate to their proper home (doctrine, the
roadmap, a proposal) **before** the rewrite. See
`doctrine/session-routines.md` > "The next-session starting
plan: written from scratch each goodnight" for the load-bearing
reasoning.

The required-signal-read discipline on shared communication
files applies (`doctrine/coordination.md` > "Required
signal+read for coordination-surface files").

## Recommended starting point

<!-- cairn:slot next-start -->
**Task + current state.** Cairn self-adopted on 2026-06-12: the `dev/`
tree, `AGENTS.md`, and the 14-module roster are installed and the merge /
template / orientation slots are filled. Two things remain to *finish*
adoption, then the real work begins: (a) the `project-overview` and
`project-conventions` slots in `AGENTS.md` are being filled through the
first dogfood proposal; (b) the R-F acceptance gate (BOOTSTRAP II-5)
runs once those land. After that, begin the **strategy + roadmap** pass
the Maintainer asked for.

**Roles to instantiate.** Strategy (to frame the roadmap and the
tighten-up); the Human Maintainer for Decisions. *Not* needed: a Legacy
Agent (greenfield), domain agents (no scientific-domain partition), a
multi-language tester (single-language).

**Agent-dispatch tier.** High for the strategy framing and any
doctrine-touching proposal; medium for mechanical slot / doc work.

**Reading order.** `AGENTS.md` → `dev/README.md` → this file →
`dev/PLANNING.md` (Where the project stands) → `README.md` →
`doctrine/` as a specific proposal requires.

**First three concrete steps.** (1) Finish the dogfood proposal filling
`AGENTS.md`'s `project-overview` + `project-conventions`, review it,
record the Decision. (2) Run the R-F gate (`pytest bootstrap/tests`,
`scripts/check_cairn.py`, `scripts/quality_gate.py`) and clear findings.
(3) Open a `dev/strategy/` note scoping the broad look + the forward
roadmap.
<!-- cairn:end next-start -->

## Other candidates

Smaller, pickable-cold tasks, each with the context to start it.

*(Empty at adoption.)*
