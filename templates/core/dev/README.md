# dev/ — the development coordination space

`dev/` is {{project_name}}'s **deliberation layer**: where the
project's direction is argued, decided, and recorded. It is not a
scratch directory — every file here is durable coordination state,
and a cold-starting agent should be able to reconstruct *what the
project is doing, and why* from this tree alone.

## The tree

| Path | What it holds |
|------|---------------|
| `README.md` (this file) | The entry point to `dev/`. |
| `collaboration_agreement.md` | The working norms, the review compact, and decision rights. |
| `agent_collaboration.md` | The role roster, the review loop, and the coordination doctrine. |
| `PLANNING.md` | The roadmap board — queued, active, and recently completed work. |
| `NEXT_SESSION.md` | The cold-pickup handoff — what to start next, with enough context to begin. |
| `proposals/` | The deliberation record — one file per substantive change, append-only. |
| `proposals/_template.md` | The proposal structure and the full lifecycle doctrine. |
| `proposals/archive/` | Closed proposals — read for rationale; do not edit. |
| `plans/` | Execution plans for non-trivial accepted proposals. |
| `plans/_template.md` | The plan structure and the plan-archive doctrine. |
| `plans/archive/` | Closed plans — read for what shipped and why. |
| `modules/` | Dimension-selected add-ons — one file per installed module (see `modules/<name>.md` for each). Read each module's `Adds to:` line to find where its content merges into the kernel. |

A `vision.md` (the project's north star), a `strategy/` directory
(longer-horizon research notes), and an `upstream_issues/`
directory (external-project issue drafts) are added when the
project needs them — they are not part of the invariant core.

## How to use it

* **Read it on entry.** The session-start orientation pass (see
  `AGENTS.md`) begins here.
* **Coordinate through it, not around it.** Agents coordinate
  *stigmergically* — by reading and updating these artifacts, not
  by message-passing. Nothing load-bearing lives only in a
  conversation; if it matters, it is written here and committed.
* **Put a file in the right place.** A deliberation goes in
  `proposals/`; an execution plan in `plans/`; roadmap status in
  `PLANNING.md`. The `dev/` tree is about the project's
  *becoming* — aspiration, decisions in progress, the method of
  deciding — not about the software as it exists today (that is
  the descriptive `docs/` layer).
