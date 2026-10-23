# Tool usage — worked examples

Cairn ships a few small scripts that use only Python's standard library.
Each one does a cheap, mechanical check so you do not have to remember it.
They advise; none of them blocks your work. This page shows how to run each
one and what to do with its output.

Install paths below are the defaults; substitute your own if your profile
placed them elsewhere. Tools marked *(team-gated)* install only when their
module is selected.

## claim_check — verify path / line claims

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

**What to do.** Fix a hard flag before committing (a real broken path, or a
forward-reference you must *mark* with a `Proposed/Untracked/External-repo
paths:` line, or — for a single cross-document citation — a document-scoped
`<!-- claim-check-allow: <glob> -->` directive).

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

**What it does.** Prints one row for every proposal and plan under `dev/`: kind, artifact, status, the Review and Plan review lines, when it opened, its source proposal, and any `Waiting on Maintainer` line. With `--maintainer` or `--json` it also reads the `dev/PLANNING.md` rows that declare a wait. `--json` prints the same board as plain JSON (`cairn-board/1`), so you can build your own view without scraping the table; see [`docs/build-a-board-view.md`](build-a-board-view.md). It only reports what the artifacts say, skips symbolic links, and makes no judgments. The artifact is the authority; this is a view of it.

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
reports the ones that do not.

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

**What it does.** The **live-invariant** leg of the three-kind numeric-claim
discipline. When `claim_check` retired its category-D count soft-flag, the
*decision-irrelevant* and *snapshot* kinds were handled by doctrine (approximate;
date) — but a count cited as **present fact** and prone to drift (a headline
file size re-quoted across docs as it changes) is registered in a code-side
registry (`scripts/measurements.py`) and re-measured here. **Not installed into
adopters** (not in `_CORE_MAPPINGS`); it dogfoods on Cairn's own docs.

A doc annotates the number with `<!-- verify: <key> -->` **immediately after the
number it verifies** (RR1 — the verifier reads the number directly preceding the
annotation on that line; for a `Snapshot`, put the `as_of` date before the number
or after the annotation, not between them). The annotation carries **only a
registry key** — never a path, never a command — so there is no document-supplied
path and no shell surface (every measurement is root-contained; `git` runs
`shell=False`).

```bash
python scripts/verify_counts.py docs/tool-usage.md
```

Two kinds dispatch from the registry: an **`Invariant`** is re-measured today and
the annotated number compared to it (a mismatch is **drift**); a **`Snapshot`** is
**never re-measured** — only its value-equality and the presence of the ISO
`as_of` date on the line are checked (re-running would erase the evidence the
snapshot is). An `Invariant` whose `root` is an **absent** sibling checkout
degrades to a **visible** `SKIPPED (root absent: …)` (a distinct non-clean exit
status), never a silent pass; an **unregistered** key is **refused**.

Worked example (the number and its annotation share one physical line, per RR1):

> Cairn's `claim_check` watch file is currently 1704 lines `<!-- verify: claim_check_watch_file_lines -->`.

`verify_counts` re-measures it and flags that line if the two ever diverge.

**What to do.** Keep the registry **small** (soft cap ~10 keys) and each
measurement cheap (a bounded stdlib scan or `git log` range) — there is no cache
by design. If the verifier ever runs slowly or the registry churns more than the
docs drift, that is the **curation-tax kill-signal**: shrink or freeze the
registry, do not accelerate it. Most numbers are decision-irrelevant — approximate
them; reserve a registered invariant for the few that are cited as live fact and
genuinely drift.

## See also

* The role-dispatch heuristics — `doctrine/roles.md` > "When to dispatch which
  role".
* The verify-before-asserting discipline these tools serve —
  `doctrine/rationale.md` and the `claim-check` module.
