<!-- cairn-internal-ref-allow: doctrine/proposals.md doctrine/dual-review.md doctrine/rationale.md doctrine/lifecycle.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- Two deliberate forward references, both named repeatedly outside the Proposed-paths block: the new test file lands with the implementing plan, and scripts/transition_lint.py is the SIBLING proposal's proposed path, cited here only to argue about whether it should be built. -->
<!-- claim-check-allow: bootstrap/tests/test_lifecycle_stage_patterns.py, scripts/transition_lint.py -->

# Repair `_STAGE_COMMIT_PATTERNS` — the shipped lifecycle-stage commit vocabulary reads nothing

**Author**: Claude (Strategy)
**Model**: Claude Opus 4.8
**Date opened**: 2026-07-22
**Status**: proposed
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
