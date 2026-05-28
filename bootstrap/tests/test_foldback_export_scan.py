"""Fixture-test coverage for the foldback_export_scan scanner.

The five mechanical no-export classes get one fixture each;
the test asserts (a) the gate exits non-zero on each leak shape
and (b) the finding's detector class matches the expected class.
Plus: clean-draft smoke (exit 0); RFC 5737 documentation-IP
allowlist (does NOT trigger the IP detector); missing denylist
file (proprietary-token detector silent; other four still run).

The fixture-draft tests pin the scanner against silent regression
across the five classes the active-surfacing protocol promises to
gate; the documentation-IP test pins the false-positive guard
against drift; the missing-denylist test pins the four-detector
fallback behavior.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
SCANNER_SRC = (
    CAIRN_ROOT / "templates" / "modules" / "default-on" / "foldback_export_scan.py"
)

pytestmark = pytest.mark.skipif(
    not SCANNER_SRC.exists(),
    reason="foldback_export_scan.py not available",
)


def _load_scanner(name: str = "_foldback_export_scan_under_test") -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, SCANNER_SRC)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def fes() -> ModuleType:
    return _load_scanner()


def _write_draft(tmp_path: Path, body: str, name: str = "draft.md") -> Path:
    p = tmp_path / name
    p.write_text(body, encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# Five mechanical class fixture-tests
# ---------------------------------------------------------------------------


class TestCredentialClass:
    """Fixture for the credential-like-assignment detector."""

    def test_password_assignment_flags(self, fes, tmp_path):
        d = _write_draft(tmp_path, 'password = "super-secret-token"\n')
        findings = fes.scan_file(d, denylist=[])
        assert any(f.detector == "credentials" for f in findings), (
            f"credentials detector silent on `password = \"...\"`: {findings}"
        )

    def test_api_key_assignment_flags(self, fes, tmp_path):
        d = _write_draft(tmp_path, 'api_key = "abc123def456ghi789"\n')
        findings = fes.scan_file(d, denylist=[])
        assert any(f.detector == "credentials" for f in findings), (
            f"credentials detector silent on `api_key = \"...\"`: {findings}"
        )

    def test_bearer_token_flags(self, fes, tmp_path):
        d = _write_draft(tmp_path, 'AUTH_TOKEN=eyJhbGciOiJIUzI1NiJ9.payload.sig\n')
        findings = fes.scan_file(d, denylist=[])
        assert any(f.detector == "credentials" for f in findings), (
            f"credentials detector silent on AUTH_TOKEN=...: {findings}"
        )


class TestPrivatePathClass:
    """Fixture for the user-scoped-absolute-path detector."""

    def test_posix_user_home_flags(self, fes, tmp_path):
        d = _write_draft(tmp_path, "See /Users/alice/projects/secret.md.\n")
        findings = fes.scan_file(d, denylist=[])
        assert any(f.detector == "private-path" for f in findings), (
            f"private-path detector silent on /Users/alice/...: {findings}"
        )

    def test_posix_home_dir_flags(self, fes, tmp_path):
        d = _write_draft(tmp_path, "Path: /home/bob/data/internal.csv\n")
        findings = fes.scan_file(d, denylist=[])
        assert any(f.detector == "private-path" for f in findings), (
            f"private-path detector silent on /home/bob/...: {findings}"
        )

    def test_private_dir_flags(self, fes, tmp_path):
        d = _write_draft(tmp_path, "Cached at /private/var/folders/scratch.\n")
        findings = fes.scan_file(d, denylist=[])
        assert any(f.detector == "private-path" for f in findings)

    def test_windows_user_home_flags(self, fes, tmp_path):
        d = _write_draft(tmp_path, "Path: C:\\Users\\Charlie\\Documents\\secret.docx\n")
        findings = fes.scan_file(d, denylist=[])
        assert any(f.detector == "private-path" for f in findings), (
            f"private-path detector silent on Windows user home: {findings}"
        )


class TestIPAddressClass:
    """Fixture for the IPv4 + IPv6 leak detector.

    Per Anthony's plan-review directive: BOTH deployment-internal IPs
    AND remote-repo IPs are bright-line no-export.
    """

    def test_internal_ipv4_flags(self, fes, tmp_path):
        # RFC 1918 internal -- deployment-internal shape.
        d = _write_draft(tmp_path, "Internal server at 10.0.0.5.\n")
        findings = fes.scan_file(d, denylist=[])
        assert any(f.detector == "ip-address" for f in findings), (
            f"ip-address detector silent on RFC 1918 (10.0.0.5): {findings}"
        )

    def test_public_ipv4_flags(self, fes, tmp_path):
        # Public / remote-repo shape -- also flagged per the maintainer
        # bright-line directive (deployment-internal AND remote-repo).
        d = _write_draft(tmp_path, "Remote repo at 198.184.7.42 (made up).\n")
        findings = fes.scan_file(d, denylist=[])
        assert any(f.detector == "ip-address" for f in findings), (
            f"ip-address detector silent on a public IP: {findings}"
        )

    def test_ipv6_flags(self, fes, tmp_path):
        d = _write_draft(tmp_path, "IPv6: 2607:f8b0:4005:80c::200e.\n")
        findings = fes.scan_file(d, denylist=[])
        assert any(f.detector == "ip-address" for f in findings), (
            f"ip-address detector silent on IPv6: {findings}"
        )

    def test_documentation_ipv4_does_NOT_flag(self, fes, tmp_path):
        # RFC 5737 documentation IPs must NOT trigger -- they're the
        # legitimate "example" allowlist the scanner has to recognize
        # so adopter docs can cite IPs without false alarms.
        for doc_ip in ("192.0.2.1", "198.51.100.42", "203.0.113.7"):
            d = _write_draft(tmp_path, f"Example IP: {doc_ip}.\n", name=f"d-{doc_ip}.md")
            findings = fes.scan_file(d, denylist=[])
            ip_finds = [f for f in findings if f.detector == "ip-address"]
            assert ip_finds == [], (
                f"RFC 5737 documentation IP {doc_ip} false-positive: "
                f"{ip_finds}"
            )

    def test_documentation_ipv6_does_NOT_flag(self, fes, tmp_path):
        # RFC 3849 IPv6 doc-block: 2001:db8::/32.
        d = _write_draft(tmp_path, "Example v6: 2001:db8::1.\n")
        findings = fes.scan_file(d, denylist=[])
        ip_finds = [f for f in findings if f.detector == "ip-address"]
        assert ip_finds == [], (
            f"RFC 3849 documentation IPv6 false-positive: {ip_finds}"
        )


class TestInternalHostnameClass:
    """Fixture for the .local / .internal / .lan suffix detector."""

    def test_dot_local_flags(self, fes, tmp_path):
        d = _write_draft(tmp_path, "Hostname: workstation.local.\n")
        findings = fes.scan_file(d, denylist=[])
        assert any(f.detector == "internal-hostname" for f in findings)

    def test_dot_internal_flags(self, fes, tmp_path):
        d = _write_draft(tmp_path, "Service at api.internal.\n")
        findings = fes.scan_file(d, denylist=[])
        assert any(f.detector == "internal-hostname" for f in findings)

    def test_dot_corp_flags(self, fes, tmp_path):
        d = _write_draft(tmp_path, "Build server: builds.corp.\n")
        findings = fes.scan_file(d, denylist=[])
        assert any(f.detector == "internal-hostname" for f in findings)


class TestProprietaryTokenClass:
    """Fixture for the adopter-configurable proprietary-token detector."""

    def test_denylisted_token_flags(self, fes, tmp_path):
        d = _write_draft(tmp_path, "Client name: AcmeCorp signed off.\n")
        findings = fes.scan_file(d, denylist=["AcmeCorp"])
        assert any(
            f.detector == "proprietary-token" and "AcmeCorp" in f.message
            for f in findings
        ), f"proprietary-token detector silent on `AcmeCorp`: {findings}"

    def test_denylist_is_case_sensitive(self, fes, tmp_path):
        d = _write_draft(tmp_path, "we use acmecorp tools (lowercase).\n")
        findings = fes.scan_file(d, denylist=["AcmeCorp"])
        # Case-sensitive: `acmecorp` should NOT match `AcmeCorp` in the
        # denylist (the adopter enumerates the specific casing).
        assert not any(
            f.detector == "proprietary-token" for f in findings
        ), (
            "proprietary-token matched case-insensitively (expected "
            "case-sensitive)"
        )

    def test_denylist_is_word_boundary(self, fes, tmp_path):
        # Inner substring should NOT match -- `Acme` as a denylist entry
        # should NOT flag `AcmeOff` or `AcmeAcademy`.
        d = _write_draft(tmp_path, "AcmeAcademy is an unrelated entity.\n")
        findings = fes.scan_file(d, denylist=["Acme"])
        assert not any(
            f.detector == "proprietary-token" for f in findings
        ), f"proprietary-token matched inner substring: {findings}"


# ---------------------------------------------------------------------------
# Smoke tests
# ---------------------------------------------------------------------------


class TestSmokes:
    def test_clean_draft_exits_zero(self, fes, tmp_path):
        d = _write_draft(tmp_path, "# A clean draft\n\nNo leaks here.\n")
        findings = fes.scan_file(d, denylist=[])
        assert findings == [], f"clean draft surfaced findings: {findings}"

    def test_main_clean_returns_zero(self, fes, tmp_path):
        d = _write_draft(tmp_path, "# Clean.\n")
        # Use an explicit empty allowlist file so the default path
        # (which may exist in CWD) is not picked up.
        empty_allow = tmp_path / "empty_allowlist.txt"
        empty_allow.write_text("")
        rc = fes.main([str(d), "--allowlist", str(empty_allow)])
        assert rc == 0

    def test_main_leak_returns_nonzero(self, fes, tmp_path):
        d = _write_draft(tmp_path, 'password = "super-secret-token"\n')
        empty_allow = tmp_path / "empty_allowlist.txt"
        empty_allow.write_text("")
        rc = fes.main([str(d), "--allowlist", str(empty_allow)])
        assert rc == 1

    def test_main_missing_file_returns_2(self, fes, tmp_path):
        rc = fes.main([str(tmp_path / "does-not-exist.md")])
        assert rc == 2


class TestDenylistFileHandling:
    def test_missing_denylist_silent_other_detectors_run(
        self, fes, tmp_path,
    ):
        # When the denylist file does not exist, the proprietary-token
        # detector goes silent.  The other four detectors must still
        # run (the scanner is not gated on the allowlist's presence).
        d = _write_draft(
            tmp_path,
            'password = "leaked"\n'
            '/Users/dave/leak\n'
            '10.0.0.1\n'
            'host.local\n',
        )
        denylist = fes.load_denylist(tmp_path / "missing.txt")
        assert denylist == []
        findings = fes.scan_file(d, denylist=denylist)
        detectors = {f.detector for f in findings}
        # Four other classes still fire.
        assert "credentials" in detectors
        assert "private-path" in detectors
        assert "ip-address" in detectors
        assert "internal-hostname" in detectors
        # Proprietary-token silent (no list to match against).
        assert "proprietary-token" not in detectors

    def test_denylist_skips_blank_and_comment_lines(self, fes, tmp_path):
        denyfile = tmp_path / "denylist.txt"
        denyfile.write_text(
            "# This is a comment\n"
            "\n"
            "AcmeCorp\n"
            "    \n"  # whitespace-only
            "# Another comment\n"
            "ProjectBlue\n"
        )
        denylist = fes.load_denylist(denyfile)
        assert denylist == ["AcmeCorp", "ProjectBlue"]
