# World Labs

Create with Atlas APIs and tools.

Agent skills for World Labs Atlas, packaged as one plugin for Codex and Claude Code.

| Skill | What it does |
| --- | --- |
| `atlas-flythrough` | Make a camera-move video through a scene from one or more images. |
| `atlas-splats` | Turn one or more images into a 3D scene as Gaussian splats. |
| `atlas-blender` | See and shape Atlas scenes in Blender: posed images as cameras and point clouds, a camera path on the timeline, native splats. The Atlas add-on is optional. |
| `worldlabs-cli` | Set up the World Labs CLI and run any other Atlas API task with it. |

## How the skills are built

Edit the skills from these ideas. When a session shows a problem, find which idea the text
failed to carry and fix that, instead of appending a rule.

- **The person directs; the agent does the work.** Where the work happens, what the result
  should be, and when to spend on the long step are the person's decisions. Asking is the
  default: the agent asks each in one line, and decides for itself only when the person says
  outright not to ask. Even then it chooses what the person would most likely choose.
- **Blender is the preferred place** when it is installed, because both of them can see the
  scene in 3D. The Atlas add-on is optional.
- **Build the scene first, then make things from it.** The scene is explored outward in rounds
  of a few views, each placed from what the last revealed, before any video or reconstruction. The path or the splats come from the scene,
  and each result is looked at before it is handed over.
- **Say what good looks like.** The skills describe a good path or a good set of views and leave
  the camera placement to the agent. Code appears only for calls to our own tools.
- **Hand over things the person can use:** the video or splats, the project file, and what the
  model invented.
- **Method and place are separate.** `atlas-flythrough` and `atlas-splats` hold the method.
  `atlas-blender` and `worldlabs-cli` hold how to do it in one place. Each skill is complete
  without the others, so the two method skills carry identical copies of their shared material;
  see [Development](#development).

## Install

### ChatGPT

Install World Labs from the ChatGPT plugin directory and connect your World Labs account. The hosted
connection runs the Atlas tasks: generating images and views, estimating cameras and depth,
reconstructing Gaussian splats, and extracting meshes. The plugin carries every skill in this
repository and its supporting files. The video, splats and CLI skills are written for a shell
with the World Labs CLI, and the Atlas for Blender skill requires a compatible local Blender
environment; a hosted chat without that access uses the connected tools. The plugin does not
install Blender, its extension, or the World Labs CLI.

### Codex

```sh
codex plugin marketplace add worldlabsai/skills
codex plugin add worldlabs@worldlabs
```

Start a new chat and invoke a skill, such as `$worldlabs:atlas-flythrough` or `$worldlabs:atlas-blender`.

### Claude Code

```sh
claude plugin marketplace add worldlabsai/skills
claude plugin install worldlabs@worldlabs
```

Start a new session and invoke `/worldlabs:atlas-flythrough`, `/worldlabs:atlas-splats`,
`/worldlabs:atlas-blender` or `/worldlabs:worldlabs-cli`.

The plugin also adds the hosted World Labs MCP server. Run `/mcp`, select `worldlabs`, and sign in
with your World Labs account to run the same tasks as the CLI without an API key.

### Other agents

With the World Labs CLI installed, `worldlabs skills install` installs every skill in this
repository for the agents it detects, through [Skills CLI](https://skills.sh). Pass
`--client <agent>` to choose one.

### Claude

In Claude on the web or desktop, add a custom connector in **Settings > Connectors** with the URL
`https://api.atlas.worldlabs.ai/mcp`, then sign in with your World Labs account. Claude in a
chat cannot upload a file you attach, so give it a public image URL to import.

## Set up the tools

### World Labs API

Install the CLI with Node.js 22 or newer:

```sh
npm install -g @worldlabsai/cli@latest
worldlabs auth login
worldlabs tasks list --json
```

Enter your API key in the CLI's private prompt. Make sure `worldlabs` is available in the agent's
shell. The video skill also needs `ffmpeg`.

### Atlas for Blender

Atlas requires Blender 5.3+. Three separate pieces
are involved, and this plugin installs none of them:

1. The Blender MCP add-on, installed inside Blender.
2. The Blender MCP server or connector, configured in your agent client. In Claude Desktop, add
   **Customize > Connectors > Blender > Add**; Claude's Blender connector uses the same
   Blender-developed MCP implementation. For other clients, see
   [Blender's MCP setup](https://www.blender.org/lab/mcp-server/).
3. The Atlas add-on, installed separately inside Blender. The `atlas-blender` skill tells the agent
   how to use it.

Blender MCP is the recommended way for an agent to work in Blender, and the skill offers to install
and configure it when it is missing. It is not strictly required: the Atlas commands also run
through Blender's Python Console, Text Editor, or command line. If Blender MCP already works with your agent, you only need
the Atlas add-on and this skill.

Install [Atlas 0.1.4](https://cdn.atlas.worldlabs.ai/showcase/blender/worldlabs_atlas-0.1.4.zip)
for the Blender Python workflows in this skill. See [setup](skills/atlas-blender/references/setup.md)
for installation, checksums, and a read-only compatibility check.

## Try it

- “Make a video that moves into the room in this photo and circles the table.”
- “Turn this photo into a 3D scene I can look around in.”
- “List the tasks available through the World Labs API.”
- “Find my open Atlas Blender session and inspect its frames without changing anything.”
- “Import this calibrated Atlas project and inspect its cameras and point clouds.”

## Development

Clone this repository and load it locally:

```sh
git clone https://github.com/worldlabsai/skills.git
cd skills
```

For Codex, register the checkout with `codex plugin marketplace add "$PWD"`, then install
`worldlabs@worldlabs`. After edits, remove and reinstall the plugin to refresh its cached copy.
For Claude Code, run `claude --plugin-dir "$PWD"` and restart the session after edits.

Validate the plugin metadata with `claude plugin validate --strict .`.

Use the [test scenarios](tests/scenarios.md) to check skill selection and tool behavior.
Both hosts share the same `skills/` content. Each workflow skill also has test cases in its
`evals/evals.json`, in the [Agent Skills](https://agentskills.io/skill-creation/evaluating-skills)
format.

The Agent Skills format has no way to share files between skills, and a skill can be installed
alone. `atlas-flythrough` and `atlas-splats` therefore each hold a copy of
`references/scene.md`, `references/conventions.md` and the first files of `assets/example/`.
Edit one copy, then copy it over the other. This prints nothing when they match:

```sh
for f in references/scene.md references/conventions.md assets/example/pose-request.json \
  assets/example/pose-result.json assets/example/round-1-request.json \
  assets/example/round-2-request.json assets/example/round-3-request.json assets/example/views.jpg; do
  cmp "skills/atlas-flythrough/$f" "skills/atlas-splats/$f"
done
```

## License

Copyright 2026 World Labs Technologies, Inc.

The skills and helper code in this repository are licensed under [Apache-2.0](LICENSE).
World Labs names and logos remain trademarks of their respective owners. The World Labs API
and separately distributed Blender add-on are governed by their own terms and licenses.

## Publish to the Claude directory

The plugin bundle and the hosted MCP connector are separate submissions in
[Anthropic's developer portal](https://claude.ai/directory/manage). A plugin submission does not
submit its referenced MCP server for a connector listing. The connector can be submitted while
the plugin is under review; plugin approval or publication is not a prerequisite.

1. Test the hosted endpoint as a custom Claude connector, including sign-in and each tool, before
   submitting it for review.
2. Submit `https://api.atlas.worldlabs.ai/mcp` as an **MCP connector**, using the same
   organization that owns the World Labs plugin submission.
3. Keep the existing plugin submission pointed at the intended release branch containing
   `.mcp.json`. Check the portal's reviewed commit/version when updating a pending submission;
   pushing a PR does not update the tracked branch or confirm that reviewers have the new version.
4. Pair the connector and plugin listings in the portal. Keep the endpoint URL identical in the
   connector listing and `.mcp.json` so users who install both get one set of tools.

See [Anthropic's plugin and connector submission guidance](https://claude.com/docs/directory/publish#submit-your-plugin-and-your-mcp-server-as-a-connector)
and [connector review requirements](https://claude.com/docs/connectors/building/submission).
