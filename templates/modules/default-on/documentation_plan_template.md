<!-- The docs/* paths above are illustrative Diátaxis doc-tier examples in the
     structure table below — the dirs an *adopter* creates, not claims about
     this tree — so they are exempted from claim_check path resolution (they
     never resolve in Cairn's own tree; this keeps `check_cairn` clean). -->

# Documentation Plan

**Status**: living document.

This file is **the single source of truth** for how this project's
documentation and doctrine are organized.  It states the
documentation **vision**, derives every artifact's placement from
it, and tells contributors -- human or AI -- *where new content
goes* and *what voice to use*.  It is the load-bearing artifact
behind the doc structure: `AGENTS.md` plays this role for
operational doctrine, `dev/proposals/_template.md` and
`dev/plans/_template.md` play it for deliberation; this file plays
it for documentation and doctrine.

The procedure landed via the **`documentation-plan` Cairn module**
(installed by default; opt out via `modules: [-documentation-plan]`
in `profile.yml` if your deployment doesn't want the discipline
yet).  After install, customize the worked examples below to match
your own file inventory + tier vocabulary.

## The documentation vision -- four layers

Documentation and doctrine answer four fundamentally different
questions.  *Which question an artifact answers* determines which
**layer** it belongs to, and the layer determines where it lives.

### 1. Entry layer -- "What is this, and how do I enter?"

`README.md` (the project front door) and `CHANGELOG.md` (the
release record), plus any other root-level convention surface
(`SECURITY.md`, `CONTRIBUTING.md`, ...).  These live at the repo
**root** because *external convention* puts them there -- a visitor
expects `README.md`; the Keep a Changelog convention expects
`CHANGELOG.md`; the security disclosure convention expects
`SECURITY.md`.  Their placement is inherited, not a project
choice.

### 2. Governing layer -- "How must I build?"

Prescriptive doctrine a contributor (human or AI) must follow to
make a correct change.  Two properties define the layer: it is
**prescriptive** ("do X", "build it this way") and it **governs
how something is built or organized**.  The layer has two ranges:

* **Cross-cutting governing doctrine** -- prescription that
  applies repo-wide regardless of task: `AGENTS.md` (operational
  rules read by every agent at session start) and a vendor-
  addendum file (`CLAUDE.md` / `GEMINI.md` / ...) carrying tool-
  specific habits.  Because the cost of a builder *not* reading
  it is high, and because external tooling loads these from the
  repo root, cross-cutting governing doctrine lives at **root** --
  the one place every contributor sees first, with zero
  navigation.
* **Domain-local governance** -- prescription that governs the
  organization of *one domain* and lives **in that domain**.  A
  domain-governance doc names the things it governs without
  living among each of them.  Examples a typical deployment ships:
  * `tests/TEST_PLAN.md` governs test-tier placement and lives
    in `tests/`.
  * `dev/proposals/_template.md` and `dev/plans/_template.md`
    govern proposal / plan structure and live in those
    directories.
  * **This file** (`docs/DOCUMENTATION_PLAN.md`) governs
    documentation placement and lives in `docs/`.  Organizing
    documentation is the documentation domain's own concern --
    so its governance map is domain-local.  This file's own
    placement in `docs/` is therefore *derived* from the vision,
    not an unexplained exception to it.

### 3. Deliberation layer -- "What should the project become, and how do we decide?"  (`dev/`)

The project **charter** (e.g., `dev/vision.md` or a `vision.md`
at the docs root, deployment's choice), the **roadmap boards**
(`dev/PLANNING.md`, `dev/NEXT_SESSION.md`), the **deliberation
record** (`dev/proposals/`, `dev/plans/`, `dev/strategy/`,
`dev/.cairn/`), and the **process doctrine** governing the
deliberation itself (`dev/collaboration_agreement.md`,
`dev/agent_collaboration.md`, optional security or architecture
review protocols).  The layer's defining property: it is about
the project's *becoming* -- aspiration, decisions in progress,
and the method of deciding -- **not** about the software as it
exists today.

### 4. Descriptive layer -- "How does the software work -- how do I use or extend it?"  (`docs/`)

Documentation of the project *as it exists today*.  Its
defining property: it **describes current reality** -- it
neither prescribes how to build nor deliberates what to build.

Most descriptive content lives under `docs/`.  Whether `docs/`
is tiered (e.g., quickstart / user-guide / theory / reference /
developer; or Diátaxis's how-to / explanation / reference /
tutorials) is a deployment choice -- pin the tier vocabulary
below in "The descriptive-layer tiers".

## The decision procedure

For any documentation or doctrine artifact, route it by one
question -- *what is it doing?*

* **Prescribing how to build or organize, cross-cutting and
  always relevant to a builder** -> the **governing layer**, at
  root (`AGENTS.md`).
* **Prescribing how *one domain* is organized** -> the
  governing layer's domain-local range, **in that domain**
  (`tests/TEST_PLAN.md`, this file in `docs/`, the
  `_template.md` files in `dev/proposals/` and `dev/plans/`).
* **Deliberating what to build, or how the team decides** -> the
  **deliberation layer**, `dev/`.
* **Describing the software as it exists today** -> the
  **descriptive layer**, `docs/` -- this *includes local how-to*
  for extending or maintaining a specific surface, which stays
  in `docs/` (e.g., `docs/developer/<topic>.md`).
* **Front door / release record** -> the **entry layer**, at
  root -- a fixed, convention-inherited exception.

The one qualifier that does the most work is **cross-cutting**.
"Prescribes how to build" alone is too broad: a section of
`docs/developer/extending.md` saying "to add a new plugin, do X"
prescribes steps, but it is *local* how-to for one surface as
it exists today, not cross-cutting doctrine.  It is descriptive-
layer content -- description of current reality plus the
procedure to extend it.  Local procedure does not promote a
file to root governing doctrine; only cross-cutting,
always-relevant prescription does.

## The descriptive-layer tiers

*Customize this section to match your `docs/` structure.* The
descriptive layer is itself tiered by audience and intent; pick
the tier that matches what you need.  A typical structure (the
Diátaxis-style split) might be:

| Tier | Audience | Intent | Voice |
|---|---|---|---|
| **Quickstart** (`docs/quickstart/`) | First-time visitors | Get to a successful first run in minutes | Imperative, narrow |
| **How-to / User guide** (`docs/user_guide/` or `docs/how-to/`) | Active users | Time-to-productive-use; ongoing reference | Descriptive + procedural |
| **Reference** (`docs/reference/`) | Anyone looking up specifics | Quick lookup of API, CLI, configuration | Terse, lookup-oriented |
| **Explanation / Theory** (`docs/theory/` or `docs/explanation/`) | Reviewers, scientists, students | Establish credibility; document design rationale | Descriptive, citation-heavy |
| **Developer** (`docs/developer/`) | Contributors extending the codebase | How the codebase is organized; how to add new surfaces | Descriptive + imperative |

Each tier's `index.md` is the landing page.  Replace this table
with your deployment's actual tier set; drop tiers that don't
apply.

## The naming convention

Root and per-directory **landmark** files are UPPERCASE; ordinary
layered content is lowercase.  A landmark is a directory's entry
point, roadmap board, or domain-governance map -- the file you
navigate *to* as a starting point.  The UPPERCASE set, repo-wide:

* **Entry** -- `README.md` (at any level: repo root, `dev/`,
  `tests/`), `CHANGELOG.md`.
* **Root governing** -- `AGENTS.md`, the vendor-addendum file
  (`CLAUDE.md` / `GEMINI.md` / ...).
* **Roadmap boards** -- `dev/PLANNING.md`, `dev/NEXT_SESSION.md`.
* **Domain-governance maps** -- `docs/DOCUMENTATION_PLAN.md`,
  `tests/TEST_PLAN.md`.

Everything else is lowercase: the process-doctrine essays
(`dev/agent_collaboration.md`, ...), `docs/` topic content,
specialized files (`_template.md`).  The casing is a navigational
signal -- an UPPERCASE name says "this is a landmark; start
here."  A domain-governance map is UPPERCASE *because* it is a
landmark, at whatever level its domain lives, not because it
sits at root.

## Figures -- the legibility check

If this project's documentation embeds figures, one check has to
exist somewhere, because nothing else catches it: **a figure that
is unreadable in the reader's theme, or clipped at narrow width,
looks perfectly fine in the source.**  Prose has spell-checkers and
link checkers; a rendered figure has neither.

Before committing a figure that is new or changed, render the page
that embeds it and confirm, recording the result in the commit
body:

* it is **readable** in both light and dark theme;
* it **scales** at narrow (phone) width as well as wide, without
  clipping or overflowing its container;
* its **caption** is present -- and for an explanatory figure,
  states **the conclusion the reader should draw**, not what the
  figure is.  The caption normally lives in the alt text of the
  embed, where it serves a screen reader at the same time.  A
  project-identity mark is the exception: it depicts nothing, so
  its alt text describes the image.
* it does **not break the page layout** around it.

**Name what runs this.**  If the project has CI that renders
documentation, say so here and put the check there.  If it does
not, the only trigger is a person remembering, and this section is
what the remembering attaches to -- write that down plainly rather
than describing a check that nothing performs.

A figure failing any of these is fixed or dropped before the commit
lands.  If the check is going to be skipped for speed, drop the
figure instead: a figure nobody verifies is decoration, and
decoration is a maintenance liability with no offsetting value --
it goes stale, breaks in a theme, or quietly contradicts the prose
beside it.

## Where new content goes

The decision procedure above, worked out for the common cases.
Identify what the content is *doing*, then route:

* **Cross-cutting prescription ("do X" / "don't do Y",
  repo-wide)** -> `AGENTS.md`.
* **Descriptive content for a user trying to do something** ->
  `docs/<user-tier>/<topic>.md`.
* **Local how-to for extending or maintaining a specific
  surface** -> `docs/developer/<topic>.md` (still
  descriptive-layer; local procedure does not promote it to
  root doctrine).
* **Lookup tables, API/CLI shape** ->
  `docs/reference/<topic>.md`.
* **Roadmap status** -> `dev/PLANNING.md`.
* **Strategic deliberation, proposals, plans** -> `dev/`.
* **Governance of one domain's organization** -> that domain's
  landmark map (a new test tier -> `tests/TEST_PLAN.md`; a
  docs routing change -> this file).

When in doubt, ask the procedure's question -- *what is this
artifact doing?* -- and route by layer.

## Voice rules per location

The voice rule is location-keyed:

| Location | Voice |
|---|---|
| `AGENTS.md` / vendor-addendum / domain-governance maps | Imperative ("do X", "don't do Y") |
| `docs/<tier>/<topic>.md` | Descriptive ("the system resolves X by ...") |
| `docs/<tier>/index.md` | Descriptive landing-page introduction |
| `dev/PLANNING.md` / `dev/NEXT_SESSION.md` | Status / queue |
| Notebook *cells* inside `examples/` | Imperative ("Run cell 3") |

## The `AGENTS.md` ↔ `agent_collaboration.md` boundary

`AGENTS.md` and `dev/agent_collaboration.md` both carry
agent-facing doctrine read by every agent, but they sit in
**different layers**: `AGENTS.md` is governing-layer
(operational), `agent_collaboration.md` is deliberation-layer
(process).  A stated boundary keeps them from duplicating and
drifting.

**Routing test** -- agent-facing doctrine sorts into three
buckets:

1. **Building the software** (naming, architecture, tests,
   project-specific conventions) -> `AGENTS.md`.
2. **Operating the repository safely** as a concurrent
   multi-agent workspace (commit hygiene, staged-index
   discipline, shared-file edit cadence, co-authorship
   trailers, the lifecycle-commit exception, the
   Decision-commit guard-rail, "never author another agent's
   review record") -> `AGENTS.md`, as a compact imperative
   rule.
3. **The team's deliberation and decision process** (roles, the
   proposal->review->decision lifecycle as a process,
   how review distance is recorded, review norms, handoffs) ->
   `dev/agent_collaboration.md`.

**Operational safety minimum.**  For bucket 2 the executable
imperative rule stays in `AGENTS.md` -- a cold agent must
commit / stage / edit a shared file correctly without first
following a pointer.  The rationale and process theory live in
`dev/agent_collaboration.md`; the two are paired (update
together).

**Thin pointers for the rest.**  Purely explanatory bucket-3
doctrine gets only a thin `AGENTS.md` pointer -- a trigger, a
one-line gloss, a cross-reference -- never a restatement.  The
same rule stated *in full* in both files is drift-prone
duplication.

## The `AGENTS.md` ↔ doctrine paired-update rule

An operational reminder in `AGENTS.md` (e.g., "Run the test
suite after any substantive change") often pairs with deeper
*why* in `dev/agent_collaboration.md` (e.g., the
testing-discipline rationale).  When new operational content
surfaces, follow this rule:

* **Operational rule (cross-cutting, always-relevant)** -> add
  to `AGENTS.md` as a one-liner; ensure a paired rationale
  exists in `dev/agent_collaboration.md` (or one of the
  doctrine essays it cites).  Cross-reference both directions.
  Both files update in the same commit.
* **Project-specific operational gotcha** -- import-location
  drift, CLI quirks, environment-setup pitfalls -- stay in
  `AGENTS.md` under the project-conventions section.  No
  paired doctrine essay is required.

**Test for new content**: "does the rule have a defensible
methodology rationale, or is it project-specific operational?"
If methodology -> paired doctrine essay + `AGENTS.md`
cross-reference.  If project-specific -> `AGENTS.md` section
only.

## Out of scope (deployment-specific to consider)

The doctrine above is the **Cairn-portable** core.  A deployment
may want to add (or strip) sections that are domain-specific:

* **High-risk modeling reminders** -- if the project involves
  numerical methods, scientific computation, or any domain
  where wrong defaults are load-bearing, a "high-risk
  reminders" section in `AGENTS.md` paired with theory-tier
  rationale is the typical shape (the reference
  deployment uses this).
* **Static-build documentation** (Sphinx, mkdocs, RTD) -- this
  file covers *content organization* only.  Choosing a static-
  build tool is a separate decision.  Markdown-as-served-from-
  GitHub is the default for new deployments.
* **Figure files -- location, naming, and license** -- where
  diagrams live, how they are named, and which license family each
  carries are deployment-specific, and depend on the project's own
  licensing.  If the project publishes figures, record the answers
  here or in a section of your own.  The legibility check above is
  the portable part; this is not.
* **Teaching tier** -- pedagogical content (notebooks +
  exercises wrapped around runnable artifacts) is a
  *descriptive-layer satellite* the Diátaxis framework calls
  "tutorials"; if the deployment publishes tutorials, name
  their location here (a common pattern is `teaching/` at the
  top level next to `examples/`; another is
  `docs/tutorials/`).

## Updating this plan

Drift the plan only via a follow-up proposal in `dev/proposals/`.
Inline edits to fix typos, update the tier table for a new
descriptive subdirectory, or refresh worked examples are fine;
structural changes -- adding / removing a layer, changing the
decision procedure, changing the naming convention, changing
the `AGENTS.md` ↔ `agent_collaboration.md` boundary -- need a
proposal.
