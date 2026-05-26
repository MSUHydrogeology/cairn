# Cairn doctrine

This directory explains the **invariant core** of the Cairn
methodology — the practices every adoption keeps, and *why* each
one exists. It is the "explain the doctrine" job of the repository
(see the top-level `README.md`).

Doctrine is **not** the templates. `doctrine/` explains the
reasoning; `templates/` ships the forkable files that put the
reasoning into a repository; `dimensions/` describes how an
adoption is *adapted* from the invariant core. Read `doctrine/` to
understand the method; copy `templates/` to adopt it.

## How to read this tree

| File | The question it answers |
|------|-------------------------|
| `README.md` (this file) | How is doctrine organized; what is the documentation model? |
| `lifecycle.md` | How does a change move from idea to shipped — the proposal and plan lifecycles? |
| `dual-review.md` | How is a change reviewed — the two-tier model and structural independence? |
| `roles.md` | Who does what — the role roster and how it scales with the team? |
| `collaboration-stance.md` | How do the team's agents engage each other — the collaborative-skeptic conduct stance? |
| `coordination.md` | How do concurrent contributors coordinate without colliding? |
| `session-routines.md` | How does a work session start and end so context survives handoff? |
| `rationale.md` | Why this method at all — the framework anchors and the gap analysis behind it? |

The invariant core is small by design. A project running Cairn
*also* selects optional modules along the adaptation dimensions
(`dimensions/`); the doctrine here is what no dimension removes.

## The four-layer documentation model

A Cairn project's own documentation answers four fundamentally
different questions, and *which question an artifact answers*
determines where it lives. This model generalizes to any adopting
repository; it is the routing rule that keeps governing doctrine,
deliberation, and description from silting together.

### 1. Entry layer — "What is this, and how do I enter?"

The repository front door and the release record — `README.md`
and a changelog. These live at the repository **root** because
external convention puts them there; their placement is inherited,
not chosen.

### 2. Governing layer — "How must I build?"

Prescriptive doctrine a contributor — human or AI — must follow to
make a correct change. Two properties define the layer: it is
**prescriptive** ("do X", "build it this way") and it **governs
how something is built or organized**. It has two ranges:

* **Cross-cutting governing doctrine** — prescription that applies
  repository-wide regardless of task. It lives at the **root**,
  the one place every contributor and every agent tool sees first.
  The cross-vendor convention is an `AGENTS.md` file; doctrine
  specific to a single agent tool is split into its own file that
  imports `AGENTS.md`, so the shared content stays single-sourced.
* **Domain-local governance** — prescription that governs the
  organization of *one domain* and lives **in that domain** (a
  test-tier guide in the test directory; a proposal-structure
  template beside the proposals). A domain owns the rules for its
  own organization.

### 3. Deliberation layer — "What should the project become, and how do we decide?"

The project charter, the roadmap boards, the **deliberation
record** (proposals, plans, strategy notes), and the process
doctrine governing deliberation itself. Its defining property: it
is about the project's *becoming* — aspiration, decisions in
progress, and the method of deciding — **not** about the software
as it exists today. Cairn places this layer in a `dev/` tree (see
`coordination.md`).

### 4. Descriptive layer — "How does the software work?"

Documentation of the software *as it exists today*, tiered by
audience. Its defining property: it **describes current reality**
— it neither prescribes how to build nor deliberates what to
build.

**Keeping descriptive docs in sync.** A descriptive doc that
*mirrors* a source of truth — a schema, example configs, an API
surface — must not be hand-maintained in parallel with that source;
it drifts. The discipline is **generate it outward from the source**
(or extract the snippet from a runnable example) and **guard it with
a drift gate** that fails the build when the two diverge. Default to
source-authoritative links; reach for snippet-sync only where inline
readability earns the sync cost. The model says *where* a doc lives;
this says *how* a generated/reference doc stays honest. The
`doc-drift-prevention` team-gated module ships the mechanism
(generators, snippet-sync, the CI drift gate); a project reaches the
principle here whether or not it installs the module.

### The routing rule

Route any documentation artifact by one question — *what is it
doing?*

* Prescribing how to build, cross-cutting and always relevant →
  **governing layer**, root.
* Prescribing how *one domain* is organized → **governing layer**,
  domain-local, in that domain.
* Deliberating what to build, or how the team decides →
  **deliberation layer**, `dev/`.
* Describing the software as it exists today → **descriptive
  layer**, tiered docs. This includes *local how-to* for extending
  one surface — description of current reality plus its extension
  procedure.
* Front door / release record → **entry layer**, root.

The qualifier that does the most work is **cross-cutting**.
"Prescribes how to build" alone is too broad: a how-to for
extending one surface prescribes steps, but it is *local*, not
cross-cutting — it is descriptive-layer content. Only
cross-cutting, always-relevant prescription belongs in root
governing doctrine.

## Voice follows layer

Each layer carries a voice, and matching voice to layer keeps a
reader oriented. Governing doctrine is **imperative** — it states
rules. The deliberation record is **deliberative** — it argues a
case. Descriptive documentation is **descriptive**, turning
imperative only where it gives a concrete procedure. The voice
tells a reader whether they are being given a rule, shown a
decision, or shown how something works.
