from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from api import get_json


class SearchBusinessesTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        query = str(tool_parameters.get("query", "")).strip()
        limit = max(1, min(50, int(tool_parameters.get("limit", 20))))
        result = get_json(
            str(self.runtime.credentials.get("api_key", "")),
            "/search",
            {"q": query, "limit": limit},
        )
        yield self.create_json_message(result)
