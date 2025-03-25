import os
# from llama_stack_client import LlamaStackClient
from llama_stack import LlamaStackAsLibraryClient
client = LlamaStackAsLibraryClient("ollama")
client.initialize()

# client = LlamaStackClient(base_url=os.getenv("LLAMA_STACK_SERVER"))

# List available models
models = client.models.list()
print("--- Available models: ---")
for m in models:
    print(f"- {m.identifier}")
print()