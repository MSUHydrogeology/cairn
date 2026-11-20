# Structure for the code: a layout the scientist can read, and central tools agents use

**Author**: Claude (Strategy)
**Model**: Claude Fable 5.2 (`claude-fable-5-2`)
**Date**: 2026-11-20
**Status**: revised
**Type**: design-exploration
**Surfaces this would feed**: the architecture-review and legacy-agent modules; `dev/tools/code_map.py`; the plan template's **Reuse** field; [the v0.8 strategic review](2026-11-19-claude-v08-strategic-review.md)

## Summary

The Maintainer reads code as a place: what each folder holds, which classes hold state, and which central tools the rest relies on. Cairn keeps that account for documents, rules and tests, and not for code, so he has kept it by hand. I recommend four changes. An agent drafts a layout page and the scientist corrects it. A check keeps the page true at each change. The plan says where new code goes and which central tool it uses. Old code is restructured by approving a page; agents do the moving. Nothing here is accepted work.

## The question

The Maintainer (chat, 2026-11-20): "When I say architecture, I mean things like 'what is in this folder in the code?' or 'what different classes exist that hold states?'. I am talking about the physical organization of the code and my ability to understand and account for it." On shared code, agents "like one-off solutions that are really customized, rather than central rock-solid capabilities with some additional function arguments." He named restructuring old code "the biggest deal".

A **central tool** is one function or file that does a common job for the whole project, such as the one reader for a model's output file. A **one-off** repeats such a job for a single task. **State** is what a program stores as it runs, such as the water in each cell.

## Method

I read the architecture-review and legacy-agent modules, Cairn's architecture record, the code map's guide, the plan template, the documentation plan, and the 0.8 layout plan and run record. Two read-only scripts measured Cairn's non-test Python at v0.8.0, installed copies set aside: folders, classes that declare or set stored values, and function names that recur with different bodies. For outside studies I read abstracts and returned excerpts only.

I could not see LHM, modflow_tools or Assai; the manual work is the Maintainer's report. This note is wrong if a scientist cannot correct an agent's layout page without reading code, or if implementers given the page write one-offs as often as before.

## Findings

**Cairn says where a document, a rule and a test go, and not where code goes.** `dev/README.md` lists each records folder and what it holds. The documentation plan places each new document, `RULES.md` routes each task to its rule file, and a tool lists the tests each change needs. For code there is the plan's **Reuse** question. A module that a search finds in none of the three presets asks the adopter for the rest: "Fill: a short map of how the system is organized today". Of Cairn's 12 code folders, 2 carry a README; `dev/tools`, with 22 files, has none.

**No record lists the classes that hold state.** The code map gives each class a one-line summary, and not what it stores. Cairn has 70 such classes in 25 files.

**Central tools are named for four jobs, and code is written around them.** Cairn's architecture record names homes for four safety helpers; one runs Git, and a central Git reader arrived on 6 November. At v0.8.0, seven functions named `git` or `_git` sit in seven files with seven different bodies, one in an archived script. The lines that load the central reader are copied into five files in three versions. Some copies are deliberate: a shipped script must run alone. Exact copies of functions across files grew from 12 groups to 22 in three weeks. Of 25 recent plans with a reuse answer, none cites the code map; they cite searches.

**Cairn's restructuring was dear.** The 0.8 layout move had a plan of 9,692 words. The first full test run afterwards failed 195 tests and hit 18 errors in 46 files; about 29 commits repaired them. Among the causes, the run record names stale paths and tests that count parent folders to find the root. My reading: many files each knew where a folder was, so moving it broke them all.

**For old code, Cairn says how to change it, not how to reorganize it.** The legacy module has the adopter fill 14 fields for each piece of old code and pin its behaviour with tests first.

**Outside studies match the Maintainer's observation.**

- Agents left duplicated logic in 50.8% of multi-step tasks by step five, while pass rates barely moved [1].
- Agent pull requests were more redundant than human ones. The authors expect such copies to do one job in different words, which copy detectors miss [2].
- In five systems, about half of the accidental differences between copies were faults [3].
- Guidance lowered where structural decay started and not its rate [4]. A report at each change cut breaks of a declared structure in eight student projects [5].
- Agents carried out a restructuring specified in detail and often failed to choose as a person did; proposing before implementing helped [6].
- Not all evidence agrees: a study of 151 Java repositories found no rise in structural problems after agents arrived [7].

**Why agents write one-offs (my reading, not a measurement).** An implementer sees one task, and a new function costs little. A change to a shared file lies outside the chunk's listed files and brings more tests. The tests pass either way.

## Recommendation

1. **A layout page.** It replaces the rubric's "Fill:" prompt and holds three lists: each folder and what belongs in it; each class that holds state, what it stores and what may change it; each central tool, its job, its promise and its home. A high-tier agent drafts it from the code, and the scientist corrects it as a description of the project.
2. **A check keeps the page true.** At each change `code_map.py` would report what the page does not cover: a new folder, a new class that holds state, a function that copies a central tool, a file over a set size. It warns, does not block, and will miss copies written in different words [2].
3. **The plan chooses the tool.** Beside **Reuse**, the plan says where each chunk's new code goes and which central tools it calls. Where a tool nearly fits, the plan adds an argument to it in an early chunk and lists its file. The plan's author decides this, not the implementer.
4. **Central tools carry the strongest tests.** Each has a stated promise and public tests of it. Code that calls the tool does not test that job again.
5. **Two questions reach the scientist.** A change to the page: "Routing would now change the snow class's stored depth. Is that right in the model?" A difference between copies: "One reader skips dry cells and the other returns zero. Which is right?"
6. **Restructuring old code.** An agent drafts two pages: the layout today and the layout proposed. The scientist corrects and approves the second. Agents plan two kinds of step, never mixed. A **move** changes where code lives and nothing else; the code map confirms each function is otherwise unchanged. A **fold** replaces several one-offs with one central tool: its promise test comes first, then each one-off becomes a call. For a model, a reference run gives the same numbers before and after. Tests reach code through one helper that knows the layout. Restructuring runs early in a release window.
7. **After each tag, the removal pass folds copies** (the review note's idea 8). Only a pass that sees every copy can see they do one job.
8. **Later:** starting layouts harvested from LHM, modflow_tools and Assai under the two-project rule.

Steps 1 to 3 change three existing things. The other paths are to leave it, add views, or add rules, which did not hold [4]. A page drawn too early freezes a poor layout, so change it by proposal. A central tool can gather too many arguments, so make one only when a second user exists.

## Open questions

1. Which project should try restructuring by page first?
2. Do steps 1 to 3 join v0.9's controls, or wait for v0.10?
3. Should a shipped script stay one file past several thousand lines? `dev/tools/meter.py` has 7,322.
4. Which languages matter after Python?

## Outside sources

Sources 1, 4 and 6 are preprints and not peer reviewed.

1. Ma et al. (2026), *Do Coding Agents Reuse Existing Code or Reinvent the Wheel?* [doi:10.48550/arxiv.2609.35357](https://doi.org/10.48550/arxiv.2609.35357)
2. Huang et al. (2026), *More Code, Less Reuse.* MSR. [doi:10.1145/3793302.3793622](https://doi.org/10.1145/3793302.3793622)
3. Juergens et al. (2009), *Do code clones matter?* ICSE. [doi:10.1109/icse.2009.5070547](https://doi.org/10.1109/icse.2009.5070547)
4. Orlanski et al. (2026), *SlopCodeBench.* [doi:10.48550/arxiv.2603.24755](https://doi.org/10.48550/arxiv.2603.24755)
5. Olsson et al. (2016), *Evaluation of an architectural conformance checking software service.* ECSA. [doi:10.1145/2993412.3003391](https://doi.org/10.1145/2993412.3003391)
6. Thillen et al. (2026), *CodeTaste.* [doi:10.48550/arxiv.2603.04177](https://doi.org/10.48550/arxiv.2603.04177)
7. Larsen and Moghaddam (2026), *Mining Architectural Quality Under Agentic AI Adoption.* [doi:10.1007/978-3-032-36587-3_34](https://doi.org/10.1007/978-3-032-36587-3_34)
