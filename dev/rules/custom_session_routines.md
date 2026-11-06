# Custom session routines

## Goodnight

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
