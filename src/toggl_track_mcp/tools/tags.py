from __future__ import annotations

import json

from mcp.server.fastmcp import Context

from toggl_track_mcp.api import TogglAPIError, TogglAuthError, TogglNotFoundError
from toggl_track_mcp.api import tags as api
from toggl_track_mcp.server import mcp


@mcp.tool()
async def list_tags(
    ctx: Context,
    workspace_id: int | None = None,
) -> str:
    """List all tags in a Toggl workspace.

    Args:
        workspace_id: Workspace ID (auto-detected if not provided).
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        result = await api.list_tags(toggl, wid)
        return json.dumps(result, indent=2)
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def create_tag(
    ctx: Context,
    name: str,
    workspace_id: int | None = None,
) -> str:
    """Create a new tag in a Toggl workspace.

    Args:
        name: Tag name.
        workspace_id: Workspace ID (auto-detected if not provided).
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        result = await api.create_tag(toggl, wid, name)
        return json.dumps(result, indent=2)
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def update_tag(
    ctx: Context,
    tag_id: int,
    name: str,
    workspace_id: int | None = None,
) -> str:
    """Rename a tag.

    Args:
        tag_id: The tag ID to update.
        name: New tag name.
        workspace_id: Workspace ID (auto-detected if not provided).
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        result = await api.update_tag(toggl, wid, tag_id, name)
        return json.dumps(result, indent=2)
    except TogglNotFoundError:
        return f"Error: Tag {tag_id} not found."
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def delete_tag(
    ctx: Context,
    tag_id: int,
    workspace_id: int | None = None,
) -> str:
    """Delete a tag permanently.

    Args:
        tag_id: The tag ID to delete.
        workspace_id: Workspace ID (auto-detected if not provided).
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        await api.delete_tag(toggl, wid, tag_id)
        return f"Tag {tag_id} deleted successfully."
    except TogglNotFoundError:
        return f"Error: Tag {tag_id} not found."
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"
