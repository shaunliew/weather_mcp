import os
import asyncio
import re
from mcp import StdioServerParameters
from mcpadapt.core import MCPAdapt
from mcpadapt.langchain_adapter import LangChainAdapter
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from geocode import geocode

async def main():
    """LangChain integration with our Weather MCP server."""
    # Provide your Anthropic API key to use Claude
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Please set the ANTHROPIC_API_KEY environment variable or provide it below:")
        api_key = input("ANTHROPIC_API_KEY: ")
        os.environ["ANTHROPIC_API_KEY"] = api_key

    print("Connecting to MCP Weather server...")
    async with MCPAdapt(
        StdioServerParameters(
            command="python",
            args=["weather.py"]
        ),
        LangChainAdapter(),
    ) as tools:
        print(f"Connected! Available tools: {[tool.name for tool in tools]}")
        
        # Create a LangChain agent
        memory = MemorySaver()
        model = ChatAnthropic(
            model_name="claude-3-opus-20240229", 
            max_tokens_to_sample=4096
        )
        agent_executor = create_react_agent(model, tools, checkpointer=memory)
        
        # Get user input for a weather question
        print("\nAsk a question about the weather (e.g., 'What's the weather like in New York City?')")
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
        config = {"configurable": {"thread_id": "weather-session"}}
        
        # Use the direct invocation to get the complete response
        result = await agent_executor.ainvoke(
            {"messages": [HumanMessage(content=enhanced_question)]},
            config
        )
        
        # Clean the response by removing thinking tags
        if "messages" in result and result["messages"]:
            response_content = result["messages"][-1].content
            # Remove thinking tags and content between them
            cleaned_response = re.sub(r'<thinking>.*?</thinking>', '', response_content, flags=re.DOTALL).strip()
            
            print("\n" + "="*50)
            print("WEATHER REPORT:")
            print("="*50)
            print(cleaned_response)
        else:
            print("\nNo response received from the agent.")
        
        print("\n\nDone! You can run this script again to ask another question.")

if __name__ == "__main__":
    asyncio.run(main())
