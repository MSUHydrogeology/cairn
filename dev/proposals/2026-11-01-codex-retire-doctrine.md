# Retire the doctrine folder

**Author**: Codex GPT-6 (proposal author)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Move Cairn's public methodology to its chosen home and retire the doctrine folder without losing guidance or breaking its consumers.

## Decision summary

Move useful public methodology into `docs/methodology/` and remove `doctrine/` after its content and live dependencies are safely accounted for. Complete operating duties belong in usable installed homes and Cairn-specific rules in `dev/rules/`. Careful review removes an extra home while preserving adopter guidance.

## Context

The Maintainer chose these destinations in the C2 routing choice in `dev/plans/archive/2026-10-28-governing-text-single-source.md`; that record says the choice made no relocation or deletion. The Maintainer has now confirmed the intention to remove the folder entirely (chat, 2026-11-01). Current `doctrine/` contains methodology and operating guidance, while `AGENTS.md` describes its references as published methodology rather than adopter-local files. References also occur in templates, tests and software; for example `scripts/check_cairn.py` classifies internal-only paths, and the session helper has shipped and self-hosted copies. Dependencies remain uncounted.

## Proposal

Inventory the current contents and their readers, links, path claims, installation mappings, executable consumers and byte pins from the committed tree. Route useful public methodology to the chosen documentation home, preserve complete operating duties in usable installed files with working pointers, and route project-specific rules to `dev/rules/`. Do not silently discard a duty or useful explanation; resolve uncertain meaning against its sources. Preserve historical records as records rather than rewriting their history.

Migrate live references and path-sensitive behavior, including internal-dependency checks, installer/configuration consumers, protected tests and the byte-identical shipped and self-hosted session helpers where affected. Keep checks effective after the old directory disappears, rather than merely making them pass. Remove the folder only after its contents and live dependencies are accounted for and the relevant checks pass. Update the active governing and descriptive guidance to reflect the new homes. Do not add redirects, a permanent inventory or ledger, a generator, or unrelated reorganization.

Coordinate with `dev/proposals/2026-11-01-codex-plain-language-docs.md`: carry forward completed improvements and review relocated material in its final homes, including installed guidance, so the same text need not be rewritten twice. Neither project may claim the other's unfinished work as complete.

Proposed paths:
- `docs/methodology/`

## Rationale

The routing is already decided; completing it gives public readers a discoverable home and keeps instructions where adopters can use them. The migration must include software and checks because a path can carry behavior even when its text looks like a link. A permanent inventory adds maintenance burden.

## Alternatives considered

Leave the folder in place: avoids migration work but leaves the chosen routing unfinished and the stated removal undone. Move files and add redirects: preserves old paths temporarily but creates another maintained surface and can conceal live dependencies. A rename alone risks installed duties and checks.

## Documentation / doctrine surface

Public methodology goes under `docs/methodology/`; cross-cutting installed prescription stays in appropriate installed governing files, project-specific rules go in `dev/rules/`, and deliberation remains in `dev/`. Update relevant `AGENTS.md`, templates and descriptions as needed. This changes protected doctrine and may touch the install contract, session binding readers and protected tests; their existing security and review obligations remain in force.

## Evidence / verification plan

The plan will map the actual content and consumers to destinations, affected test nodes and real entry points before edits, including checks that classify internal dependencies and all byte-pinned copies. It will distinguish historical references from live requirements and use a known-positive case to validate negative searches. Compare duties and usable pointers at their destination against their sources; a missing duty, broken live path, weakened check, divergent required copies or changed install behavior falsifies the result. Keep unresolved requirements open.

### Tests required

Use `python tools/test_tiers.py for` the changed paths and map affected behavior and consumers to exact nodes in `bootstrap/tests/` and other owning homes. Exercise affected install/configuration and session-helper entry points and protected path checks, including meaningful mutations where required. Run the required wide Boundary B on the clean final commit under Python 3.13 after review, with commands, counts, omissions and results recorded. This proposal does not authorize a full-tree certification or a per-plan re-anchor; the existing v0.6 cut direction remains in force.

### Examples / smoke checks

Run applicable claim, link, snippet, neutrality and internal-dependency checks, including `python scripts/check_cairn.py`, and claim checks before committing proposal, plan and documents. Check final links and pointers and test check sensitivity where required.

#### Security preflight

- **S1:** Maintainers and authors supply edits; existing committed guidance, install mappings, tests and configuration supply the inputs to routing and path checks. Some checks inspect the changed tree itself, so their expected behavior needs independent evidence.
- **S2:** A removed required duty, broken live path or incorrectly admitted internal dependency should fail a mapped check or independent comparison. No mutations have been run for this proposal; the plan must specify and record them where required.
- **S3:** The plan will identify each affected check's command, trigger and input set, then compare those with the instructions it protects. Discovery is incomplete, so no universal coverage is claimed here.
- **S4:** Missing or ambiguous sources and path-resolution failures must not grant authority or silently relax a check; leave the affected work open until resolved.
- **S5:** A plausible incorrect instruction or an unrecognized consumer can survive search and tests. Review reduces but cannot eliminate that risk.

### Independent scientific check

N/A: no scientific assumption or published scientific result is intended to change.

## Signals the change is wrong

An adopter loses a complete duty, a reader cannot reach useful methodology, a live consumer breaks, or a path check passes after its protection has been removed.

## Scope delta

None.

## Assurance path

**Assurance path**: high-assurance. Protected doctrine and potentially install, session-binding and test-control surfaces require ordinary and Security Reviews; the plan must identify the actual affected surfaces and their required checks. Any newly discovered trust boundary stops implementation for reassessment.
