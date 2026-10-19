# Modules

`modules/` holds the **dimension-selected add-ons** — the parts of
the apparatus an adoption installs only when its dimensional
profile (`dimensions/`) calls for them. The invariant kernel is in
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
