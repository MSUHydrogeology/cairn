# Module: testing-discipline

**Selected when:** the project carries automated tests (or intends to)
and wants a coherent **test-tier scheme** rather than an undifferentiated
`tests/` pile. Broadly applicable; team-gated so a preset
(`governance presets`) turns it on for the profiles that warrant it
rather than every adoption paying for it by default.
**Adds to:** a test-doctrine note in the adopting repo's `tests/` guide
(and a cross-reference from `dev/agent_collaboration.md`).

Cairn requires a change to **absorb its tests** (the lifecycle's
implement-with-tests step), but does not, on its own, say *how the test
suite is organized*. Without a scheme, "add a test" lands wherever, tiers
blur, and a reviewer cannot tell a focused unit check from a broader
integration run. This module gives the suite a shape and a small practice
for maintaining tests without losing the behavior they protect.

Cairn **embodies** this discipline (its own `bootstrap/tests/` are
tiered) and points to deeper testing craft in its
[cairn/docs/further-reading.md] software-quality entry. The guidance
below covers behavior and fault preservation during maintenance; it is
not a complete testing curriculum.

## Template content

Merged into the project's `tests/` guide:

> **Test tiers are a single coherent scheme.** Tests live in named tiers
> -- e.g. **unit** (pure logic, synthetic inputs), **contract** (a stable
> schema / API boundary pinned against drift), **integration**
> (multi-component dataflow), **workflow** (end-to-end against a small
> fixture), and any project-specific tiers (notebook, benchmark, ...). A
> tier communicates broad scope and expected cost; the test name and
> assertions show its specific behavior, and runtime is measured separately.
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
>
> **Start with behavior and plausible faults.** When changing a contract,
> name the behavior it promises and the likely ways it could break; keep a
> direct assertion or probe for each important fault.
>
> **Consolidate without losing detection.** Before combining cases or setup,
> map each removed assertion and plausible fault to a retained check. Keep a
> direct check when the remaining cases would not notice that fault.
>
> **Use public entry points and fresh state.** Exercise the public command or
> API when practical. Reuse immutable descriptions or builders, and create
> fresh paths and mutable repositories for each case.
>
> **Keep scope and runtime separate.** Choose a tier by the integration
> boundary. Record slow runtime separately; a long test may still check a
> narrow behavior.

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
See Cairn's own [cairn/docs/further-reading.md] >
"Software quality for scientists" for the pointer Cairn relies on rather
than re-teaching.
