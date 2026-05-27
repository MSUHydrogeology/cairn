# UPGRADE.md — folding new Cairn doctrine into a customized tree

Cairn keeps evolving. An adopting team that bootstrapped months ago is
frozen at the version they installed — unless they can pull new doctrine
forward **without losing their local customizations**. This is that path:
a **token- and slot-aware 3-way merge** that folds upstream changes into
your tree, preserves your filled `cairn:slot` bodies and tunings, and
surfaces genuine "local optimization vs. new doctrine" conflicts for
review instead of silently clobbering or skipping them.

The upgrade is **never an auto-overwrite**. It stages a review surface;
you (or your agent) review, resolve any conflicts, and apply — and the
applied upgrade is itself a tracked change in your repo that goes through
your own review lifecycle.

## The two on-disk artifacts the install leaves

Installing (or upgrading) writes two **tracked** artifacts into your
target's `dev/`:

* **`dev/cairn-lock.yml`** — a machine lockfile (the *upgrade ancestor* +
  the install-side provenance record). It pins the Cairn version + commit,
  the resolved profile, the module roster, and **per file**: source,
  destination, the `verbatim` flag, the content hash as written, and the
  substituted token values. It is **tool-owned: regenerate-only — do not
  hand-edit.** (It is JSON-encoded, which is valid YAML, so it round-trips
  without any YAML library.)
* **`dev/.cairn/base/`** — a cache of the **raw** upstream templates for
  the mergeable `.md` files, exactly as they stood when installed. This is
  the merge's *base*, so the upgrade works under any distribution mode
  (git clone, release tarball, copied tree) — it never needs Cairn's git
  history. It is tracked and hidden; the lockfile lists every cached path
  + hash so it stays auditable. Verbatim scripts are **not** cached (they
  use a hash policy, below), which keeps the cache to just the mergeable
  set.

## The workflow

```
python bootstrap/scaffold.py upgrade --target <repo> --plan     # 1. inspect
python bootstrap/scaffold.py upgrade --target <repo> --stage    # 2. stage
#    ... review dev/.cairn-upgrade/, resolve any conflict markers ...
python bootstrap/scaffold.py upgrade --target <repo> --apply    # 3. apply
```

* **`--plan`** is **strictly read-only**: it classifies every tracked file
  (clean / conflict / slot-removed / review-only / verbatim-* /
  up-to-date), lists new modules available since install (opt-in only) and
  modules removed upstream, and prints any flags. It writes **nothing**.
* **`--stage`** writes the merged/updated results into the **ephemeral**
  `dev/.cairn-upgrade/` staging directory (auto-seeded into your
  `.gitignore`) along with stage metadata. Originals are untouched.
  Open the staged files, resolve any `<<<<<<< ours … >>>>>>> theirs`
  conflict markers by hand.
* **`--apply`** swaps the resolved staged files into place and cleans the
  staging directory — but only under a **safety contract**: the stage must
  have been produced from the current lockfile (same tokens + roster), the
  originals must be unchanged since `--stage`, and **no conflict markers
  may remain** (a tree with markers is never applied — only a resolved,
  marker-free tree advances the lockfile). After applying, re-run a clean
  install (or `--stage`) to refresh the lockfile + base cache to the new
  version.

`--to <ref>` upgrades to a specific Cairn git ref **only when your Cairn
source is a git checkout** carrying that ref; a packaged release (tarball
/ zip) can upgrade only to the currently-running Cairn tree.

## How the merge protects your customizations

* **Slots are adopter-owned.** Content between `cairn:slot NAME` and
  `cairn:end NAME` is yours. Before merging, the tool copies your slot
  bodies into the base and upstream versions so all three agree inside the
  slot — the surrounding doctrine merges, your slot body is preserved
  verbatim, and you never get a spurious conflict inside a slot. A slot
  **added** upstream arrives with its placeholder for you to fill; a slot
  **removed** upstream whose body you had filled is **flagged** (not
  silently orphaned).
* **Tokens re-substitute.** The base is reconstructed by substituting your
  recorded token values into the cached raw template, so token sites don't
  conflict. A **new** upstream token with no recorded value is surfaced as
  *needs a value*.
* **Verbatim scripts use a hash check, not a text merge.** A shipped
  reference script (`claim_check.py`, `intent.py`, `lifecycle_metrics.py`,
  `link_check.py`, `sync_doc_snippets.py`) is meant to be byte-for-byte.
  If yours is unmodified it updates to the new upstream; if you forked it,
  the upgrade **flags it and does not clobber** — a forked tool may break
  against new doctrine, so that is a real decision for you to make.

## Migrating a tree installed before upgrade support

If you bootstrapped before this capability existed, your tree has no
lockfile. Create one:

```
python bootstrap/scaffold.py upgrade --target <repo> --init-lock
```

This synthesizes `dev/cairn-lock.yml` from your on-disk content and your
fidelity manifest's `cairn_commit`. **Important limitation:** the fidelity
manifest records token *names*, not the *values* substituted at install,
so for token-substituted files the install-time base **cannot** be
reconstructed. Those files are marked *unrecoverable-base* and upgrade as
a **review-only diff** (you compare and merge by hand) — never a pretended
3-way merge. Verbatim scripts are hash-tracked normally. For clean 3-way
merges on those files, re-install from an upgrade-capable Cairn so a full
lockfile + base cache is written.

## The lockfile and the fidelity manifest

The lockfile is the **machine authority** for what is installed (files,
modules, tokens, hashes). The human **fidelity manifest**
(`dev/strategy/…`, see `fidelity-check.md`) is the audit *narrative*; it
**cites** the lockfile's version/commit rather than re-listing the
inventory. `upgrade` warns if the manifest's citation is stale. Keep the
two one-way: regenerate the lockfile with the tool; update the manifest's
citation by hand.

## A note on secrets

Cairn templates must **not** introduce secret-bearing substitution tokens
— the lockfile records token values into a tracked file, so a secret would
leak. The lockfile writer refuses obvious secret-like token names
(`password`, `secret`, `token`, `key`, …) unless explicitly allow-listed.
See `SAFETY.md`.
