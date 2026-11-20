# Structure for the code: an agent drafts it, the scientist corrects it, a tool holds it

**Author**: Claude (Strategy)
**Model**: Claude Fable 5.2 (`claude-fable-5-2`)
**Date**: 2026-11-20
**Status**: draft
**Type**: design-exploration
**Surfaces this would feed**: the architecture-review module and its rubric in `templates/modules/team-gated/`; `dev/tools/code_map.py`; the **Reuse** field of `dev/plans/_template.md`; the Complexity tab of the v0.9 oversight website; [the v0.8 strategic review](2026-11-19-claude-v08-strategic-review.md)

## Summary

Cairn structures rules and tests. For code it shows and asks, and leaves deciding and holding to the Maintainer. I recommend three changes to things that already exist. An agent drafts the list of parts and what each may use, and the scientist corrects it in the project's own terms. The code map reads imports and warns, at each change, when code crosses a line the list does not allow. The plan names the part each chunk changes. A new coupling between parts is then the one architecture question that reaches the scientist. Nothing here is accepted work.

## The question

The Maintainer (chat, 2026-11-20): "Cairn can help scientists build better code if it structures their rules, tests, and code architecture. I feel like that latter bit is undeveloped and I have had to do a lot of manual work despite my lack of expertise". What would give a scientist who codes sound structure without asking for the expertise?

## Method

I read the architecture-review module and rubric, Cairn's own architecture record, the code map's guide, the v0.7 note and proposal on architecture and reuse, the plan template and the dashboard design. A read-only script measured Cairn's non-test Python at three revisions by the October note's stated method: functions of eight or more lines with identical structure once names and constants are stripped, byte-identical copies set aside. It also counted imports between top-level folders. I searched the 33 plans opened since 7 November for a reuse answer citing the code map. For outside studies I read abstracts and returned excerpts only; four are preprints.

I could not see LHM, modflow_tools or Assai; what the Maintainer did by hand is his report. A trial in which naming the part does not cut what a low-tier implementer reads would count against this note.

## Findings

**What exists shows and asks.** The v0.7 work made existing code cheap to see. `code_map.py` lists components, public functions and near-copies, the plan has a **Reuse** field, and Cairn's record names the homes of its safety helpers. The module's rubric is five lenses of questions and a prompt: "Fill: a short map of how the system is organized today". It asks the adopter for the answer an architect would give.

**It is off the working path.** A search finds the module in none of the three presets, and no trigger offers it. Of 25 recent plans with a reuse answer, none cites the code map in that answer; they cite searches. The module's assessment is a release-time record.

**The map does not see connections.** It reads no imports, so "tangled" has no number.

**What it measures got worse.**

| Cairn's non-test Python | 30 October | v0.7.0 | v0.8.0 |
|---|---|---|---|
| Lines | 41,020 | 59,386 | 61,275 |
| Groups of structurally identical functions in different files | 12 | 17 | 22 |
| Lines in those groups | 598 | 1,224 | 1,650 |
| Function names defined in more than one file | 48 | 80 | 80 |

The code grew by half and its exact copies nearly tripled. The October note counted 15 groups with its own script. Three weeks is a short record, and some copies are deliberate, since a shipped script must run alone. That rule has a second cost: `dev/tools/meter.py` is 6,891 lines in one file, about 87,000 tokens to read whole at four bytes a token. Cairn's folders barely import each other, with one edge at v0.8.0, so its own problems are copies and size. A package such as modflow_tools is where boundaries matter.

**Outside studies agree on where agents are weakest.**

- On probes of maintainable structure, agents solved 4.3% of cases on dependency control and 15.2% on dividing responsibility; 13.3% of all results passed every functional test and failed the structural check [1].
- When agents extended their own code, structure eroded in 77% of runs. Quality guidance lowered the starting level by up to a third and did not change the rate [2].
- More capable models wrote more coupled code, and detailed prompting did not prevent it [3]. A causal study of 151 Java repositories found no rise in architectural smells after agents were adopted, so the evidence is not uniform [4].
- A written architecture improved conformance, and an explicit plan added modularity [5]. Specifications close to code helped weaker models most [6]. Agents carried out a specified restructuring well and chose one poorly [7].
- A conformance report at each change cut violations in a field experiment with eight student projects [8].

Structure is the one place where the need grows as models improve, because volume grows.

## Options

1. **Leave it.** The Maintainer keeps deciding structure by hand.
2. **More views.** The four-view pilot helps a person see. It does not supply the expertise.
3. **More rules.** Guidance lowers the start and not the slope [2].
4. **Draft, declare, check.** I recommend this one.

## Recommendation

1. **An agent drafts the parts list.** Replace the rubric's "Fill:" prompt with a table a high-tier agent writes from the code map: each part, what it owns, what it offers and what it may use, in the project's words. The scientist reads it as a description of the system and corrects it. For a model, the parts follow the conceptual model, which the scientist knows. Hydrology already has an outside standard for a model component's outer contract: the Basic Model Interface, which the MODFLOW API builds on [9].
2. **The code map holds the line.** It already parses every Python file. Have it read imports and report the edges between parts, the edges the table does not allow, cycles, and files over a size the project sets. It warns at each change and does not block.
3. **The plan names the part.** Beside **Reuse**, the plan says which part each chunk changes and which parts it may read. The stronger model's plan then hands a low-tier implementer one part and its interface. The review note calls that selection loading.
4. **One question reaches the scientist:** a new part, or a new coupling between parts, put in the project's terms. "Routing would now read snow state. Is that coupling real in the model?" Everything inside a part is the agents' call.
5. **A move is its own kind of plan.** The stronger model lists what moves where, and the map's comparison of function structure could confirm that nothing else changed. Moves run early in a window, never at the gate; the 0.8 layout move broke tests in 46 files.
6. **Later, harvested:** starting shapes for a model, a toolkit and an agent system from LHM, modflow_tools and Assai, under the two-project rule; a size trigger that offers the module; edges and copies on the Complexity tab; copies as the consumer's third stock.

Steps 1 to 3 change three existing things and add no record. The risk is a parts list drawn too early, which freezes a poor shape, and agents did worse as structural constraints piled up [10]. Keep the list to one page and change it by proposal.

## Open questions

1. What did the manual work consist of: deciding where things go, splitting large files, untangling dependencies, or restructuring old code? The answer orders the steps.
2. Do steps 1 to 3 join v0.9's controls, or wait for v0.10?
3. Should a shipped script stay one file when it passes several thousand lines?
4. Which languages matter first after Python?

## Outside sources

Sources 2, 6, 7 and 10 are preprints and not peer reviewed.

1. Zhu, H. et al. (2026), *Needle in the Repo: Diagnosing Maintainability Failures in AI-Generated Repository Edits.* ASE. [doi:10.1145/3832783.3834401](https://doi.org/10.1145/3832783.3834401)
2. Orlanski et al. (2026), *SlopCodeBench: Benchmarking How Coding Agents Degrade Over Long-Horizon Iterative Tasks.* [doi:10.48550/arxiv.2603.24755](https://doi.org/10.48550/arxiv.2603.24755)
3. Zhu, Y., Tsantalis and Rigby (2026), *Understanding the Code and Architectural Smells Generated by LLMs and Autonomous Agents.* ASE. [doi:10.1145/3832783.3834413](https://doi.org/10.1145/3832783.3834413)
4. Larsen and Moghaddam (2026), *Mining Architectural Quality Under Agentic AI Adoption: A Causal Study of Java Repositories.* [doi:10.1007/978-3-032-36587-3_34](https://doi.org/10.1007/978-3-032-36587-3_34)
5. Cervantes, Kazman and Cai (2026), *Improving LLM-assisted code generation through the use of architectural documents and implementation plans.* [doi:10.1145/3786152.3788588](https://doi.org/10.1145/3786152.3788588)
6. Canedo (2026), *Architecture as Capability Equalizer for Coding Agents.* [doi:10.48550/arxiv.2608.21747](https://doi.org/10.48550/arxiv.2608.21747)
7. Thillen et al. (2026), *CodeTaste: Can LLMs Generate Human-Level Code Refactorings?* [doi:10.48550/arxiv.2603.04177](https://doi.org/10.48550/arxiv.2603.04177)
8. Olsson et al. (2016), *Evaluation of an architectural conformance checking software service.* ECSA. [doi:10.1145/2993412.3003391](https://doi.org/10.1145/2993412.3003391)
9. Hughes et al. (2021), *The MODFLOW Application Programming Interface for simulation control and software interoperability.* Environmental Modelling & Software. [doi:10.1016/j.envsoft.2021.105257](https://doi.org/10.1016/j.envsoft.2021.105257)
10. Dente, Satriani and Papotti (2026), *Constraint Decay: The Fragility of LLM Agents in Backend Code Generation.* [doi:10.48550/arxiv.2605.06445](https://doi.org/10.48550/arxiv.2605.06445)
