import os
from llama_stack_client import LlamaStackClient

import logging

# setup logger
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

client = LlamaStackClient(base_url=os.getenv("LLAMA_STACK_SERVER"))

response = client.inference.chat_completion(
    model_id=LLAMA_STACK_MODEL,
    messages=[
        {"role": "system", "content": "You're a helpful assistant."},
        {"role": "user", "content": "What is the temperature in Atlanta today?"},
    ],
    # temperature=0.0, 
)
logger.info(response.completion_message.content)