<!-- cairn-internal-ref-allow: doctrine/rationale.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Cairn's own adoption record (reconstructed)

**Author**: Claude (Implementation)
**Date**: 2026-07-11
**Status**: reconstruction, not a contemporaneous record

## What this document is

This note records the reasoning behind Cairn's own self-host adoption
profile (`dev/.cairn/profile.yml`, accepted by the Maintainer on
2026-06-12, Act I-6). It is **written on 2026-07-11** — nearly a month
after that acceptance — because the deliberation record `profile.yml`'s
own comment promised ("The deliberation behind it lives in `dev/strategy/`
... the adoption record") was never actually written at the time. This
document closes that gap. It is a **reconstruction from the committed
artifact**, not a transcript: it records what `profile.yml`'s own
content objectively supports, not a memory of a conversation that was
never captured. See "What is not recoverable" below for the explicit
boundary.

## The six-axis point

`profile.yml:14-16`'s own comment states Cairn's point in the adaptation
matrix: **greenfield / medium / moderate / single / solo /
concurrent-multi-type**. The six axes themselves — three describing the
codebase (age, size, complexity), three describing the team (language,
human-team, agent-team) — are defined in `dimensions/README.md` and each
axis's own file (`dimensions/age.md`, `size.md`, `complexity.md`,
`language.md`, `human-team.md`, `agent-team.md`). The canonical named
point this profile is built from is `bootstrap/BOOTSTRAP.md:178-181`'s
preset table: the `collaborative-team` preset's canonical six-axis point
is `greenfield / medium / moderate / single / small-multi /
concurrent-multi-type` — matching Cairn's own point exactly once the
`human_team: solo` override below is applied.

*(A 2026-05-14 strategy note, `2026-05-14-claude-human-ai-team-development-framework.md:443`,
discusses the `dimensions/` system's existence as part of a broader
structural survey of the project — worth citing as context for what
Cairn was thinking about around adoption time — but it does not itself
define the six-axis point values; `bootstrap/BOOTSTRAP.md` and
`dimensions/` are the technical source.)*

## The preset and its one override

**Preset: `collaborative-team`**, with **one override: `human_team: solo`**
in place of the preset's canonical `small-multi` point (`profile.yml:17-18`).
Cairn's own development, at adoption time, was one human maintainer
(Anthony Kendall) plus AI collaborators — the `small-multi` human-team
default the preset assumes did not match; `solo` does. Every other axis
of the `collaborative-team` point (greenfield codebase, medium size,
moderate complexity, single-language, concurrent-multi-type agent team)
was taken as-is.

## The three added modules

`profile.yml:20-23` lists `modules_add`, each with an inline
trust-boundary rationale already recorded at the time:

* **`issue-capture`** — GitHub Issues for gap/friction capture.
* **`security-review`** — named for "a real trust boundary: file I/O,
  path handling, YAML/module parsing" — the scaffold engine's own
  attack surface (parsing untrusted module/profile files, writing into
  a target tree).
* **`examples-gallery`** — because `examples/` ships runnable code that
  other adopters study and copy from; a trust-relevant surface for a
  methodology whose product is partly "code other people will imitate."

## Accepted 2026-06-12 (Act I-6)

The profile was accepted by the Maintainer on 2026-06-12, recorded as
Act I-6 (`profile.yml:7`). This document does not attempt to reconstruct
what "Act I-6" refers to beyond what `profile.yml`'s own comment states;
it is named here as the acceptance's own self-description, not expanded
on speculatively.

## What is not recoverable

This document draws only on `profile.yml`'s own committed content
(the axis comment, the preset/override, the per-module rationale
comments) and the `bootstrap/BOOTSTRAP.md` / `dimensions/` technical
definitions those choices resolve against. What it explicitly does
**not** claim to recover: any contemporaneous 2026-06-12 conversation,
deliberation transcript, or chat-stage reasoning that may have preceded
the committed `profile.yml`. If such a record existed, it was not
captured in a durable, discoverable form at the time, and this document
does not invent one on its behalf — doing so would repeat the exact
showcase-arc problem the sibling `review-record-integrity` proposal
corrected (recording deliberation that did not actually happen as
recorded).
