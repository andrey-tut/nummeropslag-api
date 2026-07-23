#!/usr/bin/env python3
"""
Nummeropslag MCP server — Danish phone-number lookup for Claude / your projects.

Wraps the partner API (https://nummeropslag.dk/api/v1/partner) as MCP tools.
Auth: get an API key at https://nummeropslag.dk/api-noegle and set it via the
env var NUMMEROPSLAG_API_KEY (format: npk_...).

Run:
    pip install "mcp[cli]" httpx
    export NUMMEROPSLAG_API_KEY=npk_xxx
    python server.py                # stdio transport (Claude Desktop / Claude Code)

Add to Claude Desktop (claude_desktop_config.json) or Claude Code (.mcp.json):
    {
      "mcpServers": {
        "nummeropslag": {
          "command": "python",
          "args": ["/absolute/path/to/mcp/server.py"],
          "env": { "NUMMEROPSLAG_API_KEY": "npk_xxx" }
        }
      }
    }

Then ask your agent e.g. "Is +45 70 10 20 30 spam?" or "Who owns 33 63 33 63?".
"""
from __future__ import annotations

import os
from urllib.parse import quote, urlparse

import httpx
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

BASE = os.environ.get("NUMMEROPSLAG_BASE", "https://nummeropslag.dk/api/v1/partner").rstrip("/")
KEY = os.environ.get("NUMMEROPSLAG_API_KEY", "")

# Захист: ключ (header) шлемо лише на https або на localhost — щоб підмінений
# NUMMEROPSLAG_BASE не злив ключ на чужий http-хост.
_u = urlparse(BASE)
if _u.scheme != "https" and _u.hostname not in ("localhost", "127.0.0.1", "::1"):
    raise SystemExit(f"NUMMEROPSLAG_BASE must be https (got: {BASE})")


def _seg(s: object) -> str:
    """Безпечний path-сегмент: енкодимо все (щоб number='../me' не змінив маршрут)."""
    return quote(str(s), safe="")


mcp = FastMCP("nummeropslag")


READ_ONLY = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=True,
)


def _get(path: str, params: dict | None = None) -> dict:
    if not KEY:
        return {"error": "missing_key",
                "message": "Set NUMMEROPSLAG_API_KEY (get one at https://nummeropslag.dk/api-noegle)."}
    try:
        # X-Client: mcp → сервер рахує проти ОКРЕМОЇ (меншої) MCP-квоти, не проти REST-API-квоти.
        r = httpx.get(BASE + path, params=params or {},
                      headers={"X-API-Key": KEY, "X-Client": "mcp",
                               "Accept": "application/json"}, timeout=20)
    except httpx.HTTPError as e:
        return {"error": "network", "message": str(e)}
    if r.status_code == 401:
        return {"error": "unauthorized", "message": "Invalid API key."}
    if r.status_code == 429:
        return {"error": "rate_limited", "message": "Quota or rate limit exceeded."}
    if r.status_code == 422:
        return {"error": "invalid_number", "message": "Only valid Danish numbers (8 digits)."}
    if r.status_code >= 400:
        return {"error": f"http_{r.status_code}", "message": r.text[:200]}
    try:
        return r.json()
    except Exception:
        return {"error": "bad_response", "message": r.text[:200]}


@mcp.tool(title="Look up a Danish phone number", annotations=READ_ONLY)
def lookup_number(number: str) -> dict:
    """Look up a Danish phone number and return the full record: the registered company
    (from the official CVR register), the telecom operator, the number type, a community
    spam/trust rating and recent anonymous comments. `number` is an 8-digit Danish number
    (separators, spaces and a +45 prefix are accepted)."""
    return _get(f"/lookup/{_seg(number)}")


@mcp.tool(title="Check a Danish number for spam", annotations=READ_ONLY)
def check_spam(number: str) -> dict:
    """Quick spam/scam check for a Danish phone number. Returns a compact verdict:
    spam level, score, trust rating and how many users reported it. Use this to decide
    whether an incoming call is likely spam, telemarketing or a scam."""
    return _get(f"/spam/{_seg(number)}")


@mcp.tool(title="Get a Danish number's operator", annotations=READ_ONLY)
def get_operator(number: str) -> dict:
    """Return the telecom operator and number type (mobile / landline / service) for a
    Danish phone number, from the official Danish number plan. Lightweight, no company data."""
    return _get(f"/operator/{_seg(number)}")


@mcp.tool(title="Search Danish businesses", annotations=READ_ONLY)
def search_businesses(query: str, limit: int = 20) -> dict:
    """Search Danish companies by name (from the CVR register). Returns matching
    businesses. Useful to find a company's phone number or details by name."""
    return _get("/search", {"q": query, "limit": max(1, min(50, limit))})


@mcp.tool(title="Check Nummeropslag API status", annotations=READ_ONLY)
def api_status() -> dict:
    """Return the status of the configured API key: allowed scopes, daily quota and
    how many calls have been used today."""
    return _get("/me")


if __name__ == "__main__":
    mcp.run()
