# Nummeropslag API

![API](https://img.shields.io/badge/API-REST-009688)
![OpenAPI](https://img.shields.io/badge/OpenAPI-3.1-6BA539?logo=openapiinitiative&logoColor=white)
![Auth](https://img.shields.io/badge/auth-API%20key-blue)
![Region](https://img.shields.io/badge/region-Denmark%20%F0%9F%87%A9%F0%9F%87%B0-C8102E)
![Examples](https://img.shields.io/badge/examples-curl%20%C2%B7%20python%20%C2%B7%20node%20%C2%B7%20php-lightgrey)
![MCP](https://img.shields.io/badge/MCP-server-7C4DFF?logo=anthropic&logoColor=white)
![License](https://img.shields.io/badge/examples%20license-MIT-green)

Public **Partner API** + **MCP server** for Danish phone-number lookup, caller-ID and spam/trust signals.

Identify who is calling from a Danish number: company from the official **CVR** register,
**telecom operator**, number type, and a **spam/trust verdict** based on anonymous user
reports. Powered by official open data — not scraping. Use it from any HTTP client, or plug the
**[MCP server](#mcp-server-ai-agents-)** straight into Claude and other AI agents.

> 🌐 Service: **[nummeropslag.dk](https://nummeropslag.dk)** · 🔑 Get a key: **[/api-noegle](https://nummeropslag.dk/api-noegle)** · 📘 Interactive docs: **[/docs](https://nummeropslag.dk/docs)** · 🤖 [MCP](#mcp-server-ai-agents-)
>
> This repository contains **only public API docs, the OpenAPI spec, client examples and the MCP server**. The backend source is private.

---

## Authentication

All endpoints require an API key, sent in the `X-API-Key` header:

```http
X-API-Key: npk_your_key_here
```

Each key has a **plan**, a set of **scopes** (`lookup`, `spam`, `operator`) and a **request quota**.
Check your key status any time via `GET /api/v1/partner/me`.

Base URL: `https://nummeropslag.dk/api/v1`

---

## Endpoints

| Method | Endpoint | Scope | Description |
|---|---|---|---|
| GET | `/partner/lookup/{e164}` | `lookup` | Full lookup — operator, CVR companies, spam/trust signals |
| GET | `/partner/spam/{e164}` | `spam` | Compact spam/trust verdict only |
| GET | `/partner/operator/{e164}` | `operator` | Telecom operator + number type |
| GET | `/partner/search?q=` | `lookup` | Search companies by name (CVR) |
| GET | `/partner/me` | — | Your key status: plan, scopes, quota/usage |

`{e164}` accepts an 8-digit Danish number or full E.164 — e.g. `33633363` or `+4533633363`.

Full machine-readable contract: [`openapi/openapi.yaml`](openapi/openapi.yaml) · [`openapi/openapi.json`](openapi/openapi.json).

---

## Quick start

```bash
export NUMMEROPSLAG_API_KEY=npk_your_key_here

curl -H "X-API-Key: $NUMMEROPSLAG_API_KEY" \
  https://nummeropslag.dk/api/v1/partner/spam/33633363
```

## Client examples

Ready-to-run, dependency-free clients in [`examples/`](examples/):

| Language | File | Run |
|---|---|---|
| Bash / curl | [`examples/curl.sh`](examples/curl.sh) | `./curl.sh 33633363` |
| Python (stdlib) | [`examples/python_client.py`](examples/python_client.py) | `python3 python_client.py 33633363` |
| Node.js 18+ | [`examples/node_client.js`](examples/node_client.js) | `node node_client.js 33633363` |
| PHP | [`examples/php_client.php`](examples/php_client.php) | `php php_client.php 33633363` |

All read the key from the `NUMMEROPSLAG_API_KEY` environment variable.

---

## MCP server (AI agents) 🤖

Give your AI agent (Claude Desktop, Claude Code, or any **Model Context Protocol** client)
direct access to Danish phone-number data. The server in [`mcp/`](mcp/) wraps the Partner API
as MCP tools — same official data, same privacy rules (no names of private individuals).

MCP calls are metered against a **separate MCP quota** (not your REST quota); the server sends
`X-Client: mcp` automatically.

**Tools**

| Tool | Description |
|---|---|
| `lookup_number(number)` | Full record: company (CVR), operator, spam/trust, comments |
| `check_spam(number)` | Compact spam/scam verdict (caller-ID style) |
| `get_operator(number)` | Operator + number type only (cheapest) |
| `search_businesses(query, limit)` | Find Danish companies by name (CVR) |
| `api_status()` | Your key's scopes + quota usage |

**Setup**

```bash
pip install "mcp[cli]" httpx
export NUMMEROPSLAG_API_KEY=npk_your_key_here   # https://nummeropslag.dk/api-noegle
python mcp/server.py                            # stdio transport
```

**Add to Claude Desktop** (`claude_desktop_config.json`) **or Claude Code** (`.mcp.json`):

```json
{
  "mcpServers": {
    "nummeropslag": {
      "command": "python",
      "args": ["/absolute/path/to/nummeropslag-api/mcp/server.py"],
      "env": { "NUMMEROPSLAG_API_KEY": "npk_your_key_here" }
    }
  }
}
```

Restart your client, then ask e.g. *"Is +45 70 10 20 30 spam?"* or *"Who owns 33 63 33 63?"*.

---

## Errors

Errors use a consistent envelope:

```json
{ "error": { "code": "forbidden", "message": "…", "details": {} } }
```

Common codes: `unauthorized` (missing/invalid key), `forbidden` (scope not allowed),
`rate_limited` (quota exceeded), `not_found`.

## Data & privacy

- Core data: official **CVR** (companies + production units) and the Danish **number plan** (SDFI, CC0).
- Spam verdicts use **k-anonymity** — a public "spam" label requires several independent reports.
- **Names of private individuals are never exposed.** Contacts are never uploaded (GDPR-compliant).

## License

The client examples and OpenAPI spec in this repository are released under the **MIT License**
(see [LICENSE](LICENSE)) — copy and adapt them freely. The Nummeropslag API service itself and its
data are proprietary; use is governed by the terms at [nummeropslag.dk](https://nummeropslag.dk).
