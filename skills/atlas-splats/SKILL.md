---
name: atlas-splats
description: Turn one or more photos or a generated image into a 3D scene as Gaussian splats (an SPZ file) with World Labs Atlas. Use when the user wants a 3D scene, a world to explore, splats, or a scene to view, export or mesh from images.
license: Apache-2.0
compatibility: Needs a shell with the worldlabs CLI, signed in.
---

# Atlas splats

`posedImages2Splats` reconstructs a scene from posed views with depth, then refines it. Treat it
as the final step. One run takes 15 to 25 minutes and costs 5,000 credits ($5). It generates its
own dense views while refining and does not return them, so what you control is the set of views
you give it. Get that set right first. Do not run a draft to preview: the views are the preview.

## Steps

1. **Build the scene.** Follow [references/scene.md](references/scene.md): pose the images,
   generate a sparse set of views around the main part of the scene, and show them to the person.
   Skip this if posed views from earlier in the session already cover the scene.

2. **Check the set as reconstruction input.** The posed source frames and the views that looked
   right are the input. Before submitting:

   - Every area the person will look at is in at least one view: the floor, low furniture, walls,
     and the far side of anything they will walk around. Areas no view shows come out blurry or
     invented.
   - Objects agree from view to view. A table with a different shape or place in two views
     becomes a doubled, ghosted table in the splats. Drop the view that disagrees.
   - Every frame has depth and all frames use one size.

   For a single room, 8 to 16 views in all is a good range. To add coverage, send another
   `atlasGenerate` request with the current views as `contextFrames` and `"returnDepth": true`.

3. **Submit once.** Tell the person the cost and the wait unless they already agreed to both. The
   request lists each frame's image, depth and camera; see
   [the example request](assets/example/splats-request.json).

   ```sh
   worldlabs tasks run posedImages2Splats --request splats.json --json > splats_op.json
   worldlabs operations wait <operation-id> --timeout 3600 --json
   ```

   Submit without `--wait` and keep the operation ID. If the wait times out, run it again. Do not
   submit again while the operation is running: a second run is a second charge.

4. **Download and hand over.**

   ```sh
   worldlabs operations download <operation-id> --out splats
   ```

   The result is an SPZ file, named for its splat count (`refinedSplats_2000000.spz`), in the
   same world as the cameras you sent. Report the file, the operation ID, and which parts of the
   scene the model invented. To view it, see
   [Rendering with Spark](https://docs.atlas.worldlabs.ai/rendering-with-spark.md); Blender 5.3
   and newer import SPZ files too. For a mesh, pass the SPZ asset to `splats2Mesh` as `splatAsset`.

## Example

[A complete run](references/example.md): one photo of a potter's studio, seven views around the
work table, and one reconstruction from the eight frames, with pictures of the result. Its requests and results are in
`assets/example/`. It shows one scene's choices, not values to copy.

## Notes

- Bounded, textured interiors reconstruct best. Sky, foliage, thin structures, glass, faces and
  large plain walls are where artifacts appear; say so when the scene has them. So are surfaces
  that only one view sees at close range, such as a door frame beside the source camera.
- `prompt` is optional and describes the scene. Leave it out and Atlas writes one from the
  images.
- An HTTP 422 means the request was rejected, not the key. The CLI does not print the reason;
  check that every frame has `imageAsset`, `depth.depthAsset` and `camera`, and that all cameras
  share one size.
- If `worldlabs operations download` is missing, update the CLI:
  `npm install -g @worldlabsai/cli@latest`. Setup and other tasks are in the `worldlabs-cli` skill.
- A video of the same scene uses the same views; see the `atlas-flythrough` skill.
- Guides: https://docs.atlas.worldlabs.ai/posed-images-to-splats.md and
  https://docs.atlas.worldlabs.ai/splat-best-practices.md
