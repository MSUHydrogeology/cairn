# Next session

*Rewritten from scratch at the 2026-08-19 goodnight. Read
`python tools/lifecycle_planner.py board --compact` first — it is derived and
current; this file is a hand-written orientation and may already be stale.*

## Where the project stands

**`ceremony-as-code` is done and archived.** The re-anchor ceremony is now one
command the Maintainer runs from a launcher an independent review produces — no
agent generating a script, retyping a digest, or improvising a reader. It was
not merely implemented but **performed**: the trust root moved `089a9db` →
`5f992736`, published atomically, and the roster now names a single dedicated
ceremony key (`SHA256:8R549gtP…`), verified end to end.

**No live plans.** Three accepted proposals sit terminal on the board; two of
them want plans (below).

## Start here

1. **5 unpushed commits** (`d091cdd`..`2c9cc57`). Pushing is the Maintainer's.
   `d091cdd` changes `bootstrap/reanchor.sh`, a closure member, so it is **not
   covered by the current anchor** — the next re-anchor needs a fresh M2, as any
   closure change would.
2. **Two accepted proposals await plans**: `2026-08-19-claude-full-suite-interception`
   (a conftest guard refusing collections spanning >40 test files) and
   `2026-08-19-claude-suite-run-diagnostics` (a JSONL cost ledger). Both declare
   `Plan review: required(Internal)`.
3. **`dev/PLANNING.md` carries three `[SEC]` rows filed 2026-08-19** — the
   lockfile's missing regeneration procedure, M2's review/produce conflation,
   and the lasting-truth attestation drift (prose clarified; deliberately not
   mechanised).

## What this session learned that is worth not relearning

**The mechanism held; the guidance did not.** The ceremony took six attempts and
four stalls were the assisting agent's instructions rather than the code — a
placeholder taken literally, a stage-1 rule applied at stage 2 where the answer
is opposite, a values file naming the new key when a rollover must sign with the
old, and stage 1 printing a stage-2 command that routed around a security
property. **Tests that drive commands directly cannot see this class**; two
External Security reviews and a code review passed over it.

**A summary is not the thing.** Three separate agents spent the day acting on
descriptions instead of measurements: a truncated pytest repr read as a result, a
count kept without its failure identities, a convention known by name rather than
by form, a baseline run under the wrong interpreter. Re-derive; do not carry a
figure forward. The AST runbook says this explicitly and was cited by people
doing the opposite.

**Verify in an isolated worktree.** Concurrent sessions hold uncommitted edits in
the shared tree. `test_check_runs_against_the_live_repo_and_reports` always fails
in a plain clone — a clone has no `refs/cairn/gate-anchor`.

**Canonical interpreter is `/Users/kendal30/conda_envs/lhm/bin/python3.13`.**
Running the suite under the system `python` (3.12) produces ~40 spurious
failures.

## Open, not urgent

* `dev/measurement/tag-pass-dispositions.md:56` still calls `ceremony-as-code`
  an active plan. Another session's record to correct.
* The `_has_symlink_component` fence-coverage gap: the interpreter-binding pin
  covers the caller, not the callee implementing symlink-freedom.
* Neutrality gate: **86** pre-existing FAILs, none in ceremony surfaces.
  Redundancy is clean.
