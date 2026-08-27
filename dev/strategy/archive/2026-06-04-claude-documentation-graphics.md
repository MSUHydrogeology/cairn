<!-- Migrated 2026-06-12 from modflow_tools dev/strategy/ (Cairn's development home before self-hosting). Authored from modflow_tools' vantage; some path cites and "current state" reflect that origin and are being adapted to Cairn. Preserved as Cairn's living deliberation record -- see dev/strategy/MIGRATION.md. -->
<!-- ^ proposed asset paths this strategy would create; they do not resolve
     yet.  Count claims (README length, file counts) cite the command that
     computed them rather than quoting absolutes. -->

<!-- Archived 2026-08-10: superseded by the Cairn-vantage re-scope
     `2026-08-10-claude-documentation-enhancement.md`, which carries this note's
     production model forward (Mermaid-first, existence + legibility as two
     checks, the caption states the conclusion, asset naming/provenance) and
     drops the modflow_tools figure inventory. Read for history; not current
     direction. -->

# Documentation graphics strategy

**Author**: Claude (Strategy & Research Agent)
**Model**: Opus 4.8 (1M context)
**Date**: 2026-06-04
**Status**: settled
**Type**: design-exploration
**Surfaces this would feed**: a follow-on README rewrite; per-doc figure
additions across `docs/`; a small reproducible figure-generation harness;
possibly a `docs/images/` (+ `docs/figures/`) asset convention.

---

## The felt gap

modflow_tools' documentation is **almost entirely text**. A survey found
**no embedded images across the `docs/` markdown** (per
`grep -rl '!\[' docs`), and the only raster assets in the repo are example
*outputs* under `examples/` -- calibration and particle-tracking PNGs that
are never linked from the docs. The root `README.md` (260 lines, per
`wc -l`) is clear but visually plain: no badges, no hero, no picture of
what the tool actually produces.

Two costs follow. First, **comprehension**: the hardest concepts in the
docs are exactly the ones prose serves worst -- the DIS/DISV/DISU grid
choice, the four-way YAML/workflow/notebook/CLI contract, the
multiplicative calibration parameter stack. A reader re-derives from
paragraphs what one diagram would settle. Second, **enticement**: a
prospective user -- a graduate-student hydrogeologist weighing this against
raw FloPy -- lands on a wall of text and scrolls past without seeing what
the tool *lets them do* or *produces*.

This doc is a **prioritized inventory of where graphics are needed**, a
**production model** tuned to this repo, and a **featured plan for the
README** (which the maintainer flagged as the priority; the actual rewrite
is the named follow-on, not done here).

## Current state (grounded)

* **No docs build system** (no `mkdocs.yml`, no Sphinx `conf.py` --
  verified). Docs are plain markdown rendered natively by the host
  (GitLab `gitlab.msu.edu` + GitHub). Two consequences: **Mermaid code
  fences render with zero build**, and static images embed via plain
  markdown image syntax (`![alt]`-style). No `.. plot::` /
  notebook-execution pipeline exists.
* **Existing visual assets**: a handful of PNGs, all under `examples/`
  (e.g. `examples/freyberg_pilot_points/pilot_point_field.png`,
  `.../phi_vs_iteration.png`, `.../obs_vs_sim.png`,
  `examples/freyberg_particle_tracking/expected_outputs/pathlines.png`,
  `examples/freyberg_prior_mc/forecast_distributions.png`). **None are
  embedded in `docs/`.** There is no `docs/images/` directory.
* **Figure-generation infrastructure already exists**:
  `modflow_tools/postprocess/plotting/` (`heads`, `cross_sections`,
  `budgets`, `time_series`, `observations`, `geometry`) plus `ui/plotting`
  and the runnable `examples/`. So scientific figures are **script-
  generable and reproducible**, not one-off.
* **README**: well-structured (tagline, what-it-does, quickstart, install,
  structure tree, examples table, docs links) but no badges, no hero
  visual, no example output. Enticement is low for a first-contact reader.

## Production model -- what fits a no-build, host-rendered repo

Three graphic classes, each with a production method matched to the repo's
reality (no build step, GitLab/GitHub markdown rendering, a reproducibility
ethos the project already lives by in its verifiability framework):

1. **Diagrams** (flowcharts, schematics, decision trees, architecture) ->
   **Mermaid code fences**. Diffable, version-controlled, zero-build, no
   binary bloat, render natively on GitLab/GitHub. **The default** for
   conceptual graphics. Where Mermaid can't express a spatial schematic
   (e.g. true grid-cell topology), fall back to a small committed SVG or a
   matplotlib-drawn schematic.
2. **Scientific outputs** (head maps, cross-sections, hydrographs, budgets,
   calibration plots) -> **script-generated PNG/SVG** from the existing
   plotting module. Produce them via a **committed generator**
   (`docs/figures/generate_docs_figures.py`, or per-figure example runs)
   over a tiny fixture model, with one shared matplotlib style -- so a
   restyle is a re-run, not a manual redraw, and every figure has
   provenance. This mirrors the project's own verifiability discipline:
   figures are *artifacts with a recipe*, not opaque binaries.
3. **Interactive-UI views** (the `CellPicker` painter, the convergence
   diagnostics app, notebook widgets) -> **annotated screenshots**. The one
   class that can't be scripted; highest differentiator value, lowest
   reproducibility. Keep them few, captioned, and refreshed at release
   cadence (note the staleness risk explicitly).

**Asset home**: propose `docs/images/` for screenshots + `docs/figures/`
for script-generated output (or a single `docs/images/`); decide one
convention (open question 1).

## The prioritized inventory

Priority = comprehension-leverage x audience-reach. Production = Mermaid
(pure authoring, lands immediately) / generated PNG (needs the figure
harness) / screenshot (manual capture) / **embed-existing** (near-zero
cost -- the asset already exists).

### P0 -- the near-zero-cost win (do first)

Embed the **already-existing** example PNGs into the docs that describe
them, with captions. **Use stable identity, not bare filenames**:
`phi_vs_iteration.png` exists in *three* example directories
(`freyberg_calibration`, `freyberg_pilot_points`,
`freyberg_mf2005_calibration`), so a bare name can silently point at the
wrong output. Either embed the **full relative path**, or **copy** the
chosen asset into `docs/figures/` with a descriptive kebab-case name (e.g.
`calibration-glm-phi-vs-iteration.png`) plus a manifest entry tracing it
back to the example that produced it.

| Source asset (full path) | Embed into | Caption conveys |
|---|---|---|
| `examples/freyberg_pilot_points/pilot_point_field.png` | `docs/user_guide/calibration.md` | the pilot-point HK field |
| `examples/freyberg_pilot_points/phi_vs_iteration.png` | `docs/user_guide/calibration.md` | GLM objective convergence |
| `examples/freyberg_pilot_points/obs_vs_sim.png` | `docs/user_guide/calibration.md` / `results.md` | observed-vs-simulated fit |
| `examples/freyberg_prior_mc/forecast_distributions.png` | `docs/user_guide/calibration.md` | prior-MC forecast uncertainty |
| `examples/freyberg_particle_tracking/expected_outputs/pathlines.png` | `docs/user_guide/particle_tracking.md` | forward PRT endpoints |

No new figures -- pure authoring. Highest ROI per minute.

### P1 -- highest-leverage new graphics (newcomer + most-asked concepts)

| Content | Doc(s) | Graphic | Production |
|---|---|---|---|
| **README hero**: 4-activity quadrant (Prepare / Build / Review / Calibrate) + one example head map | `README.md` | quadrant diagram + 1 output PNG | Mermaid + generated PNG |
| **Grid types**: DIS vs DISV vs DISU cell topology, + a "which grid?" decision tree | `docs/theory/modflow_concepts.md`, `docs/user_guide/mesh.md` | side-by-side schematic + decision tree | Mermaid (tree) + SVG/matplotlib (topology) |
| **The four-way contract** (YAML / workflow-fn / notebook / CLI -- who owns what) + the YAML -> Model -> FloPy -> MODFLOW data flow | `docs/user_guide/workflow.md`, `configuration.md`, `model.md` | flowchart + data-flow | Mermaid |

### P2 -- high value, conceptual or sample-output

| Content | Doc(s) | Graphic | Production |
|---|---|---|---|
| **Calibration parameter stacking** (`effective = base x scalar x zone x pilot-points`) as layer compositing | `docs/user_guide/calibration.md` | composited-layers schematic | Mermaid or matplotlib |
| **PEST++ GLM loop** (forward run -> residuals -> Jacobian -> GLM step -> phi convergence) | `docs/user_guide/calibration.md`, `docs/theory/calibration_theory.md` | flowchart | Mermaid |
| **Plotting gallery** (head contour map, X-Z cross-section, hydrograph, water-budget bar) | `docs/user_guide/plotting.md`, `results.md` | 4-figure sample gallery | generated PNG |
| **Mesh refinement** (coarse base -> refined near wells/rivers) | `docs/user_guide/mesh.md` | before/after | generated PNG |

### P3 -- differentiators + completeness

| Content | Doc(s) | Graphic | Production |
|---|---|---|---|
| `CellPicker` interactive painter | `docs/user_guide/notebook_ui.md` | annotated widget screenshot | screenshot |
| Convergence diagnostics (troublesome-cell map + cross-section) | `docs/user_guide/convergence.md` | screenshot + map | screenshot + generated PNG |
| Module / architecture layout (activity-aligned tree) | `docs/developer/architecture.md` | architecture diagram | Mermaid |
| LHM bootstrap + helper roster (`sys.path` injection -> helpers) | `docs/developer/lhm_integration.md` | import-flow diagram | Mermaid |

## The README enticement plan (featured)

The maintainer flagged the README as the priority. Today it reads clear
but dry (no badges, no hero, no output picture). The goal: in ~10 seconds
of scroll a first-contact hydrogeologist sees **(a) what it does, (b) what
it produces (a picture), (c) how to start.** Proposed shape -- this is the
*plan*; the rewrite is the follow-on (open question 5):

1. **Badges row** -- honest subset for a pre-release project: license,
   Python version, test status (if a public CI exists). **Defer**
   PyPI / conda-forge / Zenodo-DOI badges until release -- do not fake
   maintained-ness.
2. **Tagline + one-sentence value prop** -- lead with the *differentiator*:
   YAML-driven build + review + calibrate, grid-agnostic (DIS/DISV/DISU),
   MODFLOW 6 / 2005 / NWT, interactive cell painting, PEST++ / pyEMU wired
   -- i.e. what it does *better/faster than raw FloPy*.
3. **Hero visual -- lead with a real model artifact.** A genuine workflow
   output -- a Freyberg head map, a pathline plot, a calibration-convergence
   trace, a pilot-point field -- captioned with the *question it answers* is
   the strongest hook. The 4-activity quadrant (Mermaid) rides alongside as
   orientation, not in place of the artifact; the README is not a brochure
   of abstract diagrams.
4. **"What you get" mini-gallery** -- 3-4 thumbnail outputs (head map,
   hydrograph, pilot-point field, pathlines) so the reader *sees* the
   product immediately. **Rule**: every top-of-README visual either *is* an
   actual model artifact or links immediately to the runnable example that
   generated it.
5. **Quickstart-at-a-glance** -- keep the code/CLI snippet, but front it
   with "from a YAML config to a running model in a few lines," and
   **soften the install** (the LHM bootstrap currently reads intimidating
   -- a one-block copy-paste, details below).
6. **Feature highlights** -- a scannable differentiators list (interactive
   painter, zone budget, LGR, PRT/MODPATH, FOSM / data-worth / ensembles),
   ideally with small icons.
7. Existing structure (examples table, notebook templates, docs links)
   stays **below the fold**.

## Production & maintenance discipline

* **Mermaid-first, not Mermaid-only.** Mermaid is the default for
  flowcharts and decision trees -- diffable, no binary bloat, no build. But
  spatial topology and hydrogeologic geometry often need real geometry,
  scale, and visual hierarchy, so keep a clean escape hatch to a committed
  SVG or matplotlib schematic whenever Mermaid would oversimplify the
  science.
* **Mermaid: no hardcoded styles.** GitLab MSU and GitHub render a dark
  theme; a diagram with a hardcoded `fill` / colour (e.g.
  `style A fill:#fff`) goes unreadable on a theme switch. Rely on the
  default host theme.
* **Generated figures are reproducible and declared.** A committed
  `docs/figures/generate_docs_figures.py` regenerates every script-made PNG
  from a tiny fixture under one shared matplotlib style (a figure is an
  *artifact with a recipe*). Pair it with a small **provenance manifest**
  declaring, per figure: source fixture / model, the command, the output
  path, environment assumptions, and whether the committed image is
  byte-stable or only *semantically* stable. A **contract test**
  (`test_docs_figures_generation_runs`, synthetic fixture) runs the
  generator and checks that every generated figure in `docs/` is declared in
  the manifest -- catching a `postprocess/plotting/` change that breaks or
  orphans a figure. Avoid pixel-exact assertions unless the plotting stack
  is pinned tightly enough to make them meaningful.
* **Two checks, not one: bytes *and* legibility.** *(a) Existence* --
  `scripts/verify_doc_links.py` today *tolerates* any missing target whose
  suffix is not `.md` (it `continue`s -- lines 143-146), so a broken image
  reference or a deleted figure rots **undetected**; extend it to confirm
  referenced image assets (`.png` / `.svg` / `.jpg` / `.jpeg` / `.gif`)
  physically exist, landed **with the P0 embed**. *(b) Legibility* --
  existence proves only that the bytes are there; it will not catch a
  Mermaid diagram unreadable in dark mode, a clipped or oversized PNG, a
  missing legend, or text illegible on mobile. Add a **visual-QA pass**:
  preview the README and one representative docs page in the target
  renderer(s) and record that each diagram / image is readable, scaled,
  captioned, and not layout-breaking. A documented manual item now; a render
  gate if a docs build is ever added.
* **Captions carry the science.** Every embedded figure has a caption +
  alt-text -- and for a hydrogeology figure that means units, a legend, a
  colourblind-safe palette, readable contour labels where applicable, and
  enough interpretation that a screen-reader user or an images-off skimmer
  still gets the point. The rule is **"the caption states the conclusion to
  draw,"** not merely "a caption exists" -- a decoratively-captioned figure
  is still a review finding.
* **Asset naming, size, and lifecycle.** Kebab-case descriptive names (no
  generic `plot.png`); a preferred max display width; a compression pass
  (`optipng`, or WebP for photographic screenshots) against a
  **~150 KB / image target** -- a pressure, not a hard cap, with an
  exception for figures whose scientific content genuinely needs more
  resolution; a source / provenance entry per asset; and a
  screenshot-refresh trigger (release cadence). Prefer SVG / Mermaid where
  the concept allows; raster only for true scientific output; keep UI
  screenshots minimal (they can't auto-regenerate).

## Sequencing

1. **P0** -- embed the existing example PNGs (pure authoring; immediate),
   landed **with the `verify_doc_links.py` image-existence check** so the
   embeds are guarded from the first one.
2. **P1 Mermaid pieces** (grid decision tree, four-way contract, data
   flow) -- pure authoring, land immediately; **README rewrite** on
   go-ahead; the grid-topology schematic + README head map need the figure
   harness.
3. **Figure harness** (`docs/figures/`) -- a small bounded code task that
   unblocks all generated-PNG items (P1 head map, P2 gallery + mesh).
4. **P2** diagrams (Mermaid) + gallery/mesh (generated).
5. **P3** -- UI screenshots (manual pass) + architecture/LHM diagrams
   (Mermaid).

Mermaid items are pure-authoring and need no code; generated figures need
the harness (one bounded task); screenshots need a manual capture pass.

**Promote to a proposal, with three gates before the first image lands.**
The README / P0 embed is the first implementation slice; gate it on three
prerequisites so the effort becomes a durable visual-documentation system
rather than "add pictures": (1) the `verify_doc_links.py` image-existence
check; (2) the visual-QA pass (readable / scaled / captioned / not
layout-breaking, dark-mode + mobile); (3) the provenance + naming convention
(the figure manifest, kebab-case names, the `docs/figures/` vs `docs/images/`
split). The P0 embed lands only once gates (1) and (2) hold.

## Open questions for the maintainer

Each remains the maintainer's call; the recommended answer is noted.

1. **Asset convention** -- **recommended (concur): split** `docs/figures/`
   (programmatically generated) from `docs/images/` (manually-captured
   screenshots), keeping reproducible assets distinct from static ones.
2. **Mermaid vs. static SVG** -- **recommended (concur): Mermaid-first**;
   committed SVG only as the fallback for spatial topology Mermaid cannot
   express. (GitLab MSU renders Mermaid natively.)
3. **Figure reproducibility** -- **recommended (concur): build the harness
   from day one**; hand-placed plots without recipes go stale.
4. **README badges** -- **recommended (concur):** license + Python +
   test-status (if a public CI is active) pre-release; defer PyPI / conda /
   DOI to release.
5. **README rewrite go-ahead** -- the review **fully supports** it (lead
   with the 4-activity quadrant + the mini-gallery); still awaiting the
   maintainer's go-ahead to execute the rewrite as the follow-on.

## Cairn fold-up note

This connects to the Cairn `0.4` candidate **"Graphics in user
documentation + QuickStart guides"** (`dev/PLANNING.md` > Cairn track). A
visual-documentation discipline -- Mermaid-first, a reproducible
figure-generation harness, caption/alt-text as a review finding -- is
methodology-portable, so it is a **fold-up candidate** for a Cairn
docs / examples-gallery module. Note also that `docs/` is **Cairn-untracked**
(per the in-flight cairn-adoption plan's re-baseline -- "project bulk lives
in `docs/` ... all Cairn-untracked"), so this graphics work is independent
of the Cairn adoption and never touches the lockfile.
