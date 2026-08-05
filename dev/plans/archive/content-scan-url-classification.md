<!-- Historical review prose cites the live plan path, which ceases to resolve
     when this completed record moves to archive. -->
<!-- claim-check-allow: dev/plans/content-scan-url-classification.md -->

# Plan: classify URL scanning by adopter file role

**Source proposal**: [`dev/proposals/archive/2026-08-05-claude-content-scan-url-classification.md`](../../proposals/archive/2026-08-05-claude-content-scan-url-classification.md)
**Status**: archived
**Plan review**: not required -- the accepted proposal already contains the
External Security Review's four exact remedies and this plan introduces no new
security design; an independent code review remains required before archive
**Last update**: 2026-08-05
**Opened**: 2026-08-05

## Source proposal

The adopter-facing content-scan runner currently applies its template-scoped
URL detector to discussion prose. The accepted revision classifies only known
`dev/**` and `docs/**` paths as discussion prose; every other path remains in
the stricter class. Before that classification can mean anything, the runner's
Git query must stop inheriting ambient `GIT_*` steering and manifest roots must
stop being accepted as Git options.

## Scope

This plan implements accepted findings S1--S4 in
`content_scan_runner.py` and its behavioral tests. S2/S3 land first: a closed
child environment and fixed absolute Git executable, `--` before roots, and a
leading-dash root refusal. S1/S4 then add fail-closed role classification and
state the known bare-URL prose residual.

It does **not** change any detector, `scripts/check_cairn.py`'s Cairn-layout
classifier, audited roots, allowlists, residual baselines, module selection, or
Gate D-ON. No AST-attested scaffold-engine symbol changes.

### Documentation / doctrine surface

The shipped runner's module and function docstrings are the adopter-facing
contract. No governing doctrine changes. A serialized `CHANGELOG.md` line lands
at archive rather than riding an implementation commit.

## Sequence

```
1. Chunk A -- bind the audited set to the named repository       [251fefc]
2. Chunk B -- fail-closed URL role classification + residual    [8620d28]
3. Code review and archive serialization                        [pending]
```

### Chunk A -- the Git input boundary

| # | File | Change |
|---|------|--------|
| A1 | `templates/modules/team-gated/content_scan_runner.py` | Resolve one absolute executable Git path outside the candidate tree; invoke it through a runner-local launcher whose closed child environment drops ambient `GIT_*` and pins execution-bearing config inert. Print the resolved path once per audited-set resolution. |
| A2 | same | Select literal pathspec semantics, pass `--` before every `ls-files` pathspec, and reject a manifest root whose post-`!` value starts with `-`. |
| A3 | `bootstrap/tests/test_security_stack.py` | Real-Git alternate-`GIT_DIR` falsifier, leading-dash rejection, exact argv/environment capture, and resolved-executable report assertion. |

### Chunk B -- role classification

| # | File | Change |
|---|------|--------|
| B1 | `templates/modules/team-gated/content_scan_runner.py` | Disable `suspicious-url` only for known `dev/**` and `docs/**` paths. Root files, instruction surfaces, the roots manifest, misspellings, and unknown roles keep URL scanning enabled. |
| B2 | same | State the residual exactly: a bare hostile URL in known discussion prose is detected by neither URL nor egress detection unless a supported transfer verb is nearby. |
| B3 | `bootstrap/tests/test_security_stack.py` | Exercise instruction, known-prose, unknown-role, roots-manifest, egress-in-prose, and bare-URL residual cases through the real runner. Pin that Cairn's separate `templates/**` caller behavior is unchanged. |

## Acceptance criteria

* `bootstrap/tests/test_security_stack.py` and the focused check-cairn content
  tests pass under canonical Python 3.13.13 with no skips attributable here.
* Hazard perturbations are run for ambient `GIT_DIR`, removal of `--`, deletion
  of the leading-dash refusal, inversion of the fail-closed role default, and
  disabling URL scans everywhere.
* `python bootstrap/security_check.py` remains free of MEDIUM+ findings over the
  shipped runner, or its Bandit phase is run directly if concurrent worktree
  changes correctly block the release preflight.
* `python scripts/check_cairn.py` remains clean; the runner over its real
  declared roots is re-measured from `audited_text_files()`, not from a second
  file walk.
* **N/A examples:** this is a security-runner correction with behavioral
  fixtures, not a gallery feature.

### Author-accounting -- invariants, failure modes, edge cases

* The target repository supplies the audited set: a real alternate-`GIT_DIR`
  fixture must not redirect it, and a leading-dash policy value is refused
  before Git executes.
* Unknown roles retain the stricter detector. A synthetic unknown path and the
  roots manifest enforce the default; `devil/**` must not be confused with
  `dev/**`.
* Known prose loses only `suspicious-url`; an egress verb plus URL still flags.
  A bare URL is the accepted, printed residual.
* Git is an operator trust root validated for shape and containment, not for
  provenance. The post-validation execution race remains a named residual.

## Verification

Run with `PYTHONDONTWRITEBYTECODE=1` and
`/Users/kendal30/conda_envs/lhm/bin/python3.13`:

* `-m pytest bootstrap/tests/test_security_stack.py -q`
* the focused check-cairn content test module selected after mapping its nodes
* `bootstrap/security_check.py`
* `scripts/check_cairn.py`
* `scripts/claim_check.py dev/plans/content-scan-url-classification.md`

After implementation, append a code review and a stable-boundary verification
record before archive. Do not perform any AST or gate-manifest re-anchor in this
scope.

### Implementation verification -- Codex -- 2026-08-05

Stable code boundary: `8620d28` (Chunk A is `251fefc`). Run with canonical
Python 3.13.13 and `PYTHONDONTWRITEBYTECODE=1`:

* focused security-stack plus check-cairn content tests: **100 passed**;
* the production `audited_text_files()` / `audit()` path: **84 files, 0 flags,
  exit 0**, with Git resolved to
  `/opt/homebrew/Cellar/git/2.53.0/bin/git`;
* direct Bandit over the shipped runner: **0 MEDIUM/HIGH**, with only LOW B404
  and B603;
* `scripts/check_cairn.py`: **OK**, 182 Markdown files and 0 issues after the
  archived historical citation was recorded at `107d4e4`;
* `scripts/claim_check.py dev/plans/content-scan-url-classification.md`: **OK**;
* neutrality remains a known tree-wide nonzero baseline (**96 FAIL / 21 info**),
  with no finding in either implementation file touched here.

All five required hazard perturbations reddened the intended tests: ambient
`GIT_DIR`, removal of literal pathspec / `--`, deletion of the leading-dash
refusal, enumeration of only known instruction roles (5 failures), and URL
scanning disabled everywhere (the real-runner classification test failed).
The exact strict-default runner bytes were restored before the green pass.

The full suite is deliberately left for the post-review stable boundary so a
review correction does not incur a redundant release-scale run. No AST or gate
ceremony was performed in this scope.

## Code review

### Code review -- Antigravity -- 2026-08-05

**Model**: Antigravity (Google DeepMind)
**Verdict: SHIP**

### 1. Summary & Structural Independence
I served as the independent code reviewer for the `content-scan-url-classification` plan (`dev/plans/content-scan-url-classification.md`) at HEAD `68ca762` (covering implementation commits `251fefc` and `8620d28`). As Antigravity (a distinct agent type from the implementation author Codex), I supply the required structural independence under `doctrine/dual-review.md`.

---

### 2. Audited Criteria & Execution Evidence

1. **Git Input Boundary Hardening (Chunk A / S2 & S3)**:
   - `_resolve_git(repo_root)` resolves Git once outside the candidate tree, verifying absolute pathing, non-containment within the candidate repository root, regular file status, and execution bit (`os.X_OK`).
   - `_git_child_env()` strips ambient `GIT_*` steering variables, keeping only host-minimum environment variables (`PATH`, `HOME`, `TMPDIR`, etc.) and setting `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, and `GIT_TERMINAL_PROMPT=0`.
   - `_git_tracked()` executes Git with `--literal-pathspecs`, pinned inert configs (`core.hooksPath=/dev/null`, `core.useReplaceRefs=false`, `core.fsmonitor=false`, `core.quotePath=false`, `diff.external=""`), and option terminator `--` before pathspecs.
   - `load_audit_roots()` rejects leading-dash root entries (`rel.startswith("-")`), preventing manifest roots from being parsed as Git options.

2. **Role Classification & Fail-Closed Default (Chunk B / S1 & S4)**:
   - `_scan_urls_for_adopter_rel(rel)` disables `suspicious-url` scanning ONLY for known discussion roots (`dev/**` and `docs/**`).
   - Instruction surfaces (`AGENTS.md`, `.agents/skills/**`), root manifests (`content_scan_roots.txt`), unknown path roles (`mystery.md`), and misspelled directories (`devil/**`, `doc/**`) retain URL scanning enabled by default.
   - `TestRunnerUrlRoleBoundary` tests in `bootstrap/tests/test_security_stack.py` verify role classification across instruction, known-prose, unknown-role, roots-manifest, and egress-in-prose paths.

3. **Residual Risk Disclosure**:
   - Accurately states the known residual in `content_scan_runner.py` docstring: bare hostile URLs in known discussion prose are detected by neither `suspicious-url` nor `egress` unless a transfer verb is nearby.

4. **Execution Evidence & Verification**:
   - `PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_security_stack.py -q`: **96 passed in 15.01s**.
   - `scripts/check_cairn.py`: **OK -- 176 Markdown file(s) scanned; no issues**.
   - `scripts/claim_check.py dev/plans/content-scan-url-classification.md`: **OK, no claim-check flags**.

## Lasting-truth migration

At archive, add one `CHANGELOG.md > Unreleased > Fixed` line and remove this
plan from the active verification-cluster owner list. No new deferral is
expected.

## Archive -- Codex -- 2026-08-05

Implementation landed in `251fefc` and `8620d28`. The independent Antigravity
code review at `3355768` examined both commits, re-ran the focused security
tests and repository checks, and returned **SHIP** without a finding.

The post-review stable-boundary run at
`75da38349e0f804209234ef668aedbbd909caef1` used CPython 3.13.13 and
`PYTHONDONTWRITEBYTECODE=1`:

`python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0` completed with
**2513 passed, 0 failed, 0 skipped, 0 xfailed, 0 xpassed**, plus three
third-party deprecation warnings, in 329.44 seconds. The tracked worktree and
HEAD were unchanged across the run.

The accepted posture is now the lasting one: only known `dev/**` and `docs/**`
discussion prose omits `suspicious-url`; every unknown or instruction-like role
keeps the strict default. A bare hostile URL in known discussion prose remains
the disclosed detector residual unless a supported egress verb is nearby. Git
is validated for shape and containment but remains an operator trust root, with
the documented post-validation execution race. Review accepted both residuals.

The `CHANGELOG.md > Unreleased > Fixed` entry landed in `b92fa6c`. This archive
removes the plan from the active verification-cluster owner list. No new
deferral was created, and no AST or gate-manifest ceremony belongs to this
scope.
