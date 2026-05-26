# Module: testing-discipline

**Selected when:** the project carries automated tests (or intends to)
and wants a coherent **test-tier scheme** rather than an undifferentiated
`tests/` pile. Broadly applicable; team-gated so a preset
(`governance presets`, P4) turns it on for the profiles that warrant it
rather than every adoption paying for it by default.
**Adds to:** a test-doctrine note in the adopting repo's `tests/` guide
(and a cross-reference from `dev/agent_collaboration.md`).

Cairn requires a change to **absorb its tests** (the lifecycle's
implement-with-tests step), but does not, on its own, say *how the test
suite is organized*. Without a scheme, "add a test" lands wherever, tiers
blur, and a reviewer cannot tell a fast unit check from a slow
integration run. This module gives the suite a shape.

Cairn **embodies** this discipline (its own `bootstrap/tests/` are
tiered) and **points** at where to learn testing craft
([`docs/further-reading.md`](../../../docs/further-reading.md), the
software-quality entry); it does **not** teach how to write a test.

## Template content

Merged into the project's `tests/` guide:

> **Test tiers are a single coherent scheme.** Tests live in named tiers
> -- e.g. **unit** (pure logic, synthetic inputs), **contract** (a stable
> schema / API boundary pinned against drift), **integration**
> (multi-component dataflow), **workflow** (end-to-end against a small
> fixture), and any project-specific tiers (notebook, benchmark, ...). A
> tier means the **same thing** everywhere, so a reader knows a test's
> cost and scope from its tier alone.
>
> **The tier is a property of location, not a hand-applied label.** A
> test's tier is determined by where it lives (its directory / a per-tier
> config), applied automatically -- authors do not hand-tag each test, so
> the scheme cannot rot through forgotten labels.
>
> **Contract tests pin stable schemas.** A boundary the project promises
> not to break silently (a config schema, a public API shape, a
> serialized format) gets a **contract test** that fails when the shape
> changes -- the change then has to be deliberate.
>
> **Negative tests prove the guards.** A validation or safety guard is
> tested by feeding it *bad* input and asserting it **fails loudly**
> (raises / rejects), not only by confirming the happy path. A guard with
> no negative test is an unproven guard.
>
> **A change records which tier(s) it touched.** The implement-with-tests
> step names the tier a new test lands in, so the suite's shape stays
> legible as it grows.

## Relationship to `dual-language-tests`

This module is the **base** test-tier discipline. The team-gated
[`dual-language-tests`](dual-language-tests.md) module is a
**specialization on the Language axis**: it keeps this tier scheme but
adds cross-language seam structure (each language keeps its framework; a
tier means the same thing across languages; the seam where one language
calls another is a named, tested surface). They are orthogonal -- tiering
vs. cross-language seams -- so a multi-language project selects **both**:
`testing-discipline` for the scheme, `dual-language-tests` for the seams.

## Learn it deeply

The tiering *scheme* is Cairn's; the craft of writing good tests is not.
See [`docs/further-reading.md`](../../../docs/further-reading.md) >
"Software quality for scientists" for the pointer Cairn relies on rather
than re-teaching.
