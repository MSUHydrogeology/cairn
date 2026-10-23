<!-- ^ Illustrative path: this example narrates a hypothetical proposal in the example's own dev/ tree, not a claim about Cairn's tree. -->

# Minimal example — Cairn on a throwaway project

The two [`case-studies/`](../../case-studies/) are the full-apparatus
examples on real projects. This is the opposite: the **whole loop at
the smallest possible scale**, so a newcomer sees the shape of a Cairn
change *small* before reading the large ones.

The toy project is a one-file `greet` CLI. Its Cairn kernel was copied
in by hand, with no lockfile (see
[`../../on-ramp/README.md`](../../on-ramp/README.md)): a `dev/` tree
with the proposal lifecycle, run by hand.

## The change, traced through the lifecycle

Cairn first sorts a change into one of three lanes
([`../../doctrine/lifecycle.md`](../../doctrine/lifecycle.md)): a typo or
one-line fix is just a commit with its test and a code review; a change
with a settled shape gets a short note and a review; a new capability gets
the full path. The change here -- *add an optional name argument to
`greet`* -- adds a capability, so it took the full path, shown in five steps:

1. **Propose.** A proposal is written and committed:
   [`dev/proposals/archive/0001-add-name-argument.md`](dev/proposals/archive/0001-add-name-argument.md).
   It states the context, the change, and that it is small enough that no
   separate plan was needed.
2. **Review.** A fresh reviewer who did not write the proposal appends
   a `## Review` section to the same file -- here, confirming the change
   is backward-compatible and that its test is absorbed alongside the
   code.
3. **Decide.** The Maintainer appends the `## Decision` section
   (accept), closing the deliberation. The proposal then moves to
   `dev/proposals/archive/`.
4. **Implement (absorbing tests + docs).** The code change lands with
   its test in the same step — [`greet.py`](greet.py) (the change) and
   [`test_greet.py`](test_greet.py) (the absorbed test). "A change
   absorbs its tests" is the discipline; your test framework runs them
   (`python -m pytest test_greet.py`), not Cairn — see
   [`../../docs/workflow-role.md`](../../docs/workflow-role.md).
5. **Record.** The decision and rationale live in the archived
   proposal; a one-line CHANGELOG entry would record the user-visible
   change. The git history plus the archived proposal *are* the record.

That is the entire loop. On a real project the proposal is larger and
a change that is not this small opens a plan, but the shape is
identical. Review is the same at every stage: one fresh reviewer who did
not write the work. For the narrated, step-by-step version see
[`../../docs/getting-started.md`](../../docs/getting-started.md).

> **The default-on disciplines come with tools.** This hand-copied
> example runs the lifecycle by hand, but an adopter who installs
> with the scaffold gets the claim-check discipline as a
> *runnable script*, not just prose: `claim_check.py` (in `scripts/`) is
> installed and wired to the `{{claim_check_command}}` token. See the
> [`claim-check`](../../templates/modules/default-on/claim-check.md)
> module.

## Files in this example

| File | Role in the trace |
|------|-------------------|
| [`dev/proposals/archive/0001-add-name-argument.md`](dev/proposals/archive/0001-add-name-argument.md) | The deliberation record (propose + review + decide). |
| [`greet.py`](greet.py) | The implemented change. |
| [`test_greet.py`](test_greet.py) | The test absorbed by the change. |

> This example is illustrative scaffolding. The `greet` code is a toy;
> the point is the *lifecycle shape*, not the program.
