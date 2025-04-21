from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ValidationError
import os
import json
load_dotenv()

API_KEY=os.getenv("API_KEY")
INFERENCE_SERVER_URL=os.getenv("INFERENCE_SERVER_URL")
MODEL_NAME=os.getenv("MODEL_NAME")

client = OpenAI(
    api_key=API_KEY,
    base_url=INFERENCE_SERVER_URL
    )


print(INFERENCE_SERVER_URL)
print(MODEL_NAME)


class AnalyzedEmail(BaseModel):
    reason: str
    sentiment: str
    customer_name: str
    email_address: str
    product_name: str
    escalate: bool

schema_dict = AnalyzedEmail.model_json_schema()
schema_json = json.dumps(schema_dict, indent=2)

sys_prompt=f"""
Extract the support email information. Please output ONLY a JSON object (no extra text)
that exactly matches this JSON Schema:

{schema_json}

""" 


raw_response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[
        {"role": "system", "content": sys_prompt},
        {
            "role": "user",
            # "content": "Hello, I purchased a TechGear Pro Laptop, but I can't find the invoice in my email. Sincerely, David Jones david@example.org",
            "content": "Hello, I purchased a TechGear Pro Laptop, but I can't find the invoice in my email and I need it immediately for tax purposes. Sincerely, David Jones david@example.org",
            "content": "I purchased a TechGear Pro Laptop from you and the damn thing won't boot up, my project deadline is near. David david@example.org",
        },
    ],
    temperature=0.0    
)

# Print detailed information about the response
print("Response type:", type(raw_response))
print("Response attributes:", dir(raw_response))
print("Choices:", raw_response.choices)
print("Raw response content:")
content = raw_response.choices[0].message.content
print(content)
print("Content type:", type(content))
print("Content length:", len(content))
print("-----------------")

# Parse and validate the JSON response
try:
    # Check if the content is empty
    if not content.strip():
        print("Error: Empty response content")
        exit(1)
        
    # Try to parse the JSON
    response_data = json.loads(content.strip())
    print("Parsed JSON:", response_data)
    
    # Validate with Pydantic
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

except json.JSONDecodeError as e:
    print(f"JSON parsing error: {e}")
    print("Raw content that failed to parse:")
    print(content)
except ValidationError as e:
    print(f"Pydantic validation error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
    print("Raw content:")
    print(content)