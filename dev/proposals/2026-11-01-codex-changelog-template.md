# Ship a changelog template

**Author**: Codex GPT-6 (Implementation)
**Status**: revising
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Give adopters a ready-to-use changelog so they can record releases in a clear, consistent format.

## Decision summary

Ship a short changelog at the project root, with instructions in its header and an empty Unreleased section. It follows Cairn's current Major and Minor groups and starts each entry with its Keep a Changelog type. Existing project histories must be preserved; adding an installed file also means an existing history can require a deliberate upgrade collision resolution.

## Context

The committed board asks for this template and assigns Codex the proposal and implementation (`dev/PLANNING.md`, changelog-template row at commit `1e525b12`). The shipped `templates/core/AGENTS.md` and `templates/core/dev/PLANNING.md` refer to a changelog, but `_CORE_MAPPINGS` in `bootstrap/_scaffold/config.py` does not install one. Cairn's `CHANGELOG.md` shows the requested format and use instructions.

## Proposal

Add `templates/core/CHANGELOG.md`, mapped to `CHANGELOG.md` for every profile. Directly under its title put `Written in Cairn Plain Language 1.0`, linked to the installed `dev/agent_collaboration.md` rules. In the header explain briefly how to choose Major or Minor, start entries with Added, Changed, Deprecated, Removed, Fixed or Security in that order, write plainly, and open a new Unreleased section at release. Provide empty Major and Minor headings under Unreleased. Avoid Cairn-project-specific record-link requirements.

Point the existing changelog reference in shipped `AGENTS.md` to the installed file and its in-file instructions; do not add a separate process or duplicate those instructions. A normal install into an empty destination supplies the template. An existing file is preserved by normal install; explicit `--force` retains its existing overwrite meaning. On upgrade, a new core mapping at an occupied, unlocked regular file is blocked for explicit collision adoption or manual reconciliation; a destination tracked under another source is a provenance conflict, not auto-adopted. Existing history must survive these normal paths byte-for-byte. Unsafe or non-regular paths remain subject to existing refusals. Do not weaken collision handling or change upgrade semantics to make this file install silently.

Proposed paths:
- `templates/core/CHANGELOG.md`

## Rationale

The instructions travel with the file at the point of use. The governing reference makes them discoverable without repeating them. Reusing the core mapping and collision machinery avoids inventing another install path, but may require an adopter to resolve a collision when upgrading.

## Alternatives considered

Keep only references and ask adopters to make their own file: no installer change, but no starting format or local instructions. Install a separate example instead: it avoids the root collision but leaves the requested changelog absent and requires a copying step.

## Documentation / doctrine surface

The template is adopter-facing guidance; the reference belongs in the shipped governing `AGENTS.md`. The proposal is deliberation in `dev/`. The mapping changes the published install contract. Update relevant install descriptions and manifests only where needed to keep them accurate; no new doctrine is proposed.

## Evidence / verification plan

### Tests required

In `bootstrap/tests/`, exercise actual scaffold install and upgrade entry points for an empty target, an existing history on normal install, a new-core collision and its adoption, a provenance conflict, and unsafe paths; assert the history's bytes and the lock/base records where applicable. Check profile coverage, manifest membership and the template's headings, marker, type order and usable instructions. Identify exact nodes and mapped file readers in the plan after inspecting existing tests; add focused tests where absent. A silent replacement of history, missing file, broken link or misleading manifest falsifies the proposal.

### Examples / smoke checks

Run mapped iteration tests and prose claim, link, snippet and neutrality gates; run the final wide Boundary B on the clean reviewed commit under Python 3.13, with the selected commands and outcomes recorded. No full-tree certification or re-anchor is authorized by this proposal.

#### Security preflight

- **S1:** The shipped mapping selects the template and destination; the adopter supplies target paths, existing files and lock records. Existing content and lock metadata are inputs to collision decisions.
- **S2:** Focused behavior tests must fail if collision detection is bypassed or existing bytes are replaced; these mutations have not yet been run and belong in implementation evidence. A self-derived expected value would not establish preservation.
- **S3:** The plan will name the entry-point test commands and their selected cases; the adopter-facing promise is that normal install preserves an existing file and upgrade requires collision resolution. Test those exact cases, not just mapping membership.
- **S4:** A collision, ambiguous ownership or unsafe path must refuse or preserve data rather than grant overwrite authority; explicit force remains an intentional overwrite. Verify each failure path rather than infer it from the mapping.
- **S5:** A malicious actor able to alter both trusted installation records and their matching cache can still defeat integrity checks; this addition does not close that existing class. Concurrent filesystem changes remain outside a static path check.

### Independent scientific check

N/A: no scientific assumption or published scientific result changes.

## Assurance path

**Assurance path**: high-assurance. The mapping touches the scaffold engine and install contract, both high-risk surfaces; ordinary and Security Reviews are required. A plan defines the exact checks and collision evidence.

## Review -- Codex GPT-6 -- 2026-11-01

Reviewed commit: `818b6758`; target: whole proposal; prior findings: none.
Tier: usual; verdict: **PROCEED**; findings: none.
Elapsed: approximately 2 minutes; tokens: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. The board asks for a short root template with Major and Minor groups, typed entries and header instructions (`dev/PLANNING.md`, changelog row at `1e525b12`). The proposal supplies those, places the Plain Language marker on the template, and avoids repeating the instructions in the governing file. The existing changelog supplies the stated format.
2. **Best alternative.** An example beside the installed files avoids a root collision, but leaves the requested ready-to-use root changelog absent and adds a copying step. The proposed collision handling preserves the existing upgrade contract.
3. **What would show it wrong?** An actual install or upgrade replacing an existing history, a collision adoption corrupting its bytes or base record, or instructions that cannot produce the stated format. The proposal calls for entry-point tests of these cases.

**Coverage:** Read the committed proposal, board request, current changelog, core mapping and install and new-core upgrade paths. The install path skips existing files unless forced; the upgrade path distinguishes an unlocked collision from another source's ownership. Did not run implementation tests, inspect every installer path or conduct Security Review; those remain for the plan and separate review.

## Security Review -- Codex GPT-6 -- 2026-11-01

Reviewed commit: `842b0065`; target: whole proposal; prior Security findings: none.
Tier: Internal; Obligation: Security Review; verdict: **PROCEED**; findings: none.
Elapsed: approximately 4 minutes; tokens: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. The board requests an installed root changelog, and the proposal explicitly preserves normal-install history and existing upgrade collision controls. At the reviewed commit, `_install_one` skips occupied files without force; new-core upgrade planning distinguishes unlocked collisions from another source's ownership (`bootstrap/_scaffold/install.py`, `_install_one`; `bootstrap/_scaffold/upgrade.py`, new-core loop). Adding a mapping therefore deserves the proposed heavy lane and separate Security Reviews, without adding a new adopter ceremony.
2. **Best alternative.** A separate example avoids occupying the history path but loses the requested ready-to-use root file and adds copying. Reusing `_CORE_MAPPINGS` and the existing adoption path is smaller while retaining explicit overwrite authority. Adoption checks the observed and upstream digests, revalidates a regular contained destination, and writes lock/cache records without replacing the history (`adopt_collisions`).
3. **What would show it wrong?** Entry-point tests showing overwritten history, adoption of another source's destination, corrupted merge ancestry, unsafe writes or a profile missing the file. The proposal requires those behavior checks and mutation evidence; membership checks alone would not establish preservation. Its explicit force exception avoids promising preservation when overwrite was authorized.

**Coverage:** Read the committed proposal, ordinary review, board request, core mappings, install skip/write guards, new-core collision classification and collision-adoption validation/commit path. No implementation exists in this proposal review; did not run tests or mutations, inspect every upgrade/apply branch, or establish race resistance. Plan and implementation Security Reviews remain owed.

## Author response -- Codex GPT-6 -- 2026-11-01

Both reviews found no findings; no operative revision is needed. The plan and implementation retain the proposed collision, preservation and Security Review checks.

Elapsed: approximately 2 minutes; tokens: unknown.
