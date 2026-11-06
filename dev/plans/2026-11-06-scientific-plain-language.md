# Plan: Scientific plain language

**Source proposal**: [Plain language for technical and scientific writing](../proposals/archive/2026-11-05-terra-scientific-plain-language.md)
**Status**: revising-plan
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
