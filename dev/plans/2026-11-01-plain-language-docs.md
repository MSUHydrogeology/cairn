# Plan: Make Cairn's documentation easier to use

**Source proposal**: dev/proposals/archive/2026-11-01-codex-plain-language-docs.md
**Status**: ready-to-implement
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Review Cairn's documentation for clear language while preserving its instructions and technical meaning.

## Source proposal

The Maintainer accepted a heavy review of the README, documentation, existing public methodology, shipped templates and module documents, and the board against Cairn Plain Language 1.0. Improve unclear passages without changing behavior or policy; put the requested marker on shipped templates only.

## Scope

Read all requested prose, including unchanged material, in groups: reader entry points and frequently followed guidance first; remaining `docs/` and board; methodology and its installed operating homes; then remaining shipped templates and module documents. Identify shipped templates through actual install and module mappings, including `bootstrap/_scaffold/config.py`, rather than assuming every file in `templates/` is installed. Read the final committed board, changelog and proposal-summary work; coordinate owners before editing overlaps. A clear document needs no edit. Record group coverage and unresolved failures concisely in the plan; no per-file ledger, evidence folder or extra review stage.

Coordinate with `dev/plans/2026-11-01-retire-doctrine.md`. The methodology has moved to its final public home; review all of it there and account for its installed homes, including split duties. Carry any remaining improvements into the final homes. Avoid polishing the same content twice; do not treat the move itself as the reading review.

Preserve versioned Plain Language rules themselves unless separately authorized. Preserve commands, examples, conditions, warnings, permissions, claims, links and existing non-template markers. Resolve uncertain meaning against its source before editing; leave ambiguous text unchanged and its failure open until resolved. Do not introduce new requirements or policy.

**Reuse.** N/A: no code added. Use existing install mappings, prose gates and tests, not a new audit tool.

### Documentation / doctrine surface

Descriptive prose stays in `docs/`, cross-cutting prescription in governing and installed homes, and board deliberation in `dev/`. Public methodology at `docs/methodology/` and its installed homes are in scope, including duties split across those homes. Shipped authoring templates and methodology are protected surfaces.

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

## Plan review -- Codex (Security Review, gpt-6.1-sol) -- 2026-11-01

Reviewed commit: `d02d0f51e9d7d0a513f285bcb618c7bfbb270575`  
Target: Scope, C1–C4 and Verification  
Prior findings: none  
Assurance path: high-assurance (accepted proposal)

**Obligation**: Internal Security Review  
**Tier**: Internal Security Review  
**Findings**: none  
**Verdict**: No blocking findings. **Elapsed**: approximately 4 minutes; **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. C1–C3 preserve the accepted full reading scope, source meaning and template-only marker. Scope protects permissions and versioned rules; the shipped collaboration document requires versioning for reworded rules (`templates/core/dev/agent_collaboration.md`, Cairn Plain Language).
2. **Best alternative.** Use existing install mappings and checks, and record results by group. C1 uses `bootstrap/_scaffold/config.py`, and Scope excludes new machinery. Both plans coordinate final public and installed homes.
3. **What would show it wrong?** An omitted installed duty, softened prerequisite or marker that corrupts a consumer would defeat the preservation contract. C2–C3 require source comparison and installed-output inspection; Verification requires real entry points and meaningful deletion/inversion checks where needed. The retirement plan separately retains installed reach and path-dependent guards.

Titleless templates remain open unless format-safe placement preserves their consumers. Wide final integration follows both reviews; certification and re-anchor remain unauthorized.

**Coverage:** Compared the committed plan, accepted proposal, retirement coordination, installer mappings, shipped versioned-rule contract and snippet check mode. Did not inventory all readers, perform installs or mutations, run implementation checks or establish future prose equivalence.

## Plan review response -- Codex (plan author) -- 2026-11-01

**Elapsed**: approximately 1 minute; **Tokens**: unknown.

Both reviews found no blocking findings or changes to dispose. Coordinate the methodology reading with the doctrine move and read the final committed board work as Scope already specifies. The plan is ready to implement.

## Implementation verification -- Codex (Implementation) -- 2026-11-01

Closed the quickstart changelog install guidance and fixture: the throwaway
starts with only `README.md`, install supplies the template changelog and a
lockfile, and the install commit includes `CHANGELOG.md`. Added the existing-
history limitation and linked the migration guidance. No installer behavior
changed. Iteration: `python -m pytest bootstrap/tests/test_quickstart_sequence.py
bootstrap/tests/test_review_stance_in_shipped_files.py` — 490 passed in 2.89 s
under Python 3.12.9. Prose gates: claim checks on this plan and quickstart,
quickstart link check, snippet check, and neutrality gate passed. Elapsed:
approximately 8 minutes; tokens: unknown. This is focused iteration evidence;
the plan's final wide Boundary B remains open.

## Coordination -- Codex (plan author) -- 2026-11-01

The board-layout plan owns the single rewrite of `templates/core/dev/PLANNING.md`, including its shipped-template marker. This audit will read its final committed version against the accepted Plain Language and marker requirements without repeating that rewrite. Any remaining failure stays open for resolution. Elapsed: approximately 1 minute; tokens: unknown.

## Focused code review -- Codex (Internal Reviewer, gpt-6.1-sol) -- 2026-11-01

Reviewed commits: `4871b8db`, `14f94b1e` on committed tree `260231cd`  
Verdict: **Blocking finding.** Elapsed: approximately 4 minutes; tokens: unknown.

**Foundations**

1. **Should it happen as framed?** Yes. The clean-install lock writer refuses a differing tracked file, and migration records mergeable files without a recoverable base (`bootstrap/_scaffold/install.py`, `upgrade.py`). The quickstart correctly describes that tradeoff for existing history.
2. **Best alternative.** Keep the README-only starting repository and use the shipped changelog; preserving the old fixture would prevent a clean baseline. Include the changelog in both install-commit instructions.
3. **What would show it wrong?** A real terminal walkthrough that leaves the generated changelog uncommitted defeats the stated outcome; a parity comparison that stops before an operative model-tier obligation would leave drift untested.

**Finding (blocking):** The terminal `git add` command in `docs/quickstart.md` omits `CHANGELOG.md`, although the adjacent agent instruction includes it and the implementation record promises the install commit includes it. A terminal user leaves the new file untracked. Add it to the command and check the actual documented command's resulting commit. The fixture stages the changelog itself, so it does not falsify this omission.

**Evidence:** The model-tier extractor captures the entire current paragraph in both committed copies; separate clause checks retain task floors, authorization and review obligations. Targeted clean Git-backed copy checks under Python 3.12.9: fresh-install node and parity node, 2 passed in 0.27 s. An initial mistyped node selected no tests; corrected above.

**Coverage:** Reviewed the two corrections, relevant lock/migration implementation and committed plan evidence. Did not review the remaining documentation groups, run a suite, or perform Security Review; final wide Boundary B remains open.

## Focused correction -- Codex (Implementation) -- 2026-11-01

Addressed the blocking finding from review commit `6281285f`: the documented
terminal `git add` now includes `CHANGELOG.md`. The quickstart test extracts
and runs the documented `git add` and `git commit` commands, then checks the
resulting commit tree includes the changelog. In a clean Git-backed copy under
Python 3.12.9, the two selected files passed: 490 tests in 3.52 seconds.
Elapsed: approximately 5 minutes; tokens: unknown. This focused correction
returns to the same reviewer for targeted re-look; final wide Boundary B
remains open.
