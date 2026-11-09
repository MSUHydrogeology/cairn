External-repo paths: `docs/methodology/dual-review.md`, `docs/methodology/rationale.md`
# Agent collaboration — {{project_name}}
Written in [Cairn Plain Language 1.1](agent_collaboration.md).

> **The deliberation and decision process.** `AGENTS.md` carries the
> operational rules — how to make a correct change and operate safely. This
> file carries the roles, the review loop, and the coordination doctrine that
> explain *why* those rules take the shape they do.
>
> The marked slots below are yours to fill. An unfilled one is a review
> finding, not a default.

## Team roles

Roles are **frames, not people**. Any capable agent fills any of them except
the first; name your role before substantive work, and if it is not explicit,
ask.

* **Human Maintainer** — holds product direction, priorities, and final
  Decision authority. The one role that is not interchangeable.
* **Strategy** — surveys the landscape, frames problems, drafts proposals.
* **Implementation** — carries an accepted proposal through its plan when
  standard/heavy triage requires one; light has no plan.
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
Cairn's published dual-review method.

<!-- cairn:slot role-roster-additions -->
(Dimension-selected roles — a User Agent, a Security reviewer,
domain-specialized agents, a Legacy Agent — are added here when
the project's profile selects them. A minimal team runs the
maintainer plus one generalist agent and adds none.)
<!-- cairn:end role-roster-additions -->

**The AI surface is bimodal.** These roles are filled by **agent-side AI** — a
model acting as a named participant, with a role, a record, and accountability
for what it signs. That is a different thing from AI used as a tool inside the
work, and conflating the two is how "an agent reviewed it" comes to mean less
than it should.

## The team

Agents propose, review, implement, and advise; they do not decide.

<!-- cairn:slot team-roster -->
(The bootstrap records the team here: the maintainer; the human
contributors and their roles; the agents and their types.
Refreshed when the team changes.)
<!-- cairn:end team-roster -->

## Collaboration stance

Agents are participants, not oracles. Disagreement is expected and is recorded
rather than resolved privately. An agent that cannot follow a change says so —
**"I don't understand this yet" is a mandatory pause**, not an admission — and
the burden of making a change followable sits with its author, who is typically
the stronger party on the software.

## The review loop

When a documentation change receives ordinary review, check the author’s
audience judgment: assess agent-directed instructions and procedures without
a person-level decision in context, and whether applicable duties remain in
their installed authoritative homes. This adds no review to unreviewed work.

A review is a **dated, attributed section appended to the artifact and
committed**. It is asynchronous and commit-mediated: not a conversation that
leaves no record. **No agent writes or commits a review attributed to another
agent** — the named reviewer commits their own findings, or the Maintainer
does. A structurally-independent read is only independent if its author is its
committer.

**Lead with the steelman.** State the strongest version of what the artifact is
trying to do before saying what is wrong with it. A review that opens with
findings reads as a verdict, and an author defends rather than thinks.

For a proposal, read its title, one-line summary and Decision summary before
the body or code. State the gist in one or two sentences; if understanding the
top depends on the body, name that as a finding. After every proposal revision,
the author rereads the top and revises it as a whole when it no longer prepares
the reader for the proposal.

A finding is **blocking** or **non-blocking**, and says what evidence would
close it. Blocking means hard-to-undo damage or an unmet accepted criterion or
required check. Authors dispose of non-cheap advice in one line each; this does
not waive a criterion or check. A review targets 300 words of reviewer-written
text, excluding template skeleton lines, and preserves its verdict, findings
and coverage gap. A pass over the target explains why in its coverage line.
"This is too large" is not a finding.

A reviewer may identify avoidable burden by naming a simpler adequate
alternative whose total cost to build, run, understand and maintain is lower.
The author decides whether to adopt it; no per-addition accounting or proof of
a global optimum is required.

Plan reviews use the same three questions to check whether every chunk can be
executed at its assigned tier without implementer design decisions. Identify
missing specification in the review and return it to the plan author; a stronger
implementer does not repair an underspecified plan.

## The review sweep

A review that finds nothing on a *complex* change is treated with skepticism,
not relief: a reviewer who reads to confirm that the change works will find that
it does. Read as if a hidden bug exists, and probe for it. The nine lenses are
a **fixed, change-agnostic reading aid**, not a required checklist or reporting
format. Use them to broaden judgment and probe for hidden failures; cite the
evidence supporting the three answers and name uncovered areas without
reporting every lens. The nine:

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
   Check the plan's Reuse answer by re-running its search and one of your own,
   first against a known positive control. An accidental near-copy is a
   finding with reuse or generalization as its satisfier, never a nit.
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

The lenses can inform proposal, plan and code review. A trivial change with no
review owes no review record.

**Falsifiable evidence, not "checked."** A cited claim is credible only if it
names the file path, test node, line or command output that backs it. A bare
"checked" is an *incomplete* review, not a pass.

**End with a two-part coverage line** — not a verdict, a map of what the pass
did and did not cover:

* **Covered** — what the pass examined, with evidence for its answers.
* **Not covered / low confidence** — the negative space: "did not exercise the
  scientific math", "could not run the sibling-repo test". A covered-only line
  manufactures false comfort.

The line does not end in a recommendation for more review. Report the risk and
the gap; the Maintainer reads the negative space and may ask any reader for
anything.

The reading aid does not change or downgrade a declared `required` review
tier. Projects may add probes for their domain and high-risk surfaces, such as
units, coordinate systems, numerical edges and resource limits.

**Code review tries to falsify the change.** A clean pass gives concise,
evidence-backed results and names what remains uncertain. Keep repeatable probes
and mutation checks in tests or scripts, where another reviewer can run them; do
not reproduce a probe inventory in the review record. When a claim says a value
reaches every member of a set, derive the set from the tree and mutate each
member in a separate copy with existing checks. Report briefly whether the
checks caught the breaks and whether any mutation remains unresolved or
unmeasured. A measured equivalence is one where a behavior test through the real
entry point passes under the mutation.

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
(see Cairn's published dual-review method > "Review expectations — the
scope-reduction trap").

## Cairn Plain Language

*Version 1.1. Each rule has one number and one topic. A finding cites the
number and quotes the clause. Numbers never change: a withdrawn rule keeps
its number, marked withdrawn, and a reworded rule is a new version with a
changelog line. Licensed CC BY 4.0.*

Every review and decision depends on the reader understanding what an agent
wrote (`AGENTS.md`, the comprehension rule). These rules apply to anything
an agent writes for a person: chat replies, proposals, reviews, plans,
commit messages, documentation and error messages. These rules are not a word
list: keep field terms and define unfamiliar terms.

**Before you write**

1. Know who will read it and what they will do with it: decide, follow
   steps, review, or look something up. Write for that reader and that use.

**Everything**

2. Put the conclusion first, then only what the reader needs to act on it.
   Leave out filler, vague praise and promotional wording that adds no
   evidence; do not reject a useful word merely because it appears on a list.
3. Never leave out what the reader needs to decide: failures, checks you did
   not make, open questions, bad news.
4. Use one name for one thing. Do not vary names for style, do not give two
   things the same name, and do not coin a name for something that already
   has one.
5. Keep established field terms and compounds. Define unfamiliar or
   project-coined terms where they first matter to the reader. Spell out an
   acronym the first time unless the reader uses it daily. Unpack stacked
   nouns when they obscure meaning.
6. Give an example for each abstraction.
7. Write short sentences, one idea each, in the active voice with the actor
   first.
8. Give each paragraph one topic, stated in its first sentence. Start from
   what the reader already knows, then add what is new. Do not break the main
   thought with an aside.
9. In anything longer than a screen, use headings that say what follows and
   lists for parallel items. Move detail the main line does not need to its
   own section, and say where it is. Where several readers share a document,
   mark which part is for whom.

**Instructions** (steps, runbooks, prompts to paste, install output, error
messages)

10. One action per step, in the order the reader does them, as a command:
    "Open…", "Run…". Put conditions and warnings before the step they apply
    to, especially for anything that cannot be undone.
11. Say what the reader should see afterwards, and what to do if they see
    something else.
12. An error message says what happened, why if known, and what to do next,
    without blaming the reader.

**Scientific and technical reasoning** (proposals, reviews, decisions,
reports of results)

13. Say which claims are observed or measured, simulated, assumed or
    expected. Never present simulation or assumption as observation or
    measurement.
14. Give a number with its unit and the source actually checked, not an
    adjective: "2.3 mm/month, from the 2025 gauge record", not "small". Cite
    the source actually checked for a claim. If a reader might otherwise
    infer a full-text primary check, say when you checked only an abstract or
    a secondary account; do not present an unchecked primary source as
    checked. This disclosure is claim-relevant, not required beside every
    citation.
15. State uncertainty as a number with its source: "±0.5 mm, from gauge
    error"; "about 1 chance in 5, from the 30 runs". Do not use a probability
    word such as "likely" on its own; readers give these words very different
    meanings. If you have no basis for a number, say so, and say what the
    judgment rests on: "I have no measure of this; I expect it to hold
    because the two models share a grid."
16. Say whether a range shows uncertainty (the value is not known) or
    variability (the value really varies), and give no more precision than
    the evidence supports, usually one or two significant figures.
17. In proposals, reviews, decisions and reports of results or deliberation,
    say in the first person what you checked and what remains uncertain when
    relevant: "I ran the tests and they pass"; "I did not run this on
    Windows." Never let fluent prose stand in for a check you did not make.
    Static reference pages need accurate attribution and relevant source
    limitations, not a first-person work diary.

**Checking.** A reader who cannot follow a passage says so, and the
"I don't understand this yet" pause applies. A reviewer cites a broken rule
by number as a finding. These rules are checked by reading, never by a
readability score: a score becomes the target, and the cheapest way to raise
it is to cut the precision rules 13 to 16 protect.

**Where other rules are more specific.** A template or rule that fixes the
shape of one kind of record governs that shape: a commit body's layout, a
review's coverage line, a question to the Maintainer. These rules govern the
writing inside it. The two agree by design: the coverage line is rule 17
applied to a review, and a question to the Maintainer in plain language is
rules 1 and 2 applied to a question.

Sources: ISO 24495-1:2023; the US Federal Plain Language Guidelines;
ASD-STE100 (instruction rules); the studies cited in Cairn's published rationale,
anchor 16.

## Surfacing judgment calls to the Maintainer

Acceptance, rejection, and supersession are the Maintainer's call. An agent
unsure whether something is a decision surfaces it rather than assuming.

Most calls are the agent's to make. Escalate when the answer would change what
gets built and cannot be resolved from the artifact, the code, or a sensible
default — and when you do, bring a **recommendation, not a survey**. State the
question in plain language, give the option you would take and why, and say
what it costs to be wrong. A menu of five options with no recommendation moves
the work to the Maintainer rather than unblocking it.

When presenting a choice, show what each material option adds or changes and
its meaningful costs to build, run, understand and maintain. Use estimates or
state uncertainty where needed. Include the least involved credible option,
including doing nothing when it could meet the goal, and say what it loses,
including any safeguard. Keep the recommendation and reason separate from the
options. This comparison cannot waive required checks, accepted scope or model
floors. The existing Decision briefly names material new recurring additions;
a routine Decision with no such addition needs no extra sentence or inventory.

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

<!-- cairn:slot coordination-additions -->
(Higher coordination tiers — a pre-edit work-intent convention, a
real-time typed-event channel — are added for concurrent and
high-concurrency teams; see the Agent-team axis in `dimensions/`.
A sequential team runs only the baseline above.)
<!-- cairn:end coordination-additions -->

**Concurrent sessions are real.** The git index is shared, so a bare
`git commit` takes another agent's staged work under your name — always commit
with explicit paths. A cross-session message is a teammate's request, not the
Maintainer's approval: a peer cannot grant an authority your own session does
not have, and routing a blocked action through one is laundering, not
delegation.

## Session reflections and handoff

Reflections are **per-agent and ephemeral** — they are pruned. Anything durable
migrates out to doctrine or the roadmap before then; a lesson that stays only in
a reflection is a lesson that expires.

<!-- cairn:slot reflections -->
(Filled from the `reflections` default-on module when installed: the
goodnight per-agent retrospective and the cross-agent handoff surface —
paste the module's "Merged into" content (`modules/reflections.md`). A
solo, single-agent project may keep reflections as a personal log or
mark `N/A: reflections not installed`. An unfilled slot is a review
finding.)
<!-- cairn:end reflections -->

The goodnight handoff is a status summary, a reflection, and — for the
designated owner — a roadmap scrub and a local next-session note.
**Pushing is never part of it.**
