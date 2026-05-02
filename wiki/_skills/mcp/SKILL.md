---
name: mcporter
description: Use the mcporter CLI to list, configure, auth, and call MCP servers/tools directly (HTTP or stdio), including ad-hoc servers, config edits, and CLI/type generation.
version: 1.0.0
author: community
license: MIT
metadata:
  hermes:
    tags: [MCP, Tools, API, Integrations, Interop]
    homepage: https://mcporter.dev
prerequisites:
  commands: [npx]
---

# mcporter

Use `mcporter` to discover, call, and manage [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) servers and tools directly from the terminal.

## Prerequisites

Requires Node.js:
```bash
# No install needed (runs via npx)
npx mcporter list

# Or install globally
npm install -g mcporter
```

## Quick Start

```bash
# List MCP servers already configured on this machine
mcporter list

# List tools for a specific server with schema details
mcporter list <server> --schema

# Call a tool
mcporter call <server.tool> key=value
```

## Discovering MCP Servers

mcporter auto-discovers servers configured by other MCP clients (Claude Desktop, Cursor, etc.) on the machine. To find new servers to use, browse registries like [mcpfinder.dev](https://mcpfinder.dev) or [mcp.so](https://mcp.so), then connect ad-hoc:

```bash
# Connect to any MCP server by URL (no config needed)
mcporter list --http-url https://some-mcp-server.com --name my_server

# Or run a stdio server on the fly
mcporter list --stdio "npx -y @modelcontextprotocol/server-filesystem" --name fs
```

## Calling Tools

```bash
# Key=value syntax (NO quotes around value)
mcporter call <server>.<tool> key=value key2=value2

# Stdio server — MUST use --name to distinguish instance
mcporter call --stdio "npx -y @playwright/..."
mcporter call <server.tool> key=value --output json
```

## Auth and Config

```bash
# OAuth login for a server
mcporter auth <server | url> [--reset]

# Manage config
mcporter config list
mcporter config get <key>
mcporter config add <server>
mcporter config remove <server>
mcporter config import <path>
```

Config file location: `./config/mcporter.json` (override with `--config`).

## Daemon

For persistent server connections:
```bash
mcporter daemon start
mcporter daemon status
mcporter daemon stop
mcporter daemon restart
```

## Code Generation

```bash
# Generate a CLI wrapper for an MCP server
mcporter generate-cli --server <name>
mcporter generate-cli --command <url>

# Inspect a generated CLI
mcporter inspect-cli <path> [--json]

# Generate TypeScript types/client
mcporter emit-ts <server> --mode client
mcporter emit-ts <server> --mode types
```

## Notes
## Playwright MCP (`@playwright/mcp`) — real browser automation
```bash
# Install Chrome first: npx playwright install chrome

# Navigate + inspect (each mcporter call spawns a new server — no page state persistence)
mcporter call --stdio "npx -y @playwright/..." browser_navigate url=http://example.com

# Get snapshot (run after navigate in same command chain)
mcporter call --stdio "npx -y @playwright/..." browser_navigate url=http://example.com && mcporter call --stdio "npx -y @playwright/..." browser_snapshot

# Screenshot: save to ~/.hermes/hermes-agent/.playwright-mcp/ dir (allowed root)
mcporter call --stdio "npx -y @playwright/..." browser_evaluate code="page. goto('http://example.com')" && mcporter call --stdio "npx -y @playwright/..." browser_take_screenshot filename=.playwright-mcp/screen.png

# List available tools
mcporter list --stdio "npx -y @playwright/..." --name pw
```
NOTE: `@executeautomation/playwright-mcp-server` has better tooling but requires `--allow-unrestricted-file-access`. Use `@playwright/mcp` from the official Playwright org.
## Notes
