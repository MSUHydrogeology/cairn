# Cairn

**Cairn: An Adaptable Framework for Scientist-AI Research Software Teams**

> A cairn is a trail marker left for those who come after.

Cairn is a **methodology, not software**. It is an Open Science
repository for scientists building scientific-computing software who
are adopting AI agents and care about rigor, reproducibility, and
review discipline.

Cairn has four jobs:

1. **Explain the doctrine** — the invariant core of a human + AI
   development methodology, and *why* each piece exists.
2. **Ship forkable templates** — `AGENTS.md`, the `dev/`
   coordination tree, the proposal / plan / review templates, the
   session routines.
3. **Ship a single-agent bootstrap** — a procedure plus a thin
   script that installs and customizes the apparatus into a target
   repository, adapting it along a set of codebase and team
   dimensions.
4. **Show two worked case studies** — two real scientific-software
   projects as contrasting points in that dimensional space.

The two differentiators Cairn leads with: an **append-only,
git-committed deliberation lifecycle**, and a **Dual-Review model**
(two-tier review across structural independence).

## What the agent sees, and what it must not exfiltrate

Cairn asks an AI coding agent to read your repository in order to do
work. That trust is bounded:

* **What the agent reads to do its job**: the repo and the profile
  YAML you accept. The agent reads code, doctrine, and
  proposal / plan deliberation — the same things a new human
  contributor would read.
* **What must NOT enter Cairn-shipped artifacts** (the `dev/` tree,
  proposals, plans, CHANGELOG entries): secrets, credentials, API
  keys, private paths, embargoed datasets, unpublished results, or
  any other content the maintainer is not prepared to commit to a
  tracked repo. The Codebase Readiness Report's section 10
  ([`templates/codebase-readiness-report.md`](templates/codebase-readiness-report.md))
  is the place to think through the privacy boundary *before* the
  first scaffold.
* **What Cairn-shipped files are scanned for**: vendor-neutrality
  ([`bootstrap/scaffold.py`](bootstrap/scaffold.py) + lint), private
  paths and credentials patterns
  ([`templates/modules/team-gated/content_scan.py`](templates/modules/team-gated/content_scan.py),
  shipped with the `content-security` module), and broken /
  forward-reference links + path claims
  ([`templates/modules/team-gated/link_check.py`](templates/modules/team-gated/link_check.py),
  [`templates/modules/default-on/claim_check.py`](templates/modules/default-on/claim_check.py)).
* **What the agent does *not* do**: it does not exfiltrate the repo
  to a third party, it does not rewrite files outside the working
  tree it has been given access to, and it does not bypass the
  Maintainer-Decision gate. Those constraints come from Cairn's
  doctrine and from the agent's own operating posture — and they
  are reinforced by the scanners above on every release-facing
  commit.

For the full security contract, see
[`SECURITY.md`](SECURITY.md).

## Honest framing

Cairn is **slower for the first few changes**. Its speed comes
later: fewer repeated decisions, fewer forgotten assumptions, fewer
agent collisions, and less rework after unreviewed scientific
choices. Keep the apparatus only as heavy as your codebase and team
earn — the [on-ramp](on-ramp/README.md) is the self-locate aid for
that calibration.

## Who Cairn is for

* A scientist or research-software team building scientific code
  (numerical simulation, data pipelines, calibration / inversion,
  ML for science).
* Adopting one or more AI coding agents (any vendor; Cairn is
  vendor-neutral throughout).
* Wanting recorded, reviewed deliberation rather than ad-hoc
  prompting — and willing to commit the apparatus to git.
* Working at a graduate-research, faculty-research, or small-group
  scale (one human plus agents, up to a small multi-human team).

Cairn is **not** a project-management framework, a CI/CD tool, or a
prompt library. It is upstream of those — the doctrine that decides
what gets prompted, reviewed, and shipped.

## How to adopt

Want to see the apparatus in 15–25 minutes before committing to a
level? Follow [`docs/quickstart.md`](docs/quickstart.md) on a
disposable repo — one human + one AI agent, one trivial change
through the full lifecycle. The on-ramp below is the path *after*
the quickstart, when you have a real project in mind.

New to Cairn? [`docs/getting-started.md`](docs/getting-started.md)
narrates one change moving through the lifecycle, and
[`docs/workflow-role.md`](docs/workflow-role.md) explains where Cairn
sits in the workflow — and what it deliberately does *not* do.

Three graduated levels (see [`on-ramp/README.md`](on-ramp/README.md)
for the full ladder):

* **Level 0 — read the doctrine.** Read [`doctrine/`](doctrine/)
  as a handbook; let it inform how the team already works. No
  apparatus, no `dev/` tree. The lowest-commitment entry.
* **Level 1 — hand-copy the kernel.** Copy
  [`templates/core/`](templates/core/) into the repository, add
  the modules your dimensional profile selects, run the lifecycle
  by hand.
* **Level 2 — full bootstrap.** Run
  [`bootstrap/scaffold.py`](bootstrap/scaffold.py) against a
  profile YAML; the bootstrap procedure
  ([`bootstrap/BOOTSTRAP.md`](bootstrap/BOOTSTRAP.md)) walks an
  agent and the maintainer through assessment, install,
  customization, and a dogfood pass.

The bootstrap is intentionally single-agent: one capable reasoning
agent running alongside the Maintainer, working from
[`bootstrap/BOOTSTRAP.md`](bootstrap/BOOTSTRAP.md).

**Bringing a legacy scientific codebase to Cairn?** Fill
[`templates/codebase-readiness-report.md`](templates/codebase-readiness-report.md)
first. The eleven-section assessment (tests, hidden state, data I/O,
reproducibility, security boundaries, scientific assumptions, and
more) surfaces the load-bearing questions *before* you pick a level,
and the profile-mapping appendix translates your G/M/P scores into a
recommended Cairn level + module roster.

## Repository layout

| Path | What it holds |
|------|---------------|
| [`doctrine/`](doctrine/) | The invariant core: lifecycle, dual-review, coordination, role roster, session routines, rationale. |
| [`dimensions/`](dimensions/) | The six adaptation axes (age, size, complexity, language, human team, agent team) and the three module layers. |
| [`templates/`](templates/) | The forkable files: `core/` (the kernel), `modules/default-on/` and `modules/team-gated/` (the dimension-selected add-ons), and `phase-0/` (the assessment templates). |
| [`bootstrap/`](bootstrap/) | The R-A three-act bootstrap procedure (`BOOTSTRAP.md`), the mechanical scaffold (`scaffold.py` + tests), safety rules (`SAFETY.md`, R-I), and the fidelity-check manifest spec (`fidelity-check.md`, R-H). |
| [`case-studies/`](case-studies/) | Worked examples of the matrix applied: [`modflow_tools.md`](case-studies/modflow_tools.md) (smaller sibling) and [`lhm.md`](case-studies/lhm.md) (full apparatus). |
| [`on-ramp/`](on-ramp/) | The graduated-adoption ladder (Level 0 / 1 / 2). |
| [`docs/`](docs/) | Adopter orientation: Cairn's role in the workflow (`workflow-role.md`), a getting-started walkthrough (`getting-started.md`), and a curated further-reading signpost (`further-reading.md`). |
| [`examples/`](examples/) | Worked examples; [`examples/minimal/`](examples/minimal/) traces one change through the lifecycle at the smallest scale. |

## Status

Cairn is being released at **v0.1.0**.

* **Phases 1–4 complete**: doctrine extraction, forkable templates,
  bootstrap procedure + scaffold + 38 unit tests, and two case
  studies (modflow_tools, LHM) covering opposite-leaning points on
  the dimension matrix.
* **Phase 5 — launch and governance — in progress.**
* **R-H third-party correctness probe (chunk 5.3 of the plan)** is
  outstanding: it awaits a consenting third-party scientific
  repository that did not contribute to the doctrine. The
  bootstrap is validated end-to-end against modflow_tools through
  the v1 reference manifest at
  [`case-studies/modflow_tools-fidelity-manifest.yml`](case-studies/modflow_tools-fidelity-manifest.yml).

The methodology is in active use in two real projects. Cairn is
the generalized doctrine extracted from that practice.

## License

Dual-licensed:

* **Prose and templates** — doctrine, dimensions, case studies,
  bootstrap narrative, README, template documents — are licensed
  under **Creative Commons Attribution 4.0 International (CC BY
  4.0)**. See [`LICENSE-CC-BY.md`](LICENSE-CC-BY.md).
* **Scripts** — `bootstrap/scaffold.py` and its tests — are
  licensed under the **MIT License**. See
  [`LICENSE-MIT.md`](LICENSE-MIT.md).

The boundary is by file kind: anything that is text-for-humans
falls under CC BY; anything that is code-for-machines falls under
MIT. The two licenses are intentionally compatible.

## Citation

If you use Cairn, please cite it. See [`CITATION.cff`](CITATION.cff)
for citation metadata. The first release carries a Zenodo DOI —
once the release is cut, the DOI lands in `CITATION.cff` and a
release-tag note here.

## Origin

Cairn generalizes the apparatus developed for the
[`modflow_tools`](https://gitlab.msu.edu/hydrogeology/code-projects/modflow_tools)
groundwater-modeling project — the reference instance — and is
extended through application to a second project (LHM, MSU
Hydrology). Both case studies are in
[`case-studies/`](case-studies/).

The Cairn repository itself is built using Cairn — its
construction is recorded as a `cairn_methodology_repo` plan in the
modflow_tools repository's own `dev/plans/` lifecycle, with each
phase ending in a required Internal review before the next phase
starts. The plan is the artifact; Cairn is the deliverable.
