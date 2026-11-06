# Plan: Scientific plain language

**Source proposal**: [Plain language for technical and scientific writing](../proposals/archive/2026-11-05-terra-scientific-plain-language.md)
**Status**: awaiting-plan-review
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

## Scope delta

**Scope delta**: preserved.

## Verification

**Boundary A.** Before editing, search readers and byte pins for every changed file, including public and install paths. Run `python tools/test_tiers.py for <changed paths>` and the resulting scoped iteration list, including `bootstrap/tests/contract/test_writing_rules_ship.py` and its real scaffold installation. Run the relevant claim, link, snippet and neutrality gates and `python scripts/check_cairn.py`; follow any gate triggers to their actual runner. Test negative searches against a known positive. Record commands, interpreter, results, timings, mapped consumers and omissions. Use separate committed copies for writing checks and each mutation; do not bypass integrity guards. Do not run a full-tree certification for this implementation.

**Boundary C.** Ordinary code review and separate Security Review read the committed result, examine the fresh-reader examples and mutation/install evidence, and run only targeted falsification checks. Address cheap advice and required failures before archive; a substantive review fix returns to its reviewer for a targeted look.

**Boundary B.** After reviews and fixes, run wide final change verification on a clean unchanged final commit under canonical Python 3.13.x: mapped iteration checks for the reviewed range plus tier-map integration/workflow tests naming those files and applicable standing gates. Record SHA/range, interpreter, clean pre/post state, commands, counts, timings, touched surfaces, non-passes, omissions and any timing misses; add slow files to the existing consolidation list. A failed required check remains implementation work. Certification and release are separate ceremonies.
