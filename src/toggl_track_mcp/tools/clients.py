from __future__ import annotations

import json

from mcp.server.fastmcp import Context

from toggl_track_mcp.api import TogglAPIError, TogglAuthError, TogglNotFoundError
from toggl_track_mcp.api import clients as api
from toggl_track_mcp.server import mcp


@mcp.tool()
async def list_clients(
    ctx: Context,
    workspace_id: int | None = None,
    status: str | None = None,
    name: str | None = None,
) -> str:
    """List clients in a Toggl workspace.

    Args:
        workspace_id: Workspace ID (auto-detected if not provided).
        status: Filter by status: "active", "archived", or "both". Defaults to active.
        name: Filter by client name (partial match).
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        result = await api.list_clients(toggl, wid, status=status, name=name)
        return json.dumps(result, indent=2)
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def get_client(
    ctx: Context,
    client_id: int,
    workspace_id: int | None = None,
) -> str:
    """Get details for a specific client.

    Args:
        client_id: The client ID.
        workspace_id: Workspace ID (auto-detected if not provided).
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        result = await api.get_client(toggl, wid, client_id)
        return json.dumps(result, indent=2)
    except TogglNotFoundError:
        return f"Error: Client {client_id} not found."
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def create_client(
    ctx: Context,
    name: str,
    workspace_id: int | None = None,
    notes: str | None = None,
) -> str:
    """Create a new client in a Toggl workspace.

    Args:
        name: Client name.
        workspace_id: Workspace ID (auto-detected if not provided).
        notes: Optional notes about the client.
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        result = await api.create_client(toggl, wid, name, notes=notes)
        return json.dumps(result, indent=2)
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def update_client(
    ctx: Context,
    client_id: int,
    workspace_id: int | None = None,
    name: str | None = None,
    notes: str | None = None,
) -> str:
    """Update fields on an existing client.

    Args:
        client_id: The client ID to update.
        workspace_id: Workspace ID (auto-detected if not provided).
        name: New client name.
        notes: New notes.
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        result = await api.update_client(
            toggl, wid, client_id, name=name, notes=notes
        )
        return json.dumps(result, indent=2)
    except TogglNotFoundError:
        return f"Error: Client {client_id} not found."
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def delete_client(
    ctx: Context,
    client_id: int,
    workspace_id: int | None = None,
) -> str:
    """Delete a client permanently.

    Args:
        client_id: The client ID to delete.
        workspace_id: Workspace ID (auto-detected if not provided).
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        await api.delete_client(toggl, wid, client_id)
        return f"Client {client_id} deleted successfully."
    except TogglNotFoundError:
        return f"Error: Client {client_id} not found."
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def archive_client(
    ctx: Context,
    client_id: int,
    workspace_id: int | None = None,
) -> str:
    """Archive a client (soft delete). This also archives associated projects.

    Args:
        client_id: The client ID to archive.
        workspace_id: Workspace ID (auto-detected if not provided).
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        result = await api.archive_client(toggl, wid, client_id)
        return json.dumps(result, indent=2) if result else f"Client {client_id} archived successfully."
    except TogglNotFoundError:
        return f"Error: Client {client_id} not found."
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def restore_client(
    ctx: Context,
    client_id: int,
    workspace_id: int | None = None,
) -> str:
    """Restore an archived client.

    Args:
        client_id: The client ID to restore.
        workspace_id: Workspace ID (auto-detected if not provided).
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        result = await api.restore_client(toggl, wid, client_id)
        return json.dumps(result, indent=2) if result else f"Client {client_id} restored successfully."
    except TogglNotFoundError:
        return f"Error: Client {client_id} not found."
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"
