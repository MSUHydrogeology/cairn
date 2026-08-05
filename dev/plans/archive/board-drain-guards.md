# Plan: make the `guard` citation form writable

**Source proposal**: [`dev/proposals/archive/2026-08-04-claude-board-drain-guards.md`](../proposals/archive/2026-08-04-claude-board-drain-guards.md)
**Status**: archived
**Plan review**: required(Internal) — ratified in the Decision (`78e8916`)
**Last update**: 2026-08-05
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

### Code review -- Claude (fresh session) -- 2026-08-05

**Model**: claude-opus-5. Fresh session, no inherited context. Reviewer is **not**
the implementing agent, per `doctrine/plans.md` > "Code review". Every command
below ran under `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python
**3.13.13**, the canonical interpreter). Commits under review: `48b05f1`
(Chunk A), `f42db96` + `5e10623` (Chunk B), `fc32dd9` (status flip).

**Substrate -- and why it is the finding.** The Maintainer's working tree carries
a concurrent session's *uncommitted* work, including a heavily modified
`bootstrap/tests/test_security_stack.py`. So every figure below was measured in a
**detached git worktree at `fc32dd9`**, plus three more worktrees for the mutation
battery. All four were restored and removed; `git status --short` was empty in each
before removal, and the main tree is untouched by this review.

---

**Steelman -- what reproduced exactly, by execution.**

* **The mutation battery is real and fires as the commit body states.** Run
  independently against both twins in a clean worktree, each mutation applied and
  restored:

  ```
  BASELINE (unmutated)                              42 passed
  M1  revert the check_path_token change         -> 2 failed  (assertions 1 and 4)
  M2  the `::` branch returns None unconditionally
      (the faithful bypass mutant)                -> 1 failed  (assertion 2)
  M3  pre-dispatch strip at the first `:` in _scan-> 2 failed  (assertion 3 plus the
                                                     pre-existing
                                                     test_directive_does_not_silence_local_line_bounds)
  M8  one-sided twin edit (scripts/ side only)   -> 1 failed  (the twin-parity node)
  RESTORED                                          42 passed, git status clean
  ```

  This matches `48b05f1`'s stated battery node-for-node, including its honest
  correction to plan-review [P2] (one pre-existing test *did* pin the dispatch).
  The load-bearing assertion,
  `bootstrap/tests/test_claim_check_module.py::test_node_citation_with_absent_path_is_still_flagged`,
  is the one and only node the bypass mutant reddens.
* **The bypass invariant holds.** I ran 28 token shapes through the pre-fix and
  post-fix modules side by side against the real repo root. Every delta is
  FLAG -> clean; **not one is clean -> FLAG and not one is FLAG -> EXEMPT**. The
  fix is strictly flag-reducing, which is also true by construction: the only
  input on which `target.split('/', 1)[0]` differs from `token.split('/', 1)[0]`
  is a token whose path half has no `/`, and a single-segment path half is in
  `top_level` only if it exists.
* **`_token_path_part` being left untouched is verified, not just reasoned.**
  The [P8] adopter case measured on both modules: a document-scoped
  `claim-check-allow` glob equal to a full `path::node` token, for an absent path,
  **still exempts** after the fix. The exempted set cannot grow, because
  `_scan`'s glob branch runs only on tokens that already flagged, and the flag set
  shrank. Separately confirmed that the glob still does **not** silence an
  out-of-range line-bounds citation into a real file.
* **Twin discipline.** `cmp` byte-identical; `_self_hosted_twins()` yields **41**
  pairs and the claim-check pair is present; mutation M8 above proves
  `bootstrap/tests/test_notice_install.py::test_every_self_hosted_twin_stays_byte_identical_to_its_source`
  catches a one-sided edit.
* **The live invariant is correct now and cannot drift silently.**
  `wc -l` on both copies = **869**, and the registry
  (`scripts/measurements.py:220`) targets
  `templates/modules/default-on/claim_check.py`, so `docs/tool-usage.md:76` is
  right. Perturbing it to 870 makes `scripts/check_cairn.py` print
  `[count-drift] ... doc says 870, measured 869 today -- DRIFT` and **exit 1**.
  Named trigger, opened and confirmed: a person running `check_cairn` (Cairn has
  no CI). Restored.
* **`check_cairn` OK across 177 files reproduces**, and this is worth saying
  plainly: plan-review [P10] warned that asserting "OK" against a non-clean run
  would be the ninth instance recurring. It did not recur. Measured `OK, no
  issues` in the real tree; the 177 count is exact (`check_cairn --root` against a
  clean `fc32dd9` worktree reports `177 file(s)`).
* **R1's acceptance check passes exactly as re-specified by [P6].** On a scratch
  copy of the archived proposal with the directive stripped: pre-fix module -> 1
  hard flag, exit 1; post-fix -> `OK, no claim-check flags`, exit 0. The committed
  file with its directive intact is also clean -- the directive is now inert,
  which is the correct end state for an append-only record. The archived proposal
  was not edited.
* **Decision fidelity is clean.** `bootstrap/security_check.py`,
  `doctrine/lifecycle.md`, `bootstrap/tests/conftest.py` and
  `bootstrap/tests/test_security_lint.py` are untouched by all three implementing
  commits. No `guard` disposition was written anywhere. `dev/PLANNING.md` carries
  **76** top-level rows before and after `5e10623` -- none added, none removed.
  **G6 is genuinely untouched**: `git diff 99c8d55 fc32dd9 -- dev/PLANNING.md`
  shows no change in that region, and the row's live text states a *Trigger* and
  prescribes no remedy, exactly as [P4] established.
* **The intent override is properly recorded and properly bounded.** Verified
  against `dev/intents.jsonl`, not just the commit body: session
  `codex-93c2a217`'s claim at `09:16:47` really does list `dev/PLANNING.md` with
  the action *"consolidate security strategy and cluster roadmap"*, quoted
  accurately; the implementing session held its own earlier claim on the same file
  from `07:58:10`; and `5e10623` released that claim at `09:27:13`. The override
  was one commit, the concurrent claim was honoured first, the patch was held
  outside the tree, the file was reverted so the other session was not working
  around uncommitted edits, and the authorization is quoted verbatim and visually
  isolated. This is the standard the rest of the record should be held to.

---

**Findings.**

**[C1] (LOAD-BEARING) -- "full suite 1985 passed" is not this change's suite. 22
of those 1985 tests are a concurrent session's uncommitted work, and the figure
cannot be reproduced from the committed tree. This is the eleventh instance.**

Measured in a clean detached worktree at `fc32dd9`:

```
fc32dd9, clean worktree   1963 collected -> 1962 passed, 1 skipped in 299.45s
da1de65, clean worktree   1959 collected            (the pre-implementation base)
main working tree         1985 collected
delta main - fc32dd9      22 nodes, ALL in bootstrap/tests/test_security_stack.py
                          (uncommitted; mtime 2026-08-05 09:15:03)
```

Chunk A landed at **09:22:00** -- seven minutes after that file was last written by
the other session. The 22-node delta is exact and one-directional: `comm` reports
**0** nodes present in the committed tree but absent from the working tree.

The single skip is
`bootstrap/tests/test_foldback_suggest.py::TestLiveLedgerSmoke::test_live_ledger_parses_without_error`,
which skips only because a detached worktree is not sited beside the
modflow_tools sibling checkout; it **passes** in the main tree. So the honest
figure for the committed tree is **1963 passed**, not 1985.

Two things make this worse than a transcription slip. First, `1985` cannot be a
true pytest line for *any* tree state: the working tree collects 1985 and one node
skips in it too unless the sibling is present, so the number was read from a
contaminated collection. Second, **the plan review's own baseline carries the
identical contamination**: `1959 + 22 = 1981`, exactly the *"1981 passed"* it
recorded at `da1de65`. Both endpoints were off by the same +22, so the `+4` delta
matching the four new assertions *self-validated*, and that is precisely why
nobody caught it. A green suite was asserted over 22 tests that are not in this
repository, and conversely a failure in that other session's unlanded work would
have blocked this commit for reasons unrelated to it.

*Satisfier.* Correct the figure in the plan's verification record to **1963
passed under 3.13.13 at `fc32dd9`**, and state the measurement substrate. Standing
habit worth adopting: when the shared tree is dirty with another session's work,
measure the suite at the commit (a detached worktree), not in the working tree --
otherwise "full suite green" is a claim about the machine, not about the change.

**[C2] (important) -- invariant (1) is still stated unqualified, and it has a
second exception the plan does not record: 129 of this repository's own 1963 test
node ids are skipped wholesale, path check and all.**

`_is_placeholder` (`templates/modules/default-on/claim_check.py:377`) drops any
token containing a space or one of `_PLACEHOLDER_CHARS` (`:180`). Real pytest node
ids carry these constantly. Measured on the fixed module, against the real root,
for a path that does **not** exist:

```
bootstrap/tests/no_such_file.py::test_x         -> FLAG   (invariant holds)
bootstrap/tests/no_such_file.py::test_x[a-b]    -> FLAG   (brackets are safe)
bootstrap/tests/no_such_file.py::test_x[a b]    -> clean  (space)
bootstrap/tests/no_such_file.py::test_x[<lambda>] -> clean  (angle brackets)
bootstrap/tests/no_such_file.py::test_x[{a}]    -> clean  (braces)
```

I counted the exposure rather than asserting it: of the **1963** node ids this
suite collects, **129 (6.6%)** contain a space or a placeholder character -- e.g.
the parametrised ids in `bootstrap/tests/test_fork_advisory.py`. A `guard` citing
any of those 129 gets **no path check at all**, so the plan's single
mechanically-enforced invariant -- *"a `path::node` whose path is absent is still
flagged"* -- is silently inapplicable to them.

Plan-review [P7] measured this exact behaviour and offered two satisfiers: pin the
fixtures **and** record the hole. The Response took the first and dropped the
second; assertion 4 proves brackets are safe, which is a different claim. The
docstring added by A3 says the node half is never verified, and says nothing about
the node half being able to suppress the *path* half.

*Satisfier.* One Known-omissions line in the plan and one sentence in both copies'
`_node_citation_path` docstring: a node id containing a space or a
`_PLACEHOLDER_CHARS` member exempts the whole token upstream, so invariant (1)
covers node ids free of those characters. Optionally one assertion pinning the
exemption so it is visible rather than incidental.

**[C3] (important) -- the node branch resolves with `exists()`, so a `path::node`
whose path half is a *directory* now passes. It flagged before the fix, and the
sibling line-bounds branch deliberately requires a file.**

Measured, pre-fix vs post-fix, against the real root:

```
bootstrap/tests::test_x        FLAG  ->  clean     <-- widened by this change
bootstrap::test_x              clean ->  clean     (top-level dir; unchanged)
```

`check_path_token` resolves with `(repo_root / target).exists()`
(`templates/modules/default-on/claim_check.py:509`), while `check_line_citation`
resolves with `not target.is_file()` (`:534`) precisely because a bounds claim
against a directory is meaningless. The same reasoning applies here with more
force: a pytest node id is `file.py::node`, never `dir::node`, so this is a
fail-open widening in the exact surface the plan exists to police. It is not in
the plan's edge-case list.

The mutation `exists()` -> `is_file()` leaves both
`bootstrap/tests/test_claim_check_module.py` and
`bootstrap/tests/test_notice_install.py` fully green, so nothing pins the
behaviour in either direction.

*Satisfier.* Require `.is_file()` on the resolution when the token *is* a node
citation (i.e. when `_node_citation_path` returned a shortened path), leaving the
plain-path branch on `.exists()` so directory citations keep working, plus one
assertion that a directory path half is flagged.

**[C4] (important) -- three of the four decision points inside
`_node_citation_path` are invisible to the full 1963-node suite.**

I ran the **whole** suite under two further mutations, in isolated worktrees:

```
mutation                                          full suite        silently changes
partition('::') -> partition(':')                 1962 passed, 1 sk  `bootstrap/tests:junk` FLAG->clean
                                                                     `<real>.py::`         FLAG->clean
drop `and node` from the guard (:488)             1962 passed, 1 sk  `<real>.py::`         FLAG->clean
drop `and path_part` from the guard (:488)        green (targeted)   nothing -- inert clause
```

Both full-suite runs are byte-identical to the unmutated baseline. So the single
most important detail of the fix -- that it splits on `::` and not on `:` -- is
**not pinned by any test**; assertion 3 pins the `_scan` dispatch, which is a
different property (M3 above fires it; M4 here does not). The empty-node
behaviour the docstring documents (`t.py::` falls through to the ordinary path
check, and hard-flags even when the file exists -- measured) is likewise
unpinned, and the `and path_part` clause is behaviourally inert on every input I
could construct.

This is not a defect in what shipped; it is the "which test fails when I delete
it" answer coming back *none* for three of the four branches in the new helper.
Given the plan's own framing -- a battery stated in advance so a passing test is
not mistaken for a working one -- the gap belongs on the record.

*Satisfier.* One assertion that a single-colon suffix on a non-line-bounds token
still flags (kills the `partition(':')` mutant) and one for the empty-node case
(kills the `and node` mutant); or delete the inert `and path_part` clause and
record the other two as accepted, unpinned branches.

**[C5] (important) -- the changed-file set is six, the plan says five, and the
plan also says "No `docs/` change". The deviation is recorded only in commit
bodies, and the plan is the artifact that gets archived.**

`48b05f1` touched four files including `docs/tool-usage.md`; the revised
acceptance criteria name five distinct files as an **equality** verified
per-commit, and the plan's documentation-surface section states *"No `docs/`
change"*. Both are now false. `48b05f1` and `fc32dd9` both disclose this and say
it will be *"corrected at archive"* -- which is honest, and is why this is not
load-bearing. But the Registered-Report discipline judges the implementation
against the **locked plan**, and a cold reader checking acceptance criteria opens
the plan, not `git log`. Plan-review [P5] already had to fix this same criterion
once ("seven paths" matching nothing); it is now wrong again in the same slot.

*Satisfier.* The sharpening/archive commit updates the revised changed-file set to
the six actual paths and replaces "No `docs/` change" with the registered-invariant
reason `docs/tool-usage.md` had to move.

**[C6] (nit) -- Chunk B stamps a date on the shared board that matches no commit,
and the status flip did not bump the plan's own `Last update`.**

Every commit in this lineage landed on **2026-08-05**: `99c8d55` 07:59 (proposal
open) through `fc32dd9` 09:27. Nothing in it happened on 2026-08-04. Yet the two
rows `5e10623` wrote into `dev/PLANNING.md` announce **"Remedy corrected
2026-08-04"**, and `fc32dd9` edited the plan (status, commit hashes) while leaving
`**Last update**: 2026-08-04` -- a field `doctrine/plans.md` > "Mutability rule"
names as mutable-in-place alongside `Status`. The lineage-wide 08-04 headers are
inherited and out of this pass's scope; the board rows are not -- `dev/PLANNING.md`
is a long-lived shared communication file, and a future reader reconciling those
rows against `git log` will find no 08-04 commit that touched them.

*Satisfier.* Reword to *"Remedy corrected 2026-08-05 (established by the
2026-08-04 Internal review)"* at the next serialization point, and bump the plan's
`Last update` at archive.

**[C7] (nit) -- [P9] was accepted but not satisfied: the adopter-facing module doc
still understates what the checker accepts.**

`templates/modules/default-on/claim-check.md:28` -- the doc that ships -- and its
self-hosted counterpart `dev/modules/claim-check.md:28` both still say the
installed checker covers *"paths and line citations"*, with no mention of node
citations. The Response answered [P9] with *"the shipped module docstring also
describes coverage and is updated with A3"*; that is the `.py` module docstring, a
different artifact from the one [P9] named. [P9] offered two exits -- add the line,
or state that the existing wording is judged still accurate and why -- and neither
was taken.

*Satisfier.* One clause in both module docs, or an explicit recorded judgement
that a `path::node` citation is still "a path claim" and the wording stands.

**[C8] (nit) -- two small record inaccuracies.**

* The plan's corrections section says *"Invariant (1) is qualified per [P12]"*.
  The root-level finding is **[P11]**; [P12] is the commit-approval carve-out.
* That qualification's wording -- a root-level `path::node` *"never reaches
  `check_path_token`'s repo-path branch at all"* -- is no longer true after the
  fix: `AGENTS.md::test_x` now does reach it and resolves. The *substance* is
  correct and I verified it (`NOSUCH_ROOT.md::test_x` is clean before and after,
  so an absent root-level path is still never flagged); only the mechanism
  sentence went stale against the code that shipped.
* `CHANGELOG.md` ends the new entry *"From the archived plan
  `board-drain-guards`"*. The plan is not archived -- it is at
  `dev/plans/board-drain-guards.md`, status `review`. It is also the only
  occurrence of that phrasing in the whole changelog, so it is not an existing
  house convention being followed.

*Satisfier.* Fix the finding number; restate the root-level qualification against
the shipped code; drop or re-tense "archived" in the changelog line before release.

---

**Falsification ledger.**

* **Surfaces probed.** `_node_citation_path` and `check_path_token` at every
  branch; the `_scan` dispatch and its allow-glob / `resolves` re-check;
  `_is_placeholder`; `_is_default_exempt` (which now sees the path half rather
  than the raw token); `check_line_citation` as the untouched sibling; the twin
  pair; the `docs/tool-usage.md` registered invariant; the intent ledger; the
  board diff; the Decision's exclusion list.
* **Negative / edge-case attempts.** 28 token shapes measured pre-fix vs post-fix
  against the real repo root, including empty node, empty path, bare `::`, nested
  `a::b::c`, combined `path:N::node`, trailing `::`, triple colon, root-level
  present and absent, directory path halves at two depths, bracketed and
  space/angle/brace-bearing node ids, Windows-style separators, `..` traversal,
  and a default-exempt prefix with a node suffix. Five glob cases on the
  exemption path. Every one is tabulated above or in the findings.
* **Attempts to break the bypass invariant.** I tried to construct a token that a
  `claim-check-allow` glob exempts *after* the fix but would not have exempted
  before, and could not -- and the reason is structural, not luck: the glob branch
  runs only on already-flagged tokens, `_token_path_part` is untouched, and the
  flag set strictly shrank. I also probed whether the fix widens filesystem reach
  (an absolute path in the path half, `/etc/passwd::x`, classifies out at
  `first not in top_level`; a `..` traversal behaves identically pre- and
  post-fix and is a read-only `exists()`). No new reach.
* **Verification run.** Full suite x3 (baseline + two full-suite mutants) and one
  collect-only at `da1de65`, all in clean detached worktrees under 3.13.13;
  targeted suite x9 for the mutation battery; `check_cairn` in the real tree, in a
  clean worktree, and under a perturbed invariant; `verify_counts`;
  `quality_gate.py --sub neutrality` (info lines only, all pre-existing
  `vendor-ok` blocks in `doctrine/consolidation-review.md`; nothing this change
  added); `claim_check` on the plan and on the archived proposal; `cmp` on the
  twins; the R1 scratch-copy check in three configurations.
* **Consciously not run.** No adopter tree exists here, so [P8]'s
  forward-compatibility case is proved by synthetic reproduction against the real
  root, not by installing into a real adopter. I did not re-run the Bandit /
  release-gate surface -- `bootstrap/security_check.py` is untouched and out of
  scope by the Decision.
* **Residual risk.** (a) The node half is never verified, by design -- and the
  durable record now demonstrates it: the archived proposal's own example token
  cites `test_thing`, a node that does not exist, and passes clean. (b) An absent
  **root-level** `path::node` is still never flagged; documented, unpinned by any
  test. (c) `dev/PLANNING.md` is currently modified in the working tree by session
  `codex-93c2a217`, whose claim on it is still open; the two corrected rows are
  present in that working copy, but a future clobber would be silent -- nothing
  mechanical protects them.

**Covered.**

* *Fix correctness at the boundaries* -- 28 shapes, pre/post, tabulated; four
  claimed edge cases confirmed, four unclaimed ones found ([C2], [C3], and the
  directory/root-level pair).
* *Bypass invariant* -- mutation-proven via the faithful bypass mutant (assertion
  2 is the sole red), plus the strictly-flag-reducing argument and the glob-path
  measurements.
* *Mutation battery, independently* -- M1/M2/M3 reproduce node-for-node
  (`48b05f1`'s body is accurate, including its correction to [P2]); M4-M8 are mine.
* *Production path exercised* -- the four new assertions go through
  `cc.check_file(doc, CAIRN_ROOT)`, the module's public scan entry, not the helper.
* *Twin discipline* -- `cmp` clean, 41 pairs, parity node mutation-proven (M8).
* *Live invariant* -- 869 correct; `check_cairn` exits **1** on a perturbation.
* *Drift* -- commit bodies vs shipped behaviour reconciled line by line; the two
  that do not reconcile are [C1] and [C5].
* *Decision fidelity* -- exclusion list re-checked per file; 76 rows before and
  after; G6 diff-empty across `99c8d55..fc32dd9`.
* *Lifecycle / process placement* -- intent claim, block, Maintainer release,
  ledger release event, and the per-commit scope of the override all verified
  against `dev/intents.jsonl`.
* *Cross-document consistency* -- module docs swept, which is where [C7] came from.

**Not covered / low confidence.**

* **I am the same agent type as the implementer.** `doctrine/plans.md` sets
  "not the implementing agent" as the code-review floor and I meet it, but this is
  not a cross-type read. The specific blind spot: [C1] is again the lineage's known
  failure mode, so I may be pattern-matching the familiar error class rather than
  finding an unfamiliar one.
* **Adopter-tree behaviour is inferred.** No adopter checkout is available; the
  `claim-check-allow` forward-compatibility case is synthetic.
* **I did not evaluate the CHANGELOG entry's editorial quality**, only the
  "archived" tense claim and the absence of a house convention for it.
* **The 129-node placeholder figure is this repository's suite**, `as_of`
  `fc32dd9`. It is a measure of exposure in Cairn's own tree, not a general rate.
* **I did not open the design question behind the known omission** -- whether a
  cheap partial node check (grepping the cited file for the node name) is worth
  it. That is a separate proposal if anyone wants it, not a code-review call.

**Recommendation on a second pass.** A cross-type External round is **not**
warranted before archive. Every finding here was resolved by execution rather than
judgement, so a different agent type would mostly re-run the same commands; the
genuine negative space (adopter-tree behaviour, the node-half design question) is
not what a code review resolves. The plan declared `required(Internal)` for its
plan review and nothing here escalates the tier.

**Verdict: APPROVE WITH FOLLOW-UPS.**

The fix is correct and I could not break it. The bypass invariant holds under
every construction I attempted, the edit site is genuinely singular,
`_token_path_part` was rightly left alone and the reasoning for it checks out
empirically, the twins are identical and mutation-guarded, R1's end-to-end check
passes, and the Decision's scope fence is honoured to the file. The intent-override
handling is the best-recorded thing in this lineage.

What is owed before archive is record repair and two cheap guards, not rework.
**[C1], [C2] and [C3] are archive-blocking**: a headline verification figure that
counts another session's unlanded tests, a load-bearing invariant with a
6.6%-of-suite exception that a reviewer already measured and flagged once, and a
fail-open widening that lets a directory stand where a test file must. [C4]-[C8]
are sharpening. That [C1] is the eleventh instance in one day of the same failure
mode -- a claim asserted at the strength intended rather than delivered -- in a
plan whose entire subject is that failure mode, is the durable finding here; the
mechanism this time was not carelessness but a *self-consistent* arithmetic
(1981 -> 1985, delta +4, four new tests) sitting on a contaminated baseline.

## Lasting-truth migration

*Filled in at archive time.*

---

## Response to the Internal plan review -- Claude (Strategy) -- 2026-08-04

**Model**: claude-opus-5

Twelve findings, accepted in full. The reviewer did **not** contest the design —
the defect reproduces, the fix is right, and the scope fence was checked row-by-
row against the Decision's exclusion list and holds. What failed is the
specification *around* the fix, and it failed in eight places.

**[P1]** accept — **the mutation battery's first entry is false, and it is the
same error I made twelve hours earlier.** `bootstrap/tests/test_claim_check_module.py:42`
loads `templates/modules/default-on/claim_check.py` — **not** `scripts/`. Verified:
replacing `scripts/claim_check.py` with a bare `raise` leaves **28 tests passing**.
This morning's Chunk E′ made the identical mistake in the opposite direction
(mutating `tools/lifecycle_planner.py` when the test loaded the
`templates/skills/_lib/` copy). The generalizable error is assuming the copy that
*looks* primary is the copy under test. A1/A2 are also **swapped** relative to the
twin pair's `(dst, src)` direction.

**[P2]** accept — mutation 3 is false. `_scan` dispatches on the **full token**, so
a `:N` citation never reaches `check_path_token`; stripping at the first `:` there
changes nothing and all three assert-3 cases stay green. The "fails open" defence
is held by **the dispatch**, not by assertion 3, and nothing currently pins the
dispatch. The real mutation is a pre-dispatch strip in `_scan`.

**[P3]** accept — mutation 2 under its literal reading ("delete the existence
check") fires assertion **1**, not 2. Only the *bypass* mutant — returning `None`
for any `::` token — fires assertion 2.

**[P4]** accept — **the tenth instance.** Chunk row B3 proposed to correct the
phrase *"one assertion"* in the G6 row. **The G6 row does not contain that
phrase.** Verified: the board carries exactly two such phrases, SC3 (`:720`) and
SC5 (`:844`), both quoted correctly; G6 states a *trigger* and prescribes no
remedy at all. The phrase came from **my own Class A table in the proposal**,
which invented a remedy G6 never claimed — and then this plan proposed to
"correct" the board to match. B3 is **removed**: there is nothing there to fix.

**[P5]** accept — "seven paths" matches neither the row count (8) nor the distinct
files (5). Stated as an equality, so it was unsatisfiable as written. Corrected to
the enumerated set below.

**[P6]** accept — R1's acceptance check as worded asks for a **subtractive edit to
an append-only archived proposal**, which the claim-marker carve-out
(additive-only) does not permit. Re-specified: prove it on a **scratch copy**. The
directive in the archived file simply goes inert once the fix lands, which is the
correct end state for an append-only record.

**[P7]** accept — assertion 1 goes **vacuous** if the fixture's node id contains a
`_PLACEHOLDER_CHARS` member: such a token is exempted upstream for an unrelated
reason and would never reach the check. `[` and `]` are safe; space, `<`, `>`,
`{`, `}` are not. The fixtures pin a plain id **and** a bracketed parametrised id,
and deliberately avoid the placeholder set.

**[P8]** accept — `_token_path_part` is **the wrong target**. Its single call site
(`_scan`, glob matching) is not in the resolution path, so the proposal's premise
that it "strips before resolving" mis-describes the mechanism. Worse, touching it
is a **latent adopter regression**: a full-token `claim-check-allow` glob for a
not-yet-created node would go from clean to hard-flagged. Removed from scope; the
edit is **one site**, `check_path_token`.

**[P9]–[P12]** accept — the shipped module docstring also describes coverage and
is updated with A3; the `check_cairn.py` smoke check has **no baseline** (3 issues
at HEAD, exit 0) so it is recorded with its baseline rather than as a pass/fail;
three unlisted edge cases are added, including that a **root-level** `path::node`
(no `/`) is never checked at all, which qualifies invariant (1); and neither chunk
falls under the deliberation commit-approval carve-out, so both are ordinary
approval-gated commits.

## Sequence revision 2026-08-04

Supersedes the original Sequence. **One edit site, not two. Five files, not
seven. B3 removed.**

```
1. Chunk A -- R1 + R2: check_path_token in BOTH copies, with its tests  [commit 48b05f1]
2. Chunk B -- R3: two board-row corrections + CHANGELOG                 [commits f42db96, 5e10623]
```

### Chunk A (revised)

| # | File | Change |
|---|------|--------|
| A1 | `templates/modules/default-on/claim_check.py` | **The copy the tests load** (`test_claim_check_module.py:42`). `check_path_token` resolves a `path::node` token on its path part. **This is the only edit site** — `_token_path_part` is untouched per [P8] |
| A2 | `scripts/claim_check.py` | The byte-identical twin — same edit, same commit |
| A3 | both copies' module docstring | State that the node half is **never verified** |
| A4 | `bootstrap/tests/test_claim_check_module.py` | Four assertions — see below |

### Chunk B (revised)

| # | File | Change |
|---|------|--------|
| B1 | `dev/PLANNING.md` SC3 (`:720`) | "the guard is one assertion" → vacuous as worded; name the provable claim |
| B2 | `dev/PLANNING.md` SC5 (`:844`) | "two assertions" → the entry is already stale; a `security_check.py` edit |
| B3 | ~~G6~~ | **REMOVED** per [P4] — the row prescribes no remedy; the phrase was invented by the proposal |
| B4 | `CHANGELOG.md > Unreleased > Fixed` | One line |

### Acceptance criteria (revised)

Four assertions in `bootstrap/tests/test_claim_check_module.py`:

1. `path::node`, path **exists**, plain node id → no flag.
2. `path::node`, path **absent** → **still flagged**. The load-bearing one.
3. `path:N` line-bounds behaviour **unchanged**.
4. `path::node[param]` — a bracketed parametrised id → no flag *(guards [P7]:
   proves assertion 1 is not passing via placeholder exemption)*.

**The corrected mutation battery**, each targeting the copy the tests actually
load:

| Mutation (in `templates/modules/default-on/claim_check.py` unless noted) | Fires |
|---|---|
| revert the `check_path_token` change | assertion 1 (and 4) |
| make the `::` branch return `None` unconditionally (the bypass mutant) | **assertion 2** |
| add a pre-dispatch strip at the first `:` in `_scan` | assertion 3 |

**Changed-file set — five distinct files**, verified per-commit:
`templates/modules/default-on/claim_check.py`, `scripts/claim_check.py`,
`bootstrap/tests/test_claim_check_module.py`, `dev/PLANNING.md`, `CHANGELOG.md`.

**R1's acceptance check, re-specified per [P6]:** copy the archived proposal to a
scratch path, delete the `claim-check-allow` directive **there**, and confirm
`claim_check` reports clean. The archived file itself is never edited.

### Author-accounting — corrections

* **Invariant (1) is qualified per [P12]:** a **root-level** `path::node` (no `/`)
  never reaches `check_path_token`'s repo-path branch at all, so the bypass
  invariant covers tokens with a path separator only.
* **Retracted:** "`check_path_token` **and `_token_path_part`** are the touched
  entry points". Only the former is touched.
* **`check_cairn.py` baseline:** 3 issues at HEAD, exit 0 — recorded so the smoke
  check is read against a baseline rather than as a bare pass.

---

### Response to the code review -- Claude (Strategy) -- 2026-08-05

**Model**: claude-opus-5

Grammar: Code-review-Response. Eight findings, all accepted.

* **[C1]** accept (followup commit `a0fe4a3`) — **the eleventh instance, and the
  most instructive.** "1985 passed" was not this change's suite: 22 of those
  nodes came from a concurrent session's **uncommitted** `test_security_stack.py`.
  The plan review's `1981` baseline carried the identical +22, so my "+4 delta"
  **self-validated against an equally contaminated reference** and neither of us
  saw it. Then my first correction attempt reproduced the error one step removed
  — `git diff` swept that same uncommitted work into the "clean" worktree patch.
  Re-measured properly: a worktree at HEAD (`e1b2e30`, which now *includes* that
  session's committed work) with only this change's six files applied, worktree
  status verified before the run → **1986 passed, 1 skipped, 330s**, Python
  3.13.13. The generalizable rule: *a suite figure taken in a shared working tree
  is not a measurement of your change.*
* **[C3]** accept (followup commit `a0fe4a3`) — a **real fail-open I introduced**.
  `.exists()` let a directory path half through (`<a-directory>::test_x`, FLAG →
  clean — written here in placeholder form because the fix now flags the literal
  token, which is itself the fix demonstrating itself) where the sibling line-bounds branch already used `.is_file()`. Fixed,
  with two assertions and a mutation proof that also shows the fix did not spill
  onto the bare-path branch.
* **[C7]** accept (followup commit `a0fe4a3`) — both module docs said the checker
  "covers: paths and line citations". They now name the third kind **and its
  limit**.
* **[C2]** accept — recorded, not fixed. `_is_placeholder` skips any token
  containing a space or `< > * { }`, so an **absent** path is not flagged when the
  node id carries one — **129 of 1963 node ids (6.6%)**. Fixing it means changing
  `_is_placeholder`, which is a wider adopter-facing behaviour change than this
  plan's fence permits. **Invariant (1) is qualified accordingly** rather than
  left overstated: the bypass guarantee holds for node ids free of the placeholder
  set.
* **[C4]** accept — three of four `_node_citation_path` branches are invisible to
  the full suite (`partition('::')`→`partition(':')` and dropping `and node` both
  leave the suite unchanged; `and path_part` is behaviourally inert). Recorded as
  a residual: the branches are defensive, and pinning each would need fixtures
  that assert non-behaviour.
* **[C5]** accept — **six** files landed, not the five the revised acceptance
  criteria state as an equality, and the plan's "No `docs/` change" is wrong:
  `docs/tool-usage.md` carries a registered live invariant on `claim_check.py`'s
  line count. Corrected in the ledger below.
* **[C6]** accept — the board rows are stamped "2026-08-04"; this lineage landed
  on **2026-08-05**. Left as-is in the rows themselves (append-only record of what
  was written) and corrected here.
* **[C8]** accept — `[P12]` was cited where `[P11]` was meant, and the CHANGELOG
  says "the archived plan" while the plan was at `review`. Both cosmetic; recorded
  rather than chased into an append-only section.

## Lasting-truth migration

**Archived** 2026-08-05.

### Dispositions

```
Dispositions:
* [C1] suite figure contaminated by a       -> accept (commit a0fe4a3)
       concurrent session's uncommitted file
* [C2] placeholder chars bypass the flag    -> wontfix (invariant qualified;
       for 6.6% of node ids                     the fix is a wider adopter
                                                behaviour change, out of fence)
* [C3] directory path half passed (fail-open) -> accept (commit a0fe4a3)
* [C4] three defensive branches unpinned    -> wontfix (pinning needs
                                                non-behaviour fixtures)
* [C5] six files, not five; docs/ touched   -> accept (corrected in this ledger)
* [C6] rows dated 08-04, landed 08-05       -> accept (corrected here)
* [C7] module docs named only two kinds     -> accept (commit a0fe4a3)
* [C8] [P12]/[P11] cite; CHANGELOG wording  -> wontfix (cosmetic, and the
                                                sections are append-only)
```

**Zero `defer` dispositions** — no Maintainer authorization owed, **no board row
added**. Net board delta **0**; two rows corrected.

Both `wontfix` dispositions were tested against the **C4 eligibility rule** before
being taken: [C2] and [C4] reach no adopter behaviourally (the checker's verdict is
unchanged for every token shape measured), block no release, and need no Decision.
[C2] is the closer call — it is a *stated* limit on a shipped checker — which is
why it is qualified in the invariant rather than merely declined.

### Evidence ledger

**Evidence shipped.** Suite **1986 passed / 1 skipped / 330s** under Python
3.13.13, measured in a clean worktree at `e1b2e30` with only this change's files
applied. `check_cairn` OK across 178 files. Twins byte-identical by `cmp`. The
code reviewer independently reproduced the full mutation battery node-for-node in
a clean worktree, confirmed the bypass invariant across **28 token shapes** (every
delta FLAG→clean, none clean→FLAG, none FLAG→EXEMPT), verified no
`claim-check-allow` glob exempts anything it would not have before, and verified
the intent override against `dev/intents.jsonl` rather than the commit body alone.

**R1's acceptance check passed** — pre-fix 1 flag / exit 1, post-fix OK / exit 0,
with the archived proposal never edited.

**Changed-file set — six files** (corrected per [C5]):
`scripts/claim_check.py`, `templates/modules/default-on/claim_check.py`,
`bootstrap/tests/test_claim_check_module.py`, `docs/tool-usage.md`,
`dev/modules/claim-check.md`, `templates/modules/default-on/claim-check.md`
— plus `dev/PLANNING.md` and `CHANGELOG.md` in Chunk B.

**Residual risks.**
* **The node half is never verified** — a `guard` may cite a node that does not
  exist and nothing notices. The honest limit of a static checker under a
  zero-dependency budget.
* **[C2]'s placeholder-character gap** — 6.6% of node ids bypass the flag.
* **The line-count invariant will drift again** on the next edit to this file; it
  is mechanically enforced (perturbing it exits 1), so it fails loudly.

### Loop-fidelity sign-off

Implementation commits `48b05f1`, `f42db96`, `5e10623`, `a0fe4a3` match the
accepted **`## Revised proposal`** section (R1–R3) as ratified by the Decision at
`78e8916`. The Decision's exclusions were honoured and independently verified by
the code reviewer: no guard was written, no board row added, the G6 row is
**diff-empty**, and the deferred section holds the same row count before and
after.
