# Copyright (c) 2026 Anthony Kendall and the Cairn contributors
# SPDX-License-Identifier: MIT
"""The mechanics behind a runner that is currently BLOCKED, and why they still matter.

An External Security Review (Codex, 2026-08-27) returned BLOCK with seven
blocking findings, so `main()` refuses on entry. These tests pass the
acknowledgement flag explicitly to reach the machinery underneath, because the
machinery is what a redesign has to preserve or deliberately replace -- and a
suite that went silent the moment the tool was blocked would tell a future
reader nothing about which properties were ever real.

What they pin is narrower than this file once claimed. The review established
that the digest binds only the plan's *projection*, not the complete preimage
or output: two materially different trees can produce identical digests. The
moving-plan test below is honest within that model and no wider.

These pin the properties that make the typed digest an authorization rather
than a keystroke: it must match the plan that was displayed, it must still
describe the tree at the moment of writing, and a pipe must not be able to
supply it. Each refusal must also leave the artifact untouched -- a correction
that half-applies is worse than one that refuses, because the operator believes
they authorized a state that does not exist.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
TOOL = REPO / 'scripts' / 'correct_pinned_digests.py'


def _load():
    spec = importlib.util.spec_from_file_location('cairn_correct_pinned_digests', TOOL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules['cairn_correct_pinned_digests'] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def tool():
    return _load()


class TestAPipeCannotAuthorize:
    """Authorization is a human act; a redirect is not a human."""

    def test_no_tty_and_no_flag_refuses(self, tool, monkeypatch, capsys):
        """The failure mode this closes is a well-meaning wrapper script that
        pipes `yes` into the tool and turns the gate into a formality.
        """
        monkeypatch.setattr(tool, 'plan_lockfile',
                            lambda: {'remove': [{'dst': 'x'}], 'add': [], 'before': 5})
        monkeypatch.setattr(tool, 'apply_lockfile',
                            lambda plan: pytest.fail('must not apply'))
        monkeypatch.setattr(tool, 'CORRECTIONS', {
            'lockfile': (tool.plan_lockfile, tool.render_lockfile,
                         tool.apply_lockfile, 'the install lockfile')})
        monkeypatch.setattr(sys.stdin, 'isatty', lambda: False, raising=False)

        assert tool.main(['lockfile', '--i-have-read-the-block-review']) == 2
        assert 'must not be able to authorize' in capsys.readouterr().err


class TestTheTypedDigestMustMatchThePlan:
    def test_a_wrong_digest_aborts_and_writes_nothing(self, tool, monkeypatch, capsys):
        monkeypatch.setattr(tool, 'plan_lockfile',
                            lambda: {'remove': [{'dst': 'x'}], 'add': [], 'before': 5})
        monkeypatch.setattr(tool, 'apply_lockfile',
                            lambda plan: pytest.fail('must not apply'))
        monkeypatch.setattr(tool, 'CORRECTIONS', {
            'lockfile': (tool.plan_lockfile, tool.render_lockfile,
                         tool.apply_lockfile, 'the install lockfile')})

        assert tool.main(['lockfile', '--i-have-read-the-block-review',
                          '--authorize', 'deadbeef']) == 1
        assert 'not the plan digest' in capsys.readouterr().err


class TestTheTreeMustNotMoveWhileYouRead:
    """The whole reason the checksum is not theatre.

    The operator authorizes a state they read. If the tree changes between the
    display and the write -- a concurrent session committing, an editor saving
    -- the authorization no longer describes what would be written.
    """

    def test_a_plan_that_changes_after_display_refuses(self, tool, monkeypatch, capsys):
        plans = [{'remove': [{'dst': 'first'}], 'add': [], 'before': 5},
                 {'remove': [{'dst': 'second'}], 'add': [], 'before': 5}]
        calls = {'n': 0}

        def moving_plan():
            plan = plans[min(calls['n'], len(plans) - 1)]
            calls['n'] += 1
            return plan

        monkeypatch.setattr(tool, 'plan_lockfile', moving_plan)
        monkeypatch.setattr(tool, 'apply_lockfile',
                            lambda plan: pytest.fail('must not apply'))
        monkeypatch.setattr(tool, 'CORRECTIONS', {
            'lockfile': (tool.plan_lockfile, tool.render_lockfile,
                         tool.apply_lockfile, 'the install lockfile')})

        first_digest = tool.plan_digest(plans[0])[:8]
        calls['n'] = 0
        assert tool.main(['lockfile', '--i-have-read-the-block-review',
                          '--authorize', first_digest]) == 2
        err = capsys.readouterr().err
        assert 'the tree changed while you were reading' in err
        assert 'Nothing was written' in err

    def test_a_stable_plan_applies(self, tool, monkeypatch, capsys):
        """The control: without this, the test above passes if the tool refuses
        unconditionally, which would prove nothing about the guard.
        """
        plan = {'remove': [{'dst': 'x'}], 'add': [], 'before': 5}
        applied = {}
        monkeypatch.setattr(tool, 'plan_lockfile', lambda: dict(plan))
        monkeypatch.setattr(tool, 'apply_lockfile',
                            lambda p: applied.setdefault('yes', True) and 'ok' or 'ok')
        monkeypatch.setattr(tool, 'CORRECTIONS', {
            'lockfile': (tool.plan_lockfile, tool.render_lockfile,
                         tool.apply_lockfile, 'the install lockfile')})

        rc = tool.main(['lockfile', '--i-have-read-the-block-review',
                        '--authorize', tool.plan_digest(plan)[:8]])
        assert rc == 0, capsys.readouterr().err
        assert applied.get('yes'), 'the stable path must actually apply'


class TestRefusalsAreLoudAndTotal:
    def test_a_refusal_in_planning_exits_two_and_says_why(self, tool, monkeypatch, capsys):
        def refuse():
            raise tool.Refusal('a named precondition failed')
        monkeypatch.setattr(tool, 'plan_lockfile', refuse)
        monkeypatch.setattr(tool, 'CORRECTIONS', {
            'lockfile': (tool.plan_lockfile, tool.render_lockfile,
                         tool.apply_lockfile, 'the install lockfile')})
        assert tool.main(['lockfile', '--i-have-read-the-block-review']) == 2
        assert 'a named precondition failed' in capsys.readouterr().err


class TestItRunsAgainstTheRealTree:
    """A tool that only works under monkeypatch is not a tool."""

    @pytest.mark.parametrize('correction', ['ast-baseline', 'lockfile'])
    def test_the_runner_refuses_until_the_block_review_is_answered(self, correction):
        """BLOCKED by External Security Review, 2026-08-27. Seven blocking
        findings, two CRITICAL. The refusal lives in code because a warning
        nobody executes is how a blocked tool gets used anyway.
        """
        r = subprocess.run(
            [sys.executable, str(TOOL), correction],
            cwd=REPO, capture_output=True, text=True, stdin=subprocess.DEVNULL)
        assert r.returncode == 2, (r.returncode, r.stdout, r.stderr)
        assert 'BLOCKED by an External Security Review' in r.stderr

    @pytest.mark.parametrize('correction', ['ast-baseline', 'lockfile'])
    def test_planning_the_real_repo_does_not_crash(self, correction):
        """Exit 0 (nothing to correct) or a plan; never a traceback.

        This is the check that catches an API drift in `_ast_attest` or the
        lockfile shape, which is exactly what made the previous throwaway
        versions of this script wrong on first run each time.
        """
        r = subprocess.run(
            [sys.executable, str(TOOL), correction,
             '--i-have-read-the-block-review'],
            cwd=REPO, capture_output=True, text=True, stdin=subprocess.DEVNULL)
        assert 'Traceback' not in r.stderr, r.stderr
        assert r.returncode in (0, 2), (r.returncode, r.stdout, r.stderr)
