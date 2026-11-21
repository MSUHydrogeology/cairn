# Conventions

Cairn's dependency and file-naming conventions. Routed from `RULES.md`. The text below moved from `AGENTS.md` on 2026-11-10 unchanged.

Everything Cairn ships to adopters is standard-library-only. Read
`install/DEPENDENCY_BUDGET.md` before adding an import. Place prescription in
`AGENTS.md`, deliberation in `dev/`, and software description in `docs/`, per
`dev/DOCUMENTATION_PLAN.md`.

Files use uppercase names for landmarks and lowercase-kebab for content.
Plans use `<YYYY-MM-DD>-<slug>.md`; proposal and strategy files use
`<YYYY-MM-DD>-<author>-<slug>.md`. Keep test code, scripts and assets in
canonical homes. Code is MIT, prose/templates CC BY 4.0, and the brand mark
CC BY-ND.

Cairn's retry budget. Moved from `dev/agent_collaboration.md` > "Agent execution retries" on 2026-11-10 unchanged: This local budget overrides immediate escalation for ordinary execution; the shipped rule and broader methodology remain unchanged.


## Code style

The [human guide](../../docs/style_guide.md) explains these practices. Keep
the guide and these conventions aligned; optional preferences may drift.
When they disagree, follow binding routed conventions and higher-level rules,
report the discrepancy and propose a correction. No style preference permits
a security, dependency or license exception.

- Use the existing canonical home and nearby public interface.
- Name functions and variables clearly; follow the surrounding file's style.
- Keep command entry points small and report actionable failures.
- Group imports clearly; check the dependency budget before adding one.
- Add types where they clarify an interface and follow existing annotations.
- Preserve input data and make units and assumptions explicit when relevant.
- Test public promises and meaningful refusals, not private implementation wording.
- Keep tests, scripts and assets in their canonical homes.
- Preserve notices and apply the correct license to new work.
- Explain unusual decisions; do not add a rule for a merely different preference.
