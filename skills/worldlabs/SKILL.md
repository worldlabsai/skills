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

Use `worldlabs` for the Developer API. Requires Node 22+ and `@worldlabsai/cli`. If `worldlabs` is missing, locate the user-provided CLI executable or install `@worldlabsai/cli@0.3.0` with npm. Use the resolved executable consistently; do not assume plugin installation installs the CLI. Run `worldlabs --help` for command syntax and `worldlabs tasks list` for task names; account access can differ.

Read the documentation before submitting work. It is maintained with the API; where it differs from this skill, follow the documentation.

- [CLI](https://atlas-beta.worldlabs.ai/docs/cli): uploading assets, submitting request JSON, retrying with idempotency keys, waiting, and downloading results.
- [How to use Atlas](https://atlas-beta.worldlabs.ai/docs/how-to-use-atlas): which task fits, scene data, cameras and depth, and chaining tasks. Follow its links for each task's fields.
- [Generate a video or camera path](https://atlas-beta.worldlabs.ai/docs/atlas-generate#generate-a-video-or-camera-path): read before any video or flythrough.
- [Splat best practices](https://atlas-beta.worldlabs.ai/docs/splat-best-practices): read before `posedImages2Splats`.

A `posedImages2Splats` run usually takes about 20 minutes, longer than the CLI's default 600-second timeout: pass `--timeout 3600` with `--wait`, or resume with `worldlabs operations wait <operation-id> --timeout 3600 --json`.

### Authentication

Check `worldlabs auth status`. If login is needed, have the user run `worldlabs auth login` in their own terminal and enter the key privately. Never request keys in chat or put them in command arguments. Automation can supply `WLT_API_KEY`. The key selects the API project and billing; a successful status check verifies asset access, not every task permission.
