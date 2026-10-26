# Code review (Internal) — C2+C3, constitution and replacement tools — Claude Sonnet 5 — 2026-08-27

**Reviewed commits**: `3a9f8cb`, `9f0c685`, `5be48c5`, `0a431a2`, `c54ddfd`, `2432bf8`, `73d3642`
**Target**: `AGENTS.md`, `dev/agent_collaboration.md`, `dev/proposals/_template.md`, `dev/plans/_template.md` and their four `templates/core/` twins (C2); `tools/board.py`, `tools/gauge.py`, `tools/audit_report.py` and `bootstrap/tests/test_replacement_tools.py` (C3)
**Prior findings**: none (fresh context)
**Model**: Claude Sonnet 5

**Verdict**: ACCEPT-WITH-FOLLOWUPS

C3 is clean: the three tools do what they claim, are exit-0/warn-only where claimed, and `classify()` genuinely returns `None` rather than bucketing. C2's own repair commit (`2432bf8`) correctly restored the ten contracts it found missing. But the repair was scoped to what `test_lifecycle_contract.py` and `test_scope_reduction_trap.py` happened to pin, and that scope missed real content — most seriously, an archive-time obligation this very plan depends on, and a currently-enforced coordination mechanism the rewritten `dev/agent_collaboration.md` no longer even points at. Neither is a reason to revert C2 or C3; both are reasons the plan should not treat C2 as closed on the strength of the ten-contract repair alone.

## Findings

### Finding 1 (blocking) — the plan template silently dropped the entire archive-precondition / "Lasting-truth migration" doctrine, and nothing enforces it any more

The pre-C2 `dev/plans/_template.md` (at `8c83c0c`) carried a `## Lasting-truth migration` section with four load-bearing rules: the archive gate checks *substance, not the label* (a `Dispositions:` line is mandatory, `Dispositions: none` is the only valid empty case); the exact `Dispositions:` commit-body grammar; the rule that the loop-fidelity sign-off must sit *inside* this section and name a commit id plus the governing contract section; and "an append re-opens the attestation" (adding to this section after archive-time re-triggers the substance check). C2's rewrite (`3a9f8cb`) dropped the entire section, in both the self-hosted template and the shipped `templates/core/dev/plans/_template.md` twin, and it was not among the ten contracts `2432bf8` restored.

Evidence:

```
$ grep -n "Dispositions:\|[Aa]rchive precondition\|Lasting-truth" \
    dev/plans/_template.md templates/core/dev/plans/_template.md
(no output — zero hits in either file)
```

The doctrine is not gone from the repo — `doctrine/plans.md:917` still carries the full `## Lasting-truth migration doctrine` section — but nothing in the rewritten template points there:

```
$ grep -n "doctrine/plans.md\|doctrine/" dev/plans/_template.md
(no output)
```

Nor does either session-routine skill mention it:

```
$ grep -n "Dispositions\|Lasting-truth\|archive precondition" \
    .agents/skills/session-end/SKILL.md .agents/skills/session-start/SKILL.md
(no output)
```

**This is not merely a documentation gap.** C6 (`bfe6bbf`, outside this review's range but establishing the current state of the tree) deleted the lifecycle planner tool (formerly at tools/lifecycle_planner.py, per the plan's own C6 row), which is where the archive-precondition check was presumably mechanically enforced; I found no successor:

```
$ grep -rln "archive.*precondition\|Dispositions:" scripts/*.py tools/*.py bootstrap/*.py
(no output)
```

So today, a plan author working *only* from `dev/plans/_template.md` has no way to learn that an archive-time `Dispositions:` attestation is required at all, and no tool will catch its absence. The only reason this plan (`dev/plans/subtraction-sweep.md`) still carries a correct `## Dispositions` block is that it was opened before C2 landed, under the old template. A plan opened after C2 would not know to add one.

**Fix**: restore at minimum a compact pointer in `dev/plans/_template.md` (and its shipped twin) naming the `Dispositions:` requirement and pointing at `doctrine/plans.md` > "Lasting-truth migration doctrine" for the full grammar — the same compression pattern C2 already used elsewhere (e.g. the Boundary B/C rules point at nothing external and are inlined; this one needs at least the pointer, since the mechanical backstop is gone).

### Finding 2 (blocking) — `dev/agent_collaboration.md`'s Coordination section no longer mentions the work-intent protocol it is actively enforcing

Pre-C2 (`8c83c0c`), the `## Coordination` section's `<!-- cairn:slot coordination-additions -->` block (filled, on the self-hosted side, with Cairn's own content) documented: the Tier-2 work-intent claim/release protocol via `tools/intent.py`; the required-signal-read rule for coordination-surface files; the tracked collision log at `dev/measurement/collision_log.md` and its role in the doctrine rate-limit gate; per-session coordination identity; and the goodnight intent-hygiene pruning step. C2's rewrite (`5be48c5`) removed the entire slot — both the marker and the content — from the self-hosted file, leaving only a generic "concurrent sessions are real, don't use a bare `git commit`" paragraph. It left zero pointer to `dev/modules/coordination-tiers.md`, which still carries the full doctrine and commands.

```
$ grep -n "coordination-tiers\|intent.py\|work-intent\|dev/modules/" dev/agent_collaboration.md
(no output)
```

This protocol is not dormant — it is live, right now, in this repository:

```
$ cat .git/hooks/pre-commit | head -4
#!/usr/bin/env bash
# >>> cairn/intent/pre-commit BEGIN
...
/Users/kendal30/conda_envs/miniforge3/bin/python3 .../tools/intent.py _precommit_check ...

$ ls -la dev/intents.jsonl dev/measurement/collision_log.md
-rw-r--r--  318819 Aug 25 17:11 dev/intents.jsonl
-rw-r--r--    2887 Aug 27 09:42 dev/measurement/collision_log.md
```

`dev/measurement/collision_log.md` is the untracked file sitting in this very session's `git status` output, with real recorded `work-intent-claim-conflict` events through this month. An agent onboarding purely from the rewritten `dev/agent_collaboration.md` would not learn this mechanism exists, would not know to run `python tools/intent.py claim` before touching a collision-prone surface, and would not know the collision log feeds the doctrine-change rate-limit gate. The shipped twin (`templates/core/dev/agent_collaboration.md`) is correctly unaffected — its `coordination-additions` slot placeholder is byte-identical before and after C2, since it never carried Cairn-specific content — so this finding is scoped to the self-hosted file only.

**Fix**: restore a short paragraph in the Coordination section naming that Cairn runs the Tier-2 protocol and pointing at `dev/modules/coordination-tiers.md` for the commands, the way every other installed module (interpreter binding, portable-sweep trust root) still gets a named mention in `AGENTS.md`'s high-risk-surfaces list even after compression.

### Finding 3 (non-blocking) — AGENTS.md dropped the concrete procedure for untracked lifecycle drafts at cold start

Pre-C2, AGENTS.md's git-workflow section said cold-start orientation checks `dev/proposals/`, `dev/plans/`, `dev/strategy/` for untracked drafts, and gave a three-way decision rule: commit one your own intent claim covers, leave one another agent's claim covers, surface an unclaimed one to the Maintainer. This is gone from both AGENTS.md and `dev/agent_collaboration.md`; `git status --short` is still surfaced by `tools/session.py session-start`, but the *decision procedure* for what to do about an untracked draft it reveals is not written anywhere I could find:

```
$ grep -n "untracked" AGENTS.md dev/agent_collaboration.md
AGENTS.md:156:  * **New / untracked files** -- `git add <paths> && git commit <paths>` ...
AGENTS.md:164:  leave it untracked for another agent to inherit. If you can't commit this
AGENTS.md:312:  the path it returns. This is an untracked, gitignored, ...
(none of these is the cold-start disposition procedure)
```

No test pins the old wording either (checked the last-surviving copy of `test_lifecycle_contract.py`, at `2432bf8`, before C6 deleted it: zero hits for "unclaimed" or "another agent's claim covers"). Given the current session's own instructions describe three other reviewers working concurrently on the same plan, this is exactly the scenario the dropped rule existed for.

**Fix**: restore the three-way disposition rule, in `dev/agent_collaboration.md`'s Coordination section (a natural neighbor to Finding 2's fix) or AGENTS.md's commit-workflow section.

### Finding 4 (non-blocking) — the proposal template's "Author-accounting" block (invariants / failure modes / edge cases) is gone; only the narrower security preflight survived

Pre-C2, `### Author-accounting -- invariants, failure modes, edge cases` required, for high-stakes changes: an invariants list with enforcers, a failure-mode inventory (closed vs. open), an edge-case inventory, a public-path-to-test mapping (as relative markdown links, so the link checker verifies the test exists), and a known-omissions line. C2 kept only the security-touching sub-block (S1-S5), restored correctly by `2432bf8` and pinned by `bootstrap/tests/test_scaffold.py::test_installed_templates_carry_security_preflight_questions`. The wider Author-accounting content — which applied to *any* high-stakes change, not just security-touching ones (e.g. a scientific-assumption change with no trust boundary) — has no replacement and no test:

```
$ grep -rln '"\*\*Model\*\*"\|Author-accounting\|Author accounting' bootstrap/tests/*.py
bootstrap/tests/test_scaffold.py   # only the S1-S5 sub-block, per its own docstring at :493-496:
  "It does not cover the whole `### Author-accounting` block that sub-block
   sits inside -- the wider dev/**/_template.md twin-parity gap ... stays
   open outside this sub-block, by design."
```

That docstring shows the test's author already knew this gap existed at test-authoring time; it was never closed. This is squarely the kind of content the plan's own C2-deviation section says is load-bearing ("the anti-narrowing floor... a scientific assumption... that can change reported results" is exactly what Author-accounting's invariant/edge-case inventory protected), yet it fell outside the scoped-mapping repair.

**Fix**: at minimum, note the cut explicitly as a deviation (per AGENTS.md's own rule that a reviewer cannot silently narrow doctrine by omission) rather than leaving it undocumented; ideally restore a compact version scoped to non-security high-stakes changes.

### Finding 5 (non-blocking) — the `**Model**` field is gone from every proposal/plan header, Review, and Response section

Pre-C2, every proposal/plan header, `## Review`, and `## Response` section opened with `**Model**: <your actual running model — query and state it; don't copy a label from an old template or archive>`. This is gone from all four rewritten templates, self-hosted and shipped, with no replacement:

```
$ grep -n '\*\*Model\*\*' dev/proposals/_template.md dev/plans/_template.md \
    templates/core/dev/proposals/_template.md templates/core/dev/plans/_template.md
(no output — zero hits in any of the four files)
```

Cairn's Dual-Review model is structurally defined by agent-type independence ("a different agent type, or a human" for External review). Without a structural prompt to record which model authored a review, that independence becomes unverifiable after the fact from the artifact alone — a reader has to trust the reviewer's self-identification in prose, if any. (Practice still runs ahead of the template: the plan-review section in `dev/plans/subtraction-sweep.md` and this very review both state a Model line by convention, not because the template asks for it.) Not pinned by any test.

**Fix**: restore the Model line, or explicitly decide it is no longer wanted and say why (the C2 deviation section does not mention this cut at all).

### Finding 6 (non-blocking) — `audit_report.py`'s five warning detectors are 4/5 untested on their "fires when absent" direction

The commit message for `c54ddfd` says: "The verification detector was confirmed in both directions before being trusted — it fires on a plan that genuinely lacks the section and stays quiet on one that has it." `bootstrap/tests/test_replacement_tools.py`'s `TestTheAuditReporterDetectsAbsenceForRealReasons` class has three tests, and none of them constructs a document missing `## Implementation verification` to check that the "no Implementation verification section" warning actually fires — the "fires" claim for *that* detector is untested. The same is true for the other three detectors:

* `risk_answer` (`_RISK_RE`) — every fixture in the test file includes `**Risk**: low`; no fixture omits it.
* `reviews` (`_REVIEW_RE`) — every fixture includes `## Plan review -- someone -- ...`; none omits it.
* `outcome_known` (`_OUTCOME_RE` / `_OUTCOMES`) — the one negative-adjacent test, `test_pending_is_an_accepted_outcome`, tests that `pending` is *correctly recognized*, not that an out-of-vocabulary status (e.g. `**Status**: purple`) triggers the warning.

Only `falsification_output` has its "fires on absence" direction directly pinned (`test_a_ledger_naming_no_numbers_is_flagged`). I read the source and confirmed all five detectors are implemented correctly today — this is not a claim the code is wrong, it is that 4 of 5 "fires correctly" properties rest on manual verification (per the commit message) rather than a committed regression test, so a future change that made any of the other four detectors permissive (e.g. a regex that always matches) would pass the suite silently.

```
$ python -m pytest bootstrap/tests/test_replacement_tools.py -v
... 15 passed in 0.07s
```
(all 15 pass; the gap is coverage breadth, not a failing test)

**Fix**: add one negative fixture per remaining detector (missing Risk line, missing review heading, unrecognized outcome value), mirroring the existing `falsification_output` pattern.

### Finding 7 (non-blocking) — none of the three tools' `main()` entry points, including `audit_report.py`'s core "cannot fail a run" exit-code claim, are tested

All 15 tests in `test_replacement_tools.py` call internal helpers (`_rows`, `_encode`, `classify`, `_sample`, `_facts`, `_warnings`) directly; none calls `board.main()`, `gauge.main()`, or `audit.main()`. In particular, `audit_report.py`'s central doctrinal claim — "warn-only... it blocks nothing... this exists to be read... not obeyed" — is an exit-code contract (`main()` always returns 0), and that contract has no regression test. I verified it holds today by reading the source (no `sys.exit` with a non-zero argument anywhere in the file) and by running it live:

```
$ python tools/audit_report.py > /dev/null 2>&1; echo $?
0
$ python tools/audit_report.py 2>&1 | tail -1
audit: 48 change(s), 28 with at least one warning. Advisory only -- nothing here blocks anything.
```

(That last line matches the C3 commit message's claimed figures exactly — "48 archived changes, 28 carrying at least one warning" — a good, positive, independently-reproduced check.) But nothing in the suite would catch a future change that turned a warning into a `sys.exit(1)`.

**Fix**: add a test that constructs a fixture with every detector triggered and asserts `audit_report.main([...])` still returns `0`.

## Steelman — what the sweep got right

* `tools/gauge.py::classify()` genuinely returns `None` for an unmatched path rather than defaulting to any bucket (`tools/gauge.py:89-94`), confirmed by source read, by `test_an_unknown_path_is_unclassified_not_product`, and by a live run over the last four weeks that reports "every touched path is classified" with zero silent absorption.
* `tools/board.py` genuinely computes no judgment: it parses `**Field**: value` lines above the first `##` heading and nothing else (`tools/board.py:65-74`); a field the artifact doesn't carry comes back empty rather than inferred, directly pinned by `test_it_reports_only_fields_the_author_wrote`. It borrows `encode_display` from `tools/session.py` rather than a second escape table, confirmed by reading both files — `session.py` has no module-level side effects that a dynamic `importlib` load of it could trigger unexpectedly.
* `2432bf8`'s repair is accurate: I independently confirmed the ten restored items are present, verbatim, in all affected files (Boundary B full-fallback clause and its six fresh-run triggers, the `doctrine/rationale.md` pointer, the `**Plan review**:` metadata line, the S1-S5 security preflight with its exact heading shape, and the Boundary C targeted-falsification triggers in both plan templates). The one *real defect* it fixed — Cairn's own hard-coded commands (`bootstrap/tests`, `Python 3.13.x`) leaking into the adopter-facing `templates/core/AGENTS.md` — is genuinely gone; I diffed the current shipped and self-hosted AGENTS.md files and confirmed the shipped copy now says "configured full suite" / "configured interpreter/runtime" throughout, with zero remaining Cairn-specific command strings.
* The `templates/core/` twins are deliberately non-identical in the way C2's commits claim: spot-checking `AGENTS.md`, the shipped twin correctly swaps Cairn's `## project-overview` prose for an unfilled adopter slot, keeps the doctrine-reference-resolution explanation (needed by every adopter), and drops nothing that both files should share structurally.
* C3's build-table probes reproduce exactly as claimed: `tools/board.py` lists 4 active artifacts (matching the plan's "4 today"); `tools/gauge.py` reproduces the claimed shape (single-digit product share climbing to 7% in the most recent week); `tools/audit_report.py` reproduces "48 archived changes, 28 with at least one warning" exactly.

## What I could not reach

* I did not review C1, C4, C5/C6, C7, C8, or C9 — out of scope for this pass, and I relied on the plan's own text (not independent verification) for what C6 removed (the lifecycle planner tool) as context for Findings 1 and 2.
* I did not audit every one of the ~80 remaining `<!-- cairn:slot -->` markers across the eight files for correct pairing/balance beyond the ones the plan's own commit messages already claim were counted (5/5 and 3/3 slot markers, if/endif balance) — I spot-checked `coordination-additions`, `role-roster-additions`, `reflections`, and `assurance-path-triggers` on the shipped twins and found them consistent, but did not mechanically verify the full set.
* I did not diff `dev/proposals/_template.md` and `dev/plans/_template.md` against `doctrine/proposals.md` / `doctrine/plans.md` line-by-line to find every other place a pointer might have quietly become a dead end (I found the two cases in Findings 1 and 5 by following specific threads, not by an exhaustive pass).
* I did not run the full test suite (`CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests`) myself; I relied on the plan's own Boundary B record for C7 (`b1e655d`, dated 2026-08-27) as evidence the suite was green at a nearby commit, and ran only the targeted tests and tools cited above.
* I did not verify whether Finding 1's or Finding 2's gaps are already known to the plan author outside the plan text itself (e.g. in a session not yet committed) — I checked only the committed record.
* I ran `claim_check.py` over this review file before committing; it reported clean.
