<!-- cairn-internal-ref-allow: doctrine/coordination.md doctrine/dual-review.md doctrine/lifecycle.md doctrine/plans.md doctrine/proposals.md doctrine/rationale.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
# A review-efficient lifecycle: bounded contracts, inherited plan readiness, and one stable evidence record

**Author**: Codex (Strategy)
**Model**: GPT-5 (Codex)
**Date opened**: 2026-08-10
**Status**: proposed
**Touches**: `doctrine/proposals.md`, `doctrine/plans.md`,
`doctrine/dual-review.md`, `doctrine/lifecycle.md`,
`dev/proposals/_template.md`, `dev/plans/_template.md`, their
`templates/core/dev/` twins, `tools/lifecycle.py`,
`tools/lifecycle_planner.py`, its installed twin, and lifecycle tests
**Related**: [`verification-evidence-boundaries`](../plans/archive/verification-evidence-boundaries.md),
[`board-drain-guards`](../plans/archive/board-drain-guards.md), and the
Maintainer's 2026-08-10 drafting direction to improve the proposal -> plan ->
implementation -> archive sequence without weakening review
**Plan review**: required(**External**) -- this changes Cairn's governing
lifecycle and its shipped enforcement, so it uses the high-assurance path it
proposes.

## Context

Cairn's review discipline is paying for itself. Independent reviewers have
found real security, correctness, and evidence defects that author sessions and
green suites missed. The answer is not fewer independent checks.

The present lifecycle nevertheless makes each check consume too much material.
Append-only proposal history is often repeated into a plan; plan-review
responses repeat operative chunk cells in amendment tables; later reviewers
read the original, every response, every amendment, the folded plan, and the
implementation record. Broad verification was also historically repeated at
implementation and review until `verification-evidence-boundaries` established
one stable integration record plus independent targeted falsification.

The scale is now large enough to impair review rather than merely inconvenience
it. Six recent plan files unaffected by the current dirty worktree total
**10,636 lines, as_of 2026-08-10**: `content-scan-detectors`,
`separator-detection`, `verification-evidence-boundaries`,
`dependency-advisory-coverage`, `release-security-orchestration`, and
`content-scan-url-classification`. The `content-scan-detectors` proposal and
plan total **58,160 words, as_of 2026-08-10**; the corresponding separator pair
totals **32,857 words**. Those records contain valuable reasoning, but a later
reviewer should not need to ingest all historical states to identify the
current contract.

This matters especially for scientific teams. Review time competes with model
development, data curation, and interpretation. A process that is robust only
when a scientist can repeatedly fund very large contexts will be abandoned or
performed ceremonially. The useful target is a lifecycle whose safety cost is
proportional to risk and whose evidence can be inspected without reconstructing
the entire argument.

## Proposal

Adopt a **review-efficient lifecycle contract** with five parts:

1. two assurance paths for proposal-worthy work;
2. a bounded current-contract target for every review;
3. plan-readiness inheritance for ordinary-risk work only;
4. stable evidence reuse through code review and correction;
5. a mechanical closeout preflight with no new substantive archive essay.

The proposal does not remove proposal review, Maintainer Decision authority,
or independent code review. It removes repeated review of unchanged material.

### 1. Assurance paths

Keep the existing direct-commit path for changes below proposal triage. A
proposal-worthy change declares one of two assurance paths:

| Path | Applies when | Required independent boundaries |
|---|---|---|
| **Standard** | Non-trivial work with bounded, reversible consequences and no high-assurance trigger | proposal review; plan review either inherited or distinct; independent code review |
| **High assurance** | A trigger below applies, or the author/reviewer cannot bound the effect confidently | proposal review; a distinct plan review; independent code review; any named ceremony review |

High-assurance triggers are:

* a security trust boundary, credential, executable path, untrusted-input
  parser, network boundary, or protected surface named in `AGENTS.md`;
* a scientific assumption, transformation, unit/CRS convention, numerical
  method, or data-selection rule that can change reported results;
* a destructive migration, data-loss risk, public compatibility break, or
  release/trust ceremony;
* a governing doctrine or lifecycle-enforcement change;
* an explicit escalation by a reviewer or the Maintainer.

A standard-path author may escalate at any time. A downgrade from high
assurance requires a recorded Maintainer Decision. Uncertainty about whether a
trigger applies resolves to high assurance.

Review tiers remain non-cumulative. A first-pass External review satisfies the
declared External floor without a preceding Internal pass. Internal and
External retain their different purposes; a second pass occurs when the first
review recommends it and the Maintainer chooses it, or when a separately
declared boundary requires it. This makes the existing recommend-and-decide
rule operational rather than allowing Internal + External to become an
unwritten default stack.

### 2. Every review names a bounded target

Every proposal, plan, and code review begins with a four-field review basis:

```text
Reviewed commit: <full commit id>
Target: <current-contract section, operative plan sections, or code range>
Prior findings: <ids being closed, or none>
Assurance path: <standard | high-assurance>
```

The basis is navigation, not permission to ignore relevant history. A reviewer
may open any prior section and must do so when a claim depends on it. The
default review input, however, is the named current contract plus the diff from
the last reviewed commit. A later review does not silently inherit an earlier
reviewer's claims: it either verifies them or names them as not covered.

Proposal history remains append-only. After responding to findings, the author
appends one **complete current-contract revision** that supersedes earlier
proposal content for implementation purposes. It states scope, invariants,
public paths, evidence, omissions, and deferred work without replaying the
argument. The earlier sections remain the deliberation record; the newest
complete revision is the thing a Decision and later reviewer can read as the
operative contract.

Plans use their existing mutability rule more directly. Before implementation,
accepted plan-review corrections are folded into the operative scope, chunk,
acceptance, and verification cells in place. The appended Response is a compact
finding-disposition table pointing to the changed sections and commit. It does
not reproduce replacement cells in an amendment ledger. Once a chunk is in
flight, its existing append-only sequence-revision rule still applies.

New blocking findings remain allowed at every review. Delta-focused does not
mean delta-blind: a correctness, security, scientific-validity, or scope defect
is blocking whenever found. A second-round reviewer who raises a new blocker
states the executed falsifier or the exact contract contradiction and names its
satisfier. Non-blocking precision improvements become follow-ups or explicit
`wontfix`, rather than forcing another full rewrite.

### 3. Standard plans may inherit a plan-readiness attestation

A proposal reviewer may add:

```text
Plan readiness: READY | DISTINCT REVIEW REQUIRED
Basis: <reviewed proposal commit and current-contract heading>
```

`READY` means the proposal already fixes all of the information a plan reviewer
would assess:

* scope and explicit exclusions;
* invariants, failure dispositions, public paths, and known omissions;
* affected test homes and standing gates;
* documentation and release-note surfaces;
* implementation areas and sequencing constraints;
* Maintainer fences and ceremonies, if any.

Only a **standard-path** proposal can receive `READY`. The Decision records the
same reviewed proposal commit and must not modify its contract. The resulting
plan declares:

```text
Plan review: inherited(<review commit>; proposal=<accepted commit>)
```

The plan may translate the accepted contract into file rows, commit chunks, and
progress markers. It may not introduce a new scope item, invariant, public
path, failure disposition, trust boundary, or ceremony. Any such addition
invalidates inheritance, changes the metadata to `required(<tier>)`, and stops
implementation until a distinct plan review lands.

High-assurance plans cannot inherit plan readiness. They retain a distinct plan
review because sequencing itself can create risk even when the proposal is
sound. A proposal reviewer can also require a distinct review for an ordinary
change whenever the execution outline is not mature enough.

This saves one review boundary only where that boundary has already been
performed against the exact accepted contract. It does not treat an author's
Response as review, infer readiness from a section's presence, or allow a plan
to self-attest.

### 4. One stable integration record survives review

Retain `verification-evidence-boundaries` unchanged as the execution model:

* Boundary A maps scoped tests and standing gates while iterating.
* Boundary B runs the broad integration suite once on a clean, stable commit.
* Boundary C validates that record and performs independent targeted
  falsification.

Clarify the correction path. When code review returns REVISE, the implementer
runs the finding's focused falsifiers while correcting. After the final
executable/test bytes settle, one replacement Boundary B record covers the
complete corrected range. The correction reviewer validates that record and
runs the prior falsifiers. It repeats the broad suite only when one of Boundary
C's existing six triggers fires.

Proposal responses, Decisions, review appendices, implementation-verification
records, and archive moves do not run the engine suite merely because they are
lifecycle transitions. They run their applicable claim, link, schema, and
record-conformance checks. A release or trust ceremony retains its own accepted
commands and never borrows this optimization.

### 5. Archive is validation and migration, not another argument

Add a read-only command:

```text
python tools/lifecycle.py closeout <plan> --dry-run
```

It reports, without editing:

* plan status and source proposal state;
* the accepted proposal commit and assurance path;
* plan-review satisfaction, including valid inheritance;
* the Boundary B record and reviewed implementation range;
* the latest code-review verdict and unresolved finding ids;
* deferred follow-ups lacking dispositions or durable homes;
* the exact files/board entries the archive transition must touch.

The command does not decide whether review was competent, summarize prose, run
tests, move files, edit the board, or commit. It is a completeness preflight,
not an authority source.

The archive record itself is restricted to five items: implementing commits,
the stable verification record, code-review verdict, residual dispositions,
and Decision-to-implementation loop fidelity. It points to existing sections
instead of retelling them. Once `closeout --dry-run` is clean and code review is
SHIP, archive requires no new review and no new broad test run.

### Tool support

Add a second read-only navigation command:

```text
python tools/lifecycle.py review-brief <artifact>
```

It emits the declared assurance path and tier, current-contract heading spans,
the last reviewed commit, outstanding finding ids, changed paths since that
commit, and any Boundary B summary. It extracts and points; it does not create
an AI summary, select evidence, or declare a gate satisfied.

`tools/lifecycle_planner.py` and its installed twin gain the minimum schema
needed to validate the review basis and inherited plan-readiness chain. The
existing exact review-record grammar work must land first; this proposal does
not share its dirty implementation window.

### Documentation / doctrine surface

The accepted design would update the lifecycle, proposal, plan, and dual-review
doctrine; the proposal and plan templates; Cairn's collaboration guidance; and
their shipped template twins. `docs/workflow-role.md` and the getting-started
workflow receive a concise user-facing explanation after the pilot proves the
shape. `CHANGELOG.md` records the adopter-visible lifecycle change.

This content is process prescription, so its canonical home is doctrine plus
the governing collaboration surface. The commands are described in tool usage
documentation; the proposal and plan remain the deliberation record.

### Doctrine-change rate-limit

This clears the goodnight-synthesis route. The 2026-08-05 handoff aggregated
repeated review and evidence friction across the security wave, including
duplicate full-suite execution, amendment tables that had to be folded back
into operative cells, repeated stale-figure remeasurement, and ceremonies whose
planned path set no longer matched the live held set. The dated measurements in
this proposal show that the recurrence has become an artifact-scale problem,
not a single inconvenient review.

## Pilot and measurement

Ship the contract as a **six-plan Cairn pilot** before publishing it as the
default adopter workflow. The pilot includes the first six eligible standard
plans opened after implementation. High-assurance plans continue through the
full path and serve as a safety comparison, not as quota fillers.

Record vendor-neutral process measures from git and command evidence:

* bytes in each declared review target plus its review diff;
* lifecycle transition commits and review rounds;
* broad-suite executions and elapsed time;
* Maintainer decision prompts;
* blocking findings by proposal, plan, and code-review boundary;
* any code-review blocker attributable to a contract issue a distinct plan
  review would reasonably have caught.

Do not claim model-billing tokens across vendors. Review-input bytes are the
portable proxy; elapsed command time is measured separately.

After six eligible plans, a short evaluation recommends **promote**, **revise**,
or **retire**. One high-severity escaped finding attributable to inherited plan
review pauses the pilot immediately. Two lower-severity instances also pause
it. Promotion requires a measurable reduction in review input and at least one
transition removed from inherited plans; safety findings and reviewer coverage
are reported alongside the savings, never hidden inside one score.

## Rationale

The proposal preserves Cairn's Registered Report analogy. Stage 1 still locks
the question, contract, and evidence before implementation; Stage 2 still tests
the implementation against it. The change is that an ordinary proposal whose
execution contract was already reviewed does not pay another reviewer to read
the same contract under a new filename.

For scientists, this improves three things:

* **attention** -- reviewers spend context on assumptions, data pathways, and
  falsification rather than record reconstruction;
* **reproducibility** -- every review and evidence claim names exact commits and
  ranges;
* **adoptability** -- ordinary work has a bounded path, while result-changing
  scientific and security work visibly retains higher assurance.

The proposal also respects the Maintainer's decision-rights floor. Agents own
mechanical closure, finding disposition, and evidence checks. The Maintainer is
asked for product direction, risk acceptance, downgrade of a high-assurance
trigger, and ceremonies requiring their authority -- not routine archive
bookkeeping.

## Alternatives considered

**Keep the lifecycle and only make the test suite faster.** Rejected. Boundary
B/C already addresses repeated broad execution. Most current cost is artifact
reconstruction and duplicate review, not pytest alone.

**Remove plan review for every plan.** Rejected. Sequencing creates independent
risk on security, scientific, destructive, and ceremony-bound work. Those
plans retain a distinct review.

**Combine proposal and plan into one universal artifact.** Rejected. It forces
detailed implementation planning before the Maintainer has accepted the idea
and bloats rejected proposals. Plan-readiness inheritance gains the useful part
without erasing the decision/execution distinction.

**Summarize old records with an AI-generated digest.** Rejected as authority.
A lossy summary can hide the exact condition a reviewer needs. `review-brief`
extracts headings, commits, findings, and ranges; the authored current contract
remains authoritative.

**Hard word or token caps.** Rejected. High-risk work sometimes needs space,
and vendor token accounting is not portable. Bounded targets, no repeated cells,
and measured review-input bytes address the cost without rewarding omission.

**Make every External review follow an Internal review.** Rejected as an
automatic rule. The tiers have different purposes, but the existing doctrine
already makes a second structurally independent pass a recommend-and-decide
choice. High-assurance work can still require both explicitly.

**Do nothing.** Rejected. A method scientists cannot afford to execute reliably
will be bypassed, which is less safe than designing an honest lower-cost path.

## Evidence / verification plan

### Tests required

* Extend `bootstrap/tests/test_lifecycle_contract.py` with the two assurance
  paths, exact inherited-review commit chain, invalidation on changed accepted
  commit, refusal for high assurance, and refusal when a standard plan expands
  its declared contract.
* Extend lifecycle CLI tests for `review-brief` and `closeout --dry-run`,
  including malformed records, unresolved findings, missing dispositions,
  stale Boundary B evidence, and output escaping.
* Preserve byte identity between `tools/lifecycle_planner.py` and
  `templates/skills/_lib/lifecycle_planner.py`.
* Run the canonical full suite once at the final stable implementation boundary
  because this changes a shipped lifecycle gate.

### Examples / smoke checks

* Exercise one standard READY fixture end to end from accepted proposal through
  plan execution eligibility and closeout preflight.
* Exercise one high-assurance fixture and prove inheritance is refused.
* Run `scripts/check_cairn.py`, claim checks over every changed deliberation and
  doctrine file, link checking, lifecycle scan, and the doctrine/template drift
  checks.

### Docs required

* Doctrine and template surfaces named above.
* Tool usage for the two read-only commands.
* A concise workflow explanation for adopters after pilot evaluation.
* `CHANGELOG.md > Unreleased > Changed` when the adopter-visible contract is
  promoted.

### Author-accounting -- invariants, failure modes, edge cases

| Claim | Enforcer / evidence |
|---|---|
| High-assurance work never inherits plan review | parser refusal plus high-assurance fixture |
| An inherited review binds exact accepted proposal bytes | full commit ids in review, Decision, and plan metadata; mismatch fixture |
| A plan cannot knowingly expand the inherited contract | explicit invalidation rule, review checklist, and negative fixtures for declared additions; semantic completeness remains reviewer-checked |
| External review is not replaced by an author's Response | reviewer-authored READY record and existing authorship gate |
| Stable test evidence covers exact executable bytes | unchanged Boundary B/C commit and range checks |
| Closeout cannot grant authority or mutate state | read-only implementation and mutation-sentinel tests |
| Historical reasoning remains available | proposal append-only rule and git history; review-brief only points |

**Known omissions.** No parser can prove that a plan's prose is semantically
identical to a proposal. The mechanism binds exact source bytes and rejects
declared expansions; independent code review and the trusted-contributor model
remain the backstop for a concealed expansion. The pilot is specifically meant
to test whether this residual is acceptable.

## Signals the change is wrong

* A high-assurance plan reaches execution through inherited review. Stop and
  revert inheritance before further implementation.
* Code review finds a high-severity contract or sequencing defect that a
  distinct plan review would reasonably have caught, or two lower-severity
  examples occur during the pilot. Pause inheritance and evaluate.
* Reviewers still need to read the whole artifact history to determine the
  current contract. The current-contract grammar or review brief is inadequate;
  revise before promotion.
* The process saves transitions but shifts unresolved decisions to the
  Maintainer. Revise the decision-rights routing; that is not an efficiency win.
* Review-input bytes or elapsed time do not materially fall for eligible plans.
  Retire the added mechanism rather than keeping complexity that does not pay.

## Reviewer brief

An External reviewer should attack the classification boundary first: find a
standard-path change whose sequencing could alter scientific results, widen a
trust boundary, or create irreversible loss. Then attack whether READY can be
invalidated reliably when a plan adds semantic content that the parser cannot
recognize. Finally, assess whether the six-plan pilot can detect a safety
regression with a sample that small.

## Advisory read -- Claude (Implementation) -- 2026-08-10

**This is not the declared review and does not discharge any tier.** It is filed
under a heading that deliberately does **not** match the review-pass grammar, so
no gate can read it as satisfying the `required(**External**)` floor. The
Maintainer has a second, independent review in hand.

**Conflict of interest, stated first because it should discount everything
below.** I am structurally a different agent type from the author, so I would
*qualify* as External. I should not count as it: I authored most of the artifacts
whose scale this proposal measures (including the 3,422-line
`content-scan-detectors` plan in its evidence), and I have been the party
enforcing the discipline it relaxes. Both directions of bias are live.

**Recommendation: accept, with F1 fixed before implementation and F2/F3 folded
in.** The proposal identifies the right cost driver and keeps the boundaries that
have been paying for themselves.

### What reproduces

Every headline measurement was re-derived independently:

| claim | measured | verdict |
|---|---|---|
| six plans total **10,636 lines** `as_of` 2026-08-10 | 10,636 | **exact** |
| separator pair **32,857 words** | 32,857 | **exact** |
| `content-scan-detectors` pair **58,160 words** | 58,156 | **reproduces** (4 words; that plan is under concurrent edit) |

A proposal about evidence discipline whose own evidence reproduces. Noted because
the opposite has been common in this repo: figures went stale within single
sessions all last week.

### [F1 -- blocking] The pilot's eligible population may be empty, so the evaluation gate never fires

The pilot is defined as "the first six eligible **standard** plans opened after
implementation," and promotion/retirement is decided "after six eligible plans."
But the high-assurance triggers include any security trust boundary, executable
path, untrusted-input parser, protected surface named in `AGENTS.md`, **or a
governing doctrine or lifecycle-enforcement change**.

Measured against the 11 plans currently in `dev/plans/` — by keyword proxy, which
is suggestive rather than a classification — **every one** carries heavy trigger
signal. The two lowest, `transition-lint` and `review-gate-enforcement`, are both
themselves lifecycle-enforcement changes, which is an explicit trigger.

So the plausible eligible population today is **zero**. The failure mode is not
"weak evidence" but *no* evidence: the mechanism lands in doctrine, the evaluation
condition never becomes true, and inheritance sits unmeasured indefinitely. That
is worse than either adopting or rejecting it, because it looks decided.

**Remedy** — make the condition falsifiable. Either time-box it ("after six
eligible plans **or 60 days, whichever comes first**", where an empty sample is
reported as a finding about trigger breadth rather than as silence), or run the
pilot against a deliberately narrowed trigger set and state which triggers were
relaxed for the pilot only. As written, "six eligible standard plans" cannot be
shown to have failed.

### [F2 -- important] The current-contract revision needs a withdrawal ledger

The single complete current-contract revision is the proposal's biggest win. But
nothing requires it to state **what it drops**. A constraint silently absent from
the newest revision is invisible unless a reviewer diffs it against every prior
state — which is exactly the reconstruction cost this proposal exists to remove.
Append-only preserves the words and loses the signal.

**Remedy** — require the revision to carry an explicit **withdrawn / superseded**
list: each earlier commitment it drops, and why. Precedent from this repository,
2026-08-05: `content-scan-url-classification`'s Revision 1 withdrew the
proposal's point 1 outright, and the *explicit* withdrawal is the only reason its
reviewer could evaluate the current design rather than an abandoned one. Without
that line the reviewer would have reviewed a mechanism already dead.

### [F3 -- important] Inheritance invalidation catches declared expansions; the undeclared case is the real risk

The proposal is honest here — *"No parser can prove that a plan's prose is
semantically identical to a proposal"* — and names independent code review as the
backstop. The gap is that the backstop is **unbound**: nothing requires the code
reviewer to affirm the no-expansion property, so "code review is the backstop" is
true but unexercised.

**Remedy** — make it an attested checklist item: the code reviewer states, with a
named basis, that the plan introduced no new scope item, invariant, public path,
failure disposition, trust boundary, or ceremony. That converts an assumed check
into a recorded one.

This is a failure shape with a fresh precedent worth citing, because it was mine:
in `review-gate-enforcement` I bound the legacy-manifest *digest* to the raw
heading line and left the *selection* running through a permissive parser, then
assumed the strict half covered the loose one. The 2026-08-10 code review
reproduced three headings that cleared both gate surfaces while matching no exact
grammar. A strict component does not make a permissive neighbour safe.

### Two smaller notes

* **Dependency chain length.** The tool work correctly sequences behind the exact
  review-record grammar. That plan carries an open REVISE under active
  sharpening, so this proposal's benefit sits behind: grammar sharpening → its
  code review → this implementation. Worth stating in the plan so the delay is
  expected rather than discovered.
* **Reconcile with the gate's code-review blindness.** Found 2026-08-10: the
  shipped review-record gate filters to `## Plan review` and never evaluates
  `## Code review`, so a code review declaring `**Findings**: raised` with no
  disposition passes unflagged. This proposal adds a review-basis block to code
  reviews; if the gate is widened to that section kind, those fields become
  gate-checkable there. The two changes touch the same predicate and should not
  be designed independently.

### What I could not assess

Whether the classification boundary holds against a *standard-path* change whose
sequencing could alter scientific results — the reviewer brief's first question. I
have no scientific-domain case in this tree to test it against; every candidate
here is security or lifecycle. That question needs the declared reviewer, and it
is the one I would weight highest after F1.
