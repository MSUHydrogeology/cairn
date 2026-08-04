<!-- cairn-internal-ref-allow: doctrine/runtime-contract.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# The contained-kernel recipe — run Cairn with no host-installed Python

Cairn's engine (install / upgrade / 3-way merge / lockfile) is **stdlib-only
Python**. This recipe lets a team whose application stack is **not** Python run
that engine **only at the install/upgrade boundary**, inside a throwaway,
contained container — so **no Python is installed on the host and no Python
enters the application's build/test CI**.

> **Maturity note (read first).** v1 is **containerized Python — a convenience,
> not extrication.** A Python interpreter in an OCI image is still part of your
> trusted computing base, and Docker/Podman is a new runtime dependency. The
> honest promise is *"no host-installed Python, and no Python in your
> application's build/test CI,"* **not** *"no Python anywhere."* Full
> stack-neutrality — a native, non-Python re-implementation — is **future work**,
> reachable through the **extrication seam** documented at the end of this file
> (the Move 5 follow-up). Do not mistake the contained kernel for a port.

This recipe targets the **settled install/upgrade CLI** (`scaffold.py`), not the
engine's internal module layout, so it survives engine refactors unchanged.

---

## What you need

* An **OCI runtime**: **rootless Podman** *or* Docker. (v1 is tested on rootless
  Podman 5.x and builds OCI-standard images.)
* A checkout of a **pinned** Cairn ref — a release tag or a specific commit. A
  **mutable branch is refused** (see Phase 1); a branch tip can move under the pin.
* **No host Python.** The engine runs *inside* the container; your host needs
  only the OCI runtime.

---

## The two phases (the narrowed trust boundary)

The recipe keeps **acquisition** and **mutation** in two separate privilege
domains. This is what makes the container a *narrowed* trust boundary rather than
a convenient Python carrier.

### Phase 1 — acquire + verify (networked, read-only)

1. Acquire a **pinned** Cairn checkout, and **verify** it. Establish the
   checkout's authenticity *first*, with the out-of-band bootstrap in
   `bootstrap/PROVENANCE.md` — system `git`, a workspace you created, and a key
   fingerprint you compared on two independent channels. `verify-ref.sh` lives
   *inside* the checkout, so running it is already executing candidate bytes; it
   is a convenience downstream of that bootstrap, never a replacement for it.

   ```sh
   bootstrap/container/verify-ref.sh --signers ~/.config/cairn/release-signers \
       /path/to/cairn <tag>
   ```

   Provenance mode is the default: it requires a **signed, name-bound annotated
   tag** and a trusted roster from outside the candidate, and exits `0`
   (`PROVENANCED`). It **refuses a mutable branch ref**, an abbreviated SHA, and
   a **dirty or untracked build surface** — the last is a refusal, not an
   advisory, because a built image would not byte-match the pin.

   A development checkout has no signed release tag. Pass `--unprovenanced` for
   that case: it accepts an immutable commit pin, exits `3`, and states in its
   own output that **no signature was checked**.

2. Build the engine image. The **base image is pinned by digest** in the
   `Dockerfile`; the build **emits the Cairn identity** as OCI labels
   (`org.cairn.commit`, `org.cairn.ref`):

   ```sh
   podman build -f bootstrap/container/Dockerfile --target engine \
     --build-arg CAIRN_COMMIT="$(git -C /path/to/cairn rev-parse HEAD)" \
     --build-arg CAIRN_REF="$(git -C /path/to/cairn describe --tags --always)" \
     -t cairn-kernel:pinned /path/to/cairn
   ```

   Inspect the emitted identity with
   `podman image inspect cairn-kernel:pinned --format '{{ .Labels }}'`.

Phase 1 is the **only** networked step (pulling the base image, building). No
mutable-branch fetch happens at build or run.

### Phase 2 — mutate (offline, write-capable, contained)

Run the engine **offline** with the full containment set. **Only the target repo
is writable**; the engine source is read-only in the image; **no credentials are
mounted** (the engine does not fetch — `upgrade` reads templates from the local
image tree).

```sh
# INSTALL into a fresh target repo
podman run --rm \
  --network=none --read-only --tmpfs /tmp:rw,size=64m \
  --cap-drop=ALL --security-opt no-new-privileges \
  -e PYTHONDONTWRITEBYTECODE=1 -e HOME=/tmp \
  -v "$PWD":/work:rw,Z \
  cairn-kernel:pinned \
  --config /work/.cairn-profile.yml --target /work --cairn-root /cairn \
  --non-interactive

# UPGRADE an already-installed target (plan -> stage -> apply), same containment
podman run --rm --network=none --read-only --tmpfs /tmp:rw,size=64m \
  --cap-drop=ALL --security-opt no-new-privileges \
  -e PYTHONDONTWRITEBYTECODE=1 -e HOME=/tmp -v "$PWD":/work:rw,Z \
  cairn-kernel:pinned upgrade --target /work --cairn-root /cairn --apply
```

The containment flags, and why each matters:

| Flag | Guarantee |
|---|---|
| `--network=none` | the mutation phase has **no network**; no credential or source can egress |
| `--read-only` + `--tmpfs /tmp` | the container root FS is **read-only**; only a bounded tmpfs is writable scratch |
| `--cap-drop=ALL` | **no Linux capabilities** |
| `--security-opt no-new-privileges` | no privilege escalation |
| `-v <target>:/work:rw` | **only** the target repo is writable; nothing else of the host is mounted |
| (engine in-image, RO) | the verified engine source cannot be mutated at run time |
| `-e PYTHONDONTWRITEBYTECODE=1` | the read-only engine tree is never written (no `.pyc`) |

Do **not** mount a Docker socket, `$HOME`, an SSH agent, a credential helper, or
any path other than the target repo. `git` is present in the image as a **system
tool** the engine needs (the 3-way merge shells out to `git merge-file`); it is
**not** a Python dependency and, under `--network=none`, never reaches the network.

---

## Permissions-sanity (the FIRST thing to check)

A volume-mounted `dev/` tree must end up **owned by your host user** — no manual
`chown` fixup.

* **Rootless Podman (v1 tested):** container→host ownership maps **automatically**;
  do **not** pass `--user`. Files land owned by the invoking user.
* **Docker on Linux:** the container runs as root by default; pass
  `--user "$(id -u):$(id -g)"` so the written `dev/` tree is host-owned.

If, after a run, files under `dev/` are root-owned, **stop** — the
ownership/runtime mapping is wrong for your platform; fix it before relying on the
recipe (do not paper over it with `sudo chown`).

---

## Platform matrix (v1)

| Platform | Status |
|---|---|
| **Rootless Linux + Podman/Docker** | **Supported, tested** (the F4 acceptance gate is run here by hand) |
| macOS (Podman/Docker Desktop) | **Best-effort** — the engine runs in the runtime's Linux VM; ownership maps via rootless Podman. Exercised in development; not a gated platform. |
| Windows (Docker Desktop / WSL2) | **Best-effort** — not yet exercised end-to-end |

The **floor gate** (`bootstrap/container/floor-gate.sh`) and the **acceptance
test** (`bootstrap/container/acceptance.sh`) are run by the maintainer from a
Cairn checkout, not in an adopter's CI — and not by anything automatic here: no
test and no script in `scripts/` runs either gate. (The suite does *read*
`acceptance.sh`: `bootstrap/tests/test_verify_ref.py` extracts its marked
negative pins and replays them, so a pin weakened there is weakened in the suite
too. That pins the assertions; it does not run the container gate.) The
acceptance test records **SKIPPED** (never PASS) on a host with no OCI runtime —
a missing gate is *degraded assurance*, not a silent green.

---

## What the engine writes (so you can verify a run)

After install, the target carries: `dev/.cairn/cairn-lock.yml` (the version +
provenance lockfile), `dev/.cairn/base/` (the upstream template cache for 3-way
merge), and the `dev/` tree. An upgrade advances the lockfile + base cache and
3-way-merges template changes into your (possibly locally-edited) files.

---

## The extrication seam (the path to a native port — Move 5, future work)

The contained kernel is **convenience now**; the door to true stack-neutrality (a
non-Python re-implementation an adopter owns) stays open through a **stable,
enumerated seam** — and v1 adds **no container-only behaviour** that a future
port would have to special-case:

* **The boundary is a CLI, not an API.** Everything runs through
  `scaffold.py install` and `scaffold.py upgrade` — a process with arguments, a
  target directory, and an exit code. A port re-implements *that surface*, not the
  engine's internal modules.
* **The behavioural contracts a port must honour** (exit semantics, path
  containment, the lockfile schema + versioning, strict slot parsing, 3-way merge
  behaviour, and the security refusals) are the engine's **observable** contract.
  Enumerating them as language-neutral conformance fixtures + golden vectors is the
  **Move 5 follow-up** (deferred, its own proposal) — until that ships, the
  "build a port" claim stays modest: the seam is named, the executable conformance
  evidence is future work.
* **No-lock-in invariant:** the recipe never makes the engine do anything in the
  container it would not do natively. Running Cairn in the contained kernel and
  running it from a host Python install produce the **same** install/upgrade
  result, so adopting the container does not entrench Python.

See `doctrine/runtime-contract.md` for the floor/runtime contract this recipe
serves, and the Move 5 follow-up proposal for the conformance-fixture work.
