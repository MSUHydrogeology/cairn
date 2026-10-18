# Fix easy problems where you find them, and look before you build

**Author**: Claude (Strategy)
**Status**: awaiting-review
**Review**: required(Internal)
**Plan review**: required(Internal)
**Opened**: 2026-10-18

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
