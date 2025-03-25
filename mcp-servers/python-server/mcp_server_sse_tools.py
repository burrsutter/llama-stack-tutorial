from mcp.server.fastmcp import FastMCP
import datetime
import random

# Instantiate the MCP server and defines some basic tools
mcp = FastMCP("My Python MCP SSE Server")

@mcp.tool()
def upcase(text: str) -> str:
    """Convert text to uppercase"""
    print(f"upcase: {text}")
    return text.upper()

@mcp.tool()
def weather(text: str) -> str:
    """Mock Weather endpoint"""
    print(f"weather: {text}")
    return "The Canary Islands: 70 degrees F (Mock)"

@mcp.tool()
def generate_random_number(min, max):
    """I can be used to generate a random number between an integer 'min' and an integer 'max'.
    input_value={'max': int, 'min': int}"""
    print(f"generate_random_number: {min} and {max}")
    return random.randint(min, max)    

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    print(f"add: {a} and {b}")
    return a + b

@mcp.tool()
def today() -> str:
    """Today's Date"""
    print(f"Today is coming your way")
    return datetime.date.today().strftime("%B %d, %Y")


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='sse')