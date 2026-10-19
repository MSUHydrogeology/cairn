<!-- cairn-internal-ref-allow: doctrine/plans.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- cairn-internal-ref-allow: doctrine/lifecycle.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- The plan template. Copy everything below the rule into
     `dev/plans/<slug>.md`. Keep it short: a plan is a working
     document, not a second proposal. -->

# Plan template

A non-trivial accepted proposal opens a plan. The plan says how the work
happens and how you will know it worked; it does not re-argue the decision.

## Lifecycle

```
awaiting-plan-review -> revising-plan -> ready-to-implement
  -> implementing -> awaiting-code-review <-> revising-code
  -> ready-to-archive -> archived
```

Each status names **who holds it next**. Opening a plan archives its source
proposal in the same commit.

**Reviews, responses and decisions append and are never edited. Operative
cells — Scope, Sequence, Acceptance criteria, Verification — revise in place
until implementation begins.**

**A plan answers plan review in its cells, not in a contract revision.** This
is the one place the plan's rule is the *opposite* of the proposal's, so it is
stated rather than left to be inferred: a proposal Response appends a complete
current contract carrying a withdrawal ledger; a plan does not. Before
implementation, fold plan-review corrections straight into the mutable
operative cells and let the appended `## Response to plan review` be a
disposition table that *points at* them — a second copy of a cell is
immediately a second answer to the same question.
Once execution of a chunk begins, changes append instead.

**Deviating from an accepted plan takes the Maintainer's word** — new scope, a
contract review never saw, an acceptance criterion you cannot meet, **or
accepted scope removed**. Removal counts in both directions: accepted scope is
a floor, and a reviewer cannot create authority to narrow by calling the
remainder out of scope.

**The Waiting line.** When a plan's next move becomes the Maintainer's, write
one header line, `**Waiting on Maintainer**: <what>`, in the header block,
beside Status, and delete it when they answer. Write it at three moments: work
reaches a fenced chunk (one marked MAINTAINER-GATED or MAINTAINER-ONLY), you
put a `defer` batch to the Maintainer, or you make a deviation request. Keep
`<what>` under 48 characters, the board's cell width; the detail stays in the
plan. A change note (`dev/plans/<slug>.md`) carries the line the same way. The
colon sits outside the bold, exactly as shown: with the colon inside the bold
the board does not read the line. `python tools/board.py --maintainer` lists
every artifact that carries it. This paragraph sits above the rule, so the line
is described here and not printed in the header below: a header line the board
reads would list every new plan as waiting.

## Review

**One stance at every stage.** A review is by a fresh reviewer who did not
write the work, on the work's side: it makes the work better by questioning
its foundations, and it answers in writing. No agent picks a kind of review.
A plan review is fresh-context and one round: the fold carries the plan to
`ready-to-implement`, and there is no second plan-review pass. Plan review and
code review each ask three questions:

* **Plan review.** *Should this happen as framed?* The Decision settled the
  premise. Does the plan deliver it? *Best alternative:* a simpler path to the
  same outcomes. *What would show it wrong:* the result showing it cannot
  deliver.
* **Code review.** *Should this happen as framed?* Does it really do what it
  claims? Try to break it, in order to fix it. *Best alternative:* a simpler or
  safer build, if any. *What would show it wrong:* the input or run that breaks
  it, and what was tried; Answer 3 points at the falsification ledger rather
  than restating it.

Each pass opens with a **Foundations** block of three lines, one answer per
question, each ending in the file, test, line or command that backs it.
**Improve means recommend**: the reviewer proposes the better version ("don't do
this" and "do it differently" count) and the author decides. **There is no
quota of findings.** "No defects found" is allowed only with the three answers
evidenced and the gaps named.

Code review's job is falsification, and its floor is **not the implementing
agent**. It never reopens the Decision (what to build is settled; how it was
built, and what breaks it, is the question). A clean code review shows a
falsification ledger (`dev/agent_collaboration.md` > "The review sweep").

**More distance is the Maintainer's call, and only theirs.**

* **What it is.** An *External read* is a review the Maintainer asked for on one
  named artifact that exists now, in chat or inside a Decision, outside the usual
  procedure. A call that covers artifacts not yet written is a standing floor (a
  rule that applies without being asked), and a standing floor returns only by
  proposal. A roster the Maintainer sets in `dev/collaboration_agreement.md`
  (which agent types work the tree) is the team's shape, not a call: it adds no
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

A plan whose surface calls for security treatment declares `Plan review:
required(Internal + Internal Security Review)`. Only an appended `## Plan review`
pass whose `**Obligation**` line matches clears it, never an ordinary Internal
pass. No tool reads that line: the next reviewer, the code reviewer and the
Maintainer check it.

## Forward-reference paths

A path that does not exist yet trips `claim_check`. Declare it instead — the
literal `Proposed paths:` line, no blank line before the first bullet, one
physical line per bullet. Drop a line once its path resolves.

---

# Plan: {{short title}}

**Source proposal**: {{dev/proposals/archive/...}}
**Status**: awaiting-plan-review
**Plan review**: {{required(Internal) | required(Internal + Internal Security Review)}}
**Opened**: {{YYYY-MM-DD}}

## Source proposal

One paragraph: what the proposal decided. The plan executes it.

## Scope

What this plan does and, where it is not obvious, what it deliberately does
not. Name the surfaces it touches.

### Documentation / doctrine surface

<!-- cairn:slot documentation-tier-home -->
(Filled from the `documentation-plan` default-on module when installed
— paste content from `dev/modules/documentation-plan.md` > "Merged
into" > Block 3: dev/plans/_template.md. The merged content names
the per-layer routing rule for doc + doctrine changes, pointing at
`docs/DOCUMENTATION_PLAN.md`. If documentation-plan is not installed,
replace with `N/A: documentation-plan not installed`. An unfilled
slot is a review finding.)
<!-- cairn:end documentation-tier-home -->

## Sequence

One row per chunk: what it does, what gates it, roughly what it ships. Mark a
chunk MAINTAINER-GATED or MAINTAINER-ONLY where approval is actually
load-bearing — that fence, not a blanket per-commit gate, is where approval
binds to something specific. When work reaches a fenced chunk, write the
Waiting line (`**Waiting on Maintainer**: <what>`) in the header block, beside
Status, and delete it when the Maintainer answers.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | | | |

## Acceptance criteria

Per chunk, each falsifiable. A criterion you cannot imagine failing is not one.

A security-touching plan re-answers the five security-preflight
questions only where its chunking changes an answer — most often S2
(which chunk runs the mutation) and S3 (which gate command fires the
check).

**An independent scientific check is accepted scope.** If the proposal names
one, it becomes an acceptance criterion. A replacement qualifies only if it
fails under the error the original names. If nothing qualifies, dropping the
check is a scope reduction under *Scope delta* and needs the Maintainer's
quoted allowance. Saying that the result now rests on the implementation does
not settle it. When the check fails for real during implementation, one line
records whether anything else would have shown the error.


  <!-- cairn:slot acceptance-doc-tooling -->
  (Adopter-specific doc-generation tooling — the exact schema source +
  render command, the snippet-sync command, the CLI / notebook smoke
  surfaces the project uses. Fill with the project's commands, or
  replace with `N/A: no generated or snippet-synced docs`.)
  <!-- cairn:end acceptance-doc-tooling -->

## Scope delta

**Accepted scope is a floor.** The baseline is the scope as accepted by the
proposal, and dropping an outcome it committed to is a deviation exactly as
adding one is. Sequencing is free — moving work between chunks of a live plan
owes nothing — but delivering less does not. Work handed to a plan that is not
open yet is a `defer`, with a board row listing the items. When the accepted
text assigns that work to the later plan, the `defer` line quotes that
assigning sentence and the Decision, which is the authorization; a plan that
simply fell short has no assignment to quote, and its remainder goes to the
Maintainer.

**A reviewer cannot create that authority by calling the remainder "out of
scope."** Narrowing is the path of least resistance in review: it costs the
reviewer nothing, reads as prudence, and can never be shown wrong, because the
wider version is never built. Neither author nor reviewer may concede a
baseline outcome; only the Maintainer can.

If scope is reduced, declare it here — one grouped record, not a set of roadmap
rows, and each entry blocks archive until dispositioned:

**Scope delta**: preserved | degraded | lost

One line per removed unit, each carrying its own
`**disposition**: <accept | guard | wontfix | defer>` — a group-level home is a
location, not a decision. Say what was dropped, why specifying was rejected in
favour of cutting, and quote the Maintainer's allowance. Declining a proposed *expansion* is not a
reduction — it was never in the baseline. A chunk's own fence bounds this pass,
not the accepted proposal.

## Verification

**Boundary A (iteration, scoped).** The tests owning each touched surface,
plus its standing gates.

<!-- cairn:slot verification-commands -->
Before implementation, make Boundary A a **reviewed mapping**: for each changed
invariant and public path, name the exact affected test node/file and every
standing non-test gate for the touched surface. Run that scope while iterating.
There is no permanent fast tier; if a substantive surface has no reviewed
mapping or cannot be bounded confidently, run the configured full suite.
**The full suite runs only as a certifying run** (`AGENTS.md` > Verification
boundaries): this plan's own records are scoped and carry
`**Certified by**: <commit>`, or `pending` until a certifying run covers them.

After the final implementation commit, Boundary B runs once against a clean,
unchanged commit under the project's canonical interpreter/runtime. The default
is the **configured full suite** plus standing integration gates; a plan whose
reviewed mapping **bounds the change's effects confidently** may instead run
that mapping plus every standing gate for every touched surface. Bounded mode
**refuses** — run full — when the change touches a **contract surface** (the
project's install contract, manifests, or lockfile schema) or a
**trust-ceremony surface** (any high-risk surface the governing file names, or
release/security ceremony work). **Uncertainty resolves to `full`.** List those
concrete commands here, including test outcomes and every plan-specific
acceptance command.

Only after that stable run, append a dated section named
`Implementation verification -- <agent> -- YYYY-MM-DD` at H2. Do not place an
empty heading in a new plan. The record uses these exact fields:

* **Boundary B mode** — `full` | `bounded`. On `bounded`, also name the touched
  surfaces, the reviewed mapping and standing gates run, why the effects are
  bounded, and the explicit absence of any contract or trust-ceremony surface.
* **Tested commit** — full revision ID.
* **Reviewed range** — base and tested endpoint.
* **Interpreter/runtime** — canonical path and version.
* **Pre-run state** and **Post-run state** — clean tree and identical tested
  revision.
* A command table with **Command**, **Exit**, **Outcomes**, and **Elapsed**
  columns, including pass/fail/skip/xfail/xpass counts where applicable.
* **Non-pass disposition**, **Plan-specific acceptance commands**, and
  **Known omissions**.

Also name the project's documentation, schema, snippet, security, and smoke
gates here. If none applies, record `N/A` with a reason rather than omitting the
surface silently.
<!-- cairn:end verification-commands -->

**Boundary B (integration).** After the final implementation commit, against a
clean unchanged commit under the canonical interpreter. Record
`**Boundary B mode**: full | bounded`. **Uncertainty resolves to `full`**, and
`full` is mandatory for any contract or trust-ceremony surface. On `bounded`,
name the touched surfaces, the mapping run, and why the effects are bounded.

Append the evidence as `## Implementation verification -- <agent> -- YYYY-MM-DD`:
tested SHA, interpreter, clean pre/post state, commands, outcomes, timing,
disposition of every non-pass, known omissions.

**Boundary C (falsification)** is the code reviewer's, and it is not re-running
Boundary B's command. Verify the record against the reviewed range, then run
independent **targeted falsification** — attack the claims that would hurt most
if wrong.

A **fresh full run** is required, and the record does not carry, when any of
these holds: **no valid Boundary B record exists**; an **unrecorded
cross-surface dependency** appears; the run reports a **skip, xfail, or xpass**
the record does not dispose of; **review sharpening changes implementation,
tests, executable templates, or** fixtures; a **trust ceremony that explicitly
requires** one applies; or there is a **concrete reason to distrust or falsify**
the evidence.

## Dispositions

*Filled at archive-preparation, and this section is why the plan cannot archive
without it.* Every **explicitly-deferred follow-up** this plan carries takes one
recorded disposition: `accept` (fixed in scope), `guard (<path>::<node>)` (homed
in something that **executes** and names the node -- a comment is not eligible,
because comments do not fire), `wontfix` (explicit non-action, with a
rationale), or `defer`.

**Every deferred item is recorded in `dev/PLANNING.md`, and requires the
Maintainer's authorization quoted verbatim.** Writing the disposition is not
performing the deposit. An item left only in a plan that then archives is
invisible to anyone looking for outstanding work, and archived artifacts are
not scanned by default -- so it is not deferred, it is lost. Present `defer`
requests as **one batch**; that batching keeps the Maintainer gate affordable.
When you put the batch to the Maintainer, write the Waiting line
(`**Waiting on Maintainer**: <what>`) in the header block, beside Status, and
delete it when they answer.

**Archived files are records, not to-do lists.** Nothing still to be done may
have an archived file as its **only home**. A live home is an open proposal or
plan that names the item in its own text, an issue by number, or a board row;
a pointer to an archived file, or to a plan that is not open yet, is not a live
home. The archive commit writes its own changelog entry, so no line is left
owed to the next session. An archiving plan carries no Waiting line: a wait
still open at archive moves to a board row marked with the Waiting line.

Record the outcome as a `Dispositions: ...` line so it reconstructs from the
durable record alone. **An append re-opens the attestation**: this section is
append-only, so if you add content after writing the line, restate or amend it.

Two eligibility rules bound the choice: a follow-up that **reaches an adopter,
blocks a release, or needs a Decision** cannot be `wontfix`; and one **named by
a closed artifact's disposition block** cannot be `wontfix` without the
Maintainer.

**Nothing mechanical checks any of this.** The lifecycle planner that once
parsed for a `Dispositions:` block was retired in August 2026; the enforcer is a
reviewer opening the artifact at archive-preparation. The full rule, including
why, is `doctrine/lifecycle.md` > "Archive precondition" and
`doctrine/plans.md` > "Lasting-truth migration doctrine".

## Plan review -- <reviewer> -- <YYYY-MM-DD>

Open every pass with its basis, so a later reader knows what was actually read:

```
Reviewed commit: <full commit id>
Target: <the sections this pass reviewed>
Prior findings: <ids being closed, or none>
Assurance path: <the plan's declared path>
```

**Obligation**: <the one clause this pass clears>
**Tier**: <Internal | Internal Security Review>
**Findings**: <raised | none>

*On a read the Maintainer called, add these two lines, with the Maintainer's
words beneath them, verbatim and apart:*

**Tier**: External
**Called by**: Maintainer -- Decision at <commit>

**Foundations** (the plan row; one line per answer, each ending in the file,
test, line or command that backs it):

1. **Should this happen as framed?** <the Decision settled the premise; does the plan deliver it> -- <evidence>
2. **Best alternative.** <a simpler path to the same outcomes> -- <evidence>
3. **What would show it wrong.** <the result showing it cannot deliver> -- <evidence>

An H3 inside another pass does not count as a pass of its own — a heading at
the left margin is what the checker reads.

## Code review -- <reviewer> -- <YYYY-MM-DD>

Code review's floor is not the implementing agent; a fresh session clears it. It
never reopens the Decision. Self-committed by its author; blocking findings move
the plan to `revising-code`, and the implementer's answer carries it to
`ready-to-archive`. A second code-review pass runs only when the revision
introduced new defects, never to re-confirm that the first round's findings were
addressed. Same basis block, with the range made explicit:

```
Reviewed commit: <full commit id>
Target: <the code range this pass reviewed>
Prior findings: <ids being closed, or none>
```

**Foundations** (the code row; one line per answer, each ending in the file,
test, line or command that backs it):

1. **Should this happen as framed?** <does it really do what it claims; try to break it, in order to fix it> -- <evidence>
2. **Best alternative.** <a simpler or safer build, if any> -- <evidence>
3. **What would show it wrong.** <the input or run that breaks it, and what was tried> -- see the falsification ledger (`dev/agent_collaboration.md` > "The review sweep")

**Bounding**: ACCEPTED | FULL RUN REQUIRED — recorded only after challenging a
named surface or mapped test, never because the field is present.

**Waiting-line check.** `git log -p` on the plan must show a Waiting line for
each fenced chunk whose fence became the next move inside the reviewed range,
and for each deviation request made in it. A fence the range did not reach is
not checked, and one whose wait is declared on a marked board row is checked
there. A missing line is a finding, recorded in
the project's incident tracker.
