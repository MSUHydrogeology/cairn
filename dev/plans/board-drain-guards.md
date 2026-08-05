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

### Internal plan review -- Claude (fresh session) -- 2026-08-04

**Model**: claude-opus-5. Fresh session, no inherited context, at HEAD `da1de65`.
All commands run with `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python
3.13.13, the canonical interpreter).

Requested by the Maintainer as the `required(Internal)` plan review the Decision
ratified. Implementation has not started, so the bar is *is this correctly
specified and sequenced*, not *does the code work*. I reproduced the defect
before accepting it, then attacked the three things a pre-implementation review
can actually falsify: whether the named edit site is the right one, whether the
stated mutation battery holds, and whether the acceptance criteria are
satisfiable as written.

**Structural-independence stance.** Plan author: Claude (Strategy). Reviewer:
Claude, fresh session. Internal floor per `doctrine/plans.md` > "Reviewer
identity" -- same-agent-fresh-session is sufficient for a plan review, and this
plan carries no scientific or architectural risk that would force the External
tier. That floor is a real limit and I name it in *Not covered* below.

**Verification done before drafting.**

* **Defect reproduced independently.** A scratch file citing the mandated form
  hard-flags *"cited path does not resolve"* and exits 1 under 3.13.13. The
  plan's premise holds.
* **Read the mechanism end to end** -- `scripts/claim_check.py:369`
  (`_is_placeholder`), `:465`-`:485` (`check_path_token`), `:488`-`:522`
  (`check_line_citation`), `:583`-`:587` (`_token_path_part`), `:630`-`:670` (the
  `_scan` dispatch, glob match, and `resolves` re-check).
* **Built the fix twice and ran the plan's own assertions against it** -- a
  minimal variant (`check_path_token` only) and a two-site variant
  (`check_path_token` + `_token_path_part`) -- plus four mutants, in a scratch
  tree. Results are tabulated in the findings.
* **Swept all 266 `.md` files in the tree** with the unfixed module and both
  fixed variants: identical hard-flag sets (23 files each), zero deltas. The fix
  regresses nothing that exists today.
* **Mutation-tested the twin-parity enforcer** (finding-free -- see Steelman).
* **Grepped the board** for the three rows R3 corrects, with a multi-line regex
  (the phrases wrap across lines).
* **Ran the full suite at HEAD**: `1981 passed, 3 warnings in 330.41s` under
  3.13.13 -- the pre-implementation baseline.
* Ran `scripts/check_cairn.py` and `scripts/quality_gate.py --sub neutrality` at
  HEAD to establish their baselines too.

**Steelman.**

* **The defect is real, and the plan's diagnosis of it is exact.** A1's
  parenthetical -- `_LINE_CITATION_RE`'s `path` group is `[^:\s]+` and so cannot
  match a double-colon token -- is true by inspection (`scripts/claim_check.py:167`)
  and true empirically: the `:N` / `:N-M` behaviour is completely untouched by any
  change confined to the path-token branch. That is the single most important
  structural fact about this fix and the plan got it right.
* **Scope fidelity is clean.** I checked all eight chunk rows against the
  Decision's *"What it does not carry"* list. No guard is written; nothing lands in
  `bootstrap/tests/test_security_lint.py` or `bootstrap/tests/conftest.py`;
  `bootstrap/security_check.py` is untouched; `doctrine/lifecycle.md` is untouched.
  Nothing removed by the Decision is smuggled back and nothing is parked. The two
  additions beyond R1-R3 (the docstring, the changelog line) are each justified in
  the plan's own doc-surface section.
* **The twin-parity enforcer claim is true, and it is the one enforcer claim in
  this plan stated at exactly the strength it delivers.** Verified by mutation, not
  by reading: `_self_hosted_twins()` yields **41** pairs and the claim-check pair is
  present as the exact tuple the plan quotes. Appending one comment line to
  `scripts/claim_check.py` turns the twin node red (*"twin parity broken"*);
  restored, `cmp` clean, `git status` clean. The plan's "Verified 2026-08-04 by
  probe" is honest.
* **The glob edge case is right for the reason stated.** A double-colon token whose
  path part carries a glob is skipped upstream by the placeholder rule -- measured
  clean on the *unfixed* module, so it is genuinely handled upstream and not by
  anything this plan adds.
* **The Known-omissions paragraph is the lineage's failure mode being actively
  resisted.** "The node half is never verified" is correct, and invariant (1) is
  scoped to the path half rather than overclaimed. That instinct is right; two of my
  findings are that it was not applied consistently enough elsewhere.
* **R1's end-to-end check works mechanically.** On a scratch copy of the archived
  proposal with the directive stripped: unfixed module -> 1 hard flag, exit 1; fixed
  module -> *"OK, no claim-check flags"*, exit 0. The *idea* of the check is sound;
  [P6] is about how the plan says to perform it, not whether it proves what it
  claims.

---

**Findings.**

**[P1] (LOAD-BEARING) -- mutation 1 is false: the tests do not load A1's file, so
"revert A1 -> assertion 1 fails" cannot happen.**

`bootstrap/tests/test_claim_check_module.py:41`-`:43` sets its source to
`templates/modules/default-on/claim_check.py` -- the **A2** file. So does
`scripts/check_cairn.py:84`-`:86`. `scripts/claim_check.py` (A1) has no automated
consumer at all; it is reached only by a human typing the CLI path.

Proof by mutation: I replaced the entire contents of `scripts/claim_check.py` with
`raise RuntimeError(...)` and ran the module's own suite --

```
$ python -m pytest bootstrap/tests/test_claim_check_module.py -q
............................                    [100%]
28 passed in 0.05s
```

-- and `scripts/check_cairn.py` still imported and ran. Restored; `cmp` and
`git status --short` clean.

So reverting A1 leaves all three new assertions **green**. The only thing that
notices a one-sided edit is the twin-parity node, and what it reports is *"twin
parity broken"* -- not *"the fix is missing"*.

Relatedly, the chunk table has the twin direction backwards. `_self_hosted_twins()`
yields `(dst, src)` pairs, and the claim-check pair is
`('scripts/claim_check.py', 'templates/modules/default-on/claim_check.py')` -- the
**template is the source**, `scripts/` the derived self-hosted copy. A1 names the
derived copy as the primary edit and A2 the "twin".

*Satisfier.* Swap A1 and A2 so the row every automated consumer actually loads is
named first, and restate the mutation as: *revert the fix in
`templates/modules/default-on/claim_check.py` -> assertion 1 fails; revert it in
`scripts/claim_check.py` only -> all three assertions still pass and the
twin-parity node is the sole enforcer.* That second half is worth writing down: it
is the plan's actual protection, and it is not what the plan currently claims.

**[P2] (LOAD-BEARING) -- mutation 3 is false for the implementation A1 describes:
stripping at the first colon does not break assertion 3.**

`scripts/claim_check.py:643`-`:648` dispatches on the **full token**:
`_LINE_CITATION_RE.match(token)` routes to `check_line_citation`, everything else
to `check_path_token`. A `:N` / `:N-M` citation therefore never enters the
path-token branch, so no weakening *inside* that branch -- nor inside
`_token_path_part`, whose only call site is `:650` -- can change line-bounds
behaviour.

Measured. I implemented A1 in `check_path_token`, then applied the stated weakening
(split on `':'` instead of `'::'`) and ran the assertions:

```
assertion                                    fixed   weakened-to-first-colon
assert1  path exists      -> no flag          PASS          PASS
assert2  path missing     -> flagged          PASS          PASS
assert3a in-bounds :N     -> clean            PASS          PASS
assert3b out-of-bounds :N -> line-bounds      PASS          PASS
assert3c :N-M range       -> line-bounds      PASS          PASS
```

Assertion 3 does not fail. This matters because *"fails open, pinned by assertion
3"* is the plan's stated defence for its own named failure mode. Assertion 3 does
not hold that defence -- **the dispatch does**, and nothing in the plan pins the
dispatch.

There is exactly one implementation shape under which the stated mutation holds:
pre-stripping the token in `_scan` *before* the `_LINE_CITATION_RE` dispatch. I
built it; assertion 3b then goes clean (no flag), i.e. red. But A1 does not
describe that shape -- it points at the path-token branch alongside
`_LINE_CITATION_RE`, which is the shape where the mutation is inert.

*Satisfier.* Pin the edit site in A1 (*"inside `check_path_token`, after the
top-level-segment and default-exempt gates"*), and replace mutation 3 with one that
actually fires: *pre-strip the token at the first `:` in `_scan` before the
`_LINE_CITATION_RE` dispatch -> assertion 3 fails.* Then say plainly in the
failure-mode bullet that the dispatch, not assertion 3, is what makes the
over-broad split structurally unreachable at the specified site.

**[P3] (important) -- mutation 2 is false under its literal reading; it holds only
under a different mutation.**

"Delete A1's existence check" reads as removing
`if (repo_root / <path>).exists(): return None`. That makes `check_path_token` flag
*everything*, so assertion 2 -- which expects a flag -- still **passes**, and
assertion **1** is what fails. Measured:

```
mutant                                    assert1   assert2
delete the existence check                 FAIL      PASS
'::' branch returns None unconditionally   PASS      FAIL
```

Only the second mutant produces the stated failure, and it is a *bypass*, not a
deleted existence check -- which is, to be fair, exactly the invariant the plan
names ("the fix does not become a bypass"). The wording and the intent have come
apart.

*Satisfier.* Restate as: *make the double-colon branch return `None`
unconditionally (the bypass) -> assertion 2 fails.*

**[P4] (LOAD-BEARING) -- B3 corrects a phrase the G6 board row does not contain.
This is the tenth instance.**

`dev/PLANNING.md` carries exactly **two** "N assertion(s)" phrases. A multi-line
regex sweep over the whole file for `(one|two)\s+assertions?` returns:

* `dev/PLANNING.md:719` -- SC3, *"the guard is one assertion and should be written
  rather than re-deferred"* (the phrase wraps across `:719`-`:720`, which is why a
  line-oriented grep misses it).
* `dev/PLANNING.md:844` -- SC5, *"the guard is two assertions (key still on disk;
  key still produced by a live Bandit finding)"*.

B1 and B2 quote these accurately. **G6 has no such phrase.** Its row
(`dev/PLANNING.md:944`-`:950`) reads *"Nothing enforces the suite's `0 skipped`
invariant ... Trigger: the first suite run reporting a non-zero skip count, or the
next change to `bootstrap/tests/conftest.py`."* It states a **trigger**, not a
remedy -- so there is no wrong remedy to correct, and the Scope line's *"three
`dev/PLANNING.md` rows **whose stated remedies are wrong**"* is false of one third
of its population.

The phrase traces to the proposal's own Class A table
(`dev/proposals/archive/2026-08-04-claude-board-drain-guards.md:51`, *"one
assertion at session end"*) under a header claiming *"Rows whose **own text** names
the remedy as one or two assertions"* -- true of SC3 and SC5, false of G6. `[I4]`
demolished the substance; nobody checked whether the row said it. The plan
inherited the paraphrase and set it in a chunk cell as a quoted correction.

This is the lineage's recorded failure mode -- a claim asserted at the strength
intended rather than the strength delivered -- appearing for the **tenth** time
(the Response records `[I5]` as the eighth; commit `b8ab678` records the ninth). It
has now moved from Author-accounting slots and commit bodies into the **chunk
table**, which is the one surface an implementer executes literally.

*Satisfier.* Decide and record one of:
(a) **Drop B3** -- nothing on the G6 row is wrong -- and correct the Scope line and
the sequence text from "three rows" to "two"; or
(b) **Re-specify B3 against the row's actual text** -- the row names no revival
remedy at all, and its trigger *"the next change to `bootstrap/tests/conftest.py`"*
understates a skip *policy* over 91 sites against a documented 3-skipped config.
That is a defensible correction, but it is a different correction from the one the
cell states.
Either way, quote the row verbatim in the cell so the next reader can check it
without re-deriving it.

**[P5] (important) -- the changed-file set names a count that matches nothing.**

Acceptance says the changed-file set *"must equal the seven paths named above"*.
The chunk tables name **eight rows** across **five distinct paths**:
`scripts/claim_check.py` (A1, A3), `templates/modules/default-on/claim_check.py`
(A2), `bootstrap/tests/test_claim_check_module.py` (A4), `dev/PLANNING.md` (B1-B3),
`CHANGELOG.md` (B4). Neither eight nor five is seven.

Because the criterion is an **equality**, verified per-commit, an implementer who
follows it literally cannot satisfy it -- Chunk A will show 3 files and Chunk B
will show 2. And a count that corresponds to nothing is precisely the class of
claim this plan exists to make checkable.

*Satisfier.* Replace the count with the enumerated set, per commit (Chunk A: three
files; Chunk B: two), and state explicitly that the plan file's own status flip is
a separate lifecycle commit outside the set.

**[P6] (important) -- R1's acceptance check, as worded, asks for a subtractive edit
to an archived append-only proposal, and contradicts the plan's own changed-file
set.**

`doctrine/lifecycle.md:85` -- *"A proposal file is **append-only**: never edit a
prior section."* The single carve-out (`doctrine/lifecycle.md:91` onward) is
**additive-only**, is specifically for *inserting a `claim_check` marker line*, and
requires its own labelled `claim-marker maintenance:` commit. Deleting a
`claim-check-allow` directive from the `## Response` section of an archived
proposal is subtractive, is not a marker line, and is not covered. The plan says
this check *"is performed in Chunk A"* -- whose table does not name the proposal,
and whose changed-file criterion would be violated by touching it.

The check does not need the edit. On a scratch copy:

```
unfixed module, directive removed  -> 1 hard flag, exit 1
fixed module,   directive removed  -> OK, no flags, exit 0
fixed module,   directive present  -> OK, no flags, exit 0
```

The third line resolves this: after the fix the token no longer flags, so the
directive is simply **inert** and can stay where it is as the historical evidence
the `b8ab678` commit body says it is.

*Satisfier.* Reword to: *on a scratch copy of the archived proposal with the
directive removed, the fixed checker exits 0; the committed file is not edited and
its directive becomes inert.* If in-place removal is genuinely wanted, it is a
Maintainer call needing its own commit and its own justification against the
append-only rule -- not a line inside Chunk A.

**[P7] (important) -- assertion 1 can pass vacuously, and assertion 2 can be red
forever, depending on a fixture token the plan does not pin.**

`_is_placeholder` (`scripts/claim_check.py:369`-`:371`) skips any token containing
a space or one of `< > * { }`. Real pytest node ids carry all of these -- angle
brackets in `<lambda>` / `<locals>` ids, spaces in hand-written parametrise ids.
Measured on the **unfixed** module, in a scratch tree where the cited file does not
exist:

```
tests/unit/test_gone.py::test_x[a-b]        -> path flag   (checked)
tests/unit/test_gone.py::test_x[a b]        -> clean       (skipped: space)
tests/unit/test_gone.py::test_x[<lambda>]   -> clean       (skipped: '<')
```

So an assertion 1 written with a spaced or angle-bracketed node id is **green
before the fix** -- vacuous, and indistinguishable from a working test. An
assertion 2 written with one is **red after** it. Square brackets alone are safe:
they are not in `_PLACEHOLDER_CHARS`, and a plain parametrised id resolves
correctly under the fix (measured).

*Satisfier.* Pin the exact fixture tokens in A4 (a plain node id, no placeholder
characters), and add a fourth assertion -- or a Known-omissions line -- recording
that a node id containing a placeholder character is skipped wholesale, so the hole
is documented rather than tripped over.

**[P8] (important) -- the plan points the implementer at `_token_path_part`, which
is not in the resolution path and whose change is a latent adopter-facing
regression.**

`_token_path_part` has exactly **one** call site: `scripts/claim_check.py:650`,
inside `_scan`, feeding the allow-glob match and the `resolves` re-check at `:663`.
The hard-check resolution happens elsewhere -- `:480`
(`(repo_root / token).exists()`, on the **raw** token) and `:501`
(`_LINE_CITATION_RE.match(token).group('path')`). So the proposal's R1 premise --
*"already strips a `:N` / `:N-M` line-bounds suffix **before resolving**
(`_token_path_part`)"* -- mis-describes the mechanism, and the plan's
Author-accounting repeats it by naming `_token_path_part` a touched entry point.

Measured consequence of touching it. A document carrying a `claim-check-allow`
directive whose glob is a full `path::node` token, for a node in a file that does
not exist yet:

```
fix in check_path_token only                  -> clean      (exemption still works)
fix in check_path_token AND _token_path_part  -> path flag  (the glob no longer
                                                 matches the shortened path part)
```

No file in the tree is affected today -- I swept all 266 `.md` files with the
unfixed module and both variants and got identical hard-flag sets (23 files each,
zero deltas). This is a **forward-compatibility break for adopters**, not a current
regression, but `claim_check.py` ships and this is exactly the directive an adopter
would write for a not-yet-created guard node.

*Satisfier.* Make the fix a **single** edit in `check_path_token`, drop
`_token_path_part` from the touched set, and correct the Author-accounting
sentence. If it is touched anyway, add an assertion pinning that a full-token
allow-glob still exempts, and put the behaviour change in `CHANGELOG.md`.

This also answers A1's implicit framing: the change **is** one edit site -- but only
if the plan stops naming the second one.

**[P9] (nit) -- the doc surface is larger than "the module docstring".**

The plan asserts *"the checker's behaviour is documented in its own module
docstring, which R1 updates"* and *"No `docs/` change"*. But
`templates/modules/default-on/claim-check.md` -- shipped to adopters -- and its
self-hosted counterpart `dev/modules/claim-check.md` both describe coverage as
*"paths and line citations"* (`dev/modules/claim-check.md:17` and `:28`). They are
**not** byte-identical twins (they differ, and they are not in the 41-pair set), so
no parity obligation follows; but the shipped module doc is the adopter-facing
statement of what the checker accepts, and the `guard` form is precisely what an
adopter now needs to know is accepted.

*Satisfier.* Either add the module-doc line to the chunk table and the changed-file
set, or state explicitly that *"paths and line citations"* is judged still accurate
(a `path::node` citation is still a path claim) and why that is enough.

**[P10] (nit) -- `check_cairn.py` is listed as a smoke check with no baseline, and
it is not clean at HEAD.**

At `da1de65` it reports **3 issue(s) across 176 file(s)** -- unresolved-path flags
in `dev/plans/api-web-security-modules.md:2542` (two) and
`dev/plans/release-security-bar.md:2710` -- and still **exits 0**. All three
arrived in other plans' Response commits after `b8ab678`, so the baseline moved
between plan-open and now and will move again. An implementer told to "run
`scripts/check_cairn.py`" with no stated baseline can neither pass nor fail it --
and "check_cairn OK" asserted against a non-clean run is the precise shape of the
ninth instance this lineage recorded.

*Satisfier.* State the criterion as a delta against a dated baseline: *"3 issues,
exit 0, as_of 2026-08-04 at `da1de65`; the run must not increase it."*

**[P11] (nit) -- the edge-case list states a mechanism without its outcome, and
misses three cases; one of them qualifies invariant (1).**

* **Empty node.** The plan says `foo.py::` *"falls through to the ordinary path
  check"* but not what that yields: a **hard flag**, because the raw token is not a
  real path (measured, on all three variants). That is a defensible design choice
  for a malformed guard, but it should be stated as an outcome, not left as a
  mechanism.
* **Unlisted, measured on the fixed variant:**
  - A combined `path:N::node` token hard-flags as a *path* error and its `:N` half
    is never bounds-checked.
  - A token that is only `::` is clean (harmless).
  - **A root-level `path::node` is never checked at all.** `check_path_token`
    classifies on `token.split('/', 1)[0]` (`scripts/claim_check.py:475`), which for
    a root file is the entire double-colon token and so is never in `top_level`.
    Measured: a citation naming a root file, existing or not, is clean on the
    unfixed module **and** after the fix.

That last one qualifies the plan's single mechanically-enforced invariant.
Invariant (1) says *"a `path::node` whose path is absent is still flagged"*,
unqualified; it is true only for tokens whose first `/`-separated segment is a real
top-level entry. Given that this plan's whole subject is claims stated at their
delivered strength, the qualifier belongs in the sentence.

*Satisfier.* Add the outcome for the empty-node case; qualify invariant (1) with
the top-level-segment precondition (or extend the classifier to run on the path
part, which is a one-line widening of the same edit).

**[P12] (nit) -- neither chunk falls under the commit-approval carve-out, and Chunk
B touches a serialization-gated shared file.**

`AGENTS.md` restricts roadmap-board edits to *"defined serialization points (a
lifecycle archive, the goodnight routine, explicit instruction)"*. The Decision's
acceptance of R3 **is** the explicit instruction -- worth naming in Chunk B so the
implementer neither stalls on the rule nor quietly ignores it. And the deliberation
carve-out covers `dev/proposals/`, `dev/plans/`, `dev/strategy/` and `dev/.cairn/`
only: `dev/PLANNING.md` and `CHANGELOG.md` are outside it, so **both** chunk commits
need explicit Maintainer approval before landing.

---

**Suggested sharpening before implementation.**

1. **Rewrite the mutation battery.** Two of three stated mutations do not hold
   ([P1], [P2]) and a third holds only under a re-reading ([P3]). A battery stated
   in advance that does not fire is worse than none, because it reads as rigour. Run
   each mutation once before writing it down.
2. **Pin the edit site to `check_path_token` and drop `_token_path_part`** ([P8],
   [P2]). The fix is one edit; the plan currently names two, and the second is a
   latent adopter regression.
3. **Swap A1/A2** so the file the tests actually load is the primary row ([P1]).
4. **Settle B3** -- drop it or re-specify it against the row's real text -- and fix
   the "three rows" wording in Scope ([P4]).
5. **Replace "seven paths" with the enumerated per-commit sets** ([P5]).
6. **Reword R1's acceptance check to a scratch-copy check** and record that the
   archived directive stays and goes inert ([P6]).
7. **Pin the fixture node ids in A4** and record the placeholder-character hole
   ([P7]).
8. **Give `check_cairn.py` a dated baseline and a delta criterion** ([P10]).
9. **Qualify invariant (1)** with the top-level-segment precondition ([P11]).

**Coverage + second-round recommendation** (`doctrine/dual-review.md` >
"Recommend-and-decide"):

* **Covered.**
  * *Defect reality* -- reproduced at HEAD under 3.13.13; exit 1, *"cited path does
    not resolve"*.
  * *Edit-site correctness* -- traced all call sites of `_token_path_part` (one:
    `scripts/claim_check.py:650`) and both resolution points (`:480`, `:501`); built
    and ran both a one-site and a two-site fix.
  * *Mutation battery* -- all three stated mutations built and executed; results
    tabulated in [P1]-[P3]. A fourth mutant (pre-dispatch strip) built to find the
    shape under which mutation 3 *would* hold.
  * *Acceptance-assertion sufficiency* -- all three run against unfixed, fixed, and
    four mutants. Assertion 2 is green on the **unfixed** module, so assertion 1 is
    the only fix-detecting assertion of the three; assertion 2 is a regression
    guard, which is what the plan intends but not what "the load-bearing one"
    implies.
  * *Twin-parity enforcer* -- verified by mutation: 41 pairs, exact tuple present,
    node goes red on a one-sided edit, restored clean.
  * *Regression surface* -- all 266 `.md` files swept under three module variants;
    zero deltas.
  * *Edge cases* -- twelve token shapes measured across three variants, including
    the four the plan names.
  * *Board-row claims* -- multi-line regex sweep of `dev/PLANNING.md`; SC3 and SC5
    verified verbatim, G6 disproven.
  * *Scope fidelity* -- all eight chunk rows checked against the Decision's
    exclusion list; clean.
  * *Append-only compliance* -- `doctrine/lifecycle.md:85` and its carve-out read in
    full against what R1's acceptance check asks for.
  * *Suite baseline* -- `1981 passed, 3 warnings in 330.41s` at `da1de65` under
    3.13.13. Green before implementation, so any failure afterwards is this plan's.
* **Not covered / low confidence.**
  * **I am the same agent type as the plan's author.** This is the Internal floor,
    and it does not discharge an External read. The specific blind spot to worry
    about is that I found the same *class* of error the author's own Internal review
    found (a claim stronger than its delivery) -- which may mean I am
    pattern-matching the lineage's known failure rather than looking for an unknown
    one.
  * **Adopter-tree behaviour is inferred, not measured.** My sweep covers Cairn's own
    266 `.md` files. [P8]'s regression is reasoned from the code path plus a
    synthetic reproduction, not observed in a real adopter tree -- none is available
    here.
  * **I did not evaluate whether the CHANGELOG wording (B4) is right**, only that the
    target section exists (`CHANGELOG.md` > Unreleased > Fixed is present).
  * **The node-half omission is accepted, not tested.** I confirmed no static check
    can reach it in a zero-dependency budget, but I did not explore whether a cheaper
    partial check (e.g. grepping the cited file for the node name) would be worth it.
    That is a design question this review did not open.
  * **`quality_gate.py --sub neutrality` was run but not read closely** -- it emits
    `info` lines for vendor-ok-blocked tokens in existing doctrine. I did not
    establish whether it has a failing threshold this change could cross.

**Recommendation: a second cross-type pass is not recommended before
implementation.** The findings are mechanical and I resolved every one by execution
rather than judgement, so a different agent type has little to add that a re-run
would not also produce. The negative space that would justify escalation --
adopter-tree behaviour and the node-half design question -- is not what a plan
review resolves: the first is empirical and belongs to the code review, the second
is a separate proposal if anyone wants it. The declared `required(Internal)` tier is
discharged by this pass once its findings are dispositioned.

**Verdict: REVISE.**

The design is right and should not be re-litigated: the defect is real, the fix is
correct, it is genuinely one edit site, and the scope fence honours the Decision
exactly. What needs correction before implementation is the **specification around**
that fix -- a mutation battery of which two thirds does not fire ([P1], [P2]), a
chunk cell correcting a phrase that is not on the board ([P4]), an acceptance
criterion that cannot be met as counted ([P5]), and an end-to-end check that as
worded asks for an edit the append-only rule forbids ([P6]). None of these is a
reason to reopen the Decision. All of them are reasons not to start typing yet.

## Code review

*Filled in after implementation. Reviewer is not the implementing agent.*

## Lasting-truth migration

*Filled in at archive time.*
