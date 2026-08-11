<!-- Opened 2026-06-05 (migrated 2026-06-12 from modflow_tools dev/strategy/,
     Cairn's development home before self-hosting). Rewritten top-down
     2026-08-11: the original line-count instrument and the ledgers built on it
     are retired, not archived -- see "Why the previous instrument was retired".
     Strategy notes are inline-revised, so the arc lives in git log. -->

# Cairn complexity — a measured instrument, and what it finds

**Author**: Claude (Strategy & Research Agent)
**Model**: Opus 4.8 (2026-06-05 original); Opus 5 (2026-08-11 rewrite)
**Date**: 2026-06-05, rewritten 2026-08-11
**Status**: draft (the rewrite has not been reviewed; prior conclusions retired)
**Type**: design-exploration
**Surfaces this would feed**: a proposal to ship the measurement script as a
Cairn tool; a re-scoped split queue (the previous queue is withdrawn below); the
cost-validation study that would tell Cairn whether any of this work pays.

---

## The question

**What should Cairn measure to know where complexity is actually costing it
something?**

Not "which file is biggest." That question has an easy answer and a useless
one. The question that matters is where the project is *paying interest* — and
that requires an instrument that can tell a large-but-flat file from a
small-but-tangled one, and can tell a file being actively fought with from one
that has been stable for a month.

The previous version of this note answered the easy question. It built a ledger
from line counts and top-level `def` counts, screened files by size, and
convicted them by reading their symbol names. That instrument produced a
plausible queue, and the queue was wrong in ways this rewrite can now
demonstrate — so the instrument is retired and rebuilt here.

## Why the previous instrument was retired

Three defects, in ascending order of seriousness. They are recorded because
each one shaped the replacement, not as a post-mortem for its own sake.

**1. It measured volume, not complexity.** Lines and top-level `def` count are
size proxies. A file of forty flat, independent functions is easier to work in
than a six-hundred-line file with depth-8 nesting and one shared mutable path.
The old instrument ranked them the wrong way round, and its central table
sorted by a number that answers no question anyone has.

**2. Its "symptom" was a reading, not a measurement — and its validation was
close to circular.** The old note was careful to say size only *screens* and
that responsibility spread *convicts*. Good instinct. But it operationalized
responsibility spread by **clustering symbol names by hand**, which measures
naming discipline, not coupling. The note then offered, as its headline
evidence, that this method "predicted the seams" of two later splits. It did —
but the names and the splits share an author lineage and a naming convention,
so name-clustering predicting where that author would cut is very nearly a
tautology. It demonstrated that the codebase is consistently named. It did not
validate the criterion. **Treating that as validation was the note's largest
error**, because it licensed a queue nobody re-checked.

**3. It had no cost side, so it had no stopping rule.** "Debt" implies
interest. The old note never asked what any monolith actually cost — in review
findings, revision rounds, or rework — and so could not say when the work was
done. The symptom of that gap is visible in the record: a program declared
*bounded and complete* immediately regenerated a second ledger of the same
shape. That was not a discovery. That was an instrument with no zero.

**What survives.** The screen/convict two-stage shape is right; only the
convicting step was wrong. The bounded-program discipline — order by value,
gate follow-ons on the first one proving the cost model — is right, and is
reused below. And the trust-boundary factor was right but *underweighted*: on a
trust root, complexity is a **reviewability** property, which is a security
property, not an aesthetic one.

## Method

Four instruments, all standard-library Python plus `git`, all re-runnable. The
script is ~110 lines and currently lives outside the tree; productionizing it is
Recommendation 1.

1. **Function-level shape.** Per module-level function: line span and maximum
   nesting depth (`ast`, counting `If`/`For`/`While`/`With`/`Try`). Per file:
   function count, and **concentration** = share of all function lines held by
   the largest three.
2. **Measured separability.** Build the intra-file call graph among
   module-level functions (`ast.Call` resolved by name), take connected
   components, and count components with ≥2 members as candidate subsystems.
   This replaces name-reading with something reproducible.
3. **Churn.** `git log` commit counts per file, in a bounded recent window.
4. **Hotspot.** `recent churn × concentration × max nesting` — the
   churn-weighted priority that says *stable complexity is cheap; complexity
   you keep touching is not.*

Plus **change coupling**: co-change frequency between file pairs over a 60-day
window, normalized by each file's own churn.

### Limits, stated up front

Every one of these is a proxy, and two of them bit during this pass:

* **The churn window is nearly the whole repository.** History begins
  2026-05-19; this pass ran 2026-08-11. A first attempt used a 90-day window,
  which is the entire project — so "recent churn" equalled "all churn" and
  carried no recency signal at all. The tables below use **30 days**. Any
  future run must re-check this: the window has to be short relative to the
  history, and Cairn's history is still short.
* **`--follow` inherits rename history.** `upgrade.py` and `cli.py` report
  ~90+ all-time commits because `--follow` traces them back through the
  `scaffold.py` split. All-time churn is therefore **not comparable** between
  pre- and post-split files. Only the windowed figure is used for ranking.
* **The call graph is name-resolved.** It matches `ast.Call` nodes by
  identifier or attribute name, so it over-matches same-named methods and
  misses dynamic dispatch. More importantly, **a single shared helper collapses
  everything into one component**, so a low component count is weak evidence of
  cohesion. It is strong evidence *against* a confident high count — which is
  the use it is put to below.
* **Concentration is uninterpretable without function count.** A file with two
  module-level functions scores 1.00 trivially. Read the two columns together.
* **Nesting depth is a crude stand-in** for cognitive complexity — no
  cyclomatic count, no boolean-operator weighting.

**What would falsify the ranking:** the cost study in Recommendation 2. If
findings-per-change shows no relationship to hotspot rank, this instrument is
measuring shape that nobody pays for, and it should be retired the same way its
predecessor was.

## Findings

### The ranking (30-day churn window, 2026-08-11, files ≥400 lines)

`conc` = top-3 function-line share · `nest` = max nesting · `subs` = call-graph
components with ≥2 members · `30d` = commits in window · `hot` = 30d × conc × nest

| # | File | ln | fns | conc | nest | subs | 30d | hot |
|---|---|---|---|---|---|---|---|---|
| 1 | `bootstrap/_scaffold/lockfile.py` | 633 | 12 | 0.69 | **8** | 2 | 5 | **27.7** |
| 2 | `bootstrap/_scaffold/cli.py` | 753 | **2** | 1.00 | 4 | 1 | 6 | 24.0 |
| 3 | `bootstrap/_scaffold/config.py` | 1769 | 17 | 0.65 | 5 | 2 | 7 | 22.6 |
| 4 | `tools/lifecycle_planner.py` | 1728 | 46 | 0.28 | 5 | 2 | 13 | 18.2 |
| 5 | `bootstrap/security_check.py` | 1099 | 33 | 0.29 | 5 | **3** | 8 | 11.6 |
| … | | | | | | | | |
| 11 | `bootstrap/_scaffold/install.py` | 1848 | 34 | 0.34 | 4 | **4** | 5 | 6.8 |
| 14 | `bootstrap/_scaffold/upgrade.py` | **2353** | 37 | 0.40 | 4 | **1** | 4 | 6.3 |
| 15 | `tools/lifecycle.py` | 1412 | 44 | 0.25 | 4 | 2 | 6 | 6.0 |

### F1 — The two files the size screen never looked at are the top two hotspots

**`lockfile.py` is 633 lines** — far below any threshold the old instrument
would have noticed — and carries **nesting depth 8, the deepest in the
repository**, with 69% of its function lines in three functions. It is also the
integrity record: the artifact `verify_integrity` reads to decide whether an
adopter's tree has been tampered with. Depth-8 control flow on the file that
decides a trust question is a **reviewability** problem before it is a
complexity one.

**`cli.py` is 753 lines in two module-level functions.** Not "top-three
dominate" — there are only two. This is the purest mega-function surface in the
engine, and the old instrument's `def`-count screen actively hid it: a low
function count read as *simple*.

### F2 — The previous queue is falsified on both its headline rows

This note's own prior version, committed 2026-08-10, is the thing being
corrected:

* **`upgrade.py` was ranked the headline split** on 2,353 lines and a claimed
  **"≥6 separable subsystems."** That figure came from reading name prefixes.
  The measured call graph does not support it — the module-level functions form
  **one** connected component, and the file ranks **14th** by hotspot with the
  *lowest recent churn* of the top-15. It is the largest file in the engine and
  close to the least troublesome by every measure that isn't size. Its long
  functions (`_compute_upgrade`, 341 ln) are a real finding; "six subsystems
  waiting to be lifted" was not.
* **`lifecycle.py` was promoted from watch to split-tier** because its line and
  `def` counts grew ~20%. It ranks **15th**, with the **lowest concentration of
  any large file (0.25)** — i.e. it grew by adding *more, smaller* functions,
  which is what healthy growth looks like. The promotion is withdrawn.

The old trigger fired on growth. Growth in a well-decomposed file is not debt,
and an instrument that cannot tell those apart will keep generating queues.

### F3 — Separability and pain are different axes, and the old note conflated them

`install.py` has the **most** candidate subsystems (4) of any file measured —
it is the most genuinely *separable* file in the engine. It also ranks 11th by
hotspot: low concentration, moderate nesting, modest churn. It is easy to split
and there is little reason to.

`lockfile.py` has 2 components and is the top hotspot. Hard to split, and it is
where the cost is.

**Separability tells you whether a split is cheap. Hotspot tells you whether it
is worth doing.** A queue ordered by the first is a queue ordered by
convenience.

### F4 — Change coupling finds nothing hidden, which is a real result

Over 60 days and 88 commits touching Python, the only strong co-change pairs
are **shipped↔self-hosted twins**:

| co-change | pair |
|---|---|
| 92% (12×) | `templates/skills/_lib/lifecycle_planner.py` ↔ `tools/lifecycle_planner.py` |
| 80% (4×) | `scripts/claim_check.py` ↔ `templates/modules/default-on/claim_check.py` |
| 57% (4×) | `templates/skills/_lib/lifecycle.py` ↔ `tools/lifecycle.py` |

These are *by construction* — a byte-parity test enforces them, deriving its
pairs from the installer's own manifest. Below them, nothing crosses the
threshold. **There is no logical module smeared across unrelated files**, which
is the inverse debt a size-only instrument is structurally blind to and which a
split-heavy program might plausibly have created. The architecture is clean on
this axis; the instrument earns its keep by being able to say so.

The twins do swamp the signal, so change coupling is low-yield for Cairn until
it can exclude manifest twins by construction.

### F5 — The trust surfaces cluster at the top, and that should drive priority

Four of the top five hotspots are trust-relevant: `lockfile.py` (integrity
record), `config.py` (profile parsing — its deepest function is
`_minimal_yaml_parse`, the fallback parser an independent review separately
flagged as diverging from the real parser), `cli.py` (the engine's entry
point), and `security_check.py` (3 subsystems, the scan surface).

That is not a coincidence to note in passing. On a trust root, the question
complexity actually poses is *can one reviewer hold the path from untrusted
input to a dangerous sink in their head?* — and depth-8 nesting on the
integrity record is a direct answer of "no." **Trust-boundary concentration
should be the primary ordering factor, not a secondary multiplier.**

## What this instrument still cannot see

It measures *shape* and *activity*. It does not measure **cost**, and cost is
the whole justification for the word "debt."

Cairn is unusually well-positioned to close this, and has not: `lifecycle_metrics`
already extracts review findings, revision counts, and time-to-decision per
proposal, and every plan's commits are discoverable by subject stem. The join
is available and unrun:

> for each archived plan → its commits (`git log --grep='^<stem>:'`) → the files
> those commits touched → **findings and revision rounds per surface**.

That yields the number this note has never had: *does changing a
high-complexity surface actually cost more review?* It also yields a real test
of the completed split program — post-split changes to `_scaffold/` should show
lower findings-per-change than pre-split changes to `scaffold.py`, or the
program did not pay for itself.

Until that runs, every ranking here — including the corrected one — is a
hypothesis about where cost lives, not a measurement of it.

## Options

1. **Retire complexity auditing entirely** until something hurts. Defensible:
   no incident traces to any file on this list, and the security and lifecycle
   work in flight is higher-stakes. Cost: the trust-surface reviewability
   finding (F5) goes unaddressed, and that one is about review integrity.
2. **Ship the instrument, act on nothing yet.** Make the measurement
   reproducible and re-run it at release boundaries; let evidence accumulate
   before opening any split.
3. **Ship the instrument and run the cost study**, then let the two together
   decide the queue. Slower to a first refactor, but it is the only path that
   produces a stopping rule.
4. **Act on the current ranking now** — take `lockfile.py` and `cli.py` on
   their hotspot scores. Fastest, and repeats the previous instrument's
   mistake: acting on an unvalidated proxy.

## Recommendation

**Option 3, in three steps, and no split opens until step 2 reports.**

1. **Ship the measurement as a Cairn tool** (~110 lines, stdlib-only, so it
   sits inside the dependency budget). It belongs beside `quality_gate.py` as a
   *report*, not a gate — there is no defensible threshold to fail a build on,
   and inventing one would repeat the line-count error at higher cost. Fix the
   window relative to history at runtime rather than hardcoding 30 days.
2. **Run the cost study** described above. It is a join over data Cairn already
   produces, and it is the only thing that can falsify the ranking or retire
   the whole inquiry. This is the highest-value item in the note.
3. **Then, and only then, open at most one split** — chosen by hotspot ×
   trust-surface × measured cost, not by size. On present evidence that is
   `lockfile.py`, and the framing is reviewability of the integrity record, not
   its line count.

**Withdrawn, explicitly:** the `upgrade.py` split (its "≥6 subsystems" was a
reading the measurement contradicts), the `lifecycle.py` promotion to
split-tier (it is among the healthiest large files), and the `install.py` /
`config.py` "screened, pending a symbol read" rows — symbol reads are the
method being retired. `config.py` returns on its own merits at rank 3.

**Two smaller items, independent of the above:** the `_minimal_yaml_parse`
depth (F5) is worth a targeted look as a *correctness* question rather than a
complexity one, since an independent review already flagged its behaviour. And
`doctrine/plans.md` at 836 lines — corpus-largest, with ~900 words duplicated
against `proposals.md` — is a one-home violation to fix as such, not a size
target to hit.

**The stopping rule this note previously lacked:** the queue is empty when
findings-per-change on the remaining surfaces is indistinguishable from the
repository baseline. Without that number, any ledger regenerates forever — as
the last one did, within a day of being declared complete.

## Open questions for the maintainer

1. **Appetite.** Option 3 (instrument + cost study, no split yet), or Option 1
   (retire the inquiry until something hurts)? *(Recommended: 3 — but 1 is a
   real answer, and better than the status quo of queues nobody validates.)*
2. **Does the instrument ship?** As a report beside `quality_gate.py`, or does
   it stay a scratch tool re-run by hand at release boundaries? *(Recommended:
   ship it as a report — an instrument nobody can re-run is how the last
   ledger went two months without anyone noticing it had inverted.)*
3. **Trust-surface priority.** Promote trust-boundary concentration to the
   primary ordering factor? *(Recommended: yes. It reframes complexity work as
   review integrity, which is a thing Cairn already claims to care about, and
   it is the finding on this list with an actual argument behind it.)*
4. **Is `lockfile.py`'s depth-8 nesting a security review item now**, ahead of
   any refactor? *(Recommended: yes, and cheaply — one reviewer reading the
   integrity path end to end and reporting whether they could hold it.)*

## Fold-up note

The remediations are Cairn-internal. Three findings are methodology-general and
are fold-up candidates, each needing its own proposal under the
one-incident-is-not-doctrine rate-limit gate:

* **Name-clustering is not evidence when the namer and the splitter share an
  author.** The general rule: a predictor validated only against work by the
  same author, under the same conventions, is validated against its own
  assumptions. This generalizes well past complexity auditing — it is the same
  structure as the shared-blind-spot argument that motivates Cairn's External
  review tier, applied to a measurement rather than a review.
* **A debt ledger without a cost side has no stopping rule and will
  regenerate.** Demonstrated here twice: a bounded program completed, and the
  next ledger opened the following day.
* **On a trust boundary, complexity is a reviewability property.** The metric
  that matters is whether one reviewer can hold the untrusted-input-to-sink
  path, not the file's length. Cairn already ties decision authority to
  comprehension; this is that same principle applied to code review.
