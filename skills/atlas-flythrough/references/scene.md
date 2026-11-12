# Build the scene

A video and splats start the same way: pose the images, generate a small set of views that shows
the scene from all around, and show them to the person before the long step. This file is
identical in `atlas-flythrough` and `atlas-splats`. If posed views of the scene already exist from
earlier in the session, reuse them and go to the long step.

Camera and depth conventions are in [conventions.md](conventions.md). A complete run is in
[example.md](example.md).

## 1. Pose the images

Upload each image, estimate its camera and depth, and save the result:

```sh
worldlabs assets upload room.jpg --json                    # note the "id"
echo '{"frames":[{"imageAsset":{"assetId":"<id>"}}],"targetResolution":[1280,720]}' > pose.json
worldlabs tasks run images2PosedRGBD --request pose.json --wait --json > pose_op.json
worldlabs operations download <pose-operation-id> --out scene
```

- `targetResolution` sets the grid every later step uses. Choose the size closest to the image's
  shape: `[1280, 720]`, `[960, 720]`, `[528, 704]` or `[720, 1280]`.
- Photos of one real place go in one request, so their cameras share a world.
- Posing puts the scene in a level, Y-up world. Pose an image from `atlasTextToImage` as well: the
  depth that task can return is not levelled.
- `scene/operation.json` holds each frame's camera, and for its image, depth and confidence the
  local `path` and the `assetId`. Later requests name frames by those asset IDs; nothing is
  uploaded again.

## 2. Read the scene

Open the depth and the camera before placing anything. Find the typical depth, what lies straight
ahead, the nearest objects, the floor, and the field of view. Decide what the main part of the
scene is: the object or area the person cares about, which the views will surround. Distances are
in the depth's units, so this is what tells you how big a move is and where there is room to
stand.

## 3. Generate a sparse set of views

Generate about 6 to 12 views that together show the main part of the scene. For splats, which
the person can look at from anywhere, that means from all around. For a video it means along the
route and toward what the camera will look at. They are one `atlasGenerate` request: the posed frames as `contextFrames`, your cameras as
`targetCameras`, and `"returnDepth": true` so each view comes back with depth and can be used in
the long step.

Where the cameras go is your decision. What tends to work:

- **Around the subject.** Cameras spread around the main part of the scene, each looking at it,
  at a height a person would stand or sit at. Around a table or a group of furniture that is
  roughly a ring. In a narrow space it may be a few positions along it, looking both ways.
- **In empty space the frames saw.** Use the depth to keep every camera where the posed frames
  show free space. A camera inside an object, behind a wall, or outside what the frames saw gets
  large invented objects in front of the lens.
- **Moved, not only turned.** Give each view its own position. Views made by turning in place are
  weak context for later steps, and a request whose cameras all share one position is rejected
  when it asks for depth.
- **Overlapping.** Neighbouring views should share part of what they see.
- **One request.** Views generated together agree with each other. The model decides the unseen
  sides of the scene once, for all of them.

These views are what let the long step go far. From one image alone, the model only follows a
camera that turns about half the field of view or moves about a third of the typical depth;
past that it invents what it shows. So do not plan the long step inside those limits. Place views
out where you want to go. The unseen parts are decided here, in a request that takes under a
minute, and you and the person see them before anything is built on them.

```sh
worldlabs tasks run atlasGenerate --request views.json --wait --timeout 900 --json > views_op.json
worldlabs operations download <views-operation-id> --out views
```

The request is short; see [the example's](../assets/example/views-request.json). At current rates
it costs 50 credits plus 10 for each view after the first, so 8 views are about 120 credits
($0.12). With at most 11 context frames and 32 targets, depth is reconstructed in the same
step; the [task guide](https://docs.atlas.worldlabs.ai/atlas-generate.md) covers larger requests.

Look at every view. Objects should keep their position, shape and appearance from view to view,
and nothing large should block a lens. Drop a view that disagrees with the rest. To replace it or
to fill a gap, send another request with the good views added to `contextFrames`.

## 4. Show the person

Put the views on one contact sheet and show it beside the source image. Any tool works; with
ffmpeg:

```sh
ffmpeg -pattern_type glob -i 'views/frames_*_image.jpg' -vf "scale=640:-1,tile=4x3" -frames:v 1 views.jpg
```

Say in a line or two what came from the source and what the model invented, and what the long
step will cost and how long it takes. Ask whether this is the scene they want. The long step
costs more, takes longer, and builds on these views, so this is the cheap moment to change
direction.

If the person asked for the result in one go, or told you not to check in, look at the views
yourself and carry on.
