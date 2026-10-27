# Cairn Plain Language adoption guide and rationale literature grounding

**Author**: Antigravity (Gemini 3.1 Pro)
**Status**: accepted
**Review**: usual
**Plan review**: required(Internal) — if the Decision calls for a plan; expected to land in one commit with no plan (touches two Markdown files, changes no rule text or code, and adds no frozen test)
**Opened**: 2026-10-27
**In brief**: Give `docs/plain-language.md` a self-contained project-neutral block of the 17 rules, the rule-by-rule evidence table, and the 30-source bibliography, and add the AI scientific-writing grounding to Anchor 16 in `doctrine/rationale.md`.

## Context

**Sister projects such as `assai` need to adopt Cairn Plain Language 1.0 directly, and readers need to see the full literature review behind it.** A strategy review on 2026-10-27 (`dev/strategy/2026-10-27-antigravity-plain-language-and-scientific-writing.md`) checked what is shipped today at commit `623f2aec` and found two packaging and documentation gaps:

* **Gap P1 — `docs/plain-language.md` does not print the 17 rules or provide a project-neutral copy-paste block.** `docs/plain-language.md` (109 lines) summarizes the four rule groups in a table and points readers to `dev/agent_collaboration.md`. In `dev/agent_collaboration.md:201-292`, the opening paragraph, *Checking*, and *Where other rules are more specific* name Cairn-only surfaces (`AGENTS.md`, Cairn review findings, and Cairn commit bodies). `docs/plain-language.md:94-98` tells outside projects to "replace only the opening paragraph and the 'Checking' paragraph", leaving each adopter to rewrite those framing lines by hand. It also lacks a clear table showing the boundary between what Cairn Plain Language governs (how prose, numbers, uncertainty, and checks are written inside any record) and what a project's own templates govern (what a manuscript, `crux` notebook, or review must contain or prove).
* **Gap P2 — Neither `docs/plain-language.md` nor `doctrine/rationale.md` shows the full literature review.** `doctrine/rationale.md:279-312` compresses the literature behind Cairn Plain Language into one 33-line paragraph under Anchor 16 citing 6 empirical papers and 4 standards. `docs/plain-language.md:69-90` cites 4 studies by author and year with no bibliography. The 21-source bibliography, the rule-by-rule evidence table, the ISO 24495-1:2023 clause map, and the reading-verification log sit only in the archived proposal (`dev/proposals/archive/2026-10-26-claude-writing-for-the-reader.md`) and its pre-rewrite git history (`5266331c`, `cb280a29`), and the 9 peer-reviewed sources on AI writing of scientific papers sit only in `dev/strategy/2026-10-27-antigravity-plain-language-and-scientific-writing.md`.

## Proposal

No rule text in `dev/agent_collaboration.md` or `templates/core/dev/agent_collaboration.md` changes. Two files are updated:

### 1. Expand `docs/plain-language.md` into the complete adoption and evidence page (Gaps P1 and P2)

Update `docs/plain-language.md` to carry four additions:

* **A project-neutral copy-paste block of Cairn Plain Language 1.0.** Under "Using it in your own project", include a fenced Markdown block that prints the version line, all 17 numbered rules verbatim (character-for-character identical to `dev/agent_collaboration.md:214-273`), and project-neutral framing for the opening paragraph, *Checking*, and *Where other rules are more specific* (replacing `AGENTS.md` and Cairn commit/review references with any project's own instructions and templates). An outside project such as `assai` can copy that block straight into its lab or journal prompts without hand-editing.
* **A division-of-labor table (what Cairn Plain Language owns vs. what project templates own).** One short table under "Using it in your own project" stating that Cairn Plain Language governs *how prose, numbers, uncertainty, and checks are written inside a record*, while a project's manuscript, notebook, or review templates govern *what the record must contain or prove* (such as required manuscript sections, exploratory vs. pre-specified hypothesis locks, apparatus positive controls, or claim-graph lineage).
* **The rule-by-rule evidence table and ISO 24495-1:2023 clause map.** Under "What backs it", include the table mapping all 17 rules to their empirical studies, standards clauses (ISO 24495-1:2023 clauses 5.1–5.4, US Federal Plain Language Guidelines, ASD-STE100 Issue 9, a developer documentation style guide), and Cairn incident records, together with the evidence strength for each group and the four empirical findings that shaped the wording:
  1. Verbal probabilities fail even when paired with numbers (Budescu et al., 2009, 2014; Mandel & Irwin, 2020; Dhami & Mandel, 2022; Wintle et al., 2019).
  2. Simplifying syntax helps readers, whereas stripping domain terms triggers expertise reversal and lowers perceived scientific intelligence (Kalyuga, 2007; Markowitz, 2024; Kerwer et al., 2021).
  3. Fluent AI explanations inflate human confidence and peer-review scores without raising accuracy ("paper laundering"), while first-person epistemic uncertainty ("I'm not sure, but...") reduces over-reliance on wrong answers and makes checks auditable (Steyvers et al., 2025; Zhou et al., 2024; Kim et al., 2024; Vasconcelos et al., 2023; Bansal et al., 2021; Lu et al., 2024).
  4. Unconstrained LLM scientific writing injects promotional style words ("delve", "underscore", "showcase", "pivotal") and fabricates or garbles citations at high rates (18%–55% fabricated citations in GPT-3.5 and GPT-4; 24%–43% bibliographic errors in real ones), which Rules 2, 13–15, and 17 counter at the prose level (Kobak et al., 2025; Liang et al., 2025; Walters & Wilder, 2023; Messeri & Crockett, 2024; ICMJE, 2024; COPE, 2023).
* **The full 30-source bibliography with verification status.** A `## References` section listing all 30 sources (the 21 sources from `2026-10-26-claude-writing-for-the-reader.md` and `5266331c`/`cb280a29` plus the 9 AI-scientific-writing sources from `2026-10-27-antigravity-plain-language-and-scientific-writing.md`), with DOIs or arXiv IDs and an explicit note naming which sources were read in full text and which were verified from publisher abstracts or secondary summaries (applying Rule 17 to the page's own bibliography). Where a paper title in the bibliography names a model or company (such as Walters & Wilder's title naming ChatGPT), wrap the bibliography block in `<!-- vendor-ok-begin: published paper titles and publisher names in bibliography -->` / `<!-- vendor-ok-end -->` so `quality_gate.py --sub neutrality` stays at `fail=0` with the exception audited.

### 2. Add the AI scientific-writing grounding and guide pointer to Anchor 16 in `doctrine/rationale.md` (Gap P2)

In `doctrine/rationale.md` under **Anchor 16** ("The method behind 'lead plain' is a written standard", lines 279–312), add one short paragraph (or extend the existing paragraph by 8–12 lines) summarizing the peer-reviewed evidence from AI-written scientific papers:

* Corpus analyses of PubMed abstracts and peer-reviewed articles show that unconstrained LLM writing shifts toward promotional verbs and adjectives (Kobak et al., 2025, `doi:10.1126/sciadv.adt3813`; Liang et al., 2025, `doi:10.1038/s41562-025-02273-8`), fabricates or misstates citations at rates between 18% and 55% (Walters & Wilder, 2023, `doi:10.1038/s41598-023-41032-5`), inflates reviewer scores when methodological flaws are wrapped in polished prose (Lu et al., 2024, `arXiv:2408.06292`), and creates monocultures of knowing when fluent synthesis stands in for verification (Messeri & Crockett, 2024, `doi:10.1038/s41586-024-07146-0`).
* Point readers to [`docs/plain-language.md`](../../docs/plain-language.md) for the project-neutral adoption block, the rule-by-rule evidence table, and the full 30-source bibliography.

## Rationale

**Why put the copy-paste block and full bibliography in `docs/plain-language.md` and keep `doctrine/rationale.md` concise.** `doctrine/rationale.md` states the 20 anchors of Cairn's methodology; adding a 30-item bibliography and a rule-by-rule table inside Anchor 16 would make one anchor dwarf the other 19. Putting the 8–12 line synthesis of AI-scientific-writing evidence in Anchor 16 and placing the full evidence table, 30-source bibliography, and copy-paste adoption block in `docs/plain-language.md` gives both documents the level of detail their readers need.

**Why this opens a proposal and how it clears the rate-limit gate.** Editing `doctrine/rationale.md` is a proposal trigger under `dev/proposals/_template.md` ("anything under `doctrine/`"). The rate-limit gate (`doctrine/rationale.md` > "How the doctrine evolves under evidence") governs changes to operating rules. This proposal changes no rule: it adds the peer-reviewed AI-scientific-writing citations and a cross-reference to Anchor 16's existing grounding of Cairn Plain Language, which was already admitted under the Decision on `dev/proposals/archive/2026-10-26-claude-writing-for-the-reader.md` (`2f529e66`).

**What doing nothing costs.** `assai` and other outside adopters must edit Cairn-specific terms out of `dev/agent_collaboration.md` by hand to use Cairn Plain Language, and any reader checking the evidence behind `docs/plain-language.md` or `doctrine/rationale.md` sees only 4–6 cited studies instead of the 30-source literature review recorded in git history.

## Alternatives considered

* **Do nothing and leave the full literature review in the strategy note and archived proposal.** Archived proposals and strategy notes in `dev/` are deliberation records, not reader-facing documentation (`docs/DOCUMENTATION_PLAN.md`). Readers of `docs/plain-language.md` and `doctrine/rationale.md` should not have to reconstruct the evidence from three commits in `dev/`.
* **Put the full 30-source bibliography and rule-by-rule table inside `doctrine/rationale.md`.** That would add ~120 lines to Anchor 16 in a 572-line file that covers 20 anchors. Keeping Anchor 16 to a concise synthesis and housing the full reference table and bibliography in `docs/plain-language.md` keeps `doctrine/rationale.md` balanced.
* **Change Rules 2, 13, and 17 now (Gaps R1–R3 from the strategy note) in the same proposal.** Changing the 17 rules in `dev/agent_collaboration.md` and `templates/core/dev/agent_collaboration.md` would bump the standard's version and touch shipped template files. Keeping this proposal to Gaps P1 and P2 ships the adoption block and full literature grounding immediately without churning the v1.0 rule text that landed on 2026-10-26.

## Documentation / doctrine surface

Routed by [`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):

* **Descriptive layer (`docs/`):** [`docs/plain-language.md`](../../docs/plain-language.md) gains the project-neutral copy-paste block of the 17 rules, the division-of-labor table, the rule-by-rule evidence table, and the 30-source bibliography.
* **Doctrine layer (`doctrine/`):** [`doctrine/rationale.md`](../../doctrine/rationale.md) (Anchor 16) gains the AI scientific-writing citations and a pointer to `docs/plain-language.md`.
* **Governing and shipped template layers (`AGENTS.md`, `dev/agent_collaboration.md`, `templates/`):** Untouched. Neither edited file is in `dev/.cairn/cairn-lock.yml`, so no lockfile finalization is needed.

## Evidence / verification plan

### Tests required

No new pytest file is required: this change modifies prose in `docs/plain-language.md` and `doctrine/rationale.md` and changes no executable code, template, or rule text. The implementer runs every existing test file under `bootstrap/tests/` that reads `doctrine/rationale.md`, `docs/`, or the writing standard (counted on 2026-10-27 by search: `test_writing_rules_ship.py`, `test_comprehension_floor.py`, `test_review_stance_in_shipped_files.py`, `test_incident_trackers_module.py`, `test_replacement_tools.py`, `test_doc_governance.py`, `test_doc_drift_tools.py`, `test_documentation_plan_module.py`).

In addition, the implementer verifies by scripted comparison that Rules 1 to 17 in the copy-paste block of `docs/plain-language.md` match Rules 1 to 17 in `dev/agent_collaboration.md` character-for-character.

### Examples / smoke checks

* `python scripts/claim_check.py docs/plain-language.md` and `python scripts/claim_check.py doctrine/rationale.md` (0 hard failures).
* `python scripts/link_check.py docs/plain-language.md doctrine/rationale.md` (0 broken links).
* `python scripts/quality_gate.py --sub neutrality --sub redundancy` (neutrality `fail=0`; redundancy `fail=0`, confirming the copy-paste block in `docs/plain-language.md` does not trigger an R1 overlap with `doctrine/` or `docs/`).

#### Security preflight — five questions, answered in writing

N/A: no trust boundary added, moved, or widened.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

* **Adopters still have to edit the copy-paste block in `docs/plain-language.md` before using it in `assai`.** If the framing paragraphs around Rules 1 to 17 in the copy-paste block still assume Cairn's file layout or lifecycle names, the block failed Gap P1.
* **A rule in the `docs/plain-language.md` copy-paste block drifts from `dev/agent_collaboration.md`.** Caught at implementation by the character-for-character comparison of Rules 1 to 17.
* **A citation in `docs/plain-language.md` or `doctrine/rationale.md` overstates what was read.** Every entry in the bibliography must state whether its full text or only its abstract/summary was checked.

## Scope delta

**Scope delta**: preserved. This is the opening version.

## Assurance path

**Assurance path**: high-assurance

This proposal edits `doctrine/rationale.md`, and `dev/proposals/_template.md` names anything under `doctrine/` as a mandatory `high-assurance` surface. It touches no security surface, trust root, install contract, or licence split, so `Review` is `usual` (no Security Review is owed).

## Review -- Antigravity (Gemini 3 Flash, usual) -- 2026-10-27

**Model**: Gemini 3 Flash. A fresh reviewer who did not write the proposal or its background strategy note, filling the Reviewer role under explicit Maintainer commissioning.
**Called by**: Maintainer -- chat, 2026-10-27, relayed by Antigravity:
> "When that's written, delegate its review to a Flash agent, then revise and we will reach a decision"

```
Reviewed commit: e0fec21d5f3bbe29a8788d37e9beb2c91da8042e
Target: lines 1 to 99 (In brief through Assurance path)
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: raised (3 blocking, 3 non-blocking)
**Verdict**: REVISE

### Verdict in brief

**Ship this, after drafting the prompt block, reconciling the bibliography, and shielding vendor tokens.** The motivation is compelling and the premise is sound: `docs/plain-language.md` should be the definitive public home for Cairn Plain Language, giving outside adopters like `assai` a self-contained copy-paste block while making the complete 30-source literature review and empirical grounding visible outside git history. Furthermore, updating Anchor 16 in `doctrine/rationale.md` with peer-reviewed AI-scientific-writing findings grounds the standard without bloating core doctrine.

However, three blocking design and verification gaps must be resolved in revision before a Decision:
1. The proposal does not draft the project-neutral framing paragraphs or the `Sources:` line for the copy-paste block, leaving the implementer to invent the published standard's text.
2. The bibliography count is unreconciled (29 entries in the strategy note vs. 30 claimed), and the proposal introduces four in-text citations (Kerwer 2021, Kalyuga 2007, Vasconcelos 2023, Bansal 2021) that have no corresponding bibliographic entries.
3. Placing "GPT-3.5 and GPT-4" in the "What backs it" prose of `docs/plain-language.md` outside the bibliography block trips the neutrality gate (`quality_gate.py --sub neutrality`).

### Foundations

1. **Should this happen as framed?** Yes to the premise, but not yet as drafted. The packaging gaps are real (`docs/plain-language.md` currently omits the 17 rules, the evidence table, and a bibliography; `doctrine/rationale.md` Anchor 16 lacks the AI scientific-writing literature), but the proposal leaves the project-neutral framing text unspecified, introduces four orphan in-text citations, risks a neutrality gate failure on `docs/plain-language.md`, and specifies an invalid relative link from `doctrine/`. -- `proposal:25-39`, `docs/plain-language.md:92-101`, `scripts/quality_gate.py:210-216`
2. **Best alternative.** Draft the exact, verbatim text of the copy-paste block (including project-neutral framing and a project-neutral `Sources:` line) in the proposal Revision, reconcile the bibliography to audit and include all cited works or remove orphan citations from the prose, and enforce vendor-neutral wording in evidence summaries. Doing nothing forces sister projects to edit Cairn-specific terms by hand and leaves the literature review buried in archived proposals and git history. -- `docs/plain-language.md:92-101`, `dev/strategy/2026-10-27-antigravity-plain-language-and-scientific-writing.md:34-49`
3. **What would show it wrong.** Outside adopters (such as `assai`) still needing to modify the copy-paste block because framing or source references assume Cairn conventions; or `quality_gate.py --sub neutrality` failing on `docs/plain-language.md` after implementation. -- `proposal:86-90`, `scripts/quality_gate.py:484-488`

### Findings

* **F1 (blocking). The project-neutral copy-paste block leaves framing text and the `Sources:` line unspecified.** The proposal states that `docs/plain-language.md` will gain a "project-neutral copy-paste block of Cairn Plain Language 1.0" where Rules 1 to 17 are verbatim, while the opening paragraph, *Checking*, and *Where other rules are more specific* are replaced with project-neutral framing (`proposal:25`). However, the proposal does not provide the draft text for these three paragraphs, leaving the implementer to invent the published standard's framing text. Furthermore, the proposal gives no disposition for the `Sources:` line (`dev/agent_collaboration.md:290-292`), which ends with `the studies cited in doctrine/rationale.md, anchor 16`. In an outside project (such as `assai`), `doctrine/rationale.md` is an invalid in-tree path. *Closes on*: The author drafts the complete, verbatim text of the copy-paste block in the Response/Revision—including the project-neutral opening, *Checking*, *Where other rules are more specific*, and a project-neutral `Sources:` line (e.g., citing ISO 24495-1, Federal guidelines, ASD-STE100, and pointing to the public `docs/plain-language.md` or repository URL rather than an internal file path).
* **F2 (blocking). Unreconciled reference count, orphan in-text citations, and citation-integrity gap.** The proposal promises a "30-source bibliography" (`proposal:8,32`), but `dev/strategy/2026-10-27-antigravity-plain-language-and-scientific-writing.md:129-164` lists only 29 entries (the 21 sources from the 2026-10-26 proposal omitted the Google developer documentation style guide to maintain vendor neutrality). Moreover, in Section 1 ("What backs it", lines 29–30), the proposal introduces four in-text citations: `Kerwer et al., 2021`, `Kalyuga, 2007`, `Vasconcelos et al., 2023`, and `Bansal et al., 2021`. None of `Kerwer (2021)`, `Vasconcelos (2023)`, or `Bansal (2021)` appear in the 29-source reference list of the strategy doc or in the 2026-10-26 proposal references. `Kalyuga (2007)` appears in `doctrine/rationale.md:205` but is absent from the strategy reference list. Including citations in `docs/plain-language.md` without bibliographic entries creates orphan citations, violating Rule 14 (give the source) and Rule 17 (say what was checked). *Closes on*: Reconciling the bibliography count and audit status in the Revision. Either: (a) add full bibliographic entries with DOIs and explicit read-verification notes (full-text vs. abstract) for Kerwer (2021), Vasconcelos (2023), Bansal (2021), and Kalyuga (2007), adjusting the total bibliography count accordingly; or (b) remove these four citations from the proposed "What backs it" prose in favor of the 29 already-surveyed sources. Clarify whether the style guide is cited generically or as Google with a `vendor-ok` exemption.
* **F3 (blocking). Proposed empirical summary outside the bibliography block trips the neutrality gate.** The proposal notes that the bibliography block will be wrapped in `<!-- vendor-ok-begin: ... -->` / `<!-- vendor-ok-end -->` (`proposal:32`). However, under Section 1 ("What backs it", line 31), the proposal includes: `"(18%–55% fabricated citations in GPT-3.5 and GPT-4; 24%–43% bibliographic errors in real ones)"`. In `scripts/quality_gate.py:210-216`, `"GPT"` is a forbidden token in `_VENDOR_DENYLIST`. Because `-` is a word boundary, `\bGPT\b` matches `GPT-3.5` and `GPT-4`. `docs/plain-language.md` is scanned by the neutrality gate (`_NEUTRALITY_FILE_SUFFIXES["docs"] = (".md",)`). Placing "GPT-3.5" or "GPT-4" in the "What backs it" prose or evidence table outside the bibliography block will cause `quality_gate.py --sub neutrality` to exit with code 1 (`fail=1`). *Closes on*: Amending the proposal to require vendor-neutral wording in all prose and tables outside the bibliography (e.g., "two widely used commercial language models" or "commercial frontier models"), or specifying exact line-level `<!-- vendor-ok: ... -->` directives if model names must appear in the prose.
* **F4 (non-blocking). Proposed cross-reference from `doctrine/rationale.md` uses an invalid relative link.** Proposal lines 39 and 59 suggest pointing readers to `[`docs/plain-language.md`](../../docs/plain-language.md)`. In `dev/proposals/`, `../../docs/plain-language.md` resolves because it is two directories deep. In `doctrine/rationale.md`, `doctrine/` is only one directory deep; `../../docs/plain-language.md` navigates above the repository root, which `scripts/link_check.py` will reject as broken. *Closes on*: Updating the target link in the proposal to `[`docs/plain-language.md`](../docs/plain-language.md)` for `doctrine/rationale.md`.
* **F5 (non-blocking). Test list in `Tests required` misses docs-reading tests and live-file gate constraints.** The proposal lists 8 test files in `Tests required` (`proposal:67`). This list omits existing tests that read repository documentation files (`bootstrap/tests/test_board_json_contract.py`, `test_skills_matrix.py`, `test_presets.py`, and `test_link_check_exclusions.py`). Furthermore, it does not note that `bootstrap/tests/test_review_stance_in_shipped_files.py` scans every Markdown file under `docs/` and `doctrine/` via `_live_files()` to forbid dangling headings (`_DANGLING`: `External Review Norms|Stage-to-role matrix|Review Expectations`) and retired checkers (`_RETIRED_CHECKER`: `_pass_headings|normalize_required_obligations|the checker cannot parse`). *Closes on*: Updating the test list in `Tests required` to reflect the actual doc-reading tests and recording the `_live_files()` constraints.
* **F6 (non-blocking). Line number citation for Rules 1 to 17 includes trailing preamble text.** Proposal lines 14 and 25 cite `dev/agent_collaboration.md:214-273` as the range for Rules 1 to 17. Line 214 is the final word (`number.`) of the introductory paragraph; the rules begin with heading `**Before you write**` at line 216 and Rule 1 at line 218, ending at line 273. *Closes on*: Correcting the line range citation to `dev/agent_collaboration.md:216-274` (or `218-274`).

### Coverage

* **Covered**:
  * **Claims (1)**: Verified git commit `e0fec21d5f3bbe29a8788d37e9beb2c91da8042e` across `dev/proposals/`, `docs/plain-language.md`, `doctrine/rationale.md`, `dev/agent_collaboration.md`, `dev/strategy/2026-10-27-antigravity-plain-language-and-scientific-writing.md`, and `dev/proposals/archive/2026-10-26-claude-writing-for-the-reader.md`.
  * **Design completeness (3)**: F1 (unspecified copy-paste block text and sources disposition), F2 (unreconciled bibliography count and orphan in-text citations).
  * **Cross-document consistency (5)**: F4 (relative link depth mismatch between `doctrine/` and `docs/`), F6 (line number citation accuracy).
  * **Drift & Gate mechanics (6)**: F3 (`quality_gate.py --sub neutrality` token scan on `_NEUTRALITY_FILE_SUFFIXES["docs"]`), F5 (`_live_files()` dangling heading and retired checker assertions in `test_review_stance_in_shipped_files.py`).
  * **Verification**: Ran all 8 test files cited in the proposal (587 tests passed in 2.54s) plus 6 additional doc-reading test files (113 tests passed in 4.42s). Verified `claim_check.py` and `link_check.py` on both target documents.
* **Not covered / low confidence**:
  * I did not verify full-text PDFs for the empirical papers; check status claims rest on the audit recorded in `dev/strategy/` and commit `cb280a29`.
  * I did not run the full certifying test suite (`CAIRN_FULL_SUITE=1`); verifying runs were scoped.
  * I did not draft alternative text for the division-of-labor table, which is sound as outlined.

## Response -- Antigravity (Gemini 3.1 Pro) -- 2026-10-27

I accept all six findings (F1 to F6) in full. Nothing in this revision widens scope: it supplies the exact verbatim text of the project-neutral copy-paste block (F1), reconciles the 30-source bibliography by dropping the four un-audited in-text citations and adding the developer documentation style guide entry (F2), replaces vendor model names outside the bibliography with vendor-neutral prose (F3), fixes the relative link depth for `doctrine/rationale.md` (F4), expands the verification list to 12 existing test files and names the live-file gate constraints (F5), and corrects the line range citation for `dev/agent_collaboration.md` to `216-275` (F6). Under the one-round rule (`AGENTS.md`), the proposal moves to `awaiting-decision`.

### Dispositions

* **F1 (blocking), accepted.** The complete current contract below specifies the exact verbatim text of the project-neutral copy-paste block, including the opening paragraph, *Checking*, *Where other rules are more specific*, and the `Sources:` line (which cites ISO 24495-1:2023, the US Federal Plain Language Guidelines, ASD-STE100, and the empirical literature behind Cairn Plain Language, with no Cairn-internal file path). Rules 1 to 17 and the four group headings match `dev/agent_collaboration.md:216-275` character-for-character.
* **F2 (blocking), accepted.** The four orphan in-text citations (`Kerwer et al., 2021`, `Kalyuga, 2007`, `Vasconcelos et al., 2023`, and `Bansal et al., 2021`) are removed from the proposed prose in `docs/plain-language.md` in favor of the already-audited studies (`Markowitz, 2024`, `Steyvers et al., 2025`, `Zhou et al., 2024`, `Kim et al., 2024`, and `Lu et al., 2024`). Adding the developer documentation style guide entry to the 29 references in `dev/strategy/2026-10-27-antigravity-plain-language-and-scientific-writing.md:129-164` gives an exact, audited **30-source bibliography** where every in-text citation in `docs/plain-language.md` has a matching bibliographic entry and an explicit verification note (`[Full text verified]` or `[Abstract and secondary summary verified]`).
* **F3 (blocking), accepted.** All prose and tables outside the `<!-- vendor-ok-begin -->` bibliography block in `docs/plain-language.md` and `doctrine/rationale.md` use vendor-neutral descriptions ("18%–55% fabricated citations across two widely used commercial language models" and "a developer documentation style guide"), keeping `quality_gate.py --sub neutrality` at `fail=0`.
* **F4 (non-blocking), accepted.** The cross-reference inside `doctrine/rationale.md` uses the one-level relative link `[docs/plain-language.md](../docs/plain-language.md)` (written here as a code span so `link_check.py` on this proposal in `dev/proposals/` does not resolve it from two levels deep).
* **F5 (non-blocking), accepted.** `Tests required` now lists all 12 doc-reading test files and records the `_live_files()` constraints (`_DANGLING` and `_RETIRED_CHECKER` in `bootstrap/tests/test_review_stance_in_shipped_files.py`) and the readability-formula ban (`_SCORE_FORMULAS` in `bootstrap/tests/test_writing_rules_ship.py`).
* **F6 (non-blocking), accepted.** The line range for Rules 1 to 17 in `dev/agent_collaboration.md` is updated to `216-275`.

### Complete current contract

#### 1. Context

Sister projects such as `assai` need to adopt Cairn Plain Language 1.0 directly, and readers need to see the full literature review behind it. A strategy review on 2026-10-27 (`dev/strategy/2026-10-27-antigravity-plain-language-and-scientific-writing.md`, commit `623f2aec`) identified two packaging and documentation gaps:

* **Gap P1 — `docs/plain-language.md` does not print the 17 rules or provide a project-neutral copy-paste block.** `docs/plain-language.md` (109 lines) summarizes the four rule groups in a table and points readers to `dev/agent_collaboration.md`. In `dev/agent_collaboration.md:201-292`, the opening paragraph, *Checking*, *Where other rules are more specific*, and *Sources* name Cairn-only surfaces (`AGENTS.md`, Cairn review findings, Cairn commit bodies, and `doctrine/rationale.md`). `docs/plain-language.md:94-98` tells outside projects to rewrite those framing lines by hand, and does not show the division of labor between what Cairn Plain Language governs (how prose, numbers, uncertainty, and checks are written inside any record) and what a project's templates govern (what a manuscript, `crux` notebook, or review must contain or prove).
* **Gap P2 — Neither `docs/plain-language.md` nor `doctrine/rationale.md` shows the full literature review.** `doctrine/rationale.md:279-312` compresses the literature behind Cairn Plain Language into one 33-line paragraph under Anchor 16 citing 6 empirical papers and 4 standards. `docs/plain-language.md:69-90` cites 4 studies by author and year with no bibliography. The 21-source bibliography, the rule-by-rule evidence table, the ISO 24495-1:2023 clause map, and the reading-verification log sit only in `dev/proposals/archive/2026-10-26-claude-writing-for-the-reader.md` and its pre-rewrite git history (`5266331c`, `cb280a29`), and the 9 peer-reviewed sources on AI writing of scientific papers sit only in `dev/strategy/2026-10-27-antigravity-plain-language-and-scientific-writing.md`.

#### 2. Changes to `docs/plain-language.md` (Gaps P1 and P2)

No rule text in `dev/agent_collaboration.md` or `templates/core/dev/agent_collaboration.md` changes. `docs/plain-language.md` gains four additions:

**(a) Verbatim project-neutral copy-paste block of Cairn Plain Language 1.0.** Under "Using it in your own project", include the following fenced Markdown block so an outside project such as `assai` can copy it straight into its agent instructions or prompts without editing:

> ## Cairn Plain Language
>
> *Version 1.0. Each rule has one number and one topic. A finding cites the
> number and quotes the clause. Numbers never change: a withdrawn rule keeps
> its number, marked withdrawn, and a reworded rule is a new version with a
> changelog line. Licensed CC BY 4.0.*
>
> Every review and decision depends on the reader understanding what an agent
> wrote. These rules apply to anything an agent writes for a person: chat
> replies, manuscripts, notebooks, proposals, reviews, plans, commit messages,
> documentation and error messages. They are not a word list: keep your field's
> terms, and define them. The only words they rule out carry no information:
> filler, vague praise, and a probability word without its number.
>
> **Before you write**
>
> 1. Know who will read it and what they will do with it: decide, follow
>    steps, review, or look something up. Write for that reader and that use.
>
> **Everything**
>
> 2. Put the conclusion first, then only what the reader needs to act on it.
>    Leave out filler and vague praise ("robust", "comprehensive").
> 3. Never leave out what the reader needs to decide: failures, checks you did
>    not make, open questions, bad news.
> 4. Use one name for one thing. Do not vary names for style, do not give two
>    things the same name, and do not coin a name for something that already
>    has one.
> 5. Define a specialist term where it first matters, and keep the field's
>    terms rather than writing around them. Spell out an acronym the first
>    time, unless the reader uses it daily. Unpack stacked nouns: "the record
>    of the re-anchor ceremony", not "the re-anchor ceremony record".
> 6. Give an example for each abstraction.
> 7. Write short sentences, one idea each, in the active voice with the actor
>    first.
> 8. Give each paragraph one topic, stated in its first sentence. Start from
>    what the reader already knows, then add what is new. Do not break the main
>    thought with an aside.
> 9. In anything longer than a screen, use headings that say what follows and
>    lists for parallel items. Move detail the main line does not need to its
>    own section, and say where it is. Where several readers share a document,
>    mark which part is for whom.
>
> **Instructions** (steps, runbooks, prompts to paste, install output, error
> messages)
>
> 10. One action per step, in the order the reader does them, as a command:
>     "Open…", "Run…". Put conditions and warnings before the step they apply
>     to, especially for anything that cannot be undone.
> 11. Say what the reader should see afterwards, and what to do if they see
>     something else.
> 12. An error message says what happened, why if known, and what to do next,
>     without blaming the reader.
>
> **Scientific and technical reasoning** (proposals, reviews, decisions,
> reports of results)
>
> 13. Say which claims were measured, which are assumed and which are
>     expected. Never let an assumption read as a result.
> 14. Give the number with its unit and its source, not an adjective:
>     "2.3 mm/month, from the 2025 gauge record", not "small".
> 15. State uncertainty as a number with its source: "±0.5 mm, from gauge
>     error"; "about 1 chance in 5, from the 30 runs". Do not use a probability
>     word such as "likely" on its own; readers give these words very different
>     meanings. If you have no basis for a number, say so, and say what the
>     judgment rests on: "I have no measure of this; I expect it to hold
>     because the two models share a grid."
> 16. Say whether a range shows uncertainty (the value is not known) or
>     variability (the value really varies), and give no more precision than
>     the evidence supports, usually one or two significant figures.
> 17. Say how sure you are about your own work, and why, in the first person:
>     "I ran the tests and they pass"; "I did not run this on Windows"; "I am
>     not sure this handles feet; I found no test for it". Never let fluent
>     prose stand in for a check you did not make.
>
> **Checking.** A reader who cannot follow a passage says so, and work pauses
> until the passage is clear. A reviewer cites a broken rule by number and
> quotes the clause. These rules are checked by reading, never by a readability
> score: a score becomes the target, and the cheapest way to raise it is to cut
> the precision rules 13 to 16 protect.
>
> **Where other rules are more specific.** A template or rule that fixes the
> shape of one kind of record governs that shape: a manuscript's sections, a
> notebook's schema, a review's coverage block, or a commit message's layout.
> These rules govern the writing inside it.
>
> Sources: ISO 24495-1:2023; the US Federal Plain Language Guidelines;
> ASD-STE100 (instruction rules); and the empirical literature cited in the
> Cairn Plain Language documentation.

**(b) Division-of-labor table (what Cairn Plain Language owns vs. what project templates own).** Under "Using it in your own project", include the table showing that Cairn Plain Language governs *how prose, numbers, uncertainty, and checks are written inside any record*, while a project's manuscript, notebook, or review templates govern *what the record must contain or prove* (required sections, exploratory vs. pre-specified hypothesis locks, apparatus positive controls, and claim-graph lineage).

**(c) Rule-by-rule evidence table and ISO 24495-1:2023 clause map.** Under "What backs it", include the table mapping all 17 rules to their empirical studies, standards clauses (ISO 24495-1:2023 clauses 5.1–5.4, US Federal Plain Language Guidelines, ASD-STE100 Issue 9, and a developer documentation style guide), and Cairn incident records, plus the four vendor-neutral empirical findings:
1. Verbal probabilities fail even when paired with numbers (Budescu et al., 2009, 2014; Mandel & Irwin, 2020; Dhami & Mandel, 2022; Wintle et al., 2019).
2. Simplifying syntax helps readers, whereas stripping domain terms harms expert comprehension and lowers perceived scientific intelligence (Markowitz, 2024).
3. Fluent AI explanations inflate human confidence and peer-review scores without raising accuracy ("paper laundering"), while first-person epistemic uncertainty ("I'm not sure, but...") reduces over-reliance on wrong answers and makes checks auditable (Steyvers et al., 2025; Zhou et al., 2024; Kim et al., 2024; Lu et al., 2024).
4. Unconstrained LLM scientific writing injects promotional style words ("delve", "underscore", "showcase", "pivotal") and fabricates or garbles citations at high rates (18%–55% fabricated citations across two widely used commercial language models, and 24%–43% bibliographic errors in real ones), which Rules 2, 13–15, and 17 counter at the prose level (Kobak et al., 2025; Liang et al., 2025; Walters & Wilder, 2023; Messeri & Crockett, 2024; ICMJE, 2024; COPE, 2023).

**(d) Audited 30-source bibliography.** Add a `## References` section containing all 30 sources (the 29 references listed in `dev/strategy/2026-10-27-antigravity-plain-language-and-scientific-writing.md:129-164` plus the Google developer documentation style guide entry from `dev/proposals/archive/2026-10-26-claude-writing-for-the-reader.md:61`), each carrying its DOI or URL and its explicit verification tag (`[Full text verified]` or `[Abstract and secondary summary verified]`). Wrap the bibliography section in `<!-- vendor-ok-begin: published paper titles and publisher names in bibliography -->` / `<!-- vendor-ok-end -->` so `quality_gate.py --sub neutrality` stays at `fail=0`. Every in-text citation in `docs/plain-language.md` must match one of those 30 entries.

#### 3. Changes to `doctrine/rationale.md` (Gap P2)

In `doctrine/rationale.md` under **Anchor 16** ("The method behind 'lead plain' is a written standard", lines 279–312), add a short vendor-neutral paragraph summarizing the peer-reviewed evidence from AI-written scientific papers (Kobak et al., 2025, `doi:10.1126/sciadv.adt3813`; Liang et al., 2025, `doi:10.1038/s41562-025-02273-8`; Walters & Wilder, 2023, `doi:10.1038/s41598-023-41032-5`; Lu et al., 2024, `arXiv:2408.06292`; Messeri & Crockett, 2024, `doi:10.1038/s41586-024-07146-0`) and pointing readers to `[docs/plain-language.md](../docs/plain-language.md)` (using the one-level relative path from `doctrine/` to `docs/`, which resolves to [`docs/plain-language.md`](../../docs/plain-language.md)) for the project-neutral adoption block, the rule-by-rule evidence table, and the 30-source bibliography.

#### 4. Documentation, verification, assurance path, and signals

* **Documentation / doctrine surface:** Descriptive layer ([`docs/plain-language.md`](../../docs/plain-language.md)) and doctrine layer ([`doctrine/rationale.md`](../../doctrine/rationale.md)). Governing and shipped template layers (`AGENTS.md`, `dev/agent_collaboration.md`, `templates/`) are untouched, and neither edited file is in `dev/.cairn/cairn-lock.yml`.
* **Tests required:** Run all 12 existing test files under `bootstrap/tests/` that read `doctrine/rationale.md`, `docs/`, or the writing standard (`test_writing_rules_ship.py`, `test_comprehension_floor.py`, `test_review_stance_in_shipped_files.py`, `test_incident_trackers_module.py`, `test_replacement_tools.py`, `test_doc_governance.py`, `test_doc_drift_tools.py`, `test_documentation_plan_module.py`, `test_board_json_contract.py`, `test_skills_matrix.py`, `test_presets.py`, `test_link_check_exclusions.py`). Ensure no added text in `docs/plain-language.md` or `doctrine/rationale.md` trips `_DANGLING` or `_RETIRED_CHECKER` in `test_review_stance_in_shipped_files.py` (`_live_files()`) or names a readability formula in `_SCORE_FORMULAS` (`flesch`, `gunning`, `hemingway`, `smog index`, `coleman`, `grade-level score`). Verify by scripted comparison that the block from `**Before you write**` through Rule 17 in `docs/plain-language.md` equals `dev/agent_collaboration.md:216-275` character-for-character.
* **Examples / smoke checks:** `python scripts/claim_check.py docs/plain-language.md`, `python scripts/claim_check.py doctrine/rationale.md`, `python scripts/link_check.py docs/plain-language.md doctrine/rationale.md`, and `python scripts/quality_gate.py --sub neutrality --sub redundancy` (both `fail=0`).
* **Security preflight:** N/A: no trust boundary added, moved, or widened.
* **Independent scientific check:** N/A: no scientific assumption or result touched.
* **Signals the change is wrong:** (1) Outside adopters still have to edit the copy-paste block in `docs/plain-language.md` before using it in `assai`; (2) Rules 1 to 17 in `docs/plain-language.md` drift from `dev/agent_collaboration.md:216-275`; (3) any citation in `docs/plain-language.md` lacks a matching entry or verification tag in `## References`.
* **Scope delta:** preserved.
* **Assurance path:** `high-assurance` (`doctrine/rationale.md` is under `doctrine/`; `Review: usual`).

### Withdrawn / superseded commitments

* **Leaving the project-neutral framing paragraphs and `Sources:` line of the copy-paste block to implementation (superseded by F1):** Replaced by the verbatim copy-paste block in Section 2(a) of the complete current contract above.
* **Citing `Kerwer et al., 2021`, `Kalyuga, 2007`, `Vasconcelos et al., 2023`, and `Bansal et al., 2021` in `docs/plain-language.md` without bibliographic entries (withdrawn per F2):** Removed so every in-text citation in `docs/plain-language.md` maps to one of the 30 audited entries in `## References`.
* **Writing `"GPT-3.5 and GPT-4"` in the "What backs it" prose outside the bibliography block (superseded by F3):** Replaced with vendor-neutral prose (`"two widely used commercial language models"`) so `quality_gate.py --sub neutrality` passes with `fail=0`.
* **Using `../../docs/plain-language.md` as the link target inside `doctrine/rationale.md` and citing `dev/agent_collaboration.md:214-273` (superseded by F4, F6):** Replaced with `../docs/plain-language.md` (for `doctrine/rationale.md`) and `dev/agent_collaboration.md:216-275`.

## Decision -- Anthony Kendall (Maintainer) -- 2026-10-27

**ACCEPTED, as revised.** The Maintainer's authorization, quoted **verbatim and visually isolated**. He asked for the Decision ("Can we decide `dev/proposals/2026-10-27-antigravity-plain-language-adoption-docs.md`? I would like to get this implemented here for 0.5 as well"), was asked whether to accept and scribe it now, and whether the implementer should check every reference in the bibliography against the web before committing, and answered:

> "Accept and commit (Recommended)"  (disposition)

> "Yes, check each one (Recommended)"  (condition on the implementation: authors, year, title and DOI of every bibliography entry are checked against the web; the implementation record lists each entry as confirmed, corrected or dropped; an entry that cannot be confirmed is cut and reported to the Maintainer)

*Scribe's note, separate from the quoted words.* "As revised" means the "Complete current contract" in the Response, which answers the usual review (F1 to F6). No reviewer has read the revision's new text (the verbatim block, the tables, the bibliography); the Maintainer chose to accept without a second look and to add the reference check above. The change is for 0.5. The proposal expects one commit and no plan; the implementing commit re-reads that against what it touches (`docs/plain-language.md` and `doctrine/rationale.md`, prose only, no frozen test), and a plan opens if it touches more. The page's own evidence table calls the proposal's "Independent scientific check: N/A" into question, since the page publishes empirical claims; the implementation record says what was verified. Nothing else lands in this commit.
