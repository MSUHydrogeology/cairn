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

* **Findings report first.** Survey and write a prioritized list. Then fix
  genuinely easy items already authorized, with their applicable checks. Bring
  material scope, tradeoff and release-readiness choices to the Maintainer for
  triage; ordinary authorized fixes need no extra decision.
* **Route work by its existing authority.** Eligible trivial repairs take the
  direct path with any needed test and no code review. Other substantive work
  starts with a proposal and a Maintainer Decision sets its tier. Light keeps
  implementation and final verification on the accepted proposal, including
  multi-chunk work. Standard and heavy retain plan triage and their required
  reviews, checks and fences; heavy adds Security Review. Named high-risk
  surfaces and added or widened trust boundaries trigger heavy.
  Deferred work goes to a durable home with a revival condition — never to an untracked
  note.
* **Close out lifecycle records before the cut.** Review the latest committed
  state of active and archived plans and any change-note records for accepted
  scope, required checks, unresolved findings, follow-ups and deferred work.
  Use the changes since the previous release to identify plans implemented
  wholly or partly in this version, including plans already archived; do not
  rely only on the active-plan list. For each follow-up, locate its recorded
  disposition: acted on with evidence, declined with a reason by the authorized
  decision-maker, filed as a linked issue, or retained as a named item on
  `dev/PLANNING.md`. Confirm that issue and board homes actually exist and
  carry enough context to resume the work. Filing an issue or board item does
  not itself authorize deferral of accepted scope or close a required check.
  Record the plans examined and unresolved items with the cut's existing sweep
  evidence; add no separate follow-up ledger. For an advisory, plan-by-plan
  benefit-versus-cost summary, the existing closeout owner can run
  `python tools/audit_report.py`; it reads archive records, is read-only, and
  is not a release gate.
  Treat old pending language as historical when later records supersede it.
  Fix genuinely easy, already-authorized items with applicable checks; bring
  meaningful remaining choices to the Maintainer in one batch. Defer only with
  the Maintainer's explicit disposition, a named live home and a revival
  condition. An unmet required check or criterion stays open.
* **Retire addressed strategies and reconcile the release board.** Compare
  each relevant strategy's commitments with delivered work and the follow-up
  dispositions above. Archive a strategy only when all its outcomes are
  addressed, preserving its record and repairing links; age or an associated
  plan's archive is not sufficient. Keep a strategy live if it still owns
  unresolved work. Reconcile this version's `dev/PLANNING.md` rows under the
  board's existing completion and removal rules. Move unfinished items to the
  next release with their remaining scope, source records, owner or next
  action, prerequisites and revival condition intact. Name the carryovers
  and the Maintainer's scheduling authorization in the existing release sweep
  evidence. Rescheduling is not completion or permission to release with an
  unmet requirement; retain applicable fences and obtain any required scope
  or release-readiness disposition rather than silently dropping work.
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

## Strict release-security evidence

At the final release candidate, run the strict check on native Mac and Windows
under Python 3.13. Give each run a new absolute record path outside its
checkout:

```bash
python bootstrap/security_check.py --record /absolute/path/mac.json
python bootstrap/security_check.py --record /absolute/path/windows.json
```

Each local run preserves both full-suite orders: the direct default order and
the quality gate's seed-0 order, along with neutrality, redundancy, Bandit and
the Cairn document check. It writes exact collected IDs and phase outcomes to
temporary files outside the byte-verified checkout, validates them, and emits
a local record. A successful local run says `INCOMPLETE` and exits 5. A child
pytest exit 5 means it collected no tests and is a failure.

The Maintainer joins the two records from a clean checkout at the same final
commit:

```bash
python bootstrap/security_check.py --join /absolute/path/mac.json /absolute/path/windows.json
```

Only the join can print `PASS`. It checks the fixed source-reviewed native-ID
policy, both order labels, complete per-node outcomes, every phase, platform,
Python 3.13 and the current full `HEAD`. Attach both local records and the
joined output to the existing release notes. The local records are not
authenticated; their suppliers remain a human-reviewed part of the ceremony.

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
