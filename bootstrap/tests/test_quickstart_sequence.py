"""
2-layer regression test for ``docs/quickstart.md``.

The quickstart is the adopter-friction package's load-bearing
first-contact surface (modflow_tools plan stem:
``2026-05-28-claude-cairn-adopter-friction-package``, Chunk 3).
A page that prescribes shell commands and lifecycle steps drifts
silently across releases unless tested.  This module is the
regression gate.

**Two layers, separately named** (per accepted Plan-review
finding):

* **Layer A (deterministic shell coverage)**: drives the literal
  shell commands in Steps 1-3 of the quickstart against a temp
  repo and asserts the expected file tree after each step.
  This is the shell + scaffold portion that adopter behaviour
  faithfully mirrors.

* **Layer B (lifecycle-shape coverage via scripted surrogate)**:
  scripts the file operations the agent + maintainer would
  perform in Steps 4-6 (programmatic proposal-open, a fresh-session
  Review append, a quoted Decision, ``git mv`` to archive,
  ``CHANGELOG.md`` line).
  This is **explicitly NOT a literal AI-agent execution** --
  the test cannot faithfully exercise the prompt-mediated path.
  The module-level constant
  ``LAYER_B_IS_LIFECYCLE_SHAPE_ONLY = True`` documents the
  boundary: passing Layer B proves the lifecycle's *shape* is
  achievable on the installed tree, not that an agent reading
  the quickstart prose will produce the same shape.  The
  literal-pilot evidence (modflow_tools plan Chunk 4) is the
  only evidence the prompt-mediated path works for an adopter.

Promises:
- The --summary preview names the solo-greenfield preset and its default-on
  modules, and writes no files.
- A solo-greenfield install writes the kernel files, the default-on module docs
  and tool scripts, a lockfile and the changelog.
- The module count and unfilled-slot count that docs/quickstart.md states match
  what a solo-greenfield install reports.
- The install commit the quickstart documents includes CHANGELOG.md.

Run from the cairn repo root::

    python -m pytest bootstrap/tests/test_quickstart_sequence.py
"""

from __future__ import annotations

import re
import shlex
import subprocess
import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
PROFILES_DIR = CAIRN_ROOT / "bootstrap" / "profiles"
SCAFFOLD = CAIRN_ROOT / "bootstrap" / "scaffold.py"
SOLO_GREENFIELD_YAML = PROFILES_DIR / "solo-greenfield.yml"

# Sentinel constant.  Documents that Layer B is lifecycle-shape
# coverage, not a literal AI-agent execution -- the test cannot
# faithfully exercise the prompt-mediated path the quickstart
# documents.  A scripted surrogate creates the proposal, appends
# the Review and the Decision, moves the proposal to archive, and adds the
# CHANGELOG line; the resulting tree shape matches what the
# quickstart describes, but no AI agent or maintainer was
# involved in producing it.
LAYER_B_IS_LIFECYCLE_SHAPE_ONLY = True


def _run_git(*args: str, cwd: Path) -> None:
    """Run a git command in ``cwd``, asserting it succeeded."""
    result = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, (
        f"git {' '.join(args)} in {cwd} exited {result.returncode}; "
        f"stderr:\n{result.stderr}"
    )


@pytest.fixture
def disposable_repo(tmp_path: Path) -> Path:
    """A fresh disposable repo mirroring Step 1 of the quickstart:
    git init + README.md + initial commit."""
    repo = tmp_path / "cairn-quickstart-sim"
    repo.mkdir()
    _run_git("init", "-q", cwd=repo)
    # The init commit uses a deterministic author so the test does
    # not depend on the running user's git config.
    _run_git("config", "user.email", "test@example.invalid", cwd=repo)
    _run_git("config", "user.name", "Test User", cwd=repo)
    (repo / "README.md").write_text("# quickstart\n")
    _run_git("add", "README.md", cwd=repo)
    _run_git("commit", "-q", "-m", "init", cwd=repo)
    return repo


# ---------------------------------------------------------------------------
# Layer A -- deterministic shell coverage (Steps 1-3)
# ---------------------------------------------------------------------------


class TestLayerAStepsOneThroughThree:
    """Drives the literal shell commands in Steps 1-3 and asserts
    the post-step file tree.  This layer faithfully mirrors what
    an adopter sees when they copy-paste."""


    def test_step3_summary_previews_without_installing(
        self, disposable_repo: Path
    ) -> None:
        """Step 3's --summary invocation prints the profile + roster
        and exits without writing files."""
        repo = disposable_repo
        (repo / "profile.yml").write_text(SOLO_GREENFIELD_YAML.read_text())
        before = set(p.name for p in repo.iterdir())
        result = subprocess.run(
            [
                sys.executable,
                str(SCAFFOLD),
                "--config",
                str(repo / "profile.yml"),
                "--target",
                str(repo),
                "--summary",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        after = set(p.name for p in repo.iterdir())
        assert before == after, (
            f"--summary should not write files; tree changed: {after - before}"
        )
        # The preview prints the preset's identity + the default-on roster.
        assert "Preset: solo-greenfield" in result.stdout
        for default_on in ("reflections", "claim-check"):
            assert default_on in result.stdout, (
                f"--summary output should include {default_on!r}; got:\n{result.stdout}"
            )

    def test_step3_install_writes_expected_kernel_and_modules(
        self, disposable_repo: Path
    ) -> None:
        """Step 3's install (no --summary) writes the kernel
        files, the default-on module docs, and the default-on tool
        scripts."""
        repo = disposable_repo
        (repo / "profile.yml").write_text(SOLO_GREENFIELD_YAML.read_text())
        result = subprocess.run(
            [
                sys.executable,
                str(SCAFFOLD),
                "--config",
                str(repo / "profile.yml"),
                "--target",
                str(repo),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, (
            f"scaffold install exited {result.returncode}; stderr:\n{result.stderr}"
        )
        # The quickstart's "you should see" list maps to these paths.
        expected_paths = [
            "AGENTS.md",
            "VENDOR.md",
            "dev/README.md",
            "dev/PLANNING.md",
            "dev/agent_collaboration.md",
            "dev/proposals/_template.md",
            "dev/plans/_template.md",
            "dev/modules/reflections.md",
            "dev/modules/claim-check.md",
            "scripts/claim_check.py",
            "dev/.cairn/cairn-lock.yml",
            "CHANGELOG.md",
        ]
        for relative in expected_paths:
            assert (repo / relative).exists(), (
                f"quickstart Step 3 should install {relative}; not present after run"
            )
        assert "## Unreleased" in (repo / "CHANGELOG.md").read_text()
        assert not (repo / "dev" / "collaboration_agreement.md").exists()
        # Drift-gate -- close the prose<->runtime loop (the 2026-06-12
        # adopter-friction audit). NO hardcoded count lives here: the
        # quickstart's two load-bearing numbers are read FROM the doc and
        # compared to what the live solo-greenfield install actually
        # produced, so the gate fires the moment the default-on set (and
        # thus the counts) drifts -- instead of an adopter discovering the
        # mismatch at Step 3.
        quickstart = (CAIRN_ROOT / "docs" / "quickstart.md").read_text()
        # The `-> modules:` info line goes to stderr; the slot tally to
        # stdout -- search the combined stream for both.
        combined = result.stdout + result.stderr

        # Module count: the resolved roster the scaffold logged.
        live_mods = re.search(r"-> modules: ([^\n.]+)", combined)
        assert live_mods, f"scaffold did not log a resolved roster:\n{combined}"
        live_module_count = len(
            [m for m in live_mods.group(1).split(",") if m.strip()]
        )
        prose_mods = re.search(r"\*\*(\d+)\*\* modules listed", quickstart)
        assert prose_mods, (
            "docs/quickstart.md must state '**N** modules listed' for solo-greenfield"
        )
        assert int(prose_mods.group(1)) == live_module_count, (
            f"docs/quickstart.md says '**{prose_mods.group(1)}** modules' but the live "
            f"solo-greenfield install resolves {live_module_count} "
            f"({live_mods.group(1).strip()}) -- refresh the quickstart prose."
        )

        # Slot count: what the scaffold actually emitted.
        live_slots = re.search(
            r"Block slots requiring agent attention \((\d+)\)", combined
        )
        assert live_slots, f"scaffold did not report a slot count:\n{combined}"
        prose_slots = re.search(r"\*\*(\d+) unfilled block slots\*\*", quickstart)
        assert prose_slots, "docs/quickstart.md must state '**N unfilled block slots**'"
        assert prose_slots.group(1) == live_slots.group(1), (
            f"docs/quickstart.md says '{prose_slots.group(1)} unfilled block slots' "
            f"but the live install reports {live_slots.group(1)} -- refresh the "
            f"quickstart prose to match the scaffold."
        )

        # Execute the literal terminal install-commit commands from the
        # quickstart and verify the generated changelog is in that commit.
        commit_commands = re.search(
            r"Then commit the install;.*?```text\n"
            r"(?P<add>git add [^\n]+)\n(?P<commit>git commit [^\n]+)\n```",
            quickstart,
            re.DOTALL,
        )
        assert commit_commands, "quickstart must show terminal install-commit commands"
        _run_git(*shlex.split(commit_commands.group("add"))[1:], cwd=repo)
        _run_git(*shlex.split(commit_commands.group("commit"))[1:], cwd=repo)
        committed_paths = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", "HEAD"],
            cwd=repo,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()
        assert "CHANGELOG.md" in committed_paths, (
            "quickstart's documented install commit must include CHANGELOG.md"
        )


# ---------------------------------------------------------------------------
# Layer B -- lifecycle-shape coverage via scripted surrogate (Steps 4-6)
# ---------------------------------------------------------------------------


_PROPOSAL_STEM = "2026-05-28-test-readme-tagline"
_PROPOSAL_TEXT = (
    "# README tagline\n\n"
    "**Author**: Agent\n"
    "**Status**: awaiting-review\n"
    "**Opened**: 2026-05-28\n\n"
    "## Proposal\n\nAdd a one-line project tagline to README.md.\n"
)
_REVIEW_TEXT = (
    "\n## Review -- Reviewer -- 2026-05-28\n\n"
    "**Tier**: usual\n**Findings**: none\n**Verdict**: ACCEPT\n"
)
_DECISION_TEXT = (
    "\n## Decision -- Maintainer -- 2026-05-28\n\n"
    "**ACCEPTED.** The Maintainer's authorization, quoted verbatim:\n\n"
    '> "Accepted as a light example.  Implement the tagline, run the applicable final check, record its results and omissions in the proposal, then archive it in a later commit."\n'
)


def _set_status(path: Path, status: str) -> None:
    text = path.read_text()
    current = re.search(r"\*\*Status\*\*: [a-z-]+", text)
    assert current, f"no Status line in {path}"
    path.write_text(text.replace(current.group(0), f"**Status**: {status}", 1))


def _open_review_decide(repo: Path) -> Path:
    """Steps 4-5a as the quickstart prescribes them: open the proposal,
    a fresh session appends its Review, then the Maintainer's quoted
    Decision, each in its own commit.  Returns the proposal path."""
    proposal_path = repo / "dev" / "proposals" / f"{_PROPOSAL_STEM}.md"
    rel = str(proposal_path.relative_to(repo))
    proposal_path.write_text(_PROPOSAL_TEXT)
    _run_git("add", rel, cwd=repo)
    _run_git("commit", "-q", "-m", "Open proposal: README tagline", cwd=repo)
    with proposal_path.open("a") as fh:
        fh.write(_REVIEW_TEXT)
    _set_status(proposal_path, "awaiting-decision")
    _run_git("commit", "-q", "-m", "Review: README tagline", rel, cwd=repo)
    with proposal_path.open("a") as fh:
        fh.write(_DECISION_TEXT)
    _set_status(proposal_path, "accepted")
    _run_git("commit", "-q", "-m", "Decision: accept README tagline", rel, cwd=repo)
    return proposal_path


def _implement_verify_archive(repo: Path, proposal_path: Path, tagline: str) -> Path:
    """Implement, record the final check, then archive in later commits."""
    readme = repo / "README.md"
    readme.write_text(readme.read_text() + f"\n> {tagline}\n")
    changelog = repo / "CHANGELOG.md"
    changelog.write_text(
        changelog.read_text().replace(
            "## Unreleased\n",
            "## Unreleased\n\n### Added\n\n- README tagline.\n",
        )
    )
    _run_git(
        "commit", "-m", "Implement README tagline",
        str(readme.relative_to(repo)), str(changelog.relative_to(repo)), cwd=repo,
    )

    verification = (
        "\n## Implementation verification -- Agent -- 2026-05-28\n\n"
        "**Mode**: bounded\n"
        "**Command**: applicable final integration selection\n"
        "**Result**: pass (simulated lifecycle record)\n"
        "**Omissions**: none in this small example\n"
    )
    with proposal_path.open("a") as fh:
        fh.write(verification)
    rel_proposal = str(proposal_path.relative_to(repo))
    _run_git(
        "commit", "-m", "Record final verification", rel_proposal, cwd=repo,
    )

    archive_path = proposal_path.parent / "archive" / proposal_path.name
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    _run_git(
        "mv", rel_proposal, str(archive_path.relative_to(repo)), cwd=repo,
    )
    _run_git(
        "commit", "-m", "Archive README tagline proposal",
        str(archive_path.relative_to(repo)), rel_proposal, cwd=repo,
    )
    return archive_path


def _assert_verification_order(repo: Path, proposal_path: Path) -> None:
    """Reject absent or premature verification evidence in constructed history."""
    result = subprocess.run(
        ["git", "log", "--format=%H%x09%s"], cwd=repo,
        capture_output=True, text=True, check=True,
    )
    entries = [line.split("\t", 1) for line in result.stdout.splitlines()]
    subjects = [subject for _, subject in entries]
    expected = [
        "Archive README tagline proposal",
        "Record final verification",
        "Implement README tagline",
        "Decision: accept README tagline",
        "Review: README tagline",
        "Open proposal: README tagline",
        "Install Cairn kernel",
        "init",
    ]
    assert subjects == expected, (
        "quickstart must record verification after implementation and before "
        f"archive; got commit subjects: {subjects}"
    )
    verification_sha = entries[1][0]
    rel_proposal = str(proposal_path.relative_to(repo))
    recorded = subprocess.run(
        ["git", "show", f"{verification_sha}:{rel_proposal}"], cwd=repo,
        capture_output=True, text=True, check=True,
    ).stdout
    assert "## Implementation verification -- Agent -- 2026-05-28" in recorded
    assert "**Mode**: bounded" in recorded
    for field in ("Command", "Result", "Omissions"):
        assert re.search(rf"^\*\*{field}\*\*: \S.*$", recorded, re.MULTILINE), (
            f"verification record needs a non-empty {field} field"
        )
    implementation_sha = entries[2][0]
    before_verification = subprocess.run(
        ["git", "show", f"{implementation_sha}:{rel_proposal}"], cwd=repo,
        capture_output=True, text=True, check=True,
    ).stdout
    assert "## Implementation verification" not in before_verification, (
        "verification must be committed after the implementation check"
    )


class TestLayerBLifecycleShapeOnly:
    """Layer B uses a scripted surrogate to perform the file
    operations the agent + maintainer would do in Steps 4-6.
    This is **NOT a literal AI-agent execution** -- see the
    module docstring and the ``LAYER_B_IS_LIFECYCLE_SHAPE_ONLY``
    constant.  Passing these tests proves the resulting tree
    shape is achievable, not that an adopter following the
    prompts will produce it."""

    def _install_cairn(self, repo: Path) -> None:
        """Helper: run Layer A's full Step 3 install so Layer B can
        operate on the kernel."""
        (repo / "profile.yml").write_text(SOLO_GREENFIELD_YAML.read_text())
        subprocess.run(
            [
                sys.executable,
                str(SCAFFOLD),
                "--config",
                str(repo / "profile.yml"),
                "--target",
                str(repo),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        # Commit the install per Step 3's "Commit the install" instruction.
        _run_git(
            "add", "AGENTS.md", "VENDOR.md", "dev", "tools", "scripts",
            "CHANGELOG.md", cwd=repo,
        )
        _run_git("commit", "-q", "-m", "Install Cairn kernel", cwd=repo)


    def test_step5_decision_then_implement_and_archive(
        self, disposable_repo: Path
    ) -> None:
        """Step 5 surrogate: commit the fresh-session Review and the
        Maintainer's quoted Decision separately; commit the implementation,
        record its final check in the accepted proposal, then archive that
        proposal in a later commit."""
        repo = disposable_repo
        self._install_cairn(repo)
        # --- Steps 4-5a: open, review, decide ---
        proposals_dir = repo / "dev" / "proposals"
        proposal_path = _open_review_decide(repo)

        # --- Step 5b: implement, check, record, then archive ---
        archive_path = _implement_verify_archive(
            repo, proposal_path, "The disposable quickstart repo."
        )
        _assert_verification_order(repo, proposal_path)
        readme = repo / "README.md"
        changelog = repo / "CHANGELOG.md"

        # --- Assertions: lifecycle shape on disk ---
        # The proposal moved to archive/.
        assert archive_path.exists()
        assert not proposal_path.exists()
        # The Decision section is in the archived proposal.
        archived_text = archive_path.read_text()
        assert "## Review -- Reviewer -- 2026-05-28" in archived_text
        assert "## Decision -- Maintainer -- 2026-05-28" in archived_text
        assert "**Status**: accepted" in archived_text
        assert "## Implementation verification -- Agent -- 2026-05-28" in archived_text
        assert (
            '> "Accepted as a light example.  Implement the tagline, run the '
            'applicable final check, record its results and omissions in the '
            'proposal, then archive it in a later commit."'
        ) in archived_text
        # The CHANGELOG carries the new line.
        assert "README tagline" in changelog.read_text()
        # The README carries the tagline.
        assert "disposable quickstart repo" in readme.read_text()

    def test_step6_git_log_has_lifecycle_boundaries(
        self, disposable_repo: Path
    ) -> None:
        """Step 6 says ``git log --oneline`` shows eight commits
        with clear lifecycle boundaries: init, install, proposal-open,
        review, decision, implementation, verification record and archive.
        This test reaches the same end-state and pins the commit count
        and boundary subjects."""
        repo = disposable_repo
        # Re-use Step 5's setup end-to-end.
        self._install_cairn(repo)
        proposals_dir = repo / "dev" / "proposals"
        proposal_path = _open_review_decide(repo)
        archived_path = _implement_verify_archive(
            repo, proposal_path, "Tagline."
        )
        _assert_verification_order(repo, proposal_path)
        changelog = repo / "CHANGELOG.md"

        # --- Step 6 assertions ---
        result = subprocess.run(
            ["git", "log", "--oneline"],
            cwd=repo, capture_output=True, text=True, check=True,
        )
        lines = result.stdout.strip().splitlines()
        # Eight commits preserve each lifecycle boundary, including the
        # implementation check record and the later archive transition.
        assert len(lines) == 8, (
            f"quickstart Step 6 documents eight commits; got {len(lines)}:\n{result.stdout}"
        )
        subjects = [line.split(" ", 1)[1] for line in lines]
        assert subjects == [
            "Archive README tagline proposal",
            "Record final verification",
            "Implement README tagline",
            "Decision: accept README tagline",
            "Review: README tagline",
            "Open proposal: README tagline",
            "Install Cairn kernel",
            "init",
        ]
        # The proposal is in archive/ (listed in Python, so the check
        # also runs where no `ls` exists).
        archive_names = {p.name for p in (proposals_dir / "archive").iterdir()}
        assert f"{_PROPOSAL_STEM}.md" in archive_names
        assert archived_path.exists()
