# Copyright (c) 2026 Anthony Kendall and the Cairn contributors
# SPDX-License-Identifier: MIT
"""Cairn's prose declares claim-check exemptions in config, not in its body.

An exemption is a real declaration and has to live somewhere. The question is
*where*: a comment at the top of a document is read by every human who opens
the document and acted on by none of them, and it accumulates -- Cairn carried
135 such globs across 29 files before they moved.

The pair of properties below is what keeps that from returning. The first says
the config is load-bearing (remove it and the flags come back), so a reader can
trust that the exemptions are really declared there. The second says no
document has quietly grown its own directive again.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
CONFIG = REPO / 'dev' / '.cairn' / 'claim-check-allow.json'


def _claim_check():
    spec = importlib.util.spec_from_file_location(
        'cairn_claim_check_cfg', REPO / 'scripts' / 'claim_check.py')
    mod = importlib.util.module_from_spec(spec)
    sys.modules['cairn_claim_check_cfg'] = mod
    spec.loader.exec_module(mod)
    return mod


class TestTheConfigIsWhereExemptionsLive:
    """The config grants real exemptions, and an unreadable one grants none."""

    def test_a_configured_document_is_clean_and_is_not_clean_without_it(
            self, tmp_path: Path) -> None:
        """Removing the config must make the checker stricter, not quieter.

        Asserted on a document the config actually covers, chosen at runtime,
        so the test cannot pass by naming a file whose exemptions went away.
        """
        cc = _claim_check()
        cfg = json.loads(CONFIG.read_text(encoding='utf-8'))
        covered = [d for d, spec in cfg['exemptions'].items()
                   if spec['paths'] and (REPO / d).is_file()]
        assert covered, 'the config covers no existing document'

        for rel in covered:
            with_cfg = cc.check_file(REPO / rel, REPO)
            if with_cfg.exempted:
                break
        else:
            pytest.fail('no configured document actually uses its exemptions')

        assert not with_cfg.hard_flags, (
            f'{rel} should be clean with the config present, got '
            f'{[f.message for f in with_cfg.hard_flags]}')

        moved = tmp_path / 'claim-check-allow.json'
        CONFIG.rename(moved)
        try:
            without = cc.check_file(REPO / rel, REPO)
        finally:
            moved.rename(CONFIG)
        assert without.hard_flags, (
            f'{rel} is clean even without the config -- the config is not '
            f'load-bearing, so this suite proves nothing about it')

    def test_an_unreadable_config_grants_nothing(self, tmp_path: Path) -> None:
        """Fail toward strict: a config that cannot be parsed exempts nothing.

        The opposite -- treating an unparseable exemption list as permissive --
        would let a corrupted file silence the checker.
        """
        cc = _claim_check()
        (tmp_path / 'dev' / '.cairn').mkdir(parents=True)
        (tmp_path / 'dev' / '.cairn' / 'claim-check-allow.json').write_text(
            '{ this is not json', encoding='utf-8')
        assert cc.load_allow_config(tmp_path) == {}

    def test_a_tree_with_no_config_is_not_an_error(self, tmp_path: Path) -> None:
        """An adopter who never writes one simply has no exemptions."""
        assert _claim_check().load_allow_config(tmp_path) == {}


class TestProseCarriesNoClaimCheckDirective:
    """No Cairn document has grown its own in-body exemption comment again."""

    def test_no_live_markdown_declares_an_inline_directive(self) -> None:
        """A directive on its own line is the boilerplate that moved out.

        Prose that *quotes* the syntax inside backticks is documentation and is
        deliberately not matched -- the check is for a real directive, which
        must start the line.
        """
        import re
        import subprocess

        listing = subprocess.run(
            ['git', 'ls-files', '*.md'], cwd=REPO,
            capture_output=True, text=True, check=True).stdout.split()
        directive = re.compile(r'^[ \t]*<!--[ \t]*claim-check-allow:')

        offenders: list[str] = []
        for rel in listing:
            parts = Path(rel).parent.parts
            archived = (parts and parts[0] == 'dev'
                        and ('archive' in parts
                             or parts[:2] == ('dev', 'reflections')))
            if archived:
                continue        # historical record; enforcement was its own era
            text = (REPO / rel).read_text(encoding='utf-8', errors='replace')
            for lineno, line in enumerate(text.split('\n'), start=1):
                if directive.match(line):
                    offenders.append(f'{rel}:{lineno}')

        assert not offenders, (
            'these documents carry an inline claim-check-allow directive; '
            f'move the globs into {CONFIG.relative_to(REPO)} instead: '
            f'{offenders}')
