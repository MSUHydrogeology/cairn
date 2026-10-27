# Tool usage — worked examples

Cairn ships a small set of scripts that use only Python's standard library.
Orientation and coordination tools (`tools/session.py`, `tools/board.py`,
`tools/intent.py`) report repository state without blocking your work.
Verification and security scripts (`scripts/claim_check.py`,
`scripts/link_check.py`, `scripts/run_portable_security_sweeps.py`) exit
non-zero when they find a broken path, a broken link, or a security finding.
This page shows how to run each tool and how to read its output.

Install paths below are the defaults; substitute your own if your profile
placed them elsewhere. Tools marked *(team-gated)* install only when their
module is selected.

## tools/session.py — orient at session start and close out at session end *(default-on)*

**What it does.** Gathers the mechanical context at the start and end of a
working session: commits since the last handoff, working-tree status, active
proposals and plans, active file claims, and the resolved Python interpreter.
At session end, `--drain` releases any file claims held by your agent.

```bash
python tools/session.py session-start
python tools/session.py session-end --agent "<your-agent>" --drain
```

**What to do.** Run `session-start` at the beginning of a session and read only
the in-flight proposals or plans relevant to your task. Run `session-end` when
wrapping up a session so the next session starts from a clean state.

## scripts/claim_check.py — verify path and line claims *(default-on: claim-check)*

**What it does.** Reads a Markdown proposal, plan or doc and flags file paths
that do not exist and line numbers that are out of range. Run it while you
write and before you commit a proposal or plan.

```bash
python scripts/claim_check.py dev/proposals/2026-06-01-me-new-thing.md
```

A clean file:

```
claim_check: dev/proposals/2026-06-01-me-new-thing.md -- OK, no claim-check flags.
```

A file with problems (exit code 1):

```
claim_check: ... -- 1 hard flag(s):
  ...:42: [path] cited path does not resolve: `frontend/helpre/util.py`
```

**What to do.** Fix a hard flag before committing: correct a typo in the path
or line range, list a planned or external path under a
`Proposed/Untracked/External-repo paths:` line in the document, or declare a
document-scoped path exemption in `dev/.cairn/claim-check-allow.json` (or a
one-off `<!-- claim-check-allow: <glob> -->` directive).

## tools/intent.py — claim work before editing *(team-gated: coordination-tiers)*

**What it does.** On a concurrent team, you claim a set of files before
editing them so a second agent sees the claim and coordinates rather than
colliding. The post-commit hook auto-releases your claim.

```bash
python tools/intent.py claim --files frontend/prep/soils.py tests/test_soils.py \
    --action "fix soil-temp fold-in"
# ... edit, commit (the post-commit hook releases the claim) ...
python tools/intent.py list            # what is claimed right now, by whom
```

First-session setup (opt-in; the scaffold never mutates `.git/hooks`):

```bash
python tools/intent.py install-hook        # post-commit auto-release
python tools/intent.py install-precommit   # pre-commit work-intent check (warn-only)
python tools/intent.py hooks-status        # confirm both are installed
```

**What to do.** If a pre-commit warning says a staged path has no active
claim, either claim it or proceed deliberately — the check is warn-only, not a
gate. If `list` shows a path held by another session, coordinate before
editing it.

## tools/board.py — see what is actually in flight *(default-on)*

**What it does.** Prints one row for every proposal and plan under `dev/`: kind, artifact, status, the Review and Plan review lines, when it opened, its source proposal, and any `Waiting on Maintainer` line. With `--maintainer` or `--json` it also reads the `dev/PLANNING.md` rows that declare a wait. `--json` prints the same board as plain JSON (`cairn-board/1`), so you can build your own view without scraping the table; see [`docs/build-a-board-view.md`](build-a-board-view.md). It only reports what the artifacts say and skips symbolic links. The one check it makes is on the status word: if an active proposal or plan carries a retired status (such as `proposed`) or a value that is not a status, it adds an advisory line naming it, and still lists the artifact. `session-start` prints the same advisory under its in-flight threads. The artifact is the authority; this is a view of it.

```bash
python tools/board.py
python tools/board.py --maintainer
python tools/board.py --json
```

**What to do.** Run it instead of maintaining a hand-written "currently active"
list. A derived view cannot go stale the way a table does; the failure mode it
replaces is a board still describing archived work as in flight. If a row looks
wrong, fix the artifact's header block — not this output.

## scripts/link_check.py — check cross-references resolve *(team-gated: doc-drift-prevention)*

**What it does.** Resolves the Markdown links across your tracked docs and
reports the ones that do not. A tracked file that is deleted from disk but not
yet committed is skipped, and the run prints how many it skipped.

```bash
python scripts/link_check.py                 # whole tracked tree
python scripts/link_check.py docs/guide.md   # specific files
python scripts/link_check.py --check-external # also probe http(s) links
```

**What to do.** Fix a broken internal link before committing the doc change
that introduced it; treat it as the link sibling of a `claim_check` path flag.
External-link probing is opt-in (slower, network-dependent) — run it at
release-prep, not every edit.

## scripts/run_portable_security_sweeps.py — one measured offline secret sweep *(team-gated: portable-security-sweeps)*

This runs a local secret scan. It needs Gitleaks installed, and it never reports "clean" unless it fully ran.

**Installation check.** The module installs three files as one group:
`scripts/run_portable_security_sweeps.py`,
`scripts/portable_security_policy.json`, and
`dev/modules/portable-security-sweeps.md`. If they are not there, the module is
not selected in your profile.

**It installs no scanner.** You supply **Gitleaks** on `PATH` yourself. `git`
must also be present — the runner calls it for a pre-execution configuration
screen, and Gitleaks calls it transitively for the history leg.

```bash
python scripts/run_portable_security_sweeps.py --target .
python scripts/run_portable_security_sweeps.py --json    # deterministic summary
python scripts/run_portable_security_sweeps.py --security-verification
```

**Offline by default, and there is no other mode.** No network flag exists; the
child environment drops every inherited proxy variable.

**Two version modes.** **full** requires the resolved binary's SHA-256 to match a
digest the project's admission ceremony recorded for your exact
`(version, platform, architecture)`; only full mode can report `0`. **reduced** is
what you get otherwise: real current-tree findings, and an honest `INCOMPLETE`
instead of a clean result it has not earned. A **recorded** digest that does not
match is a contradiction, not an absence, and degrades.

**How to read the exit code.**

| Exit | Meaning | What to do |
|---|---|---|
| `0` | CLEAN — every leg ran in full mode and found nothing | nothing; it is a tripwire that did not trip, not a proof |
| `5` | INCOMPLETE — a leg did not fully run | read the named reason: absent binary, shallow clone, non-Git export, or an unadmitted version |
| `10` | FINDINGS | triage each; suppress only by adding a **reviewed fingerprint** to the policy |
| `20` | DEGRADED — a refusal, or a result the runner will not trust | do not treat as clean; the reason names the control that fired |

Precedence is `20 > 10 > 5 > 0`, so a finding is never hidden behind an
incomplete sibling leg. `NOT APPLICABLE` is distinct from `INCOMPLETE` and never
weakens another leg.

**Suppressions.** The policy carries reviewed fingerprints and nothing else — no
path, argv, environment variable, executable, config file, baseline, digest or
version. A `.gitleaksignore` found *inside* the tree under check is a **refusal**
(exit `20`), not a suppression source.

**Admitting a new adapter version** — an operator act, never part of a sweep and
never reachable from a standing command:

```bash
python scripts/run_portable_security_sweeps.py \
    --verify-version-support /abs/path/to/candidate \
    --confirm-executing-an-unadmitted-binary
```

It **executes a binary the project has not admitted**, says so in its first line
of output, and emits an evidence record. It never admits anything itself:
admission is a reviewed source change.

## For Cairn maintainers: scripts/verify_counts.py — re-measure registered counts

*This script is for Cairn's own maintainers. It is not installed in your project, so skip this section unless you work on Cairn itself.*

**What it does.** Checks that numbers cited as current facts in Cairn's own
documentation still match the repository. Each checked number is registered in
`scripts/measurements.py` and followed in the Markdown file by an HTML comment
naming its registry key: `<!-- verify: <key> -->` placed immediately after the
number on the same line. The comment holds only a registry key—never a file
path or shell command—so checking a document never runs arbitrary commands.

```bash
python scripts/verify_counts.py docs/tool-usage.md
```

The registry supports two entry types:

* **`Invariant`** — re-measured against the live tree every time `verify_counts.py`
  runs. If the number in the document no longer matches the measured value, the
  script exits non-zero. If an entry depends on a sibling checkout that is not
  present on disk, the script reports `SKIPPED (root absent: …)` with a distinct
  non-zero exit code rather than passing silently.
* **`Snapshot`** — a historical measurement tied to an ISO `as_of` date on the
  same line (placed before the number or after the comment, not between them).
  The script checks that the number and date match the recorded snapshot without
  re-measuring the live tree.

Worked example (the number and its comment share one line):

> Cairn's `claim_check` watch file is currently 1704 lines `<!-- verify: claim_check_watch_file_lines -->`.

`verify_counts.py` re-measures that file and flags the line above if the line
count changes.

**What to do.** Keep `scripts/measurements.py` small (around 10 keys or fewer)
and each measurement fast. Most numbers in prose do not need a registered check:
use approximate wording or a dated snapshot unless a number must stay exact as
the tree changes.

## See also

* The role-dispatch heuristics — `doctrine/roles.md` > "When to dispatch which
  role".
* The verify-before-asserting discipline these tools serve —
  `doctrine/rationale.md` and the `claim-check` module.
