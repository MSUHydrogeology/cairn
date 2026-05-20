# Case studies

Worked examples of the Cairn dimension matrix applied to real
projects. Each case study walks through:

1. The project — what it is, what it builds, who it is for.
2. The dimension scores — the six axes, with a reproducible
   reason for each placement.
3. The derived module selection — kernel, default-on, and
   team-gated.
4. The role roster.
5. The customization narrative — how the kernel block slots were
   filled.
6. What might surprise an adopter — the non-obvious decisions and
   the project-local adaptations.

The case studies are **descriptive**, not prescriptive — they
record how a specific project landed at a specific
configuration, with the reasoning the bootstrap procedure
(R-A Act I) requires. Two real projects, sitting at different
points on the matrix, illustrate the range without forcing an
adopter to imagine intermediate cases.

## The matched pair

| File | Profile | Module shape |
|------|---------|--------------|
| [`modflow_tools.md`](modflow_tools.md) | legacy · medium · complex · single · solo · concurrent-multi-type | Kernel + all default-on + two team-gated (`dual-review`, `coordination-tiers`) |
| [`lhm.md`](lhm.md) | legacy · large · complex · multi · solo · concurrent-multi-type | Kernel + all default-on + **all five team-gated** |

The pair shares the team axes (solo human, concurrent-multi-type
agents) and the complexity axis. They diverge on size, language,
and the depth of legacy. The divergences drive the module-set
difference — that's the matrix doing its work.

## Reference manifests

A **fidelity manifest** (R-H) is the machine-readable companion
to a case study: the dimension profile, the installed modules,
the role roster, the slot statuses, the Cairn reference commit
that informed the install. The format spec is in
[`../bootstrap/fidelity-check.md`](../bootstrap/fidelity-check.md).

* [`modflow_tools-fidelity-manifest.yml`](modflow_tools-fidelity-manifest.yml)
  — the descriptive manifest for the modflow_tools case study.

LHM keeps its fidelity manifest in its own repository (the
project's home for living state); only the descriptive
walkthrough lives here.

## Safety

Case studies are governed by R-I rule 3 in
[`../bootstrap/SAFETY.md`](../bootstrap/SAFETY.md): the
Maintainer of the target project must explicitly approve any
content before it is committed to this directory. Both case
studies here have the Maintainer's recorded approval (Anthony
Kendall is the Maintainer of both modflow_tools and LHM); see
the corresponding plan in the modflow_tools repository
(`dev/plans/cairn_methodology_repo.md`) for the approval record.

The case studies contain methodology content only — dimension
profiles, module selection, customization narrative. They do
not contain scientific results, calibration data, source-code
snippets, or any embargoed material. Project-specific
operational detail lives in each project's own `dev/` tree.

## Adding a new case study

A future adopter who wants to contribute a case study should:

1. Open a proposal in the adopter's own repository describing
   the adoption — the dimension profile, the module selection,
   the customization.
2. Run the bootstrap procedure to produce a fidelity manifest
   (`R-H`).
3. Propose the case-study walkthrough to Cairn via a Cairn-side
   proposal, with the Maintainer's explicit approval recorded
   (R-I rule 3).

The bar is the matrix doing distinguishable work — a third case
study earns its place by sitting somewhere meaningfully
different from the two reference cases (a small greenfield
project; a multi-human team; a single-agent adoption; a
massively-multi-domain partition). Replicating an existing
profile shape adds little.
