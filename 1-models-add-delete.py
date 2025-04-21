import os
from llama_stack_client import LlamaStackClient

LLAMA_STACK_SERVER=os.getenv("LLAMA_STACK_SERVER")


client = LlamaStackClient(base_url=LLAMA_STACK_SERVER)

model_name="meta-llama/Llama-3.1-8B-Instruct" 

# Register the model
model = client.models.register(
    model_id=model_name,
    model_type="llm",
    provider_id="ollama",
    provider_model_id="llama3.1:8b-instruct-fp16",
    metadata={"description": "llama3.1:8b-instruct-fp16 via ollama"}
)

models = client.models.list()
print("--- Available models: ---")
for m in models:
    print(f"{m.identifier} - {m.provider_id} - {m.provider_resource_id}")
print()

# Unregister the model
model = client.models.unregister(
    model_id=model_name    
)