# Finish the public contract repairs exposed by testing

**Author**: GPT-6.1 Terra (proposal author)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy — installer, oracle and portable-sweep surfaces
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-12
**In brief**: Handle damaged project data cleanly and finish the remaining correctness repairs found while replacing private tests.

## Decision summary

Some damaged project files make install or upgrade print a Python traceback.
The comparison tool also fails to ignore the two provenance fields it promises
to ignore. Repair these existing contracts, remove an unused Git parser and
correct stale references to tests. This adds no tool, command, dependency or
routine Maintainer task. One bounded implementation plan delivers board item
24, including its affected public-test gaps; release signing stays separate.

## Context

On committed `f8b02eea`, Python 3.13.13 reproduced three public CLI failures:
`upgrade --plan` raises UnicodeDecodeError for invalid UTF-8 in tracked
`AGENTS.md`, raises KeyError for a lockfile record missing its destination,
and plain installation raises PermissionError for an unreadable `.git/cairn`.
All returned 1 with tracebacks; targets were unchanged. The valid plan control
returned 0. The temporary reproducible script is
`/private/tmp/cairn-board24-public-repro-20261112/repro.py`.

The oracle documents normalization of only `cairn_version` and `cairn_commit`.
Its `_normalize` matches column-zero YAML keys, while the lock writer emits
JSON. A small generated-format comparison differing only in those fields
remained unequal. Source searches also found the sweep's `_git_subcommand`
and `ACCOUNTED_GIT_SUBCOMMANDS` referenced only by their definitions and tests.
The malformed non-list `files` variant has not been reproduced separately.

## Proposal

Deliver these existing promises without expanding the interfaces:

1. Install and upgrade refuse unreadable or malformed state with a bounded,
   useful diagnostic and a nonzero result, without a traceback, false success
   or unintended write. Cover invalid text, malformed lock structure and
   denied binding-directory access at their existing entry points. Keep the
   existing path, source-identity and containment checks; do not hide unrelated
   programming errors behind a broad catch.
2. Make the oracle's public comparison honor its existing, narrow provenance
   allowance for real lockfiles. Normalize only the two named top-level
   fields. Preserve differences in per-file hashes, nested fields, other
   metadata and other files; ambiguous or malformed input must not become an
   apparent match. Preserve unrelated byte differences rather than broadly
   reserializing both inputs into equality.
3. Remove the unused sweep parser and its unused command set after confirming
   no production consumer. Keep the active invocation accounting, admission
   matrix, unknown-command refusal and host evidence rules unchanged.
4. Correct stale guard names in the already identified source comments and
   shipped twins. Reconcile the affected held tests in the existing Promise
   worklist through actual public promises; add no interface merely to expose
   a private helper for testing. Required release guards remain intact.

Use existing functions, test homes and delivery machinery. Keep shipped twins
identical and update only the source records the normal development workflow
requires. No repin, re-anchor or historical certification is a plan prerequisite.

## Rationale

These are observable correctness repairs already on the v0.7 board. They let
the testing work finish against working contracts rather than preserving
private tests indefinitely. The continuing burden is a few public promise
checks, using existing parameterized refusal cases where possible.

## Alternatives considered

Keep the tracebacks and inert comparison allowance documented. That avoids
implementation work but leaves the recorded contracts broken and the related
test conversions unfinished. Adding new commands for private helpers would
increase the product surface without solving a user need.

## Documentation / doctrine surface

No new doctrine. Correct affected software descriptions and guard references,
preserve the existing runbooks' assurances, and extend the relevant changelog
entry. The implementation record names what was actually fixed and checked.

## Evidence / verification plan

### Tests required

Extend existing public install/upgrade refusal checks and the oracle's public
comparison workflow. Each must detect its concrete fault before the fix and
pass afterward; the ordinary valid workflow remains a control. Reuse current
sweep accounting checks to show removing dead code changes no actual admission
behavior. Keep one useful check per promise or distinct refusal class, without
per-test equivalence trials, new harnesses or permanent debugging tests.

### Examples / smoke checks

Use changed-file selections, prose gates for changed descriptions, twin checks
and the plan's final integration selection. Full release certification runs
once at its existing boundary, not after each repair.

#### Security preflight — five questions, answered in writing

1. Project files and Git administration paths are untrusted inputs; trusted
   source and policy still determine what may be read, written or compared.
2. The three recorded failures and provenance-only false difference are
   falsifiers. A changed content hash must still produce a real difference.
3. The plan binds checks to existing public entry points and actual inputs;
   deleting a test or unused name alone is not evidence of working behavior.
4. Error paths refuse safely. Normalization grants no extra provenance,
   path, signature or execution authority.
5. This does not protect against a compromised host or authenticate the
   scientific meaning of project content.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A malformed project reports success, a failed operation changes project data,
or a real content difference disappears from the oracle report.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance
