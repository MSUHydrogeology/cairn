# Keep the interpreter binding in Git's local directory

**Author**: Codex gpt-6.1-sol
**Status**: accepted
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-29
**In brief**: Keep the locally chosen interpreter outside the checkout so a copied project or patch cannot supply the program session tools run.

## Context

The scaffold writes `dev/.cairn/local-env.json`; `tools/session.py` reads its executable path and validates its shape and Git index status. `bootstrap/SAFETY.md` documents that an archive, patch, untracking operation or copied working folder can still plant an untracked binding. The check does not authenticate the executable. `dev/PLANNING.md` promotes moving the binding into `.git` to proposal work.

## Proposal

Store the binding in a Cairn-owned file under the **per-worktree Git directory**, resolved using Git, not by assuming `.git` is a directory. Each linked worktree has its own binding; the common Git directory is not the location. Install writes the current resolved interpreter there without overwriting an existing binding unless explicitly forced. The session reader uses only that location, retaining the existing interpreter schema, path checks, warnings and safe fallback behavior where applicable. It never reads or automatically migrates the old checkout binding: an operator who wants a binding re-runs the install with their intended interpreter. A missing binding uses the current interpreter with guidance, as today.

Git directory discovery must work from the target repository, with Git environment overrides scrubbed; failure, an unavailable repository, an unsafe destination or ambiguity must not cause a write elsewhere or a read of the legacy file. Verify the directory and binding are not reached through unsafe links; refuse unsafe or unreadable state before executing the named program. Preserve the existing refusal for a tracked in-project executable. Define exact handling of Git's normal linked-worktree `.git` pointer separately from a link in the binding path. Do not delete old files automatically. A checkout cannot choose the new binding through a tracked `.git` entry or a redirected Git environment; control of the local Git directory or interpreter remains trusted operator authority.

## Rationale

Git's per-worktree private directory separates this executable choice from files delivered by ordinary checkout, patch or archive. Explicit rebinding avoids silently granting authority to the old file. Per-worktree storage avoids one worktree's install changing another's interpreter. This reduces the documented checkout-origin risk, not the risk of a malicious local operator or executable.

## Alternatives considered

Keep the current index check: it avoids migration, but the documented untracked-file routes remain. Automatically copy the old binding: it preserves convenience but carries precisely the untrusted input across the boundary. A shared Git directory saves repeated setup but couples worktrees with potentially different environments.

## Documentation / doctrine surface

Update descriptive install, upgrade and security guidance in `bootstrap/UPGRADE.md` and `bootstrap/SAFETY.md`, and relevant reader and scaffold guidance. Update the governing high-risk surface description in `AGENTS.md` and any shipped governing equivalent through its normal routing; retain the old ignore rule where needed so legacy absolute paths do not become accidentally staged. Inventory all references before implementation. No scientific doctrine changes.

## Evidence / verification plan

### Tests required

Map readers, writers and consumers from the tree in the plan. Exercise actual install and session entry points in `bootstrap/tests/test_skills_install.py`, `bootstrap/tests/test_session_binding_untracked.py`, and `bootstrap/tests/test_session_binding_gate_and_printing_hold.py`, updating or replacing affected assertions. Cover normal repositories and linked worktrees with distinct bindings; no repository, failed or hostile Git discovery; unsafe links and unreadable paths; malformed, stale and tracked executable cases; non-clobber and explicit force; and an old malicious binding that cannot launch, including after archive or patch delivery. Check that a new binding does launch the locally selected executable and that unsafe destination writes do not escape. A failure to distinguish those cases falsifies the design. Include existing owning security and install checks found by the inventory, and the applicable standing gates. The reviewed plan sets the exact nodes and wide Boundary B mapping; certification remains a separate authorized event.

### Examples / smoke checks

Run `python scripts/check_cairn.py` and the applicable claim, link, snippet and neutrality gates for changed prose, plus an install and session smoke in disposable normal and linked-worktree repositories. No full-suite run is requested here.

#### Security preflight

* **S1:** The operator supplies the interpreter and local Git administration state; a checkout supplies repository content and may contain the legacy binding. Git returns the per-worktree directory; neither that response nor the executable is authenticated against an independent trust root.
* **S2:** The planned discriminating test plants a marker executable in the old binding and fails if session execution creates its marker; it has not yet been run against the proposed implementation. Also mutate the new-path selection to read the old path and show the test fails during implementation.
* **S3:** The planned install/session tests invoke their real entry points and cover the stated normal, linked-worktree and hostile-input cases; the plan must identify exact commands and reconcile them with the revised adopter-facing guidance, which does not yet exist.
* **S4:** Missing binding falls back with guidance; malformed or unsafe state refuses before launch. Discovery errors cannot silently select a checkout path or permit an uncontrolled write. A stale executable retains the existing warned fallback.
* **S5:** A checkout or patch author who cannot write local Git administrative state is in scope. Someone who can alter that state or the selected executable can still choose what runs; neither shape validation nor this relocation authenticates it.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A delivered checkout can redirect the selected binding, a linked worktree changes another's interpreter, a normal supported installation cannot rebind without manual repair, or the safety checks prevent routine use without a proportionate remedy.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance.


## Review -- Codex gpt-6.1-sol -- 2026-10-29

```
Reviewed commit: dd42c5603f8a48332387243d502ed425fe5d660b
Target: opening proposal
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Foundations**

1. **Should this happen as framed?** Yes to separating executable selection from ordinary repository content; revise the installation and delivery claims before accepting the contract -- `bootstrap/SAFETY.md`, interpreter-binding residual-risk section.
2. **Best alternative.** Using the current interpreter exclusively removes the binding reader and migration burden, but loses persistent environment selection when shell activation is absent; retaining that benefit justifies a small local binding -- `bootstrap/_scaffold/install.py::write_local_env`.
3. **What would show it wrong.** A routine first install cannot complete, a nested target writes its parent's binding, or a delivered folder still selects an executable despite the advertised protection -- `bootstrap/tests/test_skills_install.py::scaffolded`, proposal Signals section.

The strongest benefit is practical: a patch or checkout cannot silently turn a
local environment preference into a command launcher. Per-worktree storage also
keeps independent environments independent. Avoiding automatic migration is the
right default; re-running install needs a precise, usable rebinding path.

**U1 -- blocking: settle the repository-less and nested-target install contract.**
The existing `scaffolded` fixture installs successfully before `git init`;
`test_installed_cli_runs_read_only` initializes Git afterwards. The proposal
requires a repository for the new writer without saying whether ordinary install
now fails, succeeds without a binding, or initializes Git. Git discovery can
also find an ancestor repository when the target is merely its subdirectory.
“From the target” does not establish that the discovered repository belongs to
that target. **Satisfier:** specify first-install and nested-target behavior,
including the visible result and exact later rebinding step. Require tests for
both through scaffold `main`, proving no ancestor binding is changed. This
preserves the outcome; it makes its prerequisites explicit.

**U2 -- blocking: narrow the delivered-folder claim accurately.**
The In brief promises that a “copied project” cannot supply the program, while
the Rationale correctly limits the separation to ordinary checkout, patch and
archive. Copying a working folder including its Git administration directory
copies the new binding too. `bootstrap/SAFETY.md` explicitly includes copying
the whole working folder among today's five routes. **Satisfier:** distinguish
content-only delivery from delivery of Git administrative state in the current
contract and revised safety guidance; record the latter as a remaining trust
assumption, including linked-worktree pointer delivery. Do not describe all
five routes as closed. This corrects the claim; accepting the residual belongs
to the Maintainer.

**U3 -- blocking: make Windows coverage explicit.**
Both named binding test modules skip the entire module on Windows because their
stand-in interpreter is a shell script. Naming those files does not cover new
Git-directory discovery, junction/reparse handling, or native path behavior on
Windows. **Satisfier:** require portable production-entry tests and state which
native-platform evidence is required before implementation acceptance; retain
an explicit gap for any unsupported link case.

**Covered:** claims/design/failure behavior/domain scope: U1–U3; production
paths: the cited install fixture and both binding modules; consistency/drift:
`bootstrap/SAFETY.md`, `bootstrap/UPGRADE.md`; lifecycle: proposal security and
plan declarations; satisfiers: each finding above. **Not covered / low
confidence:** no implementation exists to execute; no native Windows or HFS+
run; no full suite; executable provenance and Git-administration compromise
remain outside this usual pass. The separate Security Review remains open.


## Review -- Codex gpt-6.1-sol Security -- 2026-10-29

```
Reviewed commit: f413f3415d43ca21076d9a095bd74253b47c47a3
Target: opening proposal and usual review
Prior findings: none for this obligation
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE

**Foundations**

1. **Should this happen as framed?** Move the binding, but distinguish trusted Git administration from delivered content before claiming the boundary closes -- `bootstrap/SAFETY.md:275-309`.
2. **Best alternative.** Always using the running interpreter eliminates this executable-selection file; retain a binding only for persistent environment selection without shell activation -- `tools/session.py:947-993`, `bootstrap/_scaffold/install.py:435-467`.
3. **What would show it wrong.** A nested target consumes its ancestor's binding, or an admitted Git pointer selects checkout-owned state, defeats the intended separation -- proposal Proposal and Security preflight S1/S5.

The strongest version separates a useful machine-local choice from ordinary
project content without automatically promoting the old, unauthenticated file.
Per-worktree storage is appropriate: sharing through the common directory would
make independently installed environments interfere. Explicit rebinding and
keeping the legacy ignore rule are sound.

**S1 -- blocking: state where administrative authority begins.** Agree with
U1/U2: “from the target” and “unsafe links” do not yet specify whether a
repository subdirectory, a nested repository, or a regular `.git` pointer is
accepted. Git's answer identifies a directory; it does not prove an operator
created it. A copied directory including administration or a delivered worktree
pointer still supplies administrative authority. The opening summary's copied
project claim therefore exceeds S5's threat model. **Satisfier:** define the
accepted relationship between install/session root, worktree root and private
Git directory; explicitly distinguish normal linked-worktree pointers from
untrusted delivered administration. State whether external separate Git
directories and submodules are supported or visibly refused. Require real
entry-point cases proving no ancestor binding is consumed or changed, no
content-only delivered file becomes authority, and copied administration
remains an explicit residual rather than a closed route. This specifies the
boundary; it does not authorize dropping an outcome.

**S2 -- blocking: give refusal and containment an observable contract.** The
proposal promises both existing fallbacks “where applicable” and refusal of
unsafe or unreadable state. Today's missing-file shortcut precedes the link
and index checks (`tools/session.py:995-997`); copying that order could classify
a dangling binding link as absence. The existing writer confines writes to the
target (`bootstrap/_scaffold/install.py:462-466`), whereas linked-worktree
administration normally lies outside it. **Satisfier:** distinguish true
absence from dangling links, wrong file types and unreadable state before
fallback, and define containment against the verified per-worktree directory,
without broadly relaxing the scaffold's existing target guard. Require
non-clobber and force cases for unsafe existing destinations, with no escaped
write or selected-executable launch. As U3 notes, portable tests must not all
skip Windows; state native junction/reparse evidence and any remaining gap.

**Coverage:** claims, design, fail-closed behavior and scope: S1/S2; production
path and consistency/drift: cited reader/writer and safety text; lifecycle:
required separate Security plan pass; satisfiers: above. Scientific validity:
not applicable. **Not covered:** implementation does not exist; no executable
probe, native Windows/HFS+ run or suite was performed. Git executable provenance,
same-user races and compromised local administration are not authenticated by
this relocation. The Security obligation remains open pending these satisfiers.

## Response -- Codex gpt-6.1-sol -- 2026-10-29

U1/S1: accept; specify roots and installation. U2/S1: accept; copied administration remains a risk. U3/S2: accept; require native Windows evidence and safe destination handling.

## Current contract

Move the binding to a Cairn-owned file in each worktree’s Git administrative directory, separate from checkout content, patches and content-only archives. Never read or migrate the old binding; retain its ignore rule and instruct operators to rerun install with their chosen interpreter.

For both install and session, Git discovery must identify the exact supplied project root as its worktree root, not an ancestor. Verify this using a scrubbed Git environment. A normal repository, linked worktree, separate Git directory and submodule are supported when Git identifies that exact root and its per-worktree administrative directory. Normal Git file pointers are permitted, not filesystem links or reparse points in the pointer or binding path. Ambiguous or unsafe discovery refuses access with guidance. Copied `.git` administration or a delivered pointer can still supply a binding. Operators must trust that administration and rebind after receiving it from an untrusted source. Same-user races and executable provenance remain outside this boundary.

An install into a non-repository target succeeds without a binding, reports that fact and explains how to initialize Git and rerun the install using the intended interpreter. A nested target without its own repository behaves likewise and never accesses its ancestor binding. Session without a repository uses the current interpreter with explicit guidance; an actual discovery error or unsafe state refuses, not a silent fallback. Re-running install after Git initialization writes the binding; existing bindings are preserved unless forced, without overriding safety.

Inspect path components without following links; only true absence falls back. Dangling links, wrong types, unreadable state and unsafe path components refuse before launching the selected program. Preserve strict schema, executable shape and tracked in-project executable checks; a stale executable retains its warned fallback. Writes are confined to the verified per-worktree administrative directory using a dedicated safety check, without relaxing the scaffold's target-tree write guard. No unsafe destination is overwritten even under force.

Inventory readers, writers and documentation; update `AGENTS.md`, its shipped equivalent, `bootstrap/UPGRADE.md` and `bootstrap/SAFETY.md`. Correct the copied-folder claim. The plan maps wide Boundary B and standing gates. Exercise real scaffold and session entry points for normal, linked, separate-directory and submodule repositories, non-repository and nested targets, old malicious bindings, hostile Git environment, unsafe destinations with and without force, and valid, malformed, stale and tracked executables. Prove ancestor isolation, containment, refusal before launch and worktree independence. Use portable tests that run on Windows, not only shell-script fixtures. Native Windows evidence must cover discovery and junction/reparse handling before implementation acceptance; explicitly record any unsupported link case and keep a required case open if it cannot be checked. Run prose and applicable standing gates; certification is separate.

Security preflight: the operator supplies Git administration and the executable; project content may supply the legacy file. The old-binding marker test must fail when selection is deliberately redirected to it, and has not yet been run. The plan maps commands to revised guidance. Missing state falls back only as specified; unsafe and unreadable state refuses. Control of trusted administration or the executable still wins. No scientific assumption is touched. Redirection, interference or failed rebinding falsifies the design.

**Scope delta**: preserved. Copied administration remains a residual for the Maintainer to judge.

**Assurance path**: high-assurance; usual and Security Reviews and Internal plus Internal Security plan review remain required.

### Withdrawn / superseded commitments

The opening summary overstates copied-project protection; copied administration remains trusted input.


## Review -- Codex gpt-6.1-sol Security -- 2026-10-29

```
Reviewed commit: 734d88db5ba276d17f550cf34b63b420c6faace9
Target: Response, Current contract and withdrawal ledger
Prior findings: S1, S2
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: none
**Verdict**: ACCEPT

**Foundations**

1. **Should this happen as framed?** Yes: the revised boundary separates checkout content from explicitly trusted Git administration and no longer claims protection from copied administration -- Current contract, paragraphs 1–2.
2. **Best alternative.** Always use the running interpreter; the retained binding buys persistent environment choice, now with explicit repository prerequisites and safe rebinding -- Current contract, paragraphs 1–3; `tools/session.py:947-993`.
3. **What would show it wrong.** Ancestor access, redirected writes or launch from an unsafe binding falsifies the contract; the required entry-point cases now name those observations -- Current contract, paragraphs 3–5.

**S1 closed at proposal stage.** The contract requires exact worktree-root
identity; explicitly supports linked, separate-directory and submodule roots;
and distinguishes absent repositories from discovery errors. Nested targets
cannot consume or change ancestor bindings. Copied administration and delivered
Git pointers are explicitly trusted inputs, not authenticated by discovery.
The withdrawal ledger correctly replaces the opening overclaim without
pretending the residual was closed. The Maintainer still judges that residual.

**S2 closed at proposal stage.** True absence is distinct from dangling links,
wrong types and unreadable state. Force cannot override destination safety.
Containment uses a dedicated administrative-directory guard and leaves the
scaffold's target guard intact. The contract requires portable entry-point
tests plus native Windows discovery and junction/reparse evidence before
implementation acceptance; an unmet required case stays open.

**Coverage:** discovery, trust, containment, absence/refusal, copied-state claims,
portability and withdrawal accounting: the cited revised contract. No new
blocker found within this obligation. **Not covered:** no implementation exists
to establish those properties; no executable probe, suite or native-platform
run was performed. Executable provenance, trusted-administration compromise
and same-user races remain explicit assumptions. This clears the proposal
Security obligation only; plan and implementation evidence remain owed.


## Response -- Codex gpt-6.1-sol -- 2026-10-29

The Security Review closes S1 and S2 with no new findings. The contract is unchanged; copied administration remains a Maintainer decision.

## Current contract

Move the binding to a Cairn-owned file in each worktree’s Git administrative directory, separate from checkout content, patches and content-only archives. Never read or migrate the old binding; retain its ignore rule and instruct operators to rerun install with their chosen interpreter.

For both install and session, Git discovery must identify the exact supplied project root as its worktree root, not an ancestor. Verify this using a scrubbed Git environment. A normal repository, linked worktree, separate Git directory and submodule are supported when Git identifies that exact root and its per-worktree administrative directory. Normal Git file pointers are permitted, not filesystem links or reparse points in the pointer or binding path. Ambiguous or unsafe discovery refuses access with guidance. Copied `.git` administration or a delivered pointer can still supply a binding. Operators must trust that administration and rebind after receiving it from an untrusted source. Same-user races and executable provenance remain outside this boundary.

An install into a non-repository target succeeds without a binding, reports that fact and explains how to initialize Git and rerun the install using the intended interpreter. A nested target without its own repository behaves likewise and never accesses its ancestor binding. Session without a repository uses the current interpreter with explicit guidance; an actual discovery error or unsafe state refuses, not a silent fallback. Re-running install after Git initialization writes the binding; existing bindings are preserved unless forced, without overriding safety.

Inspect path components without following links; only true absence falls back. Dangling links, wrong types, unreadable state and unsafe path components refuse before launching the selected program. Preserve strict schema, executable shape and tracked in-project executable checks; a stale executable retains its warned fallback. Writes are confined to the verified per-worktree administrative directory using a dedicated safety check, without relaxing the scaffold's target-tree write guard. No unsafe destination is overwritten even under force.

Inventory readers, writers and documentation; update `AGENTS.md`, its shipped equivalent, `bootstrap/UPGRADE.md` and `bootstrap/SAFETY.md`. Correct the copied-folder claim. The plan maps wide Boundary B and standing gates. Exercise real scaffold and session entry points for normal, linked, separate-directory and submodule repositories, non-repository and nested targets, old malicious bindings, hostile Git environment, unsafe destinations with and without force, and valid, malformed, stale and tracked executables. Prove ancestor isolation, containment, refusal before launch and worktree independence. Use portable tests that run on Windows, not only shell-script fixtures. Native Windows evidence must cover discovery and junction/reparse handling before implementation acceptance; explicitly record any unsupported link case and keep a required case open if it cannot be checked. Run prose and applicable standing gates; certification is separate.

Security preflight: the operator supplies Git administration and the executable; project content may supply the legacy file. The old-binding marker test must fail when selection is deliberately redirected to it, and has not yet been run. The plan maps commands to revised guidance. Missing state falls back only as specified; unsafe and unreadable state refuses. Control of trusted administration or the executable still wins. No scientific assumption is touched. Redirection, interference or failed rebinding falsifies the design.

**Scope delta**: preserved. Copied administration remains a residual for the Maintainer to judge.

**Assurance path**: high-assurance; usual and Security Reviews and Internal plus Internal Security plan review remain required.

### Withdrawn / superseded commitments

The opening summary overstates copied-project protection; copied administration remains trusted input.

## Decision -- Anthony Kendall (Maintainer) -- 2026-10-30

**ACCEPTED, as revised.** The Maintainer's authorization, quoted **verbatim and visually isolated**:

> "Accept all 7 proposals as revised."

