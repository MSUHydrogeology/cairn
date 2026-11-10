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

When asking the Maintainer to choose, describe what each material option adds
or changes and its meaningful costs to build, run, understand and maintain; use
estimates or name uncertainty where useful. Include the least involved credible
option, including doing nothing when it could meet the goal, and state what it
would lose, including any safeguard. Give the recommendation and its reason
separately from the option descriptions. This comparison cannot waive required
checks, accepted scope or model floors. In the existing Decision cost prose,
name material human operations each option adds or changes, their follow-up
homes, and estimated counts, including zero when useful to show absence.
Briefly name material new recurring additions. Do not inventory routine agent
work. If neither human operations nor recurring additions are material, no
extra sentence is needed.

## Review rules

A fresh reviewer who did not write the work, on the work's side, reads a
committed version. One review stance applies at every stage. The stage sets
the questions; no agent picks another kind. Each reviewer
answers the stage's three questions: should it happen as framed, what is the
best alternative, and what would show it wrong? The nine lenses in
`dev/agent_collaboration.md` are a reading aid; cite evidence for the answers
and name what the pass did not cover, without a required lens-by-lens report.
Understanding is a precondition of the Decision:
if it fails, pause. Lead plain, with precision beneath. A pass starts with three
evidenced Foundations answers. Each answer states its point in a sentence;
it may also point to a finding. Question 3 names a forward test even when
there are no findings. It recommends improvements; the author decides.
There is no finding quota. Target each pass at 300 words of reviewer-written
text, excluding template skeleton lines: verdict, findings and coverage gap.
A pass over the target explains why in its coverage line. Findings state their
evidence and what would close them. A
finding blocks only when shipping could cause hard-to-undo damage or an
accepted criterion or required check is unmet. Authors dispose of non-cheap
advice in one line. They do not waive criteria or checks. A reviewer proposing a
narrower scope names what would be lost and why the rest still reaches the
cause; only the Maintainer concedes a loss.

Plan review checks whether each chunk is specified for its assigned model tier
without asking the implementer to make design decisions. Name missing design
in the existing three answers and return the chunk to its author for repair;
do not substitute a stronger implementer for an incomplete plan.

Near plan chunks and code-review response, cheap follow-ups mean a few
person-steps, no new Decision or public name beyond the plan, and a test in
existing test files. Code review identifies cheap findings and advice; before
archive the response fixes each or uses an existing deferral reason with the
Maintainer's verbatim authorization. Cheapness grants no scope, boundary or
check waiver. Non-cheap advice keeps its existing disposition. Required failed
checks remain implementation work.

Every existing step record captures elapsed time and reported or defensibly estimated token use;
write `unknown` when unavailable.

The Maintainer alone calls an External read on one named artifact that exists
now. A standing call covering future artifacts requires a proposal. A team
roster adds no read. The called reviewer answers the same three questions and
names the distance in the record. The record and commit quote the Maintainer's
call verbatim and identify its source as `Called by: Maintainer -- Decision at
<commit>` or `-- chat, <date>`. `Tier: External` without
`Called by` is an ordinary pass. No tool checks the quote; the next reviewer
and Maintainer do. The call adds focus, removes no owed answer, replaces no
usual review, clears no Security Review and grants no Decision or plan-fence
authority. Agents never request or declare External as required; they may name a
risk and coverage gap. High-risk work keeps its separate Security Review
obligation. `usual + Security Review` means two passes; the ordinary pass
cannot clear it. A plan's `required(Internal + Internal Security Review)` is
cleared only by an appended plan review with a matching `Obligation` line;
readers, not a tool, check that line. Plan review is fresh-context; code review
is by someone other than the implementer and does not reopen the Decision. A
reviewer does not re-run implementation checks; the implementation record owns
that evidence. See Cairn's published dual-review procedure for the complete
details.

The proposal Decision sets its tier: `light` (one short review, no plan),
`standard` (one pass per stage), or `heavy` (adds Security Review). Light is
the default; plan triage applies only to standard/heavy. An author's higher proposed tier stands unless the Decision
changes it. Named high-risk surfaces and added or widened trust boundaries
trigger heavy. A newly discovered boundary stops the work for reassessment.
Ordinary uncertainty takes the lighter lane with its reason. The trivial lane
is unchanged. See Cairn's published lifecycle method for lane details.

## Agent execution retries

**Execution retries.** For a correctable execution error in work at or above its
capability floor, allow up to two same-tier retries after the initial failed
attempt. Each retry uses concrete failure feedback, retains earlier failure
evidence and reruns only the affected check during the correction loop. After
two failed retries, re-run once one tier up. Escalate immediately if the failure
shows the task exceeds the assigned tier; work below its capability floor is
not eligible. Retries never replace independent review or Security Review,
waive an accepted criterion or required check, expand authority, cross a plan
fence or data-governance boundary, or change capability floors. Before
repeating a potentially destructive operation, establish the previous attempt's
effects. The correction-loop limit does not remove final Boundary B or any
other required check. A review finding is not an execution retry.

## Plans and records

Set a useful plan goal first, using the existing sections: Scope names the
specific result and why it matters to the accepted objective; Acceptance
criteria make delivery observable; Sequence shows available capabilities and
prerequisites and gives a realistic work-window estimate with uncertainty.
The estimate is not a deadline or permission to leave accepted work undone.
At plan opening, use authority and resources already available. Keep an outcome
that awaits an unavailable approval or passive calendar wait queued on the
existing board with its source, owner and concrete restart condition; open that
work when ready. A ready, approved scientific observation remains
implementation work even when it spans days, and its duration belongs in the
estimate; the unapproved future-usage Meter trial stays queued until its
approval is available. Missing required evidence still leaves the outcome
unverified; queueing does not waive checks or remove accepted scope.
One plan may include dependent internal chunks when they deliver one coherent
independently finishable outcome: its implementation, required reviews, checks
and archive do not wait on another unfinished plan. A proposal may retain
several outcomes across plans: name their
prerequisites and intended release or capability, and keep queued outcomes on
the existing board with their source and revival condition. Do not split work
by default or lose accepted scope.

At the commit or archive that finishes work, update applicable roadmap and
changelog records under their existing ownership and serialization rules. Do
not defer those entries to session end; the session-end routine checks for
omissions. Do not add entries for work the project's existing rules do not
record.


An implementation plan finishes after accepted agent-owned scope, required
reviews and applicable checks are complete, including change verification.
Do not make a routine human-run trust or release operation a completion
prerequisite or a final plan chunk. Track it in a separate named standalone
board wait with its owner and evidence; do not create a release plan. A reviewed
baseline awaiting a specifically named human operation remains unpassed. A
routine unavailable approval or passive calendar wait stays queued with its
source, owner and restart condition; an unexpected permission question still
requires the existing stop and decision. A defect, failed check, missing
functional or scientific evidence, or required
review remains implementation work. An unexplained integrity failure also
remains implementation work, not a human operation. Archive is
not permission to activate or release, and fixing an issue closes it at the
fixing commit, not at release.

## Working tree and commits

Edit functional prose (tracked text under the base-revision union of
content-scanner roots and `scripts/prose_roots.txt`) by exact replacement or
patch; never regenerate or rewrap it, list deliberate rule changes in commit
bodies, and include `scripts/prose_diff.py` output in trivial-lane commit
bodies, with any removed or changed rule making the edit non-trivial.

For each documentation change, judge agent-directed instructions and
procedures without a person-level decision in context. Preserve applicable
agent duties and route them to their installed authoritative home.

Search before building and reuse existing code. On a shared tree, coordinate
overlaps; claim exact files before editing if the project uses file claims.
Commit only explicit paths; never use a bare `git commit`. For
tracked files, `git commit <paths>` stages and commits atomically. For new
files, add and commit them in one invocation; if it fails, immediately unstage
those paths. Before inspecting paths, agree with other writers to serialize
them through the commit. Inspect your candidate against `HEAD`, including
staged and unstaged bytes; verify through `git status --short` and
`git diff <paths>`, never the shared cached index. Reinspect changed bytes and
stop if a candidate contains another writer's work. If writers cannot hold the
agreement, use a fresh worktree for checks that write or mutate files. A
reviewer in a shared tree writes only their own review record, claimed first if
the project uses file claims, and committed by explicit path; they use no
`restore`, `checkout`, `stash`, `reset`
or `clean` there.

Reviewers read a commit, never a shared working tree. All other writing checks
run on a separate copy of that commit; figures count only when measured on its
bytes. A claim that a value reaches every member of a set requires listing
the set from the tree and mutating each member in a separate copy. Keep
repeatable mutation checks in tests or scripts; summarize their outcome and any
unresolved or unmeasured mutations concisely. Equivalent means a behavior test
through the real entry point passes under mutation. Otherwise mutation is the reviewer's choice. A
noncooperating writer can defeat shared-file inspection; coordinate that risk.

A defect breaks a promise already in the file. Count person-steps, not machine
time. A cheap defect fix may restore only a promise already in an edited file, with
its test, and may add no other file, function, option or public name. It must
change no rule text, contract, high-risk/hash-pinned surface or fenced step.
Record `Defect fix: <promise> -> <file> -- test <path::node> -- changes no
rule text` in the commit body. A known cheap defect left open needs a plan
template deferral reason. An explicitly authorized Decision scribe quotes the
Maintainer verbatim in the Decision and commit body and commits nothing else.

Do not edit shared roadmap/changelog files except at their defined
serialization points. For commit bodies, target 15–30 lines with source
artifact, concise changed surfaces and concrete verification; keep them to 30
lines excluding verbatim Decision quotations.

## Verification

A scoped certification names the tested commit, components, checks, results
and omissions in the existing work record. It covers only those behaviors;
unrelated components, untested combined behavior and earlier changes are not
certified by that claim. Reopen the claim if a later failure contradicts it.
Required project checks and ceremonies remain owed; a whole suite runs when
an applicable requirement calls for it. The reviewer never runs the full suite.

Scientific model evidence belongs with the work or release that requires it;
scientific subject alone does not add a run to routine tree certification. A
configured suite member remains required at every required point, including a
scientific or slow run. Accepted criteria, safety and security checks, and
release requirements remain required too. Subject and duration do not waive a
run or authorize rescheduling it; that needs separate authority. Keep the
configured suite, its commands and its triggers unchanged.

Choose checks from the promises and boundaries the change affects. Use the
project's existing component owners and test homes: unit checks for local
behavior, contract checks for public interfaces and data formats, integration
checks for connected components, and a small workflow through the real entry
point. For simulations, keep real equations on small domains and use analytical
or convergence benchmarks when relevant; retain work-specific long runs where
the scientific question requires them. Runtime alone does not establish
coverage. Search changed behavior, callers, imports, configuration and data
readers, and public paths; map existing checks to affected components and
consumers in the implementation record. Add or extend a test only for a
plausible uncovered fault, and explain any uncertainty. Local effects default
to affected checks. Shared contracts, common infrastructure, language seams,
solver or physics behavior, and uncertain dependencies widen to owning test
families and relevant consumer or integration paths. If tangled dependencies
prevent a defensible selection, name the missing seam and the smallest useful
remedy; optional architecture review remains optional. Agents make this routine
mapping and reviewers challenge it; the Maintainer sets high-level project
needs and material exceptions, not per-change test selections.
Routine project operations use affected checks. At integration or release
boundaries, identify a representative cross-component workflow and applicable
safety, security, scientific, and release checks through existing project
commands. A whole suite is optional unless a project requirement makes it
mandatory.

Pinned prose is a substantive surface; unpinned prose uses prose gates.
Boundary B applies to every implementation, trivial changes included: run one
integration selection after code review when required, or after the final
implementation when no code review applies. Use a clean, unchanged final commit
under the configured interpreter/runtime. It consists of the iteration list
for every file in the reviewed range and integration/workflow tests in the tier
map that name those files. Record `bounded` or `wide`,
SHA/range, interpreter, clean pre/post state,
commands and counts, elapsed time, non-pass disposition and omissions.
Timing targets are 30 seconds for iteration, 10 seconds per test file, 3
minutes for integration, and 10 minutes for certification. They are
diagnostics, not agent scores; a miss does not block work. Record misses, and
put each test file over 10 seconds on the project's test-consolidation list,
slowest first.
Bounded covers affected behavior and consumers; wide covers owning test families,
known integration and public paths, and standing gates. Use `wide` for a contract
or trust-ceremony surface; trust ceremonies include named high-risk surfaces. Name
touched surfaces and test files or nodes in the record. A known unmet check keeps work
open; a future certification cannot close it. The author appends the record
under `## Implementation verification -- <agent> -- YYYY-MM-DD` in the plan,
or in the accepted proposal for light work with no plan. Code review reads the
iteration evidence and runs the tightest targeted checks that could falsify the
change; it never runs a suite. It names a missing test when coverage is absent.
A review fix that changes more than a failing test returns to the same reviewer
for a targeted look before the final integration run. See the plan template
for full Boundary A/B/C rules.

Boundary A is scoped iteration; Boundary B mode is `bounded | wide`; Boundary C
is independent falsification. Its `Bounding` verdict is `WIDER RUN REQUIRED`
when mapped checks are insufficient. An already-open plan may switch to this
contract by one line in its record. The final integration run follows review,
so review fixes are included. Change verification and tree
certification are separate. Release verification is a separate strict ceremony.

Prose-only work runs the relevant claim, link, snippet and neutrality gates,
plus tests that actually read the changed file. Search for readers and byte
pins; do not assume either is absent. Do not run the suite unless prose bytes
are pinned. Name the interpreter with every suite figure.

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

At goodnight, leave a committed handoff and reflection and a next-session note,
never committed; the note is refused if its path, `dev/reflections` or `dev` is a link.
Goodnight does not authorize a push.
The full-handoff owner runs the configured fast/default smoke selection, if
present, and records its command, result and coverage limits. An absent
selection is unavailable, not passed; a failed command is failed. Reflection-only
participants gain no test obligation. Slow tests remain due at release and when
an accepted plan, safety or security requirement, or the Maintainer requires
them. Change checks and Boundary B remain due on their existing schedule; the
smoke does not replace them or any required certification.

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
