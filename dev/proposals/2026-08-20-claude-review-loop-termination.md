# Give the review loop a termination condition

**Author**: Claude (Strategy)
**Model**: claude-opus-5 (Claude Opus 5)
**Date opened**: 2026-08-20
**Status**: revising
**Assurance path**: **standard** — this changes deliberation doctrine and the
lifecycle templates. It touches no executable trust root, no install contract,
no frozen surface, and ships no code. It does change what a reviewer is
permitted to certify, which is why it takes a review rather than an edit.
**Touches**: `dev/proposals/_template.md` and its shipped twin;
`dev/plans/_template.md` and its shipped twin; `doctrine/plans.md`;
`doctrine/dual-review.md`. Two optional tooling items are named and
deliberately **not** in scope (see *Alternatives*).
**Related**: measured against the three artifacts opened 2026-08-19/20 —
`suite-run-diagnostics`, `full-suite-interception`, `metrics-events-not-prose`;
`dev/PLANNING.md` > "Agent-facing discipline does not survive delegation";
`doctrine/rationale.md` > "How the doctrine evolves under evidence".
**Plan review**: not required(this is four doctrine edits and two template
edits, single-area, no sequencing, no deferred follow-ups — the plan triage
rule's own skip case). If a reviewer disagrees, the escalation is theirs.

## Context

**The Maintainer's report, which is the reason this exists:** the process "has
slowed remarkably," is "caught in endless review loops," and is "preventing real
improvements."

Measured across the three artifacts opened on 2026-08-19 and 2026-08-20:

| | |
|---|---|
| Deliberation written | **11,169 lines** across six artifacts |
| Review rounds | **25** |
| Code shipped | **124 lines** |

Ninety lines of prose per line of code. One review round per five lines.

**The review work is not the problem.** Ninety-four findings were raised across
those 25 rounds and **not one was false, refuted, or withdrawn**. Every finding
was a real defect. Three would have shipped broken behaviour: a guard that
destroyed another plugin's diagnostic, a contract requiring tests that could not
be constructed, and an activation cutoff that would have stranded concurrent
commits.

So this proposal does not argue for less review. It argues that the review is
being carried in a container that costs more than the review does, and that the
loop has no condition under which it stops.

**Three mechanisms produce the cost.**

**1. The contract is re-typed in full, every round.** `dev/proposals/_template.md`
requires each Response to append "one complete current contract … Not a delta and
not a diff." Across the three proposals that restatement is roughly 2,600–3,200
lines — about **28% of everything written**.

That restatement is not free in defects either. Three of today's blocking
findings were sections *silently lost during the mandated rewrite*. The rule
written to prevent drift was producing it.

**2. The toll buys a bridge that was never open.** Complete restatement exists so
an External reviewer can record `Plan readiness: READY` and let the derived plan
take a lighter Internal pass. In the eleven review rounds across these two
proposals that record the field, the value was `DISTINCT REVIEW REQUIRED`
**eleven times out of eleven**. Zero grants. The toll was paid every round for a
bridge closed from the first.

**3. Narrow rounds can clear.** Fourteen of the 25 rounds narrowed their
`Target:` to the previous round's findings, and reviewers routinely prescribed
the next round's scope. Two of the only three clean passes in the entire corpus
were terminal rounds scoped to two findings each. A reviewer certifying a delta
they can diff is not certifying the artifact — which is why defects surfaced in
order of *adjacency* rather than severity. A round-4 review found three blocking
findings in a region four earlier rounds had never visited.

**And the question that would have prevented today's stall is on nobody's
list.** *Can the evidence this contract demands actually be produced?* It was
asked for the first time **after** `suite-run-diagnostics` was accepted and
archived — and the answer was no. That plan has 1,027 lines and has shipped
nothing, because its accepted contract requires falsifiers its own guards make
unconstructible. Closing it took an amendment to an archived artifact.

## Proposal

### 1. Complete restatement once, at the end — not every round

**Now** (`dev/proposals/_template.md`): every Response appends one complete
current contract.

**Proposed**: each Response appends (a) the full text of every section this round
**changes, adds, or withdraws**; (b) a `### Section manifest` naming **every**
section of the current contract in reading order, each tagged `new` / `revised` /
`carried from R<k>` / `withdrawn`; and (c) the existing withdrawal ledger,
unchanged. A section appearing in neither the manifest nor the ledger **refuses**
at `lifecycle_planner.py scan`. A `carried` section is in force with byte-exact
earlier text; rewording it makes it `revised` and it appears in full.

**One exception, load-bearing: the last revision before the Decision is one
complete self-contained contract**, exactly as today. That is the document the
Maintainer signs and the plan binds. It stays whole.

### 2. A narrowed round may raise findings. It may not clear the artifact.

**Now**: any round may return a clearing verdict, whatever its `Target:`.

**Proposed**: `Target:` stays, as the record of what was read closely. Two rules
join it. **(a)** A round whose Target is narrower than the whole operative
contract may raise findings but **may not record a clearing verdict** — SHIP,
ACCEPT, PASS or `READY` requires a whole-contract read. **(b)** A reviewer does
not set the next round's scope.

### 3. Constructibility is declared before a proposal reaches the Maintainer

**Now**: the template names required tests. Nothing asks whether they can be
built.

**Proposed**: no proposal reaches `awaiting-decision` until one review round
records a `Constructibility:` block. For each falsifier or fixture the contract
requires, it names **the route that produces it** — which process writes it,
which reader observes it, which of the design's own guards it passes through. An
item with no route is recorded `no admitted route` and is **blocking** at
whatever round it appears. `Constructibility: asserted` is not a record. The
same block is required at plan `ready-to-implement`.

### 4. Correct the false price on the plan layer

**Now** (`doctrine/plans.md`): *"When in doubt, open the plan. The cost is low
(one file in `dev/plans/`)."*

**Proposed**: keep *"when in doubt, open the plan"* — plan review caught two of
the three real defects and must not be discouraged. Replace the cost claim with
the measurement: **three plans cost 4,705 lines across eight review rounds — 588
lines per round, higher than the proposals they derived from.** In the same
place, surface the two de-escalation routes that already exist and were used in
none of these three: `Plan review: not required(<rationale>)` straight to
`ready-to-implement`, and the quickstart's trivial-accept collapse.

## Rationale

**The container costs more than the contents.** Ninety-four real findings is a
healthy yield. Eleven thousand lines to carry them is not. Changes 1 and 4
attack volume; 2 and 3 attack termination.

**Changes 1 and 2 must ship together or neither ships.** Shrinking the revision
while still letting narrow briefs clear would leave reviewers certifying deltas.
Change 2 costs a round per artifact; it is the insurance that makes change 1
safe.

**Change 3 is the one every analysis kept.** Four independent designs proposed
it and eight adversarial passes left it standing. It is also the cheapest: one
block, one round, and it converts the most expensive failure mode available —
discovering after acceptance that the contract cannot be built — into a question
asked before.

**Restatement is also a detector, which is why change 1 does not delete it.**
One of today's findings was caught precisely because the plan reproduced a rule
next to its divergence. Byte-exact carrying keeps the detector and removes the
erosion.

## Alternatives considered

**Delete the plan layer for code changes.** Rejected on evidence. The claim that
motivated it — that proposal review found none of the real defects — is false
and was checked: finding Z1, raised in a *proposal* round, is the
`env = os.environ.copy()` fix that shipped. Every one of today's 124 shipped
lines traces to a proposal-round blocking finding. Plan review separately caught
two of the three severe defects. Neither layer is dead weight.

**Cap rounds at a fixed number.** Rejected: a cap terminates the loop by
truncation rather than by convergence, and the round that would be cut is
unknowable in advance. Change 2 makes rounds converge instead; change 3 removes
the most common cause of a late one.

**Two tooling items, deliberately out of scope.** A `claim_check --self-consistency`
mode (row counts checked against the table they describe; one token counted two
ways in one document) would retire most of the apparatus findings in the plan
layer. A landed-pass count on `lifecycle_planner board` would give the Maintainer
a *how deep is this loop* number at session start. Both are an afternoon each and
bind nothing. They are named here so they are not lost, and excluded so this
proposal stays decidable on its doctrine changes alone.

## Evidence / verification plan

Prose-only; no pytest mapping. The applicable gates are `claim_check.py`,
`link_check.py`, `scripts/check_cairn.py`, and
`scripts/quality_gate.py --sub neutrality` over the two shipped template twins.

| claim | how a reviewer checks it |
|---|---|
| 11,169 lines / 25 rounds / 124 lines shipped | `wc -l` the six artifacts; count `^## .*[Rr]eview` sections; `git diff --stat a316d75~1..HEAD -- 'bootstrap/tests/conftest.py' 'scripts/quality_gate.py'` |
| 94 findings, none false | read the review sections; the classification is the load-bearing number and should be re-derived, not accepted |
| `DISTINCT REVIEW REQUIRED` 11/11 | `grep -o "Plan readiness.*" <the two proposals> \| sort \| uniq -c` |
| restatement ≈ 28% of all lines | section-boundary line counts per artifact |
| 14 of 25 rounds narrowed their Target | read each `Target:` field |
| plan layer at 588 lines/round | `wc -l` the three plans; count their review sections |
| Z1 shipped | `grep -n "Z1" dev/proposals/archive/2026-08-19-claude-full-suite-interception.md`, then compare to `scripts/quality_gate.py` |

**This proposal is deliberately short.** A 2,000-line proposal arguing that
proposals are too long would refute itself, and the restraint is part of the
claim: the operative contract above is four rule changes, and everything else
here is evidence for them. If a reviewer finds it under-specified, that is a
finding worth having — it is the first test of whether the discipline this
proposes is livable.

## Signals the change is wrong

* **A defect ships that a full restatement would have caught.** Change 1's
  central bet is that byte-exact carrying preserves the detector. If a carried
  section turns out to conceal a drift that a rewrite would have exposed, the
  bet is wrong.
* **Round counts do not fall**, or fall while findings-per-round rises — meaning
  the same defects are being found later rather than fewer defects existing.
* **Change 2 costs more than one round per artifact.** It is priced as
  insurance; if it doubles round counts it is a tax instead.
* **`Constructibility:` becomes a ritual.** If blocks start reading "each
  falsifier is constructible by writing it," the mechanism has been defeated and
  is worse than nothing, because it will be cited as assurance.
* **A reviewer cannot tell what the current contract is** without reassembling
  it from a manifest and four earlier rounds. That is the failure mode change 1
  risks, and the Decision-time complete contract is the mitigation. If reviewers
  report assembling difficulty *before* that point, the mitigation is
  insufficient.

## Revision 1 -- Claude -- 2026-08-20 (Maintainer-directed reframing)

**No review has landed; this revises the opened contract on the Maintainer's
own diagnosis, which is better than the one the proposal opened with.** Quoted
verbatim and visually isolated:

> "I don't want the 'REVISE' and 'SHIP' labels to be treated like they need the
> reviewer to get to 'SHIP'."

> "in peer review, the reviewers don't make the decision to accept a
> manuscript, the editor (or associate editor) does."

### What this reframing exposes

**Cairn has an editor for proposals and none for plans or code.** A proposal
ends at `awaiting-decision`, which is the Maintainer's. But the plan and code
lifecycles have no such state:

```
awaiting-plan-review <-> revising-plan -> ready-to-implement
  -> implementing -> awaiting-code-review <-> revising-code
```

A plan review's verdict moves the artifact directly. A code review's verdict
moves the artifact directly. **The reviewer holds the gate.**

That is the loop's actual generator, and it is a structural asymmetry rather
than anyone's failing. If clearing requires satisfying the reviewer, and every
review round finds real defects — 94 of them, none false — then no natural
stopping point exists. The reviewer is not obstructing; they have been handed a
decision that is not theirs to make.

**Observed today, four times.** The Maintainer closed a Security Review by
fiat, converted a plan-review tier mid-flight, directed a clearing round be
skipped, and finally stopped the process outright. Each read as an exception.
Each was the editor function asserting itself through a hole in the lifecycle.

### The change this replaces

**Change 2 is withdrawn.** It proposed that a narrowed round may raise findings
but *may not record a clearing verdict* — which makes the reviewer's verdict
**more** load-bearing, in a process whose defect is that the reviewer's verdict
is load-bearing at all. It was a refinement of the wrong structure. Under the
editor model it is unnecessary: no round clears anything, narrow or wide, so
there is nothing to restrict.

### The change that replaces it

**2'. A review recommends; the Maintainer disposes.** Plan review and code
review each gain a disposition step, mirroring the proposal lifecycle:

* A review records **findings** and a **recommendation** — the existing
  vocabulary (`PASS` / `REVISE` / `SHIP`) is retained but reclassified as
  advisory. A reviewer never moves the artifact.
* The artifact moves on a **Maintainer disposition**: `accept as-is`,
  `accept with named changes`, or `return for revision`. The Maintainer may
  accept over a `REVISE`, and may return an artifact a reviewer passed.
* A disposition accepting over open findings **names them and their standing
  state**, so acceptance is a recorded judgement rather than an omission. This
  proposal's own sibling plan carries a worked example: a Security finding left
  open, its exact residual shape measured and pinned by a test that asserts the
  limit as it actually behaves.
* **The reviewer keeps the finding; they lose the veto.** Nothing here reduces
  what a review may say, and no finding is erased by a disposition.

### Why this is the stronger proposal

The original four changes attacked volume and asked the loop to converge faster.
This one gives the loop a **terminator**: a role whose job is to stop it. Peer
review has run on that separation for three centuries, and for the reason that
applies exactly here — a reviewer optimises for what could still be wrong, which
is unbounded, while an editor optimises for whether it is good enough to
proceed, which is a decision.

Changes 1, 3 and 4 stand unaltered. They reduce what the loop costs per turn;
2' is what ends it.

### Consequence for the count

The proposal is now **three changes plus one replacement**, not four. That is a
smaller contract than the one it opened with, which is the correct direction for
a proposal arguing that contracts are too large.

## Revision 2 -- Claude -- 2026-08-20 (Maintainer-corrected: plans do not loop)

**Still no review landed.** The Maintainer corrected the model again, and the
correction is simpler than both prior versions. Quoted verbatim and visually
isolated:

> "For plans, there is no editor. It's just
> Plan->Review->Revise->Execute->Code Review->Dispositions (if any)->Archive"

> "No reviewer gates on second rounds, except maybe a security review"

### What was wrong with Revision 1

Revision 1 proposed giving plan review and code review an **editor disposition
step**, mirroring the proposal lifecycle. That was over-built. It accepted the
premise that plans loop and tried to add a terminator to the loop.

**Plans are not supposed to loop at all.** A plan gets one review. The author's
revision closes it. Execution follows. There is no clearing round to seek and no
editor needed, because there is nothing to adjudicate between rounds — there are
no rounds.

### The operative model

```
Plan -> Review -> Revise -> Execute -> Code Review -> Dispositions (if any) -> Archive
```

**One review. One revision. Then work.**

* **A reviewer does not gate a second round.** The verdict vocabulary
  (`PASS` / `REVISE`) records what the reviewer found; it does not hold the
  artifact. A `REVISE` is answered by revising, and the answer closes it.
* **The single exception is a Security Review**, which may take a second round
  on a trust surface. That is the one place where "the author says it is fixed"
  is not sufficient, because the failure mode is silent.
* **`Dispositions (if any)`** is where the editor function lives, and it lives
  there **once** — at code review, for findings that will not be fixed. Not
  between plan-review rounds, because there are none.

### Why this is the right shape and Revision 1 was not

The plan is a *translation* of an already-accepted contract into sequenced work.
The deliberative weight sat on the proposal, which has an editor and a Decision.
A plan review's job is to catch translation errors before code is written — a
single pass, and the pass is either useful or it is not.

Rounds two through four exist only because a reviewer who has not been satisfied
can hold the artifact. Remove the hold and they do not arise. Today's evidence is
exact: `metrics-events-not-prose` took **four** plan-review rounds and the fourth
found three blocking findings in a region the first three never visited — which
is not convergence, and no number of further rounds would have made it so.

**A consequence worth stating plainly: with no second round, the author's
revision is the last prose check before code exists.** That raises the stakes on
the revision rather than lowering them, and it is the correct place for the
stakes to sit — the next check after it is code review, which reads executable
bytes rather than a description of them.

### Standing contract after this revision

**Change 1** (restatement once, at the end) — unchanged.
**Change 2'** (editor disposition for plans and code) — **withdrawn**. Replaced
by the single-pass model above.
**Change 3** (constructibility declared before the Maintainer's Decision) —
unchanged, and now load-bearing: it is the check that a single-pass plan review
most needs, because there is no second pass to catch a contract that cannot be
built.
**Change 4** (correct the false price on the plan layer) — unchanged.

Three changes and one model correction. The contract has shrunk at every
revision, which for this proposal is the argument.

### Addendum to Revision 2 -- where a loop is allowed, and why

One further Maintainer correction, quoted verbatim:

> "I don't mind if code review enters a bit of a loop"

**Plan review is single-pass; code review may loop.** That asymmetry is not a
compromise, it is the whole principle stated in one line: **a loop is allowed
where the artifact is executable.**

| stage | loops? | why |
|---|---|---|
| Proposal | yes, bounded by the Decision | the Maintainer is the editor and terminates it |
| Plan review | **no** — one pass | prose about work not yet done; a second reader finds a different set, not a smaller one |
| Code review | **yes** | the artifact runs; findings are reproducible; a clean pass is a real result rather than a failure of effort |

The reason a prose loop does not converge and a code loop does: on prose,
"nothing further to say" is indistinguishable from "did not look hard enough,"
so a reviewer with more time always produces more findings. On code, a finding is
a behaviour you can make happen, its absence is a probe that came back clean, and
the reviewer's own measurement tells them when to stop.

Today's corpus shows both. Four plan-review rounds on `metrics-events-not-prose`
produced escalating find counts in regions earlier rounds had never entered. The
code review of the guard, by contrast, produced three findings anchored to
reproductions — and the most valuable of them was that **a test could not fail**,
which is only discoverable by running it.

**Consequence for change 3.** Constructibility is declared before the Decision
precisely so the single-pass stage is not the one asked to catch an unbuildable
contract. The loop that would have caught it is the one that no longer runs
there.

## Review -- Codex (External) -- 2026-08-21

**Model**: GPT-5.6 (Codex)

Reviewed commit: 997bf2212b78111cc38c49eb1388cf579d3d9671
Target: the complete current contract: opened proposal plus Revision 1, Revision 2, and its code-review-loop addendum
Prior findings: none
Assurance path: standard
**Tier**: External
**Findings**: raised (3 blocking)
**Plan readiness**: DISTINCT REVIEW REQUIRED

### Steelman

The proposal correctly distinguishes the value of finding defects from the cost
of repeatedly carrying the same deliberation. Its strongest observation is the
asymmetry in the addendum: executable code can be probed to a clean result,
whereas another prose pass can simply discover a different adjacency. Keeping
code-review iteration while seeking a single, constructive plan-review pass is
therefore a more disciplined response than capping review or discarding it.

### Findings

#### RLT-01 — BLOCKING: the proposed fail-closed rules require new executable enforcement, but the proposal excludes it

Change 1 says an omitted section *refuses at* `lifecycle_planner.py scan`; Change
3 bars both `awaiting-decision` and plan `ready-to-implement` without a
Constructibility record. The current planner and its shipped twin contain no
`Section manifest` or `Constructibility` parser/validator, and the current
state gates therefore cannot enforce either claim. The proposal nonetheless
declares only doctrine/template touches, "ships no code," no pytest mapping,
and no plan required.

Revise the operative scope to include the planner and its byte-identical twin,
the lifecycle-contract tests, and the needed template/doctrine changes. Give
those new checks a test mapping and re-triage this as a non-trivial plan: it now
changes executable state gates across proposal and plan lifecycles, not one
prose area.

#### RLT-02 — BLOCKING: the single-pass model does not specify a valid lifecycle transition or its Security exception

Revision 2 says a blocking plan review goes `Plan -> Review -> Revise ->
Execute`, but does not state which status transition the author's revision
makes, what record proves it, or how the planner distinguishes that ordinary
return from the retained Security second round. Today `revising-plan` returns
only to `awaiting-plan-review`; `ready-to-implement` requires a clearing review,
and the reviewer's commit carries both transitions. Code review is likewise
described as looping with dispositions "if any," without saying when a reviewer
clears, when the Maintainer disposes open findings, or which state owns each
move.

State the complete proposal/plan/code transition tables, including status owner,
commit carrier, evidence predicate, and the Security-review return arm. The
new planner rules and their negative fixtures must be derived from that table;
otherwise "one review" is an aspiration that conflicts with the shipped state
machine.

#### RLT-03 — BLOCKING: the section-manifest contract has no stable identity or comparison rule

`carried from R<k>` does not identify a section within a revision, prove
byte-exactness, or tell a scanner which earlier headings remain commitments
rather than superseded history. A manifest can name whatever its author wants;
without a closed section identity and resolution rule, the claimed refusal for
a silently omitted section cannot distinguish omission from an unlisted or
renamed section. This is the central safety argument for reducing restatement,
so it cannot be deferred to implementation taste.

Specify the manifest grammar: a stable section identifier, the exact source
revision/commit and section it carries, the byte-exact comparison (or digest),
withdrawal linkage, and the complete-set algorithm. Include positive and
negative fixtures for a missing, renamed, edited-carried, duplicate, and
withdrawn section. That provides the constructible route Change 3 itself asks
for.

### Coverage

Covered: the proposal's entire current contract and all revisions; current
planner transition and gate code (`PLAN_TRANSITIONS`, `_gating_preconditions`,
and `_STATUS_MOVES_WITH`); the proposal/plan templates; and the lifecycle-plan
status doctrine. `rg` found neither `Section manifest` nor `Constructibility`
in the planner or its shipped twin; the only repository hit was an unrelated
test comment. Not covered: the proposal's historical line/finding counts were
not re-derived, because the executable-contract omissions already block a
Decision. Second-round recommendation: **recommended** after a complete current
contract supplies the missing enforcement and transition specification.
