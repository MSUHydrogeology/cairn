"""Security-gate tests for the lifecycle skills (Chunk 5 of the executing plan
`2026-06-01-claude-cairn-vendor-neutral-skills`).

The skills widen Cairn's agent-instruction supply chain (an executable CLI + a
trusted activation `description`), so security is a first-class acceptance gate:

* **S4 content-scan** over every agent-ingested artifact -- the canonical
  ``SKILL.md`` sources *and* the rendered/installed copies *and* the CLI --
  using the shipped ``content_scan`` tripwire (credential / exfiltration /
  prompt-injection patterns); a flag fails the build.
* **S5 no-network / bounded surface** -- the CLI opens no in-process socket, and
  its source imports no network client.
* **S3 path-containment** -- a crafted ``CAIRN_AGENT`` cannot redirect the
  reflection write outside ``dev/reflections/``.
* **per-artifact integrity** -- each installed skill artifact's on-disk hash
  matches the ``dev/cairn-lock.yml`` record (so an upgrade tells an adopter edit
  from tampering).
* **generated-output leak test (D6)** -- the tracked / installed artifacts carry
  no local path, IP, token, or maintainer alias.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_skills_security.py
"""
from __future__ import annotations

import hashlib
import importlib.util
import re
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap.scaffold import main, read_lockfile  # noqa: E402

TEMPLATES_ROOT = CAIRN_ROOT / "templates"
LIFECYCLE_SRC = TEMPLATES_ROOT / "skills" / "_lib" / "lifecycle.py"
CONTENT_SCAN_SRC = TEMPLATES_ROOT / "modules" / "team-gated" / "content_scan.py"
SKILL_SOURCES = sorted((TEMPLATES_ROOT / "skills").glob("*/SKILL.md"))

pytestmark = pytest.mark.skipif(
    not LIFECYCLE_SRC.exists(), reason="templates/skills not available",
)


def _load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod  # so @dataclass can resolve cls.__module__
    spec.loader.exec_module(mod)
    return mod


lifecycle = _load("cairn_lifecycle_sec", LIFECYCLE_SRC)
content_scan = _load("cairn_content_scan", CONTENT_SCAN_SRC)


# --- S4: content-scan over source + rendered artifacts ----------------------


@pytest.mark.parametrize(
    "artifact", [LIFECYCLE_SRC, *SKILL_SOURCES],
    ids=lambda p: p.name if p.name != "SKILL.md" else p.parent.name,
)
def test_canonical_artifacts_pass_content_scan(artifact: Path):
    flags = content_scan.scan_file(artifact)
    assert flags == [], f"{artifact} tripped the content scanner: {flags}"


def test_installed_artifacts_pass_content_scan(tmp_path: Path):
    target = _scaffold(tmp_path)
    for rel in (
        ".agents/skills/session-start/SKILL.md",
        ".agents/skills/session-end/SKILL.md",
        "tools/lifecycle.py",
    ):
        assert content_scan.scan_file(target / rel) == [], rel


# --- S5: no network / bounded surface ---------------------------------------


def test_cli_source_imports_no_network_client():
    src = LIFECYCLE_SRC.read_text(encoding="utf-8")
    for needle in ("urllib", "http.client", "requests", "urlopen",
                   "create_connection", "curl", "wget"):
        assert needle not in src, f"network primitive in lifecycle CLI: {needle}"


def test_session_start_opens_no_socket(tmp_path, monkeypatch, capsys):
    repo = _git_repo(tmp_path)

    opened = {"n": 0}

    def _boom(*a, **k):
        opened["n"] += 1
        raise AssertionError("lifecycle opened a socket")

    monkeypatch.setattr(lifecycle.socket, "socket", _boom)
    monkeypatch.chdir(repo)

    rc = lifecycle.main(["session-start"])
    assert rc == 0
    assert opened["n"] == 0  # bounded surface: no in-process socket


# --- S3: path-containment on the reflection write ---------------------------


def test_crafted_agent_cannot_escape_reflections(tmp_path, monkeypatch):
    repo = _git_repo(tmp_path)
    monkeypatch.setenv("CAIRN_AGENT", "../../../escape")
    monkeypatch.chdir(repo)

    rc = lifecycle.main(["session-end"])
    assert rc == 0

    # No file landed outside dev/reflections/ ...
    assert not (repo.parent / "escape.md").exists()
    assert not (repo / "escape.md").exists()
    # ... and the sanitized reflection is inside it.
    written = list((repo / "dev" / "reflections").glob("*.md"))
    assert written, "no reflection written"
    for p in written:
        p.resolve().relative_to((repo / "dev" / "reflections").resolve())


def test_assert_within_rejects_traversal(tmp_path):
    base = tmp_path / "dev" / "reflections"
    base.mkdir(parents=True)
    with pytest.raises(lifecycle.LifecycleError):
        lifecycle._assert_within(base / ".." / ".." / "evil.md", base)


# --- per-artifact integrity + D6 leak test ----------------------------------


def test_installed_artifacts_match_lockfile_hash(tmp_path: Path):
    target = _scaffold(tmp_path)
    lock = read_lockfile(target)
    assert lock is not None
    skill_dsts = {
        ".agents/skills/session-start/SKILL.md",
        ".agents/skills/session-end/SKILL.md",
        "tools/lifecycle.py",
    }
    for rec in lock["files"]:
        if rec["dst"] not in skill_dsts:
            continue
        on_disk = (target / rec["dst"]).read_bytes()
        digest = "sha256:" + hashlib.sha256(on_disk).hexdigest()
        assert digest == rec["hash"], f"integrity mismatch: {rec['dst']}"


def test_tracked_artifacts_have_no_local_path_or_token_leak(tmp_path: Path):
    target = _scaffold(tmp_path)
    ip_re = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
    for rel in (
        ".agents/skills/session-start/SKILL.md",
        ".agents/skills/session-end/SKILL.md",
        "tools/lifecycle.py",
    ):
        text = (target / rel).read_text(encoding="utf-8")
        assert "/Users/" not in text and "/home/" not in text, rel
        assert "kendal" not in text.lower(), rel
        assert not ip_re.search(text), f"IP-like token in {rel}"
    # The interpreter binding is the one place an absolute path is allowed --
    # and it is untracked (gitignored), so it is not a commit leak.
    assert "dev/.cairn/local-env.json" in (
        target / ".gitignore"
    ).read_text(encoding="utf-8")


# --- helpers -----------------------------------------------------------------


def _scaffold(tmp_path: Path) -> Path:
    target = tmp_path.resolve()
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: SecTest\ntest_command: pytest\nmodules: []\n",
        encoding="utf-8",
    )
    assert main([
        "--config", str(cfg), "--target", str(target),
        "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
    ]) == 0
    return target


def _git_repo(tmp_path: Path) -> Path:
    import subprocess
    root = tmp_path.resolve()
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "t@e.com"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "T"], cwd=root, check=True)
    (root / "f.txt").write_text("x", encoding="utf-8")
    subprocess.run(["git", "add", "f.txt"], cwd=root, check=True, capture_output=True)
    subprocess.run(
        ["git", "-c", "commit.gpgsign=false", "commit", "-q", "-m", "init"],
        cwd=root, check=True, capture_output=True,
    )
    return root
