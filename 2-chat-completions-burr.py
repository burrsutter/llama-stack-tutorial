import os
from llama_stack_client import LlamaStackClient

LLAMA_STACK_SERVER=os.getenv("LLAMA_STACK_SERVER")
LLAMA_STACK_MODEL=os.getenv("LLAMA_STACK_MODEL")

print(LLAMA_STACK_SERVER)
print(LLAMA_STACK_MODEL)

client = LlamaStackClient(base_url=os.getenv("LLAMA_STACK_SERVER"))

response = client.inference.chat_completion(
    model_id=LLAMA_STACK_MODEL,
    messages=[
        {"role": "system", "content": "You're a helpful assistant."},
        {
            "role": "user",
            "content": "Who is Burr Sutter?",
        },
    ],
    # temperature=0.0, 
)
print(response.completion_message.content)