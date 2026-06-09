# syntax=docker/dockerfile:1
#
# Cairn contained-kernel recipe — run the stdlib-only bootstrap engine at the
# install/upgrade boundary in a throwaway, contained container, with no
# host-installed Python and no Python in the adopter's application build/test CI.
#
# This is the v1 reference image for `bootstrap/container/recipe.md`. It targets
# the SETTLED install/upgrade CLI boundary (`scaffold.py`), not internal engine
# topology, so it survives engine refactors unchanged.
#
# Two privilege domains, kept separate (the narrowed trust boundary):
#   * BUILD  = the tail of Phase 1 (acquire + verify): the build context is a
#              VERIFIED, pinned Cairn checkout (the recipe's verify-ref.sh refuses
#              a mutable branch / unverified ref BEFORE building); the base image
#              is pinned BY DIGEST; the build bakes the engine and EMITS the
#              identity (Cairn commit + ref as OCI labels). No mutable-branch
#              fetch occurs at build or run.
#   * RUN    = Phase 2 (mutate): the engine runs OFFLINE (`--network=none`), with
#              NO credentials, only the target repo mounted writable and the engine
#              read-only — see recipe.md for the full `podman run` containment set
#              (drop caps, --no-new-privileges, read-only root FS, bounded tmpfs).
#
# The shipped `engine` stage is STDLIB-ONLY (no pip install). Dev/test tooling
# (vermin, the floor conformance slice) lives ONLY in the separate `floor` stage,
# so the shipped image carries no third-party runtime dependency.

# Base images are pinned BY DIGEST (Codex R2). Override with --build-arg to roll
# the pin forward deliberately; never to a mutable tag in a supported build.
ARG PYTHON_BASE=python:3.13-slim@sha256:b04b5d7233d2ad9c379e22ea8927cd1378cd15c60d4ef876c065b25ea8fb3bf3
ARG PYTHON_FLOOR=python:3.11-slim@sha256:9f9cf0cf317945d260703ea2fb0b64a10d0f43abf86eedde0d5c038d337004f7

# ---------------------------------------------------------------------------
# engine — the shipped, stdlib-only runtime image (Phase 2 mutation runs here)
# ---------------------------------------------------------------------------
FROM ${PYTHON_BASE} AS engine

# Identity emitted into the image (Phase 1 provenance — Codex R2). The recipe
# passes the host-VERIFIED commit/ref; `unknown` is a build-without-verify smell.
# PYTHON_BASE is re-declared in-stage so the org.cairn.base LABEL captures the
# digest-pinned base (a global pre-FROM ARG is out of scope inside a stage).
ARG CAIRN_COMMIT=unknown
ARG CAIRN_REF=unknown
ARG PYTHON_BASE
LABEL org.cairn.recipe="contained-kernel-v1" \
      org.cairn.commit="${CAIRN_COMMIT}" \
      org.cairn.ref="${CAIRN_REF}" \
      org.cairn.base="${PYTHON_BASE}"

# git is a required SYSTEM tool for the engine (the upgrade 3-way merge shells out
# to `git merge-file`, and `git show <ref>` reads ref-pinned templates). It is NOT
# a Python dependency — the engine stays stdlib-only re: pip. The recipe runs the
# mutation phase offline (`--network=none`), so git here never reaches the network.
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# The install/upgrade engine + the template source it reads. Deliberately NOT the
# whole repo: only scaffold.py (the launcher), _scaffold/ (the engine), and
# templates/ (the install source). No bootstrap/tests/, no .git, no docs — the
# image is the minimum that runs install + upgrade.
WORKDIR /cairn
COPY bootstrap/scaffold.py ./bootstrap/scaffold.py
COPY bootstrap/_scaffold/ ./bootstrap/_scaffold/
COPY templates/ ./templates/
# CITATION.cff is the engine's version source (lockfile.py:_cairn_version) — it
# must be present so the lockfile records a real Cairn version, not "unknown".
COPY CITATION.cff ./CITATION.cff

# The engine is invoked as an explicit argv; "upgrade" as the first arg routes to
# the upgrade CLI, anything else is install. The run step supplies --target /work
# and (for a read-only engine mount) --cairn-root /cairn.
ENTRYPOINT ["python", "/cairn/bootstrap/scaffold.py"]
CMD ["--help"]

# ---------------------------------------------------------------------------
# floor — the floor/compat conformance stage (Cairn's CI only; NOT shipped)
# ---------------------------------------------------------------------------
# Runs at the declared compatibility floor (3.11) and carries the dev-only
# tooling (vermin) the floor gate needs. floor-gate.sh drives it: vermin over the
# engine + a runtime conformance slice (CLI help, a clean install, a controlled
# upgrade). Keeping vermin here — never in `engine` — is what lets the shipped
# image stay stdlib-only.
FROM ${PYTHON_FLOOR} AS floor
ARG CAIRN_COMMIT=unknown
LABEL org.cairn.recipe="floor-compat-gate" \
      org.cairn.commit="${CAIRN_COMMIT}"
WORKDIR /cairn
# git: the upgrade conformance slice needs the system git (3-way merge). vermin:
# the dev-only floor checker, isolated to THIS stage so `engine` stays pip-clean.
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir vermin==1.6.0
COPY bootstrap/scaffold.py ./bootstrap/scaffold.py
COPY bootstrap/_scaffold/ ./bootstrap/_scaffold/
COPY templates/ ./templates/
# CITATION.cff is the engine's version source (lockfile.py:_cairn_version) — it
# must be present so the lockfile records a real Cairn version, not "unknown".
COPY CITATION.cff ./CITATION.cff
ENTRYPOINT ["python", "/cairn/bootstrap/scaffold.py"]
CMD ["--help"]
