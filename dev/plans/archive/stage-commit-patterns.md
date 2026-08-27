<!-- One deliberate forward reference: bootstrap/tests/test_lifecycle_stage_patterns.py is the
<!-- ^ Source/sibling proposals archived 2026-08-04. These citations sit in
     append-only sections, so the path is exempted rather than rewritten. -->

     behavioural test this plan creates in Chunk A. It is registered under `Proposed paths:`
     below and named repeatedly outside that block, so it is exempted here as well. -->
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

# Plan: the shipped lifecycle-stage commit vocabulary reads nothing — repair the reader

**Source proposal**: `stage-commit-patterns` (stem
`2026-07-22-claude-stage-commit-patterns`, accepted 2026-07-22 by Maintainer
Decision, *"as revised"*). It currently sits under `dev/proposals/` and moves to
`dev/proposals/archive/` when this plan opens. **All `proposal :<n>` line
citations below are into that file and stay valid across the move**: a proposal
is append-only, so a section's line numbers never shift once committed.
**Status**: archived
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
  **The hazard has a documentation half as well (I9): that same function's
  docstring at `gitmeta.py:33-37` carries a second falsely-exhaustive cause list
  — "git is not available, the repo is not a git checkout, or the path has no
  history" — which omits the `returncode != 0` path at `:50-51` that *is* R12c.
  P3 is not widened to reach it (that file is outside the ratified change set,
  and Chunk B's grep is scoped so it structurally cannot see it), so the
  docstring travels with the behaviour into the same durable home.** Home
  pre-declared in `## Lasting-truth migration`.
* **The `Exact`-with-no-hours row.** `2026-08-03-claude-r6-unused-def-blindspot`
  reports `Exact` with all three `hours_*` empty under the repaired classifier.
  **Mechanism, re-derived this revision — the earlier statement of it was
  wrong.** `_stage_reliability`
  (`templates/modules/default-on/_lifecycle_metrics/gitmeta.py:108-121`) reads
  `if not resolved: 'Best-effort'` / `if present and present.issubset(resolved):
  'Exact'` / else `'Good'`, so an **empty** `present` yields `Good`, *not*
  `Exact` (confirmed on a synthetic repo: a proposal file with no dated stage
  sections and four resolving commits reports `Good`). The real cause is a
  non-empty *proper* subset: that proposal's only dated stage section is
  `## Decision -- … -- 2026-08-03`, so `present = {'decision'}`, while its git
  history resolves `{'open', 'decision'}` — subset holds, tier is `Exact` — and
  every `hours_*` needs an *adjacent pair*, none of which is complete.
  Pre-existing tier semantics, unchanged by this plan, newly *visible* because
  of it. Observation only.
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
`as_of 2026-08-04`, on a quiet tree. **Re-measured in the post-review revision at
`HEAD` `da2d00e` (same day, quiet tree): the corpus is still 35 files / 246
distinct subjects, and every figure in the table below and in (a)–(d) reproduced
to the digit.** The proposal's own figures were measured on
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
reopened.** The narrowing bought what it was ratified to buy — **zero
wrong-stage assignments *on Cairn's own corpus*, whose scoped subjects are
lifecycle transitions by convention** (re-verified in the revision: all 115
classified subjects are genuine transitions), and 9 of the panel's 10
adopter-plausible probes to `None` (the tenth is the pre-existing
shipped-pattern hit named above). **That guarantee does not extend inside the
scope gate** — see **(e)** below, which is the residual the Internal review's
[I1] surfaced and this plan now prices and pins. `Good` is the honest
tier for a row whose subjects the vocabulary cannot read; `Exact` on a guessed
stage is the failure the whole revision exists to prevent. But the Decision's
own summary — *"One reliability tier was surrendered"* — was true of the corpus
it was measured on and is not true of today's, and the Maintainer is entitled to
see that before the change lands. It is raised in `## Plan review — the brief`
as the reviewer's first question and named in the Maintainer fence.

**(b) The hyphen-compound guard now has zero measured effect on the live
corpus — and so do seven of its siblings.** Ablating `(?<!-)` / `(?!-)` from
both scoped patterns and re-running over all 246 subjects flips **0**. This is
not evidence the guard is wrong — it is a consequence of R3: the guard's sole
historical justification (`dev/plans: archive review-record-integrity …`) is now
excluded by the scope gate before the guard is ever reached. The guard is
therefore pinned **only by constructed probes**, and Chunk A says so in the test
docstring rather than implying corpus evidence it does not have.

**The guard is not singular in this, and the earlier draft of this section
implied it was.** Per-literal ablation over all 246 subjects, re-measured in the
revision (I5):

| literal ablated | corpus flips |
|---|---|
| hyphen guards `(?<!-)` / `(?!-)` | **0** |
| `decision` arm 2 (`\|(?<!-)\bmaintainer\s+decision\b(?!-)`) | **0** |
| the *optionality* of `(?:dev/)?` — i.e. requiring `^dev/proposals?\s*:` | **0** |
| the *singular* branch of `proposals?` — i.e. requiring `^(?:dev/)?proposals\s*:` | **0** |
| `(?:ing)?` in `^open(?:ing)?\b` | **0** |
| U+2013 / U+2014 in `_STAGE_PHRASE_SEP_RE` (ASCII `--` only) | **0** |
| `revise` token | **0** |
| `respond\s+to` token | **0** |
| `responses` token | 2 |
| `revised` token | 3 |
| `response` token | 13 |

**Eight literals have zero live constraint, not one.** Every one of them is
retained — they are transcribed from a ratified design and removing one is a
Decision-level change — but the plan now labels them as a class rather than
singling out the guard. Two consequences carried below: `decision` arm 2 is the
widest of them (it searches the whole body, not just the stage phrase) and
supplies two of **(e)**'s worst probes; and the *singular* branch is the direct
cause of the T8 shadowing in **[I6]**.

*Precision note (the ablation is direction-sensitive).* "Ablating `(?:dev/)?`"
means **removing the optionality** — requiring the `dev/` segment — which flips
**0**. Deleting the whole segment (forbidding `dev/`) flips **115**, because
every real Cairn subject carries it; that is a measurement of the prefix, not of
its optional branch, and is not what this row claims.

Verified discriminating probes for the guard:

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

**(e) The residual the scope gate does not reach — measured, and previously
unstated.** Every probe behind this plan's "no commit is ever mislabelled at
`Exact`" claim is a subject the gate *declines*. The panel's 10 adopter probes
are all un-scoped, so `if match is None: return None` disposes of them before
the vocabulary is consulted: they establish that the gate exists, not what
happens inside it. And Cairn's own corpus is clean **by convention** — its
non-lifecycle commits that touch proposal files happen not to carry the prefix,
and the one that does (`proposals: repair four check_cairn issues introduced by
the landed reviews`) escapes only because `reviews` is plural and `\breview\b`
fails on the trailing `s`. That is a coincidence, not a guard.

Fourteen **scoped-but-not-a-transition** probes, run through the transcribed
classifier this revision — **10 of 14 receive a stage**, each of which would
stamp a wrong timestamp and be reported at `Exact`:

| probe | classified |
|---|---|
| `dev/proposals: widget -- still awaiting the maintainer decision on scope` | `decision` |
| `dev/proposals: foo -- Maintainer Decision pending, do not merge` | `decision` |
| `dev/proposals: fix a typo in the review section heading` | `reviewed` |
| `dev/proposals: foo -- fix a broken link in the Review section` | `reviewed` |
| `dev/proposals: foo -- rename the file after the review` | `reviewed` |
| `dev/proposals: foo -- drop the stale review checklist` | `reviewed` |
| `dev/proposals: foo -- correct a claim-check finding in the review record` | `reviewed` |
| `dev/proposals: foo -- add the missing Response heading placeholder` | `revised` |
| `dev/proposals: foo -- update responses table formatting` | `revised` |
| `dev/proposals: opening statement rewritten for clarity` | `open` |
| `dev/proposals: reformat all tables -- no content change` | `None` |
| `dev/proposals: archive the superseded contributor-entry` | `None` |
| `dev/proposals: foo -- revert the accidental revision` | `None` |
| `proposals: repair four check_cairn issues introduced by the landed reviews` | `None` |

The sharp edge is this plan's own scope fence: **"No commit-message convention
is created."** The fix's safety therefore rests on a subject convention the plan
explicitly refuses to document. Cairn keeps it by habit; an adopter installing
`lifecycle-metrics` has been told nothing. For them, "matches the scope prefix"
is a proxy for *touched a proposal file*, not for *is a lifecycle transition*.

**This is not grounds to reopen the Decision and this plan does not treat it as
such.** These 10 are a strict subset of what the bare fallback would
misclassify, so the ratified narrowing is still the better trade — it is the
*size* of the claim, not the design, that was wrong. Three things change instead:
the guarantee above is qualified to Cairn's corpus (see the amended paragraph in
**(a)**), **T2b** below pins the residual with hand-written literals under the
existing oracle rule, and it is registered as known omission **(g)**.

**Lockfile and gate posture, re-verified — both changed since the proposal:**

* `~/conda_envs/lhm/bin/python3.13 bootstrap/verify_integrity.py --target .`
  now exits 1 with **2** violations (`AGENTS.md`,
  `dev/modules/security-review.md`) — not the 41 the proposal measured;
  re-confirmed at `da2d00e`, still exactly those two. The two records this plan
  touches are **current**: the `tools/_lifecycle_metrics/gitmeta.py` record
  spans `dev/.cairn/cairn-lock.yml:496-501` with its `hash`
  (`sha256:5a47849b…`) **on `:499`**, and the
  `tools/_lifecycle_metrics/__init__.py` record spans `:468-473` with its `hash`
  (`sha256:c0e169e7…`) **on `:471`**; both equal the bytes on disk. **The `dst`
  lines are `:498` and `:470` and the `base_hash` lines are `:497` and `:469` —
  an earlier draft of this bullet and of Chunk C's acceptance cited the `dst`
  lines as the hash lines, which would have had an implementer observe the named
  lines *unchanged* after a correct finalize and revert it (I2).** **This is
  precisely the state that makes the scoped finalize mandatory**, exactly as the
  Decision reasoned.
* The **gate-manifest fixture is also current now**, contrary to the proposal's
  measurement:
  `bootstrap/tests/fixtures/gate_manifest.json:2770` freezes `5a47849b…` and
  `:2766` freezes `c0e169e7…`. Editing either file makes the committed fixture
  stale for exactly those two `frozen_files` digests (the `tools/` twins are not
  in `frozen_files` at all). **That staleness is not a `pytest` gate**, verified
  two ways this revision: `bootstrap/tests/test_gate_manifest.py` verifies a
  **freshly produced** manifest (`produced = G.produce(_REPO)`, `:33`) and only
  ever calls `verify()` on `tmp_path` manifests, and no other file under
  `bootstrap/tests/` reads the committed fixture against the live tree.
  **Correction (I3): the committed fixture has no `anchor_ref` key** — its
  top-level keys are `cascade_mutable`, `collection`, `frozen_files`,
  `gate_commands`, `interpreter`, `mapping_symbols`, `phase_mutable`, `schema`.
  `anchor_ref` is a *parameter* of `_gate_manifest.verify()`, supplied by the
  CLI or the re-anchor flow; the durable anchor state is the git ref
  `refs/cairn/gate-anchor` (`bootstrap/tests/_gate_reanchor.py:64`), which
  **exists and points at `e45e1fcc84ded159…`**. A populated ref is the *normal
  standing trust root*, not a stop signal. The performable pre-Chunk-A check is
  in the Maintainer fence.
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
              behavioural test; both gitmeta.py copies              [2177d5f]
2. Chunk B -- P3: the degradation docstring; both __init__.py copies
                                                                    [321ed1a]
3. Chunk C -- the scoped `upgrade --finalize` for the two lockfile records
                                                                    [543f785]
4. Chunk D -- release note + roadmap row (serialized; text returned, owner lands)
                                                        [HELD -- see below]
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
| 16 | — the alternation between them | a regex `\|` joining the two arms — the R2 repair; without arm 2, two of the three Decision forms T6 asserts misclassify. **Both of those two are *constructed* probes, not observed forms** (I5): `-- Maintainer Decision` occurs **0 times in the entire repository log**, and all 36 `Maintainer Decision` subjects are the head-first form arm **1** matches. Arm 2 flips **0 of 246** corpus subjects — it is one of the eight zero-live-evidence literals catalogued at **(b)**, and the widest of them | `:842-843` |
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
| A4 | `bootstrap/tests/test_lifecycle_stage_patterns.py` | **New file.** Tests T1–T12 below, including **T2b** (added in the post-Internal-review revision; same oracle rule, same mechanism, no new surface). Loads the **template** launcher `templates/modules/default-on/lifecycle_metrics.py` via `importlib.util.spec_from_file_location`, the same idiom and for the same recorded reason as `bootstrap/tests/test_lifecycle_metrics_config.py:27-36` (whose own docstring at `:13-16` records the posture) — a new test file is FROZEN-NEW / COLLECTION-ADDED to the gate manifest and needs no re-anchor, whereas `bootstrap/tests/test_reference_scripts.py` is in `frozen_files` and editing it would HOLD. The launcher facade re-exports `_stage_for_subject`, `_resolve_stage_commits` and `proposal_rows` (verified this session), so the test reaches both the private classifier and the public path through one load. |

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
| **T2** no bare-subject fallback | the panel's 10 adopter-plausible subjects: 9 → `None`; `review: tighten the recharge bounds` → `reviewed`, with the docstring labelling it **pre-existing shipped-pattern behaviour, not a choice this fix made** | Delete `if match is None: return None`; fall through with `body = text` | **8 of the 9 `None` expectations flip** to `revised`/`reviewed`/`open`/`decision` (re-measured this revision; the ninth, `docs: address reviewer comments`, stays `None` — `\breview\b` fails on `reviewer`) |
| **T2b** the residual *inside* the gate — the class T2 cannot reach | the 14 **scoped-but-not-a-transition** probes tabulated at **(e)**, as hand-written literals: the 4 `None` expectations are real assertions; the 10 that receive a stage are pinned as **accepted, documented misclassifications**, exactly as T2 already does for `review: tighten the recharge bounds`. Docstring states the point plainly: **the scope gate is a proxy for *touched a proposal file*, not for *is a lifecycle transition*, and Cairn's corpus is clean by an undocumented convention this plan's fence refuses to create** | Widen the scoped `reviewed` pattern (`(?<!-)\breview\b(?!-)` → `(?<!-)\breviews?\b(?!-)`) | the 4 `None` expectations drop to 3: `proposals: repair four check_cairn issues introduced by the landed reviews` flips `None → reviewed`. **Second perturbation, the one that matters for the residual's size:** delete `decision` arm 2 → the two `decision` probes flip (`… still awaiting the maintainer decision on scope` → `None`, `… Maintainer Decision pending, do not merge` → `None`), which is the measurement showing arm 2 is the widest zero-evidence literal |
| **T3** `dev/plans:` never classifies | the 16 live plan-open subjects (15 of the form `dev/plans: open <slug> (+ archive proposal)`, one `dev/plans: open adopter-entry-doc-refresh; archive the accepted proposal`), plus `dev/plans: archive review-record-integrity (Chunk C pointer + lifecycle close)` and `dev/plans: <slug> -- Code review (fresh-context, disclosed scribe)` → all `None`. **Docstring labels the archive vector as inert under this row's own perturbation** (I7) — the same weakness T4b/T8/T12 carry, and it must not be left for a reader to infer, because that subject is the one **(b)** names as the hyphen guard's sole historical justification | Re-add `plans?` to `_STAGE_SCOPE_PREFIX_RE` | 16 corpus subjects flip `None → open` (re-measured this revision: exactly the 16 listed, `Counter({(None,'open'): 16})`); the Code-review probe flips `None → reviewed`. **The archive vector does not flip** — measured all four ways: baseline `None`, `plans?` re-add `None`, hyphen-guard strip `None`, conjunction `reviewed`. It falls only under the conjunction |
| **T4** hyphen-compound guard | `dev/proposals: interpreter-trust-root -- add Security-Review section` → `None`; `dev/proposals: foo -- close out the review-record-integrity thread` → `None`. Docstring records that **no live corpus subject discriminates this guard** (0 flips over 246) and that these are constructed probes | Strip `(?<!-)` / `(?!-)` from the scoped `reviewed` pattern | both flip `None → reviewed` |
| **T4b** the retained weak vector, labelled as one | `dev/proposals: open interpreter-trust-root-fallback (F2 split; Security-Review gated)` → `open`. Kept per R6 for continuity with the proposal's test list. **Its docstring states what it does not pin**: it is green with the guard and without it, and green with `reviewed` moved ahead of `open`. It falls only under the *conjunction* | Remove the hyphen guard **and** move `reviewed` ahead of `open` | flips `open → reviewed`. Under either perturbation alone it stays `open` — measured all four ways this session |
| **T4c** priority order, actually discriminating | `dev/proposals: open widget-thing -- respond to the review` → `open` (head-anchored `open` beats a `revised` token in the stage phrase) | Move `revised` ahead of `open` in `_SCOPED_STAGE_PATTERNS` | flips `open → revised` |
| **T5** one stage per subject | `dev/proposals: licensing -- Response to Gemini External review` → `revised`; `dev/proposals: adopter-entry doc-refresh -- Internal review panel + Response + Revised` → `revised` | Swap `revised` and `reviewed` in `_SCOPED_STAGE_PATTERNS` | both flip `revised → reviewed` |
| **T6** the three Decision forms — **one observed, two constructed** | head-first, slug-first, and slug-first-with-trailing-`review` → `decision`; `dev/proposals: foo -- SUPERSEDE bar` → `None` as a **documented, accepted false negative**. **Docstring states which is which** (I5): only the head-first form (`dev/proposals: Maintainer Decision -- ACCEPT <slug>`) is observed — 36 occurrences, all matched by arm **1**. The two slug-first vectors are constructed: `-- Maintainer Decision` occurs **0 times in the entire repository log**. The word "real" is struck from this row and from the transcription table | Delete arm 2 (`\|(?<!-)\bmaintainer\s+decision\b(?!-)`) | re-measured this revision: `… licensing -- Maintainer Decision -- ACCEPT` → `None`; `… transition-lint -- Maintainer Decision -- ACCEPT (post Internal review)` → **`reviewed`** (the R2 wrong-stage-at-`Exact` bug). The head-first form is unmoved. The perturbation is sound; the *provenance claim* was not |
| **T7a** sharpening false-negative guard | `dev/proposals: <stem> -- Internal review (fresh-context panel) + Sharpening` → `reviewed` | Add `(?!.*\bsharpening\b)` to the **scoped** `reviewed` pattern | flips `reviewed → None` — the R4 widening this design refuses |
| **T7b** shipped exclusion preserved | `Review sharpening pass` → `None` | Delete `(?!.*\bsharpening\b)` from the **shipped** pattern at `gitmeta.py:24` | flips `None → reviewed` |
| **T8** legacy / quickstart forms | the twelve backward-compatibility strings, asserted verbatim, including `Open proposal: README tagline` (`docs/quickstart.md:240`) and `Open proposal alice thing` (`bootstrap/tests/test_reference_scripts.py:476`). **Docstring records the shadowing limit** (I6): because the scope prefix accepts the *singular* `proposals?`, every legacy form beginning `proposal:` is re-matched by the new scoped vocabulary, so T8 cannot see its shipped pattern being deleted | Delete the shipped `open` pattern at `gitmeta.py:18-19` | 3 of its 4 `open` vectors fail; `proposal: open widget` stays `open` — **shadowed**. Measured per shipped pattern this revision: `open` 3 of 4 detected, `revised` **1 of 3** (both `proposal:`-prefixed vectors shadowed, so deleting the *entire* shipped `revised` pattern is invisible to them), `decision` 1 of 2, `reviewed` 1 of 1. So T8 pins the `^Open proposal` / `opening proposal` / `^Decision[:–—-]` / `Revised proposal` / `^Review` arms **and nothing else**. **Stated honestly: T8 is green before *and* after this plan's diff** — backward compatibility is guaranteed by construction, since the shipped patterns are not edited. Its falsifying future state is a later author editing the five arms above |
| **T9** P2, no fall-through | Synthetic `tmp_path` git repo, one proposal file, two commits: `dev/proposals: open widget-thing (first)` then `dev/proposals: open widget-thing again -- respond to the review`. Assert `_resolve_stage_commits` gives `open` = commit 1 and `revised` **is `None`** | Restore a fall-through loop (re-test remaining stages when the classified slot is filled) | `revised` takes commit 2. Docstring records that this is the **only** thing pinning P2 and that the live corpus does not exercise it (0 of 35 file histories differ between the two loop shapes) |
| **T10** end-to-end, public path | Synthetic `tmp_path` repo scaffolded with `lifecycle-metrics`, one proposal file, four commits in the scoped subject form (open / review / response / decision). Assert `stage_timestamp_reliability == 'Exact'` and each `hours_*` **`!= ''` and `isinstance(v, float)` and `>= 0` — never a truthiness assertion** (I8). **Two spec conditions the implementer must not have to rediscover, both measured this revision:** (i) all three deltas are exactly **`0.0`** — four commits in one test run share a committer timestamp — so `assert row['hours_open_to_reviewed']` fails on a falsy float, which is the same fact P3 correction 2 exists to document; (ii) the synthetic proposal file **must carry dated stage sections** (`## Review -- … -- <date>`, `## Response -- …`, `## Decision -- …`), because `stage_present` is derived from the *document*, and a bare file yields **`Good`**, not `Exact` — measured both ways | Revert `gitmeta.py` to `HEAD` | `Best-effort`, all `hours_*` empty. **Never asserts a tier against the live Cairn corpus** — R12c's quiet-tree hazard makes that non-reproducible under load |
| **T11** never raises | `''`, `'   '`, a separator-only subject, a prefix-only subject, non-ASCII (`dev/proposals: ünïcödé revisé`), and a 500-character subject → all return without raising | Replace `phrase = parts[1] if len(parts) > 1 else body` with an unconditional `parts[1]` | `IndexError` on **3 of the 6** vectors — the three that carry the scope prefix. `''`, `'   '` and the separator-only subject return `None` at `if match is None: return None`, *before* the split (I8: the earlier claim of "every separator-less subject" was measured wrong). The test still reds; the perturbation is valid, its stated reach was not |
| **T12** degradation preserved | A `tmp_path` scaffold with **no** `.git` → `Best-effort`, all `hours_*` empty. Deliberately duplicates `bootstrap/tests/test_reference_scripts.py:443-457` so the guarantee is local to the changed code | Seed a stage unconditionally in `_resolve_stage_commits` (`out['open'] = ('x', <now>)` before the loop) | tier flips to `Exact` on a repo with no history. **Stated honestly: no change in this plan's own diff can red T12** — it re-asserts a pre-existing guarantee |

**Acceptance criteria — Chunk A.**

* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_lifecycle_stage_patterns.py -q`
  → all pass, 0 skipped.
* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests -q` → **no *new*
  failure relative to a baseline measured immediately before the commit on a
  quiet tree**, `0 skipped`, collection grows by exactly the new nodes and drops
  none. **Not "green" unconditionally (I4):** the suite is red today from
  sibling workflows' uncommitted `bootstrap/_scaffold/` work, and a criterion
  that cannot be met is a criterion that gets waived. Measured in this revision
  at `HEAD` `da2d00e`: **2 failed, 1788 passed, 0 skipped**, both failures
  `bootstrap/tests/test_ast_attest.py`
  (`test_committed_baseline_accounted_for_across_the_engine_package`,
  `test_ast_gate_passes_over_the_full_scaffold_module_set`).
  * **The baseline is measured, never carried forward — including from this
    plan.** The Internal review recorded `4 failed, 1777 passed` a few hours
    earlier, naming two `bootstrap/tests/test_profile_grammar.py` nodes that are
    green again by `da2d00e`. A pinned list of failing node IDs decays inside a
    day on this tree, so this plan does not pin one; the implementer measures at
    the commit and records the pair (baseline, post-change) in the commit body.
  * Not carried forward from the proposal's `1437` either, which is two months
    and many landings stale.
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
  an install-manifest row. **Labelled non-falsifiable by this diff, alongside T8
  and T12 (I10):** the entire matching output is the single row
  `tools/_lifecycle_metrics/gitmeta.py<TAB>modules/default-on/_lifecycle_metrics/gitmeta.py<TAB>verbatim`
  — `dst`, `src`, mode, **no digest and no size**, so no content edit can move
  it. Measured this revision. It is kept because it guards the *mapping*, which
  the scope fence also forecloses; it is not a third independent guard and must
  not be counted as one.
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
* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests -q` → **no *new*
  failure relative to a baseline measured immediately before the commit on a
  quiet tree**, `0 skipped`
  (`test_every_self_hosted_twin_stays_byte_identical_to_its_source` is the node
  that matters here, and it must be **green**, not merely un-regressed).
  **Not "green" unconditionally (I4).** An earlier draft of this revision
  restated Chunk A's criterion and the plan-level one but left this one reading
  "→ green" — two of the three the review named. That is not cosmetic: the suite
  is red today from sibling workflows' uncommitted `bootstrap/_scaffold/` work
  (**2 failed, 1788 passed, 0 skipped** at `da2d00e`), and *Acceptance criteria*
  states plainly that "per-chunk criteria are above", so the corrected
  plan-level wording does **not** override this line. An implementer executing
  Chunk B would read "→ green", see red, and either waive the criterion or
  block — the exact disarmed-check failure [I4] exists to prevent, surviving
  inside the fix for it.
* `~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py` → clean.
* `~/conda_envs/lhm/bin/python3.13 -c "import sys; sys.path.insert(0,'tools'); import _lifecycle_metrics"`
  → imports cleanly (a docstring edit that breaks the triple-quote would fail
  here before it reached the suite).
* **No perturbation test.** B is prose in a docstring; there is no behaviour to
  falsify. Said explicitly rather than left as an unexplained gap — the guard is
  the twin-parity test and the import check, and neither is evidence about the
  *content* of the sentence. The reviewer reads it.
* **The old sentence must not survive anywhere.** `grep -rn "the default branch
  is named" templates/ tools/` returns only the corrected text. **Scope limit,
  stated rather than left implicit (I9):** that grep matches exactly
  `templates/modules/default-on/_lifecycle_metrics/__init__.py:75` and its twin
  (verified this revision), so it **cannot** see the *second* falsely-exhaustive
  cause list in this module — `_git_log_for_path`'s own docstring at
  `gitmeta.py:33-37`, which omits the `returncode != 0` path at `:50-51`. That
  is deliberate: reaching it would widen P3 past the ratified change set. It is
  homed with R12c in `## Lasting-truth migration` instead, so the archive does
  not orphan it.

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
  `"hash":` — **`:471`** (the `tools/_lifecycle_metrics/__init__.py` record) and
  **`:499`** (the `tools/_lifecycle_metrics/gitmeta.py` record). **Corrected
  from `:470` / `:498`, which are the records' `dst` lines and do not move
  (I2)**: an implementer checking the old numbers literally would observe them
  unchanged after a *correct* finalize and, on this chunk's own "a different
  number means the scope did not bind" rule, have grounds to revert a
  Decision-mandated write. Line numbers verified at `HEAD` `da2d00e`; re-derive
  them by `grep -n` on the `dst` values rather than trusting these figures, and
  anchor the check on the two **records**, not on absolute line numbers. Any
  `base_hash` (`:469`, `:497`), `src`, `dst`, `verbatim`, or `living_state`
  movement is a defect of this chunk. (`base_hash` is already present on both
  records, so the engine's "preserve-the-as-shipped-baseline" branch is a no-op
  here — verified.)
* The two new `hash` values equal `sha256:` + the `shasum -a 256` of the
  post-Chunk-A/B files. Checked against a shell hash, not against the tool's own
  output.
* `~/conda_envs/lhm/bin/python3.13 bootstrap/verify_integrity.py --target .`
  reports **no violation naming either `_lifecycle_metrics` path**. It will still
  exit 1 while `AGENTS.md` and `dev/modules/security-review.md` remain
  mismatched — pre-existing, not this plan's, and **not** to be swept in. Record
  the before/after violation lists side by side in the commit body so the
  delta is legible.
* **Re-run the four engine preconditions immediately before finalizing (I11).**
  The finalize path traverses **another workflow's uncommitted engine code**:
  `bootstrap/_scaffold/upgrade.py` and `bootstrap/_scaffold/lockfile.py` both
  carry uncommitted changes, and `cmd_upgrade` reaches the unlanded
  `trusted_upstream(...)` / `forked_facade_findings(..., upstream=…)` path at
  `bootstrap/_scaffold/upgrade.py:2225-2226` **before** the `--finalize`
  dispatch at `:2230-2232`. Verified in the plan's favour at `HEAD` `da2d00e`,
  and every one of these is a statement about *uncommitted* bytes that can
  change under this plan, so each is re-checked at execution time rather than
  cited:
  1. `_cmd_finalize_lockfile` (`upgrade.py:1612`) is **AST-identical to `HEAD`**
     (checked by comparing `ast.dump` of the function against
     `git show HEAD:bootstrap/_scaffold/upgrade.py`); `cmd_upgrade` is **not**.
  2. `_emit_lock_yaml(read_lockfile(Path('.')))` round-trips the committed
     lockfile **byte-identically** (24925 bytes in, 24925 out, equal) — this is
     what makes "exactly two lines" achievable at all.
  3. The scope filter matches on `dst`, which is exactly the two paths named.
  4. The `core/VENDOR.md` rename-resolution branch, which runs *before* the
     scope filter and could silently rewrite a third line, is inert here: that
     record's `dst` is already `CLAUDE.md` and the file exists.

  If (1) or (2) no longer holds, **stop and re-sequence** rather than
  finalizing — see Maintainer fence item 2.
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
>   ablations, do not read-only) — landed 2026-08-04, REVISE, eleven findings,
>   all dispositioned in the plan. Two observations the plan surfaces rather
>   than settles: the price of the ratified narrowing is now ~17 reliability
>   tiers on the live corpus, not the one measured at Decision time; and the
>   scope gate's safety rests on a subject convention the fix deliberately does
>   not document.

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
    suite under the canonical interpreter (3.13.13), **0 skipped, and no *new*
    failure against a baseline measured on a quiet tree immediately before the
    first implementing commit**. **Not an unconditional green (I4)** — see
    Chunk A's criterion for why, and for the measured `2 failed, 1788 passed, 0
    skipped` at `HEAD` `da2d00e`. **Not** carried forward from the proposal's
    `1437 passed` (2026-07-22), nor from this plan's own figures.
  * `bootstrap/tests/test_lifecycle_stage_patterns.py` — T1–T12 (incl. T2b),
    new file.
  * [`bootstrap/tests/test_notice_install.py`](../../bootstrap/tests/test_notice_install.py)
    — unchanged and green; it is what enforces both twin pairs.
  * [`bootstrap/tests/test_reference_scripts.py`](../../bootstrap/tests/test_reference_scripts.py)
    — unchanged and green. It is in the gate manifest's `frozen_files`; **it is
    not edited**, which is why T1–T12 land in a new file.
  * [`bootstrap/tests/test_ast_attest.py`](../../bootstrap/tests/test_ast_attest.py)
    — **unchanged, and its result unchanged relative to the pre-change
    baseline**. **Not "green" (I4).** It is red today from sibling `_scaffold`
    work, and "green" is exactly the phrasing that gets waived as
    "pre-existing, not mine" — which retires the one instrument the scope
    fence's "no AST re-anchor" claim rests on. The invariant is therefore
    checked **structurally**, in a form that survives a red neighbour:
    `git diff HEAD --stat -- bootstrap/_scaffold/` shows no line attributable to
    this plan, and the attestation's CHANGED / MISSING symbol list contains no
    symbol from `_lifecycle_metrics`. Measured at `HEAD` `da2d00e`: the six
    reported symbols are `_minimal_yaml_parse` and `load_config`
    (`bootstrap/_scaffold/config.py`), `cmd_upgrade`
    (`bootstrap/_scaffold/upgrade.py`), `forked_facade_findings` and
    `format_forked_facade_warning` (`bootstrap/_scaffold/lockfile.py`), and one
    `MISSING Try` — every one of them another workflow's, none in
    `_lifecycle_metrics`. That is the check; the green/red bit is not.
  * **Every new test shown non-vacuous by a run perturbation**, ledger in the
    commit body. Where a test cannot be made to fail by this plan's own diff
    (T8, T12) the plan says so above instead of claiming a guard it does not
    have — as does the `--manifest` criterion in Chunk A, which joined that list
    in this revision (I10).
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
  * *A **scoped** subject that is not a lifecycle transition may still receive a
    stage.* **This is a priced residual, not an invariant** — 10 of 14 measured
    probes classify (see **(e)**). Pinned as documented outcomes by T2b; RED
    under a widening of the scoped `reviewed` pattern. Named here because the
    ledger below previously implied the opposite.
  * *A `dev/plans:` subject classifies as nothing.* Enforced by T3; RED under
    the `plans?` re-add, 16 corpus subjects flipping.
  * *`_STAGE_COMMIT_PATTERNS` is byte-unchanged.* Enforced **structurally** (the
    diff), checked once in Chunk A's acceptance, and pinned in one direction by
    T7b and T8. **Not guarded by a test that fails when a future author edits
    it** — T8 catches a *deletion*, not a widening, **and not even every
    deletion (I6): the scoped vocabulary shadows the `proposal:`-prefixed
    legacy forms, so T8 sees 3 of 4 `open` vectors, 1 of 3 `revised`, 1 of 2
    `decision`, 1 of 1 `reviewed` — deleting the whole shipped `revised` pattern
    is invisible to both of its shadowed vectors.** A real guard is one line —
    assert `_STAGE_COMMIT_PATTERNS` against a hand-written literal tuple of the
    four pattern strings — but that is a new oracle and sits outside this scope
    fence. Stated because it is the claim a reviewer should attack.
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
    each have their own perturbation-verified test (T2, T4, T5, T6). **T2, T4,
    T5 and T6 pin the gate, the guard, the priority order and the Decision arms
    — they do not pin vocabulary looseness *inside* the gate, and the earlier
    wording of this bullet read as if they did (I1).** Inside the gate the
    vocabulary is as loose as the panel found it — `\breview\b` anywhere in the
    stage phrase, `\bresponse\b` anywhere, `maintainer\s+decision` anywhere in
    the body — and 10 of 14 measured scoped non-transition probes land a stage.
    That residual is pinned by **T2b** and priced at **(e)**; it is accepted,
    not eliminated.
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
  (g) **The scoped-but-not-a-transition residual.** Inside the scope gate the
  vocabulary is loose, and **10 of 14 measured probes receive a stage** (**(e)**).
  The zero-wrong-stage evidence base does not reach this class: the panel's 10
  adopter probes are all un-scoped, and Cairn's own corpus is clean by an
  undocumented subject convention that this plan's fence explicitly declines to
  create. T2b pins the residual as documented outcomes; nothing eliminates it,
  and an adopter's tree has no reason to share Cairn's convention.
  (h) **Eight of the transcribed literals have zero live corpus constraint**
  (**(b)**), not just the hyphen guard. Each is a widening surface with no
  measured check; all are retained because removing one is a Decision-level
  change, and all are now labelled rather than one being singled out.

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
| The `_git_log_for_path` quiet-degradation hazard (R12c) — a transient `git log` failure returns `[]` and silently downgrades a row with no signal — **and its documentation half: the same function's docstring at `gitmeta.py:33-37` carries a second falsely-exhaustive cause list that omits the `returncode != 0` path at `:50-51`** (I9) | A new proposal stem under `dev/proposals/`, opened only on the Maintainer's go-ahead under the standing build-nothing-new rule. Until then, a one-line entry under `dev/PLANNING.md > Queued` naming it as a known pre-existing defect. **The entry names both halves** — the behaviour and the docstring — so the archive does not orphan the second cause list, which Chunk B's grep is structurally scoped not to see. |
| The `Exact`-with-empty-`hours_*` row produced by `_stage_reliability` when a proposal's dated stage sections are a **non-empty proper subset** of the stages its git history resolves (r6-unused-def-blindspot: `present = {'decision'}`, `resolved = {'open','decision'}`) | Same `dev/PLANNING.md > Queued` entry, as a second bullet — both are tier-semantics observations about the same module and should not be split across two homes. |
| The scoped-but-not-a-transition residual — 10 of 14 measured probes classify inside the gate, and the safety of the gate rests on an undocumented subject convention (**(e)**, known omission (g)) | **Already homed** — pinned as documented outcomes in T2b's literal table in `bootstrap/tests/test_lifecycle_stage_patterns.py`, priced at **(e)**, and registered as known omission (g). Whether an adopter-facing safety claim may rest on an undocumented convention is a doctrine question, not this plan's; if the Maintainer wants it pursued it is a new proposal, not an amendment here. |
| The eight transcribed literals with zero live corpus constraint (**(b)**, known omission (h)) | Named in the archive record's evidence ledger as an accepted residual. Every one is transcribed from a ratified design, so narrowing any of them is a Decision-level change and is not carried forward as work. |
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
   committed `bootstrap/tests/fixtures/gate_manifest.json` stale for their two
   `frozen_files` digests (`:2766`, `:2770`; the `tools/` twins are not in
   `frozen_files`). Today that is harmless — but **the check this item used to
   name could not be performed (I3)**: the committed fixture has **no
   `anchor_ref` key**, so "re-check that `anchor_ref` is `null`" was an
   instruction an implementer would have had to skip or improvise, on the item
   that gates a Maintainer-only trust-root ceremony. Replaced by three checks
   that can actually be run, immediately before Chunk A:
   * **`git for-each-ref refs/cairn/gate-anchor`** — this is the durable anchor
     state (`bootstrap/tests/_gate_reanchor.py:64`,
     `bootstrap/tests/_gate_preflight.py:53`). **A populated ref is the normal
     standing trust root and is NOT a stop signal** — it points at
     `e45e1fcc84ded159…` today. Record what it points at; a *move* between the
     pre-check and the commit is the signal.
   * **Confirm no consumer of the committed fixture has appeared**:
     `grep -rn "fixtures/gate_manifest" bootstrap/tests/*.py`.
     `bootstrap/tests/test_gate_manifest.py` verifies a **freshly produced**
     manifest (`G.produce(_REPO)`, `:33`) and calls `verify()` only on
     `tmp_path` manifests, so the committed artifact is not a `pytest` gate —
     re-confirm rather than inherit.
   * **Ask whether a supervised re-anchor ceremony is in flight** per
     `bootstrap/REANCHOR_RUNBOOK.md` Phase 0. That state is a Maintainer-run
     ceremony, not a repository flag, and no command reports it. If one is,
     **stop** — the edit routes through that runbook, which is Maintainer-
     authored and is not this plan's to run. `bootstrap/REANCHOR_RUNBOOK.md` is
     a serialized shared file and is not edited here in any case.
2. **Commit approval — and sequencing against the concurrent `_scaffold` work.**
   Chunks A, B and C touch shipped code, a test, and the integrity lockfile —
   none of them fall under the deliberation-artifact carve-in, so each needs
   explicit maintainer approval before `git commit`, and pushing needs approval
   regardless. Only this plan file and the `dev/PLANNING.md` row-move ride the
   carve-in. **Added after the Internal review (I4, I11): whether Chunks A/B/C
   wait on the sibling `bootstrap/_scaffold/` work landing is a Maintainer
   sequencing call, not an implementer's.** Two concrete reasons: the suite is
   red today from that work, so "no new failure vs. baseline" is the only
   honest gate and the AST invariant must be checked structurally; and Chunk C's
   finalize executes `cmd_upgrade`, which is *itself* among the uncommitted
   engine files. Neither is a defect in this plan; both are conditions an
   implementing session should not resolve alone.
3. **The re-priced trade, and the residual behind it.** The Decision ratified
   the narrowing on a corpus where it cost one reliability tier; on today's
   corpus it costs about seventeen (12 `Exact` / 23 `Good` under the accepted
   design vs. 29 / 6 under the bare fallback — reproduced in this revision at
   `HEAD` `da2d00e`). The plan **executes the ratified design unchanged** and
   does not treat this as grounds to reopen anything. But the Maintainer should
   see the number before implementation, and if they read it as changing the
   trade, that is a new proposal — not an amendment made inside this plan.

   **Two things the Maintainer should see alongside the number**, added after
   the Internal review:
   * The 17 tiers the bare fallback buys are bought *by classifying subjects it
     cannot read* — the wrong-stage-at-`Exact` hazard R1 blocked. Measured at
     n=1 when the Decision ratified it and at n=17 today, the trade points the
     same way; the re-pricing is evidence the narrowing is working, not
     evidence against it.
   * **The gate is not as tight as the guarantee implied (I1).** 10 of 14
     scoped-but-not-a-transition probes receive a stage (**(e)**). Cairn's own
     corpus is clean by a subject convention this plan's fence explicitly
     refuses to document, and an adopter has no reason to share it. The plan
     now qualifies the claim, pins the residual with T2b, and registers it as
     known omission (g). **Whether an adopter-facing safety claim may rest on
     an undocumented convention is a Maintainer/doctrine question, and — like
     the re-priced trade — a new proposal if it is to be pursued, not an
     amendment made inside this plan.**

## Plan review -- Claude (Internal, same-agent-type; security lens) -- 2026-08-04

**Model**: Claude Opus 5 (`claude-opus-5`).

*Placement note.* The `## Plan review — the brief` block above asks for a
`### Plan review -- <reviewer> -- YYYY-MM-DD` sub-heading under that section;
this round was directed to append at the end of the file. Relocating this
section under that heading is a pure move and loses nothing. Dated `2026-08-04`
to match the plan's own `**Opened**` and `as_of` — a review dated before the
artifact it reviews is a record defect.

**Standing — no cross-type independence.** Same agent type as the plan's author
(both Claude). This is the Internal floor `doctrine/dual-review.md` sets — the
same agent in a fresh session — and nothing more. The threat model I bring is
the author's, and a blind spot they have I probably share. Concretely: the
author and I both reason about this classifier as an artifact of *Cairn's own*
commit corpus. The one finding below that steps outside that frame (**[I1]**)
came from deliberately hunting the gap the brief pointed at, not from an
independent instinct; a different-agent-type reader would likely have reached it
sooner, and may reach others I did not.

**Does this discharge the declared tier? Yes.** The proposal declared
`required(Internal)`, the Decision ratified it, and the plan attached an
*execution* obligation rather than a reading one. That obligation is discharged:
every headline figure, all four ablations, all twelve tests' named
perturbations, three synthetic-repo tests, both required checkers, and the full
engine suite were **run**. Real output is in `### Covered`. Nothing below asks
to reopen the Decision, and I explicitly decline the invitation in brief-question
1 (see the reply to it at the end of `### Covered`).

### Steelman

This is the most honestly-measured plan I have read in this tree, and it is
strong on precisely the axis the Decision told it to be strong on. The
re-measurement section is not decoration: three figures moved materially since
2026-07-22, and the author put the one that cuts *against* the change — the
price of the ratified narrowing going from one tier to roughly seventeen — at
the top, in its own labelled subsection, with a Maintainer-fence item attached,
rather than leaving a reviewer to discover it. I reproduced all four pipeline
figures and all three named ablations to the digit; nothing in that section is
wrong.

The transcription framing is the right instrument for the right failure mode.
This chunk's realistic defect is a one-character regex drift that every test
shipping alongside it would pass, so turning P1 into a 30-row checklist keyed to
numbered source lines — and telling the Code review to read it character by
character — is proportionate, not ceremony. Every one of those 30 rows resolves
correctly against `dev/proposals/2026-07-22-claude-stage-commit-patterns.md`; I
checked all of them.

The **oracle rule** ("every expected value is a hand-written literal in the test
file… A test whose expected set is the subject's own data structure is green
forever") is stated once, binding, and is exactly the right answer to this
repository's recurring failure — the artifact under verification supplying the
material used to verify it. Chunk C carries the same discipline without a test
to hide behind: its acceptance names a shell hash and a before/after violation
list, both produced outside the tool. And the plan repeatedly labels its own
weak vectors (T4b, T8, T12) rather than letting them pass as coverage. The
findings below are, in large part, an argument that it should apply that same
labelling discipline in four more places where it currently does not.

### Concerns

---

**[I1] — The scope gate is the entire safety argument, and every probe
supporting the "zero wrong-stage" claim is one the gate disposes of by
construction. The residual — *scoped* subjects that are not lifecycle
transitions — is unmeasured and untested.**

The plan asserts, in its own voice and as re-measured evidence: *"The narrowing
bought what it was ratified to buy — zero wrong-stage assignments, and 9 of the
panel's 10 adopter-plausible probes to `None`."* The failure-mode ledger repeats
it: a wrong stage at `Exact` is *"the one failure mode worse than the status
quo, which is why the scope gate, the phrase restriction, the hyphen guard and
the priority order each have their own perturbation-verified test (T2, T4, T5,
T6)."*

The evidence base for that claim is two things, and neither reaches the
residual:

1. **The panel's 10 adopter probes are all *un*scoped.** Not one matches
   `_STAGE_SCOPE_PREFIX_RE`, so `if match is None: return None` disposes of them
   before the vocabulary is consulted. They test that the gate exists. They
   cannot test what happens *inside* it.
2. **Cairn's own 246-subject corpus is clean only by convention.** Cairn's
   non-lifecycle commits that touch proposal files happen not to carry the
   prefix (`claim-marker maintenance: …`, `agent-context-scrub: the Internal
   Response that should have preceded the Decision`), and the one that does —
   `proposals: repair four check_cairn issues introduced by the landed reviews`
   — escapes only because `reviews` is plural and `\breview\b` fails on the
   trailing `s`. That is a coincidence, not a guard.

Inside the gate the vocabulary is as loose as the panel found it: `\breview\b`
anywhere in the stage phrase, `\bresponse\b` anywhere, `maintainer\s+decision`
anywhere in the body. I ran 14 scoped-but-not-a-transition probes through the
transcribed classifier. **10 of 14 receive a stage** — each of which would stamp
a wrong timestamp and be reported at `Exact`:

| probe | classified |
|---|---|
| `dev/proposals: widget -- still awaiting the maintainer decision on scope` | `decision` |
| `dev/proposals: foo -- Maintainer Decision pending, do not merge` | `decision` |
| `dev/proposals: fix a typo in the review section heading` | `reviewed` |
| `dev/proposals: foo -- fix a broken link in the Review section` | `reviewed` |
| `dev/proposals: foo -- rename the file after the review` | `reviewed` |
| `dev/proposals: foo -- drop the stale review checklist` | `reviewed` |
| `dev/proposals: foo -- correct a claim-check finding in the review record` | `reviewed` |
| `dev/proposals: foo -- add the missing Response heading placeholder` | `revised` |
| `dev/proposals: foo -- update responses table formatting` | `revised` |
| `dev/proposals: opening statement rewritten for clarity` | `open` |
| `dev/proposals: reformat all tables -- no content change` | `None` |
| `dev/proposals: archive the superseded contributor-entry` | `None` |
| `dev/proposals: foo -- revert the accidental revision` | `None` |
| `proposals: repair four check_cairn issues introduced by the landed reviews` | `None` |

The sharp edge is the scope fence's own rule: **"No commit-message convention is
created."** The fix's safety therefore rests on a subject convention that the
plan explicitly refuses to document. Cairn keeps that convention by habit; an
adopter who installs `lifecycle-metrics` has been told nothing and has no reason
to. For them, "matches the scope prefix" is not a proxy for "is a lifecycle
transition" — it is a proxy for "touched a proposal file".

**Not a design objection, and not grounds to reopen.** The 10 above are a *strict
subset* of what the bare fallback would misclassify, so the ratified narrowing is
still the right call and I am not asking to change a regex. What I am asking is
that the plan stop stating a guarantee its evidence does not reach, and pin the
residual instead:

* **Add a T2b vector class** to `bootstrap/tests/test_lifecycle_stage_patterns.py`:
  ~8 scoped-but-not-a-transition subjects with hand-written literal
  expectations — recording the misclassifying ones as *accepted, documented*
  outcomes exactly as T2 already does for `review: tighten the recharge bounds`,
  and the `None` ones as real assertions. Same oracle rule, no new mechanism, no
  Decision surface. Perturbation that reds it: any widening of the scoped
  `reviewed` / `revised` patterns.
* **Soften the two claims.** "Zero wrong-stage assignments" → "zero wrong-stage
  assignments *on Cairn's own corpus*, whose scoped subjects are lifecycle
  transitions by convention". And in the failure-mode ledger, note that T2/T4/T5/
  T6 pin the gate, the guard, the priority order and the Decision arms — but that
  nothing pins vocabulary looseness *inside* the gate.
* **Add a `(g)` to "Known omissions"**: the residual above, with the count.

---

**[I2] — Chunk C's two lockfile line citations point at the `dst` lines, not the
`hash` lines. An implementer following the acceptance criterion literally reads
a false negative on a Decision-mandated write.**

The plan states: *"`dev/.cairn/cairn-lock.yml:498` records `sha256:5a47849b…`
for `tools/_lifecycle_metrics/gitmeta.py` and `:470` records `sha256:c0e169e7…`
for `tools/_lifecycle_metrics/__init__.py`"*, and Chunk C's acceptance requires
*"`git diff dev/.cairn/cairn-lock.yml` touches **exactly two lines**, both
`"hash":`, in the records at `:470` and `:498`."*

Measured at `HEAD` `eacb7dd`:

```
470:       "dst": "tools/_lifecycle_metrics/__init__.py",
471:       "hash": "sha256:c0e169e79956e1612501517dfd150c5917cb88de1078ef07c8151b878eaf3db5",
498:       "dst": "tools/_lifecycle_metrics/gitmeta.py",
499:       "hash": "sha256:5a47849b9937e4fa17a32d4eb9e28968466d880c454a7813281d2cc7401bf1a0",
```

`:470` and `:498` are `dst` lines. The hashes are at `:471` and `:499`. The
finalize will change 471 and 499 and leave 470 and 498 untouched — so an
implementer checking the criterion as written observes the named lines
*unchanged* and, on the plan's own stated rule ("a different number means the
scope did not bind and the change is reverted, not committed"), has grounds to
revert a correct write. Two-character fix; it is in the one chunk the Decision
made mandatory and the one with no test behind it.

*(The record-anchored reading — "the records at :470 and :498" — is defensible in
the acceptance criterion, but the earlier sentence says the line "records
`sha256:…`", which is not.)*

---

**[I3] — The Maintainer fence's gate-manifest check names a field that does not
exist in the file it names, and the state that *does* hold the anchor is
non-null.**

The plan asserts twice — in the re-measurement section and in Maintainer fence
item 1 — that *"the committed fixture's `anchor_ref` is `null`"*, and instructs:
*"**Re-check `anchor_ref` immediately before Chunk A.**"*

`bootstrap/tests/fixtures/gate_manifest.json` has **no `anchor_ref` key**. Its
top-level keys are `cascade_mutable`, `collection`, `frozen_files`,
`gate_commands`, `interpreter`, `mapping_symbols`, `phase_mutable`, `schema`.
`anchor_ref` is a *parameter* to `bootstrap/tests/_gate_manifest.py`'s
`verify()`, supplied by the CLI or the re-anchor flow. The durable anchor state
is the git ref `refs/cairn/gate-anchor`, and in this repository it **exists and
points at `e45e1fcc`** — the opposite signal from the one the fence's phrasing
leads a reader to expect.

**The plan's conclusion is nonetheless correct, and I verified it
independently**: no pytest test reads the committed fixture against the live
tree. `bootstrap/tests/test_gate_manifest.py` produces a fresh manifest
(`G.produce(_REPO)`, `:33`) and only ever calls `verify()` on `tmp_path`
manifests; grep over `bootstrap/tests/*.py` finds no other consumer of the
committed artifact. Editing the two shipped files does stale exactly two
`frozen_files` digests (`bootstrap/tests/fixtures/gate_manifest.json:2766` and
`:2770`, both verified) and the `tools/` twins are not in `frozen_files` at all,
so the blast radius is two entries and no gate.

So this is a *wrong instrument, right answer*. Rewrite the fence to name the
check that can actually be performed — `git for-each-ref refs/cairn/gate-anchor`
plus "is a supervised re-anchor batch in flight per
`bootstrap/REANCHOR_RUNBOOK.md`" — because a fence item an implementer cannot
execute will either be skipped or improvised, and this one gates a
Maintainer-only trust-root ceremony.

---

**[I4] — The engine suite is RED on today's tree, and one of the four failures is
`test_ast_attest.py` — the plan's own instrument for its "no AST re-anchor"
invariant.**

`~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests -q` at `HEAD`
`eacb7dd`, canonical interpreter 3.13.13:

```
FAILED bootstrap/tests/test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package
FAILED bootstrap/tests/test_ast_attest.py::test_ast_gate_passes_over_the_full_scaffold_module_set
FAILED bootstrap/tests/test_profile_grammar.py::TestResolveCurrentProfileIsAudible::test_unreadable_profile_names_what_it_swallowed
FAILED bootstrap/tests/test_profile_grammar.py::TestResolveCurrentProfileIsAudible::test_ungrammatical_profile_names_what_it_swallowed
4 failed, 1777 passed, 3 warnings in 144.00s
```

The AST failures are **not this plan's** — they are other workflows' uncommitted
`bootstrap/_scaffold/` edits (`note: NEW FunctionDef:_assert_mapping_ownership
(upgrade.py)`, `assert_always_on_complete` / `missing_always_on_sources`
(install.py), `missing_required_tokens` (config.py)). `git status --short` shows
nine modified engine files and two untracked test files.

But three of the plan's acceptance criteria are written as unconditional greens:

* Chunk A: *"`pytest bootstrap/tests -q` → green, 0 failed / 0 skipped"*
* Chunk B: *"`pytest bootstrap/tests -q` → green"*
* Plan-level: *"`bootstrap/tests/test_ast_attest.py` — unchanged and green,
  **confirming no re-anchor was triggered**."*

None is achievable today. The third is the dangerous one: the plan's scope fence
claims "no AST re-anchor" and cites `test_ast_attest.py` as what confirms it. An
implementer who runs it, sees red, and files the redness as "pre-existing, not
mine" has just retired the exact instrument that would catch an unintended
engine change. That is the recurring failure pattern in a new dress — the check
disarmed by a condition it was not designed to distinguish.

Two fixes, both cheap: (a) record a **named pre-existing-failure baseline** in
the plan (these four node IDs, at this HEAD, from these workflows) and restate
the criteria as "no *new* failures relative to that baseline, and the four named
ones unchanged"; (b) for the AST invariant specifically, replace "green" with a
check that survives a red neighbour — `git diff HEAD --stat -- bootstrap/_scaffold/`
shows no line attributable to this plan, plus the `verify()` note list contains
no symbol from `_lifecycle_metrics`. Also worth naming in Maintainer fence item
2: Chunks A/B may need to wait on the `_scaffold` work landing, which is a
sequencing decision, not an implementer's call.

*(For the record: `0 skipped` does hold today — the run reports no skips.)*

---

**[I5] — Arm 2 of the `decision` pattern is in exactly the position the plan
flags for the hyphen guard — zero corpus effect, constructed probes only — and
the plan gives it a *stronger* justification than the corpus supports. It is one
of at least six such literals; singling out the guard misleads.**

The plan is scrupulous at **(b)**: the hyphen guard *"now has zero measured
effect on the live corpus"*, *"pinned **only by constructed probes**, and Chunk A
says so in the test docstring rather than implying corpus evidence it does not
have."* Reproduced: **0 flips over 246**.

Transcription row 16 justifies arm 2 as: *"the R2 repair; without arm 2, **two of
the three real Decision forms** misclassify"*, and T6 asserts *"all three **real**
Decision forms"*. Measured:

* Ablating arm 2 (`|(?<!-)\bmaintainer\s+decision\b(?!-)`) flips **0 of 246**
  corpus subjects.
* `-- Maintainer Decision` (the slug-first form) occurs **0 times** in the
  246-subject corpus **and 0 times in the entire repository log**. All 36
  `Maintainer Decision` subjects in the repo are the head-first form
  `dev/proposals: Maintainer Decision…`, which arm **1** matches.

So `dev/proposals: licensing -- Maintainer Decision -- ACCEPT` and
`dev/proposals: transition-lint -- Maintainer Decision -- ACCEPT (post Internal
review)` are **constructed probes**, not real forms. They do discriminate
(verified: `None` and `reviewed` respectively under the arm-2 ablation) — the
perturbation is sound. The word **"real"** is what is wrong, in the one document
whose stated discipline is not implying corpus evidence it does not have.

Nor is the guard alone. Per-literal ablation over all 246 subjects:

| literal | corpus flips |
|---|---|
| hyphen guards `(?<!-)` / `(?!-)` | **0** *(plan flags this)* |
| `decision` arm 2 | **0** |
| `(?:dev/)?` optional prefix segment | **0** |
| `(?:ing)?` in `^open(?:ing)?\b` | **0** |
| U+2013 / U+2014 separators (ASCII `--` only) | **0** |
| `revise` token | **0** |
| `respond\s+to` token | **0** |
| `responses` token | 2 |
| `revised` token | 3 |
| `response` token | 13 |

Brief-question 2 asks whether the hyphen guard earns its place with no corpus
evidence. **The honest answer is that it earns exactly as much as six siblings,
and the plan should say so** — one sentence in **(b)** listing them, so the
guard is not framed as uniquely unsupported when it is representative. Under the
security lens this also reframes the residual: each zero-effect literal is a
widening surface with no live constraint, and arm 2 is the widest of them
(`decision` matches the phrase *anywhere* in the body, not at its head) — which
is why two of **[I1]**'s worst probes are arm-2 hits.

Keep every literal — they are transcribed from a ratified design and removing one
is a Decision-level change. Just label them the way the guard is labelled.

---

**[I6] — T8's power against the shipped patterns is weaker than the invariant
ledger claims: the new scoped vocabulary *shadows* three of the four shipped
patterns, so a deletion of them is invisible to it.**

The Author-accounting states: *"`_STAGE_COMMIT_PATTERNS` is byte-unchanged…
pinned in one direction by T7b and T8. Not guarded by a test that fails when a
future author edits it — **T8 catches a *deletion***, not a widening."*

T8 catches *some* deletions. Because the new `_STAGE_SCOPE_PREFIX_RE` accepts
`proposals?` (singular), every shipped legacy form that begins `proposal:` is now
re-matched by the scoped vocabulary. Measured, by dropping each shipped pattern
and re-classifying:

| dropped shipped pattern | legacy form | detected by T8? |
|---|---|---|
| `open` | `Open proposal: README tagline` | yes (`open` → `None`) |
| `open` | `Open proposal alice thing` | yes |
| `open` | `opening proposal widget` | yes |
| `open` | `proposal: open widget` | **no — shadowed, stays `open`** |
| `revised` | `Revised proposal for widget` | yes |
| `revised` | `proposal: respond to review` | **no — shadowed, stays `revised`** |
| `revised` | `proposal: revise the thing` | **no — shadowed, stays `revised`** |
| `decision` | `Decision: accept widget` | yes |
| `decision` | `proposal: Decision accept widget` | **no — shadowed, stays `decision`** |
| `reviewed` | `Review of the widget proposal` | yes |

Deleting the **entire** shipped `revised` pattern is invisible to both of its
`proposal:`-prefixed vectors. This does not change behaviour today (the shipped
loop runs first, so shadowing is unobservable while both exist) and does not
weaken backward compatibility — which really is guaranteed by construction. It
weakens **T8 as evidence**, and the plan cites T8 as the deletion guard.

The plan already states honestly that T8 is green before *and* after this diff.
Add the second half: for the `proposal:`-prefixed forms it stays green even if the
shipped pattern is *removed*, so T8 pins the `^Open proposal` / `opening
proposal` / `^Decision[:–—-]` / `Revised proposal` / `^Review` arms and nothing
else. If a real guard is wanted it is one line — assert `_STAGE_COMMIT_PATTERNS`
against a hand-written literal tuple of the four pattern strings — but that is a
new oracle and I agree it sits outside this scope fence.

---

**[I7] — T3 carries a vector its own named perturbation cannot red, and unlike
T4b / T8 / T12 the plan does not label it.**

T3's assertion set includes `dev/plans: archive review-record-integrity (Chunk C
pointer + lifecycle close)` → `None`. Under T3's named perturbation (re-add
`plans?` to `_STAGE_SCOPE_PREFIX_RE`), measured:

```
baseline           -> None
plans? re-add      -> None      <-- inert under T3's own perturbation
noguard            -> None
plans? + noguard   -> reviewed
```

It falls only under the *conjunction*, which is structurally the same weakness
the plan labels for T4b and then labels again for T8 and T12. The rest of T3 is
strong (16 corpus flips `None → open`, reproduced exactly; the `Code review`
probe flips `None → reviewed`, reproduced). This is a one-clause docstring fix,
and it matters because the archive vector is the very subject the plan names at
**(b)** as the hyphen guard's sole historical justification — so its status
should not be left to a reader to infer.

*(Verified separately: the `dev/plans: <slug> -- Code review (fresh-context,
disclosed scribe)` probe is a real subject form — 9 occurrences in the repository
log — templated with a placeholder slug. The plan does not claim it is in the
proposal corpus, and it is not. That framing is correct.)*

---

**[I8] — Two test specifications will bite the implementer as written.**

*T10 must not assert truthiness.* The spec is *"all three `hours_*` non-empty and
`>= 0`."* I built the synthetic four-commit repo (`open` / review / response /
decision, scoped subjects) and ran the public path:

```
tier: Exact
hours_open_to_reviewed = 0.0
hours_reviewed_to_revised = 0.0
hours_revised_to_decision = 0.0
```

All three are `0.0` — non-empty and `>= 0`, so the spec is met, but
`assert row['hours_open_to_reviewed']` fails on a falsy float. The plan *already
knows this*: P3 correction 2 exists precisely because a batch-committed session
yields exactly `0.0` (re-verified: three real proposals do). Wire that knowledge
into T10's spec — `!= ''` / `isinstance(v, float)`, never truthiness — so the
implementer does not have to rediscover it.

*T11's perturbation is described too broadly.* The plan says an unconditional
`parts[1]` gives *"`IndexError` on every separator-less subject."* Measured, it
raises on 3 of T11's 6 listed vectors — the scope-prefixed ones (the prefix-only
subject, the non-ASCII subject, the 500-char subject). `''`, `'   '` and a separator-only
subject return `None` at `if match is None: return None`, before the split. The
test still reds, so the perturbation is valid; the sentence is not.

---

**[I9] — P3 corrects one of two falsely-exhaustive cause lists in this module,
and Chunk B's grep is scoped so it cannot see the other.**

Chunk B's premise is right: *"every clause of its cause list is false of the
failure actually observed."* The same defect sits one file away, in the function
whose behaviour R12c *is*. `templates/modules/default-on/_lifecycle_metrics/gitmeta.py:33-37`:

> Returns an empty list when git is not available, the repo is not a git
> checkout, or the path has no history

That list omits the transient-failure path at `gitmeta.py:50-51`
(`if result.returncode != 0: return []`) — which is exactly R12c, the hazard the
plan defers and the reason every corpus verification here runs on a quiet tree.
Chunk B's acceptance grep is `"the default branch is named"`, which matches only
`__init__.py:75` in both copies (verified — it does run correctly as a
single-line grep; the wrap in the plan text is cosmetic), so it structurally
cannot see the sibling.

**I am not asking to widen P3** — that would edit a file outside the ratified
change set. I am asking that the deferred-R12c bullet and the corresponding
`## Lasting-truth migration` row name the *docstring* alongside the behaviour, so
the `dev/PLANNING.md > Queued` entry that eventually homes R12c covers both and
the second false cause list is not orphaned by the archive.

---

**[I10] — Chunk A's "the install manifest does not move" criterion cannot fail
from a byte edit; it belongs on the plan's own non-falsifiable list.**

Criterion: *"`bootstrap/scaffold.py --manifest | grep gitmeta` → **unchanged**.
Capture before the edit, diff after."* Measured, the entire matching output is:

```
tools/_lifecycle_metrics/gitmeta.py	modules/default-on/_lifecycle_metrics/gitmeta.py	verbatim
```

`dst`, `src`, mode — no digest, no size. A content change to `gitmeta.py` cannot
move that row; only a mapping change could, and a mapping change is already
foreclosed by the scope fence. The check is correct to keep (it guards the
mapping), but it is structurally green, exactly like T8 and T12. The plan earns
credit for labelling those two; this one should join them rather than reading as
a third independent guard.

---

**[I11] — Chunk C will execute a finalize engine that is itself another
workflow's uncommitted work-in-progress, and the plan names the concurrency only
for the dirty-tree rationale.**

The plan correctly reasons that a *scoped* finalize is exempt from the #56
dirty-tree guard, and correctly notes that other workflows are editing
`bootstrap/_scaffold/` concurrently. What it does not name is that **the finalize
engine is among the modified files**: `bootstrap/_scaffold/upgrade.py` and
`bootstrap/_scaffold/lockfile.py` both carry uncommitted changes, and
`cmd_upgrade` reaches the new, unlanded `trusted_upstream(...)` /
`forked_facade_findings(..., upstream=...)` path *before* the `--finalize`
dispatch.

Verified in the plan's favour, so this is a sequencing note rather than a defect:

* `_cmd_finalize_lockfile` itself is byte-unchanged from `HEAD`; the scope filter
  matches on `dst`, which is exactly the two paths the plan names.
* `_emit_lock_yaml(read_lockfile(...))` round-trips the committed lockfile
  **byte-identically** today, so "exactly two lines" is achievable.
* The `base_hash` preserve branch is a genuine no-op — both records already
  carry `base_hash` (`:469`, `:497`).
* The `core/VENDOR.md` rename-resolution branch, which runs *before* the scope
  filter and could silently rewrite a third line, is inert here: that record's
  `dst` is already `CLAUDE.md` and the file exists.
* The expected message format is real: `upgrade.py` builds
  `f"Finalized {_LOCKFILE_REL}: advanced {changed} hash(es){scope} …"` with
  `scope = f" (scoped to {len(matched)} path(s))"`.

Add one line to Chunk C: **re-run the round-trip and no-op checks immediately
before finalizing**, because every one of the five bullets above was verified
against a tree state that is not committed and can change under the plan.

---

### Covered — what I ran, with output

All under `~/conda_envs/lhm/bin/python3.13` (Python 3.13.13), `HEAD` `eacb7dd`,
`as_of 2026-08-04`, no concurrent load during the git-dependent measurements.

**Required checkers — both clean.**

```
$ … scripts/claim_check.py dev/plans/stage-commit-patterns.md
claim_check: dev/plans/stage-commit-patterns.md -- 12 path(s) exempted by claim-check-allow
claim_check: dev/plans/stage-commit-patterns.md -- OK, no claim-check flags.   exit=0

$ … scripts/check_cairn.py dev/plans/stage-commit-patterns.md
check_cairn: OK -- 1 Markdown file(s) scanned; no issues.                       exit=0
```

**Reconstruction, and what it is.** `_stage_for_subject` does not exist yet, so I
extracted proposal lines `833-869` verbatim, spliced them into a **scratch copy**
of `tools/_lifecycle_metrics/` outside the repository, and applied P2's loop
replacement there. **This is a reconstruction from the plan's own cited source,
not the author's code**; a transcription drift in the real Chunk A would not
show up in it. Nothing in the repository was modified.

**Corpus and headline figures — every one reproduces exactly.**

| measure | plan | measured |
|---|---|---|
| proposal files | 35 | **35** |
| distinct `--follow` subjects | 246 | **246** |
| classified by the shipped patterns | 0 | **0** |
| classified by the revised design | 115 (33/12/34/36) | **115** — `open` 33, `reviewed` 12, `revised` 34, `decision` 36 |
| pipeline, shipped | 35/35 `Best-effort` | **`Best-effort` 35** |
| pipeline, revised | 12 `Exact` / 23 `Good` / 0 `Best-effort` | **`Exact` 12, `Good` 23** |
| pipeline, bare fallback | 29 / 6 / 0 | **`Exact` 29, `Good` 6** |
| negative `hours_*` deltas | 0 | **0** |
| `Exact`-with-empty-hours row | `…-r6-unused-def-blindspot` | **confirmed, that row only** |
| `plans?` ablation | 16 flips, all `None → open` | **16, `Counter({(None,'open'): 16})`** |
| hyphen-guard ablation | 0 flips / 246 | **0** |
| P2 fall-through | 0 of 35 file histories differ | **0 of 35** |

**P3's two live examples re-verified.** `hours_reviewed_to_revised == 0.0` for
`2026-07-22-claude-interpreter-trust-root-fallback`, `…-lockfile-provenance-fields`
and `…-transition-lint`. The four 2026-07-11 proposals carry
`hours_revised_to_decision` of `116.474 / 116.459 / 116.459 / 116.459` beside
`days_revised_to_decision = 11`.

**Perturbations — all twelve run against the reconstruction; all discriminate.**
T2 (8 of 9 `None` expectations flip, matching the plan exactly); T3 (16 + the
`Code review` probe — see **[I7]** for the inert vector); T4 (both probes
`None → reviewed`); T4b (`open` under baseline, noguard-only and reorder-only;
`reviewed` only under the conjunction — the plan's four-way claim is exact);
T4c (`open → revised`); T5 (both `revised → reviewed`); T6 (`None` and
`reviewed` respectively — see **[I5]** on "real"); T7a (`reviewed → None`);
T7b (`None → reviewed`); T8 (see **[I6]**); T11 (see **[I8]**).

**Synthetic-repo tests built and run.** T9: two commits, `open` = commit 1,
`revised` is `None`; under a restored fall-through loop `revised` takes commit 2
— the perturbation reds it. T10: four commits, `Exact` and three populated
`hours_*` (see **[I8]**). T12: no `.git` → `Best-effort`, all three empty.

**Environment and gate posture.** `verify_integrity.py --target .` → exit 1,
**exactly 2** violations (`AGENTS.md`, `dev/modules/security-review.md`) — as
stated. `security_check.py`'s `scan_targets()` → **74** targets, both
`templates/modules/default-on/_lifecycle_metrics/gitmeta.py` and `…/__init__.py`
present. **18** shipped template `.py` files carry non-ASCII. Both twin pairs
byte-identical (`5a47849b…`, `c0e169e7…`). The template launcher
`templates/modules/default-on/lifecycle_metrics.py` re-exports
`_resolve_stage_commits` / `proposal_rows` / `_STAGE_COMMIT_PATTERNS` and
resolves to the **template** engine copy — so A4's load idiom reaches the edited
file, as claimed.

**Line citations.** Every `proposal :<n>` in the 30-row transcription table
resolves correctly (`:833` prefix, `:835` separator, `:837-838` comment, `:839`
list, `:840` open, `:842-843` decision arms, `:844-846` revised, `:847`
reviewed, `:850` head-anchored, `:853-854` signature, `:856-858` shipped-first,
`:859-861` the `return None`, `:863-864` split, `:865-868` per-stage target).
`gitmeta.py:9 / 17-25 / 18-19 / 21 / 24 / 50-51 / 81-85 / 108-121`,
`__init__.py:74-78`, `extract.py:41-83`, `test_ast_attest.py:20`,
`test_notice_install.py:98`, `test_lifecycle_metrics_config.py:13-16` and
`:27-36`, `test_reference_scripts.py:443-457` and `:476`, `docs/quickstart.md:240`
(correctly updated from the proposal's stale `:231`), and
`gate_manifest.json:2766` / `:2770` all resolve. The two lockfile citations do
not — **[I2]**.

**Decision quotations.** All five checked verbatim against
`dev/proposals/2026-07-22-claude-stage-commit-patterns.md` `:1219-1281`: *"as
revised"*, the bare-fallback sentence, *"One reliability tier was surrendered"*,
*"OQ3 — the plan-review tier stays `required(Internal)`"*, and the scoped-finalize
condition. The four ratified plan conditions the `## Lasting-truth migration`
sign-off enumerates match the Decision's four exactly. No quotation is a
paraphrase.

**Scope boundaries hold.** No sibling surface is absorbed:
`scripts/transition_lint.py` is named once, inside the fence, only to record that
it is not built. Nothing new appears against the Decision's stopping rule — no
CLI, config key, output column, exported helper, or mandated commit convention.
`PROPOSAL_COLUMNS` is untouched. The one mild widening is editorial: the Chunk D
`dev/PLANNING.md` row carries the contested ~17-tier observation onto a
serialized board, which is stylistically consistent with that board's existing
discursive rows but does put a review-open question into shared state. The
Maintainer may prefer it stay in the plan.

**Brief-question 1 — my answer.** Confirmed both ways to the digit (12/23/0 vs
29/6/0). **The plan's position is right and I concur: the design is not
reopened.** Two reasons the re-pricing is less alarming than the raw number.
First, it is not a *regression* — the bare-fallback arm buys its 17 tiers by
classifying subjects it cannot read, which is the wrong-stage-at-`Exact` hazard
R1 blocked, and **[I1]** shows that hazard is *larger* today than at Decision
time, not smaller, because the 2026-08-03 wave writes looser subjects. Second,
`Good` is the honest tier for a row the vocabulary cannot read; trading 17 honest
`Good`s for 17 possibly-wrong `Exact`s is the trade the Decision already rejected
at n=1, and n=17 strengthens it. The number should still reach the Maintainer —
the fence item is correct — but as *evidence the narrowing is working*, not as
grounds to revisit. I would say that in the fence item rather than leaving it
neutral.

### Not covered / low confidence

* **The transcription itself.** I verified the plan's 30-row table against the
  proposal, and I ran a reconstruction — but the reconstruction is *my* splice of
  the cited block, not the implementer's. A one-character drift in the landed code
  is invisible to everything I did, and to every test that ships with it. The
  Code-review obligation to read the landed block character-by-character against
  `:833-869` is the only control, and it remains load-bearing.
* **Adopter corpora.** I extended the probe set (**[I1]**) but constructed it
  myself, from the same hydrogeology frame the panel used. Known omission (b)
  stands and my probes do not retire it.
* **`bootstrap/security_check.py` (Bandit) was not run.** I confirmed both files
  are in `scan_targets()` but did not execute the gate; the change adds compiled
  regexes and a pure string function, so I have no reason to expect a finding, but
  I did not verify that.
* **`scripts/quality_gate.py`** was not run over the plan.
* **Chunk C was not executed**, by design — it writes the lockfile. My round-trip,
  scope-matching, `base_hash` and VENDOR-branch checks are static reads of the
  engine, not a dry run, and per **[I11]** they were taken against uncommitted
  engine bytes.
* **The four pre-existing suite failures** were diagnosed to other workflows'
  `_scaffold` edits from the failure text; I did not confirm by reverting, since
  the tree is not mine to mutate.
* **Same-agent-type blind spot.** Per the standing paragraph — nothing here
  substitutes for a cross-type read, and the plan's own tier does not call for
  one. If the Maintainer wants an independent read of **[I1]**'s framing
  specifically (whether an adopter-facing safety claim can rest on an
  undocumented subject convention), that is the question a different agent type
  would be worth spending on.

### Recommendation

**Revise and proceed — no second review round.** Eleven findings, none of which
reopens the Decision, and none of which asks for a regex change. Ten are plan-text
and test-specification corrections the author can land in a `### Sharpening`
revision; one (**[I1]**) adds a vector class to Chunk A under the existing oracle
rule and mechanism, which is inside the scope fence.

Ordered by what should block an implementing commit:

* **Blocking on implementation**: **[I2]** (wrong line for a Decision-mandated
  write), **[I4]** (the suite gate and the AST instrument are unachievable as
  written on today's tree — this needs a Maintainer sequencing call, not an
  implementer's judgement), **[I3]** (a fence check that cannot be performed).
* **Blocking on the plan's own honesty standard**: **[I1]** (the guarantee
  overstates its evidence; add T2b), **[I5]** (drop "real", list the six
  zero-evidence literals), **[I6]** and **[I7]** (label two more weak vectors the
  way T4b/T8/T12 are labelled).
* **Land with the revision**: **[I8]**, **[I9]**, **[I10]**, **[I11]**.

If the author's Response instead concludes that **[I1]** warrants changing the
scoped vocabulary — it does not, in my reading — that is a new proposal, not an
amendment inside this plan, exactly as Maintainer fence item 3 says of the
re-priced trade.

## Revision after Internal plan review -- Claude (author) -- 2026-08-04

**Model**: Claude Opus 5 (`claude-opus-5`).

The review's recommendation was **REVISE and proceed, no second round**. Eleven
findings, all dispositioned below. **Ten folded in; one folded in with its
proposed remedy declined and replaced.** No regex changed, no scope-fence line
moved, the Decision is not reopened, and no source file was touched by this
revision — the whole diff is this plan file.

**Method — every finding was re-derived from primary source before disposition,
not taken from the review's wording.** The review is a report, and reports are
what produced the defects it found. Re-derivation used a scratch reconstruction
of proposal `:833-869` spliced onto the shipped `_STAGE_COMMIT_PATTERNS`,
outside the repository; the live corpus rebuilt from `git log --follow`; the
real `tools/_lifecycle_metrics` engine with `_resolve_stage_commits`
monkeypatched for the pipeline runs; and direct reads of
`bootstrap/tests/fixtures/gate_manifest.json`, `dev/.cairn/cairn-lock.yml` and
`bootstrap/_scaffold/upgrade.py`. All under
`~/conda_envs/lhm/bin/python3.13` (Python 3.13.13), **`HEAD` `da2d00e`**
(the review measured at `eacb7dd`), `as_of 2026-08-04`, quiet tree.

**Re-measured, and unchanged from the plan's table**: 35 proposal files, 246
distinct `--follow` subjects, **0** classified by the shipped patterns, **115**
by the accepted revised design (`open` 33, `reviewed` 12, `revised` 34,
`decision` 36), pipeline **35/35 `Best-effort`** shipped → **12 `Exact` / 23
`Good` / 0 `Best-effort`** revised → **29 / 6 / 0** under the bare fallback, **0**
negative `hours_*`, `plans?` ablation **16** flips all `None → open`,
hyphen-guard ablation **0** flips, P2 fall-through **0 of 35**. Every one of the
twelve named perturbations was re-run and discriminates as the table states.
Twin pairs still byte-identical (`5a47849b…`, `c0e169e7…`); `verify_integrity`
still exactly 2 violations; `security_check.scan_targets()` still 74 with both
files in it.

### Disposition, finding by finding

**[I1] — the scope gate disposes of its own safety argument. ACCEPTED, folded
in.** Re-derived: the 14 scoped-but-not-a-transition probes give **10 of 14
classified** — identical to the review. Independently confirmed the two supports
the review said do not reach the residual: the panel's 10 adopter probes are all
un-scoped (9 → `None`, the tenth a pre-existing shipped-pattern hit), and all
115 classified corpus subjects are genuine transitions, with
`proposals: repair four check_cairn issues introduced by the landed reviews`
escaping only on the plural `reviews`. Changed: new subsection **(e)** carrying
the probe table and the "proxy for *touched a proposal file*" framing; the
"zero wrong-stage assignments" claim in **(a)** qualified to Cairn's own corpus;
a new **T2b** row in the test table with hand-written literals and **two**
perturbations (widen the scoped `reviewed` to `reviews?`, which drops the `None`
expectations from 4 to 3; and delete `decision` arm 2, which drops both
`decision` probes) — the second measured for this revision; a new
invariant-ledger entry naming the residual as *priced, not invariant*; the
wrong-stage failure-mode bullet amended to say what T2/T4/T5/T6 do **not** pin;
known omission **(g)**; a `## Lasting-truth migration` row; and a second bullet
under Maintainer fence item 3. **Declined:** any change to the scoped
vocabulary. The 10 are a strict subset of what the bare fallback misclassifies,
so the ratified narrowing still dominates; what was wrong was the size of the
claim, not the design.

**[I2] — the lockfile citations point at `dst`, not `hash`. ACCEPTED, folded
in.** Re-derived at `da2d00e`: the `tools/_lifecycle_metrics/__init__.py` record
runs `:468-473` with `base_hash` `:469`, `dst` `:470`, **`hash` `:471`**; the
`gitmeta.py` record runs `:496-501` with `base_hash` `:497`, `dst` `:498`,
**`hash` `:499`**. Changed: the re-measurement bullet now names `:499` / `:471`
as the hash lines and `:498` / `:470` as `dst`, and Chunk C's acceptance
criterion is corrected to `:471` and `:499` — with an added instruction to
re-derive the numbers by `grep -n` on the `dst` values and anchor the check on
the two **records**, since a lockfile line number is not stable across the
plan's life.

**[I3] — the fence names a field that does not exist. ACCEPTED, folded in with
a corrected instrument.** Re-derived: `bootstrap/tests/fixtures/gate_manifest.json`
has top-level keys `cascade_mutable`, `collection`, `frozen_files`,
`gate_commands`, `interpreter`, `mapping_symbols`, `phase_mutable`, `schema` —
**no `anchor_ref`**. `anchor_ref` is a parameter of `_gate_manifest.verify()`;
`refs/cairn/gate-anchor` exists at **`e45e1fcc84ded159…`**. Independently
confirmed the plan's conclusion is nonetheless right: `test_gate_manifest.py`
uses `G.produce(_REPO)` (`:33`) and calls `verify()` only on `tmp_path`
manifests, and no other file under `bootstrap/tests/` reads the committed
fixture against the live tree. Changed: the gate-posture bullet and Maintainer
fence item 1 rewritten around three performable checks. **One addition beyond
the review's remedy:** the fence now states explicitly that **a populated
`refs/cairn/gate-anchor` is the normal standing trust root and is not a stop
signal** — the ref is always populated, so "check the ref" phrased without that
clause would have replaced an unperformable check with a permanently-tripping
one.

**[I4] — the suite is red and `test_ast_attest.py` is the plan's own instrument.
ACCEPTED; remedy (a) DECLINED and replaced.** Re-measured today: **2 failed,
1788 passed, 0 skipped** — *not* the review's `4 failed, 1777 passed`. The two
`bootstrap/tests/test_profile_grammar.py` failures it named are green again
hours later; only the two `test_ast_attest.py` nodes remain. **That measurement
is why the review's fix (a) — pin these four node IDs at this HEAD as a named
baseline — is declined: a frozen node-ID list decays within a day on this tree,
and a stale baseline is the same disarmed-check failure in a new dress.** Folded
in instead: **all three** suite criteria the review named — Chunk A's, **Chunk
B's**, and the plan-level one — restated as "no *new*
failure against a baseline **measured at the commit**, 0 skipped", explicitly
not carried forward from the proposal's `1437`, from the review's four nodes, or
from this plan's own `2 / 1788`; and the review's fix (b) adopted in full — the
AST invariant is now checked **structurally** (`git diff HEAD --stat --
bootstrap/_scaffold/` shows nothing attributable to this plan, and the
attestation's symbol list contains no `_lifecycle_metrics` symbol), with today's
six reported symbols recorded as evidence that check works: `_minimal_yaml_parse`,
`load_config` (`config.py`), `cmd_upgrade` (`upgrade.py`),
`forked_facade_findings`, `format_forked_facade_warning` (`lockfile.py`), and one
`MISSING Try`. Maintainer fence item 2 now names the sequencing call as the
Maintainer's.

**[I5] — "real" Decision forms, and the guard is not uniquely unsupported.
ACCEPTED, folded in, and extended by two measurements.** Re-derived: arm 2 flips
**0 of 246**; `-- Maintainer Decision` occurs **0 times in the entire repository
log**; all **36** `Maintainer Decision` subjects are the head-first form arm 1
matches. Changed: the word "real" struck from transcription row 16 and from T6's
description, with both now stating which vector is observed and which two are
constructed; and **(b)** rewritten to carry a per-literal ablation table.
**Two corrections to the review's own table**, both measured: (i) it lists
**six** zero-flip siblings; there are **seven** — the *singular* branch of
`proposals?` also flips 0, and is the direct cause of [I6]'s shadowing, making
**eight** zero-live-evidence literals in total; (ii) its `(?:dev/)?` row is
direction-ambiguous — removing the **optionality** (requiring `^dev/proposals?:`)
flips **0**, but deleting the segment (forbidding `dev/`) flips **115**. The
plan now states which ablation the row claims. Known omission **(h)** added; no
literal removed, since each is transcribed from a ratified design.

**[I6] — the scoped vocabulary shadows the shipped patterns. ACCEPTED, folded
in.** Re-derived by dropping each shipped pattern and re-classifying the ten
legacy vectors: **4 of 10 shadowed** — `proposal: open widget`,
`proposal: respond to review`, `proposal: revise the thing`,
`proposal: Decision accept widget`. Per pattern: `open` 3 of 4 detected,
`revised` **1 of 3**, `decision` 1 of 2, `reviewed` 1 of 1. So deleting the
whole shipped `revised` pattern is invisible to both of its `proposal:`-prefixed
vectors. Changed: T8's row now records the shadowing limit and enumerates the
five arms it actually pins; the invariant-ledger entry for
`_STAGE_COMMIT_PATTERNS` amended from "T8 catches a *deletion*" to "not even
every deletion", with the one-line real guard named and explicitly left outside
the scope fence.

**[I7] — T3 carries an unlabelled inert vector. ACCEPTED, folded in.**
Re-derived all four ways for
`dev/plans: archive review-record-integrity (Chunk C pointer + lifecycle close)`:
baseline `None`, `plans?` re-add `None`, hyphen-guard strip `None`, conjunction
`reviewed`. Changed: T3's row now states that the archive vector is inert under
T3's own perturbation and falls only under the conjunction — the same label
T4b/T8/T12 already carry — and says why it matters, since that subject is the
one **(b)** names as the hyphen guard's sole historical justification. The rest
of T3 reproduced exactly (16 flips, all `None → open`; the Code-review probe
`None → reviewed`).

**[I8] — two test specifications bite the implementer. ACCEPTED, folded in, and
one further condition found.** Re-derived: a synthetic four-commit repo yields
`hours_open_to_reviewed` / `hours_reviewed_to_revised` /
`hours_revised_to_decision` all exactly **`0.0`** (all four commits share one
committer timestamp), so a truthiness assertion fails on a passing spec; and the
unconditional-`parts[1]` perturbation raises on **3 of T11's 6** vectors, not
"every separator-less subject" — `''`, `'   '` and the separator-only subject
return at `if match is None: return None` before the split. **Found in
re-derivation, beyond the review:** T10's `== 'Exact'` is *also* unachievable as
specified. `stage_present` is derived from the **document's** dated stage
sections, so a synthetic proposal file without them reports **`Good`** even with
four resolving commits — measured both ways. Changed: T10's row now specifies
`!= ''` / `isinstance(v, float)` / `>= 0` and never truthiness, and requires the
synthetic file to carry dated `## Review` / `## Response` / `## Decision`
sections; T11's row now states the perturbation's true reach and notes the test
still reds.

**[I9] — the second falsely-exhaustive cause list. ACCEPTED, folded in; P3 not
widened.** Re-derived: `_git_log_for_path`'s docstring at
`templates/modules/default-on/_lifecycle_metrics/gitmeta.py:33-37` lists "git is
not available, the repo is not a git checkout, or the path has no history" and
omits `if result.returncode != 0: return []` at `:50-51` — which *is* R12c. And
Chunk B's grep string matches exactly `__init__.py:75` in both copies, so it
structurally cannot see it. Changed: the deferred R12c bullet now names the
docstring alongside the behaviour; Chunk B's acceptance states the grep's scope
limit and why P3 is not widened; the `## Lasting-truth migration` row now homes
both halves in one `dev/PLANNING.md > Queued` entry. **Declined:** editing
`gitmeta.py`'s docstring, which is outside the ratified change set.

**[I10] — the `--manifest` criterion is structurally non-falsifiable. ACCEPTED,
folded in.** Re-derived: the entire matching output is one row —
`tools/_lifecycle_metrics/gitmeta.py`, `modules/default-on/_lifecycle_metrics/gitmeta.py`,
`verbatim` — with no digest and no size, so no content edit can move it. Changed:
the criterion is kept (it guards the *mapping*) but now carries the same
explicit non-falsifiable label as T8 and T12, and says it must not be counted as
a third independent guard.

**[I11] — Chunk C runs another workflow's uncommitted engine. ACCEPTED, folded
in.** Re-derived at `da2d00e`: `bootstrap/_scaffold/upgrade.py` and
`bootstrap/_scaffold/lockfile.py` both carry uncommitted changes;
`cmd_upgrade` reaches `trusted_upstream(...)` / `forked_facade_findings(...)` at
`upgrade.py:2225-2226`, **before** the `--finalize` dispatch at `:2230-2232`;
`_cmd_finalize_lockfile` (`:1612`) is **AST-identical to `HEAD`** while
`cmd_upgrade` is **not** (compared via `ast.dump` against
`git show HEAD:bootstrap/_scaffold/upgrade.py`); and
`_emit_lock_yaml(read_lockfile(Path('.')))` round-trips the committed lockfile
**byte-identically** (24925 bytes in, 24925 out). Changed: a new Chunk C
acceptance criterion requiring all four preconditions to be **re-run
immediately before finalizing**, with "stop and re-sequence" as the failure
disposition, plus the sequencing note in Maintainer fence item 2.

### Two things the review raised that this revision did not change

* **T4b, which the reviewer invited striking.** Kept. It is already labelled as
  falling only under a two-part perturbation, and this revision *adds* two more
  labelled-weak vectors (T3's archive probe, the `--manifest` criterion) on the
  principle that a labelled weak vector is worth more than a deleted one. If the
  Maintainer prefers it struck, that is a one-row deletion at implementation
  time and costs nothing.
* **The `dev/PLANNING.md` row carrying a review-open question onto a serialized
  board.** Kept, and now carries a second such observation ([I1]'s residual),
  because both are things the Maintainer should see before implementation and
  the board is where they will see them. Flagged here so the choice is visible;
  the serialization owner may drop either clause when landing the row.

### Bookkeeping

The landed review is a `## Plan review -- …` section at the end of the file
rather than a `### Plan review -- …` sub-heading under `## Plan review — the
brief`, as the review's own placement note records. **Not moved here** — a
relocation is the Maintainer's or a serialization-point call, not something to
bundle into an author revision, and the section is untouched by this revision in
any case.

### Verification of this revision

* `~/conda_envs/lhm/bin/python3.13 scripts/claim_check.py dev/plans/stage-commit-patterns.md`
* `~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py dev/plans/stage-commit-patterns.md`

Both run after the edits; results recorded with the revision commit. No source
file, fixture, `CHANGELOG.md`, `dev/PLANNING.md`, or `AGENTS.md` was touched.

## Implementation record -- Claude -- 2026-08-04

Chunks A, B and C landed at `2177d5f`, `321ed1a`, `543f785`; verified by an
agent that did not write them (CONFIRMED, 18 perturbations re-run
independently, every one reddening its own node). **Chunk D is held** — see
both notes below.

**Disclosure: the Maintainer fence was not satisfied as written.** Fence item 2
requires *"explicit maintainer approval before `git commit`"* for each of A, B
and C, none of which fall under the deliberation carve-in. The Maintainer
authorized the *implementation* of this plan; they did not approve the three
commits individually. They landed on an orchestrating agent's instruction,
which is not the Maintainer's approval. Recorded here rather than left to the
commit log: nothing is pushed, so this is ratifiable, and the Maintainer should
ratify or object rather than discover it. The fence's other half — whether A–C
should wait on the sibling `bootstrap/_scaffold/` work — resolved on its own;
that work is committed and the engine tree is clean.

**Chunk D is held because its own text went stale during implementation.** D1
says the shipped vocabulary *"matched **zero** of Cairn's real commit
subjects"* and read `Best-effort` *"on every row"*. Re-measured at
implementation: it now matches **exactly one of 251** subjects, and assigns it
the **wrong stage**. The subject is
`review-gate-enforcement: Response to the External review (status: revised)` —
a **`revised`** transition claimed by the shipped `^Review\b`, because the word
boundary sits between `w` and the hyphen in `review-gate`. It reads
`Best-effort` on 36 of 37 rows, not all 37.

That is a genuine wrong-stage assignment on Cairn's own corpus, and it is worth
recording *why* it appeared today: the subject was written this session, by the
same agent implementing this plan. The shipped vocabulary did not change; the
corpus did. A claim of the form "matches zero of our commits" is only ever true
`as_of` a corpus, and this plan's D1 asserted it without one.

The corrected D1 text is in the implementing agent's return and is the version
to land. It is **not** landed here because `CHANGELOG.md` and `dev/PLANNING.md`
are serialized shared files outside the carve-in, and because the correction is
substantive rather than mechanical.

### Maintainer ratification -- Anthony Kendall -- 2026-08-04

**Maintainer's authorization (verbatim):**

> #2: Ratify A/B/C and accept D, totally fine about that changelog variance.

Chunks A, B and C (`2177d5f`, `321ed1a`, `543f785`) are **ratified**, resolving
the Maintainer-fence item 2 disclosure above: they landed without the
per-commit approval the fence requires, and that is accepted after the fact.

**Chunk D is accepted in its corrected form** — the release note states that the
shipped vocabulary matched **one** of 251 subjects and assigned it the *wrong*
stage, not the plan's original "zero". The Maintainer accepted the variance
explicitly. D lands as this plan's fourth chunk.

Scribed by Claude (Implementation).

## Code review -- Antigravity (External) -- 2026-08-10

**Tier**: required(**External**)

**Findings**: SHIP

### Judgments & Verification Ledger

* **Boundary B/C Verification**:
  - Interpreter: `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13), `PYTHONDONTWRITEBYTECODE=1`.
  - SHA / Range: `43e0116` (`as_of 2026-08-10`).
  - Command: `PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_lifecycle_stage_patterns.py -v`
  - Outcome: **126 passed in 0.30s** (0 failed, 0 skipped, 0 xfailed).

* **Judgment (a) Reliability Tier Cost of Narrowing**:
  - **Judged sound**: The ratified scope-gate narrowing (`if match is None: return None`, requiring `dev/proposals:`) surrenders `Exact` reliability for 17 unscoped proposal subjects on Cairn's live corpus (reporting `Good` instead of `Exact`), but achieves **0 false-positive stage assignments** on Cairn's corpus and avoids misclassifying ordinary commits as lifecycle transitions. `Good` is the honest tier when subjects cannot be read unambiguously.

* **Judgment (b) Scope Gate Safety & Commit-Subject Convention**:
  - **Judged sound**: The scope gate `^(?:dev/)?proposals?\s*:\s*` relies on authors writing `dev/proposals:` prefixes for proposal commits. While this convention is established by habit in Cairn, the plan explicitly fences creating a mandatory commit-message convention. For adopters, the scope prefix acts as a proxy for "touched a proposal file" rather than "is a lifecycle transition." This residual is documented in the plan's known omissions (g) and residual set, and `Good` is the honest tier when subjects cannot be read unambiguously.

* **Judgment (c) SHIPPED Vocabulary Single Wrong-Stage Assignment**:
  - **Judged sound**: The shipped pattern `^Review\b` matches across a hyphen word boundary in `review-gate-enforcement: Response to the External review...`, misclassifying a `revised` transition commit as `reviewed`. This occurred because `^Review\b` matches `review` at the start of the subject before `-gate`. Fixing `_STAGE_COMMIT_PATTERNS` directly was rejected by Revision P1 (to keep P1 additive and avoid changing shipped defaults). The plan transparently documented this single corpus misclassification in the Implementation Record (`2107-2110`) and Changelog entry, and the Maintainer explicitly accepted this variance in their 2026-08-04 ratification (`2111-2126`).

* **Judged After-the-Fact Ratification Record**:
  - **Judged adequate and compliant**: The Maintainer fence required per-commit approval for Chunks A, B, and C. An orchestrating agent committed A, B, and C without per-commit approval. The implementation record explicitly disclosed this non-compliance at lines 2079-2089. The Maintainer Anthony Kendall reviewed the disclosure and explicitly ratified commits `2177d5f`, `321ed1a`, and `543f785` in writing under `## Maintainer ratification -- Anthony Kendall -- 2026-08-04` quoting their verbatim instruction: `"#2: Ratify A/B/C and accept D, totally fine about that changelog variance."` This disclosure and verbatim ratification strictly adhere to Cairn's scribing and audit rules.


## Implementation verification -- Claude -- 2026-08-10

**Why this record exists, and what it does NOT do.** This plan had **no
`## Implementation verification` record of any kind** when its
`## Code review -- Antigravity (External) -- 2026-08-10` was performed -- its
2026-08-04 `## Implementation record` is a chunk-landing narrative, not a
Boundary B integration record, and carries none of the record schema's fields.
Per `doctrine/dual-review.md` trigger 1 -- *"no valid Boundary B record
exists"* -- that obliged the reviewer to run a **fresh full suite** in place of
the absent record. The review ran one file
(`pytest bootstrap/tests/test_lifecycle_stage_patterns.py -v`, 126 passed in
0.30s). It did not run the full suite, `scripts/check_cairn.py`, or
`scripts/quality_gate.py` -- all three of which this plan's own
`## Verification` section mandates ("the full suite gates the cut").

**This record supplies the missing broad evidence AFTER the review, so the
review neither validated it nor could have.** That matters more here than for a
prose-only change: this plan altered `tools/lifecycle_planner.py` and its
shipped twin `templates/skills/_lib/lifecycle_planner.py`, so the reviewed
bytes reach adopters. The Maintainer was shown this gap explicitly, in a choice
that included sending the review back for a confirmation pass on exactly that
ground, and selected **"Append record, note the gap, archive"** -- append the
Boundary B record, state plainly that the code review predates it, and archive
on that basis. The disposition is theirs; this record's job is to make the
shortfall legible to anyone reading the archived plan later.

| field | value |
|---|---|
| Tested commit | `36a3388` |
| Reviewed range | `2177d5f` (Chunk A), `321ed1a` (Chunk B), `543f785` (Chunk C), `18ea25d` (Chunk D1); Chunk D2 is the `dev/PLANNING.md` row at `b486b40`. All five confirmed ancestors of the tested commit via `git merge-base --is-ancestor`. Listed as commits rather than a `first..last` range because this tree is shared by several concurrent sessions and a `..` span would misrepresent unrelated plans' commits as part of what this record verifies. |
| Interpreter/runtime | `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python **3.13.13**, `PYTHONDONTWRITEBYTECODE=1` |
| Pre-run state | HEAD `36a3388`. Tracked files clean **except** `dev/proposals/2026-08-10-codex-lifecycle-status-vocabulary.md`, another session's live in-progress proposal. Untracked throughout: `.claude/`, `dev/measurement/collision_log.md`, `dev/measurement/snapshots/`. Stated exactly rather than asserted as "clean". |
| Post-run state | HEAD advanced to `5eec62e` during the run, via `6afa131`, `6fabc3f`, `5eec62e`. `git diff --name-only 36a3388..HEAD` returns files under `dev/` **only** -- all three are proposal appends, no code, so the figures below are unaffected by the advance. |
| Command | `python -m pytest bootstrap/tests -q` |
| Exit | 1 |
| Outcomes | **2 failed, 2591 passed**, 3 warnings |
| Elapsed | 362.93s (0:06:02) |
| Non-pass disposition | Both failures are `test_ast_attest.py` (`::test_committed_baseline_accounted_for_across_the_engine_package`, `::test_ast_gate_passes_over_the_full_scaffold_module_set`) and neither is attributable to this plan, which touches no file under `bootstrap/_scaffold/`. `_classify` reports **CHANGED 2, MISSING 0, DUPLICATE 0**: `Assign:_MODULE_MAPPINGS` (`config.py`, `security-verification-activation` Chunk A) and `FunctionDef:format_forked_facade_warning` (`lockfile.py`, `fork-advisory-semantics` Chunk B at `aba0242`). This is the **declared** red window `fork-advisory-semantics` opens at its Chunk B and closes at its Maintainer-only Chunk R re-anchor ceremony; neither symbol is in `_ast_attest._UPDATE_ALLOWLIST`, so neither is self-service repairable. |
| Plan-specific acceptance commands | `python scripts/check_cairn.py` -> **OK**, 176 Markdown files scanned, no issues, 48 external links not probed, rc **0**. `python scripts/quality_gate.py --sub neutrality --sub redundancy` -> rc **1**; neutrality `fail=96 info=21`, redundancy `fail=0 info=2`. The rc-1 is the **known pre-existing neutrality baseline**, not a regression: `fail=96 info=21` reproduces the independent re-measurement recorded at `dev/plans/security-verification-activation.md:2681` (taken at `6b488a2`), which also notes that the `fail=95` figure quoted across several plans is stale. Three neutrality fail lines do fall in `templates/skills/_lib/lifecycle_planner.py`, a file this plan touched, and each was checked individually against the pre-plan tree (`2177d5f^`) rather than assumed: `Codex` (line 187) and `Antigravity` (line 521) are unchanged at count 1 -> 1, so both predate this plan. **`Gemini` (line 936) does not** -- it goes 0 -> 1, and `git log -S` attributes it to `ab70660`, a commit of the **`review-gate-enforcement`** plan (archived 2026-08-10 at `be42ba6`), where it appears inside a docstring quoting a real review heading as an example. So no line is attributable to this plan -- but the third is a live defect belonging to an already-archived plan, recorded in the note below rather than left inside a disposition cell. |
| Known omissions | No independent falsification of this plan's own implementation was performed by this record -- that is the code review's job, and the point of this record is that the review's broad-run portion was never performed by anyone. The three judgment calls the review dispositioned (the reliability-tier cost of the narrowing, the undocumented commit-subject convention the scope gate relies on, and the single wrong-stage assignment from `^Review\b` matching across a hyphen) are **judgments, not measurements**, and this record re-derives none of them; they are under independent check. R12c remains deferred. The `CHANGELOG.md` variance the Maintainer accepted on 2026-08-04 is unchanged. |

**A live defect surfaced by this record, belonging to another plan.**
`templates/skills/_lib/lifecycle_planner.py:936` carries the vendor token
`Gemini`, inside a docstring that quotes a real review heading
(`## Plan review -- Gemini Flash (External, security lens) -- 2026-08-03`) as a
worked example. It was introduced by `ab70660` under **`review-gate-enforcement`**,
which archived on 2026-08-10 at `be42ba6` -- so it landed, passed through that
plan's review, and archived without the neutrality gate ever being run against
it.

This is not cosmetic. `AGENTS.md` lists vendor-neutrality as a **high-risk
surface** and the gate's own message for this path is explicit: *"no exemption
path; templates must stay clean by construction"* -- unlike `docs/` or
`doctrine/`, a file under `templates/` cannot be exempted with a `vendor-ok`
marker, because it ships to adopters. The remedy is to rewrite the docstring
example with a neutral reviewer name, which changes no behaviour; the token is
illustrative, not load-bearing.

Recorded here because this record's broad run is what surfaced it, and because
the owning plan is already archived and cannot carry it. It is **not** this
plan's to fix and does not gate this plan's archive; it is referred to the
Maintainer for placement.

This section is append-only once written.

## Archive record -- Claude -- 2026-08-10

**Status: archived.** Maintainer-directed: after selecting **"Append record, note
the gap, archive"** for this plan's missing Boundary B evidence, the Maintainer
confirmed **"I'm okay with you proceeding on the archive of both plans."**

**Correction to the Boundary B record above (`ad9f30c`), found while verifying
this archive's loop-fidelity conditions rather than asserting them.** That record
twice names the wrong module. It says this plan "altered
`tools/lifecycle_planner.py` and its shipped twin
`templates/skills/_lib/lifecycle_planner.py`", and its neutrality cell calls
`templates/skills/_lib/lifecycle_planner.py` "a file this plan touched". **This
plan never touched `lifecycle_planner.py`.** Its four commits touch exactly:

| commit | files |
|---|---|
| `2177d5f` (Chunk A) | `bootstrap/tests/test_lifecycle_stage_patterns.py`, `tools/_lifecycle_metrics/gitmeta.py`, `templates/modules/default-on/_lifecycle_metrics/gitmeta.py` |
| `321ed1a` (Chunk B) | `tools/_lifecycle_metrics/__init__.py`, `templates/modules/default-on/_lifecycle_metrics/__init__.py` |
| `543f785` (Chunk C) | `dev/.cairn/cairn-lock.yml` |
| `18ea25d` (Chunk D1) | `CHANGELOG.md` |

Two consequences, in opposite directions. The record's **conclusion** survives --
`templates/modules/default-on/_lifecycle_metrics/` ships, so the reviewed bytes
do reach adopters, which was the point being made. But its **neutrality
disposition was reasoning about the wrong file**: the three
`lifecycle_planner.py` vendor-token findings have nothing to do with this plan,
and the `Gemini` token at `:936` is neither this plan's nor in a file it touched.
That finding stands on its own -- it belongs to `review-gate-enforcement`
(`ab70660`, archived `be42ba6`) and is still a live shipped-template neutrality
defect -- but it is not this plan's residual and never was. Zero neutrality fail
lines fall in any of the six files above.

**Loop-fidelity sign-off** (`doctrine/lifecycle.md` > "Loop-fidelity
verification"). All four ratified plan conditions verified at archive, each
re-derived rather than carried forward:

| condition | verification |
|---|---|
| The **scoped** `upgrade --finalize` | `543f785` changes `dev/.cairn/cairn-lock.yml` by exactly **2 insertions / 2 deletions** -- two `hash:` values, one per twinned file. Scoped, not a blanket re-finalize. |
| **Twin byte-parity on both pairs** | `cmp tools/_lifecycle_metrics/gitmeta.py templates/modules/default-on/_lifecycle_metrics/gitmeta.py` -> identical; same for `__init__.py`. Both pairs byte-identical at archive. |
| **No AST re-anchor** | `git diff --name-only 2177d5f^ 18ea25d` contains no path under `bootstrap/_scaffold/`. The plan cannot have moved the AST baseline. |
| **The stopping rule** -- no new CLI, config key, output column, exported helper, or mandated commit convention | The four names Chunk A adds are all underscore-private: `_STAGE_SCOPE_PREFIX_RE`, `_STAGE_PHRASE_SEP_RE`, `_HEAD_ANCHORED_STAGES`, `_stage_for_subject`. The `__init__.py` change is **docstring-only**. No CLI, config key, or output column added; no commit convention mandated -- which is exactly the residual (e)/(g) the code review dispositioned. |

**Evidence ledger -- accepted residuals, carried as record and not as work.**

| residual | disposition |
|---|---|
| The **eight transcribed literals** with zero live-corpus constraint (**(b)**, known omission (h)) | Accepted. Every one is transcribed from a ratified design, so narrowing any of them is a Decision-level change, not follow-up work. |
| **Nothing guards `_STAGE_COMMIT_PATTERNS` against a future *widening* edit** | Accepted. Such a guard is a new test with a new oracle and sits outside this plan's scope fence. |
| The **scoped-but-not-a-transition** residual -- 10 of 14 measured probes classify inside the gate, and the gate's safety rests on an undocumented subject convention (**(e)**, omission (g)) | Already homed: pinned as documented outcomes in T2b's literal table in `bootstrap/tests/test_lifecycle_stage_patterns.py`. Whether an adopter-facing safety claim may rest on an undocumented convention is a doctrine question and would be a new proposal, not an amendment here. |
| The **one pre-existing shipped-pattern false positive** (`review: tighten the recharge bounds` -> `reviewed`) | Already homed: an explicitly-labelled expectation in T2's table, whose docstring records that it is inherited, not chosen. |
| The **transition-lint verdict** | Already homed in the source proposal's `## Decision`. Not re-stated or re-opened here. |
| **R12c** (both halves), the **`Exact`-with-empty-`hours_*`** tier row, and the **~17-tier price** question | Migrated to `dev/PLANNING.md > Queued` in this commit, as the Lasting-truth table pre-declared. |

**What this plan did not settle, and hands to the Maintainer.** The code review
judged all three sound; none is a measurement this archive can close. (a) The
ratified narrowing's reliability-tier cost is the live-corpus figure, not the one
priced at Decision time. (b) The scope gate's safety rests on a convention the
fix deliberately declines to document -- and for an adopter with no such habit,
the honest outcome is silent degradation to `Good`. (c) The **shipped**,
unedited vocabulary makes one wrong-stage assignment on Cairn's own corpus,
because a subject matches `^Review\b` across a hyphen. (c) ships to adopters and
is the one worth a decision.

This section is append-only once written.
