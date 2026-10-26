# Vendor wrapper — Cairn (Claude Code)

> **Thin vendor wrapper.** This is Cairn's own renamed copy of the
> shipped `templates/core/VENDOR.md`, pointed at Claude Code's
> auto-loaded file. It carries *only* habits specific to this one tool.
> Codex and other harnesses read the shared `AGENTS.md` directly; their
> tool-specific habits, if any, belong in their own wrapper, not here.

@AGENTS.md

<!-- The line above imports the shared, vendor-neutral AGENTS.md so an
agent reading this wrapper gets the project's required reading, the
`dev/` tree, the lifecycle, the roles, and the operational reference —
single-sourced. Adjust this one import line per tool; do not copy
AGENTS.md's content down here. -->

## Tool-specific habits

<!-- cairn:slot vendor-addendum -->
- **Context compaction or resume is a context-loss event.** When Claude
  Code summarizes/compacts this session, or you resume after a break, do
  not assume continuity — re-run the `session-start` orientation before
  substantive work (see `AGENTS.md` > Session start). The summary is a
  re-entry point, not proof you are still oriented.
- **Skills.** The `session-start` and `session-end` routines live under
  `.agents/skills/`; `session-start` self-heals a `.claude/skills`
  symlink so this harness surfaces them as slash commands. Invoke them
  rather than improvising the routine.
- **Pass the model on every new agent call.** An agent resumed with
  `SendMessage` is assumed to keep the model it started with (not checked
  here), so start a fresh lower-tier agent for new work instead of
  resuming a higher-tier one.
- **Durable state lives in the repo, not in tool memory.** Claude Code's
  persistent memory directory is private to this harness and is not
  shared with Codex or a human reviewer. Anything that must survive a
  handoff goes in the committed `dev/` tree (a proposal, a strategy
  note, the roadmap boards), never only in memory.
<!-- cairn:end vendor-addendum -->

---

**Drift guard.** This file stays thin by construction. Anything an
agent of a *different* tool would also need belongs in `AGENTS.md`
(shared), not here. A wrapper that has grown to duplicate the test
command, the git rules, the routines, or the required-reading list has
drifted into a fat fourth doc — fold that content back to its single
source and leave only the pointer.
