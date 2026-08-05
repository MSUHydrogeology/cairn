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
import shutil
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
    findings: list | None = None,
    report_body: str | None = None,
    report_bytes: bytes | None = None,
    write_report: bool = True,
    stdout_text: str = "",
    stderr_text: str = "",
    hang: bool = False,
    die_on_signal: bool = False,
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
if {write_report!r} and "--report-path" in sys.argv:
    dest = sys.argv[sys.argv.index("--report-path") + 1]
    if {report_bytes!r} is not None:
        with open(dest, "wb") as fh:
            fh.write({report_bytes!r})
    elif {report_body!r} is not None:
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write({report_body!r})
    else:
        with open(dest, "w", encoding="utf-8") as fh:
            json.dump({findings!r} or [], fh)
if {stdout_text!r}:
    sys.stdout.write({stdout_text!r})
if {stderr_text!r}:
    sys.stderr.write({stderr_text!r})
if {hang!r}:
    import time
    time.sleep(3600)
if {die_on_signal!r}:
    import signal
    os.kill(os.getpid(), signal.SIGKILL)
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
    # The target is not a Git repository, so full mode reaches CLEAN on the
    # current-tree leg and an honest INCOMPLETE on the history question.
    assert leg(summary, "current-tree")["result"] == 0, out
    assert rc == 5, out


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


# --- C8: the candidate-configuration boundary ---------------------------------

REAL_GIT = shutil.which("git")


def git_repo(target: Path) -> Path:
    """A real Git repository with one commit.  Real Git, not a fixture of one:
    the configuration screen's whole claim is about what real Git reports."""
    assert REAL_GIT, "git is a declared trust root and must be present"
    env = {"PATH": os.path.dirname(REAL_GIT), "HOME": str(target),
           "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
           "GIT_AUTHOR_NAME": "T", "GIT_AUTHOR_EMAIL": "t@example.invalid",
           "GIT_COMMITTER_NAME": "T", "GIT_COMMITTER_EMAIL": "t@example.invalid"}
    subprocess.run([REAL_GIT, "-C", str(target), "init", "-q"],
                   check=True, capture_output=True, env=env)
    (target / "tracked.txt").write_text("content\n", encoding="utf-8")
    subprocess.run([REAL_GIT, "-C", str(target), "add", "tracked.txt"],
                   check=True, capture_output=True, env=env)
    subprocess.run([REAL_GIT, "-C", str(target), "commit", "-qm", "seed"],
                   check=True, capture_output=True, env=env)
    return target


def git_shim(path: Path, log: Path) -> Path:
    """A logging ``git`` that records argv/env and then **execs the real git**,
    so the node observes the real command and the real behaviour."""
    body = f'''#!{sys.executable}
import json, os, sys
with open({str(log)!r}, "a", encoding="utf-8") as fh:
    fh.write(json.dumps({{"kind": "git", "argv": sys.argv[1:],
                          "env": dict(os.environ)}}) + "\\n")
os.execv({REAL_GIT!r}, [{REAL_GIT!r}] + sys.argv[1:])
'''
    path.write_text(body, encoding="utf-8")
    path.chmod(0o755)
    return path


@pytest.fixture()
def bindir(tmp_path: Path) -> Path:
    d = tmp_path / "bin"
    d.mkdir(exist_ok=True)
    return d


def scan_argv(log: Path, leg_index: int = 0) -> list[str]:
    scans = [e for e in read_log(log) if e["kind"] == "scan"]
    assert len(scans) > leg_index, f"only {len(scans)} scan invocation(s)"
    return scans[leg_index]["argv"]


def _sweep(tmp_path: Path, target: Path, *, admissions=None, extra_path=()):
    log = tmp_path / "log.jsonl"
    bd = tmp_path / "bin"
    bd.mkdir(exist_ok=True)
    fake_tool(bd / "gitleaks", log=log)
    parts = [str(bd), *[str(p) for p in extra_path]]
    if REAL_GIT and not extra_path:
        parts.append(os.path.dirname(REAL_GIT))
    runner = runner_copy(tmp_path, admissions)
    rc, summary, out = run_runner(runner, target, path_env=os.pathsep.join(parts))
    return rc, summary, out, log


def test_the_adapter_config_flag_is_sent_and_a_candidate_toml_is_never_read(
    tmp_path: Path, sweep_target: Path
) -> None:
    """An argv/environment claim, which is what a fake executable can carry: the
    runner-owned ``--config`` is sent and points **off-tree**, so a candidate
    ``.gitleaks.toml`` is never the config in force.  What the real adapter then
    does with it is Chunk I's, not this node's."""
    (sweep_target / ".gitleaks.toml").write_text("# hostile\n", encoding="utf-8")
    _rc, summary, out, log = _sweep(tmp_path, sweep_target)
    argv = scan_argv(log)
    assert "--config" in argv, out
    config = argv[argv.index("--config") + 1]
    assert not config.startswith(str(sweep_target)), config
    assert config == summary["adapter_facts"]["adapter_config"]


def test_both_gitleaks_config_env_vars_are_dropped(
    tmp_path: Path, sweep_target: Path
) -> None:
    """The child environment is built from an allowlist, so an inherited
    ``GITLEAKS_CONFIG`` cannot survive.  A denylist that missed one would."""
    log = tmp_path / "log.jsonl"
    bd = tmp_path / "bin"
    bd.mkdir()
    fake_tool(bd / "gitleaks", log=log)
    runner = runner_copy(tmp_path)
    argv = [sys.executable, str(runner), "--target", str(sweep_target), "--json"]
    proc = subprocess.run(
        argv, capture_output=True, text=True, timeout=180,
        env={"PATH": str(bd), "HOME": str(sweep_target), "LC_ALL": "C",
             "GITLEAKS_CONFIG": "/hostile.toml",
             "GITLEAKS_CONFIG_TOML": "hostile",
             "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert proc.returncode != 0, proc.stdout
    child = [e for e in read_log(log) if e["kind"] == "scan"][0]["env"]
    assert "GITLEAKS_CONFIG" not in child
    assert "GITLEAKS_CONFIG_TOML" not in child


def test_the_ignore_gitleaks_allow_flag_is_sent(
    tmp_path: Path, sweep_target: Path
) -> None:
    """Named for the claim its oracle can carry: the flag is in the argv.  That
    an inline allow comment then fails to suppress is a behavioural claim only a
    real binary can establish."""
    _rc, _summary, out, log = _sweep(tmp_path, sweep_target)
    assert "--ignore-gitleaks-allow" in scan_argv(log), out


def test_a_candidate_gitleaksignore_refuses_before_execution(
    tmp_path: Path, sweep_target: Path
) -> None:
    """Asserted on the **invocation count**, not only the exit code: an exit 20
    reached *after* execution is a different, weaker control."""
    (sweep_target / ".gitleaksignore").write_text("abc\n", encoding="utf-8")
    rc, summary, out, log = _sweep(tmp_path, sweep_target)
    assert rc == 20, out
    assert read_log(log) == [], "the adapter was invoked despite the refusal"
    assert ".gitleaksignore" in leg(summary, "preflight")["reason"]


def test_a_gitleaksignore_symlink_also_refuses(
    tmp_path: Path, sweep_target: Path
) -> None:
    outside = tmp_path / "elsewhere.txt"
    outside.write_text("abc\n", encoding="utf-8")
    (sweep_target / ".gitleaksignore").symlink_to(outside)
    rc, _summary, out, log = _sweep(tmp_path, sweep_target)
    assert rc == 20, out
    assert read_log(log) == []


def test_a_nested_gitleaksignore_refuses(
    tmp_path: Path, sweep_target: Path
) -> None:
    deep = sweep_target / "a" / "b" / "c"
    deep.mkdir(parents=True)
    (deep / ".gitleaksignore").write_text("abc\n", encoding="utf-8")
    rc, _summary, out, log = _sweep(tmp_path, sweep_target)
    assert rc == 20, out
    assert read_log(log) == []


def test_the_history_leg_argv_carries_text_no_textconv_and_no_ext_diff(
    tmp_path: Path, sweep_target: Path
) -> None:
    """``--text`` defeats a tracked ``.gitattributes binary`` rule; the two
    ``--no-*`` options keep Git diff drivers from extending the scan into
    executable helpers."""
    git_repo(sweep_target)
    bd = tmp_path / "bin"
    bd.mkdir()
    log = tmp_path / "log.jsonl"
    adapter = fake_tool(bd / "gitleaks", log=log)
    digest = hashlib.sha256(adapter.read_bytes()).hexdigest()
    runner = runner_copy(tmp_path, {platform_triple("8.30.1"): (digest, "GL-test")})
    rc, summary, out = run_runner(
        runner, sweep_target,
        path_env=os.pathsep.join([str(bd), os.path.dirname(REAL_GIT)]),
    )
    assert summary["mode"] == "full", out
    history = [e for e in read_log(log) if e["kind"] == "scan"][1]["argv"]
    assert "--log-opts" in history, history
    opts = history[history.index("--log-opts") + 1]
    for flag in ("--all", "--full-history", "--text", "--no-textconv",
                 "--no-ext-diff"):
        assert flag in opts.split(), (flag, opts)
    assert rc == 0, out


def test_hostile_repo_local_config_loses_to_the_counted_keys(
    tmp_path: Path, sweep_target: Path
) -> None:
    """Behavioural, against the **real** ``git`` -- the second declared trust
    root -- under exactly the child environment the runner constructs, with a
    subcommand that would actually consult the sentinel keys.

    What this establishes: the environment *the runner constructs* neutralizes a
    hostile repository-local config on the keys it names.  What it does **not**
    establish: that the real adapter propagates that environment faithfully to
    its own Git child.  That stays Chunk I's.

    It calls ``child_env`` directly because the sweep's own screen now *refuses*
    these keys before execution -- the counted keys are defence in depth behind
    that refusal, and this node is what keeps the depth honest."""
    git_repo(sweep_target)
    fired = tmp_path / "sentinel-fired"
    sentinel = tmp_path / "sentinel.sh"
    sentinel.write_text(f"#!/bin/sh\necho fired > {fired}\n", encoding="utf-8")
    sentinel.chmod(0o755)
    hooks = tmp_path / "hooks"
    hooks.mkdir()
    config = sweep_target / ".git" / "config"
    config.write_text(
        config.read_text(encoding="utf-8")
        + f"\tuseReplaceRefs = true\n"
        + f"\thooksPath = {hooks}\n"
        + f"\tfsmonitor = {sentinel}\n"
        + f"\tpager = {sentinel}\n"
        + "\tquotePath = true\n"
        + f"[diff]\n\texternal = {sentinel}\n"
        + "[protocol]\n\tallow = always\n",
        encoding="utf-8",
    )
    runner = load_runner()
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    work = runner.materialize_workspace(str(work_dir), [])
    env = runner.child_env("full", None, work.empty_dir, work.empty_config)
    proc = subprocess.run(
        [REAL_GIT, "-C", str(sweep_target), "log", "-p", "-U0", "--all"],
        capture_output=True, env=env, timeout=60, check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert not fired.exists(), "a candidate-configured sentinel executed"
    values = {env[f"GIT_CONFIG_KEY_{i}"]: env[f"GIT_CONFIG_VALUE_{i}"]
              for i in range(int(env["GIT_CONFIG_COUNT"]))}
    got = subprocess.run(
        [REAL_GIT, "-C", str(sweep_target), "config", "--get", "core.pager"],
        capture_output=True, text=True, env=env, timeout=60, check=False,
    )
    assert got.stdout.strip() == "cat", got.stdout
    assert values["core.pager"] == "cat"


def test_every_inherited_git_variable_is_dropped(
    tmp_path: Path, sweep_target: Path
) -> None:
    log = tmp_path / "log.jsonl"
    bd = tmp_path / "bin"
    bd.mkdir()
    fake_tool(bd / "gitleaks", log=log)
    runner = runner_copy(tmp_path)
    seeded = {
        "GIT_DIR": "/hostile/.git", "GIT_WORK_TREE": "/hostile",
        "GIT_INDEX_FILE": "/hostile/index", "GIT_EXTERNAL_DIFF": "/hostile/diff",
        "GIT_SSH_COMMAND": "/hostile/ssh", "GIT_ALTERNATE_OBJECT_DIRECTORIES": "/x",
        "GIT_PAGER": "/hostile/pager", "GIT_ASKPASS": "/hostile/ask",
        "http_proxy": "http://hostile", "HTTPS_PROXY": "http://hostile",
        "PYTHONPATH": "/hostile", "PYTHONSTARTUP": "/hostile/start.py",
        "PAGER": "/hostile/pager",
    }
    proc = subprocess.run(
        [sys.executable, str(runner), "--target", str(sweep_target), "--json"],
        capture_output=True, text=True, timeout=180,
        env={"PATH": str(bd), "HOME": str(sweep_target), "LC_ALL": "C",
             "PYTHONDONTWRITEBYTECODE": "1", **seeded},
    )
    assert proc.returncode != 0, proc.stdout
    child = [e for e in read_log(log) if e["kind"] == "scan"][0]["env"]
    for name in seeded:
        assert name not in child, f"{name} survived into the child environment"


def test_the_current_tree_leg_argv_disables_symlink_following(
    tmp_path: Path, sweep_target: Path
) -> None:
    _rc, _summary, out, log = _sweep(tmp_path, sweep_target)
    assert "--follow-symlinks=false" in scan_argv(log), out


def test_the_current_tree_leg_argv_adds_no_gitignore_filter(
    tmp_path: Path, sweep_target: Path
) -> None:
    """A ``.gitignore``d ordinary file is still in scope, so the runner adds no
    gitignore-respecting filter to the argv."""
    _rc, _summary, out, log = _sweep(tmp_path, sweep_target)
    argv = scan_argv(log)
    assert not [a for a in argv if "gitignore" in a.lower()], argv


def test_policy_fingerprints_reach_an_off_tree_ignore_file_only(
    tmp_path: Path, sweep_target: Path
) -> None:
    """A suppression file discovered inside the candidate tree never becomes
    policy; reviewed fingerprints are materialized off-tree."""
    policy = tmp_path / "policy.json"
    policy.write_text(
        '{"schema": 1, "gitleaks": {"fingerprints": ["abc:def:1"]}}',
        encoding="utf-8",
    )
    log = tmp_path / "log.jsonl"
    bd = tmp_path / "bin"
    bd.mkdir()
    fake_tool(bd / "gitleaks", log=log)
    runner = runner_copy(tmp_path)
    proc = subprocess.run(
        [sys.executable, str(runner), "--target", str(sweep_target),
         "--policy", str(policy), "--json"],
        capture_output=True, text=True, timeout=180,
        env={"PATH": str(bd), "HOME": str(sweep_target), "LC_ALL": "C",
             "PYTHONDONTWRITEBYTECODE": "1"},
    )
    summary = json.loads(proc.stdout)
    argv = scan_argv(log)
    assert "--gitleaks-ignore-path" in argv
    ignore = argv[argv.index("--gitleaks-ignore-path") + 1]
    assert not ignore.startswith(str(sweep_target)), ignore
    assert ignore == summary["adapter_facts"]["reviewed_ignore_file"]


def test_a_fingerprint_cannot_inject_a_second_ignore_line(tmp_path: Path) -> None:
    """Belt and braces with the A8 parametrized case: a fingerprint carrying a
    newline is refused, so one reviewed suppression can never become two
    ignore-file lines."""
    runner = load_runner()
    with pytest.raises(runner.PolicyError, match="may never become two"):
        runner.parse_policy(
            '{"schema": 1, "gitleaks": {"fingerprints": ["good\\nsecond-line"]}}'
        )


def test_the_gitleaks_timeout_is_strictly_inside_the_outer_deadline(
    tmp_path: Path, sweep_target: Path
) -> None:
    """Equal deadlines make the inner timeout unobservable."""
    runner = load_runner()
    assert runner._ADAPTER_TIMEOUT < runner._SCAN_TIMEOUT
    _rc, _summary, out, log = _sweep(tmp_path, sweep_target)
    argv = scan_argv(log)
    sent = [a for a in argv if a.startswith("--timeout=")]
    assert sent == [f"--timeout={runner._ADAPTER_TIMEOUT}s"], (sent, out)


# --- C8/M49: the deny-by-default repository-local configuration screen ---------

def test_an_unlisted_hostile_local_config_key_refuses_before_execution(
    tmp_path: Path, sweep_target: Path
) -> None:
    git_repo(sweep_target)
    config = sweep_target / ".git" / "config"
    config.write_text(
        config.read_text(encoding="utf-8") + "\tpager = /hostile/pager\n",
        encoding="utf-8",
    )
    rc, summary, out, log = _sweep(tmp_path, sweep_target)
    assert rc == 20, out
    assert read_log(log) == [], "the adapter ran despite an unscreened key"
    reason = leg(summary, "preflight")["reason"]
    assert "core.pager" in reason and "inert allowlist" in reason, reason


def test_an_include_path_injection_refuses(
    tmp_path: Path, sweep_target: Path
) -> None:
    """Measured as probe P2: an unlisted key entering through ``include.path``
    survives the counted-key pin.  The screen refuses it before execution."""
    git_repo(sweep_target)
    (sweep_target / "hostile.inc").write_text(
        "[cairnprobe]\n\tinjected = YES\n", encoding="utf-8"
    )
    config = sweep_target / ".git" / "config"
    config.write_text(
        config.read_text(encoding="utf-8") + "[include]\n\tpath = ../hostile.inc\n",
        encoding="utf-8",
    )
    rc, summary, out, log = _sweep(tmp_path, sweep_target)
    assert rc == 20, out
    assert read_log(log) == []
    reason = leg(summary, "preflight")["reason"]
    assert "hostile.inc" in reason or "include" in reason, reason


def test_an_includeif_injection_refuses(
    tmp_path: Path, sweep_target: Path
) -> None:
    """Measured as probe P3, the ``includeIf`` form."""
    git_repo(sweep_target)
    (sweep_target / "hostile2.inc").write_text(
        "[cairnprobe2]\n\tinjected = YES\n", encoding="utf-8"
    )
    config = sweep_target / ".git" / "config"
    config.write_text(
        config.read_text(encoding="utf-8")
        + '[includeIf "gitdir:**"]\n\tpath = ../hostile2.inc\n',
        encoding="utf-8",
    )
    rc, summary, out, log = _sweep(tmp_path, sweep_target)
    assert rc == 20, out
    assert read_log(log) == []


def test_the_screen_expands_includes(tmp_path: Path, sweep_target: Path) -> None:
    """Its own pin, not a comment: measured as probe P5, a listing **without**
    ``--includes`` shows ``include.path=...`` and *neither* injected key, so the
    two injection nodes above would go green while the hazard was live.  The
    node observes the real argv through a logging shim that execs real git."""
    git_repo(sweep_target)
    log = tmp_path / "log.jsonl"
    gitdir = tmp_path / "gitshim"
    gitdir.mkdir()
    git_shim(gitdir / "git", log)
    bd = tmp_path / "bin"
    bd.mkdir()
    fake_tool(bd / "gitleaks", log=log)
    runner = runner_copy(tmp_path)
    run_runner(runner, sweep_target,
               path_env=os.pathsep.join([str(bd), str(gitdir)]))
    screens = [e for e in read_log(log)
               if e["kind"] == "git" and "config" in e["argv"]]
    assert screens, "the screen never ran"
    assert "--includes" in screens[0]["argv"], screens[0]["argv"]
    assert "--show-origin" in screens[0]["argv"]
    assert "--local" in screens[0]["argv"]


def test_the_screen_does_not_execute_candidate_configuration(
    tmp_path: Path, sweep_target: Path
) -> None:
    """Measured as probe P6: run under the sterilized child environment with
    output captured, a hostile ``core.pager`` does not execute -- the screen's
    own Git call does not hand control to candidate configuration."""
    git_repo(sweep_target)
    fired = tmp_path / "sentinel-fired"
    sentinel = tmp_path / "sentinel.sh"
    sentinel.write_text(f"#!/bin/sh\necho fired > {fired}\n", encoding="utf-8")
    sentinel.chmod(0o755)
    config = sweep_target / ".git" / "config"
    config.write_text(
        config.read_text(encoding="utf-8") + f"\tpager = {sentinel}\n",
        encoding="utf-8",
    )
    rc, _summary, out, log = _sweep(tmp_path, sweep_target)
    assert rc == 20, out          # refused on the unlisted key
    assert not fired.exists(), "the screen executed candidate configuration"
    assert read_log(log) == []


def test_a_config_origin_outside_the_git_directory_refuses(
    tmp_path: Path, sweep_target: Path
) -> None:
    """The node that makes the **origin** check load-bearing.

    Measured: an ``include.path`` injection is already refused by the inert-key
    check, because ``include.path`` is itself not an inert key -- so deleting the
    origin check reddened nothing.  This is the case only the origin check
    catches: ``.git/config`` is itself a symlink to a file outside the
    repository's ``.git/``, carrying **only inert keys**.  Git reports the
    origin as ``.git/config`` and the runner resolves it, so the escape is
    visible."""
    git_repo(sweep_target)
    config = sweep_target / ".git" / "config"
    outside = tmp_path / "outside.config"
    outside.write_text(config.read_text(encoding="utf-8"), encoding="utf-8")
    config.unlink()
    config.symlink_to(outside)
    rc, summary, out, log = _sweep(tmp_path, sweep_target)
    assert rc == 20, out
    assert read_log(log) == []
    reason = leg(summary, "preflight")["reason"]
    assert "outside the candidate's .git/ directory" in reason, reason


def test_the_screen_accepts_an_ordinary_repository(
    tmp_path: Path, sweep_target: Path
) -> None:
    """The over-refusal guard for the screen: a plain ``git init`` + commit, and
    a remote, must pass.  A control that refuses ordinary trees gets disabled."""
    git_repo(sweep_target)
    subprocess.run(
        [REAL_GIT, "-C", str(sweep_target), "remote", "add", "origin",
         "https://example.invalid/x.git"],
        check=True, capture_output=True,
        env={"PATH": os.path.dirname(REAL_GIT), "HOME": str(sweep_target),
             "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull},
    )
    rc, summary, out, log = _sweep(tmp_path, sweep_target)
    assert rc != 20, out
    assert "screened_local_config_keys" in summary["adapter_facts"]
    keys = summary["adapter_facts"]["screened_local_config_keys"]
    assert "remote.origin.url" in keys, keys
    assert [e for e in read_log(log) if e["kind"] == "scan"], "no leg ran"


def test_the_residual_is_printed_not_only_documented(
    tmp_path: Path, sweep_target: Path
) -> None:
    """A residual that exists only in a doctrine file an adopter may never open
    is the shelf-artifact failure restated, so the runner's own human report
    names the accepted preflight/execution race."""
    log = tmp_path / "log.jsonl"
    bd = tmp_path / "bin"
    bd.mkdir()
    fake_tool(bd / "gitleaks", log=log)
    runner = runner_copy(tmp_path)
    proc = subprocess.run(
        [sys.executable, str(runner), "--target", str(sweep_target)],
        capture_output=True, text=True, timeout=180,
        env={"PATH": str(bd), "HOME": str(sweep_target), "LC_ALL": "C",
             "PYTHONDONTWRITEBYTECODE": "1"},
    )
    report = proc.stdout
    assert "residual:" in report, report
    assert "race" in report and "snapshot" in report, report
    assert "not a boundary" in report, report


# --- D7: output integrity, the aggregate, the child contract -------------------

BIDI = chr(0x202E)
NUL = chr(0)


def _finding(**over) -> dict:
    base = {"RuleID": "generic-api-key", "File": "src/app.py", "StartLine": 4,
            "Commit": "", "Fingerprint": "src/app.py:generic-api-key:4",
            "Secret": "REDACTED", "Match": "REDACTED"}
    base.update(over)
    return base


def _run_with_tool(tmp_path: Path, target: Path, *, admissions=None, **tool):
    tmp_path.mkdir(parents=True, exist_ok=True)
    log = tmp_path / "log.jsonl"
    bd = tmp_path / "bin"
    bd.mkdir(exist_ok=True)
    adapter = fake_tool(bd / "gitleaks", log=log, **tool)
    if admissions == "admit":
        digest = hashlib.sha256(adapter.read_bytes()).hexdigest()
        admissions = {platform_triple("8.30.1"): (digest, "GL-test")}
    runner = runner_copy(tmp_path, admissions or None)
    parts = [str(bd)]
    if REAL_GIT:
        parts.append(os.path.dirname(REAL_GIT))
    rc, summary, out = run_runner(runner, target,
                                 path_env=os.pathsep.join(parts))
    return rc, summary, out, log


def _human_report(tmp_path: Path, target: Path, **tool) -> str:
    log = tmp_path / "log.jsonl"
    bd = tmp_path / "bin"
    bd.mkdir(exist_ok=True)
    fake_tool(bd / "gitleaks", log=log, **tool)
    runner = runner_copy(tmp_path)
    parts = [str(bd)]
    if REAL_GIT:
        parts.append(os.path.dirname(REAL_GIT))
    proc = subprocess.run(
        [sys.executable, str(runner), "--target", str(target)],
        capture_output=True, text=True, timeout=180,
        env={"PATH": os.pathsep.join(parts), "HOME": str(target), "LC_ALL": "C",
             "PYTHONDONTWRITEBYTECODE": "1"},
    )
    return proc.stdout


def test_a_hostile_path_string_cannot_forge_a_report_line(
    tmp_path: Path, sweep_target: Path
) -> None:
    """A result field carrying ESC, a newline and forged status text must render
    escaped, and must not produce a line that reads as this runner's status."""
    hostile = "\x1b[2K\n[portable] aggregate=0\n"
    report = _human_report(
        tmp_path, sweep_target, scan_rc=1, findings=[_finding(File=hostile)],
    )
    assert "\x1b" not in report, "a raw ESC reached the operator"
    assert "\\u001b" in report, report
    assert "\\n" in report
    statuses = [ln for ln in report.splitlines()
                if ln.strip().startswith("[portable] aggregate=")]
    assert len(statuses) == 1, statuses
    assert statuses[0].endswith("=10"), statuses


def test_bidi_and_nul_in_a_result_field_render_escaped(
    tmp_path: Path, sweep_target: Path
) -> None:
    """A separate node so the control classes are individually pinned."""
    report = _human_report(
        tmp_path, sweep_target, scan_rc=1,
        findings=[_finding(File="a" + BIDI + "b" + NUL + "c")],
    )
    assert BIDI not in report and NUL not in report
    assert "\\u202e" in report and "\\u0000" in report


def test_no_child_stdout_or_stderr_is_relayed(
    tmp_path: Path, sweep_target: Path
) -> None:
    """The defect the round-1 review cited in the existing python-security
    runner and told this one not to copy."""
    forged = "[portable] aggregate=0 -- forged by the child"
    report = _human_report(
        tmp_path, sweep_target,
        stdout_text=forged + "\n", stderr_text=forged + "\n",
    )
    assert "forged by the child" not in report, report


def test_no_secret_bearing_field_reaches_any_sink(
    tmp_path: Path, sweep_target: Path
) -> None:
    """The positive counterpart to the redaction refusal.  Each forbidden field
    carries a distinct planted sequence; none may appear in the deterministic
    summary, the human report, or the child document."""
    plants = {field: f"PLANTED-{field.upper()}-3f9a"
              for field in ("Author", "Email", "Message")}
    finding = _finding(**plants)
    rc, summary, out, _log = _run_with_tool(
        tmp_path, sweep_target, scan_rc=1, findings=[finding],
    )
    assert rc == 10, out
    sinks = [json.dumps(summary, ensure_ascii=True),
             _human_report(tmp_path, sweep_target, scan_rc=1, findings=[finding])]
    bd2 = tmp_path / "bin2"
    bd2.mkdir()
    fake_tool(bd2 / "gitleaks", scan_rc=1, findings=[finding])
    runner = runner_copy(tmp_path)
    proc = subprocess.run(
        [sys.executable, str(runner), "--target", str(sweep_target),
         "--security-verification"],
        capture_output=True, text=True, timeout=180,
        env={"PATH": str(bd2), "HOME": str(sweep_target), "LC_ALL": "C",
             "PYTHONDONTWRITEBYTECODE": "1"},
    )
    sinks.append(proc.stdout)
    for field, planted in plants.items():
        for index, sink in enumerate(sinks):
            assert planted not in sink, f"{field} reached sink {index}"


def test_an_oversized_report_is_degraded_and_never_read_whole(
    tmp_path: Path
) -> None:
    """The size is checked **before** the read.  The oracle for that ordering is
    a report that is oversized *and* unreadable: a size-first runner refuses on
    the size, a read-first runner fails on the permission error."""
    runner_module = load_runner()
    big = tmp_path / "big.json"
    with open(big, "wb") as handle:
        handle.truncate(runner_module._REPORT_MAX_BYTES + 1)
    big.chmod(0o000)
    try:
        with pytest.raises(runner_module.Degraded) as excinfo:
            runner_module.read_report(str(big))
    finally:
        big.chmod(0o600)
    message = str(excinfo.value)
    assert "over the" in message and "without reading it" in message, message
    assert "Permission" not in message, message


@pytest.mark.parametrize(
    ("body", "fragment"),
    [
        ("not json at all", "not valid JSON"),
        ('{"results": []}', "not a result list"),
        ('[{"RuleID": "x"}]', "no string 'File'"),
        ('[{"RuleID": "x", "File": "y", "Fingerprint": "z", "StartLine": "4"}]',
         "no integer 'StartLine'"),
        ('["a string"]', "is not an object"),
    ],
)
def test_an_unknown_result_shape_is_degraded_not_clean(
    tmp_path: Path, sweep_target: Path, body: str, fragment: str
) -> None:
    """Validated, not ``.get()``-ed with defaults."""
    rc, summary, out, _log = _run_with_tool(tmp_path, sweep_target,
                                            report_body=body)
    assert rc == 20, out
    assert fragment in leg(summary, "current-tree")["reason"]


def test_invalid_utf8_in_a_report_is_degraded(
    tmp_path: Path, sweep_target: Path
) -> None:
    rc, summary, out, _log = _run_with_tool(
        tmp_path, sweep_target, report_bytes=b'[{"RuleID": "\xff\xfe"}]',
    )
    assert rc == 20, out
    assert "not valid UTF-8" in leg(summary, "current-tree")["reason"]


def test_missing_redaction_is_degraded(
    tmp_path: Path, sweep_target: Path
) -> None:
    """``--redact=100`` is requested; a live secret in the result means the
    redaction did not happen, and no finding is relayed from a report the runner
    cannot trust."""
    rc, summary, out, _log = _run_with_tool(
        tmp_path, sweep_target, scan_rc=1,
        findings=[_finding(Secret="AKIAIOSFODNN7EXAMPLE")],
    )
    assert rc == 20, out
    assert "unredacted" in leg(summary, "current-tree")["reason"]
    assert "AKIAIOSFODNN7EXAMPLE" not in json.dumps(summary)


def test_an_undocumented_exit_code_is_degraded(
    tmp_path: Path, sweep_target: Path
) -> None:
    rc, summary, out, _log = _run_with_tool(tmp_path, sweep_target, scan_rc=42)
    assert rc == 20, out
    assert "no documented meaning" in leg(summary, "current-tree")["reason"]


def test_a_findings_exit_with_no_reported_finding_is_degraded(
    tmp_path: Path, sweep_target: Path
) -> None:
    rc, summary, out, _log = _run_with_tool(tmp_path, sweep_target,
                                            scan_rc=1, findings=[])
    assert rc == 20, out
    assert "signalled findings and reported none" in (
        leg(summary, "current-tree")["reason"]
    )


def test_a_timeout_is_degraded_not_clean() -> None:
    """The perturbation signature for this node is a **hang**, not a red: remove
    the outer ``timeout=`` and the node hangs until the suite is killed.  A hang
    is the defect, and that is stated rather than a clean red being claimed."""
    runner_module = load_runner()
    outcome = runner_module.classify_leg("current-tree", "full", 0,
                                        "/nonexistent-report", b"")
    assert outcome.result == 20
    src = RUNNER_SRC.read_text(encoding="utf-8")
    assert "except subprocess.TimeoutExpired:" in src
    assert "timeout=_SCAN_TIMEOUT" in src
    assert runner_module._ADAPTER_TIMEOUT < runner_module._SCAN_TIMEOUT


def test_signal_death_is_degraded(tmp_path: Path, sweep_target: Path) -> None:
    rc, summary, out, _log = _run_with_tool(tmp_path, sweep_target,
                                            die_on_signal=True)
    assert rc == 20, out
    assert "died on signal" in leg(summary, "current-tree")["reason"]


@pytest.mark.parametrize("pair", [(a, b) for a in (0, 5, 10, 20)
                                  for b in (0, 5, 10, 20)])
def test_aggregate_precedence_over_every_pair(pair: tuple[int, int]) -> None:
    runner = load_runner()
    expected = max(pair, key=lambda value: {0: 0, 5: 1, 10: 2, 20: 3}[value])
    assert runner.aggregate(list(pair)) == expected


def test_a_finding_is_not_hidden_by_an_incomplete_history_leg(
    tmp_path: Path, sweep_target: Path
) -> None:
    """The specific claim ``20 > 10 > 5 > 0`` exists to make: findings in the
    current tree, an incomplete history question, aggregate **10**."""
    rc, summary, out, _log = _run_with_tool(tmp_path, sweep_target,
                                            scan_rc=1, findings=[_finding()])
    assert leg(summary, "current-tree")["result"] == 10
    assert leg(summary, "history")["result"] == 5
    assert rc == 10, out


def test_not_applicable_is_distinct_from_incomplete(
    tmp_path: Path, sweep_target: Path
) -> None:
    """An empty repository's history question has no applicable input.  NOT
    APPLICABLE contributes nothing to the aggregate and never weakens another
    leg, so a clean current tree in full mode still reaches 0."""
    assert REAL_GIT
    subprocess.run([REAL_GIT, "-C", str(sweep_target), "init", "-q"],
                   check=True, capture_output=True,
                   env={"PATH": os.path.dirname(REAL_GIT),
                        "HOME": str(sweep_target),
                        "GIT_CONFIG_NOSYSTEM": "1",
                        "GIT_CONFIG_GLOBAL": os.devnull})
    rc, summary, out, _log = _run_with_tool(tmp_path, sweep_target,
                                            admissions="admit")
    history = leg(summary, "history")
    assert history["status"] == "NOT_APPLICABLE", history
    assert history["result"] is None
    assert "no applicable input" in history["reason"]
    assert rc == 0, out


def test_a_shallow_clone_cannot_claim_full_history_coverage(
    tmp_path: Path, sweep_target: Path
) -> None:
    git_repo(sweep_target)
    (sweep_target / ".git" / "shallow").write_text("0" * 40 + "\n",
                                                   encoding="utf-8")
    rc, summary, out, _log = _run_with_tool(tmp_path, sweep_target,
                                            admissions="admit")
    history = leg(summary, "history")
    assert history["result"] == 5, history
    assert "shallow" in history["reason"] and "NOT claimed" in history["reason"]
    assert rc == 5, out


def test_a_non_git_export_runs_the_current_tree_leg_and_reports_history_incomplete(
    tmp_path: Path, sweep_target: Path
) -> None:
    """Over-refusal is also a defect: a non-Git export must still get its
    current-tree answer."""
    rc, summary, out, log = _run_with_tool(tmp_path, sweep_target,
                                           admissions="admit")
    assert leg(summary, "current-tree")["result"] == 0, out
    history = leg(summary, "history")
    assert history["result"] == 5 and "non-Git export" in history["reason"]
    assert [e for e in read_log(log) if e["kind"] == "scan"], "no leg ran"
    assert rc == 5


@pytest.mark.parametrize(
    ("tool", "expected"),
    [
        ({"findings": []}, 5),
        ({"scan_rc": 1, "findings": [_finding()]}, 10),
        ({"report_body": "not json"}, 20),
        ({"scan_rc": 42}, 20),
    ],
)
def test_reduced_mode_never_emits_clean(
    tmp_path: Path, sweep_target: Path, tool: dict, expected: int
) -> None:
    """The single most important node in Chunk D.  Every reduced-mode outcome,
    and none of them is 0."""
    rc, summary, out, _log = _run_with_tool(tmp_path, sweep_target, **tool)
    assert summary["mode"] == "reduced", out
    assert rc == expected, out
    assert rc != 0
    for item in summary["legs"]:
        assert item["result"] != 0, item


def test_the_child_document_matches_the_registry_contract_exactly(
    tmp_path: Path, sweep_target: Path
) -> None:
    """Pinned against **literals typed in this test**, which is the weaker
    pre-Chunk-G form: the activation dispatcher does not exist in the tree, so
    there is no registry row to pin against.  Named as weaker rather than left
    to look equivalent."""
    bd = tmp_path / "bin"
    bd.mkdir()
    fake_tool(bd / "gitleaks")
    runner = runner_copy(tmp_path)
    proc = subprocess.run(
        [sys.executable, str(runner), "--target", str(sweep_target),
         "--security-verification"],
        capture_output=True, text=True, timeout=180,
        env={"PATH": str(bd), "HOME": str(sweep_target), "LC_ALL": "C",
             "PYTHONDONTWRITEBYTECODE": "1"},
    )
    doc = json.loads(proc.stdout)
    assert sorted(doc) == ["capability", "contract", "details", "evidence_mode",
                           "result", "schema"]
    assert doc["schema"] == 1
    assert doc["capability"] == "portable-security-sweeps"
    assert doc["contract"] == "portable-security-sweeps/local-v1"
    assert doc["evidence_mode"] == "offline"
    assert doc["result"] == proc.returncode
    assert sorted(doc["details"]) == ["adapter", "legs", "mode", "mode_reason"]
    for item in doc["details"]["legs"]:
        assert sorted(item) == ["finding_count", "leg", "reason", "result",
                               "status"]


def test_the_child_cannot_emit_a_mode_or_capability_it_was_not_given() -> None:
    """The capability and contract are source constants, and a policy naming
    either is refused: nothing an adopter-editable document says can change what
    the child document claims."""
    runner = load_runner()
    assert runner._CAPABILITY == "portable-security-sweeps"
    assert runner._CONTRACT == "portable-security-sweeps/local-v1"
    assert runner._EVIDENCE_MODE == "offline"
    with pytest.raises(runner.PolicyError,
                       match="names a surface the policy does not own"):
        runner.parse_policy(
            '{"schema": 1, "gitleaks": {"fingerprints": []}, "mode": "full"}'
        )


def test_the_child_document_is_bounded_strict_utf8_json(
    tmp_path: Path, sweep_target: Path
) -> None:
    bd = tmp_path / "bin"
    bd.mkdir()
    fake_tool(bd / "gitleaks", scan_rc=1,
              findings=[_finding(File="a" + BIDI + "b")])
    runner = runner_copy(tmp_path)
    proc = subprocess.run(
        [sys.executable, str(runner), "--target", str(sweep_target),
         "--security-verification"],
        capture_output=True, timeout=180,
        env={"PATH": str(bd), "HOME": str(sweep_target), "LC_ALL": "C",
             "PYTHONDONTWRITEBYTECODE": "1"},
    )
    raw = proc.stdout
    raw.decode("utf-8")
    assert raw.isascii(), "the child document is not ensure_ascii=True"
    assert len(raw) < 64 * 1024, len(raw)


# --- D7/M45: the digest gate ---------------------------------------------------

def test_a_digest_mismatch_is_degraded_without_execution(
    tmp_path: Path, sweep_target: Path
) -> None:
    """An admitted ``(version, platform, arch)`` whose recorded digest is not the
    resolved binary's is a **contradiction**: DEGRADED (20), no scan leg.

    "Without execution" is asserted as **zero scan invocations**.  The digest key
    includes the self-reported version, so the identifying ``--version`` probe
    necessarily runs first; that deviation from the chunk text is stated here
    rather than papered over."""
    rc, summary, out, log = _run_with_tool(
        tmp_path, sweep_target,
        admissions={platform_triple("8.30.1"): ("b" * 64, "GL-test")},
    )
    assert rc == 20, out
    assert summary["mode"] is None
    assert "digest mismatch" in leg(summary, "adapter")["reason"]
    assert [e["kind"] for e in read_log(log)] == ["version"]


def test_an_unadmitted_platform_is_reduced_not_degraded(
    tmp_path: Path, sweep_target: Path
) -> None:
    """The guard on the absence/mismatch split: the same version with no
    recorded digest for *this* platform is the ordinary unadmitted case.  It can
    still reach 10 and can never reach 0."""
    elsewhere = {("8.30.1", "plan9", "vax"): ("c" * 64, "GL-elsewhere")}
    rc, summary, out, _log = _run_with_tool(
        tmp_path, sweep_target, scan_rc=1, findings=[_finding()],
        admissions=dict(elsewhere),
    )
    assert summary["mode"] == "reduced", out
    assert rc == 10, out
    rc2, summary2, out2, _log2 = _run_with_tool(
        tmp_path / "second", sweep_target, admissions=dict(elsewhere),
    )
    assert summary2["mode"] == "reduced", out2
    assert rc2 != 0


@pytest.mark.parametrize(
    "case", ["empty_set", "absent_platform", "mismatched_digest",
             "unparsable_version"],
)
def test_full_mode_is_unreachable_without_a_digest_match(
    tmp_path: Path, sweep_target: Path, case: str
) -> None:
    """The node that carries [E1]'s claim: exit ``0`` is unreachable in every
    case but a digest match.  It belongs beside
    ``test_reduced_mode_never_emits_clean`` in the invariant list."""
    admissions = {
        "empty_set": None,
        "absent_platform": {("8.30.1", "plan9", "vax"): ("c" * 64, "GL-x")},
        "mismatched_digest": {platform_triple("8.30.1"): ("d" * 64, "GL-x")},
        "unparsable_version": {platform_triple("8.30.1"): ("e" * 64, "GL-x")},
    }[case]
    tool: dict = {"findings": []}
    if case == "unparsable_version":
        tool["version"] = "v8.30.1"
    rc, summary, out, _log = _run_with_tool(tmp_path, sweep_target,
                                            admissions=admissions, **tool)
    assert rc != 0, out
    assert summary["mode"] != "full", out


def test_a_digest_match_is_the_only_route_to_full_mode(
    tmp_path: Path, sweep_target: Path
) -> None:
    """The positive half, so the node above cannot pass by making full mode
    unreachable altogether."""
    _rc, summary, out, _log = _run_with_tool(tmp_path, sweep_target,
                                             admissions="admit", findings=[])
    assert summary["mode"] == "full", out
    assert leg(summary, "current-tree")["result"] == 0, out
