from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from lfx.custom import Component
from lfx.io import DropdownInput, IntInput, MessageTextInput, Output, SecretStrInput
from lfx.schema import Data


class NummeropslagComponent(Component):
    display_name = "Nummeropslag"
    description = (
        "Look up Danish callers, official CVR companies, operators and spam signals."
    )
    documentation = "https://andrey-tut.github.io/nummeropslag-api/"
    icon = "phone-search"
    name = "Nummeropslag"

    inputs = [
        SecretStrInput(
            name="api_key",
            display_name="API Key",
            info="Get a key at https://nummeropslag.dk/api-noegle",
            required=True,
        ),
        DropdownInput(
            name="operation",
            display_name="Operation",
            options=[
                "Look Up Number",
                "Check Spam",
                "Get Operator",
                "Search Businesses",
                "Get API Status",
            ],
            value="Look Up Number",
        ),
        MessageTextInput(
            name="query",
            display_name="Phone Number or Business Name",
            info="A Danish phone number, or a company name for Search Businesses.",
            tool_mode=True,
        ),
        IntInput(
            name="limit",
            display_name="Search Result Limit",
            value=20,
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="Result", name="result", method="run_nummeropslag"),
    ]

    def _secret(self) -> str:
        value = self.api_key
        if hasattr(value, "get_secret_value"):
            return str(value.get_secret_value())
        return str(value)

    def _request(self) -> dict:
        operation = self.operation
        query = str(self.query or "").strip()
        params = None

        if operation == "Look Up Number":
            path = f"/lookup/{quote(query, safe='')}"
        elif operation == "Check Spam":
            path = f"/spam/{quote(query, safe='')}"
        elif operation == "Get Operator":
            path = f"/operator/{quote(query, safe='')}"
        elif operation == "Search Businesses":
            path = "/search"
            params = {"q": query, "limit": max(1, min(50, int(self.limit or 20)))}
        elif operation == "Get API Status":
            path = "/me"
        else:
            raise ValueError(f"Unsupported operation: {operation}")

        suffix = f"?{urlencode(params)}" if params else ""
        request = Request(
            f"https://nummeropslag.dk/api/v1/partner{path}{suffix}",
            headers={
                "Accept": "application/json",
                "X-API-Key": self._secret(),
                "X-Client": "langflow",
            },
            method="GET",
        )

        try:
            with urlopen(request, timeout=20) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")[:500]
            return {
                "error": f"http_{error.code}",
                "message": detail or error.reason,
            }
        except URLError as error:
            return {"error": "network", "message": str(error.reason)}

    def run_nummeropslag(self) -> Data:
        result = self._request()
        self.status = result
        return Data(data=result)
