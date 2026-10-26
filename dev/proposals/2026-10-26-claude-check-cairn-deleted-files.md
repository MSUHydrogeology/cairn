# check_cairn crashes when a tracked Markdown file is deleted but not yet committed

**Author**: Claude (Implementation)
**Status**: awaiting-review
**Review**: usual
**Plan review**: not required(one commit: a one-line filter in `scripts/check_cairn.py`, one new test, and the Maintainer-run gate-manifest re-anchor that a frozen-file edit owes)
**Opened**: 2026-10-26
**In brief**: Make `python scripts/check_cairn.py` skip tracked Markdown files that have been deleted from disk but not yet committed, so it reports findings instead of crashing with a traceback.

## Context

**The check crashes whenever the working tree holds an uncommitted deletion of a tracked `.md` file.** Run on the live tree on 2026-10-26, under Python 3.13 (`/Users/kendal30/conda_envs/lhm/bin/python3.13`), at commit `a8970806`, with two such deletions present (`git status` shows `D dev/strategy/2026-10-19-codex-assai-runtime-architecture.md` and `D dev/strategy/2026-10-19-codex-cairn-and-assai.md`):

```
FileNotFoundError: [Errno 2] No such file or directory:
'/Users/kendal30/Code/cairn/dev/strategy/2026-10-19-codex-assai-runtime-architecture.md'
```

**Cause.** The default scan set comes from `tracked_markdown()` at `scripts/check_cairn.py:177-182`, which runs `git ls-files '*.md'`. That command lists what the git index tracks, and the index still lists a file whose deletion is not committed (`git ls-files -d` prints both paths). `main()` passes that list through `link_check.filter_sources` (`scripts/check_cairn.py:547`; the filter drops archives and vendored directories by path, never by existence) and into `check_tree()`. The first thing `check_tree()` does with each file is read it, at `scripts/check_cairn.py:491` (`md.read_text(...)`), which raises.

**Only that one read is reachable with a missing file.** The other reads of file text (`scripts/check_cairn.py:336` in the incident-tracker check and `:454` in the loop-fidelity check) come after line 491 has already succeeded for the same file. So one filter in front of the loop covers every site; there is nothing to fix at the others.

**Why it matters beyond annoyance.** The gate manifest lists `python scripts/check_cairn.py` as the `check-cairn` gate command, expecting "green" (`bootstrap/tests/fixtures/gate_manifest.json`, `gate_commands`, id `check-cairn`). A deletion in progress, which is an ordinary state during a rename, a move or a cleanup, turns a gate into a traceback with no finding to act on.

**What the check does once past the crash.** I ran it with the two deleted paths filtered out, from a throwaway wrapper outside the repo (it patched `tracked_markdown` to drop paths absent on disk and called `main([])`). It scanned 182 files and returned exit 1 with one finding: `dev/PLANNING.md:42: [path] cited path does not resolve: dev/strategy/2026-10-19-codex-cairn-and-assai.md`. That is correct behaviour: a live document cites a file that is being deleted. A fix must let that finding through, not hide it.

## Proposal

Proposed paths:
- `bootstrap/tests/test_check_cairn_deleted_files.py`

Change `tracked_markdown()` to return only tracked paths that exist on disk:

```python
return [root / line for line in out.stdout.splitlines()
        if line.strip() and (root / line).is_file()]
```

A deleted file has no content to check, so it is not scanned. Files named explicitly on the command line (`check_cairn.py some.md`) are unchanged: naming a path that does not exist is a user error and should still fail loudly.

Add one test that builds a temporary git repository, commits a Markdown file, deletes it from disk without committing, runs the default scan, and asserts it completes and does not scan the deleted file.

## Rationale

The filter is at the source of the list, the single place the missing paths enter, rather than a `try/except` around the read at line 491. A `try/except FileNotFoundError` would also swallow a file that vanishes mid-scan and would hide the cause. One line, and the behaviour reads from the code.

**Why this is a proposal and not a trivial-lane commit.** `scripts/check_cairn.py` is frozen: it has an entry in `frozen_files` in `bootstrap/tests/fixtures/gate_manifest.json` (oid `48679dd7...`). `AGENTS.md` says "a frozen-file edit owes the gate-manifest ceremony", and the manifest goes stale silently, so after the edit the committed manifest is out of date until the Maintainer-run re-anchor (`bootstrap/REANCHOR_RUNBOOK.md`). The code change is small; the ceremony it owes is what makes it more than a simple fix. I did not edit the file.

## Alternatives considered

* **Do nothing.** Costs a traceback in any working tree with an uncommitted deletion, and makes the `check-cairn` gate command unusable in that state. Workaround today: commit or restore the deletion first.
* **`try/except FileNotFoundError` around line 491.** Rejected, as above: broader than the defect, and it would hide a real mid-scan failure.
* **Use `git ls-files --cached --exclude-standard` with `--deleted` subtracted.** Same effect with a second git call and more code than an `is_file()` test.
* **Treat a deleted file as a finding.** Rejected: a deletion in progress is not a defect in the tree, and the useful signal (a live document citing the deleted file) already comes from the link and claim checks, as the run above showed.
* **Do the same fix in `link_check.py` / `claim_check.py`.** Not needed: neither is given the deleted paths by `check_cairn` beyond this list. I did not audit their own standalone default scans; the plan should state whether they share the defect.

## Documentation / doctrine surface

No doctrine, rule text or adopter-facing document changes. The one-line behaviour (deleted files are skipped) belongs in the module docstring's "Scanned set" paragraph at `scripts/check_cairn.py:50` ("the whole tracked Markdown tree"), which would gain "that exists on disk". Routing: descriptive layer, inside the file being edited.

## Evidence / verification plan

### Tests required

* **New test**, in a new file `bootstrap/tests/test_check_cairn_deleted_files.py` (a new file avoids editing the frozen `test_check_cairn_counts.py` and `test_check_cairn_content.py`, which are both in `frozen_files`). Name it for the property, for example `test_default_scan_skips_tracked_markdown_deleted_from_disk`. It must fail before the fix with `FileNotFoundError` and pass after.
* **Owning tests to re-run, scoped**: `bootstrap/tests/test_check_cairn_counts.py`, `test_check_cairn_content.py`, `test_loop_fidelity_gate.py`, `test_security_check.py::test_check_cairn_fails_closed_when_the_interpreter_cannot_be_spawned` (all import or run `scripts/check_cairn.py`; found with `grep -rl check_cairn bootstrap/tests`). Boundary B: this edits a frozen file, so the record is a bounded run only if the reviewer accepts that no contract surface is touched; the gate manifest is part of the install contract, so the Maintainer's call on `full` versus `bounded` applies. Certification comes from the next certifying run, not this change.
* **Live check**: `python scripts/check_cairn.py` on the tree above must complete and report the `PLANNING.md:42` finding, not crash.

### Examples / smoke checks

`python scripts/check_cairn.py` itself. After the re-anchor: `python bootstrap/tests/_gate_manifest.py verify`.

#### Security preflight

N/A: no trust boundary added, moved, or widened. The change narrows the list of files read; it adds no subprocess, parsing or path handling beyond an `is_file()` test on paths git already returned.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

* The new test passes before the fix (it did not reproduce the crash).
* The live run stops reporting `PLANNING.md:42` (the filter hid a real finding).
* A path that exists but is unreadable (permissions) starts being skipped silently; `is_file()` is true for it, so it should still raise. If it does not, the filter is too broad.

## Scope delta

**Scope delta**: preserved

No baseline outcome removed.

## Assurance path

**Assurance path**: high-assurance

Declared high-assurance because the change owes a gate-manifest re-anchor, and the gate manifest is part of the install contract (`AGENTS.md` > "High-risk surfaces"). The code itself touches no trust boundary; if the Maintainer reads the re-anchor as routine ceremony rather than a contract change, `standard` would fit.
