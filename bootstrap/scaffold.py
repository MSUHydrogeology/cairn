#!/usr/bin/env python3
"""Compatibility notice for the relocated Cairn installer."""
import sys

if __name__ == "__main__":
    print("Cairn moved: use python install/scaffold.py", file=sys.stderr)
    raise SystemExit(2)
