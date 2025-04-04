import os
import re
import asyncio
from mcp import StdioServerParameters
from smolagents import CodeAgent, LiteLLMModel
from smolagents.tools import ToolCollection
from geocode import geocode

async def main():
    """SmolAgents integration with our Weather MCP server."""
    # Provide your Anthropic API key to use Claude
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Please set the ANTHROPIC_API_KEY environment variable or provide it below:")
        api_key = input("ANTHROPIC_API_KEY: ")
        os.environ["ANTHROPIC_API_KEY"] = api_key

    # Initialize the model
    model = LiteLLMModel(model_id="claude-3-opus-20240229",
                     api_key=os.environ["ANTHROPIC_API_KEY"])

    print("Connecting to MCP Weather server...")
    # Setup the MCP server parameters
    server_params = StdioServerParameters(command="python", args=["weather.py"])
    
    # Use the ToolCollection.from_mcp with proper unpacking of tools
    with ToolCollection.from_mcp(server_params, trust_remote_code=True) as tool_collection:
        print(f"Connected! Available tools: {[t.name for t in tool_collection.tools]}")
        
        # Create the agent with the properly unpacked MCP tools
        agent = CodeAgent(
            tools=[*tool_collection.tools],  # Unpack the tools properly
            model=model
        )
        
        # Get user input for a weather question
        print("\nAsk a question about the weather (e.g., 'Are there any weather alerts in California? What's the forecast for San Francisco?')")
        question = input("Your question: ")
        
        # Check if the question contains a location that needs geocoding
        location_pattern = r"in\s+([A-Za-z\s,]+)[\?.]?"
        match = re.search(location_pattern, question)
        
        if match:
            location = match.group(1).strip()
            print(f"\nGeocoding location: {location}...")
            lat, lon = await geocode(location)
            
            if lat and lon:
                print(f"Found coordinates: {lat}, {lon}")
                # Add the coordinates to the question
                enhanced_question = f"{question} I found that {location} is at latitude {lat}, longitude {lon}."
            else:
                print(f"Could not geocode location: {location}")
                enhanced_question = question
        else:
            enhanced_question = question
        
        # Use the agent to answer the question
        print("\nThinking...")
        response = agent.run(enhanced_question)
        
        print("\n" + "="*50)
        print("WEATHER REPORT:")
        print("="*50)
        print(response)
        
        print("\n\nDone! You can run this script again to ask another question.")

if __name__ == "__main__":
    asyncio.run(main())
