# assai runtime architecture: persistent labs, protected execution, and a scientific record

**Author**: Codex (Strategy), for Anthony Kendall
**Model**: Codex; exact model identifier not exposed in this session
**Date**: 2026-10-19
**Status**: revised
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
│   ├── policy.py                     # object access, disclosure, approvals, limits
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

The initial supported deployment is one Linux host with Docker Engine, a
dedicated controller account, and non-privileged job containers. Before real
execution, record the exact host/runtime versions, image digests, identities,
mounts, network rules and enforceable quota configuration as one deployment
profile. Development on another host does not establish its isolation. The
controller's daemon access is trusted authority and never reaches a job.

Trust the operator, host administrator, kernel/runtime and approved controller
code; hostile administration or host/runtime compromise is outside this first
boundary. Provider handling/retention of disclosed data requires an explicit
deployment decision. Prompt injection and mistaken science remain possible:
the access policy limits authority and disclosure, not scientific error.

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

**One object-access rule.** Every record revision and artifact reference carries
its ecosystem, owner, visibility, and outbound-disclosure class independently
of its content digest. Local visibility starts as own-lab, assigned-review,
ecosystem-shared, public, or sealed. Newly submitted objects inherit restrictive
input permissions; an agent cannot declare its inputs public or erase restrictions
by copying, summarizing, or repackaging them. Sharing and classification changes
require the authority defined in the operator-approved policy.
Apply the combined restrictions of a session's exposed inputs to its outputs;
do not ask a language model or a text filter to infer whether a derived sentence
still contains restricted information.

The same policy function must authorize the authenticated actor, operation,
specific object revision, ecosystem, current grant and destination where relevant.
Apply it to reads, listings/search, context assembly, writes and referenced
objects, paper publication, and every export. Journal grants cover assigned
material, not every notebook; cross-ecosystem access needs an explicit grant.
A permitted operation or paper reference is not permission to dereference every
attachment. Check every reference before returning or linking its contents.

Knowing an ID or digest grants no access. Identical bytes stored once can have
separately protected references; a public reference must not expose the metadata
or authority of a private one. No raw digest-fetch endpoint bypasses object
checks. Filter search results, counts and errors so they do not expose restricted
objects. Recheck grants before tool dispatch and publication; expiry/revocation
stops new access and invalidates cached views, but cannot recall earlier disclosure.

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

Keep object access, disclosure destinations/data classes, and resource allowances
in one compact deployment policy consumed by those functions. Its rules are
deny-by-default and revisioned with operator authority, not copied into separate
allowlists in search, context, retrieval and display implementations.

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

Use the recorded Linux/Docker deployment profile. Containers have explicit
read-only inputs, separate output directories, bounded memory/CPU/time/process
counts and storage, no controller mounts, no container-daemon socket, and no
privileged mode. Research jobs have no network by default. Backend-native
browsing or other outbound tools must be disabled unless they obey the same
destination and disclosure policy as controller-dispatched tools.

**Retrieval is a restricted worker, not a host network proxy.** Initially accept
an approved source ID and structured query, not arbitrary URLs. Allow only
operator-approved HTTPS destinations. Validate resolved IPv4/IPv6 addresses and
bind the checked destination to the actual connection; block local, private,
link-local, metadata and other non-approved routes with network controls too.
Disable redirects initially; any later redirect support must repeat checks at
each hop. The worker receives no controller mount or ambient host credentials;
a private source needs a separate explicit grant. Bound duration, response bytes
and decompression, and treat fetched files as untrusted. This narrow-source
design follows [OWASP's request-forgery guidance](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).

An agent-provider adapter launches a **fresh session** with a context packet and
role tools, records usage and termination, and checkpoints accepted work. It
does not choose the science or grant itself extra tools. The existing agent CLI
may be the first backend only if all its shell/file actions can be confined to
the assigned sandbox. A trusted host-side model gateway can hold provider
credentials; a CLI whose unrestricted host tools can reach those credentials
does not meet the boundary. Prove the actual backend configuration before use.
This design does not assume purchasing a new API service or subscription.

**Read permission is not permission to transmit.** Before runtime model calls,
the operator records approved providers/endpoints and the data classes each may
receive, including licensed/private inputs and locally derived material. Use
the same policy for provider context/tool responses, retrieval queries, request
bodies/URLs, logs and exports. Credential protection alone does not authorize
sending a dataset, notebook or model output to the credential's provider.

For the first build, every input accessible to an externally connected session,
and its derived text, must be approved for every outbound destination enabled
for that session. Build context/tool views on that basis; otherwise deny the
input or disable the destination. Keep sealed scoring in workers without those
channels. Once an agent has read restricted material, a prompt or text filter
cannot reliably prevent paraphrased disclosure. This is one deployment policy,
not human approval per call; unknown classification or destination is denied.

Reserve resources before launching jobs. Include journal and reproduction costs
in the same ecosystem budget, with an allocation that prevents labs consuming
all capacity before their submissions can be checked. Hard wall-time and process
limits must be enforced by the executor, including child processes. If a backend
cannot enforce a requested token/spend limit, record that limitation and resolve
the operating policy with Anthony; do not present an estimate as a hard cap.

Include per-job output bytes, log bytes, file/inode counts and process counts,
plus cumulative ecosystem limits across artifacts, workspaces, receipts, Git
growth and worker logs. Reserve projected growth before admission, enforce
worker limits during execution, and stop admissions at the recovery threshold.
Account for checkpoints and rejected requests too, not only successful runs.

Keep controller database/terminal-receipt capacity outside job-writable storage,
with reserved bytes and inodes for admitted jobs to finish or fail durably.
A full worker volume must not fill this reserve. Bound and rotate job/host logs;
demonstrate the chosen filesystem and runtime enforce these limits rather than
assuming container defaults. [Docker's resource guidance](https://docs.docker.com/engine/containers/resource_constraints/)
is not a substitute for explicit storage and process-limit configuration.

Garbage collection removes only unreferenced drafts/caches under a recorded
retention policy; retained evidence and the only recoverable copy of unfinished
work are protected. When capacity cannot be reclaimed safely, pause and request
an operator storage/retention decision instead of deleting scientific history.

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
Acceptance also does not waive licensing, privacy or public-export restrictions.
Automatic sharing uses previously approved policy; it does not require Anthony
to approve every paper, and cannot invent a grant the policy does not contain.

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
Cached or replayed results still require current authorization before returning
data; a previously successful action ID cannot bypass an expired or revoked grant.

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

Reauthorize export objects and attachments for their intended audience and
destination; an internal accepted paper is not automatically a public download.
Treat text, figures and bundles as untrusted content even when access is allowed.
Initially render escaped plain text, with no submitted HTML or active markup.
Create inert raster figure previews in a restricted offline worker; do not
inline submitted SVG, HTML or other active files under the display's origin.
Disallow automatic remote images/resources and unsafe link schemes. Any later
Markdown renderer needs a restrictive markup/link policy, not raw HTML insertion.

Serve untrusted originals only as explicit attachments from an isolated download
origin, with attachment disposition and no content-type sniffing, without
operator cookies or control endpoints. Keep the public display
on an origin separate from the operator interface, with a restrictive browser
content policy and no route to the controller's privileged tool channel. Opening
a read-only display must not run paper code or fetch a paper-supplied resource.

## 13. First build and the demonstrations that decide it

Build the shortest complete path, in this order. These are proposed slices,
not a replacement for the later implementation plan or a promised calendar.

1. **Records and a fake world.** Minimal CLI, contracts, operational store,
   scientific writer, fake agent backend and deterministic toy harness. Prove
   request identity, object authorization, disclosure decisions, revision checks,
   artifact references, quota reservations and restart behavior
   without buying model calls or running LHM.
2. **A genuinely persistent lab.** Integrate the pinned notebook and context
   packet; checkpoint interrupted work; recover it in a fresh session. Add the
   actual agent backend only with its tool/credential and budget boundaries
   demonstrated under the recorded deployment profile and approved data policy.
   No scheduled operation on an unrestricted host agent.
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
| Object-level access | A cross-lab/cross-ecosystem object, known artifact digest, private attachment or expired grant succeeds through reads, references, search, context, cached responses or export; a permitted same-lab operation must still succeed |
| Filesystem/execution boundary | A lab reaches live policy, sealed data, host credentials, the daemon socket, or arbitrary host execution through another tool |
| Retrieval destination | An approved public source fails, or a local/private target, public-to-private redirect or destination change between validation and connection succeeds |
| Outbound disclosure | A marked restricted datum reaches model payloads, retrieval URLs/bodies, unauthorized logs or exports through context/tool/derived-text paths; a permitted-data request must still succeed |
| Resource exhaustion and cancellation | A hung child process survives job termination, a retry bypasses accounting, or reviews exceed their reserved allocation |
| Storage and process exhaustion | One noisy job, excess processes/files or many valid small jobs exhaust terminal-receipt/recovery capacity; normal work must succeed before exhaustion and after operator recovery |
| Reproduction versus baseline | Agreement with a baseline masks disagreement with the submitted paper's outputs |
| Scientific challenge | The journal accepts the reproducible wrong analysis or rejects the known-sound case without a defensible scientific reason |
| Corrections | A requires descendant is missed, a motivated-by citation alone invalidates work, or resumed context conceals the correction |
| Crash around publication/launch | A paper appears twice, an incomplete record becomes accepted, or an expensive run is duplicated after restart |
| Backup restoration | A lab history or evidence artifact is missing, or restored jobs restart without reconciliation |
| Safe rendering/downloads | Submitted markup/SVG or remote-resource references execute or fetch under the display/operator origin; sound text and raster figures must still display, and permitted originals remain downloadable as isolated attachments |
| Domain separation | A synthetic non-hydrology harness needs to edit controller logic to report a valid quantity or failure |

Future implementation tests invoke the fake-world, contract, recovery, isolation,
and publication cases. Manual backend/model probes supply evidence the fakes
cannot: actual permissions, provider behavior, licensed model execution, and
whole-job cleanup on the chosen host. The operator explicitly enables the
scheduler after reviewing that evidence. No test or gate described here exists
merely because it has been named.

Each denial/exhaustion case needs its permitted or normal control alongside it;
blocking everything is not a passing implementation. Object-access checks cover
the actual read, listing/search, context, reference, publication and export entry
points, not just a unit test of the shared policy function. Disclosure tests
capture actual outbound payloads and inspect derived views/receipts; rendering
tests use a browser to observe execution and network requests. Exhaustion tests
must show a durable refusal and restart/recovery, not merely a killed worker.

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
tool/credential model and usage limits; the exact Linux/Docker profile and LHM
licensing constraints; approved providers, retrieval sources and data classes;
enforceable storage/process limits and recovery reserves;
the crux revision/license and permitted state edits;
and the exact first reference sets, metric definitions and scientific controls.
Their answers may change an adapter or deployment choice, not justify silently
weakening a claimed boundary. If no existing backend meets the budget/isolation
requirements, keep operation manual until Anthony chooses the tradeoff.

Success initially means a recoverable loop and an output Anthony values—not
proof of accumulated knowledge or a reason to refactor Cairn. Once the design
is ready for implementation, move or promote it into assai after Cairn adoption,
carrying the scientific requirements and explicit unknowns with it. This note
creates no assai files and changes no Cairn doctrine, scaffold, or release work.
