import os


from llama_stack_client import LlamaStackClient
client = LlamaStackClient(base_url=os.getenv("LLAMA_STACK_SERVER"))

# from llama_stack import LlamaStackAsLibraryClient
# client = LlamaStackAsLibraryClient("ollama")
# client.initialize()


# List available models
models = client.models.list()
print("--- Available models: ---")
for m in models:
    print(f"{m.identifier} - {m.provider_id} - {m.provider_resource_id}")
print()