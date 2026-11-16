# Ship a Git attributes file so line endings match on every machine

**Author**: Claude Sonnet 5.5 (`claude-sonnet-5-5`)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: standard — it adds an installed file through the install table and the lockfile, an install-contract change (the Maintainer sets the tier)
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-16
**In brief**: Cairn would install a root `.gitattributes` that stores and checks out text files with the same line endings everywhere, so a Windows checkout stops silently differing from the repository.

## Decision summary

Without a Git attributes file, each machine's Git setting decides the line ending on disk. A Windows checkout wrote CRLF while the repository stores LF; issue #91 (part 1) reports LF-written exact-text edits silently missing, and #63 (part 2) every saved upgrade ancestor looking invalid. I recommend option A: ship a small `.gitattributes` through the installer, never overwriting an adopter's own. Cost: one engine edit, Security Review, and guide text on renormalizing an existing repository. Option B (guide text only) carries the same content without an engine change.

## Context

- Cairn's own repository has no `.gitattributes` (`git ls-files` finds none; checked at `e8703b2c`).
- The reporter says their file (`* text=auto eol=lf`, CRLF for `.bat` and `.cmd`) kept `git status` clean from 2026-11-14. Not reproduced: I am on macOS and nothing here was tried on Windows.
- The install table is `_CORE_MAPPINGS` in `bootstrap/_scaffold/config.py` (line 534; protected).
- A fresh install skips an existing destination unless `--force` (`install.py:367`), and the lockfile is not written at all if any installed file differs from a clean install (`install.py:2343`).
- On upgrade, a new core file that meets an existing untracked file is `new-core-blocked`: shown, never overwritten, adoptable with `--adopt-collisions` (`upgrade.py:1007-1038`). `UPGRADE.md` "If `RULES.md` meets your project rules" documents the same route.
- I found no code-evolution area map in this tree (`grep` for `code_evolution`, `area_map`: no match); it is probably the reporter's own test (not checked). The one root-file lister here, `scripts/claim_check.py:539`, skips dot-entries, so it needs no change.

## Proposal

Proposed paths:
- `templates/core/gitattributes.txt`

**Options.**

| | What it is | Cost to adopters | Cost to Cairn |
|---|---|---|---|
| A (recommended) | Install the file | Nothing on a fresh install; an existing repository renormalizes (below) | Protected-file edit, Security Review, AST re-anchor |
| B | Guide text only | Each adopter must read and create the file; one who does not still hits the symptom | No engine change |
| C | Only the upgrade diagnostic (defects draft item 1) | Windows adopters still get CRLF; it only explains afterwards | None |

**Content (A and B).** Safe defaults for every project:

```
* text=auto eol=lf
*.bat text eol=crlf
*.cmd text eol=crlf
*.png binary
*.pdf binary
```

The binary list continues, one pattern per line (`.jpg`, `.gif`, `.zip`, `.gz`, `.nc`, `.h5`, `.npy`, `.tif`). Project choices, shipped as commented examples because Cairn cannot know the paths: `-text` for recorded evidence that must stay byte-for-byte (raw instrument output), and CRLF for any file a Windows tool requires. Which tools: not checked.

**Installer behavior (A).**
1. Add one mapping to `_CORE_MAPPINGS`. The source is named `templates/core/gitattributes.txt`, not a dot-name, because a `.gitattributes` there would apply inside Cairn's own checkout.
2. Never overwrite: an existing `.gitattributes` is kept even with `--force`, and the install prints the recommended lines for the adopter to merge by hand. The plan must change the lockfile step so a kept file does not stop the lockfile being written; today it would (`install.py:2343`), and an existing `.gitattributes` is far likelier than an existing `AGENTS.md`.
3. On upgrade, the existing collision route applies unchanged: never overwritten, never silently merged. Adopting it records the adopter's file as a tracked fork; later upstream edits then appear as a normal three-way merge in `--plan`.
4. Add `.gitattributes` to `_LIVING_STATE_DSTS` (`lockfile.py:197`), as for `RULES.md`, so adopter edits to project-choice lines are not tamper findings.

**Migration risk.** Adding the file to a repository whose index holds CRLF text shows those files as modified. The guides will say: commit `.gitattributes` alone first; see affected files with `git ls-files --eol`; with no other work uncommitted, run `git add --renormalize .`, review `git diff --cached --stat`, commit, then re-checkout (a fresh clone is simplest). Cairn's lockfile hashes LF bytes, so once the checkout is LF the hashes match again. The defects draft's item 1 diagnostic still serves repositories that have not added the file, and its message should point here.

**Dependencies.**
- The defects draft (`dev/proposals/2026-11-16-claude-adopter-defects-0-7-0.md`) is not decided. Item 7 sends this proposal here. If it is decided differently on item 1 (for example, normalizing before hashing), this proposal still prevents the cause but matters less; if item 7 is withdrawn, this stands alone.
- Under A, land before the accepted layout proposal (`2026-11-09-claude-repository-layout.md`): the mapping is written once and moves with the installer. The layout installs under `dev/` and keeps root governing files, but `.gitattributes` must sit at the root to cover the repository, so the layout plan must name it as an exception. If the layout lands first, only paths here change.

## Rationale

Windows is an equal partner (Maintainer, 2026-11-10, quoted on the board: "We want full windows support--it is an equal partner."). The cause is one missing file. A diagnostic alone leaves every new Windows adopter hitting the problem first.

## Alternatives considered

B and C above. Both lost because the symptom is silent: a guide or diagnostic reaches the adopter only after the failure.

## Documentation / doctrine surface

`bootstrap/BOOTSTRAP.md` and `bootstrap/UPGRADE.md` (descriptive layer): the renormalize steps and the existing-file route. No governing-layer change.

## Evidence / verification plan

Through the installer's public entry points: a fresh install writes the file and the lockfile; a different existing `.gitattributes` survives install, `--force` and upgrade byte for byte with the lockfile still written; `upgrade --plan` shows `new-core-blocked`; `verify_integrity` accepts an edited copy. Run via `python tools/test_tiers.py for <paths>`. Falsified if any path overwrites an existing file.

**Windows check, not run here:** the implementer, on the Windows VM (`dev/rules/development-environment.md`) with `core.autocrlf=true`, installs into a fresh repository and confirms `git status` is clean, `git ls-files --eol` shows `w/lf`, and `upgrade --plan` has no review-only files.

#### Security preflight

N/A here: the Security Review answers S1-S5 for the protected edits.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

CRLF on a Windows disk with the file present; an adopter's file changed by install, `--force` or upgrade.

## Scope delta

N/A: opening draft.

## Assurance path

**Assurance path**: high-assurance — the install contract and scaffold engine are touched.
