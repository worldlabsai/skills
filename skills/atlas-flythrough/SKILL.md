---
name: atlas-flythrough
description: Make a camera-move video through a scene (flythrough, walkthrough, orbit, push-in, pan) from one or more photos or a generated image with World Labs Atlas. Use when the user wants a video or a camera move from images, or new angles of a scene that may become one.
license: Apache-2.0
compatibility: Needs the worldlabs CLI, signed in, and ffmpeg. Blender is preferred when installed.
---

# Atlas flythrough

A flythrough is a camera path rendered by `atlasGenerate`: one camera per frame, all in one
request, one image back per camera.

A good one goes somewhere. The camera travels a real distance through the scene, shows things
the first frame did not, and ends on a different view from where it began.

The work is in two parts, in this order: build out the scene, then find a path through it. One
posed image is a single view of a place. Going in, crossing to the far side and looking back, a
few views at a time, uncovers the rest of the space, and that is what gives the camera somewhere
to go.

The shot is chosen in step 2, from the scene. Until then there is no route: do not describe a
camera move to the person or place views along one. A path planned from the one image has only
what that image showed to work with.

## Steps

1. **Agree where to work, then build the scene.** Before anything else, check whether Blender
   is installed and ask the person where to work. With Blender installed, the choice is:

   - **Open Blender**, so they can watch the scene build and scrub through it; or
   - **Build in the background** and hand over the `.blend` at the end.

   If they choose the open window, open it as soon as the first image is posed, before any
   views or path, so they watch from the start. Without Blender, work in the shell.
   [references/scene.md](references/scene.md) has the question for each setup and the steps:
   pose the images, build the scene out in rounds of a few views, and show it. At the end of
   this step there is a scene, not one image: views from all around it, including from the far
   side looking back toward where the first camera stood, which you and the person have both
   looked at. Views that stay beside the first camera and face the way it faced are not that.
   The scene is blocked out in full, a dozen or more views with no gaps, before any path.

2. **Choose the path through the scene you built.** Look at what the views uncovered and pick a
   route that uses it. How you build the cameras is up to you. A good path:

   - crosses the scene: to its far side, or around its main subject. A short arc beside the
     starting view is not a flythrough;
   - leaves the starting view early and keeps moving, so most of the video is somewhere the
     first frame was not;
   - has a shape a person would describe: down the aisle and round to the windows, through the
     doorway and around the table;
   - opens on a view the person knows. To open on the photo, the first camera is its posed
     camera;
   - stays in open space, near where the views stood. Check the stretches between them too: a
     straight line between two open positions can pass through a door frame;
   - has one camera per frame (seconds x frame rate; 24 a second is a good default), evenly and
     closely spaced.

   If the best route needs somewhere the views do not show yet, add views there first.

   In Blender the path is an animated camera, and the cameras you send are its pose at each
   frame. In a shell, draw the route over the scene and check that turns go the way the person
   asked.

3. **Generate once.** Send the whole path as one request as soon as it is ready. It takes one
   to three minutes.

   ```sh
   worldlabs tasks run atlasGenerate --request path.json --wait --timeout 1800 --json > path_op.json
   ```

   `contextFrames` holds the posed frames and the views you kept, each with its camera and
   depth. `targetCameras` holds the path in order. Set `"returnDepth": false`. See
   [the example request](assets/example/path-request.json).

   The whole path goes in one request, because frames from separate requests do not match each
   other. More than a thousand frames fit. If the wait times out, resume with
   `worldlabs operations wait <operation-id> --json`.

4. **Hand it over.**

   ```sh
   worldlabs operations download <path-operation-id> --out frames
   ffmpeg -framerate 24 -pattern_type glob -i 'frames/frames_*_image.jpg' -c:v libx264 -pix_fmt yuv420p flythrough.mp4
   ```

   Look at about a dozen frames spread through the video before you report. The first should
   match its camera's view, the motion should go the way the person asked, and objects should
   keep their shape.

   Give the person the video, the operation IDs, and what the model invented. When Blender was
   used, give them the project file as well; the `atlas-blender` skill says what it should
   contain.

## Example

[A complete run](references/example.md): one photo of a potter's studio, the room built out in
three rounds of views, and an eight-second flythrough chosen from what they revealed. Its
requests and results are in `assets/example/`. It shows one scene's choices, not values to copy.

## Facts

- `prompt` describes the scene, never the camera move. Leave it out and Atlas writes one from
  the images. For a second request on the same scene, pass the first response's `promptUsed` as
  `prompt` with `"enhancePrompt": false` to save time.
- Frames are named in path order, with indexes padded to the same width (`frames_000_image.jpg`
  for a long path, `frames_0_image.jpg` for a few views). `operation.json` lists them in order
  too. Use the extension the files have.
- An HTTP 422 means the request was rejected. The CLI does not print the reason; check sizes,
  depth on every context frame, and the camera fields against
  [conventions](references/conventions.md).
- A path of a hundred or more cameras does not fit through a connected tool call. Without a
  shell, show the views and say the video needs a coding agent with a shell.
- CLI setup, errors and other tasks are in the `worldlabs-cli` skill. Request fields and limits:
  https://docs.atlas.worldlabs.ai/atlas-generate.md
