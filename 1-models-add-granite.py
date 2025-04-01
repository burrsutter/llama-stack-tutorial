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


# Make sure to `ollama run granite3.2:2b-instruct-fp16 --keepalive 60m`

# Register a model
model = client.models.register(
    model_id="ibm/Granite-3.2-2B-Instruct",    
    model_type="llm",
    provider_id="ollama",
    provider_model_id="granite3.2:2b-instruct-fp16",
    metadata={"description": "granite3.2:2b-instruct-fp16 via ollama"}
)