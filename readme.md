https://llama-stack.readthedocs.io/en/latest/getting_started/index.html

## Ollama server

**Terminal 1**

```
ollama serve
```

**Terminal 2**

Llama Stack does not dynamically load models even though that is a feature of ollama.  Use the "keepalive" technique otherwise ollama quickly returns that memory back to the host

```
ollama run llama3.2:3b-instruct-fp16 --keepalive 60m
```

To check if the model is still running and in memory

```
ollama ps
```

## Llama Stack Server

**Terminal 3**

```
export LLAMA_STACK_MODEL="meta-llama/Llama-3.2-3B-Instruct"
export INFERENCE_MODEL="meta-llama/Llama-3.2-3B-Instruct"
export LLAMA_STACK_PORT=8321
export LLAMA_STACK_SERVER=http://localhost:$LLAMA_STACK_PORT
```

Reset data

```
rm -rf ~/.llama
mkdir -p ~/.llama
```

**Terminal 3**

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

**Terminal 4**
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

I use `jq` to parse the JSON returned by the curl command.  It is optional, your eyeballs can parse the JSON.

```
brew install jq
```

```
curl -sS $LLAMA_STACK_SERVER/v1/models -H "Content-Type: application/json" | jq -r '.data[].identifier'
```

Results:

```
meta-llama/Llama-3.2-3B-Instruct
all-MiniLM-L6-v2
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

Check out requirements.txt and install the deps if needed

```
pip install -r requirements.txt
```

To prove connectivity and find out more about the capabilities of the server

Code originally from  https://llama-stack.readthedocs.io/en/latest/getting_started/index.html#run-inference-with-python-sdk

### Test of setup

```
python 0-test.py
```

Lots of configuration output and then a haiku

```
Here is a haiku about coding:

Lines of code unfold
Logic flows through digital night
Beauty in the bits
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

### Add a model


Make sure ollama has the model running

```
ollama run llama3.1:8b-instruct-fp16 --keepalive 60m
```

```
python 1-models-add.py
```

```
llama-stack-client models list
```

```
Available Models

┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ model_type ┃ identifier                       ┃ provider_resource_id      ┃ metadata                       ┃ provider_id          ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ llm        │ meta-llama/Llama-3.2-3B-Instruct │ llama3.2:3b-instruct-fp16 │                                │ ollama               │
├────────────┼──────────────────────────────────┼───────────────────────────┼────────────────────────────────┼──────────────────────┤
│ embedding  │ all-MiniLM-L6-v2                 │ all-MiniLM-L6-v2          │ {'embedding_dimension': 384.0} │ sentence-transforme… │
├────────────┼──────────────────────────────────┼───────────────────────────┼────────────────────────────────┼──────────────────────┤
│ llm        │ meta-llama/Llama-3.1:8B-Instruct │ llama3.1:8b-instruct-fp16 │ {'description':                │ ollama               │
│            │                                  │                           │ 'llama3.1:8b-instruct-fp16 via │                      │
│            │                                  │                           │ ollama'}                       │                      │
└────────────┴──────────────────────────────────┴───────────────────────────┴────────────────────────────────┴──────────────────────┘

Total models: 3
```

### Delete a model

Does not work as of March 23

```
python 1-models-delete.py
```

### simple chat-completions example

```
python 2-chat-completions.py
```

### Structured Output

```
python 3-structured-output.py 
```

### Tools

```
python 4-tools-weather.py
```

### Agents

```
python 5-base-agent.py
```

### Agents with Tools

Stop the docker run

Get an API KEY

https://app.tavily.com/home

```
export TAVILY_SEARCH_API_KEY=your-key
```

```
docker run -it \
  -p $LLAMA_STACK_PORT:$LLAMA_STACK_PORT \
  -v ~/.llama:/root/.llama \
  llamastack/distribution-ollama \
  --port $LLAMA_STACK_PORT \
  --env INFERENCE_MODEL=$LLAMA_STACK_MODEL \
  --env TAVILY_SEARCH_API_KEY=$TAVILY_SEARCH_API_KEY \
  --env OLLAMA_URL=http://host.docker.internal:11434
```

Add meta-llama/Llama-3.1-8B-Instruct

```
python 1-models-add.py
```

```
python 5-basic-agent-websearch-tool.py
```

```
The winner of the last Super Bowl was the Philadelphia Eagles who defeated the Kansas City Chiefs with a score of 40-22 in Super Bowl LIX.
```

With Tavily Search (already pre-registered, see run `python 0-test.py`)

export TAVILY_SEARCH_API_KEY=your-key

And there is a `tavily-test.py` to test your key/connectivity

```
python 5-base-agent-tavily-tool.py
```

### RAG

As of March 23, the 0.1.8 version is not on pypi.org, so install client directly from github

```
pip install git+https://github.com/meta-llama/llama-stack-client-python.git
pip install llama-stack
pip install aiosqlite
pip install ollama
pip install openai
pip install datasets
pip install opentelemetry-instrumentation
pip install opentelemetry-exporter-otlp
pip install faiss-cpu
pip install mcp
pip install autoevals
# pip install opentelemetry-exporter-prometheus
```

```
python 5-basic-rag.py
```

### Shields (Safety, Guardrails)

```
ollama pull llama-guard3:8b-q4_0
```

```
ollama run llama-guard3:8b-q4_0 --keepalive 60m
```


Shut-down any previously running Llama Stack server

```
docker ps
```

note: your container id will be different

```
docker stop fc3eae32f44c
```

Not sure if the following is needed?

```
export SAFETY_MODEL="meta-llama/Llama-Guard-3-8B"
```

but starting/restarting clean is often a good idea

```
rm -rf ~/.llama
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

Register the guard/guardian model

```
python 1-models-add-guard.py
```

Register the shield and attempt to use it

```
python 6-shield-content.py
```

See the registered shields

```
python list-shields.py
```

Now an agent + shield

```
python 6-agent-shield.py
```


### MCP Servers

The file system MCP server is one of the easiest, git it up and running in a terminal.


New terminal to run the MCP server process

```
cd node-stdio-server-math
```

See its readme.md for how to start it up

Register the toolgroup

```
curl -X POST -H "Content-Type: application/json" --data '{ "provider_id" : "model-context-protocol", "toolgroup_id" : "mcp::my-node-server-math", "mcp_endpoint" : { "uri" : "http://host.docker.internal:8002/sse"}}' http://localhost:8321/v1/toolgroups
```

```
python 7-mcp-client-node-server.py
```

#### Web page fetcher tool

Included in the MCP python-sdk

```
git clone https://github.com/modelcontextprotocol/python-sdk
```

```
cd python-sdk/examples/servers/simple-tool
```

review README.md

```
export MCP_PORT=8005
uv run mcp-simple-tool --transport sse --port $MCP_PORT
```

```
INFO:     Started server process [84213]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8005 (Press CTRL+C to quit)
```

```
curl -X POST -H "Content-Type: application/json" --data '{ "provider_id" : "model-context-protocol", "toolgroup_id" : "mcp::mcp-website-fetcher", "mcp_endpoint" : { "uri" : "http://host.docker.internal:8005/sse"}}' http://localhost:8321/v1/toolgroups
```

```
python 7-mcp-client-web-page-fetcher.py
```



## Library Mode

Using Llama Stack as an embedded library/framework instead of a remote API server.

Still using ollama 

https://llama-stack.readthedocs.io/en/latest/distributions/importing_as_library.html

```
python3.11 -m venv venv
```

```
source venv/bin/activate
```

```
pip install llama-stack
pip install aiosqlite
pip install ollama
pip install openai
pip install datasets
pip install opentelemetry-instrumentation
pip install opentelemetry-exporter-prometheus
pip install opentelemetry-exporter-otlp
pip install faiss-cpu
pip install mcp
pip install autoevals
pip install bwrap
```

```
python 0-test-library-client.py
```

## Playground


```
export LLAMA_STACK_ENDPOINT=http://localhost:8321
```

```
git clone https://github.com/meta-llama/llama-stack

cd llama-stack/llama_stack/distribution/ui

pip install -r requirements.txt

pip install llama_stack

streamlit run app.py
```

Check out the README.md in that director for more ideass


## ToDos

Shields output

https://github.com/meta-llama/llama-stack/pull/1419


https://llama-stack.readthedocs.io/en/latest/building_applications/rag.html
versus
https://github.com/burrsutter/python-plain-agentic-examples/tree/main/rag

Working Tavily+Agent

Working Brave+Agent

PatternFly Chatbot
https://github.com/patternfly/chatbot

Playground
https://llama-stack.readthedocs.io/en/latest/playground/index.html
/Users/burr/my-projects/llama-stack/llama_stack/distribution/ui

agent steps
   response = agent.create_turn(
        messages=[
            {
                "role": "user",
                "content": "Call get_boiling_point twice to answer: What is the boiling point of polyjuice in both celsius and fahrenheit?",
            },
        ],
        session_id=session_id,
        stream=False,
    )
    steps = response.steps
    assert len(steps) == 7
    assert steps[0].step_type == "shield_call"
    assert steps[1].step_type == "inference"
    assert steps[2].step_type == "shield_call"
    assert steps[3].step_type == "tool_execution"
    assert steps[4].step_type == "shield_call"
    assert steps[5].step_type == "inference"
    assert steps[6].step_type == "shield_call"


## Clean Docker

```
docker kill $(docker ps -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q)
docker system prune -a --volumes
```