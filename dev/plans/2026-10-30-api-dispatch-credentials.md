# Plan: API dispatch credentials

**Source proposal**: dev/proposals/archive/2026-10-30-codex-api-dispatch-credentials.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Pass only the local API policy's credentials to its dispatched check so configured checks can run.

## Source proposal

The accepted heavy proposal authorizes the local API leg to receive only present credentials derived from its validated local policy, while preserving binding, isolation and fail-closed behavior.

## Scope

Change the shipped dispatcher and its tests; update the API module description if needed. No doctrine surface. Reuse `_bind_runner` and the existing policy `load_policy` and `Policy.credential_names("local")`; searches of the dispatcher, API facade and `_security_net/policy.py` found these existing binding and derivation paths. No second parser or credential registry.

The parent first binds the facade and every engine member it will execute, using the existing immutable lockfile checks, including containment and no symlinks. Only then load that bound sibling package, verify engine completeness, import its policy module, and validate the bound local policy before deriving names. Do not import the facade or execute unbound package initialization. A binding, engine or policy failure fails closed without reading credential values. Preserve the runner's own verification-before-credential ordering. If this path cannot preserve the existing binding and isolation guarantees, stop for reassessment. Account for Windows paths and subprocess behavior without introducing platform-specific shell commands.

### Documentation / doctrine surface

The shipped module describes the handoff if its current wording needs correction; no governing doctrine changes.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Bind and load the existing policy engine safely, pass the selected local credentials, and cover installed dispatch | Both plan reviews and their dispositions | Dispatcher, tests and any necessary module description |

## Acceptance criteria

**C1.** Only present names from validated local principals reach the API local child; deployed-only, unrelated and malformed names do not. Other legs receive none, and reports reveal neither names nor values. Invalid or unreadable policy and missing credentials refuse or remain incomplete without broadening the environment. Existing runner, policy, engine binding and isolation checks remain effective; tampering with engine initialization or a policy member is refused before parent execution or credential lookup. The installed actual dispatcher and runner with a two-principal loopback fixture match direct execution. Omitting a local credential and admitting a deployed-only credential each make their respective tests fail. The implementation records those mutations and the applicable checks below.

## Scope delta

**Scope delta**: preserved

## Verification

Boundary A: run `python tools/test_tiers.py for <changed paths>` and its selected tests, plus applicable prose claim, link, snippet, neutrality and `python scripts/check_cairn.py` gates. Inspect actual readers and byte pins. Include the configured installed-dispatcher and isolation nodes added to `bootstrap/tests/test_security_verification.py`, alongside existing `TestRealFacadesDrivenByTheRealDispatcher` and `test_child_env_is_minimal_and_strips_proxies_and_credentials`; use the loopback fixture in `bootstrap/tests/test_api_access_security.py` where practical. Exercise the negative engine tamper and both handoff mutations in separate copies. Map exact added nodes and any additional callers in the implementation record.

Boundary C: independent ordinary code and Security Reviews read the committed implementation and its iteration evidence, and run only targeted falsification checks. Boundary B follows review once on a clean unchanged final commit under canonical Python 3.13.x: **wide**, because this changes a credential trust boundary. Run the iteration selection for the entire reviewed range plus mapped integration/workflow tests, the API and dispatcher owning test families and applicable standing gates. Record the tested SHA and reviewed range, interpreter, clean pre/post state, commands, counts, times, token use, non-pass dispositions and omissions; `Certified by: pending`. Full-tree certification and re-anchor are separate ceremonies, not part of this change.

## Plan Review -- Codex GPT-6 -- 2026-10-30

**Reviewed commit**: 38b19294
**Obligation**: Internal (plan)
**Verdict**: PROCEED
**Elapsed**: approximately 2 minutes
**Tokens**: unknown

**Foundations**:

1. **Should it happen as framed?** Yes. The accepted proposal requires exact local-policy credentials through the actual dispatcher. At 38b19294, `_evaluate_capability` binds the runner and policy before `_run_child`, whose `_build_child_env` currently excludes those credentials. C1 preserves that binding and requires the configured installed path, not just a helper test.
2. **Best alternative.** Running the API runner directly avoids the new handoff but loses dispatcher execution. Reusing the bound policy engine and its existing credential-name derivation is the smallest path that retains the accepted isolation; a prefix allowlist would admit unrelated credentials.
3. **What would show it wrong?** A direct and dispatched configured run disagree, either required handoff mutation survives, or engine tampering executes before refusal. C1 and its verification require these checks; their results are not yet measured.

**Findings**: None. The plan maps the accepted delivery, refusal, isolation and tamper outcomes to one implementation chunk and requires exact test nodes in the implementation record.

**Coverage**: Read the committed plan, accepted proposal and dispatcher binding and child launch paths, and inspected the runner's policy and credential ordering. Did not execute implementation tests, audit every policy validation edge, or assess the boundary in depth; the separate Security Review remains owed.
