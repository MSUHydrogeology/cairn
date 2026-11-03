# Independent AST-pin packet read -- v0.6.1

## Foundations

1. **Should this happen as framed?** Yes, as a code-pin correction only.
   The source equals reviewed `1273e3f7`; ordinary `96f26e1d` and Security
   `58f3f563` accepted that code, not release readiness.
2. **Best alternative.** Use the existing two-fixture correction, without new
   machinery. Leaving pins unchanged retains both observed AST failures.
3. **What would show it wrong?** Unaccounted symbols, changed authority, or
   incorrect fingerprints. Raw-object comparisons and the real-tree probes
   below challenged those possibilities.

**Reader/model:** Codex inherited runtime (exact identifier unavailable), HIGH
Security / independent ceremony reader; fresh same-vendor reader, not the code
author. **Date:** 2026-11-03. **Elapsed at record:** approximately four minutes.
**Tokens:** unknown.

**Verdict: ACCEPT -- code-pin packet only. Findings: none.** This record grants
no agent authority to write trust records, sign, or release.

P's signature verified against P's raw signer roster and independently supplied
fingerprint `SHA256:8R549gtP0SJPaCWlQlausCtAbRBquXCIhbM6395ESsM`;
`dev/PLANNING.md` records its Maintainer installation. All 12 authority blobs
are byte-identical in P/C. P-authenticated, unchanged parser/builder helpers
regenerated the complete transaction byte-for-byte: 11 baseline digest/span
updates, two known-new rekeys; membership remains 169/105, with no additions,
deletions, duplicates or lockfile output. Prepared hashes, launcher substitution,
values paths, executable digests and public-key bytes were independently checked.

Python 3.13.13, disposable C copies, only proposed fixture outputs changed:
`bootstrap/tests/test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package`
and `bootstrap/tests/test_ast_attest.py::test_ast_gate_passes_over_the_full_scaffold_module_set`:
original fixtures **2 failed (0.21 s)**; proposed **2 passed (0.17 s)**;
one restored old `_LIVING_STATE_DSTS` digest **2 failed (0.20 s)**.

**Covered:** authenticated P, raw C, packet/transaction derivation, approved
source provenance and targeted falsification. **Not covered:** full certification,
prior-verifier collection, release security, host containment, key-away state,
historical AST review, actual pin installation, re-anchor or publication.

## Protocol Data

read-commit ed1478bee2d19b6c42954f50a745508741d40ea0
prior-anchor 67cdb805704425132de3122dacf384830734f5fa
packet-sha256 9b823fa8ad35dddd492e427ef0a1049cd3df18d9695b753ca767b433b898c56c
launcher-sha256 9de4bec43109d7390bd2f10e0ded8b7c26d564cd764248ea51f4e478158a0f28
member a2d69778bc92e94d0b0bf9c5e74c24b0cb1b1ec0892280ffe28ad031a1fef8b5 bootstrap/REANCHOR_RUNBOOK.md
member ebccccf7b7b0080099003f12a050dcb5c40b8952e14a9080b029d587fbac36d1 bootstrap/reanchor-launcher.template.sh
member 5bcde4bee5c286fe09d3047254e4f3f7b1e5970c4648dd84171673d24dcaa1a7 bootstrap/reanchor.sh
member 7a1aabccc3d3c80fdba9d86c23923e0af100c1bbd996a1b7bcab14aff819d3f4 bootstrap/tests/_gate_manifest.py
member f7bd99f71b279be7bcb612f6217fd505b84accd6e1dc5e681c800db48954bfd0 bootstrap/tests/_gate_preflight.py
member 093eed2b496df0a9d7ec989e68c5c9ff50d0a68f318e5200ac7d951844430538 bootstrap/tests/_gate_reanchor.py
member 545625aea1d229d3977abd52118151477caf1bc5d87479d2e0a3cc08436bca17 bootstrap/tests/_gate_transition.py
member afc9951ecbbc2693caba76ad14843d4d38560e1c524dddbad37e04e1c3896bed bootstrap/tests/_oracle.py
member 930f5230922c0167acf8fd1fe0be8439bd47f26ae0f6f584c4e1ad55f99ea141 bootstrap/tests/_oracle_activation.py
member 725692f9ad21f1276532dcba7ae49ed307fbd9c18bfdc25212fb048de0c63f42 bootstrap/tests/_oracle_trust.py
member 188fa76d82744be571bdc7ca91a43d605776b9df5ba0ac729e2cf22af66b8cc4 bootstrap/tests/fixtures/protected_test_roster.json
member 8b7fa2f745f187cc06316732a27a2d9f552a6244d57393d95dd3e1a8e923c242 dev/.cairn/allowed_signers
ast-transaction-sha256 dc16dc29f802253c8664f39c6ce2dd2de47a96ea35095bf97cddcaf12169ef97
