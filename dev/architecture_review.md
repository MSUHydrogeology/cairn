# Cairn Architecture Review

This is Cairn's current architecture record, using the selected module's five
lenses. It is not approval to change a trust boundary or a release verdict.

## Current Shape

The scaffold engine installs and upgrades the template tree. Installed tools
coordinate work through project records. Gate and oracle code control trust
ceremonies separately from ordinary lifecycle work. Published documentation
explains the method; adopter templates carry its operative instructions.

## Critical Helper Homes

| Contract | Owner | Limits and preserving checks |
|---|---|---|
| Session regular-file reads | `tools/session.py::_read_regular_bytes`, with its installed twin | Leaf identity/regular-file checks, not a byte cap or universal ancestor guard; `bootstrap/tests/test_session_writes_contained.py`. |
| Engine reads and destination writes | `bootstrap/_scaffold/security.py` | Engine-specific regular reads and guarded replacement; `bootstrap/tests/test_security_leaf.py` and `bootstrap/_scaffold/SECURITY_MUTATIONS.md`. |
| Bounded descriptor-relative source reads | `tools/code_map.py::_read_at`, with its installed twin | Specialized caps and descriptor traversal, unavailable on the tested Windows runtime; `bootstrap/tests/test_code_map.py`. |
| Terminal text | `tools/session.py::encode_display`, with its installed twin | One escape policy; wrappers may elide after encoding. `bootstrap/tests/test_session_kernel.py` and the real board output checks own this contract. |
| Git in trust ceremonies | `bootstrap/tests/_gate_manifest.py::_git` and the ceremony's pinned readers | Ceremony-specific authority, not a general-purpose helper. Follow the runbook and its gate tests. |
| General untrusted-repository Git reads | Not yet delivered: board item 2d | Its proposal is awaiting Decision. Existing gauge/session Git calls are not a safe replacement; Git-backed architecture work remains open. |

The engine leaf, session kernel and standalone collector have different import
and resource constraints. Do not merge their readers on name similarity.
Verbatim shipped copies are intentional; their owning tests check fidelity.
ASCII JSON or builtin `ascii()` output is not a competing terminal escape table.
The narrow owner-name check in `test_session_kernel.py` catches new forks of
`encode_display` and `_read_regular_bytes` in its listed runtime roots, not
renamed clones, unsafe bodies, every possible implementation or arbitrary code.

## Five-Lens Assessment

1. **Workflow coherence.** Trace scaffold, upgrade and session entry points
   independently. Shared helpers must not erase their different refusal rules.
2. **Data contracts.** Lock and install records are contracts; semantic changes
   need their existing integration and security checks, not only parser tests.
3. **Correctness / provenance trust.** A map is investigation evidence. Windows
   traversal, safe Git and the four-view pilot are unfinished; no complete
   cross-platform or capability assessment is claimed.
4. **Extensibility.** Reuse the existing module mapping and selected-module
   delivery. A new registry or orchestration layer needs a present consumer.
5. **Operational maturity.** Use the existing test-selection and timing records;
   slow tests and broad coverage are different questions. Release growth and
   consolidation evidence still belong to the active architecture and meter plans.

## Application Examples

Applying the shipped rubric's fictional cases: the legacy normalization case
calls for a behavioral comparison before reuse; the new direct workflow is
adequate without a plugin system; the mixed readers need contract comparison,
not unconditional deduplication. These are author applications for later review,
not human-trial evidence or measurements of an adopter.

## Release Assessment

Not completed. The filesystem map slice is available, but its Windows backend,
the safe-Git dependency, the independent four-view comparison, endpoint-growth
join and the plan's final reviews/checks remain open in
[the architecture plan](plans/2026-11-05-architecture-and-reuse.md).
Do not infer unused code, completed capabilities or release readiness from
symbols, neighbor scores or these example applications.
