---
name: worldlabs
description: Generate and edit scene images, estimate cameras and depth, reconstruct Gaussian splats, or extract meshes with World Labs, through its connected tools or its CLI.
license: Apache-2.0
---

# World Labs

## Choose a path

- If World Labs tools are connected (`list_projects`, `import_image`, `create_image_upload`, `estimate_camera_depth`, `get_operation`, `get_asset`), use them to estimate a camera and depth from one image. The connected tools cover only this task.
  - Pick a project from `list_projects` whose `available_tools` include `estimate_camera_depth`; ask when several fit.
  - Get the image into that project. For a file attached in the chat, call `import_image`. For a local file, call `create_image_upload` with its type and exact size, upload the bytes to `upload_url` with an HTTP PUT that sends exactly the returned `headers` (for example `curl -X PUT -H 'content-type: image/jpeg' --upload-file photo.jpg '<upload_url>'`), and use the returned `asset_id`. Never put image bytes in a tool argument.
  - Before estimating, name the project and say the task uses its World Labs Developer API credits. Reuse the same `idempotency_key` when retrying, and poll `get_operation` until `done`.
- With a local shell, use the CLI below for tasks the connected tools do not cover, or for every task when they are not connected.
- With neither, say which task the user wants is unavailable here, and that connecting World Labs or installing the CLI makes it available.

## Use the CLI

Use `worldlabs` for the Developer API. The examples use a POSIX shell. Requires Node 22+ and `@worldlabsai/cli`. If `worldlabs` is missing, locate the user-provided CLI executable or install `@worldlabsai/cli@0.3.0` with npm. Use the resolved executable consistently; do not assume plugin installation installs the CLI. Run `worldlabs --help` for command syntax.

### Choose a task

| Task | Purpose |
| --- | --- |
| `atlasTextToImage` | Generate starting images from a description of an environment. |
| `images2PosedRGBD` | Estimate cameras and depth from images of a scene. |
| `atlasGenerate` | Generate new viewpoints using posed RGBD context. |
| `atlasChisel` | Generate posed images from a prompt and optional depth layouts. |
| `atlasMasked` | Fill masked regions across posed images. |
| `posedImages2Splats` | Reconstruct refined Gaussian splats from posed RGBD images. |
| `splats2Mesh` | Extract a mesh from a Gaussian splat scene. |

Read [How To Use Atlas](https://marble5.worldlabs.ai/docs/how-to-use-atlas) before choosing model inputs, calculating cameras, or chaining tasks. It explains scene data, model behavior, and the requirements that affect results. Follow its task or camera links when you need exact fields or geometry calculations. `worldlabs tasks list` reports SDK task names; account access can differ.

For videos and flythroughs, read [Generate a video or camera path](https://marble5.worldlabs.ai/docs/atlas-generate#generate-a-video-or-camera-path) before submitting. Keep the complete ordered trajectory in one `atlasGenerate` request so Atlas can share generated context across the sequence. Do not independently batch frames or splice preview outputs into the final sequence; reusing a seed does not preserve continuity across separate requests.

For `posedImages2Splats`, give every frame its depth (`depth.depthAsset`, as `images2PosedRGBD` returns), and prefer at least 8 frames for a compact scene and 16 or more for a larger one. A run usually takes about 20 minutes, longer than the CLI's default 600-second timeout: pass `--timeout 3600` with `--wait`, or resume with `worldlabs operations wait <operation-id> --timeout 3600 --json`. The response's `refinedSplats` maps splat counts to SPZ assets.

### Submit and inspect

Upload a local image:

```sh
worldlabs assets upload photo.jpg --json > asset.json
```

Write `request.json` as `{"frames":[{"imageAsset":{"assetId":"<id>"}}]}`, replacing `<id>` with the uploaded asset's `id` from `asset.json`.

```sh
worldlabs tasks run images2PosedRGBD --request request.json --wait --json > result.json
```

Use `--request -` to read JSON from stdin. Results go to stdout; diagnostics and the submission's idempotency key go to stderr. Preserve the key and reuse it with `--idempotency-key <key>` and the same request if submission is interrupted.

A timeout stops local waiting, not server work. Resume with `worldlabs operations wait <operation-id> --json`. Check a completed operation's `error` before reading `response`. Download returned assets with `worldlabs assets download <asset-id> --out result.png`. Inspect the outputs before using them in another task; keep each image, camera, depth, and confidence together.

### Authentication

Check `worldlabs auth status`. If login is needed, have the user run `worldlabs auth login` in their own terminal and enter the key privately. Never request keys in chat or put them in command arguments. Automation can supply `WLT_API_KEY`. The key selects the API project and billing; a successful status check verifies asset access, not every task permission.
