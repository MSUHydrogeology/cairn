# Cairn development environments

Project-local reference, not shipped methodology. Verified 2026-11-03; check
versions again before a new validation run.

## macOS

The canonical project interpreter is
`$HOME/conda_envs/lhm/bin/python3.13` (Python 3.13.13). Invoke that interpreter
explicitly for Cairn checks rather than relying on the shell's `python`.

For Python 3.12 compatibility runs, `$HOME/conda_envs/miniforge3/bin/python3.12`
(Python 3.12.9, pytest 9.0.3) was used on 2026-11-13. It is not the certifying
interpreter.

### Graphical signing prompt

The local Homebrew installation includes `ssh-askpass` 1.5.1. For
`repin.py baseline-install` and manual release-tag signing, select it in the
Maintainer's Terminal before running the signing command:

```sh
export SSH_ASKPASS=/opt/homebrew/bin/ssh-askpass
export SSH_ASKPASS_REQUIRE=force
```

These settings apply to that Terminal and its children; they do not load a key
into `ssh-agent`. No background service was enabled. The existing
[Maintainer-only signing procedure](../../bootstrap/REANCHOR_RUNBOOK.md)
still applies. Both signing paths worked with this prompt on 2026-11-03.

## Windows VM

UTM hosts Windows ARM64. The configured SSH alias is `cairn-windows`.
Authentication stays in the host's SSH configuration; no credentials belong
in this note.

The existing base Miniconda interpreter is:

```text
C:\ProgramData\miniconda3\python.exe
```

It reports Python 3.13.17 (ARM64) and pytest 9.2.0; Git reports
2.56.0.windows.4. Miniconda is not on the SSH login's command path: plain
`python` reaches the Windows Store alias and `py` is absent. Use the explicit
interpreter path, for example:

```sh
ssh cairn-windows "C:\ProgramData\miniconda3\python.exe -m pytest --version"
```

The VM's `lhm` conda environment, `C:\ProgramData\miniconda3\envs\lhm\python.exe`,
is an x64 (emulated) Python 3.13.18 with pytest 9.2.0, so a Windows run can use
either the native ARM64 or the x64 build. The 2026-11-13 rerun used both; its
steps and results are in `dev/measurement/windows-native-rerun-2026-11-13.md`.
Run files with `-rfsE` so setup errors are listed with the failures.

Use a new disposable validation folder rather than overwriting an existing
project checkout. Record the Windows interpreter separately from the macOS
canonical one; a simulated Windows path test is not native Windows evidence.

### Tools and packages the VM does not put on `PATH`

Checked 2026-11-13 by a read-only directory listing and `where` over SSH.

- **OpenSSL.** `test_web_hosting_security.py` (16 setup errors in the x64 run,
  one in the ARM64 run) builds certificate fixtures with `openssl`, through the
  fixture at `bootstrap/tests/test_security_net.py:948`, and stops with
  "openssl is required to generate the A-7 certificate fixtures" when `PATH`
  has none. `where openssl` finds nothing on the VM. The copy found is the one
  Git for Windows ships: `C:\Program Files\Git\usr\bin\openssl.exe`. Put that
  folder on `PATH` for the pytest process only, never system-wide:

  ```sh
  ssh cairn-windows 'cd /d C:\Users\cairn\<folder> && set "PATH=C:\Program Files\Git\usr\bin;%PATH%" && C:\ProgramData\miniconda3\envs\lhm\python.exe -m pytest -q -p no:cacheprovider -rfsE <nodes>'
  ```

  The folder was listed, not run: nothing here shows the change makes any of
  those files pass. The 2026-11-13 run with Git's tools folder on `PATH` still
  had 27 failures across the web-hosting, API-access and security-stack files,
  and their causes were not read. The folder also puts Git's `sh.exe` and other
  POSIX tools ahead of the Windows ones for that process.
- **PyYAML.** The base ARM64 Python has none, so
  `test_model_selection_stub.py::TestFidelityCheck::test_cli_success_no_error_output`
  fails there ("structural validation skipped: PyYAML not installed"). The
  `lhm` x64 environment has it and the same node passed. Run that file under
  `lhm`; do not install packages into the base Python without the Maintainer's
  go-ahead.
- **Git.** `where git` finds `C:\Program Files\Git\cmd\git.exe`
  (2.56.0.windows.4). The Windows worker in `templates/skills/_lib/git_read.py`
  runs real Git only after a test binds the verified helper bytes
  (`bind_verified_source`). A test that calls it unbound gets a failed read
  (`verified-helper-buffer-unavailable`, or `hook-index-repository-unavailable`
  through the hook-index route) and some real-Git tests skip with "Git 2.44 or
  newer is required"; that is a test setup gap, not a missing Git.

The shell's `python3` may select Python 3.12. Use the explicit canonical interpreter above for Cairn's own certification and record the interpreter used for compatibility checks. Python 3.12 compatibility for the shared Git reader and installed entry points is tracked in the Python 3.12 support plan.

## Shared Linux VM

Verified 2026-11-12. Start **Linux Development** in UTM, then connect from the Mac:

```sh
ssh linux-dev
```

This is a general development VM for projects on this Mac. The SSH alias in
the Mac's configuration selects the `cairn` guest account, dedicated key and
loopback-only connection at `127.0.0.1:2228`. No mouse or keyboard capture is
needed. Concurrent SSH sessions work; use separate project folders under
`~/projects` and a separate `.venv` for each project. Independent test runs
should use separate working folders. Follow the project's coordination rules
when agents edit a shared checkout, and coordinate shutdown with other users.

| Tool / resource | Verified value |
|---|---|
| Guest | Ubuntu 24.04 LTS, ARM64 (`aarch64`) |
| Python | 3.12.3; `python3 -m venv` works |
| Base pytest | 7.4.4; install each project's test dependencies in its venv |
| Git | 2.56.1, selected in SSH sessions |
| Capacity | 2 CPU cores, 3 GiB RAM, 64 GiB virtual disk |

Git is built from checksum-verified official upstream source in
`~/opt/git-2.56.1` and selected by the guest's `.bashrc`. Ubuntu's stock Git
and package sources remain intact. This separate Git build needs its own
updates; Ubuntu's package updater does not update it. No host directory is
shared automatically. Transfer each project's files to its own working folder.

Cairn's Linux Python 3.12 compatibility checks use this VM. Cairn's certifying
run continues to use the canonical macOS Python 3.13 interpreter above.
