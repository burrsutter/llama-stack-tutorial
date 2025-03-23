import os
from uuid import uuid4
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.agents.event_logger import EventLogger as AgentEventLogger

LLAMA_STACK_SERVER=os.getenv("LLAMA_STACK_SERVER")
LLAMA_STACK_MODEL=os.getenv("LLAMA_STACK_MODEL")

print(LLAMA_STACK_SERVER)
print(LLAMA_STACK_MODEL)

client = LlamaStackClient(base_url=os.getenv("LLAMA_STACK_SERVER"))

agent = Agent(
    client,
    model=LLAMA_STACK_MODEL,  # or another valid model identifier
    instructions="You are a helpful assistant.",  # system prompt instructions for the agent
    enable_session_persistence=False
)

session_id = agent.create_session(f"test-session-{uuid4()}")

response = agent.create_turn(
    messages=[
        {
            "role": "user",
            "content": "Give me a sentence that contains the word: hello",
        }
    ],
    session_id=session_id,
)

print(f"response: {response}")
print()
print()
for log in AgentEventLogger().log(response):
    log.print()
