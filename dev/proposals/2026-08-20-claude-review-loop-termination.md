# Give the review loop a termination condition

**Author**: Claude (Strategy)
**Model**: claude-opus-5 (Claude Opus 5)
**Date opened**: 2026-08-20
**Status**: awaiting-review
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
