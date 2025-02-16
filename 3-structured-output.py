import os
import json
from pydantic import BaseModel
from llama_stack_client import LlamaStackClient

LLAMA_STACK_SERVER=os.getenv("LLAMA_STACK_SERVER")
LLAMA_STACK_MODEL=os.getenv("LLAMA_STACK_MODEL")

print(LLAMA_STACK_SERVER)
print(LLAMA_STACK_MODEL)

client = LlamaStackClient(base_url=os.getenv("LLAMA_STACK_SERVER"))

class AnalyzedEmail(BaseModel):
    reason: str
    sentiment: str
    customer_name: str
    email_address: str
    product_name: str
    escalate: bool

sys_prompt="Extract the support email information." 

response = client.inference.chat_completion(
    model_id=LLAMA_STACK_MODEL,
    messages=[
        {"role": "system", "content": sys_prompt},
        {
            "role": "user",
            "content": "Hello, I purchased a TechGear Pro Laptop, but I can't find the invoice in my email. Sincerely, David Jones david@example.org",
            # "content": "Hello, I purchased a TechGear Pro Laptop, but I can't find the invoice in my email and I need it immediately for tax purposes. Sincerely, David Jones david@example.org",
            # "content": "I purchased a TechGear Pro Laptop from you and the damn thing won't boot up, my project deadline is near. David david@example.org",
        },
    ],
    stream=False,    
    response_format={
            "type": "json_schema",
            "json_schema": AnalyzedEmail.model_json_schema(),
        }
)

# print("-----------------")
# print(response.completion_message.content)
# print("-----------------")

# Parse and validate the JSON response
try:
    response_data = json.loads(response.completion_message.content)
    emailanalysis = AnalyzedEmail(**response_data)    
    print("-------")
    print(emailanalysis)
    print("-------")
    print("Reason:   ", emailanalysis.reason)
    print("Customer: ", emailanalysis.customer_name)
    print("Email:    ", emailanalysis.email_address)
    print("Product:  ", emailanalysis.product_name)
    print("Sentiment:", emailanalysis.sentiment)
    print("Escalate: ", emailanalysis.escalate)

except (json.JSONDecodeError, ValueError) as e:
    print(f"Invalid format: {e}")