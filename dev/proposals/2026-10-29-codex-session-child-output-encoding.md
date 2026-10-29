# Encode session child output before it reaches the terminal

**Author**: Codex (Strategy, gpt-6.1-sol)
**Status**: awaiting-review
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
