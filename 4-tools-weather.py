import os
from llama_stack_client import LlamaStackClient
import requests
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

# https://llama-stack.readthedocs.io/en/latest/building_applications/tools.html

logger.info(LLAMA_STACK_SERVER)
logger.info(LLAMA_STACK_MODEL)

# --------------------------------------------------------------
# Step 1: Create client
# --------------------------------------------------------------


client = LlamaStackClient(base_url=os.getenv("LLAMA_STACK_SERVER"))

# --------------------------------------------------------------
# Step 2: Define the tool (function) that we want to call
# --------------------------------------------------------------

def get_weather(latitude, longitude):
    """This is a publically available API that returns the weather for a given location."""
    logger.info("get_weather Tool invoked")    
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    data = response.json()
    return data["current"]


# --------------------------------------------------------------
# Step 3: Describe the get_weather tool 
# --------------------------------------------------------------

tools = [
    {
        "tool_name": "get_weather",        
        "name": "get_weather",
        "description": "Get current temperature for provided coordinates in celsius.",
        "parameters": {            
            "latitude": {
                "param_type": "number",                
                "description": "latitude of city",
            },
            "longitude": {
                "param_type": "number"},
                "description": "longitude of city",
        },
    }
]

# --------------------------------------------------------------
# Step 4: Call the model with the tool
# --------------------------------------------------------------


system_prompt = "You are a helpful weather assistant."

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "What is the temperature in Atlanta today?"},
]

response = client.inference.chat_completion(
    model_id=LLAMA_STACK_MODEL,
    messages=messages,
    tools=tools,
    tool_prompt_format="python_list",
    tool_choice="auto"
)

logger.info(response.completion_message.content)
