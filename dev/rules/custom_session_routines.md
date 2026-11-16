# Custom session routines

## Goodnight

**Usage report, every goodnight (reflection-only included).** Run the step
the session-end skill will carry once the meter is installed and enabled
(Maintainer, chat 2026-11-16: "Cairn's should start it--as if the skill were
installed here"). First `python tools/meter.py refresh --json`. If it
completes, render `python tools/gauge.py --pulse --meter-aggregate
dev/measurement/meter.json`. Put the result in the reflection: the token
counts if it completed, or the status and reason exactly as printed (for
example `unavailable` with `source_budget_exceeded`). A refresh that does
not complete is reported as such, never as zero use. Do not commit the
per-project `meter.json` until the Maintainer decides it may be committed.
The refresh reads only the sources and projects named in the private
consent file, `~/.cairn/meter.json`; never edit that file without the
Maintainer's yes.

For a full handoff, run Cairn's local fast/default smoke selection from the
repository root:

```sh
python -m pytest bootstrap/tests/test_profiles_smoke.py
```

Use the canonical project Python 3.13 interpreter. Record the exact command,
result and elapsed time in the handoff, along with its limits: this selection
checks profile parsing, preset expansion and scaffold summaries; it does not
certify the tree or establish general test coverage. A missing selection is
unavailable, and a failed command is failed; neither may be reported as a
pass. Do not add this run for a reflection-only session.

Slow tests remain due at release and whenever an accepted plan, safety or
security requirement, or the Maintainer requires them. Change-specific checks
and Boundary B remain due on their existing schedule. Goodnight does not defer
or replace them.
