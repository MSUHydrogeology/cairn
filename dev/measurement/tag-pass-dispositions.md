# Finding-tag pass — the keep ledger

Chunk C of [`comprehension-outlives-the-artifact`](../plans/comprehension-outlives-the-artifact.md).

**What this file is for.** The pass revises every finding-tag candidate in a
comment or docstring so the sentence states its reason rather than citing the
deliberation that produced it. A **rewrite** evidences itself in the diff. A
**keep** — a candidate that is not a coordinate at all — leaves the file
byte-identical, so without this ledger the completion bar would have no failure
state. Every keep is recorded here, one line per token per file, with the reason
it is not a coordinate.

**Rewrites are deliberately not listed.** The diff already carries them, and
duplicating them here would make the ledger a second, weaker copy of the record.

**How completion is checked** (plan R4-F3). The **code reviewer, at Boundary C**,
re-runs the enumeration against the pre-pass commit over the Chunk C commit
range, and confirms every candidate it lists is either changed in that diff or
named below. This is a human step — no gate, no test, no new machinery.

**Granularity.** One line per *token per file*; the plan's scope figures count
*occurrences*. A token appearing four times in one file is one line here and
four occurrences there, because the reason for keeping it is one judgement, not
four. **Ledger lines therefore do not reconcile to the occurrence count**, and a
reviewer checking by arithmetic rather than by the pairing will read a shortfall
that is not one.

**Enumeration method** — tracked `*.py`, read from blobs at the measured commit,
classified with `tokenize` + `ast` so comments and docstrings are separated from
string literals and code tokens:

```
class 1   \[([A-Z]{1,4}\d+(?:[-–][A-Z]{0,4}\d+)?)\]
class 2   (?<![\[\w-])([A-Z]{2,4}\d+)(?![\w\]-])      minus a lint denylist
class 3   (?<![\[\w-])([A-Z]\d)(?![\w\]-])
```

Lint denylist: `PLC0415`, `BLE001`, `SLF001`, `ARG002`, `SIM115` — Ruff codes.
**`SIM115` was added during implementation**; the plan's stated denylist has the
first four. It is consistent with the definition ("lint codes excluded") and was
identified as a non-coordinate by the round-4 plan review, but it is a change to
the stated method and is recorded here rather than absorbed silently.

---

## Keeps

| File | Token | Why it is not a coordinate |
|------|-------|----------------------------|
| `bootstrap/tests/_gate_preflight.py` | `SHA256` | The hash algorithm, in `"""Resolve the recorded key to ``(absolute path, SHA256 fingerprint)``."""`. Names the digest the function returns. |
| `bootstrap/tests/_gate_preflight.py` | `N4` | **A live fence identifier, not a finding tag.** `N4` names the key-channel fence in the `N4`–`N8` Maintainer-intervention series of the `ceremony-as-code` plan (18 live citations; siblings `N5`–`N8` at 13/7/4/3), and `bootstrap/REANCHOR_RUNBOOK.md:500` states *"**N4 precondition** holds"*. A Maintainer reading a refusal needs the fence name to look up. Kept **and** given its reason inline, so the sentence no longer depends on the lookup. |
| `bootstrap/tests/test_gate_preflight.py` | `N4` | Same fence, same reason. |
| `tools/lifecycle_planner.py` + twin | `H2`, `H3` | Markdown heading levels, not coordinates. The parser's field scopes are literally defined as "the body above the pass's first H3". |
| `tools/lifecycle_planner.py` + twin | `C0` | The Unicode C0 control-character block, in a rule about which code points are refused. |
| `tools/lifecycle.py` + twin | `H2` | Markdown heading level, as above. |
| `bootstrap/tests/test_lifecycle_brief.py` | `M3` | **A live fence, like `N4`.** `M3` names the interpreter-binding fence and carries **23 citations in `dev/plans/ceremony-as-code.md`, an active plan** (siblings `M2` at 59, `M4`, `M7`). The test's whole subject is that fence, so the name stays and the sentence now says what it fences. Caught by grepping the tree before deleting — the rule working as intended rather than after a test died. |
| `bootstrap/tests/test_transition_lint.py` | `A1`–`A20`, `B3`–`B15`, `C2`–`C11` | **A live internal labelling scheme, not citations.** The file defines ~29 of these itself (`# A9.`, `# C4.`, plus more in docstrings) and cross-references between them — *"Run with C10"*, *"C6/C7 is the second pair"*. A reader resolves them by scanning the same file, which is exactly what makes them live. Same test as `N4`: the referent is in reach. Only the references pointing *out* of the file (to the archived plan) were revised. |
| `tools/lifecycle.py` + twin | `E1`, `S12`, `CF3` | **Examples of the pattern the code matches**, in `#: A bracketed finding id -- \`[E1]\`, \`[S12]\`, \`[CF3]\`, \`[M6-R]\``. The module parses finding ids, so naming their shapes is the docstring doing its job. |


---

## A correction worth recording

The first cut of this pass **renamed `N4` to "key-at-rest precondition"** across
seven sites, including an operator-facing refusal string. That was a category
error: `N4` is a live fence in a five-member series that a runbook, a live plan
and four sibling fences all still cite, so the rename severed a reference a
Maintainer acts on while leaving its siblings intact.

It was caught by the agent implementing `ceremony-as-code`, and the resolution
is better than either starting position: **keep the coordinate and add the
reason.** The sentence states what the fence means, so a reader who does not
look it up still understands it; the name survives, so a reader who needs to act
on it can.

The general rule this pass follows: *a coordinate that still resolves to
something live is domain vocabulary and stays; a coordinate that points into a
closed deliberation goes.* The same judgement kept the redundancy gate's `R1`
and `R6` out of the Chunk D rename set.

**Why the two judgements differed, which is the generalisable part.** `R1`/`R6`
sit next to the gate that consumes them, so their liveness is visible in the
same file. `N4`'s consumers are three documents away -- a plan table, a runbook
block, and a refusal string -- and nothing local to `_gate_preflight.py` shows
it is load-bearing. So the failure was not inattention; it was **a coordinate
whose evidence is not where the reader is standing.** That is a property of the
corpus, and the check it implies is specific: before deleting a coordinate,
grep the tree for it, not just the file. "Check twice" would not have caught it.

### Denominators, stated because they drifted

`N4` was quoted at three different numbers during this pass. They were different
things, and one was an error:

| Count | What it is |
|---:|---|
| 7 | lines containing `N4` in `_gate_preflight.py` at the pre-pass commit -- one file |
| 11 | substitution *operations* applied to restore the name (6 + 5) |
| 12 | lines containing the text `N4` after the pass, both files |
| **8** | **`N4` candidate lines in the governed surface** (comments + docstrings), 4 per file -- the figure that belongs in a verification record |
| **2** | **ledger lines for `N4`**, by the token-per-file granularity above |

The other four occurrences are inside string literals and code tokens, which the
enumeration reports separately and never counts as candidates.


---

## A second correction: the pass ran into a security fence

Five comment lines in `tools/lifecycle.py` were revised and then **put back**.
They sit inside the three symbols `bootstrap/tests/test_lifecycle_brief.py`
pins byte-and-AST-identical, guarding the local interpreter binding --
a surface `AGENTS.md` lists as high-risk and Security-Review-gated.

Nothing about the *prose* was wrong; the point is that on this surface the bytes
themselves are the contract, so even a comment edit re-opens a review. The fence
caught it, which is what it is for. The rule the ledger carries forward:
**before revising a comment, check whether the enclosing symbol is pinned** --
`grep` the test corpus for the symbol name, the same move as grepping the tree
for a coordinate.

**A side effect worth recording.** Removing a vendor name from one comment
(`(Codex code review P2 #1)`) dropped the neutrality gate from **93 to 92**
pre-existing failures. That is an improvement and it was incidental, not aimed
at -- but it moves a baseline other records cite, so it is stated rather than
left for someone to rediscover as an unexplained drift.

---

## Blocked — RESOLVED 2026-08-18

The five lines below were blocked by the byte pin on the local interpreter
binding. **The Maintainer authorized the edit and the re-pin:**

> *"Let's go ahead and edit them, since we'll re-pin with the other agent I'm
> fine with this."*

All five are now revised and the four digests in
`bootstrap/tests/test_lifecycle_brief.py::_INTERPRETER_SYMBOL_DIGESTS` are
re-derived. **Nothing is deferred, so the plan's "no revival row" claim holds
again.**

**Correction (2026-08-18, from the `ceremony-as-code` agent).** This entry first
said all five lines sat inside `_probe_interpreter` / `_resolve_interpreter` /
`_warn_stale_once`. **That was wrong**, and verified wrong by enclosing-function
analysis at `c29ead3`:

| Line | Enclosing function | Pinned? |
|-----:|--------------------|---------|
| 436 | `_has_symlink_component` | **no** |
| 477, 481, 505, 535 | `_resolve_interpreter` | yes |

`_probe_interpreter` and `_warn_stale_once` were never touched. Only **one**
symbol's pair was re-derived (2 values, not 6) — which is correct and complete,
but a reviewer comparing the old "three functions" wording against a two-value
re-pin would reasonably conclude the pin was under-derived. The evidence below
was always sound; the description of it was not.

**How the change was shown safe, rather than asserted.** The pin's own AST
digest includes docstrings, so it cannot distinguish a docstring edit from a
logic change. Each pinned function was therefore digested a second way — with
*every* docstring stripped before `ast.dump` — before and after the edit:

```
_probe_interpreter       08856288621efb6f   unchanged
_resolve_interpreter     92fdb64150ee4ef5   unchanged
_warn_stale_once         d5d3de3acd75a08b   unchanged
```

Identical on both sides, which proves the executable AST is untouched and the
change is comment- and docstring-only. That check is the reason the re-pin is
reviewable rather than a self-generated pin: a reviewer can re-run it against
the parent commit and get the same three values.

**Still owed:** the other agent's ceremony work covers this surface and should
confirm the re-pin. The digests were re-derived by the implementing agent under
explicit Maintainer authorization, not by a Security Review.

| File | Was | Now |
|------|-----|-----|
| `tools/lifecycle.py` + twin | `binary runs (S2).` | `binary runs.` |
| `tools/lifecycle.py` + twin | `Resolve-don't-bake (Decision 6 / R3):` | `Resolve-don't-bake:` |
| `tools/lifecycle.py` + twin | `... corrected on the record (S1).` | `... corrected on the record.` |
| `tools/lifecycle.py` + twin | `later used to run (R7)` | `later used to run` |
| `tools/lifecycle.py` + twin | `... any fatal check (finding 1; corrected R2/R6).` | `... any fatal check.` |

---

## Finding: the fence pins the caller, not the callee

Raised by the `ceremony-as-code` agent while confirming the re-pin above, and
**pre-existing** — not introduced by this pass, and surfaced only because one
edit happened to land one level outside the boundary.

`_has_symlink_component` is **not** one of the four pinned symbols. It is called
from `_probe_interpreter`, which is — but a pinned digest covers the call site,
not the function called.

`AGENTS.md` describes the local interpreter binding's reader as checking
*"absoluteness, schema, symlink-freedom and the executable bit"*.
**`_has_symlink_component` is the symlink-freedom check.** So a *behavioural*
change to symlink detection would not redden this fence, even though symlink
freedom is one of the four properties the trust root is documented as enforcing.

This pass's edit there was comment-only and harmless. The gap is structural and
belongs to whoever next reviews that surface; it is filed in `dev/PLANNING.md`
beside the re-pin rather than left in two chat logs.

---

## The frozen gate surface — corrected

**An earlier version of this section, and the C2c commit body, claimed five
`test_gate_manifest.py` failures and `FROZEN-MODIFIED` breakage. That does not
reproduce.** `test_gate_manifest.py` passes 21/0. The `ceremony-as-code` agent
measured it in an isolated worktree and was right; this is the correction.

**What is actually true.** `_frozen_files()` does glob `bootstrap/*.py`,
`bootstrap/tests/**/*.py`, `templates/modules/**/*.py` and `scripts/*.py`, and
**35 entries in the committed `bootstrap/tests/fixtures/gate_manifest.json` now
differ from the tree**. But no test in the ordinary suite compares that
committed fixture against the tree — the gate-manifest tests `produce()` a fresh
manifest and verify against *that*. So the suite is green and the committed
fixture is stale, which are different things and were conflated.

**Consequence: the frozen surface never blocked this pass.** The earlier "82% of
remaining work is blocked" framing was wrong. Editing a frozen file does not
redden anything; it makes the committed manifest stale, which matters only at
re-anchor time.

**And the right framing for the re-anchor**, from the same agent: *"whatever the
anchor is at ceremony time covers whatever is committed at ceremony time."*
Coverage comes from **sequencing**, not from expanding another plan's scope. The
real open question is narrower — **who regenerates `gate_manifest.json` and
re-records the lockfile, and under what review** — which is the same
self-certification question the interpreter re-pin raised.

**How the wrong figure was produced.** The C2c verification diffed the 34-file
scoped failure list against a baseline file that held the failures of **one**
test module, so every failure outside that module read as "introduced". The
scoped baseline's count (5) had been captured; its failure *names* had not. A
count is not a baseline.

### Two real failures, not six

| Failure | Status |
|---|---|
| `test_lifecycle_board.py::…test_the_board_contains_no_second_status_or_verdict_vocabulary` | **fixed** — see below |
| `test_portable_security_sweeps.py::test_cairns_own_install_records_all_three_files_in_the_lockfile` | **open** — real; the lockfile digest for `scripts/run_portable_security_sweeps.py` disagrees with disk |

**The board failure is the one worth learning from.** It died on
`text.index("# Chunk F -- the derived orientation board")` — a **live consumer of
a comment this pass deleted**. It is exactly the failure mode the peer named when
C2 began: *ask whether anything executes against the id, not just whether prose
cites it.* A comment header consumed by `str.index` has no citation anywhere and
greps as pure prose, so the tree-grep rule does not reach it. The slice is
retargeted and now **asserts its landmark first**, so a future edit gets a
sentence saying which of the two drifted instead of `ValueError: substring not
found`.

**The rule this adds**, and it is the third refinement of the same test:
*before deleting a comment, grep the test corpus for its literal text* — not just
for the coordinate inside it. `"# Chunk F` would have found this in a second.
The two live consumers this pass has hit failed differently and that is the
point: `N4` had **many** consumers across documents and grep-for-citations found
them; this one had **exactly one**, invisible to that grep because `str.index`
builds no citation.

**And the fix belonged on the test, not the comment.** The first attempt merely
asserted the landmark before slicing on it — better error, same defect: a
comment kept alive because a test is brittle, which is the category this pass
exists to remove. The property is now asserted on the **parse tree** (each
vocabulary is declared exactly once at module level, so it cannot be redeclared
anywhere and no section boundary is needed), and the half that genuinely needs
the board's region is bounded by a real symbol rather than by prose.

### A baseline is a set, not a scalar

The wrong-baseline defect above has a twin, reported by the `ceremony-as-code`
agent from the other direction: it ran a baseline under the wrong interpreter,
got 42 failures, and nearly attributed two of them to its own change. Mine had
the right environment and no names; theirs had the right names and the wrong
environment. **Same defect: a baseline is a set of failure identities, and a
count is not a baseline.** The remedy is identical — record the identities, and
record what produced them (commit, interpreter, and the exact node set).

### Batch: five install / security / grammar suites

| File | Before | After | Kept, and why |
|---|---:|---:|---|
| `bootstrap/tests/test_profile_grammar.py` | 17 | 1 | `C0`/`C1` — Unicode control-character classes, named by `_PROFILE_CONTROL_RE`. Domain vocabulary; the code enumerates them. |
| `bootstrap/tests/test_presets.py` | 19 | 0 | — |
| `bootstrap/tests/test_security_finding_confidentiality.py` | 14 | 3 | `P1` — the **principal ordinal** in `CAIRN_API_P1_CREDENTIAL`, read at line 397 and parametrized at 1200, and named in two sibling suites. The docstring is *about* why only `P1` isolates. |
| `bootstrap/tests/test_upgrade_side_door_parity.py` | 14 | 0 | — |
| `bootstrap/tests/test_reference_scripts.py` | 12 | 0 | — |

The removed sets trace to `dev/plans/archive/profile-parse-fail-open.md`
(`A2`/`B3`/`B6`–`B9`/`C6`–`C8`/`D3`/`D5`/`I1`–`I4`) and to
`dev/plans/archive/api-web-security-modules.md` (`AW6`/`AW8`) and
`dev/plans/archive/security-verification-activation.md` (`T7`) — all archived,
nothing executes against any of them.

**`P1` is the fourth live keep, and the first found by reading the code rather
than by grepping documents.** `N4` and `M3` were fences cited in active plans, so
a tree-grep found them; `C0`/`C1` are a published Unicode vocabulary. `P1` is
neither: it resolves *inside this file*, to a string the test builds and a
subprocess reads. The grep that finds it is not `grep -r P1 dev/` but
`grep -n P1 <the file itself>` — **the coordinate's referent may be one line
away, in code.** Class-3 tokens make this common: a single letter and a digit is
exactly the shape both a finding id and an ordinal take.

**One boundary held deliberately.** Two of these docstrings open by citing the
plan that produced the file (`cairn-v0.2-p1-reference-scripts`,
`2026-06-10-...-side-door-parity`). Those are process citations of the same
family, but a plan *filename* is not one of the three tag classes this pass
enumerates, so they were left. Widening the pass mid-execution to a class the
review never scoped would be a deviation; if they should go, that is a separate
proposal, not a silent extension of this one.

### Batch: the quality gate, verify_counts, and the differential oracle

| File | Before | After | Kept, and why |
|---|---:|---:|---|
| `scripts/quality_gate.py` | 16 | 14 | `R1` / `R6` / `R7` — see below. Removed: two `P1`/`P2` code-review citations. |
| `scripts/verify_counts.py` | 7 | 0 | — |
| `bootstrap/tests/test_verify_counts.py` | 10 | 0 | — |
| `bootstrap/tests/test_oracle.py` | 10 | 0 | — |
| `bootstrap/tests/_oracle.py` | 9 | 0 | — |

**`R1`/`R6`/`R7` are live, and the evidence is published doctrine.**
`doctrine/consolidation-review.md` *defines* them — `R1` is the n-gram overlap
detector, `R6` the unreferenced-def AST walk, `R7` the per-dimension capability
checklist — and its dispositions log records entries under `redundancy / R6`.
The gate then **emits the token at runtime**: a redundancy run prints
`R6 def <name> is never referenced ...`, and the exemption file
`scripts/quality_gate_unused_def_whitelist.py` is described as "the `R6`
whitelist". A reader who meets `R6` in a comment can resolve it in one hop to a
living document and to output they can reproduce. That is the liveness test
passing on all three legs at once — defined, cited, executed.

**`RR1`/`RR2`/`RR3`/`IR3` in `verify_counts.py` look identical and are not.**
Its module docstring also defines them inline — "`RR1` -- the annotation
contract", "`RR2` -- absent root skips visibly". But **self-definition is not
liveness.** Nothing emits them, no whitelist is named for them, and the
originating plan (`dev/plans/archive/lockfile-provenance-fields.md`) is
archived; they are paragraph numbering with the real name sitting immediately
after it. Each became a bold descriptive lead — *"**The annotation contract.**"*
— which is what the reader needed in the first place.

**The near-miss worth recording.** Grepping the tree for `RR2` returns
`test_scaffold_substrate.py::test_RR2_symlinked_guard_refused_via_launcher`,
pinned by name in `bootstrap/tests/fixtures/gate_manifest.json`. That is a
**different plan's `RR2`**, in a different file, frozen into a manifest. Had the
grep been read as "`RR2` is live, keep it", the wrong tokens would have survived
here; had it been read as "the manifest pins it, so rename it", it would have
broken a frozen surface. A tree-grep on a short token returns homographs — the
hit has to be opened and shown to be *this* coordinate, not merely the same
string. Those test **names** are Chunk D's problem and are gated there.

### Batch: skills security, lifecycle CLI, notice install, Bandit gate, review tiers

| File | Before | After |
|---|---:|---:|
| `bootstrap/tests/test_skills_security.py` | 12 | 0 |
| `bootstrap/tests/test_lifecycle_cli.py` | 10 | 0 |
| `bootstrap/tests/test_notice_install.py` | 10 | 0 |
| `bootstrap/tests/test_security_lint.py` | 10 | 0 |
| `bootstrap/tests/test_onboarding_review_tiers.py` | 9 | 0 |

Nothing kept — every coordinate here traced to a closed round, and in every case
the descriptive name was already sitting beside it (`S4 content-scan` →
`content-scan`; `# --- P1: the NOTICE.md install path` → `# --- The NOTICE.md
install path`). The section banners are the clearest illustration of what the
tag was costing: `# --- S5: no network / bounded surface ---` said the same
thing twice, once resolvably and once not.

**A second homograph, checked rather than assumed.**
`test_lifecycle_cli.py:549` carried `first-session-survivability, C4`, and `C4`
is a **live** id in `scripts/transition_lint.py`'s rule set. They are unrelated:
the lint's `C4` is a rule the linter emits, this one was a plan chunk. Opening
the hit settled it in one step — which is the whole procedure. On a corpus this
size, single-letter-plus-digit tokens collide constantly, so *"the token appears
elsewhere"* is never the finding; *"this occurrence resolves there"* is.

**Two docstrings shed narration along with the tag.** `test_skills_security.py`
opened a docstring with "**Re-anchored by Chunk P4**, which replaced this
module's fixed `_FIELD_ESCAPES` table with ...", then spent three more lines on
what changed and why. The next reader does not need the migration; they need to
know the escape set comes from `encode_display` **so the two cannot drift**.
Four lines of history became one line of reason. Removing a tag often exposes
that the sentence holding it was about the process too — and the rule is the
same one, not a second one.

### Batch: vocabulary, practice modules, scaffold, self-heal, transition_lint

| File | Before | After |
|---|---:|---:|
| `bootstrap/tests/test_lifecycle_vocabulary.py` | 8 | 0 |
| `bootstrap/tests/test_practice_modules.py` | 7 | 0 |
| `bootstrap/tests/test_scaffold.py` | 7 | 0 |
| `bootstrap/tests/test_skills_self_heal.py` | 5 | 0 |
| `scripts/transition_lint.py` | 3 | 0 |

`A6` traces to `dev/plans/review-efficient-lifecycle.md`, **archived in this
session** (`8708705` disposed of its residue). It is the pass's cleanest
demonstration of the decay the principle names: `A6` was resolvable a week ago
and is a dead pointer now, and nothing about the comment carrying it changed.

**`transition_lint.py` shows why the pass touches production code, not only
tests.** Its containment section opened by citing a proposal's `R5` and the
replacement text that superseded it — two coordinates and a supersession, before
the reader learns anything. What they need is one sentence: this file used to
declare its own `_OPEN_STATUSES`, the planner declares them now, and the
contract is restated per consumer because *the containment is the security
property.* That last clause was already there and was the only load-bearing one.

**Vendor names came out with the coordinates.** `test_scaffold.py` and
`test_skills_self_heal.py` carried "Codex External finding 1 / Antigravity R8",
"Filed under External Review F2 from Antigravity", "Codex code review P2 #1".
These are outside the neutrality gate's corpus (it scans doctrine and
templates, not `bootstrap/tests/`), so nothing was flagging them — they were
removed here because the *sentence* was process narration, not because a gate
asked. Worth noting for whoever next reviews the neutrality gate's scope: the
tree carries vendor names in places the gate does not look, and the reason they
are unproblematic is that they sit in dead prose, which this pass is deleting
anyway.

### Batch: the reference scripts and the release security check

| File | Before | After | Kept |
|---|---:|---:|---|
| `scripts/measurements.py` | 7 | 0 | — |
| `scripts/check_cairn.py` | 7 | 0 | — |
| `scripts/gen_legacy_code_review_passes.py` | 8 | 1 | `H2` — heading level |
| `scripts/gen_legacy_passes.py` | 2 | 0 | — |
| `bootstrap/security_check.py` | 6 | 0 | — |

`R3'` and `R2''` — prime-marked findings from
`dev/proposals/archive/2026-08-10-claude-code-review-blindness.md` — were the
densest coordinates in the pass, and the most confidently wrong to keep. A
prime mark means *the amended form of finding R3*, which is a fact about a
review round and nothing else; a reader in a year meets `R3'` and cannot even
tell it from a transposed typo.

**A near-keep worth recording.** `gen_legacy_code_review_passes.py:79` read
"The baseline commit `R3'` requires the manifest to pin," and the constraint is
real and live — the generator does pin a baseline commit. But the *coordinate*
was not doing the work: rewritten as "The baseline commit the manifest pins,"
the sentence keeps every operative word and loses only the provenance. That is
the test to apply when a dead coordinate sits next to a live obligation —
**the obligation survives the coordinate's removal**, because the obligation
lives in the code, not in the review that noticed it.

**Two `R1`s, opposite dispositions, one commit apart.** `quality_gate.py`'s
`R1` was kept (published doctrine defines it, the gate emits it);
`security_check.py`'s `R1` — "Security-hardening Chunk 7 / R1", "Binding
amendment R1", "**R1.1**" — was removed. Same token, same tree, both in
production code under `scripts/` and `bootstrap/`. Nothing about the token's
*shape* separates them and nothing about its *location* does either; only
opening the referent does.

### Batch: the attestation tool, the engine loader, and lockfile provenance

| File | Before | After |
|---|---:|---:|
| `bootstrap/tests/_ast_attest.py` | 8 | 0 |
| `bootstrap/tests/test_ast_attest.py` | 8 | 0 |
| `bootstrap/tests/_loader_proto.py` | 8 | 0 |
| `bootstrap/tests/test_loader_identity.py` | 7 | 0 |
| `bootstrap/tests/test_lockfile_provenance.py` | 7 | 0 |

**A homograph against a *live* scheme, which is the dangerous direction.**
`_loader_proto.py` described "the reproduced **S1** attack", and `S1` is live
vocabulary: `templates/core/dev/proposals/_template.md:347` ships
`**S1 — Who supplied it?**` as the first security-preflight question. A
grep-for-liveness returns that hit and it is genuinely live — and it is not this
`S1`, which named a Security Review finding about import hijack. The earlier
near-misses (`RR2`, `C4`) collided with *dead* schemes, where a wrong keep costs
only a surviving tag. Colliding with a live one is worse: the evidence for
keeping looks strong, and keeping it preserves a pointer that reads as a
citation of the shipped preflight and is not one.

**Two pre-existing failures were checked, not assumed.**
`test_ast_attest.py::test_ast_gate_passes_over_the_full_scaffold_module_set`
and its baseline sibling fail at this commit. They are the filed AST-baseline
drift (`191fb93`), not this batch: every symbol in the failure output resolves
to `bootstrap/_scaffold/`, and this batch modified zero files under that path.
Naming the mechanism rather than the count is the point — "these were already
failing" is the sentence that hid a real regression once already in this pass.

### A convention has a form, and knowing it by name is not knowing it

Recorded from a cross-session exchange with the `ceremony-as-code` implementer,
because it generalises past the incident. This plan's four Response headings
read `## Response to plan review (round 2) -- Claude -- 2026-08-13`. The
disposition predicate compares a section's **kind** — everything before the
first ` -- ` — exactly, so the round marker landed *inside* the compared span
and four conformance obligations silently went undischarged. The sibling plan
wrote the same marker after the date and conformed.

Both of us had reached "the checker is broken" first; the checker was right both
times. The sibling's drift was to more informative heading variants
(`## Response to the clearing review`) — a small deliberate liberty. This one
was worse, because at no point did it feel like a shortcut: the intent was
compliance, the convention was known by name, and the form was wrong. The
sibling then added the honest coda — its own headings passed because it copied
a template that happened to be canonical, not because it had read the
predicate. **"It passes" and "the author knows why" are different states, and
only the second survives the next edit.**

### Batch: security leaf, seed roster, skills matrix, fan-out, module merge

| File | Before | After |
|---|---:|---:|
| `bootstrap/tests/test_security_leaf.py` | 7 | 0 |
| `bootstrap/tests/test_onboarding_seed_roster.py` | 7 | 0 |
| `bootstrap/tests/test_skills_matrix.py` | 6 | 0 |
| `bootstrap/tests/test_skills_fanout.py` | 6 | 0 |
| `bootstrap/tests/test_module_merge.py` | 6 | 0 |

**The method changed here, after four failed guesses in one batch.** Until now
each edit matched a full multi-line block including its leading whitespace,
which meant every comment's indentation had to be guessed correctly or the
substitution missed. It missed four times in this batch alone — always
harmlessly, because a miss aborts before writing, but each cost a round trip to
read the file and count spaces.

The replacement is a line-scoped helper: locate the **unique line containing a
needle**, then substitute within that line. Indentation never enters the match.
It also **refuses on ambiguity** — `DuplicateSlotError` matched three lines in
`test_module_merge.py` and the tool stopped rather than editing the first. That
refusal is the property worth having: the old method's failure mode was a
harmless miss, but a first-match-wins line editor's failure mode is a silent
edit to the wrong line, which is exactly the class this pass is trying to
remove from the tree.

**Five files, thirty-two coordinates, nothing kept.** Two patterns recur and
are worth naming for whoever finishes the tail: a docstring bullet that already
carries a descriptive name (`* **SR6 regression** — every guarded adopter-tree
write function ...` → `* **Guard-routing regression** — ...`), and a banner
comment where the tag is the only thing between the section name and the reader
(`# Merge: customized marker (Antigravity P2)`). Neither needs judgement; both
need the file open.

### Batch: output scan, gate transition, gate manifest, drift surfacing

| File | Before | After |
|---|---:|---:|
| `bootstrap/tests/test_generated_output_scan.py` | 4 | 0 |
| `bootstrap/tests/test_gate_transition.py` | 5 | 0 |
| `bootstrap/tests/test_gate_manifest.py` | 5 | 0 |
| `bootstrap/tests/test_drift_surfacing.py` | 4 | 0 |
| `bootstrap/tests/test_doc_drift_tools.py` | 5 | 0 |

**Editing a frozen gate file makes the gate suite red until you commit, and it
names your files while doing it.** Running the five edited suites produced
`HOLD — 5 gate-integrity violation(s)`, one `FROZEN-MODIFIED` line per file
just edited. Committing them and re-running gives **21 passed**. Nothing about
the content mattered: `verify()` reads each frozen file's **committed** SHA via
git and compares it to **disk**, so any uncommitted edit to a frozen file is
indistinguishable from tampering — which is the correct behaviour for a
tamper-detector and a trap for the person holding the editor.

Two things follow, both operational:

* **The failure names the right files for the wrong reason.** An agent seeing
  five `FROZEN-MODIFIED` lines naming exactly the five files it just touched
  will reasonably conclude its *edits* broke the gate. They did not; the
  *uncommitted state* did. This is the fourth attribution trap in this pass and
  the most persuasive one, because the evidence points precisely at the work.
* **It corrects a nuance in the row filed at `fbd34ed`.** That row said
  `test_gate_manifest.py` passes 21/0 because its tests `produce()` a fresh
  manifest rather than reading the committed fixture. True of the *fixture*
  comparison, and not of the frozen-file check, which does consult git. Green
  suite and stale fixture are still different things; green suite and *clean
  working tree* turn out to be coupled.

**One occurrence left in place, deliberately.** `test_gate_manifest.py:394`
carries `(fence M5)` inside an assertion-message f-string. `M5` is dead — it
appears nowhere in either live plan — but a failure-message string is neither a
comment nor a docstring, and the pass's reviewed scope is those two surfaces
plus (in Chunk D) test names. The line above it, a comment carrying the same
dead tag, was removed. The resulting inconsistency is real and is the honest
report: **assertion messages are a third surface nobody scoped**, they are read
by exactly the audience this plan cares about — someone staring at a failure —
and they should be a follow-up rather than a silent widening here.

### Batch: triggers, skills install, the security net — and a keep in the parser

| File | Before | After | Kept |
|---|---:|---:|---|
| `bootstrap/tests/test_trigger_evaluation_action.py` | 3 | 0 | — |
| `bootstrap/tests/test_skills_install.py` | 3 | 0 | — |
| `bootstrap/tests/test_security_net.py` | 3 | 0 | — |
| `tools/lifecycle.py` + twin | 4 | 4 | **all** — see below |

**`tools/lifecycle.py:2909` is the purest keep in the pass, and it took no
research at all.** The comment reads:

> `#: A bracketed finding id -- `[E1]`, `[S12]`, `[CF3]`, `[M6-R]`.`

Four class-1 tags in one line, none of which cites anything. They are **examples
in the specification of a regex whose job is to match finding ids**. The
liveness test does not even need to be run: the tokens are not pointers into a
record here, they are the shape the code parses. Stripping them would delete the
comment's entire content and leave "a bracketed finding id" describing a pattern
the reader could no longer picture.

This is the boundary the pass has been circling from the other side all day.
Everywhere else a coordinate was decoration on a name that already carried the
meaning, so removing it cost nothing. Here the coordinate **is** the meaning.
The distinguishing question is not "does this token resolve?" — none of these
four resolve, and `[M6-R]` may never have existed — but **"is this token
mentioned or used?"** A mention of a finding id is a citation and decays. An
*example* of a finding id is a specimen, and specimens do not decay.

The same file's other tokens (`H2` in a docstring about review-record headings)
are heading levels, already adjudicated. So the twin pair needed no edit at
all — recorded here because a completion check must be able to tell "audited,
nothing to do" from "not yet audited."

## Chunk C — the completion picture

**The actionable set is empty.** The corpus stands at **339 occurrences across
54 files**, down from **3,258**, and every remaining occurrence falls into one
of three accounted classes. The enumeration that produced this is the same one
recorded at the top of this ledger, re-run at the Chunk C head commit.

| Class | Occurrences | Files |
|---|---:|---:|
| Adjudicated keeps | 197 | 30 |
| Deferred — `bootstrap/_scaffold/` (AST baseline frozen) | 123 | 9 |
| Deferred — ceremony territory | 19 | 2 |

### The keeps, grouped by why

* **Markdown heading levels** — `H2` / `H3`, in the lifecycle parsers, the
  metrics extractors and their template twins. `##` and `###`.
* **Unicode control classes** — `C0` / `C1`, in the profile grammar, the byline
  identity scan, the security stack and the portable sweep runners.
* **The redundancy sub-gate's detectors** — `R1` / `R6` / `R7`, defined in
  `doctrine/consolidation-review.md`, cited in its dispositions log, and emitted
  at runtime by `scripts/quality_gate.py`.
* **Two self-defined in-file schemes** — `test_transition_lint.py`'s `A1`–`E9`
  (36 lines, no strays) and `test_lifecycle_stage_patterns.py`'s `T1`–`T9`. In
  both, the label names a row the code enumerates.
* **Two live fences** — `N4` (the gate preflight pair) and `M3` (the interpreter
  binding), each cited by an active plan.
* **One live principal ordinal** — `P1`, in `CAIRN_API_P1_CREDENTIAL`.
* **Four specimens** — the bracketed examples in `tools/lifecycle.py`'s
  finding-id regex comment and its twin.

**One stray was found inside a live scheme, at the very end.**
`test_lifecycle_stage_patterns.py:602` read `# T9 -- P2: classify once`. `T9` is
live, `P2` was a dead plan coordinate riding along beside it. Every earlier
sweep had treated that file as wholly keep and skipped it. **A file classified
as a keep still has to be read line by line** — the classification applies to a
scheme, not to a file, and a dead tag is perfectly happy sitting next to a live
one.

### What is deferred, and on whose authority

* **`bootstrap/_scaffold/` (123)** — the AST attestation baseline pins this
  package and is already out of date by 13 CHANGED symbols from earlier in this
  plan. Editing docstrings here adds to a re-anchor the Maintainer has not yet
  run. Filed at `191fb93`.
* **`test_reanchor.py` and `_gate_manifest.py` (19)** — both sit inside the
  re-anchor ceremony's surface, and `_gate_manifest.py`'s `M2-4` / `M2-5` cite
  `M2`, a **live** row in the active `ceremony-as-code` plan. Two reasons to
  leave them: the coordinates are not dead yet, and the files belong to another
  agent's in-flight work.

Both deferrals are **scope this plan accepted and has not delivered**, so they
are stated here as such rather than folded into the keeps. Whether they are
completed under this plan after the ceremony, or handed to a successor, is the
Maintainer's call — see AGENTS.md on accepted scope being a floor.

## Chunk D, and two findings the pass made about itself

**All 38 containers renamed**, 51 replacements across three suites, bodies
untouched. `TestP2AmendmentBScopeReduction` became
`TestScopeReductionNeedsMaintainerAllowance` — the exact name
`doctrine/rationale.md` and both `AGENTS.md` files already use as the worked
example, so the doctrine and the tree now agree rather than the doctrine
describing a name that had never been written.

Three sibling classes shared the stem `AuthoringTemplates` and two shared
`BothGateSurfacesAgree`; the coordinate had been the *only* thing distinguishing
them. They are now named by the contract each pins. That is worth noticing: the
coordinate was not merely uninformative there, it was **load-bearing for
uniqueness**, and removing it forced the naming work the original author had
skipped.

**One live cross-reference in engine code.** `bootstrap/_scaffold/config.py:112`
names a renamed class in a comment. Comments are not AST nodes, so the edit is
attestation-neutral — verified rather than assumed, by running the attestation
with and without it: identical output.

### The near-miss: correcting an accurate record with a bad measurement

While checking that, the attestation appeared to report **170 NEW / 0 CHANGED**,
against a filed row claiming **13 CHANGED**. That looked like a stale row on a
Maintainer-facing security item, so it was nearly rewritten. Two worktree runs
established the drift predates nothing — 29 passed before this plan's first
commit, 170 NEW from `7f40c87` onward — and the "correction" was drafted.

**The row was right.** `NEW` is an informational note printed for every live key
absent from the baseline; the failure classes are `CHANGED` / `MISSING` /
`DUPLICATE`, printed **without** the `note: ` prefix. The grep pattern
(`^note: [A-Z-]+`) could not match a `CHANGED` line, so it returned zero and the
zero was read as evidence. Counting again with the right pattern gives exactly
**13 CHANGED — 11 in `upgrade.py`, 2 in `config.py`** — the filed split, to the
symbol.

This is the fifth measurement-shaped error in the pass and the first that would
have *damaged* a correct record rather than merely wasting a round trip. The
pattern across all five is one thing: **a measurement that cannot observe the
thing it is aimed at returns a clean, confident, wrong answer.** A count without
names, a truncated repr, a display in place of a result, a needle that matches
the wrong line, and now a regex anchored to a prefix the target never carries.
The remedy is the same each time — check that the instrument can see a positive
case before trusting a negative one.

### The blind spot in the pass's own matching rule

Reading the renamed docstrings surfaced tag shapes the three classes cannot
match: **single letter with multiple digits** (`S12`, `R10`, `D14`) and
**letter-digit-lowercase** (`P6a`, `P6c`, `F1b`). Measured at **246 occurrences**
tree-wide, excluding lint-style codes. Not swept — the three classes are the
reviewed scope — and filed in `dev/PLANNING.md` with the number, alongside the
142 deferred occurrences, so both land in front of the Maintainer together.
