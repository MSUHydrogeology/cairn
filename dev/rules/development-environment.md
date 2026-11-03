# Cairn development environments

Project-local reference, not shipped methodology. Verified 2026-11-03; check
versions again before a new validation run.

## macOS

The canonical project interpreter is
`$HOME/conda_envs/lhm/bin/python3.13` (Python 3.13.13). Invoke that interpreter
explicitly for Cairn checks rather than relying on the shell's `python`.

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

Use a new disposable validation folder rather than overwriting an existing
project checkout. Record the Windows interpreter separately from the macOS
canonical one; a simulated Windows path test is not native Windows evidence.
