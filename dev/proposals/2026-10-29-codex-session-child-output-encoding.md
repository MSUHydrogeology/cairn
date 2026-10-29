# Encode session child output before it reaches the terminal

**Author**: Codex (Strategy, gpt-6.1-sol)
**Status**: awaiting-decision
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-29
**In brief**: Encode captured output from session helper processes so project-controlled text cannot alter the terminal display.

## Context

`tools/session.py` and its byte-identical shipped twin,
`templates/skills/_lib/session.py`, already define `encode_display` as the single
terminal encoder. Three helpers capture child-process output and write the raw
text to stdout or through `_warn`: `_prune_intents`, `_surface_intents`, and
`_run_evolution_infer`. `_surface_intents` runs during `session-start` and the
full handoff; the other two run during the full handoff. Their children read
project-controlled coordination and incident data, so a fixed interpreter and
argument list do not make the returned text safe to print.

The `intent_list_run_failure`, `intent_prune_run_failure`, and
`evolution_infer_run_failure` cases in
`bootstrap/tests/test_session_binding_gate_and_printing_hold.py` replace the
subprocess with an `OSError`. They check that exception text is encoded, but do
not supply hostile text in a successful child's stdout or stderr. The queued
v0.6 correction in `dev/PLANNING.md` identifies the raw child-output gap; the
existing encoder and these three call sites confirm it is still present.

## Proposal

At each of the three helper call sites, pass captured stdout and any reported
stderr through the existing `encode_display` before writing it. Keep the
current command selection, exit-code handling, warning labels, and skip
behavior. Apply the same edits to both byte-identical source files. Do not add
an encoder, change interpreter resolution, or alter what either child runs.

## Rationale

The child output is data shown to a person, not a trusted terminal program.
Using the existing encoder applies the established control-character and
invisible-character policy at the last point before display. It keeps the fix
at the output boundary and avoids a second escaping policy.

## Alternatives considered

Leaving the output raw keeps today's formatting but preserves the queued
terminal-injection gap. Adding a separate escape table duplicates the existing
policy and risks weaker coverage. A shared subprocess framework would touch
more code than these three existing writes and is not needed to close this
finding.

## Documentation / doctrine surface

No doctrine or documentation change is needed. The change implements the
existing `encode_display` contract in executable code and its shipped twin.

## Evidence / verification plan

### Tests required

Extend `bootstrap/tests/test_session_binding_gate_and_printing_hold.py` with
successful-child controls for all three helpers. Have the stand-in return
ordinary text plus the existing hostile characters in stdout and stderr;
assert normal text remains visible, hostile characters are escaped, and the
subprocess call is reached. A control with raw pass-through restored must fail
the hostile-output assertion. Exercise `_surface_intents` through the
`session-start` path and the handoff helpers through their handoff path, or
show equivalent real call-site coverage in the reviewed mapping. Run the
owning test file. Retain
`bootstrap/tests/test_session_kernel.py::TestTheTwinIsByteIdentical::test_both_copies_match`
to prove the shipped copy is the tested copy. The protected-test ceremony
required by the current tree remains part of implementation verification.

### Examples / smoke checks

Run `python scripts/check_cairn.py` on the proposal and the scoped test
families from a clean committed candidate. No full suite is proposed at this
stage; the authorized certification point remains separate.

#### Security preflight

1. **S1 — Who supplied it?** The decision is whether captured stdout and stderr
   may be written to the terminal. Inputs are the `CompletedProcess` text from
   `intent.py` and `evolution_infer.py`, run with the resolved interpreter from
   fixed argument lists; their output can reflect project-controlled intent
   logs and incident trackers.
2. **S2 — Can it fail?** A stand-in child returns the existing hostile test
   string in each stream. The output assertion must fail if a raw write is
   restored and pass only when the actual call site encodes it.
3. **S3 — What fires it, over what?** A person runs
   `python -m pytest bootstrap/tests/test_session_binding_gate_and_printing_hold.py`;
   its stand-ins select each helper's captured-output path. The adopter invokes
   `python tools/session.py session-start` as shown in
   `templates/skills/session-start/SKILL.md`, and the designated operator runs
   `CAIRN_HANDOFF_OWNER=1 python tools/session.py session-end --handoff` as
   shown in `templates/skills/session-end/SKILL.md`. The former invokes
   `_surface_intents`; the latter invokes all three helpers. The test mapping
   must cover both public paths.
4. **S4 — Which way does it break?** Missing optional tools still produce the
   current skip note, and child failures still produce the current warning;
   their text becomes escaped display text. An encoding defect must not turn a
   child failure into a successful security result or change the exit status.
5. **S5 — Who still wins?** This assumes a project can influence child output
   through its data. Encoding prevents raw terminal controls and invisible
   characters from being interpreted, but it does not authenticate a child,
   validate its claims, or prevent misleading ordinary text.

### Independent scientific check

N/A: no scientific assumption or result is touched.

## Signals the change is wrong

The proposal is wrong if raw control or invisible characters still reach the
terminal from any of the three helper call sites, if ordinary child output is
lost rather than represented, or if the fix changes which child runs or how
its exit status is handled.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance


## Response -- Codex (Strategy, gpt-6.1-sol) -- 2026-10-29

**R1 — accepted.** Split only on literal LF, encode each segment with
`encode_display`, and join with parent-written LFs. Preserve report lines and
append a parent LF when nonempty stdout lacks a final LF. Keep CR and other
separators inside encoded segments; do not decode escapes or use `splitlines()`.

**R2 — accepted.** For each helper, cover zero and nonzero returns: encode
stdout in both; keep successful stderr suppressed; encode nonzero stderr under
the current warning label. Retain launch-exception controls.

## Context

The byte-identical `tools/session.py` and
`templates/skills/_lib/session.py` share `encode_display`, but three helpers
write captured child stdout and reported stderr raw. The children can reflect
project data. Current owner tests cover launch exceptions, not returned
streams; the v0.6 queue records this gap.

## Proposal

Add one framing helper: split only on LF, encode each segment, rejoin with
parent-owned LFs, and terminate nonempty stdout. Use it at all three sites;
stderr remains hidden on success and is encoded on failure. Preserve commands,
status handling, warning labels, skips, and twin parity.

## Rationale

Per-LF framing keeps reports readable while the encoder makes child text inert;
CR and Unicode separators are never promoted to framing.

## Alternatives considered

Whole-payload encoding hides report lines. `splitlines()` could trust child CR
or Unicode separators. A second encoder or subprocess framework adds needless
machinery; doing nothing leaves the display gap.

## Documentation / doctrine surface

No doctrine or documentation change; executable code applies the existing
display contract in both copies.

## Evidence / verification plan

### Tests required

Extend `bootstrap/tests/test_session_binding_gate_and_printing_hold.py` for
each helper: multiline stdout without a final LF followed by a parent message; zero and nonzero
returns; suppressed success stderr; encoded failure stderr. Include literal
`\x1b` notation, ESC/OSC, CR, C1, bidi and invisible characters. A raw-write
mutation must fail against a positive control. Cover both public paths and
retain `bootstrap/tests/test_session_kernel.py::TestTheTwinIsByteIdentical::test_both_copies_match`.
The test delta joins v0.6 re-anchor; that ceremony does not itself block
implementation. No historical anchor comparison is in scope.

### Examples / smoke checks

Run the owner tests and twin check on the committed candidate, plus
`python scripts/check_cairn.py` on authored Markdown. No full suite; authorized
certification remains separate.

#### Security preflight

1. **S1 — Who supplied it?** Captured `CompletedProcess` text comes from
   `intent.py` and `evolution_infer.py` under fixed argv and the resolved
   interpreter; it can reflect project data.
2. **S2 — Can it fail?** Restore a raw output write; the hostile-segment test
   must fail against its unmutated control. This is planned, not yet run.
3. **S3 — What fires it, over what?** A person runs
   `python -m pytest bootstrap/tests/test_session_binding_gate_and_printing_hold.py`.
   `python tools/session.py session-start` (the session-start skill) reaches
   `_surface_intents`; the designated
   `CAIRN_HANDOFF_OWNER=1 python tools/session.py session-end --handoff`
   reaches all three helpers. Tests cover both paths.
4. **S4 — Which way does it break?** Missing tools still skip; child failures
   still warn; success stderr stays hidden. Only displayed text changes.
5. **S5 — Who still wins?** Encoding blocks terminal controls, not false
   printable claims or malicious child execution.

### Independent scientific check

N/A: no scientific assumption or result is touched.

## Signals the change is wrong

Raw controls survive; CR or Unicode separators become framing; report lines
collapse or run into later messages; escapes are decoded; success stderr shows;
or warning/status behavior changes.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance

### Withdrawn / superseded commitments

Unspecified output framing is replaced by literal-LF segments for readable
reports and message separation. No scope outcome is withdrawn.


## Review -- Sol (gpt-6.1-sol) -- 2026-10-29

```
Reviewed commit: a764d5dae0dc8ed76250ceab47e9ef2f23a2fce5
Target: opening proposal
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Foundations**:

1. **Should this happen as framed?** Close the raw-child-output gap, but state
   the intended display layout before approval: the existing encoder makes
   ordinary report newlines literal escapes -- `tools/session.py:189`,
   `tools/session.py:1795`, `tools/session.py:1829`, `tools/session.py:1864`.
2. **Best alternative.** Keep the one encoder and add trusted output framing
   outside encoded child text; a subprocess framework adds no needed protection
   here, while doing nothing leaves raw display controls --
   `tools/session.py:110`, `tools/session.py:213`, `tools/session.py:1795`.
3. **What would show it wrong.** A representative multi-line report that loses
   usable separation from subsequent session messages, or a nonzero child whose
   stderr reaches the warning unencoded, defeats the intended outcome --
   `tools/evolution_infer.py:364`, `tools/session.py:1796`,
   `tools/session.py:1830`, `tools/session.py:1865`.

The proposal correctly treats child output as untrusted display data, keeps the
existing encoder, preserves subprocess selection and failure handling, and
requires the shipped twin to match. The raw stdout and conditional stderr
writes exist at all three named sites in the reviewed commit. The cited tests
exercise launch exceptions, not returned child streams
(`bootstrap/tests/test_session_binding_gate_and_printing_hold.py:598`).

**R1 -- blocking: specify framing for encoded reports.** The encoder escapes LF,
CR, tabs, backslashes and pipes as well as hostile invisible characters
(`tools/session.py:110`, `tools/session.py:213`). Applying it to the whole
stdout therefore removes the child's final newline and collapses multiline
reports. A read-only probe executing the encoder definitions from
`git show a764d5da:tools/session.py` transformed an evolution-report header,
blank line and suggestion line into one string containing three literal
`\x0a` escapes and no real line terminator. The next lifecycle message would
be written directly after that escaped tail. The actual child report is
multiline (`tools/evolution_infer.py:364`). "Ordinary text remains visible"
does not decide whether that result is acceptable.

**Satisfier:** state the intended representation and trusted framing in the
Response and derived plan. The smallest option is an encoded payload followed
by a parent-generated newline; if multiline readability is required, specify
how trusted separators are reconstructed without passing child controls raw.
Keep the single encoder. Add a representative multiline report followed by a
session message to the acceptance examples, asserting the chosen separation
and escaped hostile payload. No outcome needs to be removed.

**R2 -- non-blocking clarification:** explicitly require both zero and nonzero
return codes in the child-stream controls. Stderr is displayed only for
nonzero returns at all three sites; zero-return stand-ins carrying hostile
stderr cannot test those branches. The satisfier is a verification mapping
that reaches each conditional warning and also preserves successful-child
stderr suppression (`tools/session.py:1796`, `tools/session.py:1830`,
`tools/session.py:1865`).

**Coverage:** checked claims, entry-path wiring, encoder reuse, layout and
failure branches, source/test consistency, lifecycle placement and scope
against the named commit; no scientific surface is involved. This is design
review, not implementation verification. No full suite, Security Review,
protected-test ceremony, or historical trust-root reconciliation was performed;
the separately required Security Review remains open.


## Review -- Codex Security (gpt-6.1-sol) -- 2026-10-29

```
Reviewed commit: 19cd3fcd75a7895c68a5be7e13d12f07662c2c7f
Target: opening proposal and ordinary review
Prior findings: none for this obligation; ordinary R1/R2 remain with author
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: none
**Verdict**: ACCEPT

**Foundations**:

1. **Should this happen as framed?** Yes: captured child output crosses a real
   display boundary, and reusing the encoder removes terminal controls without
   changing executable authority -- `tools/session.py:1795`,
   `tools/session.py:1829`, `tools/session.py:1864`.
2. **Best alternative.** Preserve useful report lines by encoding each LF-delimited
   payload segment and writing trusted separators, if the author chooses that
   layout in response to R1; whole-payload encoding plus a trusted final newline
   is simpler but less readable -- `tools/session.py:189`,
   `tools/evolution_infer.py:364`.
3. **What would show it wrong.** A raw ESC, C1 control, CR or bidi override in
   displayed child data, or a formatting repair that decodes an encoded escape,
   defeats the boundary -- `tools/session.py:110`, `tools/session.py:213`.

The proposal's strongest property is placement: it treats returned text as
untrusted even when the command and interpreter are fixed. The three stdout
writes and nonzero-stderr branches bypass the existing encoder. The encoder
escapes both ESC and the C1 control range, covering terminal command introducers;
it also escapes carriage returns, backspaces and the enumerated invisible
characters. This protects terminal presentation, not truthfulness of printable
messages, child authenticity, or execution of a malicious project tool. S1/S5
correctly keep those claims separate.

A read-only AST probe of the encoder definitions from the reviewed commit used
an ordinary multiline header with tabs, CR, an ESC erase-display sequence, an
ESC clipboard-control sequence, a C1 introducer and a bidi override. Its result
contained printable escapes and no raw ESC, C1 or LF. This establishes both the
security mechanism and ordinary R1's formatting cost; it is not a live-terminal
experiment or implementation evidence.

**Implementation recommendation:** retain meaningful line layout without
weakening the encoder. If choosing per-line framing, split only on literal LF,
encode every resulting segment, and emit separators as parent-owned framing.
Do not use general escape decoding, weaken `encode_display`, or turn CR and
Unicode separators into trusted line breaks through `splitlines()`. Include a
payload containing literal backslash escape notation to prove it is never
interpreted. Add ESC/OSC and CR cases beside the existing C1/bidi/invisible
fixture; cover successful stdout and nonzero stderr for each helper, with a
normal multiline report and subsequent parent message. These recommendations
refine the proposed tests; ordinary R1/R2 still need their author dispositions.

**Coverage:** claims and trust boundary: named writes and encoder above; public
paths and exception-only test gap:
`bootstrap/tests/test_session_binding_gate_and_printing_hold.py:598`; layout and
failure behavior: ordinary R1/R2; scope and lifecycle: this proposal's security
preflight and assurance declaration. No scientific premise applies. No shipped
bytes changed, full suite ran, protected-test ceremony ran, or historical trust
root was reconciled. This clears this proposal's Security Review obligation;
implementation and plan security reviews remain separately owed.
