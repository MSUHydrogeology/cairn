# Module: doc-drift-prevention

**Selected when:** the project ships documentation that *describes code*
(a config reference, API docs, inline examples) and wants it to stay true
as the code changes. Broadly applicable; team-gated so a preset
(`governance presets`, P4) turns it on for the profiles that warrant it.
**Adds to:** a drift-prevention note in the adopting repo's docs guide
(and a cross-reference from `dev/agent_collaboration.md`), **plus two
runnable, stdlib-only scripts** the scaffold installs into the target's
`scripts/` directory — `link_check.py` and `sync_doc_snippets.py` (see
"Doctrine + tooling" below).

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

## Doctrine + tooling

This module ships the **discipline above** *and* a **stack-neutral,
scaffold-installed tooling set** -- the way the `claim-check` and
`lifecycle-metrics` modules ship runnable scripts (the 1:many
verbatim-install pattern). Two stdlib-only scripts land in the target's
`scripts/` directory:

* **`link_check.py`** -- the link / anchor half of the gate. Confirms
  every internal Markdown link, image, and reference definition resolves
  (relative targets exist; heading anchors resolve under GitHub slug
  rules). Vendor-neutral; external links are skipped unless
  `--check-external`.
* **`sync_doc_snippets.py`** -- the snippet half. A fenced doc block is
  mirrored from a named region of a runnable source file
  (`<!-- snippet: src#region -->` in the doc; `snippet-start: region` /
  `snippet-end: region` markers in the source, matched as plain
  substrings so any comment syntax works). `--check` is the CI drift
  gate; `--sync` rewrites a drifted block from its source (only the
  directive-bearing Markdown file is ever rewritten — never the source —
  and absolute / `..`-escaping source paths are refused).

**The claim half is *not* shipped here.** The default-on `claim-check`
module already installs `claim_check.py` (broken repo paths,
out-of-bounds citations) into the target's `scripts/`. The doc-drift gate
**composes** with it rather
than bundling a second copy: the full authoring-time check runs
`claim_check.py` (claims) + `link_check.py` (links) +
`sync_doc_snippets.py --check` (snippet drift). One source per check, no
duplication. Cairn itself runs this composition —
[`scripts/check_cairn.py`](../../../scripts/check_cairn.py) imports the
*shipped* `link_check.py` and `claim_check.py`, so the methodology's own
gate and the tools it hands an adopter are the same code.

**The schema-doc generator is deferred — an adopter slot, not a shipped
tool.** Generating a reference doc from a machine-readable schema (a
config schema, a type definition) inherently couples to one schema
language, so a *generic* generator cannot ship stack-neutrally. The
adopter wires their own (e.g. a `render_schema_docs.py` under `scripts/`
over their schema source), and the "generated, do not hand-edit" doctrine
above tells them what contract it must satisfy. Shipping it as an
optional, explicitly stack-specific module is a possible future
enhancement; it is intentionally **not** in the default install set.

## Learn it deeply

See [`docs/further-reading.md`](../../../docs/further-reading.md) >
"Reproducible, ethical, collaborative practice" for the reproducibility
craft Cairn points at rather than re-teaching.
