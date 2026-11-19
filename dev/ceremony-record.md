# Independent transition packet read -- v0.8

## Foundations

1. **Should this happen as framed?** Yes, as a layout transition only. The
   eleven changed authority files trace to path relocation or to the accepted
   layout plan's transition mode. -- `dev/plans/archive/2026-11-17-repository-layout.md`
   > "Layout transition".
2. **Best alternative.** Use the maintained `ceremony --transition` with layout
   evidence; no new machinery. Leaving the anchor at P keeps the old layout
   unsigned. -- `release/REANCHOR_RUNBOOK.md` > "First cut after the layout move".
3. **What would show it wrong?** A member, roster or launcher byte differing
   from raw C, a shrunk protected set, or a P signature not by the confirmed
   key. Raw-object comparisons below challenged each. -- `git show`, `shasum -a 256`,
   `git verify-commit`.

**Reader/model:** Claude Opus 5.5, HIGH Security / independent ceremony reader;
fresh reader, not the code author. **Date:** 2026-11-19. **Elapsed at record:**
approximately 20 minutes. **Tokens:** unknown.

**Verdict: ACCEPT -- transition packet only. Blocking findings: none.** This
record grants no agent authority to sign, move refs or release.

Checks: packet and launcher digests equal the inputs; the launcher equals C's
template with only the one `@PACKET_SHA256@` slot filled. All 12 members equal
raw C blobs and the layout evidence (digest matches); 11 differ from P.
`dev/.cairn/allowed_signers` is identical at P and C and holds only the
confirmed key. `release/repin.py` and the Python executable match the stated
digests. P (`e5b7fd0a`, the trusted anchor ref, no replace refs) verifies with
only the confirmed public key as allowed signer. The new anchor's roster is
C's `tests/fixtures/protected_test_roster.json`.

Non-blocking findings for the Maintainer:
- E7 in layout mode is P's raw scan functions driven by a wrapper in C's
  `release/repin.py`, which maps decision classes to new paths; it replaces
  P's own `scan-digest` entry. Planned; it rests on the reviewed repin bytes.
- `_gate_preflight.py` adds `_layout_stage`: an externally hashed context,
  accepted only in transition mode, with the legacy P manifest, a record-only
  tip and the reviewed roster digest. The report takes its scan from it.
- The phase-split allowance narrows (protected paths removed): stricter.
- Frozen globs and scanned new-file roots move from `scripts/`, `bootstrap/`
  to `install/`, `release/`, `dev/tools/`; `_oracle.py` gains old/new engine
  selection. Relocation.
- The launcher's `scan-digest` now lists the anchor's `tests` tree; it is not
  used for this cut.
- Roster: enforced lists 90/7/57 relocate one-to-one; none added or removed.
  Three protected tests were deleted before P; P's verifier reports them.
  Informational lists keep old paths.

**Covered:** packet, launcher, values interpreter, members, roster structure,
signer, the ten named authority diffs. **Not covered:** `_oracle_trust.py`
(unchanged), line-by-line runbook prose, full certification, release readiness,
host containment, key-away state, the prior verifier's 488 HOLD dispositions
(the Maintainer decides), executing any test.

## Protocol Data

read-commit ed893f0d90339598c58c89feeefd261e41d74e5e
prior-anchor e5b7fd0adb0b6d0402e89e2789f57c5f42045e62
packet-sha256 6448a3a0452d3b7402ce8674d6d247669c0547809c531c012484b97966fb3fb7
launcher-sha256 2b984f9fcce77407ddb552610fa50a7562c5f73ee7124412c8951b53b98ac37c
layout-evidence-sha256 de3aa23af8831567bb90606416e62f3ed333dc21cd837aba76eca99563256d97
member 8b7fa2f745f187cc06316732a27a2d9f552a6244d57393d95dd3e1a8e923c242 dev/.cairn/allowed_signers
member 8b6a7547b949f1527334948ed87c6c26cc6435bf6bf65abd29d5b531f034a35c release/REANCHOR_RUNBOOK.md
member a9f437fa1d17d9d1595370c7380250d9263ebc38eb3e574cc6995de100baee7c release/reanchor-launcher.template.sh
member e41010d0c9dad22b2ea0d456e2cb6c745daa284a58284c628d226daf802c0be0 release/reanchor.sh
member 79b58258bff21794a5f73d2258ba1608d717b8d0a97dd7bcebbdc684b5ebdb9f tests/_gate_manifest.py
member 8d647939cae9cc1cd3e9149cd37fd51d8a5928efb4942f11e18ffdfe7adcc172 tests/_gate_preflight.py
member 46a0bfe407e501e9cb277f455722c739aef4bc60bd78d7092431c59dd133348d tests/_gate_reanchor.py
member 495ecbab9fb5bbd2607434d880796a9f81f6e2308d82207ac972f5db6a0ae397 tests/_gate_transition.py
member 3fb76b01ee92f7b24c1b90a3fe7defbea5abc14eb5d64d9c4c8937ccd52f22da tests/_oracle.py
member 4afb36485d00f5f4cdf09155f7c50f80eed69c779a2b33e357e11dfd85abea27 tests/_oracle_activation.py
member 725692f9ad21f1276532dcba7ae49ed307fbd9c18bfdc25212fb048de0c63f42 tests/_oracle_trust.py
member 098734196db5962be8a11850c7481abdf8a52d53cd0f1b0d7e177305356f82e6 tests/fixtures/protected_test_roster.json
