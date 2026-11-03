# Connecting the tools

Jade uses tools already authenticated in the client. The package includes no credentials and does not connect accounts automatically. Reusing existing connectors avoids duplicate configuration.

## Jira and Confluence in Claude Code

If Atlassian is not configured yet, add the official server:

```bash
claude mcp add --transport http atlassian https://mcp.atlassian.com/v2/mcp
```

Open `/mcp` in Claude Code and complete authentication. The available operations depend on the account, the site and the organization's policies. Jade must check the exposed tools and read the ticket/page before claiming access.

## GitHub

Use the already authenticated connector/MCP or an authenticated GitHub CLI (`gh`). The alternative in `.mcp.example.json` uses the official remote server and the `JADE_GITHUB_PAT` variable; provide the secret through the environment's secure mechanism, never inside the versioned file or a prompt.

If you choose the example, merge only the needed entry into the existing configuration and check the connection in `/mcp`. The installer writes `.mcp.jade.example.json` and does not replace `.mcp.json`.

## Back-end repository and Figma

Give the authorized back-end repo/path in `jade.project.json` or in the request. If it is outside the directory allowed by the client, grant access through the client's own mechanism. Jade does not bypass the restriction.

For Figma, reuse the already connected official MCP and provide a URL with a node-id. The
tool must expose the needed design context; parameters must
follow the schema actually available. If the server is not connected yet,
add it (the `figma` entry is also in `.mcp.example.json`):

```bash
claude mcp add --transport http figma https://mcp.figma.com/mcp
```

Open `/mcp` and complete OAuth authentication. While `get_design_context` is not
exposed and authenticated, `jade-figma-to-code` records `BLOCKED` on the
visual step and does not recreate the screen from memory.

## OpenSpec

Jade always runs with OpenSpec. Install the CLI and initialize the project:

```bash
npm install -g @fission-ai/openspec@latest
openspec init
```

`openspec init` generates the slash commands for your tool (`/opsx:propose`, `/opsx:apply`, etc.). Without the CLI, Jade writes the artifacts by hand and marks `openspec validate` as `NOT RUN`.

## Project configuration

Copy `jade.project.example.json` to `jade.project.json` and fill in only the known fields. Empty fields mean unknown; they are not fake contracts or endpoints. Do not fill in tokens, cookies, passwords or customer payloads.

URLs identify resources; they do not authorize writes or make an undeployed API available. In each task, check the consulted commit and the environment evidence.

## Official sources consulted

- https://code.claude.com/docs/en/mcp
- https://code.claude.com/docs/en/sub-agents#preload-skills-into-subagents
- https://support.atlassian.com/atlassian-ai-gateway/docs/get-started-with-the-atlassian-remote-mcp-server/
- https://github.com/Fission-AI/OpenSpec/blob/main/docs/installation.md
- https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md
