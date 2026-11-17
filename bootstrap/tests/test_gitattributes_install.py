"""Public install and Git behavior for the shipped root attributes file."""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

from bootstrap.tests._repo_root import repository_root

CAIRN_ROOT = repository_root(Path(__file__))
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap import scaffold as s  # noqa: E402
from bootstrap import verify_integrity  # noqa: E402
from bootstrap._scaffold import install as engine  # noqa: E402

TEMPLATES_ROOT = CAIRN_ROOT / "templates"
ATTRS = TEMPLATES_ROOT / "core" / "gitattributes.txt"
EXPECTED_TEMPLATE = b"""# Line endings. Text files are stored and checked out with LF on every machine,
# so a Windows checkout matches the repository and Cairn's recorded file hashes.
# Cairn installs this file only when the project has none, and never replaces
# yours. Edit the project choices below.
* text=auto eol=lf

# Windows scripts keep CRLF. Name only paths Cairn does not install, because
# Cairn records the hash of each installed file's LF bytes.
*.bat text eol=crlf
*.cmd text eol=crlf

# Binary files are never converted.
*.png binary
*.jpg binary
*.gif binary
*.pdf binary
*.zip binary
*.gz binary
*.tif binary
*.nc binary
*.h5 binary
*.npy binary

# Project choices: Cairn cannot know your paths. Uncomment and edit.
# Data and evidence that must stay byte for byte (raw instrument output):
# *.csv -text
# *.dat -text
# Files a Windows tool requires with CRLF:
# *.sln text eol=crlf
# *.reg text eol=crlf
"""


def _install(target: Path, extra: list[str] | None = None) -> int:
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: Demo\ntest_command: pytest\npreset: solo-greenfield\n",
        encoding="utf-8",
    )
    return s.main([
        "--config", str(cfg), "--target", str(target),
        "--cairn-root", str(CAIRN_ROOT), "--allow-dev", *(extra or []),
    ])


def _git(target: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    env = os.environ.copy()
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    return subprocess.run(
        ["git", *args], cwd=target, env=env, check=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )


def test_fresh_install_writes_the_file_and_records_it(tmp_path: Path) -> None:
    target = tmp_path.resolve()
    assert _install(target) == 0
    content = ATTRS.read_bytes()
    assert content == EXPECTED_TEMPLATE
    assert (target / ".gitattributes").read_bytes() == content
    rows = [r for r in s.read_lockfile(target)["files"]
            if r["dst"] == ".gitattributes"]
    assert len(rows) == 1
    row = rows[0]
    assert row["verbatim"] is True
    assert row["living_state"] is True
    assert "base_cache" not in row
    assert row["hash"] == "sha256:" + hashlib.sha256(content).hexdigest()


def test_an_existing_different_file_is_kept_byte_for_byte(
    tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    cases = [([], EXPECTED_TEMPLATE.replace(b"\n", b"\r\n")),
             (["--force"], b"# mine\n*.dat -text\n")]
    for index, (extra, existing) in enumerate(cases):
        target = (tmp_path / str(index)).resolve()
        target.mkdir(parents=True, exist_ok=True)
        (target / ".gitattributes").write_bytes(existing)
        assert _install(target, extra) == 0
        assert (target / ".gitattributes").read_bytes() == existing
        lock_path = target / "dev" / ".cairn" / "cairn-lock.yml"
        assert lock_path.is_file()
        destinations = {r["dst"] for r in s.read_lockfile(target)["files"]}
        assert {"AGENTS.md", "tools/board.py"} <= destinations
        assert ".gitattributes" not in destinations
        stderr = capsys.readouterr().err
        expected = [line for line in EXPECTED_TEMPLATE.decode("utf-8").splitlines()
                    if line.strip() and not line.lstrip().startswith("#")]
        assert all(line in stderr for line in expected)


def test_no_other_differing_file_gets_the_exemption(tmp_path: Path) -> None:
    target = tmp_path.resolve()
    target.mkdir(parents=True, exist_ok=True)
    (target / "tools").mkdir()
    (target / "tools" / "board.py").write_bytes(b"planted\n")
    (target / "NOTICE.md").write_bytes(b"planted\n")
    (target / ".gitattributes").write_bytes(b"# mine\n")
    assert _install(target) == 0
    assert (target / "tools" / "board.py").read_bytes() == b"planted\n"
    assert (target / ".gitattributes").read_bytes() == b"# mine\n"
    assert not (target / "dev" / ".cairn" / "cairn-lock.yml").exists()


def _write_lock(target: Path, lock: dict) -> None:
    lock_path = target / "dev" / ".cairn" / "cairn-lock.yml"
    lock_path.write_text(s._emit_lock_yaml(lock), encoding="utf-8")


def _upgrade_base(target: Path) -> list[str]:
    return ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]


def test_upgrade_keeps_it_blocked_until_adopted_and_adoption_saves_no_copy(
    tmp_path: Path,
) -> None:
    target = tmp_path.resolve()
    assert _install(target) == 0
    attrs = target / ".gitattributes"
    attrs.write_bytes(b"# mine\n")
    lock = s.read_lockfile(target)
    lock["files"] = [r for r in lock["files"] if r["dst"] != ".gitattributes"]
    _write_lock(target, lock)
    mine = attrs.read_bytes()

    lock = s.read_lockfile(target)
    plans, _ = s._compute_upgrade(target, CAIRN_ROOT, TEMPLATES_ROOT, lock, None)
    fp = next(p for p in plans if p.dst == ".gitattributes")
    assert fp.kind == "new-core-blocked"
    assert fp.src == "core/gitattributes.txt"
    assert fp.verbatim is True
    base = _upgrade_base(target)
    assert s.main(base + ["--stage"]) == 0
    assert s.main(base + ["--apply"]) != 0
    assert s.main(base + ["--apply", "--force"]) != 0
    assert attrs.read_bytes() == mine

    observed = s._sha256_hex(mine)
    upstream = s._sha256_hex((fp.theirs_raw or "").encode("utf-8"))
    triple = f".gitattributes@{observed}@{upstream}"
    assert s.main(base + ["--adopt-collisions", triple]) == 0
    assert attrs.read_bytes() == mine
    rec = next(r for r in s.read_lockfile(target)["files"]
               if r["dst"] == ".gitattributes")
    assert rec["verbatim"] is True
    assert rec["living_state"] is True
    assert "base_cache" not in rec
    assert rec["hash"] == "sha256:" + observed
    assert rec["base_hash"] == "sha256:" + upstream

    plans, _ = s._compute_upgrade(
        target, CAIRN_ROOT, TEMPLATES_ROOT, s.read_lockfile(target), None,
    )
    assert not any(p.dst == ".gitattributes" and p.kind == "new-core-blocked"
                   for p in plans)
    assert s.main(base + ["--stage"]) == 0
    assert s.main(base + ["--apply"]) == 0
    assert attrs.read_bytes() == mine
    _git(target, "init")
    assert list((target / "dev").rglob(".gitattributes")) == []
    assert _git(target, "check-attr", "-a", "--",
                 "dev/.cairn/base/AGENTS.md").stdout == b""


def test_verify_integrity_accepts_an_edited_copy(tmp_path: Path) -> None:
    target = tmp_path.resolve()
    assert _install(target) == 0
    attrs = target / ".gitattributes"
    attrs.write_bytes(attrs.read_bytes() + b"*.csv -text\n")
    assert verify_integrity.verify(target) == 0
    board = target / "tools" / "board.py"
    board.write_bytes(board.read_bytes() + b"\n# changed\n")
    assert verify_integrity.verify(target) != 0


def test_no_crlf_rule_matches_an_installed_path(tmp_path: Path) -> None:
    target = tmp_path.resolve()
    all_modules = sorted(s._MODULE_MAPPINGS)
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: Demo\ntest_command: pytest\n"
        "python_package: demo_pkg\nmodules:\n"
        + "".join(f"  - {name}\n" for name in all_modules),
        encoding="utf-8",
    )
    assert s.main([
        "--config", str(cfg), "--target", str(target),
        "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
    ]) == 0
    _git(target, "init")
    installed = sorted(
        str(path.relative_to(target)).replace(os.sep, "/")
        for path in target.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(target).parts
    )
    probes = [*installed, "probe.bat"]
    env = os.environ.copy()
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    result = subprocess.run(
        ["git", "check-attr", "--stdin", "-z", "eol"], cwd=target,
        env=env, input=("\0".join(probes) + "\0").encode("utf-8"),
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    fields = result.stdout.split(b"\0")
    rows = [fields[i:i + 3] for i in range(0, len(fields) - 2, 3)]
    crlf = {path.decode("utf-8") for path, attr, value in rows
            if attr == b"eol" and value == b"crlf"}
    assert "probe.bat" in crlf
    assert not (set(installed) & crlf)


@pytest.mark.parametrize(
    ("case", "line_endings"),
    [("crlf-in-index", b"\r\n"), ("lf-only", b"\n"),
     ("own-file-kept", b"\r\n"), ("read-unavailable", b"\r\n")],
)
def test_install_counts_crlf_files_in_the_index(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch,
    case: str, line_endings: bytes,
) -> None:
    version = subprocess.run(
        ["git", "--version"], check=True, capture_output=True, text=True,
    ).stdout.strip().split()[-1]
    numbers = tuple(int(part) for part in version.split(".")[:2])
    if numbers < (2, 45):
        pytest.skip(f"Git {version} is below the safe reader's 2.45 floor")
    target = tmp_path.resolve()
    target.mkdir(parents=True, exist_ok=True)
    (target / "first.txt").write_bytes(b"one" + line_endings)
    (target / "second.txt").write_bytes(b"two" + line_endings)
    if case == "own-file-kept":
        (target / ".gitattributes").write_bytes(b"# mine\n")
    _git(target, "init")
    _git(target, "-c", "core.autocrlf=false", "add", "-A")

    if case == "read-unavailable":
        helper = engine._git_read_helper()
        original = helper.run_git

        def unavailable(root: str, args: tuple[str, ...], **kwargs):
            if args == ("ls-files", "--eol"):
                return helper.ReadResult("failed", None, b"", "x")
            return original(root, args, **kwargs)

        monkeypatch.setattr(helper, "run_git", unavailable)
    assert _install(target) == 0
    captured = capsys.readouterr()
    report = captured.out + captured.err
    if case == "crlf-in-index":
        assert re.search(r"\[note\] 2 [^\n]*i/crlf", report)
    elif case == "read-unavailable":
        assert "ls-files --eol" in report
        assert "file(s) in the Git index have CRLF" not in report
    else:
        assert "i/crlf" not in report
        assert "ls-files --eol" not in report
