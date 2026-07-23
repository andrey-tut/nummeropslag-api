# Nummeropslag component for Langflow

This custom Langflow component adds five operations:

- full Danish phone-number lookup;
- compact spam/trust check;
- telecom operator and number type;
- official CVR business-name search;
- API key and quota status.

The query field supports Langflow Tool Mode, so the component can be connected
to an Agent's Tools input.

## Install

Copy the `nummeropslag` directory into a category directory under your
`LANGFLOW_COMPONENTS_PATH`, or mount this folder in Docker:

```bash
docker run -d \
  -p 7860:7860 \
  -v "$PWD:/app/custom_components" \
  -e LANGFLOW_COMPONENTS_PATH=/app/custom_components \
  langflowai/langflow:latest
```

Restart Langflow, add **Nummeropslag**, and enter an API key from
<https://nummeropslag.dk/api-noegle>.

The component uses only Python's standard library and requires no additional
runtime dependency.
