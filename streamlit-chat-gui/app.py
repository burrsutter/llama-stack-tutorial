import streamlit as st
from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.types.agent_create_params import AgentConfig
import os

from dotenv import load_dotenv
import logging

load_dotenv()

LLAMA_STACK_SERVER=os.getenv("LLAMA_STACK_SERVER")
LLAMA_STACK_MODEL=os.getenv("LLAMA_STACK_MODEL")

print(LLAMA_STACK_SERVER)
print(LLAMA_STACK_MODEL)

from llama_stack_client import LlamaStackClient
client = LlamaStackClient(
    base_url=LLAMA_STACK_SERVER
)


# Streamlit UI
st.title("Llama-stack MCP server demo")
st.markdown("Query an orders system using MCP and Llama-stack")
# enquiry = st.sidebar.text_area("Ask a question", "Addition")
# Chat history management if not initialized
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for new messages
prompt = st.chat_input("Ask something...")
if prompt:
    full_response = ""
    agent_config = AgentConfig(
        model=LLAMA_STACK_MODEL,
        instructions="You are a helpful assistant",
        sampling_params={
            "strategy": {"type": "top_p", "temperature": 1.0, "top_p": 0.9},
        },
        toolgroups=(
            [
                "mcp::my-python-server-math"
            ]
        ),
        tool_choice="auto",
        input_shields=[],
        output_shields=[],
        enable_session_persistence=True,
    )
    agent = Agent(client, agent_config)
    session_id = agent.create_session("test-session")
    # Add user input to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from LlamaStack API
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = agent.create_turn(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            session_id=session_id,
        )
     
        for chunk in response:
            print(chunk)
            if chunk.event.payload.event_type == "step_progress":
                if chunk.event.payload.delta.type == "text":
                    full_response += chunk.event.payload.delta.text
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
    
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    