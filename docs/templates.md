# Templates

`templates/` holds the **forkable files** that put the Cairn
methodology into a repository. Where `docs/methodology/` *explains* the <!-- cairn-internal-ref: docs/methodology/ reason=docs/methodology/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where docs/methodology/ references resolve") -->
method and `install/dimensions/` describes how an adoption is *adapted*,
`templates/` is what an adopter actually copies.

## How the tree is organized

* **`core/`** — the **invariant kernel**: the files *every*
  adoption gets, unchanged in shape. A repository running Cairn
  has all of these — an `AGENTS.md` governing-doctrine file at the
  root and a `dev/` coordination tree.
* **`modules/`** — **dimension-selected add-ons**, split into the
  **default-on** set (installed unless a dimension removes them)
  and the **team-gated** set (installed only when the team has the
  structure to run them). Which modules an adoption installs is
  decided from its dimensional profile — see `install/dimensions/`.
* **`skills/`** — the **lifecycle-routine skills**: the agentskills.io
  `SKILL.md` pair (`session-start`, `session-end`) plus the deterministic
  CLI they orchestrate (`_lib/session.py`, plus `_lib/board.py`) and the
  data-driven vendor
  fan-out table (`_data/vendor_targets.yml`). Because the session routines
  are invariant kernel, the skills install **unconditionally, like `core/`**
  (to the canonical `.agents/skills/` + `dev/tools/session.py`), not
  conditionally like a module.

## The `{{placeholder}}` convention

Template files carry **`{{placeholder}}`** tokens for the values
that are specific to an adopting project. There are **three** kinds,
and the distinctions are load-bearing — they mark the line between
what a script can do, what needs a reasoning agent, and what is
filled at write-time by a document author.

* **Inline tokens** — `{{project_name}}`, `{{test_command}}`,
  `{{claim_check_command}}` and the like:
  a short value substituted in place. Inline tokens are
  **mechanical** — the bootstrap fills them by simple substitution
  from the profile config at install time. The current set is
  listed in `install/BOOTSTRAP.md > Appendix A`.
* **Block slots** — a delimited region a contributor fills with
  project-specific prose: the project's own operational pitfalls,
  its architecture summary, its high-risk surfaces. A block slot
  is marked so it is unmistakable, and never silently shipped
  empty:

  ```
  <!-- cairn:slot project-conventions -->
  (A reasoning agent or the maintainer fills this region with the
  project's real, specific content. Shipping it unfilled is a
  review finding.)
  <!-- cairn:end project-conventions -->
  ```

  Block slots are **judgment work** — writing a project's genuine
  operational pitfalls is authorship, not substitution. The
  bootstrap leaves them for an agent and the maintainer.
* **Document-author placeholders** — `{{Maintainer}}`, `{{author}}`,
  `{{reviewer}}`, `{{assessor}}`: written as `{{...}}` but
  intentionally *kept unfilled* in the installed template, to be
  filled by the document author at write time (e.g., when a
  reviewer appends a `## Review -- {{reviewer}} -- {{YYYY-MM-DD}}`
  header to a proposal). The bootstrap does not substitute these
  and the post-scaffold report does not warn about them. They
  share the `{{...}}` syntax with inline tokens but live in a
  different lifecycle.

Every template states, at its top, which placeholders it carries.

Template authors adding new placeholders: register inline tokens in
`install/scaffold.py`'s `KNOWN_TOKENS` and in `BOOTSTRAP.md`
Appendix A; document-author placeholders register in
`scaffold.py`'s `_DOC_AUTHOR_TOKENS` and in Appendix A's
document-author table. Unregistered `{{...}}` tokens will appear in
the post-scaffold report's "unfilled token" warning, which is the
intended signal that a token has no contract.

## Using the templates

* **With the scaffold** — the way to install. The bootstrap
  (`install/`) copies and customizes the templates: it fills the
  inline tokens mechanically and leaves the block slots, with the
  dimensional profile, for the customizing agent. The profile decides
  which modules arrive; the on-ramp (`install/on-ramp/`) describes how to
  choose one.
* **By hand.** Copying `core/` and the selected modules into a
  repository and filling the placeholders yourself gives you the
  kernel, but not the files the installer adds on top of it (the
  session tools, the skills, the profile's day-one task list) and no lockfile,
  so the tree receives no upgrades until it runs
  `scaffold.py upgrade --init-lock` (see `install/on-ramp/README.md`).

Only the scaffold produces the complete tree; a copy by hand is the
kernel alone.

## Vendor-neutrality

Every template here is **vendor-neutral** — it names no specific
AI agent tool. The cross-vendor convention is a single `AGENTS.md`
governing-doctrine file; doctrine specific to one agent tool goes
in a separate file that imports `AGENTS.md`, so the shared content
stays single-sourced. The `core/` templates ship that split as the
model, not as an afterthought.

# Modules

`modules/` holds the **dimension-selected add-ons** — the parts of
the apparatus an adoption installs only when its dimensional
profile (`install/dimensions/`) calls for them. The invariant kernel is in
`core/`; everything here is conditional.

## Two sets

* **`default-on/`** — installed *unless* a dimension removes them.
  A typical adoption keeps all of them.
* **`team-gated/`** — installed only when the team has the
  structure to *run* them. A team-gated module is not "advanced";
  it is simply unstaffable below a certain team shape.

## How a module is structured

Each module is one Markdown file that states, at its top:

* **Selected when** — the dimensional condition that installs it.
* **Adds to** — where its content goes: a section merged into a
  `core/` file, or a new file.

The body is the module's **template content** — the doctrine
fragment, role, or tool contract the module contributes, carrying
`{{placeholder}}` tokens like any other template. A module that
ships a tool generalizes it from the methodology's reference
instance; the module file states the tool's contract.

## The modules

The scaffold writes a project-specific inventory to
dev/modules/README.md. That inventory lists only the resolved roster and
points to a first-use action and installed entry point for each selected
module. A fresh planning board receives one plain first-use task per selected
module. Neither artifact runs commands or makes a module mandatory. After the
task is written, the planning board belongs to the project; later installs and
repeat adoption do not restore or reconcile tasks. If you copy a module by
hand, run `upgrade --adopt-module` for that module. First adoption appends its
task at the end of the board and updates the inventory and lockfile; repeat
adoption can update the inventory without changing the board.

| Set | Module | Selected when |
|-----|--------|---------------|
| default-on | `claim-check` | default |
| default-on | `reflections` | multi-agent adoptions; a solo, single-agent project may omit (the cross-agent handoff function disappears) |
| default-on | `content-security` | default; explicit `modules_remove` opt-out for operator-attached-only workflows |
| default-on | `security-verification` | default; installs the local evidence *route* — the dispatcher plus its source-owned registry, which ships **empty**, so an adopter with no admitted security capability gathers nothing and is told so |
| token-gated | `python-security` | selected when `python_package` is declared and filled; never for a non-Python adopter |
| team-gated | `dual-review` | the team has two agent types, or multiple humans |
| team-gated | `domain-agents` | the codebase is large *and* the agent team is multiple |
| team-gated | `legacy-agent` | the codebase is legacy (the Age axis) |
| team-gated | `dual-language-tests` | the codebase is multi-language |
| team-gated | `coordination-tiers` | the agent team is concurrent, or high-concurrency |
| team-gated | `security-review` | the project has a non-trivial trust boundary (untrusted input meets the system); trust-boundary-first, complexity tunes cadence/depth |
| team-gated | `issue-capture` | the team uses an issue tracker for gap / friction capture (the User Agent surface) |
| team-gated | `architecture-review` | the codebase's architecture *accreted rather than was deliberately designed* (inherited legacy, merged prototypes, vibe-coded growth); not gated on team shape — a solo maintainer with an inherited legacy codebase qualifies |

The kernel's own review — a fresh reviewer who did not write the work —
runs without the `dual-review` module; the module *adds* guidance for a
team with two agent types or several people on staffing a read the
Maintainer has called.

# issue-capture — forge-specific reference starters

The `issue-capture` module works with any issue tracker. It defines four
types of reports — Bug, Gap, Friction, and Wish — and when to review them,
without requiring a particular hosting service. The `templates/modules/team-gated/issue-capture/reference/` directory provides
starter files for GitLab and GitHub so adopters can use the guidance without
building forms from the field lists.

* `.gitlab/` — issue templates (GitLab's web UI auto-discovers
  `issue_templates/`) + a `labels.yml` manifest applied by a bootstrap
  script.
* `.github/` — `ISSUE_TEMPLATE/` markdown forms (YAML frontmatter
  carries the labels) + a `labels.yml` for `gh label` / a label-sync
  action.

**These are starters, not rules.** Copy the directory for your hosting
service into your repository root. Then add any project-specific routing
labels to `labels.yml` (for example, `domain::<area>` or `legacy`). The
starter labels are the minimum assumed by the triage guidance.
