# n8n-nodes-nummeropslag

An [n8n](https://n8n.io/) community node for privacy-first Danish caller ID and
reverse phone lookup through [Nummeropslag](https://nummeropslag.dk/).

The node uses official CVR and Danish number-plan data plus anonymous community
spam reports. It never uploads contacts and never returns names of private
individuals.

## Operations

- **Look Up Number** — company, operator, number type, spam/trust and comments.
- **Check Spam** — compact spam/scam verdict for routing workflows.
- **Get Operator** — operator and number type.
- **Search Businesses** — search Danish companies by name in CVR data.
- **Get API Status** — scopes, quota and current usage.

Every operation can also be exposed as an n8n AI tool.

## Installation

Install `n8n-nodes-nummeropslag` from **Settings → Community Nodes** in a
self-hosted n8n instance, or follow the
[n8n community-node installation guide](https://docs.n8n.io/integrations/community-nodes/installation/).

## Credentials

1. Get a Nummeropslag API key at <https://nummeropslag.dk/api-noegle>.
2. Create a **Nummeropslag API** credential in n8n.
3. Paste the key. n8n stores it as a secret credential and sends it only in the
   `X-API-Key` header to `https://nummeropslag.dk`.

## Example workflows

- Route likely spam calls to an alert channel.
- Enrich CRM leads with registered Danish company data.
- Verify the operator and number type before sending an SMS.
- Let an n8n AI Agent look up a caller without exposing private contacts.

## Development

```bash
npm install
npm run lint
npm run build
```

API documentation: <https://andrey-tut.github.io/nummeropslag-api/>

## License

MIT
