# dev/reflections/ — the per-agent handoff channel

This directory holds **per-agent session reflections**: at the goodnight
routine each agent writes a short retrospective — what it shipped, what went
well, what went wrong and the lesson it leaves. The next session's handoff
owner reads the day's reflections (glob `<date>-*.md`, gathering every session)
to understand each agent's experience before writing the next plan.

**Conventions**

* **Per-agent, per-session** — each agent writes its own file, and each
  *session* gets a distinct one: `<date>-<agent>-<session>.md`, where
  `<session>` is the harness session id (or a short **random** token fixed at
  session start — ≥4 hex chars, never a minute-resolution timestamp). This
  keeps concurrent same-agent sessions from clobbering each other. No agent
  edits another's.
* **Ephemeral + untracked** — reflection files are gitignored and periodically
  pruned; only this `README.md` is tracked (it is the directory's *guide*, not
  a reflection). Durable observations migrate out — to a proposal, the roadmap,
  or doctrine.
* **A retrospective, not a decision surface** — a point that belongs in a
  proposal does not live in a reflection.

See the `reflections` module (`dev/modules/reflections.md`) and your
process-doctrine file for the full convention.
