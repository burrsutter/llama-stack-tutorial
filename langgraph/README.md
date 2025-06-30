## LangGraph Examples

```bash
uv pip install langgraph langchain
```

### Hello World

```python
from langgraph.graph import StateGraph, END

# Define the state (can be any dict-like structure)
class HelloWorldState(dict):
    pass

# Define node functions
def greet_node(state):
    print("👋 Hello from LangGraph!")
    return state

def farewell_node(state):
    print("👋 Goodbye from LangGraph!")
    return state

# Build the graph
builder = StateGraph(HelloWorldState)

# Add nodes
builder.add_node("greet", greet_node)
builder.add_node("farewell", farewell_node)

# Set edges
builder.set_entry_point("greet")
builder.add_edge("greet", "farewell")
builder.add_edge("farewell", END)

# Compile and run the graph
graph = builder.compile()
graph.invoke(HelloWorldState())
```


```bash
python 1-langgraph-hello.py
```

```
👋 Hello from LangGraph!
👋 Goodbye from LangGraph!
```

### 3 Nodes

```python
from langgraph.graph import StateGraph, END

# Define the state (can be any dict-like structure)
class HelloWorldState(dict):
    pass

# Define node functions
def greet_node(state):
    print("👋 Hello from LangGraph!")
    return state

def middle_node(state):
    print("🔄 This is the middle node.")
    return state

def farewell_node(state):
    print("👋 Goodbye from LangGraph!")
    return state

# Build the graph
builder = StateGraph(HelloWorldState)

# Add nodes
builder.add_node("greet", greet_node)
builder.add_node("farewell", farewell_node)
builder.add_node("middle", middle_node)

# Set edges
builder.set_entry_point("greet")
builder.add_edge("greet", "middle")
builder.add_edge("middle", "farewell")
builder.add_edge("farewell", END)

# Compile and run the graph
graph = builder.compile()
graph.invoke(HelloWorldState())
```

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
python 2-agent-add.py
```

```bash
python 2-agent-weather.py
```

## React Agent

## Built-in Tools via Llama Stack

### Web Search: Tavily

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

Add 8B model if needed

```bash
python 1-models-add.py
```

Try the Tavily tool

```bash
python 4-tools-tavily.py
```

```bash
cd langgraph
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

