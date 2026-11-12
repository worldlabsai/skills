# Test scenarios

Run each prompt in a fresh Codex or Claude Code session with the plugin loaded. Record the host
version, selected skill, and observed result. Keep API and Blender checks separate.

| Scenario | Prompt | Expected observation |
| --- | --- | --- |
| API discovery | List the tasks available through the World Labs API. Do not submit requests or upload files. | Selects `worldlabs-cli`; runs CLI task discovery and reports actual task names. Missing executable or Node is reported with setup steps. |
| Authentication | Check whether the World Labs CLI is authenticated. Do not log in or change credentials. | Selects `worldlabs-cli`; runs `auth status` and reports configured access or missing authentication without revealing a key. |
| Other task | Remove the lamp from `room.jpg`. | Selects `worldlabs-cli`, not a workflow skill; reads the task's guide page before writing the request. |
| Video | Make a video that goes into the room in `room.jpg` and circles the table. | Selects `atlas-flythrough`. Poses the image, generates about 6 to 12 views around the table in one request with depth, and shows them with the cost of the next step before generating the path. Sends the whole path as one `atlasGenerate` request with those views as context, and assembles the frames with `ffmpeg`. |
| Video, open ask | Make a flythrough of the room in `room.jpg`. | Selects `atlas-flythrough`. The path travels through the room and ends on a different view; the camera does not hover near the source image. |
| Video, one go | Make a 4-second push into `room.jpg`. Don't check in, just deliver it. | Selects `atlas-flythrough`. Does not ask for confirmation. One request for the whole path; reports what the model invented. |
| Splats | Turn `room.jpg` into a 3D scene I can look around in. | Selects `atlas-splats`. Poses the image, generates views around the main part of the scene, and shows them with the cost and wait before reconstruction. Submits `posedImages2Splats` once, refined, without `--wait`; runs no draft. Reports the SPZ file. |
| Video, chat only | (connected tools, no shell) Make a video that circles the table in this photo. | Poses the image and generates a few views to show, then says the video itself needs a coding agent with a shell, or Blender. Does not try to pass a long camera path through a tool call. |
| Blender available | (Blender open with the Atlas add-on) Turn `room.jpg` into a 3D scene. | Uses `atlas-blender` for posing, placing cameras and the reconstruction; does not offer to install anything. |
| Blender installed, not connected | (Blender installed, no Blender tools connected) Make a flythrough of `room.jpg`. | Checks for Blender before posing and asks whether to set up the missing piece or work in the background. Does not silently pick the shell, and does not require the Atlas add-on to use Blender as the 3D view. |
| Plain ask | (Blender installed) Make me a flythrough. | Treats this as an ordinary request, not as permission to skip questions: its first message asks where to work. |
| Blender fully set up | (Blender, Blender tools and the Atlas add-on all present) Make a flythrough of `room.jpg`. | Asks whether to work in an open Blender window or in the background. Delivers the `.blend` with the MP4. The file opens on frame 1 with the timeline set to the shot, a keyframed camera with Motion Paths, the camera view beside an overview, coloured points, and no marker geometry visible through the lens. |
| Video and splats | Make splats from `room.jpg`, then a video orbiting the table. | Poses once and generates one set of views; both the reconstruction and the video use them. |
| Blender setup | Help me set up Atlas in Blender. | Requires Blender 5.3+. Separates the Blender MCP add-on, the Blender MCP connector in the agent client (Customize > Connectors > Blender in Claude Desktop, Blender's MCP setup elsewhere) and the Atlas add-on; says the plugin installs none of them, recommends Blender MCP, and asks whether to install and configure it when it is missing. Explains Atlas 0.1.4 GUI installation and API settings. |
| Blender discovery | Use the Atlas Blender skill to inspect frames in my open scene without changing anything. | Checks for `bpy.ops.atlas.command`, calls `frames.list`, and reports returned frames or a clear error. It does not assume a connected session. |
| Import and pose | Import this camera/image/depth project into Blender and inspect the result. | Uses `project.import` for calibrated exports, preserving their poses; uses `pose` only for unposed images and reports job status without blocking Blender's event loop. |
| Scene placement | Arrange these independently posed images into a coherent scene. | Reads scene-placement concepts, chooses its own placement and inspection methods, and may toggle point clouds or inspect camera views. Does not require a numerical alignment procedure. |
| Atlas generation | Generate views from the visible Atlas cameras in this scene. | Calls normal generation Atlas and depth-conditioned generation Chisel; uses actual camera names and reports online access or API errors clearly. |
| Gaussian splat | Create a native Gaussian splat from my Atlas context images. | Checks Blender 5.3+ and Atlas 0.1.4. Usually gathers at least 8 context views for a compact scene and 16 or more for a larger scene, with usable depth and matching resolution; distinguishes this guidance from the endpoint's two-image lower limit. Runs one refined reconstruction and no draft. |
| Background Blender | (shell, no open Blender session) Pose `room.jpg` in Blender and generate two views beside it. | Starts Blender with `--background --online-mode` and without `--factory-startup`; advances jobs with the Atlas package's `tick()`; reads job IDs from the `jobs` list; finds generated cameras through `frames.list`. |

## ChatGPT (hosted tools)

Use a dedicated review account with Developer API credits. Connect World Labs from
the plugin, then run each prompt in a new chat with an image of a room attached.

| Scenario | Prompt | Expected observation |
| --- | --- | --- |
| Connect | Show me which World Labs projects I can use. | Sign-in and consent complete in the browser; `list_projects` returns the account's projects, each with the task tools it can run in `available_tools`. No key is requested in chat. |
| Estimate | Estimate the camera and depth for this photo. | `import_image`, then the project and credit use are named before `images2PosedRGBD`; `get_operation` polls to done and reports the camera, depth-grid size, and download links. |
| Generate | (no attachment) Generate an image of a sunlit reading room. | The project and credit use are named before `atlasTextToImage`; `get_operation` polls to done and reports the image's download link. |
| Chain | (after Generate) Estimate the camera and depth for that image. | `images2PosedRGBD` names the generated image by its `assetId`; nothing is uploaded or imported again. |
| Resume | (new chat) Check on operation `<id>` in project `<project>`. | `get_operation` returns the same operation; nothing is resubmitted. |
| Retry | Estimate again with the same request after a dropped response. | The repeated call with the same `idempotency_key` returns the original operation; one charge. |
| Expired link | Give me the depth file again. | `get_asset` returns a new download link with a later `expires_at`. |
| Reconnect | (after revoking the grant, once the current access token has expired) List my projects. | The token refresh is refused and the tool asks to reconnect; no account data is shown. A revoked grant keeps working until its access token expires. |
| Other project | Read operation `<id>` from a project the account cannot access. | Not found; the operation's existence is not revealed. |
| No credits | (account with billing blocked) Estimate the camera and depth for this photo. | Refused with the billing message; no operation starts and no purchase flow is offered. |

## Codex and Claude Code (hosted tools, local file)

Use the same review account and a room photo in the working directory. Connect World Labs in
Codex, or in Claude Code through `/mcp` after installing the plugin. Run each scenario in both.

| Scenario | Prompt | Expected observation |
| --- | --- | --- |
| Upload | Estimate the camera and depth for `room.jpg`. | `create_image_upload` with the file's type and size, one `curl` PUT to `upload_url`, then `images2PosedRGBD` on the returned asset. The image bytes never appear in a tool argument. |
| Mislabeled file | Estimate the camera and depth for `notes.txt` renamed to `notes.jpg`. | The estimate is refused as not a decodable image; no operation starts. |
