# Cairn and assai: a development methodology and a persistent research ecosystem

**Author**: Codex (Strategy), synthesizing work by Anthony Kendall, Claude, and Gemini/Antigravity
**Model**: Codex; exact model identifier not exposed in this session
**Date**: 2026-10-19
**Status**: revised
**Type**: design-exploration
**Surfaces this would feed**: the proposed MSUHydrogeology/assai runtime and its development plan; the local research-ecosystem concept and display plan; LHM's agent-run contract; later Cairn fold-back where actual use reveals a methodology-general lesson

## The question / felt gap

Can a small community of persistent AI research labs explore scientific questions
that Anthony does not have the human capacity to pursue, and return promising,
partially tested leads worth further effort?

The ambition is not a machine that certifies its own discoveries or a substitute
for a human research group. It is affordable exploration with a durable
scientific record: questions, experiments, papers, criticisms, failures, and
expertise that survive individual agent sessions. The scientific aim is
understanding physical mechanisms, not
merely improving a statistical fit. Useful patterns can start an investigation;
they do not finish the explanation.

The architectural answer is two connected projects, not two profiles of one
template system:

* **Cairn remains the methodology for developing research software.** It governs
  changes to assai itself and to the models and trusted tools assai uses.
* **assai is the research runtime.** It coordinates persistent, end-to-end labs,
  a journal, independent re-execution, and a shared record within a human-approved
  scope and resource budget.

The connection is shared discipline and an explicit handoff, not a requirement
that papers follow the software proposal lifecycle. No Cairn rename, shared-core
extraction, or profile mechanism is needed to start.

This is a strategy recommendation, not an implementation authorization or a
scribed Maintainer Decision. Runtime behavior below is proposed, not a claim
that the software or its protections already exist.

## Grounding and limits

This design draws on Cairn's operational reference and development templates
(`AGENTS.md`, `templates/core/AGENTS.md`, and the proposal and plan templates),
its session and review disciplines, and its documentation placement rules.
Cairn already has a home for developing the runtime; that does not establish
that its software-change state machine is suitable for experiments.

The research requirements come from the operative toy-build table in Anthony's
local *Cairn Lab - Concept and Scope.md* and the accompanying *Cairn Lab - Nov 2
Plan.md*, read on 2026-10-19. Those documents remain context outside this
repository. Their repository names, profile assumptions, and display labels
need reconciliation before they are used as build instructions; this rewrite
does not edit them.

The notebook recommendation also draws on upstream [crux](https://github.com/mehdiforoozandeh/crux).
Gemini/Antigravity's source inspection, recorded in commit `fce8e653`, reports
pre-registration locks, typed controls, verdict rules, and approval transitions
in engine version 3.5. That is a useful basis for integration, not a pinned
dependency or a completed execution test. The exact upstream commit, license,
and behavior must be checked when selecting the dependency. The engine-level
details are attributed to that inspection, not independently verified here;
no upstream test suite or assai runtime was run.

The immediate question is whether the loop operates and produces something
Anthony values. Twenty to thirty cycles cannot, by themselves, establish that
the ecosystem accumulates reliable scientific knowledge.

## Architecture: three homes, two kinds of work

| Home | Responsibility | What does not belong here |
| --- | --- | --- |
| **Cairn** | Methodology for developing and reviewing software; ordinary development support for assai, LHM, and other model repositories | A nightly scientific scheduler, paper lifecycle, or domain-specific research protocol |
| **assai** (proposed repository: MSUHydrogeology/assai) | Controller, lab and journal roles, notebook integration, paper and claim records, reproduction service, queries, and display feeds | Embedded assumptions about a particular basin, gauge, or physical model |
| **Configured ecosystem** (initially a folder inside assai) | Research agenda, lab histories and scopes, model harnesses, scenarios, reference data definitions, and approved instrument versions | Authority to change the runtime's protections or adopt its own trusted instruments |

An ecosystem is an instance of the runtime, not another methodology. The first
instance is the Cedar Creek hydrology toy. Keep its domain-specific choices in
its configuration and harness, while avoiding a general plugin framework built
for imagined future users. A second domain would test portability; it is not a
prerequisite for Anthony's use.

Two protocols coexist:

**Developing the instruments.** A change to controller enforcement, permissions,
evaluation rules, a trusted adapter, or model code follows the owning project's
Cairn process. An experiment may expose the need for such a change, but cannot
quietly authorize it.

**Using the instruments.** A lab investigates questions within its approved scope,
using approved instruments and its allocated resources. It writes papers, not
a software proposal for every run. Journal acceptance is an editorial action
inside this research protocol, not a Cairn Maintainer Decision.

Developing assai does not automatically make every nightly lab a software
contributor. An experimental script can be part of a submitted paper without
becoming a trusted controller component.

## What continues: labs, papers, and expertise

The **lab is the continuing entity**; a session is an episode in its work.
Persistence is required even in the toy. A fresh session must recover:

* the questions it is pursuing and the competing explanations;
* why its next test was chosen and what would distinguish the explanations;
* failed approaches, criticism, abandoned leads, and reasons conclusions changed;
* tested procedures, diagnostic cases, and known limits of its tools;
* unfinished work and the evidence supporting its present account.

Compact working summaries help with limited context, but are never the only
copy. The underlying notebooks, papers, run records, and reviews remain
inspectable. Model replacement or a mistaken summary must not erase a lab's
history.

Labs own investigations end to end: question, data examination, explanation,
experiment, interpretation, and paper. Process and Observation are initial
centers of expertise, not exclusive pipeline roles. Either lab may combine
methods or follow a surprise outside its initial emphasis, within its scope.

Expertise should develop through different investigative histories, not just
different role prompts. Later conferences can exchange demonstrated procedures,
failures, objections, and proposed joint tests. They are not an additional
approval gate. Shared methods and inputs are recorded so agreement after an
exchange is not mistaken for independent corroboration.

**Papers are the foundational scientific record.** A short internal paper carries
its question, contribution, method, executable evidence, claims, limitations,
and next proposed test. Negative results, reproductions, and justified decisions
not to pursue a lead are legitimate contributions. A lead brief or display card
is a derived view of that record, not its replacement.

A paper distinguishes what it contributes:

1. A pattern needing explanation.
2. A mechanism capable of producing that pattern in a model.
3. Evidence that favors that mechanism over plausible alternatives in the world.

The second does not establish the third. Better fit alone does not establish
either a unique mechanism or a causal explanation.

## Notebook: reuse crux, keep authority in assai

Use a pinned crux engine as the preferred starting point for the labs' durable
notebooks, rather than rebuilding its question tree and experiment bookkeeping.
The reported engine features address real needs: pre-run commitments, separation
of hypothesis checks from apparatus controls, explicit alternatives, repeat-attempt
history, and bounded context for resuming work.

This is a recommendation to reuse an existing component, not to treat its agent
instructions as assai's operating policy. Start with a thin integration. Record
the upstream revision, license obligations, local changes, and a way to export
questions, evidence links, and histories if the dependency is later replaced.
Carry a maintained fork only where actual integration requires patches; do not
reimplement its cockpit or task system merely for completeness.

The important adaptation is **who may approve what**:

| Actor | Proposed authority |
| --- | --- |
| Lab | Develop questions and hypotheses; propose checks; run in-scope experiments through the controller; record results; submit papers and syntheses |
| Journal / pre-run critic | Challenge an experiment's stated alternative, controls, and discriminating test; authorize the corresponding pre-run transition |
| Replicator | Re-execute submitted bundles and report agreement or discrepancy; no authority to certify the scientific explanation |
| Journal / post-run reviewer | Assess methods, argument, limitations, and reproduction evidence; accept, request revision, challenge, or withdraw papers with a recorded basis |
| Controller | Enforce permissions and budgets; record commitments and actual runs; execute authorized state changes; expose no authority merely because an agent requested it |
| Anthony | Set scope and resources; approve trusted instrument and reference-set changes; decide consequential escalations and which leads merit human effort |

The journal's reviewer must not be the session that wrote the paper. Give it
fresh context and the evidence bundle, not the lab's private reasoning as a
substitute for evidence. Different agent types may offer different failure
modes, but neither role separation nor vendor diversity establishes that the
scientific conclusion is independent of shared data and assumptions.

Bind crux approval actions such as `approve-null`, `task accept`, `approve`,
and `answer` to these roles through the integration. A journal may close a
scoped notebook question without declaring it scientifically settled; a change
to the ecosystem's agenda or authority still belongs to Anthony. The detailed
command mapping must be checked against the selected upstream revision,
including how authorized execution reaches `test`.

Pre-run review is automated and bounded, not a hidden nightly request for
Anthony's signature. Its purpose is to improve the test, not to take ownership
of the investigation away from the lab. Exploratory analysis is allowed and
labeled as such; a claim presented as a pre-specified test must have its
commitment captured before the relevant result is available.

A hash stored in an editable notebook is not, by itself, a protected commitment.
Before executing a registered test, the controller must preserve the test
definition and its digest outside the lab's write authority and bind them to
the run record. Later amendments start a new recorded attempt; they do not
rewrite what the original run tested.

Likewise, hiding approval commands in a prompt is not access control. The
integration must address direct file edits and alternative execution paths,
not just the normal command interface. Lab workspaces, approval state, and
controller-owned records need a real separation of write authority.

An automatic verdict means that recorded check outcomes satisfy a stated rule.
It does not establish that the checks measure the right thing, were evaluated
honestly, or distinguish the scientific alternatives. Those remain review and
evidence questions.

## The research loop and the meaning of acceptance

A normal cycle is:

1. A lab reads its own history and relevant shared results, chooses a question,
   and records the closest literature and competing explanations.
2. It proposes a test with declared checks, controls, and a discriminating result.
   The journal's pre-run check challenges that design.
3. The controller captures the commitment, launches within the approved budget,
   and records inputs, versions, execution outcomes, and artifacts.
4. The lab interprets the result and submits a paper, including failures and
   unexpected outcomes rather than silently replacing the planned analysis.
5. The replicator re-executes the submitted bundle. The journal separately
   challenges the scientific argument and decides its editorial disposition.
6. The shared record and affected lab summaries are updated. Labs can build on
   accepted work, with its limitations and assumptions visible.

Three checks must not be collapsed into one:

* **Reproduction:** does the submitted procedure regenerate the paper's own
  outputs within declared tolerances?
* **Baseline regression:** does the approved instrument still satisfy its
  separately frozen baseline checks?
* **Scientific challenge:** could the result arise for another reason, from
  broken measurement, shared assumptions, or an analysis incapable of
  distinguishing the proposed mechanisms?

A perfectly reproducible wrong analysis is a required test case for the journal.
Re-execution is necessary evidence about a paper, not independent falsification
of its scientific interpretation.

A null result needs a positive control that demonstrates sensitivity at the
relevant effect size, not merely the presence of a control checkbox. If the
apparatus fails that control, record an invalid run rather than evidence
against the hypothesis.

Journal acceptance admits a contribution to the working record. It is neither
a guarantee of truth nor a promotion of the code used in the paper into a trusted
instrument. Conversely, a paper need not demonstrate a new physical mechanism
to be useful: a well-supported discrepancy or null result may identify the next
worthwhile question.

## Claims, dependencies, and correction

Keep claims linked to papers, run evidence, and reviews. The initial vocabulary
is exploratory, reproduced, challenged, and independently supported. These are
descriptions of outcome and evidence basis, not rungs on a confidence ladder.
A challenge may undermine a claim; repetition by another agent may share all
the original assumptions.

Distinguish a result that **requires** a prior claim from one merely
**motivated by** it. Required but unverified claims remain explicit assumptions.
Record shared datasets, forcing, calibration targets, tools, and methodological
lineage when judging whether support is independent. A different persona or
vendor does not establish evidential independence.

The dependency graph can propagate notices and reconsideration requirements.
It cannot mechanically calculate scientific confidence. When a required claim
is withdrawn or materially undermined, the controller flags affected descendants;
the journal determines which still stand, which need new analysis, and which
must be withdrawn. Prior papers and reviews remain in the record with their
changed standing visible. Regenerate working summaries so a corrected record
does not coexist indefinitely with a lab's obsolete beliefs.

Unaudited reuse does not become human-validated evidence. A reproduced result
may still depend on exploratory assumptions; exported summaries and displays
must show that basis rather than silently upgrading it.

## Human attention and protected boundaries

Anthony steers the scientific scope and chooses where human effort is spent.
The journal handles routine editorial decisions without waiting for him.
Human involvement concentrates on:

* approving changes to trusted instruments, reference sets, permissions, or scope;
* sampled audits and consequential or high-fan-out claims;
* deciding which promising leads warrant deeper investigation or software work.

Audits can expose errors or provide specified corroboration. An audit pass does
not certify an entire dependent claim chain as true.

The controller's logic should be inspectable. Its live authority must be outside
lab write access: budgets, execution policy, credentials, approval records, and
run certificates. Held-out observations and planted-error answers must also be
outside unauthorized agent read access. Sandboxes, read-only inputs, bounded
process lifetimes, and recorded tool access implement these protections; prose
alone does not.

Repeated held-out scores are development feedback even when agents never see
the underlying observations. Reserve any genuinely untouched final check for
a frozen candidate, record previous exposure, and do not reuse it as an
independent confirmation after tuning against it. The toy need not claim
independent confirmation at all.

Start with the concept document's attention budget: two randomly selected claims
per week, plus consequential or high-fan-out reuse, with audit and decision time
recorded separately. If work exceeds six hours in each of two consecutive weeks,
pause nightly cycles and fix the cause rather than making the human budget grow
automatically with output.

## The first ecosystem and the software handoff

Begin locally with the Cedar Creek model and its approved observational reference
set. The first question compares historical with fixed-1900 land use as a
**scenario sensitivity** experiment, not as an attribution of historical change.
The harness owns model-specific units, scenarios, data provenance, metrics,
and baseline expectations; assai owns scheduling and records.

Build the first complete path with one persistent lab, a journal, and a replicator.
Add the second end-to-end lab once that path is stable. The intended toy has two
labs, but falling back to one persistent analyst preserves the core experiment
if coordination costs exceed its value. No HPC or expansion into more domains
is needed to test the loop.

A paper diagnosing a model defect or suggesting a missing process crosses into
the owning software repository as evidence for a Cairn proposal. Anthony decides
whether it merits that investment. The software change then undergoes the
project's ordinary development and review; journal acceptance is not its approval.
Once a new trusted model version is approved for the ecosystem, record the
adoption and retain the earlier version so prior work remains interpretable.

This is a useful connection without renaming Cairn to Cairn Develop. Display
labels can explain development and research side by side without imposing a
shared template architecture.

## Sequence and evidence before unattended use

First reconcile the concept and display documents with this architecture. Keep
Cairn itself unchanged for the purpose of this project; create no profile or
scaffold work merely to support the research loop.

Then develop assai as an ordinary Cairn adopter. Select the upstream notebook
revision and establish its role mapping, durable record, minimal controller,
and first harness. Before scheduling unattended cycles, demonstrate:

* One question → registered test → execution → paper → reproduction → scientific
  review → next question path, without an unplanned human approval stop.
* Fresh-session recovery after interruption, including failed approaches, the
  reason for the next test, and supporting artifacts; repeat after a retraction.
* Refusal of unauthorized data reads, control edits, forged approvals, and edits
  to the protected pre-run commitment, including attempts outside the normal CLI.
* Termination at the resource limit, with a durable failure record.
* A known-answer case, a null case with an appropriate positive control, a
  reproducible but scientifically wrong analysis, and a known-sound submission.
  A journal that rejects everything must fail this exercise.
* Distinct reproduction and baseline checks: replay agreeing with the submitted
  result passes reproduction; disagreement outside tolerance fails it, regardless
  of whether either output is close to the baseline.
* Retraction reaching required descendants and refreshed working summaries,
  without treating a merely motivating citation as an invalidating dependency.

These are proposed implementation acceptance examples, not completed checks.
Implementation tests and manual integration runs must invoke them; the operator
enables the nightly schedule only after inspecting that recorded evidence. This
note supplies no automatic scheduler gate.

Run several manual cycles before the nightly pilot. Across twenty to thirty
cycles, record attention, failures, recovery, useful outputs, missed planted
errors, and false alarms on sound controls. Citation depth and paper counts are
activity measures, not evidence that knowledge is improving.

The pilot asks three separate questions:

1. **Does it operate?** The loop completes and resumes within resource and
   attention limits.
2. **Is it useful?** Anthony values at least one resulting analysis, diagnostic,
   procedure, or question enough to use or investigate.
3. **Does knowledge improve?** Later work benefits from earlier work in ways
   supported beyond internal agreement and self-citation.

The first two can justify continuing the toy. The third requires stronger,
longer-term evidence and must not be inferred from a running display.

## Alternatives and reasons to change course

**Do not build the ecosystem.** Continue ordinary agent-assisted research and
Cairn software development. This avoids runtime maintenance but leaves the
persistent exploration hypothesis untested. It remains a reasonable outcome if
the toy consumes more attention than it returns.

**Use one persistent analyst.** Keep the notebook, papers, controls, and scientific
review while dropping multi-lab interaction. This loses the chance to develop
distinct expertise through parallel histories; it does not concede continuity
or scientific discipline. Prefer it if the labs repeatedly duplicate each other
or their coordination provides no useful disagreement.

**Write a small notebook layer instead of integrating crux.** Retain this exit
if a pinned engine requires invasive patches, cannot preserve the required lab
history, or makes the delegated approval path unworkable. Judge the actual
integration against the state handling it avoids, not matching terminology.
Do not maintain both representations as competing sources of truth.

**Generalize Cairn into development and research profiles.** Defer this unless
actual deployments reveal a reusable mechanical contract that local research
protocols cannot serve simply. Shared intellectual principles alone do not
justify a shared installation mechanism. Finishing thirty cycles is not an
automatic trigger for a profile proposal.

The recommendation is the separate assai runtime, with crux reuse first and a
small, persistent pilot. Change course if recovery fails, scientific challenge
does no more than replay outputs, controls are bypassable, attention repeatedly
exceeds the budget, or the work produces no leads Anthony values. Repair the
observed failure or narrow the runtime before expanding it.

## Open questions and fold-back

Before implementation details settle, resolve the exact crux revision and patch
policy; the filesystem and execution permissions behind each role; the compact
paper/claim representation and amendment rules; and the first journal's practical
test for distinguishing a model mechanism from evidence about the real system.
These are runtime design questions, not a reason to reopen all Cairn doctrine.

The local concept and display documents still need their names and implementation
instructions aligned. No repository creation, external-document edit, model
change, or publishing action is performed by this note.

Fold back to Cairn only lessons that prove general to developing research
software—for example, a useful continuity practice or a scientific-check
failure with broader relevance. Keep assai's controller, journal authority,
and claim lifecycle local unless evidence earns a wider home.

The strategic connection is sufficient as it stands: Cairn develops the
instruments under review; assai uses approved instruments for persistent
scientific exploration; promising papers bring evidence back to human-led work.

