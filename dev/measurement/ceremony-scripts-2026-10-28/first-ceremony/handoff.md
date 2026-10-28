# Handoff: packet and launcher for candidate parent 38965e4a

**Result:** packet and launcher built from git objects at 38965e4a378e1cd89e8a35e2e47614ca362f53c3; all four checks pass.

- Packet SHA-256: `c046d864947779590c125900b71698da2752e0ca86e544735ac97bbb291608db`
- Launcher SHA-256: `f22bf72ca8f1da638e3a51a527bba48028391b4d7609af181bcc26df24493a04`
- Provenance line: `fresh-session build from git objects at 38965e4a; builder wrote nothing in the range; same vendor as reader`

I am a fresh same-vendor session that wrote nothing in the range. That is a statement; nothing here checks it.

## Members (blob digest at 38965e4a)
- bootstrap/REANCHOR_RUNBOOK.md `43ae37a83932a3be253f08509fa2df3feb3a0c8650003e194a02b8577333db90`
- bootstrap/reanchor-launcher.template.sh `a40375c702ecacc453ba9a6fff7582d71b82fe14440cf0611b74fd49ebd870aa`
- bootstrap/reanchor.sh `5bcde4bee5c286fe09d3047254e4f3f7b1e5970c4648dd84171673d24dcaa1a7` (also the artifact_sha256)
- bootstrap/tests/_gate_manifest.py `e4c25061dd422f890795200c6ce4924744fdfaa3f47053282265fc4402d09725`
- bootstrap/tests/_gate_preflight.py `bdf33a202d2a6b86e13c7e025c591c05cf7f4b4c441c3a9f009fa2f254a6bd5d`
- bootstrap/tests/_gate_reanchor.py `3cd5d39ec6b64296557bda4ee41d838158c40e89699fc6b3372f4c412466be7c`
- bootstrap/tests/_gate_transition.py `545625aea1d229d3977abd52118151477caf1bc5d87479d2e0a3cc08436bca17`
- bootstrap/tests/_oracle.py `afc9951ecbbc2693caba76ad14843d4d38560e1c524dddbad37e04e1c3896bed`
- bootstrap/tests/_oracle_activation.py `f8f94efa73eea79d6b366f280024d2bace4d13b4b111f12c65d9ae0f85c9d2c4`
- bootstrap/tests/_oracle_trust.py `725692f9ad21f1276532dcba7ae49ed307fbd9c18bfdc25212fb048de0c63f42`
- dev/.cairn/allowed_signers `8b7fa2f745f187cc06316732a27a2d9f552a6244d57393d95dd3e1a8e923c242`

## Checked (measured)
1. `cmp` of launcher.sh against the template with the slot filled: identical (SAME). No `@PACKET_SHA256@` remains.
2. A second packet from a separate Python script: byte-identical.
3. Each member digest equals the blob at X. The path list equals the template's `EXPECTED_PATHS` (eleven, sorted).
4. The launcher has no safe mode: every mode reads a real values file first. So I did not run it. I extracted its own `read_packet` and `parse_packet` text into a scratch harness: it accepted the packet. A tampered packet was refused.

Also: no control characters; longest line 118 bytes; files mode 0644, not symlinks.

## Not checked
- The launcher's later stages (resolve, extract, scan, stages 1 and 2).
- Whether the template or the closure files are safe.
- Candidate commit content; the reader's record commit changes only dev/ceremony-record.md, which is outside the closure (assumed from the instruction).
