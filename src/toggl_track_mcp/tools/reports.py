from __future__ import annotations

import json

from mcp.server.fastmcp import Context

from toggl_track_mcp.api import TogglAPIError, TogglAuthError
from toggl_track_mcp.api import reports as api
from toggl_track_mcp.server import mcp


@mcp.tool()
async def get_summary_report(
    ctx: Context,
    start_date: str,
    end_date: str,
    workspace_id: int | None = None,
    project_ids: list[int] | None = None,
    client_ids: list[int] | None = None,
    tag_ids: list[int] | None = None,
    billable: bool | None = None,
    grouping: str | None = None,
    sub_grouping: str | None = None,
) -> str:
    """Get a summary report of tracked time, grouped by project or client (Reports API v3).

    Args:
        start_date: Start date (YYYY-MM-DD).
        end_date: End date (YYYY-MM-DD).
        workspace_id: Workspace ID (auto-detected if not provided).
        project_ids: Filter by project IDs.
        client_ids: Filter by client IDs.
        tag_ids: Filter by tag IDs.
        billable: Filter by billable status.
        grouping: Primary grouping (e.g. "projects", "clients", "users").
        sub_grouping: Secondary grouping (e.g. "projects", "clients", "users", "time_entries").
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        result = await api.get_summary_report(
            toggl, wid, start_date, end_date,
            project_ids=project_ids,
            client_ids=client_ids,
            tag_ids=tag_ids,
            billable=billable,
            grouping=grouping,
            sub_grouping=sub_grouping,
        )
        return json.dumps(result, indent=2)
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def search_detailed_report(
    ctx: Context,
    start_date: str,
    end_date: str,
    workspace_id: int | None = None,
    description: str | None = None,
    project_ids: list[int] | None = None,
    client_ids: list[int] | None = None,
    tag_ids: list[int] | None = None,
    billable: bool | None = None,
    page_size: int = 50,
    first_row_number: int | None = None,
) -> str:
    """Search time entries with detailed breakdown using the Reports API v3.

    Args:
        start_date: Start date (YYYY-MM-DD).
        end_date: End date (YYYY-MM-DD).
        workspace_id: Workspace ID (auto-detected if not provided).
        description: Filter by description text.
        project_ids: Filter by project IDs.
        client_ids: Filter by client IDs.
        tag_ids: Filter by tag IDs.
        billable: Filter by billable status.
        page_size: Number of results per page (default 50, max 50).
        first_row_number: Row number to start from (for pagination).
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        result = await api.search_detailed_report(
            toggl, wid, start_date, end_date,
            description=description,
            project_ids=project_ids,
            client_ids=client_ids,
            tag_ids=tag_ids,
            billable=billable,
            page_size=page_size,
            first_row_number=first_row_number,
        )
        return json.dumps(result, indent=2)
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"


@mcp.tool()
async def get_weekly_report(
    ctx: Context,
    start_date: str,
    end_date: str,
    workspace_id: int | None = None,
    project_ids: list[int] | None = None,
    user_ids: list[int] | None = None,
    billable: bool | None = None,
) -> str:
    """Get a weekly report showing daily time breakdowns (Reports API v3).

    Args:
        start_date: Start date (YYYY-MM-DD).
        end_date: End date (YYYY-MM-DD).
        workspace_id: Workspace ID (auto-detected if not provided).
        project_ids: Filter by project IDs.
        user_ids: Filter by user IDs.
        billable: Filter by billable status.
    """
    try:
        toggl = ctx.request_context.lifespan_context.toggl
        wid = workspace_id or await toggl.get_default_workspace_id()
        result = await api.get_weekly_report(
            toggl, wid, start_date, end_date,
            project_ids=project_ids,
            user_ids=user_ids,
            billable=billable,
        )
        return json.dumps(result, indent=2)
    except TogglAuthError:
        return "Error: Invalid API token. Check TOGGL_API_TOKEN."
    except TogglAPIError as e:
        return f"Error: Toggl API returned {e.status_code}: {e.message}"
