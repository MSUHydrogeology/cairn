"""
Tests for Cairn installation, lockfile migration, module adoption and upgrade.

Promises:
- Installation selects the requested profile and writes a lockfile whose
  hashes match installed files; mergeable files retain raw template bases.
- Profile changes update gated files without losing required operational
  sections, and an unchanged profile upgrades cleanly.
- ``upgrade --plan`` is read-only and reports adopter-visible merge states;
  staging and merging preserve local slot content or expose conflicts and
  review-only work for human review.
- ``upgrade --apply`` advances only a valid, complete stage. Stale or corrupt
  stages, unresolved conflicts, malformed paths, conflicting dirty work and
  hostile filesystem changes refuse without overwriting protected data.
- ``upgrade --init-lock`` migrates lockless installs into a reviewable lock,
  preserving profile values and identifying content it cannot recover.
- ``upgrade --plan`` warns when an installed fidelity manifest cites a stale
  lock and prefers the canonical manifest home over its legacy location.
- ``upgrade --finalize`` records the installed content and resolved wrapper
  path while retaining the upstream base needed to detect later forks.
- ``upgrade --adopt-module`` records only known opt-in modules, preserves their
  on-disk content and refuses unknown modules or missing/unsafe required data.
- Install and module adoption refuse token names that look secret before
  writing or recording project state; the public lockfile writer allows an
  explicit ``allow_secret_tokens`` list of names.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/
"""

from __future__ import annotations

import json
import io
import re
import shutil
import stat
import sys
from pathlib import Path, PureWindowsPath

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap import scaffold as s  # noqa: E402
from bootstrap import verify_integrity  # noqa: E402

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)


def _install(target: Path, preset: str = "solo-greenfield") -> int:
    cfg = target / "profile.yml"
    cfg.write_text(
        f"project_name: Demo\ntest_command: pytest\npreset: {preset}\n"
    )
    return s.main([
        "--config", str(cfg), "--target", str(target),
        "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
    ])


def _seed_profile(target: Path, **overrides: str) -> Path:
    """Write a complete six-axis dev/.cairn/profile.yml so `init-lock` can run
    (init-lock now requires a committed install-config)."""
    axes = {"age": "greenfield", "size": "small", "complexity": "simple",
            "language": "single", "human_team": "solo", "agent_team": "single"}
    axes.update(overrides)
    lines = ['project_name: "Demo"', 'test_command: "pytest"']
    lines += [f"{k}: {v}" for k, v in axes.items()]
    p = target / "dev" / ".cairn" / "profile.yml"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# Lockfile + base cache
# ---------------------------------------------------------------------------

class TestLockfile:
    def test_round_trip(self, tmp_path: Path) -> None:
        assert _install(tmp_path) == 0
        lock = s.read_lockfile(tmp_path)
        assert lock is not None
        assert lock["cairn_version"] and lock["files"]
        # every recorded hash matches the on-disk file
        for rec in lock["files"]:
            on_disk = (tmp_path / rec["dst"]).read_bytes()
            assert rec["hash"] == "sha256:" + s._sha256_hex(on_disk), rec["dst"]

    def test_base_cache_is_raw_mergeable_only(self, tmp_path: Path) -> None:
        assert _install(tmp_path) == 0
        lock = s.read_lockfile(tmp_path)
        for rec in lock["files"]:
            if rec["verbatim"]:
                assert "base_cache" not in rec  # scripts are not cached
                continue
            cache = tmp_path / rec["base_cache"]
            assert cache.exists(), rec["base_cache"]
            # the cache is the RAW upstream template (pre-substitution)
            raw = (TEMPLATES_ROOT / rec["src"]).read_text(encoding="utf-8")
            assert cache.read_text(encoding="utf-8") == raw
        # no .py under the base cache
        assert not list((tmp_path / "dev" / ".cairn" / "base").rglob("*.py"))

    def test_fail_closed_on_divergence(self, tmp_path: Path) -> None:
        assert _install(tmp_path) == 0
        (tmp_path / "AGENTS.md").write_text(
            (tmp_path / "AGENTS.md").read_text() + "\n<!-- local -->\n")
        (tmp_path / "dev" / ".cairn" / "cairn-lock.yml").unlink()
        # re-run install (skips existing); lockfile must NOT be written
        assert _install(tmp_path) == 0
        assert not (tmp_path / "dev" / ".cairn" / "cairn-lock.yml").exists()

    def test_public_writer_refuses_secret_tokens_without_writing_state(
        self, tmp_path: Path,
    ) -> None:
        assert _install(tmp_path) == 0
        lock = s.read_lockfile(tmp_path)
        assert lock is not None
        lock_path = tmp_path / "dev/.cairn/cairn-lock.yml"
        lock_before = lock_path.read_bytes()
        cache = tmp_path / "dev/.cairn/base"

        def cache_snapshot() -> dict[str, bytes]:
            return {
                p.relative_to(cache).as_posix(): p.read_bytes()
                for p in sorted(cache.rglob("*")) if p.is_file()
            }

        cache_before = cache_snapshot()
        modules, _summary = s.expand_preset({
            "preset": lock["profile"]["preset"],
        })
        writer_args = {
            "tokens": dict(lock["tokens"]),
            "modules": modules,
            "optional": list(lock["optional_templates"]),
            "profile": lock["profile"],
            "onboarding_preset": lock["profile"].get("preset"),
        }
        for name in (
            "api_token", "secret_key", "db_password", "apiKey",
            "secretToken", "dbPassword", "mysecret", "accessKey",
            "passwdstr",
        ):
            tokens = dict(lock["tokens"])
            tokens[name] = "harmless-fake-value"
            with pytest.raises(s.PresetError):
                s.write_install_lockfile(
                    tmp_path, CAIRN_ROOT, TEMPLATES_ROOT,
                    **{**writer_args, "tokens": tokens},
                )
            assert lock_path.read_bytes() == lock_before
            assert cache_snapshot() == cache_before

        # The public allow-list permits this benign fake value and completes
        # the same writer operation against the otherwise-valid install.
        allowed_tokens = dict(lock["tokens"])
        allowed_tokens["apiKey"] = "harmless-fake-value"
        written = s.write_install_lockfile(
            tmp_path, CAIRN_ROOT, TEMPLATES_ROOT,
            **{**writer_args, "tokens": allowed_tokens},
            allow_secret_tokens=("apiKey",),
        )
        assert written is not None
        assert s.read_lockfile(tmp_path)["tokens"]["apiKey"] == (
            "harmless-fake-value"
        )


# ---------------------------------------------------------------------------
# Profile-sized assembly: the lockfile's
# expected-clean-install `would` is stripped with the SAME embedded profile the
# install stripped the on-disk file with, so a profile-stripped install writes a
# clean lockfile (would == on-disk) and verifies clean -- while base_cache keeps
# the RAW (with-directive) template for the 3-way merge to reconstruct + restrip.
# ---------------------------------------------------------------------------

class TestProfileSizedAssembly:
    # A genuinely profile-optional region: kept only for multi-human teams.
    # The sentinel is deliberately unique so it cannot collide with real
    # template prose (the real AGENTS.md already discusses human contributors).
    _SENTINEL = "PROFILE_SIZED_ASSEMBLY_GATED_SENTINEL"
    _REGION = (
        "\n<!-- cairn:if human_team in small-multi,large-multi -->\n"
        f"## {_SENTINEL}\n"
        "Team-coordination prose only multi-human adopters carry.\n"
        "<!-- cairn:endif -->\n"
    )

    def _cairn_with_directive(self, tmp_path: Path) -> Path:
        """Copy the real templates tree into a tmp cairn-root and append a
        cairn:if region to core/AGENTS.md (gating has not yet reached the real
        template, so we inject one to exercise the strip end-to-end)."""
        croot = tmp_path / "cairn"
        shutil.copytree(TEMPLATES_ROOT, croot / "templates")
        (croot / "bootstrap" / "_scaffold").mkdir(parents=True)
        for name in ("config.py", "install.py"):
            shutil.copy2(CAIRN_ROOT / "bootstrap" / "_scaffold" / name,
                         croot / "bootstrap" / "_scaffold" / name)
        cff = CAIRN_ROOT / "CITATION.cff"
        if cff.exists():
            shutil.copy2(cff, croot / "CITATION.cff")
        agents = croot / "templates" / "core" / "AGENTS.md"
        agents.write_text(
            agents.read_text(encoding="utf-8") + self._REGION, encoding="utf-8")
        return croot

    @staticmethod
    def _install_from(target: Path, croot: Path, preset: str) -> int:
        target.mkdir(parents=True, exist_ok=True)
        cfg = target / "profile.yml"
        cfg.write_text(
            f"project_name: Demo\ntest_command: pytest\npreset: {preset}\n")
        return s.main([
            "--config", str(cfg), "--target", str(target),
            "--cairn-root", str(croot), "--allow-dev",
        ])

    def test_solo_strips_region_lockfile_and_verify_clean(
        self, tmp_path: Path
    ) -> None:
        croot = self._cairn_with_directive(tmp_path)
        target = tmp_path / "solo"
        assert self._install_from(target, croot, "solo-greenfield") == 0
        agents = (target / "AGENTS.md").read_text(encoding="utf-8")
        # the gated region is stripped from the solo install, markers and all
        assert self._SENTINEL not in agents
        assert "cairn:if" not in agents and "cairn:endif" not in agents
        # would == on-disk: the lockfile is written (not fail-closed-diverged)
        lock = s.read_lockfile(target)
        assert lock is not None
        rec = next(r for r in lock["files"] if r["dst"] == "AGENTS.md")
        on_disk = (target / "AGENTS.md").read_bytes()
        assert rec["hash"] == "sha256:" + s._sha256_hex(on_disk)
        # base_cache keeps the RAW (with-directive) template -- strip is a
        # reconstruction-time concern, not baked into the cache (it is restripped)
        cache = (target / rec["base_cache"]).read_text(encoding="utf-8")
        assert "cairn:if human_team" in cache
        # the tamper check attests the stripped install clean
        assert verify_integrity.verify(target) == 0

    def test_multi_keeps_region_lockfile_and_verify_clean(
        self, tmp_path: Path
    ) -> None:
        croot = self._cairn_with_directive(tmp_path)
        target = tmp_path / "multi"
        # collaborative-team resolves human_team=small-multi -> region kept
        assert self._install_from(target, croot, "collaborative-team") == 0
        agents = (target / "AGENTS.md").read_text(encoding="utf-8")
        assert self._SENTINEL in agents              # kept for the team
        assert "cairn:if" not in agents and "cairn:endif" not in agents
        lock = s.read_lockfile(target)
        assert lock is not None
        rec = next(r for r in lock["files"] if r["dst"] == "AGENTS.md")
        on_disk = (target / "AGENTS.md").read_bytes()
        assert rec["hash"] == "sha256:" + s._sha256_hex(on_disk)
        assert verify_integrity.verify(target) == 0

    def test_same_profile_upgrade_is_a_clean_noop(self, tmp_path: Path) -> None:
        """The previously-49-failing surface: a profile-stripped (solo) install
        upgrades against the same upstream + same profile with NOTHING to
        re-stage -- base, theirs and ours all agree on the stripped region, so
        the merge is a clean no-op (no spurious conflict / locally-modified)."""
        croot = self._cairn_with_directive(tmp_path)
        target = tmp_path / "solo"
        assert self._install_from(target, croot, "solo-greenfield") == 0
        assert s.main(["upgrade", "--target", str(target), "--stage",
                       "--cairn-root", str(croot)]) == 0
        staged = target / "dev" / ".cairn-upgrade" / "files"
        # AGENTS.md is not re-staged: the stripped ancestor matches the install
        assert not (staged / "AGENTS.md").exists()
        assert verify_integrity.verify(target) == 0

    def test_profile_change_solo_to_multi_reincludes_region(
        self, tmp_path: Path
    ) -> None:
        """An adopter who flips solo -> multi and upgrades gets the
        gated region cleanly RE-INCLUDED (a clean ADD relative to the
        old-profile base), with a local customization preserved, the lockfile
        profile re-embedded to the new profile, and verify clean -- no clobber."""
        croot = self._cairn_with_directive(tmp_path)
        target = tmp_path / "adopter"
        assert self._install_from(target, croot, "solo-greenfield") == 0
        agents_path = target / "AGENTS.md"
        assert self._SENTINEL not in agents_path.read_text(encoding="utf-8")
        # the adopter customizes a line NEAR THE TOP (far from the end-appended
        # gated region, so the two changes land in different merge hunks) ...
        lines = agents_path.read_text(encoding="utf-8").splitlines(keepends=True)
        lines.insert(1, "<!-- LOCAL CUSTOMIZATION: keep me -->\n")
        agents_path.write_text("".join(lines), encoding="utf-8")
        # ... and flips their committed profile from solo to multi-human.
        prof = target / "dev" / ".cairn" / "profile.yml"
        prof.parent.mkdir(parents=True, exist_ok=True)
        prof.write_text(
            "project_name: Demo\ntest_command: pytest\n"
            "age: greenfield\nsize: small\ncomplexity: simple\n"
            "language: single\nhuman_team: small-multi\nagent_team: single\n",
            encoding="utf-8")
        assert s.main(["upgrade", "--target", str(target), "--stage",
                       "--cairn-root", str(croot)]) == 0
        assert s.main(["upgrade", "--target", str(target), "--apply",
                       "--cairn-root", str(croot)]) == 0
        merged = agents_path.read_text(encoding="utf-8")
        assert self._SENTINEL in merged                       # region re-included
        assert "LOCAL CUSTOMIZATION: keep me" in merged       # customization kept
        # the advanced lockfile re-embeds the NEW profile + verify attests clean
        lock2 = s.read_lockfile(target)
        assert lock2["profile"]["axes"]["human_team"] == "small-multi"
        rec = next(r for r in lock2["files"] if r["dst"] == "AGENTS.md")
        assert rec["hash"] == "sha256:" + s._sha256_hex(agents_path.read_bytes())
        assert verify_integrity.verify(target) == 0


# ---------------------------------------------------------------------------
# Template gating safety: core AGENTS.md carries every operative rule for
# every profile. Human-contributor guidance is selected as an optional file.
# ---------------------------------------------------------------------------

class TestTemplateGatingSafety:
    def _template(self) -> str:
        return (TEMPLATES_ROOT / "core" / "AGENTS.md").read_text(
            encoding="utf-8")

    def test_optional_contributor_file_is_selected_by_human_team(self) -> None:
        """The human-team axis selects the optional file, not core rules."""
        from bootstrap._scaffold.config import select_optional_templates  # noqa: PLC0415,E501
        text = self._template()
        assert "cairn:if" not in text and "cairn:endif" not in text
        assert select_optional_templates({"human_team": "solo"}) == []
        expected = [("optional/CONTRIBUTING.md", "CONTRIBUTING.md")]
        assert select_optional_templates({"human_team": "small-multi"}) == expected
        assert select_optional_templates({"human_team": "large-multi"}) == expected

    def test_solo_keeps_all_brightlines_without_contributor_file(
        self, tmp_path: Path
    ) -> None:
        assert _install(tmp_path, "solo-greenfield") == 0
        agents = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
        assert not (tmp_path / "CONTRIBUTING.md").exists()
        assert "cairn:if" not in agents and "cairn:endif" not in agents
        assert verify_integrity.verify(tmp_path) == 0

    def test_multi_keeps_brightlines_and_installs_contributor_file(self, tmp_path: Path) -> None:
        assert _install(tmp_path, "collaborative-team") == 0
        agents = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
        contributing = (tmp_path / "CONTRIBUTING.md").read_text(encoding="utf-8")
        assert "# Contributing to Demo" in contributing
        assert "{{project_name}}" not in contributing
        assert "cairn:if" not in agents and "cairn:endif" not in agents
        assert verify_integrity.verify(tmp_path) == 0


# ---------------------------------------------------------------------------
# Slot parser fail-closed
# ---------------------------------------------------------------------------

class TestSlotParser:
    def test_valid(self) -> None:
        slots = s.parse_slots(
            "a\n<!-- cairn:slot x -->\nB\n<!-- cairn:end x -->\nc\n")
        assert [(sl.name, sl.body) for sl in slots] == [("x", "B")]

    @pytest.mark.parametrize("text", [
        "<!-- cairn:slot a -->\n<!-- cairn:end a -->\n"
        "<!-- cairn:slot a -->\n<!-- cairn:end a -->\n",                  # dup
        "<!-- cairn:slot a -->\n<!-- cairn:slot b -->\n"
        "<!-- cairn:end b -->\n<!-- cairn:end a -->\n",                   # nested
        "<!-- cairn:end a -->\n",                                        # end-first
        "<!-- cairn:slot a -->\n<!-- cairn:end b -->\n",                  # mismatch
        "<!-- cairn:slot a -->\nbody\n",                                 # unclosed
    ])
    def test_fail_closed(self, text: str) -> None:
        with pytest.raises(s.SlotError):
            s.parse_slots(text)


# ---------------------------------------------------------------------------
# Merge engine
# ---------------------------------------------------------------------------

class TestMerge:
    BASE = ("# {{project_name}}\nIntro.\n"
            "<!-- cairn:slot n -->\nPH\n<!-- cairn:end n -->\nFoot.\n")
    OURS = ("# Demo\nIntro.\n"
            "<!-- cairn:slot n -->\nMINE\n<!-- cairn:end n -->\nFoot.\n")
    TOK = {"project_name": "Demo"}

    def test_clean_fold_preserves_slot(self) -> None:
        theirs = self.BASE.replace("Intro.\n", "Intro.\nNEW doctrine.\n")
        r = s.merge_file(self.BASE, theirs, self.OURS, self.TOK)
        assert r.status == "clean"
        assert "MINE" in r.merged and "NEW doctrine." in r.merged
        assert "PH" not in r.merged

    def test_slot_survives_prose_rewrite(self) -> None:
        theirs = self.BASE.replace("Intro.", "Rewritten intro.").replace(
            "Foot.", "New foot.")
        r = s.merge_file(self.BASE, theirs, self.OURS, self.TOK)
        assert "MINE" in r.merged

    def test_true_conflict_emits_markers(self) -> None:
        ours = self.OURS.replace("Intro.", "Intro (ours).")
        theirs = self.BASE.replace("Intro.", "Intro (theirs).")
        r = s.merge_file(self.BASE, theirs, ours, self.TOK)
        assert r.status == "conflict"
        assert "<<<<<<< ours" in r.merged and ">>>>>>> theirs" in r.merged

    def test_slot_removed_fail_closed(self) -> None:
        theirs = "# {{project_name}}\nIntro.\nFoot.\n"  # slot gone
        r = s.merge_file(self.BASE, theirs, self.OURS, self.TOK)
        assert r.status == "slot-removed"

    def test_empty_slot_body_transplants_faithfully(self) -> None:
        """A single-empty-line slot body must not be dropped during
        transplant (it would desync the three inputs and spuriously
        conflict)."""
        base = ("# {{project_name}}\n"
                "<!-- cairn:slot n -->\n\n<!-- cairn:end n -->\nFoot.\n")
        ours = ("# Demo\n"
                "<!-- cairn:slot n -->\n\n<!-- cairn:end n -->\nFoot.\n")
        theirs = base.replace("Foot.", "New foot.")
        r = s.merge_file(base, theirs, ours, self.TOK)
        assert r.status == "clean", (r.status, r.merged)
        assert "New foot." in r.merged
        # the transplant preserved ours faithfully (round-trips to ours-shape)
        assert s.parse_slots(r.merged)[0].body == ""

    def test_needs_value_is_non_advancing(self) -> None:
        # upstream introduces a brand-new token with no recorded value
        theirs = self.BASE.replace("Intro.", "Owner: {{owner_email}}")
        r = s.merge_file(self.BASE, theirs, self.OURS, self.TOK)
        assert r.status == "needs-value"  # not "clean" -> won't stage/apply


# ---------------------------------------------------------------------------
# Verbatim hash policy (Part 4)
# ---------------------------------------------------------------------------

class TestVerbatim:
    def test_classify(self) -> None:
        script = b"print('x')\n"
        h = "sha256:" + s._sha256_hex(script)
        assert s.classify_verbatim(script, h, b"print('v2')\n") == "update"
        assert s.classify_verbatim(b"forked\n", h, b"v2\n") == "locally-modified"
        assert s.classify_verbatim(script, h, script) == "up-to-date"
        assert s.classify_verbatim(None, h, script) == "missing"

    def test_apply_leaves_base_hash_equal_to_hash_for_an_untouched_verbatim(
        self, tmp_path: Path,
    ) -> None:
        """After an apply installs upstream bytes for a verbatim record, that
        record's ``base_hash`` must equal its ``hash``.

        ``base_hash`` is the as-shipped baseline the NEXT upgrade uses for fork
        detection (``classify_verbatim``). A verbatim record has no
        ``base_cache``, so if apply advances ``hash`` without ``base_hash`` the
        two fields disagree while the file on disk is untouched upstream
        content -- and the next upgrade reads that disagreement as an adopter
        fork. It then refuses to update the file, to protect a customization
        that does not exist, and the adopter is frozen on that version for
        good. Measured on two real adopter trees: 32 files stuck on templates
        four months old, with no adopter edit behind any of them.
        """
        assert _install(tmp_path) == 0
        lock = s.read_lockfile(tmp_path)
        verbatim = [r for r in lock["files"]
                    if r.get("verbatim") and (tmp_path / r["dst"]).exists()]
        assert verbatim, "the preset must install at least one verbatim file"

        # Model an OLD install: the file and both hash fields carry content
        # that predates the current upstream template, so the upgrade sees a
        # genuine upstream change with no adopter edit behind it.
        rec = verbatim[0]
        old = b"# old upstream content\n"
        (tmp_path / rec["dst"]).write_bytes(old)
        old_h = "sha256:" + s._sha256_hex(old)
        for r in lock["files"]:
            if r["dst"] == rec["dst"]:
                r["hash"] = r["base_hash"] = old_h
        (tmp_path / "dev" / ".cairn" / "cairn-lock.yml").write_text(
            s._emit_lock_yaml(lock), encoding="utf-8")

        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        assert s.main(["upgrade", "--target", str(tmp_path), "--apply",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0

        after = next(r for r in s.read_lockfile(tmp_path)["files"]
                     if r["dst"] == rec["dst"])
        on_disk = "sha256:" + s._sha256_hex((tmp_path / rec["dst"]).read_bytes())
        assert after["hash"] == on_disk, "apply must advance hash to the applied bytes"
        assert after["base_hash"] == after["hash"], (
            f"base_hash went stale: hash={after['hash'][:19]} "
            f"base_hash={after.get('base_hash', '(none)')[:19]}. The next "
            f"upgrade will read {rec['dst']} as an adopter fork and stop "
            f"updating it."
        )


# ---------------------------------------------------------------------------
# upgrade subcommand: modes + safety contract
# ---------------------------------------------------------------------------

class TestUpgradeModes:
    def _diverge_base(self, target: Path) -> None:
        """Model an *old install + adopter customization*: the cached base
        AND the adopter's file both carry the old header (so it matches the
        old base), while the current upstream template carries the new
        header -> a real upstream change folds into ours, and ours' added
        line is preserved, with no conflict."""
        base = target / "dev" / ".cairn" / "base" / "AGENTS.md"
        base.write_text(
            base.read_text(encoding="utf-8").replace("# AGENTS.md", "# OLD", 1),
            encoding="utf-8", newline="\n")
        a = target / "AGENTS.md"
        a.write_text(
            a.read_text(encoding="utf-8").replace("# AGENTS.md", "# OLD", 1)
            + "\n<!-- keep me -->\n", encoding="utf-8", newline="\n")
        lock = s.read_lockfile(target)
        rec = next(r for r in lock["files"] if r["dst"] == "AGENTS.md")
        rec["base_hash"] = "sha256:" + s._sha256_hex(base.read_bytes())
        (target / "dev" / ".cairn" / "cairn-lock.yml").write_text(
            s._emit_lock_yaml(lock), encoding="utf-8")

    def test_plan_writes_nothing(self, tmp_path: Path) -> None:
        assert _install(tmp_path) == 0
        self._diverge_base(tmp_path)

        def project_snapshot() -> dict[str, tuple[object, ...]]:
            entries: dict[str, tuple[object, ...]] = {}
            root_info = tmp_path.lstat()
            entries["."] = ("directory", stat.S_IMODE(root_info.st_mode))
            for path in sorted(tmp_path.rglob("*")):
                rel = path.relative_to(tmp_path).as_posix()
                info = path.lstat()
                mode = stat.S_IMODE(info.st_mode)
                if stat.S_ISLNK(info.st_mode):
                    entries[rel] = ("symlink", mode, path.readlink().as_posix())
                elif stat.S_ISDIR(info.st_mode):
                    entries[rel] = ("directory", mode)
                elif stat.S_ISREG(info.st_mode):
                    entries[rel] = ("file", mode, path.read_bytes())
                else:
                    entries[rel] = ("other", stat.S_IFMT(info.st_mode), mode)
            return entries

        before = project_snapshot()
        rc = s.main(["upgrade", "--target", str(tmp_path), "--plan",
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 0
        assert not (tmp_path / "dev" / ".cairn-upgrade").exists()
        after = project_snapshot()
        changed = sorted(
            path for path in before.keys() | after.keys()
            if before.get(path) != after.get(path)
        )
        assert after == before, f"upgrade --plan changed project entries: {changed}"

    def test_stage_then_apply(self, tmp_path: Path) -> None:
        assert _install(tmp_path) == 0
        self._diverge_base(tmp_path)
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        staged = tmp_path / "dev" / ".cairn-upgrade" / "files" / "AGENTS.md"
        assert staged.exists() and "keep me" in staged.read_text()
        assert "OLD" not in staged.read_text()  # upstream header folded
        assert s.main(["upgrade", "--target", str(tmp_path), "--apply",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        ag = tmp_path / "AGENTS.md"
        assert "keep me" in ag.read_text() and "# OLD" not in ag.read_text()
        assert not (tmp_path / "dev" / ".cairn-upgrade").exists()  # cleaned
        # apply ADVANCED the machine authority -- the lockfile hash
        # now matches the applied file, and the base cache is the new
        # upstream raw template (not the old "# OLD" base).
        lock = s.read_lockfile(tmp_path)
        rec = next(r for r in lock["files"] if r["dst"] == "AGENTS.md")
        assert rec["hash"] == "sha256:" + s._sha256_hex(ag.read_bytes())
        base = tmp_path / "dev" / ".cairn" / "base" / "AGENTS.md"
        assert "# OLD" not in base.read_text()  # base advanced
        assert rec["base_hash"] == "sha256:" + s._sha256_hex(base.read_bytes())
        # A second upgrade on the now-current tree is a no-op (clean loop).
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        sd = tmp_path / "dev" / ".cairn-upgrade" / "files"
        assert not (sd.exists() and any(sd.rglob("*")))  # nothing to re-stage

    @pytest.mark.parametrize("bad_evidence", [
        "altered-cache", "missing-cache", "missing-digest", "malformed-digest",
        "unreadable-cache", "invalid-utf8", "legacy-record",
    ])
    def test_bad_ancestor_uses_review_recovery_and_preserves_evidence(
        self, tmp_path: Path, bad_evidence: str, monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        assert _install(tmp_path) == 0
        lock = s.read_lockfile(tmp_path)
        rec = next(r for r in lock["files"] if r["dst"] == "AGENTS.md")
        cache = tmp_path / rec["base_cache"]
        original_bad = cache.read_bytes()
        if bad_evidence == "altered-cache":
            cache.write_bytes(original_bad + b"altered\n")
        elif bad_evidence == "missing-cache":
            cache.unlink()
        elif bad_evidence == "missing-digest":
            rec.pop("base_hash", None)
        elif bad_evidence == "malformed-digest":
            rec["base_hash"] = "sha256:1234"
        elif bad_evidence == "unreadable-cache":
            pass
        elif bad_evidence == "invalid-utf8":
            cache.write_bytes(b"\xff\xfe invalid utf8")
            rec["base_hash"] = "sha256:" + s._sha256_hex(cache.read_bytes())
        elif bad_evidence == "legacy-record":
            rec.pop("base_hash", None)
        lockfile = tmp_path / "dev" / ".cairn" / "cairn-lock.yml"
        lockfile.write_text(s._emit_lock_yaml(lock), encoding="utf-8")
        lock_before_apply = s.read_lockfile(tmp_path)
        bad_cache_before_apply = cache.read_bytes() if cache.exists() else None
        adopter_before = (tmp_path / "AGENTS.md").read_bytes()

        if bad_evidence == "unreadable-cache":
            from bootstrap._scaffold import upgrade as upgrade_module
            read_regular = upgrade_module._read_regular_bytes

            def read_with_unreadable_ancestor(path: Path):
                if path == cache:
                    raise PermissionError("synthetic unreadable cache")
                return read_regular(path)

            with monkeypatch.context() as patcher:
                patcher.setattr(upgrade_module, "_read_regular_bytes",
                                read_with_unreadable_ancestor)
                assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                               "--cairn-root", str(CAIRN_ROOT)]) == 0
        else:
            assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                           "--cairn-root", str(CAIRN_ROOT)]) == 0
        stage = tmp_path / "dev" / ".cairn-upgrade"
        review = stage / "review-only" / "AGENTS.md.theirs"
        assert review.is_file()
        assert (tmp_path / "AGENTS.md").read_bytes() == adopter_before
        assert "AGENTS.md" in json.loads((stage / s._STAGE_META).read_text())["review_only"]

        if bad_evidence == "unreadable-cache":
            rc = s.main(["upgrade", "--target", str(tmp_path), "--apply",
                         "--ack-review-only", "--cairn-root", str(CAIRN_ROOT)])
            assert rc == 1  # the cache became readable after this stage snapshot
            assert (tmp_path / "AGENTS.md").read_bytes() == adopter_before
            assert s.read_lockfile(tmp_path) == lock_before_apply
            assert stage.exists()
            return

        # Manual reconciliation selects the displayed upstream text. Apply
        # records that result and establishes its raw upstream source as the
        # next ancestor, while the original cache remains untouched evidence.
        (tmp_path / "AGENTS.md").write_text(review.read_text(), encoding="utf-8")
        assert s.main(["upgrade", "--target", str(tmp_path), "--apply",
                       "--ack-review-only", "--cairn-root", str(CAIRN_ROOT)]) == 0
        lock_after = s.read_lockfile(tmp_path)
        rec_after = next(r for r in lock_after["files"] if r["dst"] == "AGENTS.md")
        assert rec_after["base_cache"] != rec["base_cache"]
        if bad_cache_before_apply is None:
            assert not cache.exists()
        else:
            assert cache.read_bytes() == bad_cache_before_apply
        new_base = tmp_path / rec_after["base_cache"]
        assert rec_after["base_hash"] == "sha256:" + s._sha256_hex(new_base.read_bytes())
        assert new_base.read_bytes() == (TEMPLATES_ROOT / rec_after["src"]).read_bytes()

        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        if bad_evidence == "altered-cache":
            new_base.write_bytes(b"second corrupted ancestor")
            assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                           "--cairn-root", str(CAIRN_ROOT)]) == 0
            review = stage / "review-only" / "AGENTS.md.theirs"
            (tmp_path / "AGENTS.md").write_text(review.read_text(), encoding="utf-8")
            assert s.main(["upgrade", "--target", str(tmp_path), "--apply",
                           "--ack-review-only", "--cairn-root", str(CAIRN_ROOT)]) == 0
            second = next(r for r in s.read_lockfile(tmp_path)["files"]
                          if r["dst"] == "AGENTS.md")
            assert second["base_cache"] != rec_after["base_cache"]
            assert new_base.read_bytes() == b"second corrupted ancestor"
            assert cache.read_bytes() == bad_cache_before_apply
            assert (tmp_path / second["base_cache"]).read_bytes() == (
                TEMPLATES_ROOT / second["src"]).read_bytes()

    def test_apply_rejects_stale_stage(self, tmp_path: Path) -> None:
        assert _install(tmp_path) == 0
        self._diverge_base(tmp_path)
        s.main(["upgrade", "--target", str(tmp_path), "--stage",
                "--cairn-root", str(CAIRN_ROOT)])
        # adopter edits the original after staging
        a = tmp_path / "AGENTS.md"
        a.write_text(a.read_text() + "\nlater edit\n")
        before = (a.read_bytes(), (tmp_path / s._LOCKFILE_REL).read_bytes())
        rc = s.main(["upgrade", "--target", str(tmp_path), "--apply",
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 1  # stale -> refused
        assert (a.read_bytes(), (tmp_path / s._LOCKFILE_REL).read_bytes()) == before

    @pytest.mark.parametrize("rules_deleted", [False, True],
                             ids=["agents", "deleted-rules"])
    def test_apply_rejects_changed_ancestor_since_stage(
        self, tmp_path: Path, rules_deleted: bool
    ) -> None:
        assert _install(tmp_path) == 0
        self._diverge_base(tmp_path)
        if rules_deleted:
            (tmp_path / "RULES.md").unlink()
        lock_before = s.read_lockfile(tmp_path)
        original_file = (tmp_path / "AGENTS.md").read_bytes()
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        ancestor_dst = "RULES.md" if rules_deleted else "AGENTS.md"
        rec = next(r for r in lock_before["files"] if r["dst"] == ancestor_dst)
        cache = tmp_path / rec["base_cache"]
        cache.write_bytes(cache.read_bytes() + b"changed after stage\n")
        rc = s.main(["upgrade", "--target", str(tmp_path), "--apply",
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 1
        assert (tmp_path / "AGENTS.md").read_bytes() == original_file
        if rules_deleted:
            assert not (tmp_path / "RULES.md").exists()
        assert s.read_lockfile(tmp_path) == lock_before
        assert (tmp_path / "dev" / ".cairn-upgrade").exists()

    def test_apply_rejects_changed_digest_since_stage(self, tmp_path: Path) -> None:
        assert _install(tmp_path) == 0
        self._diverge_base(tmp_path)
        lock_before = s.read_lockfile(tmp_path)
        original_file = (tmp_path / "AGENTS.md").read_bytes()
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        changed = s.read_lockfile(tmp_path)
        rec = next(r for r in changed["files"] if r["dst"] == "AGENTS.md")
        rec["base_hash"] = "sha256:" + "0" * 64
        lockfile = tmp_path / "dev" / ".cairn" / "cairn-lock.yml"
        lockfile.write_text(s._emit_lock_yaml(changed), encoding="utf-8")

        rc = s.main(["upgrade", "--target", str(tmp_path), "--apply",
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 1
        assert (tmp_path / "AGENTS.md").read_bytes() == original_file
        assert (tmp_path / "dev" / ".cairn-upgrade").exists()
        assert s.read_lockfile(tmp_path) == changed

    def test_apply_rechecks_ancestor_before_each_destination_write(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        assert _install(tmp_path) == 0
        self._diverge_base(tmp_path)
        lock = s.read_lockfile(tmp_path)
        second_dst = "VENDOR.md"
        second_base = tmp_path / "dev" / ".cairn" / "base" / second_dst
        second_file = tmp_path / second_dst
        second_old = "# Vendor wrapper"
        second_base.write_text(
            second_base.read_text().replace(second_old, "# OLD VENDOR", 1),
            encoding="utf-8")
        second_file.write_text(
            second_file.read_text().replace(second_old, "# OLD VENDOR", 1),
            encoding="utf-8")
        second_rec = next(r for r in lock["files"] if r["dst"] == second_dst)
        second_rec["base_hash"] = "sha256:" + s._sha256_hex(second_base.read_bytes())
        (tmp_path / "dev" / ".cairn" / "cairn-lock.yml").write_text(
            s._emit_lock_yaml(lock), encoding="utf-8")
        lock_before = s.read_lockfile(tmp_path)
        original_first = (tmp_path / "AGENTS.md").read_bytes()
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        stage = tmp_path / "dev" / ".cairn-upgrade"
        meta = json.loads((stage / s._STAGE_META).read_text())
        evidenced = [dst for dst in meta["staged_files"]
                     if dst in meta["ancestor_evidence"]]
        assert "AGENTS.md" in evidenced and second_dst in evidenced

        first_path = tmp_path / evidenced[0]
        second_evidence_dst = next(dst for dst in evidenced if dst != evidenced[0])
        second_original = (tmp_path / second_evidence_dst).read_bytes()
        second_cache = tmp_path / meta["ancestor_evidence"][second_evidence_dst]["base_cache"]
        real_write_text = Path.write_text
        changed = False

        def change_later_ancestor_after_first_write(path: Path, *args, **kwargs):
            nonlocal changed
            result = real_write_text(path, *args, **kwargs)
            if path == first_path and not changed:
                second_cache.write_bytes(second_cache.read_bytes() + b"late change\n")
                changed = True
            return result

        monkeypatch.setattr(Path, "write_text", change_later_ancestor_after_first_write)
        rc = s.main(["upgrade", "--target", str(tmp_path), "--apply",
                     "--cairn-root", str(CAIRN_ROOT)])
        output = capsys.readouterr().err
        assert rc == 1 and changed
        assert "during apply" in output and "Earlier files already applied" in output
        assert first_path.read_bytes() != original_first
        assert (tmp_path / second_evidence_dst).read_bytes() == second_original
        assert s.read_lockfile(tmp_path) == lock_before
        assert stage.exists()

    def test_apply_rejects_conflict_markers(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str],
    ) -> None:
        assert _install(tmp_path) == 0
        self._diverge_base(tmp_path)
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        stage = tmp_path / "dev" / ".cairn-upgrade"
        (stage / "files" / "AGENTS.md").write_text(
            "<<<<<<< ours\nx\n=======\ny\n>>>>>>> theirs\n")
        meta = json.loads((stage / s._STAGE_META).read_text())
        assert "AGENTS.md" in meta["staged_files"]
        assert meta["directory_observed"]
        rc = s.main(["upgrade", "--target", str(tmp_path), "--apply",
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 1
        assert "AGENTS.md still has conflict markers" in capsys.readouterr().err

    # ---- B-C-1: clean-vs-locally-modified split in the upgrade summary
    # `--plan` previously lumped every clean merge into one `clean` row,
    # hiding from the adopter whether their customizations rode through.
    # The split distinguishes `clean (untouched)` from
    # `locally-modified (merged clean)` so the adopter sees the merge
    # preserved their edits.

    def test_plan_reports_clean_untouched_after_upstream_advance(
        self, tmp_path: Path, capsys,
    ) -> None:
        """The public plan identifies an upstream-only edit as untouched."""
        assert _install(tmp_path) == 0
        base = tmp_path / "dev" / ".cairn" / "base" / "NOTICE.md"
        ours = tmp_path / "NOTICE.md"
        old_header = "Cairn asks essentially nothing of you"
        assert old_header in ours.read_text()
        prior = "Cairn once asked nothing of you"
        base.write_text(base.read_text().replace(old_header, prior, 1))
        ours.write_text(ours.read_text().replace(old_header, prior, 1))
        lock = s.read_lockfile(tmp_path)
        rec = next(r for r in lock["files"] if r["dst"] == "NOTICE.md")
        rec["base_hash"] = "sha256:" + s._sha256_hex(base.read_bytes())
        (tmp_path / "dev" / ".cairn" / "cairn-lock.yml").write_text(
            s._emit_lock_yaml(lock), encoding="utf-8")

        capsys.readouterr()
        rc = s.main(["upgrade", "--target", str(tmp_path), "--plan",
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 0
        out = capsys.readouterr().out
        assert any("clean (untouched)" in line and "NOTICE.md" in line
                   for line in out.splitlines()), out

    def test_a_merged_slot_makes_AGENTS_md_locally_modified_on_upgrade(
        self, tmp_path: Path
    ) -> None:
        """**Characterization, not a guard.** A green run here records an
        open residual rather than a closed one.

        `security-verification-activation` Chunk B made
        `security-verification` default-on, and that module is the first
        shipped one to carry a `cairn:merge-target` directive.  So on a
        stock install the module-merge pass rewrites AGENTS.md *after*
        `install_core` wrote it, while the base-template cache under
        ``dev/.cairn/base/`` keeps the **unmerged** template.  ``ours !=
        substitute_tokens(base, tokens)`` immediately, with no adopter edit
        at all -- so **every** adopter's AGENTS.md now reports
        ``clean-locally-modified`` on their first upgrade instead of
        ``clean``.

        Consequences, stated rather than implied:

        * It is **not** a failed or blocked upgrade.  Both kinds are in
          ``_ADVANCING_KINDS`` (asserted below), so the file stages and
          applies identically; only the label the adopter reads changes.
        * The label is nonetheless **inaccurate** for an adopter who
          customized nothing: it says "locally modified" about a
          difference Cairn's own install created.
        * Closing it would mean teaching the base-template cache about the
          merge overlay -- engine scope neither this plan nor its reviews
          authorized.  Pinned here so the next author finds it.
        """
        assert _install(tmp_path) == 0
        base = tmp_path / "dev" / ".cairn" / "base" / "AGENTS.md"
        ours = tmp_path / "AGENTS.md"
        merged_fragment = "scripts/run_security_verification.py"
        assert merged_fragment in ours.read_text(), (
            "the module-merge pass did not fill the security-verification "
            "slot on a stock install -- this node's premise is gone"
        )
        assert merged_fragment not in base.read_text(), (
            "the base-template cache now carries the merged text; if that "
            "is deliberate, this residual is CLOSED and the node should be "
            "replaced by a guard"
        )
        lock = s.read_lockfile(tmp_path)
        plans, _structural = s._compute_upgrade(
            tmp_path, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref=None,
        )
        ag_plan = next(p for p in plans if p.dst == "AGENTS.md")
        assert ag_plan.kind == "clean-locally-modified", (
            f"expected the recorded residual (a stock install already reads "
            f"as locally modified); got {ag_plan.kind!r}"
        )
        assert ag_plan.kind in s._ADVANCING_KINDS, (
            "the residual is a mislabel, not a blocked upgrade -- if this "
            "fails it has become a real regression"
        )


    def test_finalize_makes_customized_install_verifiable(
        self, tmp_path: Path
    ) -> None:
        """A *customized* install -- a filled slot /
        edited doc plus the ``VENDOR.md -> CLAUDE.md`` wrapper rename -- fails
        ``verify_integrity`` because the lockfile records the clean-install
        hashes (and the absent VENDOR.md).  ``upgrade --finalize`` advances each
        record's ``hash`` to the committed on-disk content and resolves the
        wrapper dst, so the verifier attests the tree the adopter actually
        ships.  The upgrade ancestor (``base_cache`` / ``base_hash``) is left
        intact."""
        from bootstrap.verify_integrity import verify

        assert _install(tmp_path) == 0
        ag = tmp_path / "AGENTS.md"
        ag.write_text(ag.read_text() + "\n<!-- adopter customization -->\n")
        (tmp_path / "VENDOR.md").rename(tmp_path / "CLAUDE.md")  # adopter rename
        # Before finalize: integrity fails (edited hash + missing VENDOR.md).
        assert verify(tmp_path) == 1
        assert s.main(["upgrade", "--finalize", "--target", str(tmp_path),
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        # After finalize: integrity attests the customized tree.
        assert verify(tmp_path) == 0
        lock = s.read_lockfile(tmp_path)
        dsts = {r["dst"] for r in lock["files"]}
        assert "CLAUDE.md" in dsts and "VENDOR.md" not in dsts
        # The wrapper's hash advanced to the on-disk (renamed) file.
        wrapper = next(r for r in lock["files"] if r["src"] == "core/VENDOR.md")
        assert wrapper["hash"] == "sha256:" + s._sha256_hex(
            (tmp_path / "CLAUDE.md").read_bytes())
        # Idempotent: a second finalize changes nothing and still verifies.
        assert s.main(["upgrade", "--finalize", "--target", str(tmp_path),
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        assert verify(tmp_path) == 0

    def test_finalize_preserves_verbatim_fork_detection(
        self, tmp_path: Path
    ) -> None:
        """Companion: finalize advances a forked
        verbatim script's ``hash`` to the fork but preserves the as-shipped
        ``base_hash``, so ``classify_verbatim`` still sees a fork (a subsequent
        upgrade classifies it ``verbatim-locally-modified``, not a clean
        ``update`` that would clobber the project-owned fork)."""
        assert _install(tmp_path) == 0
        lock = s.read_lockfile(tmp_path)
        vrec = next(r for r in lock["files"] if r.get("verbatim"))
        forked = tmp_path / vrec["dst"]
        forked.write_text(forked.read_text() + "\n# adopter fork\n")
        assert s.main(["upgrade", "--finalize", "--target", str(tmp_path),
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        lock2 = s.read_lockfile(tmp_path)
        vrec2 = next(r for r in lock2["files"] if r["dst"] == vrec["dst"])
        # hash advanced to the fork; base_hash still the as-shipped baseline.
        assert vrec2["hash"] == "sha256:" + s._sha256_hex(forked.read_bytes())
        assert vrec2.get("base_hash") and vrec2["base_hash"] != vrec2["hash"]
        # Fork detection survives: the next upgrade sees a local modification.
        plans, _ = s._compute_upgrade(
            tmp_path, CAIRN_ROOT, TEMPLATES_ROOT, lock2, to_ref=None)
        p = next(x for x in plans if x.dst == vrec["dst"])
        assert p.kind == "verbatim-locally-modified", (
            f"forked verbatim script should stay locally-modified; got {p.kind!r}"
        )

    def test_renamed_wrapper_apply_advances_to_resolved_dst(
        self, tmp_path: Path
    ) -> None:
        """A renamed-wrapper adopter
        (``VENDOR.md -> CLAUDE.md``) that stages and applies an upgrade must
        have its wrapper record advanced to the real on-disk dst (CLAUDE.md),
        not left dangling at VENDOR.md.  Without the apply-time heal,
        ``verify_integrity`` after ``--apply`` fails on the missing VENDOR.md."""
        from bootstrap.verify_integrity import verify

        assert _install(tmp_path) == 0
        (tmp_path / "VENDOR.md").rename(tmp_path / "CLAUDE.md")  # adopter rename
        self._diverge_base(tmp_path)  # give the upgrade something to stage
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        assert s.main(["upgrade", "--target", str(tmp_path), "--apply",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        lock = s.read_lockfile(tmp_path)
        dsts = {r["dst"] for r in lock["files"]}
        assert "CLAUDE.md" in dsts and "VENDOR.md" not in dsts, (
            "apply should resolve the wrapper record to its on-disk dst"
        )
        assert verify(tmp_path) == 0

    def test_plan_summary_shows_distinct_labels(
        self, tmp_path: Path, capsys
    ) -> None:
        """The `--plan` report uses the adopter-facing display labels:
        `clean (untouched)` and `locally-modified (merged clean)` --
        not the internal kind strings.
        """
        assert _install(tmp_path) == 0
        self._diverge_base(tmp_path)
        rc = s.main(["upgrade", "--target", str(tmp_path), "--plan",
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 0
        out = capsys.readouterr().out
        # The adopter-facing label, not the internal kind:
        assert "locally-modified (merged clean)" in out, (
            f"adopter-facing label missing from --plan summary; got:\n{out}"
        )
        # The internal kind string must NOT leak through the label layer.
        assert "clean-locally-modified " not in out, (
            "internal kind string leaked into adopter-facing summary"
        )

    def test_to_ref_requires_git_source(self, tmp_path: Path, monkeypatch) -> None:
        assert _install(tmp_path) == 0
        # _cairn_is_git is owned by the upgrade submodule (scaffold-split Stage 7);
        # cmd_upgrade reads it from there, so patch it at its owning module object --
        # the facade re-export is a separate binding that the internal caller no
        # longer observes once the symbol has been extracted out of the engine
        # __init__. (Patch the module object, not a dotted string: the launcher
        # aliases bootstrap.scaffold, so `bootstrap._scaffold` is not a plain
        # attribute of `bootstrap` for pytest's string-path walk.)
        from bootstrap._scaffold import upgrade as _up  # noqa: PLC0415
        monkeypatch.setattr(_up, "_cairn_is_git", lambda root: False)
        rc = s.main(["upgrade", "--target", str(tmp_path), "--plan",
                     "--to", "v0.1.0", "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 1  # packaged source can't --to a ref

    def test_no_lockfile_directs_to_init(self, tmp_path: Path) -> None:
        (tmp_path / "dev").mkdir()
        rc = s.main(["upgrade", "--target", str(tmp_path), "--plan",
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 1  # no lockfile

    def test_structural_new_modules(self, tmp_path: Path, capsys) -> None:
        assert _install(tmp_path) == 0   # solo-greenfield: minimal roster
        s.main(["upgrade", "--target", str(tmp_path), "--plan",
                "--cairn-root", str(CAIRN_ROOT)])
        out = capsys.readouterr().out
        assert "new modules available" in out

    def test_slot_removed_is_not_staged(self, tmp_path: Path) -> None:
        """A slot-removed (or any non-advancing) file is never staged,
        so it can never be applied."""
        assert _install(tmp_path) == 0
        # ours fills a slot; the cached base has the slot; upstream (current
        # template) for this file is forced to have the slot removed by
        # blanking the base cache differently -> simulate via a fake file:
        # use AGENTS.md, give ours a fabricated slot the template lacks.
        base = tmp_path / "dev" / ".cairn" / "base" / "AGENTS.md"
        base.write_text(base.read_text()
                        + "\n<!-- cairn:slot zzz -->\nB\n<!-- cairn:end zzz -->\n")
        lock = s.read_lockfile(tmp_path)
        rec = next(r for r in lock["files"] if r["dst"] == "AGENTS.md")
        rec["base_hash"] = "sha256:" + s._sha256_hex(base.read_bytes())
        (tmp_path / "dev" / ".cairn" / "cairn-lock.yml").write_text(
            s._emit_lock_yaml(lock), encoding="utf-8")
        a = tmp_path / "AGENTS.md"
        a.write_text(a.read_text()
                     + "\n<!-- cairn:slot zzz -->\nMINE\n<!-- cairn:end zzz -->\n")
        # current upstream AGENTS.md has no `zzz` slot -> slot-removed.
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        staged = tmp_path / "dev" / ".cairn-upgrade" / "files" / "AGENTS.md"
        assert not staged.exists()  # slot-removed not staged

    def test_apply_rejects_corrupt_stage(self, tmp_path: Path) -> None:
        """The on-disk staged set must equal the stage manifest."""
        assert _install(tmp_path) == 0
        self._diverge_base(tmp_path)
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        # inject an extra file not in the manifest
        extra = tmp_path / "dev" / ".cairn-upgrade" / "files" / "dev" / "README.md"
        extra.parent.mkdir(parents=True, exist_ok=True)
        extra.write_text("rogue\n")
        rc = s.main(["upgrade", "--target", str(tmp_path), "--apply",
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 1  # exact-set mismatch -> refused

    def test_apply_accepts_windows_filesystem_path_rendering(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        assert _install(tmp_path) == 0
        self._diverge_base(tmp_path)
        lock = s.read_lockfile(tmp_path)
        nested = next(r for r in lock["files"] if r["dst"] == "dev/agent_collaboration.md")
        for name in (nested["base_cache"], nested["dst"]):
            path = tmp_path / name
            path.write_bytes(b"# old prefix\n" + path.read_bytes())
        nested["base_hash"] = "sha256:" + s._sha256_hex(
            (tmp_path / nested["base_cache"]).read_bytes())
        (tmp_path / s._LOCKFILE_REL).write_text(s._emit_lock_yaml(lock), encoding="utf-8")
        args = ["upgrade", "--target", str(tmp_path),
                "--cairn-root", str(CAIRN_ROOT)]
        assert s.main(args + ["--stage"]) == 0
        files = tmp_path.resolve() / s._STAGING_REL / "files"
        relative_to = Path.relative_to
        observed = []

        def windows_relative(path, *other, **kwargs):
            relative = relative_to(path, *other, **kwargs)
            if other == (files,):
                observed.append(relative.as_posix())
                return PureWindowsPath(relative.as_posix())
            return relative

        monkeypatch.setattr(Path, "relative_to", windows_relative)
        assert s.main(args + ["--apply"]) == 0
        assert observed and any("/" in name for name in observed)
        assert "keep me" in (tmp_path / "AGENTS.md").read_text(encoding="utf-8")

    @pytest.mark.parametrize("change", ["missing", "literal-backslash", "metadata"])
    def test_apply_keeps_path_and_exact_set_refusals(
        self, tmp_path: Path, change: str
    ) -> None:
        assert _install(tmp_path) == 0
        self._diverge_base(tmp_path)
        args = ["upgrade", "--target", str(tmp_path),
                "--cairn-root", str(CAIRN_ROOT)]
        assert s.main(args + ["--stage"]) == 0
        stage = tmp_path / s._STAGING_REL
        lock_before = (tmp_path / s._LOCKFILE_REL).read_bytes()
        original = (tmp_path / "AGENTS.md").read_bytes()
        if change == "missing":
            (stage / "files" / "AGENTS.md").unlink()
        elif change == "literal-backslash":
            rogue = stage / "files" / "dev\\rogue.md"
            rogue.parent.mkdir(parents=True, exist_ok=True)
            rogue.write_bytes(b"not a manifest entry\n")
        else:
            meta_path = stage / "stage-metadata.json"
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            meta["staged_files"].append("dev\\..\\rogue.md")
            meta_path.write_text(json.dumps(meta), encoding="utf-8")
        assert s.main(args + ["--apply"]) != 0
        assert (tmp_path / "AGENTS.md").read_bytes() == original
        assert (tmp_path / s._LOCKFILE_REL).read_bytes() == lock_before

    @pytest.mark.parametrize("kind,name", [
        ("review-only", "dev/notes.md"), ("clean", "dev/\u8bb0\u5f55.md"),
    ])
    def test_upgrade_report_supports_legacy_console_encoding(self, kind, name):
        from contextlib import redirect_stdout
        from bootstrap._scaffold.upgrade import FilePlan, _print_upgrade_report

        raw = io.BytesIO()
        console = io.TextIOWrapper(raw, encoding="cp1252", errors="strict")
        plan = FilePlan(name, kind, None, "review this", None, None)
        with redirect_stdout(console):
            _print_upgrade_report([plan], {"new_modules": [], "removed_modules": []},
                                  None, mode="stage")
        console.flush()
        text = raw.getvalue().decode("cp1252")
        assert ascii(name)[1:-1] in text
        assert plan.dst == name

    def test_discovery_records_use_windows_posix_keys(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        from bootstrap._scaffold.upgrade import _record_discovery_outputs

        target = tmp_path.resolve()
        names = ["dev/PLANNING.md", "dev/modules/README.md"]
        lock = {"files": [{"dst": name, "hash": "old"} for name in names]}
        updates = [(target / name, name.encode("utf-8")) for name in names]
        relative_to = Path.relative_to

        def windows_relative(path, *other, **kwargs):
            relative = relative_to(path, *other, **kwargs)
            return (PureWindowsPath(relative.as_posix())
                    if other == (target,) else relative)

        monkeypatch.setattr(Path, "relative_to", windows_relative)
        _record_discovery_outputs(target, TEMPLATES_ROOT, lock, updates, [])
        assert {rec["dst"] for rec in lock["files"]} == set(names)
        for rec in lock["files"]:
            assert rec["hash"] == "sha256:" + s._sha256_hex(rec["dst"].encode("utf-8"))


# ---------------------------------------------------------------------------
# --init-lock migration
# ---------------------------------------------------------------------------

class TestInitLock:
    def test_migrates_and_marks_unrecoverable(self, tmp_path: Path) -> None:
        assert _install(tmp_path) == 0
        # simulate a pre-lockfile tree
        (tmp_path / "dev" / ".cairn" / "cairn-lock.yml").unlink()
        import shutil
        shutil.rmtree(tmp_path / "dev" / ".cairn")
        _seed_profile(tmp_path)
        rc = s.main(["upgrade", "--target", str(tmp_path), "--init-lock",
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 0
        lock = s.read_lockfile(tmp_path)
        assert lock["migrated"] is True
        # token-substituted files are marked unrecoverable (no base cache)
        md = [r for r in lock["files"] if not r["verbatim"]]
        assert md and all(r.get("unrecoverable_base") for r in md)

    def test_init_lock_then_plan_is_review_only(self, tmp_path: Path, capsys) -> None:
        assert _install(tmp_path) == 0
        (tmp_path / "dev" / ".cairn" / "cairn-lock.yml").unlink()
        import shutil
        shutil.rmtree(tmp_path / "dev" / ".cairn")
        _seed_profile(tmp_path)
        s.main(["upgrade", "--target", str(tmp_path), "--init-lock",
                "--cairn-root", str(CAIRN_ROOT)])
        capsys.readouterr()
        s.main(["upgrade", "--target", str(tmp_path), "--plan",
                "--cairn-root", str(CAIRN_ROOT)])
        out = capsys.readouterr().out
        assert "review-only" in out  # no pretended 3-way merge

    def test_migration_note_never_advises_reinstalling_over_the_tree(
        self, tmp_path: Path, capsys
    ) -> None:
        """The note printed after a migration must point at the merge, not
        at a re-install.  A re-install over an existing tree skips every file
        already there and writes no lockfile, and ``--force`` overwrites the
        adopter's own edits -- so advising one sends the adopter nowhere, or
        into data loss."""
        assert _install(tmp_path) == 0
        (tmp_path / "dev" / ".cairn" / "cairn-lock.yml").unlink()
        import shutil
        shutil.rmtree(tmp_path / "dev" / ".cairn")
        _seed_profile(tmp_path)
        capsys.readouterr()
        assert s.main(["upgrade", "--target", str(tmp_path), "--init-lock",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        out = capsys.readouterr().out
        assert "review-only" in out  # the note itself is still printed
        assert not re.search(r"re-?install", out, re.IGNORECASE)
        assert "--stage" in out  # names the step that does the merge

    def test_install_over_a_migrated_tree_points_at_upgrade_not_init_lock(
        self, tmp_path: Path, capsys
    ) -> None:
        """An install that declines to write a lockfile must not send the
        adopter to ``--init-lock`` when the tree already has one: that command
        answers "already exists" and does nothing, a loop with no exit.  The
        existing lockfile is kept, and ``upgrade`` is the way forward."""
        assert _install(tmp_path) == 0
        (tmp_path / "dev" / ".cairn" / "cairn-lock.yml").unlink()
        import shutil
        shutil.rmtree(tmp_path / "dev" / ".cairn")
        _seed_profile(tmp_path)
        assert s.main(["upgrade", "--target", str(tmp_path), "--init-lock",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        lock_path = tmp_path / "dev" / ".cairn" / "cairn-lock.yml"
        before = lock_path.read_bytes()
        agents = tmp_path / "AGENTS.md"
        agents.write_text(agents.read_text() + "\nAn adopter's own line.\n")
        capsys.readouterr()
        assert _install(tmp_path) == 0
        err = capsys.readouterr().err
        warning = next(line for line in err.splitlines() if "NOT written" in line)
        assert "--init-lock" not in warning
        assert "upgrade" in warning and "--plan" in warning
        assert lock_path.read_bytes() == before  # the migrated lockfile is kept

    def test_review_pairs_leave_no_placeholder_the_install_filled(
        self, tmp_path: Path,
    ) -> None:
        """A review-only pair is for spotting what changed, so ``.theirs``
        carries the tokens an install of this profile fills.  On a migrated
        tree nobody has edited, every ``{{token}}`` left in a ``.theirs`` must
        therefore also be in its ``.ours`` -- a template-only placeholder such
        as ``{{author}}`` stays on both sides; one the install filled would
        read as a change the adopter never made."""
        assert _install(tmp_path) == 0
        (tmp_path / "dev" / ".cairn" / "cairn-lock.yml").unlink()
        import shutil
        shutil.rmtree(tmp_path / "dev" / ".cairn")
        _seed_profile(tmp_path)
        assert s.main(["upgrade", "--target", str(tmp_path), "--init-lock",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        review = tmp_path / "dev" / ".cairn-upgrade" / "review-only"
        pairs = [(th, th.with_name(th.name[:-len(".theirs")] + ".ours"))
                 for th in sorted(review.rglob("*.theirs"))]
        pairs = [(th, ours) for th, ours in pairs if ours.exists()]
        assert pairs, "the migrated tree staged no review pairs"
        placeholder = re.compile(r"\{\{[a-z_]+\}\}")
        unfilled = {
            str(th.relative_to(review)): sorted(extra)
            for th, ours in pairs
            if (extra := set(placeholder.findall(th.read_text(encoding="utf-8")))
                - set(placeholder.findall(ours.read_text(encoding="utf-8"))))
        }
        assert unfilled == {}, unfilled
        # Outside slot bodies and the independently rendered inventory block,
        # the two sides are byte-equal: tokens, sizing and markers all match.
        slot_body = re.compile(
            r"(<!-- cairn:slot (\S+) -->).*?(<!-- cairn:end \2 -->)", re.S)
        inventory_body = re.compile(
            r"(<!-- cairn:generated-modules:start -->).*?"
            r"(<!-- cairn:generated-modules:end -->)", re.S)
        def outside_slots(path: Path) -> str:
            text = slot_body.sub(r"\1\3", path.read_text(encoding="utf-8"))
            return inventory_body.sub(r"\1\2", text)
        differing = [str(th.relative_to(review)) for th, ours in pairs
                     if outside_slots(th) != outside_slots(ours)]
        assert differing == [], differing
        inventory_theirs = (review / "dev/modules/README.md.theirs").read_text()
        installed_modules = s.read_lockfile(tmp_path)["modules"]
        assert [line for line in inventory_theirs.splitlines()
                if line.startswith("<!-- cairn:module id=")] == [
                    f"<!-- cairn:module id={name} -->"
                    for name in installed_modules]

    def _migrate(self, target: Path, *profile_lines: str) -> Path:
        """Install, drop the lockfile, and migrate with the given extra
        profile lines; return where ``--stage`` writes the review pairs."""
        assert _install(target) == 0
        import shutil
        shutil.rmtree(target / "dev" / ".cairn")
        prof = _seed_profile(target)
        if profile_lines:
            prof.write_text(prof.read_text() + "\n".join(profile_lines) + "\n")
        assert s.main(["upgrade", "--target", str(target), "--init-lock",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        return target / "dev" / ".cairn-upgrade" / "review-only"

    def _inventory_review_case(self, target: Path, modules: list[str]) -> tuple[Path, bytes, dict[str, bytes]]:
        review = self._migrate(target)
        lock_path = target / "dev" / ".cairn" / "cairn-lock.yml"
        lock = s.read_lockfile(target)
        lock["modules"] = modules
        lock_path.write_text(s._emit_lock_yaml(lock), encoding="utf-8")
        inventory = target / "dev" / "modules" / "README.md"
        inventory.write_text(inventory.read_text() + "\nlocal inventory note\n",
                             encoding="utf-8")
        rec = next(r for r in lock["files"]
                   if r["dst"] == "dev/modules/README.md")
        ancestor_bytes = {str(path.relative_to(target)): path.read_bytes()
                          for path in (target / "dev/.cairn/base").rglob("*")
                          if path.is_file()}
        return review, inventory.read_bytes(), ancestor_bytes

    @pytest.mark.parametrize("modules, expected", [
        (["security-review", "coordination-tiers"],
         ["<!-- cairn:module id=security-review -->",
          "<!-- cairn:module id=coordination-tiers -->"]),
        ([], []),
    ])
    def test_review_inventory_renders_selected_roster_from_current_source(
        self, tmp_path: Path, modules: list[str], expected: list[str],
    ) -> None:
        review, installed_before, _ancestors_before = self._inventory_review_case(
            tmp_path, modules)
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        theirs = (review / "dev/modules/README.md.theirs").read_text()
        ours = (review / "dev/modules/README.md.ours").read_bytes()
        assert [line for line in theirs.splitlines()
                if line.startswith("<!-- cairn:module id=")] == expected
        assert "local inventory note" not in theirs
        assert "local inventory note" in ours.decode()
        assert (tmp_path / "dev/modules/README.md").read_bytes() == installed_before
        for rel, raw in _ancestors_before.items():
            assert (tmp_path / rel).read_bytes() == raw

    def test_review_inventory_theirs_excludes_local_edit_when_roster_matches(
        self, tmp_path: Path,
    ) -> None:
        review = self._migrate(tmp_path)
        modules = s.read_lockfile(tmp_path)["modules"]
        inventory = tmp_path / "dev/modules/README.md"
        inventory.write_text(inventory.read_text() + "\nprivate local note\n",
                             encoding="utf-8")
        installed_before = inventory.read_bytes()
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        ours = (review / "dev/modules/README.md.ours").read_text()
        theirs = (review / "dev/modules/README.md.theirs").read_text()
        assert "private local note" in ours
        assert "private local note" not in theirs
        assert [line for line in theirs.splitlines()
                if line.startswith("<!-- cairn:module id=")] == [
                    f"<!-- cairn:module id={name} -->" for name in modules]
        assert inventory.read_bytes() == installed_before

    def test_missing_installed_inventory_has_no_ours_pair(
        self, tmp_path: Path,
    ) -> None:
        review, _installed, _ancestors = self._inventory_review_case(
            tmp_path, ["security-review"])
        inventory = tmp_path / "dev/modules/README.md"
        inventory.unlink()
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        theirs = review / "dev/modules/README.md.theirs"
        ours = review / "dev/modules/README.md.ours"
        assert theirs.is_file()
        assert "<!-- cairn:module id=security-review -->" in theirs.read_text()
        assert not ours.exists()
        assert not inventory.exists()

    def test_duplicate_upstream_inventory_entries_refuse_and_clean_stage(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys,
    ) -> None:
        review, installed_before, ancestors_before = self._inventory_review_case(
            tmp_path, ["security-review"])
        source = TEMPLATES_ROOT / "core/dev/modules/README.md"
        original = source.read_text(encoding="utf-8")
        from bootstrap._scaffold.install import _render_module_inventory
        duplicate = _render_module_inventory(["security-review"])
        malformed = original.replace(
            "<!-- cairn:generated-modules:end -->",
            duplicate + "\n" + duplicate + "\n"
            "<!-- cairn:generated-modules:end -->")
        from bootstrap._scaffold import upgrade as _up
        read_bytes = _up._theirs_bytes
        monkeypatch.setattr(
            _up, "_theirs_bytes",
            lambda root, templates, rel, to_ref: (
                malformed.encode("utf-8")
                if rel == "core/dev/modules/README.md"
                else read_bytes(root, templates, rel, to_ref)),
        )
        stage = tmp_path / "dev/.cairn-upgrade"
        stage.mkdir(parents=True)
        (stage / "stale-marker").write_text("previous stage")
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 2
        assert "duplicate" in capsys.readouterr().err.lower()
        assert not stage.exists()
        assert (tmp_path / "dev/modules/README.md").read_bytes() == installed_before
        for rel, raw in ancestors_before.items():
            assert (tmp_path / rel).read_bytes() == raw
        assert not (review / "dev/modules/README.md.theirs").exists()

    @pytest.mark.parametrize("malformation", [
        "missing-template", "missing-generated", "duplicate-generated", "nested-entry",
        "unmatched-entry", "entry-outside-generated",
    ])
    def test_malformed_upstream_inventory_refuses_without_partial_stage(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, malformation: str,
    ) -> None:
        review, installed_before, ancestors_before = self._inventory_review_case(
            tmp_path, ["security-review"])
        source = TEMPLATES_ROOT / "core/dev/modules/README.md"
        original = source.read_text()
        if malformation in ("missing-template", "missing-generated"):
            malformed = original.replace(
                "<!-- cairn:generated-modules:start -->\n", "")
        elif malformation == "duplicate-generated":
            malformed = original.replace(
                "<!-- cairn:generated-modules:start -->",
                "<!-- cairn:generated-modules:start -->\n<!-- cairn:generated-modules:start -->")
        elif malformation == "nested-entry":
            malformed = original.replace(
                "<!-- cairn:generated-modules:end -->",
                "<!-- cairn:module id=security-review -->\n"
                "<!-- cairn:module id=coordination-tiers -->\n"
                "<!-- cairn:module-end id=coordination-tiers -->\n"
                "<!-- cairn:module-end id=security-review -->\n"
                "<!-- cairn:generated-modules:end -->")
        elif malformation == "entry-outside-generated":
            malformed = original.replace(
                "<!-- cairn:generated-modules:end -->",
                "<!-- cairn:generated-modules:end -->\n"
                "<!-- cairn:module id=security-review -->\n"
                "<!-- cairn:module-end id=security-review -->")
        else:
            malformed = original.replace(
                "<!-- cairn:generated-modules:end -->",
                "<!-- cairn:module id=security-review -->\n"
                "<!-- cairn:generated-modules:end -->")
        # The source tree is shared with the running test process; supply the
        # malformed selected bytes at the renderer's real source-read boundary.
        from bootstrap._scaffold import upgrade as _up
        read_bytes = _up._theirs_bytes
        monkeypatch.setattr(
            _up, "_theirs_bytes",
            lambda root, templates, rel, to_ref: (
                (None if malformation == "missing-template" else malformed.encode())
                if rel == "core/dev/modules/README.md"
                else read_bytes(root, templates, rel, to_ref)),
        )
        stage = tmp_path / "dev/.cairn-upgrade"
        stage.mkdir(parents=True)
        (stage / "stale-marker").write_text("previous stage")
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 2
        assert not stage.exists()
        assert (tmp_path / "dev/modules/README.md").read_bytes() == installed_before
        for rel, raw in ancestors_before.items():
            if (tmp_path / rel).exists():
                assert (tmp_path / rel).read_bytes() == raw

    def test_unknown_inventory_member_refuses_stage(self, tmp_path: Path) -> None:
        review = self._migrate(tmp_path)
        lock_path = tmp_path / "dev/.cairn/cairn-lock.yml"
        lock = s.read_lockfile(tmp_path)
        lock["modules"] = ["made-up-module"]
        lock_path.write_text(s._emit_lock_yaml(lock), encoding="utf-8")
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 2
        assert not (tmp_path / "dev/.cairn-upgrade").exists()

    def test_matching_historical_renderer_stages_inventory(self, tmp_path: Path) -> None:
        review, _installed, _ancestors = self._inventory_review_case(
            tmp_path, ["security-review"])
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--to", "HEAD", "--cairn-root", str(CAIRN_ROOT)]) == 0
        theirs = (review / "dev/modules/README.md.theirs").read_text()
        assert "<!-- cairn:module id=security-review -->" in theirs
        assert "**security-review**" in theirs

    def test_historical_inventory_description_is_used_for_theirs(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        review, _installed, _ancestors = self._inventory_review_case(
            tmp_path, ["security-review"])
        from bootstrap._scaffold import upgrade as _up
        helper = _up._git_read_helper()
        real_run_git = helper.run_git
        from bootstrap._scaffold.install import _render_module_inventory
        entry = _render_module_inventory(["security-review"]).replace(
            "Identify trust boundaries that may need review.",
            "Historical description.")
        historical = (
            "# Modules\n\n<!-- cairn:generated-modules:start -->\n"
            + entry + "\n<!-- cairn:generated-modules:end -->\n")

        def historical_description(target, args, **kwargs):
            if (args[0] == "show"
                    and args[1].endswith(":templates/core/dev/modules/README.md")):
                return helper.ReadResult("completed", 0, historical.encode())
            return real_run_git(target, args, **kwargs)

        monkeypatch.setattr(helper, "run_git", historical_description)
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--to", "HEAD", "--cairn-root", str(CAIRN_ROOT)]) == 0
        theirs = (review / "dev/modules/README.md.theirs").read_text()
        assert "Historical description." in theirs

    def test_changed_historical_renderer_refuses_and_cleans_stage(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        _review, installed_before, ancestors_before = self._inventory_review_case(
            tmp_path, ["security-review"])
        from bootstrap._scaffold import upgrade as _up
        helper = _up._git_read_helper()
        real_run_git = helper.run_git

        def changed_renderer(target, args, **kwargs):
            if (args[0] == "show"
                    and args[1].endswith(":bootstrap/_scaffold/install.py")):
                return helper.ReadResult("completed", 0, b"changed renderer")
            return real_run_git(target, args, **kwargs)

        monkeypatch.setattr(helper, "run_git", changed_renderer)
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--to", "HEAD", "--cairn-root", str(CAIRN_ROOT)]) == 2
        assert not (tmp_path / "dev/.cairn-upgrade").exists()
        assert (tmp_path / "dev/modules/README.md").read_bytes() == installed_before
        for rel, raw in ancestors_before.items():
            path = tmp_path / rel
            if path.exists():
                assert path.read_bytes() == raw

    def test_changed_historical_metadata_refuses_and_cleans_stage(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        self._inventory_review_case(tmp_path, ["security-review"])
        from bootstrap._scaffold import upgrade as _up
        helper = _up._git_read_helper()
        real_run_git = helper.run_git

        def changed_metadata(target, args, **kwargs):
            if (args[0] == "show"
                    and args[1].endswith(":bootstrap/_scaffold/config.py")):
                return helper.ReadResult("completed", 0, b"changed metadata")
            return real_run_git(target, args, **kwargs)

        monkeypatch.setattr(helper, "run_git", changed_metadata)
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--to", "HEAD", "--cairn-root", str(CAIRN_ROOT)]) == 2
        assert not (tmp_path / "dev/.cairn-upgrade").exists()

    def test_review_copy_keeps_a_profile_supplied_command_token(
        self, tmp_path: Path,
    ) -> None:
        """The install's reference-script default fills a command token only
        when the profile left it empty; the review copy must do the same, or
        an adopter's own invocation reads as an upstream change."""
        review = self._migrate(
            tmp_path, 'claim_check_command: "make claims"')
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        theirs = (review / "dev" / "modules" / "claim-check.md.theirs").read_text()
        assert "make claims" in theirs
        assert "{{claim_check_command}}" not in theirs

    def test_review_copy_uses_profile_neutral_core_template(
        self, tmp_path: Path,
    ) -> None:
        """A human-team profile change does not remove shared core rules from
        a migrated install's upstream review copy."""
        review = self._migrate(tmp_path)
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        solo_theirs = (review / "AGENTS.md.theirs").read_text()
        prof = tmp_path / "dev" / ".cairn" / "profile.yml"
        prof.write_text(prof.read_text().replace(
            "human_team: solo", "human_team: small-multi"))
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        theirs = (review / "AGENTS.md.theirs").read_text()
        assert theirs == solo_theirs
        assert "cairn:if" not in theirs and "cairn:endif" not in theirs

    def test_install_without_a_readable_lockfile_points_at_init_lock(
        self, tmp_path: Path, capsys
    ) -> None:
        """With no lockfile, or one that does not parse, --init-lock is the
        command that works, so that is what the warning names."""
        assert _install(tmp_path) == 0
        agents = tmp_path / "AGENTS.md"
        agents.write_text(agents.read_text() + "\nAn adopter's own line.\n")
        lock_path = tmp_path / "dev" / ".cairn" / "cairn-lock.yml"
        for state in ("absent", "unparseable"):
            if state == "absent":
                lock_path.unlink()
            else:
                lock_path.write_text("this is not a lockfile\n")
            capsys.readouterr()
            assert _install(tmp_path) == 0
            err = capsys.readouterr().err
            warning = next(line for line in err.splitlines()
                           if "NOT written" in line)
            assert "--init-lock" in warning, (state, warning)
            assert "--plan" not in warning, (state, warning)

    def test_init_lock_follows_vendor_rename(self, tmp_path: Path) -> None:
        """#45: a renamed vendor wrapper (VENDOR.md -> CLAUDE.md) is resolved
        and tracked under its real dst, not dropped to untracked."""
        assert _install(tmp_path) == 0
        (tmp_path / "VENDOR.md").rename(tmp_path / "CLAUDE.md")  # adopter rename
        (tmp_path / "dev" / ".cairn" / "cairn-lock.yml").unlink()
        import shutil
        shutil.rmtree(tmp_path / "dev" / ".cairn")
        _seed_profile(tmp_path)
        assert s.main(["upgrade", "--target", str(tmp_path), "--init-lock",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        lock = s.read_lockfile(tmp_path)
        dsts = {r["dst"] for r in lock["files"]}
        assert "CLAUDE.md" in dsts and "VENDOR.md" not in dsts
        rec = next(r for r in lock["files"] if r["dst"] == "CLAUDE.md")
        assert rec["src"] == "core/VENDOR.md" and rec.get("unrecoverable_base")

    def test_init_lock_warns_on_unresolvable_wrapper(
        self, tmp_path: Path, capsys
    ) -> None:
        """#45: with no resolvable wrapper, warn (do not silently skip) and
        never record a wrong file."""
        assert _install(tmp_path) == 0
        (tmp_path / "VENDOR.md").unlink()  # gone; no rename, no known wrapper
        (tmp_path / "dev" / ".cairn" / "cairn-lock.yml").unlink()
        import shutil
        shutil.rmtree(tmp_path / "dev" / ".cairn")
        _seed_profile(tmp_path)
        capsys.readouterr()
        assert s.main(["upgrade", "--target", str(tmp_path), "--init-lock",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        err = capsys.readouterr().err
        assert "vendor wrapper" in err and "untracked" in err
        dsts = {r["dst"] for r in s.read_lockfile(tmp_path)["files"]}
        assert "VENDOR.md" not in dsts
        assert not (dsts & set(s._KNOWN_VENDOR_WRAPPERS))  # no wrong-file record

    def test_untracked_wrapper_warning_gives_a_recovery_that_works(
        self, tmp_path: Path, capsys
    ) -> None:
        """Following the warning's own advice must end with the wrapper
        tracked.  The lockfile is written in the same run that warns, and
        --init-lock refuses once one exists, so renaming alone cannot work;
        a re-install over the tree writes no lockfile at all."""
        assert _install(tmp_path) == 0
        (tmp_path / "VENDOR.md").unlink()
        (tmp_path / "dev" / ".cairn" / "cairn-lock.yml").unlink()
        import shutil
        shutil.rmtree(tmp_path / "dev" / ".cairn")
        _seed_profile(tmp_path)
        capsys.readouterr()
        assert s.main(["upgrade", "--target", str(tmp_path), "--init-lock",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        err = capsys.readouterr().err
        assert not re.search(r"re-?install", err, re.IGNORECASE)
        assert "delete dev/.cairn/cairn-lock.yml" in err
        # Do what it says: put the wrapper at a known name, drop the lockfile
        # that run wrote, and migrate again.
        wrapper = sorted(s._KNOWN_VENDOR_WRAPPERS)[0]
        (tmp_path / wrapper).write_text(
            (CAIRN_ROOT / "templates" / "core" / "VENDOR.md").read_text())
        (tmp_path / "dev" / ".cairn" / "cairn-lock.yml").unlink()
        assert s.main(["upgrade", "--target", str(tmp_path), "--init-lock",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        dsts = {r["dst"] for r in s.read_lockfile(tmp_path)["files"]}
        assert wrapper in dsts


class TestInitLockFullProfile:
    """init-lock-full-profile: init-lock embeds the **full six-axis**
    profile (fail-with-template when no config; validate axes against `_AXES`) and
    recovers `cairn_commit` from the `dev/.cairn/` manifest home (legacy
    `dev/strategy/` fallback)."""

    def _prelock(self, tmp_path: Path) -> None:
        assert _install(tmp_path) == 0
        import shutil
        shutil.rmtree(tmp_path / "dev" / ".cairn")  # simulate a pre-lockfile tree

    def test_no_config_writes_template_and_fails(self, tmp_path: Path) -> None:
        """No committed config -> prefill template + fail loud, no
        lockfile."""
        self._prelock(tmp_path)
        rc = s.main(["upgrade", "--target", str(tmp_path), "--init-lock",
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc != 0
        assert s.read_lockfile(tmp_path) is None  # no lockfile written
        prof = (tmp_path / "dev" / ".cairn" / "profile.yml").read_text()
        assert "<small|medium|large>" in prof       # size placeholder surfaced
        assert "age: greenfield" in prof            # inferred (no legacy-agent.md)
        assert "agent_team: single" in prof         # inferred

    def test_with_config_embeds_full_profile(self, tmp_path: Path) -> None:
        """A complete config -> all six axes + tokens embedded."""
        self._prelock(tmp_path)
        _seed_profile(tmp_path, size="large", complexity="complex")
        assert s.main(["upgrade", "--target", str(tmp_path), "--init-lock",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        lock = s.read_lockfile(tmp_path)
        axes = lock["profile"]["axes"]
        assert set(axes) == set(s._AXES)            # all six, never a stub
        assert axes["size"] == "large" and axes["complexity"] == "complex"
        assert lock["tokens"]["project_name"] == "Demo"  # tokens recovered

    def test_incomplete_config_fails(self, tmp_path: Path, capsys) -> None:
        self._prelock(tmp_path)
        (tmp_path / "dev" / ".cairn").mkdir(parents=True, exist_ok=True)
        (tmp_path / "dev" / ".cairn" / "profile.yml").write_text(
            'project_name: "Demo"\ntest_command: "pytest"\nage: greenfield\n')
        rc = s.main(["upgrade", "--target", str(tmp_path), "--init-lock",
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 1 and s.read_lockfile(tmp_path) is None
        assert "missing axis" in capsys.readouterr().err

    def test_invalid_axis_value_fails(self, tmp_path: Path, capsys) -> None:
        """A value outside `_AXES` is rejected, not just a placeholder."""
        self._prelock(tmp_path)
        _seed_profile(tmp_path, size="enormous")    # not in _AXES["size"]
        rc = s.main(["upgrade", "--target", str(tmp_path), "--init-lock",
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 1 and s.read_lockfile(tmp_path) is None
        assert "invalid axis" in capsys.readouterr().err

    def test_unfilled_placeholder_token_fails(self, tmp_path: Path, capsys) -> None:
        self._prelock(tmp_path)
        p = _seed_profile(tmp_path)
        p.write_text(p.read_text().replace('"Demo"', '"<your project name>"'))
        rc = s.main(["upgrade", "--target", str(tmp_path), "--init-lock",
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 1 and "placeholder" in capsys.readouterr().err

    def test_cairn_commit_from_cairn_home(self, tmp_path: Path) -> None:
        """cairn_commit recovered from a `dev/.cairn/` manifest."""
        self._prelock(tmp_path)
        _seed_profile(tmp_path)
        (tmp_path / "dev" / ".cairn" / "demo-fidelity-manifest.yml").write_text(
            'cairn_commit: "abc1234"\n')
        assert s.main(["upgrade", "--target", str(tmp_path), "--init-lock",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        assert s.read_lockfile(tmp_path)["cairn_commit"] == "abc1234"

    def test_cairn_commit_legacy_strategy_fallback(
        self, tmp_path: Path, capsys
    ) -> None:
        """Legacy `dev/strategy/` manifest still works, with a migration
        advisory."""
        self._prelock(tmp_path)
        _seed_profile(tmp_path)
        (tmp_path / "dev" / "strategy").mkdir(parents=True, exist_ok=True)
        (tmp_path / "dev" / "strategy" / "demo-fidelity-manifest.yml").write_text(
            'cairn_commit: "def5678"\n')
        assert s.main(["upgrade", "--target", str(tmp_path), "--init-lock",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        assert s.read_lockfile(tmp_path)["cairn_commit"] == "def5678"
        assert "legacy" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# #44 (cairn-upgrade-flow-hardening): review-only files owe a by-hand merge.
# The flow must surface them per-file, stage a theirs/ours review pair OUTSIDE
# files/, and fail-close --apply until they are reconciled.
# ---------------------------------------------------------------------------

class TestReviewOnlyMerge:
    def _init_locked(self, target: Path) -> None:
        """Install, then synthesize a migrated lockfile -- so every
        token-substituted file is unrecoverable-base -> review-only."""
        assert _install(target) == 0
        (target / "dev" / ".cairn" / "cairn-lock.yml").unlink()
        import shutil
        shutil.rmtree(target / "dev" / ".cairn")
        _seed_profile(target)
        assert s.main(["upgrade", "--target", str(target), "--init-lock",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0

    def _review_only_dst(self, target: Path) -> str:
        """A nested, non-verbatim (token-substituted) tracked file -> review-only
        after --init-lock.  Nested ('/') to exercise the parent-mkdir path."""
        lock = s.read_lockfile(target)
        nested = [r["dst"] for r in lock["files"]
                  if not r["verbatim"] and "/" in r["dst"]]
        assert nested, "expected a nested token-substituted file in the lockfile"
        return nested[0]

    def test_review_only_surfaced_per_file(self, tmp_path: Path, capsys) -> None:
        self._init_locked(tmp_path)
        dst = self._review_only_dst(tmp_path)
        capsys.readouterr()
        s.main(["upgrade", "--target", str(tmp_path), "--plan",
                "--cairn-root", str(CAIRN_ROOT)])
        out = capsys.readouterr().out
        assert "manual merge owed" in out      # the header, not just a count
        assert dst in out                       # surfaced PER FILE
        assert "--ack-review-only" in out       # the concrete next-step pointer

    def test_stage_writes_review_only_pair(self, tmp_path: Path) -> None:
        self._init_locked(tmp_path)
        dst = self._review_only_dst(tmp_path)
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        ro = tmp_path / "dev" / ".cairn-upgrade" / "review-only"
        assert (ro / (dst + ".theirs")).exists()   # new upstream
        assert (ro / (dst + ".ours")).exists()      # current on-disk copy
        # The pair lives OUTSIDE files/ so it cannot trip apply's exactness.
        files_dir = tmp_path / "dev" / ".cairn-upgrade" / "files"
        staged = ({str(p.relative_to(files_dir)) for p in files_dir.rglob("*")
                   if p.is_file()} if files_dir.exists() else set())
        assert dst not in staged

    def test_stage_review_only_file_missing_only_theirs(self, tmp_path: Path) -> None:
        """LHM's actual incident shape: a tracked file missing on disk (a
        default-on module slot that never installed).  Only ``.theirs`` is
        written -- there is no on-disk ``.ours`` to pair (
        second-read Finding 4)."""
        self._init_locked(tmp_path)
        dst = self._review_only_dst(tmp_path)
        (tmp_path / dst).unlink()                   # gone before --stage
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        ro = tmp_path / "dev" / ".cairn-upgrade" / "review-only"
        assert (ro / (dst + ".theirs")).exists()
        assert not (ro / (dst + ".ours")).exists()  # nothing on disk to pair
        lock = s.read_lockfile(tmp_path)
        plans, _ = s._compute_upgrade(tmp_path, CAIRN_ROOT, TEMPLATES_ROOT,
                                      lock, to_ref=None)
        fp = next(p for p in plans if p.dst == dst)
        assert fp.kind == "review-only" and "missing on disk" in fp.detail

    def test_apply_fail_closes_on_review_only(self, tmp_path: Path, capsys) -> None:
        """The #44 completion gate: --apply refuses to advance the lockfile
        while files still owe a by-hand merge (the exact LHM failure mode)."""
        self._init_locked(tmp_path)
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        capsys.readouterr()
        rc = s.main(["upgrade", "--target", str(tmp_path), "--apply",
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 1
        err = capsys.readouterr().err
        assert "not complete" in err and "--ack-review-only" in err
        # fail-closed: the stage is NOT consumed and the lockfile is untouched.
        assert (tmp_path / "dev" / ".cairn-upgrade").exists()

    def test_apply_ack_review_only_overrides_and_cleans(self, tmp_path: Path) -> None:
        """--ack-review-only is the explicit override: --apply proceeds and
        rmtree cleans the whole stage incl. review-only/."""
        self._init_locked(tmp_path)
        ro_dst = self._review_only_dst(tmp_path)
        lock_before = s.read_lockfile(tmp_path)
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        assert (tmp_path / "dev" / ".cairn-upgrade" / "review-only").exists()
        rc = s.main(["upgrade", "--target", str(tmp_path), "--apply",
                     "--ack-review-only", "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 0
        assert not (tmp_path / "dev" / ".cairn-upgrade").exists()  # incl. review-only/
        # the review-only file never advanced: its lockfile record is unchanged
        # (only advancing kinds recompute their hash on --apply).
        lock_after = s.read_lockfile(tmp_path)
        rec_before = next(r for r in lock_before["files"] if r["dst"] == ro_dst)
        rec_after = next(r for r in lock_after["files"] if r["dst"] == ro_dst)
        assert rec_after["hash"] == rec_before["hash"]



class TestAdoptModule:
    """`upgrade --adopt-module <name>` (#49): record an already-on-disk opt-in
    module into the lockfile so it 3-way-merges on later upgrades."""

    NAME = "architecture-review"  # team-gated, opt-in; not in solo-greenfield

    def test_adopt_installs_missing_and_records(self, tmp_path: Path) -> None:
        target = tmp_path.resolve()
        _install(target)
        assert self.NAME not in s.read_lockfile(target)["modules"]

        rc = s.main(["upgrade", "--target", str(target),
                     "--cairn-root", str(CAIRN_ROOT), "--adopt-module", self.NAME])
        assert rc == 0
        lock = s.read_lockfile(target)
        assert self.NAME in lock["modules"]
        dsts = {sp.dst for sp in s._MODULE_MAPPINGS[self.NAME]}
        recorded = {r["dst"]: r for r in lock["files"]}
        assert dsts <= set(recorded)
        for d in dsts:
            assert (target / d).is_file()           # installed from template
            rec = recorded[d]
            if not rec["verbatim"]:                 # mergeable -> base cache
                assert rec.get("base_cache")
                assert (target / rec["base_cache"]).is_file()
                assert rec.get("base_hash")

    def test_adopt_records_on_disk_content_not_template(self, tmp_path: Path) -> None:
        # The LHM scenario: the module's files are already on disk + customized.
        target = tmp_path.resolve()
        _install(target)
        s.main(["upgrade", "--target", str(target),
                "--cairn-root", str(CAIRN_ROOT), "--adopt-module", self.NAME])
        # Strip it back out (files stay on disk), then fill a file in place.
        lock = s.read_lockfile(target)
        dsts = {sp.dst for sp in s._MODULE_MAPPINGS[self.NAME]}
        lock["modules"] = [m for m in lock["modules"] if m != self.NAME]
        lock["files"] = [r for r in lock["files"] if r["dst"] not in dsts]
        (target / "dev" / ".cairn").mkdir(parents=True, exist_ok=True)
        (target / "dev" / ".cairn" / "cairn-lock.yml").write_text(
            s._emit_lock_yaml(lock), encoding="utf-8")
        victim = sorted(dsts)[0]
        (target / victim).write_text("ADOPTER-FILLED\n", encoding="utf-8")

        rc = s.main(["upgrade", "--target", str(target),
                     "--cairn-root", str(CAIRN_ROOT), "--adopt-module", self.NAME])
        assert rc == 0
        rec = next(r for r in s.read_lockfile(target)["files"]
                   if r["dst"] == victim)
        on_disk = "sha256:" + s._sha256_hex((target / victim).read_bytes())
        assert rec["hash"] == on_disk             # records the on-disk (filled) content
        # base cache is the RAW upstream template -- distinct from the fill, so a
        # 3-way merge later treats the fill as a local modification, not a fork.
        assert (target / rec["base_cache"]).read_text() != "ADOPTER-FILLED\n"

    def test_adopt_idempotent(self, tmp_path: Path) -> None:
        target = tmp_path.resolve()
        _install(target)
        for _ in range(2):
            rc = s.main(["upgrade", "--target", str(target),
                         "--cairn-root", str(CAIRN_ROOT),
                         "--adopt-module", self.NAME])
            assert rc == 0  # second run: already-recorded no-op
        assert s.read_lockfile(target)["modules"].count(self.NAME) == 1

    def test_adopt_unknown_module_fails_closed(self, tmp_path: Path) -> None:
        target = tmp_path.resolve()
        _install(target)
        rc = s.main(["upgrade", "--target", str(target), "--cairn-root",
                     str(CAIRN_ROOT), "--adopt-module", "no-such-module"])
        assert rc == 1

    # -- D1: required-token resolution (profile seed + lockfile authority,
    # the strict placeholder predicate, the secret-token guard) --------------

    #: `python-security` (not `architecture-review`): the one module with a
    #: declared required token (`_MODULE_REQUIRED_TOKENS`), so it is the
    #: right fixture for D1's token-resolution + refusal edge cases.
    TOKEN_NAME = "python-security"

    def test_adopt_required_token_absent_entirely_refuses_closed(
        self, tmp_path: Path,
    ) -> None:
        """No dev/.cairn/profile.yml AND no lockfile value: the required
        token resolves from nowhere -- refuse before any write or lockfile
        mutation (edge cases: no profile.yml; token absent)."""
        target = tmp_path.resolve()
        _install(target)
        before = s.read_lockfile(target)
        rc = s.main(["upgrade", "--target", str(target), "--cairn-root",
                     str(CAIRN_ROOT), "--adopt-module", self.TOKEN_NAME])
        assert rc == 2
        assert not (target / "scripts" / "run_security_audit.py").exists()
        assert not (target / "dev" / "modules" / "python-security.md").exists()
        assert s.read_lockfile(target) == before  # lockfile byte-for-byte unchanged

    def test_adopt_required_token_curly_placeholder_refuses_closed(
        self, tmp_path: Path,
    ) -> None:
        """A `{{...}}` placeholder value in the lockfile is unfilled, not a
        real value -- refuse (edge case: an unfilled placeholder, curly
        form)."""
        target = tmp_path.resolve()
        _install(target)
        lock = s.read_lockfile(target)
        lock["tokens"]["python_package"] = "{{python_package}}"
        (target / "dev" / ".cairn" / "cairn-lock.yml").write_text(
            s._emit_lock_yaml(lock), encoding="utf-8")
        before = s.read_lockfile(target)
        rc = s.main(["upgrade", "--target", str(target), "--cairn-root",
                     str(CAIRN_ROOT), "--adopt-module", self.TOKEN_NAME])
        assert rc == 2
        assert not (target / "scripts" / "run_security_audit.py").exists()
        assert s.read_lockfile(target) == before

    @pytest.mark.parametrize("value", ["", " ", "\t"])
    def test_adopt_required_token_blank_refuses_closed(
        self, tmp_path: Path, value: str,
    ) -> None:
        target = tmp_path.resolve()
        _install(target)
        lock = s.read_lockfile(target)
        lock["tokens"]["python_package"] = value
        lock_path = target / "dev/.cairn/cairn-lock.yml"
        lock_path.write_text(s._emit_lock_yaml(lock), encoding="utf-8")
        before = lock_path.read_bytes()
        rc = s.main(["upgrade", "--target", str(target), "--cairn-root",
                     str(CAIRN_ROOT), "--adopt-module", self.TOKEN_NAME])
        assert rc == 2
        assert not (target / "scripts/run_security_audit.py").exists()
        assert lock_path.read_bytes() == before

    def test_adopt_required_token_angle_placeholder_refuses_closed(
        self, tmp_path: Path,
    ) -> None:
        """The `<my package>` regression (#5): an angle-bracket placeholder
        -- the shape `_cmd_init_lock`'s own template writes -- must refuse
        too, even though `missing_required_tokens` alone would not catch it
        (edge case: an unfilled placeholder, angle-bracket form)."""
        target = tmp_path.resolve()
        _install(target)
        lock = s.read_lockfile(target)
        lock["tokens"]["python_package"] = "<my package>"
        (target / "dev" / ".cairn" / "cairn-lock.yml").write_text(
            s._emit_lock_yaml(lock), encoding="utf-8")
        before = s.read_lockfile(target)
        rc = s.main(["upgrade", "--target", str(target), "--cairn-root",
                     str(CAIRN_ROOT), "--adopt-module", self.TOKEN_NAME])
        assert rc == 2
        assert not (target / "scripts" / "run_security_audit.py").exists()
        assert s.read_lockfile(target) == before

    def test_adopt_refusal_names_a_remedy_that_works(
        self, tmp_path: Path, capsys
    ) -> None:
        """The refusal must point at something that fills the token.  Adopting
        needs a lockfile, and --init-lock answers "already exists" once there
        is one, so naming it sends the adopter nowhere.  Following the
        message's own advice -- the install profile, with the value added, at
        the committed install-config path -- must make the retry succeed."""
        target = tmp_path.resolve()
        _install(target)
        capsys.readouterr()
        rc = s.main(["upgrade", "--target", str(target), "--cairn-root",
                     str(CAIRN_ROOT), "--adopt-module", self.TOKEN_NAME])
        assert rc == 2
        err = capsys.readouterr().err
        assert "init-lock" not in err
        assert "dev/.cairn/profile.yml" in err and "python_package" in err
        config = target / "dev" / ".cairn" / "profile.yml"
        config.write_text((target / "profile.yml").read_text(encoding="utf-8")
                          + "python_package: mypkg\n", encoding="utf-8")
        rc = s.main(["upgrade", "--target", str(target), "--cairn-root",
                     str(CAIRN_ROOT), "--adopt-module", self.TOKEN_NAME])
        assert rc == 0
        assert self.TOKEN_NAME in s.read_lockfile(target)["modules"]

    def test_adopt_refusal_says_what_a_complete_profile_is(
        self, tmp_path: Path, capsys
    ) -> None:
        """dev/.cairn/profile.yml seeds a token only when it is a complete
        profile -- a preset, or every axis.  An install from a literal
        `modules:` list has neither, so copying that profile there, as told,
        is refused again, by a warning that points at --init-lock, which a
        tree with a lockfile answers "already exists".  The refusal has to
        say what complete means, and following it must succeed."""
        target = tmp_path.resolve()
        cfg = target / "profile.yml"
        cfg.write_text("project_name: Demo\ntest_command: pytest\n"
                       "modules:\n  - claim-check\n", encoding="utf-8")
        assert s.main(["--config", str(cfg), "--target", str(target),
                       "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]) == 0
        capsys.readouterr()
        rc = s.main(["upgrade", "--target", str(target), "--cairn-root",
                     str(CAIRN_ROOT), "--adopt-module", self.TOKEN_NAME])
        assert rc == 2
        err = capsys.readouterr().err
        assert "preset:" in err
        assert "age, size, complexity, language, human_team, agent_team" in err
        config = target / "dev" / ".cairn" / "profile.yml"
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(
            cfg.read_text(encoding="utf-8")
            + "age: greenfield\nsize: small\ncomplexity: simple\n"
            "language: single\nhuman_team: solo\nagent_team: single\n"
            "python_package: mypkg\n", encoding="utf-8")
        rc = s.main(["upgrade", "--target", str(target), "--cairn-root",
                     str(CAIRN_ROOT), "--adopt-module", self.TOKEN_NAME])
        assert rc == 0
        assert self.TOKEN_NAME in s.read_lockfile(target)["modules"]

    def test_adopt_required_token_seeded_from_profile(
        self, tmp_path: Path,
    ) -> None:
        """D1: a required token absent from the lockfile resolves from the
        committed `dev/.cairn/profile.yml` and is PERSISTED into the
        lockfile by the adopt itself -- the profile is a seed, and after
        adoption the lockfile is the single authority, as before."""
        target = tmp_path.resolve()
        _install(target)
        assert "python_package" not in s.read_lockfile(target)["tokens"]
        (target / "dev" / ".cairn").mkdir(parents=True, exist_ok=True)
        (target / "dev" / ".cairn" / "profile.yml").write_text(
            "project_name: Demo\ntest_command: pytest\n"
            "age: greenfield\nsize: small\ncomplexity: simple\n"
            "language: single\nhuman_team: solo\nagent_team: single\n"
            "python_package: mypkg\n",
            encoding="utf-8",
        )
        rc = s.main(["upgrade", "--target", str(target), "--cairn-root",
                     str(CAIRN_ROOT), "--adopt-module", self.TOKEN_NAME])
        assert rc == 0
        lock = s.read_lockfile(target)
        assert self.TOKEN_NAME in lock["modules"]
        assert lock["tokens"]["python_package"] == "mypkg"
        # a previously-tracked token this profile read doesn't mention
        # survives -- merged into the lockfile map, never assigned over it.
        assert lock["tokens"]["project_name"] == "Demo"

    def test_adopt_required_token_lockfile_wins_over_profile(
        self, tmp_path: Path,
    ) -> None:
        """Token in both sources, disagreeing: the lockfile value wins
        (the lockfile is the single post-adoption authority; the profile is
        only ever a seed for a gap)."""
        target = tmp_path.resolve()
        _install(target)
        lock = s.read_lockfile(target)
        lock["tokens"]["python_package"] = "from_lockfile"
        (target / "dev" / ".cairn" / "cairn-lock.yml").write_text(
            s._emit_lock_yaml(lock), encoding="utf-8")
        (target / "dev" / ".cairn" / "profile.yml").write_text(
            "project_name: Demo\ntest_command: pytest\n"
            "age: greenfield\nsize: small\ncomplexity: simple\n"
            "language: single\nhuman_team: solo\nagent_team: single\n"
            "python_package: from_profile\n",
            encoding="utf-8",
        )
        rc = s.main(["upgrade", "--target", str(target), "--cairn-root",
                     str(CAIRN_ROOT), "--adopt-module", self.TOKEN_NAME])
        assert rc == 0
        assert s.read_lockfile(target)["tokens"]["python_package"] == "from_lockfile"

    def test_adopt_secret_shaped_required_token_refuses_closed(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """The secret-token guard now runs on `--adopt-module`, before any
        write. No real `KNOWN_TOKENS` name is secret-shaped today, so this
        ARRANGES its own known required token (per the plan's S2) rather
        than deriving an expectation from the live registry -- a test that
        reads its expectation from the thing it checks cannot fail."""
        from bootstrap._scaffold import upgrade as UP  # noqa: PLC0415

        target = tmp_path.resolve()
        _install(target)
        monkeypatch.setitem(
            UP._MODULE_REQUIRED_TOKENS, self.NAME, ("api_secret_key",))
        lock = s.read_lockfile(target)
        lock["tokens"]["api_secret_key"] = "sk-not-a-real-secret"
        (target / "dev" / ".cairn" / "cairn-lock.yml").write_text(
            s._emit_lock_yaml(lock), encoding="utf-8")
        before = s.read_lockfile(target)

        rc = s.main(["upgrade", "--target", str(target), "--cairn-root",
                     str(CAIRN_ROOT), "--adopt-module", self.NAME])
        assert rc == 2
        # no destination written (the no-destination-written assertion the
        # plan's S2 table names for this exact mutation's regression)
        assert not (target / "dev" / "architecture_review.md").exists()
        assert not (target / "dev" / "modules" / "architecture-review.md").exists()
        assert s.read_lockfile(target) == before

    # -- D2: advisory on both quiet branches ----------------------------------

    def test_adopt_advisory_fires_when_kept_file_differs(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str],
    ) -> None:
        """A kept (already-on-disk) destination that differs from what this
        spec would install gets an advisory -- never blocks, never
        overwrites. `dev/architecture_review.md` is ALSO a declared
        superseded surface for this same module (`config.py:1144-1145` vs.
        `:1209`), so this also pins the D2/`_superseded_surface_note`
        must-not-both-fire edge case: only the more precise D2 advisory
        fires, not the coarser 'reconcile or retire' note."""
        target = tmp_path.resolve()
        _install(target)
        dst = target / "dev" / "architecture_review.md"
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text("ADOPTER-CUSTOM-CONTENT\n", encoding="utf-8")

        capsys.readouterr()
        rc = s.main(["upgrade", "--target", str(target), "--cairn-root",
                     str(CAIRN_ROOT), "--adopt-module", self.NAME])
        assert rc == 0
        err = capsys.readouterr().err
        assert "dev/architecture_review.md" in err
        assert "differs from what module" in err
        assert "reconcile or retire" not in err  # D2 covers it; the note must not also fire
        # advisory only: the customized content survives untouched
        assert dst.read_text() == "ADOPTER-CUSTOM-CONTENT\n"

    def test_adopt_advisory_silent_when_kept_file_matches(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str],
    ) -> None:
        """The paired case: a kept destination byte-identical to what this
        spec would install gets NO advisory -- without this pair, the byte
        comparison could always-fire and still pass the differs-case alone."""
        target = tmp_path.resolve()
        _install(target)
        assert s.main(["upgrade", "--target", str(target), "--cairn-root",
                       str(CAIRN_ROOT), "--adopt-module", self.NAME]) == 0
        # Strip the module back out of the lockfile; the files stay on disk,
        # UNTOUCHED -- still byte-identical to what adoption would install.
        lock = s.read_lockfile(target)
        dsts = {sp.dst for sp in s._MODULE_MAPPINGS[self.NAME]}
        lock["modules"] = [m for m in lock["modules"] if m != self.NAME]
        lock["files"] = [r for r in lock["files"] if r["dst"] not in dsts]
        (target / "dev" / ".cairn" / "cairn-lock.yml").write_text(
            s._emit_lock_yaml(lock), encoding="utf-8")

        capsys.readouterr()
        rc = s.main(["upgrade", "--target", str(target), "--cairn-root",
                     str(CAIRN_ROOT), "--adopt-module", self.NAME])
        assert rc == 0
        err = capsys.readouterr().err
        assert "differs from what module" not in err

    def test_adopt_advisory_and_count_when_destination_already_tracked(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str],
    ) -> None:
        """The OTHER quiet branch (`continue`, not `else`): a destination
        already tracked under another roster entry is skipped, but now
        advises instead of producing no output whatsoever -- and the
        `recorded N file(s)` line is reconciled to say what happened rather
        than silently under-counting."""
        target = tmp_path.resolve()
        _install(target)
        lock = s.read_lockfile(target)
        base_cache = "dev/.cairn/base/dev/modules/architecture-review.md"
        base_bytes = b"previous upstream\n"
        cache_path = target / base_cache
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_bytes(base_bytes)
        lock["files"].append({
            "src": "modules/other/placeholder.md",
            "dst": "dev/modules/architecture-review.md",
            "verbatim": False,
            "hash": "sha256:" + s._sha256_hex(b"pre-existing\n"),
            "base_hash": "sha256:" + s._sha256_hex(base_bytes),
            "base_cache": base_cache,
        })
        (target / "dev" / "modules").mkdir(parents=True, exist_ok=True)
        (target / "dev" / "modules" / "architecture-review.md").write_text(
            "pre-existing\n", encoding="utf-8")
        (target / "dev" / ".cairn" / "cairn-lock.yml").write_text(
            s._emit_lock_yaml(lock), encoding="utf-8")

        capsys.readouterr()
        rc = s.main(["upgrade", "--target", str(target), "--cairn-root",
                     str(CAIRN_ROOT), "--adopt-module", self.NAME])
        assert rc == 0
        out = capsys.readouterr()
        assert "dev/modules/architecture-review.md" in out.err
        assert "already tracked under another roster entry" in out.err
        assert "recorded 2 file(s)" in out.out
        assert "1 already tracked under another roster entry" in out.out
        lock2 = s.read_lockfile(target)
        assert "dev/architecture_review.md" in {r["dst"] for r in lock2["files"]}
        assert "tools/code_map.py" in {r["dst"] for r in lock2["files"]}
        assert (target / "tools/code_map.py").read_bytes() == (
            CAIRN_ROOT / "templates/modules/team-gated/code_map.py").read_bytes()
        # the pre-existing record for the skipped destination is untouched
        pre = next(r for r in lock2["files"]
                   if r["dst"] == "dev/modules/architecture-review.md")
        assert pre["src"] == "modules/other/placeholder.md"


# ---------------------------------------------------------------------------
# RULES.md living-state upgrade promises
# ---------------------------------------------------------------------------

class TestRulesMdUpgrade:
    def test_clean_rules_is_listed_without_mutating_file_or_lock(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """The public plan shows tracked rules as clean and preserves both records."""
        target = tmp_path.resolve()
        assert _install(target) == 0
        rules = target / "RULES.md"
        rules_before = rules.read_bytes()
        lock_path = target / s._LOCKFILE_REL
        lock_before = lock_path.read_bytes()
        lock = s.read_lockfile(target)
        rec = next(r for r in lock["files"] if r["dst"] == "RULES.md")
        assert rec["src"] == "core/RULES.md"
        assert rec.get("living_state") is True
        assert rec.get("base_cache") and rec.get("base_hash")
        capsys.readouterr()
        assert s.main([
            "upgrade", "--target", str(target),
            "--cairn-root", str(CAIRN_ROOT), "--plan",
        ]) == 0
        output = capsys.readouterr().out
        assert any(
            "RULES.md" in line and "clean (untouched)" in line
            for line in output.splitlines()
        )
        assert rules.read_bytes() == rules_before
        assert lock_path.read_bytes() == lock_before

    def test_repeated_upgrades_keep_deleted_rules_absent(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        target = tmp_path.resolve()
        assert _install(target) == 0
        rules = target / "RULES.md"
        rules.unlink()
        lock_before = s.read_lockfile(target)
        rec_before = next(r for r in lock_before["files"]
                          if r["dst"] == "RULES.md")
        rec_before = dict(rec_before)
        cache = target / rec_before["base_cache"]
        cache_before = cache.read_bytes()
        base = ["upgrade", "--target", str(target), "--cairn-root", str(CAIRN_ROOT)]

        for _ in range(2):
            capsys.readouterr()
            assert s.main(base + ["--stage"]) == 0
            output = capsys.readouterr().out
            assert any(
                "RULES.md" in line and "up-to-date" in line
                for line in output.splitlines()
            )
            assert s.main(base + ["--apply"]) == 0
            assert not rules.exists()
            lock = s.read_lockfile(target)
            rec = next(r for r in lock["files"] if r["dst"] == "RULES.md")
            assert rec == rec_before
            assert cache.read_bytes() == cache_before

    def test_dangling_rules_link_is_refused(self, tmp_path: Path) -> None:
        target = tmp_path.resolve()
        assert _install(target) == 0
        rules = target / "RULES.md"
        rules.unlink()
        missing_target = target / "missing-rules-target"
        rules.symlink_to(missing_target)
        lock_before = s.read_lockfile(target)

        assert s.main(["upgrade", "--target", str(target),
                       "--cairn-root", str(CAIRN_ROOT), "--plan"]) != 0
        assert rules.is_symlink()
        assert s.read_lockfile(target) == lock_before


class TestLivingStatePartition:
    """`verify_integrity` excludes adopter-authored *living-state* files (a
    living roadmap, the per-goodnight handoff, the fold-back ledger, the signed
    agreement) from the tamper check -- they are tracked for upgrade but their
    constant churn must not red the supply-chain check on the shipped
    apparatus. Captured by the modflow_tools reference adopter (finalize-cadence
    fold-up)."""

    def test_install_flags_living_state_records(self, tmp_path: Path) -> None:
        assert _install(tmp_path) == 0
        lock = s.read_lockfile(tmp_path)
        flagged = {r["dst"] for r in lock["files"] if r.get("living_state")}
        # PLANNING.md is core -> always present + flagged. A handoff file is
        # no longer shipped, so a new install records none.
        assert "dev/PLANNING.md" in flagged
        assert "CHANGELOG.md" in flagged
        assert "RULES.md" in flagged
        assert "dev/NEXT_SESSION.md" not in flagged
        # Apparatus is never flagged.
        assert "AGENTS.md" not in flagged
        # Every flagged dst is in the authoritative policy set.
        assert flagged <= set(s._LIVING_STATE_DSTS)

    def test_editing_living_state_does_not_fail_integrity(
        self, tmp_path: Path
    ) -> None:
        from bootstrap.verify_integrity import verify

        assert _install(tmp_path) == 0
        assert verify(tmp_path) == 0
        # A routine edit to a living-state file stays clean (excluded).
        for name in ("dev/PLANNING.md", "CHANGELOG.md", "RULES.md"):
            p = tmp_path / name
            p.write_text(p.read_text(encoding="utf-8") + "\nRoutine edit.\n",
                         encoding="utf-8")
            assert verify(tmp_path) == 0
        # But tampering with shipped apparatus still fails closed.
        ag = tmp_path / "AGENTS.md"
        ag.write_text(ag.read_text() + "\n<!-- tampered apparatus -->\n")
        assert verify(tmp_path) == 1

    def test_finalize_migrates_pre_living_state_lockfile(
        self, tmp_path: Path
    ) -> None:
        """An older lockfile (no ``living_state`` flags) is migrated by
        ``--finalize``: the flag is stamped from the policy set, so a churned
        living-state file stops tripping the verifier."""
        from bootstrap.verify_integrity import verify

        assert _install(tmp_path) == 0
        lock = s.read_lockfile(tmp_path)
        for r in lock["files"]:
            r.pop("living_state", None)  # simulate a pre-partition lockfile
        (tmp_path / s._LOCKFILE_REL).write_text(
            s._emit_lock_yaml(lock), encoding="utf-8")
        p = tmp_path / "dev" / "PLANNING.md"
        p.write_text(p.read_text() + "\n<!-- edit -->\n")
        assert verify(tmp_path) == 1  # stale recorded hash trips pre-migration
        assert s.main(["upgrade", "--finalize", "--target", str(tmp_path),
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        lock2 = s.read_lockfile(tmp_path)
        rec = next(r for r in lock2["files"] if r["dst"] == "dev/PLANNING.md")
        assert rec.get("living_state") is True
        assert verify(tmp_path) == 0

    def test_living_state_flag_rejected_outside_authoritative_set(
        self, tmp_path: Path
    ) -> None:
        """The living-state opt-out is a *verifier policy*, not
        a self-asserted lockfile escape hatch.  A record whose ``dst`` is not in
        ``_LIVING_STATE_DSTS`` may not exclude itself from the tamper check by
        setting ``living_state: true`` -- otherwise a modified script could be
        hidden from ``verify_integrity`` by flipping one lockfile field."""
        from bootstrap.verify_integrity import verify

        assert _install(tmp_path) == 0
        assert verify(tmp_path) == 0
        lock = s.read_lockfile(tmp_path)
        vrec = next(r for r in lock["files"]
                    if r.get("verbatim") and r["dst"].endswith(".py"))
        # Tamper the script on disk -> caught (no flag).
        f = tmp_path / vrec["dst"]
        f.write_text(f.read_text() + "\n# tampered\n")
        assert verify(tmp_path) == 1
        # Attempt the bypass: mark the *script* record living_state.
        for r in lock["files"]:
            if r["dst"] == vrec["dst"]:
                r["living_state"] = True
        (tmp_path / s._LOCKFILE_REL).write_text(
            s._emit_lock_yaml(lock), encoding="utf-8")
        # Still fails closed -- the flag is honored only for the policy set.
        assert verify(tmp_path) == 1

    @pytest.mark.parametrize("mode", ["apply", "finalize", "init-lock"])
    def test_old_changelog_record_migrates_without_repinning(
        self, tmp_path: Path, mode: str
    ) -> None:
        from bootstrap.verify_integrity import verify

        assert _install(tmp_path) == 0
        lock = s.read_lockfile(tmp_path)
        rec = next(r for r in lock["files"] if r["dst"] == "CHANGELOG.md")
        rec.pop("living_state", None)
        old_hash = rec["hash"]
        (tmp_path / s._LOCKFILE_REL).write_text(s._emit_lock_yaml(lock), encoding="utf-8")
        args = ["upgrade", "--target", str(tmp_path),
                "--cairn-root", str(CAIRN_ROOT)]
        if mode == "apply":
            assert s.main(args + ["--stage"]) == 0
            meta = json.loads((tmp_path / s._STAGING_REL / "stage-metadata.json").read_text())
            assert "CHANGELOG.md" not in meta["staged_files"]
            assert s.main(args + ["--apply"]) == 0
        elif mode == "finalize":
            assert s.main(args + ["--finalize", "CHANGELOG.md"]) == 0
        else:
            (tmp_path / s._LOCKFILE_REL).unlink()
            _seed_profile(tmp_path)
            assert s.main(args + ["--init-lock"]) == 0
        current = s.read_lockfile(tmp_path)
        migrated = next(r for r in current["files"] if r["dst"] == "CHANGELOG.md")
        assert migrated.get("living_state") is True
        assert migrated["hash"] == old_hash
        history = tmp_path / "CHANGELOG.md"
        history.write_bytes(history.read_bytes() + "\nRelease notes: \u8bb0\u5f55.\n".encode("utf-8"))
        assert verify(tmp_path) == 0
        script = next(r for r in current["files"] if r.get("verbatim") and r["dst"].endswith(".py"))
        path = tmp_path / script["dst"]
        path.write_bytes(path.read_bytes() + b"\n# modified script\n")
        assert verify(tmp_path) == 1


# ---------------------------------------------------------------------------
# Layer 3 (#56): the upgrade dirty-tree guard
# ---------------------------------------------------------------------------
#
# `upgrade --apply` must not silently overwrite a tracked file the adopter has
# uncommitted edits in (a concurrent session's in-flight work).  --apply
# refuses on a dirty *tracked* intersection (--force overrides); --stage only
# advises and completes; benign untracked/gitignored dirt never trips it.

import shutil  # noqa: E402


@pytest.mark.skipif(shutil.which("git") is None, reason="git not available")
class TestDirtyTreeGuard:
    def _git(self, target: Path, *argv: str) -> None:
        import subprocess
        subprocess.run(["git", "-C", str(target), *argv],
                       check=True, capture_output=True, text=True)

    def _init_committed(self, target: Path) -> None:
        """Install, then commit the whole pristine install -> a clean tree."""
        assert _install(target) == 0
        self._git(target, "init", "-q")
        self._git(target, "config", "user.email", "t@example.com")
        self._git(target, "config", "user.name", "Test")
        self._git(target, "add", "-A")
        self._git(target, "commit", "-q", "-m", "install")

    def _stage_agents_change(self, target: Path) -> None:
        """Diverge AGENTS.md (now uncommitted-dirty vs HEAD) and stage the
        upgrade -- staged_files includes AGENTS.md, the write-set/dirt overlap."""
        TestUpgradeModes()._diverge_base(target)
        assert s.main(["upgrade", "--target", str(target), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0

    def test_apply_refuses_on_dirty_tracked_intersection(
        self, tmp_path: Path, capsys
    ) -> None:
        """(v) --apply refuses when the write-set overlaps a tracked,
        uncommitted path -- it would clobber in-flight work."""
        self._init_committed(tmp_path)
        self._stage_agents_change(tmp_path)  # AGENTS.md dirty + staged
        rc = s.main(["upgrade", "--target", str(tmp_path), "--apply",
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 1
        err = capsys.readouterr().err
        assert "refusing --apply" in err and "AGENTS.md" in err
        # Not swapped: the diverged ("# OLD") content is untouched on disk.
        assert "# OLD" in (tmp_path / "AGENTS.md").read_text()
        # Stage not cleaned -- the upgrade did not proceed.
        assert (tmp_path / "dev" / ".cairn-upgrade").exists()

    def test_literal_pathspec_name_is_a_single_tracked_path(self, tmp_path: Path) -> None:
        """Caller paths that resemble Git pathspec syntax remain literal."""
        self._init_committed(tmp_path)
        special = ":(glob)**.md"
        (tmp_path / special).write_text("initial\n")
        self._git(tmp_path, "add", "--", special)
        self._git(tmp_path, "commit", "-q", "-m", "track literal pathspec name")

        (tmp_path / special).write_text("changed literal path\n")
        (tmp_path / "AGENTS.md").write_text("ordinary dirty path\n")
        assert s._dirty_tracked_paths(tmp_path, [special]) == {special}
        assert s._dirty_tracked_paths(tmp_path, ["AGENTS.md"]) == {"AGENTS.md"}
        self._git(tmp_path, "add", "--", special)
        assert s._dirty_tracked_paths(tmp_path, [special]) == {special}

    def test_force_overrides_dirty_guard(self, tmp_path: Path) -> None:
        """--force overrides the guard: --apply proceeds and swaps."""
        self._init_committed(tmp_path)
        self._stage_agents_change(tmp_path)
        rc = s.main(["upgrade", "--target", str(tmp_path), "--apply",
                     "--force", "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 0
        ag = (tmp_path / "AGENTS.md").read_text()
        assert "keep me" in ag and "# OLD" not in ag  # upstream header folded
        assert not (tmp_path / "dev" / ".cairn-upgrade").exists()  # cleaned

    def test_stage_advises_but_completes_on_dirty(
        self, tmp_path: Path, capsys
    ) -> None:
        """--stage writes only the gitignored review surface: it
        completes on a dirty tree but advises about the overlap."""
        self._init_committed(tmp_path)
        TestUpgradeModes()._diverge_base(tmp_path)  # AGENTS.md dirty
        rc = s.main(["upgrade", "--target", str(tmp_path), "--stage",
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 0  # completes
        err = capsys.readouterr().err
        assert "advisory" in err and "AGENTS.md" in err
        assert (tmp_path / "dev" / ".cairn-upgrade" / "files" /
                "AGENTS.md").exists()

    def test_benign_untracked_dirt_does_not_trip(
        self, tmp_path: Path
    ) -> None:
        """(vii) Untracked scratch is not a tracked uncommitted change -- the
        guard ignores it and --apply proceeds."""
        # Install + diverge, then commit the diverged state -> clean tree whose
        # committed base still differs from upstream, so AGENTS.md still stages.
        assert _install(tmp_path) == 0
        TestUpgradeModes()._diverge_base(tmp_path)
        self._git(tmp_path, "init", "-q")
        self._git(tmp_path, "config", "user.email", "t@example.com")
        self._git(tmp_path, "config", "user.name", "Test")
        self._git(tmp_path, "add", "-A")
        self._git(tmp_path, "commit", "-q", "-m", "install+diverge")
        # Benign dirt: an untracked scratch file, disjoint from the write-set.
        (tmp_path / "scratch-notes.md").write_text("local scratch\n")
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        rc = s.main(["upgrade", "--target", str(tmp_path), "--apply",
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 0  # untracked dirt did not trip the guard
        ag = (tmp_path / "AGENTS.md").read_text()
        assert "keep me" in ag and "# OLD" not in ag

    def test_disjoint_tracked_dirt_does_not_trip(
        self, tmp_path: Path
    ) -> None:
        """A tracked file with uncommitted edits that is *not* in the write-set
        does not trip the guard (the intersection, not mere dirtiness, gates)."""
        assert _install(tmp_path) == 0
        TestUpgradeModes()._diverge_base(tmp_path)
        self._git(tmp_path, "init", "-q")
        self._git(tmp_path, "config", "user.email", "t@example.com")
        self._git(tmp_path, "config", "user.name", "Test")
        self._git(tmp_path, "add", "-A")
        self._git(tmp_path, "commit", "-q", "-m", "install+diverge")
        # Dirty a tracked file outside the write-set (profile.yml is committed
        # but never part of an upgrade stage).
        (tmp_path / "profile.yml").write_text("project_name: Edited\n")
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        rc = s.main(["upgrade", "--target", str(tmp_path), "--apply",
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 0  # disjoint tracked dirt did not trip the guard


class TestManifestHomeAndSelfHeal:
    """The citation check finds the manifest in `dev/.cairn/` first
    (legacy `dev/strategy/` fallback); a missing `profile.yml` self-heals
    from the lockfile (merging tokens + profile), composing with the #56
    dirty-tree guard."""

    def test_plan_reports_citation_status_through_public_command(
        self, tmp_path: Path, capsys,
    ) -> None:
        assert _install(tmp_path) == 0
        lock = s.read_lockfile(tmp_path)
        args = ["upgrade", "--target", str(tmp_path), "--plan",
                "--cairn-root", str(CAIRN_ROOT)]

        canonical = tmp_path / "dev" / ".cairn" / "x-fidelity-manifest.yml"
        canonical.write_text(f'cairn_commit: "{lock["cairn_commit"]}"\n')
        assert s.main(args) == 0
        out, _err = capsys.readouterr()
        assert "fidelity manifest does NOT cite" not in out

        canonical.write_text('cairn_commit: "0000000"\n')
        assert s.main(args) == 0
        out, _err = capsys.readouterr()
        assert "fidelity manifest does NOT cite" in out

        canonical.unlink()
        legacy = tmp_path / "dev" / "strategy" / "x-fidelity-manifest.yml"
        legacy.parent.mkdir(parents=True, exist_ok=True)
        legacy.write_text(f'cairn_commit: "{lock["cairn_commit"]}"\n')
        assert s.main(args) == 0
        out, err = capsys.readouterr()
        assert "fidelity manifest does NOT cite" not in out
        assert "legacy" in err

        canonical.write_text(f'cairn_commit: "{lock["cairn_commit"]}"\n')
        legacy.write_text('cairn_commit: "0000000"\n')
        assert s.main(args) == 0
        out, err = capsys.readouterr()
        assert "fidelity manifest does NOT cite" not in out
        assert "legacy" not in err

    @pytest.mark.parametrize("profile_state", ["present", "empty-lock-profile"])
    def test_apply_self_heal_preserves_present_profile_or_skips_stub(
        self, tmp_path: Path, profile_state: str,
    ) -> None:
        assert _install(tmp_path) == 0
        profile = tmp_path / "dev" / ".cairn" / "profile.yml"
        lock_path = tmp_path / "dev" / ".cairn" / "cairn-lock.yml"
        if profile_state == "present":
            _seed_profile(tmp_path, size="large")
            profile_before = profile.read_bytes()
            assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                           "--cairn-root", str(CAIRN_ROOT)]) == 0
            assert s.main(["upgrade", "--target", str(tmp_path), "--apply",
                           "--cairn-root", str(CAIRN_ROOT)]) == 0
            assert profile.read_bytes() == profile_before
        else:
            lock = s.read_lockfile(tmp_path)
            lock["profile"] = {}
            lock_path.write_text(s._emit_lock_yaml(lock), encoding="utf-8")
            lock_before = lock_path.read_bytes()
            profile.unlink(missing_ok=True)
            assert s.main(["upgrade", "--target", str(tmp_path), "--apply",
                           "--cairn-root", str(CAIRN_ROOT)]) != 0
            assert not profile.exists()
            assert lock_path.read_bytes() == lock_before

    def test_self_heal_through_apply_not_stage(self, tmp_path: Path) -> None:
        """(T-1) self-heal is wired through `cmd_upgrade --apply`; (S-1) `--stage`
        is a non-mutating preview and must NOT materialize the config."""
        assert _install(tmp_path) == 0
        prof = tmp_path / "dev" / ".cairn" / "profile.yml"
        assert not prof.exists()  # install does not write the config there
        # --stage is a preview: it must not self-heal (S-1).
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        assert not prof.exists()
        # --apply self-heals through the public entry point (T-1).
        assert s.main(["upgrade", "--target", str(tmp_path), "--apply",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        assert prof.exists()
        cfg = s.load_config(prof)
        assert cfg["project_name"] == "Demo" and all(cfg.get(a) for a in s._AXES)

    @pytest.mark.skipif(shutil.which("git") is None, reason="git not available")
    def test_self_heal_composes_with_dirty_tree_guard(self, tmp_path: Path) -> None:
        """(invariant vi) The self-healed profile.yml is untracked, so the #56
        tracked-only dirty-tree guard does not see it as a collision."""
        import subprocess
        assert _install(tmp_path) == 0
        for c in (["init", "-q"], ["config", "user.email", "t@t"],
                  ["config", "user.name", "t"], ["add", "-A"],
                  ["commit", "-q", "-m", "install"]):
            subprocess.run(["git", "-C", str(tmp_path), *c],
                           check=True, capture_output=True, text=True)
        # self-heal now writes an untracked profile.yml on a clean committed tree
        assert s._self_heal_profile_config(tmp_path, s.read_lockfile(tmp_path))
        dirty = s._dirty_tracked_paths(tmp_path)
        assert dirty is not None
        assert "dev/.cairn/profile.yml" not in dirty   # untracked -> excluded

    def test_self_heal_does_not_write_retired_metrics_command(
            self, tmp_path: Path) -> None:
        """Defect 18: an old lockfile still carries the retired
        ``metrics_command`` token. The self-heal writer must not write it, so
        the materialized profile.yml loads with no unrecognized key."""
        lock = {
            "profile": {
                "preset": "collaborative-team",
                "axes": {
                    "age": "greenfield", "size": "medium",
                    "complexity": "moderate", "language": "single",
                    "human_team": "small-multi",
                    "agent_team": "concurrent-multi-type",
                },
            },
            "tokens": {
                "project_name": "Demo",
                "test_command": "pytest -q",
                "metrics_command": "python tools/metrics.py",
            },
            "modules": ["claim-check"],
        }
        assert s._self_heal_profile_config(tmp_path, lock) is True
        prof = tmp_path / "dev" / ".cairn" / "profile.yml"
        assert "metrics_command" not in prof.read_text(encoding="utf-8")
        cfg = s.load_config(prof)  # raises on any unrecognized key
        assert cfg["project_name"] == "Demo"


def _git_commit_install(tmp_path: Path) -> None:
    """Make `tmp_path` a committed git work tree so the #56 dirty-tree guard
    (which keys on `git status --porcelain`) is live."""
    import subprocess
    for c in (["init", "-q"], ["config", "user.email", "t@t"],
              ["config", "user.name", "t"], ["add", "-A"],
              ["commit", "-q", "-m", "install"]):
        subprocess.run(["git", "-C", str(tmp_path), *c],
                       check=True, capture_output=True, text=True)


@pytest.mark.skipif(shutil.which("git") is None, reason="git not available")
class TestFinalizeDirtyTreeGuard:
    """#56 dirty-tree guard, finalize arm: an *unscoped* whole-tree
    ``--finalize`` on a dirty tree advances the lockfile hash of every drifted
    tracked file -- including a concurrent session's uncommitted WIP -- so it
    refuses unless scoped (``--finalize <path>...``) or forced (``--force``).
    Witnessed by the modflow_tools reference adopter (a single-file re-finalize
    swept a concurrent session's facade-migration WIP)."""

    def test_unscoped_finalize_refuses_on_dirty_tree(self, tmp_path: Path) -> None:
        assert _install(tmp_path) == 0
        _git_commit_install(tmp_path)
        ag = tmp_path / "AGENTS.md"
        ag.write_text(ag.read_text() + "\n<!-- concurrent WIP -->\n")  # dirty
        lock_before = s.read_lockfile(tmp_path)
        rc = s.main(["upgrade", "--finalize", "--target", str(tmp_path),
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 1, "unscoped finalize must refuse on a dirty tree"
        assert s.read_lockfile(tmp_path) == lock_before, \
            "a refused finalize must not write the lockfile"

    def test_force_overrides_finalize_dirty_tree_guard(self, tmp_path: Path) -> None:
        assert _install(tmp_path) == 0
        _git_commit_install(tmp_path)
        ag = tmp_path / "AGENTS.md"
        ag.write_text(ag.read_text() + "\n<!-- WIP -->\n")
        rc = s.main(["upgrade", "--finalize", "--force", "--target", str(tmp_path),
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 0, "--force must override the finalize dirty-tree guard"

    def test_scoped_finalize_touches_only_named_records(self, tmp_path: Path) -> None:
        """The anti-sweep guarantee: ``--finalize AGENTS.md`` advances only the
        named record's hash, leaving a concurrent session's drifted file (a
        verbatim script edited in parallel) untouched in the lockfile."""
        assert _install(tmp_path) == 0
        _git_commit_install(tmp_path)
        lock0 = s.read_lockfile(tmp_path)
        wip = next(r for r in lock0["files"] if r.get("verbatim"))  # concurrent WIP
        wip_dst = wip["dst"]
        assert wip_dst != "AGENTS.md"
        # Both files drift: AGENTS.md (mine) + the verbatim script (the other agent).
        ag = tmp_path / "AGENTS.md"
        ag.write_text(ag.read_text() + "\n<!-- mine -->\n")
        wipf = tmp_path / wip_dst
        wipf.write_text(wipf.read_text() + "\n# concurrent WIP\n")
        # Scope the finalize to AGENTS.md only.
        rc = s.main(["upgrade", "--finalize", "AGENTS.md", "--target",
                     str(tmp_path), "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 0
        lock1 = s.read_lockfile(tmp_path)
        rec_ag = next(r for r in lock1["files"] if r["dst"] == "AGENTS.md")
        rec_wip = next(r for r in lock1["files"] if r["dst"] == wip_dst)
        # AGENTS.md advanced to its on-disk content...
        assert rec_ag["hash"] == "sha256:" + s._sha256_hex(ag.read_bytes())
        # ...but the concurrent WIP's hash is UNCHANGED (not swept).
        assert rec_wip["hash"] == wip["hash"], \
            "scoped finalize must not advance the concurrent file's hash"
        assert rec_wip["hash"] != "sha256:" + s._sha256_hex(wipf.read_bytes())

    def test_scoped_finalize_unknown_path_fails_closed(self, tmp_path: Path) -> None:
        assert _install(tmp_path) == 0
        rc = s.main(["upgrade", "--finalize", "does/not/exist.md", "--target",
                     str(tmp_path), "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 1, "a named path not in the lockfile must fail closed"

    def test_positional_path_without_finalize_rejected(self, tmp_path: Path) -> None:
        assert _install(tmp_path) == 0
        rc = s.main(["upgrade", "AGENTS.md", "--target", str(tmp_path),
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 2, "positional PATH is only valid with --finalize"

    def test_scoped_finalize_renamed_wrapper_by_recorded_name(
        self, tmp_path: Path
    ) -> None:
        """A renamed vendor wrapper can be scoped by its
        lockfile-recorded name (VENDOR.md) even though it resolves on disk to
        CLAUDE.md -- the recorded name must not fail closed once it resolves.
        (Scoped finalize bypasses the dirty-tree guard, so no git tree needed.)"""
        assert _install(tmp_path) == 0
        (tmp_path / "VENDOR.md").rename(tmp_path / "CLAUDE.md")  # adopter rename
        claude = tmp_path / "CLAUDE.md"
        claude.write_text(claude.read_text() + "\n<!-- adopter edit -->\n")
        rc = s.main(["upgrade", "--finalize", "VENDOR.md", "--target",
                     str(tmp_path), "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 0, "scoping by the recorded VENDOR.md name must resolve"
        lock = s.read_lockfile(tmp_path)
        wrapper = next(r for r in lock["files"] if r["src"] == "core/VENDOR.md")
        assert wrapper["dst"] == "CLAUDE.md"
        assert wrapper["hash"] == "sha256:" + s._sha256_hex(claude.read_bytes())


class TestTrackedDirectoryCollisions:
    def test_plan_prefers_custom_wrapper_file_to_known_name_directory(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str],
    ) -> None:
        assert _install(tmp_path) == 0
        (tmp_path / "VENDOR.md").rename(tmp_path / "CUSTOM.md")
        (tmp_path / "CUSTOM.md").write_text(
            "# Custom wrapper\n@AGENTS.md\n", encoding="utf-8",
        )
        (tmp_path / "CLAUDE.md").mkdir()

        assert s.main(["upgrade", "--target", str(tmp_path), "--plan",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        out = capsys.readouterr().out
        assert "CUSTOM.md" in out, out
        assert "CLAUDE.md  directory-blocked" not in out, out

    def test_finalize_prefers_custom_wrapper_file_to_known_name_directory(
        self, tmp_path: Path,
    ) -> None:
        assert _install(tmp_path) == 0
        (tmp_path / "VENDOR.md").rename(tmp_path / "CUSTOM.md")
        custom = tmp_path / "CUSTOM.md"
        custom.write_text("# Custom wrapper\n@AGENTS.md\n", encoding="utf-8")
        (tmp_path / "CLAUDE.md").mkdir()

        assert s.main(["upgrade", "--finalize", "VENDOR.md", "--target",
                       str(tmp_path), "--cairn-root", str(CAIRN_ROOT)]) == 0
        wrapper = next(r for r in s.read_lockfile(tmp_path)["files"]
                       if r["src"] == "core/VENDOR.md")
        assert wrapper["dst"] == "CUSTOM.md"
        assert wrapper["hash"] == "sha256:" + s._sha256_hex(custom.read_bytes())

    @pytest.mark.parametrize("review_only", [False, True])
    def test_stage_catches_directory_that_appears_after_classification(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
        review_only: bool,
    ) -> None:
        assert _install(tmp_path) == 0
        TestUpgradeModes()._diverge_base(tmp_path)
        if review_only:
            (tmp_path / "dev/.cairn/base/AGENTS.md").unlink()
        dst = tmp_path / "AGENTS.md"
        assert s.main(["upgrade", "--target", str(tmp_path), "--plan",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0

        real_compute = s._compute_upgrade
        changed = False

        def classify_then_replace_with_directory(*args, **kwargs):
            nonlocal changed
            plans, structural = real_compute(*args, **kwargs)
            planned = next(fp for fp in plans if fp.dst == "AGENTS.md")
            assert planned.kind == ("review-only" if review_only else
                                    "clean-locally-modified")
            dst.unlink()
            dst.mkdir()
            (dst / "nested.txt").write_bytes(b"preserve")
            changed = True
            return plans, structural

        upgrade_module = sys.modules[s._compute_upgrade.__module__]
        monkeypatch.setattr(upgrade_module, "_compute_upgrade",
                            classify_then_replace_with_directory)
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        assert changed
        meta = json.loads((tmp_path / "dev/.cairn-upgrade" / s._STAGE_META).read_text())
        assert "AGENTS.md" in meta["directory_blocked"]
        assert "AGENTS.md" not in meta["staged_files"]
        assert "AGENTS.md" not in meta["review_only"]
        assert not (tmp_path / "dev/.cairn-upgrade/review-only/AGENTS.md.ours").exists()
        assert (dst / "nested.txt").read_bytes() == b"preserve"

    @pytest.mark.parametrize("observation", ["complete", "missing", "empty", "omitted"])
    def test_noop_tracked_file_becoming_directory_blocks_apply(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str], observation: str,
    ) -> None:
        assert _install(tmp_path) == 0
        TestUpgradeModes()._diverge_base(tmp_path)
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        stage = tmp_path / "dev/.cairn-upgrade"
        meta = json.loads((stage / s._STAGE_META).read_text())
        lock = s.read_lockfile(tmp_path)
        rec = next(r for r in lock["files"]
                   if r["src"] != "core/VENDOR.md"
                   and r["dst"] in meta["directory_observed"]
                   and r["dst"] not in meta["staged_files"]
                   and (tmp_path / r["dst"]).is_file())
        if observation == "missing":
            del meta["directory_observed"]
        elif observation == "empty":
            meta["directory_observed"] = []
        elif observation == "omitted":
            meta["directory_observed"].remove(rec["dst"])
        (stage / s._STAGE_META).write_text(json.dumps(meta))
        dst = tmp_path / rec["dst"]
        dst.unlink()
        dst.mkdir()
        content = dst / "adopter-data"
        content.write_bytes(b"preserve")
        before = content.stat()
        lock_path = tmp_path / "dev/.cairn/cairn-lock.yml"
        lock_before = lock_path.read_bytes()
        cache_path = tmp_path / "dev/.cairn/base/AGENTS.md"
        cache_before = cache_path.read_bytes()
        rc = s.main(["upgrade", "--target", str(tmp_path), "--apply",
                     "--force", "--ack-review-only",
                     "--cairn-root", str(CAIRN_ROOT)])
        err = capsys.readouterr().err
        assert rc == 1
        expected = {"complete": "became directories",
                    "missing": "lacks directory observations",
                    "empty": "incomplete directory observations",
                    "omitted": "incomplete directory observations"}
        assert expected[observation] in err
        assert content.read_bytes() == b"preserve"
        assert content.stat().st_mode == before.st_mode
        assert content.stat().st_mtime_ns == before.st_mtime_ns
        assert lock_path.read_bytes() == lock_before
        assert cache_path.read_bytes() == cache_before
        assert stage.exists()

    @pytest.mark.parametrize("wrapper_name", ["VENDOR.md", "CUSTOM.md"])
    def test_wrapper_observation_cannot_be_omitted(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str],
        wrapper_name: str,
    ) -> None:
        """Apply requires the canonical or custom recorded wrapper destination."""
        assert _install(tmp_path) == 0
        if wrapper_name != "VENDOR.md":
            (tmp_path / "VENDOR.md").rename(tmp_path / wrapper_name)
            if wrapper_name == "CUSTOM.md":
                (tmp_path / wrapper_name).write_text(
                    "# Custom vendor wrapper\n@AGENTS.md\n", encoding="utf-8")
            lock_before = s.read_lockfile(tmp_path)
            other_records_before = [r for r in lock_before["files"]
                                    if r["src"] != "core/VENDOR.md"]
            stage = tmp_path / "dev/.cairn-upgrade"
            capsys.readouterr()
            rc = s.main(["upgrade", "--target", str(tmp_path), "--stage",
                         "--cairn-root", str(CAIRN_ROOT)])
            err = capsys.readouterr().err
            assert rc == 1
            assert "Review the full contents" in err
            assert "--finalize VENDOR.md" in err
            assert not stage.exists()

            assert s.main(["upgrade", "--target", str(tmp_path), "--finalize",
                           "VENDOR.md", "--cairn-root", str(CAIRN_ROOT)]) == 0
            lock_after = s.read_lockfile(tmp_path)
            wrapper = next(r for r in lock_after["files"]
                           if r["src"] == "core/VENDOR.md")
            assert wrapper["dst"] == wrapper_name
            assert wrapper["hash"] == "sha256:" + s._sha256_hex(
                (tmp_path / wrapper_name).read_bytes())
            assert [r for r in lock_after["files"]
                    if r["src"] != "core/VENDOR.md"] == other_records_before
        TestUpgradeModes()._diverge_base(tmp_path)
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        stage = tmp_path / "dev/.cairn-upgrade"
        meta = json.loads((stage / s._STAGE_META).read_text())
        assert wrapper_name in meta["directory_observed"]
        meta["directory_observed"].remove(wrapper_name)
        (stage / s._STAGE_META).write_text(json.dumps(meta))

        dst = tmp_path / wrapper_name
        dst.unlink()
        dst.mkdir()
        content = dst / "adopter-data"
        content.write_bytes(b"preserve wrapper data")
        before = content.stat()
        lock_path = tmp_path / "dev/.cairn/cairn-lock.yml"
        lock_before = lock_path.read_bytes()
        cache_path = tmp_path / "dev/.cairn/base/VENDOR.md"
        cache_before = cache_path.read_bytes()

        rc = s.main(["upgrade", "--target", str(tmp_path), "--apply",
                     "--force", "--ack-review-only",
                     "--cairn-root", str(CAIRN_ROOT)])
        err = capsys.readouterr().err
        assert rc == 1
        assert "incomplete directory observations" in err
        assert content.read_bytes() == b"preserve wrapper data"
        assert content.stat().st_mode == before.st_mode
        assert content.stat().st_mtime_ns == before.st_mtime_ns
        assert lock_path.read_bytes() == lock_before
        assert cache_path.read_bytes() == cache_before
        assert stage.exists()

    def test_lock_record_without_src_refuses_apply_cleanly(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str],
    ) -> None:
        assert _install(tmp_path) == 0
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        lock_path = tmp_path / "dev/.cairn/cairn-lock.yml"
        lock = s.read_lockfile(tmp_path)
        lock["files"][0].pop("src")
        lock_path.write_text(s._emit_lock_yaml(lock), encoding="utf-8")
        malformed_lock = lock_path.read_bytes()
        cache_path = tmp_path / "dev/.cairn/base/AGENTS.md"
        cache_before = cache_path.read_bytes()

        rc = s.main(["upgrade", "--target", str(tmp_path), "--apply",
                     "--force", "--ack-review-only",
                     "--cairn-root", str(CAIRN_ROOT)])
        err = capsys.readouterr().err
        assert rc == 1
        assert "malformed file record" in err
        assert "Traceback" not in err
        assert lock_path.read_bytes() == malformed_lock
        assert cache_path.read_bytes() == cache_before


    def test_restage_after_directory_collision_restores_regular_file(
        self, tmp_path: Path,
    ) -> None:
        assert _install(tmp_path) == 0
        dst = tmp_path / ".agents/skills/_data/vendor_targets.yml"
        original_file = dst.read_bytes()
        dst.unlink()
        dst.mkdir()
        (dst / "data").write_text("preserve")
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        saved_dir = tmp_path / "saved-directory"
        dst.rename(saved_dir)
        dst.write_bytes(original_file)
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        assert s.main(["upgrade", "--target", str(tmp_path), "--apply",
                       "--ack-review-only", "--force",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        assert dst.is_file()
        assert dst.read_bytes() == original_file
        assert (saved_dir / "data").read_text() == "preserve"

    def test_plan_stage_and_recovery_preserve_mergeable_directory(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str],
    ) -> None:
        assert _install(tmp_path) == 0
        TestUpgradeModes()._diverge_base(tmp_path)
        dst = tmp_path / "AGENTS.md"
        original_file = dst.read_bytes()
        assert s.main(["upgrade", "--target", str(tmp_path), "--plan",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        dst.unlink()
        dst.mkdir()
        nested = dst / "adopter" / "notes.txt"
        nested.parent.mkdir()
        nested.write_bytes(b"keep these bytes\x00\n")
        nested.chmod(0o640)
        before_stat = nested.stat()
        expected_lock = (tmp_path / "dev/.cairn/cairn-lock.yml").read_bytes()
        expected_cache = (tmp_path / "dev/.cairn/base/AGENTS.md").read_bytes()

        assert s.main(["upgrade", "--target", str(tmp_path), "--plan",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        assert "BLOCKED" in capsys.readouterr().out

        rc = s.main(["upgrade", "--target", str(tmp_path), "--stage",
                     "--cairn-root", str(CAIRN_ROOT)])
        out = capsys.readouterr().out
        assert rc == 0
        assert "BLOCKED" in out
        assert "clean (untouched)" in out
        stage = tmp_path / "dev/.cairn-upgrade"
        meta = json.loads((stage / s._STAGE_META).read_text())
        assert "AGENTS.md" in meta["directory_blocked"]
        assert "AGENTS.md" not in meta["staged_files"]
        assert nested.read_bytes() == b"keep these bytes\x00\n"
        assert nested.stat().st_mode == before_stat.st_mode
        assert nested.stat().st_mtime_ns == before_stat.st_mtime_ns
        assert (tmp_path / "dev/.cairn/cairn-lock.yml").read_bytes() == expected_lock
        assert (tmp_path / "dev/.cairn/base/AGENTS.md").read_bytes() == expected_cache

        # Repairing the live path cannot unlock a stage that recorded a block.
        saved_dir = tmp_path / "AGENTS.md.saved"
        saved_nested = saved_dir / nested.relative_to(dst)
        dst.rename(saved_dir)
        dst.write_bytes(original_file)
        rc = s.main(["upgrade", "--target", str(tmp_path), "--apply",
                     "--ack-review-only", "--force",
                     "--cairn-root", str(CAIRN_ROOT)])
        err = capsys.readouterr().err
        assert rc == 1 and "directories" in err and "upgrade --stage" in err
        assert "restore the tracked path as a regular file" in err
        assert "choose its absence" not in err
        assert dst.read_bytes() == original_file
        assert saved_nested.read_bytes() == b"keep these bytes\x00\n"
        assert saved_nested.stat().st_mode == before_stat.st_mode
        assert saved_nested.stat().st_mtime_ns == before_stat.st_mtime_ns
        assert (tmp_path / "dev/.cairn/cairn-lock.yml").read_bytes() == expected_lock
        assert stage.exists()

        # Restore the tracked file and create a fresh stage; normal apply works.
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        assert s.main(["upgrade", "--target", str(tmp_path), "--apply",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0

    def test_verbatim_directory_and_directory_after_stage_block_apply(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str],
    ) -> None:
        assert _install(tmp_path) == 0
        lock = s.read_lockfile(tmp_path)
        rec = next(r for r in lock["files"]
                   if r.get("verbatim") and (tmp_path / r["dst"]).is_file())
        dst = tmp_path / rec["dst"]
        dst.unlink()
        dst.mkdir(parents=True)
        content = dst / "nested.txt"
        content.write_text("adopter data")
        assert s.main(["upgrade", "--target", str(tmp_path), "--plan",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        assert "BLOCKED" in capsys.readouterr().out
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        meta = json.loads((tmp_path / "dev/.cairn-upgrade" / s._STAGE_META).read_text())
        assert rec["dst"] in meta["directory_blocked"]
        assert content.read_text() == "adopter data"

        # A separate staged file becoming a directory is caught before any
        # destination, lockfile or base-cache write.
        second = tmp_path / "second"
        second.mkdir()
        assert _install(second) == 0
        TestUpgradeModes()._diverge_base(second)
        assert s.main(["upgrade", "--target", str(second), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        second_agents = second / "AGENTS.md"
        second_agents.unlink()
        second_agents.mkdir()
        nested = second_agents / "nested.txt"
        nested.write_bytes(b"preserve")
        lock_before = (second / "dev/.cairn/cairn-lock.yml").read_bytes()
        cache_before = (second / "dev/.cairn/base/AGENTS.md").read_bytes()
        rc = s.main(["upgrade", "--target", str(second), "--apply",
                     "--force", "--cairn-root", str(CAIRN_ROOT)])
        err = capsys.readouterr().err
        assert rc == 1 and "became directories" in err
        assert nested.read_bytes() == b"preserve"
        assert (second / "dev/.cairn/cairn-lock.yml").read_bytes() == lock_before
        assert (second / "dev/.cairn/base/AGENTS.md").read_bytes() == cache_before
        assert (second / "dev/.cairn-upgrade").exists()
