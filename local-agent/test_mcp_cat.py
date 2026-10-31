import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
import traceback


MCP_SERVER_URL = "https://catfact.ninja/mcp"


def print_tool_result(result):
    """Print text or structured content returned by an MCP tool."""
    if result.isError:
        print("The MCP server reported an error.")

    if result.structuredContent is not None:
        print(result.structuredContent)

    for item in result.content:
        if hasattr(item, "text"):
            print(item.text)
        else:
            print(item)


async def main():
    print(f"Connecting to: {MCP_SERVER_URL}")

    # New MCP SDK API:
    # streamable_http_client returns exactly two streams.
    async with streamable_http_client(MCP_SERVER_URL) as (
        read_stream,
        write_stream,
        get_session_id,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the MCP session.
            await session.initialize()
            print("\nConnected successfully.")

            # Discover tools exposed by the server.
            tools_response = await session.list_tools()

            print("\nAvailable MCP tools:")
            for tool in tools_response.tools:
                print(f"\n- {tool.name}")
                print(f"  Description: {tool.description}")
                print(f"  Input schema: {tool.inputSchema}")

            # Test 1: Get one random cat fact.
            print("\n" + "=" * 60)
            print("TEST 1: random-cat-fact")
            print("=" * 60)

            result = await session.call_tool(
                "random-cat-fact",
                arguments={"max_length": 200},
            )
            print_tool_result(result)

            # Test 2: Get three cat facts.
            print("\n" + "=" * 60)
            print("TEST 2: list-cat-facts")
            print("=" * 60)

            result = await session.call_tool(
                "list-cat-facts",
                arguments={"limit": 3, "max_length": 200},
            )
            print_tool_result(result)

            # Test 3: Get five cat breeds.
            print("\n" + "=" * 60)
            print("TEST 3: list-breeds")
            print("=" * 60)

            result = await session.call_tool(
                "list-breeds",
                arguments={"limit": 5},
            )
            print_tool_result(result)

            print("\nAll test calls completed.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nTest interrupted.")
    except Exception as exc:
        print(f"\nMCP test failed: {type(exc).__name__}: {exc}")
