# Plan: Living plans and concise records

**Source proposal**: dev/proposals/archive/2026-11-12-claude-plan-records-and-living-plans.md
**Author**: gpt-6.1-terra (Medium), plan author
**Status**: revising-code
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-12
**In brief**: Keep active plans current while preserving reviewed evidence and making costs visible at closeout.

## Build summary

Make the four operative plan cells editable throughout active work, with review bound to substantive changes. Preserve historical authority and every verification duty while shortening repeated instructions. Give final records a countable benefit judgment and add its advisory summary to Cairn's existing release report.

## Source proposal

Decision `5962633b` accepted the revised heavy v0.7 proposal, including its design-origin routing. Its Proposal A–C, security preflight and retained scope govern this plan; its historical measurements are not implementation evidence.

## Scope

Change Cairn's `AGENTS.md`, `dev/agent_collaboration.md`, plan and proposal templates and their `templates/core/` counterparts; reconcile `docs/methodology/plans.md`, `lifecycle.md` and `lifecycle-contract.md` with the installed rules. Change `tools/board.py` and its shipped `templates/skills/_lib/board.py` twin, Cairn-only `tools/audit_report.py`, and `docs/release-process.md`. Inventory other actual consumers of review headings and verification records before editing, including audit pulse; preserve their evidence semantics. Do not ship the audit reporter or change release authority.

Reuse: `tools/board.py`'s `--next` review/response reader and H2 section parser, its shipped twin, and `tools/audit_report.py`'s archive walk, `--root` and pulse paths already serve these jobs. `rg` for their headings and filenames found the board contract and replacement-tool tests; extend their public entry paths, not a new command, checker, collector or sidecar.

## Sequence

Estimate two focused implementation windows plus independent reviews and final verification. The main uncertainty is preserving advisory reader compatibility across legacy and amended records. Both chunks are agent-executable after the required plan reviews; C2 depends on C1's contract. Commit each lifecycle transition separately.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Reconcile active-plan lifecycle, record grammar and receipt guidance. | Plan reviews | Paired governing templates and methodology |
| C2 | Implement and verify existing readers and release invocation. | C1 | Board twins, advisory audit report, public-contract tests and release guidance |

C1: Scope, Sequence, Acceptance criteria and Verification remain mutable only while active. A change-log entry identifies the revision commit, cells, change and reason; it cannot rewrite historical Reviews, responses, records, Decisions, quotations, accepted proposal scope or fences. Substantive changes stop affected and dependent work; return to `revising-plan`, commit the replacement, request a fresh non-author ordinary review and applicable Security Review, record author disposition, then use `ready-to-implement` before resuming. Preserve owed code-review returns, final verification, scope-reduction approval and Security Review caps. Wording/status changes that change no obligation need no amendment review; missing design returns to the existing operative cells.

For machine-readable amendment chains, each change-log entry names the full prior and replacement Git object IDs (40 or 64 hexadecimal characters), affected cells/dependencies, change, reason and exact required obligations. The operative revision commit may use `this commit` for its replacement while status is `revising-plan`; the next plan-only metadata fill commit replaces that marker in the same entry with the just-created revision SHA before review. This fill is not another revision. Affected work remains stopped until the ID is bound and review and disposition are complete. The first prior ID is the original full-review target; each later prior ID is the preceding amendment replacement SHA, not a review or disposition commit.

Each distinct `## Plan amendment review -- <reviewer> -- <date>` records the identical prior/replacement pair, affected cells/dependencies, one `**Obligation**` and `**Verdict**`. Record affected cells and dependent chunk IDs as a comma-separated set of exact operative headings and chunk IDs, without duplicates; reviews repeat that set. Every revision needs exactly one unambiguous review per required obligation. If the latest complete review set contains REVISE, only author revision may be suggested while status is `revising-plan`; implementation remains stopped. A successor must link directly to that rejected replacement and carry forward the union of unresolved affected entries and required obligations, alongside its own changes. Its reviewers assess the replacement afresh; earlier ACCEPTs never transfer. Missing, extra, conflicting or duplicate predecessor records stop selection; a rejected predecessor is traversable only through this explicit successor. The latest revision becomes actionable only with all ACCEPTs and its paired author ready disposition. Security Review passes across replacements count toward the existing cap; no successor resets it. Make these corrections in the paired C1 template/collaboration rules and methodology during C2. Committed records are authority; the board is advisory and compares strings and record order without invoking Git or proving SHA ownership. A consistently forged SHA cannot be detected by this text-only comparison. No historical record is overwritten. Keep original full review distinct and existing full-review behavior compatible.

C1 also replaces the repeated Verification instructions in both plan templates toward 700 words each, mapping each removed passage to its retained duty: Boundary A selection and prose gates; Boundary B timing, clean unchanged final commit, mode/rationale and consumers, range, interpreter, command outcomes/counts/elapsed/Tokens, acceptance commands, non-pass disposition and omissions; Boundary C, timing diagnostics, conditional Tokens retirement, review fixes and final commit duties. Keep checks, not merely field names. Replace the old closing sentence in both plan and light-proposal templates and lifecycle guidance with `**Benefit versus cost**: <verdict> -- <benefit>; cost <measured>; remaining burden <measured>`. Verdict is `worth it`, `partly`, `not worth it`, or `unknown` with revisit condition. Use the declared implementation-to-tested range for Git counts and net burden; distinguish aggregate agent elapsed from wall time, report missing as `unknown`, and include available decision counts, shipped/always-loaded word changes, test count/runtime and installed-file deltas from existing records. No new collector or review stage.

C2: board `--next` recognizes the chain without counting amendment records as duplicate original reviews. A latest rejected revision with complete, unambiguous records selects only author revision; a fully reviewed, directly linked successor with carried-forward affected entries and obligations may resume after its own all-ACCEPT reviews and ready disposition. A missing, conflicting, extra or skipped link/obligation, duplicate or mismatched record, narrowed carry-forward, or unresolved marker stops selection. Git and non-Git roots behave identically for identical records; unavailable Git never approves an unknown marker. Changed Verification or dependencies cannot inherit an earlier ACCEPT. The audit command selects each archive's last H2 implementation-verification section only, ignores fenced and quoted examples, lists each plan then verdict totals, reports absent lines `no line` without a new warning, and malformed/duplicate/conflicting current lines `unknown` with advisory diagnostic. Keep historical archives unchanged; preserve existing audit and pulse evidence semantics. Document `python tools/audit_report.py` for the existing release-closeout owner; it is read-only, advisory and not a release gate.

## Acceptance criteria

### C1

The paired rules and published explanations agree on the revision, stop, review and resume conditions and retain accepted baseline, immutable history and all prior assurance duties. Compare each original Verification duty and receipt field to its new home; measure both sections and both always-loaded caps (Cairn 2,000; shipped 1,500). The 700-word target is not a cap or permission to omit evidence. Light and planned final records use the same countable line, including unknowns and range.

### C2

Extend `bootstrap/tests/test_board_json_contract.py` through `board.py --next --json` for both board copies using temporary artifacts: complete ordinary/Security reviews, latest REVISE selecting only author revision, then a directly linked successor with carried-forward affected set and obligations selecting implementation only after fresh ACCEPTs and author disposition. Missing, skipped, extra, duplicate, mismatched or conflicting records, incomplete rejected predecessors, narrowed carry-forward, unresolved markers, and latest REVISE with no successor cannot select an implementer in Git or non-Git fixtures; Verification-only weakening and changed dependency cannot reuse old approval. Extend `bootstrap/tests/test_replacement_tools.py` through `python tools/audit_report.py --root <temporary-root>`: last versus earlier record, historical absence, duplicate/malformed current line, fenced/quoted example, and valid totals. Preserve existing public pulse and review-evidence behavior. Tests assert structured fields, verdicts and stop behavior, not prose wording; temporary developmental probes are removed. Security preflight S2/S3 uses these real entry points; no identity authentication or tamper-proof Git is claimed.

## Scope delta

**Scope delta**: preserved.

## Verification

Before implementation run `python tools/test_tiers.py for <changed paths>`; pass the reviewed range for governing text. Run mapped tests and applicable claim, link/content, snippet and neutrality prose gates; count negative searches against a known-positive case. Compare paired copies and receipt-duty mapping, measure word counts and exercise the named public commands. Boundary C is independent ordinary and Security code review with targeted falsification. After reviews, Boundary B is wide for governing and trust surfaces, on a clean unchanged final commit: mapped iteration and integration tests, owning/public paths, standing gates and plan-specific commands. Record mode and rationale, full tested SHA and reviewed range, interpreter, pre/post state, command table including outcomes, elapsed and Tokens, non-passes and omissions. Certification remains separate.

## Plan review -- GPT-6 Sol (Security Review, High) -- 2026-11-12

Reviewed commit: `857ff426`

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: approximately 5 minutes
**Tokens**: unknown

**Steelman.** Active plans can stay accurate while commit-linked review records preserve earlier authority and the existing advisory board shows the next move.

**Foundations**
1. **Should this happen as framed?** Yes, once amendment identity is specified so changed Verification cannot inherit old approval -- source proposal, Proposal A and S1-S5.
2. **Best alternative.** Keep the board and distinct records, defining unresolvable-history behavior -- `tools/board.py`, `_next_review_state`.
3. **What would show it wrong?** A Verification-only revision labeled `this commit` remains actionable through an old ACCEPT; test both boards with Git and non-Git fixtures -- C2 acceptance criterion.

**Blocking finding -- amendment binding is underspecified.** C1 permits `this commit` as a replacement identifier, but later reviews use a full commit ID. The board reads plan text without Git history (`tools/board.py`, `_next_sections`/`_next_review_state`); its `--root` fixtures need not be Git repositories (`bootstrap/tests/test_board_json_contract.py`). Specify how to resolve that marker, check original-to-amendment and subsequent links across separate review commits, and stop when a link cannot be established, including without Git. Test complete and forged, skipped or unresolvable chains through `--next --json`. This trust-boundary choice cannot be left to a Low implementer.

**Does any rule weaken or disappear?** Freeze and one-round rules change intentionally; C1 retains fences, history, Security caps and Boundary A/B/C duties, subject to the gap above.

**Covered:** source A-C/S1-S5, plan C1/C2, board reader and tests, receipt fields. **Not covered / low confidence:** implementation, parser probe or test run.

## Plan review -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-12

Reviewed commit: 857ff426

**Obligation**: Internal
**Tier**: Internal
**Findings**: blocking
**Verdict**: REVISE
**Elapsed**: approximately four minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes in purpose: current operative cells and retained evidence can coexist, but the reader needs a specified commit-binding mechanism before Low execution -- accepted proposal A; Sequence C1–C2.
2. **Best alternative.** Reuse the existing advisory board and committed records with a small, explicit resolution rule; do not add another authority source -- `tools/board.py` `--next`; proposal A6.
3. **What would show it wrong?** A changed Verification or dependency accepted under an earlier review, or an unresolved replacement treated as approved, would falsify it. Exercise both board copies through `--next --json` with linked Git revisions and unavailable history -- C2.

**Blocking:** C1 permits `this commit`, but neither its grammar nor C2 says how the reader identifies the revision containing that line, matches it to the review's full replacement SHA and prior chain, or behaves when Git history is unavailable or ambiguous. Current public `--root` fixtures use plain temporary directories; they cannot establish that binding. Specify the smallest workable resolution and conservative advisory stop, including how changed Verification and dependencies are associated with the reviewed replacement; add public Git and non-Git falsifiers. This closes the execution design without making the advisory board an authority.

**Rules and audience:** The freeze after implementation intentionally changes; immutable history, accepted scope, review and verification duties remain specified in C1. Installed guidance must carry those duties for agents without a person-level decision.

**Coverage:** Read the committed plan, accepted proposal, plan template, board reader and representative public fixtures. Did not implement, run tests or independently review every consumer; Security Review is separate.


## Response -- GPT-6.1 Terra (plan author, Medium) -- 2026-11-12

- **Security blocking finding / ordinary blocking finding:** C1 now requires explicit full object IDs in settled entries, a plan-only metadata fill before review, the original review target as the first prior and the preceding replacement as each later prior. It binds affected cells, dependencies and separate required obligation records to the same pair and requires author disposition. The board compares record strings and order, stops on unresolved or broken chains and does not use Git; its inability to detect a consistently forged SHA is explicit. C2 adds the requested public Git and non-Git falsifiers and next-revision coverage. These additions are necessary to close the two findings and account for the opening plan exceeding its 1,000-word target.

No implementation, new review pass or scope waiver is claimed. **Elapsed**: unknown. **Tokens**: unknown.


## Review disposition -- GPT-6.1 Terra (Implementation coordinator, Medium) -- 2026-11-12

Revision `fed04f9b` answers the two plan findings (`cd52a24e`, `e41e8038`) using the High-tier design handoff: settled full IDs, first and subsequent link rules, separate obligation records, unresolved-marker stop and identical text-only behavior without Git. The stated forgery limit prevents an authentication claim. Both findings are closed by that specification and the author response; no clearing review or waiver is added. The plan is ready for Low execution, with independent code and Security Reviews and final verification still owed. Elapsed: approximately three minutes; Tokens: unknown.

## C2 implementation checkpoint -- GPT-6 Luna -- 2026-11-12

**Stage**: audit-summary slice committed; C2 remains in progress.

**Change**: The advisory audit reports the final real H2 implementation-
verification record only, ignores fenced and quoted examples, lists one benefit
verdict per archive plan, and prints totals. Missing lines report `no line`
without a new warning; malformed or duplicate current lines report `unknown`
with an advisory diagnostic. The existing release-closeout owner has the
read-only, non-gating command documented in `docs/release-process.md`.

**Verification**: The public command test passed once with canonical Python
3.13: final versus earlier record, historical absence, fenced/quoted examples,
all four verdicts, duplicate/malformed diagnostics and totals. Existing pulse
paths were not changed. Elapsed: unknown. Tokens: unknown.

**Remaining C2**: The board twins and their public tests remain pending High
design on how a rejected amendment attempt links to a successful successor.
This checkpoint changes no scope and does not mark C2 complete.

## Plan change -- GPT-6 Sol (High design author) -- 2026-11-12

**Prior reviewed commit**: 857ff426b8c1eb90e1d780dd932a1b8aad491976
**Replacement commit**: 0c3571eed321612c4989ec73890d68778dab11de
**Affected cells and dependencies**: Sequence, Acceptance criteria, C1, C2
**Change**: Specify a directly linked successor to a completely reviewed REVISE candidate, with affected material and obligations carried forward, fresh reviews, author-only interim advice and Security Review cap continuity. C2 corrects the paired C1 guidance as well as the board twins and public tests.
**Reason**: A permanent stop after any historical REVISE would prevent the accepted A3/A5 revision-and-resume path; A6 still stops the latest rejected candidate and every ambiguous or broken chain. No accepted outcome or check is removed.
**Required obligations**: Internal + Internal Security Review


## Plan amendment review -- GPT-6.1 Sol (Security Review, High) -- 2026-11-12

**Prior reviewed commit**: 857ff426b8c1eb90e1d780dd932a1b8aad491976
**Replacement commit**: 0c3571eed321612c4989ec73890d68778dab11de
**Affected cells and dependencies**: Sequence, Acceptance criteria, C1, C2
**Obligation**: Internal Security Review
**Verdict**: ACCEPT
**Findings**: none

**Foundations**

1. **Should this happen as framed?** Yes: a directly linked, freshly approved successor permits accepted revision-and-resume without treating its rejected predecessor as approved -- source A3/A5/A6; C1 chain specification.
2. **Best alternative.** Keep a finite ordered record chain in the existing advisory board; inherited affected entries and obligations plus fresh latest reviews avoid another workflow engine -- Sequence C1–C2.
3. **What would show it wrong?** A skipped rejected revision, narrowed carry-forward, transferred ACCEPT or missing latest ready disposition selecting implementation would falsify the amendment -- C2 public Git/non-Git acceptance fixtures.

The amendment specifies complete predecessor review sets, exact contiguous
commit pairs, affected-set/obligation carry-forward, author-only interim advice,
and all-ACCEPT/latest-ready resumption. Malformed, extra, duplicate, conflicting,
unresolved or incomplete records stop selection. The same finite grammar is
executable at Low without choosing a new authority mechanism. Metadata commit
`e00eeed8` only binds the replacement marker; it supplies no approval.

Source scope and Maintainer fences remain intact: this uses a new approval for
the replacement, never an earlier ACCEPT. Immutable history and original full
reviews remain distinct. The specified C2 correction to paired C1 guidance
reconciles its current unconditional non-ACCEPT stop with the successor rule.
Text-only SHA comparison still cannot authenticate consistently forged records.

**Coverage:** Compared the accepted source, original target, operative amendment,
metadata fill, current templates/collaboration grammar and existing board reader.
No implementation, parser execution, tests, suites or other consumers audited.
This is the second plan Security pass after `cd52a24e`; successors do not reset
the cap or waive code review/final verification. No rule weakened beyond the
accepted active-plan change.

**Elapsed**: approximately eight minutes. **Tokens**: unknown.

## Plan amendment review -- GPT-6.1 Terra (ordinary reviewer, Medium) -- 2026-11-12

**Prior reviewed commit**: 857ff426b8c1eb90e1d780dd932a1b8aad491976
**Replacement commit**: 0c3571eed321612c4989ec73890d68778dab11de
**Affected cells and dependencies**: Sequence, Acceptance criteria, C1, C2
**Obligation**: Internal
**Verdict**: ACCEPT
**Findings**: none

The amendment lets an author correct rejected work without erasing it or treating an older approval as permission to implement new material.

1. **Should this happen as framed?** Yes. Source A3/A5 requires revision and resumption, while A6 forbids inheriting an earlier ACCEPT. The specified complete predecessor, direct successor and fresh latest review set satisfy both -- accepted source A3/A5/A6; amended Sequence.
2. **Best alternative.** Use the finite ordered records and existing advisory reader. A second workflow engine or Git-history validator would add machinery beyond this text-consistency contract -- C1/C2; retained text-only limitation.
3. **What would show it wrong?** A successor that drops an unresolved dependency or required obligation, or a latest REVISE selecting implementation, would falsify the result. C2 names public tests of both behaviors, including Git and non-Git roots -- C2 Acceptance criterion.

The executor now has exact links, carried-forward sets, review associations, latest ready disposition and stop cases. Paired C1 guidance is explicitly corrected with C2, avoiding contradictory installed instructions. Original reviews, historical rejected records, accepted scope and all check duties remain; Security caps do not reset. Metadata fill `e00eeed8` binds the reference without approving it. This adds no recurring Human operation or approval role.

**Coverage:** Compared the accepted source, operative amendment, metadata-only fill, current C1 grammar and named public command/test homes. No parser, tests, suite or code review ran. The separate audit fence-parser defect and all implementation assurance remain work to finish; this plan review clears neither. No accepted rule weakens or disappears.

**Elapsed**: approximately five minutes. **Tokens**: unknown.


## Response -- GPT-6.1 Terra (Implementation coordinator) -- 2026-11-12

**Prior reviewed commit**: 857ff426b8c1eb90e1d780dd932a1b8aad491976
**Replacement commit**: 0c3571eed321612c4989ec73890d68778dab11de
**Affected cells and dependencies**: Sequence, Acceptance criteria, C1, C2
**Disposition**: ready-to-implement

Both required amendment reviews accept the specification without findings: Internal `b5fa92d1` and Internal Security Review `a3d15a50`. Resume C2 under the amended specification, correcting its paired C1 guidance and retaining the audit fence-parser repair. The second plan Security pass does not reset the cap. Independent code reviews and final shared verification remain required. Elapsed: approximately one minute; Tokens: unknown.

## C2 audit grammar repair -- GPT-6 Luna -- 2026-11-12

**Change**: A would-be closing fence now closes only when its matching marker
and length are followed by whitespace. Opener info strings remain valid. The
existing public audit fixture includes a malformed closing marker containing
fake H2 and benefit text; the actual record stays authoritative.

**Verification**: The named public command test passed once with Python 3.13
(1 passed, 37 deselected). It exercises the CLI, last-record selection and the
existing totals. No separate private parser fixture was added. C2 remains in
progress for the amendment reader and paired guidance. Elapsed: unknown;
Tokens: unknown.

## C2 amendment reader -- GPT-6 Luna -- 2026-11-12

**Change**: The paired board readers now compare amendment records in text
order. They require the first prior ID to match a full original review target,
then direct full-ID links; complete per-obligation reviews on each attempt;
carry-forward of the predecessor's unresolved affected set and obligations;
fresh review; a ready author response for each accepted predecessor and the
latest revision; and the existing cumulative Security Review cap. A complete
latest REVISE selects only author revision. Malformed, incomplete, extra,
duplicate, conflicting, narrowed, skipped and unresolved records stop. The
paired templates, collaboration guides and plan methodology describe the same
finite chain. The existing release guide names the read-only audit command.
The board source pin in `dev/.cairn/cairn-lock.yml` matches both byte-identical
board copies.

**Verification**: Public `--next --json` checks through both shipped board
copies passed 60 selected cases (135 deselected): complete REVISE-to-successor flow,
Git/non-Git equivalence, and stop cases for short baseline, incomplete or
duplicate/extra/mismatched reviews, skipped links, narrowed carry-forward,
unresolved IDs, missing fresh dependency review, rejected latest status, and
an accepted predecessor without its author disposition. The installed-board
schema node passed once after the Python 3.12 staged-install addition. The
audit public CLI case passed once above. Link and snippet checks passed for the
five amended guidance files; the board twins are byte-identical and their
source pin matches. The 20-file mapped governing selection and final Boundary
B were not run here; root will join final verification. C2 is delivered and
awaiting independent code review. Elapsed: unknown; Tokens: unknown.


## Code review -- GPT-6.1 Sol (Security Review, High) -- 2026-11-12

**Reviewed**: C1 `a8bfdc5d`, audit `a4a24dda`/`4fbab5bd`, C2 `4bbaf375` through `d3953c9e`.
**Obligation**: Internal Security Review
**Verdict**: REVISE
**Findings**: four blocking, cheap repairs

**Foundations**

1. **Should this happen as framed?** Yes, but example text and misordered records currently establish false amendment approval -- public board falsifiers below.
2. **Best alternative.** Correct existing section parsing, ordering and review classification, retaining the finite advisory reader -- `tools/board.py::_next_plan_amendments`.
3. **What would show it wrong?** Fenced approvals, premature ready dispositions or an unauthorized third Security pass selecting implementation fail C2; all three selected implementer -- frozen `d3953c9e` probes.

1. **Blocking:** `_next_sections` accepts amendment ACCEPTs inside code fences. Ignore fenced/quoted example authority through the existing iterator; add that class to the public malformed-chain fixture.
2. **Blocking:** A ready Response placed before its reviews still resumes implementation. Retain section positions and enforce change, complete reviews, then paired disposition; rejected reviews must precede their successor. Extend the same public fixture.
3. **Blocking:** Cap counting recognizes original Security reviews only by heading, unlike `_next_review_state`'s Obligation/Tier handling. A neutral-heading Security review plus two amendment passes bypasses the cap. Reuse that classification and add the demonstrated public case.
4. **Blocking:** Both plan templates dropped the explicit command-table requirement. Restore Command/Exit/Outcomes/Elapsed/Tokens table instructions; source B7 retains this duty, and published methodology alone cannot govern adopters.

**Evidence/limits:** Recipe `/private/tmp/cairn-living-code-security-probe.py`; results via `/private/tmp/cairn-living-code-security-sol-location`. Valid control resumed; audit ignored fenced/quoted later records. Paired guidance, remaining receipt duties, board twins and installed hash agree; loaded totals are Cairn 1,488/2,000 and shipped 1,495/1,500 words. No suites, 60+1 control replay, exhaustive consumer audit or final wide Boundary B. Advisory records still cannot authenticate identity; no scope waiver. **Elapsed**: public probes 0.31 seconds; total unknown. **Tokens**: unknown.
