<!-- cairn-internal-ref-allow: doctrine/dual-review.md doctrine/rationale.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
# Module: lifecycle-metrics

**Selected when:** default-on — kept by every adoption except the
smallest, where the proposal corpus is too thin to measure.
**Adds to:** a short note in `dev/agent_collaboration.md`
documenting the lifecycle-metrics discipline, **plus a runnable
extractor** the scaffold installs to `tools/lifecycle_metrics.py`
(see "Reference implementation" below).

The lifecycle-metrics layer makes the team's discipline
**measurable** rather than asserted. A small read-only extractor
walks `dev/proposals/` and `dev/plans/` and emits per-proposal
metrics — review rounds, revision counts, time-to-decision,
finding severities — so a claim like "External review catches what
the author cannot" becomes a quantity, not a belief.

## Template content

Merged into `dev/agent_collaboration.md`:

> **Lifecycle metrics.** The extractor `python tools/lifecycle_metrics.py` walks
> the proposal / plan corpus and emits per-proposal lifecycle
> metrics. Run it to read the team's own discipline; the output is
> derived and uncommitted.

The `python tools/lifecycle_metrics.py` token is filled from the adopter's
profile YAML with whatever invocation runs their extractor (e.g.
`python tools/lifecycle_metrics.py`).

The default metrics table is a **derived** artifact — regenerable
from the repository at any commit — and is therefore deliberately
not committed; when a project wants a dated, citable record it runs
`--snapshot`, which persists an indexed CSV under
`dev/measurement/snapshots/` (the snapshot layer described below).

A measured baseline is the gating artifact for any claim the
project makes about its own method — run the extractor before
asserting one.

## The Measurement Compact

Measuring a team's own collaboration is double-edged: the surface
that diagnoses where the apparatus drifts can become a ranking or
punishment instrument the moment it is read out of context. An
adoption that produces per-member or per-tier metrics takes on five
commitments — the **Measurement Compact** — constraining how those
measures are interpreted and published:

1. **Metrics serve system learning, not member punishment.**
   Per-member and per-tier surfaces exist to find where the
   *collaboration apparatus* drifts, not to rank contributors.
2. **No single composite score.** A composite hides the diagnostic
   value of per-dimension signals and invites ranking-style
   reading.
3. **No role- or tier-confounded metric is read as capability
   proof.** Per-tier and per-role surfaces are confounded by task
   assignment and escalation rules; reading them as capability
   comparison collapses the confounder structure.
4. **No cross-team generality from a single corpus.** One team is
   N=1 in the methodology-export sense; a cross-team claim needs
   independent teams, not a deeper read of one.
5. **Internal-diagnostic posture, not external-marketing posture.**
   The metrics are tools for the team's own feedback loops; any
   externally-published artifact derived from them is a separate,
   gated act.

**Two-tier enforcement.**

* **Tier 1 — gated.** Any *externally-published* artifact derived
  from per-member or per-tier surfaces requires an explicit
  Maintainer decision before publication (changelog entries, public
  docs, case studies, talks, papers).
* **Tier 2 — normative.** Internal-only reading of the surfaces is
  governed by the five commitments as guidance, not an enforced
  gate. Reading the snapshot at a goodnight is Tier 2 — no decision
  required, but the commitments still constrain interpretation.

The Compact is **dormant until** an adoption actually publishes
per-member / per-tier data; a small or solo team that never does
carries it at zero cost. It composes with the doctrine-evolution
gate (`doctrine/rationale.md` > "How the doctrine evolves under
evidence"): metrics diagnose, doctrine adapts under rate-limit.

### Doctrine and enforcement are separate

The five commitments are *doctrine*. Whether to back them with a
mechanical *enforcement gate* is a separate, optional choice. A
team may add a local **wording gate** — a test that scans
externally-facing files for the per-member / per-tier phrasing
Tier 1 prohibits and fails the build on a match. If it does:

* The gate's **banned-token list is a parameter the adopter
  supplies** — read from the team's profile configuration or a
  local ignore-list file — **never hardcoded into the template or
  the doctrine.** Baking specific contributor, model, or vendor
  identities into shipped framework text violates vendor-neutrality:
  it would freeze one team's roster into everyone's apparatus.
* A reader of this module should see *where their own list plugs
  in*, not inherit someone else's. The shape is "here is the slot;
  you fill it":

  > A wording gate reads its denylist from *your* banned-token
  > source — a profile key or a local ignore-list file — then scans
  > *your* externally-facing surfaces (changelog, public docs) for
  > those tokens. The token set is yours; the **mechanism** is what
  > Cairn describes.

One concrete implementation exists in the field — see the
case study — but it is *one* instance shaped by that project's own
file layout and roster, **not the canonical form.** Do not copy its
scanner phrases as if they were the gate's definition.

### Late-blocker reduction — measuring the review sweep

When an adoption runs a structured **review sweep** and a
**recommend-and-decide** second pass (`doctrine/dual-review.md`), the
question worth measuring is not first-round *volume* — a reviewer can
inflate that with low-value findings — but whether the sweep moves
findings *earlier*. The bundle:

* **Accepted / actionable first-pass findings** — that the first pass is
  doing real work, not padding.
* **Late P1 / P2 findings after the first pass** — the cost the sweep is
  meant to reduce; the headline number, watched *down*.
* **Review rounds by risk tier** — so a routine change and a
  contract-touching one are read against their own baselines, not pooled.
* **Recurrence of a missed category** — the same lens-coverage miss
  recurring is the signal to tighten that lens.

**Size the irreducible share prospectively.** The one experiment that
separates *lens-coverage* misses (reducible by the sweep) from genuine
*structural-independence* value (not reducible): run the strong sweep as
pass one, then *still* run an independent cross-type pass on a sample,
and count the residual **cross-type-only** findings the swept first pass
did not produce. That residual is the independence value, measured — the
honest check on whether the sweep captures what it hopes, and whether
recommend-and-decide trades away independence it should not.

**Home.** These records belong in the project's **`dev/measurement/`**
surface — the standard home for records the project keeps *for
measurement* (metrics, the collision log, signature logs), distinct from
historical reference — in a structured, parseable form rather than
decaying prose, so a metrics tool can aggregate them. Late-blocker
metrics live in that folder's **canonical structured metrics store**,
with dated CSV exports under its **`snapshots/`** subdirectory; the
store's filename and format are this module's tooling concern, while the
*home* and its membership rule are the `dev/measurement/` standard (see
that folder's `README.md`). This module *consumes* the standard folder as
the home and does not define it. All of it is **subject to the
Measurement Compact** above: system learning, no per-member read-out,
Tier-1 gating on any external publication.

## Reference implementation

**The scaffold installs a runnable extractor.** Enabling this module
writes `tools/lifecycle_metrics.py` into the target repo (copied
verbatim) and fills `python tools/lifecycle_metrics.py` to point at it. It is a
read-only, **standard-library-only** walker over
`dev/proposals/{,archive/}` and `dev/plans/{,archive/}` that emits a
per-proposal / per-plan CSV (or markdown) with review rounds, revision
counts, time-to-decision, and finding severities. Run it via:

> `python tools/lifecycle_metrics.py` &nbsp; (`proposals` by default; `plans` for the
> plan corpus; `--root` targets another tree; `--format md` for a
> human-readable table)

Nothing to clone or reimplement -- the default is a working tool. It
parses the proposal / plan lifecycle headers the Cairn scaffold installs,
so it runs cleanly against a freshly bootstrapped repo; project-specific
extensions to those headers may need small parser tweaks at the top of
the script.

**Scope of the shipped script.** The shipped extractor is the **v1
core** spine (the measurable lifecycle table) **plus the full
measurement layer** generalized from the reference implementation: a
longitudinal *snapshot layer* (indexed, dated CSV snapshots of the
unified proposal+plan schema under
`dev/measurement/snapshots/<YYYY-MM-DD>-<N>.csv`, carrying
`corpus_commit` / `snapshot_event` / `snapshot_timestamp_utc`
provenance, with same-day runs coalescing by index and a bounded
`--backfill-from`); a rolling-window collision-log correlation;
per-doctrine annotation counts; and per-role × per-tier model
aggregation. Every project-specific value — the model-tier vocabulary,
the annotation / collision-log locations, the snapshot directory, the
window tunables — is read from `dev/.cairn/metrics-config.json` (the
`dev/.cairn/` machine-config convention), falling back to vendor-neutral
built-in defaults when the file is absent, so the tool runs unconfigured
out of the box and the model-tier list stays an **open** `[substring,
label]` map — never a closed enum. The snapshot is the only write
surface — additive and regenerable. Producing or reading per-member or
per-tier surfaces stays bound by **the Measurement Compact** above.
