# Prepare the handoff before the user runs pruning

**Author**: Codex gpt-6.1-sol
**Status**: awaiting-review
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
