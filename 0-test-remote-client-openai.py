from dotenv import load_dotenv
from openai import OpenAI

import os

load_dotenv()

API_KEY=os.getenv("API_KEY","none")
INFERENCE_SERVER_URL=os.getenv("LLAMA_STACK_SERVER")
MODEL_NAME=os.getenv("INFERENCE_MODEL")

client = OpenAI(
    api_key=API_KEY,
    base_url=f"{INFERENCE_SERVER_URL}/v1/openai/v1",
    )

print(INFERENCE_SERVER_URL)
print(MODEL_NAME)

completion_1 = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[
        {"role": "system", "content": "You're a helpful assistant."},
        {
            "role": "user",
            "content": "What length of the Pont des Arts in meters?",
        },
    ],
    temperature=0.0, 
)

response = completion_1.choices[0].message.content

print(response)


completion_2 = client.chat.completions.create(
    model=MODEL_NAME,    
    messages=[
        {"role": "system", "content": "You're a helpful assistant."},
        {
            "role": "user",
            "content": "What is the top speed of a leopard in kilometers per hour?",
        },
    ],
    temperature=0.0, 
)

response = completion_2.choices[0].message.content

print(response)
