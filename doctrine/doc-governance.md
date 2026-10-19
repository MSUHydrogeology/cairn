<!-- ^ illustrative adopter-tree paths in the tier-recognition and
     common-homes-for-vision sections; these are adopter-side
     conceptual paths, not Cairn-tree paths. -->

# Doc governance — where content lives

This document routes Cairn's documentation and doctrine content into
two areas: the **governing layer** (`AGENTS.md`,
`agent_collaboration.md`) carrying *prescription* — how to build, how
to decide, how to coordinate — and the **descriptive layer** (`docs/`)
carrying *description* — what the project is, what its conventions
are, where common content lives. Each area has its own routing rules
and its own way of resisting drift.

The doctrine is organized into two halves:

* **Governing-file routing** (the first four sections below) tells a
  Cairn adopter where in the two-file governing layer
  (`AGENTS.md` vs `agent_collaboration.md`) a given rule belongs, so
  the two files do not blur or re-accrete each other's content over
  time.
* **Descriptive-layer recognition** (the remaining four sections)
  recognizes the conventional tiers of `docs/` (Quickstart / User
  Guide / Theory-Reference / Developer), states Cairn's
  format-neutrality with respect to the adopter's docs format, and
  enumerates the common homes for two often-misplaced descriptive
  artifacts (project vision and project-specific style conventions)
  *without* legislating any one location.

The two halves share a common method — **name the distinction, don't
legislate the boundary** — and both resist the same failure mode:
content slowly migrating into the wrong layer because the boundary
was never stated.

## Governing-file routing — `AGENTS.md` vs `agent_collaboration.md`

A Cairn project keeps its governing instructions in two files, and a
reader — human or agent — must be able to predict which one holds a
given rule without searching both. `AGENTS.md` is the **operational**
reference; `agent_collaboration.md` is the **process** doctrine. The
four subsections below are the routing rule that keeps the two from
blurring.

### The three buckets

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
   decision lifecycle, the review stance and how distance is recorded,
   the session handoff routines — the deeper *why* behind the
   operational rules.

`AGENTS.md` holds buckets 1 and 2 because they are what an agent must
have loaded to act correctly *right now*; `agent_collaboration.md`
holds bucket 3 because deliberation doctrine is read when reasoning
about *how to change the system*, not in the middle of a routine edit.

### One canonical home, thin pointers

Each rule lives in **exactly one** of the two files. The other file may
*point* to it — a one-line cross-reference — but never restates it. The
failure mode this prevents is duplication drift: the same rule copied
into both files, later edited in one, and now silently contradictory.
When you find content that belongs in the other bucket, **move it and
leave a pointer**; do not copy it.

### The operational-safety minimum stays minimal

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

### Adaptation

The routing rule is team-size-neutral. A solo project still benefits
from knowing which file a rule belongs in — it keeps `AGENTS.md`
readable as the project grows — and a large multi-agent team needs the
one-home rule to keep the two governing files from diverging. Both
files are part of every Cairn adoption; this rule governs how their
content is split from the first commit, so the duplication never has a
chance to accrete.

## Project-owned rules — the `RULES.md` convention

Some project doctrine is genuinely *not* Cairn doctrine: a project's
own bright-line rules — its development environment, its naming and
domain conventions, the safety rails specific to its problem domain.
Cairn's governing template (`AGENTS.md`) exposes a small budget of
**slots** (`project-overview`, `project-conventions`) for the *stable
identity* of such content, but a heavily-customized project's rule
corpus can exceed what slots hold, and rules placed in the
Cairn-tracked body *outside* a slot conflict on every upgrade that
touches that region.

`RULES.md` is the clean structural answer: an optional, repo-root,
**project-owned** rules file that Cairn **never templates and never
tracks**. It is absent from the install mappings (`_CORE_MAPPINGS`,
the skills mappings, the optional templates, and every module's install
specs), so the lockfile never records it and `scaffold.py upgrade`
never writes a base-cache entry for it — it is *structurally incapable*
of conflicting on upgrade. A one-line pointer in the core `AGENTS.md`
template (under **Session routines → Session start**) is the only
Cairn-side trace: it tells every adopter's agents to read `RULES.md`
first *if the project keeps one*. The file is otherwise the adopter's
to own end to end.

**Cairn declines *merge* opinion on `RULES.md`; the adopter keeps
*integrity* opinion on it.** "Untracked by Cairn" is not "unreviewed":
the file is tracked in the adopter's own git repo and covered by the
adopter's local quality gates (link checks, claim checks, and — if the
project loads it on every turn — its always-on token budget). An
adopter-side contract test should assert Cairn's lockfile / upgrade
output never tracks it.

**One home per rule (the boundary).** Each rule lives in exactly one
of three tiers, never duplicated verbatim across them:

| Tier | Holds | Tracked by | Load |
|------|-------|-----------|------|
| Cairn `AGENTS.md` slots (`project-overview` / `project-conventions`) | stable project *identity* + one-line high-risk pointers | Cairn lockfile (upgradeable) | always-on |
| `RULES.md` (project router) | the project's *bright-line rules* + a routing table | adopter repo (never by Cairn) | always-on, deliberately small |
| project `docs/` | bulky elaboration, domain references, incident logs | adopter repo | on-demand |

`RULES.md` is a **router, not a doctrine dump**: it carries only the
few rules that must apply every turn plus pointers to the on-demand
docs; the bulk stays in `docs/`. Keeping it small is what makes it a
token *win* rather than a relocation of the bloat.

**Where the routed elaboration lives is the project's choice** — Cairn
names the distinction, it does not legislate the location. Descriptive
detail (naming, domain references) belongs in the project's `docs/` per
the descriptive-layer routing below; *project-owned agent-discipline*
detail with no existing doc home may sit in a dedicated folder (e.g. a
`dev/rules/`-style directory beside the coordination docs) so it does not
clutter the top-level coordination space. Either way the rule has **one
home** and `RULES.md` only points.

**When does a rule belong in `RULES.md`?** A rule earns an always-on
slot only when **all** of these hold; otherwise it routes to a doc:

* **Every-turn.** An agent could get a routine action wrong *without it
  loaded on every turn* — the environment to run in, a naming/domain
  convention, a safety rail, a commit constraint. Reference an agent
  consults only *sometimes* (a how-to, a decision table, a dated
  incident log) is on-demand: it routes to a doc, with at most a pointer
  here. *A log of past instances never belongs in always-on context.*
* **Project-owned, not Cairn doctrine.** If the rule generalizes beyond
  this project, it is a **fold-back candidate** (it belongs *up* in
  Cairn), not a `RULES.md` entry.
* **Bright-line, not bulky.** State the rule in a line or two and route
  the elaboration. If it needs a table or multiple paragraphs to land,
  the *elaboration* is on-demand; only the bright-line summary stays.

This is a **growth-governance** question, not a one-time fill: a
deployment running the session routines re-scans for `RULES.md` drift in
both directions every goodnight (promote a new bright-line rule in;
demote bloat out) — see
[`doctrine/session-routines.md`](session-routines.md) > "Goodnight
`RULES.md` maintenance". The scan is what keeps `RULES.md` from slowly
re-bloating into a second always-on magnet.

## Descriptive-layer recognition — `docs/` and what lives in it

The second half of the doctrine recognizes the conventional tiering of
the adopter's descriptive layer, states Cairn's format-neutrality
toward the adopter's format choice, and enumerates the common homes
for two often-misplaced descriptive artifacts (project vision and
project-specific style conventions). Cairn **names** these
distinctions; it does **not** legislate any one location -- the
adopter picks, per the layer-prescriptiveness gradient (recognition
holds, legislation drops at the descriptive layer).

### Tier recognition

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

### Common homes for project vision / charter material

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

### Adopter `docs/` format-neutrality

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

### Common homes for project-specific style conventions

A project's **style conventions** — naming patterns, type prefixes,
language-specific idioms the codebase has standardized on — are
project-specific descriptive content rather than universal governing
doctrine. Code style varies per codebase (camelCase function args
in one project, snake_case in another; xarray-everywhere in a
scientific project, pandas-everywhere in an analytics shop), so the
**descriptive layer is the right home** for them. Cairn does not
prescribe one location; common choices include:

* **`docs/developer/style.md`** when the project has a Developer
  tier and the style guide is read alongside architecture /
  contributing / extending. A new contributor browsing the developer
  tier finds the conventions where the *how is the codebase
  organized* answer lives.
* **`docs/style.md`** when the project wants the style guide as a
  top-level descriptive surface outside the Developer tier — useful
  for projects whose contributor audience is not primarily
  developer-focused.
* **A project-specific equivalent** when the project uses a
  different `docs/` shape entirely (Sphinx-style, MkDocs-style,
  Quarto-style, etc.). The principle is *descriptive layer*;
  the exact filename and location follow the adopter's `docs/`
  convention.
* **At root (`STYLE_GUIDE.md`)** when the project wants
  external-tooling visibility from the repo entrance. The
  trade-off is that root files mix with governing-layer entries
  (`AGENTS.md`, `CHANGELOG.md`) and the reader has to disambiguate
  prescriptive code style from operational instructions. Cold-start
  agent discoverability for the agent-critical conventions can be
  preserved by direct `AGENTS.md` pointers wherever the style guide
  lives.

The adopter picks. Cairn's interactive-onboarding mechanism
(forthcoming as a `0.3` goal) eventually carries the dialogue
surface; today the choice is made by reading this section and
matching the project's audience.

Style guides are project-specific descriptive content because the
**choices** they encode (camelCase vs snake_case, type prefixes,
preferred libraries, line-length conventions) belong to the project,
not to Cairn. The methodology's bias is to **describe** where style
content commonly lives (here), not to legislate its specific
location.

## Cache-stable load order

Prompt caching only helps up to the first point the loaded context
changes; volatile content placed *before* stable doctrine busts the
cache for everything after it. So order the agent-loaded surface
**stable doctrine first (the cacheable prefix), volatile session-state
last.** This is scoped to what the **adopter controls**:

* Keep volatile boards — `dev/NEXT_SESSION.md`, `dev/PLANNING.md`, the
  current date/time — **out of the always-loaded files** (`AGENTS.md`
  and the vendor wrapper); load them on demand at session-start, not as
  part of the auto-loaded prefix.
* When a skill or routine loads several files within a session, read the
  **stable** ones (doctrine, conventions) before the **volatile** ones
  (today's boards, the handoff).

It does **not** promise cache savings on the harness-injected prefix:
for some agent tools the position of the auto-loaded `AGENTS.md` /
wrapper and the volatile date reminder relative to the doctrine prefix
is harness-determined, not doctrine-determined. The convention governs
the adopter-controlled surface; name which targets' load order is
actually controllable rather than claim a universal win.

## Profile-sized assembly — right-sizing the always-on surface

`AGENTS.md` is always-loaded, so every token it carries is a cost paid
on every turn. The **profile-sized assembly** mechanism lets a
template author shrink that cost for profiles that genuinely do not
need a section — without splitting the template or maintaining
per-profile forks.

**The `cairn:if` directive.** A template section may be wrapped with

```
<!-- cairn:if AXIS in val1,val2 -->
…content…
<!-- cairn:endif -->
```

where `AXIS` is one of the six profile dimensions and `val1,val2` is a
comma-separated membership set. Semantics:

* **keep-on-match** — axis value in the set → content kept, marker
  lines dropped.
* **remove-otherwise** — axis present, value not in the set → entire
  region dropped.
* **keep-on-missing-axis** — axis absent from the profile → content
  kept (the safe/conservative default for an always-on file; the
  opposite of `select_optional_templates`, which omits on missing).
* **raise-on-unbalanced** — unclosed `cairn:if`, stray `cairn:endif`,
  or nested directives → error.

No nesting is supported; the grammar is intentionally minimal.

**The never-gate-a-bright-line rule.** A `cairn:if` region may wrap
only profile-**optional** content — informational sections whose
absence leaves the operational rules intact. **No bright-line / safety
rule may ever be gated**: the inline-rule inventory (Git workflow, the
lifecycle, review, verifying claims, session routines, roles) must be
present for *every* profile, including the most restrictive. The
currently gated section in the core `AGENTS.md` template is `##
Human contributors`, gated on `human_team in small-multi,large-multi`
— informational to a solo maintainer who ships no `CONTRIBUTING.md`.
The test suite asserts that no IR1–IR13 rule is ever gated.

**Consistency at every materialization point.** The strip runs at
every point the template becomes an installed file — install,
lockfile expected hash, and the 3-way merge ancestor and `theirs`
sides — so the installed file, the cached expected-clean-install
hash, and the merge base all agree for a given profile. The base
cache stores the **raw, unsized** template; the strip is
reconstruction-time only, so a later profile change can still
re-include a previously-stripped section. `verify_integrity` is
unchanged: it compares the on-disk file against the lockfile hash,
and since the lockfile hash is now the hash of the *stripped* install,
the check stays consistent.

The implementation lives in
`bootstrap/_scaffold/config.py` (`strip_conditional_regions`), at the
DAG root beside `resolve_axes`. The tests (dedicated
profile-sized-assembly suite) assert both the grammar semantics and
the never-gate constraint.
