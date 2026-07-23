const response = await fetch('https://nummeropslag.dk/api/v1/partner/me', {
  headers: {
    Accept: 'application/json',
    'X-API-Key': $vars.NUMMEROPSLAG_API_KEY,
    'X-Client': 'flowise',
  },
});
const body = await response.text();
if (!response.ok) throw new Error(`Nummeropslag HTTP ${response.status}: ${body}`);
return body;
