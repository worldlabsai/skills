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

## From images to a video or splats

The work has the same shape as outside Blender, and Blender lets you and the user see it in 3D:

1. Pose the images. Their cameras and point clouds appear in the scene.
2. Place about 6 to 12 target cameras around the main part of the scene, in space the point
   clouds show as empty, each looking at it. Generate them in one request with depth. Where they
   go is your call; look through them, or at the scene from above, before generating.
3. Show the user the generated views and the scene, and say what the model invented. Skip the
   check-in if they asked for the result in one go.
4. Then do the long step. For splats, run `splat` once on the views that agree with each other.
   For a video, generate the camera path as one request with the views as context.

With a shell and no open Blender session, run the same commands in
[background Blender](references/background.md).

For Atlas concepts, see the [Atlas documentation](https://docs.atlas.worldlabs.ai/how-to-use-atlas).
