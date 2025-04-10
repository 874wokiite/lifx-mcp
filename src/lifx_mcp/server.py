import asyncio
from lifxlan import LifxLAN
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel


class LIFXLightControlSchema(BaseModel):
    red: int
    green: int
    blue: int


async def serve() -> None:
    server = Server("lifx-mcp")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="control_light_by_rgb",
                description="RGB値に基づいてLIFX電球の色を設定します",
                inputSchema=LIFXLightControlSchema.model_json_schema(),
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, args: dict) -> list[TextContent]:
        match name:
            case "control_light_by_rgb":
                try:
                    lifx = LifxLAN()
                    devices = lifx.get_lights()

                    if not devices:
                        return [
                            TextContent(
                                type="text", text="LIFX電球が見つかりませんでした"
                            )
                        ]

                    bulb = devices[0]
                    red = args["red"]
                    green = args["green"]
                    blue = args["blue"]

                    if not all(0 <= val <= 255 for val in [red, green, blue]):
                        return [
                            TextContent(
                                type="text", text="RGB値は0-255の範囲で指定してください"
                            )
                        ]

                    # RGBをLIFX形式(0-65535)に変換
                    hue = int((red / 255) * 65535)
                    saturation = int((green / 255) * 65535)
                    brightness = int((blue / 255) * 65535)
                    bulb.set_color([hue, saturation, brightness, 3500])
                    return [
                        TextContent(
                            type="text", text=f"RGB({red},{green},{blue})で設定しました"
                        )
                    ]

                except Exception as e:
                    return [
                        TextContent(type="text", text=f"エラーが発生しました: {str(e)}")
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
