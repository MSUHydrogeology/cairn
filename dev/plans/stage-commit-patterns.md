<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/dual-review.md doctrine/proposals.md doctrine/lifecycle.md doctrine/rationale.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- One deliberate forward reference: bootstrap/tests/test_lifecycle_stage_patterns.py is the
     behavioural test this plan creates in Chunk A. It is registered under `Proposed paths:`
     below and named repeatedly outside that block, so it is exempted here as well. -->
<!-- claim-check-allow: bootstrap/tests/test_lifecycle_stage_patterns.py -->
<!-- claim-marker maintenance 2026-08-04: `dev/plans:` below is a COMMIT-SUBJECT PREFIX
     LITERAL -- the area prefix in Cairn's subject grammar, which is exactly the token this
     plan's repaired reader must DECLINE to classify -- not a path reference. The real
     directory is `dev/plans/` with a trailing slash. Every occurrence is a quoted subject
     string inside a test vector or a measurement table. Typo guard applied: checked one by
     one, none is a mistyped path. Same treatment, same reason, as the source proposal's own
     marker. Surfaced, not silenced. -->
<!-- One further deliberate forward reference: `scripts/transition_lint.py` is the SIBLING
     proposal's proposed path, cited here once inside the scope fence solely to record that
     this plan does not build it. -->
<!-- claim-check-allow: dev/plans:, scripts/transition_lint.py -->

# Plan: the shipped lifecycle-stage commit vocabulary reads nothing — repair the reader

**Source proposal**: `stage-commit-patterns` (stem
`2026-07-22-claude-stage-commit-patterns`, accepted 2026-07-22 by Maintainer
Decision, *"as revised"*). It currently sits under `dev/proposals/` and moves to
`dev/proposals/archive/` when this plan opens. **All `proposal :<n>` line
citations below are into that file and stay valid across the move**: a proposal
is append-only, so a section's line numbers never shift once committed.
**Status**: open
**Plan review**: required(Internal) — the tier the proposal declared, the Internal
panel concurred with, and the Decision ratified under *"OQ3 — the plan-review
tier stays `required(Internal)`."* The review carries an **execution** obligation,
not a reading one; see `## Plan review — the brief`. **No implementation commit
lands before a `### Plan review -- <reviewer> -- YYYY-MM-DD` sub-heading is in the
tree.**
**Last update**: 2026-08-04
**Opened**: 2026-08-04

## Source proposal

`stage-commit-patterns` settles one thing: **`_STAGE_COMMIT_PATTERNS` in a
default-on shipped module matched zero of Cairn's real commit subjects, so every
stage-timing metric came back empty at `Best-effort` while the tool exited 0 —
and the repair must narrow rather than widen, so that no commit is ever
mislabelled at `Exact`.** The plan executes that decision and does not
re-litigate it.

The proposal went through an Internal three-lens fresh-context panel (twelve
findings, R1 blocking), an author Response plus a `## Revised proposal` that
**redesigned P1 from an edit-the-vocabulary repair into an additive,
scope-gated one**, a Gemini External round (SHIP, five verifications, all
re-executed on the canonical interpreter), and an author Response to that round
which **inverted the External's lockfile advice** because OQ1 resolved between
the review and the Response. The Decision accepted it as revised and ratified
four plan conditions.

**Where the original `## Proposal` and the `## Revised proposal` disagree, the
revision wins; where the revision and the `## Decision` disagree, the Decision
wins.** Three places this actually bites, all carried below:

1. **P1 is additive.** `_STAGE_COMMIT_PATTERNS` is **not edited** — not its
   name, type, priority order, four regexes, or the `sharpening` exclusion. The
   original P1 replaced all four. The revision adds a second, scope-gated
   vocabulary consulted only when the shipped one declines.
2. **No bare-subject fallback.** An un-scoped subject sees the shipped patterns
   and nothing else. The Decision states the ground in terms: a bare fallback
   "would mislabel ordinary commits as lifecycle transitions and report the
   wrong timestamps as `Exact`, where today's all-`Best-effort` at least tells
   the truth."
3. **The scoped lockfile finalize is mandatory.** The External review advised
   leaving the lockfile alone; that advice was correct on a tree with 41 stale
   records and became wrong when they were finalized. The Decision converts it
   into a binding plan condition.

## Proposed paths

Proposed paths:
- `bootstrap/tests/test_lifecycle_stage_patterns.py` — the behavioural test for the repaired vocabulary; lands in Chunk A.

## Scope

This plan lands the accepted repair in four commits: the classifier and its
behavioural test (P1 + P2), the degradation-docstring correction (P3), the
scoped lockfile finalize the Decision made mandatory, and the release note.

**Touched, and nothing else:**

* `templates/modules/default-on/_lifecycle_metrics/gitmeta.py` and its
  byte-identical self-hosted twin `tools/_lifecycle_metrics/gitmeta.py`.
* `templates/modules/default-on/_lifecycle_metrics/__init__.py` and its twin
  `tools/_lifecycle_metrics/__init__.py` (P3, two paragraphs of docstring).
* One new file, `bootstrap/tests/test_lifecycle_stage_patterns.py`.
* `dev/.cairn/cairn-lock.yml` — two `hash` fields, advanced by
  `scaffold.py upgrade --finalize` scoped to the two `dst` paths.
* `CHANGELOG.md > Unreleased > Fixed` and one `dev/PLANNING.md` row — both
  serialized shared files; the implementing agent returns the exact text and the
  serialization owner lands it.

### The scope fence — carried from the proposal, unchanged

* **No new tool, command, subcommand, flag, module, or output column.**
  `PROPOSAL_COLUMNS` (`templates/modules/default-on/_lifecycle_metrics/extract.py:41-83`)
  is untouched; the same columns are emitted with values that are now correct.
* **No configurability.** No config key, no way for an adopter to supply their
  own patterns.
* **No public export.** `_stage_for_subject` is private, stays inside
  `_lifecycle_metrics`, and is imported by nothing outside it.
* **No commit-message convention is created.** Nothing in `AGENTS.md`,
  `doctrine/proposals.md`, or the templates gains a subject-grammar rule. If a
  reviewer reads this fix as establishing one, that reading is wrong and the fix
  is over-scoped.
* **No vocabulary beyond the four doctrinal stage nouns.** `archive`,
  `supersede`, `accept`, `reject`, `sharpening`, `claim-marker maintenance` get
  **no** stage.
* **No engine change, no manifest row change, no AST re-anchor, no gate
  re-anchor.** `bootstrap/tests/test_ast_attest.py:20` pins
  `bootstrap/_scaffold/__init__.py` and verifies over that package's `*.py`
  glob; a module template under `templates/modules/default-on/` cannot enter it.
  Re-verified against the working tree this session.
* **`scripts/transition_lint.py` is not proposed, prototyped, or prepared for.**
  The sibling proposal `2026-07-22-claude-transition-lint` stays parked pending
  the Maintainer's explicit go-ahead.
* **The `plans?` scope prefix stays out**, and `dev/plans:` subjects therefore
  classify as nothing. This is the R3 narrowing; Chunk A pins it and the plan
  re-measures it (16 corpus subjects, below).

### Deferred — named so it does not drift back in

* **The `_git_log_for_path` quiet-degradation hazard** (R12c): a `git log` that
  fails for any reason — including transient contention under concurrent load —
  returns `[]` at
  `templates/modules/default-on/_lifecycle_metrics/gitmeta.py:50-51` and silently
  downgrades a whole row with no signal. Pre-existing, out of scope, and the
  reason every corpus verification in this plan must run on a quiet tree.
  Durable home pre-declared in `## Lasting-truth migration`.
* **The `Exact`-with-no-hours row.** `2026-08-03-claude-r6-unused-def-blindspot`
  reports `Exact` with all three `hours_*` empty under the repaired classifier,
  because `_stage_reliability`
  (`templates/modules/default-on/_lifecycle_metrics/gitmeta.py:108-121`) returns
  `Exact` when the set of stages *present in the document* is empty and anything
  resolved. Pre-existing tier semantics, unchanged by this plan, newly *visible*
  because of it. Observation only.
* **The one pre-existing shipped-pattern false positive.**
  `review: tighten the recharge bounds` classifies `reviewed` today via the
  shipped `^Review\b`, and still will. Repairing it means editing the shipped
  vocabulary, which the revision deliberately does not do. Pinned as an
  explicitly-labelled expectation in Chunk A, not silently inherited.

### Documentation / doctrine surface

**Doctrine: none.** No file under `doctrine/`, no `AGENTS.md` rule, no template
`.md`, no module `.md`. `doctrine/proposals.md` is *cited as the source of truth
this fix conforms to* and is not edited.

**Documentation: one docstring, in two byte-identical copies (P3).**
`templates/modules/default-on/_lifecycle_metrics/__init__.py:74-78` and its
twin.

`templates/modules/default-on/lifecycle-metrics.md` is checked and
**deliberately untouched** — re-verified this session: it says nothing about
commit-subject matching or the reliability tiers.

<!-- cairn:slot documentation-tier-home -->
**Doc tier home rule** — route doc and doctrine changes by layer per
[`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):
cross-cutting prescription → governing layer (`AGENTS.md`);
deliberation about what to build → deliberation layer (`dev/`);
description of the software as it is → descriptive layer (`docs/`). A
plan's *Scope* must name the doctrine-surface touched (or an explicit
"no doctrine surface").
<!-- cairn:end documentation-tier-home -->

Routed: the P3 correction is **descriptive** — it describes the software as it
is, and its canonical home is the module's own docstring, where the incorrect
sentence already lives.

## What the working tree says today — re-measured for this plan

Every figure below was produced this session on the **canonical interpreter**
(`~/conda_envs/lhm/bin/python3.13`, Python 3.13.13) at `HEAD` `eacb7dd`,
`as_of 2026-08-04`, on a quiet tree. The proposal's own figures were measured on
2026-07-22 against a 12-proposal corpus; the corpus is now 35 proposals and
**two of the headline numbers have moved materially**. The proposal itself
required this: *"All counts are HEAD-dependent and will be re-measured
immediately before the opening commit."*

Corpus construction: the union of `git log --follow` subjects for all 35
proposal files under `dev/proposals/` and `dev/proposals/archive/`, excluding
`_template.md`.

| measure | 2026-07-22 (proposal) | **2026-08-04 (this plan)** |
| --- | --- | --- |
| proposal files | 12 | **35** |
| distinct `--follow` subjects | 76 | **246** |
| subjects classified by the **shipped** patterns | 0 | **0** |
| subjects classified by the **accepted revised design** | 52 | **115** (33 `open`, 12 `reviewed`, 34 `revised`, 36 `decision`) |
| proposal rows at `Best-effort` | 12 / 12 | **0 / 35** |
| proposal rows at `Exact` | 10 | **12** |
| proposal rows at `Good` | 2 | **23** |
| negative `hours_*` deltas | 0 | **0** |

**The defect reproduces at three times the scale, and the Decision's headline
claim holds: `Best-effort` goes from 35/35 to 0/35.** Two findings need saying
plainly rather than being left for the reviewer to discover:

**(a) The price of the narrowing is now roughly 17 tiers, not one.** Re-running
the identical pipeline with the bare-subject fallback restored — the design R1
blocked and the Decision rejected — gives **29 `Exact` / 6 `Good` / 0
`Best-effort`** against the accepted design's **12 / 23 / 0**. On 2026-07-22 the
same ablation cost exactly one tier (11 → 10). The cause is not a change in the
design: it is that the 2026-08-03 wave of proposals writes unscoped subjects
(`fork-advisory-semantics: Response to Internal review`,
`Append Gemini Flash External Security Review of scan-coverage proposal`), which
the scope gate declines by construction.

**This does not reopen the Decision, and this plan does not treat it as
reopened.** The narrowing bought what it was ratified to buy — zero wrong-stage
assignments, and 9 of the panel's 10 adopter-plausible probes to `None` (the
tenth is the pre-existing shipped-pattern hit named above). `Good` is the honest
tier for a row whose subjects the vocabulary cannot read; `Exact` on a guessed
stage is the failure the whole revision exists to prevent. But the Decision's
own summary — *"One reliability tier was surrendered"* — was true of the corpus
it was measured on and is not true of today's, and the Maintainer is entitled to
see that before the change lands. It is raised in `## Plan review — the brief`
as the reviewer's first question and named in the Maintainer fence.

**(b) The hyphen-compound guard now has zero measured effect on the live
corpus.** Ablating `(?<!-)` / `(?!-)` from both scoped patterns and re-running
over all 246 subjects flips **0**. This is not evidence the guard is wrong — it
is a consequence of R3: the guard's sole historical justification
(`dev/plans: archive review-record-integrity …`) is now excluded by the scope
gate before the guard is ever reached. The guard is therefore pinned **only by
constructed probes**, and Chunk A says so in the test docstring rather than
implying corpus evidence it does not have. Verified discriminating probes:

| probe | guarded | unguarded |
| --- | --- | --- |
| `dev/proposals: interpreter-trust-root -- add Security-Review section` | `None` | `reviewed` |
| `dev/proposals: foo -- close out the review-record-integrity thread` | `None` | `reviewed` |
| `dev/proposals: open interpreter-trust-root-fallback (F2 split; Security-Review gated)` | `open` | `open` |

The third discriminates nothing — it is a **priority-order** test and is
labelled as one (R6). Proposed test 2 in the original proposal offered it as
guard evidence; that framing is dead.

**(c) The `plans?` ablation reproduces and is larger.** Re-adding `plans?` to
the scope prefix flips **16** corpus subjects, every one of them
`None → open`, every one of them a `dev/plans: open <slug> (+ archive proposal)`
commit — i.e. the proposal's **archive** event being read as its **opening**.
R3's finding at 4 subjects is now 16.

**(d) P2's fall-through remains latent.** Running both loop shapes over
`_git_log_for_path` output for all 35 proposal files with the patterns held
constant: **0 of 35 differ**. R10's correction holds at the larger corpus. P2
stays because pure-function classification is the right invariant and it is
free; the synthetic test in Chunk A is the only thing pinning it, and its
docstring says so.

**Lockfile and gate posture, re-verified — both changed since the proposal:**

* `~/conda_envs/lhm/bin/python3.13 bootstrap/verify_integrity.py --target .`
  now exits 1 with **2** violations (`AGENTS.md`,
  `dev/modules/security-review.md`) — not the 41 the proposal measured. The two
  records this plan touches are **current**: `dev/.cairn/cairn-lock.yml:498`
  records `sha256:5a47849b…` for `tools/_lifecycle_metrics/gitmeta.py` and
  `:470` records `sha256:c0e169e7…` for `tools/_lifecycle_metrics/__init__.py`,
  both equal to the bytes on disk. **This is precisely the state that makes the
  scoped finalize mandatory**, exactly as the Decision reasoned.
* The **gate-manifest fixture is also current now**, contrary to the proposal's
  measurement:
  `bootstrap/tests/fixtures/gate_manifest.json:2770` freezes `5a47849b…` and
  `:2766` freezes `c0e169e7…`. Editing either file makes the committed fixture
  stale — a `FROZEN-MODIFIED` hold **only if an anchored batch is live**. It is
  not: the committed fixture's `anchor_ref` is `null`, and
  `bootstrap/tests/test_gate_manifest.py` verifies a **freshly produced**
  manifest (`produced = G.produce(_REPO)`) against the live tree, so the
  committed fixture is never a `pytest` gate. Re-confirm at implementation time;
  see the Maintainer fence.
* **Twin parity holds today.** Both pairs are byte-identical
  (`gitmeta.py` = `sha256:5a47849b…`, `__init__.py` = `sha256:c0e169e7…` on both
  sides), and `bootstrap/tests/test_notice_install.py:98`
  (`test_every_self_hosted_twin_stays_byte_identical_to_its_source`) reds the
  suite if only one side is edited.
* **Bandit scope includes both files.** `bootstrap/security_check.py`'s
  `scan_targets()` returns 74 targets this session and both
  `templates/modules/default-on/_lifecycle_metrics/gitmeta.py` and
  `…/__init__.py` are in it (verified by calling it). The change adds compiled
  regexes and one pure string function — no `subprocess`, `eval`, or
  deserialization — so no new finding is expected, and the gate is run rather
  than assumed.
* **The two Unicode dash literals set no new precedent.** `_STAGE_PHRASE_SEP_RE`
  needs U+2013 (EN DASH) and U+2014 (EM DASH). Both already appear in the
  shipped file, at
  `templates/modules/default-on/_lifecycle_metrics/gitmeta.py:21`, inside the
  shipped `decision` pattern's character class. 18 shipped template `.py` files
  already carry non-ASCII. No ASCII-only gate exists over shipped Python.

## Sequence

```
1. Chunk A -- P1 + P2: the scoped vocabulary, the pure classifier, and the
              behavioural test; both gitmeta.py copies         [commit pending]
2. Chunk B -- P3: the degradation docstring; both __init__.py copies
                                                               [commit pending]
3. Chunk C -- the scoped `upgrade --finalize` for the two lockfile records
                                                               [commit pending]
4. Chunk D -- release note + roadmap row (serialized; text returned, owner lands)
                                                               [commit pending]
```

Order is load-bearing in one place only: **Chunk C must follow A and B**, because
it records the post-edit bytes. A and B are independent of each other and B could
land first; the order above keeps the defect fix at the head of the log.

---

### Chunk A — P1 + P2: the scoped vocabulary and the pure classifier

**Part 1 is transcription, not audit.** The design was verified twice — by the
author against the live corpus in the `## Revised proposal`, and by Gemini's
External round, which *re-executed* the classifier on the canonical interpreter
and independently reproduced the counts. The implementer **transcribes the code
block at proposal `:833-869` — the `## Revised proposal`'s P1 listing —
character-for-character** and does not re-derive, re-tune, or "improve" any
regex. A transcription that differs from the source in any character is a defect
of this chunk, not a design choice.

The transcription table below is the checklist. Each row is one literal the new
code introduces, with the line in the accepted revision it comes from. It was
verified against the working tree this session by transcribing the block,
running it over all 246 corpus subjects and all 30 test vectors, and getting
zero mismatches against the expected table.

| # | symbol / literal | value | source line |
|---|---|---|---|
| 1 | `_STAGE_SCOPE_PREFIX_RE` | `^(?:dev/)?proposals?\s*:\s*`, `re.I` | `:833` |
| 2 | — prefix optional segment | `(?:dev/)?` | `:833` |
| 3 | — tree token | `proposals?` (singular or plural; **`plans?` absent**, R3) | `:833` |
| 4 | — colon with optional space | `\s*:\s*` | `:833` |
| 5 | `_STAGE_PHRASE_SEP_RE` | `\s+(?:--\|–\|—)\s+` | `:835` |
| 6 | — ASCII separator | `--` | `:835` |
| 7 | — EN DASH separator | U+2013 | `:835` |
| 8 | — EM DASH separator | U+2014 | `:835` |
| 9 | `_SCOPED_STAGE_PATTERNS` | `List[Tuple[str, 're.Pattern[str]']]`, four entries | `:839` |
| 10 | — comment above it | the two-line "Consulted ONLY …" note | `:837-838` |
| 11 | `open` pattern | `^open(?:ing)?\b`, `re.I` | `:840` |
| 12 | — token `open` | anchored at head of the de-prefixed body | `:840` |
| 13 | — token `opening` | via `(?:ing)?` | `:840` |
| 14 | `decision` pattern, arm 1 | `^(?:maintainer\s+)?decision\b` | `:842` |
| 15 | `decision` pattern, arm 2 | `(?<!-)\bmaintainer\s+decision\b(?!-)` | `:843` |
| 16 | — the alternation between them | a regex `\|` joining the two arms — the R2 repair; without arm 2, two of the three real Decision forms misclassify | `:842-843` |
| 17 | `revised` pattern | `(?<!-)\b(?:response\|responses\|revised\|revise\|respond\s+to)\b(?!-)`, `re.I` | `:844-846` |
| 18 | — token `response` | | `:845` |
| 19 | — token `responses` | | `:845` |
| 20 | — token `revised` | | `:845` |
| 21 | — token `revise` | | `:845` |
| 22 | — token `respond to` | `respond\s+to` | `:845` |
| 23 | `reviewed` pattern | `(?<!-)\breview\b(?!-)`, `re.I` — **no `sharpening` lookahead**; that exclusion stays only in the shipped pattern (R4) | `:847` |
| 24 | hyphen guards | `(?<!-)` … `(?!-)` on `revised`, `reviewed`, and arm 2 of `decision` | `:843,845,847` |
| 25 | `_HEAD_ANCHORED_STAGES` | `frozenset({'open', 'decision'})` | `:850` |
| 26 | `_stage_for_subject` | signature `(subject: str) -> Optional[str]`, docstring `"""Classify a commit subject as AT MOST ONE lifecycle stage."""` | `:853-854` |
| 27 | — shipped-first order | the shipped `_STAGE_COMMIT_PATTERNS` loop runs **before** the scope check, using `.match()` | `:856-858` |
| 28 | — no bare-subject fallback | `if match is None: return None` — the ratified narrowing | `:859-861` |
| 29 | — phrase split | `_STAGE_PHRASE_SEP_RE.split(body, maxsplit=1)`, `phrase = parts[1] if len(parts) > 1 else body` | `:863-864` |
| 30 | — per-stage target | `body` for a head-anchored stage, `phrase` otherwise; `.search()` | `:865-868` |

`Optional` is already imported at
`templates/modules/default-on/_lifecycle_metrics/gitmeta.py:9`; no import change
is needed.

| # | File | Change |
|---|------|--------|
| A1 | `templates/modules/default-on/_lifecycle_metrics/gitmeta.py` | **P1.** Transcribe rows 1–30 above verbatim, inserted after the existing `_STAGE_COMMIT_PATTERNS` block (which is **not edited** — verify byte-equality of lines 17–25 against `HEAD` before committing). |
| A2 | (same file) | **P2.** Replace the inner loop at `gitmeta.py:81-85` with the three-line form at proposal `:184-187`: classify once via `_stage_for_subject`, assign only if the stage is unfilled, no `break`-on-assign, no re-test. `reversed(log)` iteration and first-match-wins slot filling are unchanged. |
| A3 | `tools/_lifecycle_metrics/gitmeta.py` | The self-hosted twin: `cp` the template copy over it. **Same commit as A1/A2** — `test_every_self_hosted_twin_stays_byte_identical_to_its_source` reds the suite otherwise. Verify with `shasum -a 256` on both paths, not by eye. |
| A4 | `bootstrap/tests/test_lifecycle_stage_patterns.py` | **New file.** Tests T1–T12 below. Loads the **template** launcher `templates/modules/default-on/lifecycle_metrics.py` via `importlib.util.spec_from_file_location`, the same idiom and for the same recorded reason as `bootstrap/tests/test_lifecycle_metrics_config.py:27-36` (whose own docstring at `:13-16` records the posture) — a new test file is FROZEN-NEW / COLLECTION-ADDED to the gate manifest and needs no re-anchor, whereas `bootstrap/tests/test_reference_scripts.py` is in `frozen_files` and editing it would HOLD. The launcher facade re-exports `_stage_for_subject`, `_resolve_stage_commits` and `proposal_rows` (verified this session), so the test reaches both the private classifier and the public path through one load. |

**The oracle rule, stated once and binding on every test in A4.** Every expected
value is a **hand-written literal in the test file**. No expectation is derived
from `_SCOPED_STAGE_PATTERNS`, `_STAGE_COMMIT_PATTERNS`, `_stage_for_subject`, or
any object the code under test owns. A test whose expected set is the subject's
own data structure is green forever and proves nothing — this session has shipped
two of those and will not ship a third.

#### The tests, each with the perturbation that makes it RED

Each perturbation edits **the hazard** — the shipped file's regexes, guards, or
loop — never the test's own body. Every one below was executed this session
against a transcribed copy and observed to discriminate; the implementer re-runs
each against the real edited file and writes the ledger (change made, failure
observed, byte-identical restore confirmed by `git hash-object` vs
`git rev-parse HEAD:<path>`) into the commit body.

| test | asserts | perturbation that makes it RED | observed |
|---|---|---|---|
| **T1** corpus regression | ~40 literal `(subject, expected)` pairs drawn from the live 246-subject corpus, parametrized, including every `None` expectation in the table | Revert `gitmeta.py` to `HEAD` (shipped classifier only) | `AttributeError` / every scoped vector → `None`; **this is the test that would have caught the original defect** |
| **T2** no bare-subject fallback | the panel's 10 adopter-plausible subjects: 9 → `None`; `review: tighten the recharge bounds` → `reviewed`, with the docstring labelling it **pre-existing shipped-pattern behaviour, not a choice this fix made** | Delete `if match is None: return None`; fall through with `body = text` | **8 of the 9 `None` expectations flip** to `revised`/`reviewed`/`open`/`decision` |
| **T3** `dev/plans:` never classifies | the 16 live plan-open subjects (15 of the form `dev/plans: open <slug> (+ archive proposal)`, one `dev/plans: open adopter-entry-doc-refresh; archive the accepted proposal`), plus `dev/plans: archive review-record-integrity (Chunk C pointer + lifecycle close)` and `dev/plans: <slug> -- Code review (fresh-context, disclosed scribe)` → all `None` | Re-add `plans?` to `_STAGE_SCOPE_PREFIX_RE` | 16 corpus subjects flip `None → open`; the Code-review probe flips `None → reviewed` |
| **T4** hyphen-compound guard | `dev/proposals: interpreter-trust-root -- add Security-Review section` → `None`; `dev/proposals: foo -- close out the review-record-integrity thread` → `None`. Docstring records that **no live corpus subject discriminates this guard** (0 flips over 246) and that these are constructed probes | Strip `(?<!-)` / `(?!-)` from the scoped `reviewed` pattern | both flip `None → reviewed` |
| **T4b** the retained weak vector, labelled as one | `dev/proposals: open interpreter-trust-root-fallback (F2 split; Security-Review gated)` → `open`. Kept per R6 for continuity with the proposal's test list. **Its docstring states what it does not pin**: it is green with the guard and without it, and green with `reviewed` moved ahead of `open`. It falls only under the *conjunction* | Remove the hyphen guard **and** move `reviewed` ahead of `open` | flips `open → reviewed`. Under either perturbation alone it stays `open` — measured all four ways this session |
| **T4c** priority order, actually discriminating | `dev/proposals: open widget-thing -- respond to the review` → `open` (head-anchored `open` beats a `revised` token in the stage phrase) | Move `revised` ahead of `open` in `_SCOPED_STAGE_PATTERNS` | flips `open → revised` |
| **T5** one stage per subject | `dev/proposals: licensing -- Response to Gemini External review` → `revised`; `dev/proposals: adopter-entry doc-refresh -- Internal review panel + Response + Revised` → `revised` | Swap `revised` and `reviewed` in `_SCOPED_STAGE_PATTERNS` | both flip `revised → reviewed` |
| **T6** all three real Decision forms | head-first, slug-first, and slug-first-with-trailing-`review` → `decision`; `dev/proposals: foo -- SUPERSEDE bar` → `None` as a **documented, accepted false negative** | Delete arm 2 (`\|(?<!-)\bmaintainer\s+decision\b(?!-)`) | `… licensing -- Maintainer Decision -- ACCEPT` → `None`; `… transition-lint -- Maintainer Decision -- ACCEPT (post Internal review)` → **`reviewed`** (the R2 wrong-stage-at-`Exact` bug) |
| **T7a** sharpening false-negative guard | `dev/proposals: <stem> -- Internal review (fresh-context panel) + Sharpening` → `reviewed` | Add `(?!.*\bsharpening\b)` to the **scoped** `reviewed` pattern | flips `reviewed → None` — the R4 widening this design refuses |
| **T7b** shipped exclusion preserved | `Review sharpening pass` → `None` | Delete `(?!.*\bsharpening\b)` from the **shipped** pattern at `gitmeta.py:24` | flips `None → reviewed` |
| **T8** legacy / quickstart forms | the twelve backward-compatibility strings, asserted verbatim, including `Open proposal: README tagline` (`docs/quickstart.md:240`) and `Open proposal alice thing` (`bootstrap/tests/test_reference_scripts.py:476`) | Delete the shipped `open` pattern at `gitmeta.py:18-19` | 4 vectors fail. **Stated honestly: T8 is green before *and* after this plan's diff** — backward compatibility is guaranteed by construction, since the shipped patterns are not edited. Its falsifying future state is a later author editing them |
| **T9** P2, no fall-through | Synthetic `tmp_path` git repo, one proposal file, two commits: `dev/proposals: open widget-thing (first)` then `dev/proposals: open widget-thing again -- respond to the review`. Assert `_resolve_stage_commits` gives `open` = commit 1 and `revised` **is `None`** | Restore a fall-through loop (re-test remaining stages when the classified slot is filled) | `revised` takes commit 2. Docstring records that this is the **only** thing pinning P2 and that the live corpus does not exercise it (0 of 35 file histories differ between the two loop shapes) |
| **T10** end-to-end, public path | Synthetic `tmp_path` repo scaffolded with `lifecycle-metrics`, one proposal file, four commits in the scoped subject form (open / review / response / decision). Assert `proposal_rows(tmp_path)` yields `stage_timestamp_reliability == 'Exact'`, all three `hours_*` non-empty and `>= 0` | Revert `gitmeta.py` to `HEAD` | `Best-effort`, all `hours_*` empty. **Never asserts a tier against the live Cairn corpus** — R12c's quiet-tree hazard makes that non-reproducible under load |
| **T11** never raises | `''`, `'   '`, a separator-only subject, a prefix-only subject, non-ASCII (`dev/proposals: ünïcödé revisé`), and a 500-character subject → all return without raising | Replace `phrase = parts[1] if len(parts) > 1 else body` with an unconditional `parts[1]` | `IndexError` on every separator-less subject |
| **T12** degradation preserved | A `tmp_path` scaffold with **no** `.git` → `Best-effort`, all `hours_*` empty. Deliberately duplicates `bootstrap/tests/test_reference_scripts.py:443-457` so the guarantee is local to the changed code | Seed a stage unconditionally in `_resolve_stage_commits` (`out['open'] = ('x', <now>)` before the loop) | tier flips to `Exact` on a repo with no history. **Stated honestly: no change in this plan's own diff can red T12** — it re-asserts a pre-existing guarantee |

**Acceptance criteria — Chunk A.**

* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_lifecycle_stage_patterns.py -q`
  → all pass, 0 skipped.
* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests -q` → green, 0
  failed / 0 skipped, collection grows by exactly the new nodes and drops none.
  **Baseline measured immediately before the commit, on a quiet tree** — not
  carried forward from the proposal's `1437`, which is two months and many
  landings stale.
* `shasum -a 256` on both `gitmeta.py` paths → equal.
* `git diff HEAD -- templates/modules/default-on/_lifecycle_metrics/gitmeta.py`
  shows **no change to lines 17–25** (`_STAGE_COMMIT_PATTERNS`), and no change to
  `_git_log_for_path`, `_hour_delta`, `_day_delta`, `_stage_reliability`,
  `_get_head_commit`, or `_list_goodnight_commits`.
* **Corpus re-measurement, on a quiet tree**, reproducing the table above at
  then-current HEAD: 0/N classified before, ≈115/246 after, 0 `Best-effort`
  rows, 0 negative `hours_*`. Figures move with HEAD; the invariants
  (`Best-effort` → 0, negative deltas → 0, `dev/plans:` → 0 classified) do not.
* `~/conda_envs/lhm/bin/python3.13 bootstrap/security_check.py` → `PASS`, no new
  finding over the shipped surface including this file.
* `~/conda_envs/lhm/bin/python3.13 bootstrap/scaffold.py --manifest | grep gitmeta`
  → **unchanged**. Capture before the edit, diff after. This fix must not move
  an install-manifest row.
* **Every perturbation in the table above RUN, not reasoned about**, with the
  ledger in the commit body and each restore confirmed by hash.
* **Channel note.** Subject: `_stage_for_subject` and `_resolve_stage_commits`
  in `gitmeta.py`. Oracle: literal expectation tables hand-written in the test
  file (T1–T8, T11) and real `git` histories built by the test in `tmp_path`
  (T9, T10, T12). Neither input is derived from any object the subject owns.

---

### Chunk B — P3: the degradation docstring, both copies

The sentence at
`templates/modules/default-on/_lifecycle_metrics/__init__.py:74-78` is the only
adopter-facing documentation of this reliability tier, and every clause of its
cause list is false of the failure actually observed: git was present, the tree
was a checkout, the branch was `master`, and the tier was still `Best-effort`.

P3 corrects **three** things, per the revision at proposal `:923-938`:

1. the falsely-exhaustive cause list — add *or when no commit subject in a
   file's history matches the stage vocabulary*;
2. what the hour deltas measure (R5b): the interval between the **commits that
   recorded** each transition, which for a batch-committed session can be near
   zero. Live example to keep the sentence honest, re-measured this session:
   `hours_reviewed_to_revised` is exactly `0.0` for
   `2026-07-22-claude-interpreter-trust-root-fallback`,
   `…-lockfile-provenance-fields`, and `…-transition-lint`;
3. that `hours_*` can legitimately disagree with `days_*` (R5a) when a
   proposal's header `**Date opened**` predates its opening commit. Live
   example, re-measured: four 2026-07-11 proposals carry
   `hours_revised_to_decision ≈ 116.46` (4.85 days) beside
   `days_revised_to_decision = 11`.

| # | File | Change |
|---|------|--------|
| B1 | `templates/modules/default-on/_lifecycle_metrics/__init__.py` | Rewrite the paragraph at `:74-78` per the three corrections above. Prose only — no code, no `_SUBMODULES` change, no import change. |
| B2 | `tools/_lifecycle_metrics/__init__.py` | `cp` the template copy over it, same commit. Verify by `shasum -a 256`. |

**Acceptance criteria — Chunk B.**

* Both `__init__.py` paths hash equal.
* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests -q` → green
  (`test_every_self_hosted_twin_stays_byte_identical_to_its_source` is the one
  that matters here).
* `~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py` → clean.
* `~/conda_envs/lhm/bin/python3.13 -c "import sys; sys.path.insert(0,'tools'); import _lifecycle_metrics"`
  → imports cleanly (a docstring edit that breaks the triple-quote would fail
  here before it reached the suite).
* **No perturbation test.** B is prose in a docstring; there is no behaviour to
  falsify. Said explicitly rather than left as an unexplained gap — the guard is
  the twin-parity test and the import check, and neither is evidence about the
  *content* of the sentence. The reviewer reads it.
* **The old sentence must not survive anywhere.** `grep -rn "the default branch
  is named" templates/ tools/` returns only the corrected text.

---

### Chunk C — the scoped `upgrade --finalize` the Decision made mandatory

Ratified plan condition, quoted from the Decision: *"A **scoped `upgrade
--finalize`** for `gitmeta.py` and its `__init__.py` twin. This is now
*mandatory*."* The ground, re-verified above: both lockfile records are current
today, so editing the files without finalizing creates two fresh mismatches and
re-reds `verify_integrity`.

| # | File | Change |
|---|------|--------|
| C1 | `dev/.cairn/cairn-lock.yml` | Produced, never hand-edited, by:<br>`~/conda_envs/lhm/bin/python3.13 bootstrap/scaffold.py upgrade --target . --finalize tools/_lifecycle_metrics/gitmeta.py tools/_lifecycle_metrics/__init__.py` |

**Why scoped, and why it must stay scoped.** The positional-`PATH` form scopes
the write-set to exactly the named `dst` records; a bare `--finalize` sweeps the
whole tree and would advance **other sessions' in-flight work** into the
integrity record. Other workflows are editing `bootstrap/_scaffold/` and
`bootstrap/` concurrently as this plan is written. The engine's own #56
dirty-tree guard refuses an *unscoped* finalize on a dirty tree for this exact
reason; a scoped finalize is permitted and is the correct instrument. **`--force`
is never passed.**

**Acceptance criteria — Chunk C.**

* The command prints `Finalized dev/.cairn/cairn-lock.yml: advanced 2 hash(es)
  (scoped to 2 path(s)) …`. **Exactly 2** — a different number means the scope
  did not bind and the change is reverted, not committed.
* `git diff dev/.cairn/cairn-lock.yml` touches **exactly two lines**, both
  `"hash":`, in the records at `:470` and `:498`. Any `base_hash`, `src`, `dst`,
  `verbatim`, or `living_state` movement is a defect of this chunk. (`base_hash`
  is already present on both records, so the engine's
  "preserve-the-as-shipped-baseline" branch is a no-op here — verified.)
* The two new `hash` values equal `sha256:` + the `shasum -a 256` of the
  post-Chunk-A/B files. Checked against a shell hash, not against the tool's own
  output.
* `~/conda_envs/lhm/bin/python3.13 bootstrap/verify_integrity.py --target .`
  reports **no violation naming either `_lifecycle_metrics` path**. It will still
  exit 1 while `AGENTS.md` and `dev/modules/security-review.md` remain
  mismatched — pre-existing, not this plan's, and **not** to be swept in. Record
  the before/after violation lists side by side in the commit body so the
  delta is legible.
* **This chunk cannot be verified by a test and does not pretend to be.** Its
  oracle is the shell hash and the before/after violation list, both produced
  outside the artifact under verification.

---

### Chunk D — release note and roadmap row

Both files are **serialized shared surfaces**. The implementing agent produces
the exact text and does not edit either file; the serialization owner lands it.

| # | File | Change |
|---|------|--------|
| D1 | `CHANGELOG.md > Unreleased > Fixed` | One entry — text below. |
| D2 | `dev/PLANNING.md > Active` | One row for the open plan; removed at the next goodnight scrub after archive, per the board's own rule. |

**D1, exact text to land:**

> - **The shipped lifecycle-stage commit vocabulary read nothing.**
>   `_STAGE_COMMIT_PATTERNS` in the default-on `lifecycle-metrics` module matched
>   **zero** of Cairn's real commit subjects, so `hours_open_to_reviewed`,
>   `hours_reviewed_to_revised` and `hours_revised_to_decision` came back empty
>   and `stage_timestamp_reliability` read `Best-effort` on every row — while the
>   tool exited 0 and emitted a well-formed report. The reader now consults a
>   second, **scope-gated** vocabulary when the shipped one declines, and
>   classification is a pure function of the subject. Deliberately narrow: an
>   un-scoped subject still classifies as nothing, so no commit is ever
>   mislabelled at `Exact`. Accepted proposal stem `stage-commit-patterns`;
>   plan stem `stage-commit-patterns`.

**D2, exact row text to land under `## Active`:**

> * **stage-commit-patterns** *(plan open 2026-08-04; proposal accepted
>   2026-07-22)* — repairs the default-on `lifecycle-metrics` stage-timing
>   reader, which matched zero real commit subjects. Four commits: the
>   scope-gated classifier + behavioural test, the degradation docstring, a
>   scoped lockfile finalize, the release note. Plan review
>   **required(Internal)** with an execution obligation (re-run the corpus
>   ablations, do not read-only). One observation the plan surfaces rather than
>   settles: the price of the ratified narrowing is now ~17 reliability tiers on
>   the live corpus, not the one measured at Decision time.

**Acceptance criteria — Chunk D.**

* `~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py` clean after the owner
  lands both.
* No path link to a plan or proposal in either file — filename stem only, per
  `AGENTS.md > Shared communication files`.

---

## Acceptance criteria

Per-chunk criteria are above; these are the plan-level deliverables.

* **Tests that must pass.**
  * `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests` — the whole
    suite, green, **0 failed / 0 skipped**, under the canonical interpreter
    (3.13.13). Baseline re-measured on a quiet tree immediately before the first
    implementing commit; **not** carried forward from the proposal's
    `1437 passed` (2026-07-22), which predates two months of landings.
  * `bootstrap/tests/test_lifecycle_stage_patterns.py` — T1–T12, new file.
  * [`bootstrap/tests/test_notice_install.py`](../../bootstrap/tests/test_notice_install.py)
    — unchanged and green; it is what enforces both twin pairs.
  * [`bootstrap/tests/test_reference_scripts.py`](../../bootstrap/tests/test_reference_scripts.py)
    — unchanged and green. It is in the gate manifest's `frozen_files`; **it is
    not edited**, which is why T1–T12 land in a new file.
  * [`bootstrap/tests/test_ast_attest.py`](../../bootstrap/tests/test_ast_attest.py)
    — unchanged and green, confirming no re-anchor was triggered.
  * **Every new test shown non-vacuous by a run perturbation**, ledger in the
    commit body. Where a test cannot be made to fail by this plan's own diff
    (T8, T12) the plan says so above instead of claiming a guard it does not
    have.
* **Doc updates that must land.** All hand-authored: the P3 docstring in two
  copies (Chunk B) and `CHANGELOG.md > Unreleased > Fixed` (Chunk D). No
  generated docs, no snippet-synced blocks, no `docs/` page.
* **Examples / smoke checks required.**
  * `~/conda_envs/lhm/bin/python3.13 tools/lifecycle_metrics.py proposals --format csv`
    — **on a quiet tree** — expect 0 `Best-effort` rows and populated `hours_*`.
    R12c: concurrent git load makes `_git_log_for_path` return `[]` at
    `templates/modules/default-on/_lifecycle_metrics/gitmeta.py:50-51` and
    silently degrades a row, so a run during a background suite is not evidence.
  * `~/conda_envs/lhm/bin/python3.13 bootstrap/security_check.py` — `PASS`.
  * `~/conda_envs/lhm/bin/python3.13 bootstrap/scaffold.py --manifest` —
    **unchanged**, diffed against a capture taken at the plan-open commit.
  * **N/A**: the example gallery. `examples/minimal/` and
    `examples/scientific-minimal/` demonstrate nothing this change touches.
* **Inbound path-link updates.** None expected. `dev/PLANNING.md` and
  `dev/NEXT_SESSION.md` refer to plans by filename stem, so the archive-move
  needs no edit there. Confirm at archive time rather than assume.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants, each with the chunk and test that enforces it.**
  * *At most one stage per subject.* `_stage_for_subject` returns a single
    `Optional[str]`. Enforced by T5 in
    `bootstrap/tests/test_lifecycle_stage_patterns.py` (cited as a path, not a
    link: it lands in Chunk A and the link checker resolves targets);
    RED under a priority-order swap.
  * *No un-scoped subject reaches the new vocabulary.* The ratified narrowing.
    Enforced by T2; RED under deletion of the `return None`, with 8 of 9 probes
    flipping.
  * *A `dev/plans:` subject classifies as nothing.* Enforced by T3; RED under
    the `plans?` re-add, 16 corpus subjects flipping.
  * *`_STAGE_COMMIT_PATTERNS` is byte-unchanged.* Enforced **structurally** (the
    diff), checked once in Chunk A's acceptance, and pinned in one direction by
    T7b and T8. **Not guarded by a test that fails when a future author edits
    it** — T8 catches a *deletion*, not a widening. Stated because it is the
    claim a reviewer should attack.
  * *Slot assignment stays first-match-wins, oldest-first.* The `reversed(log)`
    iteration is unchanged. Enforced by T9.
  * *The function never raises on any subject.* Enforced by T11; RED under an
    unconditional `parts[1]`.
  * *Twin byte-parity, both pairs.* Enforced by
    `test_every_self_hosted_twin_stays_byte_identical_to_its_source`
    ([`bootstrap/tests/test_notice_install.py`](../../bootstrap/tests/test_notice_install.py)).
  * *Reliability-tier semantics unchanged.* `_stage_reliability` is not edited.
  * *The install manifest does not move.* Enforced by the diff against a
    pre-change capture, in Chunk A's acceptance. Not test-guarded.
  * *The lockfile attests the tree after the change.* Enforced by Chunk C's
    two-line diff plus `verify_integrity`. Not test-guarded, and cannot be —
    its oracle is a shell hash.
* **Public-path → test mapping.** The change adds **no** public entry point.
  The public path whose *behaviour* changes is `proposal_rows(root)` → the
  `stage_timestamp_reliability` and three `hours_*` columns. It is exercised
  through its public path — on a synthetic repo, never on the live corpus — by
  T10 and T12 in
  `bootstrap/tests/test_lifecycle_stage_patterns.py` (path, not link — it lands
  in Chunk A), and remains exercised by `TestVcsRobustness` in
  [`bootstrap/tests/test_reference_scripts.py`](../../bootstrap/tests/test_reference_scripts.py).
  T1–T8 and T11 address the private classifier directly and are labelled as unit
  tests, not public-path coverage.
* **Failure modes — all open (degrade), none closed (raise), intentionally.**
  * No subject matches → every slot `None` → `Best-effort` + empty hour columns.
    Identical to today, which is the correct floor. Pinned by T12.
  * A subject matches the **wrong** stage → a wrong hour-delta reported as
    `Exact`. The one failure mode worse than the status quo, which is why the
    scope gate, the phrase restriction, the hyphen guard and the priority order
    each have their own perturbation-verified test (T2, T4, T5, T6).
  * A subject the vocabulary cannot read → `None` → the row degrades to `Good`,
    honestly. This is the priced cost, and at 23 of 35 rows it is now the
    *common* case; see the re-measurement section.
  * git absent / not a checkout → unchanged (`_git_log_for_path` returns `[]`).
    Pinned by T12 and by
    [`bootstrap/tests/test_reference_scripts.py`](../../bootstrap/tests/test_reference_scripts.py).
  * git present but the log call fails transiently → `[]`, silent row
    degradation. **Open, pre-existing, deferred** (R12c).
  * A scoped finalize that binds the wrong records → caught by the "exactly 2"
    and two-line-diff criteria in Chunk C, both checked outside the tool.
* **Edge cases handled.** Empty and whitespace-only subject; no area prefix
  (quickstart form); prefix with no stage token; multiple ` -- ` separators (only
  the first splits, `maxsplit=1`); U+2013 and U+2014 separators; mixed case
  (`re.I` throughout); a stage word appearing only inside a slug; a stage word
  inside a hyphen compound; two `open`-classified commits in one history; a
  bundled review+response commit; `dev/plans:`-prefixed commits inside a
  proposal's `--follow` history; a 500-character subject; non-ASCII subject text.
  **Out of scope:** merge commits; non-English subjects; any project whose
  subjects carry no doctrinal stage noun — these correctly yield `Best-effort`,
  which is the honest answer.
* **Known omissions, stated rather than implied.**
  (a) The frozen expectation table is a **snapshot of real subjects copied into
  the test file**, not a live `git log`. It cannot catch a *future* Cairn subject
  style drifting away from the vocabulary; only a re-measurement can. Deliberate
  — a live-history test would rot on every commit and would not run in an
  adopter's tree.
  (b) No second real corpus exists. The 10 adopter probes are one lens's
  construction from one domain, illustrative rather than measured.
  (c) Nothing guards `_STAGE_COMMIT_PATTERNS` against a future *widening* edit.
  (d) The `Exact`-with-empty-hours row
  (`2026-08-03-claude-r6-unused-def-blindspot`) is left as-is; the tier
  semantics that produce it are pre-existing and out of scope.
  (e) The interaction of the repaired vocabulary with an adopter's non-Cairn
  commit conventions is untested, because no such corpus exists to test against.
  (f) Whether the ~17-tier price of the narrowing (vs. the one tier priced at
  Decision time) warrants revisiting the trade is a Maintainer question this plan
  raises and does not answer.

## Verification

Run under the canonical interpreter (`~/conda_envs/lhm/bin/python3.13`, Python
3.13.13). A different Python minor silently changes the suite figure; name the
interpreter alongside any figure asserted.

<!-- cairn:slot verification-commands -->
The standing gates Cairn runs before a change lands (the same ones CI
enforces):

* **Engine suite** — `python -m pytest bootstrap/tests` (the whole
  suite; scope to `bootstrap/tests/test_<surface>.py` while iterating,
  but the full suite gates the cut).
* **Prose integrity** — `python scripts/check_cairn.py` (internal link
  / anchor resolution + claim-path check over the Markdown tree).
* **Quality gate** — `python scripts/quality_gate.py` (order-
  independence + vendor-neutrality + redundancy; `--sub neutrality`
  alone for a doctrine / template wording change).
* **Write-time claim check** — `python scripts/claim_check.py <file>` over
  each proposal / plan / doc the change authored. **One file per
  invocation** — the checker takes a single path and exits 2 (usage) on
  more, so loop rather than passing a list.

Plan-specific gates (a security-lint budget, a doc-drift gate, the
model-selection mapping check `python scripts/check_model_selection.py`)
are added per plan when the change touches that surface.
<!-- cairn:end verification-commands -->

Plan-specific, in addition:

* `~/conda_envs/lhm/bin/python3.13 bootstrap/security_check.py` — Bandit over
  the shipped surface, which includes both edited files.
* `~/conda_envs/lhm/bin/python3.13 bootstrap/verify_integrity.py --target .` —
  before and after Chunk C, violation lists compared.
* `~/conda_envs/lhm/bin/python3.13 bootstrap/scaffold.py --manifest` — captured
  before and diffed after.
* `shasum -a 256` over both twin pairs.
* The corpus re-measurement and all four ablations (scope prefix, `plans?`,
  hyphen guard, bare fallback) — **on a quiet tree**, per R12c.

**Note on doc gates**: drift gates catch **drift**, not **absence** of new doc
updates. Confirm the P3 docstring and the changelog entry were actually written;
the gates do not enforce that.

## Plan review — the brief, and whether the Internal round discharges it

*Required — Internal. Implementation does not start until a review has landed
under this heading.*

**Declared tier: `required(Internal)`.** The proposal declared it, the Internal
panel concurred on the doctrine text (`doctrine/dual-review.md` reserves the
different-agent-type round for a high-risk or contract-touching plan; the install
contract is untouched and `gitmeta.py` is none of `AGENTS.md`'s enumerated
high-risk surfaces), and the Decision ratified it: *"OQ3 — the plan-review tier
stays `required(Internal)`."*

**Does the Internal round about to run discharge it? Yes — on one condition,
stated plainly: the reviewer must EXECUTE, not read.** The proposal's Internal
panel recorded that four of its six most serious findings (R2, R3, R5, R6) were
invisible from reading and surfaced only by ablating the proposed regexes against
the live corpus, and that the before/after table *reproduces exactly*, which makes
a reading-only review feel confirmatory while the design decisions underneath go
unchecked. The Decision carried that obligation into this plan. A review that
reports "the tables look right" does **not** discharge the tier; it should be
returned.

**The three questions this review should aim at**, in descending weight:

1. **Is the ~17-tier price still the right trade at 35 proposals?** Re-run the
   pipeline both ways. Confirm 12 `Exact` / 23 `Good` / 0 `Best-effort` under the
   accepted design and 29 / 6 / 0 under the bare fallback. Then say whether the
   Decision's ratification — written when the price was one tier — should be
   re-surfaced to the Maintainer before implementation, or whether the
   zero-wrong-stage guarantee still obviously dominates. **This plan's position
   is that it does and that the design is not reopened**; the reviewer is invited
   to disagree.
2. **Does the hyphen guard earn its place with no corpus evidence?** Reproduce
   the ablation: 0 flips over 246 subjects. Then check T4's two constructed
   probes actually discriminate and T4b's does not. If the guard cannot be
   falsified by anything but hand-built strings, say whether it should stay — it
   is transcribed from a ratified design, so removing it is a Decision-level
   change, but a reviewer should not let "ratified" stand in for "tested".
3. **Do the perturbations in Chunk A perturb the hazard or the test?** Pick two
   at random, run them yourself against the real edited file, and confirm the
   named failure. T8 and T12 are declared non-falsifiable by this diff — check
   that the declaration is honest rather than an excuse, and that no *other* test
   quietly shares the same defect.

Two things a reviewer is invited to strike rather than accept: **T4b**, which is
retained only for continuity with the proposal's test list and falls solely under
a two-part perturbation — a weak vector kept with its weakness labelled, which a
reviewer may reasonably prefer deleted over documented; and the duplication in
**T12** of a guarantee `test_reference_scripts.py` already holds.

> **The landed review appends here as a `### Plan review -- <reviewer> --
> YYYY-MM-DD` sub-heading** (plus a `### Sharpening` sub-heading if it raised
> findings). **Do not rename this heading to a bare `## Plan review`.** The
> planner's gate (`tools/lifecycle_planner.py next <plan>`) matches a section
> *kind*, not a review, so a bare `## Plan review` heading with nothing under it
> satisfies it. This heading is shaped so a placeholder cannot.

## Code review

*Filled in after implementation commits land.* The reviewer is not the
implementing agent. Begin with `**Model**: <model or tier when known; "unknown"
if not. Do not copy-paste old model labels; query and state your actual running
model identity.>` immediately below the section header (or below a
`### Code review -- <reviewer> -- YYYY-MM-DD` sub-heading).

The falsification ledger this review owes, at minimum:

* **Independently re-run at least three of Chunk A's perturbations** rather than
  re-trusting the implementing session's transcript, and confirm each restore was
  byte-identical (`git hash-object <path>` vs `git rev-parse HEAD:<path>`).
* **Diff `_STAGE_COMMIT_PATTERNS` against the pre-change blob** and confirm it is
  byte-unchanged. The whole backward-compatibility argument is that claim, and no
  test enforces it against a widening edit.
* **Confirm the Chunk C lockfile diff is exactly two `hash` lines**, and that the
  two values equal an independently-computed `shasum -a 256`.
* **Confirm the transcription** — read the landed `_SCOPED_STAGE_PATTERNS` block
  against proposal `:833-869` character by character. This is the one chunk where
  a one-character drift is invisible to every test that ships with it.

## Lasting-truth migration

*Filled in at archive time.* Per the
[Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home outside the
plan. **Pre-declared here so archive time is bookkeeping rather than recall:**

| deferred item | durable home at archive |
|---|---|
| The `_git_log_for_path` quiet-degradation hazard (R12c) — a transient `git log` failure returns `[]` and silently downgrades a row with no signal | A new proposal stem under `dev/proposals/`, opened only on the Maintainer's go-ahead under the standing build-nothing-new rule. Until then, a one-line entry under `dev/PLANNING.md > Queued` naming it as a known pre-existing defect. |
| The `Exact`-with-empty-`hours_*` row produced by `_stage_reliability` when a proposal document presents no stage sections | Same `dev/PLANNING.md > Queued` entry, as a second bullet — both are tier-semantics observations about the same module and should not be split across two homes. |
| The one pre-existing shipped-pattern false positive (`review: tighten the recharge bounds` → `reviewed`) | **Already homed** — an explicitly-labelled expectation in T2's table in `bootstrap/tests/test_lifecycle_stage_patterns.py`, with the docstring recording that it is inherited, not chosen. No further migration needed. |
| The ~17-tier price of the ratified narrowing, and whether it warrants revisiting the trade | The archived proposal is Stage 1 and must not be retro-fitted, so this lands as a `dev/PLANNING.md > Queued` line naming it as a Maintainer question, cross-referencing this plan's re-measurement section by stem. If the Maintainer settles it during the plan review or the Decision-to-archive window, the resolution is recorded in the archive record instead and no `Queued` line is created. |
| Nothing guards `_STAGE_COMMIT_PATTERNS` against a future *widening* edit | Named in the archive record's evidence ledger as an accepted residual, not carried forward as work. Adding such a guard is a new test with a new oracle and is out of this plan's scope fence. |
| The transition-lint verdict (the sibling's assigned obligation) | **Already homed** — recorded in the proposal's `## Decision`, which is the durable record. This plan neither re-states nor re-opens it. |

Loop-fidelity sign-off (`doctrine/lifecycle.md` > "Loop-fidelity verification")
is owed at archive: confirm the four ratified plan conditions were each met —
the scoped finalize, twin byte-parity on both pairs, no AST re-anchor, and the
stopping rule (no new CLI, config key, output column, exported helper, or
mandated commit convention).

This section is append-only once written.

## Maintainer fence

Three things this plan does not do without the Maintainer, named so no
implementing session has to decide them mid-flight.

1. **The gate-manifest re-anchor.** Editing the two shipped files makes the
   committed `bootstrap/tests/fixtures/gate_manifest.json` stale for their
   `frozen_files` digests. Today that is harmless: the fixture's `anchor_ref` is
   `null`, no anchored unattended batch is live, and `pytest` compares only a
   freshly-produced manifest. **Re-check `anchor_ref` immediately before Chunk
   A.** If a batch *is* live, **stop** — the edit routes through the supervised
   re-anchor ceremony in `bootstrap/REANCHOR_RUNBOOK.md`, which is
   Maintainer-authored and is not this plan's to run. `bootstrap/REANCHOR_RUNBOOK.md`
   is a serialized shared file and is not edited here in any case.
2. **Commit approval.** Chunks A, B and C touch shipped code, a test, and the
   integrity lockfile — none of them fall under the deliberation-artifact
   carve-in, so each needs explicit maintainer approval before `git commit`, and
   pushing needs approval regardless. Only this plan file and the `dev/PLANNING.md`
   row-move ride the carve-in.
3. **The re-priced trade.** The Decision ratified the narrowing on a corpus where
   it cost one reliability tier; on today's corpus it costs about seventeen. The
   plan **executes the ratified design unchanged** and does not treat this as
   grounds to reopen anything. But the Maintainer should see the number before
   implementation, and if they read it as changing the trade, that is a new
   proposal — not an amendment made inside this plan.
