# Plan: classify URL scanning by adopter file role

**Source proposal**: [`dev/proposals/archive/2026-08-05-claude-content-scan-url-classification.md`](../proposals/archive/2026-08-05-claude-content-scan-url-classification.md)
**Status**: open
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
1. Chunk A -- bind the audited set to the named repository       [commit pending]
2. Chunk B -- fail-closed URL role classification + residual    [commit pending]
3. Code review and archive serialization                        [pending]
```

### Chunk A -- the Git input boundary

| # | File | Change |
|---|------|--------|
| A1 | `templates/modules/team-gated/content_scan_runner.py` | Resolve one absolute executable Git path outside the candidate tree; invoke it through a runner-local launcher whose closed child environment drops ambient `GIT_*` and pins execution-bearing config inert. Print the resolved path once per audited-set resolution. |
| A2 | same | Pass `--` before every `ls-files` pathspec and reject a manifest root whose post-`!` value starts with `-`. |
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

## Code review

Pending independent review after Chunks A--B.

## Lasting-truth migration

At archive, add one `CHANGELOG.md > Unreleased > Fixed` line and remove this
plan from the active verification-cluster owner list. No new deferral is
expected.
