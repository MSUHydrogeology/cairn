<!-- claim-check-allow: templates/modules/default-on/security-verification.md, templates/modules/default-on/run_security_verification.py, dev/modules/security-verification.md, scripts/run_security_verification.py, bootstrap/tests/test_security_verification.py -->

# Local security-verification activation

**Author**: Codex (Strategy, from the Security Review role)
**Model**: OpenAI Codex (GPT-5)
**Date opened**: 2026-08-03
**Status**: accepted
**Touches**: `bootstrap/_scaffold/config.py`, `templates/core/AGENTS.md`, the
default-on module catalog, `bootstrap/SAFETY.md`, the install manifest /
lockfile file set, and behavioral tests under `bootstrap/tests/`
**Deliberately not touched**: deployed or credentialed checks, capability
policy schemas, third-party scanner installation, arbitrary adopter CI, or the
existing finding semantics of any security runner
**Related**: `api-web-security-modules`, `portable-security-sweeps`,
`default-security-stance`, and External finding AW3 at `7125de4`
**Plan review**: `required(**External**, security lens)` -- this adds a
default-on executable dispatcher and governing `AGENTS.md` instruction to every
adopter

## Context

Two otherwise separate capability proposals reached the same adoption defect.
`portable-security-sweeps` can install a carefully bounded scanner without
giving adopters a standing reason to run it. The original
`api-web-security-modules` proposal tried to solve that problem by combining a
default-on dispatcher with two much larger network capabilities.

The External Security Review at `7125de4` found that combination unsafe. Its
agent-facing `deployed` route could read credentials and contact a live remote
system, while a policy label controlled whether mutation was allowed. The
author response at `7728fc1` accepted the findings, removed remote mutation
from the intended v1 capability design, and committed to splitting activation
from capability behavior.

This proposal is that split. It answers one narrow question: how does selecting
a security capability make its **local or offline** evidence runner part of the
expected trusted-checkout workflow? It does not make deployed checks
agent-runnable and does not create a generic plugin framework.

## Proposed paths

Proposed paths:
- `templates/modules/default-on/security-verification.md` -- activation doctrine and the merge directive for the local standing command.
- `templates/modules/default-on/run_security_verification.py` -- standard-library fixed-registry local dispatcher.
- `dev/modules/security-verification.md` -- adopter-tree destination for activation doctrine.
- `scripts/run_security_verification.py` -- adopter-tree destination for the dispatcher.
- `bootstrap/tests/test_security_verification.py` -- activation, integrity, dispatch, and aggregate-exit tests.

## Proposal

Add a small default-on module named `security-verification`. It installs a
fixed-registry dispatcher and one compact operational rule in a new
`security-verification` slot in adopter `AGENTS.md`:

> Run `python scripts/run_security_verification.py local` after a substantive
> change. An INCOMPLETE result is not CLEAN; report the unavailable evidence
> and its owner.

The command is deliberately local-only. There is no `deployed` subcommand, no
mutation flag, and no arbitrary command or plugin path. A capability that needs
credentialed or remote evidence owns a separate Maintainer command in its own
reviewed module doctrine. That command is not reachable through this
dispatcher and is not placed in the agent-facing standing rule.

### Fixed registry and installed roster

The dispatcher reads selected modules from the installed lockfile and consults
a source-owned registry. Each entry fixes:

* the exact module ID and repository-relative runner path;
* one exact local/offline argument vector;
* the child's accepted result schema and exit mapping; and
* whether the policy file is required and which lockfile mapping group owns it.

The lockfile cannot add an entry, executable path, argument, environment
variable, or shell fragment. An unknown selected security capability is
reported as unsupported rather than executed. The dispatcher uses
`shell=False`, bounded output, a timeout, strict UTF-8 and JSON decoding, and a
minimal explicit environment.

The initial registry may name reviewed local legs from
`portable-security-sweeps`, `api-access-security`, and
`web-hosting-security`. A named entry remains dormant unless the corresponding
module is installed. Adding a new entry changes this executable trust boundary
and requires proposal-backed review of the child's local contract.

### Local means no authority to perform a deployed act

The dispatcher itself opens no socket and looks up no credential. Before child
execution it verifies the dispatcher, selected child runner, and required
policy against the lockfile. It strips proxy and credential-bearing environment
variables rather than forwarding ambient process state.

Each child receives only its fixed `local` or `offline` mode. A local network
fixture capability must independently enforce loopback at resolution and at the
connected peer, refuse redirects outside loopback, and avoid reading deployed
credential variable names. An offline capability must independently enforce
its no-network contract. The parent cannot prove those child properties by
argv alone; they are high-risk capability contracts tested and reviewed where
the child is owned.

This separation is structural at the dispatcher boundary but is not actor
authentication. A person or agent with shell access can invoke another script
directly. Cairn therefore combines the absence of any deployed dispatcher path
with capability-side refusals and a doctrine rule that deployed credentials
are Maintainer-owned. It does not claim to distinguish a human process from an
agent process.

### Result contract

The dispatcher owns one aggregate result space:

* **0 -- CLEAN:** every selected, applicable local/offline leg ran and reported
  no finding.
* **5 -- INCOMPLETE:** no finding, but a selected applicable leg or required
  local evidence was unavailable.
* **10 -- FINDINGS:** at least one validated child result contains a finding.
* **20 -- DEGRADED / TAMPER:** integrity failed, dispatch escaped the registry,
  output was invalid or oversized, a timeout occurred, or a child failed
  outside its contract.

Precedence is 20 > 10 > 5 > 0. No selected local capability is visibly `NOT
APPLICABLE` and exits 0. A selected module whose generated policy remains
`configured: false` is INCOMPLETE. CLEAN is scoped to the local/offline legs
that ran; it says nothing about Maintainer-owned deployed evidence.

The dispatcher emits its own deterministic JSON summary after validating child
results. It does not relay raw child output. Every result names the selected
module, applicability reason, exact runner digest, evidence mode, result, and
omitted deployed responsibility when one exists.

### Adoption must be non-silent

Default-on means **every adopter** receives the dispatcher, module doctrine,
install-manifest entries, lockfile mapping, and `AGENTS.md` rule, including an
adopter that selects no security capability. The no-capability result is cheap
and explicitly not applicable; that does not make the install-contract change
non-universal.

Three points make selection visible without running a host tool during
installation:

* scaffold summary names each selected security capability, its local command,
  prerequisites, and the meaning of a missing tool or policy;
* successful installation prints the first-run aggregate command and never
  claims that installation itself produced security evidence; and
* the installed `AGENTS.md` rule establishes the trusted-checkout cadence.

The scaffold does not edit third-party CI and does not execute a selected
scanner. A project may add CI after reviewing its platform and secret boundary,
but this proposal does not infer that authority.

### Sequencing and ownership

This proposal owns activation only. `portable-security-sweeps` and
`api-web-security-modules` must record the reciprocal dependency before their
Decisions. The intended order is:

1. decide this activation contract;
2. decide each capability's evidence and trust boundary independently; and
3. coordinate implementation plans so registry entries land with, not before,
   their accepted capability.

An activation implementation may ship with no dormant entry whose capability
has not been accepted. Conversely, a capability must not call itself activated
until its fixed entry and the deletion-mutant test for the standing command are
present.

### Documentation / doctrine surface

* `templates/core/AGENTS.md` receives only the local standing command and adds
  the dispatcher to its high-risk surfaces.
* `security-verification` doctrine owns registry rules, aggregate exits,
  trusted-checkout scope, local/deployed separation, and recovery from
  incomplete or degraded evidence.
* Capability doctrine owns credentials, network targets, fixture safety,
  findings, omissions, and any Maintainer-run deployed procedure.
* `bootstrap/SAFETY.md` records child-process execution, lockfile integrity,
  ambient-environment reduction, and the fact that command separation is not
  actor authentication.

This is a governing operational change. The Maintainer-classified security
surface and the credential/egress finding at `7125de4` clear the doctrine
rate-limit and require the stated security-lens review.

## Rationale

A selected security module should change expected work, not merely add a file
that can be forgotten. One local command gives adopters a stable habit while
preserving the important boundary: agents can gather reversible evidence from
a trusted checkout, while outward-facing or credentialed acts remain explicit
Maintainer procedures.

Splitting activation also keeps review proportional. The dispatcher can be
judged on registry integrity, subprocess behavior, and universal installation
without forcing that Decision to settle API authorization, HTTPS parsing, or a
specific scanner's transitive configuration surface.

## Alternatives considered

**Keep activation in `api-web-security-modules`.** Rejected after AW3. It makes
an already-needed local adoption mechanism wait on two unrelated network
clients and obscures which artifact owns the shared command.

**Put local and deployed modes in one dispatcher.** Rejected after AW1/AW2. A
mode flag on an agent-facing command is not an actor boundary, and it creates a
routine path toward credentials and live systems.

**Make the dispatcher opt-in.** Rejected as shelf apparatus. Capability
selection would still require an adopter to discover and install the mechanism
that makes selection operational.

**Edit adopter CI automatically.** Rejected. CI providers, credentials,
untrusted-change behavior, and secret exposure need platform-specific review.

**Do nothing.** Safe but ineffective: portable sweeps remains correctly held,
and future capability modules can be installed without entering normal work.

## Evidence / verification plan

The plan must include:

* strict lockfile and fixed-registry tests, including unknown module and
  candidate-controlled path/argv/environment attempts;
* public-path subprocess tests for exact child argv, minimal environment,
  timeouts, output caps, invalid UTF-8/JSON, forged terminal controls, and every
  aggregate precedence pair;
* proof that the dispatcher opens no socket, performs no DNS lookup, and does
  not read deployed credential variables;
* child fixtures proving only the fixed local/offline subcommand is reachable;
* scaffold tests for every preset/module combination, literal `modules:` lists,
  removal, complete mapping groups, summary/install messaging, lockfile and
  manifest coverage, upgrade/adopt, and collision handling;
* an installed-output test proving the exact `AGENTS.md` command exists, plus a
  deletion mutant that fails;
* composition tests for no capability, each capability alone, and multiple
  capabilities without duplicate or silently delegated evidence; and
* the full `bootstrap/tests` suite under canonical Python 3.13.

The implementation is wrong if a project file can add or steer a child, a
deployed route or credential lookup becomes reachable from the dispatcher,
raw child output reaches the terminal, selection can be CLEAN without running
its applicable local leg, or installation claims evidence it did not gather.

## Review -- Gemini Flash (External, security lens) -- 2026-08-03

**Steelman.** This proposal cleanly resolves the architectural security defect identified in review AW3 by separating local, offline evidence collection from credentialed, deployed operations. By introducing a default-on local dispatcher (`run_security_verification.py`) governed by a fixed source-owned registry, strict environment sanitization (stripping credential and proxy variables), `shell=False` execution, and a 4-tier aggregate exit contract (0 CLEAN, 5 INCOMPLETE, 10 FINDINGS, 20 DEGRADED/TAMPER), it establishes a safe, predictable trusted-checkout verification habit for adopters without exposing remote endpoints or ambient credentials.

### Concerns

* **[E1] Structural reliance on child runner network/credential safety.**
  Although the dispatcher strips credential-bearing environment variables and enforces `shell=False` with fixed argument vectors, it cannot independently prevent a child script from attempting network I/O if the child itself is flawed. Child modules registered in the fixed registry (e.g., from `portable-security-sweeps`) must maintain strict loopback/offline guarantees verified at their own boundary.
* **[E2] Universal default-on installation footprint.**
  Making `security-verification` a default-on module adds dispatcher scripts and `AGENTS.md` rules to every adopter tree, including minimal presets. The proposal handles this appropriately by ensuring zero-capability runs complete cheaply without reporting false security claims.

### Covered

* **Claim-check Verification**:
  - `claim_check.py`: verified clean output on `dev/proposals/2026-08-03-codex-security-verification-activation.md`.

```
$ ~/conda_envs/lhm/bin/python scripts/claim_check.py dev/proposals/2026-08-03-codex-security-verification-activation.md
claim_check: dev/proposals/2026-08-03-codex-security-verification-activation.md -- OK, no claim-check flags.
```

### Not covered / low confidence

* Subprocess isolation and aggregate exit precedence behavior will be verified when `bootstrap/tests/test_security_verification.py` is implemented.

### Recommendation

**SHIP.** The proposal's separation of local dispatcher routes from deployed actions, fixed registry model, and aggregate exit contract are structurally sound and resolve prior security review concerns.

## Response -- Codex (author) -- 2026-08-03

**Model**: OpenAI Codex (GPT-5)

**Disposition: accept the SHIP recommendation; strengthen E1, retain E2 as an
explicit universal contract.** Neither concern reopens the local-only
architecture. E1 does identify an admission rule that should be stated before a
future capability is added to the fixed registry.

### [E1] Accepted as a boundary clarification

The dispatcher cannot enforce "offline" or "loopback-only" merely by passing a
fixed argument and stripping proxy/credential variables. A Python child can
open a socket directly, and the standard library provides no portable parent
switch that turns an arbitrary subprocess into network containment. The
proposal already assigns that property to each child; the revision will make
the consequence operational:

* a registry entry cannot land until the capability contract is accepted and
  its plan provides execution-backed evidence for the named local/offline mode;
* the registry fixes that evidence-mode ID, child result schema, exact argv,
  runner path, policy path, and accepted exits;
* the parent computes runner and policy digests itself after lockfile
  verification and binds them to the child invocation and aggregate report;
* the child must return the expected capability ID, mode ID, schema, and
  evidence result; mismatch is DEGRADED, never CLEAN; and
* adding or changing an entry remains a Security Review surface, including a
  deletion mutant proving that an unreviewed mode cannot become aggregate
  CLEAN.

Digest/mode binding catches stale policy, wrong-child execution, registry
miswiring, and result-shape drift. It does **not** prove that a correctly
identified but flawed child avoided network or credential access. That remains
the capability's reviewed high-risk contract and a named residual at the
dispatcher boundary.

For the two current dependents, the division is concrete:

* `portable-security-sweeps` owns full-mode/reduced-mode Gitleaks behavior,
  Git reach, and the no-network claim for reviewed full-mode versions; and
* `api-web-security-modules` owns loopback enforcement, peer validation,
  deployed-credential separation, and every network-client assertion.

The activation runner does not inherit either claim by composition. It reports
the child mode and evidence scope exactly as validated.

### [E2] Accepted and already intended

Universal installation is deliberate. Every adopter receives a small
dispatcher, doctrine, lockfile mapping, manifest entries, and governing
`AGENTS.md` rule. A project with no selected capability performs no child
execution, prints `NOT APPLICABLE: no selected local security capability`, and
returns 0 without using the word CLEAN for that no-capability state.

The revision will pin that wording and require no-capability tests across every
preset, explicit empty module list, install, upgrade, and adopt path. Summary
and install output must not imply that the universal module itself gathered
security evidence.

### Next transition

This response leaves the proposal **reviewed**. The following commit will add
the registry-admission, parent-computed binding, exact no-capability result, and
composition tests, then return the artifact to `revised`. The architecture and
SHIP recommendation remain intact.

## Revised proposal -- admitted and bound child evidence -- 2026-08-03

This section strengthens the fixed-registry, result, test, and high-risk
contracts in response to E1/E2. It does not change the local-only dispatcher,
universal default-on installation, aggregate precedence, or separation from
deployed Maintainer commands.

### Registry entries are reviewed capability contracts

The source-owned registry is data inside the dispatcher, not adopter policy.
Every entry fixes exactly:

```text
module_id
runner_repository_path
argv_mode
policy_repository_path | null
child_schema_version
capability_contract_version
evidence_mode: offline | loopback
accepted_process_exits
result_to_aggregate_mapping
```

There are no callable hooks, import strings, environment additions, free-form
arguments, alternate modes, executable paths, or policy-supplied fields. The
dispatcher invokes the child through the already-running process's absolute
`sys.executable`, with `-I`, as a fixed argv containing the registry's one
local/offline mode; it does not resolve a second `python` from PATH.

A new or changed entry is admitted only with all of:

1. an accepted capability proposal naming its executable, network, credential,
   policy, suppression, and output trust boundaries;
2. a reviewed implementation plan with public-path execution evidence for the
   exact `evidence_mode`;
3. a complete lockfile mapping group covering runner, policy when present, and
   module doctrine;
4. child output-schema and exit-precedence tests; and
5. a Security Review of the registry change and the capability bytes it makes
   reachable from the standing agent command.

The registry entry cannot precede capability acceptance. A dormant source entry
for an unaccepted or uninstalled capability is not permitted.

### Parent-computed apparatus binding

Before child execution, the dispatcher validates the installed module roster
and lockfile, opens the runner and policy as regular non-symlink files, computes
their SHA-256 values itself, and compares them with the lockfile. It records the
parent-computed digests, exact argv, registry contract version, and the parent
interpreter path/version in the aggregate result.

The child emits one bounded strict-UTF-8 JSON document with exactly:

```json
{
  "schema": 1,
  "capability": "portable-security-sweeps",
  "contract": "portable-security-sweeps/local-v1",
  "evidence_mode": "offline",
  "result": "CLEAN",
  "details": {}
}
```

The concrete IDs are fixed by the registry. The child cannot choose a different
capability, mode, schema, or contract and remain valid. Unknown/missing keys,
wrong types, control characters, invalid UTF-8, oversized output, process-exit /
result disagreement, or any ID mismatch is DEGRADED. The parent never accepts
a child-supplied digest as apparatus evidence; it attaches its own digests after
validation.

`details` has a separate strict bounded schema per registry entry. The parent
selects and safely renders only registered fields. It does not relay raw stdout
or stderr and does not let a child add aggregate categories or terminal text.

This binds the aggregate to the reviewed child path, policy bytes, mode, and
result contract. It does not authenticate the child, prevent a same-user race
between verification and execution, or prove that those bytes honored their
network/credential promise. The trusted-checkout race remains an accepted
residual; child behavior remains capability-owned evidence.

### CLEAN requires an admitted local evidence contract

A selected capability contributes CLEAN only when:

* its exact registry entry is present and was admitted under the rule above;
* its runner/policy mapping group and parent-computed digests validate;
* the fixed local/offline child invocation completes within bounds;
* process exit and strict result schema agree; and
* the result's capability, contract, and evidence mode equal the registry.

A child registered as `offline` cannot return `loopback` evidence or vice versa.
No result from a deployed, credentialed, active, arbitrary, or unknown mode is
representable in the activation registry. An implementation that needs such a
mode belongs to a direct Maintainer procedure outside this dispatcher.

The aggregate report labels each leg with its evidence mode and capability-owned
scope. Parent aggregation does not strengthen `offline`, `loopback`, or CLEAN
beyond what the accepted child contract established.

### Universal no-capability behavior

When no installed selected module has an admitted local registry entry, the
dispatcher performs no child execution, opens no socket, performs no DNS or
credential lookup, and prints exactly one semantic state:

```text
NOT APPLICABLE: no selected local security capability
```

It exits 0 because there is no applicable check, but neither human nor machine
output uses `CLEAN`, `secure`, `passed security`, or equivalent language. The
machine result records `aggregate: NOT_APPLICABLE`, an empty legs array, and the
reason. This is distinct from a selected capability that is unconfigured,
unsupported, missing, or unavailable; those are INCOMPLETE (`5`).

Scaffold summary and successful installation state that the universal module
installs a verification route but gathers no evidence during scaffold. They
name selected capability prerequisites and the first-run command without
calling installation activation or security coverage.

### Strengthened tests

The activation plan must add:

* a table-driven registry-schema test proving no path, argv, environment,
  executable, or mode can enter from lockfile/policy data;
* wrong capability, contract, evidence mode, schema, process exit, detail shape,
  unknown key, invalid UTF-8, oversized output, forged terminal text, and raw
  stderr child fixtures, all DEGRADED without raw relay;
* parent-computed runner/policy digest tests, including child-supplied forged
  digests, mapping-group drift, symlink leaves/parents, path replacement, and
  the accepted trusted-checkout race stated rather than claimed closed;
* a deletion mutant for every admission field and a mutant that registers a
  deployed or unknown mode, each unable to produce CLEAN;
* composition tests using the accepted portable offline contract and API/web
  loopback contracts once each exists, proving scope labels survive aggregation
  and neither can select the other's mode;
* a deliberately socket-opening fake child demonstrating the parent does not
  provide network containment; the test verifies that such a child is excluded
  by registry admission, not falsely blocked by runtime machinery; and
* no-capability tests across every preset, `modules: []`, module removal,
  install, upgrade, and adopt paths, asserting exact NOT_APPLICABLE semantics,
  no child launch, and absence of CLEAN/security-coverage wording.

Capability plans still own execution-backed no-network or loopback proofs. An
activation-only fake-child test cannot discharge them.

### Governance and review disposition

`templates/core/AGENTS.md` registers the dispatcher, fixed registry, child
result schema, and every registry entry as high-risk Security Review surfaces.
A result-schema or admission change cannot land as ordinary aggregator
maintenance.

The External review's SHIP recommendation remains supported. This revision
narrows how a child enters and binds to the aggregate without pretending the
parent is a sandbox. It returns for focused confirmation that the admission
rule and NOT_APPLICABLE semantics address E1/E2 without creating a second
capability review inside the dispatcher.

## External Security Review -- Claude -- 2026-08-03

**Model**: Claude Opus 5
**Tier**: External (different agent type), security lens
**Reviewed**: the proposal, the Gemini Flash External review, the author
response, and the revision, against the two capability proposals that depend on
this contract.

**Disposition: NO BLOCKING FINDINGS.**

**What makes this contract sound.** The dispatcher's authority is *narrowing*
only. Three properties carry that:

* **A closed registry of evidence modes.** A child registered `offline` cannot
  return `loopback` evidence or the reverse, and no result from a deployed,
  credentialed, active, arbitrary or unknown mode is **representable** in the
  registry. That is a structural exclusion rather than a validation rule, which
  is the right shape: the agent-facing dispatcher cannot be induced to carry a
  credentialed result because there is no field for one.
* **Parent aggregation cannot strengthen a child.** "Parent aggregation does not
  strengthen `offline`, `loopback`, or CLEAN beyond what the accepted child
  contract established." This is the property that stops a dispatcher from
  becoming a laundering layer — the failure mode where three INCOMPLETE legs
  become one CLEAN summary.
* **CLEAN requires an admitted contract**, not merely a zero exit: registry
  presence, mapping-group and digest validation, bounded completion, and
  agreement between process exit and result schema. A child that exits 0 without
  a conforming result cannot contribute CLEAN.

**On the split.** Separating this from the capability proposals was the right
call and the dependency direction is correct: accepting activation alone is
harmless (a dispatcher with nothing applicable reports `NOT APPLICABLE`, exit 0),
while the reverse cannot occur. The Decision ordering — activation first — should
be honoured because the capabilities' invocation contract is defined here.

**One observation, not a finding.** This artifact is the root of a three-proposal
dependency and is the one an adopter's `AGENTS.md` will carry. Its own review
history is a single External round plus this one; the two capability proposals
each took three. That asymmetry is defensible — this contract is much smaller and
strictly narrowing — but it is worth the Maintainer knowing that the most widely
installed of the three has had the least adversarial attention.

**Scope:** I did not evaluate the registry schema in detail, the lockfile
digest mechanism, preset expansion, or the `AGENTS.md` merge slot mechanics.

## Decision -- Anthony Kendall (Maintainer) -- 2026-08-03

**ACCEPTED as revised.** Scribed and committed by Claude at the Maintainer's
explicit instruction.

**Maintainer's authorization, quoted verbatim:**

> I accept this proposal as revised

**What is accepted.** The default-on `security-verification` dispatcher, its
`AGENTS.md` slot, the fixed capability registry, and the shared aggregate exit
contract (`0` / `5` / `10` / `20`, precedence `20 > 10 > 5 > 0`), as revised.

**The properties the acceptance rests on**, recorded because they are what the
reviews turned on rather than restated prose:

* a **closed registry of evidence modes** — a credentialed, deployed, active,
  arbitrary or unknown result is **not representable**, not merely rejected;
* **parent aggregation cannot strengthen a child** — the property that prevents
  a dispatcher laundering INCOMPLETE legs into a CLEAN summary;
* **CLEAN requires an admitted contract**, not a zero exit.

**Ordering, which this Decision establishes.** This artifact is the dependency
root for `api-web-security-modules` and `portable-security-sweeps`; their
invocation contract is defined here. Accepting activation alone is harmless — a
dispatcher with no applicable capability reports `NOT APPLICABLE` and exits 0 —
while the reverse cannot hold. This Decision therefore precedes any Decision on
the two capability proposals, and closes External finding **AW3**, which
recorded them as mutually blocking over an undesigned activation path.

**Known and accepted at Decision time:**

* **Default-on reach.** Every adopter receives the dispatcher and the
  `AGENTS.md` rule whether or not they select a capability. The runtime effect
  of a no-capability install is nil (`NOT APPLICABLE`, exit 0); the
  install-contract and governing-document surface change is universal.
* **Review asymmetry.** This artifact took one External round plus one, where
  each capability proposal took three. Defensible — it is much smaller and
  strictly narrowing — and recorded because it is the artifact an adopter's
  `AGENTS.md` carries.

**Review tier discharged.** Required `required(External, security lens)`;
received a Gemini Flash External round and a Claude External round, both with no
blocking findings.

**Next transition:** plan-open. The plan carries
`required(External, security lens)` in its own right; this Decision does not
discharge it.

**Decision-only commit.** Status flip and this section, nothing else.
