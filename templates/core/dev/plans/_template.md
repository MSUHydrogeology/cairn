External-repo paths: `docs/methodology/plans.md`, `docs/methodology/lifecycle.md`
<!-- The plan template. Copy only the opening header and operative section
     headings (`Build summary` through `Verification`) below the rule into
     `dev/plans/<YYYY-MM-DD>-<slug>.md`, replace every prompt with your answer
     (or `N/A`), and re-read this file before writing or revising; its word
     budgets and copy rules change. -->

# Plan template
Written in [Cairn Plain Language 1.0](../agent_collaboration.md).

A non-trivial accepted standard/heavy proposal opens a plan. Light has no plan,
even for multi-area or wide work; its accepted proposal holds Boundary B
evidence after implementation. The plan says how the work
happens and how you will know it worked; it does not re-argue the decision.

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

**Reviews, responses and decisions append and are never edited. Operative
cells — Scope, Sequence, Acceptance criteria, Verification — revise in place
until implementation begins.**

**Revise operative text in place.** A proposal Response revises the proposal's
current text; reviews, earlier responses and decisions remain appended. A plan
response disposes of findings and points to corrected plan cells. Revise those
cells in place until implementation begins; after a chunk begins, changes
append instead.

**Deviating from an accepted plan takes the Maintainer's word** — new scope, a
contract review never saw, an acceptance criterion you cannot meet, **or
accepted scope removed**. Removal counts in both directions: accepted scope is
a floor, and a reviewer cannot create authority to narrow by calling the
remainder out of scope.

A defect fix made under the defect-fix rule
(`AGENTS.md` > "Working tree and commits") is not new scope.

**The Waiting line.** When a plan's next move becomes the Maintainer's, write
one header line, `**Waiting on Maintainer**: <what>`, in the header block,
beside Status, and delete it when they answer. Write it at three moments: work
reaches a fenced chunk (one marked MAINTAINER-GATED or MAINTAINER-ONLY), you
put a `defer` batch to the Maintainer, or you make a deviation request. Keep
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

For test changes or removals, the reviewer also asks: **Does every removed
caller-visible fault remain caught by a retained promise check through its
public entry point?** This is a coverage question, not a fourth Foundations
answer.

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
work. Work that depends on an unavailable future plan stays queued on the
existing board with its proposal source and revival condition. A shipped
capability may be a prerequisite; another plan's future review, archive or
release may not be required to finish this plan.

One row per chunk: what it does, what gates it, roughly what it ships. Mark a
chunk MAINTAINER-GATED or MAINTAINER-ONLY where approval is actually
load-bearing — that fence, not a blanket per-commit gate, is where approval
binds to something specific. When work reaches a fenced chunk, write the
Waiting line (`**Waiting on Maintainer**: <what>`) in the header block, beside
Status, and delete it when the Maintainer answers.

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
checks and Boundary B are complete. Track a human operation in a separate,
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
public entry point that checks it. Identify the existing promise test or the
plausible uncovered fault that requires a new or extended check; do not request
a test only because the implementation changed.

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

**Boundary A (iteration, scoped).** The tests owning each touched surface,
plus its standing gates.

Select coverage from the promises and boundaries affected. Start with component
ownership and the project's test homes: unit checks for local behavior,
contract checks for public interfaces and data formats, integration checks for
connected components, and a small workflow through the real entry point. For
simulations, use real equations on small domains and analytical or convergence
benchmarks when relevant; retain work-specific long runs where the scientific
question requires them. Trace changed behavior through callers, imports,
configuration and data readers, and public paths; map existing checks to
affected components and consumers. Add or extend a test only for a plausible
uncovered fault. Local effects default to affected checks. Shared contracts,
common infrastructure, language seams, solver or physics behavior, and
uncertain dependencies widen to owning families and relevant consumers. Name
uncertainty and the smallest useful remedy when dependencies cannot be bounded.
Routine mapping belongs to the implementation and is challenged by review;
Maintainers set high-level project needs and material exceptions.

<!-- cairn:slot verification-commands -->
Before implementation, use the project's test-tier tool's `for <paths>`
subcommand to list tests that import or cite each changed file by path or file
name. This list is
the iteration scope; do not widen it by judgment. Run applicable standing prose
gates for prose. For governing text like AGENTS.md, if the broad list exceeds
the runner's limit, the selector returns only tests pinning changed passages
and reports the rest as omitted. Folder sweepers are covered by the release
run. The selector claims no unknown dependencies. A known missing path,
required check, or unmet criterion keeps the change open.

Boundary B runs once after code review, on a clean, unchanged final commit
under the configured interpreter/runtime. It consists of the iteration list
for every file in the reviewed range, plus integration and workflow tests in
the tier map that name those files. Record
`**Boundary B mode**: bounded | wide`. Use `wide` for a contract or
trust-ceremony surface. A contract change includes its producers, consumers,
and public paths; a trust ceremony retains every prescribed security and
ceremony check. `bounded` covers mapped affected behavior and consumers;
`wide` covers owning test families, known integration and public paths, and
standing gates when effects cannot be confidently bounded. The change record
is separate from tree-certification evidence. A scoped certification names its
tested commit, components, checks, results and omissions in the existing record. It claims no unrelated or untested combined
behavior or earlier changes, and reopens if a later failure contradicts it.
Required project checks and ceremonies remain owed; a full suite runs when an
applicable requirement calls for it. Broader certification does not replace
missing change evidence.

Record each actual tree-certification run once: use the existing release or
re-anchor evidence for those ceremonies. For another authorized run, put a
`Tree certification -- <tested SHA>` section with the SHA, commands, results,
and any failures in a useful commit message in shared project history. After
fetching the relevant shared refs, readers can search
`git log --all --grep='Tree certification --'`; it searches only refs available
locally. Do not create a commit just for this record or backfill archived plans.
An absent record does not show that a run passed.
Timing targets are 30 seconds for iteration, 10 seconds per test file, 3
minutes for integration, and 10 minutes for certification. These are
diagnostics, not agent scores; a miss does not block work. Record misses and
add each test file over 10 seconds to the test-consolidation list, slowest
first.

The commands and checks named for Boundary B are the mapped tests, each
surface's standing gates, and all plan-specific acceptance commands, including
documentation, schema, snippet, security, and public-path checks where they
apply. Name the command and the property it checks; record `N/A` with a reason
when none applies.

Only after that stable run, append a dated section named
`Implementation verification -- <agent> -- YYYY-MM-DD` at H2. Do not place an
empty heading in a new plan. The record uses these exact fields:

* **Boundary B mode** — `bounded` | `wide`. On `bounded`, name the touched
  surfaces, mapped tests and standing gates, why the effects are bounded, and
  how affected consumers are covered. On `wide`, name the owning families,
  known integration/public paths, and gates run, and explain why narrower
  bounds were not confident.
* **Tested commit** — full revision ID.
* **Reviewed range** — base and tested endpoint.
* **Interpreter/runtime** — canonical path and version.
* **Pre-run state** and **Post-run state** — clean tree and identical tested
  revision.
* A command table with **Command**, **Exit**, **Outcomes**, **Elapsed**, and **Tokens**
  columns, including pass/fail/skip/xfail/xpass counts where applicable.
* **Non-pass disposition**, **Plan-specific acceptance commands**, and
  **Known omissions**.

Close the implementation verification record with one concise sentence
judging whether the delivered benefit justified the observed effort and
remaining burden. Say `unknown` when evidence cannot support that judgment.
This is a retrospective in the existing record, not another archive gate,
score, timesheet or Maintainer response.

Also name the project's documentation, schema, snippet, security, and smoke
gates here. If none applies, record `N/A` with a reason rather than omitting the
surface silently.
<!-- cairn:end verification-commands -->

**Boundary B (integration).** Run after code review as specified above; the
dated record below names the mode, checked consumers and public paths. A
known missing check keeps the change open.

Append the evidence as `## Implementation verification -- <agent> -- YYYY-MM-DD`:
tested SHA, interpreter, clean pre/post state, commands, outcomes, elapsed time,
token use or `unknown`, disposition of every non-pass, known omissions.

**Boundary C (falsification)** is the code reviewer's, before Boundary B. Read
the implementation and iteration evidence, then run only targeted checks that
could falsify the change; never run a suite. Name a specific missing test when
coverage is absent, and have the author add it. The final integration run then
covers all review fixes. If a fix after a failed integration run changes more
than the failing test, return it to the same reviewer for a targeted look
before rerunning the integration selection. Tree certification remains a
separate authorized integration run; a ceremony keeps its own required checks.

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
