# toggl-track-mcp

[![PyPI version](https://img.shields.io/pypi/v/toggl-track-mcp)](https://pypi.org/project/toggl-track-mcp/)
[![Python](https://img.shields.io/pypi/pyversions/toggl-track-mcp)](https://pypi.org/project/toggl-track-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server for [Toggl Track](https://toggl.com/track/) — the popular time tracking tool.

This server gives AI assistants (Claude Desktop, Claude Code, Cursor, etc.) full control over your Toggl Track account: start/stop timers, manage projects, clients, tags, tasks, and pull reports — all through natural language.

**35 tools** covering every Toggl Track entity with full create, read, update, and delete support.

## Prerequisites

- **Python 3.10+**
- **[uv](https://docs.astral.sh/uv/)** package manager (recommended) or pip
- **Toggl Track account** with an API token

### Getting Your API Token

1. Log in to [Toggl Track](https://track.toggl.com/)
2. Go to your **Profile** (click avatar bottom-left > Profile Settings)
3. Scroll to the bottom — your **API Token** is there
4. Copy it — you'll need it in the next step

## Installation

### Option A: pip install from PyPI (recommended)

```bash
pip install toggl-track-mcp
```

### Option B: Run directly with uvx (no install needed)

```bash
uvx toggl-track-mcp
```

### Option C: Install from GitHub (latest)

```bash
pip install git+https://github.com/dovahkaal/TogglTrackMcp.git
```

### Option D: Clone and install locally (for development)

```bash
git clone https://github.com/dovahkaal/TogglTrackMcp.git
cd TogglTrackMcp
uv sync
```

## Configuration

The server needs one environment variable:

| Variable | Required | Description |
|----------|----------|-------------|
| `TOGGL_API_TOKEN` | Yes | Your Toggl Track API token |
| `TOGGL_WORKSPACE_ID` | No | Default workspace ID. If not set, auto-detects from your Toggl profile |

### Claude Desktop

Add this to your `claude_desktop_config.json`:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

#### Using PyPI install (simplest)

```json
{
  "mcpServers": {
    "toggl-track": {
      "command": "uvx",
      "args": ["toggl-track-mcp"],
      "env": {
        "TOGGL_API_TOKEN": "your-api-token-here"
      }
    }
  }
}
```

#### Using a local clone

```json
{
  "mcpServers": {
    "toggl-track": {
      "command": "uv",
      "args": ["--directory", "/path/to/TogglTrackMcp", "run", "toggl-track-mcp"],
      "env": {
        "TOGGL_API_TOKEN": "your-api-token-here"
      }
    }
  }
}
```

> Replace `/path/to/TogglTrackMcp` with the actual path where you cloned the repo. On Windows use double backslashes: `C:\\Users\\you\\TogglTrackMcp`.

After saving, **restart Claude Desktop**. You should see the Toggl Track tools appear in the tools menu (hammer icon).

### Claude Code

```bash
claude mcp add toggl-track -e TOGGL_API_TOKEN=your-api-token-here -- uvx toggl-track-mcp
```

### Cursor / Other MCP Clients

Use the same configuration pattern — set `command` to `uvx`, `args` to `["toggl-track-mcp"]`, and pass `TOGGL_API_TOKEN` in the environment.

### Running Standalone

```bash
export TOGGL_API_TOKEN="your-api-token-here"
uvx toggl-track-mcp
```

The server communicates over stdio using the MCP protocol — it's meant to be launched by an MCP client, not used directly in a terminal.

## Available Tools (35)

### Time Entries (8)

| Tool | Description |
|------|-------------|
| `list_time_entries` | List recent time entries, optionally filtered by date range (YYYY-MM-DD) |
| `get_current_time_entry` | Get the currently running timer, or confirms no timer is running |
| `get_time_entry` | Get a specific time entry by its ID |
| `start_time_entry` | Start a new live timer with optional description, project, tags |
| `stop_time_entry` | Stop a currently running timer |
| `create_time_entry` | Log a completed time entry for past work (start time + duration) |
| `update_time_entry` | Update any field on an existing time entry |
| `delete_time_entry` | Permanently delete a time entry |

### Projects (5)

| Tool | Description |
|------|-------------|
| `list_projects` | List all projects, optionally filtered by active status or name |
| `get_project` | Get full details for a specific project |
| `create_project` | Create a new project with optional client, color, billable settings |
| `update_project` | Update project name, client, color, status, or other fields |
| `delete_project` | Permanently delete a project |

### Clients (7)

| Tool | Description |
|------|-------------|
| `list_clients` | List clients, filterable by status (active/archived) or name |
| `get_client` | Get full details for a specific client |
| `create_client` | Create a new client with optional notes |
| `update_client` | Update client name or notes |
| `delete_client` | Permanently delete a client |
| `archive_client` | Soft-delete a client (and its projects) — can be restored later |
| `restore_client` | Restore a previously archived client |

### Tags (4)

| Tool | Description |
|------|-------------|
| `list_tags` | List all tags in the workspace |
| `create_tag` | Create a new tag |
| `update_tag` | Rename an existing tag |
| `delete_tag` | Permanently delete a tag |

### Tasks (5)

| Tool | Description |
|------|-------------|
| `list_tasks` | List tasks for a project (requires Toggl Pro) |
| `get_task` | Get details for a specific task |
| `create_task` | Create a task on a project, with optional time estimate |
| `update_task` | Update task name, estimate, or active status |
| `delete_task` | Permanently delete a task |

### Workspaces (3)

| Tool | Description |
|------|-------------|
| `list_workspaces` | List all workspaces you have access to |
| `get_workspace` | Get details for a specific workspace |
| `get_me` | Get your Toggl profile (email, timezone, default workspace) |

### Reports — Toggl Reports API v3 (3)

| Tool | Description |
|------|-------------|
| `get_summary_report` | Aggregated time summary grouped by project, client, or user |
| `search_detailed_report` | Search and filter individual time entries with full detail |
| `get_weekly_report` | Weekly breakdown showing hours per day |

## Example Prompts

Once connected, just talk naturally:

- **"Start a timer for code review on Project X"**
- **"What am I currently tracking?"**
- **"Stop my timer"**
- **"Log 2 hours for the meeting with Acme Corp yesterday at 2pm"**
- **"Show me a summary of my hours this week"**
- **"List all my projects and clients"**
- **"How much time did I spend on Project Y last month?"**
- **"Create a new tag called 'urgent'"**
- **"Archive the client Acme Corp"**

## Architecture

```
src/toggl_track_mcp/
├── server.py              # FastMCP instance + lifespan context
├── api/
│   ├── client.py          # Async HTTP client (auth, rate limiting, errors)
│   ├── time_entries.py    # Toggl API v9 endpoints per entity
│   ├── projects.py
│   ├── clients.py
│   ├── tags.py
│   ├── tasks.py
│   ├── workspaces.py
│   └── reports.py         # Reports API v3 endpoints
└── tools/
    ├── time_entries.py    # MCP tool definitions per entity
    ├── projects.py
    ├── clients.py
    ├── tags.py
    ├── tasks.py
    ├── workspaces.py
    └── reports.py
```

- **API layer**: Async `httpx` client with rate limiting (1 req/sec), typed exceptions, and automatic workspace detection
- **Tools layer**: `@mcp.tool()` decorators with LLM-optimized docstrings and graceful error messages
- **Lifespan pattern**: HTTP client is created once at startup and shared across all tool calls

## Development

```bash
# Clone
git clone https://github.com/dovahkaal/TogglTrackMcp.git
cd TogglTrackMcp

# Install with dev dependencies
uv sync --extra dev

# Run tests (43 tests, all mocked — no API token needed)
uv run pytest

# Run tests with verbose output
uv run pytest -v
```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests at [github.com/dovahkaal/TogglTrackMcp](https://github.com/dovahkaal/TogglTrackMcp).

## License

MIT
