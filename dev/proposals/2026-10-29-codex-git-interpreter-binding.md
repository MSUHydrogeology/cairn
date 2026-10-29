# Keep the interpreter binding in Git's local directory

**Author**: Codex gpt-6.1-sol
**Status**: awaiting-review
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
