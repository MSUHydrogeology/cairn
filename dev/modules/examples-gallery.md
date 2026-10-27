# Module: examples-gallery

**Selected when:** the project benefits from a set of small, runnable
**worked examples** an adopter (or a new contributor) can run, read, and
learn from -- a library, a toolkit, a modeling apparatus. Team-gated (and
the narrowest-applicability of the practice modules), so a preset
(`governance presets`) selects it where worked examples earn their
keep rather than every adoption carrying it.
**Adds to:** an examples-discipline note in the adopting repo's examples
guide (and a cross-reference from `dev/agent_collaboration.md`).

Documentation tells; a **runnable example shows** -- and, unlike prose, a
runnable example can be *executed* to prove it still works. The risk is
the same drift `doc-drift-prevention` guards against: an example that is
not run rots into a confidently-wrong artifact. This module names the
discipline that keeps a gallery honest and makes it a learning surface.

Cairn **embodies** this -- its own `cairn/examples/minimal/`
traces one change end-to-end at the smallest scale -- and **points** at
the software-quality craft
(Cairn's own [cairn/docs/further-reading.md]); it does
**not** teach example *authoring*.

## Template content

Merged into the project's examples guide:

> **The gallery is a catalog, kept in lockstep.** Examples live in one
> place with a short catalog (what each shows, how to run it). The
> catalog and the example set stay in step -- a new example is added to
> the catalog in the same change; a removed one is struck.
>
> **Every example is runnable, and run.** An example is a *tested
> artifact*, not illustrative prose: it executes (a smoke test, a
> notebook-execution check, or a CI run) so a broken example fails the
> build rather than misleading a reader. An example that cannot be run is
> a snippet, and belongs in the docs under the drift gate, not the
> gallery.
>
> **Smallest-scale-first.** The gallery includes at least one *minimal*
> example -- the whole loop at the smallest scale -- so a newcomer sees
> the shape before the full-apparatus cases.
>
> **Disassemble / reassemble to learn.** A worked example doubles as a
> teaching surface: a learner takes a complete example apart and rebuilds
> it (or adapts it to a near neighbor) to internalize the apparatus,
> rather than reading it passively. The example is the substrate; the
> take-apart/rebuild is the exercise.

## Learn it deeply

The gallery *discipline* is Cairn's; building good examples and teaching
materials is craft Cairn points at, not re-teaches. See
Cairn's own [cairn/docs/further-reading.md] >
"Software quality for scientists".
