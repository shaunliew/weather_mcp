# Weather MCP Server with LangChain and SmolAgents

This repository contains a Model Context Protocol (MCP) server that provides weather forecast and alert information. It also includes examples of how to use this server with LangChain and SmolAgents frameworks.

## Project Structure

- `weather.py` - The MCP server implementation
- `langchain_weather.py` - Example of using the MCP server with LangChain
- `smolagents_weather.py` - Example of using the MCP server with SmolAgents
- `geocode.py` - Utility for converting place names to geographic coordinates
- `requirements.txt` - Dependencies for the project

## Features

- **Weather Forecasts**: Get detailed weather forecasts for any location using latitude/longitude coordinates
- **Weather Alerts**: Check for active weather alerts in any US state
- **Geocoding**: Convert city or location names to the required latitude/longitude coordinates automatically
- **Framework Integration**: Examples for both LangChain and SmolAgents frameworks

## Setup

1. Create a virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Set your Anthropic API key (if you don't set it, the scripts will prompt you):

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Usage

### Running with LangChain

```bash
python langchain_weather.py
```

### Running with SmolAgents

```bash
python smolagents_weather.py
```

## MCP Server Capabilities

The MCP Weather server provides two main tools:

1. `get_alerts` - Get weather alerts for a US state using a two-letter state code (e.g., CA, NY)
2. `get_forecast` - Get weather forecast for a location using latitude and longitude coordinates

## Using with Claude Desktop

You can also use this MCP server with Claude Desktop by adding it to your configuration file:

- Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Add the following configuration:

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

Restart Claude Desktop and look for the tool icon (hammer) in the UI. When you ask about weather, Claude will automatically use your MCP server to get real-time data!
