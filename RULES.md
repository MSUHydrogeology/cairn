# Cairn's project rules

The few rules that apply every turn when working on Cairn, and where the detail lives. Cairn adopts itself, so this is the project router that `dev/rules/README.md` describes. Keep it small.

## Bright lines

- Run only the tests that name a changed file. Never set `CAIRN_FULL_SUITE=1` except for the Maintainer's certifying run.
- Only the Maintainer re-anchors, pushes, or merges.
- Code Cairn ships to adopters is standard-library-only.
- `AGENTS.md`, `CLAUDE.md` and `RULES.md` together stay at or under 1,500 words.

## Where to read more

| When you | Read |
|---|---|
| are asked for a certifying run | `dev/rules/certifying-runs.md` |
| edit an engine, a protected test, a manifest, the interpreter binding or the portable sweeps | `dev/rules/protected-surfaces.md` |
| add an import, name a new file, or retry a failed step | `dev/rules/conventions.md` |
| decide, ask the Maintainer, brief an agent, edit the roadmap or changelog, or run or cut tests | `dev/rules/working-agreements.md` |
| set up a machine to run Cairn's checks | `dev/rules/development-environment.md` |
| run goodnight | `dev/rules/custom_session_routines.md` |
