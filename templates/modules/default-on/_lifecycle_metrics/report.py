from __future__ import annotations

import csv
import io
from typing import Dict, Sequence


def _csv_safe(value: object) -> str:
    """Neutralize spreadsheet formula-injection.

    A cell whose text begins with a formula trigger (``= + - @`` or a
    leading tab / carriage-return) is prefixed with a single quote so a
    spreadsheet treats it as literal text, not a formula. The metrics
    corpus is the team's own committed proposals, but in an adopter repo a
    proposal *title* (which flows into a cell) can carry untrusted
    contributor text, so the emitter neutralizes defensively
    (security-hardening, informational)."""
    s = '' if value is None else str(value)
    if s[:1] in ('=', '+', '-', '@', '\t', '\r'):
        return "'" + s
    return s


def format_csv(
    rows: Sequence[Dict[str, object]], columns: Sequence[str],
) -> str:
    """Render rows as CSV text (the default, machine-readable form).

    Data cells are passed through :func:`_csv_safe` to neutralize
    formula-injection; column headers are Cairn-defined and emitted as-is."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(columns)
    for row in rows:
        writer.writerow([_csv_safe(row.get(c, '')) for c in columns])
    return buf.getvalue()


def format_md(
    rows: Sequence[Dict[str, object]], columns: Sequence[str],
) -> str:
    """Render rows as a GitHub-flavored markdown table.  Pipe characters
    in cells are escaped so the table stays well-formed."""
    def _cell(value: object) -> str:
        return str(value).replace('|', r'\|')

    lines = [
        '| ' + ' | '.join(columns) + ' |',
        '| ' + ' | '.join('---' for _ in columns) + ' |',
    ]
    for row in rows:
        lines.append(
            '| ' + ' | '.join(_cell(row.get(c, '')) for c in columns) + ' |')
    return '\n'.join(lines) + '\n'
