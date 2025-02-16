import os
import json
from pydantic import BaseModel
from llama_stack_client import LlamaStackClient

LLAMA_STACK_SERVER=os.getenv("LLAMA_STACK_SERVER")
LLAMA_STACK_MODEL=os.getenv("LLAMA_STACK_MODEL")

print(LLAMA_STACK_SERVER)
print(LLAMA_STACK_MODEL)

client = LlamaStackClient(base_url=os.getenv("LLAMA_STACK_SERVER"))


class LeopardSpeed(BaseModel):
    speed: int


response = client.inference.chat_completion(
    model_id=LLAMA_STACK_MODEL,
    messages=[
        {"role": "system", "content": "You're a helpful assistant."},
        {
            "role": "user",
            "content": "What is the top speed of a leopard in kilometers per hour?",            
        },
    ],
    stream=False,    
    response_format={
            "type": "json_schema",
            "json_schema": LeopardSpeed.model_json_schema(),
        }
)

# print("-----------------")
# print(response.completion_message.content)
# print("-----------------")

# Parse and validate the JSON response
try:
    response_data = json.loads(response.completion_message.content)
    leopard = LeopardSpeed(**response_data)    
    print("-------")
    print("Speed: ", leopard.speed)
    print("-------")
except (json.JSONDecodeError, ValueError) as e:
    print(f"Invalid format: {e}")