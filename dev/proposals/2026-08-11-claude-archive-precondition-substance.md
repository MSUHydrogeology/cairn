# Archive preconditions that test what they name

**Author**: Claude (Implementation)
**Model**: Claude Opus 5 (`claude-opus-5`)
**Date opened**: 2026-08-11
**Status**: proposed
**Touches**: `tools/lifecycle_planner.py` and its byte-identical twin
`templates/skills/_lib/lifecycle_planner.py`; `bootstrap/tests/test_lifecycle_contract.py`;
`dev/plans/_template.md`; potentially `doctrine/lifecycle-contract.md` and
`doctrine/dual-review.md`
**Related**: `dev/PLANNING.md` **[SP8-1]**, **[SP8-9]**; the archives of
`api-web-security-modules` and `security-verification-activation` (`98ad97a`);
the partial fix at the commit that opens this proposal
**Plan review**: required(External) — this changes a shipped checker's archive
contract, which every adopter's lifecycle depends on

## Context

On 2026-08-11 two plans archived with **no code review at all** while the
archive precondition reported success. The gate was
`_has_kind(art, "Code review")` — it tested the section's **presence**. Every plan
scaffolded from `dev/plans/_template.md` ships that section pre-written as a
placeholder (*"Filled in after implementation commits land."*), so **the gate
could not fail on any plan Cairn generates.**

`AGENTS.md` > *Verifying claims* already names this failure class: *"a tool that
returns success without testing the claimed property is a worse defect than no
tool, because it is silent."* This was that, in Cairn's own lifecycle checker,
guarding the review discipline that is one of Cairn's two stated
differentiators.

Investigating it surfaced a second defect in the **opposite** direction, and two
more gates with the same shape. The commit opening this proposal fixes the two
that are unambiguous bugs; this proposal exists for the part that is a design
decision.

### What the investigation actually measured

| Gate | Defect | Direction |
|---|---|---|
| `## Code review` | satisfied by section presence; the shipped template's placeholder passes | **false pass** |
| `Dispositions:` | matched an unbolded-only pattern, so the repository's own `**Dispositions:**` house style read as absent — **12 archived plans** each carrying a block were flagged as having none | **false fail** |
| `Dispositions:` (pre-transition) | hardcoded `True` in the `--to archived` gate list | **false pass** |
| loop-fidelity (post-hoc) | case-insensitive regex for the phrase *"Fidelity sign-off"* or *"loop-fidelity"* anywhere in the artifact; writing the phrase satisfies it | **false pass** |
| loop-fidelity (pre-transition) | hardcoded `True` in the `--to archived` gate list | **false pass** |

Two figures worth recording because they were each measured wrong first, and the
wrong ones are the plausible ones:

* **Archived plans with no real code review anywhere: 3**, not 27. A first pass
  said 27 because it examined only the first `## Code review` section per file;
  a plan may carry the placeholder *and* a real reviewer's section further down.
  An earlier pass said 23 because it looked only at the section's first three
  lines. The three are `api-web-security-modules`,
  `security-verification-activation`, and `gate-reanchor-preflight` — the last
  previously unknown.
* **The `lifecycle_planner scan` subcommand does not cover `dev/plans/archive/`**
  (6 artifacts scanned). So none of these post-hoc violations was ever surfaced
  by the scan; they are reachable only by pointing `next` at an archived file.
  That is why the defects survived: the checker had the rule and never applied it
  to the corpus where it mattered.

## Proposed paths

<!-- claim-check-allow: doctrine/lifecycle-contract.md, doctrine/dual-review.md -->

* `tools/lifecycle_planner.py` + `templates/skills/_lib/lifecycle_planner.py`
  (byte-identical twins — both, same commit)
* `bootstrap/tests/test_lifecycle_contract.py`
* `dev/plans/_template.md`
* `doctrine/lifecycle-contract.md`, `doctrine/dual-review.md` — only if the
  decision changes stated doctrine rather than only its enforcement

## Proposal

Three questions, in decreasing confidence about the answer.

### 1. The two hardcoded `True` gates should test their conditions

In the `--to archived` pre-transition gate list, the Dispositions gate and the
loop-fidelity gate are literal `True`. They always report met, so
`next <plan> --to archived` tells an agent both preconditions are satisfied
before either has been written. **This is the gate an agent consults when
deciding whether it may archive**, which makes it the load-bearing one — the
post-hoc `status == archived` check runs after the fact, on a corpus the scan
does not walk.

Proposed: both consult the parsed flags, as the code-review gate now does.

This is close to a bug fix, and it is separated from the commit opening this
proposal only because it will make `--to archived` refuse for artifacts that
currently pass, which is a behaviour change adopters will see.

### 2. Should the scan cover `dev/plans/archive/`?

Today it does not, which is why 3 unreviewed archives and 12 falsely-flagged
Dispositions blocks went unnoticed. Arguments both ways:

* **For**: a precondition nobody ever evaluates is not a precondition. The whole
  archived corpus is exactly where "did this actually get reviewed?" is
  answerable.
* **Against**: archived artifacts are immutable history. A scan that reds on
  historical records is unactionable noise and will be ignored or suppressed —
  and a suppressed gate is the defect this proposal is about, one level up.

A middle option: scan the archive but classify pre-existing violations as a
dated, enumerated backlog rather than as failures, so the count is visible and
drainable without making the scan permanently non-zero. **This needs a decision,
not an implementation.**

### 3. What can a text scanner honestly assert about a review?

The fix in the opening commit tests for a **marker** — a `**Model**:` identity
line or a dated `Code review -- <reviewer> -- YYYY-MM-DD` heading. It moves the
gate from *impossible to fail* to *requires a deliberate false statement*. That
is a real improvement and an honest limit, but it is not "a review occurred", and
the gate's message should not imply otherwise.

The deeper question is whether the lifecycle contract should stop asserting
"code review occurred" at all and instead assert the checkable thing — "a review
section bearing a reviewer identity and date is present" — with the actual
assurance resting where it already rests: on `AGENTS.md`'s rule that reviews are
attributed and self-committed. That is a doctrine question, which is why this is
a proposal rather than a patch.

## Rationale

Cairn's two differentiators are the append-only deliberation lifecycle and the
Dual-Review model. A checker that reports a satisfied review precondition when no
review exists undermines the second one, and it does so **silently** — which is
worse than the absence of a checker, because the passing gate is cited as
evidence. It was in fact about to be cited that way: both 2026-08-11 archives
passed their preconditions.

The false-fail direction matters for the same reason inverted. A precondition
that flags a correct record trains its readers to disregard it, and 12 archived
plans were being flagged for using the house style that the plan which
introduced the vocabulary had itself used.

## Alternatives considered

* **Fix nothing; rely on discipline.** Rejected: the discipline held — the
  Dispositions blocks and sign-offs were written — and the checker still got both
  answers wrong. This is a tooling defect, not a compliance one.
* **Require a reviewer name from the AI registry / human maintainer set.** The
  planner already loads an `IdentityModel`. Stronger than a marker, but it would
  reject a legitimate external reviewer not yet in the registry, and it
  centralizes a decision about who may review. Worth considering in the plan.
* **Make the placeholder absent from the template**, so presence alone means
  something. Tempting and cheap, but it silently breaks the template's guidance
  role, and any adopter who pastes the old placeholder back re-opens the hole.
  Fixing the checker is the durable half; the template is at most a companion
  change.
* **Fix all five gates in the opening commit.** Rejected: two are unambiguous
  bugs and three are behaviour changes with adopter impact. Bundling them would
  put a contract change in a bug-fix commit and give the reviewers nothing to
  disagree with separately.

## Evidence / verification plan

Already established, in the commit that opens this proposal:

* Eight tests in `bootstrap/tests/test_lifecycle_contract.py`, including one
  asserting **the real shipped `dev/plans/_template.md` does not pass the gate**
  (measured against the file, not an imitation), and one asserting that a
  placeholder followed by a real review section *does* pass — the case the first
  blast-radius measurement got wrong.
* Both fixes perturbed against `templates/skills/_lib/lifecycle_planner.py`
  (the copy the suite loads, **not** the `tools/` twin — this repository has hit
  the twin-mutation trap twice): each mutant red at the predicted node, restored
  byte-exactly by `shasum -a 256`.
* 246 passed across the seven suites touching the planner.

Still owed, and belonging to the plan rather than here:

* A test that the two pre-transition gates refuse — currently unwritable, since
  they are literal `True`.
* A decision-dependent test for whichever archive-scan option is chosen.
* Re-derivation of the "3 archived plans with no real code review" figure at
  implementation time. **Do not carry that number forward from this proposal**;
  it moves as reviews land, and the review prompt for two of the three is already
  out.

### Security preflight — five questions, answered in writing

1. **Does this parse untrusted input?** It parses `dev/` artifacts, which are
   repository-controlled and reviewed. No new external input.
2. **Does it execute anything?** No. The planner is read-only and never mutates
   or commits; this changes only predicates.
3. **Can it be made to pass when it should fail?** Yes, and that is the stated
   residual — an author can write `**Model**: x` without reviewing. Named in the
   gate's own comment and in **[SP8-9]**, not hidden.
4. **Can it be made to fail when it should pass?** This is the direction that
   just bit us. Any tightening must be measured against the whole archived corpus
   before landing, which is what caught the 12 false flags.
5. **Does it widen a trust boundary?** No. It narrows an existing precondition
   and corrects another. The shipped twin must stay byte-identical, and the
   template copy is lockfile-covered, so a scoped `--finalize` is required.

## Signals the change is wrong

* The archive scan becomes routinely red and someone proposes suppressing it —
  that means option 2 was decided wrong, not that the gate should go.
* Agents begin writing `**Model**:` lines mechanically to clear the gate without
  a review happening. That would mean the marker approach bought nothing and the
  identity-registry alternative is needed.
* An adopter's legitimate archive is blocked by a reviewer format Cairn did not
  anticipate.

## Review -- Claude (Internal) -- 2026-08-11

**Tier**: Internal. Same agent type as the author, fresh context — this meets
the Internal floor and **does not** meet the External one. The proposal's
`**Plan review**: required(External)` is unaffected; this complements it rather
than substituting for it.

**Verified before commenting** (not inherited from the proposal text): the twins
are byte-identical right now; the planner's substantive-review predicate is
`^#{2,3} Code review\s*--\s*\S+.*\d{4}-\d{2}-\d{2}` plus the `**Model**:`
alternative; and the archived corpus was re-measured independently.

### Steelman

The proposal does the thing that is easy to skip: it found a false-pass gate,
and then kept looking and found a false-*fail* in the opposite direction plus
three more gates of the same shape. Splitting unambiguous bugs from
adopter-visible behaviour changes is right, and the "measured wrong first, and
the wrong numbers are the plausible ones" paragraph is the most valuable thing
here — 27 → 23 → 3 is exactly the correction sequence a reader needs to see to
trust the final figure. The instruction *not* to carry the 3 forward is already
vindicated: measuring today, only **one** archived plan (`gate-reanchor-preflight`)
fails both markers, because reviews landed for the other two.

### Findings

**[I1] A second implementation of this predicate already exists, disagrees, and
nothing keeps them in sync.** `_lifecycle_metrics/parse.py` detects code reviews
for the metrics layer with `r'### (?:[a-z]+ )?code review\b'` — **H3 only**.
The planner accepts `#{2,3}`. Measured over the 36 archived plans:

| | plans |
|---|---|
| both patterns find a review | 10 |
| **planner finds, metrics misses** | **25** |
| metrics finds, planner misses | 0 |
| neither | 1 |

The planner's pattern strictly dominates — there is no case the metrics regex
catches that the planner misses. Two consequences for this proposal. First, it
is **evidence for question 3**: the marker approach is not merely a defensible
compromise, it is measurably the better-calibrated of the two shapes Cairn
currently ships, and `#{2,3}` matches what `dev/plans/_template.md` actually
prescribes. Second, and more important: **two components now answer "did a code
review happen" differently, and no mechanism keeps them agreeing.** That is the
proposal's own thesis — a check that names a property without testing it — at
one level up.

*Recommended disposition: name it, do not absorb it.* The metrics defect belongs
to the `lifecycle-metrics` module, has a consequence this proposal does not
share (fixing it changes the values of every historical snapshot), and pulling
it in would put a second module's contract change inside a lifecycle-planner
proposal. But question 3 should record that whatever predicate it settles on
becomes the **definition other components must converge to**, and the plan
should say where that definition lives so the next implementation copies rather
than re-invents.

**[I2] Question 2 has an existing precedent the proposal does not cite.** The
metrics extractor already walks `dev/plans/archive/` routinely — its plan
corpus is 38 rows, 36 of them archived — and this has produced no noise
complaints, because it **reports** rather than **fails**. That is the proposal's
own middle option, already running in another component. Worth citing: it turns
"a scan that reds on history is unactionable noise" from a prediction into a
comparison against something Cairn already does.

**[I3] Is the gate enumeration complete?** The table lists five. The
`Plan review` gate carries a comment (S12) documenting the *identical* failure
class — a prefix-presence test that cleared on a bare container, an undated
heading, an H3 pass, and an `Internal`-only pass on an `External` floor. It
appears already fixed, so it is correctly out of scope, but its existence means
this is a **pattern across the planner's gates rather than five isolated bugs**.
Recommend the plan enumerate *every* gate in the `--to` lists and record each
one's predicate, so the next reader can see coverage rather than infer it from
the five that happened to be investigated.

**[I4] One wording tightening.** The Context says the gate "could not fail on
any plan Cairn generates." That is right for the template's placeholder, but
the sentence reads as *no plan could ever fail*, when a hand-written plan
omitting the section entirely would still have failed. Narrow to "could not
fail on any plan scaffolded from the shipped template" — the claim is strong
enough without the broader reading, and the broader reading is the kind a
skeptical reviewer will test.

### Recommendation

**Land questions 1 and 3; decide 2 with [I2] on the table.** Question 1 is a
bug fix wearing a behaviour-change coat and should not linger — a gate that
reports met before its condition is written is the same defect class the
proposal exists to close. Question 3 is the one that needs the External plan
review the header already requires, and [I1] gives it a concrete obligation:
whatever it decides is a definition with at least one other consumer.

Nothing here blocks. The proposal is well-scoped and unusually honest about its
own measurement errors; my findings add a second consumer, a precedent, a
completeness question, and one sentence to narrow.
