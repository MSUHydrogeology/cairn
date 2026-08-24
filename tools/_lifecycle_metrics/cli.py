# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from .config import _REPO_ROOT
from .extract import PROPOSAL_COLUMNS, PLAN_COLUMNS, proposal_rows, plan_rows
from .report import format_csv, format_md
from .snapshot import emit_snapshot, format_manifest_md


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog='lifecycle_metrics',
        description=(
            'Extract lifecycle metrics from the proposal / plan corpus. '
            'Read-only over the corpus; emits a derived CSV / markdown '
            'table, snapshots, or the output manifest.'
        ),
    )
    parser.add_argument(
        'kind', nargs='?', choices=['proposals', 'plans'],
        default='proposals',
        help='Which corpus to walk. Default: proposals.',
    )
    parser.add_argument(
        '--root', type=Path, default=_REPO_ROOT,
        help=f'Repo root for the dev/ corpus. Default: {_REPO_ROOT}.',
    )
    parser.add_argument(
        '--out', type=Path, default=None,
        help='Write the report to this file instead of stdout.',
    )
    parser.add_argument(
        '--format', choices=['csv', 'md'], default='csv',
        help='Output format. Default: csv.',
    )
    parser.add_argument(
        '--snapshot', action='store_true',
        help=(
            'Persist an indexed CSV snapshot under the snapshots_dir '
            '(default dev/measurement/snapshots/<YYYY-MM-DD>-<N>.csv) '
            'carrying the unified proposal+plan schema + meta-columns. '
            'Additive: the normal stdout/--out emission still happens.'
        ),
    )
    parser.add_argument(
        '--event',
        choices=[
            'plan-archive', 'goodnight', 'doctrine-intervention',
            'manual',
        ],
        default='manual',
        help='Snapshot trigger label (used only with --snapshot). Default: manual.',
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help=(
            'With --snapshot, compute the would-be snapshot path + row '
            'count without writing.'
        ),
    )
    parser.add_argument(
        '--manifest', action='store_true',
        help=(
            'Emit the output manifest (markdown table naming every output '
            'file, its format, columns, and stability tier). Read-only.'
        ),
    )
    args = parser.parse_args(argv)

    if not args.root.is_dir():
        print(
            f'lifecycle_metrics: --root is not a directory: {args.root}',
            file=sys.stderr,
        )
        return 2

    # Manifest path: pure read-only surface, no corpus traversal.
    if args.manifest:
        text = format_manifest_md()
        if args.out is not None:
            args.out.write_text(text, encoding='utf-8')
            print(
                f'lifecycle_metrics: wrote manifest to {args.out}',
                file=sys.stderr,
            )
        else:
            sys.stdout.write(text)
        return 0

    # Snapshot path.
    if args.snapshot:
        path, row_count = emit_snapshot(
            root=args.root, event=args.event, dry_run=args.dry_run,
        )
        if args.dry_run:
            print(
                f'lifecycle_metrics: would write {row_count} rows to '
                f'{path} (event={args.event!r}; dry-run, no write)',
                file=sys.stderr,
            )
        else:
            print(
                f'lifecycle_metrics: wrote {row_count} rows to '
                f'{path} (event={args.event!r})',
                file=sys.stderr,
            )
        return 0

    # Default report path.
    if args.kind == 'proposals':
        rows = proposal_rows(args.root)
        columns = PROPOSAL_COLUMNS
    else:
        rows = plan_rows(args.root)
        columns = PLAN_COLUMNS

    text = (
        format_csv(rows, columns)
        if args.format == 'csv'
        else format_md(rows, columns)
    )

    if args.out is not None:
        args.out.write_text(text, encoding='utf-8')
        print(
            f'lifecycle_metrics: wrote {len(rows)} {args.kind} rows to '
            f'{args.out}',
            file=sys.stderr,
        )
    else:
        sys.stdout.write(text)

    return 0
