# Run Atlas in background Blender

Atlas commands work in `blender --background`, with no window and no Blender MCP. This suits a
coding agent that drives Blender from a shell. The differences from an open session are below.

## Start Blender

```sh
WLT_API_KEY=... blender --background --online-mode --python script.py
```

- `--online-mode` allows online access for this run. Without it, posing and generation are
  refused unless **Allow Online Access** is already on in Preferences.
- Atlas uses the API key from its settings, or `WLT_API_KEY` from the environment when the
  settings hold none. Take the key from the environment; never ask for it in chat.
- Do not pass `--factory-startup`. It skips the preferences that enable Atlas, and
  `bpy.ops.atlas.command` does not exist.
- Pass a `.blend` path before `--python` to continue a saved scene.

## Advance jobs yourself

The timer that advances jobs runs only with a window. In background mode call the Atlas
package's `tick()` between status checks:

```python
import sys
import time

atlas_package = next(module for name, module in sys.modules.items() if name.split(".")[-1] == "worldlabs_atlas")

def wait(job_id, timeout=1800):
    deadline = time.time() + timeout
    while time.time() < deadline:
        atlas_package.tick()
        job = atlas("jobs.status", jobId=job_id)["jobs"][0]
        if job["state"] in ("ready", "failed", "cancelled", "paused"):
            return job
        time.sleep(2)
    raise TimeoutError(job_id)
```

`atlas` is the helper from [commands](commands.md). Sleeping is fine here because there is no
interface to block.

- A submission (`pose`, `generate`, `chisel`, `splat`) returns `{"jobs": [...]}`. Each job has
  `id`, `state`, `operationId`, `attached` and, when it failed, `error`.
- `tick()` imports a `ready` job's result into the active scene, after which the job reports
  `"attached": true`. Call `jobs.import` only for a ready job that is still unattached.
- Two jobs run at a time. Others stay `queued` until a slot frees on a later `tick()`.
- A stopped script does not cancel a submitted job. Save the `.blend` after submitting a long
  one, and in a later session check `jobs.status` before submitting again.

## What a script cannot assume

- **Camera names.** Imported and generated frames are camera objects named `Atlas image`,
  `Atlas image.001` and so on. Find a frame's camera from `frames.list`, which gives each
  frame's `id`, `label` (`Image 01`, `Generated 02`), `cameraName` and `matrixWorld`.
- **Target lenses.** `camera.create` makes a 50 mm camera. Copy `data.lens` from a posed camera
  to keep its field of view. Target cameras are always generated at 1280x720.
- **Coordinates.** Blender is Z-up; the API is Y-up. `camera.set` takes a Blender world matrix
  by default, or an API camera-to-world matrix with `coordinateSystem="api"`.
- **Prompt reuse.** After the first generation with prompt enhancement, Atlas stores the prompt
  it wrote in the scene and turns enhancement off, so later requests reuse it. Pass `prompt` or
  `enhancePrompt` to override.
- **Request size.** One `generate` call takes at most 128 views, context plus targets. A camera
  path longer than that needs the API directly; see the `atlas-flythrough` skill.
- **Files.** Until the scene is saved, frames and jobs live in Blender's user data folder under
  `datafiles/worldlabs_atlas/<scene id>`. Save the `.blend` to keep the scene; `cache.pack`
  then copies the Atlas files beside it.
