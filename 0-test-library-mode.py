import os
import sys
from llama_stack import LlamaStackAsLibraryClient

client = LlamaStackAsLibraryClient("ollama")
if not client.initialize():
   print("llama stack not built properly")
   sys.exit(1)
    
print("--- Haiku ---")

response = client.inference.chat_completion(
    model_id=os.environ["INFERENCE_MODEL"],
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a haiku about coding"},
    ],
)

print(response.completion_message.content)