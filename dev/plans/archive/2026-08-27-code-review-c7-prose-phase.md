# Code review (Internal) — C7, the prose phase — Claude Sonnet 5 — 2026-08-27

**Reviewed range**: `6cbea39` through `b1e655d` (the nine C7 commits named in the
brief), read against `dev/plans/subtraction-sweep.md` at current `HEAD`
(`610f521`) and against the live tree at `HEAD`.

**Verdict**: ACCEPT-WITH-FOLLOWUPS

No blocking findings. I spot-checked a broad sample of the bankruptcy pass's
dead-row and folded-row claims, independently tested all three checker
falsifier clauses and the config's fail-toward-strict property in a scratch
copy, verified the two directive families are in the state the scope delta
claims, and reproduced `check_cairn.py` and `quality_gate.py` myself against
the exact figures the plan's Boundary B record cites. Everything I could
verify checked out. I found two real, evidence-backed defects, both narrow and
non-blocking — one a bookkeeping gap in the plan's own accounting record, one
a content error left behind by a mechanically-clean repair.

## Findings

### Finding 1 (non-blocking) — one of the "twelve security-cluster rows" the plan says it folded is neither folded with content nor listed as dead

**What is wrong.** `dev/plans/subtraction-sweep.md`'s "Second pass" section
(the `39e05fa` account) states: *"Queued held twelve security-cluster rows...
four `[SEC]`, plus `[TRU-1]`x2, `[TRU-4]`, `[TRU-5]`, `[TRU-7]`, `[BND-6]`,
`[REL-6]` and `[REC]`... Folded 2026-08-27 into the register with the rest;
one (`[TRU-7]`...) was a duplicate... needed no content."* That accounts for
12 rows as 11-folded-with-content + 1-duplicate. It does not hold up for one
of the four `[SEC]` rows.

**Evidence.** `git show 39e05fa -- dev/PLANNING.md` shows exactly four rows
starting `* **[SEC]`:
1. `M2 conflates "review" with "produce"...` → present in the register as
   `[REC] A second clearing review manufactures a competing authority pair`
   (`dev/strategy/2026-08-05-codex-security-strategy.md:1103`). Matches.
2. `The lockfile has no regeneration procedure...` → present as
   `[TRU-1] There is no command that regenerates an existing lockfile`
   (`:805`). Matches, same test name and same script-at-`77d2b3b` detail.
3. `~~Two install-contract artifacts are stale after the tag pass~~ —
   RESOLVED 2026-08-19 at 77d2b3b` (gate-manifest 35 stale frozen entries,
   `run_portable_security_sweeps.py` lockfile-digest mismatch) → **not found**.
   I grepped the register for `35 frozen`, `173 baselined symbols`,
   `install-contract artifacts`, `77d2b3b` — zero hits for this row's content.
4. `The interpreter-binding re-pin at c29ead3 — REPRODUCTION CONFIRMED...` →
   present as `[TRU-5] The interpreter-binding re-pin: reproduction
   confirmed...` (`:998`). Matches.

Row 3 is also **not** the row the plan's separate "seven more Queued rows were
dead or closed" list names as its seventh item — that seventh is a
**different**, `[VER]`-tagged row (`* **[VER] ~~The AST attestation baseline
needs re-anchoring after the tag pass~~ — CLOSED 2026-08-20...`, at line 191 of
the same diff), confirmed by its distinctive "CLOSED 2026-08-20" wording
matching the plan's own phrase exactly, versus row 3's "RESOLVED 2026-08-19".
Two separate rows about the same `77d2b3b` ceremony, and only one of them is
accounted for anywhere in the plan's bankruptcy record.

**Why this is not a live-thing-dropped-as-dead hazard.** Row 3's resolved
finding (the stale-fixture reconciliation) is genuinely historical — it was
fixed at `77d2b3b`, same as the AST-baseline row that *is* accounted for. Its
one live remainder — *"who regenerates the manifest and re-records the
lockfile, and under what review"* — is the same open question the folded
`[TRU-1]` entry (row 2) already carries, and the plan's own later "C8 state,
measured 2026-08-27" section cites exactly that `[TRU-1]` entry as the live
blocker on the lockfile leg. So nothing live was actually lost. But the
plan's own arithmetic ("eleven folded with content + one duplicate = twelve")
does not enumerate to twelve when checked against the tree, and this row's
specific fate is not stated anywhere the way `[TRU-7]`'s is.

**Fix.** A one-line addition to either the "Second pass" section or the "seven
more" table, naming row 3 explicitly as subsumed by `[TRU-1]` (or as an eighth
dead/closed row), so the count is reconstructible without independently
re-deriving it the way I had to.

### Finding 2 (non-blocking) — a prose repair left a shipped doctrine link pointing at an unrelated file

**What is wrong.** `doctrine/session-routines.md:417` (post-`6cbea39`) reads:

```
The trackers feed the rate-limit gate; the
[`lifecycle-metrics`](../README.md)
module's eventual cross-adopter harvest correlates across them.
```

The link target `../README.md` resolves from `doctrine/` to the repository's
top-level `README.md` — which does not mention `lifecycle-metrics` or
"cross-adopter harvest" anywhere (`grep -n "lifecycle-metrics\|cross-adopter\|harvest" README.md` returns nothing). Before this repair the link pointed at
`../templates/modules/default-on/lifecycle-metrics.md`, the module's own doc —
which this sweep's own scope delta ("the lifecycle-metrics module is
removed") deleted. The repair swapped a dead target for a live-but-wrong one:
the link now resolves (so `link_check`/`check_cairn` are silent on it) while
pointing a reader who follows "lifecycle-metrics" at the repo's front-door
README, which says nothing about the subject. The sentence itself is also
stale: it still describes the module's "eventual... harvest" in the present
tense, when the module the sentence is about no longer exists in the tree at
all (confirmed above: templates/modules/default-on/_lifecycle_metrics/parse.py
does not resolve).

**Why this is worth flagging rather than a nitpick.** It is the mechanical
inverse of the exact hazard I was briefed to hunt for in the checker itself:
a check that passes while the thing it is supposed to guarantee is false. This
one slipped through both `link_check` (target exists) and `claim_check`
(markdown-link syntax, not a bare backtick token, so out of that checker's
scope) — genuinely undetectable by either gate, which is exactly why a human
read matters here. It is also the **only** instance of this pattern in the
commit: I read the full diff of `6cbea39` (14 changed prose files) and every
other repair of the same kind (`the retired fold-back doctrine`, `an issue on
Cairn's tracker`, `a module doc`, `tools/session.py` for `tools/lifecycle.py`,
`archive/2026-08-20-...` for the archived sibling) either de-linked to plain
text or correctly repointed at a still-existing file. This one row is the
outlier.

**Fix.** Either strip the markdown-link syntax the way every sibling repair in
the same commit did (`` `lifecycle-metrics` `` module's eventual cross-adopter
harvest...`), or — better, since the module is not "eventual" but gone —
revise the sentence to match the C6 scope delta the way the `doctrine/onboarding.md`
fold-back-trigger row in this same commit did (*"the ledger is retired
upstream; this trigger fires only where an adopter still keeps one"*).

## What I verified and confirmed correct

Recorded so a later reader does not have to re-derive what was already
checked, and so the two findings above are read in proportion to how much of
the pass held up.

**Dead-row spot checks (bankruptcy record), each independently re-measured,
not re-read:**
* Preflight R3's trigger (`transition_lint.py`) — file gone.
* Preflight R5's `Author-accounting` sub-block — zero hits in `templates/`.
* Preflight R6's `_has_kind` — survives only in `scripts/gen_legacy_passes.py`
  (a one-off generator); every other hit is inside `dev/plans/archive/` or
  `dev/proposals/archive/`.
* `_gitignore_status` — zero hits tree-wide except the dead-row citation
  itself.
* `_agent_of` — hits only in `CHANGELOG.md` and archived plans/proposals.
* templates/modules/default-on/_lifecycle_metrics/parse.py,
  bootstrap/tests/test_lifecycle_contract.py, tools/lifecycle_planner.py —
  all confirmed gone from the tree.
* The four byline-classification rows — `_fold_word` has zero hits outside
  `dev/` (and even the `dev/` hits are all inside archived plans/proposals);
  `agent-identities.json` no longer exists anywhere in the tree (`find`
  returns nothing) and its only remaining mention is historical, in
  `CHANGELOG.md`. `IdentityModel` and `independent_review` both zero hits
  outside `dev/`; `human_maintainers`' only non-archived mention is
  `CHANGELOG.md`.
* SP8-9's `--include-archive` scan mode — the only tree-wide hits are inside
  archived plans/proposals or the sweep plan's own citation;
  `test_loop_fidelity_gate.py` (the surviving, separate gate) is confirmed to
  still exist and is unrelated to the deleted mode.

**Folded-row spot checks, each confirmed present in the register with a
revival trigger intact:** `[TRU-5]` gate-reanchor trusted-contributor posture;
`[TRU-5]` interpreter-binding re-pin (correctly re-measured, not
transcribed — the register states the digest pin itself is now gone, which I
independently confirmed: `_INTERPRETER_SYMBOL_DIGESTS` has zero tree-wide
hits); `[REC-1]` byline classifier finding, with its "six ratified residuals
lose their subject" framing and its measured evidence (`IdentityModel`,
`independent_review`, `human_maintainers`, `agent-identities.json` — all
re-verified by me directly, not taken on the register's word); `[TRU-1]` "no
command regenerates an existing lockfile"; `[TRU-7]` gate-anchor-unpublished
row, confirmed to genuinely mirror an already-existing entry rather than being
a hidden drop.

**Checker de-scope falsifiers, tested directly in a scratch copy
(`rsync`-cloned tree, `--root` override), not read off the plan's prose:**
* **Archived file draws no flag by default.**
  `claim_check.py dev/plans/archive/byline-classification.md --root .` →
  `archived source, not checked`, exit 0.
* **`--include-archives` still catches real breakage**, proving a scope
  decision rather than a disabled checker — same file, same flag added →
  47 hard flags, exit 1 (tools/lifecycle_planner.py,
  dev/.cairn/agent-identities.json, etc., all genuinely unresolved).
* **Prose files carry zero checker boilerplate.**
  `grep -rln "^<!-- claim-check-allow:" --include="*.md" .` — zero hits
  tree-wide, live or archived (the family was fully retired from in-body
  comments).
* **Family separation matches the scope delta exactly.** `claim-check-allow`
  directives: 0 remaining anywhere as inline comments (all moved to the
  config). `cairn-internal-ref-allow` directives: 40 files still carry them
  inline outside `archive/`, and the config JSON contains zero
  `cairn-internal-ref-allow` keys — confirming only one family moved, as the
  scope delta claims.

**Config fail-toward-strict, tested by deliberately breaking a scratch copy
five ways** (missing file, malformed JSON, wrong top-level shape, missing
`"exemptions"` key, unreadable/permission-denied): every one of the five
produced **zero exemptions**, a **stricter** result than the valid-config
baseline (0 hard flags → 40 hard flags on the same document), and a non-zero
exit code; four of the five also announced the failure on stderr (the fifth,
a genuinely missing file, is documented in the function's own docstring as
the one silent case, by design, and I confirm the code matches that
documentation). This matches
`bootstrap/tests/test_claim_check_allow_config.py::TestTheConfigIsWhereExemptionsLive`,
which I also ran directly (part of the 125-test run below) and which
independently exercises the malformed-JSON case against a real temp config.

**Reproduced the plan's own Boundary B figures myself, not trusted from the
record:**
* `python scripts/check_cairn.py` → 2 issues, both the pre-existing
  bare-`` `1` `` footnote links in
  `dev/proposals/2026-08-20-claude-scanner-claim-scope.md`, confirmed present
  at `ea3d649~1` (before C7 began).
* `python scripts/quality_gate.py --sub neutrality --sub redundancy` →
  neutrality fail=79 info=21, redundancy fail=0 — matches the plan's
  Implementation-verification record exactly.
* Targeted suite: `test_claim_check_allow_config.py`, `test_claim_check_module.py`,
  `test_check_cairn_content.py`, `test_check_cairn_counts.py`,
  `test_link_check_exclusions.py`, `test_gate_manifest.py` → **125 passed**,
  0 failed. `test_ast_attest.py` → **29 passed** (the plan's own C7-time record
  showed 2 failing here as pre-existing AST-baseline debt; it is clean now,
  consistent with the Maintainer's re-anchor the plan says happened at C8,
  after C7's own scope closed).

**Prose-repair spot checks beyond Finding 2, all confirmed correct:**
onboarding templates (`templates/onboarding/*.md`, `dev/modules/onboarding/*.md`)
no longer invoke `tools/lifecycle.py`; `docs/tool-usage.md` points at
`tools/board.py` in place of the deleted `lifecycle_metrics.py` reference;
both `.github/*/foldback.md` templates now correctly describe the affirmation
as the whole export boundary rather than instructing a scrub that cannot run.

Given all of the above, and that the two real defects found are both narrow,
self-contained, and do not touch any live commitment, contract surface, or
test — I do not believe either rises to blocking.

## What I could not reach

* I did not read `dev/strategy/2026-08-05-codex-security-strategy.md`'s Live
  residual register end to end at the same depth I gave the rows I spot-checked
  — I sampled roughly a dozen of the ~75 folded rows plus the 12 second-pass
  rows, not all of them. A systematic pass over the remaining ~60 is possible
  but was not performed.
* I did not independently re-verify every one of the 21 dead rows in the C7
  bankruptcy record — I checked roughly half, chosen to span both passes
  (Security-cluster routing and Queued) and both failure directions (a
  genuinely-gone subject vs. a mis-filed row). The unchecked remainder is
  plausible by the same method but not independently confirmed by me.
* I did not run the full `CAIRN_FULL_SUITE=1 pytest bootstrap/tests` suite
  myself (the plan's own record already has a clean, recent full run at
  `b1e655d` with the delta accounted for; per `AGENTS.md`'s verification
  boundaries, my job is to falsify that record with targeted probes, not
  re-run its broad command, and my targeted runs found nothing to falsify).
  If a future reviewer has reason to distrust that record specifically, a
  fresh full run is still owed independently of this review.
* I did not review `link-check-allow`'s fold-in against its own four stated
  falsifiers in depth (Note 2 of the plan-review pass flagged this as a real,
  if non-blocking, gap in the accepted design) — out of this review's
  explicit brief, which named the `claim-check-allow` /
  `cairn-internal-ref-allow` split as the pair to verify.
* I did not review C8 or C9 content — out of scope for C7, and both are
  explicitly unexecuted per the plan's own "Still owed before this plan can
  archive" section.
