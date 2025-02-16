import os
from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.agents.client_tool import client_tool
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

response = client.inference.chat_completion(
    model_id=LLAMA_STACK_MODEL,
    messages=messages,
    tools=[get_weather.get_tool_definition()],
    tool_prompt_format="python_list",    
    tool_choice="auto"
)

logger.info(response.completion_message.content)
