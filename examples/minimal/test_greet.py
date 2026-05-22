"""The test absorbed by proposal 0001 -- 'a change absorbs its tests.'

Run with: ``python -m pytest test_greet.py`` (Cairn does not run this;
your test framework does -- see ../../docs/workflow-role.md).
"""
from greet import greet


def test_default_greeting():
    assert greet() == "Hello, world!"


def test_named_greeting():
    assert greet("Cairn") == "Hello, Cairn!"
