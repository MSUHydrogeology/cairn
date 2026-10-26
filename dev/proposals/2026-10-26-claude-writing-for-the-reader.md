# A plain-language standard for what agents write to people

**Author**: Claude (Strategy)
**Status**: awaiting-review
**Review**: usual
**Plan review**: not required(one commit: one new section in the shipped collaboration doc and its Cairn copy, one pointer sentence in each `AGENTS.md`, one paragraph in `doctrine/rationale.md`, one ship test)
**Opened**: 2026-10-26
**In brief**: Give every install a one-page standard for how agents write to people, covering instructions and scientific reasoning, so a scientist can understand and judge what an agent hands them.

## Context

**The rule exists; what it asks for does not.** The shipped `AGENTS.md` makes
comprehension a precondition of the Decision: "Lead plain and keep the
precision beneath it; define a specialist term the first time it carries
weight; and treat *'I don't understand this yet'* as a **mandatory pause**."
`doctrine/rationale.md` grounds it (anchor 16, the comprehension floor). But
nothing tells an agent what plain *is*. "Lead plain" is a goal, not a method,
and every agent fills it in differently.

**The same failure keeps recurring: text the reader cannot use.**

* The guide star's anchor 16 began with one: a change described as "AST
  source-motion attestation" that the Maintainer had to reverse-engineer
  before they could review it.
* On 2026-08-13 three accepted proposals (`comprehension-outlives-the-room`,
  `finding-tags-are-not-reasons`, `test-names-outlive-their-plans`) fixed the
  same shape in comments, docstrings and test names: text that only made
  sense to whoever was in the conversation.
* On 2026-10-23 three read-only audits of the reader-facing docs found
  undefined internal codes, coined terms and dense passages across most
  pages; the Maintainer judged the two case studies "impossible to use", and
  both were rewritten.

**What the reader is.** Cairn's adopters are scientists. They are experts in
their domain and often not in software, and they decide on work an agent
wrote. Two of their needs are not met by general plain-language advice:
instructions they can follow without a software background, and reasoning
that separates what was measured from what was assumed, with uncertainty
they can act on.

**What already exists.** A literature search (2026-10-26) found no standard
that gives plain-language rules for AI agents writing to scientists, covering
both instructions and scientific reasoning. It found good parts to build on:

* **General plain language.** ISO 24495-1:2023 (*Plain language — Part 1:
  Governing principles and guidelines*) sets four principles: readers get
  what they need, can find it, understand it, and use it. It is a paid
  standard, so Cairn cites it and does not copy it. The US Federal Plain
  Language Guidelines are public domain (the GSA repository that published
  them says so) and can be borrowed from freely.
* **Instructions.** ASD-STE100 (Issue 9, 2025) has the sharpest rules for
  procedures. It is free to download but copyrighted, so Cairn can paraphrase
  rules, not ship its dictionary. The Google developer documentation style
  guide (CC BY 4.0) covers active voice and conditions before instructions.
  Nielsen Norman Group's error-message guidance (Neusesser & Sunwall, 2023)
  covers saying what happened and what to do next.
* **Uncertainty.** Budescu, Por, Broomell & Smithson (2014, *Nature Climate
  Change* 4:508–512) surveyed 25 samples in 24 countries: lay readers pulled
  the IPCC's probability words toward 50%, and pairing the words with numeric
  ranges brought readings much closer to what was meant. EFSA's *Guidance on
  Communication of Uncertainty in Scientific Assessments* (Hart et al., 2019,
  *EFSA Journal* 17(1):e05520) says to give the number first and the word
  second, to avoid hedges such as "about", to give no more precision than the
  assessment supports, and to say whether a range shows uncertainty or
  variability. It is CC BY-ND 4.0: cite it, do not adapt its text.
* **AI explanations.** Steyvers et al. (2025, *Nature Machine Intelligence*;
  arXiv:2401.13835) found people overestimate the accuracy of language-model
  answers given default explanations, that longer explanations raise
  confidence without raising accuracy, and that explanations matched to the
  model's real confidence narrow the gap. This is the most direct evidence
  that how an agent writes changes what a reader trusts.
* **Document types.** Diátaxis (Procida; CC BY-SA 4.0) separates tutorials,
  how-to guides, reference and explanation by reader need. The two registers
  below (instructions, and reasoning) follow the same idea.
* **Not found anywhere:** a rule to separate measured, assumed and expected
  claims; a rule to say where the precise version is when precision is cut;
  any writing standard aimed at AI agents as the writer. Agent
  instruction-file conventions and spec-driven frameworks found in the search
  prescribe no writing standard for agent-to-human text.

## Proposal

**1. A new section, "Writing for the reader"**, in the shipped collaboration
doc `templates/core/dev/agent_collaboration.md`, and in Cairn's own
`dev/agent_collaboration.md`, placed before "Surfacing judgment calls to the
Maintainer". Its text:

> ## Writing for the reader
>
> Every review and decision depends on the reader understanding what an agent
> wrote (`AGENTS.md`, the comprehension rule). These rules apply to anything an
> agent writes for a person: chat replies, proposals, reviews, plans, commit
> messages, documentation and error messages. They limit structure, not
> vocabulary: keep your field's own terms, and define them.
>
> **Everything**
>
> 1. Put the conclusion first, then the reason.
> 2. Use one name for one thing. Do not vary names for style, and do not give
>    two things the same name.
> 3. Define a specialist term where it first matters. Keep the field's terms;
>    do not write around them.
> 4. Give an example for each abstraction.
> 5. Write short sentences in the active voice, with the actor first.
> 6. Spell out an acronym the first time, unless the reader uses it daily.
> 7. Unpack stacked nouns: "the record of the re-anchor ceremony for the gate
>    manifest", not "the gate-manifest re-anchor ceremony record".
> 8. Do not coin a name for something that already has one.
>
> **Instructions** (steps, runbooks, prompts to paste, install output, error
> messages)
>
> 9. One action per step, in the order the reader does them, as a command:
>    "Open…", "Run…". Put a condition before the step it applies to.
> 10. Say what the reader should see afterwards, and what to do if they see
>     something else.
> 11. An error message says what happened, why if known, and what to do next.
>
> **Scientific and technical reasoning** (proposals, reviews, decisions,
> reports of results)
>
> 12. Say which claims were measured, which are assumed and which are
>     expected. Never let an assumption read as a result.
> 13. Give the number with its unit and its source, not an adjective:
>     "2.3 mm/month, from the 2025 gauge record", not "small".
> 14. State uncertainty as a number with its source: "±0.5 mm, from gauge
>     error". If you add a word such as "likely", put the number first and the
>     word second, because readers read probability words very differently.
> 15. Say whether a range shows uncertainty (the value is not known) or
>     variability (the value really varies).
> 16. Give no more precision than the evidence supports, usually one or two
>     significant figures.
> 17. When you shorten something for the reader, say where the full version
>     is.
>
> **Checking.** A reader who cannot follow a passage says so, and the
> "I don't understand this yet" pause applies. A reviewer cites a broken rule
> by its number as a finding. These rules are checked by reading, never by a
> readability score: a score rewards the wrong edits.
>
> Sources: ISO 24495-1:2023; the US Federal Plain Language Guidelines;
> ASD-STE100 (instruction rules); EFSA (2019) and Budescu et al. (2014)
> (uncertainty); `doctrine/rationale.md` (the comprehension floor).

**2. A pointer** in the comprehension paragraph of `AGENTS.md` and
`templates/core/AGENTS.md`, after "define a specialist term the first time it
carries weight;", one sentence: "the rules for how to write it are in
`dev/agent_collaboration.md` > 'Writing for the reader'". The paragraph stays
in the Review section, where `bootstrap/tests/test_comprehension_floor.py`
requires it.

**3. One paragraph in `doctrine/rationale.md`**, under anchor 16, naming the
sources above and the two choices that need defending: the standard limits
structure, not vocabulary (so it serves experts and newcomers alike, the
expertise-reversal concern the anchor already cites); and it is checked by
reading, not scored (anchor 21's rule against measuring prose).

**4. One ship test**, modelled on
`bootstrap/tests/test_stewardship_rules_ship.py`: the section and its three
headings reach a fresh install's `dev/agent_collaboration.md`; the pointer is
in both `AGENTS.md` copies; and no copy carries a readability-score
instruction.

Proposed paths: `bootstrap/tests/test_writing_rules_ship.py`

**5. Built so others can adopt it.** The text is written so it can be lifted
out of Cairn unchanged:

* **A name and a version** at the top of the section ("Writing for the
  reader, version 1.0"), changed only by a Cairn proposal, with a changelog
  line per version.
* **Stable rule numbers.** A rule is never renumbered; a withdrawn rule keeps
  its number, marked withdrawn. Reviews, and other projects, can then cite
  "rule 13" and mean the same thing a year later.
* **CC BY 4.0**, like the rest of Cairn's prose, so anyone may copy and adapt
  it with attribution.
* **No Cairn-only terms in the rules themselves.** Only the opening sentence
  and the *Checking* paragraph mention Cairn's comprehension rule and review
  findings, so another project replaces those two passages and keeps rules 1
  to 17 as written.

Publishing it as a standalone standard (its own page on the project site, a
copy-paste block for any agent instruction file, a packaged agent skill,
worked before-and-after examples, and its own DOI) is a separate, later step:
Question 5.

**What this does not do.** No new module, no new profile axis, no tool, no
score, no change to the install list. It does not build the per-reader
"communication calibration" setting the guide star parks until an outside
adoption; it makes the rule every adopter already has concrete.

## Rationale

**Why rules about structure, not a word list.** ASD-STE100 controls
vocabulary, which suits maintenance procedures and fails scientific argument:
a scientist's hedges and domain terms are the content. Every rule above limits
how a sentence is built or what it must state, so a hydrologist's
"hydraulic conductivity" stays, and a newcomer still gets a definition.

**Why the reasoning rules are the core.** The general and instruction rules
restate well-established advice. Rules 12 to 17 are where scientists are
served badly today, and where the evidence is strongest: readers misread
probability words without numbers (Budescu et al., 2014), and fluent,
confident explanations raise trust without raising accuracy (Steyvers et al.,
2025). An agent that writes "the residual is small and the model is likely
fine" invites exactly the over-reliance the comprehension floor exists to
stop.

**Why in the collaboration doc.** `docs/DOCUMENTATION_PLAN.md` sends guidance
about how the team deliberates and hands work over to
`agent_collaboration.md`, with a thin pointer in `AGENTS.md`. That file ships
in every install, so an adopter's agent can read it locally, and it keeps the
always-loaded `AGENTS.md` from growing by more than a sentence.

## Alternatives considered

* **Do nothing.** "Lead plain" stays a goal each agent interprets. The record
  shows the cost: three rounds of fixes in five months, the latest a rewrite
  of most reader-facing pages.
* **Adopt ASD-STE100 as the default.** It is built for procedures, controls
  vocabulary in a way that strips scientific hedges and domain terms, needs a
  dictionary and a checker to verify, and cannot be shipped. Its instruction
  rules are borrowed instead.
* **Point at ISO 24495-1 or the Federal guidelines and add nothing.** Neither
  covers scientific reasoning or uncertainty, and ISO's text cannot be shipped,
  so an adopter's agent could not read it.
* **A readability score or checker.** Rejected by anchor 21 (never measure
  prose): a score becomes the target, and the cheapest way to raise it is to
  cut the precision the reasoning rules protect.
* **Build the per-reader calibration setting now.** The guide star gates it on
  an outside adoption. A fixed standard first is the cheaper step, and its
  use will show whether a setting is needed.
* **Put the full rules in `AGENTS.md`.** About 30 more lines in a file every
  agent reads every session; the documentation plan routes this kind of
  guidance to the collaboration doc with a pointer.

## Documentation / doctrine surface

Routed by `docs/DOCUMENTATION_PLAN.md`:

* **Deliberation-process guidance (bucket 3):**
  `templates/core/dev/agent_collaboration.md` and `dev/agent_collaboration.md`
  gain the section.
* **Governing layer:** `templates/core/AGENTS.md` and `AGENTS.md` gain one
  pointer sentence, inside the comprehension paragraph.
* **Doctrine:** `doctrine/rationale.md`, anchor 16, gains one paragraph.
* **Changelog:** one entry when the change lands.

The shipped collaboration doc reaches existing installs through the ordinary
three-way upgrade merge.

## Evidence / verification plan

### Tests required

* **New:** `bootstrap/tests/test_writing_rules_ship.py`, as in Proposal item 4,
  reading a real install of the smallest profile, since the installed copy is
  what an adopter's agent reads.
* **Existing readers, unedited, must stay green:** 8 frozen tests read
  `agent_collaboration.md`, 41 read `AGENTS.md`, and 4 read
  `doctrine/rationale.md` (counted 2026-10-26 by file name). The change adds
  text and removes none, which usually leaves short-phrase pins green;
  `test_comprehension_floor.py` must pass unedited. The implementer re-runs
  every reader of the three files, found by search.
* **Mutation:** delete the section from the shipped collaboration doc, and
  delete the pointer from each `AGENTS.md`; each must turn a named node of the
  new test red, beside an unmutated control.

### Examples / smoke checks

`python scripts/claim_check.py`, `python scripts/link_check.py` and
`python scripts/check_cairn.py` over every changed file;
`python scripts/quality_gate.py --sub neutrality --sub redundancy`
(neutrality must stay at 0 failures; the rules name no vendor). A fresh
`solo-greenfield` install, read for the new section.

**A trial on real text.** Before the change lands, the implementer rewrites
two recent passages under the rules (one review finding from an archived
proposal, and one step of `docs/quickstart.md`) and shows before and after in
the plan or commit. If the rules make either worse, the rules change first.

#### Security preflight — five questions, answered in writing

N/A: no trust boundary added, moved, or widened.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Questions for the Maintainer

Each has my default. An unanswered question takes it.

1. **Is the name right?** *Default:* "Writing for the reader".
2. **Do the reasoning rules (12 to 17) apply in chat too, or only in
   committed records?** *Default:* everywhere an agent writes for a person,
   chat included. Chat is where most decisions start.
3. **Number first, word second, for probabilities (rule 14)?** *Default:*
   yes, following EFSA (2019), because of the Budescu et al. (2014) evidence.
4. **The rate-limit gate.** *Default:* treated as met by recurrence (see
   below); the reasoning rules rest on the literature rather than on a Cairn
   incident, and the Decision should say so.
5. **Publish it for other projects too?** *Default:* not in this change. Build
   it so it can be lifted out (Proposal item 5), use it in Cairn and its two
   case-study projects for about three months, then open a separate proposal
   to publish it standalone, with the before-and-after examples that use has
   produced.

## The rate-limit gate

The gate (`doctrine/rationale.md` > "How the doctrine evolves under evidence")
allows a doctrine change on recurrence. The failure shape here, text its
reader cannot use, recurred three times between the origin of anchor 16 and
2026-10-23, each time fixed locally and never at its cause, which is that
"lead plain" names no method. That supports rules 1 to 11.

Rules 12 to 17 (scientific reasoning) have no Cairn incident behind them. They
rest on the evidence cited in *Context* and on Cairn's audience. The Decision
should record that, and may narrow the change to rules 1 to 11 if that is not
enough.

## Signals the change is wrong

* **Reviews fill with rule-number findings about style**, and changes slow
  down for wording. The rules are being policed rather than used; cut them to
  the reasoning rules and the conclusion-first rule.
* **Agents strip domain terms** to look plain, or round numbers past what the
  evidence supports, to look simple. Rules 3 and 16 are being misread;
  sharpen them.
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
or license file, so no Security Review is owed.

## Open checks for the reviewer

* Two sources were read only as abstracts or summaries: Budescu et al. (2014)
  and ISO 24495-1:2023. The Maintainer can supply the full texts; the
  reviewer should confirm the claims made from them here.
* Whether the 17 rules are too many. The review should name any that do not
  earn their place.

## Author's addendum -- Claude (author) -- 2026-10-26 -- a second literature check

Added before any review, so the reviewer reads it with the opening text. A
second search, through the Consensus research agent over peer-reviewed papers
(thread: https://consensus.app/search/i-am-drafting-a-short-plain-language-writing-stand/-YIk55gaRdm4VnanpzKYbA/),
confirmed the novelty finding: no standard combines plain-language rules for
AI-written text, instructions and scientific reasoning for technical readers.
It changes one rule, proposes one more, and corrects one citation.

**Rule 14 changes: the number alone, not number then word.** The opening
text followed EFSA (2019): number first, word second. Newer experimental work
finds the word adds nothing and can hurt. Words and numbers together did no
better than numbers alone, and both beat words alone (Mandel & Irwin, 2020,
*Judgment and Decision Making*, preprint doi:10.31234/osf.io/hm7zu). Pairing
probability words with numeric ranges can confuse readers and delay decisions
(Dhami & Mandel, 2022, *Trends in Cognitive Sciences*,
doi:10.1016/j.tics.2022.03.002). Bracketed numbers raised agreement with a
standard's intended meanings from 32% to 66%, still well short of full
agreement (Wintle, Fraser, Wills, Nicholson & Fidler, 2019, *PLoS ONE* 14,
doi:10.1371/journal.pone.0213522). The proposed replacement for rule 14:

> 14. State uncertainty as a number with its source: "±0.5 mm, from gauge
>     error", "about 1 chance in 5, from the 30 runs". Do not use probability
>     words ("likely", "probably") on their own; readers give them very
>     different meanings.

Question 3 changes accordingly. *Default:* the number alone.

**A proposed rule 18: say how sure you are about your own work.** Language
models rarely express uncertainty unprompted, and when prompted they are
overconfident: an average of 47% of their confident answers were wrong (Zhou,
Hwang, Ren & Sap, 2024, arXiv:2401.06730). First-person uncertainty ("I'm not
sure, but...") reduced people's reliance on wrong answers and raised their
accuracy, though it did not remove over-reliance (Kim, Liao, Vorvoreanu,
Ballard & Vaughan, 2024, *ACM FAccT*, doi:10.1145/3630106.3658941). Explanations
that match the model's real confidence narrow the gap between what people
trust and what is right (Steyvers et al., 2025). This is the one rule aimed at
the agent as the writer, and it has the most direct evidence of any:

> 18. Say how sure you are about your own work, and why, in the first person:
>     "I ran the tests and they pass", "I did not run this on Windows", "I am
>     not sure this handles feet; I found no test for it". Never let fluent
>     prose stand in for a check you did not make.

It sits under *Scientific and technical reasoning*. It also restates, for
writing, the existing doctrine to verify before asserting.

**A caveat for the general rules (1 to 8).** Simpler AI-written summaries
improved lay readers' comprehension, but made the scientists seem more
credible and *less intelligent* (Markowitz, 2024, *PNAS Nexus* 3,
doi:10.1093/pnasnexus/pgae387). The evidence for plain language comes mostly
from lay readers, not experts. This supports rule 3 (keep the field's terms)
and the anchor's expertise-reversal concern; it is not a reason to drop rules
1 to 8, but the evidence for them is weaker for expert readers than for
newcomers, and the instruction rules (9 to 11) have the weakest direct
evidence of the three groups.

**Supporting evidence for rule 12 (measured, assumed, expected).** In
observational studies in a general medical journal, 20% used causal language
inconsistently, and some authors moved from an association straight to a
recommendation without stating the assumption (Bertizzolo, Schroter,
Dechartres & Goetghebeur, 2021, *BMJ Open* 11, doi:10.1136/bmjopen-2020-043339).
Claim frameworks and the hedging literature already separate observations from
inferences (Blake, 2010, *Journal of Biomedical Informatics* 43(2):173–189;
Hyland, 1995). Neither states the measured, assumed and expected split.

**Citation correction.** Steyvers et al. is *Nature Machine Intelligence*
7:221–231, doi:10.1038/s42256-024-00976-7 (volume 7 is the 2025 volume; the
search index dates it 2024). Budescu, Por, Broomell & Smithson (2014) is
confirmed as cited: *Nature Climate Change* 4(6):508–512.

**Still unconfirmed:** the full EFSA author list; Robillard & DeLine (2011),
Fischhoff & Davis (2014), Kuhn (2014) and Gopen & Swan (1990) were not in the
second search's results and rest on the first search.
