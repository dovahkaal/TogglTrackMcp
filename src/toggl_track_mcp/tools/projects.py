from __future__ import annotations

import json

from mcp.server.fastmcp import Context

from toggl_track_mcp.api import TogglAPIError, TogglAuthError, TogglNotFoundError
from toggl_track_mcp.api import projects as api
from toggl_track_mcp.server import mcp


@mcp.tool()
async def list_projects(
    ctx: Context,
    workspace_id: int | None = None,
    active: bool | None = None,
    name: str | None = None,
) -> str:
    """List projects in a Toggl workspace.

    Args:
        workspace_id: Workspace ID (auto-detected if not provided).
        active: Filter by active status (true/false). Returns all if omitted.
        name: Filter by project name (partial match).
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        result = await api.list_projects(toggl, wid, active=active, name=name)
        return json.dumps(result, indent=2)
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def get_project(
    ctx: Context,
    project_id: int,
    workspace_id: int | None = None,
) -> str:
    """Get details for a specific project.

    Args:
        project_id: The project ID.
        workspace_id: Workspace ID (auto-detected if not provided).
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        result = await api.get_project(toggl, wid, project_id)
        return json.dumps(result, indent=2)
    except TogglNotFoundError:
        return f"Error: Project {project_id} not found."
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def create_project(
    ctx: Context,
    name: str,
    workspace_id: int | None = None,
    client_id: int | None = None,
    color: str | None = None,
    billable: bool | None = None,
    is_private: bool | None = None,
    estimated_hours: int | None = None,
) -> str:
    """Create a new project in a Toggl workspace.

    Args:
        name: Project name.
        workspace_id: Workspace ID (auto-detected if not provided).
        client_id: Client ID to associate with.
        color: Project color hex code (e.g. "#FF0000").
        billable: Whether the project is billable.
        is_private: Whether the project is private.
        estimated_hours: Estimated hours for the project.
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        result = await api.create_project(
            toggl, wid, name,
            client_id=client_id,
            color=color,
            billable=billable,
            is_private=is_private,
            estimated_hours=estimated_hours,
        )
        return json.dumps(result, indent=2)
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def update_project(
    ctx: Context,
    project_id: int,
    workspace_id: int | None = None,
    name: str | None = None,
    client_id: int | None = None,
    color: str | None = None,
    billable: bool | None = None,
    is_private: bool | None = None,
    active: bool | None = None,
    estimated_hours: int | None = None,
) -> str:
    """Update fields on an existing project.

    Args:
        project_id: The project ID to update.
        workspace_id: Workspace ID (auto-detected if not provided).
        name: New project name.
        client_id: New client ID.
        color: New color hex code.
        billable: New billable status.
        is_private: New privacy setting.
        active: Set to false to archive the project.
        estimated_hours: New estimated hours.
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        fields: dict = {}
        if name is not None:
            fields["name"] = name
        if client_id is not None:
            fields["client_id"] = client_id
        if color is not None:
            fields["color"] = color
        if billable is not None:
            fields["billable"] = billable
        if is_private is not None:
            fields["is_private"] = is_private
        if active is not None:
            fields["active"] = active
        if estimated_hours is not None:
            fields["estimated_hours"] = estimated_hours
        result = await api.update_project(toggl, wid, project_id, **fields)
        return json.dumps(result, indent=2)
    except TogglNotFoundError:
        return f"Error: Project {project_id} not found."
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def delete_project(
    ctx: Context,
    project_id: int,
    workspace_id: int | None = None,
) -> str:
    """Delete a project permanently.

    Args:
        project_id: The project ID to delete.
        workspace_id: Workspace ID (auto-detected if not provided).
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        await api.delete_project(toggl, wid, project_id)
        return f"Project {project_id} deleted successfully."
    except TogglNotFoundError:
        return f"Error: Project {project_id} not found."
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"
