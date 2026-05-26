# Project Profile — greenfield design checklist

> Fill this for a **greenfield** codebase — one built with the
> methodology from the start. This is the *light* v1 checklist;
> deep greenfield design facilitation is a named methodology
> follow-up, not part of v1.
>
> **Fast path:** the `solo-greenfield` preset (or `collaborative-team`
> for a concurrent multi-agent team) pre-fills the six-axis point for a
> greenfield project — start there and adjust the axes below to the
> project's real scores. See `README.md > Governance presets`.

**Project:** {{project_name}}
**Drafted:** {{YYYY-MM-DD}}

A short, structured pass — a paragraph or two each:

* **Vision** — what the software is for; the scientific ambition.
* **Target users** — who runs it.
* **Scientific scope and non-goals** — what it does, and
  explicitly what it will not.
* **Core data model** — the canonical internal representations.
* **Architecture sketch** — the first-cut module shape.
* **Verification strategy** — how correctness will be shown.
* **Documentation plan** — the doc layers the project will keep.
* **First vertical slice** — the smallest end-to-end piece to
  build first.
* **"Ready to scale" criteria** — what tells the project it is
  past the prototype.

<!-- cairn:slot greenfield-checklist -->
(The bootstrapping agent works through the items above with the
Maintainer and records the answers here.)
<!-- cairn:end greenfield-checklist -->

## Dimensional placement

* **Age:** greenfield
* **Size:** {{size_position}} — {{size_reason}}
* **Complexity:** {{complexity_position}} — {{complexity_reason}}
* **Language:** {{language_position}} — {{language_reason}}

### Module-selection signals

Two conditions select team-gated modules even for a greenfield
project:

* **Trust boundary?** If untrusted input meets the system
  (deserialization, subprocess invocation, file / network I/O,
  path handling), select the `security-review` module — the gate
  is trust-boundary-first, not complexity-gated (see
  `modules/team-gated/security-review.md`).
* **Issue tracker?** If the team uses an issue tracker for gap /
  friction capture, select the `issue-capture` module (see
  `modules/team-gated/issue-capture.md`).
