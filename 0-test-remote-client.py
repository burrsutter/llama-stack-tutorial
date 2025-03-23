import os
import sys
from llama_stack_client import LlamaStackClient
# from llama_stack import LlamaStackAsLibraryClient

client = LlamaStackClient(
  base_url=f"{os.environ['LLAMA_STACK_SERVER']}"
)

print("--- Haiku ---")

response = client.inference.chat_completion(
    model_id=os.environ["INFERENCE_MODEL"],
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a haiku about coding"},
    ],
)

print(response.completion_message.content)