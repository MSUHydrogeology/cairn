# Consolidation review -- the manual half of the redundancy gate

`scripts/quality_gate.py`'s redundancy sub-gate ships **R1** (n-gram
overlap detection) and **R6** (stdlib AST unreferenced-def detection)
automatically.  Two pieces of the original Sweep-G consolidation
review stay **manual** because no static tool can do them honestly:

* **R7 -- capability necessity.** Per dimension, are all the listed
  capabilities still warranted, or has the surface accumulated noise
  that should be pruned?  Answering well requires judgment about
  what each capability is *for*; the R6 detector finds dead defs,
  not dead capabilities.

* **R1's layer-contract filter.** R1 surfaces n-gram overlap
  candidates; the layer contract (L1 = doctrine prescription, L2 =
  condensed instantiations of L1) means some overlap is **expected
  by design**.  A condensed instantiation legitimately re-uses
  doctrine phrasing.  R1's tunable threshold reduces noise, but the
  "is this overlap legitimate?" call is per-candidate human judgment.

This doc carries the **manual disposition checklists** + the
**dogfood disposition log** (a dated table of findings + dispositions
the gate has surfaced over time, so audit trails outlive the
commit-body summary).

## R7 -- capability necessity (per-dimension checklist)

Run pre-cut, ahead of the dogfood pass below.  For each dimension
file under `dimensions/`:

1. **List the capabilities** the dimension currently advertises.
2. For each capability, answer:
   * **Is it load-bearing?**  Cite at least one Cairn surface
     (template, doctrine, scaffold path) that depends on it.
   * **Is its surface area justified?**  A 5-line capability with
     no dependents is a stronger removal candidate than a 50-line
     capability with five dependents.
   * **Has it been demonstrated end-to-end?**  An undemonstrated
     capability is a Layer 5 candidate, not a Layer 3 promise.
3. **Decide**: keep / shrink / remove / promote / demote.

R7 outputs feed the next major-version cut, not the 0.2.x
point-release window.

## R1 layer-contract filter (per-candidate checklist)

For each R1 candidate (an n-gram-overlap pair the tool surfaces),
ask:

1. **Are both passages prescriptive doctrine (both L1)?**  If yes,
   one is redundant -- consolidate.
2. **Is one L1 and the other an L2 condensed instantiation?**  If
   yes, the overlap is the layer contract working -- expected;
   leave it.  Note the candidate in the dogfood disposition log
   below with status `accepted-layer-contract`.
3. **Are both L2?**  Two condensed instantiations of the same L1
   may be redundant: do both serve distinct *roles* (different
   modules, different audiences)?  If yes, leave.  If no, merge.
4. **Is one prose and the other a code comment quoting it?**
   Comments-quoting-prose is the standard pattern -- leave it
   unless the prose has drifted and the comment hasn't.

## Dogfood disposition log

Each dogfood pass of `quality_gate.py` appends a dated table row
naming the per-finding disposition.  This is the **durable audit
trail**: commit bodies summarize totals, this log carries the
per-finding rationale (the gate will surface false-positives + noise
between true findings; without the log, the next reader cannot tell
which the prior pass dispositioned as which).

<!-- vendor-ok-begin: dispositions log -- the "Token / Candidate" column legitimately quotes the tokens that the gate surfaced; not a vendor leak in framework doctrine but a literal audit of what was reviewed and how -->
| Date | Sub-gate | File:line | Token / Candidate | Disposition | Rationale |
|---|---|---|---|---|---|
| 2026-05-28 | neutrality | `bootstrap/fidelity-check.md` (lines 5, 308, 309) | `modflow_tools` (3x) | accepted-exemption-added | Doc names modflow_tools as the case-study reference for fidelity-check practice; legitimate doctrine.  Wrapped both occurrences in `<!-- vendor-ok-begin: ... -->` blocks. |
| 2026-05-28 | neutrality | `docs/quickstart.md:24-26` | `Claude`, `Codex`, `Cursor` | accepted-exemption-added | Illustrative list of adopter-side tools; the surrounding prose explicitly says "Cairn is vendor-neutral".  Wrapped in `<!-- vendor-ok-begin: ... -->`. |
| 2026-05-28 | neutrality | `docs/quickstart.md:189` | `Cursor` | accepted-exemption-added | Editor-name list (VS Code, Cursor) -- illustrative options for adopters opening their disposable repo.  Wrapped in `<!-- vendor-ok-begin: ... -->`. |
| 2026-05-28 | neutrality | `doctrine/consolidation-review.md:67` (this file) | `Codex` | fixed | The phrasing cited the reviewer-attribution rather than the substance.  Rewrote inline to drop the cross-agent name (doctrine doc should not carry session-specific reviewer cites). |
| 2026-05-28 | redundancy / R6 | `templates/modules/default-on/claim_check.py:670` | def `check_text` | accepted-exemption-added | Public-API export for adopters wanting to scan pre-loaded text directly; Cairn's own callers use `check_file`.  Added to `scripts/quality_gate_unused_def_whitelist.py` with rationale comment. |
| 2026-05-28 | redundancy / R6 | `templates/modules/team-gated/_intent/__init__.py:515` | def `iter_log` | accepted-exemption-added | Public-API iterator over the intent log for adopter tooling; unreferenced from within Cairn's own tree.  Added to `_UNUSED_DEF_WHITELIST` at first-dogfood time. (Citation re-pointed from the pre-split `intent.py:456` to the owned `_intent/` engine package at intent-split phase A.) |
| 2026-05-28 | redundancy / R6 | `bootstrap/tests/**` | ~60 `Test*` class defs | fixed | Pytest discovers test classes by `Test*` name pattern, not by static reference.  R6's first dogfood pass surfaced ~60 such false positives.  Fixed in this Chunk 8 commit by scoping R6 out of `bootstrap/tests/` (new `_R6_EXCLUDE_DIRS` tuple) AND skipping `Test*` / `test_*` names defensively in `_run_r6_redundancy` (so a misplaced test file under `scripts/` or `bootstrap/<not-tests>/` would not trip either). |
| 2026-05-28 (code-review sharpening) | neutrality | `templates/modules/default-on/lifecycle_metrics.py` (lines 139, 187, 573) | `Codex` (2x), `Claude` (1x) | fixed | Pre-existing illustrative docstring examples shipping to adopters via the lifecycle_metrics module install.  Rephrased to placeholder names (`<reviewer>`, `Alice`, `Bob42`).  Exposed by the P1 code-review fix that closed the template-leak short-circuit; the gate is now doing its job and surfaced the latent leaks. |
| 2026-05-28 (code-review sharpening) | neutrality | `templates/modules/team-gated/link_check.py:158` | `Codex` | fixed | Pre-existing review-attribution comment inside the SSRF guard docstring.  Rephrased to "(caught in review, finding 1)" -- preserves the historical signal that a review caught this case without leaking the reviewer's vendor name into adopter trees. |
<!-- vendor-ok-end -->

Disposition vocabulary:

* **fixed** -- the gate caught a real drift; the implementing
  commit corrects it.
* **accepted-layer-contract** -- R1 overlap that is the layer
  contract working (L1 + L2); no code change.
* **accepted-noise** -- the gate's heuristic flagged a non-issue
  this iteration; left as-is (and noted here so the next
  reader sees the prior disposition).
* **accepted-exemption-added** -- a sanctioned exception (a
  `vendor-ok` directive added in this commit; cite the diff).
* **wontfix** -- the gate is wrong for this finding's shape and
  the cost of fixing the gate exceeds the value here; ledger as a
  candidate `quality_gate.py` follow-up.

The dogfood log is **not** a commit-message substitute -- the
commit body still summarizes the totals (count fixed, count
accepted, count wontfix) for the `git log` skim.  This log carries
the per-finding rationale that does not fit in a commit body.
