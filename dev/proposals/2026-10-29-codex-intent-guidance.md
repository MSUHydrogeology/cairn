# Make work-intent guidance match enforcement and session identity

**Author**: Codex (GPT-6)
**Status**: awaiting-review
**Review**: usual
**Plan review**: required(Internal)
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
