# dev/reflections/ — the per-agent handoff channel

This directory holds **per-agent session reflections**: at the goodnight
routine each agent writes a short retrospective — what it shipped, what went
well, what went wrong and the lesson it leaves. The next session's handoff
owner reads the day's reflections to understand each agent's experience before
writing the next plan.

**Conventions**

* **Per-agent** — each agent writes its own file (e.g. `<date>-<agent>.md`);
  no agent edits another's.
* **Ephemeral + untracked** — reflection files are gitignored and periodically
  pruned; only this `README.md` is tracked (it is the directory's *guide*, not
  a reflection). Durable observations migrate out — to a proposal, the roadmap,
  or doctrine.
* **A retrospective, not a decision surface** — a point that belongs in a
  proposal does not live in a reflection.

See the `reflections` module (`dev/modules/reflections.md`) and your
process-doctrine file for the full convention.
