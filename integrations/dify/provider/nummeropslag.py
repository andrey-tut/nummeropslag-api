from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from api import get_json


class NummeropslagProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            get_json(str(credentials.get("api_key", "")), "/me")
        except Exception as error:
            raise ToolProviderCredentialValidationError(str(error)) from error
