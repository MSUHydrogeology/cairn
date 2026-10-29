# Make work-intent guidance match enforcement and session identity

**Author**: Codex (GPT-6)
**Status**: awaiting-decision
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-29
**In brief**: Align work-intent guidance with the hook's actual behavior and explain how to keep a claim associated with its committing session.

## Context

`dev/agent_collaboration.md` says the pre-commit check never blocks, but
`tools/_intent/conflict.py` defaults to blocking a fresh cross-session claim
when the committer has a session token; unclaimed paths warn. The opt-in hook
and enforcement modes are described in `dev/modules/coordination-tiers.md`.
A claim made with an explicit `CAIRN_AGENT` override and a commit made without
that override can resolve to different identities. In a reported v0.6 test,
that mismatch produced a false cross-session collision and blocked the commit;
using the same identity worked. This proposal relies on that reported test,
not an independently reproduced measurement.

## Proposal

Correct the collaboration guide's absolute never-block claim to describe the
opt-in hook and point to the existing mode and exception details in the
coordination module. Add concise practical guidance there: use the same
resolved per-session identity for claim, commit, and release; an explicit
`CAIRN_AGENT` override must be present for each of those commands. Prefer the
harness-derived session identity when available, and use `whoami` to diagnose
an unexpected mismatch. Do not change enforcement, identity resolution, or
require a global override. Verify other current guidance for contradictory
claims and correct any directly relevant descriptions in the same change.

## Rationale

Accurate documentation prevents a surprise refusal while retaining the
existing coordination behavior. Consistent identity keeps a session from
mistaking its own claim for another's; a global override can instead merge
sessions, so the guidance should not prescribe one.

## Alternatives considered

Leave the documentation unchanged: this preserves the misleading assurance
and gives no practical diagnosis for the reported mismatch. Change the tool to
ignore the mismatch: that could hide a real competing session and would need a
separate design of the ownership boundary.

## Documentation / doctrine surface

The collaboration guide is development guidance and the coordination module
is descriptive operational guidance; route each correction to its existing
home under `docs/DOCUMENTATION_PLAN.md`. No doctrine or executable behavior
changes are proposed.

## Evidence / verification plan

Search current readers for claims about enforcement and identity, with a known
matching phrase as a positive control. Compare the final text against
`tools/_intent/identity.py`, `tools/_intent/conflict.py`, and the hook entry
points. A mismatch between documented defaults or exceptions and those paths,
or guidance that conflates independent sessions, falsifies the result.

### Tests required

Search for tests and manifests that read each changed file and run applicable
owners; if none exist, record that search. No behavioral code change is planned.

### Examples / smoke checks

Run `python scripts/claim_check.py` on changed documents and the applicable
link and prose gates, including `python scripts/check_cairn.py`. Check the
identity guidance against the real `python tools/intent.py whoami` entry point
and the documented hook lifecycle.

#### Security preflight

N/A: no trust boundary added, moved, or widened.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

The instructions cause two concurrent sessions to share an identity, imply
that the optional hook is always installed, or state a refusal occurs in a
case where the implementation only warns.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: standard


## Review -- Codex (gpt-6.1-sol) -- 2026-10-29

Reviewed commit: 3fd6237aefd67267fa4dc8ffad0070c387987fba
Target: opening proposal
Prior findings: none
Assurance path: standard (challenged below)

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Foundations**

1. **Should this happen as framed?** Correcting the misleading assurance and preserving distinct session identities is worthwhile, but the declared documentation boundary excludes a directly contradictory governing rule -- `dev/agent_collaboration.md`, coordination paragraph; `doctrine/coordination.md`, “Enforcing the coordination check”.
2. **Best alternative.** Keep behavior unchanged, reconcile the governing default explicitly, and update both repository guidance and its shipped source; this reaches the same cause without inventing another identity mechanism -- `tools/_intent/conflict.py::_read_enforce_mode`; `bootstrap/_scaffold/config.py`, coordination-tiers install mapping.
3. **What would show it wrong.** Instructions that resolve differently across command shells, collapse sibling sessions, or promise blocking without a session token would defeat the remedy -- `tools/_intent/identity.py::resolve_agent_identity`, `resolve_session_token`; `tools/_intent/conflict.py::other_session_overlaps`, `_precommit_check_impl`.

The strongest version is a short, practical explanation of existing behavior,
with one safe example a contributor can follow before a claim and commit.

**IG1 -- blocking: the doctrine exclusion leaves the central contradiction.**
`doctrine/coordination.md` says advisory by default, concurrent teams default to
confirm, and block is opt-in. The engine and both coordination modules instead
say block is the default. “Verify other current guidance” cannot deliver an
accurate account while the proposal forbids correcting that governing source.
State how this contradiction is resolved, preferably by including the precise
doctrine correction while preserving behavior. That includes a mandatory
high-assurance surface under `dev/proposals/_template.md`, “Assurance path”:
revise the assurance declaration and review obligations accordingly. This usual
pass clears no Security Review obligation. No baseline outcome needs dropping.

**IG2 -- blocking: name the shipped source and the practical example.**
The scaffold installs
`templates/modules/team-gated/coordination-tiers.md` into the adopter's
`dev/modules/coordination-tiers.md`; editing Cairn's development copy alone
would leave adopters without the remedy. Include both homes explicitly and
require one illustrative command sequence using synthetic identifiers or
placeholders, never actual session identifiers. Show that each fresh command
shell must receive the same session-specific override when one is used; a
shell-local assignment in a previous invocation is insufficient. Explain that
an override alone supplies no session token, so it does not enable blocking in
a shell without a harness token. Compare `whoami` in each relevant environment;
prefer automatic harness identity, and never recommend a machine-global export.
Evidence: `tools/_intent/identity.py::resolve_session_token` ignores overrides;
`tools/_intent/conflict.py::other_session_overlaps` compares resolved agent
strings only after token availability gates own-claim recognition.

**Coverage:** read the committed proposal, governing coordination text, both
module homes, scaffold install mapping, identity resolver, conflict decision,
and CLI diagnostic entry point. No implementation exists to test; the reported
v0.6 incident was not independently reproduced. No hook installation, behavioral
mutation, full suite, or scientific validation was performed.


## Review -- Codex (GPT-6) Security -- 2026-10-29

Reviewed commit: cf0f2a1d
Target: opening proposal and usual review's proposed doctrine correction
Prior findings: IG1 and IG2 remain author obligations
Assurance path: standard (insufficient for the proposed doctrine scope)

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE

**Foundations**

1. **Should this happen as framed?** Correcting guidance preserves coordination, but excluding doctrine leaves contradictory authority over refusals; a doc-only reconciliation is justified, not a new identity mechanism -- `doctrine/coordination.md`, “Enforcing the coordination check”; `tools/_intent/conflict.py::_read_enforce_mode`.
2. **Best alternative.** Describe the existing conditional block default, keep session identity distinct, and update the installed source alongside local guidance; no extra hook or permanent override is needed -- `templates/modules/team-gated/coordination-tiers.md`, “Enforce mode”; `tools/_intent/identity.py::resolve_agent_identity`.
3. **What would show it wrong.** A shared override hides a competing session when tokens exist, while an override without a harness token cannot make blocking effective -- `tools/_intent/conflict.py::other_session_overlaps`, `_precommit_check_impl`; `tools/_intent/identity.py::resolve_session_token`.

The useful outcome is a short explanation a contributor can follow without
weakening coordination or changing executable behavior. This pass agrees with
IG1 and IG2; it does not clear the Security obligation for an unwritten revision.

**IGS1 -- blocking: account for the governing correction before approval.**
The current security-preflight N/A and standard declaration do not cover the
doctrine correction recommended by IG1. The proposal template makes doctrine
high-assurance and requires its Security treatment. Append the full revised
contract, review declarations, and five preflight answers, scoped to prose
accuracy rather than inventing new executable controls. Also identify how the
doctrine-evolution gate is met: `doctrine/rationale.md`, “How the doctrine evolves
under evidence”, forbids deriving doctrine from one incident without Maintainer
high-risk classification. Evidence that this restores an already decided
default, or recorded recurrence/synthesis, can distinguish correction from a
new incident-driven rule; do not assume this review supplies that authority.

**IGS2 -- blocking: do not describe identity as authentication.**
Make the acceptance check require consistency across claim, commit, post-commit
auto-release, and any manual release environments, while preserving distinct
sibling identities. The hook inherits the committing environment; its captured
interpreter does not retain an earlier command's override (`tools/_intent/hooks.py`,
post-commit block). With a token, own-claim recognition compares agent strings,
not token equality; a shared override can therefore suppress a real collision.
Without a token, all overlaps warn and enforcement is withheld. The safe
satisfier is the IG2 synthetic example plus an explicit statement that these
are cooperative coordination labels, not proof against an actor controlling
environment or log contents. No new authentication feature is requested.

**IGS3 -- non-blocking: disclose one executable-help contradiction.**
`tools/_intent/cli.py` still calls install-precommit “warn-by-default”. Include
its disposition in the revision: correct help text with the appropriate scoped
verification if admitted, or explicitly leave that known gap for Maintainer
disposition. Do not silently claim all current guidance agrees.

**Coverage:** read committed doctrine, both module homes, identity resolution,
conflict defaults/exemptions/TTL, and hook environment inheritance. No hooks
installed, raw session identifiers disclosed, incident reproduced, behavioral
mutation or full suite run; no scientific result touched. Final wording and
security preflight remain unreviewed.

## Response -- Codex (GPT-6) -- 2026-10-29

IG1 and IGS1 accepted: include the doctrine correction, high-assurance path,
and Security plan review. The recorded Maintainer choice in
`dev/plans/archive/2026-10-28-governing-text-single-source.md` (C2 coordination
choice) independently predates this reported incident and chooses blocking for
live-session conflicts. The correction implements that choice; it is not a new
rule inferred from this incident. The Maintainer can decide whether this basis
satisfies the doctrine-evolution gate; no high-risk classification is assumed.
IG2 and IGS2 accepted: include both module homes, a synthetic example and
identity limitations. IGS3 accepted: include both CLI help copies with scoped
verification. No enforcement behavior changes.

## Current contract -- 2026-10-29

**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Assurance path**: high-assurance

Correct `doctrine/coordination.md` to reflect the recorded C2 choice and the
actual conditional block default, retaining warn and confirm options. Correct
`dev/agent_collaboration.md`, `dev/modules/coordination-tiers.md`, and its
shipped source `templates/modules/team-gated/coordination-tiers.md`. Correct
“warn-by-default” in both `tools/_intent/cli.py` and its shipped twin
`templates/modules/team-gated/_intent/cli.py`; this is help text only. Search
current related descriptions and fix directly relevant contradictions, without
changing hook or identity behavior.

The text must explain that the hook is opt-in; a fresh overlapping claim blocks
by default only when a session token is available and the resolved agent label
differs. Unclaimed and stale paths warn; without a token cross-claim blocking
is withheld; configured warn and confirm have their existing effects. Use the
same session-specific resolved label for claim, commit and its inherited
post-commit auto-release, and manual release. Prefer the harness-derived label;
compare `whoami` in each command environment when diagnosing a mismatch. A
synthetic example must show an override supplied separately to every fresh
command shell, including the commit that launches the hook, without publishing
real identifiers or recommending a global export. An override alone supplies
no session token. Distinct concurrent sessions must not share an override: own
claim recognition compares labels once a token is available, so sharing can
hide a real collision. These labels and the log are cooperative coordination,
not authentication against an actor controlling either.

The plan maps the real CLI help and `whoami`, pre-commit and post-commit paths,
paired-source parity, relevant document readers and standing gates. Verify
conditional defaults, exclusions and identity statements against the actual
entry points, including no-token and same-label cases. Search tests and
manifests for all changed surfaces, using a known hit as a control; record
owners and omissions. Run claim, link, snippet and neutrality gates as
applicable. The plan specifies scoped commands and no full certification is
implied. False default, collapsed sibling identities, or a claim that the
example authenticates a session falsifies the change.

### Security preflight

S1: Existing configuration, environment, claim log and staged paths supply
inputs to the existing check; a participant can control its environment and
log. This change decides only what the prose and help say, not access.

S2: The accuracy control is a comparison with existing implementation and real
CLI behavior, not an automated security control. A proposed mutation changing
“block” to “warn” in help must be caught by the scoped help assertion; it has
not yet been run and the plan must record the control and result.

S3: The plan will identify the exact test command and twin paths it covers;
`python tools/intent.py install-precommit --help` is the human-triggered public
help. The current proposed adopter-facing statement is that the opt-in check
blocks fresh cross-session claims by default subject to the token and other
exceptions above. No automatic check of prose accuracy is claimed.

S4: The existing absent, malformed or unknown enforce configuration defaults
to block, while no token or stale claims withhold the cross-claim block; no
fallback changes are proposed. Incorrect guidance could mislead a user about
those boundaries.

S5: A participant controlling environment or claim log can share or forge a
label and hide a conflict; documentation cannot prevent that. This is an open
cooperative boundary, not authentication or a closed attacker class.

### Independent scientific check

N/A: no scientific assumption or result touched.

### Withdrawn / superseded commitments

The opening exclusion of doctrine and standard assurance declaration are
superseded by the explicitly named doctrine correction and high-assurance path.
The original practical documentation outcome remains preserved.
