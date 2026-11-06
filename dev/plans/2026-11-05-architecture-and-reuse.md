# Plan: Discover existing code and review system shape

**Source proposal**: dev/proposals/archive/2026-11-02-codex-architecture-and-reuse.md
**Author**: Codex (plan author; high; runtime model identifier unavailable)
**Status**: implementing
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

Implementation paths:
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

## Plan review -- Codex Sol (HIGH) -- 2026-11-05

**Foundations**

1. **Should this happen as framed?** Yes. C1-C4 preserve the accepted outcomes while bounding untrusted inspection, denying target execution and retaining independent pilot answers -- accepted proposal, Proposal 1-6/AR-S1-S2 response/Decision; plan, C1-C4.
2. **Best alternative.** Keep one static collector and compare manual practice with the existing product before investing in graphics, as planned; another collection engine or platform adds upkeep, while omitting the pilot loses accepted scope -- plan, Reuse/C3; accepted proposal, Alternatives.
3. **What would show it wrong?** Real-command overflow/deep-input cases must terminate incomplete, planted imports/Git settings must not execute, hostile display data must stay inert, and independent pilot answers must expose misses -- plan, C1/C3 and Verification; accepted proposal, S2-S5.

Reviewed commit: f6fdf95a2d6070078ab390c92d07f5f744882d00
Ordinary review read: a50da78b; path released directly by its reviewer.

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none
**Verdict**: ACCEPT -- plan only.

Finite entry/read/source/AST/symbol/comparison limits, interruptible parser work
and 5/30/60-second deadlines make resource claims falsifiable. Truncated
neighbors expose unsampled work; honest incompleteness is allowed. Measured
starting scale proves neither hostile-input safety nor host containment.
Boundary/overflow controls remain owed for every budget.

Existing reuse candidates contain unsafe-for-this-purpose paths: measurements
can import from its supplied root, and gauge inherits Git configuration.
Scope excludes both behaviors. Git-backed work waits for 2d's accepted,
implemented and reviewed helper; its pending Decision grants no fallback.
C1 separately requires root/link/reparse/race and unsafe-output tests, terminal/
HTML escaping and no target imports; C3 requires offline output.

Existing verbatim-install/preservation tests are extension homes, not proof of
future delivery. C2's named critical owners and divergence guards preserve
justified wrappers/copies, not a generic clone ban. Comparator assessment,
independently prepared answers and agent/human evidence labels make
self-scored graphics claims insufficient evidence. Grouped retirement remains live.

**Elapsed**: unknown. **Tokens**: unknown.

**Coverage**: Committed plan/source/reviews/response/Decision, ordinary review,
current template, module registry, collection call sites and concrete
verbatim/preservation test bodies. **Not covered**: future collector or budget
enforcement, filesystem races, comparator licensing/execution, pilot results or
all readers. No tests or suite run; output text cannot authenticate its inputs.

## Plan response -- Codex Luna (Implementation, LOW) -- 2026-11-05

Both required plan reviews recommend proceeding and report no findings. I leave
the operative plan and all accepted C1-C4 outcomes unchanged. Per the parent
High's authorization in this task handoff, this fold advances the plan to
`ready-to-implement`; no Maintainer Decision or scope change is asserted.

**Elapsed**: approximately 2 minutes. **Tokens**: unknown.

## Implementation log -- C1 filesystem slice -- Codex Terra (MEDIUM) -- 2026-11-05

The optional module installs a bounded filesystem map and advisory neighbors:
`9547bf74` adds the collector, its identical template, mapping, tests, docs
and tier entry. It reports nested public definitions, compares private and
local functions, counts work after failed reads, and declares metadata
omissions. Deadline controls exercise the real `_walk` and parser worker with
an injected clock; that particular control is not a public CLI test. The
interim Windows missing-capability case remains incomplete within C1.

Parent High corrected a gate test's legacy-versus-roster oracle in `62dfccd7`
(about four minutes; tokens unknown). `7f9fa112` updates module installation,
adoption and both Python-count tests; `cfffd42c` adds the required MIT headers
to both twins; `ed6f1136` updates the total manifest-row check while requiring
the exact code-map row. No trust policy, baseline, anchor or roster changed.
The author used Python 3.13.13; total author elapsed and tokens are unknown.

Parent High reports a separate real CLI workflow on clean `9547bf74` at
`/private/tmp/cairn-map-workflow-9547bf74`: exit 0, 900 files (236 parsed
Python), 1,001 entries, 7,374 definitions, 792,509 AST nodes, 6,963,547 bytes,
one declared `.git` omission and no diagnostics; command 10.305s. This was
under concurrent load, not a benchmark, benefit claim or certification.

## Iteration verification -- Codex Terra (MEDIUM) -- 2026-11-05

Canonical interpreter: `/Users/kendal30/conda_envs/lhm/bin/python3.13`,
Python 3.13.13. Git-backed checking copies had clean pre/post states, branch
`0.7-dev`, and the existing `refs/cairn/gate-anchor` at
`977b5250abed59badd06b4940dccd39324644705`. The parent verified that anchor's
signature separately; these checks did not sign, re-anchor or change it.

* At `9547bf74b620673c5ea330fe696c2379419a5d0a`, `tools/test_tiers.py for`
  selected 60 files for `CHANGELOG.md`, `bootstrap/_scaffold/config.py`,
  `bootstrap/tests/test_code_map.py`, `bootstrap/tests/test_reference_scripts.py`,
  `docs/code-map.md`, both code-map copies and `tools/test_tiers.json`. Exact
  selection: `/private/tmp/cairn-c1-a-9547bf74-selection.txt`. The first 30
  selected files ran with `python3.13 -m pytest -q --tb=short --junitxml=`
  `/private/tmp/cairn-c1-a-9547bf74-batch1.xml`: 1,503 passed, 1 failed,
  9 skipped in 316.35s. The other 30 used the same command and
  `/private/tmp/cairn-c1-a-9547bf74-batch2.xml`: 2,692 passed, 3 failed in
  836.46s. The failures were the gate roster oracle, module spec count,
  template Python count and adoption count; the skips were native-only.
* At `62dfccd7999b9778eb96fc9d5e843d9c5937fe99`, the nine-file oracle delta
  used the same pytest options and `/private/tmp/cairn-c1-delta-62dfccd7.xml`:
  968 passed, 2 failed in 305.46s, retaining the spec and adoption failures.
  The files were `bootstrap/tests/test_board_json_contract.py`,
  `test_gate_preflight.py`, `test_quickstart_sequence.py`, `test_reanchor.py`,
  `test_scaffold.py`, `test_security_marker.py`, `test_upgrade.py`,
  `test_upgrade_module_additions.py` and `test_verify_ref.py` (all under
  `bootstrap/tests/`).
* At `7f9fa112c269be18171aebc6286eaab345c23452`, the 20-file correction
  selection (`/private/tmp/cairn-c1-fix-7f9fa112-selection.txt`) used the same
  options and `/private/tmp/cairn-c1-fix-7f9fa112.xml`: 1,308 passed, 3 failed
  in 340.36s. Two failures exposed missing SPDX headers and one exposed the
  total manifest-row pin. These were corrected in the commits above.
* At `ed6f11360bfc4c49c6c24333fa3dfab06d85cb61`, the correction union for
  `test_gate_preflight.py`, `CHANGELOG.md`, `test_scaffold.py`,
  `test_security_lint.py`, `test_notice_install.py`, `test_upgrade.py` and
  both code-map copies selected 22 files. Exact names:
  `/private/tmp/cairn-c1-finalfix-ed6f1136-selection.txt`. The same pytest
  options with `/private/tmp/cairn-c1-finalfix-ed6f1136.xml` produced 1,369
  passed and three deprecation warnings in 362.56s. The prior failed runs are
  not a green same-SHA union; unchanged passing observations are retained.

`python3.13 scripts/check_cairn.py CHANGELOG.md docs/code-map.md`, snippet
sync, neutrality and twin byte comparison passed on the final copy; three
external links were not probed. An extra direct content scan with URL checking
flagged two pre-existing changelog GitHub links; this is separate from the
configured passing gate. The 30-second iteration target was exceeded; measured
files above 10 seconds are recorded in the suite-consolidation plan. C1's
Windows capability and remaining work, C2-C4, usual and Security code reviews,
and wide Boundary B remain open. No full certification was run.

## Implementation log -- C2 rubric and helper homes -- Codex Sol (HIGH) -- 2026-11-05

`29f0835f` delivers the five-lens rubric additions, fictional legacy/new/mixed
examples, selected-module release-assessment instructions and Cairn's current
`dev/architecture_review.md`. Author applications of the cases are recorded
there, not represented as human or independent-review evidence.

The existing kernel test home now checks two owner names across three explicit
runtime roots. Six planted forks are detected; owner-copy and delegation
controls pass. This is a narrow name-fork guard, not semantic equivalence,
renamed-clone detection or an assurance about every helper body. Existing
owner behavior and twin checks remain. The installed-copy test also checks
the rubric's five lenses/examples and preservation of an adopter edit.

**Boundary A:** clean committed `29f0835f`, separate Git-backed copy, Python
3.13.13, clean pre/post state. `tools/test_tiers.py for` on the source commit's
six changed paths selected eight files: `test_board_json_contract.py`,
`test_code_map.py`, `test_quickstart_sequence.py`, `test_scaffold.py`,
`test_session_kernel.py`, `test_upgrade.py`, `test_upgrade_module_additions.py`
and `test_verify_ref.py`, all under `bootstrap/tests/`. Pytest with `-q
--durations=0 --junitxml=/private/tmp/cairn-architecture-c2-a-29f0835f.xml`
and those files passed 446 cases, zero failures/skips, in 103.51 seconds
pytest / 107.47 seconds wall. The iteration target was missed; three slow-file
observations are in the consolidation plan. Earlier focused controls passed
eight owner checks and one installed-copy check; these are not added to 446.
Claim, content, snippet, neutrality, redundancy and diff checks passed on
isolated candidate bytes; three external links were not probed.

C1's Windows capability, C3's safe-Git dependency and independent four-view
pilot, C4, ordinary/Security code reviews and final wide Boundary B remain
open. The release assessment is explicitly unfinished; this checkpoint does
not close the whole plan or claim complete growth/capability evidence.
No suite certification, trust operation or private inspection occurred.
**Elapsed**: 107.47 seconds wall for mapped A; overall elapsed unknown.
**Tokens**: unknown.

## Implementation log -- C1 native Windows capability -- Codex GPT-6 Luna (Low) -- 2026-11-06

On the local Windows 11 ARM64 VM, explicit Python `C:\ProgramData\miniconda3\python.exe`
reported 3.13.17. The descriptor probe found `os.open` and `os.stat` lack
`dir_fd`, `os.scandir` lacks fd support, and `O_NOFOLLOW` / `O_DIRECTORY` are
absent. From committed source at `f14169e83110130eb30525330a7d4a990d5cc8d6`
(31,215 bytes; SHA-256 `b72922068e3b6cf62121461c5ef3df64bfafba70cedd1428fc98713b9bdcd7ff`),
the real isolated CLI ran against a tiny synthetic Python/TypeScript/Markdown
fixture. Both default map and `--changed sample.py` returned exit 1, status
`incomplete`, zero entries/files, and `secure-traversal-unavailable` with the
no-weaker-fallback remedy. Changed mode returned no neighbors because traversal
did not begin. Reported command times were 0.091s and 0.102s; SSH wall times
were 0.579s and 0.398s. No inspected code ran; no unsafe-path probe was
attempted after the capability gate. This confirms honest incompleteness on
native Windows, but native mapping and neighbor behavior remain unmet; C1 stays
open. No full test file, suite, or certification ran.

**Elapsed**: approximately 8 minutes. **Tokens**: unknown.
