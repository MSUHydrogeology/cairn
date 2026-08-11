<!-- Migrated 2026-06-12 from modflow_tools dev/strategy/ (Cairn's development
     home before self-hosting); see dev/strategy/MIGRATION.md. Strategy notes
     are inline-revised, so the deliberation arc lives in git log, not here. -->

# Cairn complexity — a measured instrument, its grounding, and what it finds

**Author**: Claude (Strategy & Research Agent)
**Model**: Opus 5
**Date**: 2026-06-05, last revised 2026-08-11
**Status**: revised (External round 1 — Codex, security lens — folded in and
removed 2026-08-11)
**Type**: design-exploration
**Surfaces this would feed**: one bounded validation proposal that carries the
instrument, its fixtures, and a preregistered cost pilot together; a targeted
Security read of the integrity path; the release-boundary re-measure cadence.

---

## The question

**What should Cairn measure to know where complexity is actually costing it
something?**

Not "which file is biggest." That question has an easy answer and a useless
one. What matters is where the project pays *interest* — which needs an
instrument that can tell a large-but-flat file from a small-but-tangled one,
and a file being actively fought with from one that has been stable.

This note builds that instrument, grounds it in the measurement literature,
reports what it finds, and — most importantly — states what it is not yet
entitled to conclude.

## Framework anchors

The complexity-measurement literature is unusually well developed *and*
unusually humbling: several of its strongest results argue against the kind of
instrument built here. Both directions are recorded, because an anchor set that
only supports the author's design is decoration.

**Static measurement — and the case against it**

1. **Control flow as the unit** — McCabe, T. J. (1976). *A Complexity
   Measure.* IEEE Transactions on Software Engineering SE-2(4): 308–320. The
   founding move: measure a program's branching structure, not its length.
2. **The correlation problem** — Jay, G., Hale, J. E., Smith, R. K., Hale, D.,
   Kraft, N. A., & Ward, C. (2009). *Cyclomatic Complexity and Lines of Code:
   Empirical Evidence of a Stable Linear Relationship.* Journal of Software
   Engineering and Applications 2(3): 137–143. Cyclomatic complexity is
   strongly, roughly linearly correlated with size across large corpora — so a
   static complexity metric may be **re-measuring length in a costlier way**.
   This is the sharpest threat to the static half of the instrument below, and
   it generates a concrete obligation: show decorrelation from lines, or admit
   the metric adds nothing.
3. **Nesting-weighted readability** — Campbell, G. A. (2018). *Cognitive
   Complexity: An Overview and Evaluation.* Proceedings of the 1st
   International Conference on Technical Debt (TechDebt '18). Designed
   explicitly to fix what cyclomatic complexity misses about human
   comprehension by penalizing *nested* control flow rather than counting
   branches. The nesting proxy used below is a crude approximation of it.

**Process measurement — the better-supported half**

4. **Process beats product** — Rahman, F., & Devanbu, P. (2013). *How, and Why,
   Process Metrics Are Better.* Proceedings of the 35th International
   Conference on Software Engineering (ICSE 2013). History-derived metrics
   (churn, developer counts, change patterns) outperform code-derived metrics
   for defect prediction, and generalize better across projects. The strongest
   single reason to weight the churn side of any hotspot formula.
5. **Relative, not absolute, churn** — Nagappan, N., & Ball, T. (2005). *Use of
   Relative Code Churn Measures to Predict System Defect Density.* ICSE 2005.
   Churn normalized by file size predicts defect density; absolute churn
   predicts much less well. A direct, unmet specification for the formula
   below.
6. **Change coupling** — Gall, H., Hajek, K., & Jazayeri, M. (1998).
   *Detection of Logical Coupling Based on Product Release History.* ICSM 1998;
   with Zimmermann, T., Weissgerber, P., Diehl, S., & Zeller, A. (2005).
   *Mining Version Histories to Guide Software Changes.* IEEE Transactions on
   Software Engineering 31(6): 429–445. Files that change together are coupled
   whether or not any static analysis can see it — the one debt class a
   file-shape instrument is structurally blind to.
7. **The practitioner synthesis** — Tornhill, A. (2018). *Software Design
   X-Rays: Fix Technical Debt with Behavioral Code Analysis.* Pragmatic
   Bookshelf. Hotspot = complexity × change frequency. Trade press rather than
   peer-reviewed, and used here as the *shape* of the priority function, with
   anchors 4–5 supplying its empirical warrant.

**Structure, cohesion, and clustering**

8. **The construct being approximated** — Stevens, W. P., Myers, G. J., &
   Constantine, L. L. (1974). *Structured Design.* IBM Systems Journal 13(2):
   115–139. Coupling and cohesion are the actual properties; "separable
   subsystems" is a restatement of cohesion, and should be measured as such.
9. **How to find modules properly** — Newman, M. E. J. (2006). *Modularity and
   Community Structure in Networks.* PNAS 103(23): 8577–8582; with Mancoridis,
   S., Mitchell, B. S., Rorres, C., Chen, Y., & Gansner, E. R. (1998). *Using
   Automatic Clustering to Produce High-Level System Organizations of Source
   Code.* IWPC 1998. Community detection over a weighted graph, optimizing
   modularity, is the established method. **Connected components — what the
   instrument below actually computes — is a degenerate special case** that any
   single shared helper collapses to one.

**Debt, review, and evidence discipline**

10. **Debt needs an interest model** — Cunningham, W. (1992). *The WyCash
    Portfolio Management System.* OOPSLA '92 Experience Report (the origin of
    the metaphor); with Kruchten, P., Nord, R. L., & Ozkaya, I. (2012).
    *Technical Debt: From Metaphor to Theory and Practice.* IEEE Software
    29(6): 18–21, which argues the metaphor is only useful when principal and
    interest are made concrete. A ledger without a cost side is the failure
    mode this anchor names.
11. **Review as the thing complexity actually taxes** — Rigby, P. C., & Bird,
    C. (2013). *Convergent Contemporary Software Peer Review Practices.*
    ESEC/FSE 2013; with Sadowski, C., Söderberg, E., Church, L., Sipko, M., &
    Bacchelli, A. (2018). *Modern Code Review: A Case Study at Google.*
    ICSE-SEIP 2018. Review effectiveness falls as change size and complexity
    rise — the mechanism behind treating trust-surface complexity as a
    reviewability problem.
12. **Register before you measure** — Chambers, C. D. (2013). *Registered
    Reports: A New Publishing Initiative at Cortex.* Cortex 49(3): 609–610.
    Specifying hypothesis, population, and analysis before seeing results is
    the guard against fitting a conclusion to a table. Cairn's own proposal
    template is already registered-report-shaped; the cost pilot below inherits
    that discipline rather than inventing it.

**What the anchor set implies, taken together.** Anchors 2 and 4 point the same
way: **the history-derived half of this instrument is better supported than the
static half**, and the static half owes a decorrelation check before it earns
its place. Anchors 5 and 9 say two specific components are mis-specified as
built. Anchor 10 says the whole exercise is unjustified until cost is modeled.
That is the honest position: a defensible triage tool, not a measurement of
debt.

## Why size alone is the wrong screen

Lines and top-level `def` counts are volume proxies. A file of forty flat,
independent functions is easier to work in than a six-hundred-line file with
depth-8 nesting and one shared mutable path, and a size-ordered list ranks them
backwards.

Two failure modes follow, and both are visible in the findings below. A
size-ordered screen **misses small tangled files entirely** — the top-ranked
artifact here is 633 lines, far below any threshold a size screen would set.
And a `def`-count screen **reads a mega-function file as simple**, because two
enormous functions score lower than forty small ones.

There is also a methodological trap worth naming, since it is cheap to fall
into and expensive to detect: **inferring module boundaries by clustering
symbol names by hand is not evidence.** Names and structure share an author and
a naming convention, so name-clustering predicts where that author *would* cut,
which is close to circular. It demonstrates naming consistency. Anchor 8 names
the property actually wanted (cohesion) and anchor 9 the method that measures it.

## Method

Four instruments, standard-library Python plus `git`.

1. **Function-level shape** — per module-level function, line span and maximum
   nesting depth (`ast`, counting `If`/`For`/`While`/`With`/`Try`); per
   artifact, function count and **concentration**, the share of all function
   lines held by the largest three.
2. **Separability** — the intra-file call graph among module-level functions
   (`ast.Call` resolved by name), reported as connected components with ≥2
   members.
3. **Churn** — commits touching the artifact in a bounded recent window.
4. **Hotspot** — `churn × concentration × max nesting`.

Plus **change coupling**: co-change frequency between pairs over a 60-day
window, normalized by each file's own churn.

### The corpus, declared before the ranking

A ranking is meaningless unless its population is stated, and partial
exclusions silently reshape conclusions. The corpus rule, fixed in advance:

* **Every tracked `.py` file of ≥400 lines is in scope** — including files that
  live only under `templates/`. Shipped templates are not prose; several are
  registered executable trust roots, and excluding them would bias exactly the
  trust-surface question this note asks.
* **Byte-identical copies collapse to one logical artifact.** Cairn
  self-hosts the tools it ships, so twins are one thing in two places. The
  representative is the non-`templates/` path; **churn is the union of commits
  touching any copy** — using either copy alone understates it, and the copies
  do not carry equal history.
* **Tests are a separate stratum**, never mixed into the production ranking.
  The instrument counts module-level functions and ignores `pytest` class
  methods, so a class-based test file reports a structure it does not have.
* **Strata are ranked independently.** A cross-stratum rank has no meaning.

### Limits, stated before the findings

* **Concentration is uninterpretable without function count.** Two
  module-level functions score 1.00 trivially — read the columns together.
* **Nesting is a crude stand-in** for cognitive complexity (anchor 3): no
  cyclomatic count, no boolean-operator weighting.
* **The hotspot formula multiplies file-level churn and concentration by the
  deepest function's nesting** — three observations that may come from three
  different functions and three unrelated changes. It is a triage score, not a
  claim about any particular function.
* **Churn is absolute, not size-normalized**, contrary to anchor 5. This is a
  known mis-specification, not a considered choice.
* **Connected components is the degenerate case of module detection**
  (anchor 9): one shared helper collapses a file to a single component. A low
  count is therefore weak evidence of cohesion, though it is strong evidence
  *against* a confident high count.
* **The call graph is name-resolved** — it over-matches same-named methods and
  misses dynamic dispatch.
* **The churn window must stay short relative to history.** Cairn's history
  begins 2026-05-19; a 90-day window is the entire project and carries no
  recency signal at all. The tables use 30 days, and any future run must
  re-derive the window rather than inherit it.
* **`--follow` inherits rename history**, so all-time churn is not comparable
  across the scaffold split. Only windowed churn is ranked.

**What would falsify this instrument.** Two tests, both currently unrun. If
hotspot rank shows no relationship to measured review cost, it is ranking shape
nobody pays for. And if the static components do not decorrelate from raw line
count (anchor 2), they are an expensive way to sort by size.

## Findings

Measured 2026-08-11 against the working tree at `0e6ce06` (one unrelated file
modified). Twins collapsed; `cp` = copies collapsed into the artifact.

### Production stratum — 34 artifacts ≥400 lines, top 12

| # | Artifact | ln | fns | conc | nest | subs | 30d | hot | cp |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `bootstrap/_scaffold/cli.py` | 754 | **2** | 1.00 | 4 | 1 | 7 | **28.0** | 1 |
| 2 | `bootstrap/_scaffold/lockfile.py` | 633 | 12 | 0.69 | **8** | 2 | 5 | 27.7 | 1 |
| 3 | `bootstrap/_scaffold/config.py` | 1773 | 17 | 0.65 | 5 | 2 | 8 | 25.9 | 1 |
| 4 | `scripts/run_portable_security_sweeps.py` | 1858 | 39 | 0.38 | 7 | 1 | 8 | 21.3 | 2 |
| 5 | `tools/lifecycle_planner.py` | 1728 | 46 | 0.28 | 5 | 2 | 13 | 18.2 | 2 |
| 6 | `scripts/content_scan.py` | 914 | 22 | 0.41 | 4 | 1 | 9 | 14.7 | 2 |
| 7 | `bootstrap/security_check.py` | 1099 | 33 | 0.29 | 5 | **3** | 8 | 11.6 | 1 |
| 8 | `tools/lifecycle.py` | 1412 | 44 | 0.25 | 4 | 2 | 10 | 9.9 | 2 |
| 9 | `scripts/claim_check.py` | 878 | 19 | 0.45 | 5 | 1 | 4 | 9.0 | 2 |
| 10 | `scripts/content_scan_runner.py` | 610 | 14 | 0.56 | 4 | 1 | 4 | 8.9 | 2 |
| 11 | `tools/_intent/cli.py` | 502 | 9 | 0.71 | 5 | 1 | 2 | 7.1 | 2 |
| 12 | `bootstrap/_scaffold/install.py` | 1848 | 34 | 0.34 | 4 | **4** | 5 | 6.8 | 1 |

### F1 — The instrument's whole value is that its top three are not the biggest files

`cli.py` (754 ln) and `lockfile.py` (633 ln) sit at ranks 1 and 2. The two
largest files in the corpus — `run_portable_security_sweeps.py` (1,858) and
`install.py` (1,848) — sit at 4 and 12. `bootstrap/_scaffold/upgrade.py`, the
largest file in the engine at 2,353 lines, **does not appear in the top twelve
at all**: concentration 0.40, nesting 4, and the lowest recent churn of any
large engine file.

That divergence is the instrument's entire claim to existence, and per anchor 2
it is also the thing that must be verified quantitatively rather than admired
in a table.

Two specific shapes the size screen inverts:

* **`cli.py` is 754 lines in two module-level functions.** Not "the top three
  dominate" — there are only two. A `def`-count screen reads this as simple.
* **`lockfile.py` carries nesting depth 8, the deepest in the repository**, at
  633 lines — below any plausible size threshold — with 69% concentration.

### F2 — Separability and pain are different axes

`install.py` has the **most** candidate subsystems (4) in the corpus — the most
genuinely separable artifact — and ranks 12th by hotspot. It is cheap to split
and there is little reason to. `lockfile.py` has 2 and ranks 2nd: harder to
split, and where the cost appears to be.

**Separability estimates whether a split is cheap; hotspot estimates whether it
is worth doing.** Ordering a queue by the former orders it by convenience. Both
are proxies, and per anchor 9 the separability figure is the weaker of the two.

### F3 — Trust surfaces cluster at the top

Five of the top seven are trust-relevant: `cli.py` (engine entry point),
`lockfile.py` (the integrity record `verify_integrity` reads),
`config.py` (profile parsing), `run_portable_security_sweeps.py` (a registered
executable trust root), and `security_check.py` (the scan surface, and the
corpus's second-highest subsystem count).

Per anchor 11, review effectiveness degrades as complexity rises, which makes
this a **reviewability** question rather than an aesthetic one: can one reviewer
hold the path from untrusted input to a dangerous sink? That argues
trust-boundary concentration should be the **primary** ordering factor.

The limit on that inference is real and worth stating precisely: the instrument
**traces no input-to-sink path**. Depth-8 nesting on the integrity record does
not establish that no reviewer can comprehend it. It establishes that
`lockfile.py` is the highest-priority surface to *inspect*. The inspection is
the evidence; the metric is only the triage.

### F4 — Change coupling finds nothing hidden, which is a real result

Over 60 days and 88 commits touching Python, the only strong co-change pairs
are byte-identical twins — 92% (`lifecycle_planner`), 80% (`claim_check`), 57%
(`lifecycle`) — which a parity test enforces by construction, deriving its pairs
from the installer's own manifest. Below them, nothing crosses threshold.

Per anchor 6, this is the one debt class file-shape analysis cannot see, and
the answer is clean: **no logical module is smeared across unrelated files.**
The twins swamp the signal, so this instrument stays low-yield for Cairn until
it excludes manifest twins by construction — which the corpus rule above now
does for the shape metrics and should also do here.

### F5 — Tests are a different population and must never share a ranking

The test stratum's top artifact (`test_transition_lint.py`, hot 12.9) would
place fifth in a merged list, and `test_scaffold.py` reports **1,192 lines in
one module-level function, concentration 1.00** — an artifact of class-based
test structure, not a mega-function. Any merged ranking is measuring the
instrument's blind spot rather than the code.

## What this instrument cannot see

It measures shape and activity. It does not measure **cost** — and per anchor
10, cost is the entire justification for the word "debt."

The obvious-looking join is **not available**, and the specifics matter because
they determine what a real study must do instead:

* `lifecycle_metrics`' per-plan rows carry **round counts** (plan-review,
  code-review), not code-review finding counts and not file attribution. Its
  finding counts are **per proposal** — raised *before* implementation, mostly
  against design and governance. Attributing those to every file a later plan
  touched cannot show that a code surface caused review cost.
* Recovering a plan's commits by subject stem is incomplete: the literal
  `git log --grep='^<stem>:'` recipe returns **zero commits for 7 of 34
  archived plans**, because implementation subjects also take forms like
  `<stem> Chunk …` or a component name.

So the cost side needs a **purpose-built pilot**, not a query. Per anchor 12,
its design is registered before its results exist:

* **Unit of change** — a plan's reviewed implementation range.
* **Outcome** — findings extracted from that plan's `## Code review` passes,
  attributed to a file only when the finding or its disposition **names that
  file**. Zero-finding plans are retained; dropping them is the survivorship
  error.
* **Covariates** — review tier, changed lines, mechanical-only changes, and
  trust-surface status.
* **Kept separate** — proposal findings and plan-review findings remain their
  own process outcomes, never evidence that code shape caused rework.
* **Declared in advance** — repository baseline, minimum sample, uncertainty
  treatment, and an explicit **INCONCLUSIVE** outcome, so "indistinguishable
  from baseline" is a defined result rather than a rhetorical exit.

A manual pilot over a handful of plans is preferable to expanding
`lifecycle_metrics` before the signal is known to exist.

Until that runs, every ranking here is a **hypothesis about where cost lives**,
not a measurement of it.

## Options

1. **Retire the inquiry** until something hurts. Defensible — no incident
   traces to any artifact on this list. Cost: the trust-surface reviewability
   question (F3) goes unasked, and that one is about review integrity.
2. **Ship the instrument as a standing Cairn tool now**, act on nothing.
   Premature: it would give an unvalidated proxy a maintained product surface
   and the authority that comes with one.
3. **Carry the instrument inside a bounded validation proposal** — fixtures,
   declared corpus, the preregistered cost pilot, and the targeted Security
   read — and decide afterwards whether it deserves to be a product.
4. **Act on the current ranking now.** Fastest, and it treats an explicitly
   unvalidated proxy as a finding.

## Recommendation

**Option 3, with the Security read running in parallel.**

1. **One proposal carries the instrument and its validation together.** The
   script, golden fixtures pinning the declared corpus and strata, the
   decorrelation check anchor 2 demands, and the preregistered cost pilot ship
   as a single reviewable unit. The instrument is *checked in* — a ranking
   nobody can reproduce is not evidence — but it is **not** promoted to a
   maintained Cairn tool until the pilot reports.
2. **Run the pilot.** It is the only thing that can either justify the queue or
   retire the inquiry, and it is the highest-value item in this note.
3. **Two mis-specifications get fixed as part of (1)**, both dictated by the
   anchors rather than by taste: size-normalized churn (anchor 5), and
   modularity-based clustering in place of connected components (anchor 9).
4. **In parallel, one targeted Security read of `lockfile.py`** — identify the
   actual integrity decision path, assess its branches and tests end to end,
   and report whether a reviewer could hold it. It is cheap, it tests this
   note's strongest inference directly, and it **authorizes no refactor**.
5. **Then, and only then, consider at most one split**, chosen by measured cost
   × trust surface, and opened only if the Security read or the pilot finds a
   concrete comprehension or defect burden.

**The stopping rule.** The queue is empty when findings-per-change on the
remaining surfaces is indistinguishable from the repository baseline — with
"indistinguishable" defined by the pilot's preregistered analysis, including its
INCONCLUSIVE branch. Without that number, per anchor 10, a ledger regenerates
indefinitely because nothing tells it when to stop.

**One adjacent item, correctly scoped.** `doctrine/plans.md` at 836 lines is
the corpus-largest doctrine file, with roughly 900 words duplicated against
`proposals.md`. That is a one-home violation to fix as such — not a size target,
and not part of this program.

## Open questions for the maintainer

1. **Appetite.** Option 3 (instrument inside a validation proposal, no split
   yet), or Option 1 (retire until something hurts)? *(Recommended: 3 — but 1
   is a real answer and better than acting on an unvalidated proxy.)*
2. **Pilot scale.** How many plans is a credible first sample, given a corpus of
   34 archived plans and a hand-extraction cost per plan? *(Recommended: the
   maintainer sets the minimum before extraction begins, per anchor 12 — not
   after seeing the first few.)*
3. **Trust-surface priority.** Promote trust-boundary concentration to the
   primary ordering factor? *(Recommended: yes — it reframes complexity work as
   review integrity, which is the finding here with an actual mechanism behind
   it, per anchor 11.)*
4. **Does this note become a `living-reference`?** It is now a standing
   instrument with a release-boundary re-measure cadence rather than a
   point-in-time exploration. The folder's validity rule ties that type to
   `Status: living` and forbids promotion, so the switch waits until the
   validation proposal has been carried. *(Recommended: convert once the pilot
   reports; keep it a `design-exploration` until then.)*

## Fold-up note

The remediations are Cairn-internal. Three findings are methodology-general and
are fold-up candidates, each needing its own proposal under the
one-incident-is-not-doctrine rate-limit gate:

* **A predictor validated only against work by the same author, under the same
  conventions, is validated against its own assumptions.** Inferring structure
  from naming is the concrete case; the general shape is identical to the
  shared-blind-spot argument that motivates Cairn's External review tier,
  applied to a measurement rather than a review.
* **A debt ledger without a cost model has no stopping rule** (anchor 10), and
  a ranking without a declared population is not reproducible — partial
  exclusions reshape conclusions silently, and excluding a trust root from a
  trust-surface finding is the flattering direction.
* **On a trust boundary, complexity is a reviewability property** (anchor 11).
  The question is whether one reviewer can hold the untrusted-input-to-sink
  path, not how long the file is. Cairn already ties decision authority to
  comprehension; this applies the same principle to code review.
