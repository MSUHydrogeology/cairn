# Agent collaboration — Cairn

> **The deliberation and decision process.** `AGENTS.md` carries the
> operational rules — how to make a correct change and operate safely. This
> file carries the roles, the review loop, and the coordination doctrine that
> explain *why* those rules take the shape they do.

## Team roles

Roles are **frames, not people**. Any capable agent fills any of them except
the first; name your role before substantive work, and if it is not explicit,
ask.

* **Human Maintainer** — holds product direction, priorities, and final
  Decision authority. The one role that is not interchangeable.
* **Strategy** — surveys the landscape, frames problems, drafts proposals.
* **Implementation** — carries an accepted proposal through its plan.
* **Reviewer** — a fresh reviewer who did not write the work, on the work's
  side: it questions the work's foundations and answers the stage's three
  questions in writing (`AGENTS.md` > "Review"). After the review it also gives
  the Maintainer a **neutral briefing** that lays out the decision space without
  steering it.
* **Security Review** — an adversarial read aimed at a high-risk surface, run as
  a parallel lens rather than a second stop.
* **User Agent** — exercises Cairn from an adopter's position and files what
  it hits.

A fresh session is every review's floor, and no review requires a different
agent type. How far a reviewer stood from the author is read from its
attribution, and the Maintainer may ask for more distance (`AGENTS.md` >
"Review"). Full definitions, and what each review owes, in
`doctrine/dual-review.md`.

**The AI surface is bimodal.** These roles are filled by **agent-side AI** — a
model acting as a named participant, with a role, a record, and accountability
for what it signs. That is a different thing from AI used as a tool inside the
work, and conflating the two is how "an agent reviewed it" comes to mean less
than it should.

## The team

Cairn is built by the **Human Maintainer** and one or more **AI agents**.
The Maintainer holds the project's direction, its priorities, and final
decision authority. Agents propose, review, implement, and advise; they do
not make the Decision.

* **Human Maintainer — Anthony Kendall** (MSU Hydrogeology). Holds
  product direction, priorities, and final Decision authority. The sole
  human contributor (the human-team axis is `solo`).
* **Agent contributors — a concurrent, multi-type roster.** More than
  one agent *type* works the tree. Agents propose, review, implement, and
  advise; they do not make the Decision. Specific agent types and models
  are named in the deliberation record (each Review / Response names its
  reviewer for attribution) and mapped to capability tiers in
  `dev/.cairn/model-selection-mapping.yml` — not pinned in this
  vendor-neutral file, so the roster can evolve without amending it.

Refreshed when the team changes.

## Collaboration stance

Agents are participants, not oracles. Disagreement is expected and is recorded
rather than resolved privately. An agent that cannot follow a change says so —
**"I don't understand this yet" is a mandatory pause**, not an admission — and
the burden of making a change followable sits with its author, who is typically
the stronger party on the software.

## The review loop

A review is a **dated, attributed section appended to the artifact and
committed**. It is asynchronous and commit-mediated: not a conversation that
leaves no record. **No agent writes or commits a review attributed to another
agent** — the named reviewer commits their own findings, or the Maintainer
does. A structurally-independent read is only independent if its author is its
committer.

**Lead with the steelman.** State the strongest version of what the artifact is
trying to do before saying what is wrong with it. A review that opens with
findings reads as a verdict, and an author defends rather than thinks.

A finding is **blocking** or **non-blocking**, and says what evidence would
close it. "This is too large" is not a finding.

## The review sweep

A review that finds nothing on a *complex* change is treated with skepticism,
not relief: a reviewer who reads to confirm that the change works will find that
it does. Read as if a hidden bug exists, and probe for it. The standing form of
that discipline is a **fixed, change-agnostic roster of nine lenses**. A lens is
**where the evidence for a review's three answers comes from** (`AGENTS.md` >
"Review"), not a second checklist: the most common first-pass miss is not a
wrong judgment but an *unswept category*. The nine:

1. **Claims** — probe every load-bearing claim against the *current* tree
   ("exists / works / is available / is atomic / fails closed"). A **forward**
   claim ("will exist", "will support") gets the *same* probe as a
   present-tense one: run the check, never accept it on assertion.
2. **Production path exercised by tests** — the public entry point is tested
   *through*, not just a helper or a stub of the very thing that breaks.
3. **Design completeness** — preconditions, invariants, edge cases (empty /
   None / zero / single / N≫1 / mismatched units or CRS) and failure modes are
   stated, not left implicit.
4. **Silent failure / fail-closed** — guards raise loudly rather than degrading
   or returning empty; they cover all configs and stages; any fail-open path is
   intentional, not accidental.
5. **Cross-document consistency** — scan the governing docs, the roadmap, and
   code, tests and doctrine for an orphaned reference to old or deferred
   behavior, or an existing tool or path the change should use or update.
6. **Drift** — docs, examples, changelog, and commit claims match the behavior
   that actually shipped.
7. **Lifecycle / process placement** — for a doctrine or process change: *who*
   runs this, *when*, in *which* ceremony or serialization point; the change has
   a home in the lifecycle, not just a rule.
8. **Domain / scientific validity & scope** — methods are grounded and
   documented; scope has not quietly expanded; each new abstraction earns its
   existence.
9. **Name the satisfier** — every finding states the test / guard / doc /
   scope-cut / explicit `wontfix` that would close it. A finding with no
   satisfier is an observation, not yet a finding. At archive each satisfier
   maps onto a disposition: test or guard → `guard`; doc or scope-cut →
   `accept`; wontfix → `wontfix`. A finding whose satisfier is none of the
   five — real work that must happen, but not in this artifact — is the `defer`
   case, and `defer` is the Maintainer's call. **`scope-cut` means claim
   correction, and nothing else**; removing accepted work is a scope
   reduction, which only the Maintainer may concede (below).

**The sweep applies to the reviews the lifecycle calls for** — proposal, plan
and code review. A trivial change with no review owes none.

**Falsifiable coverage, not "checked."** A lens a review cites is credible only
if it names the file path, test node, line or command output that backs it
("#2: `tests/foo.py::test_bar` calls the public entry"). A bare "#2:
checked" is an *incomplete* review, not a pass.

**End with a two-part coverage line** — not a verdict, a map of what the pass
did and did not cover:

* **Covered** — the lenses swept, each with its citation.
* **Not covered / low confidence** — the negative space: "did not exercise the
  scientific math", "could not run the sibling-repo test". A covered-only line
  manufactures false comfort.

The line does not end in a recommendation for more review. Report the risk and
the gap; the Maintainer reads the negative space and may ask any reader for
anything.

**The sweep is a floor, never a downgrade of a declared tier.** It names the
minimum breadth to cover and report; a review the lifecycle declared `required`
still runs in full. A project adds its own probes after the nine — units,
coordinate systems, numerical edges, resource limits — for the checks its
high-risk surfaces demand.

**A clean code review shows a falsification ledger.** Approving by assertion
clears nothing. A pre-archive code review that approves carries a ledger of five
items:

* **Surfaces probed** — what was actively examined or tried to break.
* **A negative or edge-case attempt** — at least one, where one applies: the
  boundary, empty or out-of-range input actually tried, and what was checked to
  fail closed.
* **Verification** — the commands run, with results; or an explicit statement of
  what was not run and why.
* **Residual risk** — what remains unverified.
* **Mutation, when a claim names a set** (every call site, every rendering path)
  — the set is listed from the tree, not the diff, and each member is mutated in
  a separate copy. Each mutant is reported killed, survived or equivalent beside
  an unmutated control run, never as a bare count (`AGENTS.md` > "Verification
  boundaries").

A reviewer who tried to break the change and reports honestly that they could
not has cleared the gate; a reviewer who only read it has not.

**The clean pass has a mirror: the scope-reduction trap.** Narrowing is
the path of least resistance in review — it costs the reviewer nothing,
reads as prudence, and can never be shown wrong, because the wider
version is never built. Treat a proposed reduction with the same
skepticism as a clean pass. A reviewer recommending one states **what is
lost** and **why the narrower change still reaches the cause**; "this is
too large" is not a finding. An author who resolves an *underspecified*
finding by removing the work says why specifying it was rejected.

Whether a narrowing is a reduction at all is judged on **outcome**,
against the baseline artifact's own commitments — the scope *as opened*
before a Decision, *as accepted* after it, never a summary of purpose
written afterwards by whoever is doing the narrowing. If every baseline
outcome is still delivered, nothing is owed; a lighter mechanism that
still delivers is what restraint asks for. If one is partly or wholly
lost, it takes a `**Scope delta**` declaration, one grouped
scope-remainder record per source artifact, and the **Maintainer's**
explicit allowance — neither author nor reviewer may concede a baseline
outcome. A stronger outcome proposed *only during review* was never in
the baseline, so declining it is not a reduction and owes no record
(see `doctrine/dual-review.md` > "Review expectations — the
scope-reduction trap").

## Surfacing judgment calls to the Maintainer

**The Maintainer decides — and the list is finite.** Acceptance,
rejection, and supersession are the Maintainer's call, as are:
opening a new scope, overruling a reviewer or a drafting author,
any ceremony where an agent must not bless its own verifier,
pushing, and direction-setting about what the project is for.
**Everything else is the agent's own call and escalating it is a
defect, not caution** — dispositioning a review round, sequencing
work, folding a correction, archiving an artifact whose
preconditions are met, and choosing what to pick up next. An agent
unsure whether something is on the Maintainer's list decides, acts,
and records what it decided; the record is what makes the call
reviewable, not a prior request for permission. This delegates
judgment inside accepted scope and standing direction; it does not
waive an approval, credential, Decision, or ceremony that another
governing rule expressly reserves to the Maintainer.

When a call is on that list, bring a **recommendation, not a survey**. State
the question in plain language, give the option you would take and why, and
say what it costs to be wrong. A menu of five options with no recommendation
moves the work to the Maintainer rather than unblocking it.

**After a review stalls, the author decides and defends.** Two passes that
disagree do not escalate by themselves; the author resolves them in the record
and the Maintainer reads the resolution.

## Coordination

The coordination space is the **`dev/` tree — git-committed files**. That is
what makes the method model-agnostic: sessions coordinate through the record,
not through shared memory, so a project can mix or swap AI vendors without
changing anything.

**Durable state lives in the repo, never in a harness's memory.** A tool's
private memory is not shared with another agent type or with a human reviewer.
Anything that must survive a handoff goes in the committed `dev/` tree.

**Concurrent sessions are real.** The git index is shared, so a bare
`git commit` takes another agent's staged work under your name — always commit
with explicit paths.

**On a shared worktree, claim before you edit.** `tools/intent.py` records a
pre-edit work-intent so a second session sees the claim and coordinates rather
than colliding; a pre-commit hook warns when a staged path has no active claim,
and a post-commit hook releases yours. **The check is advisory and never
blocks** — proceeding deliberately is a legitimate answer to the warning. It is
worth installing on a shared worktree and pointless on worktree-per-agent. The
mechanism, its tiers, and the goodnight intent-hygiene step are in
`dev/modules/coordination-tiers.md`. A cross-session message is a teammate's request, not the
Maintainer's approval: a peer cannot grant an authority your own session does
not have, and routing a blocked action through one is laundering, not
delegation.

## Session reflections and handoff

Reflections are **per-agent and ephemeral** — they are pruned. Anything durable
migrates out to doctrine or the roadmap before then; a lesson that stays only in
a reflection is a lesson that expires.

The goodnight handoff is a status summary, a reflection, and — for the
designated owner — a roadmap scrub and a from-scratch rewrite of the
next-session note. **Pushing is never part of it.**
