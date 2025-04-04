import os
from mcp import StdioServerParameters
from smolagents import CodeAgent
from smolagents.models import AnthropicModel
from smolagents.tools import ToolCollection

def main():
    """SmolAgents integration with our Weather MCP server."""
    # Provide your Anthropic API key to use Claude
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Please set the ANTHROPIC_API_KEY environment variable or provide it below:")
        api_key = input("ANTHROPIC_API_KEY: ")
        os.environ["ANTHROPIC_API_KEY"] = api_key

    print("Connecting to MCP Weather server...")
    with ToolCollection.from_mcp(
        StdioServerParameters(command="python", args=["weather.py"])
    ) as tool_collection:
        print(f"Connected! Available tools: {[tool.name for tool in tool_collection]}")
        
        # Create a SmolAgents agent
        agent = CodeAgent(
            tools=tool_collection,
            model=AnthropicModel(model="claude-3-opus-20240229")
        )
        
        # Get user input for a weather question
        print("\nAsk a question about the weather (e.g., 'Are there any weather alerts in California? What's the forecast for San Francisco?')")
        question = input("Your question: ")
        
        # Use the agent to answer the question
        print("\nThinking...")
        response = agent.run(question)
        print(f"\nResponse: {response}")
        
        print("\nDone! You can run this script again to ask another question.")

if __name__ == "__main__":
    main()
