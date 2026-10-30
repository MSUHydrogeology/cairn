# Keep plan evidence necessary and concise

**Author**: Codex gpt-6.1-terra (Strategy)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Stop requiring a folder for every plan and keep extra plan documents only when necessary.

## Context

The Maintainer said in chat on 2026-10-30: “There is very little reason to create such folders--it's really just a way to circumvent the length limits in plans” and “I think we need notes in place forbidding such things unless absolutely necessary. That's too much documentation.” The local and shipped plan templates require a same-stem evidence folder for every plan (`dev/plans/_template.md`, `templates/core/dev/plans/_template.md`); `doctrine/plans.md` repeats that requirement. The templates already call for concise evidence and repeatable checks in tests or scripts. A mandatory folder creates a place to expand a plan without showing that another document is needed. The Maintainer clarified in chat: “And, remembering that we are only recording evidence if it's needed for plan implementation--not for review.” and “Reviews accept the word of agents summarizing evidence. Or verify (if necessary).”

## Proposal

Remove the mandatory folder requirement from both plan templates and doctrine. A plan records required evidence, results, and limitations concisely in its existing lifecycle records, citing durable evidence where needed. Record evidence only as needed for plan implementation or an existing required safety or security ceremony, not to supply reviewers with separate files or ledgers. Reviews accept agents' concise evidence summaries and may independently verify when necessary. Do not create extra plan documents, sidecars, or evidence folders merely for convenience or to evade plan length limits. Create a separate evidence artifact only when genuinely necessary to preserve or inspect evidence that cannot reasonably fit in the concise record or its canonical home; explain that necessity and cite it in the plan. Keep repeatable tests and scripts in their canonical homes. Preserve existing records and their links; do not retroactively delete or move evidence. This does not change required verification, review, or security ceremonies.

Update any live guidance or actual consumers found to depend on the mandatory folder, including archive instructions, to handle plans with no folder and preserve any necessary existing evidence. Do not add a new enforcement mechanism.

## Rationale

A short record and a pointer normally give a reviewer what they need without an additional document to maintain. Necessary evidence still has a home, and existing evidence remains available.

## Alternatives considered

Keep the mandatory folder: it creates documentation even where no evidence needs it and makes the length limit easier to bypass. Ban all separate evidence: it could discard evidence that cannot reasonably be recorded inline or kept in a test or script.

## Documentation / doctrine surface

Change plan prescription in the local and shipped plan templates and `doctrine/plans.md`; inspect governing guidance and actual consumers for conflicting requirements. Preserve archived deliberation as history. Doctrine changes must satisfy the evolution gate in `doctrine/rationale.md`; the Maintainer's repeated concern and the existing mandatory wording are the evidence for this change.

## Evidence / verification plan

### Tests required

Search live guidance, readers, and byte pins for the folder requirement and update affected checks if needed. Run the mapped tests for changed files and the standing prose gates. Verify a plan without a folder remains discoverable and archivable through any actual affected consumer, and that an existing evidence folder remains preserved. A consumer that still requires a folder, or wording that permits sidecars to evade length limits, falsifies the change.

### Examples / smoke checks

Inspect the local and shipped templates and doctrine together for consistent rules; check links and claims on changed prose.

#### Security preflight

No new trust boundary is intended. Templates and doctrine are protected lifecycle surfaces, so their usual and Security Reviews remain required.

### Independent scientific check

N/A: no scientific claim or result changes.

## Signals the change is wrong

Reviewers cannot find required evidence, or necessary evidence is routinely excluded because the rule is unclear.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance — governing doctrine and authoring templates.

## Proposal review -- Codex gpt-6.1-terra -- 2026-10-30

**Verdict: proceed as framed, subject to the role-floor finding.**

1. **Should it happen?** Yes. At `7a76dd32`, both plan templates and `doctrine/plans.md` require a same-stem folder even when no separate evidence is needed; the proposal removes that requirement while retaining required verification and existing evidence.
2. **Best alternative.** Keep the folder optional without adding a new enforcement mechanism. That is the proposed approach; banning all separate artifacts could lose necessary evidence, while retaining the mandate preserves the burden the Maintainer identified.
3. **What would show it wrong?** A live archive consumer losing an existing folder, a plan without one becoming undiscoverable, or a required ceremony losing evidence would falsify the proposal. Its verification calls for both folder cases and preservation of ceremonies.

**Finding:** The author names the Strategy role while the model mapping assigns Terra to medium and Strategy to high (`dev/.cairn/model-selection-mapping.yml`). No quoted Maintainer exception appears in the proposal. Clarify the role and applicable floor, or obtain the Maintainer’s explicit disposition.

**Coverage:** Read the proposal and committed template, checked the matching requirements in both templates and doctrine, and searched for archive references. Did not exhaustively inspect consumers, execute archive behavior, or assess security controls; implementation and the separate Security Review cover those gaps. No suite run. Elapsed time and tokens: unknown.


## Security Review -- Codex gpt-6.1-sol -- 2026-10-30

Reviewed commit: 7a76dd323890150eb4db8a89049a4b89e8235d19
Target: operative proposal and security consequences
Prior findings: none
Assurance path: high-assurance

**Tier**: Security Review
**Findings**: none
**Verdict**: ACCEPT (security design)
**Elapsed**: approximately 4 minutes, including serialization wait
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes. Removing an automatic folder does not remove required checks: the proposal explicitly preserves verification, review, security ceremonies and existing evidence; the current folder mandate appears in `dev/plans/_template.md`, `templates/core/dev/plans/_template.md` and `doctrine/plans.md`.
2. **Best alternative.** Keep concise implementation records with canonical tests/scripts and allow separate artifacts only when necessary. An absolute ban could obstruct required ceremony evidence; the proposal's explicit ceremony exception and preservation rule avoid that loss -- Proposal and Alternatives considered.
3. **What would show it wrong?** A consumer still requiring a folder, evidence lost during archive, or a required security record treated as optional. The verification plan names folderless discovery/archive and preservation checks, while the operative text retains required ceremonies -- Tests required and Proposal.

No security blocker found. Accepting concise agent summaries leaves independent verification available and does not authorize skipping checks. This conclusion concerns the proposed rule; the ordinary review separately addresses author/model attribution.

**Covered**: committed proposal, mandatory-folder passages in both templates and doctrine, and preservation of safety obligations. **Not covered / low confidence**: implementation, exhaustive consumer discovery, archive behavior or ceremony execution; no tests or suites run.
