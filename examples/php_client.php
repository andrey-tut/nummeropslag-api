<?php
// Nummeropslag Partner API — minimal PHP client (curl).
// All endpoints require an API key. Get one at https://nummeropslag.dk/api-noegle
//   NUMMEROPSLAG_API_KEY=pk_... php php_client.php 33633363

const BASE = "https://nummeropslag.dk/api/v1";

function api_get(string $path, array $params = []): array {
    $key = getenv("NUMMEROPSLAG_API_KEY") ?: "";
    if ($key === "") { fwrite(STDERR, "Set NUMMEROPSLAG_API_KEY=pk_... (https://nummeropslag.dk/api-noegle)\n"); exit(1); }
    $url = BASE . $path;
    if ($params) $url .= "?" . http_build_query($params);
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER     => ["Accept: application/json", "X-API-Key: " . $key],
        CURLOPT_TIMEOUT        => 15,
    ]);
    $body = curl_exec($ch);
    $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    if ($code >= 400) { fwrite(STDERR, "HTTP $code\n"); exit(1); }
    return json_decode($body, true);
}

// Full lookup — operator, CVR companies, spam/trust (scope: lookup)
function partner_lookup(string $e164): array { return api_get("/partner/lookup/$e164"); }
// Compact spam/trust verdict (scope: spam)
function spam_verdict(string $e164): array { return api_get("/partner/spam/$e164"); }
// Operator + number type (scope: operator)
function operator(string $e164): array { return api_get("/partner/operator/$e164"); }
// Search companies by name in CVR (scope: lookup)
function search(string $q): array { return api_get("/partner/search", ["q" => $q]); }

$number = $argv[1] ?? "33633363";
echo "Full lookup:\n";
echo json_encode(partner_lookup($number), JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n";
echo "\nSpam verdict:\n";
echo json_encode(spam_verdict($number), JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n";
