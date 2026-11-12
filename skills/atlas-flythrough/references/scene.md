# Build the scene

A video and splats start the same way: agree how to work, pose the images, generate views that
uncover the scene, and look at them with the person before the long step. This file is identical in
`atlas-flythrough` and `atlas-splats`. If posed views of the scene already exist from earlier in
the session, reuse them and go to the long step.

Camera and depth conventions are in [conventions.md](conventions.md). A complete run is in
[example.md](example.md).

## Agree how to work

The person directs and you do the work. Three decisions are theirs:

- **Where the work happens.** Blender is the preferred place when it is installed. Both of you
  see the scene in 3D, they can shape the result, and they keep a project file at the end.
- **What the result should be.** The subject, how far the camera goes, what they want to be able
  to look at.
- **When to spend on the long step.** They see the views, the cost and the wait first.

Asking is the default. Ask each in one short line when it comes up, and then carry on. A plain
request, such as "make me a flythrough", is not a request to skip the questions.

Decide for the person only when they say outright that they do not want to be asked, for example
"don't check in, just deliver it". Then choose what they would most likely choose, and say what
you chose. For where to work, that is Blender in the background whenever it is installed.

Where to work comes first, before posing or reading further. Check what is there, then ask the
question that fits:

| What you find | What to ask |
| --- | --- |
| Blender 5.3 or newer, connected (it is open and you can run Python in it through Blender tools), with the Atlas add-on | Work in the open window where they can watch, or in the background and hand over the project at the end? |
| Blender installed, but the Blender tools or the Atlas add-on missing | Set that up now, or work in the background with what is there? Background work needs neither. |
| No Blender | Nothing. Work in the shell, and mention once that Blender would let both of you see the scene in 3D. |

Put the question in the person's terms: what each choice lets them see, and what it needs from
them. Words like "connected" describe your side of it and mean little to them. For example:
"Blender is installed. I can build this in an open Blender window so you can watch it take
shape, which needs Blender open and takes me a minute to link up, or build it in the background
and give you the Blender file at the end. Which would you like?"

`blender --version`, or `/Applications/Blender.app` on a Mac, tells you whether it is installed.
The `atlas-blender` skill covers working in Blender, with or without the add-on. Atlas tasks
themselves always run through the `worldlabs` CLI below, or through the add-on.

With only connected World Labs tools and no shell, the task tools take the same requests. The
depth files usually cannot be read there, so cameras are placed without measuring: stay near
space the image clearly shows as open, generate a few views at a time, and look at each result.

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

## 2. See the scene

Look at the scene before placing anything, and look at it as a picture, not only as numbers. In
Blender the posed frames are cameras with point clouds. In a shell, draw the depth points from
above with the camera on them; walls, furniture and open floor show at a glance.

Find how far away things are, where the floor is, and where there is room to stand. Distances
are in the depth's units, which is what tells you how big a move is. Settle with the person what
the main part of the scene is.

## 3. Generate views

Generate about 6 to 12 views that uncover the scene: the main part of it from all around, and
the space beside and beyond what the image showed. One image is a single view of a place. After
this step there should be a scene, with enough of the space known that there are real choices
about where a camera can go or where a person can look.

These views are what make the long step possible. From one image alone, the model only follows a
camera that turns about half the field of view or moves about a third of the typical depth; past
that it invents what it shows. What the image did not show gets decided here, in a request that
takes under a minute, and you both see it before anything is built on it.

Where the cameras go is your decision. Good views:

- stand in space the posed frames show as empty. A camera inside an object, behind a wall, or
  outside what the frames saw gets large invented objects in front of the lens;
- each have their own position. Views that only turn in place add little for later steps, and a
  request whose cameras all share one position cannot return depth;
- overlap their neighbours;
- look at what matters, from about the height a person would see it.

Send them as one `atlasGenerate` request: the posed frames as `contextFrames`, your cameras as
`targetCameras`, and `"returnDepth": true` so each view can be used in the long step. Views
generated together agree with each other. When a scene is hard to see in advance, work a view or
two at a time instead: generate, look, add the result to `contextFrames`, and place the next.

```sh
worldlabs tasks run atlasGenerate --request views.json --wait --timeout 900 --json > views_op.json
worldlabs operations download <views-operation-id> --out views
```

The request is short; see [the example's](../assets/example/views-request.json). At current rates
it costs 50 credits plus 10 for each view after the first, so 8 views are about 120 credits
($0.12). With at most 11 context frames and 32 targets, depth is reconstructed in the same step;
the [task guide](https://docs.atlas.worldlabs.ai/atlas-generate.md) covers larger requests.

Look at every view. Objects should keep their position, shape and appearance from view to view,
and nothing large should block a lens. Drop a view that disagrees with the rest. To replace it or
to fill a gap, send another request with the good views added to `contextFrames`.

## 4. Show the person

Show the views beside the source image. In Blender they are in the scene as cameras, each with
its image, depth and point cloud; tell the person they are there to look through and move
around. In a shell, one contact sheet does it.

Say in a line or two what came from the source and what the model invented, and what the long
step will cost and how long it takes. Then ask whether this is the scene they want, and wait
for the answer. They are being invited to steer, and this is the cheap moment to do it.
