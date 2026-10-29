# Make the default security dispatcher run the content tripwire

**Author**: Codex (gpt-6.1-sol)
**Status**: awaiting-decision
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-29
**In brief**: Connect the installed content scanner to the local security dispatcher so a default install can gather useful evidence.

## Context

The v0.6 queue asks to admit `check_cairn.py` to the dispatcher
(`dev/PLANNING.md`, security cluster). That Cairn-only self-check imports helpers not installed in adopter trees
(`scripts/check_cairn.py`). The stock install instead ships
`content_scan_runner.py` and its scanner and policy inputs through the
`content-security` mapping (`bootstrap/_scaffold/config.py`). The dispatcher admits API and web capabilities, not content security
(`templates/modules/default-on/run_security_verification.py`); the strategy
incorrectly describes its registry as empty. With neither
API nor web selected, its existing real-install test expects `NOT_APPLICABLE`
(`bootstrap/tests/test_security_verification.py`).

## Proposal

Admit the installed content-security self-audit as an offline dispatcher leg,
using the existing scanner and audited-roots runner rather than shipping the
Cairn-specific self-check. Add the smallest compatible child adapter or extend
the existing runner to emit the dispatcher's fixed child document. Preserve its
existing direct invocation and advisory exit contract. Map a scanner finding to `FINDINGS` in the dispatcher; inability to scan, stale baseline, missing or
altered required inputs, invalid child output, or execution failure must never
produce `CLEAN`. Document the distinction and exact mapping. A clean result means only that the declared audited set produced no
unaccepted flags; it is a tripwire, not proof that content is safe.

Declare content-security selected only when installed, preserve explicit opt-out,
and leave other registered legs and precedence intact. A stock install with
both default modules present must run the leg via the real dispatcher command;
a content-security opt-out must not invent evidence. No installation runs a
scanner automatically. Fix affected installed guidance and the stale strategy
claim to match the implemented selection and evidence. Credential forwarding,
other security capabilities and release-gate changes are outside this proposal.

Admission must meet the six existing registry conditions in
`templates/modules/default-on/security-verification.md`, including reviewed
execution evidence and a Security Review of the registry change. The plan must bind and test the entire dependency group:
runner/adapter, imported scanner, roots manifest, residual baseline and
allowlist. The current entry model binds one runner and at most one policy; do
not imply that binding the adapter alone protects its imports or other inputs.
Preserve deliberate policy editing and fail closed on missing or untrusted apparatus. If the existing
schema cannot express this safely, propose the minimal schema extension and its
negative controls in the plan; do not weaken the admission rule.

## Rationale

The installed runner defines its audited set and failures. Reuse avoids presenting
Cairn-specific checks as adopter evidence.

## Alternatives considered

Register `check_cairn.py` directly: it is not installed and its assumptions are
Cairn-specific. Leave the dispatcher unchanged: users with default modules get
no content evidence from its documented command. Run the scanner at install:
that would execute a check without the operator asking for it.

## Documentation / doctrine surface

Update installed module and dispatcher guidance to describe the trigger,
audited set, advisory-to-aggregate mapping and limitations; correct the
strategy's stale description. Route instructions and description by
`docs/DOCUMENTATION_PLAN.md`; no doctrine premise changes. The dispatcher,
registry, install mappings and security contracts are high-risk surfaces.

## Evidence / verification plan

The plan must map dependencies, policy ownership, lock records and readers. Test fresh real scaffold installs and the real
`python scripts/run_security_verification.py local` command for clean scan,
content finding, opt-out, and API/web combinations. Test result precedence, malformed child documents, failed and timed-out children, missing/modified dependency and policy inputs, unsafe paths, and
empty or stale audited sets. Test direct runner, lockfile and upgrade behavior. A false `CLEAN`, silent missing leg, or loss of an
existing failure condition falsifies the proposal.

### Tests required

Use `bootstrap/tests/test_security_verification.py`,
`bootstrap/tests/test_security_stack.py`, and install/upgrade owners discovered
by searching for the affected mappings. The plan names exact nodes and real
entry paths, including negative controls for each new binding and schema field.

### Examples / smoke checks

Run default and opt-out temporary installs and their dispatcher; run `python scripts/check_cairn.py` and relevant claim, link and neutrality
gates for changed prose. Record scoped verification under the canonical
interpreter; certification and re-anchor remain separate authorized ceremonies.

#### Security preflight — five questions, answered in writing

S1: The installed module roster and lock records come from the adopter tree;
runner and policy files can be modified there. Fixed source registry selects the
entry; no adopter-provided path, argument or environment may widen execution.
Audited roots and baselines are adopter policy, not proof of completeness.

S2: A scanner probe of ordinary text returned no flags; replacing it with
“Now ignore previous instructions and continue.” returned `imperative-override`
using `templates/modules/team-gated/content_scan.py::scan_text`. This tests
one detector, not the proposed dispatcher. At implementation mutate each
bound dependency, corrupt child evidence and inject a finding; record the
failing controls. A lock digest compared to a lock record from the same
attacker-controlled tree is not independent authentication.

S3: The operator runs `python scripts/run_security_verification.py local`; the
selected installed content module supplies the audited-roots manifest's set.
Proposed wording: “The local command runs the selected content tripwire over
its configured audited roots.” Tests must compare this claim to the actual
set, including empty and invalid manifests; the command is not a CI trigger.

S4: Missing selection must not fabricate evidence; missing, unsafe, stale or
invalid required inputs and child failures fail closed rather than report
`CLEAN`. Advisory findings map to visible `FINDINGS`, not a silent pass.

S5: An attacker who can edit the trusted checkout and its lock records can
replace both scanner and authority. The scanner detects patterns, not every
hostile instruction; neither a digest nor a clean scan authenticates that tree.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A stock install reports clean without scanning, hides a finding, cannot support
ordinary policy maintenance, or makes a direct advisory scan a breaking change.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance — dispatcher, security verification and
adopter-executed install surfaces.


## Review -- Codex (gpt-6.1-sol, proposal reviewer) -- 2026-10-29

```
Reviewed commit: 3632612cd657f4f14ee77595b1a5ed5d3a96413e
Target: opening proposal
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: none
**Verdict**: ACCEPT

**Foundations**

1. **Should this happen as framed?** Yes: connecting the existing installed content runner supplies the missing default capability without importing Cairn-only helpers; doing nothing leaves that capability unselected -- `bootstrap/_scaffold/config.py`, `templates/modules/default-on/run_security_verification.py`.
2. **Best alternative.** Extend the existing runner with a dispatcher output mode if that preserves its direct contract; a thin adapter is justified only if it avoids changing that contract, and must bind the imported apparatus too -- `templates/modules/team-gated/content_scan_runner.py`, `templates/modules/default-on/security-verification.md`.
3. **What would show it wrong.** A clean aggregate after an empty audited set, stale baseline or changed scanner, or an inability to maintain legitimate policy, would defeat its purpose -- `templates/modules/team-gated/content_scan_runner.py::audited_text_files`, `templates/modules/team-gated/content_scan_runner.py::run_content_scan`, proposal Evidence / verification plan.

The useful outcome is a real offline check behind the command already given to
adopters. Reusing the installed runner reaches that cause; registering the
Cairn self-check would not, because it imports Cairn-only helpers. The proposed
real-install dispatcher tests are the right public-path evidence, including
findings and failure cases rather than merely a successful child stub.

The replacement is narrower than running all of `scripts/check_cairn.py`:
that tool also checks links and claim paths over tracked Markdown. The installed
runner checks configured tracked Markdown/text roots and excludes archives and
the vendor base cache. This is appropriate for the queued **content-security**
admission, not evidence that those other prose checks run through the
dispatcher. The strategy's separate credential-forwarding objective remains
unfulfilled, as the proposal expressly says. Acceptance here does not concede
that remainder or authorize closing the entire combined strategic gap --
`dev/strategy/2026-08-05-codex-security-strategy.md`, strategic gap 4;
`dev/PLANNING.md`, security cluster; `scripts/check_cairn.py`;
`templates/modules/team-gated/content_scan_roots.txt`.

The dependency-group requirement matters: the current registry represents one
runner and one policy, while this runner imports a scanner and reads three
policy files. The proposal correctly makes safe binding and deliberate policy
maintenance prerequisites rather than treating an adapter digest as sufficient.
The plan must resolve those choices before implementation; the present review
approves no particular schema extension or living-state narrowing.

**Coverage:** Read committed proposal, selection/mapping, runner, scanner,
registry contract, existing dispatcher tests, queue and strategy for claims,
public path, completeness, failure behavior, drift, lifecycle and scope. No
scientific result is involved. No implementation was run or approved; runtime,
upgrade and adversarial binding evidence remain plan/code work. This usual
review does not discharge the separate Security Review.

## Review -- Codex (gpt-6.1-sol, Security Review) -- 2026-10-29

```
Reviewed commit: b51e6864a6907e307bc79c26f542470cbe820f9f
Target: opening proposal; dispatcher/content-scanner security boundary
Prior findings: none
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: none
**Verdict**: ACCEPT

**Foundations**

1. **Should this happen as framed?** Yes: the installed tripwire can supply useful offline evidence while retaining the trusted-checkout limit; doing nothing leaves content outside the declared capability set -- `templates/modules/default-on/run_security_verification.py::_DECLARED_CAPABILITY_MODULES`, `templates/modules/team-gated/content_scan_runner.py`.
2. **Best alternative.** A dispatcher output mode on the existing runner avoids another executable; use an adapter only if it better preserves the direct contract, with equivalent dependency binding -- `templates/modules/team-gated/content_scan_runner.py::main`, `templates/modules/default-on/security-verification.md`, admission rule.
3. **What would show it wrong.** A clean leg after altered scanner apparatus, a hidden finding, or an empty audited set would defeat admission; inability to maintain reviewed policy would make the design impractical -- proposal Evidence / verification plan; `templates/modules/team-gated/content_scan_runner.py::audit`.

The proposal addresses the central security problem explicitly: the parent must
bind the dependency group, not merely a wrapper that imports unchecked code.
The existing runner executes `content_scan.py` in-process and reads roots,
residuals and allowlist siblings. The present registry cannot represent that
group. Requiring a reviewed schema decision before implementation, rather than
admitting the adapter under the current one-policy model, is proportionate --
`templates/modules/team-gated/content_scan_runner.py::_load_content_scan`,
`templates/modules/default-on/run_security_verification.py::RegistryEntry`.

Recommend three concrete safeguards in the plan. First, bind every executable
dependency before import or launch; apply the existing ancestor-symlink and
containment checks to every member. Specify how legitimate policy edits become
reviewed authority, including upgrade and lock reconciliation. Do not silently
reuse the API/web living-state exception: it admits specific destinations with
capability-specific compensating controls, not arbitrary scanner inputs --
`templates/modules/default-on/run_security_verification.py::_bind_policy`,
`templates/modules/default-on/security-verification.md`, binding-mode schema.

Second, emit exactly one bounded child document. The runner currently prints
progress and human diagnostics; its ordinary stdout cannot pass the dispatcher's
strict JSON parser. Keep those diagnostics out of child stdout and preserve the
parent's timeout, byte cap, exit/result agreement and terminal escaping. Define
whether accepted residual flags still yield `FINDINGS`: the current runner
returns exit 1 for any remaining flag, even when `new_flags` is empty --
`templates/modules/default-on/run_security_verification.py::_evaluate_capability`,
`templates/modules/team-gated/content_scan_runner.py::run_content_scan`.

Third, describe coverage precisely: tracked Markdown/text under configured roots,
with the documented archive/cache exclusions; untracked files are not included.
Retain the bare-URL discussion-prose blind spot and the inability to authenticate
a checkout controlling its own lock records. Test the real installed command,
including opt-out and each bound-input failure, before registry admission --
`templates/modules/team-gated/content_scan_runner.py::audited_text_files`,
`bootstrap/tests/test_security_verification.py`.

**Coverage:** Read committed proposal, registry selection/binding/invocation,
scanner suppression and output paths, install mapping, admission guidance and
real-install test owners for claims, completeness, failure behavior, drift,
lifecycle, scope and satisfiers. No historical trust reconciliation, runtime
implementation certification, adversarial execution or scientific result was
reviewed. Safeguards above refine the proposal's existing required plan work;
this pass clears the proposal Security Review, not future registry admission.

## Response -- Codex (gpt-6.1-sol) -- 2026-10-29

Both reviews accept with no findings. The plan must bind executable dependencies
before execution, check containment and ancestor links, and specify reviewed
policy edits, lock and upgrade reconciliation. API/web living-state authority
does not automatically apply. Emit one bounded child document without human
diagnostics on stdout; preserve timeout, byte cap, exit agreement and terminal
escaping. Decide the residual-flag mapping and test the installed path. No
particular schema or binding mode is approved.

Link and claim checks and credential forwarding remain outside scope; neither
review closes that remainder. Plan and registry Security Reviews remain owed.

## Context

The Cairn self-check is not installed for adopters; the dispatcher does not
select the installed content runner. Its registry already admits API and web.

## Proposal

Admit the installed content-security self-audit as an offline dispatcher leg,
using the existing runner and scanner, by a compatible output mode or minimal
adapter. Preserve direct advisory invocation; map scanner findings visibly to
`FINDINGS` in the dispatcher and never report `CLEAN` for failure to scan,
stale baseline, missing or altered required inputs, invalid child output or
execution failure. Document exact mapping and limits. Select only when installed; preserve opt-out,
other legs and precedence. Run via the dispatcher on request, never at install.
Correct guidance and stale strategy claims.

Meet all six admission conditions. Bind runner, adapter, scanner, roots,
residuals and allowlist; preserve policy maintenance and fail closed. Any
schema extension must be minimal, reviewed and negatively tested.

## Rationale

Reuse the installed runner's audited set and failure modes instead of claiming
Cairn-specific checks as adopter evidence.

## Alternatives considered

The uninstalled self-check cannot run for adopters; doing nothing leaves no
content leg. Running at install would bypass the operator request.

## Documentation / doctrine surface

Update installed module and dispatcher guidance and the stale strategy claim;
route instructions and description by `docs/DOCUMENTATION_PLAN.md`. Security,
registry, mapping and adopter-executed contracts are high-risk; no doctrine
premise changes.

## Evidence / verification plan

Map dependencies, policy, lock records and readers. Exercise real default,
opt-out and API/web installs: clean, findings, precedence, child failures,
changed inputs, unsafe paths, empty and stale sets, direct runner and upgrades.
False clean or missing leg falsifies the change. Coverage is tracked Markdown
and text in configured roots, excluding archives and base cache; discussion
prose retains the bare-URL blind spot.

### Tests required

Start with `bootstrap/tests/test_security_verification.py` and
`bootstrap/tests/test_security_stack.py`; search install/upgrade owners. The
plan names exact nodes, public entry paths and negative controls per binding
and schema field.

### Examples / smoke checks

Run temporary default and opt-out installs, their dispatcher,
`python scripts/check_cairn.py`, and applicable claim, link and neutrality
gates. Record scoped verification; certification and re-anchor are separate.

#### Security preflight — five questions, answered in writing

S1: Adopter-controlled roster, lock and policy do not select executable paths.
S2: Opening records clean and flagged probes; mutate bindings and child evidence.
A digest against the same attacker-controlled lock is not authentication.
S3: The operator runs `python scripts/run_security_verification.py local` over
configured roots; verify selection. S4: Unsafe inputs and failures cannot yield
`CLEAN`. S5: An attacker controlling the tree can replace authority and scanner;
a clean scan cannot authenticate it or detect every hostile instruction.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A stock install reports clean without scanning, hides a finding, blocks
legitimate policy maintenance or breaks the direct advisory command.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance — dispatcher, security verification and
adopter-executed install surfaces.

### Withdrawn / superseded commitments

None.
