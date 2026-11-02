# Remove the stray finding ID

**Author**: Codex (GPT-6)
**Status**: revising
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-02
**In brief**: Remove an obsolete review finding ID from the scaffold security inventory so readers are not pointed to a closed review.

## Decision summary

Remove `(R5)` from the `new-core-blocked` entry in the security mutation inventory. The Maintainer already requested correction of the identified cases; the file's next edit has occurred. The change is one deletion, but the inventory is in the named high-risk scaffold surface and requires its review process.

## Context

`dev/PLANNING.md` records the trigger and the Maintainer's 2026-10-27 direction:

> "Please correct those cases you've found"

The file was edited in commit `e9adb1f98e4e5bd65d11149d2c1b89c956b50c2d`, and the entry still contains `(R5)`. The board explicitly retains `SR-1`, which the frozen audit script defines.

## Proposal

Delete only `(R5)` and its preceding space from the `new-core-blocked` / `new-core-lockconflict` bullet in `bootstrap/_scaffold/SECURITY_MUTATIONS.md`. Preserve the behavior description and other identifiers.

## Rationale

The marker points into an ended review and adds no explanation to this entry. Removing it fulfills the existing request without altering the documented safeguard.

## Alternatives considered

Leave the marker: this costs no implementation effort but leaves the identified obsolete reference in place after its trigger. Broader identifier cleanup exceeds the recorded request and is not proposed.

## Documentation / doctrine surface

The change is descriptive security inventory prose at its existing home under `bootstrap/_scaffold/`; it changes no governing prescription. This proposal is deliberation in `dev/`.

## Evidence / verification plan

Compare the final inventory against its parent to verify the sole intended deletion and preserved behavior text. Search for readers and byte pins, run the applicable prose gates and file-naming tests, and perform wide Boundary B on the final reviewed commit under Python 3.13.x. The plan will map the precise checks and consumers. An altered safeguard description or a reader depending on this marker would falsify the proposed edit and require reassessment.

### Tests required

Determine the file-naming test list with `python tools/test_tiers.py for bootstrap/_scaffold/SECURITY_MUTATIONS.md`, inspect readers and byte pins, and map any affected checks in the plan. No behavior change or new test is proposed.

### Examples / smoke checks

Run applicable claim, link, snippet and neutrality gates for the changed prose; select and record exact commands in the plan. No full-tree certification is requested by this proposal.

#### Security preflight — five questions, answered in writing

- **S1:** The Maintainer's recorded direction and the current inventory supply the proposed deletion; the change makes no admission or authorization decision.
- **S2:** A comparison against the parent should fail if any other bytes change; the implementation must demonstrate that control. This prospective check has not been run.
- **S3:** The implementation plan must identify the exact diff and prose-check commands, selection, input set and applicable reader-facing claim; these have not yet been measured.
- **S4:** The deletion adds no default, fallback, normalization or parse-error path.
- **S5:** This prose edit changes no attacker capability or security boundary; existing scaffold risks remain as documented in `bootstrap/SAFETY.md`.

### Independent scientific check

N/A: no scientific assumption or result is changed.

## Signals the change is wrong

The identifier proves necessary to interpret a live safeguard or a consumer relies on its exact bytes.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance

The inventory is under the named high-risk `bootstrap/_scaffold/` surface. Usual and Security Reviews apply; the Decision and any plan fences remain the Maintainer's authority.

## Proposal review -- Codex (GPT-6) -- 2026-11-02

**Verdict:** Proceed as framed; no blocking findings.

**Foundations.** (1) Yes: `dev/PLANNING.md` records the Maintainer's direction, identifies this marker and retains `SR-1`; commit `e9adb1f9` subsequently edited the inventory, while line 70 at `a7a87d96` still carries `(R5)`. The proposed deletion addresses the recorded case without changing its safeguard description. (2) Leaving it costs no work but loses that correction; a broader cleanup adds work outside the recorded case. The named high-risk `bootstrap/_scaffold/` surface in `AGENTS.md` supports the heavy path even for this prose edit; the documented cheap-defect exception does not remove the proposal's stated assurance obligations. (3) A reader or byte-pinned consumer needing this exact marker, or a diff changing the safeguard description, would show the change wrong. The proposed reader and pin search and exact diff comparison can expose those cases.

**Coverage:** Read the proposal and committed inventory, planning trigger, relevant high-risk rule and subsequent inventory edit. Did not independently enumerate consumers or run implementation checks; those remain prospective. Elapsed: approximately 3 minutes. Tokens: unknown.

## Security Review -- Codex gpt-6.1-sol -- 2026-11-02

Reviewed commit: 10fc47b6594820b51ccfe4ef3f825dfe5df2daca  
Target: exact marker deletion, retained safeguard and declared assurance  
Prior findings: none  
Assurance path: high-assurance

**Tier**: Security Review  
**Findings**: none  
**Verdict**: ACCEPT as framed; recommendation, not a Maintainer Decision.  
**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. Removing only the space and `(R5)` leaves the occupied-destination hard block, lock-source conflict, no-silent-overwrite promise and historical cause intact. The retained `SR-1` is outside this exact edit. -- Committed SECURITY_MUTATIONS, new-core-blocked bullet; Proposal; planning direction.
2. **Best alternative.** Leave the marker: no editing cost, but the obsolete reference remains after its recorded trigger. An identifier scanner, broader cleanup or new security check adds no value for this one deletion. -- Proposal, Alternatives and Scope; planning's separately deferred warning-scan proposal.
3. **What would show it wrong?** A consumer requiring the exact identifier or another byte changing, especially the refusal semantics. The proposed reader/pin search and parent-byte comparison address these possibilities without rerunning runtime security behavior. -- Proposal, verification plan and S2/S3; committed inventory bullet.

The current governing rule names `bootstrap/_scaffold/` as high-risk, and the author's heavy declaration stands unless the Maintainer changes it; this supports the present Security obligation. That directory rule does not make the deletion intrinsically complex. The proposal separately declares required plan review: do not silently waive that declaration, but do not add machinery or extra checks beyond its mapped existing obligations. Any plan should remain proportional to the exact deletion.

Coverage: read committed proposal, ordinary review, target bullet, planning context, governing high-risk/tier rules and current proposal template. Did not enumerate all readers/pins, execute the prospective byte control or run suites. No security behavior, authority or safeguard deletion is proposed.
