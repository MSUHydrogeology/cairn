# `dev/rules/` — project-owned agent-discipline detail

**This folder ships from Cairn, but its rule files are entirely the
adopter's own — Cairn never templates them.** The folder and this README
arrive at adoption; the files inside are written by the project team as
discipline accumulates. An empty `rules/` is a normal starting state.

## What lives here

`RULES.md` at the repo root is the **always-loaded router**: the few
bright-line rules that apply every turn, plus a routing table pointing to
elaboration elsewhere. This folder holds that **on-demand elaboration**
for rules whose full detail is *project-owned agent discipline* — the
"tail" of the head/tail split that keeps `RULES.md` compact.

**Registering a project rule never edits shared doctrine.** Add its file
here and index it from `RULES.md`'s routing table — *not* by adding a
pointer to `AGENTS.md` or `dev/agent_collaboration.md`. Because `RULES.md`
is always-loaded (read first at session-start), routing through it lets a
project add or retire its own rules without ever touching methodology Cairn
owns — the entire reason a project-owned rules surface exists. (A rule that
*generalizes* past this project is the exception: it folds *up* to Cairn,
not into shared doctrine in place — see below.)

* **Project-owned agent-discipline doctrine** — writing-time / review-time
  discipline, with any project evidence logs, that `RULES.md` routes to
  but that should not ride in every-call context.

## What does NOT live here

* **Descriptive software docs** — naming/style, library pitfalls,
  architecture. Those belong in `docs/` per your documentation plan.
* **Coordination / lifecycle process** — the proposal/plan lifecycle,
  review tiers, work-intents. That stays in `dev/agent_collaboration.md`
  and other top-level `dev/` coordination docs.
* **General (non-project) agent doctrine.** If a rule generalizes beyond
  this project it is a Cairn fold-back candidate (filed as a Cairn
  issue), not a project rule — it belongs *up*
  in Cairn methodology, not here.

## How files arrive and leave

Session orientation reads project rules first (`AGENTS.md` > "Roles").
When a rule needs explanation, this folder or `docs/` can hold it. Keep
`RULES.md` a small router; no scheduled rewrite is prescribed here.

## Contents

*(empty at adoption — add files as agent-discipline elaboration accumulates)*
