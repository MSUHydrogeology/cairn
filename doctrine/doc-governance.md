<!-- claim-check-allow: docs/developer/, docs/developer/vision.md, docs/vision.md -->
<!-- ^ illustrative adopter-tree paths in the tier-recognition and
     common-homes-for-vision sections; these are adopter-side
     conceptual paths, not Cairn-tree paths. -->

# Doc governance — where content lives

A Cairn project keeps its governing instructions in two files, and a
reader — human or agent — must be able to predict which one holds a
given rule without searching both. `AGENTS.md` is the **operational**
reference; `agent_collaboration.md` is the **process** doctrine. This
document is the routing rule that keeps the two from blurring and, over
time, from re-accreting each other's content.

## The three buckets

Sort every piece of governing content into one of three buckets; the
bucket decides its home.

1. **Building the software → `AGENTS.md`.** How to make a correct
   change to *this* project: the architecture, the conventions, the
   test and build commands, the domain-specific rules a contributor
   must follow.

2. **Operating the repository safely as a concurrent multi-agent
   workspace → `AGENTS.md`, as a compact imperative.** The
   *operational safety minimum*: the small set of active gates that
   keep concurrent contributors from corrupting the repository or each
   other's work — commit discipline, the shared-file edit cadence, the
   coordination signal. Stated as terse imperatives a cold-starting
   agent can internalize fast.

3. **The deliberation and decision process → `agent_collaboration.md`.**
   How the team *decides*: the role roster, the proposal → review →
   decision lifecycle, the review tiers and structural-independence
   floors, the session handoff routines — the deeper *why* behind the
   operational rules.

`AGENTS.md` holds buckets 1 and 2 because they are what an agent must
have loaded to act correctly *right now*; `agent_collaboration.md`
holds bucket 3 because deliberation doctrine is read when reasoning
about *how to change the system*, not in the middle of a routine edit.

## One canonical home, thin pointers

Each rule lives in **exactly one** of the two files. The other file may
*point* to it — a one-line cross-reference — but never restates it. The
failure mode this prevents is duplication drift: the same rule copied
into both files, later edited in one, and now silently contradictory.
When you find content that belongs in the other bucket, **move it and
leave a pointer**; do not copy it.

## The operational-safety minimum stays minimal

Bucket 2 is the one most prone to bloat. Every incident tempts a new
"operational" paragraph, and `AGENTS.md` slowly becomes a process
manual a cold-starting agent cannot absorb — which defeats its purpose,
since the operational reference is only useful if it is read and
retained. Hold the line: the operational-safety minimum is a **short
imperative limited to active git / commit / coordination gates** — the
rules that, if missed, let one contributor damage the repository or
another's in-flight work. Detailed walkthroughs, the reasoning behind a
gate, role definitions, templates, and deliberation-process guidance
are bucket 3: they live in `agent_collaboration.md`, and `AGENTS.md`
points to them. A rule earns a place in `AGENTS.md` only if an agent
must follow it to make a correct change *and* it is terse enough not to
crowd out the rest.

## Adaptation

The routing rule is team-size-neutral. A solo project still benefits
from knowing which file a rule belongs in — it keeps `AGENTS.md`
readable as the project grows — and a large multi-agent team needs the
one-home rule to keep the two governing files from diverging. Both
files are part of every Cairn adoption; this rule governs how their
content is split from the first commit, so the duplication never has a
chance to accrete.

## The descriptive layer (`docs/`) — tier recognition

Cairn recognizes the **descriptive layer** (`docs/`) as conventionally
tiered by audience: **Quickstart** (first-time users), **User Guide**
(regular use), **Theory / Reference** (theoretical grounding and the
API contract), and **Developer** (contributors maintaining or
extending the codebase — "how is this organized; how do I add a
thing"). An adopter's `docs/` chooses which tiers fit; not every
project needs all of them, and some projects use entirely different
conventions (Sphinx-shaped, MkDocs-shaped, Quarto-shaped, etc.).

Developer-facing content — architecture notes, contributing guides,
build / test / release procedures, code-organization notes — **commonly
lives in** `docs/developer/` when an adopter uses that tier; some
projects do not separate it out, and that is fine. `dev/` (the
deliberation layer) and `docs/developer/` (the descriptive developer
surface) carry different content kinds: `dev/` records *what is being
decided*, `docs/developer/` describes *how the codebase is*. Cairn
names the distinction but does not legislate the boundary's exact
location.

## Common homes for project vision / charter material

A project's vision or charter — the north-star description of what the
project is, who it serves, and what success looks like — is upstream
of deliberation. Cairn does not prescribe a single home for it; common
choices include:

* **`docs/developer/vision.md`** when the project has a Developer tier
  and the charter is read alongside architecture / contributing / etc.
  This is where a first-contact developer-onboarding reader naturally
  looks; it places the charter in the descriptive layer where it sits
  alongside other "how the project is" content.
* **`README.md`** when the charter is short enough to live at the
  entry surface a first-contact reader encounters before clicking
  through to `docs/`. Best for small or single-purpose projects.
* **A `docs/`-root vision page** (`docs/vision.md` or equivalent) when
  the project wants the charter as a top-level descriptive surface
  outside any specific tier — useful for projects whose audience is
  not primarily developer-focused.
* **`dev/vision.md`** when the project treats the charter as a
  deliberation artifact — what the project *should become* rather than
  what it is — and keeps it alongside proposals / plans / strategy.
  This places the charter in the deliberation layer; the trade-off is
  reduced discoverability for first-contact readers.

The adopter picks. Cairn's interactive-onboarding mechanism
(forthcoming as a `0.3` goal) eventually carries the dialogue surface
that helps adopters choose; today the choice is made by reading this
section and matching the project's audience.

## Adopter `docs/` format-neutrality

An adopter's `docs/` format is the **adopter's choice**. Cairn assumes
nothing about Markdown vs. reStructuredText vs. Asciidoc vs. Quarto.
Cairn's own canonical docs are `.md`; cross-references from Cairn-
shipped modules into Cairn's own docs use `.md` filenames because that
is where Cairn's docs live. Those references point **into the Cairn
repository**, not the adopter's tree. The adopter's `docs/` -- whatever
format -- is not constrained by Cairn's template format.

This is why Cairn-shipped team-gated modules disambiguate further-
reading references with the "Cairn's own" prefix: a Cairn module's
`See Cairn's own [\`cairn/docs/further-reading.md\`][rel-link]`
attribution makes the target unambiguously Cairn-owned, so an adopter
using Sphinx + reStructuredText is not steered toward `.md` by a
relative link the module ships.
