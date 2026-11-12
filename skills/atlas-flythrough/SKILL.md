---
name: atlas-flythrough
description: Make a camera-move video through a scene (flythrough, walkthrough, orbit, push-in, pan) from one or more photos or a generated image with World Labs Atlas. Use when the user wants a video or a camera move from images.
license: Apache-2.0
compatibility: Needs the worldlabs CLI, signed in, and ffmpeg. Blender is preferred when installed.
---

# Atlas flythrough

A flythrough is a camera path rendered by `atlasGenerate`: one camera per frame, all in one
request, one image back per camera.

A good one goes somewhere. The camera travels a real distance through the scene, shows things
the first frame did not, and ends on a different view from where it began. The model follows a
path where it has views of the scene to work from, so the work is in two parts: a few views of
where the camera will go, then the path.

## Steps

1. **Build the scene.** Follow [references/scene.md](references/scene.md). It starts by agreeing
   with the person how to work, with Blender as the preferred place, then poses the images,
   generates views along the route, and shows them. Decide roughly where the path goes before
   placing the views, so they make that route possible.

2. **Choose the path.** How you build the cameras is up to you. A good path:

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

   Make the move the person asked for. If they want a slow push on one subject, that is the
   shot, and the posed image alone is enough context for it.

   In Blender the path is an animated camera, and the cameras you send are its pose at each
   frame. In a shell, draw the route over the scene and check that turns go the way the person
   asked.

3. **Generate once.** Say what it costs first: at current rates, 40 credits plus 8 for each
   frame after the first, so 192 frames are about 1,570 credits ($1.57). It takes one to three
   minutes.

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

[A complete run](references/example.md): one photo of a potter's studio, seven views around the
work table, and an eight-second orbit. Its requests and results are in `assets/example/`. It
shows one scene's choices, not values to copy.

## Facts

- `prompt` describes the scene, never the camera move. Leave it out and Atlas writes one from
  the images. For a second request on the same scene, pass the first response's `promptUsed` as
  `prompt` with `"enhancePrompt": false` to save time.
- Frames are named in path order (`frames_000_image.jpg`, ...). Use the extension the files have.
- An HTTP 422 means the request was rejected. The CLI does not print the reason; check sizes,
  depth on every context frame, and the camera fields against
  [conventions](references/conventions.md).
- A path of a hundred or more cameras does not fit through a connected tool call. Without a
  shell, show the views and say the video needs a coding agent with a shell.
- CLI setup, errors and other tasks are in the `worldlabs-cli` skill. Request fields and limits:
  https://docs.atlas.worldlabs.ai/atlas-generate.md
