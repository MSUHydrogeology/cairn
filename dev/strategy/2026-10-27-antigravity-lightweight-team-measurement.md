# Lightweight team measurement — watching tokens, model tiers, and reviews without adding machinery

**Author**: Antigravity (Strategy)
**Model**: Gemini 3.1 Pro
**Date**: 2026-10-27
**Status**: settled
**Type**: product-strategy
**Surfaces this would feed**: [`tools/gauge.py`](../../tools/gauge.py); [`scripts/token_budget.py`](../../scripts/token_budget.py); [`tools/audit_report.py`](../../tools/audit_report.py); [`dev/proposals/_template.md`](../proposals/_template.md); [`dev/plans/_template.md`](../plans/_template.md); [`dev/measurement/README.md`](../measurement/README.md)

## Conclusion first

**A Maintainer overseeing a team of AI agents needs four numbers at a glance: how many tokens deliberation is burning, whether agents are using overly heavy models, whether changes are accumulating excessive review passes, and whether product work outpaces process prose.**

Earlier Cairn measurement (`lifecycle_metrics.py`) became heavy because it maintained separate metrics stores, required manual incident-table updates at `goodnight`, and scraped prose with brittle regexes. When the August 2026 subtraction sweep (`dev/plans/archive/subtraction-sweep.md`) retired that engine, four small, zero-token stdlib scripts survived (`scripts/token_budget.py`, `tools/gauge.py`, `tools/audit_report.py`, and `tools/evolution_infer.py`), **but none of them measures artifact token volume, model-tier intensity, or review pass counts.**

We can measure all four with **zero new workflow steps for agents and no separate metrics store**: every needed fact is already recorded structurally in file byte sizes, `git log --numstat`, and the standard `**Author**:`, `**Model**:`, and `## Review --` lines. In addition, measuring the October 2026 (`0.5-dev`) artifacts in **words and bytes rather than lines** uncovered why the October 26 "Keep it short" template update (`3ba6aba1`) did not reduce token cost — and points to a fast, zero-frozen-test fix for `0.5`.

---

## The question / felt gap

Managing a multi-agent team without gauges leaves the Maintainer flying blind until a context window overflows or a simple change takes six review passes. Conversely, adding heavy measurement machinery (new ledgers, per-transition emitters, or blocking linters) slows the team down and turns the measurement target into a game.

We need to answer two questions:
1. **Where is Cairn on measurement today, and what does the current `0.5-dev` data show when measured honestly?**
2. **What is the lightest possible way to measure token spend, model-tier intensity, and review volume — and to make "Keep it short" actually work for `0.5`?**

---

## Method

I audited the existing measurement tools and records at commit `5e52e207` on `2026-10-27` under Python 3.13.13:
* Read [`dev/measurement/README.md`](../measurement/README.md), [`dev/strategy/archive/2026-05-20-claude-team-productivity-metrics.md`](archive/2026-05-20-claude-team-productivity-metrics.md), [`dev/strategy/2026-08-21-claude-nimbleness-recovery.md`](2026-08-21-claude-nimbleness-recovery.md), [`scripts/token_budget.py`](../../scripts/token_budget.py), [`scripts/measurements.py`](../../scripts/measurements.py), [`tools/gauge.py`](../../tools/gauge.py), [`tools/audit_report.py`](../../tools/audit_report.py), and [`tools/evolution_infer.py`](../../tools/evolution_infer.py).
* Ran `scripts/token_budget.py`, `tools/gauge.py --since 2026-08-25`, and `tools/audit_report.py --sample 5` against the live repository.
* Measured byte sizes, estimated token counts (`bytes / 4`), word counts, line counts, section breakdowns (`## ` headings), review pass counts, and `**Model**:` declarations across all **22 proposals** and **18 main plans** from the October 2026 (`0.5-dev`) cycle (`2026-10-17` to `2026-10-27`).
* Checked [`dev/plans/archive/2026-10-26-review-keep-it-short-templates.md`](../plans/archive/2026-10-26-review-keep-it-short-templates.md) to verify which frozen tests in `bootstrap/tests/` read `## Keep the proposal short` and `## Keep the plan short`.

---

## Findings

### 1. What Cairn's four existing measurement tools do — and what they miss

| Tool | Size | What it measures today (measured `2026-10-27`) | What it misses |
|---|---:|---|---|
| [`scripts/token_budget.py`](../../scripts/token_budget.py) | 123 lines | Always-on prompt prefix (`CLAUDE.md` + `AGENTS.md` = **9,815 est. tokens / 39,409 B**). | Ignores the **deliberation load** (`dev/agent_collaboration.md` + `_template.md` = **+15,400 est. tokens / 61,600 B**) and ignores the **token size of proposals, plans, and reviews**. |
| [`tools/gauge.py`](../../tools/gauge.py) | 169 lines | Weekly `git log --numstat` lines added across `dev`, `security-machinery`, `other-machinery`, and `product`. | Counts **lines** (which unwrapped paragraphs game), misfiles `bootstrap/_scaffold/` (Cairn's installer product) under `other-machinery` (making Oct 2026 `product` share read `2%–14%`), and leaves `.zenodo.json` unclassified. |
| [`tools/audit_report.py`](../../tools/audit_report.py) | 142 lines | Checks `dev/plans/archive/*.md` for a minimum floor (`reviews > 0`, verification present, test counts present). | Checks only for **too little** review, never **excessive** reviews (`> 2` passes), oversize artifacts, or **model-tier usage**; and flags 4 of 5 sampled files because separate `*.code-review.md` side-files lack plan headers. |
| [`tools/evolution_infer.py`](../../tools/evolution_infer.py) | 407 lines | Evaluates rolling-window recurrence (`>= 2` `Impact = occurred` rows) across tables in `dev/measurement/*.md`. | Depends on manual Markdown table migration during `goodnight`; meanwhile `dev/measurement/` holds 8 historical files from July–August that are no longer live gauges. |

### 2. The unwrapped-line Goodhart effect on `0.5-dev` (why "Keep it short" didn't cut tokens)

Measuring the October 2026 (`0.5-dev`) proposals and plans by **bytes and words** alongside **lines** exposes a striking divergence:

| Cohort (`0.5-dev`, Oct 2026) | Count | Median lines | Median bytes | Median est. tokens (`B / 4`) | Total cohort tokens (`B / 4`) |
|---|---:|---:|---:|---:|---:|
| All Oct 2026 proposals (`2026-10-17` to `10-27`) | 22 | 883 lines | 75,086 B | ~18,771 tok | ~525,964 tok |
| All Oct 2026 main plans (`2026-10-17` to `10-27`) | 18 | 534 lines | 78,812 B | ~19,703 tok | ~496,020 tok |
| **Post-"Keep it short" proposals (`Oct 26–27`)** | **12** | **681 lines** | **75,086 B** | **~18,771 tok** | **~248,400 tok** |
| **Post-"Keep it short" plans (`Oct 26–27`)** | **8** | **364 lines** | **72,176 B** | **~18,044 tok** | **~149,600 tok** |

* **Why line counts fell by 32% while token counts barely moved (-8%):** When line count was treated as the size target (e.g., "plans ≤ 350 lines"), agents stopped wrapping lines at 80 columns and wrote single 400–1,000-character lines. For example:
  * [`dev/plans/archive/repin-ceremony-hardening.md`](../plans/archive/repin-ceremony-hardening.md) is **315 lines**, which looks compact — but it is **71,901 bytes (10,561 words / ~17,975 tokens)**, averaging **228 characters per line**.
  * [`dev/plans/archive/upgrade-edit-check-no-repository-programs.md`](../plans/archive/upgrade-edit-check-no-repository-programs.md) is **297 lines** — and **72,926 bytes (10,341 words / ~18,231 tokens)**, averaging **245 characters per line**.
  * [`dev/plans/repin-build.md`](../plans/repin-build.md) is **534 lines** — and **110,895 bytes (16,583 words / ~27,724 tokens)**.
* **Where the tokens inside a 72 KB (~18,000-token) plan actually go:** A section-by-section breakdown of those three plans shows two culprits:
  1. **`## Acceptance criteria` alone is 13.7 KB to 27.4 KB (2,000 to 3,859 words)** — because plan-review and security-review findings are folded in by bolting more specification clauses onto each chunk paragraph.
  2. **Appended reviews, responses, and verification blocks take 42 KB to 70 KB (6,500 to 10,800 words)** — single review passes run 1,200 to 4,326 words (`8 KB–27.7 KB`) each.
* **The multiplier cost:** Because every subsequent agent in the lifecycle (author, plan reviewer, security reviewer, implementer, code reviewer) reads the accumulated proposal and plan, one 75 KB proposal + 72 KB plan costs **~200,000 to 350,000 input tokens** across a single feature's lifecycle.

### 3. Model-tier intensity and review pass counts on `0.5-dev`

* **Model-tier shift (`Opus` vs. `Sonnet` / `Flash`):**
  * **Oct 17–19 (10 proposals):** 8 of 10 proposals had their `usual` / `Internal` or `External` review run on `Claude Opus 5.5` (highest tier), in addition to `Security Review` on `Opus 5.5`.
  * **Oct 26–27 (after `model-tier-rules` landed):** 11 of 12 proposals and all 8 plans ran their `usual` / `Internal` review, implementation, and code review on medium-tier models (`Claude Sonnet 5.5` or `Gemini 3 Flash`), reserving `Opus 5.5` for `Security Review` and Strategy authoring. The rule worked immediately once stated, **but no tool reports the tier mix**, so regressions are invisible unless someone greps the headers.
* **Review pass volume:**
  * **Standard (`usual`) changes:** Now average **1.2 proposal review passes** (`1` pass on 10 of 12 Oct 26–27 proposals; `2` passes only when scope widened), and 1-commit bounded changes (`writing-for-the-reader`, `review-keep-it-short-templates`) skipped the plan entirely.
  * **High-assurance (`usual + Security Review`) changes:** Still accumulate **5 to 6 review passes** across proposal + plan (`2` proposal reviews + `2` plan reviews + `1–2` code reviews), plus `3–4` author response and verification sections per file.

---

## Why "Keep it short" (`3ba6aba1`) needs a 1-bullet fix for `0.5` — and why it is easy

On `2026-10-26`, commit `3ba6aba1` added `## Keep the proposal short` and `## Keep the plan short` to the four template files (`dev/proposals/_template.md`, `templates/core/dev/proposals/_template.md`, `dev/plans/_template.md`, `templates/core/dev/plans/_template.md`).

**Why it didn't curb the 72 KB files:**
1. It says *"Keep what goes in it small"* and *"Scripts and task briefs stay out"*, but gives **no word or byte target** for the opening body, for `## Acceptance criteria`, or for an appended `## Review` / `## Response` pass.
2. It encourages `grep -n '^## ' <plan>` ("Read by section"), which helps readers skip sections, **but agents still write 2,000-word `Acceptance criteria` cells and 1,800-word review passes** on unwrapped lines.

**Why fixing it right now is cheap (no frozen test touched):**
* As verified in [`dev/plans/archive/2026-10-26-review-keep-it-short-templates.md`](../plans/archive/2026-10-26-review-keep-it-short-templates.md#falsification-ledger) (lines 139–146), **no frozen test in `bootstrap/tests/` pins the wording of `## Keep the proposal short` or `## Keep the plan short`** (`test_board_json_contract.py` only requires that the section sit above the `---` rule and hold no `---` line).
* Adding one explicit **word-budget bullet** to `## Keep the proposal short` and `## Keep the plan short` in the four `_template.md` files (and finalizing the two lockfile hashes in `dev/.cairn/cairn-lock.yml`) requires **zero frozen-test edits** and **zero gate-manifest re-anchors**:
  > * **Count words, not lines — never unwrap lines to look short.** Aim for **≤ 1,000 words (~6 KB)** for an opening proposal or plan body, **≤ 150 words per chunk** in `Acceptance criteria` (state what must hold, not how to code it), and **≤ 600 words (~4 KB)** per review pass or response.

---

## Options for Lightweight Team Measurement

| Option | How it works | Pros | Cons |
|---|---|---|---|
| **Option A: Do nothing** | Keep `token_budget.py`, `gauge.py`, and `audit_report.py` as they are. | Zero code changes. | Line-count Goodharting continues; `gauge.py` misreports Cairn's product share (`3%`); no visibility into artifact token sizes, review pass counts, or model-tier usage. |
| **Option B: Reintroduce a lifecycle metrics store** | Emit JSONL rows at each commit/transition into `dev/measurement/` and maintain CSV snapshots. | Historical time-series store. | Recreates the exact machinery debt retired in August 2026 (merge conflicts, dirty trees, schema drift). Violates the nimbleness principle. |
| **Option C (Recommended): Zero-machinery "Team Pulse" inside existing read-only tools** | Compute artifact tokens/words, review pass counts, and model-tier mix on demand directly from git and existing file headers in `tools/gauge.py` (or `scripts/token_budget.py` + `tools/audit_report.py`). | **Zero new files, zero agent workflow steps, zero prose-scraping fragility**; catches token bloat, model-tier drift, and excessive reviews in one command. | Requires ~60–80 lines of stdlib Python across existing non-frozen scripts in `tools/` / `scripts/`. |

---

## Recommendation: A Four-Part Lightweight Upgrade

### 1. Immediate `0.5` fix: Add the word-budget bullet to `## Keep the proposal/plan short`
* Edit the `## Keep the proposal short` and `## Keep the plan short` sections in `dev/proposals/_template.md`, `templates/core/dev/proposals/_template.md`, `dev/plans/_template.md`, and `templates/core/dev/plans/_template.md` to state explicit word/byte budgets (opening body **≤ 1,000 words / ~6 KB**; `Acceptance criteria` **≤ 150 words/chunk**; review pass **≤ 600 words / ~4 KB**) and ban line-unwrapping to game line counts.
* Update the two line-count targets in [`dev/strategy/2026-08-21-claude-nimbleness-recovery.md`](2026-08-21-claude-nimbleness-recovery.md#how-to-judge-whether-cairn-is-staying-nimble) (line 97) to state **words / KB alongside lines** so the strategy note itself does not incentivize unwrapped lines.

### 2. Upgrade `tools/gauge.py` to report bytes/tokens, fix `product` bucketing, and print a `--pulse` summary
Keep `tools/gauge.py` as the single on-demand command the Maintainer runs to check team health:
* **Fix Cairn's path classification:** Classify `bootstrap/_scaffold/`, `bootstrap/scaffold.py`, and `.zenodo.json` as `product` (since the scaffold installer/upgrader *is* Cairn's shipped software product), so `product share` reflects shipped adopter value vs. `dev/` and test machinery.
* **Report KB / estimated tokens alongside lines:** `git log --numstat` measures lines; adding byte/word counts for touched files stops unwrapped lines from hiding volume.
* **Add a `--pulse` (or default bottom block) summary over `--since <date>`:** Scanning `dev/proposals/` and `dev/plans/` files touched since `--since`, print four lines:
  1. **Artifact size (words & est. tokens):** median and max opening body vs. appended reviews (flagging any proposal/plan over `4,000` words / `~25 KB`).
  2. **Review passes per artifact:** median and max `## Review` / `## Plan review` / `## Code review` / `## Security review` headings per file (flagging any artifact with `> 2` passes).
  3. **Model-tier mix:** count of `high` (Opus / Pro), `medium` (Sonnet / Flash), `low` (Haiku / Flash-Lite), and `unspecified` across `**Author**:`, `**Model**:`, and `## ... review --` headers.
  4. **Always-on + deliberation prompt tax:** current token count of `AGENTS.md` + wrapper (`token_budget.py`) plus `dev/agent_collaboration.md` + `_template.md`.

### 3. Fix `tools/audit_report.py` on side-files and oversize/over-reviewed plans
* Skip `*.code-review.md` and `*.second-look.md` side-files when enumerating plans in `dev/plans/archive/` (or attach their counts to the parent plan stem) so `audit_report.py` stops emitting false-positive "no review section / no risk answer" warnings on standalone review files.
* Add two advisory warnings for the *upper* bound: warn when an archived plan exceeds `3` total review passes or `8,000` words (`~50 KB`).

### 4. Archive closed one-off records out of `dev/measurement/`
* [`dev/measurement/README.md`](../measurement/README.md) states: *"Not an archive. Historical / closed records live under `dev/**/archive/`. This folder is live measurement, not a graveyard of finished work."*
* Move the closed July–August one-off files (`attestation-replay-failures.md`, `gitleaks-version-support.md`, `pip-audit-closure-ratio.md`, `tag-pass-dispositions.md`, `queued-issue-drafts.md`, `suite-cost.md`, `suite-runs.jsonl`) to an `archive/` subfolder (checking `claim_check.py` and test references first), leaving only the active incident trackers (`collision_log.md`, `maintainer-view-misses.md`, `review-floor-deviations.md`) and `README.md`.
