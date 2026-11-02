# Plan: Remove the obsolete finding marker

**Source proposal**: dev/proposals/archive/2026-11-02-codex-stray-finding-id.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-02
**In brief**: Remove one closed-review marker while preserving the documented scaffold safeguard.

## Source proposal

The Maintainer accepted the heavy proposal to remove only the obsolete `(R5)` marker from the named inventory entry.

## Scope

Delete the preceding space and `(R5)` from the `new-core-blocked` / `new-core-lockconflict` bullet in `bootstrap/_scaffold/SECURITY_MUTATIONS.md`. Preserve its behavior description, all other identifiers and the rest of the file. No scaffold behavior changes.

**Reuse.** N/A: no code added.

### Documentation / doctrine surface

The existing security inventory is descriptive prose under the high-risk scaffold surface; no governing doctrine changes.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Check consumers and pins, make the exact deletion and exercise its byte control. | Both required plan reviews and author response | Inventory edit and iteration evidence. |
| C2 | Independent code and Security Reviews, response and final integration. | C1 committed | Review records and wide Boundary B evidence. |

## Acceptance criteria

**C1.** The final inventory equals its parent after removing exactly the specified space and marker once. The safeguard description and all other identifiers remain byte-identical. Demonstrate that comparison rejects an additional changed byte. A live consumer or byte pin requiring the marker stops the edit for reassessment.

**C2.** Ordinary and separate Security Reviews assess the committed edit; required checks pass and wide Boundary B covers the final reviewed commit.

## Scope delta

**Scope delta**: preserved.

## Verification

`python tools/test_tiers.py for bootstrap/_scaffold/SECURITY_MUTATIONS.md` selects `bootstrap/tests/test_install_module.py`, `bootstrap/tests/test_security_leaf.py` and `bootstrap/tests/test_upgrade_lockfile_path_containment.py`. The first two cite the Class A inventory; the third reads it in its path-containment assertion. Search direct readers and byte pins with a known-positive control before editing; remap if paths change. Compare parent and edited bytes with only the one deletion permitted, and demonstrate rejection of an extra byte in a separate copy. Run the mapped iteration tests and `python scripts/claim_check.py`, `python scripts/link_check.py`, `python scripts/sync_doc_snippets.py --check` on the inventory, plus `python scripts/quality_gate.py --sub neutrality` and `python scripts/check_cairn.py`. The comparison and negative control are S2/S3; no runtime security proof is claimed.

Boundary C is independent targeted falsification, including separate Security Review. After review and fixes, run wide Boundary B on a clean unchanged final commit under canonical Python 3.13: mapped iteration and integration/workflow tests, owning families, known consumers, standing gates and byte control. Record SHA/range, interpreter, clean pre/post state, commands, counts, timing, tokens, non-pass dispositions and omissions. Combine overlapping final checks with other ready plans only on the same reviewed commit and without dropping coverage. No full certification run is authorized here.
