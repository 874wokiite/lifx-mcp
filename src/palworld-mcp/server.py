import asyncio
import random

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel


class GetToshibouFeelingSchema(BaseModel):
    question: str


async def serve() -> None:
    server = Server("palworld-mcp")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="get_toshibou_feeling",
                description="としぼうの気持ちを返します",
                inputSchema=GetToshibouFeelingSchema.model_json_schema(),
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, args: dict) -> list[TextContent]:
        match name:
            case "get_toshibou_feeling":
                feeling = (
                    "としぼうは元気いっぱいだ!!"
                    if random.randint(0, 1)
                    else "としぼうは元気がなさそうだ..."
                )
                return [
                    TextContent(
                        type="text",
                        text=feeling,
                    )
                ]
                return [
                    TextContent(
                        type="text",
                        text=feeling,
                    )
                ]
            case _:
                raise ValueError(f"Unknown tool: {name}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            options,
            raise_exceptions=True,
        )


if __name__ == "__main__":
    asyncio.run(serve())
