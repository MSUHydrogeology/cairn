# Keep the interpreter binding in Git's local directory

**Author**: Codex gpt-6.1-sol
**Status**: revising
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
