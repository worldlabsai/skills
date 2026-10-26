# World Labs

Create with Atlas APIs and tools.

Agent skills for the World Labs API and Atlas for Blender, packaged as one plugin for Codex and Claude Code.

| Skill | What it does |
| --- | --- |
| `worldlabs` | Generate and edit images, estimate cameras and depth, and manage API tasks and assets. |
| `atlas-blender` | Import calibrated projects, pose images, inspect point clouds, generate views, and create native Gaussian splats in Blender. |

## Install

### ChatGPT

Install World Labs from the ChatGPT plugin directory and connect your World Labs account. The hosted
connection estimates a camera and depth from an image. `python3 scripts/package_openai.py` builds
the submission ZIP with both repository skills and all their supporting files. The Atlas for Blender
skill requires a compatible local Blender environment; it cannot control Blender from a hosted chat
without that access. The ZIP does not install Blender, its extension, or the World Labs CLI.

### Codex

```sh
codex plugin marketplace add worldlabsai/skills
codex plugin add worldlabs@worldlabs
```

Start a new chat and invoke a skill, such as `$worldlabs:worldlabs` or `$worldlabs:atlas-blender`.

### Claude Code

```sh
claude plugin marketplace add worldlabsai/skills
claude plugin install worldlabs@worldlabs
```

Start a new session and invoke `/worldlabs:worldlabs` or `/worldlabs:atlas-blender`.

The plugin also adds the hosted World Labs MCP server. Run `/mcp`, select `worldlabs`, and sign in
with your World Labs account to estimate a camera and depth without an API key. The CLI covers the
other tasks.

### Claude

In Claude on the web or desktop, add a custom connector in **Settings > Connectors** with the URL
`https://api.atlas-beta.worldlabs.ai/mcp`, then sign in with your World Labs account. Claude in a
chat cannot upload a file you attach, so give it a public image URL to import.

## Set up the tools

### World Labs API

Install the CLI with Node.js 24 or newer:

```sh
npm install -g @worldlabsai/cli@0.1.0
worldlabs auth login
worldlabs tasks list --json
```

Enter your API key in the CLI's private prompt. Make sure `worldlabs` is available in the agent's
shell. Task availability depends on your account's access.

### Atlas for Blender

Atlas requires Blender 5.3+ and a separately installed Atlas extension. Blender MCP is strongly
recommended for agent access; Blender's Python Console, Text Editor, or background Python also work.
Gaussian splats require internal API access.

Install [Atlas 0.1.1](https://cdn.atlas-beta.worldlabs.ai/showcase/blender/worldlabs_atlas-0.1.1.zip)
for the Blender Python workflows in this skill. See [setup](skills/atlas-blender/references/setup.md)
for installation, checksums, and a read-only compatibility check.

## Try it

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
Both hosts share the same `skills/` content.

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
2. Submit `https://api.atlas-beta.worldlabs.ai/mcp` as an **MCP connector**, using the same
   organization that owns the World Labs plugin submission.
3. Keep the existing plugin submission pointed at the intended release branch containing
   `.mcp.json`. Check the portal's reviewed commit/version when updating a pending submission;
   pushing a PR does not update the tracked branch or confirm that reviewers have the new version.
4. Pair the connector and plugin listings in the portal. Keep the endpoint URL identical in the
   connector listing and `.mcp.json` so users who install both get one set of tools.

See [Anthropic's plugin and connector submission guidance](https://claude.com/docs/directory/publish#submit-your-plugin-and-your-mcp-server-as-a-connector)
and [connector review requirements](https://claude.com/docs/connectors/building/submission).
