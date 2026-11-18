External-repo paths: `docs/methodology/dual-review.md`, `docs/methodology/rationale.md`
# Agent collaboration — {{project_name}}
Written in [Cairn Plain Language 1.1](agent_collaboration.md).

> The marked slots below are yours to fill. An unfilled one is a review
> finding, not a default.

## Team roles

Roles are **frames, not people**. Any capable agent fills any of them except the first.

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
* **User Agent** — exercises Cairn from an adopter's position, reproduces and
  diagnoses failures from real use, and captures friction with its root cause.
* **Operator** (optional) — runs the project's software under its run rules,
  may reproduce and diagnose defects, and files them in its tracker. For either
  role, if the tracker is unavailable, record reproduction, context and labels for
  later filing or the Maintainer. Both roles use the defect-fix rule in
  `dev/agent_collaboration.md` > "Working tree and commits"; an Operator
  switches to Implementation before a fix.

A fresh session is every review's floor, and no review requires a different
agent type. How far a reviewer stood from the author is read from its
attribution, and the Maintainer may ask for more distance (`AGENTS.md` >
"Review").

<!-- cairn:slot role-roster-additions -->
(Dimension-selected roles — an Operator, a User Agent, a Security reviewer,
domain-specialized agents, a Legacy Agent — are added here when
the project's profile selects them. A minimal team runs the
maintainer plus one generalist agent and adds none.)
<!-- cairn:end role-roster-additions -->


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
the burden of making a change followable sits with its author.

## The review loop

When a documentation change receives ordinary review, check the author’s
audience judgment: assess agent-directed instructions and procedures without
a person-level decision in context, and whether applicable duties remain in
their installed authoritative homes. This adds no review to unreviewed work.

A review is a **dated, attributed section appended to the artifact and
committed**. **No agent writes or commits a review attributed to another
agent** — the named reviewer commits their own findings, or the Maintainer
does.

**Lead with the steelman.** State the strongest version of what the artifact is
trying to do before saying what is wrong with it.

Before body or code read the proposal's title, one-line summary and Decision summary; state the gist in one or two sentences. If the top needs the body for understanding, make a finding. After every revision the author rereads and revises the top as a whole when needed.

A finding is **blocking** or **non-blocking**, and says what evidence would
close it. Blocking means hard-to-undo damage or an unmet accepted criterion or
required check. Authors dispose of non-cheap advice in one line each; this does
not waive a criterion or check. A review targets 300 words of reviewer-written
text, excluding template skeleton lines, and preserves its verdict, findings
and coverage gap. A pass over the target explains why in its coverage line.
"This is too large" is not a finding.

A reviewer may name a simpler adequate alternative with lower total build, run, understanding and maintenance cost. The author decides; no per-addition accounting or global optimum proof is required.


## The review sweep

A review that finds nothing on a *complex* change is treated with skepticism,
not relief. Read as if a hidden bug exists, and probe for it. The nine lenses are
a **fixed, change-agnostic reading aid**, not a required checklist or reporting
format. Use them to broaden judgment and probe for hidden failures; cite the
evidence supporting the three answers and name uncovered areas without
reporting every lens. The nine:

1. **Claims** — Check load-bearing claims against the current tree with committed evidence or adequate reasoning; cite evidence and limits. Forward behavior needs executable evidence; inventory and check every applicable member for a set-wide claim.
2. **Production path** — Test the failing path through the public entry point, not a helper or stub.
3. **Design completeness** — State preconditions, invariants, edge cases and failure modes.
4. **Fail-closed** — Guards fail loudly, not by degrading or returning empty, across configurations and stages; make fail-open paths intentional.
5. **Consistency** — Check docs, roadmap, code, tests and doctrine for stale references and reusable tools. Repeat the plan's reuse search and one of your own, testing each against a known positive; an accidental near-copy is a finding satisfied by reuse or generalization.
6. **Drift** — Match docs, examples, changelog and commit claims to shipped behavior.
7. **Placement** — For process changes, identify who acts, when, and in which ceremony or serialization point.
8. **Scientific validity and scope** — Ground and document methods, prevent quiet scope expansion, and justify new abstractions.
9. **Satisfier** — Every finding names a closing test, guard, doc, scope-cut or explicit `wontfix`; without one it is an observation. At archive, test or guard maps to `guard`, doc or scope-cut to `accept`, and wontfix to `wontfix`. Other real work is `defer`, the Maintainer's call. A scope-cut corrects a claim; only the Maintainer may concede removal of accepted work.

Unreviewed trivial changes owe no review record.



Cite a file, test, line or command; report coverage, low confidence, risks and gaps, not a recommendation for more review. The Maintainer may ask any reader.

The reading aid does not change or downgrade a declared `required` review
tier. Projects may add probes for their domain and high-risk surfaces, such as
units, coordinate systems, numerical edges and resource limits.

**Code review tries to falsify the change.** A clean pass gives concise,
evidence-backed results and names what remains uncertain. Mutation
is optional unless a specific requirement calls for it. Keep existing negative
controls; a new security check needs a demonstrated failing case. Preserve
every applicable security check and review. For scientific work that touches
an assumption or a published or acted-on result, retain the independent error
check and positive control even when the intended result is unchanged.




An honest, evidence-backed failure to falsify clears the review; unsupported assertion does not. **The scope-reduction trap.** Scrutinize narrowing as carefully as a clean pass. Reviewers state what is lost and why the narrower change reaches the cause. An author removing underspecified work says why specification was rejected. Compare outcomes with the artifact as opened before Decision and as accepted afterward, never a later summary. A lighter mechanism delivering every outcome is no reduction. Lost outcomes require a `**Scope delta**`, one grouped scope-remainder record per source artifact, and the Maintainer's explicit allowance. Declining an outcome proposed only during review is not a reduction.

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

## Offering optional modules

When an upgrade plan lists unselected modules, read the list, this project's
installed module inventory and module descriptions in the exact Cairn source used
for that upgrade. Explain each available module's purpose and concrete known
costs; say when a cost is unknown. Ask the Maintainer which, if any, to adopt.
Explain separately that apply adds new unconditional core and skills files and
that additions to already selected modules follow their selection.

Between upgrades, when a task reveals a concrete need, consult the installed
inventory and onboarding guidance. The inventory describes selected modules
only: check an accessible, verified Cairn source or reference, such as its
`install/BOOTSTRAP.md` and relevant `templates/modules/` guidance, for a
suitable unselected module. If a usable description is unavailable, say so and
defer the offer until one is available; do not invent a purpose or cost. Ask
before adoption, even if the task suggests a need. Do not repeat an offer
refused in the same conversation.

A yes for a named module permits the existing `upgrade --adopt-module <name>`
for that module, subject to its safety, collision and provenance checks. A no
leaves it unselected. Neither an offer nor an upgrade grants credential access
or resets prior consent. The separate rules-folder offer retains its existing
threshold, answer record and approval for changes to project rules.

## Outward reports

When a task finds a Cairn or dependency problem, draft it in `dev/upstream/`.
The folder README routes each channel to its template and publication protocol.
Check and reread the full public material, then obtain explicit approval of the
actual report and destination for each filing. The Human Maintainer submits
Cairn pull requests by hand; an agent may file an individually approved Cairn
issue. Separate channels require separate drafts and approvals.

## Surfacing judgment calls to the Maintainer

Acceptance, rejection, and supersession are the Maintainer's call. An agent
unsure whether something is a decision surfaces it rather than assuming.

Most calls are the agent's to make. Escalate when the answer would change what
gets built and cannot be resolved from the artifact, the code, or a sensible
default — and when you do, bring a **recommendation, not a survey**. State the
question in plain language, give the option you would take and why, and say
what it costs to be wrong.


**After a review stalls, the author decides and defends.** Two passes that
disagree do not escalate by themselves; the author resolves them in the record
and the Maintainer reads the resolution.

When asking the Maintainer to choose, show each material option's changes and build, run, understanding and maintenance costs, with estimates or uncertainty. Include the least involved credible option, including doing nothing when viable, and losses including safeguards. Separate recommendation and reason from options. Waive no required check, accepted scope or model floor. Name changed or added material human operations, estimated counts (zero when informative), and recurring additions; omit routine agent work. The Decision names material new recurring additions; none needs no extra sentence or inventory.

## Review rules

A fresh reviewer, not the author, reads a committed version. One review stance applies at every stage; the stage sets the questions. Answer three: should this happen as framed, what is the best alternative, and what would show it wrong? Each answer states its point in a sentence, then gives its evidence. Name what the pass did not cover. Question 3 names a forward test even when there are no findings. There is no finding quota.  Recommend improvements; the author decides.  A further Security Review pass names the unresolved question or newly changed material, why earlier passes and evidence cannot resolve it, its expected value, and the artifact and scope. Clean work and closed findings advance without a clearing review.

For each proposed new refusal in the upgrade path, identify the attacker, the input they control, the harmful action, how it connects to the existing threat model, and evidence or a test that distinguishes the threat. If it falls outside that model, name the residual risk and get the Maintainer's explicit disposition. An unexplained threat or unmet protection stays open. Keep existing refusals and checks; this rule does not authorize removing or weakening them.

Plan review checks that each chunk is specified well enough for its assigned model tier, with no design left to the implementer. Name missing design in the three answers and return the chunk to its author; do not swap in a stronger implementer.

A follow-up is cheap if it takes a few person-steps, adds no Decision or public name beyond the plan, and needs only a test in an existing test file. Code review names cheap findings and advice; before archive the response fixes each, or defers it with the Maintainer's verbatim authorization. Cheapness waives no scope, boundary or check. Failed required checks stay implementation work. This is not the narrower cheap defect fix in "Working tree and commits".

Only the Maintainer calls an External read on one existing artifact; a standing call needs a proposal. A roster adds or upgrades no read. The reviewer answers three questions and states distance. Record the Maintainer's verbatim words set apart and commit them with their source: `Called by: Maintainer -- Decision at <commit>` or `-- chat, <date>`, adding `, relayed by <who>` where relayed. Without that line the pass is ordinary; `**Tier**: External` needs it. The call adds focus, replaces no review or owed answer, clears Security Review only as one, and grants no Decision or fence authority. Waivers or scope changes take effect only in a Decision or plan fence. Agents never request or declare one, say a change needs one, recommend more distance, head a pass External or start one without the Maintainer's words; they may name risk and gaps. The next reviewer and Maintainer, not a tool, check the quote. High-risk work retains separate ordinary and Security passes; Internal cannot clear Security. A plan's Internal Security Review needs the matching `Obligation` line. Plan review is fresh-context; code review is by another agent, never reopens the Decision or reruns implementation checks. Detail: Cairn's published dual-review procedure.

The proposal Decision sets the tier: `light` (one short review, no plan), `standard` (one pass per stage) or `heavy` (adds Security Review). Light is the default. A higher tier proposed by the author stands unless the Decision changes it. A change gets the heavy tier when it alters what a high-risk surface does or accepts, or adds a place where outside input meets the system; merely touching a surface does not. When in doubt, take the Security Review. A project rule that names its own Security Review still applies. A newly found boundary stops work for reassessment. Ordinary uncertainty elsewhere takes the lighter lane, with the reason. Detail: Cairn's published lifecycle method.

**Lowering a tier.** Only the Maintainer lowers a tier, in chat or a Decision; an author or reviewer may recommend it. The plan records it in one appended `Plan change`: the Maintainer's words verbatim with their source, the cancelled chunks, the obligations that lapse (those whose only source was a cancelled chunk, such as a Security Review of code no longer written) and those that remain (fences, Maintainer-reserved steps, model floors, anything tied to a remaining chunk), the new header values, and that the remaining scope does not alter a high-risk surface or widen a boundary. A review already held stays valid for the scope it covered and transfers to nothing else. A raise follows the same pattern. The amendment review checks the lapse list against the cancelled chunks.

## Agent execution retries

**Execution retries.** For a correctable error in work at or above its capability floor, allow up to two same-tier retries. Each retry uses concrete failure feedback, keeps the earlier failure evidence, and reruns only the affected check. After two failed retries, re-run once one tier up. Escalate at once if the failure shows the task exceeds the assigned tier; work below its floor is not eligible. Retries never replace independent review or Security Review, waive a criterion or required check, expand authority, or cross a plan fence or data-governance boundary. Before repeating a potentially destructive operation, establish what the earlier attempt did. The retry limit removes no required check, including joined Boundary B when due under the arc's schedule. A review finding is not a retry.

## Plans and records

Set a useful goal, scope and observable criteria; estimate the work window and uncertainty, not a deadline or waiver. Open only outcomes with authority and resources; queue unavailable approval or passive calendar waits with source, owner and restart condition. Approved scientific observation remains implementation across days; missing evidence stays unverified. A plan may group dependent chunks that deliver one independently finishable outcome; the coordinator decides connected-arc grouping. A commit, work item or contract label alone never forces another artifact. Shared reviews name changes and cover every obligation; grouping waives no Decisions, fences, scope, checks, floors or trust and release operations. Uncovered promises, new boundaries, failed checks and changed scope follow existing stop rules. Name each outcome's prerequisites and release; queue the rest without losing accepted scope. A shipped capability may be a prerequisite; another plan's future review, archive or release may not be required to finish this plan.

When work finishes, update the roadmap and changelog records the project's rules require, at the commit or archive that finishes it. Do not defer them to session end, which only checks for omissions. Add no entry the project's rules do not record.


A plan's four operative cells — Scope, Sequence, Acceptance criteria and
Verification — remain editable throughout active work. Reviews, responses,
amendment reviews and Decisions append and are never edited. During
implementation, a substantive cell change stops affected and dependent work,
returns the plan to `revising-plan`, and requires fresh non-author review for
each exact obligation plus author disposition before `ready-to-implement` and
resumption. Wording or status changes that alter no obligation need no review;
missing design returns to the operative cells.



A plan is finished when accepted agent-owned scope, required reviews and applicable checks (change verification included) are complete. A routine human-run trust or release operation is not a completion prerequisite or a final chunk: track it as a separate named board wait with its owner, evidence and a link to the implementation, and create no release plan; keep its result unpassed until its evidence exists. A reviewed baseline awaiting a named human operation stays unpassed. An unexpected permission question still needs the existing stop and decision. A defect, failed check, missing evidence, required review or unexplained integrity failure stays implementation work. Archive is not permission to activate or release; fixing an issue closes it at the fixing commit, not at release.

## Working tree and commits

Edit functional prose (tracked text under the base-revision union of
content-scanner roots and `dev/tools/prose_roots.txt`) by exact replacement or
patch (`dev/tools/exact_replace.py` makes the exact replacement); never regenerate or rewrap it, list deliberate rule changes in commit
bodies, and include `dev/tools/prose_diff.py` output in trivial-lane commit
bodies, with any removed or changed rule making the edit non-trivial.

For each documentation change, judge agent-directed instructions and
procedures without a person-level decision in context. Preserve applicable
agent duties and route them to their installed authoritative home.

Search and reuse before building. Coordinate shared-tree overlaps and claim exact files before editing where claims are used. Commit explicit paths, never bare `git commit`; add and commit a new file in one invocation, unstaging it if that fails. Serialize commits with other writers. Inspect staged and unstaged candidate changes against `HEAD` with `git status --short` and `git diff <paths>`, never the shared cached index; stop if another writer's work appears. Without that agreement use a fresh worktree for writing checks. A shared-tree reviewer claims, writes and commits only their own review by explicit path; no `restore`, `checkout`, `stash`, `reset` or `clean` there.

Reviewers read a commit, never a shared working tree. Run other writing checks on a separate copy of that commit, and count a figure only if measured on its bytes. A noncooperating writer can defeat shared-file inspection; coordinate that risk.

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

A scoped certification names the tested commit, the components, checks, results and omissions in the work record. It covers only those behaviors; reopen it if a later failure contradicts it. A whole suite runs only when a project requirement calls for it, and a reviewer never runs one.

Scientific model evidence belongs with the work or release that requires it; scientific subject alone adds no run to routine checks. A configured suite member stays required wherever it is required, including slow or scientific runs. Subject and duration waive no run and authorize no rescheduling.

Apply the **Pareto testing principle**: aim for 80% fault coverage in 20% of runtime and maintenance. Permanent tests guard external promises through public entries: primary workflows, scientific or data invariants, and one parameterized check per security or refusal class. Run developmental tests during coding and delete them before archive. Do not keep private-helper tests, change-specific pins or wording tests; do not add separate input variations on the same code branch. Pruning non-promise, private-helper or over-budget tests needs no per-member mutation proof unless specifically required. Simulations use real equations on small domains and analytical or convergence benchmarks. Local effects use affected checks; shared contracts, common infrastructure, language seams, solver behavior and uncertain dependencies widen to owning families and consumers. Agents select routinely, reviewers challenge, and the Maintainer sets high-level needs and material exceptions.

Plans finish as in “Plans and records”; they do not wait for later integration. The arc owner runs one joined integration selection under the canonical runtime after connected plans finish, or earlier at a critical shared boundary. Before arc completion or release, record final combined coverage, evidence producers and consumers, results and omissions. Reuse applicable results only for unchanged behavior and inputs; after corrections rerun affected interactions. The arc owner records and repairs post-archive defects without reopening the plan. Missing evidence, failed promises and required checks remain plan work. Routine human trust and release operations remain separate. Cover the clean final combined revision; do not replay the whole selection solely to stamp a new commit ID.

Boundary A is scoped iteration. Boundary C is independent falsification; its `Bounding` verdict is `WIDER RUN REQUIRED` when mapped checks are insufficient. A review fix larger than a failing test returns to the reviewer for a targeted look before Boundary B. Change verification, tree certification and release verification are separate.


Implementation verification closes with `**Benefit versus cost**: <verdict>
-- <benefit>; cost <measured>; remaining burden <measured>`. Use `worth it`,
`partly`, `not worth it`, or `unknown`, and include a revisit condition. Use
the implementation-to-tested range for Git counts and net burden; distinguish
aggregate agent elapsed from wall time and use existing records for available
decision counts, shipped/always-loaded word changes, test count/runtime and
installed-file deltas. Missing evidence is `unknown`.

Pinned prose is a substantive surface; unpinned prose uses prose gates. Prose-only work runs the claim, link, snippet and neutrality gates plus tests that read the changed file. Search for readers and byte pins; do not assume either is absent. Do not run the suite unless prose bytes are pinned. Name the interpreter with every suite figure.

## Coordination


The coordination space is the **`dev/` tree — git-committed files**.

**Durable state lives in the repo, never in a harness's memory.**
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

At goodnight commit a handoff and reflection, and leave an uncommitted next-session note; refuse it if its path, `dev/reflections` or `dev` is a link. Goodnight never authorizes a push. The full-handoff owner runs configured fast smoke if present, recording command, result and coverage limits; absence is unavailable, not passed, and failure is failed. Reflection-only participants owe no test. Slow tests remain due at release and when an accepted plan, safety/security requirement or Maintainer requires them. Change checks and joined Boundary B remain due on their schedules; smoke replaces neither them nor required certification.

Reflections are **per-agent and ephemeral** — they are pruned. Anything durable
migrates out to doctrine or the roadmap before then.

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
