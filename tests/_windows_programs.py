"""Small programs a test puts on a path, in a form every host can start.

A POSIX host starts a script by its `#!` line. Windows starts a program by its
executable format and finds it by a name that ends in `.exe`, so a script named
`git` or `gitleaks` cannot stand in there. On Windows each program placed by
`place_program` is a compiled launcher with the script appended to it as a zip
archive: the launcher runs `<python> <its own file> <arguments>`, and Python runs
a file that ends in a zip archive. The script is part of the file, so a change to
the script is a change to the file's bytes, which tests of digests and of a file
swapped after it was checked rely on. The launcher is compiled once per process
with the .NET compiler every Windows ships, as
`tests/security/test_git_read_routes.py` does for its own stand-in.

Nothing here runs on a POSIX host except `link` and `program_name`.
"""
from __future__ import annotations

import atexit
import io
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

import pytest

#: ``SystemRoot`` and ``WINDIR``. Windows will not start a program that opens a
#: socket without them, so a test that gives a child program an explicit
#: environment adds these. Empty on a POSIX host.
SYSTEM_ENV: dict[str, str] = {
    key: os.environ[key] for key in ("SystemRoot", "WINDIR")
    if os.name == "nt" and key in os.environ
}

_LAUNCHER_SOURCE = r"""
using System;
using System.Diagnostics;
using System.Text;

internal static class Launcher
{
    private const string Python = @"@@PYTHON@@";

    private static string Quote(string arg)
    {
        if (arg.Length > 0 && arg.IndexOfAny(new char[] { ' ', '\t', '\n', '\v', '"' }) < 0)
        {
            return arg;
        }
        StringBuilder text = new StringBuilder("\"");
        int slashes = 0;
        foreach (char c in arg)
        {
            if (c == '\\') { slashes++; continue; }
            if (c == '"') { text.Append('\\', slashes * 2 + 1); text.Append('"'); slashes = 0; continue; }
            text.Append('\\', slashes); slashes = 0; text.Append(c);
        }
        text.Append('\\', slashes * 2);
        text.Append('"');
        return text.ToString();
    }

    private static int Main(string[] args)
    {
        string self = Process.GetCurrentProcess().MainModule.FileName;
        StringBuilder line = new StringBuilder(Quote(self));
        foreach (string arg in args) { line.Append(' '); line.Append(Quote(arg)); }
        ProcessStartInfo info = new ProcessStartInfo(Python, line.ToString());
        info.UseShellExecute = false;
        using (Process child = Process.Start(info))
        {
            child.WaitForExit();
            return child.ExitCode;
        }
    }
}
"""

_launcher: list[Path] = []


def _compile_launcher() -> Path:
    csc = (Path(os.environ.get("SystemRoot", r"C:\Windows")) / "Microsoft.NET"
           / "Framework64" / "v4.0.30319" / "csc.exe")
    assert csc.is_file(), "the Windows compiler for the stand-in programs is unavailable"
    folder = Path(tempfile.mkdtemp(prefix="cairn-launcher-"))
    atexit.register(shutil.rmtree, folder, True)
    source = folder / "launcher.cs"
    source.write_text(
        _LAUNCHER_SOURCE.replace("@@PYTHON@@", sys.executable), encoding="utf-8")
    output = folder / "launcher.exe"
    built = subprocess.run(
        [str(csc), "/nologo", "/out:" + str(output), str(source)],
        stdin=subprocess.DEVNULL, capture_output=True, timeout=120, check=False)
    assert built.returncode == 0, (built.stdout + built.stderr).decode("utf-8", "replace")
    return output


def program_name(name: str) -> str:
    """The file name a program called *name* has on this host."""
    return name + ".exe" if os.name == "nt" else name


def place_program(path: Path, body: str) -> Path:
    """Write the Python script *body* (its first line a `#!` line) as an
    executable at *path* and return the file a path search will find: *path*
    itself on a POSIX host, *path* with `.exe` added on Windows.

    The script sees its own file as ``sys.argv[0]``; it must not use
    ``__file__``, which on Windows names a place inside the archive."""
    if os.name != "nt":
        path.write_text(body, encoding="utf-8")
        path.chmod(0o755)
        return path
    if not _launcher:
        _launcher.append(_compile_launcher())
    script = body.split("\n", 1)[1]
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, "w") as zipped:
        zipped.writestr("__main__.py", script)
    program = path.with_name(program_name(path.name))
    program.write_bytes(_launcher[0].read_bytes() + archive.getvalue())
    return program


def make_symlink(path: Path, target: Path) -> None:
    """Make *path* a symbolic link to *target*; skip only when Windows withholds
    the privilege to make one."""
    try:
        path.symlink_to(target)
    except OSError as error:
        if os.name == "nt" and getattr(error, "winerror", None) == 1314:
            pytest.skip("this Windows account cannot create symbolic links")
        raise
