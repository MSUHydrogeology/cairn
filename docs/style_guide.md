# Cairn code style guide

Keep this guide and `dev/rules/conventions.md` aligned when either changes.
Optional style preferences may drift; report a discrepancy and propose a
correction. Routed agent conventions govern coding decisions under higher-level
rules. Neither this guide nor drift permits an exception to security,
dependency or licensing duties.

Cairn's code should be easy for a research team to inspect and change. This
human-facing guide explains common practices; the short agent conventions keep
working instructions close at hand. For prose, use [Cairn Plain Language](plain-language.md).

| Area | Working preference |
|---|---|
| Dependencies | Shipped code uses the standard library; check the dependency budget before imports. |
| Layout | Keep installation in `install/`, development tools in `dev/tools/`, and tests in `tests/`. |
| Names | Use clear lowercase names for functions and variables; content files use lowercase-kebab names. |
| Python | Use annotations where they clarify interfaces; many modules postpone annotation evaluation. |
| Commands | Keep entry points small and make failures visible with useful diagnostics and exit status. |
| Tests | Exercise public promises and meaningful refusal cases, not implementation wording. |

## Imports and dependencies

Check `install/DEPENDENCY_BUDGET.md` before adding an import. Code shipped to
adopters is standard-library-only. Group imports clearly and use existing
project patterns; an import's availability does not establish permission to
add a dependency.

## Files and interfaces

Use a canonical home rather than a parallel copy. Landmarks use uppercase
names; content uses lowercase-kebab names. Keep a module's purpose and public
entry point visible, use descriptive names and make diagnostics actionable.
Several tools accept output streams for testing; follow the local interface
when extending one rather than forcing a new pattern on unrelated code.

## Types, tests and licensing

Many Python modules use `from __future__ import annotations`; match the file
and add types where they help the reader. Prefer a small test of an external
promise to a test of a private helper. Code is MIT, prose and templates are
CC BY 4.0, and the brand mark is CC BY-ND; preserve existing notices and add
appropriate notices to new work. These descriptions do not replace routed
rules or the project's review and verification requirements.
