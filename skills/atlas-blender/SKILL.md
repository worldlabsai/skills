---
name: atlas-blender
description: Use Blender to see and shape Atlas scenes in 3D. Load posed images as cameras and point clouds, place cameras by eye, animate a camera path, view splats, and optionally run Atlas tasks from inside Blender with the Atlas add-on. Use when Blender is installed or the user works in Blender.
license: Apache-2.0
---

# Atlas in Blender

Blender is where you and the user can both see an Atlas scene: posed images as cameras with
point clouds, cameras placed by eye, a camera path on the timeline, and splats to fly through.
It is the preferred place for Atlas work when it is installed.

The method for a video or for splats is in the `atlas-flythrough` and `atlas-splats` skills.
This skill is how that work is done in Blender. It needs Blender 5.3 or newer.

## Agree how to use Blender

How Blender is used is the user's choice. Ask in one line:

- **An open window or the background.** In an open Blender you work through
  [Blender MCP](https://www.blender.org/lab/mcp-server/) and the user watches the scene change.
  In the background you build a `.blend` from the shell and hand it over at the end; see
  [background](references/background.md).
- **Anything missing.** If the Blender tools or the Atlas add-on are not there, ask whether the
  user wants them set up; see [setup](references/setup.md). This plugin installs neither, and
  background work needs neither.

## What the Atlas add-on adds

Blender alone is enough to look at and plan a scene. Atlas tasks then run through the
`worldlabs` CLI, and you bring the results in.

The Atlas add-on makes two things easier:

- **Loading results.** One import turns a folder of posed frames into cameras with images and
  point clouds. It works offline and needs no API key; see "Import CLI results" in
  [commands](references/commands.md). Without the add-on, build the cameras and point clouds
  from each frame's camera and depth yourself.
- **Running Atlas from inside Blender.** It can pose images, generate views from the cameras in
  the scene, and build splats, using its own API key. Read [commands](references/commands.md)
  for the calls and job handling.

## The steps, in Blender

| Step | In Blender |
| --- | --- |
| Pose the images | The add-on's `pose`, or pose with the CLI and import the result |
| See the scene | The viewport: through a posed camera, or from above |
| Place views | Ordinary camera tools, or `camera.create` and `camera.set`, in space the point clouds show as empty |
| Generate views | The add-on's `generate` with depth, or the CLI with the cameras' poses |
| Show the person | The scene itself, with each generated image on its camera |
| Camera path | An animated camera; its pose at each frame is what you send to Atlas |
| Video | The CLI for a path of any length; the add-on's `generate` holds up to 128 views, context included |
| Splats | The add-on's `splat`, or the CLI; the result imports as a native object |

When placing separately posed images in one scene, read
[scene placement](references/scene-placement.md). Camera visibility decides which frames the
add-on uses as context; **Points** toggles the point clouds on their own.

## Leave a normal Blender project

The user should be able to open the file and use it like any Blender project. Work with
Blender's own features.

- **A camera move is an animated camera**, keyframed on the timeline. If the user wants to
  reshape the shot by dragging handles, it is a camera on a Bezier curve with a Follow Path
  constraint.
- **The route is shown by Motion Paths** on that camera. Markers added as scene objects show up
  through the lens.
- **Play works on first open.** The timeline has the shot's length and frame rate and sits on
  the first frame.
- **The window is laid out for watching:** the view through the camera beside an overview in
  which the camera is visible, with overlays on.
- **Colours show.** Points and splats draw grey in Solid shading, so the viewports are in
  Material Preview or Rendered.
- **Blender and Atlas agree.** What plays in Blender is the path that was rendered. The viewport
  shows the estimated point cloud; the video holds the finished frames.

Before handing over, save, reopen the saved file and play it through, looking near the start
and the end. Give the user the file's path with the result.

For Atlas concepts, see the [Atlas documentation](https://docs.atlas.worldlabs.ai/how-to-use-atlas).
