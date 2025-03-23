import os
import json
from llama_stack_client import LlamaStackClient
from rich.pretty import pprint
from dotenv import load_dotenv
import logging

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
    base_url=os.getenv("LLAMA_STACK_SERVER")
)


for toolgroup in client.toolgroups.list():
    pprint(toolgroup)
