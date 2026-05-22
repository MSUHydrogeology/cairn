"""A throwaway 'greet' CLI -- the toy project this example adopts Cairn on.

This file is the *result* of the worked change traced in
``README.md`` (proposal 0001 added the optional ``name`` argument and
its test).  It exists only to make the lifecycle trace concrete; it is
not part of Cairn's apparatus.
"""
import sys


def greet(name: str = "world") -> str:
    """Return a greeting for ``name`` (default ``world``)."""
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(greet(sys.argv[1] if len(sys.argv) > 1 else "world"))
