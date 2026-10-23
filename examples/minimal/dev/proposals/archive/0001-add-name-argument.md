# Add an optional name argument to `greet`

**Author**: Maintainer
**Status**: accepted
**Review**: usual
**Plan review**: not required(one function and one test; implemented and archived in one commit)
**Opened**: 2026-05-22
**In brief**: Let `greet` say hello to a named person, keeping "world" as the default.

> This is a deliberately tiny, illustrative proposal for the
> `examples/minimal/` walkthrough. It shows the *shape* of a Cairn
> record at the smallest scale. Adding an option is a new capability, so
> it takes the full proposal path; see the example `README.md` for the
> narrated trace.

## Context

The toy `greet` CLI always greets `"world"`. A user asked to greet a
named person.

## Proposal

Add an optional `name` argument, `greet(name="world")`, returning
`"Hello, <name>!"`. The CLI passes `sys.argv[1]` through when present.
The change lands with a test covering the default and the named case.

## Alternatives considered

* **Do nothing.** The user keeps editing the source to change the name.
* **A required argument.** Breaks every existing call; rejected.

## Evidence / verification plan

`test_greet.py` checks that `greet()` still returns `"Hello, world!"`
and that `greet("Ada")` returns `"Hello, Ada!"`.

## Signals the change is wrong

Any existing caller of `greet()` gets a different greeting.

## Review -- Reviewer -- 2026-05-22

```
Reviewed commit: illustrative example; no real commit
Target: the whole proposal
Prior findings: none
Assurance path: standard
```

**Tier**: usual
**Findings**: none
**Verdict**: ACCEPT

**Foundations**:

1. **Should this happen as framed?** Yes: one optional argument, and the
   default keeps today's behaviour -- `greet.py`.
2. **Best alternative.** Doing nothing, which leaves users editing the
   source; the proposal is the smaller cost -- *Alternatives considered*.
3. **What would show it wrong.** `greet()` returning anything other than
   `"Hello, world!"`; the default-case test pins it -- `test_greet.py`.

No findings. A plan is not needed at this size.

## Decision -- Maintainer -- 2026-05-22

**ACCEPTED.** The Maintainer's authorization, quoted verbatim:

> "Accepted. Implement it with its test and archive this proposal in the same commit."

Implemented in the commit that archived this proposal, with the test and a
CHANGELOG line.
