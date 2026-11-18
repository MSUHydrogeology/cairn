# Vendor wrapper — {{project_name}}
Written in [Cairn Plain Language 1.0](dev/agent_collaboration.md).

@AGENTS.md

For a client that needs a wrapper, use its auto-loaded file and keep it thin: only habits specific to that one tool. The import line above gives the tool the shared `AGENTS.md`; adjust that one line if the tool imports another way. A client that loads `AGENTS.md` directly needs no wrapper.

## Tool-specific habits

<!-- cairn:slot vendor-addendum -->
(Harness-specific habits only: this tool's session and context model, scratch directory, command quirks, and how a context compaction or resume should trigger re-orientation. Do not restate the test command, required reading, routines or conventions; they live in `AGENTS.md`. An empty slot is valid.)
<!-- cairn:end vendor-addendum -->

---

**Drift guard.** Anything an agent of a different tool would also need belongs in `AGENTS.md`, not here. A wrapper that duplicates the test command, git rules, routines or required reading has drifted: fold that content back to its single source and leave the pointer.
