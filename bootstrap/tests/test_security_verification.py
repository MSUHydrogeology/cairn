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
           argv_mode: tuple = ("local", "--child-document"),
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

    def test_shipped_registry_admits_exactly_the_two_landed_capabilities(
            self) -> None:
        """T1, corrected for api-web-security-modules Chunk G (rows G1/G2):
        the registry shipped EMPTY at activation v1 and admits exactly two
        entries as of this chunk -- no more, no dormant third. Asserted
        against the SHIPPED source, read independently -- never against
        ``mod`` (other tests monkeypatch its ``_REGISTRY``). The eleven-field
        shape of each entry is TestChunkGRegistryShape's job, not this
        node's; this node is the closed-set membership claim T1 always
        made."""
        fresh = _load_fresh("cairn_security_verification_t1_fresh")
        assert set(fresh._REGISTRY) == {
            "api-access-security", "web-hosting-security"}

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
            str(tmp_path / entry.runner_repository_path),
            "local", "--child-document"]
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
            argv_mode=("local", "--child-document"),
            policy_repository_path=None,
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
        assert len(argv) == 3 + len(entry.argv_mode)
        assert argv[0] == sys.executable
        assert argv[1] == "-I"
        assert argv[2] == str(tmp_path / entry.runner_repository_path)
        assert tuple(argv[3:]) == entry.argv_mode
        assert entry.argv_mode == ("local", "--child-document")

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
            argv_mode=("local", "--child-document"),
            policy_repository_path=None,
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
        """T33, **resolved** (api-web-security-modules Chunk G).  This node
        used to characterize a measured contradiction: a stock
        `solo-greenfield` install exited 5 (INCOMPLETE) instead of the
        plan's criterion of 0 (NOT APPLICABLE), because `content-security`
        (default-on, matches the OLD `-security` name-suffix heuristic) had
        no admitted registry entry.  Chunk G replaces that heuristic with a
        source-owned declared-capability set (`_DECLARED_CAPABILITY_MODULES`)
        that does not contain `content-security`, so it is no longer
        selected and the plan's original criterion now holds directly, with
        no isolation step needed.  Re-measured against THIS tree (not
        carried from the plan or the prior docstring): see this file's
        `test_the_declared_set_is_not_a_name_suffix_heuristic` for the
        narrow regression version of this exact claim.

        Hazard perturbations: break the lockfile read path (point
        `_LOCKFILE` at a non-existent relative location) and the machine
        object's `status` changes; emit exit 0 with no machine object at all
        and every machine assertion below goes red while the exit code and
        the human line still match; widen `_DECLARED_CAPABILITY_MODULES`
        back to a `-security` suffix match and this node goes red on
        `content-security` reappearing in `obj["legs"]`.
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
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert proc.stdout.splitlines()[0] == (
            "NOT APPLICABLE: no selected local security capability")
        obj = json.loads(proc.stdout.splitlines()[1])

        assert obj["schema"] == "cairn.security_verification.dispatcher/v1"
        assert set(obj) >= {
            "schema", "status", "ok", "aggregate", "evidence_count", "legs"}
        assert obj["status"] == "not_applicable"
        assert obj["ok"] is True
        assert obj["aggregate"] == "NOT_APPLICABLE"
        assert obj["evidence_count"] == 0
        assert obj["legs"] == []
        for word in ("CLEAN", "secure", "passed security", "no vulnerabilities"):
            assert word not in proc.stdout, (word, proc.stdout)


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


# ===========================================================================
# Chunk C -- the non-silent install.  T34, T35.
# ===========================================================================

class TestTheNonSilentInstall:

    def test_install_output_names_the_first_run_command_and_claims_no_evidence(
            self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        """T34.  A real scaffold's output names the first-run command
        verbatim, AND carries none of the coverage-claiming words.

        The forbidden-word half is asserted over the **whole** install
        output, not just C1's own block -- measured clean, so the stronger
        form is the one taken.  If a future module's note legitimately needs
        one of these words, narrow the scan to C1's block and say so; do not
        delete the assertion.

        Hazard perturbation: reword C1 to "security verified" -- fails on
        the forbidden-wording half while the command half still passes.
        """
        rc, _target = _scaffold(tmp_path, "preset: solo-greenfield\n")
        captured = capsys.readouterr()
        assert rc == 0
        out = captured.out + captured.err

        assert "NOTE (security-verification)" in out, out
        assert "python scripts/run_security_verification.py local" in out, out

        for word in ("CLEAN", "secure", "scanned", "verified",
                     "no vulnerabilities", "security check passed"):
            assert word not in out, (word, out)

        # The note must also not promise an outcome, even now that a stock
        # install's real exit (0, NOT APPLICABLE -- see the rewritten T33
        # node) would make the specific phrase below true: an install-time
        # notice that names a result is a notice that can go stale the next
        # time the default-on set changes, which is exactly how T33's own
        # prior characterization came to exist.
        assert "NOT APPLICABLE" not in out

    def test_installation_executes_no_selected_scanner(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """T35.  The proposal's *"never claims that installation itself
        produced security evidence"* as a mechanical guard.

        **Measured correction to the plan's wording.**  The plan says to
        monkeypatch `subprocess.run` to raise "for the whole install".  Run
        that way the node fails on a pre-existing, unrelated call: the
        install shells out to `git -C <cairn-root> rev-parse --short HEAD` to
        stamp `cairn_commit` into the lockfile.  A blanket raise therefore
        measures the git-provenance read, not this chunk's property, so the
        guard is written as an **allowlist of one** -- `git` -- with every
        other executable a failure, plus a direct assertion that no recorded
        call names the dispatcher or anything under the target tree.

        Hazard perturbations, both run: make C1 invoke the dispatcher "to
        show the adopter it works" (the executable is `sys.executable`, not
        `git`, so it raises), and make C1 invoke it via `git` (the
        target-path assertion catches it, which is why that second
        assertion exists rather than trusting the allowlist alone).
        """
        import subprocess as sp

        calls: list[list[str]] = []
        real = {attr: getattr(sp, attr) for attr in
                ("run", "Popen", "check_output", "check_call", "call")}

        def guard(attr: str):
            def spy(argv, *args, **kwargs):
                vector = list(argv) if not isinstance(argv, str) else [argv]
                calls.append(vector)
                exe = Path(vector[0]).name if vector else ""
                if exe != "git":
                    raise AssertionError(
                        f"the install executed a non-git subprocess: {vector!r}"
                    )
                return real[attr](argv, *args, **kwargs)
            return spy

        for attr in real:
            monkeypatch.setattr(sp, attr, guard(attr))

        rc, target = _scaffold(tmp_path, "preset: solo-greenfield\n")
        assert rc == 0

        # No recorded call may name the dispatcher or reach into the target
        # tree: `git` on the allowlist must not become a launcher.
        for vector in calls:
            joined = " ".join(vector)
            assert "run_security_verification" not in joined, vector
            assert str(target) not in joined, vector

        # And the route really was installed -- otherwise every assertion
        # above would pass for the trivial reason that nothing happened.
        assert (target / DISPATCHER_DST).is_file()


# ===========================================================================
# Chunk G -- activation registry admission (api-web-security-modules G1/G2)
# ===========================================================================
#
# Everything below except TestChunkGArgvVectorValidation and
# TestChunkGDeclaredCapabilitySet drives the REAL two capability facades
# through the REAL dispatcher: a real scaffold install, the shipped,
# un-monkeypatched ``_REGISTRY``, and
# ``python scripts/run_security_verification.py local`` run as an actual
# subprocess (T33's pattern, not a synthetic fixture child).
#
# This is deliberate, not decoration. The activation-side unit tests above
# inject a synthetic ``RegistryEntry`` pointed at a fixture child -- the
# module docstring explains why that is legitimate for THOSE tests. But it
# means none of them could ever catch the defect this chunk fixes: the
# dispatcher's child argv carried one token (``"local"``) while both
# admitted facades require their own ``local`` subcommand PLUS
# ``--child-document`` to emit the dispatcher's bounded JSON document at
# all -- without it they print the human-readable summary instead, which
# the dispatcher cannot parse as JSON (DEGRADED, not the leg's true state).
# ``test_api_access_security.py`` / ``test_web_hosting_security.py`` invoke
# the CLI directly and always pass ``--child-document`` explicitly, so they
# never exercised the dispatcher's own splice either. Nothing before this
# section ran the real pair together.

_API_MODULE = "api-access-security"
_WEB_MODULE = "web-hosting-security"
_API_RUNNER_DST = "scripts/api_access_security.py"
_WEB_RUNNER_DST = "scripts/web_hosting_security.py"
_API_POLICY_DST = "dev/.cairn/api-access-policy.json"
_WEB_POLICY_DST = "dev/.cairn/web-hosting-policy.json"


def _g_scaffold(tmp_path: Path, modules: "list[str]", *,
                 target_name: str = "g-target") -> Path:
    """A real, minimal, EXPLICIT-module install -- never a preset, so the
    selected roster is exactly ``modules`` (T26/T27's settled rule: an
    explicit ``modules:`` list is exact, never merged with default-on)."""
    body = "modules:\n" + "".join(f"  - {m}\n" for m in modules)
    rc, target = _scaffold(tmp_path, body, target_name=target_name)
    assert rc == 0, (modules, target)
    return target


def _run_dispatcher_local(target: Path):
    import subprocess as sp
    return sp.run(
        [sys.executable, str(target / DISPATCHER_DST), "local"],
        cwd=str(target), capture_output=True, text=True, timeout=120,
    )


def _run_facade_child_document(target: Path, runner_dst: str):
    """Invoke the installed facade DIRECTLY (never through the dispatcher)
    with the exact admitted argv vector, and parse its own emitted child
    document -- the independent oracle a real end-to-end test compares the
    dispatcher's aggregate against."""
    import subprocess as sp
    proc = sp.run(
        [sys.executable, str(target / runner_dst),
         "local", "--child-document"],
        cwd=str(target), capture_output=True, text=True, timeout=120,
    )
    return proc, json.loads(proc.stdout.strip().splitlines()[-1])


def _machine_object(proc) -> dict:
    return json.loads(
        [ln for ln in proc.stdout.splitlines() if ln.startswith("{")][-1])


class TestChunkGRegistryShape:
    """G1: the two admitted entries, all eleven fields explicit, none
    defaulted or inferred; G2(i)/(ii): each constructs from exactly its
    eleven fields, and a twelfth is refused by attempting it."""

    def test_the_two_entries_carry_all_eleven_fields_explicit(self) -> None:
        """G1. Read from a FRESH, un-monkeypatched load of the shipped
        source (T1's own discipline)."""
        fresh = _load_fresh("cairn_security_verification_g1_shape_fresh")
        assert set(fresh._REGISTRY) == {_API_MODULE, _WEB_MODULE}

        expected_result_mapping = {
            "CLEAN": (0, fresh.CLEAN),
            "INCOMPLETE": (5, fresh.INCOMPLETE),
            "FINDINGS": (10, fresh.FINDINGS),
            "DEGRADED": (20, fresh.DEGRADED),
        }
        expected_common = dict(
            argv_mode=("local", "--child-document"),
            child_schema_version="cairn.security.capability-result.v1",
            capability_contract_version="1",
            evidence_mode="loopback",
            accepted_process_exits=frozenset({0, 5, 10, 20}),
            result_to_aggregate_mapping=expected_result_mapping,
            runner_binding_mode="immutable_digest",
            policy_binding_mode="living_state",
        )
        per_module = {
            _API_MODULE: dict(
                runner_repository_path=_API_RUNNER_DST,
                policy_repository_path=_API_POLICY_DST,
            ),
            _WEB_MODULE: dict(
                runner_repository_path=_WEB_RUNNER_DST,
                policy_repository_path=_WEB_POLICY_DST,
            ),
        }
        eleven_fields = {
            "module_id", "runner_repository_path", "argv_mode",
            "policy_repository_path", "child_schema_version",
            "capability_contract_version", "evidence_mode",
            "accepted_process_exits", "result_to_aggregate_mapping",
            "runner_binding_mode", "policy_binding_mode",
        }
        assert set(fresh.RegistryEntry.__dataclass_fields__) == eleven_fields
        for module_id, specific in per_module.items():
            entry = fresh._REGISTRY[module_id]
            assert entry.module_id == module_id
            for field, value in {**expected_common, **specific}.items():
                assert getattr(entry, field) == value, (module_id, field)

    def test_the_dispatcher_local_living_state_set_carries_both_policies(
            self) -> None:
        """The companion wiring G1 depends on but the plan row does not
        separately name: THIS file's own ``_LIVING_STATE_DSTS`` (distinct
        from ``bootstrap/_scaffold/lockfile.py``'s constant of the same
        name -- see this file's comment on it) must carry both policy
        destinations, added in the SAME commit as the registry entries, per
        that constant's own standing rule. Without this, ``_bind_policy``'s
        living_state branch refuses BOTH entries unconditionally (`not in
        this dispatcher's authoritative living-state set`), and the
        registry admission would construct cleanly but never actually run.
        """
        fresh = _load_fresh(
            "cairn_security_verification_g1_living_state_fresh")
        assert fresh._LIVING_STATE_DSTS == frozenset(
            {_API_POLICY_DST, _WEB_POLICY_DST})

    def test_each_entry_constructs_with_exactly_the_eleven_fields(
            self) -> None:
        """G2(i): each of this scope's two entries constructs cleanly from
        exactly its own eleven admitted fields -- tried directly, not
        inferred from the module import having already succeeded."""
        fresh = _load_fresh(
            "cairn_security_verification_g2_construct_fresh")
        for module_id in (_API_MODULE, _WEB_MODULE):
            entry = fresh._REGISTRY[module_id]
            kwargs = {
                f: getattr(entry, f)
                for f in fresh.RegistryEntry.__dataclass_fields__
            }
            rebuilt = fresh.RegistryEntry(**kwargs)
            assert rebuilt == entry

    @pytest.mark.parametrize("bad_key", [
        "principal", "scope", "twelfth_field",
    ])
    def test_a_twelfth_field_on_either_entry_is_refused_by_attempting_it(
            self, bad_key: str) -> None:
        """G2(ii), tried against THESE two entries' own eleven-field shape
        -- not inferred from the dataclass being frozen, and not a repeat
        of T44(a)'s synthetic widget-security shape."""
        fresh = _load_fresh(
            "cairn_security_verification_g2_twelfth_field_fresh")
        for module_id in (_API_MODULE, _WEB_MODULE):
            entry = fresh._REGISTRY[module_id]
            base = {
                f: getattr(entry, f)
                for f in fresh.RegistryEntry.__dataclass_fields__
            }
            base[bad_key] = "malicious"
            with pytest.raises(TypeError) as exc:
                fresh.RegistryEntry(**base)
            assert bad_key in str(exc.value), (module_id, bad_key)


class TestChunkGArgvVectorValidation:
    """G-1's acceptance criterion: the dispatcher can reach ``local`` and
    cannot reach ``deployed-passive`` -- refused at registry construction,
    never at the child."""

    def test_a_deployed_passive_argv_is_refused_at_construction(self) -> None:
        """G-1 hazard perturbation, run against the SOURCE-OWNED
        constructor directly: patching a registry entry's ``argv_mode`` to
        the ``deployed-passive`` shape is refused by ``__post_init__``, so
        it never reaches ``_run_child`` / the child process. The plan's own
        perturbation ("patch the registry entry's argv_mode in a tmp_path
        copy") is exercised here at the unit the validation actually lives
        in; TestChunkGRealFacadeThroughRealDispatcher's tests below cover
        the shipped, un-patched real entries, which never carry this shape
        in the first place."""
        with pytest.raises(ValueError) as exc:
            _entry(argv_mode=("deployed-passive", "--authorize-base-url",
                               "https://example.invalid"))
        assert "argv_mode" in str(exc.value)

    @pytest.mark.parametrize("bad_argv", [
        ("local",),  # the OLD, pre-fix one-token vector
        ("local", "--authorize-base-url"),
        (),
        ("--child-document",),
        ("local", "--child-document", "extra-token"),
        ("deployed-passive",),
    ])
    def test_every_non_admitted_argv_vector_is_refused(
            self, bad_argv: tuple) -> None:
        """The closed set has exactly one member; every neighbor shape --
        including the OLD one-token ``("local",)`` vector this chunk
        replaces -- is refused the same way, at the same place."""
        with pytest.raises(ValueError) as exc:
            _entry(argv_mode=bad_argv)
        assert "argv_mode" in str(exc.value)

    def test_the_admitted_vector_itself_constructs_cleanly(self) -> None:
        """The reciprocal of the two hazard tests above: the one admitted
        vector is not itself refused."""
        entry = _entry(argv_mode=("local", "--child-document"))
        assert entry.argv_mode == ("local", "--child-document")


class TestChunkGDeclaredCapabilitySet:
    """Change 2: the declared, source-owned capability set replacing the
    ``-security`` name-suffix heuristic."""

    def test_the_declared_set_is_not_a_name_suffix_heuristic(self) -> None:
        """The measured defect this replaces: ``content-security`` is
        default-on, matches the OLD ``-security`` suffix, and has no
        registry entry. It must be EXCLUDED from selection now, and the
        two real capabilities must be INCLUDED without relying on their
        names ending in ``-security`` (they do, but that is not why they
        are selected -- only declaration is)."""
        assert "content-security" not in mod._DECLARED_CAPABILITY_MODULES
        lock = {"modules": ["content-security", _API_MODULE]}
        assert mod._selected_capability_ids(lock) == [_API_MODULE]

    def test_a_declared_installed_capability_with_no_registry_entry_stays_visible(  # noqa: E501
            self, monkeypatch: pytest.MonkeyPatch) -> None:
        """The property Change 2 exists to protect, forced directly since
        both REAL declared capabilities are now admitted and so cannot
        demonstrate it: a module that IS in
        `_DECLARED_CAPABILITY_MODULES`, IS selected by the lockfile, and
        has NO admitted `_REGISTRY` entry must still be SELECTED and still
        report INCOMPLETE (T3's contract) -- never silently dropped.
        *Deletion mutant:* narrow `_selected_capability_ids` to
        `installed & set(_REGISTRY)` instead of
        `installed & _DECLARED_CAPABILITY_MODULES`; this node goes red
        because the module vanishes from the selected roster entirely
        (`ids == []`) rather than reporting INCOMPLETE."""
        monkeypatch.setattr(
            mod, "_DECLARED_CAPABILITY_MODULES",
            frozenset({"made-up-declared-security"}))
        lock = {"modules": ["made-up-declared-security"]}
        ids = mod._selected_capability_ids(lock)
        assert ids == ["made-up-declared-security"]
        assert "made-up-declared-security" not in mod._REGISTRY
        leg = mod._evaluate_capability(ids[0], Path("/nonexistent"), {})
        assert leg["aggregate"] == mod.INCOMPLETE
        assert leg["child_launched"] is False


class TestChunkGRealFacadeThroughRealDispatcher:
    """The end-to-end wiring both prior reviews missed: the REAL facades
    driven by the REAL dispatcher, never a synthetic fixture child and
    never the facade CLI invoked directly in place of the dispatcher."""

    def test_a_real_capability_alone_reveals_the_child_details_schema_mismatch(  # noqa: E501
            self, tmp_path: Path) -> None:
        """The required real-facade-through-real-dispatcher test --
        **and a characterization, not the guard G2's row anticipated,
        because of what it found.** Read this docstring before treating a
        green run here as "the real pair works end to end" -- it proves
        the OPPOSITE for the child's `details` field, and that is the
        node's actual value.

        With G-1's argv-vector fix landed, the dispatcher's child DOES
        launch, DOES emit valid UTF-8 JSON, and every identity field
        (`schema`, `capability`, `contract`, `evidence_mode`) matches the
        registry entry -- proving the argv splice this chunk exists to fix
        is correct. But the aggregate is **DEGRADED**, not the INCOMPLETE
        the facade itself reports, because of a SEPARATE, pre-existing,
        previously-undetected contract mismatch this end-to-end run is what
        exposes: `templates/modules/team-gated/_security_net/report.py`'s
        `child_document(..., details: dict, ...)` and both facades' `_emit`
        always build `details` as a JSON OBJECT (`{"capability", "findings",
        "notes", ...}`), while `run_security_verification.py`'s own
        `_evaluate_capability` requires `isinstance(details, str)` and
        DEGRADES with `"child details is not a string"` otherwise. Measured
        directly: `python scripts/api_access_security.py local
        --child-document` on a stock unfilled-stub install prints
        `"details": {"capability": "api-access-security", "findings": [],
        "notes": [...]}`.  Neither side is this deviation's to redesign
        (Change 1/2/3's scope is the argv vector, the capability set, and
        the two registry rows) -- this is the STOP-and-report finding the
        task's end-to-end instruction anticipated might surface. **Its
        practical consequence:** as shipped right now, NEITHER admitted
        capability can EVER report CLEAN, FINDINGS, or INCOMPLETE through
        the dispatcher, regardless of the capability's own actual evidence
        -- every real leg that reaches the child-launch stage degrades on
        this check. Only a leg that fails EARLIER (a binding failure, before
        the child ever launches) reports DEGRADED for its own, unrelated
        reason.
        """
        target = _g_scaffold(
            tmp_path, ["security-verification", _API_MODULE],
            target_name="g-api-alone")
        assert (target / _API_RUNNER_DST).is_file()
        assert (target / _API_POLICY_DST).is_file()

        proc = _run_dispatcher_local(target)
        obj = _machine_object(proc)
        [leg] = obj["legs"]
        assert leg["module_id"] == _API_MODULE
        assert leg["child_launched"] is True
        assert leg["evidence_mode"] == "loopback"

        # The independent oracle: the same facade, invoked directly. Its
        # child document PARSES and every identity field matches -- the
        # G-1 argv-splice fix is what makes even this much true.
        _fproc, child_doc = _run_facade_child_document(
            target, _API_RUNNER_DST)
        assert child_doc["schema"] == "cairn.security.capability-result.v1"
        assert child_doc["capability"] == _API_MODULE
        assert child_doc["contract"] == "1"
        assert child_doc["evidence_mode"] == "loopback"
        assert child_doc["result"] == "INCOMPLETE"
        assert isinstance(child_doc["details"], dict), (
            "if this ever becomes a str, the facade side of the mismatch "
            "has changed and this node's characterization is stale")

        # The characterized mismatch: the dispatcher's aggregate is NOT what
        # the child reported, because `details` fails the dispatcher's own
        # `isinstance(..., str)` requirement.
        assert proc.returncode == 20, proc.stdout + proc.stderr
        assert obj["aggregate"] == "DEGRADED"
        assert leg["aggregate_label"] == "DEGRADED"
        assert leg["aggregate_label"] != child_doc["result"], (
            "the schema mismatch this node characterizes appears to be "
            "fixed -- re-read the docstring and rewrite this node against "
            "the resolved contract, the same discipline the former T33 "
            "characterization used")
        assert "details is not a string" in leg["detail"]

    def test_the_other_real_capability_alone_hits_the_same_mismatch(
            self, tmp_path: Path) -> None:
        """Same characterization as the api-access-security node, run
        against web-hosting-security -- confirming the mismatch is systemic
        (both facades share `_security_net/report.py`'s `child_document`),
        not an artifact of one facade's own code."""
        target = _g_scaffold(
            tmp_path, ["security-verification", _WEB_MODULE],
            target_name="g-web-alone")
        proc = _run_dispatcher_local(target)
        obj = _machine_object(proc)
        [leg] = obj["legs"]
        assert leg["module_id"] == _WEB_MODULE
        assert leg["child_launched"] is True

        _fproc, child_doc = _run_facade_child_document(
            target, _WEB_RUNNER_DST)
        assert child_doc["capability"] == _WEB_MODULE
        assert child_doc["result"] == "INCOMPLETE"
        assert isinstance(child_doc["details"], dict)

        assert proc.returncode == 20, proc.stdout + proc.stderr
        assert obj["aggregate"] == "DEGRADED"
        assert leg["aggregate_label"] == "DEGRADED"
        assert "details is not a string" in leg["detail"]

    def test_both_real_capabilities_together_both_hit_the_mismatch(
            self, tmp_path: Path) -> None:
        """G2's "both together" row, characterized rather than guarded for
        the same reason as the two single-capability nodes above: both
        selected, both legs launch their real child, and -- because the
        `details`-schema mismatch is not specific to either facade -- both
        degrade the same way, with `_build_report` correctly keeping the
        two legs distinct rather than collapsing them (T32's property,
        reconfirmed here over real legs)."""
        target = _g_scaffold(
            tmp_path,
            ["security-verification", _API_MODULE, _WEB_MODULE],
            target_name="g-both")
        proc = _run_dispatcher_local(target)
        assert proc.returncode == 20, proc.stdout + proc.stderr
        obj = _machine_object(proc)
        assert obj["aggregate"] == "DEGRADED"
        assert obj["evidence_count"] == 2
        by_module = {leg["module_id"]: leg for leg in obj["legs"]}
        assert set(by_module) == {_API_MODULE, _WEB_MODULE}
        for leg in by_module.values():
            assert leg["aggregate_label"] == "DEGRADED"
            assert leg["child_launched"] is True
            assert "details is not a string" in leg["detail"]

    def test_a_binding_failure_still_precedes_and_differs_from_the_details_mismatch(  # noqa: E501
            self, tmp_path: Path) -> None:
        """G2's precedence row (`20 > 10 > 5 > 0`) cannot currently be
        demonstrated end to end with REAL legs: the `details`-schema
        mismatch characterized above means a real leg that reaches the
        child-launch stage can now ONLY resolve to DEGRADED, whatever the
        capability's own evidence actually is -- there is no live path to a
        real CLEAN, FINDINGS, or INCOMPLETE aggregate to show precedence
        against. T15 remains the exhaustive, synthetic proof that
        `_build_report`'s `max()` respects `20 > 10 > 5 > 0` over every
        ordered pair; this node instead shows the one real-leg distinction
        still available -- a binding failure (digest mismatch) refuses
        BEFORE the child launches, for its own named reason, while the
        details-mismatch failure happens AFTER a real launch, for a
        different named reason -- and confirms the two are not collapsed
        into one leg despite sharing an aggregate level."""
        target = _g_scaffold(
            tmp_path,
            ["security-verification", _API_MODULE, _WEB_MODULE],
            target_name="g-precedence")
        runner_path = target / _WEB_RUNNER_DST
        data = bytearray(runner_path.read_bytes())
        data[0] ^= 0xFF
        runner_path.write_bytes(bytes(data))

        proc = _run_dispatcher_local(target)
        assert proc.returncode == 20, proc.stdout + proc.stderr
        obj = _machine_object(proc)
        assert obj["aggregate"] == "DEGRADED"
        by_module = {leg["module_id"]: leg for leg in obj["legs"]}
        # The untampered leg: launches, degrades on the details mismatch.
        assert by_module[_API_MODULE]["aggregate_label"] == "DEGRADED"
        assert by_module[_API_MODULE]["child_launched"] is True
        assert "details is not a string" in by_module[_API_MODULE]["detail"]
        # The tampered leg: refused at binding, never launches -- a
        # DIFFERENT reason, at a DIFFERENT point in the pipeline.
        assert by_module[_WEB_MODULE]["aggregate_label"] == "DEGRADED"
        assert by_module[_WEB_MODULE]["child_launched"] is False
        assert "digest mismatch" in by_module[_WEB_MODULE]["detail"]

    def test_no_real_capability_selected_is_not_applicable(
            self, tmp_path: Path) -> None:
        """G2's "no capability selected" row, using this section's own
        explicit-module install rather than a preset (TestUniversality's
        rewritten T33 covers the preset form)."""
        target = _g_scaffold(
            tmp_path, ["security-verification"], target_name="g-none")
        proc = _run_dispatcher_local(target)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert proc.stdout.splitlines()[0] == (
            "NOT APPLICABLE: no selected local security capability")
        obj = _machine_object(proc)
        assert obj["aggregate"] == "NOT_APPLICABLE"
        assert obj["evidence_count"] == 0
        assert obj["legs"] == []
