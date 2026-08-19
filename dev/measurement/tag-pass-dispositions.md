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

## The frozen gate surface — why this pass leaves the gate red

**82% of Chunk C's remaining work is on frozen gate surface**, and neither the
plan nor its five review rounds anticipated it.

`bootstrap/tests/_gate_manifest.py::_frozen_files()` globs `bootstrap/*.py`,
`bootstrap/tests/**/*.py`, `templates/modules/**/*.py` **and** `scripts/*.py`.
Any byte change to those files — a comment included — puts them out of sync with
`bootstrap/tests/fixtures/gate_manifest.json` and reports `FROZEN-MODIFIED`.

Measured at the C2c commit:

| Surface | Files | Remaining candidates |
|---|---:|---:|
| frozen gate surface | 120 | **1543** |
| free surface | 17 | 336 |

**What this pass did not do.** It did **not** regenerate the gate manifest.
Regeneration is step 2 of `bootstrap/REANCHOR_RUNBOOK.md`, whose step 3 is a
supervised **Maintainer-authored** commit, and the runbook states that
confirming the hashes out of band *"is what makes this a reviewed pin and not a
self-generated one."* The plan already fences exactly this for Chunk D (D2,
MAINTAINER-GATED); it simply did not foresee that Chunk C's comment edits land
on the same surface.

**Maintainer decision, 2026-08-19:**

> *"I think we should land this one -- the other plan will re-anchor"*

So C2c lands with the gate red, and the re-anchor is batched into the
`ceremony-as-code` plan's own ceremony, which covers this surface anyway. One
ceremony then clears C2c, the remaining 1543 frozen candidates, and Chunk D's
renames together.

**The red gate is accurate, not a defect**: the frozen surface genuinely did
change. What would be a defect is a green gate over changed bytes.
