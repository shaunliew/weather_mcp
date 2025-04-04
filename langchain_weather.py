import os
import asyncio
from mcp import StdioServerParameters
from mcpadapt.core import MCPAdapt
from mcpadapt.langchain_adapter import LangChainAdapter
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

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
            max_tokens_to_sample=8192
        )
        agent_executor = create_react_agent(model, tools, checkpointer=memory)
        
        # Get user input for a weather question
        print("\nAsk a question about the weather (e.g., 'What's the weather like in New York City?')")
        question = input("Your question: ")
        
        # Use the agent to answer the question
        print("\nThinking...")
        config = {"configurable": {"thread_id": "weather-session"}}
        async for event in agent_executor.astream(
            {"messages": [HumanMessage(content=question)]},
            config,
        ):
            if "messages" in event:
                for message in event["messages"]:
                    print(f"{message.content}")
            else:
                print(".", end="", flush=True)
        
        print("\n\nDone! You can run this script again to ask another question.")

if __name__ == "__main__":
    asyncio.run(main())
