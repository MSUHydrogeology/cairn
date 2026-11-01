# Plan: Make Cairn's documentation easier to use

**Source proposal**: dev/proposals/archive/2026-11-01-codex-plain-language-docs.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Review Cairn's documentation for clear language while preserving its instructions and technical meaning.

## Source proposal

The Maintainer accepted a heavy review of the README, documentation, existing public methodology, shipped templates and module documents, and the board against Cairn Plain Language 1.0. Improve unclear passages without changing behavior or policy; put the requested marker on shipped templates only.

## Scope

Read all requested prose, including unchanged material, in groups: reader entry points and frequently followed guidance first; remaining `docs/` and board; methodology and its installed operating homes; then remaining shipped templates and module documents. Identify shipped templates through actual install and module mappings, including `bootstrap/_scaffold/config.py`, rather than assuming every file in `templates/` is installed. Read the final committed board, changelog and proposal-summary work; coordinate owners before editing overlaps. A clear document needs no edit. Record group coverage and unresolved failures concisely in the plan; no per-file ledger, evidence folder or extra review stage.

Coordinate with `dev/plans/2026-11-01-retire-doctrine.md`. While its move is not ready, work on other groups and review current methodology if waiting would otherwise indefinitely delay the audit. Carry finished improvements into the move. If it moves first, account for and read all relocated content at its final public and installed homes, including split duties. Avoid polishing the same content twice; do not treat the move itself as the reading review.

Preserve versioned Plain Language rules themselves unless separately authorized. Preserve commands, examples, conditions, warnings, permissions, claims, links and existing non-template markers. Resolve uncertain meaning against its source before editing; leave ambiguous text unchanged and its failure open until resolved. Do not introduce new requirements or policy.

**Reuse.** N/A: no code added. Use existing install mappings, prose gates and tests, not a new audit tool.

### Documentation / doctrine surface

Descriptive prose stays in `docs/`, cross-cutting prescription in governing and installed homes, and board deliberation in `dev/`. Public methodology currently in `doctrine/` and its final public and installed homes are in scope; relocation remains the separate plan's work. Shipped authoring templates and doctrine are protected surfaces.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Inventory requested groups and installed templates, readers, pins and checks; coordinate overlapping owners and relocation timing | Plan reviews | Concise group scope and check mapping in implementation record |
| C2 | Read and improve entry points, frequently followed guidance, remaining docs and board | C1; coordinate owners | Clearer reader-facing prose |
| C3 | Read methodology at current or final homes and remaining shipped templates and module documents; add template markers | C1; coordinate relocation and owners | Reviewed guidance and markers |
| C4 | Ordinary and Security Reviews; fix findings and run final wide integration | C2–C3 and iteration evidence | Review and verification records |

## Acceptance criteria

### C1

Inventory the requested prose from the committed tree and actual install/module mappings, identify titles and format constraints for shipped templates, and search for readers, byte pins and applicable checks. Test negative searches against a known positive. Map checks to their triggers, input sets and real entry points before editing; record group boundaries and coordination. Unresolved meaning or a required check keeps its group open.

### C2–C3

Read every inventoried group against all 17 rules and improve failures without changing intended behavior. Compare changes to their sources, retain the versioned rules, and preserve existing non-template markers. Place `Written in Cairn Plain Language 1.0` directly below each shipped template title only. For a titleless template, use an existing format-safe title or add a format-safe title and marker only if its consumers retain their behavior; if neither is possible, keep that group open for resolution. Inspect installed output and real consumers where relevant. Account for all methodology content, including installed splits, and record unresolved failures by group until closed. No scope is silently dropped.

### C4

Independent ordinary and Security Reviews inspect the committed implementation and iteration evidence; review fixes receive the required targeted look. Final wide Boundary B covers the reviewed range and review fixes on a clean final commit. Unmet criteria and checks block archive.

## Scope delta

**Scope delta**: preserved.

## Verification

**Boundary A:** Before editing, run `python tools/test_tiers.py for <changed paths>` and its selected tests during iteration. Search actual readers and pins, follow each named check to its trigger and runner, and compare checks with the instructions they protect. Run applicable claim, link, snippet and neutrality gates, including `python scripts/check_cairn.py`, `python scripts/claim_check.py` on documents before commit, `python scripts/link_check.py`, `python scripts/sync_doc_snippets.py` in check mode where applicable, and `python scripts/quality_gate.py --sub neutrality`. Preserve snippet sources, installed output and fidelity contracts. Exercise real entry points and meaningful deletion or inversion mutations where required to establish that affected checks detect lost conditions or altered protected instructions; report omissions and failures. Inspect markers and sample instructions for placement and unchanged behavior.

**Boundary C:** A reviewer other than the implementer reads committed changes and iteration evidence and runs only targeted falsification checks, not a suite. The separate Security Review remains required. A fix beyond a failing test returns for the required targeted look.

**Boundary B:** After review, run the mapped iteration and integration/workflow selections and applicable standing gates in wide mode on a clean, unchanged final commit under canonical Python 3.13. Record tested SHA and range, interpreter, pre/post state, commands and counts, elapsed time, tokens or `unknown`, non-pass dispositions, omissions, timing misses and slow-test reporting. Keep missing checks open.

## Plan review -- Codex (Internal Reviewer, gpt-6.1-sol) -- 2026-11-01

Reviewed commit: `7e12719f`  
Obligation: Internal  
Verdict: No blocking findings. Elapsed time: approximately 2 minutes; tokens: unknown.

**Foundations**

1. **Should it happen as framed?** Yes. The accepted proposal calls for the full prose set, preserved meaning and a marker only on shipped templates. Scope and C1–C3 cover those outcomes, identify installed templates from actual mappings, and retain versioned rules.
2. **Best alternative.** Wait until the doctrine move is complete before reading methodology. This avoids a possible repeat, but risks indefinite delay; Scope instead permits reading now and carrying improvements forward, or reading all final homes and splits if the move happens first. The separate retirement plan leaves the reading review here.
3. **What would show it wrong?** An unread relocated duty, a lost condition or a marker that breaks a template would falsify the result. C2–C3 require source comparison, all methodology content, and format-safe placement; Verification maps checks to actual consumers.

The group-based sequence gives useful priorities without a per-file ledger or new audit machinery. Its plain language makes the sequence and stopping conditions clear. Coordination and reading the final board, changelog and proposal-summary work prevent assuming those changes complete the broader audit.

**Coverage:** Compared the committed plan with the accepted proposal and doctrine retirement plan, including scope, sequencing and verification. Did not inventory every template or reader, run implementation checks, or assess future edits; separate Security Review remains due.
