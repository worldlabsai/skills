---
name: atlas-blender
description: Use Blender to see and shape Atlas scenes in 3D. Load posed images as cameras and point clouds, place cameras by eye, view splats, and optionally run Atlas tasks from inside Blender with the Atlas add-on. Use when Blender is installed or the user works in Blender.
license: Apache-2.0
---

# Atlas in Blender

Blender gives you and the user a shared 3D view of an Atlas scene: posed images as cameras with
point clouds, cameras you can place by eye, and splats you can fly through. There are two ways
to use it, and the first needs no Atlas add-on.

## 1. Blender as the 3D view

Run the Atlas tasks with the CLI (see `atlas-flythrough`, `atlas-splats` and `worldlabs-cli`) and
put the results in Blender to look at and plan from. This needs Blender 5.3 or newer and a way to
run Python in it:

- **A live connection.** Blender is open and you reach it through
  [Blender MCP](https://www.blender.org/lab/mcp-server/). The user watches the scene change.
- **In the background.** Build a `.blend` from the shell with
  [background Blender](references/background.md) and hand it over at the end.

Ask the user which they want. If the Blender tools or the Atlas add-on are missing, ask whether
they would like you to set them up; see [setup](references/setup.md). Do not pick for them.

Loading results is one command when the Atlas add-on is installed, and it works offline with no
API key; see "Import CLI results" in [commands](references/commands.md). Without the add-on,
create the cameras and point clouds yourself from each frame's camera and depth.

## Leave a normal Blender project

Whatever you build, the user should be able to open the file and use it the way they use any
Blender project. Work with Blender's own features, not stand-ins for them.

- **A camera move is an animated camera.** Keyframe the camera on the timeline. If the user
  wants to reshape the shot by dragging handles, put the camera on a Bezier curve with a Follow
  Path constraint instead.
- **Show the path with Blender's own guides.** Motion Paths on the animated camera draws its
  route. Do not add spheres, curves or other markers as scene geometry: they show up through the
  lens.
- **Play should work on first open.** Set the timeline to the shot's length and frame rate, and
  leave it on the first frame.
- **Lay out the window for watching.** Put the view through the camera beside an overview in
  which the camera is visible, with overlays on, so the user sees the camera move when they
  press Play.
- **Show colours.** Points and splats draw grey in Solid shading. Leave the viewports in
  Material Preview or Rendered.
- **Keep Blender and Atlas in step.** The cameras sent to Atlas are the animated camera's own
  pose at each frame. Say that the viewport shows the estimated point cloud, and that the video
  holds the finished frames.
- **Check it as the user will.** Save, reopen the saved file, play it through, and look near the
  start and the end before handing it over. Give the user the file's path along with the result.

All of this can be produced in background Blender when there is no open session.

## 2. Atlas inside Blender, with the add-on

The Atlas add-on poses images, generates views and builds splats from inside Blender, using its
own API key. Enable it in Blender 5.3+; see [setup](references/setup.md) for installation and
read-only verification. It is a separate add-on from Blender MCP, and this plugin installs
neither. If this host has no access to Blender, explain the local requirements instead of
attempting Blender operations.

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
