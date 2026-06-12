<!-- Migrated 2026-06-12 from modflow_tools dev/strategy/ (Cairn's development home before self-hosting). Authored from modflow_tools' vantage; some path cites and "current state" reflect that origin and are being adapted to Cairn. Preserved as Cairn's living deliberation record -- see dev/strategy/MIGRATION.md. -->
<!-- claim-check-allow: templates/modules/team-gated/intent.py, templates/modules/default-on/onboarding_activate.py, templates/modules/default-on/claim_check.py, templates/modules/default-on/lifecycle_metrics.py, templates/skills/_lib/lifecycle.py, templates/core/dev/proposals/_template.md, templates/core/dev/plans/_template.md, scripts/quality_gate.py -->
<!-- ^ Cairn-repo paths (~/Code/cairn); bootstrap/ + doctrine/ tokens don't
     resolve locally and aren't flagged (first segment not a local top-level
     dir). scripts/quality_gate.py IS a local-resolving first segment, so it is
     allow-listed explicitly. -->
<!-- claim-check-allow-count: 4865 lines, 2021 lines, 2035 lines, 1767 lines, 1173 lines, 876 lines, 823 lines, 766 lines, 776 lines, 821 lines, 800 lines, 14982 lines, 5464 lines, 449 lines, 225 lines, 1583 lines, 600 lines, 1000 lines, 12 files, 59, 50, 49, 39, 23, 18, 29 -->
<!-- ^ point-in-time line counts of ~/Code/cairn (and one modflow_tools-local
     count, `2035 lines` / `49` = the lifecycle_metrics v2 fork), computed
     2026-06-05 via the `wc -l` / `grep -cE '^(def |class )'` commands cited in
     Method; not memory-quoted. -->

# Cairn complexity-debt audit

**Author**: Claude (Strategy & Research Agent)
**Model**: Opus 4.8 (1M context)
**Date**: 2026-06-05
**Status**: revised
**Type**: comparative-research
**Surfaces this would feed**: the in-flight scaffold-split proposal
(`2026-06-05-claude-scaffold-split`, the precedent + reusable discipline); two
follow-on Cairn-internal split scopings (`intent.py`, `onboarding_activate.py`,
same shape); a lifecycle-template-thinning proposal (route accreted doctrine to
`doctrine/`); a **`lifecycle_metrics` split-then-fold-up** (split the
modflow_tools v2 fork, fold the clean package up to Cairn — eliminates Fork 7a +
upgrades Cairn).

---

## The question

While splitting `bootstrap/scaffold.py`, is Cairn carrying *other* accumulated
complexity debt worth addressing — and if so, where, and is it a bounded program
or a sprawling cleanup?

**The finding: the debt is concentrated, not pervasive.** It is a handful of
over-grown monolithic `.py` tools plus lifecycle-template bloat; everything else
is clean. That makes remediation a **bounded, sequenceable** program — finite
and orderable, though each split is a heavy refactor and the program is *gated*
on the first one proving out (see Recommendation) — not an open-ended
audit-and-fix.

## Method (so the findings are falsifiable)

Read-only scan of `~/Code/cairn`, 2026-06-05, re-runnable:

* Composition + largest files: `find … -name '*.py'/'*.md' | xargs wc -l | sort -rn`.
* Monolith signal: `grep -cE '^(def |class )' <file>` (top-level symbols per file)
  + sampling the symbol names for responsibility spread.
* Test-to-code ratio: `find bootstrap/tests` vs `find bootstrap -not tests` line sums.
* Hygiene: `grep -rInE 'TODO|FIXME|HACK|XXX|DEPRECAT'`.
* Duplication: `find -name '*.py' | sed 's#.*/##' | sort | uniq -d`.
* Template bloat: heading + `cairn:slot` counts in the `_template.md` files.
* Fork measurement (modflow_tools-local, the one non-`~/Code/cairn` probe):
  `wc -l tools/lifecycle_metrics.py` + `grep -cE '^(def |class )'` + a symbol-name
  scan — the lifecycle_metrics **v2 keep-ours fork**'s size and subsystem count.

## Findings

### Where the debt is (prioritized)

| # | Item | Size | Why it's debt |
|---|---|---|---|
| 1 | `bootstrap/scaffold.py` | 4865 lines | The headline — **already being split**. It is ~**89%** of bootstrap's non-test code (the rest of `bootstrap/` is ~600 lines). |
| 2 | `intent.py` (team-gated) | 2021 lines, **59** defs/classes | The next monolith, **same shape** as scaffold.py — five responsibilities in one file: record I/O · identity/session · conflict-check · CLI commands · git-hook install. A clean split candidate; **modflow_tools forks it** (ledger Fork 7c), so a clean Cairn split also unblocks the un-fork. |
| 3 | `onboarding_activate.py` (default-on) | 1767 lines, **50** defs/classes | The third monolith: slot/preset parsing · a large **trigger-evaluation** cluster (`_count_*`, `_has_cross_type_review_*`, `_foldback_*`) · prompt rendering. Same split treatment. |
| 4 | Lifecycle templates — `proposals/_template.md` (776 lines), `plans/_template.md` (821 lines) | ~800 lines each | **Template bloat**: 27–35 headings but only **3–4 actual `cairn:slot`s** — ~85% accreted *teaching-doctrine*, ~15% fill-in form. Both now exceed the largest doctrine file (`doctrine/lifecycle.md`, 449 lines). Per Cairn's own doc-governance routing, that doctrine belongs in `doctrine/`, leaving a thin template. |

### The criterion — size screens, a symptom convicts

Line- and def-count are a **screen**, not the verdict. The split-worthy symptom
is **responsibility spread**, defined concretely so it is not an aesthetic call:
count a file's **separable subsystems** — clusters of symbols on distinct domain
boundaries, low-coupled to each other, each liftable into its own module behind
a narrow interface. This deliberately does *not* count verbs-within-one-domain
(a single pipeline's parse/validate/format facets are **one** responsibility,
not three). The bar: size co-occurring with **≥3 separable subsystems**.

Two secondary factors *raise the priority* of a file that already clears the bar
but never promote one on their own:

* **Fork-divergence** — a file `modflow_tools` keeps-ours-forks costs more to
  carry un-split, so an upstream split also unblocks the un-fork. A payoff
  multiplier, not a trigger: a *cohesive* fork stays watch.
* **Trust-boundary concentration** — `scaffold.py` is the install/upgrade trust
  boundary no single reviewer holds at once.

Applying it (subsystem counts from the symbol-name clustering cited in Method):

| File | Lines | defs | Separable subsystems | Verdict |
|---|---|---|---|---|
| `intent.py` | 2021 | 59 | **5** — record I/O · identity/session · conflict-check · CLI · *git-hook install* (domain-orthogonal, lifts cleanly) | **split** |
| `onboarding_activate.py` | 1767 | 50 | **3** — slot/preset parse · trigger-eval · prompt render | **split** |
| `lifecycle.py` | 1173 | 39 | ~2 liftable inside a broad session-routines orchestrator | **watch** \* |
| `claim_check.py` | 876 | 23 | size-screened out | **watch** |
| `scripts/quality_gate.py` | 823 | 18 | size-screened out (dev-tool, not shipped) | **watch** |
| `lifecycle_metrics.py` | 766 | 29 | **1** — a linear extract-rows ETL (corpus → parse → row → format) | **watch** |

`lifecycle_metrics.py` needs a correction the first two reviews carried — a
**v1/fork conflation**. *Cairn's installed v1* (the 766-line row above) is one
cohesive ETL → watch *in Cairn's tree*. But the **modflow_tools keep-ours fork**
is a *different, larger* file: the v2 instrumentation at **2035 ln / 49 defs /
~6 separable subsystems** (base ETL · annotations · collision-log ·
review-yield/model-tier · manifest · snapshot time-series) — decisively
**split-tier**. So lifecycle_metrics is *not* the "forked-but-cohesive stays
watch" example (that measured v1 and mislabelled it the fork); it is the worked
case of an **enhancement-fork accreting past its lean upstream**, and its
remediation is *split-then-fold-up* (Recommendation item 5). The fork rule's
*principle* stands (a genuinely cohesive fork would stay watch); lifecycle_metrics
just turned out to illustrate the flip side. \* `lifecycle.py`
is the honest borderline: at 39 defs / 1173 ln it is clearly below the split
tier on size (22% fewer defs and 34% fewer lines than `onboarding`), but as an
orchestrator it carries ~2 liftable clusters (skill-fan-out healing,
handoff-locking); it stays **watch** on the size gap with a documented trigger —
promote it if a third separable subsystem appears or the fan-out-healing cluster
grows. Either borderline call is **confirmed at per-file scoping**, not closed
here.

**Counting caveat (load-bearing):** the def figures are *top-level* symbols via
`grep -cE '^(def |class )'`. A non-anchored count that also catches indented
methods inflates each ~15–20% (e.g. `lifecycle.py` reads 47 non-anchored vs 39
anchored) — the two must never be mixed across rows, or the tier boundary
dissolves into an artifact of the regex.

### Also watched (not size-split candidates)

* **Test surface** — `bootstrap/tests/` is 14982 lines, **~2.7×** the 5464 lines
  of non-test engine code. *High but justified* for a security-critical
  install/upgrade engine; a redundancy pass is eventually worthwhile, not urgent.
* **Module count** — 26 module docs across 3 profiles; worth an orphan-inventory
  (any module never selected by a profile?), but no confirmed sprawl.

### What is genuinely clean (not debt)

* **Hygiene is excellent** — only **6** TODO/FIXME/HACK/deprecated marker lines
  in the entire repo.
* **No internal duplication** — no copy-paste/fork pattern *within* Cairn (forks
  are Cairn↔adopter, not internal).
* **Doctrine is well-distributed** — 12 files, the largest 449 lines
  (`lifecycle.md`), most in the 225–449 band (a few smaller); no monster
  doctrine document.
* `CHANGELOG.md` (1583 lines) is large but is normal accretion, not debt.

## Recommendation — a bounded program, gated on the first split

This is not a sprawling cleanup; it is **three over-grown Cairn tools, the
template bloat, and one adopter-fork (`lifecycle_metrics`)**, in order. Two
honesty caveats keep "bounded" from reading as "cheap":

* **Cost.** The scaffold-split arc established that splitting a monolith of this
  class is a high-operational-blast-radius refactor needing two Security Reviews
  and source-motion AST attestation. Each of (2)–(3) carries that *same*
  per-split cost — budget roughly one scaffold-split's worth of effort apiece,
  not a quick template reuse.
* **Gate.** Items (2)–(4) do **not** open until the scaffold-split *lands and
  proves the template affordable* in practice. If that first split runs over its
  risk/effort budget, the cost model above is falsified and the follow-ons must
  be re-justified from symptoms — not auto-triggered by this audit.

1. **Finish the scaffold-split** (in flight). Its hardened discipline — the
   launcher/facade topology, the `CAIRN_ROOT` contract, source-motion AST
   attestation, the recursive security scan, per-stage gates — becomes the
   **reusable template** for the next two *and* the live test of whether that
   template is affordable.
2. **Split `intent.py`** (highest follow-on value: second-largest *and* forked,
   so a clean split also unblocks the un-fork) using that template — *after* (1).
3. **Split `onboarding_activate.py`** (third monolith) — *after* (2).
4. **Thin the lifecycle templates** (independent, lower-risk). The `_template.md`
   files are ~85% teaching-doctrine — but this item is **not** "delete bloat."
   Routing that doctrine wholesale into `doctrine/lifecycle.md` (449 ln) would
   push it past 1000 lines, manufacturing the *monster doctrine document* this
   audit credits Cairn for not having. So it needs (a) a concrete destination
   that does not create a new monolith — route the *type-specific* teaching into
   two new pages, `doctrine/proposals.md` and `doctrine/plans.md` (parallel to
   the two templates), leaving the *shared* lifecycle concepts in the existing
   `doctrine/lifecycle.md`; final structure confirmed at scoping — and (b) a
   deliberate-vs-accreted split: some inline teaching is *intentional* (cf. the
   strategy `_template.md`, which places doctrine above each rule on purpose).
   Scope only the genuinely-redundant teaching; preserve the deliberate inline
   scaffolding.
5. **Split-then-fold-up `lifecycle_metrics` (independent of the gate).** Distinct
   from (1)–(4): the monolith here is **not in Cairn's tree** but in the
   **modflow_tools fork** (v2, 2035 ln / ~6 subsystems vs Cairn's lean 766-ln
   v1). Break the fork into a clean package, then **fold the split version up to
   Cairn** (replacing v1) — *one* refactor that **eliminates Fork 7a** *and*
   **upgrades Cairn's measurement layer**, with no monolith complexity
   transferred (the worry behind "don't bring that up to Cairn" is the monolith,
   which the split removes). The v2 logic is methodology-general
   (proposals/plans/review-yield/collisions/model-tiers), so it ports up cleanly
   — *scoping check*: split off any modflow_tools-specific bits to stay local.
   **Lower-ceremony** than (1)–(3) (a measurement tool — no install-engine /
   security surface) and **not gated** on the scaffold-split, so it can run
   anytime; arguably the cleanest early win. Authored as the Cairn-side payload
   (the split lands in the `~/Code/cairn` clone, pulled down to un-fork).

Each of (1)–(3) is a **Cairn-internal refactor** (the tools are Cairn's; not
distributed verbatim the way the installed scripts are checked — to confirm
per-tool at scoping), so the scaffold-split's risk profile and the
behavior-preserving + AST-attestation discipline carry over. (4) is a doctrine
re-home, not code. (5) is a **fold-up** (split authored in the Cairn clone,
pulled down to un-fork) — behavior-preserving + tests-green, but without the
install-engine blast radius of (1)–(3).

## Open questions for the maintainer

1. **Appetite + order.** Confirm the sequence above (intent.py before
   onboarding), or reprioritize? *(Recommended: as listed — intent.py is the
   biggest follow-on win and helps un-fork it.)*
2. **Template thinning scope.** Is (4) wanted now, or deferred until the three
   splits land? *(Recommended: defer — it is independent and lower-risk; do it
   after, or opportunistically.)*
3. **Test-redundancy pass.** Worth a dedicated look at the 14982-line test
   surface, or leave it as justified assurance? *(Recommended: leave for now;
   revisit if a split makes a test cluster obviously redundant.)*

## Fold-up note

This is an audit of Cairn's own tree; its remediations are **Cairn-internal**
(refactors of Cairn's engine/tools + a doctrine re-home), deliberated here and
implemented in the local `~/Code/cairn` clone (never pushed). The
`intent.py` / `onboarding_activate.py` scopings, when opened, follow the
scaffold-split pattern; none is a distribute-and-pull-down fold-up.
