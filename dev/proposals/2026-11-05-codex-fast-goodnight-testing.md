# Fast goodnight checks and explicit slow-test triggers

**Author**: Codex Terra (Medium)
**Status**: revising
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-05
**In brief**: Use a project's fast smoke checks at goodnight while keeping slow tests mandatory at their actual required triggers.

## Decision summary

Replace the ambiguous instruction to run the test suite at a full handoff with
the project's existing fast or default smoke selection, a small check of basic
operation. Report what ran and what did not; a smoke pass is not a full-suite
pass. Slow checks still run when required by a release, an accepted plan,
safety or security requirements, or the Maintainer. The tradeoff is less
routine end-of-session coverage in exchange for a shorter handoff, without
postponing any independently required check.

## Context

The full-handoff owner is told to run the test suite in
`docs/methodology/session-routines.md` but the project's concrete test command
is owned by its optional `dev/rules/custom_session_routines.md`. The governing
`templates/core/AGENTS.md` already requires configured suite members at their
required points and preserves change-specific verification. Cairn's own
`AGENTS.md` limits full-tree certification to named triggers; its release
command is in `docs/release-process.md`. Board item 2g records the requested
correction in `dev/PLANNING.md`; issue #53 supplies the work item.

## Proposal

Deliver one v0.7 cadence correction, coordinated with the suite-consolidation
owner before editing shared guidance or test selections. The full-handoff owner
uses the project's existing fast/default smoke command, records command,
result and coverage limitations, and reports an absent or failed selection as
unavailable or failed, not passed. Do not invent a universal command or claim
that the smoke certifies the tree. Reflection-only participants acquire no new
suite obligation.

State explicitly that slow tests remain required at release and wherever an
accepted plan, safety or security requirement, or Maintainer request requires
them. Change-specific checks and Boundary B remain due on their existing
schedule; goodnight does not defer them. Preserve Cairn's existing full-tree
certification commands and triggers, including before a push when required,
re-anchor, release cut, or Maintainer request. No new registry, scheduler,
automatic deferral, or blanket waiver is authorized.

At release, the documented executable command or sequence must include the
project's required slow tier, not merely say that it should. For Cairn, trace
the existing release commands and current suite selection with the 2a owner;
retain the certification pair and any separately required security or slow
commands. Do not change the protected gate machinery or configured suite to
make this true; a discovered need to do so stops for reassessment.

## Rationale

The routine gives useful immediate feedback without implying coverage it did
not obtain. Explicit trigger precedence prevents a fast check from becoming a
reason to miss an already-required expensive check. Runtime savings are
expected, not measured here, and depend on the adopter's existing selection.

## Alternatives considered

Keep the current wording: no implementation cost, but “test suite” remains
ambiguous and can demand an unnecessary full run or overstate coverage. Run
all tests at every goodnight: simpler to describe and broader routine coverage,
but adds recurring time even when no full run is due. A new registry or
scheduler would add maintenance and another source of truth; existing project
commands and requirements suffice for this outcome.

## Documentation / doctrine surface

Change `docs/methodology/session-routines.md` for the published routine and
`templates/core/AGENTS.md` and `AGENTS.md` for governing prescription where
needed; keep local and shipped obligations aligned. Update the applicable
release instructions in `docs/release-process.md` and shipped guidance in
`templates/skills/session-end/SKILL.md` only where their actual wording or
command needs correction. Inspect `templates/modules/team-gated/testing-discipline.md`
and its `dev/modules/testing-discipline.md` counterpart for consistency;
change them only if needed. Review readers and byte pins before edits. The
implementation plan owns exact affected tests and coordination with 2a.

## Evidence / verification plan

### Tests required

Trace the changed instructions to their actual adopter-facing and local entry
points, commands, test selectors and readers. Extend existing relevant
`bootstrap/tests/` homes for a plausible omission: a fast handoff cannot be
reported as full coverage, and a required slow member cannot disappear from
the release selection. Exercise the real documented release selection in an
isolated copy, including a known slow member and a deliberately omitted member;
the latter must be detected. Identify the actual members and nodes with the 2a
owner and record any uncertainty. Run the mapped iteration checks, independent
review and wide Boundary B on the final implementation, plus required security
review. A known unmet required check keeps the work open.

### Examples / smoke checks

Check an adopter with an existing fast command and one without a configured
command: the first reports its actual coverage, the second does not claim a
pass. Run applicable claim, link, snippet and neutrality gates. These examples
do not replace the release selection proof or change-specific checks.

#### Security preflight

1. **S1:** Project maintainers supply commands and suite configuration; the
   handoff owner reports results. A project's own configuration selects its
   tests, so the object being assessed influences selection; independent
   release requirements and review must challenge omissions.
2. **S2:** Removing a required slow member from the release selection must make
   the coverage check fail. This mutation has not been run; implementation
   must run and record it against the actual release entry point.
3. **S3:** The actual release command and exact selected members must be
   established with 2a during implementation and compared with the final
   adopter-facing sentence; neither is asserted as verified here. The existing
   Cairn certification command is in `docs/release-process.md`.
4. **S4:** Missing configuration, failed commands, skips or unproven release
   coverage must not become a pass or confer release authority. Existing
   stricter release and security failure handling remains in force.
5. **S5:** This addresses accidental omission by a cooperating local operator;
   a malicious maintainer who changes both requirements and evidence can still
   misrepresent coverage. It does not establish command or evidence provenance.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A handoff report implies full coverage from a smoke pass, a required slow test
is absent from the actual release selection, or a change-specific check slips
past its existing boundary. Any of these falsifies the proposal's safety case.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance

The change touches governing methodology and shipped doctrine; heavy review
and a separate Security Review are required. It does not authorize changing
protected test or release control machinery.

## Review -- Codex Terra -- 2026-11-05

Reviewed commit: a92969cf53dee7302d51d01cfe9c25f3c126ca2f

**Model**: Codex Terra (Medium); fresh reviewer instance, not the author,
despite the matching display name.
**Tier**: usual
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** The cadence correction is useful, but the assumed local smoke and release-omission proof need grounding before a Decision (F1-F2) -- `docs/methodology/session-routines.md`; `docs/release-process.md`.
2. **Best alternative.** Keep the current requirement until a real fast selection and an honest unavailable case are specified; this costs handoff time but avoids promising savings without a runnable selection -- `docs/methodology/session-routines.md` and `bootstrap/tests/conftest.py`.
3. **What would show it wrong?** Exercise a handoff without a configured selection and remove a required slow member from the actual release selection; a false pass or a missed omission falsifies the design -- proposal, Evidence / verification plan.

1. **F1 (blocking): Establish the actual fast path.** The custom routine is optional and absent in this tree; `session-end --prepare-handoff` gathers evidence, not tests, and the broad-run guard refuses an ordinary run over 40 files without an override. The proposal permits unavailable reporting but does not establish whether Cairn has an existing fast/default smoke, its command or coverage, or what useful correction remains when none exists. Identify and trace the actual command, or explicitly describe the no-selection outcome and its loss without inventing a universal command. Evidence: `docs/methodology/session-routines.md` (project customization); `templates/skills/session-end/SKILL.md`; `bootstrap/tests/conftest.py` (`pytest_collection_finish`).

2. **F2 (blocking): Make the release proof falsifiable.** The release command runs `CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0`; the flag overrides the breadth guard, not an independent slow-member inventory. The proposal requires detecting a deliberately omitted member but names neither the independent required set nor the check and trigger that would detect it; deriving expectations from the selected collection would miss the omission. Identify the authoritative requirements, actual release entry point and detection mechanism, and show how a real omission goes red without changing protected machinery, or stop for reassessment. Evidence: `docs/release-process.md`, Checks to run; `bootstrap/tests/conftest.py` (`_refuse_broad_run_if_warranted`).

The proposal explicitly retains change-specific checks and Boundary B on their existing schedule; implementation must demonstrate that an unfinished required check cannot be reported as complete at handoff.

**Coverage:** Read the committed proposal, template, local and shipped session and verification guidance, release command and selector hooks; no full suite, mutation, Security Review, or external issue contents were run or checked. This pass exceeds the word target to distinguish the two independent evidence gaps.

## Review -- Codex Sol (Security Review) -- 2026-11-05

Reviewed commit: a92969cf53dee7302d51d01cfe9c25f3c126ca2f

**Model**: gpt-6.1-sol (High)
**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes in principle: a fast handoff should not impersonate release or security evidence, but the current contract cannot yet show the required slow selection is preserved -- `templates/core/AGENTS.md` > Verification; finding SR1.
2. **Best alternative.** Keep today's suite instruction until the existing project command and independently required release members are named; a new runner or registry is unnecessary -- `docs/methodology/session-routines.md` > Goodnight; `docs/release-process.md` > Checks to run.
3. **What would show it wrong?** A fast green handoff followed by a release command that omits a required slow or security member without a failing check would falsify the safety case -- proposal S2/S4.

**SR1 (blocking, overlaps ordinary F2):** `CAIRN_FULL_SUITE=1` only bypasses the over-40-file refusal in `bootstrap/tests/conftest.py::_refuse_broad_run_if_warranted`; it does not establish which slow members should be collected. The release instructions name a broad pytest command but no independent required-member set or comparison. A project default that excludes a slow tier could therefore look green unless some other existing release owner detects the omission. Name that owner and the expected members independently of the observed collection, then require a separate omitted-member fault to go red. Preserve the existing release/security run triggers; a fast handoff cannot waive them.

**SR2 (blocking, overlaps ordinary F1):** The optional custom routine is absent here, and `session-end --prepare-handoff` gathers a manifest rather than executing a fast test. The proposal permits an unavailable result, but has not identified the useful default check that satisfies issue #53 for Cairn. State the actual fast selection or explicitly accept the no-selection loss before a Decision; never label an unavailable check green.

**Coverage:** Committed proposal, ordinary review, actual session/release instructions and broad-run guard. **Not covered:** an adopter's configured slow tier, a release selection mutation, full suite, or implementation. No check was claimed run by this Security Review. The two blockers add no new mechanism beyond the ordinary review's evidence gaps.
