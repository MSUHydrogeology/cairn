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

* **Fold-back only adds.** Cairn's improvement loop appends proven doctrine
  inward; nothing in the lifecycle pushes back toward consolidation. Duplication,
  stale doctrine, overlapping modules, and dead code accumulate *by construction*
  between cuts.
* **Many agents, many sessions.** A release batch is landed by several agents.
  Each change is reviewed in isolation, but no per-change review is scoped to
  whole-tree coherence, currency, or cold-start safety.
* **The blast radius is downstream.** Cairn's templates become every adopter's
  governing instructions. An incoherence or dangling reference shipped at a cut
  propagates to every adopter at once.

## The sweep roster

Seven orthogonal lenses. They are independent and can run in parallel under
different owners; they converge on one findings surface the Maintainer triages
before the cut.

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
  deliberate lane: proposal, review, the Maintainer's decision, plan. Deferred
  work goes to a durable home with a revival condition — never to an untracked
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

```bash
CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0
python scripts/quality_gate.py --sub neutrality --sub redundancy
python scripts/check_cairn.py
```

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
* An **annotated tag**, signed or on a Maintainer-approved release commit on
  the protected branch, then push.
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
