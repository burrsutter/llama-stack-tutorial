import os
from llama_stack_client import LlamaStackClient
from llama_stack_client.types import CompletionMessage
import requests
import json
from pydantic import BaseModel, Field

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
    logger.info("get_weather tool invoked")    
    response = requests.get(
        # celsius, metric 
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
        # fahrenheit, imperial
        # f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m&temperature_unit=fahrenheit&wind_speed_unit=mph"
    )
    data = response.json()
    logger.debug(data)
    return data["current"]


# --------------------------------------------------------------
# Step 3: Describe the get_weather tool 
# --------------------------------------------------------------

tool = [
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
    tools=tool,
    tool_prompt_format="python_list",
    tool_choice="auto"
)

# --------------------------------------------------------------
# Step 5: Debugging output
# --------------------------------------------------------------

logger.debug(type(response.completion_message))
logger.debug(response.completion_message)

logger.debug("Tools to be invoked?")
logger.debug(response.completion_message.tool_calls)


# for debugging what is in messages
def log_messages(messages):
    logger.debug("********************")
    logger.debug(f"Total messages: {len(messages)}")

    for i, message in enumerate(messages):
            logger.debug(f"Message {i + 1} - Type: {type(message)}")

            # If the message is a dictionary, print it nicely
            if isinstance(message, dict):
                logger.debug(json.dumps(message, indent=4))  # Pretty print JSON
                
            # If it's a list, iterate over its items and print them
            elif isinstance(message, list):
                logger.debug(f"List with {len(message)} items:")
                for j, item in enumerate(message):
                    logger.debug(f"  Item {j + 1}: {item}")

            # If it's a CompletionMessage, extract useful attributes
            elif isinstance(message, CompletionMessage):                
                logger.debug(f"Role: {message.role}")
                logger.debug(f"Content: {message.content}")
                if message.tool_calls:
                    logger.debug("Tool Calls:")
                    for tool_call in message.tool_calls:
                        logger.debug(f"  - Name: {tool_call.tool_name}")
                        logger.debug(f"  - Arguments: {tool_call.arguments}")

            # If it's another type, just print it
            else:
                logger.debug(f"Unknown type: {message}")

    logger.debug("********************")


# --------------------------------------------------------------
# Step 6: Execute get_weather function callback
# --------------------------------------------------------------


def call_function(name, args):
    if name == "get_weather":
        return get_weather(**args)


if response.completion_message.tool_calls:
    for tool_call in response.completion_message.tool_calls:
        name = tool_call.tool_name
        logger.debug("tool_call %s", tool_call)        
        logger.debug("arguments value %s", tool_call.arguments)
        args = tool_call.arguments
        logger.debug("What? %s", response.completion_message)
        messages.append(response.completion_message)

        result = call_function(name, args)

        messages.append(
            {
                "role": "tool",
                "call_id": tool_call.call_id,  
                "tool_name": tool_call.tool_name,  
                "content": json.dumps(result)
            }
        )
        log_messages(messages)


# --------------------------------------------------------------
# Step 7: Describe result and call model again
# --------------------------------------------------------------

class WeatherResponse(BaseModel):
    temperature: float = Field(
        description="The current temperature in celsius for the given location."
    )
    response: str = Field(
        description="A natural language response to the user's question."
    )


response = client.inference.chat_completion(
    model_id=LLAMA_STACK_MODEL,
    messages=messages,
    tools=tool,
    tool_prompt_format="python_list",
    tool_choice="auto",
    response_format={
       "type": "json_schema",
       "json_schema": WeatherResponse.model_json_schema(),
    }    
)

# --------------------------------------------------------------
# Step 7: Check model response
# --------------------------------------------------------------

# Parse and validate the JSON response
try:
    response_data = json.loads(response.completion_message.content)
    weather = WeatherResponse(**response_data)    
    print("-------")
    print(weather)
    print("-------")
    print("Temperature:   ", weather.temperature)
    print("Description:   ", weather.response)

except (json.JSONDecodeError, ValueError) as e:
    print(f"Invalid format: {e}")