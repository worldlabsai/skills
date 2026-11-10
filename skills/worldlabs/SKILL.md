---
name: worldlabs
description: Generate and edit scene images, estimate cameras and depth, reconstruct Gaussian splats, or extract meshes with World Labs, through its connected tools or its CLI.
license: Apache-2.0
---

# World Labs

## Choose a path

- If World Labs tools are connected (`list_projects` and a tool per task, such as `images2PosedRGBD` or `atlasGenerate`), use them. A task's tool has the task's name and takes `project_id`, `idempotency_key`, and `request`, the request body the documentation gives for that task.
  - Pick a project from `list_projects` whose `available_tools` include the task; ask when several fit.
  - If a tool reports that the sign-in has no Atlas account, ask the user to open https://atlas.worldlabs.ai and finish signing up, then call the tool again. Connecting does not create the account; reconnecting is not needed.
  - Get an image into that project before a task needs it. For a file attached in the chat, call `import_image`. For a local file, call `create_image_upload` with its type and exact size, upload the bytes to `upload_url` with an HTTP PUT that sends exactly the returned `headers` (for example `curl -X PUT -H 'content-type: image/jpeg' --upload-file photo.jpg '<upload_url>'`), and use the returned `asset_id`. A request names media as `{"assetId": "<id>"}`, or as `{"url": "<url>"}` for a public file. Never put image bytes in a tool argument.
  - Before starting a task, name the project and say the task uses its World Labs Developer API credits. Reuse the same `idempotency_key` when retrying, and poll `get_operation` until `done`.
  - A task's outputs are assets. Pass one to the next task by its `assetId`, and call `get_asset` for a fresh download link when one has expired.
- With a local shell and no connected tools, use the CLI below.
- With neither, say which task the user wants is unavailable here, and that connecting World Labs or installing the CLI makes it available.

## Read the documentation first

Read the documentation before submitting work on either path. It is maintained with the API; where it differs from this skill, follow the documentation.

- [How to use Atlas](https://docs.atlas.worldlabs.ai/how-to-use-atlas): which task fits, scene data, cameras and depth, and chaining tasks. Follow its links for each task's fields.
- [Generate a video or camera path](https://docs.atlas.worldlabs.ai/atlas-generate#generate-a-video-or-camera-path): read before any video or flythrough.
- [Splat best practices](https://docs.atlas.worldlabs.ai/splat-best-practices): read before `posedImages2Splats`.

A `posedImages2Splats` run usually takes 10 to 20 minutes. Keep the operation ID and check on it until it is done, with `get_operation` or `worldlabs operations wait <operation-id> --json`. Don't resubmit while it runs.

## Use the CLI

Use `worldlabs` for the Developer API. Requires Node 22+ and `@worldlabsai/cli`. If `worldlabs` is missing, locate the user-provided CLI executable or install `@worldlabsai/cli@latest` with npm. Use the resolved executable consistently; do not assume plugin installation installs the CLI. Run `worldlabs --help` for command syntax and `worldlabs tasks list` for task names.

The [CLI](https://docs.atlas.worldlabs.ai/cli) guide covers uploading assets, submitting request JSON, retrying with idempotency keys, waiting, and downloading results. Submit a `posedImages2Splats` run without `--wait`.

### Authentication

Check `worldlabs auth status`. If login is needed, have the user run `worldlabs auth login` in their own terminal and enter the key privately. Never request keys in chat or put them in command arguments. Automation can supply `WLT_API_KEY`. The key selects the API project and billing; a successful status check verifies asset access, not every task permission.
