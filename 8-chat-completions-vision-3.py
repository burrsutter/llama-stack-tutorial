import os
from llama_stack_client import LlamaStackClient
from dotenv import load_dotenv
import logging
import base64

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# Model: meta-llama/Llama-3.2-vision-11B
# ollama run llama3.2-vision:11b --keepalive 60m

LLAMA_STACK_SERVER=os.getenv("LLAMA_STACK_SERVER")
LLAMA_STACK_VISION_MODEL=os.getenv("LLAMA_STACK_VISION_MODEL")

IMAGE_TO_ANALYZE="images/invoice-1.jpg"

logger.info(LLAMA_STACK_SERVER)
logger.info(LLAMA_STACK_VISION_MODEL)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode("utf-8")        
        return base64_string

client = LlamaStackClient(base_url=os.getenv("LLAMA_STACK_SERVER"))

response = client.inference.chat_completion(
    model_id=LLAMA_STACK_VISION_MODEL,
    messages=[
        # {"role": "system", "content": "You are an expert image analyzer"},
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": {
                        "data": encode_image(IMAGE_TO_ANALYZE)
                    }
                },
                {
                    "type": "text",
                    "text": "what is the total amount, only the total",
                }
            ]
        }
    ],    
    # temperature=0.0, 
)

print(response.completion_message.content)

response = client.inference.chat_completion(
    model_id=LLAMA_STACK_VISION_MODEL,
    messages=[
        # {"role": "system", "content": "You are an expert image analyzer"},
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": {
                        "data": encode_image(IMAGE_TO_ANALYZE)
                    }
                },
                {
                    "type": "text",
                    "text": "what is customer's address",
                }
            ]
        }
    ],    
    # temperature=0.0, 
)

print(response.completion_message.content)