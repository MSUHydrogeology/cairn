"""Behavioural tests for the ``portable-security-sweeps`` module.

Deliberately a **new** file with **no module-level ``pytestmark``**: a
module-level skip marker would register every node here as skipped-by-default,
which is the defect ``profile-parse-fail-open`` measured elsewhere in this
suite.  Every node below runs unconditionally.

Chunk A's matrices: the install / manifest / group / collision matrix, the
strict-policy matrix, and the version-mode classification matrix.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_portable_security_sweeps.py
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import bootstrap.scaffold as s  # noqa: E402
from bootstrap._scaffold.config import (  # noqa: E402
    _MODULE_MAPPINGS,
    _MODULE_REQUIRED_TOKENS,
)
from bootstrap._scaffold.lockfile import read_lockfile  # noqa: E402

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
MODULE = "portable-security-sweeps"

RUNNER_SRC = CAIRN_ROOT / "templates/modules/team-gated/run_portable_security_sweeps.py"
POLICY_SRC = CAIRN_ROOT / "templates/modules/team-gated/portable_security_policy.json"
DOCTRINE_SRC = CAIRN_ROOT / "templates/modules/team-gated/portable-security-sweeps.md"

#: The three ``(src, dst, verbatim)`` triples the registration must carry --
#: typed here, in the test, so the pin has an oracle the registry does not
#: supply.
EXPECTED_GROUP = (
    ("team-gated/portable-security-sweeps.md",
     "dev/modules/portable-security-sweeps.md", False),
    ("team-gated/run_portable_security_sweeps.py",
     "scripts/run_portable_security_sweeps.py", True),
    ("team-gated/portable_security_policy.json",
     "scripts/portable_security_policy.json", True),
)


# --- helpers -----------------------------------------------------------------

def load_runner(path: Path | None = None):
    """Import the runner from its file path.  Used only for the pure functions
    (policy validation, version parsing, mode selection) whose public CLI path
    does not exist until the adapter boundary lands."""
    src = path or RUNNER_SRC
    spec = importlib.util.spec_from_file_location(
        f"_portable_runner_{abs(hash(str(src)))}", src
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_ADMISSIONS_LINE = (
    "_ADMITTED_ARTIFACTS: dict[tuple[str, str, str], Admission] = {}"
)


def platform_triple(version: str) -> tuple[str, str, str]:
    import platform  # noqa: PLC0415
    return (version, platform.system().lower(), platform.machine().lower())


def runner_copy(tmp_path: Path, admissions: dict | None = None) -> Path:
    """A copy of the shipped runner in *tmp_path*, optionally with the
    admitted-artifact block replaced.

    Editing that block **is** the admission path -- it is a reviewed source
    change by construction, which is why a test that needs an admitted version
    edits a copy of the source rather than reaching a policy, an environment
    variable or a flag.  The shipped file is never touched; a node below
    asserts that."""
    text = RUNNER_SRC.read_text(encoding="utf-8")
    assert text.count(_ADMISSIONS_LINE) == 1
    if admissions:
        entries = ", ".join(
            f'({k[0]!r}, {k[1]!r}, {k[2]!r}): Admission({v[0]!r}, {v[1]!r})'
            for k, v in admissions.items()
        )
        text = text.replace(
            _ADMISSIONS_LINE,
            "_ADMITTED_ARTIFACTS: dict[tuple[str, str, str], Admission] = "
            "{%s}" % entries,
        )
    dest_dir = tmp_path / "runner"
    dest_dir.mkdir(exist_ok=True)
    dest = dest_dir / RUNNER_SRC.name
    dest.write_text(text, encoding="utf-8")
    (dest_dir / POLICY_SRC.name).write_text(
        POLICY_SRC.read_text(encoding="utf-8"), encoding="utf-8"
    )
    return dest


def fake_tool(
    path: Path,
    *,
    version: str = "8.30.1",
    version_rc: int = 0,
    log: Path | None = None,
    scan_rc: int = 0,
    mutate_self_on_version: bool = False,
    extra: str = "",
) -> Path:
    """A fake adapter that records exactly what it received.

    The oracle is the *log this tool writes*, never anything the runner
    computes.  The shebang is an absolute interpreter path on purpose: the
    child ``PATH`` the runner builds contains no ``/usr/bin``, so a
    ``#!/usr/bin/env python3`` shebang would not resolve."""
    body = f'''#!{sys.executable}
import json, os, sys
LOG = {str(log) if log is None else repr(str(log))}
def record(kind):
    if LOG is None:
        return
    with open(LOG, "a", encoding="utf-8") as fh:
        probe = []
        for part in os.environ.get("PATH", "").split(os.pathsep):
            try:
                probe.append([part, sorted(os.listdir(part))])
            except OSError:
                probe.append([part, None])
        fh.write(json.dumps({{"kind": kind, "argv": sys.argv[1:],
                              "env": dict(os.environ),
                              "path_probe": probe,
                              "cwd": os.getcwd()}}) + "\\n")
if "--version" in sys.argv[1:]:
    record("version")
    if {mutate_self_on_version!r}:
        with open(__file__, "a", encoding="utf-8") as fh:
            fh.write("# swapped between validation and invocation\\n")
    sys.stdout.write({version!r} + "\\n")
    raise SystemExit({version_rc!r})
record("scan")
{extra}
raise SystemExit({scan_rc!r})
'''
    path.write_text(body, encoding="utf-8")
    path.chmod(0o755)
    return path


def read_log(log: Path) -> list[dict]:
    if not log.exists():
        return []
    return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def run_runner(
    runner: Path, target: Path, *, path_env: str, extra_argv: list[str] | None = None,
    expect_json: bool = True,
) -> tuple[int, dict, str]:
    argv = [sys.executable, str(runner), "--target", str(target)]
    argv += extra_argv if extra_argv is not None else ["--json"]
    proc = subprocess.run(
        argv, capture_output=True, text=True, timeout=180,
        env={"PATH": path_env, "HOME": str(target), "LC_ALL": "C",
             "PYTHONDONTWRITEBYTECODE": "1"},
    )
    payload: dict = {}
    if expect_json and proc.stdout.strip():
        payload = json.loads(proc.stdout)
    return proc.returncode, payload, proc.stdout + proc.stderr


def leg(summary: dict, name: str) -> dict:
    matches = [item for item in summary["legs"] if item["leg"] == name]
    assert matches, f"no {name!r} leg in {[i['leg'] for i in summary['legs']]}"
    return matches[0]


@pytest.fixture()
def sweep_target(tmp_path: Path) -> Path:
    target = tmp_path / "candidate"
    target.mkdir()
    (target / "README.md").write_text("hello\n", encoding="utf-8")
    return target


def _profile(tmp_path: Path, modules: list[str]) -> Path:
    cfg = tmp_path / "profile.yml"
    body = "project_name: PortableTest\ntest_command: pytest\nmodules:\n"
    if modules:
        body += "".join(f"  - {name}\n" for name in modules)
    else:
        body = "project_name: PortableTest\ntest_command: pytest\nmodules: []\n"
    cfg.write_text(body, encoding="utf-8")
    return cfg


def _install(tmp_path: Path, modules: list[str]) -> int:
    cfg = _profile(tmp_path, modules)
    return s.main([
        "--config", str(cfg), "--target", str(tmp_path),
        "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
    ])


@pytest.fixture()
def installed(tmp_path: Path) -> Path:
    assert _install(tmp_path, [MODULE]) == 0
    return tmp_path


# --- A8: install / manifest / group / collision -------------------------------

def test_the_module_installs_exactly_three_files(installed: Path) -> None:
    """The three declared destinations land, and the module contributes no
    fourth file to the target tree."""
    for _src, dst, _verbatim in EXPECTED_GROUP:
        assert (installed / dst).is_file(), f"missing installed destination: {dst}"
    # ``dev/.cairn/base/`` is the engine's base-template cache for every
    # substituted spec, not a module destination; excluded so the node judges
    # install destinations rather than upgrade bookkeeping.
    on_disk = sorted(
        str(p.relative_to(installed))
        for p in installed.rglob("*portable*")
        if p.is_file() and "dev/.cairn/base/" not in str(p.relative_to(installed))
    )
    expected = sorted(dst for _s, dst, _v in EXPECTED_GROUP)
    assert on_disk == expected, (
        f"the module contributed files beyond its declared group: {on_disk}"
    )


def test_the_registration_pins_all_three_specs_as_one_group() -> None:
    """A **test-side membership pin**, not an engine refusal: the engine
    performs no group-completeness check for ``_MODULE_MAPPINGS`` (its only
    such enforcement is scoped to the always-on onboarding group), so nothing
    but this node refuses a registration that drops a group member."""
    specs = _MODULE_MAPPINGS[MODULE]
    actual = tuple((spec.src, spec.dst, spec.verbatim) for spec in specs)
    assert actual == EXPECTED_GROUP, (
        "the registered group is not the three declared specs: "
        f"{actual!r} != {EXPECTED_GROUP!r}"
    )


def test_the_module_declares_no_required_token(tmp_path: Path) -> None:
    """A profile selecting only this module installs with no ``python_package``
    and exits 0 -- the module declares no required token."""
    assert MODULE not in _MODULE_REQUIRED_TOKENS
    assert _install(tmp_path, [MODULE]) == 0
    lock = read_lockfile(tmp_path)
    assert lock is not None
    assert "python_package" not in (lock.get("tokens") or {})
    assert MODULE in lock.get("modules", [])


def test_module_destinations_collide_with_nothing() -> None:
    """``install_manifest`` refuses a duplicate destination by raising; this
    node asserts the whole-catalog manifest builds and that the module's three
    destinations are unique within it."""
    rows = s.install_manifest(modules=None)
    dsts = [dst for _src, dst, _verbatim in rows]
    assert len(dsts) == len(set(dsts)), "duplicate destination in the manifest"
    for _src, dst, _v in EXPECTED_GROUP:
        assert dsts.count(dst) == 1, f"{dst} is not uniquely owned"


def test_adopt_module_and_upgrade_carry_the_whole_group(tmp_path: Path) -> None:
    """``--adopt-module`` on a tree installed before the module existed writes
    all three files and records all three in the lockfile.  The hazard is the
    registration / adopt write-set, not the lockfile reader."""
    assert _install(tmp_path, []) == 0
    lock = read_lockfile(tmp_path)
    assert lock is not None and MODULE not in lock.get("modules", [])

    rc = s.main([
        "upgrade", "--target", str(tmp_path), "--adopt-module", MODULE,
        "--cairn-root", str(CAIRN_ROOT),
    ])
    assert rc == 0, "adopt-module refused"

    lock = read_lockfile(tmp_path)
    assert lock is not None and MODULE in lock.get("modules", [])
    recorded = {rec["dst"] for rec in lock.get("files", [])}
    written = []
    for _src, dst, _v in EXPECTED_GROUP:
        assert dst in recorded, f"{dst} not recorded in the lockfile"
        assert (tmp_path / dst).is_file(), f"{dst} not written to disk"
        written.append(dst)
    assert len(written) == 3


# --- A8: the strict policy matrix --------------------------------------------

def test_policy_accepts_the_shipped_v1_document() -> None:
    """The byte content of the shipped policy validates."""
    runner = load_runner()
    accepted = runner.parse_policy(POLICY_SRC.read_text(encoding="utf-8"))
    assert accepted == {"schema": 1, "gitleaks": {"fingerprints": []}}


def _fp(*items: str) -> str:
    return '{"schema": 1, "gitleaks": {"fingerprints": [%s]}}' % ", ".join(items)


def _top(extra_key: str, value: str = '"x"') -> str:
    return ('{"schema": 1, "gitleaks": {"fingerprints": []}, "%s": %s}'
            % (extra_key, value))


#: ``case -> (document, the refusal reason fragment that names its branch)``.
#:
#: Each case pins **both** that the document is refused **and** which branch
#: refused it.  That is not belt-and-braces: the fingerprint charset check
#: alone would refuse an empty, control-charactered or newline-bearing
#: fingerprint, so a node asserting refusal only would stay green after its own
#: branch was deleted.  Pinning the reason is what makes deleting one branch
#: redden exactly the node that names it.
_MALFORMATIONS: dict[str, tuple[str, str]] = {
    "unknown_top_level_key": (_top("extra", "1"), "unknown top-level policy key"),
    "missing_top_level_key": ('{"schema": 1}', "missing top-level policy key"),
    "unknown_gitleaks_key": (
        '{"schema": 1, "gitleaks": {"fingerprints": [], "other": 1}}',
        "unknown key\\(s\\) under 'gitleaks'",
    ),
    "duplicate_json_key": (
        '{"schema": 1, "schema": 1, "gitleaks": {"fingerprints": []}}',
        "duplicate JSON key",
    ),
    "not_json": ("{not json", "not valid JSON"),
    "top_level_not_an_object": ("[]", "top level must be a JSON object"),
    "gitleaks_not_an_object": (
        '{"schema": 1, "gitleaks": []}', "'gitleaks' must be a JSON object",
    ),
    "fingerprints_not_a_list": (
        '{"schema": 1, "gitleaks": {"fingerprints": "aa"}}',
        "'gitleaks.fingerprints' must be a list",
    ),
    "non_string_fingerprint": (_fp("7"), "fingerprint is not a string"),
    "duplicate_fingerprint": (_fp('"aa"', '"aa"'), "duplicate fingerprint"),
    "empty_fingerprint": (_fp('""'), "fingerprint is empty"),
    "oversized_fingerprint": (_fp('"' + "a" * 400 + '"'), "exceeds 200 characters"),
    "control_char_fingerprint": (_fp('"a\\u0007b"'), "control character"),
    "newline_fingerprint": (_fp('"a\\nb"'), "may never become two"),
    "disallowed_char_fingerprint": (_fp('"a b"'), "disallowed character"),
    "unsupported_schema": (
        '{"schema": 2, "gitleaks": {"fingerprints": []}}',
        "unsupported policy schema",
    ),
}


@pytest.mark.parametrize("case", sorted(_MALFORMATIONS))
def test_policy_refuses_every_named_malformation(case: str) -> None:
    """One node per malformation, each pinned to the branch that owns it, so
    deleting one validator branch reddens exactly that node."""
    runner = load_runner()
    document, reason = _MALFORMATIONS[case]
    with pytest.raises(runner.PolicyError, match=reason):
        runner.parse_policy(document)


#: Every surface the policy may never name.  These are *also* caught by the
#: closed-key rule, so the node asserts the refusal **names the class** --
#: otherwise deleting the forbidden-name check would redden nothing.
_FORBIDDEN_NAMES = [
    "path", "argv", "env", "executable", "command", "config", "baseline",
    "digest", "hash", "checksum", "artifact", "admitted_binary", "url",
    "network",
]


@pytest.mark.parametrize("key", _FORBIDDEN_NAMES)
def test_policy_refuses_a_key_that_names_a_forbidden_surface(key: str) -> None:
    """The policy carries reviewed fingerprint suppressions and nothing else:
    no path, argv, environment variable, executable, config file, baseline, or
    -- per the digest design -- digest, hash, checksum or admitted artifact.

    A digest an adopter could edit would let a candidate *admit its own
    binary*, which is strictly weaker than the self-reported version string it
    was meant to replace.  That is why the digest lives in source."""
    runner = load_runner()
    with pytest.raises(runner.PolicyError,
                       match="names a surface the policy does not own"):
        runner.parse_policy(_top(key))


@pytest.mark.parametrize("key", ["version", "versions", "mode"])
def test_policy_cannot_select_a_version_or_mode(key: str) -> None:
    """A policy naming a version or a mode refuses, and the refusal says so.
    Admission is a reviewed source change; nothing an adopter-editable document
    says can reach it."""
    runner = load_runner()
    with pytest.raises(runner.PolicyError,
                       match="names a surface the policy does not own"):
        runner.parse_policy(_top(key, '"8.30.1"'))


def test_policy_refusal_precedes_every_side_effect(tmp_path: Path) -> None:
    """A malformed policy refuses **before** the adapter seam is reached: the
    emitted summary carries the policy leg and no adapter leg at all."""
    import subprocess  # noqa: PLC0415 -- test-only child invocation

    bad = tmp_path / "bad_policy.json"
    bad.write_text('{"schema": 99}', encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(RUNNER_SRC), "--target", str(tmp_path),
         "--policy", str(bad), "--json"],
        capture_output=True, text=True, timeout=60,
    )
    assert proc.returncode == 20, proc.stdout + proc.stderr
    summary = json.loads(proc.stdout)
    legs = [leg["leg"] for leg in summary["legs"]]
    assert legs == ["policy"], (
        f"a refused policy still reached a later stage: legs={legs}"
    )
    assert summary["mode"] is None


# --- A8: strict version parsing and mode classification -----------------------

@pytest.mark.parametrize(
    ("text", "accepted"),
    [
        ("8.30.1", True),
        ("v8.30.1", False),
        ("8.30", False),
        ("8.30.1-rc1", False),
        ("8.30.1\n", False),
        ("8.30.1 ", False),
        ("8.30.01x", False),
        ("8.30.\x001", False),
        ("٨.٣٠.١", False),
    ],
)
def test_version_string_parsing_is_strict(text: str, accepted: bool) -> None:
    """``[0-9]`` and not ``\\d``: a permissive parser accepts Unicode decimal
    digits, a ``v`` prefix, or a trailing newline, and every one of those is an
    unmeasured version being treated as a measured one."""
    runner = load_runner()
    got = runner.parse_version(text)
    if accepted:
        assert got == (8, 30, 1)
    else:
        assert got is None, f"{text!r} was accepted as {got!r}"


def test_mode_selection_maps_versions_to_modes() -> None:
    """The full classification table, driven with an injected admitted-artifact
    set so the node does not depend on what the shipped set happens to hold."""
    runner = load_runner()
    key = ("darwin", "arm64")
    digest = "a" * 64
    admissions = {
        ("8.30.1", "darwin", "arm64"): runner.Admission(digest, "GL-8.30.1-darwin-arm64"),
    }

    full = runner.select_mode("8.30.1", digest, key, admissions)
    assert full.mode == "full" and full.result is None

    reduced = runner.select_mode("8.29.0", digest, key, admissions)
    assert reduced.mode == "reduced" and reduced.result is None

    for unmeasured in ("9.0.0", "7.9.9", "8.30.1-rc1", "not-a-version"):
        choice = runner.select_mode(unmeasured, digest, key, admissions)
        assert choice.mode is None, f"{unmeasured!r} selected {choice.mode!r}"
        assert choice.result == runner._AGG_INCOMPLETE, (
            f"{unmeasured!r} did not classify as INCOMPLETE without execution"
        )


def test_the_shipped_admitted_artifact_set_is_empty_until_a_record_exists() -> None:
    """The shipped set starts empty: ``8.30.1`` enters only when the admission
    matrix emits a record against a checksum-verified binary.  An empty set
    means reduced-provenance-only -- honest INCOMPLETE, never CLEAN."""
    runner = load_runner()
    assert runner._ADMITTED_ARTIFACTS == {}


# --- B6: the executable trust boundary ---------------------------------------

def test_absent_gitleaks_is_incomplete_not_clean(
    tmp_path: Path, sweep_target: Path
) -> None:
    """The plan's canonical "did not run must not read as clean" node: with no
    adapter anywhere on the child path the aggregate is **5**, and the report
    names the absence."""
    runner = runner_copy(tmp_path)
    empty = tmp_path / "nobin"
    empty.mkdir()
    rc, summary, out = run_runner(runner, sweep_target, path_env=str(empty))
    assert rc == 5, out
    assert summary["result"] == 5
    assert summary["mode"] is None
    reason = leg(summary, "adapter")["reason"]
    assert "gitleaks" in reason and "not found" in reason, reason


def test_absent_git_is_incomplete_for_the_history_leg(
    tmp_path: Path, sweep_target: Path
) -> None:
    """The adapter is present and Git is not: the history question is
    INCOMPLETE, never optional-and-clean."""
    bindir = tmp_path / "bin"
    bindir.mkdir()
    log = tmp_path / "log.jsonl"
    fake_tool(bindir / "gitleaks", log=log)
    runner = runner_copy(tmp_path)
    rc, summary, out = run_runner(runner, sweep_target, path_env=str(bindir))
    assert rc == 5, out
    history = leg(summary, "history")
    assert history["result"] == 5 and history["status"] == "INCOMPLETE"
    assert "git" in history["reason"].lower()


def test_a_repo_local_executable_is_refused(
    tmp_path: Path, sweep_target: Path
) -> None:
    """An executable planted **inside** the tree under check, first on the
    child path, is refused: the candidate tree may not choose the executable."""
    fake_tool(sweep_target / "gitleaks", log=tmp_path / "log.jsonl")
    runner = runner_copy(tmp_path)
    rc, summary, out = run_runner(runner, sweep_target, path_env=str(sweep_target))
    assert rc == 20, out
    reason = leg(summary, "adapter")["reason"]
    assert "inside the tree under check" in reason, reason
    assert read_log(tmp_path / "log.jsonl") == [], "the planted binary was invoked"


def test_a_repo_local_symlink_to_an_outside_binary_is_refused(
    tmp_path: Path, sweep_target: Path
) -> None:
    """The mirror case, and the one that makes the LEXICAL check load-bearing:
    the name found on the child path lives **inside** the tree under check but
    resolves **outside** it.  The resolved-path check alone accepts this --
    measured: deleting the lexical check reddens this node and no other."""
    cellar = tmp_path / "cellar"
    cellar.mkdir()
    real = fake_tool(cellar / "gitleaks-real", log=tmp_path / "log.jsonl")
    (sweep_target / "gitleaks").symlink_to(real)
    runner = runner_copy(tmp_path)
    rc, summary, out = run_runner(runner, sweep_target, path_env=str(sweep_target))
    assert rc == 20, out
    reason = leg(summary, "adapter")["reason"]
    assert "lexical path" in reason and "inside the tree under check" in reason, reason
    assert read_log(tmp_path / "log.jsonl") == []


def test_a_symlink_resolving_into_the_repo_is_refused(
    tmp_path: Path, sweep_target: Path
) -> None:
    """The case the lexical check alone lets through: a symlink **outside** the
    tree whose target resolves **inside** it."""
    inner = sweep_target / "tools"
    inner.mkdir()
    fake_tool(inner / "gitleaks-real", log=tmp_path / "log.jsonl")
    bindir = tmp_path / "bin"
    bindir.mkdir()
    (bindir / "gitleaks").symlink_to(inner / "gitleaks-real")
    runner = runner_copy(tmp_path)
    rc, summary, out = run_runner(runner, sweep_target, path_env=str(bindir))
    assert rc == 20, out
    reason = leg(summary, "adapter")["reason"]
    assert "resolved path" in reason and "inside the tree under check" in reason
    assert read_log(tmp_path / "log.jsonl") == []


def test_a_package_manager_symlink_outside_the_repo_is_accepted_and_both_paths_recorded(
    tmp_path: Path, sweep_target: Path
) -> None:
    """The over-refusal guard.  A legitimate package-manager symlink -- both
    paths outside the tree -- is accepted, and both are recorded.  Over-refusal
    is the failure mode that gets a security control switched off."""
    cellar = tmp_path / "cellar"
    cellar.mkdir()
    real = fake_tool(cellar / "gitleaks-8.30.1", log=tmp_path / "log.jsonl")
    bindir = tmp_path / "bin"
    bindir.mkdir()
    (bindir / "gitleaks").symlink_to(real)
    runner = runner_copy(tmp_path)
    rc, summary, out = run_runner(runner, sweep_target, path_env=str(bindir))
    assert rc != 20, out
    facts = summary["adapter_facts"]
    assert facts["adapter_lexical"] == str(bindir / "gitleaks")
    assert facts["adapter_resolved"] == str(real)
    assert facts["adapter_lexical"] != facts["adapter_resolved"]


def test_a_non_executable_file_is_degraded(
    tmp_path: Path, sweep_target: Path
) -> None:
    bindir = tmp_path / "bin"
    bindir.mkdir()
    tool = fake_tool(bindir / "gitleaks")
    tool.chmod(0o644)
    runner = runner_copy(tmp_path)
    rc, summary, out = run_runner(runner, sweep_target, path_env=str(bindir))
    # shutil.which() itself screens on the executable bit, so the observable is
    # a refusal either way; what this node pins is that it is NOT clean and NOT
    # a silent skip.
    assert rc in (5, 20), out
    assert summary["result"] != 0
    assert summary["mode"] is None


def test_a_version_command_failure_is_degraded_not_incomplete(
    tmp_path: Path, sweep_target: Path
) -> None:
    """*Absent* is 5; *present but unsound* is 20.  The distinction is the
    contract, so a failing ``--version`` must not borrow the absence code."""
    bindir = tmp_path / "bin"
    bindir.mkdir()
    fake_tool(bindir / "gitleaks", version_rc=3, log=tmp_path / "log.jsonl")
    runner = runner_copy(tmp_path)
    rc, summary, out = run_runner(runner, sweep_target, path_env=str(bindir))
    assert rc == 20, out
    assert "present but unsound" in leg(summary, "adapter")["reason"]


def test_path_drift_between_validation_and_invocation_is_degraded(
    tmp_path: Path, sweep_target: Path
) -> None:
    """The fake adapter rewrites itself during the ``--version`` probe, so the
    binary validated is not the binary about to be invoked."""
    bindir = tmp_path / "bin"
    bindir.mkdir()
    log = tmp_path / "log.jsonl"
    fake_tool(bindir / "gitleaks", log=log, mutate_self_on_version=True)
    runner = runner_copy(tmp_path)
    rc, summary, out = run_runner(runner, sweep_target, path_env=str(bindir))
    assert rc == 20, out
    reasons = " ".join(item["reason"] for item in summary["legs"])
    assert "drifted between validation and invocation" in reasons, reasons
    assert [entry["kind"] for entry in read_log(log)] == ["version"], (
        "a scan leg ran against a binary that had drifted"
    )


def test_reduced_mode_child_path_is_an_empty_off_tree_directory(
    tmp_path: Path, sweep_target: Path
) -> None:
    """The node that proves reduced mode **cannot reach Git**: its child
    ``PATH`` is a single empty directory outside the tree under check."""
    bindir = tmp_path / "bin"
    bindir.mkdir()
    log = tmp_path / "log.jsonl"
    fake_tool(bindir / "gitleaks", log=log)
    # git IS resolvable here, so the empty PATH is a choice, not an accident.
    (bindir / "git").symlink_to(fake_tool(bindir / "git-real", log=log))
    runner = runner_copy(tmp_path)
    rc, summary, out = run_runner(runner, sweep_target, path_env=str(bindir))
    assert summary["mode"] == "reduced", out
    scans = [entry for entry in read_log(log) if entry["kind"] == "scan"]
    assert scans, "the current-tree leg did not run"
    child_path = scans[0]["env"]["PATH"]
    assert os.pathsep not in child_path, child_path
    # The oracle is what the child observed, recorded by the fake tool at
    # invocation time -- the directory is a per-run temporary and is gone by
    # the time this assertion runs.
    probe = scans[0]["path_probe"]
    assert probe == [[child_path, []]], probe
    assert not child_path.startswith(str(sweep_target.resolve())), (
        "the child PATH dir is inside the tree under check"
    )
    assert rc != 0


def test_full_mode_child_path_contains_only_the_verified_git_directory(
    tmp_path: Path, sweep_target: Path
) -> None:
    """Full mode gets the verified Git directory and nothing else -- never the
    inherited path."""
    bindir = tmp_path / "bin"
    bindir.mkdir()
    gitdir = tmp_path / "gitbin"
    gitdir.mkdir()
    log = tmp_path / "log.jsonl"
    adapter = fake_tool(bindir / "gitleaks", log=log)
    fake_tool(gitdir / "git", log=log)
    digest = hashlib.sha256(adapter.read_bytes()).hexdigest()
    runner = runner_copy(tmp_path, {
        platform_triple("8.30.1"): (digest, "GL-8.30.1-test"),
    })
    rc, summary, out = run_runner(
        runner, sweep_target,
        path_env=os.pathsep.join([str(bindir), str(gitdir)]),
    )
    assert summary["mode"] == "full", out
    scans = [entry for entry in read_log(log) if entry["kind"] == "scan"]
    assert scans, "no scan leg ran in full mode"
    assert scans[0]["env"]["PATH"] == str(gitdir), scans[0]["env"]["PATH"]
    assert str(bindir) not in scans[0]["env"]["PATH"]
    assert rc != 0  # the output contract is not validated until Chunk D


def test_the_shipped_runner_is_never_mutated_by_a_test(tmp_path: Path) -> None:
    """The admission path is a source edit, and the tests exercise it by
    editing a **copy**.  This node pins that the shipped file is byte-identical
    across a copy-with-admissions -- a content snapshot, not `git status`,
    because a legitimately-modified working tree is not the property at issue."""
    before = RUNNER_SRC.read_bytes()
    copied = runner_copy(tmp_path, {platform_triple("8.30.1"): ("a" * 64, "x")})
    assert RUNNER_SRC.read_bytes() == before, "the shipped runner was mutated"
    assert copied.read_bytes() != before, "the copy carries no admission"


def test_the_trust_roots_are_enumerated_not_generalized() -> None:
    """The doctrine must name the two host executables as a list a reader can
    audit, and must say plainly that this is shape and containment validation
    rather than provenance."""
    runner = load_runner()
    assert runner.TRUST_ROOTS == ("gitleaks", "git")
    doctrine = DOCTRINE_SRC.read_text(encoding="utf-8")
    assert "`gitleaks`" in doctrine and "`git`" in doctrine
    assert "shape and containment" in doctrine
    assert "not provenance" in doctrine or "never for provenance" in doctrine
