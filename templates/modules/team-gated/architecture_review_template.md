# Architecture Review Frame — {{project_name}}

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
  live under the plan's folder, not the top-level `dev/`.
* **Assessment artifacts** the program produces.

When future architecture reviews run, they cite back to this document
for the lenses and biases. Updating the lenses or biases is itself a
deliberation worth a proposal — don't drift the rubric quietly.

## Current architectural shape

*(Fill: a short map of how the system is organized today — the major
components / packages and what each owns. State why the shape is the way
it is, and the single question the review most needs to answer about
it.)*

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

### 2. Data contracts

Questions: *(Which data structures cross module boundaries, and are they
stable enough to be treated as contracts? Are type / format boundaries
documented and contained? Is normalization handled in one place?)*

Signals to look for: *(Ad hoc dictionaries crossing boundaries; the same
spec re-interpreted in several places; silent type conversions inside
package logic; public functions with unclear expectations about their
inputs.)*

### 3. Correctness / provenance trust

Questions: *(Does each workflow provide enough diagnostics to catch a
bad assumption early? Can a user trace where an output came from? Are
derived results framed defensibly — can a numerical issue be told apart
from a judgment call?)*

Signals to look for: *(Late errors that could have been preflighted;
outputs without provenance; helpers that hide weighting or
transformation assumptions; summaries that don't expose the underlying
data.)*

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

### 5. Operational maturity

Questions: *(Can agents and humans change the system safely without
rediscovering context each time? Are tests and benchmarks aligned with
the claims the project wants to make? Are docs updated where readers
actually look? Is the session handoff producing enough context?)*

Signals to look for: *(Docs left stale after a feature change; test
tiers that don't match common dev environments; missing example coverage
for important workflows; roadmap items without success criteria.)*

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
