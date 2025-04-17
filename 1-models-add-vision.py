import os


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

from llama_stack_client import LlamaStackClient
client = LlamaStackClient(base_url=LLAMA_STACK_SERVER)

# from llama_stack import LlamaStackAsLibraryClient
# client = LlamaStackAsLibraryClient("ollama")
# client.initialize()

# Make sure to `ollama run llama3.2-vision:11b --keepalive 60m`

# Register a model
model = client.models.register(    
    model_id="meta-llama/Llama-3.2-vision-11B",
    model_type="llm",
    provider_id="ollama",
    provider_model_id="llama3.2-vision:11b",
    metadata={"description": "llama3.2-vision:11b via ollama"}
)