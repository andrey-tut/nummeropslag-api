#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
version="${1:-1.0.0}"
build_dir="${repo_dir}/dist/mcpb-build"
artifact="${repo_dir}/dist/nummeropslag-mcp-${version}.mcpb"

rm -rf "${build_dir}"
mkdir -p "${build_dir}"

cp "${repo_dir}/mcpb/manifest.json" "${build_dir}/manifest.json"
cp "${repo_dir}/mcpb/pyproject.toml" "${build_dir}/pyproject.toml"
cp "${repo_dir}/mcpb/README.md" "${build_dir}/README.md"
cp "${repo_dir}/mcp/server.py" "${build_dir}/server.py"
curl -fsSL "https://nummeropslag.dk/static/img/favicon-192.png" -o "${build_dir}/icon.png"

npx --yes @anthropic-ai/mcpb@2.1.2 validate "${build_dir}/manifest.json"
npx --yes @anthropic-ai/mcpb@2.1.2 pack "${build_dir}" "${artifact}"

printf '%s\n' "${artifact}"
