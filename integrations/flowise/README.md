# Nummeropslag tools for Flowise

Flowise supports Nummeropslag immediately through its built-in **Custom Tool**
node. Create a Flowise variable named `NUMMEROPSLAG_API_KEY`, then add the tools
below to an Agentflow or Chatflow.

The ready-to-paste functions are in `tools/`. Each function reads the API key
from `$vars.NUMMEROPSLAG_API_KEY`; do not hard-code a key in the function.

## Input schemas

For `lookup_number`, `check_spam`, and `get_operator`:

```json
{
  "number": {
    "type": "string",
    "description": "An 8-digit Danish phone number or a number with +45",
    "required": true
  }
}
```

For `search_businesses`:

```json
{
  "query": {
    "type": "string",
    "description": "Danish business name",
    "required": true
  },
  "limit": {
    "type": "number",
    "description": "Maximum results from 1 to 50",
    "required": false
  }
}
```

`api_status` has no input fields.

API keys are available at <https://nummeropslag.dk/api-noegle>.
