const limit = Math.max(1, Math.min(50, Number($limit || 20)));
const url = new URL('https://nummeropslag.dk/api/v1/partner/search');
url.searchParams.set('q', $query);
url.searchParams.set('limit', String(limit));
const response = await fetch(url, {
  headers: {
    Accept: 'application/json',
    'X-API-Key': $vars.NUMMEROPSLAG_API_KEY,
    'X-Client': 'flowise',
  },
});
const body = await response.text();
if (!response.ok) throw new Error(`Nummeropslag HTTP ${response.status}: ${body}`);
return body;
