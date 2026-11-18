<!-- The proposal template. Copy only the opening header and section
     headings (`Decision summary` through `Assurance path`) below the rule into
     `dev/proposals/<YYYY-MM-DD>-<author>-<slug>.md` and replace every prompt
     with your answer (or a one-line `N/A`). Re-read this file before writing
     or revising; its word budgets and copy rules change. -->

# Proposal template
Written in [Cairn Plain Language 1.0](../agent_collaboration.md).

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

Release-side content should cite deliberation by date and topic, not by a
`dev/` path; development guides may cite development records.

## Lifecycle

```
awaiting-review <-> revising -> awaiting-decision
                             -> accepted / rejected / superseded
```

Each status names **who holds it next**. A review moves a proposal to
`revising`; the author's response carries it to `awaiting-decision`. One usual
proposal review and response suffice.  In the usual proposal
review, consider whether the Maintainer could explain the choice
without a live translation. This is a reading judgment, not a checklist or
score.
`accepted` is terminal — archiving is a file move, not a status.

Two rules are bright-line:

* **Revise operative text in place.** Update the current proposal sections
  rather than appending a full replacement. Git history preserves prior
  wording. Reviews, responses and decisions remain appended and unchanged.
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

For functional-prose changes, also ask: **Does any rule weaken or disappear?**
This is a reading question, not a fourth Foundations answer.

Each pass opens with a **Foundations** block of three lines, one answer per
question, each ending in the file, test, line or command that backs it. Each
answer states its point in a sentence; it may also point to a finding. Question
3 names a forward test even when there are no findings.
 "No defects found" is allowed only with the three answers
evidenced and the gaps named.
Reviews are **attributed and self-committed**: a review you did not write is not
yours to sign, and an independent read is only independent if its author is its
committer.

**More distance is the Maintainer's call, and only theirs.** See `dev/agent_collaboration.md` > "Review rules".

A change gets the heavy tier when it alters what a high-risk surface does or accepts, or adds a place where outside input meets the system; merely touching a surface does not. A template is not high-risk solely because it contains prose; code, installer structure, and functional configuration may remain high-risk under the project's written list. When in doubt, take the Security Review (`dev/agent_collaboration.md` > "Review rules"). A project rule that names its own Security Review still applies. `usual + Security Review` in a
header means two passes: the usual pass and a Security Review pass that names its
own obligation. The usual pass never clears the second.
In a proposal review, `**Tier**: Security Review` names that obligation; the
skeleton does not call for a separate `**Obligation**` line.

**Write for the reader.** Follow Cairn Plain Language (the section of `dev/agent_collaboration.md`): conclusion first, and measured, assumed and expected claims kept apart.

**Rules that apply.** List the rule file paths from the `RULES.md` routing table that apply, never rule text, or write `bright lines only`. A rule that applies but is not listed is still followed; add it to the line. The line never narrows a review, a Security Review trigger or a protected-surface obligation. Reviewers compare it with Scope.

## Keep the proposal short

The proposal stays one file: reviews, responses and decisions are appended to it. Keep what goes in it small.

* **Count words, not lines — never unwrap lines to look short.** Target an
  opening proposal of **1,000 words (~6 KB)** and each appended review pass or
  response of **300 words (~2 KB)**; these are targets, not trimming triggers.
  The opening budget binds the opening draft. After review, add only what
  accepted findings require, and name the finding for each addition in the
  response. When shortening, cut repeatable detail available elsewhere before
  cutting explanation; shorten the Decision summary last. A modest
  clarity-preserving overrun is preferable to obscurity.
* **Never copy template boilerplate or later-stage sections.** Copy only the
  opening headings (`## Decision summary` through `## Assurance path`) below
  the rule;
  replace prompts and gated blocks (`Security preflight`, `Independent
  scientific check`) with your answer or a one-line `N/A: ...`, and never copy
  template instructions, slot comments, or the `## Review`, `## Response`, and
  `## Decision` skeletons until that lifecycle step occurs.
* **Scripts and task briefs stay out.** A checker lives in a script or a test
  file, not in the plan. Put temporary briefs, drafts and script scratch output
  in the ignored dev/scratch/ folder; keep durable conclusions in existing
  records. Cite a committed task brief by path and commit.
  The proposal carries the criterion and the result, not the code behind them.
* **Cite evidence concisely.** Point to reproducible tests or scripts and state
  their outcome; do not copy probe inventories into lifecycle records.
* **Read by section.** Give each review, response or decision its own `##` heading, titled by what it holds and when it was written. Readers list them with `grep -n '^## ' <proposal>` and read only the sections the job needs.
* **Appendix.** Default none. Allowed only for a table or arithmetic a reviewer must check that no cited record can hold: one separate file per proposal, `<proposal-stem>--appendix.md`, beside it, never inline. The board skips it; session start still lists it. The 1,000-word budget applies to the text at the Decision, so cut or move review additions before it.

## Forward-reference paths

A path that does not exist yet trips `claim_check`. Declare it under a literal
`Proposed paths:` line — no blank line before the first bullet, one physical
line each. Drop a line once its path resolves.

**The summary line.** In the `In brief` header line below the rule, write one plain
sentence a scientist outside the project could follow, and keep it on one physical
line because the board reads that line only. Leave no placeholder in a finished
artifact, because the board prints whatever the line holds.

---

# {{proposal title}}

**Author**: {{agent or human}}
**Status**: awaiting-review
**Review**: {{usual | usual + Security Review}}
**Proposed tier**: {{light | standard | heavy}} — light is the default; the author may propose a higher tier, which stands unless the Decision changes it
**Plan review**: {{required(Internal) | required(Internal + Internal Security Review)}} — for light, use `not required(no plan: light tier)` even for multi-area or wide work; standard/heavy use plan triage and may use `not required(no plan: <how each plan-skip condition holds>)`
**Opened**: {{YYYY-MM-DD}}
**Rules that apply**: {{rule file paths from the RULES.md routing table | bright lines only}}
**In brief**: {{one plain sentence: what changes and why it matters}}

## Decision summary

Briefly name in plain language the issue people notice, proposed change, material outputs added, changed or removed, and meaningful costs or tradeoffs. Define technical terms at first use; give a concrete example when it clarifies an abstraction. Supporting evidence and technical detail go below. This reading aid is not another scope contract; correct mismatches to the operative proposal text.

## Context

Describe current state and problem with evidence; demonstrate claimed failures.

## Proposal

What changes. Be specific enough that a reviewer can disagree with something.
State each useful delivery outcome, its prerequisites and intended release or
capability. A proposal may authorize several plans; retain later outcomes on
the existing board with this source and a condition for reviving each one.
The first plan opening archives the accepted proposal under the existing rule;
later unchanged authorized work remains linked to that immutable source and
does not need a new Decision. Preserve all accepted outcomes and checks. Do not
split work into plans by default; one plan may include dependent chunks that
deliver one independently finishable outcome. Its required implementation,
reviews, checks and archive must not wait on another unfinished plan. Keep
routine human operations as separately owned, evidenced waits, never as final
plan tasks. Failed required checks remain implementation work.




## Rationale

Why this rather than the obvious alternative. If the change is costly, say what
it buys.

## Alternatives considered

At least one real one, with the reason it lost. "We considered doing nothing"
counts only if you say what doing nothing costs.

## Documentation / doctrine surface

Name affected documentation, doctrine and contract surfaces and their destinations.

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

For each implementation change, name its caller-visible promise and public entry point. Identify a plausible uncovered fault or extend an existing promise test; do not propose a test merely because a change exists.



<!-- cairn:slot tests-tier-home -->
(Name the project's test homes, affected behavioral nodes and public paths exercised through their real entry points.  Record speed or environment tiers, but speed alone does not establish affected coverage. The reviewed plan maps changed behavior, not a permanent fast set: `bounded` covers affected behavior and consumers; `wide` covers owning families, known integration, public paths and standing gates. Name uncertainty; never claim unknown dependencies covered, and keep known unmet checks or criteria open. Certification cannot replace a missing check.
 Fill from the project's test plan, or replace with
`N/A: no test layout` plus the project's scoped test procedure.)
<!-- cairn:end tests-tier-home -->

### Examples / smoke checks

<!-- cairn:slot examples-smoke-home -->
(Adopter-specific examples / smoke-check surfaces — the gallery, CLI
sanity commands, notebook smokes the change can exercise end-to-end.
Fill with the project's runnable checks, or replace with `N/A: no
end-to-end exercisable surface`.)
<!-- cairn:end examples-smoke-home -->

#### Security preflight — five questions, answered in writing

*Gated to a **security-touching** change: one that adds or widens a
trust boundary (deserialization, subprocess invocation, parsing, file and path
handling, network I/O, credentials and environment), or one that alters what a high-risk surface this project's `AGENTS.md` names does or accepts. When in doubt, take the Security Review (`dev/agent_collaboration.md` > "Review rules"). For every other change, one
line — "N/A: no trust boundary added or widened" — is the correct
entry.*

Answer all five, one or two sentences each. These are **design questions, asked
while the design is still movable** — not documentation written after it is
fixed. An absent answer is a review finding; a *wrong* answer is a falsifiable
one.

Structural questions about where material comes from and what runs. They do not
check whether an answer is *true*; they convert a hidden property into a written
claim a reviewer can falsify. Prospective only — an archived artifact is never
retro-fitted with them.

* **S1 — Who supplied it?** For each step where this change *decides*
  something (verifies, authenticates, authorizes, classifies, admits), name
  every input and the channel it arrives by, and say whether any input is
  supplied — directly or **by reference** — by the thing being decided about.
* **S2 — Can it fail?** For each check this change relies on, cite an
  applicable existing negative control, or for a new check state the one-line
  mutation that makes it fail and confirm the failing case. **If a check derives
  what it expects from the same object it is checking, say so plainly — that
  check cannot fail.**
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
  failing run.

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
(Adopter-specific high-assurance triggers beyond the mandatory list above —
the project's own protected surfaces, its scientific-assumption or
unit/CRS-convention classes, its release or trust ceremonies. Fill with your
project's bullets, or replace with `N/A: no project-specific high-assurance
triggers`. An unfilled slot is a review finding.)
<!-- cairn:end assurance-path-triggers -->

<!-- Later-stage sections — do NOT copy into a new proposal; append each
     section only when that lifecycle step occurs. -->

## Review -- {{reviewer}} -- {{YYYY-MM-DD}}

```
Reviewed commit: <full commit id>
```

**Tier**: {{usual | Security Review}}
**Findings**: {{raised | none}}
**Verdict**: {{ACCEPT | REVISE}}

**Elapsed**: <duration>
**Tokens**: <reported or defensibly estimated count | unknown>

*On a read the Maintainer called, replace the Tier line with these two, and set
the Maintainer's words beneath them, verbatim and apart:*

**Tier**: External
**Called by**: Maintainer -- Decision at <commit>

**Foundations** (the proposal row; one line per answer, each ending in the file,
test, line or command that backs it):

1. **Should this happen as framed?** {{should this exist as framed, and is there a better design, doing nothing included}} -- <evidence>
2. **Best alternative.** {{the strongest, doing nothing included}} -- <evidence>
3. **What would show it wrong.** {{what would make the author withdraw}} -- <evidence>

When the change edits functional prose, the review also answers the reading
question: **Does any rule weaken or disappear?**

Lead with the strongest version of what the proposal is trying to do, then the
findings (blocking or non-blocking, with the evidence that closes each). If
answering a Response, also verify its withdrawal ledger.

## Response -- {{author}} -- {{YYYY-MM-DD}}

List one disposition per finding and the reason. Revise operative proposal
text in place; do not repeat it here. End with a real H3 headed
`### Withdrawn / superseded commitments` listing commitments replaced or
dropped and why, or `None` if none. Reviews and prior responses stay intact.
Record elapsed time and token use for this step; use `unknown` when unavailable.

## Decision -- {{Maintainer}} -- {{YYYY-MM-DD}}

Record elapsed time and token use for this step; use `unknown` when unavailable.

**Tier**: {{light | standard | heavy}}

Light is the default and requires no plan regardless of implementation size. A change gets the heavy tier when it alters what a high-risk surface does or accepts, or adds a place where outside input meets the system; merely touching a surface does not. A template is not high-risk solely because it contains prose; code, installer structure, and functional configuration may remain high-risk under the project's written list. When in doubt, take the Security Review (`dev/agent_collaboration.md` > "Review rules"). A project rule that names its own Security Review still applies.

**{{ACCEPTED | REJECTED | SUPERSEDED}}.** The Maintainer's authorization,
quoted **verbatim and visually isolated** (no paraphrase):

> "{{the authorizing words}}"

An agent may scribe a Decision only on an unambiguous instruction, and the
commit carries nothing else.

## Implementation verification -- <agent> -- YYYY-MM-DD

*Append for light work only; the accepted proposal is its implementation and
verification record.* Record the selected changed-promise checks, tested
revision, canonical runtime, commands and results, non-pass dispositions and
omissions. Cite reused results and their limits.  Record elapsed time and tokens, using `unknown` when unavailable.
