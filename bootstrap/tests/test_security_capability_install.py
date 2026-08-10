"""Tests for `api-web-security-modules` Chunk F, row **F5** -- the LANDING
part's acceptance criteria (F-1..F-6) for the two explicit-selection
capability modules, `api-access-security` and `web-hosting-security`:
the selection contract (explicit `modules_add` / an exact `modules:` list /
`modules_remove`; absence from every preset and the default-on set),
mapping-group completeness, the install-time capability notice, `upgrade`
/ `--adopt-module` behaviour, and **B2's installer-record field
vocabulary** (three parts: the exact writer vocabulary; the tried
impossibility at `verify_integrity`; and where B2 is actually satisfied --
recorded here, not implemented here).

**Scope: the landing part only** (F1, F3-F6). Every assertion here is
reachable with an empty registry, no living-state record, and no filled
policy -- Chunk F row **F2** (`_LIVING_STATE_DSTS`) is fenced and has not
landed, and Chunk G (the activation registry) has not landed either. This
file measures the tree **as it stands**; it does not assert the shape F2
will later produce. See the per-destination key-set note below for
exactly where that seam is.

Run from the Cairn repo root:
    python -m pytest bootstrap/tests/test_security_capability_install.py
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap import scaffold as s  # noqa: E402
from bootstrap._scaffold import install as _install_mod  # noqa: E402
from bootstrap._scaffold.install import (  # noqa: E402
    _CAPABILITY_NOTICE_MODULES,
    capability_install_notice_lines,
)
from bootstrap.verify_integrity import verify  # noqa: E402

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent

_CAPABILITY_MODULES = ("api-access-security", "web-hosting-security")

# The four statements F-6 / Chunk F row F3 require the notice to carry, for
# BOTH capabilities. Checked as substrings against rendered output, not
# reproduced as a full expected string, so this file does not silently pass
# by re-deriving the renderer's own text.
_NOTICE_FRAGMENTS = (
    "python scripts/api_access_security.py local",
    "python scripts/api_access_security.py deployed-passive "
    "--authorize-base-url",
    "python scripts/web_hosting_security.py local",
    "python scripts/web_hosting_security.py deployed-passive "
    "--authorize-base-url",
    "byte-for-byte",
    "No deployed credential is read during install or during local "
    "evidence.",
)


def _write_profile(path: Path, body: str) -> Path:
    path.write_text(
        "project_name: security-capability-test\n"
        "test_command: pytest\n" + body,
        encoding="utf-8",
    )
    return path


def _install(tmp_path: Path, body: str) -> tuple[int, Path]:
    cfg = _write_profile(tmp_path / "profile.yml", body)
    target = tmp_path / "target"
    target.mkdir(exist_ok=True)
    rc = s.main([
        "--config", str(cfg), "--target", str(target),
        "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
    ])
    return rc, target


def _summary_roster(output: str) -> set[str]:
    lines = output.splitlines()
    start = lines.index("Module roster (to install):") + 1
    roster = []
    for line in lines[start:]:
        if not line.startswith("  - "):
            break
        roster.append(line.removeprefix("  - "))
    return set(roster)


def _group_destinations(name: str) -> list[str]:
    """The destinations F1 registered for *name*, read off
    `_MODULE_MAPPINGS` itself (never hand-typed), so this file cannot
    silently drift from what F1 actually wired."""
    return [spec.dst for spec in s._MODULE_MAPPINGS[name]]


_ALL_CAPABILITY_DESTINATIONS = [
    dst for name in _CAPABILITY_MODULES for dst in _group_destinations(name)
]


# ---------------------------------------------------------------------------
# Selection contract: explicit modules_add / an exact modules: list /
# modules_remove
# ---------------------------------------------------------------------------

def test_modules_add_with_a_preset_installs_both_capabilities(
    tmp_path: Path,
) -> None:
    rc, target = _install(
        tmp_path,
        "preset: solo-greenfield\nmodules_add:\n  - api-access-security\n"
        "  - web-hosting-security\n",
    )
    assert rc == 0
    for dst in _ALL_CAPABILITY_DESTINATIONS:
        assert (target / dst).exists(), f"missing {dst}"


def test_an_exact_modules_list_installs_both_capabilities(
    tmp_path: Path,
) -> None:
    rc, target = _install(
        tmp_path,
        "modules:\n  - api-access-security\n  - web-hosting-security\n",
    )
    assert rc == 0
    for dst in _ALL_CAPABILITY_DESTINATIONS:
        assert (target / dst).exists(), f"missing {dst}"


def test_modules_remove_wins_over_modules_add(tmp_path: Path) -> None:
    rc, target = _install(
        tmp_path,
        "preset: solo-greenfield\nmodules_add:\n  - api-access-security\n"
        "  - web-hosting-security\nmodules_remove:\n  - web-hosting-security\n",
    )
    assert rc == 0
    for dst in _group_destinations("api-access-security"):
        assert (target / dst).exists(), f"missing {dst}"
    for dst in _group_destinations("web-hosting-security"):
        assert not (target / dst).exists(), f"should be absent: {dst}"


def test_neither_capability_installs_without_explicit_selection(
    tmp_path: Path,
) -> None:
    rc, target = _install(tmp_path, "preset: high-rigor-legacy\n")
    assert rc == 0
    for dst in _ALL_CAPABILITY_DESTINATIONS:
        assert not (target / dst).exists(), f"unexpectedly present: {dst}"


# ---------------------------------------------------------------------------
# F-5: no preset, no default-on -- and the erosion hazard
# ---------------------------------------------------------------------------

def _assert_absent_from_default_on(default_on) -> None:
    for name in _CAPABILITY_MODULES:
        assert name not in default_on, (
            f"{name} has leaked into the default-on set"
        )


def _assert_absent_from_every_preset_baseline(presets: dict) -> None:
    for preset, cfg in presets.items():
        baseline = set(cfg["baseline"])
        for name in _CAPABILITY_MODULES:
            assert name not in baseline, (
                f"{name} has leaked into preset {preset!r}'s baseline roster"
            )


def test_neither_capability_is_default_on() -> None:
    _assert_absent_from_default_on(s._DEFAULT_ON_MODULES)


def test_neither_capability_is_in_any_preset_baseline() -> None:
    _assert_absent_from_every_preset_baseline(s._PRESETS)


def test_hazard_default_on_erosion_is_caught() -> None:
    """F-5 hazard perturbation, default-on half: add a capability module to
    a PATCHED COPY of the default-on set and confirm the shared assertion
    helper actually fires -- proving the positive test above is not
    vacuously green."""
    patched = tuple(s._DEFAULT_ON_MODULES) + ("api-access-security",)
    with pytest.raises(AssertionError):
        _assert_absent_from_default_on(patched)


def test_hazard_preset_baseline_erosion_is_caught() -> None:
    """F-5 hazard perturbation, preset half: add one to a preset roster in
    a patched copy and confirm the test fails."""
    patched = dict(s._PRESETS)
    patched["solo-greenfield"] = {
        **patched["solo-greenfield"],
        "baseline": (
            tuple(patched["solo-greenfield"]["baseline"])
            + ("api-access-security",)
        ),
    }
    with pytest.raises(AssertionError):
        _assert_absent_from_every_preset_baseline(patched)


@pytest.mark.parametrize("preset", sorted(s._PRESETS))
def test_summary_lists_neither_capability_for_any_preset(
    preset: str, tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    cfg = _write_profile(tmp_path / "profile.yml", f"preset: {preset}\n")
    assert s.main(["--summary", "--config", str(cfg)]) == 0
    out = capsys.readouterr().out
    roster = _summary_roster(out)
    for name in _CAPABILITY_MODULES:
        assert name not in roster


# ---------------------------------------------------------------------------
# Complete mapping-group installation, and F-4 (build-time + runtime halves)
# ---------------------------------------------------------------------------

def test_api_access_security_alone_installs_a_complete_group(
    tmp_path: Path,
) -> None:
    rc, target = _install(tmp_path, "modules:\n  - api-access-security\n")
    assert rc == 0
    for dst in _group_destinations("api-access-security"):
        assert (target / dst).is_file(), f"missing {dst}"
    for dst in _group_destinations("web-hosting-security"):
        assert not (target / dst).exists()


def test_web_hosting_security_alone_installs_a_complete_group(
    tmp_path: Path,
) -> None:
    rc, target = _install(tmp_path, "modules:\n  - web-hosting-security\n")
    assert rc == 0
    for dst in _group_destinations("web-hosting-security"):
        assert (target / dst).is_file(), f"missing {dst}"
    for dst in _group_destinations("api-access-security"):
        assert not (target / dst).exists()


def test_every_mapping_source_exists_under_templates_modules() -> None:
    """F-4, build-time half: every `InstallSpec.src` in both new groups
    exists under `templates/modules/` -- a missing source would otherwise
    install an incomplete group SILENTLY (`install_modules` warns and
    continues; see the runtime half below, which is the second, independent
    catch for the same hazard)."""
    missing = []
    for name in _CAPABILITY_MODULES:
        for spec in s._MODULE_MAPPINGS[name]:
            src = CAIRN_ROOT / "templates" / "modules" / spec.src
            if not src.is_file():
                missing.append(f"{name}: {spec.src}")
    assert not missing, "missing InstallSpec source(s):\n" + "\n".join(missing)


def test_hazard_a_renamed_engine_source_degrades_the_facade_at_runtime(
    tmp_path: Path,
) -> None:
    """F-4, runtime half: rename one source in a `tmp_path` COPY of the
    templates tree and confirm the install is caught -- not by a fail-closed
    refusal (`install_modules` fails OPEN: it warns and continues, per the
    module comment in `config.py`), but by the installed facade's own A-10
    import self-check, which must degrade (exit 20) rather than traceback."""
    templates_root = tmp_path / "templates"
    shutil.copytree(CAIRN_ROOT / "templates", templates_root)
    victim = (
        templates_root / "modules" / "team-gated" / "_security_net" / "net.py"
    )
    victim.unlink()

    target = tmp_path / "target"
    target.mkdir()
    s.install_modules(
        templates_root, target, {}, ["api-access-security"], force=True,
    )
    assert not (
        target / "scripts" / "_api_access_security" / "net.py"
    ).exists()
    facade = target / "scripts" / "api_access_security.py"
    assert facade.is_file()

    result = subprocess.run(
        [sys.executable, str(facade), "local"],
        cwd=target, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 20, (
        f"expected DEGRADED (20) on an incomplete engine, got "
        f"{result.returncode}\nstdout={result.stdout}\nstderr={result.stderr}"
    )
    assert "engine_incomplete" in result.stdout


# ---------------------------------------------------------------------------
# F-1: the manifest moves by exactly the declared rows, and the collision
# hazard
# ---------------------------------------------------------------------------

def test_manifest_carries_exactly_the_fourteen_destinations() -> None:
    """F-1, re-measured rather than quoted: the plan's '14' was a
    d73d436 prediction against a manifest total that keeps moving as
    sibling scopes land; the durable invariant is that the manifest
    contains exactly one row per `_MODULE_MAPPINGS` destination for each
    capability group. Re-measured here at 7 destinations per group x 2
    groups = 14, matching the already-landed F1 verification record's own
    re-measurement (`python bootstrap/scaffold.py --manifest`: 114 rows,
    +14 over the pre-scope 100)."""
    rows = s.install_manifest(modules=None)
    by_dst = {dst for _src, dst, _verbatim in rows}
    expected = set(_ALL_CAPABILITY_DESTINATIONS)
    assert expected <= by_dst, f"missing from manifest: {expected - by_dst}"
    assert len(expected) == 14, (
        f"re-measured: expected 14 destinations (7 per capability group), "
        f"found {len(expected)} -- if a group's shape changed, update this "
        f"comment, not the number"
    )


def test_hazard_a_colliding_destination_is_refused_by_install_manifest(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """F-1 hazard perturbation: a destination collision with a sibling
    scope's new module must still raise `ValueError` -- proving the two new
    groups sit inside the EXISTING duplicate-destination refusal
    (`duplicate_destinations`, called from `install_manifest`), not a
    special case that only happens to hold today. Patches
    `bootstrap._scaffold.install._MODULE_MAPPINGS` specifically: `install.py`
    holds its own `from .config import _MODULE_MAPPINGS` binding, distinct
    from the facade's re-export, so a patch there is where
    `install_manifest` actually reads it."""
    stolen_dst = s._MODULE_MAPPINGS["web-hosting-security"][0].dst
    colliding = s.InstallSpec(
        "team-gated/api_access_security.py", stolen_dst,
    )
    patched = dict(_install_mod._MODULE_MAPPINGS)
    patched["api-access-security"] = list(
        _install_mod._MODULE_MAPPINGS["api-access-security"]
    ) + [colliding]
    monkeypatch.setattr(_install_mod, "_MODULE_MAPPINGS", patched)
    with pytest.raises(ValueError, match="destination-ownership conflict"):
        s.install_manifest(modules=None)


# ---------------------------------------------------------------------------
# F-2: every new row round-trips through the lockfile (empty-registry form),
# and the engine-tamper hazard
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "modules_body",
    [
        "modules:\n  - api-access-security\n",
        "modules:\n  - web-hosting-security\n",
        "modules:\n  - api-access-security\n  - web-hosting-security\n",
    ],
    ids=("api-only", "hosting-only", "both"),
)
def test_every_installed_destination_round_trips_and_verifies_ok(
    modules_body: str, tmp_path: Path,
) -> None:
    rc, target = _install(tmp_path, modules_body)
    assert rc == 0
    lock = s.read_lockfile(target)
    lock_dsts = {rec["dst"] for rec in lock["files"]}
    expected: list[str] = []
    if "api-access-security" in modules_body:
        expected += _group_destinations("api-access-security")
    if "web-hosting-security" in modules_body:
        expected += _group_destinations("web-hosting-security")
    for dst in expected:
        assert dst in lock_dsts, f"{dst} not recorded in the lockfile"
    assert verify(target) == 0


def test_hazard_a_tampered_engine_member_fails_the_fresh_install(
    tmp_path: Path,
) -> None:
    """F-2 hazard perturbation: modify an installed engine member by one
    byte and confirm `verify_integrity` reports `modified (hash mismatch)`
    -- the runner must NOT be living-state (F2 has not landed, and even
    once it lands, `_LIVING_STATE_DSTS` only ever covers the two policy
    destinations, never an engine member -- see F2-1's own hazard)."""
    rc, target = _install(
        tmp_path, "modules:\n  - api-access-security\n",
    )
    assert rc == 0
    assert verify(target) == 0
    member = target / "scripts" / "_api_access_security" / "net.py"
    member.write_bytes(member.read_bytes() + b"\n# tampered\n")
    assert verify(target) == 1


# ---------------------------------------------------------------------------
# F-3: the illegal living-state opt-out still refuses
# ---------------------------------------------------------------------------

def test_hazard_an_illegal_living_state_opt_out_still_refuses(
    tmp_path: Path,
) -> None:
    """F-3: hand-edit an installed lockfile to set `living_state: true` on
    a runner record; `verify_integrity` must report the illegal opt-out and
    fail closed. This is existing engine behaviour
    (`bootstrap/verify_integrity.py`'s `_LIVING_STATE_DSTS` membership
    check) exercised against the two new capability groups' records; the
    record is planted by this test, not produced by any code this row
    lands."""
    rc, target = _install(
        tmp_path, "modules:\n  - api-access-security\n",
    )
    assert rc == 0
    lock = s.read_lockfile(target)
    for rec in lock["files"]:
        if rec["dst"] == "scripts/api_access_security.py":
            rec["living_state"] = True
    (target / s._LOCKFILE_REL).write_text(
        s._emit_lock_yaml(lock), encoding="utf-8",
    )
    assert verify(target) == 1


# ---------------------------------------------------------------------------
# B2's installer-record field vocabulary, in three parts (F5's own framing)
# ---------------------------------------------------------------------------

def _expected_lockfile_keys() -> dict[str, frozenset[str]]:
    """Per-destination expected key set (F5(a)) -- NOT one global set.

    Measured against the current tree (`write_install_lockfile`,
    `bootstrap/_scaffold/install.py`, the per-record dict-literal block just
    before `file_records.append(rec)`): every record carries `{src, dst,
    verbatim, hash}`; a VERBATIM destination (the facade + the four engine
    members, ten of the fourteen) additionally carries `base_hash` alone
    (the `else` arm of the `if not verbatim` branch); a SUBSTITUTED
    destination (the two doctrine `.md` files + the two policy stubs, four
    of the fourteen) additionally carries BOTH `base_cache` and `base_hash`.

    **Coupling to Chunk F row F2 (not landed by this file).** F2 adds the
    two `dev/.cairn/*-policy.json` destinations
    (`dev/.cairn/api-access-policy.json`,
    `dev/.cairn/web-hosting-policy.json`) to `_LIVING_STATE_DSTS`; once it
    lands, `write_install_lockfile`'s `if dst_rel in _LIVING_STATE_DSTS`
    branch (`bootstrap/_scaffold/install.py`) will add a `living_state:
    true` key to EXACTLY those two records and no others. This map is
    per-destination for exactly that reason: F2 extends those two entries
    in place; the other twelve are untouched by F2.
    """
    expected: dict[str, frozenset[str]] = {}
    for name in _CAPABILITY_MODULES:
        for spec in s._MODULE_MAPPINGS[name]:
            keys = {"src", "dst", "verbatim", "hash", "base_hash"}
            if not spec.verbatim:
                keys.add("base_cache")
            expected[spec.dst] = frozenset(keys)
    return expected


def test_f5a_the_lockfile_record_key_set_is_exact_per_destination(
    tmp_path: Path,
) -> None:
    """F5(a), exact writer vocabulary. `write_install_lockfile`'s
    per-record dict is a source-owned exact dict literal, so an extra key
    is structurally unreachable at write time; this asserts the key set
    rather than inferring that impossibility."""
    rc, target = _install(
        tmp_path,
        "modules:\n  - api-access-security\n  - web-hosting-security\n",
    )
    assert rc == 0
    lock = s.read_lockfile(target)
    by_dst = {rec["dst"]: rec for rec in lock["files"]}
    expected = _expected_lockfile_keys()
    for dst, expected_keys in expected.items():
        rec = by_dst[dst]
        # F2 COUPLING (see _expected_lockfile_keys docstring): F2, once
        # landed, adds `living_state` to exactly these two destinations.
        # Measured here at F2's pre-landing state -- neither carries it.
        if dst in (
            "dev/.cairn/api-access-policy.json",
            "dev/.cairn/web-hosting-policy.json",
        ):
            assert "living_state" not in rec, (
                f"{dst} unexpectedly carries living_state before F2 lands"
            )
        assert set(rec) == expected_keys, (
            f"{dst}: expected key set {sorted(expected_keys)}, got "
            f"{sorted(rec)}"
        )


def test_f5b_an_unrecognized_lockfile_key_is_silently_ignored_by_verify(
    tmp_path: Path,
) -> None:
    """F5(b), the tried impossibility -- a CHARACTERIZATION test.

    A green result here is a recorded GAP, not B2 satisfied:
    `bootstrap/verify_integrity.py` reads each record with `rec.get(...)`
    and never enumerates the permitted keys, so hand-adding an unrecognized
    key to an installed record is silently ignored, not refused. B2's
    closed-vocabulary refusal is NOT implemented by this file -- see F5(c)
    below.
    """
    rc, target = _install(
        tmp_path, "modules:\n  - api-access-security\n",
    )
    assert rc == 0
    lock = s.read_lockfile(target)
    for rec in lock["files"]:
        if rec["dst"] == "scripts/api_access_security.py":
            rec["an_unrecognized_extra_field"] = "tamper-carrying-payload"
    (target / s._LOCKFILE_REL).write_text(
        s._emit_lock_yaml(lock), encoding="utf-8",
    )
    assert verify(target) == 0, (
        "characterization failed: verify_integrity now refuses an "
        "unrecognized lockfile key -- if this is now true, B2's closing "
        "half has moved into verify_integrity.py and F5(c)'s note below "
        "is stale"
    )


# F5(c), where B2 is actually satisfied: the closed-vocabulary refusal that
# NAMES the unrecognized key lives in the DISPATCHER's lockfile-record
# reader (owned and tested by `security-verification-activation`, its T44),
# not in `bootstrap/verify_integrity.py`. Closing the `verify_integrity`
# half is a change to that file, which is outside this plan's declared
# symbol delta and outside its Proposed paths -- it does not land here or
# in this test file; it is routed as a lasting truth at archive. No test
# is added for it in this file, deliberately.


# ---------------------------------------------------------------------------
# The summary and post-install notice text (F-6)
# ---------------------------------------------------------------------------

def test_capability_install_notice_lines_is_empty_when_neither_selected() -> None:
    assert capability_install_notice_lines([]) == []
    assert capability_install_notice_lines(["claim-check"]) == []


@pytest.mark.parametrize("name", _CAPABILITY_MODULES)
def test_capability_install_notice_lines_states_the_four_things(
    name: str,
) -> None:
    rendered = "\n".join(capability_install_notice_lines([name]))
    facade = _CAPABILITY_NOTICE_MODULES[name]["facade"]
    assert f"python {facade} local" in rendered
    assert f"python {facade} deployed-passive --authorize-base-url" in rendered
    assert "byte-for-byte" in rendered
    assert (
        "No deployed credential is read during install or during local "
        "evidence." in rendered
    )
    assert "Maintainer-invoked" in rendered


def test_summary_and_post_install_notice_appear_when_selected(
    tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    body = (
        "preset: solo-greenfield\nmodules_add:\n  - api-access-security\n"
        "  - web-hosting-security\n"
    )
    cfg = _write_profile(tmp_path / "profile.yml", body)
    assert s.main(["--summary", "--config", str(cfg)]) == 0
    summary_out = capsys.readouterr().out
    for fragment in _NOTICE_FRAGMENTS:
        assert fragment in summary_out, f"missing from --summary: {fragment!r}"

    rc, _target = _install(tmp_path, body)
    assert rc == 0
    install_out = capsys.readouterr().out
    for fragment in _NOTICE_FRAGMENTS:
        assert fragment in install_out, (
            f"missing from post-install output: {fragment!r}"
        )


def test_summary_and_post_install_notice_absent_when_neither_selected(
    tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    body = "preset: solo-greenfield\n"
    cfg = _write_profile(tmp_path / "profile.yml", body)
    assert s.main(["--summary", "--config", str(cfg)]) == 0
    summary_out = capsys.readouterr().out
    for fragment in _NOTICE_FRAGMENTS:
        assert fragment not in summary_out

    rc, _target = _install(tmp_path, body)
    assert rc == 0
    install_out = capsys.readouterr().out
    for fragment in _NOTICE_FRAGMENTS:
        assert fragment not in install_out


# ---------------------------------------------------------------------------
# upgrade / --adopt-module behaviour
# ---------------------------------------------------------------------------

def test_upgrade_plan_lists_both_capabilities_as_new_modules_available(
    tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    rc, target = _install(tmp_path, "modules:\n  - claim-check\n")
    assert rc == 0
    capsys.readouterr()
    rc = s.main([
        "upgrade", "--plan", "--target", str(target),
        "--cairn-root", str(CAIRN_ROOT),
    ])
    out = capsys.readouterr().out
    assert rc == 0
    assert "new modules available (opt-in)" in out
    for name in _CAPABILITY_MODULES:
        assert name in out
    for dst in _ALL_CAPABILITY_DESTINATIONS:
        assert not (target / dst).exists()


def test_adopt_module_records_api_access_security_into_an_existing_lockfile(
    tmp_path: Path,
) -> None:
    rc, target = _install(tmp_path, "modules:\n  - claim-check\n")
    assert rc == 0
    rc = s.main([
        "upgrade", "--adopt-module", "api-access-security",
        "--target", str(target), "--cairn-root", str(CAIRN_ROOT),
    ])
    assert rc == 0
    lock = s.read_lockfile(target)
    assert "api-access-security" in lock.get("modules", [])
    lock_dsts = {rec["dst"] for rec in lock["files"]}
    for dst in _group_destinations("api-access-security"):
        assert dst in lock_dsts, f"{dst} not recorded after --adopt-module"
        assert (target / dst).is_file(), f"{dst} not written after --adopt-module"
    assert verify(target) == 0
