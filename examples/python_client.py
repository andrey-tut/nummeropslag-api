"""Nummeropslag Partner API — minimal Python client (stdlib only).

All endpoints require an API key. Get one at https://nummeropslag.dk/api-noegle
    export NUMMEROPSLAG_API_KEY=pk_...
    python3 python_client.py 33633363
"""
from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request

BASE = "https://nummeropslag.dk/api/v1"
API_KEY = os.environ.get("NUMMEROPSLAG_API_KEY", "")


def _get(path: str, params: dict | None = None) -> dict:
    if not API_KEY:
        raise SystemExit("Set NUMMEROPSLAG_API_KEY=pk_... (https://nummeropslag.dk/api-noegle)")
    url = f"{BASE}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Accept": "application/json", "X-API-Key": API_KEY})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def partner_lookup(e164: str) -> dict:
    """Full lookup — operator, CVR companies, spam/trust signals (scope: lookup)."""
    return _get(f"/partner/lookup/{e164}")


def spam_verdict(e164: str) -> dict:
    """Compact spam/trust verdict (scope: spam)."""
    return _get(f"/partner/spam/{e164}")


def operator(e164: str) -> dict:
    """Operator + number type (scope: operator)."""
    return _get(f"/partner/operator/{e164}")


def search(query: str) -> dict:
    """Search companies by name in CVR (scope: lookup)."""
    return _get("/partner/search", params={"q": query})


def me() -> dict:
    """API key status: plan, scopes, quota."""
    return _get("/partner/me")


def main() -> None:
    number = sys.argv[1] if len(sys.argv) > 1 else "33633363"
    print("Full lookup:")
    print(json.dumps(partner_lookup(number), ensure_ascii=False, indent=2))
    print("\nSpam verdict:")
    print(json.dumps(spam_verdict(number), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
