# Build the scene

A video and splats start the same way: agree how to work, pose the images, and build the scene
out a few views at a time until it is blocked out with no gaps. This file is identical in
`atlas-flythrough` and `atlas-splats`.

Building the scene is also a job on its own. When the person asks for new angles of an image,
the other side of something, or more of a place, do it this way, starting with where to work,
whether or not they have chosen a video or splats yet. Views that already exist from earlier in
the session are the start of the scene: bring them in and keep building from there.

Camera and depth conventions are in [conventions.md](conventions.md). A complete run is in
[example.md](example.md).

## Agree how to work

The person directs and you do the work. Two decisions are theirs:

- **Where the work happens.** Blender is the preferred place when it is installed. Both of you
  see the scene in 3D, they can shape the result, and they keep a project file at the end.
- **What the result should be.** The subject, how far the camera goes, what they want to be able
  to look at.

Asking is the default for those two. Ask each in one short line when it comes up. A plain
request, such as "make me a flythrough", is not a request to skip the questions.

Once they are settled, carry the work through to the finished result without stopping. Show
each stage as it lands (the posed image, each round of views, the path) so the person can steer
whenever they want to. They have asked for the result, so the steps that produce it need no
go-ahead and no price quoted.

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

## 3. Build the scene out

One image is a single view of a place. This step decides what the rest of the place is: the far
side of the table, the wall behind the camera, what is round the corner. The model invents
whatever a camera sees that no frame has shown, and here that is the point. A round takes under
a minute, and you and the person see the result before anything is built on it.

Explore the way a person would walk into a room they had only seen in a photo: go in, cross to
the other side, turn round and look back. At this stage the question is what is in this place,
not where a camera path or a viewer will go. That comes after, and it will be better for having
a real scene to choose from.

Work in rounds:

1. **Place a few cameras** that stand somewhere no frame has stood and look at something no
   frame has shown: from one side of the main subject across to the other, from the far end
   back toward where the first camera stood, into a corner, through an opening.
2. **Generate them** as one `atlasGenerate` request, with the frames so far as `contextFrames`
   and `"returnDepth": true`, so each new view joins the scene with its own depth.
3. **Look at what came back.** Each view shows new surfaces and new open space. Drop a view that
   disagrees with the others.
4. **Place the next few** from what the new views revealed: floor that turned out to be open, a
   wall or a doorway nobody had seen.

**Take big steps.** A new view should show mostly new things. Look through each camera at the
scene's points before generating it. A frame about half filled with known points is a good
step. A frame that is nearly full is a view you already have, and a round of those leaves the
scene where it was. A frame with only a sliver of known points gives the model too little to
hold on to, and that view tends to disagree with the others; reach that spot a round later.

**The scene is built when it is blocked out, with no gaps.** That means views from opposite
sides of the main subject, a view from the far end looking back toward where the first camera
stood, and every wall, corner and stretch of floor in at least one view. Check from above with
all the point clouds showing: the floor and walls should be continuous. A hole is a place no
view has looked at, so put a view on it. A room usually takes three or four rounds and 12 to 16
views.

Block the whole place out before the path or the reconstruction, whatever route or subject the
person named. A scene built only along the route you expect has gaps the person finds as soon
as they look around, and it leaves the path and the splats nothing to work with beyond it.

Where the cameras go is your decision. Two things hold for all of them:

- They stand in space the frames so far show as empty. A camera inside an object, behind a
  wall, or outside what the frames saw gets large invented objects in front of the lens.
- Each has its own position. Views that only turn in place add little for the next round, and
  a request whose cameras all share one position cannot return depth.

```sh
worldlabs tasks run atlasGenerate --request views.json --wait --timeout 900 --json > views_op.json
worldlabs operations download <views-operation-id> --out views
```

The request is short; see [the example's second round](../assets/example/round-2-request.json).
With at most 11 context frames and 32 targets, depth is reconstructed in the same step, so in
later rounds pass the frames nearest the new cameras as context, not every frame. The
[task guide](https://docs.atlas.worldlabs.ai/atlas-generate.md) covers larger requests.

In Blender each round's views appear in the scene as cameras with point clouds, so the person
watches the place fill in.

## 4. Show the person

Show the views beside the source image. In Blender they are in the scene as cameras, each with
its image, depth and point cloud; tell the person they are there to look through and move
around. In a shell, one contact sheet does it.

Say in a line or two what came from the source and what the model invented, then carry on to
the long step. If they want something different they will say so, and changing the scene now is
quick.
