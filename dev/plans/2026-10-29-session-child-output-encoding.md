# Plan: Encode session child output

**Source proposal**: [dev/proposals/archive/2026-10-29-codex-session-child-output-encoding.md](../proposals/archive/2026-10-29-codex-session-child-output-encoding.md)
**Status**: revising-plan
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-29
**In brief**: Make captured session helper output safe to display while keeping multiline reports readable.

## Source proposal

The Maintainer accepted the revised proposal: encode child output at all three session helper boundaries, retaining report layout, failure behavior and identical shipped copies.

## Scope

Change `tools/session.py`, its shipped twin `templates/skills/_lib/session.py`, and `bootstrap/tests/test_session_binding_gate_and_printing_hold.py`. No doctrine surface changes. Search `rg 'encode_display|_prune_intents|_surface_intents|_run_evolution_infer' tools/session.py bootstrap/tests/test_session_binding_gate_and_printing_hold.py` found the existing encoder, three writes and exception controls. Reuse that encoder; add only the framing helper, not another escaping policy.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Frame and encode captured output; add controls | Both plan reviews and response | Twin code and tests |
| C2 | Verify and hand off | C1 committed | Stable evidence and independent code review; protected-test delta remains for v0.6 re-anchor |

## Acceptance criteria

**C1.** Capture child streams as bytes and decode using the same default encoding and strict error behavior as the current text-mode subprocess, without universal newline conversion. Malformed bytes retain the current decoding exception behavior. Split only literal LF, encode every segment with `encode_display`, and rejoin using parent-owned LFs. Terminate nonempty stdout lacking a final LF; never decode escapes or promote CR or Unicode separators to framing. Each helper encodes stdout on zero and nonzero returns, suppresses success stderr, and encodes reported nonzero stderr under its existing warning label. Preserve command selection, exit handling, skips and launch exceptions. Both source copies remain byte-identical.

For each helper, test both return branches with multiline output, a subsequent parent message, literal backslash escape notation, ESC/OSC, CR, C1, bidi and invisible characters. Assert ordinary text, safe rendering, warning and suppression behavior, and child invocation. Exercise real subprocess bytes through each helper, including nonzero stderr: bare CR and the CR in CRLF remain encoded, while LF separates lines. Cover `session-start` and handoff public paths or demonstrate equivalent real call-site coverage. A raw-write mutation at each helper must fail against an unmutated control. S2's mutations occur in C1; S3's person-run test command is in Verification. The independent scientific check is not applicable.

**C2.** Record clean-commit verification and non-passes; preserve the protected-test ceremony obligation for the v0.6 re-anchor. Do not claim that ceremony or historical anchor comparison occurred. Independent code review follows.

## Scope delta

**Scope delta**: preserved

## Verification

Boundary A: run `python -m pytest bootstrap/tests/test_session_binding_gate_and_printing_hold.py` for new real-child transport, hostile streams, branch and exception controls; `bootstrap/tests/test_session_kernel.py` for encoder and twin parity; `bootstrap/tests/test_session_routines.py` for session-start and handoff wiring and prune behavior; `bootstrap/tests/test_session_failsafe.py` for handoff and interpreter failure behavior; and `bootstrap/tests/test_session_binding_untracked.py` for real session-start and binding integration. Run each as `python -m pytest <file>`, splitting invocations if needed. Search `rg 'session.py|test_session' bootstrap/tests/test_session*.py` also finds `test_session_writes_contained.py` (write containment) and `test_session_start_drain_rules.py` (skill rules); neither owns changed output or capture behavior, so they are excluded. New controls exercise real child bytes through all three helpers and the public paths as stated in C1. Run the unmutated control and one raw-write mutant per helper in isolated copies.

Run `python scripts/check_cairn.py`, `python scripts/link_check.py`, `python scripts/sync_doc_snippets.py --check`, and `python scripts/quality_gate.py --sub neutrality` for Markdown links, cross-references, synced snippets and neutrality, and `python scripts/claim_check.py` on authored Markdown. The protected-test change joins the existing v0.6 re-anchor; follow `bootstrap/REANCHOR_RUNBOOK.md` for its applicable Maintainer ceremony, without performing or claiming it here.

Boundary B is **wide** for this security boundary: after the final implementation commit, run the mapped families, real-child controls, mutations and standing gates under canonical Python 3.13 on a clean unchanged commit. Record tested SHA and range, interpreter, pre/post state, commands, counts, elapsed times, non-pass dispositions and omissions, with **Certified by**: pending. Report the unmutated control and each helper's raw-write mutant separately. No full-suite certification is implied. Boundary C is independent targeted falsification by the code reviewer, who assesses the evidence and bounding.


## Plan review -- Codex (gpt-6.1-sol) -- 2026-10-29

```
Reviewed commit: 2d721690fa59131b321e2487f924314368fb6945
Target: opening plan against the accepted revised proposal
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**Foundations**:

1. **Should this happen as framed?** The framing and branch criteria deliver the accepted behavior, but the wide verification map is incomplete -- `dev/plans/2026-10-29-session-child-output-encoding.md` > Acceptance criteria and Verification.
2. **Best alternative.** Keep the shared encoder and literal-LF framing; map the relevant existing session test families and gates rather than introduce another framework -- `tools/session.py:189`, `bootstrap/tests/test_session_kernel.py`.
3. **What would show it wrong.** A mapped run that misses a public path or a failure-stream branch cannot establish the promised behavior -- `dev/proposals/archive/2026-10-29-codex-session-child-output-encoding.md` > Response > Evidence / verification plan.

**R1 -- blocking: complete the wide verification mapping.** The plan calls Boundary B wide but names only the printing test file and one twin-parity node. Other existing tests read the changed kernel or its shipped copy, including `bootstrap/tests/test_session_kernel.py`, `bootstrap/tests/test_session_failsafe.py`, and `bootstrap/tests/test_session_binding_untracked.py`. The plan does not identify the owning families, known integration and public paths, or applicable standing gates as required for wide verification (`dev/plans/_template.md` > Verification). Saying to preserve a mapping in future tests and evidence does not provide a mapping to review now. Search the readers and owning tests, specify the relevant families and gates with commands and properties, and explain any exclusions. This retains the accepted scope.

The criteria explicitly cover literal LF framing, literal escape notation, hostile characters, both return branches, suppressed successful stderr, and reported failure stderr at each helper. They also require real public-path coverage or an equivalent call-site mapping and per-helper raw-write mutations. These are appropriate to the accepted Response.

**Coverage:** read the committed plan, accepted proposal, template, three committed call sites, and a reader search. No implementation tests, mutations, Security Review, protected-test ceremony, or full suite were run; this pass does not assess the independent security obligation.


## Plan review -- Codex (gpt-6.1-sol, Security) -- 2026-10-29

```
Reviewed commit: a4399b820b9d1211014f4e33f45a36d06aa523a2
Target: plan against accepted revised proposal and ordinary plan review
Prior findings: none for this obligation
Assurance path: high-assurance
```

**Obligation**: Internal Security Review
**Tier**: Internal
**Findings**: raised
**Verdict**: REVISE

**Foundations**:

1. **Should this happen as framed?** The planned encoder and literal-LF framing preserve the accepted boundary, but child capture currently destroys CR before that boundary -- `tools/session.py:1791`, `tools/session.py:1821`, `tools/session.py:1855`.
2. **Best alternative.** Keep one encoder and one framing helper; preserve CR during capture and test real child bytes rather than add another escaping policy -- `tools/session.py:189`, this plan > Acceptance criteria.
3. **What would show it wrong.** A child emitting CR that becomes a new report line defeats the promised LF-only contract; the Python 3.13.13 subprocess probe below demonstrates this before encoding -- `tools/session.py:1792`, `tools/session.py:1825`, `tools/session.py:1859`.

**S1 -- blocking: preserve CR before framing and test the real transport.** All three calls use `subprocess.run(..., text=True)`. Its newline conversion turns child CR and CRLF into LF before a proposed framing helper sees the returned string. Splitting that string only on LF therefore still promotes child CR to framing. Stand-ins returning a `CompletedProcess` string containing CR bypass the conversion and could pass while the real path violates C1 and the accepted Response.

A read-only standard-library probe under canonical Python 3.13.13 launched a Python child using the same `capture_output=True, text=True, check=False` options. The child wrote stdout bytes `a\rb\r\nc\nd` and stderr bytes `e\rf`; the returned strings were `a\nb\nc\nd` and `e\nf`. This measures the capture behavior, not unimplemented framing code.

**Satisfier:** make capture preserve CR until `encode_display` handles it, without changing argv, status handling, skips or warning labels. Map real subprocess controls through each actual helper, including failure stderr: bare CR must remain an escaped segment character, CRLF must not silently discard CR, and literal LF must retain readable report separation. Keep stand-ins for branch coverage, ordinary Unicode text, literal escapes, ESC/OSC, C1, bidi and invisible characters, success-stderr suppression, and later parent messages. Define byte decoding and malformed-byte disposition if capture changes to bytes. This delivers existing accepted scope; it does not require a new subprocess framework.

**Covered:** claims and production path (#1–2), capture/framing completeness and failure visibility (#3–4), reuse and drift (#5–6: repeated the plan's named search plus `rg 'subprocess|stdout|stderr' tools/session.py`), lifecycle and scope (#7–8: accepted Response, C1/C2, and v0.6 ceremony deferral), and satisfier (#9 above). The ordinary review's wide-map finding remains separate. No scientific result is involved.

**Not covered / low confidence:** no implementation exists in this range; no tests, mutations, full suite, or protected-test ceremony were run. Printable false claims remain outside the encoder's protection, as the accepted preflight states. This security obligation remains open pending the author's response.


## Response to plan reviews -- Codex (gpt-6.1-sol) -- 2026-10-29

| Finding | Disposition |
|---|---|
| R1 | Accepted. Verification now maps owning families, public paths, standing gates and exclusions. |
| S1 | Accepted. C1 preserves CR through byte capture and strict default-encoding decoding, and requires real-child controls for each helper and failure stderr. |

The Security Review obligation remains open until a Security Review clears it; implementation has not begun.


## Plan review -- Codex (gpt-6.1-sol, Security) -- 2026-10-29

```
Reviewed commit: 5844b93b
Target: amended C1 and Verification against open S1 only
Prior findings: S1 from fd68aaca
Assurance path: high-assurance
```

**Obligation**: Internal Security Review
**Tier**: Internal
**Findings**: none remaining for S1
**Verdict**: CLEAR

**Foundations**:

1. **Should this happen as framed?** C1 now requires byte capture with CR preserved until encoding, and real-child controls through every affected helper including failure stderr; this closes the planned transport gap -- this plan > Acceptance criteria at `5844b93b`.
2. **Best alternative.** The revised byte capture, default-encoding strict decoding and existing encoder deliver the accepted outcome without a subprocess framework or second escape policy -- this plan > Acceptance criteria and Scope at `5844b93b`.
3. **What would show it wrong.** A real child's bare CR becoming framing, a CRLF losing its CR, or decoding diverging from existing text-mode strict behavior would fail the amended criteria; the mapped owner file is the person-run check -- this plan > Acceptance criteria and Verification at `5844b93b`.

**S1 cleared at plan level.** The revision supplies each requested satisfier: capture without universal-newline conversion, explicit preservation of current default encoding and strict decoding exceptions, real subprocess bytes through all three helpers and nonzero stderr, and retained LF readability and branch controls. The existing command, warning, skip and status contracts remain required. These are requirements for implementation, not a claim that implementation already passes. This pass clears only the open Security obligation; it does not repeat ordinary plan review.

**Covered:** S1's transport, test-path and decoding satisfiers against the amended operative cells and author response (#1–4, #6, #9); retained shared-encoder design, accepted outcome and review placement (#5, #7–8), all at `5844b93b` in this plan. No scope loss is introduced by these corrections.

**Not covered / low confidence:** no implementation, tests, mutations, broad suite, or protected-test ceremony were run. Correct default-encoding selection and CR preservation remain implementation and code-review checks. The ordinary verification-map finding is outside this clearance.
