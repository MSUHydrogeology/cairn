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
| Bounded descriptor-relative source reads | `tools/code_map.py::_read_at`, with its installed twin | Specialized caps and descriptor traversal; the Windows-native handle walk has passed ordinary and Security Reviews; final mapped verification remains due; `bootstrap/tests/security/test_code_map.py`. |
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
3. **Correctness / provenance trust.** A map is investigation evidence. Local-NTFS Windows
   traversal is implemented and reviewed; safe Git and the four-view pilot
   remain unfinished. No complete capability assessment is claimed.
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

### Filesystem assessment — 2026-11-06

At committed `166e5bc8`, the real `--release` command, run from a trusted copy
outside the inspected clean checkout under Python 3.13.13, mapped 925 files
in 12 top-level components. It read 7,625,307 Python-source bytes and found
7,944 definitions; command time was 24.418 seconds. Four metadata directories
were excluded as declared. No source was executed. This is a filesystem
assessment, not a release verdict or a complete capability assessment.

The neighbor search sampled 1,000,000 of 26,780,221 possible pairs; 25,780,221
were not compared. Its scores rank investigation leads, not equivalent code.
The existing public inventory comparison between `135ddd2f` and `ee8d4ab6`
recorded 136 test files at both endpoints and 312 additional decoded source
lines. It had no baseline timing report, so runtime growth is unknown. This
narrow observation does not measure total release growth or editing activity.

| Priority | Candidate and disposition | Preserving checks |
|---|---|---|
| 1 | Immutable test preparation rebuilt during global shuffling is a verified reuse opportunity, now being corrected in the existing suite plan. Keep mutable case state separate. | Existing ceremony refusal/digest/environment checks, reanchor key/ref isolation and upgrade collision snapshot control. |
| 2 | Session and scaffold containment helpers score 0.8063, but their standalone delivery and exception contracts differ. Keep their named homes; similarity alone does not justify a shared import. | `bootstrap/tests/test_session_writes_contained.py` and `bootstrap/tests/test_security_leaf.py`. |
| 3 | GitHub and GitLab label creators score 0.8481 but call different service interfaces. Keep the separately installed scripts rather than adding a common shipped dependency for similar request assembly. | `bootstrap/tests/test_issue_capture_bootstrap.py` exercises both scripts and delivery. |

The score-1.0 `dump` pair includes a historical ceremony-script snapshot;
retain that record rather than edit it to reduce apparent duplication.
Verbatim installed twins also remain intentional and fidelity-tested.

The safe-Git dependency, independent four-view comparison, broader endpoint
growth join and final mapped verification remain open in
[the architecture plan](plans/2026-11-05-architecture-and-reuse.md).
No unused-code, human-usability or release-readiness claim follows from this
assessment. Elapsed: command 24.418 seconds; analysis time unknown. Tokens: unknown.
