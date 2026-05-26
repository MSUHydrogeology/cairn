# Module: doc-drift-prevention

**Selected when:** the project ships documentation that *describes code*
(a config reference, API docs, inline examples) and wants it to stay true
as the code changes. Broadly applicable; team-gated so a preset
(`governance presets`, P4) turns it on for the profiles that warrant it.
**Adds to:** a drift-prevention note in the adopting repo's docs guide
(and a cross-reference from `dev/agent_collaboration.md`).

Documentation that restates what the code does will drift the moment the
code moves -- and stale docs are worse than none, because a reader
trusts them. Cairn requires a change to **absorb its docs**, but
hand-written docs that *duplicate* a source of truth defeat that:
the doc and the source diverge silently. This module names the
**authoring-time gates** that make drift a build failure instead of a
latent surprise.

Cairn **embodies** this discipline -- its own `check_cairn` self-check
runs over its tree, and Cairn's reference content is kept in lockstep with
its source -- and **points** at the reproducibility craft
([`docs/further-reading.md`](../../../docs/further-reading.md), the
Turing Way entry); it does **not** teach documentation writing.

## Template content

Merged into the project's docs guide:

> **One source of truth, generated outward.** A reference doc that
> mirrors a machine-readable source (a config schema, a type definition)
> is **generated** from that source, never hand-edited. The generator is
> re-run on change; the generated file is checked in but marked
> "do not edit by hand."
>
> **Inline examples are pulled from runnable sources.** A documentation
> snippet that shows real input is **extracted** from a runnable example
> (the example is the authority), not retyped into the prose -- so a
> snippet cannot fall out of step with the thing it illustrates.
>
> **A drift gate fails the build.** A check in CI compares each generated
> doc / synced snippet against its current source and **fails** when they
> diverge, so drift is caught at authoring time, not by a confused reader
> months later. A link- and claim-integrity check (every internal link
> resolves; every cited path / line exists) runs in the same gate.
>
> **The gate catches drift, not absence.** A drift gate confirms existing
> docs match their source; it does not know a *new* capability went
> undocumented. The "absorb docs into the change" lifecycle step covers
> that -- the gate and the discipline are complementary.

## Doctrine, not (yet) tools

This module ships the **discipline**; an adopter wires their own stack's
equivalents (schema-doc generators, snippet-sync, a link checker). A
*generic, scaffold-installed* drift-tooling set -- the way the
`claim-check` and `lifecycle-metrics` modules ship runnable scripts -- is
a **named future Cairn enhancement**, not part of this module. Until
then, the module is "here is the gate to build," and
[`scripts/check_cairn.py`](../../../scripts/check_cairn.py) is the worked
example of the link/claim half running on Cairn's own tree.

## Learn it deeply

See [`docs/further-reading.md`](../../../docs/further-reading.md) >
"Reproducible, ethical, collaborative practice" for the reproducibility
craft Cairn points at rather than re-teaching.
