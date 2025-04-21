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

# schema_dict = AnalyzedEmail.model_json_schema()
# schema_json = json.dumps(schema_dict, indent=2)


sys_prompt="Extract the support email information. "


user_message = "Hello, I purchased a TechGear Pro Laptop, but I can't find the invoice in my email. Sincerely, David Jones david@example.org"
# user_message = "Hello, I purchased a TechGear Pro Laptop, but I can't find the invoice in my email and I need it immediately for tax purposes. Sincerely, David Jones david@example.org"
# user_message = "I purchased a TechGear Pro Laptop from you and the damn thing won't boot up, my project deadline is near. David david@example.org"

completion = client.beta.chat.completions.parse(
    model=MODEL_NAME,
    messages=[
        {"role": "system", "content": "Extract the support email information."},
        {
            "role": "user",
            "content": user_message,
        },
    ],
    response_format=AnalyzedEmail,
)

emailanalysis = completion.choices[0].message.parsed

print(emailanalysis)

print("-----------------")

print("-------")
print(emailanalysis)
print("-------")
print("Reason:   ", emailanalysis.reason)
print("Customer: ", emailanalysis.customer_name)
print("Email:    ", emailanalysis.email_address)
print("Product:  ", emailanalysis.product_name)
print("Sentiment:", emailanalysis.sentiment)
print("Escalate: ", emailanalysis.escalate)

