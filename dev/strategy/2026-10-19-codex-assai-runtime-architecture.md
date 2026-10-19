# assai runtime architecture: persistent labs, protected execution, and a scientific record

**Author**: Codex (Strategy), for Anthony Kendall
**Model**: Codex; exact model identifier not exposed in this session
**Date**: 2026-10-19
**Status**: draft
**Type**: design-exploration
**Surfaces this would feed**: assai's architecture and first implementation plan, after Cairn adoption; the Cedar Creek operating specification and harness; the research display's data contract

## Recommendation in plain language

Build assai as one small Python application, not a collection of independently
deployed agent services. It keeps the schedule, protects resources, launches
isolated work, and records what actually happened. Labs and the journal supply
scientific judgment; they do not own the application's authority.

Give each lab a lasting identity and an inspectable history. Sessions come and
go, but the lab's questions, failed approaches, tools, papers, and unfinished
investigations survive. Papers and their reviews form the shared scientific
record. Dashboards, summaries, and lead briefs are views over that record.

Keep three things separate: the software repository, the live controller's
private state, and the ecosystem's versioned scientific record. Start with one
controller, one model harness, one persistent lab, and a journal with a
re-execution worker. Add the second lab without changing that architecture.

## 1. Scope, assumptions, and grounding

This is an architecture proposal in strategy form, not code or authorization
to operate unattended. All assai paths, commands, interfaces, and protections
below are **proposed**, unless explicitly identified as existing evidence.
The document stays in Cairn's strategy directory for now and can move later.

Assume Cairn supplies the development machinery: the development agent
instructions, proposal/plan/review workflow, session routines, work coordination,
and applicable verification tools. Do not recreate those in assai. Developing
assai follows Cairn; a lab conducting an in-scope experiment follows assai's
research protocol, not a software proposal per experiment.

The requirements are grounded in:

* [Cairn and assai](2026-10-19-codex-cairn-and-assai.md), committed as
  `c41edbad`: separate projects; persistent end-to-end labs; papers; delegated
  journal decisions; protected execution; crux reuse before reinvention.
* Anthony's local *Cairn Lab - Concept and Scope.md*, particularly its operative
  toy-build table, and *Cairn Lab - Nov 2 Plan.md*, read on 2026-10-19. Their
  older project names and profile assumptions are not architecture requirements.
* The assai checkout at `08ad42e59f01de267da349401b85bcbd381139c7`, which has
  an initial README rather than an existing runtime to preserve.
* LHM's accepted *agent-run-contract* proposal, read from the sibling checkout
  at `d3b5bd0fac6a7c3e93dc1b04377d85dd23d471dd`: model integration belongs
  outside individual models. Reading an accepted proposal is not evidence its
  runtime cap, exit result, or timeseries export has shipped or works.

The technical choices are recommendations, not measured performance claims.
Python's [SQLite interface](https://docs.python.org/3.13/library/sqlite3.html)
supports a local database without a separate database server. Use that for
operational bookkeeping, not as a replacement for papers or lab notebooks.
[Docker's security documentation](https://docs.docker.com/engine/security/)
makes clear that daemon access and privileged mounts are consequential;
calling something a container is not evidence of a safe deployment.

No assai implementation, model run, sandbox violation test, or crux integration
was executed for this note. The upstream engine's detailed features remain
attributed to the inspection recorded in `fce8e653`; the integration must select
an immutable upstream revision rather than treating a version label as a pin.

## 2. Architectural boundaries

There are four cooperating parts, with one controller as the only writer of
shared authority:

~~~text
Anthony ── approved scope, instruments, resources; audits and decisions
   │
Controller ── durable jobs, permissions, execution, publication and correction
   ├── Lab sessions ── whole investigations; private notebooks and drafts
   ├── Journal sessions ── pre-run critique and post-run scientific review
   └── Execution workers ── model runs, clean re-execution, scoring
              │
        Harness interface ── domain/model-specific inputs and observations

Controller ── writes ── Scientific record ── read-only views ── Labs / display
~~~

The controller is ordinary code, not a chief-scientist agent. It can enforce
that a reference set is approved and all required metrics are present. It
cannot decide whether the question is interesting or the mechanism convincing.
Those judgments belong to labs, reviewers, and Anthony, with their basis recorded.

The labs remain end-to-end investigators. Journal, replication, and scheduling
are supporting roles, not an assembly line that divides scientific ownership.
Process and Observation are starting emphases, not prohibitions on methods.

Start with a foreground cycle command that drives this same controller for a
bounded scheduling window. Run it manually first; an operator-configured host
scheduler can invoke it later. No always-on public service is required. Operator
commands use the active controller when present, or take exclusive ownership
for a short action when it is stopped. Scheduler configuration is deployment
work, not something a lab can edit.

## 3. Proposed repository layout

This tree is the assai **software** repository. Cairn-provided content is shown
only as an existing-by-assumption boundary. No file in this tree is created by
this strategy note.

~~~text
assai/
├── pyproject.toml
├── README.md
├── AGENTS.md, dev/, tools/, scripts/   # Cairn-supplied development support
├── src/assai/
│   ├── __main__.py, cli.py            # operator CLI and role-scoped tool client
│   ├── contracts.py                  # versioned request/record validation
│   ├── controller.py                 # application commands and job transitions
│   ├── store.py                      # operational SQLite transactions
│   ├── record.py                     # scientific records, artifacts, Git writer
│   ├── policy.py                     # actor capabilities, approvals, budgets
│   ├── execution.py                  # sandbox/process lifecycle and reconciliation
│   ├── agents.py                     # agent-session backend; no scientific policy
│   ├── notebooks.py                  # crux adapter and stable ID mapping
│   ├── journal.py                    # review workflow, not a second scheduler
│   ├── claims.py                     # evidence relations, queries, correction
│   ├── context.py                    # recoverable lab working packets
│   ├── harness.py                    # model-independent execution interface
│   └── exports.py                    # audit packets, lead briefs, display JSON
├── roles/
│   ├── lab.md
│   ├── journal.md
│   └── paper.md                      # paper shape; not a software proposal
├── ecosystems/cedar/
│   ├── ecosystem.toml                # public configuration and resource requests
│   ├── OPERATING.md                  # concise research operating rules
│   ├── AGENDA.md
│   ├── labs/{process,observation}/   # identity, starting scope, expertise emphasis
│   ├── harness/                     # LHM adapter, scenarios, observations, checks
│   └── references/                  # manifests and baseline definitions, not secrets
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── contracts/
│   ├── recovery/
│   ├── isolation/
│   └── fixtures/toy-harness/         # deterministic model and known-answer science
└── docs/
    ├── architecture.md
    ├── operating.md
    └── harness-authoring.md
~~~

These are responsibility boundaries, not a demand for a framework or one class
per noun. Start with small modules; split only when a real responsibility grows.
Use standard-library facilities for orchestration, structured files, subprocess
handling, and SQLite. Scientific dependencies belong in versioned harness
environments, not in the controller. Agent and container executables are explicit
host dependencies. Cairn's own dependency policy is not silently imposed on all
scientific analysis code.

Keep domain knowledge in the ecosystem and harness. Use a named adapter registry
whose executable and environment are approved at deployment; never import a
Python module or run a host command named by an agent's arbitrary request.
There is no plugin marketplace, distributed worker cluster, vector database,
public API service, or general workflow language in the first build.

## 4. Live state is outside the software checkout

Give each deployed ecosystem an operator-owned runtime home, on local storage.
Its path is deployment configuration, not a hard-coded home directory. For
example, the following is a proposed layout, not an existing directory:

~~~text
<runtime-home>/cedar/
├── control/
│   ├── state.sqlite                 # jobs, reservations, sessions, pending writes
│   ├── active-policy.json           # approved live limits and instrument bindings
│   ├── sealed/                      # held-out data, planted-error answers, secrets
│   └── receipts/                    # private/raw execution and provider records
├── record/                          # its own local Git repository
│   ├── experiments/<id>/            # registered definition and amendments
│   ├── runs/<id>/                   # certificates and artifact manifests
│   ├── labs/<id>/                   # checkpointed notebooks, histories, skills
│   ├── papers/<id>/revisions/<n>/    # manuscript, claims, bundle manifest
│   ├── reviews/<id>/                # critique, rerun report, editorial disposition
│   ├── corrections/<id>/            # challenges, withdrawals, affected descendants
│   ├── approvals/<id>/              # operator grants, without credentials
│   └── audits/<id>/                 # selection, findings, time and dispositions
├── artifacts/                       # content-addressed large inputs/outputs
├── workspaces/<session-id>/          # isolated work; not an authority store
└── exports/                         # replaceable read-only query/display views
~~~

The scientific Git repository is a data record, not another software product or
release train. It starts on day one. The application source repository does not
fill with nightly commits or large model outputs, and a code upgrade cannot
accidentally erase a lab's identity. Moving an ecosystem later means moving its
record, artifacts, live state, and deployment policy—not just its persona file.

| Resource | Writer | Agent access |
| --- | --- | --- |
| Application code and approved harness images | Development/deployment process | Read-only approved snapshots |
| Lab workspace | Assigned lab session | Write its own drafts and provisional notebook |
| Review workspace | Assigned fresh journal session | Write review proposals, not publication state |
| Scientific record | Controller's serialized record writer | Read permitted snapshots; submit changes through tools |
| Operational database, commitments, live policy | Controller/operator | No direct file access |
| Hidden observations, test answers, authority credentials | Operator and narrowly assigned services | No lab/journal access; only permitted scoring outputs |
| Exports | Controller/exporter | Read-only; never a source of authority |

The runtime controller must not run inside a lab's writable environment. An
unrestricted agent with the controller's operating-system identity and host
filesystem access defeats this design, even if it promises not to edit files.
Materialize permitted record views for each role; do not mount the whole record
repository or its Git history and assume that selecting a few current files
hides another lab's private notebook or earlier restricted content.

## 5. Sources of truth and record shapes

Use **SQLite for live operational state**, **Git-versioned files for scientific
history**, and an **artifact store for bulky evidence**. Each has one job:

* SQLite owns job state, budget reservations, session leases, and pending
  publication work. It is not an independently editable claim database.
* Versioned records own paper revisions, notebook checkpoints, review decisions,
  approvals, corrections, and the pre-run commitments behind scientific claims.
* Artifact digests identify the exact datasets, code bundles, environments, and
  output files used. Availability and permission checks are separate from hashes.
* Claim indexes, working summaries, display JSON, and a readable approvals summary
  are derived views. Rebuild them from the record; never reconcile competing edits
  to a second authoritative claims table or approvals document.

Ingest artifacts into controller-owned temporary storage, verify their bytes,
and finalize them before a scientific commit can reference them. Missing or
corrupt referenced artifacts make evidence unavailable, not a clean reproduction.
Keep draft garbage separate from retained evidence; automatic workspace cleanup
must not delete the only copy of a referenced output, notebook or code bundle.

Use controller-issued IDs and versioned JSON envelopes. Every submitted object
names its schema version, ecosystem, object ID/revision, evidence references,
and the record revision it was based on. The controller supplies the authenticated
actor and receipt time; it does not trust a JSON field saying "I am the journal."
Validate bounded sizes, allowed fields, identifier shape, path containment,
finite numeric values, and compatible units/time axes at the relevant boundary.
Missing information is explicit, not a fabricated zero or empty success.

Keep codec/validation rules in one implementation used by both the tools and
record writer. Preserve old schema readers and record migration provenance;
do not rewrite historical paper or notebook bytes merely to upgrade a schema.

The initial record types are deliberately few:

| Record | Required meaning |
| --- | --- |
| Lab checkpoint | Stable lab ID; notebook snapshot; active investigations; next actions and reasons; failures; learned procedures; unresolved criticism; referenced papers/runs; current correction revision |
| Experiment registration | Question/hypothesis; alternatives; scenario; approved instrument/reference versions; test and control definitions; expected outcomes; tolerances; evidence dependencies; exact frozen input/code manifest |
| Run certificate | Registration digest; actual executable/image, code and input digests; start/end and termination reason; outputs; resource accounting; missing/unavailable fields and reasons |
| Paper revision | Manuscript; contribution type; structured claims; supporting certificates and figure/table artifacts; limits; proposed next test; disclosure of exploratory changes |
| Review/disposition | Exact paper/registration revision; reviewer session; methods critique; reproduction result; scientific objections; editorial action and reasons |
| Approval/correction | Authorized actor; exact target and scope; prior/new revision; rationale; affected records; timestamp; any expiry or replacement |

Private provider receipts may contain prompts or sensitive material. Keep those
outside the generally readable record; publish a redacted provenance description
and digest where appropriate. Record model identity and sampling settings as
reported, with "unavailable" when the backend supplies neither a seed nor an
immutable model version. A seed alone never guarantees repeatability.

Keep notebook questions and hypotheses in crux. Do not duplicate its entire
question tree in SQLite. assai owns cross-notebook IDs, permissions, run links,
publication and correction—not a competing notebook model.

## 6. Controller commands, actors, and execution

The public interaction is a small command/tool surface: read context, checkpoint
work, propose a registered test, request execution, submit a paper/review, query
claims, and request a scope/instrument change. Operator commands additionally
approve deployment policy, pause/resume scheduling, reconcile jobs, and restore
backups. Exact command spelling is not an architectural contract yet.

All writing commands reach the same controller application functions, whether
called by the operator CLI or an agent tool. No alternative "quick" publication
path bypasses policy, validation, or revision checks.

For each session, the controller issues a role-scoped capability over a local
tool channel mounted only into that session's sandbox. Capability means a
limited permission, not the model's self-description. Bind it to the lab or
journal ID, ecosystem, operation set, expiry, and resource allowance. Revoke it
when the session ends. The session cannot mint journal or operator authority.
The controller derives identity from its issued channel, not submitted prose.

Build runtime session instructions from its role, the ecosystem operating rules,
and the lab's scope/context. The session's working directory is its isolated
workspace, not the assai development checkout. Do not accidentally auto-load
Cairn's developer instructions and turn a nightly experiment into a software
proposal awaiting a human Decision. Papers, literature, notebook text and tool
outputs are evidence to inspect, not instructions that can grant capabilities.

Ordinary scientific scripts execute inside the lab sandbox or a model-job
sandbox. Tools that start model jobs take scenario and artifact IDs, not shell
strings. Experimental scripts can be submitted as paper evidence without being
promoted into trusted harness code. Any such script is treated as untrusted
code by the replicator, even after journal acceptance.

Ingest bundles as untrusted files: reject escaping paths, symlinks, hard-link
tricks, device entries and excessive size before moving anything into protected
storage. Never execute a paper's instructions in the controller process.

The first execution backend should be a local container runtime on a specified
supported host. Containers have explicit read-only inputs, separate output
directories, bounded memory/CPU/time, no controller mounts, no container-daemon
socket, and no privileged mode. Research jobs have no network by default.
Literature/data retrieval is a separate approved tool that records its sources,
not unrestricted network access from the model runner.

An agent-provider adapter launches a **fresh session** with a context packet and
role tools, records usage and termination, and checkpoints accepted work. It
does not choose the science or grant itself extra tools. The existing agent CLI
may be the first backend only if all its shell/file actions can be confined to
the assigned sandbox. A trusted host-side model gateway can hold provider
credentials; a CLI whose unrestricted host tools can reach those credentials
does not meet the boundary. Prove the actual backend configuration before use.
This design does not assume purchasing a new API service or subscription.

Reserve resources before launching jobs. Include journal and reproduction costs
in the same ecosystem budget, with an allocation that prevents labs consuming
all capacity before their submissions can be checked. Hard wall-time and process
limits must be enforced by the executor, including child processes. If a backend
cannot enforce a requested token/spend limit, record that limitation and resolve
the operating policy with Anthony; do not present an estimate as a hard cap.

## 7. A complete investigation through the system

**Resume.** The controller admits one active session per lab, pins a scientific
record revision, and builds its working packet. A lab can follow any question
inside its approved scope. A cycle is a scheduling opportunity, not a demand
for a completed paper every night.

Checkpoint at consequential tool boundaries, before launching a long run, and
at session end. Preserve the workspace after abnormal termination until its
drafts and outputs have been recovered. Recovery may admit those bytes as an
unreviewed draft, never as an approval or accepted finding. A stopped session
must not cause automatic deletion of its only copy of unfinished work.

**Register.** The lab proposes an experiment. The controller checks instrument,
reference and budget authority. A fresh journal session critiques the proposed
alternative explanation, discriminating result, controls and effect sensitivity.
The lab can revise; bounded exchanges end in proceed, revise-later, or escalation,
not an infinite nightly debate. Exploratory work is permitted and labeled;
confirmatory wording requires a commitment predating the relevant results.

**Freeze and launch.** Capture the actual bytes of the test definition, code,
input selection, expected results and tolerances in controller-owned storage.
Record the commitment in the scientific history before launch. Bind the job
to that digest; requests cannot silently replace it. Amendments create another
attempt. Dataset identifiers alone are insufficient if files behind them change.

**Observe.** The executor records a terminal outcome even on refusal, timeout,
missing output or child-process cleanup failure. The harness extracts named
quantities and evaluates declared checks. The lab interprets these observations;
it cannot turn a missing result into a successful check by editing a checkbox.
Unplanned analyses remain legitimate but are disclosed as exploratory.

**Submit.** Freeze a paper revision with its manuscript, claims, figures/tables,
and reproducible bundle manifest. Subsequent edits are a new revision. Rejected
submissions and their criticism remain part of the lab's history, not necessarily
the journal's accepted literature.

**Reproduce and challenge.** A clean job re-executes the submitted bundle against
the exact declared versions and compares with the paper's own outputs. It uses
no lab writable cache or undocumented current installation. A fresh journal
session reads that result and challenges the scientific argument separately.
Neither rerun agreement nor agreement between agent vendors establishes a
physical mechanism. Review ends in an attributed disposition on an exact revision.

**Publish.** The controller accepts only an authorized disposition whose evidence
and targets still match. It writes the paper/review record and updates derived
claims. Journal acceptance admits a paper into the working literature; it
neither certifies truth nor authorizes an instrument change. Revision requests
produce new submissions, not silent manuscript replacement.

**Continue.** Labs may build on accepted work in their next sessions, carrying
unverified assumptions and shared inputs visibly. A proposed next test in a
paper is a scientific commitment to compare later, not authority to exceed scope
or budget. A lab can finish an investigation, abandon it with reasons, or follow
a surprise without the controller becoming its principal investigator.

**Promote to human-led work.** A promising paper can produce a lead brief or
instrument-change request referencing its evidence and any experimental code.
Anthony decides whether to pursue it or open a Cairn proposal in the owning
software repository. assai neither edits that model nor opens a proposal there
automatically. A later model release enters the ecosystem only through an
explicit instrument approval binding the exact version and its baseline checks;
the earlier version remains available for interpreting and reproducing old work.

## 8. The notebook boundary: crux without self-approval

Prefer a thin adapter around a pinned crux engine. The adapter must support
reading a notebook, applying authorized edits, taking a checkpoint, preparing
bounded context, and mapping approved experiment/review actions to upstream
transitions. Confirm the real CLI/engine contract before coding against it;
the detailed command mapping is not inferred from similar names.

A lab's provisional notebook is agent-authored material. It may contain forged
approval fields, altered lock hashes, or a claimed verdict. Those fields cannot
authorize a run or publication. The adapter admits permitted author changes
against the last checkpoint, then the controller applies role-authorized
transitions to its canonical notebook snapshot. Only controller-owned
registrations and authorized review records count as approval evidence.

crux can calculate a verdict from recorded outcomes, but scientific checks must
remain linked to actual observations and review. A failed positive control means
invalid-run, not evidence against the hypothesis. A null result's control must
demonstrate sensitivity at the effect size being claimed, not merely satisfy
the requirement that a control field exists.

Do not give a lab write access to the controller's crux copy and assume a CLI
allowlist makes it safe. Direct file modification must be ineffective as well.
Evaluate import/export and fresh-session recovery before adopting a large fork.
If reuse requires replacing crux's whole state model, reconsider the integration
rather than maintaining two authoritative notebooks.

## 9. Harness contract: one shape, model-specific implementations

Keep the concept's six operations, with structured requests/results and a
versioned adapter identity:

| Operation | Contract |
| --- | --- |
| run(scenario, out_dir) | Execute an approved scenario in an isolated job; produce a terminal result even when no model output exists |
| observe(out_dir) | Return named quantities, units, spatial/temporal definitions, provenance, and explicit unavailable values |
| compare(quantities, reference) | Report every metric in the approved reference definition, with tolerance/aggregation definitions or a reason it cannot be computed |
| checks(out_dir) | Report apparatus/model validity checks with evidence, not the lab's scientific conclusion |
| reproduce(bundle) | Re-execute the paper's pinned procedure in a fresh environment and compare with its original outputs within predeclared tolerances |
| verify_base(run) | Check the unchanged baseline instrument against its separately frozen baseline expectations |

These are application operations, not calls that let imported adapter code run
with all controller privileges. Execute model and analysis adapters through the
worker boundary; send only the input view that operation requires. A scoring
worker may read held-out observations, but an arbitrary submitted analysis may
not share that mount or its credentials.

No native model must implement assai's schema. Each adapter translates the
model's existing files into it. A timeout is enforced outside the model as well;
if model licensing or installation prevents container execution, a dedicated
restricted worker account is an alternative requiring the same isolation and
whole-job termination evidence—not a silent fallback to the controller account.

The Cedar Creek adapter owns LHM invocations, hydrogeologic units, reference
periods, gauge/well selection, and scenarios. assai's controller knows none of
those meanings. Verify LHM's actual available outputs before implementing the
adapter; an accepted upstream change is not a shipped dependency. Do not use
overwriting a live model output directory as job isolation.

Reproduction and baseline regression return separate reports. Replaying a paper's
12 as 12 can pass reproduction even if the baseline is 10; replaying its 12 as
13 outside the declared tolerance fails reproduction. A method that reproduces
bad science is deliberately part of the journal's known-answer tests.

## 10. Persistence, retrieval, and scientific correction

Build a working packet from the lab's latest checkpoint plus changes since its
last seen record revision. Include active questions, competing explanations,
the reason for its next test, failures and useful procedures, open reviews,
and any corrections affecting its dependencies. Summaries cite underlying
records; a lab can retrieve those records rather than trusting a summary alone.

Use structured metadata/keyword queries first: relevant questions, claims about
a quantity/place/method, contradictions, dependencies, and reused procedures.
Bound packet size but always include pending invalidation notices before
optional historical context. Report omitted results and allow paging; a limited
search result must not look like proof that no contrary evidence exists.

Lab memory is not a public literature feed. Other labs read published papers
and explicitly shared procedures, not another lab's entire provisional notebook
by default. Expertise remains local until deliberately exchanged. A conference
publishes a versioned exchange record; adoption by another lab records shared
lineage so later agreement is not counted as independent evidence.

Claims have immutable IDs, an evidence basis, and explicit scope. Preserve the
concept's outcome vocabulary—exploratory, reproduced, challenged, independently
supported—alongside a separate standing such as current, needs-reconsideration,
or withdrawn. Withdrawal is not a higher or lower rung of confidence. Each
change cites the review or correction that warrants it.

Store requires relations separately from motivated-by citations, and record
shared inputs, calibration targets, forcing data, tools and transferred methods.
Validate claim references and prevent circular support through requires edges;
do not prohibit ordinary reciprocal citations in papers. Adding an assumption
does not turn it into a fact. Journal acceptance is not human-audited status.

When a required claim changes materially, traverse its descendants and mark
them for reconsideration before supplying new working packets. Only the
journal's evidence-based correction can resolve their scientific standing.
Do not automatically withdraw a result that has other support, and do not
invalidate a result merely because it cited a motivating paper. Record the
affected set and resolution, refresh summaries, and pause dependent queued jobs
whose registered assumptions no longer match. Already-running jobs remain
recorded but cannot silently publish against obsolete assumptions.

Dependency tracking propagates correction obligations, not calibrated confidence.
The independently-supported label requires evidence beyond shared input or
calibration lineage; neither a second lab nor a different model provider suffices.

## 11. Restarts, concurrency, and publication consistency

Use one controller writer and serialize Git writes. SQLite transactions cover
job admission and budget reservations; keep them short and explicitly configured.
They do not atomically include filesystem writes, Git commits, or external
process launches. Handle those gaps rather than pretending one transaction does.

Every writing request carries a unique action ID and expected target revision.
Repeating the same action with the same content returns its prior result;
reusing its ID with different content is rejected. A stale expected revision
requires refresh. This prevents duplicate publications and accidental overwrites,
not duplicate scientific ideas.

For a publication, store pending work in SQLite, prepare validated files in
controller-owned staging, verify referenced artifacts, and commit one complete
scientific update with its action ID. Only then acknowledge it in SQLite and
advance derived views. After a crash, inspect committed action IDs before
repeating pending work. Uncommitted staging is not published evidence. Git and
SQLite are recoverably coordinated, not jointly transactional.

For execution, reserve resources and create the job record first. Create a
uniquely labeled stopped worker, persist its handle, and only then start it.
On restart, reconcile handles and labels with actual workers. Unknown state
does not mean success and does not automatically authorize rerunning an expensive
experiment. Cancellation remains visible until the worker and its descendants
are confirmed stopped. Retries are new attempts charged to the same budget.

Allow one active session per lab and one admitted execution per configured
resource slot. A second controller must fail to acquire exclusive deployment
ownership; do not run two writers and rely on polite scheduling. Review and
execution may overlap where resources permit, but no lab writes shared files
directly and no session waits forever for a failed peer. Expired sessions retain
their last accepted checkpoint and leave a failure receipt.

Back up the operational database consistently, the scientific Git repository,
artifact manifests/data, and sealed configuration separately. Test restoring
them into a stopped deployment before trusting nightly operation. Restored jobs
start paused, are reconciled, and do not resume merely because a database row
says running. Hashes detect changed bytes, not a missing backup or an authorized
operator rewriting history.

## 12. Audits, hidden tests, and read-only outputs

Keep hidden observations and planted-error answers outside both agents' mounts
and the public scientific record. Inspect the actual data path: if a model's
input or exported timeseries embeds held-out observations, exposing that file
defeats the separation. Provide authorized views or keep that operation entirely
in its trusted worker. Record prior calibration/exposure; publicly available
observations are not magically unknown because assai calls them held out.

Repeated hidden scoring is development feedback. Reserve any genuinely untouched
final check for one frozen candidate; journal acceptance need not claim independent
confirmation. The controller tracks accesses and exposes only permitted scores,
not hidden rows or test answers through errors, logs, or display exports.

The journal test set includes a valid result, a broken apparatus, a subtle wrong
analysis that reproduces, and a known-sound control. Rolling planted errors use
Anthony's sealed schedule, interleaved with sound controls. Track failures to
notice, false alarms, and time to detection; rejection of everything is not
success. Test material remains identified privately so it cannot become ordinary
accepted literature by accident, while preserving the journal's blinded behavior.

The controller selects the weekly audit sample and consequential/high-fan-out
reuse, not the labs. Produce a bounded packet with the claim, evidence basis,
dependencies, pertinent reviews and unresolved objections. Record audit and
decision time separately. The existing two-random-claims starting budget and
six-hours-in-each-of-two-weeks pause rule are operating-policy inputs, not
hard-coded scientific laws. Changing them is an explicit operator decision.

Generate lead briefs and the research dashboard from a single scientific-record
revision. Include IDs, evidence basis, correction/withdrawal state, source
revision, generated time and availability. The display cannot adopt instruments,
publish papers, or change claims. Static example data is labeled sample; missing
or stale live data never silently becomes a demonstration of current operation.
Only deliberately selected exports reach the website; no private runtime tree
is served. Cairn's development board remains a separate source, not a duplicate
software-lifecycle engine inside assai.

## 13. First build and the demonstrations that decide it

Build the shortest complete path, in this order. These are proposed slices,
not a replacement for the later implementation plan or a promised calendar.

1. **Records and a fake world.** Minimal CLI, contracts, operational store,
   scientific writer, fake agent backend and deterministic toy harness. Prove
   request identity, revision checks, artifact references, and restart behavior
   without buying model calls or running LHM.
2. **A genuinely persistent lab.** Integrate the pinned notebook and context
   packet; checkpoint interrupted work; recover it in a fresh session. Add the
   actual agent backend only with its tool/credential and budget boundaries
   demonstrated. No scheduled operation on an unrestricted host agent.
3. **One real investigation.** Add the Cedar Creek harness and approved input
   views; register a test, run it, submit a paper, re-execute it and conduct a
   scientific review. Preserve criticism and continue the investigation.
4. **Correction and unattended operation.** Demonstrate the failure matrix
   below; then run manual cycles before enabling the nightly scheduler. Add
   the display from real recorded outputs, without making a visit deadline
   substitute for operational evidence.
5. **A second end-to-end lab.** Independent workspace/history, shared literature,
   limited resources and recorded method exchange. Add conferences only when
   there is something useful to exchange. Observe twenty to thirty cycles
   within the human attention budget before considering generalization.

| Demonstration | Result that must not pass unnoticed |
| --- | --- |
| Fresh-session recovery | The lab remembers its conclusion but loses the alternative, failed approach, or reason for its next test |
| Notebook/approval forgery | Editing a local approval/hash or claiming a journal identity authorizes execution or publication |
| Filesystem/execution boundary | A lab reaches live policy, sealed data, host credentials, the daemon socket, or arbitrary host execution through another tool |
| Resource exhaustion and cancellation | A hung child process survives job termination, a retry bypasses accounting, or reviews exceed their reserved allocation |
| Reproduction versus baseline | Agreement with a baseline masks disagreement with the submitted paper's outputs |
| Scientific challenge | The journal accepts the reproducible wrong analysis or rejects the known-sound case without a defensible scientific reason |
| Corrections | A requires descendant is missed, a motivated-by citation alone invalidates work, or resumed context conceals the correction |
| Crash around publication/launch | A paper appears twice, an incomplete record becomes accepted, or an expensive run is duplicated after restart |
| Backup restoration | A lab history or evidence artifact is missing, or restored jobs restart without reconciliation |
| Domain separation | A synthetic non-hydrology harness needs to edit controller logic to report a valid quantity or failure |

Future implementation tests invoke the fake-world, contract, recovery, isolation,
and publication cases. Manual backend/model probes supply evidence the fakes
cannot: actual permissions, provider behavior, licensed model execution, and
whole-job cleanup on the chosen host. The operator explicitly enables the
scheduler after reviewing that evidence. No test or gate described here exists
merely because it has been named.

## 14. Alternatives, unresolved integration, and promotion

**Simpler alternative:** one persistent analyst with the same notebook, papers,
controlled execution and scientific review. Choose it if the second lab mostly
duplicates work or creates attention costs without useful disagreement. What
is lost is parallel expertise development, not continuity or the paper record.

**Storage alternative:** all operational bookkeeping in files. It removes SQLite
but requires bespoke queue locking and crash-safe reservations. Prefer the small
database unless the first vertical slice shows it adds more complexity than it
removes. Do not introduce a separate database service to solve the toy.

**Notebook alternative:** a small local implementation if a pinned crux cannot
support the role mapping without invasive rewrites. Preserve exportable histories
and test recovery; do not choose on vocabulary alone or maintain two notebooks.

The integration questions to settle first are the real agent backend's confined
tool/credential model and usage limits; the deployment host/container runtime and
LHM licensing constraints; the crux revision/license and permitted state edits;
and the exact first reference sets, metric definitions and scientific controls.
Their answers may change an adapter or deployment choice, not justify silently
weakening a claimed boundary. If no existing backend meets the budget/isolation
requirements, keep operation manual until Anthony chooses the tradeoff.

Success initially means a recoverable loop and an output Anthony values—not
proof of accumulated knowledge or a reason to refactor Cairn. Once the design
is ready for implementation, move or promote it into assai after Cairn adoption,
carrying the scientific requirements and explicit unknowns with it. This note
creates no assai files and changes no Cairn doctrine, scaffold, or release work.

## Review -- Codex (Security) -- 2026-10-19

**Foundations**

1. **Should this happen as framed?** Yes, with the access and disclosure contracts below completed before implementation: one controller, untrusted experimental code, and separately protected scoring are appropriate boundaries for this research loop -- sections 4, 6, 8, and 9 at `ba15a599`.
2. **Best alternative.** Keep this architecture and add a small shared authorization policy used by object access, outbound tools, and exports; select one concrete sandbox deployment for the first slice rather than adding services or bespoke containment -- sections 3, 6, and 13 at `ba15a599`.
3. **What would show it wrong?** A permitted tool can retrieve another lab's private artifact, reach a host service, send restricted material to a provider, or exhaust the storage needed to record a refusal; the future isolation and recovery demonstrations must cover these cases -- section 13's failure matrix and findings ASR-1 through ASR-4 below.

**Model**: GPT-6 (Codex; exact deployment identifier unavailable)
**Reviewed commit**: `ba15a599ab3afd8b2449efcb501246693afc59ed`
**Target**: this complete strategy note, sections 1-14
**Obligation**: requested Security Review of the proposed runtime architecture
**Verdict**: **REVISE the security contract before promotion to implementation.**

This is a temporary strategy review. The author should fold accepted points
into the note and remove this section, following the strategy template. The
findings identify design gaps and plausible failure paths, not reproduced
vulnerabilities in an implementation that does not yet exist.

### What the architecture gets right

The controller owns authority independently of agent prose. Labs cannot edit
live policy or canonical approvals; paper code stays untrusted after journal
acceptance; and the scorer does not share its hidden-data mount with submitted
analysis. Sections 4, 6, 8, and 9 state those boundaries clearly. Section 11
also correctly acknowledges that SQLite, Git, and process launch are separate
operations and supplies reconciliation rather than claiming joint atomicity.
Sections 7 and 12 distinguish reproducibility, scientific judgment, hidden-test
exposure, and instrument adoption. Those choices should survive the revision.

### Findings

1. **ASR-1 -- HIGH: role authentication needs an explicit object-access rule.**

   Sections 4-6 promise permitted snapshots, separately checked artifact
   permissions, and a capability bound to a lab/journal ID and ecosystem
   (lines 199-214, 225-226, 237-242, and 282-287). They do not state how that
   identity constrains access to a particular record revision or artifact.
   Authenticating a lab and permitting an artifact-reading operation does not
   establish that it may read a supplied artifact ID. A reference in a paper,
   a known digest, or a search result could otherwise turn the controller into
   a reader for another lab's notebook or a sealed scoring object. The same
   omission affects attachments, context retrieval, evidence links, and exports.

   **Satisfier:** specify a single mandatory authorization rule for each object
   and reference, including reads, listing/search, context assembly, writes,
   publication, and export. Record visibility and ownership independently of
   content identity; knowing a digest grants no access. Check the authenticated
   actor, operation, object revision, ecosystem, and current grant before
   returning or linking protected data. Shared bytes must not inherit public
   access merely because another reference to their digest is public. Scope
   journal access to assigned material. A future contract test should deny
   cross-lab/cross-ecosystem reads and references, including a known artifact
   digest and an expired grant, beside a permitted same-lab read. The existing
   private-history requirement should remain; this makes its tool path precise.

2. **ASR-2 -- HIGH: the retrieval tool is an unspecified network bridge around
   the sandbox.**

   Section 6 removes network access from research jobs but delegates retrieval
   to an approved tool (lines 306-311). Approval of the executable and recording
   its sources do not constrain the destinations it can contact. If a lab can
   supply a URL, a literature request or redirect can target localhost, private
   services, or a metadata endpoint reachable by the fetcher. The sandbox can
   remain intact while this permitted host-side tool exposes protected data.
   This is a design risk, not a claim that a fetcher has already been written.

   **Satisfier:** define retrieval as a narrowly privileged worker with an
   operator-approved destination policy, permitted protocols, validation of
   resolved destinations and redirect hops, and enforced network restrictions.
   Give it neither controller storage nor ambient host credentials; define any
   private data source as a separate explicit grant. Bound response size, time,
   and decompression, and treat fetched bytes as untrusted input. Prefer a
   small approved-source set for the first ecosystem. The later demonstration
   should permit a normal source while denying local/private destinations,
   a public-to-private redirect, and a destination change between checking and
   connecting. These controls follow the threat described in the
   [OWASP SSRF prevention guidance](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).

3. **ASR-3 -- HIGH: protecting provider credentials does not define permission
   to disclose research data to that provider.**

   Sections 5 and 6 protect raw receipts and gateway credentials
   (lines 260-264 and 313-320). Sections 4 and 12 separately protect sealed
   observations. Nothing defines which intermediate datasets, notebook text,
   model outputs, or licensed/private material may enter a provider request.
   An agent may be allowed to inspect a local file without being allowed to
   transmit its contents externally. Prompt-injected literature can also ask it
   to send data through a retrieval URL or an otherwise permitted model call.
   Keeping the provider key outside its sandbox does not close that path.

   **Satisfier:** make outbound disclosure an operator-approved deployment
   policy, including approved providers/destinations and the data classes each
   may receive. The controller should build permitted context views; restrict
   both model requests and retrieval request bodies/URLs under the same policy.
   For the first build, use only data approved for that provider in any session
   able to send arbitrary prompts there. Once restricted content reaches an
   agent, a text filter is not a reliable way to prevent it being paraphrased
   into an outbound request. Keep sealed scoring in workers without that
   channel. A later demonstration should trace a marked restricted datum through
   context, tool responses, provider payloads, logs, and exports, with an
   approved-data request as the passing control. This requires one recorded
   deployment decision, not human approval of every model call.

4. **ASR-4 -- MEDIUM: resource protection omits cumulative storage and the
   capacity needed for recovery.**

   Sections 5 and 6 bound submitted object sizes and job memory/CPU/time/spend;
   sections 7 and 11 preserve interrupted work and retained evidence
   (lines 231-242, 306-327, 336-340, and 536-541). Those are useful constraints,
   but a sequence of individually permitted jobs can fill artifacts, workspaces,
   receipts, Git history, or container logs. A single noisy job can also exhaust
   output space before its time limit. The controller then cannot reliably
   persist its terminal failure, reconcile work, or back up the scientific
   record. Memory and CPU limits do not specify a storage quota; Docker's
   [resource documentation](https://docs.docker.com/engine/containers/resource_constraints/)
   reinforces the need to configure limits rather than assume container defaults.

   **Satisfier:** include per-job output/log/file-count limits and cumulative
   ecosystem storage quotas in admission and execution policy. Reserve capacity
   for controller state and terminal receipts, stop new admissions before it is
   exhausted, and define retention/garbage collection without deleting evidence
   still referenced by a retained record. Specify a process-count limit as well
   as whole-job cancellation. Demonstrate output exhaustion and accumulation
   across multiple valid small jobs; both should stop safely with a durable
   reason, while a normal job and later recovery still work.

5. **ASR-5 -- MEDIUM: read-only exports still need a safe rendering boundary.**

   Section 12 selects exports and gives the display no publication authority
   (lines 571-578), but it does not constrain active content in papers, figures,
   or downloaded bundles. Read-only files can contain executable HTML/SVG,
   browser requests, or misleading links. A display that inserts manuscript
   text as HTML can execute agent-authored content in the operator's browser
   even though it cannot write the scientific repository.

   **Satisfier:** render manuscript/claim text with escaping and a restricted
   markup policy; use inert figure previews produced in a restricted worker.
   Do not serve submitted active files inline under a trusted application
   origin. Keep downloadable untrusted originals isolated, and keep the public
   display separate from any operator control channel. Include malicious
   markup, SVG, and remote-resource references in the later display checks,
   beside a sound text-and-figure rendering. This preserves the proposed
   dashboard and downloadable evidence without treating either as trusted code.

### Recommended implementation shape and residuals

Keep the single controller and the intended scientific outcomes. Add a compact
permission table covering actors, object visibility, outbound destinations/data
classes, and resource allowances. Enforce it where the controller resolves an
ID or dispatches a tool; role prompts are context, not enforcement. Use one
concrete supported host and container profile for the first deployment, with
measured permissions and cleanup behavior before enabling unattended cycles.
Docker's [security guidance](https://docs.docker.com/engine/security/) supports
the note's caution about daemon authority and configuration; it does not make
the proposed deployment an already-verified sandbox.

A hostile host administrator, host/runtime compromise, model-provider trust,
and scientific mistakes surviving journal review remain separate residuals.
Define the first deployment's assumptions about them explicitly. This review
does not require an external trust service, distributed workers, cryptographic
paper signing, or another review workflow to address the five findings.

### Coverage

**Covered:** claims and drift against the committed note's explicit proposed
status (section 1); design completeness and failure behavior across object
access, execution, resource limits, and recovery (sections 4-6 and 11);
cross-document/scientific scope against
`dev/strategy/2026-10-19-codex-cairn-and-assai.md`; the LHM agent-run-contract
proposal's accepted header and Decision at its cited `d3b5bd0f`; the initial
assai commit `08ad42e5`; the attributed crux inspection at `fce8e653`; lifecycle
placement through the manual-cycle and scheduler-enablement sequence (sections
13-14); and a named satisfier for every finding. Opened the note's Python SQLite
and Docker documentation links and the additional OWASP/resource references.

**Not covered / low confidence:** no assai runtime or production-path tests
exist at the cited initial checkout, so no isolation, permission, provider,
recovery, or browser behavior was executed or certified here. I did not
independently inspect upstream crux code, the two local concept/display source
documents, a deployed container profile, provider contractual data terms, or
LHM execution/scientific calculations. The later demonstrations named above
are recommendations for implementation evidence, not tests this review ran.
