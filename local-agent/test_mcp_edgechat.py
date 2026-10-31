import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

MCP_SERVER_URL = "https://www.edgechat.ai/mcp"


async def main():
    async with streamable_http_client(MCP_SERVER_URL) as (
        read_stream,
        write_stream,
        get_session_id
    ):
        async with ClientSession(read_stream, write_stream) as session:

            await session.initialize()

            # Step 1: Search for an article
            search_result = await session.call_tool(
                "search",
                arguments={
                    "query": "Mount Fuji",
                    "limit": 3
                }
            )

            print("\n--- SEARCH RESULTS ---")

            for item in search_result.content:
                if hasattr(item, "text"):
                    print(item.text)

            # Step 2: Fetch the full article
            article_result = await session.call_tool(
                "fetch",
                arguments={
                    "id": "mount-fuji",
                    "length": "lead"
                }
            )

            print("\n--- FULL ARTICLE ---")

            for item in article_result.content:
                if hasattr(item, "text"):
                    print(item.text)

            print("\nFetch error:", article_result.isError)


if __name__ == "__main__":
    asyncio.run(main())