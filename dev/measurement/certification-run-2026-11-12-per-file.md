# Per-file results of the 0.7 certification run

Measured 2026-11-12; this table was derived on 2026-11-16. It is a dated
snapshot, not a live figure.

**Table:** [certification-run-2026-11-12-per-file.csv](certification-run-2026-11-12-per-file.csv),
one row for each of the 130 test files: cases, failed, errors, skipped and the
sum of case times in seconds.

**Source.** The JUnit report of the single certification run at commit
`072d82d2` (Python 3.13.13, macOS): 5,413 cases, of which 5,344 passed, 6
failed and 63 were skipped, in 49 minutes 6 seconds. The table shows the run
as it happened. The failures were followed by focused corrections, recorded
at `91e17bf1`; this note does not re-examine them.

**Why the raw report is not committed.** It carries the host name and local
paths. When this was written it sat in a temporary folder on the Maintainer's
machine, so it may no longer exist.

**Method.** Each case's class name was mapped to the longest matching `.py`
path tracked at that commit; none was left unmatched. Case times were summed
per file.

**Limit.** A case-time sum is not a file's wall time: it leaves out
collection and shared setup. The sums total 2,938 seconds against 2,947 for
the run.

**Readers.** The draft proposal on release tests
(`dev/proposals/2026-11-16-claude-release-tests-shipped-only.md`) takes its
Cairn-side share from this table. [Slowest test files](slowest-test-owners-2026-11-13.md)
lists the 51 files above ten seconds from the same run, and
[suite-cost.md](suite-cost.md) gives the longer account.
