# Cairn Plain Language: Literature Synthesis, Generalizability, and the Boundary with `assai`

**Author**: Antigravity (Strategy)
**Model**: Gemini 3.1 Pro
**Date**: 2026-10-27
**Status**: settled
**Type**: comparative-research
**Surfaces this would feed**: `docs/plain-language.md`, `doctrine/rationale.md` (Anchor 16), `dev/agent_collaboration.md`, and `assai`'s direct adoption of Cairn Plain Language alongside its own paper and journal templates

## In brief

1. **The boundary that keeps Cairn Plain Language generalizable:** Cairn Plain Language governs **how an agent writes prose and states claims** so a reader can understand, check, and act on them. It does **not** govern what an artifact must contain or prove. As its closing paragraph states (*"Where other rules are more specific"*), a template or protocol fixes the shape and methodological requirements of a specific record—whether that is a Cairn commit body, an `assai` internal paper, a `crux` notebook entry, or an IMRaD journal manuscript—and Cairn Plain Language governs the writing inside that shape.
2. **Because of that boundary, Cairn Plain Language 1.0 is already highly generalizable to `assai` and scientific writing.** What `assai` requires beyond Cairn Plain Language—the three-level contribution hierarchy (pattern vs. model mechanism vs. world mechanism), pre-registration locks (`exploratory` vs. `pre-specified`), positive controls on apparatus sensitivity, and claim-graph dependency rules—belongs in **`assai`'s paper and review templates**, just as Cairn's *Independent scientific check* lives in Cairn's proposal template rather than in the writing standard.
3. **Does `doctrine/rationale.md` or `docs/plain-language.md` show the whole literature review?** **No.** [`doctrine/rationale.md`](../../doctrine/rationale.md) compresses the grounding into one 33-line paragraph under Anchor 16 (6 empirical studies and 4 standards), and [`docs/plain-language.md`](../../docs/plain-language.md) names only 4 studies by author-year with no bibliography and no copy of the 17 rules. The full 21-source literature review, the rule-by-rule evidence table, the ISO 24495-1:2023 clause map, and the full-text verification audit sit buried in [`dev/proposals/archive/2026-10-26-claude-writing-for-the-reader.md`](../proposals/archive/2026-10-26-claude-writing-for-the-reader.md) and its pre-rewrite commits (`5266331c`, `cb280a29`).
4. **What the AI-scientific-writing literature adds—and the only genuine gaps to close for `assai`:** Expanding the literature review to empirical studies of LLM-assisted scientific writing (Kobak et al., 2025; Liang et al., 2025; Walters & Wilder, 2023; Messeri & Crockett, 2024; Lu et al., 2024; Bertizzolo et al., 2021) reveals **two surface/packaging gaps** in Cairn's docs and **three small prose-level refinements** inside the writing rules themselves:
   * **Packaging & doctrine gaps (in `docs/plain-language.md` and `doctrine/rationale.md`):**
     1. [`docs/plain-language.md`](../../docs/plain-language.md) does not actually print the 17 rules or provide a project-neutral copy-paste block that `assai` can drop into its lab and journal prompts.
     2. Neither [`docs/plain-language.md`](../../docs/plain-language.md) nor [`doctrine/rationale.md`](../../doctrine/rationale.md) shows the full rule-by-rule evidence table or the 30-source bibliography.
   * **Writing-level refinements (optional v1.1 tightening vs. keeping v1.0 as-is):**
     1. *Rule 2 (AI promotional vocabulary):* Kobak et al. (2025) and Liang et al. (2025) show LLMs flood scientific prose with promotional style words (*"delve"*, *"underscore"*, *"showcase"*, *"intricate"*, *"pivotal"*, *"novel"*, *"compelling"*), which inflate perceived quality during review ("paper laundering"; Lu et al., 2024). Rule 2 already bans *"filler and vague praise ('robust', 'comprehensive')"*; naming promotional verbs/adjectives sharpens the existing rule.
     2. *Rule 13 (Simulated vs. observed):* In simulation science, agents routinely call a model run's output "measured". Clarifying that Rule 13 distinguishes **observed/measured, simulated, assumed, and expected** prevents model output from reading as field measurement.
     3. *Rule 14 & Rule 17 (Citation reading honesty):* Walters & Wilder (2023) found 18%–55% fabricated citations and 24%–43% citation errors in LLM scientific writing. Applying Rule 14 (give the source) and Rule 17 (say what you checked) to citations means: never cite a source you have not checked, and say when you read only an abstract or secondary summary rather than the primary text.

---

## Method

* **Repository & git-history audit (measured).** Read the shipped standard in [`dev/agent_collaboration.md`](../agent_collaboration.md) (lines 201–292), the doctrine grounding in [`doctrine/rationale.md`](../../doctrine/rationale.md) (lines 189–317), the public guide in [`docs/plain-language.md`](../../docs/plain-language.md) (lines 1–109), the archived proposal [`dev/proposals/archive/2026-10-26-claude-writing-for-the-reader.md`](../proposals/archive/2026-10-26-claude-writing-for-the-reader.md), its two pre-rewrite addenda (`5266331c`, `cb280a29`), and the `assai` design notes in Cairn's git history (`6ea4d4d7^`).
* **Literature expansion on AI writing of scientific papers (searched 2026-10-27).** Surveyed peer-reviewed empirical studies and editorial standards on LLM-assisted scientific writing: corpus-scale vocabulary shifts (Kobak et al., 2025; Liang et al., 2025), citation fabrication and errors (Walters & Wilder, 2023), autonomous manuscript generation and review failure modes (Lu et al., 2024), cognitive illusions of understanding in AI-assisted science (Messeri & Crockett, 2024), causal spin and scientific hedging (Bertizzolo et al., 2021; Blake, 2010; Hyland, 1998), and authorship/accountability guidelines (ICMJE, 2024; COPE, 2023).
* **Verification status of cited literature (Rule 17).** Six sources were verified against full text in commit `cb280a29` (Budescu et al. 2009, 2014; Steyvers et al. 2025; ISO 24495-1:2023; Robillard & DeLine 2011; Kuhn 2014). The remaining 15 sources from the 2026-10-26 proposal and the 9 new sources on AI scientific paper writing were checked via published abstracts, DOIs, and bibliographic indexes during this session, not full-text PDFs.

---

## Part 1: The Division of Labor — Writing Standard vs. Artifact Template

A writing standard fails if it tries to swallow domain methodology or document templates. Cairn Plain Language 1.0 already states the right architectural boundary in its final paragraph ([`dev/agent_collaboration.md`](../agent_collaboration.md), lines 283–288):

> **Where other rules are more specific.** A template or rule that fixes the shape of one kind of record governs that shape: a commit body's layout, a review's coverage line, a question to the Maintainer. These rules govern the writing inside it.

Applying that boundary across Cairn, `assai`, and journal manuscripts separates **what Cairn Plain Language owns** from **what each artifact's template or protocol owns**:

| Dimension | Owned by **Cairn Plain Language** (the shared writing standard) | Owned by **Cairn's proposal / plan templates** (software methodology) | Owned by **`assai`'s paper, `crux`, and journal templates** (autonomous research runtime) | Owned by **external journal / publisher guidelines** (human-authored manuscripts) |
| --- | --- | --- | --- | --- |
| **Structure & order** | Conclusion first by default (Rule 2); one topic per paragraph, old-before-new (Rule 8); informative headings and lists (Rule 9) | Proposal sections (`Context`, `Proposal`, `Alternatives`, `Verification`); commit-body layout (verification block at the foot) | Short internal paper structure (question, contribution, method, executable evidence, claims, limitations, next test); lead-brief card layout | IMRaD section order (Abstract, Introduction, Methods, Results, Discussion, Data Availability) |
| **Vocabulary & tone** | One name per thing (Rule 4); keep and define domain terms, unpack noun stacks (Rule 5); active voice (Rule 7); no filler or promotional praise (Rule 2) | Neutrality gate (no vendor leakage in shipped templates); status words (`awaiting-review`, etc.) | Claim-standing vocabulary (`exploratory`, `reproduced`, `challenged`, `independently supported`) | Journal-specific nomenclature, unit systems (SI), and style sheet |
| **Scientific & technical claims** | Separate measured/simulated, assumed, and expected (Rule 13); give numbers with units and sources, not adjectives (Rule 14) | **Independent scientific check**: name one check with an independent basis and record a purposeful failing run + positive control | **Three-level contribution rule**: distinguish (1) pattern, (2) model mechanism, and (3) world mechanism; **pre-run lock** (`pre-specified` vs. `exploratory`); apparatus positive control at the target effect size | Study-design reporting checklists (e.g., CONSORT, PRISMA, Agu/EGU model-evaluation standards) |
| **Uncertainty & precision** | State uncertainty as a number with its source, or give the non-numeric basis; no bare `"likely"` (Rule 15); distinguish uncertainty from variability; match significant figures to evidence (Rule 16) | Falsification ledger in code review; Boundary B verification record | Claim dependency graph: record shared datasets, forcing, calibration targets, and lineage when evaluating whether two runs are independent | Statistical reporting requirements (confidence/credible intervals, exact $p$-values or Bayes factors, ensemble spread) |
| **Epistemic accountability & attribution** | Say what you checked and did not check in the first person (`"I ran X; I did not check Y"`, Rule 17); never omit failures or bad news (Rule 3) | Co-authored-by trailers; self-committed reviews with `Reviewed commit:` and two-part coverage line (`Covered` / `Not covered`) | Lab, Replicator, and Journal Reviewer attribution on every paper and run certificate | **Human authorship accountability** (ICMJE / COPE: AI cannot be an author; `"we"` means human authors; mandatory AI-use disclosure; agent provides a separate verification ledger to human co-authors) |

### Why this division of labor matters

Because `assai`'s paper template and `crux` notebook contract own the **research-protocol requirements** (pattern vs. model mechanism vs. world mechanism, pre-registration locks, positive controls, and claim-graph lineage), **Cairn Plain Language does not need to bloat into a scientific-method treatise to serve `assai`.** Its 17 rules stay short (~80 lines), universal, and focused on how any agent writes a sentence, a paragraph, a number, an uncertainty range, or a statement of what it checked.

---

## Part 2: Audit of `doctrine/rationale.md` and `docs/plain-language.md`

### Where the literature review currently lives vs. where readers look

While the 17 rules themselves are lean and portable, Cairn's **published documentation of the standard and its literature review** is currently split in the wrong places:

| File | Role | What it currently contains | Gap |
| --- | --- | --- | --- |
| [`doctrine/rationale.md`](../../doctrine/rationale.md) (Anchor 16, lines 189–317) | Cairn's published methodology rationale (cited by `AGENTS.md` and external projects) | 5 comprehension-floor citations (Miller 2019; Kalyuga 2007; Clark & Brennan 1991; appropriate-reliance preprints; Naur 1985) + **one 33-line paragraph** on Cairn Plain Language citing 6 empirical papers (Budescu et al. 2009, 2014; Mandel & Irwin 2020; Steyvers et al. 2025; Zhou et al. 2024; Kim et al. 2024; Markowitz 2024) | Omits 10 of the 21 sources from the proposal/addenda; has no rule-by-rule evidence table; does not distinguish rules backed by direct experiments from rules backed by professional consensus; omits the AI-scientific-writing literature |
| [`docs/plain-language.md`](../../docs/plain-language.md) (lines 1–109) | Public, adopter-facing guide to Cairn Plain Language | A 4-row summary table of the rules (`## What it asks`) and a 22-line `## What backs it` section naming 4 studies by author and year only (Zhou et al. 2024; Budescu et al. 2014; Mandel & Irwin 2020; Kim et al. 2024) | **Does not print the 17 rules** (tells the reader to open `dev/agent_collaboration.md`); **contains no bibliography** (no titles, journals, or DOIs); and points the reader to `dev/proposals/archive/` for the evidence |
| [`dev/proposals/archive/2026-10-26-claude-writing-for-the-reader.md`](../proposals/archive/2026-10-26-claude-writing-for-the-reader.md) + commits `5266331c`, `cb280a29` | Internal archived deliberation record | The 19-source reference list, the rule-by-rule evidence table, the rule-to-incident map, the ISO 24495-1 clause map, and the full-text audit (plus Blake 2010 and Hyland 1995 in `5266331c`) | Buried in `dev/proposals/archive/`, which is an internal history folder rather than a reader-facing reference |

### The complete literature review brought together (all 30 sources)

Combining the 21 sources from the 2026-10-26 proposal and its pre-rewrite addenda (`5266331c`, `cb280a29`) with 9 peer-reviewed studies and editorial standards on AI writing of scientific papers gives the complete evidentiary foundation for Cairn Plain Language:

| Domain | Rules supported | Key sources | Quantitative / empirical findings | Evidence strength & check status |
| --- | --- | --- | --- | --- |
| **1. Reader-tailored explanation & expertise reversal** | **Rule 1** (know the reader and their task); **Rule 5** (keep domain terms, define where needed) | Miller (2019); Kalyuga (2007); Clark & Brennan (1991); ISO 24495-1:2023 (5.1, 5.3.2c); Kuhn (2014); Markowitz (2024) | Explanations that spell out novice background *reduce* expert performance by adding cognitive load (Kalyuga, 2007). Controlled vocabularies (such as ASD-STE100's dictionary) fail in science because specialist terms carry irreducibly precise meaning (Kuhn, 2014). Replacing scientific terms with simple words improves lay comprehension but makes scientists appear *less intelligent* to evaluators (Markowitz, 2024). | **Strong experimental & theoretical grounding** (ISO 24495-1 & Kuhn 2014 read in full; Markowitz 2024 from abstract) |
| **2. Length, fluency, excess vocabulary, and illusions of understanding in AI prose** | **Rule 2** (conclusion first; no filler or promotional praise); **Rule 3** (never omit failures or unchecked items) | Steyvers et al. (2025); Messeri & Crockett (2024); Kobak et al. (2025); Liang et al. (2025); Lu et al. (2024); ISO 24495-1:2023 (5.2.2a) | Readers overestimate default LLM accuracy, and **longer explanations raise human confidence without raising accuracy** (Steyvers et al., 2025). Polished AI synthesis induces *illusions of explanatory depth* and *illusions of exploratory breadth* (Messeri & Crockett, 2024). Across 15M+ PubMed abstracts (Kobak et al., 2025) and 1.1M+ preprints/papers (Liang et al., 2025), LLMs inject measurable spikes of promotional filler (*"delve"*, *"underscore"*, *"showcase"*, *"intricate"*, *"pivotal"*, *"testament"*), affecting ≥10%–22% of 2024 papers and enabling "paper laundering" where style masks weak evidence in review (Lu et al., 2024). | **Direct experimental & corpus-scale empirical evidence** (Steyvers et al. 2025 & ISO 24495-1 read in full; Kobak 2025, Liang 2025, Messeri & Crockett 2024, Lu 2024 from abstracts/metadata) |
| **3. Terminology stability, examples, and reader-expectation structure** | **Rule 4** (one name per thing); **Rule 6** (examples); **Rules 7–9** (short active sentences; one topic per paragraph, old-before-new; headings & lists) | Robillard & DeLine (2011); Gopen & Swan (1990); ISO 24495-1:2023 (5.3.2e, 5.3.2g, 5.3.3c, 5.3.4a, 5.3.5, 5.3.6); Procida (Diátaxis) | In a field study of >440 developers, missing examples and unclear intent were the top barriers to using technical docs (Robillard & DeLine, 2011). Scientific readers parse complex claims accurately when the actor occupies the grammatical subject ("topic position"), old context precedes new content, and new emphasis sits at the end ("stress position"; Gopen & Swan, 1990). | **Direct field study (Rule 6) + rhetorical/professional consensus (Rules 4, 7–9)** (Robillard & DeLine 2011 & ISO 24495-1 read in full; Gopen & Swan 1990 abstract/secondary) |
| **4. Procedural instructions & error messages** | **Rules 10–12** (one action per step in time order; warnings before irreversible actions; state expected output; constructive error messages) | ISO 24495-1:2023 (5.2.2c, 5.2.2e); ASD-STE100 Issue 9 (2025); Plain Language Guidelines (2011); Neusesser & Sunwall (2023) | Putting conditions and irreversible-action warnings *before* the command verb prevents execution errors before the reader acts. | **Professional consensus** (weakest controlled experimental base; ISO 24495-1 read in full) |
| **5. Claim taxonomy, causal spin, and citation integrity** | **Rules 13 & 14** (separate measured / assumed / expected; give numbers with units and sources) | Bertizzolo et al. (2021); Blake (2010); Hyland (1998); Walters & Wilder (2023) | In *BMJ* observational studies, **20% used causal language inconsistently** between Results and Abstract/Discussion, jumping from association to recommendation without stating assumptions (Bertizzolo et al., 2021). Claim frameworks separate explicit observations from correlations and implicit claims (Blake, 2010). In LLM-generated literature reviews across 42 topics, **55% (GPT-3.5) and 18% (GPT-4) of citations were fabricated**, and 24%–43% of real citations had bibliographic errors (Walters & Wilder, 2023). | **Direct empirical audits of scientific papers & LLM outputs** (abstracts/metadata) |
| **6. Quantified uncertainty vs. verbal probabilities** | **Rules 15 & 16** (uncertainty as a number with its source, or explicit non-numeric basis; no bare probability words; uncertainty vs. variability; honest significant figures) | Budescu et al. (2009, 2014); Mandel & Irwin (2020); Dhami & Mandel (2022); Wintle et al. (2019); EFSA (2019); Fischhoff & Davis (2014) | Across 25 samples in 24 countries, readers regressed IPCC verbal probabilities (*"likely"*, *"very likely"*) toward 50%; pairing words with numeric ranges raised IPCC-consistent interpretations only from **27% to 40%** and range overlap from **18.5% to 33.6%** (Budescu et al., 2014; Budescu et al. 2009 found inconsistent readings fell from 53% to 41% across 223 participants). Words + numbers perform no better than numbers alone (Mandel & Irwin, 2020) and can confuse readers and slow decisions (Dhami & Mandel, 2022). Bracketed numbers raised agreement from **32% to 66%** in Wintle et al. (2019). | **Strong, replicated multi-country experimental evidence** (Budescu et al. 2009, 2014 read in full; others from abstracts) |
| **7. First-person agent epistemic disclosure & human authorship accountability** | **Rule 17** (state how sure you are about your own work and what you checked/did not check in the first person) | Zhou et al. (2024); Kim et al. (2024); Steyvers et al. (2025); ICMJE (2024); COPE (2023) | LLMs rarely express uncertainty unprompted and are **wrong on 47% of answers marked confident**; third-person certainty markers do not reduce human over-reliance (Zhou et al., 2024). First-person uncertainty (*"I'm not sure, but..."*) reduced reliance on wrong LLM answers in a controlled study, though over-reliance remained (Kim et al., 2024). In published science, AI cannot be an author and humans bear 100% accountability for accuracy (ICMJE, 2024; COPE, 2023). | **Direct experimental evidence on human-LLM interaction + universal editorial policy** (Steyvers et al. 2025 read in full; Zhou 2024 & Kim 2024 from abstracts) |

---

## Part 3: The Specific Gaps to Close for Direct Use in `assai`

Keeping the boundary clear—**Cairn Plain Language governs how prose is written; `assai`'s templates govern what an `assai` paper or review must contain**—leaves **five concrete, bounded gaps** to make Cairn Plain Language ready for `assai`:

### 1. Packaging & Documentation Gaps (No change to the 17 rules required)

* **Gap P1 — `docs/plain-language.md` does not include the full rules or a drop-in prompt block.**
  * *Current state:* [`docs/plain-language.md`](../../docs/plain-language.md) only summarizes the 17 rules in a 4-row table and tells readers to open `dev/agent_collaboration.md`. Inside `dev/agent_collaboration.md`, the opening paragraph and the closing *Checking* / *Where other rules are more specific* paragraphs reference Cairn's `AGENTS.md` and commit bodies.
  * *Fix:* Put the **complete, verbatim 17 rules** directly into [`docs/plain-language.md`](../../docs/plain-language.md) inside a **self-contained, project-neutral block** (where the opening and closing lines work in any project—whether `assai` lab prompts, `assai` journal prompts, LHM, or an outside adopter).
* **Gap P2 — The literature review and bibliography are trapped in `dev/proposals/archive/`.**
  * *Current state:* [`docs/plain-language.md`](../../docs/plain-language.md) has no bibliography and only 4 author-year citations; [`doctrine/rationale.md`](../../doctrine/rationale.md) has a single 33-line paragraph.
  * *Fix:* Add the **rule-by-rule evidence table** and the **full bibliography with DOIs** to [`docs/plain-language.md`](../../docs/plain-language.md), and update Anchor 16 in [`doctrine/rationale.md`](../../doctrine/rationale.md) to include the AI-scientific-writing evidence (Kobak et al., 2025; Liang et al., 2025; Walters & Wilder, 2023; Messeri & Crockett, 2024; Bertizzolo et al., 2021) with a pointer to `docs/plain-language.md`.

### 2. Optional Prose-Level Refinements to the 17 Rules (If we want a v1.01 / v1.1 tightening before `assai` copies them)

Even when `assai`'s paper template owns the scientific-method rules, three tiny wording gaps inside Cairn Plain Language 1.0's existing 17 rules show up when an AI writes scientific prose:

* **Gap R1 — Promotional / "excess vocabulary" in Rule 2:**
  * *Current Rule 2:* `"2. Put the conclusion first, then only what the reader needs to act on it. Leave out filler and vague praise ('robust', 'comprehensive')."`
  * *Why it matters for `assai`:* Kobak et al. (2025) and Liang et al. (2025) show LLMs systematically inject promotional verbs and adjectives (*"delve"*, *"underscore"*, *"showcase"*, *"intricate"*, *"pivotal"*, *"novel"*, *"compelling"*) that inflate peer-review scores without adding content ("paper laundering"; Lu et al., 2024).
  * *Minimal tightening:* `"2. Put the conclusion first, then only what the reader needs to act on it. Leave out filler, promotional claims and vague praise ('robust', 'comprehensive', 'novel', 'compelling', 'pivotal', 'underscores', 'showcases', 'delves into')."`
* **Gap R2 — Simulated vs. measured in Rule 13:**
  * *Current Rule 13:* `"13. Say which claims were measured, which are assumed and which are expected. Never let an assumption read as a result."`
  * *Why it matters for `assai`:* In hydrology and simulation science, an agent that runs a model script routinely calls the model's output "measured", blurring field observations with simulation output.
  * *Minimal tightening:* `"13. Say which claims were measured (or simulated), which are assumed and which are expected. Never let an assumption read as a result, or a simulation read as an observation."`
* **Gap R3 — Citation verification honesty in Rule 14 / Rule 17:**
  * *Current Rule 14:* `"14. Give the number with its unit and its source, not an adjective: '2.3 mm/month, from the 2025 gauge record', not 'small'."`
  * *Current Rule 17:* `"17. Say how sure you are about your own work, and why, in the first person: 'I ran the tests and they pass'; 'I did not run this on Windows'; 'I am not sure this handles feet; I found no test for it'. Never let fluent prose stand in for a check you did not make."`
  * *Why it matters for `assai` and paper writing:* Walters & Wilder (2023) show LLMs fabricate 18%–55% of citations or cite full papers when they only saw an abstract or title. Adding `"I read only the abstract of X"` to Rule 17's examples (or a clause in Rule 14/17) closes citation laundering without adding a 18th rule.

---

## Options & Recommendation

1. **Immediate, zero-churn improvement (Packaging & Doctrine — Gaps P1 & P2):**
   * Expand [`docs/plain-language.md`](../../docs/plain-language.md) so it carries:
     1. The **full, copy-pasteable text of Cairn Plain Language** (with a clean, project-neutral wrapper block that `assai` can drop straight into its prompts);
     2. How the **"Where other rules are more specific"** boundary works for software repos, `assai` research labs, and human-authored journal papers;
     3. The **complete rule-by-rule evidence table** and **full 30-source bibliography** (including the AI-scientific-writing literature).
   * Expand Anchor 16 in [`doctrine/rationale.md`](../../doctrine/rationale.md) by one short paragraph summarizing the AI-scientific-writing literature (Kobak et al., 2025; Liang et al., 2025; Walters & Wilder, 2023; Messeri & Crockett, 2024; Bertizzolo et al., 2021).
2. **Optional rule-text tightening (Gaps R1, R2, R3):**
   * Either fold the three small prose tightenings (Rule 2 promotional words, Rule 13 simulated vs. observed, Rule 17 `"I read only the abstract"`) into the 17 rules now while v1.0 is still unreleased on `0.5-dev`, **or** keep the v1.0 text in `dev/agent_collaboration.md` untouched and note those three points in [`docs/plain-language.md`](../../docs/plain-language.md) under "Using it for scientific papers and research labs".

---

## Consolidated References (Plain Language + AI Scientific Writing)

### Plain language, technical documentation, and controlled languages
* AeroSpace, Security and Defence Industries Association of Europe. (2025). *ASD-STE100 Simplified Technical English, Issue 9*. https://www.asd-europe.org/standards-specifications/simplified-technical-english
* Gopen, G. D., & Swan, J. A. (1990). The science of scientific writing. *American Scientist*, 78(6), 550–558.
* International Organization for Standardization. (2023). *ISO 24495-1:2023 Plain language — Part 1: Governing principles and guidelines* (1st ed.).
* Kuhn, T. (2014). A survey and classification of controlled natural languages. *Computational Linguistics*, 40(1), 121–170. doi:10.1162/COLI_a_00168
* Markowitz, D. M. (2024). From complexity to clarity: How AI enhances perceptions of scientists and the public's understanding of science. *PNAS Nexus*, 3(9), pgae387. doi:10.1093/pnasnexus/pgae387
* Neusesser, T., & Sunwall, E. (2023). *Error-message guidelines*. Nielsen Norman Group. https://www.nngroup.com/articles/error-message-guidelines/
* Plain Language Action and Information Network. (2011). *Federal plain language guidelines*. https://www.plainlanguage.gov/guidelines/
* Procida, D. (n.d.). *Diátaxis documentation framework*. https://diataxis.fr/
* Robillard, M. P., & DeLine, R. (2011). A field study of API learning obstacles. *Empirical Software Engineering*, 16(6), 703–732. doi:10.1007/s10664-010-9150-8

### Uncertainty communication, causal claims, and scientific hedging
* Bertizzolo, L., Schroter, S., Dechartres, A., & Goetghebeur, E. (2021). Consistency of causal claims in observational studies: A review of papers published in a general medical journal. *BMJ Open*, 11(5), e043339. doi:10.1136/bmjopen-2020-043339
* Blake, C. (2010). Beyond genes, proteins, and abstracts: Identifying scientific claims from full-text biomedical articles. *Journal of Biomedical Informatics*, 43(2), 173–189. doi:10.1016/j.jbi.2009.11.001
* Budescu, D. V., Broomell, S., & Por, H.-H. (2009). Improving communication of uncertainty in the reports of the Intergovernmental Panel on Climate Change. *Psychological Science*, 20(3), 299–308. doi:10.1111/j.1467-9280.2009.02284.x
* Budescu, D. V., Por, H.-H., Broomell, S. B., & Smithson, M. (2014). The interpretation of IPCC probabilistic statements around the world. *Nature Climate Change*, 4(6), 508–512. doi:10.1038/nclimate2194
* Dhami, M. K., & Mandel, D. R. (2022). Communicating uncertainty using words and numbers. *Trends in Cognitive Sciences*, 26(6), 514–526. doi:10.1016/j.tics.2022.03.002
* EFSA Scientific Committee, Hart, A., Maxim, L., Siegrist, M., Von Goetz, N., da Cruz, C., Merten, C., Mosbach-Schulz, O., Lahaniatis, M., Smith, A., & Hardy, A. (2019). Guidance on communication of uncertainty in scientific assessments. *EFSA Journal*, 17(1), e05520. doi:10.2903/j.efsa.2019.5520
* Fischhoff, B., & Davis, A. L. (2014). Communicating scientific uncertainty. *Proceedings of the National Academy of Sciences*, 111(Suppl. 4), 13664–13671. doi:10.1073/pnas.1317504111
* Hyland, K. (1998). *Hedging in Scientific Research Articles*. John Benjamins Publishing Company. doi:10.1075/pbns.54
* Mandel, D. R., & Irwin, D. (2020). Facilitating sender-receiver agreement in communicated probabilities: Is it best to use words, numbers or both? *Judgment and Decision Making*, 16(2), 363–393 (preprint doi:10.31234/osf.io/hm7zu).
* Wintle, B. C., Fraser, H., Wills, B. C., Nicholson, A. E., & Fidler, F. (2019). Verbal probabilities: Very likely to be somewhat more confusing than numbers. *PLOS ONE*, 14(4), e0213522. doi:10.1371/journal.pone.0213522

### Human-AI reliance, explanation calibration, and AI writing of scientific papers
* Committee on Publication Ethics (COPE). (2023). *Authorship and AI tools — COPE position statement*. https://publicationethics.org/cope-position-statements/ai-author
* International Committee of Medical Journal Editors (ICMJE). (2024). *Recommendations for the Conduct, Reporting, Editing, and Publication of Scholarly Work in Medical Journals* (Section II.A.4, Artificial Intelligence-Assisted Technology). https://www.icmje.org/
* Kim, S. S. Y., Liao, Q. V., Vorvoreanu, M., Ballard, S., & Vaughan, J. W. (2024). "I'm not sure, but...": Examining the impact of large language models' uncertainty expression on user reliance and trust. *Proceedings of the 2024 ACM Conference on Fairness, Accountability, and Transparency (FAccT '24)*, 822–835. doi:10.1145/3630106.3658941
* Kobak, D., González-Márquez, R., Horvát, E.-Á., & Lause, J. (2025). Delving into LLM-assisted writing in biomedical publications through excess vocabulary. *Science Advances*, 11(27), eadt3813 (preprint arXiv:2406.07016). doi:10.1126/sciadv.adt3813
* Liang, W., Zhang, Y., Wu, Z., Lepp, H., Ji, W., Zhao, X., Cao, H., Liu, S., He, S., Huang, Z., Yang, D., Potts, C., Manning, C. D., & Zou, J. (2025). Mapping the increasing use of LLMs in scientific papers. *Nature Human Behaviour* (preprint arXiv:2404.01268). doi:10.1038/s41562-025-02273-8
* Lu, C., Lu, C., Lange, R. T., Foerster, J., Clune, J., & Ha, D. (2024). The AI Scientist: Towards fully automated open-ended scientific discovery. arXiv:2408.06292. doi:10.48550/arXiv.2408.06292
* Messeri, L., & Crockett, M. J. (2024). Artificial intelligence and illusions of understanding in scientific research. *Nature*, 627, 49–58. doi:10.1038/s41586-024-07146-0
* Steyvers, M., Tejeda, H., Kumar, A., Belem, C., Karny, S., Hu, X., Mayer, L. W., & Smyth, P. (2025). What large language models know and what people think they know. *Nature Machine Intelligence*, 7, 221–231. doi:10.1038/s42256-024-00976-7
* Walters, W. H., & Wilder, E. I. (2023). Fabrication and errors in the bibliographic citations generated by ChatGPT. *Scientific Reports*, 13, 14045. doi:10.1038/s41598-023-41032-5
* Zhou, K., Hwang, J. D., Ren, X., & Sap, M. (2024). Relying on the unreliable: The impact of language models' reluctance to express uncertainty. arXiv:2401.06730. doi:10.48550/arXiv.2401.06730
