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

# Proof of connectivity
print(llm.invoke("Hello"))

llm_with_tools = llm.bind_tools(
    [          
        {
            "type": "mcp",
            "server_label": "my-python-mcp-server-math",            
            "require_approval": "never",
        },
    ])


# # --- Node that runs the agent ---
# def agent_node(state):
#     messages = state["messages"]
#     response = llm.invoke(messages)
#     return {
#         "messages": messages + [response],
#         "intermediate_step": response
#     }

# # --- Tool execution step ---
# def tool_node(state):
#     tool_calls = state["intermediate_step"].tool_calls
#     messages = state["messages"]

#     for tool_call in tool_calls:
#         tool_name = tool_call["name"]
#         args = tool_call["args"]

#         if tool_name == "get_weather_by_location":
#             result = get_weather_by_location.invoke(args)
#         else:
#             result = f"Unknown tool: {tool_name}"

#         messages.append(ToolMessage(tool_call_id=tool_call["id"], content=result))

#     return {"messages": messages}

# # --- Conditional logic to stop or continue ---
# def should_continue(state):
#     tool_calls = state.get("intermediate_step", {}).tool_calls
#     if tool_calls and len(tool_calls) > 0:
#         return "tool"
#     else:
#         return END

# # --- Build LangGraph ---
# builder = StateGraph(dict)
# builder.add_node("agent", agent_node)
# builder.add_node("tool", tool_node)
# builder.set_entry_point("agent")

# # Branch based on whether more tools need to run
# builder.add_conditional_edges("agent", should_continue)
# builder.add_edge("tool", "agent")

# graph = builder.compile()

# # --- Run the graph with a weather question ---
# initial_state = {
#     "messages": [
#         HumanMessage(content="What's the weather like in Boston?")
#     ]
# }

# final_state = graph.invoke(initial_state)

# # --- Print conversation ---
# for m in final_state["messages"]:
#     print(f"{m.type.upper()}: {m.content}")