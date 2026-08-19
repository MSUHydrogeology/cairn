"""Tests for the lockfile provenance fields (`source_repository`,
`source_licenses`), per the executing plan `lockfile-provenance-fields`
(P1-P5).

Covers:

* Reader nodes -- `_cairn_provenance`'s degrade/parse behavior, including
  the load-bearing regression case (R12a): CITATION.cff's `license:` block
  is immediately followed by a `keywords:` block with its own `- ` items.
* Writer nodes -- a fresh install and `--init-lock` both carry the fields.
* Upgrade nodes -- the three-case `--stage`/`--apply` compatibility matrix:
  a new stage backfills; an old stage preserves an existing provenance-
  bearing lock's values; an old stage preserves a pre-provenance lock's
  *absence*, never writing a JSON `null` (the case the original
  `.get()`-chain design gets wrong). Plus a `--finalize` round-trip, which
  preserves but does not backfill.
* The shipped `run_security_audit.py` reader (which parses the lockfile
  itself, not via `read_lockfile`) stays compatible.
* The emitted lockfile header carries the declared-not-attested wording.
* Facade-identity coverage for `_cairn_provenance`.

**Not** `bootstrap/tests/test_upgrade.py` -- that file is in the gate
manifest's pinned `frozen_files` set; editing it produces `FROZEN-MODIFIED`
(a hard-stop hold), not a note. This file reads `FROZEN-NEW` (allowed).
Imports the install harness from `test_upgrade.py` by reference, not
duplication -- importing a frozen file does not modify it.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_lockfile_provenance.py
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap import scaffold as s  # noqa: E402
from bootstrap._scaffold.lockfile import _cairn_provenance, _emit_lock_yaml  # noqa: E402

from bootstrap.tests.test_upgrade import _install, _seed_profile  # noqa: E402

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"
_TEAM_GATED = TEMPLATES_ROOT / "modules" / "team-gated"

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)


def _read_lock_json(lock_path: Path) -> dict:
    """Strip the `#`-prefixed header comment lines, then JSON-parse."""
    lines = lock_path.read_text(encoding="utf-8").splitlines(keepends=True)
    body = "".join(line for line in lines if not line.startswith("#"))
    return json.loads(body)


def _write_lock_json(lock_path: Path, data: dict) -> None:
    lines = lock_path.read_text(encoding="utf-8").splitlines(keepends=True)
    header = "".join(line for line in lines if line.startswith("#"))
    lock_path.write_text(header + json.dumps(data), encoding="utf-8")


# --- Reader nodes -------------------------------------------------------


def test_cairn_provenance_degrades_on_absent_citation(tmp_path):
    assert _cairn_provenance(tmp_path) == ("unknown", [])


def test_cairn_provenance_stops_license_block_at_keywords(tmp_path):
    # The load-bearing regression case (R12a): a scanner that kept consuming
    # past the license: block would silently record keywords as licenses.
    (tmp_path / "CITATION.cff").write_text(
        'repository-code: "https://example.com/x"\n'
        "license:\n"
        "  - CC-BY-4.0\n"
        "  - MIT\n"
        "keywords:\n"
        "  - not-a-license\n",
        encoding="utf-8",
    )
    repo, licenses = _cairn_provenance(tmp_path)
    assert repo == "https://example.com/x"
    assert licenses == ["CC-BY-4.0", "MIT"]


def test_cairn_provenance_accepts_scalar_license(tmp_path):
    (tmp_path / "CITATION.cff").write_text("license: MIT\n", encoding="utf-8")
    _, licenses = _cairn_provenance(tmp_path)
    assert licenses == ["MIT"]


def test_cairn_provenance_on_cairns_own_citation_cff():
    # Regression against the live shape of Cairn's own CITATION.cff.
    repo, licenses = _cairn_provenance(CAIRN_ROOT)
    assert repo == "https://github.com/MSUHydrogeology/cairn-scientist-ai-teams"
    assert licenses == ["CC-BY-4.0", "MIT"]


# --- Writer nodes ---------------------------------------------------------


def test_fresh_install_lockfile_carries_provenance(tmp_path):
    assert _install(tmp_path) == 0
    lock = s.read_lockfile(tmp_path)
    expected_repo, expected_licenses = _cairn_provenance(CAIRN_ROOT)
    assert lock["source_repository"] == expected_repo
    assert lock["source_licenses"] == expected_licenses


def test_init_lock_synthesized_lockfile_carries_provenance(tmp_path):
    assert _install(tmp_path) == 0
    (tmp_path / "dev" / ".cairn" / "cairn-lock.yml").unlink()
    _seed_profile(tmp_path)
    assert s.main([
        "upgrade", "--init-lock", "--target", str(tmp_path),
        "--cairn-root", str(CAIRN_ROOT),
    ]) == 0
    lock = s.read_lockfile(tmp_path)
    expected_repo, expected_licenses = _cairn_provenance(CAIRN_ROOT)
    assert lock["source_repository"] == expected_repo
    assert lock["source_licenses"] == expected_licenses
    assert lock["migrated"] is True


# --- Upgrade nodes -- the three-case compatibility matrix ---------------


def test_apply_backfills_provenance_from_new_stage(tmp_path):
    """(i) new stage + pre-provenance lock -- backfill, matching
    _cairn_provenance(cairn_root) for the same root (the install-vs-apply
    parity invariant)."""
    assert _install(tmp_path) == 0
    assert s.main([
        "upgrade", "--stage", "--target", str(tmp_path),
        "--cairn-root", str(CAIRN_ROOT),
    ]) == 0
    assert s.main([
        "upgrade", "--apply", "--target", str(tmp_path),
        "--cairn-root", str(CAIRN_ROOT),
    ]) == 0
    lock = s.read_lockfile(tmp_path)
    expected_repo, expected_licenses = _cairn_provenance(CAIRN_ROOT)
    assert lock["source_repository"] == expected_repo
    assert lock["source_licenses"] == expected_licenses


def test_apply_preserves_existing_provenance_from_old_stage(tmp_path):
    """(ii) old stage (no new_source_* keys, simulating a stage produced
    before this change) applied to a lock that already carries provenance
    -- the existing values are preserved unchanged."""
    assert _install(tmp_path) == 0
    assert s.main([
        "upgrade", "--stage", "--target", str(tmp_path),
        "--cairn-root", str(CAIRN_ROOT),
    ]) == 0
    meta_path = tmp_path / "dev" / ".cairn-upgrade" / "stage-metadata.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta.pop("new_source_repository", None)
    meta.pop("new_source_licenses", None)
    meta_path.write_text(json.dumps(meta), encoding="utf-8")

    assert s.main([
        "upgrade", "--apply", "--target", str(tmp_path),
        "--cairn-root", str(CAIRN_ROOT),
    ]) == 0
    lock = s.read_lockfile(tmp_path)
    expected_repo, expected_licenses = _cairn_provenance(CAIRN_ROOT)
    assert lock["source_repository"] == expected_repo
    assert lock["source_licenses"] == expected_licenses


def test_apply_preserves_absence_from_old_stage_no_null(tmp_path):
    """(iii) old stage + pre-provenance lock -- absence preserved, never a
    JSON null -- the case the original .get()-chain design got wrong,
    reproduced by mutation testing during implementation."""
    assert _install(tmp_path) == 0
    lock_path = tmp_path / "dev" / ".cairn" / "cairn-lock.yml"
    lock = _read_lock_json(lock_path)
    lock.pop("source_repository", None)
    lock.pop("source_licenses", None)
    _write_lock_json(lock_path, lock)

    assert s.main([
        "upgrade", "--stage", "--target", str(tmp_path),
        "--cairn-root", str(CAIRN_ROOT),
    ]) == 0
    meta_path = tmp_path / "dev" / ".cairn-upgrade" / "stage-metadata.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta.pop("new_source_repository", None)
    meta.pop("new_source_licenses", None)
    meta_path.write_text(json.dumps(meta), encoding="utf-8")

    assert s.main([
        "upgrade", "--apply", "--target", str(tmp_path),
        "--cairn-root", str(CAIRN_ROOT),
    ]) == 0

    raw = lock_path.read_text(encoding="utf-8")
    new_lock = _read_lock_json(lock_path)
    assert "source_repository" not in new_lock
    assert "source_licenses" not in new_lock
    assert '"source_repository": null' not in raw
    assert '"source_licenses": null' not in raw


def test_finalize_preserves_but_does_not_backfill_provenance(tmp_path):
    """--finalize preserves whatever provenance the lockfile already has (or
    lacks) verbatim -- it does not backfill (R3a's stated limit:
    --finalize/--adopt-module do not backfill, only preserve)."""
    assert _install(tmp_path) == 0
    lock_path = tmp_path / "dev" / ".cairn" / "cairn-lock.yml"
    lock = _read_lock_json(lock_path)
    lock.pop("source_repository", None)
    lock.pop("source_licenses", None)
    _write_lock_json(lock_path, lock)

    assert s.main([
        "upgrade", "--finalize", "--target", str(tmp_path),
        "--cairn-root", str(CAIRN_ROOT),
    ]) == 0

    lock_after = s.read_lockfile(tmp_path)
    assert "source_repository" not in lock_after
    assert "source_licenses" not in lock_after


# --- run_security_audit.py compatibility ---------------------------------


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_run_security_audit_reader_tolerates_provenance_fields(tmp_path):
    """The shipped, hash-tracked run_security_audit.py reader parses the
    whole lockfile itself (not via read_lockfile) -- a provenance-bearing
    lockfile must not change its behavior. This is the actual Cairn-tree
    source; it installs verbatim into an adopter tree as
    scripts/run_security_audit.py, which does not exist in Cairn's own
    scripts/ (the module is team-gated / optional, not installed here)."""
    orch = _load(
        "run_security_audit_lockfile_probe",
        _TEAM_GATED / "run_security_audit.py",
    )
    assert _install(tmp_path) == 0
    lock_path = tmp_path / "dev" / ".cairn" / "cairn-lock.yml"
    lock = orch.load_lockfile(lock_path)
    assert lock["source_repository"]
    assert lock["source_licenses"]
    # required_apparatus_dsts must not choke on the new keys.
    dsts = orch.required_apparatus_dsts(lock)
    assert isinstance(dsts, list)


# --- The emitted lockfile header carries the declared-not-attested wording ---


def test_emitted_lockfile_header_states_declared_not_attested():
    out = _emit_lock_yaml({"schema": 1})
    assert "declared" in out


# --- Facade-identity coverage for _cairn_provenance -----------------------
# NOT bootstrap/tests/test_lockfile_module.py's _MOVED tuple -- that file is
# FROZEN in the gate manifest; this assertion lands here instead.


def test_cairn_provenance_single_identity_across_consumers():
    from bootstrap._scaffold import lockfile as LK  # noqa: PLC0415

    import bootstrap._scaffold as engine  # noqa: PLC0415
    import bootstrap.scaffold  # noqa: PLC0415,F401  (facade == engine)

    facade = sys.modules["bootstrap.scaffold"]
    obj = LK._cairn_provenance
    assert engine._cairn_provenance is obj
    assert facade._cairn_provenance is obj
