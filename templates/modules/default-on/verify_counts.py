#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Check registered numeric claims in the installed project."""
from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

_MEASUREMENTS_SRC = Path(__file__).resolve().parent / 'measurements.py'

# The annotation: ``<!-- verify: <key> -->``.  The key is registry-only --
# word characters and hyphens, no path / command syntax.
_VERIFY_RE = re.compile(r'<!--\s*verify:\s*(?P<key>[\w-]+)\s*-->')

# A number token (optional thousands grouping): ``786``, ``1,294``.
_NUMBER_RE = re.compile(r'(?P<num>\d{1,3}(?:,\d{3})+|\d+)')


def _load_measurements(name: str = 'cairn_measurements') -> ModuleType:
    """Import the sibling ``measurements.py`` by file path (the house
    spec_from_file_location pattern; register before exec so its
    ``@dataclass`` defs resolve)."""
    spec = importlib.util.spec_from_file_location(name, _MEASUREMENTS_SRC)
    if spec is None or spec.loader is None:
        raise ImportError(f'cannot load measurements from {_MEASUREMENTS_SRC}')
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@dataclass
class Result:
    """One verification outcome."""

    path: Path
    line: int
    key: str
    annotated: int | None
    status: str   # 'pass' | 'drift' | 'refused' | 'error' | 'skipped'
    message: str


def parse_annotations(text: str) -> list[tuple[int, int | None, str]]:
    """Return ``(lineno, annotated_number_or_None, key)`` for every
    ``<!-- verify: <key> -->`` annotation.

    The annotated number is the one **immediately preceding** the
    annotation on the *same* line.  A line whose annotation has no
    preceding number yields ``None`` (a malformed annotation the caller
    reports as an error -- the annotation exists to verify a number).
    """
    out: list[tuple[int, int | None, str]] = []
    attempted = re.compile(r"<!--\s*verify:")
    pos = 0
    while match := attempted.search(text, pos):
        line_start = text.rfind('\n', 0, match.start()) + 1
        line_end = text.find('\n', match.start())
        if line_end < 0:
            line_end = len(text)
        lineno = text.count('\n', 0, match.start()) + 1
        line = text[line_start:line_end]
        offset = match.start() - line_start
        valid = _VERIFY_RE.match(line, offset)
        if valid is None:
            out.append((lineno, None, "malformed marker"))
            pos = match.end()
            continue
        numbers = list(_NUMBER_RE.finditer(line[:offset]))
        number = int(numbers[-1].group('num').replace(',', '')) if numbers else None
        out.append((lineno, number, valid.group('key')))
        pos = line_start + valid.end()

    return out


def verify_text(
    text: str, path: Path, registry: dict, measurements: ModuleType,
) -> list[Result]:
    """Verify every annotation in *text* against *registry*."""
    results: list[Result] = []
    for lineno, annotated, key in parse_annotations(text):
        if annotated is None:
            results.append(Result(
                path, lineno, key, None, 'error',
                f'`<!-- verify: {key} -->` has no number immediately '
                f'preceding it on the line',
            ))
            continue
        entry = registry.get(key)
        if entry is None:
            results.append(Result(
                path, lineno, key, annotated, 'refused',
                f'unregistered verify key `{key}` -- not in the '
                f'measurement registry (no silent pass)',
            ))
            continue
        if isinstance(entry, measurements.Snapshot):
            # Never re-measure: confirm value equality + the ISO as_of is
            # present on the line so the human prose is dated and agrees.
            line_text = text.split('\n')[lineno - 1]
            if annotated != entry.value:
                results.append(Result(
                    path, lineno, key, annotated, 'drift',
                    f'snapshot `{key}`: annotated {annotated} != frozen '
                    f'value {entry.value} (snapshots are never re-measured; '
                    f'fix the prose, not the registry)',
                ))
            elif entry.as_of not in line_text:
                results.append(Result(
                    path, lineno, key, annotated, 'drift',
                    f'snapshot `{key}`: the ISO as_of date `{entry.as_of}` '
                    f'is missing from the verified line',
                ))
            else:
                results.append(Result(
                    path, lineno, key, annotated, 'pass',
                    f'snapshot `{key}` = {annotated}, dated {entry.as_of}',
                ))
            continue
        # Invariant -- visible skip on an absent root, else re-measure.
        if not entry.root.exists():
            results.append(Result(
                path, lineno, key, annotated, 'skipped',
                f'SKIPPED (root absent: {entry.root}) -- invariant `{key}` '
                f'not verified',
            ))
            continue
        try:
            measured = measurements.measure(entry)
        except Exception as exc:  # containment refusal, missing target, etc.
            results.append(Result(
                path, lineno, key, annotated, 'error',
                f'invariant `{key}` could not be measured: {exc}',
            ))
            continue
        if measured == annotated:
            results.append(Result(
                path, lineno, key, annotated, 'pass',
                f'invariant `{key}` = {measured} (matches)',
            ))
        else:
            results.append(Result(
                path, lineno, key, annotated, 'drift',
                f'invariant `{key}`: doc says {annotated}, measured '
                f'{measured} today -- DRIFT',
            ))
    return results


def _exit_code(results: list[Result]) -> int:
    statuses = {r.status for r in results}
    if statuses & {'drift', 'refused', 'error'}:
        return 1
    if 'skipped' in statuses:
        return 3
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog='verify_counts',
        description=(
            'Re-measure registered live-invariant counts annotated with '
            '`<!-- verify: <key> -->` in project documents.'
        ),
    )
    parser.add_argument(
        'files', type=Path, nargs='+', help='Markdown file(s) to verify.')
    args = parser.parse_args(argv)

    try:
        measurements = _load_measurements()
        registry = measurements.load_registry()
    except Exception as exc:
        print(f"verify_counts: registry or support unavailable: {exc}", file=sys.stderr)
        return 1

    all_results: list[Result] = []
    for file in args.files:
        if not file.is_file():
            print(f'verify_counts: not a file: {file}', file=sys.stderr)
            return 2
        all_results.extend(
            verify_text(
                file.read_text(encoding='utf-8', errors='replace'),
                file, registry, measurements,
            )
        )

    failures = [r for r in all_results if r.status in {'drift', 'refused', 'error'}]
    skipped = [r for r in all_results if r.status == 'skipped']
    passed = [r for r in all_results if r.status == 'pass']

    for result in failures:
        print(
            f'verify_counts: {result.path}:{result.line}: '
            f'[{result.status}] {result.message}',
            file=sys.stderr,
        )
    for result in skipped:
        print(f'verify_counts: {result.path}:{result.line}: {result.message}')
    for result in passed:
        print(f'verify_counts: {result.path}:{result.line}: {result.message}')

    print(
        f'verify_counts: {len(passed)} ok, {len(failures)} failed, '
        f'{len(skipped)} skipped.'
    )
    return _exit_code(all_results)


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
