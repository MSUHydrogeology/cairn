# Module: lifecycle-metrics

**Selected when:** default-on — kept by every adoption except the
smallest, where the proposal corpus is too thin to measure.
**Adds to:** a `tools/`-level script, plus a short note in
`dev/agent_collaboration.md`.

The lifecycle-metrics layer makes the team's discipline
**measurable** rather than asserted. A small read-only extractor
walks `dev/proposals/` and `dev/plans/` and emits per-proposal
metrics — review rounds, revision counts, time-to-decision,
finding severities — so a claim like "External review catches what
the author cannot" becomes a quantity, not a belief.

## Template content

The module ships the extractor as a `tools/`-level script,
generalized from the methodology's reference instance. The emitted
metrics file is a **derived** artifact — regenerable from the
repository at any commit — and is therefore deliberately not
committed; a dated, citable snapshot is a project's own later
choice.

The note merged into `dev/agent_collaboration.md`:

> **Lifecycle metrics.** The extractor `{{metrics_command}}` walks
> the proposal / plan corpus and emits per-proposal lifecycle
> metrics. Run it to read the team's own discipline; the output is
> derived and uncommitted.

A measured baseline is the gating artifact for any claim the
project makes about its own method — run the extractor before
asserting one.
