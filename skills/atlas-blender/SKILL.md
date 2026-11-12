---
name: atlas-blender
description: Use Atlas in Blender to import camera/image/depth projects, pose images into point clouds, place cameras and generate views with Atlas or Chisel, and create native Gaussian splats. Use when the user works in Blender or wants the scene laid out in 3D.
license: Apache-2.0
---

# Atlas for Blender

Enable Atlas in Blender 5.3+; see [setup](references/setup.md) for installation and read-only verification. Atlas is a separate Blender add-on from Blender MCP. Use [Blender MCP](https://www.blender.org/lab/mcp-server/) for agent access; this plugin neither installs nor configures it. If Blender MCP is not connected, ask the user whether they want you to install and configure it for them, following [setup](references/setup.md). If they decline, run the Atlas commands through Blender's Python Console, Text Editor, or command line.

If this host has no access to Blender, explain the local requirements instead of attempting Blender operations.

Run Atlas's operators inside Blender's Python environment. Read [commands](references/commands.md) when you need call syntax, import formats, or job handling.

Import exports containing camera JSON, images, depth, and confidence directly; they already have poses. Inspect unfamiliar layouts rather than assuming an exact folder structure or re-posing calibrated images.

When assembling posed images into a shared scene, read [scene placement](references/scene-placement.md) for the concepts. Choose your own placement and inspection methods.

Camera visibility controls Atlas context. **Points** toggles point clouds independently. Use ordinary Blender tools and scene state for everything else.

## A video or splats, in Blender

The method is in the `atlas-flythrough` and `atlas-splats` skills. This is how each of their
steps is done here:

| Step | In Blender |
| --- | --- |
| Pose the images | `pose`; the frames appear as cameras with point clouds |
| See the scene | The viewport: look through a posed camera, or at the scene from above |
| Place views | `camera.create` and `camera.set`, or ordinary Blender camera tools, in space the point clouds show as empty |
| Generate views | `generate` with depth, on the cameras you placed |
| Show the person | The scene itself, and the generated images on their cameras |
| Splats | `splat`, once; the result imports as a native object |
| Video | `generate` for a path of up to 128 views, context included; a longer path goes through the CLI |

With a shell and no open Blender session, run the same commands in
[background Blender](references/background.md).

For Atlas concepts, see the [Atlas documentation](https://docs.atlas.worldlabs.ai/how-to-use-atlas).
