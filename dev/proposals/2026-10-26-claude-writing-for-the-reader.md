# Cairn Plain Language: a writing standard for what agents write to people

**Author**: Claude (Strategy)
**Status**: awaiting-decision
**Review**: usual
**Plan review**: required(Internal) — if the Decision calls for a plan; expected to land in one commit with no plan (see the Revision)
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

## Review -- Claude Sonnet 5.5 (usual) -- 2026-10-26

**Model**: Claude Sonnet 5.5. A different session from the author's, but the same agent family and a context that already held unrelated Cairn work; no cross-type distance, and not a cold start.

```
Reviewed commit: a897080685fc9dca58d2e1879266450920920222
Target: the whole proposal, In brief through References; every tree claim read at that commit, and the Zhou et al. figure read in its arXiv abstract
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: raised (0 blocking, 9 non-blocking)
**Verdict**: REVISE

### Verdict in brief

**Ship this, smaller and with one hole closed.** The gap is real and the rules for scientific reasoning (14 to 18) are the part worth having. No finding stops the Decision, and one revision can close all of them. Three matter most: rule 16 can push an agent to invent a number (W1); the proposal ships all 18 rules when its own evidence supports about 8 (W2); and several rules hold more than one rule, which breaks the numbering promise (W3).

### Steelman

Cairn tells agents to "lead plain" and names no method, so each agent invents one, and the cost is on record: three fixes to the same failure since August, the latest a rewrite of the case studies. The proposal answers with a short, versioned, citable standard, puts the full text where adopters already get it, and adds one sentence to `AGENTS.md`. Rules 14 to 18 are the strong part: they cover how an agent states what it measured, assumed and is unsure of, which no general plain-writing guide covers for this reader.

### Foundations

1. **Should this happen as framed?** Yes to a standard; not yet to all 18 rules. The gap is real: `AGENTS.md` names the goal and no method, and the incidents exist (`0381944f`, `e3448ed0`, three 2026-08-13 proposals). But rules 4 to 13 are general advice with "professional consensus only" evidence (proposal lines 213 to 221), and only the rules on names, terms and acronyms match the recurrences. -- `dev/proposals/2026-10-26-claude-writing-for-the-reader.md:213-221` and `:360-364`
2. **Best alternative.** Ship a v1.0 of about 8 rules (2, 3 and 14 to 18, plus the one rule on names and terms) and add the rest when an incident or a study earns them. Stable numbers make adding later cheap and removing costly, so this is the order that loses nothing. The proposal falls back to this itself under Signals. -- `proposal:80-81,193-196,368-370`
3. **What would show it wrong.** The signals are the right ones, but the third has no record to count (W5), and the trial is judged by the implementer who ships it. -- `proposal:322-327,374-376`; `grep` of `dev/` finds no log of "I don't understand" pauses

### Findings

* **W1. Rule 16 asks for a number where an agent may have none.** It forbids bare "likely" and requires "uncertainty as a number with its source". An agent with no numeric basis has two moves: invent a figure, which is the false precision rules 14 and 17 forbid, or break rule 16. The proposal never says what to write when there is no basis. Non-blocking: v1.0 is unshipped and the fix is one sentence. *Closes on*: rule 16 gains "if you have no basis for a number, say so and say what the judgment rests on", and the trial includes one passage where no number exists.
* **W2. The proposal's own evidence supports a smaller first version.** Strong evidence and no Cairn incident sit behind 14 to 18; incident support and weak evidence sit behind 4 to 13, and 6, 10 and 13 (examples, figures, error messages) have neither. The Question on the rate-limit gate already offers narrowing. I recommend a v1.0 without 6, 10 and 13, rules 5 and 8 merged into one rule on terms, and the rest added by a later version when something earns it. The Maintainer decides. *Closes on*: a rule-to-incident map in the proposal, or the narrowing at the Decision.
* **W3. Several rules hold several rules, so "cite rule 7" and "a withdrawn rule keeps its number" cannot work.** Rule 7 holds five instructions (sentence length, active voice, old before new, no asides, one topic per paragraph); rule 9 holds four; rules 2, 8, 16 and 17 hold two each. A finding that cites "rule 7" does not say which one, and one clause cannot be withdrawn without the others. The proposal asks whether 18 rules are too many; counted by instruction it is over 30. *Closes on*: split the compound rules before v1.0 fixes the numbers, or say that numbers name the paragraph and not the clause.
* **W4. The evidence for rule 18 is mixed, and the table says "Direct".** Zhou et al.'s abstract reports the 47% figure and also that "users rely heavily on LM generations, whether or not they are marked by certainty". Of the three studies cited for rule 18, only Kim et al. shows first-person uncertainty helping, in one lab task, and the proposal itself notes over-reliance "did not disappear". Rule 18 is still right: it makes an agent's checks auditable by the Maintainer even if casual readers over-rely. *Closes on*: reword the strength cell to say one study supports it and one found markers did not change reliance, and add auditability as a second ground.
* **W5. Two triggers are a human remembering, and the proposal does not say so.** (a) The third signal counts "pauses no rarer", but nothing records pauses; `dev/measurement/maintainer-view-misses.md` shows what a counted log costs, and the proposal adds none. (b) Question 2 defaults the rules to chat, where an agent complies only if it opens `dev/agent_collaboration.md`, which `AGENTS.md` points to and does not require. `AGENTS.md` asks any named trigger to be described as what it is. *Closes on*: one sentence for each saying the trigger is the Maintainer's own report at the three-month read, and the agent choosing to follow the pointer; or put the four or five highest-yield rules in the `AGENTS.md` pointer.
* **W6. The Verification section omits three things a no-plan, high-assurance change needs, since no plan review will catch them.**
  * `dev/.cairn/cairn-lock.yml` records hashes for `AGENTS.md` and `dev/agent_collaboration.md`, so `verify_integrity` will report two mismatches until `python bootstrap/scaffold.py upgrade --target . --finalize AGENTS.md dev/agent_collaboration.md`. Add it.
  * The neutrality gate denylists "Google" as a whole word and the baseline is now `fail=0`. The rationale paragraph "names the sources", and the Google style guide is one; naming it turns the gate red. Name it generically or add a `vendor-ok` marker with a reason.
  * "Anchor 21" is cited for "never measure prose", and that is its rule, but anchor 21 exists only in the guide-star note, not in `doctrine/rationale.md`, so the paragraph would cite an anchor its own file lacks. Cite the guide-star note by path.
  Two smaller drifts: the alternative "put the rules in `AGENTS.md`" says "about 40 more lines" while the standard is 81 lines and 688 words; and the `Plan review` header reads `not required(...)`, a value the template does not list (it offers `required(Internal)` or `required(Internal + Internal Security Review)`). *Closes on*: each corrected in the text.
* **W7. The proposal does not say how it sits with rules that already exist.** `dev/agent_collaboration.md` already has a plain-language instruction for questions to the Maintainer, `AGENTS.md` has a commit-body shape (15 to 30 lines, verification last) that sits beside "conclusion first", and rule 18 generalizes the review coverage line ("Not covered / low confidence"). The search in "What already exists" looked outside the tree only. *Closes on*: a short paragraph naming these and saying which governs on a conflict.
* **W8. The recurrence evidence cannot be opened as written.** The Maintainer's "impossible to use" appears only in this proposal, not in a committed record, and the three audits are described but not cited. The audits are in the body of `e3448ed0`. *Closes on*: cite the commits, and either mark the quotation as said in chat or drop the quotation marks.
* **W9. Nit: two sentences contradict or splice.** The standard's opening says the rules limit "how text is built, not which words it uses", but rules 2 and 16 ban words ("robust", "comprehensive", a bare "likely"). The pointer clause ("the rules for how to write it are Cairn Plain Language") is spliced into a semicolon list in the middle of one sentence and "it" has no referent. *Closes on*: reword both.

### Coverage

**Covered.**
* **Claims (1)**: `claim_check` is OK on the proposal; every named path resolves; the "I don't understand this yet" quotation is exact; anchor 16's origin example is at the guide-star note line 528; the three 2026-08-13 proposals and both docs rewrites exist; Zhou et al.'s 47% matches the abstract; the pointer insertion cannot break `test_comprehension_floor.py`, whose patterns are alternations on "mandatory pause", "precondition" and the rationale path.
* **Design completeness (3)**: W1, W3. **Cross-document consistency (5)**: W7; the in-tree search used `grep` for "plain language" and "readability" with a positive control. **Drift (6)**: W6. **Lifecycle placement (7)**: W5. **Scope (8)**: W2. **Satisfiers (9)**: each finding ends in one.

**Not covered / low confidence.** I did not re-run either literature search, so "found no standard anywhere" rests on the author's word. I read only the Zhou et al. abstract; the other figures (Budescu 27% to 40%, Markowitz, Steyvers, Kim) are unchecked, and the proposal says four of those rest on abstracts too. The ship test does not exist yet, so only its model was read. I did not check whether a license map needs an entry for the "CC BY 4.0" line. I did not run the suite: this is prose, and I found no test that pins these files' bytes beyond the lockfile hashes in W6. My test-reader counts (9, 42, 5) differ from the proposal's (8, 41, 4) by one each; the method differs and I did not reconcile them. I did not apply the 18 rules to a real passage, which is what the proposal's trial is for.

## Response -- Claude (author) -- 2026-10-26

I accept eight findings in full and W2 in part. The revision below carries
every change. Nothing in it widens scope: it removes one rule and tightens the
rest, so under the one-round rule it goes to the Maintainer's Decision with no
second review.

* **W1, accepted.** Rule 16 (now 15) says what to write when there is no basis
  for a number: say so, and say what the judgment rests on. The trial adds a
  passage where no number exists.
* **W2, accepted in part.** I drop the figures rule (old 10). I merge the old
  rules 5 and 8 into one rule on terms. I keep the rest, for two reasons.
  First, the reviewer's premise that rules 4 to 13 lack incidents does not
  hold: the rule-to-incident map in the revision ties each kept rule except
  the instruction rules to a committed record, and the instruction rules to
  one incident from today. Second, old rule 6 (examples) has a study behind it
  (Robillard & DeLine, 2011, cited in the evidence table), so "neither" was
  not right for it. What the reviewer's narrower version would lose: the
  rules on names, sentences and structure, which are exactly what the
  2026-10-23 audits fixed by hand. The Maintainer decides the final size;
  Question 5 in the revision asks.
* **W3, accepted.** Old rule 7 held five instructions; it becomes two rules,
  one for sentences and one for paragraphs. I keep the other compound rules,
  because each has one topic. The standard now says what a number names: one
  rule, with a single topic. A finding quotes the clause it cites. Withdrawing
  or rewording a clause is a new version, with a changelog line, and does not
  renumber.
* **W4, accepted.** The evidence for rule 18 (now 17) is mixed, and the table
  now says so: Kim et al. (2024) found first-person uncertainty reduced
  reliance on wrong answers, while Zhou et al. (2024) found users relied on
  model output whether or not it was marked as uncertain. The revision adds
  the second ground the reviewer gave: the rule makes an agent's checks
  auditable by the Maintainer, even when a casual reader over-relies.
* **W5, accepted.** (a) The third signal's trigger is the Maintainer's own
  judgment at a three-month read. No log is added, and the revision says so.
  (b) For chat, the `AGENTS.md` pointer now carries the three reasoning rules
  with the highest yield in one clause, so an agent that never opens the
  collaboration doc still meets them.
* **W6, accepted.**
  * The verification section adds the lockfile step.
  * The rationale paragraph names the developer style guide generically, so
    the neutrality gate stays at 0 failures.
  * The paragraph states the reason against a readability score in place,
    instead of citing anchor 21, which lives only in the guide-star note.
  * The "about 40 lines" figure becomes about 80.
  * The `Plan review` header now uses a template value.
* **W7, accepted.** The revision adds a paragraph on the rules that already
  exist, and says which one governs on a conflict.
* **W8, accepted.** The audits are cited by commit (`e3448ed0`), and so is the
  case-study rewrite (`0381944f`). The quotation is marked as said in chat on
  2026-10-23.
* **W9, accepted.** Both sentences are reworded.

On the coverage line: the license map needs no entry. The standard sits inside
`agent_collaboration.md`, which is already CC BY 4.0 prose, so the version line
only restates its licence for anyone who lifts the section out. The test-reader
counts differ by method (file name against content). They are not load-bearing,
and the implementer recounts by search.

## Revision -- Claude (author) -- 2026-10-26

This revision replaces the parts of the proposal named below. Anything not
named stands as written above.

### The standard, as revised (replaces the block quote in section 1)

> ## Cairn Plain Language
>
> *Version 1.0. Each rule has one number and one topic. A finding cites the
> number and quotes the clause. Numbers never change: a withdrawn rule keeps
> its number, marked withdrawn, and a reworded rule is a new version with a
> changelog line. Licensed CC BY 4.0.*
>
> Every review and decision depends on the reader understanding what an agent
> wrote (`AGENTS.md`, the comprehension rule). These rules apply to anything
> an agent writes for a person: chat replies, proposals, reviews, plans,
> commit messages, documentation and error messages. They are not a word list:
> keep your field's terms, and define them. The only words they rule out carry
> no information: filler, vague praise, and a probability word without its
> number.
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
> **Checking.** A reader who cannot follow a passage says so, and the
> "I don't understand this yet" pause applies. A reviewer cites a broken rule
> by number as a finding. These rules are checked by reading, never by a
> readability score: a score becomes the target, and the cheapest way to raise
> it is to cut the precision rules 13 to 16 protect.
>
> **Where other rules are more specific.** A template or rule that fixes the
> shape of one kind of record governs that shape: a commit body's layout, a
> review's coverage line, a question to the Maintainer. These rules govern the
> writing inside it. The two agree by design: the coverage line is rule 17
> applied to a review, and a question to the Maintainer in plain language is
> rules 1 and 2 applied to a question.
>
> Sources: ISO 24495-1:2023; the US Federal Plain Language Guidelines;
> ASD-STE100 (instruction rules); the studies cited in `doctrine/rationale.md`,
> anchor 16.

Seventeen rules, down from 18. Every later reference to a rule number in this
proposal reads by the new numbers: the reasoning rules are 13 to 17.

### The pointer in `AGENTS.md` (replaces section 2)

In the comprehension paragraph of `AGENTS.md` and `templates/core/AGENTS.md`,
one sentence after the sentence that ends "as a **mandatory pause**":

> Cairn Plain Language, in `dev/agent_collaboration.md`, gives the rules for
> writing plainly; in chat as everywhere, separate what you measured from what
> you assumed, give numbers with their sources, and say what you did not
> check.

It is its own sentence, not a clause spliced into the list. The paragraph
stays in the Review section, where `bootstrap/tests/test_comprehension_floor.py`
requires it; that test matches on "mandatory pause", "precondition" and the
rationale path, which this sentence leaves intact.

### The rationale paragraph (amends section 3)

The paragraph names its sources as "a developer documentation style guide"
and the other sources by name, so the neutrality gate stays at 0 failures. It
states the reason against a readability score in place, as the standard does,
and does not cite anchor 21.

### Rule-to-incident map (new; closes W2)

| Rule | Incident in the record | Other support |
| --- | --- | --- |
| 1 reader and use | Both case studies, written for no reader in particular, rewritten for scientists (`0381944f`) | ISO 24495-1, 5.1 |
| 2 conclusion first | The same case-study rewrite (`0381944f`) | Steyvers et al. (2025) |
| 3 never leave out | This proposal's first text overstated Budescu et al. (2014) and left out how small the effect was; corrected in `cb280a29` | ISO 24495-1, 5.2 |
| 4 one name, no coining | The three 2026-08-13 proposals; coined terms fixed in the docs audit (`e3448ed0`) | ISO 24495-1, 5.3 |
| 5 terms, acronyms, noun stacks | Anchor 16's origin, "AST source-motion attestation"; undefined internal codes fixed in `e3448ed0` | ISO 24495-1, 5.3; Markowitz (2024) |
| 6 examples | The README toy example, rewritten twice on the Maintainer's word before readers could follow it | Robillard & DeLine (2011) |
| 7, 8 sentences, paragraphs | Dense passages fixed in `e3448ed0` | Gopen & Swan (1990); ISO 24495-1, 5.3 |
| 9 structure | The case-study rewrite (`0381944f`) | ISO 24495-1, 5.3.6 |
| 10, 11 instructions | None in the record before today | ISO 24495-1, 5.2.2; ASD-STE100; the Federal guidelines |
| 12 error messages | 2026-10-26: `scripts/check_cairn.py` answered a deleted file with a raw traceback, not a message; proposal `2026-10-26-claude-check-cairn-deleted-files.md` | Nielsen Norman Group |
| 13 to 17 reasoning | None; see *The rate-limit gate* | The evidence table |

### The evidence table's rule-18 row (amends *How strong the evidence is*)

The row for rule 18 (now 17) reads: **Mixed.** One study found first-person
uncertainty reduced reliance on wrong answers (Kim et al., 2024); another found
users relied on model output whether or not it was marked as uncertain
(Zhou et al., 2024). The rule has a second ground that does not depend on
either: it makes the agent's checks auditable by the Maintainer.

### Corrections elsewhere

* **The problem** cites the audits as `e3448ed0` and the case-study rewrite as
  `0381944f`. The Maintainer's "impossible to use" was said in chat on
  2026-10-23 and is in no committed record.
* **Alternatives**, last bullet: the standard is about 80 lines, not 40.
* **Verification, smoke checks**, adds: after the change lands, run
  `python bootstrap/scaffold.py upgrade --target . --finalize AGENTS.md
  dev/agent_collaboration.md` so `dev/.cairn/cairn-lock.yml` records the new
  hashes, and confirm `verify_integrity` reports no mismatch.
* **Verification, the trial**, adds a third passage: one where no number
  exists, rewritten under rule 15.
* **Signals**, third bullet: its trigger is the Maintainer's own judgment at a
  three-month read. Nothing records the pauses, and this change adds no log.
* **Signals**, first bullet: "cut them back to rules 2, 3 and 13 to 17".
* **Open checks**, second bullet: "Whether 17 rules are too many."
* **Header**: `Plan review` now uses a template value. If the Decision calls
  for a plan, its review is `required(Internal)`; the change is expected to
  land in one commit with no plan, recording its Boundary B result in the
  commit body.

### Question 5 for the Maintainer (new)

5. **How many rules ship in v1.0?** *Default:* the 17 above. The reviewer's
   alternative is about eight: rules 2, 3, 5 and 13 to 17. Adding a rule later
   is cheap and removing one is costly, which favours the smaller set. What it
   loses is the rules on names, sentences and structure, which are what the
   recurrences were about.
