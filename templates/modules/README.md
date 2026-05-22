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
| default-on | `lifecycle-metrics` | default; removed only for the smallest adoptions |
| default-on | `claim-check` | default |
| default-on | `reflections` | multi-agent adoptions; a solo, single-agent project may omit (the cross-agent handoff function disappears) |
| team-gated | `dual-review` | the team has two agent types, or multiple humans |
| team-gated | `domain-agents` | the codebase is large *and* the agent team is multiple |
| team-gated | `legacy-agent` | the codebase is legacy (the Age axis) |
| team-gated | `dual-language-tests` | the codebase is multi-language |
| team-gated | `coordination-tiers` | the agent team is concurrent, or high-concurrency |
| team-gated | `security-review` | the project has a non-trivial trust boundary (untrusted input meets the system); trust-boundary-first, complexity tunes cadence/depth |
| team-gated | `issue-capture` | the team uses an issue tracker for gap / friction capture (the User Agent surface) |

The kernel's own review — the same agent in a fresh session — runs
without the `dual-review` module; the module *adds* the second,
structurally-independent tier when the team can staff it.
