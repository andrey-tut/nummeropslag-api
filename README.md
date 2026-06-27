# Nummeropslag API

![API](https://img.shields.io/badge/API-REST-009688)
![OpenAPI](https://img.shields.io/badge/OpenAPI-3.1-6BA539?logo=openapiinitiative&logoColor=white)
![Auth](https://img.shields.io/badge/auth-API%20key-blue)
![Region](https://img.shields.io/badge/region-Denmark%20%F0%9F%87%A9%F0%9F%87%B0-C8102E)
![Examples](https://img.shields.io/badge/examples-curl%20%C2%B7%20python%20%C2%B7%20node%20%C2%B7%20php-lightgrey)
![License](https://img.shields.io/badge/examples%20license-MIT-green)

Public **Partner API** for Danish phone-number lookup, caller-ID and spam/trust signals.

Identify who is calling from a Danish number: company from the official **CVR** register,
**telecom operator**, number type, and a **spam/trust verdict** based on anonymous user
reports. Powered by official open data — not scraping.

> 🌐 Service: **[nummeropslag.dk](https://nummeropslag.dk)** · 🔑 Get a key: **[/api-noegle](https://nummeropslag.dk/api-noegle)** · 📘 Interactive docs: **[/docs](https://nummeropslag.dk/docs)**
>
> This repository contains **only public API docs, the OpenAPI spec and client examples**. The backend source is private.

---

## Authentication

All endpoints require an API key, sent in the `X-API-Key` header:

```http
X-API-Key: pk_your_key_here
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
export NUMMEROPSLAG_API_KEY=pk_your_key_here

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
