<!-- cairn-internal-ref-allow: doctrine/coordination.md doctrine/session-routines.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
# Next-session candidates — Cairn

`NEXT_SESSION.md` carries the **cold-pickup handoff**: the
recommended next task and a queue of candidates, each with enough
context — file paths, scope, effort, payoff, risks — to begin
without the prior session's conversation.

It complements `PLANNING.md`: `PLANNING.md` says *what* is queued;
`NEXT_SESSION.md` says *how to actually pick it up*.

`NEXT_SESSION.md` is **rewritten from scratch** by the full-
handoff owner at each goodnight — the physical action is "open
a blank file and write," not "edit the previous version."
Anything in the previous goodnight's version that does not
earn its place in the next session's orientation is dropped;
durable claims migrate to their proper home (doctrine, the
roadmap, a proposal) **before** the rewrite. See
`doctrine/session-routines.md` > "The next-session starting
plan: written from scratch each goodnight" for the load-bearing
reasoning.

The required-signal-read discipline on shared communication
files applies (`doctrine/coordination.md` > "Required
signal+read for coordination-surface files").

## Recommended starting point

<!-- cairn:slot next-start -->
**Task + current state.** Open the plan for **`stage-commit-patterns`** (accepted
2026-07-22, awaiting plan-open) and implement it. It is the last accepted
proposal with adopter-facing value still unimplemented, and it is small: the
audit is already done, so Part 1 is transcription rather than investigation.

*What it fixes:* `_STAGE_COMMIT_PATTERNS` in
`templates/modules/default-on/_lifecycle_metrics/gitmeta.py` maps commit
subjects to lifecycle stages. It ships **default-on in every adopter tree** and
matches **zero of 76** real commit subjects — so every stage-timing metric is
empty and `stage_timestamp_reliability` reads `Best-effort` on 100% of rows,
while the tool exits 0 and emits a well-formed report. The vocabulary was never
Cairn's: an invented grammar validated only against Cairn's own toy examples.

*Three ratified plan conditions* (from the Decision — do not re-derive them):
1. **Scoped `upgrade --finalize`** for `gitmeta.py` and its `__init__.py` twin.
   This is mandatory, not optional: the lockfile was finalized at `41875e4`, so
   leaving these records stale now *creates* a fresh mismatch and re-reds
   `verify_integrity`. (The External review advised the opposite, correctly, on
   a tree where 41 entries were already stale — that premise is dead.)
2. **Template + installed-copy byte-parity** across both file pairs.
3. **No AST re-anchor** — nothing under `bootstrap/_scaffold/` is touched.

**Standing directions that order everything** (Maintainer, 2026-07-22):
*postdoc-first* (does it affect the first external adopter's first two weeks?)
and *fix defects, build nothing new* (any new tool or mechanism needs an
explicit go-ahead, however well it reviews).

**Roles to instantiate.** Implementation for the plan; the Human Maintainer for
the Decision on anything new. A fresh-context reader for the plan review
(`required(Internal)`).

**Agent-dispatch tier.** Medium — the design is settled and the audit is done;
this is careful mechanical work plus its tests.

**Reading order.** `AGENTS.md` → this file → `dev/PLANNING.md` (Where the
project stands) → the accepted proposal `2026-07-22-claude-stage-commit-patterns`
(read its **Revised proposal** and **Decision** first; they supersede the
original design).

**First three concrete steps.** (1) `python3 tools/lifecycle.py session-start`
to orient and heal the skills fan-out. (2) Open the plan (which archives the
proposal) and get its Internal plan-review. (3) Implement, transcribing the
verified 28-symbol table rather than re-auditing.

**Environment, non-negotiable.** Run the suite under the **canonical
interpreter, Python 3.13.x** — on this machine `~/conda_envs/lhm/bin/python`.
A different minor produces hundreds of *spurious* AST mismatches and silently
skips `bandit`. Name the interpreter alongside any suite figure you assert.
See `bootstrap/DEPENDENCY_BUDGET.md` > "The canonical interpreter". The suite
is currently **fully green: 1446 passed, 0 failed, 0 skipped**.
<!-- cairn:end next-start -->

## Other candidates

Smaller, pickable-cold tasks, each with the context to start it.

* **`transition-lint`** *(accepted, queued, explicitly not next)* — an advisory
  check that a commit's message claim is supported by its diff. Accepted
  2026-07-22 as the explicit go-ahead the build-nothing-new rule requires, but
  recorded **queued, not next**: it is maintainer-facing apparatus and the
  standing priority is postdoc-first. Its plan conditions are ratified in the
  Decision (rename-awareness via `-M`, trigger narrowed to
  `dev/proposals/`|`dev/plans/`, exception vocabulary bounded to restating
  `AGENTS.md`'s carve-in, advisory = always exit 0, no silent-clean on an
  unresolvable rev-range). Do not start this ahead of adopter-path work.

* **Verify the claude-code skills path** *(small, and it closes a real
  evidence gap)* — `.claude/skills -> ../.agents/skills` was created this
  session and both `SKILL.md` files are well-formed, but the Maintainer
  reported the skills not appearing in their list. Unresolved whether that is
  discovery-at-startup or `disable-model-invocation: true` behaving as
  documented. **Either answer is worth recording**: `docs/skills-compatibility.md`
  currently rates every harness `native-claimed-unverified` — zero verified
  targets — and the fixture protocol's promotion transcript has never been
  written. This is the cheapest available move from "claimed" to "tested".

* **`.claude/` is untracked and not gitignored** *(tree hygiene, Maintainer's
  call)* — it now holds the skills symlink plus harness `worktrees`. Not
  gitignored unilaterally this session because `.gitignore` is a shared
  surface.

* **Cite lifecycle artifacts by filename stem, not path** *(recurring defect,
  two counted instances)* — `AGENTS.md`'s shared-communication-file rule
  already mandates stems for the boards precisely so an archive-move needs no
  edit; proposals do not inherit that protection. Two live proposals had path
  citations broken by legitimate archive-moves this session, each needing
  claim-marker maintenance. Cheap to state; would prevent a recurring class.

* **The 0.4 gates remain outstanding** — the R-H third-party correctness probe
  (blocked on enrolling a third party, and with no in-tree protocol), and the
  standing pre-release sweep, which has no v0.4 instance. Both are launch-path,
  not postdoc-path.
