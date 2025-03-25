import os
from dotenv import load_dotenv
import logging
from uuid import uuid4
from llama_stack.apis.common.content_types import URL
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.lib.agents.event_logger import EventLogger as AgentEventLogger

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

LLAMA_STACK_SERVER=os.getenv("LLAMA_STACK_SERVER")
LLAMA_STACK_MODEL=os.getenv("LLAMA_STACK_MODEL")

print(LLAMA_STACK_SERVER)
print(LLAMA_STACK_MODEL)

from llama_stack_client import LlamaStackClient
client = LlamaStackClient(
    base_url=LLAMA_STACK_SERVER
)

# from llama_stack import LlamaStackAsLibraryClient
# client = LlamaStackAsLibraryClient("ollama")
# client.initialize()


client.toolgroups.register(
    toolgroup_id="mcp::my-node-server",
    provider_id="model-context-protocol",
    mcp_endpoint=URL(uri="http://localhost:3001/sse") 
)

agent = Agent(
    client,
    model=LLAMA_STACK_MODEL,  # or another valid model identifier
    instructions="You are a helpful assistant.",  # system prompt instructions for the agent
    enable_session_persistence=False,
    tools=["mcp::my-node-server"]
)

session_id = agent.create_session(f"test-session-{uuid4()}")

response = agent.create_turn(
    messages=[
        {
            "role": "user",
            "content": "Add 2 and 2",
        }
    ],
    session_id=session_id,
)

print(f"response: {response}")
print()
print()
for log in AgentEventLogger().log(response):
    log.print()
