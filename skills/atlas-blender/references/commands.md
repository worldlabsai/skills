# Atlas Blender calls

Execute these snippets inside Blender through MCP or another Python execution method. The operator works regardless of the extension's installed Python package name.

```python
import bpy
import json

def atlas(command, **args):
    bpy.ops.atlas.command(request_json=json.dumps({"command": command, "args": args}))
    response = json.loads(bpy.context.window_manager.atlas_result)
    if not response["ok"]:
        raise RuntimeError(response["error"]["message"])
    return response["result"]

print(atlas("frames.list"))
```

Read frame IDs, camera names, and job IDs from results. Online posing and generation require **Allow Online Access** and an API key in Atlas **Settings > Connection**. Local imports work offline.

## Import

```python
print(atlas("project.import", path="/absolute/path/to/project"))
```

A camera JSON path also works. Atlas prefers `cameras.json`, otherwise one unambiguous supported JSON. Manifests accept a camera list or a `frames`/`cameras` list containing calibration and local image paths. Depth and confidence can be explicit or companion files. Missing or ambiguous inputs produce errors; do not invent calibration.

### Import CLI results

A folder saved by `worldlabs operations download` imports once it has a `cameras.json` listing
its frames. The frames in `operation.json` already have the shape the importer reads:

```python
import json
from pathlib import Path

folder = Path("/absolute/path/to/views")
frames = json.loads((folder / "operation.json").read_text())["response"]["frames"]
(folder / "cameras.json").write_text(json.dumps({"frames": frames}))
print(atlas("project.import", path=str(folder)))
```

Each frame becomes a camera with its image and a point cloud, placed in Blender's Z-up world.
This needs no API key and no online access.

For unposed images of the same subject:

```python
print(atlas("pose", files=["/absolute/path/front.png", "/absolute/path/side.png"], mode="reconstruct"))
```

Use `mode="separate"` for independent images. Posing requests depth; imported depth creates point clouds parented to the cameras.

## Cameras

```python
made = atlas("camera.create", name="Target 01")              # also takes matrixWorld, or fromView=True
atlas("camera.set", name=made["cameraName"], matrixWorld=[[...], [...], [...], [0, 0, 0, 1]])
```

Both return `cameraName` and `matrixWorld`. `matrixWorld` is a Blender world matrix (Z-up). Pass
`coordinateSystem="api"` to `camera.set` to give an API camera-to-world matrix (Y-up) instead.
`camera.set` also takes `frameId` to move a frame's camera. A created camera has a 50 mm lens;
copy the lens of a posed camera to match its field of view. Ordinary Blender camera tools work
as well.

To send a Blender camera to the API yourself, convert its world pose from Blender's Z-up world
to the API's Y-up one: API x is Blender x, API y is Blender z, and API z is minus Blender y. The
camera's own axes are the same in both (right, up, back).

## Atlas and Chisel generation

Use actual target camera names from the scene:

```python
print(atlas("generate", targetNames=["Camera A", "Camera B"], prompt="Describe the subject", returnDepth=True))
print(atlas("chisel", targetNames=["Camera A", "Camera B"], prompt="Describe the scene", returnDepth=True))
```

These are alternatives: Atlas (`generate`) uses visible, depth-ready cameras as context; Chisel (`chisel`) uses scene geometry depth. Chisel needs at least two target positions for RGBD; one produces RGB only. Omit prompt and depth arguments to use the scene's Atlas settings.

## Splats

```python
print(atlas("splat"))
```

Usually gather at least 8 posed context images for a compact scene, and 16 or more for a larger
scene. Increase coverage with scene size; additional nearly identical views do not cover unseen
regions. Use visible, depth-ready images at the same resolution. The endpoint accepts two images,
but that is a technical lower limit, not the usual context target.

Splats are refined by default and are a final output: a run takes 15 to 25 minutes and costs
5,000 credits ($5). Check the context views first rather than running a draft to preview.
The result imports as a native Gaussian splat object saved in the `.blend`. `jobs.import` returns
`objectNames` for splats; image jobs return `frameIds`.

## Jobs

Submission returns `{"jobs": [...]}`; read each job's `id` and `state` from it. Let Blender's event loop run between calls; do not block it with a polling loop or sleep. Background scripts must call the loaded Atlas package's `tick()` to advance jobs because the UI timer does not run there; see [background](background.md).

```python
print(atlas("jobs.status"))
print(atlas("jobs.status", jobId="JOB_ID"))
print(atlas("jobs.import", jobId="JOB_ID"))  # Import a ready result.
```

A disconnected client does not cancel a submitted job. Check existing jobs before resubmitting. `jobs.cancel` and `jobs.resume` also take `jobId`.

## Images and points

```python
print(atlas("frames.inspect", frameId="FRAME_ID"))
bpy.ops.atlas.toggle_points()
```

Use native object selection, visibility, transforms, camera tools, and Blender save operations. Point visibility does not change Atlas context membership.
