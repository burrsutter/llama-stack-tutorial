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

try:
    client.toolgroups.register(
        toolgroup_id="mcp::weather",
        provider_id="model-context-protocol",
        mcp_endpoint=URL(uri="http://localhost:3001/sse")
    )
    logger.info("Successfully registered mcp::weather toolgroup.")
except Exception as e:
    logger.error("Failed to register mcp::weather toolgroup", exc_info=True)
    # Optionally transform the error into a custom exception:
    raise RuntimeError("Could not set up mcp::weather toolgroup") from e