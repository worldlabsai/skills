---
name: atlas-splats
description: Turn one or more photos or a generated image into a 3D scene as Gaussian splats (an SPZ file) with World Labs Atlas. Use when the user wants a 3D scene, a world to explore, splats, or a scene to view, export or mesh from images.
license: Apache-2.0
compatibility: Needs the worldlabs CLI, signed in. Blender is preferred when installed.
---

# Atlas splats

`posedImages2Splats` reconstructs a scene from posed views with depth, then refines it into an
SPZ file. It is the final step: one run takes 15 to 25 minutes and costs 5,000 credits ($5).
While refining it generates its own dense views, which it does not return.

What you control is the set of views you give it, so a good result comes from getting that set
right. The views are also the preview of the result.

## Steps

1. **Build the scene.** Follow [references/scene.md](references/scene.md). Its first part is a
   question to the person about where to work, with Blender as the preferred place. Ask it
   before anything else. It then poses the images, generates views around the main part of the
   scene, and shows them.

2. **Check the set as reconstruction input.** The posed frames and the views you kept are the
   input. A good set:

   - shows every area the person will look at: the floor, low furniture, walls, and the far side
     of anything they will move around. Areas no view shows come out blurry or invented;
   - agrees with itself. An object with a different shape or place in two views becomes a
     doubled, ghosted object;
   - has depth over most of every frame, and one size for all frames. A view can look right and
     still have depth on only a small part of it.

   For a single room, 8 to 16 views in all is a good range. To add coverage, send another
   `atlasGenerate` request with the current views as `contextFrames` and `"returnDepth": true`.

3. **Reconstruct once.** This is the step to confirm with the person: say the cost and the wait
   and get a yes. The request lists each frame's image, depth and camera; see
   [the example request](assets/example/splats-request.json).

   ```sh
   worldlabs tasks run posedImages2Splats --request splats.json --json > splats_op.json
   worldlabs operations wait <operation-id> --timeout 3600 --json
   ```

   Submit without `--wait` and keep the operation ID. If the wait times out, wait again. One
   submission is one charge, so a second submission while the first runs is a second charge.

4. **Hand it over.**

   ```sh
   worldlabs operations download <operation-id> --out splats
   ```

   The result is an SPZ file named for its splat count (`refinedSplats_2000000.spz`), in the
   same world as the cameras you sent. Look at it before you report: from the start view, and
   from places the person will go.

   Give the person the file, a way to look at it, the operation ID, and which parts of the scene
   the model invented. In Blender the splats import into the scene they have been watching.
   Otherwise see [Rendering with Spark](https://docs.atlas.worldlabs.ai/rendering-with-spark.md).

## Example

[A complete run](references/example.md): one photo of a potter's studio, seven views around the
work table, and one reconstruction from the eight frames, with pictures of the result. Its
requests and results are in `assets/example/`. It shows one scene's choices, not values to copy.

## Facts

- Bounded, textured interiors reconstruct best. Sky, foliage, thin structures, glass, faces and
  large plain walls are where artifacts appear, and so are surfaces that only one view sees at
  close range. Say so when the scene has them.
- `prompt` describes the scene. Leave it out and Atlas writes one from the images.
- For a mesh, pass the SPZ asset to `splats2Mesh` as `splatAsset`.
- A video of the same scene uses the same views; see the `atlas-flythrough` skill.
- An HTTP 422 means the request was rejected. The CLI does not print the reason; check that
  every frame has `imageAsset`, `depth.depthAsset` and `camera`, and that all cameras share one
  size.
- CLI setup, errors and other tasks are in the `worldlabs-cli` skill. Guides:
  https://docs.atlas.worldlabs.ai/posed-images-to-splats.md and
  https://docs.atlas.worldlabs.ai/splat-best-practices.md
