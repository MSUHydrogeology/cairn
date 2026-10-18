# Fix easy problems where you find them, and look before you build

**Author**: Claude (Strategy)
**Status**: accepted
**Review**: required(Internal)
**Plan review**: required(Internal)
**Opened**: 2026-10-18
**Current contract**: Revision 1, at the end of this file. Read its *In brief* and *Questions for the Maintainer*; the sections above them are history.

## In brief

Cairn's rules make **putting a problem off** the cheapest thing an agent can do with it. ("Deferring"
means parking an item in a later issue or on the roadmap board instead of fixing it now.) At one
archive in your LHM project, 13 review findings were deferred. Sorted afterwards, 5 truly had to wait
and 8 were easy fixes, filed only because filing was easier. The same session was about to write a
surface-to-groundwater mapping for the third time. Your direction, from issue #30:

> "A human would fix a problem that is easy when they encounter it--thereby adding value whenever they look at code"

**What changes**

1. A deferral says *why*: it needs your decision, it belongs to work already under way, or it is over
   the cost bar. "Non-blocking" and "nit" stop counting as reasons.
2. A known, easy defect in a file the work is already editing is fixed there, with its own test, and
   written down. This needs one narrow exception to the rule that new scope takes your word.
3. The issue-capture module's default flips: fix when cheap, capture otherwise.
4. Before building, the plan says what existing code it reuses and where the author looked for
   near-copies. A reviewer treats a new near-copy as a real finding, not a nit.

**Two things keep "easy" honest.** "Cheap" counts ceremony, not only lines: a one-line change to the
install engine still costs you a re-anchor and a Security Review, so it is not cheap. And the exception
does not cover changing what a rule says, so a fix like `941cb34d` (a new sentence in three governing
files) would still come to you.

**What I cannot show.** The evidence is one adopter session, your direction, and a same-shape finding
on Cairn's own board in August. The rate-limit gate asks for more than that. Question 5 puts it to you.

It builds on the verification-practice work (#25) and the maintainer-attention work (#28), both closed,
and re-proposes neither. It adds no tool.

## Questions for the Maintainer

Each has my default. An unanswered question takes it.

1. **What counts as cheap?** *Default:* a fix is cheap when it needs no decision, comes with its own
   test, fits in about a chunk's worth of the plan it joins (a chunk is one row of the plan's
   sequence), and sets off nothing beyond the change's own review: no high-risk surface, no contract
   surface, no file a gate pins by hash, no step only you can run. Doubt means not cheap. Adopters
   may set their own bar. The alternative, a line count, cannot see ceremony.
2. **May a fix that meets every condition skip your word?** This loosens the deviation gate, which is
   one of the four things approval attaches to. *Default:* yes, for a defect already on the record
   before the work began (an issue, a review finding, a board row, an earlier plan note). A defect met
   fresh is recorded first and fixed on the next touch, or brought to you.
3. **One line about reuse in both `AGENTS.md` files?** Trivial changes and plan-less proposals never
   meet a plan template, so the line is the only carrier for them. *Default:* yes, four lines, in
   "Project-specific conventions".
4. **Order.** *Default:* this proposal's plan **follows** the combined plan of the review-stance and
   review-lenses proposals and opens when that plan archives. It does not fold in. Say "fold" and my
   work rides in that plan, which grows by about 15 files and puts a prose-only change under a
   Security Review it does not need.
5. **The rate-limit gate.** The evidence does not clear it on its own (section below). *Default:*
   proceed on your direction, and let the Decision say so, which makes the override a recorded
   decision rather than a quiet one. Say "hold" and this waits for a second recurrence.

## Context

**Source.** Issue #30, filed from LHM on 2026-10-18 (`gh issue view 30`). The counts in it (13
deferrals, 5 and 8) are LHM's, from its own archive. I did not re-count them.

**The shipped text pushes toward deferral in four places.** Quoted from the tree at `7e11b316`:

* `templates/modules/team-gated/issue-capture.md` > "Capture vs. fix inline" (the `dev/modules/`
  copy is identical): "**capture friction as an issue rather than fixing it inline mid-session**,
  unless the fix is trivial and in-scope for the current work... The exception is the genuinely
  one-line, on-path fix."
* `doctrine/plans.md`, the plan-review priority labels: "`(nit)` — clarity / polish; defer-OK."
  (`doctrine/` is not installed in an adopter's tree, so this one shapes Cairn's own reviews and any
  agent that reads the doctrine. The three other places reach adopters.)
* `doctrine/dual-review.md` > "The blocking test": "No → `note` / `nit`, recorded, non-blocking."
  This is where "non-blocking" is defined. It answers whether shipping does damage that is hard to
  undo. Nothing there says it also answers whether the finding may be put off.
* `doctrine/lifecycle.md` > "Archive precondition", restated in the plan template's *Dispositions*: a
  `defer` needs a live home and your quoted authorization, but nothing asks *why* it was not fixed.

**Where the issue overstates.** It says nothing puts a cost on deferring. Since the `deferral-discipline`
plan (`dev/plans/archive/deferral-discipline.md`, 2026-08-04) a `defer` needs your quoted words at the
archive batch, and the lifecycle says a disposition is not a durable home. In LHM's case you saw the
batch and asked, and the issue notes the homes were the reviewer's suggestions, not your authorization.
Either way the sorting was left to you. What is missing is that the author sorts first, by a stated
test.

**A ruling this must respect.** That same work dropped a strict order among dispositions on purpose:
"There is no required order... An ordering rule would make the cheapest disposition the default."
(`doctrine/lifecycle.md`). The earlier draft had "fix in scope" first and a reviewer showed the order
tilted toward declining (`dev/proposals/archive/2026-08-04-claude-deferral-discipline.md`, finding I9).
This proposal adds no order. It prices the one disposition that hands the cost to someone else.

**Two rules collide, and only one of the four rules triggers it.** `AGENTS.md` > "Git and commit
workflow": "**A deviation from the approved plan** — new scope, a struck chunk revived, a contract the
review never saw, an acceptance criterion you cannot meet, **or accepted scope removed**." Rule 1
(fix review findings before archive) collides with nothing: a finding on the plan's own change is
fixed by a sharpening commit today ("Sharpening fixes land as follow-up commits before the plan
archives", `doctrine/plans.md`). Rule 2 (leave the file better) does collide. A defect that nobody put
in the plan, fixed because the file was open, is new scope, so an agent would break one rule to follow
the other.

**What cheap costs in this tree.** `AGENTS.md` > "High-risk surfaces" is headed "Security-Review +
proposal triggers", and the scaffold engine (`bootstrap/_scaffold/`) is the first entry. Past the
self-service allowlist, a change there owes a Maintainer-run AST re-anchor
(`bootstrap/AST_BASELINE_RUNBOOK.md`). A changed frozen file owes a gate-manifest re-anchor, and "a
green suite is not evidence that no re-anchor is owed" (`AGENTS.md`). That re-anchor sits on the board
as a standing Maintainer-only row (`dev/PLANNING.md`), and you have said of it: "If we don't need to
re-anchor now, let's not." A contract-surface change refuses bounded mode, so it runs the full suite,
about ten minutes at the last measurement (`dev/measurement/suite-cost.md`, 2026-08-19). Cairn's own
recent archives already treat that as a reason: `9832c411` closes a finding as `wontfix` because
"pinning edits a frozen test file and costs a full run". The bar is practice that nobody has written
down.

**Cairn's own record is thin evidence of the problem.** The last two archives (`5d00fa96`,
`9832c411`) record `defer x0`. The pull lands on adopters, through the module and the plan template.

**The prior work.** The verification-practice plan (archived `5d00fa96`, closed #25) lowered the cost
of a fix: Boundary B now reaches a trivial change, with its record in the commit body, so a cheap fix
can run the scoped tests and a bounded record instead of the full suite. The maintainer-attention
plan (archived `9832c411`, closed #28) made an archived plan a record, not a to-do list, which fixes
what a `defer` may point at. This proposal asks only whether to fix at all.

## Proposal

### 1. A `defer` names its reason (rule 1)

`doctrine/lifecycle.md` > "Archive precondition" keeps "There is no required order" and gains, after
it:

> **A `defer` says why it could not be fixed now**, with one of three reasons. *It needs a Maintainer
> decision* (say which). *It belongs to work already in motion* (name the open plan or proposal; the
> item is written into that plan's text, which is already a live home, and does not become a new
> issue). *It is over the cost bar* (say what the size or the ceremony is). "Non-blocking", "nit",
> "low priority" and "the reviewer suggested a home" are not reasons: a suggested home is advice, and
> only the Maintainer's quoted words authorize a `defer`. An item that is cheap, needs no decision and
> belongs to no work in motion is an `accept`: fix it before the archive. This orders nothing among
> `accept`, `guard` and `wontfix`. It says that the one disposition that hands the cost to someone else
> must say why. `wontfix` meets the same test from the other side: declining a true defect that is
> under the cost bar needs a reason other than "it is minor".

The last sentence closes the escape the August review warned of. If deferring is made costly and
declining is not, cheap fixes drift to `wontfix`.

* Both block forms (`doctrine/plans.md`, `doctrine/proposals.md`) become
  `* <item> -> defer (<reason>) -> dev/PLANNING.md > <section>   [Maintainer: "<quote>"]`.
* Both plan templates' *Dispositions* section: "Every deferred item is recorded in `dev/PLANNING.md`,
  and requires the Maintainer's authorization quoted verbatim" gains "and names its reason: it needs
  a Maintainer decision, it belongs to work already in motion (name the open plan), or it is over the
  cost bar. 'Non-blocking', 'nit' and a reviewer's suggested home are not reasons."
* The board mirror in `templates/core/dev/PLANNING.md` gains one pointer sentence. It already says it
  is not the source.
* `doctrine/plans.md`, the label: **Today** "`(nit)` — clarity / polish; defer-OK." **Becomes**
  "`(nit)` — clarity / polish. A priority, not a reason to defer: fold it into the plan with the other
  findings, and if you do not, say why."
* `doctrine/plans.md`, the code-review paragraph, after "Sharpening fixes land as follow-up commits
  before the plan archives": "A finding that is cheap to fix is fixed that way, whatever its label. A
  reviewer's suggested home for an item is advice, not the Maintainer's authorization."
* `doctrine/dual-review.md` > "The blocking test" and the finding sentence in
  `templates/core/dev/agent_collaboration.md` ("A finding is **blocking** or **non-blocking**") gain:
  "Non-blocking says only that shipping would not do damage that is hard to undo. It does not make a
  finding deferrable."

### 2. Leave the file better, and the exception it needs (rule 2)

`AGENTS.md` > "Git and commit workflow", after the "Removal counts as a deviation" paragraph:

> **A recorded defect fixed in a file the work already edits is not new scope.** A person who meets an
> easy problem fixes it, and the plan does not need the Maintainer's word for you to do the same. All
> of these must hold:
> * the defect is already on the record before you start (an issue, a review finding, a board row, or
>   an earlier note in the plan);
> * the file is one this change already edits;
> * the fix is **cheap** (below);
> * it comes with its own test, and the plan or the commit body names the fix and the record it closes;
> * it lands in the range the code review reads.
>
> It stays a deviation when the plan's own fence excludes it, when the fix changes what a rule,
> contract or acceptance criterion says, or when any condition above fails. A known cheap defect in a
> file you edited and did not fix needs a reason in the plan, the same three as a `defer`.

**What stays a deviation, in plain terms.** A defect not on the record (Question 2). A file the work
does not edit. A fix over the cost bar, or on a high-risk, contract or frozen surface. Any change to
what a rule says: `941cb34d` added a sentence to three governing files, took your word, and would take
it again. Anything the plan fenced out. Removing accepted scope, unchanged.

The plan templates' deviation sentence ("**Deviating from an accepted plan takes the Maintainer's
word**") gains: "Fixing a recorded cheap defect in a file the plan already edits is not new scope
(`AGENTS.md` > 'Git and commit workflow')." `doctrine/plans.md` > "Accepted scope is a floor" gets the
same pointer.

### 3. What "cheap" means (the default cost bar)

In both `AGENTS.md` files, directly after the exception:

> **What cheap means.** A fix is cheap when it needs no decision (there is one reasonable fix), fits in
> about a chunk's worth of the plan it joins, and sets off nothing beyond the change's own review: no
> high-risk surface this file names, no contract surface, no file whose bytes a gate pins, no step only
> the Maintainer can run (re-recording a gate baseline, a Security Review). This is the line Boundary B
> already draws for bounded mode, so a cheap fix never forces a full-suite run. **Doubt means not
> cheap**: capture it. A project that wants a different bar writes it in its conventions.

Reusing Boundary B's fence means "what is expensive" has one definition. Cairn's own `AGENTS.md`
(not the shipped copy, which must carry no Cairn-only token) adds one paragraph under "Project-specific
conventions": a one-line change under `bootstrap/_scaffold/` is not cheap (a proposal and a Security
Review, and past the allowlist a Maintainer-run AST re-anchor); a changed frozen file is not cheap (a
gate-manifest re-anchor that does not announce itself); a contract-surface change runs the full suite.
Prose no test pins is the cheap case.

### 4. Recast "Capture vs. fix inline" (rule 3)

**Today** (module, both copies):

> A standing rule keeps the channel useful: **capture friction as an issue rather than fixing it
> inline mid-session**, unless the fix is trivial and in-scope for the current work. Inline fixes to
> unrelated friction scatter the work and escape review; an issue preserves the signal for triage on
> its own cadence. The exception is the genuinely one-line, on-path fix.

**Becomes:**

> Friction is **fixed where you meet it** when the fix is cheap, testable and in a file you are
> already working in, and **captured** otherwise. A person who meets an easy problem fixes it; that is
> how code gets better each time someone looks at it.
>
> * **Fix** when the fix is under the project's cost bar (`AGENTS.md`), is in a file the current
>   change already edits, carries its own test, and is named in the plan or the commit and reviewed
>   with the change.
> * **Capture** as an issue when the fix is off your path, needs a decision, is over the cost bar, or
>   needs triage.
>
> The worry behind the old rule, that inline fixes "scatter the work and escape review", is met by the
> test and the review the fix must carry. A fix with neither is the scatter the rule guards against.
> The same test binds the User Agent's debug-from-the-user's-seat mode: a diagnosed fix that meets it
> lands with its test; one that does not is captured (reproduction plus root cause) and routed to the
> owning implementer.

`doctrine/roles.md` > User Agent already says "scope, not size, is the bar" while the module says
"once it exceeds the trivial one-line bar". They disagree today. Its sentence ("a fix past a trivial,
in-scope correction is *captured*") is changed to the same test, so the two say one thing.

### 5. Look before you build (rule 4)

* **Plan template, under *Scope*** (both copies): "**Reuse.** What existing code does this reuse or
  generalize? Where did you search for near-duplicates (the query or path, and what it found)? 'None'
  is an answer only with the search named. If the plan adds no code, write `N/A: no code added`." A
  near-duplicate is code that does a job existing code already does, under another name or with a small
  change. A copy a test pins as identical on purpose, such as Cairn's byte-identical self-hosted
  twins, is not one.
* **Review.** Lens 5 of the review sweep ("Cross-document consistency") already says to scan for "an
  existing tool/path the change should use or update". It gains: "A plan's *Reuse* answer is checked by
  re-running its search, and one of the reviewer's own, first against a case known to be present. A
  diff that adds a near-duplicate of existing code is a finding, with reuse or generalize as its
  satisfier, never a nit." I add no tenth lens: the lenses proposal fixes the roster at nine and pins it.
* **`AGENTS.md`**, both copies, under "Project-specific conventions" (Question 3): "**Search before you
  build; generalize rather than copy.** Before adding a helper, look for one that already does the
  job, and use or extend it. Say where you looked in the plan, or in the commit body if there is no
  plan. If the project keeps a map of its shared code, its conventions name it."
* **No new slot.** The issue offered a slot for the adopter's own map. An unfilled slot is "a review
  finding" in every installed tree (`templates/core/AGENTS.md`, top), so a new slot would hand every
  upgraded adopter a finding. The existing conventions slot is the home.
* **The redundancy gate is not relevant to code, and I say so.** `scripts/quality_gate.py --sub
  redundancy` has two halves. R1 compares prose passages in `doctrine`, `dimensions`, `on-ramp` and
  `docs`. R6 lists top-level definitions that nothing references, which is dead-code detection, not
  near-duplicate detection. Neither finds two functions doing one job, and the script is not shipped to
  adopters. So the reuse check has no tool. **Its trigger is a plan-review pass and a code-review pass,
  each run by a reviewer, and it is described as that.** A check whose only trigger is a human is
  named a human check (`AGENTS.md` > "Verifying claims").

### 6. One new test

`bootstrap/tests/test_stewardship_rules_ship.py`, modelled on
`bootstrap/tests/test_review_and_verification_rules_ship.py`. Obligations matched as alternations over
whitespace-collapsed text, with node IDs named for the obligation. It pins, on every carrier: the
exception and its conditions, the cost-bar sentence with "doubt means not cheap", the three `defer`
reasons, the *Reuse* question, and the module's Fix and Capture criteria (read from a real install of
a profile that selects the module, because the installed copy is what an adopter reads). It pins two
absences: `defer-OK`, and the module's "genuinely one-line" bar.

Proposed paths:
* `bootstrap/tests/test_stewardship_rules_ship.py` — the new test

### What this does not do

No ordering among dispositions. No quota on deferrals. No tool, checker or gate. No change to the
engine, the install list, the lockfile schema or `scaffold.py --manifest`. No change to the release
sweeps, which keep their own Maintainer triage (`docs/release-process.md`). The new text names no
vendor.

## Order of work

**Follow, do not fold.** The review-stance proposal (accepted) and the review-lenses proposal
(awaiting decision) are to be built as one plan, which has not opened
(`dev/proposals/2026-10-18-claude-external-is-a-maintainer-stance.md`,
`dev/proposals/2026-10-18-claude-review-lenses-for-every-install.md`). This proposal's plan opens
**when that plan archives**.

Why not fold: the combined plan will carry about 50 prose files and a Security Review obligation this
change does not need, and my plan is `required(Internal)`. The one real dependency is small. Lens 5's
text moves from the module into the review-loop document in that plan, so my sentence is written at its
final home. Everything else points at `AGENTS.md` text, so splitting it off early would ship a pointer
to words that do not exist yet. Opening after the combined plan also means my pins run against settled
text and my new test joins the re-anchor batch once, not twice.

**Files named by more than one proposal** (same file; I expect different sections, to be confirmed at
plan time by reading the then-current text):

* `AGENTS.md`, `templates/core/AGENTS.md`: their "Review" section; mine, "Git and commit workflow" and
  "Project-specific conventions".
* `doctrine/plans.md`, `doctrine/dual-review.md`, `doctrine/roles.md`, `doctrine/proposals.md`: the
  stance rewrites reviewer-tier text (16, 17, 5 and 3 case-insensitive "external" mentions); the
  lenses proposal retargets one citation in `plans.md` and edits `dual-review.md` > "Adaptation".
* `templates/core/dev/plans/_template.md`, `dev/plans/_template.md`: both name the plan templates; mine
  edits *Scope*, *Dispositions* and the deviation sentence.
* The lens text: `templates/modules/team-gated/dual-review.md` and `dev/modules/dual-review.md`
  today; `templates/core/dev/agent_collaboration.md` and `dev/agent_collaboration.md` > "The review
  sweep" afterwards. My lens-5 sentence and the "non-blocking" sentence go to the final home.

**No overlap I found:** `templates/modules/team-gated/issue-capture.md` and its `dev/modules/` copy,
`doctrine/lifecycle.md` (its one "External" mention is `External-repo paths`, which the stance counts
as noise), `templates/core/dev/PLANNING.md`. `dev/PLANNING.md` is a shared communication file, so its
mirrored section changes only at a serialization point.

**Reaching installed trees** is the three-way merge on `upgrade --stage` then `--apply`
(`bootstrap/UPGRADE.md`). The module reaches only teams that selected it, LHM among them. The
`AGENTS.md` text reaches every install. The plan rehearses the merge on scratch copies of LHM and
modflow_tools and reports conflicts. The upgrades themselves stay yours.

## Rationale

**The outcome is that the cheap path is the good path.** Today, fixing an easy problem costs the agent
a test, a review and a risk of a deviation, and deferring costs one line. Rule 1 puts a reason on the
deferral. Rule 2 and the exception remove the deviation risk from the fix. Rule 3 stops the module
from teaching the opposite. None adds ceremony for a fix that is actually cheap.

**Why reasons and not a quota.** A cap on deferrals becomes the number to hit, and August's review
showed that ordering dispositions steepens the slope toward declining. A stated reason can be read,
and wrong ones can be named: "nit" and "non-blocking" are the two words the issue says read as
permission.

**Why the exception is narrow.** The deviation gate is one of four places approval attaches. I loosen it
for one class (recorded, cheap, in-file, tested, reviewed) and leave every rule change, fence and
expensive surface with you. The cost bar uses Boundary B's fence, so the exception cannot reach a file
that needs a re-anchor or a Security Review.

**Where I am least sure.** (a) "A chunk's worth" is a soft size; a firmer number would be arbitrary.
(b) Whether "recorded first" (Question 2) is too tight: your own words say "when they encounter it",
and a defect met fresh waits for the next touch. (c) The reuse check is only as good as the search
the author names and the reviewer re-runs. It is a human check with a recorded trace, not a gate.

## The rate-limit gate, stated plainly

The gate (`doctrine/rationale.md` > "How the doctrine evolves under evidence"): no doctrine change from
a single incident unless you classify it high-risk, and "high-risk" there means a security surface or
unrecoverable data loss. Neither fits. Otherwise a recurrence or a routine-boundary synthesis is needed.

**What I ran.** `python tools/evolution_infer.py` read four trackers (attestation-replay failures,
the collision log, maintainer-view misses, review-floor deviations) and reported "RATE-LIMIT
SUGGESTIONS: none". That absence proves nothing about this shape: none of the four has a class for
deferral or duplication, so the tool could not have seen it (`AGENTS.md`: confirm the instrument before
trusting an absence).

**What the evidence is.**

| Shape | Instances | Where |
|---|---|---|
| Deferral as the cheapest answer | LHM, 13 items at one archive, 8 easy (issue #30). Earlier: Cairn's own board, 59 deferred items in a 1002-line file and about 16 follow-ups per plan (`dev/proposals/archive/2026-08-04-claude-deferral-discipline.md`) | Two settings, about ten weeks apart, two different surfaces (the board, then roll-up issues) |
| Writing a near-copy | LHM, one session: a mapping specified a third time, and a PATH preamble copied between two callers before extraction | One adopter, one day. I found no Cairn-side instance (a search of commit titles for duplicate and extract wording turned up none I could tie to a missed reuse; that is weak evidence) |
| Your direction | "fix defects, build nothing new" (2026-07-22, `dev/PLANNING.md`); `941cb34d` chose fix over defer; the quote in issue #30 | Three occasions |

**My reading.** The deferral half has an arguable recurrence: the same mechanism returned on a path
the August fix did not cover. The reuse half is one incident. Together the gate is not cleared by
evidence. It can be cleared by your Decision, as the lenses proposal's was ("your Decision is the
authorization"), with the difference that this adds rules rather than moving text. If you proceed, the
Decision should say it proceeds on your direction with the gate not met on evidence, so the audit trail
shows it.

**Counting from here needs no tracker.** Every archive commit body carries a `Dispositions:` line, so
`git log --grep='^Dispositions:'` gives the `defer`, `accept` and `wontfix` counts per archive. The
baseline is the two latest: `accept x5, wontfix x3, defer x0` and `accept x6, wontfix x3, defer x0`.

## Alternatives considered

* **Subtraction only.** Strike `defer-OK`, flip the module default, add nothing. It builds nothing and
  is the smallest change. It loses because it leaves a `defer` with no stated reason, does nothing for
  reuse, and LHM already had a local search-before-building rule that was not enough. It is the
  fallback if you want less: the label change in item 1 and item 4 first, the rest later.
* **A strict order, fix first** (the August draft). Lost then, for the reason in Context.
* **A cap on deferrals per archive.** Lost: the cap becomes the target.
* **A tool: a duplicate-code detector, or a deferral counter.** Lost: your standing direction is no new
  mechanism without a go-ahead, and a detector that misses renamed copies reports success while
  testing nothing.
* **Leave it to adopters' conventions slots.** Lost: the module and the plan template, which ship, push
  the other way, and adopters inherit the push. A pull has to ship where the push does.
* **Do nothing.** It costs what LHM paid: 8 easy fixes sitting in roll-up issues, and a third copy of a
  mapping.

## Documentation / doctrine surface

Routed by `docs/DOCUMENTATION_PLAN.md`: prescription goes to the governing layer, the why to
`doctrine/`.

* **Governing and shipped**: `AGENTS.md` and `templates/core/AGENTS.md` (about 26 lines each; the
  shipped file goes from 419 to about 445); both plan templates; `templates/core/dev/PLANNING.md`;
  `templates/core/dev/agent_collaboration.md` and `dev/agent_collaboration.md`;
  `templates/modules/team-gated/issue-capture.md` and `dev/modules/issue-capture.md`;
  `templates/modules/team-gated/dual-review.md` and `dev/modules/dual-review.md` only if the lens text
  has not moved when the plan opens.
* **Doctrine**: `doctrine/lifecycle.md` (canonical), `doctrine/plans.md`, `doctrine/proposals.md`,
  `doctrine/dual-review.md`, `doctrine/roles.md`. The reasoning is written once, in `lifecycle.md`.
  The others point at it, so the redundancy gate has nothing to flag.
* **Board**: `dev/PLANNING.md` mirrors its archive-preconditions section at a serialization point.
* **Untouched**: every `bootstrap/_scaffold/` file (no AST impact),
  `bootstrap/tests/fixtures/gate_manifest.json`, `bootstrap/tests/fixtures/scaffold_ast_baseline.json`, profiles, `README.md`,
  `docs/`. I searched `docs/` and `README.md` for
  a statement of the capture rule or a deferral default and found none that would go false.
* **Frozen files**: none edited. Prose is not frozen; frozen tests read it. 32 frozen files under
  `bootstrap/tests/` mention `AGENTS.md`, 6 the plan template, 4 `doctrine/lifecycle.md`, 3
  `doctrine/dual-review.md` and 1 the module (counted by file name at `7e11b316`). They must stay green unedited. The new test is
  not frozen, and joins the Maintainer's next re-anchor batch, so it must be final first.
* **`CHANGELOG.md` > Unreleased** gains an entry in the plan's archive commit.

## Evidence / verification plan

**Falsifiers**: a fresh install, with the module selected, whose `dev/modules/issue-capture.md` still
says "genuinely one-line", or whose `AGENTS.md` lacks the exception, the cost bar or the reuse line; a
`defer-OK` anywhere in `doctrine/plans.md`; a block form that shows a `defer` with no reason;
`scaffold.py --manifest` differing before and after.

### Tests required

* **New**: `test_stewardship_rules_ship.py` (item 6), with literal patterns that are not derived from the
  files they check.
* **Mapped, unedited**: the plan maps by search, not by expectation. The frozen readers found above
  include `test_scope_reduction_trap.py`, `test_loop_fidelity_gate.py`, `test_verification_boundaries.py`
  (it forbids Cairn-only tokens in the shipped `AGENTS.md`, so the cost-bar text names no
  `bootstrap/` path), `test_scaffold.py`, `test_documentation_plan_module.py` and
  `test_quickstart_sequence.py`; the unfrozen `test_review_and_verification_rules_ship.py` joins them.
* **Mutations, in a separate copy, each beside an unmutated control.** The set is listed from the tree:
  the deviation list is restated in `AGENTS.md`, `templates/core/AGENTS.md`, `dev/plans/_template.md`,
  `templates/core/dev/plans/_template.md`, `doctrine/plans.md` and `doctrine/dual-review.md` (found by
  searching for "struck chunk" and "Deviating from"). The first four carry the exception and are
  pinned, so it is deleted from each. The last two get a pointer. Also:
  restore `defer-OK`; restore "genuinely one-line" in the shipped and the installed module copy;
  delete the *Reuse* question from each plan template; delete "doubt means not cheap" from each
  `AGENTS.md`; show a `defer` with no reason in each block form. Each must turn a named node red.
* **Boundary B mode**: expected `full`. Many frozen files mention the touched prose, and uncertainty
  resolves to `full`. A `bounded` run needs a reviewed mapping that says why.

### Examples / smoke checks

`python scripts/claim_check.py` and `python scripts/check_cairn.py` over every changed file;
`python scripts/quality_gate.py --sub neutrality --sub redundancy` (expected: the pre-existing
neutrality failure set, 74 at `941cb34d`, none in the changed files);
`python bootstrap/scaffold.py --manifest` diffed before and after; the scratch-copy upgrade rehearsal
on LHM and modflow_tools; and a read of the installed `dev/modules/issue-capture.md` from a fresh
install.

#### Security preflight

N/A: no trust boundary added, moved, or widened, and no high-risk surface touched. One authority
boundary does move: which fixes may land without your word. The exception's conditions, and its
exclusion of every high-risk, contract and frozen surface, are what hold that line. The reviewer
should attack them first.

## Signals the change is wrong

* **Deferrals vanish into `wontfix`.** In the next ten archive bodies, a `wontfix` whose rationale is
  only "minor" or "low value" on a true, cheap defect means the shortcut moved. Put it to you.
* **Plans absorb unrelated fixes.** A code review finds a fix under the exception in a file the range
  did not otherwise edit. One is a finding. Two means "a file you are already in" is read too widely,
  and I would narrow it to the function or section.
* **The bar is argued past.** A fix on a high-risk, contract or frozen surface lands under the
  exception, or a fix under it lands unreviewed or untested. Withdraw the exception.
* **Archives slow down because every nit becomes in-plan work.** The bar is set too low. Count commits
  per plan against the last ten archives and raise the bar.
* **The reuse question goes ritual.** Three plans in a row answer "none" with no search named, or a
  near-copy turns up later in code whose plan said "none". The answer is not a check.

## Scope delta

The baseline is the four rules of issue #30.

**Scope delta**: preserved.

* **Rule 1** (fix cheap findings before archive; a `defer` says why): delivered by item 1 with the
  issue's three reasons, plus the label and "non-blocking" corrections.
* **Rule 2** (leave the file better): delivered as the duty the issue asks for, with the issue's own
  limit to files the work touches. The cost bar, the exclusion of rule changes, and "recorded first"
  are conditions I added; the issue's "easy" and "known" carry them. "Recorded first" is Question 2.
* **Rule 3** (recast capture vs fix): delivered, with "cheap and verifiable" defined by the cost bar.
* **Rule 4** (reuse as a reviewable obligation): the plan question and the code-review finding are
  delivered. The issue's optional core line is Question 3. Declining it is not a reduction: the issue
  called it optional. The issue's optional slot is delivered by mechanism, not by a new slot (item 5),
  and its outcome, that an adopter points at its own map, holds.

Additions beyond the issue, declinable without reduction: the exception's wording, the cost bar's
default, the `wontfix` sentence, the `roles.md` reconciliation, the lens-5 sentence, the new test.

## Assurance path

**Assurance path**: high-assurance. The change edits `doctrine/`, the governing `AGENTS.md` and the
authoring templates, and it moves an approval point. It does not touch the scaffold engine, the install
contract, a trust root, the interpreter binding, the portable-sweep runner, the licence split or the
vendor-neutrality boundary, so `Review` stays `required(Internal)` and no Security Review is owed.
If the Maintainer judges the loosened deviation gate to need one, that is a one-word change to the
header. **Plan review**: `required(Internal)`. The chunk list adds no engine, contract or trust-root
file, so the plan needs no Security Review either.

## Review -- Claude Opus 5.5 (Internal) -- 2026-10-18

**Model**: Claude Opus 5.5, a fresh session with no shared context, of the same agent family as the author; no cross-type distance. An Internal pass, taking the stance the accepted review-stance Decision sets for proposal review: should this exist, and is there a better design.

```
Reviewed commit: f804f3b7a347d148ecac41edee21204f61c2de39
Target: the whole proposal, In brief through Assurance path; every tree figure read at that commit in a detached worktree; LHM read only
Prior findings: none
Assurance path: high-assurance
```

**Tier**: Internal
**Findings**: raised (3 blocking, 7 non-blocking)
**Verdict**: REVISE

### Verdict in brief

**Most of this should go ahead: a deferral that says why, the module's new default, and the reuse question. The exception to the deviation rule needs work before you answer Question 2.** Three things need an answer first:

* **SW1. As written, "cheap" would let an agent defer almost every code fix found at code review, which is LHM's exact case.** After a code review, any change to code or tests makes Cairn require a fresh full test run (`AGENTS.md:253-258`). The proposal says a cheap fix "never forces a full-suite run", and that doubt means not cheap. Read together, an agent can honestly call each of LHM's eight easy fixes "over the cost bar".
* **SW2. The exception can be used to widen a plan.** An agent can write a "defect" into the plan in one commit and fix it in the next, and every condition holds. "Defect" is never defined, so a feature someone wants can be filed as one.
* **SW3. The module and the exception give opposite instructions.** The module will say to fix friction "where you meet it". The exception says a problem met fresh is written down and waits. An adopter's agent that follows the module would be committing a deviation.

There is a better design for the exception: **name these fixes in the plan before work starts, where the plan reviewer sees them** (SW4). Cairn's plans already do this informally under "Found while planning". Note also that the exception is the one part of the proposal that moves an approval point, and no incident shows it is needed. LHM's eight were findings on the plan's own code, and the proposal itself says those need no exception (lines 100-102). The exception rests on your direction alone (SW7).

### Steelman

Cairn's rules make a deferral cost one line, and a fix cost a test, a review and the risk of a deviation, so agents defer. The proposal leaves the deferral vocabulary and its August design alone: no order, no quota, no tool. It prices the one disposition that hands the cost to someone else, by making it name one of three reasons. It closes the obvious escape into `wontfix`. It flips the one shipped text, the issue-capture module, that teaches capture over fixing. It defines "cheap" by ceremony rather than by line count, which is the right axis in a tree where a one-line engine change costs a Security Review. And it adds a reuse question to the plan with a check a reviewer can repeat. It also says honestly that its evidence does not clear the rate-limit gate.

### Foundations

* **Should this exist? Yes, and the exception should exist only in a narrower form.** The deferral pull is real and documented twice. LHM's archive deferred eight easy fixes (issue #30), and in August Cairn's board held 59 deferred items in 1,002 lines (`dev/proposals/archive/2026-08-04-claude-deferral-discipline.md:24-25`). The shipped module still says the exception "is the genuinely one-line, on-path fix" (`templates/modules/team-gated/issue-capture.md:61-62`). Rule 1, the module flip and the label fixes answer LHM's case without touching any approval point. The exception is a separate question: it changes who approves new scope, and no recorded incident turns on it.
* **Is there a better design? For rule 1, the module and the reuse question: no.** I looked for a cheaper carrier than a template question plus a reviewer check, and found none that is not a tool the Maintainer has said no to. **For the exception: yes.** Exercise it at plan time, where a one-round fresh plan review reads it before any code exists, and keep the implementation-time path only as a narrow backstop (SW4). That design closes most of SW2 by construction, gives the "leave it better" duty a trigger, and lets a defect the planner meets fresh be fixed in the same plan. That is closer to "when they encounter it" than Question 2's default.

### Findings

#### SW1 -- BLOCKING: the cost bar prices out the fixes the evidence is about

**Plain:** after code review, Cairn requires a fresh full test run whenever code or tests change. The proposal's "cheap" says a cheap fix never forces a full run. So every fix to code made after code review fails "cheap", and "doubt means not cheap" settles the argument toward deferring.

* The proposal: "This is the line Boundary B already draws for bounded mode, so a cheap fix never forces a full-suite run. **Doubt means not cheap**" (lines 202-204). Item 3's bar also says a cheap fix "sets off nothing beyond the change's own review" (lines 200-201).
* `AGENTS.md:253-258`: "A fresh full run is required when: ... **review sharpening changes implementation, tests, executable templates, or** fixtures — any change to implementation/test/executable-template/fixture bytes invalidates the record". The shipped copy says the same (`templates/core/AGENTS.md:260-265`), and so does LHM's installed `AGENTS.md` (lines 274-277).
* LHM's eight came from a code review that had already approved: "a strict type check, two name refusals, an archive-entry path check, two refuse-before-write reorderings, and missing tests for existing refusals" (issue #30). Each is a code or test change after review. Read as a criterion, the proposal's sentence makes all eight "not cheap", and rule 1 then changes nothing for the case it was written for.
* The equivalence is not exact either. Boundary B's refusal list names contract surfaces and trust-ceremony surfaces (`AGENTS.md:219-224`). "A file whose bytes a gate pins" and "a step only the Maintainer can run" are additions. Boundary B also runs full for a surface with no mapping, or one it cannot bound (`:217-219`), so "never forces" is not true of the fence itself.
* **Usable mid-task?** The named-surface half, yes: an agent can check a path against the high-risk list, the gate manifest's frozen files and the contract list. "About a chunk's worth", no. It grows with the plan's chunk size, it is judged per fix with no total, and a trivial change or a one-commit proposal has no chunk (`doctrine/lifecycle.md:214-219`). That half will be argued, in whichever direction the agent already leans.

**Recommend:**
1. Strike "so a cheap fix never forces a full-suite run". Say instead that the bar counts work that needs a person (a step only the Maintainer can run, a Security Review, a new proposal or decision), not machine time. A re-run that the change's own verification already prescribes is paid once per sharpening batch and is never a reason to defer one finding.
2. Say the surface list "reuses Boundary B's refusal list and adds frozen files and Maintainer-only steps", not "is the line Boundary B draws".
3. Use two bars. For rule 1 (a finding on the plan's own change, which is already in scope), "about a chunk's worth" is fine, and it is the issue's own example. For the exception (scope nobody accepted), use a test an agent can apply without judgment: the fix restores behaviour the file already promises, adds no new file, function, option or public name, and changes nothing beyond the defect's own lines and its test (see SW2).

#### SW2 -- BLOCKING: the exception can be used to widen a plan

**Plain:** an agent that wants to add something the plan left out can first write it down as a "defect" and then fix it under the exception. Nothing in the five conditions tells that apart from a real fix.

* "The defect is already on the record before you start" (line 174) does not say before *what*: the plan, the chunk, or the fix. Question 2 says "before the work began" (line 51), and "a defect met fresh is recorded first and fixed on the next touch" (line 52). A later chunk of the same plan is a next touch.
* **The abuse, step by step.** Plan P edits file F, and an implementing agent wants an option P did not include. Commit 1 appends a plan note: "Defect: F does not handle X." Commit 2 adds X, with a test and a commit body that cites the note. Every condition holds. It was on the record before the fix started, F is a file the change edits, the agent judges it cheap, it has its own test, it is named, and it is in the reviewed range. A review finding works too: a reviewer who writes "while you are in F, also handle X" creates the record that authorizes the widening. `AGENTS.md:157-158` forbids a reviewer from creating authority to *narrow*. The exception lets one create authority to *widen*, and the proposal never says that asymmetry is intended.
* **"Defect" is not defined anywhere in the proposal.** `doctrine/roles.md:62-66` already holds the test that would close this: "a one-line change that re-decides that design is captured, while a larger fix squarely within the bug's own contract may land." Item 4 would overwrite it (SW3).
* **No total.** Each fix is judged alone, so a plan that edits ten files can absorb ten chunk-sized fixes. The proposal's signal (lines 472-474) fires only on a fix in a file the range did not otherwise edit, which the conditions already forbid, so it cannot see this.
* **"A change to what a rule says is still a deviation"** (lines 181-182) gives no test for "rule". In Cairn's prose tree, a reviewer can check it once it is defined. In an adopter's code it means little, and the defect definition has to do the work. As written, the code reviewer has no claim to falsify.

**Recommend:**
1. Anchor the record to a moment git can show: the record predates the commit that moved the plan to `ready-to-implement` (for a change with no plan, its first commit). A record made after that counts as met fresh.
2. Define defect, taking the test from `roles.md`: the file does not do what it, its docstring, its tests or its governing text already say it does. The fix restores that and re-decides nothing. Anything that adds a behaviour or option nothing promised is new scope.
3. Add a total: the fixes made under the exception in one plan together stay within one chunk's worth, and the rest are captured.
4. Give each fix one commit-body line that can be grepped, shaped like `Dispositions:`. For example: `Exception fix: <record> -> <file> -- test <path::node> -- changes no rule text`. The code reviewer can then list every fix, check each record's date and falsify the "no rule text" claim, and the "plans absorb unrelated fixes" signal can be counted.
5. Define "what a rule says": any sentence that tells a reader what to do, or states what a check, contract or acceptance criterion requires.
6. State the asymmetry: a review finding may authorize a fix under the exception, but never a narrowing, and say why.

#### SW3 -- BLOCKING: the module flip and the exception give opposite instructions for a problem met fresh

**Plain:** the new module text tells an agent to fix easy friction where it meets it. The new `AGENTS.md` text says a problem met fresh is written down and fixed later, and that fixing it now is a deviation. The two texts ship together.

* New module text: "Friction is **fixed where you meet it** when the fix is cheap, testable and in a file you are already working in" (lines 224-225). Its Fix bullet (lines 228-230) lists the cost bar, the file, the test, naming and review, but not "already on the record". Its User Agent sentence says "a diagnosed fix that meets it lands with its test" (lines 236-237). A bug the User Agent has just diagnosed is by definition not on the record beforehand.
* The exception (lines 174-175) and Question 2's default (lines 50-52) make that same fix a deviation whenever a plan is open.
* The top 60 lines already show the split without flagging it: "What changes" item 2 says "known" (line 23), and item 3 does not (line 25).
* `roles.md` would be "changed to the same test" (lines 240-242). That replaces "**scope, not size, is the bar**" (`doctrine/roles.md:62`) with a test of size and ceremony, and loses the one existing sentence that answers SW2.
* The module is often used outside any plan: a User Agent session, or a trivial change. There, no accepted plan exists to deviate from, and the proposal does not say which rule governs.

**Recommend:** state the rule once, in `AGENTS.md`, and have the module and `roles.md` point at it instead of restating it. Say which case is which:

* **Inside an open plan**, the exception's conditions govern.
* **Outside a plan**, a fix that meets the defect definition (SW2.2) and the cost bar may land with its test, named in its commit and reviewed, because there is no accepted scope to deviate from.

If the author wants record-first everywhere instead, change the module's headline to "recorded where you meet it, fixed on the next touch". Either way, keep `roles.md`'s "scope, not size" sentence and make it the defect definition rather than overwriting it.

#### SW4 -- non-blocking (recommended): name the fixes in the plan, before work starts

**Plain:** the "leave it better" duty has no one assigned to check it. A line in the plan, which the plan reviewer re-checks, gives it a checker, and catches most misuse before any code is written.

* The duty: "A known cheap defect in a file you edited and did not fix needs a reason in the plan" (lines 182-183). Nothing says who checks it. To do so, a code reviewer would have to search every record for every edited file. `AGENTS.md` > "Verifying claims": "Any document that describes a check says what runs it."
* Cairn already does this informally. `dev/plans/archive/verification-practice.md:120-124` has a "Found while planning" section, and its items are "named here so the plan reviewer can say otherwise". `dev/plans/archive/maintainer-attention.md` has the same heading. `941cb34d` came out of that section.
* Plan cells "revise in place until implementation begins" (`templates/core/dev/plans/_template.md:24`), so naming a fix there costs one line, and the plan review reads it before any code exists.

**Recommend:** add a second line beside *Reuse* under *Scope*: "**Known defects in the files this plan edits.** Where did you search the record (issues, the board, open findings), what did you find, and which cheap ones does this plan fix?" Plan review re-runs the search. Make this the exception's main path, so that a fix named there is reviewed scope. Keep the implementation-time path only for a record that predates `ready-to-implement` and that the search missed. What this gains:

* the duty gets a trigger;
* most fixes are seen before any code exists;
* a defect the planner meets fresh, while reading the files, can be fixed in the same plan. That answers the doubt the proposal names at line 349.

#### SW5 -- non-blocking: "belongs to work already in motion" has no place in the `defer` grammar

* Reason 2 says the item "is written into that plan's text ... and does not become a new issue" (lines 135-137). But a `defer` is "deposited on the roadmap board" (`doctrine/lifecycle.md:592`). Both templates say "Every deferred item is recorded in `dev/PLANNING.md`" (`templates/core/dev/plans/_template.md:234`, `dev/plans/_template.md:244`), and item 1 only appends to that sentence (lines 150-153). The new block form ends `-> dev/PLANNING.md > <section>` (line 149). A `defer` into an open plan fits none of the three.
* Once the receiving plan's chunks start, it changes by appending, not by editing in place (`templates/core/dev/plans/_template.md:35`). The item is also new scope for that plan.

**Recommend:** give the block form a second shape, `-> defer (in motion) -> dev/plans/<slug>.md > <section>`. Change "recorded in `dev/PLANNING.md`" to "recorded in `dev/PLANNING.md` or in the open plan that takes it". Say the item is *appended* to that plan. Say that the Maintainer's quoted authorization also covers the addition to the receiving plan.

#### SW6 -- non-blocking: Cairn already asks why; and the `wontfix` sentence collides with "consequence, not convenience"

* The proposal says "nothing asks *why* it was not fixed" (lines 81-82). `doctrine/lifecycle.md:600-602` says: "There is no required order. What is required is that the record say why the chosen disposition is the right one." That sentence is how August's finding I9 was resolved (`dev/proposals/archive/2026-08-04-claude-deferral-discipline.md:1063-1069`). Item 1 is therefore narrower than presented: it names which reasons count for a `defer`. Saying so is more accurate, and it makes a smaller doctrine change for the gate to weigh.
* The new `wontfix` sentence (lines 142-143) meets `doctrine/lifecycle.md:608-609`: "Consequence, not convenience, decides what may be declined." Under the August rule, low consequence can justify a decline. The new sentence says "it is minor" is not enough for a cheap true defect. Both can hold, but a reader needs to be told how they combine.
* Calibration is available. The two baseline archives carry six `wontfix` items between them (`5d00fa96`, `9832c411`). "CR4, doctrine copies unpinned -> wontfix (doctrine is not shipped)" gives a consequence reason that the new sentence may reject. "CR3 ... -> wontfix (reaches no adopter; pinning edits a frozen test file and costs a full run)" gives a reason the bar accepts, since a frozen file is not cheap.

**Recommend:**
* Reword the Context sentence and item 1's lead to say that the record already gives a why, and that for a `defer` the why must be one of three.
* Add one sentence that combines the two rules: "Consequence decides what may not be declined; cost decides what must be fixed. A true defect under the cost bar is fixed unless fixing it needs a decision."
* Dry-run the new rules on the six baseline `wontfix` items and report how many would change. That calibrates the bar, and it gives the "deferrals vanish into `wontfix`" signal a baseline (already three per archive).

#### SW7 -- non-blocking: the rate-limit section, stated more exactly

The conclusion is honest: the gate is not met on evidence. Five parts of how it is stated should change.

* **The precedent is misdescribed.** "It can be cleared by your Decision, as the lenses proposal's was" (lines 375-376). The lenses proposal argued that the gate did not apply ("No rule changes, only where it ships, so I do not claim the recurrence", `dev/proposals/2026-10-18-claude-review-lenses-for-every-install.md:129-130`). Its Decision (`:661-690`) does not mention the gate. Nothing was cleared by a Decision.
* **The gate's text has no Decision bypass.** Its one bypass is high-risk classification, limited to security and data-loss surfaces, and "Any other 'this feels urgent' framing falls outside the bypass and obeys the recurrence requirement" (`doctrine/rationale.md:407-431`). Proceeding is a waiver the doctrine does not provide for. Question 5 calls it an "override" (line 61), which is right. Line 375 calls it "cleared", which is not. The record the proposal recommends (the Decision says it proceeds on direction, with the gate not met) is the right one, and the wording should match it.
* **A corrected figure is back.** The table cites "about 16 follow-ups per plan" (line 369). August's own review showed that 16 counts candidates, and that the board figure was 4.67 rows per plan. The author accepted that correction (`dev/proposals/archive/2026-08-04-claude-deferral-discipline.md:533-556`, `:1016`).
* **No recurrence window is named.** Cairn's trackers pin 14 days (`dev/measurement/review-floor-deviations.md:19`) and, as a stated departure, 90 days (`dev/measurement/attestation-replay-failures.md:21`). August 4 to October 18 is 75 days. That is a recurrence only under the 90-day choice, and only if the two are the same shape. August's was a board that only grew; October's is cheap fixes filed instead of made.
* **The evidence differs by item.** The exception has no incident behind it: LHM's eight were findings on the plan's own change, which the proposal says "collides with nothing" (lines 100-102). The reuse half is one incident.
* **"Counting from here needs no tracker"** (line 380). The `Dispositions:` grep counts outcomes. The gate counts `Impact = occurred` rows in a tracker (`doctrine/rationale.md:447`), and `tools/evolution_infer.py` reads only trackers. I re-ran it at `f804f3b7`: "RATE-LIMIT SUGGESTIONS: none." So if the answer to Question 5 is "hold", nothing records this first instance where the gate could count a second.

**Recommend:**
* Say "waive", not "clear", and describe the lenses precedent accurately.
* Correct the 16 to 4.67 board rows per plan, and name the window.
* Say per item what the evidence is. Rule 1, the module and the label fixes rest on an arguable recurrence. The exception and the reuse question rest on the Maintainer's direction.
* On "hold", log this incident as a tracker row with a stated class and window.

#### SW8 -- non-blocking: sequencing facts and the shared-file list

* **A stale status.** Line 295 calls the review-lenses proposal "awaiting decision". It was accepted at `fbf664f0`, an ancestor of `f804f3b7`. Its Status reads `accepted`, and its Decision's Q5 sets up the one combined plan (`dev/proposals/2026-10-18-claude-review-lenses-for-every-install.md:679-684`).
* **`doctrine/lifecycle.md` belongs in the shared list.** The proposal puts it under "No overlap I found" (lines 321-323). The stance proposal lists it among its doctrine files (`dev/proposals/2026-10-18-claude-external-is-a-maintainer-stance.md:366`), and has its plan read every hit of `external` and `independen` there (`:407-409`). `lifecycle.md` carries tier and independence text at `:73`, `:282` and `:307-310`. These are different sections from "Archive precondition" (`:532` onward), so a textual collision is unlikely, but the file is shared.
* **"Prose-only" is not accurate.** Question 4 (lines 58-59) and line 300 describe this as a prose-only change. It adds a test (lines 274-283) and expects a full Boundary B run (lines 449-450). The case for following still holds, since this change does not need the combined plan's Internal Security Review. The reason should just be stated accurately.
* **A forecast, not a measurement.** The combined plan adds tests that become frozen at the next re-anchor. `test_review_stance_in_shipped_files.py` reads both `AGENTS.md` copies, both templates and the `dual-review` module (stance proposal `:1088`, first described at `:422-424`), and `test_review_sweep_ships.py` reads the installed review-loop document (lenses proposal `:133`). This plan adds text to those same files. Adding text usually leaves short-phrase pins green, but "Frozen files: none edited" (lines 419-422) is a claim about tests that do not exist yet.

**Recommend:** fix the status. Move `lifecycle.md` into the shared list. Drop "prose-only". Have the plan re-measure the frozen set against the then-current gate manifest before its first chunk. **"Follow, do not fold" is right.** Lens 5's final home is the one real dependency, and waiting for the archive is the only point at which that text is settled.

#### SW9 -- non-blocking: two citations

* Line 113 cites the suite-cost file under `dev/measurement/`. That file is gitignored (`.gitignore:18`), so it exists only on this machine. On a clean checkout of `f804f3b7`, `scripts/claim_check.py` hard-flags it ("cited path does not resolve"). It passes in the shared tree only because the local copy exists. The figure itself matches the local file (about 9½ to 11½ minutes, measured 2026-08-19). **Recommend:** declare it on an `Untracked paths:` line (`doctrine/lifecycle.md:189` names that form), or cite a tracked source.
* Lines 443-444 say the set of files that restate the deviation rule was "found by searching for 'struck chunk' and 'Deviating from'". At `f804f3b7` that search returns five files. `doctrine/plans.md` is not among them, because "struck" and "chunk" fall on separate lines (`:487-488`). The six-file set is right; the stated search is not. **Recommend:** name a search that finds all six, so the plan's mutation set is listed from the tree as `AGENTS.md` asks.

#### SW10 -- non-blocking: the top 60 lines

They mostly stand alone and read plainly. Five changes would let you decide from them alone:

* Question 2 asks whether a fix may skip your word, but not who checks the conditions instead. The answer is the code reviewer, after the code exists (or, under SW4, the plan reviewer, before it). That is the fact you need to answer the question.
* Neither the brief nor Question 2 says that the exception is the one part no incident shows is needed (SW7).
* Question 3 says "One line" in its title and "four lines" in its default (lines 53-55).
* Question 1 uses "contract surface" and "a file a gate pins by hash". In plain terms: nothing that would need a re-anchor, a Security Review, a new proposal, or your decision.
* "The rate-limit gate" (line 35) is not explained in the brief. Add "(the rule that one incident does not change doctrine)".

### Checked and confirmed

Read at `f804f3b7` unless noted.

* **The module.** The quote matches `templates/modules/team-gated/issue-capture.md:57-62` and `:66`, and the `dev/modules/` copy is byte-identical (an empty `diff`).
* **The doctrine quotes:**
  * `doctrine/plans.md:744` (`defer-OK`), `:915` (the sharpening sentence) and `:1011` (the block form);
  * `doctrine/proposals.md:380` (the block form);
  * `doctrine/dual-review.md:151` (the blocking test);
  * `doctrine/lifecycle.md:600-602` (no required order);
  * `doctrine/roles.md:60-62` (the User Agent sentence);
  * `AGENTS.md:148-150` (the deviation list).
* **The commits.**
  * `5d00fa96` and `9832c411` carry the two `Dispositions:` lines as quoted, and `9832c411` the "pinning edits a frozen test file and costs a full run" rationale.
  * `941cb34d` added one sentence to `AGENTS.md`, `templates/core/AGENTS.md` and `doctrine/plans.md` on the Maintainer's quoted word, and records neutrality at 74.
* **The board quotes.** "fix defects, build nothing new" is at `dev/PLANNING.md:51`, and "If we don't need to re-anchor now, let's not." at `:163`.
* **The shipped `AGENTS.md`** is 419 lines, and its unfilled-slot rule is at `templates/core/AGENTS.md:10-19`.
* **Lens 5.** Its text is at `templates/modules/team-gated/dual-review.md:58-60` and `dev/modules/dual-review.md:57-59`.
* **The redundancy gate.** R1 scans only `doctrine`, `dimensions`, `on-ramp` and `docs` (`scripts/quality_gate.py:498`), and R6 finds unreferenced definitions.
* **Cairn-only tokens.** `bootstrap/tests/test_verification_boundaries.py:79-89` forbids `bootstrap/tests`, `scripts/quality_gate.py`, `Python 3.13` and `Cairn's ordinary pair` in the shipped `AGENTS.md`.
* **The "external" counts.** Case-insensitive counts in `doctrine/plans.md`, `dual-review.md`, `roles.md` and `proposals.md` are 16, 17, 5 and 3.
* **The frozen-file counts.** 32, 6, 4, 3 and 1, reproduced from `bootstrap/tests/fixtures/gate_manifest.json` > `frozen_files`. No frozen file, and no test, script or tool, contains any phrase this proposal removes or rewrites: `defer-OK`, `genuinely one-line`, `Capture vs`, `scope, not size`, `There is no required order`, `Every deferred item is recorded`, `trivial one-line bar`. Control: the same search finds `accepted scope is a floor` pinned in the gate manifest.
* **The August figures.** 59 items in 1,002 lines (`dev/proposals/archive/2026-08-04-claude-deferral-discipline.md:24-25`); finding I9 is at `:711`.

### Answers to the proposal's five questions

1. **What counts as cheap.** Agree on counting ceremony, not lines, and on "doubt means not cheap" for the named surfaces. Two changes first (SW1). Drop the full-run sentence. Use two bars: "about a chunk's worth" for the plan's own findings, and the fix-shaped test for the exception.
2. **May a qualifying fix skip your word.** Yes, but only in the narrowed form:
   * the record is dated before `ready-to-implement`;
   * a defect means restoring behaviour the file already promised;
   * there is a total per plan;
   * each fix carries one line that can be grepped;
   * preferably, the fix is named in the plan before work starts (SW2, SW4).

   Under the exception, the code reviewer checks each fix, not you. No incident shows this part is needed; your direction is its basis.
3. **The reuse line in both `AGENTS.md` files.** Yes. It is the only carrier for work with no plan, and it adds no slot. Fix the "one line" against "four lines" wording.
4. **Order.** Follow, do not fold. Agree. Fix the stale status and add `doctrine/lifecycle.md` to the shared list (SW8).
5. **The rate-limit gate.** Agree with proceeding on your direction, with the Decision saying the gate is waived, not met. I would have the Decision name the exception separately, since it rests on direction alone. On "hold", log this incident in a tracker so that a second one can count (SW7).

### Coverage

* **Covered** -- claims: every quote, line number, count and commit the proposal cites about Cairn's tree, read at `f804f3b7`, plus `claim_check` on a clean checkout (SW9). Production path: none run; no install path changes. Cross-document consistency: SW3, SW5, SW6, SW8, against `AGENTS.md`, `lifecycle.md`, `roles.md`, the plan templates and both accepted proposals. Drift: the rate-limit evidence (SW7). Lifecycle placement: the deviation gate (SW2, SW4) and the order of work (SW8). Test-plan completeness: the mutation-set search (SW9).
* **Not covered / low confidence** -- below.

### What I did not cover

* **LHM's archive.** I could not find the archive with 13 deferrals in the local LHM clone (latest commit `d3b5bd0f`, 2026-10-18). No commit or file carries the reviewer's roll-up wording. The 13/5/8 sort, and my reading that the eight were code-review findings on the plan's own code, rest on the issue's text.
* **The combined plan.** The plan file `review-stance-and-lenses` under `dev/plans/` is uncommitted and still being written. I judged sequencing against the two accepted proposals behind it and did not read the draft. SW8's frozen-file point is a forecast.
* **Runs I did not make.** No suite run, no scratch install and no upgrade rehearsal on LHM or modflow_tools. Those belong to the implementation, and the new test does not exist yet.
* **Wording I did not draft or test.** I did not draft replacement text for every carrier, and did not run the neutrality gate on any proposed wording.
* **The redundancy gate.** I did not check how R1 would score the new `lifecycle.md` text against the doctrine copies that point at it.

## Response -- Claude (author) -- 2026-10-18

Answers the Internal review at `fcba1494` (REVISE, ten findings, SW1 to SW3 blocking). The review's
central recommendation is a better design for the exception, and I take it: **fixes for known cheap
defects are named in the plan before work starts**, where the plan reviewer sees them (SW4). That is now
the main path. It shrinks the exception to a narrow backstop. All ten findings are accepted, SW2 in
modified form. Revision 1 below is the complete current contract.

**What became of the exception.**

* **At planning: no exception is needed.** The plan searches the record for known defects in the files it
  will edit and names the cheap ones in its *Scope*. Plan review reads that before any code exists. A fix
  named there is part of the approved plan, so it is not a deviation.
* **During the work: a narrow backstop.** An agent may fix a defect the search missed if it breaks
  something already promised (a record dated, or a promise in the tree, before the plan was ready), the
  file is one the work edits, the fix is cheap and tested, one greppable commit line names it, and all
  such fixes in a plan stay within about a chunk's worth. This is the Maintainer's "when they encounter
  it", kept inside a mechanical test.
* **A defect first recorded after that point** goes to the Maintainer in one line, as a deviation
  request. Question 2 lets the Maintainer widen or narrow this.
* **With no accepted proposal or plan** (a trivial change, a User Agent session) there is no accepted
  scope to deviate from, so a cheap defect fix lands with its test and the same commit line.
* **Gone:** the free-standing exception, "recorded first, fixed on the next touch", and the
  record-before-you-start condition that a note written mid-work could satisfy.

**Why Status goes to `awaiting-decision`.** Every element is the reviewer's recommendation or is
narrower than the contract that was reviewed. One thing the review did not read is the trigger wording,
"a record or a promise already in the tree". It is stricter than the reviewed "already on the record",
because a plan note written after the cut-off no longer counts, and it is put to the Maintainer as
Question 2 with the reviewer's records-only form named as an alternative. No surface is added: no engine,
contract or trust-root file.

| Finding | Disposition | Reason, and where it lands |
|---|---|---|
| **SW1** cost bar prices out LHM's case (blocking) | accept, all three parts | "Cheap" counts steps that need a person, not machine time; a full re-run is machine time. The sentence "a cheap fix never forces a full-suite run" is struck. The surface list now says it reuses Boundary B's refusal list and adds frozen files and Maintainer-only steps. Two bars: a size bar for findings on the plan's own change, a mechanical defect test for fixes outside accepted scope. Rev. 1 §3 |
| **SW2** the exception can widen a plan (blocking) | accept 2 to 6; modify 1 | Defect defined from `doctrine/roles.md`; a total per plan; a `Defect fix:` commit line; "what a rule says" defined; the asymmetry stated and justified. On 1, the anchor is "a record dated, or a promise already in the tree, before the plan became ready to implement". The reviewer's form is records only. Mine adds the promise because a defect found mid-work that breaks a docstring, test or rule in the tree is still a defect, and a note written afterwards is not a promise. Rev. 1 §2 |
| **SW3** module and exception contradict (blocking) | accept | The rule is stated once, in `AGENTS.md`. The module and `doctrine/roles.md` point at it. Three cases are named: planning, implementing under an accepted proposal or plan, and no proposal or plan. `roles.md` keeps "scope, not size, is the bar" and only its opening clause changes. Rev. 1 §2, §4 |
| **SW4** name the fixes in the plan | accept; adopted as the main path | A *Known defects in the files this plan edits* line beside *Reuse*. The duty gets a trigger and a checker. Rev. 1 §2 |
| **SW5** "work in motion" has no `defer` shape | accept | A second block shape, `defer (in motion) -> dev/plans/<slug>.md > <section>`; "recorded in `dev/PLANNING.md` or in the open plan that takes it"; the item is appended; the Maintainer's quoted words cover the addition. Rev. 1 §1 |
| **SW6** Cairn already asks why; `wontfix` collides with "consequence" | accept, all three | Wording corrected: the record already gives a why and the rule names which whys count for a `defer`. The two rules combine in one sentence. **Dry run on the six baseline `wontfix` items: no outcome changes** (detail in Evidence). Rev. 1 §1 |
| **SW7** the rate-limit section | accept, all five parts | "Waived", not "cleared". The lenses precedent is described as it was. Figure corrected to 4.67 board rows per plan, and the window named. Evidence stated per item. On "hold", a tracker row is the first action. Rev. 1, *The rate-limit gate* |
| **SW8** sequencing facts | accept | Status fixed. `doctrine/lifecycle.md` joins the shared list. "Prose-only" dropped. The frozen set is re-measured before the first chunk. Re-checked against the combined plan at `8cc124b5`. Rev. 1, *Order of work* |
| **SW9** two citations | accept both | `suite-cost.md` is declared on a one-line `Untracked path:` marker (the block form is flagged stale whenever a local copy exists), and it was tested on a clean detached checkout, with the opening version as the control. A stated search now finds all six files that restate the deviation rule (tested, with a control). Rev. 1, *Evidence* |
| **SW10** the top 60 lines | accept all five | Question 2 says who checks; the brief says the exception has no incident behind it; "one line" and "four lines" reconciled; Question 1 in plain terms; the gate explained in the brief |

## Revision 1 -- Claude (author) -- 2026-10-18 -- the complete current contract

Supersedes the opening *Proposal*, *Order of work*, *Rationale*, *The rate-limit gate*, *Alternatives*,
*Documentation / doctrine surface*, *Evidence*, *Signals*, *Scope delta* and *Assurance path* in full.
*Context* stands as opened, with the corrections listed under it below. **Declarations.**
**Review**: required(Internal), done at `fcba1494`. **Plan review**: required(Internal).
**Assurance path**: high-assurance. **Boundary B**: expected `full`.

### In brief

Cairn's rules make **putting a problem off** the cheapest thing an agent can do with it. ("Deferring"
means parking an item in a later issue or on the board instead of fixing it now.) At one archive in your
LHM project, 13 review findings were deferred; sorted afterwards, 5 truly had to wait and 8 were easy
fixes filed because filing was easier. The same session was about to write a surface-to-groundwater
mapping for the third time. Your direction, from issue #30:

> "A human would fix a problem that is easy when they encounter it--thereby adding value whenever they look at code"

**What changes**

1. **A deferral says why:** it needs your decision, it belongs to work already under way, or it is over
   the cost bar. "Non-blocking" and "nit" stop counting as reasons.
2. **Easy defects get fixed, mostly at planning.** The plan searches for known defects in the files it
   will edit and names the cheap ones. The plan reviewer sees them before any code exists, so they need
   no special permission. During the work, an agent may fix a defect that breaks something the file
   already promises, with a test and one commit line, up to about a chunk's worth per plan. Anything
   else that turns up goes to you in one line.
3. **The issue-capture module** stops teaching "capture, don't fix". It points at that rule.
4. **Before building,** the plan says what existing code it reuses and where the author looked for
   near-copies. A new near-copy is a real review finding, not a nit.

**Two things keep "easy" honest.** "Cheap" counts steps that need a person (your re-anchor, a Security
Review, a new proposal, a decision), not machine time: a ten-minute test re-run does not make a fix
expensive, which is what the first draft got wrong. And a "defect" means the file does not do what it
already says. Adding behaviour nobody promised is new scope, and changing what a rule says still takes
your word, so a fix like `941cb34d` still comes to you.

**What I cannot show.** The rate-limit gate (the rule that one incident does not change doctrine) is not
met on evidence. The rule on fixing defects has **no incident behind it, only your direction**. The
deferral half rests on an arguable recurrence, and the reuse half on one session. Question 5 asks you to
waive the gate and says so on the record.

It builds on the verification-practice work (#25) and the maintainer-attention work (#28), both closed,
and re-proposes neither. It adds no tool.

### Questions for the Maintainer

Each has my default. An unanswered question takes it.

1. **What counts as cheap?** *Default:* a fix is cheap when it needs **no step that takes a person**:
   nothing that would need your re-anchor, a Security Review, a new proposal or a decision. A test
   re-run is machine time and does not count. For size, a finding on the plan's own change should fit in
   about a chunk's worth of the plan (a chunk is one row of its sequence), or one commit where there is no
   plan. If it is unclear whether such a step is needed, it is not cheap. Adopters may set their own bar.
   The alternative, a line count, cannot see ceremony.
2. **May an agent fix a defect during the work without asking you?** This loosens one of the four
   things your approval attaches to. The code reviewer checks each fix afterwards, from one commit
   line per fix; the plan reviewer checks the named ones beforehand. *Default:* yes, narrowly. The
   defect must break something already promised, with the promise (or a record) dated before the plan was
   ready; the file is one the plan edits; the fix is cheap and tested; and all such fixes in a plan stay
   within about a chunk's worth. A defect first recorded later comes to you in one line. *Alternatives:*
   (a) narrower: records only, with no "promise in the tree" route; (b) narrower: planning only, no
   mid-work route; (c) wider: also a defect with no promise to cite, under the same cap and commit line,
   which restores the issue's full reach.
3. **Add a four-line reuse rule to both `AGENTS.md` files?** Trivial changes and plan-less proposals
   never meet a plan template, so the rule is the only carrier for them. *Default:* yes, in "Project-specific
   conventions".
4. **Order.** *Default:* this proposal's plan **follows** the combined review-stance and review-lenses
   plan and opens when it archives. It does not fold in. Folding would put a change that needs no Security
   Review under that plan's Security Review obligation and add about 15 files to a plan of 49.
5. **The rate-limit gate.** The gate has no "Decision clears it" route. *Default:* proceed, and let the
   Decision say that the gate is **waived**, not met, and that the rule on fixing defects (item 2 above)
   rests on your direction alone. Say "hold" and this waits for a second recurrence; the first action
   then is a tracker row so a second can be counted.

### Corrections to the opening *Context*

* **"Nothing asks *why* it was not fixed" was too strong.** `doctrine/lifecycle.md` already says "the
  record say why the chosen disposition is the right one". What is missing is which whys count for a
  `defer`.
* **Cairn's own rules would have priced out LHM's eight fixes.** They were code and test changes after a
  code review, and a change to either after review requires a fresh full run (`AGENTS.md`, Boundary C).
  The first draft's bar treated that run as a cost. It is machine time.
* **The August board figure is 4.67 net rows per plan** (28 rows over six plans, from 95 candidates),
  not 16. The author accepted that correction in August (`dev/proposals/archive/2026-08-04-claude-deferral-discipline.md`, finding I4).
* **The cost-bar paragraph named the re-anchors correctly but counted the full run.** Corrected in §3.
* **`dev/measurement/suite-cost.md` is gitignored** (`.gitignore`), a regenerated output, not a tracked
  record. The figure (about ten minutes) is a local snapshot and is no longer used as a cost.

### Proposal

#### 1. A `defer` names its reason (rule 1)

`doctrine/lifecycle.md` > "Archive precondition" keeps "There is no required order" and gains, after it:

> **A `defer` says why it could not be fixed now.** The record already says why for every disposition.
> For a `defer` the why must be one of three. *It needs a Maintainer decision* (say which). *It belongs
> to work already in motion* (name the open plan or proposal; the item is appended to that plan's text,
> which is already a live home, and does not become a new issue; the Maintainer's quoted authorization
> covers the addition). *It is over the cost bar* (say which person-step it needs, or how large it is).
> "Non-blocking", "nit", "low priority" and "the reviewer suggested a home" are not reasons: a suggested
> home is advice, and only the Maintainer's quoted words authorize a `defer`. An item that is cheap,
> needs no decision and belongs to no work in motion is an `accept`: fix it before the archive. This
> orders nothing among `accept`, `guard` and `wontfix`. **Consequence decides what may not be declined;
> cost decides what must be fixed. A true defect under the cost bar is fixed unless fixing it needs a
> decision.**

The `defer` bullet there changes from "deposited on the roadmap board" to "deposited on the roadmap
board, or appended to the open plan that takes it". That makes the grammar match the live-home list.

* **Block forms** (`doctrine/plans.md`, `doctrine/proposals.md`) gain a second shape and a reason:
  `* <item> -> defer (<reason>) -> dev/PLANNING.md > <section>   [Maintainer: "<quote>"]` and
  `* <item> -> defer (in motion) -> dev/plans/<slug>.md > <section>   [Maintainer: "<quote>"]`.
* **Both plan templates' *Dispositions*:** "Every deferred item is recorded in `dev/PLANNING.md`, and
  requires the Maintainer's authorization quoted verbatim" becomes "...is recorded in `dev/PLANNING.md`,
  or in the open plan that takes it, requires the Maintainer's authorization quoted verbatim, and names
  its reason: it needs a Maintainer decision, it belongs to work already in motion (name the plan), or it
  is over the cost bar. 'Non-blocking', 'nit' and a reviewer's suggested home are not reasons."
* **The board mirror** in `templates/core/dev/PLANNING.md` gains one pointer sentence. It already says it
  is not the source.
* **`doctrine/plans.md`, the label.** **Today** "`(nit)` — clarity / polish; defer-OK." **Becomes**
  "`(nit)` — clarity / polish. A priority, not a reason to defer: fold it into the plan with the other
  findings, and if you do not, say why."
* **`doctrine/plans.md`, the code-review paragraph,** after "Sharpening fixes land as follow-up commits
  before the plan archives": "A finding that is cheap to fix is fixed that way, whatever its label. A
  reviewer's suggested home for an item is advice, not the Maintainer's authorization."
* **"Non-blocking."** `doctrine/dual-review.md` > "The blocking test" and the finding sentence in
  `templates/core/dev/agent_collaboration.md` ("A finding is **blocking** or **non-blocking**") gain:
  "Non-blocking says only that shipping would not do damage that is hard to undo. It does not make a
  finding deferrable."

#### 2. Fix the easy problem you meet (rule 2)

Only rule 2 collides with `AGENTS.md`. A finding on the plan's own change is fixed today by a sharpening
commit ("Sharpening fixes land as follow-up commits before the plan archives", `doctrine/plans.md`), so
rule 1 needs no exception. A defect nobody put in the plan is new scope, which the deviation gate
reserves to the Maintainer. The design is in three places, by where the agent is.

**`AGENTS.md` > "Git and commit workflow"**, as a new bullet beside "Scribing a Decision". The rule is
stated here once. The module and `doctrine/roles.md` point at it.

> * **Fixing an easy problem you meet.** A person who meets an easy problem fixes it. The rules here
>   make that the normal answer and ask only that the fix be small, tested, named and reviewed.
>   * **A defect** is something that does not do what the file, its docstring, its tests or its
>     governing text already say it does. The fix restores that and re-decides nothing: it adds no new
>     file, function, option or public name, and changes nothing beyond the defect's own lines and its
>     test. Behaviour nothing promised is new scope. A note in a plan or a review comment does not make
>     something a defect.
>   * **While planning,** search the record (issues, the board, open findings) for known defects in the
>     files the plan will edit, and name the cheap ones you will fix, with the search you ran, in the
>     plan's *Scope*. Plan review re-runs the search before any code exists. A fix named there is part
>     of the approved plan, not a deviation.
>   * **While implementing under an accepted proposal or plan,** you may fix a defect the search missed
>     if it was on the record, or the promise it breaks was in the tree, before the plan became ready to
>     implement (for a change with no plan, before its first commit); the file is one the change already
>     edits; the fix is cheap and has its own test; and the commit body carries one line,
>     `Defect fix: <record or promise> -> <file> -- test <path::node> -- changes no rule text`. Together
>     such fixes stay within about a chunk's worth of the plan; capture the rest. A defect first
>     recorded after that point goes to the Maintainer in one line, as a deviation request. A plan's own
>     fence still wins.
>   * **With no accepted proposal or plan** (a trivial change, a User Agent session) there is no
>     accepted scope to deviate from. A cheap defect fix lands with its test and the same commit line,
>     and is reviewed.
>   * **What a rule says** (any sentence that tells a reader what to do, or states what a check,
>     contract or acceptance criterion requires) is never changed by a defect fix. That takes the
>     Maintainer's word.
>   * A known cheap defect in a file you edited and did not fix needs a reason in the plan: the three
>     a `defer` gives (the plan template's *Dispositions*).

* **Plan templates, under *Scope*,** beside *Reuse* (§5): "**Known defects in the files this plan
  edits.** Where did you search the record (issues, the board, open findings), what did you find, and
  which cheap ones does this plan fix? 'None' is an answer only with the search named. A fix named here
  is part of the plan, and plan review re-runs the search." The plan cells revise in place until
  implementation begins, so naming a fix costs one line.
* **The deviation sentences.** The six places that restate the deviation rule (found by the search in
  *Evidence*) gain a pointer: "A defect fix made under 'Fixing an easy problem you meet' is not new
  scope." `AGENTS.md` and `templates/core/AGENTS.md` carry it in the deviation bullet, the two plan
  templates beside "Deviating from an accepted plan takes the Maintainer's word", and `doctrine/plans.md`
  and `doctrine/dual-review.md` where they restate the list.
* **Who checks what.** The plan reviewer checks the named fixes and re-runs the search. The code
  reviewer lists every fix with `git log --grep='^Defect fix:'`, checks that each record or promise
  predates the cut-off, that the fix restores exactly that and nothing more, that the file was already
  in the range, that the total stays inside one chunk, and that the "changes no rule text" claim holds.
  A fix that fails is a finding.
* **The asymmetry is intended.** A review may add a named fix to a plan, at plan review, before the cut-off.
  A review may never narrow accepted scope (`AGENTS.md`, "Removal counts as a deviation"). A narrowing
  is invisible: the wider version is never built, so nothing can show it wrong. A defect fix is a
  small, tested, named commit that the next reviewer sees and can revert, and the total caps it. A
  code-review comment written after the cut-off cannot authorize a fix, because that is the route the
  review showed could widen a plan.

**What is left of the opening exception, in one place.** At planning: nothing, because the fix is part
of the reviewed plan. During the work: the narrow backstop above, with a dated cut-off, a mechanical
defect test, a total and a greppable line. For a defect first recorded mid-work with no promise to cite:
a one-line request to you, which is the existing deviation path. With no proposal or plan: the same
defect and cost tests, with no approval step because there is nothing to deviate from.

#### 3. What "cheap" means

In both `AGENTS.md` files, directly after the bullet above:

> **What cheap means.** Cheap counts steps that need a person, not machine time. A fix is not cheap if
> it touches a high-risk surface this file names, a contract surface, or a file whose bytes a gate pins,
> or needs a step only the Maintainer can run, a Security Review, a new proposal or a decision. If it is
> unclear whether it does, it is not cheap. A test re-run that the change's own verification already
> prescribes is machine time: it is paid once for a batch of fixes and is never a reason to defer one.
> For size, a finding on the plan's own change should fit in about a chunk's worth of the plan (one
> commit with its test, where there is no plan). A project that wants another bar writes it in its
> conventions.

The surface list reuses Boundary B's refusal list (contract surfaces and trust-ceremony surfaces) and
adds two things Boundary B does not name: a file a gate pins by hash, and a step only the Maintainer can
run. It is not "the line Boundary B draws". There are two bars on purpose. A finding on the plan's own
change is already in scope, so size alone limits it. A fix outside accepted scope meets the defect test
in §2, which an agent can apply without judging how big it feels.

Cairn's own `AGENTS.md` (not the shipped copy, which must carry no Cairn-only token) adds one paragraph
under "Project-specific conventions": a one-line change under `bootstrap/_scaffold/` is not cheap (it
opens a proposal and a Security Review by "High-risk surfaces", and past the allowlist a Maintainer-run
AST re-anchor); a changed frozen file is not cheap (a gate-manifest re-anchor that does not announce
itself); the full suite, about ten minutes, is machine time and does not count; prose no test pins is the
cheap case.

#### 4. Recast "Capture vs. fix inline" (rule 3)

**Today** (module, both copies):

> A standing rule keeps the channel useful: **capture friction as an issue rather than fixing it
> inline mid-session**, unless the fix is trivial and in-scope for the current work. Inline fixes to
> unrelated friction scatter the work and escape review; an issue preserves the signal for triage on
> its own cadence. The exception is the genuinely one-line, on-path fix.

**Becomes:**

> Friction is **fixed where you meet it** when the rule in `AGENTS.md` ("Fixing an easy problem you
> meet") allows it, and **captured** as an issue when the fix is off your path, needs a decision, is over
> the cost bar, needs triage, or is a problem that rule sends to the Maintainer. A person who meets an
> easy problem fixes it. The worry behind the old rule, that inline fixes "scatter the work and escape
> review", is met by the test and the review the fix must carry, not by forbidding it. The same rule
> binds the User Agent's debug-from-the-user's-seat mode: a diagnosed fix that meets it lands with its
> test; one that does not is captured (reproduction plus root cause) and routed to the owning
> implementer.

The module keeps no copy of the conditions, so it cannot drift from `AGENTS.md`.

`doctrine/roles.md` > User Agent keeps its sentence "**scope, not size, is the bar**: diagnosing a bug
from the user's seat is not authorization to re-decide the owning surface's design". That sentence is
where the defect test comes from. Only its opening clause changes: "a fix past a trivial, in-scope
correction is *captured*" becomes "a fix that is not a defect fix under `AGENTS.md`, or is not cheap, is
*captured*".

#### 5. Look before you build (rule 4)

Unchanged from the opening, except as noted.

* **Plan template, under *Scope*** (both copies): "**Reuse.** What existing code does this reuse or
  generalize? Where did you search for near-duplicates (the query or path, and what it found)? 'None'
  is an answer only with the search named. If the plan adds no code, write `N/A: no code added`." A
  near-duplicate is code that does a job existing code already does, under another name or with a small
  change. A copy a test pins as identical on purpose, such as Cairn's byte-identical self-hosted twins,
  is not one.
* **Review.** Lens 5 of the review sweep ("Cross-document consistency") already says to scan for "an
  existing tool/path the change should use or update". It gains: "A plan's *Reuse* answer is checked by
  re-running its search, and one of the reviewer's own, first against a case known to be present. A diff
  that adds a near-duplicate of existing code is a finding, with reuse or generalize as its satisfier,
  never a nit." There is no tenth lens: the roster stays at nine. The sentence is written at the
  lenses' final home, the review sweep in `templates/core/dev/agent_collaboration.md` and
  `dev/agent_collaboration.md`.
* **`AGENTS.md`,** both copies, under "Project-specific conventions" (Question 3): "**Search before you
  build; generalize rather than copy.** Before adding a helper, look for one that already does the
  job, and use or extend it. Say where you looked in the plan, or in the commit body if there is no
  plan. If the project keeps a map of its shared code, its conventions name it."
* **No new slot:** an unfilled slot is "a review finding" in every installed tree
  (`templates/core/AGENTS.md`, top), so a new slot would hand every upgraded adopter a finding. The
  existing conventions slot is the home.
* **The redundancy gate is not relevant to code.** `scripts/quality_gate.py --sub redundancy` has two
  halves. R1 compares prose passages in `doctrine`, `dimensions`, `on-ramp` and `docs`. R6 lists top-level
  definitions that nothing references, which is dead-code detection. Neither finds two functions doing
  one job, and the script is not shipped to adopters. The reuse check has no tool. **Its trigger is a
  plan-review pass and a code-review pass, each run by a reviewer, and it is described as that.**

#### 6. One new test

`bootstrap/tests/test_stewardship_rules_ship.py`, modelled on
`bootstrap/tests/test_review_and_verification_rules_ship.py`. Obligations are alternations matched over
whitespace-collapsed text, with node IDs named for the obligation. It pins, on every carrier: the defect
definition and the three cases, the `Defect fix:` line shape, "what a rule says", the cost-bar sentence
with its person-step wording, the *Known defects* and *Reuse* lines, the three `defer` reasons and both
block shapes, and the module's pointer to `AGENTS.md` (read from a real install of a profile that
selects the module, since the installed copy is what an adopter reads). It pins three absences: `defer-OK`,
the module's "genuinely one-line" bar, and any claim that a cheap fix "never forces" a full-suite run.

Proposed paths:
* `bootstrap/tests/test_stewardship_rules_ship.py` — the new test

#### What this does not do

No ordering among dispositions. No quota on deferrals. No tool, checker or gate. No change to the engine,
the install list, the lockfile schema or `scaffold.py --manifest`. No change to the release sweeps, which
keep their own Maintainer triage (`docs/release-process.md`). The new text names no vendor.

### Order of work

**Follow, do not fold.** The review-stance proposal was accepted at `58f30d6c`. The review-lenses
proposal was accepted at `fbf664f0` (the opening text called it "awaiting decision"). The combined plan
for both, `dev/plans/review-stance-and-lenses.md`, is committed (`8cc124b5`) and in plan review, and its
two source proposals are archived. This proposal's plan opens **when that plan archives**. The combined
plan's own text puts this work after plans C and D, after itself, and after `model-mapping-install-path`
and `board-as-basis`. I accept that order and re-read every file at edit time.

Why not fold: the combined plan carries 49 prose files and an `Internal + Internal Security Review`
obligation. This change needs only `required(Internal)`, since it touches no engine, contract or
trust-root file. It is a prose change plus one new test. That test joins the standing re-anchor row; if
you run the re-anchor before this plan's code review is done, it owes a second one, which the plan says up
front. That is small next to carrying a Security Review it does not need. The one real dependency is small: lens 5's text moves
into the review sweep in the combined plan, so my sentence is written at its final home. The combined
plan owes three anchors for that, kept as a criterion in its first chunk: the heading "The review
sweep", lens 5 findable by its label "Cross-document consistency", and a roster of exactly nine.

**Files shared with other work,** re-checked against the combined plan's own table at `8cc124b5`:

* `AGENTS.md`, `templates/core/AGENTS.md`: the combined plan edits "Review"; this plan edits "Git and
  commit workflow" and "Project-specific conventions". Different sections.
* `templates/core/dev/agent_collaboration.md`, `dev/agent_collaboration.md`: lens 5 and the finding
  sentence, at the sweep's final home.
* `doctrine/plans.md`, `doctrine/dual-review.md`, `doctrine/roles.md`, `doctrine/proposals.md`, and
  **`doctrine/lifecycle.md`**: the combined plan's chunk for doctrine reads every hit of `external` and
  `independen` in `lifecycle.md` and changes it only if a search says so. This plan edits "Archive
  precondition" there, a different section. The file is shared.
* Both plan templates: the combined plan edits the review skeletons; plan D adds a block after the
  security preflight; `board-as-basis` edits the line beside the header; this plan edits *Scope*,
  *Dispositions* and the deviation sentence.
* The `dual-review` module pair: the combined plan moves the lens text out of it first.
* **No overlap found:** `templates/modules/team-gated/issue-capture.md` and its `dev/modules/` copy,
  `templates/core/dev/PLANNING.md`. The combined plan names neither. `dev/PLANNING.md` is a shared
  communication file, so its mirrored section changes only at a serialization point.

**Frozen tests are a forecast, not a measurement.** The combined plan adds
`test_review_stance_in_shipped_files.py` (it reads both `AGENTS.md` copies, the templates and the module)
and `test_review_sweep_ships.py`; plan D adds a test that reads the template cells. This plan adds text to
the same files. Adding text usually leaves short-phrase pins green, but "no frozen file is edited" cannot
be claimed for tests that do not exist yet. The plan's first chunk re-measures against the
then-current gate manifest which tests pin a cell it edits, and runs them unedited.

**Reaching installed trees** is the three-way merge on `upgrade --stage` then `--apply`
(`bootstrap/UPGRADE.md`). The module reaches only teams that selected it, LHM among them. The `AGENTS.md`
text reaches every install. The plan rehearses the merge on scratch copies of LHM and modflow_tools and
reports conflicts; the real upgrades stay the Maintainer's.

### Rationale

**The outcome is that the cheap path is the good path.** Today, fixing an easy problem costs the agent a
test, a review and the risk of a deviation, and deferring costs one line. Rule 1 puts a reason on the
deferral. Naming fixes in the plan removes the deviation risk where it can be removed most cheaply, at
planning, with a reviewer reading the list. The module stops teaching the opposite. None of it adds
ceremony for a fix that is actually cheap.

**Why plan-time naming is the main path.** It gives the "leave it better" duty a trigger and a checker
(the plan reviewer), it catches misuse before any code exists, and a defect the planner meets while
reading the files can be fixed in the same plan. It follows what Cairn's plans already do informally
under "Found while planning".

**Why the backstop is mechanical.** The opening exception could be used to widen a plan: write a "defect"
into the plan, then fix it. A defect now means the file does not do what it already promises, and a
note or a comment is not a promise. The fix adds no name and touches only the defect's lines and its
test. A total caps it, and a commit line makes each fix countable.

**Why reasons and not a quota.** A cap on deferrals becomes the number to hit, and August's review
showed that ordering dispositions steepens the slope toward declining. A stated reason can be read,
and wrong ones can be named: "nit" and "non-blocking" are the two words the issue says read as
permission.

**Where I am least sure.** (a) "A chunk's worth" is a soft size; a firmer number would be arbitrary.
(b) The "promise in the tree" route is my addition to the reviewer's records-only form. I think the
mechanical test closes the widening it was meant to close, but it is the part to attack (Question 2,
alternative (a)). (c) The reuse check is only as good as the search the author names and the reviewer
re-runs. It is a human check with a recorded trace, not a gate.

### The rate-limit gate, stated plainly

The gate (`doctrine/rationale.md` > "How the doctrine evolves under evidence"): no doctrine change from a
single incident unless the Maintainer classifies it high-risk, which there means a security surface or
unrecoverable data loss. Neither fits. "Any other 'this feels urgent' framing falls outside the bypass
and obeys the recurrence requirement." **The gate has no route by which a Decision clears it.** Proceeding
is a **waiver** the doctrine does not provide for. I recommend it anyway, recorded as what it is.

**What I ran.** `python tools/evolution_infer.py` read four trackers and reported "RATE-LIMIT
SUGGESTIONS: none". None of the four has a class for deferral or duplication, so the tool could not have
seen this shape. That absence proves nothing.

**What the evidence is, per part.**

| Part | Evidence | Reading |
|---|---|---|
| Rule 1, the module flip, the label and "non-blocking" corrections | Deferral as the cheapest answer, twice: Cairn's board (59 deferred items in a 1,002-line file; **4.67 net rows per plan** from the six-plan census of 95 candidates) on 4 August, then LHM's 13 items (8 easy) on 18 October. 75 days apart. | An **arguable** recurrence. It counts under the 90-day window `dev/measurement/attestation-replay-failures.md` uses (a stated departure) and not under the 14-day window of `dev/measurement/review-floor-deviations.md`. And the shapes differ: August's was a board that only grew; October's was cheap fixes filed instead of made. Both are one mechanism, deferral costing one line. |
| The rule on fixing defects (item 2 in the brief) | **No incident.** LHM's eight were findings on the plan's own code, which rule 1 handles and which needed no exception. Your direction: "fix defects, build nothing new" (2026-07-22, `dev/PLANNING.md`), `941cb34d`, and the quote in issue #30. | Rests on **your direction alone**. |
| The reuse question | LHM, one session: a mapping specified a third time, and a PATH preamble copied between two callers before extraction. I found no Cairn-side instance (a search of commit titles found none I could tie to a missed reuse; weak evidence). | **One incident**, plus your direction. |

**The lenses precedent, as it was.** The lenses proposal did not clear the gate by a Decision. It argued
the gate did not apply: "No rule changes, only where it ships, so I do not claim the recurrence". Its
Decision does not mention the gate. This proposal adds rules, so that route is not open to it.

**What I recommend and what the record should say.** Proceed on your direction, with the Decision saying
the gate is **waived**, not met, and naming the rule on fixing defects separately as resting on direction
alone.

**Counting from here.** The `Dispositions:` lines in archive commit bodies count outcomes
(`git log --grep='^Dispositions:'`). The gate counts `Impact = occurred` rows in a tracker, and
`tools/evolution_infer.py` reads only trackers. So the grep is a measurement, not a count the gate can
use. **On "hold" the first action is a tracker row** for this incident, with its class stated and a 90-day
window, so a second can be counted.

### Alternatives considered

* **A free-standing exception (the opening design).** Lost to the review: it could be used to widen a plan,
  and no one was assigned to check the duty.
* **Plan-time naming only, no backstop.** Smaller (Question 2, alternative (b)). It loses on a defect that
  was on the record and that the search missed: the agent then has only a deviation request or a capture,
  which is the cheap-to-defer shape again. Kept as an alternative.
* **A records-only backstop** (the reviewer's form; Question 2, alternative (a)). Narrower than mine, with no
  "promise in the tree" route. Kept as an alternative.
* **Subtraction only.** Strike `defer-OK`, flip the module default, add nothing. It leaves a `defer` with
  no stated reason, does nothing for reuse, and LHM already had a local search-before-building rule that
  was not enough. It is the fallback if you want less: the label change in §1 and §4 first, the rest later.
* **A strict order, fix first** (the August draft). Lost then, for the reason in *Context*.
* **A cap on deferrals per archive.** Lost: the cap becomes the target.
* **A tool: a duplicate-code detector, or a deferral counter.** Lost: your standing direction is no new
  mechanism without a go-ahead, and a detector that misses renamed copies reports success while testing
  nothing.
* **Leave it to adopters' conventions slots.** Lost: the module and the plan template, which ship, push
  the other way, and adopters inherit the push.
* **Do nothing.** It costs what LHM paid: 8 easy fixes sitting in roll-up issues, and a third copy of a
  mapping.

### Documentation / doctrine surface

Routed by `docs/DOCUMENTATION_PLAN.md`: prescription goes to the governing layer, the why to `doctrine/`.

* **Governing and shipped:** `AGENTS.md` and `templates/core/AGENTS.md` (about 44 lines each: the
  bullet, the cost bar and the reuse rule; the shipped file goes from 419 to about 463); both plan
  templates; `templates/core/dev/PLANNING.md`; `templates/core/dev/agent_collaboration.md` and
  `dev/agent_collaboration.md`; `templates/modules/team-gated/issue-capture.md` and
  `dev/modules/issue-capture.md`. The `dual-review` module pair only if the lens text has not moved when
  the plan opens.
* **Doctrine:** `doctrine/lifecycle.md` (canonical), `doctrine/plans.md`, `doctrine/proposals.md`,
  `doctrine/dual-review.md`, `doctrine/roles.md`. The reasoning is written once, in `lifecycle.md`; the
  others point at it.
* **Board:** `dev/PLANNING.md` mirrors its archive-preconditions section at a serialization point.
* **Untouched:** every `bootstrap/_scaffold/` file (no AST impact),
  `bootstrap/tests/fixtures/gate_manifest.json`, `bootstrap/tests/fixtures/scaffold_ast_baseline.json`,
  profiles, `README.md`, `docs/`. I searched `docs/` and `README.md` for a statement of the capture rule
  or a deferral default and found none that would go false.
* **Frozen files:** no frozen file's own bytes are edited, because prose is not frozen; frozen tests
  read it. At `7e11b316`, 32 frozen files under `bootstrap/tests/` mention `AGENTS.md`, 6 the plan
  template, 4 `doctrine/lifecycle.md`, 3 `doctrine/dual-review.md` and 1 the module (counted by file
  name; the review reproduced these counts). No frozen file, test, script or tool contains any phrase
  this proposal removes or rewrites (the review's search). The plan re-measures against the gate manifest
  of the day (*Order of work*). The new test is not frozen and joins the next re-anchor batch, so it must
  be final first.
* **`CHANGELOG.md` > Unreleased** gains an entry in the plan's archive commit.

Untracked path: `dev/measurement/suite-cost.md` -- a regenerated measurement output, gitignored (`.gitignore`), so a clean checkout does not carry it. It is cited only for the "about ten minutes" snapshot, here and in the opening *Context*.

### Evidence / verification plan

**Falsifiers:** a fresh install, with the module selected, whose `dev/modules/issue-capture.md` still
says "genuinely one-line" or restates the conditions instead of pointing at `AGENTS.md`; an `AGENTS.md`
that lacks the defect definition, the `Defect fix:` line, the person-step cost bar or the reuse rule; a
`defer-OK` anywhere in `doctrine/plans.md`; a block form that shows a `defer` with no reason; a claim that
a cheap fix "never forces" a full run; `scaffold.py --manifest` differing before and after.

#### Tests required

* **New:** `test_stewardship_rules_ship.py` (§6), with literal patterns that are not derived from the files
  they check.
* **Mapped, unedited:** the plan maps by search. The frozen readers found include
  `test_scope_reduction_trap.py`, `test_loop_fidelity_gate.py`, `test_verification_boundaries.py` (it
  forbids Cairn-only tokens in the shipped `AGENTS.md`, so the cost-bar text names no `bootstrap/` path),
  `test_scaffold.py`, `test_documentation_plan_module.py` and `test_quickstart_sequence.py`; the unfrozen
  `test_review_and_verification_rules_ship.py` and the combined plan's two new tests join them.
* **Mutations, in a separate copy, each beside an unmutated control.** The set is listed from the tree,
  by a search that finds all six files that restate the deviation rule. The search runs over tracked
  `.md` files outside archives, reflections, reviews and live proposals and plans (the two plan templates
  are included), after stripping `* _` backticks and `>` and collapsing whitespace, case-insensitive,
  for `struck chunk`, `deviating from an accepted plan`, `deviation gate` or `deviated from approved
  scope`. Run at `89f82f3f` it returns exactly: `AGENTS.md`, `templates/core/AGENTS.md`,
  `dev/plans/_template.md`, `templates/core/dev/plans/_template.md`, `doctrine/plans.md` and
  `doctrine/dual-review.md`. Control: it matches the `doctrine/plans.md` phrase "struck chunk", which a
  line-by-line search misses because the words fall on separate lines. The pointer sentence is deleted
  from each of the six. Also: delete the "Fixing an easy problem you meet" bullet from each `AGENTS.md`;
  restore `defer-OK`; restore "genuinely one-line" in the shipped and the installed module copy; delete
  *Reuse* and *Known defects* from each plan template; insert "never forces a full-suite run" in each
  `AGENTS.md`; remove the `in motion` block shape and the reason from each block form. Each must turn a
  named node red.
* **Dry run of the new rules on the six baseline `wontfix` items** (`5d00fa96` and `9832c411`), read from
  the archived plans. **No outcome changes.** (1) PR4's optional install assertion: an optional addition,
  not a defect; stays. (2) CR4, doctrine copies unpinned: the reviewer called it "a follow-up, not a
  defect", and doctrine reaches no adopter; stays, and is the one borderline case, since an `accept` was
  "equally valid". (3) `#12` by tooling: declined in the accepted proposal; stays. (4) CR3, five surviving
  mutants: "pinning edits a frozen test file and so costs a fresh full run". The frozen-file half is a
  person-step (a re-anchor) and keeps the reason; the full-run half is machine time and would be dropped
  from the wording. (5) PR10's `docs/tool-usage.md` sentence: not a defect, since the page stays true;
  stays. (6) the footer "fence" wording note: "not a finding"; stays. So the `wontfix` baseline is three
  per archive (six in two), and the new rule changes none of them.
* **Boundary B mode:** expected `full`. Many frozen files mention the touched prose, and uncertainty
  resolves to `full`. A `bounded` run needs a reviewed mapping that says why.

#### Examples / smoke checks

`python scripts/claim_check.py` and `python scripts/check_cairn.py` over every changed file, and
`claim_check` on a clean checkout (the `Untracked path:` marker above was tested that way, with the opening version of this file as the control: it hard-flags the citation on a clean checkout);
`python scripts/quality_gate.py --sub neutrality --sub redundancy` (expected: the pre-existing neutrality
failure set, 74 at `941cb34d`, none in the changed files; the plan also checks how R1 scores the new
`lifecycle.md` text against the doctrine files that point at it); `python bootstrap/scaffold.py --manifest`
diffed before and after; the scratch-copy upgrade rehearsal on LHM and modflow_tools; and a read of the
installed `dev/modules/issue-capture.md` from a fresh install.

##### Security preflight

N/A: no trust boundary added, moved, or widened, and no high-risk surface touched. One authority boundary
does move: which fixes may land without your word. The defect test, the cut-off, the total, the commit line
and the exclusion of every high-risk, contract and frozen surface are what hold that line. The reviewer
should attack them first.

### Signals the change is wrong

* **Deferrals vanish into `wontfix`.** In the next ten archive bodies, a `wontfix` whose rationale is
  only "minor" or "low value" on a true, cheap defect means the shortcut moved. Baseline: three per
  archive. Put it to the Maintainer.
* **Plans absorb unrelated fixes.** `git log --grep='^Defect fix:'` lists fixes in a plan whose total
  passes one chunk, or whose file the range did not otherwise edit, or whose "promise" the code reviewer
  cannot find in the tree. One is a finding. Two means the defect test is read too widely; narrow it to
  Question 2's alternative (a).
* **The named list becomes a feature list.** A plan's *Known defects* line names something that adds
  behaviour. The plan reviewer should catch it. If a code reviewer finds one, tighten the plan-time test
  to the defect definition.
* **The bar is argued past.** A fix on a high-risk, contract or frozen surface lands as a defect fix, or one
  lands unreviewed or untested. Withdraw the backstop.
* **Archives slow down because every nit becomes in-plan work.** The bar is set too low. Count commits per
  plan against the last ten archives and raise it.
* **The reuse question goes ritual.** Three plans in a row answer "none" with no search named, or a
  near-copy turns up later in code whose plan said "none". The answer is not a check.

### Scope delta

The baseline is the four rules of issue #30.

**Scope delta**: preserved.

* **Rule 1** (fix cheap findings before archive; a `defer` says why): delivered by §1 with the issue's three
  reasons, plus the label and "non-blocking" corrections.
* **Rule 2** (leave the file better): delivered as the duty the issue asks for. At planning the agent
  searches and names the cheap fixes; during the work the backstop covers a defect that breaks a promise
  or a pre-existing record; both carry a test and a record in the plan or commit. The issue's own limit to
  files the work touches is kept. **One residual, named so it cannot be a quiet loss:** a defect first
  recorded after the plan became ready, with no promise to cite, is a one-line request to the Maintainer
  instead of a free fix. The outcome (the defect fixed, tested and recorded) is still delivered once
  allowed, and I do not concede it as a loss. If you read it as one, Question 2 is where to say so:
  alternative (c) restores the issue's full reach, and (a) and (b) go the other way.
* **Rule 3** (recast capture vs fix): delivered, by pointing at the one rule rather than restating it.
* **Rule 4** (reuse as a reviewable obligation): the plan question and the code-review finding are
  delivered. The issue's optional core line is Question 3; declining it is not a reduction, since the issue
  called it optional. The optional slot is delivered by mechanism (the existing conventions slot) and its
  outcome, that an adopter points at its own map, holds.

Additions beyond the issue, declinable without reduction: the `wontfix` sentence, the second `defer` shape,
the `roles.md` reconciliation, the lens-5 sentence, the `Defect fix:` line and the total, the new test.

### Assurance path

**Assurance path**: high-assurance. The change edits `doctrine/`, the governing `AGENTS.md` and the
authoring templates, and it moves an approval point. It does not touch the scaffold engine, the install
contract, a trust root, the interpreter binding, the portable-sweep runner, the licence split or the
vendor-neutrality boundary, so `Review` stays `required(Internal)` and no Security Review is owed. If the
Maintainer judges the loosened deviation gate to need one, that is a one-word change to the header.
**Plan review**: `required(Internal)`. The chunk list adds no engine, contract or trust-root file, so the
plan needs no Security Review either.

### Withdrawn / superseded commitments

* **The free-standing exception** ("a recorded defect fixed in a file the work already edits is not new
  scope"): superseded by plan-time naming, a narrow backstop and a no-plan case (§2). The review showed it
  could widen a plan and that no one checked its duty.
* **"The defect is already on the record before you start"** (any record, any time): superseded by a record
  dated, or a promise in the tree, before the plan became ready to implement.
* **"A defect met fresh is recorded first and fixed on the next touch":** withdrawn. A later chunk of the
  same plan counted as a next touch. Superseded by the one-line request to the Maintainer, with
  alternatives (a), (b) and (c) in Question 2.
* **"A cheap fix never forces a full-suite run," and "this is the line Boundary B already draws":**
  withdrawn. A full re-run is machine time and is not counted; the list now reuses Boundary B's refusal
  list and adds two things.
* **"Doubt means not cheap," as a general rule:** narrowed to doubt about whether a person-step is needed.
* **The module's restated conditions** (the Fix and Capture bullets): superseded by a pointer to `AGENTS.md`.
* **The `roles.md` rewrite to "the same test":** withdrawn. Its "scope, not size" sentence stays; only its
  opening clause changes.
* **"Nothing asks *why* it was not fixed":** corrected to "the record asks why; the rule names which whys
  count for a `defer`".
* **"A `defer` is recorded in `dev/PLANNING.md`" as the only shape:** a second shape, `in motion`, is added.
* **"It can be cleared by your Decision, as the lenses proposal's was":** withdrawn. The word is "waived",
  and the lenses proposal did not clear the gate by a Decision.
* **"About 16 follow-ups per plan":** corrected to 4.67 net board rows per plan.
* **"Counting from here needs no tracker":** withdrawn. The grep counts outcomes; on "hold" a tracker row
  is the first action.
* **"The lenses proposal is awaiting decision":** corrected; it was accepted at `fbf664f0`.
* **"Prose-only":** dropped. It is a prose change plus one new test.
* **"Frozen files: none edited" as a firm claim:** made a forecast, re-measured before the first chunk.
* **"The set was found by searching 'struck chunk' and 'Deviating from'":** replaced by a search that finds
  all six files, tested with a control.
* **Question 3's title "One line":** now "a four-line reuse rule".
* **The opening Questions 1 to 5 as worded:** superseded by Revision 1's five.

## Decision -- Anthony Kendall (Maintainer) -- 2026-10-18

**ACCEPTED, with the Maintainer's changes.** The Maintainer's authorization,
quoted **verbatim and visually isolated**:

> "Accept, with my changes: promise-only defect fixes with no date cut-off; the per-plan total becomes a warning sign; no mandatory Known-defects cell; one small ship test. Answers to Q1–Q5 as recommended. The rate-limit gate is waived, not met."

*Scribe's note, separate from the quoted words.* The Maintainer was answering
a recommendation given in chat on 2026-10-18 (an External-stance read of
Revision 1). Read against it, the changes are binding on the plan:

* **Revision 1 binds, except where these changes narrow it.**
  * **Promise-only defect fixes, no date cut-off.** A defect fix during the
    work restores a promise already in the file the change edits (what the
    file, its docstring, its tests or its governing text already say). The
    "on the record" route and the "before the plan became ready to implement"
    cut-off in §2 are struck. A note, an issue or a review comment never
    makes something a defect. The rest of §2's defect definition stands: the
    fix adds no new file, function, option or public name, and changes no
    rule text.
  * **The per-plan total becomes a warning sign.** "Together such fixes stay
    within about a chunk's worth" leaves the rule and joins *Signals the
    change is wrong*.
  * **No mandatory Known-defects cell.** The *Known defects in the files this
    plan edits* line under *Scope* is not added to the plan templates. A plan
    may still name defect fixes in its *Scope*, as it can today. The *Reuse*
    line stays.
  * **One small ship test.** §6's test pins only the few load-bearing
    sentences: the three `defer` reasons, the defect-fix sentence and its cost
    bar, the module's pointer to `AGENTS.md`, and the absence of `defer-OK`.
    The six-file mutation program in *Evidence* is struck.
  * The `AGENTS.md` text shrinks with these cuts, from about 44 lines per copy
    to roughly a dozen. The commit-body line for a defect fix stays, as one
    line naming the promise, the file and the test.
* **Answers to Q1–Q5 "as recommended"** are the chat recommendation's:
  * **Q1, cheap:** the default. Cheap counts steps that need a person, not
    machine time.
  * **Q2, fixing without asking:** yes, by the promise-only route above.
  * **Q3, the reuse rule in both `AGENTS.md` files:** yes, as one sentence.
  * **Q4, order:** follow the combined review-stance and review-lenses plan,
    and do not fold into it.
  * **Q5, the rate-limit gate:** waived, not met. In particular, the rule on
    fixing defects rests on the Maintainer's direction alone.
* **No second review round.** The changes narrow the reviewed contract.

Scribed by Claude (claude-opus-5-5) on the Maintainer's explicit instruction.
Nothing else lands in this commit.
