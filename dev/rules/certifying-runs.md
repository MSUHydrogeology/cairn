# Certifying runs

Cairn's rule for the full-suite certifying run. Routed from `RULES.md`. The text below moved from `AGENTS.md` on 2026-11-10 unchanged.

Do not run a full-tree certifying suite for ordinary implementation. The
authorized certifying run is the pair on a clean committed tree under Python
3.13.x: `CAIRN_FULL_SUITE=1 python -m pytest tests
--quality-gate-shuffle-seed=0`, then `python tests/quality_gate.py --sub
neutrality --sub redundancy`. It is run only before a push when required,
before re-anchor, before a release cut, or when the Maintainer asks. It
certifies every change at or before that commit for bisect. The reviewer never
runs the full suite. Never set
`CAIRN_FULL_SUITE=1` for another reason.

**A release is certified on three platforms.** The Mac runs the whole suite
once, as above. Linux and Windows run only the shipped files that can depend
on the system: the files `python tests/tier_inventory.py cert-files` prints,
with `@PATH` (the file `cert-files --write PATH` saved) in place of `tests` in
the command above. Cairn-only tests, the release-only files
(`python tests/tier_inventory.py release-only`) and the files
`tests/test_tiers.json` lists as system-independent run on the Mac only; the
strict native-evidence check's file also runs on Windows, whose list is
`cert-files --host windows`. At an ordinary development change do not run a
release-only file unless the change touches its subject;
`python tests/tier_inventory.py for` leaves it out. Each run is at the
release commit, on a clean tree, under Python 3.13; on Linux and Windows an
earlier run stands for the files whose inputs have not changed (last paragraph).
The release note gives the
three results: for each, the platform, the full commit id from
`git rev-parse HEAD`, the Python version, the counts of passed,
failed and skipped, and every test skipped on that platform with its reason; for
Linux and Windows also the `cert-files` command and its file count. A
platform whose run did not pass is not certified. Only the Maintainer can cut
a release without it, in words quoted in the release note that name the
platform and the run that failed or is missing, with a home and revival
condition for the repair. A test that cannot
pass on a platform is marked to skip there, with its reason written in the
test. A skip of a test that `dev/rules/protected-surfaces.md` lets be cut only
through a Security Review takes that review first, on every platform. On the
Mac, where the membership check runs, a skip in a security-family file also
needs its exact ID in `NATIVE_ONLY_NODE_IDS`, or the check refuses it.

**An earlier run counts when nothing it read has changed.** Running a test
again on the same inputs shows nothing new. A Linux or Windows run at an earlier
commit E stands for the release commit R, one test file at a time, for each file
that passed there (a recorded skip counts as the same skip at R) and whose inputs
are the same at R: the test file, every file
under `tests/` it imports, `tests/conftest.py`, and every file it names
(`python tests/tier_inventory.py for --include-release-only` over `git diff --name-only --diff-filter=d E R`
lists the tests that name them) or sweeps. A file that failed at E, or whose
inputs you cannot show unchanged, is run at R; a failed node fixed since is run
alone, and its commit is named. Keep every run, finished or not, under
`dev/measurement/certification-evidence/`: the junit report, per-file counts,
the full commit id, the platform and the Python version. The release note names,
for each platform, the commit E, the number of files that stand on it, and each
file rerun with the changed path that put it there. The Mac still runs the whole
suite at R; it is the canonical host and the check on this paragraph.
