# check_cairn crashes when a tracked Markdown file is deleted but not yet committed

**Author**: Claude (Implementation)
**Status**: revising
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

## Review -- Claude (Reviewer, Sonnet) -- 2026-10-26

```
Reviewed commit: 4c5bc159
Target: the whole proposal, weighted to the stated cause, the claim that one filter covers every site, the gate-manifest cost, and what the proposal leaves out
Prior findings: none
Assurance path: high-assurance (as declared)
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Foundations**:

1. **Should this happen as framed?** Yes. The cause is the one stated, and the two-line filter in `tracked_markdown()` is the right size. I reproduced the crash and the fix in a detached worktree of `4c5bc159`: before the fix, `python scripts/check_cairn.py` ends in `FileNotFoundError` at `scripts/check_cairn.py:491`; after it, the run completes (M2, M3 below).
2. **Best alternative.** Doing nothing is allowed but weak: the workaround is to commit or restore the deletion first, and an in-flight deletion is the normal state when two agents share a tree. The strongest real alternative is to fix the shared helper once instead of one of its copies (RV1). The author's `try/except` alternative is correctly rejected.
3. **What would show it wrong.** A tracked path whose absence from the scan hides a finding. I tried that case and the finding survives (M5). What the proposal does not yet show is that the same defect sits in two sibling scripts (RV1, M4).

### Verdict in brief

**Revise, then decide.** The proposal should exist and its code change is correct. Three things need an answer before you decide:

* **The same defect lives in two other scripts, and one of them ships to adopters (RV1).** The proposal says it did not audit them. I did: both crash the same way.
* **The re-anchor it says this change owes is already owed (RV2).** That changes what the change costs you, and the order it should land in.
* **The test does not pin the property the proposal says matters most (RV3).** A fix that hid real findings would pass it.

### Steelman

The proposal keeps a gate script from turning an ordinary state, a deletion in progress, into a traceback. It finds the one place the missing paths enter. It refuses the broader `try/except`. It says out loud that the fix must let the real finding through, and it ran the check with the deletions filtered to show that it does. It declares its own cost (a frozen-file edit) and why that makes it a proposal. The strongest form: one filter at the source, no new name, one new test file.

### What I measured

Detached worktrees of `4c5bc159` in my scratch directory, Python 3.13 (`/Users/kendal30/conda_envs/lhm/bin/python3.13`), both removed afterwards. The main tree was not written. `CAIRN_FULL_SUITE` was not set.

| # | Measurement | Result |
|---|---|---|
| M1 | Claims against the tree | `scripts/check_cairn.py:177` is `tracked_markdown`, `:547` is the `filter_sources` call, `:491` is the first read, `:336` and `:454` are later reads (`check_tree` reaches `_check_incident_tracker_schema` and the internal-ref check only after `:491`), `:50` is the "Scanned set" line. `tracked_markdown` has one caller in `check_cairn` (`:548`). `git ls-files -d` printed both deleted paths. All as the proposal says |
| M2 | Crash, then fix, in the worktree with the two `dev/strategy/` files removed | Before: `FileNotFoundError` on the first deleted path. After the two-line change: exit 1, 183 files, two findings. The proposal's "182 files, one finding" was taken at `a8970806`; its own file is the 183rd, and the second finding is explained in M6 |
| M3 | The proposal's new test, written as described (temporary git repo, commit a file, delete it, run `main(["--root", ...])`) | Fails before the fix with `FileNotFoundError`, passes after. With the fix: the three `check_cairn` test files plus my 3 probe tests, 19 passed in 0.29 s. On the unfixed file the owning tests also pass (50 passed, adding `test_notice_install.py`, `test_gate_manifest.py` and the `test_security_check.py` node) |
| M4 | The other default scans, same deletion, same worktree | `scripts/link_check.py` and `scripts/sync_doc_snippets.py` both end in `FileNotFoundError`: each has its own copy of the same `tracked_markdown` (`scripts/link_check.py:491`, `scripts/sync_doc_snippets.py:249`). `scripts/claim_check.py` takes one file, so is not affected. `diff -q` reports both scripts byte-identical to `templates/modules/team-gated/link_check.py` and `.../sync_doc_snippets.py` |
| M5 | Does the filter hide a real finding? A temporary repo with `keep.md` linking to `gone.md`; `gone.md` committed, then deleted | Exit 1 and `keep.md:1: [link] broken link target: gone.md`. The finding survives |
| M6 | Clean checkout of `4c5bc159`, nothing deleted | `check_cairn` reports 1 issue across 185 files: `dev/reviews/2026-10-18-security-review-session-writes.md:131` cites a build-cache directory that is gitignored and exists only in a tree where Python has run. So the `check-cairn` gate is already red on a fresh checkout, with or without this change |
| M7 | `python bootstrap/tests/_gate_manifest.py verify` on the main tree (read-only) | Already reports a HOLD: `FROZEN-MODIFIED` and `FROZEN-OID` for `bootstrap/tests/test_quickstart_sequence.py`. In the worktree with the fix and a new test file, it adds `FROZEN-MODIFIED: scripts/check_cairn.py` and records the new test nodes as `COLLECTION-ADDED` (allowed) |

### Findings

**RV1 -- Medium -- blocking for the Decision: the Response states what happens to the two sibling copies.**
**The same defect is in `link_check.py` and `sync_doc_snippets.py`, and `link_check.py` is shipped to adopters.**

*Plain.* `tracked_markdown()` exists in three scripts as a copy. The proposal fixes one and says "I did not audit" the others. I ran them (M4): two crash on an uncommitted deletion exactly as `check_cairn` does. `link_check.py` is a shipped module with a byte-identical twin, so an adopter hits this in their own tree during any rename.

*Evidence.* M4. `AGENTS.md` says to generalize rather than copy, and `check_cairn` already imports `link_check` (it calls `link_check.filter_sources` at `scripts/check_cairn.py:547`).

*Recommendation.* Two ways to close it; the author decides.
* **Widen now.** Fix `tracked_markdown` in `link_check.py` and `sync_doc_snippets.py` (each with its template twin), and have `check_cairn` call `link_check.tracked_markdown` so there is one copy of that function to fix. All of these are frozen, so they ride the same re-anchor (RV2) at no extra ceremony. The cost is a shipped-template change and a second review round, because widening is new scope. I think this reaches the cause; the narrow change leaves two known crashes.
* **Keep it narrow and name the rest.** State in the Response that the siblings are unfixed and why, and queue a row for them. The easy-defect permission in `AGENTS.md` does not cover them: it reaches only files the work already edits.

Either way, "Not needed" in Alternatives and "the plan should state whether they share the defect" cannot stand: they do share it, and the Plan review line says no plan is written.

**RV2 -- Medium -- non-blocking: the proposal's cost statement is out of date. The re-anchor is already owed.**
**This edit adds one file to a ceremony the Maintainer already has queued.**

*Plain.* The proposal says the committed manifest "is out of date until the Maintainer-run re-anchor". It is already out of date for another file (M7), and `dev/PLANNING.md:100` queues the re-anchor, "one frozen test changed". So this change costs nothing extra if it lands before that ceremony. If the re-anchor runs first, it costs a second ceremony.

*Satisfier.* The Response names the ordering ("land before the queued re-anchor") and says who updates the `dev/PLANNING.md` row, whose "one frozen test changed" and "no engine symbol changed" wording would no longer be true. That edit belongs at a serialization point, not in this commit.

**RV3 -- Low -- non-blocking: the test should pin "the real finding survives".**
**The proposal's own bar is not in its test.**

*Plain.* Context says "a fix must let that finding through, not hide it". The test it proposes asserts only that the scan completes and skips the deleted file. A different fix that swallowed every flag would pass it. The "live check" meant to cover this cites `dev/PLANNING.md:42`, which stops being true when the other agent's deletion is committed or that line is edited, and which a later reader cannot reproduce.

*Satisfier.* Add one assertion to the new test, as in M5: a surviving file links to the deleted one, and the run exits 1 with that link flagged. It passed under the fix. Drop the live check as an acceptance criterion, or label it a one-off observation.

**RV4 -- Low -- non-blocking: three statements to correct or add.**

* **`test_security_check.py` does not run `check_cairn`.** The node named in Tests required (`bootstrap/tests/test_security_check.py:500`) patches `subprocess.run` and never runs or imports it, so "all import or run" is wrong for that node. The real consumer is `security_check.run_check_cairn` (`bootstrap/security_check.py:959`), which runs `check_cairn` on the live tree in the release security check; `docs/release-process.md:84` names it too. This strengthens the motivation (the release check would also stop on a deletion in progress). Cite it, instead of the gate manifest alone.
* **A tracked Markdown symlink whose target is gone** also crashes today (I tried it) and would be silently skipped after the fix, because `is_file()` is false for it. That may be right, but the Signals section lists only the unreadable-file case. Say which way it should go.
* **The skip is silent.** After the fix a scan of "182 files" says nothing about the files left out. A one-line note on stderr ("skipped N tracked file(s) deleted from disk") would keep the count honest. Optional; if taken, the test asserts it.

**RV5 -- Low -- non-blocking: the declared assurance path and the Boundary B wording.**
Nothing in this change edits the gate manifest or its schema; only a pinned hash changes, through the same ceremony every frozen edit owes. `standard` fits at least as well as `high-assurance`; if you keep `high-assurance`, say what it adds here. On Boundary B, `AGENTS.md` makes `full` the rule when a contract surface is touched, and the full run is the next certifying run, so "the Maintainer's call on full versus bounded" is not a call. The record is scoped with `Certified by: pending`.

**Observation, no satisfier here.** M6: the `check-cairn` gate is red on a clean checkout because of one review citing a build-cache directory. It is separate from this proposal. The proposal is right that a deletion turns the gate into a traceback; it is not the only reason the gate is not green on a fresh clone. Worth a row, not a change here.

### What I tried to break

* **Fix hides a finding.** M5: it does not.
* **Fix swallows a real failure.** An explicitly named missing path (`check_cairn.py gone.md`) still raises `FileNotFoundError` with the fix applied, as the proposal says.
* **Other read sites.** Listed from the tree (`read_text` in `scripts/check_cairn.py`: `:336`, `:454`, `:491`); the loop order puts `:491` first.
* **Unreadable file.** Not run. `is_file()` follows `stat`, which succeeds on an unreadable file, so it should still raise. Unverified.

Coverage -- **Covered**: lens 1 (claims: M1, M2, M7), lens 2 (production path: M3 calls `main()`, not a helper), lens 3 (edge cases: deleted file, dangling symlink, explicit path, citing doc, M5), lens 4 (silent skip: RV4), lens 5 (sibling copies and consumers: M4, RV1, RV4), lens 6 (drift: file and finding counts, M2/M6; the PLANNING row, RV2), lens 7 (re-anchor placement: RV2), lens 9 (each finding names a satisfier). Lens 8 does not apply. **Not covered / low confidence**: I did not run the full suite or a certifying run (not mine to run); I did not run `bootstrap/reanchor.sh` or look past the runbook's opening and `_gate_manifest.py verify`; I did not test an unreadable file or a Windows path; I did not check whether widening to the shipped templates (RV1) disturbs the adopter upgrade path or any pin outside `_gate_manifest.py`.
