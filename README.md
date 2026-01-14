
### Testing

Get session ID

```bash
curl -L -X POST http://127.0.0.1:8000/mcp/ \
  -H "Content-Type: application/json" \
  -H "MCP-Protocol-Version: 2025-06-18" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{"tools":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}'

export SESSION_ID=session_id
```

List tools

```bash
curl -L -X POST http://127.0.0.1:8000/mcp/ \
  -H "Content-Type: application/json" \
  -H "MCP-Protocol-Version: 2025-06-18" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
```

Call tool

```bash
curl -L -X POST http://127.0.0.1:8000/mcp/ \
  -H "Content-Type: application/json" \
  -H "MCP-Protocol-Version: 2025-06-18" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"scrape","arguments":{"url":"https://github.com","prompt":"Summarize"}}}'
```

Run local

```bash
podman run -it \
  -e HOST=0.0.0.0 \
  -e PORT=8000 \
  -e OPENAI_BASE_URL=http://localhost:9000/v1 \
  -e OPENAI_MODEL=model-name \
  -e OPENAI_MODEL_TOKENS=8192 \
  -e OPENAI_EMBEDDING_BASE_URL=http://localhost:9000/v1 \
  -e OPENAI_EMBEDDING_MODEL=embedding-model-name \
  -e OPENAI_EMBEDDING_MODEL_TOKENS=8192 \
  localhost/scrape:latest
```

References:
- https://github.com/oleksandrsirenko/mcp-simple-server