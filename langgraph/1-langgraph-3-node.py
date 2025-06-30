from langgraph.graph import StateGraph, END

# Define the state (can be any dict-like structure)
class HelloWorldState(dict):
    pass

# Define node functions
def greet_node(state):
    print("👋 Hello from LangGraph!")
    return state

def middle_node(state):
    print("🔄 This is the middle node.")
    return state

def farewell_node(state):
    print("👋 Goodbye from LangGraph!")
    return state

# Build the graph
builder = StateGraph(HelloWorldState)

# Add nodes
builder.add_node("greet", greet_node)
builder.add_node("farewell", farewell_node)
builder.add_node("middle", middle_node)

# Set edges
builder.set_entry_point("greet")
builder.add_edge("greet", "middle")
builder.add_edge("middle", "farewell")
builder.add_edge("farewell", END)

# Compile and run the graph
graph = builder.compile()
graph.invoke(HelloWorldState())