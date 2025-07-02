import os
from dotenv import load_dotenv
from uuid import uuid4
import logging
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.lib.agents.event_logger import EventLogger as AgentEventLogger
from llama_stack_client import LlamaStackClient

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


client = LlamaStackClient(
    base_url=LLAMA_STACK_SERVER
)

# System prompt configures the assistant behavior
sys_prompt = "You are a helpful assistant with access to the math tool. Use the math tool to answer questions."


agent = Agent(
    client,
    model=LLAMA_STACK_MODEL,
    instructions=sys_prompt,
    enable_session_persistence=False,
    tools=["mcp::my-python-mcp-server-math"]
)

user_prompt = "What's 2+2?"

session_id = agent.create_session(f"test-session-{uuid4()}")


response = agent.create_turn(
    messages=[
        {
        "role": "user",
        "content": user_prompt
        }
    ],
    session_id=session_id,
    stream=True,
)

print(f"Response: {response}")
print()
print()
for log in AgentEventLogger().log(response):
    log.print()
