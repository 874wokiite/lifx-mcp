# lifx-mcp

MCP server for controlling LIFX smart bulbs via RGB values

## Requirements

- LIFX bulb must be on the same local network
- Python 3.12 or higher
- UDP port 56700 must be open on the network

## Features

- Change LIFX bulb color based on RGB values (0-255)
- Input validation (range check 0-255)
- Automatic conversion of RGB values to LIFX format

## Usage

1. Install dependencies:
```bash
uv pip install -e .
```

2. Start MCP server:
```bash
uv run src/lifx_mcp/server.py
```

3. Use the `control_light_by_rgb` tool:
```json
{
  "red": 255,
  "green": 100,
  "blue": 50
}
```

4. If bulb doesn't respond:
- Check bulb power
- Verify it's on the same network
- Check firewall settings
