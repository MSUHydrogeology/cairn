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
| 2026-05-28 | redundancy / R6 | `templates/modules/team-gated/_intent/record_io.py:279` | def `iter_log` | accepted-exemption-added | Public-API iterator over the intent log for adopter tooling; unreferenced from within Cairn's own tree.  Added to `_UNUSED_DEF_WHITELIST` at first-dogfood time. (Citation re-pointed from the pre-split `intent.py:456` to the owned `_intent/` engine package; `iter_log` lives in the record-I/O subsystem after the phase-A 5-way split.) |
| 2026-05-28 | redundancy / R6 | `bootstrap/tests/**` | ~60 `Test*` class defs | fixed | Pytest discovers test classes by `Test*` name pattern, not by static reference.  R6's first dogfood pass surfaced ~60 such false positives.  Fixed in this Chunk 8 commit by scoping R6 out of `bootstrap/tests/` (new `_R6_EXCLUDE_DIRS` tuple) AND skipping `Test*` / `test_*` names defensively in `_run_r6_redundancy` (so a misplaced test file under `scripts/` or `bootstrap/<not-tests>/` would not trip either). |
| 2026-05-28 (code-review sharpening) | neutrality | the retired lifecycle-metrics module (lines 139, 187, 573) | `Codex` (2x), `Claude` (1x) | fixed | Pre-existing illustrative docstring examples shipping to adopters via the lifecycle_metrics module install.  Rephrased to placeholder names (`<reviewer>`, `Alice`, `Bob42`).  Exposed by the P1 code-review fix that closed the template-leak short-circuit; the gate is now doing its job and surfaced the latent leaks. |
| 2026-05-28 (code-review sharpening) | neutrality | `templates/modules/team-gated/link_check.py:158` | `Codex` | fixed | Pre-existing review-attribution comment inside the SSRF guard docstring.  Rephrased to "(caught in review, finding 1)" -- preserves the historical signal that a review caught this case without leaking the reviewer's vendor name into adopter trees. |
| 2026-08-03 | redundancy / R6 | `bootstrap/_scaffold/_guard.py:108` plus 10 sibling findings (full pass output in `2026-08-03-claude-r6-unused-def-blindspot`) | 11 defs reported "never referenced" -- among them `install`, `render_compatibility_matrix`, `_find_cairn_root`, and four `_onboarding` helpers counted twice via their shipped twins | fixed | All 11 were false and all had one shape: the def's only in-corpus reference is a `from X import Y` package-facade re-export, and the reference harvester collected only `ast.Name` / `ast.Attribute` nodes -- an import's `alias` children are neither, so every facade-exported def read as dead.  The sharpest was `install`, the engine import boundary that installs the `EngineFinder` and refuses an out-of-tree cached engine child (the SR1 containment control): R6 advised deleting it at `fail` severity.  Four more named files under `templates/modules/default-on/_onboarding/`, which the scaffold copies into adopter trees.  Fixed in this commit by one `ast.ImportFrom` branch that harvests the imported symbol name only -- not the local `as` binding, and not plain `import x.y` (both wider variants were simulated; each collapses this corpus to the same residual set while suppressing strictly more, so the narrower one wins).  Pass total 13 -> 2 findings, 10 `fail` -> 0 `fail`.  The two survivors -- `_per_role_per_tier_summary` and `_author_reviewer_matrix`, both `info`, both in its engine package -- are genuinely unreferenced and are deliberately left **undispositioned** here: whether they are dead code or an unfinished metrics feature is a content call about a shipped module, not a call about the detector.  The next pass owns them. |
| 2026-10-18 | neutrality | `scripts/quality_gate.py` (the `templates/` branch, `_NEUTRALITY_FILE_SUFFIXES`, `_VENDOR_DENYLIST`) | whole-line HTML comments, `.json` and `.txt` files under `templates/`; `Copilot`, `Windsurf`, `Cline`, `OpenCode` | fixed | The gate skipped whole-line comments in `templates/`, read neither `.json` nor `.txt` there, and lacked four names the routing table lists. Widening it moved the count from 74 to 81 and only up: the seven added are three `reviewer="Claude (Implementation)"` credits and the four new names on one routing-table line. Nothing was exempted to get there. |
| 2026-10-18 | neutrality | 54 lines under `templates/` (skills 13, onboarding package 27, scanner and intent tool 3, Markdown 8, `reviewer=` credits 3) | reviewer credits, `modflow_tools`, harness names in comments, docstrings, one routing-table `_doc` string and prose | fixed | Reworded to the property the text relied on, or to "the reference deployment"; no program changed (docstring-stripped `ast.dump` equal for all ten edited modules). Twins were edited in the same commits and 12 lockfile records finalized. The old wording stays in `git log -p`. |
| 2026-10-18 | neutrality | `docs/agent-team-onboarding.md` (8), `doctrine/lifecycle-contract.md` (5), `doctrine/rationale.md` (3), `bootstrap/tests/fixtures/skills/README.md` (4) | 20 token occurrences: `Claude`, `Codex`, `Cursor`, `Gemini`, `GPT`, `Antigravity` | accepted-exemption-added | Illustrative mentions in Cairn's own documents, which do not ship. Each took a same-line `vendor-ok` marker with a one-sentence reason (one code fence in `docs/agent-team-onboarding.md` took a block marker instead, since a marker inside it would change the example). The markers add text only: removing them gives back the parent bytes, and no line was added to either doctrine file. `info=` rose by 21. |
| 2026-10-18 | neutrality | `docs/DOCUMENTATION_PLAN.md` (six lines), `bootstrap/tests/fixtures/skills/README.md:35` | `modflow_tools` (6x), `Codex` | fixed | Six lines said Cairn does not yet keep its own `dev/` tree, which has been untrue for months; they now say where Cairn's records are, each checked with a command. The fixture README's credit was reworded and keeps its reason. |
| 2026-10-18 | neutrality | the whole gate | none: `fail=0` | recorded | Why zero should hold this time. `29ffeea6` reached `fail=0` on 2026-05-28 and `dbc09557` put the first reviewer credit into `_onboarding/` that afternoon, so the first refill took hours. Two things have changed since: Boundary B runs this gate on every plan (`5f6ecccc`, 2026-08-05), and `013847b6` (2026-08-18) bars process coordinates such as reviewer credits from code comments. |
| 2026-10-18 | neutrality | the claim "zero" | what zero does not cover | recorded | Zero means no listed name, as a whole word in its normal capitals, in the file types the gate reads. It does not cover lower-case or joined spellings, hidden characters, names missing from the list, file types not on the list, or someone hiding a name on purpose. Outside `templates/`, a line or block carrying a `vendor-ok` marker is exempt by design (those files do not ship), so `info=` is the only sign of a name added under a marker. Standing trigger: a Boundary B record after archive that shows a neutrality failure the change under test did not introduce means the commit hook is owed. The trigger is Boundary B's own second command (`AGENTS.md` > Verification boundaries), which a person runs; no hook runs the gate today. |
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
