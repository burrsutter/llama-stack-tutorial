import os
from llama_stack_client import LlamaStackClient

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

client = LlamaStackClient(base_url=LLAMA_STACK_SERVER)

# Make sure to `ollama run llama3.1:8b-instruct-fp16 --keepalive 60m`

# Register a model
model = client.models.register(
    model_id="meta-llama/Llama-Guard-3-8B",
    model_type="llm",
    provider_id="ollama",
    provider_model_id="llama-guard3:8b-q4_0",
    metadata={"description": "llama-guard3:8b-q4_0 via ollama"}
)