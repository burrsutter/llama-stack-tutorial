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

models = client.models.list()
logger.info("--- Available models: ---")
for m in models:
    logger.info(f"{m.identifier}")

logger.info("Now let's try to unregister one of these")

# Unregister a model
model = client.models.unregister(
    model_id="meta-llama/Llama3.1:8B-Instruct"
)