# Ship the existing measurement tools to adopters

**Author**: Terra (Implementation)
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-18
**Elapsed**: unknown
**Tokens**: unknown
**Rules that apply**: `dev/rules/conventions.md`, `dev/rules/working-agreements.md`, `dev/rules/protected-surfaces.md`
**In brief**: Give adopters the existing tools for estimating always-loaded text and checking registered counts, with instructions and an empty starting registry.

## Decision summary

Ship two commands that help keep instructions small and published numbers current. The documentation-plan module gains a token-estimate command. Claim-check gains a count-checking command, its support code and an empty settings file. For example, an adopter can name a count of documentation files `docs-files` in both the settings and the annotation beside the published number. Both guides gain a usage paragraph. The settings survive upgrades, and the shipped Python stays under integrity checking. Cairn must maintain four added files in the install and upgrade records. Adopters review definitions in Git. Token estimates are approximate. Counts come from the adopter project, and history counts need supported Git.

## Context

`tests/token_budget.py` optionally imports a tokenizer. The pair `tests/verify_counts.py` and `tests/measurements.py` bundles Cairn definitions, a pinned Git reader and a Cairn installer import. `tests/check_cairn.py` uses it for Cairn's docs. Copying that pair also derives the wrong project root. Group 4 in `dev/PLANNING.md` calls for an empty adopter registry.

## Proposal

Deliver in v0.8 through the existing module install and upgrade paths. Adapt the current commands and reuse their parsing and measurement code while preserving Cairn's internal entry points, definitions, preset count and audit report. The installed estimator uses the standard-library characters-divided-by-four estimate, labelled in text and JSON. It detects common always-loaded files at the installed project root or accepts a list from the operator. Keep warnings by default and strict caps opt-in.

Seed `dev/.cairn/measurements.json` with an empty object. Read it as data at that fixed location and refuse links that escape the project. Each key selects a dated snapshot or a count of lines, files, Python definitions or commits in a Git revision range. Reject invalid types, unknown fields and duplicate keys. A whole key in either input must match the inherited grammar `[\w-]+`, allowing one or more Unicode alphanumeric characters, underscores or hyphens. An annotation supplies only a key. Treat an HTML comment beginning with `verify:` after optional whitespace as an attempted check. Fail malformed or unclosed markers and markers without a preceding number on the same line.

Default to the project root above `dev/tools/`. A definition may select a project-relative subdirectory. Check containment before reporting an absent root as a skip. Refuse file targets and child links that resolve outside the selected root. For a Git count, confirm the resolved Git worktree root equals the selected root. Use the existing bounded offline read, reject option-shaped ranges and put the validated range before a final `--` so Git reads revisions only. History reads require Git 2.45 or later. Cairn's preset module count and sibling-checkout measurements stay internal.

Use existing lock and baseline rules to keep the JSON mergeable and all shipped Python integrity-checked. Reuse the pinned helper at `dev/tools/git_read.py` under its unconditional owner with no fallback path. Document each command's use and limits. Report zero checks when there are no markers. Report skips separately with exit 3 when there are no failures. An unknown key fails.

| Module | Source | Installed path |
|---|---|---|
| documentation-plan | `templates/modules/default-on/token_budget.py` | `dev/tools/token_budget.py` |
| claim-check | `templates/modules/default-on/verify_counts.py` | `dev/tools/verify_counts.py` |
| claim-check | `templates/modules/default-on/measurements.py` | `dev/tools/measurements.py` |
| claim-check | `templates/modules/default-on/measurements.json` | `dev/.cairn/measurements.json` |

Proposed paths:
- `templates/modules/default-on/token_budget.py`
- `templates/modules/default-on/verify_counts.py`
- `templates/modules/default-on/measurements.py`
- `templates/modules/default-on/measurements.json`
- `dev/tools/token_budget.py`
- `dev/tools/verify_counts.py`
- `dev/tools/measurements.py`
- `dev/.cairn/measurements.json`

## Rationale

A small data reader reuses the counters and limits definition edits to choosing what gets counted.

## Alternatives considered

Leaving both internal avoids install maintenance and leaves adopters to assemble the tools themselves. An editable Python registry reuses the current import but gives each definition edit authority to run code as the operator and conflicts with the existing adopted-Python integrity gate.

## Documentation / doctrine surface

Update the installed module guides, published install inventory, tool descriptions and release records.

## Evidence / verification plan

### Tests required

Use public install, upgrade and integrity commands to check the empty seed, definition preservation and rejection of changed support. Extend `tests/test_manifest.py` and `tests/test_upgrade_module_additions.py`. Through the installed checker, exercise zero checks, match, drift, exit 3 for an absent contained root, unknown key, invalid definition, direct and child-link escapes, a valid Git count and rejection of changed helper bytes. Reject `docs.files` as a definition key. With a valid registry, also fail a document whose only marker uses `docs.files`. A range with missing revisions must fail even if a file has that name. Test explicit token files, labelled estimates and strict caps. Map affected nodes in the plan, including `tests/test_verify_counts.py`.

### Examples / smoke checks

Run both commands from outside a disposable install. Check the installed roster and guides with applicable prose and release gates.

#### Security preflight — five questions, answered in writing

- **S1:** The operator chooses the modules, install target and input files. The project maintains the JSON definitions. Document authors supply numbers and keys. For snapshots, the reviewed definition supplies the frozen value and date.
- **S2:** Change a cited count to provoke drift. Add an unknown key, supply an escaping target or alter a pinned helper byte to provoke failure. Registry edits must pass integrity verification while a support code edit fails.
- **S3:** Run `python dev/tools/verify_counts.py <file> ...`. The guide will say “The registry starts empty. The command checks markers in the named files. Malformed markers fail. With no markers, it reports zero checks.”
- **S4:** An invalid or missing registry, malformed marker, unknown key or measurement error fails. An absent contained root skips visibly with nonzero status. Install collision and customization protections still apply.
- **S5:** A registry editor can change what a key counts, including its date and value for a snapshot, so the adopter reviews definitions in Git. The checker dispatches only the fixed operations. The operator still trusts the installed Python entry point and host Git.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A normal install cannot execute the tools, local entries disappear on upgrade, or maintaining the definitions costs more than the measurements save.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance. The plan and implementation require ordinary and Security reviews because this changes the install contract and adopter-executed Python.

## Review -- Terra (Reviewer) -- 2026-11-18

Reviewed commit: 1122369eabd6a40e9831ac16fec2753270657672

**Tier**: usual
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: delivering both existing tools with their support and guides gives adopters usable measurements while preserving their own registry on upgrade. -- `dev/PLANNING.md`, Proposal, Evidence / verification plan
2. **Best alternative.** Leaving the tools internal avoids install and upgrade maintenance, but forces adopters to assemble the checker and its dependencies themselves. -- `tests/verify_counts.py`, `tests/measurements.py`
3. **What would show it wrong.** A real fresh install that cannot run the commands, or an upgrade that loses a registered adopter measurement, would falsify delivery. -- Proposal, Evidence / verification plan

The proposal accounts for the paired checker and support, including the eagerly verified Git helper; its plan must resolve their installed paths and ownership. The current support derives its root from its present location, so copying it into `dev/tools/` unchanged would not suffice. The proposed fresh-install and upgrade checks exercise that risk. The high-assurance path and separate Security Review are appropriate for adopter-executed code and the changed install contract. -- `tests/measurements.py`, `install/_scaffold/config.py`

The guide paragraphs route use to the installed modules and preserve the key-only annotation duty; no existing rule is proposed for removal. Coverage: read the board, installer mappings, tools and proposed checks; did not execute the tools or upgrades, determine the final registry design, or assess the security boundary. No test suite was run.

## Review -- Sol (Security Review, High) -- 2026-11-18

```text
Reviewed commit: 73c2a6c5723c6d6b1b50767ec97b54417b67e04e
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Ship both tools once the installed defaults and upgrade boundary are explicit. The mapping and adopter-executed Python warrant the heavy lane. `install/_scaffold/config.py:1044-1058`, `dev/rules/protected-surfaces.md`.
2. **Best alternative.** Reuse the existing core-owned Git helper and keep mutable definitions separate from integrity-checked measurement code. `install/_scaffold/config.py:908-917`, `install/_scaffold/lockfile.py:175-200`.
3. **What would show it wrong?** A public install and upgrade that loses a local count, accepts drift or an escaping measurement target, or executes a changed Git helper falsifies delivery. `tests/test_upgrade_module_additions.py:241-273`, `tests/test_verify_counts.py:537-579`, `tests/test_verify_counts.py:649-660`, `tests/test_verify_counts.py:814-823`.

- **Blocking — define the registry boundary.** The checker executes its sibling registry on import. Its support derives the root from its current location and can import Cairn's own installer. Specify the adopter root, the existing helper's canonical path, and the supported operations without Cairn's installer. Separate mutable definitions from shipped executable support. Say whether definitions are parsed data or explicitly trusted project code, who reviews changes, and which files remain integrity-checked. Verify integrity still accepts registry customization and rejects changed shipped support after upgrade. `tests/verify_counts.py:59-79`, `tests/measurements.py:49-61`, `tests/measurements.py:271-302`.
- **Blocking — define honest defaults.** The estimator automatically imports optional third-party code. Use a labelled standard-library estimate in the installed command. The checker exits successfully on zero matches. Make the empty seed and zero verified claims explicit in the command and guide, while preserving unknown-key failure and distinct visible skips. Exercise these through the installed commands. `tests/token_budget.py:52-61`, `tests/verify_counts.py:191-246`, `RULES.md`.

Coverage: committed source and named test paths, with no implementation, installer, command, suite or platform execution.

## Response -- Sol (Strategy, High) -- 2026-11-18

**Elapsed**: unknown
**Tokens**: unknown

- **Registry boundary:** accepted. A JSON definitions file stays in the existing mergeable project-state class. The adopted-Python source gate in `templates/modules/team-gated/run_security_audit.py` hashes every adopted Python file, so exempting an editable Python registry would either break that check or weaken it. The shipped support stays checked. The currently installed Git helper and the source in `templates/skills/_lib/git_read.py` have matching bytes and the existing caller pin. The proposal names the root, supported operations and adopter review authority. The count checker needs changes to its support and loading path as well as its command.
- **Honest defaults:** accepted. The installed estimator always uses the labelled standard-library estimate. The checker distinguishes zero checks, skips and failed claims. A parsed empty seed contains no Cairn-specific definitions.

The new public JSON input was a design option in the first Security Review, but that pass could not assess the chosen schema and authority. A focused second Security pass should check whether the declared fields can select an escaping target or an unintended Git read and whether the single integrity exclusion leaves Python checked. I inspected source and checked the helper digest. Installer, upgrade and runtime behavior remain unverified.

### Withdrawn / superseded commitments

The review draft's executable registry becomes data. Cairn's preset module count and sibling-checkout behavior remain available through its internal tools. The installed command covers its own project, with distinct skips for absent subdirectories.

## Review -- Sol (Security Review, High, pass 2) -- 2026-11-18

```text
Reviewed commit: 1a760b4732bb7af7d55bc7b3dae91d9185c27b0c
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes, once accepted keys can all be checked. Fixed operations and key-only annotations keep registry edits out of executable support. -- Proposal, `tests/measurements.py:294-302`
2. **Best alternative.** Keep both tools internal. With the single JSON exclusion, adopters can edit definitions while both Python checks and the upgrade baseline stay in place. -- `install/verify_integrity.py:434-467`, `install/_scaffold/upgrade.py:2050-2084`, `templates/modules/team-gated/run_security_audit.py:876-906`
3. **What would show it wrong.** An installed upgrade loses an edited definition, or the installed checker accepts changed Git helper bytes, an escaping child link, or a range-shaped filename as valid history. -- Evidence / verification plan, `tests/measurements.py:223-235`, `tests/test_verify_counts.py:814-823`

- **Blocking — make registry and annotation keys agree.** The inherited matcher ignores `<!-- verify: docs.files -->`, so an accepted JSON key `docs.files` could yield a clean zero-check report. Use the same key grammar for both inputs and fail malformed verify markers. Exercise an invalid key and malformed marker through the installed command. -- `tests/verify_counts.py:59-66`, `tests/verify_counts.py:94-114`
- **Non-blocking — carry these checks into the plan.** Keep skips nonzero. In Git 2.53.0, `log --oneline missing-left..missing-right` returned a commit for a file with that name. Appending `--` made the same input fail. Check that the revision-only call rejects that file, and compare the resolved Git top level with the selected root. The probe distinguished a linked worktree from a plain subdirectory. -- `tests/verify_counts.py:191-197`, `tests/measurements.py:253-268`, `install/_scaffold/install.py:487-511`

Coverage: the new data boundary and a disposable Git probe. The earlier ordinary review still covers the shipping goals. Installed commands, upgrades, other platforms and suites were outside this pass.

## Response -- Sol (Strategy, High) -- 2026-11-18

**Elapsed**: unknown
**Tokens**: unknown

- **Key grammar and malformed markers:** accepted. Both inputs use the inherited key grammar in `tests/verify_counts.py:63`. The proposal pairs a valid key example with negative checks for a dotted key in the registry and a dotted marker in a document. A malformed marker fails even if the file contains no valid annotations, reserving zero checks for files with no markers.
- **Git, links and skips:** carried into the plan requirements. History selects the resolved worktree root and leaves Git's path list empty. The plan must exercise a filename that matches an invalid revision range, an escaping child link and a visible skip with exit 3.

This resolves how the reviewed registry reaches the existing operations. I read the inherited parser and exit status. I did not repeat the Git probe or run the proposed installed checks.

### Withdrawn / superseded commitments

None.

## Decision -- Maintainer (scribed by Antigravity Gemini 4 Hydrogen) -- 2026-11-18

**Tier**: heavy

**ACCEPTED.**

> "Yes, please accept all four as revised."

This accepts the v0.8 measurement-tools proposal as revised (`heavy` tier), shipping `token_budget.py`, `verify_counts.py`, `measurements.py`, and the empty mergeable `dev/.cairn/measurements.json` data registry. Adopters review definition edits in Git; zero new Cairn recurring human operations.

**Elapsed:** under 1 minute. **Tokens:** unknown.
