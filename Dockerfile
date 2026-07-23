FROM python:3.12-slim

LABEL org.opencontainers.image.title="Nummeropslag MCP"
LABEL org.opencontainers.image.description="Privacy-first Danish phone-number lookup MCP server"
LABEL org.opencontainers.image.source="https://github.com/andrey-tut/nummeropslag-api"
LABEL org.opencontainers.image.licenses="MIT"
LABEL io.modelcontextprotocol.server.name="io.github.andrey-tut/nummeropslag"

WORKDIR /app

COPY mcp/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --requirement requirements.txt

COPY mcp/server.py ./server.py

ENTRYPOINT ["python", "server.py"]
