# Plan: make the `guard` citation form writable

**Source proposal**: [`dev/proposals/archive/2026-08-04-claude-board-drain-guards.md`](../proposals/archive/2026-08-04-claude-board-drain-guards.md)
**Status**: awaiting-plan-review
**Plan review**: required(Internal) — ratified in the Decision (`78e8916`)
**Last update**: 2026-08-04
**Opened**: 2026-08-04

## Source proposal

`doctrine/lifecycle.md` > "Archive precondition" requires a `guard` disposition to
name its node as `path::node`. `scripts/claim_check.py` hard-flags that form —
verified: a file citing a test node exits 1 with *"cited path does not resolve"*.
So the token's mandated citation is unwritable in any claim-checked file, in this
tree and in every adopter tree, since the checker ships. The tree is green only
because no real `guard` has been written yet.

Accepted as revised at `78e8916` after an Internal review returned **SPLIT**:
three proposed guards and a whole assessment class were removed from scope, and
this defect — surfaced as that review's bonus finding — became the proposal.

## Scope

**R1** — `claim_check` resolves a `path::node` token on its path part.
**R2** — three mutation-proven assertions in `bootstrap/tests/test_claim_check_module.py`.
**R3** — correct three `dev/PLANNING.md` rows whose stated remedies are wrong.

**Scope fence — not in this plan:**

* **Writing any `guard`.** SC3's assertion is vacuous as its row words it (the
  registry is a subset of the manifest, so deleting the union is a no-op), SC5's
  is red before it is written, and G6 is a policy question over 91 skip sites.
  All three established by execution in the Internal review; all three removed by
  the Decision and **not parked**.
* **The stale `ALLOWLIST` entry.** Real, and it edits `bootstrap/security_check.py`
  — the release-gate single source, absent from the proposal's `Touches`.
* **Any doctrine change.** The `path::node` requirement is correct as written;
  naming the node is what makes a `guard` verifiable. Only the checker moves.
* **Verifying the node half.** Out of reach for a static checker, and stated as a
  known omission rather than implied away.

### Documentation / doctrine surface

**No doctrine surface.** `doctrine/lifecycle.md` is deliberately untouched — the
rule is right and the tool is wrong. No `docs/` change: the checker's behaviour is
documented in its own module docstring, which R1 updates. One
`CHANGELOG.md > Unreleased > Fixed` line, because `claim_check.py` ships to
adopters and this changes what it accepts.

## Sequence

```
1. Chunk A -- R1 + R2: the checker fix in both twins, with its tests   [pending]
2. Chunk B -- R3: the three board-row corrections + CHANGELOG          [pending]
```

### Chunk A — the fix and its tests

| # | File | Change |
|---|------|--------|
| A1 | `scripts/claim_check.py` | A `path::node` token resolves on its **path part only**. Sits alongside the existing `:N` line-bounds handling (`_LINE_CITATION_RE`, whose `path` group is `[^:\s]+` and so cannot match a `::` token today) |
| A2 | `templates/modules/default-on/claim_check.py` | The **byte-identical twin** — same edit, same commit |
| A3 | `scripts/claim_check.py` module docstring | State what the node half is *not*: never verified |
| A4 | `bootstrap/tests/test_claim_check_module.py` | Three assertions — see *Acceptance* |

### Chunk B — the board corrections

| # | File | Change |
|---|------|--------|
| B1 | `dev/PLANNING.md` SC3 | "the guard is one assertion" → the union assertion is **vacuous**; name the provable claim |
| B2 | `dev/PLANNING.md` SC5 | "two assertions" → the entry is **already stale**; a `security_check.py` edit, not a guard |
| B3 | `dev/PLANNING.md` G6 | "one assertion" → a session hook + skip policy over 91 sites, against a documented 3-skipped config |
| B4 | `CHANGELOG.md > Unreleased > Fixed` | One line: `claim_check` accepts the `path::node` citation form |

## Acceptance criteria

* **Tests that must pass** — `python -m pytest bootstrap/tests` (full suite,
  canonical Python 3.13.x). Three new assertions in
  [`bootstrap/tests/test_claim_check_module.py`](../../bootstrap/tests/test_claim_check_module.py):
  1. `path::node` where the **path exists** → no flag.
  2. `path::node` where the **path does not exist** → **still flagged**. *This is
     the load-bearing one*: the fix must not become a bypass.
  3. The existing `:N` / `:N-M` line-bounds behaviour is **unchanged**.

  **Each is mutation-proven, and the proof is stated in advance** so a passing
  test cannot be mistaken for a working one: revert A1 → assertion 1 fails;
  weaken A1 to strip everything after the first `:` → assertion 3 fails; delete
  A1's existence check → assertion 2 fails.
* **Doc updates that must land** — the A3 docstring; `CHANGELOG.md > Unreleased >
  Fixed` (B4). Hand-authored, none generated or snippet-synced.
* **Examples / smoke checks** — `python scripts/check_cairn.py`;
  `python scripts/claim_check.py` over this plan and the archived proposal.
* **R1's own acceptance check, stated by the proposal:** deleting the
  `claim-check-allow` directive the proposal needed in order to cite the
  defective token must leave that file **clean**. This is the end-to-end proof
  and it is performed in Chunk A.
* **Changed-file set** must equal the seven paths named above, verified
  per-commit (`git show --format="" --name-only <sha>`), not by a range diff —
  a range picks up concurrent sessions' work.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants.**
  1. *The fix does not become a bypass* — a `path::node` whose path is absent is
     still flagged. **Enforcer: acceptance assertion 2.** A real mechanical
     enforcer, stated at the strength it delivers: it guards the **path** half
     and nothing about the node half.
  2. *The twins stay byte-identical* — **Enforcer:**
     [`bootstrap/tests/test_notice_install.py`](../../bootstrap/tests/test_notice_install.py)
     `::test_every_self_hosted_twin_stays_byte_identical_to_its_source`. Verified
     2026-08-04 by probe: `('scripts/claim_check.py',
     'templates/modules/default-on/claim_check.py')` is one of 41 pairs it
     iterates, so a one-sided edit fails it.
* **Failure modes.** An over-broad split (stripping at the first `:`) swallows
  line-bounds citations — **fails open**, pinned by assertion 3. A too-narrow
  regex silently keeps flagging valid `guard` citations — **fails closed**,
  caught by assertion 1 and by R1's own acceptance check.
* **Edge cases.** `path::node` with an *empty* node (`foo.py::`) — treat as not a
  node citation, so it falls through to the ordinary path check. A token with
  more than one `::` — split on the **first**, since pytest node ids nest with
  `::`. A `::` token whose path part carries a glob → already handled upstream by
  the placeholder-character rule.
* **Public-path → test mapping.** `check_path_token` and `_token_path_part` are
  the touched entry points; both are exercised through the module's public scan
  path by the three acceptance assertions above.
* **Known omissions.** **The node half is never verified** — a `guard` may cite a
  node that does not exist and nothing notices. This means `guard`'s enforcement
  is weaker than the parent proposal implied, and that is recorded rather than
  papered over. Closing it would require collection, which a static checker in a
  zero-dependency budget will not do.

## Verification

Cairn has **no CI**; every command below is run by a person or an agent at the
commit boundary and nothing enforces them automatically.

* `python -m pytest bootstrap/tests` — full suite, canonical Python 3.13.x.
* `python scripts/check_cairn.py` — prose integrity.
* `python scripts/quality_gate.py --sub neutrality` — the checker ships, so the
  neutrality surface applies.
* `python scripts/claim_check.py <file>` — one file per invocation.
* **The mutation battery** named in *Acceptance*, run and restored.

## Plan review

*Awaiting Internal plan review — implementation does not begin until this section
lands.*

## Code review

*Filled in after implementation. Reviewer is not the implementing agent.*

## Lasting-truth migration

*Filled in at archive time.*
