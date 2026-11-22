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
the command above. Cairn-only tests and the files `tests/test_tiers.json` lists
as system-independent run on the Mac only. Each run is at the
release commit, on a clean tree, under Python 3.13. The release note gives the
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
