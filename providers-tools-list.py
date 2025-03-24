import os
import json
from llama_stack_client import LlamaStackClient
from rich.pretty import pprint
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

logger.info(LLAMA_STACK_SERVER)
logger.info(LLAMA_STACK_MODEL)

client = LlamaStackClient(
    base_url=os.getenv("LLAMA_STACK_SERVER")
)


# List all available providers
providers = client.providers.list()
logger.info("Available providers:")
for provider in providers:
    logger.info(f"- {provider.provider_id} (type: {provider.provider_type})")

# List all available tools
tools = client.tools.list()
logger.info("\nAvailable tools:")
for tool in tools:
    logger.info(f"- {tool.identifier} (provider: {tool.provider_id})")