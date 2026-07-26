#!/usr/bin/env python3
"""Standalone launcher — kept so `python server.py` keeps working as documented.
The actual server lives in the `nummeropslag_mcp` package (also on PyPI as
`nummeropslag-mcp`; console command: `nummeropslag-mcp`)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from nummeropslag_mcp.server import main

if __name__ == "__main__":
    main()
