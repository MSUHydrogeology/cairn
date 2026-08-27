<!-- ^ A forward reference: the accepted `transition-lint` proposal CREATES this
     file, so it cannot resolve until that scope lands. Named here because the
     fact that it is new is exactly why that scope collides with nothing. -->

# Sequencing the accepted security work into waves

**Author**: Claude (Strategy)
**Model**: Claude Opus 5.
**Date**: 2026-08-03
**Status**: **archived 2026-08-05** — retired on Maintainer instruction. Its
sequencing was superseded by `2026-08-05-codex-security-strategy.md`, which
consolidated the security cluster; the collision constraints it computed were
consumed by the waves that have since landed. Historical context only — not
current direction (see `../README.md` > "Archive trigger").

A scheduling note, not a decision. It answers one question: **given what each
accepted proposal touches, what can run at the same time without two agents
editing one file, and what must wait?** Every collision below was computed
from the proposals' own `Touches` headers and checked against the working
tree; nothing here is inferred from titles.

## The two constraints that actually bind

Almost everything sequences cleanly. Two things do the real work:

1. **`bootstrap/_scaffold/` changes are serialized by the AST ceremony, not by
   file overlap.** The baseline pins a *falsifiable union* of CHANGED symbols
   agreed in advance, so a concurrent engine change from an unplanned scope
   does not merely add to the union — it destroys the property the ceremony
   exists to provide. Two engine scopes may share one ceremony only if their
   union is declared before either lands.
2. **`templates/modules/team-gated/content_scan.py` is a frozen gate-manifest
   file.** Any content edit reports `FROZEN-MODIFIED` and needs a supervised
   re-pin, and ordinary `pytest bootstrap/tests` does **not** catch it. Every
   scope that edits the scanner should be batched into one ceremony rather
   than each buying its own.

## Collision map

| Scope | Principal surface |
|---|---|
| `fork-advisory-semantics` *(in flight)* | `_scaffold/lockfile.py`, `install.py`, `upgrade.py`, `verify_integrity.py` |
| `profile-parse-fail-open` *(in flight)* | `_scaffold/config.py`, `upgrade.py`, `cli.py` |
| `planner-line-semantics` | `tools/lifecycle_planner.py`, `tools/lifecycle.py`, + `templates/skills/_lib/` twins |
| `agent-context-scrub` | `tools/lifecycle.py` + twin, `SECURITY.md` |
| `content-scan-detectors` | `templates/modules/team-gated/content_scan.py`, `content-security.md` |
| `separator-detection` *(not yet decided)* | the same two files |
| `default-security-stance` | `_scaffold/config.py`, `bootstrap/profiles/*.yml`, `content-security.md`, `python-security.md`, `scripts/check_cairn.py` |
| `gate-claims-vs-enforcement` | `bootstrap/SAFETY.md`, `DEPENDENCY_BUDGET.md`, `floor-gate.sh`, `fidelity-check.md`, `doctrine/`, `AGENTS.md` |
| `stage-commit-patterns` | `tools/_lifecycle_metrics/gitmeta.py` + twin |
| `transition-lint` | **all new files** — `scripts/transition_lint.py`, its whitelist, a new test, a docs section |
| `release-security-bar` | **no code** — one plan, one `dev/PLANNING.md` row |

**The five real collisions:**

* `default-security-stance` ↔ `profile-parse-fail-open` — both edit
  `_scaffold/config.py`. Constraint 1 applies: `default-security-stance` lands
  **after** Wave 2's ceremony, not beside it.
* `default-security-stance` ↔ `content-scan-detectors` — both edit
  `templates/modules/team-gated/content-security.md`, and
  `default-security-stance`'s parity test binds the installed copy of a file
  `content-scan-detectors` is changing. The parity test wants stable content.
* `content-scan-detectors` ↔ `separator-detection` — the same scanner and the
  same test module. Constraint 2 says batch them.
* `planner-line-semantics` → `agent-context-scrub` — order already ratified by
  Maintainer ruling; they meet at exactly one expression and are behaviourally
  order-sensitive.
* `gate-claims-vs-enforcement` ↔ `scan-coverage` — `bootstrap/SAFETY.md` and
  `test_security_lint.py`. `scan-coverage` is committed, so this is only an
  ordering fact, not a conflict.

## Proposed waves

**Wave 2 — running.** `fork-advisory-semantics` → `profile-parse-fail-open`,
sequential (shared `upgrade.py`). Ends at the Maintainer fence.
→ **Ceremony 1: the batched engine re-anchor.** Maintainer-only.

**Wave 3 — four scopes, fully parallel.** Verified pairwise disjoint, and all
four disjoint from Wave 2's surface:

* `transition-lint` — creates only new files; collides with nothing by
  construction. The cheapest thing on the board.
* `stage-commit-patterns` — confined to `tools/_lifecycle_metrics/` and its
  `templates/modules/default-on/` twin.
* `planner-line-semantics` — `tools/lifecycle*.py` and twins. Its plan and
  Internal review are being written now.
* `gate-claims-vs-enforcement` — documentation and doctrine. Its `AGENTS.md`
  edit is a serialized shared file and should be returned for the
  serialization commit rather than made in-agent.

**Wave 4 — two scopes, parallel with each other.**

* `agent-context-scrub` — released once `planner-line-semantics` has landed.
* `content-scan-detectors` **+** `separator-detection` batched as one scope on
  the scanner, *if* `separator-detection` is accepted by then; otherwise
  `content-scan-detectors` alone.
  → **Ceremony 2: the frozen-file re-pin** for `content_scan.py`. Maintainer-only.

**Wave 5 — one scope.** `default-security-stance`, which needs
`_scaffold/config.py` free (after Ceremony 1) *and* `content-security.md` free
(after Wave 4) *and* stable scanner content for its parity test. It is last
because it depends on both ceremonies, not because it is least important — it
is the change that makes every other scope in this list reach an adopter by
default.

**Any time, off the critical path.** `release-security-bar` touches no code:
it opens a plan and adds a `dev/PLANNING.md` row defining the release bar. It
is worth landing *early* precisely because it is the bar the other waves are
measured against.

## What this note does not settle

* **Whether `separator-detection` is accepted.** Wave 4's shape depends on it.
  If it is still open when Wave 4 starts, `content-scan-detectors` goes alone
  and the scanner buys a second ceremony later — the avoidable cost this note
  exists to flag.
* **The two ceremonies.** Both are Maintainer-only and neither is schedulable
  by an agent.
* **Wave 1's archive preconditions**, which are a separate thread: `scan-coverage`
  owes four follow-ups a durable home, `byline-classification` waits on three
  Maintainer questions, and `release-authenticity` cannot archive until its
  Chunk M runs.

---

## Revision 2026-08-04 — what actually happened, and the collisions this note missed

Appended rather than rewritten: the note above was accurate when written and
is kept so the drift is visible.

**Waves 2 and 3 landed.** `fork-advisory-semantics` (`9bd6752`) and
`profile-parse-fail-open` (`e7394cb`) shipped sequentially as planned, and
**Ceremony 1** — the batched AST re-anchor — was run by the Maintainer and
recorded at `3852cf7`: 5 CHANGED, 1 MISSING (`Try`), baseline 174 → 173. The
union was formed from two **per-plan isolated** measurements, which is the part
worth carrying forward: a shared-tree measurement shows the union and cannot be
attributed, and one earlier attempt was contaminated by a sibling's hunk and had
to be retaken. `gate-claims-vs-enforcement` landed as five chunk commits
(`8d23afe`…`84fbef4`).

**Two collisions this note did not predict.**

1. **`dev/.cairn/cairn-lock.yml` is a shared surface, and it is *generated*.**
   `stage-commit-patterns` Chunk C and `planner-line-semantics` B4 both write
   it — the former by `upgrade --finalize`, which regenerates the file. Two
   concurrent runs do not merge, they clobber, and the loser's finalize is
   silently invalid. The collision map above tracks *principal* surfaces and
   missed it because neither plan's headline surface is the lockfile.
   **Lesson: a generated shared file is a harder collision than an edited one**,
   because the damage is invisible in a diff. Sequenced 2026-08-04:
   `stage-commit-patterns` first, `planner-line-semantics` behind it.
2. **The `_scaffold/config.py` cluster is five scopes, not two** —
   `profile-parse-fail-open`, `default-security-stance`, and the three Codex
   module-registration scopes (`api-web-security-modules`,
   `portable-security-sweeps`, `security-verification-activation`). The note's
   "five real collisions" list understated the fan-in on this one file.

**Two scopes exist that this note predates**, neither in any wave:

* **`review-gate-enforcement`** (proposal accepted `eb1b2b7`, plan open
  `8dfb664`) — the review-before-implement gate clears on the *presence* of a
  section, tier-blind. Surface: `tools/lifecycle_planner.py` + twin,
  `doctrine/plans.md`, both plan templates, the planner scaffold. **Collides
  with `planner-line-semantics`** on the same module and twin, so it sequences
  after it. Not startable yet: its own Response requires a settled record
  schema and a second External round first.
* **Class C** — six `upgrade`-family commands that write into an adopter tree
  without the `_assert_safe_write` containment guard. Assigned to
  `fork-advisory-semantics` by Maintainer ruling `a429530`, landing as
  additional chunks **after** that plan's current chunks commit. It touches
  `_scaffold/upgrade.py`, so it re-opens the Wave 2 surface and will need its
  own AST re-anchor accounting.

**Wave 4's open question is settled.** `separator-detection` is **accepted**, so
it batches with `content-scan-detectors` as one scope on the scanner and
Ceremony 2 is paid once — the avoidable cost this note flagged.

**Still true, and the note's most useful line:** `transition-lint` creates only
new files and collides with nothing by construction. It was startable at any
point and was started last, on 2026-08-04.
