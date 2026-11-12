---
name: worldlabs-cli
description: Run World Labs Atlas API tasks from a terminal with the worldlabs CLI. Covers install and sign-in, uploading files, running a task from a JSON request, waiting for it, and downloading its outputs. Use for any Atlas job without a skill of its own, such as generating or editing an image, estimating camera and depth, or extracting a mesh, and for CLI setup and errors. New views of a scene belong to atlas-splats or atlas-flythrough. Also covers the connected World Labs tools when there is no shell.
license: Apache-2.0
compatibility: Needs Node.js 22 or newer and network access to api.atlas.worldlabs.ai.
---

# World Labs CLI

`worldlabs` runs Atlas API tasks. Every task works the same way: upload the files it needs, write
its request as JSON, run it, wait, and download what it made.

For a video or camera move use the `atlas-flythrough` skill, for a 3D scene as splats use
`atlas-splats`, and for work inside Blender use `atlas-blender`. New views of a place from an
image (other angles, the far side, more of the room) are building a scene, which is the first
part of both workflows: use either of those skills for them, even when the person has not yet
chosen a video or splats. This skill covers setup and every other task.

## Set up

```sh
npm install -g @worldlabsai/cli@latest
worldlabs auth status
```

If the status check reports no key, have the person run `worldlabs auth login` in their own
terminal and enter the key at its private prompt. Never ask for a key in chat or put one in a
command. Automation can set `WLT_API_KEY`. The key selects the API project and its billing. A
passing status check confirms asset access, not every task's permission.

The CLI needs network access. In a sandbox that blocks it, ask for approval instead of retrying.

## Run a task

```sh
worldlabs tasks list                                        # task names
worldlabs assets upload photo.jpg --json                    # note the "id"
worldlabs tasks run <task> --request request.json --wait --json > op.json
worldlabs operations download <operation-id> --out results
```

- **Request.** A request names an uploaded file as `{"assetId": "<id>"}`. Each task's fields are
  on its guide page, linked from https://docs.atlas.worldlabs.ai/task-overview.md. Read the page
  before writing a request; `https://docs.atlas.worldlabs.ai/llms.txt` lists every page.
- **Wait.** `--wait` stops waiting after 10 minutes unless `--timeout <seconds>` says otherwise.
  The task keeps running. Resume with `worldlabs operations wait <operation-id> --json`.
- **Retry.** `tasks run` prints an idempotency key. If a submission is interrupted, run it again
  with the same request and `--idempotency-key <key>` so the task is not started twice.
- **Result.** A finished operation has `response` or `error`; check `error` first.
  `operations download` saves every output file to a new directory, named for its place in the
  response (`frames_003_image.jpg`, `frames_003_depth.exr`), and writes `operation.json` with
  each file's local path. If the command is missing, update the CLI.
- **Errors.** The CLI does not print the API's reason. HTTP 422 means the request body was
  rejected: check it against the task's guide page. HTTP 402 means the project is out of credits
  or over its spend limit. HTTP 401 or 403 is the key or its permissions. An operation that ends
  `THROTTLED` hit a capacity limit, not a problem with the request: tell the person, wait a few
  minutes, and run it again. See https://docs.atlas.worldlabs.ai/errors.md

Tasks spend the project's credits. Run the tasks the request needs without quoting prices or
asking for a go-ahead; https://docs.atlas.worldlabs.ai/billing.md has the rates if the person
asks. Do not rerun a finished task to see whether the result changes.

## Without a shell

If World Labs tools are connected (`list_projects` and a tool per task, such as
`images2PosedRGBD`), they run the same tasks. A task's tool takes `project_id`,
`idempotency_key`, and `request`, the same request body the task's guide page gives.

- Pick a project from `list_projects` whose `available_tools` include the task; ask when several
  fit. If a tool reports that the sign-in has no Atlas account, ask the person to finish signing
  up at https://atlas.worldlabs.ai, then call the tool again.
- Get an image into the project first: `import_image` for a file attached in the chat, or
  `create_image_upload` and an HTTP PUT with exactly the returned `headers` for a local file.
  Never put image bytes in a tool argument.
- Reuse the same `idempotency_key` when retrying, and poll `get_operation` until `done`.
- Outputs are assets. Pass one to the next task by its `assetId`, and call `get_asset` for a
  fresh download link when one has expired.

With neither a shell nor connected tools, say that the task is unavailable here and that
installing the CLI or connecting World Labs makes it available.
