import requests
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
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


# --- Weather Tool using api.weather.gov ---
@tool
def get_weather_by_location(lat: float, lon: float) -> str:
    """Get the current forecast from weather.gov given a latitude and longitude."""
    try:
        points_url = f"https://api.weather.gov/points/{lat},{lon}"
        points_resp = requests.get(points_url, timeout=10)
        forecast_url = points_resp.json()["properties"]["forecast"]

        forecast_resp = requests.get(forecast_url, timeout=10)
        forecast = forecast_resp.json()["properties"]["periods"][0]["detailedForecast"]
        return forecast
    except Exception as e:
        return f"Failed to get weather: {str(e)}"

tools = [get_weather_by_location]

# --- LLM that supports function-calling ---
llm = ChatOpenAI(
    model=INFERENCE_MODEL,
    openai_api_key=API_KEY,  
    openai_api_base=INFERENCE_SERVER_OPENAI 
).bind_tools(tools)

# --- Node that runs the agent ---
def agent_node(state):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {
        "messages": messages + [response],
        "intermediate_step": response,
    }

# --- Node that executes tool call ---
def tool_node(state):
    tool_call = state["intermediate_step"].tool_calls[0]
    result = get_weather_by_location.invoke(tool_call["args"])
    return {
        "messages": state["messages"] + [
            ToolMessage(tool_call_id=tool_call["id"], content=str(result))
        ]
    }

# --- Build LangGraph ---
graph = StateGraph(dict)
graph.add_node("agent", agent_node)
graph.add_node("tool", tool_node)

graph.set_entry_point("agent")
graph.add_edge("agent", "tool")
graph.add_edge("tool", END)

compiled_graph = graph.compile()

# --- Run it ---
initial_state = {
    "messages": [HumanMessage(content="What's the weather in Boston, MA?")]
}

final_state = compiled_graph.invoke(initial_state)

# --- Output ---
for msg in final_state["messages"]:
    print(f"{msg.type.upper()}: {msg.content}")