from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.types.agent_create_params import AgentConfig
from llama_stack_client.lib.agents.event_logger import EventLogger
from llama_stack_client import LlamaStackClient

client = LlamaStackClient(
    base_url=f"http://localhost:8321"
)

agent = Agent(
    client,
    model="meta-llama/Llama-3.2-3B-Instruct",
    instructions=(
        "You are a web search assistant, must use websearch tool to look up the most current and precise information available. "
    ),
    tools=["builtin::websearch"],
)

session_id = agent.create_session("websearch-session")

query = "Who won the 2025 Super Bowl?"
# query = "Who won the 2025 UCL Final?"
# query = "How did the USA perform in the last Olympics?"

response = agent.create_turn(
    messages=[
        {"role": "user", "content": query}
    ],
    session_id=session_id,
)
for log in EventLogger().log(response):
    log.print()