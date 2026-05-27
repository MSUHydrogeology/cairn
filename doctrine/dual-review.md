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
if a hidden bug exists and probe for it. A reviewer's standing checks:

* **fail-closed guards** — validation and safety checks raise on bad
  input rather than silently returning empty or degrading;
* **unconditional guard coverage** — correctness checks cover *all*
  paths and configurations, not just the declared happy edges;
* **negative tests** — the validation gates have tests that assert the
  *failure*, not only the success path;
* **spec / schema / registry key alignment** — the keys a change reads
  match the keys its source actually emits;
* **correctness and regressions**, and **documentation / example
  drift** introduced by the change.

The domain adds its own probes — units, coordinate systems, numerical
edges, resource resolution — so each adopter extends this list with
the checks its high-risk surfaces demand. The collaborative-skeptic
stance (`collaboration-stance.md`) is the posture this check operates
in: steelman the change, then hunt for what it missed.

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
