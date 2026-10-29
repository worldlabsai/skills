# Set up Atlas for Blender

Requires Blender 5.3 or newer. Gaussian splats require Marble 2 beta access.

An agent works with Atlas in Blender through three separate pieces:

1. **Blender MCP add-on**, installed inside Blender. It lets an agent run Python in the open
   Blender session.
2. **Blender MCP server**, configured in the agent client as a connector or MCP server.
3. **Atlas add-on**, installed separately inside Blender. This plugin's Atlas skill tells the agent
   how to use it.

This plugin installs none of them and does not configure Blender MCP.

## Connect an agent through Blender MCP

Use Blender MCP: it is the recommended way for an agent to work in Blender. If it is not set up,
ask the user whether they want you to install and configure it for them, then follow the steps
below for their client. It is not strictly required; without it, the Atlas commands also run
through Blender's Python Console, Text Editor, or command line.

- **Claude Desktop:** Claude's Blender integration uses the same Blender-developed MCP
  implementation, not a separate one
  ([announcement](https://www.anthropic.com/news/claude-for-creative-work)). Add it under
  **Customize > Connectors > Blender > Add**, then install the Blender-side add-on as
  [Claude's Blender connector setup](https://academy.claude.com/tutorials/using-the-blender-connector-in-claude)
  describes.
- **Other agent clients:** follow [Blender's MCP setup](https://www.blender.org/lab/mcp-server/)
  for the add-on and the client configuration.

If Blender MCP already works with your agent, you only need the Atlas add-on and this skill.

## Install and configure Atlas

Download [Atlas 0.1.2](https://cdn.atlas-beta.worldlabs.ai/showcase/blender/worldlabs_atlas-0.1.2.zip)
([SHA-256 checksum](https://cdn.atlas-beta.worldlabs.ai/showcase/blender/worldlabs_atlas-0.1.2.zip.sha256)).
Version 0.1.2 includes the Blender Python commands used by this skill and creates refined splats by default; upgrade older installations.

1. In the intended Blender installation, open **Preferences > Get Extensions > Install from Disk**;
   select `worldlabs_atlas-0.1.2.zip` and enable Atlas. Confirm version **0.1.2** in the extension details.
2. For online posing and generation, enable **Allow Online Access** in Blender Preferences and
   enter the World Labs API key in the Atlas sidebar under **Settings > Connection**. Local imports
   work offline. Keep keys out of chat.
3. Keep the Blender project open.

## Verify the add-on

Run this from Blender's Python environment. It lists Atlas frames without editing scene objects or
making an online request:

```python
import bpy
import json

if bpy.app.version < (5, 3, 0):
    raise RuntimeError("Atlas requires Blender 5.3 or newer")

try:
    bpy.ops.atlas.command.get_rna_type()
except KeyError as exc:
    raise RuntimeError("Enable an Atlas build with bpy.ops.atlas.command support") from exc

bpy.ops.atlas.command(request_json=json.dumps({"command": "frames.list", "args": {}}))
response = json.loads(bpy.context.window_manager.atlas_result)
if not response.get("ok"):
    raise RuntimeError(response.get("error", {}).get("message", "Atlas request failed"))
print(response["result"])
```

An empty frame list is valid. For operator syntax and import, posing, generation, and job commands,
see [commands](commands.md).
