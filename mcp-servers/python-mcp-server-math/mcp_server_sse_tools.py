from mcp.server.fastmcp import FastMCP
import datetime

# Instantiate the MCP server and defines some basic tools
mcp = FastMCP("My Python MCP SSE Server")

# @mcp.tool()
# def upcase(text: str) -> str:
#     """Convert text to uppercase"""
#     print(f"upcase: {text}")
#     return text.upper()

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    print(f"add: {a} and {b}")
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers."""
    print(f"subtract: {a} and {b}")
    return a - b


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='sse')