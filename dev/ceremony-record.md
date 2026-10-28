# Ceremony record: reader, second re-anchor ceremony under the new design (the AST pin through repin)
# I am a fresh same-vendor session that wrote nothing in the range; this is a statement, nothing checks it.
# Reader: Claude Opus 5.5 (claude-opus-5-5), 2026-10-28. Range read: 2433453c (the anchor) to the read-commit below, three commits.
# The range changes six files: three prose files (CHANGELOG.md, dev/PLANNING.md, dev/plans/archive/ceremony-without-external-review.md), this record (the previous reader's version), and the two AST fixtures (bootstrap/tests/fixtures/scaffold_ast_baseline.json, scaffold_ast_known_new.json). All mode 100644. No code, test or closure file changed; all 11 closure blobs equal the anchor's.
# AST pin (000b0e9a, fixtures only): baseline 173 to 169 keys, the four deletions exactly the four constants dev/plans/archive/install-time-onboarding.md names and fa86e2cb removed from bootstrap/_scaffold/install.py; 21 entries change digest/span only; known-new 62 to 81 keys, 23 added, 7 rekeyed, 4 dropped. In a detached worktree of the read-commit (Python 3.13.13): _ast_attest.py verify --known-new ends "AST attestation OK" (169 symbols); test_ast_attest.py 30 passed. Control: the parent's fixtures make verify exit 1.
# Scan hits: none (0 hits, 0 paths line-scanned; not line-scanned: outside-coverage 4, frozen 1, cascade-mutable 1). Scan digest over anchor..read-commit dbac70a6980522636d511a551b9c9860b8c030b8a1f1a63a093201ecbe0c46f6. Control (shell=True planted in scripts/repin.py in a scratch clone) fired: 2 hits, process-start 1, shell-true 1.
read-commit 000b0e9a515f8fefea6590f65efe71fc15ddcdbb
packet-sha256 374b18cd2c8598957963ff021f5be6e82c2f13daaebc44825f0700c89807cada
launcher-sha256 c9079ff56fc696b669a37ce53444f25b11d901a6e85ae655533a8780a6612304
member 43ae37a83932a3be253f08509fa2df3feb3a0c8650003e194a02b8577333db90 bootstrap/REANCHOR_RUNBOOK.md
member a40375c702ecacc453ba9a6fff7582d71b82fe14440cf0611b74fd49ebd870aa bootstrap/reanchor-launcher.template.sh
member 5bcde4bee5c286fe09d3047254e4f3f7b1e5970c4648dd84171673d24dcaa1a7 bootstrap/reanchor.sh
member e4c25061dd422f890795200c6ce4924744fdfaa3f47053282265fc4402d09725 bootstrap/tests/_gate_manifest.py
member bdf33a202d2a6b86e13c7e025c591c05cf7f4b4c441c3a9f009fa2f254a6bd5d bootstrap/tests/_gate_preflight.py
member 3cd5d39ec6b64296557bda4ee41d838158c40e89699fc6b3372f4c412466be7c bootstrap/tests/_gate_reanchor.py
member 545625aea1d229d3977abd52118151477caf1bc5d87479d2e0a3cc08436bca17 bootstrap/tests/_gate_transition.py
member afc9951ecbbc2693caba76ad14843d4d38560e1c524dddbad37e04e1c3896bed bootstrap/tests/_oracle.py
member f8f94efa73eea79d6b366f280024d2bace4d13b4b111f12c65d9ae0f85c9d2c4 bootstrap/tests/_oracle_activation.py
member 725692f9ad21f1276532dcba7ae49ed307fbd9c18bfdc25212fb048de0c63f42 bootstrap/tests/_oracle_trust.py
member 8b7fa2f745f187cc06316732a27a2d9f552a6244d57393d95dd3e1a8e923c242 dev/.cairn/allowed_signers
