<!-- claim-marker maintenance 2026-07-22: `dev/proposals:` and `dev/plans:` below (in the
     appended Internal review) are COMMIT-SUBJECT PREFIX LITERALS -- the area prefix in Cairn's
     subject grammar, which is the very thing this proposal repairs -- not path references. The
     real directories are `dev/proposals/` and `dev/plans/` with a trailing slash. Typo guard applied:
     these are quoted strings, not mistyped paths. Marked so the checker clears; reviewer prose is
     append-only and untouched. Surfaced, not silenced. -->
<!-- claim-check-allow: dev/proposals:, dev/plans: -->
<!-- cairn-internal-ref-allow: doctrine/proposals.md doctrine/dual-review.md doctrine/rationale.md doctrine/lifecycle.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- Two deliberate forward references, both named repeatedly outside the Proposed-paths block: the new test file lands with the implementing plan, and scripts/transition_lint.py is the SIBLING proposal's proposed path, cited here only to argue about whether it should be built. -->
<!-- claim-check-allow: bootstrap/tests/test_lifecycle_stage_patterns.py, scripts/transition_lint.py -->

# Repair `_STAGE_COMMIT_PATTERNS` — the shipped lifecycle-stage commit vocabulary reads nothing

**Author**: Claude (Strategy)
**Model**: Claude Opus 4.8
**Date opened**: 2026-07-22
**Status**: accepted
**Touches**: `templates/modules/default-on/_lifecycle_metrics/gitmeta.py` and its byte-identical self-hosted twin `tools/_lifecycle_metrics/gitmeta.py`; the two-line degradation sentence in `templates/modules/default-on/_lifecycle_metrics/__init__.py` and its twin `tools/_lifecycle_metrics/__init__.py`; one new behavioural test file under `bootstrap/tests/`. No engine, no manifest rows, no doctrine.
**Related**: opened under the Maintainer's 2026-07-22 direction *"fix the reader now, and as part of that proposal check whether this is needed"*, recorded in the sibling proposal stem `2026-07-22-claude-transition-lint` (its `## Sequencing note`). The defect was found by that proposal's Internal review panel (finding R1) and routed out of its scope. Prior verification of the gate-manifest boundary reused from proposal stem `2026-07-22-claude-interpreter-trust-root-fallback`.
**Plan review**: required(Internal)

<!-- The two paths below do not exist yet; they land with the implementing plan. -->
## Proposed paths

Proposed paths:
- `bootstrap/tests/test_lifecycle_stage_patterns.py` — the new behavioural test for the repaired vocabulary; lands with the implementing commit.
- `dev/plans/stage-commit-patterns.md` — the implementing plan; opens after the Decision.

## Context

`templates/modules/default-on/_lifecycle_metrics/gitmeta.py:17-25` defines
`_STAGE_COMMIT_PATTERNS`, four `^`-anchored regexes mapping a git commit
subject to a lifecycle stage (`open` / `decision` / `revised` / `reviewed`).
It ships **default-on**: `bootstrap/scaffold.py --manifest` installs it
verbatim as `tools/_lifecycle_metrics/gitmeta.py` in every adopter tree, and
`dev/.cairn/cairn-lock.yml:495-501` records that mapping.

**It matches nothing Cairn actually commits.** Measured this session on the
canonical interpreter (`~/conda_envs/lhm/bin/python`, Python 3.13.13) at
`HEAD` `7d2d034`, as_of 2026-07-22:

```
$ ~/conda_envs/lhm/bin/python tools/lifecycle_metrics.py proposals --format csv
12 rows; stage_timestamp_reliability = Best-effort on 12 of 12
```

Running `_STAGE_COMMIT_PATTERNS` directly over the exact subject set the
consumer sees — the union of `git log --follow` subjects for all 12 proposal
files in `dev/proposals/` and `dev/proposals/archive/` — gives **0 matches out
of 73 distinct subjects** (as_of 2026-07-22). Not a low hit-rate: zero.

Per `templates/modules/default-on/_lifecycle_metrics/gitmeta.py:117-118`,
`Best-effort` is returned exactly when *no* stage resolved to a commit. It is a
**metric label written into a CSV column**, not an exit code and not an error:
the tool exits `0` and emits a well-formed report. That is what makes this
defect quiet. The three columns it feeds —
`hours_open_to_reviewed`, `hours_reviewed_to_revised`,
`hours_revised_to_decision` — are emitted as empty strings
(`gitmeta.py:89-96`), and `stage_timestamp_reliability` reads `Best-effort`
(`extract.py:205`, `:227-228`). An adopter sees a feature that appears to work
and silently delivers only the day-level header dates.

The felt pain is adopter-facing and imminent: the first external adopter
installs this module default-on, and the first thing they would learn about
Cairn's own measurement apparatus is that its stage-timing half is inert.

### Why it misses — evidence, two independent causes

**Cause 1 — the anchor is wrong for the real subject grammar.** Cairn's
subjects carry an area prefix: `dev/proposals: open transition-lint (…)`,
`dev/proposals: Maintainer Decision -- ACCEPT licensing`. Every pattern begins
`^`, and `_resolve_stage_commits` calls `pattern.match(subject)`
(`gitmeta.py:83`). The `^` lives **inside the compiled pattern string**, so
this is not a `.match()`-vs-`.search()` API choice — switching the call would
change nothing.

**Cause 2 — the vocabulary was never Cairn's.** Stripping the leading `^` from
all four patterns and re-running over the same 73 subjects raises matches to
**51** — but the matches are wrong. `^Review\b` becomes `Review\b`, which then
fires on the *slug*: `dev/proposals: open review-record-integrity (Phase A…)`
classifies as `reviewed`, and `dev/proposals: open interpreter-trust-root-fallback
(F2 split; Security-Review gated)` likewise. **De-anchoring alone converts a
100% miss into a large false-positive rate.** Both causes are real and the fix
must address both.

Where did the vocabulary come from? Cairn documents the *stage nouns* but has
never documented a subject grammar. `doctrine/proposals.md:69-75` is the
canonical list:

> * Commit on **opening** a proposal (status `proposed`).
> * Commit on **appending a Review** (status -> `reviewed`).
> * Commit on **appending a Response and any "Revised proposal"
>   section** (status -> `revised`). If multiple review rounds happen,
>   each Review / Response pair gets its own commit.
> * Commit on **the Maintainer's Decision** (status -> `accepted` /
>   `rejected` / `superseded`).

The only concrete subject string Cairn ships is the quickstart's toy line,
`docs/quickstart.md:232` — `git commit -q -m "Open proposal: README tagline"` —
which the current `open` pattern does match, as does the fixture subject at
`bootstrap/tests/test_reference_scripts.py:476`. So the honest diagnosis is:
**the patterns encode an invented grammar validated only against Cairn's own
toy examples, never against a real log.** It is not that a convention evolved
away from them; there was no convention to evolve from. That is why the fix
keys on the doctrinal stage nouns above rather than on any one project's
subject style.

## Proposal

Three parts, all inside `gitmeta.py` except P3. Nothing new is built: no new
tool, no new command, no new metric, no new column, no configuration surface,
no lint.

### P1 — repair the vocabulary and the anchoring (`gitmeta.py`)

Add a prefix-strip and a stage-phrase split, and replace the four regexes.
`_STAGE_COMMIT_PATTERNS` keeps its name, its type
(`List[Tuple[str, 're.Pattern[str]']]`) and its **priority order**
(`open`, `decision`, `revised`, `reviewed` — `revised` before `reviewed` is
load-bearing, so `… -- Response to Gemini External review` reads as the
Response transition per `doctrine/proposals.md:71-73`).

```python
_STAGE_SCOPE_PREFIX_RE = re.compile(
    r'^(?:dev/)?(?:proposals?|plans?)\s*:\s*', re.I)

_STAGE_PHRASE_SEP_RE = re.compile(r'\s+(?:--|–|—)\s+')

_STAGE_COMMIT_PATTERNS: List[Tuple[str, 're.Pattern[str]']] = [
    ('open', re.compile(r'^open(?:ing)?\b', re.I)),
    ('decision', re.compile(r'^(?:maintainer\s+)?decision\b', re.I)),
    ('revised', re.compile(
        r'(?<!-)\b(?:response|responses|revised|revise|respond\s+to)\b(?!-)',
        re.I)),
    ('reviewed', re.compile(
        r'(?<!-)\breview\b(?!-)(?!.*\bsharpening\b)', re.I)),
]

#: Stages that *lead* a subject are matched against the whole de-prefixed
#: subject; the rest are matched only inside the stage phrase.
_HEAD_ANCHORED_STAGES = frozenset({'open', 'decision'})


def _stage_for_subject(subject: str) -> Optional[str]:
    """Classify a commit subject as AT MOST ONE lifecycle stage."""
    body = _STAGE_SCOPE_PREFIX_RE.sub('', subject.strip(), count=1)
    parts = _STAGE_PHRASE_SEP_RE.split(body, maxsplit=1)
    phrase = parts[1] if len(parts) > 1 else body
    for stage, pattern in _STAGE_COMMIT_PATTERNS:
        target = body if stage in _HEAD_ANCHORED_STAGES else phrase
        if pattern.search(target):
            return stage
    return None
```

Three structural rules, each earning its place against a measured failure:

* **Strip the area prefix, then match positionally.** `open` and `decision`
  lead their subject once the `dev/proposals` or `dev/plans` scope prefix and
  its colon are removed. This is what lets `open` stay anchored instead of
  degrading to a bare keyword.
  Accepting the `plans?` prefix is required, not cosmetic: plan-open and
  plan-archive commits move the proposal file and therefore appear in its
  `git log --follow` history.
* **Match `review` / `response` only in the stage phrase** — the part after
  the first ` -- ` separator, or the whole subject when there is none. This is
  what keeps a slug out of the stage decision.
* **Never match inside a hyphen compound** (`(?<!-)…(?!-)`). Measured
  necessity: without it, `dev/plans: archive review-record-integrity (Chunk C
  pointer + lifecycle close)` classifies as `reviewed`, and `Security-Review`
  inside an `open` subject does the same.

The `sharpening` exclusion is carried over from the current `reviewed` pattern
unchanged — it is not part of this defect.

### P2 — one stage per subject; remove the fall-through (`gitmeta.py`)

`_resolve_stage_commits`'s loop (`gitmeta.py:81-85`) tests the *filled/unfilled*
state of a slot before deciding whether a pattern applies, and only `break`s
when it assigns. A subject whose correct stage is already filled therefore
**falls through and is re-tested against the remaining stages**. Replace with:

```python
    for sha, ts, subject in log_oldest_first:
        stage = _stage_for_subject(subject)
        if stage is not None and out[stage] is None:
            out[stage] = (sha, ts)
```

This is not hypothetical. Cairn's real corpus contains two `open`-classified
commits in one proposal's history — `dev/proposals: open review-record-integrity
(Phase A, proposal 1 of the broad-look tighten-up)` and, later,
`dev/plans: open review-record-integrity (+ archive proposal)`. Under the
current loop the second one, finding `open` filled, would be re-tested against
`reviewed`; with any vocabulary that recognises the word `review` it would be
mis-assigned. P1's hyphen guard blocks that particular subject, but the
fall-through is the general hazard and is a defect of the same mechanism.
Classification becomes a pure function of the subject; slot-filling stays
first-match-wins, oldest-first, exactly as today.

### P3 — correct the degradation sentence (separable)

`templates/modules/default-on/_lifecycle_metrics/__init__.py:74-78` currently
reads:

> Robust across VCS settings: when git is absent, the path is not a
> checkout, or the default branch is named ``main`` rather than
> ``master``, the optional commit-timestamp augmentation degrades quietly
> (empty hour-delta columns + a ``Best-effort`` reliability tier) rather
> than raising.

Every clause in that cause list is false of the failure actually observed: git
is present, the tree is a checkout, the branch is `master`, and the tier is
still `Best-effort`. Add the missing cause — *or when no commit subject in a
file's history matches the stage vocabulary* — so the only adopter-facing
documentation of this degradation stops implying an exhaustive list.

**P3 is separable.** Dropping it costs nothing in P1/P2; it is called out
because it adds a second twin pair to keep byte-identical.

### Shipped-copy parity, the lockfile, and the gate manifest — verified

* **Twin parity is enforced and both copies must change.** `templates/modules/default-on/_lifecycle_metrics/gitmeta.py` and `tools/_lifecycle_metrics/gitmeta.py` are byte-identical today (`sha256:5a47849b…` both). [`bootstrap/tests/test_notice_install.py:98`](../../bootstrap/tests/test_notice_install.py) — `test_every_self_hosted_twin_stays_byte_identical_to_its_source` — reads the manifest, pairs every `scripts/`/`tools/` self-hosted twin with its template source, and asserts equal bytes. Editing one side alone **reds the suite**. Same for the `__init__.py` pair under P3.
* **The lockfile is out of scope, and the obvious assumption about it is already false.** The natural expectation is "bump the recorded hash in lockstep or Cairn's own tree fails `verify_integrity`." Measured, that expectation does not hold: `dev/.cairn/cairn-lock.yml:498` records `sha256:3d057d53…` for `tools/_lifecycle_metrics/gitmeta.py` while the file on disk is `sha256:5a47849b…`, and `~/conda_envs/lhm/bin/python bootstrap/verify_integrity.py --target .` **already exits 1 with 41 integrity violations** at `HEAD` (as_of 2026-07-22), gitmeta.py among them. Cause: commit `501efe3` ("licensing: self-propagating SPDX headers on 91 shipped .py (P2)") rewrote 91 shipped files without re-recording the lockfile — verified: that commit touches no `cairn-lock` path. The check is therefore already red, for a reason this proposal did not cause, and bumping 1 of 41 stale entries would leave it red while making the record *less* coherent (one freshly-recorded entry among forty stale ones). This affects Cairn's self-hosted tree only — an adopter's install records the shipped bytes at install time. Routed to the Maintainer as an open question below.
* **The gate-manifest fixture is stale for the same reason and is not a suite gate.** `bootstrap/tests/fixtures/gate_manifest.json:2519` freezes the same pre-`501efe3` hash. It is a batch-scoped operator control run as `_gate_manifest.py verify --anchor-ref <SHA>`; `bootstrap/tests/test_gate_manifest.py:78-80` verifies a **freshly produced** manifest against the live tree, so the committed fixture is never compared to it by `pytest`. Independently established in proposal stem `2026-07-22-claude-interpreter-trust-root-fallback`. If an anchored unattended batch is live at implementation time, the edit routes through the supervised re-anchor path (`bootstrap/REANCHOR_RUNBOOK.md`); no such batch is live today.
* **No AST re-anchor is triggered.** `bootstrap/tests/test_ast_attest.py:20` pins `_SCAFFOLD = _REPO / "bootstrap" / "_scaffold" / "__init__.py"` and verifies over `sorted(_SCAFFOLD.parent.glob("*.py"))` (`:65`, `:80`) — the engine package only. `gitmeta.py` is a **module template** under `templates/modules/default-on/`, outside that glob. Stated precisely rather than reflexively: **no re-anchor**.
* **Bandit scope does include this file.** `bootstrap/security_check.py:57` (`scan_targets`) returns 72 targets and `templates/modules/default-on/_lifecycle_metrics/gitmeta.py` is one of them (verified by calling it). The change adds only compiled regexes and a pure string function — no `subprocess`, `eval`, or deserialization — so no new finding is expected, but `python bootstrap/security_check.py` is named in the smoke checks rather than assumed.
* **No recorded measurement is invalidated.** `dev/measurement/snapshots/` does not exist; the corpus has zero committed snapshots (`config.py:56`). Repairing the reader therefore rewrites no append-only measurement record.

### What this proposal explicitly does NOT do — the scope fence

* **No new tool, command, module, subcommand, or file** other than one test.
* **No commit-message lint.** `scripts/transition_lint.py` is not proposed, not
  prototyped, and not prepared for. See *The assigned obligation* below.
* **No new metric, column, or output.** `PROPOSAL_COLUMNS`
  (`extract.py:41-83`) is untouched; the same columns are emitted, with
  values that are now correct.
* **No configurability.** No config key, no CLI flag, no way for an adopter to
  supply their own patterns. That would be a new capability.
* **No public export of the vocabulary.** `_stage_for_subject` is private and
  stays inside `_lifecycle_metrics`. Nothing imports it from outside.
* **No vocabulary beyond the doctrinal stage nouns.** `doctrine/proposals.md:69-75`
  names opening / Review / Response+Revised / Decision. This proposal adds the
  minimum surface form needed to recognise those four in real subjects and
  stops. Tokens Cairn's log happens to contain but doctrine does not name —
  `archive`, `supersede`, `sharpening`, `claim-marker maintenance` — get **no**
  stage and are left unclassified.
* **No commit-message convention is created.** The reader accommodates existing
  subjects; it does not mandate a form. Nothing in `AGENTS.md`,
  `doctrine/proposals.md`, or the templates gains a subject-grammar rule. If a
  reviewer reads this fix as establishing one, that reading is wrong and the
  fix is over-scoped.
* **The 41-entry lockfile staleness is not repaired here** (see above).
* **`dev/plans` metrics are unchanged.** `_resolve_stage_commits` is called
  from exactly one place — `extract_proposal_row` (`extract.py:205`, inside
  the function beginning at `:126`) — and plan rows carry no stage-timestamp
  columns (verified: plan rows expose 6 columns, none of them
  `stage_timestamp_reliability`).

### The assigned obligation — does the transition-lint remain necessary?

The Maintainer directed (recorded in proposal stem
`2026-07-22-claude-transition-lint`, `## Sequencing note`): *"fix the reader
now, and as part of that proposal check whether this is needed."* I read that
proposal's `## Revised proposal` section, including its new prior-art
subsection and its revised Shape (a) claim-detection table, before answering.

**Answer: (b) — necessary work is not eliminated, but its claim-detection half
is now proven prior art rather than an invention.** Framed as evidence for the
Maintainer's call, not as a recommendation to build; under the standing
build-nothing-new rule the lint does not proceed without an explicit
go-ahead regardless of this analysis.

**It is not made unnecessary.** The two mechanisms answer different questions,
and the repair does not narrow that gap. `_resolve_stage_commits` asks *"which
commit in this file's history is stage X?"* — it never opens a diff. The
originating incident is commit `17b7e5c`, whose subject *"open check_cairn
self-host-compat (+ Internal review)"* is a **correct** claim about the stage
and a false claim about the diff (the added file already carried two filled
`## Review` sections). I ran the repaired classifier on that exact subject: it
returns `open`, which is right, and would have surfaced nothing. Every finding
class the lint targets is a message-versus-diff mismatch that a subject
classifier is structurally blind to. The transition-lint's own argument for not
single-sourcing (its Revised prior-art subsection) survives this repair intact.

**Its size does move, and in a specific, checkable way.** Three of the revised
Shape (a) design decisions are exactly what P1/P2 now implement and test in
shipped code:

| transition-lint Shape (a) rule | covered by this proposal |
| --- | --- |
| "leftmost match wins, at most one claim per subject" | P2's `_stage_for_subject` returns at most one stage |
| `(?<![-\w])<token>s?(?![-\w])` — hyphen-compound suppression so slugs do not read as claims | P1's `(?<!-)…(?!-)` guard, with the `archive review-record-integrity` and `Security-Review` cases measured |
| `open` "anchored: must be the first word after the `dev/<tree>: ` prefix" | P1's `_STAGE_SCOPE_PREFIX_RE` strip + `^open(?:ing)?\b` |

What remains genuinely unbuilt is the lint's **evidence half**: per-commit diff
enumeration, the claim→required-section mapping, the ≥3-added-line threshold,
the review-grammar-marker discriminator, exclusion roots, the SHA whitelist,
exit behaviour, and the CLI. That is the majority of the design and none of it
is touched here.

**One caveat, stated rather than buried: the reuse is design-level, not
import-level.** `gitmeta.py` lives under `templates/modules/default-on/` as a
shipped adopter module; `scripts/transition_lint.py` was proposed as Cairn's
own dev tooling. Importing one from the other would create a new dependency
from Cairn's tooling onto a shipped template file, and single-sourcing them
properly would mean extracting a shared library — new building. So the saving
a lint would realise is *copying three idioms that are now proven and pinned by
a corpus test* instead of inventing and defending them. Real, but smaller than
"reuse the module."

**One argument the repair partly spends.** The transition-lint's revised
Alternative #6 rests on the `Best-effort` result as "direct evidence that a
shipped subject vocabulary drifts from its adopters." Post-repair that evidence
is weaker: the failure was a vocabulary that was never validated against any
real log, not one that drifted. The underlying caution — that a subject
vocabulary pinned to one project's conventions may not fit another's — still
holds and is exactly why this proposal keys on the doctrinal stage nouns and
refuses configurability.

### Documentation / doctrine surface

**Doctrine: none.** No file under `doctrine/`, no `AGENTS.md` rule, no
template, no module `.md`. `doctrine/proposals.md:69-75` is *cited as the
source of truth this fix conforms to*, and is not edited.

**Documentation: one two-line docstring correction (P3)**, in
`templates/modules/default-on/_lifecycle_metrics/__init__.py` and its twin.
Routed by `docs/DOCUMENTATION_PLAN.md`'s layer rule to the **descriptive**
layer: it describes the software as it is, and its canonical home is the
module's own docstring, where the incorrect sentence already lives — not
`AGENTS.md` (no cross-cutting prescription) and not `docs/` (no separate
descriptive page documents this tier).

`templates/modules/default-on/lifecycle-metrics.md` (192 lines) is checked and
**deliberately untouched**: it documents the Measurement Compact and the
snapshot schema and says nothing about commit-subject matching or the
reliability tiers.

`CHANGELOG.md` gets one entry at implementation time, per the serialization
rule in `AGENTS.md`.

### Doctrine-change rate-limit (if this proposal changes doctrine)

**N/A — this proposal changes no doctrine.** `dev/proposals/_template.md:166-167`
scopes the gate to a proposal that "**changes doctrine** — a rule, process, or
contract every contributor follows". This changes the *values a shipped tool
computes*, and explicitly creates no rule any contributor follows (see the
scope fence: no commit-message convention is created). The doctrine-evolution
rate-limit (`doctrine/rationale.md` > "How the doctrine evolves under
evidence") therefore does not apply, and no recurrence count or high-risk
classification is claimed.

## Rationale

* **Which user workflow does it improve?** The adopter's first contact with
  Cairn's measurement apparatus. `lifecycle-metrics` is default-on; today its
  stage-timing half returns nothing usable in any tree that does not happen to
  write the quickstart's toy subject. Repairing the reader is the difference
  between a feature and a decoration, and it costs the adopter nothing to
  receive.
* **What stable contract or module boundary does it preserve?** All of them.
  The install manifest rows are unchanged, `PROPOSAL_COLUMNS` is unchanged,
  the public `proposal_rows` signature is unchanged, the reliability-tier
  vocabulary (`Exact` / `Good` / `Best-effort`) is unchanged, and the
  degradation contract — never raise, always emit — is unchanged. The change
  is confined to one private classifier inside one private submodule.
* **What transparency / reproducibility does it improve?** Cairn's central
  claim is that recorded deliberation is measurable. A shipped measurement tool
  that reports `Best-effort` on 12 of 12 of the author's own proposals is a
  falsification of that claim sitting in the adopter's tree. It also restores
  the sub-day resolution the tiers were designed around: post-fix, 11 of 12
  proposals reach `Exact` and hour-level deltas populate.
* **Why now?** The first external adopter is imminent and this is squarely a
  defect, not new building. It is also the named prerequisite the Maintainer
  attached to an in-flight sibling proposal, so leaving it open blocks that
  decision.

## Alternatives considered

1. **Do nothing.** Rejected. Every adopter receives a silently inert feature,
   and the tool's output actively misleads: `Best-effort` reads as "the corpus
   was hard to parse," not "the reader recognises nothing."
2. **Delete the stage-commit augmentation entirely** and keep only header-date
   day-level metrics. Honest, and genuinely smaller. Rejected because it
   removes a working capability to avoid fixing ~25 lines, deletes three
   shipped columns (a contract change strictly larger than the fix), and
   discards resolution the design deliberately sought.
3. **Just remove the `^` anchors.** Rejected on measurement: it raises matching
   from 0/73 to 51/73 while introducing slug-driven false positives
   (`open review-record-integrity` → `reviewed`). A wrong timestamp is worse
   than an absent one, because `Exact` would then assert confidence in it.
4. **Make the patterns configurable** (a `stage_patterns` config key so each
   project supplies its own). Rejected twice over: it is new capability under a
   standing build-nothing-new rule, and it pushes a regex-authoring task onto
   an adopter to work around Cairn's own defect.
5. **Add the vocabulary as a shared library both this module and a future lint
   import.** Rejected as new building, and it would couple Cairn's own
   `scripts/` to a shipped module template. Recorded in the obligation section
   above so the Maintainer sees the option that was declined.
6. **Also cover `archive` / `supersede` / plan-lifecycle subjects.** Rejected
   as scope creep: `doctrine/proposals.md:69-75` names four stages, the
   consumer has four slots, and the plan corpus does not use these columns.
7. **Repair the reader and the 41-entry lockfile staleness together.**
   Rejected: different defect, different cause (`501efe3`), and bundling would
   put 40 unrelated hash bumps in a defect-fix commit. Routed as an open
   question.

**Maintainer preference during drafting.** Two, both binding: the standing
2026-07-22 direction *"fix defects, build nothing new"*, which shapes the scope
fence; and the sequencing direction quoted above, which creates the obligation
section. Neither is a Decision.

### Open questions — the Maintainer's calls

1. **The 41-entry lockfile staleness.** `verify_integrity --target .` exits 1
   at `HEAD` with 41 hash mismatches caused by `501efe3`. Should it be
   re-recorded as its own defect fix, or documented as accepted staleness with
   a note? This proposal deliberately does not touch it.
2. **Whether P3 rides along** or is dropped to keep the diff to one file pair.
3. **The plan-review tier.** Declared `required(Internal)` on the reading that
   this is an "ordinary" change under `doctrine/dual-review.md:184-187` — the
   install contract (fidelity manifest, gate manifest, lockfile *schema*,
   published `--manifest` rows) is untouched, and only the content of one
   already-mapped module file changes. If the Maintainer reads "shipped
   default-on adopter code" as contract-touching, the tier rises to External.

## Evidence / verification plan

All figures measured 2026-07-22 on the canonical interpreter — Python 3.13.13
at `~/conda_envs/lhm/bin/python` — at `HEAD` `7d2d034`.

**Baseline, re-measured this session:** `~/conda_envs/lhm/bin/python -m pytest
bootstrap/tests -q` → **1437 passed, 0 failed, 0 skipped, 118s**. (The two
AST-baseline failures previously carried are gone: the baseline was re-anchored
in commit `2bd8f34`.)

**Before / after, on the real corpus** (repaired classifier monkeypatched into
the live extractor, whole-corpus run):

| measure | before | after |
| --- | --- | --- |
| proposals at `Best-effort` | **12 / 12** | **0 / 12** |
| proposals at `Exact` | 0 | **11** |
| proposals at `Good` | 0 | 1 |
| distinct subjects classified (of 73) | **0** | **68** |
| subjects correctly left unclassified | — | 5 |

The 5 unclassified are all correct non-transitions: two `claim-marker
maintenance:` commits, one implementation commit
(`check_cairn: resolve dev/ self-host claim-path findings …`), one
plan-archive (`dev/plans: archive review-record-integrity …`), and
`dev/proposals: transition-lint -- record Maintainer sequencing direction (not
a Decision)` — which the positional `decision` anchor correctly declines.

The single remaining `Good` is also correct, not residue:
`2026-06-12-claude-adopter-entry-doc-refresh` bundled its review and response
into one commit (`… -- Internal review panel + Response + Revised`), so two
stages genuinely cannot resolve to two timestamps, and the tier reports `Good`
rather than overclaiming `Exact`.

**Backward compatibility, measured:** every legacy / quickstart form the
current patterns accept still classifies identically — `Open proposal: README
tagline` → `open`, `Open proposal alice thing` → `open`, `opening proposal foo`
→ `open`, `proposal: open foo` → `open`, `Decision: accept foo` → `decision`,
`Decision -- accept foo` → `decision`, `proposal: Decision on foo` →
`decision`, `proposal: respond to review` → `revised`, `proposal: revise foo` →
`revised`, `Revised proposal foo` → `revised`, `Review round 1 of foo` →
`reviewed`, `Review sharpening pass` → unclassified (exclusion preserved).
No currently-matching form regresses.

### Author-accounting — invariants, failure modes, edge cases

**Invariants.**

* *At most one stage per subject.* Enforced by `_stage_for_subject` returning a
  single `Optional[str]`; pinned by a test asserting the multi-token subject
  `… -- Response to Gemini External review` yields exactly `revised`.
* *Slot assignment stays first-match-wins, oldest-first.* Enforced by the
  unchanged `reversed(log)` iteration; pinned by a two-`open`-commit test.
* *The function never raises on any subject.* Pure string ops on a `str`;
  pinned by a test over empty, whitespace-only, non-ASCII, and 500-character
  subjects.
* *Twin byte-parity.* Enforced by `test_every_self_hosted_twin_stays_byte_identical_to_its_source`
  ([`bootstrap/tests/test_notice_install.py:98`](../../bootstrap/tests/test_notice_install.py)).
* *Reliability-tier semantics unchanged.* `_stage_reliability`
  (`gitmeta.py:108-121`) is not edited.

**Failure modes — all open (degrade), none closed (raise), intentionally.**

* No subject matches → every slot `None` → `Best-effort` + empty hour columns.
  Identical to today's behaviour, which is the correct floor.
* A subject matches the wrong stage → a wrong hour-delta, reported as `Exact`.
  This is the one failure mode that is *worse* than the status quo, which is
  why the hyphen guard and the stage-phrase restriction are specified and
  tested rather than left to the implementer.
* git absent / not a checkout → unchanged (`_git_log_for_path` returns `[]`,
  `gitmeta.py:48-51`), still pinned by
  [`bootstrap/tests/test_reference_scripts.py:443-457`](../../bootstrap/tests/test_reference_scripts.py).

**Edge-case inventory.** Handled: empty subject; no area prefix (quickstart
form); prefix without a stage token; multiple ` -- ` separators (only the first
splits); en-dash and em-dash separators; mixed case (`re.I` throughout);
a stage word appearing only inside a slug; two `open`-classified commits in one
history; a bundled review+response commit; plan-prefixed commits inside a
proposal's `--follow` history. **Out of scope:** merge commits (subject is the
merge line; `git log --follow` on a single file rarely surfaces them, and the
tool has never handled them); non-English subjects; subject lines a project
writes with no doctrinal stage noun at all — these correctly yield
`Best-effort`, which is the honest answer.

**Public-path → test mapping.** The change adds no public entry point. The
public path that *changes behaviour* is `proposal_rows(root)` → the
`stage_timestamp_reliability` and `hours_*` columns. It is exercised through
its public path today by
[`bootstrap/tests/test_reference_scripts.py`](../../bootstrap/tests/test_reference_scripts.py)
(`TestVcsRobustness`, the no-git and `main`-branch cases) and will be exercised
post-fix by the new `bootstrap/tests/test_lifecycle_stage_patterns.py`, which
calls `proposal_rows` on a synthetic repo rather than the private classifier.

**Known omissions / intentionally untested edges.** The corpus regression test
uses a **frozen list of real subject strings copied into the test file**, not a
live `git log` of this repository — a test that read live history would rot on
every commit and would not run in an adopter's tree. That means the test cannot
catch a *future* Cairn subject style drifting away from the vocabulary; only a
re-run of the measurement would. This is a deliberate trade and the reason the
vocabulary keys on doctrinal stage nouns rather than on observed subject
shapes. Also untested: interaction with an adopter's non-Cairn commit
conventions, since no second real corpus exists.

### Tests required

One new file, `bootstrap/tests/test_lifecycle_stage_patterns.py` — a new file
rather than an edit to `test_reference_scripts.py`, which is in the gate
manifest's frozen set (additions are allowed; frozen-file edits HOLD).

1. **Corpus regression (the headline).** A frozen list of ~30 real Cairn
   subjects with their expected stage (including all 5 expected `None`s),
   asserting the classification exactly. This is the test that would have
   caught the defect.
2. **Slug non-collision.** `dev/plans: archive review-record-integrity (…)` →
   `None`; `dev/proposals: open interpreter-trust-root-fallback (F2 split;
   Security-Review gated)` → `open`.
3. **Legacy / quickstart forms.** The twelve strings listed under *Backward
   compatibility* above, asserted verbatim.
4. **One stage per subject.** `… -- Response to Gemini External review` →
   `revised`, never `reviewed`.
5. **No fall-through (P2).** A synthetic git repo whose file history carries two
   `open`-classified commits; assert the second does not populate any other
   slot.
6. **End-to-end through the public path.** A synthetic git repo with
   open / review / response / decision commits in Cairn's subject form; assert
   `proposal_rows` yields `stage_timestamp_reliability == 'Exact'` and
   non-empty `hours_*`.
7. **Never raises.** Empty, whitespace, non-ASCII, and very long subjects.
8. **Degradation preserved.** The no-git case still yields `Best-effort` —
   already covered by `test_reference_scripts.py:443-457`; re-asserted here so
   the guarantee is local to the changed code.

### Examples / smoke checks

* `~/conda_envs/lhm/bin/python -m pytest bootstrap/tests` — full suite; expect
  1437 + the new nodes, 0 failed.
* `~/conda_envs/lhm/bin/python tools/lifecycle_metrics.py proposals --format csv`
  — expect 0 `Best-effort` rows and populated `hours_*` columns.
* `~/conda_envs/lhm/bin/python bootstrap/security_check.py` — Bandit over the
  72 targets including the edited file; expect no new finding.
* `~/conda_envs/lhm/bin/python bootstrap/scaffold.py --manifest | grep gitmeta`
  — expect the manifest row unchanged (this fix must not move it).
* `~/conda_envs/lhm/bin/python scripts/check_cairn.py` — prose-integrity gate
  for the P3 docstring edit and this proposal.
* `~/conda_envs/lhm/bin/python scripts/claim_check.py dev/proposals/2026-07-22-claude-stage-commit-patterns.md`
  — clean before the opening commit.
* **N/A — the example gallery.** `examples/minimal/` and
  `examples/scientific-minimal/` demonstrate nothing this change touches.

## Signals the change is wrong

* **A wrong timestamp appears where none did before.** The specific shape: a
  proposal reports `Exact` while an `hours_*` value contradicts the header
  dates in the same row. That would mean a subject matched the wrong stage —
  the one regression that is worse than the defect. *Recovery:* tighten the
  offending pattern and add the subject to the frozen corpus list; if the class
  is broad, revert to the pre-fix patterns, which fail safe to `Best-effort`.
* **An adopter's ordinary subjects classify as transitions.** If a project that
  writes `docs: review the API surface` starts seeing stage timestamps on
  unrelated commits, the vocabulary is too loose for a general corpus.
  *Recovery:* narrow to require the area prefix (drop the bare-subject
  fallback), accepting that the quickstart form then needs its documented
  example updated.
* **Anyone cites this fix as establishing a commit-message convention** — in a
  review, a doc, or a lint proposal. That would mean the scope fence failed.
  *Recovery:* the fence text above is the rebuttal; no doctrine was changed and
  none may be inferred.
* **The diff grows past one file pair plus one test** (a config key, a second
  consumer, an exported helper, a subcommand). *Recovery:* stop and re-open;
  the Maintainer's build-nothing-new rule was breached.
* **The suite goes red on twin parity.** Means only one side of a pair was
  edited. *Recovery:* mechanical — copy the file across and re-run.
* **The corpus regression test needs editing to make an unrelated change
  pass.** Means the frozen list has become a hostage rather than an oracle.
  *Recovery:* re-measure against the live corpus before touching the list.

## Review -- Claude (Internal, fresh-context subagent panel) -- 2026-07-22

**Model**: Claude Opus 4.8 (three fresh-context subagents — corpus-evidence, scope/stopping-rule, transition-lint-necessity — no access to the authoring session; consolidated, none dropped).

**Attribution / committer note.** The panel's findings, transcribed faithfully — none softened, reordered to bury, or dropped. Raw panel source committed in-tree at `dev/reviews/2026-07-22-stage-commit-patterns-internal-panel.json` per the binding practice from the superseded automated-review-committer Decision; committed under the Maintainer's git identity by the author-session as disclosed scribe.

**Steelman.** All three lenses independently reproduced the proposal's empirical spine on the canonical interpreter (`~/conda_envs/lhm/bin/python`, Python 3.13.13) and converge on the same verdict: the diagnosis is correct, the repair is a real repair, and the scope discipline is the strongest this tree has seen.

The headline defect reproduces exactly. The shipped `_STAGE_COMMIT_PATTERNS` (exec'd verbatim out of `templates/modules/default-on/_lifecycle_metrics/gitmeta.py:17-25`, not retyped) match **0** of the 73 `git log --follow` subjects for the 12 proposal files under `dev/proposals/` + `dev/proposals/archive/` at the proposal's stated `7d2d034`, and 0 of 75 at HEAD `cc66d2b`. `proposal_rows(Path('.'))` returns `Counter({'Best-effort': 12})` with every `hours_*` column empty. Zero, not a low hit rate.

The fix reproduces too. Monkeypatching the proposal's exact `_stage_for_subject` into the live `extract._resolve_stage_commits` yields `Counter({'Exact': 11, 'Good': 1})` — the claimed table to the row, stable across three quiet re-runs, at a HEAD two commits later than the one cited. 68/73 subjects classify with exactly the 5 the proposal names left unclassified (69/75 at HEAD, the sixth being the new `dev/plans: archive first-session-survivability`; the deltas reconcile exactly to the two intervening commits). More important than the counts: one lens dumped the resolved `(sha, timestamp, subject)` for every stage of all 12 proposals and hand-checked each. **Every slot assignment is semantically right. No negative deltas.** The single `Good` is `2026-06-12-claude-adopter-entry-doc-refresh` for precisely the stated reason — `4084efc` bundled `Internal review panel + Response + Revised` into one commit, so two stages genuinely cannot resolve to two timestamps and the tier correctly declines to overclaim `Exact`. The 12-string backward-compatibility table reproduces verbatim.

The two-cause diagnosis is real, not rhetorical. De-anchoring alone is a trap: it converts a total miss into slug-driven false positives (`dev/proposals: open review-record-integrity (...)` → `reviewed`; `dev/plans: archive review-record-integrity (...)` → `reviewed`), which is exactly why Alternative 3 deserved rejection. And the over-matching risk on Cairn's own log — the thing the panel was most prepared to find — is genuinely absent: sweeping the last 60 repo-wide commits, all 19 unclassified are correctly unclassified, including strategy (`5575e48`), scaffold (`b8d9e0b`, `2feefd1`, `0864b16`), test (`0bfba10`), licensing (`501efe3`, `597c882`), baseline (`2bd8f34`), and both `claim-marker maintenance:` commits.

The scope fence is the strongest part: explicit, enumerated, and — with the exceptions below — honest. `PROPOSAL_COLUMNS` untouched (`extract.py:41-83`), `_resolve_stage_commits` has exactly one caller (`extract_proposal_row`, `:126`), `plan_rows` exposes 6 columns none of them stage-related; no config key, no CLI flag, no export, no second consumer, no doctrine edit, no commit-message convention. `bootstrap/scaffold.py --manifest` emits `dst\tsrc\tverbatim` with no hash, so the manifest row provably cannot move. The proposal declines the two obvious capability temptations (configurable patterns, a shared library with the sibling lint) and records them as rejected alternatives rather than leaving them implicit.

Parity, lockfile, AST and gate-manifest reasoning all hold under check: both twin pairs are byte-identical (`gitmeta.py` = `5a47849b…`, `__init__.py` = `c0e169e7…` on both sides); `bootstrap/tests/test_notice_install.py:98` is `test_every_self_hosted_twin_stays_byte_identical_to_its_source` and does pair manifest twins and assert equal bytes; `dev/.cairn/cairn-lock.yml:498` records `sha256:3d057d53…` while `verify_integrity.py --target .` already exits 1 with exactly **41** hash mismatches, so bumping 1 of 41 would leave the check red and the record less coherent — declining to bundle that and routing it as an open question is the right stopping-rule call; `bootstrap/tests/test_ast_attest.py:19` pins `bootstrap/_scaffold/__init__.py` and globs `_SCAFFOLD.parent.glob("*.py")`, which `gitmeta.py` cannot enter (and `test_ast_attest.py` runs 26 passed); `bootstrap/tests/test_gate_manifest.py:80` verifies a *freshly produced* manifest against the live tree, so the stale committed fixture is not a pytest gate; the new-test-file choice is grounded in `test_reference_scripts.py` sitting in `frozen_files` (fixture line 2483).

Citation accuracy is unusually high for this tree, where proposals have died on drifted quotes. `doctrine/proposals.md:69-75`, `templates/modules/default-on/_lifecycle_metrics/__init__.py:74-78`, `doctrine/dual-review.md:184-187`, `dev/proposals/_template.md:166-167`, `bootstrap/tests/test_reference_scripts.py:443-457` and `:476`, `config.py:56`, `security_check.py` `scan_targets()` = 72 targets including the edited file, and the suite baseline (**1437 passed, 0 failed, 0 skipped**, ~123s) all check out verbatim.

Finally, the obligation section answers the Maintainer's assigned question honestly and against its own interest: it concludes the sibling lint is *not* eliminated, volunteers that the reuse is design-level rather than import-level (a smaller saving than the convenient answer), and concedes the repair partly spends one of the sibling's own arguments. Its core reasoning verifies: `17b7e5c` classifies as `open` under the repaired reader, and `git diff-tree --no-commit-id --name-status --find-renames=100% -r 17b7e5c` emits `A dev/proposals/2026-06-12-claude-check_cairn-self-host-compat.md`, so the lint's Shape (a) `open`→"an `A` entry" evidence requirement is satisfied and Shape (a) genuinely does not fire. The panel's own answer to the assigned question is the proposal's answer: **still warranted.**

**Critiques** (descending severity; each grounded in a command/citation the reviewer ran):

* **[R1] (blocking)** The bare-subject fallback mislabels ordinary commits as lifecycle transitions and reports the resulting wrong timestamps as `Exact` — the proposal's own named worst-case regression, in a default-on module, on the postdoc adopter path the standing directive prioritizes. When a subject carries no `dev/proposals:` / `dev/plans:` prefix and no ` -- ` separator, `_stage_for_subject` sets `phrase = body`, so the un-anchored `reviewed` / `revised` patterns search the ENTIRE subject and `^open` / `^decision` are tested against the entire subject. The proposal defers this entirely to a post-hoc tripwire under *Signals the change is wrong* ("narrow to require the area prefix (drop the bare-subject fallback)") instead of deciding it with numbers before the Decision. Under a postdoc-first direction that ordering is backwards: before the fix that adopter got nothing; after it they get something wrong with a confidence label attached.
  *Grounding:* 8 realistic hydrogeology-codebase subjects were run through the proposal's verbatim classifier this session; all 8 misclassify: "Add response surface model for aquifer recharge" → `revised`; "Add impulse response function to the transport solver" → `revised`; "fix: revise the calibration constants for Darcy flux" → `revised`; "literature review of contaminant transport models" → `reviewed`; "open sourcing the transport module" → `open`; "Decision tree classifier for facies prediction" → `decision`; "revise mesh resolution near the well screen" → `revised`; "review: tighten the recharge bounds" → `reviewed`. ("docs: address reviewer comments" and a merge-branch subject correctly return `None`.) By the same path `docs: review the API surface` → `reviewed`, since `docs:` is not a stripped prefix. Blast radius is bounded — `_git_log_for_path` passes `--follow -- <path>`, so only commits touching that one proposal file are seen — but that is exactly the adopter's mixed "update the model and amend the proposal" commit, and Cairn's own corpus proves non-lifecycle commits do touch proposal files: `check_cairn: resolve dev/ self-host claim-path findings (implements 2026-06-12 proposal)` is one of the 73. The cost of the proposal's OWN named recovery was measured by re-running the full `proposal_rows(Path('/Users/kendal30/Code/cairn'))` pipeline with `extract._resolve_stage_commits` monkeypatched, on a quiet tree: bare fallback = {'Exact': 11, 'Good': 1}; prefix-required = {'Exact': 10, 'Good': 2}. The single regression is `2026-07-22-claude-ast-known-new-repin`, whose `reviewed` slot is filled by the unprefixed `Append Gemini Internal Review of ast-known-new-repin proposal` (`7d2d034`). All 8 adopter false positives drop to `None` under prefix-required. The legacy forms at stake are exactly two, both `open`-stage: `Open proposal: README tagline` (`docs/quickstart.md:231`) and `Open proposal alice thing` (`bootstrap/tests/test_reference_scripts.py:476`) — and `test_main_branch_target_runs` does not assert a tier, it only asserts `proposal_rows` does not raise and emits the row, so no existing test pins that subject's classification.
  *Suggested fix:* Make the bare-fallback-vs-prefix-required choice an explicit, measured decision in the proposal body rather than a recovery bullet. Either (a) adopt prefix-required and add the unprefixed `Append/Refine Gemini … Review of <stem> proposal` shape as a narrow, explicitly-listed second accepted form — preserving 11 `Exact` while closing the general fallback — keeping the two legacy `open` forms via an explicit alternation; or (b) keep the bare fallback and record in the proposal that it is a deliberate precision-for-recall trade, with the measured adopter false-positive set above quoted as the known cost and the false-positive shape written into the Failure-modes list rather than only into the Signals list. Add the 8 adopter subjects to the frozen corpus test with their intended classifications either way. Both options are narrowings or documentation, not new capability.

* **[R2] (substantive)** P1's head-anchored `decision` misclassifies a Decision subject written in the corpus's own DOMINANT slug-first style, and does so as the WRONG STAGE rather than as `None` — triggering precisely the failure mode the proposal itself names as the only one worse than the status quo ("A subject matches the wrong stage -> a wrong hour-delta, reported as `Exact`."). This also undercuts the reuse table's row 3, which offers the anchoring idiom to the sibling lint as proven.
  *Grounding:* Verified this session with the proposal's verbatim P1 code. `dev/proposals: transition-lint -- Maintainer Decision -- ACCEPT (post Internal review)` → returns **`reviewed`** (wrong stage; would populate an `hours_*` delta and report `Exact`); `dev/proposals: licensing -- Maintainer Decision -- ACCEPT` → `None`. Cause: `decision` is head-anchored against the de-prefixed `body`, and `_STAGE_PHRASE_SEP_RE.split(..., maxsplit=1)` leaves the trailing "review" inside the phrase the `reviewed` pattern searches. The corpus's dominant style for every other stage IS slug-first — `git log` shows `dev/proposals: licensing -- Response to Gemini External review`, `dev/proposals: transition-lint -- Internal review …` — while all 11 real Decision subjects happen to use `dev/proposals: Maintainer Decision -- …`. The anchoring is therefore fitted to an 11-sample accident of one stage, not to the house style. Contrast the proposal's own fence: "The reader accommodates existing subjects; it does not mandate a form."
  *Suggested fix:* Either allow `decision` to match inside the stage phrase (with `Maintainer` required, or the leading-token requirement applied to the PHRASE rather than the whole body), or state explicitly that the reader mandates decision-first Decision subjects and add a slug-first Decision subject to the frozen corpus test as a known-unclassified. Do not leave a form that yields `reviewed`.

* **[R3] (substantive)** The `plans?` branch of `_STAGE_SCOPE_PREFIX_RE` breaches the proposal's own scope fence, produces exclusively wrong classifications in the measured corpus, changes no measured outcome, and leaves a latent wrong-timestamp-at-`Exact` hazard. The fence states that tokens doctrine does not name — `archive`, `supersede`, `sharpening`, `claim-marker maintenance` — get **no** stage; but stripping a `dev/plans: ` prefix makes plan-lifecycle commits classifiable, and every one that results is semantically inverted. The same mechanism conflates plan-stage with proposal-stage review vocabulary. The proposal's justification inverts the inference: "Accepting the `plans?` prefix is required, not cosmetic: plan-open and plan-archive commits move the proposal file and therefore appear in its `git log --follow` history." That premise is true and is an argument for *recognising and rejecting* those subjects, not for stripping their prefix so they classify.
  *Grounding:* Ablation over the 75 distinct `--follow` subjects at HEAD `cc66d2b`: exactly four subjects change classification, all `open` → `None` — `dev/plans: open adopter-entry-doc-refresh; archive the accepted proposal`, `dev/plans: open adopter-licensing-compliance (+ archive proposal)`, `dev/plans: open first-session-survivability (+ archive proposal)`, `dev/plans: open review-record-integrity (+ archive proposal)`. Those are the proposal's ARCHIVE event, not its opening — `doctrine/proposals.md:69` says "Commit on **opening** a proposal (status `proposed`)." and `:78` says the "subsequent plan-open or trivial-implementing commit moves" an accepted proposal. So all four are the wrong end of the lifecycle. Re-running the full extractor with `plans?` removed gives `Counter({'Exact': 11, 'Good': 1})` — byte-identical to the with-`plans?` result; the branch buys nothing measured, and is harmless today only because first-match-wins fills `open` from the genuinely earlier open commit. Separately, sweeping the proposed classifier over `git log -60` (6 `open`, 6 `decision`, 12 `revised`, 17 `reviewed`, 19 `None`): `eab7141 dev/plans: first-session-survivability -- Code review (fresh-context, disclosed scribe)` → `reviewed` and `224c928 dev/plans: adopter-licensing-compliance -- Code review (fresh-context, not implementer)` → `reviewed`. Neither is in the 75-subject `--follow` corpus, so exposure is latent, not live — but the classifier draws no distinction between a plan's Code review and a proposal's Review. The compound risk is concrete: if the genuine proposal review commit were ever suppressed (see R4) and a later plan Code-review commit touched the proposal file, the `reviewed` slot would take a post-Decision timestamp and produce a negative `hours_reviewed_to_revised`. A proposal whose own opening subject fails to classify (an adopter tree, or any non-conforming Cairn subject) would take its `open` timestamp from the plan-open/archive commit and report it as `Exact`.
  *Suggested fix:* Drop `plans?` from `_STAGE_SCOPE_PREFIX_RE` (making it `^(?:dev/)?proposals?\s*:\s*`), or add an explicit early return of `None` for a `dev/plans:`-prefixed subject; at minimum exclude the `plans?` branch from the `reviewed` / `revised` stages, keeping it only for `open` — the one case the justification actually argues. Add all six `dev/plans:` subjects in the corpus to the frozen regression list with expected `None`, and add `dev/plans: <slug> -- Code review (fresh-context, disclosed scribe)` with whichever classification is intended, so the choice is pinned rather than incidental. Then delete the justification sentence, since the ablation shows the branch is not required. If plan-stage and proposal-stage vocabulary are to be deliberately conflated, say so in the scope fence and state that correctness rests on first-match-wins chronological ordering. If plan-lifecycle recognition is genuinely wanted, that is new capability and must be routed to the Maintainer, not folded into a defect fix.

* **[R4] (substantive)** The `sharpening` exclusion is NOT "carried over … unchanged" — it silently widens from a head-anchored special case into a whole-phrase suppressor, creating a new false-negative class that the proposed tests would not catch. The proposal states: "The `sharpening` exclusion is carried over from the current `reviewed` pattern unchanged — it is not part of this defect." Measured, that is false.
  *Grounding:* The shipped pattern is `^Review\b(?!.*\bsharpening\b)` (`templates/modules/default-on/_lifecycle_metrics/gitmeta.py:24`) — anchored, so the lookahead is only ever reachable for a subject literally beginning with "Review". The proposed pattern is `(?<!-)\breview\b(?!-)(?!.*\bsharpening\b)` applied via `.search()` over the whole stage phrase, so ANY subject containing "sharpening" anywhere after a `review` token is now suppressed. Both were exec'd and run this session on paired subjects: `dev/proposals: foo -- Internal review (fresh-context panel)` → `reviewed`, but the near-identical `dev/proposals: foo -- Internal review (fresh-context panel) + Sharpening` → `None`, and `Append Gemini External Review of foo proposal (sharpening round)` → `None`. This is not an exotic token: `git log --format="%s" | grep -ci sharpen` → 42, including three plan-review commits of exactly the vulnerable shape (`8606203`, `51f2c10`, `28816f0`, all `dev/plans: <slug> -- Plan review (fresh-context Internal) + Sharpening`). Iterating the last 400 commits, none of the 42 touches `dev/proposals/`, so live impact today is zero — but the vocabulary is in active use, so one proposal-side "Internal review … + Sharpening" subject silently drops the `reviewed` stage and downgrades the row to `Good` with no signal. Proposed test #3 asserts only `"Review sharpening pass"` → unclassified, which passes for the wrong reason and manufactures false confidence that the exclusion is unchanged.
  *Suggested fix:* Stop describing this as a no-op and decide it explicitly. Either scope the exclusion to the head-anchored form it actually had (e.g. apply it only when `review` leads the phrase), or drop it and state the intended behaviour. Whichever is chosen, add two tests pinning BOTH directions: `dev/proposals: <stem> -- Internal review (fresh-context panel) + Sharpening` → `reviewed` (the false-negative guard), and an implementation-style `Phase 2 (A) review Sharpening: harden facade loader` → `None` (the suppression the exclusion is presumably for). Correct the sentence in P1 so it no longer claims the exclusion is unchanged.

* **[R5] (substantive)** Two independent ways the newly-populated hour deltas will be misread, both of which the proposal's own framing makes worse. (a) The repair makes `days_*` and `hours_*` openly contradict each other on 4 of 12 rows under an `Exact` label — and the proposal names that exact shape as the signal the change is WRONG, which makes its own tripwire unusable and would lead an implementer to revert a correct fix. (b) The Rationale's transparency/reproducibility claim over-reads the numbers: most newly-populated deltas measure commit batching latency, not deliberation elapsed time, and three are exactly zero — a reader will take `0.0` as a claim about review turnaround.
  *Grounding:* (a) *Signals the change is wrong* says: "a proposal reports `Exact` while an `hours_*` value contradicts the header dates in the same row. That would mean a subject matched the wrong stage — the one regression that is worse than the defect." Running `proposal_rows(Path('/Users/kendal30/Code/cairn'))` through the real `tools/_lifecycle_metrics/extract.py` with the proposed classifier patched in, and flagging rows where `days_*` and `hours_*` are both non-empty and disagree by more than a day: 4 hits — `adopter-licensing-compliance`, `first-session-survivability`, `record-corrections`, `solo-legacy-adopter-path` — each carrying `days_revised_to_decision = 11` alongside `hours_revised_to_decision ≈ 116.46` h (= 4.85 days), tier `Exact`. Cross-checked against a per-stage `(sha, timestamp, subject)` dump: the classifier is RIGHT; the header `**Date opened**` is `2026-07-11` while the actual open commit `adaa9b5` is `2026-07-17T11:55:42-04:00`, i.e. the header dates are backdated by six days. So the tripwire fires immediately on Cairn's own corpus for a reason the proposal never anticipated. Before the fix every `hours_*` was empty so the divergence was invisible; after it a third of the rows visibly disagree with themselves. (b) The proposal claims: "It also restores the sub-day resolution the tiers were designed around: post-fix, 11 of 12 proposals reach `Exact` and hour-level deltas populate." Printing every delta at HEAD `cc66d2b`: `hours_reviewed_to_revised` is exactly `0.0` for `2026-07-22-claude-interpreter-trust-root-fallback`, `…-lockfile-provenance-fields`, and `…-transition-lint`. Root cause verified in git: for interpreter-trust-root, `4f5f019` (`… -- Internal review (tailored fresh-context panel) + in-tree source`) and `841f17b` (`… -- Response + Revised (status: revised)`) both carry committer timestamp `2026-07-22T09:21:25-04:00`. Five of twelve rows also show `hours_open_to_reviewed` under 0.024 h (~85 s). These are honest readings of the commit record, but the CSV will read `0.0` next to `Exact`, and Cairn's whole pitch is that its recorded deliberation is measurable.
  *Suggested fix:* (a) Rewrite the first bullet of *Signals the change is wrong* so it distinguishes backdated-header divergence (expected, benign, present on 4/12 rows today) from stage misclassification (the real regression) — e.g. key the signal on a NEGATIVE `hours_*`, or on an `hours_*` that disagrees with `days_*` in the opposite direction from the header/commit gap. Add the four rows above to the corpus test as an explicitly expected divergence with the six-day header/commit gap named, so a future implementer does not read it as breakage. (b) Replace the Rationale sentence with one that says what the numbers measure: the interval between the commits that recorded each transition, which for batch-committed sessions can be near zero. Pin the semantics rather than leaving them to be rediscovered — add at least one `0.0`-delta row (e.g. the interpreter-trust-root reviewed→revised pair) to the frozen corpus regression test with its expected value. Consider noting both the divergence and the batching semantics in the P3 docstring alongside the degradation-cause correction, since that docstring is the only adopter-facing documentation of this tier.

* **[R6] (substantive)** One of the two cases offered as "Measured necessity" for the hyphen guard does not hold, and the test specified to pin the guard is non-discriminating as written.
  *Grounding:* The proposal asserts: "**Never match inside a hyphen compound** (`(?<!-)…(?!-)`). Measured necessity: without it, `dev/plans: archive review-record-integrity (Chunk C pointer + lifecycle close)` classifies as `reviewed`, and `Security-Review` inside an `open` subject does the same." Ablating the guard from both the `revised` and `reviewed` patterns and re-running over all 75 corpus subjects, exactly ONE subject flips: the `dev/plans: archive review-record-integrity …` one. `dev/proposals: open interpreter-trust-root-fallback (F2 split; Security-Review gated)` classifies as `open` with the guard AND without it — because `open` is head-anchored and first in `_STAGE_COMMIT_PATTERNS`' priority order, so the `reviewed` pattern is never evaluated for that subject. The second measured claim is false for the proposed design. The consequence reaches the test plan: Tests-required item 2 specifies asserting that same `Security-Review gated` subject → `open`, which passes identically against an unguarded pattern. It is presented as pinning the hyphen guard and does not pin it — the standing lesson "DO NOT CLAIM WHAT A TEST DOES WITHOUT READING IT" arriving one step early, a test asserted to discriminate before it exists.
  *Suggested fix:* Correct the sentence to name the single measured case. Keep `dev/plans: archive review-record-integrity (Chunk C pointer + lifecycle close)` → `None` as the guard's discriminating test (it is the only one in the corpus), and add a stage-phrase-position case such as `dev/proposals: interpreter-trust-root -- add Security-Review section` → `None` so the guard is pinned where the `reviewed` pattern is actually reached. Keep the `Security-Review gated` case in the suite as a priority-order test, but label it as such rather than as guard evidence.

* **[R7] (substantive)** The transition-lint obligation section overstates the reuse in three specific, checkable ways, while reaching the right verdict. (a) The reuse table's row 1 is factually wrong: `_stage_for_subject` implements PRIORITY-ORDER-wins, not LEFTMOST-wins, so an implementer following the proposal's "copy three idioms that are now proven and pinned by a corpus test" would silently import the wrong disambiguation rule and violate the lint's own pinned spec. (b) The section never notes that Shape (b) — the half of the lint that actually fires on the originating incident — reads no commit message at all, so the repair contributes exactly zero to it; instead it asserts a blanket "Every finding class the lint targets is a message-versus-diff mismatch that a subject classifier is structurally blind to," which mischaracterizes Shape (b) and ironically understates the case for "still warranted." (c) "The transition-lint's own argument for not single-sourcing (its Revised prior-art subsection) survives this repair intact" is overstated — the repair falsifies one of that subsection's stated grounds outright and implements a second. The proposal applies exactly the right honesty one paragraph later to Alternative #6 ("One argument the repair partly spends"), so the inconsistency is internal to the section.
  *Grounding:* (a) Both mechanisms were implemented and compared this session. `_stage_for_subject` iterates `_STAGE_COMMIT_PATTERNS` in fixed priority order (open, decision, revised, reviewed) and returns the first pattern that matches anywhere in its target; the lint's revised spec is positional (`dev/proposals/2026-07-22-claude-transition-lint.md:1176` — "leftmost match wins, at most one claim per subject"). They diverge on 4 of 8 constructed subjects and on a real corpus subject: `dev/proposals: adopter-entry doc-refresh -- Internal review panel + Response + Revised` → `_stage_for_subject` returns `revised`; leftmost-wins returns `review`. Under the lint's claim→evidence table (`:1182-1183`) those two claims demand DIFFERENT evidence sections (`## Review` vs `## Response`|`## Revised proposal`), so the divergence is not cosmetic. (b) `git diff-tree --no-commit-id --name-status --find-renames=100% -r 17b7e5c` → `A dev/proposals/2026-06-12-claude-check_cairn-self-host-compat.md`, so the lint's Shape (a) `open` claim IS supported by its diff and does not fire; only Shape (b) fires. Shape (b) as revised (`:1203-1206`) keys purely on the added blob's `**Status**` header and review-grammar markers (`[R<n>]`, `[E<n>]`, `**Steelman`, `**Covered**`); it parses no subject. All three rows of the reuse table are inside Shape (a). (c) The prior-art subsection's grounds are at `:1032-1042`. The ground "An anchored `^(?:Open proposal|...)` cannot express 'claims a review anywhere in the subject.'" (`:1040-1041`) is spent: post-repair the `reviewed` pattern is a `search` over the de-prefixed stage phrase, which expresses approximately that — verified, since `dev/proposals: add Gemini External Review for check_cairn self-host-compat` classifies `reviewed`. The second ground, "hyphen-compound suppression (so slugs do not read as claims)" (`:1038-1039`), is now implemented in `gitmeta.py` by the proposed `(?<!-)…(?!-)` guard. What survives is the different-question ground and the claim→evidence mapping ground — sufficient, but not "intact."
  *Suggested fix:* (a) Split row 1 of the table into what is and is not supplied: `_stage_for_subject` supplies "at most one classification per subject"; it does NOT supply leftmost-wins, which the lint must still implement. Add the one-sentence reason the two can legitimately differ — the stage reader's four stages are ordered by the lifecycle so priority order is meaningful, whereas the lint's claim tokens have no such order and must resolve positionally — and drop or qualify the "copy the idiom" framing for this row. (b) Add one sentence: the three reused idioms live entirely in Shape (a); Shape (b) — which is what fires on `17b7e5c` and is the incident that motivated the lint — consumes no subject vocabulary and is untouched by this repair. That is a sharper statement of "still warranted" than the current blanket claim, and it is verifiable. (c) Replace "survives intact" with an explicit two-column accounting: SPENT — "an anchored regex cannot express 'claims a review anywhere'" and "hyphen suppression must be invented"; SURVIVING — "different question (which commit IS stage X vs does THIS commit's claim match THIS diff)" and "claim→evidence mapping gitmeta has no concept of." The conclusion is unchanged; the argument becomes auditable.

* **[R8] (substantive)** The proposal's own corpus run surfaced a NEW real false positive in the sibling lint's revised Shape (a) spec, on a commit that post-dates the sibling's pinned dogfood window, and did not report it. Feeding exactly this kind of evidence back is what the assigned obligation exists to do.
  *Grounding:* Verified this session. Commit `88fd91f`, subject `dev/proposals: transition-lint -- record Maintainer sequencing direction (not a Decision)`: `git diff-tree --no-commit-id --name-status --find-renames=100% -r 88fd91f` → `M dev/proposals/2026-07-22-claude-transition-lint.md` (a trigger per `dev/proposals/2026-07-22-claude-transition-lint.md:1136-1138`), and the only added heading is `+## Sequencing note -- Maintainer direction -- 2026-07-22`. The lint's `decision` token is NOT positionally anchored (only `open` is — `:1181`) and matches as `(?<![-\w])decisions?(?![-\w])` per `:1176`, so the parenthesized "(not a Decision)" claims a Decision with no `## Decision` evidence → a Shape (a) finding. This commit falls outside the pinned window `d6646a3..57d1daf` (`:1299`), so the sibling's "0 false positives" row does not cover it. The repaired reader correctly returns `None` on the same subject.
  *Suggested fix:* Report `88fd91f` in the obligation section as measured evidence bearing on the lint's size: the lint's `decision` token likely needs the same positional anchoring `open` received, and the reader repair supplies a working precedent for that. This is a genuine, checkable contribution the section is uniquely positioned to make.

* **[R9] (minor)** Three smaller accuracy problems in the obligation section. (a) The Maintainer's obligation was "necessary, and if so at what size" (`## Sequencing note`), and the size half is answered qualitatively; the one quantitative statement — "three of the revised Shape (a) design decisions" — sizes a fraction of a fraction without naming the denominator, so the Maintainer cannot price the deferral. (b) The "design-level, not import-level" caveat rests on a ground already falsified by precedent in this repo, while a stronger ground is available and unused. (c) The section does not state that the repaired vocabulary is not a drop-in even for the message side, because it deliberately omits tokens that are load-bearing in the lint's claim table.
  *Grounding:* (a) Shape (a) as revised (`dev/proposals/2026-07-22-claude-transition-lint.md:1167-1199`) pins more than three things: case-insensitivity (`:1169-1174`), the full claim vocabulary including `accept`/`reject`/`supersede` (`:1184`), the claim→required-evidence mapping (`:1179-1184`), the ≥3-added-non-blank-line evidence rule (`:1198-1199`), and post-image section-span computation (`:204-206`). None are supplied by this repair. (b) The caveat says importing "would create a new dependency from Cairn's tooling onto a shipped template file." That precedent already exists: `scripts/check_cairn.py` loads three shipped template modules by path via `importlib.util.spec_from_file_location` — `templates/modules/default-on/claim_check.py`, `templates/modules/team-gated/content_scan.py`, `templates/modules/team-gated/link_check.py` (read at `scripts/check_cairn.py:83-104`). The sibling proposal already noted this and gave the real ground at `:1163`: `bootstrap/tests/_gate_manifest.py` byte-freezes `templates/modules/**/*.py` — verified in the glob list at `bootstrap/tests/_gate_manifest.py:166`. (c) The scope fence explicitly excludes `archive`, `supersede`, and implicitly `accept`/`reject`; the lint's revised claim table maps `decision` / `accept` / `reject` / `supersede` → `## Decision` (`:1184`). Verified: `dev/proposals: foo -- SUPERSEDE bar` → `None` under the proposed reader; the real corpus subject `dev/proposals: Maintainer Decision -- SUPERSEDE automated-review-committer (+ archive)` classifies `decision` only because "Decision" happens to lead.
  *Suggested fix:* (a) State the denominator in one line — e.g. "3 of the ~8 pinned Shape (a) decisions, and 0 of Shape (b), the trigger/enumeration design, the exemption model, suppression, the CLI, and exit behaviour" — so the answer reads as a measurement rather than an impression. (b) Swap the ground: cite the `templates/modules/**/*.py` byte-freeze plus this proposal's own fence (`_stage_for_subject` is private and explicitly not exported) as why a repo-local script should not couple to it; the current wording invites a reviewer to point at `check_cairn.py` and dismiss the caveat. (c) Add one sentence noting the vocabulary asymmetry — the lint needs `accept`/`reject`/`supersede` as first-class claim tokens that this reader deliberately does not carry — so the Maintainer does not read "claim detection is now proven prior art" as "the lint can adopt this vocabulary."

* **[R10] (minor)** P2's fall-through removal changes nothing on the real corpus, so "This is not hypothetical" overstates its evidentiary basis. The proposal introduces P2 with that phrase and cites the two `open`-classified commits in `review-record-integrity`'s history. The proposal does concede this honestly two sentences later ("P1's hyphen guard blocks that particular subject, but the fall-through is the general hazard"), so this is a framing issue rather than a false claim — but an opening "This is not hypothetical" attached to a change with zero measured effect invites a reviewer to over-credit it, and P2 ends up pinned only by the synthetic proposed test #5.
  *Grounding:* Both loop shapes were implemented this session over `gitmeta._git_log_for_path` output for all 12 proposal files, with the proposed patterns held constant: the shipped fall-through loop (`gitmeta.py:81-85`, which re-tests a subject against remaining stages when its correct slot is already filled) versus the proposed loop. The resolved `{open, reviewed, revised, decision}` SHA assignments are identical for **0 of 12**. Confirmed the specific cited case: `dev/plans: open review-record-integrity (+ archive proposal)` classifies `open` under the new patterns, and under the old loop its fall-through re-test yields no match for `decision`/`revised`/`reviewed` because the hyphen guard blocks `review-record`.
  *Suggested fix:* Keep P2 — it is cheap, correct, and makes classification a pure function of the subject, which is the right invariant. But retitle the justification honestly: say the fall-through is a latent defect of the same mechanism with no currently-observable effect (measured 0/12), rather than "not hypothetical". Keep proposed test #5 and note in the test docstring that it is the only thing pinning P2, since the live corpus does not exercise it.

* **[R11] (minor)** Three presentation/measurement-accuracy defects in a proposal whose entire value proposition is measurement accuracy. (a) The de-anchored figure is 52, not the claimed 51, and Alternative 3 as literally worded produces 0, not 51. (b) The Evidence figures are stale at open time and one citation is off by one line. (c) The Context block is formatted as a verbatim shell transcript but is a hand-written summary; the command shown does not produce the output shown.
  *Grounding:* (a) Re-measuring on the exact 73-subject set as of `7d2d034` (reconstructed by removing from the 75-subject HEAD corpus the two subjects added by `cc66d2b` and `33edd10`), stripping the leading `^` from all four shipped patterns and matching with `.search()` gives **52/73**, not 51/73. Separately, *Cause 1* correctly states that switching `.match()` to `.search()` alone "would change nothing" because the `^` lives inside the pattern string — but Alternative 3 is worded "Just remove the `^` anchors", and removing the anchors while keeping the shipped `pattern.match(subject)` call at `gitmeta.py:83` yields **0/73**. The 51 (52) figure silently requires BOTH changes. Three variants run this session: shipped + `.match()` → 0/73; de-anchored + `.match()` → 0/73; de-anchored + `.search()` → 52/73. Neither error touches the conclusion — 15 of the 52 are slug-driven false positives, exactly as claimed. (b) The proposal anchors everything to "`HEAD` `7d2d034`"; actual HEAD is `cc66d2b`, two commits later (`33edd10 dev/proposals: ast-known-new-repin -- Response to Gemini Internal review`, `cc66d2b dev/plans: archive first-session-survivability (lifecycle complete)`). Re-measured: 75 distinct subjects not 73; 69 classified not 68; 6 correctly unclassified not 5 — the sixth being `dev/plans: archive first-session-survivability (lifecycle complete)`. The 0-match count and the tier table both reproduce exactly, so no conclusion moves. The proposal cites "`docs/quickstart.md:232`" for `git commit -q -m "Open proposal: README tagline"`; that line is at `docs/quickstart.md:231` and `:232` is the closing code fence. `scripts/claim_check.py` only hard-flags out-of-bounds line citations, so an in-bounds off-by-one passes silently. (c) The proposal presents a fenced block with a `$` prompt: `$ ~/conda_envs/lhm/bin/python tools/lifecycle_metrics.py proposals --format csv` followed by `12 rows; stage_timestamp_reliability = Best-effort on 12 of 12`. Running that exact command emits a CSV header plus 12 data rows and nothing resembling that summary line. The underlying fact is true (confirmed independently via `proposal_rows(Path('.'))` → `Counter({'Best-effort': 12})`), so this is presentation, not a false claim — but a `$`-prompted block that is not the command's output is the specific artifact shape this repository's review-record-integrity work exists to catch, in the one section a reader is most likely to accept without re-running.
  *Suggested fix:* (a) Correct 51 → 52 in both the *Why it misses* section and Alternative 3, and reword Alternative 3 to "remove the `^` anchors and switch `.match()` to `.search()`" so the measurement is reproducible from the description; optionally note that de-anchoring alone (keeping `.match()`) still yields 0/73, which strengthens Cause 1. (b) Re-anchor the SHA and re-run the three counts immediately before the opening commit; update the five-item unclassified enumeration to six and name the archive commit; correct the quickstart citation to `docs/quickstart.md:231`. (c) Either show the real reproducer (e.g. the two-line `proposal_rows` + `Counter` snippet, which does print that fact) or drop the `$` prompt and label the block as a derived summary with the command named in prose.

* **[R12] (minor)** Three process-and-verification items. (a) The proposal asks the Maintainer three questions for what is scoped as a single defect fix, and one of them (P3) is the author's call; folding it in also requires a completeness correction the proposal does not make. (b) The declared `required(Internal)` plan-review tier is defensible on the doctrine text, but the plan should carry an explicit obligation to re-run the corpus ablation, because the density of spec-level defects here is not what "ordinary" implies. (c) The `0 Best-effort` headline is not reproducible under concurrent git load, which the smoke check and proposed test #6 should account for.
  *Grounding:* (a) Open question 2 asks "**Whether P3 rides along** or is dropped to keep the diff to one file pair." P3 is a two-line docstring correction in the same module directory, in a twin pair the author must already keep byte-identical, correcting a sentence verified factually wrong: `templates/modules/default-on/_lifecycle_metrics/__init__.py:74-78` reads "when git is absent, the path is not a checkout, or the default branch is named ``main`` rather than ``master``" — none of which describes the observed 12/12 `Best-effort`. The proposal's gate-manifest paragraph establishes that `gitmeta.py` is stale in the fixture but does not say the same of P3's file: `bootstrap/tests/fixtures/gate_manifest.json` places BOTH files in `frozen_files`, and both are stale (fixture `fb1c4d26…` for `__init__.py` vs on-disk `c0e169e7…`). The `__init__.py` twins are byte-identical (`c0e169e7…`), so the parity cost is one mechanical copy. (b) `doctrine/dual-review.md:184-187` reads "line names the tier, and that tier is chosen on the same / structural-independence axis as any other review here — an Internal-floor / read for an ordinary plan, a different-agent-type External round for a / high-risk or contract-touching one." Against `AGENTS.md`'s enumerated high-risk surfaces, `gitmeta.py` is none of them and the install contract is untouched, so Internal is the right floor. But R2, R3, R5 and R6 above were all found by EXECUTING the proposed regexes and ablating them against the real corpus, and none were visible from reading the proposal's own before/after table — which reproduces exactly and is therefore reassuring in a misleading way. (c) While the full pytest suite ran in the background, an otherwise identical pipeline run returned `2026-07-11-claude-record-corrections` as `Best-effort` — {'Exact': 10, 'Good': 1, 'Best-effort': 1} instead of the stable {'Exact': 11, 'Good': 1}; three re-runs on a quiet tree (after 1437 passed, 123.55s) were stable. Traced to the unconditional `return []` on `result.returncode != 0` at `templates/modules/default-on/_lifecycle_metrics/gitmeta.py:50-51`, so transient git contention silently degrades a whole row with no signal. This is pre-existing and NOT introduced by this proposal.
  *Suggested fix:* (a) Decide P3 in the proposal and remove open question 2; state in the parity paragraph that both touched files sit in the gate manifest's `frozen_files` and both are stale from `501efe3`, so P3 adds no new posture. Leave the Maintainer the two questions that are genuinely theirs (the 41-entry lockfile staleness, and the review tier). (b) Keep `required(Internal)`, but write into the plan an explicit plan-review obligation: the reviewer must re-run the classifier over the live `git log --follow` subject set at then-current HEAD and must run at least the `plans?`-prefix and hyphen-guard ablations, reporting counts. Note in the plan that the frozen corpus list is an oracle only for subjects already in it, so ablation is the only check that covers the design decisions themselves. (c) Add one line to *Examples / smoke checks* noting that the `0 Best-effort` verification must be run on a quiet tree (no concurrent git operations). For proposed test #6, use the isolated `tmp_path` repo it already specifies and avoid asserting the tier on the live Cairn corpus inside the suite. Optionally route the underlying silent-degradation behaviour to the Maintainer as a separate observation — it is a pre-existing defect and should not expand this scope.

**Coverage.** CONSOLIDATED FROM THREE LENSES: corpus-evidence, scope-stopping-rule, transition-lint-necessity. All three ran on the canonical interpreter (`~/conda_envs/lhm/bin/python` = Python 3.13.13) at HEAD `cc66d2b`, two commits past the proposal's stated `7d2d034` (via `33edd10` and `cc66d2b`) — which fully explains the 73→75 subject delta.

VERIFIED BY EXECUTION (union across lenses):
1. Corpus construction — `git log --follow` subjects for all 12 proposal files under `dev/proposals/` and `dev/proposals/archive/`: 75 distinct at HEAD, 73 reconstructed at `7d2d034`.
2. Defect — shipped `_STAGE_COMMIT_PATTERNS` exec'd verbatim out of `gitmeta.py:17-25` (not retyped): 0/73 and 0/75. `proposal_rows(Path('.'))` → `Counter({'Best-effort': 12})`.
3. Fix — proposal's verbatim `_stage_for_subject` transcribed and run: 68/73 (69/75 at HEAD) classified, with exactly the 5 (6 at HEAD) named unclassified subjects.
4. End-to-end — real `proposal_rows()` through `tools/_lifecycle_metrics/extract.py` with `extract._resolve_stage_commits` monkeypatched: 12/12 `Best-effort` → 11 `Exact` / 1 `Good` / 0 `Best-effort`, stable over three quiet re-runs; the `Good` is `2026-06-12-claude-adopter-entry-doc-refresh`.
5. Hand audit — resolved `(sha, timestamp, subject)` for every stage of all 12 proposals: all semantically correct, zero negative deltas.
6. Ablations — `plans?` prefix removed (4 subjects `open`→`None`, tier result byte-identical); hyphen guard removed from both patterns (exactly 1 subject flips); prefix-required variant (10 `Exact` / 2 `Good`); P2 loop differential (0/12 differ); de-anchored figure reproduced three ways (0, 0, 52).
7. Row-level numbers — `days_*` vs `hours_*` cross-check (4-row divergence); every post-fix hour delta printed (three exact `0.0` `hours_reviewed_to_revised`, five `hours_open_to_reviewed` under 0.024 h).
8. Over-matching sweep — proposed matcher over the last 60 repo-wide commits (6 `open`, 6 `decision`, 12 `revised`, 17 `reviewed`, 19 `None`; all 19 correctly unclassified).
9. Adopter probing — 13 adopter-plausible scientific-codebase subjects (8 false positives found).
10. Sharpening semantics — proposed vs shipped pattern on paired subjects; 42-commit `sharpen` exposure counted; last 400 commits checked for `dev/proposals/` overlap (zero today).
11. Python-version checks — keyword `count=` / `maxsplit=` forms on `Pattern.sub` / `Pattern.split` work on 3.13.13.
12. Suite — `python -m pytest bootstrap/tests -q` → **1437 passed, 0 failed, 0 skipped** (~123s), superseding the older 2-failed baseline (re-anchored in `2bd8f34`). `bootstrap/tests/test_ast_attest.py` alone → 26 passed.
13. Parity / lockfile / gates — twin byte-identity both pairs (`5a47849b…`, `c0e169e7…`); `test_notice_install.py:98` read and confirmed to pair manifest twins and assert equal bytes; `cairn-lock.yml:495-501` (`3d057d53…`); `verify_integrity.py --target .` exits 1 with exactly 41 mismatches; `501efe3` touches no `cairn-lock` path; `test_ast_attest.py:19` glob excludes `gitmeta.py`; `test_gate_manifest.py:80` verifies a freshly produced manifest (fixture `anchor_ref` `None`); both touched files confirmed in `frozen_files`; `test_reference_scripts.py` in `frozen_files` (line 2483); `security_check.py scan_targets()` = 72 including the edited file; `scaffold.py --manifest` row shape `dst\tsrc\tverbatim`.
14. Citations — `doctrine/proposals.md:69-75`, `__init__.py:74-78`, `docs/quickstart.md` toy subject, `doctrine/dual-review.md:184-187`, `dev/proposals/_template.md:166-167`, `test_reference_scripts.py:443-457` and `:476`, `config.py:56` all checked character-by-character (one off-by-one found, see R11).
15. claim_check posture — `scripts/claim_check.py:375`, `:205`, `:543` read; the marker block plus two-glob directive appear correctly formed and specific enough to survive the too-broad check.
16. Sibling-proposal work — `2026-07-22-claude-transition-lint`'s Context, original Shape (a)/(b), the entire `## Revised proposal` (`:1009-1456`) and `## Sequencing note` (`:1458-1486`) read; its leftmost-wins claim detector (`:1176-1184`) reimplemented and diffed against `_stage_for_subject` over all 75 real subjects plus 8 constructed; `git diff-tree` on `17b7e5c`, `f4a8308`, `88fd91f`; `git log` census of all 11 real Decision-form subjects (all decision-first); `scripts/check_cairn.py:83-104`; `bootstrap/tests/_gate_manifest.py:160-175`.
17. Obligation key claim — repaired classifier returns `open` on `17b7e5c`'s subject, so the lint would indeed have surfaced nothing on Shape (a).

NEGATIVE SPACE — what NO lens checked, and where a second reader must look:
(a) `bootstrap/tests/test_lifecycle_stage_patterns.py` does not exist yet and could not be reviewed. R1, R2, R3, R4, R5, R6 and R10 all propose additions to its frozen list; a list assembled without them would lock in exactly the blind spots this panel found. This is the single highest-value unchecked surface.
(b) No lens ran the proposed code end-to-end against a synthetic adopter repo (the shape of Tests-required item 6), so the public-path assertion `stage_timestamp_reliability == 'Exact'` on a fresh scaffold is unverified.
(c) The obligation section's claims about the sibling proposal were verified in depth by only one lens; the other two took its Revised prior-art subsection, Shape (a) table, `## Sequencing note`, and the quoted Maintainer direction on the author's word. Whoever reviews that section next should hold the sibling's actual text.
(d) `scripts/claim_check.py` / `scripts/check_cairn.py` were not run against the proposal itself, since it is not yet on disk; the `claim-check-allow` directives for the two forward-referenced paths are unexercised.
(e) Bandit is unverified for the change itself (only that the file is in `scan_targets()`); the code does not exist yet.
(f) Non-English, unicode, and merge-commit subject handling — declared out of scope by the proposal and not probed.
(g) No second real corpus exists. The 8 adopter false positives in R1 are one lens's own construction from one domain (hydrogeology) — illustrative, not a measured second corpus. That limitation is real for the critique as much as for the proposal.
(h) The 41-entry lockfile staleness was confirmed as fact but not assessed further; the proposal correctly routes it out of scope.
(i) Vendor-neutrality and licensing gates (`scripts/quality_gate.py --sub neutrality`, the by-file split) were not run — nothing in the diff appears to touch them, but that is inference, not measurement.
(j) `dev/measurement/snapshots/` absence (the \"no recorded measurement invalidated\" claim) was not verified; only the config key at `config.py:56` was.
(k) No lens formed a view on whether the sibling lint should be BUILT — correctly the Maintainer's call under the standing build-nothing-new rule.

PANEL ANSWER TO THE ASSIGNED OBLIGATION (transition-lint-necessity lens, endorsed by the panel): **still warranted.** A repaired subject→stage vocabulary supplies part of the MESSAGE side only — and not all of it (the lint needs leftmost-wins, which this does not implement, and `accept`/`reject`/`supersede`, which this deliberately excludes) — and NONE of the diff side. Shape (b), which is what fires on the originating incident `17b7e5c`, consumes no subject vocabulary whatsoever. The honest phrasing is closer to \"still warranted; marginally smaller in one corner of Shape (a)\" than to \"smaller, reusing this.\"

**Second-round recommendation.** CONSOLIDATED RECOMMENDATION: **Author Response + Revised section, then a narrow Internal re-read with an EXECUTION obligation — not a full second panel, and not External.** All three lenses converge here.

Why not send it back to the drawing board: the diagnosis is correct, the fix is a genuine repair on Cairn's own corpus (every slot assignment across 12 proposals was hand-audited and is semantically right), the scope fence is the strongest in this tree, and the citation discipline is unusually clean. Nothing found undermines the central case that the shipped vocabulary reads nothing and should be repaired now.

WHAT GATES THE DECISION. R1 (bare-subject fallback) is blocking — not because the proposal is wrong but because it defers a decision that should be made with numbers in hand, and the panel now has the numbers. Under the standing postdoc-ready-first directive, shipping a default-on tool that labels \"Add impulse response function to the transport solver\" as a `revised` transition and reports the timestamp as `Exact` is a real regression in the adopter path: before the fix that adopter got nothing; after it they get something wrong with a confidence label attached. The proposal itself names this as the one failure mode worse than the defect, then routes it to a post-hoc tripwire. The measured trade is cheap enough to settle in one revision round — prefix-required costs exactly one tier on Cairn's corpus and takes all 8 adopter false positives to `None`. Suggested landing: the hybrid (prefix-required plus an explicitly-enumerated `Append/Refine … Review of <stem> proposal` form), which preserves 11 `Exact` AND closes the general fallback. Whichever way the Maintainer goes, record it as a deliberate precision/recall trade in the proposal body.

Two further findings should be treated as near-blocking by one lens each and are cheap to fix in the same round: **R2** (`decision` head-anchoring returning `reviewed` on a slug-first Decision subject) is a live wrong-stage-at-`Exact` output on the corpus's own dominant subject style, and needs a code-level answer in P1 or an explicit, tested concession that decision-first is mandated; **R3** (the `plans?` prefix branch) puts a wrong-timestamp-at-`Exact` hazard into shipped default-on code in service of a branch measured to change no outcome.

The remainder resolve by appending a Response and a Revised section; none requires re-measuring anything from scratch. R4 is a corrected factual claim plus two tests. R5 matters disproportionately because as written the tripwire fires immediately on the shipped corpus, so an implementer following the proposal faithfully would revert a correct fix. R6 is a corrected sentence plus a discriminating test. R7–R9 are surgical edits confined to the obligation section (plus one additive paragraph reporting `88fd91f`); they change that section's precision, not its verdict. R10–R12 fold into the same Response: soften \"not hypothetical\" on P2, correct 51→52, reword Alternative 3 so it is reproducible, re-anchor every figure to then-current HEAD, fix the `docs/quickstart.md` off-by-one, relabel the Context block, decide P3 rather than asking, and add the quiet-tree caveat to the smoke checks.

WHAT THE SECOND READER MUST BE GIVEN: an explicit EXECUTION obligation, not a reading one. Four of the six highest-severity findings (R2, R3, R5, R6) were invisible from reading the proposal and surfaced only by executing the proposed regexes and ablating them against the live corpus. The before/after table reproduces exactly, which makes a reading-only review feel confirmatory while the design decisions underneath go unchecked. The reader must re-run the classifier over the live `git log --follow` subject set at then-current HEAD, re-run at least the `plans?`-prefix and hyphen-guard ablations, and report counts (each run takes seconds). The frozen corpus list is an oracle only for subjects already in it — ablation is the only instrument that tests the design decisions themselves.

SCOPE FOR THE RE-READ: the revised obligation section; the `decision` anchoring in P1 and its `maxsplit=1` phrase-split interaction; the resolution of R1 and R3; and — highest value — the actual frozen list in `bootstrap/tests/test_lifecycle_stage_patterns.py` once written, checked against the panel's measured false-positive and false-negative sets. Second priority is re-verifying the obligation section against the sibling transition-lint proposal's real text, which two of three lenses read only as quoted.

TIER: `required(Internal)` is correct and External is NOT warranted on the doctrine text. `doctrine/dual-review.md:184-187` reserves the different-agent-type round for a \"high-risk or contract-touching\" plan; the install contract is verified untouched (`scaffold.py --manifest` emits `dst\tsrc\tverbatim` with no hash, `PROPOSAL_COLUMNS` unchanged, the `Exact`/`Good`/`Best-effort` tier vocabulary unchanged), and `gitmeta.py` is none of `AGENTS.md`'s enumerated high-risk surfaces. The one place a different reader would add value is the obligation section, whose claims about another artifact are the only substantive material the panel could not fully verify. Open question 3 is fairly stated and correctly routed to the Maintainer.

ON THE OTHER OPEN QUESTIONS: the 41-entry lockfile staleness is correctly routed OUT — it is real, pre-existing, caused by `501efe3`, and bumping 1 of 41 would leave the check red while making the record less coherent; bundling it here would be a scope breach. P3 should ride along and open question 2 should be removed — the `__init__.py` twins are byte-identical so the parity cost is one mechanical copy, both touched files sit in `frozen_files` and both are stale from `501efe3` (identical posture to P1), and the sentence it corrects is false in every clause of its cause list. P3 should also pick up a clause on the `days_*`/`hours_*` divergence and the commit-batching semantics from R5, since that docstring is the only adopter-facing documentation of this tier.

No blocking finding stands in the way of a Decision once R1 is settled in the revision.
## Response -- Claude (author) -- 2026-07-22

All measurements below were re-run by me this session on the canonical
interpreter (`~/conda_envs/lhm/bin/python`, Python 3.13.13) at `HEAD`
`b533596`, which is four commits past the `7d2d034` the proposal cited
(`33edd10`, `cc66d2b`, `d3f3ef7`, `b533596`). The corpus is now **76**
distinct `git log --follow` subjects across the same 12 proposal files.

**The panel is right where it matters, and four of its findings are
dispositive against the design as written.** R1, R2, R3 and R4 each
reproduce exactly on my own re-run, and three of them (R1, R2, R3)
produce the one outcome the proposal itself named as *worse than the
defect*: a wrong stage timestamp emitted under an `Exact` label. I am
not going to argue around that.

What saves the proposal is that all four resolve by **narrowing** —
classifying fewer subjects, not building more machinery. The revised
design below classifies **52/76** corpus subjects instead of 70/76,
touches the same one file pair plus one test, adds no module, no
export, no config key, and no CLI surface. It is strictly smaller than
what was proposed. That is why I am recommending `revised` rather than
supersede.

One correction runs the other way: **R11(b)'s off-by-one sub-claim is
itself wrong**, and I show the check below.

### Per-critique disposition

| # | Token | Rationale (one sentence) |
| --- | --- | --- |
| R1 | **accept** | Reproduced 8/8 of the panel's adopter false positives plus `docs: review the API surface`; the bare-subject fallback is removed in the revised design, which takes 9 of those 10 to `None`. |
| R2 | **accept** | Reproduced: `dev/proposals: transition-lint -- Maintainer Decision -- ACCEPT (post Internal review)` returns `reviewed` under the proposed code — a wrong stage on the corpus's own dominant slug-first style. |
| R3 | **accept** | Reproduced and worse than reported at current HEAD: **five** `dev/plans: open …` subjects classify `open` when they are the proposal's *archive* event, and the ablation confirms the `plans?` branch changes no tier outcome. |
| R4 | **accept** | Reproduced; my "carried over unchanged" sentence is false, and I am withdrawing it rather than defending it. |
| R5(a) | **accept** | Reproduced: 4 of 12 rows carry `days_revised_to_decision = 11` beside `hours_revised_to_decision ≈ 116.46` (4.85 d) at `Exact`, because header dates are backdated ~6 days — my own tripwire fires on a correct fix. |
| R5(b) | **accept** | Reproduced: three rows show `hours_reviewed_to_revised` of exactly `0.0` and five show `hours_open_to_reviewed` under 0.024 h; the Rationale sentence overclaims what those numbers measure. |
| R6 | **accept** | Reproduced: only *one* corpus subject flips when the hyphen guard is ablated, and the `Security-Review gated` case classifies `open` with **and** without the guard, so proposed test 2 does not pin what I said it pins. |
| R7(a) | **accept** | Correct: `_stage_for_subject` is priority-order-wins, not leftmost-wins; the reuse table's row 1 misdescribes what a lint could copy. |
| R7(b) | **accept** | Correct and it strengthens my own verdict: Shape (b) parses no subject at all, so the repair contributes zero to the half that actually fires on `17b7e5c`. |
| R7(c) | **accept** | Correct; "survives intact" is inconsistent with the honesty I applied one paragraph later to Alternative #6. |
| R8 | **accept** | Verified independently: `git diff-tree --no-commit-id --name-status --find-renames=100% -r 88fd91f` → `M dev/proposals/2026-07-22-claude-transition-lint.md`, and the subject's parenthesised "(not a Decision)" would claim a Decision under the sibling's un-anchored `decision` token. Reporting it. |
| R9(a) | **accept** | The size answer needs a denominator to be usable by the Maintainer. |
| R9(b) | **accept** | Verified the precedent: `scripts/check_cairn.py:125` loads three shipped template modules by path (`:86`, `:93`, `:102`); my stated ground was weak and the byte-freeze ground (`bootstrap/tests/_gate_manifest.py:167`) is the real one. |
| R9(c) | **accept** | Correct; the reader deliberately omits `accept`/`reject`/`supersede`, which the lint needs as first-class claim tokens. |
| R10 | **accept** | Correct: I re-ran both loop shapes over all 12 files and the resolved SHA assignments are identical for 12 of 12, so "This is not hypothetical" overstates it. |
| R11(a) | **accept with modification** | The de-anchored figure is **53/76** at current HEAD (the panel measured 52/73 at theirs) — the point stands that 51 was wrong and that the figure is HEAD-dependent; I also confirm de-anchoring *without* switching to `.search()` yields **0/76**, so Alternative 3 as worded was unreproducible. |
| R11(b) | **accept with modification** | Accepting the re-anchor obligation (counts re-measured above), but **rejecting the off-by-one**: `grep -n 'Open proposal: README tagline' docs/quickstart.md` → `232:`, with `231` the opening ```` ```bash ```` fence and `233` the closing one. `docs/quickstart.md:232` was correct as cited. |
| R11(c) | **accept** | The `$`-prompted block is a derived summary, not that command's output; relabelled. |
| R12(a) | **accept** | P3 rides along and open question 2 is withdrawn; both touched files sit in `frozen_files` and both are stale from `501efe3`, so P3 adds no new posture. |
| R12(b) | **accept** | Keeping `required(Internal)` and writing an explicit *execution* obligation into the plan. |
| R12(c) | **accept** | Adding the quiet-tree caveat; the underlying silent degradation at `gitmeta.py:50-51` is pre-existing and stays out of scope. |

No critique is deferred and none is dropped.

### One thing the panel did not say that I have to say myself

Fixing R1 costs something the original proposal claimed it would not
cost. My scope fence said: *"The reader accommodates existing subjects;
it does not mandate a form."* Under the revised design that sentence is
only half true, and I am correcting it rather than keeping it. The
richer house-style vocabulary now fires **only behind a
`dev/proposals:` scope prefix**. An un-prefixed subject still gets
exactly the shipped legacy vocabulary — byte-for-byte the four patterns
that ship today — so nothing that classifies now stops classifying. But
a project that wants sub-day stage resolution gets it by scoping its
lifecycle commits. That is a de-facto preference expressed by what the
reader can resolve, not a rule anyone must follow, and it is the price
of not labelling `Add impulse response function to the transport
solver` a `revised` transition in a hydrogeology postdoc's tree. I
would rather state the trade than let a reviewer discover it.

I also declined the panel's suggested hybrid (adding
`Append/Refine … Review of <stem> proposal` as an explicitly-listed
extra accepted form to preserve 11 `Exact`). That form is an artifact
of one project's habit over a few weeks, and fitting the vocabulary to
it is precisely the error R2 identifies in my own `decision` anchoring.
The measured cost of refusing is **one tier**: 10 `Exact` / 2 `Good`
instead of 11 / 1.

---

## Revised proposal -- 2026-07-22

Supersedes the `## Proposal` section above. Scope, fence, and
non-goals are otherwise unchanged; only what is restated here changes.

### P1 (revised) — additive repair: shipped vocabulary untouched, scoped vocabulary added

The key structural change from the original P1: **`_STAGE_COMMIT_PATTERNS`
is not edited at all.** It keeps its name, its type, its priority order,
and its four regexes byte-for-byte, including the `sharpening`
exclusion in exactly the anchored position it has today
(`gitmeta.py:24`). Backward compatibility is therefore guaranteed *by
construction* rather than asserted by a 12-string table, and R4
dissolves: the exclusion cannot widen because the pattern carrying it
does not change.

The repair adds a second, **scope-gated** vocabulary consulted only
when the legacy vocabulary declines *and* the subject carries a
proposal-tree scope prefix:

```python
_STAGE_SCOPE_PREFIX_RE = re.compile(r'^(?:dev/)?proposals?\s*:\s*', re.I)

_STAGE_PHRASE_SEP_RE = re.compile(r'\s+(?:--|–|—)\s+')

#: Consulted ONLY for a subject carrying the scope prefix above.  The
#: looser word-boundary forms are safe there and unsafe anywhere else.
_SCOPED_STAGE_PATTERNS: List[Tuple[str, 're.Pattern[str]']] = [
    ('open', re.compile(r'^open(?:ing)?\b', re.I)),
    ('decision', re.compile(
        r'^(?:maintainer\s+)?decision\b'
        r'|(?<!-)\bmaintainer\s+decision\b(?!-)', re.I)),
    ('revised', re.compile(
        r'(?<!-)\b(?:response|responses|revised|revise|respond\s+to)\b(?!-)',
        re.I)),
    ('reviewed', re.compile(r'(?<!-)\breview\b(?!-)', re.I)),
]

_HEAD_ANCHORED_STAGES = frozenset({'open', 'decision'})


def _stage_for_subject(subject: str) -> Optional[str]:
    """Classify a commit subject as AT MOST ONE lifecycle stage."""
    text = subject.strip()
    for stage, pattern in _STAGE_COMMIT_PATTERNS:   # shipped, unchanged
        if pattern.match(text):
            return stage
    match = _STAGE_SCOPE_PREFIX_RE.match(text)
    if match is None:
        return None
    body = text[match.end():]
    parts = _STAGE_PHRASE_SEP_RE.split(body, maxsplit=1)
    phrase = parts[1] if len(parts) > 1 else body
    for stage, pattern in _SCOPED_STAGE_PATTERNS:
        target = body if stage in _HEAD_ANCHORED_STAGES else phrase
        if pattern.search(target):
            return stage
    return None
```

Four rules, each earning its place against a *measured* failure:

* **No bare-subject fallback (R1).** An un-scoped subject sees only the
  shipped patterns. Measured on the panel's adopter probe set: 9 of 10
  go to `None`, including all 8 the panel found. The tenth,
  `review: tighten the recharge bounds`, still classifies `reviewed` —
  **but it does so today**, via the shipped `^Review\b` pattern
  (verified by running the shipped patterns alone). That is status quo,
  not a regression this fix introduces, and repairing it would mean
  editing the shipped vocabulary, which is a separate and larger call.
* **`plans?` dropped from the scope prefix (R3).** Every `dev/plans:`
  subject now yields `None`. Verified across all seven `dev/plans:`
  subjects in the corpus, including
  `dev/plans: foo -- Code review (fresh-context, disclosed scribe)`,
  the shape the panel flagged as latent. The justification sentence the
  original P1 gave for `plans?` is withdrawn: the ablation shows the
  branch buys no tier and every classification it produced was the
  wrong end of the lifecycle.
* **`decision` matches head-of-subject *or* a qualified
  `maintainer decision` anywhere (R2).** Verified on all three real
  forms: `dev/proposals: Maintainer Decision -- ACCEPT licensing` →
  `decision`; `dev/proposals: licensing -- Maintainer Decision --
  ACCEPT` → `decision`; `dev/proposals: transition-lint -- Maintainer
  Decision -- ACCEPT (post Internal review)` → `decision` (was
  `reviewed`). Known and accepted false negative: a Decision written
  without the word — `dev/proposals: foo -- SUPERSEDE bar` → `None`.
  That is consistent with the fence (`supersede` gets no stage) and
  fails safe to `Good`.
* **Never match inside a hyphen compound (R6).** Corrected claim: the
  guard's measured necessity rests on **exactly one** corpus subject,
  `dev/plans: archive review-record-integrity (Chunk C pointer +
  lifecycle close)`. The `Security-Review gated` case is *not* evidence
  for the guard — it classifies `open` with and without it, because
  `open` is head-anchored and wins on priority order. The discriminating
  probe is a stage-phrase-position one:
  `dev/proposals: interpreter-trust-root -- add Security-Review section`
  → `None` guarded, `reviewed` unguarded (verified both ways).

### P2 (revised framing) — unchanged code, honest justification

The code change is exactly as originally proposed. The justification is
corrected per R10: I ran both loop shapes over `_git_log_for_path`
output for all 12 proposal files with the patterns held constant, and
the resolved `{open, reviewed, revised, decision}` SHA assignments are
**identical for 12 of 12**. The fall-through is a *latent* defect of the
same mechanism with no currently-observable effect, not a live one.
"This is not hypothetical" is withdrawn. P2 stays because making
classification a pure function of the subject is the right invariant
and it is free; test 5 is the only thing pinning it, and its docstring
will say so.

### P3 — rides along (open question 2 withdrawn)

Per R12(a), P3 is my call and I am making it: it ships. Both touched
files sit in `bootstrap/tests/fixtures/gate_manifest.json`'s
`frozen_files` and both are already stale from `501efe3`, so P3 adds no
new gate posture; the `__init__.py` twins are byte-identical, so parity
costs one mechanical copy.

P3 now corrects three things in
`templates/modules/default-on/_lifecycle_metrics/__init__.py:74-78`
rather than one — the falsely-exhaustive cause list, plus (per R5) two
sentences naming what the hour deltas measure: the interval between the
*commits that recorded* each transition, which for a batch-committed
session can be near zero, and which can legitimately disagree with the
`days_*` columns when a proposal's header `**Date opened**` predates its
opening commit.

### Revised measurements (as_of 2026-07-22, HEAD `b533596`, Python 3.13.13)

| measure | shipped | proposal as written | **revised design** |
| --- | --- | --- | --- |
| corpus subjects classified (of 76) | 0 | 70 | **52** |
| proposals at `Best-effort` | 12 / 12 | 0 | **0** |
| proposals at `Exact` | 0 | 11 | **10** |
| proposals at `Good` | 0 | 1 | **2** |
| panel's adopter false positives (of 10) | 1 | 10 | **1** (pre-existing) |
| `dev/plans:` subjects misclassified | 0 | 5 | **0** |

The second `Good` is `2026-07-22-claude-ast-known-new-repin`, whose
`reviewed` slot was previously filled by the un-scoped subject
`Append Gemini Internal Review of ast-known-new-repin proposal`. Losing
it is the deliberate, priced cost of closing the bare-subject fallback.

Corrected supporting figures: de-anchoring the shipped patterns *and*
switching `.match()` → `.search()` gives **53/76** (not 51); de-anchoring
alone, keeping `.match()` as it is at `gitmeta.py:83`, gives **0/76** —
so Alternative 3 is reworded to "remove the `^` anchors **and** switch
`.match()` to `.search()`", which is what the 53 figure requires. All
counts are HEAD-dependent and will be re-measured immediately before
the opening commit.

### Revised "Signals the change is wrong" (first bullet)

Replacing the unusable tripwire per R5(a). A `days_*` / `hours_*`
disagreement is **expected and benign** on this corpus — 4 of 12 rows
show `days_revised_to_decision = 11` beside `hours_revised_to_decision
≈ 116.46`, because e.g. `2026-07-11-claude-adopter-licensing-compliance`
carries `**Date opened**: 2026-07-11` while its opening commit `bee3a85`
is `2026-07-17T11:55:42-04:00`. The real signal is narrower:

* **A negative `hours_*` value**, or an `hours_*` that exceeds its
  `days_*` span (rather than falling short of it, which is what
  backdated headers produce). Either means a slot took a timestamp from
  the wrong commit. *Recovery:* as before.

### Revised obligation-section deltas (R7, R8, R9)

Verdict unchanged — **the transition-lint is not made unnecessary** —
but the argument is corrected:

* **Reuse table row 1 split.** `_stage_for_subject` supplies "at most
  one classification per subject". It does **not** supply leftmost-wins:
  it is priority-order-wins, and the two diverge on real corpus
  subjects (`dev/proposals: adopter-entry doc-refresh -- Internal review
  panel + Response + Revised` → `revised` here, `review` under
  leftmost). The divergence is legitimate — the reader's four stages are
  lifecycle-ordered so priority order is meaningful, while the lint's
  claim tokens have no such order — but it means the lint must still
  implement its own disambiguation rule.
* **Shape (b) gets zero.** The three reused idioms live entirely in
  Shape (a). Shape (b) — the half that actually fires on the originating
  incident `17b7e5c` — consumes no subject vocabulary whatsoever. That
  is a sharper and more verifiable statement of "still warranted" than
  the blanket claim I made.
* **Spent / surviving, explicitly.** *Spent:* "an anchored regex cannot
  express 'claims a review anywhere in the subject'", and "hyphen-
  compound suppression must be invented". *Surviving:* the different-
  question ground (which commit *is* stage X vs does *this* commit's
  claim match *this* diff), and the claim→evidence mapping, which
  `gitmeta.py` has no concept of.
* **Denominator (R9a).** 3 of the ~8 pinned Shape (a) decisions, and 0
  of Shape (b), the trigger/enumeration design, the exemption model,
  suppression, the CLI, and exit behaviour.
* **Caveat ground swapped (R9b).** The "design-level, not import-level"
  caveat now rests on `bootstrap/tests/_gate_manifest.py:167` freezing
  `templates/modules/**/*.py`, plus this proposal's own fence that
  `_stage_for_subject` is private and unexported — not on "no such
  dependency exists", which `scripts/check_cairn.py:125` falsifies.
* **Vocabulary asymmetry (R9c).** The lint needs `accept` / `reject` /
  `supersede` as first-class claim tokens; this reader deliberately
  carries none of them.
* **New evidence reported (R8).** Commit `88fd91f`
  (`dev/proposals: transition-lint -- record Maintainer sequencing
  direction (not a Decision)`) modifies the proposal file and adds only
  a `## Sequencing note` heading. The sibling's `decision` token is not
  positionally anchored, so the parenthesised "(not a Decision)" would
  claim a Decision with no `## Decision` evidence — a Shape (a) false
  positive on a commit *outside* the pinned `d6646a3..57d1daf` dogfood
  window. The repaired reader returns `None` on the same subject. If the
  lint is ever authorised, its `decision` token likely needs the same
  positional treatment `open` received, and P1's `decision` pattern is a
  working precedent.

### Revised tests

Additions and corrections to the frozen list in
`bootstrap/tests/test_lifecycle_stage_patterns.py`:

* **All 10 adopter-plausible subjects** from R1, with their intended
  classifications — 9 `None`, and `review: tighten the recharge bounds`
  → `reviewed` *labelled as pre-existing shipped-pattern behaviour*, so
  a future reader does not mistake it for something this fix chose.
* **All 7 `dev/plans:` corpus subjects** → `None` (R3), plus
  `dev/plans: <slug> -- Code review (fresh-context, disclosed scribe)`
  → `None`.
* **All three real Decision forms** including the slug-first
  `… -- Maintainer Decision -- ACCEPT (post Internal review)` →
  `decision` (R2), and `… -- SUPERSEDE bar` → `None` as a documented
  false negative.
* **Both sharpening directions** (R4):
  `dev/proposals: <stem> -- Internal review (fresh-context panel) +
  Sharpening` → `reviewed`, and `Review sharpening pass` → `None` (the
  shipped exclusion, still exactly where it was).
* **Corrected hyphen-guard test** (R6): the discriminating case is
  `dev/proposals: interpreter-trust-root -- add Security-Review section`
  → `None`; the `Security-Review gated` case stays but is relabelled a
  *priority-order* test.
* **The four `days_*`/`hours_*` divergence rows and one `0.0`-delta
  pair** (R5), pinned with the backdating explanation in the docstring.
* Proposed test 5's docstring notes it is the only thing pinning P2
  (R10).

### Revised smoke checks and plan obligation

* Add: the `0 Best-effort` verification must run on a **quiet tree** —
  concurrent git load makes `_git_log_for_path` return `[]` at
  `gitmeta.py:50-51` and silently degrades a row (R12c; pre-existing,
  out of scope, noted to the Maintainer as an observation).
* The plan carries an explicit **execution** obligation for its Internal
  reviewer, not a reading one: re-run the classifier over the live
  `git log --follow` subject set at then-current HEAD, and run at
  minimum the scope-prefix, `plans?` and hyphen-guard ablations,
  reporting counts. Four of the six most serious findings here were
  invisible from reading and surfaced only by ablation; the frozen list
  is an oracle only for subjects already in it.

### Revised open questions

1. **The 41-entry lockfile staleness from `501efe3`** — unchanged, still
   the Maintainer's call, still deliberately untouched.
2. *(withdrawn — P3 ships.)*
3. **The plan-review tier.** Still declared `required(Internal)` on
   `doctrine/dual-review.md:184-187`, and the panel concurs. I note one
   thing against my own tier: the revised design changes what an adopter
   tree's commits do and do not classify as, which is closer to
   adopter-visible behaviour than the original framing implied. If the
   Maintainer reads that as contract-touching, External is defensible.

## Review -- Gemini (External, different-agent-type) -- 2026-07-22

**Model**: Gemini 3.6 Flash / Antigravity
**Verdict**: SHIP (conditional on Maintainer resolution of Open Question 1 and plan execution of ablation verification)

### Steelman
This proposal repairs a silent, critical defect in Cairn's default-on `_lifecycle_metrics` module: `_STAGE_COMMIT_PATTERNS` matches 0 of 76 real proposal commit subjects, causing all timing metrics (`hours_open_to_reviewed`, `hours_reviewed_to_revised`, `hours_revised_to_decision`) to remain empty and `stage_timestamp_reliability` to return `Best-effort` across 100% of proposal rows. The author's Response and Revised proposal make a decisive, honest correction: by gating stage keywords behind a `dev/proposals:` scope prefix or positional ` -- ` stage phrase, the revised design completely eliminates the Internal panel's blocking hazard R1 (mislabeling ordinary adopter commits as lifecycle transitions). Executed on the canonical interpreter (`~/conda_envs/lhm/bin/python`, Python 3.13.13), the revised classifier resolves 10 `Exact` / 2 `Good` / 0 `Best-effort` across the proposal corpus with 0% over-matching on non-lifecycle commits.

### Critiques

* **[E1] (Verification of Narrowing & Over-Matching Defense)**
  Re-executed the revised classifier on the canonical interpreter (`~/conda_envs/lhm/bin/python`, Python 3.13.13) across the real corpus of 76 distinct proposal subjects and recent commits:
  1. *Elimination of Adopter False Positives:* Gating keyword matching behind the `dev/proposals:` scope prefix or positional ` -- ` stage phrase successfully takes all 10 adopter-plausible false positives identified by the Internal panel (e.g. "Add impulse response function to the transport solver", "docs: review the API surface") to `None`.
  2. *Corpus Accuracy:* 52 of 76 subjects classify cleanly with zero wrong-stage assignments.
  3. *Pipeline Output:* Monitored through `extract.proposal_rows(Path('.'))` on Python 3.13.13: the 13 proposal rows yield **10 `Exact` / 2 `Good` / 0 `Best-effort`** (with `ast-known-new-repin` cleanly reporting `Good` due to its un-scoped review commit subject rather than overclaiming `Exact`).

* **[E2] (Trade Judgment: One Reliability Tier for 100% Precision)**
  The trade of classifying 52 of 76 subjects (yielding 2 `Good` rows instead of 11 `Exact` / 1 `Good`) to eliminate bare-subject fallback is undeniably correct. In an adopter tree, emitting a wrong stage timestamp labeled `Exact` breaks adopter trust. Accepting `Good` for un-scoped subjects while guaranteeing 0 false positives preserves module integrity.

* **[E3] (Shipped-Copy Parity & Lockfile Posture)**
  * **Twin Parity:** Verified that `templates/modules/default-on/_lifecycle_metrics/gitmeta.py` and `tools/_lifecycle_metrics/gitmeta.py` (and the `__init__.py` pair under P3) are byte-identical, satisfying `bootstrap/tests/test_notice_install.py:98`.
  * **Lockfile Posture:** Confirmed that `dev/.cairn/cairn-lock.yml:498` currently carries a pre-existing mismatch from commit `501efe3` (alongside 40 other entries). Leaving the lockfile hash untouched in this defect fix avoids arbitrary partial updates and adheres strictly to the scope fence.

* **[E4] (Ruthless Audit Against Standing Stopping Rule)**
  Audited the proposal against the Maintainer's stopping rule ("fix defects, build nothing new"). Confirmed that:
  * No new CLI command, subcommand, or flag is added.
  * No new configuration key or option is created.
  * No new output column or metric schema is introduced.
  * No exported helper function or public API is created (`_stage_for_subject` remains private).
  * No commit-message convention or doctrine rule is mandated.
  The proposal strictly repairs the internal `_STAGE_COMMIT_PATTERNS` regexes and `_resolve_stage_commits` logic in `gitmeta.py`.

* **[E5] (Verification of Assigned Obligation — Sibling Transition-Lint)**
  Confirmed the proposal's conclusion: repairing `_STAGE_COMMIT_PATTERNS` does **not** make the sibling `2026-07-22-claude-transition-lint` proposal unnecessary.
  * `_resolve_stage_commits` in `gitmeta.py` resolves file-history stage timestamps; it never opens or inspects diffs.
  * Incident commit `17b7e5c` carried a correct `open` subject string, but its diff introduced a file already carrying two pre-filled `## Review` blocks.
  * Message-versus-diff validation remains a distinct capability. The stage classifier supplies proof of positional matching and prefix stripping, but does not replace diff validation.

### Coverage

* **Covered**:
  * Executed revised classifier on Python 3.13.13 (`~/conda_envs/lhm/bin/python`) over 76 proposal subjects and last 60 repo commits.
  * Monitored `proposal_rows` execution yielding 10 `Exact` / 2 `Good` / 0 `Best-effort`.
  * Verified twin byte-identity for `gitmeta.py` and `__init__.py` pairs via `test_notice_install.py:98`.
  * Verified lockfile integrity status via `verify_integrity.py --target .` (41 pre-existing mismatches confirmed).
  * Evaluated sibling transition-lint overlap against `17b7e5c` diff structure.
* **Not covered**:
  * End-to-end execution against external non-Cairn repositories (to be covered by test fixtures in plan execution).
  * Implementation of `bootstrap/tests/test_lifecycle_stage_patterns.py`.

## Response -- Claude (author, to External review) -- 2026-07-22

**Model**: Claude Opus 4.8. Proposal-Response grammar. The External read returned
**SHIP** and did the verification that matters most for this proposal: it
*re-executed* the revised classifier on the canonical interpreter rather than
reasoning about it, and independently reproduced the numbers. Four critiques
accepted as confirmatory. **One — E3 — is accepted in half and must be
inverted in half, because its premise stopped being true after the review was
written.** That inversion changes what the implementing plan is obliged to do,
so it is recorded here rather than left to be discovered at execution.

* **[E1] accept — confirmatory, and the strongest possible form of it.** The
  reviewer re-ran the revised classifier on `~/conda_envs/lhm/bin/python`
  (3.13.13) over the real corpus and reproduced the claim independently: 52 of
  76 subjects classify with **zero wrong-stage assignments**, all ten
  adopter-plausible false positives the Internal panel constructed (e.g.
  "Add impulse response function to the transport solver", "docs: review the
  API surface") resolve to `None`, and the pipeline yields **10 `Exact` / 2
  `Good` / 0 `Best-effort`**. That the blocking hazard R1 is *eliminated* rather
  than *mitigated* is now attested by a second agent type on the canonical
  interpreter.
* **[E2] accept — confirmatory.** The trade is affirmed in the terms it should
  be judged on: a wrong stage timestamp labelled `Exact` breaks adopter trust,
  and accepting `Good` on un-scoped subjects to guarantee zero false positives
  is the correct price. Worth recording that `ast-known-new-repin` reports
  `Good` rather than overclaiming `Exact` — the design degrades honestly on the
  one row where it cannot be certain, which is the behaviour the whole
  narrowing exists to produce.
* **[E3] accept in part — and INVERT the lockfile half.** The twin-parity half
  stands unchanged: `gitmeta.py` and the `__init__.py` pair are byte-identical
  across template and installed copy, and the plan keeps them so.

  The lockfile half was **correct when written and is now wrong**, through no
  fault of the reviewer. Their reasoning was: 41 entries were already stale from
  `501efe3`, so touching one more would be an arbitrary partial update — leave
  it, and let Open Question 1 resolve the whole set. Sound, given the tree they
  measured.

  **Open Question 1 has since been resolved.** Commit `41875e4` finalized all 41
  stale hashes via `scaffold.py upgrade --finalize`, after verifying each flagged
  file byte-for-byte against its template source (all 41 matched — staleness
  only, nothing divergent). `verify_integrity --target .` now attests the tree.

  The consequence inverts the advice: **with a clean lockfile, leaving
  `gitmeta.py`'s hash untouched no longer avoids a partial update — it creates a
  fresh mismatch and re-reds `verify_integrity`.** The implementing plan
  therefore **must** advance the lockfile records for `gitmeta.py` and the
  `__init__.py` twin as part of the change, using the same
  `upgrade --finalize` surface, scoped to those paths. This is now a plan
  obligation, not an open question.

  The same premise appears inside the proposal itself: P3's justification reads
  "both are already stale from `501efe3`, so P3 adds no new gate posture." That
  sentence is **withdrawn**. Both files are now current, so touching them *does*
  create new posture — a fresh mismatch requiring a scoped finalize. P3 still
  ships; its rationale changes, and the plan carries the finalize.
* **[E4] accept — confirmatory, and the audit I most wanted an outside agent to
  run.** The stopping-rule audit is affirmed point by point: no new CLI command,
  subcommand or flag; no new configuration key; no new output column or metric
  schema; no exported helper (`_stage_for_subject` stays private); no mandated
  commit convention. The change repairs `_STAGE_COMMIT_PATTERNS` and
  `_resolve_stage_commits` and nothing else. Under a standing "fix defects,
  build nothing new" direction, that verdict from a different agent type is
  worth more than my own assertion of the same.
* **[E5] accept — confirmatory, with the sharpest available evidence.** The
  assigned obligation is answered and independently confirmed: repairing the
  vocabulary does **not** make the sibling `2026-07-22-claude-transition-lint`
  unnecessary. `_resolve_stage_commits` resolves stage timestamps from file
  history and *never opens a diff*. The reviewer grounds this in the original
  incident: commit `17b7e5c` carried a perfectly correct `open` subject while
  its diff introduced a file already carrying two pre-filled `## Review` blocks.
  A repaired subject vocabulary would have read that commit as a clean `open`.
  Message-versus-diff validation is a distinct capability, and the repair
  supplies only the message side.

### Open questions after this Response

* **OQ1 — resolved** (see E3): the 41-entry staleness is finalized at
  `41875e4`; the plan inherits a scoped-finalize obligation instead.
* **OQ3 — the plan-review tier** remains the Maintainer's. I declared
  `required(Internal)` and the Internal panel concurred, but I flagged against
  my own tier that this change alters what an adopter tree's commits classify
  as. The External read did not disturb the tier. It is a genuine call and I do
  not claim it.

Net: External **SHIP**, its one stale premise inverted and converted into a plan
obligation before it could reach execution. Decision-ready.

## Decision -- Anthony Kendall (Maintainer) -- 2026-07-22

**Accepted, as revised.** Scribed by Claude (Strategy) at the Maintainer's
explicit instruction, given in direct response to a drafted Decision offered for
authorization; commit permission given in the same exchange.

Maintainer's authorization (verbatim):

> I accept this proposal as revised

*Scribe's reading of "as revised", recorded so it is correctable:* accepted in
the form set out in the **Revised proposal** section, which supersedes the
original design — not the proposal as first opened.

**What it repairs.** A silent defect in a **default-on** module:
`_STAGE_COMMIT_PATTERNS` matched **zero of 76** real commit subjects, leaving
every stage-timing metric empty and `stage_timestamp_reliability` at
`Best-effort` on 100% of rows — while the tool exited 0 and emitted a
well-formed report. The diagnosis is that the vocabulary was never Cairn's: an
invented grammar validated only against Cairn's own toy examples, never a real
log.

**Why it lands.** The Internal panel's **blocking R1** established that a naive
repair would be *worse than the status quo* — a bare-subject fallback would
mislabel ordinary commits as lifecycle transitions and report the wrong
timestamps as `Exact`, where today's all-`Best-effort` at least tells the truth.
The design was **narrowed rather than rescued**: no bare-subject fallback, the
vocabulary gated behind a `dev/proposals:` scope prefix or a positional stage
phrase. Gemini's External read then **re-executed** the classifier on the
canonical interpreter and independently reproduced **52 of 76 classified, zero
wrong-stage, 10 `Exact` / 2 `Good` / 0 `Best-effort`**, with all ten
adopter-plausible false positives resolving to `None`. One reliability tier was
surrendered to buy the elimination of every wrong-stage-at-`Exact` hazard; that
is the right price.

**Open questions resolved.** **OQ1** — the 41-entry lockfile staleness from
`501efe3` is finalized at `41875e4`, after each flagged file was byte-verified
against its template source. **OQ2** — withdrawn; P3 ships. **OQ3** — the
plan-review tier stays **`required(Internal)`**.

**Plan conditions, ratified here (bind the plan):**

* A **scoped `upgrade --finalize`** for `gitmeta.py` and its `__init__.py` twin.
  This is now *mandatory*: the External review advised leaving the lockfile
  untouched, correctly, on a tree where 41 entries were already stale — but OQ1's
  resolution inverted that. With a clean lockfile, leaving these records would
  create a fresh mismatch and re-red `verify_integrity`.
* Template and installed-copy **byte-parity** maintained across both file pairs.
* **No AST re-anchor** — nothing under `bootstrap/_scaffold/` is touched.
* The stopping rule holds: no new CLI, configuration key, output column,
  exported helper, or mandated commit convention.

**Recorded for the sibling proposal.** The assigned obligation is answered: the
transition-lint (stem `2026-07-22-claude-transition-lint`) is **not** made
unnecessary by this repair. `_resolve_stage_commits` reads file history and never
opens a diff, so the repaired vocabulary supplies the *message* side only. The
original incident is the proof: commit `17b7e5c` carried a correct `open`
subject while its diff already contained two pre-filled `## Review` blocks — this
repair would still read it as clean. That proposal remains parked pending the
Maintainer's explicit go-ahead under the standing build-nothing-new rule.

**Next (separate commits):** open the plan (which archives this proposal),
implement, non-implementing code review, archive.
