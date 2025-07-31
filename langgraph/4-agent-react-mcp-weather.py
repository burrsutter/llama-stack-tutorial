from langgraph.graph import StateGraph, END, START
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

import os
from dotenv import load_dotenv
load_dotenv()

INFERENCE_SERVER_OPENAI = os.getenv("LLAMA_STACK_ENDPOINT_OPENAI")
INFERENCE_MODEL=os.getenv("INFERENCE_MODEL")
API_KEY=os.getenv("OPENAI_API_KEY", "not applicable")


print("INFERENCE_SERVER_OPENAI: ", INFERENCE_SERVER_OPENAI)
print("INFERENCE_MODEL: ", INFERENCE_MODEL)
print("API_KEY: ", API_KEY)


llm = ChatOpenAI(
    model=INFERENCE_MODEL,
    openai_api_key=API_KEY,  
    openai_api_base=INFERENCE_SERVER_OPENAI,
    use_responses_api=True
)

# Proof of connectivity
print(llm.invoke("Hello"))

# llm_with_tools = llm.bind_tools(
#     [          
#         {
#             "type": "mcp",
#             "server_label": "weather",     
#             "server_url": "http://localhost:3001/sse",       
#             "require_approval": "never",
#         },
#     ])

# llm_with_tools = llm.bind_tools(
#     [          
#         {
#             "type": "mcp",
#             "server_label": "weather"
#         },
#     ])

llm_with_tools = llm.bind_tools([{"type": "mcp::weather"}])



class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])
    #print(message)
    return {"messages": [message]}

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

response = graph.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in Seattle?"}]})

for m in response['messages']:
    m.pretty_print() 





