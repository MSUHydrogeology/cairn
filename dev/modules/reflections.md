# Module: reflections

**Selected when:** default-on — kept by every multi-agent
adoption. A solo, single-agent project may omit it; without a
second agent to hand off *to*, the cross-agent function the
channel exists for is absent (a reflection becomes a personal log).
**Adds to:** a section in `dev/agent_collaboration.md`, plus a
`dev/reflections/` directory with a tracked `README.md` guide (the
per-agent reflection entries themselves stay untracked).

The reflections channel is the **cross-agent handoff surface**: at
the goodnight routine each agent writes a short, per-agent
retrospective, and the next handoff reads them. It is what lets a
new session pick up where another agent left off — the durable
record carries decisions; the reflections carry the *experience*
of getting there.

## Template content

Merged into `dev/agent_collaboration.md` (or its equivalent
process-doctrine file):

> **Reflections.** At the goodnight routine each agent writes a
> short, per-agent reflection — what it shipped, what went well,
> what went wrong and the lesson it leaves — to a per-session file
> in an untracked `dev/reflections/` directory. Reflections are:
>
> * **per-agent, per-session** — each agent writes its own, and each
>   *session* writes a distinct file (`<date>-<agent>-<session>.md`) so
>   concurrent same-agent sessions never share a path and cannot clobber
>   one another. The `<agent>-<session>` tail is the filename's last
>   component so it reads as one identity string. `<session>` is, in
>   resolution order: **(1)** the per-session token of the
>   coordination/intent identity *when that module is installed* — `python
>   tools/intent.py whoami --session-token` (the 8-hex `sha256` of the
>   harness session id), so the `<agent>-<session>` tail reconstructs the
>   intent log's `agent` field and a reflection links to its session's
>   `dev/intents.jsonl` entries; **(2)** else the raw harness session id
>   where exposed; **(3)** else a short **random** token fixed at session
>   start (≥4 hex chars — never a minute-resolution timestamp, which
>   re-collides under concurrent start). No agent writes or edits another's;
> * **ephemeral** — reflection files are untracked and periodically
>   pruned (only the directory's tracked `README.md` guide persists);
>   durable observations migrate to doctrine or the roadmap;
> * **a cross-agent handoff surface** — the goodnight owner reads
>   the day's reflections (glob `dev/reflections/<date>-*.md`, every
>   session) to understand each agent's experience before writing the
>   next session's plan.
>
> A reflection is a retrospective, not a decision surface — a
> point that belongs in a proposal does not live in a reflection.

A solo, single-agent project may keep this as a personal log or
omit it entirely; the cross-agent handoff function only earns its
keep with a multi-agent team.
