# Protect nested Git data during upgrade

**Author**: Codex GPT-6
**Status**: awaiting-review
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-29
**In brief**: Refuse upgrade paths into nested Git data so a staged upgrade cannot plant a Git hook.

## Context

The project path guard in `bootstrap/_scaffold/upgrade.py` rejects `.git` only as the first path component. The independent review in `dev/plans/archive/2026-10-26-code-review-lockfile-path-findings.md` F2 reports that a crafted review area applied `sub/.git/hooks/post-merge`, and a lockfile destination `sub/.git/description` was replaced. A hook is a program Git can run. The same review measured an any-component guard against its owner tests; its Windows trailing-dot and space concern was reasoned, not run. `dev/PLANNING.md` records the queued issue. Existing guidance in `bootstrap/UPGRADE.md` promises root `.git` protection, so this is a contract expansion.

## Proposal

For project paths supplied by the lockfile or staged review metadata, refuse any path component equivalent to `.git` after case folding and stripping trailing ASCII dots and spaces. Apply the rule at the existing project-path guard, including destination and base-cache paths and staged names, before reads or writes. Keep the Cairn source-tree rule unchanged. Preserve legitimate lookalikes such as `.gitignore`, `.github`, and `.git-notes.md`. Refuse with an actionable diagnostic; recovery is to remove or correct the offending lockfile record or discard the untrusted stage and create a fresh one, without modifying Git data. Do not claim protection against a concurrent hostile filesystem writer.

## Rationale

A nested repository's Git data is as sensitive as the root's. One guard covers its existing project-path callers, including the independently demonstrated staged and lockfile paths, rather than protecting only a hook spelling. Normalizing trailing dots and spaces also addresses names treated as equivalent on Windows; the implementation must verify the rule without claiming a Windows run that did not happen.

## Alternatives considered

Doing nothing retains the demonstrated hook write. Rejecting only hooks leaves configuration and other Git data exposed. Rejecting only exact lowercase `.git` leaves case variants and Windows aliases; rejecting all names beginning `.git` would unnecessarily block ordinary files.

## Documentation / doctrine surface

Update `bootstrap/UPGRADE.md` to describe the expanded refusal and recovery. This is descriptive software guidance; deliberation remains in `dev/`, following `docs/DOCUMENTATION_PLAN.md`. No doctrine change is proposed.

## Evidence / verification plan

### Tests required

Add behavioral coverage in `bootstrap/tests/test_upgrade_lockfile_path_containment.py` and its owning upgrade tests. Through public upgrade commands, exercise lockfile `dst` and `base_cache` and crafted review-area names, including nested hooks and Git data, case variants, trailing-dot and space variants, unchanged protected data and metadata on refusal, and recovery with a fresh stage. Test valid lookalikes and source-tree behavior. Search all project-path guard callers and cover each relevant public entry point; preserve existing containment and link refusals. The plan maps owning tests, consumers and standing gates and records wide Boundary B on the final implementation commit; certification is separate.

### Examples / smoke checks

Exercise public commands in scratch projects and run applicable claim, link, snippet and neutrality checks and `python scripts/check_cairn.py` for changed prose. Engine changes require the existing Maintainer-run AST re-anchor; this proposal does not authorize it.

#### Security preflight — five questions

* **S1:** The adopter supplies lockfile and review-area path names and the project filesystem; Cairn supplies its source tree. The object being checked supplies the names.
* **S2:** Removing the any-component check, case folding, or trailing-character normalization must cause corresponding tests to fail. These mutations have not been run for the proposed implementation.
* **S3:** Public upgrade commands select lockfile records and staged metadata; the guard checks project names at its callers. The current guidance says a record inside `.git/` is refused (`bootstrap/UPGRADE.md`); revise it to match the expanded set and test each caller.
* **S4:** A matching component refuses before access, granting less authority. Invalid shapes and existing containment and link errors retain refusal; normalization must not turn a nonmatching path into an allowed Git alias.
* **S5:** An attacker who can supply a lockfile or stage can choose names, but should not use these paths to access nested Git data. An attacker who can race filesystem operations after checks may still succeed; this does not claim arbitrary concurrent-writer protection.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A nested Git path is read or written through an upgrade, refusal changes Git data or metadata, a valid lookalike is blocked, or normal recovery cannot produce a usable stage.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance
