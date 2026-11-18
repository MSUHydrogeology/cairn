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

Adopters cannot install two existing Cairn tools that help keep instructions small and numbers current. Add the token estimator to the documentation-plan module and the count checker to claim-check, each with a short installed guide paragraph. The count checker also needs its measurement support and an initially empty registry that adopters can maintain without losing their entries on upgrade. The changes add installed files and maintenance of their release and upgrade records; count definitions still require human work. The estimator may use a clearly labelled approximation, and neither tool makes a count correct by itself. Cairn's separate audit report remains internal.

## Context

`tests/token_budget.py` detects common always-loaded files or accepts an explicit list, labels its estimator, and warns by default; `--strict` is optional. `tests/verify_counts.py` loads sibling `tests/measurements.py`, whose registry currently contains Cairn-specific entries and whose verified Git helper is loaded eagerly. Copying the checker alone cannot work. The installer maps module files in `install/_scaffold/config.py`; the selected modules already install guides and tools. The board's Group 4 row records the Maintainer's direction to ship these tools with an empty adopter registry.

## Proposal

Deliver in v0.8 through the existing module installation and upgrade paths. Ship the existing token estimator with documentation-plan and the existing count checker with claim-check under `dev/tools/`. Supply the measurement support and any existing pinned helper it actually needs, using the existing verified helper and install ownership mechanisms; provide an empty adopter registry rather than Cairn's entries. Preserve the checker's key-only annotations, contained measurement behavior, visible skips and refusal of unknown keys. An adopter can add reviewed measurements and retain them through normal upgrades; use the existing managed-customization and baseline mechanisms rather than silently replacing their work. Keep Cairn's own measurements and `tests/audit_report.py` internal.

Add a concise paragraph to each installed module guide: purpose, invocation, limitations and how to supply the applicable file list or register counts. Explain the approximation and opt-in strict mode for token estimates, and the empty starting registry for counts. Update applicable published install inventory, lock and release-quality records through existing processes. Keep shipped code standard-library-only. If implementation needs a new runtime trust boundary or a design beyond these existing contracts, stop for strategy and review before choosing it.

## Rationale

These are working tools with a direct purpose for adopters. Shipping their necessary support and guidance makes the existing capability usable without prescribing a new reporting system.

## Alternatives considered

Leave both internal: no install maintenance, but adopters must build or copy the same tools and reconcile their dependencies themselves.

## Documentation / doctrine surface

Installed module guides in `templates/modules/default-on/` carry usage and the relevant practice; published install and tool descriptions reflect the delivered paths. No governing methodology change is proposed.

## Evidence / verification plan

### Tests required

Exercise the real installer and upgrade entry points with the relevant modules selected: a fresh install has working tools and an empty registry, and an upgrade preserves a registered adopter measurement. Extend existing manifest and module-upgrade tests for missing support or overwritten customization. Through installed commands, check a known registered count, a mismatched count and an unknown key; check the estimator's explicit files, labelled estimate and opt-in strict cap. A missing helper, Cairn registry entry, lost customization or silent unknown-key success falsifies delivery. Use existing `tests/test_manifest.py`, `tests/test_upgrade_module_additions.py` and relevant tool tests, selecting affected nodes in the plan.

### Examples / smoke checks

Run the installed commands in a disposable project and the applicable prose and quality gates; use the published manifest and existing release checks to confirm the installed roster. No full certification is implied.

#### Security preflight — five questions, answered in writing

- **S1:** The installer receives module selections and target paths from the operator; the count checker reads document annotations and a project-maintained code registry. An annotation supplies a key, not executable code or a path.
- **S2:** An unknown key must fail; a deliberately wrong registered count must report drift. A changed helper must fail its existing pinned verification. Exercise these negative controls on the installed delivery.
- **S3:** The installed checker is invoked on named documents and checks their annotations against the registry. The installed guide must say this same scope and its initial empty state; its final wording is reviewed against the actual command.
- **S4:** Unknown keys and measurement errors report failure; missing roots are visible skips. The estimator labels its fallback and strict mode is opt-in. Existing install collision and customization protections remain in force.
- **S5:** A document author can choose annotations but cannot supply a command through one; a person able to alter the executable registry can still change what it executes. Review that project-owned code before trusting it.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A normal install cannot execute the tools, project entries disappear on upgrade, or maintaining the registry costs more than the measurements save.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance. The installer contract and adopter-executed Python change; the engine change also requires Security Review. A plan is needed to specify the exact existing ownership and helper handling before implementation.
