import os
from llama_stack_client import LlamaStackClient

client = LlamaStackClient(base_url=os.getenv("LLAMA_STACK_SERVER"))

# List available models
models = client.models.list()
print("--- Available models: ---")
for m in models:
    print(f"- {m.identifier}")
print()