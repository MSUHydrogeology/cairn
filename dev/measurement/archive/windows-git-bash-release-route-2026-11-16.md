# Windows Git Bash release routes, 2026-11-16

A record of one run of both release routes in `bootstrap/PROVENANCE.md` under
Git Bash on the Windows VM. It is the evidence behind the dated Windows
sentence there, and it is the baseline to re-run when `bootstrap/` is renamed
by the repository layout work (`dev/proposals/2026-11-09-claude-repository-layout.md`).
Proposal: `dev/proposals/2026-11-16-claude-release-route-documentation.md`.

## Result

Both routes ran to the end in Git Bash with no change to their commands. The
ordinary route fetched `v0.7.0`, matched it to the release notes and made a
clean checkout. The stronger route verified the real signature on `v0.7.0`
against a roster file written from the release key, and refused a roster
holding a different key. The one thing that failed is outside the route
commands: a bare `python` in Git Bash is the Microsoft Store stub, so the
documented `python bootstrap/verify_integrity.py ...` needed the real
interpreter's full path.

## What was run

- **Date and place.** 2026-11-16, about 17:24 to 17:28 UTC, on the VM reached
  as `cairn-windows` (Windows ARM64 build 10.0.26300 under UTM). A new folder,
  `C:\Users\cairn\cairn-release-route-20261116`, held everything; no existing
  checkout was touched and no system setting or package was changed.
- **How Git Bash was started.** By its full path, from the SSH session:
  `"C:\Program Files\Git\bin\bash.exe" <script file>`. This is a
  non-interactive shell, not the Start-menu entry; the Start-menu launch was
  not run.
- **Versions (measured).** GNU bash 5.3.15; Git 2.56.0.windows.4 (ARM64 build,
  `/clangarm64/bin/git`); curl 8.23.0; GNU Awk 5.4.1; mktemp (GNU coreutils)
  8.32; Python 3.13.17 at `C:\ProgramData\miniconda3\python.exe`.
- **Commands.** The route blocks were cut verbatim from `bootstrap/PROVENANCE.md`
  at commit `7ce6d5f1` (ordinary route step 1 and steps 2-3; stronger route
  step 2 and the bootstrap block between its two `cairn:bootstrap-block`
  markers) and run as `bash <file>`, the same way
  `bootstrap/tests/test_verify_ref.py` runs the block. Only the documented
  inputs were set: the tag `v0.7.0`, its percent-encoded form (the same),
  version `0.7.0`, and the full commit `2f9fda2ba410077e2523547b8ef3c055257ea61d`
  from the release notes; the candidate was the literal official URL. For
  stronger-route step 2 `HOME` was pointed at a folder inside the disposable
  folder, so `~/.config/cairn/release-signers` landed there and not in the VM
  user's real home.

## Which tool each name resolved to

Inside Git Bash, `command -v`:

| Name | Resolved to |
|---|---|
| `sh` | `/usr/bin/sh` |
| `awk` | `/usr/bin/awk` |
| `mktemp` | `/usr/bin/mktemp` |
| `ssh-keygen` | `/usr/bin/ssh-keygen` (Git's own copy) |
| `git` | `/clangarm64/bin/git` |
| `curl` | `/clangarm64/bin/curl` |
| `test` | shell built-in |
| `python`, `python3` | `/c/Users/cairn/AppData/Local/Microsoft/WindowsApps/python` (the Store stub) |

On the plain SSH login (`where` in `cmd`), by contrast: `bash`, `sh`, `awk` and
`mktemp` are not found; `ssh-keygen` is `C:\Windows\System32\OpenSSH\ssh-keygen.exe`;
`curl` is `C:\Windows\System32\curl.exe`; `python` is the same Store stub. So
the route needs Git Bash started explicitly.

## Results

| Step | Outcome |
|---|---|
| Ordinary route step 1 (two `curl` calls, `--max-redirs 0`) | Both exited 0 and printed `200`. The API fields read: `tag_name` `v0.7.0`, canonical `html_url`, `draft` false, `prerelease` false, `published_at` 2026-11-13T16:51:00Z; the release notes name commit `2f9fda2b...`. |
| Ordinary route steps 2-3 (isolated bare repo, one-tag fetch, detached checkout) | Exit 0. `refs/tags/v0.7.0` was an annotated tag; its commit equalled the notes' commit; 999 files checked out. |
| Pre-execution checks (`rev-parse HEAD`, `diff --quiet`, `status --porcelain ...`) | `HEAD` equalled the full commit; `diff --quiet` exit 0; status empty. |
| Stronger route step 2 (write the roster, print the fingerprint) | Exit 0; `ssh-keygen -l -f` printed a `SHA256:` line. The roster key came from GitHub's public signing-key endpoint for the Maintainer's account, one channel only. |
| Stronger route step 3 (bootstrap block, official URL) | Exit 0. `verify-tag` printed `Good "git" signature for cairn-release` with the same fingerprint as step 2; the block printed `PROVENANCED: tag 'v0.7.0' (object 49dfa217...), commit 2f9fda2b...`. The same three pre-execution checks passed on its checkout. |
| Negative control (a freshly generated key as the roster) | Exit 1: `No principal matched.` then `REFUSED: the signature on 'v0.7.0' did not verify against <roster>`. The check can fail on Windows. |
| `/dev/null` isolation (the open question in the proposal's Context) | A planted global `user.name` showed by default and was gone with `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_SYSTEM=/dev/null` set. A `pre-commit` hook ran by default and did not run with `-c core.hooksPath=/dev/null`. |
| The new installer line's command, run on the `v0.7.0` checkout | `scaffold.py --config <solo-greenfield profile> --target <fresh git repo>` exited 0; `verify_integrity.py --target <that repo>` printed `OK -- 46 recorded file(s) match dev/.cairn/cairn-lock.yml` and exited 0, both with the full path to Python 3.13.17. |

## What failed

- **`python` in Git Bash.** `python bootstrap/verify_integrity.py --target ...`
  printed "Python was not found; run without arguments to install from the
  Microsoft Store..." and exited 49, because the first `python` on the path is
  the Store alias. With the interpreter's full path the same command passed.
  The route commands themselves do not call Python; the installer step does.
  I did not change any setting (disabling the alias is a system setting).
- Nothing else failed. No command needed a fix.

## What this did not cover

- A Start-menu or login-shell Git Bash. The path order there (`/mingw64/bin`
  then `/usr/bin`, or `/clangarm64/bin` on ARM64) is from Git for Windows'
  profile, not measured here; this run used a non-login shell.
- The route with Windows' own `ssh-keygen.exe` first on the path, and an x64
  Git for Windows (this VM has the ARM64 build).
- `bootstrap/tests/test_verify_ref.py` on Windows.
- The refusal cases other than a wrong roster key (a substituted tag name, an
  unsigned or lightweight tag, a redirect, a non-200 reply, a dirty checkout).
- The two-channel fingerprint comparison in Step 1 of the stronger route. It is
  a person's procedure, not a command; this run used one channel to test the
  commands, not the independence.
- The `UPGRADE.md` upgrade routes, and anything run against a prerelease.
- Whether a person ends up with the same result when pasting a block into an
  interactive Git Bash window; the run used script files.

## Cleanup

The three scratch workspaces the routes made under `/tmp` were removed after
the checks. The disposable folder remains on the VM for the Maintainer to
delete.
