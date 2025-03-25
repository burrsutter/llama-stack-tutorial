## Python super simple MCP Server

Uses `uv` and supergateway

```
cd python-server
```

```
brew install uv
```

```
uv add "mcp[cli]"
```

```
source .venv/bin/activate
```

```
npx -y supergateway --port 8001 --stdio "uv --directory /Users/burr/my-projects/llama-stack-tutorial/mcp-servers/python-mcp-server-math run mcp_server_sse_tools.py"
```