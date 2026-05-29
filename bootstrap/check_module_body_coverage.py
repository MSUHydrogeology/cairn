#!/usr/bin/env python3
"""Body-coverage probe — the reference implementation of fidelity-check
step 6a's body-coverage dimension.

Cairn's `templates/modules/*.md` files (which scaffold into an
adopter's `dev/modules/`) are deliberately short "kernel-merge stub"
surfaces: each one's `Adds to:` declares what merges into the adopter's
kernel docs (typically `dev/agent_collaboration.md`). The full upstream
doctrine for that subject lives in a *separate* `doctrine/<stem>.md`
file in the Cairn repo, and that body is several times larger than the
stub.

`bootstrap/fidelity-check.md` step 6a's **body-coverage dimension**
asks: for a module whose stem matches an upstream `doctrine/<stem>.md`,
do the doctrine body's load-bearing topics reach the adopter's live
surfaces — not just the short `Adds to:` stub? A stub that silently
dropped a doctrine-body topic otherwise passes 6a unnoticed. This
script mechanizes that check.

It runs from an **adopter's** tree (`--target`, default the current
directory) and compares against a **Cairn checkout's** `doctrine/`
bodies (`--cairn-root`, default the Cairn repo this script ships in).
For each `dev/modules/<stem>.md` with a same-stem `doctrine/<stem>.md`,
it extracts the doctrine body's top-level (`## `) headings and flags
any whose text appears nowhere in the module file or the adopter's
kernel-fold target (`dev/agent_collaboration.md`).

Usage
-----

    # From an adopter tree, against the Cairn checkout this script is in:
    python /path/to/cairn/bootstrap/check_module_body_coverage.py

    # Explicit paths:
    python .../check_module_body_coverage.py \
        --target /path/to/adopter --cairn-root /path/to/cairn

Exit codes
----------

* 0 — clean (no missing topics across all matched modules), or all
  modules unmatched (no same-stem Cairn doctrine to compare against).
* 1 — found at least one missing upstream-doctrine topic.
* 2 — configuration error (`--cairn-root` / `--target` not found, no
  modules dir). Emits a clear warning, never a Python traceback.

Limitations
-----------

* **Same-stem name matching.** Only modules whose stem matches a Cairn
  `doctrine/<stem>.md` file get checked. Modules without a same-stem
  upstream doctrine (e.g. `claim-check`, `lifecycle-metrics`) report as
  `skipped`. A future enhancement could read a mapping from the
  module's front-matter.
* **Loose heading match.** A heading's *normalized* text (lowercased,
  punctuation collapsed) is searched as a substring in the adopter
  surfaces. False positives are possible (a passing mention counts as
  coverage); false negatives too (paraphrased coverage that doesn't
  repeat the upstream heading text). This is a heading-name proxy — it
  catches the gross "heading X is named upstream but appears nowhere in
  the adopter's tree" case; semantic coverage is out of scope.
* **Stdlib only.** No PyYAML, no third-party parsing.

Provenance: generalized from LHM's adopter-side stopgap
(`scripts/check_module_body_coverage.py`) per Cairn fold-back #39 —
the mechanization the step-6a body-coverage refinement (fold-back #31)
named as a candidate to ship in `bootstrap/`.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# ----------------------------------------------------------------------
# Configuration / defaults
# ----------------------------------------------------------------------

#: The Cairn checkout this script ships in (bootstrap/ -> repo root).
#: Its doctrine/ holds the upstream bodies to compare against.
DEFAULT_CAIRN_ROOT = Path(__file__).resolve().parent.parent

# ----------------------------------------------------------------------
# Parsing helpers (stdlib only)
# ----------------------------------------------------------------------


def extract_h2_headings(md_text: str) -> list[str]:
    """Return the list of `## ...` heading titles in *md_text*.

    Lines inside fenced code blocks (```/~~~) are skipped so a
    code-block ``##`` doesn't get picked up. HTML comments and
    blockquotes are also not heading sources.
    """
    headings: list[str] = []
    in_fence = False
    for raw in md_text.split("\n"):
        if re.match(r"^\s{0,3}(```|~~~)", raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^##\s+(.+?)\s*$", raw)
        if m:
            headings.append(m.group(1).strip())
    return headings


def normalize(text: str) -> str:
    """Normalize heading text for substring matching.

    Lowercase; collapse runs of non-alphanumerics to a single space;
    trim. Captures heading equivalence across stylistic punctuation
    variation ('Review expectations — the clean-pass trap' vs
    'Review expectations -- the clean-pass trap'); does *not* handle
    word-level paraphrase ('Reviewer' vs 'Review' — see Limitations).
    """
    out = re.sub(r"[^a-z0-9]+", " ", text.lower())
    return out.strip()


def contains_normalized(haystack: str, needle: str) -> bool:
    """True if *needle* appears as a normalized substring of *haystack*."""
    return normalize(needle) in normalize(haystack)


# ----------------------------------------------------------------------
# Probe core
# ----------------------------------------------------------------------


def find_upstream_doctrine(cairn_root: Path, module_stem: str) -> Path | None:
    """Return the same-stem doctrine file in cairn_root, or None."""
    candidate = cairn_root / "doctrine" / f"{module_stem}.md"
    return candidate if candidate.is_file() else None


def coverage_for_module(
    module_path: Path,
    doctrine_path: Path,
    live_surfaces: list[Path],
) -> list[str]:
    """Return upstream-doctrine H2 titles missing from adopter surfaces."""
    doctrine_text = doctrine_path.read_text(encoding="utf-8")
    module_text = module_path.read_text(encoding="utf-8")

    upstream_headings = extract_h2_headings(doctrine_text)
    if not upstream_headings:
        return []

    # The doctrine's own template-content / scaffold headings aren't
    # doctrine the adopter should carry. Conservative: only the literal
    # "Template content" heading.
    upstream_headings = [
        h for h in upstream_headings
        if normalize(h) not in {normalize("Template content")}
    ]

    surface_texts = [module_text]
    for path in live_surfaces:
        if path.is_file():
            surface_texts.append(path.read_text(encoding="utf-8"))

    missing: list[str] = []
    for heading in upstream_headings:
        if any(contains_normalized(text, heading) for text in surface_texts):
            continue
        missing.append(heading)

    return missing


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------


def warn(msg: str) -> None:
    print(f"check_module_body_coverage: {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"check_module_body_coverage: {msg}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Probe an adopter's installed modules against Cairn upstream "
            "doctrine bodies; flag heading-topics named upstream but absent "
            "from the adopter's live surfaces (fidelity-check step 6a "
            "body-coverage dimension)."
        ),
    )
    parser.add_argument(
        "--cairn-root",
        type=Path,
        default=DEFAULT_CAIRN_ROOT,
        help=(
            f"Path to the Cairn checkout holding doctrine/*.md "
            f"(default: the repo this script ships in, {DEFAULT_CAIRN_ROOT})."
        ),
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=Path.cwd(),
        help=(
            "Adopter repo root (default: current directory). "
            "--modules-dir and --fold-target derive from this unless given."
        ),
    )
    parser.add_argument(
        "--modules-dir",
        type=Path,
        default=None,
        help="Adopter modules dir (default: <target>/dev/modules).",
    )
    parser.add_argument(
        "--fold-target",
        type=Path,
        default=None,
        help=(
            "Adopter kernel-fold target (default: "
            "<target>/dev/agent_collaboration.md). Headings present here "
            "count as covered."
        ),
    )
    args = parser.parse_args(argv)

    modules_dir = args.modules_dir or (args.target / "dev" / "modules")
    fold_target = args.fold_target or (
        args.target / "dev" / "agent_collaboration.md"
    )

    # Graceful-failure gate: cairn-root must exist and contain doctrine/.
    if not args.cairn_root.is_dir():
        warn(
            f"--cairn-root not found at {args.cairn_root}; cannot run "
            f"body-coverage check. Pass --cairn-root <path> pointing at a "
            f"Cairn checkout."
        )
        return 2
    doctrine_dir = args.cairn_root / "doctrine"
    if not doctrine_dir.is_dir():
        warn(
            f"--cairn-root exists but has no doctrine/ subdir at "
            f"{doctrine_dir}; cannot run body-coverage check."
        )
        return 2
    if not modules_dir.is_dir():
        warn(
            f"modules dir not found at {modules_dir}; cannot run "
            f"body-coverage check (pass --modules-dir or --target)."
        )
        return 2

    info(f"cairn-root:  {args.cairn_root.resolve()}")
    info(f"modules:     {modules_dir}")
    info(f"fold-target: {fold_target}")

    module_files = sorted(modules_dir.glob("*.md"))
    module_files = [p for p in module_files if p.name != "README.md"]
    if not module_files:
        warn(f"no module files found at {modules_dir}/*.md")
        return 2

    live_surfaces = [fold_target]

    total_missing = 0
    skipped = 0
    matched = 0

    for module_path in module_files:
        stem = module_path.stem
        upstream = find_upstream_doctrine(args.cairn_root, stem)
        if upstream is None:
            print(f"  {stem}: skipped (no upstream doctrine/{stem}.md)")
            skipped += 1
            continue

        matched += 1
        missing = coverage_for_module(module_path, upstream, live_surfaces)
        if not missing:
            print(f"  {stem}: OK ({upstream.relative_to(args.cairn_root)})")
            continue

        print(f"  {stem}: {len(missing)} missing topic(s)")
        for heading in missing:
            print(f"    - {heading!r}")
        total_missing += len(missing)

    print()
    info(
        f"summary: {matched} module(s) matched, {skipped} skipped, "
        f"{total_missing} missing topic(s) across matched modules."
    )

    if total_missing > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
