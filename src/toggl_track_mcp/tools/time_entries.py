from __future__ import annotations

import json
from datetime import datetime, timezone

from mcp.server.fastmcp import Context

from toggl_track_mcp.api import TogglAPIError, TogglAuthError, TogglNotFoundError
from toggl_track_mcp.api import time_entries as api
from toggl_track_mcp.server import mcp


@mcp.tool()
async def list_time_entries(
    ctx: Context,
    start_date: str | None = None,
    end_date: str | None = None,
) -> str:
    """List recent time entries for the authenticated user.

    Args:
        start_date: Filter start date (YYYY-MM-DD). Defaults to ~9 days ago.
        end_date: Filter end date (YYYY-MM-DD). Defaults to today.
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        result = await api.list_time_entries(toggl, start_date, end_date)
        return json.dumps(result, indent=2)
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def get_current_time_entry(ctx: Context) -> str:
    """Get the currently running time entry, or null if no timer is running."""
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        result = await api.get_current_time_entry(toggl)
        if result is None:
            return "No timer is currently running."
        return json.dumps(result, indent=2)
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def get_time_entry(ctx: Context, time_entry_id: int) -> str:
    """Get a specific time entry by its ID.

    Args:
        time_entry_id: The ID of the time entry to retrieve.
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        result = await api.get_time_entry(toggl, time_entry_id)
        return json.dumps(result, indent=2)
    except TogglNotFoundError:
        return f"Error: Time entry {time_entry_id} not found."
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def start_time_entry(
    ctx: Context,
    description: str | None = None,
    project_id: int | None = None,
    task_id: int | None = None,
    tags: list[str] | None = None,
    billable: bool = False,
    workspace_id: int | None = None,
) -> str:
    """Start a new timer (running time entry).

    Args:
        description: What you're working on.
        project_id: Toggl project ID to associate with.
        task_id: Toggl task ID to associate with.
        tags: List of tag names to apply.
        billable: Whether this time is billable.
        workspace_id: Workspace ID (auto-detected if not provided).
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        now = datetime.now(timezone.utc).isoformat()
        result = await api.create_time_entry(
            toggl,
            workspace_id=wid,
            start=now,
            duration=-1,
            description=description,
            project_id=project_id,
            task_id=task_id,
            billable=billable,
            tags=tags,
        )
        return json.dumps(result, indent=2)
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def stop_time_entry(
    ctx: Context,
    time_entry_id: int,
    workspace_id: int | None = None,
) -> str:
    """Stop a currently running time entry.

    Args:
        time_entry_id: The ID of the running time entry to stop.
        workspace_id: Workspace ID (auto-detected if not provided).
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        result = await api.stop_time_entry(toggl, wid, time_entry_id)
        return json.dumps(result, indent=2)
    except TogglNotFoundError:
        return f"Error: Time entry {time_entry_id} not found or not running."
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def create_time_entry(
    ctx: Context,
    start: str,
    duration: int,
    description: str | None = None,
    project_id: int | None = None,
    task_id: int | None = None,
    tags: list[str] | None = None,
    billable: bool = False,
    workspace_id: int | None = None,
) -> str:
    """Create a completed time entry (log past time).

    Args:
        start: Start time in ISO 8601 format (e.g. 2024-01-15T09:00:00Z).
        duration: Duration in seconds.
        description: What was worked on.
        project_id: Toggl project ID.
        task_id: Toggl task ID.
        tags: List of tag names.
        billable: Whether this time is billable.
        workspace_id: Workspace ID (auto-detected if not provided).
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        result = await api.create_time_entry(
            toggl,
            workspace_id=wid,
            start=start,
            duration=duration,
            description=description,
            project_id=project_id,
            task_id=task_id,
            billable=billable,
            tags=tags,
        )
        return json.dumps(result, indent=2)
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def update_time_entry(
    ctx: Context,
    time_entry_id: int,
    workspace_id: int | None = None,
    description: str | None = None,
    project_id: int | None = None,
    task_id: int | None = None,
    tags: list[str] | None = None,
    billable: bool | None = None,
    start: str | None = None,
    stop: str | None = None,
    duration: int | None = None,
) -> str:
    """Update fields on an existing time entry.

    Args:
        time_entry_id: The ID of the time entry to update.
        workspace_id: Workspace ID (auto-detected if not provided).
        description: New description.
        project_id: New project ID.
        task_id: New task ID.
        tags: New list of tag names (replaces existing tags).
        billable: New billable status.
        start: New start time (ISO 8601).
        stop: New stop time (ISO 8601).
        duration: New duration in seconds.
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        fields: dict = {}
        if description is not None:
            fields["description"] = description
        if project_id is not None:
            fields["project_id"] = project_id
        if task_id is not None:
            fields["task_id"] = task_id
        if tags is not None:
            fields["tags"] = tags
        if billable is not None:
            fields["billable"] = billable
        if start is not None:
            fields["start"] = start
        if stop is not None:
            fields["stop"] = stop
        if duration is not None:
            fields["duration"] = duration
        result = await api.update_time_entry(
            toggl, wid, time_entry_id, **fields
        )
        return json.dumps(result, indent=2)
    except TogglNotFoundError:
        return f"Error: Time entry {time_entry_id} not found."
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def delete_time_entry(
    ctx: Context,
    time_entry_id: int,
    workspace_id: int | None = None,
) -> str:
    """Delete a time entry permanently.

    Args:
        time_entry_id: The ID of the time entry to delete.
        workspace_id: Workspace ID (auto-detected if not provided).
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        await api.delete_time_entry(toggl, wid, time_entry_id)
        return f"Time entry {time_entry_id} deleted successfully."
    except TogglNotFoundError:
        return f"Error: Time entry {time_entry_id} not found."
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"
