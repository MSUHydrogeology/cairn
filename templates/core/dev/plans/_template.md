External-repo paths: `docs/methodology/plans.md`, `docs/methodology/lifecycle.md`
<!-- The plan template. Copy only the opening header and operative section
     headings (`Build summary` through `Verification`) below the rule into
     `dev/plans/<YYYY-MM-DD>-<slug>.md`, replace every prompt with your answer
     (or `N/A`), and re-read this file before writing or revising; its word
     budgets and copy rules change. -->

# Plan template
Written in [Cairn Plain Language 1.0](../agent_collaboration.md).

A non-trivial accepted standard/heavy proposal opens a plan. Light has no plan,
even for multi-area or wide work. The accepted proposal holds its own checks;
the arc owner joins related work at the selected integration point. The plan
says how the work happens and how you will know it worked; it does not
re-argue the decision.

## Lifecycle

```
awaiting-plan-review -> revising-plan -> ready-to-implement
  -> implementing -> awaiting-code-review <-> revising-code
  -> ready-to-archive -> archived
```

Each status names **who holds it next**. Opening a plan archives its source
proposal in the same commit. Name the plan
`<YYYY-MM-DD>-<slug>.md`, using its opening date. Plans need no folder by
default; shared tests, scripts, and assets stay in their canonical homes.

**Reviews, responses and decisions append and are never edited. The four
operative cells — Scope, Sequence, Acceptance criteria, Verification — remain
editable throughout active work.**

**Revise operative text in place.** A proposal Response revises the proposal's
current text; reviews, earlier responses and decisions remain appended. A plan
response disposes of findings and points to corrected plan cells.
Substantive plan changes during implementation stop affected and dependent
work, return the plan to `revising-plan`, and use the amendment record below.
Wording or status edits that change no obligation need no amendment review;
missing design returns to the existing operative cells.

**Plan amendments.** Append a `## Plan change -- <author> -- <date>` entry
with `**Prior reviewed commit**`, `**Replacement commit**`, `**Affected cells
and dependencies**`, `**Change**`, `**Reason**`, and `**Required obligations**` (exact `Internal` and/or `Internal Security
Review` strings, joined with ` + `).
IDs are full 40- or 64-hex Git object IDs. The revision commit may use `this
commit` for Replacement commit while status is `revising-plan`; the next
plan-only metadata-fill commit replaces that marker with the revision SHA in
the same entry before review. This fill is not another revision. The first
Prior reviewed commit is the original full-review target; later ones name the
preceding amendment replacement, never a review or disposition commit. Affected
work stays stopped until the ID is bound, reviews and author disposition are
complete, and the plan returns to `ready-to-implement`.

List affected operative headings and dependent chunk IDs as a comma-separated
set without duplicates; each review repeats that exact set. Each required
obligation gets one `## Plan amendment review -- <reviewer> -- <date>` record
with the same prior/replacement pair and set, one `**Obligation**` (`Internal`
or `Internal Security Review`) and one `**Verdict**` (`ACCEPT` or `REVISE`).
The first prior ID must match the full ID in the original plan review;
subsequent entries link directly to the preceding replacement. Preserve the
original review and all prior amendment records. A short legacy `Reviewed
commit` remains valid for ordinary review, but cannot establish an amendment
baseline, so that chain stops rather than guessing.

Every attempt needs a complete, unambiguous set of reviews. A latest set with
REVISE selects only author revision while status is `revising-plan`. A
successor must name that rejected replacement as its prior, carry forward the
union of unresolved affected entries and required obligations, and add its own
changes. Its reviews are fresh; no earlier ACCEPT transfers. Missing, extra,
duplicate, conflicting, mismatched, narrowed or skipped records stop selection.
The latest revision is actionable only after every required review is ACCEPT
and its paired author Response records `**Disposition**: ready-to-implement`.
Security Review passes across all replacements count toward the existing cap;
a successor does not reset it. The advisory reader compares committed text and
record order without Git or SHA ownership proof; consistently forged IDs are
not detectable. Changed Verification or dependencies cannot inherit approval.

**Deviating from an accepted plan takes the Maintainer's word** — new scope, a
contract review never saw, an acceptance criterion you cannot meet, **or
accepted scope removed**. Removal counts in both directions: accepted scope is
a floor, and a reviewer cannot create authority to narrow by calling the
remainder out of scope.

A defect fix made under the defect-fix rule
(`AGENTS.md` > "Working tree and commits") is not new scope.

**The Waiting line.** When a plan's next move becomes the Maintainer's, write
one header line, `**Waiting on Maintainer**: <what>`, in the header block,
beside Status, and delete it when they answer. Use it for an actual decision or
permission question in opened work, an unexpected authority stop, a `defer`
batch, or a deviation request. Do not plan routine approval or passive calendar
waits as Maintainer-gated final chunks; queue those outcomes before opening
their work. Keep
`<what>` under 48 characters, the board's cell width; the detail stays in the
plan. The colon sits outside the bold, exactly as shown: with the colon
inside the bold the board does not read the line. `python tools/board.py --maintainer` lists
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
  it, and what was tried; Answer 3 points to evidence briefly and names any
  remaining uncertainty.

For functional-prose changes, plan and code reviews also ask: **Does any rule
weaken or disappear?** This is a reading question, not a fourth Foundations
answer.

Each pass opens with a **Foundations** block of three lines, one answer per
question, each ending in the file, test, line or command that backs it. Each
answer states its point in a sentence; it may also point to a finding. Question
3 names a forward test even when there are no findings.
**Improve means recommend**: the reviewer proposes the better version ("don't do
this" and "do it differently" count) and the author decides. **There is no
quota of findings.** "No defects found" is allowed only with the three answers
evidenced and the gaps named.

Code review's job is falsification, and its floor is **not the implementing
agent**. It never reopens the Decision (what to build is settled; how it was
built, and what breaks it, is the question). A clean code review reports concise evidence and remaining uncertainty
(`dev/agent_collaboration.md` > "The review sweep").

For test additions or removals, the reviewer asks: **Are permanent tests
limited to external promises worth their runtime (the Pareto 80/20 rule), with
developmental and private-helper tests removed?** This is a coverage question,
not a fourth Foundations answer.

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

A plan whose surface calls for security treatment declares `Plan review:
required(Internal + Internal Security Review)`. Only an appended `## Plan review`
pass whose `**Obligation**` line matches clears it, never an ordinary Internal
pass. No tool reads that line: the next reviewer, the code reviewer and the
Maintainer check it.

**Write for the reader.** Follow Cairn Plain Language (the section of `dev/agent_collaboration.md`): conclusion first, and measured, assumed and expected claims kept apart.

## Keep the plan short

A plan is one file by default: reviews, responses and records are appended to it. Keep what goes in it small. Create a separate artifact only when evidence genuinely needed for implementation or an existing required safety or security ceremony cannot reasonably fit in the concise record or its canonical home. Explain why and cite it in the plan. Do not create sidecars for reviewer convenience or to evade a length limit. Reviews accept concise summaries and may verify when necessary.

* **Count words, not lines — never unwrap lines to look short.** Target an
  opening plan body of **1,000 words (~6 KB)**, `## Acceptance criteria` of
  **150 words per chunk** (state what must hold when the chunk is done, not
  line-by-line code instructions), and each appended review pass or response to
  **300 words (~2 KB)**; these are targets, not trimming triggers. The opening
  budget binds the opening draft. After review, add only what accepted findings
  require, and name the finding for each addition in the response. Wrap prose
  normally; long unwrapped lines save zero
  tokens. When shortening, cut repeatable detail before explanation and shorten
  the Build summary last; a modest clarity-preserving overrun is preferable to
  obscure compression.
* **Never copy template boilerplate or later-stage sections.** Copy only the
  operative headings (`## Build summary` through `## Verification`), replace
  prompts and slot blocks with your plan's specifics (or a one-line `N/A`), and
  do not copy template instructions or the `## Dispositions`, `## Plan review`,
  and `## Code review` sections until those lifecycle steps occur.
* **Scripts and task briefs stay out.** A checker lives in a script or a test
  file, not in the plan. A task brief for a sub-agent is a short note or file,
  cited by path and commit.
  The plan carries the criterion and the result, not the code behind them.
* **A log entry is a pointer.** Commit bodies hold the facts. The entry names
  the commit and adds only a decision, a finding, or a departure from the
  criteria.
* **Cite evidence concisely.** Point to reproducible tests or scripts and state
  their outcome; do not copy probe inventories or mutation-by-mutation results
  into lifecycle records.
* **Read by section.** Give each pass, log or record its own `##` heading,
  titled by what it holds and when it was written. Readers list them with
  `grep -n '^## ' <plan>` and read only the sections the job needs.

## Forward-reference paths

A path that does not exist yet trips `claim_check`. Declare it instead — the
literal `Proposed paths:` line, no blank line before the first bullet, one
physical line per bullet. Drop a line once its path resolves.

**The summary line.** In the `In brief` header line below the rule, write one plain
sentence a scientist outside the project could follow, and keep it on one physical
line because the board reads that line only. `python tools/board.py --json` prints
it as `in_brief` and a view shows it in place of the title; a longer `## In brief`
section below the header is separate and is not read by the board. Leave no
placeholder in a finished artifact, because the board prints whatever the line holds.

---

# Plan: {{short title}}

**Source proposal**: {{dev/proposals/archive/...}}
**Status**: awaiting-plan-review
**Plan review**: {{required(Internal) | required(Internal + Internal Security Review)}}
**Opened**: {{YYYY-MM-DD}}
**In brief**: {{one plain sentence: what changes and why it matters}}

## Build summary

In a few ordinary-language sentences, state the accepted result and the
material outputs this plan will produce or change. Do not repeat the technical
inventory in Scope. This is a reading aid: if it conflicts with operative
Scope, correct the summary to match the accepted work.

## Source proposal

One paragraph: what the proposal decided. The plan executes it.

## Scope

What this plan does and, where it is not obvious, what it deliberately does
not. Name the surfaces it touches.

State the specific useful result and why it advances the accepted objective.
One plan may include dependent internal chunks when together they deliver a
coherent outcome whose implementation, required evidence, reviews and archive
finish without another unfinished plan. Do not split work by default or leave
an accepted outcome unassigned.

For related authorized work in a connected arc, the coordinator decides
whether separate plans and reviews are needed or a shared arc scope and review
cover it. Do not create a plan or review artifact per work item when that
shared record actually covers it. Grouping keeps all required ordinary and
Security Review coverage, scientific checks, Human Decisions and fences,
model/data floors, and trust operations due. Outside a connected arc, apply
existing tier defaults: light work has no plan; nontrivial standard/heavy work
uses the usual plan and reviews.

**Reuse.** What existing code does this reuse or generalize? Where did you
search for near-duplicates (query or path, and what it found)? "None" needs a
named search; for no code added, write `N/A: no code added`. A near-duplicate
does a job existing code already does under another name or with a small
change; intentional copies pinned as identical are not near-duplicates.

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

Show that the goal is achievable with the capabilities and prerequisites
available to this plan. Give a realistic work-window estimate and name material
uncertainty; it is a planning estimate, not a deadline or a waiver of accepted
work. Open only outcomes with their needed authority and resources available.
Keep an outcome waiting for an unavailable approval or passive calendar
observation queued on the existing board with its proposal source, owner and
concrete restart condition. A ready, approved scientific observation remains
implementation work even when it spans days; include that duration in the
estimate. Missing required evidence still leaves the outcome unverified. A
shipped capability may be a prerequisite; another plan's future review,
archive or release may not be required to finish this plan.

One row per chunk: what it does, what gates it, roughly what it ships. Mark a
chunk MAINTAINER-GATED or MAINTAINER-ONLY only when an actual decision or
permission is load-bearing to carry out accepted work. Do not use a fence for a
routine approval or passive calendar wait. If work already opened encounters
unexpected missing authority, stop that action and use the Waiting line
(`**Waiting on Maintainer**: <what>`) in the header block, beside Status; delete
it when the Maintainer answers.

Cheap follow-ups mean a few person-steps, no new Decision or public name beyond
the plan, and a test that fits existing test files. This is not the narrower
cheap defect-fix exception in `AGENTS.md`. Code review identifies cheap
findings and advice; in the code-review response, fix each before archive or
use an existing deferral reason with the Maintainer's verbatim authorization.
Cheapness grants no scope, boundary or required-check waiver. Non-cheap advice
keeps its existing disposition, and a required failed check remains
implementation work.

A fence is for a Decision or permission needed to carry out accepted scope,
not a routine human-run trust or release operation. A plan reaches
`ready-to-archive` after its agent-owned scope, required reviews, applicable
checks, findings and dispositions are complete. Track a human operation in a separate,
named standalone board wait with its owner, evidence and link to the
implementation; do not create a release plan. Keep its result unpassed until
its evidence exists. A reviewed baseline awaiting a specifically named human
operation remains unpassed; an unexplained integrity failure remains
implementation work.
Do not make a routine human-run trust or release operation a final plan chunk
or a condition of completion.
Missing checks, defects and functional or scientific evidence stay in the
implementation. Archive is not permission to activate or release; an issue
closes at its fixing commit, not at release.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | | | |

## Acceptance criteria

Make completion observable against the useful result in Scope. Per chunk, each
criterion is falsifiable; do not substitute a count of files or checkboxes for
evidence that the outcome works. A criterion you cannot imagine failing is not
one.

Optional prompts for a criterion: condition, observable behavior, behavior
that must remain unchanged, and the check that demonstrates the result. Use
only prompts that help make the outcome observable. EARS is optional; one form
is `WHEN <condition> THE SYSTEM SHALL <observable behavior>`. Example ordinary
defect: current behavior: `greet("Ada")` returns `Hello, world!`; expected:
`Hello, Ada!`; unchanged: `greet()` still returns `Hello, world!`; check: the
named-greeting and default-greeting tests. These prompts do not replace accepted
scope or required checks.

For each change, name the caller-visible promise it adds or alters and the
public entry point that checks it. Separate temporary developmental checks
(deleted before archive) from permanent promise tests (often none when an
existing public promise check covers the branch); do not request a permanent
test only because the implementation changed.

A security-touching plan re-answers the five security-preflight
questions only where its chunking changes an answer — most often S2
(which existing negative control applies, or which new check demonstrates a
failing case) and S3 (which gate command fires the check).

**An independent scientific check is accepted scope.** If the proposal names
one, it becomes an acceptance criterion. A replacement qualifies only if it
fails under the error the original names. If nothing qualifies, dropping the
check is a scope reduction under *Scope delta* and needs the Maintainer's
quoted allowance. Saying that the result now rests on the implementation does
not settle it. When the check fails for real during implementation, one line
records whether anything else would have shown the error.

Record scientific evidence with the work or release that requires it. A run is
not part of routine tree certification merely because it is scientific, but a
configured suite member and every other applicable requirement remain required
at each required point. Subject or duration does not authorize a waiver or
rescheduling.


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
scope."** Neither author nor reviewer may concede a baseline outcome; only the
Maintainer can.

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

For each plan, name changed caller-visible promises, public entry points and
outputs, then select the smallest checks that could expose plausible faults.
Group equivalent paths. Reuse a result only when its tested bytes, platform,
input and obligation still apply; cite its source and limit. A changed boundary,
failed check, uncovered fault or explicit requirement expands the selection.
For a claim about every member, inventory the set and check each applicable
path without making a separate mutant for each. Permanent tests guard external
promises; temporary development probes leave before archive. Forward behavior
needs executable evidence before completion; forward structure can be checked
on committed structure. Missing or failed required evidence keeps work open.
Preserve required security checks and reviews, scientific independent error and
positive controls, and release operations.

**Example.** A plan changes the public summary from `upgrade --plan` and checks
that output with the same command. It reuses the existing denied-path control,
citing that it covers denial but not successful installation. After connected
plans finish review, the arc owner joins their selected checks against the final
combined revision.

<!-- cairn:slot verification-commands -->
Use the project's test-tier tool's `for <paths>` subcommand to list tests that
import or cite changed files. This is the iteration scope; do not widen it by
judgment. Run applicable standing prose gates for prose. For governing text,
pass the complete reviewed range when required. The selector claims no unknown
dependencies. Keep canonical runtimes and standing project checks in their
existing homes.

The arc owner joins connected work after reviews and dispositions, or earlier
at a named critical shared boundary. Use the canonical runtime and applicable
standing gates. Cover the clean final combined revision before arc completion
or release; record the revision, selected producers and consumers, results and
omissions in the existing verification record. Applicable prior results may
cover unchanged behavior and inputs. After a repair, rerun only affected
checks. A post-archive defect belongs to the arc owner, who records and repairs
it under existing rules without reopening the archived plan. Do not replay the
whole selection solely to stamp a new commit ID. A failed promise or required
check remains plan work before archive.

Record each tree certification once in its existing release/re-anchor
record. For another authorized run, include SHA, commands, results and failures
in a useful commit message under `Tree certification -- <tested SHA>`; readers
can find it with `git log --all --grep='Tree certification --'` among locally
fetched refs. Create no record-only commit and backfill no archive; absence is
not evidence of a pass.
<!-- cairn:end verification-commands -->

Code review remains an independent required review. Reviewers may use committed
code and existing evidence when adequate, reserving a fresh probe for a specific
uncertainty. Tree certification and trust ceremonies retain their existing
authorized triggers and required checks.

<!-- Later-stage sections — do NOT copy into a new plan; append each
     section only when that lifecycle step occurs. -->

## Dispositions

*Appended at archive-preparation (see Cairn's published lifecycle method > "Archive
precondition" and published plan method > "Lasting-truth migration
doctrine").* Record one `Dispositions: ...` line per deferred follow-up:
`accept` (fixed in scope), `guard (<path>::<node>)` (homed in an executing
test/check, never a comment), `wontfix` (with rationale; ineligible if it
reaches an adopter, blocks a release, needs a Decision, or was named by a
closed artifact's disposition block without Maintainer approval), or `defer`
(deposited in `dev/PLANNING.md` or an open plan, with the Maintainer's
verbatim authorization and reason: needs a decision, belongs to in-motion
work, or exceeds the cost bar). Present `defer` requests as one batch and set
`**Waiting on Maintainer**: <what>` in the header until answered; an archiving
plan carries no Waiting line and leaves no item homed only in an archived
file.

## Plan review -- <reviewer> -- <YYYY-MM-DD>

Target 300 words for this pass, preserving its verdict, findings and coverage gap.
Explain any over-target pass in its coverage line.
Record elapsed time and reported or defensibly estimated token use; write
`unknown` when unavailable.

Open every pass with its basis, so a later reader knows what was actually read:

```
Reviewed commit: <full commit id>
```

**Obligation**: <the one clause this pass clears>
**Tier**: <Internal | Internal Security Review>
**Findings**: <raised | none>

*On a read the Maintainer called, replace the Tier line with these two, with the Maintainer's
words beneath them, verbatim and apart:*

**Tier**: External
**Called by**: Maintainer -- Decision at <commit>

**Foundations** (the plan row; one line per answer, each ending in the file,
test, line or command that backs it):

1. **Should this happen as framed?** <the Decision settled the premise; does the plan deliver it> -- <evidence>
2. **Best alternative.** <a simpler path to the same outcomes> -- <evidence>
3. **What would show it wrong.** <the result showing it cannot deliver> -- <evidence>

When the plan changes functional prose, also answer the reading question:
**Does any rule weaken or disappear?**

An H3 inside another pass does not count as a pass of its own — a heading at
the left margin is what the checker reads.

## Code review -- <reviewer> -- <YYYY-MM-DD>

Target 300 words for this pass, preserving its verdict, findings and coverage gap.
Explain any over-target pass in its coverage line.
Record elapsed time and reported or defensibly estimated token use; write
`unknown` when unavailable. Report verification and mutation outcomes and any
unresolved or unmeasured cases concisely; keep repeatable evidence in tests or
scripts.

Code review's floor is not the implementing agent; a fresh session clears it. It
never reopens the Decision. Self-committed by its author; blocking findings move
the plan to `revising-code`, and the implementer's answer carries it to
`ready-to-archive`. A second code-review pass runs only when the revision
introduced new defects, never to re-confirm that the first round's findings were
addressed. Same basis block, with the range made explicit:

```
Reviewed commit: <full commit id>
```

**Foundations** (the code row; one line per answer, each ending in the file,
test, line or command that backs it):

1. **Should this happen as framed?** <does it really do what it claims; try to break it, in order to fix it> -- <evidence>
2. **Best alternative.** <a simpler or safer build, if any> -- <evidence>
3. **What would show it wrong.** <the input or run that breaks it, and what was tried> -- see the review evidence (`dev/agent_collaboration.md` > "The review sweep")

When the reviewed change edits functional prose, also answer the reading
question: **Does any rule weaken or disappear?**

For test changes or removals, also answer: **Does every removed caller-visible
fault remain caught by a retained promise check through its public entry
point?**

**Bounding**: ACCEPTED | WIDER RUN REQUIRED — recorded only after challenging a
named surface, mapped test, or stated omission. The second verdict names the
missing behavior and check; the author adds it and records new final-commit
evidence before acceptance.

**Waiting-line check.** `git log -p` on the plan must show a Waiting line for
each fenced chunk whose fence became the next move inside the reviewed range,
and for each deviation request made in it. A fence the range did not reach is
not checked, and one whose wait is declared on a marked board row is checked
there. A missing line is a finding, recorded in
the project's incident tracker.
