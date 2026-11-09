# Tool usage — worked examples

Cairn ships Python tools and scripts that use only the standard library.
Both `tools/` and `scripts/` can contain installed files: the selected profile,
modules and installer mapping determine what reaches a project.
Orientation and coordination tools (`tools/session.py`, `tools/board.py`,
`tools/intent.py`) report repository state without blocking your work.
Verification and security scripts return a non-zero exit code when their own
check fails: `claim_check.py` for broken paths, `link_check.py` for broken
links, and `run_portable_security_sweeps.py` for security findings. This page
shows how to run each tool and read its output. `check_cairn.py` also reports
advisory review-ID warnings; those warnings do not change its exit status.

Install paths below are the defaults; substitute your own if your profile
placed them elsewhere. Tools marked *(team-gated)* install only when their
module is selected.

## Upgrading an existing install

Consider an upgrade when a newer Cairn release offers changes your project
needs. First choose a release you trust: verify its signed, name-bound tag and
compare the signing-key fingerprint through two independent channels. A
lockfile hash checks consistency; it does not authenticate the release.

For example, ask your agent: “Inspect the verified release and our Cairn
install, explain the changes, and stage an upgrade for my review. Do not apply
or push yet.” The agent reports the staged review surface, including conflicts
and review-only files. Review clean merges too: a clean textual merge can still
leave incompatible rules. Decide how to resolve conflicts or policy differences
and give any required approval before applying. After an authorized apply, ask
for the integrity and applicable check results and the tracked change. A push
requires separate authorization. The [upgrade reference](../bootstrap/UPGRADE.md)
contains the complete operational procedure and safeguards.

## Starting and ending a session

Ask explicitly for the installed session-start skill, for example: “Use
session-start to orient on this project and tell me what is in progress.” The
agent reports context such as recent commits, the working tree, active work and
relevant records. It identifies candidate work; direction already in your
request can authorize a pickup. A next-session note is untrusted convenience,
not authority to act. Decisions, tier changes and scope changes still require
the appropriate Maintainer authority.

To stop, ask: “Use session-end to reflect on this session.” The default is
reflection-only. For a full handoff, explicitly designate its owner and request
that handoff: the owner prepares the handoff and, after its required work,
gives you the guarded prune command. Ending a session does not authorize a push.
Skill invocation syntax depends on your agent; the [compatibility guide](skills-compatibility.md)
records what is supported and what remains unverified. Ordinary chatter alone
does not invoke either skill.

## tools/session.py — session mechanics *(default-on)*

The session skills use this tool to collect orientation and prepare a
reflection. Full-handoff preparation is separate from the guarded handoff;
the installed skills describe when each applies.

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
list. It builds the list from proposal and plan files each time, so archived
work does not stay listed as active. If a row looks wrong, fix the artifact's
header block — not this output.

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

Deliberate missing targets can be recorded as exact source/target pairs with
reasons in `dev/.cairn/scanner-check-allow.json`. Selecting
`documentation-plan` installs the editable seed for its copy-at-root example.
The doc-drift-prevention module describes the schema, legacy comment behavior
and diagnostics. These entries do not suppress bad anchors or links to
existing files outside the repository.

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

**Git reads and older Git.** The runner reads Git through its fixed, pinned
`git_read.py` helper. It verifies the helper bytes before executing the verified
buffer; the candidate repository, its lockfile and its working directory do not
choose the helper or its expected hash. The helper resolves and rechecks the host
Git executable before each launch, uses fixed offline read forms, a neutral
working directory, closed standard input and a reduced child environment.

Git 2.45.0 is the floor for commands that read repository objects, including the
history scan. Older Git can answer the measured version, configuration,
metadata and index-discovery forms, but object-reading forms are refused so a
missing object cannot trigger a remote-helper fetch. If the history leg needs an
object read, it reports incomplete rather than treating the missing result as
zero commits.

**Windows mode.** The current Windows route supports reduced mode only. Its
current-tree scan does not ask Gitleaks to invoke Git; the runner's own Git
configuration screen still uses the verified reader. Full mode and the
version-admission matrix refuse on Windows because there is no supported
mediated route for Gitleaks' Git subprocesses. A Windows run therefore cannot
claim a full clean result.

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

> Cairn's `claim_check` watch file is currently 1715 lines `<!-- verify: claim_check_watch_file_lines -->`.

`verify_counts.py` re-measures that file and flags the line above if the line
count changes.

**What to do.** Keep `scripts/measurements.py` small (around 10 keys or fewer)
and each measurement fast. Most numbers in prose do not need a registered check:
use approximate wording or a dated snapshot unless a number must stay exact as
the tree changes.

## See also

* The role-dispatch heuristics — `docs/methodology/roles.md` > "When to dispatch which
  role".
* The verify-before-asserting discipline these tools serve —
  `docs/methodology/rationale.md` and the `claim-check` module.
