from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.agents import tool
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage

import os
from dotenv import load_dotenv
load_dotenv()

INFERENCE_SERVER_OPENAI = os.getenv("LLAMA_STACK_ENDPOINT_OPENAI")
INFERENCE_MODEL=os.getenv("INFERENCE_MODEL")
API_KEY=os.getenv("OPENAI_API_KEY", "not applicable")


print("INFERENCE_SERVER_OPENAI: ", INFERENCE_SERVER_OPENAI)
print("INFERENCE_MODEL: ", INFERENCE_MODEL)
print("API_KEY: ", API_KEY)


# --- LLM 
llm = ChatOpenAI(
    model=INFERENCE_MODEL,
    openai_api_key=API_KEY,  
    openai_api_base=INFERENCE_SERVER_OPENAI,
    use_responses_api=True
)

# # Proof of connectivity
# print(llm.invoke("Hello"))

websearch_tool = {
    "name": "web_search",
    "description": "Search the web for a given query.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search string to use"
            }
        },
        "required": ["query"]
    }
}

llm_with_tools = llm.bind_tools([websearch_tool])

response = llm_with_tools.invoke("Who won the 2025 Super Bowl?")
print("Raw response:", response)

# If it's a normal text reply:
if isinstance(response, AIMessage):
    print("Answer:", response.content)


