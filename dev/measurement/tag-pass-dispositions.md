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
| `tools/lifecycle.py` + twin | `S1`, `S2`, `R2`, `R6`, `R7`, `R3` | **Inside a byte-pinned security fence.** Five lines sit within `_probe_interpreter` / `_resolve_interpreter` / `_warn_stale_once`, which `bootstrap/tests/test_lifecycle_brief.py` pins byte-and-AST-identical. `AGENTS.md` makes the local interpreter binding a Security-Review surface, and the pin's own message says a change "STOPS for a new Security Review". Re-pinning is that review's commit, not this pass's. Revised and then **reverted** when the fence caught it. |

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