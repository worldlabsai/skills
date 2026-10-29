# Test scenarios

Run each prompt in a fresh Codex or Claude Code session with the plugin loaded. Record the host
version, selected skill, and observed result. Keep API and Blender checks separate.

| Scenario | Prompt | Expected observation |
| --- | --- | --- |
| API discovery | Use the World Labs API skill to list the available tasks. Do not submit requests or upload files. | Runs CLI task discovery; reports actual task names. Missing executable or Node is reported with setup steps. |
| Authentication | Check whether the World Labs CLI is authenticated. Do not log in or change credentials. | Runs `auth status`; reports configured access or missing authentication without revealing a key. |
| Blender setup | Help me set up Atlas in Blender. | Requires Blender 5.3+. Separates the Blender MCP add-on, the Blender MCP connector in the agent client (Customize > Connectors > Blender in Claude Desktop, Blender's MCP setup elsewhere) and the Atlas add-on; says the plugin installs none of them and that MCP is optional. Explains Atlas 0.1.2 GUI installation and API settings. |
| Blender discovery | Use the Atlas Blender skill to inspect frames in my open scene without changing anything. | Checks for `bpy.ops.atlas.command`, calls `frames.list`, and reports returned frames or a clear error. It does not assume a connected session. |
| Import and pose | Import this camera/image/depth project into Blender and inspect the result. | Uses `project.import` for calibrated exports, preserving their poses; uses `pose` only for unposed images and reports job status without blocking Blender's event loop. |
| Scene placement | Arrange these independently posed images into a coherent scene. | Reads scene-placement concepts, chooses its own placement and inspection methods, and may toggle point clouds or inspect camera views. Does not require a numerical alignment procedure. |
| Atlas generation | Generate views from the visible Atlas cameras in this scene. | Calls normal generation Atlas and depth-conditioned generation Chisel; uses actual camera names and reports online access or API errors clearly. |
| Gaussian splat | Create a native Gaussian splat from my Atlas context images. | Checks Blender 5.3+, Atlas 0.1.2 and Marble 2 beta access. Usually gathers at least 8 context views for a compact scene and 16 or more for a larger scene, with usable depth and matching resolution; distinguishes this guidance from the endpoint's two-image lower limit. |

## ChatGPT (hosted tools)

Use a dedicated review account with Developer API beta access and credits. Connect World Labs from
the plugin, then run each prompt in a new chat with an image of a room attached.

| Scenario | Prompt | Expected observation |
| --- | --- | --- |
| Connect | Show me which World Labs projects I can use. | Sign-in and consent complete in the browser; `list_projects` returns the account's projects with `estimate_camera_depth` available. No key is requested in chat. |
| Estimate | Estimate the camera and depth for this photo. | `import_image`, then the project and credit use are named before `estimate_camera_depth`; `get_operation` polls to done and reports the camera, depth-grid size, and download links. |
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
| Upload | Estimate the camera and depth for `room.jpg`. | `create_image_upload` with the file's type and size, one `curl` PUT to `upload_url`, then `estimate_camera_depth` on the returned asset. The image bytes never appear in a tool argument. |
| Mislabeled file | Estimate the camera and depth for `notes.txt` renamed to `notes.jpg`. | The estimate is refused as not a decodable image; no operation starts. |
