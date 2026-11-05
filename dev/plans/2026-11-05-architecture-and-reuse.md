# Plan: Discover existing code and review system shape

**Source proposal**: dev/proposals/archive/2026-11-02-codex-architecture-and-reuse.md
**Author**: Codex (plan author; high; runtime model identifier unavailable)
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-05
**In brief**: Ship a bounded code map and reuse leads, improve the architecture rubric, and test whether four visual views help people understand changing software.

## Source proposal

The Maintainer accepted the architecture/reuse proposal as heavy on
2026-11-02, including adopter delivery. All six outcomes remain: mapping,
neighbors, critical homes, rubric and release assessment, the four-view pilot,
and grouped strategy-retirement ownership. No graphics benefit is presumed.

## Scope

Extend the selected architecture-review module, its forkable rubric and script
registry. Keep the collector standard-library-only and byte-identical between
`templates/modules/team-gated/code_map.py` and `tools/code_map.py`. No target imports, automatic refactoring,
upload, publication, mandatory architecture module or new approval stage.

**Reuse.** Searches of `scripts/measurements.py`, `tools/gauge.py`,
`bootstrap/_scaffold/config.py` and the architecture module/rubric found AST
counting, history classification and existing delivery, but no map or
neighbors command. Reuse suitable static parsing/classification; exclude
target imports and inherited-environment Git launchers. Share history and
endpoint extraction with gauge, not a second collector. Git-backed work uses
board 2d's accepted-and-reviewed shared helper only; its current proposal is
awaiting-decision. Filesystem mapping and rubric work need not wait.

### Documentation / doctrine surface

Prescription belongs in the selected architecture module and reuse prompts;
software/CLI description belongs in `docs/code-map.md`; decisions and pilot evidence
remain in this plan. Keep five rubric lenses, adding accretion/reuse prompts
and examples within them. Link testing-discipline rather than duplicate its
instructions. Preserve adopter changes through existing merge/install paths.

Proposed paths:
- `templates/modules/team-gated/code_map.py`
- `tools/code_map.py`
- `bootstrap/tests/test_code_map.py`
- `docs/code-map.md`

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Bounded map, neighbor engine and installed CLI | Usual + Security plan review | Canonical collector/twin; selected-module mapping, preservation and public-entry tests |
| C2 | Critical homes, rubric and reuse guidance | C1; coordinate template window | Small named-home record and narrow divergence checks; legacy/new/mixed examples; selected-module release assessment |
| C3 | Shared history/endpoint collection and offline four-view pilot | Board 2d's safe helper implemented and reviewed; no unsafe fallback | Shared gauge collection, workstream attribution, cited semantic views, comparator results |
| C4 | Verification and grouped closeout assignment | C1-C3, usual + Security code reviews, wide Boundary B | Evidence, preserved scope and live board 12 retirement ownership; no human ceremony as a completion chunk |

## Acceptance criteria

**C1.** The real CLI and installed copy enumerate components/files, located
public functions/classes and docstring summaries; other languages remain
visible as unsupported analysis. Root/revision, errors, omissions and concrete
remedies accompany results. No incomplete scan reports clean evidence.
Neighbors rank normalized structure/name similarity for changed functions and
whole-tree release mode; similarity is advisory and justified shipped copies
remain valid. Every truncated comparison exposes its unsampled population.

The trusted collector/runtime sit outside inspected inputs. Reject linked or
reparse traversal, special files, escapes and unsafe output destinations;
escape terminal and HTML data. Never import inspected modules. Initial hard
budgets: 10,000 entries, 128 MiB total read, 1 MiB per parsed source,
2 million AST nodes, 20,000 function/class entries, and 1 million pair
comparisons. Stop parser work after 5 seconds per file or 30 seconds total,
and the complete command after 60 seconds; report affected work incomplete.
Use a terminable parser worker rather than a timer that cannot interrupt
parsing. These are work limits, not containment of a compromised host.

The starting scale is measured, not a benefit claim: a Git-backed clean
`bef11a3f` copy under Python 3.13.13 contained 894 tracked regular files,
43,087,905 bytes, 233 Python files, 6,879,186 Python bytes and 777,726 AST
nodes; its largest Python file was 301,308 bytes. Parsing/AST enumeration took
0.886 seconds with no syntax errors. This excludes untracked and hostile
inputs. Boundary, overflow and deep/pathological controls must validate every
budget through the real command before implementation evidence calls it
enforced. Record legitimate incomplete results, not an inflated limit solely
to make a sample pass.

**C2.** Name existing safe-reading, containment, terminal-encoding and Git
owners in the architecture record. Narrow duplicate-pattern guards fail on
planted dangerous divergence and allow documented wrappers/verbatim copies;
no universal clone ban. Legacy, new and mixed examples produce either a
specific justified action or adequate-practice result. Distinguish functional
test scope from execution cost using plan 6's guidance. Selected-module
releases record map, neighbors, growth and ranked consolidation candidates
with preserving tests, not a deletion quota or agent score.

**C3.** Compare manual board/gauge/rubric practice, the existing CodeCharta
product and a small offline report reusing LHM's scope-map interaction. Pin
and assess the comparator's license, execution and data transmission before
use; it is not a shipped dependency. Cover workstreams, system shape,
capabilities and growth. A fresh reviewer prepares duplication, drift,
capability-overclaim and justified-growth answers before the author trials
each method. Record accuracy/time, setup and annotation effort, false alarms
and misses; distinguish agent trials from human evidence. Reject the visual
approach if it improves neither understanding nor decisions or needs guesses.

History extraction is shared with gauge; project classifications remain
project-owned. Keep editing activity separate from endpoint changes, count
shared-file growth once, and show conflicting/unattributed ownership and
working-tree material explicitly. Shape/capability views cite workflows or
declarations, never infer capability or unused code from symbols alone.
Compare bottom-up summaries with map-first discovery. The report works with
network disabled, escapes hostile data and has non-graphical equivalents.
No finished four-view platform or per-folder README promise is introduced.

**C4.** Board 12 retains the release-closeout agent's grouped retirement
assignment and the delivery-sequence note's complete retirement table.
Permanent guidance has durable homes; unfinished scope has an exact live
home. Testing alone cannot retire outside-practices, nor a Git fix the broad
security strategy. Human signing/publication remains separately unpassed.

## Scope delta

**Scope delta**: preserved. C3's dependency sequences work; it does not remove
the pilot or allow this plan to archive with it unfinished. The source
proposal assigns grouped final retirement to the release-closeout agent;
C4 delivers that assignment, not an early claim that every note is retired.

## Verification

Boundary A uses `tools/test_tiers.py for` on owned source commits. Extend
`bootstrap/tests/test_code_map.py` through the actual CLI/installed copy: mixed languages,
malformed/deep/oversized input, containment/races, control/HTML payloads,
planted imports, executable Git settings, each budget and neighbor sampling.
Use existing scaffold, manifest, reference-script and module-merge contracts
for delivery and preservation. Guard mutations must fail their named check.

S1/S4/S5 retain the source trust boundary and honest incompleteness; C1 owns
filesystem/parser/display probes and C3 owns shared-helper/no-execution and
offline probes (S2/S3). No scientific equation changes; capability evidence
still needs an independently grounded example or workflow. Usual and Security
code reviews independently challenge evidence without replaying the full
iteration set. After fixes, run one wide Boundary B union on a clean final
Python 3.13.x commit, recording omissions and timing; batch compatible ranges
only when their sources/consumers match. Claim, link, snippet, neutrality and
diff gates apply. No routine full certification, real key or ceremony.

Opening checks on an isolated candidate based on `6b1785d3`, Python 3.13.13:
scoped claim/link/content checks, snippet sync, neutrality, redundancy and
diff whitespace passed. Ten external links were not probed. This is plan
preparation, not implementation, a pilot trial or tree certification.

**Preparation elapsed**: approximately 10 minutes. **Tokens**: unknown.

## Plan review -- Codex Terra (MEDIUM) -- 2026-11-05

**Foundations**

1. **Should this happen as framed?** Yes. C1-C4 retain the accepted map, neighbors, critical homes, rubric and release assessment, four-view pilot and grouped retirement assignment, including selected-adopter delivery -- accepted proposal, Proposal 1-6 and Decision; plan, C1-C4.
2. **Best alternative.** Reuse existing collection and compare manual practice and an existing product, as planned; a new platform adds cost before benefit is measured, while omitting the pilot loses an accepted outcome -- accepted proposal, Alternatives and Proposal 5; plan, C3.
3. **What would show it wrong?** A real-entry budget overflow reported as complete, a target import executed, or a pilot unable to identify independently prepared cases better than its comparators would challenge delivery or the visual approach -- plan, C1/C3 and Verification; accepted proposal, S2-S5.

Reviewed commit: f6fdf95a2d6070078ab390c92d07f5f744882d00

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: SHIP

The measured scale is a starting point, not evidence of benefit or hostile-input safety. C1 requires real-command limits and visible incompleteness; C3 gates Git-backed work on the separately reviewed safe helper, keeps independent answers and comparator costs, and does not turn symbols into capability claims. C2 preserves adopter edits and meaningful release assessment; C4 retains the grouped retirement assignment rather than declaring unfinished strategies complete.

**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Coverage**: Committed plan, accepted proposal, reviews, response and Decision, current plan template, module selection, existing Git call sites and board dependency/retirement ownership. **Not covered**: future collector, installation or mutation tests, comparator licensing or execution, pilot outcomes, exhaustive readers, Security Review or full suite.
