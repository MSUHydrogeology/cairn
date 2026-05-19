# Templates

`templates/` holds the **forkable files** that put the Cairn
methodology into a repository. Where `doctrine/` *explains* the
method and `dimensions/` describes how an adoption is *adapted*,
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
  decided from its dimensional profile — see `dimensions/`.

## The `{{placeholder}}` convention

Template files carry **`{{placeholder}}`** tokens for the values
that are specific to an adopting project. There are two kinds, and
the distinction is load-bearing — it is the line between what a
script can do and what needs a reasoning agent.

* **Inline tokens** — `{{project_name}}`, `{{primary_language}}`,
  `{{test_command}}`, `{{maintainer_name}}`, `{{repo_host}}`, and
  the like: a short value substituted in place. Inline tokens are
  **mechanical** — the bootstrap fills them by simple substitution.
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

Every template states, at its top, which placeholders it carries.

## Using the templates

* **Level 1 — hand-copy.** Copy `core/` into the repository, add
  the modules the dimensional profile selects, and fill the
  placeholders by hand. The graduated on-ramp (`on-ramp/`)
  describes this path.
* **Level 2 — bootstrap.** The bootstrap (`bootstrap/`) copies and
  customizes the templates: it fills the inline tokens
  mechanically and leaves the block slots, with the dimensional
  profile, for the customizing agent.

Either way the *result* is the same tree; the bootstrap only
automates the mechanical part.

## Vendor-neutrality

Every template here is **vendor-neutral** — it names no specific
AI agent tool. The cross-vendor convention is a single `AGENTS.md`
governing-doctrine file; doctrine specific to one agent tool goes
in a separate file that imports `AGENTS.md`, so the shared content
stays single-sourced. The `core/` templates ship that split as the
model, not as an afterthought.
