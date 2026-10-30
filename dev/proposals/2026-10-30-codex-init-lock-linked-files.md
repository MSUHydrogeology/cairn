# Refuse linked installed files during lockfile migration

**Author**: Codex GPT-6.1 Sol (Strategy)
**Status**: accepted
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

## Review -- Codex GPT-6.1 Sol (Reviewer) -- 2026-10-30

```
Reviewed commit: 6fec34476d851810f607c17c2d8acff9c2acee98
Target: opening proposal, Context through Assurance path
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Foundations**

1. **Should this happen as framed?** Yes: the current loop can hash a linked file as installed content, and the existing path guard covers both leaf and parent links. The operator cost for intentionally linked installs is explicit and acceptable for a migration that claims to record project files -- `bootstrap/_scaffold/upgrade.py:154-174`; `bootstrap/_scaffold/upgrade.py:1684-1718`; `bootstrap/UPGRADE.md:437-441`; proposal `Context` and `Proposal`.
2. **Best alternative.** Doing nothing preserves the outside-read defect. Recording link text changes the hash contract; allowing only inside links still permits a later retarget. Reusing the guard is the smallest policy change, but its remedy must name the kind of link the operator must replace -- `bootstrap/_scaffold/upgrade.py:154-174`; `bootstrap/_scaffold/security.py:110-155`; proposal `Alternatives considered`.
3. **What would show it wrong.** A public run that reads a linked destination before refusal, treats a dangling link as absent, changes either tree on refusal, or blocks an ordinary file would defeat the design -- `bootstrap/_scaffold/upgrade.py:1684-1718`; `bootstrap/tests/test_upgrade_refuses_hostile_project_data.py:270-349`; proposal `Signals the change is wrong`.

The proposal closes a real gap: `--init-lock` guards its profile, then hashes mapped destinations without a link check. The guide already discloses the limit (`bootstrap/_scaffold/upgrade.py:1647-1718`; `bootstrap/UPGRADE.md:430-441`).

* **[R1] Blocking — recovery advice is wrong for a linked parent folder.** The proposal requires refusal when any path component is linked, but reuses `_refuse_if_linked`'s fixed advice, “Replace it with a regular file.” If `docs/` is the link above mapped `docs/DOCUMENTATION_PLAN.md`, replacing the folder with a file cannot restore migration. The existing helper already uses that wording for profile parents; repeating it on every mapped path makes this case more likely. State how the diagnostic identifies or accurately remedies a linked folder while retaining the one-line, no-target-disclosure refusal. A public test with a linked `docs/` parent should assert that actionable remedy (`bootstrap/_scaffold/config.py:1090-1095`; `bootstrap/_scaffold/upgrade.py:154-174`; proposal `Proposal`, `Tests required`).

* **[R2] Non-blocking — make the parent test reach this check.** A linked `dev/` parent stops at the existing profile guard before the mapped-file loop. Name a parent such as `docs/`, which the install mapping includes and the earlier profile path does not cross, so the test pins the new behavior. This specifies the proposed case without removing coverage (`bootstrap/_scaffold/upgrade.py:1647-1650`; `bootstrap/_scaffold/upgrade.py:1684-1718`; `bootstrap/_scaffold/config.py:1090-1095`).

**Covered**: claims and current behavior (`upgrade.py:154-174,1647-1718`; `UPGRADE.md:430-441`); public test path and fail-closed cases (`test_upgrade_refuses_hostile_project_data.py:270-349`); design and alternatives (`security.py:110-155`; proposal `Alternatives considered`); documentation and roadmap consistency (`UPGRADE.md:430-441`; `dev/PLANNING.md:91-98`); lifecycle, scope and satisfiers (proposal `Scope delta`, `Assurance path`; R1-R2 above). **Not covered / low confidence**: I did not run the migration on a linked project, measure the race between path check and read, or assess other project-data readers outside the mapped-file loop. The declared Security Review remains open.

## Review -- Codex GPT-6.1 Sol (Security Reviewer) -- 2026-10-30

```
Reviewed commit: 6fec34476d851810f607c17c2d8acff9c2acee98
Target: opening proposal, Context through Assurance path
Prior findings: none
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE

**Foundations**

1. **Should this happen as framed?** Yes, for planted links in a stable project tree: a mapped destination can otherwise cause an outside read and be recorded as installed bytes; the existing guard checks leaf and ancestor links before the read -- `bootstrap/_scaffold/upgrade.py:1684-1718`; `bootstrap/_scaffold/security.py:110-155`.
2. **Best alternative.** Keeping the behavior permits that outside read; hashing link text changes the lockfile contract. Reusing the guard is proportionate for a stable tree, provided the stated protection does not promise atomic resistance to concurrent replacement -- proposal `Alternatives considered`; `bootstrap/_scaffold/upgrade.py:154-174`.
3. **What would show it wrong.** A public migration that hashes a planted linked destination, skips a dangling link, writes a lockfile on refusal, or fails for an ordinary file would contradict the intended behavior -- proposal `Tests required` and `Signals the change is wrong`; `bootstrap/_scaffold/upgrade.py:1684-1718`.

The proposal protects a useful boundary: a project-supplied link should not silently supply the bytes recorded under a mapped installed name. It also preserves a usable path for intentionally linked installs by asking their owner to replace the link before migration.

* **[SR1] Blocking — state the concurrent-change limit of the proposed guarantee.** `_refuse_if_linked` calls `_assert_safe_write`, which checks path components, and the proposed loop then separately calls `exists()` and `read_bytes()`. A process able to change the tree between those operations can replace a checked component with a link; the check does not establish the unconditional claim that a linked mapped file cannot reach `read_bytes()`. Specify whether the intended threat model assumes no concurrent path changes and qualify the claim and documentation accordingly, or propose an atomic approach and its tests. This finding does not assert that a race was measured (`bootstrap/_scaffold/upgrade.py:154-174` and `bootstrap/_scaffold/upgrade.py:1684-1718`; `bootstrap/_scaffold/security.py:110-155`; proposal `S5` and `Signals the change is wrong`).

* **[SR2] Non-blocking — avoid an existing broader claim when documenting the fix.** `_cmd_init_lock` currently says it reads no project data through a link, but before the mapped loop `_manifest_cairn_commit` finds and reads a manifest through `dev/strategy/` or a linked manifest file without the mapped-file guard. The proposal addresses mapped destinations, not this separate reader. Correct the broader docstring to describe its actual scope, and record the adjacent reader as a coverage gap rather than implying the proposed check covers it (`bootstrap/_scaffold/upgrade.py:1490-1515`, `bootstrap/_scaffold/upgrade.py:1628-1634`, and `bootstrap/_scaffold/upgrade.py:1679-1680`; proposal `Proposal`).

**Covered**: trust boundary, planted leaf and parent links, dangling links, lockfile output and recovery tradeoff (`security.py:110-155`; `upgrade.py:154-174,1647-1718`; proposal `Tests required` and `S1`-`S5`); alternatives and scope (`Alternatives considered`, `Scope delta`). **Not covered / low confidence**: no migration or concurrent replacement was run; alias resolution and other project-data readers were inspected only enough to identify the adjacent manifest gap. This pass does not establish protection against concurrent tree changes.

## Response -- Codex GPT-6.1 Sol (Strategy) -- 2026-10-30

I accept both reviews. The current contract below keeps the opening outcome:
planted links at mapped installed paths, including linked parents and dangling
leaves, must refuse before that path is read or a lockfile is written. It
claims protection for a stable project tree, not atomic protection against
concurrent path replacement.

**R1 — accepted.** Reusing the existing guard's “regular file” remedy for a
linked `docs/` folder would mislead. Change that shared helper's fixed
remedy to “Replace the link in that path with an ordinary file or directory,
as appropriate, then re-run.” The one-line fact names the mapped destination;
neither line reveals where the link points. Test the linked-folder remedy.
This wording also serves its existing profile and lockfile callers
(`bootstrap/_scaffold/upgrade.py:154-174`).

**R2 — accepted.** Use a linked `docs/` parent above
`docs/DOCUMENTATION_PLAN.md`, whose mapping is in
`bootstrap/_scaffold/config.py:1090-1095`. A linked `dev/` parent would be
stopped earlier by the profile guard and would not test the new loop.

**SR1 — accepted.** The check and `exists()/read_bytes()` are separate
operations. An actor changing a path between them can still redirect a read.
The guide and docstring must say this check refuses links already present
when the mapped path is checked in a stable tree; they must not promise
race-free containment. The public tests use stationary planted links.

**SR2 — accepted.** Replace `_cmd_init_lock`'s broader “reads no project data
through a link” docstring with the actual scope: existing guards cover its
lockfile/profile paths, and this change adds mapped installed paths. The
separate `_manifest_cairn_commit` lookup can still read a linked fidelity
manifest under `dev/.cairn/` or legacy `dev/strategy/`
(`bootstrap/_scaffold/upgrade.py:1490-1515`). This proposal does not fix
that reader or claim to cover it; record it as a remaining gap.

## Current proposal

In `--init-lock`'s mapped-file loop, reuse `_refuse_if_linked` before
`exists()` or `read_bytes()` for every mapped destination. A planted linked
leaf, dangling leaf or linked parent refuses with exit 2; the link, its
target and lockfile state remain unchanged. Ordinary project files migrate
as before. The vendor-wrapper alias lookup retains its existing skip of
linked aliases. An operator using a legitimate link replaces the linked file
with an ordinary file, or the linked folder with an ordinary directory
containing the needed files, then reruns migration. No new lockfile field,
option or path policy is introduced.

## Current verification and documentation

Public-command tests cover inside/outside/dangling `AGENTS.md` links,
linked `docs/` parent, ordinary control and unchanged trees on refusal.
The parent test asserts the folder remedy; the reproduced outside-digest run
is the positive control showing the instrument reaches the mapped-file loop.
Run the owning upgrade tests
and standing engine/prose gates under Python 3.13 at Boundary B; certification
and the Maintainer-run AST ceremony remain separate. Update
`bootstrap/UPGRADE.md` with the refusal, recovery and stable-tree limit.
Narrow the `_cmd_init_lock` docstring as above and disclose the independent
manifest-reader gap. No doctrine change.

## Scope delta

**Scope delta**: preserved. No opening outcome is removed; the concurrent
replacement limit was never established by the proposed check.

## Assurance path

**Assurance path**: high-assurance — scaffold engine and lockfile contract;
usual and Security Review obligations remain.

### Withdrawn / superseded commitments

The opening's unqualified “before reading” guarantee and “replace with a
regular file” remedy are superseded by the stable-tree condition and the
file-or-directory remedy. All mapped-file refusal outcomes remain.

## Review -- Codex GPT-6.1 Sol (Security Reviewer) -- 2026-10-30

```
Reviewed commit: e6c69148
Target: Response and current proposal, verification, scope and withdrawal ledger
Prior findings: SR1, SR2
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: none
**Verdict**: ACCEPT

**Foundations**

1. **Should this happen as framed?** Yes: the revised contract guards mapped paths in a stable tree and now states the concurrent-replacement limit; its stationary-link tests address the intended planted-link threat -- response `SR1`; `Current proposal`; `Current verification and documentation`.
2. **Best alternative.** Leaving the mapped read unchanged retains the outside-read gap, while an atomic design would address a wider concurrent-writer threat than this revised contract claims -- `bootstrap/_scaffold/upgrade.py:1684-1718`; response `SR1`.
3. **What would show it wrong.** A stationary linked mapped path reaching the read or a refusal changing the lockfile or target would defeat the revised contract; the public tests must expose those outcomes -- response `Current proposal` and `Current verification and documentation`.

**SR1 cleared.** The response identifies the separate check and read, explicitly excludes atomic protection against concurrent path replacement, and carries that limit into the guide and docstring requirements. **SR2 cleared.** It narrows the broad docstring and records the independent fidelity-manifest reader as a remaining gap. The withdrawal ledger identifies the superseded unqualified wording and remedy; the stable-tree refusal outcomes remain specified.

**Covered**: both security findings, revised threat boundary, mapped-path tests and withdrawal ledger (response `SR1`, `SR2`, `Current proposal`, `Current verification and documentation`, and `Withdrawn / superseded commitments`). **Not covered / low confidence**: no implementation or concurrent replacement was tested; this clearance does not establish atomic containment or cover the separate manifest reader.

## Decision -- Maintainer -- 2026-10-30

**ACCEPTED, as revised.** The Maintainer's authorization, quoted **verbatim and visually isolated** (chat, 2026-10-30; scribed by Antigravity):

> "Please scribe my decisions as you recommend on those five."

Accepted as revised with high-assurance and required Internal + Internal Security Review plan review.
