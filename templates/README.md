<!-- cairn-internal-ref-allow: doctrine/ reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
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
* **`skills/`** — the **lifecycle-routine skills**: the agentskills.io
  `SKILL.md` pair (`session-start`, `session-end`) plus the deterministic
  CLI they orchestrate (`_lib/session.py`, plus `_lib/board.py`) and the
  data-driven vendor
  fan-out table (`_data/vendor_targets.yml`). Because the session routines
  are invariant kernel, the skills install **unconditionally, like `core/`**
  (to the canonical `.agents/skills/` + `tools/session.py`), not
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
  listed in `bootstrap/BOOTSTRAP.md > Appendix A`.
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
`bootstrap/scaffold.py`'s `KNOWN_TOKENS` and in `BOOTSTRAP.md`
Appendix A; document-author placeholders register in
`scaffold.py`'s `_DOC_AUTHOR_TOKENS` and in Appendix A's
document-author table. Unregistered `{{...}}` tokens will appear in
the post-scaffold report's "unfilled token" warning, which is the
intended signal that a token has no contract.

## Using the templates

* **With the scaffold** — the way to install. The bootstrap
  (`bootstrap/`) copies and customizes the templates: it fills the
  inline tokens mechanically and leaves the block slots, with the
  dimensional profile, for the customizing agent. The profile decides
  which modules arrive; the on-ramp (`on-ramp/`) describes how to
  choose one.
* **By hand.** Copying `core/` and the selected modules into a
  repository and filling the placeholders yourself gives you the
  kernel, but not the files the installer adds on top of it (the
  session tools, the skills, the profile's day-one task list) and no lockfile,
  so the tree receives no upgrades until it runs
  `scaffold.py upgrade --init-lock` (see `on-ramp/README.md`).

Only the scaffold produces the complete tree; a copy by hand is the
kernel alone.

## Vendor-neutrality

Every template here is **vendor-neutral** — it names no specific
AI agent tool. The cross-vendor convention is a single `AGENTS.md`
governing-doctrine file; doctrine specific to one agent tool goes
in a separate file that imports `AGENTS.md`, so the shared content
stays single-sourced. The `core/` templates ship that split as the
model, not as an afterthought.
