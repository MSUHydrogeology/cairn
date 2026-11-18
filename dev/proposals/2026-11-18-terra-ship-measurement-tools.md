# Ship the existing measurement tools to adopters

**Author**: Terra (Implementation)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-18
**Elapsed**: unknown
**Tokens**: unknown
**Rules that apply**: `dev/rules/conventions.md`, `dev/rules/working-agreements.md`, `dev/rules/protected-surfaces.md`
**In brief**: Give adopters the existing tools for estimating always-loaded text and checking registered counts, with instructions and an empty starting registry.

## Decision summary

Ship two commands that help keep instructions small and published numbers current. The documentation-plan module gains a token-estimate command. Claim-check gains a count-checking command, its support code and an empty settings file for count definitions. For example, an adopter can register the number of files in a directory and check an annotated claim after the directory changes. Both guides gain a usage paragraph. The settings survive upgrades, and the shipped Python stays under integrity checking. Cairn must maintain four added files in the install and upgrade records. Adopters who use the checker review definitions in Git. Token estimates are approximate. Counts come from the adopter project, and history counts need supported Git.

## Context

`tests/token_budget.py` optionally imports a tokenizer. The pair `tests/verify_counts.py` and `tests/measurements.py` bundles Cairn definitions, a pinned Git reader and a Cairn installer import. `tests/check_cairn.py` uses it for Cairn's docs. Copying that pair also derives the wrong project root. Group 4 in `dev/PLANNING.md` calls for an empty adopter registry.

## Proposal

Deliver in v0.8 through the existing module install and upgrade paths. Adapt the current commands and reuse their parsing and measurement code while preserving Cairn's internal entry points, definitions, preset count and audit report. The installed estimator uses the standard-library characters-divided-by-four estimate, labelled in text and JSON. It detects common always-loaded files at the installed project root or accepts a list from the operator. Keep warnings by default and strict caps opt-in.

Seed `dev/.cairn/measurements.json` with an empty object. Read it as data at that fixed location and refuse links that escape the project. Each key selects a dated snapshot or a count of lines, files, Python definitions or commits in a Git revision range. Reject invalid types, unknown fields and duplicate keys. A document annotation only selects a key. Default to the project root above the installed `dev/tools/` directory. A definition may select a project-relative subdirectory as its root. Check containment before reporting an absent root as a skip. Refuse file targets or inspected descendants that resolve outside the selected root. Use a fixed, bounded offline Git read after confirming that the selected root is the worktree root. Treat the validated range only as revisions. The existing helper requires Git 2.45 or later for history reads. Cairn's project-specific preset module count and sibling-checkout measurements stay internal.

Manage only the JSON file as mergeable project state through the existing lock and baseline rules. Manage all three Python files as integrity-checked sources. Reuse the existing caller-pinned helper binding at `dev/tools/git_read.py`, with its unconditional owner and no fallback path. Add each command's purpose, invocation and limits to its module guide. The checker reports zero checks explicitly when the named files contain no annotations, reports skips separately and fails on unknown keys.

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

Use public install, upgrade and integrity commands to check the empty seed, definition preservation and rejection of changed support. Extend `tests/test_manifest.py` and `tests/test_upgrade_module_additions.py`. Through the installed checker, exercise zero checks, match, drift, skip, unknown key, invalid definition, path escape, Git count and rejection of changed helper bytes. Test explicit token files, labelled output and strict caps. Map affected nodes in the plan, including `tests/test_verify_counts.py` where behavior is shared.

### Examples / smoke checks

Run both commands from outside a disposable install. Check the installed roster and guides with applicable prose and release gates.

#### Security preflight — five questions, answered in writing

- **S1:** The operator chooses the modules, install target and input files. The project maintains the JSON definitions. Document authors supply numbers and keys. For snapshots, the reviewed definition supplies the frozen value and date.
- **S2:** Change a cited count to provoke drift. Add an unknown key, supply an escaping target or alter a pinned helper byte to provoke failure. Registry edits must pass integrity verification while a support code edit fails.
- **S3:** Run `python dev/tools/verify_counts.py <file> ...`. The guide will say “The command checks annotations in the named files. The registry starts empty. With no annotations, the command reports zero checks.”
- **S4:** An invalid or missing registry, unknown key, or measurement error fails. An absent contained root skips visibly. Zero annotations report zero checks. Install collision and customization protections still apply.
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
