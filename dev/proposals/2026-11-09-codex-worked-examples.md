# Worked examples people can run and follow

**Author**: Codex Sol (Strategy)
**Status**: awaiting-review
**Review**: usual
**Proposed tier**: standard
**Plan review**: required(Internal)
**Opened**: 2026-11-09
**Target release**: v0.8
**In brief**: Expand Cairn's small examples into runnable walkthroughs showing a change, scientific evidence, adoption and a useful handoff.

## Decision summary

Build out `examples/` for v0.8 after the proposed repository reorganization
lands. A scientist should be able to run a small project, understand why its
change was made, see what evidence caught a mistake, and follow how work is
continued. Extend the existing examples rather than introduce a tutorial
framework or another sample application for every module.

Deliver four short walkthroughs using the existing greeting and water-budget
projects, plus an index that helps readers choose. The cost is keeping a small
set of executable commands and illustrative lifecycle records current. No new
routine human operation, external account, model service or full-suite trigger
is proposed. This is queued v0.8 work, not authorization to implement now.

## Context

`examples/minimal/README.md` traces a greeting change through a hand-copied
kernel, explicitly without an installation lockfile.
`examples/scientific-minimal/README.md` does the same for a synthetic monthly
water budget. Both have runnable code and self-tests, but their five-step
traces do not demonstrate a separate implementation plan, installed tools,
an upgrade or a handoff. Their commands and links also refer to today's
repository layout.

The [repository-layout proposal](2026-11-09-claude-repository-layout.md)
would move installation to `install/`, consolidate installed tools under
`dev/tools/`, and separate Cairn's tests and release machinery. It does not
propose moving `examples/`. New walkthroughs should teach that resulting
layout, not freeze the paths it intends to replace.

## Proposal

Deliver the following coherent example set in v0.8:

1. **Choose an example.** Add a short index under `examples/`: what question
   each walkthrough answers, prerequisites, commands, expected outputs and
   limitations. Distinguish runnable examples from installer templates and
   real-project case studies. Do not repeat the methodology manual.
2. **A small change without unnecessary ceremony.** Refresh the greeting
   example to demonstrate the current light lane: a short reviewed proposal,
   Decision, implementation and observable result, without an invented plan.
   Mark any narrated review or Decision as illustrative rather than claiming
   independent assurance from a sample record.
3. **A planned scientific change.** Extend the water-budget example with a
   compact, internally consistent proposal-to-plan-to-implementation trace,
   including code review, verification and archive. Keep the synthetic data,
   units, sign convention and tolerance rationale visible. Demonstrate both
   the closed-budget result and a deliberately unbalanced input that fails;
   explain that conservation alone does not validate a scientific model.
   Do not add a solver, calibration or new physical assumptions.
4. **Install, customize, upgrade.** Use a disposable copy of the scientific
   project and the real installer to show installation, one project-owned
   customization and an upgrade preserving it. Name an available local
   previous-release checkout as the upgrade input, with its revision and
   compatibility requirements. No silent download, tool installation or
   modification of the reader's real project. Contrast generated tool files
   with project-owned records; do not check in an entire installed tree.
5. **Leave and resume work.** Use that same scientific project to demonstrate
   a bounded handoff: completed change, unresolved question, next useful
   action and verification actually run. Explain the distinction between a
   smoke check and scientific/release evidence. Keep this tool-neutral; no
   agent service or conversation transcript is needed.

Keep these as short Markdown walkthroughs and small fixtures alongside the
two existing projects. Add files only where readers need a distinct runnable
input or record. No new framework, registry, dashboard or mandatory command.
Each walkthrough states whether its records are illustrative or produced by
the reproducible exercise; neither is presented as an actual research result.

Open one implementation plan only after the layout capability is delivered
and the local prior-release fixture is available. Its implementation, reviews,
checks and archive must then finish without waiting on another plan or a
human-run ceremony. Estimated work is two to four agent work sessions after
those prerequisites, uncertain mainly around upgrade-fixture maintenance.

## Rationale

Two small projects can show several workflows without multiplying applications
and dependencies. A scientist sees an outcome, its evidence and its limits,
not just completed paperwork. Generating the installed example during the
exercise avoids a second frozen copy of Cairn's shipped tools.

## Alternatives considered

- **Only repair existing links.** Cheapest, but still teaches neither installed
  behavior nor planning and continuation. Those repairs belong to the layout
  migration independently of this expansion.
- **One example per module.** More coverage, but more fixtures and duplicated
  explanation than a newcomer needs. Start with the four named workflows.
- **A larger realistic research application.** More domain depth, but adds
  scientific validation and dependency costs unrelated to learning Cairn.

## Documentation / doctrine surface

Description belongs in the example READMEs and a short discovery link from
the getting-started documentation after its v0.7 revision. Deliberation stays
here. This proposal adds no doctrine, installer behavior or installed files.
Use the final layout's paths and update affected links, not a parallel guide.

## Evidence / verification plan

### Tests required

Extend the existing example self-tests for the greeting and water-budget
promises. Run documented commands in disposable directories through real
entry points. Assert expected outputs and exit codes, including rejection of
the deliberately unbalanced input. An inverted flux sign must make an
independent expected-value assertion fail, not merely change another result
computed by the same function.

Use the existing installation/upgrade test homes for a focused example
workflow asserting that the stated customization survives. Reuse existing
fixtures; add no standalone example runner. Bound the check selection to
changed examples, documentation readers and the named integration consumers.
Do not add a full-suite run to each walkthrough or change certification.

### Examples / smoke checks

Reproduce every documented command from a clean local checkout, without an
agent account or network access. Record interpreter, input revision, outputs
and omissions. Run the applicable claim, link, snippet and neutrality gates.
A missing prior-release fixture is a missing prerequisite, not a passed
upgrade demonstration. Verify illustrative lifecycle records against current
templates without presenting them as real reviews or Decisions.

#### Security preflight

N/A: no trust boundary added or widened. Exercises use trusted local fixtures
and existing installation entry points in disposable directories; they add no
installer implementation, remote execution, credentials or automatic fetching.
If implementation requires any such boundary change, reassess before editing.

### Independent scientific check

Check a hand-calculated row against the water-budget residual, with units and
the storage sign shown independently of the implementation. Synthetic closure
and fault detection are the claims; no field-data accuracy claim is made.

## Signals the change is wrong

A reader cannot reproduce a stated result from the instructions; a wrong sign
or unbalanced input still passes; upgrade loses the documented customization;
or maintaining the examples requires copies of the installer or methodology.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: standard

This is an unreviewed v0.8 draft. The Maintainer requested no review yet.

Proposed paths:
- `dev/tools/`
