# Make Cairn's documentation easier to use

**Author**: Codex GPT-6 (Implementation)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Review the requested documentation for plain language so readers can find and follow Cairn's guidance without losing technical precision.

## Decision summary

Review the README, documentation, shipped templates and module documents, and the board against Cairn Plain Language 1.0. Improve passages that make readers work unnecessarily, while preserving instructions and technical meaning. Put the requested Plain Language line under the title of shipped templates only. This is a broad reading task: staging the work makes it manageable, but does not reduce the set to be read.

## Context

The board requests this audit and specifies the template-only marker (`dev/PLANNING.md`, audit row). The 17 rules in `dev/agent_collaboration.md` call for conclusion-first writing, defined terms, useful steps and honest evidence; they require reading, not a readability score. The changelog pass at `ca6cc14d` is an example. The proposal-summary plan is already changing authoring guidance, and the board and changelog have active work; coordinate with their owners and review their final committed text instead of overwriting it.

## Proposal

Inventory the requested prose from the committed tree, including `README.md`, `docs/`, shipped templates and module documents, and the board. Identify installed templates through the actual install and module mappings, not the directory name alone. Read all applicable prose against the 17 rules, prioritizing entry points and frequently followed instructions first, then the remaining materials. Make changes in manageable groups. A document that already communicates clearly needs no edit. Keep commands, examples, conditions, warnings, links, claims, and permissions accurate; resolve uncertain meaning from its source before changing it. Do not introduce new process requirements or change policy under the guise of editing prose.

Place `Written in Cairn Plain Language 1.0` directly below each shipped template's title. Identify how to handle templates without a conventional title in the plan without changing their usable format. Do not add the marker to other documents. Preserve existing non-template markers unless separately authorized to change them. Account for work already completed or underway, including the board and changelog, without claiming their coverage before reading the committed result.

## Rationale

The board asks for the full set, so a priority order is a way to deliver useful improvements early, not permission to skip less-used pages. Reading everything costs more than polishing only the front page, but overlooked instructions can still mislead adopters. Record scope and results by group rather than creating a per-file evidence ledger or a new checklist.

## Alternatives considered

Review only the most visible pages: faster, but leaves the requested templates and module guidance unchecked. Add a score or a permanent audit process: neither establishes comprehension and both add continuing burden. Leave the prose as it is: avoids the work but retains the problems the board asks to address.

## Documentation / doctrine surface

This changes descriptive prose in `README.md` and `docs/`, deliberation on the board, and adopter-facing template and module guidance in `templates/`. Governing instructions remain in their existing governing homes; no new doctrine or changed obligation is proposed. Authoring templates are protected lifecycle surfaces, so their edits retain their existing Security Review and high-assurance obligations.

## Evidence / verification plan

The plan will define the actual inventory, group boundaries, ownership coordination, applicable readers and byte pins before editing, and tests selected by `python tools/test_tiers.py for` the changed paths. Preserve any affected install, fidelity, snippet and template contracts. For each group, inspect the committed changes for meaning and run the applicable claim, link, snippet and neutrality gates and tests that read changed files. A changed command, missing condition, broken link, altered obligation or unsupported marker placement falsifies the result. Use the existing review process, not extra review stages or per-file evidence requirements.

### Tests required

Use the mapped tests and real entry points for changed files and their consumers; the plan will name exact nodes after the inventory and reader search. Run the required final wide Boundary B after review on the clean final commit under Python 3.13, with its scope, commands and results recorded. No full-tree certification or re-anchor is authorized here.

### Examples / smoke checks

Run `python scripts/check_cairn.py` and the applicable prose, snippet and neutrality gates, plus claim checks on proposal, plan and documents before committing. Check that the marker is positioned as requested and that sample instructions retain their original behavior.

#### Security preflight

- **S1:** Existing templates and module guidance supply instructions to adopters and reviewers; authors and maintainers supply the edits. Existing rules and implementation are the sources for intended meaning.
- **S2:** Mapped tests and review must detect a removed condition or altered protected instruction; select and run meaningful mutations where required during implementation. No mutation has been run for this proposal.
- **S3:** The plan will name each affected check, trigger and input set after the inventory. Compare those checks to the actual instructions they protect, not a claim that every prose change is automatically checked.
- **S4:** An ambiguous rewrite must remain unchanged until its meaning is established; it must not silently relax a refusal or grant authority.
- **S5:** A plausible but incorrect rewrite may evade tests and a reading review. Technical source comparison and independent review reduce that risk but cannot eliminate it.

### Independent scientific check

N/A: no scientific assumption or published scientific result is intended to change.

## Signals the change is wrong

Readers lose a necessary condition, examples stop working, protected instructions change meaning, or the audit produces process and documentation burden greater than its benefit.

## Scope delta

None.

## Assurance path

**Assurance path**: high-assurance. The requested shipped authoring templates are protected lifecycle surfaces. The plan will distinguish them from other documentation and retain the applicable ordinary and Security Reviews and checks.
