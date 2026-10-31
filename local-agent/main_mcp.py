
import asyncio
import ollama

from mcp_client import MCPClient


# Configuration

MODEL = "qwen3.5:0.8b"

MCP_SERVER_URL = "https://catfact.ninja/mcp"

MAX_AGENT_STEPS = 5


SYSTEM_PROMPT = """
You are a helpful cat facts assistant.

You have access to these tools:
- random-cat-fact: Get one random cat fact.
- list-cat-facts: Get multiple cat facts.
- list-breeds: Get a list of cat breeds.

Rules:
1. Use the appropriate tool when the user asks for cat facts or breeds.
2. Do not invent cat facts.
3. Use the tool output as the source of truth.
4. If a tool returns an error, explain it to the user.
5. Answer in simple language.
"""


async def run_agent():

    # Initialize MCP client

    mcp_client = MCPClient(MCP_SERVER_URL)

    try:

        await mcp_client.connect()

        # Discover MCP tools

        mcp_tools = await mcp_client.list_tools()

        print("\nAvailable MCP tools:")

        for tool in mcp_tools:
            print(f"- {tool.name}: {tool.description}")

        # Convert MCP tools to Ollama format

        ollama_tools = mcp_client.convert_tools_to_ollama(
            mcp_tools
        )

        # Initialize conversation

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        print("\nCat Facts Agent is ready!")
        print("Type 'exit' to quit.")

        # Agent loop

        while True:

            user_input = input("\nYou: ").strip()

            if user_input.lower() in ["exit", "quit"]:
                break

            if not user_input:
                continue

            messages.append({
                "role": "user",
                "content": user_input
            })

            for step in range(MAX_AGENT_STEPS):

                print(f"\n[Agent step {step + 1}]")

                # Ask Ollama to process the request

                response = ollama.chat(
                    model=MODEL,
                    messages=messages,
                    tools=ollama_tools,
                    think=False
                )

                assistant_message = response.message

                messages.append(assistant_message)

                # Check for tool calls

                if not assistant_message.tool_calls:

                    print("\nAssistant:")
                    print(assistant_message.content)

                    break

                # Execute requested MCP tools

                for tool_call in assistant_message.tool_calls:

                    tool_name = tool_call.function.name

                    arguments = tool_call.function.arguments

                    tool_output = await mcp_client.execute_tool(
                        tool_name,
                        arguments
                    )

                    # Return tool result to Ollama

                    messages.append({
                        "role": "tool",
                        "tool_name": tool_name,
                        "content": tool_output
                    })

            else:

                print(
                    "\nMaximum agent steps reached. "
                    "Please try a simpler question."
                )

    finally:

        await mcp_client.disconnect()


if __name__ == "__main__":
    asyncio.run(run_agent())
