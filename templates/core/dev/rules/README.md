# `dev/rules/` — project-owned agent-discipline detail
Written in [Cairn Plain Language 1.0](../agent_collaboration.md).

**This folder ships from Cairn, but its rule files are entirely the
adopter's own — Cairn never templates the files in it; `RULES.md` is seeded once, and upgrade merges preserve your edits to it.** The folder and this README
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

## Optional run rules

A project whose agents run its software may put run rules in root
`RULES.md`. Opt in by writing them there; they ship whole. Run rules add
limits and never relax `AGENTS.md`. They do not cite `dev/`; development
rules in this folder may cite run rules. Shared essentials can live in
`RULES.md`, but the governing instructions to read it and ask before pushing
remain in `AGENTS.md`. A release may retain `AGENTS.md` pointers into `dev/`
even when that folder is absent.

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
When a rule needs explanation, this folder or `docs/` can hold it. A Maintainer's rule goes in the rule file with the Maintainer's approved wording, never only in an agent's memory. Keep
`RULES.md` a small router; no scheduled rewrite is prescribed here.

## When this folder grows

Offered when: the Markdown files under `dev/rules/` (`README.md` excluded) hold more than 5000 words.

When that line is true, session start offers the guide below once and keeps the answer.

**Offer** (an agent fills in FIGURE and COMMAND). Your rules folder now holds
FIGURE words, counted with COMMAND, which adds up the words in each file.
Cairn has a short guide for a folder this size, in this file under "When this
folder grows": one shape for each rule, a line saying when it applies, a size
limit per entry, run rules (how to run the project's software or analyses)
kept apart from development rules (how to change its code and documents), and
how a rule enters and leaves. It costs about 425 words to read, adds no tool
and changes none of the files every session loads. Do you want help applying
it? If yes, I will propose a plan and change no rule file until you approve
that change. If no, I will not ask again. Either answer is fine.

**The guide.**

* **One shape per entry:** title, rule, why it exists, where its wording came from.
* **An `Applies when:` line** in each entry, so an agent can skip entries a
  task does not touch.
* **A size limit per entry.** About 300 words is a starting point; an entry
  well past it is usually two rules.
* **Run rules apart from development rules,** in different files. Run rules
  say how to run the project's software or analyses; development rules say how
  to change its code and documents. A session doing one kind of work then
  loads fewer words.
* **How a rule enters and leaves.** It enters as the person's approved wording
  in its file, never only in agent memory. It leaves by a dated line saying
  why, not by silent deletion.

**The record.** Answers are kept in dev/modules/offers.md: a first line
`# Offers record (format 1)`, then one line per answer, and nothing else but
blank lines.

`2026-11-16 | rules-folder-growth | declined | answered by: <name or role> | measured 5412 words`

The answer is `accepted` or `declined`. The name or role is what the person
gave (up to 40 characters, no `|`), or `not given`. The last field is
`measured`, a whole number and `words`. The file is at most 20,000 bytes of
UTF-8. Anything else makes it unreadable: no offer is made, and the agent says
why and leaves it as it is. To be asked again, delete your line; Git keeps it.

## Contents

*(empty at adoption — add files as agent-discipline elaboration accumulates)*
