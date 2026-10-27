<!-- The proposal template. Copy only the opening header and section
     headings (`Context` through `Assurance path`) below the rule into
     `dev/proposals/<YYYY-MM-DD>-<author>-<slug>.md`, replace every prompt
     with your answer (or a one-line `N/A`), and do NOT copy template
     commentary or the later-stage `Review`, `Response`, and `Decision`
     skeletons at the bottom. -->

# Proposal template

A substantive change — a new abstraction, a cross-cutting refactor, a contract
change, anything worth a second opinion — goes through a proposal. Everything
else is a trivial change: make it, and say so in the commit.

Additional triggers this project treats as non-trivial:

<!-- cairn:slot triage-extra-triggers -->
Cairn guards several protected contracts — a change touching any of
these opens a proposal regardless of size:

* **Invariant-kernel or doctrine change** — anything under
  `doctrine/`, the dimension matrix / module gate-table (`dimensions/`,
  `bootstrap/BOOTSTRAP.md`), or the framework anchors in
  `doctrine/rationale.md`. The kernel is what makes a thing Cairn at
  all; it does not move silently, and a doctrine change additionally
  clears the doctrine-evolution rate-limit gate (`doctrine/rationale.md`
  > "How the doctrine evolves under evidence").
* **Bootstrap fidelity / install contract** — the scaffold's install
  set, the fidelity manifest (`bootstrap/fidelity-check.md`), the gate
  manifest, the lockfile schema, or the published install manifest
  (`scaffold.py --manifest`). Adopters depend on these.
* **Vendor-neutrality boundary** — introducing a model / vendor name
  into doctrine or a template (the `quality_gate.py --sub neutrality`
  surface). The deliberation record may name reviewers; shipped
  doctrine may not.
* **Bootstrap safety / security stack** — `bootstrap/SAFETY.md` (R-I),
  `bootstrap/security_check.py`, or the content scanner; a change here
  is also a Security Review trigger.
* **Licensing / provenance** — the by-file license split or
  `bootstrap/PROVENANCE.md`.
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
clears the obligation it was raised against. A second review round exists only
when the revision **widened scope** — material the review never saw.
`accepted` is terminal — archiving is a file move, not a status.

Two rules are bright-line:

* **Append-only.** Never edit a prior section — append a revising one. The
  record shows what was believed *at each point*, not a tidied final state. A
  Response carries the complete current contract, so a reader never has to
  reassemble it from diffs.
* **One commit per transition.** Open, review, response, and decision each get
  their own commit; bundling hides who changed what.

## Review

**One stance at every stage.** A review is by a fresh reviewer who did not
write the work, on the work's side: it makes the work better by questioning
its foundations, and it answers in writing. No agent picks a kind of review.
A proposal review asks three questions:

* **Should this happen as framed?** Should this exist as framed? Is there a
  better design, doing nothing included?
* **What is the best alternative?** The strongest, doing nothing included.
* **What would show it wrong?** What would make the author withdraw.

Each pass opens with a **Foundations** block of three lines, one answer per
question, each ending in the file, test, line or command that backs it.
**Improve means recommend**: the reviewer proposes the better version ("don't do
this" and "do it differently" count) and the author decides. **There is no
quota of findings.** "No defects found" is allowed only with the three answers
evidenced and the gaps named.
Reviews are **attributed and self-committed**: a review you did not write is not
yours to sign, and an independent read is only independent if its author is its
committer.

**More distance is the Maintainer's call, and only theirs.**

* **What it is.** An *External read* is a review the Maintainer asked for on one
  named artifact that exists now, in chat or inside a Decision, outside the usual
  procedure. A call that covers artifacts not yet written is a standing floor (a
  rule that applies without being asked), and a standing floor returns only by
  proposal. A roster the Maintainer sets (which agent types work the tree)
  is the team's shape, not a call: it adds no
  read and upgrades none. Distance is information, not a rule: a different agent
  type has different failure modes and a person has different knowledge. The
  staffing reviewer follows the Maintainer's brief, answers the same three
  questions from that distance, and says so.
* **How it is recorded.** The pass carries `**Called by**: Maintainer -- Decision
  at <commit>` (or `-- chat, <date>`, with `, relayed by <who>` where it was
  relayed), followed by the Maintainer's words, verbatim and set apart. The same
  words go in the commit message, as for a scribed Decision. `**Tier**: External`
  is valid only with that line, and a pass headed External without it is read as
  the usual review.
* **What an agent never does.** Declare External as a required review in a
  header, say a change needs one, recommend more distance, head a pass External
  on its own, or start one without those words. It may name a risk and a gap in
  its coverage line.
* **What a called read never does to the other reviews.** It adds to the usual
  review and replaces nothing. Its brief may add focus; it removes no owed
  answer, and it discharges no Security Review by its distance or its brief (a
  pass clears a Security Review only by being one). Any other authority in the
  quoted words, such as a waiver or a change of scope, takes effect only where
  Maintainer authorizations already live, a Decision block or a plan's fence,
  and never from a `Called by` line. Nothing checks the quote mechanically, in
  the pass or in the commit message: the next reviewer and the Maintainer at the
  Decision are the check.

**A high-risk surface takes a Security Review.** `usual + Security Review` in a
header means two passes: the usual pass and a Security Review pass that names its
own obligation. The usual pass never clears the second.
In a proposal review, `**Tier**: Security Review` names that obligation; the
skeleton does not call for a separate `**Obligation**` line.

**Write for the reader.** Follow Cairn Plain Language (the section of `dev/agent_collaboration.md`): conclusion first, and measured, assumed and expected claims kept apart.

## Keep the proposal short

The proposal stays one file: reviews, responses and decisions are appended to it. Keep what goes in it small.

* **Count words, not lines — never unwrap lines to look short.** Keep an
  opening proposal to **≤ 1,000 words (~6 KB)** and each appended review pass
  or response to **≤ 600 words (~4 KB)**. Wrap prose normally; putting a
  paragraph on one 400-character line to lower `wc -l` saves zero tokens.
* **Never copy template boilerplate or later-stage sections.** Copy only the
  opening headings (`## Context` through `## Assurance path`) below the rule;
  replace prompts and gated blocks (`Security preflight`, `Independent
  scientific check`) with your answer or a one-line `N/A: ...`, and never copy
  template instructions, slot comments, or the `## Review`, `## Response`, and
  `## Decision` skeletons until that lifecycle step occurs.
* **Scripts and task briefs stay out.** A checker lives in a script or a test
  file, not in the plan. A task brief for a sub-agent is a short note or file,
  cited by path and commit.
  The proposal carries the criterion and the result, not the code behind them.
* **Cite evidence by path, not by quotation.** A falsification ledger has one
  line per probe, with no output pasted.
* **Read by section.** Give each review, response or decision its own `##`
  heading, titled by what it holds and when it was written. Readers list them
  with `grep -n '^## ' <proposal>` and read only the sections the job needs.

## Forward-reference paths

A path that does not exist yet trips `claim_check`. Declare it under a literal
`Proposed paths:` line — no blank line before the first bullet, one physical
line each. Drop a line once its path resolves.

**The summary line.** In the `In brief` header line below the rule, write one plain
sentence a scientist outside the project could follow, and keep it on one physical
line because the board reads that line only. `python tools/board.py --json` prints
it as `in_brief` and a view shows it in place of the title; a longer `## In brief`
section below the header is separate and is not read by the board. Leave no
placeholder in a finished artifact, because the board prints whatever the line holds.

---

# {{proposal title}}

**Author**: {{agent or human}}
**Status**: awaiting-review
**Review**: {{usual | usual + Security Review}}
**Plan review**: {{required(Internal) | required(Internal + Internal Security Review)}} — the tier the derived plan will declare, decided here where the surface is still visible; or `not required(no plan: <how each plan-skip condition holds>)` when the change needs no plan (the skip conditions are in the plan triage rule)
**Opened**: {{YYYY-MM-DD}}
**In brief**: {{one plain sentence: what changes and why it matters}}

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
**Doc tier home rule** — route doc and doctrine changes by layer per
[`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):
cross-cutting prescription → governing layer (`AGENTS.md`);
deliberation about what to build → deliberation layer (`dev/`);
description of the software as it is → descriptive layer (`docs/`). A
proposal that omits the doctrine-surface routing is itself a review
finding.
<!-- cairn:end documentation-tier-home -->

## Evidence / verification plan

How anyone will know this worked — the tests, the checks, the observation. Name
what would falsify it.

### Tests required

<!-- cairn:slot tests-tier-home -->
Cairn's behavioral **test homes** are:

* **`bootstrap/tests/`** — the engine suite (the scaffold, the module
  merge, the upgrade path, the security stack, the gates). Fast,
  offline, `pytest` + standard library only (`vermin` is the one
  dev-only floor-check dep). Run the whole suite with
  `python -m pytest bootstrap/tests`; route by file
  (`test_<surface>.py`) and by node when scoping a change.
* **The example self-tests** — `examples/minimal/test_greet.py` and
  `examples/scientific-minimal/test_water_budget.py`, which prove the
  shipped runnable examples still run.

For the proposed change, name the affected test homes, exact behavioral nodes,
and public paths that must be exercised through their real entry points. Record
any speed or environment tiers that exist, but **speed alone does not establish
affected coverage**. The eventual plan owns a reviewed change-specific mapping,
not a permanent fast set; **unknown or uncertain scope falls back to the full
suite**. Prose-integrity and quality gates (below) are not pytest tests; name
them under *Examples / smoke checks* and the plan's verification commands.
<!-- cairn:end tests-tier-home -->

### Examples / smoke checks

<!-- cairn:slot examples-smoke-home -->
End-to-end surfaces a change can exercise:

* **The example gallery** — `examples/minimal/` and
  `examples/scientific-minimal/` run their own `greet.py` /
  `water_budget.py` under `pytest`; a change that touches what the
  examples demonstrate runs them.
* **The scaffold, without writing** — `python bootstrap/scaffold.py
  --summary --config <profile>`, `--dry-run`, and `--manifest`
  exercise the install path end-to-end with no side effects.
* **The prose-integrity gate** — `python scripts/check_cairn.py`
  (internal link resolution + claim-path check) is the doc smoke for
  any Markdown / doctrine change.
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

### Independent scientific check

*Gated to a change that touches a scientific assumption, or a result the
project publishes or acts on: a governing equation, a unit or sign convention,
a boundary condition, a parameter default, a calibration setup, or a coupling
between models. For every other change, one line — "N/A: no scientific
assumption or result touched" — is the correct entry.*

Name **one** check that could show the change is wrong about the world, not
only about itself:

* **What it compares.** The quantity, the expected value, and the tolerance
  with its source. Say whether you have opened the data and confirmed it holds
  what the check needs; if not, name what you would open to confirm it. If the
  check depends on data that does not exist yet, say so.
* **Why the expectation is independent.** Neither the proposed code nor a test
  written from the same understanding computes it. Its basis is one of these:
  * an analytical or manufactured solution;
  * a conservation law chosen against the error this change risks (a closed
    budget does not catch a wrong input);
  * a trusted observation or benchmark;
  * an independent implementation, or the saved output of the model the code
    reads (independent of the port, not of the model's physics);
  * a domain expert's expectation, written down before the result is seen.
* **The error it would catch.** The plausible mistake under which the check
  fails (a reversed sign, a unit slip, a misplaced boundary, a missed
  warm-up). This is security preflight S2's "Can it fail?", asked of a
  scientific check. At implementation, the implementer makes that mistake on
  purpose and records the check's failing output.
* **When the check passes by finding nothing.** A check that passes on "no
  change", "no difference" or "no effect" is evidence only if it could have
  found a change. Show the same analysis detecting a known effect of the size
  that matters (a positive control), or say plainly that it cannot. The failing
  run above serves as the control when the mistake it makes produces an effect
  of that size. At implementation, the implementer records the control with the
  failing run. For example, an analysis that reports no streamflow depletion
  from a pumping well first recovers the depletion of a synthetic well at the
  same rate, distance and schedule.

**Reviewers.** The proposal reviewer challenges whether the basis is really
independent of the code under review. The code reviewer verifies the recorded
failing run and, where one is owed, the positive control, and re-runs them when
that is cheap. The Maintainer judges at the Decision whether this is the right
check and the expected value is right. If no independent basis exists, say so;
the Maintainer weighs that, and it is not a reason to invent one.

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
Cairn's own mandatory high-assurance surfaces, each named in `AGENTS.md` >
"High-risk surfaces" and each already a Security-Review trigger:

* the **scaffold / merge engine** (`bootstrap/scaffold.py` →
  `bootstrap/_scaffold/`) — untrusted module/profile parsing, path handling,
  and writes into a target tree;
* the **install contract** — the fidelity manifest, the gate manifest, the
  lockfile schema, and the published `scaffold.py --manifest`;
* the **local interpreter binding** — `dev/.cairn/local-env.json`, its reader,
  and every call site that executes the path it returns;
* the **portable-sweep executable trust root** —
  `run_portable_security_sweeps.py`, its resolve/revalidate pair, and
  `portable_security_policy.json`;
* **governing doctrine and lifecycle enforcement** — anything under
  `doctrine/`, the lifecycle planner's gate predicates, or the authoring
  templates themselves.

Plus the two non-surface triggers: the **by-file license split**, and the
**vendor-neutrality boundary** (a model/vendor name reaching doctrine or a
shipped template).
<!-- cairn:end assurance-path-triggers -->

<!-- Later-stage sections — do NOT copy into a new proposal; append each
     section only when that lifecycle step occurs. -->

## Review -- {{reviewer}} -- {{YYYY-MM-DD}}

```
Reviewed commit: <full commit id>
Target: <the sections this pass reviewed>
Prior findings: <ids being closed, or none>
Assurance path: <the declared path>
```

**Tier**: {{usual | Security Review}}
**Findings**: {{raised | none}}
**Verdict**: {{ACCEPT | REVISE}}

*On a read the Maintainer called, replace the Tier line with these two, and set
the Maintainer's words beneath them, verbatim and apart:*

**Tier**: External
**Called by**: Maintainer -- Decision at <commit>

**Foundations** (the proposal row; one line per answer, each ending in the file,
test, line or command that backs it):

1. **Should this happen as framed?** {{should this exist as framed, and is there a better design, doing nothing included}} -- <evidence>
2. **Best alternative.** {{the strongest, doing nothing included}} -- <evidence>
3. **What would show it wrong.** {{what would make the author withdraw}} -- <evidence>

Lead with the strongest version of what the proposal is trying to do, then the
findings (blocking or non-blocking, with the evidence that closes each). If
answering a Response, also verify its withdrawal ledger.

## Response -- {{author}} -- {{YYYY-MM-DD}}

One disposition per finding, followed by the complete current contract at
left-margin headings (not a diff against the opening proposal, and not nested
as H3s inside an earlier section). End the revision with a real H3 headed
`### Withdrawn / superseded commitments` listing every dropped or replaced
commitment with why, or `None` if nothing was withdrawn.

## Decision -- {{Maintainer}} -- {{YYYY-MM-DD}}

**{{ACCEPTED | REJECTED | SUPERSEDED}}.** The Maintainer's authorization,
quoted **verbatim and visually isolated** (no paraphrase):

> "{{the authorizing words}}"

An agent may scribe a Decision only on an unambiguous instruction, and the
commit carries nothing else.
