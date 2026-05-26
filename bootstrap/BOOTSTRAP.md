# BOOTSTRAP.md — the Cairn bootstrap procedure

**Audience**: a capable reasoning agent running alongside a Human
Maintainer who is adopting Cairn for a repository.

**What this document is**: the authoritative procedure for a
**Level 2 bootstrap** (see `../on-ramp/README.md`). It has three
acts that must run in order. Act I produces a profile the
Maintainer accepts before anything is installed. Act II installs
and customizes the methodology. Act III is the operating posture
the team takes after installation.

**Vendor-neutral hard constraint (R-G)**: this procedure names no
specific AI model or vendor. Every instruction speaks to "the
agent" — any capable reasoning agent. The installed files inherit
the same constraint; run the vendor-neutrality lint (Step II-5)
before declaring the installation complete.

---

## Act I — Understand

*Run before touching the target repository.*

The goal of Act I is a **dimension profile** and a **module
selection** that the Maintainer has accepted. Installing the
apparatus before the Maintainer has accepted the profile is a
mistake: the profile drives every subsequent choice, and correcting
it after installation is far costlier than before.

### I-1 Read the doctrine

Before assessing the target project, read:

* `../doctrine/README.md` — the four-layer map of what Cairn is
* `../doctrine/lifecycle.md` — the proposal and plan lifecycles
* `../dimensions/README.md` — the six adaptation axes and the
  three module layers

This takes a few minutes and prevents mismatches between what the
doctrine says and what the assessment implies.

### I-2 Fill the project profile

Choose the applicable profile template:

* **Legacy project** (existing codebase, existing contributors):
  `../templates/phase-0/project-profile-legacy.md`
* **Greenfield project** (new or near-new codebase):
  `../templates/phase-0/project-profile-greenfield.md`

Fill the template. Do not skimp on the scientific-surface and
documentation-trust sections — those drive the legacy-agent and
scientific-trust-reviewer decisions downstream. If uncertain,
mark a field `[TBD — needs maintainer input]` rather than guessing;
the profile is presented to the Maintainer before installation.

### I-3 Fill the team profile

Fill `../templates/phase-0/team-profile.md`. Key questions:

* How many humans contribute regularly?
* How many agent types are in use (or planned)?
* Is concurrent multi-agent work happening (multiple agents in the
  same session simultaneously)?
* Does the codebase span multiple languages?

### I-4 Score the six axes

Using the filled profiles and the rubrics in `../dimensions/`,
assign a score to each of the six axes. Record a one-sentence
*reproducible reason* for each placement — "the codebase is 15
years old with no automated tests" is a reproducible reason;
"seems legacy" is not.

| Axis | Score | Reason |
|------|-------|--------|
| Age | greenfield / legacy | |
| Size | small / medium / large | |
| Complexity | simple / moderate / complex | |
| Language | single / multi | |
| Human team | solo / small-multi / large-multi | |
| Agent team | single / concurrent-single-type / concurrent-multi-type | |

### I-5 Derive the module selection

From the six-axis profile, select the module set:

1. **Invariant kernel** (always): the **lifecycle** (proposal →
   review → decision, plus the plan lifecycle for non-trivial
   accepted proposals); one designated Human Maintainer holding
   final Decision authority; append-only, commit-recorded
   deliberation; stigmergic coordination through a `dev/` tree;
   the baseline coordination tier; the session routines. These
   are non-negotiable — see
   `../dimensions/README.md > The three module layers`.

2. **Default-on modules** (installed unless a dimension removes
   them): lifecycle-metrics, reflections, claim-check. Remove a
   default-on module only when the dimensional profile gives a
   specific reason — record the reason.

3. **Team-gated modules** (add when the team can staff them):

   | Team-gated module | Install when |
   |-------------------|--------------|
   | `dual-review` | Agent team is concurrent-multi-type (can staff two-tier reviews with structural independence by agent type) |
   | `domain-agents` | Size is large and the codebase partitions into distinct scientific domains |
   | `legacy-agent` | Age is legacy and a readiness map plus characterization-testing harness are needed |
   | `dual-language-tests` | Language is multi |
   | `coordination-tiers` | Agent team is concurrent-multi-type and asynchronous or real-time coordination is needed |
   | `security-review` | The project has a non-trivial trust boundary (untrusted input meets the system: deserialization, subprocess, file/network I/O, path handling). Trust-boundary-first — complexity tunes the review cadence, not whether it installs |
   | `issue-capture` | The team uses an issue tracker for gap / friction capture (the User Agent surface) |
   | `model-selection` | Complexity is moderate or complex — instruments the capability-floor-by-role-and-risk discipline (`doctrine/roles.md`) with a tier rubric and a per-role mapping template |

4. **Optional top-level templates** (gated on a dimension axis): the
   human-facing `CONTRIBUTING.md` installs when the **human-team** axis
   is `small-multi` or `large-multi` (a repo with human authors beyond a
   solo maintainer) — it points to `AGENTS.md` for the shared rules
   rather than duplicating them. The scaffold records each installed
   optional template under `optional_templates:` in the fidelity
   manifest so the gate is auditable (`fidelity-check.md`). A solo
   project installs none. (The thin vendor wrapper `VENDOR.md` is *not*
   gated — it installs by default; see Act II.)

### I-6 Present the profile to the Maintainer

Write a short summary for the Maintainer before proceeding:

```
## Dimension profile — <project_name>

Age:          <score> — <reason>
Size:         <score> — <reason>
Complexity:   <score> — <reason>
Language:     <score> — <reason>
Human team:   <score> — <reason>
Agent team:   <score> — <reason>

Module selection
  Kernel (always):       lifecycle, Maintainer authority, append-only
                         deliberation, dev/ tree, baseline coordination,
                         session routines
  Default-on (selected): lifecycle-metrics, reflections, claim-check
  Team-gated (selected): <list, or "none">
  Team-gated (deferred): <list with reason, or "none">
  Optional templates:    <CONTRIBUTING.md if human-team >= small-multi,
                          else "none"; VENDOR.md always>

Adoption level: Level 2 (full bootstrap)

Does this profile look right before I install anything?
```

**Do not proceed to Act II until the Maintainer has accepted the
profile.** If corrections are needed, revise and re-present.

---

## Act II — Install

*Run after the Maintainer accepts the profile.*

### II-1 Accept

The Maintainer's acceptance is the gate. Record the accepted
profile somewhere durable — the project's `dev/PLANNING.md` or a
`dev/strategy/` note — so that a future agent can audit why these
modules are installed and not others.

### II-2 Scaffold

Run the mechanical scaffold script from the Cairn repo:

```
python bootstrap/scaffold.py \
    --config <profile.yml> \
    --target <path/to/target/repo>
```

Or, if invoking from inside the target repository:

```
python <path/to/cairn>/bootstrap/scaffold.py \
    --config <profile.yml> \
    --target .
```

The script:

* Creates the `dev/` directory tree.
* Copies `templates/core/` into the target — including the thin
  vendor wrapper `VENDOR.md` (`@AGENTS.md` + a harness-only addendum);
  **rename it to your AI tool's auto-loaded file** (`CLAUDE.md`, …) and
  keep it thin (see `AGENTS.md` > "Vendor addendum").
* Copies the selected module files into the target's `dev/modules/`
  directory.
* Installs any **optional top-level templates** the profile's axes
  select — e.g. `CONTRIBUTING.md` at human-team `small-multi` /
  `large-multi` (I-5 step 4) — and surfaces them for recording under
  `optional_templates:` in the fidelity manifest.
* Substitutes all inline `{{placeholder}}` tokens with the values
  from the profile config.
* Writes a post-scaffold report listing every installed file and
  every block slot that still needs agent attention.

See `scaffold.py` for the config format and flags. The script does
**not** fill block slots — those are judgment work for the agent
and the Maintainer.

**Safe-by-default re-runs.** If a target file already exists, the
scaffold **skips** it by default and prints a skip warning rather
than overwriting it — a re-run (e.g., to install a newly enabled
module, or to upgrade Cairn) preserves any filled block slots and
project-local customizations the existing file carries. Pass
`--force` to opt into overwriting:

```
python <path/to/cairn>/bootstrap/scaffold.py \
    --config <profile.yml> \
    --target . \
    --force
```

Before running `--force` against an already-customized target,
commit your current state so git records what the overwrite would
discard.

### II-2a Legacy & existing-docs adopters — migrate state, de-risk the reorganization

> **Greenfield projects skip this step.** A new project has no
> pre-existing planning state to preserve and no existing
> documentation build to reorganize. Proceed to II-3.

A non-greenfield adoption carries two risks a greenfield one does
not; Act II handles both here.

**Plan-migration ledger** (a project with pre-existing planning
docs). A legacy project usually already has ad-hoc planning
documents holding real state — shipped phases, blocked items, links
to issues. A mechanical move into the Cairn `dev/` tree erases that
state silently. Before relocating any existing planning material,
build a **migration ledger** that preserves it, one row per
migrated item:

| Field | What it records |
|-------|-----------------|
| old path | where the planning item lived |
| new path | its home in the Cairn `dev/` tree |
| owning domain | who is responsible (if domain-agents is in play) |
| status | shipped / active / blocked / deferred |
| shipped-commit range | the commits that delivered already-done work |
| blocked-on | the dependency, if blocked |
| related issues | tracker links carried across |
| retroactive-review-exemption | whether already-shipped work is exempt from the proposal → review lifecycle, since it predates adoption |

The ledger is what a future agent reads to understand why
already-shipped work has no Cairn proposal behind it.

**Two-phase de-risking** (a project with an existing documentation
build). Do not combine the apparatus install with a risky
documentation reorganization in one undifferentiated step. Split
adoption into two phases:

* **Phase 1 — the collaboration apparatus.** The scaffold (II-2)
  writes new files into a `dev/` tree; it touches no existing
  build. This phase is near-zero-risk and is verified on its own
  (II-5) *before* Phase 2 begins.
* **Phase 2 — the risky reorganization.** Any relocation that
  touches an existing documentation build — moving docs, rewiring a
  docs generator, changing the build's expected layout — lands
  *after* Phase 1 is verified. A defect in the relocation then
  cannot obscure whether the apparatus itself works; the two
  failure surfaces stay separated.

A project with no existing documentation build runs only Phase 1.

### II-3 Select (confirm)

Review the post-scaffold report:

* Every file listed as "installed" should be present on disk.
* The module set should match the accepted profile.
* The block-slot list should be complete — every
  `<!-- cairn:slot ... -->` region in every installed file should
  appear.

If the scaffold missed a file or installed an unselected module,
correct it before proceeding.

### II-4 Customize (fill block slots)

For each block slot in the post-scaffold report, fill it with the
project's real, specific content. The slot's placeholder text
describes what is expected. A shipped empty slot is a review
finding.

**Several kernel slots are filled from installed module content, not
authored from scratch** — every module's `Adds to:` target is
slot-marked, so the R-F unfilled-slot check (Step II-5) *enforces* the
merge rather than relying on this prose alone:

* `role-roster-additions` in `dev/agent_collaboration.md` — the
  domain-agents / legacy-agent / security-review / issue-capture /
  model-selection roles
* `coordination-additions` in `dev/agent_collaboration.md` —
  `coordination-tiers`
* `claim-check` in `AGENTS.md` — the `claim-check` default-on module
* `reflections` in `dev/agent_collaboration.md` — the `reflections`
  default-on module
* `lifecycle-metrics` in `dev/agent_collaboration.md` — the
  `lifecycle-metrics` default-on module

A module whose `Adds to:` target is an existing prose section rather
than a slot (e.g. `dual-review` → the review-loop section) is merged
into that section per its `Merged into:` block. When a *selected*
module is not installed, mark its slot `N/A: <module> not installed`
so the gate tells a deliberate omission from a dropped merge.

Each module template under `<target>/dev/modules/<name>.md`
carries an **`Adds to:`** line near the top naming the kernel
section (and, by implication, the slot) its content belongs in,
plus a **`Merged into:`** block under `## Template content`
holding the prose to splice. For each installed module:

1. Read the module's `Adds to:` line — it names the kernel
   destination.
2. Read the module's `Merged into:` block — it contains the prose.
3. Paste that prose between the named slot's `<!-- cairn:slot
   ... -->` and `<!-- cairn:end ... -->` markers in the kernel
   file, replacing the placeholder text. Preserve the markers
   themselves.

Example: `<target>/dev/modules/dual-review.md` carries "Adds to:
the review section of `dev/agent_collaboration.md`" and a "Merged
into `dev/agent_collaboration.md`:" block whose content fills the
`role-roster-additions` slot. A first-pass adopter who writes a
paragraph from scratch into `role-roster-additions` ships kernel
doctrine that does *not* reflect the installed modules — the R-F
gate sees the slot filled but cannot see that it was filled with
the wrong content.

**Invariant**: no installed module should leave its declared
`Adds to:` slot unfilled. The R-F block-slot check (Step II-5)
confirms each slot has substantive content; this invariant
confirms the content is the *right* content.

**The remaining slots require Maintainer input directly** (no
module supplies them):

* `project-overview` in `AGENTS.md` — what the project does and
  who it is for.
* `project-conventions` in `AGENTS.md` — naming conventions,
  development environment, high-risk surfaces, operational
  pitfalls. This is judgment work; a reasoning agent and the
  Maintainer write it together.
* `team-roster` in `dev/collaboration_agreement.md` — the team
  members and their roles.

### II-5 Verify (R-F acceptance gate)

All items below must pass before declaring the installation
complete.

**Structural checks**
- [ ] `AGENTS.md` is present at the target repository root.
- [ ] `dev/README.md` is present.
- [ ] `dev/proposals/_template.md` and `dev/plans/_template.md`
      are present.
- [ ] `dev/collaboration_agreement.md` and
      `dev/agent_collaboration.md` are present.
- [ ] `dev/PLANNING.md` and `dev/NEXT_SESSION.md` are present.
- [ ] Each selected module file is present under `dev/modules/`.
- [ ] `dev/proposals/`, `dev/proposals/archive/`, `dev/plans/`,
      and `dev/plans/archive/` directories exist.

**Token checks**
- [ ] No `{{...}}` inline token remains unfilled in any installed
      file. Quick check:
      ```
      grep -r '{{' <target>/AGENTS.md <target>/dev/
      ```

**Block-slot checks**
- [ ] Every `<!-- cairn:slot ... -->` region has been filled (or
      carries an explicit `N/A: <reason>`). The placeholder text
      inside the markers is the unfilled state; replace it with
      real content. Quick check:
      ```
      grep -rn 'cairn:slot' <target>/AGENTS.md <target>/dev/
      ```
      Then confirm each match has substantive content between its
      open and close markers.

**Vendor-neutrality lint (R-G)**
- [ ] No specific AI model or vendor name appears in the **doctrine /
      template** files. Run, scoped to exclude the deliberation record:
      ```
      grep -rni \
        'claude\|codex\|gpt-4\|gpt-3\|gemini\|llama\|anthropic\|openai\|mistral' \
        <target>/AGENTS.md <target>/dev/ \
        --exclude-dir=proposals --exclude-dir=plans
      ```
      Three classes of match are **expected and allowed**, not
      findings — which is why the lint is scoped, not blanket:
      * **deliberation-artifact content** under `dev/proposals/` and
        `dev/plans/` — a Review / Response / Decision *names its
        reviewer* for attribution; that record is supposed to say who
        said what (hence the `--exclude-dir`s above);
      * **filename citations** — a proposal / plan stem may carry an
        author or agent name (e.g. `…-claude-…`); a *reference* to the
        file is not a content leak;
      * a **vendor-addendum file reference** (`CLAUDE.md`) — the
        sanctioned home for tool-specific habits, which imports
        `AGENTS.md`.
      Any *other* match in content (not a quoted example) is a finding:
      replace with "the agent", the role name, or a vendor-addendum
      reference. The addendum file itself must not contaminate the
      shared `AGENTS.md` or `dev/` doctrine.

**Dogfood gate (see Step II-6)**
- [ ] At least one real change has gone through the installed
      lifecycle — a proposal was written, reviewed, and a Decision
      recorded.

### II-6 Dogfood

Run one real change through the lifecycle before declaring the
bootstrap done. The goal is to find gaps in the customization
before they cost real work.

The suggested first change: filling the `project-overview` and
`project-conventions` block slots in `AGENTS.md`. These are
non-trivial enough to warrant a proposal (they define the project's
operating contract), and running that proposal through a review —
even a same-session internal review — exercises every piece of the
installed apparatus.

The dogfood run confirms:

* Proposals can be written in `dev/proposals/`.
* Review is recorded by appending a section and committing.
* Decisions are appended by the Maintainer.
* The post-decision file-move works.
* `AGENTS.md > Git and commit workflow` reflects the project's
  actual commit conventions.

---

## Act III — Operate and improve

*The ongoing operating posture after installation.*

### Session start

At the start of every session — cold start or after a context-loss
event — the agent runs a short orientation pass:

* Re-anchor on `dev/README.md` and the `dev/` tree.
* Read the commit log since the last handoff.
* Note any in-flight proposals or open plans.
* Confirm the role before substantive work.

See `AGENTS.md > Session start` in the installed target for the
full routine.

### Goodnight

At the end of every session the agent leaves a clean handoff:

* A status summary.
* A per-agent reflection (if the reflections module is installed).
* A scrub of the roadmap boards (`dev/PLANNING.md` and
  `dev/NEXT_SESSION.md`).

Committing and pushing are never implied — they wait on explicit
Maintainer approval.

See `AGENTS.md > Goodnight` in the installed target for the full
routine.

### Evolving the configuration

The configuration is not permanent. As the project grows:

* **Adding a module**: when the team gains the structure to staff
  a team-gated module, add it by copying the module file, filling
  its block slots, and opening a proposal for the change (the
  module is infrastructure; adding it changes the project's
  operating contract).
* **Updating the dimension profile**: re-run Act I-4 and I-5
  against the current state; update the accepted profile record;
  open a proposal if the update implies a module change.
* **Retiring a module**: requires a proposal (same reason as
  adding one).

### Self-assessment (periodic)

After the first few months of operation, or before a major phase
change, re-run the Act I assessment. The project's position on the
six axes drifts over time — a greenfield project ages, a small
codebase grows. The configuration should reflect the project as it
is, not as it was at bootstrap time.

---

## Appendix A — placeholder tokens in core templates

The scaffold fills these **inline tokens** from the profile config
(mechanical substitution):

| Token | File(s) | Description |
|-------|---------|-------------|
| `{{project_name}}` | `AGENTS.md`, `dev/README.md`, `dev/collaboration_agreement.md`, `dev/agent_collaboration.md` | The project's display name |
| `{{test_command}}` | `AGENTS.md` | The command to run the test suite |
| `{{claim_check_command}}` | `dev/modules/claim-check.md` (when the claim-check module is installed) | The command to run the write-time claim checker |
| `{{metrics_command}}` | `dev/modules/lifecycle-metrics.md` (when the lifecycle-metrics module is installed) | The command to run the lifecycle-metrics extractor |

**Document-author placeholders** — written as `{{...}}` but **kept**
in the installed templates for the document author to fill at write
time (e.g., when authoring a review or response). The scaffold does
not substitute these and the post-scaffold report does not warn
about them:

| Token | Where it appears | Filled by |
|-------|------------------|-----------|
| `{{Maintainer}}` | `dev/proposals/_template.md` Decision header | The Maintainer authoring a Decision |
| `{{author}}` | `dev/proposals/_template.md` Response header | The proposal author writing a Response |
| `{{reviewer}}` | `dev/proposals/_template.md` Review header | The reviewer writing a Review section |
| `{{assessor}}` | Phase-0 assessment templates | The agent filling the dimension profile |

Block slots (judgment work, left for the agent and Maintainer):

| Slot name | File | Expected content |
|-----------|------|-----------------|
| `project-overview` | `AGENTS.md` | What the project does and who it is for |
| `project-conventions` | `AGENTS.md` | Naming conventions, dev environment, high-risk surfaces, operational pitfalls |
| `role-roster-additions` | `dev/agent_collaboration.md` | Dimension-selected roles beyond the base roster |
| `coordination-additions` | `dev/agent_collaboration.md` | Higher coordination tiers if the team profile selects them |
| `claim-check` | `AGENTS.md` | The `claim-check` module's verify-before-asserting note (or `N/A` if not installed) |
| `reflections` | `dev/agent_collaboration.md` | The `reflections` module's per-agent handoff content (or `N/A`) |
| `lifecycle-metrics` | `dev/agent_collaboration.md` | The `lifecycle-metrics` module's extractor note (or `N/A`) |
| `team-roster` | `dev/collaboration_agreement.md` | The team members and their roles |

---

## Appendix B — profile config YAML format

The scaffold script reads a YAML file with the following shape:

```yaml
# Inline token values (mechanical substitution)
project_name: "MyProject"
test_command: "pytest"

# Module selection
modules:
  # Default-on (remove a line only if the dimensional profile gives
  # a specific reason to omit it):
  - lifecycle-metrics
  - reflections
  - claim-check
  # Team-gated (add from templates/modules/team-gated/ as needed):
  # - dual-review
  # - domain-agents
  # - legacy-agent
  # - dual-language-tests
  # - coordination-tiers
  # - security-review
  # - issue-capture
  # - model-selection
```

The `--target` flag tells the script where to write the installed
files. See `scaffold.py --help` for all flags.

---

## Appendix C — the bootstrap safety rules

See `SAFETY.md` in this directory for the full R-I safety
constraints. The two most critical:

1. The bootstrap **never** reads private content from the target
   repository into a file that will enter the Cairn repository or
   be shared publicly.
2. Generated `AGENTS.md` and `dev/` files must carry **no**
   secrets, credentials, local filesystem paths, or proprietary
   data.

The bootstrap's scope is *installation* — copying templates and
filling placeholders. Reading the target repo's source code,
architecture, or data to generate content is Act I analysis work
performed by the agent, not by the scaffold script.
