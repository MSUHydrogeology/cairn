# Cairn test maintenance

## Which test files Linux and Windows run at certification

*This section is for Cairn's own maintainers. It is not installed in your project.*

At certification the Mac runs the whole suite once. Linux and Windows run the files `python tests/tier_inventory.py cert-files` prints: every test file except the release-only files (next paragraph) and the files `tests/test_tiers.json` lists under `system_independent`. On Windows, `cert-files --host windows` also keeps the release-only files listed for Windows. A listed file has no sign that its outcome depends on the operating system, so it runs on the Mac only. An unlisted file counts as system-dependent and runs everywhere. Add a file to the list only with evidence that it has no such sign (links, permissions, line endings, path lookup, platform branches, terminals, sockets) and that it passed, with no skip, on the Mac, Linux and Windows in one full run. `python tests/tier_inventory.py check` refuses a listed pattern that places no file or that matches a security-tier or an excluded file.

A **release-only** file exists only to protect Cairn's own release cut: the signing and re-anchor ceremony, the gate and oracle tools, the quality gate, the release's publication and member checks, and the strict native-evidence check (`release/security_check.py`, which records evidence on the Mac and on Windows and joins the two). It tests the release procedure, not code an adopter runs. `tests/test_tiers.json` lists each one under `hosts.release_only`, in groups that name the hosts that run it at certification (the Mac, and for the strict check's file also Windows) and a reason, so none runs on Linux. `python tests/tier_inventory.py release-only` prints them; `--host mac` or `--host windows` keeps one host's files. When you change Cairn in ordinary development, do not run them: `python tests/tier_inventory.py for PATH...` leaves them out unless a changed path is release machinery (`hosts.release_paths`) or is the test file itself, and `--include-release-only` keeps them. List a file only when its subject is release machinery that neither an adopter nor an ordinary developer runs; a test of shipped code stays unlisted, even for a security tool. Every file in `RELEASE_EXCLUDED_TESTS` (`tests/security_manifest.py`) must be listed, for the Mac only. `check` refuses a pattern that places no file, a file that two groups or `system_independent` also list, an excluded file that is missing or listed for Windows, and a malformed group.

## Re-measure registered counts

*This script is for Cairn's own maintainers. It is not installed in your project, so skip this section unless you work on Cairn itself.*

**What it does.** Checks that numbers cited as current facts in Cairn's own
documentation still match the repository. Each checked number is registered in
`tests/measurements.py` and followed in the Markdown file by an HTML comment
naming its registry key: `<!-- verify: <key> -->` placed immediately after the
number on the same line. The comment holds only a registry key—never a file
path or shell command—so checking a document never runs arbitrary commands.

```bash
python tests/verify_counts.py docs/tool-usage.md
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

> Cairn's `claim_check` watch file is currently 1716 lines `<!-- verify: claim_check_watch_file_lines -->`.

`verify_counts.py` re-measures that file and flags the line above if the line
count changes.

**What to do.** Keep `tests/measurements.py` small (around 10 keys or fewer)
and each measurement fast. Most numbers in prose do not need a registered check:
use approximate wording or a dated snapshot unless a number must stay exact as
the tree changes.

