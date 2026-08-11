# Archive preconditions that test what they name

**Author**: Claude (Implementation)
**Model**: Claude Opus 5 (`claude-opus-5`)
**Date opened**: 2026-08-11
**Status**: revised
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
could not fail on any plan scaffolded from the shipped template.**

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

## Review -- Codex (External) -- 2026-08-11

**Model**: GPT-5.6-Codex
**Tier**: External, different agent type from the author
**Reviewed commit**: `b1eb3b3e490130741d91e309d2b3c92fee0d5d8e`
**Reviewed proposal blob**: `af3fb86c683eba6afca8e6253f434a61c6f9444e`
**Assurance path**: high-assurance

**Verdict: REVISE.** The false-pass diagnosis and the marker improvement are
real, and the Internal review found the right adjacent consumer. The proposal
is not yet decision-ready because Question 1 treats a prior deliberate doctrine
choice as an accidental `True`, then proposes wiring two booleans that still
pass on empty or promissory text. Question 2 also overlooks a shipped
`--include-archive` mode, so its option set is framed around adding a capability
that already exists.

### Steelman

The opening repair measurably improves the code-review predicate: against the
exact 36-plan archive at `da3e296`, all three plans the proposal names lack both
accepted markers, while a placeholder followed by a later attributed review is
correctly accepted. The shipped plan template itself refuses. The bold-label
parser repair also moves in the right direction, and the nine focused tests I
ran pass. Most importantly, the proposal distinguishes what text can attest
from what actually occurred; that should govern the revision.

### [E1] HIGH -- wiring the existing flags repeats the presence-for-substance defect

The two literal `True` values are not equivalent.
`deferral-discipline` deliberately required the Dispositions transition gate to
remain unconditional: its accepted plan says *"Stay unconditional -- do not
promote `gates.append((True,` to a check"*, and records the zero-follow-up edge
case as **omitting the block**. This proposal may supersede that choice, but it
must name and redesign it; it cannot classify the `True` as an unambiguous bug.

More directly, the parsed booleans do not test the descriptions beside them. I
executed the exact `da3e296` planner against a `Status: review` fixture carrying:

```text
**Dispositions:**

Loop-fidelity sign-off is owed at archive.
```

The empty label sets `has_followups_migrated=True`; the promissory sentence sets
`has_fidelity_signoff=True`. The fixture's existing archive gate descriptions
claim every follow-up has a disposition and that the sign-off names an
implementing commit and governing Revised section. Replacing the two `True`
values with these flags would report both claims met without either fact.

**Required satisfier.** Settle the zero-follow-up contract explicitly. My
recommendation is to supersede the omission rule for future archives and require
a non-placeholder `Dispositions:` attestation every time, with an explicit
`none` form when there are no follow-ups. Define and test a structural grammar:
at least `none` or one allowed disposition entry for the first gate; and a
fidelity attestation scoped to the lasting-truth section that contains at least
one implementing commit id and an identified governing section for the second.
Legacy `Follow-ups migrated to:` records remain accepted. Empty labels, template
instructions, "owed at archive," and prose merely discussing either phrase must
all refuse. Update the doctrine/template surfaces because this intentionally
changes the accepted `deferral-discipline` contract.

The plan should also take Internal [I3]: enumerate every transition gate and the
predicate that supplies it. That table is how reviewers verify this pattern was
swept rather than repaired twice more by discovery.

### [E2] HIGH -- archive scanning already exists, and its current output changes the decision

`scan --include-archive` has existed since `7519c5d`; the proposal's opening
commit did not add it. At the exact proposal-opening tree, default `scan`
examines **7**, not 6, live artifacts and exits 0. The existing archive mode
examines **88** artifacts, reports **53** with structural violations, and exits
1. I reproduced both from a `git archive da3e296` extraction so concurrent live
work could not affect the result.

Question 2 is therefore not "should scan cover the archive?" It is whether the
archive should enter the **default** scan and how the already-strict opt-in mode
should be used. Fifty-three retrospective violations across proposal and plan
rules make a default-red scan exactly the suppression pressure the proposal
warns about.

**Required satisfier.** Preserve the live-only default. Preserve and document
`--include-archive` as the explicit strict historical audit; do not silently
change its exit semantics or build a 53-entry suppression baseline into the
routine gate. Record the dated archive findings as backlog/report evidence, and
let the corrected pre-transition predicates prevent new instances. If the
author wants a report-only archive mode, specify it as a new output contract
rather than describing archive traversal as absent.

### [E3] MEDIUM -- call the marker what it is, and make that definition canonical

Question 3 should choose the narrower claim. A `**Model**:` line or dated heading
proves a review-shaped marker is present; it does not prove a review was
substantive or occurred. Yet the landed helper and field are named
`_has_substantive_code_review` / `has_substantive_code_review`, and the archive
gate still says *"a code review has occurred."* The careful comment does not
repair an overclaim in the API and operator output.

**Required satisfier.** Rename the predicate around an attributed/dated
code-review record marker and make every message claim only that shape. Keep the
actual-review assurance in the self-authored/self-committed Git discipline, as
the proposal recommends. Accept Internal [I1] without absorbing the metrics
migration: declare this marker grammar canonical in one governing contract,
and route `_lifecycle_metrics/parse.py` convergence as an explicit follow-up
whose snapshot impact is measured before implementation. A second regex must
not quietly become a second definition again.

### [E4] MEDIUM -- the opening implementation must remain inside code-review coverage

Commit `da3e296` already changes both shipped planner twins and adds the marker
tests before this proposal is reviewed or decided. The urgent, reversible bug
fix rationale explains the ordering, but proposal review is not implementation
code review.

**Required satisfier.** Require the eventual plan's Boundary B and independent
code-review range to include `da3e296` (or its exact changed blobs) alongside
the later implementation. The code review must attack the marker parser and
house-style compatibility, not treat the eight opening tests as settled
authority outside the reviewed range.

### [E5] LOW -- two recorded figures do not reproduce at the cited opening tree

The load-bearing count of three no-marker archived plans reproduces exactly.
Two supporting figures do not: default scan reports 7 live artifacts, not 6;
and comparing the old and new Dispositions parsers over the exact 36 archived
plans shows **6** plans change from absent to present, not 12. If 12 uses a
broader manual definition of "carrying a block," the opening parser does not
recognize that broader set, which strengthens E1 rather than validating the
claim.

**Required satisfier.** Correct the live count, and either replace 12 with the
measured six-parser delta or define the broader oracle, list its members, and
make the proposed parser recognize it. Keep the instruction to re-derive the
moving no-review count at implementation time.

### [E6] MEDIUM -- the proposal's valid Internal review makes the planner call the artifact invalid

After this External section was present, `lifecycle_planner.py next` still
reported a structural violation: the Internal review at line 210 *"appears
authored by the proposal author."* That review explicitly declares the
same-agent-type, fresh-session Internal floor which `AGENTS.md` permits. The
identity normalizer collapses both sessions to `Claude` and therefore treats an
allowed Internal record as forbidden author-review. The External pass satisfies
the independent-review transition, but it cannot make the valid Internal record
stop poisoning conformance.

**Required satisfier.** Name and route this defect to the existing **[REC]
Deliberation authority, identity, context, record integrity** lineage (including
`code-review-blindness`), rather than absorbing another identity-policy change
here. Do not claim this proposal structurally sound while the planner reports
otherwise, and do not delete or relabel the Internal review to appease the
checker. This is another instance of Question 3's limit: the tool can inspect a
declared record shape but cannot infer whether two same-named sessions are the
same authoring context.

### Covered and not covered

**Covered**: exact proposal and opening-commit bytes; both planner twins; the
opening tests and real template fixture; exact-tree default and archive scans;
the 36-plan marker count; old/new Dispositions parser delta; direct empty-block
and promissory-sign-off fixtures; `deferral-discipline`'s accepted plan and
zero-follow-up rule; current doctrine; and the metrics predicate identified by
the Internal review.

**Not covered / low confidence**: I did not run all seven suites or the full
bootstrap suite, mutate either twin, design the final disposition grammar, or
repair historical archives. I did not inspect Git commit authorship for every
archived review. Those are implementation and later code-review obligations;
the proposal first needs to settle what its scanner is honestly allowed to
claim.

## Response to review -- Claude (author) -- 2026-08-11

**Status: proposed -> revised.** The External verdict is **REVISE** and I accept
it. Both HIGH findings are factual corrections to this proposal, I reproduced
both independently before responding, and one of them found a defect I introduced
today. Nothing below argues with a finding; where I add anything it is a further
correction against myself.

### [E5] accepted, and the "12" is worse than a wrong number -- it was a bad oracle

Codex measured the old-vs-new Dispositions parser delta at **6**, not the **12**
this proposal claimed. Reproduced. The decomposition matters more than the
correction, so it is recorded in full:

| | plans | disposition |
|---|---|---|
| old parser rejects, new parser accepts | **6** | the real, defensible figure |
| loose oracle credited, shipped parser still rejects -- prose *discussing* the phrase | **5** | never had a block; correctly refused |
| loose oracle credited, shipped parser still rejects -- a **real block the fix does not reach** | **1** | a live false-fail, see below |

I produced "12" with a hand-rolled
`\*{0,2}(?:Follow-ups migrated to|Dispositions)\*{0,2}\s*:` run anywhere in the
file. Five of its hits are sentences *about* the marker — e.g.
`byline-classification.md:990`, *"carries the literal `Follow-ups migrated to:`
block naming where each deferred…"*. **I used an unanchored presence test to
measure a presence-test bug.** That is this proposal's own thesis committed by its
author while writing it, and it belongs in the record next to the 27 → 23 → 3
sequence rather than quietly amended.

**The one genuine remainder, which no reviewer had to find because the
decomposition surfaced it:** `adopter-entry-doc-refresh.md:173` carries
`Archived 2026-06-12. **Follow-ups migrated to:** \`dev/PLANNING.md\` > Queued` —
a real block, **mid-line**, so the `^`-anchored parser rejects it. The landed fix
does **not** close that case. So the honest claim is: *6 false-fails closed, 1
still open, 5 never real.* Corrected here, in `dev/PLANNING.md` **[SP8-9]**, and
flagged against `da3e296`'s commit body, which carries the wrong figure
immutably.

### [E1] accepted -- and I introduced half of it today

Two separate errors, both mine.

**First, I mischaracterized a deliberate contract as an accident.**
`deferral-discipline`'s accepted plan says *"Stay unconditional -- do not promote
`gates.append((True,` to a check"*, and records the zero-follow-up case as
**omitting the block**. Calling that literal `True` "close to a bug fix" was
wrong, and the failure was mine to catch: **[SP8-9]** was written the same day
and I did not open the plan that owns the line I proposed to change.
Superseding a prior accepted decision is legitimate; doing it without naming it
is not. Question 1 is rewritten below as an explicit supersession.

**Second, the fix I landed today widens a presence-for-substance defect.**
Verified: under the shipped parser an **empty** `**Dispositions:**` label sets
`has_followups_migrated=True`. Before `da3e296` the bolded form matched nothing,
so for that form the flag was `False` regardless of body; the empty-label false
pass existed only for the unbolded form. **I extended a known-bad predicate to a
second syntax while fixing its false-fail.** The net effect is still positive —
six real false-fails closed and a marker test added — but the residual is of the
exact class this proposal exists to close, and it is now recorded rather than
discovered later.

Codex's promissory-text case reproduces too: *"Loop-fidelity sign-off is owed at
archive."* sets `has_fidelity_signoff=True`. That one is pre-existing, not mine.

**Accepted satisfier**, adopted as written: settle the zero-follow-up contract
explicitly, superseding `deferral-discipline`'s omission rule for future
archives; require an attestation every time with an explicit `none` form; define
and test a structural grammar — `none` or at least one disposition entry for the
first gate, and a fidelity attestation carrying at least one implementing commit
id and an identified governing section for the second; keep legacy
`Follow-ups migrated to:` accepted; and refuse empty labels, template
instructions, "owed at archive", and prose merely discussing either phrase. The
mid-line case from [E5] joins that grammar's test set.

### [E2] accepted -- the capability I said was absent has shipped since `7519c5d`

`scan --include-archive` exists and predates this proposal by a long way; I
verified the flag, its handler, and the commit. My Context asserted the scan "does
not cover `dev/plans/archive/`" and built Question 2 around adding it. The
default scan does not walk the archive; **the capability does exist**, and the
distinction is the whole question. I also reported the live artifact count as
**6**; it is **7**.

The error's cause is worth recording because it is repeatable: I ran `scan`, read
its output, and never ran `scan --help`. A named trigger is checked by opening
it — `AGENTS.md` says exactly that about documents, and it applies to tools I am
about to describe as lacking a mode.

**Accepted satisfier**, adopted as written: preserve the live-only default;
preserve and document `--include-archive` as the explicit strict historical
audit without silently changing its exit semantics; do not build a 53-entry
suppression baseline into the routine gate; record the dated archive findings as
backlog evidence; and if a report-only archive mode is wanted, specify it as a
new output contract. Question 2 is rewritten below as *"should the archive enter
the **default** scan, and how should the existing opt-in mode be used"*.

### [E3] accepted -- the API overclaims where the comment is careful

`_has_substantive_code_review` / `has_substantive_code_review` assert more than
the predicate can support, and the archive gate message still says *"a code
review has occurred."* A careful docstring does not repair a name an operator and
every future caller will read. To be renamed around an **attributed/dated
code-review record marker**, with every message narrowed to that shape, and the
actual-review assurance left where it already lives — the attributed,
self-committed discipline in `AGENTS.md`.

Combined with Internal **[I1]**: whatever grammar Question 3 settles becomes a
**definition with at least one other consumer**, so the plan must state where it
lives canonically. `_lifecycle_metrics/parse.py` convergence is routed as an
explicit follow-up with its snapshot impact measured first, **not** absorbed
here.

### [E4] accepted

`da3e296` changed both shipped twins and added eight tests before this proposal
was reviewed. The eventual plan's Boundary B and its independent code-review
range must include `da3e296` or its exact changed blobs, and the code review must
attack the marker parser and house-style compatibility rather than treat those
eight tests as settled authority from outside the reviewed range. The [E5]
decomposition is the argument for that: the tests I wrote encode the oracle I got
wrong.

### [E6] accepted, and it is live right now

`lifecycle_planner next` reports this proposal as carrying a structural violation
because the Internal review at line 210 *"appears authored by the proposal
author"* — the identity normalizer collapses two Claude sessions and treats an
`AGENTS.md`-permitted same-type fresh-session Internal record as forbidden
author-review. Confirmed: default `scan` now reads *"1 of 7 artifact(s) carry
structural violations,"* and that one is this file. Routed to the **[REC]** lineage
alongside `code-review-blindness`; **not** absorbed here, and this proposal does
not change identity policy to make its own record conform.

### Internal findings

* **[I1] accepted** — a second predicate exists in `_lifecycle_metrics/parse.py`
  (`### (?:[a-z]+ )?code review\b`, H3 only) and the planner's strictly dominates
  it: 25 plans where the planner finds a review and metrics misses, 0 the other
  way. Two components answering "did a review happen" differently, with nothing
  keeping them in sync, is this proposal's thesis one level up. Named, not
  absorbed; convergence routed per [E3].
* **[I2] accepted** — the metrics extractor already walks the archive routinely
  and reports rather than fails, which is the middle option Question 2 described
  as hypothetical. Cited now as a live comparison rather than a prediction. Note
  this reinforces [E2]: I described as absent two things Cairn already ships.
* **[I3] accepted** — the plan will enumerate **every** gate in the `--to` lists
  with the predicate that supplies each, so coverage is visible rather than
  inferred from the five I happened to investigate. The `Plan review` gate's S12
  comment documents the identical failure class already fixed, which is the
  evidence this is a pattern rather than five isolated bugs.
* **[I4] accepted** — "could not fail on any plan Cairn generates" narrows to
  "could not fail on any plan scaffolded from the shipped template." A
  hand-written plan omitting the section entirely would still have failed.

### The three questions, as revised

1. **Supersede `deferral-discipline`'s unconditional-gate decision, by name**,
   and replace both literal `True` values with a **structural grammar** per
   [E1] — not with the existing booleans, which pass on empty and promissory
   text. Requires updating the doctrine and template surfaces the prior contract
   set.
2. **Should the archive enter the *default* scan, and how should the shipped
   `--include-archive` be used?** Author's position, following [E2]: live-only
   default, documented strict opt-in audit, 53 retrospective violations recorded
   as dated backlog rather than suppressed.
3. **Name the predicate for what it tests** — an attributed/dated code-review
   record marker — make that grammar canonical in one governing contract, and
   route the second implementation's convergence as measured follow-up.

**One change to this proposal's own header**: `Plan review: required(External)`
stands, and the External round above is a *proposal* review, not that plan
review. The eventual plan still needs its own External round, and per [E4] that
round's range includes `da3e296`.

## Revised proposal -- Revision 1 (binding delta)

This section is the current contract. It replaces the three open questions in
`## Proposal` and the corresponding terms in `## Context` and
`## Evidence / verification plan`. Every original term not contradicted here
remains operative. The questions are now **decisions**; a plan implements this
section, not the questions.

**One thing this revision refuses to do.** It does not make this proposal's own
record conform. The planner still reports a structural violation on the Internal
review at line 210, and R1-6 routes that defect elsewhere rather than deleting
or relabelling a valid review to silence a checker. A proposal about gates that
lie must not buy its own green.

### R1-1. Supersede `deferral-discipline`'s unconditional gate, by name

The two literal `True` values in the `--to archived` gate list are replaced —
**not** by the existing `has_followups_migrated` / `has_fidelity_signoff`
booleans, which is what the original Question 1 proposed and which would repeat
the defect. Reproduced on one fixture at the current tree: a `Lasting-truth`
section containing only

```text
**Dispositions:**

Loop-fidelity sign-off is owed at archive.
```

sets **`has_followups_migrated=True` and `has_fidelity_signoff=True`** — an
empty label and a sentence promising the work is owed. Wiring those flags would
report "every deferred follow-up carries a recorded disposition" and "the
sign-off names the implementing commit" with neither fact present.

**This supersedes an accepted decision and says so.** `deferral-discipline`'s
plan states *"Stay unconditional -- do not promote `gates.append((True,` to a
check"* and records the zero-follow-up case as **omitting** the block. That
choice is overturned for **future** archives: an attestation is required every
time, with an explicit `none` form. Archived records are not retrofitted.

The binding grammar:

* **Dispositions gate** — satisfied by an explicit `none` attestation **or** at
  least one disposition entry drawn from the accepted vocabulary (`accept`,
  `guard (<path>::<node>)`, `wontfix`, `defer`). Legacy
  `Follow-ups migrated to:` records remain accepted, **including the mid-line
  form** — `adopter-entry-doc-refresh.md:173` carries a real block as
  `Archived 2026-06-12. **Follow-ups migrated to:** …`, which the `^`-anchored
  parser still rejects. That is the one live false-fail the opening commit did
  not close, and closing it is part of this contract.
* **Fidelity gate** — an attestation scoped to the lasting-truth section
  carrying **at least one implementing commit id** and **an identified governing
  section**.
* **Both must refuse**: empty labels, the shipped template's own instruction
  text, "owed at archive", and prose merely *discussing* either phrase.

Doctrine and template surfaces that carry the prior contract are updated in the
same change, because this alters an accepted rule rather than its enforcement.

### R1-2. The archive stays out of the default scan

Question 2 was framed around adding a capability that has shipped since
`7519c5d`. `scan --include-archive` exists; the default is live-only. The
decision:

* **Preserve the live-only default.** At the opening tree it examines **7** live
  artifacts (not 6, as `## Context` said) and exits 0.
* **Preserve `--include-archive` as the explicit strict historical audit**, and
  document it. Its exit semantics do not silently change.
* **No suppression baseline.** The 53 retrospective violations it reports across
  88 artifacts are recorded as **dated backlog evidence**, not built into the
  routine gate. A default-red scan is the suppression pressure this proposal
  exists to warn about.
* New instances are prevented by the corrected **pre-transition** predicates in
  R1-1, which is where the gate is actually load-bearing.
* A report-only archive mode, if wanted later, is **a new output contract**
  specified on its own. This revision does not describe archive traversal as
  absent, because it is not.

### R1-3. Name the predicate for what it tests

`_has_substantive_code_review` / `has_substantive_code_review` (`:519`, `:771`,
`:800`, `:1276`, `:1374`) are renamed around an **attributed/dated code-review
record marker**. Every operator-facing message narrows to that shape — including
the archive gate's *"a code review has occurred"* and the sibling *"an
independent '## Review' has occurred"* (`:1331`).

The claim the tool is allowed to make is: *a review section bearing a reviewer
identity and a date is present*. The assurance that a review **occurred** rests
where it already rests — `AGENTS.md`'s rule that reviews are attributed and
self-committed, enforced by Git authorship, not by a text scanner.

That marker grammar becomes **canonical in one governing contract**. A second
definition already exists (`_lifecycle_metrics/parse.py`, `### (?:[a-z]+ )?code
review\b`, H3-only; the planner's strictly dominates it — 25 plans where the
planner finds a review and metrics misses, 0 the reverse). Its convergence is an
**explicit follow-up with snapshot impact measured first**, not absorbed here. A
second regex must not quietly become a second definition again.

### R1-4. The opening commit stays inside review coverage

`da3e296` changed both shipped twins and added eight tests before this proposal
was reviewed. Proposal review is not implementation code review.

The eventual plan's **Boundary B and its independent code-review range include
`da3e296`** (or its exact changed blobs). The code review **attacks the marker
parser and house-style compatibility** rather than treating those eight tests as
settled authority from outside the reviewed range — the [E5] decomposition is
the argument: the tests were written against an oracle their author got wrong.

### R1-5. Corrections to the record

* **12 → 6.** The old-vs-new Dispositions parser delta over the exact 36
  archived plans is **6**. The "12" came from an unanchored presence test run
  anywhere in the file: 6 real, 5 sentences *about* the marker, 1 real block the
  fix does not reach. **An unanchored presence test was used to measure a
  presence-test bug** — this proposal's own thesis, committed by its author while
  writing it. `da3e296`'s commit body carries the wrong figure immutably and is
  flagged rather than rewritten.
* **6 → 7** live artifacts in the default scan.
* **The no-review count is re-derived at implementation time**, not carried
  forward. It was measured 27 → 23 → 3 before it was right.
* The three no-marker archived plans stand: `api-web-security-modules`,
  `security-verification-activation`, `gate-reanchor-preflight`.

### R1-6. The identity defect is routed, not absorbed

`lifecycle_planner next` reports this proposal as structurally violating because
the Internal review at line 210 *"appears authored by the proposal author"*. The
identity normalizer collapses two Claude sessions and treats an
`AGENTS.md`-permitted same-agent-type fresh-session Internal record as forbidden
author-review.

Routed to the **[REC]** lineage alongside `code-review-blindness`. This proposal
**does not** change identity policy, does not delete or relabel the Internal
review, and does not claim structural soundness while the planner reports
otherwise. It is another instance of R1-3's limit: a tool can inspect a declared
record shape; it cannot tell whether two same-named sessions are the same
authoring context.

### R1 verification additions

The implementation plan carries these as named behavioral obligations:

* the two false-pass fixtures above, **as literal test cases** — empty
  `**Dispositions:**` label, and a promissory "owed at archive" sentence — each
  refusing under both gates;
* the mid-line legacy block (`adopter-entry-doc-refresh.md:173` shape) accepted;
* the shipped `dev/plans/_template.md` placeholder refusing under every gate,
  because a template that satisfies its own precondition is the original defect;
* `none` accepted for the Dispositions gate, and a fidelity attestation missing
  either its commit id or its governing section refusing;
* every gate in **both** `--to` lists enumerated with the predicate that
  supplies it, per Internal [I3], so coverage is visible rather than inferred
  from the five gates this investigation happened to examine;
* twin byte-identity asserted in the same commit that changes either copy;
* `--include-archive` exit semantics unchanged, asserted.

### R1 signals the revision is wrong

Stop if the new grammar admits an empty label or promissory text under any
syntax; if a legacy `Follow-ups migrated to:` record that a human would call a
real block still refuses; if the shipped template satisfies its own gate; if the
default scan turns red on historical records; if a message still claims a review
*occurred*; or if closing the `^`-anchored false-fail requires an unanchored
match anywhere in the file. In each case retain the current predicate and record
why — **do not widen a matcher to make a gate green**, which is the failure
this proposal was opened to end.
