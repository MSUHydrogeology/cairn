#!/usr/bin/env python3
"""Phase 4 — the **two-stage** supervised re-anchor (executable evidence /
data-only promotion), per the round-4 final contract (Codex, 2026-06-11).

The earlier all-in-one ``promote`` conflated *evidence gathering* (which executes
candidate code) with *promotion* (which the plan requires to be **data-only**),
and called a mutable working-tree manifest write a completed external re-anchor.
This module replaces it with the agreed contract:

**Stage A — evidence (executable, NON-authoritative)** — :func:`gather_evidence`.
Resolve candidate ``C`` to an immutable SHA, **materialize it into an isolated,
credential-scrubbed temp tree** (never the live target), run activation, the
differential oracle over the required scenarios, and the pytest collection needed
to derive the **prospective manifest**, and emit a deterministic
:class:`EvidenceBundle`. Evidence alone updates no ref and consumes no authority,
so its seams may be injected for testing — Stage B re-verifies everything.

**Stage B — promotion (data-only, AUTHORITATIVE)** — :func:`promote_data_only`.
Run trusted code at the immutable anchor ``A``; resolve the promotion
authorization + trusted activation from the **git object at ``A``** (not arbitrary
paths); verify the authorization exactly binds ``A``, ``C``, the evidence-bundle
hash, every authorized changed-file hash, the checker hash, and the prospective
manifest bytes; **execute no candidate code** (git-object reads only); construct
the new immutable anchor ``N = C + the trusted manifest commit`` via plumbing and
prove ``N`` differs from ``C`` only by ``gate_manifest.json``; **atomically
advance the one designated trusted ref ``A → N`` via ``git update-ref`` expected-
old compare-and-swap** — that ref update is the single-use authority and replay
defense; then statically verify ``N``. ``reanchored=True`` only after the CAS and
the verify succeed; a failure before the CAS leaves authority untouched.

Run from the trusted ``master`` checkout. *Advancing the designated ref* is the
Maintainer's supervised act — guarded by explicit confirmation. Stdlib only.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path

try:  # package import (pytest)
    from bootstrap.tests import _oracle as O
    from bootstrap.tests import _oracle_activation as A
    from bootstrap.tests import _gate_transition as G
    from bootstrap.tests import _gate_manifest as M
    from bootstrap.tests import _oracle_trust as _trust
except ImportError:  # script mode
    import _oracle as O
    import _oracle_activation as A
    import _gate_transition as G
    import _gate_manifest as M
    import _oracle_trust as _trust

_MANIFEST_REL = "bootstrap/tests/fixtures/gate_manifest.json"
_ACTIVATION_REL = "dev/.cairn/active-refactor.yml"               # evaluated, in the candidate tree
_AUTHZ_REL = "dev/.cairn/promotion-authorization.yml"           # authority bundle @ A
_TRUSTED_ACT_REL = "dev/.cairn/trusted-activation.yml"          # authority bundle @ A
_DESIGNATED_REF = "refs/cairn/gate-anchor"                      # the ONE designated gate ref (fixed by trusted code)
_AUTHORIZATION_REF = "refs/cairn/gate-authorization"           # the ONE authorization ref A is resolved from

# Fixed authoring identity + dates so the constructed anchor N is deterministic.
_REANCHOR_ENV = {
    "GIT_AUTHOR_NAME": "cairn-reanchor", "GIT_AUTHOR_EMAIL": "reanchor@cairn",
    "GIT_COMMITTER_NAME": "cairn-reanchor", "GIT_COMMITTER_EMAIL": "reanchor@cairn",
    "GIT_AUTHOR_DATE": "2000-01-01T00:00:00 +0000",
    "GIT_COMMITTER_DATE": "2000-01-01T00:00:00 +0000",
}

# Substrings that mark a credential-bearing env var; scrubbed for Stage A.
_CREDENTIAL_HINTS = ("TOKEN", "SECRET", "PASSWORD", "PASSWD", "CREDENTIAL",
                     "AWS_", "GITHUB_", "GH_TOKEN", "SSH_", "GPG_", "NPM_", "PYPI_",
                     "ANTHROPIC", "OPENAI")


def _sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _git(repo: Path, *args: str, input_bytes: bytes | None = None,
         env: dict | None = None, want_bytes: bool = False):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        input=input_bytes, capture_output=True, check=False,
        env=env, text=not want_bytes if input_bytes is None else False)


def _resolve_sha(repo: Path, ref: str) -> str:
    p = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}"],
        capture_output=True, text=True, check=False)
    sha = (p.stdout or "").strip()
    if p.returncode != 0 or len(sha) != 40 or any(c not in "0123456789abcdef" for c in sha):
        raise ValueError(f"ref does not resolve to a commit: {ref!r} ({p.stderr.strip()})")
    return sha


def _git_show_bytes(repo: Path, sha: str, rel: str) -> bytes | None:
    p = subprocess.run(["git", "-C", str(repo), "show", f"{sha}:{rel}"],
                       capture_output=True, check=False)
    return p.stdout if p.returncode == 0 else None


@contextlib.contextmanager
def _scrubbed_environ():
    """Best-effort credential-free environment for Stage A (contained, not
    hermetic): drop credential-bearing vars, point HOME at a throwaway, and block
    interactive git prompts. Subprocesses spawned within inherit the scrub."""
    saved = dict(os.environ)
    tmp_home = tempfile.mkdtemp(prefix="cairn-evidence-home-")
    try:
        for k in list(os.environ):
            up = k.upper()
            if any(h in up for h in _CREDENTIAL_HINTS):
                os.environ.pop(k, None)
        os.environ["HOME"] = tmp_home
        os.environ["GIT_TERMINAL_PROMPT"] = "0"
        yield
    finally:
        os.environ.clear()
        os.environ.update(saved)


# --------------------------------------------------- trust-root authenticity

def _authority_code_files():
    """The modules whose executing code makes the promotion decision, mapped to
    their canonical repo-relative paths. Hashing the ACTUAL imported files (their
    ``__file__``) and comparing to P's pinned trusted hashes proves Stage B runs
    trusted verifier code, not whatever happens to be in the invoking checkout."""
    import sys as _sys
    mods = [_sys.modules[__name__], G, A, M, O, _trust]
    return [("bootstrap/tests/" + Path(m.__file__).name, m.__file__) for m in mods]


def _verify_executing_authority_code(trusted_repo: Path, prior_sha: str,
                                     *, include_preflight: bool = False) -> tuple[bool, list[str]]:
    """Pin the EXECUTING authority code against the immutable trusted gate manifest
    at the prior gate state ``P`` (re-review round-5 Finding 1b). Refuses if a
    verifier module is unpinned or its running bytes differ from P's frozen hash."""
    raw = _git_show_bytes(trusted_repo, prior_sha, _MANIFEST_REL)
    if raw is None:
        return False, [f"prior gate manifest absent at P {prior_sha[:12]} — cannot pin authority code"]
    try:
        prior_manifest = json.loads(raw)
        frozen = prior_manifest.get("frozen_files", {})
    except json.JSONDecodeError:
        return False, ["prior gate manifest at P is unparseable — cannot pin authority code"]
    refusals: list[str] = []
    for rel, path in _authority_code_files():
        entry = frozen.get(rel)
        pinned = M._entry_sha256(entry) if entry is not None else None
        if pinned is None:
            refusals.append(f"authority code {rel} is not pinned in P's trusted gate manifest")
            continue
        actual = hashlib.sha256(Path(path).read_bytes()).hexdigest()      # P frozen hashes are bare hex
        if actual != pinned:
            refusals.append(f"executing authority code {rel} differs from P's pinned hash "
                            f"(untrusted verifier code in the invoking checkout)")
    if include_preflight:
        # _gate_preflight is not imported in this process yet. Validate the
        # exact source object that the trusted loader will execute below.
        rel = "bootstrap/tests/_gate_preflight.py"
        entry = frozen.get(rel)
        source = _git_show_bytes(trusted_repo, prior_sha, rel)
        if entry is None:
            refusals.append(f"authority code {rel} is not pinned in P's trusted gate manifest")
        elif source is None or hashlib.sha256(source).hexdigest() != M._entry_sha256(entry):
            refusals.append(f"authority code {rel} differs from P's pinned hash")
    return (not refusals), refusals


def _load_pinned_preflight(trusted_repo: Path, prior_sha: str):
    """Execute only the preflight source bytes pinned by roster-installed P."""
    import sys
    import types
    rel = "bootstrap/tests/_gate_preflight.py"
    manifest_raw = _git_show_bytes(trusted_repo, prior_sha, _MANIFEST_REL)
    source = _git_show_bytes(trusted_repo, prior_sha, rel)
    if manifest_raw is None or source is None:
        raise RuntimeError("prior anchor does not carry the preflight authority source")
    manifest = json.loads(manifest_raw)
    entry = manifest.get("frozen_files", {}).get(rel)
    if entry is None or hashlib.sha256(source).hexdigest() != M._entry_sha256(entry):
        raise RuntimeError("prior anchor does not authenticate preflight authority source")
    # Its source imports the already-loaded, authority-pinned M and this R.
    # Install those identities under both supported import spellings before
    # executing the anchored source, so Python cannot resolve a second copy
    # from the invoking checkout or an import-path shadow.
    current = sys.modules.get(__name__)
    package = sys.modules.get("bootstrap.tests")
    aliases = {
        "bootstrap.tests._gate_manifest": M,
        "bootstrap.tests._gate_reanchor": current,
        "_gate_manifest": M,
        "_gate_reanchor": current,
    }
    if current is None:
        raise RuntimeError("executing reanchor module is not registered")
    if package is not None:
        for short, obj in (("_gate_manifest", M), ("_gate_reanchor", current)):
            existing = getattr(package, short, None)
            if existing is not None and existing is not obj:
                raise RuntimeError(f"trusted import package conflicts at {short}")
            setattr(package, short, obj)
    for alias, obj in aliases.items():
        if obj is None:
            continue
        existing = sys.modules.get(alias)
        if existing is not None and existing is not obj:
            raise RuntimeError(f"trusted import alias conflicts at {alias}")
        sys.modules[alias] = obj

    module_name = ("bootstrap.tests._gate_preflight_stage_b_"
                   + hashlib.sha256(source).hexdigest())
    if module_name in sys.modules:
        raise RuntimeError("pinned preflight module identity is already occupied")
    module = types.ModuleType(module_name)
    module.__file__ = str(Path(trusted_repo).resolve() / rel)
    module.__package__ = "bootstrap.tests"
    sys.modules[module_name] = module
    try:
        exec(compile(source, module.__file__, "exec"), module.__dict__)
    except BaseException:
        sys.modules.pop(module_name, None)
        raise
    return module


def _static_verify_anchor(trusted_repo: Path, n_sha: str, prospective_bytes: str) -> bool:
    """Run the EXISTING trusted gate verifier statically against the immutable
    anchor ``N``: **materialize ``N`` into a temp
    tree and check the frozen-file / mapping state against THAT tree** (``repo=<N>``)
    — not the invoking working tree — so verification follows ``N`` regardless of
    whatever happens to be checked out. The verifier code and the anchor object are
    still resolved from the trusted checkout (``trusted_repo``); the candidate is
    never executed (``do_collect=False``)."""
    trusted_repo = Path(trusted_repo)
    with tempfile.TemporaryDirectory(prefix="cairn-anchor-verify-") as td:
        n_tree = Path(td) / "N"
        _trust.extract_ref_tree(n_sha, n_tree, trusted_repo)        # N's tree, as data
        manifest_in_n = n_tree / _MANIFEST_REL
        if not manifest_in_n.is_file() or manifest_in_n.read_text(encoding="utf-8") != prospective_bytes:
            return False                                            # N must carry the reviewed manifest
        with open(os.devnull, "w") as devnull:
            rc = M.verify(manifest_in_n, anchor_ref=n_sha, repo=n_tree,
                          do_collect=False, out=devnull,
                          trusted_repo=trusted_repo, trusted_ref=n_sha)
    return rc == 0


# --------------------------------------------------------------------- Stage A

@dataclass
class EvidenceBundle:
    candidate_sha: str
    prior_anchor: str
    required_scenarios: list[str]
    scenario_results: dict[str, str]            # name -> status ("match")
    prospective_manifest_bytes: str             # the manifest Stage A derived for C
    prospective_manifest_hash: str              # sha256 of the above
    checker_hash: str                           # sha256 of the candidate's transition checker
    oracle_ok: bool

    def canonical(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))

    def digest(self) -> str:
        return _sha256_bytes(self.canonical().encode("utf-8"))


def gather_evidence(
    *,
    trusted_repo: Path,
    candidate_ref: str,
    prior_anchor: str,
    workdir: Path,
    baseline_ref: str | None = None,
    trusted_ref: str | None = None,
    required_scenarios: list[str] | None = None,
    run_oracle_fn=None,
    produce_fn=None,
    materialize_fn=None,
    env_scrub: bool = True,
    manifest_rel: str = _MANIFEST_REL,
    checker_rel: str = "bootstrap/tests/_gate_transition.py",
) -> EvidenceBundle:
    """**Stage A.** Materialize candidate ``C`` into an isolated, credential-scrubbed
    temp tree and gather the (NON-authoritative) evidence bundle. Never executes
    from the live target. The seams (*run_oracle_fn*, *produce_fn*,
    *materialize_fn*) exist because evidence is non-authoritative — Stage B
    re-verifies the bundle hash + every candidate byte against git objects."""
    run_oracle_fn = run_oracle_fn or O.run_oracle
    produce_fn = produce_fn or M.produce
    materialize_fn = materialize_fn or _trust.extract_ref_tree
    workdir = Path(workdir)

    candidate_sha = _resolve_sha(trusted_repo, candidate_ref)
    prior_sha = _resolve_sha(trusted_repo, prior_anchor)
    # Membership is read from the prior signed gate manifest. A roster-less
    # anchor keeps the legacy broad policy; this public path cannot establish
    # the new initial roster or admit a candidate replacement.
    protected_roster = M._trusted_roster_from_anchor(
        prior_sha, candidate_sha, repo=trusted_repo)
    required = list(required_scenarios) if required_scenarios else [fx["name"] for fx in O.FIXTURES]

    mat = workdir / "_candidate_tree"
    materialize_fn(candidate_sha, mat, trusted_repo)            # isolated, credential-free tree

    scrub = _scrubbed_environ() if env_scrub else contextlib.nullcontext()
    with scrub:
        report = run_oracle_fn(workdir / "oracle", baseline_ref=baseline_ref,
                               trusted_ref=trusted_ref, repo=trusted_repo, target_root=mat)
        produced = (produce_fn(mat, protected_roster=protected_roster)
                    if protected_roster is not None else produce_fn(mat))
        prospective = json.dumps(produced, indent=2, sort_keys=True) + "\n"

    matched = {f["name"]: f["status"] for f in report.get("fixtures", [])}
    matched.update({p["name"]: p["status"] for p in report.get("privileged", [])})
    checker_bytes = (mat / checker_rel).read_bytes() if (mat / checker_rel).is_file() else b""

    return EvidenceBundle(
        candidate_sha=candidate_sha, prior_anchor=prior_sha,
        required_scenarios=required,
        scenario_results={s: matched.get(s, "absent") for s in required},
        prospective_manifest_bytes=prospective,
        prospective_manifest_hash=_sha256_bytes(prospective.encode("utf-8")),
        checker_hash=_sha256_bytes(checker_bytes),
        oracle_ok=bool(report.get("ok")) and report.get("status") == "ran",
    )


# --------------------------------------------------------------------- Stage B

@dataclass
class PromotionResult:
    ok: bool
    candidate_sha: str | None
    new_anchor: str | None = None               # N, once constructed / advanced
    refusals: list[str] = field(default_factory=list)
    checks: dict[str, bool] = field(default_factory=dict)
    ref_advanced: bool = False
    reanchored: bool = False


def _construct_anchor_commit(repo: Path, candidate_sha: str, manifest_rel: str,
                             manifest_bytes: bytes) -> str:
    """**Data-only** construction of ``N = C + the manifest commit`` via git
    plumbing — NO candidate code is executed (no checkout, no collection): read C's
    tree into a temp index, insert the trusted manifest blob, write the tree, and
    commit-tree on top of C with a fixed deterministic identity."""
    with tempfile.TemporaryDirectory(prefix="cairn-anchor-idx-") as td:
        env = dict(os.environ, GIT_INDEX_FILE=str(Path(td) / "index"), **_REANCHOR_ENV)
        rt = subprocess.run(["git", "-C", str(repo), "read-tree", candidate_sha],
                            capture_output=True, text=True, env=env, check=False)
        if rt.returncode != 0:
            raise RuntimeError(f"read-tree {candidate_sha[:12]} failed: {rt.stderr.strip()}")
        ho = subprocess.run(["git", "-C", str(repo), "hash-object", "-w", "--stdin"],
                            input=manifest_bytes, capture_output=True, env=env, check=False)
        if ho.returncode != 0:
            raise RuntimeError(f"hash-object failed: {ho.stderr.decode('utf-8', 'replace')[:200]}")
        blob = ho.stdout.decode().strip()
        ui = subprocess.run(["git", "-C", str(repo), "update-index", "--add",
                             "--cacheinfo", f"100644,{blob},{manifest_rel}"],
                            capture_output=True, text=True, env=env, check=False)
        if ui.returncode != 0:
            raise RuntimeError(f"update-index failed: {ui.stderr.strip()}")
        wt = subprocess.run(["git", "-C", str(repo), "write-tree"],
                            capture_output=True, text=True, env=env, check=False)
        tree = wt.stdout.strip()
        if wt.returncode != 0 or not tree:
            raise RuntimeError(f"write-tree failed: {wt.stderr.strip()}")
        ct = subprocess.run(["git", "-C", str(repo), "commit-tree", tree,
                             "-p", candidate_sha, "-m", "cairn: supervised gate re-anchor (N = C + manifest)"],
                            capture_output=True, text=True, env=env, check=False)
        n = ct.stdout.strip()
        if ct.returncode != 0 or len(n) != 40:
            raise RuntimeError(f"commit-tree failed: {ct.stderr.strip()}")
        return n


def _diff_name_only(repo: Path, a: str, b: str) -> list[str]:
    out = subprocess.run(["git", "-C", str(repo), "diff", "--name-only", f"{a}..{b}"],
                         capture_output=True, text=True, check=False)
    return [f for f in out.stdout.splitlines() if f.strip()]


def _cas_advance_ref(repo: Path, ref: str, new_sha: str, expected_old: str) -> tuple[bool, str]:
    """Atomically advance *ref* from *expected_old* to *new_sha* (git's native
    compare-and-swap). Returns (ok, detail). A stale/changed ref refuses — this is
    the single-use authority + replay defense."""
    p = subprocess.run(["git", "-C", str(repo), "update-ref", ref, new_sha, expected_old],
                       capture_output=True, text=True, check=False)
    return (p.returncode == 0), (p.stderr.strip() or p.stdout.strip())


def promote_data_only(
    *,
    trusted_repo: Path,
    anchor_ref: str,
    evidence: EvidenceBundle,
    designated_ref: str = _DESIGNATED_REF,
    confirm: bool = False,
    authz_rel: str = _AUTHZ_REL,
    trusted_act_rel: str = _TRUSTED_ACT_REL,
    manifest_rel: str = _MANIFEST_REL,
    activation_rel: str = _ACTIVATION_REL,
    is_sensitive=A.is_sensitive,
    verify_anchor_fn=None,
) -> PromotionResult:
    """**Stage B.** Data-only, authoritative promotion. Resolves the authorization
    from the git object at ``A``, verifies it binds the evidence + candidate
    exactly, executes **no** candidate code, constructs ``N`` and (with *confirm*)
    advances the designated ref ``A → N`` via expected-old CAS, then statically
    verifies ``N``. Without *confirm* it stops before the CAS and reports the
    prepared ``N`` (``reanchored=False``) — advancing the ref is the supervised act."""
    trusted_repo = Path(trusted_repo)
    refusals: list[str] = []
    checks: dict[str, bool] = {}

    A_sha = _resolve_sha(trusted_repo, anchor_ref)
    candidate_sha = evidence.candidate_sha

    # (1) Authority bundle resolved from the IMMUTABLE git object at A (no paths).
    authz_bytes = _git_show_bytes(trusted_repo, A_sha, authz_rel)
    tact_bytes = _git_show_bytes(trusted_repo, A_sha, trusted_act_rel)
    if authz_bytes is None or tact_bytes is None:
        return PromotionResult(ok=False, candidate_sha=candidate_sha,
                               refusals=[f"authority bundle absent at anchor {A_sha[:12]} "
                                         f"({authz_rel} / {trusted_act_rel})"], checks=checks)
    try:
        manifest = G.parse_promotion(authz_bytes.decode("utf-8"))
        trusted_act = A.parse_activation(tact_bytes.decode("utf-8"))
    except (G.PromotionError, A.ActivationError) as e:
        return PromotionResult(ok=False, candidate_sha=candidate_sha,
                               refusals=[f"authority bundle malformed: {e}"], checks=checks)

    # The prior gate state P is the manifest's declared prior, INDEPENDENTLY
    # confirmed to be the designated ref's current head (so a manifest cannot lie
    # about what it builds on). The authorization's binding to the authority anchor
    # A is positional — it was read from the immutable git object AT A.
    P = manifest.prior_anchor
    try:
        gate_head = _resolve_sha(trusted_repo, designated_ref)
    except ValueError:
        gate_head = None

    # (2) The reviewed authorization must bind C, the evidence hash, the
    #     prospective manifest bytes, and the prior gate state — exactly.
    checks["gate_ref_at_prior"] = (gate_head is not None and gate_head == P)
    checks["binds_candidate"] = (manifest.candidate_sha == candidate_sha == evidence.candidate_sha)
    checks["binds_evidence_hash"] = (manifest.evidence_hash == evidence.digest())
    checks["binds_prospective_manifest"] = (
        manifest.prospective_manifest_hash == evidence.prospective_manifest_hash
        and manifest.prospective_manifest_hash == _sha256_bytes(
            evidence.prospective_manifest_bytes.encode("utf-8")))
    checks["evidence_oracle_ok"] = bool(evidence.oracle_ok)
    checks["required_scenarios_matched"] = all(
        evidence.scenario_results.get(s) == "match" for s in trusted_act.required_scenarios) \
        and bool(trusted_act.required_scenarios)

    # (2a) Authority-anchor AUTHENTICITY: A must be a one-parent
    #      authorization commit on P whose diff from P is ONLY the bounded
    #      authorization artifacts — so an attacker cannot mint a self-consistent A
    #      that also smuggles candidate content. (The fixed authorization ref that A
    #      is resolved from is enforced by `promote`, the production entry point.)
    rl = subprocess.run(["git", "-C", str(trusted_repo), "rev-list", "--parents", "-n", "1", A_sha],
                        capture_output=True, text=True, check=False)
    a_parents = rl.stdout.split()[1:] if rl.returncode == 0 else []
    checks["authority_anchor_parent"] = (len(a_parents) == 1 and a_parents[0] == P)
    a_diff = _diff_name_only(trusted_repo, P, A_sha) if checks["gate_ref_at_prior"] else ["<prior-unknown>"]
    checks["authority_bounded_diff"] = (bool(a_diff) and set(a_diff) <= {authz_rel, trusted_act_rel})

    # (2b) Authority-CODE pin: the executing verifier code must match
    #      P's trusted gate manifest — reading authority DATA from A is not enough.
    roster = None
    roster_resolution_error = None
    if checks["gate_ref_at_prior"]:
        try:
            roster = M._trusted_roster_from_anchor(P, candidate_sha, repo=trusted_repo)
        except Exception as exc:
            roster_resolution_error = str(exc)
    code_ok, code_holds = _verify_executing_authority_code(
        trusted_repo, P, include_preflight=roster is not None) \
        if checks["gate_ref_at_prior"] else (
            False, ["prior gate state unknown — cannot pin authority code"])
    checks["authority_code_pinned"] = code_ok

    # Independently bind the prospective membership and static manifest fields
    # to P and C before any anchor commit is constructed. The producer's pytest
    # collection remains evidence; the producer cannot choose the frozen set.
    static_ok = False
    static_error = "executing authority code is not pinned by P"
    if code_ok:
        try:
            if roster_resolution_error:
                raise RuntimeError(roster_resolution_error)
            proposed = json.loads(evidence.prospective_manifest_bytes)
            if roster is not None:
                # Execute source read from P only after its hash is matched to
                # P's signed frozen entry. Never import the invoking checkout's
                # copy on the authority path.
                P_gate = _load_pinned_preflight(trusted_repo, P)
                static = P_gate.rederive_static_manifest(
                    candidate_sha, protected_roster=roster, repo=trusted_repo)
                expected_fields = ((set(static) - {"object_format"})
                                   | set(P_gate._EXECUTABLE_ONLY_FIELDS))
                report = P_gate.Report()
                P_gate.check_static_manifest(
                    {"manifest": proposed}, candidate_sha, report,
                    protected_roster=roster, repo=trusted_repo)
                static_ok = (set(proposed) == expected_fields
                             and not any(f.level == "refuse" for f in report.findings))
            else:
                # A roster-less prior anchor keeps the old broad policy. The
                # legacy callable may neither emit a narrowed roster nor omit
                # a tracked frozen path or substitute its digest.
                if "protected_roster" in proposed:
                    raise ValueError("legacy path cannot install a protected roster")
                # The old signed closure predates _gate_preflight. Preserve its
                # broad frozen policy using only already-pinned M and _trust.
                with tempfile.TemporaryDirectory(prefix="cairn-legacy-static-") as td:
                    tree = _trust.extract_ref_tree(candidate_sha, Path(td) / "candidate",
                                                   trusted_repo)
                    blob_ids = M._tree_blobs(trusted_repo, candidate_sha)
                    expected = {
                        rel: M._blob_sha256(trusted_repo, blob_ids[rel][1])
                        for rel in M._legacy_frozen_files(tree)
                        if rel in blob_ids
                    }
                actual = {rel: M._entry_sha256(value)
                          for rel, value in proposed.get("frozen_files", {}).items()}
                static_ok = actual == expected
                if not static_ok:
                    static_error = "legacy broad frozen set or digest differs from candidate objects"
            static_error = "candidate fields differ from trusted raw-tree derivation"
        except Exception as exc:
            static_error = str(exc)
    checks["trusted_manifest_derivation"] = static_ok
    if not static_ok:
        refusals.append(f"manifest: {static_error}")

    for name, ok in (("gate_ref_at_prior", f"designated ref {designated_ref} is not at the "
                      f"manifest's prior gate state (stale/wrong prior)"),
                     ("authority_anchor_parent", "authority anchor A is not a one-parent commit on P"),
                     ("authority_bounded_diff", "authority anchor A changes more than the bounded "
                      "authorization artifacts (diff P..A not limited to the authz bundle)"),
                     ("trusted_manifest_derivation", "candidate manifest does not match the prior roster and raw tree"),
                     ("binds_candidate", "authorization candidate_sha != C/evidence"),
                     ("binds_evidence_hash", "authorization evidence_hash != Stage-A bundle digest"),
                     ("binds_prospective_manifest", "authorization prospective_manifest_hash != evidence"),
                     ("evidence_oracle_ok", "Stage-A oracle did not pass"),
                     ("required_scenarios_matched", "a required scenario is not matched in the evidence")):
        if not checks[name]:
            refusals.append(ok)
    refusals.extend(f"authority-code: {h}" for h in code_holds)

    # (3) Data-only candidate-byte validation (git objects only; never executes C).
    ok_files, holds = G.check_promotion(
        trusted_repo, manifest, prior_anchor_actual=P,
        candidate=candidate_sha, is_sensitive=is_sensitive)
    checks["data_only_files"] = ok_files
    refusals.extend(f"files: {h}" for h in holds)

    # (3b) Data-only activation acceptance vs the trusted expectation @ A. The
    #      evaluated activation is read from the candidate git OBJECT (no checkout).
    eval_act_bytes = _git_show_bytes(trusted_repo, candidate_sha, activation_rel)
    with tempfile.TemporaryDirectory(prefix="cairn-eval-act-") as td:
        eval_path = Path(td) / "active-refactor.yml"
        if eval_act_bytes is not None:
            eval_path.write_bytes(eval_act_bytes)
        ok_act, holds_act, _changed = A.run_acceptance(
            trusted_repo, P, candidate_sha, trusted_expectation=trusted_act,
            evaluated_activation_path=eval_path, is_sensitive_fn=is_sensitive)
    checks["data_only_activation"] = ok_act
    refusals.extend(f"activation: {h}" for h in holds_act)

    if refusals:
        return PromotionResult(ok=False, candidate_sha=candidate_sha,
                               refusals=refusals, checks=checks)

    # (4) Construct N = C + the trusted manifest commit (data-only plumbing); prove
    #     N differs from C only by the gate manifest.
    n_sha = _construct_anchor_commit(
        trusted_repo, candidate_sha, manifest_rel,
        evidence.prospective_manifest_bytes.encode("utf-8"))
    changed = _diff_name_only(trusted_repo, candidate_sha, n_sha)
    checks["anchor_minimal"] = (changed == [manifest_rel])
    if not checks["anchor_minimal"]:
        return PromotionResult(ok=False, candidate_sha=candidate_sha, new_anchor=n_sha,
                               refusals=[f"constructed anchor N changes more than the manifest: {changed}"],
                               checks=checks)

    # (4b) Completion proof: the EXISTING trusted gate verifier must
    #      accept N as the immutable anchor — not merely byte-identity. Run it
    #      statically (data-only) BEFORE the CAS, so a malformed-but-byte-identical
    #      prospective manifest refuses without spending authority.
    verify_anchor_fn = verify_anchor_fn or _static_verify_anchor
    checks["anchor_static_verified"] = bool(
        verify_anchor_fn(trusted_repo, n_sha, evidence.prospective_manifest_bytes))
    if not checks["anchor_static_verified"]:
        return PromotionResult(ok=False, candidate_sha=candidate_sha, new_anchor=n_sha,
                               refusals=["static gate verification of N failed (the existing gate "
                                         "verifier does not accept the prospective manifest at N)"],
                               checks=checks)

    # (5) Authority: advance the ONE designated ref A -> N via expected-old CAS.
    #     This is the supervised act — guarded by `confirm`.
    if not confirm:
        return PromotionResult(ok=True, candidate_sha=candidate_sha, new_anchor=n_sha,
                               checks=checks, ref_advanced=False, reanchored=False,
                               refusals=["prepared (data-only validated); supervised CAS advance "
                                         "pending — re-run with confirm=True / --confirm-supervised-reanchor"])
    advanced, detail = _cas_advance_ref(trusted_repo, designated_ref, n_sha, P)
    checks["cas_advanced"] = advanced
    if not advanced:
        return PromotionResult(ok=False, candidate_sha=candidate_sha, new_anchor=n_sha,
                               refusals=[f"expected-old CAS {designated_ref} {P[:12]}->{n_sha[:12]} "
                                         f"refused (stale/replayed anchor): {detail}"],
                               checks=checks, ref_advanced=False)

    # (6) Verify N statically from the trusted checkout (no candidate execution):
    #     the manifest in N must equal the reviewed prospective bytes.
    n_manifest = _git_show_bytes(trusted_repo, n_sha, manifest_rel)
    checks["anchor_verified"] = (n_manifest is not None
                                 and n_manifest.decode("utf-8") == evidence.prospective_manifest_bytes)
    if not checks["anchor_verified"]:
        return PromotionResult(ok=False, candidate_sha=candidate_sha, new_anchor=n_sha,
                               refusals=["post-advance verification failed: N's manifest != reviewed "
                                         "prospective bytes (loud recovery state tied to N)"],
                               checks=checks, ref_advanced=True, reanchored=False)
    return PromotionResult(ok=True, candidate_sha=candidate_sha, new_anchor=n_sha,
                           checks=checks, ref_advanced=True, reanchored=True)


# ------------------------------------------------------------------- orchestrate

def promote(
    *,
    trusted_repo: Path,
    candidate_ref: str,
    workdir: Path | None = None,
    baseline_ref: str | None = None,
    trusted_ref: str | None = None,
    confirm: bool = False,
) -> PromotionResult:
    """Run Stage A (evidence) then Stage B (data-only promotion). The production
    path is **not** dependency-injectable, and both authority refs are **fixed by
    trusted code**: the prior gate state ``P`` is the current head
    of the fixed designated ref, and the authority anchor ``A`` is resolved from the
    fixed authorization ref — neither is a caller-supplied SHA or ref. The
    designated-ref advance is gated by *confirm* (the Maintainer's supervised act)."""
    trusted_repo = Path(trusted_repo)
    P = _resolve_sha(trusted_repo, _DESIGNATED_REF)            # fixed gate ref → prior state P
    A_sha = _resolve_sha(trusted_repo, _AUTHORIZATION_REF)     # fixed authorization ref → A
    wd = Path(workdir) if workdir else Path(tempfile.mkdtemp(prefix="cairn-promote-"))
    evidence = gather_evidence(
        trusted_repo=trusted_repo, candidate_ref=candidate_ref, prior_anchor=P,
        workdir=wd, baseline_ref=baseline_ref, trusted_ref=trusted_ref)
    return promote_data_only(
        trusted_repo=trusted_repo, anchor_ref=A_sha, evidence=evidence,
        designated_ref=_DESIGNATED_REF, confirm=confirm)


# --------------------------------------------------------------------------- CLI

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="gate_reanchor", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, helptext in (("prepare", "Stage A+B through data-only validation; NO ref advance"),
                           ("promote", "SUPERVISED: + advance the designated ref A->N (expected-old CAS)")):
        p = sub.add_parser(name, help=helptext)
        p.add_argument("--repo", required=True, help="the TRUSTED checkout (authority + verifier)")
        p.add_argument("--candidate-ref", default="HEAD", help="candidate C ref in the trusted repo")
        p.add_argument("--baseline-ref", default=None, help="the oracle's pre-refactor baseline ref")
        p.add_argument("--trusted-ref", default=None, help="the oracle's out-of-band trusted ref")
        # The authority refs are FIXED by trusted code: A is resolved
        # from refs/cairn/gate-authorization and P from refs/cairn/gate-anchor — neither
        # is a CLI override, so the caller cannot redirect the authority or the one gate ref.
        if name == "promote":
            p.add_argument("--confirm-supervised-reanchor", action="store_true",
                           help="REQUIRED: confirm the Maintainer's supervised ref advance")
    args = ap.parse_args(argv)
    res = promote(
        trusted_repo=Path(args.repo), candidate_ref=args.candidate_ref,
        baseline_ref=args.baseline_ref, trusted_ref=args.trusted_ref,
        confirm=(args.cmd == "promote" and bool(args.confirm_supervised_reanchor)))
    print(f"[reanchor] candidate {(res.candidate_sha or '?')[:12]}  N={(res.new_anchor or '-')[:12]}  "
          f"ref_advanced={res.ref_advanced}  reanchored={res.reanchored}")
    for k, v in res.checks.items():
        print(f"  {'PASS' if v else 'FAIL'}  {k}")
    if res.ok and (args.cmd == "prepare" or res.reanchored):
        print("[reanchor] OK" + ("" if res.reanchored else " — prepared (supervised promote pending)."))
        return 0
    print("[reanchor] HOLD:", file=sys.stderr)
    for r in res.refusals:
        print(f"  {r}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
