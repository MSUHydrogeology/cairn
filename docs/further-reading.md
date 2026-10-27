# Further reading — the craft Cairn relies on but does not re-teach

Cairn governs the **deliberation lifecycle**; it does not teach the
underlying software-engineering and open-science craft. This page is a
**curated signpost**, not a literature review: it points an adopter at
the resources that fill the gaps Cairn deliberately leaves to better
sources.

**Curation governance.** This list earns its keep by staying short and
honest:

* **One slot per resource**, one line of description, and a
  *why it matters to a Cairn adopter* that names **the one Cairn
  lifecycle gap it fills**. If a resource doesn't map to a specific
  gap, it doesn't belong here.
* Each entry carries a **last-checked** date. On review, stale or
  superseded entries are removed — this is a signpost, not an archive.
* When in doubt, prefer fewer, load-bearing pointers over completeness.

---

## Reproducible, ethical, collaborative practice

* **The Turing Way** — <https://book.the-turing-way.org/> *(last
  checked 2026-05-22)*. A community handbook for reproducible,
  ethical, and collaborative data science.
  *Why it matters:* Cairn's lifecycle records *that* a change was
  reviewed and reproducible, but does not teach reproducible-research
  practice itself — the Turing Way does, and is the model for
  adopting Cairn by reading the doctrine alone.

## Foundational computing skills

* **The Carpentries / Software Carpentry** — <https://carpentries.org/>
  (Software Carpentry: <https://software-carpentry.org/>) *(last
  checked 2026-05-22)*. Hands-on lessons in shell, version control,
  and programming for researchers.
  *Why it matters:* Cairn assumes a working baseline in git and
  scripting (the apparatus *is* git-committed); the Carpentries teach
  that baseline, which Cairn does not.

## Working with AI agents in science

* **"Ten simple rules for using large language models in science"**
  (PLOS Computational Biology, 2024) —
  <https://doi.org/10.1371/journal.pcbi.1011767> *(last checked
  2026-05-22)*. Practical rules for LLM-assisted scientific work.
  *Why it matters:* Cairn governs how an AI-produced change is
  reviewed and recorded, but does not enumerate how to *use* an LLM
  well in the first place — this does.
* **"Ten simple rules for navigating AI in science"** (PLOS
  Computational Biology, 2025) —
  <https://doi.org/10.1371/journal.pcbi.1013259> *(last checked
  2026-05-22)*. The risk-and-navigation companion to the rules above.
  *Why it matters:* Cairn's Dual-Review exists because AI output needs
  independent scrutiny; this frames *which risks* that scrutiny is
  guarding against.

## Software quality for scientists

* **"Ten simple rules for training scientists to make better
  software"** (PLOS Computational Biology, 2024) —
  <https://doi.org/10.1371/journal.pcbi.1012410> *(last checked
  2026-05-22)*. Testing, structure, and quality habits for research
  software.
  *Why it matters:* Cairn *requires* a change to absorb tests and docs
  but does not teach what good tests or structure look like — this
  fills that gap.

## Verification and reproducibility for scientific computing

* **Sandve et al. (2013), "Ten Simple Rules for Reproducible
  Computational Research"** (PLOS Computational Biology 9(10):e1003285;
  doi:10.1371/journal.pcbi.1003285) *(last checked 2026-06-11)*.
  Ten concrete rules for reproducible results: avoid manual data-
  manipulation steps, record exact versions, record all intermediate
  results, connect results to statements in papers, and provide scripts
  for results that rely on statistical tests. For the deeper V&V
  framework (verification vs. validation vs. uncertainty quantification
  as distinct activities), see Oberkampf & Roy (2010), *Verification
  and Validation in Scientific Computing* (Cambridge UP,
  ISBN 9780521113601), and the W3C PROV-DM provenance data model (2013).
  *Why it matters:* For any change that touches a scientific assumption,
  Cairn's proposal and plan templates require one **Independent scientific
  check** (an expected value from an analytical solution, conservation law,
  observation, independent implementation, or prior expert expectation, paired
  with a purposeful failing run). That check catches a mistake on a single
  change, but it is not a full verification, validation, and uncertainty-
  quantification (VVUQ) programme — these resources teach that broader craft.

---

*Maintainers:* keep this page to the format above (one line + one
"why it matters" naming a Cairn gap + a last-checked date). When a
resource is superseded or no longer maps to a gap, remove it. See
[`workflow-role.md`](workflow-role.md) for the boundary this page
enforces (Cairn points outward for craft instruction).
