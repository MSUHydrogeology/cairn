# Add an optional name argument to `greet`

**Author**: Maintainer
**Date opened**: 2026-05-22
**Status**: accepted
**Touches**: `greet.py`, `test_greet.py`

> This is a deliberately tiny, illustrative proposal for the
> `examples/minimal/` walkthrough. It shows the *shape* of a Cairn
> lifecycle record at the smallest possible scale — a trivial-accept
> change on a throwaway project. See the example `README.md` for the
> narrated trace.

## Context

The toy `greet` CLI always greets `"world"`. A user asked to greet a
named person. This is a one-function change with one test — small
enough to be a **trivial accept** (no separate plan).

## Proposal

Add an optional `name` argument to `greet(name="world")`, returning
`"Hello, <name>!"`, and absorb a test covering the default and the
named case. Update the CLI to pass through `sys.argv[1]` when present.

## Review -- Reviewer (Internal) -- 2026-05-22

Verified the change is one function + one test, backward-compatible
(the default preserves the old behavior). No interface beyond the new
optional argument; nothing to gate. Recommend **accept** as a trivial
change — the test absorbed alongside the code is exactly the discipline
("a change absorbs its tests"). No plan needed at this size.

## Decision -- Maintainer -- 2026-05-22

**Accepted** as a trivial change. Implemented in the same commit that
archived this proposal; the test landed with it, and the CHANGELOG line
recorded it. This is the whole loop at minimum scale:
propose → review → decide → implement (with the test) → record.
