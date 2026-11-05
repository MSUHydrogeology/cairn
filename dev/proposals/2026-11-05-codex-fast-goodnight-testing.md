# Fast goodnight checks and explicit slow-test triggers

**Author**: Codex Terra (Medium)
**Status**: awaiting-decision
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-05
**In brief**: Give goodnight an honest project-owned smoke selection without weakening required slow or release checks.

## Decision summary

Replace the ambiguous instruction to run the test suite at a full handoff with
a project-owned smoke selection, a small check of basic operation. Cairn has no
configured goodnight test selection today; its existing profile smoke test is
a candidate for a Cairn-local command, not a current default or a measured
speedup. Report what ran and what did not. Slow checks still run when required
by a release, an accepted plan, safety or security requirements, or the
Maintainer. At release, an added result comparison is proposed for the existing
full-suite invocation; the current command alone does not detect an omitted
required member. This adds one release check to build and maintain, not a
second suite execution.

## Context

The full-handoff owner is told to run the test suite in
`docs/methodology/session-routines.md` but the project's concrete test command
is owned by its optional `dev/rules/custom_session_routines.md`. The governing
`templates/core/AGENTS.md` already requires configured suite members at their
required points and preserves change-specific verification. Cairn's own
`AGENTS.md` limits full-tree certification to named triggers; its release
command is in `docs/release-process.md`. `templates/skills/session-end/SKILL.md`
says the optional custom file's missing Goodnight section means no custom steps,
and `tools/session.py session-end --prepare-handoff` does not execute tests.
`bootstrap/tests/test_profiles_smoke.py` documents a runnable profile-selection
command, but no goodnight instruction invokes it. Board item 2g records the
requested correction in `dev/PLANNING.md`; issue #53 supplies the work item.

## Proposal

Deliver one v0.7 cadence correction, coordinated with the suite-consolidation
owner before editing shared guidance or test selections. The full-handoff owner
uses its configured fast/default smoke command, records command, result and
coverage limitations, and reports an absent or failed selection as unavailable
or failed, not passed. Do not invent a universal command or claim that the
smoke certifies the tree. Reflection-only participants acquire no new suite
obligation. Without local configuration, Cairn would run no goodnight tests:
it loses even immediate profile smoke feedback. The smallest useful local
correction is to add a Cairn-owned `## Goodnight` section in the currently
absent `dev/rules/custom_session_routines.md` naming
`python -m pytest bootstrap/tests/test_profiles_smoke.py`, an existing command
that checks profile parsing, preset expansion and scaffold summaries. It is a
candidate local selection, not a claim of general coverage or measured speed;
verify it under the canonical interpreter before adoption.

State explicitly that slow tests remain required at release and wherever an
accepted plan, safety or security requirement, or Maintainer request requires
them. Change-specific checks and Boundary B remain due on their existing
schedule; goodnight does not defer them. Preserve Cairn's existing full-tree
certification commands and triggers, including before a push when required,
re-anchor, release cut, or Maintainer request. No new registry, scheduler,
automatic deferral, or blanket waiver is authorized.

At release, the documented executable command or sequence must include the
project's required slow and security members, not merely say that it should.
Cairn's current command is `CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests
--quality-gate-shuffle-seed=0` followed by the two quality sub-gates and
`scripts/check_cairn.py` in the release checklist;
`CAIRN_FULL_SUITE=1` permits breadth but does not prove member coverage.
`bootstrap/tests/security_manifest.py` owns the named security family of 17
files; `bootstrap/tests/test_security_marker.py` independently pins its
reviewed membership. Neither currently compares those requirements with the
actual release invocation. Propose adding only JUnit XML reporting to that
same pytest invocation, then immediately running the proposed Cairn-specific,
standard-library `scripts/check_release_test_members.py` on its fresh XML.
The comparator checks actual file membership and outcomes against
`SECURITY_FAMILY` and requires `test_security_marker.py` to contribute a
successful case, so an altered
selection cannot silently omit the whole roster-guard file. It fails on absent,
stale, malformed or ambiguous XML, a missing required file, no executed case
for a required file, or an unsuccessful case; the documented sequence also
preserves any nonzero pytest exit. It runs no tests itself. A synthetic
omission must be made in the release invocation, not only in the expected
set, and must make that sequence fail.

For an adopter with an authoritative slow-test configuration, the analogous
comparison uses that project-owned required set, independent of the observed
XML. Cairn has no configured slow tier: `tools/test_tiers.json` has a security
tier, but runtime alone does not create a slow roster. Therefore this proposal
does not assert a Cairn slow-file list or waive any configured suite member.
The proposed check proves file-level presence and reported outcomes, not every
test node (including the exact reviewed-set assertion), command provenance,
or semantic test adequacy. The protected `bootstrap/security_check.py`
release/security run remains a separate owed check; this comparator neither
edits its hooks nor substitutes for it. The
Maintainer must choose whether this additional release comparison earns its
build, run and maintenance cost. No implementation or authority follows from
the design probe alone.

## Rationale

The routine gives useful immediate feedback without implying coverage it did
not obtain. Explicit trigger precedence prevents a fast check from becoming a
reason to miss an already-required expensive check. No runtime saving is
measured here; report the local candidate's cost and coverage before claiming
a faster handoff.

## Alternatives considered

Keep the current wording: no implementation cost, but “test suite” remains
ambiguous and can demand an unnecessary full run or overstate coverage. Run
all tests at every goodnight: simpler to describe and broader routine coverage,
but adds recurring time even when no full run is due. A new registry or
scheduler would add maintenance and another source of truth. The least-involved
release alternative is to keep the current full pytest command and inspect its
result manually; it adds no code but cannot automatically detect a file omitted
by altered selection. The proposed XML comparison adds a small, release-only
check and an output artifact while retaining one pytest execution.

## Documentation / doctrine surface

Change `docs/methodology/session-routines.md` for the published routine and
`templates/core/AGENTS.md` and `AGENTS.md` for governing prescription where
needed; keep local and shipped obligations aligned. Update the applicable
release instructions in `docs/release-process.md` and shipped guidance in
`templates/skills/session-end/SKILL.md` only where their actual wording or
command needs correction. Inspect `templates/modules/team-gated/testing-discipline.md`
and its `dev/modules/testing-discipline.md` counterpart for consistency;
change them only if needed. The proposed Cairn-local custom file is not a
shipped default. Review readers and byte pins before edits. The implementation
plan owns exact affected tests and coordination with 2a.

Proposed paths:
* `dev/rules/custom_session_routines.md` -- Cairn-local goodnight selection only.
* `scripts/check_release_test_members.py` -- Cairn-local comparison of release XML with required files.

## Evidence / verification plan

### Tests required

Trace the changed instructions to actual adopter-facing and local entry points,
commands, selectors and readers. Check the Cairn-local profile smoke selection
through its real command, and check that no configured command or a failed
command can produce a green handoff report. A release proof must compare a
required set owned independently of observed execution with the *actual*
release entry point's executed members. The comparison also requires the
reviewed-set test file, which is not one of the 17 manifest members. Append
`--junitxml=<path>` to the existing release pytest command without changing
its suite selection, seed or trigger. Require a new output path absent before
the run; run the comparator immediately afterward and fail the sequence if
either command fails. Include the existing reviewed security-family pin in
the verification. In isolated copies, omit one required
security file from the actual invocation, and separately omit a configured
slow file from a project-owned slow selection; each must make the comparison
fail even when pytest itself exits zero. Also test missing, malformed and
stale XML, skipped/failed required cases and pytest failure propagation.
No second test execution is part of this check. Run mapped iteration checks,
independent review and wide Boundary B on the final implementation, plus
required Security Review. A known unmet required check keeps work open.

### Examples / smoke checks

Check an adopter with an existing fast command and one without a configured
command: the first reports its actual coverage, the second does not claim a
pass. Measure the candidate Cairn-local profile smoke selection before any
runtime assertion. Run applicable claim, link, snippet and neutrality gates.
These examples do not replace release selection proof or change-specific checks.

#### Security preflight

1. **S1:** The XML comes from the pytest invocation being checked, so it cannot
   define its own required set. Cairn's security requirements come from
   `security_manifest.py`, independently pinned by `test_security_marker.py`;
   the proposed comparison requires a successful case from that pin file;
   an adopter's slow requirements come from its project-owned configuration.
2. **S2:** Omit one required security file from the actual release pytest
   selection, and one configured slow file in an adopter fixture. The
   coordinator reports that Arendt's synthetic omissions made a prototype
   comparison fail under Python 3.12.9; no artifact or canonical Python 3.13
   run was checked here. Both real-entry-point mutations remain required.
3. **S3:** At the existing release trigger, `docs/release-process.md` must
   invoke its current full-suite pytest selection with added JUnit reporting,
   then compare that run's fresh XML with the independent required files;
   both statuses govern the result. The adopter-facing wording must name the
   file-level limit and separate security run, not claim complete test proof.
4. **S4:** Missing required configuration, absent or stale XML, parse errors,
   ambiguous file identity, failed commands, and skipped or failed required
   cases land on non-pass. Existing stricter release and security failure
   handling remains in force; no result confers release authority.
5. **S5:** This addresses accidental omission by a cooperating local operator;
   a malicious maintainer who changes both requirements and evidence, or forges
   the XML, can still misrepresent coverage. It does not establish command or
   evidence provenance or replace the separate protected security run.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A handoff report implies full coverage from a smoke pass, the XML comparator
passes after a required file is omitted from the release run, or a
change-specific check slips past its existing boundary. Any of these
falsifies the proposal's safety case.

## Scope delta

**Scope delta**: preserved. The release comparison specifies the original
required-member proof; it adds no new outcome, roster, scheduler or protected
hook. Its recurring release-check cost is explicit for the Maintainer's choice.

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

## Response -- Codex Terra (Medium) -- 2026-11-05

**Elapsed**: unknown
**Tokens**: unknown

1. **F1:** Accepted. Cairn has no configured goodnight test selection: the
   custom routine is absent and `session-end --prepare-handoff` does not run
   tests. The operative text now names that loss and the smallest local
   correction, using the existing profile smoke command without claiming a
   measured speedup or universal default.
2. **F2:** Accepted, unresolved. The current release command and breadth flag
   do not prove required-member selection. Security membership has an owner
   and a separate reviewed pin, but neither is compared with the actual
   release run; no independent slow-tier roster is established. I have named
   this design blocker for Maintainer disposition rather than promise a future
   discovery or waive the criterion.
3. **SR1:** Accepted; same unresolved release-proof blocker as F2. The
   security manifest and pin are not evidence of actual release execution.
   Current certification and security triggers stay intact; no protected
   machinery is changed or authorized here.
4. **SR2:** Accepted; same no-selection correction as F1. An unconfigured or
   failed smoke result must never be reported green.

### Withdrawn / superseded commitments

* Withdrawn: the claim that Cairn already has an existing fast/default
  goodnight selection. It has none today.
* Superseded: leaving the release-required set and omission detector to be
  discovered during implementation. The proposal now records the missing
  actual-run comparison as a blocking design question for the Maintainer.

## Response addendum -- Codex Terra (Medium) -- 2026-11-05

**Elapsed**: unknown
**Tokens**: unknown

The coordinator relayed Arendt's independent Python 3.12.9 design probe: a
JUnit-file comparison went red for synthetic omissions of a security file and
a configured slow file, without a second test execution. I did not inspect a
probe artifact or verify it under canonical Python 3.13. The operative text now
specifies this as a permitted **proposal**, not an authorized implementation:
the existing release pytest run emits fresh XML, and a Cairn-local check
compares its file membership and outcomes with the separately pinned security
family. An adopter with a slow selection must use its own authoritative
configuration. Cairn has no such slow tier. The comparison is specified to fail
closed and preserve pytest's failure; `bootstrap/security_check.py` remains
separate.

This resolves the design unknown named in F2/SR1 at the proposal level but
does not claim those findings experimentally closed. The comparator specifies
the original release-proof criterion rather than widening its outcome; it adds
one release check, no new registry, scheduler or protected hook. The Maintainer
still chooses whether that recurring cost is justified, and implementation
must supply canonical evidence and the owed reviews and checks. The prior
response and its historical blocker statement remain intact above.

## Review -- Codex Terra -- 2026-11-05

Reviewed commit: 3b023fd3244c857ede0cb0c64140828030f76a79

**Model**: Codex Terra (Medium); fresh ordinary reviewer, not the author.
**Tier**: usual
**Findings**: none
**Verdict**: SHIP
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes, for the widened comparison: an independent file set and fresh results can expose a whole-file omission without another suite run; the result is not node-level proof -- proposal, Tests required; `bootstrap/tests/security_manifest.py`.
2. **Best alternative.** Retain the existing command and inspect its output manually, avoiding a new release check but losing automatic omission detection -- `docs/release-process.md`, Checks to run.
3. **What would show it wrong?** Omit a required file in the actual release invocation and demand a non-pass even when pytest exits zero; separately probe an adopter's independently configured slow file -- proposal, Tests required.

The contract requires both statuses, a new output path, malformed or ambiguous
XML refusal, and non-passing required outcomes. An implementation must map
JUnit identities unambiguously and test these refusals against real output;
otherwise an identity collision can falsely pass or refuse a release. A
successful case from `test_security_marker.py` does not prove its reviewed-set
assertion ran, as the proposal acknowledges. The separate
`bootstrap/security_check.py` run retains its stricter skip and xfail handling;
ordinary pytest XML alone is not a substitute. Cairn has no specified slow
roster, and the withdrawal ledger retains the earlier blocker history.

**Coverage:** Widened contract, prior reviews and responses, release command,
manifest, pin tests and outcome hook at the named commit. No implementation,
XML probe, full suite, adopter configuration or Security Review was performed;
the required real-entry-point mutations remain unverified.
