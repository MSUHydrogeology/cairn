External-repo paths: `docs/methodology/doc-governance.md`
# dev/ — the development coordination space
Written in [Cairn Plain Language 1.0](agent_collaboration.md).

`dev/` is {{project_name}}'s **deliberation layer**: where the
project's direction is argued, decided, and recorded. It is not a
scratch directory — every file here is durable coordination state,
and a cold-starting agent should be able to reconstruct *what the
project is doing, and why* from this tree alone.

## The tree

| Path | What it holds |
|------|---------------|
| `README.md` (this file) | The entry point to `dev/`. |
| `agent_collaboration.md` | The role roster, the review loop, and the coordination doctrine. |
| `PLANNING.md` | The roadmap board — queued and active work (a current-state index; completed work migrates out to archived plans, not a "completed" section). |
| `proposals/` | One file per substantive change; operative text revises in place and reviews/responses append. |
| `proposals/_template.md` | The proposal structure and the full lifecycle doctrine. |
| `proposals/archive/` | Closed proposals — read for rationale; do not edit. |
| `plans/` | Execution plans for non-trivial accepted standard/heavy proposals; light has no plan. |
| `plans/_template.md` | The plan structure and the plan-archive doctrine. |
| `plans/archive/` | Closed plans — read for what shipped and why. |
| `modules/` | Dimension-selected add-ons — one file per installed module (see `modules/<name>.md` for each). Read each module's `Adds to:` line to find where its content merges into the kernel. |
| `upstream/` | Draft issue reports for external OSS dependencies — bugs and capability gaps to file upstream. See `upstream/README.md`. Distinct from the methodology fold-back channel (an issue on Cairn's tracker). |
| `rules/` | Project-owned agent-discipline detail routed from `RULES.md`. The folder ships from Cairn; the rule files inside are entirely the adopter's own. Empty at adoption. |
| `strategy/` | Stage-0 exploration notes — comparative research, tool analysis, product strategy — written before a commitment is ready to propose. See `strategy/README.md`. |

The project's **vision** / charter belongs in the descriptive
layer rather than the deliberation tree — see Cairn's published
doc-governance method > "Common homes for project vision / charter
material" for the choices. The reference points to Cairn's published
methodology, not a file in the adopter's tree.

## How this relates to other docs

<!-- cairn:slot cross-layer-doc-pointers -->
*(Empty at adoption — wire the project's cross-layer pointers here: links
from this `dev/` entry point to the repo's documentation map, test plan,
vision, or descriptive-layer references a cold-starting agent or contributor
should reach in one hop. Replace this placeholder when filling.)*
<!-- cairn:end cross-layer-doc-pointers -->

## How to use it

* **Read it on entry.** The session-start orientation pass (see
  `AGENTS.md`) begins here.
* **Coordinate through it, not around it.** Agents coordinate by
  reading and updating these artifacts, not by exchanging messages.
  Nothing load-bearing lives only in a
  conversation; if it matters, it is written here and committed.
* **Put a file in the right place.** A deliberation goes in
  `proposals/`; an execution plan in `plans/`; roadmap status in
  `PLANNING.md`. The `dev/` tree is about the project's
  *becoming* — aspiration, decisions in progress, the method of
  deciding — not about the software as it exists today (that is
  the descriptive `docs/` layer).
