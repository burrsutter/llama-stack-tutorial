import os
from uuid import uuid4
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.agents.event_logger import EventLogger as AgentEventLogger

from dotenv import load_dotenv
import logging

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

LLAMA_STACK_SERVER=os.getenv("LLAMA_STACK_SERVER")
LLAMA_STACK_MODEL=os.getenv("LLAMA_STACK_MODEL")
TAVILY_SEARCH_API_KEY=os.getenv("TAVILY_SEARCH_API_KEY")

print(LLAMA_STACK_SERVER)
print(LLAMA_STACK_MODEL)

client = LlamaStackClient(
    base_url=os.getenv("LLAMA_STACK_SERVER"),
    provider_data={"tavily_search_api_key":TAVILY_SEARCH_API_KEY}
)

agent = Agent(
    client,
    model=LLAMA_STACK_MODEL,  # or another valid model identifier
    instructions="You are a helpful assistant.",  # system prompt instructions for the agent
    tools=[
        "tavily-search::web_search",
    ],
    enable_session_persistence=False
)

session_id = agent.create_session(f"test-session-{uuid4()}")

response = agent.create_turn(
    messages=[
        {
            "role": "user",
            "content": "Search the web and and tell me who won the last Super Bowl?",
        }
    ],
    session_id=session_id,
)

print(f"response: {response}")
print()
print()
for log in AgentEventLogger().log(response):
    log.print()
