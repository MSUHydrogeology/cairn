# Cairn's release process

**What this is.** The procedure Cairn follows before and during a version cut.
It is version-independent: the roster, the method, and the cut steps below are
the same every time; only the findings change.

**Where the evidence lives.** Each cut's actual sweep records — who ran what,
what they found, how it was triaged — live with the cut. The v0.2.0 instance
that established this pattern is preserved at
`dev/strategy/archive/2026-05-27-claude-cairn-pre-release-sweep.md` (archived
2026-08-26; this page carries everything version-independent). Read this to
run a release; read that to see how the first one went.

## Why a sweep before every cut

Three structural forces make a whole-tree pass worth running before *any*
release, not just a large one.

* **The improvement loop adds but does not consolidate.** Cairn adds proven
  guidance, but the lifecycle has no regular step to remove or combine it.
  Duplication, outdated guidance, overlapping modules, and unused code can
  therefore accumulate between releases.
* **Many agents, many sessions.** A release batch is landed by several agents.
  Each change is reviewed in isolation, but no per-change review is scoped to
  whole-tree coherence, currency, or cold-start safety.
* **The blast radius is downstream.** Cairn's templates become every adopter's
  governing instructions. An incoherence or dangling reference shipped at a cut
  propagates to every adopter at once.

## The sweep roster

Seven independent review areas. Different owners can run them in parallel and
report to one findings list for the Maintainer to triage before the release.

| # | Sweep | The question it owns |
|---|---|---|
| A | Documentation / doctrine-coherence | Do the docs and doctrine cohere, stay current, and read safely cold? |
| B | Security & supply-chain | Is the agent-instruction supply chain and the shipped executable surface safe? |
| C | Bootstrap & tooling integration | Does the machinery work end to end for a fresh adopter — not just the docs about it? |
| D | Test & verification health | Does the suite actually prove what shipped: coverage, skips, determinism? |
| E | Vendor / project neutrality | Do the shipped templates and doctrine leak any vendor or project name? |
| F | Release-mechanics & provenance | Can the cut itself proceed cleanly: version files, changelog, tag posture? |
| G | Redundancy / consolidation | Is there duplicate or unnecessary functionality anywhere in the tree? |

The lenses overlap slightly by design, but each **owns** a distinct question so
a finding has exactly one home. If the roster is too granular for a given cut,
the natural consolidations are **E into A** and **F into C**; keep them split
only when distinct owners run them.

**Ownership is assigned, not fixed.** The Maintainer assigns; an agent planning
a sweep slots into the matching row or proposes a new lens.

## Method, for every sweep

* **Findings report first.** Survey, then a written prioritized list, then
  Maintainer triage into in-scope-for-cut versus deferred, then fixes. No edits
  before the report unless trivially mechanical.
* **Route fixes by lane.** A typo or one-line fix takes the trivial lane: the
  change and its test, with no code review. A fix whose shape is settled takes the
  standard lane: a short change note, reviewed, then the change and a code
  review. A new feature, a contract change or a high-risk surface takes the
  deliberate lane: proposal, review, and the Maintainer's decision. A
  non-trivial accepted standard or heavy proposal gets plan triage; light is
  the default and has no plan, including for wide or multi-area work. Named
  high-risk surfaces and added or widened trust boundaries trigger heavy.
  Deferred work goes to a durable home with a revival condition — never to an untracked
  note.
* **An empty sweep is a successful sweep.** A sweep that finds nothing records
  an explicit "clean as of `<date>`". Silence is not a result.
* **Verify before recording a finding.** A large fraction of first signals are
  false positives that one more check dissolves; this has held on every sweep
  run so far. Treat the first cheap signal as a *candidate*, confirm it against
  the real file, then record it. This is verify-before-asserting applied to the
  sweep itself, and it is what keeps the report trustworthy rather than noisy.
* **Coordinate on contended files.** Cairn is a live multi-agent tree: claim
  before editing, read the active claim set, commit with explicit paths.

## Checks to run

These are the mechanical gates; a sweep is judgement on top of them, not a
substitute for them.

Use the canonical Python 3.13 environment. The first block keeps the existing
pytest selection and seed, writes a fresh JUnit report and immediately compares
its file outcomes with the independently owned security family. Stop on a nonzero
block result; neither a pytest failure nor a comparison failure may be lost.

```bash
(
report_dir=$(python -c 'import tempfile; print(tempfile.mkdtemp(prefix="cairn-release-"))') || exit 1
report="$report_dir/pytest.xml"
test ! -e "$report" && test ! -L "$report" || exit 1
started_ns=$(python -c 'import time; print(time.time_ns())') || exit 1
pytest_status=0
CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0 --junitxml="$report" || pytest_status=$?
compare_status=0
python scripts/check_release_test_members.py "$report" --started-ns "$started_ns" || compare_status=$?
test "$pytest_status" -eq 0 || exit "$pytest_status"
test "$compare_status" -eq 0 || exit "$compare_status"
)
```

After that block succeeds, run the remaining existing gates:

```bash
python scripts/quality_gate.py --sub neutrality --sub redundancy
python scripts/check_cairn.py
```

The comparison requires every file in
`bootstrap/tests/security_manifest.py`'s `SECURITY_FAMILY` and a successful case
from `bootstrap/tests/test_security_marker.py`. Verify the reviewed family pin
through that file's `test_the_manifest_still_names_exactly_the_reviewed_set`
test as part of the selected run. The comparator rejects missing or stale
reports, malformed or ambiguous identities, missing source files, missing
executed cases, and skipped or failed required cases. Preserve the report for
inspection; its path is in pytest's output. Do not reuse an old report path.

This is file-level presence and reported outcomes only, not every required node,
command provenance or semantic adequacy. It does not authenticate forged XML.
The separate `bootstrap/security_check.py` run and all existing safety, security
and release checks remain required at their own triggers. A goodnight smoke
result does not replace any of them.

Cairn has no configured slow-file roster. An adopter using an independently
owned required-file list can supply it with `--required-files <json-path>` and
`--root <project-root>`; this explicit mode replaces Cairn's required set with
that project's nonempty JSON list of project-relative Python test paths. The
list must come from the project's authoritative configuration, never the
observed report. This creates no Cairn registry or new test run. Cairn's release
block above always uses the default security family, not this adopter mode.

Name the interpreter alongside every suite figure — see
`bootstrap/DEPENDENCY_BUDGET.md` for the canonical one. Security-capability
sweeps are run through their own module runners rather than this list; see
`bootstrap/SAFETY.md` for which surfaces carry which gate.

**Retired files — a person runs this; nothing else fires it.** `upgrade
--remove-retired` removes only files on the list `_RETIRED_INSTALLS` in
`bootstrap/_scaffold/config.py`, so a template deleted without a row there
leaves its file in every project, and nothing warns. Before each cut, run
`git diff --name-status --no-renames --diff-filter=D <previous-tag> <new-tag> -- templates`.
Then run the manifest comparison, which the diff cannot do and which also sees
a template that stays while its mapping drops the destination: extract each
tag with `git archive <tag>`, run `python bootstrap/scaffold.py --manifest` in
each extraction, and list the destinations the old manifest has and the new one
lacks. Add a row for each template an install could have written, with the
SHA-256 of the template at the previous tag, at the new tag and at the commit
before the one that deleted it (`git cat-file blob <rev>:<template>`; stop on a
nonzero git exit, because a revision without the template would hash as the
empty file). A template renamed to a destination still shipped needs no row:
the comparison decides, not the diff. Control: from v0.3.0 to v0.4.0 the diff
lists 20 templates, the collaboration agreement among them, and the comparison
lists the same 20 destinations.

Two techniques that earned their place in past runs:

* **Grep the tree for the outgoing version string first.** It proves the
  version is single-sourced in one command — the highest confidence per
  effort of any release check. Make it the first release-mechanics step.
* **Test upgrades against a real prior version with `git worktree add
  <old-commit>`.** A throwaway worktree gives a genuine older base without
  touching the live checkout, so the upgrade round-trip runs on real trees
  rather than synthetic fixtures.

## The cut

**Maintainer-performed and mechanical.** The sweep does not perform the cut; it
produces the confidence the cut rests on.

* `CITATION.cff` — bump `version` and `date-released`.
* `.zenodo.json` — check that its title, description, creators and keywords
  still match `CITATION.cff`. It carries no version number. Its `license`
  differs on purpose: Zenodo accepts only one license per record, so
  `.zenodo.json` names MIT, while `CITATION.cff` lists both MIT and CC BY 4.0.
  Do not "fix" that difference.
* `CHANGELOG.md` — rename `## Unreleased` to `## <version> — <date>`, and open
  a fresh empty `Unreleased` above it.
* **The GitHub release notes** — copied from that renamed changelog section,
  never drafted in a separate file: a kept draft goes stale (the 0.4.0 draft
  did, and its wrong repository URL and profile names reached the published
  notes). Above the copied section, write a short summary paragraph at release
  time, once the section is final: in plain words, what changed for someone who
  has already installed Cairn, and what they need to do about it. Then check
  the page against the tree: the repository URL, the profile names and every
  command it shows. Record the commit id the security gate checked, with the
  gate output (`bootstrap/PROVENANCE.md`).
* A **signed annotated tag** naming the exact full commit id reported by the
  security gate. That commit must be on the protected branch; then push the
  tag.
* **Publish the GitHub Release separately from pushing the tag.** Create the
  Release, or edit the existing Release for that tag, using the prepared notes.
  Check that the notes match the tree, including the repository URL, profile
  names and commands; open each source-download link. A tag push alone does not
  publish or update a GitHub Release. Then run the read-only check with the
  independently recorded gate commit:

  ```bash
  python scripts/check_release_publication.py \
    --repository OWNER/REPO \
    --tag <tag> \
    --expected-commit <full-gate-commit>
  ```

  Success means GitHub reports a published Release for the tag and the remote
  annotated tag peels to the supplied gate commit. This checks publication
  state and remote tag identity; opening source links checks availability.
  Neither verifies the contents of GitHub's cached source archives.
* **After Zenodo mints the version DOI** for the new release, record it in the
  version-DOI comment at the foot of `CITATION.cff`. The `doi:` field and the
  README badge hold the concept DOI, which covers all versions and does not
  change.

**Gate condition.** Every sweep in the roster is either green or its findings
triaged: in-scope items fixed, deferrals homed. Sweep F is the final pre-flight.

## Adding a sweep type

Propose the lens, the question it owns, and why an existing lens does not cover
it. A new sweep earns its place by owning a question, not by adding coverage
that another lens already provides — the roster is a cost paid at every cut.
