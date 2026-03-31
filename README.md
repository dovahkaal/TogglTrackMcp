# toggl-track-mcp

MCP server for Toggl Track — full CRUD for time entries, projects, clients, tags, tasks, and Reports API v3.

## Quick Start

### Install

```bash
# Using uvx (no install needed)
uvx toggl-track-mcp

# Or install with pip
pip install toggl-track-mcp
```

### Configure

Set your Toggl API token (get it from https://track.toggl.com/profile):

```bash
export TOGGL_API_TOKEN="your-api-token"
```

Optionally set a default workspace:

```bash
export TOGGL_WORKSPACE_ID="your-workspace-id"
```

### Claude Desktop Configuration

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "toggl-track": {
      "command": "uvx",
      "args": ["toggl-track-mcp"],
      "env": {
        "TOGGL_API_TOKEN": "your-api-token"
      }
    }
  }
}
```

### Claude Code Configuration

```bash
claude mcp add toggl-track -- uvx toggl-track-mcp
```

Then set the env var `TOGGL_API_TOKEN` in your shell.

## Available Tools (35)

### Time Entries (8)

| Tool | Description |
|------|-------------|
| `list_time_entries` | List recent time entries, optionally filtered by date range |
| `get_current_time_entry` | Get the currently running timer |
| `get_time_entry` | Get a specific time entry by ID |
| `start_time_entry` | Start a new timer |
| `stop_time_entry` | Stop a running timer |
| `create_time_entry` | Log a completed time entry (past time) |
| `update_time_entry` | Update fields on an existing time entry |
| `delete_time_entry` | Delete a time entry |

### Projects (5)

| Tool | Description |
|------|-------------|
| `list_projects` | List projects, optionally filtered by status or name |
| `get_project` | Get project details |
| `create_project` | Create a new project |
| `update_project` | Update project fields |
| `delete_project` | Delete a project |

### Clients (7)

| Tool | Description |
|------|-------------|
| `list_clients` | List clients, optionally filtered by status or name |
| `get_client` | Get client details |
| `create_client` | Create a new client |
| `update_client` | Update client fields |
| `delete_client` | Delete a client permanently |
| `archive_client` | Archive a client (soft delete) |
| `restore_client` | Restore an archived client |

### Tags (4)

| Tool | Description |
|------|-------------|
| `list_tags` | List all tags in workspace |
| `create_tag` | Create a new tag |
| `update_tag` | Rename a tag |
| `delete_tag` | Delete a tag |

### Tasks (5)

| Tool | Description |
|------|-------------|
| `list_tasks` | List tasks for a project (Pro only) |
| `get_task` | Get task details |
| `create_task` | Create a new task on a project |
| `update_task` | Update task fields |
| `delete_task` | Delete a task |

### Workspaces (3)

| Tool | Description |
|------|-------------|
| `list_workspaces` | List all accessible workspaces |
| `get_workspace` | Get workspace details |
| `get_me` | Get authenticated user profile |

### Reports (3)

| Tool | Description |
|------|-------------|
| `get_summary_report` | Summary report grouped by project/client (Reports API v3) |
| `search_detailed_report` | Detailed time entry search with filters (Reports API v3) |
| `get_weekly_report` | Weekly report with daily breakdowns (Reports API v3) |

## Example Prompts

- "Start a timer for code review on Project X"
- "What am I currently tracking?"
- "Stop my current timer"
- "Show me a summary of hours this week"
- "List all projects in my workspace"
- "Create a new client called Acme Corp"
- "How much time did I spend on Project Y last month?"

## Development

```bash
# Clone and install
git clone https://github.com/youruser/toggl-track-mcp.git
cd toggl-track-mcp
uv sync --extra dev

# Run tests
uv run pytest

# Run the server locally
TOGGL_API_TOKEN=your-token uv run toggl-track-mcp
```

## License

MIT
