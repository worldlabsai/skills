---
name: atlas-flythrough
description: Make a camera-move video through a scene (flythrough, walkthrough, orbit, push-in, pan) from one or more photos or a generated image with World Labs Atlas. Use when the user wants a video or a camera move from images.
license: Apache-2.0
compatibility: Needs a shell with ffmpeg and the worldlabs CLI, signed in.
---

# Atlas flythrough

A flythrough is a camera path rendered by `atlasGenerate`: every frame's camera goes in one
request, and one image comes back per camera. The model follows a path well where it has views of
the scene to work from. So the work has two parts: a few views of where the camera will go, then
the path.

A flythrough should go somewhere. The camera travels a real distance through the scene, shows
things the first frame did not, and ends on a different view from the one it started on. A camera
that drifts a little near the source image is not a flythrough, and it is the usual way these
come out dull. Unless the person asks for a subtle move, plan a path with a destination.

## Steps

1. **Build the scene.** Follow [references/scene.md](references/scene.md): pose the images,
   generate a sparse set of views, and show them to the person. For a video the views cover the
   route and what the camera will look at along it, which need not be the full circle. Decide
   roughly where the path goes first, so the views can make that route possible. Skip this if
   posed views from earlier in the session already cover it.

2. **Choose the path.** How you build the cameras is up to you. A path that works well:

   - leaves the starting view early and keeps moving. Most of the video is spent somewhere the
     first frame was not;
   - has a shape a person would describe: down the aisle and round to the windows, through the
     doorway and around the table, up and over;
   - starts on a camera the person knows. To open on the photo, make the first camera the posed
     source camera;
   - stays in space the views show as empty, and near where the sparse views stood. The model has
     seen the scene from those places. Check the stretch between the source camera and the first
     view too: a straight line between two good positions can pass through a door frame;
   - keeps the subject in frame the way the person described the move;
   - has one camera per video frame (seconds x frame rate; 24 frames a second is a good default),
     evenly and closely spaced so the motion reads as smooth.

   Check the path before paying for it. Confirm that turns go the way the person asked and that no
   camera is inside an object. A sign error costs a full request.

3. **Generate once.** Tell the person the cost first: at current rates, 40 credits plus 8 for each
   frame after the first, so 192 frames are about 1,570 credits ($1.57). It takes one to three
   minutes.

   ```sh
   worldlabs tasks run atlasGenerate --request path.json --wait --timeout 1800 --json > path_op.json
   ```

   `contextFrames` holds the posed source frames and the sparse views that looked right, each with
   its camera and depth. `targetCameras` holds the path in order. Set `"returnDepth": false`. See
   [the example request](assets/example/path-request.json).

   Send the whole path in one request. Frames from separate requests do not match each other, so
   do not split a path into batches or splice in frames from an earlier request. More than a
   thousand frames fit in one request. If the wait times out, resume with
   `worldlabs operations wait <operation-id> --json`; do not submit again.

4. **Assemble and look.**

   ```sh
   worldlabs operations download <path-operation-id> --out frames
   ffmpeg -framerate 24 -pattern_type glob -i 'frames/frames_*_image.jpg' -c:v libx264 -pix_fmt yuv420p flythrough.mp4
   ```

   Frames are named in order (`frames_000_image.jpg`, ...); use the extension the files have. Look
   at about a dozen frames spread through the video. The first should match its camera's view, the
   motion should go the way the person asked, and objects should keep their shape. Report the
   video, the operation IDs, and what the model invented.

## Example

[A complete run](references/example.md): one photo of a potter's studio, seven views around the
work table, and an eight-second orbit. Its requests and results are in `assets/example/`. It
shows one scene's choices, not values to copy.

## Notes

- If the person asks for a subtle move, such as a slow push on one subject, make that. It is the
  one case where the source frame alone is enough context.
- `prompt` is optional and describes the scene, never the camera move or an edit. Leave it out and
  Atlas writes one from the images. To save time on a second request for the same scene, pass the
  first response's `promptUsed` as `prompt` with `"enhancePrompt": false`.
- An HTTP 422 means the request was rejected, not the key. The CLI does not print the reason;
  check sizes, depth on every context frame, and the camera fields against
  [conventions](references/conventions.md).
- If `worldlabs operations download` is missing, update the CLI:
  `npm install -g @worldlabsai/cli@latest`. Setup and other tasks are in the `worldlabs-cli` skill.
- No shell: connected World Labs tools take the same request bodies under the same task names,
  but a long path is impractical to pass through a tool call. Prefer a shell for video.
- Request fields and limits: https://docs.atlas.worldlabs.ai/atlas-generate.md
