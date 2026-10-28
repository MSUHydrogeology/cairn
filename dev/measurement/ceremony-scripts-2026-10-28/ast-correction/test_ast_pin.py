"""Tests for ast_pin.py.  Every run is against a scratch clone of the repository, never the real
tree: the clone shares objects with it (read-only) and gets the gate-anchor ref copied in.
The one thing that touches the real repo is a read of its `git status`, to prove nothing changed."""
import json, os, re, subprocess, sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ast_pin as P

REAL = Path("/Users/kendal30/Code/cairn")
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"


def g(repo, *a):
    return subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, check=True).stdout


def commit(repo, msg, *paths):
    g(repo, "-c", "commit.gpgsign=false", "-c", "user.name=t", "-c", "user.email=t@invalid",
      "commit", "--no-verify", "-q", "-m", msg, *paths)


@pytest.fixture
def clone(tmp_path):
    c = tmp_path / "clone"
    subprocess.run(["git", "clone", "-q", "--shared", str(REAL), str(c)], check=True)
    g(c, "fetch", "-q", str(REAL), "+refs/cairn/gate-anchor:refs/cairn/gate-anchor")
    g(c, "checkout", "-q", "--detach", g(REAL, "rev-parse", "HEAD").strip())
    return c


def state(repo):
    return (g(repo, "status", "--short", "--ignored"), g(repo, "worktree", "list"), g(repo, "rev-parse", "HEAD"),
            [(Path(repo) / r).read_bytes() for r in (P.BASE, P.KNOWN)])


def test_dry_run_on_untouched_clone_passes_and_writes_nothing(clone, capsys):
    before, real_before = state(clone), g(REAL, "status", "--short")
    assert P.main(["--repo", str(clone)]) == 0
    out = capsys.readouterr().out
    assert "DRY RUN" in out and "AST attestation OK" in out and "IDENTICAL" in out
    assert state(clone) == before          # no file, no index change, no leftover worktree, same HEAD
    assert g(REAL, "status", "--short") == real_before


def test_fifth_missing_symbol_is_refused(clone, capsys):
    base = json.loads((clone / P.BASE).read_bytes())
    base["Assign:_A_FIFTH_SYMBOL"] = next(iter(base.values()))
    (clone / P.BASE).write_bytes(P.dump(base))
    commit(clone, "baseline gains a symbol the engine does not have", P.BASE)
    before = state(clone)
    assert P.main(["--repo", str(clone)]) == 2
    err = capsys.readouterr().err
    assert "_A_FIFTH_SYMBOL" in err and "expected exactly the four" in err
    assert state(clone) == before


def test_wrong_deleting_commit_is_refused(clone, capsys):
    before = state(clone)
    assert P.main(["--repo", str(clone), "--deleted-by", "HEAD~1"]) == 2
    assert "latest commit touching" in capsys.readouterr().err
    assert state(clone) == before


@pytest.mark.parametrize("tamper, expect", [
    ("lockfile", "unexpected files"),
    ("extra_known_new", "ADDED"),
    ("changed_unchanged_baseline_symbol", "CHANGED"),
])
def test_unexpected_transaction_content_is_refused(clone, capsys, monkeypatch, tamper, expect):
    real_check = P.check_txn

    def tampered(txn, *rest):
        o = txn["outputs"]
        if tamper == "lockfile":
            o["dev/.cairn/cairn-lock.yml"] = {"new_text": "x", "new_sha256": P.sha(b"x")}
        else:
            rel = P.KNOWN if tamper == "extra_known_new" else P.BASE
            doc = json.loads(o[rel]["new_text"])
            if tamper == "extra_known_new":
                doc["FunctionDef:_smuggled"] = ["0" * 16]
            else:  # a baseline symbol repin did not list as CHANGED
                k = next(k for k in doc if k.startswith("ClassDef"))
                doc[k]["digest"] = "0" * 16
            raw = P.dump(doc)
            o[rel] = {**o[rel], "new_text": raw.decode(), "new_sha256": P.sha(raw)}
        return real_check(txn, *rest)

    monkeypatch.setattr(P, "check_txn", tampered)
    assert P.main(["--repo", str(clone)]) == 2
    assert expect in capsys.readouterr().err


def test_checker_can_fail(clone):
    """Instrument control: attest_ok must refuse the OLD fixtures, else 'OK' would prove nothing."""
    with pytest.raises(P.Stop):
        P.attest_ok(clone, clone / P.BASE, clone / P.KNOWN)


def test_apply_writes_exactly_the_two_fixtures_and_the_engine_verifies(clone, capsys):
    assert P.main(["--repo", str(clone), "--apply"]) == 0
    out = capsys.readouterr().out
    changed = sorted(l for l in g(clone, "status", "--short").splitlines())
    assert changed == [f" M {P.BASE}", f" M {P.KNOWN}"]          # nothing else, no untracked files
    assert "git commit " + P.BASE + " " + P.KNOWN in out and "passed" in out
    shown = {rel: digest for digest, rel in re.findall(r"([0-9a-f]{64})  (bootstrap\S+)", out)}
    assert set(shown) == {P.BASE, P.KNOWN}
    for rel, digest in shown.items():
        assert P.sha((clone / rel).read_bytes()) == digest      # the printed digest is the file's digest
    r = subprocess.run([sys.executable, "-I", "-B", "bootstrap/tests/_ast_attest.py", "verify", P.BASE,
                        "--known-new", P.KNOWN, *sorted(str(p.relative_to(clone)) for p in (clone / P.ENGINE).glob("*.py"))],
                       cwd=clone, capture_output=True, text=True)
    assert r.returncode == 0 and "AST attestation OK — 169" in r.stdout
    assert g(clone, "log", "-1", "--format=%H").strip() == g(REAL, "rev-parse", "HEAD").strip()  # not committed


def test_apply_refuses_when_a_fixture_is_already_edited(clone, capsys):
    (clone / P.KNOWN).write_text("{}\n")
    before = (clone / P.KNOWN).read_bytes(), (clone / P.BASE).read_bytes()
    assert P.main(["--repo", str(clone), "--apply"]) == 2
    assert "differs from HEAD" in capsys.readouterr().err
    assert ((clone / P.KNOWN).read_bytes(), (clone / P.BASE).read_bytes()) == before
