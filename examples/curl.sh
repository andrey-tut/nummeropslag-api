#!/usr/bin/env bash
# Nummeropslag Partner API — curl examples
# All endpoints require an API key. Get one at https://nummeropslag.dk/api-noegle
#   export NUMMEROPSLAG_API_KEY=npk_...
#   ./curl.sh 33633363
set -euo pipefail

BASE="https://nummeropslag.dk/api/v1"
KEY="${NUMMEROPSLAG_API_KEY:?Set NUMMEROPSLAG_API_KEY=npk_...}"
NUMBER="${1:-33633363}"

echo "# Full lookup (scope: lookup)"
curl -s -H "X-API-Key: $KEY" "$BASE/partner/lookup/$NUMBER" | jq .

echo "# Compact spam/trust verdict (scope: spam)"
curl -s -H "X-API-Key: $KEY" "$BASE/partner/spam/$NUMBER" | jq .

echo "# Operator + number type (scope: operator)"
curl -s -H "X-API-Key: $KEY" "$BASE/partner/operator/$NUMBER" | jq .

echo "# Search companies by name (CVR)"
curl -s -H "X-API-Key: $KEY" "$BASE/partner/search?q=netto" | jq .

echo "# API key status (plan, scopes, quota)"
curl -s -H "X-API-Key: $KEY" "$BASE/partner/me" | jq .
