import os
from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.agents.client_tool import client_tool
from llama_stack_client.types import CompletionMessage
import requests
import logging
import json

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

@client_tool
def get_weather(latitude: float, longitude: float) -> dict:
    """gets the current weather 
    
    :param latitude: latitude of city
    :param longitude: longitude of city
    :returns: Dictionary containing the temperature and wind speed
    """
    
    logger.info("get_weather Tool invoked with latitude " + latitude + " and logitude " + longitude)
    # https://api.open-meteo.com/v1/forecast?latitude=33.749&longitude=-84.388&current=temperature_2m
    response = requests.get(
        # celsius, metric 
        # f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
        # fahrenheit, imperial
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m&temperature_unit=fahrenheit&wind_speed_unit=mph"
    )
    data = response.json()
    logger.info(data)
    return data["current"]


# --------------------------------------------------------------
# Step 3: Call the model with the tool
# --------------------------------------------------------------

system_prompt = "You are a helpful weather assistant."

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "What is the temperature in Atlanta today?"},
]


# tools = [get_weather.get_tool_definition()]

# something is not right with .get_tool_definition()
# if not isinstance(tools[0], dict):
#     raise ValueError("Tool definition must be a dictionary!")

# logger.debug("Tool definition BEFORE: %s", json.dumps(tools[0], indent=4))

# def replace_name_with_tool_name(tools):
#     if isinstance(tools, dict):
#         return {("tool_name" if k == "name" else k): replace_name_with_tool_name(v) for k, v in tools.items()}
#     elif isinstance(tools, list):
#         return [replace_name_with_tool_name(item) for item in tools]
#     else:
#         return tools

# tools = replace_name_with_tool_name(tools)

# logger.debug("Tool definition AFTER: %s", json.dumps(tools[0], indent=4))

tools = [
    {
        "tool_name": "get_weather",        
        "description": "Get current temperature for provided coordinates in celsius.",
        "parameters": {            
            "latitude": {
                "param_type": "float",
                "description": "latitude of city"
            },
            "longitude": {
                "param_type": "float",
                "description": "longitude of city"
            }
        }
    }
]



response = client.inference.chat_completion(
    model_id=LLAMA_STACK_MODEL,
    messages=messages,
    tools=tools,
    tool_prompt_format="python_list",    
    tool_choice="auto"
)

logger.info(response.completion_message.content)


# --------------------------------------------------------------
# Step 4: Debugging output
# --------------------------------------------------------------

logger.info(type(response.completion_message))
logger.info(response.completion_message)

logger.info("Tools to be invoked?")
logger.info(response.completion_message.tool_calls)


# for debugging what is in messages
def log_messages(messages):
    logger.info("********************")
    logger.info(f"Total messages: {len(messages)}")

    for i, message in enumerate(messages):
            logger.info(f"Message {i + 1} - Type: {type(message)}")

            # If the message is a dictionary, print it nicely
            if isinstance(message, dict):
                logger.info(json.dumps(message, indent=4))  # Pretty print JSON
                
            # If it's a list, iterate over its items and print them
            elif isinstance(message, list):
                logger.info(f"List with {len(message)} items:")
                for j, item in enumerate(message):
                    logger.info(f"  Item {j + 1}: {item}")

            # If it's a CompletionMessage, extract useful attributes
            elif isinstance(message, CompletionMessage):                
                logger.info(f"Role: {message.role}")
                logger.info(f"Content: {message.content}")
                if message.tool_calls:
                    logger.info("Tool Calls:")
                    for tool_call in message.tool_calls:
                        logger.info(f"  - Name: {tool_call.tool_name}")
                        logger.info(f"  - Arguments: {tool_call.arguments}")

            # If it's another type, just print it
            else:
                logger.info(f"Unknown type: {message}")

    logger.info("********************")



