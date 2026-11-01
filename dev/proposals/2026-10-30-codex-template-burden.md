# Reduce template reading and authoring burden

**Author**: Codex (gpt-6.1-terra), proposal author
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Shorten proposal and plan templates while preserving the rules and the installed templates' independent usability.

## Context

At this commit, `dev/plans/_template.md` and `dev/proposals/_template.md` have 468 and 471 lines; their installed counterparts in `templates/core/dev/` have 464 and 418. Lines are a rough reading-burden indicator, not a target or a measure of duplicated meaning. Both plan templates say a proposal response appends a complete current contract, while `dev/proposals/_template.md` says to revise operative text in place. The accepted `dev/proposals/archive/2026-10-30-claude-cut-the-apparatus.md` chose in-place proposal revision and less continuing burden. The accepted `dev/proposals/archive/2026-10-30-codex-plan-evidence.md` makes one plan file the default and retains required evidence without routine sidecars.

## Proposal

Correct the contradictory plan preambles in both copies. Reduce repeated instructions across the four templates, including external reads, verification records, copy-only guidance and scope delta, by consolidating each rule at a clear point of use and shortening explanatory examples where the rule remains understandable. Treat these as candidates, not a mandate to remove any particular passage. Keep the actual prompts and record fields needed at each lifecycle stage, security and scientific gates, review obligations, scope protection, verification and sidecar rules. Preserve machine-recognized headings, slots and other contracts unless their actual consumers are changed and verified together.

The installed templates must remain usable independently by an adopter with the shipped `AGENTS.md` and `dev/` tree; do not rely on unshipped doctrine to recover an omitted rule. Preserve distinctions between Cairn's own and installed guidance where justified. Do not create new documents, tools, or a line quota. This is a v0.6 proposal, not authorization to implement before Decision and plan review.

## Rationale

The same lifecycle instructions appear in several places a reader must navigate, increasing the chance of drift as well as reading cost. Consolidation within each usable template can reduce that burden while keeping the safety and review obligations at hand. Correcting the specific stale statement removes an observable contradiction.

## Alternatives considered

Fix only the contradiction: smaller, but leaves the recurring burden in four templates. Move detailed rules into doctrine: shorter templates, but installed adopters do not receive that directory and would lose operative guidance.

## Documentation / doctrine surface

The four templates are the proposed operative surfaces; this proposal is deliberation in `dev/`. Search governing and shipped guidance and consumers for affected rules and update existing affected surfaces only if needed to preserve consistency. No new documentation home is proposed.

## Evidence / verification plan

### Tests required

Inventory readers, slot consumers, byte pins and lifecycle checks for all four files before editing; use `python tools/test_tiers.py for <changed paths>` and the mapped tests, including affected installed-template and lifecycle consumers. Verify behavior through real entry points where applicable. A missing rule, changed parser contract, or an installed template that requires unshipped doctrine falsifies the result. The plan must map exact tests and public paths after the inventory; do not assume a negative search without a known-positive control.

### Examples / smoke checks

Run applicable claim, link, snippet and neutrality prose gates and `python scripts/claim_check.py` on the proposal and plan. Identify concrete repeated passages in the plan, then compare final reading and authoring burden with the committed baseline, including added cross-reading and retained duplication; explain if safe cuts prove immaterial. Compare the four final templates against the accepted rules and each other, recording where each obligation remains accessible to its intended reader. Run the required wide Boundary B on a clean final commit after code review; certification and re-anchor are outside this proposal.

#### Security preflight — five questions, answered in writing

S1: The change decides no access or admission; template text is supplied by repository authors and later read by agents and adopters. S2: Removing a required gate or parser marker should be caught by an independent obligation and consumer comparison; the plan must identify and run a concrete mutation for each relevant check. S3: The plan must name each check, its selector and input set, and compare any adopter-facing coverage claim with it; these are not yet measured. S4: No new fallback or parsing behavior is proposed; the plan must assess any discovered consumer behavior before changing it. S5: A hostile contributor with authority to alter accepted rules can still change them; review and the existing trust model remain necessary.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Readers cannot author a valid artifact from the installed guidance, a required obligation becomes ambiguous or absent, consumers break, or the shorter text requires more cross-reading to understand than the original.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance

Authoring templates are a named high-assurance surface; the heavy tier and separate Security Review apply.

## Review -- Codex (gpt-6.1-terra) -- 2026-10-30

```
Reviewed commit: 818933e26433968b1049d3deb39d6c13721d3f29
Target: proposal, four template preambles and selected repetition
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: raised
**Verdict**: ACCEPT
**Elapsed**: 3 minutes (estimated)
**Tokens**: unknown

**Foundations**:

1. **Should this happen as framed?** Yes: correct a real contradiction while keeping adopter guidance usable; both plan preambles prescribe appended proposal contracts, while the accepted apparatus proposal chose in-place revision (`dev/plans/_template.md:33`, `templates/core/dev/plans/_template.md:35`, `dev/proposals/archive/2026-10-30-claude-cut-the-apparatus.md:66`).
2. **Best alternative.** Fix only the contradiction if evidence shows no meaningful safe consolidation; it costs less but leaves repeated guidance, including External-read instructions in the plan templates (`dev/plans/_template.md:98`, `:417`).
3. **What would show it wrong.** A final adopter template that needs unshipped doctrine, loses a required obligation or increases cross-reading would defeat its purpose (proposal, Evidence / verification plan and Signals).

**R1 — Non-blocking:** The proposal names candidate topics but makes every cut optional and gives no before/after burden comparison. A correction alone could satisfy its explicit instructions without delivering meaningful reduction. For the plan, identify concrete repeated passages and compare final reading/authoring burden against the committed baseline, including added cross-reading and any retained duplication; explain if safe cuts prove immaterial. Preserve the independent adopter rules rather than moving them to inaccessible doctrine.

Coverage: reviewed the proposal, accepted in-place decision, plan preambles and selected repetition at the named commit. Did not inventory all template consumers, test pins, or independently assess security controls; those remain for the plan and Security Review.

## Review -- Codex (gpt-6.1-sol) -- 2026-10-30

```
Reviewed commit: 818933e26433968b1049d3deb39d6c13721d3f29
Target: proposal security design and installed-rule preservation
Prior findings: none
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: ACCEPT
**Elapsed**: 6 minutes (estimated)
**Tokens**: unknown

**Foundations**:

1. **Should this happen as framed?** Yes. Consolidating repeated guidance can remove drift without removing gates: the Proposal explicitly preserves security obligations, scientific checks, scope protection and independent installed usability. Both plan preambles contradict in-place proposal revision (`dev/plans/_template.md`, `templates/core/dev/plans/_template.md`, `dev/proposals/_template.md`).
2. **Best alternative.** Correct only that contradiction if consolidation cannot preserve runnable guidance. It retains today's repetition; moving rules to doctrine loses adopter access because installed `AGENTS.md` explicitly says doctrine is unshipped (`templates/core/AGENTS.md`, Where doctrine/ references resolve).
3. **What would show it wrong.** A missing gate, broken machine marker or adopter dependent on unshipped instructions. The proposal already requires obligation comparison, consumer inventory and concrete mutations; their results belong in implementation evidence, not an additional process.

**S1 — Non-blocking:** The header attributes Strategy to gpt-6.1-terra, while `dev/.cairn/model-selection-mapping.yml` assigns Terra medium and Strategy high. The coordinating author reports this was ordinary proposal writing, whose floor is medium. Correct the inaccurate role label to match that assignment.

Coverage: examined committed proposal, current template response/security instructions and installed doctrine boundary. Did not measure shortened templates, inventory all consumers, run implementation checks, or certify adopter behavior; no implementation exists in this review.

## Response -- Codex (gpt-6.1-terra) -- 2026-10-30

**Elapsed**: 2 minutes (estimated)
**Tokens**: unknown

- R1: Accepted. The verification plan now requires concrete candidates and a before/after burden comparison, including cross-reading and retained duplication.
- S1: Accepted. The header now identifies the ordinary proposal-author assignment; the original Strategy label was inaccurate.

### Withdrawn / superseded commitments

None.

## Decision -- Maintainer -- 2026-11-01

**Elapsed**: unknown
**Tokens**: unknown

**Tier**: heavy

**ACCEPTED.** The Maintainer’s authorization, quoted verbatim, in chat on 2026-11-01:

> Accept and implement
