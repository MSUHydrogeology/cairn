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

## Review -- Claude Sonnet 5.5 (ordinary Reviewer, Medium) -- 2026-11-16

**Reviewed commit**: `19b2d666` (Release the two follow-on drafts for ordinary and Security review), branch `master`
**Tier**: usual
**Findings**: 1 blocking, 6 non-blocking
**Verdict**: REVISE
**Elapsed**: about 8 minutes (15:30 to 15:38 EST)
**Tokens**: unknown

**Steelman.** One missing file is the cause of two reported Windows failures, and a diagnostic only explains the failure after it has happened. Shipping the file once, never over an adopter's own, is the smallest fix that prevents it.

**Foundations.**
1. *Should this happen as framed?* Yes. The mechanism is real: `install.py:367` skips an existing file and the `diverged` check (`install.py:2323`, block at 2347) withholds the lockfile, so the draft's reading of today's code is right. The Windows result is unmeasured, and the draft says so.
2. *Best alternative.* Option B (guide text) is weaker for a silent symptom. A middle option is untested: install the file only when none exists and report the index's line endings (`git ls-files --eol`) before writing it into an existing repository (finding 4).
3. *What would show it wrong?* The draft's own checks (CRLF on disk with the file present; an overwritten adopter file) are the right ones. Add: any file in an existing repository that shows as modified after install.

**Findings.**
1. **Blocking: "Dependencies" is false today.** It says the defects draft "is not decided" and links `dev/proposals/2026-11-16-claude-adopter-defects-0-7-0.md`. That proposal is accepted and archived (`dev/proposals/archive/`), so the link is dead. Decision 1 rejected folding line endings before hashing, and the item 1 diagnostic landed as diagnostic only (`c62d18fa`). Decision 7 also says "a separate light proposal", while this draft proposes `standard`. Closes it: rewrite the paragraph against the Decision, fix the link, and state why `standard`.
2. **Non-blocking: line cites drifted.** `lockfile.py:197` is 201; the `new-core-blocked` code is `upgrade.py` 1040-1080, not 1007-1038. `config.py:534`, `install.py:367` and `claim_check.py:540` hold. The "no area map" claim also holds (no match in the tree). Re-cite.
3. **Non-blocking: kept-file semantics underspecified.** `--force` currently overwrites (`install.py:367`), so "never, even with `--force`" needs a new special case; the draft names no site. A kept file is not in the lockfile, so every upgrade shows `new-core-blocked` and `--stage` stops (`UPGRADE.md:217`) until `--adopt-collisions`. For the common adopter that is a first-upgrade stop. The proposal should say so, and say whether the plan writes any record for the kept file.
4. **Non-blocking: brownfield install.** The default `* text=auto eol=lf` dropped into a repository whose index holds CRLF makes every text file show modified, and the installer would do it silently. Closes it: the installer counts `i/crlf` files and warns, or the guide step is printed at install time.
5. **Non-blocking: "safe defaults for every project" is overstated.** `renormalize` rewrites stored text data (csv, dat) and changes blob hashes, which breaks any recorded checksum. `.sln`, `.reg` and some Windows tools need CRLF. Add both to the Migration risk text, not only commented examples.
6. **Non-blocking: re-checkout step is vague** ("then re-checkout"). If read as `git rm --cached -r . && git reset --hard`, it loses uncommitted work. Name one safe command or say "fresh clone".
7. **Non-blocking: living-state weakens tamper detection.** Step 4 exempts `.gitattributes` from the tamper check, yet it can bind `filter`/`merge` drivers. For Security Review to weigh; plain-language surface is fine and no governing rule disappears.

**Audience.** The guide edits are descriptive; the install-time print should be written for an agent without a person in context.

**Coverage.** Read the proposal, the defects Decision and plan C2/C3/C6/C8, issue #91 (read-only), and the cited code. Not run: tests, the installer, Windows. Not reviewed: Security questions S1-S5.

## Security Review -- Claude Opus 5.5 (Security Reviewer, High) -- 2026-11-16

```
Reviewed commit: 556275b4
```

**Tier**: Security Review
**Findings**: 1 blocking, 4 non-blocking
**Verdict**: REVISE
**Elapsed**: about 4 minutes (15:31 to 15:35 EST)
**Tokens**: unknown

Obligation: decide whether a Cairn-installed, adopter-edited or planted `.gitattributes` can make Cairn's checks run a program, hide a change, or bypass a guard.

Steelman: Cairn's integrity checks hash bytes themselves and never ask Git to convert them, so a text-only attributes file cannot change their answer.

**Foundations**

1. **Should this happen as framed?** Yes. No attribute reaches a hash check: `verify_integrity` hashes disk bytes (`bootstrap/verify_integrity.py:463-465`); `_committed_copy_matches` reads the raw blob (`upgrade.py:3396-3398`); the edit check hashes files itself and folds CRLF only from config (`upgrade.py:3088-3094`, `3159-3161`). An attribute runs a program only with a driver defined in config. `git_read` blanks global and system config, sets no `HOME`, and disables textconv, external diff and, for `status`, every configured filter (`tools/git_read.py:515-517`, `606-618`, `676-704`, `1735-1742`).
2. **Best alternative.** Install only when absent and write no record for a kept file. Strict tracking plus a refusal of driver attributes was weighed and rejected: subdirectory files and `.git/info/attributes` bypass a root-only refusal, and today the file has no tamper signal at all.
3. **What would show it wrong.** A clean install over a different pre-existing `tools/` file that writes a lockfile. Or `git check-attr -a` finding a live attributes file under `dev/.cairn/base/`.

1. **Blocking.** Step 2 says a kept file must not stop the lockfile being written. That check is the guard which refuses to attest a tree when any file differs from a clean install (`install.py:2269-2272`, `2321-2323`). `verify_integrity` checks only the records present. The attack: someone plants a hostile `tools/` script before install. A generalized "kept file" exemption leaves it with no record and writes the lockfile, and verify then reports OK. Closes with: an exemption keyed to the one path `.gitattributes`, no record for the kept copy, and a test that any other diverged file still withholds the lockfile.
2. **Non-blocking.** Step 3's three-way merge means a substituted install. That writes a base cache copy at `dev/.cairn/base/.gitattributes` (`install.py:2335-2338`; the cache is tracked, `lockfile.py:48`). Git honors it for that folder, which is the hazard step 1 avoids for Cairn's own checkout. Adoption writes the same copy. Closes with: a non-dot cache name or a verbatim install, named in the plan.
3. **Non-blocking.** The living-state residual is not named. `-diff`, `binary` or `linguist-generated` lines can hide governing-file diffs from human and agent review, the file's own diff included. The hash check still catches Cairn files. Closes with: one sentence on the residual beside the `_LIVING_STATE_DSTS` entry and in the guide.
4. **Non-blocking.** The `eol=crlf` lines must match no Cairn-installed path. The lockfile hashes LF bytes, so a fresh clone of a matched path would fail integrity. No `.bat` or `.cmd` ships today (`git ls-files`). Closes with: a test asserting this.
5. **Non-blocking, existing and not widened.** `git_read`'s `status` still honors attributes in Cairn's own checkout (no `GIT_ATTR_NOSYSTEM`). An `ident` line in `.git/info/attributes` can make an edit inside `$Id: ...$` read as clean in the provenance check (`install.py:2143-2144`). Separate item.

**Coverage:** Read the proposal, the ordinary review, the cited code, `SAFETY.md:395-450` and `SECURITY_MUTATIONS.md:124-125`. Point (d): no bypass found. A dangling link at the destination reaches `_assert_safe_write`, which refuses it (`security.py:134`). Adoption requires a regular file that is not a link (`upgrade.py:1069-1070`). Not run: tests, the installer, Git experiments, or Windows. The `ident` behavior is from Git's documented conversion and was not measured. Not reviewed: the upgrade stage folder's handling of a dot-named file, or hardlinked destinations.
