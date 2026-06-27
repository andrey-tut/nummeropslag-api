// Nummeropslag Partner API — minimal Node.js client (no dependencies, Node 18+ for global fetch).
// All endpoints require an API key. Get one at https://nummeropslag.dk/api-noegle
//   export NUMMEROPSLAG_API_KEY=npk_...
//   node node_client.js 33633363

const BASE = "https://nummeropslag.dk/api/v1";
const API_KEY = process.env.NUMMEROPSLAG_API_KEY || "";

async function get(path, params) {
  if (!API_KEY) throw new Error("Set NUMMEROPSLAG_API_KEY=npk_... (https://nummeropslag.dk/api-noegle)");
  const url = new URL(BASE + path);
  if (params) for (const [k, v] of Object.entries(params)) url.searchParams.set(k, v);
  const res = await fetch(url, { headers: { Accept: "application/json", "X-API-Key": API_KEY } });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

// Full lookup — operator, CVR companies, spam/trust (scope: lookup)
const partnerLookup = (e164) => get(`/partner/lookup/${e164}`);
// Compact spam/trust verdict (scope: spam)
const spamVerdict = (e164) => get(`/partner/spam/${e164}`);
// Operator + number type (scope: operator)
const operator = (e164) => get(`/partner/operator/${e164}`);
// Search companies by name in CVR (scope: lookup)
const search = (q) => get(`/partner/search`, { q });
// API key status: plan, scopes, quota
const me = () => get(`/partner/me`);

async function main() {
  const number = process.argv[2] || "33633363";
  console.log("Full lookup:");
  console.log(JSON.stringify(await partnerLookup(number), null, 2));
  console.log("\nSpam verdict:");
  console.log(JSON.stringify(await spamVerdict(number), null, 2));
}

main().catch((e) => {
  console.error("Error:", e.message);
  process.exit(1);
});

export { partnerLookup, spamVerdict, operator, search, me };
