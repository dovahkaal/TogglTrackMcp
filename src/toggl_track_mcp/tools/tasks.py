from __future__ import annotations

import json

from mcp.server.fastmcp import Context

from toggl_track_mcp.api import TogglAPIError, TogglAuthError, TogglNotFoundError
from toggl_track_mcp.api import tasks as api
from toggl_track_mcp.server import mcp


@mcp.tool()
async def list_tasks(
    ctx: Context,
    project_id: int,
    workspace_id: int | None = None,
) -> str:
    """List tasks for a project. Requires Toggl Pro workspace.

    Args:
        project_id: The project ID to list tasks for.
        workspace_id: Workspace ID (auto-detected if not provided).
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        result = await api.list_tasks(toggl, wid, project_id)
        return json.dumps(result, indent=2)
    except TogglNotFoundError:
        return f"Error: Project {project_id} not found."
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        if e.status_code == 402:
            return "Error: Tasks require a Toggl Pro workspace."
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def get_task(
    ctx: Context,
    project_id: int,
    task_id: int,
    workspace_id: int | None = None,
) -> str:
    """Get a specific task by ID. Requires Toggl Pro workspace.

    Args:
        project_id: The project ID the task belongs to.
        task_id: The task ID.
        workspace_id: Workspace ID (auto-detected if not provided).
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        result = await api.get_task(toggl, wid, project_id, task_id)
        return json.dumps(result, indent=2)
    except TogglNotFoundError:
        return f"Error: Task {task_id} not found in project {project_id}."
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        if e.status_code == 402:
            return "Error: Tasks require a Toggl Pro workspace."
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def create_task(
    ctx: Context,
    project_id: int,
    name: str,
    workspace_id: int | None = None,
    estimated_seconds: int | None = None,
    user_id: int | None = None,
) -> str:
    """Create a new task on a project. Requires Toggl Pro workspace.

    Args:
        project_id: The project ID to create the task in.
        name: Task name.
        workspace_id: Workspace ID (auto-detected if not provided).
        estimated_seconds: Estimated time in seconds.
        user_id: Assign the task to a specific user.
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        result = await api.create_task(
            toggl, wid, project_id, name,
            estimated_seconds=estimated_seconds,
            user_id=user_id,
        )
        return json.dumps(result, indent=2)
    except TogglNotFoundError:
        return f"Error: Project {project_id} not found."
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        if e.status_code == 402:
            return "Error: Tasks require a Toggl Pro workspace."
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def update_task(
    ctx: Context,
    project_id: int,
    task_id: int,
    workspace_id: int | None = None,
    name: str | None = None,
    estimated_seconds: int | None = None,
    active: bool | None = None,
) -> str:
    """Update fields on an existing task. Requires Toggl Pro workspace.

    Args:
        project_id: The project ID the task belongs to.
        task_id: The task ID to update.
        workspace_id: Workspace ID (auto-detected if not provided).
        name: New task name.
        estimated_seconds: New estimated time in seconds.
        active: Set to false to mark task as done.
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        fields: dict = {}
        if name is not None:
            fields["name"] = name
        if estimated_seconds is not None:
            fields["estimated_seconds"] = estimated_seconds
        if active is not None:
            fields["active"] = active
        result = await api.update_task(
            toggl, wid, project_id, task_id, **fields
        )
        return json.dumps(result, indent=2)
    except TogglNotFoundError:
        return f"Error: Task {task_id} not found in project {project_id}."
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        if e.status_code == 402:
            return "Error: Tasks require a Toggl Pro workspace."
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def delete_task(
    ctx: Context,
    project_id: int,
    task_id: int,
    workspace_id: int | None = None,
) -> str:
    """Delete a task permanently. Requires Toggl Pro workspace.

    Args:
        project_id: The project ID the task belongs to.
        task_id: The task ID to delete.
        workspace_id: Workspace ID (auto-detected if not provided).
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        await api.delete_task(toggl, wid, project_id, task_id)
        return f"Task {task_id} deleted successfully."
    except TogglNotFoundError:
        return f"Error: Task {task_id} not found in project {project_id}."
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        if e.status_code == 402:
            return "Error: Tasks require a Toggl Pro workspace."
        return f"Error: Toggl API returned {e.status_code}: {e.message}"
