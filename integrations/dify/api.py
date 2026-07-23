from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://nummeropslag.dk/api/v1/partner"


def get_json(api_key: str, path: str, params: dict | None = None) -> dict:
    if not api_key:
        raise ValueError("A Nummeropslag API key is required.")

    query = f"?{urlencode(params)}" if params else ""
    request = Request(
        f"{BASE_URL}{path}{query}",
        headers={
            "Accept": "application/json",
            "X-API-Key": api_key,
            "X-Client": "dify",
        },
        method="GET",
    )

    try:
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")[:500]
        if error.code == 401:
            raise ValueError("Invalid Nummeropslag API key.") from error
        if error.code == 422:
            raise ValueError("Enter a valid 8-digit Danish phone number.") from error
        if error.code == 429:
            raise RuntimeError("Nummeropslag quota or rate limit exceeded.") from error
        raise RuntimeError(f"Nummeropslag API returned HTTP {error.code}: {detail}") from error
    except URLError as error:
        raise RuntimeError(f"Could not reach Nummeropslag: {error.reason}") from error


def phone_path(prefix: str, number: object) -> str:
    return f"/{prefix}/{quote(str(number), safe='')}"
