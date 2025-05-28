import os
import sys
from llama_stack_client import LlamaStackClient
from llama_stack_client.types import VersionInfo

client = LlamaStackClient(
  base_url=f"{os.environ['LLAMA_STACK_SERVER']}"
)

# Print client version
print(f"Client Version: {client._version}")

# Print server version
print(f"Server Version: {client.inspect.version().version}")


print("--- Haiku ---")

response = client.inference.chat_completion(
    model_id=os.environ["INFERENCE_MODEL"],
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a haiku about coding"},
    ],
)

print(response.completion_message.content)