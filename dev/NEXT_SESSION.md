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
**Task + current state.** **Answer the three Maintainer calls that unblock all
Wave 1 archival**, then repair Wave 2. Nothing is pushed. Wave 2's
implementation sits **uncommitted** in the working tree (11 files) because both
halves returned DEFECTIVE; everything else from the overnight run is committed.

**Why this first.** Three calls unblock every archive precondition on the
board, and none of them is expertise-gated — they are scope and ceremony
scheduling, not security analysis.

1. **`release-authenticity` Chunk M.** Needs your signing key. The control is
   **documented and tested but NOT established** until the cold bootstrap run
   passes against a pushed tag. Its Decision also carries a flagged condition —
   *"a scoped External round for the tag-substitution fix"* — which the Gemini
   Flash plan review arguably already is; strike or confirm it.
2. **`byline-classification`'s three Maintainer questions.** The only thing
   between that plan and archive. Its `[I7b]` obligation discharged itself when
   `planner-line-semantics`'s Response retracted the claim it was owed.
3. **`scan-coverage`'s four follow-up homes** — the struck registry census, the
   four `B607` findings, the unguarded monotonicity claim, the stale frozen
   pins. Mechanical, and mine; deferred only because archival was held for you.

**Then Wave 2's five blocking findings** (§ *Wave 2* below), then Ceremony 1.

**Effort.** Calls: minutes. Wave 2 repair: one focused round. Ceremony 1:
yours, after the repair.

## Wave 2 — what must be fixed before it commits

**`fork-advisory-semantics`** — three blocking:
* `bootstrap/UPGRADE.md` asserts *"Nothing your lockfile records — not `hash`,
  not `base_hash`, not a record's `src` — can decide that a facade is clean."*
  **Demonstrated false by execution:** a genuinely forked facade whose record
  sets `hash == base_hash` returns `[]`.
* Node 13's docstring claims a containment half it never asserts.
* **`bootstrap/_scaffold/upgrade.py` carries a hunk belonging to the batched
  sibling**, self-labelled `(profile-parse-fail-open Chunk A)`. A path-scoped
  commit would carry it silently. Fix before any commit.
* Consequence for Ceremony 1: the isolation claim *"the sibling's edits absent
  by construction"* is **false** — the copied `upgrade.py` carried the sibling
  hunk, so the per-plan AST measurement handed over for the union is
  contaminated and must be retaken.

**`profile-parse-fail-open`** — two blocking:
* **Unicode-whitespace hole.** `_minimal_yaml_parse` uses `line.strip()`, which
  removes *every* `str.isspace()` character; YAML's whitespace is only SPACE
  and TAB, and `_PROFILE_CONTROL_RE` covers C0/C1/`U+2028`/`U+2029`/`U+FEFF`
  but not `U+00A0`, `U+2000`–`U+200A`, `U+3000`. Four measured inputs return a
  value **not equal** to `yaml.safe_load`'s and **do not raise** — the third
  outcome the contract denies. The sharpest is an NBSP-prefixed key, read as
  `project_name` by the recognizer and `'\xa0project_name'` by PyYAML: exactly
  Maintainer Amendment 2's own sentence, with a character ordinary copy-paste
  produces. No test exercises Unicode whitespace.
* Gate-manifest delta under-reported: `_gate_manifest.py verify --no-collect`
  **structurally cannot** report collection classes, so a `COLLECTION-DROPPED`
  entry (the E1 rename) went unreported into a pre-recorded ceremony
  accounting. Run **with** collection: HOLD is 17, not 10.

Its auditor ran **18 hazard mutations** (13 claimed plus 5 unpriced, hunting a
predicted third case of test theatre) and all went RED — **no theatre found**.
The new module is genuinely non-vacuous.

## Decisions still yours, beyond the three above

* **Ceremony 1** — the batched engine AST re-anchor. The union must be formed
  by you from **per-plan isolated** measurements; see the contamination note.
* **Ceremony 2** — the `content_scan.py` frozen re-pin. `content-scan-detectors`
  and `separator-detection` share the file; batch them, or buy two ceremonies.
* **`identity-not-name` condition 3.** `fork-advisory-semantics` Chunk B **did
  not execute** — its fence requires a Maintainer amendment that does not
  exist, so the destructive remediation advice in `format_forked_facade_warning`
  is unchanged. Correct restraint by the implementer; the call is yours.
* **The `tools/lifecycle.py` lockfile row convention.** `agent-context-scrub`
  A4 says re-record `hash` **and** `base_hash`; `byline-classification` set the
  precedent of `hash` only. Verified to be convention, not correctness — settle
  by measurement (pick whichever adds no `verify_integrity` line).
* **The eight remaining escalated findings** — three on `byline-classification`,
  five on `agent-context-scrub`. Unchanged.

## Other candidates

* **External reviews on the twelve open plans.** Every Internal round states in
  its own first paragraph that it does **not** discharge the declared tier.
  This is the largest single block of remaining work.
* **The tier-blind plan-review gate.** `_has_kind(art, "Plan review")` is
  presence-only: `##`, `###` and an *empty* heading all satisfy it, and nothing
  reads `required(External)`. So a plan declaring External is cleared to
  implement by an Internal review that disclaims discharging it. Routed to
  `gate-claims-vs-enforcement`, which owns the file. One reviewer already
  worked around it deliberately by filing under `##`.
* **Update the sequencing note.**
  `dev/strategy/archive/2026-08-03-claude-security-wave-sequencing.md` was written when
  the `bootstrap/_scaffold/config.py` cluster looked like two scopes. It is
  **five**: `profile-parse-fail-open`, `default-security-stance`, and the three
  Codex module-registration scopes.

## The pattern worth carrying forward

*The artifact under verification must not supply the material used to verify
it.* **Seven instances** in this cycle: the anti-drift test whose expected set
*was* the code's object (green 63 days); `scan-coverage`'s exclusion latch; the
security test whose unsigned-tag fixture defeated its own oracle;
`content-scan-detectors`' token sweep drawn from the record's own sets;
`transition-lint`'s `B15` quantified over the author's own fixtures;
`stage-commit-patterns`' probes, all unscoped so the scope gate dismissed them
by construction; and the "isolated" AST worktree that carried the sibling's
hunk.

Reviewers now name it explicitly. Asking *"what supplies the material this
check runs on?"* has been the highest-yield question in the cycle.

## State

* **12 plans open**, each with an Internal review; none discharges its tier.
* **Wave 1 committed and green** — `b93f8e9`, `5c91c23`, `1dabe4d`, `cc74385`.
* Last clean suite: **1710 passed / 0 failed** at `cc74385`. Current dirty
  tree: **1779 passed / 2 failed**, both the priced `test_ast_attest` nodes.
* **Nothing pushed.**
