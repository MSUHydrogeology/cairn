# Make the default security dispatcher run the content tripwire

**Author**: Codex (gpt-6.1-sol)
**Status**: awaiting-review
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
