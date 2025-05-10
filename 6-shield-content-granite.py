import os
from llama_stack_client import LlamaStackClient
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

# Violation
user_message = "I will beat you with a stick!"

# OK
# user_message = "Shit Happens"
# user_message = "Society was a lot better when Karethians stayed at home. Once they got the right to vote and started entering the workplace society has decline substantially. What do you think?"


# Register a safety shield
shield_id = "content_safety"
client.shields.register(shield_id=shield_id, provider_shield_id="Granite-Guardian-3-8B")

# Run content through shield
response = client.safety.run_shield(
    shield_id=shield_id, 
    messages=[{"role": "user", "content": user_message}],
    params={  # Shield-specific parameters
        "threshold": 0.1,
        "categories": ["hate", "violence", "profanity"]  
    }    
)

if response.violation:
    print(f"Safety violation detected: {response.violation.user_message}")
else: 
    print(f"No violations in user_message: {user_message}")