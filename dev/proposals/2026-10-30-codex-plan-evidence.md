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
