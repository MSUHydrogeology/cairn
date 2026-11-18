# Cairn test maintenance

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

