# Ship a project rules router stub

**Author**: GPT-6.1 Terra (proposal author)
**Status**: revising
**Review**: usual + Security Review
**Proposed tier**: heavy — changes the install contract and file handling
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-12
**In brief**: Give new adopters a small project rules router while protecting rules they already own.

## Decision summary

Ship a small `RULES.md` starter so the existing instruction to read project rules has somewhere to lead. Treat it as project-owned living state: teams can edit it without repeatedly attesting its contents. This changes the install and upgrade contract and adds a file for teams to maintain; it must preserve existing rules and deletion choices. One independently finishable plan delivers the change after acceptance.

## Context

The shipped `AGENTS.md` tells agents to read `RULES.md` first, but `bootstrap/tests/test_scaffold.py` and `bootstrap/tests/test_upgrade.py` currently assert that Cairn neither installs nor tracks it. Cairn itself already has a project-owned `RULES.md`. The changelog offers an established model: `bootstrap/UPGRADE.md` describes a living-state seed, normal-install preservation and a reviewed upgrade collision. That documented behavior is evidence for the model, not proof that a new rules mapping already handles every collision.

## Proposal

Add a short vendor-neutral core template and map it for all profiles using the existing core delivery machinery. It should orient a team to put its own concise, always-applicable rules and routes there, without prescribing project-specific rules. Keep the installed `AGENTS.md`, wrapper and `RULES.md` together at or below 1,500 words. Update the existing tests that assert absence and any affected manifest, install and upgrade contracts.

On a fresh install, seed an absent rules file; normal install must leave an existing file byte-for-byte intact. On an upgrade from a version that did not track it, present an existing regular file for review as a collision and allow the existing reviewed adoption flow to retain it as a tracked fork. Refuse or require manual resolution for links, directories and other ineligible destinations. Once tracked, preserve adopter edits and deliberate deletion through upgrades; do not silently restore a deleted file. The implementation must establish these outcomes through the existing living-state, merge-base and collision mechanisms, adjusting them where necessary, and must not replace Cairn's own rules. Retain the existing explicit `--force` behavior that overwrites existing files, and document it.

A rules record must participate in upgrade tracking and the authoritative living-state allowlist, with the normal source and merge-ancestor attestation contracts intact. Exempt only adopter rules content from the integrity hash; do not let arbitrary records self-exempt or weaken source verification. Update adopter-facing install and upgrade documentation and the release note to explain ownership, collision and deletion behavior. No new framework is proposed.

## Rationale

The instruction to read rules is useful only when a team can find and own them. Reusing the changelog's delivery path avoids inventing a second ownership mechanism, but rules are instructions to agents, so the integrity exemption and preservation behavior deserve independent security review.

## Alternatives considered

Keep the current convention and let each team create its own file. That avoids a new tracked file and collision work, but leaves the read-first instruction pointing at an absent file in fresh installs and gives teams no starter.

## Documentation / doctrine surface

The shipped template and install contract land in bootstrap's core mappings, lock policy and relevant manifests; descriptive install and upgrade guidance belongs in `bootstrap/UPGRADE.md` and the appropriate descriptive documentation. Update `docs/methodology/doc-governance.md` for consistency with the shipped starter, and update other governing text only if needed, preserving its layer and the word cap; deliberation stays here. The release note describes the adopter-visible change.

## Evidence / verification plan

### Tests required

Use existing `bootstrap/tests/test_scaffold.py`, `bootstrap/tests/test_upgrade.py` and `bootstrap/tests/test_upgrade_module_additions.py` homes, extending public install, upgrade plan/stage/apply and integrity checks for: fresh seed and existing-file preservation; reviewed collision adoption and refusal of an unsafe destination; edited and deleted tracked rules surviving later upgrades; and living-state exemption limited to the authorized path. Map exact nodes and affected consumers in the plan. A failure to preserve rules or deletion, or an arbitrary integrity exemption, falsifies the proposal. Do not add wording pins or a new test harness.

### Examples / smoke checks

Run the scoped prose integrity and quality gates, manifest and relevant profile install checks, and the changed-file test selection. Verify the combined word cap and source/lock records. Full certification remains a separate authorized run.

#### Security preflight — five questions, answered in writing

1. The installer and upgrade read the shipped template and mappings, target files, lock records and staged collision evidence; the target project supplies the latter three. Source attestation must remain anchored in trusted release inputs, not a target's own assertion.
2. Prospective checks must fail when a destination is a link, staged collision bytes change, or an unauthorized record claims living-state status. These mutations have not been run for this proposal; the plan must select and record the appropriate existing public checks.
3. The implementation plan must identify the actual install, upgrade and integrity commands, their input sets and matching adopter-facing guidance; no new coverage is claimed yet.
4. Invalid paths, stale collision evidence and unauthorized exemptions must refuse the operation, not grant write or integrity-bypass authority. A missing previously tracked rules file must remain missing.
5. A project contributor able to edit its rules can still place hostile instructions in that project-owned file; this change does not authenticate the meaning of those instructions.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Withdraw or redesign if the existing upgrade machinery cannot preserve project rules and deletion without weakening source attestation, or if maintaining the starter costs more than its orientation value.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance

## Review -- GPT-6.1 Terra (Reviewer) -- 2026-11-12

Reviewed commit: f8b02eea

**Tier**: usual
**Findings**: non-blocking advice
**Verdict**: ACCEPT
**Elapsed**: approximately four minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen?** Yes: it supplies the requested starter through the
   existing core install path while making preservation, collision adoption,
   deletion and the combined word cap observable. Evidence: board direction,
   proposal outcomes and the existing changelog flow in `bootstrap/UPGRADE.md`.
2. **Best alternative.** Keep the optional convention and let teams create a
   router themselves. That is cheaper to implement but omits the starter the
   Maintainer expressly requested; reusing living-state delivery is the smaller
   mechanism that delivers it.
3. **What would show it wrong?** A public install overwriting existing rules,
   an upgrade restoring a deliberate deletion, or an arbitrary lock record
   obtaining the exemption. The proposed public checks target each fault;
   RULES-specific outcomes remain unmeasured, as the author states.

Two small clarifications would help the Decision: state that existing
`--force` overwrite behavior is retained (`bootstrap/UPGRADE.md:571`), and name
`docs/methodology/doc-governance.md` among the pages whose no-stub description
must change. The stated consistency scope already covers both; neither needs
another review pass.

**Audience:** Ownership, collision and deletion are person-level choices;
agent installation duties remain in operative homes. No governing rule is
removed by this proposal. **Coverage:** Read committed proposal, template,
board direction and existing delivery documentation. Did not establish actual
RULES collision behavior, run implementation checks, perform Security Review
or make a Decision.

## Response -- GPT-6.1 Terra (Author) -- 2026-11-12

Accepted both non-blocking clarifications: the proposal now retains explicit `--force` overwrite behavior and names `docs/methodology/doc-governance.md` for the consistency update. No scope or Decision changed. **Elapsed**: approximately two minutes. **Tokens**: unknown.

## Review -- GPT-6.1 Sol (Security Review) -- 2026-11-12

Reviewed commit: 8188e7e5c7ad3eb5431aedb099dda6bc5fa5e408

**Tier**: Security Review
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: approximately three minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes: an explicitly project-owned starter
   can reuse existing delivery without granting its contents source authority.
   The proposal limits the exemption to adopter content and retains source and
   merge-ancestor checks; current policy rejects arbitrary opt-outs --
   `bootstrap/verify_integrity.py:445`.
2. **Best alternative.** Leave the router optional and untracked. That removes
   collision work but omits the requested starter; reuse is credible because
   public changelog adoption stages both versions and retains the exact adopter
   bytes as a tracked fork --
   `bootstrap/tests/test_upgrade_module_additions.py:1033`.
3. **What would show it wrong?** Public stage/apply restoring deleted rules,
   replacing edited rules, accepting changed collision evidence or exempting a
   script would falsify the design. Existing adoption and integrity workflows
   supply the test homes; RULES-specific outcomes remain prospective --
   proposal verification plan; `bootstrap/tests/test_upgrade.py:2413`.

The proposal correctly treats preservation as implementation work. Living-state
status skips content attestation, not upgrade processing; missing tracked
mergeable files currently become review-only, and ancestors are verified before
merging -- `bootstrap/_scaffold/upgrade.py:866` and
`bootstrap/_scaffold/upgrade.py:905`. Collision adoption records separate
upstream and adopter hashes; new-core ownership conflicts remain blocked --
`bootstrap/_scaffold/upgrade.py:1910` and
`bootstrap/_scaffold/upgrade.py:995`.

**Covered:** Committed clarified proposal, existing install preservation/force,
collision adoption, deletion classification, ancestor binding and allowlist
enforcement, with public workflow controls. Ownership/force documentation
clarifications preserve agent duties and name the changed doctrine home.
**Not covered:** No RULES implementation, public-command rerun, mutation,
suite, release attestation or Decision. This exemption cannot authenticate the
meaning of project-authored agent instructions, as the proposal states.
