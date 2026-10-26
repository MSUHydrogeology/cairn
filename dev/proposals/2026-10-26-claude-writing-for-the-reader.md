# Cairn Plain Language: a writing standard for what agents write to people

**Author**: Claude (Strategy)
**Status**: awaiting-review
**Review**: usual
**Plan review**: not required(one commit: one new section in the shipped collaboration doc and its Cairn copy, one pointer sentence in each `AGENTS.md`, one paragraph in `doctrine/rationale.md`, one ship test)
**Opened**: 2026-10-26
**In brief**: Give every install a one-page, versioned writing standard, Cairn Plain Language, so that what an agent writes is something a scientist can understand, check and act on.

> Rewritten before review on the Maintainer's instruction, 2026-10-26, into
> one document. The earlier drafts and their two addenda are in git history:
> `44e539ce`, `5266331c` and `cb280a29`.

## The problem

**Cairn's comprehension rule names a goal but no method.** The shipped
`AGENTS.md` makes understanding a precondition of every Decision: "Lead plain
and keep the precision beneath it; define a specialist term the first time it
carries weight; and treat *'I don't understand this yet'* as a **mandatory
pause**." `doctrine/rationale.md` grounds it (anchor 16, the comprehension
floor). Nothing says what "plain" means, so every agent decides for itself.

**The result is a recurring failure: text its reader cannot use.**

* The guide star's anchor 16 began with one: a change described as "AST
  source-motion attestation", which the Maintainer had to reverse-engineer
  before they could review it.
* On 2026-08-13 three accepted proposals (`comprehension-outlives-the-room`,
  `finding-tags-are-not-reasons`, `test-names-outlive-their-plans`) fixed the
  same failure in comments, docstrings and test names.
* On 2026-10-23 three audits of the reader-facing docs found undefined internal
  codes, coined terms and dense passages on most pages. The Maintainer judged
  the two case studies "impossible to use", and both were rewritten.

**The readers are scientists who must decide.** They are experts in their
field and often not in software. Two of their needs go unmet by general advice
on plain writing: instructions they can follow without a software background,
and reasoning that separates what was measured from what was assumed, with
uncertainty stated so they can act on it.

**Agents add a failure of their own: they sound surer than they are.**
Language models rarely express uncertainty unprompted, and when asked to, they
are overconfident: on average, 47% of their confident answers were wrong
(Zhou et al., 2024). Readers overestimate the accuracy of model answers, and
longer explanations raise their confidence without raising accuracy (Steyvers
et al., 2025). Fluent prose from an agent is therefore not neutral: it shifts
how much a scientist trusts work they have not checked.

## What already exists

Two searches on 2026-10-26, one of the web and one of the peer-reviewed
literature through the Consensus research agent, found **no standard that
gives plain-language rules for AI agents writing to scientists, covering both
instructions and scientific reasoning.** The parts exist separately:

| Source | What it covers | Licence | Use here |
| --- | --- | --- | --- |
| ISO 24495-1:2023, *Plain language* | Four principles (readers get what they need, can find it, understand it, use it) and guidelines for each | Copyright; sold | Cited by clause; no text copied |
| US Federal Plain Language Guidelines | Plain writing for government documents | Public domain | Borrowed from freely |
| ASD-STE100, Issue 9 (2025) | Controlled language for maintenance procedures | Copyright; free download | Instruction rules paraphrased; dictionary not used |
| Google developer documentation style guide | Developer documentation: active voice, conditions before instructions | CC BY 4.0 | Borrowed from |
| EFSA (2019) uncertainty guidance | Communicating uncertainty in scientific assessments | CC BY-ND 4.0 | Cited; not adapted |
| Diátaxis | Documentation types by reader need | CC BY-SA 4.0 | Cited for the idea of separate registers |

**Not found anywhere:** a rule to separate measured, assumed and expected
claims; a rule that an agent states how sure it is about its own work; and any
writing standard aimed at AI agents as the writer.

## The proposal

### 1. The standard

A new section in the shipped collaboration doc,
`templates/core/dev/agent_collaboration.md`, and in Cairn's own
`dev/agent_collaboration.md`, placed before "Surfacing judgment calls to the
Maintainer". Its full text:

> ## Cairn Plain Language
>
> *Version 1.0. Rule numbers never change; a withdrawn rule keeps its number,
> marked withdrawn. Licensed CC BY 4.0.*
>
> Every review and decision depends on the reader understanding what an agent
> wrote (`AGENTS.md`, the comprehension rule). These rules apply to anything
> an agent writes for a person: chat replies, proposals, reviews, plans,
> commit messages, documentation and error messages. They limit how text is
> built, not which words it uses: keep your field's terms, and define them.
>
> **Before you write**
>
> 1. Know who will read it and what they will do with it: decide, follow
>    steps, review, or look something up. Write for that reader and that use.
>
> **Everything**
>
> 2. Put the conclusion first, then only what the reader needs to act on it.
>    Leave out the rest, including filler and vague praise ("robust",
>    "comprehensive").
> 3. Never leave out what the reader needs to decide: failures, checks you did
>    not make, open questions, bad news.
> 4. Use one name for one thing. Do not vary names for style, do not give two
>    things the same name, and do not coin a name for something that already
>    has one.
> 5. Define a specialist term where it first matters. Keep the field's terms;
>    do not write around them.
> 6. Give an example for each abstraction.
> 7. Write short sentences, one idea each, in the active voice with the actor
>    first. Start from what the reader already knows, then add what is new. Do
>    not break the main thought with an aside. Give each paragraph one topic,
>    stated in its first sentence.
> 8. Spell out an acronym the first time, unless the reader uses it daily.
>    Unpack stacked nouns: "the record of the re-anchor ceremony", not "the
>    re-anchor ceremony record".
> 9. In anything longer than a screen, use headings that say what follows and
>    lists for parallel items. Move detail the main line does not need to its
>    own section, and say where it is. Where several readers share a
>    document, mark which part is for whom.
> 10. A figure or table supports the text, sits next to it, and has a caption
>     that states what the reader should conclude.
>
> **Instructions** (steps, runbooks, prompts to paste, install output, error
> messages)
>
> 11. One action per step, in the order the reader does them, as a command:
>     "Open…", "Run…". Put conditions and warnings before the step they apply
>     to, especially for anything that cannot be undone.
> 12. Say what the reader should see afterwards, and what to do if they see
>     something else.
> 13. An error message says what happened, why if known, and what to do next,
>     without blaming the reader.
>
> **Scientific and technical reasoning** (proposals, reviews, decisions,
> reports of results)
>
> 14. Say which claims were measured, which are assumed and which are
>     expected. Never let an assumption read as a result.
> 15. Give the number with its unit and its source, not an adjective:
>     "2.3 mm/month, from the 2025 gauge record", not "small".
> 16. State uncertainty as a number with its source: "±0.5 mm, from gauge
>     error"; "about 1 chance in 5, from the 30 runs". Do not use probability
>     words such as "likely" on their own; readers give them very different
>     meanings.
> 17. Say whether a range shows uncertainty (the value is not known) or
>     variability (the value really varies), and give no more precision than
>     the evidence supports, usually one or two significant figures.
> 18. Say how sure you are about your own work, and why, in the first person:
>     "I ran the tests and they pass"; "I did not run this on Windows"; "I am
>     not sure this handles feet; I found no test for it". Never let fluent
>     prose stand in for a check you did not make.
>
> **Checking.** A reader who cannot follow a passage says so, and the
> "I don't understand this yet" pause applies. A reviewer cites a broken rule
> by number as a finding. These rules are checked by reading, never by a
> readability score, because a score rewards the wrong edits.
>
> Sources: ISO 24495-1:2023; the US Federal Plain Language Guidelines;
> ASD-STE100 (instruction rules); the studies cited in `doctrine/rationale.md`,
> anchor 16.

### 2. A pointer in `AGENTS.md`

In the comprehension paragraph of `AGENTS.md` and `templates/core/AGENTS.md`,
after "define a specialist term the first time it carries weight;", one
sentence: "the rules for how to write it are Cairn Plain Language, in
`dev/agent_collaboration.md`". The paragraph stays in the Review section, where
`bootstrap/tests/test_comprehension_floor.py` requires it.

### 3. The reasoning in `doctrine/rationale.md`

One paragraph under anchor 16 names the sources (see *References*) and defends
the standard's two design choices: it limits structure, not vocabulary, so it
serves experts and newcomers alike (the expertise-reversal concern the anchor
already cites); and it is checked by reading, not scored (anchor 21's rule
against measuring prose).

### 4. One ship test

`bootstrap/tests/test_writing_rules_ship.py`, modelled on
`bootstrap/tests/test_stewardship_rules_ship.py`, reading a fresh install of
the smallest profile:

* the section, its version line and its group headings reach the
  installed `dev/agent_collaboration.md`;
* the pointer is in both `AGENTS.md` copies;
* no copy tells agents to use a readability score.

Proposed paths: `bootstrap/tests/test_writing_rules_ship.py`

### 5. Built so others can adopt it

The standard is written to be lifted out of Cairn unchanged:

* **A name and a version**, changed only by a Cairn proposal, with a changelog
  line per version.
* **Stable rule numbers**, so "rule 16" means the same thing in any project, a
  year later.
* **CC BY 4.0**, like the rest of Cairn's prose.
* **No Cairn-only terms in the rules.** Only the opening paragraph and
  *Checking* mention Cairn's comprehension rule and review findings; another
  project replaces those two passages and keeps rules 1 to 18 as written.

Publishing it as a standalone standard (its own page on the project site, a
block to paste into any agent's instruction file, a packaged agent skill,
worked before-and-after examples, its own DOI) is a later, separate proposal.

### What this does not do

No new module, profile axis, tool or score, and no change to the install list.
It does not build the per-reader "communication calibration" setting the guide
star parks until an outside project adopts Cairn. It makes concrete the rule
every adopter already has.

## How strong the evidence is, rule by rule

| Rules | Evidence | Strength |
| --- | --- | --- |
| 2 (only what the reader needs) and 18 (how sure you are) | Studies of how people read AI-written text: Steyvers et al. (2025); Kim et al. (2024); Zhou et al. (2024) | Direct, and about agents specifically |
| 14 to 17 (scientific reasoning) | Experiments on how people read probability words and numbers: Budescu et al. (2009, 2014); Mandel & Irwin (2020); Dhami & Mandel (2022); Wintle et al. (2019). Reviews of claims in published science: Bertizzolo et al. (2021) | Direct for 16 and 17; indirect for 14 and 15 |
| 4 to 8 (wording and sentences) | ISO 24495-1 (5.3.2 to 5.3.5); Gopen & Swan (1990); Robillard & DeLine (2011) for 6 | Professional consensus; evidence mostly from lay readers |
| 1, 3, 9, 10 (readers, content, structure, figures) | ISO 24495-1 (5.1, 5.2, 5.3.6) | Professional consensus only |
| 11 to 13 (instructions) | ISO 24495-1 (5.2.2); ASD-STE100; Google style guide; Nielsen Norman Group | Professional consensus; the weakest direct evidence of the four groups |

Three findings shape how the rules are worded:

* **Numbers, not words, for probability (rule 16).** Pairing probability words
  with numeric ranges helps, but less than it seems: in 25 samples across 24
  countries, judgments consistent with the IPCC's intended meanings rose from
  27% to 40% (Budescu et al., 2014). Words with numbers do no better than
  numbers alone (Mandel & Irwin, 2020), and pairing them can confuse readers
  and delay decisions (Dhami & Mandel, 2022).
* **Simpler text can cost credibility with readers who judge expertise.**
  Simpler AI-written summaries improved lay readers' comprehension, and made
  the scientists seem more credible but less intelligent (Markowitz, 2024).
  That is why rule 5 keeps the field's terms rather than replacing them.
* **First-person uncertainty works (rule 18).** When a model said "I'm not
  sure, but…", people relied less on its wrong answers and became more
  accurate, though over-reliance did not disappear (Kim et al., 2024).

**A known limit.** ISO 24495-1 also asks that plain-language text be evaluated
and revised with real readers over time (clause 5.4). This standard does that
once, in the trial below, and then only through the *Signals* section. A
standing evaluation is left to the later publishing proposal.

## Rationale

**Why rules about structure, not a word list.** ASD-STE100 controls vocabulary,
which suits maintenance procedures and fails scientific argument, where hedges
and domain terms are the content. Each rule here limits how text is built or
what it must state, so a hydrologist's "hydraulic conductivity" stays, and a
newcomer still gets a definition.

**Why the reasoning rules are the core.** Rules 1 to 13 restate established
advice in a form an agent can follow. Rules 14 to 18 are where scientists are
served worst today and where the evidence is strongest. An agent that writes
"the residual is small and the model is likely fine" invites the over-reliance
the comprehension floor exists to stop.

**Why in the collaboration doc.** `docs/DOCUMENTATION_PLAN.md` routes guidance
on how the team deliberates and hands work over to `agent_collaboration.md`,
with a thin pointer in `AGENTS.md`. That file ships in every install, so an
adopter's agent can read it, and `AGENTS.md`, which every agent reads every
session, grows by one sentence.

## Alternatives considered

* **Do nothing.** "Lead plain" stays a goal each agent interprets. The record
  shows the cost: three rounds of fixes in five months, the latest a rewrite of
  most reader-facing pages.
* **Adopt ASD-STE100.** It is built for procedures, controls vocabulary in a
  way that strips scientific hedges and domain terms, needs a dictionary and a
  checker, and cannot be shipped. Its instruction rules are borrowed instead.
* **Point at ISO 24495-1 or the Federal guidelines and add nothing.** Neither
  covers scientific reasoning, uncertainty or an agent's account of its own
  work, and ISO's text cannot be shipped for an agent to read.
* **A readability score or checker.** Rejected by anchor 21 and by ISO 24495-1
  itself: a score becomes the target, and the cheapest way to raise it is to
  cut the precision rules 14 to 17 protect.
* **Build the per-reader calibration setting now.** The guide star gates it on
  an outside adoption. A fixed standard is the cheaper first step, and using it
  will show whether a setting is needed.
* **Put the full rules in `AGENTS.md`.** About 40 more lines in a file every
  agent reads every session; the documentation plan routes this kind of
  guidance elsewhere, with a pointer.

## Documentation and doctrine surface

Routed by `docs/DOCUMENTATION_PLAN.md`:

* **Collaboration process (bucket 3):** the section, in
  `templates/core/dev/agent_collaboration.md` and `dev/agent_collaboration.md`.
* **Governing layer:** one pointer sentence in `templates/core/AGENTS.md` and
  `AGENTS.md`, inside the comprehension paragraph.
* **Doctrine:** one paragraph in `doctrine/rationale.md`, anchor 16.
* **Changelog:** one entry when the change lands.

The shipped collaboration doc reaches existing installs through the ordinary
three-way upgrade merge.

## Verification

### Tests

* **New:** `bootstrap/tests/test_writing_rules_ship.py` (section 4 above).
* **Existing readers, unedited, must stay green.** Eight frozen tests read
  `agent_collaboration.md`, 41 read `AGENTS.md`, and 4 read
  `doctrine/rationale.md` (counted on 2026-10-26 by file name). The change only
  adds text, which usually leaves short-phrase checks green;
  `test_comprehension_floor.py` must pass unedited. The implementer re-runs
  every reader of the three files, found by search.
* **Mutation:** delete the section from the shipped collaboration doc, then the
  pointer from each `AGENTS.md`. Each deletion must turn a named test red,
  beside an unmutated control run.

### Smoke checks

`python scripts/claim_check.py`, `python scripts/link_check.py` and
`python scripts/check_cairn.py` over every changed file;
`python scripts/quality_gate.py --sub neutrality --sub redundancy`, with
neutrality at 0 failures (the rules name no vendor); and a fresh
`solo-greenfield` install, read for the new section.

### A trial on real text

Before the change lands, the implementer rewrites two recent passages under
the rules, one review finding from an archived proposal and one step of
`docs/quickstart.md`, and shows before and after in the commit. If the rules
make either passage worse, the rules change first.

### Security and scientific checks

* **Security preflight:** N/A. No trust boundary added, moved or widened.
* **Independent scientific check:** N/A. No scientific assumption or result
  touched.

## Questions for the Maintainer

Each has a default; an unanswered question takes it.

1. **The name.** *Default:* "Cairn Plain Language". "Plain language" is the
   recognized term (ISO 24495, the US Plain Writing Act). "Calibrated" was
   considered and rejected: to hydrologists it means a model fitted to data,
   and the IPCC uses it for a fixed likelihood scale this standard does not
   adopt.
2. **Do the reasoning rules (14 to 18) apply in chat as well as in committed
   records?** *Default:* everywhere an agent writes for a person. Chat is where
   most decisions start.
3. **When to publish it for other projects.** *Default:* use it in Cairn, LHM
   and modflow_tools for about three months, then propose publishing it
   standalone, with the before-and-after examples that use has produced.
4. **The rate-limit gate.** *Default:* met by recurrence for rules 1 to 13 (see
   below). Rules 14 to 18 rest on the literature rather than on a Cairn
   incident, and the Decision should say so.

## The rate-limit gate

The gate (`doctrine/rationale.md` > "How the doctrine evolves under evidence")
allows a doctrine change when a failure recurs. Text its reader cannot use
recurred three times between the origin of anchor 16 and 2026-10-23. Each time
it was fixed where it appeared and never at its cause, which is that "lead
plain" names no method. That supports rules 1 to 13.

Rules 14 to 18 have no Cairn incident behind them. They rest on the evidence
above and on who Cairn's readers are. The Decision should record that, and may
narrow the change to rules 1 to 13 if that is not enough.

## Signals the change is wrong

* **Reviews fill with rule-number findings about style**, and changes slow
  down over wording. The rules are being policed, not used; cut them back to
  rules 2, 3 and 14 to 18.
* **Agents strip domain terms to look plain, or round numbers past what the
  evidence supports to look simple.** Rules 5 and 17 are being misread; sharpen
  them.
* **Three months after landing, the Maintainer's "I don't understand this"
  pauses are no rarer.** The rules are not changing the writing. Counted from
  the record, not scored.

## Scope delta

**Scope delta**: preserved. This is the opening contract.

## Assurance path

**Assurance path**: high-assurance. The change edits `doctrine/` and the
shipped kernel (`templates/core/AGENTS.md`,
`templates/core/dev/agent_collaboration.md`), which the template names as
mandatory high-assurance surfaces. It touches no engine, contract, trust root
or licence file, so no Security Review is owed.

## Open checks for the reviewer

* **What I read in full, and what I did not.** I read the full text of
  Budescu et al. (2009, 2014), Steyvers et al. (2025), ISO 24495-1:2023,
  Robillard & DeLine (2011) and Kuhn (2014). The other studies rest on their
  abstracts and the Consensus search summaries. I have not confirmed the full
  EFSA (2019) author list or the details of Gopen & Swan (1990).
* **Whether 18 rules are too many.** Name any that do not earn their place.

## References

* AeroSpace, Security and Defence Industries Association of Europe. (2025).
  *ASD-STE100 Simplified Technical English, Issue 9*.
  https://www.asd-europe.org/standards-specifications/simplified-technical-english
* Bertizzolo, L., Schroter, S., Dechartres, A., & Goetghebeur, E. (2021).
  Consistency of causal claims in observational studies: A review of papers
  published in a general medical journal. *BMJ Open*, 11.
  doi:10.1136/bmjopen-2020-043339
* Budescu, D. V., Broomell, S., & Por, H.-H. (2009). Improving communication
  of uncertainty in the reports of the Intergovernmental Panel on Climate
  Change. *Psychological Science*, 20(3), 299–308.
* Budescu, D. V., Por, H.-H., Broomell, S. B., & Smithson, M. (2014). The
  interpretation of IPCC probabilistic statements around the world. *Nature
  Climate Change*, 4, 508–512. doi:10.1038/nclimate2194
* Dhami, M. K., & Mandel, D. R. (2022). Communicating uncertainty using words
  and numbers. *Trends in Cognitive Sciences*. doi:10.1016/j.tics.2022.03.002
* EFSA Scientific Committee, Hart, A., Maxim, L., Siegrist, M., et al.
  (2019). Guidance on communication of uncertainty in scientific assessments.
  *EFSA Journal*, 17(1), e05520. doi:10.2903/j.efsa.2019.5520
* Gopen, G. D., & Swan, J. A. (1990). The science of scientific writing.
  *American Scientist*, 78(6), 550–558.
* Google. (n.d.). *Google developer documentation style guide*. Retrieved
  2026-10-26 from https://developers.google.com/style
* International Organization for Standardization. (2023). *ISO 24495-1:2023
  Plain language — Part 1: Governing principles and guidelines* (1st ed.).
* Kim, S. S. Y., Liao, Q. V., Vorvoreanu, M., Ballard, S., & Vaughan, J. W.
  (2024). "I'm not sure, but...": Examining the impact of large language
  models' uncertainty expression on user reliance and trust. *Proceedings of
  the 2024 ACM Conference on Fairness, Accountability, and Transparency*.
  doi:10.1145/3630106.3658941
* Kuhn, T. (2014). A survey and classification of controlled natural
  languages. *Computational Linguistics*, 40(1), 121–170.
  doi:10.1162/COLI_a_00168
* Mandel, D. R., & Irwin, D. (2020). Facilitating sender-receiver agreement in
  communicated probabilities: Is it best to use words, numbers or both?
  *Judgment and Decision Making* (preprint doi:10.31234/osf.io/hm7zu).
* Markowitz, D. M. (2024). From complexity to clarity: How AI enhances
  perceptions of scientists and the public's understanding of science. *PNAS
  Nexus*, 3. doi:10.1093/pnasnexus/pgae387
* Neusesser, T., & Sunwall, E. (2023). *Error-message guidelines*. Nielsen
  Norman Group. https://www.nngroup.com/articles/error-message-guidelines/
* Plain Language Action and Information Network. (2011). *Federal plain
  language guidelines*. https://www.plainlanguage.gov/guidelines/
* Procida, D. (n.d.). *Diátaxis*. https://diataxis.fr/
* Robillard, M. P., & DeLine, R. (2011). A field study of API learning
  obstacles. *Empirical Software Engineering*, 16, 703–732.
  doi:10.1007/s10664-010-9150-8
* Steyvers, M., Tejeda, H., Kumar, A., Belem, C., Karny, S., Hu, X.,
  Mayer, L. W., & Smyth, P. (2025). What large language models know and what
  people think they know. *Nature Machine Intelligence*, 7, 221–231.
  doi:10.1038/s42256-024-00976-7
* Wintle, B. C., Fraser, H., Wills, B. C., Nicholson, A. E., & Fidler, F.
  (2019). Verbal probabilities: Very likely to be somewhat more confusing than
  numbers. *PLoS ONE*, 14. doi:10.1371/journal.pone.0213522
* Zhou, K., Hwang, J. D., Ren, X., & Sap, M. (2024). Relying on the
  unreliable: The impact of language models' reluctance to express
  uncertainty. arXiv:2401.06730
