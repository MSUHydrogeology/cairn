<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/lifecycle.md doctrine/proposals.md doctrine/dual-review.md doctrine/rationale.md doctrine/consolidation-review.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- The three paths below are forward references: every code file this plan
     creates is NEW, and they materialize across Chunks A-E. They are also
     registered under `Proposed paths:` -- that marker exempts only its own
     contiguous bullet block, so the file-scoped directive covers the chunk
     tables and acceptance criteria that cite the same paths in prose. Marked,
     not silenced; each line drops when its file lands. -->
<!-- claim-check-allow: scripts/transition_lint.py, scripts/transition_lint_whitelist.py, bootstrap/tests/test_transition_lint.py -->

# Plan: the transition-lint — an advisory check that a commit's message matches its lifecycle diff

**Source proposal**: `2026-07-22-claude-transition-lint` (accepted 2026-07-22 by
Maintainer Decision, *"Accepted, and queued"*). It sits under `dev/proposals/`
at the time of writing and moves to `dev/proposals/archive/` in the plan-open
commit. Referred to by **stem, not path**, throughout — the proposal's own head
carries three claim-marker maintenance notes about exactly this breakage.
**Status**: open
**Plan review**: required(**Internal**) — carried verbatim from the Decision
(*"`Plan review: required(Internal)` stands — no shipped-template,
install-contract, doctrine, or security surface is touched"*). See
[Plan review — the brief](#plan-review--the-brief-and-the-one-question-the-decision-could-not-have-asked)
for what this round must additionally settle. **No implementation commit lands
before a `### Plan review` sub-heading is in the tree.**
**Last update**: 2026-08-04
**Opened**: 2026-08-04

## Proposed paths

Every code file this plan creates is **new**, which is why this scope collides
with nothing in flight. They do not exist on disk yet, so they are registered
here rather than linked; the acceptance criteria rewrite them as relative
markdown links once they land (the same treatment the proposal used).

Proposed paths:
- `scripts/transition_lint.py` — the advisory check; lands across Chunks A–C.
- `scripts/transition_lint_whitelist.py` — its commit-SHA suppression whitelist; lands in Chunk D.
- `bootstrap/tests/test_transition_lint.py` — its behavioural + corpus tests; grows across Chunks A–E.

## Source proposal

The proposal settles one contract: **a stdlib-only, standalone, always-advisory
script that flags two shapes over a bounded rev-range** — (a) a commit subject
claiming a review / response / decision transition whose diff adds no such
section, and (b) a proposal- or plan-*open* commit whose added file already
carries a real review. It never gates anything, it ships no exception
vocabulary, and it enforces an existing rule (`doctrine/lifecycle.md:28-30`)
rather than creating one. The plan executes that decision and does not
re-litigate it.

The proposal was split out of the accepted `2026-07-08-claude-review-record-integrity`
(its Part C), went through a three-lens Internal panel that returned twelve
findings and a unanimous REVISE, an author Response accepting eleven (three with
modification, zero rejected), a Revised proposal, a Maintainer sequencing note
that held it undecided pending the sibling reader-fix, and finally a scribed
Decision. **Where the original proposal text and the Revised proposal or the
Decision disagree, the later document governs** — the original's `HEAD~20..HEAD`
default, its "ships empty" whitelist, its `-M` enumeration flag, its
proposals-only shape (b), and its case-sensitive matcher were all overturned in
revision and are dead text.

## The pre-registered constraints — the reason this scope was allowed to exist

Part C was not merely deferred; it was **split out under five named
constraints** that the sibling's Internal panel raised and the sibling's author
Response carried forward as pre-registrations. They are why the split was
permitted, and a plan that drops one silently re-opens what that review closed.
Each is restated below with its source anchor and the **acceptance criterion**
that discharges it. All five are also indexed in
[Acceptance criteria](#acceptance-criteria).

| # | Constraint, as pre-registered | Source (sibling, archived) | Discharged by |
| --- | --- | --- | --- |
| **R2** | Enumerate changes with `-M` / `--find-renames`. Rename-blind plumbing reports a plan-open's archived proposal as an *added* file carrying `## Review` and `## Decision`, which false-flags the dominant lifecycle commit shape. Add the rename-to-archive case as a must-not-flag test. | `dev/proposals/archive/2026-07-08-claude-review-record-integrity.md:291-302`; carried at `:434-438` | **AC-R2** — Chunk A ships `--find-renames=100%` enumeration; A6 pins `5140e21`/`57d1daf` (plan-open, `R100` + a genuine `A`) as must-trigger-but-not-flag, and E3 pins the archive renames as must-produce-zero-findings. |
| **R3** | State the load-bearing narrowing (fire only on commits touching `dev/proposals/` \| `dev/plans/`, excluding archive moves); name the exemption source of truth; **bound the vocabulary to restating it**; dogfood over ~30 real commits. | `:303-314`; carried at `:439-441` | **AC-R3** — Chunk A ships the narrowing as module constants; A7 pins the four carve-in commit shapes as never-triggered; the bright line (no exception keyword, no opt-out directive, no new contributor obligation) is a **scope fence**, restated in [Scope](#scope) and tested by A8. Dogfood is 868 commits, not 30. |
| **R4** | Part C's rules, exception vocabulary, and home are all deferred and must be **pinned against the real commit corpus** before implementation; evaluate `quality_gate.py --sub transition` versus a standalone script. | `:315-321`; carried at `:442-447` | **AC-R4** — the home is settled (standalone; the Revised proposal's four grounds, one downgraded). The corpus pinning is *re-executed for this plan* against the tree as it stands today, and it **did not hold** — see [The corpus has moved](#the-corpus-has-moved-and-this-is-the-plans-central-finding). That re-derivation, not the proposal's, is what Chunks B and E pin. |
| **R9** | Replace the speculative dogfood with **corpus-derived** edge cases (plan-open rename, plan-archive + `PLANNING.md` bundle, strategy / goodnight carve-in commits); drop the false "rejected-in-place adds no section" edge case. | `:362-370`; carried at `:475-478` | **AC-R9** — every synthetic fixture in Chunks A–C is traced to a **named real commit** in its table row, and Chunk E pins the real SHAs directly. The false edge case is gone; the Revised proposal reclassified the rejected/superseded case to *Known omissions* and this plan pins it as **must-SKIP**, not must-not-flag. |
| **R10** | Recast the `quality_gate.py` analogy to its `info` tier; **pin exact exit behaviour (advisory = always exit 0)**; commit to a suppression mechanism (exclusion roots + whitelist + info downgrade). | `:371-378`; carried at `:479-481` | **AC-R10** — Chunk A pins the exit contract with a test asserting `main()` returns 0 on a repo *with* findings. Suppression is exclusion roots (Chunk A) + a populated SHA whitelist (Chunk D). **The third layer — the class-level info downgrade — is dropped, and the Revised proposal says so in terms rather than silently.** This plan carries that disclosure forward as a first-class acceptance criterion (AC-R10b) so the unmet pre-registration cannot go quiet a second time. |

## The corpus has moved, and this is the plan's central finding

Everything in this section was measured **for this plan**, at HEAD `8f47c76`
(2026-08-03), under the canonical interpreter
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.x), by a throwaway
prototype of the Revised proposal's pinned heuristics that lives in this
session's scratch space and is deliberately not committed. Read the third row
first.

| window | scanned | triggered | findings | true positives | false positives |
| --- | --- | --- | --- | --- | --- |
| `<root>..d6646a3` (all history before the self-host) | 415 | 0 | 0 | 0 | 0 |
| `d6646a3..57d1daf` (the proposal's pinned window) | **120** | **52** | **3** | 3 | **0** |
| `57d1daf..HEAD` (everything since the proposal was written) | **333** | **265** | **20** | 0 | **20** |

`<root>` is `0f1fc68`, the repository's root commit. `A..B` is exclusive of `A`.
The three windows partition the 868-commit history exactly (415 + 120 + 333).

**Row 2 reproduces the Revised proposal to the digit** — 120 scanned, 52
triggered, 3 findings, and the findings are exactly `17b7e5c` twice (shape (b),
once per baked-in review section) and `f4a8308` once (shape (a)). SHA-pinning the
window was the right call and it paid off: nine months of drift later the numbers
still land. That is the R2-of-this-proposal fix vindicated.

**Row 3 is the problem.** The heuristics that scored zero false positives across
the proposal's corpus produce **twenty findings on the 333 commits written
since**, and every one I could classify is a false positive. The trigger rate
also jumped from 43 % to 80 % — Cairn's commit mix has shifted heavily toward
deliberation commits, so the narrowing filters far less than it did.

### The five false-positive classes, each with its cause and its count

| class | count | representative commit | cause |
| --- | --- | --- | --- |
| **FP-1 — the evidence-heading vocabulary is incomplete** | 5 | `cc8a25d` *"Add dedicated interpreter trust-root Security Review"* adds `## Security Review -- Codex …` | `## Security Review`, `## Security code review`, `## External Security Review`, `## Plan re-review`, `## Focused External first-use … review` do **not** start with `## Review` \| `## Plan review` \| `## Code review`. Measured: **26** h2 headings under `dev/proposals/` + `dev/plans/` contain "review" and match none of the three pinned prefixes. |
| **FP-2 — responses land as `###` sub-headings** | 7 | `31c40a0` *"lockfile-provenance-fields -- Response to External review (Codex)"* adds `### Response -- Claude (author)` inside an existing `## Plan review -- Codex …` h2 | Shape (a)'s span logic scans **h2 sections only**. A plan whose response is an h3 inside the review it answers carries no `## Response` h2 *at that commit*, so the added body falls inside the `## Plan review` span and finds no evidence section. Measured: 7 `### Response` sub-headings across the tree, and — the sharper point — the `## Response to plan review` **h2** convention that would have satisfied the rule did not yet exist when these seven commits landed; all 7 of its instances are dated 2026-08-03, after the last FP-2 commit. The convention changed *inside* the false-positive window. |
| **FP-3 — `accept` as ordinary English, plus a subject prefix hyphen-suppression eats** | 5 | `7728fc1` *"proposal-response: accept api-web actor boundary findings"* | `proposal-response` is a hyphen compound, so the true `response` claim is suppressed; `accept` then wins leftmost and demands a `## Decision`. **The `accept` token has 0 true positives and 5 false positives across all 868 subjects** — every real Decision subject also carries the word "Decision", which wins leftmost anyway. This is the identical evidence shape that retired `opening`. |
| **FP-4 — "respond to … review" reads as a review claim** | 2 | `283be88` *"portable-security-sweeps: respond to External security review"* adds `## Response -- Codex (author)` | `respond` is not a token (`responses?` does not match it), so `review` wins leftmost and demands a review section the commit correctly did not add. |
| **FP-5 — an explicit negation** | 1 | `88fd91f` *"dev/proposals: transition-lint -- record Maintainer sequencing direction (not a Decision)"* | `Decision` matches inside a parenthetical that literally denies the claim. Fittingly, this is a commit on the transition-lint proposal itself. |

Twenty findings, twenty false positives, **zero of them shape (b)**. That
asymmetry is the second finding and it is good news: across 333 new commits
including **six** new plan-opens (`7a573d9`, `3900b05`, `4cfa047`, `49c85bc`,
`05515df`, `9c45d51`), the grammar-marker discriminator produced not one false
positive. The Revised proposal's shape-(b) extension to plans — `**Status**:
proposed | open | awaiting-plan-review`, sections `## Review` \| `## Plan review`
\| `## Code review`, markers `[R<n>]` \| `[E<n>]` \| `**Steelman` \|
`**Covered**` — validated on two plan-opens and now holds on eight.

### What this means for the plan, stated as a scope question and not decided here

The proposal's *Signals the change is wrong* section is explicit: *"It fires on
a benign commit in ordinary use. Recovery: whitelist the SHA with a written
reason **and** open a follow-up to fix the heuristic … If entries accumulate
past a handful, retire the tool."* Twenty entries is not a handful. **Shipping
the heuristics exactly as pinned and whitelisting twenty SHAs is therefore not
an option this plan will take** — it is the failure mode the proposal names.

Three of the five classes are **mechanical widenings of an explicitly-pinned
list**: FP-1 adds heading prefixes, FP-2 adds h3 spans, FP-4 adds `respond` (or
demotes `review` behind it). Widening the *evidence* side can only ever reduce
findings; it cannot make the tool flag something it did not flag before, so it
cannot manufacture a new false positive. That is a safe, one-directional change
and Chunk B ships it.

Two are not mechanical. **FP-3 requires deleting `accept` from the claim
vocabulary table the Decision reproduces**, and FP-5 requires either a negation
guard or an accepted residual. Deleting a token *narrows* the tool, which can
create a false negative, and the accepted scope quotes that table. This plan
**does not decide those two**; it ships the evidence and routes them to the plan
review and the Maintainer — see
[Maintainer fence](#maintainer-fence--the-two-decisions-this-plan-does-not-take).

## Scope

Executes the accepted contract across six chunks and four files. **Every code
file is new**, so no file in flight is touched and no frozen file is modified.
Nothing ships to an adopter; no manifest row moves.

**Out of scope, fenced explicitly:**

* **Any exception keyword, in-message opt-out directive, or new obligation on a
  contributor.** This is the proposal's bright line, unchanged and verbatim
  across the original, the Revised proposal and the Decision. If implementation
  discovers it needs a rule neither `AGENTS.md`'s approval carve-in nor
  `doctrine/proposals.md` > "File moves" already states, that is **new
  operational doctrine** and it stops for its own rate-limited proposal. It does
  not ship inside this tool. Pinned by A8.
* **Rename-only commits — reject/supersede Decisions and plan-archives.**
  Documented as a **gap**, never claimed as coverage (the Revised proposal's
  *Known omissions*). `reject` and `supersede` stay in the vocabulary as
  commented dead tokens. The v2 candidate (let an `R` into `archive/` trigger
  shape (a) only) is recorded, not built — and see the correction to its premise
  in Chunk E.
* **Bundling detection.** The tool checks only that a claim is *supported*; it
  does not detect unannounced lifecycle work or lifecycle work bundled with
  implementation work. Leftmost-wins makes this structural. Named in
  `docs/tool-usage.md`, not fixed.
* **Merge commits, squashed / rebased / amended history, `git notes`, commit
  bodies.** Only the subject line is parsed. Re-verified for this plan: the
  repository has exactly two merges (`4bf4ee4` 2026-06-09, `d6646a3`
  2026-06-10), both outside the pinned window, and `git rev-list --merges
  --count d6646a3..57d1daf` → **0**.
* **Shipping to adopters.** Deferred to v2. The Revised proposal re-argued the
  natural home as a `lifecycle_metrics` subcommand (zero new manifest entries),
  and rejected v1 shipping on the ground that survives: the heuristics are pinned
  against Cairn's own subject conventions. Row 3 of the table above is now direct
  evidence for that rejection — the conventions drifted inside **one tree in
  twelve days**.
* **The `_STAGE_COMMIT_PATTERNS` reader-fix.** Its own proposal stem
  (`2026-07-22-claude-stage-commit-patterns`). This plan imports nothing from
  `templates/` and shares no regex with it.
* **Any `bootstrap/_scaffold/` change.** None. If implementation finds itself
  touching that package, that is a scope breach and it stops.
* **Any import across the `scripts/` ↔ `templates/` boundary.** Ruled out by the
  Revised proposal on the narrow ground that it would couple a repo-local script
  to a file `bootstrap/tests/_gate_manifest.py:165-167` byte-freezes. The `-z`
  walk idiom is **copied and re-implemented**, not imported. Pinned by A9.

### Documentation / doctrine surface

* **Governing layer — none.** No `AGENTS.md` change, no `doctrine/` change. The
  rule the tool makes visible is already accepted and already written
  (`doctrine/lifecycle.md:28-30`). The doctrine-change rate-limit in
  `doctrine/rationale.md` is therefore not engaged, exactly as the proposal's
  own "N/A" declared.
* **Descriptive layer — `docs/tool-usage.md`**, one new section (Chunk F),
  routed per [`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md) as
  a description of the software as it is. Modelled on the
  `## scripts/verify_counts.py — re-measure registered live-invariant counts
  *(Cairn-maintainer-only)*` heading at `docs/tool-usage.md:44`, plus a
  `## See also` cross-link at `docs/tool-usage.md:147`.
* **Code-adjacent prose** — the module docstring of `scripts/transition_lint.py`
  and the per-entry rationale comments in
  `scripts/transition_lint_whitelist.py`, landing in the same commits as the
  behaviour they describe.
* **Release-facing — `CHANGELOG.md > Unreleased > Added`**, one line. **This is
  a serialized shared file**: the implementing agent returns the exact text and
  does not edit the file.
* **Deliberation layer** — this plan, its plan review, its code review, and the
  one-line `dev/PLANNING.md` row-move that serializes the plan-open. **Also
  serialized**: the row-move text is returned, not applied.
* **No shipped template, no module, no install-manifest entry.** Re-verified for
  this plan: `python bootstrap/scaffold.py --manifest` carries no `scripts/`
  entry, and Cairn's own `scripts/` tools are repo-local by construction.

<!-- cairn:slot documentation-tier-home -->
**Doc tier home rule** — route doc and doctrine changes by layer per
[`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):
cross-cutting prescription → governing layer (`AGENTS.md`);
deliberation about what to build → deliberation layer (`dev/`);
description of the software as it is → descriptive layer (`docs/`). A
plan's *Scope* must name the doctrine-surface touched (or an explicit
"no doctrine surface").
<!-- cairn:end documentation-tier-home -->

### Gate accounting

Every figure is a dated snapshot measured for this plan; re-take at
implementation rather than quoting from here.

* **Suite baseline: 2 failed, 1744 passed, 0 skipped**, `as_of 2026-08-04`, under
  `/Users/kendal30/conda_envs/lhm/bin/python3.13` with `PYTHONDONTWRITEBYTECODE=1`
  (206 s). The two failures are the known stale AST-attestation nodes
  (`test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package`
  and `::test_ast_gate_passes_over_the_full_scaffold_module_set`, issue #1).
  **This corrects the proposal's baseline**, which recorded *3 failed, 1408
  passed, 3 skipped* on 2026-07-22 and named a third node,
  `test_evolution_infer.py::TestGateEval::test_main_suggests_and_json` — that
  node passes today. The correct claim is **"the two known failures stay the
  only failures, 0 skipped stays 0, and collection grows by exactly the new
  nodes."** **Caveat, disclosed rather than buried:** this figure was taken with
  several concurrent workflows' edits live in the working tree (`bootstrap/_scaffold/`,
  `bootstrap/verify_integrity.py`, two new test files, six untracked sibling
  plans). It is therefore a *working-tree* baseline, not a HEAD baseline, and the
  implementing agent must re-take it at the plan's own starting commit before
  asserting any delta.
* **No frozen file is modified, and this was checked rather than assumed.**
  `bootstrap/tests/_gate_manifest.py:165-167` globs `scripts/*.py` and
  `bootstrap/tests/**/*.py` into the frozen set, and `:15-16` makes modifying a
  frozen file a HOLD. All three code files here are **new**, so
  `bootstrap/tests/_gate_manifest.py:366` records them as `FROZEN-NEW`
  (*"new gate/test file — allowed, recorded"*), not `:364`'s
  `FROZEN-MODIFIED`. **There is therefore no supervised re-pin ceremony on this
  plan** — a claim a reviewer should check by reading those three lines.
* **No AST re-anchor.** Nothing under `bootstrap/_scaffold/` changes;
  `bootstrap/tests/test_ast_attest.py` pins that package only, so
  `bootstrap/REANCHOR_RUNBOOK.md` is not in play.
* **The install contract must not move.** Expected diff against a pre-change
  `python bootstrap/scaffold.py --manifest` capture: **empty**. A diff means
  something reached the engine and the plan stops.
* **Doc gates.** `python scripts/check_cairn.py` → OK over **180** Markdown
  files, `as_of 2026-08-04`; the count may only grow.
  `python scripts/quality_gate.py --sub neutrality` → **fail=95, info=21**,
  `as_of 2026-08-04`. **This corrects the proposal's `fail=99`**, which was
  accurate on 2026-07-22 and has since moved; the figure must not move *because
  of this plan*, which is the checkable claim.
* **`scripts/` file count.** `ls scripts/*.py | wc -l` → **16**, `as_of
  2026-08-04`, matching the Revised proposal. This lands as the **17th and
  18th**. No doctrine tracks script-count growth in `scripts/` — the Revised
  proposal established that `doctrine/consolidation-review.md` does not cover it
  — so this remains a judgement call the Maintainer makes explicitly.

## Sequence

Chunk order is load-bearing. **Chunk A lands the enumeration, the exit contract
and the census before any finding logic exists**, so that at no intermediate
commit can the script print a finding it cannot justify, and so the advisory
exit contract is pinned by a test before there is anything to be tempted to gate
on. **Chunk D lands before Chunk E** because the corpus tier needs the
whitelist-bypass argument.

```
0. plan-open -- this plan + the dev/PLANNING.md row-move            [commit pending]
   (plan review) -- required(Internal); NO code before it lands
1. Chunk A -- plumbing: rev-range, enumeration, narrowing, exit     [commit pending]
2. Chunk B -- shape (a): claim detection and section evidence       [commit pending]
3. Chunk C -- shape (b): the baked-in-review detector               [commit pending]
4. Chunk D -- the suppression whitelist and its hygiene tests       [commit pending]
5. Chunk E -- the corpus-regression tier                            [commit pending]
6. Chunk F -- docs/tool-usage.md + the changelog line               [commit pending]
```

---

### Chunk A — plumbing: the rev-range, the enumeration, the narrowing, the exit contract

Discharges **AC-R2**, **AC-R3** and **AC-R10** (exit half). Nothing in this
chunk can produce a finding; `scan()` returns an empty list and `main()` prints
only the census. That is deliberate — the invariant *"`main()` never returns 1"*
is easier to pin before there is a finding to gate on, and R10's whole point is
that the fail-tier must never get wired up by accident.

| # | File | Change |
|---|------|--------|
| A1 | `scripts/transition_lint.py` | Module docstring: what the tool is, that it is **advisory and never gates**, that it is Cairn-repo-local and **not installed into adopter trees**, and the two-posture git-error rule stated where the code is — *fail-fast on inputs, degrade-quiet on per-commit enumeration*. Stdlib-only imports (`argparse`, `re`, `subprocess`, `sys`, `dataclasses`, `pathlib`). |
| A2 | `scripts/transition_lint.py` | `@dataclass class Finding` carrying exactly `(sha, shape, file, message)` — **no `severity` field**, so there is no fail-tier present to sum. Contrast `scripts/quality_gate.py:91` (which does carry one), its `failed` property at `:117`, and `:833`'s `return 1 if report.failed else 0`. The docstring records that the missing field is *not* the pin — the Revised proposal withdrew "pinned in the type system" — and points at A11 as the actual pin. |
| A3 | `scripts/transition_lint.py` | Module constants in the shape of `scripts/quality_gate.py:497` / `:500`: `_TRIGGER_ROOTS = ("dev/proposals/", "dev/plans/")`, `_EXCLUDE_SUBSTRING = "/archive/"`, `_EXCLUDE_BASENAME = "_template.md"`. A comment attributes the `/archive/` exclusion to `doctrine/proposals.md` > "File moves" (`:316-320` blesses the plan-open archive bundle; `:322-325` the reject/supersede archive bundle) — **not** to the `AGENTS.md` approval carve-in, per the Revised proposal's retitling. |
| A4 | `scripts/transition_lint.py` | `_validate_range(rev_range)` — **fail-fast on inputs**. Re-implement the narrow regex from `scripts/measurements.py:54` (`^[0-9A-Za-z._/~^-]+\.\.\.?[0-9A-Za-z._/~^-]+$`), then resolve **both endpoints** with `git rev-parse --verify`. Any failure → a one-line stderr message and `return 2`, matching the usage-error convention at `scripts/quality_gate.py:817-822`. This is the silent-clean fix the Decision ratified: *"A rev-range that parses but does not resolve … must not exit 0 with no output."* Fixed argument vector, `shell=False`, no shell string — the security posture recorded at `scripts/measurements.py:24-27` and implemented at `:142-155`. |
| A5 | `scripts/transition_lint.py` | `_entries(sha)` — **degrade-quiet on enumeration**. `git diff-tree --no-commit-id --name-status --find-renames=100% -r -z <sha>`, parsed by a **copied and re-implemented** `-z` token walk: `R<score>\0<source>\0<dest>` advances 3, `<status>\0<path>` advances 2. The idiom is at `templates/modules/team-gated/_intent/conflict.py:771-790`; its degrade-quiet posture (`check=False` at `:765`, empty return on non-zero at `:769-770`) is at `:767-770`. **Nothing is imported** — that function runs `git diff --cached`, takes no rev-range, and discards every non-`R` entry, so it cannot enumerate an A/M set. A git error yields an empty list and the commit is skipped. |
| A6 | `scripts/transition_lint.py` | `_triggers(entries)` — a commit is examined only if it has an `A` or `M` entry under a trigger root, after the two exclusions. A rename is never a trigger. |
| A7 | `scripts/transition_lint.py` | `scan(rev_range, root, whitelist)` returning `(scanned, triggered, findings)`, and `main(argv)` printing the **census on every run including a clean one** — `scanned N commits, T triggered, F findings` — then each finding. `--report` emits TAB-separated `sha<TAB>shape<TAB>file<TAB>message`, mirroring `quality_gate`'s machine mode. The rev-range positional is **required**; omitting it is exit 2, not a default (Open question 1, resolved in revision: a HEAD-relative default is what produced the proposal's own stale-endpoint defect). |
| A8 | `bootstrap/tests/test_transition_lint.py` | Module scaffolding: load the script by path via `importlib.util.spec_from_file_location` (the idiom at `bootstrap/tests/test_quality_gate_cli.py:29-35`), a module-level `pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")` in the posture of `bootstrap/tests/test_upgrade.py:1278`, and a `_repo(tmp_path)` fixture building a throwaway git repo with a fixed `-c user.name` / `-c user.email` identity. |

**Acceptance criteria — Chunk A.** Every test below names the perturbation that
makes it RED, and the perturbation is on the **hazard**, never on the test's own
body. *Perturbing a test's own fixture validates the fixture; only perturbing
the thing the test claims to guard validates the claim.*

| test | asserts | the perturbation that makes it RED |
| --- | --- | --- |
| **A9** `test_main_returns_zero_on_a_repo_with_findings` | `main([rev_range, "--root", repo])` → `0`, with at least one finding printed to stdout. Deferred to Chunk B for the finding; land in A as an xfail-free stub against a hand-planted stub finding injected through `scan`'s public return. | **Change `main`'s tail to `return 1 if findings else 0`.** This is R10's invariant and A9 is the pin the Revised proposal named when it withdrew the type-system claim. Run it: the test must go red on that one-line edit. |
| **A10** `test_unresolvable_but_parsable_range_exits_2` | `main(["deadbeef000..HEAD", "--root", repo])` → `2`, stderr non-empty. | **Delete the `git rev-parse --verify` call in A4**, leaving only the regex. The range then passes validation, enumerates nothing, prints `scanned 0 …`, and returns 0 — the exact silent-clean hole the Decision forbids. Red. |
| **A11** `test_malformed_range_exits_2` | `main(["not a range", "--root", repo])` → `2`. | Delete the regex guard; `git rev-list` then errors and the degrade-quiet path swallows it. Red. |
| **A12** `test_missing_range_exits_2` | `main(["--root", repo])` → `2`. | Give the positional a `HEAD~20..HEAD` default. Red — and this is the perturbation that restores the *original* proposal's behaviour, which revision overturned. |
| **A13** `test_census_prints_on_a_clean_run` | A repo with one benign lifecycle commit → stdout contains `scanned 1 commits, 1 triggered, 0 findings`. | Guard the census print behind `if findings:`. Red. A zero-finding run must be positive evidence, not silence. |
| **A14** `test_a_rename_into_archive_never_triggers` | Fixture: `git mv dev/proposals/<slug>.md dev/proposals/archive/<slug>.md`, subject *"Maintainer Decision — SUPERSEDE thing"*. `triggered == 0`. **Traced to `b064576`** (the tree's only supersession). | **Delete `_EXCLUDE_SUBSTRING` from A3.** The archive destination then reaches the trigger set. Red. |
| **A15** `test_a_plan_open_triggers_but_the_archived_proposal_does_not` | Fixture: one commit adding `dev/plans/<slug>.md` **and** renaming `dev/proposals/<slug>.md` into `archive/` byte-identically. The plan file triggers; the archive path is excluded. **Traced to `5140e21` and `57d1daf`.** | **Drop `--find-renames=100%` from A5's argument vector.** Verified against the working tree for this plan: `git diff-tree --no-commit-id --name-status -r 5140e21` reports `D dev/proposals/…` + `A dev/proposals/archive/…` where `--find-renames=100%` reports `R100`. The `A` is still excluded by `/archive/`, so this alone stays green — which is why A16 exists. **This is R2's constraint and the pair A15+A16 is what discharges it.** |
| **A16** `test_a_proposal_derived_plan_is_not_absorbed_into_a_rename` | Fixture: a plan-open whose new `dev/plans/<slug>.md` is a near-copy of the proposal it derives from (Cairn plans are proposal-derived — `dev/plans/archive/review-record-integrity.md:15`, `## Source proposal`) and the proposal is deleted **without** archiving. Asserts the plan enumerates as `A` and the commit triggers. | **Replace `--find-renames=100%` with bare `-M`.** The two files pair at ~96 % similarity, the genuine `A` is absorbed into an `R`, and the commit silently un-triggers. Red. This is the hazard the Revised proposal pinned the threshold against, and the *reason* the threshold is exactly `100%` and not `-M`. |
| **A17** `test_a_commit_with_no_lifecycle_A_or_M_never_triggers` | Fixture: a `dev/strategy/`-only commit whose subject reads *"open … review … Decision"*; and a second fixture bundling only `dev/PLANNING.md` + `CHANGELOG.md` + `dev/NEXT_SESSION.md`. `triggered == 0` for both. **Traced to `18707e9`, `d0ba903`, `ebb1d6e`** (strategy carve-in) and the goodnight-handoff shape. | **Add `dev/strategy/` to `_TRIGGER_ROOTS`.** Red. This is **AC-R3**: the narrowing alone discharges the approval carve-in, so the tool needs no exception vocabulary — and this test is what proves the narrowing is doing that work rather than a keyword list quietly doing it. |
| **A18** `test_the_tool_ships_no_exception_vocabulary` | A source-level assertion over `scripts/transition_lint.py`: the file contains no `skip`/`exempt`/`no-lint`/`transition-lint:` directive token, and `scan` reads nothing from the commit **body** (`%b`) or from `git notes`. | **Add a `# transition-lint: skip` opt-out branch.** Red. The bright line the Decision ratified is *"no exception keyword, no in-message opt-out directive, no new obligation."* A prose fence is not a fence; this makes it mechanical. |
| **A19** `test_no_import_crosses_the_scripts_templates_boundary` | AST-walk `scripts/transition_lint.py`: no `Import`/`ImportFrom` naming a `templates` path, no `sys.path` mutation, no `spec_from_file_location` pointing under `templates/`. | **Add `from templates.modules...conflict import _rename_map_via_git`.** Red. Pins the Revised proposal's header scope claim: the `-z` idiom is copied, never imported, because importing would couple a repo-local script to a file `bootstrap/tests/_gate_manifest.py:165-167` byte-freezes. |
| **A20** `test_empty_range_is_clean_and_zero` | `main(["HEAD..HEAD", "--root", repo])` → `0`, census reads `scanned 0 commits, 0 triggered, 0 findings`. | Make `scan` raise on an empty commit list. Red. |

---

### Chunk B — shape (a): the message claims a transition the diff does not contain

Discharges **AC-R4** (the corpus re-pinning). This is where the twenty
false positives are answered.

| # | File | Change |
|---|------|--------|
| B1 | `scripts/transition_lint.py` | `_claim(subject)` — **case-insensitive (`re.IGNORECASE`)**, each token matched as `(?<![-\w])<token>s?(?![-\w])`, **leftmost match wins**, at most one claim per subject. Case-insensitivity is not optional and the comment says why: `f4a8308`'s subject is *"dev/proposals: add Gemini External **Review** for check_cairn self-host-compat"* — capital `R`. A case-sensitive build produces no claim, no finding, and silently inverts the headline result. |
| B2 | `scripts/transition_lint.py` | The claim vocabulary. `open` — **positionally anchored** as the first word after the `dev/<tree>: ` prefix. `review`/`reviews`. `response`/`responses`. `decision`, and — pending the Maintainer fence — `accept`. `reject` and `supersede` are retained with an inline comment marking them **dead tokens in v1** (rename-only Decision commits are never examined). `opening` is **not** present: 0 true positives in 868 subjects, re-verified for this plan. |
| B3 | `scripts/transition_lint.py` | `_section_spans(sha, path, prefixes)` — read the post-image with `git show <sha>:<path>`, find headings, and return `(start_line, end_line, heading)` per matching section. **Amended for FP-1 and FP-2**: match **h2 and h3** headings, and match a section by *containing* its kind rather than by a three-prefix `startswith`. The measured gap, `as_of 2026-08-04`, is **26** h2 headings under `dev/proposals/` + `dev/plans/` that contain "review" and match none of `## Review` \| `## Plan review` \| `## Code review` — of which **24** are genuine review sections (`## Security Review`, `## Security code review`, `## External Security Review` and its round variants, `## Plan re-review` ×5, `## Focused External first-use … review` ×6, `## Re-Review`) and 2 are prose sections whose titles merely contain the word. Plus **7** `### Response` sub-headings whose bodies sit inside a `## Plan review` span. The implementing agent re-derives both figures rather than quoting them. |
| B4 | `scripts/transition_lint.py` | `_added_nonblank_lines(sha, path)` — parse `git show --find-renames=100% --format= --unified=0 <sha> -- <path>` hunk headers for the post-image start, then walk the `+` lines counting non-blank. **Pin the header grammar explicitly**: `@@ -a,b +c,d @@` where a missing `,d` means count 1, and `+c,0` is a pure deletion. Note the flag change — the Revised proposal wrote `-M` here and `--find-renames=100%` for `diff-tree`; the two must agree or the evidence and the trigger disagree about what the file is. |
| B5 | `scripts/transition_lint.py` | Evidence rule: **≥ 3 non-blank added lines whose post-image line numbers fall inside a matching section's span**. Heading-presence is worthless and the comment records why: `3ae1d47` seeds a titled `## Review …` placeholder at line 249 of the added blob, so the genuine review-append `e31625c` adds **zero** `+## Review` lines — a heading rule flags the honest commit and misses the dishonest one. Verified for this plan: `git show --format= --unified=0 e31625c \| grep -c '^+## Review'` → **0**, and its single hunk is `@@ -251,6 +251,166 @@`, i.e. 166 added lines starting inside the span. |
| B6 | `scripts/transition_lint.py` | The `open` claim's evidence is an `A` entry under a trigger root — the one claim whose evidence is structural rather than sectional. |

**Acceptance criteria — Chunk B.**

| test | asserts | the perturbation that makes it RED |
| --- | --- | --- |
| **B7** `test_case_insensitive_subjects_produce_the_same_finding` | Two fixture commits identical but for subject case (`add gemini external review …` / `ADD GEMINI EXTERNAL REVIEW …`) produce the **same** finding. | **Drop `re.IGNORECASE` from B1.** The uppercase fixture stops flagging. Red. Note the honest asymmetry: the *dogfood cannot catch this* — a case-sensitive build also scores zero false positives; it just produces silent false negatives that look like passes. That is why this is a test and not a corpus row. |
| **B8** `test_a_review_claim_with_no_added_body_flags` | Fixture reproducing `f4a8308`: subject claims a Review append; the diff adds only two marker lines at the top of the file, none inside any review span. Flags shape (a). | **Lower the threshold in B5 from 3 to 0**, i.e. accept heading-presence. The seeded placeholder then counts as evidence. Red. |
| **B9** `test_a_genuine_review_append_does_not_flag` | Fixture reproducing `3ae1d47` → `e31625c`: an open commit seeding `## Review — …` with an *"(Awaiting …)"* body, then a review commit replacing that body with 20 lines and adding **no** `+## Review` line. No finding. | **Change B5 to require an added `+## <kind>` heading line.** The honest commit flags. Red. This is the pair that kills the naive heading rule, and running both halves is what makes B8 and B9 a discriminating pair rather than two green lights. |
| **B10** `test_hyphen_compounds_do_not_claim` | Subjects `dev/plans: review-record-integrity -- Sharpening`, `dev/proposals: automated-review-committer -- open`, and `dev/measurement: review-floor deviations` produce no *review* claim from the slug. **Traced to `2432f10`.** | **Replace the lookaround with a bare `re.search("review")`.** All three flag. Red. |
| **B11** `test_open_is_positionally_anchored` | The three subjects the Internal panel constructed must not flag: `dev/proposals: transition-lint -- resolve open questions from the Internal review`; `dev/plans: X -- close out the open acceptance criteria`; `dev/plans: transition-lint -- opening sequence step 1`. | **Remove the positional anchor**, matching `open` anywhere. All three demand an `A` entry an M-only commit lacks. Red. "Open questions" is live Cairn vocabulary — `templates/core/dev/strategy/_template.md:129` — so this is a real subject shape, not a constructed one. |
| **B12** `test_a_security_review_section_counts_as_review_evidence` | **FP-1.** Fixture: subject *"Add dedicated interpreter trust-root Security Review"*, body added under `## Security Review -- <reviewer> -- <date>`. No finding. **Traced to `cc8a25d`, `d0102a6`, `3da58c1`.** | **Revert B3 to the three-prefix `startswith`.** The section becomes invisible and the honest commit flags. Red. |
| **B13** `test_an_h3_response_inside_a_plan_review_counts_as_response_evidence` | **FP-2.** Fixture: a plan carrying `## Plan review -- <reviewer>` with a later `### Response -- <author>` sub-heading receiving 30 added lines. Subject *"dev/plans: X -- Response to External review"*. No finding. **Traced to `31c40a0`, `8900e46`, `8abd453`, `8d876e0`, `eb4ec16`, `ce8e20e`, `e953095`.** | **Restrict B3's span scan to h2.** The fixture's response body then falls inside the `## Plan review` span with no `## Response` h2 present, and the commit flags. Red. The fixture must reproduce the *pre-2026-08-03* plan shape (h3 response, no `## Response` h2) — building it from a current plan would hand the test a `## Response to plan review` h2 that satisfies even the un-widened rule, and the test would pass under both. |
| **B14** `test_respond_to_a_review_is_not_a_review_claim` | **FP-4.** Subject *"portable-security-sweeps: respond to External security review"* adding a `## Response` section produces no finding. **Traced to `283be88`, `9754635`.** | Two candidate fixes; the plan review chooses. Either add `respond`/`responds` as a **response** token (so leftmost-wins picks it up before `review`), or accept `## Response` as evidence for a review claim. The perturbation for either is deleting it — the subject then claims *review*, finds no review section, and flags. Red. |
| **B15** `test_the_evidence_widening_cannot_create_a_finding` | A property test over the corpus fixture set: for every fixture in Chunks A–C, the finding set under B3-as-shipped is a **subset** of the finding set under the three-prefix h2-only rule. | Invert one widening so it also *narrows* (e.g. make the kind-match exclusive rather than containing). Red. This is the pin on the claim in [Scope](#what-this-means-for-the-plan-stated-as-a-scope-question-and-not-decided-here) that widening the evidence side is one-directional — asserted there, tested here. |

---

### Chunk C — shape (b): an open commit whose added file already carries a real review

The chunk that reproduces the original incident. Zero false positives across
868 commits and eight plan-opens, measured for this plan — the strongest result
in the whole exercise, and the one Chunk E must keep true.

| # | File | Change |
|---|------|--------|
| C1 | `scripts/transition_lint.py` | For each `A` entry under a trigger root: read the added blob's **first 60 lines** (the header bound the Revised proposal pinned after the panel's negative-space #3 flagged it undefined) and require `**Status**:` to be one of `proposed` \| `open` \| `awaiting-plan-review`. Verified for this plan: across every file under `dev/proposals/` and `dev/plans/` including archives, the deepest `**Status**:` line in a non-template file is **line 31** (this proposal's own, behind a long marker header); the two `_template.md` files sit at 77 and 123 and are excluded by `_EXCLUDE_BASENAME`. 60 has ~29 lines of headroom and the bound is stated in the code, not inferred. |
| C2 | `scripts/transition_lint.py` | Scan `## Review` \| `## Plan review` \| `## Code review` section bodies (extended per B3) for a **review-grammar marker**: `[R<n>]`, `[E<n>]`, `**Steelman`, `**Covered**`. The marker is the discriminator between a seeded placeholder and a baked-in review — it is what makes shape (b) fire twice on `17b7e5c` and stay silent on `3ae1d47`, `87d3498`, and all six new plan-opens. |
| C3 | `scripts/transition_lint.py` | One `Finding` **per baked-in section**, not per commit — `17b7e5c` must produce two, once per review section. |

**Acceptance criteria — Chunk C.**

| test | asserts | the perturbation that makes it RED |
| --- | --- | --- |
| **C4** `test_an_open_commit_with_a_baked_in_review_flags_once_per_section` | Fixture reproducing `17b7e5c`: an `A` blob with `**Status**: proposed` and two `## Review …` sections, each carrying `[R1]` markers. **Two** findings. | **Delete the grammar-marker check in C2**, accepting any non-empty section. Then C5 flags too — so run C4 and C5 together; the pair is what makes the discriminator load-bearing rather than decorative. |
| **C5** `test_a_seeded_placeholder_review_at_open_does_not_flag` | Fixture reproducing `3ae1d47`: an `A` blob with `**Status**: proposed` and `## Review — <reviewer> — <date>` whose body is *"(Awaiting the Internal review…)"*. No finding. | Same perturbation as C4. Red. |
| **C6** `test_a_baked_in_plan_review_at_plan_open_flags` | Fixture: an `A` blob with `**Status**: awaiting-plan-review` and a `## Plan review` section carrying `[E1]`. One finding. | **Revert C1 to `proposed` only** (the original proposal's rule). No plan ever carries `proposed`, so the exact analogue of the `17b7e5c` incident becomes undetectable. Red. **This is R9-of-this-proposal's fix and it must not regress.** |
| **C7** `test_a_placeholder_plan_review_at_plan_open_does_not_flag` | Fixture reproducing `5140e21` / `57d1daf`: `**Status**: awaiting-plan-review` with **empty** `## Plan review` / `## Code review` placeholders and zero grammar markers. No finding. | Delete the marker check. Red — and this is the false positive C6's widening would otherwise buy, so C6 and C7 are the second discriminating pair. |
| **C8** `test_a_status_beyond_the_header_bound_is_not_read` | Fixture: an `A` blob whose `**Status**: proposed` sits at line 80 with a baked-in review below. No finding, and the bound is the documented reason. | Raise the bound to the whole file. Green→red is the wrong direction here, so assert the **inverse**: move the status line to line 31 (the real-world deepest) and confirm the finding *appears*. A bound test that only ever asserts silence cannot distinguish "bounded correctly" from "never fires". |
| **C9** `test_a_template_file_is_never_examined` | Fixture: `A dev/proposals/_template.md` carrying `**Status**: proposed` **inside** the 60-line header bound plus a `## Review` section with grammar markers. No finding. | **Delete `_EXCLUDE_BASENAME`.** Red. **State the honest accounting rather than overclaiming the hazard:** the *real* `dev/proposals/_template.md` carries `**Status**: proposed` at line 123, `## Review -- {{reviewer}}` at line 313, and 7 grammar-marker instances (verified 2026-08-04) — so today the 60-line header bound *already* excludes it and the basename rule is defence in depth. The fixture deliberately places the status inside the bound so that the basename exclusion is the only thing standing between the template and a finding; otherwise the test would pass with `_EXCLUDE_BASENAME` deleted and prove nothing. |

---

### Chunk D — the suppression whitelist, and its side-door hygiene

The whitelist is a **fail-open side-door by construction**, and it gets the
treatment `scan-coverage` had to give `_SCAN_EXCLUSIONS`: every entry carries a
rationale, a stale entry trips the suite, and an entry that has become redundant
is **deleted rather than left as a latch**. Discharges **AC-R10** (suppression
half) and **AC-R10b** (the dropped third layer, disclosed).

| # | File | Change |
|---|------|--------|
| D1 | `scripts/transition_lint_whitelist.py` | `WHITELIST: dict[str, str]` — full 40-character SHA → **mandatory non-empty rationale**. A `dict`, not the `frozenset` of `scripts/quality_gate_unused_def_whitelist.py`, precisely because that file's structure makes a rationale optional (it carries them as free comments, and its own docstring says *"If R6's false-positive rate climbs … add per-symbol comments"* — an aspiration a scanner cannot check). Loading mirrors `scripts/quality_gate.py:70-83`: `spec_from_file_location` by file path, so the CLI works from any cwd. |
| D2 | `scripts/transition_lint_whitelist.py` | **Ships populated** with the two incident SHAs, each rationale naming the corpus test that keeps asserting them. This reverses the original proposal's "ships empty ... the acid test": the findings are on immutable history and can never be fixed, so leaving them live makes the one documented invocation a permanent three-line wall — the Theme-3.4 *"trains people to ignore it"* failure arriving on day one. The acid test belongs in pytest. |
| D3 | `scripts/transition_lint.py` | `scan(..., whitelist=None)` — `None` loads `WHITELIST`; an explicit `{}` **bypasses** it. The bypass is what lets Chunk E assert the incident findings while human-facing runs stay quiet. |
| D4 | `scripts/transition_lint.py` | Module comment recording, in the code and not only in the record, that **R10's third pre-registered layer — the class-level `info` downgrade — is deliberately dropped**, with the Revised proposal's argument: measured 0 false positives across the proposal's corpus meant a class-level suppressor was machinery for a failure that had not occurred, and the *Signals* section routes accumulating entries to **retiring the tool**, not to a third layer. **Row 3 of this plan's corpus table is new evidence against that argument and the code comment must say so** — a recurring false-positive *shape* did in fact appear, twelve days later. See the Maintainer fence. |

**Acceptance criteria — Chunk D.** Modelled directly on `scan-coverage`'s
`_SCAN_EXCLUSIONS` guards, including the (e)-class one that does not follow from
the others.

| test | asserts | the perturbation that makes it RED |
| --- | --- | --- |
| **D5** `test_every_whitelist_entry_has_a_nonempty_rationale` | Every value in `WHITELIST` is a non-empty string. | Add `{"<a real sha>": ""}`. Red. |
| **D6** `test_every_whitelist_entry_is_a_full_40_char_sha_that_resolves` | Every key is 40 hex chars **and** `git rev-parse --verify` resolves it. | Add a plausible-looking but non-resolving SHA. Red. Catches a typo'd or rebased-away entry, which is how a suppression silently widens. |
| **D7** `test_no_whitelist_entry_is_stale` | Every entry, with the whitelist **bypassed**, still produces at least one finding over the pinned corpus window. | Add an entry for a benign in-window SHA that flags nothing. Red. **This is the "stale entries must trip the suite" guard**: an entry suppressing nothing is a latch waiting to absorb a future regression on that commit. It is the direct analogue of `scan-coverage`'s C3(e), and like C3(e) it does **not** follow from D5/D6 — an entry can have a rationale and resolve and still suppress nothing. |
| **D8** `test_the_whitelist_suppresses_and_the_bypass_restores` | Over the pinned window: default → 0 findings; `whitelist={}` → the 3 pinned findings. | Make `scan` ignore the whitelist argument. Red in the first direction. Then make it ignore the bypass. Red in the second. Both directions must be run — a suppression test that only checks silence cannot tell suppression from breakage. |
| **D9** `test_a_whitelist_entry_cannot_suppress_a_different_commit` | Whitelisting `17b7e5c` leaves `f4a8308`'s finding intact. | Key the suppression on the abbreviated SHA prefix instead of the full 40. Red. |

---

### Chunk E — the corpus-regression tier

Cairn-repo-only and **self-skipping**: it skips, never fails, if the root is not
a git work tree or if any pinned SHA does not resolve, because a history rewrite
must not redden the suite for a reason unrelated to the code. Open question 2
was left to the Maintainer and the Revised proposal's position — keep it in
pytest, now that it pins must-SKIP entries as well — stands unless the plan
review overturns it.

| # | File | Change |
|---|------|--------|
| E1 | `bootstrap/tests/test_transition_lint.py` | The guard: `pytest.skip` when `CAIRN_ROOT/.git` is absent or any pinned SHA fails `git rev-parse --verify`. |
| E2 | `bootstrap/tests/test_transition_lint.py` | **Window 1** — `d6646a3..57d1daf`, whitelist bypassed: `scanned == 120`, `triggered == 52`, and the finding set is **exactly** `{(17b7e5c, b) ×2, (f4a8308, a)}`. Re-verified for this plan at HEAD `8f47c76`: 120 / 52 / 3, reproducing the Revised proposal to the digit. |
| E3 | `bootstrap/tests/test_transition_lint.py` | **Window 2** — `e31625c~1..57d1daf`: `scanned == 45`, `triggered == 41`, **0 findings** with the whitelist bypassed. Re-verified: 45 / 41 / 0. The must-not-flag set is asserted by construction (zero findings over a window containing all 20 named SHAs) rather than by 20 separate lookups. |
| E4 | `bootstrap/tests/test_transition_lint.py` | **Must-SKIP** — `b064576` and `d789414` are never *examined*: `triggered` does not include them. **A correction the plan must carry, verified against the working tree:** the Revised proposal justifies this by quoting `git diff-tree … -M -r b064576` → a single `R091` line, but under the **pinned** `--find-renames=100%` the same commit enumerates as `D dev/proposals/…` + `A dev/proposals/archive/…` (91 % similarity is below the 100 % threshold, because the Decision was appended in the same commit). `d789414` behaves identically. **The conclusion survives — neither commit is examined — but the mechanism is the `/archive/` exclusion, not rename-blindness.** The test asserts the outcome and the comment states the real mechanism. |
| E5 | `bootstrap/tests/test_transition_lint.py` | **Window 3** — `57d1daf..HEAD`, the corpus written since the proposal. Pinned to whatever finding set the Maintainer fence resolves to; the number to beat is **0**, and the number as-pinned-by-the-proposal is **20**. This node is the one that fails on the day the heuristics drift again, which is the whole point of having it. |

**Acceptance criteria — Chunk E.**

* The three windows reproduce from the **committed** script, not from the
  scratch prototype. The Internal panel bound the plan to exactly this: *"the
  plan should additionally be bound to re-derive the heuristics and re-run the
  dogfood numbers from the COMMITTED script … the finding set is the one claim
  no reviewer could check this round."* This is **AC-R4** and **AC-R9** landing
  together.
* **Perturbation, RUN.** Repoint window 1 at `d6646a3..HEAD`. It must fail on the
  scanned count — proving the test pins a *window*, not merely a finding set, and
  that a HEAD-relative range cannot sneak back in.
* **Perturbation, RUN.** Rename one pinned SHA to a non-resolving one. The tier
  must **skip**, not fail. Then break the guard itself and confirm it fails —
  a skip-guard that can only skip is indistinguishable from a disabled test.
* **The honest non-perturbation, recorded.** `git rev-list --merges --count
  d6646a3..57d1daf` → **0**, so no merge-blindness assertion is possible inside
  the pinned window; the property is documented in `docs/tool-usage.md` and
  asserted only by a synthetic merge fixture in Chunk A, if at all. The
  Revised proposal already corrected the original's false *"2 merge commits in
  the window"* claim; this plan does not re-introduce a window-scoped merge
  number.
* **Correction to the recorded v2 candidate.** The Revised proposal's *Known
  omissions* proposes, as a v2 candidate, letting an `R` entry into `archive/`
  trigger shape (a). Under the pinned `--find-renames=100%` those commits produce
  `D`+`A`, not `R` — so the v2 design as written would not fire. Recorded here so
  the follow-up starts from the true enumeration rather than re-deriving it.

---

### Chunk F — `docs/tool-usage.md` and the changelog

| # | File | Change |
|---|------|--------|
| F1 | `docs/tool-usage.md` | One new section in the shape of `docs/tool-usage.md:44` (`## scripts/verify_counts.py — … *(Cairn-maintainer-only)*`): what it does, the required rev-range, the exit contract (**0 on any completed scan; 2 only for a usage error; never 1**), the census line, the two-layer suppression, and — as its own paragraph — **what it does not cover**: bundling, rename-only Decisions and plan-archives, merges, rebased history, commit bodies. Placed before the existing `## See also` at `docs/tool-usage.md:147`, with a cross-link added there. |
| F2 | `docs/tool-usage.md` | A short *"how to add a whitelist entry"* paragraph carrying the proposal's own rule verbatim in substance: an entry needs a written reason **and** a paired follow-up on the heuristic; entries accumulating past a handful is the signal to retire the tool, not to grow the list. |
| F3 | `CHANGELOG.md > Unreleased > Added` | **Serialized shared file — return the text, do not edit.** One line: an advisory `scripts/transition_lint.py` that checks a commit's message claim against its lifecycle diff, cross-linking proposal and plan by stem. |

**Acceptance criteria — Chunk F.**

* `python scripts/check_cairn.py` → OK, ≥ **180** Markdown files.
* `python scripts/claim_check.py docs/tool-usage.md` and `… dev/plans/transition-lint.md` — **one file per invocation**; the checker exits 2 on more.
* `python scripts/quality_gate.py --sub neutrality` → **fail=95, info=21**, unchanged. The two new `scripts/*.py` files and `docs/` are inside its scan roots, so this is a real check that the tool names no vendor. Note the corpus tables above name reviewer *agent types* only in the deliberation record, never in shipped prose.
* `python scripts/quality_gate.py --sub redundancy` — the new script adds **no** R6 unreferenced-def finding, or any addition is a legitimate, rationale'd whitelist entry. Re-measure the baseline before the chunk; the proposal never captured it (the Internal panel's negative space #7).
* **Verify the quoted `docs/tool-usage.md` line anchors before editing.** `:44` and `:147` were verified for this plan on 2026-08-04; a sibling doc change moves them.

## Acceptance criteria

Per-chunk criteria are above; these are the plan-level deliverables.

* **The five pre-registered constraints, each explicitly discharged.**
  * **AC-R2 — rename-awareness.** `--find-renames=100%` enumeration; A15 and A16 together (A15 alone is not sufficient and the plan says so).
  * **AC-R3 — the narrowing carries the exemption model, and no vocabulary ships.** A17 (narrowing) and A18 (no exception keyword, mechanically asserted).
  * **AC-R4 — heuristics pinned against the real corpus.** Chunk E, from the **committed** script, over three windows partitioning 868 commits — and the honest report that the proposal's pinning no longer holds on the newest third.
  * **AC-R9 — corpus-derived edge cases, no speculation.** Every synthetic fixture in Chunks A–C traces to a named real commit in its own table row; `b064576` and `d789414` are **must-SKIP**, not must-not-flag.
  * **AC-R10 — advisory exit contract plus a suppression mechanism.** A9 (`main()` returns 0 on a repo *with* findings, perturbed by wiring the fail-tier), A3 (exclusion roots), D1–D9 (the whitelist and its hygiene).
  * **AC-R10b — the dropped third layer stays disclosed.** The class-level `info` downgrade is not shipped. It is stated in `scripts/transition_lint.py`'s module comment (D4), in `docs/tool-usage.md` (F1), and in the Maintainer fence below — never left to a reader to notice. A pre-registered constraint went silently unmet once in this artifact's history; it does not go quiet twice.
* **Tests that must pass.** `bootstrap/tests/test_transition_lint.py` in two tiers — synthetic (Chunks A–D) and corpus-regression (Chunk E) — plus the full suite. **Every new test has a named perturbation, and the perturbation is on the hazard, not on the test's own body.** Where a test cannot be made to fail, the plan says so instead of implying a guard exists. The perturbation ledger — the change made, the failure observed with its message, the byte-identical restore verified with `git diff <path>` empty — goes in each chunk's commit body.
* **Suite figure.** `python -m pytest bootstrap/tests` under `/Users/kendal30/conda_envs/lhm/bin/python3.13` with `PYTHONDONTWRITEBYTECODE=1`. Baseline **2 failed / 1744 passed / 0 skipped**, `as_of 2026-08-04`. The claim is *"the two known AST-attestation failures stay the only failures, 0 skipped stays 0, and collection grows by exactly the new nodes."* Not "the suite stays green" — that is false today.
* **Doc updates that must land.** All hand-authored: the `docs/tool-usage.md` section (F1, F2), the `scripts/transition_lint.py` module docstring, the per-entry rationales in `scripts/transition_lint_whitelist.py`, and the `CHANGELOG.md > Unreleased > Added` line (F3, returned not edited). No generated docs, no snippet-synced blocks.
* **Examples / smoke checks required.** `python scripts/transition_lint.py d6646a3..57d1daf` — the live dogfood from the shipped script, reproducing 120 / 52 and the census. `python scripts/transition_lint.py <plan-open>..<final>` over this plan's own commit series — each must come back clean, the same self-application the sibling used. `python bootstrap/scaffold.py --manifest` — expected **unchanged**, which is the assertion that this plan installs nothing into an adopter tree.
* **Inbound path-link updates.** None expected. `dev/PLANNING.md` and `dev/NEXT_SESSION.md` refer to plans by filename stem, not path link (`AGENTS.md` > *Shared communication files*), so the archive-move needs no edit there. Confirm at archive time rather than assume.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants, each with the chunk that enforces it.**
  * *`main()` never returns 1.* Enforced by **A9**, perturbed by wiring `return 1 if findings else 0`. **Not** enforced by `Finding` lacking a `severity` field — the Revised proposal withdrew that claim and this plan does not restore it.
  * *A rev-range that parses but does not resolve never exits 0 silently.* Enforced by **A10**, perturbed by deleting the `rev-parse --verify` call.
  * *Renames are never treated as additions; a genuine `A` is never absorbed into a rename.* Enforced by **A14**, **A15**, **A16** — the third is the one that pins the `100%` threshold rather than merely the presence of rename detection.
  * *A commit with no `A`/`M` under a trigger root produces no findings regardless of its subject.* Enforced by **A17**.
  * *The tool ships no exception vocabulary.* Enforced by **A18** (source-level) and **A19** (no cross-layer import).
  * *Widening the evidence vocabulary cannot create a finding.* Enforced by **B15**, the property test — asserted in *Scope*, tested here, because a one-directional-change claim that is only asserted is exactly the class of overclaim this repository kills proposals for.
  * *The two incident commits keep flagging.* Enforced by **E2** with the whitelist bypassed, so the acid test lives in pytest and not in every human-facing run.
  * *No whitelist entry is stale or unreasoned.* Enforced by **D5**, **D6**, **D7** — and D7 does not follow from D5/D6.
* **Public-path → test mapping.** `transition_lint.main(argv)` and
  `transition_lint.scan(rev_range, root, whitelist)` are the two public entry
  points; both are exercised **through their public paths** by
  `bootstrap/tests/test_transition_lint.py` — `main` through `argv`, `scan`
  through its signature, never through a stub of themselves. Fixtures stub the
  *repository*, never the function under test. Written as bare paths because the
  test file does not exist yet and a relative link would break
  `scripts/check_cairn.py`'s link check; **the implementing agent converts these
  to relative markdown links in the final chunk**, once the file is on disk.
* **Failure modes — all open by design.**
  * A missed real case → degrades to today's memory-enforced status quo.
  * A false positive → a printed line a human dismisses. **Twenty of them is not
    a printed line a human dismisses; it is the "trains people to ignore it"
    failure**, which is why Chunk B exists and why the fence below is not
    optional.
  * A `git diff-tree` that errors → empty enumeration, commit skipped, per
    `templates/modules/team-gated/_intent/conflict.py:767-770`.
  * An unresolvable rev-range → **closed**: exit 2 with a message (A4, A10).
  * A history rewrite → the corpus tier **skips**; if it fails instead, that is a
    bug in the guard and the tier demotes to a manual command.
* **Edge cases handled.** Empty range (A20). A `**Status**` line beyond the
  60-line header bound (C8, asserted in both directions). `_template.md` (C9).
  A hunk header with no `,count` (B4). A pure-deletion hunk (B4). Case-varied
  subjects (B7). Hyphen compounds (B10). Cairn's live "Open questions"
  vocabulary (B11).
* **Known omissions, stated rather than implied.** (a) Merge commits, squashed /
  rebased / amended history, `git notes`, and commit **bodies** — only the
  subject is parsed. (b) Bundling — the tool detects over-claiming only; an
  honest bundler is checked on its first claim, so `28816f0`'s shape passes
  clean. (c) Rename-only commits — reject/supersede Decisions and plan-archives
  are never examined; `reject`/`supersede` are dead tokens. (d) The tool is a
  heuristic over **Cairn's own** subject conventions and will not generalise
  unchanged to another tree — and row 3 of the corpus table shows it does not
  reliably generalise across twelve days of *the same* tree. (e) No human has
  read every one of the 265 triggered commits in window 3; twenty findings were
  classified by hand and the remaining 245 clean triggers were not individually
  audited for **false negatives** — the tool's silence on them is unverified.
  (f) FP-5 (an explicit negation, *"(not a Decision)"*) has no proposed fix in
  this plan and is routed to the fence.

## Verification

Run under the canonical interpreter `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(Python 3.13.x) with `PYTHONDONTWRITEBYTECODE=1`; a different minor silently
changes the suite figure. See `bootstrap/DEPENDENCY_BUDGET.md` > *The canonical
interpreter*.

<!-- cairn:slot verification-commands -->
The standing gates Cairn runs before a change lands (the same ones CI
enforces):

* **Engine suite** — `python -m pytest bootstrap/tests` (the whole
  suite; scope to `bootstrap/tests/test_<surface>.py` while iterating,
  but the full suite gates the cut).
* **Prose integrity** — `python scripts/check_cairn.py` (internal link
  / anchor resolution + claim-path check over the Markdown tree).
* **Quality gate** — `python scripts/quality_gate.py` (order-
  independence + vendor-neutrality + redundancy; `--sub neutrality`
  alone for a doctrine / template wording change).
* **Write-time claim check** — `python scripts/claim_check.py <file>` over
  each proposal / plan / doc the change authored. **One file per
  invocation** — the checker takes a single path and exits 2 (usage) on
  more, so loop rather than passing a list.

Plan-specific gates (a security-lint budget, a doc-drift gate, the
model-selection mapping check `python scripts/check_model_selection.py`)
are added per plan when the change touches that surface.
<!-- cairn:end verification-commands -->

**Plan-specific gates, added because this change touches those surfaces.**

* **The tool itself, on the pinned windows** — `python scripts/transition_lint.py
  d6646a3..57d1daf` → census `scanned 120 commits, 52 triggered, 0 findings`
  (whitelist active). With the bypass, 3 findings. And
  `python scripts/transition_lint.py e31625c~1..57d1daf` → 45 / 41 / 0.
* **The tool on itself** — over this plan's own commit series, expected clean.
  A tool that flags its own implementation arc has failed its first real test.
* **The install-contract assertion** — `python bootstrap/scaffold.py --manifest`
  diffed against a capture at the plan-open commit. **Expected empty.**
* **The gate-integrity note** — the final commit body records that
  `scripts/transition_lint.py`, `scripts/transition_lint_whitelist.py` and
  `bootstrap/tests/test_transition_lint.py` are new entries in the frozen glob
  set, so `_gate_manifest.py verify` will report three **`FROZEN-NEW`** rows
  (allowed and recorded, `bootstrap/tests/_gate_manifest.py:366`) and **zero**
  `FROZEN-MODIFIED`. **Do not re-pin.**
* **The perturbation ledgers** — per chunk, in the commit body: the change made,
  the failure observed with its message, and the byte-identical restore verified
  with `git diff <path>` (empty).

### Serialized shared files — returned, never edited in-agent

`CHANGELOG.md`, `dev/PLANNING.md`, `AGENTS.md`, `docs/DOCUMENTATION_PLAN.md`,
and `bootstrap/REANCHOR_RUNBOOK.md` are edited only at defined serialization
points. This plan touches the first two and neither is an implementing agent's
to write: the `CHANGELOG.md > Unreleased > Added` line (F3) and the one-line
`dev/PLANNING.md` row-move at plan-open are **returned as exact text** for the
orchestrator to land. `AGENTS.md`, `docs/DOCUMENTATION_PLAN.md` and
`bootstrap/REANCHOR_RUNBOOK.md` are untouched by this plan entirely.

## Maintainer fence — the two decisions this plan does not take

Neither needs a signing key, a credential, or a supervised re-pin ceremony —
**checked, not assumed**: all three code files are new, so the gate manifest
records `FROZEN-NEW` rows rather than `FROZEN-MODIFIED`, and nothing under
`bootstrap/_scaffold/` changes, so `bootstrap/REANCHOR_RUNBOOK.md` is not
engaged. The fence is about **scope authority**, not about access.

**Fence 1 — may this plan amend the accepted claim vocabulary?** The Decision's
*Accepted scope* reproduces the claim-token table, and the Revised proposal says
of that section *"Everything below is pinned here, not deferred to the plan"* —
which was the whole reason Part C was split out. This plan's corpus
re-derivation shows the table now yields 20 false positives in 333 commits.
Three sub-questions, in descending order of how safe the change is:

1. **The evidence widenings (FP-1, FP-2, FP-4 — 14 of the 20).** One-directional:
   they can only reduce findings. Read as within *"execute the decision"*, and
   Chunk B ships them subject to B15's property test. Strikeable in one line if
   the Maintainer disagrees.
2. **Deleting `accept` from the claim vocabulary (FP-3 — 5 of the 20).** This
   **narrows** the tool and edits a table the Decision quotes. The evidence is as
   clean as the evidence that retired `opening`: **0 true positives and 5 false
   positives across all 868 subjects**, because every genuine Decision subject
   also carries the word "Decision", which wins leftmost regardless. Recommended,
   **not taken here**.
3. **FP-5, the explicit negation (1 of the 20).** *"(not a Decision)"* claims a
   Decision. Options: a negation guard (new, unvalidated, n=1 design — exactly the
   move the Response identified as having produced R2), a single whitelist entry
   with a rationale, or an accepted residual documented in `docs/tool-usage.md`.
   The plan's recommendation is the **third**; the fence is that it is a
   recommendation.

**If all three are struck**, the tool ships as pinned and the whitelist takes 20
entries — which the proposal's own *Signals* section names as the trigger to
**retire the tool to a manual checklist item**. That is a coherent outcome and
the plan states it plainly rather than letting the alternative pass by default;
it is the *Alternative #1 re-weighed* question arriving once more, now with the
number attached.

**Fence 2 — R10's third suppression layer stays dropped.** The Revised proposal
argued two layers suffice on the ground that *"the measured false-positive rate
is 0 across all 538 subjects, so a class-level suppressor would be machinery for
a failure that has never occurred."* **That premise is now falsified**: five
distinct false-positive *shapes* appeared within twelve days. The plan still
does not ship the layer — a class-level downgrade would let a bad shape be
absorbed rather than surfaced, which is the wrong direction for a tool whose
value is honesty about the record — but the Maintainer should know the argument
that justified dropping it no longer holds, and that the honest replacement is
the one the Revised proposal already named: *a recurring false-positive shape is
evidence the heuristics are wrong, which should surface as a proposal rather
than be absorbed.*

## Plan review — the brief, and the one question the Decision could not have asked

*Required — **Internal**. Implementation does not start until a review has
landed under this heading.*

**Does the Internal round about to run discharge the tier? Yes, on tier — and
the plan says why rather than assuming it.** The Decision ratified
`required(Internal)` on the ground that no shipped-template, install-contract,
doctrine, or security surface is touched, and that remains true of this plan:
every file is new and repo-local, no manifest row moves, no `bootstrap/_scaffold/`
byte changes, no frozen file is modified, and no doctrine or `AGENTS.md` line is
edited. An External read is welcome and is not required. **What the round must
additionally do is answer a question the Decision could not have asked**,
because the corpus it was decided against did not yet contain the 333 commits
that break it. A reviewer who returns SHIP without engaging Fence 1 has not
discharged this round.

**The three questions this review should aim at**, in descending weight:

1. **Reproduce row 3 of the corpus table.** Build the Revised proposal's
   heuristics from its text alone and run them over `57d1daf..HEAD`. If you do
   not get 20 findings, the plan's central finding is wrong and Chunk B should
   be struck. If you do, classify them independently — do not re-trust this
   session's five-class taxonomy. Then answer Fence 1 directly: is amending the
   pinned vocabulary within *"execute the decision"*, or does it go back to the
   Maintainer?
2. **Attack the perturbation ledger, not the test list.** For each of A9, A10,
   A16, B9, B15, C6, C8 and D7, ask: *does the named perturbation touch the
   hazard, or only the test's own fixture?* Two tests shipped in this repository
   recently could not fail — an anti-drift assertion whose expected set was the
   code's own object (green for 63 days), and a security test whose fixture
   defeated its own oracle. The pairs are deliberate (B8/B9, C4/C5, C6/C7,
   D8's two directions); say whether each pair is genuinely discriminating or
   whether both halves fall to the same edit.
3. **Is the whitelist a real side-door guard or a shape borrowed from
   `scan-coverage`?** D7 is the one that matters — it is the analogue of C3(e),
   the assertion that does *not* follow from "exists and is rationale'd". Check
   that a stale entry actually reddens, and that D8 runs in both directions.

Two things a reviewer is invited to **strike** rather than accept: Chunk B's
evidence widenings, which amend a pinned table; and Chunk E's window 3, which
pins a finding set the fence has not yet resolved.

> **The landed review appends here as a `### Plan review -- <reviewer> --
> YYYY-MM-DD` sub-heading** (plus a `### Sharpening` sub-heading if it raised
> findings). **Do not rename this heading to a bare `## Plan review`** — the
> planner gate matches a section *kind*, not a review, so a bare heading would
> let an empty section satisfy it.

## Code review

*Filled in after implementation commits land.* The reviewer is **not** the
implementing agent. Begin with `**Model**: <model or tier when known; "unknown"
if not. Do not copy-paste an old model label; query and state your actual
running model identity.>` immediately below a `### Code review -- <reviewer> --
YYYY-MM-DD` sub-heading.

The falsification ledger this review owes, at minimum: independently re-run the
three corpus windows from the committed script rather than re-trusting the
implementing session's transcript; independently re-run at least three
perturbations, chosen from A9, A16, B9 and D7, and confirm each byte-identical
restore with `git hash-object` against `git rev-parse HEAD:<path>`; and confirm
by reading `scripts/transition_lint.py` end to end that no exception keyword,
no in-message opt-out directive, and no `templates/` import exists — A18 and A19
assert it, and a reviewer should check that the assertions are not themselves
hollow.

## Lasting-truth migration

*Filled in at archive time.* Per the
[Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home outside
the plan. **Pre-declared here so archive time is bookkeeping rather than
recall** — each follow-up with the home it goes to:

| deferred follow-up | durable home | why there |
| --- | --- | --- |
| **Adopter shipping (v2)** — as a `lifecycle_metrics` subcommand, not a new module; revisit when a second real tree's corpus exists. | A new row on `dev/PLANNING.md`'s deferred board, carrying the corpus-drift evidence (row 3) as the reason the deferral hardened rather than softened. | It is a scope decision awaiting an external trigger, not an open question about this code. |
| **The rename-only coverage gap (v2 candidate)** — let an `R` into `archive/` trigger shape (a) only, for `decision`/`reject`/`supersede` claims. **Its premise needs correcting first**: under `--find-renames=100%` those commits enumerate `D`+`A`, not `R`. | Its own proposal, opened only if the gap is ever felt. The corrected premise is recorded in Chunk E so the proposal does not start from the wrong enumeration. | New design validated on n=1 is what produced the proposal's own R2; it does not ride in on a plan. |
| **The symmetric bundling check (v2 candidate)** — flag when ≥ 2 distinct evidence sections each receive ≥ 3 added non-blank lines. Declined for v1; its known collision is the legitimate `## Response` + `## Revised proposal` commit, Cairn's standard shape. | Its own proposal, with the collision written into the opening. | Needs its own corpus pass. |
| **R10's class-level `info` downgrade, dropped** — and the argument for dropping it now falsified (Fence 2). | `docs/tool-usage.md` (the user-visible statement of what suppression exists) **and** a `dev/PLANNING.md` deferred row carrying the falsification. | An unmet pre-registration needs a home a reader reaches without reading an archived plan. |
| **Whether the corpus-regression tier belongs in pytest** (Open question 2, never explicitly ruled on). | Answered by the plan review; the answer is recorded in `docs/tool-usage.md`'s section on the tool's test posture. | A live posture, not a deferral. |
| **`dev/reviews/` sits outside every named boundary** (Revised proposal, Open question 5 — 4 committed panel-source files as_of 2026-07-22, 8 as_of 2026-08-04). | **Not this plan's** — it is a gap in the `AGENTS.md` approval carve-in and belongs to the Maintainer. Carried forward as a surfaced note, not a deferral this plan owns. | Naming it here so it is not lost; claiming it would be scope creep into `AGENTS.md`. |
| **The `_STAGE_COMMIT_PATTERNS` reader-fix** | Its own proposal stem `2026-07-22-claude-stage-commit-patterns`, already open. | Already homed; recorded so the archive check does not re-raise it. |

**Loop-fidelity sign-off** (see `doctrine/lifecycle.md` > *Loop-fidelity
verification*): at archive, confirm that what shipped is what the Decision
accepted — specifically, that the exit contract is exit-0-always, that no
exception vocabulary shipped, and that any amendment to the claim-token table
carries the Maintainer's answer to Fence 1 rather than an implementing agent's
judgement.

This section is append-only once written.

## Plan review -- Claude (Internal, same-agent-type; security lens) -- 2026-08-03

**Model**: claude-opus-5 (Claude Opus 5).

**Standing, stated plainly.** I am the **same agent type as the plan's author**,
in a fresh session. This round carries **no cross-type structural
independence**: the threat model I bring is the author's threat model, and a
blind spot the author has I probably share. On the plan's declared tier —
`required(**Internal**)`, floor "the same agent in a fresh session" — this round
**meets the structural floor and discharges the tier**, and the plan's own
argument for that tier (`#plan-review--the-brief-and-the-one-question-the-decision-could-not-have-asked`)
survives my check with one correction (see **[I7]**: `scripts/` *is* a shipped
destination namespace, though `transition_lint.py` still takes no manifest row).
What this round cannot do is supply a different threat model, and after **[I1]**
and **[I2]** I think an External read is now worth more than the plan judged —
the failure class turned out to be "the author's own corpus measurement did not
surface that the tool fires on the deliberation record itself", which is exactly
the class a same-type reader is worst placed to have caught by reasoning. I
caught it by *running*, not by reading.

**Dates.** The heading date is the one this round was commissioned under; the
session crossed midnight and **every measurement below is `as_of 2026-08-04`**,
taken at working-tree HEAD `eacb7dd` and later `8763eb6` (the corpus moved twice
mid-review — see **[I8]**). Interpreter throughout:
`/Users/kendal30/conda_envs/lhm/bin/python3.13`.

### Steelman

This is the best-measured plan I have reviewed in this tree, and the thing it
does best is the thing plans in this repository most often fake.

The author did not quote the proposal's corpus numbers forward. They rebuilt the
pinned heuristics and re-ran them, discovered the pinning **no longer holds**,
and led the plan with the disconfirming result instead of burying it in a
caveat. Row 2 of the corpus table is not a rhetorical claim — I reconstructed the
heuristics independently from the Revised proposal's text alone and got
**120 scanned / 52 triggered / 3 findings, with the finding identities matching
exactly** (`17b7e5c` twice, shape (b); `f4a8308` once, shape (a)). That is a
reproduction to the digit by a reader who did not see the author's code. Row 1
(`415 / 0 / 0`) and E3's window (`45 / 41 / 0`) reproduce exactly too. When this
plan says it measured something, it measured it.

The corrections it volunteers are all real and all checked out: `b064576` and
`d789414` genuinely enumerate `D`+`A` under `--find-renames=100%` and `R091`
under `-M`, so E4's correction to the Revised proposal's stated mechanism is
right and the v2-candidate premise correction that follows from it is right;
`e31625c` genuinely adds **zero** `+## Review` lines with a single
`@@ -251,6 +251,166 @@` hunk, so B5's argument that heading-presence is
worthless is not rhetoric; the deepest non-template `**Status**:` really is line
**31** and the two templates really are at **77** and **123**, so C1's 60-line
bound is a measured bound with stated headroom rather than a guess; `opening`
really has **0** occurrences across every subject in history. `dev/reviews/`
really is 8 files now, up from 4. Neutrality really is `fail=95 info=21`,
exactly. Every one of ~25 line citations I checked — `quality_gate.py` 91 / 117 /
497 / 500 / 70-83 / 817-822 / 833, `measurements.py` 54 / 142-155,
`conflict.py` 765 / 767-770 / 771-790, `_gate_manifest.py` 15-16 / 165-167 / 364
/ 366, `docs/tool-usage.md` 44 / 147, `test_quality_gate_cli.py` 29-35,
`test_upgrade.py` 1278, `doctrine/lifecycle.md` 28-30, `doctrine/proposals.md`
316-320 / 322-325 — lands on the line it claims, after the author re-anchored
them. That is not normal and it should be said.

The structural instincts are right too. Chunk A landing the exit contract
*before* any finding logic exists is the correct sequencing for an
advisory-forever tool. A15's row **admitting its own perturbation leaves it
green** and pairing with A16 is the honest move most authors skip. The
discriminating-pair discipline (B8/B9, C4/C5, C6/C7, D8 in both directions) is
the right shape. D7 is a genuine (e)-class guard that does not follow from
D5/D6. And the Maintainer fence is real fencing — the plan declines to edit a
table the Decision quotes, states the recommendation, and hands it up.

The reason the concerns below are severe is not that the plan is careless. It is
that the plan's method was good enough to get within one measurement of the
answer, and the measurement it did not take is the one that inverts the result.

### Concerns

**[I1] — Chunk C's headline result is false. A real plan-open flagged
shape (b) during this review, and appending *this review* makes the plan's own
plan-open flag too.**

Chunk C claims: *"Zero false positives across 868 commits and eight plan-opens,
measured for this plan — the strongest result in the whole exercise."* E5 says
*"the number to beat is 0."* Verification says *"The tool on itself — over this
plan's own commit series, expected clean. A tool that flags its own
implementation arc has failed its first real test."*

Measured, under the heuristics **exactly as pinned** (no Chunk B widening):

* `000e480` — `dev/plans: open planner-line-semantics`, which **landed while I
  was reviewing** — produces a **shape (b) finding**. Its added blob carries
  `**Status**: open` at line 11 (inside the 60-line bound) and the section
  `## Plan review — the brief, and why the tier is not discharged`, whose body
  cites `[E1]` while describing what the round must do. Grammar marker inside a
  `## Plan review` span at open ⇒ flagged.
* `57d1daf..HEAD` at HEAD `8763eb6` is therefore now **335 / 267 / 21 findings,
  one of them shape (b)** — not "20 findings, **zero of them shape (b)**".

The discriminator does not distinguish a *baked-in review* from a *brief that
tells a reviewer what to do*, because a brief naturally cites finding-id grammar.
Cairn's convention of writing an instructive `## Plan review — the brief …`
section at plan-open is exactly the shape that defeats it, and that convention is
spreading — this plan has such a section at `:670`.

Now the part that is not a hypothetical. I simulated the transition-lint
plan-open in a scratch repo (the plan file is still untracked, so its plan-open
commit has not landed):

| where the review section is placed | shape (b) on the plan-open |
| --- | --- |
| `### Plan review -- <reviewer>` at the very end, after `## Lasting-truth migration` | **0 findings** |
| `### Plan review -- <reviewer>` under the `## Plan review — the brief` h2, **where this plan's own instruction at `:713-717` directs** | **1 finding** |
| `## Plan review -- <reviewer>` h2 appended at the end — **the heading this round was instructed to use, i.e. the one above** | **1 finding** |

The mechanism is the `**Steelman` marker the plan's own brief asks a reviewer to
write (`:687-707` requests a Steelman by name), landing inside a span opened by
the review heading. So: **this plan's plan-open commit will be a shape-(b) false
positive of its own tool, caused by the review the plan required.** The
Verification bullet pre-registers a self-test the plan fails at commit 0.

Note also what the table shows about the detector: the verdict flips on *where a
reviewer pasted a section*. That is not a discriminator, it is a coin flip
conditioned on formatting.

What I think follows: C2's marker set cannot stand alone. The options I can see —
none of which I am asking the plan to pick blind — are (i) require the marker to
appear in a section whose heading also carries a reviewer attribution (the
`-- <name> -- <date>` shape both `17b7e5c` sections have and every brief lacks),
(ii) exclude sections whose heading contains "the brief" / "brief," (fragile,
n=2), or (iii) accept that shape (b) needs the same corpus-re-derivation Chunk B
got and give it one. Whatever is chosen, **E5's "number to beat is 0" and Chunk
C's zero-FP headline must be restated before this lands**, and the
`docs/tool-usage.md` text in F1 must not repeat the zero-FP claim.

**[I2] — "Widening the evidence side is one-directional" is false on the real
corpus, and B15 cannot catch it because it tests only the author's own
fixtures.**

Scope asserts: *"Widening the evidence side can only ever reduce findings; it
cannot make the tool flag something it did not flag before, so it cannot
manufacture a new false positive. That is a safe, one-directional change and
Chunk B ships it."* B15 is the pin: *"a property test over the corpus fixture
set: for every fixture in Chunks A–C, the finding set under B3-as-shipped is a
subset of the finding set under the three-prefix h2-only rule."*

Measured over `57d1daf..HEAD` with B3's two widenings applied (h2+h3 spans,
kind-*containing* heading match), findings go 20 → 11 — and **one of the 11 is
new**:

```
('fd6be5a', 'b', 'dev/proposals/2026-07-22-claude-transition-lint.md',
 '### Shape (b) — an open commit whose added file already carries a real review')
```

`fd6be5a` is `dev/proposals: open transition-lint`. The h3 heading contains
"review", so contains-mode makes it a review-kind section; its body is the
proposal's own defining sentence — *"a **review-grammar marker** — `[R<n>]`,
`[E<n>]`, `**Steelman`, or `**Covered**` — flag it"* — so the specification of
the markers **is** an instance of the markers. The tool's own spec text triggers
the tool, and only after the widening.

The mechanism is structural, not incidental: C2 says shape (b) scans review
section bodies *"(extended per B3)"*. In shape (a), B3's span function selects
**evidence** — widening it is monotone downward. In shape (b), the same function
selects the **detector** — widening it is monotone *upward*. The plan's
one-directional argument is sound for shape (a) and false for shape (b), and the
two share one function.

B15 as specified cannot find this. It quantifies over *"every fixture in Chunks
A–C"* — the fixture set the author built to demonstrate the widening's intended
cases. The counterexample lives in the tree, not in the fixtures. **This is the
artifact under verification supplying the material used to verify it**, in the
precise form the brief asked me to hunt for, and it is the same failure the
brief itself cites from recent history ("an anti-drift assertion whose expected
set was the code's own object"). B15 must quantify over a **corpus window**, not
over the fixtures — and when it does, it goes red as written.

**[I3] — A16's premise does not reproduce; AC-R2 is left with no test whose
named perturbation demonstrably reddens it.**

A16's named perturbation: *"Replace `--find-renames=100%` with bare `-M`. The two
files pair at ~96 % similarity, the genuine `A` is absorbed into an `R`, and the
commit silently un-triggers. Red. This is the hazard the Revised proposal pinned
the threshold against, and the *reason* the threshold is exactly `100%` and not
`-M`."*

I built the real pair the plan cites as its ground — the proposal at
`5140e21~1:dev/proposals/2026-07-08-claude-review-record-integrity.md` (654
lines) and the plan derived from it at
`5140e21:dev/plans/review-record-integrity.md` (202 lines) — in a scratch repo
with the real filenames, one commit deleting the proposal and adding the plan.
Git's rename detection **never pairs them**, at any threshold:

```
-M                    ->  A dev/plans/review-record-integrity.md   D dev/proposals/2026-07-08-...md
--find-renames=30%    ->  A ... D ...
--find-renames=10%    ->  A ... D ...
--find-renames=5%     ->  A ... D ...
--find-renames=1%     ->  A ... D ...
```

Harness control, so this is not my rig: an artificially near-identical pair in
the same rig gives `R099` under `-M` and `A`+`D` under `--find-renames=100%`. The
rig detects renames; these two files are simply not similar. Cairn plans *cite*
their proposals; they are not derived by copying them. The "~96 %" figure came
forward from the Revised proposal and appears never to have been measured.

Consequences, and this is why it is severe rather than cosmetic:

* A16 as specified **will pass under both flags** with a corpus-derived fixture.
  An implementing agent following the row will build the fixture, run the
  perturbation, see green, and — if they are not careful — record it as a pass.
* A15's row already **admits** its perturbation leaves it green (correctly; I
  confirmed the bare enumeration yields `A dev/proposals/archive/…`, which
  `_EXCLUDE_SUBSTRING` catches).
* **AC-R2 is discharged by "A15 and A16 together."** One admits it cannot fail;
  the other's stated perturbation does not fire. As written, the pre-registered
  rename constraint has no red-capable test.

A16 *can* be made red — with a synthetic fixture engineered above git's 50 %
threshold. But then it is not corpus-derived, which collides head-on with
**AC-R9** (*"every synthetic fixture in Chunks A–C is traced to a **named real
commit** in its table row"*) — and A16's row is the one row in Chunks A–C that
names no commit. Either A16 becomes an explicitly-labelled synthetic hazard test
and AC-R9 is amended to say so, or AC-R2 needs a different second test.

Minor, in the same area: the A-table column header is *"the perturbation that
makes it RED"*, and A15's cell says the perturbation does **not** make it red.
Honest, but the column header is falsified by its own cell; a reader skimming the
column will bank A15 as pinned.

**[I4] — The five-class taxonomy mis-assigns three commits, and the "6
remaining" figure that Fence 1 rests on is wrong by 5.**

I classified the 20 independently, by claim token, without reference to the
plan's taxonomy. At `57d1daf..8f47c76`: **accept 5, response 7, decision 2,
review 6.** FP-2 (7) and FP-3 (5) match the plan exactly, and B13's seven traced
SHAs are exactly my seven. The other three classes do not survive:

* **`9754635`** — *"portable-security-sweeps: require an adoption path before
  Decision"* — is traced in B14 to **FP-4** ("respond to … review"). Its subject
  contains neither `respond` nor a claim-side `review`; it is a `decision`-token
  match on a subject that names a Decision it is explicitly **not** making. It is
  a second instance of the **FP-5** shape. So FP-4 = **1**, FP-5 = **2**. Fence 1
  item 3 prices FP-5 as "1 of the 20" and recommends an accepted residual on that
  basis; at n=2, spanning two sub-shapes (negation, and forward-reference), that
  pricing changes.
* **`355aedb`** (*"close the first-use exact-byte review"*) and **`f3ddc74`**
  (*"resolve the security code review"*) are counted inside FP-1 but are
  **claim-side** shapes — "close/resolve a review" is not "add a review". Neither
  is an evidence-heading problem. `355aedb` **survives** B3's widening. `f3ddc74`
  is silenced only because its added `## Response to security code review`
  heading contains the word "review", so contains-mode counts a *Response*
  section as evidence for a *review* claim — a false negative bought, not a false
  positive fixed. Neither is named anywhere in Chunk B; B12 traces FP-1 to three
  commits while counting five.
* **`8abd453`** is one of B13's seven FP-2 commits, but its diff adds **no**
  response section at all: added lines land at post-image ~128–390 (`### Chunk G
  …`), while the post-image's `### Response -- Claude (author)` sits at line
  **905**. The h3 widening cannot reach it. It survives.

Net, measured: after everything Chunk B ships, findings are **11**, not 6.
Adding an FP-4 fix (`respond`/`responds` as response tokens) still leaves **11**
(the set shifts; `283be88` clears and another surfaces). The plan's arithmetic —
*"FP-1, FP-2, FP-4 — 14 of the 20"*, remainder 6 — is off by 5, and Fence 1's
whole cost-benefit ("if all three are struck … the whitelist takes 20 entries")
is computed on it. Fence 1 should go to the Maintainer with the measured numbers,
not these.

**[I5] — B3's "26" understates the widening's reach by threefold, and the set it
excludes is exactly the set contains-mode will wrongly absorb.**

B3 states: *"The measured gap, `as_of 2026-08-04`, is **26** h2 headings under
`dev/proposals/` + `dev/plans/` that contain 'review' and match none of
`## Review` | `## Plan review` | `## Code review`."* Read literally, that
measures **78**. The 26 is recovered only by *additionally* excluding headings
that start `## Response` / `## Revised proposal` — **52** of them, nearly all of
the form `## Response -- Claude (author, to External Security Review) -- …`.

That exclusion is exactly wrong for the rule being shipped. Under contains-mode
there is no way to know that `## Response -- … to External Security Review` is a
response and not a review: it contains "review", so it becomes review-kind
evidence. That is the mechanism that silenced `f3ddc74` in my run. So the
widening's real reach is 78 headings, of which 52 are semantically inverted, and
the plan's measurement excluded precisely those 52 before reporting.

The cost is false negatives, and nothing in the plan measures them. Known
omission (e) already concedes *"the tool's silence on them is unverified"* for
245 clean triggers; **[I2]** and this finding together mean the widening
manufactures new silence by construction. If B3 ships, it needs a kind-match that
is anchored (heading *starts with* an optional qualifier then the kind) rather
than a bare substring, and the 26/78 figure needs restating with the exclusion
made explicit.

**[I6] — The suite baseline is not reproducible at any tree state, and the
acceptance criterion built on it cannot be checked.**

Plan: *"Suite baseline: 2 failed, 1744 passed, 0 skipped, `as_of 2026-08-04`"*,
failures attributed to the two stale AST-attestation nodes (issue #1); AC at
`:503` states the claim as *"the two known AST-attestation failures stay the only
failures, 0 skipped stays 0."* Measured today, both under the canonical
interpreter with `PYTHONDONTWRITEBYTECODE=1`:

| tree state | result |
| --- | --- |
| working tree (as the plan was written against) | **19 failed, 1730 passed, 0 skipped** (148.85 s) |
| clean `--no-hardlinks` clone of HEAD `eacb7dd` | **1 failed, 1708 passed, 1 skipped** (166.64 s) |

Two things follow. First, no tree state I can produce yields 2/1744/0, so the AC
as phrased is uncheckable. Second — and this matters more — **both AST-attestation
nodes PASS at clean HEAD**. Their failure in the working tree is caused by the
concurrent workflows' uncommitted `bootstrap/_scaffold/` edits, not by a stale
baseline, so the plan's attribution to "the known stale AST-attestation nodes
(issue #1)" is wrong for the tree it measured. The clean clone's single failure
is `test_gate_preflight.py::TestPublicCli::test_check_runs_against_the_live_repo_and_reports`
— a different node entirely.

Honest caveat: the clone's 1 failure and 1 skip may be clone-environment
artifacts (that test runs against "the live repo" by name). But the plan already
knows to re-take the baseline; what it should **not** do is carry a named
attribution and an absolute AC forward. Restate the AC as "the failure *set* at
the plan's starting commit is unchanged, and collection grows by exactly the new
nodes", with the set captured at that commit rather than named here.

**[I7] — "The manifest carries no `scripts/` entry" is false, and the ground it
supports is wrong.**

Scope: *"No shipped template, no module, no install-manifest entry. Re-verified
for this plan: `python bootstrap/scaffold.py --manifest` carries no `scripts/`
entry, and Cairn's own `scripts/` tools are repo-local by construction."*

Measured: the manifest carries **24** `scripts/`-destination rows — **13** bare
`scripts/*.py` (`claim_check.py`, `link_check.py`, `content_scan.py`,
`content_scan_runner.py`, `run_security_audit.py`, `verify_stems.py`,
`check_model_selection.py`, `foldback_export_scan.py`, `foldback_suggest.py`,
`sync_doc_snippets.py`, `onboarding_activate.py`, `bootstrap_github_labels.py`,
`bootstrap_gitlab_labels.py`) plus a `scripts/_onboarding/` package.

The **conclusion survives** — the manifest is an explicit list, `transition_lint.py`
is not on it, and the expected-empty manifest diff still holds. But `scripts/` is
a **shipped destination namespace**, not a repo-local one, and three of the
reference checkers `AGENTS.md` says Cairn ships adopters live there. So:

* A1's required docstring ("Cairn-repo-local and **not installed into adopter
  trees**") is true of the *file*, not of the *directory* — it should say why
  (no manifest row), or a future reader will infer the wrong convention.
* The `scripts/*.py` frozen glob (`bootstrap/tests/_gate_manifest.py:165-167`) is
  partly shipped and partly repo-local, which makes a `scripts/*.py` addition
  slightly closer to the install contract than "no manifest row moves" conveys.

This is a one-clause fix, but it was offered as "re-verified", which is the
category of claim this repository treats as load-bearing.

**[I8] — Window 3 is HEAD-relative, which the plan forbids elsewhere; it moved
twice during this review.**

E5 pins window 3 as `57d1daf..HEAD`. Chunk E's own acceptance criteria say:
*"Repoint window 1 at `d6646a3..HEAD`. It must fail on the scanned count —
proving the test pins a **window**, not merely a finding set, and that a
HEAD-relative range cannot sneak back in."* A12's perturbation is *"give the
positional a `HEAD~20..HEAD` default. Red."* E5 is the thing both forbid.

It is not theoretical. During this session `57d1daf..HEAD` went **333 → 335**
(`000e480` and `8763eb6` landed mid-review), and the finding count went 20 → 21.
A committed node asserting `scanned == N` over that range is red on the next
commit by anyone; a node asserting only a finding set silently accretes new
corpus and stops meaning what it says. Pin window 3 to a SHA, like the other two.

Related, and checkable: the plan says the table was measured *"at HEAD
`8f47c76`"*, but `git rev-list --count 57d1daf..8f47c76` = **332**, not 333. And
`git rev-list --count 8f47c76` = **868** while `415 + 120 + 333 = 868` only holds
at `eacb7dd` (869 total, less the root). Two measurement points are conflated,
and *"the three windows partition the 868-commit history exactly"* silently drops
the root commit `0f1fc68` — the partition covers 868 of 869. The "868 subjects"
denominator used in the `opening` and `accept` token claims inherits the same
slip (both claims still hold; I re-measured `opening` = 0 occurrences).

**[I9] — The pre-registration discharge table cites implementation rows where it
means test rows, three times.**

This is the one table a reviewer checks first to confirm the five split-out
constraints are discharged. Three of its five rows point at rows that test
nothing:

* `:73` (AC-R2): *"**A6** pins `5140e21`/`57d1daf` … as must-trigger-but-not-flag"*
  — A6 is the `_triggers(entries)` implementation row. The test naming those SHAs
  is **A15**. `:496` gets it right.
* `:74` (AC-R3): *"the bright line … is a scope fence … tested by **A8**"* — A8 is
  the test-module scaffolding row (importlib loader, `pytestmark`, `_repo`
  fixture). The bright-line test is **A18**. `:497` gets it right.
* `:73` also credits **E3** with pinning *"the archive renames as
  must-produce-zero-findings"*; E3 is the `e31625c~1..57d1daf` window, and the
  `b064576`/`d789414` must-SKIP pins are **E4**.

Cheap to fix, but a Maintainer reading only the pre-registration table to confirm
R2/R3 are discharged is reading three pointers to nothing.

**[I10] — A18's token assertion collides with what AC-R3 and A5 require the file
to say.** *(design reading, not a measurement — the file does not exist yet)*

A18 asserts the source *"contains no `skip`/`exempt`/`no-lint`/`transition-lint:`
directive token"*. But A5 requires the degrade-quiet posture documented in the
module, whose natural wording is *"the commit is skipped"* (the plan's own A5
prose says exactly that), and AC-R3 requires the file to **name the exemption
source of truth** — the Revised proposal's section is titled *Exemption model*. A
bare-substring assertion goes red on the module's own required prose, and the
pressure will be to relax it until it asserts nothing — the hollow-guard failure
the brief names. Assert a directive **shape** (e.g. `#\s*transition-lint:\s*\w+`,
plus "no `argparse` flag whose name contains skip/exempt/ignore") rather than
bare tokens, and say so in the row so the implementer does not weaken it by
improvisation.

### Covered

Everything below was run for this review. The prototype is a **reconstruction —
not the author's code**: `…/scratchpad/planrev/proto_tl.py`, built from the
Revised proposal's `:1143-1231` text alone, outside the repo tree.

* **Required checkers.** `claim_check.py dev/plans/transition-lint.md` → *"OK, no
  claim-check flags"* (40 paths exempted via the file-scoped directive; the
  directive's scope reasoning in the header checks out).
  `check_cairn.py dev/plans/transition-lint.md` → *"OK — 1 Markdown file(s)
  scanned; no issues."* Both exit 0.
* **Corpus reproduction, un-widened.** Row 1 `0f1fc68..d6646a3` → **415 / 0 / 0**
  ✓. Row 2 `d6646a3..57d1daf` → **120 / 52 / 3**, findings exactly `17b7e5c`
  (`## Review -- … Internal`), `17b7e5c` (`## Review -- … External`), `f4a8308`
  (shape a) — **reproduces the plan to the digit, independently**. E3
  `e31625c~1..57d1daf` → **45 / 41 / 0** ✓. Row 3 `57d1daf..8f47c76` → **332** /
  265 / 20 (plan says 333 scanned). Row 3 at HEAD `8763eb6` → **335 / 267 / 21**,
  one shape (b).
* **Independent classification of the 20** by claim token: accept 5 / response 7
  / decision 2 / review 6. B13's seven FP-2 SHAs match mine exactly; FP-3's five
  match; the three re-assignments are in **[I4]**.
* **Widening experiments** over `57d1daf..HEAD`: contains-only → 16; h3-only →
  **20** (h3 alone fixes nothing — the two amendments are inseparable); both →
  **11**, including the new `fd6be5a`. Both widenings over the pinned window 2
  leave it at **3** findings, unchanged — E2 is undisturbed.
* **Self-application**, three placements of the review section, un-widened —
  results in **[I1]**'s table. The heading this round was told to use produces a
  finding.
* **Rename enumeration.** `b064576` → `D`+`A` at `--find-renames=100%`, `R091` at
  `-M` ✓; `d789414` identical ✓ (E4's correction is right). `5140e21` → `R100` +
  genuine `A dev/plans/review-record-integrity.md` ✓; `57d1daf` → `R100` + `A` ✓.
  Bare enumeration of `5140e21` → `A dev/proposals/archive/…`, caught by
  `/archive/` ✓ (A15's admission is right). A16 threshold probe + harness control
  in **[I3]**.
* **Suite**, both tree states, in **[I6]**.
* **Gates.** `quality_gate.py --sub neutrality` → **`fail=95 info=21`** ✓ exact.
  `check_cairn.py` (full tree) → OK, **181** Markdown files (plan says 180; its
  own `≥ 180` AC in Chunk F is satisfied). `ls scripts/*.py | wc -l` → **16** ✓.
  Neutrality scan roots include `scripts` and `docs` ✓
  (`scripts/quality_gate.py:208-211`), so F's neutrality AC is a real check.
* **Line citations**, all resolved against the working tree: `quality_gate.py` 91
  (`class Finding`), 117 (`failed`), 497 / 500 (scan-root constants), 70-83
  (`spec_from_file_location` whitelist import), 817-822 (usage-error), 833
  (`return 1 if report.failed else 0`); `measurements.py` 54 (regex text
  byte-identical to the plan's quotation), 142-155 (fixed argument vector,
  `shell=False`); `conflict.py` 765 (`check=False`), 767-770 (degrade-quiet),
  771-790 (`-z` walk), and A5's characterisation of `_rename_map_via_git` (runs
  `git diff --cached`, no rev-range, discards non-`R` at 787-789) is accurate;
  `_gate_manifest.py` 15-16, 165-167, 364, 366; `docs/tool-usage.md` 44 and 147
  (file is 152 lines); `test_quality_gate_cli.py` 29-35; `test_upgrade.py` 1278;
  `templates/core/dev/strategy/_template.md:129` (`## Open questions`);
  `dev/plans/archive/review-record-integrity.md:15`; `doctrine/lifecycle.md:28-30`;
  `doctrine/proposals.md:316-320` and `:322-325`. One soft edge:
  `measurements.py:24-27` is cited for the `shell=False` posture; the sentence
  actually spans `:27-29`, within the same paragraph.
* **Figures.** Deepest non-template `**Status**:` = **31** ✓; templates **77** and
  **123** ✓; `dev/proposals/_template.md` `## Review -- {{reviewer}}` at **313**
  ✓ with **7** marker lines ✓; `### Response` sub-headings = **7** ✓;
  `## Response to plan review` h2 = **7** ✓; `dev/reviews/` committed = **8** ✓;
  `opening` in all subjects = **0** ✓; merges = 2 (`4bf4ee4` 2026-06-09,
  `d6646a3` 2026-06-10) ✓ and `--merges --count d6646a3..57d1daf` = **0** ✓;
  `e31625c` `+## Review` count = **0** with hunk `@@ -251,6 +251,166 @@` ✓.
* **A10/A11 premises.** `measurements.py`'s regex accepts `deadbeef000..HEAD` and
  `HEAD..HEAD`, rejects `not a range`; `git rev-parse --verify deadbeef000` does
  not resolve. Both perturbations are sound.
* **Scope boundaries.** No sibling plan claims `scripts/transition_lint.py`.
  `stage-commit-patterns` touches
  `templates/modules/default-on/_lifecycle_metrics/`, its `tools/` twin, and one
  new test file — no overlap, and the plan's "imports nothing from `templates/`"
  fence holds. No `bootstrap/_scaffold/` surface. No doctrine or `AGENTS.md` line.

### Not covered / low confidence

* **False negatives are still unmeasured.** I did not audit the 245 (now 246)
  clean triggers in window 3. Known omission (e) already says so; **[I5]** makes
  the gap larger rather than smaller, and no acceptance criterion closes it.
* **The clean-clone suite figure** (1 failed / 1 skipped) may carry
  clone-environment artifacts; the load-bearing part of **[I6]** is that the AST
  nodes pass at clean HEAD, which is robust to that.
* **`quality_gate.py --sub redundancy`** baseline not taken — F's AC correctly
  notes the proposal never captured it either.
* **[I10] is a reading, not a measurement.** The file does not exist.
* **My reconstruction makes choices the proposal does not fully pin** — the
  heading-span end rule, and how "matching by containing its kind" is
  implemented. Row 2 reproducing exactly is evidence those choices match the
  author's for the *un-widened* rule; the widened results in **[I2]** and
  **[I5]** depend on my reading of B3's one-sentence spec, which is itself part
  of the finding (the spec is under-determined).
* **Fence 1 is not mine to answer** and I have not answered it. I have changed
  its inputs: the remainder is 11, not 6; FP-5 is n=2 across two sub-shapes, not
  n=1; and after **[I1]** the question is no longer only about the claim
  vocabulary but about whether shape (b)'s discriminator survives contact with
  Cairn's current plan-open convention.
* **I did not re-classify window 3's 20 by reading every commit's diff** — I
  classified by claim token and inspected the eight commits that mattered to a
  finding.

### Recommendation

**REVISE — second round required before any implementation commit.**

The plan's own gate says *"No implementation commit lands before a `### Plan
review` sub-heading is in the tree"* and its brief says *"A reviewer who returns
SHIP without engaging Fence 1 has not discharged this round."* I engaged it, and
the engagement moved the ground under it.

What must change before a second round, in order:

1. **[I1]** — restate Chunk C's zero-FP headline and E5's "number to beat is 0"
   against `000e480`, and settle what shape (b)'s discriminator becomes. Until
   then the plan's self-application test is pre-registered to fail.
2. **[I2]** — withdraw or re-scope the "one-directional" claim, and re-specify
   B15 to quantify over a corpus window rather than the author's fixtures. As
   written, B15 is a green light that cannot see its own counterexample.
3. **[I3]** — re-ground A16, and state whether it is corpus-derived or an
   explicitly-synthetic hazard test (and amend AC-R9 accordingly). AC-R2 needs at
   least one test that can be made red.
4. **[I4]**, **[I5]**, **[I8]** — correct the numbers Fence 1 and Chunk E rest
   on, and SHA-pin window 3.
5. **[I6]**, **[I7]**, **[I9]** — three factual corrections, cheap, but all three
   are claims the plan offered as re-verified.

Two things I am **not** asking for. I am not asking the plan to decide Fence 1 —
that fence is correctly placed and should stay. And I am not recommending the
plan be struck: the corpus method is sound and the disconfirming-result-first
structure is the right one. What the second round needs is the same method
applied to the two places it was not applied — shape (b)'s detector, and the
monotonicity claim.

One note on tier, offered rather than asserted. This round discharges
`required(Internal)` on its declared floor. But **[I1]** and **[I2]** are both
"the tool fires on the deliberation record that describes the tool", and I found
them by executing rather than by reading — which is exactly the kind of finding a
same-agent-type reader should not be relied on to produce twice. If the second
round is also Internal, it should be bound to **re-run**, not re-read.

*This review appended at the end of the plan per the reviewing session's
instruction, using the `## Plan review -- <reviewer> -- <date>` heading it
specified. Per **[I1]**, that heading and placement are themselves what make the
plan-open commit a shape-(b) finding under the pinned heuristics — recorded here
because it is evidence, not irony.*
