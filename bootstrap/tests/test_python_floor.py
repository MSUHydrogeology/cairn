"""Floor CI check: vermin-based Python minimum-version assertion.

Verifies that the scaffold engine (``bootstrap/_scaffold/``) does not
require a Python version **higher** than the declared supported minimum
(>=3.11).

The measured syntactic floor via ``vermin 1.8.0`` is 3.7; the declared
supported minimum is 3.11 (3.7–3.9 are all EOL; 3.8 reached end-of-life
2024-10, 3.9 in 2025-10).  This test asserts that the detected minimum does
not *exceed* 3.11 — a regression guard that fires if a future engine change
inadvertently raises the floor above the declared support line.

The check skips gracefully when ``vermin`` is not importable or not
on PATH; vermin is a dev/test-only dependency (install via
``pip install -r bootstrap/requirements-dev.txt``).

A container-pinned compile check (compiling the engine inside a
container pinned to exactly Python 3.11) is a noted future enhancement
that provides deeper assurance; the vermin-based check is the v1
mechanism and is sufficient as a regression guard.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_python_floor.py -v
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
ENGINE_DIR = CAIRN_ROOT / "bootstrap" / "_scaffold"

# The declared supported minimum floor — >=3.11: the earliest non-EOL Python
# with meaningful runway (3.8 EOL 2024-10, 3.9 EOL 2025-10, 3.10 EOL ~2026-10).
# The single source of this number is doctrine/runtime-contract.md; keep them
# in lockstep. This is the assertion bound: the detected minimum must be <= this.
DECLARED_FLOOR = (3, 11)


# ---------------------------------------------------------------------------
# Skip guard: vermin may not be installed in all environments.
# ---------------------------------------------------------------------------

def _vermin_cmd() -> list[str] | None:
    """Return the vermin invocation command, or None if vermin is unavailable.

    vermin installs as a standalone executable, not as a ``python -m vermin``
    module. Try the ``vermin`` binary on PATH first; if that fails, try the
    ``vermin`` script next to the current interpreter (common in conda/venv).
    """
    # Try PATH-resolved vermin binary. FileNotFoundError/OSError when vermin
    # is absent must yield a graceful skip (None), not a collection error.
    try:
        result = subprocess.run(
            ["vermin", "--version"],
            capture_output=True,
            timeout=10,
        )
        if result.returncode == 0:
            return ["vermin"]
    except (FileNotFoundError, OSError):
        pass

    # Try interpreter-adjacent script (e.g. conda env bin/vermin)
    import shutil
    interpreter_dir = Path(sys.executable).parent
    candidate = shutil.which("vermin", path=str(interpreter_dir))
    if candidate:
        try:
            result2 = subprocess.run(
                [candidate, "--version"],
                capture_output=True,
                timeout=10,
            )
            if result2.returncode == 0:
                return [candidate]
        except (FileNotFoundError, OSError):
            pass

    return None


def _vermin_available() -> bool:
    """Return True if a usable vermin executable is found."""
    return _vermin_cmd() is not None


_SKIP_REASON = (
    "vermin is not installed; install dev dependencies with "
    "'pip install -r bootstrap/requirements-dev.txt' to run this check"
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run_vermin(target: Path) -> tuple[int, int] | None:
    """Run vermin over *target* and return the detected (major, minor) floor.

    Returns ``None`` if vermin cannot parse a floor (unexpected output).
    The ``--backport dataclasses,typing`` flags account for the engine's
    use of ``dataclasses`` and ``typing`` (available as stdlib since 3.7),
    which vermin may otherwise flag as 3.7+ features.

    Note: vermin is a standalone CLI executable, not a ``python -m`` module.
    """
    base_cmd = _vermin_cmd()
    if base_cmd is None:
        return None
    # --eval-annotations is intentionally OMITTED: every engine module uses
    # `from __future__ import annotations`, so annotations are string-form at
    # runtime and 3.9-form annotation syntax is not a runtime requirement.
    # Adding the flag would wrongly raise the measured floor 3.7 -> 3.9.
    cmd = base_cmd + [
        "--backport", "dataclasses",
        "--backport", "typing",
        str(target),
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=60,
    )
    # vermin outputs lines like:
    #   Minimum required versions: 3.7
    #   Incompatible versions:     2.x
    # Combine stdout + stderr since tips go to stdout and the result line
    # may appear in either stream depending on version.
    output = result.stdout + result.stderr
    for line in output.splitlines():
        if line.startswith("Minimum required versions:"):
            version_str = line.split(":", 1)[1].strip()
            # version_str is "3.7" or "~3.7" (no-min) etc.
            version_str = version_str.lstrip("~").strip()
            try:
                parts = version_str.split(".")
                return (int(parts[0]), int(parts[1]))
            except (IndexError, ValueError):
                return None
    return None


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestPythonFloor:
    @pytest.mark.skipif(not _vermin_available(), reason=_SKIP_REASON)
    def test_engine_floor_does_not_exceed_declared_minimum(self) -> None:
        """The scaffold engine's detected Python floor must not exceed 3.11.

        This is a regression guard: if a future change raises the engine's
        minimum requirement above the declared >=3.11 floor, this test fails
        and the floor declaration in ``doctrine/runtime-contract.md`` must
        be updated intentionally.

        Pass condition: detected_floor <= DECLARED_FLOOR (i.e., <=3.11).
        """
        assert ENGINE_DIR.is_dir(), (
            f"Engine directory not found at {ENGINE_DIR}; "
            "run from the cairn repo root"
        )
        detected = _run_vermin(ENGINE_DIR)
        assert detected is not None, (
            "vermin did not produce a parseable 'Minimum required versions' "
            f"line for {ENGINE_DIR}; check vermin output manually"
        )
        detected_major, detected_minor = detected
        declared_major, declared_minor = DECLARED_FLOOR
        assert (detected_major, detected_minor) <= (declared_major, declared_minor), (
            f"Engine floor detected by vermin is {detected_major}.{detected_minor}, "
            f"which EXCEEDS the declared supported minimum "
            f"{declared_major}.{declared_minor}. "
            "Update doctrine/runtime-contract.md if the floor increase is "
            "intentional, or lower the engine's minimum Python requirement."
        )

    @pytest.mark.skipif(not _vermin_available(), reason=_SKIP_REASON)
    def test_engine_floor_is_at_least_3_7(self) -> None:
        """The engine must be compatible with Python 3.7+ (sanity lower bound).

        If vermin reports 2.x compatibility only (or a syntax error), something
        is wrong with the measurement. This test catches that.
        """
        assert ENGINE_DIR.is_dir(), (
            f"Engine directory not found at {ENGINE_DIR}"
        )
        detected = _run_vermin(ENGINE_DIR)
        assert detected is not None, (
            "vermin did not produce a parseable result"
        )
        detected_major, _detected_minor = detected
        assert detected_major >= 3, (
            f"vermin reports Python {detected_major}.x compatibility — "
            "engine must be Python 3+ only"
        )
