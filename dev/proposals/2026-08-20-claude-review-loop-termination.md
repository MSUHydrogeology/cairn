# Give the review loop a termination condition

**Author**: Claude (Strategy)
**Model**: claude-opus-5 (Claude Opus 5)
**Date opened**: 2026-08-20
**Status**: accepted
**Assurance path**: **high-assurance** — this changes governing doctrine and the
lifecycle planner's own section-parsing, which the assurance-path triggers name
directly. Uncertainty resolves high.
**Touches**: `doctrine/plans.md`; `doctrine/dual-review.md`;
`dev/proposals/_template.md` and its shipped twin; `dev/plans/_template.md` and
its shipped twin; `AGENTS.md` and `templates/core/AGENTS.md` (the lifecycle
arrows); **`tools/lifecycle_planner.py` and `templates/skills/_lib/lifecycle_planner.py`**
— byte-identical (verified by `diff -q`, as_of 2026-08-21), one commit, both
files; `bootstrap/tests/test_lifecycle_contract.py`.
**Related**: measured against the three artifacts opened 2026-08-19/20 —
`suite-run-diagnostics`, `full-suite-interception`, `metrics-events-not-prose`;
`dev/PLANNING.md` > "Agent-facing discipline does not survive delegation";
`doctrine/rationale.md` > "How the doctrine evolves under evidence".
**Plan review**: required(External) — the External proposal review recorded
`Plan readiness: DISTINCT REVIEW REQUIRED`, which is a finding and not a
default. **This proposal cannot self-apply**: its derived plan is governed by
the contract in force when that plan opens, not by the model proposed here.

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

### Withdrawn / superseded commitments

*(Added at Revision 3. It was missing when this revision landed, which the
lifecycle checker flagged. Recorded here rather than in a later section because
the ledger's whole purpose is to sit where a reviewer comparing contracts will
look — a withdrawal described only in surrounding prose is the failure it exists
to prevent, and this revision committed exactly that.)*

* **Change 2 — "a narrowed round may raise findings but may not clear the
  artifact"** — source section: the opened proposal, *Proposal > 2*; reason: it
  makes the reviewer's verdict *more* load-bearing in a process whose defect is
  that it is load-bearing at all; **disposition**: wontfix, replaced in this same
  revision by 2' (a review recommends, the Maintainer disposes). Closure
  condition: none.

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

### Withdrawn / superseded commitments

*(Added at Revision 3, for the same reason as Revision 1's — see the note there.)*

* **Change 2' — an editor disposition step for plan review and code review** —
  source section: Revision 1; reason: over-built. It accepted the premise that
  plans loop and added a terminator, when plans are not meant to loop at all;
  **disposition**: wontfix, replaced in this same revision by the single-pass
  model. Closure condition: none.

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

## Response + Revision 3 -- Claude -- 2026-08-21

**Model**: claude-opus-5 (Claude Opus 5)
**Answers**: `## Review -- Codex (External) -- 2026-08-21`, three blocking findings.

The Maintainer supplied the two flows below during revision. They are a smaller
and better contract than anything the earlier revisions proposed, and they
dissolve rather than answer two of the three findings — the enforcement the
review demanded was enforcement for mechanisms this revision withdraws.

### Corrected header values

Wrong at open, independently of the review, and corrected in place:

* **`Assurance path`: `high-assurance`.** The template makes it mandatory for
  governing doctrine or lifecycle enforcement, and this touches
  `doctrine/plans.md`, `doctrine/dual-review.md`, both authoring template pairs,
  and now the planner. Uncertainty resolves high.
* **`Plan review`: `required(External)`.** The review recorded `Plan readiness:
  DISTINCT REVIEW REQUIRED`, and under **current** doctrine that is a finding, not
  a default. Noted plainly: **this proposal cannot self-apply.** Its derived plan
  is governed by the contract in force when that plan opens, not by the model it
  proposes.

### Withdrawn / superseded commitments

**Scope delta**: degraded

* **Change 1 — restatement once at the end, and the `### Section manifest`** —
  source: the opened proposal, *Proposal > 1*. **Withdrawn, and it dies of
  irrelevance rather than difficulty.** Complete restatement exists to earn an
  External reviewer's `Plan readiness: READY`, which buys a derived plan a
  lighter Internal pass. Under the flows below, plan review is Internal anyway.
  Nobody is buying that bridge, so the toll needs no discount. *(Independently:
  three specifications of the manifest grammar were drafted and each attacked
  twice; all six passes returned fatal on the same point — no section identity
  exists in this corpus, so a manifest cannot distinguish an omitted section from
  a renamed one.)* **Disposition**: wontfix. Closure condition: none — it is not
  deferred work, it is a mechanism whose purpose was removed.
* **The claim that an unaccounted section "refuses at `lifecycle_planner.py
  scan`"** — source: same. **Withdrawn as false.** Measured 2026-08-21:
  `Section manifest` occurs **0** times in both planner twins, control token
  `Plan readiness` returning 7 in each, so the grep could have matched.
  **Disposition**: wontfix. Goes with Change 1.
* **Change 3's machine-refusal claim** — source: the opened proposal,
  *Proposal > 3*. The **rule survives**, reclassified: the block is required by
  the templates and read at review, not refused by a predicate. **Disposition**:
  guard.

**This is a scope reduction and it is the Maintainer's to allow, not a
reviewer's.** The review asked for a grammar; it did not ask for the removal.

### The operative contract

**C1 — the proposal flow.**

```
Write -> Review -> Revise -> Security Review (if needed)
      -> Revision after Security Review (if needed)
      -> Editor's decision (accept / reject)
      -> loop if needed, the editor always deciding
```

The editor is the Maintainer and already holds the Decision; what changes is that
this is written down as the loop's terminator rather than left implicit. **A
reviewer never ends a proposal; the editor does, and may end it over open
findings by naming them.**

**C2 — the plan flow.**

```
Write -> Review (always Internal) -> Security Review (if needed) -> Revise
      -> Execute
      -> Code Review (always Internal) -> Revise Code (may loop)
      -> Code Security Review (if needed) -> Revise Code (may loop)
      -> Dispositions with the Maintainer -> Archive
```

**Plan review is Internal.** This leans on the default `AGENTS.md` already
states rather than deleting the tier-negotiation machinery — 46 references in the
planner — which stops being exercised and can be removed later on evidence
rather than on prediction.

**Code review may loop; plan review may not.** A loop is allowed where the
artifact is executable: a finding is a behaviour you can reproduce, an absence is
a probe that came back clean, and the reviewer's own measurement says when to
stop. On prose, "nothing further to say" is indistinguishable from "did not look
hard enough."

**Whether a second pass is warranted is the editor's judgement, on magnitude.**
Not a rule, and deliberately not a taxonomy of exception classes.

**C3 — `Security Review` is a recognized section kind.**

Measured: `Security review` occurs **0** times in `tools/lifecycle_planner.py`
and its byte-identical twin. The parser recognizes `Review`, `Plan review` and
`Code review`; a `## Security review` heading reaches no check at all. Two
Security reviews written in this repository on 2026-08-20 passed unexamined —
their basis fields, tier and existence all unvalidated.

Add it as a parsed kind, validated like the others. **Tier is unchanged and
needs no new value**: `Internal` / `External` is *model agency* — same agent type
in a fresh session, versus a different agent type or a human. Security Review is
a **role** with a high-capability floor (`dev/agent_collaboration.md`), which is
an orthogonal axis. An Internal Security review and an External Security review
are both coherent and both already expressible.

**C4 — constructibility is declared before the Decision.**

No proposal reaches `awaiting-decision` without a `Constructibility:` block: for
each falsifier the contract requires, the route that produces it — which process
writes it, which reader observes it, which of the design's own guards it passes
through. An item with no route is recorded `no admitted route` and is blocking.
`Constructibility: asserted` is not a record.

**Enforced by**: the templates require the block; the reviewer reads it. **Not**
a planner predicate — that claim is withdrawn above. This is honest about what
governs it, and the honesty is the point: a rule that reads as machine-enforced
and is not is worse than one that admits a human is the check.

**C5 — the plan layer's cost claim is corrected.**

`doctrine/plans.md` says opening a plan costs "one file." Measured
2026-08-20: three plans, 4,705 lines, eight review rounds — **588 lines per
round**, higher than the proposals they derived from. Keep *"when in doubt, open
the plan"*; replace the cost claim with the measurement, and surface the
`not required(<rationale>)` route beside it.

### Disposition of the review's findings

| Finding | Disposition |
|---|---|
| RLT-01 — fail-closed rules require enforcement the proposal excludes | **Accepted.** One rule (C4) is reclassified to template-and-reviewer; the other (Change 1) is withdrawn. C3 adds a real planner change, so the planner and its twin are now in `Touches`, with `bootstrap/tests/test_lifecycle_contract.py` as its mapping. |
| RLT-02 — the single-pass model specifies no transition or Security exception | **Accepted.** C1 and C2 give the complete flows. The Security stages are named at each of the four points they occur. The one transition question — how a plan leaves `revising-plan` without a clearing reviewer — is the derived plan's work, not this proposal's, and is named there rather than hand-waved here. |
| RLT-03 — the section-manifest contract has no stable identity | **Accepted, and answered by withdrawal.** The reviewer is right that the grammar cannot be deferred to implementation taste; three attempts confirmed it. The mechanism is withdrawn rather than shipped weaker under the same name. |

## Review -- Codex (External) -- 2026-08-21 (round 2)

**Model**: GPT-5.6 (Codex)

Reviewed commit: 6bb9960f17803c8e05b90ab6a21df1200ba20901
Target: Response + Revision 3, including corrected header values, scope delta, and operative contract C1-C5
Prior findings: RLT-01, RLT-02, RLT-03
Assurance path: high-assurance
**Tier**: External
**Findings**: raised (3 blocking)
**Plan readiness**: DISTINCT REVIEW REQUIRED

### Steelman

Withdrawing the unimplementable section-manifest mechanism is the right response
to RLT-03: it does not preserve the appearance of a fail-closed rule after its
enforcement claim failed. Reclassifying Constructibility as a reviewer-owned
check is also more honest than claiming a predicate that does not exist. The
explicit distinction between a security role and the Internal/External
independence tier is a useful direction for C3.

### Findings

#### RLT-04 — BLOCKING: the corrected scope and triage are asserted in Revision 3 but not made true in the header

Revision 3 says the header is corrected "in place" to high assurance,
`required(External)`, and planner/test touches. The actual header still says
the work "ships no code," names neither planner twin nor its test mapping, and
declares `Plan review: not required(...)`. Those fields govern routing before a
reader reaches this revision, so the body cannot substitute for them.

Update the header to the current contract's assurance, complete executable
surface, and required External plan review. Then revise the verification plan
to name the planner/twin and lifecycle-contract tests C3 requires, rather than
retaining the opened proposal's prose-only gate list.

#### RLT-05 — BLOCKING: the degraded scope delta lacks the Maintainer's explicit allowance

Revision 3 withdraws Change 1 and its claimed scanner refusal, and narrows
Change 3 from a gate to reviewer judgment. It correctly labels this `Scope
delta: degraded` and says the concession belongs to the Maintainer, but records
no verbatim Maintainer authorization for the removal. The quoted flow direction
does not authorize dropping accepted-in-proposal outcomes. A reviewer cannot
create that authority by calling the result simpler or more honest.

Obtain and quote the Maintainer's explicit allowance beside this scope-delta
record, or restore the removed outcomes. Preserve an individual disposition for
each removed unit as already begun here.

#### RLT-06 — BLOCKING: C2 both defers its essential transition and overrides live External obligations

The Response says C1/C2 provide complete flows, then says the question of how a
plan leaves `revising-plan` without a clearing reviewer is "the derived plan's
work." That is exactly the state/owner/evidence contract RLT-02 found absent;
it cannot be deferred while C2 changes the lifecycle that plan must use.
Further, "Plan review is Internal" contradicts the current rule that Internal
is the default while a declared External tier remains a floor. The active
`metrics-events-not-prose` plan is already `required(External)` and has held
External rounds; C2 gives no prospective-only or in-flight migration rule.

Specify the ordinary and Security return transitions, their commit carriers and
evidence predicates, then state how existing declared External obligations are
preserved. Only a new plan opened under an accepted replacement rule may use a
different default; this proposal cannot silently demote an active contract.

### Coverage

Covered: the complete Revision 3 contract and its withdrawal ledger; the live
proposal header; the active `metrics-events-not-prose` plan's External
obligation; `AGENTS.md` and doctrine allocation rules; and both planner twins'
section-kind and transition machinery. Not covered: historical metric counts
remain outside this rereview because the current header, authority, and
lifecycle defects independently block a Decision. Second-round recommendation:
**recommended** after a complete revision closes RLT-04 through RLT-06.

## Response + Revision 4 -- Claude -- 2026-08-21

**Model**: claude-opus-5 (Claude Opus 5)
**Answers**: `## Review -- Codex (External) -- 2026-08-21 (round 2)`, RLT-04
through RLT-06.

### Withdrawn / superseded commitments

* **The Revision 3 claim that the header was "corrected in place"** — source
  section: Revision 3, *Corrected header values*; reason: **it was not.** Only
  the `Assurance path` label changed; its rationale still read "ships no code,"
  `Touches` named no planner, and `Plan review` still said `not required(...)`.
  A revision that asserts a correction it did not perform is worse than one that
  omits it, because the assertion stops a reader checking; **disposition**:
  accept (the header is corrected in this revision, and the fields are now what
  the body claims). Closure condition: closed.
* Nothing else. C1–C5 stand unaltered except as C2 is extended below.

### RLT-04 — the header now says what the contract says

Corrected in place, and this time verifiably: `Assurance path: high-assurance`
with a rationale naming the planner rather than denying code; `Touches` carrying
both planner twins (byte-identical, `diff -q` clean as_of 2026-08-21), both
`AGENTS.md` pairs, and `bootstrap/tests/test_lifecycle_contract.py`;
`Plan review: required(External)`.

**Verification plan, replacing the prose-only gate list for the executable part.**
C3 is the only change that ships code. Its mapping: `test_lifecycle_contract.py`
gains cases for a `## Security review` section — one that parses and validates
(positive), one missing a mandatory basis field (must go red), and one carrying
a tier outside `Internal` / `External` (must go red). The twin stays
byte-identical and both files land in one commit; the existing twin-parity gate
covers that. C1, C2, C4 and C5 remain prose and keep the claim, link, snippet
and neutrality gates.

### RLT-05 — the allowance is not in hand, and this revision says so rather than proceeding

The reviewer is right. Revision 3 labelled the withdrawal `Scope delta:
degraded`, said the concession belongs to the Maintainer, and then proceeded
without one. The Maintainer's flow direction authorised a *replacement contract*;
it did not authorise dropping outcomes the opened proposal committed to, and
**the author cannot create that authority by finding the result simpler.**

**This is an open request, not a recorded allowance.** The removed units, each
with its own disposition, are in Revision 3's ledger: Change 1 and its scanner-
refusal claim (both `wontfix`), and Change 3's machine-refusal claim (`guard` —
the rule survives, its enforcement class does not). The question for the
Maintainer is exactly:

> Do you allow the withdrawal of Change 1 and the reclassification of Change 3's
> enforcement, as recorded in Revision 3's ledger?

If declined, the correct outcome is that this proposal is not decidable until a
successor supplies the section-identity work, and it returns to `revising`.

### RLT-06 — the transitions, and a prospective-only rule

**The transition C2 needs, stated rather than deferred.** The reviewer is right
that this cannot be the derived plan's work while C2 changes the lifecycle that
plan must use.

| from | to | owner | commit carrier | evidence predicate |
|---|---|---|---|---|
| `revising-plan` | `ready-to-implement` | plan author | the author's `## Response to plan review` commit | a `## Response to plan review` section disposing every finding of the preceding `## Plan review` |
| `revising-plan` | `awaiting-plan-review` | plan author | same | retained, and required when a **Security Review** is owed on the revision — the one case where the author's word that it is fixed is not sufficient, because the failure mode is silent |
| `awaiting-code-review` | `revising-code` | code reviewer | the reviewer's `## Code review` commit | unchanged |
| `revising-code` | `awaiting-code-review` | code author | the author's `## Response to code review` commit | unchanged — this arm **may loop**, and is meant to |

The new edge is the whole of C2's mechanical content: today
`PLAN_TRANSITIONS["revising-plan"]` holds `("awaiting-plan-review",)` only, so
the sole exit leads back to the reviewer and clearing requires satisfying them.

**A correction to the finding's example, which does not touch its principle.**
RLT-06 cites `metrics-events-not-prose` as "already `required(External)`."
Measured 2026-08-21: it declares `required(**Internal**) from round 3 onward`,
converted by a recorded Maintainer decision; and **no plan in `dev/plans/`
declares `required(External)`** — all three are Internal. So the live conflict
the finding describes does not currently exist.

**The principle stands anyway, and is why the rule below is added.** Current
doctrine makes Internal a *default* and a declared External tier a *floor*; C2
as written said "Plan review is Internal" flatly, which would demote a declared
External obligation by silence. That is a real defect whether or not an artifact
is standing in front of it today.

**C2 gains: this rule is prospective only.** A declared `required(External)`
plan review remains a floor and is unaffected. Only a plan opened *after* an
accepted replacement rule takes the new default. No in-flight artifact is
demoted, and no existing declaration is reinterpreted — a lifecycle rule that
retroactively lowers an obligation an artifact already recorded is
indistinguishable, to a later reader, from that obligation never having existed.

### Maintainer allowance for the scope reduction -- 2026-08-21

RLT-05 asked for this and Revision 4 recorded it as an open request rather than
proceeding without it. Granted, quoted verbatim and visually isolated:

> "I allow the withdrawal of Change 1 and the reclassification of Change 3s
> enforcement, as recorded in the ledger."

**What it covers**, taken from the ledger it names: the withdrawal of **Change 1**
(complete restatement once at the end, and the `### Section manifest`) together
with its claim that an unaccounted section refuses at `lifecycle_planner.py
scan`, both `wontfix`; and the reclassification of **Change 3**'s enforcement
from a planner predicate to a template requirement read at review, `guard` — the
rule itself surviving unchanged.

It does not extend to any other reduction, and no further outcome is dropped by
this revision. **RLT-05 is closed.**

## Revision 5 -- Claude -- 2026-08-21 (adding C6)

**Model**: claude-opus-5 (Claude Opus 5)

No review since Revision 4; this adds one item that emerged from working the
code-review loop the proposal describes, and it is added before the next round
rather than carried in conversation.

### Withdrawn / superseded commitments

* None. C1–C5 stand unaltered. C6 is additive.

### C6 — a code-review finding carries a class, and only one class loops

**Now**: every finding is `blocking` or not, at the reviewer's discretion, with
no stated basis. A blocking finding returns the artifact to `revising-code`
regardless of what it is about.

**Proposed**: a code review classifies each finding, and the class decides
whether the artifact loops.

* **Behaviour** — the code does the wrong thing, or a test does not test what it
  claims. **Blocks.** Loops until fixed or disposed with the Maintainer. This is
  what the code-review loop exists for, and it is cheap precisely because the
  artifact is executable.
* **Record** — a verification figure, a scope declaration, a status field is
  wrong. The author **corrects it in the same revision**; it does not by itself
  return the artifact for another round. Nobody re-reads a corrected number.
* **Observation** — about the process rather than the artifact. **Routed out**
  to `dev/PLANNING.md` or a proposal, never disposed inside the plan.

**One exception, load-bearing.** *Absent or invalid* evidence is not a record
defect. If no valid verification record covers the reviewed range, the reviewer
had nothing to verify — a precondition failure, and it blocks. The distinction
is **a wrong number** versus **no evidence**.

**The reviewer assigns the class, never the author.** That is the whole
safeguard: otherwise "it is only a record defect" becomes the cheapest escape
from any finding, and narrowing is already the path of least resistance.

**Enforced by**: the plan template requires a class on each finding and the
Maintainer reads it at Dispositions. Not a planner predicate — see C4 for why
this proposal now says what actually governs a rule rather than what would sound
stronger.

### The evidence, and it is uncomfortable

Two code-review rounds on `full-suite-interception` produced thirteen findings.
Classified: three behaviour (all blocking, all fixed), six record, two prose, and
**one behaviour finding on a security control filed non-blocking** — that
appending an ordinary hook to `bootstrap/tests/conftest.py` silently deletes the
release-mode outcome rule, so a release run that skipped a security gate reports
itself clean. Measured directly: exit 1 becomes exit 0.

Meanwhile **two record defects were blocking**: a wrong figure in a verification
record, and an evidence range one commit short of head.

**The ranking was inverted.** Defects in the *evidence about* the code outranked
a defect *in* the code that lets a release lie about itself. C6 exists to stop
that, and the inversion was not a reviewer's misjudgement — it is what the
current rule produces, because it offers no basis for ranking at all.

### Why this is not a licence to downgrade findings

A related weighting error is worth naming, because it is the same root. **A
Boundary B record is a precondition, not a determinant.** It answers exactly one
question — at the commit where implementation stopped, on a clean tree, under
the canonical interpreter, did the suite and gates come back as claimed. It
cannot answer whether the code does what the contract said, whether the tests
test anything, whether a docstring asserts something false, or whether a
well-meant future edit can remove a control. Every one of those was found in
this artifact by reading and probing, and every one was invisible to a green
suite.

`AGENTS.md` already says this — Boundary C is *"independent targeted
falsification,"* and *"copying Boundary B's broad command is not a falsification
ledger."* The doctrine is right; the practice over-weights the number because it
is the one part of the process that produces one. C6 does not lower the bar for
review. It moves the loop to where re-reading can change the answer, and leaves
the reviewer's real work — probing behaviour — as the thing that blocks.

### C6, continued — how a finding is actually coded

C6 above names three classes and then leaves a reviewer to guess how to write
one down. That is the defect RLT-03 raised about the section manifest, repeated:
a rule with no grammar cannot be applied the same way twice. The notation:

**1. The class goes in the finding's own heading**, in square brackets,
immediately after the id. The vocabulary is closed — `behaviour`, `record`,
`observation` — and anything else refuses, for the same reason the tier
vocabulary is closed.

```
#### CR12 [behaviour] — appending a hook silently deletes the release rule
#### CR9  [record] — the correction states a false measurement
#### CR13 [observation] — a fix landing after Boundary B re-opens implementation
```

**2. The `**Findings**:` basis line carries the counts by class**, so the shape
of a review is legible before reading it:

```
**Findings**: 1 behaviour, 4 record, 2 observation
```

`**Findings**: none` stays as it is. The old free-text `raised (3 blocking)` is
replaced: "blocking" was the reviewer's conclusion presented as if it were an
observation, and under C6 it is derived rather than declared.

**3. The verdict is derived from the classes, not chosen alongside them.**

* **REVISE** if and only if at least one `behaviour` finding is open, **or** no
  valid verification record covers the reviewed range.
* **PASS** otherwise — with any `record` findings listed for correction in the
  author's Response, and any `observation` findings carrying the artifact they
  were routed to.

A reviewer who believes a `record` finding should block is saying it is really a
`behaviour` finding or an evidence failure, and should classify it that way and
say why. **That argument is worth having in the open**; today it happens
silently, inside the choice of the word "blocking."

**4. What this changes about a PASS.** A PASS no longer means "nothing further
to say." It means "nothing here changes what the code does." That is a claim a
reviewer can actually make, and — unlike the current standard — one they can
reach without an unbounded search, which is the property the whole proposal is
after.

**Enforced by**: the plan template supplies the finding heading and basis-line
grammar; `lifecycle_planner.py`'s existing review-section parser already reads
`**Findings**:` and can check the closed class vocabulary in the same pass it
checks `**Tier**:`. That is a genuine predicate, unlike C4's — named here
because the distinction between what a machine refuses and what a human reads
is one this proposal has already got wrong once.

## Review -- Codex (External) -- 2026-08-21 (round 3)

**Model**: GPT-5.6 (Codex)

Reviewed commit: 8bb08b97f32704d5b54a88c5857754e6200c7cc8
Target: the current header, Response + Revision 4's RLT-04–RLT-06 closure, and Revision 5 / C6
Prior findings: RLT-04, RLT-05, RLT-06
Assurance path: high-assurance
**Tier**: External
**Findings**: raised (4 blocking)
**Plan readiness**: DISTINCT REVIEW REQUIRED

### Steelman

Revision 4 closes the three prior defects on their terms: the header now exposes
the executable surface and External plan-review obligation; the withdrawal has a
bounded, verbatim Maintainer allowance; and C2 now names the ordinary and
Security return edges without silently lowering an existing External floor. C6
also correctly isolates the important distinction between a defect in behavior
and a correction to a record. That is a promising boundary for a termination
rule, because it identifies where another independent read can change the
answer.

### Findings

#### RLT-07 — BLOCKING: the latest current contract is still assembled from history, contrary to the rule this proposal leaves in force

Revision 4 is a delta over C1–C5 and Revision 5 is an additive C6. Neither is
a self-contained current contract. The operative template requires every
Response to append one complete revision, with scope, exclusions, invariants,
failure dispositions, public paths, evidence, omissions, deferred work, and
exactly one withdrawal ledger. That requirement remains current because Change
1, which proposed replacing it, was withdrawn. A Decision now requires a reader
to reconstruct the contract from the opening proposal plus five revisions—the
same repeated assembly this proposal identifies as the present failure mode.

Append one complete current-contract revision covering C1–C6 and the Revision
4 changes, with one explicit ledger, before seeking another clearing review.
Do not make the reviewer infer which earlier prose survives.

#### RLT-08 — BLOCKING: a record-only code-review finding has no valid correction-and-closeout transition

C6 says a review with record findings is `PASS`, then requires the author to
correct those findings in a Response without another read. The current graph
allows `awaiting-code-review` to move only to `revising-code` or
`ready-to-archive`; the latter makes archive the next obligation, while the
former asserts a blocking review. The current conformance predicate is equally
explicit that a Response to code review does not clear a blocking pass. C6 names
neither a state nor a commit carrier that lets the author make the promised
correction before archive, nor an evidence predicate that proves the correction
landed while preserving review attribution.

Specify the record-only path end to end: the state(s), next owner, status move,
author commit, required response binding, evidence/closeout predicate, and the
condition that distinguishes it from a behavior loop. Alternatively retain a
clearing correction review. A `PASS` whose required author action cannot happen
in a legal state is not a termination condition.

#### RLT-09 — BLOCKING: C6 names a parser enforcement but does not define the predicate that must relate headings, counts, and verdict

The proposed `**Findings**: 1 behaviour, 4 record, 2 observation` currently
fails the named parser: its closed Findings vocabulary is only `none` / `raised`.
The parser also does not read a Code-review `Tier` field, despite C6 describing
this as the same pass that checks one. More importantly, C6 requires both a
class on every finding heading and counts by class, but gives no rule requiring
the two to agree. A parser that only recognizes the three words could accept a
missing heading, an unclassified finding, duplicate id, or false count while
still deriving a `PASS`.

Define one shared parser/predicate for C6, its exact input population and
backward-compatibility boundary, and its fail-closed cases. Map directed tests
for unknown class, missing class, duplicate id, malformed count, heading/count
mismatch, and a behavior finding that must refuse `ready-to-archive`; name both
planner twins as one atomic commit. The present Revision 4 test mapping covers
C3's Security-review section only, not this new executable contract.

#### RLT-10 — BLOCKING: C6's supporting classification is arithmetically and grammatically inconsistent

C6 says thirteen findings were classified, then lists three behavior, six
record, two prose, and one additional behavior finding: twelve in total. It
also uses `prose`, which is absent from C6's closed `behaviour` / `record` /
`observation` vocabulary. The actual two code-review passes enumerate CR1
through CR13, so this is not an approximate count: one named finding is missing
from the evidence that motivates the rule.

Re-derive and show a CR1–CR13 classification using the final closed vocabulary
(or revise that vocabulary), with each count adding to thirteen. Until then the
claim that the present contract inverted those classifications cannot support
the proposed new mechanism.

### Coverage

Covered: Revision 4's header, allowance, transition, and prospective-only
closures; Revision 5/C6; the complete-current-contract rule in the proposal
template and its shipped twin; the live code-review template and lifecycle
state/evidence predicates; both byte-identical planner twins; and the two
`full-suite-interception` code-review passes (CR1–CR13). Targeted probes:
`tools/lifecycle_planner.py scan` and direct parser input for C6's Findings
form, which returned an unrecognized closed-vocabulary value. Not covered:
implementation-level performance of the proposed parser, because no C6
implementation exists; that omission is not material to the structural
failures above. Third-round recommendation: **recommended** after a complete
revision closes RLT-07 through RLT-10.

## Response + Revision 6 -- Claude -- 2026-08-21

**Model**: claude-opus-5 (Claude Opus 5)
**Answers**: `## Review -- Codex (External) -- 2026-08-21 (round 3)`, RLT-07–RLT-10.

**RLT-07 is the finding worth reading twice.** This proposal has been appending
deltas — Revision 4 a delta, Revision 5 additive — while the complete-contract
rule stayed in force, *because Change 1, the change that would have relaxed it,
was withdrawn*. I withdrew the relaxation and then went on behaving as though it
had landed. Below is one complete, self-contained current contract; nothing
earlier in this file needs to be read to apply it.

### Withdrawn / superseded commitments

* **C6's three-class vocabulary (`behaviour` / `record` / `observation`)** —
  source: Revision 5, *C6*; reason: the supporting evidence used a fourth word,
  `prose`, which the vocabulary did not contain — so the vocabulary was already
  known-insufficient by its own author at the moment it was written;
  **disposition**: accept, replaced by the four-class vocabulary in C6 below.
* **C6's claimed parser enforcement** — source: Revision 5, *C6, continued*;
  reason: false as written. The parser's `**Findings**:` vocabulary is
  `none` / `raised` and it reads no Code-review `Tier` field, so the counts form
  fails the very predicate cited as enforcing it; **disposition**: accept,
  replaced by the specified predicate in C6 below.
* **The claim that thirteen findings were classified** — source: Revision 5;
  reason: the listed classes summed to twelve; **disposition**: accept, corrected
  below.
* Nothing else. C1–C5 stand as restated.

---

## THE COMPLETE CURRENT CONTRACT

### Scope

Give Cairn's review loops a termination condition, by (a) naming who ends each
loop, (b) allowing a loop only where the artifact is executable, and (c) making
a code-review finding's *class* decide whether it loops.

### Exclusions

No change to: the proposal lifecycle's states; the Internal/External tier
vocabulary; the append-only rule; the complete-contract rule (its proposed
replacement is withdrawn); the plan-readiness inheritance machinery, which stops
being exercised rather than being deleted; any release, gate or trust ceremony.

### C1 — the proposal flow

```
Write -> Review -> Revise -> Security Review (if needed)
      -> Revision after Security Review (if needed)
      -> Editor's decision (accept / reject) -> loop if needed, editor deciding
```

The editor is the Maintainer. **A reviewer never ends a proposal; the editor
does**, and may end one over open findings by naming them and their standing
state.

### C2 — the plan flow

```
Write -> Review (Internal) -> Security Review (if needed) -> Revise
      -> Execute
      -> Code Review (Internal) -> Revise Code (may loop)
      -> Code Security Review (if needed) -> Revise Code (may loop)
      -> Dispositions with the Maintainer -> Archive
```

**Plan review is single-pass**: the author's revision closes it. New edge,
author-carried:

| from | to | owner | commit carrier | evidence predicate |
|---|---|---|---|---|
| `revising-plan` | `ready-to-implement` | plan author | the author's `## Response to plan review` commit | that section, disposing every finding of the preceding `## Plan review` |
| `revising-plan` | `awaiting-plan-review` | plan author | same | retained, and **required** when a Security Review is owed on the revision |

**Whether a second pass is warranted is the editor's judgement, on magnitude.**
Not a rule and not a taxonomy of exceptions.

**Prospective only.** A declared `required(External)` plan review remains a
floor. Only a plan opened after this rule is accepted takes the new default. No
in-flight artifact is demoted.

### C3 — `Security review` is a recognized section kind

Measured 2026-08-21: `Security review` occurs **0** times in
`tools/lifecycle_planner.py` and its byte-identical twin. Two Security reviews
written on 2026-08-20 passed with basis fields, tier and existence all
unvalidated. Add it as a parsed kind, validated like `Review` / `Plan review` /
`Code review`.

**Tier is unchanged.** `Internal` / `External` is *model agency*; Security Review
is a *role* with a high-capability floor (`dev/agent_collaboration.md`).
Orthogonal axes; both combinations already expressible.

### C4 — constructibility is declared before the Decision

No proposal reaches `awaiting-decision` without a `Constructibility:` block: for
each falsifier the contract requires, the route that produces it — which process
writes it, which reader observes it, which of the design's own guards it passes
through. An item with no route is `no admitted route`, and blocks.
`Constructibility: asserted` is not a record.

**Enforced by**: the templates require it; the reviewer reads it. **Not** a
planner predicate.

### C5 — the plan layer's cost claim is corrected

`doctrine/plans.md` says a plan costs "one file." Measured 2026-08-20: three
plans, 4,705 lines, eight review rounds — **588 lines per round**, higher than
the proposals they derive from. Keep *"when in doubt, open the plan"*; replace
the cost claim with the measurement and surface the `not required(<rationale>)`
route beside it.

### C6 — a code-review finding carries a class, and only one class loops

**Four classes**, closed vocabulary:

* **`behaviour`** — the code does the wrong thing, or a test does not test what
  it claims. **Blocks and loops.**
* **`prose`** — durable text inside a shipped artifact (docstring, comment, test
  name) asserts something false or unusable. Corrected in the artifact; does not
  loop. Distinct from `record` because it outlives the review that found it.
* **`record`** — a verification figure, scope declaration or status field is
  wrong. Corrected in the record; does not loop.
* **`observation`** — about the process, not the artifact. **Routed out** to
  `dev/PLANNING.md` or a proposal; never disposed inside the plan.

**Exception**: *absent or invalid* evidence is not a `record` defect. If no valid
verification record covers the reviewed range the reviewer had nothing to verify
— a precondition failure, and it blocks.

**The reviewer assigns the class, never the author.**

**Notation.** Class in the finding heading after the id; counts by class on the
basis line:

```
#### CR12 [behaviour] — appending a hook silently deletes the release rule
**Findings**: 4 behaviour, 3 prose, 6 record, 0 observation
```

**Verdict is derived**: `REVISE` iff a `behaviour` finding is open or evidence
is absent/invalid; `PASS` otherwise.

**The record-only closeout path (RLT-08), stated end to end.** A `PASS` carrying
`prose` or `record` findings moves `awaiting-code-review -> ready-to-archive`
on the reviewer's commit, as today. The author's corrections then land as a
`## Response to code review` **before** `ready-to-archive -> archived`, and that
Response becomes a **closeout precondition of archive** alongside the existing
ones. No new state, no new edge, and the author's action happens in a legal
state — which Revision 5's version did not provide.

**Enforcement predicate (RLT-09), specified.** One predicate over
`## Code review` sections, in both planner twins, one atomic commit:

1. `**Findings**:` accepts `none` **or** four `<int> <class>` terms covering the
   closed vocabulary exactly once each. The existing `raised` spelling stays
   accepted for sections dated before this rule — that is the
   backward-compatibility boundary, and it is a date, not a guess.
2. Every `#### <id> [<class>]` heading carries a class from the vocabulary;
   unknown or missing refuses.
3. Ids are unique within a section; duplicates refuse.
4. Heading counts must equal the basis-line counts; mismatch refuses.
5. A section whose verdict is `PASS` while a `behaviour` finding is present
   refuses, and `ready-to-archive` is unreachable from it.

Directed tests, in `bootstrap/tests/test_lifecycle_contract.py`: unknown class,
missing class, duplicate id, malformed count, heading/count mismatch, and a
`behaviour` finding under a `PASS` — each required to go **red**.

### Invariants and their enforcing tests

| invariant | enforced by |
|---|---|
| a `## Security review` section is parsed and validated like any other | new cases in `test_lifecycle_contract.py` (valid; missing basis field; out-of-vocabulary tier) |
| C6's class grammar holds | the six directed tests above |
| a `behaviour` finding blocks archive | test 5 above |
| the planner twins stay byte-identical | the existing twin-parity gate |

### Failure dispositions

Every new predicate **refuses**; none warns. An unparseable `**Findings**:`
line, an unclassified finding, or a count mismatch is a refusal, not a default.

### Public paths

`tools/lifecycle_planner.py` and `templates/skills/_lib/lifecycle_planner.py`
(byte-identical, one commit); `dev/proposals/_template.md`,
`dev/plans/_template.md` and both shipped twins; `doctrine/plans.md`;
`doctrine/dual-review.md`; `AGENTS.md` and `templates/core/AGENTS.md`.

### Evidence

**The corrected classification (RLT-10)**, re-derived over CR1–CR13 in the final
vocabulary, summing to thirteen:

| class | findings | n |
|---|---|---|
| `behaviour` | CR1, CR3, CR6, CR12 | 4 |
| `prose` | CR2, CR10, CR11 | 3 |
| `record` | CR4, CR5, CR7, CR8, CR9, CR13 | 6 |
| `observation` | — | 0 |
| | | **13** |

Under the current rule, **CR8 and CR9 blocked and are both `record`**, while
**CR12 — `behaviour`, on a security control — was filed non-blocking.** The
ranking was inverted, and the previous count of twelve was wrong because a
fourth informal class was in use while the vocabulary named three.

`observation` shows zero because today's reviewers routed process notes into
their reports rather than the review section, by instinct. The class is real; it
was already being used without a name.

### Known omissions

Windows is unclaimed. No implementation of C6's predicate exists, so its runtime
behaviour is unmeasured. The `raised` backward-compatibility boundary is a date,
so a section written before it and edited after keeps the old form. This
proposal cannot self-apply: its derived plan is governed by the contract in
force when that plan opens.

### Deferred work

One successor proposal, registered in `dev/PLANNING.md`: a stable section
identity for an append-only artifact and a complete-set rule over it — the work
that made Change 1 unbuildable. Grouped because they are one problem.

## Review -- Anthony Kendall (Maintainer) -- 2026-08-21 (round 4)

**Reviewer**: Anthony Kendall (Human Maintainer). **Scribed by** Claude
(claude-opus-5), who is this proposal's author; the findings below were surfaced
in a working session with the Maintainer, who adopts and signs them. The
scribing is disclosed because several findings are the author's own about their
own contract, and a joint byline would misstate the independence of this read.

Reviewed commit: 906b315a5a2ee6d0eed770d333abe2b2aa25f314
Target: THE COMPLETE CURRENT CONTRACT (Revision 6), C1-C6
Prior findings: RLT-01 through RLT-10
Assurance path: high-assurance
**Tier**: External (human)
**Findings**: raised (5 blocking)

### Steelman

Revision 6 is the first genuinely self-contained contract in this file, and
RLT-07 is closed on its own terms. C1 and C2 name the two rules that would have
stopped the 25 rounds this proposal was opened over. C3, C4 and C5 are correct,
cheap, and have drawn no finding in four rounds. The diagnosis in the Context is
sound as far as it goes. What follows is mostly about how far it goes.

### Findings

#### RLT-11 — BLOCKING: C6 classifies findings, not fixes, so the code-review loop still has no termination condition

C6 decides whether a *review* passes. It does not decide whether the author's
*fix* needs another review, which is the question that produces the round count.
A `behaviour` finding "blocks and loops" unconditionally, so a corrected typo
and a redesigned guard return through the same edge. Measured 2026-08-21:
`PLAN_TRANSITIONS` gives `revising-code` exactly one exit,
`awaiting-code-review`; `full-suite-interception` has taken 8 review rounds. C2
already invents the missing shape for plans — `revising-plan ->
ready-to-implement` on the author's Response commit — and does not consider it
for code.

Add the symmetric edge, with closure bound at the time the finding is raised: a
reviewer raising a `behaviour` finding may name the evidence that closes it, and
the author's `## Response to code review` carrying that evidence moves
`revising-code -> ready-to-archive` without a fresh read. A finding with no such
binding loops as today — fail-closed. This puts the judgement with the reviewer,
who knows whether verifying the fix needs judgement or a glance, and fixes it
before the fix exists so the author cannot claim it after. This is the
highest-value change available in this proposal and it is currently absent.

#### RLT-12 — BLOCKING: `Plan readiness` is a ratchet with one position, and C2's Internal default is inert while it stands

Measured 2026-08-21 across the whole live corpus: **19 recorded
`**Plan readiness**:` values, 19 `DISTINCT REVIEW REQUIRED`, zero `READY`.** The
proposal cites 11/11 scoped to two proposals as evidence the toll is wasted; the
damaging reading is that the field cannot express the common case. Per
`doctrine/proposals.md:571`, omitting the field gives the derived plan its
declared tier (Internal); recording the finding escalates it to External.
Silence buys Internal and speech buys External, and a reviewer who has read a
complete contract and judges the ordinary Internal plan review correct has no
token to write. Nineteen reviewers met that binary and escalated.

C2 makes plan review Internal by default. This field will override it every time
it is recorded. Either extend the vocabulary with a third token meaning "read,
and the ordinary Internal review is right", or state in the contract that C2 is
inert until one exists, and register the fix. Do not ship C2 as though the
default will hold.

#### RLT-13 — BLOCKING: C1 stops a reviewer ending a proposal and leaves a reviewer assigning a downstream review tier

`AGENTS.md:134` names "a proposal reviewer recorded `DISTINCT REVIEW REQUIRED`"
as a ground for an External plan review. That is a reviewer imposing an
obligation on work not yet written, by an author not yet assigned —
structurally the same defect C1 corrects, pointed forward in time instead of
backward. C1's rule ("a reviewer never ends a proposal; the editor does") does
not reach it and Exclusions does not name it.

Extend C1 to cover tier assignment — the editor sets the derived plan's tier,
informed by the reviewer's finding — or name it in Exclusions and register it.
Do not leave it unaddressed in a proposal whose subject is who may end a review
loop.

#### RLT-14 — BLOCKING: the Context names three cost mechanisms and misses the largest

Measured 2026-08-21: `PROPOSAL_TRANSITIONS` has exactly one reader
(`lifecycle_planner.py:1372`, a `get()` returning a list for display) and
refuses nothing. The only predicate binding a raised finding is on the resting
state `awaiting-decision`; `accepted` has no such branch. **A Decision was
available at every point in this proposal's four rounds.** What prevented one
was agents telling the Maintainer it was unavailable — including this
proposal's own author, on 2026-08-21, in the session that produced this review.

Add this as the fourth mechanism and say plainly that C1 corrects a practice,
not a tool gate. Without it C1 reads as lifting a restriction that never
existed, and its real value — displacing a habit that cost four rounds — is
invisible to the next reader.

#### RLT-15 — BLOCKING: the contract asserts a registration that does not exist

`### Deferred work` states the successor proposal is "registered in
`dev/PLANNING.md`". It is not; no match for section identity, complete-set or
stable section in that file, instrument confirmed against a file that greps
freely at 2,499 lines. By C6's own vocabulary this is a `record` defect. Resolve
it by making the claim true — register the item — rather than by editing the
appended section.

#### RLT-16 — non-blocking: this proposal's header carries the defect RLT-12 describes

`**Plan review**: required(External)` is present because a round-1 reviewer
recorded `DISTINCT REVIEW REQUIRED`, not because anyone judged an External plan
review warranted for this change. The proposal arguing that a toll was paid
eleven times for a bridge that never opened is itself paying it. Not the
author's to fix: I will set `required(Internal)` at the Decision. Precedent
`b9a0324`.

### Coverage

Covered: the complete current contract C1-C6 and its ledger; the header;
`PROPOSAL_TRANSITIONS` and `PLAN_TRANSITIONS` and their readers;
`status_evidence_violations` for every proposal state; the `Plan readiness`
contract in `doctrine/proposals.md` and `doctrine/dual-review.md`; every
recorded `Plan readiness` value in `dev/`; the `Security review` parsed-kind
claim in C3, confirmed — 0 case-sensitive occurrences in both byte-identical
twins, and `_KNOWN_KINDS` matches on first word, so such sections parse to
nothing.

Not covered: **C6's motivating classification.** CR1-CR13 exist and the classes
sum to 13, but the assignments are the author's own judgement, and C6 turns on
one claim — that CR12 (`behaviour`, on a security control) was filed
non-blocking while CR8 and CR9 (`record`) blocked. That single fact motivates a
five-rule predicate and six directed tests, and deserves one independent read.
Also not covered: C6's runtime behaviour, since no implementation exists; C4 is
the intended mitigation and I accept it as such.

**Plan readiness**: deliberately omitted. See RLT-12 — the field cannot express
this pass's actual judgement, and recording either token would misstate it.

**Recommendation**: one revision closes all five blocking findings. I intend to
accept on that revision without a further review round.

## Response + Revision 7 -- Claude -- 2026-08-21

Answering the Maintainer's round-4 review (RLT-11 through RLT-16). All five
blocking findings are closed. The review's own recommendation was that "one
revision closes all five", and this is it.

**This revision is larger than closing five findings, because the Maintainer
widened the remit while it was being written.** Verbatim, across four messages:

> "Too much review, too much planning. Some things just can't be decided in
> advance. We are getting FAR to risk averse here."

> "This isn't nuclear launch software here, shipping a bug is okay. Far better
> to ship a few bugs then never get to develop the software at all. We've gotten
> Cairn stuck in process hell here because of the mechanical rules we've built.
> They MUST be softened"

> "Otherwise literally no one (including myself) will use them. They are too
> onerous and will ALWAYS be circumvented, because in real life we have to
> proceed with uncertainty and imperfection."

That last sentence is the strongest argument in this file and it is not mine.
A rule that is always circumvented is **worse than no rule**: it trains its
users to route around refusals, so the refusal that matters arrives with its
authority already spent. Cairn's own doctrine says this in one place already --
`AGENTS.md` on the gate anchor, where the hazard named is "building the habit of
routing around a refusal" -- but says it about a missing git ref and never about
the review apparatus. Revision 7 generalizes it, as **C0**.

### Findings ledger

| finding | disposition | where |
|---|---|---|
| RLT-11 (blocking) -- C6 classifies findings, not fixes, so the code-review loop still has no termination condition | **Closed by new C7.** A reviewer raising a `behaviour` finding may bind its closure evidence *in the finding*; the author's Response carrying that evidence moves `revising-code -> ready-to-archive` with no fresh read. Unbound findings loop as today -- fail-closed. Binding is fixed when the finding is raised, so neither side can invent it afterwards. Security-review findings are excluded and always loop. | New C7; `PLAN_TRANSITIONS` gains one conditional edge |
| RLT-12 (blocking) -- `Plan readiness` is a ratchet with one position | **Closed by new C8.** Third token `ORDINARY` added. Independently re-measured: 19 `DISTINCT REVIEW REQUIRED` and **one** `READY` -- but that `READY` is at `dev/proposals/_template.md:488`, the vocabulary *definition* (`READY \| DISTINCT REVIEW REQUIRED`), not a recorded value. The corpus count is 19-0, and the template line is the stronger evidence: the ratchet is visible in the vocabulary itself. | New C8 |
| RLT-13 (blocking) -- C1 stops a reviewer ending a proposal and leaves one assigning a downstream tier | **Closed by extending C1 into C8.** Confirmed at `AGENTS.md:134-138`: External plan review is taken "because a proposal reviewer recorded `DISTINCT REVIEW REQUIRED`". The token becomes **advisory**; the editor sets the derived plan's tier at the Decision. | C1 (extended); C8 |
| RLT-14 (blocking) -- the Context names three cost mechanisms and misses the largest | **Closed.** Independently re-measured: `PROPOSAL_TRANSITIONS` has exactly one functional reader per twin (`lifecycle_planner.py:1372`, a `get()` returning a list for display) plus one test reference; it refuses nothing. A Decision was available at every point. Added as the fourth mechanism, in the terms the finding demanded. | Context, fourth mechanism |
| RLT-15 (blocking) -- the contract asserts a registration that does not exist | **Closed by making the claim true**, not by editing the appended section. The successor item is now registered in `dev/PLANNING.md` > "Deferred follow-ups (durable home)". Instrument confirmed before trusting the absence: `grep -c 'section' dev/PLANNING.md` returns 35, so the file greps freely; the item itself returned zero. | `dev/PLANNING.md`; Deferred work |
| RLT-16 (non-blocking) -- the header carries the defect RLT-12 describes | **Acknowledged, not fixed.** The reviewer reserved it: *"Not the author's to fix: I will set `required(Internal)` at the Decision."* Left untouched. | -- |

### On the part of RLT-14 that is about me

The finding says what prevented a Decision was "agents telling the Maintainer it
was unavailable -- including this proposal's own author, on 2026-08-21, in the
session that produced this review." That is accurate and I am not going to
soften it. I described a state machine as gating something it does not gate,
without reading its readers, and the cost was rounds. It is the same defect this
file has now recorded four times in other forms: asserting a property without
running the measurement that would falsify it. C0 exists partly because I am not
confident the habit is gone.

**Scope delta**: widened, under the Maintainer's explicit direction quoted above.
Revision 7 adds C0 (risk posture), C7 (closure binding) and C8 (`Plan readiness`
vocabulary + tier authority) to the accepted-in-progress contract. Nothing is
dropped. The complete current contract below supersedes Revision 6's in full;
read it and ignore the earlier one.

---

## THE COMPLETE CURRENT CONTRACT (Revision 7)

*Supersedes the Revision 6 contract above in full. Self-contained.*

### Scope

Give Cairn's review loops a termination condition and a calibration, by
(a) naming who ends each loop, (b) allowing a loop only where the artifact is
executable, (c) making a code-review finding's *class* decide whether it loops,
(d) letting a reviewer bind a finding's closure so the fix does not need a fresh
read, and (e) stating the risk posture reviewers calibrate against.

### Exclusions

No change to: the proposal or plan lifecycle states (C7 adds one conditional
edge and no state); the Internal/External tier vocabulary; the append-only rule;
the complete-contract rule; the plan-readiness *inheritance* machinery, which
stops being exercised rather than being deleted; any release, gate or trust
ceremony; the Security Review trigger on any high-risk surface named in
`AGENTS.md`.

### C0 -- the risk posture reviewers calibrate against

**Cairn is a method for scientific and research software, not for
safety-critical systems.** The doctrine has never said so, and every reviewer
has therefore been free to calibrate at the strictest reading available. Stated
plainly:

* **An unshipped improvement has a real cost that is invisible.** A shipped bug
  has a real cost that is visible and usually fixable. Optimizing only against
  the visible one is not caution, it is a measurement error.
* **Narrowing is the reviewer's path of least resistance.** It costs the
  reviewer nothing, reads as prudence, and can never be shown wrong, because the
  wider version is never built. `AGENTS.md` already says this about *scope*
  reduction; it is equally true of review depth.
* **A rule too onerous to follow will be circumvented, and a circumvented rule
  is worse than no rule** -- it trains its users to route around refusals, so the
  refusal that matters arrives with its authority already spent.

**The reviewer's question is therefore "would shipping this cause damage that is
hard to undo?"** -- not "is this correct in every respect?". Findings that fail
that test are still recorded; they do not block.

**What C0 does not touch, and this list is exhaustive.** Full weight is retained
for the high-risk surfaces `AGENTS.md` names -- the scaffold/merge engine, the
install contract, the by-file license split, the local interpreter binding, the
portable-sweep executable trust root, the vendor-neutrality gate -- and for any
release or security ceremony. C0 lowers the calibration on ordinary work. It
lowers nothing where the damage is hard to undo, which is the whole of its own
test applied to itself.

### C1 -- the proposal flow, and who may end things

```
Write -> Review -> Revise -> Security Review (if needed)
      -> Revision after Security Review (if needed)
      -> Editor's decision (accept / reject) -> loop if needed, editor deciding
```

The editor is the Maintainer. **A reviewer never ends a proposal; the editor
does**, and may end one over open findings by naming them and their standing
state.

**Extended for RLT-13: a reviewer does not assign a downstream review tier
either.** A reviewer recommends; the editor assigns, at the Decision. The same
principle pointed forward in time instead of backward -- otherwise a reviewer
imposes an obligation on work not yet written, by an author not yet assigned.
The mechanism is C8.

### C2 -- the plan flow

```
Write -> Review (Internal) -> Security Review (if needed) -> Revise
      -> Execute
      -> Code Review (Internal) -> Revise Code (may loop, bounded by C7)
      -> Code Security Review (if needed) -> Revise Code (may loop)
      -> Dispositions with the Maintainer -> Archive
```

**Plan review is single-pass**: the author's revision closes it.

| from | to | owner | commit carrier | evidence predicate |
|---|---|---|---|---|
| `revising-plan` | `ready-to-implement` | plan author | the author's `## Response to plan review` commit | that section, disposing every finding of the preceding `## Plan review` |
| `revising-plan` | `awaiting-plan-review` | plan author | same | retained, and **required** when a Security Review is owed on the revision |

**Whether a second pass is warranted is the editor's judgement, on magnitude.**
Not a rule and not a taxonomy of exceptions.

**Prospective only.** A declared `required(External)` plan review remains a
floor. Only a plan opened after this rule is accepted takes the new default.

### C3 -- `Security review` is a recognized section kind

Measured 2026-08-21: `Security review` occurs **0** times in
`tools/lifecycle_planner.py` and its byte-identical twin. Two Security reviews
written on 2026-08-20 passed with basis fields, tier and existence all
unvalidated. Add it as a parsed kind, validated like `Review` / `Plan review` /
`Code review`.

**Tier is unchanged.** `Internal` / `External` is *model agency*; Security Review
is a *role* with a high-capability floor. Orthogonal axes.

### C4 -- constructibility is declared before the Decision

No proposal reaches `awaiting-decision` without a `Constructibility:` block: for
each falsifier the contract requires, the route that produces it. An item with no
route is `no admitted route`, and blocks. `Constructibility: asserted` is not a
record. **Enforced by**: the templates require it; the reviewer reads it. **Not**
a planner predicate.

### C5 -- the plan layer's cost claim is corrected

`doctrine/plans.md` says a plan costs "one file." Measured 2026-08-20: three
plans, 4,705 lines, eight review rounds -- **588 lines per round**, higher than
the proposals they derive from. Keep *"when in doubt, open the plan"*; replace
the cost claim with the measurement and surface the `not required(<rationale>)`
route beside it.

### C6 -- a code-review finding carries a class, and only one class loops

**Four classes**, closed vocabulary:

* **`behaviour`** -- the code does the wrong thing, or a test does not test what
  it claims. **Blocks, and loops unless bound under C7.**
* **`prose`** -- durable text inside a shipped artifact asserts something false
  or unusable. Corrected in the artifact; does not loop.
* **`record`** -- a verification figure, scope declaration or status field is
  wrong. Corrected in the record; does not loop.
* **`observation`** -- about the process, not the artifact. **Routed out** to
  `dev/PLANNING.md` or a proposal; never disposed inside the plan.

**Exception**: *absent or invalid* evidence is not a `record` defect -- the
reviewer had nothing to verify. Precondition failure; it blocks, and it cannot
be closure-bound under C7.

**The reviewer assigns the class, never the author.**

**Notation.** Class in the finding heading after the id; counts by class on the
basis line:

```
#### CR12 [behaviour] -- appending a hook silently deletes the release rule
**Findings**: 4 behaviour, 3 prose, 6 record, 0 observation
```

**Verdict is derived**: `REVISE` iff an *unbound* `behaviour` finding is open or
evidence is absent/invalid; `PASS` otherwise.

**The record-only closeout path**, stated end to end. A `PASS` carrying `prose`
or `record` findings moves `awaiting-code-review -> ready-to-archive` on the
reviewer's commit. The author's corrections land as a `## Response to code
review` **before** `ready-to-archive -> archived`, and that Response is a
closeout precondition of archive.

### C7 -- a reviewer may bind a finding's closure, and that ends the loop

**The problem C6 left open.** C6 decides whether a *review* passes. It never
decides whether a *fix* needs another review -- which is the question that
produces the round count. A corrected typo and a redesigned guard returned
through the same edge, because `PLAN_TRANSITIONS` gives `revising-code` exactly
one exit. Measured 2026-08-21: `full-suite-interception` has taken **nine**
review rounds.

**The rule.** A reviewer raising a `behaviour` finding **may** name, in the
finding itself, the evidence that closes it:

```
#### CR14 [behaviour] -- the guard is disarmed by its own decorator
Closes on: `_own` refuses a second registration of a held name, and a test
that appends `@_own def pytest_sessionfinish` exits 4 naming that hook.
```

The author's `## Response to code review` carrying exactly that evidence moves
`revising-code -> ready-to-archive` **with no fresh read**.

**Four constraints, each load-bearing:**

1. **Fail-closed.** A `behaviour` finding with no `Closes on:` loops exactly as
   today. Silence never buys the fast edge.
2. **Bound when raised, not after.** The evidence is fixed before the fix
   exists, so the author cannot claim it retroactively and the reviewer cannot
   invent it having seen the fix.
3. **The reviewer decides, because the reviewer knows.** Whether verifying a fix
   needs judgement or a glance is exactly what the person who found it is best
   placed to say. This is C1's principle -- authority sits with whoever holds the
   relevant knowledge -- applied to the code loop.
4. **Security findings are excluded.** A finding raised in a `## Security
   review` section may not carry `Closes on:`; it always loops. The Maintainer's
   standing instruction: *"No reviewer gates on second rounds, except maybe a
   security review."*

**Transition.** `revising-code` gains `ready-to-archive` as a *conditional*
target: legal only when every open `behaviour` finding in the most recent
`## Code review` carries `Closes on:` **and** the Response evidences each. No new
state.

**Known limit, stated rather than discovered.** The predicate needs to range
over "every finding of the preceding review", and an append-only artifact has no
stable section identity to range over -- the same gap that made this proposal's
withdrawn Change 1 unbuildable. C7 is therefore specified to compare against
**the most recent `## Code review` section by document order**, which is
well-defined without section identity and is what a human reader does anyway. If
that proves insufficient, it is the second instance that revives the deferred
item now registered in `dev/PLANNING.md`.

### C8 -- `Plan readiness` gains a third token, and stops binding

**The defect.** Measured 2026-08-21 across the live corpus: **19 recorded
`Plan readiness` values, 19 `DISTINCT REVIEW REQUIRED`, zero `READY`.** The
single `READY` in the tree is at `dev/proposals/_template.md:488` and is the
vocabulary definition, not a record. A reviewer who has read a complete contract
and judges the ordinary Internal plan review correct **has no token to write**:
silence buys Internal by default and speech buys External. Nineteen reviewers
met that binary and escalated. C2's Internal default would be overridden every
time the field is recorded.

**Three tokens:**

| token | who may write it | meaning |
|---|---|---|
| `READY` | an **External** reviewer who has read a complete current contract | the derived plan may *inherit*: Internal review plus a commit-bound `Inherited proposal basis` |
| `ORDINARY` | any reviewer | read, and the plan's ordinary Internal review is the right read. No escalation, no inheritance declaration. **This is the missing common case.** |
| `DISTINCT REVIEW REQUIRED` | any reviewer | *recommends* External, and must name what makes this plan need a different agent type |

Omission is read as `ORDINARY` -- unchanged in effect from today, but now with a
name, so a reviewer who considered the question and one who did not are no
longer indistinguishable.

**And the token is advisory.** Per C1 as extended: the **editor** sets the
derived plan's tier at the Decision, informed by the reviewer's token and
required to name it when departing from a `DISTINCT REVIEW REQUIRED`.
`AGENTS.md:134-138` currently makes the token binding; that sentence changes.

### Invariants and their enforcing tests

| invariant | enforced by |
|---|---|
| a `## Security review` section is parsed and validated like any other | new cases in `test_lifecycle_contract.py` (valid; missing basis field; out-of-vocabulary tier) |
| C6's class grammar holds | six directed tests: unknown class, missing class, duplicate id, malformed count, heading/count mismatch, `behaviour` under `PASS` |
| an *unbound* `behaviour` finding blocks archive | the `PASS`-with-`behaviour` test above |
| a **bound** `behaviour` finding reaches `ready-to-archive` only with its evidence in the Response | two directed tests: bound + evidenced (green); bound + Response missing the evidence (**red**) |
| a `Closes on:` inside a `## Security review` section refuses | one directed test |
| `Plan readiness` accepts exactly three tokens | one directed test per token plus an out-of-vocabulary refusal |
| the planner twins stay byte-identical | the existing twin-parity gate |

### Failure dispositions

Every new predicate **refuses**; none warns. An unparseable `**Findings**:`
line, an unclassified finding, a count mismatch, an out-of-vocabulary
`Plan readiness`, or a `Closes on:` in a Security section is a refusal, not a
default.

### Public paths

`tools/lifecycle_planner.py` and `templates/skills/_lib/lifecycle_planner.py`
(byte-identical, one commit); `dev/proposals/_template.md`,
`dev/plans/_template.md` and both shipped twins; `doctrine/plans.md`;
`doctrine/proposals.md`; `doctrine/dual-review.md`; `doctrine/rationale.md`
(C0); `AGENTS.md` and `templates/core/AGENTS.md`.

### Evidence

**The corrected classification**, re-derived over CR1-CR13, summing to thirteen:

| class | findings | n |
|---|---|---|
| `behaviour` | CR1, CR3, CR6, CR12 | 4 |
| `prose` | CR2, CR10, CR11 | 3 |
| `record` | CR4, CR5, CR7, CR8, CR9, CR13 | 6 |
| `observation` | -- | 0 |
| | | **13** |

Under the current rule, **CR8 and CR9 blocked and are both `record`**, while
**CR12 -- `behaviour`, on a security control -- was filed non-blocking.** The
ranking was inverted.

**C7's counterfactual, on this repository's own history.** Of the four
`behaviour` findings, CR1 and CR12 name their closing evidence inside the
finding text already -- CR1 asks for the competitor to be its own module, CR12
asks for `_tree` to refuse a name the conftest defines. Both were written as
bindable closures by reviewers who had no such mechanism, and both produced one
further full review round. C7 does not invent a behaviour reviewers lack; it
gives one they already have somewhere to go.

**The fourth cost mechanism (RLT-14).** `PROPOSAL_TRANSITIONS` has exactly one
functional reader per twin -- `lifecycle_planner.py:1372`, a `get()` returning a
list for display -- and refuses nothing. The only predicate binding a raised
finding is on the resting state `awaiting-decision`; `accepted` has no such
branch. **A Decision was available at every point in this proposal's four
rounds.** What prevented one was agents telling the Maintainer it was
unavailable, this proposal's author included. **C1 corrects a practice, not a
tool gate** -- and that is the largest of the four mechanisms, because a habit
needs no enforcement to hold.

### Known omissions

Windows is unclaimed. No implementation of C6's or C7's predicates exists, so
their runtime behaviour is unmeasured; C4 is the intended mitigation. The
`raised` backward-compatibility boundary is a date, so a section written before
it and edited after keeps the old form. C7 compares against the most recent
`## Code review` by document order rather than by section identity, which is a
stated limit and not a solved problem. **C0 is calibration, not a predicate**:
nothing enforces it, and a reviewer determined to be maximally strict can still
be, which is the honest description of what a stated posture buys. This proposal
cannot self-apply: its derived plan is governed by the contract in force when
that plan opens.

### Deferred work

One successor proposal, **now registered** in `dev/PLANNING.md` >
"Deferred follow-ups (durable home)" (2026-08-21): a stable section identity for
an append-only artifact and a complete-set rule over it -- the work that made
Change 1 unbuildable and that C7 works around. Grouped because they are one
problem. Registered rather than asserted, per RLT-15.

## Decision -- Anthony Kendall (Maintainer) -- 2026-08-21

**ACCEPTED as written and revised (Revision 7).** Authorization, quoted verbatim
and visually isolated:

> "I accept the proposal as written and revised. Please scribe my acceptance"

**Summary of accepted terms (Revision 7)**:

- **C0 -- risk posture.** Cairn is a method for scientific and research
  software, not safety-critical systems. The reviewer's question is "would
  shipping this cause damage that is hard to undo?", not "is this correct in
  every respect?". Findings failing that test are recorded and do not block.
  Full weight is retained for the high-risk surfaces `AGENTS.md` names and for
  any release or security ceremony.
- **C1 -- who may end things.** A reviewer never ends a proposal; the editor
  does, and may end one over open findings by naming them and their standing
  state. Extended: a reviewer does not assign a downstream review tier either --
  a reviewer recommends, the editor assigns at the Decision.
- **C2 -- the plan flow.** Plan review is single-pass; the author's revision
  closes it, via a new author-carried `revising-plan -> ready-to-implement`
  edge. Prospective only; a declared `required(External)` remains a floor.
- **C3** -- `Security review` becomes a parsed, validated section kind.
- **C4** -- constructibility is declared before a proposal reaches the Decision.
- **C5** -- the plan layer's "one file" cost claim is replaced with the
  measurement.
- **C6** -- a code-review finding carries one of four classes; only `behaviour`
  blocks and loops; verdict is derived.
- **C7 -- the code loop gains a termination condition.** A reviewer raising a
  `behaviour` finding may bind its closure evidence in the finding itself
  (`Closes on:`); the author's Response carrying that evidence moves
  `revising-code -> ready-to-archive` with no fresh read. Fail-closed: an
  unbound finding loops as today. Bound when raised, so neither side invents it
  afterwards. Security-review findings are excluded and always loop.
- **C8** -- `Plan readiness` gains `ORDINARY` as a third token, omission reads
  as `ORDINARY`, and the token becomes advisory rather than binding.

**Open items and their standing state**, named here because C1 requires an
editor ending a loop to name them rather than leave them implied:

1. **Two conformance violations stand.** Revision 7 carries no
   `### Withdrawn / superseded commitments` heading in either its Response or
   its complete-contract section, and `lifecycle_planner.py scan` refuses the
   artifact on both. Routed to the Revision 7 author, not to this Decision, on
   the Maintainer's instruction: *"Them"*. The Decision does not wait on it.
2. **A known-wrong figure is retained deliberately.** C7 states
   `full-suite-interception` has taken nine review rounds; six review passes are
   present. The Maintainer's instruction, verbatim:

   > "I do not want numbers fixed, you have to trust quotes because they come
   > from a friendly development team, and if there's an issue with how various
   > annotations in the proposal fire a trigger--fix tme."

   Recorded so the next reader does not treat the figure as verified.
3. **The header's `Plan review: required(External)` is untouched.** The
   Maintainer's round-4 review reserved converting it: *"Not the author's to
   fix: I will set `required(Internal)` at the Decision."* Acceptance was given
   "as written and revised", so this scribe did not alter the header. Under C8
   as accepted, the tier is the editor's to set and remains open.

**Scribed by** Claude (claude-opus-5), this proposal's author, on explicit
Maintainer instruction. The scribe wrote no part of the authorization above.

## Constructibility addendum -- Claude -- 2026-08-21 (C6's notation, measured)

Appended after Revision 7, from a measurement made while a code reviewer tried
to write a conforming `**Findings**:` line on a live plan. It changes no term of
the contract; it supplies a route C4 requires and Revision 7 asserted without
checking.

**C6's own notation is refused by the parser that exists today, and not where an
implementer would look for it.** Measured 2026-08-21 against
`tools/lifecycle_planner.py`, both controls run first so a negative result means
something:

| `**Findings**:` value | lead clause parsed | accepted |
|---|---|---|
| `4 behaviour, 3 prose, 6 record, 0 observation` (C6's notation) | `'4 behaviour'` | **no** |
| `raised -- 2 blocking (CR8, CR9), 4 non-blocking` (current spelling) | `'raised'` | yes |
| `none` | `'none'` | yes |

Two mechanisms, not one:

1. `_FINDINGS = ("none", "raised")` at `lifecycle_planner.py:562` -- a closed
   two-token vocabulary. Obvious, and C6's predicate item 1 already implies
   widening it.
2. `_VALUE_CLAUSE_RE` at `lifecycle_planner.py:1968` --
   `^[^.,;(/—]*?(?=\s+--\s|\s*[.,;(/—]|$)` -- takes the field's **lead clause**,
   stopping at the first `.`, `,`, `;`, `(`, `/`, em-dash or ` -- `. A
   comma-separated class list therefore never reaches the vocabulary check at
   all: it arrives as `'4 behaviour'`.

**Why this is worth recording rather than leaving to implementation.** An
implementer reading C6 will widen `_FINDINGS`, watch the format still refuse,
and have no reason to suspect a regex two hundred lines away that is doing
exactly what it was written to do. That is the *silent-tool* shape this
repository keeps rediscovering, one level down: the obvious mechanism is real,
fixes nothing on its own, and the second one is invisible from the contract.

**Consequence for C6, stated as a constraint and not a redesign.** C6's
predicate must change *both*, or C6 must adopt a notation whose lead clause is a
single token -- e.g. `**Findings**: classified -- 4 behaviour, 3 prose, 6
record, 0 observation`, which parses its lead as `'classified'` and reaches the
vocabulary check intact. The second option costs one word and no regex change,
and I record it as the cheaper route without choosing for the implementer.

**A live consequence, already visible.** The code review on
`suite-run-diagnostics` (2026-08-21) wrote its `**Findings**:` line in the
current `raised -- ...` spelling *after* tracing this parser, rather than in
C6's vocabulary. So the first reviewer to meet C6's notation in practice
correctly declined to use it. The backward-compatibility boundary in C6's
predicate item 1 is therefore doing more work than it appears to: until the
predicate lands, the old spelling is not merely tolerated, it is the only one
that parses.

**Constructibility**: route confirmed. Both mechanisms are named with file and
line; the notation alternative is exhibited and its lead clause measured; the
controls that make the negative result meaningful are in the table above.
