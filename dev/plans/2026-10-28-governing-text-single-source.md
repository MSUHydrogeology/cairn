# Plan: Governing text inventory and routing

**Source proposal**: dev/proposals/archive/2026-10-28-codex-governing-text-single-source.md
**Status**: awaiting-code-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-28
**In brief**: Map where rules come from and reach adopters before choosing how to reduce repeated editing.

## Source proposal

The accepted proposal makes inventory and Maintainer routing precede consolidation. The Decision also asks why a
`doctrine/` folder exists when it is not shipped to adopters, and whether its
contents belong in `dev/rules` or `docs/` instead.

## Scope

Inventory the published doctrine and the internal and installed governing
files, including `AGENTS.md`, `dev/agent_collaboration.md`, and proposal and
plan templates. Include affected modules, boards, the documentation plan and
its forkable template. The routing choice may lead to changes in these surfaces;
Preserve adopted obligations and deliberate adopter differences.

**Reuse.** N/A: no code added. Use the existing installer, profile definitions,
rule tests, claim and link checkers, and applicable ceremonies.

### Documentation / doctrine surface

Examine `doctrine/`, `docs/DOCUMENTATION_PLAN.md`,
`templates/modules/default-on/documentation_plan_template.md`, internal and
installed governing text, and affected modules and boards. Compare their actual
purposes and history, including the Maintainer's `dev/rules` alternative;
do not assume the present placement is justified.

C1 outputs:
- `dev/strategy/2026-10-28-codex-governing-text-inventory.md`
- `dev/plans/2026-10-28-governing-text-single-source/doctrine-sections.tsv` (per-heading evidence)

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Inventory current rules, history, installed reach and editing cost | Plan review; may run alongside other plans | Evidence and routing alternatives in `dev/strategy/2026-10-28-codex-governing-text-inventory.md` |
| C2 | MAINTAINER-GATED routing choice | C1 refreshed after model-floor and scoped-verification implementation and code review; Maintainer chooses before rule relocation or deletion | Chosen routing and explicit authorization in this plan |
| C3 | Conditional edits and property guards | C2; scoped-verification implementation and code review complete before shared governing edits; test-trust-boundary work complete before frozen prose tests change | Safe consolidation, installed guards and comparison evidence |
| C4 | Verify and hand off | C3; applicable frozen-file and doctrine ceremonies | Scoped verification record and independent code review |

## Acceptance criteria

### C1

For every doctrine section record stated and observed purpose, relevant history,
prescription versus explanation, and relationship to `docs/` and `dev/rules`.
Compare retaining, moving and other evidence-supported routing without assuming
one wins. Inventory installed and internal rule homes, explanations, pointers,
duplicates, affected modules and boards, and owning or wording-pinned tests.
Inspect the installer's mapping and real small and fuller profile installs;
separate source claims from observed output and trace mandatory reachability.
Measure one operating-rule and one template-instruction edit: files, tests,
ceremonies and installed reader usability. Recommend a routing with its losses
and unresolved questions. Refresh affected evidence and mapping against the
post-model-floor and post-scoped-verification reviewed HEAD before C2; commit
the inventory before the fence.

### C2

Present the inventory and alternatives to the Maintainer. Record the choice and
its exact authorization before any operative rule is relocated or deleted.
Unresolved installed homes or mandatory pointers block those edits; published
citations alone cannot carry an installed obligation.

### C3

Change only evidence-supported redundancy or misplacement within the chosen
routing; retain installed obligations, usable triggers and distinct semantics.
Compare the two C1 edits after the change using the same measures; at least one
must become simpler without loss of reach or meaning. An 80–120-line template
length is advisory. If no safe cut or no improvement exists, seek Maintainer
disposition rather than claim success. Replace wording pins only with guards
that check the same installed obligation, pass intact output, and fail on a
removed or inverted clause. Preserve deliberately different adopter wording.

### C4

Run the mapped checks, actual installs and ceremonies, and record their results.
Review tests and output against the inventory for meaning as well as presence;
failed deletion controls or lost reach block completion. Record the before/after
comparison and any accepted scope loss under Scope delta.

## Scope delta

**Scope delta**: preserved. Any proposed loss is grouped here with its reason,
individual disposition and the Maintainer's quoted allowance before archive.

## Verification

Boundary A starts with this map; paths after arrows are installed destinations
from `bootstrap/_scaffold/config.py` `_CORE_MAPPINGS`:

- Review and verification duties: `templates/core/AGENTS.md` → `AGENTS.md`;
  `test_review_and_verification_rules_ship.py::test_agents_md_carries_the_obligation`
  checks both source copies only. Its claiming tests distinguish conditional
  adopter claiming from unconditional Cairn claiming; do not flatten that difference.
- Review sweep: `templates/core/dev/agent_collaboration.md` →
  `dev/agent_collaboration.md`, with the `AGENTS.md` pointer. In
  `bootstrap/tests/test_review_sweep_ships.py`, source tests check both copies;
  `test_installed_loop_document_carries_the_obligation` and
  `test_installed_agents_md_carries_the_pointer` check actual installs of every
  shipped profile; `test_an_install_without_the_sweep_is_reported` removes the
  sweep from installed output as a control.
- Scope reduction: core governing files and proposal/plan templates map to the
  same relative installed paths; `test_scope_reduction_trap.py::test_scope_reduction_obligation_present`
  checks source, board and doctrine surfaces, not installed output. Compare
  source/twin meaning, and verify affected installed clauses through real installs.
- Model floors: core `AGENTS.md` → installed `AGENTS.md`;
  `test_model_tier_rule_ships.py::test_the_rule_reads_the_same_in_both_copies`
  checks parity; `test_a_profile_with_no_module_still_installs_the_rule` checks
  `bootstrap/profiles/solo-greenfield.yml` output.
- Plain language: core collaboration file → installed collaboration file;
  `test_writing_rules_ship.py::test_cairns_own_copy_says_what_it_ships` checks
  source parity, and `test_standard_with_version_and_groups_reaches_install`
  checks a real core-plus-issue-capture install.

Test paths above are under `bootstrap/tests/`. The inventory and chosen routing
extend this map to each changed obligation, source owner, installed destination,
profile and exact test or gate before edits; search for every affected reader,
record uncovered consumers and check them. For each replaced guard, check the
intact real install and removed or inverted clause in installed output; a negative
control proves sensitivity, not semantic equivalence. Compare meaning against
the inventory and check source/twin parity including intentional differences.
Run the mapped owners and real installs, `scripts/claim_check.py`,
`scripts/link_check.py`, `scripts/check_cairn.py`, and
`scripts/quality_gate.py --sub neutrality --sub redundancy` as applicable.
Inspect the frozen manifest and follow the existing ceremonies. Check the inventory’s claims, links and evidence.

Boundary B uses the canonical `/Users/kendal30/conda_envs/lhm/bin/python3.13`
on a clean final implementation commit. These high-risk surfaces require full
mode, with the next certifying run supplying full-suite evidence; record
`Certified by: pending` until then. Run the scoped mapping and standing gates,
record tested SHA and range, clean pre/post state, commands, counts, timing,
non-pass dispositions and omissions. The reviewer independently falsifies the
record and changed rule reach, without running the full suite.

## Plan review -- Codex (Internal reviewer, gpt-6.1-terra) -- 2026-10-28

```
Reviewed commit: 73d9ff63803769c4764883c7117817d444f0c5f9
Target: Source proposal through Verification
Prior findings: none
Assurance path: Internal + Internal Security Review
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** Yes, subject to sequencing and a usable verification map: inventory and the Maintainer's routing choice precede any operative move or deletion -- `dev/plans/governing-text-single-source.md` > C1–C3.
2. **Best alternative.** Keep the present homes where evidence does not support a safe simplification; the existing installer delivers core and module files separately, so a published citation alone is insufficient -- `bootstrap/_scaffold/config.py` > `_CORE_MAPPINGS` and `_MODULE_MAPPINGS`.
3. **What would show it wrong.** A real install loses an obligation or its usable trigger, a deletion control passes, or neither representative edit becomes simpler without lost meaning -- `dev/proposals/archive/2026-10-28-codex-governing-text-single-source.md` > "Conditional edits and evidence".

**F1 (blocking) -- Sequence the other shared-rule work.** C3 waits for model-floor alignment but not the accepted scoped-change-verification plan, whose C1 also changes `AGENTS.md`, its shipped twin, doctrine and plan templates (`dev/plans/scoped-change-verification.md` > Scope and C1). Concurrent changes can make the inventory and its chosen edits stale or overwrite another accepted outcome. **Satisfier:** gate shared governing edits on that plan's implementation and code review too; allow C1 alongside it, but refresh the affected inventory and mapping against the completed changes before routing or edits.

**F2 (blocking) -- Map the checks and source-to-install comparison before editing.** Verification lists five starting test files and defers owner mapping until before edits, but does not map changed invariants and public paths to checks for review as the plan template requires. For example, `bootstrap/tests/test_review_and_verification_rules_ship.py` reads both `AGENTS.md` copies, including a deliberately different claiming rule; naming the file alone does not identify what protects each obligation or installed path. The accepted contract also calls for source/twin parity, not just distinct wording. **Satisfier:** map the known invariants and installed paths to test nodes or files and standing gates now, including parity and intentional differences; explain how the inventory and routing choice extend that map before edits, with any uncovered consumer recorded and checked. Keep the existing single plan-review round.

**Coverage:** Claims and production path: `_CORE_MAPPINGS`, `_MODULE_MAPPINGS`, and the cited shipped-rule tests; design and failure: C1–C4, real installs and deletion/inversion controls; consistency and drift: the accepted proposal, model-floor and scoped-verification plans; placement: C2's Maintainer fence; scope and satisfiers: conditional cuts, comparison and F1–F2. **Not covered / low confidence:** No install, test, ceremony, full doctrine-section audit, or future semantic guard was executed; the separate Internal Security Review remains open.


## Plan review -- Codex (Internal Security Reviewer, gpt-6.1-sol high) -- 2026-10-28

```
Reviewed commit: 73d9ff63803769c4764883c7117817d444f0c5f9
Target: Source proposal through Verification; accepted revised proposal and Decision 439c7b34
Prior findings: none from this security stance
Assurance path: Internal + Internal Security Review
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** The plan preserves the accepted safety contract:
   inventory actual rule homes before routing, retain installed operational
   instructions, and obtain the Maintainer's choice before relocation or deletion. Its
   verification map needs sharpening before implementation -- plan C1–C4;
   `dev/proposals/archive/2026-10-28-codex-governing-text-single-source.md` > revised
   proposal and Decision.
2. **Best alternative.** Reuse existing installed-output checks and retain distinct
   semantic guards while extending their coverage only where the inventory identifies a
   changed obligation; a new checker is unnecessary -- `bootstrap/tests/test_review_sweep_ships.py::test_an_install_without_the_sweep_is_reported`; `bootstrap/tests/test_review_and_verification_rules_ship.py::test_the_shipped_copy_makes_claiming_conditional`.
3. **What would show it wrong.** A source guard stays green while a real install loses
   an instruction, a citation substitutes for its operational home, or a
   removed/inverted clause escapes its replacement guard --
   `bootstrap/_scaffold/config.py` > `_CORE_MAPPINGS`;
   `bootstrap/tests/test_scope_reduction_trap.py` > `_REVIEW_LOOP`; plan C2–C4.

**S1 (blocking) -- Distinguish source checks from installed safety evidence in the
reviewed map.** Verification gives five starting files, then postpones the actual
mapping. They do different jobs: `test_agents_md_carries_the_obligation` in
`bootstrap/tests/test_review_and_verification_rules_ship.py` reads the source copies;
`test_installed_loop_document_carries_the_obligation` and
`test_installed_agents_md_carries_the_pointer` in
`bootstrap/tests/test_review_sweep_ships.py` inspect real CLI installs. Naming both
files does not show which installed obligation and reader path a changed guard protects.
A source-only positive/deletion pair could therefore be mistaken for the promised
installed reachability check. **Satisfier:** fold the ordinary review's F2 map into the
operative Verification cells, naming the known safety obligations, source/twin
comparison and intentional differences, installed destination/profile paths, exact
owning tests and standing gates. Distinguish source-only evidence from installed-output
evidence; identify the positive and removed/inverted-clause controls for each replaced
guard, and require the inventory/routing result to extend that map before edits. Keep
semantic comparison against the inventory: a negative control proves sensitivity to its
chosen error, not that the remaining prose means the same thing.

C2's unresolved-home refusal and C3's no-safe-cut disposition prevent silent rule loss.
The operational-safety minimum remains adopter-reachable rather than being delegated to
published rationale (`doctrine/doc-governance.md` > “The operational-safety minimum
stays minimal”). C3 also preserves frozen-test sequencing; this review authorizes
neither routing nor a trust transition.

**Covered:** #1 claims and #2 delivery: `_CORE_MAPPINGS` and the named source/installed
tests; #3 completeness and #4 failure: S1, C2–C4; #5 consistency and #6 drift: accepted
revised proposal, deliberate claiming difference, `doctrine/doc-governance.md`; #7
placement: C2 and frozen-test fence; #8 scope: conditional cuts and two-edit comparison;
#9 satisfier: S1 and ordinary F2. **Not covered / low confidence:** No install, test,
mutation, ceremony, full doctrine inventory or future semantic guard was executed. Those
remain implementation evidence; the ordinary review's sequencing finding remains
separate.

## Response to plan review -- Codex (Plan author, gpt-6.1-terra) -- 2026-10-28

| Finding | Disposition | Operative cell |
|---|---|---|
| F1 | Accepted | Sequence C2–C3; C1 refresh |
| F2 | Accepted | Verification map and C1 refresh |
| S1 | Accepted | Verification map and installed-output controls |

## Implementation verification -- Codex (Implementation, Luna) -- 2026-10-28

**Scope**: C1 initial factual inventory only. No governing-rule or executable bytes changed. This is not Boundary B and does not complete plan verification.

**Measured source SHA**: `0ac350c02422d8a8ba8c3b674a671b072c71a317` (reviewed plan revision).
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` -- Python 3.13.13.
**Clean pre/post state**: the detached measurement worktree was clean before and after the scoped checks (`git status --short` returned no paths).

**Commands and outcomes**:

- `bootstrap/scaffold.py --config bootstrap/profiles/solo-greenfield.yml --target /private/tmp/cairn-gov-small-20261028 --non-interactive --allow-dev` -- exit 0; 69 files; no `doctrine/`; two module slots remain for onboarding.
- `bootstrap/scaffold.py --config bootstrap/profiles/high-rigor-legacy.yml --target /private/tmp/cairn-gov-full-20261028 --non-interactive --allow-dev` -- exit 0; 101 files; no `doctrine/`; model mapping remains `FILL ME`, hook setup is manual, and no security host tool ran.
- `python -m pytest -q bootstrap/tests/test_model_tier_rule_ships.py bootstrap/tests/test_scope_reduction_trap.py` -- 98 passed in 0.25s.
- `python -m pytest -q bootstrap/tests/test_documentation_plan_module.py bootstrap/tests/test_review_sweep_ships.py bootstrap/tests/test_review_and_verification_rules_ship.py` -- 275 passed in 1.12s.
- `python scripts/check_cairn.py` on the inventory note and updated plan; `claim_check.py` and `link_check.py` on both files -- all pass; one Markdown file scanned per call. The test-reader search found no test importing or reading the new note/TSV (a known `doctrine/lifecycle.md` reference matched as the positive control).
- `python scripts/quality_gate.py --sub neutrality --sub redundancy` -- 0 failures, 43 informational entries, no redundancy findings.
- Per-heading source record: `dev/plans/governing-text-single-source/doctrine-sections.tsv` contains 195 H1-H3 rows from 15 doctrine files at the measured SHA. Inventory note: `dev/strategy/2026-10-28-governing-text-inventory.md` (1,378 words).

**Timing**: pytest-reported 0.25s and 1.12s; the install and prose-gate calls completed in under 2s each by tool wall time.
**Non-pass disposition**: no test skips or failures. Quality-gate informational entries were reported, not failures. Installs completed but retain the onboarding notes above.
**Known omissions**: no implementation edit, mutation, full suite or adopter-use trial; the installed `Scope delta` wording was observed but not semantically pinned by its owner test. Initial inventory only: refresh affected facts and mapping after model-floor and scoped-verification implementation and code reviews, before C2. The routing recommendation and Maintainer choice remain open.

## C1 Strategy routing judgment -- Codex (gpt-6.1-sol high) -- 2026-10-28

Strategy's recommendation is folded into
`dev/strategy/2026-10-28-governing-text-inventory.md`: public methodology
explanation/reference under `docs/`, with complete operative obligations in
usable installed homes. It compares retaining the publication split,
`dev/rules/`, relocation under `docs/`, and generation; preserves useful public
specifications and distinct template instructions; and names the lost landmark,
citation migration, unresolved installed duties and unmeasured savings. This is
Strategy work, not a review or the Maintainer's routing choice.

**Census correction**: the initial 195 H1–H3 rows include five example headings
inside code fences in `doctrine/plans.md`. There are 190 document headings.
The TSV's added `heading_context` column preserves every original row and field
while distinguishing the five examples; lexical content signals remain an
inventory aid, not a semantic audit.

**Evidence**: read the committed baseline `0ac350c0`, the inventory at
`423310d4`, representative public/installed passages and owner tests, and
history `3a190c95`, `5f619be4`, `7519c5da`, `676b7c0e`. Python 3.13.13 at
`/Users/kendal30/conda_envs/lhm/bin/python3.13` confirmed all 195 existing TSV
records/fields unchanged and census controls included real headings while
excluding fenced examples. The note has 1,293 whitespace-delimited words.
`claim_check.py`, `link_check.py` and `check_cairn.py` passed on the note and
this plan; the future destination is typed as a proposed path.
`quality_gate.py --sub neutrality --sub redundancy` reported 0 failures,
43 informational neutrality entries and no redundancy findings. Reader search
for the note basename, TSV basename and plan stem in `bootstrap/tests`,
`scripts` and `.github` found no readers; the same instrument found known
`doctrine/lifecycle.md` readers as its positive control. No executable snippets
were added, so snippet synchronization does not apply.

**Limits / next move**: no rule move, deletion, AGENTS edit, new tool, installed
mutation, full suite or ceremony. Existing source-vs-installed test limits
remain recorded in the note. Refresh affected facts and mapping after the
model-floor and scoped-verification implementations and code reviews; only
then can C2 become the Maintainer's next move. Status remains `implementing`.


## Filename maintenance -- Codex (Coordination) -- 2026-10-28

Maintainer naming instruction, verbatim:

> "Your plan docs aren't following the right naming convention. See the archive. Can you check if the template specifies this? If not, please modify it and the other templates (And shipped copies) to specify the date as part of the naming."

The filename now uses its original Opened date. Its document-owned evidence
folder, where present, uses the same dated stem and archives with the plan.
This is a path migration, not a scope or lifecycle change. Historical review
and evidence citations retain the paths valid at their named commits; current
link destinations and operative targets use the dated paths.


## C1 refreshed decision packet -- Codex (Strategy, gpt-6.1-sol high) -- 2026-10-28

**Source snapshot**: `e9928009078b666b753b3b0502af14d9d2421922`, after
model-floor archive and scoped-verification ordinary/Security reviews. The
latter remains held on its prescribed ceremony; this packet waives nothing.
C1 now reaches C2's fence; its Waiting line names the grouped routing/conflict
choice. No operative rule, source proposal or prior review was edited.

**Packet**: the settled strategy note is
`dev/strategy/2026-10-28-codex-governing-text-inventory.md`. The existing section
TSV preserves 195 baseline records and adds current coordinates/section-purpose
judgments (190 document headings, five fenced examples; 6,125 current lines).
The owned `operative-obligations.tsv` maps 55 obligation groups, including two
conflicts and 21 partial installed homes; `editing-baseline.tsv` records 21
measurements. These names resolve inside this plan's same-stem evidence folder.

**Recommendation**: public methodology explanation/reference under `docs/`,
with complete installed operation and project-local `dev/rules/`. Ask the
Maintainer explicitly to confirm the current shipped coordination default
(block only provably different live claims, warn on stale/tokenless claims,
retain warn/confirm choices) and current exact, document-wide typed path
declarations. These replace different published defaults/restrictions; routing
approval alone cannot authorize their loss. Partial-duty rows remain no-cut
barriers until their complete appropriate local owner/pointer is established.
No proposed duty loss is silently accepted.

**Verification**: canonical Python 3.13.13. Fresh empty-target CLI installs from
an exact Git archive of the snapshot, using the two named profiles and
`--non-interactive --allow-dev`, exited 0: 69 files in 0.117s and 101 in 0.095s.
Both contain the local governing/template/rules/documentation/skill homes and
omit doctrine. Current floor clauses occur in both outputs; the complete source
`Scope delta` section survives unchanged in each installed plan template. An
initial invocation refused missing target directories; creating empty targets
resolved that setup refusal. No host security tool or hook was run.

All 195 original section fields remain unchanged; current heading coordinates,
55 obligation IDs/source anchors/related test paths and baseline counts were
validated directly against committed bytes. Historical owner results are
identified in the baseline, not presented as fresh passes. No duplicate owner
suite, full suite, mutation or ceremony ran. Claim/link/check_cairn pass on the
note and this plan; neutrality/redundancy have zero failures (43 informational
neutrality entries). Reader search found no tests/scripts importing these
inventory artifacts, beside its known doctrine-path positive control.

**Next move / limits**: C2's exact Maintainer choice belongs in this plan before
any rule relocation/deletion/reconciliation. The two example editing baselines
are measured before consolidation; no after-change saving is claimed. C3 still
owes source/twin semantic comparison and positive plus removed/inverted installed
controls for changed obligations, and its trust-test sequencing fence remains.
Any subsequent affected source delta requires refresh before acting on C2.

## C2 routing choice -- Maintainer, relayed by Codex (Terra) -- 2026-10-28

Maintainer authorization in chat, verbatim:

> Yes, I like docs/methodology as a home, and other locations as you describe.

Proposed path: `docs/methodology/` (not yet created).

The chosen routing places public methodology explanation and reference under
the proposed path, complete operating duties in usable installed files, and
project-specific rules in `dev/rules/`. Preserve partially installed duties
until their complete appropriate installed home and usable pointer are shown.
This choice settles routing; the coordination-default and path-declaration
conflicts remain separate Maintainer decisions. C3's remaining sequencing and
verification gates still apply. No rule relocation or deletion is made here.

## C2 coordination choice -- Maintainer, relayed by Codex (Terra) -- 2026-10-28

Maintainer authorization in chat, verbatim:

> Blocking for live-session conflicts, yes. Agents should claim intent prior to editing.

The chosen default blocks a commit on a provably different live session's
claim; stale or unidentifiable claims warn. Agents should claim intent before
editing. This replaces the differing public default described in the C1 packet;
the warn and confirm modes remain available. The separate path-declaration
choice is still open. No operative rules or tools are changed by this record.

## C2 path-declaration choice -- Maintainer, relayed by Codex (Terra) -- 2026-10-28

Maintainer authorization in chat, verbatim:

> Document-wide, yes please update the instructions.

The Maintainer chose document-wide reuse of a declared exact path and requested
matching instructions. Preserve the checker's exact matching and provenance;
siblings, descendants, look-alikes and malformed declarations remain
unexempted. This choice supersedes the published line/block-only restriction.
The previously recorded routing and coordination choices remain in force. C3's
sequencing and verification gates still apply; no rules or tools change in this
record.

## Implementation verification -- C3 path declarations -- Codex (Luna, low) -- 2026-10-28

Implemented the focused documentation correction in source commit
`7682214db06e922a67d2a218f0cb53f79d6c3c22`. On that commit, the tracked tree
was clean before and after checks; the only status entries were the pre-existing
untracked `.claude/` and `dev/measurement/collision_log.md`. Python 3.13.13 ran
`PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -p no:cacheprovider -q
bootstrap/tests/test_claim_check_module.py bootstrap/tests/test_scope_reduction_trap.py`:
167 passed in 0.28 seconds. The owning claim-check tests cover document-wide
exact reuse, provenance, sibling/descendant/look-alike rejection, malformed
wildcards, conflicting marker kinds and the existing-file boundary. The scope
reduction test file also reads the changed proposal doctrine. `python
scripts/check_cairn.py doctrine/plans.md doctrine/proposals.md` passed for both
files. The source scan shows that all parsed typed declarations, including a
standalone marker-line declaration, enter the exact document registry;
`registry_block` controls only lifecycle liveness. No existing test directly
checks a standalone marker's recurrence outside its line.

No frozen test or checker code changed. No actual install, security ceremony,
full suite or whole-tree verification ran. The test-trust-boundary plan remains
implementing at its Maintainer roster gate. This record covers only the path
instruction correction; C3's other outcomes and the plan's completion remain
open.

## Focused C3 path-guidance review -- Codex (gpt-6.1-terra) -- 2026-10-28

Reviewed commit: `31d923855ea5b186a548c820a7521abd8e629329`
Target: source change `7682214db06e922a67d2a218f0cb53f79d6c3c22` and its focused evidence; not final C3/C4 review.
Prior findings: none.

**Foundations**

1. **Does it do what it claims?** The central standalone and exact-reuse guidance matches the scan; two qualifications below need correction -- `scripts/claim_check.py` > `_scan`.
2. **Best alternative.** Keep the focused correction and qualify its edge conditions; do not change the checker merely to match prose -- `scripts/claim_check.py` > `parse_typed_declarations` and `_scan`.
3. **What would show it wrong?** An exempted near-match, unreported conflict, or missed stale outside-block citation -- see falsification ledger below.

**F1 -- Qualify liveness and the linked mechanism.** Both doctrine pages say every structured-block declaration in a non-terminal artifact must authorize an outside occurrence. The checker instead reports non-checkable entries and archive-resolved entries informationally; immutable grandfathering also changes severity. Qualify this statement. Both pages also direct readers to the checker module docstring for the full mechanism, but its typed-registry section says duplicates in one block grant nothing; `parse_typed_declarations` actually treats same-keyword repeats as idempotent. Correct that linked description through the applicable checker/change gates, or explicitly flag the discrepancy in the guidance until corrected.

**Falsification ledger** (Python 3.13.13, fresh archive of reviewed commit; `_scan` with a synthetic active plan path as context):

- Standalone marker followed by exact missing path: no hard flags; exemption cites marker line.
- Sibling/look-alike and descendant: both hard path flags.
- Same-keyword duplicate on one marker: no hard flags; exact occurrence exempted with first declaration provenance.
- Proposed versus untracked declaration for one path: declaration conflict and outside path hard flags; no registry exemption.
- Wildcard declaration: declaration hard flag and outside path hard flag.
- Existing file with out-of-range line citation outside marker: hard line-bounds flag.
- Source and shipped checker copies compare identical (`cmp scripts/claim_check.py templates/modules/default-on/claim_check.py`).

**Evidence and limits.** The author's 167-test record names the scoped source commit and explicitly leaves standalone recurrence untested; the independent probe above supplies that targeted observation. It is not final Boundary B, and this pass does not certify C3 or C4. The author claimed source and plan before the source commit, but auto-release followed that commit; the subsequent plan evidence was edited without a renewed claim. No collision is established. Claim again before each later edit. This pass did not run an install, frozen-test changes, security ceremony or full suite; the existing plan gates remain. Status stays `implementing`.

## Response to focused C3 path-guidance review -- Codex (Luna, low) -- 2026-10-28

| Finding | Disposition | Changes |
|---|---|---|
| F1 | Accepted | Forward-reference guidance and linked checker descriptions updated in `doctrine/plans.md`, `doctrine/proposals.md`, `scripts/claim_check.py`, and `templates/modules/default-on/claim_check.py`. |

The doctrine now limits hard liveness findings to checkable structured-block
declarations in mutable lifecycle artifacts at the exact live paths. It names
the non-failing cases: paths the checker cannot resolve, entries now resolved
by the exact archive rule, and declarations in archived or terminal artifacts.
Missing or invalid status fails closed into liveness. Standalone marker-line
declarations remain exact and document-wide but have no separate liveness check.

The source and shipped module docstrings now say that same-keyword redeclarations
are idempotent, including repeats in one block; declarations under different
marker keywords conflict and grant no authority. Both copies remain byte-
identical. These are frozen gate-manifest files, so their applicable Maintainer
ceremony remains owed under C4. No runtime code or frozen test changed, and the
ceremony was not run.

## Implementation verification -- F1 path-guidance revision -- Codex (Luna, low) -- 2026-10-28

**Boundary B mode**: wide. The touched surfaces are the published proposal and
plan doctrine plus the local and shipped claim-check module descriptions. The
owning claim-check behavior family and the installed-script owner family ran;
the installed-script tests exercised the scaffolded checker. `check_cairn.py`
checked both changed doctrine files, and the standing neutrality gate ran.
Effects are bounded to instructions and module docstrings; runtime code is
unchanged. The source/twin byte comparison confirms the shipped description
matches its local source.

**Certified by**: pending
**Tested commit**: `860481db0cf36fe25af1994612860fab429dd18f`
**Reviewed range**: `0766c18f1dd6594d28b75caba87d8daadf1e5bb1..860481db0cf36fe25af1994612860fab429dd18f`
**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` — Python 3.13.13
**Pre-run state**: tracked tree clean at tested commit; two pre-existing untracked items only.
**Post-run state**: tracked tree clean; `HEAD` remained the tested commit.

| Command | Exit | Outcomes | Elapsed |
|---|---:|---|---:|
| `PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -p no:cacheprovider -q bootstrap/tests/test_claim_check_module.py` | 0 | 78 passed | 0.12 s |
| `PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -p no:cacheprovider -q bootstrap/tests/test_reference_scripts.py` | 0 | 13 passed; includes claim-check install/parity and real installed entry path | 0.72 s |
| `python scripts/check_cairn.py doctrine/plans.md doctrine/proposals.md` | 0 | 2 Markdown files; no issues | 0.04 s |
| `python scripts/quality_gate.py --sub neutrality` | 0 | 0 failures; 43 informational records | 0.75 s |
| `cmp scripts/claim_check.py templates/modules/default-on/claim_check.py` | 0 | Source and shipped copy identical | <0.01 s |

**Non-pass disposition**: none. Neutrality informational records are the existing
43 accepted exemptions. **Known omissions**: no full suite, whole-plan C3/C4
verification, profile-wide install, or gate-manifest ceremony ran. Both frozen
checker files still require the applicable Maintainer ceremony under C4; the
manifest was not changed. The focused F1 correction is verified, while C3's
remaining outcomes and the plan stay open.

## C3 installed typed-path behavior probe -- Codex (Implementation, Luna) -- 2026-10-29

**Scope**: real installed-checker behavior for the accepted exact, document-wide typed-path declaration correction. This is a targeted C3 evidence slice, not final Boundary B or C4 completion.

**Source commit**: `8b140246865bc5192199a800f8acd1ca6f3dea75`.
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` -- Python 3.13.13.
**Source worktree state**: clean before and after the probe. Fresh detached worktree; the two install targets and synthetic controls were outside the source tree.

**Installations**: `bootstrap/scaffold.py --config bootstrap/profiles/solo-greenfield.yml --target /private/tmp/cairn-gov-small-control-20261029 --non-interactive --allow-dev` exited 0; 72 files were present after installation. The equivalent `high-rigor-legacy.yml` command targeting `/private/tmp/cairn-gov-full-control-20261029` exited 0; 104 files were present. In both outputs, `scripts/claim_check.py` compared byte-identically with the source checker.

**Installed entry-point controls**: ran each profile's installed `scripts/claim_check.py` against three synthetic documents rooted in that installation. The intact declaration plus a later exact recurrence passed and reported one exemption. Removing the declaration failed on the unresolved path. Changing the repeated path to a look-alike sibling failed on that unresolved path. All three outcomes matched the intended exact-match behavior in both profiles.

**Omissions**: no source or frozen test bytes changed; no test suite, mutation framework, full-suite run, ceremony, or whole-plan before/after edit comparison ran. These checks establish current installed checker behavior, not semantic equivalence of all surrounding doctrine prose. C3's other conditional edits and C4 remain open; the v0.6 re-anchor remains deferred under the Maintainer's direction.

## C3 scope-delta template simplification -- Codex (Implementation, Luna) -- 2026-10-29

The plan-template pair no longer repeats the rationale that narrowing is the
path of least resistance. The same reason remains in installed `AGENTS.md` and
the installed review-loop document; the templates retain the actionable floor,
baseline, sequencing, Maintainer authority, grouped record, per-entry
disposition, deferral, expansion and chunk-fence instructions. Both copies
remain byte-identical. C3 adds an installed-output control to the existing
scope-reduction owner test without changing its collected node set.

The C1 editing comparison remains scoped to its two measured examples: the
task-floor presentations are unchanged, while the repeated Scope-delta
explanation is shorter in both plan-template copies. Final before/after counts
and install/test evidence belong in C4 after the final implementation commit.

Maintainer direction relayed for this implementation is to finish the source
work without requiring historical anchor comparison and without changing the
actual reference. The read-only `python scripts/repin.py status` command refused
before import because the current `_gate_manifest.py` bytes differ from its
anchor entry. No re-anchor or reference change was made, and this record does
not claim that the proposed protected roster is installed or the ceremony has
passed.


## Implementation verification -- C3 scope delta and C4 -- Codex (Implementation, Luna) -- 2026-10-29

**Boundary B mode**: wide. This contract/template change was checked across the scope owner, template readers, scaffold, install, review, and verification test families, plus real small and fuller profile installs. Effects are bounded to the plan-template Scope delta rationale and its installed guard; the changed source and shipped subsections match after whitespace normalization. The full template files intentionally differ in other generated-slot and adopter-verification guidance.

**Certified by**: pending
**Implementation verified at**: `72fecafe69f3c12e8b8c43f2b501e47955684aaa`
**Tested commit**: `72fecafe69f3c12e8b8c43f2b501e47955684aaa`
**Reviewed range**: `64a233757f303b32c5f6c521e733c78ada36ae5e..72fecafe69f3c12e8b8c43f2b501e47955684aaa`
**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` -- Python 3.13.13.
**Pre-run state**: fresh clone, detached at tested commit; `git status --short` empty.
**Post-run state**: `git status --short` empty; `HEAD` unchanged at tested commit.

| Command or check | Outcome | Timing |
|---|---|---:|
| `PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -p no:cacheprovider -q bootstrap/tests/test_scope_reduction_trap.py bootstrap/tests/test_model_tier_rule_ships.py bootstrap/tests/test_review_stance_in_shipped_files.py bootstrap/tests/test_scaffold.py bootstrap/tests/test_board_json_contract.py bootstrap/tests/test_scientific_check_guidance_ships.py bootstrap/tests/test_verification_boundaries.py bootstrap/tests/test_certifying_run_rule.py bootstrap/tests/test_install_report_slots.py bootstrap/tests/test_quickstart_sequence.py bootstrap/tests/test_documentation_plan_module.py bootstrap/tests/test_replacement_tools.py --tb=short` | 781 passed; no failures, skips or xfails reported | 6.57 s |
| `bootstrap/scaffold.py --config bootstrap/profiles/solo-greenfield.yml --target <fresh empty target> --cairn-root <tested clone> --non-interactive --allow-dev` | exit 0; 69 files; installed `dev/plans/_template.md` is byte-identical to shipped source | 0.116 s |
| Same command with `high-rigor-legacy.yml` | exit 0; 101 files; installed `dev/plans/_template.md` is byte-identical to shipped source | 0.085 s |
| Installed-output semantic control in `test_scope_reduction_trap.py` | Both profiles pass the intact output; each of three mutations per profile is detected: reviewer-authority inversion, removal of per-entry disposition, and proposed-expansion inversion | included above |
| `python scripts/claim_check.py <each of the plan and two templates>` | all three passed; five expected plan path exemptions were reported | 0.03 s combined |
| `python scripts/check_cairn.py dev/plans/2026-10-28-governing-text-single-source.md dev/plans/_template.md templates/core/dev/plans/_template.md` | 3 Markdown files scanned; passed | 0.03 s |
| `python scripts/link_check.py` on the same three files | 3 Markdown files scanned; passed | <0.01 s |
| `python scripts/quality_gate.py --sub neutrality --sub redundancy` | 0 failures; 43 informational neutrality entries; 0 redundancy findings | 1.00 s |
| Edited-subsection parity and before/after count | Source and shipped Scope delta sections match after whitespace normalization. Each shrank from 273 words / 29 lines to 243 words / 27 lines. The other task-floor example was not edited. Whole-template byte parity is not expected because installed slots and adopter-specific verification text differ. | direct comparison |

**Known omissions / limits**: No full suite, certification, re-anchor, or reference change was performed. The Maintainer waived historical anchor comparison and directed this source work to proceed; the earlier read-only `repin status` refusal on a mismatched `_gate_manifest.py` remains unresolved, so this record claims no anchor/roster installation or ceremony result. Mutation controls establish sensitivity to the three named breaks, not equivalence of every possible wording. No adopter-use trial ran. The independent code review remains next.

## Code review -- Codex (GPT-6), independent reviewer -- 2026-10-29

Reviewed commit: d498b308b70b21c7309a010e7eb58e0642ab9988
Target: C3 implementation 64a233757f303b32c5f6c521e733c78ada36ae5e..72fecafe69f3c12e8b8c43f2b501e47955684aaa and C4 evidence
Prior findings: none

**Foundations**

1. **Does it do what it claims?** The edited section is shorter and retains the actionable scope rules, but the comparison does not establish the full measured change required by C3. -- `dev/plans/_template.md` > Scope delta; F1 below.
2. **Best alternative.** Keep the focused cut and report the unchanged or changed values against each C1 measure, including costs and both examples. -- `dev/plans/2026-10-28-governing-text-single-source/editing-baseline.tsv`.
3. **What would show it wrong.** A lost installed obligation or a comparison showing no improvement would challenge the result. -- falsification ledger below.

**F1 — Blocking: complete the comparison on the same measures.** C3 requires comparing both C1 edits after the change using the same measures. The baseline records presentation files, implementation footprint, owning checks, lifecycle and ceremony cost, and installed reader path as well as section length. The addendum reports the Scope delta length and installed controls, and says the task-floor example was unchanged, but does not repeat or explicitly reconcile the other measures for both examples. Record comparable after values or explain with evidence why a baseline measure is unchanged or inapplicable; distinguish the 30-word point-of-use cut from any reduction in edit or ceremony effort. -- C1, C3 and `dev/plans/2026-10-28-governing-text-single-source/editing-baseline.tsv`.

**Bounding**: WIDER RUN REQUIRED -- complete the comparison evidence; this does not require a full suite.

**Falsification ledger**

- Installed solo profile: a fresh clone of d498b308 and a fresh target were used with Python 3.13.13 and `bootstrap/scaffold.py --config bootstrap/profiles/solo-greenfield.yml --target <fresh target> --non-interactive --allow-dev`. The installed output passed `_missing_installed_plan_scope_obligations`; independently replacing the unassigned-remainder Maintainer duty produced the expected missing-obligation result. An initial probe failed to match the line-wrapped text; a whitespace-aware probe was then used.
- Changed rule: compared the two template diffs and inspected installed authority and the surviving rationale in `templates/core/AGENTS.md` and `templates/core/dev/agent_collaboration.md`. The deleted text is explanatory; no actionable clause was deleted in the diff.
- Comparison: read C1's baseline and C4's addendum against C3's same-measures criterion; the omissions are F1.

**Covered**: scope clause preservation, one installed negative control, simplification claim, and the change-verification record. **Not covered**: all wording mutations, an adopter-use trial, historical anchor comparison, or the full suite.


## Response to code review -- F1 same-measures comparison -- Codex (Implementation, Luna) -- 2026-10-29

| C1 measure | Operating-rule example: task capability floor | Template-instruction example: Scope delta |
|---|---|---|
| Maintained presentation | All five C1 presentations remain at their recorded values: `AGENTS.md` 145 words, `templates/core/AGENTS.md` 145, `doctrine/roles.md` 902, and both model-selection module copies 510 each. Direct comparison of the C1 excerpts at `e9928009` and this implementation at `72fecafe` found identical bytes in every measured range. The later 12-line addition elsewhere in `AGENTS.md` is separate protected-test guidance, outside the measured floor excerpt. | Each of the two point-of-use sections is now 243 words and 27 lines, down from 273 words and 29 lines in C1. The same 30-word, 2-line reduction appears in the internal and shipped templates; their complete files intentionally differ in adopter slots and verification guidance. |
| Presentation-file count | Five, unchanged; no floor presentation was edited by C3. | Two, unchanged. Both copies still carry the rule; the edit retained the two-copy maintenance cost. |
| Implementation footprint | The C1 value of 15 files describes the earlier historical task-floor implementation. It remains historical and is not reduced by this C3 change, which did not edit those five presentations. | The C3 implementation commit changed four paths: the two template copies, the existing scope owner test and this plan. The follow-up verification commit changed the plan and its measurement TSV. This is a 30-word-per-copy reading reduction, not a reduction in the number of files or lifecycle steps. |
| Owning checks | The C1 record of 574 historical checks remains the prior implementation's evidence. In this pass, the model-tier owner family reported 10 passes, as part of the final 781-test Boundary B selection. No new floor check was added. | The owner test remains at 89 collected cases, as in C1. It passed 89/89 in the focused run (0.34 s); its existing accepted-floor case now exercises real installed output and detects three named mutations in each profile. Boundary B ran that file within 781 mapped passes (6.57 s). |
| Related guarded surfaces | The C1 task-floor wording is unchanged; the 14-surface Scope-delta guard map is not a task-floor measure. | The accepted-scope owner still enumerates 14 related contract surfaces. C3 changed the two template copies within that set; no other Scope-delta source was edited by the implementation commit. The earlier 8-lines-per-template floor insertion remains intact; this change removes only the repeated rationale. |
| Installed reader path | Still `AGENTS.md` > Roles for both profiles, with the model-selection module only in the fuller profile. The final fresh installs contain 69 and 101 files respectively; both contain the Model tier rule in `AGENTS.md`, the solo install has no model-selection module, and the fuller install has it. The existing model-tier tests verify the solo installed rule. | Still `dev/plans/_template.md` > Scope delta in both profiles. The 69-file and 101-file final installs contain the shipped plan template byte-for-byte. The installed semantic control passes both intact outputs and detects all six named mutations. |
| Project adaptation caveat | The task-specific model mapping remains project-owned; no change was made to that caveat. | Not applicable to the Scope-delta template measure. |
| Lifecycle and ceremony cost | No new work was required for this example; its prior C1 history remains the applicable edit-cost evidence. | The cut improves point-of-use length only. The work still required both source copies, an existing owner-test edit, mapped tests, two installs, a verification record and independent review. No re-anchor or reference change was made; the Maintainer's direction waived historical anchor comparison. No ceremony result is claimed. |
| Final installed positive reading | The C1 baseline had both profiles receiving the floor. The final installs reconfirmed the same paths; the model-tier suite passed. | The C1 baseline had the accepted floor, grouped remainder and Maintainer authority present in both profiles but no installed semantic guard. After C3, both intact outputs pass the guard, while reviewer-authority inversion, per-entry-disposition deletion and proposed-expansion inversion are each detected in both outputs. |

F1 is accepted. The rows above reconcile each C1 measure without replacing its original value; the appended entries in `editing-baseline.tsv` retain the before/after counts and source commit. The 30-word reduction is a point-of-use simplification; the measured file count, checks and lifecycle effort do not show a workflow or ceremony saving. No implementation, test, executable-template or fixture bytes changed after `72fecafe`, so the implementation verification remains tied to that commit. This response changes only the plan evidence and its status. No broad suite was rerun for this prose-only record. Status returns to `awaiting-code-review` for review of the response.

## Code review -- Codex (GPT-6.1 Sol), Security Review -- 2026-10-29

```
Reviewed commit: 3993aef0
Target: C3 implementation 72fecafe, scoped evidence d498b308 and same-measures response
Prior findings: none for this code Security Review obligation
```

**Obligation**: Security Review of rule preservation and installed scope authority.
**Findings**: none. **Bounding**: ACCEPTED for the changed rule surfaces and
installed guards. This review performs no authority installation or ceremony.

**Foundations**

1. **Does it do what it claims?** The cut removes repeated explanation while keeping the operative accepted-scope floor, Maintainer-only concession, grouped per-entry dispositions and installed reader path. Real installed controls and independent deletion probes confirmed those duties remain reachable. -- `72fecafe` template diff; `templates/core/dev/plans/_template.md` Scope delta; ledger below.
2. **Best alternative.** Retain the short rule at its point of use and reuse the existing scope owner test for installed output; moving the operating obligation into unshipped doctrine would weaken reach. -- `bootstrap/tests/test_scope_reduction_trap.py` `_assert_installed_scope_delta_obligations`; `bootstrap/_scaffold/config.py` `_CORE_MAPPINGS`.
3. **What would show it wrong?** An install losing Maintainer authority or an assignment/Decision duty, or a guard satisfied by a copied clause outside the operative section. -- falsification ledger below.

**Falsification ledger.** Python 3.13.13; fresh no-hardlink clone detached at
`3993aef0`. The implementation test and both changed templates are byte-identical
to `72fecafe`. No shared source, live key or reference changed.

- Ran `python -m pytest bootstrap/tests/test_scope_reduction_trap.py -q --tb=short -p no:cacheprovider`:
  **89 passed in 0.43 seconds**, including the author's two-profile installed
  controls. This is an owner check, not independent falsification by itself.
- Independently ran the real scaffold command for `solo-greenfield.yml` and
  `high-rigor-legacy.yml`, each into three separate fresh empty targets. Each
  installed template first passed `_missing_installed_plan_scope_obligations`.
  Then edited the installed file and read it back through that guard:
  - solo / remove the quoted Maintainer allowance: killed; missing allowance duty;
  - fuller / remove the quoted Maintainer allowance: killed; missing allowance duty;
  - solo / remove the future-plan assignment and Decision quotation: killed;
    missing assignment/Decision duty;
  - fuller / remove the future-plan assignment and Decision quotation: killed;
    missing assignment/Decision duty;
  - solo / replace the operative section with reviewer permission and move intact
    duties into an unrelated appendix: killed; missing Maintainer-only duty;
  - fuller / the same out-of-section decoy: killed; missing Maintainer-only duty.
  All six mutations were confirmed to change the text; none was equivalent or
  survived. These extend the author's three named installed mutation cases.

**Reasoning and coverage.** Claims, delivery, completeness and refusal (#1–4):
the template diff retains the obligations and the real installations above test
the actual core mapping, rather than only a source copy. The guard isolates the
Scope delta section, so an unrelated mention cannot satisfy the tested duties.
Reuse, drift and placement (#5–7): reviewed the existing scope owner, core mapping,
source/shipped section parity and surviving rationale in installed `AGENTS.md`
and collaboration text. The local and shipped full templates intentionally differ
outside that section; whole-file parity is not claimed. Scope and satisfiers
(#8–9): the same-measures response acknowledges unchanged presentation-file and
ceremony effort; the measured improvement is 30 fewer words at each point of use,
not an unmeasured operational saving. The plan history records the routing and
conflict Waiting lines and the Maintainer's choices before their changes.

The earlier path-instruction correction describes the existing exact,
document-wide registry; its recorded installed positive and sibling/declaration
negative controls and focused review remain the evidence for that slice. This
pass did not repeat those checks, the 781-test mapping, all wording permutations,
an adopter-use trial, historical-anchor reconciliation or a ceremony. Pattern
checks prove sensitivity to particular breaks, not general natural-language
semantic equivalence or truth of a Scope delta declaration. No runtime authority
or new execution surface was added by this template change. Under the Maintainer's
source-work direction, future baseline installation is separate; this pass
clears the distinct code Security Review obligation without claiming installation.
