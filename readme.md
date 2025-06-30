Original docs 

https://llama-stack.readthedocs.io/en/latest/getting_started/

Note: Most of these examples use the "client-server" approach.  There is also a library mode that is some of the examples but commented out.

## Ollama server

**Terminal 1**

```bash
ollama serve
```

**Terminal 2**

Use the "keepalive" parameter otherwise ollama quickly returns that memory back to the host


```bash
ollama run llama3.2:3b-instruct-fp16 --keepalive 60m
```

Note: this blocks the terminal as `ollama run` allows you to chat with the model.  

Use 

```bash
/bye
```

And then `ollama ps` to see if the model is still in memory


## Llama Stack Server

**Terminal 3**

There is some repetition below as I find different examples that would like slightly different env vars

```
export LLAMA_STACK_MODEL="meta-llama/Llama-3.2-3B-Instruct"
export INFERENCE_MODEL="meta-llama/Llama-3.2-3B-Instruct"
export LLAMA_STACK_PORT=8321
export LLAMA_STACK_SERVER=http://localhost:$LLAMA_STACK_PORT
export LLAMA_STACK_ENDPOINT=$LLAMA_STACK_SERVER
export LLAMA_STACK_ENDPOINT_OPENAI=$LLAMA_STACK_ENDPOINT/v1/openai/v1
```

Reset local data used by Llama Stack Server if using `docker` or `podman`.



```
rm -rf ~/.llama
mkdir -p ~/.llama
ls ~/.llama
```

**Terminal 3**

### uv approach

start clean

```bash
uv cache clean 
```

```bash
rm -rf .venv
```

```bash
rm -rf /Users/bsutter/.llama/distributions/ollama/
```

```bash
brew install python@3.12
uv venv .venv --python "/opt/homebrew/bin/python3.12"
source .venv/bin/activate
```

double check your python version

```bash
python --version
```

Check out requirements.txt and install the dependencies

```bash
uv pip install -r requirements.txt
```

Note: requirements.txt dependencies are NOT versioned in most cases.  Trying to stay on latest/greatest.

```bash
uv pip list | grep llama
llama_stack                              0.2.13
llama_stack_client                       0.2.13
ollama                                   0.5.1
```


```bash
uv run --with llama-stack llama stack build --template ollama --image-type venv --run
```


### docker, podman approach

```bash
docker run -it \
  -p $LLAMA_STACK_PORT:$LLAMA_STACK_PORT \
  -v ~/.llama:/root/.llama \
  llamastack/distribution-ollama \
  --port $LLAMA_STACK_PORT \
  --env INFERENCE_MODEL=$LLAMA_STACK_MODEL \
  --env OLLAMA_URL=http://host.docker.internal:11434
```

or 


```bash
podman run -it \
  -p $LLAMA_STACK_PORT:$LLAMA_STACK_PORT \
  -v ~/.llama:/root/.llama \
  --env INFERENCE_MODEL=$LLAMA_STACK_MODEL \
  --env OLLAMA_URL=http://host.containers.internal:11434 \
  llamastack/distribution-ollama \
  --port $LLAMA_STACK_PORT
```


You may need to start your podman backend

```bash
podman machine start
```


## Client library CLI

**Terminal 4**

```bash
source .venv/bin/activate
```


```bash
llama-stack-client configure --endpoint $LLAMA_STACK_SERVER
```

```
> Enter the API key (leave empty if no key is needed):
```

Hit Enter

```bash
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

```bash
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

```bash
brew install jq
```

Using Llama Stack API endpoint

```bash
curl -sS $LLAMA_STACK_SERVER/v1/models -H "Content-Type: application/json" | jq -r '.data[].identifier'
```

Results:

```
meta-llama/Llama-3.2-3B-Instruct
all-MiniLM-L6-v2
```

Using OpenAI API endpoint

```bash
curl -sS $LLAMA_STACK_ENDPOINT_OPENAI/models | jq -r '.data[].id'
```

Chat completions using Llama Stack API

```bash
curl -sS $LLAMA_STACK_SERVER/v1/inference/chat-completion \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d "{
     \"model_id\": \"$LLAMA_STACK_MODEL\",
     \"messages\": [{\"role\": \"user\", \"content\": \"what model are you?\"}],
     \"temperature\": 0.0
   }" | jq -r '.completion_message | select(.role == "assistant") | .content'
```

Chat completions using OpenAI API


```bash
API_KEY="none"
MODEL_NAME="meta-llama/Llama-3.2-3B-Instruct"
QUESTION="What model are you?"

curl -sS $LLAMA_STACK_ENDPOINT_OPENAI/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d "{
     \"model\": \"$MODEL_NAME\",
     \"messages\": [{\"role\": \"user\", \"content\": \"$QUESTION\"}],
     \"temperature\": 0.0
   }" | jq -r '.choices[0].message.content'
```


## Python


To prove connectivity and find out more about the capabilities of the server

Code originally from  https://llama-stack.readthedocs.io/en/latest/getting_started/index.html#run-inference-with-python-sdk

### Test of setup

```bash
python 0-test-remote-client.py
```

Lots of configuration output and then a haiku

```
Here is a haiku about coding:

Lines of code unfold
Logic flows through digital night
Beauty in the bits
```

Test OpenAI API compatibility 

Note: "v1/openai/v1" appended to the Llama Stack server host/port

```bash
python 0-test-remote-client-openai.py
```

### List of models

```bash
python 1-models.py
```

```
--- Available models: ---
- all-MiniLM-L6-v2
- meta-llama/Llama-3.2-3B-Instruct
```

### Add a bigger model

Make sure ollama has the model running

As of 0.2.2, the --keepalive is no longer required.  However, you do need to `ollama pull` 

```bash
ollama run llama3.1:8b-instruct-fp16 --keepalive 60m
```

```bash
python 1-models-add.py
```

```bash
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

We will add the Guard model later for shields/safety

### Delete a model

Note: we do use the 8b model later, this is just to exercise the API

```bash
python 1-models-delete.py
```

### simple chat-completions example

```bash
python 2-chat-completions.py
```

```bash
python 2-chat-completions-weather.py
```

```
Please note that I'm a text-based AI model and do not have the ability to access current information in real-time. If you need the most up-to-date temperature, please try one of the above options.
```

Because "what's the weather?" is the way you show off tools and MCP later on

```
python 2-chat-completions-logger.py
```

Use of dotenv and logger. A bit more advanced, sprinkled throughout some of the following examples.  Also shows off a hallunication

```
Burr Sutter is an American entrepreneur and the co-founder of GitHub, a web-based platform for version control and collaboration on software development projects. He co-founded GitHub in 2008 with Tom Preston-Werner and Chris Wanstrath.
```

### OpenAI API compatibility

```bash
export API_KEY=none
export MODEL_NAME="meta-llama/Llama-3.2-3B-Instruct"
export INFERENCE_SERVER_URL=$LLAMA_STACK_SERVER/v1/openai/v1
```

```bash
python 2-chat-completions-weather-openai.py
```

### Structured Output

Uses Pydantic model

```bash
python 3-structured-output.py 
```

```bash
python 3-structured-output-leopard.py
```

Structured output means you can get formatted responses from the LLM that allow for programmatic control

With OpenAI API

```bash
python 3-structured-output-openai.py
```

### Tools

Using tools, JSON declaration

```bash
export API_KEY=none
export MODEL_NAME="meta-llama/Llama-3.1-8B-Instruct"
export INFERENCE_SERVER_URL=$LLAMA_STACK_SERVER/v1/openai/v1
```

```bash
python 4-tools-weather-openai.py
```

Get an API KEY

https://app.tavily.com/home

```bash
export TAVILY_SEARCH_API_KEY=your-key
```

Restart Llama Stack server 

Add meta-llama/Llama-3.1-8B-Instruct if you have not already

```bash
python 4-tools-tavily.py
```

Proves you have connectivity to tavily

```bash
python list-tools.py
```

### Agents

```
python 5-basic-agent.py
```

### Agents with Tools


Get an API KEY

https://app.tavily.com/home

```bash
export TAVILY_SEARCH_API_KEY=your-key
```

Add meta-llama/Llama-3.1-8B-Instruct if you have not already

```bash
python 1-models-add.py
```

```bash
python 1-models.py
```

```bash
--- Available models: ---
all-MiniLM-L6-v2 - ollama - all-minilm:latest
meta-llama/Llama-3.1-8B-Instruct - ollama - llama3.1:8b-instruct-fp16
meta-llama/Llama-3.2-3B-Instruct - ollama - llama3.2:3b-instruct-fp16
```

Note: you do not need both 3B and 8B normally. 

```bash
python 5-basic-agent-websearch-tool.py
```

If it works it should result in something like the following.
```
The winner of the last Super Bowl was the Philadelphia Eagles who defeated the Kansas City Chiefs with a score of 40-22 in Super Bowl LIX.
```

With Tavily Search (already pre-registered)

export TAVILY_SEARCH_API_KEY=your-key

And there is a `test-tavily.py` to test your key/connectivity

```
python 5-basic-agent-tavily-tool.py
```

Note: seems to perform the web search but does NOT provide a "good" answer.  You should also notice the logs indicate it is attempting to use the brave search yet needs the tavily api key.

```
python 5-basic-agent-brave-tool.py
```


### RAG

If the version you need is not yet on pypi.org, install client directly from github

If you need to clean your previously downloaded pips:

```
rm -rf .venv
python3.11 -m venv .venv
source .venv/bin/activate
```

```
# pip install git+https://github.com/meta-llama/llama-stack-client-python.git
pip install llama-stack-client
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

```
ollama ps
```

```
NAME                         ID              SIZE      PROCESSOR    UNTIL
llama3.2:3b-instruct-fp16    195a8c01d91e    8.6 GB    100% GPU     59 minutes from now
llama-guard3:8b-q4_0         d8d7fb8dfa56    6.7 GB    100% GPU     59 minutes from now
llama3.1:8b-instruct-fp16    4aacac419454    17 GB     100% GPU     59 minutes from now
```

If the model is not alive on ollama, you will get failures.  Llama Stack server startup looks for the already running ollama models.  

You MAY need to shut-down any previously running Llama Stack server

```
docker ps
```

note: your container id will be different

```
docker stop fc3eae32f44c
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

```
Shield(
│   identifier='content_safety',
│   provider_id='llama-guard',
│   provider_resource_id='Llama-Guard-3-8B',
│   type='shield',
│   params={}
)
```

Now an agent + shield

```
python 6-agent-shield.py
```

Two of the four messages will cause violations

The violation codes

https://github.com/meta-llama/llama-stack/blob/main/llama_stack/providers/inline/safety/llama_guard/llama_guard.py#L54


### MCP Servers

The file system MCP server is one of the easiest, get it up and running in a terminal.


New terminal to run the MCP server process

```
cd mcp-servers/node-mcp-server-math
```

See its readme.md

```
npx -y supergateway --port 8002 --stdio "node index.mjs"
```


Register the toolgroup

Note: if the MCP server is not up/on, the registration will often fail with a 500 error.

```
curl -X POST -H "Content-Type: application/json" --data '{ "provider_id" : "model-context-protocol", "toolgroup_id" : "mcp::my-node-server-math", "mcp_endpoint" : { "uri" : "http://host.docker.internal:8002/sse"}}' http://localhost:8321/v1/toolgroups
```

See if it is registered

```
python providers-tools-list.py
```


```
python 7-mcp-client-node-server.py
```

```
In this response, I used the function `add` to add 2 and 2. The result is 4.
```


Go for a 2nd MCP Server

```
cd mcp-servers/node-mcp-server-other
```

review readme.md to startup

```
curl -X POST -H "Content-Type: application/json" --data '{ "provider_id" : "model-context-protocol", "toolgroup_id" : "mcp::my-node-server-other", "mcp_endpoint" : { "uri" : "http://host.docker.internal:8004/sse"}}' http://localhost:8321/v1/toolgroups
```

```
python 7-mcp-client-node-server-other.py
```

```
inference> {"function": "fetch_customer_details", "parameters": {"customer_id": "C100"}}<|python_tag|>{"function": "fetch_customer_details", "parameters": {"customer_id": "C100"}}
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

## Vision

VLM use cases - image to text:
- how many objects in an image
- what is the total amount on an invoice
- hand-writing recognition
- generating marketing copy for a new product

```
ollama run llama3.2-vision:11b --keepalive 60m
```
Uses about 12GB of VRAM (or unified RAM Mac M1,3,4)

```
model = client.models.register(    
    model_id="meta-llama/Llama-3.2-vision-11B",
    model_type="llm",
    provider_id="ollama",
    provider_model_id="llama3.2-vision:11b",
    metadata={"description": "llama3.2-vision:11b via ollama"}
)
```

### Describe an image

```
export LLAMA_STACK_VISION_MODEL="meta-llama/Llama-3.2-vision-11B"
# OR
export LLAMA_STACK_VISION_MODEL="ibm/Granite-3.2-vision-2B"
```

```
python 8-chat-completions-vision-1.py
```

### How many dogs

```
python 8-chat-completions-vision-2.py
```

### Invoice Total and customer address

```
python 8-chat-completions-vision-3.py
```

### Patient Intake: Hand-writing

```
python 8-chat-completions-vision-4.py
```

### Marketing copy creation

```
python 8-chat-completions-vision-5.py
```

### Qwen2.5-VL-7B-Instruct

https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct



## Library Mode

Using Llama Stack as an embedded library/framework instead of a remote API server.

Still using ollama 

https://llama-stack.readthedocs.io/en/latest/distributions/importing_as_library.html

```
python3.11 -m venv .venv
```

```
source .venv/bin/activate
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

### Streamlit GUI

```
cd streamlit-chat-gui
```

review readme.md 

![Streamlit GUI](streamlit-chat-gui/streamlit-chat-ui.png)

## Playground

https://llama-stack.readthedocs.io/en/latest/playground/index.html

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

Check out the README.md in that directory for more ideass


## ToDos

podman 
If I run llama-stack in podman, I use this as the address of my mcp-server:  http://host.containers.internal:8000/sse

get weather via agent API and decorator 7

MCP server with sqlite database

https://github.com/meta-llama/llama-stack/tree/main/docs/zero_to_hero_guide

Shields output

https://github.com/meta-llama/llama-stack/pull/1419

https://llama-stack.readthedocs.io/en/latest/building_applications/rag.html
versus
https://github.com/burrsutter/python-plain-agentic-examples/tree/main/rag

Working Tavily+Agent

Working Brave+Agent

PatternFly Chatbot
https://github.com/patternfly/chatbot

More MCP examples
https://towardsdatascience.com/clear-intro-to-mcp/


https://redhat-internal.slack.com/archives/C08CD63RDLG/p1743181170314839

https://github.com/meta-llama/llama-stack/pull/1354

## Clean Docker/Podman

```
docker kill $(docker ps -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q)
docker system prune -a --volumes
```

```
podman kill $(podman ps -q)
podman rm $(podman ps -a -q)
podman rmi $(podman images -q)
podman system prune -a --volumes
```