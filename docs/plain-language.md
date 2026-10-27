# Cairn Plain Language

**Cairn Plain Language is a one-page writing standard for what an AI agent
writes to a person.** It has 17 numbered rules and ships in every Cairn
install. Its aim is that a scientist can understand what the agent wrote,
check it, and act on it. This is version 1.0.

This page has three jobs: it shows the rules and their evidence, it gives a
block you can paste into your own project, and it lists every source it
cites, with what was checked about each.

## Why it exists

A Maintainer cannot review what they cannot follow. Without a method, "write
plainly" means whatever each agent decides, and the same failure came back
three times in Cairn's own record: opaque terms in a proposal, test names that
only made sense inside one plan, and reader-facing pages full of undefined
internal codes.

Agents add a second problem: they sound surer than they are. In one study, on
average 47% of a model's confident answers were wrong (Zhou et al., 2024).
Fluent prose from an agent therefore raises a reader's trust without showing
that the work was checked.

## What it asks

The rules sit in four groups. The full text is in the block under "Using it in
your own project", below.

| Group | Rules | What it asks of the writer |
| --- | --- | --- |
| Before you write | 1 | Know the reader and what they will do with the text. |
| Everything | 2 to 9 | Conclusion first. Say what you left unchecked. One name per thing. Define terms and keep the field's own. Short sentences, one topic per paragraph. Headings and lists for anything longer than a screen. |
| Instructions | 10 to 12 | One action per step. Say what the reader should see afterwards. Error messages say what to do next, without blame. |
| Scientific reasoning | 13 to 17 | Separate measured, assumed and expected. Give numbers with units and sources. State uncertainty as a number, not "likely". Do not claim more precision than the evidence supports. Say how sure you are about your own work. |

The rules limit how text is built, not which words it uses. A hydrologist's
"hydraulic conductivity" stays; the writer defines it.

## Two examples

These examples are invented to show the change. The numbers and messages in them are not real results.

**A claim about a model (rules 13 to 15 and 17).**

Before:

> The model matches the gauges well and the residuals are small, so it is
> probably fine.

After:

> Measured: Nash-Sutcliffe efficiency 0.71 at one gauge over 2015 to 2020
> (1,826 daily values, from `validate.py`, which I ran). Assumed: the gauge
> record has no ice-affected days; I did not check. Expected but not tested:
> similar skill in other years. I did not run this on Windows.

**A step in instructions (rules 10 and 11).**

Before:

> Install Cairn and make sure it worked.

After:

> 1. Open a terminal in the folder you want to work in.
> 2. Run the installer.
> 3. Check that it printed `installed` and created a `dev/` folder. If it did
>    not, copy the message it printed and ask the agent to fix it before the
>    next step.

## What backs it

The evidence is strongest where scientists are served worst today, and weakest
for the general writing rules. No study tested these 17 rules as a set. Each
row below says what supports one group of rules, and how strong that support
is. Citations such as "(Budescu et al., 2014)" are listed in the References
section at the foot of the page.

| Rules | Studies | Standards and guides | Cairn's own record | Strength |
| --- | --- | --- | --- | --- |
| 1 (know the reader) | None specific | ISO 24495-1:2023, clause 5.1 | Case studies written for no reader in particular, rewritten for scientists | Professional consensus |
| 2, 3 (conclusion first, leave nothing out) | Longer explanations raised readers' confidence without raising accuracy (Steyvers et al., 2025). Language-model style words rose sharply in published science (Kobak et al., 2025; Liang et al., 2025). Illusions of understanding (Messeri & Crockett, 2024) | ISO 24495-1:2023, clauses 5.2 and 5.2.2a | An early draft of this standard's own evidence overstated a result and left out how small the effect was | Direct for AI-written text; consensus for the rest |
| 4, 5 (one name, define terms, keep the field's terms) | Simpler AI summaries helped lay readers and cost the scientists credibility (Markowitz, 2024). Controlled languages are surveyed in Kuhn (2014) | ISO 24495-1:2023, clauses 5.3.2c, 5.3.2e and 5.3.2g; ASD-STE100 (its rules, not its restricted dictionary) | Three proposals with coined or inconsistent names; reader-facing pages with undefined internal codes | Partial: studies used lay readers |
| 6 (examples) | Missing examples and unclear intent were among the main obstacles in a field study of developers learning an interface (Robillard & DeLine, 2011) | None | A README example rewritten twice before readers could follow it | Direct, from one field study |
| 7 to 9 (sentences, paragraphs, structure) | Reader expectations about where information sits in a sentence (Gopen & Swan, 1990) | ISO 24495-1:2023, clauses 5.3.3c, 5.3.4a and 5.3.6; a framework that keeps kinds of documentation apart (Procida, n.d.) | Dense passages fixed in a documentation audit | Professional consensus; evidence mostly from lay readers |
| 10 to 12 (instructions, error messages) | None direct | ISO 24495-1:2023, clauses 5.2.2c and 5.2.2e; ASD-STE100; the Federal Plain Language Guidelines (PLAIN, 2011); a developer documentation style guide; error-message guidelines (Neusesser & Sunwall, 2023) | A checker that answered a deleted file with a raw traceback instead of a message | Professional consensus; the weakest base of the four groups |
| 13 (measured, assumed, expected) | In one review of 60 observational studies in a medical journal, 20% used causal language inconsistently (Olarte Parra et al., 2021). A claim framework separates explicit claims from observations and correlations (Blake, 2010) | None | None | Indirect |
| 14 (numbers with sources) | Fabricated and wrongly cited references in language-model output (Walters & Wilder, 2023). Naming the sources of uncertainty (Budescu et al., 2009) | EFSA (2019) | None | Indirect |
| 15, 16 (uncertainty as a number; uncertainty versus variability) | Readers give probability words very different meanings, and numbers do better than words (Budescu et al., 2009, 2014; Mandel & Irwin, 2021; Dhami & Mandel, 2022; Wintle et al., 2019). A protocol for stating the sources of uncertainty (Fischhoff & Davis, 2014). A book-length study of hedging in research articles (Hyland, 1998) | EFSA (2019) | None | Strong for 15, replicated across studies; indirect for 16 |
| 17 (say how sure you are) | First-person hedges reduced reliance on wrong answers (Kim et al., 2024); users relied on output whether or not it was marked uncertain (Zhou et al., 2024); an automated-science system's papers held hallucinated results its reviewer only partly caught (Lu et al., 2024) | Journal policy that humans answer for AI-assisted work (ICMJE, 2026; COPE, 2023) | None | Mixed. A second ground does not depend on the studies: the rule makes the agent's checks auditable |

The ISO clause numbers come from a read of a licensed copy, which the
standard's terms forbid copying. They were not re-checked on the open web.
ISO 24495-1 says plain-language text should be tested with its readers over
time (clause 5.4). This standard has not yet had that test (see Limits).

### Four findings that shaped the wording

1. **Probability words fail, even beside numbers (rule 15).** In 25 samples
   across 24 countries and 17 languages, readers took IPCC probability terms
   as nearer 50% than the authors meant. Adding numeric ranges raised
   agreement with the IPCC guidelines only from 27% to 40% (Budescu et al.,
   2014). Words plus numbers did no better than numbers alone (N = 1,202;
   Mandel & Irwin, 2021). Numeric ranges in brackets raised overlap with the
   intended ranges from 32% to 66% (924 participants; Wintle et al., 2019). A
   review found that attaching imprecise numbers to words does little to
   reduce misunderstanding, and that readers prefer precise numbers for
   consequential decisions (Dhami & Mandel, 2022).
2. **Simpler text can cost credibility with experts (rule 5).** Simply
   written AI summaries gave lay readers better comprehension, and made the
   scientists they described seem more credible and trustworthy but less
   intelligent (Markowitz, 2024). That study did not test expert readers'
   comprehension. Cairn keeps the field's terms as a design choice, not as a
   tested result.
3. **Fluent agent prose misleads, and a first-person hedge helps a little
   (rule 17).** Readers overestimate a model's accuracy, and longer
   explanations raise their confidence without raising accuracy (Steyvers et
   al., 2025). Models rarely voice doubt unprompted, and an average of 47% of
   their confident answers were wrong (Zhou et al., 2024). In a pre-registered
   study of 404 people, a first-person "I'm not sure, but..." lowered
   agreement with the model and improved accuracy; over-reliance fell but did
   not disappear, and impersonal hedges had weaker effects that were not
   statistically significant (Kim et al., 2024).
4. **Language models change how scientific prose looks, and invent
   references (rules 2, 14 and 17).** In more than 15 million PubMed
   abstracts, words such as "delves", "underscores" and "showcasing" rose
   sharply; the rise implies that at least 13.5% of 2024 abstracts were
   processed with a language model (Kobak et al., 2025). Across 1,121,912
   preprints and papers, estimated modification reached up to 22% for
   computer-science papers and up to 9% for mathematics and the Nature
   portfolio (Liang et al., 2025). In a test of two widely used commercial
   language models, 55% and 18% of the references they wrote for literature
   reviews were fabricated, and 43% and 24% of the real ones had substantive
   errors (636 references in 84 reviews on 42 topics; Walters & Wilder,
   2023). These studies describe the problem. None tested whether Cairn's
   rules fix it.

**Limits.** The rules were tried on three real passages of Cairn's own
writing before they shipped. No one has yet evaluated them with outside readers
over time, which ISO 24495-1 asks for. The reasoning rules rest on the
literature, not on an incident in Cairn's record. The Maintainer's own read,
about three months after release, is the check.

## Using it in your own project

The standard is versioned, licensed CC BY 4.0, and its rules name nothing
specific to Cairn. Rule numbers never change between versions, so "rule 15"
means the same thing in any project.

**What the standard owns, and what your templates own.** The standard governs
how prose, numbers, uncertainty and checks are written inside a record. Your
own templates govern what the record must contain or prove.

| Question | The standard governs | Your project's templates govern |
| --- | --- | --- |
| Structure | Conclusion first; one topic per paragraph; headings and lists (rules 2, 8, 9) | Required sections: a manuscript's, a notebook's, a review's |
| Words | One name per thing; define terms and keep the field's own (rules 4, 5) | Fixed vocabularies, such as claim-status labels or a journal's style sheet |
| Claims | Say which claims were measured, assumed or expected (rule 13) | Whether a hypothesis was exploratory or pre-specified; whether a positive control shows the apparatus can see the effect; how claims depend on each other |
| Uncertainty | A number with its source; uncertainty versus variability (rules 15, 16) | Which statistics a report must give |
| Accountability | Say what you checked and did not check, in the first person (rules 3, 17) | Who is named as author, reviewer or replicator |

To adopt the standard, copy the block below into your agent instructions or
prompts. It is written for any project: it names no Cairn file, process or
tool, and you can use it without editing it. Keep the rule numbers.

````markdown
## Cairn Plain Language

*Version 1.0. Each rule has one number and one topic. A finding cites the
number and quotes the clause. Numbers never change: a withdrawn rule keeps
its number, marked withdrawn, and a reworded rule is a new version with a
changelog line. Licensed CC BY 4.0.*

Every review and decision depends on the reader understanding what an agent
wrote. These rules apply to anything an agent writes for a person: chat
replies, manuscripts, notebooks, proposals, reviews, plans, commit messages,
documentation and error messages. They are not a word list: keep your field's
terms, and define them. The only words they rule out carry no information:
filler, vague praise, and a probability word without its number.

**Before you write**

1. Know who will read it and what they will do with it: decide, follow
   steps, review, or look something up. Write for that reader and that use.

**Everything**

2. Put the conclusion first, then only what the reader needs to act on it.
   Leave out filler and vague praise ("robust", "comprehensive").
3. Never leave out what the reader needs to decide: failures, checks you did
   not make, open questions, bad news.
4. Use one name for one thing. Do not vary names for style, do not give two
   things the same name, and do not coin a name for something that already
   has one.
5. Define a specialist term where it first matters, and keep the field's
   terms rather than writing around them. Spell out an acronym the first
   time, unless the reader uses it daily. Unpack stacked nouns: "the record
   of the re-anchor ceremony", not "the re-anchor ceremony record".
6. Give an example for each abstraction.
7. Write short sentences, one idea each, in the active voice with the actor
   first.
8. Give each paragraph one topic, stated in its first sentence. Start from
   what the reader already knows, then add what is new. Do not break the main
   thought with an aside.
9. In anything longer than a screen, use headings that say what follows and
   lists for parallel items. Move detail the main line does not need to its
   own section, and say where it is. Where several readers share a document,
   mark which part is for whom.

**Instructions** (steps, runbooks, prompts to paste, install output, error
messages)

10. One action per step, in the order the reader does them, as a command:
    "Open…", "Run…". Put conditions and warnings before the step they apply
    to, especially for anything that cannot be undone.
11. Say what the reader should see afterwards, and what to do if they see
    something else.
12. An error message says what happened, why if known, and what to do next,
    without blaming the reader.

**Scientific and technical reasoning** (proposals, reviews, decisions,
reports of results)

13. Say which claims were measured, which are assumed and which are
    expected. Never let an assumption read as a result.
14. Give the number with its unit and its source, not an adjective:
    "2.3 mm/month, from the 2025 gauge record", not "small".
15. State uncertainty as a number with its source: "±0.5 mm, from gauge
    error"; "about 1 chance in 5, from the 30 runs". Do not use a probability
    word such as "likely" on its own; readers give these words very different
    meanings. If you have no basis for a number, say so, and say what the
    judgment rests on: "I have no measure of this; I expect it to hold
    because the two models share a grid."
16. Say whether a range shows uncertainty (the value is not known) or
    variability (the value really varies), and give no more precision than
    the evidence supports, usually one or two significant figures.
17. Say how sure you are about your own work, and why, in the first person:
    "I ran the tests and they pass"; "I did not run this on Windows"; "I am
    not sure this handles feet; I found no test for it". Never let fluent
    prose stand in for a check you did not make.

**Checking.** A reader who cannot follow a passage says so, and work pauses
until the passage is clear. A reviewer cites a broken rule by number and
quotes the clause. These rules are checked by reading, never by a readability
score: a score becomes the target, and the cheapest way to raise it is to cut
the precision rules 13 to 16 protect.

**Where other rules are more specific.** A template or rule that fixes the
shape of one kind of record governs that shape: a manuscript's sections, a
notebook's schema, a review's coverage block, or a commit message's layout.
These rules govern the writing inside it.

Sources: ISO 24495-1:2023; the US Federal Plain Language Guidelines;
ASD-STE100 (instruction rules); and the empirical literature cited in the
Cairn Plain Language documentation.
````

A standalone release with its own DOI is planned after about three months of
use.

## References

There are 30 sources. Each carries a tag that says what was read:

* **[Full text]**: the Cairn authors read the work in full from a supplied
  copy (six sources).
* **[Abstract]**: the abstract, and the publisher, registry or preprint
  record, were read.
* **[Record or page]**: only a bibliographic record or a web page was read, not
  the work itself.

On 2026-10-27, every entry's authors, year, title, venue and identifier were
also checked against the publisher, the DOI registry (Crossref), or the
preprint server. The 27% and 40% figures from Budescu et al. (2014) come from
the full-text read and were not found on any open web page.

<!-- vendor-ok-begin: published paper titles and publisher names in bibliography -->

* AeroSpace, Security and Defence Industries Association of Europe. (2025).
  *ASD-STE100 Simplified Technical English, Issue 9*.
  https://www.asd-europe.org/news-media/news-events/news/simplified-technical-english-asd-ste100-issue-9
  [Record or page]
* Blake, C. (2010). Beyond genes, proteins, and abstracts: Identifying
  scientific claims from full-text biomedical articles. *Journal of Biomedical
  Informatics*, 43(2), 173–189. doi:10.1016/j.jbi.2009.11.001 [Abstract]
* Budescu, D. V., Broomell, S., & Por, H.-H. (2009). Improving communication
  of uncertainty in the reports of the Intergovernmental Panel on Climate
  Change. *Psychological Science*, 20(3), 299–308.
  doi:10.1111/j.1467-9280.2009.02284.x [Full text]
* Budescu, D. V., Por, H.-H., Broomell, S. B., & Smithson, M. (2014). The
  interpretation of IPCC probabilistic statements around the world. *Nature
  Climate Change*, 4(6), 508–512. doi:10.1038/nclimate2194 [Full text]
* Committee on Publication Ethics. (2023). *Authorship and AI tools: COPE
  position statement*.
  https://publicationethics.org/guidance/cope-position/authorship-and-ai-tools
  [Record or page]
* Dhami, M. K., & Mandel, D. R. (2022). Communicating uncertainty using words
  and numbers. *Trends in Cognitive Sciences*, 26(6), 514–526.
  doi:10.1016/j.tics.2022.03.002 [Abstract]
* EFSA Scientific Committee, Hart, A., Maxim, L., Siegrist, M., Von Goetz, N.,
  da Cruz, C., Merten, C., Mosbach-Schulz, O., Lahaniatis, M., Smith, A., &
  Hardy, A. (2019). Guidance on communication of uncertainty in scientific
  assessments. *EFSA Journal*, 17(1), e05520. doi:10.2903/j.efsa.2019.5520
  [Abstract]
* Fischhoff, B., & Davis, A. L. (2014). Communicating scientific uncertainty.
  *Proceedings of the National Academy of Sciences*, 111(Suppl. 4),
  13664–13671. doi:10.1073/pnas.1317504111 [Abstract]
* Google. (n.d.). *Google developer documentation style guide*.
  https://developers.google.com/style [Record or page]
* Gopen, G. D., & Swan, J. A. (1990). The science of scientific writing.
  *American Scientist*, 78(6), 550–558. [Record or page]
* Hyland, K. (1998). *Hedging in scientific research articles*. John
  Benjamins. doi:10.1075/pbns.54 [Record or page]
* International Committee of Medical Journal Editors. (2026). *Recommendations
  for the conduct, reporting, editing, and publication of scholarly work in
  medical journals* (updated January 2026), section V.A, Use of AI by Authors.
  https://www.icmje.org/recommendations/browse/artificial-intelligence/ai-use-by-authors.html
  [Record or page]
* International Organization for Standardization. (2023). *ISO 24495-1:2023
  Plain language — Part 1: Governing principles and guidelines* (1st ed.).
  [Full text]
* Kim, S. S. Y., Liao, Q. V., Vorvoreanu, M., Ballard, S., & Vaughan, J. W.
  (2024). "I'm not sure, but...": Examining the impact of large language
  models' uncertainty expression on user reliance and trust. *Proceedings of
  the 2024 ACM Conference on Fairness, Accountability, and Transparency*,
  822–835. doi:10.1145/3630106.3658941 [Abstract]
* Kobak, D., González-Márquez, R., Horvát, E.-Á., & Lause, J. (2025). Delving
  into LLM-assisted writing in biomedical publications through excess
  vocabulary. *Science Advances*, 11(27), eadt3813.
  doi:10.1126/sciadv.adt3813 (preprint arXiv:2406.07016) [Abstract]
* Kuhn, T. (2014). A survey and classification of controlled natural
  languages. *Computational Linguistics*, 40(1), 121–170.
  doi:10.1162/COLI_a_00168 [Full text]
* Liang, W., Zhang, Y., Wu, Z., Lepp, H., Ji, W., Zhao, X., Cao, H., Liu, S.,
  He, S., Huang, Z., Yang, D., Potts, C., Manning, C. D., & Zou, J. (2025).
  Quantifying large language model usage in scientific papers. *Nature Human
  Behaviour*, 9(12), 2599–2609. doi:10.1038/s41562-025-02273-8 (preprint
  arXiv:2404.01268, titled "Mapping the increasing use of LLMs in scientific
  papers") [Abstract]
* Lu, C., Lu, C., Lange, R. T., Foerster, J., Clune, J., & Ha, D. (2024). The
  AI Scientist: Towards fully automated open-ended scientific discovery.
  arXiv:2408.06292. doi:10.48550/arXiv.2408.06292 [Abstract]
* Mandel, D. R., & Irwin, D. (2021). Facilitating sender-receiver agreement in
  communicated probabilities: Is it best to use words, numbers or both?
  *Judgment and Decision Making*, 16(2), 363–393.
  doi:10.1017/s1930297500008603 (preprint 2020, doi:10.31234/osf.io/hm7zu)
  [Abstract]
* Markowitz, D. M. (2024). From complexity to clarity: How AI enhances
  perceptions of scientists and the public's understanding of science. *PNAS
  Nexus*, 3(9), pgae387. doi:10.1093/pnasnexus/pgae387 [Abstract]
* Messeri, L., & Crockett, M. J. (2024). Artificial intelligence and illusions
  of understanding in scientific research. *Nature*, 627, 49–58.
  doi:10.1038/s41586-024-07146-0 [Abstract]
* Neusesser, T., & Sunwall, E. (2023). *Error-message guidelines*. Nielsen
  Norman Group. https://www.nngroup.com/articles/error-message-guidelines/
  [Record or page]
* Olarte Parra, C., Bertizzolo, L., Schroter, S., Dechartres, A., &
  Goetghebeur, E. (2021). Consistency of causal claims in observational
  studies: A review of papers published in a general medical journal. *BMJ
  Open*, 11(5), e043339. doi:10.1136/bmjopen-2020-043339 [Abstract]
* Plain Language Action and Information Network. (2011). *Federal plain
  language guidelines* (Revision 1, May 2011). Current successor pages:
  https://digital.gov/guides/plain-language [Record or page]
* Procida, D. (n.d.). *Diátaxis documentation framework*. https://diataxis.fr/
  [Record or page]
* Robillard, M. P., & DeLine, R. (2011). A field study of API learning
  obstacles. *Empirical Software Engineering*, 16(6), 703–732.
  doi:10.1007/s10664-010-9150-8 [Full text]
* Steyvers, M., Tejeda, H., Kumar, A., Belem, C., Karny, S., Hu, X., Mayer, L.
  W., & Smyth, P. (2025). What large language models know and what people
  think they know. *Nature Machine Intelligence*, 7(2), 221–231.
  doi:10.1038/s42256-024-00976-7 [Full text]
* Walters, W. H., & Wilder, E. I. (2023). Fabrication and errors in the
  bibliographic citations generated by ChatGPT. *Scientific Reports*, 13,
  14045. doi:10.1038/s41598-023-41032-5 [Abstract]
* Wintle, B. C., Fraser, H., Wills, B. C., Nicholson, A. E., & Fidler, F.
  (2019). Verbal probabilities: Very likely to be somewhat more confusing than
  numbers. *PLOS ONE*, 14(4), e0213522. doi:10.1371/journal.pone.0213522
  [Abstract]
* Zhou, K., Hwang, J. D., Ren, X., & Sap, M. (2024). Relying on the unreliable:
  The impact of language models' reluctance to express uncertainty.
  *Proceedings of the 62nd Annual Meeting of the Association for Computational
  Linguistics (Volume 1: Long Papers)*, 3623–3643.
  doi:10.18653/v1/2024.acl-long.198 (preprint arXiv:2401.06730) [Abstract]

<!-- vendor-ok-end -->

## Where to read more

* The accepted proposal, with the full evidence and the review record:
  [`dev/proposals/archive/2026-10-26-claude-writing-for-the-reader.md`](../dev/proposals/archive/2026-10-26-claude-writing-for-the-reader.md).
* The reasoning behind it, in [the rationale](../doctrine/rationale.md), under
  "The comprehension floor".
* The [glossary](glossary.md) for any Cairn term used above.
