# Reduce template reading and authoring burden

**Author**: Codex (gpt-6.1-terra), Strategy
**Status**: awaiting-review
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

Run applicable claim, link, snippet and neutrality prose gates and `python scripts/claim_check.py` on the proposal and plan. Compare the four final templates against the accepted rules and each other, recording where each obligation remains accessible to its intended reader. Run the required wide Boundary B on a clean final commit after code review; certification and re-anchor are outside this proposal.

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
