import os
import uuid
from termcolor import cprint

# this might work with 0.1.8 and https://llama-stack.readthedocs.io/en/latest/getting_started/index.html#your-first-rag-agent
# from llama_stack_client import Agent, AgentEventLogger, RAGDocument
# As of March 23, 2025
# pip install git+https://github.com/meta-llama/llama-stack-client-python.git
# pip install llama-stack
# pip install aiosqlite
# pip install ollama
# pip install openai
# pip install datasets
# pip install opentelemetry-instrumentation
# pip install opentelemetry-exporter-otlp
# pip install faiss-cpu
# pip install mcp
# pip install autoevals

from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.lib.agents.event_logger import EventLogger as AgentEventLogger
from llama_stack_client.types.shared_params.document import Document as RAGDocument



def create_library_client(template="ollama"):
    from llama_stack import LlamaStackAsLibraryClient

    client = LlamaStackAsLibraryClient(template)
    client.initialize()
    return client

client = (
    create_library_client()
)  

# Documents to be used for RAG
urls = ["chat.rst", "llama3.rst", "memory_optimizations.rst", "lora_finetune.rst"]
documents = [
    RAGDocument(
        document_id=f"num-{i}",
        content=f"https://raw.githubusercontent.com/pytorch/torchtune/main/docs/source/tutorials/{url}",
        mime_type="text/plain",
        metadata={},
    )
    for i, url in enumerate(urls)
]

vector_providers = [
    provider for provider in client.providers.list() if provider.api == "vector_io"
]
provider_id = vector_providers[0].provider_id  # Use the first available vector provider

# Register a vector database
vector_db_id = f"test-vector-db-{uuid.uuid4().hex}"
client.vector_dbs.register(
    vector_db_id=vector_db_id,
    provider_id=provider_id,
    embedding_model="all-MiniLM-L6-v2",
    embedding_dimension=384,
)

# Insert the documents into the vector database
client.tool_runtime.rag_tool.insert(
    documents=documents,
    vector_db_id=vector_db_id,
    chunk_size_in_tokens=512,
)

rag_agent = Agent(
    client,
    model=os.environ["INFERENCE_MODEL"],
    # Define instructions for the agent ( aka system prompt)
    instructions="You are a helpful assistant",
    enable_session_persistence=False,
    # Define tools available to the agent
    tools=[
        {
            "name": "builtin::rag/knowledge_search",
            "args": {
                "vector_db_ids": [vector_db_id],
            },
        }
    ],
)
session_id = rag_agent.create_session("test-session")

user_prompts = [
    "How to optimize memory usage in torchtune? use the knowledge_search tool to get information.",
]

# Run the agent loop by calling the `create_turn` method
for prompt in user_prompts:
    cprint(f"User> {prompt}", "green")
    response = rag_agent.create_turn(
        messages=[{"role": "user", "content": prompt}],
        session_id=session_id,
    )
    for log in AgentEventLogger().log(response):
        log.print()