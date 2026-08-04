# The Dual-Review model

Cairn's most distinctive practice is its review model. A change
does not ship because its author is confident; it ships because it
has been **reviewed across structural independence** and the
reasoning held up. The model has two tiers, and which tier a
change needs scales with the team (`dimensions/`) and the change's
risk.

## Two tiers, two purposes

* **Internal review** — *helps a change land.* A second reading
  from a constructive stance: catch problems, sharpen the
  argument, surface what the author missed. The Internal reviewer
  wants the change to succeed and is improving it toward that.
* **External review** — *makes a change prove it should land.* An
  adversarial-but-friendly reading: the change must justify
  itself. The External reviewer's job is to make confidence prove
  itself — to look for the reason this should *not* ship, and to
  report honestly when there is none.

The two are not redundant. Internal review improves a change;
External review tests whether it should exist. A change can be
well-improved and still wrong.

## Structural independence

A review is worth only as much as the reviewer's independence from
the author's blind spots. Cairn does not rely on a reviewer
*trying* to be independent; it arranges **structural**
independence — the reviewer's reasoning genuinely does not share
the author's:

* **A different agent type.** A different model architecture has
  different failure modes; it does not silently inherit the
  author's. This is the strongest readily-available independence,
  and it is the External-review floor.
* **A fresh session.** The same agent type, but with no shared
  context — the mental model is rebuilt from the artifacts, not
  carried over. This is the Internal-review floor.
* **A human.** The Maintainer or another contributor.
* **Domain rotation.** On a large team of domain-specialized
  agents, the reviewer is an agent from a *different* domain —
  independence by rotation rather than by model type.

The floors: **Internal review** accepts same-agent-fresh-session;
**External review** requires a different agent type or a human.
Code review — the implementation-side pass — has its own floor:
**not the implementing agent**.

### Worked example — the floor pays its way

The different-agent-type floor is not a formality; in the reference
deployment it repeatedly caught what the same-vendor pass missed,
*including the blind spots the same-vendor reviewer shared with the
author*. A few representative findings across one development window
(all on Claude-authored work, caught by a cross-type External read):

* A **preset-name path traversal** in a security-hardening proposal; a
  **null-default interior hole** and a **partial-dict regression** in an
  override-validation change — both critical, both surfaced by the
  cross-type reviewers, and the partial-dict one was a blind spot the
  same-vendor pass *shared with the author*.
* At the implementation stage: a **diverged generated copy preserved as
  the active read-path**, and **state written before its `.gitignore`
  seed** — two supply-chain edge bugs the author's green test suite
  passed straight over.
* The single largest catch: a core integrity anchor whose facts **were
  never extracted in production** — dormant in every real build despite a
  fully green unit suite, because no unit test exercised the real call
  chain.

The cumulative signal is the point: across a run of consecutive
cross-type reviews, **each caught at least one real integrity-surface
bug**, spanning the proposal, plan, *and* code-review stages — a rate a
same-vendor reviewer (sharing the author's architecture, and often the
author's blind spot) does not match. The recurring lesson is also
portable: **green unit tests do not clear the floor** — exercise the
integration path (the real call chain, real config), not just the unit
contracts the author already trusted.

## Asynchronous and commit-mediated

A review is not a live conversation. It is a **section appended to
the artifact** — the proposal, or the plan — and committed. This
is deliberate:

* The review joins the durable, append-only record
  (`lifecycle.md`): a later reader sees the critique, not only the
  outcome.
* It removes the synchronizing cost — author and reviewer need not
  be present at once, which matters across agent handoffs and time.
* It keeps the decision surface in the artifact. A review that
  happened in conversation and was never written down did not
  happen.

## Decision-support Round-2 review

Once an author has Responded and produced a revised proposal,
the proposal is substantively ready for the Maintainer's
Decision. But a *second* reviewer may read the revised
proposal and surface findings — not findings the first
reviewer missed, but findings the revision itself
introduced or that a different reviewer's blind-spot
profile exposes. The lifecycle as drawn (review → response
→ revision, repeating) does not name this case, and two
failure modes follow if it is unnamed:

* **The second reviewer's findings get treated as
  Round-1 findings** and trigger another revision cycle.
  Author writes another Response, possibly revises again,
  cycle restarts. With each round the proposal diverges
  further from any one reviewer's read; the cycle no
  longer closes.
* **The second reviewer's findings get dropped.** The
  author refuses to re-open the cycle; the critique lives
  unanswered in a Review section; the Decision is taken
  in tension with a critique the lifecycle did not
  metabolize.

The pattern Cairn names is a **Decision-support Round-2
review** — a Review section appended *after* the author's
Response and Revised proposal. It has three structural
properties that distinguish it from a Round-1 review:

1. **The proposal's status stays `revised`.** The Round-2
   Review does not move status back to `reviewed`. The
   author has already completed their part of the cycle.
2. **Append-only against the proposal, not the cycle.**
   The author does not write a Response section to a
   Round-2 review; the cycle has already closed on the
   author's side.
3. **Feeds the Decision, not another revision.** The
   Maintainer's Decision, when written, addresses both
   Round-1 and Round-2 findings in one place.

The load-bearing word is *Decision-support*. A Round-1
reviewer's job is to test the idea so the author can
revise it. A second-reviewer-after-Response is doing
something different: providing independent perspective to
the Maintainer, who is the only actor with authority to
weigh competing reviews and Decide. Naming the role makes
the structural difference visible; without the name the
second reviewer is mis-modeled as another Round-1
reviewer and the lifecycle breaks.

**The pattern is bounded.** It is *not* "the lifecycle
allows unlimited review rounds":

* It does not permit the author to skip Responding to a
  Round-1 review by re-labeling it Round-2. Round-1
  reviews remain author-Response-bound until the
  proposal reaches status `revised`.
* It does not permit a Decision-support reviewer to demand
  another revision. If a Round-2 reviewer believes the
  revision is fundamentally wrong, the proper response is
  to recommend the Maintainer reject or supersede, not to
  require another revision.
* It does not permit unbounded Round-2 reviews after a
  Round-2 review. The Maintainer's Decision closes the
  Decision-support phase; further critique becomes a new
  proposal that amends or supersedes.

The pattern extends the existing two-tier review framework
(Internal / External, with Code review on the
implementation side) by adding one more shape — not by
adding a new tier. Internal-, External-, Code-, and
domain-rotation-review floors all still apply when a
Round-2 reviewer fills the role.

## Code review — the implementation side

Proposal review tests the *idea*; code review tests the
*implementation*. The plan-archive precondition (`lifecycle.md`)
makes code review mandatory before a plan archives — the bright
line that stops a fast implementation from closing its own loop.
Code review's floor is stricter than Internal review's: **not the
implementing agent**, because freshly written code is hard to spot
mistakes in for someone carrying the same reasoning patterns.

The *entry*-side counterpart is the **plan-review precondition**
(`lifecycle.md`): a review-required plan does not start implementation
until its plan-review section lands. The `Plan review: required(<tier>)`
line names the tier, and that tier is chosen on the same
structural-independence axis as any other review here — an Internal-floor
read for an ordinary plan, a different-agent-type External round for a
high-risk or contract-touching one.

## Review expectations — the clean-pass trap

A review that finds zero issues — or only minor style nits — on a
*complex* change should be treated with skepticism, not relief. The
clean pass is a known failure mode: a reviewer who reads to *confirm*
the change works will find that it does. The discipline is to read as
if a hidden bug exists and probe for it.

The standing form of that discipline is the **review sweep** — a fixed
roster of lenses every reviewer works through and **reports coverage
on**. It exists because the most common first-pass miss is not a wrong
judgment but an *unswept category*: the reviewer applied a narrow lens
and never looked at a whole class of failure, and a later reviewer
catches it not by being smarter but by sweeping a category the first
skipped. A shared roster makes the breadth explicit and lets one pass
cover it — so an independent later pass is spent on genuine
independence (a different prior), not on a category the first simply
did not look at.

**The sweep is generic and change-agnostic** — the same roster every
time, never a change-specific list of "what to push on." That
distinction is exactly what keeps it compatible with *don't telegraph
the lens* (below): a standing set of perspectives is not a hint about
where this change's bug lives.

**The lenses:**

1. **Claims** — probe every load-bearing claim against the *current*
   tree: "exists / works / is available / is atomic / fails closed /
   will use X." A **forward** claim ("will exist", "the translator will
   support") gets the *same* probe as a present-tense one — run the
   check (load it, call it, inspect the bytes), never accept it on
   assertion. This is the probe-reducible miss a pure checklist never
   catches.
2. **Production path exercised by tests** — the public entry point is
   tested *through*, not just a helper or a stub of the very thing that
   breaks.
3. **Design completeness** — preconditions, invariants, edge cases
   (empty / None / zero / single / N≫1 / mismatched units or CRS), and
   failure modes are stated, not left implicit for a new mechanism.
4. **Silent failure / fail-closed** — guards raise loudly rather than
   degrading or returning empty; they cover all configs and stages, not
   only the declared edges; any fail-open path is intentional, not
   accidental.
5. **Cross-document consistency** — scan the governing docs, the
   roadmap, and code/tests/doctrine for references to what is changing:
   an orphaned reference to the old or deferred behavior, or an existing
   tool / path / constraint the change should use or update.
6. **Drift** — docs, examples, changelog, and commit claims match the
   behavior that actually shipped.
7. **Lifecycle / process placement** — for a doctrine or process
   change: *who* runs this, *when*, in *which* ceremony or serialization
   point; the change has a home in the lifecycle, not just a rule.
8. **Domain / scientific validity & scope** — methods are grounded and
   documented; scope has not quietly expanded; each new abstraction
   earns its existence.
9. **Name the satisfier** — every finding states the test / guard /
   doc / scope-cut / explicit `wontfix` that would close it. A finding
   with no satisfier is an observation, not yet a finding. At archive
   time each satisfier maps onto a disposition token
   (`doctrine/lifecycle.md` > "Archive precondition"), and the mapping
   is total: *test* → `guard`, *guard* → `guard`, *doc* → `accept`,
   *scope-cut* → `accept`, *wontfix* → `wontfix`. Naming the satisfier
   and naming who pays for it are then the same act.

**Falsifiable coverage, not "checked."** A swept lens is credible only
if its claim is *falsifiable* — it cites the file path, test node,
line, or command output that backs it ("#2: `tests/contract/foo.py::test_bar`
calls the public entry"). A bare "#2: checked" is an *incomplete*
review, not a pass. This is the guard against the sweep becoming a
self-certification ritual.

**Signal the sweep is going ritual.** A coverage line that converges on
a uniform "all lenses swept, clean" *across* changes — with no
difference in finding density between a trivial change and a complex one
— is the sweep going hollow, not the changes getting cleaner. When that
pattern shows, the sweep has become a box-tick: tighten the lenses or
trim the roster. The negative-space half of the coverage line
(*Not covered / low confidence*, below) is the early antidote — it
forces naming what was *not* covered, which a hollow all-clear cannot.

**The evidence bar is staged.** The same lens demands different
evidence at different maturity levels — the sweep must not over-demand
code-level proof at proposal time, nor under-demand it at code review.
For lens #2 (production path), for example:

* **Proposal review** — is the public-path evidence *promised and
  scoped* in the verification plan?
* **Plan review** — is it *sequenced into a chunk* and protected by
  acceptance criteria?
* **Code review** — does the landed test *actually call the public
  path* today?

**The sweep is a floor, not a ceiling**, and it **never silently
downgrades a declared-`required` review tier.** It names the minimum
breadth to cover and report; it can recommend *upward* escalation when
coverage is weak (see *recommend-and-decide*, below), but a tier the
lifecycle declared `required` still runs regardless.

The domain adds its own probes — units, coordinate systems, numerical
edges, resource resolution — so each adopter extends the roster with
the checks its high-risk surfaces demand. The collaborative-skeptic
stance (`collaboration-stance.md`) is the posture the sweep operates
in: steelman the change, then hunt for what it missed.

## Recommend-and-decide — the second independent pass

The review sweep is the *one* pass that always runs. What it cannot
decide on its own is whether a **second, structurally-independent
(cross-type) pass** is worth its cost — that is the Maintainer's call,
and the first reviewer's job is to *inform* it, not pre-empt it. So
every first-pass review **ends with two things**.

**1. A two-part coverage line.** Not a verdict — a map of what the pass
did and did not cover:

* **Covered** — the lenses swept, each with its falsifiable citation
  (the file / test-node / line / command that backs it).
* **Not covered / low confidence** — the negative space: "did not
  exercise the scientific math", "could not run the sibling-repo test",
  "same-type reviewer — no cross-type independence on this pass." A
  covered-only line manufactures false comfort; the *negative* space is
  what the Maintainer most needs, and it is the evidence behind the
  recommendation.

**2. An explicit second-round recommendation.** *Recommended* or *not
recommended*, with reasons, grounded in that coverage line. The factors
that might once have fired an automatic second review — high blast
radius, a novel framework or abstraction, a scientific-correctness or
security / trust-boundary surface, weak coverage in the negative-space
line — are **inputs to this recommendation**, not a gate that fires by
itself.

**The decision is the Maintainer's, never an automatic default.** A
second independent round is neither default-on for the "risky" triggers
nor default-off for the routine; the reviewer recommends, the Maintainer
decides per change. This is the same authority structure as the
**Decision-support Round-2 review** (above): a later pass provides
independent perspective *to the Maintainer*, who is the only actor with
authority to weigh competing reads and Decide.

**A declared-`required` tier stays a floor.** Recommend-and-decide
governs only the *optional escalation beyond* what the lifecycle already
declared. A `Plan review: required(External cross-type)` line still runs
regardless of any recommendation — "don't default to a second round"
never downgrades a tier the proposal or plan declared `required`.

Why this shape: the cost of a reviewer-pass is real, and most redundant
later passes only re-caught *lens-coverage* misses the sweep now folds
into pass one. But some later passes catch what a *different prior*
genuinely sees first — irreducible independence the sweep cannot
substitute for. The record cannot size those two shares in advance, so
the safe instrument is not an automatic rule (which would trade away an
unknown amount of independence) but a human deciding per change, with
the coverage line as evidence. Whether the trade actually pays is
measured, not asserted — see the late-blocker bundle in
`lifecycle-metrics.md`.

## Briefs to reviewers — don't telegraph the lens

When handing work to a reviewer — especially the cross-agent-type
External review the independence floor calls for — brief on *facts*,
not *judgment*. A page or so, not several.

**Include**: what shipped, where (commits + file paths), the
reviewer's deliverable, how to run the tests, and procedural
constraints (don't commit, append findings, and so on).

**Leave out**: a list of "what to push on," a list of "what's already
known so you can skip it," a ranking of which surfaces matter most —
anything that telegraphs what the briefing agent expects the reviewer
to find. Spelling out the lens turns an independent read into
hypothesis-confirmation: you are asking the reviewer to check your
guesses rather than form their own. Brief on facts; trust the reviewer
to bring the lens.

**The review sweep is not telegraphing.** The standing review sweep
(above) might look like it contradicts this — it hands the reviewer a
list of lenses. It does not, and the distinction is exact: the sweep is
a **generic, change-agnostic** roster of perspectives every reviewer
applies to *every* change and reports coverage on. Telegraphing is
supplying **change-specific judgment** — "the bug is probably in the
override path", "focus on the CRS handling here" — which seeds the
answer for *this* change. A standing lens roster is the former; a hint
about where this change fails is the latter. The reviewer reporting
*which generic lenses they swept* (the coverage line) is the opposite
of a briefing agent seeding *what to find*. Keep the brief on facts;
the sweep is the reviewer's own standing instrument, not a lens you
handed them.

The same applies to Internal-review handoffs and to any task brief at
session start (an implementing agent picking up a plan): over-detailed
framing pushes the recipient toward executing your plan instead of
thinking independently. Short is honest.

## Restricted verification surfaces

Every review tier above assumes the reviewer can, in principle,
*run* what they review. When a reviewer **cannot execute** a
surface, the review is weaker in practice than its tier suggests:
the reviewer can read the change but cannot confirm its behavior.
The constraint is not about a second programming language — it is
any **asymmetrical execution environment**:

* a language the reviewing agent cannot run;
* a proprietary compiler or a licensed runtime the reviewer lacks;
* a license server, a private network, or credentials the reviewer
  does not hold;
* data at a scale the reviewer cannot stage, or specialized
  hardware the reviewer does not have.

This is a **gate on the surface, not on the team's language
count**: a single-language project with private data, a
hardware-only workflow, or a licensed runtime has restricted
verification surfaces and needs this discipline; a multi-language
project is only one common instance.

The mechanism:

* **A `verification command`** — the exact command that checks a
  change to the surface — is recorded *with* the surface (e.g. in
  the readiness map, `team-gated/legacy-agent`).
* **A `verification owner`** — *who can actually run it* — is
  recorded alongside. A command no reviewer can run is not a
  verification path.
* **Pre-framework fallback.** Until an executable verification path
  exists for a surface, a behavior change to it carries
  `verification owner = the Maintainer` and **cannot be
  autonomously verified** — the change waits on the human who can
  run it. This is honest about the review tier rather than
  pretending the structural floor was met.

The multi-language instance of this discipline — each language's
native harness, the named cross-language seams — lives in the
`team-gated/dual-language-tests` module; the readiness schema in
`team-gated/legacy-agent` reuses the same `verification command` /
`verification owner` fields. Both point here for the general rule,
so a project reaches the doctrine whether or not it selects either
module.

## Why this is the contribution

The Dual-Review model is a faithful instantiation of **scientific
peer review** — and, on the openness and independence axes, a more
rigorous one: the review is recorded in full, in the open, and the
independence is structural rather than declared. For a
scientific-software audience this is the practice that most
clearly carries the methodology's claim — that software built this
way earns trust the way a result does.

## Adaptation

Review *tiers* are roles any contributor can fill (`roles.md`);
the review *apparatus* is team-gated (`dimensions/`). A solo,
single-agent team runs the kernel's review — the same agent in a
fresh session — and reserves heavier scrutiny for genuinely
contract-touching changes. A team with two agent types, or
multiple humans, runs the full Dual-Review model. The bootstrap
never installs more review apparatus than the team can staff.
