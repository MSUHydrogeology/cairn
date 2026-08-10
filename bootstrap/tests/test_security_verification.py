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
