from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from api import get_json, phone_path


class GetOperatorTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        result = get_json(
            str(self.runtime.credentials.get("api_key", "")),
            phone_path("operator", tool_parameters.get("number", "")),
        )
        yield self.create_json_message(result)
