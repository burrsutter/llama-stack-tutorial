https://llama-stack.readthedocs.io/en/latest/getting_started/index.html

## Ollama server
```
ollama serve
```

```
ollama run llama3.2:3b-instruct-fp16 --keepalive 60m
```

## Llama Stack Server

```
export LLAMA_STACK_MODEL="meta-llama/Llama-3.2-3B-Instruct"
export INFERENCE_MODEL="meta-llama/Llama-3.2-3B-Instruct"
export LLAMA_STACK_PORT=8321
export LLAMA_STACK_SERVER=http://localhost:$LLAMA_STACK_PORT
```

```
mkdir -p ~/.llama
```

```
docker run -it \
  -p $LLAMA_STACK_PORT:$LLAMA_STACK_PORT \
  -v ~/.llama:/root/.llama \
  llamastack/distribution-ollama \
  --port $LLAMA_STACK_PORT \
  --env INFERENCE_MODEL=$LLAMA_STACK_MODEL \
  --env OLLAMA_URL=http://host.docker.internal:11434
```


## Client library CLI

```
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```


```
pip install llama-stack-client
```

```
llama-stack-client configure --endpoint $LLAMA_STACK_SERVER
```

```
> Enter the API key (leave empty if no key is needed):
```

Hit Enter

```
llama-stack-client models list
```

```
Available Models

┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┓
┃ model_type   ┃ identifier                           ┃ provider_resource_id         ┃ metadata                          ┃ provider_id           ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━┩
│ llm          │ meta-llama/Llama-3.2-3B-Instruct     │ llama3.2:3b-instruct-fp16    │                                   │ ollama                │
├──────────────┼──────────────────────────────────────┼──────────────────────────────┼───────────────────────────────────┼───────────────────────┤
│ embedding    │ all-MiniLM-L6-v2                     │ all-MiniLM-L6-v2             │ {'embedding_dimension': 384.0}    │ sentence-transformers │
└──────────────┴──────────────────────────────────────┴──────────────────────────────┴───────────────────────────────────┴───────────────────────┘

Total models: 2
```

```
llama-stack-client \
  inference chat-completion \
  --message "hello, what model are you?"
```

```
ChatCompletionResponse(
    completion_message=CompletionMessage(
        content='Hello! I\'m an AI designed to assist and communicate with users in a helpful and informative way. My primary function is to
provide information, answer questions, and engage in conversation on a wide range of topics.\n\nI\'m a type of artificial intelligence (AI) called
a large language model, which means I\'ve been trained on a massive dataset of text from various sources, including books, articles, research
papers, and online conversations. This training allows me to understand and generate human-like language, including grammar, syntax, and
vocabulary.\n\nMy architecture is based on a transformer model, which is a type of neural network designed specifically for natural language
processing tasks like language translation, question-answering, and text generation.\n\nI don\'t have a specific name or brand, but I\'m often
referred to as a "chatbot" or a "conversational AI." My goal is to provide accurate and helpful information, while also being friendly and
engaging in conversation. How can I assist you today?',
        role='assistant',
        stop_reason='end_of_turn',
        tool_calls=[]
    ),
    logprobs=None
)
```

## curl

```
curl -sS $LLAMA_STACK_SERVER/v1/models \
  -H "Content-Type: application/json" | jq -r '.data[].identifier'
```

```
curl -sS $LLAMA_STACK_SERVER/v1/inference/chat-completion \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d "{
     \"model_id\": \"$LLAMA_STACK_MODEL\",
     \"messages\": [{\"role\": \"user\", \"content\": \"what model are you?\"}],
     \"temperature\": 0.0
   }" | jq -r '.completion_message | select(.role == "assistant") | .content'
```


## Python

```
pip install llama_stack
pip install aiosqlite
pip install ollama
pip install faiss-cpu
pip install chardet
pip install pypdf
pip install datasets
pip install bwrap
pip install opentelemetry-instrumentation
pip install opentelemetry.exporter
pip install opentelemetry-exporter-prometheus
pip install opentelemetry-exporter-otlp
pip install autoevals
pip install sentence.transformers
pip install openai
pip install sqlite_vec
```

To prove connectivity and find out more about the capabilities of the server

Code originally from  https://llama-stack.readthedocs.io/en/latest/getting_started/index.html#run-inference-with-python-sdk

### Test of setup

```
python 0-test.py
```

```
Using config ollama:
apis:
- agents
- datasetio
- eval
- inference
- safety
- scoring
- telemetry
- tool_runtime
- vector_io
benchmarks: []
container_image: null
datasets: []
image_name: ollama
metadata_store:
  db_path: /Users/burr/.llama/distributions/ollama/registry.db
  namespace: null
  type: sqlite
models:
- metadata: {}
  model_id: meta-llama/Llama-3.2-3B-Instruct
  model_type: !!python/object/apply:llama_stack.apis.models.models.ModelType
  - llm
  provider_id: ollama
  provider_model_id: null
- metadata:
    embedding_dimension: 384
  model_id: all-MiniLM-L6-v2
  model_type: !!python/object/apply:llama_stack.apis.models.models.ModelType
  - embedding
  provider_id: sentence-transformers
  provider_model_id: null
providers:
  agents:
  - config:
      persistence_store:
        db_path: /Users/burr/.llama/distributions/ollama/agents_store.db
        namespace: null
        type: sqlite
    provider_id: meta-reference
    provider_type: inline::meta-reference
  datasetio:
  - config: {}
    provider_id: huggingface
    provider_type: remote::huggingface
  - config: {}
    provider_id: localfs
    provider_type: inline::localfs
  eval:
  - config: {}
    provider_id: meta-reference
    provider_type: inline::meta-reference
  inference:
  - config:
      url: http://localhost:11434
    provider_id: ollama
    provider_type: remote::ollama
  - config: {}
    provider_id: sentence-transformers
    provider_type: inline::sentence-transformers
  safety:
  - config: {}
    provider_id: llama-guard
    provider_type: inline::llama-guard
  scoring:
  - config: {}
    provider_id: basic
    provider_type: inline::basic
  - config: {}
    provider_id: llm-as-judge
    provider_type: inline::llm-as-judge
  - config:
      openai_api_key: '********'
    provider_id: braintrust
    provider_type: inline::braintrust
  telemetry:
  - config:
      service_name: llama-stack
      sinks: sqlite
      sqlite_db_path: /Users/burr/.llama/distributions/ollama/trace_store.db
    provider_id: meta-reference
    provider_type: inline::meta-reference
  tool_runtime:
  - config:
      api_key: '********'
      max_results: 3
    provider_id: brave-search
    provider_type: remote::brave-search
  - config:
      api_key: '********'
      max_results: 3
    provider_id: tavily-search
    provider_type: remote::tavily-search
  - config: {}
    provider_id: code-interpreter
    provider_type: inline::code-interpreter
  - config: {}
    provider_id: rag-runtime
    provider_type: inline::rag-runtime
  vector_io:
  - config:
      kvstore:
        db_path: /Users/burr/.llama/distributions/ollama/faiss_store.db
        namespace: null
        type: sqlite
    provider_id: faiss
    provider_type: inline::faiss
  - config:
      db_path: /Users/burr/.llama/distributions/ollama/sqlite_vec.db
      kvstore:
        db_path: /Users/burr/.llama/distributions/ollama/sqlite_vec.db
        namespace: null
        type: sqlite
    provider_id: sqlite_vec
    provider_type: inline::sqlite_vec
scoring_fns: []
server:
  port: 8321
  tls_certfile: null
  tls_keyfile: null
shields: []
tool_groups:
- args: null
  mcp_endpoint: null
  provider_id: tavily-search
  toolgroup_id: builtin::websearch
- args: null
  mcp_endpoint: null
  provider_id: rag-runtime
  toolgroup_id: builtin::rag
- args: null
  mcp_endpoint: null
  provider_id: code-interpreter
  toolgroup_id: builtin::code_interpreter
vector_dbs: []
version: '2'

--- Available models: ---
- all-MiniLM-L6-v2
- meta-llama/Llama-3.2-3B-Instruct

Here is a haiku about coding:

Lines of code unfold
Logic flows through digital night
Beauty in the bits
Error exporting span to SQLite: Cannot operate on a closed database.
```

### List of models

```
python 1-models.py
```

```
--- Available models: ---
- all-MiniLM-L6-v2
- meta-llama/Llama-3.2-3B-Instruct
```

### simple chat-completions example

```
python 2-chat-completions.py
```

### Structured Output

### Tools

### RAG

```
python 5-basic-rag.py
```

### Agents

From https://github.com/amfred/llama-stack-apps/tree/amf-test-client/examples/agents


