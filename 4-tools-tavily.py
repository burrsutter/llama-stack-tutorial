import os
import json
from llama_stack_client import LlamaStackClient
from rich.pretty import pprint
from dotenv import load_dotenv
import logging

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

LLAMA_STACK_SERVER=os.getenv("LLAMA_STACK_SERVER")
LLAMA_STACK_MODEL=os.getenv("LLAMA_STACK_MODEL")
TAVILY_SEARCH_API_KEY=os.getenv("TAVILY_SEARCH_API_KEY")

print(LLAMA_STACK_SERVER)
print(LLAMA_STACK_MODEL)

search_query="Who won the last Super Bowl?"

client = LlamaStackClient(
    base_url=os.getenv("LLAMA_STACK_SERVER"),
    provider_data={"tavily_search_api_key":TAVILY_SEARCH_API_KEY}
)

# client.toolgroups.unregister(
#     toolgroup_id="builtin::websearch"
# )

# client.toolgroups.register(
#     toolgroup_id="builtin::websearch",
#     provider_id="tavily-search",
#     args={"max_results": 10},
# )

for toolgroup in client.toolgroups.list():
    pprint(toolgroup)


response = client.tool_runtime.invoke_tool(
    tool_name="tavily-search", kwargs={"query": search_query}
)

web_search_results = json.loads(response.content)
print()
# print(web_search_results)
for item in web_search_results["top_k"]:
    print(item["url"])
    print(item["content"])

llm_response_no_context = client.inference.chat_completion(
    model_id=LLAMA_STACK_MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": search_query},
    ],
)
print()
print(llm_response_no_context.completion_message.content)

llm_response_with_context = client.inference.chat_completion(
    model_id=LLAMA_STACK_MODEL,
    messages=[
        {"role": "system", "content": f"Use the following context and only the following context to answer the user question, if the context does not contain the answer, respond with 'I could not find the answer': {web_search_results}"},
        {"role": "user", "content": search_query},
    ],
)
print()
print(llm_response_with_context.completion_message.content)