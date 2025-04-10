import asyncio
import colorsys
from lifxlan import LifxLAN
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel


class LIFXLightControlSchema(BaseModel):
    red: int
    green: int
    blue: int
    kelvin: int = 3500


async def serve() -> None:
    server = Server("lifx-mcp")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="control_light_by_rgb",
                description="Set LIFX bulb color based on RGB values",
                inputSchema=LIFXLightControlSchema.model_json_schema(),
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, args: dict) -> list[TextContent]:
        if name == "control_light_by_rgb":
            try:
                lifx = LifxLAN()
                devices = lifx.get_lights()

                if not devices:
                    return [TextContent(type="text", text="No LIFX bulbs found")]

                bulb = devices[0]
                red = args["red"]
                green = args["green"]
                blue = args["blue"]
                kelvin = args.get("kelvin", 3500)

                if not all(0 <= val <= 255 for val in [red, green, blue]):
                    return [
                        TextContent(
                            type="text", text="RGB values must be between 0 and 255"
                        )
                    ]

                r, g, b = red / 255.0, green / 255.0, blue / 255.0
                h, s, v = colorsys.rgb_to_hsv(r, g, b)

                hue = int(h * 65535)
                saturation = int(s * 65535)
                brightness = int(v * 65535)

                bulb.set_color([hue, saturation, brightness, kelvin])
                return [
                    TextContent(
                        type="text",
                        text=f"Set to RGB({red},{green},{blue}) with kelvin {kelvin}",
                    )
                ]

            except Exception as e:
                return [TextContent(type="text", text=f"Error occurred: {str(e)}")]
        else:
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
