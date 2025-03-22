import os
import sys
from llama_stack_client import LlamaStackClient
from llama_stack import LlamaStackAsLibraryClient

# --------------------------------------------------------------
# This code looks for LLAMA_STACK_PORT and INFERENCE_MODEL
# --------------------------------------------------------------

def create_http_client():
    
    return LlamaStackClient(
        base_url=f"http://localhost:{os.environ['LLAMA_STACK_PORT']}"
    )


def create_library_client(template="ollama"):
    
    client = LlamaStackAsLibraryClient(template)
    if not client.initialize():
        print("llama stack not built properly")
        sys.exit(1)
    return client


client = (
    create_library_client()
)  # or create_http_client() depending on the environment you picked

print("--- Haiku ---")

response = client.inference.chat_completion(
    model_id=os.environ["INFERENCE_MODEL"],
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a haiku about coding"},
    ],
)

print(response.completion_message.content)