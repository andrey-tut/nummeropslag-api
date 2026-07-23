from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from api import get_json


class ApiStatusTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        del tool_parameters
        yield self.create_json_message(
            get_json(str(self.runtime.credentials.get("api_key", "")), "/me")
        )
