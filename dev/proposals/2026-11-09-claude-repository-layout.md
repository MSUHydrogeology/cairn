# Repository layout: one folder per purpose, Cairn self-contained under `dev/`

**Author**: Claude Opus 5.5 (`claude-opus-5-5`), Strategy
**Status**: revising
**Review**: usual + Security Review
**Proposed tier**: heavy — the moves touch the installer, every protected test, the gate manifest, the interpreter-binding reader and both `AGENTS.md` files
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-09
**In brief**: Reorganize Cairn's folders so each one's name says what it holds, and install everything Cairn puts in an adopter's repository under `dev/`.

## Decision summary

Today a file's folder does not tell you whether it ships to adopters. Root
`scripts/` is half Cairn-only, `bootstrap/` is mostly Cairn's own tests, and
adopters receive Cairn's tools into two generic folders, `scripts/` and
`tools/`, that they may already use for their own code.

This proposal gives every folder one purpose:

- `templates/`: exactly what the installer copies into an adopter's repository.
- `install/` (renamed from `bootstrap/`): what the agent doing an install reads
  to carry it out.
- `tests/` and `release/`: Cairn's own tests and its re-anchor and release
  machinery.
- `dev/tools/`: every installed tool, in adopters' repositories and in Cairn's
  own tree. Root `scripts/` and `tools/` disappear.

Principle, from the Maintainer in chat, 2026-11-09: "having Cairn be
essentially self-contained is a huge win." Adopters get a light footprint
(`dev/`, root `AGENTS.md` and its vendor wrapper, `.agents/skills/`); in Cairn,
a reader can tell what code is for from where it sits.

Cost: heavy tier, one Security Review, one re-anchor shared with the v0.8
release, a quiet window at the start of v0.8, and one path change for every
adopter on upgrade. Human operations added: the one re-anchor (Maintainer); zero
recurring.

## Context

Measured with `git` at `dac1611c` (2026-11-09) by matching files against path
strings in `bootstrap/_scaffold/config.py`:

| Folder | Installed in adopters | Cairn-only |
|---|---|---|
| `scripts/` | 18 | 16 |
| `tools/` | 16 | 4 |
| `bootstrap/` | 0 copied; installer run from here | 188 of 200, mostly 137 test files |
| `templates/` | 111 | 5 read before install, never copied |

- Two installed files live outside `templates/`: the onboarding guides in
  `docs/` (`bootstrap/_scaffold/install.py:1681`).
- `dimensions/`, `on-ramp/`, `templates/phase-0/` and
  `templates/codebase-readiness-report.md` are read before installing; the
  installer never reads them.
- About nine shipped files cite `bootstrap/SAFETY.md`,
  `bootstrap/verify_integrity.py` or `cairn/scripts/check_cairn.py`, which do
  not exist in an adopter's tree. The citation rule covers only
  `docs/methodology/`, and the link checker runs only in Cairn's tree.
- Cairn adopts itself only halfway. `dev/.cairn/cairn-lock.yml` lists 71 files
  but says version 0.3.0 and commit `unknown`, and omits `tools/code_map.py`. A
  change to a shipped tool is made twice by hand (`4f7be4f6` edits both copies
  of `session.py`) and hashes are refreshed in separate commits.

## Proposal

One plan, eleven items, delivered in v0.8:

1. **Tests location-independent, then `bootstrap/tests/` → `tests/`.** Replace
   the 295 lines that find files by counting parent folders with one shared
   repository-root helper before moving anything.
2. **Re-anchor and release machinery → `release/`**: the re-anchor and AST
   baseline runbooks, `reanchor.sh` and its launcher and values files, and
   `repin.py`, `reanchor_ceremony.py` and the two release checks from
   `scripts/`. The plan lists every file's destination.
3. **`bootstrap/` → `install/`.** It keeps the installer, `BOOTSTRAP.md`,
   `SAFETY.md`, `verify_integrity.py`, `UPGRADE.md`, `profiles/` and `prompts/`,
   and gains `templates/phase-0/`, the readiness report, and root `dimensions/`
   and `on-ramp/`.
4. **`templates/` holds exactly what the installer reads**: the two onboarding
   guides move in; the pre-install files move out (item 3).
5. **Cairn-only scripts → `tests/` or `release/`.** Test tooling and reporting
   tools go to `tests/`, with `audit_report` beside `gauge`, which it loads.
6. **Layout test**: every file in `dev/tools/` is an install destination, no root
   `scripts/` or `tools/` exists, every installer source is under `templates/`,
   and everything under `templates/` is read by the installer.
7. **Citations to Cairn's source**: extend the citation rule so `cairn/…` always
   means Cairn's source; rewrite bare citations of `bootstrap/` files; run the
   link checker on a test install.
8. **Folder roles written once** in `docs/DOCUMENTATION_PLAN.md`, linked from
   `README.md`.
9. **`case-studies/` → `docs/case-studies/`**, with the vendor-neutrality
   exemption in `quality_gate.py` and the allowance in `check_cairn.py` moved to
   that exact path, not widened to `docs/`.
10. **Installed `scripts/` and `tools/` → one flat `dev/tools/`.** All 46 install
    destinations move. `dev/modules/` keeps module docs only; not every tool
    belongs to a module (`session`, `board`, `git_read` and `meter` are core).
    `AGENTS.md` and `docs/DOCUMENTATION_PLAN.md` reword `dev/` from
    "deliberation" to Cairn's working tree: records, state and the tools that
    act on them.
11. **Cairn adopts itself through its own installer.** Its installed files are
    produced by running the upgrade on Cairn, and item 10's move is done that
    way, so Cairn's own upgrade is the first real run of the adopter
    migration. Modules Cairn does not self-host stay out through its profile.

**Adopter transition.** The command becomes `python install/scaffold.py`. A
small `bootstrap/scaffold.py` prints the new path and exits with an error until
v1.0; it never runs the installer. Upgrade retires old tool paths and installs
new ones; the intent hooks and shipped text (about 180 path mentions in 61
files) follow. `templates/` does not move, so upgrade's reads of older versions
by path (`upgrade.py:342`) are unaffected. One line each in `UPGRADE.md` and
`CHANGELOG.md`.

**Queued outcome, separate proposal.** Ship `token_budget.py` in the
`documentation-plan` module and `verify_counts.py` with an empty registry in
`claim-check`, each with its doctrine paragraph; hold `audit_report.py`, the
slimmed replacement for the `lifecycle-metrics` module retired at `6558f3ff`.
Revival: after this plan lands, so they install straight into `dev/tools/`.

**Open placement questions (not among the eleven items).** `dev/architecture_review.md` installs to the `dev/` root beside the core files, while other module notes go under `dev/modules/`. The Maintainer suggested `dev/measurement/` on 2026-11-10: its release assessments are evidence, but that folder's README limits it to process-health records and the file's first half is living reference. Decide it with item 10. A move changes three places in `config.py`, two claim-check allow-list entries and Cairn's own copy.

A second: the Maintainer suggested `dev/.cairn/` for `dev/ceremony-record.md` (2026-11-10). That folder holds tool-read configuration and state, while the record is a reader's written note; its nearest neighbors are the earlier ceremony files in `dev/measurement/ceremony-scripts-2026-10-28/` and the release machinery that item 2 moves to `release/`. The path is fixed in `scripts/repin.py`, the runbook and `test_repin_ceremony.py`, and the ceremony refuses if the record is not committed at HEAD, so a move is a trust-ceremony change that needs the plan's Security Review. Adopters do not receive the file.

**Sequence.** Root helper; pure-rename commits (git reports 100% similarity);
reference fixes; citations; layout test and roles; Cairn's self-upgrade; then
the certifying pair before and after with counts compared, a fresh AST baseline,
and the Maintainer's re-anchor as a separate board wait. Estimate: two to four
agent work sessions, mostly item 1; start at the opening of v0.8 with no plans
in flight.

## Rationale

The moves change no behavior; they make location carry meaning. Together
they cost one re-anchor, one quiet window and one adopter path change, not
several.

## Alternatives considered

- **Do nothing.** Folder names keep misleading, and shipped files keep citing
  paths adopters lack.
- **README lists per folder**, kept honest by the layout test. About an hour;
  loses the visible separation.
- **Small move (items 4–9).** Still heavy (ceremony scripts, an installer line);
  keeps the misleading `bootstrap/` and the adopter-side split.
- **Everything shipped under one root `cairn/` folder.** Puts Cairn-only tests
  in the "ships" folder and needs upgrade to handle two layouts by version.
- **Merge into `tools/` instead of `dev/tools/`.** Changes 86 mentions rather
  than about 180, but leaves Cairn in a generic adopter folder.
- **Tools beside their module** (`dev/modules/<name>/`). Moves 24 module docs and
  splits 12 tools that load `git_read` or siblings; deferred.

## Documentation / doctrine surface

Prescription: both `AGENTS.md` files (certification command path, `dev/` role,
citation rule). Description: `docs/DOCUMENTATION_PLAN.md` folder roles,
`README.md`, `install/UPGRADE.md`. Deliberation: this proposal and its plan.
Shipped module docs and skills change paths only.

## Evidence / verification plan

### Tests required

The promise is that every test, gate and installed tool behaves identically
from its new path. Checked through the real entry points: the certifying pair
before and after the move on clean commits, with identical pass, skip and node
counts; one adopter install and one upgrade from v0.7 into a temporary
directory; Cairn's own self-upgrade. New test: the layout test (item 6), in
`tests/`.

### Examples / smoke checks

`python install/scaffold.py --summary --config <profile>` and `--dry-run`;
both example self-tests; `python scripts/check_cairn.py` before the move and its
new path after; the link checker on a test install (item 7).

#### Security preflight — five questions, answered in writing

- **S1.** The layout test and the gate manifest decide what counts as installed
  and protected; their inputs are `config.py` and the tree, both committed
  Cairn source. No adopter-supplied input decides.
- **S2.** Mutations: add a stray file to `dev/tools/`; leave one test behind
  in `bootstrap/tests/`; point one installer source outside `templates/`. Each
  must fail the layout test or the count comparison. Not yet run.
- **S3.** The layout test runs in the suite; the count comparison runs in the
  plan's verification. Both cover the whole tracked tree.
- **S4.** A missed parent-count path can land on a real but wrong folder
  rather than failing. Item 1 removes that class before the move.
- **S5.** Executable code now sits under `dev/`, which agents edit constantly.
  `verify_integrity.py` still detects changed installed files, but a check that
  assumes `dev/` holds only text would now be wrong; the Security Review names
  any such check. The rules that refuse a linked `dev` folder protect only the
  next-session note today.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A protected test that fails or silently skips only after the move; differing
node counts; an adopter upgrade leaving both old and new tool copies.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance

Proposed paths:
- `dev/tools/`
- `docs/case-studies/`

## Review -- Terra -- 2026-11-12

Reviewed commit: be015399831b62898f10696191cd60b1b325a6c1

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

The strongest case is a recognizable, self-contained install, with Cairn's
own upgrade exercising the same migration adopters use.

**Foundations**

1. **Should this happen as framed?** Not yet: the transition needs to account for preserved local copies and Cairn's stale lock before promising one clean migration. -- `bootstrap/_scaffold/upgrade.py` `_classify_retired_records`; `dev/.cairn/cairn-lock.yml`.
2. **Best alternative.** Move installer sources and repair citations first while retaining the existing tool destinations; this loses the single `dev/tools/` footprint but avoids forcing the tool migration now. -- Proposal items 4, 7 and 10.
3. **What would show it wrong?** A real upgrade with a modified old tool or stale lock that loses the modification, silently leaves competing commands, or cannot complete falsifies the migration promise. -- `bootstrap/_scaffold/upgrade.py` `_cmd_remove_retired`.

1. **Blocking: define the adopter migration for modified and unprovable files.** Retirement currently removes only known unchanged copies and keeps others; the proposal both promises retirement and treats both copies remaining as failure. Specify how users find, reconcile and safely remove retained copies, and test unchanged, modified and unprovable cases through upgrade, including interrupted reruns. -- `bootstrap/_scaffold/upgrade.py` `_classify_retired_records`, `_cmd_remove_retired`.
2. **Blocking: establish the self-upgrade prerequisite.** Cairn's lock says 0.3.0 and unknown commit, and has unrecoverable bases; item 11 does not explain how the first real upgrade preserves local adaptations or handles files missing from the lock. Specify a verified reconciliation and a real self-upgrade check before relying on it. -- `dev/.cairn/cairn-lock.yml`.
3. **Non-blocking: reconcile the historical-read claim.** Keeping the `templates/` directory does not keep moved source paths stable: `_theirs_text` reads the lock's `src` at the requested revision. Explain compatibility for moved onboarding sources and historical revisions, or demonstrate those files are outside that contract. -- `bootstrap/_scaffold/upgrade.py` `_theirs_text`; `bootstrap/_scaffold/install.py` Write E.

**Audience and rule loss:** The summary communicates the goal, but the migration
needs the user-facing distinction in finding 1. No rule loss established from
the proposed prose; actual rewritten installed instructions were not available.

**Coverage:** Read the committed proposal, template, upgrade retirement and
historical reads, onboarding source and lock header; opening is 1,649 words
including headings, above the 1,000-word target. Did not independently recount
all historical figures, run an install, mutation, suite or security review.

## Security Review -- Sol -- 2026-11-12

Reviewed commit: be015399831b62898f10696191cd60b1b325a6c1

**Tier**: Security Review
**Model basis**: Sol High, explicitly assigned by the Maintainer through the coordinator.
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: initial read/probes approximately 7 minutes; recording/checks unknown.
**Tokens**: unknown

One-purpose folders and installer-driven self-adoption would reduce duplicate
maintenance while making Cairn easier to inspect.

**Foundations**

1. **Should this happen as framed?** Yes, with explicit migration and authority preservation: upgrade currently retains recorded destinations. -- `bootstrap/_scaffold/upgrade.py:802`.
2. **Best alternative.** Keep the proposed layout, but specify destination migration rather than retirement plus installation; retirement requires the template to disappear. -- `bootstrap/_scaffold/upgrade.py:663`.
3. **What would show it wrong?** A relocated executable selecting the wrong repository falsifies behavior preservation: executing committed root-selection statements with old/new paths produced `/tmp/adopter` versus `/tmp/adopter/dev`. -- `scripts/content_scan_runner.py:83`.

1. **Blocking: preserve migration ownership and local edits.** Upgrade uses old `dst` and suppresses new core-like destinations for already-tracked sources (`bootstrap/_scaffold/upgrade.py:802`, `bootstrap/_scaffold/upgrade.py:987`). Retained templates cannot qualify for retirement. **Closure:** specify ownership, fork, merge-base and hash migration; require data-preserving refusal for occupied/linked destinations and safe interrupted reruns.
2. **Blocking: define the anchored authority transition.** Pure renames change exact frozen paths and module names checked before imports (`scripts/repin.py:635`, `scripts/repin.py:701`). Equal counts cannot establish equivalent authority. **Closure:** require an old-anchor-to-new-layout transition preserving verify-before-import, interpreter binding and Maintainer authorization, with rejection probes for substituted helpers and unauthorized candidate code.
3. **Non-blocking: root authority extends beyond tests.** Item 1 addresses tests, but the scanner probe selects `dev` after relocation. **Closure:** include installed executable/configuration root discovery and exercise installed entry points against misleading nested roots.

**Audience / rule loss:** The summary is understandable. Preserve duties in
installed authoritative instructions; source-only folder-role documentation
cannot replace them. Rewritten instructions were unavailable.

**Coverage:** I read committed rules/template, migration, integrity and anchored
loader code; confirmed 71 lock records and absent `code_map`. No full historical
recount, migration, ceremony or suite run. Session orientation failed repository
detection. This over-target record retains security closure evidence. This is
the previously reported first pass, recorded after ordinary review serialization.
