<!-- Migration ledger for the 2026-06-12 import of Cairn's own strategy docs
     from modflow_tools' dev/ (where Cairn was developed before self-hosting).
     Per BOOTSTRAP Act II-2a: a mechanical move erases provenance silently, so
     this ledger preserves old-path -> new-path + status for each migrated doc. -->

# Strategy-doc migration ledger — modflow_tools → Cairn (2026-06-12)

Cairn was developed as a project tracked in **modflow_tools'** `dev/`
lifecycle until it self-hosted on 2026-06-12. This ledger records the
import of Cairn's own **active** strategy docs into Cairn's `dev/strategy/`.

**Scope (Maintainer-directed):** *active* strategy docs only. Archived
strategy docs, and all proposals/plans, were **not** migrated — their
conclusions already live in Cairn's `doctrine/`, `dimensions/`,
`templates/`, and `docs/`. modflow_tools-science strategy docs (the
modflow-setup comparison, the FloPy/viz assessment, the `methods.md`
research, the LHM propagation ledger) were **excluded** — they are
modflow_tools' own science and must not enter the public Cairn repo.

## Migrated docs

| Old path (modflow_tools `dev/strategy/`) | New path (Cairn `dev/strategy/`) | Status | Notes |
|---|---|---|---|
| `2026-05-14-claude-human-ai-team-development-framework.md` | same | living | **The guide star** — Cairn's rationale/state/direction. Source for the P3 permanent vision/charter doc. |
| `2026-05-20-claude-team-productivity-metrics.md` | same | living | The Measurement-Compact research. **Vantage adaptation complete (2026-08-11)** — rewritten to Cairn's own tree, measures Cairn's own corpus, `claim-check-allow` directive dropped; modflow_tools now appears only as the named reference deployment. |
| `2026-05-27-claude-cairn-pre-release-sweep.md` | same | living | Version-independent release-strategy sweep. |
| `2026-05-27-codex-cairn-adopter-friction-audit.md` | → `archive/` (2026-06-12) | settled | Prospective-scientist adopter-friction lens. Superseded + archived by the v0.3 re-run `2026-06-12-claude-adopter-friction-audit.md` — itself merged into `2026-07-08-claude-broad-look-skeptical-review.md` and archived 2026-08-26. |
| `2026-06-04-claude-documentation-graphics.md` | → `archive/` (2026-08-10) | settled | Docs-graphics strategy (`docs/assets/`). Superseded + archived by the Cairn-vantage re-scope `2026-08-10-claude-documentation-enhancement.md`, which carries the portable production model forward and drops the modflow_tools figure inventory. |
| `2026-06-05-claude-cairn-complexity-debt-audit.md` | → `archive/` (2026-08-26) | settled | Complexity-debt audit. Program closed under the 2026-08 refocus with a named revival trigger; its measurement epistemics hoisted to guide-star Anchor 21. |

Each migrated file carries a `<!-- Migrated 2026-06-12 … -->` provenance
header. Original authorship dates and `Status:` fields are preserved.

## Open follow-up — vantage adaptation

These docs were authored from **modflow_tools' vantage**: they cite
modflow_tools' own tree (its user-guide, examples/freyberg, and theory
docs) as the worked example, and a few now-dangling refs to not-migrated
archived docs. Those cites are exempted by a **document-scoped
`claim-check-allow` directive** at the top of each affected doc — so the
exemption travels *with the doc* and `check_cairn.py` stays
upstream-clean (nothing to reconcile on a Cairn update). Only 4 of the 6
need one; `adopter-friction-audit` and `complexity-debt-audit` are
already clean. As each *living* doc is actively rewritten to Cairn's own
vantage, its directive shrinks or drops and the doc rejoins normal
claim-path checking. Track that here.

* **2026-08-10 — `documentation-graphics` left the live set.** Rather than
  being rewritten in place, it was superseded by a Cairn-vantage note and
  archived (row above). Its `claim-check-allow` directive travels with it
  into `archive/`. That leaves three of the original four *vantage*-directive
  docs live: `human-ai-team-development-framework`,
  `team-productivity-metrics`, and `pre-release-sweep`.
* **2026-08-11 — `team-productivity-metrics` completed vantage adaptation.**
  Rewritten to speak from Cairn's own tree: the headline corpus is now Cairn's
  49 proposals rather than an inherited reference-deployment baseline, the
  quoted Measurement Compact is the shipped generic wording rather than the
  superseded project-specific one, and the `claim-check-allow` directive is
  dropped (`claim_check` passes with none). modflow_tools remains named only
  where it is genuinely the subject — the layer's origin and the deployment
  roster. **Two of the original four vantage-directive docs remain**:
  `human-ai-team-development-framework` and `pre-release-sweep`.
  (`documentation-enhancement` also carries a directive, but it is a
  Cairn-authored note marking forward references to files it proposes
  creating — not a migration artifact, and outside this ledger's scope.)
* **2026-08-11 — `complexity-debt-audit` rejoined normal claim-path
  checking.** Its top-down rewrite drops every `claim-check-allow` directive:
  the Cairn-repo path and count exemptions it used to carry are gone, because
  the rewrite cites only locally-resolving paths and dates its snapshots
  instead of exempting counts. Verified by `claim_check.py` (OK, no flags) and
  `grep -c claim-check-allow` returning 0. It was already vantage-clean; it is
  now directive-free.

## Retroactive-review exemption

These docs predate Cairn's self-hosted lifecycle; they carry no Cairn
proposal behind them and are **exempt** from retroactive proposal/review.
They are imported as the historical deliberation record, not as new
substantive changes.
