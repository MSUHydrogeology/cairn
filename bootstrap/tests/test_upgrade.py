"""
Tests for the Cairn module-upgrade capability (3-way merge).

Covers, per the executing plan (cairn-module-upgrade-3way-merge):

* lockfile round-trip + base-cache round-trip (P-6); install fail-closed
  on a diverged tree (P-1); R9 secret-token guard.
* the slot parser fail-closed cases (R8).
* the token+slot-aware merge: clean fold, slot preservation under an
  upstream prose rewrite, true-conflict markers, slot-removed fail-closed
  (R4).
* verbatim-script hash policy (Part 4).
* the upgrade subcommand: --plan writes nothing (P-2); --stage then
  --apply swaps + cleans; --apply rejects a stale stage and residual
  conflict markers (R7/P-5); structural reconciliation; --to git-only
  (P-4); R10 stale-citation; --init-lock review-only for token files
  (R6/I3).

Run from the cairn repo root:
    python -m pytest bootstrap/tests/
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap import scaffold as s  # noqa: E402

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


# ---------------------------------------------------------------------------
# Lockfile + base cache (Ch1; P-1/P-6/R9)
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
                assert "base_cache" not in rec  # I4: scripts not cached
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
        (tmp_path / "dev" / "cairn-lock.yml").unlink()
        # re-run install (skips existing); lockfile must NOT be written
        assert _install(tmp_path) == 0
        assert not (tmp_path / "dev" / "cairn-lock.yml").exists()

    def test_secret_token_guard(self) -> None:
        # snake_case
        for name in ("api_token", "secret_key", "db_password"):
            with pytest.raises(s.PresetError):
                s._refuse_secret_tokens({name: "x"})
        # camelCase / flatcase must also be caught (Antigravity A2)
        for name in ("apiKey", "secretToken", "dbPassword", "mysecret",
                     "accessKey", "passwdstr"):
            with pytest.raises(s.PresetError):
                s._refuse_secret_tokens({name: "x"})
        # allow-list overrides; benign tokens pass
        s._refuse_secret_tokens({"apiKey": "x"}, allow=("apiKey",))
        s._refuse_secret_tokens({"project_name": "x", "test_command": "y"})


# ---------------------------------------------------------------------------
# Slot parser fail-closed (R8)
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
# Merge engine (R4)
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
        """A3: a single-empty-line slot body must not be dropped during
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


# ---------------------------------------------------------------------------
# upgrade subcommand: modes + safety contract (Ch5; P-2/R7/P-5/P-4/R10)
# ---------------------------------------------------------------------------

class TestUpgradeModes:
    def _diverge_base(self, target: Path) -> None:
        """Model an *old install + adopter customization*: the cached base
        AND the adopter's file both carry the old header (so it matches the
        old base), while the current upstream template carries the new
        header -> a real upstream change folds into ours, and ours' added
        line is preserved, with no conflict."""
        base = target / "dev" / ".cairn" / "base" / "AGENTS.md"
        base.write_text(base.read_text().replace("# AGENTS.md", "# OLD", 1))
        a = target / "AGENTS.md"
        a.write_text(
            a.read_text().replace("# AGENTS.md", "# OLD", 1) + "\n<!-- keep me -->\n")

    def test_plan_writes_nothing(self, tmp_path: Path) -> None:
        assert _install(tmp_path) == 0
        self._diverge_base(tmp_path)
        rc = s.main(["upgrade", "--target", str(tmp_path), "--plan",
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 0
        assert not (tmp_path / "dev" / ".cairn-upgrade").exists()

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
        # C1/A1: apply ADVANCED the machine authority -- the lockfile hash
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

    def test_apply_rejects_stale_stage(self, tmp_path: Path) -> None:
        assert _install(tmp_path) == 0
        self._diverge_base(tmp_path)
        s.main(["upgrade", "--target", str(tmp_path), "--stage",
                "--cairn-root", str(CAIRN_ROOT)])
        # adopter edits the original after staging
        a = tmp_path / "AGENTS.md"
        a.write_text(a.read_text() + "\nlater edit\n")
        rc = s.main(["upgrade", "--target", str(tmp_path), "--apply",
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 1  # stale -> refused

    def test_apply_rejects_conflict_markers(self, tmp_path: Path) -> None:
        assert _install(tmp_path) == 0
        stage = tmp_path / "dev" / ".cairn-upgrade"
        (stage / "files").mkdir(parents=True)
        (stage / "files" / "AGENTS.md").write_text(
            "<<<<<<< ours\nx\n=======\ny\n>>>>>>> theirs\n")
        lock = s.read_lockfile(tmp_path)
        (stage / s._STAGE_META).write_text(json.dumps({
            "lock_commit": lock["cairn_commit"], "tokens": lock["tokens"],
            "modules": lock["modules"], "staged_files": ["AGENTS.md"],
            "ours_hashes": {}, "has_conflicts": True,
        }))
        rc = s.main(["upgrade", "--target", str(tmp_path), "--apply",
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 1

    # ---- B-C-1: clean-vs-locally-modified split in the upgrade summary
    # `--plan` previously lumped every clean merge into one `clean` row,
    # hiding from the adopter whether their customizations rode through.
    # The split distinguishes `clean (untouched)` from
    # `locally-modified (merged clean)` so the adopter sees the merge
    # preserved their edits.

    def test_locally_modified_merged_clean_classified_distinctly(
        self, tmp_path: Path
    ) -> None:
        """B-C-1: ``_compute_upgrade`` flips a clean merge to
        ``clean-locally-modified`` when the adopter's on-disk file
        differs from the saved base -- i.e., they customized it locally
        and the customization merged cleanly with the new upstream.
        """
        assert _install(tmp_path) == 0
        self._diverge_base(tmp_path)  # ours has `<!-- keep me -->`; base lacks it
        lock = s.read_lockfile(tmp_path)
        plans, _structural = s._compute_upgrade(
            tmp_path, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref=None,
        )
        ag_plan = next(p for p in plans if p.dst == "AGENTS.md")
        assert ag_plan.kind == "clean-locally-modified", (
            f"AGENTS.md should classify as clean-locally-modified "
            f"(ours != base + clean merge); got {ag_plan.kind!r}"
        )
        # And it remains advancing -- stages + applies identically to clean.
        assert ag_plan.kind in s._ADVANCING_KINDS

    def test_clean_untouched_when_ours_equals_base(
        self, tmp_path: Path
    ) -> None:
        """The contrast case: when the adopter has NOT touched the file
        since install (``ours`` matches the token-substituted base) but
        the upstream has advanced, the classification stays plain
        ``clean`` (the untouched flavor).

        Models the scenario consistently with ``_diverge_base``: at
        install time both base AND ours were at the old version; the
        adopter then did NOT customize the file; upstream has since
        advanced.  Per the install-time invariant, ours = ``substitute_
        tokens(base, tokens)`` after a fresh install.
        """
        assert _install(tmp_path) == 0
        base = tmp_path / "dev" / ".cairn" / "base" / "AGENTS.md"
        ours_path = tmp_path / "AGENTS.md"
        # Edit BOTH base AND ours to model "install was at the OLD
        # version, then upstream advanced."  Critically: do NOT add any
        # local-customization marker -- this is the untouched flavor.
        base.write_text(
            base.read_text().replace("# AGENTS.md", "# OLD", 1)
        )
        ours_path.write_text(
            ours_path.read_text().replace("# AGENTS.md", "# OLD", 1)
        )
        # Now ours matches the token-substituted base; upstream still
        # carries "# AGENTS.md" (the new header).  A pure upstream
        # advance with no adopter customization.
        lock = s.read_lockfile(tmp_path)
        plans, _structural = s._compute_upgrade(
            tmp_path, CAIRN_ROOT, TEMPLATES_ROOT, lock, to_ref=None,
        )
        ag_plan = next(p for p in plans if p.dst == "AGENTS.md")
        assert ag_plan.kind == "clean", (
            f"AGENTS.md should classify as clean (ours matches "
            f"substituted base, upstream advanced); got {ag_plan.kind!r}"
        )

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
        monkeypatch.setattr(s, "_cairn_is_git", lambda root: False)
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
        """C2/A4: a slot-removed (or any non-advancing) file is never staged,
        so it can never be applied."""
        assert _install(tmp_path) == 0
        # ours fills a slot; the cached base has the slot; upstream (current
        # template) for this file is forced to have the slot removed by
        # blanking the base cache differently -> simulate via a fake file:
        # use AGENTS.md, give ours a fabricated slot the template lacks.
        base = tmp_path / "dev" / ".cairn" / "base" / "AGENTS.md"
        base.write_text(base.read_text()
                        + "\n<!-- cairn:slot zzz -->\nB\n<!-- cairn:end zzz -->\n")
        a = tmp_path / "AGENTS.md"
        a.write_text(a.read_text()
                     + "\n<!-- cairn:slot zzz -->\nMINE\n<!-- cairn:end zzz -->\n")
        # current upstream AGENTS.md has no `zzz` slot -> slot-removed.
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        staged = tmp_path / "dev" / ".cairn-upgrade" / "files" / "AGENTS.md"
        assert not staged.exists()  # slot-removed not staged

    def test_apply_rejects_corrupt_stage(self, tmp_path: Path) -> None:
        """C3: the on-disk staged set must equal the stage manifest."""
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


# ---------------------------------------------------------------------------
# --init-lock migration (Ch6; R6/I3)
# ---------------------------------------------------------------------------

class TestInitLock:
    def test_migrates_and_marks_unrecoverable(self, tmp_path: Path) -> None:
        assert _install(tmp_path) == 0
        # simulate a pre-lockfile tree
        (tmp_path / "dev" / "cairn-lock.yml").unlink()
        import shutil
        shutil.rmtree(tmp_path / "dev" / ".cairn")
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
        (tmp_path / "dev" / "cairn-lock.yml").unlink()
        import shutil
        shutil.rmtree(tmp_path / "dev" / ".cairn")
        s.main(["upgrade", "--target", str(tmp_path), "--init-lock",
                "--cairn-root", str(CAIRN_ROOT)])
        capsys.readouterr()
        s.main(["upgrade", "--target", str(tmp_path), "--plan",
                "--cairn-root", str(CAIRN_ROOT)])
        out = capsys.readouterr().out
        assert "review-only" in out  # I3: no pretended 3-way merge

    def test_init_lock_follows_vendor_rename(self, tmp_path: Path) -> None:
        """#45: a renamed vendor wrapper (VENDOR.md -> CLAUDE.md) is resolved
        and tracked under its real dst, not dropped to untracked."""
        assert _install(tmp_path) == 0
        (tmp_path / "VENDOR.md").rename(tmp_path / "CLAUDE.md")  # adopter rename
        (tmp_path / "dev" / "cairn-lock.yml").unlink()
        import shutil
        shutil.rmtree(tmp_path / "dev" / ".cairn")
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
        (tmp_path / "dev" / "cairn-lock.yml").unlink()
        import shutil
        shutil.rmtree(tmp_path / "dev" / ".cairn")
        capsys.readouterr()
        assert s.main(["upgrade", "--target", str(tmp_path), "--init-lock",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        err = capsys.readouterr().err
        assert "vendor wrapper" in err and "untracked" in err
        dsts = {r["dst"] for r in s.read_lockfile(tmp_path)["files"]}
        assert "VENDOR.md" not in dsts
        assert not (dsts & set(s._KNOWN_VENDOR_WRAPPERS))  # no wrong-file record


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
        (target / "dev" / "cairn-lock.yml").unlink()
        import shutil
        shutil.rmtree(target / "dev" / ".cairn")
        assert s.main(["upgrade", "--target", str(target), "--init-lock",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0

    def _review_only_dst(self, target: Path) -> str:
        """A nested, non-verbatim (token-substituted) tracked file -> review-only
        after --init-lock.  Nested ('/') to exercise the parent-mkdir path (S2)."""
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
        # B1: the pair lives OUTSIDE files/ so it cannot trip apply's exactness.
        files_dir = tmp_path / "dev" / ".cairn-upgrade" / "files"
        staged = ({str(p.relative_to(files_dir)) for p in files_dir.rglob("*")
                   if p.is_file()} if files_dir.exists() else set())
        assert dst not in staged

    def test_stage_review_only_file_missing_only_theirs(self, tmp_path: Path) -> None:
        """LHM's actual incident shape: a tracked file missing on disk (a
        default-on module slot that never installed).  Only ``.theirs`` is
        written -- there is no on-disk ``.ours`` to pair (Antigravity S2 /
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
        rmtree cleans the whole stage incl. review-only/ (B1)."""
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

    def test_review_only_never_in_advancing_set(self, tmp_path: Path) -> None:
        """A review-only dst is recorded in the stage's review_only list but
        never in staged_files (the advancing set --apply swaps)."""
        self._init_locked(tmp_path)
        ro_dst = self._review_only_dst(tmp_path)
        assert s.main(["upgrade", "--target", str(tmp_path), "--stage",
                       "--cairn-root", str(CAIRN_ROOT)]) == 0
        meta = json.loads(
            (tmp_path / "dev" / ".cairn-upgrade" / s._STAGE_META).read_text())
        assert ro_dst in meta["review_only"]
        assert ro_dst not in meta["staged_files"]


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
        (target / "dev" / "cairn-lock.yml").write_text(
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
