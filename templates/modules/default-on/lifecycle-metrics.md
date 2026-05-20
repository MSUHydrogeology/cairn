# Module: lifecycle-metrics

**Selected when:** default-on — kept by every adoption except the
smallest, where the proposal corpus is too thin to measure.
**Adds to:** a short note in `dev/agent_collaboration.md`
documenting the lifecycle-metrics discipline. The actual extractor
tool is the adopter's to supply (see "Reference implementation"
below).

The lifecycle-metrics layer makes the team's discipline
**measurable** rather than asserted. A small read-only extractor
walks `dev/proposals/` and `dev/plans/` and emits per-proposal
metrics — review rounds, revision counts, time-to-decision,
finding severities — so a claim like "External review catches what
the author cannot" becomes a quantity, not a belief.

## Template content

Merged into `dev/agent_collaboration.md`:

> **Lifecycle metrics.** The extractor `{{metrics_command}}` walks
> the proposal / plan corpus and emits per-proposal lifecycle
> metrics. Run it to read the team's own discipline; the output is
> derived and uncommitted.

The `{{metrics_command}}` token is filled from the adopter's
profile YAML with whatever invocation runs their extractor (e.g.
`python tools/lifecycle_metrics.py`).

The emitted metrics file is a **derived** artifact — regenerable
from the repository at any commit — and is therefore deliberately
not committed; a dated, citable snapshot is a project's own later
choice.

A measured baseline is the gating artifact for any claim the
project makes about its own method — run the extractor before
asserting one.

## Reference implementation

Cairn ships the discipline (this module, the `{{metrics_command}}`
token, the `dev/agent_collaboration.md` note) but does **not** yet
ship a generic extractor script. The methodology's reference
implementation lives at
[`modflow_tools/tools/lifecycle_metrics.py`](https://gitlab.msu.edu/hydrogeology/code-projects/modflow_tools)
— a read-only walker over `dev/proposals/{,archive/}` and
`dev/plans/{,archive/}` that emits a per-proposal / per-plan CSV
with review rounds, revision counts, time-to-decision, and
finding severities.

Adopters have two paths:

* **Copy and adapt the reference**: clone the file from the
  modflow_tools repo into the target project's `tools/` (or
  `scripts/`, etc.) and point `{{metrics_command}}` at it. The
  reference parses Markdown headers and timestamps; the
  conventions it recognises are the lifecycle templates Cairn
  ships, so it should run cleanly against a freshly bootstrapped
  Cairn repo — but project-specific extensions to the proposal /
  plan headers may need parser tweaks.
* **Write your own**: the schema is open; what matters is that
  the team can answer questions like "how often does the External
  round catch something the Internal round did not" from data
  rather than from belief.

A generalized, in-tree reference script that the scaffold installs
to a target's `tools/` directory is queued as a future Cairn
enhancement; see Cairn's own roadmap for the follow-up.
