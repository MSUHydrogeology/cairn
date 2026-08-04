<!-- cairn-internal-ref-allow: doctrine/dual-review.md doctrine/lifecycle.md doctrine/plans.md doctrine/proposals.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# The review-before-implement gate enforces presence, not the review

**Author**: Claude (Implementation)
**Model**: Claude Opus 5 (`claude-opus-5`)
**Date opened**: 2026-08-04
**Status**: proposed
**Touches**: `tools/lifecycle_planner.py` and its byte-identical twin
`templates/skills/_lib/lifecycle_planner.py`; `bootstrap/tests/test_lifecycle_contract.py`
**Related**: routed out of `gate-claims-vs-enforcement` (row E2, which accepted,
measured and **declined to fix** it — its accepted contract is *"Nothing that
executes changes"*); originally surfaced in `planner-line-semantics`'s Internal
plan review. Maintainer direction to fix rather than route, 2026-08-04.
**Plan review**: required(**External**) — this changes a shipped verifier **and**
the twin an adopter installs, so a same-type read is not the floor
`doctrine/dual-review.md` sets for a contract surface.

## Context

Cairn's central claim is that a substantive change lands only after a review it
declared. `doctrine/plans.md:111-117` states a plan *"reaches `executing` only
after a dated `## Plan review` section lands: the review **and**, when it raised
findings, a dated `### Sharpening` subsection dispositioning them"*, and
`doctrine/lifecycle.md:175-182` says of the `required(<tier>)` line that *"The
gate is **explicit, not remembered**"*.

The verifier enforces none of those four properties. It checks that a section
whose heading begins with "Plan review" exists.

**Measured at HEAD `3852cf7`** under the canonical interpreter (Python 3.13.13),
by loading `tools/lifecycle_planner.py` and calling `_conformance_violations`
directly against fixture plans. Every fixture declares
`**Plan review**: required(**External**)` at status `executing`; the fixture body
is the only variable:

| Artifact state | gate |
|---|---|
| no `Plan review` section at all | **VIOLATION** (correct) |
| full `##` review labelled `(Internal, same-agent-type)` | **clears** |
| `###` sub-heading, **empty body** | **clears** |
| bare `## Plan review` — undated, no body at all | **clears** |
| review states REVISE with findings, **no `### Sharpening`** | **clears** |

So four documented promises are unenforced: **the tier**, **the `##` level**,
**dated**, and **Sharpening**.

**The code, re-derived from source at HEAD rather than from the routing note.**
`tools/lifecycle_planner.py:787` and `:860` gate on
`_has_kind(art, "Plan review")`; `_has_kind` (`:693-694`) is
`any(s.kind.lower().startswith(prefix.lower()) for s in art.sections)`. Sections
come from `_HEADER_RE` (`:509-515`), whose `#{2,3}` accepts **both** `##` and
`###`, and whose name / role / date groups are each independently optional — so a
bare `## Plan review` parses. The declared tier is read at `:663`, `:785` and
`:853`, always as `art.plan_review.lower().startswith("required")`: the token
inside the parentheses is **never parsed anywhere in the module**. The strings
`Internal` and `External` occur exactly twice in the file, both in prose
(`:364`, `:505`), neither in a code path.

`templates/skills/_lib/lifecycle_planner.py` is byte-identical
(sha256 `f1552fc7d0ee1d68a60d957389db75b4e5f8d39d8b7cb3561a028b36aa19f808`,
`as_of 2026-08-04`), so every adopter installs the same behaviour.

**Why this is worth its own scope.** The consequence is not hypothetical: this
repository currently holds twelve open plans whose Internal reviews state in
their own first paragraph that they do **not** discharge the declared tier — and
the gate clears them anyway. One reviewer has already filed under `###`
deliberately, working around a level the tool does not enforce. A gate that
reports satisfied while the control it names is absent is worse than no gate,
because it is silent — which is precisely the claim class
`gate-claims-vs-enforcement` exists to name, and it found this one inside Cairn's
own verifier.

## Proposal

Make the gate check the four properties its documents promise. Sketch, to be
made exact in the plan:

1. **Parse the tier.** Extract the `<tier>` token from `required(<tier>)` and
   require a review whose role field names that tier or stronger. `External` is
   satisfied by a different-agent-type or human read; `Internal` by either.
2. **Require `##`.** A `###` sub-heading is a placement convention, not a landed
   review. This must be done carefully: at least one existing plan carries its
   review under `###` for a stated reason, so the change needs a migration note
   rather than a flag day.
3. **Require a date** on the heading, matching the existing `_HEADER_RE` group.
4. **Require `### Sharpening`** when the review raised findings.

Each property gets a test node with a **single-property falsifier** — a mutation
that reddens that node and no other. Cairn has found five tests this cycle that
could not fail; this proposal will not add a sixth.

## Rationale

The verifier is the only mechanism standing behind the review discipline. Every
other layer is prose. If the tier is unparsed, `required(External)` is decoration
— and Cairn's Dual-Review differentiator, the thing the methodology is *for*,
rests on it.

## Alternatives considered

* **Leave it as a board row** (the status quo `gate-claims-vs-enforcement`
  chose). Honest about scope, but the finding has now been routed **twice**
  without landing, which is the "routed finding lost at the seam" failure that
  plan itself names. The Maintainer directed on 2026-08-04 that it be fixed.
* **Fold it into `planner-line-semantics`**, which owns the file. Rejected: that
  plan is not implementable — its own Response records eight outstanding
  findings and states no implementation lands on its strength — so the fix would
  queue behind them indefinitely.
* **Fold it into `gate-claims-vs-enforcement`**, which found it. Rejected: that
  plan's accepted contract is *"Nothing that executes changes."* Widening an
  accepted scope mid-implementation is the failure this repository audits.

## Evidence / verification plan

The measurement above is the evidence and reproduces from a ~30-line script
against the live module. The plan must additionally:

* pin each of the four properties with a single-property falsifier, and
  **demonstrate** each falsifier reddens exactly one node;
* verify the twin stays byte-identical (already enforced by
  `test_every_self_hosted_twin_stays_byte_identical_to_its_source`);
* re-run the gate over **every** artifact in `dev/` and report which currently
  pass and which would newly violate — a gate that reddens the existing tree on
  landing needs that disclosed up front, not discovered;
* state the adopter-facing consequence: an installed twin changes behaviour, so
  an adopter's previously-clearing plan may begin to violate.

## Signals the change is wrong

* The tier check cannot be made without a reliable way to tell agent types
  apart — the role field is free text, and a wrong answer here blocks real work.
* The `##` requirement breaks more existing artifacts than it protects.
* The gate becomes strict enough that agents route around it by editing headings
  to satisfy the parser, which would be worse than the present silence.
