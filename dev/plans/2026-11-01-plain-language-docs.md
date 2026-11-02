# Plan: Make Cairn's documentation easier to use

**Source proposal**: dev/proposals/archive/2026-11-01-codex-plain-language-docs.md
**Status**: ready-to-archive
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Review Cairn's documentation for clear language while preserving its instructions and technical meaning.

## Source proposal

The Maintainer accepted a heavy review of the README, documentation, existing public methodology, shipped templates and module documents, and the board against Cairn Plain Language 1.0. Improve unclear passages without changing behavior or policy; put the requested marker on shipped templates only.

## Scope

Read all requested prose, including unchanged material, in groups: reader entry points and frequently followed guidance first; remaining `docs/` and board; methodology and its installed operating homes; then remaining shipped templates and module documents. Identify shipped templates through actual install and module mappings, including `bootstrap/_scaffold/config.py`, rather than assuming every file in `templates/` is installed. Read the final committed board, changelog and proposal-summary work; coordinate owners before editing overlaps. A clear document needs no edit. Record group coverage and unresolved failures concisely in the plan; no per-file ledger, evidence folder or extra review stage.

Coordinate with `dev/plans/2026-11-01-retire-doctrine.md`. The methodology has moved to its final public home; review all of it there and account for its installed homes, including split duties. Carry any remaining improvements into the final homes. Avoid polishing the same content twice; do not treat the move itself as the reading review.

Preserve versioned Plain Language rules themselves unless separately authorized. Preserve commands, examples, conditions, warnings, permissions, claims, links and existing non-template markers. Resolve uncertain meaning against its source before editing; leave ambiguous text unchanged and its failure open until resolved. Do not introduce new requirements or policy.

**Reuse.** N/A: no code added. Use existing install mappings, prose gates and tests, not a new audit tool.

### Documentation / doctrine surface

Descriptive prose stays in `docs/`, cross-cutting prescription in governing and installed homes, and board deliberation in `dev/`. Public methodology at `docs/methodology/` and its installed homes are in scope, including duties split across those homes. Shipped authoring templates and methodology are protected surfaces.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Inventory requested groups and installed templates, readers, pins and checks; coordinate overlapping owners and relocation timing | Plan reviews | Concise group scope and check mapping in implementation record |
| C2 | Read and improve entry points, frequently followed guidance, remaining docs and board | C1; coordinate owners | Clearer reader-facing prose |
| C3 | Read methodology at current or final homes and remaining shipped templates and module documents; add template markers | C1; coordinate relocation and owners | Reviewed guidance and markers |
| C4 | Ordinary and Security Reviews; fix findings and run final wide integration | C2–C3 and iteration evidence | Review and verification records |

## Acceptance criteria

### C1

Inventory the requested prose from the committed tree and actual install/module mappings, identify titles and format constraints for shipped templates, and search for readers, byte pins and applicable checks. Test negative searches against a known positive. Map checks to their triggers, input sets and real entry points before editing; record group boundaries and coordination. Unresolved meaning or a required check keeps its group open.

### C2–C3

Read every inventoried group against all 17 rules and improve failures without changing intended behavior. Compare changes to their sources, retain the versioned rules, and preserve existing non-template markers. Place `Written in Cairn Plain Language 1.0` directly below each shipped template title only. For a titleless template, use an existing format-safe title or add a format-safe title and marker only if its consumers retain their behavior; if neither is possible, keep that group open for resolution. Inspect installed output and real consumers where relevant. Account for all methodology content, including installed splits, and record unresolved failures by group until closed. No scope is silently dropped.

### C4

Independent ordinary and Security Reviews inspect the committed implementation and iteration evidence; review fixes receive the required targeted look. Final wide Boundary B covers the reviewed range and review fixes on a clean final commit. Unmet criteria and checks block archive.

## Scope delta

**Scope delta**: preserved.

## Verification

**Boundary A:** Before editing, run `python tools/test_tiers.py for <changed paths>` and its selected tests during iteration. Search actual readers and pins, follow each named check to its trigger and runner, and compare checks with the instructions they protect. Run applicable claim, link, snippet and neutrality gates, including `python scripts/check_cairn.py`, `python scripts/claim_check.py` on documents before commit, `python scripts/link_check.py`, `python scripts/sync_doc_snippets.py` in check mode where applicable, and `python scripts/quality_gate.py --sub neutrality`. Preserve snippet sources, installed output and fidelity contracts. Exercise real entry points and meaningful deletion or inversion mutations where required to establish that affected checks detect lost conditions or altered protected instructions; report omissions and failures. Inspect markers and sample instructions for placement and unchanged behavior.

**Boundary C:** A reviewer other than the implementer reads committed changes and iteration evidence and runs only targeted falsification checks, not a suite. The separate Security Review remains required. A fix beyond a failing test returns for the required targeted look.

**Boundary B:** After review, run the mapped iteration and integration/workflow selections and applicable standing gates in wide mode on a clean, unchanged final commit under canonical Python 3.13. Record tested SHA and range, interpreter, pre/post state, commands and counts, elapsed time, tokens or `unknown`, non-pass dispositions, omissions, timing misses and slow-test reporting. Keep missing checks open.

## Plan review -- Codex (Internal Reviewer, gpt-6.1-sol) -- 2026-11-01

Reviewed commit: `7e12719f`  
Obligation: Internal  
Verdict: No blocking findings. Elapsed time: approximately 2 minutes; tokens: unknown.

**Foundations**

1. **Should it happen as framed?** Yes. The accepted proposal calls for the full prose set, preserved meaning and a marker only on shipped templates. Scope and C1–C3 cover those outcomes, identify installed templates from actual mappings, and retain versioned rules.
2. **Best alternative.** Wait until the doctrine move is complete before reading methodology. This avoids a possible repeat, but risks indefinite delay; Scope instead permits reading now and carrying improvements forward, or reading all final homes and splits if the move happens first. The separate retirement plan leaves the reading review here.
3. **What would show it wrong?** An unread relocated duty, a lost condition or a marker that breaks a template would falsify the result. C2–C3 require source comparison, all methodology content, and format-safe placement; Verification maps checks to actual consumers.

The group-based sequence gives useful priorities without a per-file ledger or new audit machinery. Its plain language makes the sequence and stopping conditions clear. Coordination and reading the final board, changelog and proposal-summary work prevent assuming those changes complete the broader audit.

**Coverage:** Compared the committed plan with the accepted proposal and doctrine retirement plan, including scope, sequencing and verification. Did not inventory every template or reader, run implementation checks, or assess future edits; separate Security Review remains due.

## Plan review -- Codex (Security Review, gpt-6.1-sol) -- 2026-11-01

Reviewed commit: `d02d0f51e9d7d0a513f285bcb618c7bfbb270575`  
Target: Scope, C1–C4 and Verification  
Prior findings: none  
Assurance path: high-assurance (accepted proposal)

**Obligation**: Internal Security Review  
**Tier**: Internal Security Review  
**Findings**: none  
**Verdict**: No blocking findings. **Elapsed**: approximately 4 minutes; **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. C1–C3 preserve the accepted full reading scope, source meaning and template-only marker. Scope protects permissions and versioned rules; the shipped collaboration document requires versioning for reworded rules (`templates/core/dev/agent_collaboration.md`, Cairn Plain Language).
2. **Best alternative.** Use existing install mappings and checks, and record results by group. C1 uses `bootstrap/_scaffold/config.py`, and Scope excludes new machinery. Both plans coordinate final public and installed homes.
3. **What would show it wrong?** An omitted installed duty, softened prerequisite or marker that corrupts a consumer would defeat the preservation contract. C2–C3 require source comparison and installed-output inspection; Verification requires real entry points and meaningful deletion/inversion checks where needed. The retirement plan separately retains installed reach and path-dependent guards.

Titleless templates remain open unless format-safe placement preserves their consumers. Wide final integration follows both reviews; certification and re-anchor remain unauthorized.

**Coverage:** Compared the committed plan, accepted proposal, retirement coordination, installer mappings, shipped versioned-rule contract and snippet check mode. Did not inventory all readers, perform installs or mutations, run implementation checks or establish future prose equivalence.

## Plan review response -- Codex (plan author) -- 2026-11-01

**Elapsed**: approximately 1 minute; **Tokens**: unknown.

Both reviews found no blocking findings or changes to dispose. Coordinate the methodology reading with the doctrine move and read the final committed board work as Scope already specifies. The plan is ready to implement.

## Implementation verification -- Codex (Implementation) -- 2026-11-01

Closed the quickstart changelog install guidance and fixture: the throwaway
starts with only `README.md`, install supplies the template changelog and a
lockfile, and the install commit includes `CHANGELOG.md`. Added the existing-
history limitation and linked the migration guidance. No installer behavior
changed. Iteration: `python -m pytest bootstrap/tests/test_quickstart_sequence.py
bootstrap/tests/test_review_stance_in_shipped_files.py` — 490 passed in 2.89 s
under Python 3.12.9. Prose gates: claim checks on this plan and quickstart,
quickstart link check, snippet check, and neutrality gate passed. Elapsed:
approximately 8 minutes; tokens: unknown. This is focused iteration evidence;
the plan's final wide Boundary B remains open.

## Coordination -- Codex (plan author) -- 2026-11-01

The board-layout plan owns the single rewrite of `templates/core/dev/PLANNING.md`, including its shipped-template marker. This audit will read its final committed version against the accepted Plain Language and marker requirements without repeating that rewrite. Any remaining failure stays open for resolution. Elapsed: approximately 1 minute; tokens: unknown.

## Focused code review -- Codex (Internal Reviewer, gpt-6.1-sol) -- 2026-11-01

Reviewed commits: `4871b8db`, `14f94b1e` on committed tree `260231cd`  
Verdict: **Blocking finding.** Elapsed: approximately 4 minutes; tokens: unknown.

**Foundations**

1. **Should it happen as framed?** Yes. The clean-install lock writer refuses a differing tracked file, and migration records mergeable files without a recoverable base (`bootstrap/_scaffold/install.py`, `upgrade.py`). The quickstart correctly describes that tradeoff for existing history.
2. **Best alternative.** Keep the README-only starting repository and use the shipped changelog; preserving the old fixture would prevent a clean baseline. Include the changelog in both install-commit instructions.
3. **What would show it wrong?** A real terminal walkthrough that leaves the generated changelog uncommitted defeats the stated outcome; a parity comparison that stops before an operative model-tier obligation would leave drift untested.

**Finding (blocking):** The terminal `git add` command in `docs/quickstart.md` omits `CHANGELOG.md`, although the adjacent agent instruction includes it and the implementation record promises the install commit includes it. A terminal user leaves the new file untracked. Add it to the command and check the actual documented command's resulting commit. The fixture stages the changelog itself, so it does not falsify this omission.

**Evidence:** The model-tier extractor captures the entire current paragraph in both committed copies; separate clause checks retain task floors, authorization and review obligations. Targeted clean Git-backed copy checks under Python 3.12.9: fresh-install node and parity node, 2 passed in 0.27 s. An initial mistyped node selected no tests; corrected above.

**Coverage:** Reviewed the two corrections, relevant lock/migration implementation and committed plan evidence. Did not review the remaining documentation groups, run a suite, or perform Security Review; final wide Boundary B remains open.

## Focused correction -- Codex (Implementation) -- 2026-11-01

Addressed the blocking finding from review commit `6281285f`: the documented
terminal `git add` now includes `CHANGELOG.md`. The quickstart test extracts
and runs the documented `git add` and `git commit` commands, then checks the
resulting commit tree includes the changelog. In a clean Git-backed copy under
Python 3.12.9, the two selected files passed: 490 tests in 3.52 seconds.
Elapsed: approximately 5 minutes; tokens: unknown. This focused correction
returns to the same reviewer for targeted re-look; final wide Boundary B
remains open.

## Focused review re-look -- Codex (Internal Reviewer, gpt-6.1-sol) -- 2026-11-01

Reviewed commit: `9da627e7`. **Verdict:** The blocking finding is closed. The terminal command now stages `CHANGELOG.md`; the test extracts and executes both documented commands and checks the resulting commit. The targeted install node passed in a clean Git-backed copy under Python 3.12.9 (1 passed, 0.33 s). Elapsed: approximately 1 minute; tokens: unknown.

**Coverage:** Rechecked the correction and its behavior test only. Did not review other documentation groups or perform Security Review; final wide Boundary B remains open.

## Implementation group status -- Codex (Implementation) -- 2026-11-01

Committed work covers parts of C2 and C3; it does not establish that either
full reading group is complete. Elapsed: approximately 10 minutes; tokens:
unknown.

**C2 — entry points and frequently followed guidance.** `1f2d1f69` records
README, quickstart and project-site edits, with claim, link, snippet, Cairn
content and neutrality checks. Its mapped selection reported 1,443 passed and
one quickstart install failure (`dev/.cairn/cairn-lock.yml` expected). Later
quickstart work records 490 passed across the install-sequence and shipped
review-stance tests, and the review re-look records the install test passing;
the original selection was not rerun as a whole. `c58effb3` records the
getting-started edit and its named test and prose checks passing (481 tests).
These commits do not document a full entry-point reading review.

**C2 — remaining general docs.** `cf84805f` edits four guidance documents;
the commit records claim checks only and says targeted readers and prose gates
will be reported later. Those results are absent here. README and index material
were left to the entry-point work. The rest of `docs/`, the board, changelog,
and proposal-summary work have no recorded Plain Language read or disposition.

**C3 — public methodology.** `2643e096` records three revised methodology
documents and twelve read without a high-value edit. It defers targeted tests
to a separate copy without recording their outcome. It does not account for
the complete final public methodology or its split installed homes after the
doctrine move.

**C3 — core and module templates.** `37c07e0d` records markers on thirteen
core templates and passing prose gates; the selected test run was refused and
no tests ran. Its coordinating `PLANNING.md` rewrite still needs this audit's
read against the marker and language criteria. `af8d1263` records edits to
nine module guidance files and claim checks, but defers reader tests and prose
gates. Other shipped templates and module documents are not accounted for.

**C3 — titleless issue forms.** `9184eb50` adds an H1 and an HTML-comment
marker to four GitHub and four GitLab forms. This is the chosen format-safe
placement, but the acceptance condition is not yet evidenced: the commit
explicitly leaves the real scaffold copy path and GitHub `name`, `about`, and
`labels` values for a follow-up check. Keep this group open until those checks
are recorded and show the consumers retain their behavior.

**Still open.** C1's complete mapping of installed files, readers, pins and
checks, including the known-positive negative-search check, is not recorded.
No entry above closes the full groups it touches. Before archive, record the
missing targeted selections and standing prose gates for `cf84805f`,
`2643e096`, `37c07e0d` and `af8d1263`; complete the issue-form scaffold/YAML
check; read and disposition the remaining docs, final board/changelog and
proposal-summary work, all final methodology homes, and remaining shipped
templates. Then complete independent ordinary and Security Reviews and wide
Boundary B on the reviewed range. No tests were run for this status record.

## Supplemental implementation reports -- Codex (Implementation) -- 2026-11-01

Correction to the group status above, using implementing agents' reports
supplied in chat. These outcomes were not present in the cited commit messages.
Elapsed: approximately 3 minutes; tokens: unknown.

`cf84805f` covers the remaining general-doc reading group. Its seven targeted
tests and all standing prose gates passed under Python 3.12.9. This group is
covered; it is not waiting on the checks named in the preceding status note.

`af8d1263` covers the module-guidance group. The group review, fifteen targeted
tests, and all prose gates passed. The former claim that these reader tests and
gates were still outstanding is superseded.

`37c07e0d` has 132 targeted tests and the prose gates passing. The separate
broader 43-file selection was refused by the runner; this means that broad
selection did not run. It does not negate the focused results. The final wide
Boundary B remains required after review and must account for the mapped
coverage that the refused selection could not provide.

`9184eb50` was checked in a clean clone through the real installer: all GitHub
and GitLab forms copied; each GitHub front-matter block remained byte- and
YAML-equal; prompts were preserved; prose gates passed. This satisfies the
reported consumer-preservation check for the format-safe headings and hidden
markers on the titleless forms.

**Remaining scope and assurance.** C1's complete inventory, readers, pins,
check mapping and known-positive negative-search evidence remain unrecorded
here. This record also has no Plain Language disposition for the final board,
changelog and proposal-summary work; no complete account of final methodology
and split installed homes; and no all-17-rule read/disposition for the core
templates or other shipped templates beyond the reported module-guidance and
issue-form groups. The separate `2643e096` methodology report still defers its
targeted test outcome. These items, the required independent ordinary and
Security Reviews, and final wide Boundary B remain open. The prior status's
claim that `cf84805f`, `af8d1263` and `9184eb50` checks are missing is
superseded by this report.

## Board-reading report -- Codex (Implementation) -- 2026-11-01

Per the board-reading implementing agent's report in chat, the agent read the
final shipped board, current board, changelog and proposal/plan templates
against Cairn Plain Language 1.0. The agent corrected the board markers and
summary prompts. The read found one unexplained AST abbreviation on the
current board; `60bcaab8` spells out Abstract Syntax Tree at first use and
records passing claim, link and neutrality checks. This reports that board
reading and correction only; it does not establish completion of other reading
groups or the full board/changelog/template scope. Elapsed: approximately 2
minutes; tokens: unknown. No tests run for this record.

## Documentation group coverage -- Codex (Implementation) -- 2026-11-01

All 15 final `docs/methodology/` files were read against Cairn Plain Language
1.0. `2643e096` clarified the methodology README, consolidation review and
roles; the other 12 were read without a high-value edit. The core-template
review separately covered the installed operative homes and 15 mapped core
prose files; `f89c0908` records its clarity change. The board reading and its
change are recorded separately above.

The first-use reading covered `docs/README.md`, `docs/getting-started.md`, the
project site, all three onboarding presets, optional `CONTRIBUTING.md`, and
both shipped lifecycle skills. `00908eb2` aligns the site's three-lane graphic
and accessible description with the ordinary-uncertainty rule, and defines two
fit measures at first use. Its SVG XML parse and changed-file diff check passed;
the neutrality gate passed with fail=0. `test_tiers` selected zero direct
reader test files for the HTML and SVG. An initial `check_cairn` run found one
broken strategy-record link; `008a5378` repaired it and a later run passed.

This reading record does not establish C1's complete inventory of readers,
pins and checks, or cover every remaining shipped template and document. The
independent ordinary and Security Reviews and final wide Boundary B remain
open. Elapsed: approximately 10 minutes; tokens: unknown.

## Code review -- Codex (Internal Reviewer, gpt-6.1-sol) -- 2026-11-01

Reviewed commit: `f4b7d393`. **Verdict: Blocking findings.** Elapsed: approximately 4 minutes; tokens: unknown.

**Foundations**

1. **Should it happen as framed?** Yes. The accepted proposal covers the full requested reading and preserves conditions and template consumers; the plan's C1–C3 make those outcomes explicit.
2. **Best alternative.** Prioritize entry points while completing the remaining groups. Reviewing only those pages would lose the accepted coverage of less-visible guidance and templates.
3. **What would show it wrong?** An unread shipped instruction, a lost condition or a marker that breaks a consumer would defeat the outcome. The plan requires mapped consumers and source comparison; the issue-form report records a real installer and front-matter check.

**Findings**

- **Blocking — incomplete reading:** The documentation coverage record explicitly does not cover every remaining shipped template and document. C2–C3 require every inventoried group to be read and unresolved failures closed. Complete and record the remaining group dispositions, including final proposal-summary work, before claiming completion.
- **Blocking — incomplete mapping and checks:** The same record says C1's complete inventory of readers, pins and checks is not established; the supplemental report also identifies missing known-positive negative-search evidence. C1 and Boundary A require these checks, not merely an administrative summary. Complete the mapping, follow checks to their runners and inputs, test negative searches against a known positive, and run any outstanding required checks or record their results.

The site/SVG correction aligns ordinary uncertainty and new-boundary wording with the governing rule; the reported issue-form installer check supports the selected hidden marker placement. The focused quickstart review finding was closed by its re-look. Final wide Boundary B follows both reviews and remains due.

**Coverage:** Read the accepted proposal, committed plan and implementation reports, issue-form and site changes, and changed-surface inventory. Relied on reported implementation checks; did not independently read every changed document, rerun a suite, verify every marker or conduct Security Review.

## Code Security Review -- Codex (Security Review, gpt-6.1-sol) -- 2026-11-01

Reviewed implementation at `58544046`, including `14f94b1e`, `37c07e0d`, `af8d1263`, `9184eb50`, `f89c0908` and `00908eb2`.
**Obligation:** Internal Security Review
**Verdict:** No security blocking findings in the inspected changes. **Elapsed:** approximately 8 minutes; **Tokens:** unknown.

**Foundations**

1. **Should it happen as framed?** Yes. The accepted proposal preserves permissions and technical meaning. The inspected module edits retain domain ownership and review independence; core markers add no authority; the site now retains the explicit stop at a newly discovered trust boundary.
2. **Best alternative.** Keep format-safe headings and hidden markers for issue forms, preserving their metadata and prompts. This meets the marker request without changing default issue titles.
3. **What would show it wrong?** A lost refusal, drift hidden by the narrowed parity extractor, or changed issue metadata would defeat preservation. Source comparison found no such change in the inspected edits.

**Evidence:** Targeted committed-byte falsification under Python 3.12.9 confirmed the protected extractor captures the final reviewer obligation and detects changes to both the governance-boundary refusal and that final clause. Removing only the added heading/marker from each of eight issue forms recovered its exact prior content. An initial mutation missed wrapped text; corrected mutations asserted target presence. No suite ran. Existing clause-presence controls remain intact in `14f94b1e`.

**Coverage:** Compared accepted preservation requirements, committed plan evidence, operative model-tier guidance, module changes, core markers, issue forms and site/SVG. Relied on reported installer and prose checks. Did not read every unchanged document, independently exercise hosted issue interfaces, or run final integration; ordinary review findings remain separately owed.

## Implementation response -- Codex (Implementation) -- 2026-11-01

The phase-0/readiness group is now covered. `templates/phase-0/README.md` is
guidance, not a fillable template. The greenfield profile, legacy profile, team
profile and Codebase Readiness Report are fillable templates; `6f887f4c` puts
the marker below each title. Bootstrap instructions and adopter guidance point
to them. The profile files are not copied automatically by the installer; I
found no parser that reads their marker line. Claim and link checks, snippet
check, neutrality and the directly mapped legacy-profile test passed. No broad
selection ran.

For C1, the ordinary-review report gives a group-level mapping: `config.py`
lines 534, 913, 948 and 1020 cover core prose, skills, optional content and
modules; `install.py` lines 1562–1609 cover onboarding, and lines 1784–1821
cover forge copying. It names direct readers and maps the applicable gate
triggers to their runners and input sets. Its negative search found no direct
reader for `docs/index.html` or `docs/assets/three-lanes-of-change.svg`; the
known-positive controls for `docs/quickstart.md` and `docs/methodology/roles.md`
found their expected readers. No evidence ledger was added.

For `2643e096`, I built a clean committed snapshot and ran only the four nodes
that read `docs/methodology/roles.md`: `test_model_tier_rule_ships.py::test_proposal_authoring_and_ordinary_review_are_medium`, two
`test_review_stance_in_shipped_files.py::test_doctrine_carries_the_statement`
cases (cost rule and cleanup), and its retired-privilege case. All four passed
under Python 3.12.9. Python 3.13 was unavailable. Those assertions check the
model-tier and cost clauses, not the changed introductory passage. No test
reads the changed passages in the methodology README or consolidation review,
and the roles path classification test does not read its text. These checks do
not establish semantic equivalence for all 17 rules. No suite or broad
selection ran.

The reviewer's C1 mapping is recorded at group level; it does not establish a
per-file inventory or resolve every remaining shipped document/template
group. Independent ordinary and Security Review findings, and final wide
Boundary B, remain open. Claim check passed on this plan. Elapsed: approximately
12 minutes; tokens: unknown.

## Targeted review re-look -- Codex (Internal Reviewer, gpt-6.1-sol) -- 2026-11-01

Reviewed `af413952` and `6f887f4c` against the findings at `3c5dd98c`. **Verdict:** Both findings are closed on the reported group coverage and mapping. Elapsed: approximately 2 minutes; tokens: unknown.

The phase-0/readiness report now covers the identified missing group; the four fillable files carry the marker immediately under their titles, while the guidance README remains unmarked. The board report includes the final proposal and plan templates. Together with the earlier group reports, I have not identified a specific unread requested group. My earlier finding relied too broadly on the record's qualification rather than a named omission; an exhaustive written file ledger is not required.

The response identifies install and module mapping entry points, reader searches, gate triggers and known-positive controls, and reports the previously deferred methodology reader tests. This closes the mapping finding without requiring a per-file ledger. The reported checks do not prove prose equivalence; source comparison remains the basis for meaning. Final wide Boundary B and any independent Security Review disposition of the new changes remain due.

**Coverage:** Inspected the response and four marker diffs and relied on the implementing agents' group and check reports. Did not reread every document, independently repeat their checks, or run a suite.

## Implementation verification -- Codex (Implementation) -- 2026-11-01

The wide mapped selection ran once on a clean clone at `8362b863` under
canonical Python 3.13.13. `test_tiers.py for` selected 33 test files from the
reviewed range `7e12719f..8362b863`; its changed-passage guard omitted 37
additional `AGENTS.md` readers. Pytest ran once with the 33 selected files,
collected 1,818 nodes, and reported 1,803 passed and 15 failed in 106.25
seconds. The clone was clean before and after the run.
The 33 files were `test_ceremony_review_report.py`,
`test_certifying_run_rule.py`, `test_check_release_publication.py`,
`test_default_security_stance.py`, `test_doc_governance.py`,
`test_finalize_retired_living_state.py`, `test_incident_trackers_module.py`,
`test_intents_tool.py`, `test_loop_fidelity_gate.py`,
`test_model_selection_stub.py`, `test_module_roster.py`,
`test_onboarding_seed_roster.py`, `test_onboarding_slot_substitution.py`,
`test_oracle_activation.py`, `test_portable_security_sweeps.py`,
`test_presets.py`, `test_prune_tools.py`, `test_quickstart_sequence.py`,
`test_replacement_tools.py`, `test_review_stance_in_shipped_files.py`,
`test_review_sweep_ships.py`, `test_scaffold.py`,
`test_scientific_check_guidance_ships.py`, `test_scope_reduction_trap.py`,
`test_session_routines.py`, `test_skill_contract.py`,
`test_skills_onboarding.py`, `test_status_vocabulary_advisory.py`,
`test_upgrade_added_slots.py`, `test_upgrade_module_additions.py`,
`test_verification_boundaries.py`, `test_verify_stems.py`, and
`test_writing_rules_ship.py`.
Fourteen `test_portable_security_sweeps.py` nodes failed because the environment
refused `_Canary`'s loopback socket bind. The remaining failure,
`test_writing_rules_ship.py::test_cairns_own_copy_says_what_it_ships`, exposed
the source-citation mismatch corrected in `5fec62c4`.

On the same clone, `check_cairn` passed (187 Markdown files; 91 external links
not probed), the plan claim check passed, `link_check` passed (187 Markdown
files; 92 external links not probed), the snippet check passed (503 documents;
no drift), and neutrality passed (fail=0, info=43).

After `5fec62c4`, the implementing agent reports that the focused citation
equality test passed. On a clean clone of that commit under Python 3.13.13,
the 14 previously socket-blocked nodes passed with loopback available (14
passed in 7.17 seconds). Ordinary and Security Reviewers report no findings on
the citation correction.

The full 33-file selection has not been repeated after the correction. Its
final check remains open pending Maintainer disposition; these results do not
claim a fully passing Boundary B. Per-file timings for the 33-file run were
not captured, so its slow-file list is unknown. No full suite ran. Elapsed:
unknown; tokens: unknown.

## Implementation response -- Codex (Implementation) -- 2026-11-01

The Maintainer explicitly accepted the focused Boundary B results in chat:
"Accept focused results" (2026-11-01), in response to the request to finish
without repeating the full 33-file selection after the citation correction.
This disposes of that remaining check as accepted focused results. The record
continues to distinguish the measured 1,803-pass initial selection, the
focused citation test, and the 14 socket-blocked nodes that later passed; it
does not claim the 33-file selection was rerun or fully passed. The ordinary
and Security Reviews report no findings on the correction. No broad selection,
certification, repin or re-anchor was run. Elapsed: unknown; tokens: unknown.
