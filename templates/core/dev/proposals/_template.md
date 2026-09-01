<!-- The proposal template. Copy everything below the rule into
     `dev/proposals/<YYYY-MM-DD>-<author>-<slug>.md`. -->

# Proposal template

A substantive change — a new abstraction, a cross-cutting refactor, a contract
change, anything worth a second opinion — goes through a proposal. Everything
else is a trivial change: make it, and say so in the commit.

Additional triggers this project treats as non-trivial:

<!-- cairn:slot triage-extra-triggers -->
(Adopter-specific triage triggers beyond the general list above — e.g.
a domain assumption class the project guards, or a protected-contract
registry. Fill with your project's extra "open a proposal when…"
bullets, or replace with `N/A: no project-specific triggers`. An
unfilled slot is a review finding.)
<!-- cairn:end triage-extra-triggers -->

## Lifecycle

```
awaiting-review <-> revising -> awaiting-decision
                             -> accepted / rejected / superseded
```

Each status names **who holds it next**. A review moves a proposal to
`revising`; **the author's Response and revision carry it to
`awaiting-decision`**, which is the Maintainer's. There is no clearing round —
no review is run merely to move a status — except a Security Review, which
clears the obligation it was raised against. `accepted` is terminal —
archiving is a file move, not a status.

Two rules are bright-line:

* **Append-only.** Never edit a prior section — append a revising one. The
  record shows what was believed *at each point*, not a tidied final state. A
  Response carries the complete current contract, so a reader never has to
  reassemble it from diffs.
* **One commit per transition.** Open, review, response, and decision each get
  their own commit; bundling hides who changed what.

## Review

**Internal review** strengthens the change within the structure proposed.
**External review** evaluates that structure from outside, and owes a verdict on
whether the change should happen at all, the strongest rejected alternative, and
what would falsify it. Both are **stances**: a fresh session is the floor for
each, and no tier requires a different agent type. Reviews are **attributed and
self-committed**: a review you did not write is not yours to sign, and an
independent read is only independent if its author is its committer.

A high-risk surface takes a Security Review. Declare the tier in the header;
`required(A + B)` means one pass per clause, each naming its own obligation.

## Forward-reference paths

A path that does not exist yet trips `claim_check`. Declare it under a literal
`Proposed paths:` line — no blank line before the first bullet, one physical
line each. Drop a line once its path resolves.

---

# {{proposal title}}

**Author**: {{agent or human}}
**Status**: awaiting-review
**Review**: {{required(Internal) | required(External) | required(Internal + Security Review)}}
**Plan review**: {{required(Internal) | required(Internal + Internal Security Review)}} — the tier the derived plan will declare, decided here where the surface is still visible
**Opened**: {{YYYY-MM-DD}}

## Context

What is true today, and what about it is a problem. Evidence, not assertion —
if you are claiming something is broken, show it failing.

## Proposal

What changes. Be specific enough that a reviewer can disagree with something.

## Rationale

Why this rather than the obvious alternative. If the change is costly, say what
it buys.

## Alternatives considered

At least one real one, with the reason it lost. "We considered doing nothing"
counts only if you say what doing nothing costs.

## Documentation / doctrine surface

What documentation, doctrine, or contract surface does this change touch, and
where does the change to it land?

<!-- cairn:slot documentation-tier-home -->
(Filled from the `documentation-plan` default-on module when installed
— paste content from `dev/modules/documentation-plan.md` > "Merged
into" > Block 2: dev/proposals/_template.md. The merged content names
the per-layer routing rule for doc + doctrine changes, pointing at
`docs/DOCUMENTATION_PLAN.md`. If documentation-plan is not installed,
replace with `N/A: documentation-plan not installed`. An unfilled
slot is a review finding.)
<!-- cairn:end documentation-tier-home -->

## Evidence / verification plan

How anyone will know this worked — the tests, the checks, the observation. Name
what would falsify it.

### Tests required

<!-- cairn:slot tests-tier-home -->
(Adopter-specific test taxonomy — name the project's **test homes**, affected
behavioral nodes, and **public paths** that must be exercised through their real
entry points. Record speed / environment tiers where they exist, but **speed
alone does not establish affected coverage**. The eventual plan owns a reviewed
change-specific mapping, not a permanent fast set; **unknown or uncertain scope
falls back to the full suite**. Fill from the project's test plan, or replace
with `N/A: no test layout` plus the project's full-test fallback.)
<!-- cairn:end tests-tier-home -->

### Examples / smoke checks

<!-- cairn:slot examples-smoke-home -->
(Adopter-specific examples / smoke-check surfaces — the gallery, CLI
sanity commands, notebook smokes the change can exercise end-to-end.
Fill with the project's runnable checks, or replace with `N/A: no
end-to-end exercisable surface`.)
<!-- cairn:end examples-smoke-home -->

#### Security preflight — five questions, answered in writing

*Gated to a **security-touching** change: one that adds, moves, or widens a
trust boundary (deserialization, subprocess invocation, parsing, file and path
handling, network I/O, credentials and environment), or one that touches a
high-risk surface this project's `AGENTS.md` names. For every other change, one
line — "N/A: no trust boundary added, moved, or widened" — is the correct
entry.*

Answer all five, one or two sentences each. These are **design questions, asked
while the design is still movable** — not documentation written after it is
fixed. An absent answer is a review finding; a *wrong* answer is a falsifiable
one, which is the point: the reviewer checks a stated claim in one read instead
of hunting for an absence over four rounds.

Structural questions about where material comes from and what runs. They do not
check whether an answer is *true*; they convert a hidden property into a written
claim a reviewer can falsify. Prospective only — an archived artifact is never
retro-fitted with them.

* **S1 — Who supplied it?** For each step where this change *decides*
  something (verifies, authenticates, authorizes, classifies, admits), name
  every input and the channel it arrives by, and say whether any input is
  supplied — directly or **by reference** — by the thing being decided about.
* **S2 — Can it fail?** For each check this change relies on, state the one-line
  mutation that makes it fail, and confirm you ran it. **If a check derives what
  it expects from the same object it is checking, say so plainly — that check
  cannot fail.**
* **S3 — What fires it, over what?** Name the command that runs the check, what
  selects it, and the exact input set it covers. Then quote the adopter-facing
  sentence describing it, and show the two agree.
* **S4 — Which way does it break?** For each default, fallback, normalization
  and parse-error path, say which side of the boundary it lands on when it goes
  wrong — and whether that is *more* authority or less.
* **S5 — Who still wins?** State the attacker capability this change assumes,
  then name one that still succeeds after it. If you cannot, say whether the
  class is closed **by construction** or merely **by enumeration** —
  enumeration ages.

**What they do not reach.** A semantically valid instruction that is hostile
carries no lexical signature, and no question here finds it.

**Prospective only.** This accounting applies to active and future artifacts;
an archived proposal or plan is immutable and is never retro-fitted with it.

## Signals the change is wrong

What you would expect to see if this turns out to be a mistake. Written now,
while you are least motivated to hedge.

## Scope delta

The baseline is the scope as opened. Revising a proposal under review may
narrow it, and that is legitimate — but it is *recorded*, not silent.

**Neither author nor reviewer may concede a baseline outcome**; only the
Maintainer can. Declining a proposed expansion is not a reduction — it was
never in the baseline.

If this revision drops anything the proposal opened with, say so here as one
grouped record, each entry blocking archive until dispositioned:

**Scope delta**: preserved | degraded | lost

One line per removed unit, each carrying its own
`**disposition**: <accept | guard | wontfix | defer>`. Prefer specifying to
cutting; if you cut, say why specifying was rejected.

## Assurance path

**Assurance path**: {{standard | high-assurance}}

`high-assurance` is **mandatory** when the change touches a security surface, a
trust root, the install contract, or anything an adopter executes.
Uncertainty resolves to `high-assurance` — the fence is a refusal rule, not a
checklist to argue past. These are author declarations, not inferences: the
checker attests that a path was declared, never that it was right.

<!-- cairn:slot assurance-path-triggers -->
(Adopter-specific high-assurance triggers beyond the mandatory list above —
the project's own protected surfaces, its scientific-assumption or
unit/CRS-convention classes, its release or trust ceremonies. Fill with your
project's bullets, or replace with `N/A: no project-specific high-assurance
triggers`. An unfilled slot is a review finding.)
<!-- cairn:end assurance-path-triggers -->

## Review -- {{reviewer}} -- {{YYYY-MM-DD}}

The four-field review basis is mandatory, so a later reader knows what was read:

```
Reviewed commit: <full commit id>
Target: <the sections this pass reviewed>
Prior findings: <ids being closed, or none>
Assurance path: <the declared path>
```

**Tier**: {{Internal | External | Security Review}}
**Findings**: {{raised | none}}
**Verdict**: {{ACCEPT | REVISE}}

Lead with the strongest version of what the proposal is trying to do, then the
findings. Mark each blocking or non-blocking, and say what evidence would close
it. A reviewer answering a Response must also verify its withdrawal ledger.

## Response -- {{author}} -- {{YYYY-MM-DD}}

A disposition per finding, then the complete current contract.
Ship one complete current contract with the Response, every time — not
conditionally, and not a diff against what the proposal was.
Earlier sections remain immutable history; the newest reviewed revision binds.

Each revision's headings sit at the left margin — an H3 nested inside a prior
section is not a new revision, and the checker reads position, not intent.

Each revision ends with a ledger headed exactly
`### Withdrawn / superseded commitments` — written as a real H3 in your
proposal, not here, where it would make every scaffolded copy look like it
already had one.

List every commitment the revision drops or replaces, one per line, with why.
If nothing was withdrawn, only a written `None` distinguishes an empty ledger
from a forgotten one. The checker confirms a ledger is present and parseable;
it never verifies that the ledger is complete — that is the reviewer's job, and
it is why the ledger is read rather than counted.

## Decision -- {{Maintainer}} -- {{YYYY-MM-DD}}

**{{ACCEPTED | REJECTED | SUPERSEDED}}.** The Maintainer's authorization,
quoted **verbatim and visually isolated**:

> "{{the authorizing words}}"

Paraphrase is not permitted here — it admits drift, condition-softening, and
hallucinated approval. Explanatory prose is fine, kept clearly separate from
the quoted words. An agent may scribe a Decision only on an unambiguous
instruction, and the commit carries nothing else.
