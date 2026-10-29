# Prepare the handoff before the user runs pruning

**Author**: Codex gpt-6.1-sol
**Status**: revising
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-29
**In brief**: Prepare and record the handoff first, then give the user one command to prune when other sessions are quiet.

## Context

The Maintainer's requested sequence is recorded in `dev/PLANNING.md` under
“Handoff skill hands the prune to the user.” Today the session-end skill runs
`--handoff` before its judgment steps, and `tools/session.py` prunes reflections
and intent records before it emits the capture and rate-limit prompts. The
existing dry run prints a mutation manifest but does not emit those prompts.
The intent prune's lock does not protect against live claim/release appenders;
the skill therefore requires other sessions to have ended.

## Proposal

Add a non-destructive full-handoff preparation mode to the session CLI and its
shipped twin, `templates/skills/_lib/session.py`. It scaffolds and surveys as
usual, surfaces intents, emits the existing capture and rate-limit prompts and
the prune preview, and never prunes. Keep `--handoff` as the existing guarded
user-run prune command, including its marker, lock, containment and intent
safeguards. Do not rely on a persisted readiness flag: the user must run it
only after other sessions have ended, since a quiet observation can become stale.

Revise the canonical skill and `templates/skills/session-end/SKILL.md` so the
designated owner runs preparation, fills the reflection, performs the scrub,
note, custom steps and handoff commit, checks for unreleased claims newer than
the claim TTL and confirms no session is still appending, and then presents
`CAIRN_HANDOFF_OWNER=1 python tools/session.py session-end --handoff` to the
user. If readiness cannot be established, report the unresolved condition and
still give the command with the condition to satisfy before running it; do not
claim that a ledger scan proves there are no live appenders. Reflection-only
remains the default. Align `doctrine/session-routines.md` with the sequence
and preserve its manual invocation and single-owner guarantees. The agent does
not run the prune. The user's command may repeat non-destructive output; it must
not imply that the user's run completes the owner's judgment steps.

## Rationale

Preparation exposes the evidence needed for judgment before deletion and lets
the user run the existing single command. Leaving the command guarded preserves
existing callers and avoids presenting a check made earlier as a durable lock.

## Alternatives considered

Changing skill prose alone loses the full-handoff prompts until after the user
prunes. Running the existing command as the agent reverses the requested order.
Adding a readiness token would not prevent another session from starting later.

## Documentation / doctrine surface

The skill and shipped twin are procedure; `doctrine/session-routines.md` is the
governing methodology. The deliberation remains here. Update CLI help and
messages and any actual readers found during implementation; preserve twin
parity and the install contract. Apply the doctrine evolution gate.

## Evidence / verification plan

### Tests required

Exercise the real CLI in temporary repositories: preparation emits prompts and
preview without deleting old reflections or rewriting intent records; the
reflection-only default remains non-destructive; guarded `--handoff` still
prunes eligible records, refuses without its marker, and preserves lock and
containment protections. Cover a fresh unreleased claim and a changed intent log,
and show preparation cannot be mistaken for a guarantee of future quiet.
Map owners and consumers in `bootstrap/tests/test_session_routines.py`,
`bootstrap/tests/test_session_failsafe.py`,
`bootstrap/tests/test_session_writes_contained.py`, skill and install tests,
and both CLI copies; the plan must specify exact nodes and other readers found.
A preparation run that mutates either prune target falsifies the change.

### Examples / smoke checks

Run claim, link, neutrality and applicable skill/install checks. In a disposable
repository walk the skill sequence through preparation, capture and the
user's command; never prune the working repository. Test CLI twin parity and
record the canonical interpreter and change-specific verification.

#### Security preflight — five questions, answered in writing

* **S1:** The local operator and repository supply arguments, marker, paths,
  reflections and intent log; the log reports its own claims and cannot prove
  absence of live appenders.
* **S2:** A preparation test must fail if either prune helper is invoked or
  old fixture contents change; mutation has not yet been run. Existing guarded
  pruning tests must fail when the marker or containment check is bypassed.
* **S3:** The eventual plan maps the CLI tests and skill/install checks to their
  commands and inputs; the skill must describe the same preparation and user
  command those tests exercise. This is a proposed contract, not a check run now.
* **S4:** Missing or uncertain readiness blocks a claim of readiness; it does
  not grant permission to prune. Existing path, marker and lock refusals remain
  fail-closed. A later appender remains possible after any check.
* **S5:** A local actor who controls the repository or starts an appender after
  inspection can still race the user-run prune. This proposal does not claim to
  serialize ordinary appends; the user must establish a quiet session.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Preparation deletes or rewrites a prune target, skips a needed capture prompt,
or the user's command loses a current safeguard; the owner cannot establish
quiet without pretending that the intent ledger proves it.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance


## Review -- Codex gpt-6.1-sol -- 2026-10-29

```
Reviewed commit: 828ba4a1857912f236235055503bb7edebe5795f
Target: opening proposal, Context through Assurance path
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: none
**Verdict**: ACCEPT

**Foundations**

1. **Should this happen as framed?** Yes: capture must precede deletion, and the user should receive the existing prune command after the owner finishes the handoff. The recorded request and current order disagree -- `dev/PLANNING.md`, “Handoff skill hands the prune to the user”; `tools/session.py::_do_full_handoff`.
2. **Best alternative.** Share the existing survey, preview and prompt helpers between preparation and pruning; a prose-only reorder cannot expose the capture prompt through the current dry run, which returns before it. This preserves one agent task sequence and one user command -- `tools/session.py::cmd_session_end`, `tools/session.py::_do_full_handoff`; `.agents/skills/session-end/SKILL.md`, sections 1–2.
3. **What would show it wrong.** Preparation mutating a prune target, or the skill treating a quiet ledger as proof of no live appender, would defeat the premise. The proposed temporary-repository CLI checks and explicit conditional handoff target those failures -- this proposal, “Tests required” and “Proposal”; `.agents/skills/session-end/SKILL.md`, “Run the full handoff last”.

The strongest feature is the split at the actual responsibility boundary: the
agent completes capture and the durable handoff, then the user performs the
existing destructive operation. Preparation earns its existence because the
current dry run omits the evidence used for judgment. Keeping `--handoff`
compatible avoids another prune interface and another user ceremony. Repeating
read-only output is acceptable provided its completion message does not send
the user back through the owner's already completed tasks.

The readiness wording is appropriately limited: fresh claims matter, but an
old or empty ledger cannot establish that no session will append. Giving the
command with an unresolved condition preserves the requested handoff without
inventing a readiness token or granting permission to run it early. The
proposal retains manual invocation, reflection-only default, single ownership,
containment, marker and lock protections. Acceptance of this design does not
clear its separate Security Review or the expressly retained doctrine-evolution
gate.

**Covered**: claims and drift (#1, #6): roadmap request against
`tools/session.py::_do_full_handoff`; production-path verification design (#2):
proposed real-CLI temporary-repository checks, with existing examples in
`bootstrap/tests/test_session_routines.py::test_handoff_prunes_the_intent_surface`;
completeness and failure disposition (#3, #4): conditional readiness and preserved
guards in Proposal and security preflight; consistency and reuse (#5): existing
CLI helper boundary and skill sections 1–2; lifecycle placement (#7):
`doctrine/session-routines.md`, “The routine has two modes”; scope and satisfiers
(#8, #9): non-pruning preparation contract and “Tests required”. No findings need
satisfiers.

**Not covered / low confidence**: no implementation exists to falsify; no CLI
was run in handoff or prune mode, and no test suite was run. Security Review
remains separate. The plan must resolve exact test nodes, shared-helper design,
install consumers and the doctrine-evolution gate before implementation.
