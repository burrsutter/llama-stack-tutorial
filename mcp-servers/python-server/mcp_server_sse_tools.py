from mcp.server.fastmcp import FastMCP
import datetime

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