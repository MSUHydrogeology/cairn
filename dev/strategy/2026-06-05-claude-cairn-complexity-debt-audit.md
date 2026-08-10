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
     Method; the 2026-08-10 re-measure below is a separately dated snapshot. -->

# Cairn complexity-debt audit

**Author**: Claude (Strategy & Research Agent)
**Model**: Opus 4.8 (1M context); 2026-08-10 re-measure by Opus 5
**Date**: 2026-06-05
**Re-measured**: 2026-08-10 — **the original program is complete**; all five
recommendations landed and the gate was never tripped. A *second* ledger opens
below, because the debt did not disappear so much as move down one level.
**Status**: revised
**Type**: comparative-research
**Surfaces this would feed**: the original program's five items, all now
shipped (see *Program status*); a new `upgrade.py` split scoping; a
`lifecycle.py` promotion from watch-tier to split-tier (its documented trigger
has fired); a test-redundancy pass, which the original audit deferred and the
current ratio reopens.

---

## The question

**2026-06-05.** While splitting `bootstrap/scaffold.py`, is Cairn carrying
*other* accumulated complexity debt worth addressing — and if so, where, and is
it a bounded program or a sprawling cleanup?

**The finding: the debt is concentrated, not pervasive.** It is a handful of
over-grown monolithic `.py` tools plus lifecycle-template bloat; everything else
is clean. That makes remediation a **bounded, sequenceable** program — finite
and orderable, though each split is a heavy refactor and the program is *gated*
on the first one proving out — not an open-ended audit-and-fix.

**2026-08-10.** Two months and a large security-hardening arc later, the
re-measure asks the follow-on question the original could not: *did the bounded
program stay bounded, and did the criterion hold up?*

**The answer to both is yes, and it is worth stating plainly because the
project's own record has been underselling it** (the 2026-07-08 broad look
flagged exactly this — "the strategy record still presents the completed
complexity-debt cleanup as pending"). All five recommendations shipped. The
cost model was not falsified, so the gate on items 2–4 never had to bite. Most
strikingly, the *criterion* predicted the seams: the subsystems this audit
named by symbol-name clustering are, almost verbatim, the module names the
splits actually landed on.

**But the debt did not vanish — it descended.** Three members of the packages
the splits produced are now individually larger than the monoliths this audit
convicted, and the largest is `bootstrap/_scaffold/upgrade.py` at 2,353 lines,
which the broad look independently flagged as *"outside the debt ledger."* That
is this note's job to fix: the second ledger below puts it inside.

## Method (so the findings are falsifiable)

Read-only scan of `~/Code/cairn`, re-runnable. The 2026-06-05 pass and the
2026-08-10 re-measure use the **same commands**, so the two snapshots are
comparable:

* Composition + largest files: `git ls-files '*.py' | xargs wc -l | sort -rn`.
* Monolith signal: `grep -cE '^(def |class )' <file>` (top-level symbols per file)
  + sampling the symbol names for responsibility spread.
* Test-to-code ratio: `bootstrap/tests` vs `bootstrap` non-test line sums.
* Hygiene: `grep -rInE 'TODO|FIXME|HACK|XXX|DEPRECAT'`.
* Duplication: `git ls-files '*.py' | sed 's#.*/##' | sort | uniq -d`.
* Template bloat: heading + `cairn:slot` counts in the `_template.md` files.
* Fork measurement (2026-06-05 only, the one non-`~/Code/cairn` probe): the
  modflow_tools **v2 keep-ours fork** of `lifecycle_metrics.py` at
  **2035 ln / 49 defs**.

**Added at the re-measure**, because two of the new findings could not be
established by counting alone:

* **Twin parity**, checked rather than assumed: `cmp` over six representative
  shipped↔self-hosted pairs, *and* a read of the test that enforces it
  (`bootstrap/tests/test_notice_install.py`) to see whether its target list is
  hand-maintained or derived.
* **Subsystem reads** for the two files the size screen newly flags
  (`bootstrap/_scaffold/upgrade.py`, `tools/lifecycle.py`), since this audit's
  own criterion says size screens but only responsibility spread convicts.

**What would falsify the second ledger:** if a subsystem read of `upgrade.py`
showed one cohesive pipeline rather than separable clusters, its row drops to
*watch* regardless of its 2,353 lines — exactly as `lifecycle_metrics` v1's
766 lines were screened out in 2026-06-05 for being a single linear ETL.

## Program status — the 2026-06-05 ledger, closed

Measured 2026-08-10. Every "before" figure is this note's original snapshot.

| # | Item | Before | After | Status |
|---|---|---|---|---|
| 1 | `bootstrap/scaffold.py` | 4,865 ln | **143 ln / 5 defs** launcher + `bootstrap/_scaffold/` (10 modules, 8,651 ln) | **shipped** |
| 2 | `intent.py` | 2,021 ln / 59 defs | **139 ln / 3 defs** facade + `_intent/` (7 modules) | **shipped** |
| 3 | `onboarding_activate.py` | 1,767 ln / 50 defs | **88 ln / 1 def** facade + `_onboarding/` (8 modules) | **shipped** |
| 4 | Lifecycle templates | 776 + 821 ln | **417 ln** (24 headings, 4 slots) + **327 ln** (18 headings, 3 slots) | **shipped**, with a relocation caveat below |
| 5 | `lifecycle_metrics` split-then-fold-up | 766 ln / 29 defs (v1); 2,035 ln / 49 defs (fork) | **69 ln / 1 def** facade + `_lifecycle_metrics/` (9 modules, 2,020 ln) | **shipped** |

**The criterion predicted the seams.** This is the result most worth keeping,
because it is what makes the method reusable rather than a one-off:

* For `intent.py` the audit named five separable subsystems — *record I/O ·
  identity/session · conflict-check · CLI · git-hook install*. The realized
  package is `record_io.py`, `identity.py`, `conflict.py`, `cli.py`,
  `hooks.py`, plus `shared.py`.
* For `onboarding_activate.py` it named three — *slot/preset parse ·
  trigger-eval · prompt render*. The realized package is `slotparse.py`,
  `triggers.py`, `prompts.py`, plus `activation.py`, `cli.py`, `security.py`,
  `shared.py`.

A symbol-name clustering pass, done read-only in an afternoon, anticipated the
module boundaries of two heavy refactors. That is evidence for the
**separable-subsystems** criterion over the line-count screen, and it is the
part of this audit worth folding up.

**The gate held.** Items (2)–(4) were gated on the scaffold-split landing *and
proving the template affordable*. It did, and the launcher/facade topology it
established was reused three more times. The cost model was never falsified, so
the follow-ons never had to be re-justified from symptoms.

**Item 4's relocation caveat.** The thinning met its stated goal — the
templates lost 46% and 60% of their lines and are now form-shaped (4 and 3
slots) rather than teaching-shaped. It also honoured the audit's specific
warning: rather than dumping the teaching into `doctrine/lifecycle.md` and
"manufacturing the monster doctrine document this audit credits Cairn for not
having," the work created the two destination pages the audit specified,
`doctrine/proposals.md` and `doctrine/plans.md`. But the mass moved rather than
shrank, and the doctrine corpus no longer sits in the band this audit praised:
`doctrine/plans.md` is now **836 lines**, the largest file in the corpus, where
2026-06-05's largest was 449. Below the 1,000-line threshold the audit feared,
but well outside the 225–449 band it called well-distributed. The 2026-07-08
broad look independently found ~900 words of lifecycle rules **duplicated**
between `proposals.md` and `plans.md`, against Cairn's own one-home rule —
which is the likeliest source of the excess.

## The criterion — a size screen, a symptom convicts

*(Unchanged from 2026-06-05, and validated by the outcome above.)*

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
* **Trust-boundary concentration** — `scaffold.py` was the install/upgrade trust
  boundary no single reviewer holds at once. **`upgrade.py` has inherited that
  property**, which is why its row below is the priority one.

**Counting caveat (load-bearing, and it still binds):** the def figures are
*top-level* symbols via `grep -cE '^(def |class )'`. A non-anchored count that
also catches indented methods inflates each ~15–20% — the two must never be
mixed across rows, or the tier boundary dissolves into an artifact of the regex.

## The second ledger (2026-08-10) — where the debt went

### N1 — The split relocated three monoliths rather than eliminating them

`bootstrap/_scaffold/` is a genuine package with a narrow launcher, but three of
its members are individually at or above the size that convicted the originals:

| File | Lines | defs | Separable subsystems | Verdict |
|---|---|---|---|---|
| `bootstrap/_scaffold/upgrade.py` | 2,353 | 38 | **≥6** — root/profile resolution · upgrade computation (`FilePlan`, `_compute_upgrade`) · reporting · staging · lockfile init/finalize · module + collision adoption (four distinct `_cmd_*` entry points) · apply | **split** |
| `bootstrap/_scaffold/install.py` | 1,848 | 34 | not yet read | **screen — read before convicting** |
| `bootstrap/_scaffold/config.py` | 1,769 | 20 | not yet read | **screen — read before convicting** |

`upgrade.py` is **larger than `intent.py` was when this audit convicted it**
(2,021 ln), carries the same multi-`_cmd_*` CLI cluster that formed one of
`intent.py`'s five seams, and sits on the install/upgrade trust boundary. The
broad look reached the same file by a different route, recording *"upgrade.py
mega-functions outside the debt ledger."* This note's second ledger is where it
now lives.

The two rows marked *screen* are stated honestly as unconvicted: they clear the
size screen but this pass did not do the symbol-clustering read, and under this
audit's own criterion size alone does not convict.

### N2 — The `lifecycle.py` watch-tier trigger has fired

2026-06-05 kept `tools/lifecycle.py` at **watch** on the size gap, with a
documented promotion trigger: *"promote it if a third separable subsystem
appears or the fan-out-healing cluster grows."*

Both conditions are met. It has grown from **1,173 ln / 39 defs to 1,412 ln /
46 defs**, and the fan-out-healing cluster — the specific thing the trigger
named — is now six functions (`_skill_symlinks_available`,
`_assert_fanout_contained`, `_seed_skill_gitignore`, `_heal_skill_symlink`,
`_heal_skill_copy`, `_heal_skills_fanout`). A symbol read shows at least five
separable subsystems: interpreter / trust-root resolution
(`_probe_interpreter`, `_resolve_interpreter`) · skills fan-out healing ·
handoff locking (`HandoffLock`, `_pid_alive`, `_designation_marker_present`) ·
session-start reporting · session-end orchestration with three subprocess
runners.

**This is the audit's own trigger firing on schedule, which is the mechanism
working.** `lifecycle.py` moves from watch to split-tier. It also carries the
**local interpreter binding** — an executable trust root named in `AGENTS.md`'s
high-risk surfaces — so a split here takes a Security Review, and it is a
*twin* (below), so both copies move together.

### N3 — New standalone monoliths outside the original ledger

None existed at 2026-06-05; all are products of the security arc.

| File | Lines | defs | Note |
|---|---|---|---|
| `run_portable_security_sweeps.py` | 1,858 | 49 | executable trust root (`AGENTS.md`); shipped/self-hosted twin |
| `tools/lifecycle_planner.py` | 1,728 | 50 | twin |
| `templates/modules/team-gated/run_security_audit.py` | 1,327 | 41 | — |

These are screened, not convicted. Two carry security trust-root status, which
raises the cost of splitting them *and* the cost of not splitting them; that
tension is the open question below.

### N4 — The test ratio has roughly doubled, and the deferral should be revisited

2026-06-05: `bootstrap/tests/` at 14,982 lines against 5,464 lines of non-test
engine code — **~2.7×**, judged *"high but justified"* for a security-critical
install/upgrade engine, with a redundancy pass *"eventually worthwhile, not
urgent."*

2026-08-10: **54,421 vs 10,361 lines — ~5.25×.** The engine did not quite
double (1.9×); the test surface grew 3.6×. The largest single Python file in the
repository is now a test (`bootstrap/tests/test_portable_security_sweeps.py`,
2,356 ln), and four more test files exceed 1,500 lines.

This does not convict the test surface — an install engine that writes into
other people's repositories earns heavy assurance, and much of the growth is the
security arc's perturbation and confidentiality suites, which are the expensive
kind precisely because they are non-vacuous. But *"eventually worthwhile, not
urgent"* was a judgement made at 2.7×. At 5.25× it is worth re-deciding rather
than inheriting, and Cairn already ships the instrument
(`scripts/quality_gate.py --sub redundancy`).

### N5 — "No internal duplication" has inverted in form, but the substance is answered

The audit's duplication probe returned nothing in June; it now returns ~38
duplicate basenames. **The metric has become uninformative rather than the
property having decayed**, and the distinction matters:

* **Intra-package name reuse** — `cli.py`, `config.py`, `shared.py` in three
  different private packages. Normal, correct, and a direct consequence of the
  splits this audit recommended.
* **Deliberate shipped↔self-hosted twins** — Cairn self-hosts the tools it
  ships. Six representative pairs were `cmp`-checked this pass:
  `run_portable_security_sweeps.py`, `lifecycle.py`, `lifecycle_planner.py`,
  `claim_check.py`, `link_check.py`, `content_scan.py`. **All six byte-identical.**

The broad look's concern here — *"nothing automated keeps the 13
shipped/installed payload copies from diverging"* — is **better answered than
that wording suggests**, and the reason is worth recording. The parity test
(`test_every_self_hosted_twin_stays_byte_identical_to_its_source`) does not
iterate a hand-written list: it derives its pairs from
`install_manifest(modules=None)` — *the installer's own manifest*. That is
precisely the lesson the broad look named as a fold-up candidate ("any
scanner's target list should be generated from the same list the installer
uses"), already implemented here. A twin added to the manifest is covered
without anyone remembering to add it.

*Limit of this finding:* the parity test covers `scripts/` and `tools/` twins
of manifest `.py` sources. Non-`.py` payload copies and any shipped file
outside the manifest are not in its scope, so "13 copies" is not fully
discharged by this one test — narrowed, not closed.

### N6 — Hygiene has degraded from excellent to merely good

**6 → 34** `TODO|FIXME|HACK|XXX|DEPRECAT` marker lines across tracked files
(22 in `.md`, 12 in `.py`). Still low for a repository of this size, and the
`.md` share is largely doctrine *discussing* deprecation rather than deferred
work. But a ~6× rise means the 2026-06-05 characterization ("hygiene is
excellent — only 6 marker lines in the entire repo") should not be quoted
forward without this re-measure.

### N7 — Ambient growth, no action implied

Module docs **26 → 31** (the orphan-inventory suggestion from 2026-06-05 is
still un-run and still worth an hour). `CHANGELOG.md` **1,583 → 2,400** lines —
normal accretion, not debt, as before. Doctrine **12 → 16 files**, 5,547 lines
total.

## Recommendation — a second bounded program, same shape, gated the same way

The 2026-06-05 program's structure is the right one to reuse, because it
worked: order by value, gate the follow-ons on the first one proving the cost
model, and let the criterion — not the line count — decide what is on the list.

1. **Split `bootstrap/_scaffold/upgrade.py`** (the headline; ≥6 subsystems,
   larger than the largest file this audit originally convicted, on the
   install/upgrade trust boundary). It reuses the topology the scaffold-split
   established, and it is the row the broad look independently asked for.
   Carries the scaffold-split's full ceremony: Security Review and source-motion
   AST attestation.
2. **Promote `tools/lifecycle.py` to split-tier and scope it** — its documented
   watch trigger has fired. Both twins move together; the interpreter-binding
   trust root puts a Security Review on it.
3. **Read `install.py` and `config.py` before deciding.** A subsystem read is
   cheap; a split is not. Either they convict and join the queue, or they are
   recorded as screened-and-cleared so the next re-measure does not re-litigate
   them.
4. **Re-decide the test-redundancy pass at 5.25×** rather than inheriting a
   deferral made at 2.7×. Bounded: run `--sub redundancy`, read the output,
   decide. This is an hour, not a program.
5. **Resolve the `doctrine/plans.md` overshoot** — 836 lines, corpus-largest,
   with ~900 words duplicated against `proposals.md`. This is a doctrine
   re-home, not code, and the duplication is the likeliest cause; it should be
   fixed as a one-home violation rather than as a size target.

**The same two honesty caveats bind.** *Cost:* each of (1)–(2) is a
high-blast-radius refactor with two Security Reviews and AST attestation —
budget one scaffold-split apiece. *Gate:* (2) does not open until (1) lands and
re-proves the template on a file that is itself a package member, which is a
structurally different case from splitting a top-level monolith and may cost
more. If (1) runs over budget, (2)–(3) are re-justified from symptoms, not
auto-triggered by this note.

**One thing this program should not do.** It should not treat the second
ledger as evidence that the first program failed. Four of the five 2026-06-05
items removed real responsibility spread, and the fifth eliminated an adopter
fork. Package members growing after a split is the ordinary consequence of
continued feature work landing in the right module — which is what a good split
buys. The lesson is that a split is not terminal, and a debt ledger needs a
**re-measure cadence**, which is the fold-up candidate below.

## Open questions for the maintainer

1. **Appetite + order.** Confirm `upgrade.py` first, then `lifecycle.py`?
   *(Recommended: as listed — `upgrade.py` is both the largest and the one an
   independent review already named.)*
2. **The security-tool monoliths (N3).** `run_portable_security_sweeps.py` and
   `lifecycle_planner.py` clear the size screen, but two are executable trust
   roots where churn itself is a risk. Screen-and-hold, or scope a subsystem
   read? *(Recommended: hold. A trust root's stability has value the line count
   does not see; revisit only if a third subsystem appears, the same trigger
   discipline that just worked for `lifecycle.py`.)*
3. **Test redundancy at 5.25×.** Run the pass now, or hold until a split makes
   a cluster obviously redundant? *(Recommended: run the instrument and read
   the output now — it is cheap — but do not commit to acting on it.)*
4. **Re-measure cadence.** Should this note carry a standing re-measure trigger
   (a release boundary, or a fixed interval) rather than being re-run
   opportunistically? *(Recommended: yes — at each release cut, alongside the
   pre-release sweep, which already exists as the natural host.)*

## Fold-up note

The remediations remain **Cairn-internal** — refactors of Cairn's own engine
and tools plus a doctrine re-home. Two findings from the re-measure are
**methodology-general** and are fold-up candidates, each needing its own
proposal under the one-incident-is-not-doctrine rate-limit gate:

* **The separable-subsystems criterion is predictive, not just descriptive.**
  A read-only symbol-clustering pass named the module boundaries that two
  heavy refactors later landed on. That is a cheap, transferable technique for
  deciding *whether and where* to split — and it is stronger than the
  line-count screens most complexity guidance offers, because it produces the
  seam, not just the verdict.
* **A debt ledger needs a re-measure cadence, or it silently inverts.** This
  note sat for two months reading as "pending" while its program had in fact
  completed, and simultaneously stopped covering the largest file in the
  engine. Both failures have the same cause: a point-in-time audit with no
  scheduled re-run. The generalizable rule is that a complexity ledger is a
  *living* instrument tied to a release boundary, not a one-shot report — which
  also argues this note's own `Type:` should eventually become
  `living-reference`.
