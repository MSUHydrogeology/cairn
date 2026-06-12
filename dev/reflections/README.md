# dev/reflections/ — the per-agent handoff channel

This directory holds **per-agent session reflections**: at the goodnight
routine each agent writes a short retrospective — what it shipped, what went
well, what went wrong and the lesson it leaves. The next session's handoff
owner reads the day's reflections (glob `<date>-*.md`, gathering every session)
to understand each agent's experience before writing the next plan.

**Conventions**

* **Per-agent, per-session** — each agent writes its own file, and each
  *session* gets a distinct one: `<date>-<agent>-<session>.md` (the
  `<agent>-<session>` tail reads as one identity). `<session>` resolves, in
  order: **(1)** the coordination/intent per-session token when that module is
  installed — `python tools/intent.py whoami --session-token` — so the
  `<agent>-<session>` tail equals the intent log's `agent` field and the
  reflection links to its session's `dev/intents.jsonl` entries; **(2)** else
  the raw harness session id where exposed; **(3)** else a short **random**
  token fixed at session start (≥4 hex chars, never a minute-resolution
  timestamp). This keeps concurrent same-agent sessions from clobbering each
  other. No agent edits another's.
* **Ephemeral + untracked** — reflection files are gitignored and periodically
  pruned; only this `README.md` is tracked (it is the directory's *guide*, not
  a reflection). Durable observations migrate out — to a proposal, the roadmap,
  or doctrine.
* **A retrospective, not a decision surface** — a point that belongs in a
  proposal does not live in a reflection.

See the `reflections` module (`dev/modules/reflections.md`) and your
process-doctrine file for the full convention.
