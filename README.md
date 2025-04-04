# Weather MCP Server with LangChain and SmolAgents

This repository provides a comprehensive tutorial and example implementation of a Model Context Protocol (MCP) server for weather forecasting, along with integration examples for both LangChain and SmolAgents frameworks.

## What is MCP?

The Model Context Protocol (MCP) is an open protocol that standardizes how AI applications provide context to Large Language Models (LLMs). Think of MCP like a USB-C port for AI applications - a standardized way to connect AI models to various data sources and tools.

## Project Structure

- `weather.py` - MCP server implementation that provides weather tools
- `langchain_weather.py` - Example integration with the LangChain framework
- `smolagents_weather.py` - Example integration with the SmolAgents framework
- `geocode.py` - Utility for converting place names to geographic coordinates
- `pyproject.toml` - Project dependencies and configuration

## Features

- **Weather Forecasts**: Get detailed weather forecasts for any location using latitude/longitude coordinates
- **Weather Alerts**: Check for active weather alerts in any US state
- **Geocoding**: Automatically convert city or location names to the required coordinates
- **Framework Independence**: Same MCP server works with different agent frameworks
- **Redirect Handling**: Properly follows HTTP redirects from the weather API

## Installation

1. Clone this repository:

```bash
git clone https://github.com/shaunliew/weather_mcp.git
cd weather_mcp
```

2. Initialize and create a virtual environment with uv:

```bash
# Initialize the project
uv init

# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies from pyproject.toml:

```bash
# Install all dependencies from pyproject.toml
uv sync
```

4. Set your Anthropic API key (if you don't set it, the scripts will prompt you):

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Tutorial: How MCP Works

### 1. Understanding the MCP Architecture

MCP follows a client-server architecture:

- **MCP Servers** (like our `weather.py`): Expose tools and data sources
- **MCP Clients**: Connect to servers and translate between frameworks
- **Host Applications**: Applications like Claude Desktop that use MCP

### 2. Building an MCP Server

Our `weather.py` demonstrates how to create an MCP server with two tools:

```python
@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state."""
    # Implementation...

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location."""
    # Implementation...
```

Key features of our server:
- Clear documentation for each tool
- Proper error handling
- Redirect following for API requests
- Organized response formatting

### 3. Integrating with LangChain

The `langchain_weather.py` file shows how to integrate our MCP server with LangChain:

```python
async with MCPAdapt(
    StdioServerParameters(
        command="python",
        args=["weather.py"]
    ),
    LangChainAdapter(),
) as tools:
    # Create a LangChain agent with these tools
    agent_executor = create_react_agent(model, tools)
    
    # Use the agent
    result = await agent_executor.ainvoke({"messages": [...]})
```

Key steps:
1. Connect to the MCP server using `MCPAdapt`
2. Specify the server parameters (command and args)
3. Use the `LangChainAdapter` to convert MCP tools to LangChain format
4. Create a LangChain agent with these tools
5. Run the agent with user queries

### 4. Integrating with SmolAgents

The `smolagents_weather.py` file demonstrates SmolAgents integration:

```python
with ToolCollection.from_mcp(
    StdioServerParameters(command="python", args=["weather.py"]),
    trust_remote_code=True
) as tool_collection:
    # Create the SmolAgents agent with unpacked tools
    agent = CodeAgent(
        tools=[*tool_collection.tools],
        model=model
    )
    
    # Run the agent
    response = agent.run(question)
```

Important notes:
- **Security**: `trust_remote_code=True` acknowledges that you trust the MCP server to execute code on your system
- **Tool Unpacking**: Use `[*tool_collection.tools]` to correctly unpack the tools for SmolAgents
- **Code Execution**: SmolAgents uses a unique code-first approach to interact with tools

## Usage Examples

### Running with LangChain

```bash
# Run with uv
uv run langchain_weather.py
```

Example query: "What's the weather like in San Francisco?"

### Running with SmolAgents

```bash
# Run with uv
uv run smolagents_weather.py
```

Example query: "Are there any weather alerts in California?"

## Integrating with Claude Desktop

You can use this MCP server with Claude Desktop:

1. Edit your Claude Desktop configuration file:
   - Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the following configuration:

```json
{
    "mcpServers": {
        "weather": {
            "command": "python",
            "args": [
                "/absolute/path/to/weather_mcp/weather.py"
            ]
        }
    }
}
```

3. Restart Claude Desktop and look for the hammer icon in the UI

## Troubleshooting

### Common Issues

1. **301 Redirects**: If you see 301 status codes, make sure `follow_redirects=True` is set in the HTTP client
2. **SmolAgents Integration**: Ensure you use `[*tool_collection.tools]` to properly unpack tools for SmolAgents
3. **Security Warning**: For SmolAgents, you must acknowledge the security implications with `trust_remote_code=True`
4. **UV Installation**: If you have issues with uv, make sure you have the latest version installed

### Getting Logs

Check logs for debugging:
```bash
tail -n 20 -f ~/Library/Logs/Claude/mcp*.log
```

## Further Reading

- [MCP Documentation](https://modelcontextprotocol.io/)
- [LangChain Documentation](https://python.langchain.com/docs/)
- [SmolAgents Documentation](https://huggingface.co/docs/smolagents/)
- [UV Documentation](https://astral.sh/uv)
