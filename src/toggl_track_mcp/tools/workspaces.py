from __future__ import annotations

import json

from mcp.server.fastmcp import Context

from toggl_track_mcp.api import TogglAPIError, TogglAuthError, TogglNotFoundError
from toggl_track_mcp.api import workspaces as api
from toggl_track_mcp.server import mcp


@mcp.tool()
async def get_me(ctx: Context) -> str:
    """Get the authenticated Toggl user's profile, including default workspace ID, email, and timezone."""
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        result = await api.get_me(toggl)
        return json.dumps(result, indent=2)
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN environment variable."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def list_workspaces(ctx: Context) -> str:
    """List all Toggl workspaces accessible to the authenticated user."""
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        result = await api.list_workspaces(toggl)
        return json.dumps(result, indent=2)
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN environment variable."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def get_workspace(ctx: Context, workspace_id: int) -> str:
    """Get details for a specific Toggl workspace by ID."""
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        result = await api.get_workspace(toggl, workspace_id)
        return json.dumps(result, indent=2)
    except TogglNotFoundError:
        return f"Error: Workspace {workspace_id} not found."
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN environment variable."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"
