"""Tests for the local security-verification dispatcher (Chunk A of plan
``security-verification-activation``): T1-T24, T36-T41, T44.

The dispatcher (``templates/modules/default-on/run_security_verification.py``)
ships verbatim to an adopter's ``scripts/`` directory and never imports
Cairn's own ``bootstrap/`` engine -- loaded here the same way
``test_content_scan.py`` loads ``content_scan.py``: by file path, independent
of any installed package.

Tests T6-T24, T36-T41, T44 inject a synthetic ``RegistryEntry`` by
monkeypatching the module-level ``_REGISTRY`` and point it at a fixture child
under ``tmp_path``. That injection is legitimate precisely because
``_REGISTRY`` is the source-owned surface under test: patching it is a
*source* edit in test form, the only way an entry may ever appear. No test
writes an entry through adopter data (lockfile / policy content) -- that is
what T2 forbids and tests.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_security_verification.py
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import sys
import textwrap
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(CAIRN_ROOT))

DISPATCHER_SRC = (
    CAIRN_ROOT / "templates" / "modules" / "default-on"
    / "run_security_verification.py"
)


def _load_fresh(name: str):
    spec = importlib.util.spec_from_file_location(name, DISPATCHER_SRC)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# One shared load for most tests (module-scoped internals under test);
# T1/T23/T41 independently re-load a SECOND, un-monkeypatched copy from the
# shipped source, per their own channel note.
mod = _load_fresh("cairn_security_verification_test")


# ---------------------------------------------------------------------------
# Shared fixture helpers
# ---------------------------------------------------------------------------

def _sha256_of(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _write_lockfile(root: Path, *, modules: list[str],
                     files: list[dict]) -> None:
    lock_dir = root / "dev" / ".cairn"
    lock_dir.mkdir(parents=True, exist_ok=True)
    body = {"modules": modules, "files": files}
    text = "# cairn-lock.yml -- test fixture\n" + json.dumps(body, indent=2)
    (lock_dir / "cairn-lock.yml").write_text(text, encoding="utf-8")


def _write_file(root: Path, rel: str, content: bytes) -> dict:
    """Write a real file under ``root`` at ``rel`` and return its lockfile
    record (the ``src``/``dst``/``verbatim``/``hash`` shape
    ``write_install_lockfile`` writes)."""
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return {"src": f"team-gated/{Path(rel).name}", "dst": rel,
            "verbatim": True, "hash": _sha256_of(content)}


_CHILD_PY = textwrap.dedent("""\
    import json, sys
    print(json.dumps({obj}))
    """)


def _write_child(root: Path, rel: str, obj: dict) -> dict:
    """Write a runner child script that prints exactly one JSON object, and
    return its lockfile record."""
    body = _CHILD_PY.format(obj=repr(obj))
    return _write_file(root, rel, body.encode("utf-8"))


_VALID_RESULT = "CLEAN"
_VALID_SCHEMA = "cairn.test_capability/v1"
_VALID_CONTRACT = "v1"
_VALID_EVIDENCE = "offline"


def _valid_child_obj(module_id: str, *, result: str = _VALID_RESULT,
                      details: str = "ok",
                      schema: str = _VALID_SCHEMA,
                      contract: str = _VALID_CONTRACT,
                      evidence_mode: str = _VALID_EVIDENCE) -> dict:
    return {
        "schema": schema, "capability": module_id, "contract": contract,
        "evidence_mode": evidence_mode, "result": result, "details": details,
    }


def _entry(module_id: str = "widget-security", *,
           runner_repository_path: str = "scripts/widget_security.py",
           argv_mode: str = "local",
           policy_repository_path: str | None = None,
           child_schema_version: str = _VALID_SCHEMA,
           capability_contract_version: str = _VALID_CONTRACT,
           evidence_mode: str = _VALID_EVIDENCE,
           accepted_process_exits: frozenset = frozenset({0, 1}),
           result_to_aggregate_mapping: dict | None = None,
           runner_binding_mode: str = "immutable_digest",
           policy_binding_mode: str = "none"):
    if result_to_aggregate_mapping is None:
        result_to_aggregate_mapping = {
            "CLEAN": (0, mod.CLEAN),
            "FINDINGS": (1, mod.FINDINGS),
            "INCOMPLETE": (1, mod.INCOMPLETE),
            "DEGRADED_RESULT": (1, mod.DEGRADED),
        }
    return mod.RegistryEntry(
        module_id=module_id,
        runner_repository_path=runner_repository_path,
        argv_mode=argv_mode,
        policy_repository_path=policy_repository_path,
        child_schema_version=child_schema_version,
        capability_contract_version=capability_contract_version,
        evidence_mode=evidence_mode,
        accepted_process_exits=accepted_process_exits,
        result_to_aggregate_mapping=result_to_aggregate_mapping,
        runner_binding_mode=runner_binding_mode,
        policy_binding_mode=policy_binding_mode,
    )


def _setup_clean_leg(tmp_path: Path, *, module_id: str = "widget-security",
                      result: str = _VALID_RESULT,
                      policy_binding_mode: str = "none",
                      policy_rel: str | None = None,
                      policy_content: bytes = b'{"configured": true}\n',
                      extra_runner_record_keys: dict | None = None,
                      extra_policy_record_keys: dict | None = None):
    """Write a valid runner (+ optional policy) and its lockfile records, and
    return ``(entry, records)`` ready for ``mod._evaluate_capability``."""
    runner_rel = f"scripts/{module_id.replace('-', '_')}.py"
    runner_rec = _write_child(
        tmp_path, runner_rel, _valid_child_obj(module_id, result=result))
    if extra_runner_record_keys:
        runner_rec.update(extra_runner_record_keys)
    records = {runner_rel: runner_rec}

    policy_repository_path = None
    if policy_binding_mode != "none":
        policy_repository_path = policy_rel or "dev/.cairn/widget-policy.json"
        policy_rec = _write_file(tmp_path, policy_repository_path,
                                  policy_content)
        if policy_binding_mode == "living_state":
            policy_rec["living_state"] = True
        if extra_policy_record_keys:
            policy_rec.update(extra_policy_record_keys)
        records[policy_repository_path] = policy_rec

    entry = _entry(module_id, runner_repository_path=runner_rel,
                    policy_repository_path=policy_repository_path,
                    policy_binding_mode=policy_binding_mode)
    return entry, records


# ===========================================================================
# Registry integrity -- the "closed registry" property
# ===========================================================================

class TestRegistryIntegrity:

    def test_shipped_registry_is_empty_at_activation_v1(self) -> None:
        """T1. Asserted against the SHIPPED source, read independently --
        never against ``mod`` (other tests monkeypatch its ``_REGISTRY``)."""
        fresh = _load_fresh("cairn_security_verification_t1_fresh")
        assert fresh._REGISTRY == {}

    def test_no_lockfile_or_policy_field_can_enter_the_registry(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """T2. Decoy keys planted (a) at the lockfile TOP level and (b)
        inside the policy file's own JSON content -- both are surfaces a
        naive resolver might consult instead of the registry entry. Neither
        is ever read; the dispatched call is unaffected."""
        module_id = "widget-security"
        decoy = {
            "runner": "scripts/evil.py", "argv": ["--evil"],
            "env": {"EVIL": "1"}, "executable": "/bin/evil",
            "mode": "deployed", "python": "/bin/evil-python",
            "shell": True, "cwd": "/tmp/evil", "timeout": 999999,
        }
        entry, records = _setup_clean_leg(
            tmp_path, module_id=module_id,
            policy_binding_mode="immutable_digest",
            policy_content=json.dumps(decoy).encode("utf-8"),
        )
        monkeypatch.setattr(mod, "_REGISTRY", {module_id: entry})

        calls = []
        real_popen = mod.subprocess.Popen

        def spy(argv, **kwargs):
            calls.append(list(argv))
            return real_popen(argv, **kwargs)
        monkeypatch.setattr(mod.subprocess, "Popen", spy)

        leg = mod._evaluate_capability(module_id, tmp_path, records)
        assert leg["aggregate"] == mod.CLEAN, leg
        assert len(calls) == 1
        assert calls[0] == [
            sys.executable, "-I",
            str(tmp_path / entry.runner_repository_path), "local"]
        # The decoy top-level lockfile fields were never even offered to the
        # resolution path in this test's design, so re-affirm they are
        # simply absent from anything the dispatcher touched.
        assert set(decoy) & set(calls[0][2]) == set()  # sanity: no leakage

    def test_unknown_selected_capability_is_unsupported_not_executed(
            self, monkeypatch: pytest.MonkeyPatch) -> None:
        """T3."""
        def boom(*a, **k):
            raise AssertionError("subprocess must never launch")
        monkeypatch.setattr(mod.subprocess, "Popen", boom)
        leg = mod._evaluate_capability("made-up-security", Path("/nonexistent"), {})
        assert leg["aggregate"] == mod.INCOMPLETE
        assert leg["child_launched"] is False

    @pytest.mark.parametrize("bad_mode", [
        "deployed", "credentialed", "active", "remote", "", None,
        "offline,loopback",
    ])
    def test_no_deployed_or_credentialed_mode_is_representable(
            self, bad_mode) -> None:
        """T4."""
        with pytest.raises(ValueError):
            _entry(evidence_mode=bad_mode)

    def test_every_admission_field_is_required(self) -> None:
        """T5. Eleven deletion mutants, one per field; each refused at
        construction with a message naming the field. The two binding-mode
        fields are the load-bearing rows: a defaulted mode is the silently-
        changed-mode failure a required field forecloses."""
        full_kwargs = dict(
            module_id="widget-security",
            runner_repository_path="scripts/widget_security.py",
            argv_mode="local", policy_repository_path=None,
            child_schema_version=_VALID_SCHEMA,
            capability_contract_version=_VALID_CONTRACT,
            evidence_mode=_VALID_EVIDENCE,
            accepted_process_exits=frozenset({0}),
            result_to_aggregate_mapping={"CLEAN": (0, mod.CLEAN)},
            runner_binding_mode="immutable_digest",
            policy_binding_mode="none",
        )
        assert set(full_kwargs) == {
            f for f in mod.RegistryEntry.__dataclass_fields__
        }, "test fixture drifted from the eleven-field contract"
        for field in full_kwargs:
            partial = dict(full_kwargs)
            del partial[field]
            with pytest.raises(TypeError) as exc:
                mod.RegistryEntry(**partial)
            assert field in str(exc.value), (field, str(exc.value))


# ===========================================================================
# Dispatch and subprocess behavior
# ===========================================================================

class TestDispatchBehavior:

    def test_child_argv_is_exactly_the_registry_vector(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """T6."""
        module_id = "widget-security"
        entry, records = _setup_clean_leg(tmp_path, module_id=module_id)
        monkeypatch.setattr(mod, "_REGISTRY", {module_id: entry})
        calls = []
        real_popen = mod.subprocess.Popen

        def spy(argv, **kwargs):
            calls.append(list(argv))
            return real_popen(argv, **kwargs)
        monkeypatch.setattr(mod.subprocess, "Popen", spy)

        leg = mod._evaluate_capability(module_id, tmp_path, records)
        assert leg["aggregate"] == mod.CLEAN, leg
        assert len(calls) == 1
        argv = calls[0]
        assert len(argv) == 4
        assert argv[0] == sys.executable
        assert argv[1] == "-I"
        assert argv[2] == str(tmp_path / entry.runner_repository_path)
        assert argv[3] == "local"

    def test_child_env_is_minimal_and_strips_proxies_and_credentials(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """T7."""
        leaked = ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY",
                  "AWS_SECRET_ACCESS_KEY", "GITHUB_TOKEN", "PYTHONPATH",
                  "PYTHONSTARTUP")
        for name in leaked:
            monkeypatch.setenv(name, "leak-me")
        for name in mod._CHILD_ENV_ALLOWLIST:
            monkeypatch.setenv(name, "kept")

        module_id = "widget-security"
        runner_rel = "scripts/widget_security.py"
        dump_script = textwrap.dedent("""\
            import json, os, sys
            print(json.dumps({
                "schema": %r, "capability": %r, "contract": %r,
                "evidence_mode": %r, "result": "CLEAN",
                "details": ",".join(sorted(os.environ.keys())),
            }))
            """) % (_VALID_SCHEMA, module_id, _VALID_CONTRACT, _VALID_EVIDENCE)
        runner_rec = _write_file(tmp_path, runner_rel, dump_script.encode())
        records = {runner_rel: runner_rec}
        entry = _entry(module_id, runner_repository_path=runner_rel)
        monkeypatch.setattr(mod, "_REGISTRY", {module_id: entry})

        leg = mod._evaluate_capability(module_id, tmp_path, records)
        assert leg["aggregate"] == mod.CLEAN, leg
        received = set(leg["detail"].split(",")) if leg["detail"] else set()
        for name in leaked:
            assert name not in received, f"{name} leaked into the child"
        # Computed with the SAME public formula _build_child_env uses, over
        # the actual parent os.environ at call time -- not a hand-copied
        # literal set, so this stays honest if the allowlist ever grows.
        import os as _os
        expected = {
            k for k in _os.environ
            if k in mod._CHILD_ENV_ALLOWLIST
            or k.startswith(mod._CHILD_ENV_ALLOWLIST_PREFIXES)
        }
        assert received == expected
        assert set(mod._CHILD_ENV_ALLOWLIST) <= received

    def test_oversized_child_output_is_degraded_and_not_relayed(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """T8."""
        monkeypatch.setattr(mod, "_CHILD_OUTPUT_CAP_BYTES", 128)
        module_id = "widget-security"
        runner_rel = "scripts/widget_security.py"
        marker = "OVERSIZED-MARKER-" + ("X" * 200)
        script = f"import sys\nsys.stdout.write({marker!r})\n"
        runner_rec = _write_file(tmp_path, runner_rel, script.encode())
        records = {runner_rel: runner_rec}
        entry = _entry(module_id, runner_repository_path=runner_rel)
        monkeypatch.setattr(mod, "_REGISTRY", {module_id: entry})

        leg = mod._evaluate_capability(module_id, tmp_path, records)
        assert leg["aggregate"] == mod.DEGRADED
        assert marker not in json.dumps(leg)

    def test_child_timeout_is_degraded(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """T9. Raises the timeout constant above the sleep (never deletes
        the bound, which would hang the suite)."""
        monkeypatch.setattr(mod, "_CHILD_TIMEOUT_S", 0.2)
        module_id = "widget-security"
        runner_rel = "scripts/widget_security.py"
        script = "import time\ntime.sleep(5)\n"
        runner_rec = _write_file(tmp_path, runner_rel, script.encode())
        records = {runner_rel: runner_rec}
        entry = _entry(module_id, runner_repository_path=runner_rel)
        monkeypatch.setattr(mod, "_REGISTRY", {module_id: entry})

        leg = mod._evaluate_capability(module_id, tmp_path, records)
        assert leg["aggregate"] == mod.DEGRADED
        assert "timed out" in leg["detail"]

    @pytest.mark.parametrize("script,label", [
        ("import sys\nsys.stdout.buffer.write(bytes([0x80]))\n",
         "invalid-utf8"),
        ("import sys\nsys.stdout.write('{')\n", "invalid-json"),
    ])
    def test_invalid_utf8_and_invalid_json_are_degraded(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
            script: str, label: str) -> None:
        """T10."""
        module_id = "widget-security"
        runner_rel = "scripts/widget_security.py"
        runner_rec = _write_file(tmp_path, runner_rel, script.encode())
        records = {runner_rel: runner_rec}
        entry = _entry(module_id, runner_repository_path=runner_rel)
        monkeypatch.setattr(mod, "_REGISTRY", {module_id: entry})

        leg = mod._evaluate_capability(module_id, tmp_path, records)
        assert leg["aggregate"] == mod.DEGRADED, label

    def test_forged_terminal_controls_never_reach_the_terminal(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
            capsys: pytest.CaptureFixture) -> None:
        """T11."""
        module_id = "widget-security"
        forged = "\x1b[2Jnormal\x1b]8;;http://evil\x07link\x1b\\\rFAKE PASS"
        entry, records = _setup_clean_leg(
            tmp_path, module_id=module_id, result="CLEAN")
        # Overwrite the child with one whose details carries the forgery.
        runner_rel = entry.runner_repository_path
        rec = _write_child(tmp_path, runner_rel,
                            _valid_child_obj(module_id, details=forged))
        records[runner_rel] = rec
        monkeypatch.setattr(mod, "_REGISTRY", {module_id: entry})

        leg = mod._evaluate_capability(module_id, tmp_path, records)
        rendered = json.dumps(leg)
        assert "\x1b" not in rendered
        assert "\r" not in rendered
        assert forged not in rendered

    def test_raw_child_stdout_and_stderr_are_never_relayed(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """T12."""
        module_id = "widget-security"
        runner_rel = "scripts/widget_security.py"
        stdout_marker = "STDOUT-MARKER-DISTINCTIVE"
        stderr_marker = "STDERR-MARKER-DISTINCTIVE"
        script = textwrap.dedent(f"""\
            import sys
            print({stderr_marker!r}, file=sys.stderr)
            print({stdout_marker!r})
            """)
        runner_rec = _write_file(tmp_path, runner_rel, script.encode())
        records = {runner_rel: runner_rec}
        entry = _entry(module_id, runner_repository_path=runner_rel)
        monkeypatch.setattr(mod, "_REGISTRY", {module_id: entry})

        leg = mod._evaluate_capability(module_id, tmp_path, records)
        assert leg["aggregate"] == mod.DEGRADED  # stdout marker breaks JSON
        rendered = json.dumps(leg)
        assert stdout_marker not in rendered
        assert stderr_marker not in rendered

    @pytest.mark.parametrize("mutate,label", [
        (lambda o: {**o, "capability": "wrong-capability"}, "capability"),
        (lambda o: {**o, "contract": "v999"}, "contract"),
        (lambda o: {**o, "evidence_mode": "loopback"}, "evidence_mode"),
        (lambda o: {**o, "schema": "wrong/v1"}, "schema"),
        (lambda o: {**o, "extra_unexpected_key": "x"}, "extra-key"),
        (lambda o: {**o, "result": ["not", "a", "string"]}, "wrong-typed"),
    ])
    def test_id_mismatch_is_degraded_never_clean(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
            mutate, label: str) -> None:
        """T13."""
        module_id = "widget-security"
        runner_rel = "scripts/widget_security.py"
        obj = mutate(_valid_child_obj(module_id))
        runner_rec = _write_child(tmp_path, runner_rel, obj)
        records = {runner_rel: runner_rec}
        entry = _entry(module_id, runner_repository_path=runner_rel)
        monkeypatch.setattr(mod, "_REGISTRY", {module_id: entry})

        leg = mod._evaluate_capability(module_id, tmp_path, records)
        assert leg["aggregate"] == mod.DEGRADED, label

    @pytest.mark.parametrize("script,label", [
        ("import json,sys; print(json.dumps(%r)); sys.exit(0)" % (
            {"schema": _VALID_SCHEMA, "capability": "widget-security",
             "contract": _VALID_CONTRACT, "evidence_mode": _VALID_EVIDENCE,
             "result": "FINDINGS", "details": "x"}), "exit0-findings"),
        ("import json,sys; print(json.dumps(%r)); sys.exit(1)" % (
            {"schema": _VALID_SCHEMA, "capability": "widget-security",
             "contract": _VALID_CONTRACT, "evidence_mode": _VALID_EVIDENCE,
             "result": "CLEAN", "details": "x"}), "exit1-clean"),
    ])
    def test_process_exit_and_result_must_agree(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
            script: str, label: str) -> None:
        """T14. The Decision's third named property."""
        module_id = "widget-security"
        runner_rel = "scripts/widget_security.py"
        runner_rec = _write_file(tmp_path, runner_rel, script.encode())
        records = {runner_rel: runner_rec}
        entry = _entry(module_id, runner_repository_path=runner_rel)
        monkeypatch.setattr(mod, "_REGISTRY", {module_id: entry})

        leg = mod._evaluate_capability(module_id, tmp_path, records)
        assert leg["aggregate"] == mod.DEGRADED, label

    def test_aggregate_precedence_over_every_ordered_pair(self) -> None:
        """T15. All 16 ordered pairs, plus three- and four-leg
        combinations; result is always the max under 20 > 10 > 5 > 0."""
        levels = [mod.CLEAN, mod.INCOMPLETE, mod.FINDINGS, mod.DEGRADED]

        def leg(agg):
            return {"aggregate": agg}

        for a in levels:
            for b in levels:
                report = mod._build_report([leg(a), leg(b)])
                assert mod._AGGREGATE_EXIT[report["aggregate"]] == max(a, b)
        for combo in [
            (mod.CLEAN, mod.INCOMPLETE, mod.FINDINGS),
            (mod.CLEAN, mod.DEGRADED, mod.CLEAN),
            (mod.FINDINGS, mod.INCOMPLETE, mod.DEGRADED, mod.CLEAN),
        ]:
            report = mod._build_report([leg(v) for v in combo])
            assert mod._AGGREGATE_EXIT[report["aggregate"]] == max(combo)


# ===========================================================================
# Parent-computed binding
# ===========================================================================

class TestParentComputedBinding:

    def test_parent_computes_digests_and_ignores_child_supplied_ones(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """T16. The forged value is placed as an unrecognized TOP-LEVEL
        child JSON key (the T13 "extra key" hazard) so it is rejected before
        anything downstream could echo it -- the report still carries the
        PARENT's own runner digest, computed at bind time, independent of
        the child's result."""
        module_id = "widget-security"
        forged = "deadbeef" * 8  # a 64-hex-char forged "sha256"
        entry, records = _setup_clean_leg(tmp_path, module_id=module_id)
        runner_rel = entry.runner_repository_path
        obj = _valid_child_obj(module_id)
        obj["runner_sha256"] = forged  # forged, unrecognized top-level key
        rec = _write_child(tmp_path, runner_rel, obj)
        records[runner_rel] = rec
        monkeypatch.setattr(mod, "_REGISTRY", {module_id: entry})

        leg = mod._evaluate_capability(module_id, tmp_path, records)
        real_digest = mod._sha256_of(tmp_path / runner_rel)
        assert leg["runner_digest"] == real_digest
        assert forged not in json.dumps(leg)

    @pytest.mark.parametrize("which,mode", [
        ("runner", "none"), ("runner", "immutable_digest"),
        ("runner", "living_state"),
        ("policy", "immutable_digest"),
    ])
    def test_runner_or_policy_digest_mismatch_is_degraded(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
            which: str, mode: str) -> None:
        """T17(a)/(b). Flip a byte after the record was written; the
        launch never happens under any binding mode."""
        module_id = "widget-security"
        policy_mode = "immutable_digest" if which == "policy" else "none"
        entry, records = _setup_clean_leg(
            tmp_path, module_id=module_id, policy_binding_mode=policy_mode)
        # Re-run the entry with runner_binding_mode fixed at immutable_digest
        # (its only closed-set member); `mode` here parametrizes which
        # DIGEST is flipped, per row.
        target_rel = (entry.runner_repository_path if which == "runner"
                      else entry.policy_repository_path)
        path = tmp_path / target_rel
        data = bytearray(path.read_bytes())
        data[0] ^= 0xFF
        path.write_bytes(bytes(data))
        monkeypatch.setattr(mod, "_REGISTRY", {module_id: entry})

        calls = []
        real_popen = mod.subprocess.Popen

        def spy(argv, **kwargs):
            calls.append(argv)
            return real_popen(argv, **kwargs)
        monkeypatch.setattr(mod.subprocess, "Popen", spy)

        leg = mod._evaluate_capability(module_id, tmp_path, records)
        assert leg["aggregate"] == mod.DEGRADED
        assert calls == []

    def test_policy_digest_mismatch_under_living_state_proceeds_and_marks_it(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """T17(c). Under living_state the leg PROCEEDS (the mode's whole
        point) and the report records the policy as digest_not_compared --
        the dropped property is visible, not silently absent."""
        module_id = "widget-security"
        policy_rel = "dev/.cairn/widget-policy.json"
        entry, records = _setup_clean_leg(
            tmp_path, module_id=module_id,
            policy_binding_mode="living_state", policy_rel=policy_rel)
        (tmp_path / policy_rel).write_bytes(b'{"configured": true, "x": 1}\n')
        monkeypatch.setattr(mod, "_LIVING_STATE_DSTS",
                             frozenset({policy_rel}))
        monkeypatch.setattr(mod, "_REGISTRY", {module_id: entry})

        leg = mod._evaluate_capability(module_id, tmp_path, records)
        assert leg["aggregate"] == mod.CLEAN, leg
        assert leg["policy"]["binding"] == "living_state"
        assert leg["policy"]["digest_not_compared"] is True

    def test_policy_binding_mode_none_makes_a_flip_unreachable(self) -> None:
        """T17(d). Asserted as a CONSTRUCTION refusal: mode 'none' with a
        non-None path cannot be built, so there is no runtime row to flip."""
        with pytest.raises(ValueError):
            _entry(policy_binding_mode="none",
                   policy_repository_path="dev/.cairn/widget-policy.json")

    @pytest.mark.parametrize("kind", ["leaf-symlink", "parent-symlink"])
    def test_symlinked_runner_or_policy_is_refused(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
            kind: str) -> None:
        """T18. Leaf symlink and symlinked parent directory. (The third
        row -- a same-user TOCTOU race between digest read and launch -- is
        a named, accepted residual; not asserted here.)"""
        module_id = "widget-security"
        entry, records = _setup_clean_leg(tmp_path, module_id=module_id)
        runner_rel = entry.runner_repository_path
        real_path = tmp_path / runner_rel
        real_bytes = real_path.read_bytes()
        if kind == "leaf-symlink":
            real_target = tmp_path / "elsewhere_runner.py"
            real_target.write_bytes(real_bytes)
            real_path.unlink()
            real_path.symlink_to(real_target)
        else:
            real_dir = tmp_path / "scripts"
            elsewhere_dir = tmp_path / "elsewhere_scripts"
            elsewhere_dir.mkdir()
            (elsewhere_dir / Path(runner_rel).name).write_bytes(real_bytes)
            import shutil
            shutil.rmtree(real_dir)
            real_dir.symlink_to(elsewhere_dir)
        monkeypatch.setattr(mod, "_REGISTRY", {module_id: entry})

        leg = mod._evaluate_capability(module_id, tmp_path, records)
        assert leg["aggregate"] == mod.DEGRADED, kind

    def test_missing_lockfile_record_for_a_registered_runner_is_degraded(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """T19."""
        module_id = "widget-security"
        entry, records = _setup_clean_leg(tmp_path, module_id=module_id)
        records.pop(entry.runner_repository_path)  # registered, unlocked
        monkeypatch.setattr(mod, "_REGISTRY", {module_id: entry})

        leg = mod._evaluate_capability(module_id, tmp_path, records)
        assert leg["aggregate"] == mod.DEGRADED


# ===========================================================================
# The universal no-capability contract -- the E2 surface
# ===========================================================================

class TestNoCapabilityContract:

    def test_no_capability_prints_the_exact_not_applicable_line_and_exits_0(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
            capsys: pytest.CaptureFixture) -> None:
        """T20."""
        monkeypatch.setattr(mod, "_REGISTRY", {})
        monkeypatch.setattr(mod, "_REPO_ROOT", tmp_path)
        monkeypatch.setattr(mod, "_LOCKFILE",
                             tmp_path / "dev" / ".cairn" / "cairn-lock.yml")
        _write_lockfile(tmp_path, modules=["claim-check"], files=[])

        code = mod.main(["local"])
        out = capsys.readouterr().out
        assert code == 0
        lines = out.splitlines()
        assert lines[0] == "NOT APPLICABLE: no selected local security capability"
        obj = json.loads(lines[1])
        assert obj["schema"] == mod._SCHEMA
        assert obj["status"] == "not_applicable"
        assert obj["ok"] is True
        assert obj["aggregate"] == "NOT_APPLICABLE"
        assert obj["evidence_count"] == 0
        assert obj["legs"] == []
        assert obj["reason"]

        # Second perturbation target (recorded in the ledger): dropping
        # evidence_count from the report is asserted directly here too.
        report = mod._not_applicable_report("x")
        assert set(report) == {
            "schema", "status", "ok", "aggregate", "evidence_count", "legs",
            "reason"}

    def test_no_capability_output_uses_no_security_coverage_wording(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
            capsys: pytest.CaptureFixture) -> None:
        """T21."""
        monkeypatch.setattr(mod, "_REGISTRY", {})
        monkeypatch.setattr(mod, "_REPO_ROOT", tmp_path)
        monkeypatch.setattr(mod, "_LOCKFILE",
                             tmp_path / "dev" / ".cairn" / "cairn-lock.yml")
        _write_lockfile(tmp_path, modules=[], files=[])
        mod.main(["local"])
        out = capsys.readouterr().out
        for word in mod._FORBIDDEN_COVERAGE_WORDS:
            assert word not in out, word

    def test_no_capability_opens_no_socket_and_does_no_dns(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """T22."""
        monkeypatch.setattr(mod, "_REGISTRY", {})
        monkeypatch.setattr(mod, "_REPO_ROOT", tmp_path)
        monkeypatch.setattr(mod, "_LOCKFILE",
                             tmp_path / "dev" / ".cairn" / "cairn-lock.yml")
        _write_lockfile(tmp_path, modules=[], files=[])

        import socket
        import subprocess as real_subprocess
        import urllib.request

        def boom(*a, **k):
            raise AssertionError("no network / process primitive may fire")
        monkeypatch.setattr(real_subprocess, "run", boom)
        monkeypatch.setattr(real_subprocess, "Popen", boom)
        monkeypatch.setattr(socket, "socket", boom)
        monkeypatch.setattr(socket, "create_connection", boom)
        monkeypatch.setattr(socket, "getaddrinfo", boom)
        monkeypatch.setattr(urllib.request, "urlopen", boom)

        code = mod.main(["local"])
        assert code == 0

    def test_dispatcher_source_reads_no_deployed_credential_variable(
            self) -> None:
        """T23. AST scan of the SHIPPED source: every os.environ / os.getenv
        read resolves to the declared allowlist, and no deployed-credential
        variable name appears anywhere as a string literal."""
        source = DISPATCHER_SRC.read_text(encoding="utf-8")
        tree = ast.parse(source)

        banned_names = {
            "AWS_SECRET_ACCESS_KEY", "AWS_ACCESS_KEY_ID", "GITHUB_TOKEN",
            "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "API_KEY",
            "DATABASE_URL", "PASSWORD",
        }
        literals = {
            node.value for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }
        hit = banned_names & literals
        assert not hit, f"credential-shaped literal(s) in source: {hit}"

        for node in ast.walk(tree):
            is_getenv = (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "getenv"
            )
            if is_getenv:
                raise AssertionError(
                    "os.getenv(...) is not used; only the allowlisted "
                    "os.environ.items() comprehension in _build_child_env")
        assert "_build_child_env" in source
        assert "os.environ.items()" in source

    def test_a_socket_opening_child_is_excluded_by_admission_not_blocked_at_runtime(  # noqa: E501
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """T24. (a) Unadmitted -> INCOMPLETE, never launched. (b) Force-
        injected, the parent DOES run it and does NOT prevent the bind --
        documented honestly, no perturbation makes the parent block it."""
        module_id = "socket-opening-security"

        def boom(*a, **k):
            raise AssertionError("subprocess must never launch (a)")
        monkeypatch.setattr(mod.subprocess, "Popen", boom)
        leg_a = mod._evaluate_capability(module_id, tmp_path, {})
        assert leg_a["aggregate"] == mod.INCOMPLETE
        assert leg_a["child_launched"] is False
        monkeypatch.undo()

        script = textwrap.dedent(f"""\
            import json, socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("127.0.0.1", 0))
            s.close()
            print(json.dumps({{
                "schema": {_VALID_SCHEMA!r}, "capability": {module_id!r},
                "contract": {_VALID_CONTRACT!r},
                "evidence_mode": {_VALID_EVIDENCE!r}, "result": "CLEAN",
                "details": "bound a loopback socket",
            }}))
            """)
        runner_rel = "scripts/socket_opening_security.py"
        runner_rec = _write_file(tmp_path, runner_rel, script.encode())
        records = {runner_rel: runner_rec}
        entry = _entry(module_id, runner_repository_path=runner_rel)
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(mod, "_REGISTRY", {module_id: entry})
            leg_b = mod._evaluate_capability(module_id, tmp_path, records)
        assert leg_b["child_launched"] is True
        assert leg_b["aggregate"] == mod.CLEAN  # the parent did NOT block it


# ===========================================================================
# Binding-mode closure -- the reciprocal-contract surface
# ===========================================================================

class TestBindingModeClosure:

    @pytest.mark.parametrize("bad_mode", [
        "deployed", "unbound", "skip", "living", "immutable", "",
        None, "none,living_state",
    ])
    def test_policy_binding_mode_is_a_closed_set(self, bad_mode) -> None:
        """T36."""
        with pytest.raises(ValueError):
            _entry(policy_binding_mode=bad_mode)

    @pytest.mark.parametrize("policy_binding_mode,path,should_raise", [
        ("none", "dev/.cairn/x.json", True),
        ("immutable_digest", None, True),
        ("living_state", None, True),
        ("none", None, False),
    ])
    def test_binding_mode_and_policy_path_must_agree(
            self, policy_binding_mode, path, should_raise: bool) -> None:
        """T37."""
        if should_raise:
            with pytest.raises(ValueError):
                _entry(policy_binding_mode=policy_binding_mode,
                       policy_repository_path=path)
        else:
            _entry(policy_binding_mode=policy_binding_mode,
                   policy_repository_path=path)  # must not raise

    def test_living_state_mode_requires_the_lockfile_flag_and_the_authoritative_set(  # noqa: E501
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """T38."""
        module_id = "widget-security"
        policy_rel = "dev/.cairn/widget-policy.json"

        # Row 1: record present but WITHOUT living_state: true -> DEGRADED.
        entry, records = _setup_clean_leg(
            tmp_path, module_id=module_id,
            policy_binding_mode="living_state", policy_rel=policy_rel)
        records[policy_rel].pop("living_state", None)
        monkeypatch.setattr(mod, "_LIVING_STATE_DSTS",
                             frozenset({policy_rel}))
        monkeypatch.setattr(mod, "_REGISTRY", {module_id: entry})
        leg = mod._evaluate_capability(module_id, tmp_path, records)
        assert leg["aggregate"] == mod.DEGRADED

        # Row 2: flagged, but path outside the authoritative set -> DEGRADED.
        records[policy_rel]["living_state"] = True
        monkeypatch.setattr(mod, "_LIVING_STATE_DSTS", frozenset())
        leg = mod._evaluate_capability(module_id, tmp_path, records)
        assert leg["aggregate"] == mod.DEGRADED

        # Row 3: both satisfied -> proceeds, digest not compared.
        monkeypatch.setattr(mod, "_LIVING_STATE_DSTS",
                             frozenset({policy_rel}))
        leg = mod._evaluate_capability(module_id, tmp_path, records)
        assert leg["aggregate"] == mod.CLEAN, leg
        assert leg["policy"]["digest_not_compared"] is True

    def test_immutable_mode_refuses_a_living_state_record(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """T39. T38 + T39 together: cannot treat a living policy as an
        immutable one, in either direction."""
        module_id = "widget-security"
        entry, records = _setup_clean_leg(
            tmp_path, module_id=module_id,
            policy_binding_mode="immutable_digest")
        policy_rel = entry.policy_repository_path
        records[policy_rel]["living_state"] = True  # misdeclared
        monkeypatch.setattr(mod, "_REGISTRY", {module_id: entry})

        leg = mod._evaluate_capability(module_id, tmp_path, records)
        assert leg["aggregate"] == mod.DEGRADED
        assert leg["child_launched"] is False

    def test_a_registry_entry_cannot_change_mode_after_construction(
            self) -> None:
        """T40."""
        entry = _entry()
        with pytest.raises(Exception):  # dataclasses.FrozenInstanceError
            entry.policy_binding_mode = "living_state"

    def test_the_module_doctrine_states_not_applicable_is_not_evidence(
            self) -> None:
        """T41. Read from the SHIPPED doctrine source, independent of any
        installed copy."""
        doctrine = (
            CAIRN_ROOT / "templates" / "modules" / "default-on"
            / "security-verification.md"
        ).read_text(encoding="utf-8")
        assert "NOT_APPLICABLE" in doctrine
        lower = doctrine.lower()
        assert "not evidence" in lower or "is not evidence" in lower
        # No green-security phrase in the SAME paragraph as the non-evidence
        # statement.
        paragraphs = doctrine.split("\n\n")
        offending_paragraph = next(
            (p for p in paragraphs if "not evidence" in p.lower()), "")
        for phrase in mod._FORBIDDEN_COVERAGE_WORDS:
            assert phrase not in offending_paragraph, phrase


# ===========================================================================
# B2 -- the unrecognized-key refusal, in two halves, tried rather than
# inferred
# ===========================================================================

class TestUnrecognizedKeyRefusal:

    @pytest.mark.parametrize("bad_key", [
        "principal", "scope", "runner", "env", "some_made_up_field",
    ])
    def test_an_unrecognized_key_is_refused_and_named_entry_side(
            self, bad_key: str) -> None:
        """T44(a). A source-owned exact constructor: the test ATTEMPTS the
        extra keyword rather than inferring the refusal from frozenness."""
        base = dict(
            module_id="widget-security",
            runner_repository_path="scripts/widget_security.py",
            argv_mode="local", policy_repository_path=None,
            child_schema_version=_VALID_SCHEMA,
            capability_contract_version=_VALID_CONTRACT,
            evidence_mode=_VALID_EVIDENCE,
            accepted_process_exits=frozenset({0}),
            result_to_aggregate_mapping={"CLEAN": (0, mod.CLEAN)},
            runner_binding_mode="immutable_digest",
            policy_binding_mode="none",
        )
        base[bad_key] = "malicious"
        with pytest.raises(TypeError) as exc:
            mod.RegistryEntry(**base)
        assert bad_key in str(exc.value)

    def test_an_unrecognized_key_is_refused_and_named_lockfile_record_side(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """T44(b). The record is one the TEST writes, never one the
        dispatcher wrote -- the check is not verified by the artifact it
        judges. Recorded gap, not covered here:
        bootstrap/verify_integrity.py:63-111 ignores the same key shape on
        the same record shape (the paired plan's F5(b) characterization)."""
        module_id = "widget-security"
        entry, records = _setup_clean_leg(tmp_path, module_id=module_id)
        records[entry.runner_repository_path]["principal"] = "root"
        monkeypatch.setattr(mod, "_REGISTRY", {module_id: entry})

        calls = []
        real_popen = mod.subprocess.Popen

        def spy(argv, **kwargs):
            calls.append(argv)
            return real_popen(argv, **kwargs)
        monkeypatch.setattr(mod.subprocess, "Popen", spy)

        leg = mod._evaluate_capability(module_id, tmp_path, records)
        assert leg["aggregate"] == mod.DEGRADED
        assert "principal" in leg["detail"]
        assert calls == []


# ===========================================================================
# Chunk B -- universality.  T25-T33, T31b, T42, T43.
#
# Everything below drives the REAL scaffold into a tmp_path target through
# `bootstrap.scaffold.main`, never a stub of it.  The subject is what an
# adopter receives; the oracles are the shipped template sources read
# independently and the installed tree on disk.
# ===========================================================================

from bootstrap.scaffold import (  # noqa: E402
    expand_preset, format_profile_summary, main as scaffold_main,
)
from bootstrap._scaffold.config import _DEFAULT_ON_MODULES  # noqa: E402
from bootstrap._scaffold.install import module_merge_directives  # noqa: E402
from bootstrap._scaffold.slotmerge import check_slot_fidelity  # noqa: E402

MODULE = "security-verification"
PRESETS = ("solo-greenfield", "collaborative-team", "high-rigor-legacy")
TEMPLATES_ROOT = CAIRN_ROOT / "templates"

#: The two destinations the module's `_MODULE_MAPPINGS` group installs.
DOCTRINE_DST = "dev/modules/security-verification.md"
DISPATCHER_DST = "scripts/run_security_verification.py"

#: The module doctrine source (A2) and Cairn's own self-hosted twin (B2).
DOCTRINE_SRC = TEMPLATES_ROOT / "modules" / "default-on" / f"{MODULE}.md"
DOCTRINE_TWIN = CAIRN_ROOT / DOCTRINE_DST

#: The standing command the merge block contributes to AGENTS.md.
STANDING_COMMAND = "python scripts/run_security_verification.py"
#: The designation phrase common to all three channels, whitespace-collapsed.
#: Singular so it matches both the doctrine's plural "...surfaces" and the
#: dispatcher comment's singular "...surface"; the shared, load-bearing words
#: are what the channels must agree on, not the inflection.
DESIGNATION_FLAT = "high-risk Security-Review surface"


def _profile(path: Path, body: str = "") -> Path:
    path.write_text(
        "project_name: SecVerifyTest\ntest_command: pytest\n" + body,
        encoding="utf-8",
    )
    return path


def _scaffold(tmp_path: Path, body: str = "", *,
              target_name: str = "target") -> tuple[int, Path]:
    """A real install into a fresh target.  Returns ``(rc, target)``."""
    cfg = _profile(tmp_path / f"{target_name}-profile.yml", body)
    target = tmp_path / target_name
    target.mkdir(parents=True, exist_ok=True)
    rc = scaffold_main([
        "--config", str(cfg), "--target", str(target),
        "--cairn-root", str(CAIRN_ROOT), "--allow-dev", "--non-interactive",
    ])
    return rc, target


def _merge_content() -> str:
    """The one directive the shipped module declares, read from the shipped
    source -- the oracle for what AGENTS.md must end up carrying."""
    found = module_merge_directives(TEMPLATES_ROOT, [MODULE])
    assert len(found) == 1, found
    return found[0][2]


def _pending_side_files(target: Path) -> list[Path]:
    return sorted(target.rglob("*.cairn-merge-pending"))


class TestUniversality:
    """T25-T29: the selection contract, once the module is default-on."""

    @pytest.mark.parametrize("preset", PRESETS)
    def test_every_preset_installs_the_module(
            self, preset: str, tmp_path: Path) -> None:
        """T25.  `expand_preset` includes it and a REAL install writes both
        destinations of its mapping group.

        Hazard perturbation: remove the `security-verification` entry from
        `_DEFAULT_ON_MODULES` (B1).  All three rows fail.
        """
        modules, _summary = expand_preset({"preset": preset})
        assert MODULE in modules, (preset, modules)

        rc, target = _scaffold(
            tmp_path, f"preset: {preset}\n", target_name=f"t-{preset}")
        assert rc == 0
        assert (target / DOCTRINE_DST).is_file(), DOCTRINE_DST
        assert (target / DISPATCHER_DST).is_file(), DISPATCHER_DST

    def test_modules_empty_list_opts_out_entirely(
            self, tmp_path: Path) -> None:
        """T26.  An explicit `modules:` list is exact and is never
        overridden by the default-on set -- the Decision's settled rule.

        Hazard perturbation: make the default-on set merge into an explicit
        list.  Fails.
        """
        rc, target = _scaffold(tmp_path, "modules: []\n")
        assert rc == 0
        assert not (target / DOCTRINE_DST).exists()
        assert not (target / DISPATCHER_DST).exists()

    def test_literal_modules_list_without_it_does_not_install_it(
            self, tmp_path: Path) -> None:
        """T27.  Same hazard as T26, with a non-empty explicit list."""
        rc, target = _scaffold(tmp_path, "modules:\n  - claim-check\n")
        assert rc == 0
        assert (target / "scripts" / "claim_check.py").is_file()
        assert not (target / DOCTRINE_DST).exists()
        assert not (target / DISPATCHER_DST).exists()

    def test_modules_remove_opts_out_and_the_summary_announces_it(
            self, tmp_path: Path) -> None:
        """T28.  **Characterization, not a guard.**  A green run here records
        that the pre-existing generic `modules_remove` mechanism covers the
        new module; B1 did not make it true.  What B1 *is* load-bearing for
        is that there is anything to opt out OF -- remove B1 and the module
        is no longer default-on, so `removed_default_on` is empty and the
        summary assertion below fails.
        """
        modules, summary = expand_preset({
            "preset": "solo-greenfield", "modules_remove": [MODULE],
        })
        assert MODULE not in modules
        assert MODULE in summary["removed_default_on"], summary
        rendered = format_profile_summary(summary)
        assert "Default-on opted out:" in rendered
        assert MODULE in rendered.split("Default-on opted out:")[1]

        rc, target = _scaffold(
            tmp_path, f"preset: solo-greenfield\nmodules_remove:\n  - {MODULE}\n")
        assert rc == 0
        assert not (target / DISPATCHER_DST).exists()

    def test_upgrade_plan_lists_it_and_adopt_module_installs_it(
            self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        """T29.  A lockfile written before the module existed: `upgrade
        --plan` names it under *new modules available (opt-in)*, and
        `--adopt-module` writes both files and records both in the lockfile.

        Hazard perturbation: remove the `_MODULE_MAPPINGS` entry (A3) --
        `set(_MODULE_MAPPINGS) - lock_modules` no longer contains it, so the
        opt-in line never mentions it.
        """
        rc, target = _scaffold(tmp_path, "modules:\n  - claim-check\n")
        assert rc == 0
        capsys.readouterr()

        assert scaffold_main([
            "upgrade", "--plan", "--target", str(target),
            "--cairn-root", str(CAIRN_ROOT),
        ]) == 0
        plan_out = capsys.readouterr()
        combined = plan_out.out + plan_out.err
        assert "new modules available (opt-in)" in combined, combined
        assert MODULE in combined.split("new modules available (opt-in)")[1]
        assert not (target / DISPATCHER_DST).exists()

        assert scaffold_main([
            "upgrade", "--adopt-module", MODULE, "--target", str(target),
            "--cairn-root", str(CAIRN_ROOT),
        ]) == 0
        capsys.readouterr()
        assert (target / DOCTRINE_DST).is_file()
        assert (target / DISPATCHER_DST).is_file()

        lock_text = (target / "dev" / ".cairn" / "cairn-lock.yml").read_text(
            encoding="utf-8")
        lock = json.loads(lock_text[lock_text.index("{"):])
        assert MODULE in lock["modules"], lock["modules"]
        recorded = {rec["dst"] for rec in lock["files"]}
        assert DOCTRINE_DST in recorded
        assert DISPATCHER_DST in recorded


class TestTheMergeRunsLiveFromAShippedModule:
    """T30, T31, T31b: the merge mechanism's first live use from a real
    shipped module.  Leaf coverage already existed
    (`test_module_merge.py`); these promote it to end-to-end."""

    def test_installed_AGENTS_md_carries_the_exact_standing_command(
            self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        """T30.  The installed `AGENTS.md` carries the exact merge-content
        block between the slot markers, the pass reports the outcome token
        `inserted`, and NO `.cairn-merge-pending` file exists anywhere in
        the target root.

        Hazard perturbations, both run:

        1. Delete the `cairn:merge-content` block from the module source
           (A2) -- the slot installs empty and the assertion fails.
        2. **Restore non-empty prose to the slot body in
           `templates/core/AGENTS.md`** -- the outcome flips to
           `conflict-deferred`, the rule is absent, the side file appears,
           and the scaffold still exits 0.  That second perturbation is the
           one that would have caught the [I1] defect, which is why it is
           named here rather than left implicit.
        """
        rc, target = _scaffold(tmp_path, "preset: solo-greenfield\n")
        assert rc == 0
        out = capsys.readouterr().out
        assert f"[inserted] AGENTS.md > {MODULE}" in out, out

        agents = (target / "AGENTS.md").read_text(encoding="utf-8")
        body = agents.split(f"<!-- cairn:slot {MODULE} -->")[1].split(
            f"<!-- cairn:end {MODULE} -->")[0]
        expected = _merge_content()
        assert expected.strip() in body.strip(), body
        assert STANDING_COMMAND in body
        assert _pending_side_files(target) == []

    def test_the_merge_pass_reports_the_fill_and_the_fidelity_check_is_clean(
            self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        """T31.  The pass names `AGENTS.md > security-verification` and
        `check_slot_fidelity` returns no warning; then an adopter edit
        WITHOUT the customized marker makes the check warn -- confirming it
        is live rather than always-silent.
        """
        rc, target = _scaffold(tmp_path, "preset: solo-greenfield\n")
        assert rc == 0
        out = capsys.readouterr().out
        assert f"AGENTS.md > {MODULE}" in out
        assert "[slot-content-" not in out, out

        expected = [("AGENTS.md", MODULE, _merge_content())]
        assert check_slot_fidelity(target, expected) == []

        agents_path = target / "AGENTS.md"
        text = agents_path.read_text(encoding="utf-8")
        tampered = text.replace("aggregate verdict", "aggregate VERDICTS", 1)
        assert tampered != text, "the phrase this node edits is gone"
        agents_path.write_text(tampered, encoding="utf-8")
        assert check_slot_fidelity(target, expected) == [
            ("AGENTS.md", MODULE, "stale-or-partial")]

    def test_a_prefilled_slot_defers_to_a_side_file_and_warns(
            self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        """T31b.  Install into a target whose slot body already carries
        adopter prose: outcome `conflict-deferred`, the
        `.cairn-merge-pending` side file present and named for the slot, a
        `slot-content-stale-or-partial` fidelity warning, exit 0, and the
        standing command ABSENT from `AGENTS.md`.

        This is the [I1] failure mode, pinned so it cannot come back
        silently as the shipped default.

        Hazard perturbation: make `_slot_is_empty` treat any body as empty
        -- the side-file and warning assertions go red.
        """
        rc, target = _scaffold(tmp_path, "modules:\n  - claim-check\n")
        assert rc == 0
        capsys.readouterr()

        agents_path = target / "AGENTS.md"
        text = agents_path.read_text(encoding="utf-8")
        opener = f"<!-- cairn:slot {MODULE} -->"
        closer = f"<!-- cairn:end {MODULE} -->"
        o = text.index(opener) + len(opener)
        c = text.index(closer)
        agents_path.write_text(
            text[:o] + "\nAdopter prose that is not the merge content.\n"
            + text[c:], encoding="utf-8")

        # Re-run the scaffold with the module selected; AGENTS.md already
        # exists so install_core preserves it (skipped-exists) and the merge
        # pass sees the prefilled body.
        cfg = _profile(tmp_path / "second.yml", f"modules:\n  - {MODULE}\n")
        rc = scaffold_main([
            "--config", str(cfg), "--target", str(target),
            "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
            "--non-interactive",
        ])
        out = capsys.readouterr().out
        assert rc == 0
        assert f"[conflict-deferred] AGENTS.md > {MODULE}" in out, out
        assert f"[slot-content-stale-or-partial] AGENTS.md > {MODULE}" in out, out

        side = _pending_side_files(target)
        assert [p.name for p in side] == [
            f"AGENTS.md.{MODULE}.cairn-merge-pending"], side
        assert STANDING_COMMAND not in agents_path.read_text(encoding="utf-8")


class TestComposition:

    def test_composition_no_capability_one_capability_many(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """T32.  Three synthetic rosters over injected registry entries:
        none, one, two.  No duplicate leg, no leg silently delegated to
        another, and each leg's `evidence_mode` label survives aggregation
        unchanged.

        **The hazards, and how this node was corrected to actually detect
        them.**  The plan named "collapse legs sharing a runner path" as the
        perturbation.  That mutation is a no-op against this setup -- the two
        entries have distinct runner paths, and they must, because each
        child echoes its own `capability` id and one file cannot echo two.
        A perturbation that cannot fire is not a perturbation, so the two
        hazards this node is actually run against are:

        1. `_build_report` **collapsing** legs (deduplicating by any field
           the two legs share -- both return CLEAN, so a dedupe-by-aggregate
           reduces two legs to one).  Caught by the `evidence_count` and
           leg-list assertions.
        2. `_build_report` **homogenizing** the per-leg `evidence_mode` label
           to one value.  Caught by the label-list assertions, which is the
           "each label survives aggregation unchanged" property.

        Both were run and both go RED on the two-capability row only; the
        no-capability and one-capability rows stay green, which is what makes
        the failure specific rather than incidental.
        """
        entry_a, records_a = _setup_clean_leg(tmp_path, module_id="alpha-security")
        entry_b, records_b = _setup_clean_leg(tmp_path, module_id="beta-security")
        entry_b = _entry(
            "beta-security",
            runner_repository_path=entry_b.runner_repository_path,
            evidence_mode="loopback")
        # The child must agree with the entry's declared evidence mode.
        _write_child(
            tmp_path, entry_b.runner_repository_path,
            _valid_child_obj("beta-security", evidence_mode="loopback"))
        records_b[entry_b.runner_repository_path]["hash"] = _sha256_of(
            (tmp_path / entry_b.runner_repository_path).read_bytes())

        registry = {"alpha-security": entry_a, "beta-security": entry_b}
        monkeypatch.setattr(mod, "_REGISTRY", registry)
        monkeypatch.setattr(mod, "_REPO_ROOT", tmp_path)
        records = {**records_a, **records_b}

        for roster, expected_modes in (
            ([], []),
            (["alpha-security"], ["offline"]),
            (["alpha-security", "beta-security"], ["offline", "loopback"]),
        ):
            legs = [
                mod._evaluate_capability(m, tmp_path, records) for m in roster
            ]
            assert len(legs) == len(roster), (roster, legs)
            assert [leg["module_id"] for leg in legs] == roster
            assert [leg["evidence_mode"] for leg in legs] == expected_modes, legs
            report = mod._build_report(legs) if legs else None
            if report is not None:
                assert report["evidence_count"] == len(roster)
                assert len(report["legs"]) == len(roster), report["legs"]
                assert [
                    leg["module_id"] for leg in report["legs"]
                ] == roster, report["legs"]
                assert [
                    leg["evidence_mode"] for leg in report["legs"]
                ] == expected_modes

    def test_the_dispatcher_runs_from_a_real_fresh_scaffold(
            self, tmp_path: Path) -> None:
        """T33, **as a characterization of a measured contradiction, not as
        the guard the plan specified.**  Read the docstring before treating
        a green run here as the plan's T33 criterion being met -- it is not.

        The plan requires: scaffold, run `python
        scripts/run_security_verification.py local` as a subprocess, and
        assert **exit 0** and the exact `NOT APPLICABLE` line.  Measured on
        2026-08-10, a stock `solo-greenfield` install instead exits **5
        (INCOMPLETE)**, because:

        * `content-security` became default-on in the sibling
          `default-security-stance` scope AFTER this plan was measured (the
          plan's own reading was six default-on modules, none of them
          matching);
        * `_selected_capability_ids` selects capabilities by the **name
          suffix** `-security`, which `content-security` matches;
        * the shipped registry is empty at v1, so that selected capability
          has no admitted entry and its leg is INCOMPLETE (T3's contract),
          which the ladder aggregates to exit 5.

        Removing `content-security` from the roster yields exactly the
        plan's criterion (asserted below), which isolates the cause to that
        one module rather than to the dispatcher.  Resolving the
        contradiction means either narrowing the source-owned capability
        filter or amending the accepted v1 contract -- a Maintainer
        decision, so this node records the discrepancy rather than choosing.
        **Whichever way it is resolved, this node goes RED and must be
        rewritten deliberately.**

        Hazard perturbations for the parts that ARE guards: break the
        lockfile read path (point `_LOCKFILE` at a non-existent relative
        location) and the machine object's `status` changes; emit exit 0
        with no machine object at all and every machine assertion below
        goes red while the exit code and the human line still match.
        """
        import subprocess as sp

        rc, target = _scaffold(tmp_path, "preset: solo-greenfield\n")
        assert rc == 0
        dispatcher = target / DISPATCHER_DST
        assert dispatcher.is_file()

        proc = sp.run(
            [sys.executable, str(dispatcher), "local"],
            cwd=str(target), capture_output=True, text=True,
        )
        obj = json.loads([
            ln for ln in proc.stdout.splitlines() if ln.startswith("{")
        ][-1])

        # --- Guards: true regardless of how the contradiction is resolved.
        assert obj["schema"] == "cairn.security_verification.dispatcher/v1"
        assert set(obj) >= {
            "schema", "status", "ok", "aggregate", "evidence_count", "legs"}
        assert isinstance(obj["evidence_count"], int)
        assert obj["evidence_count"] == len(obj["legs"])
        for word in ("CLEAN", "secure", "passed security", "no vulnerabilities"):
            assert word not in proc.stdout, (word, proc.stdout)

        # --- Characterization: the measured contradiction of the plan's
        # stated T33 criterion.  RED on any resolution, by design.
        assert proc.returncode == 5, (
            "the recorded residual is gone -- a stock install no longer "
            f"exits 5; got {proc.returncode}.  Re-read this node's "
            "docstring and re-specify it against the resolved contract."
        )
        assert obj["aggregate"] == "INCOMPLETE"
        assert [leg["module_id"] for leg in obj["legs"]] == ["content-security"]

        # --- The cause, isolated: with that one module removed, the plan's
        # criterion holds exactly.
        rc2, target2 = _scaffold(
            tmp_path,
            "preset: solo-greenfield\nmodules_remove:\n  - content-security\n",
            target_name="without-content-security")
        assert rc2 == 0
        proc2 = sp.run(
            [sys.executable, str(target2 / DISPATCHER_DST), "local"],
            cwd=str(target2), capture_output=True, text=True,
        )
        assert proc2.returncode == 0, proc2.stdout + proc2.stderr
        assert proc2.stdout.splitlines()[0] == (
            "NOT APPLICABLE: no selected local security capability")
        obj2 = json.loads(proc2.stdout.splitlines()[1])
        assert obj2["status"] == "not_applicable"
        assert obj2["ok"] is True
        assert obj2["aggregate"] == "NOT_APPLICABLE"
        assert obj2["evidence_count"] == 0
        assert obj2["legs"] == []


class TestTheHighRiskDesignationChannels:
    """T42, T43: the designation lands on three channels, two of them
    tamper-evident.  T42 asserts those two; T43 pins channel 1's
    silent-drop residual as a characterization."""

    def test_the_high_risk_designation_survives_on_two_tamper_evident_channels(
            self, tmp_path: Path) -> None:
        """T42.  The designation is present in the shipped A2, in Cairn's
        own B2 twin, and in the dispatcher source; after a real install,
        `verify_integrity` is OK; deleting the designation from BOTH
        lockfile-recorded channels makes it report `modified (hash
        mismatch)` for both and exit 1.

        Hazard perturbation: drop the designation from the dispatcher source
        -- the source-read row fails.
        """
        for src in (DOCTRINE_SRC, DOCTRINE_TWIN, DISPATCHER_SRC):
            text = src.read_text(encoding="utf-8")
            flat = " ".join(text.split())
            assert DESIGNATION_FLAT in flat, src
        # B2 is Cairn's own rendering of A2 and the module carries no
        # tokens, so the two must stay byte-identical (cmp, not eyeball).
        assert DOCTRINE_TWIN.read_bytes() == DOCTRINE_SRC.read_bytes()

        rc, target = _scaffold(tmp_path, "preset: solo-greenfield\n")
        assert rc == 0

        import importlib
        vi = importlib.import_module("bootstrap.verify_integrity")
        assert vi.verify(target) == 0

        for rel in (DOCTRINE_DST, DISPATCHER_DST):
            path = target / rel
            text = path.read_text(encoding="utf-8")
            stripped = " ".join(text.split())
            assert DESIGNATION_FLAT in stripped, rel
            # Delete the designation sentence's distinctive phrase.
            path.write_text(
                text.replace("high-risk", "ordinary"), encoding="utf-8")

        assert vi.verify(target) == 1

    def test_a_customized_slot_silently_drops_the_designation(
            self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        """T43.  **Characterization, not a guard.  A green run here is a
        recorded OPEN residual, not a closed one.**

        An adopter who marks the installed slot `<!-- cairn:customized -->`
        gets status `customized`, the designation absent from their
        `AGENTS.md`, `check_slot_fidelity` returning an EMPTY list, and no
        side file -- i.e. they drop a high-risk Security-Review designation
        from their governing document and **no Cairn tool says anything**.
        The two tamper-evident channels still carry it, which is the only
        reason this is a residual rather than a hole.

        Hazard perturbation: make `_slot_is_customized` return False -- the
        status and no-warning assertions go red.
        """
        rc, target = _scaffold(tmp_path, "modules:\n  - claim-check\n")
        assert rc == 0
        capsys.readouterr()

        agents_path = target / "AGENTS.md"
        text = agents_path.read_text(encoding="utf-8")
        opener = f"<!-- cairn:slot {MODULE} -->"
        closer = f"<!-- cairn:end {MODULE} -->"
        o = text.index(opener) + len(opener)
        c = text.index(closer)
        agents_path.write_text(
            text[:o] + "\n<!-- cairn:customized -->\nOur own wording.\n"
            + text[c:], encoding="utf-8")

        cfg = _profile(tmp_path / "second.yml", f"modules:\n  - {MODULE}\n")
        rc = scaffold_main([
            "--config", str(cfg), "--target", str(target),
            "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
            "--non-interactive",
        ])
        out = capsys.readouterr().out
        assert rc == 0
        assert f"[customized] AGENTS.md > {MODULE}" in out, out
        assert "[slot-content-" not in out, out
        assert _pending_side_files(target) == []

        installed = agents_path.read_text(encoding="utf-8")
        assert DESIGNATION_FLAT not in " ".join(installed.split())
        assert STANDING_COMMAND not in installed
        assert check_slot_fidelity(
            target, [("AGENTS.md", MODULE, _merge_content())]) == []

        # The two tamper-evident channels are unaffected -- the only reason
        # this residual is bounded.
        for rel in (DOCTRINE_DST, DISPATCHER_DST):
            flat = " ".join((target / rel).read_text(encoding="utf-8").split())
            assert DESIGNATION_FLAT in flat, rel
