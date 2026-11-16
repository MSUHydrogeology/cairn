# Ship a Git attributes file so line endings match on every machine

**Author**: Claude Sonnet 5.5 (`claude-sonnet-5-5`)
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: standard — it adds to the install set and changes the lockfile step, both named protected contracts (the Maintainer sets the tier; see Dependencies)
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-16
**In brief**: Cairn would install a root `.gitattributes` that stores and checks out text files with the same line endings everywhere, so a Windows checkout stops silently differing from the repository.

## Decision summary

Without a Git attributes file, each machine's Git setting decides the line ending on disk. A Windows checkout wrote CRLF while the repository stores LF; issue #91 (part 1) reports LF-written exact-text edits silently missing, and #63 (part 2) every saved upgrade ancestor looking invalid. I recommend option A: ship a small `.gitattributes` through the installer, never overwriting an adopter's own. Cost: one engine edit, Security Review, a first-upgrade stop for adopters who keep their own file, and guide text on renormalizing an existing repository. Option B (guide text only) carries the same content without an engine change.

## Context

- Cairn's own repository has no `.gitattributes` (`git ls-files` finds none; checked at `e8703b2c`).
- The reporter says their file (`* text=auto eol=lf`, CRLF for `.bat` and `.cmd`) kept `git status` clean from 2026-11-14. Not reproduced: I am on macOS and nothing here was tried on Windows.
- The install table is `_CORE_MAPPINGS` in `bootstrap/_scaffold/config.py` (line 534; protected).
- A fresh install skips an existing destination unless `--force` (`install.py:367`), and the lockfile is not written at all if any installed file differs from a clean install (`install.py:2321-2323`, refusal at 2343-2359).
- On upgrade, a new core file that meets an existing untracked file is `new-core-blocked`: shown, never overwritten, adoptable with `--adopt-collisions` (`upgrade.py:1040-1080`). `UPGRADE.md` "If `RULES.md` meets your project rules" documents the same route.
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

**Content (A and B).** Defaults that suit most projects, not all (see Migration risk):

```
* text=auto eol=lf
*.bat text eol=crlf
*.cmd text eol=crlf
*.png binary
*.pdf binary
```

The binary list continues, one pattern per line (`.jpg`, `.gif`, `.zip`, `.gz`, `.nc`, `.h5`, `.npy`, `.tif`). Project choices, shipped as commented examples because Cairn cannot know the paths: `-text` for data and evidence files that must stay byte-for-byte (raw instrument output, `.csv`, `.dat`), and CRLF for any file a Windows tool requires (`.sln`, `.reg`; other tools not checked). The `eol=crlf` lines must match no Cairn-installed path (none ships today), because the lockfile hashes LF bytes; a test asserts this (Security Review 4).

**Installer behavior (A).**
1. Add one mapping to `_CORE_MAPPINGS`. The source is named `templates/core/gitattributes.txt`, not a dot-name, because a `.gitattributes` there would apply inside Cairn's own checkout.
2. Never overwrite: an existing `.gitattributes` is kept even with `--force`, and the install prints the recommended lines for the adopter to merge by hand. This is a new special case at the `dst.exists()` test in `_install_one` (`install.py:367`), which today overwrites under `--force`. The lockfile step changes for this one path only: in the `diverged` loop (`install.py:2321-2323`), a destination named `.gitattributes` that differs gets no lockfile record and does not join `diverged`. Any other differing file still stops the lockfile, exactly as today. Tests: with a kept `.gitattributes` the lockfile is written and lists no record for it; with a differing `tools/` file (or any other path) it is not written.
3. On upgrade, a kept file has no lockfile record, so the collision route applies: `new-core-blocked`, never overwritten, never silently merged, and `--stage` stops until `--adopt-collisions` (`UPGRADE.md` line 217). The stop repeats on every upgrade until the adopter runs `--adopt-collisions` once; that records their file as a tracked fork and ends it. The plan installs the mapping verbatim, so adoption writes no copy under `dev/.cairn/base/` (a live `.gitattributes` there would apply to that folder; Security Review 2). Verbatim also means later upstream edits show as a fork against upstream, not a three-way merge.
4. Add `.gitattributes` to `_LIVING_STATE_DSTS` (`lockfile.py:201`), as for `RULES.md`, so adopter edits to project-choice lines are not tamper findings. This does remove a tamper signal for that one file, but only on an installed copy, which would otherwise flag every adopter edit; no integrity check reads attributes, so Cairn's own file hashes are unaffected (Security Review foundation 1). Residual: `-diff`, `binary` or `linguist-generated` lines can hide changes from human and agent diff review, including this file's own diff. Strict tracking was weighed and rejected: a subdirectory file or `.git/info/attributes` bypasses it. The guide says this in one sentence.

**Migration risk.** Adding the file to a repository whose index holds CRLF text makes those text files show as modified until renormalized; a brownfield install does this silently, so the install counts `i/crlf` files (`git ls-files --eol`) and prints the guide step when any exist. Renormalizing rewrites stored text and changes blob hashes, so it breaks any recorded checksum of a data file (hence the `-text` examples above). The guides will say: commit `.gitattributes` alone first; see affected files with `git ls-files --eol`; with no other work uncommitted, run `git add --renormalize .`, review `git diff --cached --stat`, commit, then make a fresh clone (the one safe re-checkout; `git rm --cached -r . && git reset --hard` loses uncommitted work). Cairn's lockfile hashes LF bytes, so once the checkout is LF the hashes match again. The defects draft's item 1 diagnostic still serves repositories that have not added the file, and its message should point here.

**Dependencies.**
- The defects proposal is accepted and archived (`dev/proposals/archive/2026-11-16-claude-adopter-defects-0-7-0.md`). Its Decision kept line endings to a diagnostic and rejected folding CRLF before hashing (landed at `c62d18fa`), so this file is the only prevention of the cause. Its item 7 called this follow-on "a separate light proposal".
- **Tier conflict.** The template makes light the default, but the install set and lockfile step are named protected contracts (`dev/proposals/_template.md`, triage triggers), and the change needs a plan and a Security Review, which light work lacks. I keep standard; the Maintainer's Decision wording is light. See "For the Maintainer".
- Under A, land before the accepted layout proposal (`2026-11-09-claude-repository-layout.md`): the mapping is written once and moves with the installer. The layout installs under `dev/` and keeps root governing files, but `.gitattributes` must sit at the root to cover the repository, so the layout plan must name it as an exception. If the layout lands first, only paths here change.

## Rationale

Windows is an equal partner (Maintainer, 2026-11-10, quoted on the board: "We want full windows support--it is an equal partner."). The cause is one missing file. A diagnostic alone leaves every new Windows adopter hitting the problem first.

## Alternatives considered

B and C above. Both lost because the symptom is silent: a guide or diagnostic reaches the adopter only after the failure.

## Documentation / doctrine surface

`bootstrap/BOOTSTRAP.md` and `bootstrap/UPGRADE.md` (descriptive layer): the renormalize steps, the existing-file route, the repeating first-upgrade stop and the living-state residual. The install-time print is written for an agent with no person in context. No governing-layer change.

## Evidence / verification plan

Through the installer's public entry points: a fresh install writes the file and the lockfile; a different existing `.gitattributes` survives install, `--force` and upgrade byte for byte with the lockfile still written and no record for it, while any other differing file still withholds the lockfile; `upgrade --plan` shows `new-core-blocked` until `--adopt-collisions`; `verify_integrity` accepts an edited copy; no `eol=crlf` pattern matches a Cairn-installed path; `git check-attr -a` finds no live attributes file under `dev/.cairn/base/`. Run via `python tools/test_tiers.py for <paths>`. Falsified if any path overwrites an existing file.

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

## Response -- Claude Sonnet 5.5 (author) -- 2026-11-16

**Elapsed**: about 12 minutes (15:30 to 15:42 EST)
**Tokens**: unknown.

Both blocking findings are accepted and fixed. Operative text revised in place; the reviews are unchanged.

**Ordinary review**
1. **Accepted (blocking).** Dependencies now cites the archived defects proposal, its Decision (diagnostic only, no folding before hashing, landed at `c62d18fa`), and states the tier conflict. I keep standard: the install set and lockfile step are protected contracts and the work needs a plan and Security Review, which light lacks.
2. **Accepted.** Citations fixed: `lockfile.py:201`, `upgrade.py:1040-1080`, `install.py:2321-2323` and 2343-2359 (checked).
3. **Accepted.** Step 2 names the `install.py:367` special case; step 3 says a kept file gets no record, `new-core-blocked` repeats every upgrade, and one `--adopt-collisions` ends it.
4. **Accepted.** Brownfield install counts `i/crlf` files and prints the guide step.
5. **Accepted.** "Safe defaults" softened; renormalizing, `.sln`/`.reg` and `-text` for data files added.
6. **Accepted.** Fresh clone named as the one safe re-checkout.
7. **Accepted.** Step 4 answers it: one tamper signal is removed, for one file; no integrity check reads attributes; the residual is named.

**Security Review**
1. **Accepted (blocking).** The exemption names `.gitattributes` alone; any other differing file still stops the lockfile. Both tests added (steps and verification).
2. **Accepted.** Plan installs the mapping verbatim, so no copy under `dev/.cairn/base/`; a check-attr test is added. Cost: later upstream edits show as a fork, not a three-way merge.
3. **Accepted.** Residual stated beside the entry and in the guide surface.
4. **Accepted.** Content notes the `eol=crlf` constraint; test added.
5. **Declined here.** Existing `git_read` and `ident` behavior is a separate item, not widened by this change; it needs its own proposal if wanted. Not verified by me.

Not run: tests, installer, Windows. Over target (about 330 words) for 12 findings.

**For the Maintainer.**
1. Tier: your Decision called this follow-on light; the draft proposes standard. Default: standard with plan and Security Review. Pick light only if you accept an engine edit with no plan.
2. Verbatim install (finding S2) gives up three-way upstream merges for this file. Default: verbatim.
3. Item 5 (`git_read`/`ident`): separate item, default not opened now.

## Decision -- Maintainer (scribed by Antigravity Gemini 4 Hydrogen) -- 2026-11-16

**Tier**: standard

**ACCEPTED.**

> "Accept both as revised with the recommended defaults"

This accepts Option A as revised (`standard` tier with plan and Security Review), adopting the author's defaults (verbatim install without a `dev/.cairn/base/` copy, and leaving the `git_read`/`ident` item separate). New recurring human operations: zero (aside from the one-time release AST/gate update after engine edits).

**Elapsed:** under 1 minute. **Tokens:** unknown.
