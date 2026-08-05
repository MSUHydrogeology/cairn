<!-- cairn-internal-ref-allow: doctrine/coordination.md doctrine/session-routines.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
# Next-session candidates -- Cairn

`NEXT_SESSION.md` is the cold-pickup handoff. It is rewritten from scratch by
the full-handoff owner; durable roadmap truth remains in `dev/PLANNING.md` and
the security strategy.

## Recommended starting point

<!-- cairn:slot next-start -->
**Reconcile the frozen-manifest ledger, then prepare one supervised re-pin.**
The paired `content-scan-detectors` and `separator-detection` implementations
are complete and independently security-reviewed SHIP. The final canonical
boundary is **2514 passed** under Python 3.13.13, and the template/self-hosted
scanner twins are byte-identical at SHA-256
`677d07fdb93a3978339b90f4415803069169028f7165f4c2d45641b0d2dd8ae7`.

Do not begin by asking the Maintainer to run the two-file ceremony described in
the plans. A read-only verify against `e45e1fc` reports substantial older
frozen drift, and `scripts/content_scan.py` is now part of the discovered
script set. The ceremony must be derived from current output, not inherited
from an earlier path count.

1. Run the anchored gate-manifest verifier from the trusted checkout, using
   the runbook's current trusted-repository form.
2. Reduce its output to held paths and collection regressions. Map every item
   to an implemented, independently reviewed plan; new files and added nodes
   are notes, not modified-file authorization.
3. Stop on any unreviewed or unattributable held item. Otherwise record the
   exact reviewed union and prepare the Maintainer's supervised re-pin command.
4. After the re-pin verifies clean, archive both scanner plans together and
   serialize the roadmap transition.

The Maintainer should only be brought in for the final prepared command. No
security-design choice remains for them in this scanner batch.

## Next engineering work

**1. Repair `portable-security-sweeps`.** Its Codex External security code
review is REVISE with three executable findings:

* detached reachable `HEAD` is classified as no history, allowing a partial
  scan to aggregate CLEAN;
* `probe_version()` and `screen_local_config()` execute trust roots without the
  immediate path-and-digest revalidation required by the accepted race bound;
* linked worktrees are rejected because config origin is compared to the
  `.git` file rather than Git's validated common/config directory.

Add real-Git regressions for detached/unborn repositories and linked
worktrees, plus replacement-before-probe/config tests. Re-run the focused suite
and a fresh broad boundary, then obtain a different-agent correction review.

**2. Repair `review-gate-enforcement`.** Its Codex External code review is
REVISE with two parser-language bypasses: permissive spacing/trailing-space
headings pass despite S1, and any parsed kind beginning with `Response` can
disposition findings. Give the gate a raw-line grammar equivalent to S1 and
match only the exact `Response to plan review` house form. Add positive and
negative fixtures, preserve planner-twin identity, and obtain an independent
correction review.

## Ready or queued behind them

* `release-security-bar` has an External SHIP plan review. Its missing
  serialized register row and later Maintainer-owned ref/audit remain explicit;
  SHIP did not satisfy them.
* `api-web-security-modules` and `security-verification-activation` agree on
  `policy_binding_mode: living_state`. Implement the unfenced chunks first;
  retain the ratified policy-byte boundary and the Maintainer fences exactly.
* `fork-advisory-semantics` carries an External SHIP code review, but its plan
  remains open around ceremony/serialization and the deliberately skipped
  remediation-string chunk. Reconcile it with the current AST and frozen-gate
  state before archiving.
* `stage-commit-patterns`, `transition-lint`, `security-preflight-checklist`,
  and the remaining release/security work stay on the active board. Prefer
  closing reviewed implementation before opening another scope.

## Stable state

* HEAD at handoff includes Antigravity's separator correction review
  `1c77b8d`; no push was performed.
* Last fresh full suite: **2514 passed, 0 failed, 0 skipped/xfail/xpass**, three
  third-party deprecation warnings, Python 3.13.13.
* Scanner review chain: content detectors SHIP `8ea8fad`; separator original
  review REVISE `1df178b`; correction `0d02d5d`; twin `e131b33`; correction
  review SHIP `1c77b8d`.
* No active work intents, no aging fold-back candidates, and no rate-limit
  suggestions were reported by the 2026-08-05 full-handoff routine.
* Pre-existing untracked `.claude/` and measurement material are not handoff
  work. Inspect ownership before touching them.

## Review habit to retain

Ask what supplies the material a check runs on, and execute the adversarial
case through the governing call path. This session's multi-separator bypass
and omitted scanner twin were both invisible to a narrower green result.
