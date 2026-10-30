# Refuse linked installed files during lockfile migration

**Author**: Codex GPT-6.1 Sol (Strategy)
**Status**: awaiting-review
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Lockfile migration should refuse linked installed files before reading them so it cannot record the digest of another file.

## Context

`upgrade --init-lock` migrates an older install by hashing mapped files in
the target project. It refuses links in its own lockfile and profile path
(`bootstrap/_scaffold/upgrade.py:1619-1648`), but its mapped-file loop uses
`Path.exists()` and `read_bytes()` without a link check
(`bootstrap/_scaffold/upgrade.py:1684-1718`). A disposable installed project
with `AGENTS.md` replaced by a link to a file outside the project returned
exit 0. Its new lockfile recorded `AGENTS.md` with a digest exactly matching
that outside file. This reads outside content and presents it as project-owned
install state. The v0.6 board lists this finding separately from the active
upgrade ancestor and path-display plan (`dev/PLANNING.md`).

## Proposal

Before testing existence or reading any mapped destination during
`--init-lock`, refuse a link at the leaf or any path component. Reuse the
existing `_refuse_if_linked` path check and one-line recovery wording; do not
add another path policy or command option. Refuse a dangling link too, rather
than silently classifying it as a missing installed file. A refusal leaves the
lockfile absent and changes neither the link nor its target. A regular file
inside the project continues to migrate, even if its contents were copied
from elsewhere. The existing vendor-wrapper alias lookup already skips linked
aliases without reading them; that behavior is outside this proposal.

The operator can replace a linked destination with an ordinary project file
and rerun. This costs an extra step for adopters who intentionally use links
in installed file positions; `--init-lock` will no longer migrate those
installations until they choose a regular file. It does not prohibit links
elsewhere in their project, change the install manifest, or decide whether
an older linked install was safe.

## Rationale

The migration's claim is about bytes owned by the project. Refusal is simpler
than recording a link target, which may point outside the tree or change
after the digest is written. It matches the command's existing linked-profile
rule and preserves the current lockfile format. The check must precede
`exists()` because `exists()` follows links and treats a dangling one as
absent.

## Alternatives considered

Hash the link text: the lockfile's `hash` currently means file contents, so
this changes its contract and would need consumer changes. Follow only links
whose target stays within the project: the resulting lock still attests the
target's bytes while storing the link's name, and a later retarget escapes
the migration evidence. Keep the behavior: the reproduced outside read and
misleading digest remain.

## Documentation / doctrine surface

Update descriptive `bootstrap/UPGRADE.md` to state the refusal and the
replace-with-a-regular-file recovery. No doctrine or install-manifest change
is proposed.

## Evidence / verification plan

### Tests required

Add public `--init-lock` cases in
`bootstrap/tests/test_upgrade_refuses_hostile_project_data.py`: linked
`AGENTS.md` to an inside and outside file; dangling leaf; linked parent of
a mapped destination; regular-file control.
Check exit and diagnostic, unchanged project and outside snapshots, and
absence of a new lockfile on refusal. Search other `--init-lock` readers and
mapped-path consumers; retain their owning tests. The plan maps the exact
nodes and public path for wide Boundary B verification under Python 3.13.
The AST re-anchor is a separate Maintainer ceremony, not a change test.

### Examples / smoke checks

Run `python bootstrap/scaffold.py upgrade --target <scratch-repo> --init-lock`
for refusal and regular control, and `python scripts/check_cairn.py` on
changed prose. Do not run the full suite per change.

#### Security preflight — five questions, answered in writing

* **S1.** Cairn's mapping chooses destinations; the adopter supplies project
  path components and file bytes. A link can refer outside the project and
  currently supplies the bytes being classified as an installed file.
* **S2.** Removing the proposed link check should make the outside-link public
  test return success with an outside digest. That baseline was reproduced
  before opening; the implementation mutation remains to be run.
* **S3.** A person runs `bootstrap/scaffold.py upgrade --init-lock` on a
  pre-lockfile project. The check covers each mapped destination before its
  existence test or read. The guide and diagnostic must describe that scope.
* **S4.** Link, dangling link, unreadable path or unsafe component refuses
  migration with no new lockfile. A regular file keeps existing behavior;
  no fallback follows a link.
* **S5.** A project owner can copy outside content into an ordinary project
  file or edit the resulting lockfile. This prevents accidental or crafted
  link traversal at migration, not dishonest ownership claims.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A linked mapped file still reaches `read_bytes()`, a dangling link is
silently skipped, a refusal leaves a lockfile or alters the target, or an
ordinary pre-lockfile install cannot migrate.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance — scaffold engine and lockfile contract.
