# Documentation Plan -- Cairn

**Status**: living document (Cairn's own self-hosted instance of the
`documentation-plan` default-on module).

This file is **Cairn's single source of truth** for how Cairn's own
documentation and doctrine are organized.  It states the documentation
**vision**, derives every artifact's placement from it, and tells
contributors -- human or AI -- *where new content goes* and *what
voice to use*.  It is the load-bearing artifact behind the structure:
`bootstrap/fidelity-check.md` plays this role for the scaffold's
fidelity contract, `bootstrap/BOOTSTRAP.md` for the install
sequence; this file plays it for Cairn's documentation and doctrine.

The `documentation-plan` default-on module ships **a forkable copy**
of this procedure to every adopter at `docs/DOCUMENTATION_PLAN.md`
(see `cairn/templates/modules/default-on/documentation_plan_template.md`).
The two artifacts share doctrine substance; only the worked-example
paths differ -- Cairn's self-hosted instance discusses Cairn's own
file inventory (cairn-prefixed paths); the forkable discusses an
adopter's installed tree (adopter-relative paths).  Drift is
**bidirectional under maintainer review** at the goodnight
Cairn-foldback step.

For the deliberation behind this file see the accepted fold-back
proposal, which was written in the reference deployment and is not in
Cairn's own `dev/proposals/archive/` (Cairn keeps its own record in
`dev/` -- Cairn 0.3 Goal 1).  The reference-deployment source
procedure is that deployment's `docs/DOCUMENTATION_PLAN.md` (frozen
May 2026 after the whole-repo four-layer extension).

## The documentation vision -- four layers

Cairn's documentation and doctrine answer four fundamentally
different questions.  *Which question an artifact answers*
determines which **layer** it belongs to, and the layer determines
where it lives.

### 1. Entry layer -- "What is this, and how do I enter?"

`cairn/README.md` (the methodology front door), `cairn/BOOTSTRAP.md`
(the install sequence + scaffolding contract), `cairn/CHANGELOG.md`
(the release record), `cairn/SECURITY.md` (the security disclosure
surface), `cairn/PROVENANCE.md` (the methodology lineage),
`cairn/SAFETY.md` (the safety threat model).  These live at the
repo **root** because *external convention* puts them there -- a
visitor expects `README.md`; the Keep a Changelog convention
expects `CHANGELOG.md`; the security disclosure convention expects
`SECURITY.md`.  Their placement is inherited, not a project choice.

### 2. Governing layer -- "How must I build?"

Prescriptive doctrine a contributor (human or AI) must follow to
make a correct change.  Two properties define the layer: it is
**prescriptive** ("do X", "build it this way") and it **governs
how something is built or organized**.  The layer has two ranges:

* **Cross-cutting governing doctrine** -- prescription that applies
  to every Cairn contributor regardless of task.  In Cairn:
  * `cairn/doctrine/` -- Cairn's **published methodology doctrine**
    (rationale, session-routines, lifecycle, doc-governance,
    dual-review, fold-back, onboarding, rate-limit-gate, roles).
    These files are the doctrine Cairn ships *as content* to every
    adopter -- not installed into the adopter's tree, but cited
    from `cairn/templates/core/AGENTS.md` references and read in
    the Cairn repo (the methodology authority).
  * `cairn/templates/core/AGENTS.md` -- the **template-shipped**
    operational reference that lands in every adopter's tree as
    `AGENTS.md`.  This is the adopter-facing surface of Cairn's
    governing doctrine.
  * `cairn/templates/core/VENDOR.md` -- the thin vendor-addendum
    wrapper that lands in every adopter's tree (renamed to the
    tool's auto-loaded file: `CLAUDE.md`, `GEMINI.md`, ...).
* **Domain-local governance** -- prescription that governs the
  organization of *one domain* and lives **in that domain**.  A
  domain-governance doc names the things it governs without living
  among each of them.  Examples in the Cairn tree:
  * `cairn/bootstrap/BOOTSTRAP.md` governs the install sequence +
    scaffold contract; lives in `bootstrap/`.
  * `cairn/bootstrap/fidelity-check.md` governs the fidelity
    contract; lives in `bootstrap/`.
  * **This file** (`cairn/docs/DOCUMENTATION_PLAN.md`) governs
    documentation placement and lives in `docs/`.  Organizing
    documentation is the documentation domain's own concern -- so
    its governance map is domain-local, exactly as
    `BOOTSTRAP.md` is for the install sequence.  This file's own
    placement in `docs/` is therefore *derived* from the vision,
    not an unexplained exception to it.

### 3. Deliberation layer -- "What should the project become, and how do we decide?"  (`dev/`)

The project **charter**, the **roadmap boards**, the
**deliberation record** (proposals, plans, strategy, upstream),
and the **process doctrine** governing the deliberation itself
(`collaboration_agreement.md`, `agent_collaboration.md`,
`security_review_protocols.md`).  The layer's defining property:
it is about the project's *becoming* -- aspiration, decisions in
progress, and the method of deciding -- **not** about the
software as it exists today.

**Cairn's own `dev/` tree is in place** (it was Goal 1 of the 0.3
milestone).  Cairn's own deliberation artifacts about its design
live there: proposals under `dev/proposals/` (decided ones in
`dev/proposals/archive/`) and plans under `dev/plans/`.  The
fold-back proposal behind this file stays in the reference
deployment.  This file's worked examples reference
`cairn/dev/proposals/` and `cairn/dev/plans/`, which exist today
as the deliberation layer's two working directories.

Cairn ships `cairn/templates/core/dev/` as the **template** an
adopter installs into their own tree; that is the *adopter-side*
deliberation layer, not Cairn's own.

### 4. Descriptive layer -- "How does the methodology work -- how do I use or extend it?"  (`docs/`)

Documentation of Cairn *as it exists today*, by audience
(getting-started, quickstart, dev-tour, agent-team-onboarding,
workflow-role, further-reading, release-process, related-practices,
glossary).  Its defining property: it
**describes current reality** -- it neither prescribes how to build
nor deliberates what to build.

Cairn's `docs/` is tier-light (not stratified into quickstart /
user-guide / theory / reference / developer the way a domain
project's `docs/` typically is); the methodology's surface area is
narrower than a domain codebase.  The descriptive layer also hosts
`cairn/case-studies/` (current-state pedagogical content describing
real deployments).

## The decision procedure

For any documentation or doctrine artifact, route it by one
question -- *what is it doing?*

* **Prescribing how to build or organize, cross-cutting and always
  relevant to a Cairn contributor** -> the **governing layer**, at
  Cairn's `doctrine/` (the published methodology) or at
  `cairn/templates/core/AGENTS.md` (the adopter-facing operational
  surface).  The doc-governance routing rule
  (`cairn/doctrine/doc-governance.md`) distinguishes the two
  ranges: methodology doctrine vs. adopter-facing operational
  doctrine.
* **Prescribing how *one domain* is organized** -> the governing
  layer's domain-local range, **in that domain** (e.g.,
  `cairn/bootstrap/BOOTSTRAP.md`, `cairn/bootstrap/fidelity-
  check.md`, this file in `cairn/docs/`).
* **Deliberating what to build, or how the team decides** -> the
  **deliberation layer**, `cairn/dev/` (Goal 1 substrate; the
  fold-back proposal behind this file is in the reference
  deployment).
* **Describing the methodology as it exists today** -> the
  **descriptive layer**, `cairn/docs/` -- including local how-to
  for extending or maintaining a specific surface, which stays in
  `cairn/docs/` (Cairn does not separately tier developer docs
  from user docs at present).
* **Front door / release record / security surface** -> the **entry
  layer**, at root -- a fixed, convention-inherited exception.

The one qualifier that does the most work is **cross-cutting**.
"Prescribes how to build" alone is too broad: a section of
`cairn/bootstrap/BOOTSTRAP.md` saying "to add a default-on module,
update `_DEFAULT_ON_MODULES` and `_MODULE_MAPPINGS`" prescribes
steps, but it is *local* how-to for one surface (the scaffold's
module registry) as it exists today, not cross-cutting doctrine.
It is descriptive-layer content -- description of current reality
plus the procedure to extend it -- and stays in
`cairn/bootstrap/`.  Local procedure does not promote a file to
root governing doctrine; only cross-cutting, always-relevant
prescription does.

## Scope of this map

This map routes **documentation and doctrine artifacts** -- the
files telling a contributor what Cairn is, how to build it, what
it should become, and how the methodology works.  "Whole-repo"
means it spans every documentation home (root, `cairn/doctrine/`,
`cairn/dev/` (Goal 1 substrate), `cairn/docs/`, `cairn/case-
studies/`, and the `cairn/templates/` surface that ships
adopter-facing doctrine), **not** every directory.

**Outside the map** -- software and its fixtures: the bootstrap
machinery (`cairn/bootstrap/scaffold.py` + the test harness under
`cairn/bootstrap/tests/`), the helper scripts (`cairn/scripts/`),
the module + dimension assets (`cairn/templates/modules/`,
`cairn/templates/dimensions/`, `cairn/templates/onboarding/`,
`cairn/templates/presets/`).  A directory's landmark files
(`README.md`, `BOOTSTRAP.md`) are in the map even when the
directory's contents are not.

`cairn/case-studies/` is *in* the map -- a descriptive-layer
satellite -- because a case study is a pedagogical description
of a deployment.  `cairn/templates/` is *out*: it is a runnable
asset library the docs cite, not documentation itself.

## The naming convention

Root and per-directory **landmark** files are UPPERCASE; ordinary
layered content is lowercase.  A landmark is a directory's entry
point, roadmap board, or domain-governance map -- the file you
navigate *to* as a starting point.  The UPPERCASE set, repo-wide:

* **Entry** -- `README.md`, `BOOTSTRAP.md`, `CHANGELOG.md`,
  `SECURITY.md`, `PROVENANCE.md`, `SAFETY.md`.
* **Domain-governance maps** -- `cairn/bootstrap/BOOTSTRAP.md`,
  `cairn/docs/DOCUMENTATION_PLAN.md`.
* **Roadmap boards** (self-hosted in `cairn/dev/`) --
  `cairn/dev/PLANNING.md`, `cairn/dev/NEXT_SESSION.md`.

Everything else is lowercase: the methodology doctrine essays
(`cairn/doctrine/rationale.md`, `cairn/doctrine/session-
routines.md`, ...), the descriptive content
(`cairn/docs/getting-started.md`, ...), and specialized files
(`_template.md`).  The casing is a navigational signal -- an
UPPERCASE name says "this is a landmark; start here."  A
domain-governance map is UPPERCASE *because* it is a landmark,
at whatever level its domain lives, not because it sits at root.

## Assets -- where figures live, and what each one carries

The naming convention above covers Markdown files.  This covers the
image files documentation embeds: the explanatory diagrams and the
project-identity mark under `docs/assets/`.  (Distinct from the
runnable asset library under `templates/`, which "Scope of this map"
places outside the map.)

Almost nothing here is new practice.  Both assets in the tree today
-- `cairn-banner.svg` and `dual-review-independence.svg` -- already
satisfy every **file-level** rule below, so this section mostly
writes down what they do, so the third one does it too.  The
**legibility pass** at the end is the one genuinely new obligation:
no commit has recorded one yet.

**Home and name.**  Assets live in `docs/assets/`, are SVG, and are
named lowercase-kebab after **what the figure shows**, not the page
that embeds it: `dual-review-independence.svg`, never
`readme-figure-2.svg`.  A figure outlives its placement, and a name
tied to a page decays the moment the figure is reused or the page is
reorganized.

**License family -- declared per file.**  Cairn's by-file split has
three families and they must not overlap:

* **Explanatory diagrams** -- CC BY 4.0 (`LICENSE-CC-BY.md`).
* **The project-identity brand mark alone** -- CC BY-ND 4.0
  (`LICENSE-CC-BY-ND.md`), so the mark stays canonical.
* **A generator or tooling script**, wherever it lives -- MIT
  (`LICENSE-MIT.md`).

The license files name the covered assets **by path**, so adding an
asset means adding it there too.  Two records must agree: the
license file and the asset's own header.  If they disagree, the
asset is unlicensed in practice, because a reader cannot tell which
is authoritative.

**The header block.**  Every asset opens with an XML comment
carrying four things, in this order:

1. the filename and a one-line statement of what it is;
2. what it depicts -- enough that someone can check the figure
   against the doctrine it illustrates;
3. **`Provenance:`** -- hand-authored or generated, which proposal or
   plan produced it, and whether any external tool was involved;
4. **`License:`** -- the family by name, and a pointer to the
   license file or deed.

**Inertness.**  A figure is a document, not a program.  No
`<script>`, no `<image>`, no `xlink:href`, no `@import`, and no URL
that *loads* anything -- a license-deed URL inside the comment is
fine, because nothing fetches it.  Fonts are generic stacks
(`ui-sans-serif, system-ui, ...`), never a named face the reader may
not have.  Every asset carries a `viewBox` so it scales rather than
clipping.  These keep an asset renderer-portable and keep it from
becoming an injection surface.

**The caption rule -- and the caption is the alt text.**  An
**explanatory diagram**'s caption states **the conclusion the reader
should draw**, not what the figure is, and it lives in the alt text
of the Markdown embed, where it serves a screen reader at the same
time.  Compare the two in the tree: the Dual-Review figure's alt
text states the conclusion ("a first read that helps a change land,
and an independent read ... that makes it prove it should"), which
is the form to copy.  A caption that restates the prose beside it
means the figure is decoration, and decoration is a maintenance
liability with no offsetting value -- it can go stale, break in a
theme, or contradict the text next to it.  If a caption cannot be
written, the figure has not earned its place.

The rule binds explanatory diagrams, **not the identity mark**,
which depicts nothing and draws no conclusion; its alt text
describes the image, as `cairn-banner.svg`'s does.

**The legibility pass -- a human runs it, and nothing else will.**
Cairn has no CI, so this check's only trigger is a person
remembering, and it is written down here so the remembering has
something to attach to.  Before committing an asset that is new or
changed, render the page that embeds it and confirm, recording the
result in the commit body:

* it is **readable** in both light and dark theme;
* it **scales** at phone width as well as desktop, without clipping
  or overflowing;
* its **caption** (the alt text) is present, and for an explanatory
  diagram states a conclusion;
* it does **not break the page layout** around it.

An asset that fails any of these is fixed or dropped before the
commit lands.  Skipping the pass for speed is the point at which a
visual system starts costing more than it returns -- if it is going
to be skipped, drop the figure instead.

*Portability note.*  The legibility pass is the only part of this
section that is project-independent; the folder, the license
families, and the header form are Cairn's own.  Carrying it to the
forkable `documentation_plan_template.md` is a separate change under
the maintainer-review rule in "Updating this plan", not a
consequence of this one.

## The `templates/core/AGENTS.md` ↔ `templates/core/dev/agent_collaboration.md` boundary

`cairn/templates/core/AGENTS.md` and `cairn/templates/core/dev/
agent_collaboration.md` are the two adopter-facing doctrine
surfaces every adopter receives.  They carry agent-facing doctrine
read by every agent, but they sit in **different layers**:
`AGENTS.md` is governing-layer (operational), `agent_collaboration.md`
is deliberation-layer (process).  A stated boundary keeps them from
duplicating and drifting.

**Routing test** -- agent-facing adopter-side doctrine sorts into
three buckets:

1. **Building the software** (naming, architecture, tests,
   project-specific conventions) -> the adopter's `AGENTS.md`
   (filled via the `project-conventions` slot).
2. **Operating the repository safely** as a concurrent multi-agent
   workspace (commit hygiene, staged-index discipline,
   shared-file edit cadence, co-authorship trailers, the
   proposal-/plan-/strategy-doc-lifecycle commit exception,
   the Decision-commit guard-rail, "never author another agent's
   review record") -> `cairn/templates/core/AGENTS.md`, as a
   compact imperative rule.
3. **The team's deliberation and decision process** (roles, the
   proposal->review->decision lifecycle as a process, structural
   independence, review norms, handoffs) ->
   `cairn/templates/core/dev/agent_collaboration.md`.

**Operational safety minimum.**  For bucket 2 the executable
imperative rule stays in `cairn/templates/core/AGENTS.md` -- a
cold agent must commit / stage / edit a shared file correctly
without first following a pointer.  The rationale and process
theory live in `cairn/templates/core/dev/agent_collaboration.md`;
the two are paired (update together).

**Thin pointers for the rest.**  Purely explanatory bucket-3
doctrine gets only a thin `AGENTS.md` pointer -- a trigger, a
one-line gloss, a cross-reference -- never a restatement.  The
same rule stated *in full* in both files is drift-prone
duplication.

This operationalizes the Layer-2 / Layer-3 split for the two
adopter-facing files; it does not change the four-layer vision.

For the *Cairn-internal* equivalent boundary -- between Cairn's
published methodology doctrine (`cairn/doctrine/`) and Cairn's
own deliberation tree (`cairn/dev/`, Goal 1) -- the same
routing test applies: methodology doctrine stays in
`cairn/doctrine/`; in-flight deliberation stays in `cairn/dev/`.

## The `AGENTS.md` ↔ doctrine paired-update rule

For an adopter, an operational reminder in
`cairn/templates/core/AGENTS.md` (e.g., "Run the test suite after
any substantive change") often pairs with deeper *why* in
`cairn/templates/core/dev/agent_collaboration.md` (e.g., the
testing-discipline rationale).  When new operational content
surfaces, follow this rule:

* **Operational rule (cross-cutting, always-relevant)** -> add to
  `AGENTS.md` as a one-liner; ensure a paired rationale exists in
  `dev/agent_collaboration.md` (or one of the doctrine essays it
  cites).  Cross-reference both directions.  Both files update in
  the same commit.
* **Project-specific operational gotcha** -- import-location
  drift, CLI quirks, environment-setup pitfalls -- stay in
  `AGENTS.md` under the `project-conventions` slot.  No paired
  doctrine essay is required.

**Test for new content**: "does the rule have a defensible
methodology rationale in Cairn's doctrine, or is it
project-specific operational?"  If methodology -> paired
doctrine essay + `AGENTS.md` cross-reference.  If
project-specific -> `AGENTS.md` slot only.

## Updating this plan

Drift the plan only via a follow-up proposal.  Inline edits to
fix typos, add a tier subsection, or update an example are fine;
structural changes -- adding / removing a layer, changing the
decision procedure, changing the naming convention, changing
the AGENTS-vs-agent_collaboration boundary -- need a proposal.

Cross-propagation to the forkable
(`cairn/templates/modules/default-on/documentation_plan_template.md`)
is **bidirectional under maintainer review**: substantive
doctrine changes in this file should propagate to the forkable
(with paths and worked examples re-genericized to adopter-
relative form); substantive doctrine improvements that surface
adopter-side propagate back here (with paths re-cairn-prefixed).
Worked examples are deliberately divergent -- changes to one
do not auto-propagate.

## Cross-references

* **Reference deployment**: that deployment's
  `docs/DOCUMENTATION_PLAN.md` is the source-of-truth port
  reference (frozen May 2026 after the whole-repo four-layer
  extension).  Cairn-side foldback proposal:
  `2026-05-28-claude-cairn-foldback-documentation-plan` (lives
  in the reference deployment, not in `cairn/dev/`).
* **Module substrate**: `cairn/templates/modules/default-on/
  documentation-plan.md` (the module doctrine) +
  `cairn/templates/modules/default-on/documentation_plan_template.md`
  (the forkable shipped to adopters).
* **Slot anchors**: the module's `cairn:merge-target` directives
  fill `cairn:slot documentation-discipline` in
  `cairn/templates/core/AGENTS.md` and `cairn:slot
  documentation-tier-home` in the proposal + plan templates.
* **Doc-governance rule**: `cairn/doctrine/doc-governance.md`
  carries the layer-2 / layer-3 split's *methodology rationale*
  (this file carries its *concrete placement procedure*).
