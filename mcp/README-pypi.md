# nummeropslag-mcp

mcp-name: io.github.andrey-tut/nummeropslag

MCP (Model Context Protocol) server that gives AI agents — Claude Desktop, Claude Code,
or any MCP client — access to **Danish phone-number data** from
[nummeropslag.dk](https://nummeropslag.dk): company lookup from the official **CVR**
business register, telecom **operator** + number type from the Danish number register,
and a community **spam/scam verdict**.

## Install & run

```bash
pip install nummeropslag-mcp        # or: uvx nummeropslag-mcp
export NUMMEROPSLAG_API_KEY=npk_xxx # get a key: https://nummeropslag.dk/api-noegle
nummeropslag-mcp                    # stdio transport
```

Claude Desktop / Claude Code config:

```json
{
  "mcpServers": {
    "nummeropslag": {
      "command": "nummeropslag-mcp",
      "env": { "NUMMEROPSLAG_API_KEY": "npk_xxx" }
    }
  }
}
```

## Tools

| Tool | Description |
|---|---|
| `lookup_number(number)` | Full record: company (CVR), operator, spam/trust, comments |
| `check_spam(number)` | Compact spam/scam verdict (caller-ID style) |
| `get_operator(number)` | Operator + number type only |
| `search_businesses(query, limit)` | Find Danish companies by name (CVR) |
| `api_status()` | Your key's scopes + quota usage |

Docs & examples: <https://github.com/andrey-tut/nummeropslag-api> ·
API reference: <https://andrey-tut.github.io/nummeropslag-api/>
