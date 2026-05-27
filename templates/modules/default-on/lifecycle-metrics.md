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

> **Lifecycle metrics.** The extractor `{{metrics_command}}` walks
> the proposal / plan corpus and emits per-proposal lifecycle
> metrics. Run it to read the team's own discipline; the output is
> derived and uncommitted.

The `{{metrics_command}}` token is filled from the adopter's
profile YAML with whatever invocation runs their extractor (e.g.
`python tools/lifecycle_metrics.py`).

The emitted metrics file is a **derived** artifact — regenerable
from the repository at any commit — and is therefore deliberately
not committed; a dated, citable snapshot is a project's own later
choice.

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

## Reference implementation

**The scaffold installs a runnable extractor.** Enabling this module
writes `tools/lifecycle_metrics.py` into the target repo (copied
verbatim) and fills `{{metrics_command}}` to point at it. It is a
read-only, **standard-library-only** walker over
`dev/proposals/{,archive/}` and `dev/plans/{,archive/}` that emits a
per-proposal / per-plan CSV (or markdown) with review rounds, revision
counts, time-to-decision, and finding severities. Run it via:

> `{{metrics_command}}` &nbsp; (`proposals` by default; `plans` for the
> plan corpus; `--root` targets another tree; `--format md` for a
> human-readable table)

Nothing to clone or reimplement -- the default is a working tool. It
parses the proposal / plan lifecycle headers the Cairn scaffold installs,
so it runs cleanly against a freshly bootstrapped repo; project-specific
extensions to those headers may need small parser tweaks at the top of
the script.

**Scope of the shipped script.** This is the **v1 core** extractor (the
measurable spine the module promises). The reference implementation
it was generalized from also carries a *snapshot layer* — committed,
dated CSV snapshots; a collision-log correlation; per-doctrine
annotations; per-tier model aggregation — that is specific to that
project's own instrumentation and is **not** shipped here. An adoption
that wants committed snapshots can add them on top; the v1 core is what
makes the discipline measurable out of the box. Reading per-member or
per-tier surfaces stays bound by **the Measurement Compact** above.
