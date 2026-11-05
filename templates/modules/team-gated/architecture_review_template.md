# Architecture Review Frame — {{project_name}}
Written in Cairn Plain Language 1.0

This document is the **rubric** for top-down architecture review — the
lenses an architecture reviewer applies, plus the starting biases the
reviewer must re-examine rather than inherit. It is reusable across
reviews; it is **not** a plan, a proposal, or a verdict on the current
codebase.

> **Forkable frame.** The lenses below ship as *questions + signals to
> look for*. Fill each with your own system's seams, contracts, and
> failure signals — replace the bracketed prompts with concrete entries
> for your codebase. The structure is Cairn's; the content is yours.

It is intended to be cited by:

* **Proposals** that frame an architecture-review program.
* **Plans** that execute such a program — in-flight assessment artifacts
  needed to carry out implementation may live alongside the plan only when
  their evidence cannot reasonably fit in the concise record or its canonical
  home; explain why and cite each artifact in the plan. Do not create them to
  provide review evidence.
* **Assessment artifacts** the program produces.

When future architecture reviews run, they cite back to this document
for the lenses and biases. Updating the lenses or biases is itself a
deliberation worth a proposal — don't drift the rubric quietly.

## Current architectural shape

*(Fill: a short map of how the system is organized today — the major
components / packages and what each owns. State why the shape is the way
it is, and the single question the review most needs to answer about
it.)*

Record the present homes of regular-file reading, write containment, terminal
encoding and Git execution, with their callers, limits and preserving tests.
Prefer those owners before creating another helper. A wrapper or standalone
shipped copy can be justified; explain its contract and how drift is detected.
Do not treat every similar function as interchangeable.

## Review lenses

Each lens is a set of **questions** and **signals to look for**. Fill
both for your system; the bracketed text is a prompt, not the answer.

### 1. Workflow coherence

Questions: *(Can a new user or contributor trace the path through the
system end to end? Do the entry points — CLI, API, notebooks, UI — share
the same concepts? Does a new feature have an obvious home?)*

Signals to look for: *(Duplicate orchestration logic; behavior that
lives in the wrong layer; entry points that bypass validated internal
paths; features that have to reach across too many components.)*

Trace one important user workflow. Count handoffs, parallel implementations
and unfinished outcomes; fewer lines do not compensate for losing the goal.

### 2. Data contracts

Questions: *(Which data structures cross module boundaries, and are they
stable enough to be treated as contracts? Are type / format boundaries
documented and contained? Is normalization handled in one place?)*

Signals to look for: *(Ad hoc dictionaries crossing boundaries; the same
spec re-interpreted in several places; silent type conversions inside
package logic; public functions with unclear expectations about their
inputs.)*

For repeated schemas or conversions, identify their owner and the consumer
that needs each difference. Consolidate only when the contracts really agree.

### 3. Correctness / provenance trust

Questions: *(Does each workflow provide enough diagnostics to catch a
bad assumption early? Can a user trace where an output came from? Are
derived results framed defensibly — can a numerical issue be told apart
from a judgment call?)*

Signals to look for: *(Late errors that could have been preflighted;
outputs without provenance; helpers that hide weighting or
transformation assumptions; summaries that don't expose the underlying
data.)*

Check whether safety helpers have diverged from their named homes. A narrow
drift check needs a dangerous counterexample and a legitimate-copy or wrapper
control; it is not proof that all other code is safe. Capabilities need cited
workflows or declarations, not a count of symbols.

*(This lens generalizes a "Scientific Trust" lens. Keep it wherever a
system's outputs are trusted and acted on; a pure-tooling project may
scope it down to correctness alone.)*

### 4. Extensibility

Questions: *(What happens when the next major capability is added? Do
new pieces fit through a stable extension point, or require bespoke
plumbing each time? Can one subsystem grow without coupling tightly to
another?)*

Signals to look for: *(A coordination object that absorbs unrelated
responsibilities; classes whose only purpose is to run one pipeline;
extension-specific names living outside the shared registry; feature
work blocked by test-fixture gaps.)*

Ask which present requirement earns each layer, class or extension point.
Prefer a small direct implementation when no second consumer needs a framework;
retain an abstraction when it makes a real contract easier to understand.

### 5. Operational maturity

Questions: *(Can agents and humans change the system safely without
rediscovering context each time? Are tests and benchmarks aligned with
the claims the project wants to make? Are docs updated where readers
actually look? Is the session handoff producing enough context?)*

Signals to look for: *(Docs left stale after a feature change; test
tiers that don't match common dev environments; missing example coverage
for important workflows; roadmap items without success criteria.)*

Assess functional coverage separately from execution time. Follow the selected
testing-discipline module or the project's existing testing guidance rather
than inventing another test scheme. Include growth of code, docs and process,
not only runtime or test counts.

## Contrasting applications

These are fictional examples, not measured results or mandatory redesigns.

| Situation | Evidence to seek | Proportionate conclusion |
|---|---|---|
| Legacy: two import commands normalize a sample ID differently. | Trace both public paths and a conflicting ID to their outputs; identify any intended compatibility difference. | Share normalization only if the contracts agree; preserve both public-path checks. If they differ deliberately, document that boundary rather than merging it away. |
| New: one workflow has a small parser and direct validation. | A reader can trace the workflow; malformed inputs refuse and outputs preserve units. No current second consumer needs a plugin interface. | Adequate practice. Add no class hierarchy or registry merely to anticipate growth. |
| Mixed: an older library and a new CLI each contain similar file readers. | Compare link, size, race and error requirements, plus installed-copy constraints. | Use the existing owner where contracts agree. Keep a stronger bounded reader or a necessary standalone copy, with its reason and targeted drift checks. |

## Release assessment

When this module is used at a release, update this record rather than opening
another checklist. Name the map's scope and omissions, useful or justified
neighbors, endpoint growth since the stated base, and ranked consolidation
opportunities with tests that must keep their detection. Distinguish measured
results from estimates and unknowns. Similarity and size alone justify neither
deletion nor an architecture change. Do not turn this assessment into another
approval stage.

## Biases to challenge

A reviewer applying these lenses must explicitly re-examine the starting
biases they bring. Each should be **reaffirmed with new evidence,
refined with caveats, or rejected with rationale** — never silently
inherited. This meta-move — naming your assumptions and forcing each to
face evidence — is the most portable part of the frame.

*(Fill: the assumptions your team holds about the architecture that the
review must not take for granted — e.g. "the current directory split is
right," "this class should stay a coordinator," "big features should
wait for fixtures." For each, state what evidence would reaffirm,
refine, or reject it.)*

## How a review program uses this rubric

A specific architecture-review **program** (a proposal + an optional
plan) applies these lenses and biases to produce assessment artifacts.
Those artifacts carry evidence markers — `[inference]` (reasoned from
evidence), `[hypothesis]` (plausible but unconfirmed), `[unverified]`
(asserted, not checked) — so a reader can tell judgment from fact. The
rubric stays stable across programs; the artifacts each program produces
are not part of the rubric. Decision-record formatting, if a decision
from a review warrants its own durable artifact, is a follow-up — not
baked into the rubric here.
