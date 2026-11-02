# Distinguish another input from a wider trust boundary

**Author**: Codex Sol (Strategy)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy — changes a shipped security-review rule.
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Clarify that reusing an unchanged, reviewed input guard does not by itself require another Security Review.

## Decision summary

Clarify when an additional input actually changes who or what the system trusts. Another file through the same reviewed reader need not create a new security boundary. A familiar file format can still bring a new source, weaker guard or greater authority, so familiarity alone cannot excuse review. Use the existing review questions to challenge unnecessary passes; add no mandatory review field. Keep Cairn's named high-risk protections and required verification.

## Context

[Issue #37](https://github.com/MSUHydrogeology/cairn/issues/37) reports repeated Security Reviews for additional inputs of known formats. The live module already says “Movement alone is not a trigger” but does not explain reuse of guarded readers: see `dev/modules/security-review.md` and `templates/modules/team-gated/security-review.md`. `AGENTS.md` separately triggers heavy for named high-risk surfaces and added or widened trust boundaries. Savings are unmeasured.

## Proposal

Clarify the boundary-change paragraph in both module copies, retaining “adds or widens” so a genuinely new boundary remains covered. A boundary is the enforced separation between less-trusted input and protected operations or information, not each individual file or call.

Adding another input or output handled by an existing reviewed reader or writer, moving guarded code, or adding a call through an existing guard does not itself add or widen a boundary **when** the source's trust class, accepted input limits, validation, guard reachability, execution authority and information exposure remain within the reviewed contract. A different format is not required for widening. A new untrusted source, bypassed guard, broader accepted input, changed command construction or newly exposed secret can trigger review even through an existing API. A move that changes path resolution or guard ordering is not exempt merely because the code looks familiar.

Explain that the existing proposal and plan Foundations questions should challenge whether a declared Security Review has a real trigger. An author may correct an unsupported declaration before Decision; after acceptance, changing a required review follows existing Maintainer authority and plan fences. Do not introduce a necessity field, automatic cancellation or permission for a reviewer to waive an obligation.

Preserve periodic review, named high-risk triggers, Security Review obligations and the existing wide verification requirement for contract and trust-ceremony surfaces. Clarify that wide is the mapped change-verification mode, not an instruction to run the whole suite. No parser, scanner or new tracking mechanism is proposed.

## Rationale

One explanation at the existing trigger addresses the ambiguity without another form to maintain. The condition matters: an additional HDF5 file through an unchanged reviewed reader may be ordinary reuse; allowing collaborator-supplied files where only locally produced files were admitted changes trust despite an identical format. Existing Foundations already asks whether the work should happen as framed and permits questioning needless process.

## Alternatives considered

Adopt all of #37: replace “adds or widens” with “widens,” add necessity fields and permit bounded checks on non-widening high-risk edits. This more closely matches the request but adds apparatus and changes protections beyond the demonstrated ambiguity. Preserve the current text: least editing, but leaves guarded reuse unexplained. Remove named high-risk triggers: loses the independent review of edits to the controls themselves even when runtime inputs do not change.

## Documentation / doctrine surface

Local security prescription belongs in the two security-review module copies; deliberation stays here. The plan must reconcile any genuinely conflicting governing text discovered in `AGENTS.md`, its shipped copy or `docs/methodology/dual-review.md`; it must not silently weaken their independent high-risk rule. No new review skeleton field or standing record is proposed.

## Evidence / verification plan

### Tests required

Search direct readers and pins; use `tools/test_tiers.py` for every changed file. Known positive readers include `bootstrap/tests/test_review_and_verification_rules_ship.py` and `bootstrap/tests/test_review_stance_in_shipped_files.py`; open their assertions and selectors before choosing checks. Preserve tests for movement and independent high-risk obligations. Check both local and shipped wording against four cases: unchanged guarded reuse; same-format input from a newly untrusted source; move bypassing validation; non-widening edit to a named high-risk control. Only the first lacks a trigger on those facts.

### Examples / smoke checks

Run relevant claim, link, snippet and neutrality gates and scoped implementation checks, then wide Boundary B on the reviewed final commit. No whole-tree run is authorized by this proposal. The plan must identify installed consumers and exact mapped checks rather than claim prose tests prove secure runtime behavior.

#### Security preflight — five questions, answered in writing

S1: The author and reviewer classify the actual changed source, guard and authority from repository evidence; an author's assertion alone does not decide necessity. S2: Implementation must check that removing the unchanged-contract condition or exempting a bypassed guard fails an applicable rule check; not run at proposal stage. S3: Existing reader tests and prose gates are candidates; the plan must open their triggers and name actual coverage. S4: Uncertainty is resolved by identifying the changed trust relationship, without waiving an accepted obligation or presuming another pass. S5: A misleading classification can still fool reviewers; this clarification is not an authentication mechanism.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A same-format source expansion or guard bypass is excused, an accepted review is dropped without authority, or the wording invents another required record. Withdraw if the current text already resolves guarded reuse unambiguously for readers.

## Scope delta

**Scope delta**: preserved relative to this opening. Compared with issue #37, mandatory necessity lines and relaxed verification for high-risk edits are not delivered. Those are explicit Maintainer choices; this proposal neither closes the whole issue nor concedes its remaining requests.

## Assurance path

**Assurance path**: heavy, with usual and Security Review and a reviewed plan, because this changes shipped security prescription. No new trust boundary is introduced. Elapsed: approximately 8 minutes; tokens: unknown.

## Review -- Codex gpt-6.1-terra -- 2026-11-01

Reviewed commit: ff5c5b0bcd6461717353cf5d7af70460c1ec2979  
Target: entire proposal, especially clarity, burden and scope  
Prior findings: none  
Assurance path: heavy

**Tier**: usual  
**Findings**: raised  
**Verdict**: ACCEPT  
**Elapsed**: approximately 3 minutes  
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: explaining reuse at the existing trigger addresses the reported ambiguity without another field; the actual security boundary needs the separate Security Review. -- Proposal, Context and Proposal.
2. **Best alternative.** Leave the current wording in place; it avoids editing but says only that movement alone does not trigger, not how to assess guarded reuse. -- `templates/modules/team-gated/security-review.md:53-57`; Proposal, Alternatives considered.
3. **What would show it wrong?** Evidence that readers already understand guarded reuse unambiguously, or that the change creates another required record, would undermine the case. -- Proposal, Signals the change is wrong.

**N1 — non-blocking.** The conditional sentence packs six specialist terms into one rule, including “trust class” and “guard reachability,” without defining them. Add brief plain explanations or examples at first use so an adopter can apply the conditions; the HDF5 example in Rationale is a useful start. Evidence: Proposal, Proposal and Rationale.

**N2 — non-blocking.** “Those are explicit Maintainer choices” could suggest decisions have already been made, although the proposal says the remaining issue requests are not delivered. Say they are choices for the Maintainer to make, and preserve the stated loss. Evidence: Proposal, Scope delta and Alternatives considered.

Coverage: Read the committed proposal, template review rules, and current module trigger; assessed clarity, burden and the stated limits. Did not validate the adopter's reported experience, test the wording with adopters, or perform the separate security judgment.
