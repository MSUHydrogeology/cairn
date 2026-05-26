# Vendor wrapper — {{project_name}}

> **This is the thin vendor-wrapper template.** Cairn ships it as
> `VENDOR.md`; **rename it to your AI tool's own file** — `CLAUDE.md`,
> `GEMINI.md`, `.github/copilot-instructions.md`, or whatever your
> harness auto-loads — so the tool reads it on entry. Keep the wrapper
> **thin**: it carries *only* habits specific to that one tool.

@AGENTS.md

<!-- The line above imports the shared, vendor-neutral AGENTS.md so an
agent reading this wrapper gets the project's required reading, the
`dev/` tree, the lifecycle, the roles, and the operational reference —
single-sourced. The `@path` import directive is itself tool-specific:
some harnesses auto-load a named file, some support an `@import`, some
need the path inlined. Adjust this one line to your tool; do not copy
AGENTS.md's content down here. -->

## Tool-specific habits

<!-- cairn:slot vendor-addendum -->
(Harness-specific habits only — the things an agent of a *different*
tool would not need: this tool's session/context model, its scratch
directory, its keyboard or command quirks, how a context-compaction or
resume event should trigger re-orientation. **Do not** restate the
development environment, the test command, the required reading, the
session routines, the CLI, or the conventions — those live in
`AGENTS.md`, and this wrapper points there. If you find yourself
copying a rule from `AGENTS.md`, delete it and rely on the import
above. An empty slot is valid for a tool with no special habits.)
<!-- cairn:end vendor-addendum -->

---

**Drift guard.** This file stays thin by construction. Anything an
agent of a *different* tool would also need belongs in `AGENTS.md`
(shared) or `CONTRIBUTING.md` (human-facing), not here. A wrapper that
has grown to duplicate the test command, the git rules, the routines,
or the required-reading list has drifted into a fat fourth doc — fold
that content back to its single source and leave only the pointer.
