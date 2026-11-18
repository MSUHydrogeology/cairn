<!-- ^ Illustrative path: this example narrates a hypothetical proposal in the example's own dev/ tree, not a claim about Cairn's tree. -->

# Minimal example — Cairn on a throwaway project

The two [`case-studies/`](../../docs/case-studies/) are the full-apparatus
examples on real projects. This is the opposite: the **whole loop at
the smallest possible scale**, so a newcomer sees the shape of a Cairn
change *small* before reading the large ones.

The toy project is a one-file `greet` CLI. Its Cairn kernel was copied
in by hand, with no lockfile (see
[`../../install/on-ramp/README.md`](../../install/on-ramp/README.md)): a `dev/` tree
with the proposal lifecycle, run by hand.

## The change, traced through the lifecycle

This is a **light** change: an illustrative proposal, review and Decision
authorize an optional name without a separate plan. The record is a teaching
example, not evidence that an independent review or real Decision occurred.

1. Read the [illustrative proposal](dev/proposals/archive/0001-add-name-argument.md),
   including its review and Decision.
2. Run `python greet.py` for `Hello, world!` and `python greet.py Ada` for
   `Hello, Ada!` from this directory.
3. Run `python -m pytest test_greet.py`; both checks should pass. The code and
   test are the result of the illustrated change.

A real project records its actual review, Decision and implementation; it
uses a plan when its accepted standard or heavy work requires one.

## Files in this example

| File | Role in the trace |
|------|-------------------|
| [`dev/proposals/archive/0001-add-name-argument.md`](dev/proposals/archive/0001-add-name-argument.md) | The deliberation record (propose + review + decide). |
| [`greet.py`](greet.py) | The implemented change. |
| [`test_greet.py`](test_greet.py) | The test absorbed by the change. |

> This example is illustrative scaffolding. The `greet` code is a toy;
> the point is the *lifecycle shape*, not the program.
