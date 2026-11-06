# Plan: Scientific plain language

**Source proposal**: [Plain language for technical and scientific writing](../proposals/archive/2026-11-05-terra-scientific-plain-language.md)
**Status**: awaiting-code-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-06
**In brief**: Clarify the writing standard so technical terms stay precise and readers can distinguish simulation and partial source checks from observations and full-text checks.

## Build summary

Revise the existing writing standard and its shipped and public copies, keeping its 17 rule numbers. Verify that the revised standard reaches a fresh install and that its examples communicate the intended distinctions. Record the version change in the existing changelog at its serialization point.

## Source proposal

The accepted heavy proposal changes rules 2, 5, 13, 14 and 17 without adding a scanner or citation ledger. Its Decision at `d3b653d2` retains separate Security Reviews, mutation and installation evidence, fresh-reader examples and final wide Boundary B. The separate January 2027 evaluation remains with the Maintainer and is not a prerequisite.

## Scope

Update `dev/agent_collaboration.md` and `templates/core/dev/agent_collaboration.md` as aligned governing-standard sections, and the reproduced standard and affected descriptions in `docs/plain-language.md`. Check both `AGENTS.md` pointers for consistency; edit them only if needed, with coordinated claims. Update `bootstrap/tests/contract/test_writing_rules_ship.py` for the new standard version and any narrowly needed drift coverage. At the applicable serialization point, coordinate the standard's changelog line and version references in `CHANGELOG.md` with its owner. Preserve the boundary between writing rules and artifact templates, the existing source attribution and rule numbers. No new enforcement tool, research study or gate change is included.

**Reuse.** The existing writing-rules contract checks source agreement, version and a real scaffold install; the public page already reproduces the standard. Search `Cairn Plain Language`, version and rule references in these owners and their readers before editing. N/A: no production code added.

The single-incident doctrine-evolution trigger does not apply to this research-led proposal: its Context and the cited strategy's Method and Part 3 describe comparative literature and a wording audit, not an initiating local incident. This is an applicability determination, not a gate pass or exception; reassess if an initiating incident is identified. Source: delegated Sol determination relayed in coordinating chat, 2026-11-06. The same chat amended scheduling to allow opening before the separate readable-work archive; that archive is not a dependency of this plan.

## Sequence

One Low execution chunk follows both plan reviews and their response. The owners and install contract exist now; no other unfinished plan is a prerequisite. Estimate one to two focused work windows including checks and reviews; mutation and fresh-reader availability add uncertainty.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Revise the standard, public copy and version expectations; verify examples, drift and installation | Both required plan reviews and response | Aligned versioned rules and evidence for review |

After C1, obtain ordinary code review and separate Security Review by fresh reviewers, respond to findings and run final wide Boundary B. Coordinate the changelog entry at its existing serialization point; no release or human trust operation is a plan completion prerequisite.

## Acceptance criteria

**C1.** Rule 2 excludes promotional wording without a banned-word list. Rule 5 retains established domain terms and compounds, defines unfamiliar or coined terms where needed and unpacks only obscuring stacks. Rule 13 distinguishes observed or measured results from simulation, assumptions and expectations. Rules 14/17 cite what was checked and disclose abstract-only or secondary checks when otherwise misleading, without implying an unchecked primary source was read or requiring a note beside every citation. Rule 17 places relevant first-person check limits in deliberation and results records; static references need accurate attribution and limitations, not a diary.

The three standard copies agree; numbers 1–17, writing/template boundary, source attribution and no readability scoring remain. Advance version 1.0 to 1.1 in all standard and public references and the install assertion; record the change in the existing changelog. Fresh reader examples cover an established compound, a coined term, a simulated value, abstract-only and secondary-source citations, and a static reference page; record their conclusions and limits. Neither these examples nor mechanical tests certify source support.

The real scaffold install delivers the shipped standard. Separate source-only, shipped-only and version mutations must make the relevant existing checks fail; record controls, each mutation and any gap. Security preflight remains as in the proposal: no automated admission change; S2 mutations and S3 real-install check occur in C1; no new default or failure path; human review cannot guarantee citation honesty.

### Exact replacement clauses

Replace the numbered rule text in all three copies with the following, preserving their numbers and surrounding group headings:

2. Put the conclusion first, then only what the reader needs to act on it. Leave out filler, vague praise and promotional wording that adds no evidence; do not reject a useful word merely because it appears on a list.
5. Keep established field terms and compounds. Define unfamiliar or project-coined terms where they first matter to the reader. Spell out an acronym the first time unless the reader uses it daily. Unpack stacked nouns when they obscure meaning.
13. Say which claims are observed or measured, simulated, assumed or expected. Never present simulation or assumption as observation or measurement.
14. Give a number with its unit and the source actually checked, not an adjective. Cite the source actually checked for a claim. If a reader might otherwise infer a full-text primary check, say when you checked only an abstract or a secondary account; do not present an unchecked primary source as checked. This disclosure is claim-relevant, not required beside every citation.
17. In proposals, reviews, decisions and reports of results or deliberation, say in the first person what you checked and what remains uncertain when relevant: “I ran the tests and they pass”; “I did not run this on Windows.” Never let fluent prose stand in for a check you did not make. Static reference pages need accurate attribution and relevant source limitations, not a first-person work diary.

Retain rule 14's existing numeric example after the first sentence; leave all other rules and each copy's context-specific template examples intact. In the introduction remove the statement that filler, vague praise and unnumbered probability are the *only* words ruled out; say instead “These rules are not a word list: keep field terms and define unfamiliar terms.” Update the public overview's version and rule summaries to match, and retain its source-check disclosures. Update the version line and install assertion to 1.1. Preserve the remaining context-specific prose rather than making the complete public section byte-identical to the governing section.

### Blind reader check

Give a fresh independent reader the revised rules and only the following numbered prompts, without the answer key or this plan's expected interpretations. Ask them to explain each in their own words and whether the cited check supports the stated claim. Record their answers before comparing with the key; do not coach or share it first. The prompts are invented, and the cited works are hypothetical:

1. “Hydraulic conductivity is the rate coefficient used here. Our new term *bank lag* means the delay between river rise and groundwater rise.” Must either term be replaced, and what needs definition?
2. “The simulation produced 12 mm of recharge; the gauge measured 8 mm. We assume constant soil properties.” Which values were observed and simulated, and what was assumed?
3. “Paper A's abstract reports a 10% increase; I checked the abstract only.” Did the writer check the full paper?
4. “Review B reports that Paper A found a 10% increase; I read B, not A.” Which source was checked and may the writer claim to have checked A?
5. A static reference page says “Review B reports that Paper A found a 10% increase (B); A was not consulted.” Must it add a first-person diary? Is the attribution clear?

**Answer key, withheld until answers are recorded:** (1) retain the established compound; define the unfamiliar coined term where needed, with the existing definition sufficient here; (2) 8 mm observed, 12 mm simulated, soil properties assumed; (3) no; (4) B only, no; (5) no diary, yes, subject to actual support in B. Any opposite inference or inability to explain the relevant distinction fails this check and returns wording to implementation; do not count a failure as passed because the key was later shown. Reader judgment does not verify real source support. Preserve the reader's answers and comparison in the implementation record, not a new evidence folder.

### Drift and installation checks

In the existing `bootstrap/tests/contract/test_writing_rules_ship.py`, add a comparison of the whitespace-normalized text of each changed numbered rule (2, 5, 13, 14, 17) across the local, shipped and public copies. Extract each numbered paragraph through the next numbered rule or group heading; public copy's surrounding examples and source paragraph intentionally differ. Assert each named rule is present exactly once per copy before comparison. Keep this a copy check, not a claim-scoring test.

Run the unmutated contract file first as control in a clean copy of the implementation commit with its local interpreter binding. In three separate physical copies of those committed bytes, bind each copy and make exactly one mutation: (a) in local `dev/agent_collaboration.md` replace “promotional wording” with “promotional claims”; (b) make the same replacement only in the shipped `templates/core/dev/agent_collaboration.md`; (c) in the shipped section replace `*Version 1.1.` with `*Version 1.0.`. Confirm each original anchor occurs once before replacing and no other bytes change. For (a) and (b), run `test_cairns_own_copy_says_what_it_ships` and the new public comparison; both must fail their equality assertion. For (c), run `test_standard_with_version_and_groups_reaches_install`; its real scaffold fixture must install the mutated shipped text and fail its 1.1 assertion. Run the unmutated `test_install_writes_the_shipped_standard_unchanged` as part of the control, but do not treat it as detecting a consistently mutated shipped input. Record each command, exit, assertion and control; if a guard prevents the intended mutation reaching its assertion, report that as unresolved rather than a detected drift. The public comparison must also fail if the public rule alone is changed: use a fourth physical copy with the same rule 2 substitution only in `docs/plain-language.md`, then run the new comparison. No mutation establishes citation truth.

## Scope delta

**Scope delta**: preserved.

## Verification

**Boundary A.** Before editing, search readers and byte pins for every changed file, including public and install paths. Run `python tools/test_tiers.py for <changed paths>` and the resulting scoped iteration list, including `bootstrap/tests/contract/test_writing_rules_ship.py` and its real scaffold installation. Run the relevant claim, link, snippet and neutrality gates and `python scripts/check_cairn.py`; follow any gate triggers to their actual runner. Test negative searches against a known positive. Record commands, interpreter, results, timings, mapped consumers and omissions. Use separate committed copies for writing checks and each mutation; do not bypass integrity guards. Do not run a full-tree certification for this implementation.

**Boundary C.** Ordinary code review and separate Security Review read the committed result, examine the fresh-reader examples and mutation/install evidence, and run only targeted falsification checks. Address cheap advice and required failures before archive; a substantive review fix returns to its reviewer for a targeted look.

**Boundary B.** After reviews and fixes, run wide final change verification on a clean unchanged final commit under canonical Python 3.13.x: mapped iteration checks for the reviewed range plus tier-map integration/workflow tests naming those files and applicable standing gates. Record SHA/range, interpreter, clean pre/post state, commands, counts, timings, touched surfaces, non-passes, omissions and any timing misses; add slow files to the existing consolidation list. A failed required check remains implementation work. Certification and release are separate ceremonies.

## Plan review -- gpt-6.1-terra -- 2026-11-06

**Tier**: Internal
**Obligation**: Internal
**Model**: gpt-6.1-terra (Medium)
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** The scope preserves the accepted copies, numbered rules, examples and separate reviews, but C1 is not yet specified for Low execution (Decision at `d3b653d2`; C1 and finding below).
2. **Best alternative.** Specify the wording and checks in this one chunk; retaining version 1.0 would avoid copy work but leave the accepted distinctions unresolved (Decision options; current `dev/agent_collaboration.md`, rules 5 and 13).
3. **What would show it wrong?** A fresh reader inferring an observed result from simulation, or a full-text primary read from an abstract or secondary source, would falsify the result; an isolated copy mutation that stays green would falsify the drift evidence (Decision delivery fence; `test_writing_rules_ship.py`).

**Finding -- Low execution design is incomplete.** C1 describes desired effects but leaves the implementer to design the operative language for five rules, decide how a fresh reader receives and judges the examples, and select exact mutations and failure checks. The existing contract compares flattened source sections and checks an installed version, but its installed equality compares output to the same shipped source; a shipped-only mutation can make source agreement fail without independently establishing installed drift detection. Specify the rule wording, example inputs and expected interpretations, and for each isolated source-only, shipped-only and version mutation identify its changed bytes, control, real check and expected failure. State how the public copy's agreement is checked. This closes the Low-tier design gap and makes the accepted evidence reproducible without claiming that a mechanical check proves citation meaning (plan C1/Verification; `bootstrap/tests/contract/test_writing_rules_ship.py`, `test_cairns_own_copy_says_what_it_ships`, `test_install_writes_the_shipped_standard_unchanged`, and `test_standard_with_version_and_groups_reaches_install`).

**Coverage:** Read the committed plan at `5856938e`, accepted proposal and Decision, plan template and plan-review guidance, and the contract's actual install and comparison assertions. Did not execute mutations or installation, independently check cited literature, inspect future wording, or perform the separate Security Review.

## Plan review -- gpt-6.1-sol (Security Review) -- 2026-11-06

Reviewed commit: dce760bc

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Model**: gpt-6.1-sol (High)
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: approximately 4 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** The plan preserves the accepted evidence-honesty safeguards and authority limits, but its Low chunk still leaves safety-bearing wording and falsification design to execution -- Decision delivery fence at `d3b653d2`; C1; finding below.
2. **Best alternative.** Complete the wording and evidence matrix inside this same chunk, retaining human interpretation and existing install checks; a scanner adds maintenance without establishing source support -- proposal Rationale and Security preflight; `bootstrap/tests/contract/test_writing_rules_ship.py`.
3. **What would show it wrong?** Give a fresh reader the revised rules and a secondary account citing an unread primary paper: inferring primary verification falsifies citation honesty; treating a simulated value as observed falsifies rule 13 -- Decision delivery fence; current rules 13–17.

**Finding -- Specify the safety-bearing design before Low execution.** C1 lists desired distinctions but does not supply the operative clauses or example inputs and expected interpretations. An implementer must decide how claim-relevant disclosure survives static-page attribution, how established compounds remain precise, and what counts as a misleading implied primary read. Supply those clauses and the fresh-reader protocol, including secondary-source and static-page cases, with explicit failure outcomes. Also name isolated mutation bytes, controls and expected failing assertions for source-only, shipped-only and version drift, plus the public-copy comparison. The existing installed equality compares output against the shipped source: it alone cannot reject a consistently changed shipped input. These specifications close the accepted evidence gap without claiming mechanical verification of citation meaning.

The doctrine applicability statement is appropriately bounded: the actual gate prohibits change *from a single incident*; the strategy's Method and Part 3 describe a literature audit, not such an incident (`docs/methodology/rationale.md`, “How the doctrine evolves under evidence”). This is no gate pass. No new authorization, executable admission path or release operation is proposed.

**Coverage:** Read committed plan, accepted proposal/Decision, current standard, plan template, actual install/comparison assertions and doctrine trigger. Did not execute implementation checks or mutations, verify literature, judge unwritten clauses, or authorize trust operations. This single plan Security pass identifies design repairs; it does not request a clearing pass.

## Plan review response -- gpt-6.1-terra -- 2026-11-06

**Elapsed**: unknown. **Tokens**: unknown.

Both reviews' Low-readiness finding is accepted. Exact replacement clauses, blind independent-reader prompts and withheld key, and isolated copy/version mutations with controls and assertions are now specified in Acceptance criteria. The public comparison covers changed rule paragraphs, not intentionally different surrounding context. No second plan pass is called; implementation and both code reviews remain due.

## Implementation verification -- gpt-6-luna -- 2026-11-06

**Model**: gpt-6-luna (Low). **Tokens**: unknown. **Elapsed**: control 0.42 s as reported by pytest; mutation preparation and aggregate time unknown.

**Bytes and interpreter.** Control and mutations used separate physical clones of committed source `978080e0316e7350bdee2a4bd3dc497814159fae` at `/private/tmp/cairn-plain-language-978080e0` and `/private/tmp/cairn-plain-language-mut-{source-only,shipped-only,version-only,public-only}`. Each clone's local interpreter binding was installed by `bootstrap._scaffold.install.write_local_env`; canonical Python was 3.13.13. The unmutated clone was clean before and after its check. Each mutant changed exactly its named tracked file, confirmed by `git diff --name-only`.

**Control.** `python3.13 -m pytest bootstrap/tests/contract/test_writing_rules_ship.py -q` passed: 52 passed in 0.42 s. This includes the real scaffold install and unmutated `test_install_writes_the_shipped_standard_unchanged`.

**Isolated drift probes.** Every mutation began from the same committed bytes in its own clone; the anchor occurred once in its target section, and the only changed bytes were the specified substitution. All checks reached the intended assertion:

- Source-only rule 2: `dev/agent_collaboration.md`, `promotional wording` → `promotional claims`; ran `test_cairns_own_copy_says_what_it_ships` and `test_changed_rules_match_across_local_shipped_and_public_copies`. Both failed their equality assertions (2 expected failures; 0.05 s).
- Shipped-only rule 2: same substitution only in `templates/core/dev/agent_collaboration.md`; ran the same two nodes. Both failed their equality assertions (2 expected failures; 0.05 s).
- Shipped version: `*Version 1.1.` → `*Version 1.0.` only in `templates/core/dev/agent_collaboration.md`; `test_standard_with_version_and_groups_reaches_install` performed a real install and failed `assert "*Version 1.1." in section` on the installed 1.0 text (1 expected failure; 0.40 s).
- Public-only rule 2: same wording substitution only inside the fenced standard in `docs/plain-language.md`; `test_changed_rules_match_across_local_shipped_and_public_copies` failed with `rule 2 differs` (1 expected failure; 0.04 s).

**Scoped map.** In the clean 978080e0 clone, `python3.13 tools/test_tiers.py for --range 4d2658c1..978080e0 dev/agent_collaboration.md templates/core/dev/agent_collaboration.md docs/plain-language.md bootstrap/tests/contract/test_writing_rules_ship.py templates/core/AGENTS.md` selected 13 tests: `bootstrap/tests/contract/test_writing_rules_ship.py`, `bootstrap/tests/integration/test_gauge.py`, `bootstrap/tests/test_agreement_retired.py`, `test_core_dev_folders.py`, `test_documentation_plan_module.py`, `test_install_report_slots.py`, `test_quickstart_sequence.py`, `test_review_stance_in_shipped_files.py`, `test_review_sweep_ships.py`, `test_scaffold.py`, `test_scope_reduction_trap.py`, `test_upgrade.py`, and `test_upgrade_module_additions.py`. The AGENTS guard omitted 35 additional readers; the omitted set was sent to the coordinating agent. The joined implementation/changelog range and its mapped checks are root-owned and are not included in this author record.

**Fresh reader.** Blinded packet: `/private/tmp/cairn-plain-language-blind-reader-978080e0.md`, SHA-256 `90afcef43a43a7654d5593259a4c7e5d02d35216f3fc2aef64fff5cc388d1018`. It contains the revised standard, the five prompts and neutral response instructions, with no plan or answer key. Independent answers are pending; no reader result is claimed here.

**Coverage / limits.** Covered the assigned contract and all four drift targets, including installed version detection and public-copy agreement. Did not run the other 12 selected test files, the independent reader check, or final Boundary B; no claim is made about citation truth. Root owns the joined pre-review iteration and scoped prose-gate run.


## Implementation verification -- Codex coordination -- 2026-11-06 -- joined iteration and reader

Boundary A on clean `bcd65c3e`, Python 3.13.13, covered the five implementation paths plus `CHANGELOG.md`, mapped over `4d2658c1..bcd65c3e`: **1,663 passed, zero failed or skipped**, 211.266 seconds wall across all 16 selected files. Scoped claim, link, content, snippet and neutrality checks passed; tracked pre/post states were empty. Commands and results: `/private/tmp/cairn-scientific-iteration-h_a8xnsc/result.json`. All six source blobs remain identical through `67a39730`.

The changelog restored two directly named readers: 33 AGENTS guard omissions remain unrun. The 30-second iteration target was missed. The existing consolidation shortlist, slowest first by summed JUnit phases, is `test_upgrade.py` (97.411 s), then `test_upgrade_module_additions.py` (59.065 s); these are not per-file wall times. The earlier extra global prose diagnostics remain unpassed separately.

Independent reader **gpt-6.1-terra** received only the revised standard and five hypothetical prompts before seeing the key. Original answers, preserved at `/private/tmp/cairn-scientific-blind-answers-terra.md`, matched all five interpretations without coaching: established/coined terms, observed versus simulated values, abstract-only checks, secondary attribution, and static-page limits without a diary. This is agent interpretation evidence, not real-source verification or human-usability evidence.

The author's 52-case control and four physical falsifiers are recorded above. Both code reviews, corrections and final wide Boundary B remain due. No private collection, certification or release occurred. **Elapsed:** run above; additional/unknown. **Tokens:** unknown.

## Code review -- gpt-6.1-terra -- 2026-11-06

Reviewed commit: 5678bb63c89c77be985533af3643a5043b6c5ef3

**Obligation**: Internal
**Tier**: Internal
**Model**: gpt-6.1-terra (Medium)
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: unknown. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes: the five changed rules carry the specified distinctions in the three copies, and the changelog records version 1.1; the installed-version assertion and comparison cover the delivery path and changed rules (`978080e0` diff; `bcd65c3e` changelog; contract test).
2. **Best alternative.** Reuse the existing install contract and compare only changed rule paragraphs, as implemented; comparing entire public sections would reject intentional context differences (plan C1; `_numbered_rule` and `_public_section`).
3. **What would show it wrong?** An isolated changed copy passing equality, a mutated installed version passing its assertion, or a reader mistaking simulation or secondary attribution for observation or primary verification would contradict the evidence. The author reports four isolated mutants reaching the expected assertions, and the blind reader's five answers matched the key; I ran the public comparison on clean `978080e0` and it passed (1 passed, Python 3.13.13, 0.02 s).

**Bounding**: ACCEPTED. I challenged the public-copy and install boundaries: the owner reports 52 contract passes, four targeted mutation outcomes and a real install; the joined iteration reports 1,663 passes over 16 mapped files. The 33 AGENTS guard omissions are not claimed as tested, and final wide Boundary B remains due.

**Coverage:** I read the committed plan, accepted proposal, changed source and test diff, changelog, reader and implementation records. I did not repeat the owner's mutations or suite, verify cited research, establish human usability or perform the separate Security Review. The initial `python3.13` command was unavailable on PATH; the targeted check passed using the canonical interpreter path.

## Code review -- gpt-6.1-sol (Security Review) -- 2026-11-06

Reviewed commit: 8deeab5a
Reviewed implementation range: 4d2658c1..8deeab5a (scientific plain-language paths only).

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Model**: gpt-6.1-sol (High)
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: unknown. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes: rules 5, 13, 14 and 17 preserve technical terms, separate simulation from observation and forbid implying an unread primary source was checked; static-page attribution remains required without a diary -- committed standard, public block and accepted Decision delivery fence.
2. **Best alternative.** The existing install contract plus changed-rule comparisons is the proportionate mechanism; a citation scanner would add false confidence without verifying meaning, while whole-public-section equality would reject intentional context differences -- proposal Rationale; `_public_section`, `_numbered_rule` and install fixture in `bootstrap/tests/contract/test_writing_rules_ship.py`.
3. **What would show it wrong?** A changed shipped clause disappearing during installation, or a reader inferring primary verification from secondary attribution, would defeat the result. I ran `test_install_writes_the_shipped_standard_unchanged` on clean isolated `8deeab5a`: Python 3.13.13, 1 passed in 0.31 s; the recorded blind reader distinguishes B's report from checking A -- same contract; preserved reader answers and implementation record.

**Bounding**: ACCEPTED. Challenged the installed instruction boundary and citation interpretation. The author records 52 controls and four isolated mutations reaching their intended assertions, including installed-version and public-copy drift. Joined iteration records 1,663 passes, while naming 33 omitted readers and unpassed global diagnostics. These figures are owner evidence, not reruns by this reviewer. The blind answers support agent interpretation only; neither they nor equality checks establish real citation support. No admission, authority, template-shape or release permission changed; rule numbering and the template boundary remain intact. No C1 deviation or reached human-operation fence was found in the scoped history.

**Coverage:** Read committed clauses, changed tests, accepted scope, changelog, review and implementation records, and original blind answers; isolated check left tracked pre/post state clean. Did not repeat mutations or broad checks, verify literature, establish human usability or perform final wide Boundary B, which remains due.
