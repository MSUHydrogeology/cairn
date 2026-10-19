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
  perform in Steps 4-6 (programmatic proposal-open, Decision
  append, ``git mv`` to archive, ``CHANGELOG.md`` line).
  This is **explicitly NOT a literal AI-agent execution** --
  the test cannot faithfully exercise the prompt-mediated path.
  The module-level constant
  ``LAYER_B_IS_LIFECYCLE_SHAPE_ONLY = True`` documents the
  boundary: passing Layer B proves the lifecycle's *shape* is
  achievable on the installed tree, not that an agent reading
  the quickstart prose will produce the same shape.  The
  literal-pilot evidence (modflow_tools plan Chunk 4) is the
  only evidence the prompt-mediated path works for an adopter.

Run from the cairn repo root::

    python -m pytest bootstrap/tests/test_quickstart_sequence.py
"""

from __future__ import annotations

import re
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
# the Decision, moves the proposal to archive, and adds the
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
    git init + README.md + CHANGELOG.md stub + initial commit."""
    repo = tmp_path / "cairn-quickstart-sim"
    repo.mkdir()
    _run_git("init", "-q", cwd=repo)
    # The init commit uses a deterministic author so the test does
    # not depend on the running user's git config.
    _run_git("config", "user.email", "test@example.invalid", cwd=repo)
    _run_git("config", "user.name", "Test User", cwd=repo)
    (repo / "README.md").write_text("# quickstart\n")
    (repo / "CHANGELOG.md").write_text("# Changelog\n\n## Unreleased\n")
    _run_git("add", "README.md", "CHANGELOG.md", cwd=repo)
    _run_git("commit", "-q", "-m", "init", cwd=repo)
    return repo


# ---------------------------------------------------------------------------
# Layer A -- deterministic shell coverage (Steps 1-3)
# ---------------------------------------------------------------------------


class TestLayerAStepsOneThroughThree:
    """Drives the literal shell commands in Steps 1-3 and asserts
    the post-step file tree.  This layer faithfully mirrors what
    an adopter sees when they copy-paste."""

    def test_step1_init_produces_readme_and_changelog(
        self, disposable_repo: Path
    ) -> None:
        """Step 1 leaves the target with README.md + CHANGELOG.md
        + one git commit and nothing else."""
        repo = disposable_repo
        # Tracked files after init.
        result = subprocess.run(
            ["git", "ls-files"], cwd=repo, capture_output=True, text=True, check=True
        )
        tracked = set(result.stdout.split())
        assert tracked == {"README.md", "CHANGELOG.md"}, (
            f"after Step 1, tracked files should be README + CHANGELOG; got {tracked}"
        )
        # CHANGELOG carries the Unreleased anchor the quickstart uses.
        assert "## Unreleased" in (repo / "CHANGELOG.md").read_text()

    def test_step2_profile_yml_is_the_solo_greenfield_preset(
        self, disposable_repo: Path
    ) -> None:
        """Step 2 copies bootstrap/profiles/solo-greenfield.yml as
        profile.yml in the target repo."""
        repo = disposable_repo
        # Quickstart Step 2: `cp /path/to/cairn/bootstrap/profiles/solo-greenfield.yml profile.yml`
        (repo / "profile.yml").write_text(SOLO_GREENFIELD_YAML.read_text())
        cfg_text = (repo / "profile.yml").read_text()
        assert "preset: solo-greenfield" in cfg_text, (
            "Step 2 should produce profile.yml with preset: solo-greenfield"
        )

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
            "dev/NEXT_SESSION.md",
            "dev/agent_collaboration.md",
            "dev/proposals/_template.md",
            "dev/plans/_template.md",
            "dev/modules/reflections.md",
            "dev/modules/claim-check.md",
            "scripts/claim_check.py",
            "dev/.cairn/cairn-lock.yml",
        ]
        for relative in expected_paths:
            assert (repo / relative).exists(), (
                f"quickstart Step 3 should install {relative}; not present after run"
            )
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


# ---------------------------------------------------------------------------
# Layer B -- lifecycle-shape coverage via scripted surrogate (Steps 4-6)
# ---------------------------------------------------------------------------


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
            cwd=repo,
        )
        _run_git("commit", "-q", "-m", "Install Cairn kernel", cwd=repo)

    def test_layer_b_constant_is_true(self) -> None:
        """The sentinel is a documented invariant -- the module
        promises Layer B does not exercise the prompt-mediated path.
        This test pins the promise."""
        assert LAYER_B_IS_LIFECYCLE_SHAPE_ONLY is True, (
            "LAYER_B_IS_LIFECYCLE_SHAPE_ONLY must stay True -- Layer B "
            "is lifecycle-shape coverage via scripted surrogate, not a "
            "literal AI-agent execution.  See module docstring."
        )

    def test_step4_open_proposal_under_dev_proposals(
        self, disposable_repo: Path
    ) -> None:
        """Step 4 (surrogate): write a proposal file under
        dev/proposals/ and commit it on its own."""
        repo = disposable_repo
        self._install_cairn(repo)
        proposal_stem = "2026-05-28-test-readme-tagline"
        proposal_path = repo / "dev" / "proposals" / f"{proposal_stem}.md"
        proposal_path.write_text(
            "# README tagline\n\n"
            "**Status**: proposed\n\n"
            "## Proposal\n\nAdd a one-line project tagline to README.md.\n"
        )
        _run_git("add", str(proposal_path.relative_to(repo)), cwd=repo)
        _run_git("commit", "-q", "-m", "Open proposal: README tagline", cwd=repo)
        # Quickstart Step 4 asserts the proposal file lives under
        # dev/proposals/<stem>.md.
        assert proposal_path.exists()
        assert proposal_path.read_text().startswith("# README tagline")

    def test_step5_decision_then_implement_and_archive(
        self, disposable_repo: Path
    ) -> None:
        """Step 5 (surrogate): append the Decision section, commit
        decision; then implement the change, git mv the proposal
        to archive, add the CHANGELOG line, commit as a single
        implementing-and-archiving commit."""
        repo = disposable_repo
        self._install_cairn(repo)
        # --- Step 4 setup (proposal exists) ---
        proposal_stem = "2026-05-28-test-readme-tagline"
        proposals_dir = repo / "dev" / "proposals"
        proposal_path = proposals_dir / f"{proposal_stem}.md"
        proposal_path.write_text(
            "# README tagline\n\n**Status**: proposed\n\n## Proposal\n\nAdd a tagline.\n"
        )
        _run_git("add", str(proposal_path.relative_to(repo)), cwd=repo)
        _run_git("commit", "-q", "-m", "Open proposal: README tagline", cwd=repo)

        # --- Step 5a: append Decision and commit ---
        with proposal_path.open("a") as fh:
            fh.write("\n## Decision -- Maintainer -- 2026-05-28\n\nAccept.  Trivial.\n")
        _run_git("add", str(proposal_path.relative_to(repo)), cwd=repo)
        _run_git("commit", "-q", "-m", "Decision: accept README tagline", cwd=repo)

        # --- Step 5b: implement + archive + CHANGELOG, single commit ---
        # Edit README.md (the tagline).
        readme = repo / "README.md"
        readme.write_text(readme.read_text() + "\n> The disposable quickstart repo.\n")
        # git mv proposal -> archive.
        archive_dir = proposals_dir / "archive"
        archive_dir.mkdir(parents=True, exist_ok=True)
        archived_path = archive_dir / proposal_path.name
        _run_git(
            "mv",
            str(proposal_path.relative_to(repo)),
            str(archived_path.relative_to(repo)),
            cwd=repo,
        )
        # Update CHANGELOG > Unreleased.
        changelog = repo / "CHANGELOG.md"
        text = changelog.read_text()
        new_text = text.replace(
            "## Unreleased\n",
            "## Unreleased\n\n### Added\n\n- README tagline (trivial dogfood).\n",
        )
        changelog.write_text(new_text)
        # Single path-scoped commit for all three.
        _run_git(
            "commit",
            "-m",
            "Implement README tagline (trivial accept; archived)",
            str(readme.relative_to(repo)),
            str(archived_path.relative_to(repo)),
            # Naming BOTH sides of the git mv -- per AGENTS.md > "The
            # staged git index is a shared surface" / "A git mv rename
            # needs BOTH sides named in a path-scoped commit".
            str(proposal_path.relative_to(repo)),
            str(changelog.relative_to(repo)),
            cwd=repo,
        )

        # --- Assertions: lifecycle shape on disk ---
        # The proposal moved to archive/.
        assert archived_path.exists()
        assert not proposal_path.exists()
        # The Decision section is in the archived proposal.
        archived_text = archived_path.read_text()
        assert "## Decision -- Maintainer -- 2026-05-28" in archived_text
        # The CHANGELOG carries the new line.
        assert "README tagline" in changelog.read_text()
        # The README carries the tagline.
        assert "disposable quickstart repo" in readme.read_text()

    def test_step6_git_log_has_lifecycle_boundaries(
        self, disposable_repo: Path
    ) -> None:
        """Step 6 says ``git log --oneline`` shows five commits
        with clear lifecycle boundaries: init, install,
        proposal-open, decision, implement-and-archive.  This
        test reaches the same end-state and pins the commit
        count + boundary subjects."""
        repo = disposable_repo
        # Re-use Step 5's setup end-to-end.
        self._install_cairn(repo)
        proposal_stem = "2026-05-28-test-readme-tagline"
        proposals_dir = repo / "dev" / "proposals"
        proposal_path = proposals_dir / f"{proposal_stem}.md"
        proposal_path.write_text(
            "# README tagline\n\n**Status**: proposed\n\n## Proposal\n\nAdd a tagline.\n"
        )
        _run_git("add", str(proposal_path.relative_to(repo)), cwd=repo)
        _run_git("commit", "-q", "-m", "Open proposal: README tagline", cwd=repo)
        with proposal_path.open("a") as fh:
            fh.write("\n## Decision -- Maintainer -- 2026-05-28\n\nAccept.\n")
        _run_git("add", str(proposal_path.relative_to(repo)), cwd=repo)
        _run_git("commit", "-q", "-m", "Decision: accept README tagline", cwd=repo)
        readme = repo / "README.md"
        readme.write_text(readme.read_text() + "\n> Tagline.\n")
        archive_dir = proposals_dir / "archive"
        archive_dir.mkdir(parents=True, exist_ok=True)
        archived_path = archive_dir / proposal_path.name
        _run_git(
            "mv",
            str(proposal_path.relative_to(repo)),
            str(archived_path.relative_to(repo)),
            cwd=repo,
        )
        changelog = repo / "CHANGELOG.md"
        changelog.write_text(
            changelog.read_text().replace(
                "## Unreleased\n",
                "## Unreleased\n\n### Added\n\n- README tagline.\n",
            )
        )
        _run_git(
            "commit", "-m", "Implement README tagline",
            str(readme.relative_to(repo)),
            str(archived_path.relative_to(repo)),
            str(proposal_path.relative_to(repo)),
            str(changelog.relative_to(repo)),
            cwd=repo,
        )

        # --- Step 6 assertions ---
        result = subprocess.run(
            ["git", "log", "--oneline"],
            cwd=repo, capture_output=True, text=True, check=True,
        )
        lines = result.stdout.strip().splitlines()
        # Five lifecycle commits per Step 6's published count.
        assert len(lines) == 5, (
            f"quickstart Step 6 documents five commits; got {len(lines)}:\n{result.stdout}"
        )
        subjects = [line.split(" ", 1)[1] for line in lines]
        # Boundaries are present and ordered (newest first via git log).
        assert subjects[0].startswith("Implement README tagline")
        assert subjects[1].startswith("Decision: accept")
        assert subjects[2].startswith("Open proposal:")
        assert subjects[3].startswith("Install Cairn")
        assert subjects[4] == "init"
        # The proposal is in archive/.
        archive_listing = subprocess.run(
            ["ls", str(repo / "dev" / "proposals" / "archive")],
            capture_output=True, text=True, check=True,
        ).stdout
        assert f"{proposal_stem}.md" in archive_listing
