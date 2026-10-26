"""The retired agreement is absent from new installs but preserved on upgrade.

These tests exercise the public scaffold and upgrade entry point. An older
project is modeled by adding its former living-state record and cached base
to a fresh scratch install; no historical git checkout is required.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap import scaffold as s  # noqa: E402
from bootstrap.verify_integrity import verify  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
OLD = "dev/collaboration_agreement.md"
ROLES = "dev/agent_collaboration.md"


def _install(target: Path, preset: str = "solo-greenfield") -> None:
    target.mkdir(parents=True)
    profile = target / "profile.yml"
    profile.write_text(
        "project_name: AgreementRetirementTest\n"
        "test_command: pytest\n"
        "python_package: agreement_test\n"
        f"preset: {preset}\n",
        encoding="utf-8",
    )
    assert s.main([
        "--config", str(profile), "--target", str(target),
        "--cairn-root", str(ROOT), "--allow-dev",
    ]) == 0


def _old_project(target: Path) -> tuple[Path, Path, dict]:
    _install(target)
    old_file = target / OLD
    old_file.write_text("# Project-owned agreement\nLocal terms stay.\n", encoding="utf-8")
    base = target / "dev/.cairn/base/dev/collaboration_agreement.md"
    base.parent.mkdir(parents=True, exist_ok=True)
    base.write_text("# Former upstream agreement\n", encoding="utf-8")
    lock = s.read_lockfile(target)
    assert lock is not None
    record = {
        "dst": OLD,
        "src": "core/dev/collaboration_agreement.md",
        "verbatim": False,
        "living_state": True,
        "hash": "sha256:" + hashlib.sha256(old_file.read_bytes()).hexdigest(),
        "base_cache": "dev/.cairn/base/dev/collaboration_agreement.md",
        "base_hash": "sha256:" + hashlib.sha256(base.read_bytes()).hexdigest(),
    }
    lock["files"].append(record)
    (target / "dev/.cairn/cairn-lock.yml").write_text(
        s._emit_lock_yaml(lock), encoding="utf-8",
    )
    return old_file, base, record


@pytest.mark.parametrize(
    "preset", ("solo-greenfield", "collaborative-team", "high-rigor-legacy")
)
def test_fresh_installs_have_roles_but_no_agreement(
    tmp_path: Path, preset: str,
) -> None:
    target = tmp_path / preset
    _install(target, preset)
    assert not (target / OLD).exists()
    assert (target / ROLES).is_file()
    lock = s.read_lockfile(target)
    assert lock is not None
    assert OLD not in {rec["dst"] for rec in lock["files"]}
    assert verify(target) == 0


def test_old_agreement_is_reported_once_and_unchanged_by_upgrade(
    tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    target = tmp_path / "project"
    old_file, base, record = _old_project(target)
    assert verify(target) == 0
    before = (old_file.read_bytes(), base.read_bytes(), record.copy())
    assert s.main(["upgrade", "--target", str(target), "--plan",
                   "--cairn-root", str(ROOT)]) == 0
    report = capsys.readouterr().out
    assert len(re.findall(
        rf"^\s*retired, kept\s+1: {re.escape(OLD)}$", report, re.M,
    )) == 1, report
    assert s.main(["upgrade", "--target", str(target), "--stage",
                   "--cairn-root", str(ROOT)]) == 0
    assert s.main(["upgrade", "--target", str(target), "--apply",
                   "--cairn-root", str(ROOT)]) == 0
    after_lock = s.read_lockfile(target)
    assert after_lock is not None
    after_record = next(rec for rec in after_lock["files"] if rec["dst"] == OLD)
    assert (old_file.read_bytes(), base.read_bytes(), after_record) == before
    assert verify(target) == 0


def test_missing_old_file_refuses_bare_finalize_but_empty_file_survives(
    tmp_path: Path,
) -> None:
    target = tmp_path / "project"
    old_file, _, _ = _old_project(target)
    old_file.unlink()
    assert s.main(["upgrade", "--target", str(target), "--finalize",
                   "--cairn-root", str(ROOT)]) != 0
    old_file.write_text("", encoding="utf-8")
    assert s.main(["upgrade", "--target", str(target), "--finalize",
                   "--cairn-root", str(ROOT)]) == 0
    assert verify(target) == 0


def test_moved_roster_needs_explicit_integrity_finalization(
    tmp_path: Path,
) -> None:
    target = tmp_path / "project"
    _install(target)
    roles = target / ROLES
    text = roles.read_text(encoding="utf-8")
    default = (
        "(The bootstrap records the team here: the maintainer; the human\n"
        "contributors and their roles; the agents and their types.\n"
        "Refreshed when the team changes.)"
    )
    assert default in text
    roles.write_text(
        text.replace(default, "* Claude Opus -- author\n* Codex GPT -- reviewer"),
        encoding="utf-8",
    )
    assert verify(target) == 1
    assert s.main(["upgrade", "--target", str(target), "--finalize", ROLES,
                   "--cairn-root", str(ROOT)]) == 0
    assert verify(target) == 0


def _retired_citations(sources: dict[str, str]) -> list[str]:
    return [
        name for name, body in sources.items()
        if OLD in body or "collab-agreement-signing" in body
        or "sign-collab-agreement" in body
    ]


def test_no_install_source_cites_the_retired_path_or_trigger() -> None:
    rows = s.install_manifest(modules=None)
    assert OLD in s._LIVING_STATE_DSTS
    assert OLD not in {dst for _src, dst, _verbatim in rows}
    suffixes = {".md", ".py", ".yml", ".yaml", ".json", ".toml", ".txt", ".sh", ".svg"}
    paths = {ROOT / "AGENTS.md"}
    for folder in ("templates", "dev/modules", "docs", "scripts"):
        paths.update(
            path for path in (ROOT / folder).rglob("*")
            if path.is_file() and path.suffix in suffixes
        )
    sources = {
        path.relative_to(ROOT).as_posix(): path.read_text(
            encoding="utf-8", errors="replace",
        )
        for path in paths
    }
    assert len(sources) > len(rows), "the scan must reach beyond manifest rows"
    assert _retired_citations(sources) == []
    victim = "templates/core/AGENTS.md"
    assert victim in sources
    planted = {**sources, victim: sources[victim] + f"\nSee {OLD}.\n"}
    assert _retired_citations(planted) == [victim]


def test_shipped_roles_retain_the_two_agreement_sentences_without_local_rule() -> None:
    shipped = (ROOT / "templates/core/dev/agent_collaboration.md").read_text(
        encoding="utf-8",
    )
    local = (ROOT / "dev/agent_collaboration.md").read_text(encoding="utf-8")
    shipped_flat = " ".join(shipped.split())
    assert "Agents propose, review, implement, and advise; they do not decide." in shipped_flat
    assert (
        "Acceptance, rejection, and supersession are the Maintainer's call. "
        "An agent unsure whether something is a decision surfaces it rather "
        "than assuming."
    ) in shipped_flat
    assert shipped.count("<!-- cairn:slot team-roster -->") == 1
    assert "The team" in shipped
    assert "The team" in local
    assert "short fixed list" not in shipped
