
import json

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


class MCPClient:

    def __init__(self, server_url: str):
        self.server_url = server_url
        self.session = None
        self.connection = None

    async def connect(self):
        """Connect and initialize the MCP server."""

        print("Connecting to MCP server...")

        self.connection = streamable_http_client(
            self.server_url
        )

        read_stream, write_stream, get_session_id = (
            await self.connection.__aenter__()
        )

        self.session = ClientSession(
            read_stream,
            write_stream
        )

        await self.session.__aenter__()

        await self.session.initialize()

        print("Connected to MCP server!")

    async def disconnect(self):
        """Close MCP connection."""

        if self.session:
            await self.session.__aexit__(None, None, None)

        if self.connection:
            await self.connection.__aexit__(None, None, None)

        print("MCP connection closed.")

    async def list_tools(self):
        """Discover available tools from MCP server."""

        response = await self.session.list_tools()

        return response.tools

    def convert_tools_to_ollama(self, mcp_tools):
        """
        Convert MCP tool definitions into
        Ollama-compatible tool definitions.
        """

        ollama_tools = []

        for tool in mcp_tools:

            ollama_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": tool.inputSchema
                }
            })

        return ollama_tools

    async def execute_tool(self, tool_name, arguments):
        """Execute an MCP tool."""

        print(f"\n[Calling MCP tool: {tool_name}]")
        print(f"Arguments: {arguments}")

        try:

            result = await self.session.call_tool(
                tool_name,
                arguments=arguments
            )

            print(f"\n[MCP tool result: {self.format_tool_result(result)}]")
            return self.format_tool_result(result)

        except Exception as error:

            print(f"MCP execution error: {error}")

            return f"Tool execution failed: {error}"

    @staticmethod
    def format_tool_result(result):
        """Convert MCP result into text."""

        if result.isError:
            return "MCP tool execution failed."

        if result.structuredContent is not None:
            return json.dumps(
                result.structuredContent,
                indent=2
            )

        output = []

        for item in result.content:

            if hasattr(item, "text"):
                output.append(item.text)

        return "\n".join(output)
