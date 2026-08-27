<!-- cairn-internal-ref-allow: doctrine/ reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- ^ Illustrative output paths of the readiness assessment, created on first use; the cite travels with this template to adopters. -->

# Codebase Readiness Report

> **Use this template before picking a Cairn level.**  Fill it for
> your existing scientific codebase -- with your AI agent's help if
> you have one -- and the answers will tell you (a) whether you are
> ready for Level 1, Level 2, or Level 0 (read the doctrine first
> while you fix specific gaps), and (b) which Cairn modules your
> dimensional profile most plausibly warrants.
>
> A filled report is also a **gift to your future self**: even if
> you never adopt Cairn, the act of filling it surfaces the
> assumptions a scientific codebase silently carries.

**Codebase**: `<name>`
**Maintainer filling this**: `<name>`
**Date filled**: `<YYYY-MM-DD>`
**Status**: `draft` / `completed-baseline` / `archived-baseline` — this
is a point-in-time diagnostic snapshot, **not** a live roadmap plan.
Mark it `archived-baseline` once filled, so a reader never mistakes it
for active, tracked work.
**Time investment**: 30-90 minutes, depending on codebase size.

---

## How to use this report

1. Read each section's prompt.  Write 1-5 sentences of plain prose.
   **Fill it locally first**, not in a tracked file -- see "What to
   check in" below.
2. Compare your prose against the "**Good**" / "**Poor**" markers
   under each section.  Score yourself honestly -- nobody else
   reads this unless you share it.
3. At the end, the "Profile mapping" appendix translates your scores
   into a recommended Cairn level and module roster.

The eleven sections below cover the surfaces a scientific codebase
needs the AI agent (and its human maintainer) to understand
before either can safely operate on it.

## What to check in

The filled report **may contain sensitive content** -- section 10
(security boundaries) and section 11 (scientific assumptions) in
particular will ask you about private paths, embargoed datasets,
credentials history, and proprietary assumptions.  Be deliberate
about what reaches the tracked tree.

The default is **safer**: fill the full report locally, then commit
**only one of** these two artifacts to your `dev/` tree:

* **A redacted summary** -- the eleven sections' prose with
  sensitive specifics replaced by placeholders (e.g., "credentials
  for an external service are read from `<private path>`" rather
  than the literal path); commit this as
  `dev/readiness-report-summary.md`.
* **A readiness-report decision** -- a one-page artifact that
  records the G/M/P self-score table, the chosen Cairn level, and
  a follow-up action list, **without** the eleven sections'
  narrative; commit this as `dev/readiness-report-decision.md`.

The full filled report stays local (outside the tree, or in
`.gitignore`'d scratch).  Both artifacts above support the
"durable record of where the codebase stood" purpose without
exporting secrets into the tracked tree -- where they could be
read by any agent on any future session.

**Full report check-in is an explicit opt-in.**  If you decide
the full report is safe to track (small teams, no embargoed
content, no credentials history), commit
`dev/readiness-report.md` only after the Maintainer affirms
*in the commit body* that the artifact contains no secrets,
private paths, or proprietary detail.  The act of affirming is
the gate.

---

## 1. Tests

**Prompt**: What tests does the codebase have?  How are they run?
Do they pass on a fresh checkout?  What is *not* covered by tests
today?

* **Good**: A `pytest` (or equivalent) command exists, runs to
  completion in under 10 minutes, covers the core science (not just
  the I/O), and the maintainer trusts it to catch regressions.
* **Poor**: No tests, or tests that only run on the maintainer's
  laptop, or tests that have been disabled / skipped without record.

*Your answer:*

`<...>`

---

## 2. Hidden state

**Prompt**: What state lives outside the tracked tree?  Caches,
generated intermediate files, conda envs, environment variables,
`.env` files, manually edited config that nobody remembers
editing?  What breaks if someone clones the repo fresh and tries
to run it?

* **Good**: A fresh clone runs after a single documented setup
  step (`conda env create -f environment.yml`, `pip install -e .`,
  etc.); all generated artifacts are reproducible from the tree
  + a documented data source.
* **Poor**: The repo works only on machines where someone "set
  it up" manually; key files live outside the tree; the
  maintainer cannot list what state is hidden.

*Your answer:*

`<...>`

---

## 3. Scripts

**Prompt**: How many ad-hoc scripts does the repo carry?  Are they
named, documented, and dated?  Or is there a `scratch/` directory
nobody dares delete?

* **Good**: Scripts are organized (a `scripts/` directory with
  README, or a CLI module with subcommands); the maintainer can
  say what each one does without reading it.
* **Poor**: Scripts proliferate, name collisions exist (`run.py`,
  `run_v2.py`, `run_v2_actually.py`), and the maintainer fears
  deleting any of them.

*Your answer:*

`<...>`

---

## 4. Notebooks

**Prompt**: How many Jupyter / Quarto / R Markdown notebooks does
the repo carry?  Are they executed top-to-bottom on a regular
cadence, or are some carrying stale outputs from months ago?  Do
notebooks duplicate code that should be in the library?

* **Good**: Notebooks are narrative + small driver code; the heavy
  lifting lives in the library; notebooks are re-runnable in CI or
  on demand and the maintainer knows which ones are current.
* **Poor**: Notebooks contain the only copy of important logic;
  outputs are stale; multiple notebooks compute almost-the-same
  thing with different conventions.

*Your answer:*

`<...>`

---

## 5. Data I/O

**Prompt**: Where does input data come from?  Where do outputs go?
Is the I/O code separated from the science, or interleaved?  Are
input file formats documented?  Are external raw data sources (e.g.,
USGS databases, GIS layers) cited with download URLs or provenance?
Are output file formats stable enough that downstream consumers can
rely on them?

External-repo paths: `docs/io.md`
* **Good**: I/O is concentrated in named modules; input / output
  formats are documented (a schema doc, a docs/io.md file or
  equivalent, or docstrings on the loaders); downstream consumers
  know what to expect.
* **Poor**: I/O is scattered through analysis code; formats are
  inferred by reading the loader; changing a column name silently
  breaks downstream code.

*Your answer:*

`<...>`

---

## 6. Generated outputs

**Prompt**: What artifacts does the codebase produce -- figures,
tables, model outputs, parameter files?  Are they tracked, ignored,
or in a separate output directory?  Can the maintainer regenerate
all of them from the tree + the documented data source?

* **Good**: Outputs are in a clearly-named directory
  (`outputs/`, `results/`, `figures/`); they are `.gitignore`d
  unless small and lasting; a single command regenerates them.
* **Poor**: Outputs are mixed with source; some outputs are
  tracked because nobody knows how to regenerate them; the
  maintainer cannot confidently rebuild the canonical figure set.

*Your answer:*

`<...>`

---

## 7. Public APIs

**Prompt**: What does the codebase expose to its users (other
labs, downstream packages, your own future self)?  Is the public
surface documented?  Are there stability promises -- explicit or
implicit?

* **Good**: A `__init__.py` (or equivalent) names the public
  surface; docs describe the entry points; the maintainer can
  say which functions / classes are "stable" vs "internal".
* **Poor**: Anything importable is treated as public; users
  depend on internal helpers; refactors break downstream users
  without warning.

*Your answer:*

`<...>`

---

## 8. Build / run commands

**Prompt**: What command(s) does someone type to use this
codebase?  Are they discoverable from the repo root?  Are
prerequisites documented?

* **Good**: The README's first content section is "How to run
  it"; one command (or a short sequence) takes a fresh
  checkout to a working result; prerequisites are listed.
* **Poor**: No clear entry point; the maintainer says "ask me
  in person"; prerequisites are folklore.

*Your answer:*

`<...>`

---

## 9. Reproducibility

**Prompt**: If a colleague clones the repo today and tries to
reproduce a result from a paper / report / dashboard, what
breaks?  How far from "reproducible by default" is the codebase?

* **Good**: A specific commit hash + the documented run command
  + the documented data source = the canonical result.  Random
  seeds are pinned; nondeterministic steps are flagged.
* **Poor**: Results drift between runs; data versions are
  ambiguous; the canonical result was produced on a machine
  that no longer exists.

*Your answer:*

`<...>`

---

## 10. Security boundaries

**Prompt**: What sensitive data lives near (or in) this codebase?
Credentials, API keys, unpublished datasets, identifying
information, embargoed results?  Where is the boundary between
"safe for AI agents to read" and "not safe"?

This question matters in Cairn because AI agents will read parts
of your repo to do work.  Be honest about the privacy boundary
before you scaffold.

* **Good**: Secrets live outside the tree (env vars, `.env`
  files in `.gitignore`, secret managers); a documented file list
  names what AI agents may and may not read; sensitive datasets
  have a separate access channel.
* **Poor**: Secrets are checked in; the maintainer is unsure
  what is sensitive; "everything is OK to share" is asserted
  without an audit.

*Your answer:*

`<...>`

---

## 11. Scientific assumptions

**Prompt**: What scientific assumptions does the codebase carry
that a maintainer might miss?  Sign conventions, unit conventions,
default parameter values, calibration weights/parameters (e.g., parameter
bounds, covariance matrices, regularization setup), simplifications,
known-unknown caveats.  If a new contributor changed a default,
would the science silently degrade?

This is the question Cairn is most differentiated on.  Most
software-engineering frameworks do not ask it.

External-repo paths: `docs/assumptions.md`
* **Good**: A `docs/assumptions.md` (or equivalent) names the
  load-bearing scientific choices; defaults are commented in code
  with rationale; the maintainer can list the assumptions that
  *should not* be changed without a proposal.
* **Poor**: The science is "in the code" with no separate
  rationale; defaults are folklore; the maintainer would not
  know if a contributor silently changed a sign.

*Your answer:*

`<...>`

---

## Self-score summary

For each section, mark Good (G) / Mixed (M) / Poor (P).  This
is a self-locate aid, not a scorecard -- nobody else reads it
unless you share it.

| # | Section | Score |
|---|---------|-------|
| 1 | Tests | `<G/M/P>` |
| 2 | Hidden state | `<G/M/P>` |
| 3 | Scripts | `<G/M/P>` |
| 4 | Notebooks | `<G/M/P>` |
| 5 | Data I/O | `<G/M/P>` |
| 6 | Generated outputs | `<G/M/P>` |
| 7 | Public APIs | `<G/M/P>` |
| 8 | Build / run commands | `<G/M/P>` |
| 9 | Reproducibility | `<G/M/P>` |
| 10 | Security boundaries | `<G/M/P>` |
| 11 | Scientific assumptions | `<G/M/P>` |

---

## Profile mapping -- which Cairn level

The mapping below is a guide, not a verdict.  Your maintainer
judgment overrides it; the dimensional matrix in
[`dimensions/`](../dimensions/) carries the full doctrine.

* **Mostly Good (≥8 G)**: you can run **Level 2** (full
  bootstrap) cleanly.  Pick a profile from
  [`bootstrap/profiles/`](../bootstrap/profiles/) and run
  [`bootstrap/BOOTSTRAP.md`](../bootstrap/BOOTSTRAP.md).
* **Mostly Mixed, 1-2 Poor (≥6 G/M, ≤2 P)**: **Level 1**
  (hand-copy the kernel) is the right starting point.  Your
  apparatus stays light while you fix the P-scored sections.
  Move to Level 2 once those sections lift.
* **Several Poor (≥3 P)**: **Level 0** for now -- read
  [`doctrine/`](../doctrine/) as a handbook, and use *this
  report's P sections* as the queue of things to fix before
  you add the Cairn apparatus.  Adding apparatus to a codebase
  with unclear hidden state, unstable I/O, or undocumented
  scientific assumptions amplifies the problems rather than
  fixing them.
* **Section 10 (Security boundaries) is Poor regardless of
  others**: do not scaffold Cairn yet.  Establish the
  privacy boundary first (see
  [`bootstrap/SAFETY.md`](../bootstrap/SAFETY.md)).  An AI
  agent reading a tree where the maintainer cannot say what
  is sensitive is a risk multiplier.
External-repo paths: `docs/assumptions.md`
* **Section 11 (Scientific assumptions) is Poor regardless
  of others**: still scaffold-able, but **the first proposal
  the new Cairn instance should accept is a
  docs/assumptions.md file -- write down the load-bearing
  scientific choices before any AI agent edits them.**

---

## What this report does *not* do

* It does not score *your code's correctness*.  A codebase can
  be scientifically correct and still score Poor on most
  sections -- the report measures whether the codebase is
  *ready for AI-assisted development under Cairn*, not whether
  the science is right.
* It does not commit you to anything.  Filling it is useful
  even if you decide Cairn is not the right framework.
* It does not replace
  [`bootstrap/BOOTSTRAP.md`](../bootstrap/BOOTSTRAP.md)'s Act I
  assessment -- the bootstrap's six-axis dimensional profile is
  a different lens (the codebase + team, not the codebase's
  fitness for adoption).  Run both before a full Level 2 install.
