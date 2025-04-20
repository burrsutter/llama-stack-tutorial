
# pip install openai
# pip install dotenv

# as of 0.2.2, Llama Stack now supports an OpenAI compatible API

import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

load_dotenv()

API_KEY = os.getenv("API_KEY")
INFERENCE_SERVER_URL = os.getenv("INFERENCE_SERVER_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

client = OpenAI(
    api_key=API_KEY,
    base_url=INFERENCE_SERVER_URL,
    )

logger.info(INFERENCE_SERVER_URL)
logger.info(MODEL_NAME)



completion_1 = client.chat.completions.create(
    model=os.getenv("MODEL_NAME"),
    messages=[
        {"role": "system", "content": "You're a helpful assistant."},
        {
            "role": "user",
            "content": "What is the temperature in Atlanta today?",
        },
    ],
    temperature=0.0, 
)

response = completion_1.choices[0].message.content

logger.info(response)