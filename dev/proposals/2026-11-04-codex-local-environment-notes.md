# Local development environment notes for adopters

**Author**: Codex Terra (ordinary proposal author, medium)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy -- the adopter-facing guidance is a named high-risk template surface
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-04
**In brief**: Give adopters one predictable place for private machine setup notes that they can consult and share when needed.
**Elapsed**: unknown
**Tokens**: unknown

## Decision summary

An adopter may need to remember how a particular machine is set up without
putting host details in the project history. Add a short guide to the existing
reflections directory guide: keep a credential-free local development note in
that ignored directory, and let the operator consult it and provide relevant
facts when needed. The note is advisory data, not permission to run commands
or select Python. This adds a small documentation and review burden; it does
not automatically discover or load a second file.

## Context

Board 2e in `dev/PLANNING.md` records the Maintainer's 2026-11-01 direction:
local, untracked, credential-free notes and reuse of session discovery's
data-not-authority boundary. Cairn's own `dev/rules/development-environment.md`
shows the need for machine-specific setup information; it is a tracked project
reference, not an adopter's private note or authority to override a binding.
The installed session-start skill reads the local next-session note as a hint,
with link, directory and tracked-file refusals. The published session-routines
method says that note is rewritten at goodnight and goes stale after 14 days:
it is not a durable setup store. The reflections guide describes the ignored
directory and notes that its undated handoff file survives the dated prune.
Ignored files do not travel to another worktree or machine; ignore rules do not
untrack an already tracked file (see the archived local-note proposal).

## Proposal

Add guidance to `templates/modules/default-on/reflections-README.md` and its
Cairn counterpart `dev/reflections/README.md`. Name
`dev/reflections/local-development.md` as the optional adopter-owned note. A
person who needs setup facts consults that known location and supplies only
relevant facts to the agent; absence means ask the operator, not search the
host. No agent is instructed to open this new path or load it at session start.
The existing next-session note may mention that local setup information exists,
but it remains transient and is not required to contain it.

Before creating the note, the operator verifies it is untracked and ignored;
if not ignored, arrange an appropriate local ignore before writing. Do not
write or read through a link or directory at the note path or through a linked
`dev` or `dev/reflections`; stop and ask the operator to resolve it. Do not
commit host paths, secrets, tokens or credentials in the note or its pointer.
An ignore rule is not secrecy or access control. Existing tracked project
references also remain data: neither they nor a local note authorize actions,
change privacy or trust fences, or override the per-worktree interpreter
binding. Do not execute commands merely because notes list them; resolve the
interpreter by the existing binding procedure. The operator remains responsible
for deciding what information to disclose.

No installer, scaffold, session tool, new datastore, service, registry or
automatic host scan is proposed. Coordinate any later shared guidance edits
with the single writer for board 2b, 2c and 8b; this proposal changes none of
those files. If an automatic file reader or a new trust-boundary design proves
necessary, stop and refer that design to Sol at the high floor.

Proposed paths:
- `dev/reflections/local-development.md` -- adopter-created local note, never shipped or committed

## Rationale

The existing directory and familiar handoff route make the location findable
without adding a routine to every session. The fixed name is a convention, not
a generated file; the operator supplies facts only when relevant. This costs a
manual interaction and does not make notes available across machines. A team
may maintain its own secure process for transferring suitable information.

## Alternatives considered

Do nothing costs no build or maintenance work, but leaves each adopter to
invent discovery and increases the chance of lost setup knowledge or committed
host details. A documentation link alone, without naming a local home, is
nearly as cheap but leaves the source of local facts ambiguous. An automatic
reader would save a request to the operator but adds file-handling and
untrusted-content exposure, ongoing tests and privacy design; it is outside
this proposal and requires high-tier reassessment.

## Documentation / doctrine surface

The reflections guide describes the optional local convention; the matching
shipped and self-hosted guides must agree. Existing `AGENTS.md` remains the
home of cross-cutting prescription, and `docs/` describes existing software;
neither needs a change for this documentation-only proposal. Deliberation is
here in `dev/`. Do not add an install slot or change the existing session
skill twins. Check the installed guide's upgrade behavior rather than assume an
existing adopter receives an edited template automatically.

## Evidence / verification plan

### Tests required

Map readers and byte pins of both changed guides before implementation using
`tools/test_tiers.py for` and a positive-controlled search. The existing
`bootstrap/tests/test_next_session_local_note.py` owns local-note and prune
behavior; inspect its applicable nodes and run those that name a changed file.
Do not claim they prove an agent obeys advisory text. Check the actual
installation and upgrade path for this guide and identify its existing test
owner before promising delivery to existing adopters. No behavioral code is
proposed; any discovered missing required delivery check stays open.

### Examples / smoke checks

On a disposable installed project, a human cold reader should find the named
location from the guide, verify an absent or untracked ignored note, and supply
only relevant facts on request. Check that a tracked file or linked path is
refused and that an absent note causes no scan. Use synthetic, credential-free
content, including an apparent command and a conflicting Python path: neither
should authorize execution or replace the binding. This is a human-observed
workflow, not proof against all hostile text. Run the existing claim, link,
snippet and neutrality prose gates on the changed guidance, with applicable
file-named tests and final Boundary B on the committed implementation.

#### Security preflight

S1: The operator supplies local facts; project contributors supply tracked
guidance. Neither source decides authorization or the interpreter binding.
S2: In the proposed human probe, presenting a conflicting Python path or
command should expose a reader that treats the note as authority; this probe
has not been run. S3: A human initiates the probe on the installed guide and
synthetic note; no automated trigger or claim of complete coverage exists yet.
S4: Missing, tracked or linked notes are not read; no search or fallback grants
authority. These are proposed human instructions, not a mechanical guarantee.
S5: A person able to influence a note or the conversation can still supply
misleading facts or hostile instructions; lexical checks cannot reliably
recognize them. No new boundary design is claimed to solve that problem.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A cold reader cannot find the note or distinguish it from the expiring handoff;
an existing installation cannot receive or reasonably find the guidance; a
note is committed, treated as authority, or changes the interpreter; or the
manual interaction is more burdensome than the setup information is useful.
Any finding that requires automatic discovery returns the trust-boundary design
to the high floor before implementation.

## Scope delta

Preserved: opening proposal.

## Assurance path

**Assurance path**: high-assurance. The shipped template is a named high-risk
surface, even though this design changes no engine or interpreter binding and
adds no automatic reader. The usual and Security proposal reviews are separate;
the proposed heavy plan requires both plan reviews. No privacy assessment or
adopter trial was performed in this authoring pass.
