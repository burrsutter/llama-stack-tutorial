## LangGraph Examples

```bash
uv pip install langgraph langchain
```

```bash
python 1-langgraph-hello.py
```

```
👋 Hello from LangGraph!
👋 Goodbye from LangGraph!
```

### 3 Nodes

```bash
python 1-langgraph-3-node.py
```

```
👋 Hello from LangGraph!
🔄 This is the middle node.
👋 Goodbye from LangGraph!
```

## Agent

```bash
uv pip install langgraph langchain openai langchain_openai dotenv langchain_community
```


```bash
export LLAMA_STACK_ENDPOINT_OPENAI=http://localhost:8321/v1/openai/v1
export INFERENCE_MODEL=meta-llama/Llama-3.1-8B-Instruct
```

```bash
python ../1-models-add.py
```

```bash
curl -sS $LLAMA_STACK_ENDPOINT_OPENAI/models | jq -r '.data[].id'
```

```bash
python 2-agent-add.py
```

```bash
python 2-agent-weather.py
```

## React Agent

## Built-in Tools via Llama Stack

### Web Search: Tavily

Start the Llama Stack Server with the Tavily key set


```bash
export TAVILY_SEARCH_API_KEY=tvly-dev-stuff
```

```bash
TAVILY_SEARCH_API_KEY=tvly-dev-stuff uv run --with llama-stack llama stack build --template ollama --image-type venv 
```

Find the run.yaml reference in the output

```
You can find the newly-built template here: /Users/bsutter/ai-projects/llama-stack-tutorial/.venv/lib/python3.12/site-packages/llama_stack/templates/ollama/run.yaml
You can run the new Llama Stack distro via: llama stack run /Users/bsutter/ai-projects/llama-stack-tutorial/.venv/lib/python3.12/site-packages/llama_stack/templates/ollama/run.yaml --image-type venv
```

Edit that run.yaml and find

```
api_key: ${env.TAVILY_SEARCH_API_KEY:+}
```

Add your API key, save run.yaml

Run the server

```bash
llama stack run /Users/bsutter/ai-projects/llama-stack-tutorial/.venv/lib/python3.12/site-packages/llama_stack/templates/ollama/run.yaml --image-type venv
```

Query the registered toolgroups

```bash
curl -sS -H "Content-Type: application/json" $LLAMA_STACK_ENDPOINT/v1/toolgroups | jq
```

```json
{
  "data": [
    {
      "identifier": "builtin::websearch",
      "provider_resource_id": "builtin::websearch",
      "provider_id": "tavily-search",
      "type": "tool_group",
      "mcp_endpoint": null,
      "args": null
    },
    {
      "identifier": "builtin::rag",
      "provider_resource_id": "builtin::rag",
      "provider_id": "rag-runtime",
      "type": "tool_group",
      "mcp_endpoint": null,
      "args": null
    },
    {
      "identifier": "builtin::wolfram_alpha",
      "provider_resource_id": "builtin::wolfram_alpha",
      "provider_id": "wolfram-alpha",
      "type": "tool_group",
      "mcp_endpoint": null,
      "args": null
    }
  ]
}
```

Try the Tavily tool to see if it is working

```bash
?
```

```bash
python 3-agent-react-builtin-websearch.py
```


## MCP via LLama Stack

### MCP Server in Python

```bash
cd ../mcp-servers/python-mcp-server-math
```

Run the MCP Server

```bash
npx -y supergateway --port 8001 --stdio "uv --directory /Users/burr/my-projects/llama-stack-tutorial/mcp-servers/python-mcp-server-math run mcp_server_sse_tools.py"
```

Register the MCP Server

```bash
curl -X POST -H "Content-Type: application/json" --data '{ "provider_id" : "model-context-protocol", "toolgroup_id" : "mcp::my-python-mcp-server-math", "mcp_endpoint" : { "uri" : "http://host.docker.internal:8001/sse"}}' $LLAMA_STACK_ENDPOINT/v1/toolgroups
```

What MCP Servers does LLama Stack have registered?

```bash
curl -sS -H "Content-Type: application/json" $LLAMA_STACK_ENDPOINT/v1/toolgroups | jq -r '.data[] | select(.identifier | startswith("mcp::")) | .identifier'
```

```
mcp::my-python-mcp-server-math
```

